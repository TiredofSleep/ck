# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_spectrometer_runner.py -- CLI for TIG-Delta Universal Coherence Spectrometer
================================================================================
Operator: RESET (9) -- Execute, measure, record.

Usage:
    python -m ck_sim.face.ck_spectrometer_runner --mode scan --problem all
    python -m ck_sim.face.ck_spectrometer_runner --mode matrix
    python -m ck_sim.face.ck_spectrometer_runner --mode chaos --problem riemann
    python -m ck_sim.face.ck_spectrometer_runner --mode full

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import argparse
import os
import sys
import time

from ck_sim.doing.ck_spectrometer import (
    DeltaSpectrometer, SpectrometerInput, SpectrometerResult,
    FlowResult, FractalFingerprint, SandersAttackResult,
    RobustnessResult, PerturbationTrial, PerturbationType,
    ProblemType, ScanMode, Verdict, SkeletonClass, GateVerdict,
    MacroClass, classify_macro,
    CALIBRATION_CASES, FRONTIER_CASES, ROBUSTNESS_THRESHOLD,
)
from ck_sim.being.ck_tig_bundle import CLAY_PROBLEMS, ALL_PROBLEMS

try:
    from ck_sim.becoming.ck_spectrometer_journal import SpectrometerJournal
except ImportError:
    SpectrometerJournal = None


# ================================================================
#  SCAN MODE LOOKUP
# ================================================================

SCAN_MODE_MAP = {
    'surface': ScanMode.SURFACE,
    'deep': ScanMode.DEEP,
    'omega': ScanMode.OMEGA,
}

# Default noise sigmas for chaos_scan
DEFAULT_CHAOS_SIGMAS = [0.0, 0.01, 0.05, 0.1, 0.2, 0.5]


# ================================================================
#  RESULT PRINTING
# ================================================================

def print_result_summary(result: SpectrometerResult, quiet: bool = False):
    """Print a concise summary of a SpectrometerResult."""
    if quiet:
        return

    problem_label = result.problem.replace('_', ' ').upper()
    pclass = result.problem_class

    print(f'\n  {problem_label} ({pclass}) [{result.scan_mode}, seed={result.seed}]')
    print(f'    Delta:   {result.delta_value:.6f}  (trend: {result.defect_trend})')
    print(f'    Verdict: {result.verdict.upper()} \u2014 {result.reason}')
    print(f'    Hash:    {result.final_hash}')

    # Sub-measurements
    print(f'    Harmony: {result.harmony_fraction:.3f}  |  '
          f'Commutator: {result.commutator_persistence:.3f}  |  '
          f'SCA: {result.sca_progress:.0%}')
    print(f'    Vortex:  {result.vortex_class}  |  '
          f'Spine: {result.spine_fraction:.3f}')

    if result.anomaly_count > 0:
        print(f'    Anomalies: {result.anomaly_count}')
    if result.halted:
        print(f'    ** HALTED (safety rails triggered) **')

    # Defect trajectory sparkline
    traj = result.defect_trajectory
    if traj and len(traj) <= 24:
        spark = ' '.join(f'{d:.3f}' for d in traj)
        print(f'    Defect path: [{spark}]')
    elif traj:
        # Summarize long trajectories
        spark_head = ' '.join(f'{d:.3f}' for d in traj[:4])
        spark_tail = ' '.join(f'{d:.3f}' for d in traj[-4:])
        print(f'    Defect path: [{spark_head} ... {spark_tail}] ({len(traj)} levels)')


def print_chaos_summary(problem_id: str, chaos_results: list):
    """Print chaos scan summary for one problem."""
    problem_label = problem_id.replace('_', ' ').upper()
    print(f'\n  CHAOS SCAN: {problem_label}')
    print(f'  {"Sigma":>8}  {"Delta":>10}  {"Verdict":>10}  {"Trend":>10}')
    print(f'  {"-" * 44}')
    for r in chaos_results:
        sigma = r.input_key.split('sigma=')[-1] if 'sigma=' in r.input_key else '?'
        print(f'  {sigma:>8}  {r.delta_value:>10.6f}  {r.verdict:>10}  {r.defect_trend:>10}')


def print_consistency_summary(sweep: dict):
    """Print consistency sweep summary."""
    problem_label = sweep['problem'].replace('_', ' ').upper()
    print(f'\n  CONSISTENCY SWEEP: {problem_label}')
    print(f'    Seeds:          {sweep["n_seeds"]} (base={sweep["base_seed"]})')
    print(f'    Scan mode:      {sweep["scan_mode"]}')
    print(f'    Delta mean:     {sweep["delta_mean"]:.6f} +/- {sweep["delta_std"]:.6f}')
    print(f'    Delta range:    [{sweep["delta_min"]:.6f}, {sweep["delta_max"]:.6f}]')
    print(f'    99.9% CI:       [{sweep["delta_ci_lower"]:.6f}, {sweep["delta_ci_upper"]:.6f}]')
    print(f'    Falsifications: {sweep["falsifications"]} '
          f'(unstable={sweep["unstable_count"]}, singular={sweep["singular_count"]})')
    print(f'    Hashes unique:  {sweep["all_hashes_unique"]}')


def print_flow_summary(problem_id: str, flow: 'FlowResult'):
    """Print Sanders Flow scan summary for one problem."""
    problem_label = problem_id.replace('_', ' ').upper()
    lyap = 'YES' if flow.lyapunov_confirmed else 'NO'
    mono = 'YES' if flow.is_monotone else f'NO ({len(flow.violations)} violations)'
    strategy = getattr(flow, 'flow_strategy', 'noise')

    print(f'\n  SANDERS FLOW: {problem_label} ({flow.problem_class}) [{strategy}]')
    if strategy == 'scale':
        print(f'    Steps: {len(flow.sigma_steps)}  |  '
              f'Levels: {int(flow.sigma_steps[0])} -> {int(flow.sigma_steps[-1])}')
    else:
        print(f'    Steps: {len(flow.sigma_steps)}  |  '
              f'Sigma: {flow.sigma_steps[0]:.3f} -> {flow.sigma_steps[-1]:.3f}')
    print(f'    Delta: {flow.delta_initial:.6f} -> {flow.delta_final:.6f}  '
          f'(drop: {flow.delta_drop:.6f})')
    print(f'    Monotone:      {mono}  (score: {flow.monotonicity_score:.1%})')
    print(f'    Flow class:    {flow.flow_class}')
    print(f'    Lyapunov:      {lyap}')
    print(f'    Asymptotic:    {flow.asymptotic_value:.6f}')

    # Compact trajectory
    traj = flow.delta_trajectory
    if len(traj) <= 10:
        spark = ' '.join(f'{d:.4f}' for d in traj)
    else:
        spark = ' '.join(f'{d:.4f}' for d in traj[:3])
        spark += ' ... '
        spark += ' '.join(f'{d:.4f}' for d in traj[-3:])
    print(f'    Flow path: [{spark}]')


