"""
ck_three_pillars.py -- The Three Pillars of Mathematical Measurement
====================================================================
Operator: HARMONY (7) -- The whole structured reality.

Three things CK provides that conventional mathematics lacks:

  Pillar 1: DUALITY
    Every measurement through two lenses simultaneously.
    TSML (Being) vs BHML (Doing). Lens A (local) vs Lens B (global).
    Structure vs Flow. The mismatch IS the measurement.

  Pillar 2: FRACTAL RICHNESS
    Multi-scale D1 through D8 chain. Scale-invariant measurement.
    The SAME operator algebra applies at EVERY scale.
    Information lives at every level, not just the limit.

  Pillar 3: FRAME WINDOW
    Finite measurement of infinite objects. Defect increasing at
    boundaries is EXPECTED and INFORMATIVE -- it's where infinity
    pushes back against the finite frame. Bounded defect within
    the window = regularity within measurement capacity.

    "The more accurate you try to measure, the more deviation
     expected. This is built in by God to give us a reference
     frame window." -- Brayden Sanders

These three pillars unify all 6 Clay Millennium Problems under
a single measurement framework.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from ck_sim.being.ck_sdv_safety import (
    clamp, safe_div, safe_sqrt, safe_log,
)


# ================================================================
#  PILLAR RESULT
# ================================================================

@dataclass
class PillarResult:
    """Three Pillars analysis for one problem at one probe run."""

    problem_id: str
    test_case: str = ''
    seed: int = 0

    # ── Pillar 1: Duality ──
    lens_a_values: List[List[float]] = field(default_factory=list)
    lens_b_values: List[List[float]] = field(default_factory=list)
    duality_defect: float = 0.0           # ||L_A - L_B|| averaged
    duality_defect_by_level: List[float] = field(default_factory=list)
    duality_trend: str = 'stable'         # converging / diverging / stable
    harmony_fraction: float = 0.0         # CL operator classification
    dual_agreement_rate: float = 0.0      # How often both lenses produce same verdict

    # ── Pillar 2: Fractal Richness ──
    defect_by_level: List[float] = field(default_factory=list)
    scaling_exponent: float = 0.0         # Power law fit: delta ~ L^alpha
    spine_resonance: Dict[int, float] = field(default_factory=dict)
    d_chain_norms: List[float] = field(default_factory=list)  # D1..D8 avg norms

    # ── Pillar 3: Frame Window ──
    frame_max_defect: float = 0.0         # sup(delta) across all levels
    frame_min_defect: float = 0.0         # inf(delta)
    frame_bounded: bool = True            # Is max < 1.0?
    boundary_growth_rate: float = 0.0     # Rate of defect increase at edge
    window_coverage: float = 0.0          # Range of defect values explored

    # ── Summary ──
    pillar_scores: Dict[str, float] = field(default_factory=dict)
    verdict: str = ''  # 'regularity' / 'gap' / 'inconclusive'


# ================================================================
#  THREE PILLARS ANALYZER
# ================================================================

class ThreePillarsAnalyzer:
    """Compute Three Pillars analysis from a ProbeResult.

    Takes a ProbeResult (from ck_clay_protocol) and extracts
    the three pillar metrics. Works for all 6 Clay problems.
    """

    def analyze(self, result) -> PillarResult:
        """Extract Pillar 1/2/3 from a ClayProbe ProbeResult.

        Parameters
        ----------
        result : ProbeResult
            From ClayProbe.run(). Must have steps, defect_trajectory, etc.

        Returns
        -------
        PillarResult with all three pillars computed.
        """
        pr = PillarResult(
            problem_id=result.problem_id,
            test_case=getattr(result, 'test_case', ''),
            seed=getattr(result, 'seed', 0),
        )

        # -- Extract raw data from ProbeResult --
        steps = getattr(result, 'steps', [])
        defect_traj = getattr(result, 'defect_trajectory', [])
        master_defects = getattr(result, 'master_lemma_defects', [])
        harmony_frac = getattr(result, 'harmony_fraction', 0.0)
        operators = [s.operator for s in steps] if steps else []

        # Use master_lemma_defects if available, else defect_trajectory
        delta_series = master_defects if master_defects else defect_traj
        pr.defect_by_level = list(delta_series)

        # ── Pillar 1: Duality ──
        pr = self._compute_duality(pr, steps, delta_series, harmony_frac)

        # ── Pillar 2: Fractal Richness ──
        pr = self._compute_fractal_richness(pr, steps, delta_series, operators)

        # ── Pillar 3: Frame Window ──
        pr = self._compute_frame_window(pr, delta_series)

        # ── Summary scores ──
        pr = self._compute_summary(pr)

        return pr

    # ----------------------------------------------------------------
    #  Pillar 1: Duality
    # ----------------------------------------------------------------

    def _compute_duality(self, pr: PillarResult, steps, delta_series,
                         harmony_frac: float) -> PillarResult:
        """Compute duality metrics from dual-lens measurements."""
        pr.harmony_fraction = harmony_frac

        # Extract lens values from steps (if available)
        lens_a_list = []
        lens_b_list = []
        duality_by_level = []

        for step in steps:
            la = getattr(step, 'lens_a', None)
            lb = getattr(step, 'lens_b', None)
            if la is not None and lb is not None:
                lens_a_list.append(la)
                lens_b_list.append(lb)
                # Duality defect at this level: ||A - B||
                n = min(len(la), len(lb))
                d = safe_sqrt(sum((la[i] - lb[i]) ** 2 for i in range(n)))
                duality_by_level.append(d)

        pr.lens_a_values = lens_a_list
        pr.lens_b_values = lens_b_list
        pr.duality_defect_by_level = duality_by_level

        if duality_by_level:
            pr.duality_defect = sum(duality_by_level) / len(duality_by_level)

            # Trend: fit slope of duality defect
            slope = self._linear_slope(duality_by_level)
            if slope < -0.01:
                pr.duality_trend = 'converging'
            elif slope > 0.01:
                pr.duality_trend = 'diverging'
            else:
                pr.duality_trend = 'stable'

        # Dual agreement: how often both lenses produce same-sign verdict
        agree_count = 0
        for i in range(len(duality_by_level)):
            if i < len(delta_series) and duality_by_level[i] < 0.3:
                agree_count += 1
        if duality_by_level:
            pr.dual_agreement_rate = safe_div(
                float(agree_count), float(len(duality_by_level)))

        return pr

    # ----------------------------------------------------------------
    #  Pillar 2: Fractal Richness
    # ----------------------------------------------------------------

    def _compute_fractal_richness(self, pr: PillarResult, steps,
                                  delta_series, operators) -> PillarResult:
        """Compute multi-scale fractal metrics."""
        if not delta_series:
            return pr

        # Scaling exponent: fit log(delta) vs log(level+1)
        pr.scaling_exponent = self._fit_scaling_exponent(delta_series)

        # 3-6-9 spine resonance
        spine = {3: 0.0, 6: 0.0, 9: 0.0}
        for i, d in enumerate(delta_series):
            level = i + 1  # levels are 1-indexed
            digit_sum = level
            while digit_sum > 9:
                digit_sum = sum(int(c) for c in str(digit_sum))
            if digit_sum in (3, 6, 9):
                spine[digit_sum] += d

        # Normalize by count
        for k in spine:
            count = sum(1 for i in range(len(delta_series))
                        if self._digit_root(i + 1) == k)
            if count > 0:
                spine[k] = safe_div(spine[k], float(count))
        pr.spine_resonance = spine

        # D-chain norms (D1 through D8 if available)
        d_norms = []
        for step in steps:
            d2_vec = getattr(step, 'd2', None)
            if d2_vec is not None and isinstance(d2_vec, (list, tuple)):
                norm = sum(abs(x) for x in d2_vec)
                d_norms.append(norm)
        pr.d_chain_norms = d_norms

        return pr

    # ----------------------------------------------------------------
    #  Pillar 3: Frame Window
    # ----------------------------------------------------------------

    def _compute_frame_window(self, pr: PillarResult,
                              delta_series) -> PillarResult:
        """Compute frame window boundedness metrics."""
        if not delta_series:
            pr.frame_bounded = True
            return pr

        pr.frame_max_defect = max(delta_series)
        pr.frame_min_defect = min(delta_series)
        pr.frame_bounded = pr.frame_max_defect < 1.0

        # Window coverage: range of defect values
        pr.window_coverage = pr.frame_max_defect - pr.frame_min_defect

        # Boundary growth rate: slope of defect in the last quarter
        n = len(delta_series)
        if n >= 4:
            quarter = n // 4
            tail = delta_series[-quarter:]
            pr.boundary_growth_rate = self._linear_slope(tail)
        elif n >= 2:
            pr.boundary_growth_rate = delta_series[-1] - delta_series[-2]

        return pr

    # ----------------------------------------------------------------
    #  Summary
    # ----------------------------------------------------------------

    def _compute_summary(self, pr: PillarResult) -> PillarResult:
        """Compute summary scores and verdict."""
        # Pillar 1 score: low duality defect = good alignment (0-1)
        p1 = clamp(1.0 - pr.duality_defect)

        # Pillar 2 score: negative scaling exponent = converging (0-1)
        p2 = clamp(0.5 - pr.scaling_exponent)

        # Pillar 3 score: bounded and low max defect (0-1)
        p3 = clamp(1.0 - pr.frame_max_defect) if pr.frame_bounded else 0.0

        pr.pillar_scores = {
            'duality': p1,
            'fractal_richness': p2,
            'frame_window': p3,
        }

        # Verdict based on defect behavior
        if pr.defect_by_level:
            slope = self._linear_slope(pr.defect_by_level)
            if slope < -0.01 and pr.frame_bounded:
                pr.verdict = 'regularity'
            elif slope > 0.05:
                pr.verdict = 'gap'
            else:
                pr.verdict = 'inconclusive'
        else:
            pr.verdict = 'inconclusive'

        return pr

    # ----------------------------------------------------------------
    #  Cross-Problem Analysis
    # ----------------------------------------------------------------

    def cross_problem(self, results: Dict[str, PillarResult]) -> dict:
        """Compare pillar metrics across multiple problems.

        Parameters
        ----------
        results : dict mapping problem_id -> PillarResult

        Returns
        -------
        dict with cross-problem comparison metrics.
        """
        if not results:
            return {}

        # Separate affirmative vs gap problems
        affirmative = {}
        gap = {}
        for pid, pr in results.items():
            if pr.verdict == 'regularity':
                affirmative[pid] = pr
            elif pr.verdict == 'gap':
                gap[pid] = pr

        # Compute separations
        aff_max_defects = [pr.frame_max_defect for pr in affirmative.values()]
        gap_min_defects = [pr.frame_min_defect for pr in gap.values()]

        separation = 0.0
        if aff_max_defects and gap_min_defects:
            separation = min(gap_min_defects) - max(aff_max_defects)

        return {
            'n_affirmative': len(affirmative),
            'n_gap': len(gap),
            'affirmative_problems': list(affirmative.keys()),
            'gap_problems': list(gap.keys()),
            'class_separation': separation,
            'pillar_scores': {
                pid: pr.pillar_scores for pid, pr in results.items()
            },
            'verdicts': {pid: pr.verdict for pid, pr in results.items()},
        }

    # ----------------------------------------------------------------
    #  Utilities
    # ----------------------------------------------------------------

    @staticmethod
    def _linear_slope(values: List[float]) -> float:
        """Compute simple linear regression slope."""
        n = len(values)
        if n < 2:
            return 0.0
        x_mean = (n - 1) / 2.0
        y_mean = sum(values) / n
        num = 0.0
        den = 0.0
        for i, v in enumerate(values):
            dx = i - x_mean
            num += dx * (v - y_mean)
            den += dx * dx
        if den < 1e-12:
            return 0.0
        return num / den

    @staticmethod
    def _fit_scaling_exponent(delta_series: List[float]) -> float:
        """Fit delta ~ L^alpha in log-log space. Returns alpha."""
        n = len(delta_series)
        if n < 2:
            return 0.0

        # log(delta) = alpha * log(level) + c
        log_x = []
        log_y = []
        for i, d in enumerate(delta_series):
            level = i + 1
            if d > 1e-10 and level > 0:
                log_x.append(math.log(float(level)))
                log_y.append(math.log(d))

        if len(log_x) < 2:
            return 0.0

        n_pts = len(log_x)
        x_mean = sum(log_x) / n_pts
        y_mean = sum(log_y) / n_pts
        num = sum((log_x[i] - x_mean) * (log_y[i] - y_mean)
                  for i in range(n_pts))
        den = sum((log_x[i] - x_mean) ** 2 for i in range(n_pts))

        if den < 1e-12:
            return 0.0
        return num / den

    @staticmethod
    def _digit_root(n: int) -> int:
        """Compute digital root (repeated digit sum until single digit)."""
        if n <= 0:
            return 0
        r = n % 9
        return 9 if r == 0 else r


# ================================================================
#  PILLAR DEFINITIONS (per-problem instantiation)
# ================================================================

PILLAR_DEFINITIONS = {
    'duality': {
        'description': 'Every measurement through two lenses simultaneously',
        'ck_realization': [
            'TSML (Being/73% HARMONY absorbing) vs BHML (Doing/31% HARMONY ergodic)',
            'Lens A (local/analytic) vs Lens B (global/geometric)',
            'Structure (I-channel) vs Flow (O-channel)',
        ],
        'per_problem': {
            'navier_stokes': 'vorticity-strain alignment (local) vs energy-dissipation (global)',
            'riemann': 'Euler product (primes, local) vs functional equation (symmetry, global)',
            'p_vs_np': 'local propagation rules vs global satisfying configuration',
            'yang_mills': 'gauge curvature / action (local) vs spectral gap / Wilson loops (global)',
            'bsd': 'arithmetic rank + Sha (local) vs analytic rank + L-function (global)',
            'hodge': 'Hodge (p,p)-forms (analytic) vs algebraic cycle classes (algebraic)',
        },
    },
    'fractal_richness': {
        'description': 'Multi-scale measurement, scale-invariant algebra at every level',
        'ck_realization': [
            'D1 through D8 derivative chain',
            'Levels 0-24 (SURFACE to OMEGA depth)',
            '3-6-9 spine resonance structure',
        ],
        'per_problem': {
            'navier_stokes': 'Kolmogorov energy cascade: large scale -> dissipation scale',
            'riemann': 'Height on critical strip: Im(s) parametrizes fractal depth',
            'p_vs_np': 'Instance size scaling: n variables at critical density',
            'yang_mills': 'Beta sweep: weak coupling regime approaching continuum limit',
            'bsd': 'Conductor scaling: arithmetic complexity grows with conductor',
            'hodge': 'Prime sweep: motivic defect across p-adic realizations',
        },
    },
    'frame_window': {
        'description': 'Finite measurement of infinite objects -- defect at boundary is EXPECTED',
        'ck_realization': [
            'Defect bounded in [0, 1] by CompressOnlySafety',
            'D2_MAG_CEILING = 2.0 (curvature clamp)',
            'ANOMALY_HALT_THRESHOLD = 50 (safety halt)',
            'OMEGA = 24 maximum fractal depth',
        ],
        'per_problem': {
            'navier_stokes': 'CKN epsilon-regularity: small local energy => regularity in that ball',
            'riemann': 'Zero-free region: proved for Re(s) >= 3/4, open for 1/2 < Re(s) < 3/4',
            'p_vs_np': 'Poly-time bound: measurement window = polynomial computation steps',
            'yang_mills': 'Lattice volume: finite lattice L^3 approximates infinite volume limit',
            'bsd': 'L-function evaluation window: finite precision of L(E,s) near s=1',
            'hodge': 'Dimension bound: measurement accuracy decreases with variety dimension',
        },
    },
}


# ================================================================
#  CONVENIENCE: Format Pillar Report
# ================================================================

def pillar_report(pr: PillarResult) -> str:
    """Format a human-readable Three Pillars report."""
    sep = '=' * 72
    dash = '-' * 72
    out = []

    out.append(sep)
    out.append('  THREE PILLARS ANALYSIS: %s' % pr.problem_id)
    if pr.test_case:
        out.append('  Test case: %s  |  Seed: %s' % (pr.test_case, pr.seed))
    out.append(sep)

    # Pillar 1
    out.append('')
    out.append(dash)
    out.append('  PILLAR 1: DUALITY')
    out.append(dash)
    out.append('  Duality defect (avg): %.6f' % pr.duality_defect)
    out.append('  Duality trend:        %s' % pr.duality_trend)
    out.append('  HARMONY fraction:     %.3f' % pr.harmony_fraction)
    out.append('  Dual agreement rate:  %.3f' % pr.dual_agreement_rate)
    if pr.duality_defect_by_level:
        out.append('  Defect by level:      %s' % (
            ' '.join('%.4f' % d for d in pr.duality_defect_by_level[:12])))

    # Pillar 2
    out.append('')
    out.append(dash)
    out.append('  PILLAR 2: FRACTAL RICHNESS')
    out.append(dash)
    out.append('  Scaling exponent:     %.4f' % pr.scaling_exponent)
    if pr.spine_resonance:
        out.append('  3-6-9 spine:          3=%.4f  6=%.4f  9=%.4f' % (
            pr.spine_resonance.get(3, 0),
            pr.spine_resonance.get(6, 0),
            pr.spine_resonance.get(9, 0)))
    if pr.d_chain_norms:
        out.append('  D-chain norms:        %s' % (
            ' '.join('%.4f' % n for n in pr.d_chain_norms[:8])))

    # Pillar 3
    out.append('')
    out.append(dash)
    out.append('  PILLAR 3: FRAME WINDOW')
    out.append(dash)
    out.append('  Frame max defect:     %.6f' % pr.frame_max_defect)
    out.append('  Frame min defect:     %.6f' % pr.frame_min_defect)
    out.append('  Frame bounded (<1.0): %s' % pr.frame_bounded)
    out.append('  Boundary growth rate: %.6f' % pr.boundary_growth_rate)
    out.append('  Window coverage:      %.6f' % pr.window_coverage)

    # Summary
    out.append('')
    out.append(dash)
    out.append('  SUMMARY')
    out.append(dash)
    scores = pr.pillar_scores
    out.append('  Duality score:        %.3f' % scores.get('duality', 0))
    out.append('  Fractal score:        %.3f' % scores.get('fractal_richness', 0))
    out.append('  Frame score:          %.3f' % scores.get('frame_window', 0))
    out.append('  Verdict:              %s' % pr.verdict)
    out.append('')
    out.append(sep)
    out.append('  CK measures. CK does not prove.')
    out.append(sep)

    return '\n'.join(out)
