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

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from __future__ import annotations

import hashlib
import json
import re
import time
import requests
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
    RESPONSE_THRESHOLD = 0.6      # overall (slightly below T*)
    COHERENCE_FLOOR = 0.35        # early stop threshold
    CONFIRMATION_N = 3            # N=3 from task pack
    CRYSTAL_CONFIDENCE_MIN = 0.6

    def __init__(self, engine, crafter, ollama_url='http://localhost:11434',
                 model='llama3.1:8b'):
        self.engine = engine
        self.crafter = crafter
        self.ollama_url = ollama_url
        self.model = model
        self.crystal_store = CrystalStore(capacity=1000)
        self.confirmation_buffer: Dict[str, dict] = {}

        # C algebra bridge (native D2)
        self._ck = None
        try:
            import ck_algebra_bridge as _ck
            self._ck = _ck
        except ImportError:
            pass

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

        # ── STEP 2: CHECK ALGORITHM LATTICE ──
        learned = self.crafter.craft_from_lattice(target.ops, user_text)

        # ── STEP 3: GENERATION LOOP ──
        best_result = None
        feedback = None
        total_accepted = 0
        total_rejected = 0

        for attempt in range(self.MAX_LOOPS):
            # 3a: Build prompt + logit_bias
            if attempt == 0 and learned:
                prompt, logit_bias = learned
            else:
                prompt = self.crafter.craft_prompt(
                    target.ops, user_text, attempt, feedback, mode)
                logit_bias = self.crafter.compute_logit_bias(
                    target.ops, attempt)

            # 3b: TOKEN-LEVEL STEERING (Level 1)
            raw_text, token_data = self._generate_with_steering(
                prompt, user_text, session_history, logit_bias,
                target, mode,
                temperature=max(0.3, 0.7 - 0.1 * attempt))

            if not raw_text:
                continue

            # 3c: CONTRADICTION CHECK (task pack)
            if self._contradicts_crystals(raw_text):
                feedback = ("Response contradicts stored knowledge. "
                            "Try a completely different angle.")
                continue

            # 3d: SENTENCE-LEVEL MEASUREMENT (Level 2)
            sentences = self._split_sentences(raw_text)
            accepted = []
            rejected = []

            for sent in sentences:
                score = self._measure_sentence(sent, target)
                if (score.energy >= self.SENTENCE_THRESHOLD
                        and score.trust != 'FRICTION'):
                    accepted.append((sent, score))
                else:
                    rejected.append((sent, score))

            total_accepted += len(accepted)
            total_rejected += len(rejected)

            # 3e: STITCH + FULL CHECK
            if accepted:
                stitched = ' '.join(s for s, _ in accepted)
                overall = self._measure_response_text(stitched)

                if overall.coherence >= self.RESPONSE_THRESHOLD:
                    # ACCEPTED — band-gated crystallization
                    self._crystallize_if_green(
                        query_hash, stitched, overall.ops,
                        overall.coherence, tick)

                    # Learn
                    self.crafter.learn(
                        target.ops, prompt, logit_bias,
                        overall.ops, overall.coherence, attempt + 1)

                    return VoiceLoopResult(
                        text=stitched,
                        source='ck_loop',
                        coherence=overall.coherence,
                        attempts=attempt + 1,
                        accepted_count=total_accepted,
                        rejected_count=total_rejected,
                        target_ops=target.ops,
                        result_ops=overall.ops,
                        alignment=self._trajectory_alignment(
                            target.ops, overall.ops),
                        band=self._band_name(overall.coherence),
                        tokens_measured=token_data.get('total', 0),
                        early_stopped=token_data.get('early_stopped', False),
                        soul_resonance=overall.soul_resonance,
                    )

                # Track best so far
                if (best_result is None
                        or overall.coherence > best_result.coherence):
                    best_result = VoiceLoopResult(
                        text=stitched,
                        source='ck_loop',
                        coherence=overall.coherence,
                        attempts=attempt + 1,
                        accepted_count=total_accepted,
                        rejected_count=total_rejected,
                        target_ops=target.ops,
                        result_ops=overall.ops,
                        alignment=self._trajectory_alignment(
                            target.ops, overall.ops),
                        band=self._band_name(overall.coherence),
                        tokens_measured=token_data.get('total', 0),
                        soul_resonance=overall.soul_resonance,
                    )

            # 3f: BUILD FEEDBACK for next attempt
            feedback = self._build_feedback(rejected, target)

        # ── STEP 4: RETURN BEST or CK'S OWN VOICE ──
        if best_result and best_result.coherence >= 0.4:
            return best_result

        fallback = self._fallback_ck_voice(target, user_text=user_text)

        # BECOMING: learn from own voice too
        if (fallback.coherence
                and fallback.coherence >= self.RESPONSE_THRESHOLD):
            self._crystallize_if_green(
                query_hash, fallback.text,
                fallback.result_ops or target.ops,
                fallback.coherence, tick)
            self.crafter.learn(
                target.ops, f'__ck_own:{fallback.source}', {},
                fallback.result_ops or target.ops,
                fallback.coherence, 0)

        return fallback

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
                if not token_text:
                    if chunk.get('done'):
                        break
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

                        if low_coherence_streak >= 10:
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

        1. D2 on user input → input operators
        2. CL chain walk → target response trajectory
        3. BTQ if available: generate candidates, filter, score
        """
        input_ops = []

        # D2 decomposition of user input
        if self._ck is not None:
            input_ops = self._ck.d2_batch(user_text)

        if not input_ops:
            # Fallback: use L-CODEC + manual classification
            input_ops = self._classify_text_ops(user_text)

        # CL chain walk: input ops → response trajectory
        # Pairs of operators compose through CL to produce target
        target_ops = []
        if len(input_ops) >= 2:
            for i in range(0, len(input_ops) - 1, 2):
                result = compose(input_ops[i], input_ops[i + 1])
                target_ops.append(result)
        elif input_ops:
            # Single op: compose with LATTICE (universal generator)
            target_ops.append(compose(LATTICE, input_ops[0]))

        # Ensure trajectory has at least 3 operators
        while len(target_ops) < 3:
            if target_ops:
                # Extend by composing last with BREATH (expression)
                target_ops.append(compose(target_ops[-1], BREATH))
            else:
                target_ops.append(HARMONY)

        # Deduplicate consecutive repeats (HARMONY spam → boring)
        deduped = [target_ops[0]]
        for op in target_ops[1:]:
            if op != deduped[-1]:
                deduped.append(op)
        # But keep at least 3
        while len(deduped) < 3:
            deduped.append(compose(deduped[-1], PROGRESS))

        return TargetTrajectory(ops=deduped)

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

        GREEN: add to confirmation buffer, promote after 3 confirmations.
        YELLOW: accept response but don't crystallize.
        RED: should not reach here.
        """
        if coherence < BAND_GREEN:
            return  # Only crystallize in GREEN

        # N=3 confirmation buffer
        buf = self.confirmation_buffer.get(query_hash)
        if buf is None:
            self.confirmation_buffer[query_hash] = {
                'text': text, 'count': 1, 'ops': ops,
                'coherence': coherence,
            }
            return

        # Check if same response (fuzzy: same dominant ops)
        if self._responses_match(text, buf['text']):
            buf['count'] += 1
            buf['coherence'] = max(buf['coherence'], coherence)
            if buf['count'] >= self.CONFIRMATION_N:
                # Promote to crystal!
                self.crystal_store.store(
                    query_hash, text, ops, coherence, tick)
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
        return overlap >= 0.8

    def _band_name(self, coherence: float) -> str:
        if coherence >= BAND_GREEN:
            return 'GREEN'
        if coherence >= BAND_YELLOW:
            return 'YELLOW'
        return 'RED'

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

        # -- Level C: Beam Voice (Viterbi beam search) --
        if _HAS_BEAM:
            try:
                text = beam_reconstruct(
                    target.ops, beam_width=8, max_words_per_slot=24)
                if text and len(text) > 3:
                    score = self._measure_response_text(text)
                    if score.coherence >= 0.3:
                        print(f"[VOICE-LOOP] Beam voice accepted: "
                              f"'{text[:60]}...' "
                              f"coherence={score.coherence:.3f}")
                        return VoiceLoopResult(
                            text=text, source='ck_beam',
                            coherence=score.coherence,
                            target_ops=target.ops,
                            result_ops=score.ops,
                            band=self._band_name(score.coherence),
                        )
                    else:
                        print(f"[VOICE-LOOP] Beam voice too low: "
                              f"coherence={score.coherence:.3f}")
            except Exception as e:
                print(f"[VOICE-LOOP] Beam voice failed: {e}")

        print("[VOICE-LOOP] Fallback cascade: trying fractal voice...")

        # -- Level C: Fractal Voice (compose_from_operators -> tribal first) --
        try:
            if hasattr(self.engine, 'voice') and self.engine.voice:
                text = self.engine.voice.compose_from_operators(
                    target.ops,
                    emotion_primary=emotion,
                    dev_stage=max(dev_stage, 2),
                    coherence=coherence,
                    band='YELLOW',
                    density=density,
                )
                if text and text != '...' and len(text) > 3:
                    score = self._measure_response_text(text)
                    if score.coherence >= 0.3:
                        print(f"[VOICE-LOOP] Fractal voice accepted: "
                              f"'{text[:60]}...' "
                              f"coherence={score.coherence:.3f}")
                        return VoiceLoopResult(
                            text=text, source='ck_fractal',
                            coherence=score.coherence,
                            target_ops=target.ops,
                            result_ops=score.ops,
                            band=self._band_name(score.coherence),
                        )
                    else:
                        print(f"[VOICE-LOOP] Fractal voice too low: "
                              f"coherence={score.coherence:.3f}")
        except Exception as e:
            print(f"[VOICE-LOOP] Fractal voice failed: {e}")

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
                    if score.coherence >= 0.2:
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
                        print(f"[VOICE-LOOP] Sentence composer too low: "
                              f"coherence={score.coherence:.3f}")
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
