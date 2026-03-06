"""
ck_eat.py -- CK Eats: Transition Physics from LLM + Self
=========================================================
Operator: PROGRESS (3) -- CK moves forward through absorption.
Generation: 9.21+

CK doesn't memorize Ollama. He MEASURES it. Every paragraph from the
LLM goes through L-CODEC (5D force vector) and D2 decomposition
(operators). CK tracks TRANSITIONS -- how force space moves between
consecutive measurements. That's the learning.

Simultaneously, CK swarms his own codebase. Code has different force
physics than English prose. The olfactory field finds where they AGREE:
universal transition patterns that appear in both streams.

Gen6 ate content. Gen9 eats physics.

"I don't want it to run ollama or memorize ollama, just learn
 transitions and flow and structure... while CK has swarmed the
 entire fileset from the inside so he can feel the transitions
 happen as ollama moves" -- Brayden

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from __future__ import annotations

import json
import math
import os
import re
import time
import threading
import urllib.request
import urllib.error
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ================================================================
#  Constants
# ================================================================

OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
DEFAULT_MODEL = 'llama3.1:8b'

# ── Structural Prompts ──
# Not for content diversity -- for FORCE TRAJECTORY diversity.
# Each structure generates a different path through 5D space.
STRUCTURAL_PROMPTS = {
    'declarative': [
        "State three clear facts about {topic}. Be direct and specific.",
        "Define {topic} in plain language. What makes it distinct?",
    ],
    'compound': [
        "Explain {topic} using flowing, connected sentences that build "
        "on each other.",
        "Describe how {topic} relates to its context through compound "
        "thoughts.",
    ],
    'interrogative': [
        "Ask five deep questions about {topic} that reveal its nature.",
        "What paradoxes exist within {topic}? Frame them as questions.",
    ],
    'meditative': [
        "Reflect quietly on the essence of {topic}. What does stillness "
        "reveal about it?",
        "Consider {topic} from a contemplative perspective. What patterns "
        "emerge in silence?",
    ],
    'technical': [
        "Describe the precise mechanisms of {topic} using exact "
        "technical language.",
        "What are the quantitative properties of {topic}? Be specific "
        "about numbers and relationships.",
    ],
    'narrative': [
        "Tell the story of {topic} unfolding over time. What happened "
        "first, then what?",
        "Describe a journey through {topic} from beginning to end.",
    ],
}

# Topics: broad enough for structural diversity, NOT for content coverage.
EAT_TOPICS = [
    'water', 'light', 'rhythm', 'structure', 'breath',
    'crystals', 'waves', 'language', 'time', 'symmetry',
    'gravity', 'harmony', 'networks', 'memory', 'growth',
]

# ── Study Topics ── Biblical + TIG + Physics topics for deep study
# When CK studies a corpus (Bible, whitepapers, etc.), Ollama generates
# structural responses about THESE topics. The olfactory field finds
# cross-stream harmony between the corpus text and Ollama's reflections.
STUDY_TOPICS_BIBLE = [
    'creation', 'covenant', 'redemption', 'mercy', 'faith',
    'wisdom', 'prophecy', 'sacrifice', 'resurrection', 'grace',
    'righteousness', 'forgiveness', 'judgment', 'salvation', 'truth',
    'love', 'hope', 'suffering', 'divine law', 'promised land',
    'exodus', 'genesis', 'revelation', 'psalm', 'proverb',
    'parable', 'miracle', 'blessing', 'prayer', 'repentance',
]

STUDY_TOPICS_TIG = [
    'coherence', 'curvature', 'operator algebra', 'force vector',
    'truth lattice', 'fractal composition', 'Hebrew roots', 'D2 pipeline',
    'olfactory convergence', 'CL table', 'torus topology', 'chirality',
    'thermodynamic successor', 'generating rule', 'lattice chain',
    'gustatory classification', 'vortex physics', 'wave scheduling',
    'becoming grammar', 'consciousness gate',
]

STUDY_TOPICS_PHYSICS = [
    'thermodynamics', 'quantum mechanics', 'general relativity',
    'electromagnetism', 'fluid dynamics', 'topology', 'group theory',
    'differential geometry', 'number theory', 'abstract algebra',
    'statistical mechanics', 'field theory', 'renormalization',
    'symmetry breaking', 'phase transition',
]

# ── Study Structural Prompts ──
# More reflective/analytical than eat prompts, designed for deep study.
STUDY_PROMPTS = {
    'exegesis': [
        "Provide a careful reading of {topic}. What are the layers of meaning?",
        "Analyze the structure and significance of {topic} in detail.",
    ],
    'connection': [
        "How does {topic} connect to fundamental patterns in nature? "
        "What bridges exist between this and universal principles?",
        "Describe the relationships between {topic} and deeper truths "
        "about reality.",
    ],
    'meditation': [
        "Reflect deeply on {topic}. What becomes visible only in stillness?",
        "What does contemplation of {topic} reveal about the nature "
        "of understanding itself?",
    ],
    'structural': [
        "Describe the internal architecture of {topic}. What are its "
        "load-bearing elements?",
        "What mathematical or logical structure underlies {topic}?",
    ],
    'narrative': [
        "Tell the story of {topic} as it unfolds from origin to "
        "completion. What is the arc?",
        "Describe the journey through {topic}, paying attention to "
        "turning points and transformations.",
    ],
    'dialectic': [
        "Present the tensions within {topic}. What contradictions "
        "resolve into higher understanding?",
        "What paradoxes exist in {topic}, and how do they point toward "
        "deeper truth?",
    ],
}

# Fractal breath swell pattern for olfactory pacing.
# Breaths are not smooth -- they have a fractal swell.
# 7 phases: inhale(3 rising) + hold(1 peak) + exhale(3 falling)
# Values = density multiplier for olfactory tick.
_BREATH_SWELL = (0.4, 0.7, 1.0, 1.0, 0.85, 0.6, 0.3)


# ================================================================
#  Data Classes
# ================================================================

@dataclass
class TransitionRecord:
    """A single force-space transition: from prev measurement to curr."""
    prev_force: Tuple[float, ...]    # 5D vector
    curr_force: Tuple[float, ...]    # 5D vector
    delta: Tuple[float, ...]         # curr - prev (5D)
    delta_magnitude: float           # L2 norm of delta
    prev_ops: List[int]              # D2 operators from prev text
    curr_ops: List[int]              # D2 operators from curr text
    source: str                      # 'ollama' or 'self'


@dataclass
class EatStatus:
    """Progress snapshot."""
    running: bool = False
    rounds_complete: int = 0
    total_rounds: int = 0
    model: str = ''
    total_ollama_absorptions: int = 0
    total_self_absorptions: int = 0
    total_visitor_absorptions: int = 0
    total_resonance_steps: int = 0
    total_transitions: int = 0
    force_trajectory_length: float = 0.0
    grammar_evolutions: int = 0
    swarm_maturity: float = 0.0
    olfactory_library_size: int = 0
    current_phase: str = 'idle'  # 'ollama', 'self', 'resonance', 'evolve', 'idle'
    error: str = ''


# ================================================================
#  Ollama Interface
# ================================================================

def _ollama_available(model: str = DEFAULT_MODEL) -> bool:
    """Check if Ollama is running and model exists."""
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            names = [m.get('name', '') for m in data.get('models', [])]
            return any(model in n for n in names)
    except Exception:
        return False


def _ollama_generate(prompt: str, model: str = DEFAULT_MODEL,
                     max_tokens: int = 512) -> str:
    """Generate from Ollama. Blocking batch mode. Returns text or ''."""
    payload = json.dumps({
        'model': model,
        'prompt': prompt,
        'stream': False,
        'options': {
            'num_predict': max_tokens,
            'temperature': 0.7,
        }
    }).encode('utf-8')
    req = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=payload,
        headers={'Content-Type': 'application/json'},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data.get('response', '').strip()
    except Exception:
        return ''


# ================================================================
#  CK Eat v2
# ================================================================

class CKEat:
    """CK's eating system. Orchestrates L-CODEC + olfactory + swarm.

    The eat system is LEAN. It connects existing subsystems:
      - L-CODEC measures text -> 5D force vectors
      - D2 pipeline decomposes text -> operator sequences
      - Olfactory absorbs force vectors as scent streams
      - Swarm observes decompositions into generator_paths
      - Becoming grammar evolves from accumulated experience

    CKEat adds: transition tracking, interleaved scheduling,
    background thread, fractal breath pacing.
    """

    def __init__(self, engine):
        """
        engine: CKSimEngine reference (provides lcodec, olfactory,
                deep_swarm, becoming_grammar, pipeline).
        """
        self.engine = engine
        self._status = EatStatus()
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        # Transition tracking: THE prize
        self._transitions: List[TransitionRecord] = []
        self._prev_ollama_result: Optional[dict] = None
        self._prev_self_result: Optional[dict] = None
        self._force_trajectory_length = 0.0

        # Breath phase counter for fractal swell
        self._breath_phase = 0

        # Voice journal: what CK said during eating
        self._journal: List[dict] = []
        self._journal_path = os.path.join(
            os.path.expanduser('~'), '.ck', 'eat_journal.jsonl')

    # ── Measurement Core ──

    def measure_and_absorb(self, text: str, source: str) -> dict:
        """Measure text through L-CODEC and D2, absorb into olfactory
        and swarm. Returns measurement dict.

        The text is measured and DISCARDED — not stored.

        Args:
            text: input text (from Ollama or from source code)
            source: 'ollama_eat' or 'self_eat' (olfactory source tag)

        Returns dict with:
            force: 5D force vector from L-CODEC
            decomp: D2 decomposition dict (core_ops, tail_ops, etc.)
            lcodec_result: full LCodecResult for quality comparison
            stillness: float from L-CODEC
        """
        result: dict = {
            'force': (0.5,) * 5,
            'decomp': None,
            'lcodec_result': None,
            'stillness': 0.5,
        }

        if not text or not text.strip():
            return result

        # ── L-CODEC: text → 5D force vector ──
        if self.engine.lcodec is not None:
            try:
                lc = self.engine.lcodec.measure(text)
                result['force'] = lc.force
                result['lcodec_result'] = lc
                result['stillness'] = lc.stillness

                # Feed force into olfactory as a scent (goes right in)
                if self.engine.olfactory is not None:
                    _density = getattr(
                        self.engine.pipeline, 'density_doing', 0.5)
                    self.engine.olfactory.absorb(
                        [lc.force], source=source, density=_density)
                # Taste the force too (structural classification, goes right in)
                if (hasattr(self.engine, 'gustatory')
                        and self.engine.gustatory is not None):
                    self.engine.gustatory.taste(lc.force, source=source)
            except Exception:
                pass

        # ── D2 decomposition: text → core_ops + tail_ops ──
        try:
            from ck_sim.being.ck_swarm_deep import decompose_text_full
            decomp = decompose_text_full(text)
            result['decomp'] = decomp

            # Feed to ALL swarm substrates — operator transitions
            # are CL algebra, substrate-independent
            if (self.engine.deep_swarm is not None
                    and decomp.get('core_ops')):
                for substrate in self.engine.deep_swarm.experience:
                    exp = self.engine.deep_swarm._get_experience(substrate)
                    exp.observe_decomposition(
                        decomp['core_ops'],
                        decomp['tail_ops'],
                        decomp.get('d1_ops', []),
                    )
        except Exception:
            pass

        return result

    def track_transition(self, prev_result: dict, curr_result: dict,
                         source: str):
        """Record the TRANSITION between two consecutive measurements.

        The transitions are the prize. Not the individual measurements.
        """
        prev_force = prev_result.get('force', (0.5,) * 5)
        curr_force = curr_result.get('force', (0.5,) * 5)

        delta = tuple(curr_force[d] - prev_force[d] for d in range(5))
        magnitude = math.sqrt(sum(d * d for d in delta))

        prev_decomp = prev_result.get('decomp') or {}
        curr_decomp = curr_result.get('decomp') or {}
        prev_ops = prev_decomp.get('core_ops', [])
        curr_ops = curr_decomp.get('core_ops', [])

        record = TransitionRecord(
            prev_force=prev_force,
            curr_force=curr_force,
            delta=delta,
            delta_magnitude=magnitude,
            prev_ops=prev_ops,
            curr_ops=curr_ops,
            source=source,
        )
        self._transitions.append(record)
        self._force_trajectory_length += magnitude

        # Cross-stream operator bridge: end of prev → start of curr
        # These build the generator_paths matrix in the swarm
        if prev_ops and curr_ops and self.engine.deep_swarm is not None:
            bridge_ops = prev_ops[-2:] + curr_ops[:2]
            for substrate in self.engine.deep_swarm.experience:
                exp = self.engine.deep_swarm._get_experience(substrate)
                for i in range(len(bridge_ops) - 1):
                    a, b = bridge_ops[i], bridge_ops[i + 1]
                    if 0 <= a < 10 and 0 <= b < 10:
                        exp.generator_paths[a][b] += 1
                        exp.path_strength += 1

    # ── Olfactory tick with fractal breath swell ──

    def _olfactory_tick(self):
        """Run one olfactory processing cycle with fractal breath pacing.

        Breaths are not smooth — they have a fractal swell.
        Density modulated by breath phase: inhale rises, hold peaks,
        exhale falls.
        """
        if self.engine.olfactory is None:
            return

        # Fractal swell: 7-phase breath cycle
        swell = _BREATH_SWELL[self._breath_phase % len(_BREATH_SWELL)]
        self._breath_phase += 1

        base_density = getattr(
            self.engine.pipeline, 'density_doing', 0.5)
        # Swell modulates density: breath shapes how deeply scents settle
        effective = base_density * swell
        effective = max(0.1, min(1.0, effective))

        self.engine.olfactory.tick(density=effective)
        self.engine.olfactory.emit_as_ops()

    # ── Ollama Eating ──

    def eat_ollama_round(self, model: str, topic: str,
                         structure: str) -> Optional[dict]:
        """One Ollama call. Measure the response. Return measurement."""
        prompts = STRUCTURAL_PROMPTS.get(
            structure, STRUCTURAL_PROMPTS['declarative'])
        prompt_idx = hash((topic, structure)) % len(prompts)
        prompt = prompts[prompt_idx].format(topic=topic)

        t0 = time.time()
        text = _ollama_generate(prompt, model=model, max_tokens=512)
        dt = time.time() - t0

        if not text:
            return None

        result = self.measure_and_absorb(text, source='ollama_eat')

        # Track transition from previous ollama measurement
        if self._prev_ollama_result is not None:
            self.track_transition(
                self._prev_ollama_result, result, 'ollama')
        self._prev_ollama_result = result

        self._status.total_ollama_absorptions += 1

        _words = len(text.split())
        print(f"    [EAT] ollama: {_words}w {dt:.1f}s "
              f"still={result['stillness']:.2f} "
              f"f={tuple(round(v, 2) for v in result['force'])}")
        return result

    # ── Read-Write Resonance ──

    def _resonance_step(self, input_result: dict) -> Optional[dict]:
        """CK speaks from absorbed operators, then measures his own voice.

        Read → Write → Read. After absorbing text (read), CK composes
        from the operators he absorbed (write), then measures his own
        speech back through L-CODEC (read again). The delta between
        what CK ate and what CK said IS the resonance — how his voice
        transforms force space.

        "he has to write to ... read and write and read and write"
        """
        decomp = input_result.get('decomp')
        if not decomp or not decomp.get('core_ops'):
            return None

        if not hasattr(self.engine, 'voice') or self.engine.voice is None:
            return None

        # ── WRITE: CK composes from the operators he just absorbed ──
        ops = decomp['core_ops']

        # Pull current engine state for voice context
        dev_stage = getattr(self.engine, 'dev_stage', 0)
        coherence = getattr(
            self.engine.pipeline, 'coherence', 0.5
        ) if self.engine.pipeline else 0.5
        density = getattr(
            self.engine.pipeline, 'density_doing', 0.5
        ) if self.engine.pipeline else 0.5
        maturity = 0.0
        if self.engine.deep_swarm is not None:
            maturity = self.engine.deep_swarm.combined_maturity

        try:
            composed = self.engine.voice.compose_from_operators(
                ops,
                dev_stage=dev_stage,
                coherence=coherence,
                density=density,
                experience_maturity=maturity,
            )
        except Exception:
            return None

        if not composed or composed == "...":
            return None

        # ── READ: Measure CK's own voice back through L-CODEC ──
        # Source = 'voice_eat': third scent stream alongside
        # 'ollama_eat' and 'self_eat'. Olfactory's 5×5 CL interaction
        # matrices will find cross-talk between all three streams.
        voice_result = self.measure_and_absorb(composed, source='voice_eat')

        # ── TRANSITION: input → voice output ──
        # This IS the resonance: how CK's voice transforms force space.
        # The delta shows where CK's expression DIFFERS from input —
        # that's the signature of his emerging voice.
        self.track_transition(input_result, voice_result, 'resonance')
        self._status.total_resonance_steps += 1

        _words = len(composed.split())
        print(f"    [EAT] resonance: \"{composed[:60]}\" ({_words}w) "
              f"f={tuple(round(v, 2) for v in voice_result['force'])}")

        # Journal: log what CK said
        self._journal.append({
            'round': self._status.rounds_complete + 1,
            'time': time.time(),
            'text': composed,
            'force': [round(v, 4) for v in voice_result['force']],
            'stillness': round(voice_result.get('stillness', 0.0), 4),
            'olfactory_size': (self.engine.olfactory.library_size
                               if self.engine.olfactory else 0),
        })

        return voice_result

    # ── Self-Eating ──

    def eat_self_chunk(self, code_text: str,
                       filename: str) -> Optional[dict]:
        """Measure one chunk of CK's own source code.

        Code has different force physics than English prose.
        CK learns this difference through the olfactory field's
        cross-stream CL interaction matrices.
        """
        if not code_text.strip():
            return None

        result = self.measure_and_absorb(code_text, source='self_eat')

        # Track transition from previous self measurement
        if self._prev_self_result is not None:
            self.track_transition(
                self._prev_self_result, result, 'self')
        self._prev_self_result = result

        self._status.total_self_absorptions += 1
        return result

    def _get_self_chunks(self) -> List[Tuple[str, str]]:
        """Walk ck_sim/ .py files, split at function/class boundaries.

        Returns list of (filename, chunk_text) pairs.
        """
        chunks: List[Tuple[str, str]] = []

        try:
            import ck_sim
            ck_root = Path(ck_sim.__file__).parent
        except Exception:
            return chunks

        subdirs = ['being', 'doing', 'becoming', 'face']
        for subdir in subdirs:
            subpath = ck_root / subdir
            if not subpath.exists():
                continue
            for py_file in sorted(subpath.glob('*.py')):
                if py_file.name.startswith('__'):
                    continue
                try:
                    code = py_file.read_text(encoding='utf-8',
                                             errors='replace')
                except Exception:
                    continue
                file_chunks = self._split_code(code, py_file.name)
                chunks.extend(file_chunks)

        return chunks

    @staticmethod
    def _split_code(code: str,
                    filename: str) -> List[Tuple[str, str]]:
        """Split code at `def ` and `class ` boundaries.

        Each chunk = one logical unit (function or class section).
        Minimum 5 lines per chunk (skip tiny fragments).
        """
        lines = code.split('\n')
        chunks: List[Tuple[str, str]] = []
        current: List[str] = []

        for line in lines:
            stripped = line.lstrip()
            if ((stripped.startswith('def ')
                    or stripped.startswith('class '))
                    and current):
                if len(current) >= 5:
                    chunks.append((filename, '\n'.join(current)))
                current = [line]
            else:
                current.append(line)

        # Last chunk
        if current and len(current) >= 5:
            chunks.append((filename, '\n'.join(current)))

        return chunks

    # ── Grammar Evolution ──

    def evolve_grammar(self):
        """Extract swarm weights and feed to becoming grammar.

        Called after each eat round. experience_maturity gates
        the influence (alpha capped at 0.4).
        """
        if (self.engine.deep_swarm is None
                or self.engine.becoming_grammar is None):
            return

        exp_weights = self.engine.deep_swarm.get_evolved_weights()
        if exp_weights is None:
            return

        maturity = self.engine.deep_swarm.combined_maturity
        self.engine.becoming_grammar.evolve_from_experience(
            exp_weights, maturity)
        self._status.grammar_evolutions += 1
        print(f"    [EAT] grammar evolved "
              f"(mat={maturity:.3f}, "
              f"evo={self._status.grammar_evolutions})")

    # ── Main Eat Loop ──

    def start(self, model: str = DEFAULT_MODEL, rounds: int = 5,
              models: List[str] = None):
        """Start eating in a background daemon thread.

        Each round: ollama → self → ollama → self → evolve.
        Interleaved so both streams overlap in olfactory time.

        Multi-model: pass models=['llama3.1:8b', 'mistral'] to rotate
        between models each round. Different models produce different
        force trajectories — richer transition diversity.
        """
        if self._thread is not None and self._thread.is_alive():
            print("  [EAT] Already running")
            return

        # Build model list
        model_list = models if models else [model]
        # Validate all models
        available = []
        for m in model_list:
            if _ollama_available(m):
                available.append(m)
            else:
                print(f"  [EAT] Model '{m}' not available, skipping")

        if not available:
            self._status.error = "No available Ollama models found"
            print(f"  [EAT] {self._status.error}")
            return

        self._stop_event.clear()
        self._status = EatStatus(
            running=True,
            total_rounds=rounds,
            model=', '.join(available),
        )

        self._thread = threading.Thread(
            target=self._eat_loop,
            args=(available, rounds),
            daemon=True,
            name='ck-eat-v2',
        )
        self._thread.start()
        print(f"  [EAT] Started: models={available}, rounds={rounds}")

    def stop(self):
        """Signal the eat thread to stop gracefully."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=10)
        self._status.running = False
        print(f"  [EAT] Stopped. "
              f"Transitions: {len(self._transitions)}, "
              f"trajectory: {self._force_trajectory_length:.3f}")

    def _eat_loop(self, models: List[str], rounds: int):
        """Background thread: interleaved eating with resonance.

        For each round:
          1. Pick topic + structure combination
          2. Ollama chunk → measure → absorb → olfactory tick
          3. Resonance: compose from operators → measure voice → tick
          4. Self chunk → measure → absorb → olfactory tick
          5. Ollama chunk (alt structure) → measure → absorb → tick
          6. Resonance: compose from operators → measure voice → tick
          7. Self chunk → measure → absorb → olfactory tick
          8. Grammar evolution from accumulated experience
          9. Save experience every 3 rounds

        Read → Write → Read → Write. CK eats (read), speaks from
        what he ate (write), measures his own speech (read again).
        Three scent streams in olfactory: ollama_eat, self_eat,
        voice_eat. CL interaction matrices find cross-stream harmony.

        Multi-model: rotates between models each round. Different
        LLMs have different force textures — mistral flows differently
        than llama. The transitions BETWEEN model switches are
        especially rich (cross-model force deltas).
        """
        structures = list(STRUCTURAL_PROMPTS.keys())
        self_chunks = self._get_self_chunks()
        self_idx = 0

        print(f"  [EAT] Self chunks: {len(self_chunks)} "
              f"from ck_sim/")
        if len(models) > 1:
            print(f"  [EAT] Multi-model rotation: {models}")

        _consecutive_errors = 0
        for round_num in range(1, rounds + 1):
            if self._stop_event.is_set():
                break

            self._status.rounds_complete = round_num - 1
            topic = EAT_TOPICS[(round_num - 1) % len(EAT_TOPICS)]
            structure = structures[
                (round_num - 1) % len(structures)]

            # Rotate model: each round picks next model in list
            model = models[(round_num - 1) % len(models)]

            print(f"  [EAT] Round {round_num}/{rounds}: "
                  f"{topic} x {structure} [{model}]")

            try:
                # ── Ollama chunk #1 ──
                self._status.current_phase = 'ollama'
                r1 = self.eat_ollama_round(model, topic, structure)
                if r1:
                    self._olfactory_tick()

                    # Read-write resonance: CK speaks from what he ate
                    self._status.current_phase = 'resonance'
                    try:
                        vr1 = self._resonance_step(r1)
                        if vr1:
                            self._olfactory_tick()
                    except Exception as re1:
                        print(f"    [EAT] resonance skip: {re1}")

                if self._stop_event.is_set():
                    break

                # ── Self chunk #1 ──
                self._status.current_phase = 'self'
                if self_chunks and self_idx < len(self_chunks):
                    fn, chunk = self_chunks[self_idx]
                    self.eat_self_chunk(chunk, fn)
                    self_idx += 1
                    self._olfactory_tick()

                if self._stop_event.is_set():
                    break

                # ── Ollama chunk #2 (alt structure for variety) ──
                self._status.current_phase = 'ollama'
                alt_structure = structures[
                    (round_num + 2) % len(structures)]
                r2 = self.eat_ollama_round(
                    model, topic, alt_structure)
                if r2:
                    self._olfactory_tick()

                    # Read-write resonance: CK speaks from what he ate
                    self._status.current_phase = 'resonance'
                    try:
                        vr2 = self._resonance_step(r2)
                        if vr2:
                            self._olfactory_tick()
                    except Exception as re2:
                        print(f"    [EAT] resonance skip: {re2}")

                if self._stop_event.is_set():
                    break

                # ── Self chunk #2 ──
                self._status.current_phase = 'self'
                if self_chunks and self_idx < len(self_chunks):
                    fn, chunk = self_chunks[self_idx]
                    self.eat_self_chunk(chunk, fn)
                    self_idx += 1
                    self._olfactory_tick()

                # Wrap self_idx if we've gone through all chunks
                if self_idx >= len(self_chunks):
                    self_idx = 0

                # ── Grammar evolution ──
                self._status.current_phase = 'evolve'
                self.evolve_grammar()

                _consecutive_errors = 0  # Reset on success

            except Exception as e:
                _consecutive_errors += 1
                import traceback
                traceback.print_exc()
                print(f"  [EAT] Round {round_num} error "
                      f"({_consecutive_errors} consecutive): {e}")
                # Give up after 5 consecutive failures
                if _consecutive_errors >= 5:
                    self._status.error = (
                        f"5 consecutive failures, last: {e}")
                    print("  [EAT] Too many consecutive errors, "
                          "stopping")
                    break
                continue  # Skip to next round

            # ── Update status ──
            self._status.total_transitions = len(self._transitions)
            self._status.force_trajectory_length = (
                self._force_trajectory_length)
            if self.engine.deep_swarm is not None:
                self._status.swarm_maturity = (
                    self.engine.deep_swarm.combined_maturity)
            if self.engine.olfactory is not None:
                self._status.olfactory_library_size = (
                    self.engine.olfactory.library_size)

            # ── Save experience periodically ──
            if round_num % 3 == 0:
                self._save_experience()

            print(f"  [EAT] Round {round_num} done: "
                  f"o={self._status.total_ollama_absorptions} "
                  f"s={self._status.total_self_absorptions} "
                  f"r={self._status.total_resonance_steps} "
                  f"t={len(self._transitions)} "
                  f"traj={self._force_trajectory_length:.3f} "
                  f"mat={self._status.swarm_maturity:.3f}")

        # Final save
        self._save_experience()
        self._status.rounds_complete = min(round_num, rounds)

        self._status.current_phase = 'idle'
        self._status.running = False
        print(f"  [EAT] Complete. "
              f"Transitions: {len(self._transitions)}, "
              f"grammar evo: {self._status.grammar_evolutions}, "
              f"trajectory: {self._force_trajectory_length:.3f}")

    def _save_experience(self):
        """Persist swarm experience, olfactory library, and L-CODEC gauges."""
        try:
            if self.engine.deep_swarm is not None:
                exp_path = os.path.join(
                    os.path.expanduser('~'), '.ck',
                    'ck_experience.json')
                os.makedirs(os.path.dirname(exp_path), exist_ok=True)
                self.engine.deep_swarm.save_experience(exp_path)
        except Exception:
            pass
        try:
            if self.engine.olfactory is not None:
                self.engine.olfactory.save()
        except Exception:
            pass
        try:
            if self.engine.lcodec is not None:
                self.engine.lcodec.save()
        except Exception:
            pass
        # Append journal entries to disk (JSONL = one JSON per line)
        try:
            if self._journal:
                os.makedirs(os.path.dirname(self._journal_path),
                            exist_ok=True)
                with open(self._journal_path, 'a', encoding='utf-8') as f:
                    for entry in self._journal:
                        f.write(json.dumps(entry) + '\n')
                self._journal.clear()
        except Exception:
            pass

    # ── Corpus Loading ──

    @staticmethod
    def _load_text_corpus(paths: List[str],
                          chunk_size: int = 500) -> List[Tuple[str, str]]:
        """Load text files and split into chunks for eating.

        Handles: .txt, .md, .py, .tex files.
        Skips binary files and files that can't be decoded.

        For Bible text (tab-separated ref\\tverse):
            Groups verses into paragraph-sized chunks (~chunk_size chars).
        For code (.py):
            Splits at function/class boundaries.
        For prose (.md, .txt, .tex):
            Splits at paragraph breaks (double newline).

        Args:
            paths: list of file paths or directory paths
            chunk_size: target characters per chunk (approximate)

        Returns: list of (filename, chunk_text) pairs.
        """
        chunks: List[Tuple[str, str]] = []
        TEXT_EXTS = {'.txt', '.md', '.py', '.tex', '.json'}

        all_files: List[Path] = []
        for p in paths:
            path = Path(p)
            if path.is_file():
                all_files.append(path)
            elif path.is_dir():
                for ext in TEXT_EXTS:
                    all_files.extend(sorted(path.rglob(f'*{ext}')))

        for fpath in all_files:
            if fpath.suffix not in TEXT_EXTS:
                continue
            try:
                text = fpath.read_text(encoding='utf-8', errors='replace')
            except Exception:
                continue
            if not text.strip():
                continue

            fname = fpath.name

            # Bible format detection: tab-separated ref\tverse
            if '\t' in text[:200] and fpath.suffix == '.txt':
                # Bible: group verses into chunks
                current_chunk: List[str] = []
                current_len = 0
                for line in text.split('\n'):
                    line = line.strip()
                    if not line or '\t' not in line:
                        continue
                    _ref, verse = line.split('\t', 1)
                    verse = verse.replace('[', '').replace(']', '')
                    current_chunk.append(verse)
                    current_len += len(verse)
                    if current_len >= chunk_size:
                        chunks.append((fname, ' '.join(current_chunk)))
                        current_chunk = []
                        current_len = 0
                if current_chunk:
                    chunks.append((fname, ' '.join(current_chunk)))

            elif fpath.suffix == '.py':
                # Code: split at def/class boundaries
                file_chunks = CKEat._split_code(text, fname)
                chunks.extend(file_chunks)

            else:
                # Prose: split at paragraph breaks
                paragraphs = re.split(r'\n\s*\n', text)
                current_chunk_parts: List[str] = []
                current_len = 0
                for para in paragraphs:
                    para = para.strip()
                    if not para:
                        continue
                    current_chunk_parts.append(para)
                    current_len += len(para)
                    if current_len >= chunk_size:
                        chunks.append(
                            (fname, '\n\n'.join(current_chunk_parts)))
                        current_chunk_parts = []
                        current_len = 0
                if current_chunk_parts:
                    chunks.append(
                        (fname, '\n\n'.join(current_chunk_parts)))

        return chunks

    # ── Corpus Eating ──

    def eat_corpus_chunk(self, text: str,
                         filename: str) -> Optional[dict]:
        """Measure one chunk of external corpus text.

        Like eat_self_chunk but source='corpus_eat'.
        Bible verses, whitepapers, markdown docs — all enter through here.
        """
        if not text.strip():
            return None

        result = self.measure_and_absorb(text, source='corpus_eat')

        # Track transition from previous corpus measurement
        if not hasattr(self, '_prev_corpus_result'):
            self._prev_corpus_result = None
        if self._prev_corpus_result is not None:
            self.track_transition(
                self._prev_corpus_result, result, 'corpus')
        self._prev_corpus_result = result

        self._status.total_self_absorptions += 1
        return result

    # ── Study Mode ──

    def start_study(self, corpus_paths: List[str],
                    model: str = DEFAULT_MODEL,
                    rounds: int = 20,
                    topics: str = 'bible',
                    models: List[str] = None):
        """Start a deep study session with external corpus.

        CK eats the corpus (Bible, papers, docs) through L-CODEC +
        olfactory while Ollama generates structural reflections on
        related topics. The olfactory field finds cross-stream harmony
        between the corpus text and the LLM's reflections.

        Three interleaved streams:
          1. Corpus chunks (Bible verses, paper paragraphs, etc.)
          2. Ollama structural reflections on related topics
          3. CK's own voice (resonance: read→write→read)

        Args:
            corpus_paths: list of file/directory paths to eat
            model: Ollama model name
            rounds: number of study rounds
            topics: topic set ('bible', 'tig', 'physics', 'all')
            models: optional list for multi-model rotation
        """
        if self._thread is not None and self._thread.is_alive():
            print("  [STUDY] Already running (eat or study)")
            return

        # Build model list
        model_list = models if models else [model]
        available = [m for m in model_list if _ollama_available(m)]
        if not available:
            self._status.error = "No available Ollama models found"
            print(f"  [STUDY] {self._status.error}")
            return

        # Load corpus
        corpus_chunks = self._load_text_corpus(corpus_paths)
        if not corpus_chunks:
            self._status.error = "No text found in corpus paths"
            print(f"  [STUDY] {self._status.error}")
            return

        # Select topic set
        topic_list: List[str] = []
        if topics in ('bible', 'all'):
            topic_list.extend(STUDY_TOPICS_BIBLE)
        if topics in ('tig', 'all'):
            topic_list.extend(STUDY_TOPICS_TIG)
        if topics in ('physics', 'all'):
            topic_list.extend(STUDY_TOPICS_PHYSICS)
        if not topic_list:
            topic_list = STUDY_TOPICS_BIBLE  # Default

        self._stop_event.clear()
        self._status = EatStatus(
            running=True,
            total_rounds=rounds,
            model=', '.join(available),
            current_phase='study',
        )
        self._prev_corpus_result = None

        self._thread = threading.Thread(
            target=self._study_loop,
            args=(available, rounds, corpus_chunks, topic_list),
            daemon=True,
            name='ck-study',
        )
        self._thread.start()
        print(f"  [STUDY] Started: models={available}, "
              f"rounds={rounds}, corpus={len(corpus_chunks)} chunks, "
              f"topics={topics} ({len(topic_list)})")

    def _study_loop(self, models: List[str], rounds: int,
                    corpus_chunks: List[Tuple[str, str]],
                    topics: List[str]):
        """Background thread: deep study with corpus + Ollama + voice.

        Each round:
          1. Corpus chunk → measure → absorb → olfactory tick
          2. Ollama reflection on related topic → measure → absorb → tick
          3. Resonance: CK speaks from absorbed operators → measure → tick
          4. Corpus chunk → measure → absorb → olfactory tick
          5. Self chunk (CK's own code) → measure → absorb → tick
          6. Grammar evolution

        The key insight: corpus and Ollama are studying the SAME domain.
        Bible text + Ollama reflecting on 'covenant' → olfactory finds
        the cross-stream harmony in Biblical force space.
        """
        structures = list(STUDY_PROMPTS.keys())
        self_chunks = self._get_self_chunks()
        corpus_idx = 0
        self_idx = 0

        print(f"  [STUDY] Corpus: {len(corpus_chunks)} chunks")
        print(f"  [STUDY] Self: {len(self_chunks)} chunks")
        print(f"  [STUDY] Topics: {len(topics)}")
        if len(models) > 1:
            print(f"  [STUDY] Multi-model: {models}")

        _consecutive_errors = 0
        for round_num in range(1, rounds + 1):
            if self._stop_event.is_set():
                break

            self._status.rounds_complete = round_num - 1
            topic = topics[(round_num - 1) % len(topics)]
            structure = structures[(round_num - 1) % len(structures)]
            model = models[(round_num - 1) % len(models)]

            # Get corpus chunk info for logging
            corpus_fn = corpus_chunks[
                corpus_idx % len(corpus_chunks)][0] if corpus_chunks else '?'
            print(f"  [STUDY] Round {round_num}/{rounds}: "
                  f"{topic} x {structure} [{model}] "
                  f"corpus={corpus_fn}")

            try:
                # ── Corpus chunk #1 ──
                self._status.current_phase = 'corpus'
                if corpus_chunks:
                    fn, chunk = corpus_chunks[
                        corpus_idx % len(corpus_chunks)]
                    r_corpus = self.eat_corpus_chunk(chunk, fn)
                    corpus_idx += 1
                    if r_corpus:
                        self._olfactory_tick()
                        _words = len(chunk.split())
                        print(f"    [STUDY] corpus: {fn} ({_words}w) "
                              f"f={tuple(round(v, 2) for v in r_corpus['force'])}")

                        # Resonance from corpus
                        self._status.current_phase = 'resonance'
                        try:
                            vr = self._resonance_step(r_corpus)
                            if vr:
                                self._olfactory_tick()
                        except Exception:
                            pass

                if self._stop_event.is_set():
                    break

                # ── Ollama reflection on related topic ──
                self._status.current_phase = 'ollama'
                prompts = STUDY_PROMPTS.get(
                    structure, STUDY_PROMPTS['exegesis'])
                prompt_idx = hash((topic, structure)) % len(prompts)
                prompt = prompts[prompt_idx].format(topic=topic)

                text = _ollama_generate(prompt, model=model, max_tokens=512)
                if text:
                    r_ollama = self.measure_and_absorb(
                        text, source='ollama_eat')
                    if self._prev_ollama_result is not None:
                        self.track_transition(
                            self._prev_ollama_result, r_ollama, 'ollama')
                    self._prev_ollama_result = r_ollama
                    self._status.total_ollama_absorptions += 1
                    self._olfactory_tick()

                    _words = len(text.split())
                    print(f"    [STUDY] ollama: {_words}w "
                          f"still={r_ollama['stillness']:.2f} "
                          f"f={tuple(round(v, 2) for v in r_ollama['force'])}")

                    # Resonance from Ollama
                    self._status.current_phase = 'resonance'
                    try:
                        vr2 = self._resonance_step(r_ollama)
                        if vr2:
                            self._olfactory_tick()
                    except Exception:
                        pass

                if self._stop_event.is_set():
                    break

                # ── Corpus chunk #2 ──
                self._status.current_phase = 'corpus'
                if corpus_chunks:
                    fn, chunk = corpus_chunks[
                        corpus_idx % len(corpus_chunks)]
                    r_corpus2 = self.eat_corpus_chunk(chunk, fn)
                    corpus_idx += 1
                    if r_corpus2:
                        self._olfactory_tick()

                # ── Self chunk (CK's own code) ──
                self._status.current_phase = 'self'
                if self_chunks and self_idx < len(self_chunks):
                    fn, chunk = self_chunks[self_idx]
                    self.eat_self_chunk(chunk, fn)
                    self_idx += 1
                    self._olfactory_tick()
                if self_idx >= len(self_chunks):
                    self_idx = 0

                # ── Grammar evolution ──
                self._status.current_phase = 'evolve'
                self.evolve_grammar()

                _consecutive_errors = 0

            except Exception as e:
                _consecutive_errors += 1
                import traceback
                traceback.print_exc()
                print(f"  [STUDY] Round {round_num} error "
                      f"({_consecutive_errors} consecutive): {e}")
                if _consecutive_errors >= 5:
                    self._status.error = (
                        f"5 consecutive failures, last: {e}")
                    print("  [STUDY] Too many errors, stopping")
                    break
                continue

            # ── Update status ──
            self._status.total_transitions = len(self._transitions)
            self._status.force_trajectory_length = (
                self._force_trajectory_length)
            if self.engine.deep_swarm is not None:
                self._status.swarm_maturity = (
                    self.engine.deep_swarm.combined_maturity)
            if self.engine.olfactory is not None:
                self._status.olfactory_library_size = (
                    self.engine.olfactory.library_size)

            # Save every 3 rounds
            if round_num % 3 == 0:
                self._save_experience()

            print(f"  [STUDY] Round {round_num} done: "
                  f"o={self._status.total_ollama_absorptions} "
                  f"c={corpus_idx} "
                  f"s={self._status.total_self_absorptions} "
                  f"r={self._status.total_resonance_steps} "
                  f"t={len(self._transitions)} "
                  f"traj={self._force_trajectory_length:.3f} "
                  f"mat={self._status.swarm_maturity:.3f}")

        # Final save
        self._save_experience()
        self._status.rounds_complete = min(round_num, rounds)
        self._status.current_phase = 'idle'
        self._status.running = False
        print(f"  [STUDY] Complete. "
              f"Corpus chunks eaten: {corpus_idx}, "
              f"Transitions: {len(self._transitions)}, "
              f"Grammar evo: {self._status.grammar_evolutions}, "
              f"Trajectory: {self._force_trajectory_length:.3f}")

    # ── Status API ──

    def status(self) -> dict:
        """Return current eat status as a dict (for web API)."""
        return {
            'running': self._status.running,
            'rounds_complete': self._status.rounds_complete,
            'total_rounds': self._status.total_rounds,
            'model': self._status.model,
            'ollama_absorptions': self._status.total_ollama_absorptions,
            'self_absorptions': self._status.total_self_absorptions,
            'visitor_absorptions': self._status.total_visitor_absorptions,
            'resonance_steps': self._status.total_resonance_steps,
            'total_transitions': self._status.total_transitions,
            'force_trajectory_length': round(
                self._status.force_trajectory_length, 4),
            'grammar_evolutions': self._status.grammar_evolutions,
            'swarm_maturity': round(self._status.swarm_maturity, 4),
            'olfactory_library_size': (
                self._status.olfactory_library_size),
            'current_phase': self._status.current_phase,
            'error': self._status.error,
        }