def print_matrix_summary(matrix_results: list):
    """Print stability matrix summary."""
    total = len(matrix_results)
    by_verdict = {}
    for r in matrix_results:
        by_verdict[r.verdict] = by_verdict.get(r.verdict, 0) + 1

    by_problem = {}
    for r in matrix_results:
        pid = r.problem
        if pid not in by_problem:
            by_problem[pid] = {'total': 0, 'stable': 0, 'deltas': []}
        by_problem[pid]['total'] += 1
        if r.verdict == Verdict.STABLE.value:
            by_problem[pid]['stable'] += 1
        by_problem[pid]['deltas'].append(r.delta_value)

    print(f'\n  STABILITY MATRIX: {total} runs')
    print(f'  {"Verdict":>12}: ', end='')
    for v, c in sorted(by_verdict.items()):
        print(f'{v}={c}  ', end='')
    print()

    print(f'\n  {"Problem":<16} {"Runs":>5} {"Stable":>7} {"Mean Delta":>12} {"Min":>10} {"Max":>10}')
    print(f'  {"-" * 62}')
    for pid in sorted(by_problem.keys()):
        info = by_problem.get(pid, {'total': 0, 'stable': 0, 'deltas': [0.0]})
        ds = info['deltas']
        mean_d = sum(ds) / len(ds) if ds else 0.0
        print(f'  {pid:<16} {info["total"]:>5} {info["stable"]:>7} '
              f'{mean_d:>12.6f} {min(ds):>10.6f} {max(ds):>10.6f}')


def print_fingerprint(fp: FractalFingerprint, quiet: bool = False):
    """Print a single FractalFingerprint summary."""
    if quiet:
        return

    problem_label = fp.problem.replace('_', ' ').upper()
    print(f'\n  {problem_label} ({fp.regime}) [{fp.skeleton_class.upper()}]')
    print(f'    Test case:  {fp.test_case}  |  Seed: {fp.seed}')
    print(f'    Levels:     {fp.levels[0]} -> {fp.levels[-1]} ({len(fp.levels)} points)')
    print(f'    Delta:      mean={fp.delta_mean:.6f}  std={fp.delta_std:.6f}  '
          f'CV={fp.delta_cv:.3f}')
    print(f'    Range:      [{fp.delta_min:.6f}, {fp.delta_max:.6f}]  '
          f'span={fp.delta_range:.6f}')

    # Spectral
    if fp.dominant_period is not None:
        print(f'    Spectral:   entropy={fp.spectral_entropy:.3f}  '
              f'period={fp.dominant_period:.1f} levels')
    else:
        print(f'    Spectral:   entropy={fp.spectral_entropy:.3f}  '
              f'period=none (flat)')

    # Cross features
    print(f'    Deviation:  level {fp.first_deviation_level}  |  '
          f'Phase transitions: {fp.n_phase_transitions}')

    # Mini sparkline of delta_by_level
    if fp.delta_by_level:
        vals = fp.delta_by_level
        if fp.delta_range > 0:
            bars = ' _.:-=+#@'
            lo, hi = fp.delta_min, fp.delta_max
            span = hi - lo
            line = ''
            for d in vals:
                idx = int((d - lo) / span * 8) if span > 0 else 0
                idx = max(0, min(8, idx))
                line += bars[idx]
            print(f'    Skeleton:   |{line}|')
        else:
            print(f'    Skeleton:   |{"=" * len(vals)}| (flat)')


def print_atlas_summary(atlas: dict, quiet: bool = False):
    """Print cross-problem atlas summary table."""
    if quiet:
        return

    print(f'\n  {"=" * 78}')
    print(f'  FRACTAL COHERENCE ATLAS: {len(atlas)} fingerprints')
    print(f'  {"=" * 78}')

    # Summary table
    print(f'\n  {"Problem":<16} {"Regime":<12} {"Skeleton":<14} {"Mean":>8} '
          f'{"Std":>8} {"Range":>8} {"Entropy":>8} {"Period":>8}')
    print(f'  {"-" * 16} {"-" * 12} {"-" * 14} {"-" * 8} '
          f'{"-" * 8} {"-" * 8} {"-" * 8} {"-" * 8}')

    for key in sorted(atlas.keys()):
        fp = atlas[key]
        per_str = f'{fp.dominant_period:.1f}' if fp.dominant_period else 'flat'
        print(f'  {fp.problem:<16} {fp.regime:<12} {fp.skeleton_class:<14} '
              f'{fp.delta_mean:>8.4f} {fp.delta_std:>8.4f} {fp.delta_range:>8.4f} '
              f'{fp.spectral_entropy:>8.3f} {per_str:>8}')

    # Cross-problem classification summary
    classes = {}
    for key, fp in atlas.items():
        skel = fp.skeleton_class
        classes.setdefault(skel, []).append(f'{fp.problem}({fp.regime[0]})')

    print(f'\n  SKELETON CLASSIFICATION:')
    for skel in ['frozen', 'stable', 'bounded', 'oscillating', 'wild']:
        members = classes.get(skel, [])
        if members:
            print(f'    {skel.upper():>14}: {", ".join(members)}')

    # Universal pattern categories (from Fractal Attack document)
    print(f'\n  UNIVERSAL PATTERN CATEGORIES:')
    frozen = [k for k, fp in atlas.items() if fp.skeleton_class == 'frozen']
    wild_osc = [k for k, fp in atlas.items()
                if fp.skeleton_class in ('wild', 'oscillating')]
    bounded_stable = [k for k, fp in atlas.items()
                      if fp.skeleton_class in ('bounded', 'stable')]

    if frozen:
        print(f'    Self-Similar (fractal fixed points):  '
              f'{len(frozen)} fingerprints')
    if wild_osc:
        print(f'    Turbulent (scale-emergent structure): '
              f'{len(wild_osc)} fingerprints')
    if bounded_stable:
        print(f'    Confined (bounded/stable structure):  '
              f'{len(bounded_stable)} fingerprints')


def print_attack_result(ar: SandersAttackResult, quiet: bool = False):
    """Print a single Sanders Attack result."""
    if quiet:
        return

    problem_label = ar.problem.replace('_', ' ').upper()
    gate_icon = '*' if ar.gate_verdict == 'pass' else '-'
    print(f'\n  {gate_icon} {problem_label} ({ar.regime})')
    print(f'    Skeleton: {ar.fingerprint.skeleton_class.upper()} '
          f'(range={ar.fingerprint.delta_range:.4f}, '
          f'entropy={ar.fingerprint.spectral_entropy:.3f})')
    print(f'    Gate:     {ar.gate_verdict.upper()} -- {ar.gate_reason}')

    if ar.flow_result is not None:
        fr = ar.flow_result
        lyap = 'YES' if fr.lyapunov_confirmed else 'NO'
        mono = f'{fr.monotonicity_score:.0%}'
        print(f'    Flow:     delta {fr.delta_initial:.4f} -> {fr.delta_final:.4f} '
              f'| mono={mono} | Lyapunov={lyap} | class={fr.flow_class}')

    if ar.candidate_singularity:
        print(f'    >>> CANDIDATE SINGULARITY <<<')
    print(f'    Summary:  {ar.attack_summary}')


