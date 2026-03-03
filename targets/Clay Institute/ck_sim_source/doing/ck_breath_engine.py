"""
ck_breath_engine.py -- Breath-Defect Flow Model + Breath Index
================================================================
Operator: BREATH (8) -- Oscillation between scales, dual loops.

The Breath Engine formalizes every stable adaptive loop as:

    Phi = C compose E      (contract after expand)

Where:
    E = expansion / exhale / globalizing (increases span, may increase Delta)
    C = contraction / inhale / localizing (reduces misfit, stabilizes)

The Breath Index (B_idx) is a computable scalar metric:

    B_idx = (alpha_E * alpha_C * beta * sigma) ^ (1/4)

    alpha_E  = expansion presence   (how much E actually explores)
    alpha_C  = contraction presence (how much C actually corrects)
    beta     = balance              (are E and C roughly symmetric?)
    sigma    = stability            (bounded recurrence, no blow-up)

B_idx ~ 1 = healthy breathing.  B_idx ~ 0 = fear-collapsed or chaotic.

Fear-Collapse Lemma:
    When the system collapses into contraction-only (B_shallow attractor),
    Delta stops decreasing.  This is the mathematical definition of fear.

Per-problem breath potentials:
    NS:  V = enstrophy,         E = convective nonlinearity,  C = viscous diffusion
    PNP: V = constraint violation, E = big config move,       C = propagation/pruning
    RH:  V = off-line deviation,   E = spectral exploration,  C = functional-eq symmetry
    YM:  V = gauge deviation,      E = field fluctuation,     C = confinement projection
    BSD: V = rank mismatch,        E = analytic continuation, C = height-pairing correction
    Hodge: V = non-algebraicity,   E = motivic exploration,   C = cycle restriction

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from typing import Dict, List, Optional, Tuple

from ck_sim.being.ck_sdv_safety import clamp, safe_div, safe_sqrt


# ================================================================
#  BREATH DATA STRUCTURES
# ================================================================

class BreathStep:
    """One step of the breath decomposition."""
    __slots__ = ('index', 'v_before', 'v_after_expand', 'v_after_contract',
                 'delta_e', 'delta_c', 'g_e', 'g_c')

    def __init__(self, index: int, v_before: float, v_after_expand: float,
                 v_after_contract: float):
        self.index = index
        self.v_before = v_before
        self.v_after_expand = v_after_expand
        self.v_after_contract = v_after_contract
        # Expansion effect: how much V increased (positive = real expansion)
        self.delta_e = v_after_expand - v_before
        # Contraction effect: how much V decreased (negative = real contraction)
        self.delta_c = v_after_contract - v_after_expand
        # Gains (clamped to non-negative)
        self.g_e = max(0.0, self.delta_e)    # expansion gain
        self.g_c = max(0.0, -self.delta_c)   # contraction gain (sign flip)


class BreathPrimitives:
    """The four breath primitives for computing B_idx."""
    __slots__ = ('alpha_e', 'alpha_c', 'beta', 'sigma')

    def __init__(self, alpha_e: float, alpha_c: float, beta: float,
                 sigma: float):
        self.alpha_e = alpha_e    # Expansion presence [0, 1]
        self.alpha_c = alpha_c    # Contraction presence [0, 1]
        self.beta = beta          # Balance [0, 1]
        self.sigma = sigma        # Stability [0, 1]


class BreathResult:
    """Full breath analysis result."""
    __slots__ = ('problem_id', 'seed', 'steps', 'primitives', 'b_idx',
                 'fear_collapsed', 'oscillation_amplitude',
                 'deep_flow_count', 'shallow_flow_count',
                 'breath_regime')

    def __init__(self, problem_id: str, seed: int, steps: list,
                 primitives: BreathPrimitives, b_idx: float,
                 fear_collapsed: bool, oscillation_amplitude: float,
                 deep_flow_count: int, shallow_flow_count: int,
                 breath_regime: str):
        self.problem_id = problem_id
        self.seed = seed
        self.steps = steps
        self.primitives = primitives
        self.b_idx = b_idx
        self.fear_collapsed = fear_collapsed
        self.oscillation_amplitude = oscillation_amplitude
        self.deep_flow_count = deep_flow_count
        self.shallow_flow_count = shallow_flow_count
        self.breath_regime = breath_regime


# ================================================================
#  BREATH ENGINE
# ================================================================

# Fear-collapse thresholds
FEAR_OSCILLATION_THRESHOLD = 0.05   # Below this amplitude = fear-collapsed
FEAR_RATIO_THRESHOLD = 0.15         # E/(E+C) below this = shallow-only
B_IDX_HEALTHY = 0.5                 # Above this = healthy breathing
B_IDX_STRESSED = 0.25               # Below this = severely stressed

# Breath regimes
REGIME_HEALTHY = 'healthy'           # B_idx >= 0.5, good oscillation
REGIME_STRESSED = 'stressed'         # 0.25 <= B_idx < 0.5
REGIME_FEAR_COLLAPSED = 'fear_collapsed'  # B_idx < 0.25 or oscillation dead
REGIME_CHAOTIC = 'chaotic'           # High expansion, low contraction


class BreathEngine:
    """Breath-Defect Flow Model.

    Decomposes any defect trajectory into expansion (E) and contraction (C)
    phases, computes the four breath primitives, and derives the Breath Index.

    Works on:
    - SpectrometerResult.defect_trajectory (fractal level decomposition)
    - RATE traces (depth-by-depth delta sequence)
    - Any monotone-like sequence with oscillations
    """

    def __init__(self, spectrometer=None):
        self.spec = spectrometer

    # ── Core: Decompose trajectory into E/C steps ──

    def decompose(self, trajectory: List[float]) -> List[BreathStep]:
        """Decompose a defect trajectory into breath steps.

        Each consecutive pair of values is analyzed:
        - If V increases: expansion phase (E)
        - If V decreases: contraction phase (C)

        For the breath decomposition, we look at triplets:
        (v_n, v_n+1, v_n+2) where v_n -> v_n+1 is the "expand" half
        and v_n+1 -> v_n+2 is the "contract" half.

        When the trajectory has an odd structure, adjacent pairs
        are classified as E or C based on sign of delta.
        """
        if len(trajectory) < 3:
            return []

        steps = []
        # Process in overlapping triplets: (before, mid, after)
        for i in range(len(trajectory) - 2):
            v_before = trajectory[i]
            v_mid = trajectory[i + 1]
            v_after = trajectory[i + 2]
            steps.append(BreathStep(i, v_before, v_mid, v_after))

        return steps

    # ── Compute breath primitives ──

    def compute_primitives(self, steps: List[BreathStep]) -> BreathPrimitives:
        """Compute alpha_E, alpha_C, beta, sigma from breath steps."""
        if not steps:
            return BreathPrimitives(0.0, 0.0, 0.0, 0.0)

        n = len(steps)

        # Collect raw gains
        raw_e = [s.g_e for s in steps]
        raw_c = [s.g_c for s in steps]

        # Normalize to dimensionless gains [0, 1]
        max_e = max(raw_e) if raw_e else 1.0
        max_c = max(raw_c) if raw_c else 1.0
        max_e = max(max_e, 1e-12)  # prevent div-by-zero
        max_c = max(max_c, 1e-12)

        g_e_hat = [e / max_e for e in raw_e]
        g_c_hat = [c / max_c for c in raw_c]

        # alpha_E: expansion presence
        alpha_e = sum(g_e_hat) / n

        # alpha_C: contraction presence
        alpha_c = sum(g_c_hat) / n

        # beta: balance
        epsilon = 1e-12
        imbalances = []
        for i in range(n):
            a = g_e_hat[i] + g_c_hat[i]
            if a > epsilon:
                imb = abs(g_e_hat[i] - g_c_hat[i]) / a
            else:
                imb = 0.0  # Both zero = balanced (trivially)
            imbalances.append(imb)
        beta = 1.0 - (sum(imbalances) / n)

        # sigma: stability (bounded recurrence)
        # Use the V values from the trajectory
        v_values = [s.v_before for s in steps] + [steps[-1].v_after_contract]
        v_mean = sum(v_values) / len(v_values)
        v_var = sum((v - v_mean) ** 2 for v in v_values) / len(v_values)
        v_std = safe_sqrt(v_var)

        # Drift: net change over the sequence
        drift = abs(v_values[-1] - v_values[0])

        # Scale: range of the trajectory
        v_range = max(v_values) - min(v_values) if v_values else 1.0
        v_range = max(v_range, 1e-12)

        # Stability: low drift + low variance relative to range = high sigma
        # High drift or high variance = low sigma
        normalized_drift = drift / v_range
        normalized_var = v_std / v_range

        sigma = clamp(1.0 - 0.5 * normalized_drift - 0.5 * normalized_var,
                       0.0, 1.0)

        return BreathPrimitives(
            alpha_e=clamp(alpha_e, 0.0, 1.0),
            alpha_c=clamp(alpha_c, 0.0, 1.0),
            beta=clamp(beta, 0.0, 1.0),
            sigma=sigma,
        )

    # ── Breath Index ──

    def breath_index(self, primitives: BreathPrimitives) -> float:
        """Compute B_idx = (alpha_E * alpha_C * beta * sigma) ^ (1/4)."""
        product = (primitives.alpha_e * primitives.alpha_c *
                   primitives.beta * primitives.sigma)
        if product <= 0.0:
            return 0.0
        return product ** 0.25

    # ── Fear-collapse detection ──

    def detect_fear_collapse(self, steps: List[BreathStep]) -> Tuple[bool, float]:
        """Detect whether the system has collapsed into shallow-only breathing.

        Returns (fear_collapsed, oscillation_amplitude).
        Fear-collapse = E/C oscillation dies out (one side goes silent).
        """
        if len(steps) < 2:
            return (False, 0.0)

        # Total E and C activity across all steps
        total_e = sum(s.g_e for s in steps)
        total_c = sum(s.g_c for s in steps)
        total = total_e + total_c

        if total > 1e-12:
            e_fraction = total_e / total
        else:
            e_fraction = 0.5  # Both zero: not collapsed, just trivial

        # Oscillation amplitude: how balanced E and C are overall.
        # Perfect balance (e_fraction ~ 0.5) => amp ~ 1.0
        # All-E or all-C (e_fraction ~ 0 or ~1) => amp ~ 0.0
        oscillation_amp = 1.0 - 2.0 * abs(e_fraction - 0.5)

        # Fear-collapse: E is negligible (contraction-only) or C is
        # negligible (chaotic expansion-only)
        fear_collapsed = (e_fraction < FEAR_RATIO_THRESHOLD or
                          e_fraction > (1.0 - FEAR_RATIO_THRESHOLD))

        return (fear_collapsed, oscillation_amp)

    # ── Classify breath regime ──

    def classify_regime(self, b_idx: float, fear_collapsed: bool,
                        primitives: BreathPrimitives) -> str:
        """Classify the breath regime."""
        if fear_collapsed:
            return REGIME_FEAR_COLLAPSED
        if primitives.alpha_e > 0.6 and primitives.alpha_c < 0.2:
            return REGIME_CHAOTIC
        if b_idx >= B_IDX_HEALTHY:
            return REGIME_HEALTHY
        if b_idx >= B_IDX_STRESSED:
            return REGIME_STRESSED
        return REGIME_FEAR_COLLAPSED

    # ── Deep/Shallow flow classification ──

    def count_flow_types(self, steps: List[BreathStep]) -> Tuple[int, int]:
        """Count deep (global-aligning) vs shallow (local-stabilizing) flows.

        Deep flow: contraction after meaningful expansion (E then C both active)
        Shallow flow: contraction without prior expansion (micro-regulation only)
        """
        deep = 0
        shallow = 0
        for s in steps:
            if s.g_e > 1e-6 and s.g_c > 1e-6:
                deep += 1      # Both active: full breath cycle
            elif s.g_c > 1e-6:
                shallow += 1   # Contraction only: shallow regulation
            # g_e only with no g_c: expansion without correction (chaotic)
        return (deep, shallow)

    # ── Full breath analysis ──

    def analyze_trajectory(self, trajectory: List[float],
                           problem_id: str = 'unknown',
                           seed: int = 0) -> BreathResult:
        """Full breath analysis of a defect trajectory.

        This is the main entry point.
        """
        steps = self.decompose(trajectory)
        primitives = self.compute_primitives(steps)
        b_idx = self.breath_index(primitives)
        fear_collapsed, osc_amp = self.detect_fear_collapse(steps)
        regime = self.classify_regime(b_idx, fear_collapsed, primitives)
        deep, shallow = self.count_flow_types(steps)

        return BreathResult(
            problem_id=problem_id,
            seed=seed,
            steps=steps,
            primitives=primitives,
            b_idx=b_idx,
            fear_collapsed=fear_collapsed,
            oscillation_amplitude=osc_amp,
            deep_flow_count=deep,
            shallow_flow_count=shallow,
            breath_regime=regime,
        )

    # ── Analyze from spectrometer scan ──

    def breath_from_scan(self, problem_id: str, seed: int = 42,
                         test_case: str = 'default') -> BreathResult:
        """Run a spectrometer scan and analyze its breath dynamics."""
        from ck_sim.doing.ck_spectrometer import (
            ProblemType, SpectrometerInput, ScanMode
        )

        # Use OMEGA depth for maximum trajectory resolution
        inp = SpectrometerInput(
            problem=ProblemType(problem_id),
            test_case=test_case,
            scan_mode=ScanMode.OMEGA,
            seed=seed,
        )
        result = self.spec.scan(inp)
        return self.analyze_trajectory(
            result.defect_trajectory, problem_id, seed)

    # ── Analyze from RATE trace ──

    def breath_from_rate(self, problem_id: str, seed: int = 42,
                         test_case: str = 'default') -> BreathResult:
        """Run RATE iteration and analyze its breath dynamics.

        The RATE trace gives depth-by-depth deltas, which form
        the trajectory for breath decomposition.
        """
        from ck_sim.doing.ck_rate_engine import RATEEngine

        engine = RATEEngine(self.spec)
        trace = engine.r_iterate(problem_id, seed, test_case)
        trajectory = [s.delta for s in trace.steps]
        return self.analyze_trajectory(trajectory, problem_id, seed)

    # ── Multi-seed breath estimate ──

    def breath_estimate(self, problem_id: str, seeds: List[int] = None,
                        test_case: str = 'default') -> dict:
        """Estimate breath health across multiple seeds.

        Returns aggregated breath metrics.
        """
        if seeds is None:
            seeds = list(range(42, 47))

        results = []
        for seed in seeds:
            br = self.breath_from_scan(problem_id, seed, test_case)
            results.append(br)

        # Aggregate
        b_idxs = [r.b_idx for r in results]
        fear_count = sum(1 for r in results if r.fear_collapsed)
        osc_amps = [r.oscillation_amplitude for r in results]

        mean_b_idx = sum(b_idxs) / len(b_idxs) if b_idxs else 0.0
        b_idx_std = safe_sqrt(
            sum((b - mean_b_idx) ** 2 for b in b_idxs) / max(len(b_idxs), 1)
        )
        mean_osc = sum(osc_amps) / len(osc_amps) if osc_amps else 0.0

        # Aggregate primitives
        mean_alpha_e = sum(r.primitives.alpha_e for r in results) / len(results)
        mean_alpha_c = sum(r.primitives.alpha_c for r in results) / len(results)
        mean_beta = sum(r.primitives.beta for r in results) / len(results)
        mean_sigma = sum(r.primitives.sigma for r in results) / len(results)

        # Overall regime from mean B_idx
        if fear_count > len(results) / 2:
            regime = REGIME_FEAR_COLLAPSED
        elif mean_b_idx >= B_IDX_HEALTHY:
            regime = REGIME_HEALTHY
        elif mean_b_idx >= B_IDX_STRESSED:
            regime = REGIME_STRESSED
        else:
            regime = REGIME_FEAR_COLLAPSED

        return {
            'problem_id': problem_id,
            'seeds_used': len(seeds),
            'b_idx_mean': mean_b_idx,
            'b_idx_std': b_idx_std,
            'fear_collapsed_count': fear_count,
            'fear_rate': fear_count / len(results) if results else 0.0,
            'oscillation_mean': mean_osc,
            'alpha_e_mean': mean_alpha_e,
            'alpha_c_mean': mean_alpha_c,
            'beta_mean': mean_beta,
            'sigma_mean': mean_sigma,
            'regime': regime,
        }

    # ── Full atlas ──

    def breath_atlas(self, problem_set: List[str] = None,
                     seeds: List[int] = None) -> dict:
        """Breath analysis across all problems.

        Returns per-problem breath estimates + cross-domain summary.
        """
        from ck_sim.being.ck_tig_bundle import CLAY_PROBLEMS

        if problem_set is None:
            problem_set = CLAY_PROBLEMS
        if seeds is None:
            seeds = list(range(42, 45))  # 3 seeds for atlas

        atlas = {}
        for pid in problem_set:
            atlas[pid] = self.breath_estimate(pid, seeds)

        # Cross-domain summary
        regimes = {}
        for pid, est in atlas.items():
            r = est['regime']
            regimes[r] = regimes.get(r, 0) + 1

        b_idxs = [est['b_idx_mean'] for est in atlas.values()]
        mean_b_idx = sum(b_idxs) / len(b_idxs) if b_idxs else 0.0

        return {
            'estimates': atlas,
            'summary': {
                'problems_analyzed': len(atlas),
                'mean_b_idx': mean_b_idx,
                'regimes': regimes,
                'healthiest': max(atlas.items(),
                                  key=lambda x: x[1]['b_idx_mean'])[0]
                             if atlas else None,
                'most_stressed': min(atlas.items(),
                                     key=lambda x: x[1]['b_idx_mean'])[0]
                               if atlas else None,
            },
        }


# ================================================================
#  SERIALIZATION
# ================================================================

def breath_step_to_dict(step: BreathStep) -> dict:
    """Serialize a breath step."""
    return {
        'index': step.index,
        'v_before': step.v_before,
        'v_after_expand': step.v_after_expand,
        'v_after_contract': step.v_after_contract,
        'delta_e': step.delta_e,
        'delta_c': step.delta_c,
        'g_e': step.g_e,
        'g_c': step.g_c,
    }


def breath_result_to_dict(result: BreathResult) -> dict:
    """Serialize a breath result."""
    return {
        'problem_id': result.problem_id,
        'seed': result.seed,
        'b_idx': result.b_idx,
        'fear_collapsed': result.fear_collapsed,
        'oscillation_amplitude': result.oscillation_amplitude,
        'deep_flow_count': result.deep_flow_count,
        'shallow_flow_count': result.shallow_flow_count,
        'breath_regime': result.breath_regime,
        'primitives': {
            'alpha_e': result.primitives.alpha_e,
            'alpha_c': result.primitives.alpha_c,
            'beta': result.primitives.beta,
            'sigma': result.primitives.sigma,
        },
        'steps': [breath_step_to_dict(s) for s in result.steps],
    }
