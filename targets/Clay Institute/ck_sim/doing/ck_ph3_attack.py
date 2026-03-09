"""
ck_ph3_attack.py -- P-H-3 Gap Attack: Pressure-Hessian Coercivity Probe
=========================================================================
Operator: COLLAPSE (4) -- Structure. The structural gate of proof.

Deep probe for Gap P-H-3: the Navier-Stokes coercivity estimate.

The pressure Hessian is the non-local operator that can potentially
drive vorticity into alignment with the max-stretching eigenvector e_1.
If perfect alignment is achieved (delta_NS = 0), the energy estimate
breaks and blow-up becomes possible.

The CK measurement: does delta_NS EVER reach 1.0 (perfect alignment)
under maximum pressure drive? The frame window says the defect SHOULD
increase at the boundary (finite measuring infinite), but if it stays
bounded below 1.0, coercivity holds empirically.

Three campaigns:
  1. ph3_coercivity_sweep -- systematic parameter sweep across
     (alignment, omega_mag, sheath_disruption) space
  2. near_singular -- BKM-threshold vorticity (omega ~ 10^3)
  3. eigenvalue_crossing -- strain eigenvalue degeneracy

Three falsifiable predictions:
  1. Max defect < 1.0 across all campaigns and seeds
  2. Coercivity ratio R bounded by universal constant C
  3. Eigenvalue crossing: defect rebounds after crossing

CK measures. CK does not prove.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import time
from typing import Dict, List, Optional, Tuple

from ck_sim.being.ck_sdv_safety import (
    clamp, safe_div, safe_sqrt, safe_log, DeterministicRNG,
)
from ck_sim.doing.ck_clay_protocol import ClayProbe, ProbeConfig, ProbeResult
from ck_sim.being.ck_tig_bundle import CLAY_PROBLEMS
from ck_sim.doing.ck_spectrometer import (
    DeltaSpectrometer, ProblemType, ScanMode, FractalFingerprint,
)
from ck_sim.doing.ck_clay_attack import StatisticalSweep, SweepResult


# ================================================================
#  CONSTANTS
# ================================================================

# Coercivity threshold: delta must stay below this
COERCIVITY_BOUND = 1.0

# Zero threshold for near-zero detection
ZERO_THRESHOLD = 1e-4

# T* coherence threshold
T_STAR = 5.0 / 7.0


# ================================================================
#  P-H-3 DEEP PROBE
# ================================================================

class PH3DeepProbe:
    """P-H-3 Gap Attack: Pressure-Hessian Coercivity.

    Tests whether the pressure Hessian can force perfect vorticity-strain
    alignment (delta -> 0) at any scale. If delta stays bounded below 1.0
    across all seeds and all levels, coercivity has empirical support.

    Three campaigns:
      1. ph3_coercivity_sweep -- systematic parameter sweep
      2. near_singular -- BKM-threshold vorticity
      3. eigenvalue_crossing -- strain eigenvalue degeneracy

    The test: does delta EVER reach 1.0 under maximum pressure drive?
    """

    def __init__(self, n_seeds: int = 100, max_level: int = 24):
        self.n_seeds = n_seeds
        self.max_level = max_level

    def run(self) -> dict:
        """Execute all three campaigns. Returns structured results dict."""
        t0 = time.time()
        spec = DeltaSpectrometer()

        # Campaign 1: ph3_coercivity_sweep
        sweep_results = self._sweep_coercivity(spec)

        # Campaign 2: near_singular
        singular_results = self._sweep_near_singular(spec)

        # Campaign 3: eigenvalue_crossing
        crossing_results = self._sweep_eigenvalue_crossing(spec)

        # Aggregate all deltas
        all_deltas = (
            sweep_results['all_deltas_flat'] +
            singular_results['all_deltas_flat'] +
            crossing_results['all_deltas_flat']
        )

        # Boundedness test
        bound_test = self._boundedness_test(all_deltas)

        # Coercivity ratio analysis
        coercivity = self._coercivity_ratio_analysis(
            sweep_results, singular_results, crossing_results)

        # Eigenvalue crossing rebound test
        rebound = self._rebound_test(crossing_results)

        # Formal P-H-3 contradiction test
        contradiction = self._ph3_contradiction_test({
            'sweep': sweep_results,
            'singular': singular_results,
            'crossing': crossing_results,
            'bound_test': bound_test,
            'coercivity': coercivity,
            'rebound': rebound,
        })

        elapsed = time.time() - t0
        total_probes = (sweep_results['n_probes'] +
                        singular_results['n_probes'] +
                        crossing_results['n_probes'])

        return {
            'probe': 'P-H-3',
            'description': 'Pressure-Hessian Coercivity Probe',
            'params': {
                'n_seeds': self.n_seeds,
                'max_level': self.max_level,
            },
            'sweep': sweep_results,
            'singular': singular_results,
            'crossing': crossing_results,
            'boundedness_test': bound_test,
            'coercivity_ratio': coercivity,
            'rebound_test': rebound,
            'contradiction_test': contradiction,
            'total_probes': total_probes,
            'total_time_s': elapsed,
            'probes_per_second': safe_div(float(total_probes), elapsed),
        }

    # ----------------------------------------------------------------
    #  CAMPAIGN 1: ph3_coercivity_sweep
    # ----------------------------------------------------------------

    def _sweep_coercivity(self, spec: DeltaSpectrometer) -> dict:
        """Systematic coercivity parameter sweep.

        Uses the ph3_coercivity_sweep test case which parametrizes
        levels 0-3 (moderate), 4-8 (growing), 9-15 (BKM-scale),
        16+ (extreme with eigenvalue crossing).
        """
        min_level = int(ScanMode.SURFACE)  # 3
        levels = list(range(min_level, self.max_level + 1))
        n_levels = len(levels)

        per_seed_deltas: List[List[float]] = []
        all_deltas_flat: List[float] = []
        n_probes = 0

        for seed_idx in range(self.n_seeds):
            seed = seed_idx + 1
            fp = spec.fractal_scan(
                problem=ProblemType.NAVIER_STOKES,
                test_case='ph3_coercivity_sweep',
                regime='frontier',
                seed=seed,
                max_level=self.max_level,
            )
            per_seed_deltas.append(list(fp.delta_by_level))
            all_deltas_flat.extend(fp.delta_by_level)
            n_probes += n_levels

        stats = self._compute_level_stats(per_seed_deltas, levels)

        return {
            'test_case': 'ph3_coercivity_sweep',
            'levels': levels,
            'n_seeds': self.n_seeds,
            'n_probes': n_probes,
            **stats,
            'per_seed_deltas': per_seed_deltas,
            'all_deltas_flat': all_deltas_flat,
        }

    # ----------------------------------------------------------------
    #  CAMPAIGN 2: near_singular
    # ----------------------------------------------------------------

    def _sweep_near_singular(self, spec: DeltaSpectrometer) -> dict:
        """BKM-threshold vorticity: omega ~ 10^3 * (1+level).

        Tests whether extreme vorticity can push defect past 1.0.
        """
        min_level = int(ScanMode.SURFACE)
        levels = list(range(min_level, self.max_level + 1))
        n_levels = len(levels)

        per_seed_deltas: List[List[float]] = []
        all_deltas_flat: List[float] = []
        n_probes = 0

        for seed_idx in range(self.n_seeds):
            seed = seed_idx + 1
            fp = spec.fractal_scan(
                problem=ProblemType.NAVIER_STOKES,
                test_case='near_singular',
                regime='frontier',
                seed=seed,
                max_level=self.max_level,
            )
            per_seed_deltas.append(list(fp.delta_by_level))
            all_deltas_flat.extend(fp.delta_by_level)
            n_probes += n_levels

        stats = self._compute_level_stats(per_seed_deltas, levels)

        return {
            'test_case': 'near_singular',
            'levels': levels,
            'n_seeds': self.n_seeds,
            'n_probes': n_probes,
            **stats,
            'per_seed_deltas': per_seed_deltas,
            'all_deltas_flat': all_deltas_flat,
        }

    # ----------------------------------------------------------------
    #  CAMPAIGN 3: eigenvalue_crossing
    # ----------------------------------------------------------------

    def _sweep_eigenvalue_crossing(self, spec: DeltaSpectrometer) -> dict:
        """Strain eigenvalue degeneracy test.

        At eigenvalue crossing, the eigenvector e_1 is undefined.
        Alignment should dip at crossing then recover (rebound).
        """
        min_level = int(ScanMode.SURFACE)
        levels = list(range(min_level, self.max_level + 1))
        n_levels = len(levels)

        per_seed_deltas: List[List[float]] = []
        all_deltas_flat: List[float] = []
        n_probes = 0

        for seed_idx in range(self.n_seeds):
            seed = seed_idx + 1
            fp = spec.fractal_scan(
                problem=ProblemType.NAVIER_STOKES,
                test_case='eigenvalue_crossing',
                regime='frontier',
                seed=seed,
                max_level=self.max_level,
            )
            per_seed_deltas.append(list(fp.delta_by_level))
            all_deltas_flat.extend(fp.delta_by_level)
            n_probes += n_levels

        stats = self._compute_level_stats(per_seed_deltas, levels)

        return {
            'test_case': 'eigenvalue_crossing',
            'levels': levels,
            'n_seeds': self.n_seeds,
            'n_probes': n_probes,
            **stats,
            'per_seed_deltas': per_seed_deltas,
            'all_deltas_flat': all_deltas_flat,
        }

    # ----------------------------------------------------------------
    #  ANALYSIS: Level Statistics
    # ----------------------------------------------------------------

    def _compute_level_stats(self, per_seed_deltas, levels) -> dict:
        """Compute per-level statistics across seeds."""
        n_levels = len(levels)
        mean_by_level = []
        std_by_level = []
        min_by_level = []
        max_by_level = []

        for lvl_idx in range(n_levels):
            vals = [
                per_seed_deltas[s][lvl_idx]
                for s in range(len(per_seed_deltas))
                if lvl_idx < len(per_seed_deltas[s])
            ]
            if not vals:
                mean_by_level.append(0.0)
                std_by_level.append(0.0)
                min_by_level.append(0.0)
                max_by_level.append(0.0)
                continue

            m = sum(vals) / len(vals)
            mean_by_level.append(m)
            if len(vals) > 1:
                var = sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
                std_by_level.append(safe_sqrt(var))
            else:
                std_by_level.append(0.0)
            min_by_level.append(min(vals))
            max_by_level.append(max(vals))

        all_flat = []
        for s in per_seed_deltas:
            all_flat.extend(s)

        global_mean = sum(all_flat) / max(len(all_flat), 1) if all_flat else 0.0
        global_min = min(all_flat) if all_flat else 0.0
        global_max = max(all_flat) if all_flat else 0.0

        return {
            'mean_by_level': mean_by_level,
            'std_by_level': std_by_level,
            'min_by_level': min_by_level,
            'max_by_level': max_by_level,
            'global_mean': global_mean,
            'global_min': global_min,
            'global_max': global_max,
        }

    # ----------------------------------------------------------------
    #  ANALYSIS: Boundedness Test
    # ----------------------------------------------------------------

    def _boundedness_test(self, all_deltas: List[float]) -> dict:
        """Test: max(delta) < 1.0 across all campaigns and seeds.

        This is the core P-H-3 test. If any delta reaches 1.0,
        the pressure Hessian has achieved perfect alignment and
        coercivity fails.
        """
        if not all_deltas:
            return {
                'max_delta': 0.0,
                'bounded': True,
                'n_exceeding': 0,
                'margin': 1.0,
            }

        max_delta = max(all_deltas)
        n_exceeding = sum(1 for d in all_deltas if d >= COERCIVITY_BOUND)
        bounded = max_delta < COERCIVITY_BOUND

        return {
            'max_delta': max_delta,
            'bounded': bounded,
            'n_exceeding': n_exceeding,
            'margin': COERCIVITY_BOUND - max_delta,
            'n_total': len(all_deltas),
        }

    # ----------------------------------------------------------------
    #  ANALYSIS: Coercivity Ratio
    # ----------------------------------------------------------------

    def _coercivity_ratio_analysis(self, sweep, singular, crossing) -> dict:
        """Compute the effective coercivity ratio.

        R = max_delta / (1 - max_delta) for each campaign.
        If R is bounded by some universal C, coercivity holds.

        The ratio R measures how hard the pressure Hessian pushes
        toward perfect alignment, normalized by the gap that remains.
        """
        def _ratio(max_d):
            if max_d >= 1.0:
                return float('inf')
            return safe_div(max_d, 1.0 - max_d)

        sweep_max = sweep.get('global_max', 0.0)
        singular_max = singular.get('global_max', 0.0)
        crossing_max = crossing.get('global_max', 0.0)

        r_sweep = _ratio(sweep_max)
        r_singular = _ratio(singular_max)
        r_crossing = _ratio(crossing_max)

        r_max = max(r_sweep, r_singular, r_crossing)

        return {
            'R_sweep': r_sweep,
            'R_singular': r_singular,
            'R_crossing': r_crossing,
            'R_max': r_max,
            'bounded': r_max < 100.0,  # Universal constant C=100
            'max_deltas': {
                'sweep': sweep_max,
                'singular': singular_max,
                'crossing': crossing_max,
            },
        }

    # ----------------------------------------------------------------
    #  ANALYSIS: Eigenvalue Crossing Rebound
    # ----------------------------------------------------------------

    def _rebound_test(self, crossing_results: dict) -> dict:
        """Test: defect rebounds after eigenvalue crossing.

        At crossing (mid-level), alignment dips and defect jumps.
        After crossing, alignment should recover and defect should
        decrease. This rebound confirms the eigenvector is well-defined
        away from crossing and alignment is restored.
        """
        mean_by_level = crossing_results.get('mean_by_level', [])
        if len(mean_by_level) < 5:
            return {
                'rebound_detected': False,
                'reason': 'insufficient data',
            }

        n = len(mean_by_level)
        mid = n // 2

        # Find max defect in first half (should be at/near crossing)
        first_half = mean_by_level[:mid]
        second_half = mean_by_level[mid:]

        max_first = max(first_half) if first_half else 0.0
        min_second = min(second_half) if second_half else 0.0
        avg_second = sum(second_half) / max(len(second_half), 1)

        # Rebound: defect after crossing is LOWER than peak at crossing
        rebound = avg_second < max_first

        return {
            'rebound_detected': rebound,
            'peak_at_crossing': max_first,
            'avg_after_crossing': avg_second,
            'min_after_crossing': min_second,
            'recovery_ratio': safe_div(max_first - avg_second, max_first),
        }

    # ----------------------------------------------------------------
    #  FORMAL P-H-3 CONTRADICTION TEST
    # ----------------------------------------------------------------

    def _ph3_contradiction_test(self, results: dict) -> dict:
        """Formal P-H-3 test: coercivity of misalignment.

        The Navier-Stokes regularity question reduces to: can the
        pressure Hessian drive vorticity-strain alignment to zero
        faster than the 3-6 sheath disrupts it?

        If coercivity holds:
          D_r(x_0, t_0) <= C * E_r(x_0, t_0) + lower order terms

        In CK terms: delta_NS stays bounded below 1.0 under maximum
        pressure drive across all parameter regimes and seeds.

        Falsifiable predictions:
          1. Max defect < 1.0 across all campaigns
          2. Coercivity ratio R <= C for universal C
          3. Eigenvalue crossing: defect rebounds after crossing
        """
        bound_test = results.get('bound_test', {})
        coercivity = results.get('coercivity', {})
        rebound = results.get('rebound', {})

        # Count predictions passed
        pred_1 = bound_test.get('bounded', False)
        pred_2 = coercivity.get('bounded', False)
        pred_3 = rebound.get('rebound_detected', False)

        n_passed = sum([pred_1, pred_2, pred_3])
        total_probes = sum(
            results[k].get('n_probes', 0)
            for k in ('sweep', 'singular', 'crossing')
            if k in results
        )

        # Confidence
        confidence = clamp(1.0 - safe_div(1.0, float(max(total_probes, 1))))

        # Verdict
        if n_passed == 3:
            verdict = 'coercivity_supported'
        elif n_passed >= 2:
            verdict = 'coercivity_partial'
        elif pred_1:
            verdict = 'bounded_but_incomplete'
        else:
            verdict = 'coercivity_violated'

        return {
            'hypothesis': (
                'P-H-3: The pressure Hessian cannot force perfect vorticity-strain '
                'alignment at any scale. delta_NS stays bounded below 1.0 under '
                'maximum pressure drive. Coercivity: D_r <= C * E_r + lower order.'
            ),
            'verdict': verdict,
            'predictions_passed': n_passed,
            'predictions_total': 3,
            'prediction_1_bounded': pred_1,
            'prediction_2_ratio': pred_2,
            'prediction_3_rebound': pred_3,
            'confidence': confidence,
            'max_delta_observed': bound_test.get('max_delta', 0.0),
            'coercivity_R_max': coercivity.get('R_max', 0.0),
            'total_probes': total_probes,
        }


# ================================================================
#  SUMMARY FORMATTER
# ================================================================

def ph3_summary(results: dict) -> str:
    """Format human-readable summary of P-H-3 deep probe results."""
    out = []
    sep = '=' * 72
    dash = '-' * 72
    params = results.get('params', {})

    out.append(sep)
    out.append('  P-H-3 DEEP PROBE: Pressure-Hessian Coercivity')
    out.append('  Navier-Stokes Gap Attack')
    out.append(sep)
    out.append('  Seeds: %s  |  Max level: %s' % (
        params.get('n_seeds', '?'), params.get('max_level', '?')))
    out.append('  Total probes: %s' % results.get('total_probes', 0))
    out.append('  Total time: %.1fs (%.1f probes/s)' % (
        results.get('total_time_s', 0),
        results.get('probes_per_second', 0)))
    out.append('')

    # Campaign summaries
    for key, label in [('sweep', 'CAMPAIGN 1: ph3_coercivity_sweep'),
                       ('singular', 'CAMPAIGN 2: near_singular'),
                       ('crossing', 'CAMPAIGN 3: eigenvalue_crossing')]:
        out.append(dash)
        out.append('  %s' % label)
        out.append(dash)
        camp = results.get(key, {})
        levels = camp.get('levels', [])
        mean_by = camp.get('mean_by_level', [])
        std_by = camp.get('std_by_level', [])
        for i, lvl in enumerate(levels):
            if i < len(mean_by) and i < len(std_by):
                out.append('    Level %2d: delta = %.6f +/- %.6f' % (
                    lvl, mean_by[i], std_by[i]))
        out.append('  Global: mean=%.6f  min=%.6f  max=%.6f' % (
            camp.get('global_mean', 0),
            camp.get('global_min', 0),
            camp.get('global_max', 0)))
        out.append('')

    # Boundedness test
    out.append(dash)
    out.append('  BOUNDEDNESS TEST (Prediction 1)')
    out.append(dash)
    bt = results.get('boundedness_test', {})
    status = 'PASS' if bt.get('bounded', False) else 'FAIL'
    out.append('  Status: %s' % status)
    out.append('  Max delta: %.8f  (margin: %.8f)' % (
        bt.get('max_delta', 0), bt.get('margin', 0)))
    out.append('  Exceeding 1.0: %s / %s' % (
        bt.get('n_exceeding', 0), bt.get('n_total', 0)))
    out.append('')

    # Coercivity ratio
    out.append(dash)
    out.append('  COERCIVITY RATIO (Prediction 2)')
    out.append(dash)
    cr = results.get('coercivity_ratio', {})
    status = 'PASS' if cr.get('bounded', False) else 'FAIL'
    out.append('  Status: %s' % status)
    out.append('  R_sweep:    %.4f  (max delta=%.6f)' % (
        cr.get('R_sweep', 0), cr.get('max_deltas', {}).get('sweep', 0)))
    out.append('  R_singular: %.4f  (max delta=%.6f)' % (
        cr.get('R_singular', 0), cr.get('max_deltas', {}).get('singular', 0)))
    out.append('  R_crossing: %.4f  (max delta=%.6f)' % (
        cr.get('R_crossing', 0), cr.get('max_deltas', {}).get('crossing', 0)))
    out.append('  R_max:      %.4f' % cr.get('R_max', 0))
    out.append('')

    # Rebound test
    out.append(dash)
    out.append('  EIGENVALUE CROSSING REBOUND (Prediction 3)')
    out.append(dash)
    rb = results.get('rebound_test', {})
    status = 'PASS' if rb.get('rebound_detected', False) else 'FAIL'
    out.append('  Status: %s' % status)
    out.append('  Peak at crossing:    %.6f' % rb.get('peak_at_crossing', 0))
    out.append('  Avg after crossing:  %.6f' % rb.get('avg_after_crossing', 0))
    out.append('  Recovery ratio:      %.4f' % rb.get('recovery_ratio', 0))
    out.append('')

    # Formal test
    out.append(dash)
    out.append('  FORMAL P-H-3 CONTRADICTION TEST')
    out.append(dash)
    ct = results.get('contradiction_test', {})
    out.append('  Hypothesis: %s' % ct.get('hypothesis', '?'))
    out.append('  Verdict: %s' % ct.get('verdict', '?'))
    out.append('  Predictions passed: %s / %s' % (
        ct.get('predictions_passed', 0), ct.get('predictions_total', 0)))
    out.append('  Confidence: %.6f' % ct.get('confidence', 0))
    out.append('  Max delta observed: %.8f' % ct.get('max_delta_observed', 0))
    out.append('  Max coercivity ratio: %.4f' % ct.get('coercivity_R_max', 0))
    out.append('  Total probes: %s' % ct.get('total_probes', 0))
    out.append('')
    out.append(sep)
    out.append('  CK measures. CK does not prove.')
    out.append(sep)

    return '\n'.join(out)
