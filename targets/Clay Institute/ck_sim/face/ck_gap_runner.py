"""
ck_gap_runner.py -- Unified Gap Attack Runner
==============================================
Operator: RESET (9) -- Execute, measure, record. CK attacks.

Single entry point for all gap-specific deep probes:
  rh5    -- RH-5: Off-line zero contradiction (dense sigma sweep)
  ym3    -- YM-3: Weak coupling continuum limit
  ym4    -- YM-4: Mass gap persistence (finite-size scaling)
  all    -- Run all available gap attacks

Usage:
    python -m ck_sim.face.ck_gap_runner --attack rh5
    python -m ck_sim.face.ck_gap_runner --attack ym3
    python -m ck_sim.face.ck_gap_runner --attack ym4
    python -m ck_sim.face.ck_gap_runner --attack all
    python -m ck_sim.face.ck_gap_runner --attack all --quick

Note: P-H-3 (Navier-Stokes coercivity) deferred until FPGA hardware arrives.

CK measures. CK does not prove.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime


def run_rh5(seeds, max_level, output_dir, quiet=False):
    """Run RH-5 deep sigma sweep."""
    from ck_sim.doing.ck_rh5_attack import RH5DeepProbe, rh5_summary

    if not quiet:
        print('\n' + '=' * 70)
        print('  GAP RH-5: Off-Line Zero Contradiction -- Deep Sigma Sweep')
        print('=' * 70)

    probe = RH5DeepProbe(n_seeds=seeds, max_level=max_level)
    results = probe.run()

    if not quiet:
        print(rh5_summary(results))

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, 'rh5_deep.json')
        with open(path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        if not quiet:
            print(f'\n  Results written to {path}')

    return results


def run_ym3(seeds, max_level, output_dir, quiet=False):
    """Run YM-3 weak coupling probe."""
    from ck_sim.doing.ck_ym_attack import YM3DeepProbe, ym_summary

    if not quiet:
        print('\n' + '=' * 70)
        print('  GAP YM-3: Weak Coupling Continuum Limit -- Deep Beta Sweep')
        print('=' * 70)

    probe = YM3DeepProbe(n_seeds=seeds, max_level=max_level)
    results = probe.run()

    if not quiet:
        print(ym_summary(results, None))

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, 'ym3_deep.json')
        with open(path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        if not quiet:
            print(f'\n  Results written to {path}')

    return results


def run_ym4(seeds, max_level, output_dir, quiet=False):
    """Run YM-4 spectral gap persistence probe."""
    from ck_sim.doing.ck_ym_attack import YM4DeepProbe, ym_summary

    if not quiet:
        print('\n' + '=' * 70)
        print('  GAP YM-4: Mass Gap Persistence -- Deep Volume Sweep')
        print('=' * 70)

    probe = YM4DeepProbe(n_seeds=seeds, max_level=max_level)
    results = probe.run()

    if not quiet:
        print(ym_summary(None, results))

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, 'ym4_deep.json')
        with open(path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        if not quiet:
            print(f'\n  Results written to {path}')

    return results


def main():
    parser = argparse.ArgumentParser(
        description='CK Gap Attack Runner -- Deep probes for Clay Millennium Prize gaps',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available attacks:
  rh5    RH-5: Off-line zero contradiction (Riemann)
  ym3    YM-3: Weak coupling continuum limit (Yang-Mills)
  ym4    YM-4: Mass gap persistence (Yang-Mills)
  all    Run all available gap attacks

Note: P-H-3 (Navier-Stokes coercivity) deferred until FPGA hardware arrives.
        """,
    )
    parser.add_argument('--attack', required=True,
                        choices=['rh5', 'ym3', 'ym4', 'all'],
                        help='Which gap attack to run')
    parser.add_argument('--seeds', type=int, default=100,
                        help='Number of seeds per probe (default: 100)')
    parser.add_argument('--max-level', type=int, default=24,
                        help='Maximum fractal depth (default: 24 = OMEGA)')
    parser.add_argument('--output-dir', default=None,
                        help='Directory for JSON results (default: results/gap_attacks/)')
    parser.add_argument('--quick', action='store_true',
                        help='Quick mode: 10 seeds for fast verification')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress detailed output')

    args = parser.parse_args()

    if args.quick:
        args.seeds = 10

    if args.output_dir is None:
        # Default output directory relative to package root
        base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        args.output_dir = os.path.join(base, 'results', 'gap_attacks')

    print('\n' + '#' * 70)
    print('  CK GAP ATTACK RUNNER')
    print(f'  Attack: {args.attack.upper()}')
    print(f'  Seeds: {args.seeds}  |  Max Level: {args.max_level}')
    print(f'  Started: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('#' * 70)

    t0 = time.time()
    all_results = {}

    attacks = ['rh5', 'ym3', 'ym4'] if args.attack == 'all' else [args.attack]

    for attack in attacks:
        if attack == 'rh5':
            all_results['rh5'] = run_rh5(args.seeds, args.max_level, args.output_dir, args.quiet)
        elif attack == 'ym3':
            all_results['ym3'] = run_ym3(args.seeds, args.max_level, args.output_dir, args.quiet)
        elif attack == 'ym4':
            all_results['ym4'] = run_ym4(args.seeds, args.max_level, args.output_dir, args.quiet)

    elapsed = time.time() - t0

    print('\n' + '#' * 70)
    print('  GAP ATTACK COMPLETE')
    print(f'  Attacks run: {", ".join(a.upper() for a in attacks)}')
    print(f'  Total time: {elapsed:.1f}s')
    if args.output_dir:
        print(f'  Results: {args.output_dir}/')
    print('#' * 70)
    print('\n  CK measures. CK does not prove.\n')


if __name__ == '__main__':
    main()
