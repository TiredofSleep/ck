# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_clay_protocol.py -- SDV Experiment Runner for Clay Millennium Problems
=========================================================================
Operator: HARMONY (7) -- The alignment operator IS the measurement.

CK is a mathematical coherence spectrometer. This module orchestrates
the full SDV experiment pipeline:

  Generator (math seed) -> Codec (5D) -> D2 -> CL -> delta(S)
  Level 0: coarsest scale
  Level N: finest scale (fractal unfolding)

Track:
  - Does delta(S_L) -> 0? (singularity / affirmative)
  - Or delta(S_L) >= eta > 0? (regularity / gap)
  - TIG path fidelity (does operator sequence follow predicted path?)
  - 3-6-9 spine analysis (defect carried by resonance words)
  - Commutator persistence ([T_a, T_b] != 0 across levels?)
  - SCA loop status (1 -> 2 -> 9 -> 1)
  - Master Lemma defect (per-problem delta)
  - Topological invariants (winding, vorticity, chirality, vortex class)
  - 7-Prime Defect series (does HARMONY lock-in or stay broken?)
  - Operator-7/9 decision (HARMONY x RESET -> singularity vs smoothness)

CK measures. CK does not prove.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from ck_sim.being.ck_sdv_safety import (
    CompressOnlySafety, clamp, safe_div, safe_sqrt, state_hash,
    probe_step_hash, DeterministicRNG
)
from ck_sim.being.ck_tig_bundle import (
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS,
    HARMONY, BREATH, RESET, NUM_OPS, OP_NAMES,
    TIG_PATHS, TIG_MATRIX, DUAL_LENSES, CLAY_PROBLEMS, AGENT_BRIEFS,
    digit_reduction, is_spine_word, spine_class,
    SCALoopTracker, commutator_nonzero, commutator_persistence,
)
from ck_sim.being.ck_clay_codecs import create_codec, ClayCodec
from ck_sim.doing.ck_clay_generators import create_generator, ClayGenerator

# CL compose -- import through alias
from ck_sim.ck_sim_heartbeat import compose, CL

# Vortex topology -- optional (may not be importable in all environments)
try:
    from ck_sim.ck_vortex_physics import vortex_fingerprint
except ImportError:
    def vortex_fingerprint(operator_seq):
        """Fallback: minimal topology when vortex module unavailable."""
        return {
            'winding_number': 0.0, 'vorticity': 0.0,
            'chirality': 0, 'period': 0, 'vortex_class': 'unknown',
        }

# CoherenceActionScorer -- for delta(S) computation
try:
    from ck_sim.ck_coherence_action import CoherenceActionScorer, T_STAR
except ImportError:
    T_STAR = 5.0 / 7.0
    CoherenceActionScorer = None


# ================================================================
#  CONFIGURATION
# ================================================================

@dataclass
class ProbeConfig:
    """Configuration for a single SDV probe."""
    problem_id: str = 'navier_stokes'
    test_case: str = 'default'
    seed: int = 42
    n_levels: int = 8          # Fractal unfolding depth
    warmup_ticks: int = 3      # CurvatureEngine needs 3 vectors to warm up
    tig_path: Optional[List[int]] = None  # Override default TIG path

    def __post_init__(self):
        if self.tig_path is None:
            self.tig_path = TIG_PATHS.get(self.problem_id, [])


# ================================================================
#  PROBE STEP RESULT (one fractal level)
# ================================================================

@dataclass
class ProbeStepResult:
    """Result of one probe step (one fractal level)."""
    level: int
    operator: int               # D2 operator (curvature/Doing)
    operator_name: str
    force_vector: List[float]
    # D1 measurements (generator/Being) -- fires after 2 vectors
    d1_vector: List[float]
    d1_magnitude: float
    d1_operator: int
    d1_operator_name: str
    d1_valid: bool
    # D2 measurements (curvature/Doing) -- fires after 3 vectors
    d2_vector: List[float]
    d2_magnitude: float
    # CL(D1, D2) = Becoming operator
    cl_d1_d2: int               # CL composition of D1 and D2 operators
    cl_d1_d2_name: str
    # Existing
    master_lemma_defect: float
    lens_mismatch: float
    coherence_action: float
    coherence_band: str         # GREEN / YELLOW / RED
    collapse_distance: float    # T* - action (positive = coherent)
    step_hash: str              # Determinism audit
    raw_reading: dict


