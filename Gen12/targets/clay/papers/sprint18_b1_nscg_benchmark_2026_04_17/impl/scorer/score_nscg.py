"""
B1 Scorer + Curve Analyzer
Per B1_NSCG_SPEC_v1.0 §9-§10, §12.5-12.6 and B1_CURVE_ANALYSIS_ADDENDUM_v1.0.

Reads:
    data/    (CSV files)
    sealed/  (truth JSON files)
    results/ (fit JSON files from the fitter)
    manifest/{data_hashes, sealed_hashes}.json

Writes:
    scores/per_config/{config_id}.score.json
    scores/per_config_metrics.json    (one row per config, all metrics)
    scores/B1_summary.json            (overall verdict per spec §12.6)
    scores/curves.json                (aggregated curves per metric)
    scores/curve_consistency.json     (meta-metrics from addendum §3)
    plots/curve_{metric}.png          (>=10 plots)
    B1_CURVE_ANALYSIS.md              (addendum §5.2)
    B1_TOWER_STABILITY_NOTE.md        (addendum §5.3)

Usage:
    python score_nscg.py [--root <dir>]
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import statistics
import sys
from collections import defaultdict
from math import gcd
from pathlib import Path

import numpy as np

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_PLOT = True
except Exception:
    HAVE_PLOT = False

SPEC_VERSION = "B1-v1.0"
ADDENDUM_VERSION = "Addendum-v1.0"

CONFIGS = [
    (100_000, 0.05, "low"),
    (500_000, 0.15, "med"),
    (1_000_000, 0.30, "high"),
]
SEEDS = [0, 1, 2, 3, 4]

PASS_THRESHOLDS = {
    0.05: dict(R=0.90, P=0.75, A_rule=1.00, A_T=0.95),
    0.15: dict(R=0.80, P=0.60, A_rule=0.90, A_T=0.88),
    0.30: dict(R=0.60, P=0.50, A_rule=0.80, A_T=0.75),
}

# Per-noise-level pass: (min_seeds_passing,)
NOISE_LEVEL_MIN_SEEDS = {"low": 5, "med": 4, "high": 3}


# ---------------------------------------------------------------------------
# Hash check
# ---------------------------------------------------------------------------


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Per-config scoring (spec §9)
# ---------------------------------------------------------------------------


def per_config_metrics(truth: dict, fit: dict) -> dict:
    n = truth["config"]["n"]

    # A_h (§9.1)
    A_h = 1 if fit["h_hat"] == truth["h_true"] else 0

    # A_sigma (§9.2)
    sigma_true = {int(k): v for k, v in truth["sigma_true"].items()}
    sigma_hat = {int(k): v for k, v in fit["sigma_hat"].items()}
    units_true = sorted(truth["units_true"])
    # Partition match
    P_true_pairs = set()
    for u, v in [(a, b) for i, a in enumerate(units_true) for b in units_true[i + 1:]]:
        if sigma_true[u] == sigma_true[v]:
            P_true_pairs.add((u, v))
    P_hat_pairs = set()
    units_hat = sorted(fit["units_hat"])
    for u, v in [(a, b) for i, a in enumerate(units_hat) for b in units_hat[i + 1:]]:
        if u in sigma_hat and v in sigma_hat and sigma_hat[u] == sigma_hat[v]:
            P_hat_pairs.add((u, v))
    P_match = 1 if (P_true_pairs == P_hat_pairs and units_hat == units_true) else 0
    # Ordering: lower-shell class is {3, 7} per truth (sigma_true(3)=1 < sigma_true(1)=2)
    if 3 in sigma_hat and 1 in sigma_hat:
        P_order = 1 if sigma_hat[3] < sigma_hat[1] else 0
    else:
        P_order = 0
    A_sigma = P_match * P_order

    # Seam recall/precision/F1 (§9.3)
    S_true = {tuple(p) for p in truth["S_true"]}
    S_hat = {tuple(p) for p in fit["S_hat"]}
    inter = S_hat & S_true
    R_seam = len(inter) / len(S_true) if S_true else 0.0
    P_seam = (len(inter) / len(S_hat)) if S_hat else 1.0
    if R_seam == 0 or P_seam == 0:
        F_seam = 0.0
    else:
        F_seam = 2 * R_seam * P_seam / (R_seam + P_seam)

    # A_rule (§9.4)
    S_MAX_true = {tuple(p) for p in truth["S_MAX_true"]}
    S_ADD_true = {tuple(p) for p in truth["S_ADD_true"]}
    S_MAX_hat = {tuple(p) for p in fit["max_domain_hat"]}
    S_ADD_hat = {tuple(p) for p in fit["add_domain_hat"]}
    correct_rule = 0
    for p in inter:
        true_class = "MAX" if p in S_MAX_true else "ADD"
        hat_class = "MAX" if p in S_MAX_hat else ("ADD" if p in S_ADD_hat else None)
        if hat_class == true_class:
            correct_rule += 1
    A_rule = correct_rule / len(inter) if inter else 0.0

    # A_T (§9.5)
    T_true_mat = truth["T_true_matrix"]
    T_hat_mat = fit["T_hat_matrix"]
    matches = sum(
        1 for x in range(n) for y in range(n) if T_true_mat[x][y] == T_hat_mat[x][y]
    )
    A_T = matches / 100.0

    # Curve addendum §1.1
    h_hat = fit["h_hat"]
    attractor_fraction = sum(
        1 for x in range(n) for y in range(n) if T_hat_mat[x][y] == h_hat
    ) / 100.0
    seam_density = len(S_hat) / 100.0
    if S_hat:
        max_domain_fraction = len(S_MAX_hat) / len(S_hat)
        add_domain_fraction = len(S_ADD_hat) / len(S_hat)
    else:
        max_domain_fraction = 0.0
        add_domain_fraction = 0.0

    # Curve addendum §1.2 — seam topology (undirected, self-loops allowed)
    edges = set()
    self_loops = 0
    for (a, b) in S_hat:
        if a == b:
            self_loops += 1
            edges.add((a, a))
        else:
            edges.add((min(a, b), max(a, b)))
    vertices = set()
    for (a, b) in edges:
        vertices.add(a)
        vertices.add(b)
    seam_edges = len(edges)
    seam_vertices = len(vertices)
    # connected components on vertices, using BFS
    adj = defaultdict(set)
    for (a, b) in edges:
        adj[a].add(b)
        adj[b].add(a)
    visited = set()
    components = 0
    for v in vertices:
        if v in visited:
            continue
        components += 1
        stack = [v]
        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            stack.extend(adj[u] - visited)
    seam_components = components if vertices else 0
    seam_max_degree = max((len(adj[v]) for v in vertices), default=0)
    seam_is_tree = (
        seam_components == 1 and seam_edges == max(seam_vertices - 1, 0)
    )
    seam_is_forest = (
        seam_vertices > 0 and seam_edges == seam_vertices - seam_components
    )
    # diameter (largest component)
    seam_diameter = 0
    if vertices:
        largest_comp = []
        seen2 = set()
        best_size = 0
        for v in vertices:
            if v in seen2:
                continue
            comp = []
            stack = [v]
            while stack:
                u = stack.pop()
                if u in seen2:
                    continue
                seen2.add(u)
                comp.append(u)
                stack.extend(adj[u] - seen2)
            if len(comp) > best_size:
                best_size = len(comp)
                largest_comp = comp
        # BFS shortest paths
        def bfs(src):
            d = {src: 0}
            q = [src]
            while q:
                u = q.pop(0)
                for w in adj[u]:
                    if w not in d:
                        d[w] = d[u] + 1
                        q.append(w)
            return d
        diam = 0
        for v in largest_comp:
            d = bfs(v)
            for w, dist in d.items():
                if dist > diam:
                    diam = dist
        seam_diameter = diam

    # Curve addendum §1.3 — per-layer recovery
    D1 = S_MAX_true
    D2 = S_ADD_true
    D0 = {(x, y) for x in range(n) for y in range(n)} - S_true
    C0_recov = sum(1 for (x, y) in D0 if T_hat_mat[x][y] == T_true_mat[x][y])
    C1_recov = sum(1 for (x, y) in D1 if T_hat_mat[x][y] == T_true_mat[x][y])
    C2_recov = sum(1 for (x, y) in D2 if T_hat_mat[x][y] == T_true_mat[x][y])
    rho_C0 = C0_recov / 92
    rho_C1 = C1_recov / 6
    rho_C2 = C2_recov / 2

    # Curve addendum §1.4 — Hamming
    hamming = sum(
        1 for x in range(n) for y in range(n) if T_hat_mat[x][y] != T_true_mat[x][y]
    )
    norm_hamming = hamming / 100.0

    return {
        "A_h": A_h,
        "A_sigma": A_sigma,
        "R_seam": R_seam,
        "P_seam": P_seam,
        "F_seam": F_seam,
        "A_rule": A_rule,
        "A_T": A_T,
        "attractor_fraction": attractor_fraction,
        "seam_density": seam_density,
        "max_domain_fraction": max_domain_fraction,
        "add_domain_fraction": add_domain_fraction,
        "seam_edges": seam_edges,
        "seam_vertices": seam_vertices,
        "seam_components": seam_components,
        "seam_max_degree": seam_max_degree,
        "seam_is_tree": seam_is_tree,
        "seam_is_forest": seam_is_forest,
        "seam_diameter": seam_diameter,
        "C0_cells_recovered": C0_recov,
        "C1_cells_recovered": C1_recov,
        "C2_cells_recovered": C2_recov,
        "rho_C0": rho_C0,
        "rho_C1": rho_C1,
        "rho_C2": rho_C2,
        "hamming_distance": hamming,
        "normalized_hamming": norm_hamming,
    }


def passes_per_config(p: float, m: dict) -> bool:
    th = PASS_THRESHOLDS[p]
    return (
        m["A_h"] == 1
        and m["A_sigma"] == 1
        and m["R_seam"] >= th["R"]
        and m["P_seam"] >= th["P"]
        and m["A_rule"] >= th["A_rule"]
        and m["A_T"] >= th["A_T"]
    )


# ---------------------------------------------------------------------------
# Z_null (§9.6) — fast surrogate using random T_emp matrices through fitter
# ---------------------------------------------------------------------------


def _v2(n_):
    if n_ == 0:
        return 0
    k = 0
    while n_ % 2 == 0:
        n_ //= 2
        k += 1
    return k


def _C0(x, y, n, h, sigma, core):
    if x == 0 or y == 0:
        if (x, y) in {(0, h), (h, 0)}:
            return h
        return 0
    if x in core and y in core and sigma[x] != sigma[y]:
        return x if sigma[x] < sigma[y] else y
    return h


def _refit_from_T_emp(T_emp_arr: np.ndarray):
    n = T_emp_arr.shape[0]
    units = [u for u in range(n) if gcd(u, n) == 1]
    sigma = {u: _v2(3 * u + 1) for u in units}
    core = [u for u in units if u != 1]
    val_count = np.bincount(T_emp_arr.ravel(), minlength=n)
    h = int(np.argmax(val_count))
    seam_max, seam_add = [], []
    for x in range(n):
        for y in range(n):
            t = int(T_emp_arr[x, y])
            c0 = _C0(x, y, n, h, sigma, core)
            if t == c0:
                continue
            mx = max(x, y)
            ad = (x + y) % n
            if t == mx and t != ad:
                seam_max.append((x, y))
            elif t == ad and t != mx:
                seam_add.append((x, y))
            elif t == mx and t == ad:
                seam_max.append((x, y))
    T_hat = np.zeros_like(T_emp_arr)
    seam_max_set = set(seam_max)
    seam_add_set = set(seam_add)
    for x in range(n):
        for y in range(n):
            if (x, y) in seam_max_set:
                T_hat[x, y] = max(x, y)
            elif (x, y) in seam_add_set:
                T_hat[x, y] = (x + y) % n
            else:
                T_hat[x, y] = _C0(x, y, n, h, sigma, core)
    return T_hat


def z_null(T_true_mat: list[list[int]], A_T: float, K: int = 1000, rng_seed: int = 0):
    """Surrogate null per §9.6: random T_emp uniform in {0..n-1}, refit, A_T."""
    rng = np.random.default_rng(rng_seed)
    n = len(T_true_mat)
    T_true_arr = np.asarray(T_true_mat, dtype=np.int8)
    A_T_null = np.empty(K)
    for k in range(K):
        T_emp = rng.integers(0, n, size=(n, n)).astype(np.int8)
        T_hat = _refit_from_T_emp(T_emp)
        A_T_null[k] = float(np.mean(T_hat == T_true_arr))
    mu = float(A_T_null.mean())
    sd = float(A_T_null.std(ddof=1)) if K > 1 else 0.0
    if sd == 0.0:
        return {"Z_null": float("inf") if A_T > mu else 0.0, "mu_null": mu, "sigma_null": sd}
    return {"Z_null": (A_T - mu) / sd, "mu_null": mu, "sigma_null": sd}


# ---------------------------------------------------------------------------
# Curve consistency (addendum §3)
# ---------------------------------------------------------------------------


def aggregate_curves(per_config_rows: list[dict]) -> dict:
    """Returns {metric: {p_str: {mean, std, min, max}}}."""
    metric_keys = [
        "A_h", "A_sigma",
        "R_seam", "P_seam", "F_seam", "A_rule", "A_T",
        "attractor_fraction", "seam_density",
        "max_domain_fraction", "add_domain_fraction",
        "seam_edges", "seam_vertices", "seam_components", "seam_max_degree",
        "seam_diameter",
        "C0_cells_recovered", "C1_cells_recovered", "C2_cells_recovered",
        "rho_C0", "rho_C1", "rho_C2",
        "hamming_distance", "normalized_hamming",
    ]
    by_p: dict[float, list[dict]] = defaultdict(list)
    for row in per_config_rows:
        by_p[row["p_noise"]].append(row["metrics"])
    out: dict[str, dict[str, dict]] = {}
    for m in metric_keys:
        out[m] = {}
        for p in sorted(by_p):
            vals = [r[m] for r in by_p[p]]
            out[m][f"{p:.2f}"] = {
                "mean": float(statistics.mean(vals)),
                "std": float(statistics.stdev(vals)) if len(vals) > 1 else 0.0,
                "min": float(min(vals)),
                "max": float(max(vals)),
            }
    return out


def monotonicity_decreasing(curve: dict) -> int:
    means = [curve[k]["mean"] for k in sorted(curve)]
    return 1 if all(means[i] >= means[i + 1] for i in range(len(means) - 1)) else 0


def monotonicity_increasing(curve: dict) -> int:
    means = [curve[k]["mean"] for k in sorted(curve)]
    return 1 if all(means[i] <= means[i + 1] for i in range(len(means) - 1)) else 0


def smoothness(curve: dict) -> float:
    keys = sorted(curve)
    p_vals = [float(k) for k in keys]
    means = [curve[k]["mean"] for k in keys]
    if len(p_vals) < 3:
        return 1.0
    s1 = abs(means[1] - means[0]) / (p_vals[1] - p_vals[0])
    s2 = abs(means[2] - means[1]) / (p_vals[2] - p_vals[1])
    if s1 == 0 and s2 == 0:
        return 1.0
    if min(s1, s2) == 0:
        return 0.0
    return min(s1, s2) / max(s1, s2)


def curve_consistency(per_config_rows: list[dict], curves: dict) -> dict:
    # Monotonicity
    decreasing_metrics = [
        "A_T", "R_seam", "P_seam", "F_seam", "rho_C0", "rho_C1", "rho_C2", "A_rule",
    ]
    increasing_metrics = ["seam_density", "hamming_distance"]
    other_metrics = ["attractor_fraction"]  # expected stable
    mono_scores = []
    mono_detail = {}
    for m in decreasing_metrics:
        s = monotonicity_decreasing(curves[m])
        mono_detail[m] = {"expected": "decreasing", "score": s}
        mono_scores.append(s)
    for m in increasing_metrics:
        s = monotonicity_increasing(curves[m])
        mono_detail[m] = {"expected": "increasing", "score": s}
        mono_scores.append(s)
    for m in other_metrics:
        # treat as monotonic if values are nearly constant
        means = [curves[m][k]["mean"] for k in sorted(curves[m])]
        s = 1 if max(means) - min(means) < 0.05 else 0
        mono_detail[m] = {"expected": "stable", "score": s}
        mono_scores.append(s)
    mean_mono = sum(mono_scores) / len(mono_scores)

    # Smoothness on key recovery metrics
    smooth_metrics = ["A_T", "R_seam", "rho_C0", "hamming_distance"]
    smooth_scores = [smoothness(curves[m]) for m in smooth_metrics]
    mean_smooth = sum(smooth_scores) / len(smooth_scores)

    # Attractor persistence
    n_correct_h = sum(1 for r in per_config_rows if r["metrics"]["A_h"] == 1)
    attractor_persistence = n_correct_h / len(per_config_rows)

    # Seam class ratio persistence (true ratio = 6/8 = 0.75)
    sq = []
    for r in per_config_rows:
        seam_card = (
            r["metrics"]["seam_density"] * 100  # |S_hat|
        )
        if seam_card > 0:
            r_p_s = r["metrics"]["max_domain_fraction"]
        else:
            r_p_s = 0.0
        sq.append((r_p_s - 0.75) ** 2)
    rmsd = (sum(sq) / len(sq)) ** 0.5
    ratio_persistence = max(0.0, 1.0 - rmsd)

    # Layer ordering
    n_ordered = sum(
        1 for r in per_config_rows
        if r["metrics"]["rho_C0"] >= r["metrics"]["rho_C1"] >= r["metrics"]["rho_C2"]
    )
    layer_ordering = n_ordered / len(per_config_rows)

    CCS = (
        mean_mono + mean_smooth + attractor_persistence + ratio_persistence + layer_ordering
    ) / 5.0

    if CCS >= 0.85:
        band = "Lawful degradation"
    elif CCS >= 0.60:
        band = "Partially lawful"
    else:
        band = "Unstructured degradation"

    return {
        "monotonicity": {
            "detail": mono_detail,
            "mean": mean_mono,
        },
        "smoothness": {
            "detail": dict(zip(smooth_metrics, smooth_scores)),
            "mean": mean_smooth,
        },
        "attractor_persistence": attractor_persistence,
        "ratio_persistence": ratio_persistence,
        "layer_ordering": layer_ordering,
        "CCS": CCS,
        "band": band,
    }


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------


def make_plots(per_config_rows: list[dict], curves: dict, plots_dir: Path) -> list[str]:
    if not HAVE_PLOT:
        return []
    plots_dir.mkdir(parents=True, exist_ok=True)
    plot_metrics = [
        "A_T", "R_seam", "P_seam", "F_seam", "A_rule",
        "rho_C0", "rho_C1", "rho_C2",
        "attractor_fraction", "seam_density",
        "seam_edges", "hamming_distance",
    ]
    by_p: dict[float, list[dict]] = defaultdict(list)
    for row in per_config_rows:
        by_p[row["p_noise"]].append(row["metrics"])
    p_vals = sorted(by_p)
    written = []
    for m in plot_metrics:
        means = [curves[m][f"{p:.2f}"]["mean"] for p in p_vals]
        mins = [curves[m][f"{p:.2f}"]["min"] for p in p_vals]
        maxs = [curves[m][f"{p:.2f}"]["max"] for p in p_vals]
        fig, ax = plt.subplots(figsize=(5, 3.5))
        ax.errorbar(
            p_vals, means,
            yerr=[[means[i] - mins[i] for i in range(len(p_vals))],
                  [maxs[i] - means[i] for i in range(len(p_vals))]],
            fmt="o-", capsize=4, color="#1f3b73",
        )
        ax.set_xlabel("p_noise")
        ax.set_ylabel(m)
        ax.set_title(f"B1 curve: {m}")
        ax.grid(True, alpha=0.3)
        out = plots_dir / f"curve_{m}.png"
        fig.tight_layout()
        fig.savefig(out, dpi=120)
        plt.close(fig)
        written.append(str(out.name))
    return written


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------


def write_curve_analysis_md(
    out_path: Path,
    summary: dict,
    curves: dict,
    consistency: dict,
    plot_files: list[str],
    fitter_name: str,
    fitter_version: str,
) -> None:
    rep = []
    rep.append("# B1 Curve Analysis")
    rep.append("")
    rep.append(f"**Spec version:** {SPEC_VERSION} + {ADDENDUM_VERSION}")
    rep.append(f"**Run timestamp:** {summary['run_timestamp']}")
    rep.append(f"**Fitter:** `{fitter_name}` v{fitter_version}")
    rep.append(f"**Overall B1 verdict (per core spec):** **{summary['overall']['verdict']}**")
    rep.append("")
    rep.append("---")
    rep.append("")
    rep.append("## Curve Tables")
    rep.append("")
    plot_metrics = [
        "A_T", "R_seam", "P_seam", "F_seam", "A_rule",
        "rho_C0", "rho_C1", "rho_C2",
        "attractor_fraction", "seam_density",
        "seam_edges", "hamming_distance",
    ]
    for m in plot_metrics:
        rep.append(f"### {m}")
        rep.append("")
        rep.append("| p_noise | mean | std | min | max |")
        rep.append("|---|---|---|---|---|")
        for p_str in sorted(curves[m]):
            r = curves[m][p_str]
            rep.append(
                f"| {p_str} | {r['mean']:.4f} | {r['std']:.4f} | {r['min']:.4f} | {r['max']:.4f} |"
            )
        rep.append("")
    rep.append("---")
    rep.append("")
    rep.append("## Plots")
    rep.append("")
    for pf in plot_files:
        rep.append(f"![{pf}](plots/{pf})")
    rep.append("")
    rep.append("---")
    rep.append("")
    rep.append("## Meta-Metrics (Addendum §3)")
    rep.append("")
    rep.append("| Meta-metric | Value | Interpretation |")
    rep.append("|---|---|---|")
    rep.append(
        f"| Mean monotonicity | {consistency['monotonicity']['mean']:.3f} | "
        f"fraction of metrics monotone in expected direction |"
    )
    rep.append(
        f"| Mean smoothness   | {consistency['smoothness']['mean']:.3f} | "
        f"slope-ratio across A_T, R_seam, rho_C0, hamming (>=0.30 acceptable) |"
    )
    rep.append(
        f"| Attractor persistence | {consistency['attractor_persistence']:.3f} | "
        f"fraction of 15 configs with h_hat = 7 |"
    )
    rep.append(
        f"| Ratio persistence | {consistency['ratio_persistence']:.3f} | "
        f"1 - RMSD of MAX/seam ratio from true 0.75 (>=0.8 lawful) |"
    )
    rep.append(
        f"| Layer ordering    | {consistency['layer_ordering']:.3f} | "
        f"fraction with rho_C0 >= rho_C1 >= rho_C2 |"
    )
    rep.append(f"| **CCS**           | **{consistency['CCS']:.3f}** | **{consistency['band']}** |")
    rep.append("")
    rep.append("---")
    rep.append("")
    rep.append("## Lawfulness Paragraph")
    rep.append("")
    cs = consistency
    para = (
        f"The instrument's degradation under increasing noise scores "
        f"CCS = {cs['CCS']:.3f}, placing it in the **{cs['band']}** band. "
        f"Mean monotonicity is {cs['monotonicity']['mean']:.3f} "
        f"and mean smoothness across (A_T, R_seam, rho_C0, hamming) is "
        f"{cs['smoothness']['mean']:.3f}. "
        f"The attractor h = 7 is recovered in "
        f"{int(cs['attractor_persistence'] * 15)} of 15 configurations. "
        f"The MAX/seam class ratio holds at {cs['ratio_persistence']:.3f} "
        f"(true ratio 0.75; persistence = 1 - RMSD). "
        f"Layer ordering rho_C0 >= rho_C1 >= rho_C2 holds in "
        f"{int(cs['layer_ordering'] * 15)} of 15 configurations."
    )
    rep.append(para)
    rep.append("")
    if cs["CCS"] < 0.85:
        rep.append("---")
        rep.append("")
        rep.append("## Divergence from Ground Truth")
        rep.append("")
        rep.append(
            f"CCS = {cs['CCS']:.3f} < 0.85. Specific shortfalls:"
        )
        if cs["monotonicity"]["mean"] < 1.0:
            failed = [
                k for k, v in cs["monotonicity"]["detail"].items() if v["score"] == 0
            ]
            rep.append(f"- **Monotonicity violations:** {failed}")
        if cs["smoothness"]["mean"] < 0.30:
            rep.append(
                f"- **Smoothness below 0.30:** mean = {cs['smoothness']['mean']:.3f} -> kinked/bifurcating"
            )
        if cs["attractor_persistence"] < 1.0:
            rep.append(
                f"- **Attractor persistence:** {cs['attractor_persistence']:.3f} (some seeds lost h=7)"
            )
        if cs["ratio_persistence"] < 0.8:
            rep.append(
                f"- **Ratio persistence:** {cs['ratio_persistence']:.3f} -> layer mixing under noise"
            )
        if cs["layer_ordering"] < 1.0:
            rep.append(
                f"- **Layer ordering violations:** {int((1 - cs['layer_ordering']) * 15)} configs"
            )
        rep.append("")
    rep.append("---")
    rep.append("")
    rep.append("## Note on Independence from Pass/Fail")
    rep.append("")
    rep.append(
        "The curve analysis is diagnostic and does **NOT** alter the B1 pass/fail verdict. "
        "The verdict above is taken from the core spec scorer (B1-v1.0 §10)."
    )
    rep.append("")
    out_path.write_text("\n".join(rep), encoding="utf-8")


def write_tower_stability_note(
    out_path: Path,
    summary: dict,
    consistency: dict,
) -> None:
    cs = consistency
    structurally_coherent = (
        cs["CCS"] >= 0.85
        and cs["attractor_persistence"] == 1.0
        and cs["layer_ordering"] >= 0.8
    )
    if cs["CCS"] >= 0.85 and summary["overall"]["verdict"] == "PASS":
        rec = "Proceed to B2 (Wobble-Reset Generator)."
    elif cs["CCS"] >= 0.85 and summary["overall"]["verdict"] == "FAIL":
        rec = (
            "Diagnose noise-limited recovery (lawful curve, failed pointwise). "
            "Consider larger N at the failing noise level before B2."
        )
    elif summary["overall"]["verdict"] == "PASS":
        rec = (
            "Proceed to B2, but flag unstructured degradation (pass + low CCS) "
            "as a possible memorization signal in subsequent benchmarks."
        )
    else:
        rec = "Diagnose: structural defect in the fitter. Do NOT proceed to B2."

    lines = [
        "# B1 Tower Stability Note",
        "",
        f"**Spec version:** {SPEC_VERSION} + {ADDENDUM_VERSION}",
        f"**Run timestamp:** {summary['run_timestamp']}",
        f"**Overall B1 verdict (per core spec):** **{summary['overall']['verdict']}**",
        "",
        f"**CCS:** {cs['CCS']:.3f} ({cs['band']})",
        "",
        "## Preserved meta-metrics",
        "",
    ]
    for k in ("monotonicity", "smoothness", "attractor_persistence", "ratio_persistence", "layer_ordering"):
        v = cs[k]
        if isinstance(v, dict):
            v = v["mean"]
        lines.append(f"- **{k}:** {v:.3f}")
    lines.append("")
    lines.append("## Structural coherence judgement")
    lines.append("")
    lines.append(
        f"Per Addendum §4.1, the instrument is "
        f"**{'structurally coherent' if structurally_coherent else 'NOT yet structurally coherent'}** "
        f"(criteria: CCS >= 0.85, attractor persistence = 1.0, layer ordering >= 0.8)."
    )
    lines.append("")
    lines.append("## Independence from pass/fail")
    lines.append("")
    lines.append(
        "Curve metrics are diagnostic. The B1 pass/fail verdict above is set by the core spec, "
        "not by CCS."
    )
    lines.append("")
    lines.append("## Recommendation for next step")
    lines.append("")
    lines.append(rec)
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None)
    ap.add_argument("--znull-K", type=int, default=200, help="null samples per config")
    args = ap.parse_args()

    if args.root is None:
        root = Path(__file__).resolve().parent.parent
    else:
        root = Path(args.root).resolve()

    data_dir = root / "data"
    sealed_dir = root / "sealed"
    results_dir = root / "results"
    manifest_dir = root / "manifest"
    scores_dir = root / "scores"
    plots_dir = root / "plots"
    per_cfg_dir = scores_dir / "per_config"
    for d in (scores_dir, per_cfg_dir, plots_dir):
        d.mkdir(parents=True, exist_ok=True)

    # Hash verification (§11.3)
    print("Verifying hashes ... ", end="", flush=True)
    data_hashes = json.loads((manifest_dir / "data_hashes.json").read_text(encoding="utf-8"))
    sealed_hashes = json.loads((manifest_dir / "sealed_hashes.json").read_text(encoding="utf-8"))
    for fname, exp in data_hashes.items():
        got = "sha256:" + sha256_file(data_dir / fname)
        if got != exp:
            print("FAIL")
            print(f"Hash mismatch on {fname}: expected {exp}, got {got}")
            return 3
    for fname, exp in sealed_hashes.items():
        got = "sha256:" + sha256_file(sealed_dir / fname)
        if got != exp:
            print("FAIL")
            print(f"Hash mismatch on {fname}: expected {exp}, got {got}")
            return 3
    print("OK")

    fitter_name = None
    fitter_version = None
    per_config_rows: list[dict] = []
    per_config_summary: list[dict] = []
    by_noise: dict[str, list[bool]] = defaultdict(list)

    for N, p, label in CONFIGS:
        p_pct = int(round(p * 100))
        for s in SEEDS:
            cfg_id = f"N{N}_p{p_pct:03d}_s{s}"
            data_name = f"nscg_{cfg_id}.csv"
            truth_name = f"nscg_{cfg_id}.truth.json"
            fit_name = f"nscg_{cfg_id}.fit.json"

            truth = json.loads((sealed_dir / truth_name).read_text(encoding="utf-8"))
            fit = json.loads((results_dir / fit_name).read_text(encoding="utf-8"))

            # cross-check fitter recorded data hash (§11.3)
            exp_data_hash = data_hashes[data_name]
            if fit.get("data_sha256") and ("sha256:" + fit["data_sha256"]) != exp_data_hash:
                print(f"Fitter data_sha256 mismatch in {fit_name}")
                return 3

            if fitter_name is None:
                fitter_name = fit.get("algorithm_name", "Unknown")
                fitter_version = fit.get("algorithm_version", "0.0.0")

            metrics = per_config_metrics(truth, fit)
            znull = z_null(truth["T_true_matrix"], metrics["A_T"], K=args.znull_K, rng_seed=s)
            metrics.update(znull)
            passed = passes_per_config(p, metrics)

            row = {
                "config_id": cfg_id,
                "N": N, "p_noise": p, "noise_label": label, "seed": s,
                "metrics": metrics,
                "pass": passed,
            }
            per_config_rows.append(row)
            (per_cfg_dir / f"{cfg_id}.score.json").write_text(
                json.dumps(row, indent=2), encoding="utf-8"
            )
            per_config_summary.append({
                "config_id": cfg_id,
                "A_h": metrics["A_h"], "A_sigma": metrics["A_sigma"],
                "R_seam": metrics["R_seam"], "P_seam": metrics["P_seam"], "F_seam": metrics["F_seam"],
                "A_rule": metrics["A_rule"], "A_T": metrics["A_T"],
                "Z_null": metrics["Z_null"],
                "pass": passed,
            })
            by_noise[label].append(passed)
            print(f"  {cfg_id:30s} A_T={metrics['A_T']:.3f} pass={passed}")

    # Per-noise + overall verdict
    per_noise_level = {}
    for label, passes in by_noise.items():
        per_noise_level[label] = {
            "pass_rate": sum(passes),
            "total": len(passes),
            "pass": sum(passes) >= NOISE_LEVEL_MIN_SEEDS[label],
        }
    overall = {
        "low_noise_strict_pass": per_noise_level["low"]["pass_rate"] == 5,
        "med_noise_pass": per_noise_level["med"]["pass_rate"] >= 4,
        "high_noise_pass": per_noise_level["high"]["pass_rate"] >= 3,
    }
    verdict = "PASS" if (
        overall["low_noise_strict_pass"]
        and overall["med_noise_pass"]
        and overall["high_noise_pass"]
    ) else "FAIL"
    overall["verdict"] = verdict

    summary = {
        "spec_version": SPEC_VERSION,
        "addendum_version": ADDENDUM_VERSION,
        "run_timestamp": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fitter_name": fitter_name,
        "fitter_version": fitter_version,
        "per_config": per_config_summary,
        "per_noise_level": per_noise_level,
        "overall": overall,
    }
    (scores_dir / "B1_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    # Per-config metrics (full) and curves
    (scores_dir / "per_config_metrics.json").write_text(
        json.dumps(per_config_rows, indent=2), encoding="utf-8"
    )
    curves = aggregate_curves(per_config_rows)
    (scores_dir / "curves.json").write_text(json.dumps(curves, indent=2), encoding="utf-8")
    consistency = curve_consistency(per_config_rows, curves)
    (scores_dir / "curve_consistency.json").write_text(
        json.dumps(consistency, indent=2), encoding="utf-8"
    )

    # Plots
    plot_files = make_plots(per_config_rows, curves, plots_dir)

    # Reports
    write_curve_analysis_md(
        root / "B1_CURVE_ANALYSIS.md",
        summary, curves, consistency, plot_files, fitter_name, fitter_version,
    )
    write_tower_stability_note(
        root / "B1_TOWER_STABILITY_NOTE.md",
        summary, consistency,
    )

    print()
    print(f"Verdict: {verdict}")
    print(f"CCS    : {consistency['CCS']:.3f}  ({consistency['band']})")
    print(f"Wrote scores/, plots/, B1_CURVE_ANALYSIS.md, B1_TOWER_STABILITY_NOTE.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
