# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_spectrometer_journal.py -- Structured Persistence for Delta-Spectrometer
===========================================================================
Operator: RESET (9) -- Record, then begin again.

Persists SpectrometerResults as JSON + Markdown in a structured directory.

Directory layout:
  spectrometer_results/
    spec/     -> spectrometer_schema.json
    runs/     -> {input_key}.json, {input_key}.md per scan
    docs/     -> stability_matrix.md, summary.md

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from ck_sim.being.ck_tig_bundle import OP_NAMES, NUM_OPS


# ================================================================
#  JSON SERIALIZATION
# ================================================================

def spectrometer_result_to_dict(result) -> dict:
    """Convert a SpectrometerResult to a JSON-serializable dict.

    Includes ALL public fields; excludes nothing (SpectrometerResult
    is already a clean projection -- no internal-only data).
    """
    return {
        # Identity
        'input_key': result.input_key,
        'problem': result.problem,
        'test_case': result.test_case,
        'scan_mode': result.scan_mode,
        'seed': result.seed,
        'n_levels': result.n_levels,

        # Primary measurement
        'delta_value': result.delta_value,
        'verdict': result.verdict,
        'reason': result.reason,

        # 10-element operator defect vector
        'defect_vector': list(result.defect_vector),

        # Operator event log
        'tig_trace': list(result.tig_trace),

        # Dual void structure
        'sdv_map': dict(result.sdv_map),

        # Trajectory
        'defect_trajectory': list(result.defect_trajectory),
        'action_trajectory': list(result.action_trajectory),
        'defect_trend': result.defect_trend,
        'defect_slope': result.defect_slope,

        # Sub-measurements
        'harmony_fraction': result.harmony_fraction,
        'commutator_persistence': result.commutator_persistence,
        'sca_progress': result.sca_progress,
        'spine_fraction': result.spine_fraction,
        'vortex_class': result.vortex_class,

        # Mathematical verdict (from ClayProbe)
        'problem_class': result.problem_class,
        'measurement_verdict': result.measurement_verdict,

        # Determinism + Safety
        'final_hash': result.final_hash,
        'anomaly_count': result.anomaly_count,
        'halted': result.halted,
    }