def print_attack_summary(results: dict, quiet: bool = False):
    """Print cross-problem Sanders Attack summary."""
    if quiet:
        return

    total = len(results)
    passed = sum(1 for ar in results.values()
                 if ar.gate_verdict == 'pass')
    candidates = sum(1 for ar in results.values()
                     if ar.candidate_singularity)

    print(f'\n  {"=" * 70}')
    print(f'  SANDERS ATTACK SUMMARY')
    print(f'  {"=" * 70}')
    print(f'  Configurations tested: {total}')
    print(f'  Gate: {passed} PASS, {total - passed} SKIP')
    print(f'  Candidate singularities: {candidates}')

    # Table
    print(f'\n  {"Problem":<16} {"Regime":<12} {"Skeleton":<12} {"Gate":<6} '
          f'{"Flow?":<6} {"Candidate":<10}')
    print(f'  {"-" * 16} {"-" * 12} {"-" * 12} {"-" * 6} '
          f'{"-" * 6} {"-" * 10}')

    for key in sorted(results.keys()):
        ar = results[key]
        skel = ar.fingerprint.skeleton_class[:10]
        gate = ar.gate_verdict.upper()
        investigated = 'YES' if ar.was_investigated else 'no'
        cand = '>>> YES' if ar.candidate_singularity else 'no'
        print(f'  {ar.problem:<16} {ar.regime:<12} {skel:<12} {gate:<6} '
              f'{investigated:<6} {cand:<10}')

    if candidates > 0:
        print(f'\n  CANDIDATES:')
        for key, ar in results.items():
            if ar.candidate_singularity:
                print(f'    {ar.problem} ({ar.regime}): {ar.attack_summary}')
    else:
        print(f'\n  No candidate singularities found. '
              f'All configurations within expected fractal regimes.')


def print_robustness_result(rr: RobustnessResult, quiet: bool = False):
    """Print a single RobustnessResult summary."""
    if quiet:
        return

    problem_label = rr.problem.replace('_', ' ').upper()
    robust_icon = 'ROBUST' if rr.robust else 'FRAGILE'
    print(f'\n  {problem_label} ({rr.regime}) [{rr.baseline_skeleton.upper()}] '
          f'-- {robust_icon}')
    macro_label = classify_macro(rr.baseline_skeleton)
    print(f'    Survival: {rr.n_preserved}/{rr.n_trials} '
          f'({rr.survival_rate:.0%})  threshold={ROBUSTNESS_THRESHOLD:.0%}')
    print(f'    Macro:    {rr.macro_n_preserved}/{rr.n_trials} '
          f'({rr.macro_survival_rate:.0%})  [{macro_label.upper()}]')
    print(f'    Baseline: delta={rr.baseline_delta_mean:.6f}  '
          f'range={rr.baseline_delta_range:.6f}  '
          f'entropy={rr.baseline_entropy:.3f}')

    # Per-type breakdown
    by_type = {}
    for t in rr.trials:
        by_type.setdefault(t.perturbation_type, []).append(t)

    for ptype in ['tig_permutation', 'generator_jitter',
                  'channel_ablation', 'noise_distribution', 'multi_seed']:
        trials = by_type.get(ptype, [])
        if not trials:
            continue
        preserved = sum(1 for t in trials if t.skeleton_preserved)
        ptype_label = ptype.replace('_', ' ').title()
        print(f'    {ptype_label:>22}: {preserved}/{len(trials)} preserved')

    # Show any breaks
    breaks = [t for t in rr.trials if not t.skeleton_preserved]
    if breaks:
        print(f'    Breaks ({len(breaks)}):')
        for t in breaks[:5]:  # Show max 5
            print(f'      {t.perturbation_label}: '
                  f'{t.baseline_skeleton} -> {t.perturbed_skeleton} '
                  f'(delta_shift={t.delta_mean_shift:+.4f})')


def print_robustness_summary(results: dict, quiet: bool = False):
    """Print cross-problem robustness summary."""
    if quiet:
        return

    total = len(results)
    robust = sum(1 for rr in results.values() if rr.robust)

    print(f'\n  {"=" * 70}')
    print(f'  ROBUSTNESS / ABLATION SUMMARY')
    print(f'  {"=" * 70}')
    print(f'  Configurations tested: {total}')
    print(f'  Robust: {robust}/{total}  |  '
          f'Fragile: {total - robust}/{total}')

    # Table
    print(f'\n  {"Problem":<16} {"Regime":<12} {"Skeleton":<12} '
          f'{"Fine":>9} {"Macro":>9} {"Robust":>7}')
    print(f'  {"-" * 16} {"-" * 12} {"-" * 12} {"-" * 9} {"-" * 9} {"-" * 7}')

    for key in sorted(results.keys()):
        rr = results[key]
        skel = rr.baseline_skeleton[:10]
        fine_surv = f'{rr.survival_rate:.0%}'
        macro_surv = f'{rr.macro_survival_rate:.0%}'
        rob = 'YES' if rr.robust else 'NO'
        print(f'  {rr.problem:<16} {rr.regime:<12} {skel:<12} '
              f'{fine_surv:>9} {macro_surv:>9} {rob:>7}')

    # Features that survived all perturbations (based on macro robustness)
    all_robust = [k for k, rr in results.items() if rr.macro_robust]
    if all_robust:
        print(f'\n  ROBUST PATTERNS (macro survived >= {ROBUSTNESS_THRESHOLD:.0%} '
              f'of perturbations):')
        for key in all_robust:
            rr = results[key]
            print(f'    {rr.problem} ({rr.regime}): {rr.baseline_skeleton} '
                  f'(fine={rr.survival_rate:.0%}, macro={rr.macro_survival_rate:.0%})')

    fragile = [k for k, rr in results.items() if not rr.macro_robust]
    if fragile:
        print(f'\n  FRAGILE PATTERNS:')
        for key in fragile:
            rr = results[key]
            print(f'    {rr.problem} ({rr.regime}): {rr.baseline_skeleton} '
                  f'(fine={rr.survival_rate:.0%}, macro={rr.macro_survival_rate:.0%})')

    print(f'\n  Features that survive ALL perturbations are the "deeper code."')