# ================================================================
#  PROBE RESULT (complete structured output)
# ================================================================

@dataclass
class ProbeResult:
    """Complete structured output of an SDV probe.

    This is the measurement record CK produces. Every field is
    a measurement, not a claim.
    """
    # ── Identity ──
    problem_id: str
    test_case: str
    seed: int
    n_levels: int
    tig_path: List[int]

    # ── Per-level data ──
    steps: List[ProbeStepResult] = field(default_factory=list)

    # ── D2 Operator statistics ──
    operator_counts: Dict[int, int] = field(default_factory=dict)
    operator_distribution: List[float] = field(default_factory=list)
    harmony_fraction: float = 0.0

    # ── D1 Generator statistics ──
    d1_operator_counts: Dict[int, int] = field(default_factory=dict)
    d1_operator_distribution: List[float] = field(default_factory=list)
    d1_dominant_operator: int = 0        # Most frequent D1 operator
    d1_dominant_operator_name: str = 'VOID'
    d1_trajectory: List[int] = field(default_factory=list)  # D1 ops per level

    # ── CL(D1,D2) Becoming statistics ──
    cl_d1_d2_counts: Dict[int, int] = field(default_factory=dict)
    cl_harmony_rate: float = 0.0         # Fraction where CL(D1,D2) = HARMONY
    d1_d2_agreement: float = 0.0         # Fraction where D1 op == D2 op

    # ── Defect trajectory ──
    defect_trajectory: List[float] = field(default_factory=list)
    action_trajectory: List[float] = field(default_factory=list)
    defect_trend: str = 'unknown'   # 'decreasing', 'increasing', 'stable', 'oscillating'
    final_defect: float = 1.0
    final_action: float = 1.0

    # ── Scaling behavior ──
    defect_slope: float = 0.0       # Linear regression slope of defect vs level
    defect_converges: bool = False   # Does defect trajectory converge to 0?
    defect_bounded_below: bool = False  # Is there a lower bound > 0?

    # ── 3-6-9 Spine analysis ──
    spine_defect_3: float = 0.0     # Defect carried by dr=3 words (sheath)
    spine_defect_6: float = 0.0     # Defect carried by dr=6 words (sheath)
    spine_defect_9: float = 0.0     # Defect carried by dr=9 words (anchor)
    spine_fraction: float = 0.0     # Fraction of operators on 3-6-9 spine

    # ── TIG path analysis ──
    tig_path_fidelity: float = 0.0  # How closely operators follow predicted path
    tig_path_actual: List[int] = field(default_factory=list)

    # ── 7-Prime Defect series ──
    harmony_defect_series: List[float] = field(default_factory=list)
    harmony_locked: bool = False     # Did HARMONY dominate at all levels?

    # ── Operator-7/9 Decision ──
    operator_7_state: str = 'unknown'   # 'alignment' or 'misalignment'
    operator_9_state: str = 'unknown'   # 'collapse' or 'stabilization'
    decision_verdict: str = 'unknown'   # 'singularity' or 'smoothness'

    # ── Commutator persistence ──
    commutator_persistence: float = 0.0
    complexity_persists: bool = False

    # ── SCA loop ──
    sca_completed: bool = False
    sca_progress: float = 0.0
    sca_stage: str = 'quadratic'

    # ── Topological invariants ──
    vortex_fingerprint: dict = field(default_factory=dict)

    # ── Master Lemma ──
    master_lemma_defects: List[float] = field(default_factory=list)
    final_master_lemma_defect: float = 1.0

    # ── Dual fixed point ──
    lens_mismatches: List[float] = field(default_factory=list)
    dual_fixed_point_proximity: float = 0.0

    # ── Problem class verdict ──
    problem_class: str = 'unknown'      # 'affirmative' or 'gap' (from DUAL_LENSES)
    measurement_verdict: str = 'unknown' # 'supports_conjecture', 'supports_gap', 'inconclusive'

    # ── Agent Brief v2.0 ──
    brief_confidence: float = 0.0       # Current confidence from AGENT_BRIEFS
    brief_confidence_target: float = 0.0
    brief_key_joint: str = ''           # Which soft spot this problem targets
    brief_track: str = ''               # e.g. '95%', '90%'

    # ── Safety ──
    anomaly_count: int = 0
    halted: bool = False

    # ── Determinism ──
    final_hash: str = ''