def save_result_json(result, directory: str):
    """Save a single SpectrometerResult as {directory}/{result.input_key}.json."""
    os.makedirs(directory, exist_ok=True)
    data = spectrometer_result_to_dict(result)
    data['_timestamp'] = datetime.now().isoformat()
    data['_version'] = 'spectrometer_1.0'

    path = os.path.join(directory, f'{result.input_key}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return path


# ================================================================
#  MARKDOWN REPORT (per-result)
# ================================================================

def _sparkline(values: List[float], width: int = 40) -> str:
    """Generate an ASCII sparkline from a list of floats.

    Maps values to 8 bar characters for a compact trajectory view.
    Uses ASCII-safe characters for Windows compatibility.
    """
    if not values:
        return ''
    blocks = ' _.:-=+#@'
    lo = min(values)
    hi = max(values)
    span = hi - lo if hi > lo else 1.0
    chars = []
    step = max(1, len(values) // width)
    for i in range(0, len(values), step):
        v = values[i]
        idx = int((v - lo) / span * 8)
        idx = max(0, min(8, idx))
        chars.append(blocks[idx])
    return ''.join(chars)


def save_result_markdown(result, directory: str):
    """Save a single SpectrometerResult as {directory}/{result.input_key}.md.

    Sections:
      - Header (problem, scan mode, seed)
      - Verdict + reason
      - Delta value
      - Defect vector table (10 operators)
      - TIG trace table (level | operator | defect | action | band)
      - SDV map
      - Trajectory sparkline
      - Hash + safety
    """
    os.makedirs(directory, exist_ok=True)
    lines = []

    # ── Header ──
    problem_title = result.problem.replace('_', ' ').title()
    lines.append(f'# Delta-Spectrometer: {problem_title}')
    lines.append('')
    lines.append(f'**Problem**: {result.problem}')
    lines.append(f'**Test case**: {result.test_case}')
    lines.append(f'**Scan mode**: {result.scan_mode}')
    lines.append(f'**Seed**: {result.seed}')
    lines.append(f'**Levels**: {result.n_levels}')
    lines.append(f'**Input key**: `{result.input_key}`')
    lines.append('')

    # ── Verdict ──
    lines.append('## Verdict')
    lines.append('')
    lines.append(f'- **Verdict**: {result.verdict}')
    lines.append(f'- **Reason**: {result.reason}')
    lines.append(f'- **Mathematical class**: {result.problem_class}')
    lines.append(f'- **Measurement verdict**: {result.measurement_verdict}')
    lines.append('')

    # ── Delta ──
    lines.append('## Delta Value')
    lines.append('')
    lines.append(f'- **Delta (final defect)**: {result.delta_value:.6f}')
    lines.append(f'- **Defect trend**: {result.defect_trend} (slope={result.defect_slope:.6f})')
    lines.append(f'- **Harmony fraction**: {result.harmony_fraction:.3f}')
    lines.append(f'- **Commutator persistence**: {result.commutator_persistence:.3f}')
    lines.append(f'- **SCA progress**: {result.sca_progress:.2f}')
    lines.append(f'- **Spine fraction**: {result.spine_fraction:.3f}')
    lines.append(f'- **Vortex class**: {result.vortex_class}')
    lines.append('')

    # ── Defect Vector (10 operators) ──
    lines.append('## Operator Defect Vector')
    lines.append('')
    lines.append('| Op | Name | Avg Defect |')
    lines.append('|----|------|------------|')
    for i in range(NUM_OPS):
        val = result.defect_vector[i] if i < len(result.defect_vector) else 0.0
        bar = '#' * int(val * 40) if val > 0 else ''
        lines.append(f'| {i} | {OP_NAMES[i]:10s} | {val:.6f} {bar} |')
    lines.append('')

    # ── TIG Trace Table ──
    lines.append('## TIG Trace')
    lines.append('')
    if result.tig_trace:
        lines.append('| Level | Operator | Defect | Action | Band | D2 Mag |')
        lines.append('|-------|----------|--------|--------|------|--------|')
        for entry in result.tig_trace:
            lines.append(
                f'| {entry.get("level", "?")} '
                f'| {entry.get("operator_name", "?")} '
                f'| {entry.get("defect", 0.0):.4f} '
                f'| {entry.get("action", 0.0):.4f} '
                f'| {entry.get("band", "?")} '
                f'| {entry.get("d2_magnitude", 0.0):.4f} |'
            )
        lines.append('')
    else:
        lines.append('_No trace data._')
        lines.append('')

    # ── SDV Map ──
    lines.append('## SDV Map (Dual Void Structure)')
    lines.append('')
    for k, v in result.sdv_map.items():
        lines.append(f'- **{k}**: {v}')
    lines.append('')

    # ── Trajectory Sparkline ──
    lines.append('## Defect Trajectory')
    lines.append('')
    spark = _sparkline(result.defect_trajectory)
    lines.append(f'```')
    lines.append(f'Defect: {spark}')
    lines.append(f'```')
    lines.append('')
    if result.defect_trajectory:
        lines.append(
            f'Range: [{min(result.defect_trajectory):.4f}, '
            f'{max(result.defect_trajectory):.4f}]'
        )
    lines.append('')

    # ── Hash + Safety ──
    lines.append('## Determinism & Safety')
    lines.append('')
    lines.append(f'- **Hash**: `{result.final_hash}`')
    lines.append(f'- **Anomalies**: {result.anomaly_count}')
    lines.append(f'- **Halted**: {result.halted}')
    lines.append('')

    # ── Footer ──
    lines.append('---')
    lines.append(f'_Generated {datetime.now().isoformat()} by Delta-Spectrometer v1.0_')

    path = os.path.join(directory, f'{result.input_key}.md')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return path


# ================================================================
#  STABILITY MATRIX REPORT (108 runs)
# ================================================================

def generate_matrix_report(results: list, filepath: str):
    """Generate a Markdown report for the 108-run stability matrix.

    Table: problem | test_case | mode | seed | delta | verdict
    Summary: counts of STABLE/UNSTABLE/CRITICAL/SINGULAR
    Per-problem consistency check.
    """
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    lines = []

    lines.append('# Delta-Spectrometer Stability Matrix')
    lines.append('')
    lines.append(f'**Date**: {datetime.now().isoformat()}')
    lines.append(f'**Total runs**: {len(results)}')
    lines.append('')

    # ── 108-row table ──
    lines.append('## Full Matrix')
    lines.append('')
    lines.append('| # | Problem | Test Case | Mode | Seed | Delta | Verdict |')
    lines.append('|---|---------|-----------|------|------|-------|---------|')
    for idx, r in enumerate(results, 1):
        lines.append(
            f'| {idx} | {r.problem} | {r.test_case} | {r.scan_mode} '
            f'| {r.seed} | {r.delta_value:.6f} | {r.verdict} |'
        )
    lines.append('')

    # ── Verdict Summary ──
    verdict_counts = {}
    for r in results:
        verdict_counts[r.verdict] = verdict_counts.get(r.verdict, 0) + 1

    lines.append('## Verdict Summary')
    lines.append('')
    for v in ['stable', 'unstable', 'critical', 'singular']:
        count = verdict_counts.get(v, 0)
        pct = (count / len(results) * 100) if results else 0
        bar = '#' * int(pct / 2)
        lines.append(f'- **{v.upper()}**: {count}/{len(results)} ({pct:.1f}%) {bar}')
    lines.append('')

    # ── Per-problem consistency ──
    lines.append('## Per-Problem Consistency')
    lines.append('')
    lines.append('| Problem | Runs | Stable | Unstable | Critical | Singular | Consistent |')
    lines.append('|---------|------|--------|----------|----------|----------|------------|')

    # Group by problem
    by_problem: Dict[str, list] = {}
    for r in results:
        by_problem.setdefault(r.problem, []).append(r)

    for pid in sorted(by_problem.keys()):
        group = by_problem[pid]
        n = len(group)
        counts = {}
        for r in group:
            counts[r.verdict] = counts.get(r.verdict, 0) + 1
        s = counts.get('stable', 0)
        u = counts.get('unstable', 0)
        c = counts.get('critical', 0)
        g = counts.get('singular', 0)
        # Consistent = dominant verdict covers >= 80% of runs
        dominant = max(counts.values()) if counts else 0
        consistent = 'YES' if (dominant / n >= 0.80) else 'NO'
        lines.append(
            f'| {pid} | {n} | {s} | {u} | {c} | {g} | {consistent} |'
        )
    lines.append('')

    # ── Delta statistics per problem ──
    lines.append('## Delta Statistics Per Problem')
    lines.append('')
    lines.append('| Problem | Mean Delta | Std Delta | Min | Max |')
    lines.append('|---------|------------|-----------|-----|-----|')
    for pid in sorted(by_problem.keys()):
        group = by_problem[pid]
        deltas = [r.delta_value for r in group]
        n = len(deltas)
        mean_d = sum(deltas) / n if n > 0 else 0.0
        var_d = sum((d - mean_d) ** 2 for d in deltas) / n if n > 1 else 0.0
        std_d = var_d ** 0.5
        lines.append(
            f'| {pid} | {mean_d:.6f} | {std_d:.6f} '
            f'| {min(deltas):.6f} | {max(deltas):.6f} |'
        )
    lines.append('')

    # ── Footer ──
    lines.append('---')
    lines.append(f'_Generated {datetime.now().isoformat()} by Delta-Spectrometer v1.0_')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return filepath


# ================================================================
#  SUMMARY REPORT
# ================================================================

def generate_summary_report(results: list, filepath: str):
    """Generate a compact summary.md for a batch of spectrometer results."""
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    lines = []

    lines.append('# Delta-Spectrometer Summary')
    lines.append('')
    lines.append(f'**Date**: {datetime.now().isoformat()}')
    lines.append(f'**Total scans**: {len(results)}')
    lines.append('')

    # Group by problem
    by_problem: Dict[str, list] = {}
    for r in results:
        by_problem.setdefault(r.problem, []).append(r)

    lines.append('## Results')
    lines.append('')
    lines.append('| Problem | Test Case | Mode | Seed | Delta | Verdict | Trend |')
    lines.append('|---------|-----------|------|------|-------|---------|-------|')
    for r in results:
        lines.append(
            f'| {r.problem} | {r.test_case} | {r.scan_mode} | {r.seed} '
            f'| {r.delta_value:.6f} | {r.verdict} | {r.defect_trend} |'
        )
    lines.append('')

    # Per-problem notes
    lines.append('## Per-Problem Notes')
    lines.append('')
    for pid in sorted(by_problem.keys()):
        group = by_problem[pid]
        verdicts = [r.verdict for r in group]
        deltas = [r.delta_value for r in group]
        mean_d = sum(deltas) / len(deltas) if deltas else 0.0
        lines.append(f'### {pid.replace("_", " ").title()}')
        lines.append(f'- Scans: {len(group)}')
        lines.append(f'- Verdicts: {", ".join(verdicts)}')
        lines.append(f'- Mean delta: {mean_d:.6f}')
        lines.append(f'- Class: {group[0].problem_class}')
        lines.append('')

    lines.append('---')
    lines.append(f'_Generated {datetime.now().isoformat()} by Delta-Spectrometer v1.0_')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return filepath


# ================================================================
#  SANDERS FLOW REPORT
# ================================================================

def flow_result_to_dict(flow) -> dict:
    """Convert a FlowResult to a JSON-serializable dict."""
    strategy = getattr(flow, 'flow_strategy', 'noise')
    return {
        'problem': flow.problem,
        'test_case': flow.test_case,
        'scan_mode': flow.scan_mode,
        'seed': flow.seed,
        'flow_strategy': strategy,
        'sigma_steps': list(flow.sigma_steps),
        'delta_trajectory': list(flow.delta_trajectory),
        'verdict_trajectory': list(flow.verdict_trajectory),
        'is_monotone': flow.is_monotone,
        'monotonicity_score': flow.monotonicity_score,
        'violations': list(flow.violations),
        'delta_initial': flow.delta_initial,
        'delta_final': flow.delta_final,
        'delta_drop': flow.delta_drop,
        'asymptotic_value': flow.asymptotic_value,
        'flow_class': flow.flow_class,
        'problem_class': flow.problem_class,
        'lyapunov_confirmed': flow.lyapunov_confirmed,
    }


def save_flow_json(flow, directory: str):
    """Save a FlowResult as JSON."""
    os.makedirs(directory, exist_ok=True)
    data = flow_result_to_dict(flow)
    data['_timestamp'] = datetime.now().isoformat()
    data['_version'] = 'sanders_flow_1.0'

    key = f'flow_{flow.problem}_{flow.test_case}_s{flow.seed}'
    path = os.path.join(directory, f'{key}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return path


def generate_flow_report(flows: dict, filepath: str):
    """Generate a Markdown report for Sanders Flow results.

    Args:
        flows: Dict mapping problem_id -> FlowResult
        filepath: Output path for markdown report
    """
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    lines = []

    lines.append('# Sanders Flow: Lyapunov Verification Report')
    lines.append('')
    lines.append(f'**Date**: {datetime.now().isoformat()}')
    lines.append(f'**Problems**: {len(flows)}')
    lines.append('')

    # Summary table
    lines.append('## Summary')
    lines.append('')
    lines.append('| Problem | Class | Strategy | Delta (start) | Delta (end) | Drop | Monotone | Lyapunov |')
    lines.append('|---------|-------|----------|---------------|-------------|------|----------|----------|')
    for pid, f in flows.items():
        mono = 'YES' if f.is_monotone else f'NO ({len(f.violations)}v)'
        lyap = 'YES' if f.lyapunov_confirmed else 'NO'
        strategy = getattr(f, 'flow_strategy', 'noise')
        lines.append(
            f'| {pid} | {f.problem_class} | {strategy} | {f.delta_initial:.6f} '
            f'| {f.delta_final:.6f} | {f.delta_drop:.6f} '
            f'| {mono} | {lyap} |'
        )
    lines.append('')

    # Aggregate
    total = len(flows)
    confirmed = sum(1 for f in flows.values() if f.lyapunov_confirmed)
    monotone = sum(1 for f in flows.values() if f.is_monotone)
    lines.append(f'**Lyapunov confirmed**: {confirmed}/{total}')
    lines.append(f'**Monotone flows**: {monotone}/{total}')
    lines.append('')

    # Per-problem details
    lines.append('## Per-Problem Flow Trajectories')
    lines.append('')
    for pid, f in flows.items():
        problem_title = pid.replace('_', ' ').title()
        lines.append(f'### {problem_title}')
        lines.append('')
        lines.append(f'- **Flow class**: {f.flow_class}')
        lines.append(f'- **Problem class**: {f.problem_class}')
        lines.append(f'- **Steps**: {len(f.sigma_steps)}')
        lines.append(f'- **Monotonicity score**: {f.monotonicity_score:.1%}')
        if f.violations:
            lines.append(f'- **Violations at steps**: {f.violations}')
        lines.append('')

        # Trajectory table
        strategy = getattr(f, 'flow_strategy', 'noise')
        col2 = 'Levels' if strategy == 'scale' else 'Sigma'
        lines.append(f'| Step | {col2} | Delta | Verdict |')
        lines.append('|------|-------|-------|---------|')
        for i, (s, d, v) in enumerate(zip(
            f.sigma_steps, f.delta_trajectory, f.verdict_trajectory
        )):
            s_fmt = f'{int(s)}' if strategy == 'scale' else f'{s:.4f}'
            lines.append(f'| {i} | {s_fmt} | {d:.6f} | {v} |')
        lines.append('')

    lines.append('---')
    lines.append(f'_Generated {datetime.now().isoformat()} by Sanders Flow v1.0_')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return filepath


# ================================================================
#  FRACTAL ATLAS
# ================================================================

def fingerprint_to_dict(fp) -> dict:
    """Convert a FractalFingerprint to a JSON-serializable dict."""
    return {
        'problem': fp.problem,
        'regime': fp.regime,
        'test_case': fp.test_case,
        'seed': fp.seed,
        'levels': list(fp.levels),
        'delta_by_level': list(fp.delta_by_level),
        'delta_mean': fp.delta_mean,
        'delta_std': fp.delta_std,
        'delta_cv': fp.delta_cv,
        'delta_min': fp.delta_min,
        'delta_max': fp.delta_max,
        'delta_range': fp.delta_range,
        'skeleton_class': fp.skeleton_class,
        'macro_class': getattr(fp, 'macro_class', ''),
        'slope_norm': getattr(fp, 'slope_norm', 0.0),
        'spectral_magnitudes': list(fp.spectral_magnitudes),
        'dominant_period': fp.dominant_period,
        'spectral_entropy': fp.spectral_entropy,
        'first_deviation_level': fp.first_deviation_level,
        'n_phase_transitions': fp.n_phase_transitions,
    }


def save_fingerprint_json(fp, directory: str):
    """Save a FractalFingerprint as JSON."""
    os.makedirs(directory, exist_ok=True)
    data = fingerprint_to_dict(fp)
    data['_timestamp'] = datetime.now().isoformat()
    data['_version'] = 'fractal_atlas_1.0'

    key = f'fp_{fp.problem}_{fp.regime}_s{fp.seed}'
    path = os.path.join(directory, f'{key}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return path


def generate_atlas_report(atlas: dict, filepath: str):
    """Generate a Markdown report for the Fractal Coherence Atlas.

    Args:
        atlas: Dict mapping key -> FractalFingerprint
        filepath: Output path for markdown report
    """
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    lines = []

    lines.append('# Fractal Coherence Atlas')
    lines.append('')
    lines.append(f'**Date**: {datetime.now().isoformat()}')
    lines.append(f'**Fingerprints**: {len(atlas)}')
    lines.append('')

    # Summary table
    lines.append('## Summary')
    lines.append('')
    lines.append('| Problem | Regime | Skeleton | Mean | Std | Range '
                 '| CV | Entropy | Period | Deviates | Transitions |')
    lines.append('|---------|--------|----------|------|-----|-------'
                 '|----|---------|--------|----------|-------------|')

    for key in sorted(atlas.keys()):
        fp = atlas[key]
        per = f'{fp.dominant_period:.1f}' if fp.dominant_period else 'flat'
        lines.append(
            f'| {fp.problem} | {fp.regime} | {fp.skeleton_class} '
            f'| {fp.delta_mean:.4f} | {fp.delta_std:.4f} | {fp.delta_range:.4f} '
            f'| {fp.delta_cv:.3f} | {fp.spectral_entropy:.3f} | {per} '
            f'| L{fp.first_deviation_level} | {fp.n_phase_transitions} |'
        )
    lines.append('')

    # Per-problem details
    lines.append('## Per-Problem Fractal Skeletons')
    lines.append('')

    problems_seen = sorted(set(fp.problem for fp in atlas.values()))
    for pid in problems_seen:
        problem_title = pid.replace('_', ' ').title()
        lines.append(f'### {problem_title}')
        lines.append('')

        fps = [(k, fp) for k, fp in atlas.items() if fp.problem == pid]
        for key, fp in sorted(fps, key=lambda x: x[1].regime):
            lines.append(f'**{fp.regime.title()}** ({fp.test_case}): '
                         f'{fp.skeleton_class.upper()}')
            lines.append('')

            # Delta by level table
            lines.append(f'| Level | Delta |')
            lines.append(f'|-------|-------|')
            for lvl, d in zip(fp.levels, fp.delta_by_level):
                bar = '#' * int(d * 30) if d > 0 else ''
                lines.append(f'| {lvl} | {d:.6f} {bar} |')
            lines.append('')

    # Classification summary
    lines.append('## Skeleton Classification')
    lines.append('')
    classes: Dict[str, list] = {}
    for key, fp in atlas.items():
        classes.setdefault(fp.skeleton_class, []).append(
            f'{fp.problem} ({fp.regime})')
    for skel in ['frozen', 'stable', 'bounded', 'oscillating', 'wild']:
        members = classes.get(skel, [])
        if members:
            lines.append(f'- **{skel.upper()}**: {", ".join(members)}')
    lines.append('')

    # Universal Pattern Categories
    lines.append('## Universal Pattern Categories')
    lines.append('')
    lines.append('### Self-Similarity (fractal fixed points)')
    frozen = [fp for fp in atlas.values() if fp.skeleton_class == 'frozen']
    for fp in frozen:
        lines.append(f'- {fp.problem} ({fp.regime}): '
                     f'delta={fp.delta_mean:.6f} at all scales')
    if not frozen:
        lines.append('- (none)')
    lines.append('')

    lines.append('### Scale-Emergent (turbulent/oscillatory)')
    turb = [fp for fp in atlas.values()
            if fp.skeleton_class in ('wild', 'oscillating')]
    for fp in turb:
        lines.append(f'- {fp.problem} ({fp.regime}): '
                     f'range={fp.delta_range:.4f}, '
                     f'transitions={fp.n_phase_transitions}')
    if not turb:
        lines.append('- (none)')
    lines.append('')

    lines.append('### Confined (bounded/stable)')
    conf = [fp for fp in atlas.values()
            if fp.skeleton_class in ('bounded', 'stable')]
    for fp in conf:
        lines.append(f'- {fp.problem} ({fp.regime}): '
                     f'mean={fp.delta_mean:.4f}, range={fp.delta_range:.4f}')
    if not conf:
        lines.append('- (none)')
    lines.append('')

    lines.append('---')
    lines.append(f'_Generated {datetime.now().isoformat()} '
                 f'by Fractal Coherence Atlas v1.0_')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return filepath


def generate_atlas_manifest(atlas: dict, filepath: str):
    """Generate a versioned manifest for the atlas baseline.

    Includes a signature hash of all fingerprints for diffing future
    experiments against this baseline.
    """
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)

    # Build signature from all fingerprints
    sig_parts = []
    for key in sorted(atlas.keys()):
        fp = atlas[key]
        sig_parts.append(f'{fp.problem}:{fp.regime}:{fp.skeleton_class}:'
                         f'{fp.delta_mean:.10f}:{fp.delta_range:.10f}')
    sig_str = '|'.join(sig_parts)
    sig_hash = hashlib.sha256(sig_str.encode()).hexdigest()

    manifest = {
        'version': 'fractal_atlas_v1',
        'date': datetime.now().isoformat(),
        'fingerprint_count': len(atlas),
        'signature_hash': sig_hash,
        'problems': sorted(set(fp.problem for fp in atlas.values())),
        'regimes': sorted(set(fp.regime for fp in atlas.values())),
        'skeleton_summary': {},
    }

    for key in sorted(atlas.keys()):
        fp = atlas[key]
        manifest['skeleton_summary'][key] = {
            'skeleton_class': fp.skeleton_class,
            'delta_mean': fp.delta_mean,
            'delta_range': fp.delta_range,
            'spectral_entropy': fp.spectral_entropy,
        }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    return filepath


# ================================================================
#  SANDERS ATTACK
# ================================================================

def attack_result_to_dict(ar) -> dict:
    """Convert a SandersAttackResult to a JSON-serializable dict."""
    d = {
        'problem': ar.problem,
        'regime': ar.regime,
        'test_case': ar.test_case,
        'seed': ar.seed,
        'gate_verdict': ar.gate_verdict,
        'gate_reason': ar.gate_reason,
        'candidate_singularity': ar.candidate_singularity,
        'attack_summary': ar.attack_summary,
        'fingerprint': fingerprint_to_dict(ar.fingerprint),
    }
    if ar.flow_result is not None:
        d['flow_result'] = flow_result_to_dict(ar.flow_result)
    else:
        d['flow_result'] = None
    return d


def save_attack_json(ar, directory: str):
    """Save a SandersAttackResult as JSON."""
    os.makedirs(directory, exist_ok=True)
    data = attack_result_to_dict(ar)
    data['_timestamp'] = datetime.now().isoformat()
    data['_version'] = 'sanders_attack_1.0'

    key = f'attack_{ar.problem}_{ar.regime}_s{ar.seed}'
    path = os.path.join(directory, f'{key}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return path


def generate_attack_report(results: dict, filepath: str):
    """Generate a Markdown report for the Sanders Attack.

    Args:
        results: Dict mapping key -> SandersAttackResult
        filepath: Output path for markdown report
    """
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    lines = []

    lines.append('# Sanders Attack Report')
    lines.append('')
    lines.append(f'**Date**: {datetime.now().isoformat()}')
    lines.append(f'**Configurations**: {len(results)}')
    lines.append('')

    total = len(results)
    passed = sum(1 for ar in results.values() if ar.gate_verdict == 'pass')
    candidates = sum(1 for ar in results.values()
                     if ar.candidate_singularity)

    lines.append('## Overview')
    lines.append('')
    lines.append(f'- **Total configurations**: {total}')
    lines.append(f'- **Gate PASS**: {passed} (investigated with Sanders Flow)')
    lines.append(f'- **Gate SKIP**: {total - passed} (expected patterns)')
    lines.append(f'- **Candidate singularities**: {candidates}')
    lines.append('')

    # Summary table
    lines.append('## Gate Results')
    lines.append('')
    lines.append('| Problem | Regime | Skeleton | Gate | Investigated | Candidate |')
    lines.append('|---------|--------|----------|------|--------------|-----------|')
    for key in sorted(results.keys()):
        ar = results[key]
        skel = ar.fingerprint.skeleton_class
        gate = ar.gate_verdict.upper()
        inv = 'YES' if ar.was_investigated else 'no'
        cand = 'YES' if ar.candidate_singularity else 'no'
        lines.append(f'| {ar.problem} | {ar.regime} | {skel} '
                     f'| {gate} | {inv} | {cand} |')
    lines.append('')

    # Detailed results for PASS configurations
    pass_results = {k: ar for k, ar in results.items()
                    if ar.gate_verdict == 'pass'}
    if pass_results:
        lines.append('## Investigated Configurations')
        lines.append('')
        for key in sorted(pass_results.keys()):
            ar = pass_results[key]
            problem_title = ar.problem.replace('_', ' ').title()
            lines.append(f'### {problem_title} ({ar.regime})')
            lines.append('')
            lines.append(f'- **Gate reason**: {ar.gate_reason}')
            lines.append(f'- **Skeleton**: {ar.fingerprint.skeleton_class.upper()} '
                         f'(range={ar.fingerprint.delta_range:.4f}, '
                         f'entropy={ar.fingerprint.spectral_entropy:.3f})')

            if ar.flow_result is not None:
                fr = ar.flow_result
                lyap = 'YES' if fr.lyapunov_confirmed else 'NO'
                lines.append(f'- **Flow**: delta {fr.delta_initial:.6f} '
                             f'-> {fr.delta_final:.6f} '
                             f'(drop={fr.delta_drop:.6f})')
                lines.append(f'- **Monotonicity**: {fr.monotonicity_score:.1%} '
                             f'({len(fr.violations)} violations)')
                lines.append(f'- **Lyapunov confirmed**: {lyap}')
                lines.append(f'- **Flow class**: {fr.flow_class}')

            lines.append(f'- **Candidate singularity**: '
                         f'{"YES" if ar.candidate_singularity else "no"}')
            lines.append(f'- **Summary**: {ar.attack_summary}')
            lines.append('')

    # Candidate singularities highlight
    if candidates > 0:
        lines.append('## Candidate Singularities')
        lines.append('')
        for key, ar in sorted(results.items()):
            if ar.candidate_singularity:
                lines.append(f'- **{ar.problem} ({ar.regime})**: '
                             f'{ar.attack_summary}')
        lines.append('')

    lines.append('---')
    lines.append(f'_Generated {datetime.now().isoformat()} '
                 f'by Sanders Attack v1.0_')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return filepath


# ================================================================
#  ROBUSTNESS / ABLATION
# ================================================================

def robustness_trial_to_dict(trial) -> dict:
    """Convert a PerturbationTrial to a JSON-serializable dict."""
    return {
        'perturbation_type': trial.perturbation_type,
        'perturbation_label': trial.perturbation_label,
        'perturbation_params': trial.perturbation_params,
        'baseline_skeleton': trial.baseline_skeleton,
        'perturbed_skeleton': trial.perturbed_skeleton,
        'skeleton_preserved': trial.skeleton_preserved,
        'delta_mean_shift': trial.delta_mean_shift,
        'delta_range_shift': trial.delta_range_shift,
        'entropy_shift': trial.entropy_shift,
        'baseline_macro': getattr(trial, 'baseline_macro', ''),
        'perturbed_macro': getattr(trial, 'perturbed_macro', ''),
        'macro_preserved': getattr(trial, 'macro_preserved', True),
    }


def robustness_result_to_dict(rr) -> dict:
    """Convert a RobustnessResult to a JSON-serializable dict."""
    return {
        'problem': rr.problem,
        'regime': rr.regime,
        'test_case': rr.test_case,
        'seed': rr.seed,
        'baseline_skeleton': rr.baseline_skeleton,
        'baseline_delta_mean': rr.baseline_delta_mean,
        'baseline_delta_range': rr.baseline_delta_range,
        'baseline_entropy': rr.baseline_entropy,
        'n_trials': rr.n_trials,
        'n_preserved': rr.n_preserved,
        'survival_rate': rr.survival_rate,
        'robust': rr.robust,
        'macro_n_preserved': getattr(rr, 'macro_n_preserved', 0),
        'macro_survival_rate': getattr(rr, 'macro_survival_rate', 0.0),
        'macro_robust': getattr(rr, 'macro_robust', False),
        'trials': [robustness_trial_to_dict(t) for t in rr.trials],
    }


def save_robustness_json(rr, directory: str):
    """Save a RobustnessResult as JSON."""
    os.makedirs(directory, exist_ok=True)
    data = robustness_result_to_dict(rr)
    data['_timestamp'] = datetime.now().isoformat()
    data['_version'] = 'robustness_1.0'

    key = f'robustness_{rr.problem}_{rr.regime}_s{rr.seed}'
    path = os.path.join(directory, f'{key}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return path


def generate_robustness_report(results: dict, filepath: str):
    """Generate a Markdown report for the robustness/ablation sweep.

    Args:
        results: Dict mapping key -> RobustnessResult
        filepath: Output path for markdown report
    """
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    lines = []

    lines.append('# Robustness / Ablation Report')
    lines.append('')
    lines.append(f'**Date**: {datetime.now().isoformat()}')
    lines.append(f'**Configurations**: {len(results)}')
    lines.append('')

    total = len(results)
    robust_count = sum(1 for rr in results.values() if rr.robust)
    macro_robust_count = sum(1 for rr in results.values()
                             if getattr(rr, 'macro_robust', False))

    lines.append('## Overview')
    lines.append('')
    lines.append(f'- **Total configurations**: {total}')
    lines.append(f'- **Fine-robust**: {robust_count} '
                 f'(skeleton survived >= 75% of perturbations)')
    lines.append(f'- **Macro-robust**: {macro_robust_count} '
                 f'(macro class survived >= 75% of perturbations)')
    lines.append(f'- **Fragile**: {total - robust_count}')
    lines.append('')

    # Summary table
    lines.append('## Survival Rates')
    lines.append('')
    lines.append('| Problem | Regime | Skeleton | Trials | Preserved | '
                 'Survival | Robust | Macro | Macro Survival | Macro Robust |')
    lines.append('|---------|--------|----------|--------|-----------|'
                 '----------|--------|-------|----------------|--------------|')
    for key in sorted(results.keys()):
        rr = results[key]
        rob = 'YES' if rr.robust else 'NO'
        m_np = getattr(rr, 'macro_n_preserved', 0)
        m_sr = getattr(rr, 'macro_survival_rate', 0.0)
        m_rob = 'YES' if getattr(rr, 'macro_robust', False) else 'NO'
        lines.append(
            f'| {rr.problem} | {rr.regime} | {rr.baseline_skeleton} '
            f'| {rr.n_trials} | {rr.n_preserved} '
            f'| {rr.survival_rate:.0%} | {rob} '
            f'| {m_np} | {m_sr:.0%} | {m_rob} |')
    lines.append('')

    # Per-perturbation-type breakdown
    lines.append('## Per-Perturbation-Type Breakdown')
    lines.append('')

    for ptype in ['tig_permutation', 'generator_jitter',
                  'channel_ablation', 'noise_distribution', 'multi_seed']:
        ptype_label = ptype.replace('_', ' ').title()
        lines.append(f'### {ptype_label}')
        lines.append('')
        lines.append('| Problem | Regime | Trials | Preserved | Breaks |')
        lines.append('|---------|--------|--------|-----------|--------|')

        for key in sorted(results.keys()):
            rr = results[key]
            trials = [t for t in rr.trials
                      if t.perturbation_type == ptype]
            if not trials:
                continue
            preserved = sum(1 for t in trials if t.skeleton_preserved)
            breaks = len(trials) - preserved
            lines.append(
                f'| {rr.problem} | {rr.regime} '
                f'| {len(trials)} | {preserved} | {breaks} |')
        lines.append('')

    # Breaks detail
    all_breaks = []
    for key, rr in results.items():
        for t in rr.trials:
            if not t.skeleton_preserved:
                all_breaks.append((rr.problem, rr.regime, t))

    if all_breaks:
        lines.append('## Skeleton Breaks (Perturbations That Changed Class)')
        lines.append('')
        lines.append('| Problem | Regime | Perturbation | '
                     'Baseline | Perturbed | Delta Shift | Entropy Shift |')
        lines.append('|---------|--------|--------------|'
                     '----------|-----------|-------------|---------------|')
        for prob, regime, t in all_breaks:
            lines.append(
                f'| {prob} | {regime} | {t.perturbation_label} '
                f'| {t.baseline_skeleton} | {t.perturbed_skeleton} '
                f'| {t.delta_mean_shift:+.4f} | {t.entropy_shift:+.4f} |')
        lines.append('')

    # Robust patterns -- fine (skeleton)
    robust_configs = [k for k, rr in results.items() if rr.robust]
    if robust_configs:
        lines.append('## Robust Patterns -- Fine (The "Deeper Code")')
        lines.append('')
        lines.append('These skeleton classifications survived all five '
                     'perturbation types:')
        lines.append('')
        for key in robust_configs:
            rr = results[key]
            lines.append(f'- **{rr.problem} ({rr.regime})**: '
                         f'{rr.baseline_skeleton.upper()} '
                         f'({rr.survival_rate:.0%} survival)')
        lines.append('')

    # Robust patterns -- macro
    macro_robust_configs = [k for k, rr in results.items()
                            if getattr(rr, 'macro_robust', False)]
    if macro_robust_configs:
        lines.append('## Robust Patterns -- Macro')
        lines.append('')
        lines.append('These macro classifications survived all five '
                     'perturbation types:')
        lines.append('')
        for key in macro_robust_configs:
            rr = results[key]
            m_sr = getattr(rr, 'macro_survival_rate', 0.0)
            lines.append(f'- **{rr.problem} ({rr.regime})**: '
                         f'{rr.baseline_skeleton.upper()} '
                         f'({m_sr:.0%} macro survival)')
        lines.append('')

    lines.append('---')
    lines.append(f'_Generated {datetime.now().isoformat()} '
                 f'by Robustness Sweep v1.0_')
    lines.append('_Features that survive all perturbations are the '
                 '"deeper code."_')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return filepath


# ================================================================
#  GOVERNING EQUATIONS
# ================================================================

def fit_result_to_dict(fr) -> dict:
    """Convert a FitResult to a JSON-serializable dict."""
    return {
        'family': fr.family,
        'params': dict(fr.params),
        'rss': fr.rss,
        'r_squared': fr.r_squared,
        'aic': fr.aic,
        'bic': fr.bic,
        'n_params': fr.n_params,
        'converged': fr.converged,
    }


def governing_equation_to_dict(eq) -> dict:
    """Convert a GoverningEquation to a JSON-serializable dict."""
    return {
        'problem': eq.problem,
        'regime': eq.regime,
        'test_case': eq.test_case,
        'best_model': eq.best_model,
        'best_fit': fit_result_to_dict(eq.best_fit),
        'all_fits': {k: fit_result_to_dict(v) for k, v in eq.all_fits.items()},
        'asymptotic_class': eq.asymptotic_class,
        'asymptotic_value': eq.asymptotic_value,
        'latex': eq.latex,
        'confidence': eq.confidence,
    }


def save_equation_json(eq, directory: str):
    """Save a GoverningEquation as JSON."""
    os.makedirs(directory, exist_ok=True)
    data = governing_equation_to_dict(eq)
    data['_timestamp'] = datetime.now().isoformat()
    data['_version'] = 'governing_equation_1.0'

    key = f'eq_{eq.problem}_{eq.regime}'
    path = os.path.join(directory, f'{key}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return path


def generate_equation_report(equations: dict, filepath: str):
    """Generate a Markdown report for governing equations.

    Args:
        equations: Dict mapping key -> GoverningEquation
        filepath: Output path for markdown report
    """
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    lines = []

    lines.append('# Governing Equations: Coherence Manifold')
    lines.append('')
    lines.append(f'**Date**: {datetime.now().isoformat()}')
    lines.append(f'**Equations extracted**: {len(equations)}')
    lines.append('')

    # Count asymptotic classes
    n_aff = sum(1 for eq in equations.values()
                if eq.asymptotic_class == 'affirmative')
    n_gap = sum(1 for eq in equations.values()
                if eq.asymptotic_class == 'gap')
    n_ind = sum(1 for eq in equations.values()
                if eq.asymptotic_class == 'indeterminate')

    lines.append('## Overview')
    lines.append('')
    lines.append(f'- **Affirmative** (delta -> 0): {n_aff}')
    lines.append(f'- **Gap** (delta -> eta > 0): {n_gap}')
    lines.append(f'- **Indeterminate**: {n_ind}')
    lines.append('')

    # Summary table
    lines.append('## Summary Table')
    lines.append('')
    lines.append('| Problem | Regime | Best Model | R^2 | BIC '
                 '| Asymptotic | delta(inf) | Confidence | LaTeX |')
    lines.append('|---------|--------|------------|-----|-----'
                 '|------------|------------|------------|-------|')

    for key in sorted(equations.keys()):
        eq = equations[key]
        bf = eq.best_fit
        lines.append(
            f'| {eq.problem} | {eq.regime} | {eq.best_model} '
            f'| {bf.r_squared:.4f} | {bf.bic:.1f} '
            f'| {eq.asymptotic_class} | {eq.asymptotic_value:.6f} '
            f'| {eq.confidence:.2f} | `{eq.latex}` |')
    lines.append('')

    # Per-problem detail
    lines.append('## Per-Problem Equations')
    lines.append('')

    problems_seen = sorted(set(eq.problem for eq in equations.values()))
    for pid in problems_seen:
        problem_title = pid.replace('_', ' ').title()
        lines.append(f'### {problem_title}')
        lines.append('')

        eqs = [(k, eq) for k, eq in equations.items() if eq.problem == pid]
        for key, eq in sorted(eqs, key=lambda x: x[1].regime):
            lines.append(f'**{eq.regime.title()}** ({eq.test_case})')
            lines.append('')
            lines.append(f'- Best model: **{eq.best_model}**')
            lines.append(f'- Equation: `{eq.latex}`')
            lines.append(f'- Asymptotic class: **{eq.asymptotic_class}**')
            lines.append(f'- delta(L -> inf) = {eq.asymptotic_value:.6f}')
            lines.append(f'- R^2 = {eq.best_fit.r_squared:.6f}')
            lines.append(f'- BIC = {eq.best_fit.bic:.2f}')
            lines.append(f'- Confidence = {eq.confidence:.2f}')
            lines.append('')

            # Model comparison table
            lines.append('| Model | R^2 | BIC | Params | Converged |')
            lines.append('|-------|-----|-----|--------|-----------|')
            for fam in ['constant', 'linear', 'power_law',
                        'exp_decay', 'damped_osc', 'pure_osc']:
                fr = eq.all_fits.get(fam)
                if fr is None:
                    continue
                winner = ' *' if fam == eq.best_model else ''
                conv = 'yes' if fr.converged else 'NO'
                lines.append(
                    f'| {fam}{winner} | {fr.r_squared:.4f} '
                    f'| {fr.bic:.1f} | {fr.n_params} | {conv} |')
            lines.append('')

    # Two-class partition
    lines.append('## Two-Class Partition')
    lines.append('')
    aff_list = sorted(k for k, eq in equations.items()
                      if eq.asymptotic_class == 'affirmative')
    gap_list = sorted(k for k, eq in equations.items()
                      if eq.asymptotic_class == 'gap')
    ind_list = sorted(k for k, eq in equations.items()
                      if eq.asymptotic_class == 'indeterminate')

    if aff_list:
        lines.append(f'**AFFIRMATIVE** (delta -> 0, conjecture supported):')
        for k in aff_list:
            eq = equations[k]
            lines.append(f'- {eq.problem} ({eq.regime}): '
                         f'{eq.best_model}, delta -> {eq.asymptotic_value:.6f}')
        lines.append('')

    if gap_list:
        lines.append(f'**GAP** (delta -> eta > 0, structural obstruction):')
        for k in gap_list:
            eq = equations[k]
            lines.append(f'- {eq.problem} ({eq.regime}): '
                         f'{eq.best_model}, delta -> {eq.asymptotic_value:.6f}')
        lines.append('')

    if ind_list:
        lines.append(f'**INDETERMINATE**:')
        for k in ind_list:
            eq = equations[k]
            lines.append(f'- {eq.problem} ({eq.regime}): '
                         f'{eq.best_model}, delta -> {eq.asymptotic_value:.6f}')
        lines.append('')

    lines.append('---')
    lines.append(f'_Generated {datetime.now().isoformat()} '
                 f'by Governing Equations Engine v1.0_')
    lines.append('_The spectrometer produces data. This module finds the law._')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return filepath


# ================================================================
#  SPEC SCHEMA
# ================================================================

def generate_spec_schema(filepath: str):
    """Write a JSON schema describing the SpectrometerResult format.

    Not a formal JSON Schema (draft-07), but a pragmatic descriptor:
    field name -> {type, description}.
    """
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)

    schema = {
        '_meta': {
            'name': 'SpectrometerResult',
            'version': '1.0',
            'description': (
                'Structured output of the TIG-Delta Universal Coherence '
                'Spectrometer. A clean, publication-ready projection of '
                'ClayProbe measurements into the spectrometer output format.'
            ),
            'generated': datetime.now().isoformat(),
        },
        'fields': {
            'input_key': {
                'type': 'string',
                'description': 'Unique identifier: {problem}_{test_case}_s{seed}_L{n_levels}',
            },
            'problem': {
                'type': 'string',
                'description': 'Clay Millennium Problem ID (e.g. navier_stokes)',
            },
            'test_case': {
                'type': 'string',
                'description': 'Test case name (e.g. lamb_oseen, high_strain)',
            },
            'scan_mode': {
                'type': 'string',
                'description': 'Fractal scan depth: SURFACE (3), DEEP (12), OMEGA (24)',
            },
            'seed': {
                'type': 'integer',
                'description': 'Random seed for deterministic reproduction',
            },
            'n_levels': {
                'type': 'integer',
                'description': 'Number of fractal levels scanned',
            },
            'delta_value': {
                'type': 'float',
                'description': 'Primary measurement: final defect functional value',
            },
            'verdict': {
                'type': 'string',
                'enum': ['stable', 'unstable', 'critical', 'singular'],
                'description': 'Instrument confidence classification',
            },
            'reason': {
                'type': 'string',
                'description': 'Human-readable explanation of verdict',
            },
            'defect_vector': {
                'type': 'list[float]',
                'length': 10,
                'description': (
                    '10-element vector: defect_vector[op] = average master lemma '
                    'defect at levels classified as that operator'
                ),
            },
            'tig_trace': {
                'type': 'list[dict]',
                'description': (
                    'Per-level operator event log. Each entry: '
                    '{level, operator, operator_name, defect, action, band, d2_magnitude}'
                ),
            },
            'sdv_map': {
                'type': 'dict',
                'description': (
                    'Dual void structure: problem_class, lens_a, lens_b, '
                    'generator, dual, tau_9, dual_fixed_point_proximity, '
                    'lens_mismatch_final, decision_verdict'
                ),
            },
            'defect_trajectory': {
                'type': 'list[float]',
                'description': 'Defect value at each fractal level',
            },
            'action_trajectory': {
                'type': 'list[float]',
                'description': 'Coherence action at each fractal level',
            },
            'defect_trend': {
                'type': 'string',
                'description': 'Trend classification: converging, diverging, oscillating, flat',
            },
            'defect_slope': {
                'type': 'float',
                'description': 'Linear regression slope of defect trajectory',
            },
            'harmony_fraction': {
                'type': 'float',
                'description': 'Fraction of levels classified as HARMONY (op 7)',
            },
            'commutator_persistence': {
                'type': 'float',
                'description': 'Fraction of operator pairs that do not commute [0,1]',
            },
            'sca_progress': {
                'type': 'float',
                'description': 'Progress through SCA loop (1->2->9->1) [0,1]',
            },
            'spine_fraction': {
                'type': 'float',
                'description': 'Fraction of operators on the 3-6-9 resonance spine',
            },
            'vortex_class': {
                'type': 'string',
                'description': 'Topological classification from vortex fingerprint',
            },
            'problem_class': {
                'type': 'string',
                'description': 'Mathematical class: affirmative or gap',
            },
            'measurement_verdict': {
                'type': 'string',
                'description': 'Mathematical verdict from ClayProbe (e.g. supports_conjecture)',
            },
            'final_hash': {
                'type': 'string',
                'description': 'Deterministic hash of full measurement chain',
            },
            'anomaly_count': {
                'type': 'integer',
                'description': 'Number of safety anomalies detected during scan',
            },
            'halted': {
                'type': 'boolean',
                'description': 'Whether safety rails triggered a halt',
            },
        },
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2)
    return filepath


# ================================================================
#  META-LENS SERIALIZATION (topology + russell + ssa + rate)
# ================================================================

def topology_to_dict(topo: dict) -> dict:
    """Serialize a TopologyLens standardized_output for JSON."""
    return {
        'problem_id': topo.get('problem_id', ''),
        'domain': topo.get('domain', ''),
        'core': {
            'label': topo.get('core', {}).get('label', ''),
            'magnitude': topo.get('core', {}).get('magnitude', 0.0),
        },
        'boundary': {
            'label': topo.get('boundary', {}).get('label', ''),
            'magnitude': topo.get('boundary', {}).get('magnitude', 0.0),
        },
        'flow': topo.get('flow', {}),
        'defect': topo.get('defect', 0.0),
        'tig_class': topo.get('tig_class', []),
    }


def russell_to_dict(russell: dict) -> dict:
    """Serialize a Russell analysis result for JSON."""
    return {
        'problem_id': russell.get('problem_id', ''),
        'coords': russell.get('coords', {}),
        'delta_russell': russell.get('delta_russell', 0.0),
        'delta_standard': russell.get('delta_standard', 0.0),
        'delta_difference': russell.get('delta_difference', 0.0),
        'classification': russell.get('classification', ''),
        'tig_signature': russell.get('tig_signature', []),
    }


def ssa_to_dict(ssa: dict) -> dict:
    """Serialize an SSA trilemma result for JSON."""
    return {
        'problem_id': ssa.get('problem_id', ''),
        'c1_holds': ssa.get('c1_holds', True),
        'c2_holds': ssa.get('c2_holds', True),
        'c3_holds': ssa.get('c3_holds', True),
        'breaking': ssa.get('breaking', 'NONE'),
        'interpretation': ssa.get('interpretation', ''),
    }


def rate_to_dict(rate: dict) -> dict:
    """Serialize a RATE trace result for JSON."""
    return {
        'problem_id': rate.get('problem_id', ''),
        'converged': rate.get('converged', False),
        'fixed_point_delta': rate.get('fixed_point_delta', 0.0),
        'convergence_depth': rate.get('convergence_depth', 0),
        'topology_emerged': rate.get('topology_emerged', False),
        'rate_defect': rate.get('rate_defect', 0.0),
    }


def generate_meta_lens_report(atlas: dict, filepath: str):
    """Generate a Markdown meta-lens report from atlas results."""
    lines = [
        '# Meta-Lens Atlas Report',
        f'Generated: {datetime.now().isoformat()}',
        f'Problems analyzed: {len(atlas)}',
        '',
        '## SSA Trilemma Summary',
        '',
        '| Problem | C1 | C2 | C3 | Breaking | Interpretation |',
        '|---------|----|----|----|---------|-|',
    ]
    for pid in sorted(atlas.keys()):
        ssa = atlas[pid].get('ssa', {})
        c1 = 'OK' if ssa.get('c1', True) else 'BREAK'
        c2 = 'OK' if ssa.get('c2', True) else 'BREAK'
        c3 = 'OK' if ssa.get('c3', True) else 'BREAK'
        brk = ssa.get('breaking', '?')
        interp = ssa.get('interpretation', '')[:60]
        lines.append(f'| {pid} | {c1} | {c2} | {c3} | {brk} | {interp} |')

    lines += [
        '',
        '## Russell Classification Summary',
        '',
        '| Problem | delta_R | delta_std | Classification | TIG Signature |',
        '|---------|---------|-----------|---------------|--|',
    ]
    for pid in sorted(atlas.keys()):
        r = atlas[pid].get('russell', {})
        dr = r.get('delta_russell', 0.0)
        ds = r.get('delta_standard', 0.0)
        cls = r.get('classification', '?')
        sig = r.get('tig_signature', [])
        lines.append(f'| {pid} | {dr:.4f} | {ds:.4f} | {cls} | {sig} |')

    lines.append('')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return filepath


# ================================================================
#  JOURNAL CLASS
# ================================================================

class SpectrometerJournal:
    """Convenience wrapper for persisting Delta-Spectrometer results.

    Creates and manages the structured directory layout:
      {base_dir}/spec/   -> spectrometer_schema.json
      {base_dir}/runs/   -> per-scan JSON + Markdown
      {base_dir}/docs/   -> stability_matrix.md, summary.md

    Usage:
        journal = SpectrometerJournal('spectrometer_results')
        journal.record(result)
        journal.record_all(results)
        journal.record_matrix(matrix_results)
        journal.write_schema()
    """

    def __init__(self, base_dir: str = 'spectrometer_results'):
        self.base_dir = base_dir
        self.spec_dir = os.path.join(base_dir, 'spec')
        self.runs_dir = os.path.join(base_dir, 'runs')
        self.docs_dir = os.path.join(base_dir, 'docs')

        # Create directory structure
        os.makedirs(self.spec_dir, exist_ok=True)
        os.makedirs(self.runs_dir, exist_ok=True)
        os.makedirs(self.docs_dir, exist_ok=True)

    def record(self, result):
        """Record a single SpectrometerResult (JSON + Markdown) to runs/.

        Returns:
            Tuple of (json_path, md_path).
        """
        json_path = save_result_json(result, self.runs_dir)
        md_path = save_result_markdown(result, self.runs_dir)
        return json_path, md_path

    def record_all(self, results: list):
        """Record every result to runs/, then generate summary to docs/.

        Args:
            results: List of SpectrometerResult objects.

        Returns:
            Path to summary report.
        """
        for r in results:
            self.record(r)

        summary_path = os.path.join(self.docs_dir, 'summary.md')
        generate_summary_report(results, summary_path)
        return summary_path

    def record_flows(self, flows: dict):
        """Record Sanders Flow results.

        Saves each flow as JSON to runs/, then generates the flow
        report to docs/sanders_flow.md.

        Args:
            flows: Dict mapping problem_id -> FlowResult

        Returns:
            Path to flow report.
        """
        for pid, flow in flows.items():
            save_flow_json(flow, self.runs_dir)

        flow_path = os.path.join(self.docs_dir, 'sanders_flow.md')
        generate_flow_report(flows, flow_path)
        return flow_path

    def record_atlas(self, atlas: dict):
        """Record the Fractal Coherence Atlas.

        Saves each fingerprint as JSON to runs/, generates the atlas
        report to docs/fractal_atlas.md, and writes the manifest to
        spec/fractal_atlas_manifest.json.

        Args:
            atlas: Dict mapping key -> FractalFingerprint

        Returns:
            Path to atlas report.
        """
        for key, fp in atlas.items():
            save_fingerprint_json(fp, self.runs_dir)

        atlas_path = os.path.join(self.docs_dir, 'fractal_atlas.md')
        generate_atlas_report(atlas, atlas_path)

        manifest_path = os.path.join(
            self.spec_dir, 'fractal_atlas_manifest.json')
        generate_atlas_manifest(atlas, manifest_path)

        return atlas_path

    def record_attack(self, results: dict):
        """Record Sanders Attack results.

        Saves each attack result as JSON to runs/, generates the attack
        report to docs/sanders_attack.md.

        Args:
            results: Dict mapping key -> SandersAttackResult

        Returns:
            Path to attack report.
        """
        for key, ar in results.items():
            save_attack_json(ar, self.runs_dir)

        attack_path = os.path.join(self.docs_dir, 'sanders_attack.md')
        generate_attack_report(results, attack_path)
        return attack_path

    def record_matrix(self, results: list):
        """Record the 108-run stability matrix.

        Saves each result to runs/, then generates the matrix report
        to docs/stability_matrix.md.

        Args:
            results: List of 108 SpectrometerResult objects.

        Returns:
            Path to stability matrix report.
        """
        for r in results:
            self.record(r)

        matrix_path = os.path.join(self.docs_dir, 'stability_matrix.md')
        generate_matrix_report(results, matrix_path)
        return matrix_path

    def record_robustness(self, results: dict):
        """Record robustness/ablation sweep results.

        Saves each RobustnessResult as JSON to runs/, generates the
        robustness report to docs/robustness.md.

        Args:
            results: Dict mapping key -> RobustnessResult

        Returns:
            Path to robustness report.
        """
        for key, rr in results.items():
            save_robustness_json(rr, self.runs_dir)

        rob_path = os.path.join(self.docs_dir, 'robustness.md')
        generate_robustness_report(results, rob_path)
        return rob_path

    def record_equations(self, equations: dict):
        """Record governing equations.

        Saves each GoverningEquation as JSON to runs/, generates the
        equation report to docs/governing_equations.md.

        Args:
            equations: Dict mapping key -> GoverningEquation

        Returns:
            Path to equation report.
        """
        for key, eq in equations.items():
            save_equation_json(eq, self.runs_dir)

        eq_path = os.path.join(self.docs_dir, 'governing_equations.md')
        generate_equation_report(equations, eq_path)
        return eq_path

    def write_schema(self):
        """Generate the spectrometer schema to spec/spectrometer_schema.json.

        Returns:
            Path to schema file.
        """
        schema_path = os.path.join(self.spec_dir, 'spectrometer_schema.json')
        generate_spec_schema(schema_path)
        return schema_path

    def record_meta_lens(self, atlas: dict):
        """Record meta-lens atlas results (topology + russell + ssa).

        Saves individual JSON per problem + summary report.
        """
        meta_dir = os.path.join(self.base_dir, 'meta_lens')
        os.makedirs(meta_dir, exist_ok=True)

        for pid, data in atlas.items():
            entry = {
                'problem_id': pid,
                'topology': topology_to_dict(data.get('topology', {})),
                'russell': russell_to_dict(data.get('russell', {})),
                'ssa': ssa_to_dict(data.get('ssa', {})),
                'siga': data.get('siga', {}),
            }
            path = os.path.join(meta_dir, f'{pid}_meta_lens.json')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(entry, f, indent=2)

        # Generate report
        report_path = os.path.join(self.docs_dir, 'meta_lens_report.md')
        generate_meta_lens_report(atlas, report_path)
        return meta_dir

    def record_breath(self, breath_data: dict):
        """Record breath-defect flow analysis results.

        Accepts either:
        - A breath atlas dict (with 'estimates' and 'summary' keys)
        - A flat dict of per-problem breath results
        """
        breath_dir = os.path.join(self.base_dir, 'breath')
        os.makedirs(breath_dir, exist_ok=True)

        # Handle atlas format vs flat format
        if 'estimates' in breath_data:
            estimates = breath_data['estimates']
            summary = breath_data.get('summary', {})
        else:
            estimates = breath_data
            summary = {}

        for pid, data in estimates.items():
            path = os.path.join(breath_dir, f'{pid}_breath.json')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

        # Summary
        if summary:
            path = os.path.join(breath_dir, 'breath_summary.json')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)

        return breath_dir
