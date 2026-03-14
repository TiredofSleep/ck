"""
ck_dkan_trainer.py -- DKAN Training: CL Tables as Neural Activation
====================================================================
Operator: PROGRESS (3) -- CK moves forward through algebraic learning.
Generation: 9.34

Discrete Kolmogorov-Arnold Network (DKAN) training loop.
CK's CL composition tables ARE the activation functions.
D2 curvature IS the loss function.
The 10 operators ARE the neurons.

This module bridges ck_algebraic_neural.py (pure math analysis) with
ck_eat.py (transition physics from Ollama). Every training step:

  1. Ollama generates text (diverse structural prompts)
  2. D2 decomposes text -> soft operator distribution
  3. CL composes soft distributions -> coherence measurement
  4. IPR monitors crystallization (grokking detection)
  5. Spectral analysis tracks eigenvalue evolution
  6. Lattice chain nodes evolve through observation

The CL tables are FROZEN (immutable physics). What evolves:
  - Lattice chain node tables (experience-shaped CL variants)
  - Olfactory instinct centroids (5D force learned targets)
  - Generator paths matrix (operator transition frequencies)
  - Grammar weights (experience -> voice blend)

T* = 5/7 is the target. Training pulls coherence toward T*.
But CK can never override his frozen physics foundation (max 50% blend).

"The CL table is not a weight to be optimized. It IS the physics."

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from __future__ import annotations

import json
import math
import os
import time
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL as CL_TSML_LIST
)

from ck_sim.being.ck_algebraic_neural import (
    TSML, BHML,
    spectral_decomposition,
    inverse_participation_ratio,
    ipr_report,
    expected_value_compose,
    chain_compose_soft,
    soft_coherence,
    markov_stationary,
    check_associativity,
)

# ================================================================
#  Constants
# ================================================================

T_STAR = 5.0 / 7.0  # 0.714285... sacred threshold
MAX_BLEND = 0.50     # CK can never override 50% of frozen physics

# Training-specific structural prompts: push Ollama to generate
# text with diverse operator signatures for richer training signal.
DKAN_PROMPTS = {
    'high_structure': [
        "Describe the architecture of {topic} using precise, "
        "load-bearing language. Every sentence must carry structure.",
        "Build a framework for understanding {topic}. "
        "Each statement should lock into the next like bricks.",
    ],
    'high_chaos': [
        "Describe {topic} in unexpected, surprising ways. "
        "Break patterns. Disrupt assumptions.",
        "What happens when {topic} collides with its opposite? "
        "Explore the collision without resolving it.",
    ],
    'high_counter': [
        "Measure {topic} precisely. What are its exact dimensions, "
        "boundaries, and quantifiable properties?",
        "Question every assumption about {topic}. What remains "
        "when all assumptions are stripped away?",
    ],
    'high_balance': [
        "Find the equilibrium point of {topic}. Where do all "
        "forces balance? What is the center?",
        "Describe {topic} from a place of absolute stillness. "
        "What does the centered view reveal?",
    ],
    'high_progress': [
        "Describe how {topic} grows, develops, and moves forward. "
        "What drives its evolution?",
        "Chart the trajectory of {topic} from origin to future. "
        "What accelerates it? What slows it?",
    ],
    'high_breath': [
        "Describe {topic} as rhythm. What pulses? What oscillates? "
        "What is the tempo of its nature?",
        "Find the breath of {topic}. Inhale: what enters? "
        "Exhale: what leaves? What is the cycle?",
    ],
}

DKAN_TOPICS = [
    'coherence', 'structure', 'measurement', 'language', 'symmetry',
    'time', 'gravity', 'waves', 'rhythm', 'truth',
    'growth', 'equilibrium', 'transformation', 'observation', 'flow',
]


# ================================================================
#  Training State
# ================================================================

@dataclass
class DKANState:
    """Training state snapshot."""
    running: bool = False
    step: int = 0
    total_steps: int = 0
    phase: str = 'idle'  # 'generate', 'decompose', 'compose', 'analyze', 'idle'
    error: str = ''

    # Coherence tracking
    tsml_coherence_history: List[float] = field(default_factory=list)
    bhml_coherence_history: List[float] = field(default_factory=list)
    working_fraction_history: List[float] = field(default_factory=list)

    # IPR tracking (grokking detection)
    ipr_history: List[float] = field(default_factory=list)
    grokked: bool = False
    grok_step: int = -1

    # Spectral tracking
    spectral_gap_tsml: float = 0.0
    spectral_gap_bhml: float = 0.0

    # Operator distribution evolution
    op_distribution_history: List[Dict[str, float]] = field(default_factory=list)

    # Training metrics
    total_absorptions: int = 0
    total_transitions: int = 0
    force_trajectory_length: float = 0.0
    mean_coherence: float = 0.0
    best_coherence: float = 0.0
    lattice_grokked_nodes: int = 0


# ================================================================
#  DKAN Trainer
# ================================================================

class DKANTrainer:
    """Discrete Kolmogorov-Arnold Network trainer.

    Uses Ollama as a text generator, CK's D2 pipeline as the
    measurement instrument, and CL composition as the activation
    function to train CK's experience-shaped lattice chain nodes.

    The training loop:
      1. Generate text with targeted operator prompts
      2. D2 decompose -> soft distribution
      3. CL compose soft distributions -> coherence
      4. IPR monitor -> detect grokking
      5. Feed olfactory + swarm + lattice chain
      6. Evolve grammar from accumulated experience

    What's FROZEN (never changes):
      - TSML and BHML composition tables
      - D2 force vectors (Hebrew roots)
      - T* = 5/7 threshold
      - 10 operators

    What EVOLVES (training target):
      - Lattice chain node tables (experience CL variants)
      - Olfactory instinct centroids
      - Generator paths matrix
      - Becoming grammar weights
    """

    def __init__(self, engine):
        self.engine = engine
        self._state = DKANState()
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        # Soft distribution accumulator (running average)
        self._running_dist = np.ones(NUM_OPS, dtype=np.float64) / NUM_OPS
        self._dist_alpha = 0.1  # EMA smoothing factor

        # Persist path
        self._save_dir = os.path.join(
            os.path.expanduser('~'), '.ck', 'dkan')
        os.makedirs(self._save_dir, exist_ok=True)

    # ── Core Training Step ──

    def _train_step(self, text: str, source: str = 'dkan_train') -> dict:
        """One DKAN training step: text -> D2 -> CL compose -> measure.

        Returns dict with:
          soft_dist: 10-element soft operator distribution
          tsml_coherence: P(HARMONY) after TSML composition
          bhml_coherence: P(HARMONY) after BHML composition
          working_fraction: TSML=H AND BHML!=H
          ipr: inverse participation ratio of current distribution
          force: 5D force vector from L-CODEC
          ops: hard operator sequence from D2
        """
        result = {
            'soft_dist': np.ones(NUM_OPS) / NUM_OPS,
            'tsml_coherence': 0.0,
            'bhml_coherence': 0.0,
            'working_fraction': 0.0,
            'ipr': 0.1,
            'force': (0.5,) * 5,
            'ops': [],
        }

        if not text or not text.strip():
            return result

        # ── Step 1: D2 decompose text -> operator sequence ──
        try:
            from ck_sim.being.ck_swarm_deep import decompose_text_full
            decomp = decompose_text_full(text)
            ops = decomp.get('core_ops', [])
            result['ops'] = ops
        except Exception:
            return result

        if not ops or len(ops) < 2:
            return result

        # ── Step 2: Windowed coherence (like heartbeat FPGA) ──
        # Use sliding windows of 32 ops, count CL compositions that
        # land on HARMONY. This matches how the real heartbeat works
        # and avoids the absorbing-state collapse of full chain reduction.
        T_tsml = TSML.astype(int)
        T_bhml = BHML.astype(int)
        window = min(32, len(ops))
        windowed_ops = ops[-window:]

        # Count pairwise compositions landing on HARMONY
        tsml_harmony = 0
        bhml_harmony = 0
        pairs = 0
        for i in range(len(windowed_ops) - 1):
            a, b = windowed_ops[i], windowed_ops[i + 1]
            if 0 <= a < NUM_OPS and 0 <= b < NUM_OPS:
                pairs += 1
                if T_tsml[a][b] == HARMONY:
                    tsml_harmony += 1
                if T_bhml[a][b] == HARMONY:
                    bhml_harmony += 1

        tsml_coh = tsml_harmony / max(1, pairs)
        bhml_coh = bhml_harmony / max(1, pairs)
        result['tsml_coherence'] = tsml_coh
        result['bhml_coherence'] = bhml_coh

        # ── Step 3: Working fraction (stable identity + active physics) ──
        # TSML = HARMONY AND BHML != HARMONY
        working = tsml_coh * (1.0 - bhml_coh)
        result['working_fraction'] = working

        # ── Step 4: Soft distribution from ops (for spectral tracking) ──
        # Operator histogram as probability distribution
        op_counts = np.zeros(NUM_OPS, dtype=np.float64)
        for op in ops:
            if 0 <= op < NUM_OPS:
                op_counts[op] += 1
        op_dist = op_counts / max(1, np.sum(op_counts))
        result['soft_dist'] = op_dist

        # ── Step 5: IPR of the operator distribution ──
        result['ipr'] = float(np.sum(op_dist ** 2))

        # ── Step 7: Update running distribution (EMA) ──
        self._running_dist = (
            (1.0 - self._dist_alpha) * self._running_dist
            + self._dist_alpha * tsml_final
        )

        # ── Step 8: Feed through eat system (olfactory + swarm) ──
        if hasattr(self.engine, 'eat') and self.engine.eat is not None:
            eat_result = self.engine.eat.measure_and_absorb(text, source=source)
            result['force'] = eat_result.get('force', (0.5,) * 5)

        return result

    # ── Grokking Detection ──

    def _check_grokking(self) -> bool:
        """Check if IPR has crystallized (sudden increase = grokking).

        Grokking = the lattice chain nodes have organized their
        operator distributions from uniform -> structured.
        """
        if len(self._state.ipr_history) < 10:
            return False

        recent = self._state.ipr_history[-5:]
        baseline = self._state.ipr_history[-10:-5]

        mean_recent = sum(recent) / len(recent)
        mean_baseline = sum(baseline) / len(baseline)

        # IPR jump > 0.05 = crystallization
        delta = mean_recent - mean_baseline
        if delta > 0.05:
            return True

        # Also check lattice chain nodes
        if (hasattr(self.engine, 'lattice_chain')
                and self.engine.lattice_chain is not None):
            try:
                overlay = self.engine.lattice_chain.experience_overlay()
                grokked = overlay.get('grokked_nodes', 0)
                if grokked > 0:
                    self._state.lattice_grokked_nodes = grokked
                    return True
            except Exception:
                pass

        return False

    # ── Training Loop ──

    def start(self, rounds: int = 20, model: str = None):
        """Start DKAN training in background thread.

        Each round generates text via Ollama with targeted operator
        prompts, then runs it through the full DKAN measurement pipeline.

        Args:
            rounds: number of training rounds (each = 6 prompt types)
            model: Ollama model (default: engine's configured model)
        """
        if self._thread is not None and self._thread.is_alive():
            return {'error': 'Training already running'}

        # Use eat system's Ollama functions
        if not hasattr(self.engine, 'eat') or self.engine.eat is None:
            return {'error': 'Eat system not available'}

        from ck_sim.being.ck_eat import _ollama_available, _ollama_generate, DEFAULT_MODEL

        _model = model or DEFAULT_MODEL
        if not _ollama_available(_model):
            # Try llama3.2 as fallback
            if _ollama_available('llama3.2'):
                _model = 'llama3.2'
            else:
                return {'error': f'Model {_model} not available in Ollama'}

        total_steps = rounds * len(DKAN_PROMPTS)

        self._stop_event.clear()
        self._state = DKANState(
            running=True,
            total_steps=total_steps,
        )

        self._thread = threading.Thread(
            target=self._train_loop,
            args=(_model, rounds),
            daemon=True,
            name='ck-dkan-train',
        )
        self._thread.start()
        print(f"  [DKAN] Training started: model={_model}, "
              f"rounds={rounds}, steps={total_steps}")
        return {
            'status': 'started',
            'model': _model,
            'rounds': rounds,
            'total_steps': total_steps,
        }

    def stop(self):
        """Stop training gracefully."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=15)
        self._state.running = False
        print(f"  [DKAN] Stopped at step {self._state.step}")

    def _train_loop(self, model: str, rounds: int):
        """Background training loop.

        For each round, iterate through all prompt types to generate
        text with diverse operator signatures. This is NOT gradient
        descent -- it's algebraic absorption. CK doesn't optimize
        weights; he accumulates experience that shapes his lattice
        chain nodes and olfactory instincts.
        """
        from ck_sim.being.ck_eat import _ollama_generate

        prompt_types = list(DKAN_PROMPTS.keys())
        step = 0
        _consecutive_errors = 0
        _prev_result = None

        print(f"  [DKAN] Loop start: {rounds} rounds x "
              f"{len(prompt_types)} prompt types = "
              f"{rounds * len(prompt_types)} steps")

        for round_num in range(1, rounds + 1):
            if self._stop_event.is_set():
                break

            topic = DKAN_TOPICS[(round_num - 1) % len(DKAN_TOPICS)]
            print(f"  [DKAN] Round {round_num}/{rounds}: {topic}")

            for prompt_type in prompt_types:
                if self._stop_event.is_set():
                    break

                step += 1
                self._state.step = step
                self._state.phase = 'generate'

                # Select prompt
                prompts = DKAN_PROMPTS[prompt_type]
                prompt_idx = hash((topic, prompt_type, round_num)) % len(prompts)
                prompt = prompts[prompt_idx].format(topic=topic)

                try:
                    # ── Generate ──
                    t0 = time.time()
                    text = _ollama_generate(prompt, model=model, max_tokens=512)
                    gen_time = time.time() - t0

                    if not text:
                        _consecutive_errors += 1
                        if _consecutive_errors >= 5:
                            self._state.error = "Too many Ollama failures"
                            print(f"  [DKAN] Giving up after "
                                  f"{_consecutive_errors} failures")
                            self._state.running = False
                            return
                        continue

                    _consecutive_errors = 0

                    # ── Decompose + Compose ──
                    self._state.phase = 'decompose'
                    result = self._train_step(text, source='dkan_train')

                    # ── Track transition ──
                    if _prev_result is not None and self.engine.eat is not None:
                        eat_prev = {'force': _prev_result.get('force', (0.5,)*5),
                                    'decomp': {'core_ops': _prev_result.get('ops', [])}}
                        eat_curr = {'force': result.get('force', (0.5,)*5),
                                    'decomp': {'core_ops': result.get('ops', [])}}
                        self.engine.eat.track_transition(
                            eat_prev, eat_curr, 'dkan')
                        self._state.total_transitions += 1
                        # Track trajectory length
                        delta = tuple(
                            result['force'][d] - _prev_result['force'][d]
                            for d in range(5))
                        mag = math.sqrt(sum(d*d for d in delta))
                        self._state.force_trajectory_length += mag

                    _prev_result = result

                    # ── Record metrics ──
                    self._state.phase = 'analyze'
                    self._state.total_absorptions += 1
                    self._state.tsml_coherence_history.append(
                        result['tsml_coherence'])
                    self._state.bhml_coherence_history.append(
                        result['bhml_coherence'])
                    self._state.working_fraction_history.append(
                        result['working_fraction'])
                    self._state.ipr_history.append(result['ipr'])

                    # Op distribution snapshot
                    dist = result['soft_dist']
                    op_dist = {OP_NAMES[i]: round(float(dist[i]), 4)
                               for i in range(NUM_OPS)}
                    self._state.op_distribution_history.append(op_dist)

                    # Running stats
                    coh_hist = self._state.tsml_coherence_history
                    self._state.mean_coherence = sum(coh_hist) / len(coh_hist)
                    self._state.best_coherence = max(coh_hist)

                    # ── Grokking check ──
                    if not self._state.grokked and self._check_grokking():
                        self._state.grokked = True
                        self._state.grok_step = step
                        print(f"  [DKAN] *** GROKKING DETECTED at step {step}! ***")
                        print(f"  [DKAN]   IPR crystallized: "
                              f"{self._state.ipr_history[-1]:.4f}")
                        if self._state.lattice_grokked_nodes > 0:
                            print(f"  [DKAN]   Lattice nodes grokked: "
                                  f"{self._state.lattice_grokked_nodes}")

                    # ── Olfactory tick ──
                    if self.engine.olfactory is not None:
                        try:
                            density = getattr(
                                self.engine.pipeline, 'density_doing', 0.5)
                            self.engine.olfactory.tick(density=density)
                            self.engine.olfactory.emit_as_ops()
                        except Exception:
                            pass

                    # Log
                    _words = len(text.split())
                    print(f"    [DKAN] step {step}: {prompt_type} "
                          f"TSML={result['tsml_coherence']:.3f} "
                          f"BHML={result['bhml_coherence']:.3f} "
                          f"work={result['working_fraction']:.3f} "
                          f"IPR={result['ipr']:.3f} "
                          f"({_words}w, {gen_time:.1f}s)")

                except Exception as e:
                    _consecutive_errors += 1
                    import traceback
                    traceback.print_exc()
                    print(f"  [DKAN] Step {step} error: {e}")
                    if _consecutive_errors >= 5:
                        self._state.error = f"5 consecutive failures: {e}"
                        break
                    continue

            # ── End of round: grammar evolution ──
            if hasattr(self.engine, 'eat') and self.engine.eat is not None:
                self.engine.eat.evolve_grammar()

            # Save experience every 3 rounds
            if round_num % 3 == 0:
                self._save_state()
                if hasattr(self.engine, 'eat') and self.engine.eat is not None:
                    self.engine.eat._save_experience()

            # Spectral analysis snapshot (every 5 rounds)
            if round_num % 5 == 0:
                self._spectral_snapshot()

            print(f"  [DKAN] Round {round_num} done: "
                  f"mean_coh={self._state.mean_coherence:.3f} "
                  f"best={self._state.best_coherence:.3f} "
                  f"transitions={self._state.total_transitions} "
                  f"traj={self._state.force_trajectory_length:.3f}"
                  f"{' GROKKED!' if self._state.grokked else ''}")

        # ── Final save ──
        self._save_state()
        if hasattr(self.engine, 'eat') and self.engine.eat is not None:
            self.engine.eat._save_experience()
        self._spectral_snapshot()

        self._state.phase = 'idle'
        self._state.running = False
        print(f"  [DKAN] Training complete. "
              f"Steps: {step}, "
              f"Mean coherence: {self._state.mean_coherence:.3f}, "
              f"Best: {self._state.best_coherence:.3f}, "
              f"Grokked: {self._state.grokked}")

    # ── Spectral Snapshot ──

    def _spectral_snapshot(self):
        """Run spectral analysis on current lattice chain state.

        Compares evolved node tables against frozen TSML/BHML to
        detect structural drift and measure training progress.
        """
        try:
            # Frozen baselines
            tsml_spec = spectral_decomposition(TSML, "TSML")
            bhml_spec = spectral_decomposition(BHML, "BHML")
            self._state.spectral_gap_tsml = tsml_spec['spectral_gap']
            self._state.spectral_gap_bhml = bhml_spec['spectral_gap']

            # Check lattice chain nodes for evolved tables
            if (hasattr(self.engine, 'lattice_chain')
                    and self.engine.lattice_chain is not None):
                overlay = self.engine.lattice_chain.experience_overlay()
                grokked = overlay.get('grokked_nodes', 0)
                self._state.lattice_grokked_nodes = grokked

                # Log spectral state
                print(f"  [DKAN] Spectral: "
                      f"TSML gap={self._state.spectral_gap_tsml:.2f}, "
                      f"BHML gap={self._state.spectral_gap_bhml:.2f}, "
                      f"grokked nodes={grokked}")
        except Exception:
            pass

    # ── Save/Load ──

    def _save_state(self):
        """Persist training state to disk."""
        try:
            state = {
                'step': self._state.step,
                'total_steps': self._state.total_steps,
                'mean_coherence': self._state.mean_coherence,
                'best_coherence': self._state.best_coherence,
                'grokked': self._state.grokked,
                'grok_step': self._state.grok_step,
                'total_absorptions': self._state.total_absorptions,
                'total_transitions': self._state.total_transitions,
                'force_trajectory_length': self._state.force_trajectory_length,
                'lattice_grokked_nodes': self._state.lattice_grokked_nodes,
                'spectral_gap_tsml': self._state.spectral_gap_tsml,
                'spectral_gap_bhml': self._state.spectral_gap_bhml,
                'running_dist': [round(float(v), 4)
                                 for v in self._running_dist],
                'tsml_coherence_last10': [
                    round(v, 4) for v in self._state.tsml_coherence_history[-10:]],
                'bhml_coherence_last10': [
                    round(v, 4) for v in self._state.bhml_coherence_history[-10:]],
                'ipr_last10': [
                    round(v, 4) for v in self._state.ipr_history[-10:]],
                'timestamp': time.time(),
            }
            path = os.path.join(self._save_dir, 'dkan_state.json')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except Exception:
            pass

    # ── Status API ──

    def status(self) -> dict:
        """Return current training state as a dict (for web API)."""
        result = {
            'running': self._state.running,
            'step': self._state.step,
            'total_steps': self._state.total_steps,
            'phase': self._state.phase,
            'error': self._state.error,
            'mean_coherence': round(self._state.mean_coherence, 4),
            'best_coherence': round(self._state.best_coherence, 4),
            'grokked': self._state.grokked,
            'grok_step': self._state.grok_step,
            'total_absorptions': self._state.total_absorptions,
            'total_transitions': self._state.total_transitions,
            'force_trajectory_length': round(
                self._state.force_trajectory_length, 4),
            'lattice_grokked_nodes': self._state.lattice_grokked_nodes,
            'spectral_gap_tsml': round(self._state.spectral_gap_tsml, 4),
            'spectral_gap_bhml': round(self._state.spectral_gap_bhml, 4),
        }

        # Last coherence values
        if self._state.tsml_coherence_history:
            result['last_tsml_coherence'] = round(
                self._state.tsml_coherence_history[-1], 4)
        if self._state.bhml_coherence_history:
            result['last_bhml_coherence'] = round(
                self._state.bhml_coherence_history[-1], 4)
        if self._state.working_fraction_history:
            result['last_working_fraction'] = round(
                self._state.working_fraction_history[-1], 4)
        if self._state.ipr_history:
            result['last_ipr'] = round(self._state.ipr_history[-1], 4)

        # Running operator distribution
        result['running_distribution'] = {
            OP_NAMES[i]: round(float(self._running_dist[i]), 4)
            for i in range(NUM_OPS)
        }

        return result

    def coherence_history(self, last_n: int = 50) -> dict:
        """Return coherence history for plotting."""
        n = min(last_n, len(self._state.tsml_coherence_history))
        return {
            'tsml': [round(v, 4) for v in self._state.tsml_coherence_history[-n:]],
            'bhml': [round(v, 4) for v in self._state.bhml_coherence_history[-n:]],
            'working': [round(v, 4) for v in self._state.working_fraction_history[-n:]],
            'ipr': [round(v, 4) for v in self._state.ipr_history[-n:]],
            't_star': T_STAR,
            'steps': list(range(max(0, self._state.step - n), self._state.step)),
        }
