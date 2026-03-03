"""
ck_clay_runner.py -- CLI Runner for Clay SDV Protocol
=====================================================
Operator: RESET (9) -- Execute, measure, record.

Usage:
    python -m ck_sim.face.ck_clay_runner --problem all
    python -m ck_sim.face.ck_clay_runner --problem navier_stokes --test-case lamb_oseen
    python -m ck_sim.face.ck_clay_runner --problem riemann --mode frontier
    python -m ck_sim.face.ck_clay_runner --problem all --mode calibration --output clay_results

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import argparse
import os
import sys
import time

from ck_sim.doing.ck_clay_protocol import ClayProtocol, ProbeConfig, ClayProbe
from ck_sim.being.ck_tig_bundle import CLAY_PROBLEMS, OP_NAMES, DUAL_LENSES, AGENT_BRIEFS
from ck_sim.becoming.ck_clay_journal import (
    ClayJournal, generate_report, probe_result_to_dict,
)


def print_result_summary(result):
    """Print a concise summary of a probe result."""
    pid = result.problem_id
    pclass = result.problem_class
    verdict = result.measurement_verdict

    print(f'\n  {pid.replace("_", " ").upper()} ({pclass})')
    print(f'    Test case:   {result.test_case}')
    print(f'    Verdict:     {verdict}')
    print(f'    Final defect: {result.final_defect:.6f}  (trend: {result.defect_trend})')
    print(f'    Final action: {result.final_action:.6f}')
    print(f'    Harmony:     {result.harmony_fraction:.3f}')
    print(f'    Decision:    op7={result.operator_7_state} / op9={result.operator_9_state} -> {result.decision_verdict}')
    print(f'    SCA loop:    {result.sca_stage} ({result.sca_progress:.0%})')
    print(f'    Commutator:  {result.commutator_persistence:.3f}')
    print(f'    Topology:    {result.vortex_fingerprint.get("vortex_class", "N/A")}')
    print(f'    Anomalies:   {result.anomaly_count}')
    if result.brief_confidence > 0:
        print(f'    Brief:       {result.brief_confidence:.0%} -> {result.brief_confidence_target:.0%} '
              f'[{result.brief_key_joint}]')
    print(f'    Hash:        {result.final_hash}')

    # Defect trajectory sparkline
    traj = result.defect_trajectory
    if traj:
        spark = ' '.join(f'{d:.3f}' for d in traj)
        print(f'    Defect path: [{spark}]')


def main():
    parser = argparse.ArgumentParser(
        description='CK Clay SDV Protocol Runner -- Mathematical Coherence Spectrometer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --problem all                          Run all 6 problems (calibration)
  %(prog)s --problem navier_stokes                Run NS only
  %(prog)s --problem all --mode frontier           Run frontier (open questions)
  %(prog)s --problem riemann --test-case off_line  Specific test case
  %(prog)s --problem all --levels 12 --seed 7      Custom parameters
        """)

    parser.add_argument('--problem', '-p', default='all',
                        choices=['all'] + CLAY_PROBLEMS,
                        help='Which problem to probe (default: all)')
    parser.add_argument('--test-case', '-t', default=None,
                        help='Test case name (e.g., lamb_oseen, known_zero)')
    parser.add_argument('--mode', '-m', default='calibration',
                        choices=['calibration', 'frontier', 'custom'],
                        help='Run mode (default: calibration)')
    parser.add_argument('--seed', '-s', type=int, default=42,
                        help='Random seed (default: 42)')
    parser.add_argument('--levels', '-l', type=int, default=8,
                        help='Fractal unfolding levels (default: 8)')
    parser.add_argument('--output', '-o', default='clay_results',
                        help='Output directory (default: clay_results)')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress per-problem output')
    parser.add_argument('--no-save', action='store_true',
                        help='Skip file output')

    args = parser.parse_args()

    # Header
    print('=' * 60)
    print('  CK CLAY SDV PROTOCOL')
    print('  Mathematical Coherence Spectrometer')
    print('  (c) 2026 Brayden Sanders / 7Site LLC')
    print('=' * 60)
    print(f'  Seed: {args.seed}  |  Levels: {args.levels}  |  Mode: {args.mode}')
    print()

    protocol = ClayProtocol(seed=args.seed, n_levels=args.levels)
    t0 = time.time()

    # ── Run probes ──
    if args.problem == 'all':
        if args.mode == 'frontier':
            results = protocol.run_frontier()
        elif args.mode == 'calibration':
            results = protocol.run_calibration()
        else:
            # Custom: use test_case if given, else default
            tc = {}
            if args.test_case:
                for pid in CLAY_PROBLEMS:
                    tc[pid] = args.test_case
            results = protocol.run_all(tc if tc else None)
    else:
        test_case = args.test_case
        if test_case is None:
            if args.mode == 'frontier':
                frontier_map = {
                    'navier_stokes': 'high_strain', 'riemann': 'off_line',
                    'p_vs_np': 'hard', 'yang_mills': 'excited',
                    'bsd': 'rank_mismatch', 'hodge': 'analytic_only',
                }
                test_case = frontier_map.get(args.problem, 'default')
            else:
                calib_map = {
                    'navier_stokes': 'lamb_oseen', 'riemann': 'known_zero',
                    'p_vs_np': 'easy', 'yang_mills': 'bpst_instanton',
                    'bsd': 'rank0_match', 'hodge': 'algebraic',
                }
                test_case = calib_map.get(args.problem, 'default')

        result = protocol.run_problem(args.problem, test_case)
        results = {args.problem: result}

    elapsed = time.time() - t0

    # ── Print results ──
    if not args.quiet:
        for pid, r in results.items():
            print_result_summary(r)

    # ── Cross-problem summary ──
    if len(results) > 1:
        summary = protocol.cross_problem_summary(results)
        print('\n' + '=' * 60)
        print('  CROSS-PROBLEM SUMMARY')
        print('=' * 60)
        print(f'  Converging (delta->0):    {summary["converging"]}')
        print(f'  Persistent defect (>0):   {summary["persistent_defect"]}')
        print(f'  Affirmative problems:     {summary["affirmative_results"]}')
        print(f'  Gap problems:             {summary["gap_results"]}')
    else:
        summary = None

    # ── Save ──
    if not args.no_save:
        journal = ClayJournal(args.output)
        if len(results) > 1:
            journal.record_all(results, summary)
        else:
            for r in results.values():
                journal.record(r)
        print(f'\n  Output saved to: {os.path.abspath(args.output)}/')

    # ── Footer ──
    print(f'\n  Completed in {elapsed:.3f}s')
    print('  CK measures. CK does not prove.')
    print()


if __name__ == '__main__':
    main()