def run_robustness(spec, args):
    """Mode: robustness -- Full robustness/ablation sweep."""
    n_deep = getattr(args, 'seeds', 20)
    print(f'\n  Robustness/Ablation Sweep')
    print(f'  5 perturbation types x 12 configurations')
    print(f'  Deep seeds per config: {n_deep}')

    if args.problem == 'all':
        results = spec.robustness_full(
            seed=args.seed, max_level=6, n_deep_seeds=n_deep)
    else:
        pt = ProblemType(args.problem)
        results = {}
        for regime, case_map in [('calibration', CALIBRATION_CASES),
                                  ('frontier', FRONTIER_CASES)]:
            tc = args.test_case or case_map.get(args.problem, 'default')
            key = f'{args.problem}_{regime}'
            results[key] = spec.robustness_sweep(
                problem=pt, test_case=tc, regime=regime,
                seed=args.seed, max_level=6, n_deep_seeds=n_deep,
            )

    for key in sorted(results.keys()):
        print_robustness_result(results[key], quiet=args.quiet)

    print_robustness_summary(results, quiet=args.quiet)
    return results


def run_attack(spec, args):
    """Mode: attack -- Sanders Attack (fractal gate + conditional flow)."""
    strategy = getattr(args, 'flow_strategy', 'scale')
    print(f'\n  Sanders Attack: fractal gate + conditional {strategy} flow')
    print(f'  12 configurations enter. Only anomalous skeletons get flow analysis.')

    if args.problem == 'all':
        results = spec.sanders_attack_full(
            seed=args.seed, flow_strategy=strategy, n_flow_steps=10,
        )
    else:
        pt = ProblemType(args.problem)
        results = {}
        for regime, case_map in [('calibration', CALIBRATION_CASES),
                                  ('frontier', FRONTIER_CASES)]:
            tc = args.test_case or case_map.get(args.problem, 'default')
            key = f'{args.problem}_{regime}'
            results[key] = spec.sanders_attack(
                problem=pt, test_case=tc, regime=regime,
                seed=args.seed, flow_strategy=strategy,
                n_flow_steps=10,
            )

    for key in sorted(results.keys()):
        print_attack_result(results[key], quiet=args.quiet)

    print_attack_summary(results, quiet=args.quiet)
    return results


def print_equation_result(eq, quiet=False):
    """Print a single GoverningEquation result."""
    if quiet:
        return

    problem_label = eq.problem.replace('_', ' ').upper()
    bf = eq.best_fit
    print(f'\n  {problem_label} ({eq.regime}) [{eq.best_model.upper()}]')
    print(f'    Equation: {eq.latex}')
    print(f'    R^2={bf.r_squared:.4f}  BIC={bf.bic:.1f}  '
          f'confidence={eq.confidence:.2f}')
    print(f'    Asymptotic: {eq.asymptotic_class.upper()} '
          f'(delta -> {eq.asymptotic_value:.6f})')


def print_equation_summary(equations, quiet=False):
    """Print cross-problem governing equation summary."""
    if quiet:
        return

    n_aff = sum(1 for eq in equations.values()
                if eq.asymptotic_class == 'affirmative')
    n_gap = sum(1 for eq in equations.values()
                if eq.asymptotic_class == 'gap')
    n_ind = sum(1 for eq in equations.values()
                if eq.asymptotic_class == 'indeterminate')

    print(f'\n  {"=" * 70}')
    print(f'  GOVERNING EQUATIONS SUMMARY')
    print(f'  {"=" * 70}')
    print(f'  Equations extracted: {len(equations)}')
    print(f'  Affirmative (delta -> 0):    {n_aff}')
    print(f'  Gap (delta -> eta > 0):      {n_gap}')
    print(f'  Indeterminate:               {n_ind}')

    # Table
    print(f'\n  {"Problem":<20} {"Regime":<12} {"Model":<12} '
          f'{"R^2":>6} {"BIC":>8} {"Class":<14} {"delta(inf)":>10}')
    print(f'  {"-" * 20} {"-" * 12} {"-" * 12} '
          f'{"-" * 6} {"-" * 8} {"-" * 14} {"-" * 10}')

    for key in sorted(equations.keys()):
        eq = equations[key]
        bf = eq.best_fit
        print(f'  {eq.problem:<20} {eq.regime:<12} {eq.best_model:<12} '
              f'{bf.r_squared:>6.3f} {bf.bic:>8.1f} '
              f'{eq.asymptotic_class:<14} {eq.asymptotic_value:>10.6f}')

    # Two-class partition
    aff = [k for k, eq in equations.items()
           if eq.asymptotic_class == 'affirmative']
    gap = [k for k, eq in equations.items()
           if eq.asymptotic_class == 'gap']

    if aff:
        print(f'\n  AFFIRMATIVE (delta -> 0):')
        for k in sorted(aff):
            eq = equations[k]
            print(f'    {eq.problem} ({eq.regime}): {eq.best_model}')
    if gap:
        print(f'\n  GAP (delta -> eta > 0):')
        for k in sorted(gap):
            eq = equations[k]
            print(f'    {eq.problem} ({eq.regime}): {eq.best_model}')


def run_equations(spec, args):
    """Mode: equations -- Extract governing equations for all problems."""
    problem_set = 'all' if args.problem == 'all' else None

    if args.problem == 'all':
        print(f'\n  Governing Equations: extracting for all {len(ALL_PROBLEMS)} problems')
        atlas_result = spec.equation_atlas(
            seed=args.seed, problem_set='all')
        equations = atlas_result.equations
    else:
        print(f'\n  Governing Equations: extracting for {args.problem}')
        equations = {}
        for regime, case_map in [('calibration', CALIBRATION_CASES),
                                  ('frontier', FRONTIER_CASES)]:
            tc = args.test_case or case_map.get(args.problem, 'default')
            pt = ProblemType(args.problem)
            eq = spec.equation_extract(
                problem=pt, test_case=tc, regime=regime,
                seed=args.seed,
            )
            key = f'{args.problem}_{regime}'
            equations[key] = eq

    for key in sorted(equations.keys()):
        print_equation_result(equations[key], quiet=args.quiet)

    print_equation_summary(equations, quiet=args.quiet)
    return equations


# ================================================================
#  MODE DISPATCH
# ================================================================

def run_scan(spec, args):
    """Mode: scan -- Single scan of one or all problems."""
    scan_mode = SCAN_MODE_MAP[args.scan_mode]
    results = {}

    if args.problem == 'all':
        results = spec.scan_all(scan_mode=scan_mode, seed=args.seed)
    else:
        pt = ProblemType(args.problem)
        tc = args.test_case or CALIBRATION_CASES.get(args.problem, 'default')
        inp = SpectrometerInput(
            problem=pt, test_case=tc,
            scan_mode=scan_mode, seed=args.seed,
            label='cli_scan',
        )
        results[args.problem] = spec.scan(inp)

    for pid, r in results.items():
        print_result_summary(r, quiet=args.quiet)

    return results


