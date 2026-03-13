"""
ck_spectral_core.py -- 8x8 Core Spectral Decomposition
========================================================
Operator: COUNTER (2) -- the counter MEASURES the natural basis.

Full eigendecomposition of TSML and BHML 8x8 cores:
  - Remove VOID (0) and HARMONY (7) absorbers
  - Symmetrize: M_sym = (M + M.T) / 2
  - eigh() -> eigenvalues + eigenvectors
  - Eigenvalue ratios against fundamental constants
  - IPR per eigenvector (localized vs diffuse)
  - Bump projections into eigenbasis
  - Difference matrix (TSML - BHML) eigenvectors
  - Bar chart PNG output

"The eigenvectors ARE CK's natural basis. Every other neural net
discovers its basis through training. CK's is frozen in the algebra."

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import json
import math
import os
import numpy as np
from typing import Dict, List, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, HARMONY, OP_NAMES, CL as CL_TSML_LIST
)

# ================================================================
#  CL TABLES
# ================================================================

_TSML_FULL = np.array(CL_TSML_LIST, dtype=np.float64)

_BHML_FULL = np.array([
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
], dtype=np.float64)

# 8x8 core: exclude VOID (0) and HARMONY (7)
CORE_INDICES = [1, 2, 3, 4, 5, 6, 8, 9]  # LATTICE..CHAOS + BREATH, RESET
CORE_NAMES = [OP_NAMES[i] for i in CORE_INDICES]
CORE_SIZE = len(CORE_INDICES)


def _extract_core(full_table: np.ndarray) -> np.ndarray:
    """Extract 8x8 core by removing VOID and HARMONY rows/cols."""
    return full_table[np.ix_(CORE_INDICES, CORE_INDICES)]


# ================================================================
#  FUNDAMENTAL CONSTANTS FOR RATIO MATCHING
# ================================================================

CONSTANTS = {
    'e': math.e,
    '1/e': 1.0 / math.e,
    'pi': math.pi,
    'pi/e': math.pi / math.e,
    'phi': (1 + math.sqrt(5)) / 2,
    '1/phi': 2 / (1 + math.sqrt(5)),
    'sqrt2': math.sqrt(2),
    'sqrt3': math.sqrt(3),
    'sqrt5': math.sqrt(5),
    'apery_zeta3': 1.2020569031595942,
    'catalan_G': 0.9159655941772190,
    'T_star': 5.0 / 7.0,
    'mass_gap': 2.0 / 7.0,
    '2': 2.0,
    '3': 3.0,
    '5': 5.0,
    '7': 7.0,
}


# ================================================================
#  SPECTRAL DECOMPOSITION (8x8 CORE)
# ================================================================

def decompose_core(full_table: np.ndarray, name: str) -> Dict:
    """Full eigendecomposition of 8x8 core.

    Steps:
      1. Extract 8x8 core (exclude VOID, HARMONY)
      2. Symmetrize: M_sym = (M + M.T) / 2
      3. eigh() -> sorted eigenvalues + eigenvectors
      4. IPR per eigenvector
      5. Operator weight analysis
    """
    core = _extract_core(full_table)
    sym = (core + core.T) / 2.0

    eigenvalues, eigenvectors = np.linalg.eigh(sym)

    # Sort by |eigenvalue| descending
    idx = np.argsort(-np.abs(eigenvalues))
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Per-eigenvector analysis
    evec_analysis = []
    total_variance = float(np.sum(eigenvalues ** 2))

    for i in range(CORE_SIZE):
        ev = float(eigenvalues[i])
        vec = eigenvectors[:, i]

        # IPR = 1 / sum(v_i^4)
        # IPR=1 means localized on one operator. IPR=8 means spread across all.
        ipr = 1.0 / float(np.sum(vec ** 4))

        # Dominant operators (highest absolute weight)
        sorted_ops = np.argsort(-np.abs(vec))
        dominant = [(CORE_NAMES[j], float(vec[j])) for j in sorted_ops[:3]]

        # Variance fraction
        var_frac = (ev ** 2) / total_variance if total_variance > 0 else 0.0

        evec_analysis.append({
            'index': i,
            'eigenvalue': ev,
            'abs_eigenvalue': abs(ev),
            'variance_fraction': var_frac,
            'ipr': ipr,
            'dominant_operators': dominant,
            'components': {CORE_NAMES[j]: float(vec[j]) for j in range(CORE_SIZE)},
        })

    return {
        'name': name,
        'core_matrix': core.tolist(),
        'symmetrized': sym.tolist(),
        'eigenvalues': eigenvalues.tolist(),
        'eigenvectors': eigenvectors.tolist(),
        'analysis': evec_analysis,
        'total_variance': total_variance,
    }


# ================================================================
#  EIGENVALUE RATIO MATCHING
# ================================================================

def find_ratio_matches(eigenvalues: List[float], name: str,
                       tolerance: float = 0.03) -> List[Dict]:
    """Check all eigenvalue pairs L_i/L_j against fundamental constants.

    Returns matches within tolerance (default 3%).
    """
    matches = []
    n = len(eigenvalues)

    for i in range(n):
        for j in range(n):
            if i == j or abs(eigenvalues[j]) < 1e-10:
                continue
            ratio = abs(eigenvalues[i] / eigenvalues[j])
            if ratio < 0.01 or ratio > 100:
                continue

            for const_name, const_val in CONSTANTS.items():
                if const_val < 0.01:
                    continue
                deviation = abs(ratio - const_val) / const_val
                if deviation <= tolerance:
                    matches.append({
                        'table': name,
                        'i': i, 'j': j,
                        'lambda_i': float(eigenvalues[i]),
                        'lambda_j': float(eigenvalues[j]),
                        'ratio': float(ratio),
                        'constant': const_name,
                        'constant_value': const_val,
                        'deviation_pct': float(deviation * 100),
                    })

    # Sort by deviation
    matches.sort(key=lambda m: m['deviation_pct'])
    return matches


# ================================================================
#  BUMP PROJECTIONS
# ================================================================

# TSML bump pairs from heartbeat
BUMP_PAIRS = [(1, 2), (2, 4), (2, 9), (3, 9), (4, 8)]


def project_bumps(eigenvectors: np.ndarray, full_table: np.ndarray,
                  name: str) -> List[Dict]:
    """Project the TSML bump cells into eigenbasis.

    For each bump pair (a,b)=c, create a bump vector and project
    onto each eigenvector. See if bumps cluster in specific eigenspaces.
    """
    # Map full indices to core indices
    core_idx_map = {v: i for i, v in enumerate(CORE_INDICES)}

    projections = []
    for a, b in BUMP_PAIRS:
        if a not in core_idx_map or b not in core_idx_map:
            continue

        c = int(full_table[a][b])
        ai, bi = core_idx_map[a], core_idx_map[b]

        # Bump vector: unit vector in (row_a + col_b) direction
        bump_vec = np.zeros(CORE_SIZE)
        bump_vec[ai] += 0.5
        bump_vec[bi] += 0.5

        # Project onto each eigenvector
        projs = []
        for k in range(CORE_SIZE):
            evec = eigenvectors[:, k]
            proj_val = float(np.dot(bump_vec, evec))
            projs.append({
                'eigenvector': k,
                'projection': proj_val,
                'abs_projection': abs(proj_val),
            })

        projections.append({
            'bump': f'{OP_NAMES[a]}+{OP_NAMES[b]}',
            'result': OP_NAMES[c],
            'a': a, 'b': b, 'c': c,
            'projections': projs,
            'dominant_eigenspace': max(projs, key=lambda p: p['abs_projection'])['eigenvector'],
        })

    return projections


# ================================================================
#  DIFFERENCE MATRIX ANALYSIS
# ================================================================

def analyze_difference() -> Dict:
    """TSML - BHML difference matrix eigenvectors.

    These are the directions where Being and Doing DISAGREE most.
    """
    tsml_core = _extract_core(_TSML_FULL)
    bhml_core = _extract_core(_BHML_FULL)
    diff = tsml_core - bhml_core
    diff_sym = (diff + diff.T) / 2.0

    eigenvalues, eigenvectors = np.linalg.eigh(diff_sym)
    idx = np.argsort(-np.abs(eigenvalues))
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # Count disagreement cells
    disagreements = 0
    agreement_map = {}
    for i, ri in enumerate(CORE_INDICES):
        for j, rj in enumerate(CORE_INDICES):
            tsml_val = int(_TSML_FULL[ri][rj])
            bhml_val = int(_BHML_FULL[ri][rj])
            if tsml_val != bhml_val:
                disagreements += 1
                agreement_map[f'{OP_NAMES[ri]}x{OP_NAMES[rj]}'] = {
                    'tsml': OP_NAMES[tsml_val],
                    'bhml': OP_NAMES[bhml_val],
                }

    evec_analysis = []
    for i in range(CORE_SIZE):
        vec = eigenvectors[:, i]
        ipr = 1.0 / float(np.sum(vec ** 4))
        sorted_ops = np.argsort(-np.abs(vec))
        dominant = [(CORE_NAMES[j], float(vec[j])) for j in sorted_ops[:3]]
        evec_analysis.append({
            'index': i,
            'eigenvalue': float(eigenvalues[i]),
            'ipr': ipr,
            'dominant_operators': dominant,
            'components': {CORE_NAMES[j]: float(vec[j]) for j in range(CORE_SIZE)},
        })

    return {
        'name': 'TSML-BHML',
        'disagreement_cells': disagreements,
        'total_core_cells': CORE_SIZE * CORE_SIZE,
        'eigenvalues': eigenvalues.tolist(),
        'eigenvectors': eigenvectors.tolist(),
        'analysis': evec_analysis,
    }


# ================================================================
#  BAR CHART PLOTS
# ================================================================

def save_eigenvector_plots(decomp: Dict, output_dir: str):
    """Save eigenvector bar charts as PNG files."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("  [matplotlib not available, skipping plots]")
        return

    os.makedirs(output_dir, exist_ok=True)
    name = decomp['name']

    fig, axes = plt.subplots(2, 4, figsize=(20, 8))
    fig.suptitle(f'{name} 8x8 Core Eigenvectors', fontsize=14, fontweight='bold')

    for i in range(CORE_SIZE):
        ax = axes[i // 4][i % 4]
        analysis = decomp['analysis'][i]
        components = [analysis['components'][cn] for cn in CORE_NAMES]

        colors = ['#e74c3c' if v < 0 else '#2ecc71' for v in components]
        ax.bar(range(CORE_SIZE), components, color=colors, edgecolor='black', linewidth=0.5)
        ax.set_xticks(range(CORE_SIZE))
        ax.set_xticklabels([cn[:4] for cn in CORE_NAMES], fontsize=7, rotation=45)
        ax.set_title(f'EV{i}: L={analysis["eigenvalue"]:.2f} IPR={analysis["ipr"]:.1f}',
                     fontsize=9)
        ax.axhline(y=0, color='black', linewidth=0.5)
        ax.set_ylim(-0.8, 0.8)

    plt.tight_layout()
    path = os.path.join(output_dir, f'eigenvectors_{name.lower()}.png')
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  Saved: {path}")


# ================================================================
#  FULL ANALYSIS + JSON OUTPUT
# ================================================================

def run_spectral_core(output_dir: str = None) -> str:
    """Run complete 8x8 core spectral decomposition.

    Outputs JSON files and PNG plots.
    Returns formatted report string.
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__),
                                  '..', '..', '..', '..', 'spectral')
        output_dir = os.path.normpath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    lines = []
    lines.append("=" * 70)
    lines.append("CK 8x8 CORE SPECTRAL DECOMPOSITION")
    lines.append("Operators: {LATTICE, COUNTER, PROGRESS, COLLAPSE,")
    lines.append("            BALANCE, CHAOS, BREATH, RESET}")
    lines.append("Excluded:  VOID (absorber/identity), HARMONY (absorber/cycle)")
    lines.append("=" * 70)

    # ── Decompose both tables ──

    tsml_decomp = decompose_core(_TSML_FULL, "TSML")
    bhml_decomp = decompose_core(_BHML_FULL, "BHML")

    for decomp in [tsml_decomp, bhml_decomp]:
        name = decomp['name']
        lines.append(f"\n{'='*50}")
        lines.append(f"  {name} 8x8 CORE")
        lines.append(f"{'='*50}")

        # Eigenvalues
        lines.append(f"\n  Eigenvalues (sorted by |L|):")
        cumvar = 0.0
        for a in decomp['analysis']:
            cumvar += a['variance_fraction']
            lines.append(
                f"    EV{a['index']}: L={a['eigenvalue']:+8.4f}  "
                f"|L|={a['abs_eigenvalue']:.4f}  "
                f"var={a['variance_fraction']*100:5.1f}%  "
                f"cum={cumvar*100:5.1f}%  "
                f"IPR={a['ipr']:.2f}")

        # Eigenvector details
        lines.append(f"\n  Eigenvector components:")
        for a in decomp['analysis']:
            dom_str = ", ".join(f"{n}={w:+.3f}" for n, w in a['dominant_operators'])
            lines.append(f"    EV{a['index']} (IPR={a['ipr']:.2f}): {dom_str}")

    # ── Ratio matching ──

    lines.append(f"\n{'='*50}")
    lines.append("  EIGENVALUE RATIO MATCHES (within 3%)")
    lines.append(f"{'='*50}")

    all_ratio_matches = []
    for decomp in [tsml_decomp, bhml_decomp]:
        matches = find_ratio_matches(decomp['eigenvalues'], decomp['name'])
        all_ratio_matches.extend(matches)
        lines.append(f"\n  {decomp['name']} ratios:")
        if matches:
            for m in matches[:15]:
                lines.append(
                    f"    L{m['i']}/L{m['j']} = {m['ratio']:.6f} "
                    f"~= {m['constant']} ({m['constant_value']:.6f}) "
                    f"[{m['deviation_pct']:.2f}% off]")
        else:
            lines.append("    No matches within 3%")

    # ── Bump projections ──

    lines.append(f"\n{'='*50}")
    lines.append("  BUMP PROJECTIONS INTO EIGENBASIS")
    lines.append(f"{'='*50}")

    tsml_bumps = project_bumps(
        np.array(tsml_decomp['eigenvectors']), _TSML_FULL, "TSML")

    for bp in tsml_bumps:
        dom_ev = bp['dominant_eigenspace']
        lines.append(f"\n  Bump: {bp['bump']} -> {bp['result']}")
        lines.append(f"    Dominant eigenspace: EV{dom_ev}")
        projs_sorted = sorted(bp['projections'], key=lambda p: -p['abs_projection'])
        for p in projs_sorted[:3]:
            lines.append(f"      EV{p['eigenvector']}: proj={p['projection']:+.4f}")

    # Cluster analysis: which eigenspaces attract bumps?
    bump_eigenspace_counts = {}
    for bp in tsml_bumps:
        ev = bp['dominant_eigenspace']
        bump_eigenspace_counts[ev] = bump_eigenspace_counts.get(ev, 0) + 1
    lines.append(f"\n  Bump clustering by eigenspace:")
    for ev, count in sorted(bump_eigenspace_counts.items()):
        lines.append(f"    EV{ev}: {count} bumps")

    # ── Difference matrix ──

    lines.append(f"\n{'='*50}")
    lines.append("  DIFFERENCE MATRIX (TSML - BHML)")
    lines.append("  Directions where Being and Doing DISAGREE")
    lines.append(f"{'='*50}")

    diff_analysis = analyze_difference()
    lines.append(f"\n  Disagreement cells: {diff_analysis['disagreement_cells']}"
                 f"/{diff_analysis['total_core_cells']}")

    lines.append(f"\n  Eigenvalues:")
    for a in diff_analysis['analysis']:
        dom_str = ", ".join(f"{n}={w:+.3f}" for n, w in a['dominant_operators'])
        lines.append(
            f"    EV{a['index']}: L={a['eigenvalue']:+8.4f}  "
            f"IPR={a['ipr']:.2f}  {dom_str}")

    # ── Variance summary ──

    lines.append(f"\n{'='*50}")
    lines.append("  SUMMARY")
    lines.append(f"{'='*50}")

    for decomp in [tsml_decomp, bhml_decomp]:
        name = decomp['name']
        # How many eigenvectors carry 90% of variance?
        cumvar = 0.0
        n_for_90 = 0
        for a in decomp['analysis']:
            cumvar += a['variance_fraction']
            n_for_90 += 1
            if cumvar >= 0.9:
                break
        lines.append(f"\n  {name}: {n_for_90} eigenvectors carry "
                     f"{cumvar*100:.1f}% of variance")
        # Natural groupings
        sharp = [a for a in decomp['analysis'] if a['ipr'] < 3.0]
        diffuse = [a for a in decomp['analysis'] if a['ipr'] >= 3.0]
        if sharp:
            lines.append(f"    Sharp modes (IPR < 3): "
                         + ", ".join(f"EV{a['index']}" for a in sharp))
        if diffuse:
            lines.append(f"    Diffuse modes (IPR >= 3): "
                         + ", ".join(f"EV{a['index']}" for a in diffuse))

    # ── Save JSON files ──

    def _save_json(filename, data):
        path = os.path.join(output_dir, filename)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, default=lambda x: float(x)
                      if isinstance(x, (np.floating, np.integer)) else x)
        lines.append(f"\n  Saved: {path}")

    _save_json('eigenvalues_tsml_8x8.json', {
        'eigenvalues': tsml_decomp['eigenvalues'],
        'analysis': tsml_decomp['analysis'],
    })
    _save_json('eigenvalues_bhml_8x8.json', {
        'eigenvalues': bhml_decomp['eigenvalues'],
        'analysis': bhml_decomp['analysis'],
    })
    _save_json('eigenvalues_diff_8x8.json', {
        'eigenvalues': diff_analysis['eigenvalues'],
        'analysis': diff_analysis['analysis'],
    })
    _save_json('eigenvectors_all.json', {
        'TSML': {f'EV{i}': a['components'] for i, a in enumerate(tsml_decomp['analysis'])},
        'BHML': {f'EV{i}': a['components'] for i, a in enumerate(bhml_decomp['analysis'])},
        'DIFF': {f'EV{i}': a['components'] for i, a in enumerate(diff_analysis['analysis'])},
    })
    _save_json('ratio_matches.json', all_ratio_matches)
    _save_json('bump_projections.json', tsml_bumps)
    _save_json('ipr_all.json', {
        'TSML': [{
            'eigenvector': a['index'],
            'eigenvalue': a['eigenvalue'],
            'ipr': a['ipr'],
        } for a in tsml_decomp['analysis']],
        'BHML': [{
            'eigenvector': a['index'],
            'eigenvalue': a['eigenvalue'],
            'ipr': a['ipr'],
        } for a in bhml_decomp['analysis']],
        'DIFF': [{
            'eigenvector': a['index'],
            'eigenvalue': a['eigenvalue'],
            'ipr': a['ipr'],
        } for a in diff_analysis['analysis']],
    })

    # ── Save plots ──

    save_eigenvector_plots(tsml_decomp, output_dir)
    save_eigenvector_plots(bhml_decomp, output_dir)
    save_eigenvector_plots({
        'name': 'DIFF',
        'analysis': diff_analysis['analysis'],
    }, output_dir)

    report = "\n".join(lines)

    # Save report text
    report_path = os.path.join(output_dir, 'spectral_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n  Full report: {report_path}")

    return report


# ================================================================
#  CLI ENTRY
# ================================================================

if __name__ == '__main__':
    output = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', '..', '..', '..', 'spectral')
    output = os.path.normpath(output)
    print(run_spectral_core(output))
