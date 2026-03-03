"""
ck_clay_journal.py -- Structured Persistence for Clay SDV Protocol
==================================================================
Operator: RESET (9) -- Record, then begin again.

Persists ProbeResults as:
  - JSON  (machine-readable, full data)
  - CSV   (tabular, per-level metrics)
  - Markdown (human-readable report)

All output is deterministic: same seed + same probe = identical files.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

from ck_sim.being.ck_tig_bundle import OP_NAMES, NUM_OPS, DUAL_LENSES, AGENT_BRIEFS


# ================================================================
#  JSON SERIALIZATION
# ================================================================

def probe_result_to_dict(result) -> dict:
    """Convert a ProbeResult to a JSON-serializable dict."""
    steps = []
    for s in result.steps:
        steps.append({
            'level': s.level,
            'operator': s.operator,
            'operator_name': s.operator_name,
            'force_vector': s.force_vector,
            'd2_vector': s.d2_vector,
            'd2_magnitude': s.d2_magnitude,
            'master_lemma_defect': s.master_lemma_defect,
            'lens_mismatch': s.lens_mismatch,
            'coherence_action': s.coherence_action,
            'coherence_band': s.coherence_band,
            'collapse_distance': s.collapse_distance,
            'step_hash': s.step_hash,
        })

    return {
        'problem_id': result.problem_id,
        'test_case': result.test_case,
        'seed': result.seed,
        'n_levels': result.n_levels,
        'tig_path': result.tig_path,
        'steps': steps,
        'operator_counts': {str(k): v for k, v in result.operator_counts.items()},
        'operator_distribution': result.operator_distribution,
        'harmony_fraction': result.harmony_fraction,
        'defect_trajectory': result.defect_trajectory,
        'action_trajectory': result.action_trajectory,
        'defect_trend': result.defect_trend,
        'final_defect': result.final_defect,
        'final_action': result.final_action,
        'defect_slope': result.defect_slope,
        'defect_converges': result.defect_converges,
        'defect_bounded_below': result.defect_bounded_below,
        'spine_defect_3': result.spine_defect_3,
        'spine_defect_6': result.spine_defect_6,
        'spine_defect_9': result.spine_defect_9,
        'spine_fraction': result.spine_fraction,
        'tig_path_fidelity': result.tig_path_fidelity,
        'tig_path_actual': result.tig_path_actual,
        'harmony_defect_series': result.harmony_defect_series,
        'harmony_locked': result.harmony_locked,
        'operator_7_state': result.operator_7_state,
        'operator_9_state': result.operator_9_state,
        'decision_verdict': result.decision_verdict,
        'commutator_persistence': result.commutator_persistence,
        'complexity_persists': result.complexity_persists,
        'sca_completed': result.sca_completed,
        'sca_progress': result.sca_progress,
        'sca_stage': result.sca_stage,
        'vortex_fingerprint': result.vortex_fingerprint,
        'master_lemma_defects': result.master_lemma_defects,
        'final_master_lemma_defect': result.final_master_lemma_defect,
        'lens_mismatches': result.lens_mismatches,
        'dual_fixed_point_proximity': result.dual_fixed_point_proximity,
        'problem_class': result.problem_class,
        'measurement_verdict': result.measurement_verdict,
        'anomaly_count': result.anomaly_count,
        'halted': result.halted,
        'final_hash': result.final_hash,
        'brief_confidence': result.brief_confidence,
        'brief_confidence_target': result.brief_confidence_target,
        'brief_key_joint': result.brief_key_joint,
        'brief_track': result.brief_track,
    }


def save_json(result, path: str):
    """Save a single ProbeResult to JSON."""
    data = probe_result_to_dict(result)
    data['_timestamp'] = datetime.now().isoformat()
    data['_version'] = 'clay_sdv_1.0'
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def save_all_json(results: Dict, path: str):
    """Save all ProbeResults (dict keyed by problem_id) to JSON."""
    data = {
        '_timestamp': datetime.now().isoformat(),
        '_version': 'clay_sdv_1.0',
        'problems': {pid: probe_result_to_dict(r) for pid, r in results.items()},
    }
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


# ================================================================
#  CSV OUTPUT
# ================================================================

def save_csv(result, path: str):
    """Save per-level metrics as CSV."""
    headers = [
        'level', 'operator', 'operator_name',
        'aperture', 'pressure', 'depth', 'binding', 'continuity',
        'd2_magnitude', 'master_lemma_defect', 'lens_mismatch',
        'coherence_action', 'coherence_band', 'collapse_distance',
        'step_hash',
    ]
    lines = [','.join(headers)]

    for s in result.steps:
        fv = s.force_vector if len(s.force_vector) == 5 else [0.0] * 5
        row = [
            str(s.level), str(s.operator), s.operator_name,
            f'{fv[0]:.6f}', f'{fv[1]:.6f}', f'{fv[2]:.6f}',
            f'{fv[3]:.6f}', f'{fv[4]:.6f}',
            f'{s.d2_magnitude:.6f}', f'{s.master_lemma_defect:.6f}',
            f'{s.lens_mismatch:.6f}',
            f'{s.coherence_action:.6f}', s.coherence_band,
            f'{s.collapse_distance:.6f}',
            s.step_hash,
        ]
        lines.append(','.join(row))

    with open(path, 'w') as f:
        f.write('\n'.join(lines) + '\n')


# ================================================================
#  MARKDOWN REPORT
# ================================================================

def generate_report(result, include_steps: bool = True) -> str:
    """Generate a Markdown report for a single probe."""
    lines = []
    pid = result.problem_id
    lens_info = DUAL_LENSES.get(pid, {})

    lines.append(f'# SDV Probe Report: {pid.replace("_", " ").title()}')
    lines.append('')
    lines.append(f'**Problem class**: {result.problem_class}')
    lines.append(f'**Test case**: {result.test_case}')
    lines.append(f'**Seed**: {result.seed}')
    lines.append(f'**Levels**: {result.n_levels}')
    lines.append(f'**Hash**: `{result.final_hash}`')
    lines.append('')

    # Dual lens
    lines.append('## Dual Lens')
    lines.append(f'- **Lens A**: {lens_info.get("lens_a", "N/A")}')
    lines.append(f'- **Lens B**: {lens_info.get("lens_b", "N/A")}')
    lines.append(f'- **Generator**: {lens_info.get("generator", "N/A")}')
    lines.append(f'- **Dual**: {lens_info.get("dual", "N/A")}')
    lines.append('')

    # Verdict
    lines.append('## Measurement Verdict')
    lines.append(f'- **Verdict**: {result.measurement_verdict}')
    lines.append(f'- **Decision**: op7={result.operator_7_state}, op9={result.operator_9_state} -> {result.decision_verdict}')
    lines.append(f'- **Final defect**: {result.final_defect:.6f}')
    lines.append(f'- **Final action**: {result.final_action:.6f}')
    lines.append(f'- **Defect trend**: {result.defect_trend} (slope={result.defect_slope:.6f})')
    lines.append(f'- **Converges**: {result.defect_converges}')
    lines.append(f'- **Bounded below**: {result.defect_bounded_below}')
    lines.append('')

    # Operators
    lines.append('## Operator Distribution')
    for i, frac in enumerate(result.operator_distribution):
        if frac > 0:
            bar = '#' * int(frac * 40)
            lines.append(f'  {OP_NAMES[i]:10s} {frac:.3f} {bar}')
    lines.append(f'  **Harmony fraction**: {result.harmony_fraction:.3f}')
    lines.append('')

    # Spine
    lines.append('## 3-6-9 Spine')
    lines.append(f'- Spine fraction: {result.spine_fraction:.3f}')
    lines.append(f'- Sheath-3 defect: {result.spine_defect_3:.6f}')
    lines.append(f'- Sheath-6 defect: {result.spine_defect_6:.6f}')
    lines.append(f'- Anchor-9 defect: {result.spine_defect_9:.6f}')
    lines.append('')

    # TIG path
    lines.append('## TIG Path')
    expected = ' -> '.join(OP_NAMES[o] for o in result.tig_path)
    actual = ' -> '.join(OP_NAMES[o] for o in result.tig_path_actual
                         if 0 <= o < NUM_OPS)
    lines.append(f'- Expected: {expected}')
    lines.append(f'- Actual:   {actual}')
    lines.append(f'- Fidelity: {result.tig_path_fidelity:.3f}')
    lines.append('')

    # SCA loop
    lines.append('## SCA Loop (1->2->9->1)')
    lines.append(f'- Completed: {result.sca_completed}')
    lines.append(f'- Progress: {result.sca_progress:.2f}')
    lines.append(f'- Stage: {result.sca_stage}')
    lines.append('')

    # Commutators
    lines.append('## Commutator Persistence')
    lines.append(f'- Persistence: {result.commutator_persistence:.3f}')
    lines.append(f'- Complexity persists: {result.complexity_persists}')
    lines.append('')

    # Topology
    lines.append('## Vortex Topology')
    for k, v in result.vortex_fingerprint.items():
        lines.append(f'- {k}: {v}')
    lines.append('')

    # Master Lemma
    lines.append('## Master Lemma Defect')
    lines.append(f'- Final: {result.final_master_lemma_defect:.6f}')
    lines.append(f'- Dual fixed-point proximity: {result.dual_fixed_point_proximity:.6f}')
    lines.append('')

    # Agent Brief v2.0
    if result.brief_confidence > 0:
        brief = AGENT_BRIEFS.get(pid, {})
        lines.append('## Agent Brief v2.0')
        lines.append(f'- **Track**: {result.brief_track}')
        lines.append(f'- **Confidence**: {result.brief_confidence:.0%} -> {result.brief_confidence_target:.0%} target')
        lines.append(f'- **Key Joint**: {result.brief_key_joint}')
        if brief:
            lines.append(f'- **Lemma**: {brief.get("lemma_name", "N/A")}')
            lines.append(f'- **Objective**: {brief.get("objective", "N/A")}')
            lines.append(f'- **Success Criterion**: {brief.get("success", "N/A")}')
            tasks = brief.get('tasks', {})
            if tasks:
                lines.append('- **Research Tasks**:')
                for tid, desc in tasks.items():
                    lines.append(f'  - {tid}: {desc}')
        lines.append('')

    # Safety
    lines.append('## Safety')
    lines.append(f'- Anomalies: {result.anomaly_count}')
    lines.append(f'- Halted: {result.halted}')
    lines.append('')

    # Per-level table
    if include_steps and result.steps:
        lines.append('## Per-Level Data')
        lines.append('')
        lines.append('| Level | Operator | Defect | Action | Band | D2 Mag | Hash |')
        lines.append('|-------|----------|--------|--------|------|--------|------|')
        for s in result.steps:
            lines.append(
                f'| {s.level} | {s.operator_name} | {s.master_lemma_defect:.4f} | '
                f'{s.coherence_action:.4f} | {s.coherence_band} | '
                f'{s.d2_magnitude:.4f} | `{s.step_hash[:8]}` |'
            )
        lines.append('')

    return '\n'.join(lines)


def save_report(result, path: str, include_steps: bool = True):
    """Save Markdown report to file."""
    report = generate_report(result, include_steps)
    with open(path, 'w') as f:
        f.write(report)


def save_cross_problem_report(results: Dict, summary: dict, path: str):
    """Save cross-problem comparison report."""
    lines = []
    lines.append('# SDV Cross-Problem Comparison Report')
    lines.append('')
    lines.append(f'**Date**: {datetime.now().isoformat()}')
    lines.append(f'**Problems**: {len(results)}')
    lines.append('')

    # Summary table
    lines.append('## Summary')
    lines.append('')
    lines.append('| Problem | Class | Verdict | Defect | Harmony | Trend | Confidence | Track |')
    lines.append('|---------|-------|---------|--------|---------|-------|------------|-------|')
    for pid, info in summary.get('problems', {}).items():
        conf = info.get('brief_confidence', 0)
        conf_str = f'{conf:.0%}' if conf > 0 else 'N/A'
        track = info.get('brief_track', '')
        lines.append(
            f'| {pid} | {info["problem_class"]} | {info["verdict"]} | '
            f'{info["final_defect"]:.4f} | {info["harmony_fraction"]:.3f} | '
            f'{info["defect_trend"]} | {conf_str} | {track} |'
        )
    lines.append('')

    # Classification
    lines.append('## Problem Classification')
    lines.append(f'- **Affirmative** (delta->0 supports conjecture): {summary.get("affirmative_results", [])}')
    lines.append(f'- **Gap** (delta>=eta supports gap): {summary.get("gap_results", [])}')
    lines.append(f'- **Converging**: {summary.get("converging", [])}')
    lines.append(f'- **Persistent defect**: {summary.get("persistent_defect", [])}')
    lines.append('')

    # Individual summaries
    for pid, r in results.items():
        lines.append(f'## {pid.replace("_", " ").title()}')
        lines.append(f'- Verdict: {r.measurement_verdict}')
        lines.append(f'- Decision: {r.decision_verdict}')
        lines.append(f'- Defect: {r.final_defect:.6f} (trend: {r.defect_trend})')
        lines.append(f'- Topology: {r.vortex_fingerprint.get("vortex_class", "N/A")}')
        if r.brief_confidence > 0:
            lines.append(f'- Brief: {r.brief_confidence:.0%} confidence ({r.brief_key_joint})')
        lines.append('')

    with open(path, 'w') as f:
        f.write('\n'.join(lines))


# ================================================================
#  JOURNAL CLASS (convenience wrapper)
# ================================================================

class ClayJournal:
    """Convenience wrapper for persisting Clay SDV results.

    Usage:
        journal = ClayJournal('output/clay_results')
        journal.record(result)
        journal.record_all(results, summary)
    """

    def __init__(self, output_dir: str = 'clay_results'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def record(self, result, prefix: str = ''):
        """Record a single probe result (JSON + CSV + Markdown)."""
        tag = prefix or result.problem_id
        base = os.path.join(self.output_dir, f'{tag}_seed{result.seed}')

        save_json(result, f'{base}.json')
        save_csv(result, f'{base}.csv')
        save_report(result, f'{base}.md')

        return base

    def record_all(self, results: Dict, summary: Optional[dict] = None):
        """Record all probe results + cross-problem report."""
        # Individual results
        for pid, r in results.items():
            self.record(r)

        # Combined JSON
        combined_path = os.path.join(self.output_dir, 'all_results.json')
        save_all_json(results, combined_path)

        # Cross-problem report
        if summary is not None:
            report_path = os.path.join(self.output_dir, 'cross_problem_report.md')
            save_cross_problem_report(results, summary, report_path)

        return self.output_dir