def run_sweep(spec, args):
    """Mode: sweep -- scan_all at all 3 modes (SURFACE, DEEP, OMEGA)."""
    all_results = {}

    for mode in ScanMode:
        print(f'\n  --- Sweep: {mode.name} (levels={int(mode)}) ---')
        batch = spec.scan_all(scan_mode=mode, seed=args.seed)
        for pid, r in batch.items():
            key = f'{pid}_{mode.name}'
            all_results[key] = r
            print_result_summary(r, quiet=args.quiet)

    return all_results


def run_chaos(spec, args):
    """Mode: chaos -- chaos_scan for each problem (or specified problem)."""
    scan_mode = SCAN_MODE_MAP[args.scan_mode]
    problems = ALL_PROBLEMS if args.problem == 'all' else [args.problem]
    all_results = {}

    for pid in problems:
        pt = ProblemType(pid)
        tc = args.test_case or CALIBRATION_CASES.get(pid, 'default')
        chaos_results = spec.chaos_scan(
            problem=pt, test_case=tc,
            scan_mode=scan_mode, seed=args.seed,
            noise_sigmas=DEFAULT_CHAOS_SIGMAS,
        )
        all_results[pid] = chaos_results
        print_chaos_summary(pid, chaos_results)

    return all_results


def run_consistency(spec, args):
    """Mode: consistency -- consistency_sweep per problem."""
    scan_mode = SCAN_MODE_MAP[args.scan_mode]
    problems = ALL_PROBLEMS if args.problem == 'all' else [args.problem]
    all_sweeps = {}

    for pid in problems:
        pt = ProblemType(pid)
        tc = args.test_case or CALIBRATION_CASES.get(pid, 'default')
        sweep = spec.consistency_sweep(
            problem=pt, test_case=tc,
            scan_mode=scan_mode, n_seeds=args.seeds,
            base_seed=args.seed,
        )
        all_sweeps[pid] = sweep
        print_consistency_summary(sweep)

    return all_sweeps


def run_flow(spec, args):
    """Mode: flow -- Sanders Flow (Lyapunov verification) per problem."""
    scan_mode = SCAN_MODE_MAP[args.scan_mode]
    problems = ALL_PROBLEMS if args.problem == 'all' else [args.problem]
    strategy = getattr(args, 'flow_strategy', 'noise')
    all_flows = {}

    for pid in problems:
        pt = ProblemType(pid)
        tc = args.test_case or FRONTIER_CASES.get(pid, 'default')
        flow = spec.flow_scan(
            problem=pt, test_case=tc,
            scan_mode=scan_mode, seed=args.seed,
            flow_strategy=strategy,
        )
        all_flows[pid] = flow
        print_flow_summary(pid, flow)

    # Print aggregate
    total = len(all_flows)
    confirmed = sum(1 for f in all_flows.values() if f.lyapunov_confirmed)
    monotone = sum(1 for f in all_flows.values() if f.is_monotone)
    print(f'\n  SANDERS FLOW SUMMARY [{strategy}]: {confirmed}/{total} Lyapunov confirmed, '
          f'{monotone}/{total} monotone')

    return all_flows


def run_matrix(spec, args):
    """Mode: matrix -- Full 108-run stability matrix."""
    print('\n  Running stability matrix (108 runs)...')
    matrix_results = spec.stability_matrix()
    print_matrix_summary(matrix_results)
    return matrix_results


def run_atlas(spec, args):
    """Mode: atlas -- Fractal Coherence Atlas (12 fingerprints)."""
    print('\n  Building Fractal Coherence Atlas (6 problems x 2 regimes)...')

    if args.problem == 'all':
        atlas = spec.fractal_atlas(seed=args.seed)
    else:
        # Single problem, both regimes
        pt = ProblemType(args.problem)
        atlas = {}
        for regime, case_map in [('calibration', CALIBRATION_CASES),
                                  ('frontier', FRONTIER_CASES)]:
            tc = args.test_case or case_map.get(args.problem, 'default')
            fp = spec.fractal_scan(
                problem=pt, test_case=tc,
                regime=regime, seed=args.seed,
            )
            atlas[f'{args.problem}_{regime}'] = fp

    # Print individual fingerprints
    for key in sorted(atlas.keys()):
        print_fingerprint(atlas[key], quiet=args.quiet)

    # Print atlas summary
    print_atlas_summary(atlas, quiet=args.quiet)

    return atlas


# ================================================================
#  META-LENS DISPLAY + RUN FUNCTIONS
# ================================================================

def print_topology_result(result, quiet=False):
    """Display TopologyLens I/0/flow decomposition."""
    pid = result.get('problem_id', '?')
    core = result.get('core', {})
    boundary = result.get('boundary', {})
    flow = result.get('flow', {})
    defect = result.get('defect', 0.0)
    print(f'    {pid:30s}  I={core.get("label","?"):20s}  '
          f'0={boundary.get("label","?"):20s}  '
          f'delta={defect:.4f}  align={flow.get("alignment",0):.3f}')


def print_russell_result(result, quiet=False):
    """Display Russell 6D toroidal analysis."""
    pid = result.get('problem_id', '?')
    dr = result.get('delta_russell', 0.0)
    ds = result.get('delta_standard', 0.0)
    cls = result.get('classification', '?')
    coords = result.get('coords', {})
    print(f'    {pid:30s}  delta_R={dr:.4f}  delta_std={ds:.4f}  '
          f'class={cls:10s}  div={coords.get("divergence",0):.3f}  '
          f'curl={coords.get("curl",0):.3f}  void={coords.get("void_proximity",0):.3f}')


def print_ssa_result(result, quiet=False):
    """Display SSA trilemma result."""
    pid = result.get('problem_id', '?')
    breaking = result.get('breaking', '?')
    interp = result.get('interpretation', '')
    c1 = 'OK' if result.get('c1_holds') else 'BREAK'
    c2 = 'OK' if result.get('c2_holds') else 'BREAK'
    c3 = 'OK' if result.get('c3_holds') else 'BREAK'
    print(f'    {pid:30s}  C1={c1:5s}  C2={c2:5s}  C3={c3:5s}  '
          f'=> {breaking}')
    if not quiet:
        print(f'      {interp}')


def print_rate_result(result, quiet=False):
    """Display RATE R_inf convergence result."""
    pid = result.get('problem_id', '?')
    conv = result.get('converged', False)
    fp = result.get('fixed_point_delta', 0.0)
    rd = result.get('rate_defect', 0.0)
    depth = result.get('convergence_depth', 0)
    emerged = result.get('topology_emerged', False)
    status = 'CONVERGED' if conv else 'DIVERGENT'
    print(f'    {pid:30s}  {status:10s}  fixed_pt={fp:.4f}  '
          f'rate_defect={rd:.6f}  depth={depth}  topology={emerged}')


