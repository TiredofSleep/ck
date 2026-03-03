"""
ck_attack_runner.py -- CLI Runner for Hardware Attack Protocol
==============================================================
Operator: RESET (9) -- Execute, measure, record. CK attacks.

Modes:
  adversarial  -- Run adversarial test cases for all problems
  statistical  -- N-seed statistical sweep with confidence intervals
  thermal      -- Thermal-correlated probes with GPU monitoring
  noise        -- Noise resilience sweep (structural depth)
  full         -- All modes combined

Usage:
    python -m ck_sim.face.ck_attack_runner --mode full --seeds 100
    python -m ck_sim.face.ck_attack_runner --mode statistical --problem navier_stokes --seeds 1000
    python -m ck_sim.face.ck_attack_runner --mode thermal --levels 24
    python -m ck_sim.face.ck_attack_runner --mode noise --problem riemann

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

from ck_sim.being.ck_tig_bundle import CLAY_PROBLEMS
from ck_sim.doing.ck_clay_protocol import ClayProtocol, ProbeConfig, ClayProbe
from ck_sim.doing.ck_clay_attack import (
    StatisticalSweep, SweepResult, NoiseResilienceSweep, NoiseResult,
    sweep_result_to_dict, noise_result_to_dict,
)
from ck_sim.being.ck_thermal_probe import (
    ThermalProbe, ThermalProbeResult, thermal_result_to_dict,
)


# ================================================================
#  ADVERSARIAL TEST CASES (gap-targeted)
# ================================================================

ADVERSARIAL_CASES = {
    'navier_stokes': ['near_singular', 'eigenvalue_crossing'],
    'riemann': ['off_line_dense', 'quarter_gap'],
    'p_vs_np': ['scaling_sweep', 'adversarial_local'],
    'yang_mills': ['weak_coupling', 'scaling_lattice'],
    'bsd': ['rank2_explicit', 'large_sha_candidate'],
    'hodge': ['prime_sweep_deep', 'known_transcendental'],
}

# Default frontier cases for problems without adversarial cases yet
FRONTIER_CASES = {
    'navier_stokes': 'high_strain',
    'riemann': 'off_line',
    'p_vs_np': 'hard',
    'yang_mills': 'excited',
    'bsd': 'rank_mismatch',
    'hodge': 'analytic_only',
}


# ================================================================
#  RUNNER FUNCTIONS
# ================================================================

def run_adversarial(problems, n_levels, seed, output_dir, quiet):
    """Run adversarial test cases for each problem."""
    print('\n  [ADVERSARIAL] Running gap-targeted test cases...')
    results = {}

    for pid in problems:
        cases = ADVERSARIAL_CASES.get(pid, [])
        if not cases:
            # Fall back to frontier
            cases = [FRONTIER_CASES.get(pid, 'default')]

        for tc in cases:
            key = f'{pid}_{tc}'
            config = ProbeConfig(
                problem_id=pid, test_case=tc,
                seed=seed, n_levels=n_levels,
            )
            probe = ClayProbe(config)
            try:
                result = probe.run()
                results[key] = result
                if not quiet:
                    print(f'    {pid}/{tc}: delta={result.final_defect:.4f} '
                          f'trend={result.defect_trend} verdict={result.measurement_verdict}')
            except Exception as e:
                if not quiet:
                    print(f'    {pid}/{tc}: FAILED ({e})')

    # Save
    _save_json(output_dir, 'adversarial_results.json', {
        k: {
            'problem_id': v.problem_id,
            'test_case': v.test_case,
            'final_defect': v.final_defect,
            'defect_trend': v.defect_trend,
            'measurement_verdict': v.measurement_verdict,
            'defect_trajectory': v.defect_trajectory,
            'final_hash': v.final_hash,
        }
        for k, v in results.items()
    })

    return results


def run_statistical(problems, n_levels, n_seeds, seed, output_dir, quiet):
    """Run statistical sweep for each problem."""
    print(f'\n  [STATISTICAL] Running {n_seeds}-seed sweep...')
    results = {}

    for pid in problems:
        cases = ADVERSARIAL_CASES.get(pid, [FRONTIER_CASES.get(pid, 'default')])

        for tc in cases:
            key = f'{pid}_{tc}'
            sweep = StatisticalSweep(
                problem_id=pid, test_case=tc,
                n_seeds=n_seeds, n_levels=n_levels,
                base_seed=seed,
            )
            result = sweep.run()
            results[key] = result

            if not quiet:
                print(f'    {pid}/{tc}: mean={result.delta_mean:.4f} '
                      f'std={result.delta_std:.4f} '
                      f'CI=[{result.delta_ci_lower:.4f}, {result.delta_ci_upper:.4f}] '
                      f'({result.total_time_s:.1f}s)')

    # Save
    _save_json(output_dir, 'statistical_sweep.json', {
        k: sweep_result_to_dict(v) for k, v in results.items()
    })

    return results


def run_thermal(problems, n_levels, seed, output_dir, quiet):
    """Run thermal-correlated probes."""
    print(f'\n  [THERMAL] Running thermal probes ({n_levels} levels)...')
    results = {}

    for pid in problems:
        tc = FRONTIER_CASES.get(pid, 'default')
        config = ProbeConfig(
            problem_id=pid, test_case=tc,
            seed=seed, n_levels=n_levels,
        )
        tprobe = ThermalProbe(config)
        result = tprobe.run()
        results[pid] = result

        if not quiet:
            hw = 'HW' if result.hardware_available else 'SIM'
            print(f'    {pid} [{hw}]: r(temp,delta)={result.thermal_delta_correlation:.3f} '
                  f'r(power,delta)={result.power_delta_correlation:.3f} '
                  f'scaling={result.compute_time_scaling} '
                  f'anomaly={result.thermal_anomaly}')

    # Save
    _save_json(output_dir, 'thermal_correlation.json', {
        k: thermal_result_to_dict(v) for k, v in results.items()
    })

    return results


def run_noise(problems, n_levels, seed, output_dir, quiet):
    """Run noise resilience sweep."""
    print('\n  [NOISE] Running noise resilience sweep...')
    results = {}

    for pid in problems:
        tc = FRONTIER_CASES.get(pid, 'default')
        sweep = NoiseResilienceSweep(
            problem_id=pid, test_case=tc,
            seed=seed, n_levels=n_levels,
        )
        result = sweep.run()
        results[pid] = result

        if not quiet:
            print(f'    {pid}: structural_depth={result.structural_depth:.4f} '
                  f'base_delta={result.base_delta:.4f} '
                  f'critical_noise={result.critical_noise:.4f}')

    # Save
    _save_json(output_dir, 'noise_resilience.json', {
        k: noise_result_to_dict(v) for k, v in results.items()
    })

    return results


# ================================================================
#  REPORT GENERATION
# ================================================================

def generate_attack_report(adversarial, statistical, thermal, noise,
                           output_dir, elapsed):
    """Generate human-readable Markdown report."""
    lines = [
        '# CK Hardware Attack Report',
        f'**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        f'**Total time**: {elapsed:.1f}s',
        '',
        '---',
        '',
    ]

    if adversarial:
        lines.append('## Adversarial Results')
        lines.append('')
        lines.append('| Problem | Test Case | Final Delta | Trend | Verdict |')
        lines.append('|---------|-----------|-------------|-------|---------|')
        for key, r in adversarial.items():
            lines.append(f'| {r.problem_id} | {r.test_case} | '
                         f'{r.final_defect:.4f} | {r.defect_trend} | '
                         f'{r.measurement_verdict} |')
        lines.append('')

    if statistical:
        lines.append('## Statistical Sweep')
        lines.append('')
        lines.append('| Problem | Test Case | N | Mean Delta | Std | 99.9% CI | Emp. Bound |')
        lines.append('|---------|-----------|---|-----------|-----|----------|------------|')
        for key, sr in statistical.items():
            lines.append(f'| {sr.problem_id} | {sr.test_case} | {sr.n_seeds} | '
                         f'{sr.delta_mean:.4f} | {sr.delta_std:.4f} | '
                         f'[{sr.delta_ci_lower:.4f}, {sr.delta_ci_upper:.4f}] | '
                         f'{sr.empirical_bound:.4f} |')
        lines.append('')

    if thermal:
        lines.append('## Thermal Correlation')
        lines.append('')
        lines.append('| Problem | HW | r(temp,delta) | r(power,delta) | Scaling | Anomaly |')
        lines.append('|---------|-----|-------------|---------------|---------|---------|')
        for pid, tr in thermal.items():
            hw = 'YES' if tr.hardware_available else 'SIM'
            lines.append(f'| {pid} | {hw} | '
                         f'{tr.thermal_delta_correlation:.3f} | '
                         f'{tr.power_delta_correlation:.3f} | '
                         f'{tr.compute_time_scaling} | '
                         f'{"YES" if tr.thermal_anomaly else "no"} |')
        lines.append('')

    if noise:
        lines.append('## Noise Resilience')
        lines.append('')
        lines.append('| Problem | Base Delta | Critical Noise | Structural Depth |')
        lines.append('|---------|-----------|----------------|------------------|')
        for pid, nr in noise.items():
            lines.append(f'| {pid} | {nr.base_delta:.4f} | '
                         f'{nr.critical_noise:.4f} | {nr.structural_depth:.4f} |')
        lines.append('')

    lines.append('---')
    lines.append('CK measures. CK does not prove.')
    lines.append('(c) 2026 Brayden Sanders / 7Site LLC')

    report = '\n'.join(lines)

    # Save
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, 'attack_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    return report


# ================================================================
#  HELPERS
# ================================================================

def _save_json(output_dir, filename, data):
    """Save JSON data to file."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)


