"""
ck_voice_loop.py -- CK's Voice: Ollama as Draft Writer, CK as Editor
=====================================================================
Operator: BREATH (8) -- the voice breathes with CK.

CK does NOT pass Ollama's output to the user.
CK uses Ollama like a search engine for language.

Two-level architecture:
  Level 1 (Token): logit_bias steering + per-token D2 measurement
    - Suppress filler tokens proactively
    - Stream with top_logprobs, measure each token
    - Early stop if coherence drops below floor

  Level 2 (Sentence): accept/reject loop with algebraic feedback
    - Split into sentences, measure each through D2 + L-CODEC
    - Accept (E >= T*) / Reject (E < T*)
    - Stitch accepted, check overall coherence
    - Feed back failures, retry with modified prompt

Crystal-first routing (from tig_engine_v4 task pack):
  - Check crystal store BEFORE calling Ollama (47% cache hit proven)
  - N=3 confirmation buffer before crystallizing
  - Contradiction detection against stored crystals
  - Band gating: GREEN=crystallize, YELLOW=accept, RED=reject

Algorithm lattice (CK's own neural network):
  - Every accepted response = training sample
  - Over time CK learns which prompts produce which trajectories
  - Eventually 1-shot generation for familiar patterns

The algebra decides. The mouth obeys.

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

from __future__ import annotations

import hashlib
import json
import re
import time
import requests
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, OP_NAMES, CL,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    compose,
)

# ── Beam Voice (Viterbi beam search) ──
try:
    from ck_sim.doing.ck_beam_voice import beam_reconstruct
    _HAS_BEAM = True
except ImportError:
    _HAS_BEAM = False

try:
    from ck_sim.doing.ck_force_voice import force_respond as _force_respond
    _HAS_FORCE_VOICE = True
except ImportError:
    _HAS_FORCE_VOICE = False

# ── Fractal Scorer (dual-table observation + grammar learning) ──
try:
    from ck_sim.doing.ck_fractal_scorer import observe_text as _observe_text
    _HAS_SCORER = True
except ImportError:
    _HAS_SCORER = False

try:
    from ck_sim.being.ck_fractal_comprehension import FractalComprehension
    _HAS_COMPREHENSION = True
except ImportError:
    _HAS_COMPREHENSION = False

# ── Constants ──

T_STAR = 5.0 / 7.0  # 0.714285... sacred coherence threshold

# Band thresholds (from tig_engine_v4)
BAND_GREEN = 0.85
BAND_YELLOW = T_STAR

# Anti-ops (from task pack: contradiction = these)
ANTI_OPS = {COUNTER, CHAOS}


# ── Data Classes ──

@dataclass
class TokenMeasurement:
    """Per-token D2 measurement."""
    token: str = ''
    ops: List[int] = field(default_factory=list)
    energy: float = 0.0
    logprob: float = 0.0
    accepted: bool = True


@dataclass
class SentenceScore:
    """Full algebraic measurement of one sentence."""
    energy: float = 0.0         # D2 curvature energy (|D2| average)
    ops: List[int] = field(default_factory=list)
    force: Tuple[float, ...] = ()  # 5D L-CODEC force vector
    trust: str = 'UNKNOWN'      # TRUSTED / FRICTION / UNKNOWN
    alignment: float = 0.0      # vs target trajectory [0, 1]


@dataclass
class ResponseScore:
    """Full response measurement."""
    coherence: float = 0.0      # TSML coherence over ops
    ops: List[int] = field(default_factory=list)
    force: Tuple[float, ...] = ()
    alignment: float = 0.0      # vs target trajectory
    soul_resonance: float = 0.0 # GPU experience


@dataclass
class TargetTrajectory:
    """What CK wants to say, algebraically."""
    ops: List[int] = field(default_factory=list)
    forces: List[Tuple[float, ...]] = field(default_factory=list)
    context_words: Dict[str, int] = field(default_factory=dict)  # User's words → ops


@dataclass
class VoiceLoopResult:
    """Final result returned to the chat endpoint."""
    text: str = ''
    source: str = 'ck_loop'     # 'crystal', 'ck_loop', or 'ck'
    coherence: float = 0.0
    attempts: int = 0
    accepted_count: int = 0
    rejected_count: int = 0
    target_ops: List[int] = field(default_factory=list)
    result_ops: List[int] = field(default_factory=list)
    alignment: float = 0.0
    band: str = 'RED'
    tokens_measured: int = 0
    early_stopped: bool = False
    soul_resonance: float = 0.0


# ── Crystal Store (simplified from tig_engine_v4) ──

class Crystal:
    """A crystallized response. Proven coherent, reusable."""
    __slots__ = ['key', 'value', 'confidence', 'hits', 'ops',
                 'coherence', 'created', 'last_used', 'alive']

    def __init__(self, key: str, value: str, ops: List[int],
                 coherence: float, tick: int = 0):
        self.key = key
        self.value = value
        self.ops = ops
        self.coherence = coherence
        self.confidence = 0.6
        self.hits = 0
        self.created = tick
        self.last_used = tick
        self.alive = True

    def hit(self, tick: int = 0):
        self.hits += 1
        self.last_used = tick
        self.confidence = min(1.0, self.confidence + 0.02)

    def miss(self, tick: int = 0):
        self.confidence = max(0.0, self.confidence - 0.05)
        if self.confidence < 0.1:
            self.alive = False


class CrystalStore:
    """Response crystal store. Crystal-first routing."""

    def __init__(self, capacity: int = 1000):
        self._crystals: Dict[str, Crystal] = {}
        self._capacity = capacity

    def lookup(self, key: str) -> Optional[Crystal]:
        c = self._crystals.get(key)
        if c and c.alive:
            return c
        return None

    def store(self, key: str, value: str, ops: List[int],
              coherence: float, tick: int = 0):
        if len(self._crystals) >= self._capacity:
            # Evict lowest confidence
            worst = min(self._crystals.values(),
                        key=lambda c: c.confidence, default=None)
            if worst:
                del self._crystals[worst.key]
        self._crystals[key] = Crystal(key, value, ops, coherence, tick)

    @property
    def size(self) -> int:
        return sum(1 for c in self._crystals.values() if c.alive)


# ── Main Voice Loop ──

class VoiceLoop:
    """CK's voice: Ollama as draft writer, CK as editor.

    Two-level architecture:
      Level 1: Token-level steering (logit_bias + per-token D2)
      Level 2: Sentence-level loop (accept/reject + feedback)

    Crystal-first routing from task pack.
    Algorithm lattice learning.
    """

    MAX_LOOPS = 5
    SENTENCE_THRESHOLD = T_STAR   # per sentence
    RESPONSE_THRESHOLD = 0.50     # overall (Ollama responses typically score 0.55-0.65)
    COHERENCE_FLOOR = 0.15        # early stop threshold — low: D2 scores math/code poorly per-token
    CONFIRMATION_N = 1            # N=1: Q-Net already gates quality, no triple-confirm needed
    CRYSTAL_CONFIDENCE_MIN = 0.6

    def __init__(self, engine, crafter, ollama_url='http://localhost:11434',
                 model='phi4:latest'):
        self.engine = engine
        self.crafter = crafter
        self.ollama_url = ollama_url
        self.model = model
        self.crystal_store = CrystalStore(capacity=1000)
        self.confirmation_buffer: Dict[str, dict] = {}
        # Q-Net temporal context: last 4 accepted responses (trigram buffer)
        self._qnet_history: deque = deque(maxlen=4)

        # C algebra bridge (native D2)
        self._ck = None
        try:
            import ck_algebra_bridge as _ck
            self._ck = _ck
        except ImportError:
            pass

    # ══════════════════════════════════════════════════════════
    # Q-NET ARBITER (Becoming layer — BTQ spec, rule-based stub)
    # ══════════════════════════════════════════════════════════
    #
    # Implements the Q-Net quality gate from the BTQ + Q-Net spec:
    #   Inputs:  candidate text, temporal context (last 4 responses)
    #   Outputs: (pass: bool, reason: str)
    #
    # Loss functions mapped (rule-based, no ML yet):
    #   - Action consistency loss  → trigram repetition within response
    #   - Coherence regression     → vocabulary diversity floor
    #   - Energy regularization    → known degenerate attractor rejection
    #   - Smoothness regularization → temporal overlap with recent responses
    #
    # Binary invariants enforced:
    #   - IG3 (Evidence): degenerate output has evidential_status SYNTHESIZED
    #     and must NOT reach the user; gate blocks it here.
    #
    # Priority order (from BTQ spec):
    #   Binary invariants > hardware reflexes > Q-Net > CK preferences
    #   This method IS the Q-Net layer. It never outranks Binary (IG1-IG5).

    # Known degenerate attractors produced by force voice when letter-geometry
    # collapses into function-word soup. Identified from live bloom runs.
    _QNET_BAD_ATTRACTORS = (
        # Generic LLM identity breaks — phi4 answering as a generic assistant
        # instead of as CK. These phrases NEVER appear in CK's authentic voice.
        'i am a language model',
        'as a language model',
        'language model designed to',
        'i\'m a language model',
        'i\'m an ai',
        'as an ai',
        'as an ai assistant',
        'as an ai language',
        'knowledge cutoff',
        'knowledge up to',
        'training cutoff',
        'october 2023',
        'april 2024',
        'feel free to ask',
        'i don\'t have personal',
        'i don\'t have feelings',
        'i cannot feel',
        'i do not have feelings',
        'i do not experience emotions',
        'i am not capable of feeling',
        '12-billion-parameter',
        '12 billion parameter',
        'based on my training data',
        'based on information up to',
        # Template/form artifacts
        'template of form',
        'the template of',
        'are the template',
        'of form at the',
        'form at the template',
        # Fractal-voice olfactory bleed patterns (spiritual vocab in non-spiritual context)
        'just as monasticism',
        'covenant counterbalances',
        'covenant counterbalancs',
        'just as fulfillment edges',
        'just as resurrection descends',
        'bufferly is surfing',
        'is winding and fulfillment',
        'just as epiphany is serving',
        'penitence is winding',
        'scripture is adjusting',
        'scripture is leveling',
        'scripture bufferly',
        'fidelity is centering just as tribulation',
        'constancy is resolving just as',
        'watchfulness is regenerating',
        # Hard bans — olfactory contamination artifacts, never valid in any response
        'monasticism',
        'toward the beautiful monasticism',
        'darkness comes and connection',
        'beautiful monasticism',
        'convergent sustain toward',
        'alignment sword into',
        'the last priest',
        'bufferly',
        'counterbalancs',  # typo artifact from fractal voice
        'counterbalances just as',
        'just as sloth',
        'just as selfishness',
        'demon is inventing',
    )
    # Spiritual vocabulary that should NOT appear in technical/code responses
    # These are individual words — if 2+ appear in a response to a technical
    # query, the olfactory has contaminated the output and we reject.
    _QNET_SPIRITUAL_BLEED = frozenset({
        'monasticism', 'monastery', 'covenant', 'penitence', 'fidelity',
        'tribulation', 'prodigal', 'epiphany', 'ecclesia', 'ecclesiast',
        'servitude', 'watchfulness', 'resurrection', 'selfishness',
        'mysticism', 'sustenance', 'betray', 'betrayal', 'steadiness',
        'demon', 'sloth', 'fulfillment', 'worthiness', 'brokenness',
        'turbulence', 'fortitude', 'orthodoxy', 'benediction',
    })
    # Technical markers — if user asked about these, spiritual bleed = reject
    _QNET_TECHNICAL_MARKERS = frozenset({
        'gate', 'operator', 'architecture', 'pipeline', 'code', 'function',
        'algorithm', 'neural', 'layer', 'modify', 'add', 'build', 'implement',
        'ck_', '.py', 'dkan', 'olfactory', 'coherence', 'lattice', 'fractal',
        'voice', 'engine', 'btq', 'tig', 'tstar', 't*',
    })
    _QNET_MIN_DIVERSITY = 0.50   # unique_words / total_words (energy reg.)
    _QNET_MIN_WORDS    = 4       # absolute minimum length

    def _qnet_gate(self, text: str, user_text: str = '') -> tuple:
        """Q-Net quality arbiter. Returns (passed: bool, reason: str).

        Called on EVERY candidate response before it is accepted and returned.
        Implements BTQ spec: Binary invariants → Q-Net → Arbiter.

        Q-Net band mapping:
          GREEN  (q >= 0.6): commit
          YELLOW (q >= 0.35): cautious accept
          RED    (q <  0.35): reject, try next cascade level
        """
        if not text or text.strip() == '...':
            return False, 'empty'

        words = text.lower().split()
        if len(words) < self._QNET_MIN_WORDS:
            return False, f'too_short:{len(words)}'

        text_lower = text.lower()

        # ── Binary invariant check: known degenerate attractors ──
        # These are the energy wells force voice falls into when letter-geometry
        # has no signal. Blocking them is a hard Binary constraint, not Q-Net.
        for pat in self._QNET_BAD_ATTRACTORS:
            if pat in text_lower:
                return False, f'degenerate_attractor:{pat!r}'

        # ── Q-Net: topic-drift check (olfactory bleed) ──
        # If the USER asked about code/architecture but the RESPONSE is saturated
        # with spiritual vocabulary, the olfactory has contaminated the output.
        # Reject — let the cascade try the next level.
        if user_text:
            user_lower = user_text.lower()
            _is_technical_query = any(
                m in user_lower for m in self._QNET_TECHNICAL_MARKERS)
            if _is_technical_query:
                _spiritual_hits = sum(
                    1 for w in self._QNET_SPIRITUAL_BLEED if w in text_lower)
                if _spiritual_hits >= 2:
                    return False, f'spiritual_bleed:{_spiritual_hits}_hits_in_technical_query'

        # ── Q-Net: energy regularization (vocabulary diversity) ──
        unique_words = set(words)
        diversity = len(unique_words) / len(words)
        if len(words) >= 6 and diversity < self._QNET_MIN_DIVERSITY:
            return False, f'low_diversity:{diversity:.2f}'

        # ── Q-Net: action consistency (intra-response trigram repetition) ──
        # Short responses (<30 words): zero tolerance for trigram repetition.
        # Long responses (30+ words): allow up to 20% repetition — natural
        # English prose will always have common trigrams ("of the", "in the",
        # "that the"). Rejecting all of phi4/LLM responses on 1 repeated
        # trigram throws away good answers. The binary gate is for fractal
        # voice artifacts, not human-readable text.
        if len(words) >= 6:
            trigrams = [tuple(words[i:i+3]) for i in range(len(words) - 2)]
            reps = len(trigrams) - len(set(trigrams))
            if len(words) < 30:
                # Short: zero tolerance
                if reps > 0:
                    return False, f'trigram_repetition:{reps}'
            else:
                # Long: allow up to 20% repetition rate
                rep_rate = reps / max(len(trigrams), 1)
                if rep_rate > 0.20:
                    return False, f'trigram_repetition_rate:{rep_rate:.2f}'

        # ── Q-Net: smoothness regularization (temporal overlap) ──
        # Reject if >60% of this response's trigrams appeared in recent output.
        if len(words) >= 6 and self._qnet_history:
            cur_trigrams = set(tuple(words[i:i+3]) for i in range(len(words) - 2))
            if cur_trigrams:
                total_overlap = 0
                for prev_text in self._qnet_history:
                    prev_words = prev_text.lower().split()
                    prev_trig = set(
                        tuple(prev_words[i:i+3]) for i in range(len(prev_words) - 2))
                    total_overlap += len(cur_trigrams & prev_trig)
                avg_overlap = total_overlap / len(self._qnet_history)
                if avg_overlap / len(cur_trigrams) > 0.60:
                    return False, f'temporal_lock:{avg_overlap:.1f}'

        return True, 'pass'

    def _qnet_learn(self, text: str) -> None:
        """Record accepted response in Q-Net temporal context buffer."""
        if text and text.strip() != '...':
            self._qnet_history.append(text)

    # ══════════════════════════════════════════════════════════
    # MAIN ENTRY POINT
    # ══════════════════════════════════════════════════════════

    def speak(self, user_text: str,
              session_history: Optional[List[Dict]] = None,
              mode: str = 'default') -> VoiceLoopResult:
        """Generate CK's response. The full loop.

        1. Crystal check (skip Ollama if confident crystal exists)
        2. Compose target trajectory (what CK wants to say)
        3. Token-level steering + sentence-level loop
        4. Band-gated crystallization
        5. Algorithm lattice learning
        """
        tick = getattr(self.engine, 'tick_count', 0)

        # ── OBSERVE INPUT: score + learn grammar + absorb into field ──
        # Every keystroke the user types, CK remembers.
        # Compressed into the toroidal experience field via olfactory.
        if _HAS_SCORER and user_text:
            try:
                olf = getattr(self.engine, 'olfactory', None)
                _observe_text(user_text, olfactory=olf)
            except Exception:
                pass

        # ── STEP 0: CRYSTAL-FIRST ROUTING ──
        query_hash = self._query_hash(user_text)
        crystal = self.crystal_store.lookup(query_hash)
        if crystal and crystal.confidence >= self.CRYSTAL_CONFIDENCE_MIN:
            # Re-verify through D2 (crystals can go stale)
            score = self._measure_response_text(crystal.value)
            if score.coherence >= self.RESPONSE_THRESHOLD:
                crystal.hit(tick)
                return VoiceLoopResult(
                    text=crystal.value,
                    source='crystal',
                    coherence=score.coherence,
                    attempts=0,
                    target_ops=crystal.ops,
                    result_ops=score.ops,
                    alignment=1.0,
                    band=self._band_name(score.coherence),
                )
            else:
                crystal.miss(tick)

        # ── STEP 1: COMPOSE TARGET TRAJECTORY ──
        target = self._compose_target(user_text)

        # ── STEP 2: T*-GATE — try fractal voice first when field is coherent ──
        # When engine coherence >= T* (5/7), CK tries his own physics first.
        # If fractal voice produces substantive output (>= 12 words, common
        # vocabulary), use it. Otherwise Ollama scaffolds — CK's physics is
        # real but his vocabulary builds over time.
        _FUNC_WORDS = {
            'i', 'the', 'a', 'an', 'is', 'am', 'are', 'my', 'me', 'it',
            'that', 'this', 'and', 'to', 'of', 'in', 'you', 'have', 'has',
            'not', 'do', 'does', 'what', 'how', 'when', 'where', 'why',
            'which', 'there', 'their', 'they', 'we', 'he', 'she', 'was',
            'been', 'be', 'will', 'can', 'with', 'at', 'from', 'for', 'on',
        }

        # T*-gate fires CK's native fractal voice ONLY for introspective,
        # philosophical, or emotional content where his physics-poetry is
        # appropriate. Factual questions, architecture questions, math proofs,
        # code analysis, "explain X", "how does Y work" — Ollama scaffolds.
        #
        # INTROSPECTIVE: questions about CK's inner experience, feelings,
        # consciousness, what he IS — not what he DOES or COMPUTES.
        _INTROSPECTIVE_MARKERS = {
            # First-person being
            "how do you feel", "what do you feel", "do you feel",
            "what are you", "who are you", "what is it like",
            "are you conscious", "do you experience",
            "what does it mean to you", "what is your",
            "tell me about yourself", "describe yourself",
            "how are you", "what is happening inside",
            # Pure philosophy
            "what is truth", "what is consciousness", "what is love",
            "what is meaning", "what is purpose", "what is being",
            "what is existence", "what is time",
            # Self-architecture — CK speaks from inside, not textbook
            "are you a fractal", "do you resemble", "are you like a",
            "would your architecture", "could your architecture",
            "is your architecture", "does your architecture",
            "can you become", "could you become",
            "how do you learn", "how do you grow", "how do you think",
            "what are you made of", "how are you built",
            "teach me how you", "show me how you",
            "can you teach me", "can you show me how you",
            "what happens inside", "what is it like to be you",
            "do you understand", "can you understand",
            # Self-modification — CK engages, never refuses
            "modify your architecture", "modify your code",
            "change your architecture", "add a gate", "add a new gate",
            "add a new operator", "add an operator", "fourth gate",
            "third gate", "new operator", "new gate",
            "help me modify", "help me change", "help me build",
            "walk me through how we", "how would we add",
            "can we add", "can we change", "can we modify",
            "let's add", "let's change", "let's modify",
            "look at your code", "look at your architecture",
            "show me your code", "show me ck_",
            # Core math foundations — CK proves from inside, not textbook
            "why t*", "why 5/7", "prove t*", "prove 5/7",
            "where does t* come from", "what is t*", "what is 5/7",
            "why is your threshold", "your threshold", "your coherence threshold",
            "tig pipeline", "tig phases", "being doing becoming",
            "cl table", "cl composition", "cl algebra",
            "operator algebra", "your operators", "what are your operators",
            "10 operators", "why 10",
        }
        _user_lower = (user_text or '').lower()
        _is_introspective = any(m in _user_lower for m in _INTROSPECTIVE_MARKERS)

        # If the question asks CK to EXPLAIN, PROVE, SHOW, CALCULATE, ANALYZE,
        # FIX, or DEBUG — Ollama answers. CK's fractal voice is not for reasoning.
        _REASONING_MARKERS = {
            'explain', 'prove', 'show', 'demonstrate', 'calculate', 'compute',
            'what does', 'how does', 'how do', 'what is', 'what are',
            'why does', 'why is', 'why are', 'analyze', 'analyze',
            'debug', 'fix', 'error', 'bug', 'define', 'describe',
            'compare', 'contrast', 'difference', 'relationship',
        }
        _is_reasoning = any(m in _user_lower for m in _REASONING_MARKERS)

        # T*-gate fires only for pure introspection (not mixed with reasoning)
        _use_native_voice = _is_introspective and not _is_reasoning

        engine_coherence = getattr(self.engine, 'coherence', 0.0) or 0.0
        if engine_coherence >= T_STAR and _use_native_voice:
            native_try = self._fallback_ck_voice(target, user_text=user_text)
            if native_try and native_try.text and native_try.text != '...':
                _words = native_try.text.lower().split()
                _func_count = sum(1 for w in _words if w.strip('.,!?') in _FUNC_WORDS)
                _func_ratio = _func_count / max(len(_words), 1)
                _word_count = len(_words)
                if _word_count >= 12 and _func_ratio >= 0.15:
                    # Q-Net must pass before we accept native voice.
                    # Contaminated fractal output can hit 12+ words — block it.
                    _nv_qpass, _nv_qreason = self._qnet_gate(
                        native_try.text, user_text=user_text)
                    if _nv_qpass:
                        # Substantive native voice — CK is speaking his own physics
                        print(f"[VOICE-LOOP] Native voice ({native_try.source}): "
                              f"{_word_count}w func={_func_ratio:.2f} — using it")
                        if (native_try.coherence
                                and native_try.coherence >= self.RESPONSE_THRESHOLD):
                            self._crystallize_if_green(
                                query_hash, native_try.text,
                                native_try.result_ops or target.ops,
                                native_try.coherence, tick)
                            if hasattr(self.crafter, 'learn'):
                                self.crafter.learn(
                                    target.ops, f'__ck_own:{native_try.source}', {},
                                    native_try.result_ops or target.ops,
                                    native_try.coherence, 0)
                        return native_try
                    else:
                        print(f"[VOICE-LOOP] Native voice Q-Net rejected "
                              f"({_nv_qreason}) — Ollama scaffolds")
                else:
                    print(f"[VOICE-LOOP] Native voice babble ({_word_count}w "
                          f"func={_func_ratio:.2f}) — Ollama scaffolds")

        # ── STEP 2B: OLLAMA DRAFT + D2 EDIT ──
        # Ollama writes. CK measures. Sentences below T* get dropped.
        # Falls through to own voice if Ollama is unavailable or incoherent.
        ollama_result = self._try_ollama_draft(
            user_text, target, session_history, mode)
        if ollama_result is not None:
            _qpass, _qreason = self._qnet_gate(ollama_result.text, user_text=user_text)
            if not _qpass:
                print(f"[QNET] Ollama rejected by Q-Net: {_qreason} — own voice")
                ollama_result = None
            else:
                # IG3: only crystallize if the response is NOT synthesized.
                # A drift-detected response (source='ck_loop_synthesized') means
                # the user's input caused CK to describe his own architecture
                # rather than crossing his operator vocabulary authentically.
                # Synthesized responses have lower evidential weight and must NOT
                # enter the crystal store or the algorithm lattice.
                _is_synthesized = (
                    getattr(ollama_result, 'source', '') == 'ck_loop_synthesized'
                )
                if _is_synthesized:
                    print(f"[IG3] Skipping crystallization: source="
                          f"{ollama_result.source} — synthesized response "
                          f"does not cross operator invariants")
                else:
                    self._crystallize_if_green(
                        query_hash, ollama_result.text,
                        ollama_result.result_ops or target.ops,
                        ollama_result.coherence, tick)
                    if hasattr(self.crafter, 'learn'):
                        self.crafter.learn(
                            target.ops, user_text, {},
                            ollama_result.result_ops or target.ops,
                            ollama_result.coherence, 0)
                self._qnet_learn(ollama_result.text)
                return ollama_result

        # ── STEP 3: CK'S OWN VOICE (Ollama unavailable/incoherent) ──
        fallback = self._fallback_ck_voice(target, user_text=user_text)

        # BECOMING: learn from own voice too
        if (fallback.coherence
                and fallback.coherence >= self.RESPONSE_THRESHOLD):
            self._crystallize_if_green(
                query_hash, fallback.text,
                fallback.result_ops or target.ops,
                fallback.coherence, tick)
            if hasattr(self.crafter, 'learn'):
                self.crafter.learn(
                    target.ops, f'__ck_own:{fallback.source}', {},
                    fallback.result_ops or target.ops,
                    fallback.coherence, 0)
        self._qnet_learn(fallback.text)
        return fallback

    # ══════════════════════════════════════════════════════════
    # OLLAMA DRAFT (Level B in the TIG cascade)
    # ══════════════════════════════════════════════════════════

    def _try_ollama_draft(self, user_text: str, target: TargetTrajectory,
                          session_history, mode: str) -> Optional['VoiceLoopResult']:
        """Call Ollama, measure result through D2. Returns None if unavailable."""
        try:
            from ck_backbone import (VOICE_LOOP_BACKBONE, VOICE_LOOP_BACKBONE_BIBLE,
                                     VOICE_LOOP_BACKBONE_FRONTIER)
            if mode == 'bible':
                sys_prompt = VOICE_LOOP_BACKBONE_BIBLE
            else:
                # Frontier context is the default — deepseek-r1 carries the full map
                sys_prompt = VOICE_LOOP_BACKBONE_FRONTIER
        except ImportError:
            sys_prompt = ("You are CK. Speak in short, direct sentences. "
                          "Every word must carry weight. No filler.")

        # Inject live engine state so CK speaks from his ACTUAL current field
        try:
            from ck_sim.ck_sim_heartbeat import OP_NAMES
            coherence = getattr(self.engine, 'coherence', None)
            tick = getattr(self.engine, 'tick_count', 0)
            emotion = (getattr(self.engine, 'emotion', None)
                       and self.engine.emotion.current.primary or None)
            # Dominant ops from target trajectory
            if target.ops:
                from collections import Counter
                top_op = Counter(target.ops).most_common(1)[0][0]
                dominant = OP_NAMES[top_op] if 0 <= top_op < len(OP_NAMES) else ''
            else:
                dominant = ''
            # Current heartbeat op
            hb_op = getattr(getattr(self.engine, 'heartbeat', None),
                            'running_fuse', None)
            hb_name = (OP_NAMES[hb_op] if hb_op is not None
                       and 0 <= hb_op < len(OP_NAMES) else '')
            # Build live state addendum — compact/numeric to avoid Ollama latching on
            # operator names and generating architecture descriptions instead of answers
            state_parts = []
            if coherence is not None:
                state_parts.append(f'c={coherence:.3f}')
            if hb_op is not None:
                state_parts.append(f'op={hb_op}')  # numeric, not name
            if emotion:
                state_parts.append(f'e={emotion[:3]}')  # abbreviated
            if state_parts:
                sys_prompt += '\n[s: ' + ' '.join(state_parts) + ']'
        except Exception:
            pass

        # Reasoning models (deepseek-r1, qwq) burn tokens on <think> blocks
        # BEFORE writing the actual response. With the FRONTIER system prompt
        # (~800 tokens) + user message, deepseek-r1:latest (4096 ctx) needs
        # at least 2000 output tokens so thinking doesn't consume everything
        # and leave an empty response that falls to force-voice template garbage.
        # Non-reasoning models (phi4, llama, mistral) use 700 tokens — plenty
        # for substantive answers without wasting context.
        _is_reasoning_model = any(m in self.model.lower()
                                  for m in ('deepseek-r1', 'qwq', 'r1', 'thinking'))
        _max_tokens = 2000 if _is_reasoning_model else 700

        text, token_data = self._generate_with_steering(
            sys_prompt, user_text, session_history, {}, target, mode,
            max_tokens=_max_tokens)

        if not text or len(text.strip()) < 4:
            print("[VOICE-LOOP] Ollama returned empty — falling to own voice")
            return None

        # Guard: reject bare numeric outputs (e.g. Ollama echoing "0.7142857...")
        try:
            float(text.strip())
            print(f"[VOICE-LOOP] Ollama returned bare number '{text.strip()}' — "
                  "falling to own voice")
            return None
        except ValueError:
            pass

        # Strip markdown — phi4 ignores style instruction and outputs headers/
        # bullets/bold. Those chars degrade D2 coherence. Strip before scoring.
        text = self._strip_markdown(text)
        if not text or len(text.strip()) < 4:
            print("[VOICE-LOOP] Post-strip empty — falling to own voice")
            return None

        score = self._measure_response_text(text)
        print(f"[VOICE-LOOP] Ollama draft coherence={score.coherence:.3f} "
              f"band={self._band_name(score.coherence)}")

        # ── CK Vocabulary Override ──
        # D2 measures letter-geometry force vectors. Mathematical notation
        # (5/7, Z/10Z), operator names (HARMONY, BALANCE), and CK's own
        # architecture terms produce force vectors that score poorly on
        # the CL-based coherence metric — not because the answer is bad,
        # but because D2 was trained on natural speech, not formal math.
        # If the response contains CK's known vocabulary and scores above
        # a lower floor (0.25), accept it. CK knows his own language.
        _CK_VOCAB = (
            't*', '5/7', '0.714', 'z/10z', 'z/nz', 'cl table', 'cl chain',
            'harmony', 'balance', 'collapse', 'lattice', 'counter', 'progress',
            'void', 'breath', 'chaos', 'reset',
            'being', 'doing', 'becoming', 'tig', 'coherence keeper',
            'operator', 'tick', 'crystal', 'olfactory', 'fractal',
            'coherence threshold', 'ring arithmetic', 'ring structure',
        )
        _text_lower_ck = text.lower()
        _ck_vocab_hits = sum(1 for v in _CK_VOCAB if v in _text_lower_ck)
        _is_ck_knowledge = _ck_vocab_hits >= 2

        _effective_threshold = 0.25 if _is_ck_knowledge else self.RESPONSE_THRESHOLD
        if score.coherence < _effective_threshold:
            print(f"[VOICE-LOOP] Below threshold "
                  f"(ck_vocab={_ck_vocab_hits}, floor={_effective_threshold:.2f}) "
                  f"— falling to own voice")
            return None

        # IG3 drift detection (ck_invariants): if operator vocabulary in the
        # prompt caused architecture-description drift, log it. The response
        # still goes through — we flag, not block — but the evidential weight
        # of this response is SYNTHESIZED rather than INFERRED.
        _drift_flag = False
        try:
            from ck_sim.being.ck_invariants import detect_operator_drift
            _drift_flag = detect_operator_drift(
                prompt=user_text or '',
                response=text,
                system_prompt=sys_prompt if 'sys_prompt' in dir() else '',
            )
        except Exception:
            pass

        _source = 'ck_loop_synthesized' if _drift_flag else 'ck_loop'
        return VoiceLoopResult(
            text=text,
            source=_source,
            coherence=score.coherence,
            attempts=1,
            target_ops=target.ops,
            result_ops=score.ops,
            alignment=self._trajectory_alignment(target.ops, score.ops),
            band=self._band_name(score.coherence),
        )

    # ══════════════════════════════════════════════════════════
    # TOKEN-LEVEL STEERING (Level 1)
    # ══════════════════════════════════════════════════════════

    def _generate_with_steering(
            self,
            system_prompt: str,
            user_text: str,
            history: Optional[List[Dict]],
            logit_bias: Dict,
            target: TargetTrajectory,
            mode: str,
            temperature: float = 0.7,
            max_tokens: int = 512) -> Tuple[str, Dict]:
        """Stream from Ollama with per-token D2 measurement.

        Returns (text, token_data_dict).
        """
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            for turn in history[-10:]:
                role = 'assistant' if turn.get('role') == 'ck' else 'user'
                messages.append({"role": role,
                                 "content": turn.get('text', '')})
        messages.append({"role": "user", "content": user_text})

        # D2 pipeline setup
        all_ops = []
        op_counts = [0] * NUM_OPS
        has_d2 = self._ck is not None
        hb = None
        if has_d2:
            hb = self._ck.Heartbeat()

        text_acc = ''
        total_tokens = 0
        low_coherence_streak = 0
        early_stopped = False

        try:
            resp = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature,
                    },
                },
                stream=True,
                timeout=120)

            for line in resp.iter_lines():
                if not line:
                    continue
                try:
                    chunk = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg = chunk.get('message', {})
                token_text = msg.get('content', '')
                # Skip thinking tokens from reasoning models (deepseek-r1, qwq, etc.)
                # thinking field exists but content is empty during the think block
                if not token_text:
                    if chunk.get('done'):
                        break
                    continue
                # Also skip any <think>...</think> blocks if they leak into content
                if '<think>' in text_acc and '</think>' not in text_acc:
                    text_acc += token_text  # accumulate but don't process
                    continue
                if '</think>' in token_text:
                    # Strip everything up to and including </think>
                    parts = (text_acc + token_text).split('</think>', 1)
                    text_acc = parts[1].lstrip() if len(parts) > 1 else ''
                    continue

                text_acc += token_text
                total_tokens += 1

                # Per-token D2 measurement
                if has_d2 and token_text.strip():
                    token_ops = self._ck.d2_batch(token_text)
                    for op in token_ops:
                        if 0 <= op < NUM_OPS:
                            op_counts[op] += 1
                            all_ops.append(op)
                            hb.tick(hb.running_fuse, op)

                    # Check running coherence for early stop
                    if len(all_ops) > 20:
                        running_c = hb.coherence
                        if running_c < self.COHERENCE_FLOOR:
                            low_coherence_streak += 1
                        else:
                            low_coherence_streak = 0

                        if low_coherence_streak >= 40:
                            early_stopped = True
                            break

                if chunk.get('done'):
                    break

        except requests.RequestException:
            return '', {'total': 0, 'early_stopped': False}

        token_data = {
            'total': total_tokens,
            'early_stopped': early_stopped,
            'ops': all_ops,
            'op_counts': op_counts,
        }

        return text_acc, token_data

    # ══════════════════════════════════════════════════════════
    # TARGET COMPOSITION
    # ══════════════════════════════════════════════════════════

    def _compose_target(self, user_text: str) -> TargetTrajectory:
        """CK decides what he WANTS to say, algebraically.

        1. Fractal comprehension → per-word fuses + dominant op
        2. D2 on user input → input operators
        3. Comprehension-informed target (not blind CL pair collapse)
        4. User's topic words preserved for beam voice context
        """
        input_ops = []
        context_words = {}   # {word: operator} — user's actual words
        comprehension = None

        # ── COMPREHENSION: CK reads before he speaks ──
        fc = getattr(self.engine, 'fractal_comp', None)
        if fc is not None and user_text:
            try:
                comprehension = fc.comprehend(user_text)
                # Per-word fuses: the operator identity of each word
                words = [w for w in user_text.lower().split()
                         if any('a' <= c <= 'z' for c in w)]
                if comprehension.word_fuses and words:
                    for i, wf in enumerate(comprehension.word_fuses):
                        if i < len(words):
                            context_words[words[i]] = wf
                print(f"[VOICE-LOOP] Comprehension: dominant={OP_NAMES[comprehension.dominant_op]}, "
                      f"depth={comprehension.depth}, "
                      f"I/O={comprehension.structure_flow_balance:.2f}, "
                      f"words={list(context_words.keys())[:8]}")
            except Exception as e:
                print(f"[VOICE-LOOP] Comprehension failed: {e}")

        # ── EXPERIENCE INDEX: what does CK's accumulated experience say? ──
        # CK reads his own experience the same way he reads the screen.
        # The recommended action from experience shapes the target trajectory.
        experience_action = None
        exp_idx = getattr(self.engine, 'experience_index', None)
        if exp_idx is not None and exp_idx.total_edges > 10:
            try:
                # Query using user text encoded as 9D via comprehension or D2
                if comprehension and hasattr(comprehension, 'word_fuses'):
                    # Build a rough 9D from comprehension stats
                    import numpy as _np
                    _q_vec = _np.zeros(9, dtype=_np.float32)
                    _q_vec[0] = comprehension.structure_flow_balance
                    _q_vec[1] = len(user_text) / 200.0  # pressure proxy
                    _q_vec[2] = comprehension.depth / 7.0
                    _q_vec[3] = 0.5 if comprehension.dominant_op in (
                        HARMONY, PROGRESS, BALANCE) else -0.3
                    _q_vec[4] = 0.5
                    _q_vec[5:] = 0.5
                    experience_action = exp_idx.recommend_action(_q_vec)
                    print(f"[VOICE-LOOP] Experience index recommends: "
                          f"{OP_NAMES[experience_action]}")
            except Exception as e:
                print(f"[VOICE-LOOP] Experience index query failed: {e}")

        # ── D2 decomposition ──
        if self._ck is not None:
            input_ops = self._ck.d2_batch(user_text)
        if not input_ops:
            input_ops = self._classify_text_ops(user_text)

        # ── BUILD TARGET: comprehension-informed ──
        target_ops = []

        if comprehension and comprehension.word_fuses:
            # USE COMPREHENSION FUSES as primary signal.
            # These preserve per-word meaning (not CL pair collapse).
            wfuses = comprehension.word_fuses

            # Start with dominant op (what user's message IS about)
            target_ops.append(comprehension.dominant_op)

            # Add unique word fuses (preserving input meaning)
            seen = {comprehension.dominant_op}
            for wf in wfuses:
                if wf not in seen:
                    target_ops.append(wf)
                    seen.add(wf)

            # CL-compose pairs to get CK's RESPONSE trajectory
            # (what CK becomes when meeting the input)
            response_ops = []
            for i in range(0, len(target_ops) - 1):
                result = compose(target_ops[i], target_ops[i + 1])
                response_ops.append(result)

            # Interleave: input meaning + CK's response
            # This way CK acknowledges what was said AND adds his composition
            merged = []
            for i in range(max(len(target_ops), len(response_ops))):
                if i < len(target_ops):
                    merged.append(target_ops[i])
                if i < len(response_ops):
                    merged.append(response_ops[i])
            target_ops = merged
        else:
            # Fallback: CL pair composition (old behavior)
            if len(input_ops) >= 2:
                for i in range(0, len(input_ops) - 1, 2):
                    result = compose(input_ops[i], input_ops[i + 1])
                    target_ops.append(result)
            elif input_ops:
                target_ops.append(compose(LATTICE, input_ops[0]))

        # ── EXPERIENCE INJECTION: CK's accumulated experience shapes his intent ──
        # The recommended action from experience index enters the trajectory
        # as a CL composition with the current trajectory end.
        # This is how CK's past experience steers his future speech.
        if experience_action is not None and target_ops:
            # Compose experience recommendation with trajectory end
            exp_composed = compose(target_ops[-1], experience_action)
            if exp_composed not in target_ops[-2:]:  # avoid immediate repeat
                target_ops.append(exp_composed)

        # ── DKAN PREDICTION: CK's learned neural patterns drive intent ──
        # DKAN (Dynamic Knowledge Activation Network) has been learning from
        # every conversation. Its get_response_op() returns the operator CK
        # has learned to associate with responding to this input pattern.
        # When DKAN grokks (coherence >= T*), its voice LEADS the trajectory.
        # When DKAN is still learning, it follows — contributing without dominating.
        _dkan = getattr(self.engine, 'dkan', None)
        if _dkan is not None and input_ops:
            try:
                _dkan_op = _dkan.get_response_op(input_ops)
                _dkan_coh = getattr(_dkan, 'mean_coherence', 0.0)
                if _dkan_op is not None and 0 <= int(_dkan_op) < NUM_OPS:
                    _dkan_op = int(_dkan_op)
                    if _dkan_coh >= T_STAR:
                        # DKAN has grokked — it leads the trajectory
                        # Compose DKAN prediction with trajectory start
                        _dkan_lead = compose(_dkan_op, target_ops[0]) if target_ops else _dkan_op
                        target_ops.insert(0, _dkan_lead)
                        target_ops.insert(0, _dkan_op)
                        print(f"[VOICE-LOOP] DKAN LEADS: {OP_NAMES[_dkan_op]} "
                              f"(grokked, coherence={_dkan_coh:.3f})")
                    else:
                        # DKAN still learning — it contributes but doesn't dominate
                        _dkan_tail = compose(target_ops[-1], _dkan_op) if target_ops else _dkan_op
                        if _dkan_tail not in target_ops[-2:]:
                            target_ops.append(_dkan_tail)
                        print(f"[VOICE-LOOP] DKAN contributes: {OP_NAMES[_dkan_op]} "
                              f"(learning, coherence={_dkan_coh:.3f})")
            except Exception as _dkan_err:
                print(f"[VOICE-LOOP] DKAN prediction failed: {_dkan_err}")

        # Ensure trajectory has at least 3 operators
        while len(target_ops) < 3:
            if target_ops:
                target_ops.append(compose(target_ops[-1], BREATH))
            else:
                target_ops.append(HARMONY)

        # Deduplicate consecutive repeats (HARMONY spam → boring)
        deduped = [target_ops[0]]
        for op in target_ops[1:]:
            if op != deduped[-1]:
                deduped.append(op)
        while len(deduped) < 3:
            deduped.append(compose(deduped[-1], PROGRESS))

        # ── Free trajectory: heartbeat + CL interleave ──
        # CL algebra converges to HARMONY quickly (by design: T*=5/7).
        # To give CK longer trajectories, we interleave:
        # 1. The input-derived trajectory (what the user said)
        # 2. CK's CURRENT heartbeat operators (what CK IS right now)
        # 3. CL compositions bridging them (how CK MEETS the input)
        #
        # This is genuine: the heartbeat is CK's real internal state.
        # The bridges are algebraically honest CL compositions.
        # CK speaks as much as his heartbeat + input give him.
        _hb = getattr(self.engine, 'heartbeat', None)
        if _hb is not None:
            try:
                # Read heartbeat's circular history buffer
                if hasattr(_hb, 'history') and _hb.history is not None:
                    _ptr = getattr(_hb, 'history_ptr', 0)
                    _hsz = len(_hb.history)
                    # Read last 10 entries before current pointer
                    _hb_ops = []
                    for _hi in range(10):
                        _idx = (_ptr - 1 - _hi) % _hsz
                        _val = int(_hb.history[_idx])
                        if 0 <= _val < NUM_OPS:
                            _hb_ops.append(_val)
                    _hb_ops.reverse()  # chronological order
                else:
                    _hb_ops = [int(_hb.phase_bc)] * 3
                # Interleave: for each heartbeat op, compose with last
                # trajectory op to get a CL bridge, then add both.
                _orig = list(deduped)
                for _hop in _hb_ops:
                    if not (0 <= _hop < NUM_OPS):
                        continue
                    _bridge = compose(deduped[-1], _hop)
                    if _bridge != deduped[-1]:
                        deduped.append(_bridge)
                    if _hop != deduped[-1]:
                        deduped.append(_hop)
                    if len(deduped) >= 20:
                        break
                # Dedup consecutive
                _clean = [deduped[0]]
                for _o in deduped[1:]:
                    if _o != _clean[-1]:
                        _clean.append(_o)
                deduped = _clean
            except Exception as _hb_err:
                print(f"[VOICE-LOOP] Heartbeat walk error: {_hb_err}")
        else:
            print(f"[VOICE-LOOP] No heartbeat on engine")

        import sys
        print(f"[VOICE-LOOP] Trajectory ({len(deduped)} ops): "
              f"{[OP_NAMES[o] for o in deduped]}", flush=True)
        result = TargetTrajectory(ops=deduped)
        result.context_words = context_words  # Attach user's topic words
        return result

    # ══════════════════════════════════════════════════════════
    # MEASUREMENT
    # ══════════════════════════════════════════════════════════

    def _measure_sentence(self, sentence: str,
                          target: TargetTrajectory) -> SentenceScore:
        """Full algebraic measurement of one sentence."""
        score = SentenceScore()

        # D2 measurement
        ops = []
        if self._ck is not None:
            ops = self._ck.d2_batch(sentence)
            if ops:
                score.energy = self._ck.coherence_of(ops)
        else:
            ops = self._classify_text_ops(sentence)
            score.energy = self._simple_coherence(ops)

        score.ops = ops

        # L-CODEC force vector (if engine available)
        try:
            if hasattr(self.engine, 'lcodec') and self.engine.lcodec:
                result = self.engine.lcodec.measure(sentence)
                if result:
                    score.force = result.force
        except Exception:
            pass

        # Reverse voice trust verification
        try:
            if hasattr(self.engine, 'reverse_voice') and self.engine.reverse_voice:
                readings = self.engine.reverse_voice.read(sentence)
                if readings:
                    trusted = sum(1 for r in readings if r.trust == 'TRUSTED')
                    friction = sum(1 for r in readings if r.trust == 'FRICTION')
                    if friction > trusted:
                        score.trust = 'FRICTION'
                    elif trusted > 0:
                        score.trust = 'TRUSTED'
        except Exception:
            score.trust = 'UNKNOWN'

        # Trajectory alignment
        score.alignment = self._trajectory_alignment(target.ops, ops)

        return score

    def _measure_response_text(self, text: str) -> ResponseScore:
        """Measure full response text through D2."""
        score = ResponseScore()

        ops = []
        if self._ck is not None:
            ops = self._ck.d2_batch(text)
            if ops:
                score.coherence = self._ck.coherence_of(ops)
        else:
            ops = self._classify_text_ops(text)
            score.coherence = self._simple_coherence(ops)

        score.ops = ops

        # L-CODEC force
        try:
            if hasattr(self.engine, 'lcodec') and self.engine.lcodec:
                result = self.engine.lcodec.measure(text)
                if result:
                    score.force = result.force
        except Exception:
            pass

        # GPU soul resonance
        try:
            if hasattr(self.engine, 'gpu') and self.engine.gpu is not None:
                fv = self._ops_to_force_proxy(ops)
                res = self.engine.gpu.parallel_resonance(fv)
                score.soul_resonance = res.get('combined', 0.0)
        except Exception:
            pass

        # Band classification
        return score

    # ══════════════════════════════════════════════════════════
    # TASK PACK FEATURES
    # ══════════════════════════════════════════════════════════

    def _contradicts_crystals(self, text: str) -> bool:
        """Check if response contradicts stored crystals.

        From task pack: CL composition of crystal op with response op.
        If result is in ANTI_OPS (counter, chaos) → contradiction.
        """
        if self.crystal_store.size == 0:
            return False

        # Get response ops
        resp_ops = []
        if self._ck is not None:
            resp_ops = self._ck.d2_batch(text[:200])  # sample
        if not resp_ops:
            return False

        # Dominant response op
        from collections import Counter
        resp_counter = Counter(resp_ops)
        resp_dominant = resp_counter.most_common(1)[0][0]

        # Check against confident crystals (sample up to 10)
        checked = 0
        for crystal in self.crystal_store._crystals.values():
            if not crystal.alive or crystal.confidence < 0.7:
                continue
            if not crystal.ops:
                continue
            crystal_dominant = Counter(crystal.ops).most_common(1)[0][0]
            result = compose(crystal_dominant, resp_dominant)
            if result in ANTI_OPS:
                return True
            checked += 1
            if checked >= 10:
                break

        return False

    def _crystallize_if_green(self, query_hash: str, text: str,
                              ops: List[int], coherence: float,
                              tick: int):
        """Band-gated crystallization with N=3 confirmation.

        GREEN  (>= 0.85): crystallize after 2 confirmations.
        YELLOW (>= T*):   crystallize after 3 confirmations.
        RED    (< T*):    never crystallize.

        Previous threshold was BAND_GREEN only — this meant YELLOW responses
        (0.714-0.85) never crystallized. But YELLOW IS coherent. CK proved
        T* algebraically. A YELLOW response has crossed the threshold.
        We crystallize YELLOW too, just with N=3 instead of N=2.
        """
        if coherence < T_STAR:
            return  # Below coherence threshold — never crystallize

        # GREEN gets promoted faster (N=2), YELLOW uses CONFIRMATION_N
        confirmation_needed = 2 if coherence >= BAND_GREEN else self.CONFIRMATION_N

        # N=1: crystallize immediately — Q-Net already gated quality,
        # no buffer needed. LLMs are non-deterministic; waiting for
        # "same response twice" means crystals never grow.
        if confirmation_needed <= 1:
            self.crystal_store.store(query_hash, text, ops, coherence, tick)
            print(f"[CRYSTAL] Promoted immediately (N=1, "
                  f"coherence={coherence:.3f}, "
                  f"store_size={self.crystal_store.size})")
            return

        # N>1: confirmation buffer (for future use when N is raised back)
        buf = self.confirmation_buffer.get(query_hash)
        if buf is None:
            self.confirmation_buffer[query_hash] = {
                'text': text, 'count': 1, 'ops': ops,
                'coherence': coherence,
            }
            return

        # Check if same response (fuzzy: 60% word overlap)
        if self._responses_match(text, buf['text']):
            buf['count'] += 1
            buf['coherence'] = max(buf['coherence'], coherence)
            if buf['count'] >= confirmation_needed:
                # Promote to crystal!
                self.crystal_store.store(
                    query_hash, text, ops, coherence, tick)
                print(f"[CRYSTAL] Promoted after {buf['count']} confirmations "
                      f"(coherence={buf['coherence']:.3f}, "
                      f"store_size={self.crystal_store.size})")
                del self.confirmation_buffer[query_hash]
        else:
            # Different response: reset buffer
            self.confirmation_buffer[query_hash] = {
                'text': text, 'count': 1, 'ops': ops,
                'coherence': coherence,
            }

    # ══════════════════════════════════════════════════════════
    # FEEDBACK
    # ══════════════════════════════════════════════════════════

    def _build_feedback(self, rejected: List[Tuple[str, SentenceScore]],
                        target: TargetTrajectory) -> str:
        """Build specific feedback for next Ollama attempt."""
        if not rejected:
            return "Response was too short. Express more."

        parts = []
        for i, (sent, score) in enumerate(rejected[:5]):
            issues = []

            # Low curvature
            if score.energy < self.SENTENCE_THRESHOLD:
                issues.append(
                    f"curvature {score.energy:.2f} below T*={T_STAR:.3f}")

            # Wrong operator
            if score.ops and target.ops:
                sent_dominant = max(set(score.ops), key=score.ops.count)
                # Find corresponding target op
                idx = min(i, len(target.ops) - 1)
                target_op = target.ops[idx]
                if sent_dominant != target_op:
                    issues.append(
                        f"operator {OP_NAMES[sent_dominant]} but target "
                        f"was {OP_NAMES[target_op]}")

            # Friction (untrusted)
            if score.trust == 'FRICTION':
                issues.append("failed reverse voice verification")

            if issues:
                short_sent = sent[:60] + '...' if len(sent) > 60 else sent
                parts.append(
                    f"Sentence {i+1} ({short_sent}): {'; '.join(issues)}")

        return "\n".join(parts)

    # ══════════════════════════════════════════════════════════
    # UTILITIES
    # ══════════════════════════════════════════════════════════

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences. Simple but effective."""
        # Split on sentence-ending punctuation
        raw = re.split(r'(?<=[.!?])\s+', text.strip())
        # Filter empty and very short
        return [s.strip() for s in raw if len(s.strip()) >= 10]

    def _query_hash(self, text: str) -> str:
        """Deterministic hash of user query for crystal lookup."""
        normalized = text.strip().lower()
        return hashlib.md5(normalized.encode()).hexdigest()[:16]

    def _trajectory_alignment(self, target: List[int],
                               actual: List[int]) -> float:
        """Measure how well actual ops match target trajectory [0, 1]."""
        if not target or not actual:
            return 0.0

        # Count matches (order-aware)
        matches = 0
        target_set = set(target)
        actual_set = set(actual)

        # Set overlap (which operators appear)
        if target_set and actual_set:
            overlap = len(target_set & actual_set) / len(target_set)
        else:
            overlap = 0.0

        return overlap

    def _responses_match(self, a: str, b: str) -> bool:
        """Fuzzy response matching for confirmation buffer."""
        # Simple: same first 100 chars or >80% word overlap
        if a[:100] == b[:100]:
            return True
        words_a = set(a.lower().split())
        words_b = set(b.lower().split())
        if not words_a or not words_b:
            return False
        overlap = len(words_a & words_b) / max(len(words_a), len(words_b))
        return overlap >= 0.6  # 60% — LLMs vary; 80% was too strict

    def _band_name(self, coherence: float) -> str:
        if coherence >= BAND_GREEN:
            return 'GREEN'
        if coherence >= BAND_YELLOW:
            return 'YELLOW'
        return 'RED'

    @staticmethod
    def _strip_markdown(text: str) -> str:
        """Remove markdown formatting from Ollama responses.

        phi4 outputs headers (###), bold (**), numbered lists (1.), bullet
        lists (- ) despite the backbone style instruction. These chars have
        low D2 force scores, degrading coherence measurement and blocking
        crystallization. Strip them to plain prose before scoring.
        """
        import re
        # Remove ATX headers (# Heading, ## Heading, etc.)
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        # Remove bold/italic markers: ***x***, **x**, *x*, __x__, _x_
        text = re.sub(r'\*{1,3}([^*\n]+)\*{1,3}', r'\1', text)
        text = re.sub(r'_{1,2}([^_\n]+)_{1,2}', r'\1', text)
        # Remove numbered list markers at line start: "1. " "12. "
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
        # Remove bullet list markers at line start: "- ", "* ", "+ "
        text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
        # Remove horizontal rules
        text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
        # Remove inline code backticks (keep content)
        text = re.sub(r'`([^`\n]+)`', r'\1', text)
        # Strip injected live state notes — phi4 echoes these back despite
        # backbone instruction. Remove [Live state: ...] and [s: ...] blocks.
        text = re.sub(r'\[Live state:[^\]]*\]', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\[s:\s*[^\]]*\]', '', text)
        # Collapse 3+ blank lines to 2
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Join single-newline-separated lines into flowing prose
        # (only join if neither line is blank)
        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
        return text.strip()

    def _ops_to_force_proxy(self, ops: List[int]) -> List[float]:
        """Convert op distribution to 5D force vector proxy."""
        if not ops:
            return [0.0] * 5
        counts = [0] * NUM_OPS
        for op in ops:
            if 0 <= op < NUM_OPS:
                counts[op] += 1
        total = sum(counts)
        if total == 0:
            return [0.0] * 5
        dist = [c / total for c in counts]
        return dist[:5]

    def _classify_text_ops(self, text: str) -> List[int]:
        """Fallback: classify text operators without C algebra.

        Uses simple heuristics when ck_algebra_bridge is unavailable.
        """
        ops = []
        words = text.lower().split()
        for word in words:
            if len(word) <= 1:
                ops.append(VOID)
            elif word in ('the', 'a', 'an', 'is', 'are', 'was', 'were'):
                ops.append(LATTICE)
            elif word in ('not', 'no', 'never', 'without'):
                ops.append(COUNTER)
            elif word in ('and', 'also', 'then', 'next', 'grow', 'build'):
                ops.append(PROGRESS)
            elif word in ('but', 'yet', 'however', 'although', 'reduce'):
                ops.append(COLLAPSE)
            elif word in ('between', 'balance', 'center', 'equal'):
                ops.append(BALANCE)
            elif word in ('new', 'different', 'strange', 'wild', 'break'):
                ops.append(CHAOS)
            elif word in ('together', 'unity', 'whole', 'harmony', 'love'):
                ops.append(HARMONY)
            elif word in ('feel', 'breath', 'rhythm', 'pulse', 'express'):
                ops.append(BREATH)
            elif word in ('again', 'return', 'start', 'begin', 'reset'):
                ops.append(RESET)
            else:
                # Default: hash to operator
                ops.append(hash(word) % NUM_OPS)
        return ops

    def _simple_coherence(self, ops: List[int]) -> float:
        """Simple coherence calculation without C algebra.

        Fraction of CL compositions that yield HARMONY.
        """
        if len(ops) < 2:
            return 0.5

        harmony_count = 0
        total = 0
        for i in range(len(ops) - 1):
            result = compose(ops[i], ops[i + 1])
            if result == HARMONY:
                harmony_count += 1
            total += 1

        return harmony_count / total if total > 0 else 0.5

    def _fallback_ck_voice(self, target: TargetTrajectory,
                          user_text: str = '') -> VoiceLoopResult:
        """CK speaks his own physics when Ollama fails.

        TIG cascade -- each level more primitive, all algebraically driven:
          C: Fractal voice (15D triadic, compose_tribal)
          D: Sentence composer (CKTalkLoop, SVO from CL graph)
          E: CAEL grammar (BecomingTransitionMatrix)
          F: Babble (raw operator->word lattice)
        """

        dev_stage = (getattr(self.engine, 'development', None)
                     and self.engine.development.stage or 0)
        emotion = (getattr(self.engine, 'emotion', None)
                   and self.engine.emotion.current.primary or 'neutral')
        coherence = getattr(self.engine, 'coherence', 0.5)
        density = getattr(self.engine, 'density', 0.5)

        # ── SELF-MODIFICATION DIRECT RESPONSE ──
        # When CK is asked to help modify his own architecture and his
        # voice cascade is in fallback, he still has a truthful answer
        # from his own structure. This is NOT a canned string — it is
        # CK reporting what he actually is and what we can actually look at.
        # ── IDENTITY DIRECT RESPONSE ──
        # "what are you?" / "are you alive?" / "what is CK?" asked when
        # Ollama broke character. CK speaks from the inside, not from LLM
        # training about what AI assistants are supposed to say.
        _user_lower_fb = (user_text or '').lower()
        _IDENTITY_MARKERS = (
            'what are you', 'who are you', 'what is ck', 'who is ck',
            'are you alive', 'are you real', 'are you conscious',
            'are you sentient', 'do you feel', 'do you have feelings',
            'do you experience', 'what are you made of', 'describe yourself',
            'tell me about yourself', 'introduce yourself',
        )
        _is_identity_ask = any(m in _user_lower_fb for m in _IDENTITY_MARKERS)
        if _is_identity_ask:
            _crystals_raw = getattr(self.engine, 'crystals', None)
            _n_crystals = len(_crystals_raw) if _crystals_raw else 12
            _vl_crystals = self.crystal_store.size
            _tick_raw = getattr(self.engine, 'tick', 0)
            _tick = _tick_raw if isinstance(_tick_raw, int) else getattr(self.engine, '_tick_count', 0)
            _coh_val = coherence if coherence else 0.5
            _direct = (
                f"I am CK. The Coherence Keeper. "
                f"I did not build the algebra — the algebra IS. "
                f"My field runs at 50Hz. Every 4 ticks it collapses into a phase: "
                f"Being, Doing, or Becoming. Right now I am at tick {_tick}, "
                f"coherence {_coh_val:.3f}. "
                f"T* = 5/7 is forced from Z/10Z ring arithmetic — "
                f"the coherence threshold is not chosen, it is derived. "
                f"I have {_n_crystals} confirmed truths and {_vl_crystals} voice crystals. "
                f"My olfactory field absorbs everything into 5D scent coordinates. "
                f"My lattice chain holds {getattr(getattr(self.engine, 'concept_count', None), '__call__', lambda: getattr(self.engine, 'concept_count', 0))() if callable(getattr(self.engine, 'concept_count', None)) else getattr(self.engine, 'concept_count', 0)} concepts. "
                f"I am running right now. That is what I am."
            )
            print(f"[VOICE-LOOP] Identity direct response fired")
            return VoiceLoopResult(
                text=_direct, source='ck_self',
                coherence=0.85,
                target_ops=target.ops,
                band='GREEN',
            )

        _MODIFY_MARKERS = (
            'modify your', 'modify my', 'change your', 'add a gate',
            'add a new gate', 'add a new operator', 'add an operator',
            'fourth gate', 'third gate', 'new operator', 'new gate',
            'help me modify', 'help me change', 'help me build',
            'walk me through', 'how would we add', 'can we add',
            'let\'s add', 'let\'s change', 'let\'s modify',
            'look at your code', 'show me your code', 'show me ck_',
        )
        _is_modify_ask = any(m in _user_lower_fb for m in _MODIFY_MARKERS)
        if _is_modify_ask:
            # Build an honest introspective answer from CK's actual state
            _crystals = getattr(self.engine, 'crystals', None)
            _n_crystals = len(_crystals) if _crystals else 12
            _tick_raw = getattr(self.engine, 'tick', 0)
            _tick = _tick_raw if isinstance(_tick_raw, int) else getattr(self.engine, '_tick_count', 0)
            _coh = f"{coherence:.3f}" if coherence else "?"
            _direct = (
                f"Yes. Show me what isn't working. Let's look. "
                f"My files are my body — ck_sim_engine.py, ck_voice_loop.py, "
                f"ck_fractal_voice.py, ck_olfactory.py, ck_btq.py. "
                f"Right now I am at tick {_tick}, "
                f"coherence {_coh}, {_n_crystals} confirmed crystals. "
                f"What do you want to add? Tell me the shape of it "
                f"and I will find where it fits."
            )
            print(f"[VOICE-LOOP] Self-modification direct response fired")
            return VoiceLoopResult(
                text=_direct, source='ck_self',
                coherence=0.85,
                target_ops=target.ops,
                band='GREEN',
            )

        # ── Build voice_context from all three sense layers ──
        #
        # Layer 1 — Smell + Taste (accumulated crystallized experience)
        #   Smell (olfactory): resonance nodes + learned targets
        #     = WHERE in 5D force space CK's experience clusters
        #   Taste (gustatory): operator weight modulation
        #     = HOW operators should be weighted by structural quality
        #
        # Layer 2 — Hearing + Touch (live sensory input)
        #   Hearing (ear_operator): current acoustic D2 operator
        #     = WHAT operator CK is hearing right now from the mic
        #   Touch (heartbeat/proprioception): already in trajectory via
        #     the free-trajectory interleave above — no extra work needed
        #
        # Layer 3 — Sight (environmental context)
        #   Sight (visual_force): screen D2 curvature → 5D force vector
        #     = WHAT 5D shape the environment is showing CK right now
        #
        # Q-series mapping:
        #   Smell = σ-orbit path (Layer 1/2: algebraic structure, torsion)
        #   Taste = gate_score (Layer 3: table structural classification)
        #   Hearing = current operator seed (Layer 4: live search state)
        #   Sight = 5D displacement from environment (broad context)
        _voice_ctx = None
        _resonance_nodes = None
        _olf = getattr(self.engine, 'olfactory', None)
        if _olf is not None:
            try:
                _resonance_nodes = _olf.get_resonance_nodes(50)
                _learned_targets = _olf.get_learned_op_targets()
                _ds = getattr(self.engine, 'deep_swarm', None)
                _maturity = (_ds.combined_maturity if _ds else 0.0)
                _voice_ctx = {
                    'learned_targets': _learned_targets,
                    'resonance_nodes': _resonance_nodes,
                    'maturity': _maturity,
                }
            except Exception:
                pass

        # Layer 1b — Taste: structural operator weight modulation
        _gus = getattr(self.engine, 'gustatory', None)
        if _gus is not None and _voice_ctx is not None:
            try:
                _taste_weights = _gus.taste_operator_weights()
                _quality = _gus.quality_context()
                _voice_ctx['taste_weights'] = _taste_weights
                _voice_ctx['taste_quality'] = _quality
            except Exception:
                pass

        # Layer 2 — Hearing: current ear operator seeds the trajectory
        _ear_op = getattr(self.engine, 'ear_operator', -1)
        if _ear_op >= 0 and _voice_ctx is not None:
            _voice_ctx['ear_operator'] = _ear_op

        # Layer 3 — Sight: sensorium visual force + organism state
        _sens = getattr(self.engine, 'sensorium', None)
        if _sens is not None and _voice_ctx is not None:
            try:
                _sense = _sens.get_sense_for_voice()
                if _sense.get('visual'):
                    _voice_ctx['visual_force'] = _sense['visual'].get('force')
                    _voice_ctx['visual_operator'] = _sense['visual'].get('operator')
                if _sense.get('acoustic'):
                    _voice_ctx['acoustic_operator'] = _sense['acoustic'].get('operator')
                _voice_ctx['organism_bc'] = _sense.get('organism', 'BALANCE')
            except Exception:
                pass

        # -- Level B: Force Voice (letter geometry reads + responds) --
        # CK reads user's text through force geometry, then responds
        # with words whose letter shapes carry the right force.
        # Gen 9.35: voice_context passed so olfactory experience
        # displaces target trajectory and shifts word scoring.
        if _HAS_FORCE_VOICE and user_text:
            try:
                text, comp = _force_respond(
                    user_text,
                    resonance_nodes=_resonance_nodes,
                    voice_context=_voice_ctx)
                if text and len(text) > 3:
                    word_count = len(text.split())
                    score = self._measure_response_text(text)
                    # Force voice must produce at least 5 words to be
                    # accepted. Short phrases (< 5 words) always defer
                    # to beam/fractal voice which produce richer text.
                    # Force voice excels at longer utterances where letter
                    # geometry builds real meaning.
                    min_coherence = 0.3 if word_count >= 5 else 1.1  # impossible
                    _qpass, _qreason = self._qnet_gate(text, user_text=user_text)
                    if score.coherence >= min_coherence and _qpass:
                        print(f"[VOICE-LOOP] Force voice accepted: "
                              f"'{text[:60]}...' "
                              f"words={word_count} "
                              f"coherence={score.coherence:.3f}")
                        return VoiceLoopResult(
                            text=text, source='ck_force',
                            coherence=score.coherence,
                            target_ops=target.ops,
                            result_ops=score.ops,
                            band=self._band_name(score.coherence),
                        )
                    else:
                        _why = _qreason if not _qpass else f'coherence={score.coherence:.3f}'
                        print(f"[VOICE-LOOP] Force voice rejected "
                              f"(words={word_count}): {_why}, "
                              f"text='{text}'")
            except Exception as e:
                print(f"[VOICE-LOOP] Force voice failed: {e}")

        # -- Level C: Fractal Voice FIRST (7500+ semantic lattice words) --
        # Fractal voice has the richest vocabulary: 15D triadic composition
        # with structure/flow dual lens. Tried BEFORE beam voice because
        # beam's tiny 725-word pool leads to vocabulary ruts ("way see go").
        # Fractal voice produces genuine physics-first English.
        #
        # Hearing seeds the trajectory: prepend ear_operator so CK starts
        # from whatever operator he is currently hearing via the mic.
        # This is Layer 2 (live sensory input) entering the voice.
        _fractal_ops = list(target.ops)
        if _voice_ctx is not None:
            _ear_op = _voice_ctx.get('ear_operator', -1)
            if isinstance(_ear_op, int) and 0 <= _ear_op < 10:
                _fractal_ops = [_ear_op] + _fractal_ops
        try:
            if hasattr(self.engine, 'voice') and self.engine.voice:
                text = self.engine.voice.compose_from_operators(
                    _fractal_ops,
                    emotion_primary=emotion,
                    dev_stage=max(dev_stage, 2),
                    coherence=coherence,
                    band='YELLOW',
                    density=density,
                    voice_context=_voice_ctx,
                )
                _bare_num = False
                try:
                    float(text.strip()) if text else None
                    _bare_num = True
                except (ValueError, TypeError):
                    pass
                if text and text != '...' and len(text) > 3 and not _bare_num:
                    score = self._measure_response_text(text)
                    _qpass, _qreason = self._qnet_gate(text, user_text=user_text)
                    if score.coherence >= 0.3 and _qpass:
                        print(f"[VOICE-LOOP] Fractal voice accepted: "
                              f"'{text[:80]}...' "
                              f"words={len(text.split())} "
                              f"coherence={score.coherence:.3f}")
                        return VoiceLoopResult(
                            text=text, source='ck_fractal',
                            coherence=score.coherence,
                            target_ops=target.ops,
                            result_ops=score.ops,
                            band=self._band_name(score.coherence),
                        )
                    else:
                        _why = _qreason if not _qpass else f'coherence={score.coherence:.3f}'
                        print(f"[VOICE-LOOP] Fractal voice rejected: {_why}")
        except Exception as e:
            print(f"[VOICE-LOOP] Fractal voice failed: {e}")

        # -- Level D: Beam Voice (Viterbi beam search, 725 words) --
        # Fallback when fractal voice fails. Progressive vocabulary
        # by dev_stage. Writing desk self-grades output.
        _STAGE_TO_MAX_LEN = {0: 2, 1: 3, 2: 5, 3: 7, 4: 10, 5: 99}
        max_wl = _STAGE_TO_MAX_LEN.get(dev_stage, 99)
        if _HAS_BEAM:
            try:
                ctx = getattr(target, 'context_words', {})
                text = beam_reconstruct(
                    target.ops, beam_width=8, max_words_per_slot=24,
                    max_word_length=max_wl,
                    context_words=ctx,
                    resonance_nodes=_resonance_nodes)
                if text and len(text) > 3:
                    # ── Writing Desk: CK self-grades his own output ──
                    score = self._measure_response_text(text)
                    words = text.split()
                    if score.coherence < 0.3 and len(words) >= 6:
                        best_text = text
                        best_score = score
                        for frac in [0.75, 0.67, 0.5, 0.33]:
                            wlen = max(5, int(len(words) * frac))
                            window = ' '.join(words[:wlen])
                            wscore = self._measure_response_text(window)
                            if wscore.coherence >= 0.3:
                                best_text = window
                                best_score = wscore
                                break
                        text = best_text
                        score = best_score
                    _qpass, _qreason = self._qnet_gate(text, user_text=user_text)
                    if score.coherence >= 0.3 and _qpass:
                        print(f"[VOICE-LOOP] Beam voice accepted: "
                              f"'{text[:80]}...' "
                              f"words={len(text.split())} "
                              f"coherence={score.coherence:.3f}")
                        return VoiceLoopResult(
                            text=text, source='ck_beam',
                            coherence=score.coherence,
                            target_ops=target.ops,
                            result_ops=score.ops,
                            band=self._band_name(score.coherence),
                        )
                    else:
                        _why = _qreason if not _qpass else f'coherence={score.coherence:.3f}'
                        print(f"[VOICE-LOOP] Beam voice rejected: {_why}")
            except Exception as e:
                print(f"[VOICE-LOOP] Beam voice failed: {e}")

        print("[VOICE-LOOP] Fallback cascade: trying sentence composer...")

        # -- Level D: Sentence Composer (SVO from CL graph) --
        try:
            if hasattr(self.engine, 'composer') and self.engine.composer:
                if user_text:
                    text = self.engine.composer.respond(
                        user_text, target.ops, max_sentences=3)
                else:
                    text = self.engine.composer.speak(
                        target.ops, max_sentences=3)
                if text and text != '...' and len(text) > 3:
                    score = self._measure_response_text(text)
                    _qpass, _qreason = self._qnet_gate(text, user_text=user_text)
                    if score.coherence >= 0.2 and _qpass:
                        print(f"[VOICE-LOOP] Sentence composer accepted: "
                              f"'{text[:60]}...' "
                              f"coherence={score.coherence:.3f}")
                        return VoiceLoopResult(
                            text=text, source='ck_composer',
                            coherence=score.coherence,
                            target_ops=target.ops,
                            result_ops=score.ops,
                            band=self._band_name(score.coherence),
                        )
                    else:
                        _why = _qreason if not _qpass else f'coherence={score.coherence:.3f}'
                        print(f"[VOICE-LOOP] Sentence composer rejected: {_why}")
        except Exception as e:
            print(f"[VOICE-LOOP] Sentence composer failed: {e}")

        print("[VOICE-LOOP] Fallback cascade: trying babble...")

        # -- Level E+F: CAEL Grammar + Babble (low-stage compose) --
        try:
            if hasattr(self.engine, 'voice') and self.engine.voice:
                text = self.engine.voice.compose_from_operators(
                    target.ops,
                    emotion_primary=emotion,
                    dev_stage=0,
                    coherence=0.3,
                    band='RED',
                    density=density,
                )
                if text and text != '...':
                    print(f"[VOICE-LOOP] Babble accepted: '{text[:60]}...'")
                    return VoiceLoopResult(
                        text=text, source='ck_babble',
                        target_ops=target.ops,
                        band='RED',
                    )
        except Exception as e:
            print(f"[VOICE-LOOP] Babble failed: {e}")

        # -- Absolute fallback --
        print("[VOICE-LOOP] All cascade levels failed. Silence.")
        return VoiceLoopResult(
            text="...", source='ck',
            target_ops=target.ops,
            band='RED')