def print_meta_lens_summary(results, quiet=False):
    """Summary of meta-lens atlas."""
    total = len(results)
    # SSA breaking pattern counts
    break_counts = {}
    for pid, r in results.items():
        b = r.get('ssa', {}).get('breaking', 'NONE')
        break_counts[b] = break_counts.get(b, 0) + 1

    # Russell classification counts
    russell_counts = {}
    for pid, r in results.items():
        c = r.get('russell', {}).get('classification', 'unknown')
        russell_counts[c] = russell_counts.get(c, 0) + 1

    print(f'\n  META-LENS ATLAS SUMMARY ({total} problems)')
    print(f'  SSA Breaking Patterns:')
    for b, cnt in sorted(break_counts.items()):
        print(f'    {b:15s}: {cnt}')
    print(f'  Russell Classifications:')
    for c, cnt in sorted(russell_counts.items()):
        print(f'    {c:15s}: {cnt}')


def run_topology(spec, args):
    """Mode: topology -- TopologyLens I/0/flow decomposition."""
    problems = ALL_PROBLEMS if args.problem == 'all' else [args.problem]
    results = {}
    for pid in problems:
        pt = ProblemType(pid)
        tc = args.test_case or CALIBRATION_CASES.get(pid, 'default')
        result = spec.topology_scan(pt, tc, args.seed)
        results[pid] = result
        print_topology_result(result, quiet=args.quiet)
    return results


def run_russell(spec, args):
    """Mode: russell -- Russell 6D toroidal analysis."""
    problems = ALL_PROBLEMS if args.problem == 'all' else [args.problem]
    results = {}
    for pid in problems:
        pt = ProblemType(pid)
        tc = args.test_case or CALIBRATION_CASES.get(pid, 'default')
        result = spec.russell_scan(pt, tc, args.seed)
        results[pid] = result
        print_russell_result(result, quiet=args.quiet)
    return results


def run_ssa(spec, args):
    """Mode: ssa -- SSA trilemma analysis."""
    problems = ALL_PROBLEMS if args.problem == 'all' else [args.problem]
    seeds = list(range(args.seed, args.seed + min(args.seeds, 10)))
    results = {}
    for pid in problems:
        pt = ProblemType(pid)
        tc = args.test_case or CALIBRATION_CASES.get(pid, 'default')
        result = spec.ssa_analyze(pt, seeds, tc)
        results[pid] = result
        print_ssa_result(result, quiet=args.quiet)
    return results


def run_rate(spec, args):
    """Mode: rate -- RATE R_inf convergence analysis."""
    problems = ALL_PROBLEMS if args.problem == 'all' else [args.problem]
    results = {}
    for pid in problems:
        pt = ProblemType(pid)
        tc = args.test_case or CALIBRATION_CASES.get(pid, 'default')
        result = spec.rate_scan(pt, args.seed, tc)
        results[pid] = result
        print_rate_result(result, quiet=args.quiet)
    return results


def run_meta_lens(spec, args):
    """Mode: meta_lens -- Full meta-lens atlas."""
    problems = ALL_PROBLEMS if args.problem == 'all' else [args.problem]
    seeds = list(range(args.seed, args.seed + min(args.seeds, 5)))
    results = spec.meta_lens_atlas(problems, seeds)
    for pid in sorted(results.keys()):
        r = results[pid]
        topo = r.get('topology', {})
        russell = r.get('russell', {})
        ssa = r.get('ssa', {})
        if not args.quiet:
            print_topology_result(topo, quiet=True)
            print_russell_result(russell, quiet=True)
            print_ssa_result(ssa, quiet=True)
    print_meta_lens_summary(results, quiet=args.quiet)
    return results


def print_foo_result(result, quiet=False):
    """Display FOO trace result."""
    if quiet:
        return
    pid = result.get('problem_id', '?')
    kappa = result.get('kappa', 0.0)
    r_inf = result.get('r_inf', 0.0)
    depth = result.get('foo_depth', 0)
    conv = 'YES' if result.get('converged') else 'no'
    print(f'  FOO  {pid:30s}  kappa={kappa:.3f}  R_inf={r_inf:.6f}  '
          f'depth={depth}  converged={conv}')


def print_phi_result(result, quiet=False):
    """Display Phi(kappa) estimate."""
    if quiet:
        return
    pid = result.get('problem_id', '?')
    kappa = result.get('kappa', 0.0)
    phi_m = result.get('phi_measured', 0.0)
    phi_c = result.get('phi_calibrated', 0.0)
    regime = result.get('regime', '?')
    print(f'  PHI  {pid:30s}  kappa={kappa:.3f}  '
          f'Phi_measured={phi_m:.6f}  Phi_calibrated={phi_c:.3f}  '
          f'regime={regime}')


def print_phi_atlas(atlas_result, quiet=False):
    """Display Phi(kappa) curve analysis."""
    if quiet:
        return
    curve = atlas_result.get('curve', {})
    print(f'\n  Phi(kappa) Curve:')
    print(f'    Monotonic: {curve.get("monotonic", "?")}  '
          f'(violations: {curve.get("monotonic_violations", 0)})')
    regimes = curve.get('regimes', {})
    print(f'    Regimes: certifiable={regimes.get("certifiable", 0)}  '
          f'bounded={regimes.get("bounded", 0)}  '
          f'irreducible={regimes.get("irreducible", 0)}')
    print(f'    Structural consistency: '
          f'{curve.get("structural_consistency", 0.0):.3f}')


def print_breath_result(result, quiet=False):
    """Display breath analysis result."""
    if quiet:
        return
    pid = result.get('problem_id', '?')
    b_idx = result.get('b_idx', 0.0)
    regime = result.get('breath_regime', '?')
    fear = 'FEAR' if result.get('fear_collapsed') else 'ok'
    osc = result.get('oscillation_amplitude', 0.0)
    deep = result.get('deep_flow_count', 0)
    shallow = result.get('shallow_flow_count', 0)
    prims = result.get('primitives', {})
    a_e = prims.get('alpha_e', 0.0)
    a_c = prims.get('alpha_c', 0.0)
    beta = prims.get('beta', 0.0)
    sigma = prims.get('sigma', 0.0)
    print(f'  BREATH {pid:25s}  B_idx={b_idx:.4f}  regime={regime:16s}  '
          f'fear={fear:4s}  osc={osc:.3f}')
    print(f'         {"":25s}  a_E={a_e:.3f}  a_C={a_c:.3f}  '
          f'beta={beta:.3f}  sigma={sigma:.3f}  '
          f'deep={deep}  shallow={shallow}')