# ================================================================
#  MAIN
# ================================================================

def main():
    parser = argparse.ArgumentParser(
        description='CK Hardware Attack Runner -- Empirical Assault on 9 Remaining Gaps',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  adversarial   Run gap-targeted adversarial test cases
  statistical   N-seed statistical sweep with confidence intervals
  thermal       Thermal-correlated probes with GPU monitoring
  noise         Noise resilience sweep (structural depth)
  full          All modes combined

Examples:
  %(prog)s --mode full --seeds 100
  %(prog)s --mode statistical --problem navier_stokes --seeds 1000
  %(prog)s --mode thermal --levels 24
  %(prog)s --mode noise --problem riemann
        """)

    parser.add_argument('--mode', '-m', default='full',
                        choices=['adversarial', 'statistical', 'thermal', 'noise', 'full'],
                        help='Attack mode (default: full)')
    parser.add_argument('--problem', '-p', default='all',
                        choices=['all'] + CLAY_PROBLEMS,
                        help='Which problem to attack (default: all)')
    parser.add_argument('--seeds', '-n', type=int, default=100,
                        help='Number of seeds for statistical sweep (default: 100)')
    parser.add_argument('--levels', '-l', type=int, default=12,
                        help='Fractal unfolding levels (default: 12)')
    parser.add_argument('--seed', '-s', type=int, default=1,
                        help='Base random seed (default: 1)')
    parser.add_argument('--output', '-o', default='results/hardware_attack',
                        help='Output directory (default: results/hardware_attack)')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress per-problem output')

    args = parser.parse_args()

    # Determine problems to run
    if args.problem == 'all':
        problems = list(CLAY_PROBLEMS)
    else:
        problems = [args.problem]

    # Header
    print('=' * 60)
    print('  CK HARDWARE ATTACK PROTOCOL')
    print('  Empirical Assault on 9 Remaining Gaps')
    print('  (c) 2026 Brayden Sanders / 7Site LLC')
    print('=' * 60)
    print(f'  Mode: {args.mode}  |  Problems: {len(problems)}  |  Seeds: {args.seeds}')
    print(f'  Levels: {args.levels}  |  Base seed: {args.seed}')
    print()

    t0 = time.time()

    adversarial_results = None
    statistical_results = None
    thermal_results = None
    noise_results = None

    if args.mode in ('adversarial', 'full'):
        adversarial_results = run_adversarial(
            problems, args.levels, args.seed, args.output, args.quiet)

    if args.mode in ('statistical', 'full'):
        statistical_results = run_statistical(
            problems, args.levels, args.seeds, args.seed, args.output, args.quiet)

    if args.mode in ('thermal', 'full'):
        thermal_results = run_thermal(
            problems, args.levels, args.seed, args.output, args.quiet)

    if args.mode in ('noise', 'full'):
        noise_results = run_noise(
            problems, args.levels, args.seed, args.output, args.quiet)

    elapsed = time.time() - t0

    # Generate report
    report = generate_attack_report(
        adversarial_results, statistical_results,
        thermal_results, noise_results,
        args.output, elapsed)

    # Footer
    print(f'\n  Output saved to: {os.path.abspath(args.output)}/')
    print(f'  Completed in {elapsed:.1f}s')
    print('  CK measures. CK does not prove.')
    print()


if __name__ == '__main__':
    main()