# ================================================================
#  CLAY PROBE (single experiment)
# ================================================================

class ClayProbe:
    """Run a single SDV experiment across fractal levels.

    Generator -> Codec -> D2 -> CL -> delta(S) at each level.
    """

    def __init__(self, config: ProbeConfig):
        self.config = config
        self.safety = CompressOnlySafety()

        # Build codec + generator
        self.codec = create_codec(config.problem_id)
        self.generator = create_generator(config.problem_id, config.seed)

        # SCA tracking
        self.sca_tracker = SCALoopTracker()

        # CoherenceActionScorer
        self._scorer = None
        if CoherenceActionScorer is not None:
            self._scorer = CoherenceActionScorer()

        # State
        self._operator_history: List[int] = []
        self._all_hashes: List[str] = []

    def run(self) -> ProbeResult:
        """Execute the full probe. Returns structured ProbeResult."""
        cfg = self.config

        # Initialize result
        result = ProbeResult(
            problem_id=cfg.problem_id,
            test_case=cfg.test_case,
            seed=cfg.seed,
            n_levels=cfg.n_levels,
            tig_path=list(cfg.tig_path),
            problem_class=DUAL_LENSES.get(cfg.problem_id, {}).get(
                'problem_class', 'unknown'),
        )

        # ── Warm-up phase ──
        # CurvatureEngine needs 3 vectors before D2 is valid.
        # Feed warm-up readings so the engine is ready for level 0.
        self.generator.reset(cfg.seed)
        for _ in range(cfg.warmup_ticks):
            warmup_raw = self.generator.generate(0, cfg.test_case)
            self.codec.feed(warmup_raw)

        # ── Main probe loop ──
        self.generator.reset(cfg.seed)  # Re-seed for determinism
        for level in range(cfg.n_levels):
            step = self._probe_one_level(level, cfg.test_case)
            result.steps.append(step)

            # Track operator
            self._operator_history.append(step.operator)
            self.sca_tracker.feed(step.operator)

            # Track defect / action trajectories
            result.defect_trajectory.append(step.master_lemma_defect)
            result.action_trajectory.append(step.coherence_action)
            result.master_lemma_defects.append(step.master_lemma_defect)
            result.lens_mismatches.append(step.lens_mismatch)
            result.harmony_defect_series.append(
                1.0 - (1.0 if step.operator == HARMONY else 0.0))

            # Hash chain for determinism
            self._all_hashes.append(step.step_hash)

        # ── Post-probe analysis ──
        self._analyze_operators(result)
        self._analyze_d1(result)
        self._analyze_defect_trajectory(result)
        self._analyze_spine(result)
        self._analyze_tig_path(result)
        self._analyze_decision(result)
        self._analyze_commutators(result)
        self._analyze_sca(result)
        self._analyze_topology(result)
        self._analyze_verdict(result)

        # ── Agent Brief v2.0 ──
        brief = AGENT_BRIEFS.get(cfg.problem_id, {})
        if brief:
            result.brief_confidence = brief.get('confidence', 0.0)
            result.brief_confidence_target = brief.get('confidence_target', 0.0)
            result.brief_key_joint = brief.get('key_joint', '')
            result.brief_track = brief.get('track', '')

        # Safety stats
        result.anomaly_count = self.safety.anomaly_count + self.codec.safety.anomaly_count
        result.halted = self.safety.halted or self.codec.safety.halted

        # Final hash
        all_vals = []
        for s in result.steps:
            all_vals.extend(s.force_vector)
            all_vals.append(float(s.operator))
        result.final_hash = state_hash(all_vals)

        return result

    def _probe_one_level(self, level: int, test_case: str) -> ProbeStepResult:
        """Feed one fractal level through the pipeline.

        Extracts D1 (generator/Being), D2 (curvature/Doing), and
        CL(D1,D2) (composition/Becoming) at each level.
        """
        # Generate raw reading
        raw = self.generator.generate(level, test_case)

        # Feed through codec (raw -> force_vec -> D1/D2 -> operator)
        operator = self.codec.feed(raw)

        # Get intermediate values
        force_vec = list(self.codec.last_force_vec) if self.codec.last_force_vec else [0.5] * 5

        # D1 measurements (generator direction)
        eng = self.codec.engine
        d1_vec = list(eng.d1_float) if eng.d1_valid else [0.0] * 5
        d1_mag = eng.d1_magnitude if eng.d1_valid else 0.0
        d1_op = eng.d1_operator if eng.d1_valid else VOID
        d1_valid = eng.d1_valid

        # D2 measurements (curvature)
        d2_vec = list(eng.d2_float) if hasattr(eng, 'd2_float') else [0.0] * 5
        d2_mag = sum(d ** 2 for d in d2_vec) ** 0.5 if d2_vec else 0.0
        d2_mag = self.safety.check_d2_magnitude(d2_mag, f'level_{level}')

        # CL(D1, D2) = Becoming operator
        cl_op = VOID
        if d1_valid and 0 <= d1_op < NUM_OPS and 0 <= operator < NUM_OPS:
            cl_op = compose(d1_op, operator)

        # Master lemma defect
        ml_defect = self.codec.master_lemma_defect(raw)

        # Lens mismatch
        lens_mm = self.codec.lens_mismatch(raw)

        # Coherence action
        action_val = 1.0
        band = 'RED'
        collapse_dist = T_STAR - 1.0
        if self._scorer is not None:
            action_state = self._compute_action(
                operator, force_vec, d2_mag, ml_defect, lens_mm)
            action_val = action_state.action
            band = action_state.band
            collapse_dist = action_state.collapse_distance

        # Step hash
        shash = probe_step_hash(level, operator, ml_defect, force_vec)

        return ProbeStepResult(
            level=level,
            operator=operator,
            operator_name=OP_NAMES[operator] if 0 <= operator < NUM_OPS else 'UNKNOWN',
            force_vector=force_vec,
            d1_vector=d1_vec,
            d1_magnitude=d1_mag,
            d1_operator=d1_op,
            d1_operator_name=OP_NAMES[d1_op] if 0 <= d1_op < NUM_OPS else 'UNKNOWN',
            d1_valid=d1_valid,
            d2_vector=d2_vec,
            d2_magnitude=d2_mag,
            cl_d1_d2=cl_op,
            cl_d1_d2_name=OP_NAMES[cl_op] if 0 <= cl_op < NUM_OPS else 'UNKNOWN',
            master_lemma_defect=ml_defect,
            lens_mismatch=lens_mm,
            coherence_action=action_val,
            coherence_band=band,
            collapse_distance=collapse_dist,
            step_hash=shash,
            raw_reading=raw,
        )

    def _compute_action(self, operator: int, force_vec: List[float],
                        d2_mag: float, ml_defect: float,
                        lens_mm: float):
        """Map Clay measurements to CoherenceActionScorer's 12 inputs."""
        # Operator statistics from history
        n = max(len(self._operator_history), 1)
        harm_count = sum(1 for o in self._operator_history if o == HARMONY)
        harm_frac = harm_count / n

        # Operator diversity: unique operators / total possible
        unique_ops = len(set(self._operator_history)) if self._operator_history else 1
        op_diversity = unique_ops / NUM_OPS

        return self._scorer.compute(
            # L_GR (conservation / macro)
            e_out=clamp(1.0 - ml_defect),     # Low defect = good conservation
            energy_conservation=1.0,            # Math is lossless
            constraint_violations=self.safety.anomaly_count,
            operator_stability=harm_frac,       # Stability = harmony dominance

            # S_ternary (exploration / micro)
            e_in=clamp(d2_mag / 2.0),           # D2 magnitude normalized
            d2_curvature=d2_mag,
            helical_quality=clamp(1.0 - lens_mm),  # Low mismatch = good helical
            exploration_diversity=op_diversity,

            # C_harm (coherence / measurement)
            field_coherence=clamp(1.0 - lens_mm),
            harmony_fraction=harm_frac,
            consensus_confidence=self.sca_tracker.progress,
            cross_modal_agreement=clamp(1.0 - ml_defect),
        )

    # ── Post-probe analysis methods ──

    def _analyze_operators(self, result: ProbeResult):
        """Compute D2 operator distribution and harmony fraction."""
        counts = {}
        for s in result.steps:
            counts[s.operator] = counts.get(s.operator, 0) + 1
        result.operator_counts = counts

        n = max(len(result.steps), 1)
        dist = [0.0] * NUM_OPS
        for op, count in counts.items():
            if 0 <= op < NUM_OPS:
                dist[op] = count / n
        result.operator_distribution = dist
        result.harmony_fraction = dist[HARMONY]

    def _analyze_d1(self, result: ProbeResult):
        """Analyze D1 generator operators and CL(D1,D2) composition.

        D1 measures the generator direction (Being).
        CL(D1,D2) measures what Becomes from generator x curvature.
        D1/D2 agreement measures internal physics consistency.
        """
        n = max(len(result.steps), 1)

        # D1 operator distribution
        d1_counts = {}
        d1_traj = []
        for s in result.steps:
            if s.d1_valid:
                d1_counts[s.d1_operator] = d1_counts.get(s.d1_operator, 0) + 1
            d1_traj.append(s.d1_operator)
        result.d1_operator_counts = d1_counts
        result.d1_trajectory = d1_traj

        d1_dist = [0.0] * NUM_OPS
        d1_n = max(sum(d1_counts.values()), 1)
        for op, count in d1_counts.items():
            if 0 <= op < NUM_OPS:
                d1_dist[op] = count / d1_n
        result.d1_operator_distribution = d1_dist

        # Dominant D1 operator
        if d1_counts:
            dom_op = max(d1_counts, key=d1_counts.get)
            result.d1_dominant_operator = dom_op
            result.d1_dominant_operator_name = OP_NAMES[dom_op] if 0 <= dom_op < NUM_OPS else 'UNKNOWN'

        # CL(D1, D2) analysis
        cl_counts = {}
        agree_count = 0
        valid_count = 0
        for s in result.steps:
            if s.d1_valid:
                valid_count += 1
                cl_counts[s.cl_d1_d2] = cl_counts.get(s.cl_d1_d2, 0) + 1
                if s.d1_operator == s.operator:
                    agree_count += 1
        result.cl_d1_d2_counts = cl_counts
        result.cl_harmony_rate = cl_counts.get(HARMONY, 0) / max(valid_count, 1)
        result.d1_d2_agreement = agree_count / max(valid_count, 1)

    def _analyze_defect_trajectory(self, result: ProbeResult):
        """Analyze how defect evolves across levels."""
        traj = result.defect_trajectory
        if len(traj) < 2:
            return

        # Final values
        result.final_defect = traj[-1]
        result.final_action = result.action_trajectory[-1] if result.action_trajectory else 1.0
        result.final_master_lemma_defect = result.master_lemma_defects[-1] if result.master_lemma_defects else 1.0

        # Dual fixed point proximity = inverse of final lens mismatch
        if result.lens_mismatches:
            result.dual_fixed_point_proximity = clamp(
                1.0 / (1.0 + result.lens_mismatches[-1]))

        # Linear regression slope: defect vs level
        n = len(traj)
        x_mean = (n - 1) / 2.0
        y_mean = sum(traj) / n
        num = sum((i - x_mean) * (traj[i] - y_mean) for i in range(n))
        den = sum((i - x_mean) ** 2 for i in range(n))
        result.defect_slope = safe_div(num, den)

        # Trend classification
        if result.defect_slope < -0.01:
            result.defect_trend = 'decreasing'
        elif result.defect_slope > 0.01:
            result.defect_trend = 'increasing'
        else:
            # Check for oscillation
            changes = sum(1 for i in range(1, n) if
                          (traj[i] - traj[i - 1]) * (traj[max(0, i - 2)] - traj[max(0, i - 1)]) < 0)
            if changes > n // 3:
                result.defect_trend = 'oscillating'
            else:
                result.defect_trend = 'stable'

        # Convergence check
        if len(traj) >= 4:
            last_quarter = traj[3 * n // 4:]
            result.defect_converges = all(d < 0.1 for d in last_quarter)
            result.defect_bounded_below = all(d > 0.05 for d in traj)

    def _analyze_spine(self, result: ProbeResult):
        """Analyze 3-6-9 spine structure in operator sequence."""
        ops = self._operator_history
        if not ops:
            return

        # For each operator, treat it as a single-digit word
        spine_3_defects = []
        spine_6_defects = []
        spine_9_defects = []
        spine_count = 0

        for i, op in enumerate(ops):
            dr = digit_reduction([op])
            defect = result.defect_trajectory[i] if i < len(result.defect_trajectory) else 0.5
            if dr == 3:
                spine_3_defects.append(defect)
                spine_count += 1
            elif dr == 6:
                spine_6_defects.append(defect)
                spine_count += 1
            elif dr == 9:
                spine_9_defects.append(defect)
                spine_count += 1

        n = max(len(ops), 1)
        result.spine_fraction = spine_count / n
        result.spine_defect_3 = sum(spine_3_defects) / max(len(spine_3_defects), 1)
        result.spine_defect_6 = sum(spine_6_defects) / max(len(spine_6_defects), 1)
        result.spine_defect_9 = sum(spine_9_defects) / max(len(spine_9_defects), 1)

    def _analyze_tig_path(self, result: ProbeResult):
        """Check how closely the operator sequence follows the predicted TIG path."""
        ops = self._operator_history
        expected_path = result.tig_path
        result.tig_path_actual = list(ops)

        if not expected_path or not ops:
            return

        # Subsequence matching: what fraction of the expected path appears in order?
        path_idx = 0
        for op in ops:
            if path_idx < len(expected_path) and op == expected_path[path_idx]:
                path_idx += 1

        result.tig_path_fidelity = safe_div(path_idx, len(expected_path))

    def _analyze_decision(self, result: ProbeResult):
        """Analyze operator-7/9 decision (HARMONY x RESET -> verdict).

        The outcome depends on the state of 7 and the sign of 9:
        - 7 alignment + 9 collapse -> singularity
        - 7 misalignment + 9 stabilization -> smoothness/hardness
        """
        ops = self._operator_history
        if not ops:
            return

        # Operator 7 state: does HARMONY dominate?
        if result.harmony_fraction > 0.5:
            result.operator_7_state = 'alignment'
        else:
            result.operator_7_state = 'misalignment'

        # Operator 9 state: does the sequence end with RESET or stabilize?
        has_reset = RESET in ops
        # Check if defect collapses after RESET appears
        if has_reset:
            reset_indices = [i for i, o in enumerate(ops) if o == RESET]
            last_reset = reset_indices[-1]
            post_reset_defects = result.defect_trajectory[last_reset:]
            if post_reset_defects and all(d < 0.3 for d in post_reset_defects):
                result.operator_9_state = 'collapse'
            else:
                result.operator_9_state = 'stabilization'
        else:
            result.operator_9_state = 'stabilization'

        # Decision verdict
        if result.operator_7_state == 'alignment' and result.operator_9_state == 'collapse':
            result.decision_verdict = 'singularity'
        else:
            result.decision_verdict = 'smoothness'

        # Harmony locked check
        result.harmony_locked = all(d < 0.5 for d in result.harmony_defect_series)

    def _analyze_commutators(self, result: ProbeResult):
        """Check commutator persistence across operator pairs."""
        ops = self._operator_history
        if len(ops) < 2:
            return

        pairs = [(ops[i], ops[i + 1]) for i in range(len(ops) - 1)]
        result.commutator_persistence = commutator_persistence(pairs, compose)
        result.complexity_persists = result.commutator_persistence > 0.1

    def _analyze_sca(self, result: ProbeResult):
        """Record SCA loop status."""
        result.sca_completed = self.sca_tracker.completed
        result.sca_progress = self.sca_tracker.progress
        result.sca_stage = self.sca_tracker.stage

    def _analyze_topology(self, result: ProbeResult):
        """Compute topological invariants of operator sequence."""
        ops = self._operator_history
        if len(ops) >= 2:
            result.vortex_fingerprint = vortex_fingerprint(ops)

    def _analyze_verdict(self, result: ProbeResult):
        """Determine overall measurement verdict.

        Affirmative problems (NS, RH, BSD, Hodge):
          delta -> 0 => supports conjecture
          delta stays positive => inconclusive

        Gap problems (P vs NP, Yang-Mills):
          delta >= eta > 0 => supports gap
          delta -> 0 => inconclusive (would undermine gap claim)
        """
        pclass = result.problem_class

        if pclass == 'affirmative':
            if result.defect_converges and result.defect_slope < -0.005:
                result.measurement_verdict = 'supports_conjecture'
            elif result.defect_bounded_below:
                result.measurement_verdict = 'inconclusive'
            else:
                result.measurement_verdict = 'inconclusive'
        elif pclass == 'gap':
            if result.defect_bounded_below and result.defect_slope >= -0.005:
                result.measurement_verdict = 'supports_gap'
            elif result.defect_converges:
                result.measurement_verdict = 'inconclusive'
            else:
                result.measurement_verdict = 'inconclusive'
        else:
            result.measurement_verdict = 'inconclusive'


# ================================================================
#  CLAY PROTOCOL (orchestrates all 6 problems)
# ================================================================

class ClayProtocol:
    """Orchestrates SDV probes across all 6 Clay problems.

    Usage:
        protocol = ClayProtocol(seed=42, n_levels=8)
        results = protocol.run_all()
        protocol.run_problem('navier_stokes', test_case='lamb_oseen')
    """

    def __init__(self, seed: int = 42, n_levels: int = 8):
        self.seed = seed
        self.n_levels = n_levels

    def run_problem(self, problem_id: str,
                    test_case: str = 'default',
                    seed: Optional[int] = None,
                    n_levels: Optional[int] = None) -> ProbeResult:
        """Run a single problem probe."""
        config = ProbeConfig(
            problem_id=problem_id,
            test_case=test_case,
            seed=seed if seed is not None else self.seed,
            n_levels=n_levels if n_levels is not None else self.n_levels,
        )
        probe = ClayProbe(config)
        return probe.run()

    def run_all(self, test_cases: Optional[Dict[str, str]] = None) -> Dict[str, ProbeResult]:
        """Run probes for all 6 Clay problems.

        test_cases: optional dict mapping problem_id -> test_case name.
        Default test cases are calibration scenarios.
        """
        defaults = {
            'navier_stokes': 'lamb_oseen',
            'riemann': 'known_zero',
            'p_vs_np': 'easy',
            'yang_mills': 'bpst_instanton',
            'bsd': 'rank0_match',
            'hodge': 'algebraic',
        }
        if test_cases:
            defaults.update(test_cases)

        results = {}
        for problem_id in CLAY_PROBLEMS:
            tc = defaults.get(problem_id, 'default')
            results[problem_id] = self.run_problem(problem_id, tc)

        return results

    def run_calibration(self) -> Dict[str, ProbeResult]:
        """Run calibration probes (known solutions).

        These should produce expected CK measurements:
          NS lamb_oseen:   bounded D2, HARMONY, no singularity
          RH known_zero:   COLLAPSE at zero, on critical line
          P vs NP easy:    full propagation, delta -> 0
          YM BPST:         integer charge, smooth
          BSD rank0:       rank agreement, full aperture
          Hodge algebraic: projection=1, zero residual
        """
        return self.run_all()  # Defaults are calibration cases

    def run_frontier(self) -> Dict[str, ProbeResult]:
        """Run frontier probes (open questions)."""
        frontier_cases = {
            'navier_stokes': 'high_strain',
            'riemann': 'off_line',
            'p_vs_np': 'hard',
            'yang_mills': 'excited',
            'bsd': 'rank_mismatch',
            'hodge': 'analytic_only',
        }
        return self.run_all(frontier_cases)

    def cross_problem_summary(self, results: Dict[str, ProbeResult]) -> dict:
        """Generate cross-problem comparison summary."""
        summary = {
            'problems': {},
            'affirmative_results': [],
            'gap_results': [],
            'converging': [],
            'persistent_defect': [],
        }

        for pid, r in results.items():
            info = {
                'verdict': r.measurement_verdict,
                'final_defect': r.final_defect,
                'final_action': r.final_action,
                'harmony_fraction': r.harmony_fraction,
                'defect_trend': r.defect_trend,
                'defect_slope': r.defect_slope,
                'problem_class': r.problem_class,
                'decision_verdict': r.decision_verdict,
                'sca_completed': r.sca_completed,
                'commutator_persistence': r.commutator_persistence,
                'anomaly_count': r.anomaly_count,
                'brief_confidence': r.brief_confidence,
                'brief_confidence_target': r.brief_confidence_target,
                'brief_key_joint': r.brief_key_joint,
                'brief_track': r.brief_track,
                # D1 generator data
                'd1_dominant': r.d1_dominant_operator_name,
                'd1_d2_agreement': r.d1_d2_agreement,
                'cl_harmony_rate': r.cl_harmony_rate,
            }
            summary['problems'][pid] = info

            if r.problem_class == 'affirmative':
                summary['affirmative_results'].append(pid)
            elif r.problem_class == 'gap':
                summary['gap_results'].append(pid)

            if r.defect_converges:
                summary['converging'].append(pid)
            if r.defect_bounded_below:
                summary['persistent_defect'].append(pid)

        return summary