def print_breath_estimate(result, quiet=False):
    """Display aggregated breath estimate."""
    if quiet:
        return
    pid = result.get('problem_id', '?')
    b_mean = result.get('b_idx_mean', 0.0)
    b_std = result.get('b_idx_std', 0.0)
    regime = result.get('regime', '?')
    fear_rate = result.get('fear_rate', 0.0)
    osc = result.get('oscillation_mean', 0.0)
    a_e = result.get('alpha_e_mean', 0.0)
    a_c = result.get('alpha_c_mean', 0.0)
    beta = result.get('beta_mean', 0.0)
    sigma = result.get('sigma_mean', 0.0)
    print(f'  BREATH {pid:25s}  B_idx={b_mean:.4f} +/- {b_std:.4f}  '
          f'regime={regime:16s}  fear_rate={fear_rate:.2f}')
    print(f'         {"":25s}  a_E={a_e:.3f}  a_C={a_c:.3f}  '
          f'beta={beta:.3f}  sigma={sigma:.3f}  osc={osc:.3f}')


def print_breath_atlas(atlas_result, quiet=False):
    """Display breath atlas summary."""
    if quiet:
        return
    summary = atlas_result.get('summary', {})
    n = summary.get('problems_analyzed', 0)
    mean_b = summary.get('mean_b_idx', 0.0)
    regimes = summary.get('regimes', {})
    healthiest = summary.get('healthiest', '?')
    stressed = summary.get('most_stressed', '?')
    print(f'\n  BREATH ATLAS SUMMARY ({n} problems)')
    print(f'    Mean B_idx: {mean_b:.4f}')
    print(f'    Regimes:')
    for r, cnt in sorted(regimes.items()):
        print(f'      {r:20s}: {cnt}')
    print(f'    Healthiest: {healthiest}')
    print(f'    Most stressed: {stressed}')


def run_breath(spec, args):
    """Mode: breath -- Breath-Defect Flow analysis (single scan per problem)."""
    problems = ALL_PROBLEMS if args.problem == 'all' else [args.problem]
    results = {}
    for pid in problems:
        pt = ProblemType(pid)
        tc = args.test_case or CALIBRATION_CASES.get(pid, 'default')
        result = spec.breath_scan(pt, seed=args.seed, test_case=tc)
        print_breath_result(result, quiet=args.quiet)
        results[pid] = result
    return results


def run_breath_rate(spec, args):
    """Mode: breath_rate -- Breath analysis on RATE traces."""
    problems = ALL_PROBLEMS if args.problem == 'all' else [args.problem]
    results = {}
    for pid in problems:
        pt = ProblemType(pid)
        tc = args.test_case or CALIBRATION_CASES.get(pid, 'default')
        result = spec.breath_rate_scan(pt, seed=args.seed, test_case=tc)
        print_breath_result(result, quiet=args.quiet)
        results[pid] = result
    return results


def run_breath_atlas(spec, args):
    """Mode: breath_atlas -- Full breath atlas across all problems."""
    problems = list(CLAY_PROBLEMS) if args.problem == 'all' else [args.problem]
    seeds = list(range(args.seed, args.seed + min(args.seeds, 5)))
    result = spec.breath_atlas(problems, seeds)
    for pid in sorted(result.get('estimates', {}).keys()):
        print_breath_estimate(result['estimates'][pid], quiet=args.quiet)
    print_breath_atlas(result, quiet=args.quiet)
    return result


def run_foo(spec, args):
    """Mode: foo -- Fractal Optimality Operator iteration."""
    problems = ALL_PROBLEMS if args.problem == 'all' else [args.problem]
    results = {}
    for pid in problems:
        pt = ProblemType(pid)
        tc = args.test_case or CALIBRATION_CASES.get(pid, 'default')
        result = spec.foo_scan(pt, seed=args.seed, test_case=tc)
        print_foo_result(result, quiet=args.quiet)
        results[pid] = result
    return results


def run_phi(spec, args):
    """Mode: phi -- Phi(kappa) complexity horizon estimation."""
    problems = list(CLAY_PROBLEMS) if args.problem == 'all' else [args.problem]
    seeds = list(range(args.seed, args.seed + min(args.seeds, 5)))
    results = {}
    for pid in problems:
        pt = ProblemType(pid)
        tc = args.test_case or CALIBRATION_CASES.get(pid, 'default')
        result = spec.phi_estimate(pt, seeds=seeds, test_case=tc)
        print_phi_result(result, quiet=args.quiet)
        results[pid] = result
    return results


def run_phi_atlas(spec, args):
    """Mode: phi_atlas -- Full Phi(kappa) curve across all Clay problems."""
    problems = list(CLAY_PROBLEMS) if args.problem == 'all' else [args.problem]
    seeds = list(range(args.seed, args.seed + min(args.seeds, 3)))
    result = spec.phi_atlas(problems, seeds)
    for pid in sorted(result.get('estimates', {}).keys()):
        print_phi_result(result['estimates'][pid], quiet=args.quiet)
    print_phi_atlas(result, quiet=args.quiet)
    return result


def run_full(spec, args):
    """Mode: full -- scan + chaos + consistency + matrix in sequence."""
    all_output = {}

    print('\n' + '=' * 60)
    print('  PHASE 1: SCAN (all problems, deep)')
    print('=' * 60)
    all_output['scan'] = run_scan(spec, args)

    print('\n' + '=' * 60)
    print('  PHASE 2: CHAOS (noise resilience)')
    print('=' * 60)
    all_output['chaos'] = run_chaos(spec, args)

    print('\n' + '=' * 60)
    print('  PHASE 3: SANDERS FLOW (Lyapunov verification)')
    print('=' * 60)
    all_output['flow'] = run_flow(spec, args)

    print('\n' + '=' * 60)
    print('  PHASE 4: CONSISTENCY (multi-seed sweep)')
    print('=' * 60)
    all_output['consistency'] = run_consistency(spec, args)

    print('\n' + '=' * 60)
    print('  PHASE 5: STABILITY MATRIX (108 runs)')
    print('=' * 60)
    all_output['matrix'] = run_matrix(spec, args)

    print('\n' + '=' * 60)
    print('  PHASE 6: FRACTAL COHERENCE ATLAS (12 fingerprints)')
    print('=' * 60)
    all_output['atlas'] = run_atlas(spec, args)

    print('\n' + '=' * 60)
    print('  PHASE 7: SANDERS ATTACK (fractal gate + conditional flow)')
    print('=' * 60)
    all_output['attack'] = run_attack(spec, args)

    print('\n' + '=' * 60)
    print('  PHASE 8: ROBUSTNESS / ABLATION (5 perturbation types)')
    print('=' * 60)
    all_output['robustness'] = run_robustness(spec, args)

    print('\n' + '=' * 60)
    print('  PHASE 9: GOVERNING EQUATIONS (parametric model extraction)')
    print('=' * 60)
    all_output['equations'] = run_equations(spec, args)

    print('\n' + '=' * 60)
    print('  PHASE 10: META-LENS (topology + russell + ssa)')
    print('=' * 60)
    all_output['meta_lens'] = run_meta_lens(spec, args)

    print('\n' + '=' * 60)
    print('  PHASE 11: PHI(KAPPA) COMPLEXITY HORIZONS')
    print('=' * 60)
    all_output['phi_atlas'] = run_phi_atlas(spec, args)

    print('\n' + '=' * 60)
    print('  PHASE 12: BREATH-DEFECT FLOW (B_idx + fear-collapse)')
    print('=' * 60)
    all_output['breath_atlas'] = run_breath_atlas(spec, args)

    return all_output


