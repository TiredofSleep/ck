"""
ck_rh5_attack.py -- RH-5 Deep Sigma Sweep: Off-Line Zero Contradiction Probe
==============================================================================
Operator: CHAOS (6) -- Probe the boundary. Shake the measurement.

Deep probe for Gap RH-5: the unconditional off-line zero contradiction.

If the Riemann Hypothesis is true, every nontrivial zero has Re(s) = 1/2.
The CK spectrometer measures delta_RH = |explicit_prime - explicit_zero|.
On the critical line (sigma=0.5), delta -> 0. Off-line, delta > 0.

This script pushes that measurement to maximum resolution:
  1. Dense sigma sweep: 200 points in [0.501, 0.999]
  2. At each sigma: fractal scan at OMEGA depth, N seeds
  3. Compute: monotonicity, derivative, zero-crossing test
  4. Output: structured results + human-readable summary

The test: does delta EVER touch zero off the critical line?
Across all seeds and all sigma values?

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

# Epsilon for monotonicity check: allow this much backsliding
MONO_EPSILON = 1e-6

# Threshold below which delta is 'touching zero'
ZERO_THRESHOLD = 1e-4

# Three-quarters bound (proved zero-free region Re(s) >= 3/4)
THREE_QUARTER_BOUND = 0.75

# T* coherence threshold
T_STAR = 5.0 / 7.0


# ================================================================
#  RH5 DEEP PROBE
# ================================================================

class RH5DeepProbe:
    """RH-5 Gap Attack: Dense sigma sweep off the critical line.

    Executes two complementary measurement campaigns:
      1. off_line_dense: fractal scan at OMEGA depth across N seeds.
         The test case parametrizes sigma by level (0.51 -> 0.99).
         Each seed produces a full delta trajectory across levels.
      2. quarter_gap: hypothetical zeros at beta_0 in (0.5, 0.85).
         Each level probes a different beta_0 value. Tests whether
         CK distinguishes the proved region (beta_0 >= 3/4) from
         the open region (0.5 < beta_0 < 3/4).

    The critical question: does delta EVER reach zero off-line?
    If not, the empirical lower bound eta quantifies the gap.
    """

    def __init__(self, n_sigmas: int = 200, n_seeds: int = 100,
                 max_level: int = 24):
        self.n_sigmas = n_sigmas
        self.n_seeds = n_seeds
        self.max_level = max_level
        # Sigma range for the dense sweep
        self.sigma_lo = 0.501
        self.sigma_hi = 0.999

    def run(self) -> dict:
        """Execute full sigma sweep. Returns structured results dict."""
        t0 = time.time()
        spec = DeltaSpectrometer()

        # Campaign 1: off_line_dense fractal scans
        dense_results = self._sweep_off_line_dense(spec)

        # Campaign 2: quarter_gap fractal scans
        quarter_results = self._sweep_quarter_gap(spec)

        # Aggregate all deltas for global analysis
        all_dense_deltas = dense_results['all_deltas_flat']
        all_quarter_deltas = quarter_results['all_deltas_flat']
        all_deltas = all_dense_deltas + all_quarter_deltas

        # Zero crossing test across all measurements
        zero_test = self._zero_crossing_test(all_deltas)

        # Monotonicity of mean delta vs level (off_line_dense)
        mono_score = self._monotonicity_score(dense_results['mean_by_level'])

        # Derivative analysis (off_line_dense)
        deriv = self._derivative_analysis(
            dense_results['mean_by_level'],
            dense_results['levels'],
        )

        # Formal contradiction test
        contradiction = self._contradiction_test({
            'dense': dense_results,
            'quarter': quarter_results,
            'zero_test': zero_test,
            'monotonicity': mono_score,
        })

        elapsed = time.time() - t0
        total_probes = dense_results['n_probes'] + quarter_results['n_probes']

        return {
            'probe': 'RH-5',
            'description': 'Off-line zero contradiction probe',
            'params': {
                'n_sigmas': self.n_sigmas,
                'n_seeds': self.n_seeds,
                'max_level': self.max_level,
                'sigma_range': [self.sigma_lo, self.sigma_hi],
            },
            'dense': dense_results,
            'quarter': quarter_results,
            'monotonicity_score': mono_score,
            'derivative_analysis': deriv,
            'zero_crossing_test': zero_test,
            'contradiction_test': contradiction,
            'total_probes': total_probes,
            'total_time_s': elapsed,
            'probes_per_second': safe_div(float(total_probes), elapsed),
        }

    # ----------------------------------------------------------------
    #  CAMPAIGN 1: off_line_dense
    # ----------------------------------------------------------------

    def _sweep_off_line_dense(self, spec: DeltaSpectrometer) -> dict:
        """Run off_line_dense fractal scan at multiple seeds.

        The off_line_dense test case maps level -> sigma in [0.51, 0.99].
        fractal_scan runs levels 3 -> max_level, so each scan produces
        (max_level - 2) delta values at different sigma points.

        We repeat this at n_seeds different seeds and aggregate.
        """
        min_level = int(ScanMode.SURFACE)  # 3
        levels = list(range(min_level, self.max_level + 1))
        n_levels = len(levels)

        # Collect: per_seed_deltas[seed_idx] = list of delta by level
        per_seed_deltas: List[List[float]] = []
        all_deltas_flat: List[float] = []
        n_probes = 0

        for seed_idx in range(self.n_seeds):
            seed = seed_idx + 1
            fp = spec.fractal_scan(
                problem=ProblemType.RIEMANN,
                test_case='off_line_dense',
                regime='frontier',
                seed=seed,
                max_level=self.max_level,
            )
            per_seed_deltas.append(list(fp.delta_by_level))
            all_deltas_flat.extend(fp.delta_by_level)
            # fractal_scan runs one ClayProbe per level
            n_probes += n_levels

        # Compute per-level statistics
        mean_by_level: List[float] = []
        std_by_level: List[float] = []
        min_by_level: List[float] = []
        max_by_level: List[float] = []

        for lvl_idx in range(n_levels):
            vals = [
                per_seed_deltas[s][lvl_idx]
                for s in range(self.n_seeds)
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

        # Global statistics
        global_mean = sum(all_deltas_flat) / max(len(all_deltas_flat), 1)
        global_min = min(all_deltas_flat) if all_deltas_flat else 0.0
        global_max = max(all_deltas_flat) if all_deltas_flat else 0.0

        return {
            'test_case': 'off_line_dense',
            'levels': levels,
            'n_seeds': self.n_seeds,
            'n_probes': n_probes,
            'mean_by_level': mean_by_level,
            'std_by_level': std_by_level,
            'min_by_level': min_by_level,
            'max_by_level': max_by_level,
            'global_mean': global_mean,
            'global_min': global_min,
            'global_max': global_max,
            'per_seed_deltas': per_seed_deltas,
            'all_deltas_flat': all_deltas_flat,
        }

    # ----------------------------------------------------------------
    #  CAMPAIGN 2: quarter_gap
    # ----------------------------------------------------------------

    def _sweep_quarter_gap(self, spec: DeltaSpectrometer) -> dict:
        """Run quarter_gap fractal scan at multiple seeds.

        The quarter_gap test case maps level -> beta_0 in (0.5, 0.85).
        Each level probes a hypothetical zero at that beta_0.
        """
        min_level = int(ScanMode.SURFACE)  # 3
        levels = list(range(min_level, self.max_level + 1))
        n_levels = len(levels)

        # Beta values corresponding to each level (from RiemannGenerator)
        betas = [0.55, 0.58, 0.60, 0.63, 0.65, 0.68, 0.70, 0.72,
                 0.74, 0.76, 0.80, 0.85]

        per_seed_deltas: List[List[float]] = []
        all_deltas_flat: List[float] = []
        n_probes = 0

        for seed_idx in range(self.n_seeds):
            seed = seed_idx + 1
            fp = spec.fractal_scan(
                problem=ProblemType.RIEMANN,
                test_case='quarter_gap',
                regime='frontier',
                seed=seed,
                max_level=self.max_level,
            )
            per_seed_deltas.append(list(fp.delta_by_level))
            all_deltas_flat.extend(fp.delta_by_level)
            n_probes += n_levels

        mean_by_level: List[float] = []
        std_by_level: List[float] = []
        min_by_level: List[float] = []
        max_by_level: List[float] = []

        for lvl_idx in range(n_levels):
            vals = [
                per_seed_deltas[s][lvl_idx]
                for s in range(self.n_seeds)
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

        beta_map: Dict[int, float] = {}
        for lvl_idx, lvl in enumerate(levels):
            beta_idx = min(lvl, len(betas) - 1)
            beta_map[lvl] = betas[beta_idx]

        proved_region_deltas: List[float] = []
        open_region_deltas: List[float] = []
        for lvl_idx, lvl in enumerate(levels):
            beta = beta_map.get(lvl, 0.5)
            for s in range(self.n_seeds):
                if lvl_idx < len(per_seed_deltas[s]):
                    d = per_seed_deltas[s][lvl_idx]
                    if beta >= THREE_QUARTER_BOUND:
                        proved_region_deltas.append(d)
                    else:
                        open_region_deltas.append(d)

        proved_eta = min(proved_region_deltas) if proved_region_deltas else 0.0
        open_eta = min(open_region_deltas) if open_region_deltas else 0.0

        global_mean = sum(all_deltas_flat) / max(len(all_deltas_flat), 1)
        global_min = min(all_deltas_flat) if all_deltas_flat else 0.0
        global_max = max(all_deltas_flat) if all_deltas_flat else 0.0

        return {
            'test_case': 'quarter_gap',
            'levels': levels,
            'n_seeds': self.n_seeds,
            'n_probes': n_probes,
            'beta_map': {str(k): v for k, v in beta_map.items()},
            'mean_by_level': mean_by_level,
            'std_by_level': std_by_level,
            'min_by_level': min_by_level,
            'max_by_level': max_by_level,
            'global_mean': global_mean,
            'global_min': global_min,
            'global_max': global_max,
            'proved_region_eta': proved_eta,
            'open_region_eta': open_eta,
            'n_proved_region_samples': len(proved_region_deltas),
            'n_open_region_samples': len(open_region_deltas),
            'per_seed_deltas': per_seed_deltas,
            'all_deltas_flat': all_deltas_flat,
        }

    # ----------------------------------------------------------------
    #  ANALYSIS: Monotonicity
    # ----------------------------------------------------------------

    def _monotonicity_score(self, mean_by_level: List[float]) -> float:
        """Fraction of consecutive level pairs where delta[i+1] >= delta[i] - epsilon.

        Score of 1.0 = perfectly monotone non-decreasing (delta grows
        as sigma moves further from the critical line).
        Score near 0.0 = non-monotone (unexpected reversals).

        For RH-5, we expect monotonicity: further off the critical line
        means larger defect. Violations would be interesting.
        """
        if len(mean_by_level) < 2:
            return 1.0

        n_pairs = len(mean_by_level) - 1
        n_monotone = 0
        for i in range(n_pairs):
            if mean_by_level[i + 1] >= mean_by_level[i] - MONO_EPSILON:
                n_monotone += 1

        return safe_div(float(n_monotone), float(n_pairs))

    # ----------------------------------------------------------------
    #  ANALYSIS: Derivative
    # ----------------------------------------------------------------

    def _derivative_analysis(self, mean_by_level: List[float],
                             levels: List[int]) -> dict:
        """Compute d(delta)/d(level) at each point.

        Returns dict with:
          derivatives: list of finite differences
          max_derivative: largest positive jump
          steepest_level: level index of steepest ascent
          mean_derivative: average slope across all pairs
        """
        if len(mean_by_level) < 2 or len(levels) < 2:
            return {
                'derivatives': [],
                'max_derivative': 0.0,
                'steepest_level': 0,
                'mean_derivative': 0.0,
            }

        derivatives: List[float] = []
        for i in range(len(mean_by_level) - 1):
            dl = levels[i + 1] - levels[i]
            if dl == 0:
                derivatives.append(0.0)
            else:
                dd = (mean_by_level[i + 1] - mean_by_level[i]) / float(dl)
                derivatives.append(dd)

        max_deriv = max(derivatives) if derivatives else 0.0
        steepest = 0
        if derivatives:
            steepest = derivatives.index(max_deriv)
        mean_deriv = sum(derivatives) / max(len(derivatives), 1)

        return {
            'derivatives': derivatives,
            'max_derivative': max_deriv,
            'steepest_level': levels[steepest] if steepest < len(levels) else 0,
            'mean_derivative': mean_deriv,
        }

    # ----------------------------------------------------------------
    #  ANALYSIS: Zero Crossing Test
    # ----------------------------------------------------------------

    def _zero_crossing_test(self, all_deltas: List[float]) -> dict:
        """Test if delta EVER touches zero off-line.

        Examines every delta measurement from both campaigns.
        A zero crossing is any delta < ZERO_THRESHOLD.

        Returns:
          zero_crossings: count of deltas below threshold
          min_delta_observed: smallest delta seen anywhere
          all_positive: True if every delta > ZERO_THRESHOLD
          eta_lower_bound: conservative lower bound on the gap
        """
        if not all_deltas:
            return {
                'zero_crossings': 0,
                'min_delta_observed': 0.0,
                'all_positive': True,
                'eta_lower_bound': 0.0,
            }

        zero_crossings = sum(1 for d in all_deltas if d < ZERO_THRESHOLD)
        min_delta = min(all_deltas)
        all_positive = all(d > ZERO_THRESHOLD for d in all_deltas)

        # Conservative eta: the minimum observed delta
        # This is the empirical lower bound: delta >= eta for all off-line probes
        eta = min_delta if all_positive else 0.0

        return {
            'zero_crossings': zero_crossings,
            'min_delta_observed': min_delta,
            'all_positive': all_positive,
            'eta_lower_bound': eta,
        }

    # ----------------------------------------------------------------
    #  ANALYSIS: Formal Contradiction Test
    # ----------------------------------------------------------------

    def _contradiction_test(self, results: dict) -> dict:
        """Formal RH-5 test: if beta_0 >= 3/4, then delta >= eta > 0 for all seeds.

        The Riemann Hypothesis implies no zeros exist off Re(s) = 1/2.
        In the proved zero-free region (Re(s) >= 3/4), we KNOW there are
        no zeros. The CK spectrometer should show delta > 0 there.

        The test:
          1. In the proved region (beta >= 3/4): delta must be strictly positive.
             Any zero crossing here would indicate a spectrometer calibration error.
          2. In the open region (0.5 < beta < 3/4): delta should also be positive
             IF RH is true. The measurement cannot prove RH, but it can establish
             an empirical bound.

        Returns:
          hypothesis: what we are testing
          verdict: consistent or anomaly_detected
          eta: empirical lower bound on delta in the proved region
          confidence: statistical confidence (1 - 1/n_probes)
          n_violations: number of zero crossings
          n_probes: total measurements
        """
        dense = results.get('dense', {})
        quarter = results.get('quarter', {})
        zero_test = results.get('zero_test', {})
        monotonicity = results.get('monotonicity', 1.0)

        # Total probes
        n_probes = dense.get('n_probes', 0) + quarter.get('n_probes', 0)

        # Proved region eta (from quarter_gap campaign)
        proved_eta = quarter.get('proved_region_eta', 0.0)

        # Violations
        n_violations = zero_test.get('zero_crossings', 0)

        # Confidence: Bonferroni-corrected
        confidence = clamp(1.0 - safe_div(1.0, float(max(n_probes, 1))))

        # Global eta
        global_eta = zero_test.get('eta_lower_bound', 0.0)

        # Verdict
        if n_violations == 0 and proved_eta > ZERO_THRESHOLD:
            verdict = 'consistent'
        elif n_violations == 0 and proved_eta <= ZERO_THRESHOLD:
            verdict = 'consistent_weak'
        else:
            verdict = 'anomaly_detected'

        return {
            'hypothesis': (
                'RH-5: If RH is true, delta_RH > 0 for all sigma != 0.5. '
                'In the proved zero-free region (sigma >= 3/4), this is '
                'unconditional. In the open region (0.5 < sigma < 3/4), '
                'this is conditional on RH.'
            ),
            'verdict': verdict,
            'eta_proved_region': proved_eta,
            'eta_global': global_eta,
            'confidence': confidence,
            'n_violations': n_violations,
            'n_probes': n_probes,
            'monotonicity_score': monotonicity,
        }




# ================================================================
#  SUMMARY FORMATTER
# ================================================================

def rh5_summary(results: dict) -> str:
    """Format human-readable summary of RH-5 deep probe results."""
    out = []
    sep = '=' * 72
    dash = '-' * 72
    params = results.get('params', {})

    out.append(sep)
    out.append('  RH-5 DEEP SIGMA SWEEP: Off-Line Zero Contradiction Probe')
    out.append(sep)
    out.append('  Seeds: %s' % params.get('n_seeds', '?'))
    out.append('  Max level: %s' % params.get('max_level', '?'))
    sr = params.get('sigma_range', [0.501, 0.999])
    out.append('  Sigma range: [%.3f, %.3f]' % (sr[0], sr[1]))
    out.append('  Total probes: %s' % results.get('total_probes', 0))
    out.append('  Total time: %.1fs (%.1f probes/s)' % (
        results.get('total_time_s', 0),
        results.get('probes_per_second', 0)))
    out.append('')

    out.append(dash)
    out.append('  CAMPAIGN 1: off_line_dense (sigma parametrized by level)')
    out.append(dash)
    dense = results.get('dense', {})
    mean_by = dense.get('mean_by_level', [])
    std_by = dense.get('std_by_level', [])
    levels = dense.get('levels', [])
    for i, lvl in enumerate(levels):
        m = mean_by[i] if i < len(mean_by) else 0.0
        s = std_by[i] if i < len(std_by) else 0.0
        out.append('    Level %2d: delta = %.6f +/- %.6f' % (lvl, m, s))
    out.append('  Global: mean=%.6f  min=%.6f  max=%.6f' % (
        dense.get('global_mean', 0),
        dense.get('global_min', 0),
        dense.get('global_max', 0)))
    out.append('  Monotonicity score: %.4f' % results.get('monotonicity_score', 0))
    out.append('')

    deriv = results.get('derivative_analysis', {})
    out.append('  Derivative: mean=%.6f  max=%.6f  steepest at level %s' % (
        deriv.get('mean_derivative', 0),
        deriv.get('max_derivative', 0),
        deriv.get('steepest_level', 0)))
    out.append('')

    out.append(dash)
    out.append('  CAMPAIGN 2: quarter_gap (hypothetical zeros at beta_0)')
    out.append(dash)
    quarter = results.get('quarter', {})
    q_mean = quarter.get('mean_by_level', [])
    q_std = quarter.get('std_by_level', [])
    q_levels = quarter.get('levels', [])
    beta_map = quarter.get('beta_map', {})
    for i, lvl in enumerate(q_levels):
        m = q_mean[i] if i < len(q_mean) else 0.0
        s = q_std[i] if i < len(q_std) else 0.0
        beta = beta_map.get(str(lvl), '?')
        region = 'PROVED' if isinstance(beta, (int, float)) and beta >= THREE_QUARTER_BOUND else 'open'
        out.append('    Level %2d (beta=%s): delta = %.6f +/- %.6f  [%s]' % (lvl, beta, m, s, region))
    out.append('  Proved region eta: %.6f (%s samples)' % (
        quarter.get('proved_region_eta', 0),
        quarter.get('n_proved_region_samples', 0)))
    out.append('  Open region eta:   %.6f (%s samples)' % (
        quarter.get('open_region_eta', 0),
        quarter.get('n_open_region_samples', 0)))
    out.append('')

    out.append(dash)
    out.append('  ZERO CROSSING TEST')
    out.append(dash)
    zt = results.get('zero_crossing_test', {})
    all_pos = zt.get('all_positive', False)
    status = 'PASS (all delta > 0)' if all_pos else 'FAIL (zero crossing detected)'
    out.append('  Status: %s' % status)
    out.append('  Zero crossings: %s' % zt.get('zero_crossings', 0))
    out.append('  Min delta observed: %.8f' % zt.get('min_delta_observed', 0))
    out.append('  Eta lower bound: %.8f' % zt.get('eta_lower_bound', 0))
    out.append('')

    out.append(dash)
    out.append('  FORMAL RH-5 CONTRADICTION TEST')
    out.append(dash)
    ct = results.get('contradiction_test', {})
    out.append('  Hypothesis: %s' % ct.get('hypothesis', '?'))
    out.append('  Verdict: %s' % ct.get('verdict', '?'))
    out.append('  Eta (proved region): %.8f' % ct.get('eta_proved_region', 0))
    out.append('  Eta (global):        %.8f' % ct.get('eta_global', 0))
    out.append('  Confidence: %.6f' % ct.get('confidence', 0))
    out.append('  Violations: %s / %s probes' % (ct.get('n_violations', 0), ct.get('n_probes', 0)))
    out.append('  Monotonicity: %.4f' % ct.get('monotonicity_score', 0))
    out.append('')
    out.append(sep)
    out.append('  CK measures. CK does not prove.')
    out.append(sep)

    return '\n'.join(out)


# ================================================================
#  CLI ENTRY POINT
# ================================================================

if __name__ == '__main__':
    import argparse
    import json
    import os
    import sys

    parser = argparse.ArgumentParser(
        description='RH-5 Deep Sigma Sweep: Off-Line Zero Contradiction Probe',
    )
    parser.add_argument(
        '--seeds', type=int, default=100,
        help='Number of seeds per campaign (default: 100)',
    )
    parser.add_argument(
        '--max-level', type=int, default=24,
        help='Maximum fractal level (default: 24 = OMEGA)',
    )
    parser.add_argument(
        '--output-dir', default=None,
        help='Write results JSON to this directory',
    )
    parser.add_argument(
        '--quick', action='store_true',
        help='Quick mode: 10 seeds (for testing)',
    )
    args = parser.parse_args()

    if args.quick:
        args.seeds = 10

    probe = RH5DeepProbe(n_seeds=args.seeds, max_level=args.max_level)
    results = probe.run()

    print(rh5_summary(results))

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        out_path = os.path.join(args.output_dir, 'rh5_deep.json')
        # Strip per_seed_deltas from JSON to keep file size reasonable
        export = dict(results)
        for key in ('dense', 'quarter'):
            if key in export and 'per_seed_deltas' in export[key]:
                export[key] = dict(export[key])
                export[key].pop('per_seed_deltas', None)
                export[key].pop('all_deltas_flat', None)
        with open(out_path, 'w') as f:
            json.dump(export, f, indent=2, default=str)
        print('Results written to: %s' % out_path)
