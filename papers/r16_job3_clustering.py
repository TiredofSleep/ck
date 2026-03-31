"""
r16_job3_clustering.py
========================
R16 Atlas Job 3 — Three-Class Clustering Analysis

Takes reduction results from r16_job1_reduction.py and produces:
  - Three-class population breakdown (Oracle / Gate-strong / TSML-like)
  - Per-class centroid statistics
  - Atlas law verification (score prediction vs empirical rate)
  - Gradient law check (grad_score ↔ gap correlation)
  - HAR_mass cluster (position law check)
  - Phase diagram data (gate_score vs HAR_mass, colored by class)
  - Orbit_hit_rate analysis (second gap predictor candidate)

Usage:
    python r16_job3_clustering.py --input results/reduction_b55_N10000.json
    python r16_job3_clustering.py --input results/reduction_b55_N10000.json --plot

Author: Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047
Sprint 4 (March 2026) — Universal construction law atlas
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

import argparse
import json
import os
from math import gcd, sqrt
from typing import Dict, List, Optional

import numpy as np

# Reference values from sprint4 tested worlds
REFERENCE_ATLAS = {
    10:  {'score': 6.857,  'rnd_pct': 4.0,   'HAR_m': 0.650, 'gap': 0.474},
    14:  {'score': 2.500,  'rnd_pct': 0.0,   'HAR_m': 0.778, 'gap': 0.944},
    15:  {'score': 7.057,  'rnd_pct': 78.6,  'HAR_m': 0.756, 'gap': 0.677},
    22:  {'score': 5.464,  'rnd_pct': 83.3,  'HAR_m': 0.604, 'gap': 0.551},
    35:  {'score': 8.265,  'rnd_pct': 76.2,  'HAR_m': 0.722, 'gap': 0.569},
    55:  {'score': 10.045, 'rnd_pct': None,  'HAR_m': None,  'gap': None},
    65:  {'score': 9.375,  'rnd_pct': None,  'HAR_m': None,  'gap': None},
}

# Three-class thresholds (from sprint4 THREE_CLASS_LANDSCAPE.md, b=10 reference)
# Uses G_stay (G→G fraction) instead of G_reach: calibrated per |G| naturally.
TSML_GATE_THRESH    = 0.85   # gate_score ≥ this (C stays in C)
TSML_GSTAY_THRESH   = 0.12   # G_stay ≤ this (G drains to C, not loops in G)
TSML_HAR_THRESH     = 0.55   # HAR_mass ≥ this (strong attractor)
TSML_ORDER_THRESH   = 0.30   # order_align ≥ this (order crystallization)


# ═══════════════════════════════════════════════════════════════════════════════
#  CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

def classify_trial(m: dict) -> str:
    gate_ok    = m['gate_score']  >= TSML_GATE_THRESH
    g_stay_ok  = m.get('G_stay', 1.0) <= TSML_GSTAY_THRESH
    har_ok     = m['HAR_mass']    >= TSML_HAR_THRESH
    order_ok   = m['order_align'] >= TSML_ORDER_THRESH

    if gate_ok and g_stay_ok and har_ok and order_ok:
        return 'TSML-like'
    elif gate_ok and g_stay_ok:
        return 'Gate-strong'
    elif har_ok:
        return 'Oracle'
    else:
        return 'Other'


# ═══════════════════════════════════════════════════════════════════════════════
#  STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

def _stats(vals: List[float]) -> dict:
    if not vals:
        return {'n': 0, 'mean': None, 'std': None, 'min': None, 'max': None,
                'p25': None, 'p75': None}
    a = np.array(vals)
    return {
        'n':    len(vals),
        'mean': round(float(np.mean(a)), 4),
        'std':  round(float(np.std(a)), 4),
        'min':  round(float(np.min(a)), 4),
        'max':  round(float(np.max(a)), 4),
        'p25':  round(float(np.percentile(a, 25)), 4),
        'p75':  round(float(np.percentile(a, 75)), 4),
    }


def class_centroids(results: List[dict], classes: List[str]) -> dict:
    """Compute centroid statistics for each class."""
    keys = ['gate_score', 'G_reach', 'G_stay', 'HAR_mass', 'gap', 'order_align', 'objective']
    out = {}
    for cls in ['TSML-like', 'Gate-strong', 'Oracle', 'Other']:
        members = [r for r, c in zip(results, classes) if c == cls]
        out[cls] = {
            'count': len(members),
            'pct':   round(100 * len(members) / max(len(results), 1), 2),
        }
        for k in keys:
            out[cls][k] = _stats([m[k] for m in members])
    return out


def orbit_hit_rate(results: List[dict], classes: List[str],
                   world: dict) -> dict:
    """Analyze oracle_hit_rate signal as second gap predictor.

    orbit_hit_rate = fraction of (non-orbit × ALL_C) products in orbit
    We can't recompute this from the stored metrics alone (need the table),
    but we CAN measure the gap→class correlation as a proxy.

    Returns correlation analysis using available metrics.
    """
    # Within-class gap variation (the "within-grad spread")
    gate_strong = [r for r, c in zip(results, classes) if c == 'Gate-strong']
    tsml_like   = [r for r, c in zip(results, classes) if c == 'TSML-like']

    gs_gaps = [r['gap'] for r in gate_strong]
    ts_gaps = [r['gap'] for r in tsml_like]

    # Correlation of gap with objective within Gate-strong class
    if len(gate_strong) >= 5:
        objectives = [r['objective'] for r in gate_strong]
        gaps_arr = np.array(gs_gaps)
        obj_arr  = np.array(objectives)
        if gaps_arr.std() > 0 and obj_arr.std() > 0:
            r_gap_obj = float(np.corrcoef(gaps_arr, obj_arr)[0, 1])
        else:
            r_gap_obj = 0.0
    else:
        r_gap_obj = None

    # HAR_mass → gap correlation (tests gradient law proxy)
    all_gaps = np.array([r['gap'] for r in results])
    all_hars = np.array([r['HAR_mass'] for r in results])
    if all_gaps.std() > 0 and all_hars.std() > 0:
        r_har_gap = float(np.corrcoef(all_hars, all_gaps)[0, 1])
    else:
        r_har_gap = 0.0

    return {
        'gate_strong_gap':   _stats(gs_gaps),
        'tsml_like_gap':     _stats(ts_gaps),
        'r_gap_obj_within_gs': round(r_gap_obj, 4) if r_gap_obj else None,
        'r_har_gap':         round(r_har_gap, 4),
        'within_gs_spread':  round(float(np.std(gs_gaps)), 4) if gs_gaps else None,
        'note': 'orbit_hit_rate requires table re-run; gap spread here is proxy signal',
    }


def atlas_law_check(b: int, score: float, tsml_rate: float,
                    har_mass_mean: float, gap_mean: float) -> dict:
    """Verify atlas law predictions against empirical results."""
    ref = REFERENCE_ATLAS.get(b, {})
    b15 = REFERENCE_ATLAS[15]
    b10 = REFERENCE_ATLAS[10]

    checks = {}

    # Score rank check
    checks['score_above_b15'] = score > b15['score']
    checks['score_above_b10'] = score > b10['score']

    # Rate prediction: score > b15['score'] → rate > b15['rnd_pct']
    if checks['score_above_b15']:
        checks['rate_prediction'] = 'should_beat_b15_78pct'
        checks['rate_beats_b15']  = tsml_rate * 100 > b15['rnd_pct']
    else:
        checks['rate_prediction'] = 'should_beat_b10_4pct'
        checks['rate_beats_b10']  = tsml_rate * 100 > b10['rnd_pct']

    # φ-compression: b=55 has φ=8, expect lower gap than b=15 (φ=5)
    # r(φ, gap) = -0.605 → higher φ → lower gap
    checks['phi_compression_note'] = (
        f"φ={score:.0f} — "
        f"expected gap direction vs b=15 (gap=0.677): "
        f"{'lower' if b > 15 else 'similar or higher'}"
    )

    # HAR position law: if HAR = min(C\{1}) → high HAR_m (>0.70)
    # (checked separately with world geometry)

    if ref.get('rnd_pct') is not None:
        checks['ref_rate_match'] = abs(tsml_rate * 100 - ref['rnd_pct']) < 5.0

    return checks


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def analyze(data: dict, plot: bool = False) -> dict:
    """Run full clustering analysis on job1 results."""
    b        = data['b']
    n_trials = data['n_trials']
    world    = data['world']
    results  = data['results']

    print(f"\n{'='*65}")
    print(f"R16 Atlas Job 3 — Clustering Analysis: b={b}")
    print(f"Trials={n_trials}  Seeded={data.get('seeded', False)}")
    print(f"{'='*65}")

    # ── World geometry recap ─────────────────────────────────────────────────
    print(f"\nWorld geometry:")
    print(f"  C = {world['C']}  (φ={world['phi']})")
    print(f"  G = {world['G']}  HAR = {world['HAR']}")
    print(f"  Construction score = {world['score']:.4f}")
    print(f"  grad_score = {world['grad_score']:.4f}  "
          f"gate_ease = {world['gate_ease']:.4f}")

    # HAR position law check
    C_set = set(world['C'])
    HAR = world['HAR']
    C_non_one = [c for c in world['C'] if c != 1]
    if C_non_one:
        HAR_is_min = (HAR == min(C_non_one))
        print(f"  HAR={HAR} is min(C\\{{1}})? {HAR_is_min} "
              f"→ {'high HAR_m cluster predicted' if HAR_is_min else 'low HAR_m cluster'}")

    # ── Re-classify (in case thresholds differ from job1) ────────────────────
    classes = [classify_trial(r) for r in results]
    centroids = class_centroids(results, classes)

    # ── Class populations ────────────────────────────────────────────────────
    print(f"\n{'─'*65}")
    print(f"Three-Class Population (thresholds: gate≥{TSML_GATE_THRESH}, "
          f"G_stay≤{TSML_GSTAY_THRESH}, HAR_m≥{TSML_HAR_THRESH}, "
          f"order≥{TSML_ORDER_THRESH})")
    print(f"{'─'*65}")
    header = f"  {'Class':12s} {'N':>7} {'%':>7} {'gate':>7} {'G_stay':>7} "
    header += f"{'HAR_m':>7} {'gap':>7} {'order':>7}"
    print(header)
    print(f"  {'-'*65}")
    for cls in ['TSML-like', 'Gate-strong', 'Oracle', 'Other']:
        c = centroids[cls]
        if c['count'] == 0:
            print(f"  {cls:12s} {'0':>7} {'0.0%':>7}  (none)")
            continue
        gate_m  = c['gate_score']['mean']
        gs_m    = c['G_stay']['mean'] if c['G_stay']['mean'] is not None else 0.0
        har_m   = c['HAR_mass']['mean']
        gap_m   = c['gap']['mean']
        ord_m   = c['order_align']['mean']
        print(f"  {cls:12s} {c['count']:7d} {c['pct']:6.1f}%  "
              f"{gate_m:7.4f} {gs_m:7.4f} {har_m:7.4f} {gap_m:7.4f} {ord_m:7.4f}")

    # ── Atlas law checks ─────────────────────────────────────────────────────
    tsml_rate   = centroids['TSML-like']['count'] / n_trials
    har_mean    = float(np.mean([r['HAR_mass'] for r in results]))
    gap_mean    = float(np.mean([r['gap'] for r in results]))

    checks = atlas_law_check(b, world['score'], tsml_rate, har_mean, gap_mean)

    print(f"\n{'─'*65}")
    print(f"Atlas Law Checks:")
    b15, b10 = REFERENCE_ATLAS[15], REFERENCE_ATLAS[10]
    print(f"  Construction score: {world['score']:.3f}  "
          f"(b=15: {b15['score']:.3f}, b=10: {b10['score']:.3f})")
    print(f"  TSML-like rate:     {tsml_rate*100:.1f}%  "
          f"(b=15: 78.6%, b=10: 4.0%)")
    if checks.get('score_above_b15'):
        verdict = '✓ CONFIRMED' if checks.get('rate_beats_b15') else '✗ NOT YET'
        print(f"  Prediction (score > b=15 → rate > 78.6%): {verdict}")
    else:
        verdict = '✓ CONFIRMED' if checks.get('rate_beats_b10') else '✗ NOT YET'
        print(f"  Prediction (score > b=10 → rate > 4.0%): {verdict}")

    # ── HAR_mass cluster (position law) ─────────────────────────────────────
    print(f"\n{'─'*65}")
    print(f"HAR_mass Cluster Analysis (Position Law):")
    all_hars = [r['HAR_mass'] for r in results]
    best_hars = sorted(all_hars, reverse=True)[:max(1, n_trials//10)]
    print(f"  Mean HAR_mass (all): {np.mean(all_hars):.4f}")
    print(f"  Mean HAR_mass (top 10%): {np.mean(best_hars):.4f}")
    if C_non_one:
        if HAR_is_min:
            print(f"  HAR={HAR} = min(C\\{{1}}) → predicted high cluster (≥0.70)")
            verdict = '✓' if np.mean(best_hars) >= 0.70 else 'partial'
            print(f"  Top-10% mean {np.mean(best_hars):.4f}: {verdict}")
        else:
            print(f"  HAR={HAR} ≠ min(C\\{{1}}) → predicted low cluster (<0.70)")
            verdict = '✓' if np.mean(best_hars) < 0.70 else 'partial'
            print(f"  Top-10% mean {np.mean(best_hars):.4f}: {verdict}")

    # ── Gradient law check ───────────────────────────────────────────────────
    print(f"\n{'─'*65}")
    print(f"Gradient Law Check (within φ-tier):")
    print(f"  grad_score = {world['grad_score']:.4f}  φ = {world['phi']}")
    ref_worlds_same_phi = {k: v for k, v in REFERENCE_ATLAS.items()
                           if k != b and v.get('gap') is not None}
    print(f"  Reference gap at b=15 (φ=5): 0.677  grad=0.714")
    print(f"  Reference gap at b=22 (φ=5): 0.551  grad=0.500")
    print(f"  This world gap mean: {gap_mean:.4f}")
    # Within TSML-like class: gap distribution
    tsml_gaps = [r['gap'] for r, c in zip(results, classes) if c == 'TSML-like']
    if tsml_gaps:
        print(f"  TSML-like gap: mean={np.mean(tsml_gaps):.4f}  "
              f"std={np.std(tsml_gaps):.4f}")

    # ── Orbit hit rate proxy (second gap predictor) ──────────────────────────
    print(f"\n{'─'*65}")
    print(f"Within-Class Gap Spread (Second Predictor Analysis):")
    orbit_analysis = orbit_hit_rate(results, classes, world)
    gs_spread = orbit_analysis.get('within_gs_spread')
    if gs_spread is not None:
        print(f"  Gate-strong gap spread (std): {gs_spread:.4f}  "
              f"(b=10 baseline: ~0.111)")
        verdict = 'similar to b=10' if abs(gs_spread - 0.111) < 0.04 else \
                  'different — check orbit_hit_rate'
        print(f"  Verdict: {verdict}")
    print(f"  r(HAR_mass, gap) = {orbit_analysis['r_har_gap']:.4f}  "
          f"(b=10 gradient law: r=0.749)")

    # ── Comparison to predicted atlas ────────────────────────────────────────
    print(f"\n{'─'*65}")
    print(f"Semiprime Atlas Comparison:")
    ref_worlds = [(k, v) for k, v in REFERENCE_ATLAS.items()
                  if v.get('rnd_pct') is not None]
    ref_worlds.sort(key=lambda x: -x[1]['score'])
    print(f"  {'b':>5} {'score':>7} {'rnd%':>7} {'HAR_m':>7} {'gap':>7}")
    print(f"  {'-'*35}")
    for bref, vref in ref_worlds:
        marker = ' ★' if bref == b else ''
        print(f"  {bref:5d} {vref['score']:7.3f} {vref['rnd_pct']:6.1f}% "
              f"{vref['HAR_m']:7.4f} {vref['gap']:7.4f}{marker}")
    # Add current result
    print(f"  {b:5d} {world['score']:7.3f} {tsml_rate*100:6.1f}% "
          f"{np.mean(best_hars):7.4f} "
          f"{np.mean(tsml_gaps) if tsml_gaps else gap_mean:7.4f}  ← THIS RUN")

    # ── Best trial details ───────────────────────────────────────────────────
    best = max(results, key=lambda r: r['objective'])
    print(f"\n{'─'*65}")
    print(f"Best Trial (by objective={best['objective']:.4f}):")
    print(f"  gate={best['gate_score']:.4f}  G_reach={best['G_reach']:.4f}  "
          f"HAR_mass={best['HAR_mass']:.4f}  gap={best['gap']:.4f}  "
          f"order={best['order_align']:.4f}")
    print(f"  class: {classify_trial(best)}")

    # ── Output dict ─────────────────────────────────────────────────────────
    analysis = {
        'b': b,
        'n_trials': n_trials,
        'seeded': data.get('seeded', False),
        'world': world,
        'centroids': centroids,
        'atlas_law_checks': checks,
        'orbit_analysis': orbit_analysis,
        'tsml_like_rate': round(tsml_rate, 4),
        'all_stats': {
            k: _stats([r[k] for r in results if k in r])
            for k in ['gate_score', 'G_reach', 'G_stay', 'HAR_mass', 'gap',
                      'order_align', 'objective']
        },
        'best_trial': best,
        'thresholds_used': {
            'gate': TSML_GATE_THRESH,
            'G_stay': TSML_GSTAY_THRESH,
            'HAR_mass': TSML_HAR_THRESH,
            'order_align': TSML_ORDER_THRESH,
        },
    }

    if plot:
        _try_plot(results, classes, b, world)

    return analysis


def _try_plot(results: List[dict], classes: List[str],
              b: int, world: dict) -> None:
    """Optional phase diagram: gate_score vs HAR_mass, colored by class."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        colors = {'TSML-like': 'green', 'Gate-strong': 'blue',
                  'Oracle': 'orange', 'Other': 'grey'}
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Phase diagram: gate vs HAR_mass
        ax = axes[0]
        for cls in ['Other', 'Oracle', 'Gate-strong', 'TSML-like']:
            pts = [(r['gate_score'], r['HAR_mass'])
                   for r, c in zip(results, classes) if c == cls]
            if pts:
                xs, ys = zip(*pts)
                ax.scatter(xs, ys, c=colors[cls], label=cls,
                           alpha=0.4, s=5)
        ax.set_xlabel('gate_score')
        ax.set_ylabel('HAR_mass')
        ax.set_title(f'b={b}: gate vs HAR_mass')
        ax.legend(fontsize=8)
        ax.axvline(TSML_GATE_THRESH, color='black', linestyle='--', alpha=0.3)
        ax.axhline(TSML_HAR_THRESH,  color='black', linestyle='--', alpha=0.3)

        # Distribution: gap histogram per class
        ax = axes[1]
        for cls in ['Oracle', 'Gate-strong', 'TSML-like']:
            gaps = [r['gap'] for r, c in zip(results, classes) if c == cls]
            if gaps:
                ax.hist(gaps, bins=30, alpha=0.5, label=cls,
                        color=colors[cls], density=True)
        ax.set_xlabel('gap')
        ax.set_ylabel('density')
        ax.set_title(f'b={b}: gap distribution by class')
        ax.legend(fontsize=8)

        fig.suptitle(f'b={b} semiprime atlas | score={world["score"]:.3f} | '
                     f'φ={world["phi"]} HAR={world["HAR"]}', fontsize=10)
        fig.tight_layout()
        out = f'results/phase_diagram_b{b}.png'
        fig.savefig(out, dpi=150)
        print(f"\n  Phase diagram saved → {out}")
    except ImportError:
        print("\n  (matplotlib not available — skip plot)")


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='R16 Atlas Job 3: Clustering analysis on reduction results')
    parser.add_argument('--input', type=str, required=True,
                        help='Input JSON from r16_job1_reduction.py')
    parser.add_argument('--plot', action='store_true',
                        help='Generate phase diagram (requires matplotlib)')
    parser.add_argument('--output', type=str, default=None,
                        help='Output JSON path (default: auto-named in results/)')
    args = parser.parse_args()

    # Load data
    if not os.path.exists(args.input):
        print(f"ERROR: input file not found: {args.input}")
        sys.exit(1)
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Loaded {len(data['results'])} trials from {args.input}")

    # Run analysis
    analysis = analyze(data, plot=args.plot)

    # Save analysis
    if args.output:
        out_path = args.output
    else:
        inp = args.input.replace('reduction_', 'cluster_')
        out_path = inp

    with open(out_path, 'w', encoding='utf-8') as f:
        # Don't re-save raw results (already in input file)
        compact = {k: v for k, v in analysis.items()
                   if k not in ('centroids',)}
        # Re-add centroids without per-metric stats (just counts/pcts)
        compact['class_counts'] = {
            cls: {'count': analysis['centroids'][cls]['count'],
                  'pct':   analysis['centroids'][cls]['pct']}
            for cls in analysis['centroids']
        }
        json.dump(compact, f, indent=2)
    print(f"\n✓ Analysis saved → {out_path}")

    # Sprint4 atlas update hint
    b = analysis['b']
    rate = analysis['tsml_like_rate']
    world = analysis['world']
    best = analysis['best_trial']
    print(f"\n── Sprint4 Atlas Update (b={b}) ──────────────────────────────")
    print(f"  Add to SEMIPRIME_ATLAS.md:")
    print(f"  | {b} | {world['p']}×{world['q']} | {world['phi']} | "
          f"{world['score']:.3f} | {rate*100:.1f}% | — | "
          f"{best['HAR_mass']:.3f} | {best['gap']:.3f} |")


if __name__ == '__main__':
    main()