# ================================================================
#  MAIN
# ================================================================

def main():
    parser = argparse.ArgumentParser(
        description='CK TIG-Delta Universal Coherence Spectrometer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  scan          Single scan of one or all problems
  sweep         Scan all problems at SURFACE, DEEP, and OMEGA
  chaos         Noise resilience test (default sigmas: 0, 0.01, 0.05, 0.1, 0.2, 0.5)
  consistency   Multi-seed consistency sweep per problem
  flow          Sanders Flow: verify Lyapunov (--flow-strategy noise|scale)
  atlas         Fractal Coherence Atlas: skeleton fingerprints for all problems
  attack        Sanders Attack: fractal gate + conditional Sanders Flow
  robustness    Robustness/ablation sweep: 5 perturbation types across all configs
  equations     Extract governing equations for all 41 problems
  breath        Breath-Defect Flow analysis (B_idx per problem)
  breath_rate   Breath analysis on RATE R_inf traces
  breath_atlas  Full breath atlas: B_idx + fear-collapse across all problems
  matrix        Full 108-run stability matrix (6 problems x 2 suites x 3 modes x 3 seeds)
  full          Runs all modes in sequence (scan through breath_atlas)

Examples:
  %(prog)s --mode scan --problem all
  %(prog)s --mode scan --problem navier_stokes --scan-mode omega
  %(prog)s --mode chaos --problem riemann --seed 137
  %(prog)s --mode equations --problem all
  %(prog)s --mode consistency --problem all --seeds 200
  %(prog)s --mode matrix
  %(prog)s --mode full --output full_results
        """)

    parser.add_argument('--mode', default='scan',
                        choices=['scan', 'sweep', 'chaos', 'consistency', 'flow',
                                 'atlas', 'attack', 'robustness', 'equations',
                                 'topology', 'russell', 'ssa', 'rate', 'meta_lens',
                                 'foo', 'phi', 'phi_atlas',
                                 'breath', 'breath_rate', 'breath_atlas',
                                 'matrix', 'full'],
                        help='Spectrometer run mode (default: scan)')
    parser.add_argument('--problem', '-p', default='all',
                        choices=['all'] + ALL_PROBLEMS,
                        help='Which problem to probe (default: all)')
    parser.add_argument('--test-case', '-t', default=None,
                        help='Test case name override (e.g., lamb_oseen, known_zero)')
    parser.add_argument('--scan-mode', default='deep',
                        choices=['surface', 'deep', 'omega'],
                        help='Fractal scan depth (default: deep)')
    parser.add_argument('--seeds', type=int, default=100,
                        help='Number of seeds for sweep/consistency (default: 100)')
    parser.add_argument('--seed', '-s', type=int, default=42,
                        help='Base random seed (default: 42)')
    parser.add_argument('--output', '-o', default='spectrometer_results',
                        help='Output directory (default: spectrometer_results)')
    parser.add_argument('--flow-strategy', default='noise',
                        choices=['noise', 'scale'],
                        help='Sanders Flow strategy: noise (sigma sweep) or scale (fractal depth)')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress per-scan output')

    args = parser.parse_args()

    # ── Header ──
    print('=' * 60)
    print('  CK TIG-DELTA UNIVERSAL COHERENCE SPECTROMETER')
    print('  (c) 2026 Brayden Sanders / 7Site LLC')
    print('=' * 60)
    print(f'  Mode: {args.mode}  |  Problem: {args.problem}  |  '
          f'Scan: {args.scan_mode}  |  Seed: {args.seed}')
    print()

    spec = DeltaSpectrometer()
    t0 = time.time()

    # ── Mode dispatch ──
    mode_fn = {
        'scan': run_scan,
        'sweep': run_sweep,
        'chaos': run_chaos,
        'consistency': run_consistency,
        'flow': run_flow,
        'atlas': run_atlas,
        'attack': run_attack,
        'robustness': run_robustness,
        'equations': run_equations,
        'topology': run_topology,
        'russell': run_russell,
        'ssa': run_ssa,
        'rate': run_rate,
        'meta_lens': run_meta_lens,
        'foo': run_foo,
        'phi': run_phi,
        'phi_atlas': run_phi_atlas,
        'breath': run_breath,
        'breath_rate': run_breath_rate,
        'breath_atlas': run_breath_atlas,
        'matrix': run_matrix,
        'full': run_full,
    }

    output = mode_fn[args.mode](spec, args)

    elapsed = time.time() - t0

    # ── Journal (if available) ──
    if SpectrometerJournal is not None:
        try:
            journal = SpectrometerJournal(args.output)

            if args.mode == 'matrix':
                journal.record_matrix(output)
            elif args.mode == 'full':
                if 'scan' in output:
                    journal.record_all(list(output['scan'].values()))
                if 'flow' in output:
                    journal.record_flows(output['flow'])
                if 'matrix' in output:
                    journal.record_matrix(output['matrix'])
                if 'atlas' in output:
                    journal.record_atlas(output['atlas'])
                if 'attack' in output:
                    journal.record_attack(output['attack'])
                if 'robustness' in output:
                    journal.record_robustness(output['robustness'])
                if 'equations' in output:
                    journal.record_equations(output['equations'])
                if 'meta_lens' in output:
                    journal.record_meta_lens(output['meta_lens'])
                if 'breath_atlas' in output:
                    journal.record_breath(output['breath_atlas'])
            elif args.mode in ('breath', 'breath_rate', 'breath_atlas'):
                journal.record_breath(output)
            elif args.mode == 'meta_lens':
                journal.record_meta_lens(output)
            elif args.mode == 'robustness':
                journal.record_robustness(output)
            elif args.mode == 'equations':
                journal.record_equations(output)
            elif args.mode in ('scan', 'sweep'):
                journal.record_all(list(output.values()))
            elif args.mode == 'chaos':
                flat = [r for results in output.values() for r in results]
                journal.record_all(flat)
            elif args.mode == 'flow':
                journal.record_flows(output)
            elif args.mode == 'atlas':
                journal.record_atlas(output)
            elif args.mode == 'attack':
                journal.record_attack(output)
            elif args.mode == 'consistency':
                pass  # consistency returns dicts, not SpectrometerResults

            journal.write_schema()
            print(f'\n  Output saved to: {os.path.abspath(args.output)}/')
        except Exception as e:
            print(f'\n  Journal error: {e}')
    else:
        print(f'\n  (SpectrometerJournal not available -- results printed only)')

    # ── Footer ──
    print(f'\n  Completed in {elapsed:.3f}s')
    print('  CK measures. CK does not prove.')
    print()


if __name__ == '__main__':
    main()
