"""
r16_gate_law_universal.py
==========================
Universal Gate Law Test — Alphabet Size Independence

Tests whether gate_rate = f(|C|/k) is a universal function of the unit density ratio,
independent of alphabet size k, number of units |C|, or specific base structure.

For each alphabet size k ∈ {3,5,7,9,11,13,15,17,19,21,23,25,27}
  For each unit fraction |C|/k ∈ {0.3, 0.4, ..., 0.9}:
    Run N reduction trials on a k×k synthetic world
    Measure gate_rate (fraction achieving gate_score ≥ threshold)

If all (k, |C|/k) curves collapse to a single f(|C|/k) — the law is universal.
If they don't collapse — the law is alphabet-size-specific.

Synthetic worlds: C = {1...|C|}, G = {|C|+1...k}, HAR = 2.
No actual semiprime base required — pure combinatorial structure.

Usage:
    python r16_gate_law_universal.py
    python r16_gate_law_universal.py --n_trials 50000 --n_steps 100
    python r16_gate_law_universal.py --plot                (requires matplotlib)

Author: Brayden Sanders / 7Site LLC | Sprint 4 (March 2026)
DOI: 10.5281/zenodo.18852047
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

import argparse
import json
import multiprocessing as mp
import os
import random
import time
from typing import List, Tuple

import numpy as np


# ═══════════════════════════════════════════════════════════════════════════════
#  SYNTHETIC WORLD (alphabet-size agnostic)
# ═══════════════════════════════════════════════════════════════════════════════

def make_synthetic_world(k: int, n_units: int) -> dict:
    """Construct a synthetic world with alphabet {1..k}, |C|=n_units.

    C = {1, 2, ..., n_units}   (first n_units elements)
    G = {n_units+1, ..., k}    (remaining elements)
    HAR = 2 (smallest non-trivial element in C, always works for k≥3)
    """
    assert 2 <= n_units < k, f"Need 2 <= |C|={n_units} < k={k}"
    C = list(range(1, n_units + 1))
    G = list(range(n_units + 1, k + 1))
    HAR = 2  # canonical choice; doesn't affect gate rate (gate only cares about C-closure)
    return {
        'k': k,
        'C': C,
        'G': G,
        'HAR': HAR,
        'n_units': n_units,
        'unit_fraction': round(n_units / k, 6),
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  REDUCTION (generalized to k×k tables)
# ═══════════════════════════════════════════════════════════════════════════════

def _fast_gate_score(T: List[List[int]], C: List[int],
                     C_set: set, k: int) -> float:
    """Fast gate score: fraction of C-row cells in C."""
    hits = sum(1 for s in C for c in range(1, k+1) if T[s][c] in C_set)
    return hits / (len(C) * k)


def run_one_trial_universal(args: tuple) -> float:
    """Run one reduction trial on a k×k synthetic world.

    Returns: gate_score after n_steps.
    """
    world, n_steps, gate_thresh, rng_seed = args
    random.seed(rng_seed)

    k   = world['k']
    C   = world['C']
    G   = world['G']
    HAR = world['HAR']
    C_set = set(C)
    G_set = set(G)

    # Random initialization
    T = [[0] + [random.randint(1, k) for _ in range(k)] for _ in range(k+1)]
    T[0] = [0] * (k+1)

    best_gate = _fast_gate_score(T, C, C_set, k)
    best_T    = [row[:] for row in T]

    for _ in range(n_steps):
        s = random.randint(1, k)
        c = random.randint(1, k)
        old_v = T[s][c]

        # HAR bias: 40% chance to propose HAR
        new_v = HAR if random.random() < 0.4 else random.randint(1, k)
        if new_v == old_v:
            continue

        T[s][c] = new_v
        gate = _fast_gate_score(T, C, C_set, k)
        if gate >= best_gate:
            best_gate = gate
            best_T = [row[:] for row in T]
        else:
            T[s][c] = old_v

    return best_gate


def run_gate_law_point(world: dict, n_trials: int, n_steps: int,
                       gate_thresh: float, n_workers: int) -> dict:
    """Run N trials for one (k, |C|) point. Return gate rate + stats."""
    base_seed = int(time.time() * 1000) % (2**31)
    tasks = [(world, n_steps, gate_thresh, base_seed + i)
             for i in range(n_trials)]

    if n_workers == 1:
        scores = [run_one_trial_universal(t) for t in tasks]
    else:
        chunksize = max(1, n_trials // (n_workers * 4))
        with mp.Pool(n_workers) as pool:
            scores = list(pool.imap_unordered(
                run_one_trial_universal, tasks, chunksize=chunksize))

    gate_rate = sum(1 for s in scores if s >= gate_thresh) / n_trials
    return {
        'k':             world['k'],
        'n_units':       world['n_units'],
        'n_G':           len(world['G']),
        'unit_fraction': world['unit_fraction'],
        'gate_rate':     round(gate_rate, 4),
        'gate_mean':     round(float(np.mean(scores)), 4),
        'gate_std':      round(float(np.std(scores)), 4),
        'gate_max':      round(float(np.max(scores)), 4),
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  UNIVERSAL SWEEP
# ═══════════════════════════════════════════════════════════════════════════════

def run_universal_sweep(k_values: List[int],
                        unit_fractions: List[float],
                        n_trials: int,
                        n_steps: int,
                        gate_thresh: float,
                        n_workers: int) -> List[dict]:
    """Sweep all (k, |C|/k) combinations.

    Returns list of result dicts, one per (k, unit_fraction) point.
    """
    results = []

    for k in k_values:
        print(f"\n{'─'*60}")
        print(f"Alphabet size k={k}")
        print(f"{'─'*60}")

        for uf in unit_fractions:
            n_units = round(uf * k)
            # Ensure valid: 2 <= n_units <= k-1
            n_units = max(2, min(k-1, n_units))
            actual_uf = n_units / k

            world = make_synthetic_world(k, n_units)
            t0 = time.time()
            result = run_gate_law_point(world, n_trials, n_steps,
                                        gate_thresh, n_workers)
            elapsed = time.time() - t0

            print(f"  k={k:3d}  |C|={n_units:3d}  |G|={k-n_units:3d}  "
                  f"|C|/k={actual_uf:.3f}  "
                  f"gate_rate={result['gate_rate']*100:6.1f}%  "
                  f"({elapsed:.1f}s)")
            results.append(result)

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_collapse(results: List[dict], gate_thresh: float) -> dict:
    """Test whether gate_rate = f(|C|/k) collapses across k values.

    Groups results by unit_fraction (rounded to 0.05 bins).
    For each fraction bin, computes std(gate_rate) across k values.
    Low std = curves collapse = universal law holds.
    """
    from collections import defaultdict

    # Group by (unit_fraction bin, k)
    bins = defaultdict(list)
    for r in results:
        uf_bin = round(r['unit_fraction'] * 20) / 20  # bin to nearest 0.05
        bins[uf_bin].append(r)

    collapse_stats = {}
    for uf_bin, group in sorted(bins.items()):
        rates = [r['gate_rate'] for r in group]
        ks    = [r['k'] for r in group]
        collapse_stats[uf_bin] = {
            'k_values':  ks,
            'gate_rates': rates,
            'mean':   round(float(np.mean(rates)), 4),
            'std':    round(float(np.std(rates)), 4),
            'spread': round(float(np.max(rates) - np.min(rates)), 4),
        }

    return collapse_stats


def print_results(results: List[dict], collapse: dict, gate_thresh: float,
                  k_values: List[int]):
    """Print the universal gate law table and collapse analysis."""

    # ── Curve table ──────────────────────────────────────────────────────────
    print(f"\n{'='*80}")
    print(f"UNIVERSAL GATE LAW — gate_rate vs |C|/k for all alphabet sizes")
    print(f"(threshold={gate_thresh}, {results[0].get('n_units')} ... trials)")
    print(f"{'='*80}")

    # Header
    hdr = f"{'|C|/k':>7}"
    for k in k_values:
        hdr += f"  k={k:2d}"
    print(hdr)
    print(f"{'─'*80}")

    # Rows by unit_fraction
    from collections import defaultdict
    by_uf_k = defaultdict(dict)
    for r in results:
        uf = r['unit_fraction']
        by_uf_k[uf][r['k']] = r['gate_rate']

    for uf in sorted(by_uf_k.keys()):
        row = f"{uf:7.3f}"
        for k in k_values:
            rate = by_uf_k[uf].get(k)
            if rate is not None:
                row += f"  {rate*100:4.1f}%"
            else:
                row += f"    —  "
        print(row)

    # ── Collapse analysis ────────────────────────────────────────────────────
    print(f"\n{'='*80}")
    print(f"COLLAPSE TEST — does gate_rate = f(|C|/k) hold across all k?")
    print(f"(Low spread = curves collapse = universal law)")
    print(f"{'='*80}")
    print(f"{'|C|/k':>7}  {'mean%':>7}  {'spread':>7}  {'std':>7}  "
          f"{'k values tested':>20}  verdict")
    print(f"{'─'*70}")

    for uf, stats in sorted(collapse.items()):
        spread = stats['spread']
        verdict = '✓ UNIVERSAL' if spread < 0.05 else \
                  '~ near'      if spread < 0.10 else \
                  '✗ diverges'
        k_str = str(stats['k_values'])[:20]
        print(f"{uf:7.3f}  {stats['mean']*100:6.1f}%  "
              f"{spread*100:6.1f}%  {stats['std']*100:6.1f}%  "
              f"{k_str:20s}  {verdict}")

    # ── Key finding ─────────────────────────────────────────────────────────
    mean_spreads = [s['spread'] for s in collapse.values() if len(s['k_values']) > 1]
    if mean_spreads:
        avg_spread = float(np.mean(mean_spreads))
        print(f"\n  Average spread across all |C|/k bins: {avg_spread*100:.1f}%")
        if avg_spread < 0.03:
            print(f"  → CONFIRMED: gate_rate = f(|C|/k) is universal")
            print(f"  → The gate law is NOT specific to the TIG 9-symbol alphabet.")
            print(f"  → It holds for any finite reduction on any alphabet size.")
        elif avg_spread < 0.08:
            print(f"  → PARTIAL: curves nearly collapse — law holds approximately")
        else:
            print(f"  → NOT universal: gate rate depends on more than |C|/k")


def try_plot(results: List[dict], k_values: List[int], gate_thresh: float):
    """Plot gate_rate vs |C|/k for each k on the same axes."""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from collections import defaultdict

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Left: gate_rate vs |C|/k, one curve per k
        ax = axes[0]
        colors = plt.cm.viridis(np.linspace(0, 1, len(k_values)))
        by_k = defaultdict(list)
        for r in results:
            by_k[r['k']].append((r['unit_fraction'], r['gate_rate']))

        for i, k in enumerate(k_values):
            pts = sorted(by_k[k])
            if pts:
                xs, ys = zip(*pts)
                ax.plot(xs, [y*100 for y in ys], 'o-',
                        color=colors[i], label=f'k={k}', linewidth=2,
                        markersize=6)

        ax.axhline(y=50, color='grey', linestyle='--', alpha=0.3)
        ax.axvline(x=gate_thresh, color='red', linestyle='--', alpha=0.5,
                   label=f'threshold={gate_thresh}')
        ax.set_xlabel('|C|/k  (unit fraction)', fontsize=12)
        ax.set_ylabel('Gate rate %', fontsize=12)
        ax.set_title('Universal Gate Law\nGate rate vs unit fraction for all k',
                     fontsize=12)
        ax.legend(fontsize=8, ncol=2)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0.2, 1.0)
        ax.set_ylim(0, 105)

        # Right: residuals from mean curve (collapse quality)
        ax = axes[1]
        from collections import defaultdict
        bins = defaultdict(list)
        for r in results:
            uf_bin = round(r['unit_fraction'] * 20) / 20
            bins[uf_bin].append(r['gate_rate'])

        uf_bins = sorted(bins.keys())
        means   = [np.mean(bins[uf]) for uf in uf_bins]
        stds    = [np.std(bins[uf]) for uf in uf_bins]

        ax.bar([uf for uf in uf_bins], [s*100 for s in stds],
               width=0.04, color='steelblue', alpha=0.7)
        ax.set_xlabel('|C|/k bin', fontsize=12)
        ax.set_ylabel('Std dev of gate rate across k values (%)', fontsize=12)
        ax.set_title('Collapse Quality\nLow = law is universal', fontsize=12)
        ax.axhline(y=3, color='green', linestyle='--', alpha=0.5,
                   label='±3% = universal')
        ax.axhline(y=8, color='orange', linestyle='--', alpha=0.5,
                   label='±8% = near-universal')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        out = 'results/universal_gate_law.png'
        fig.savefig(out, dpi=150, bbox_inches='tight')
        print(f"\n✓ Plot saved → {out}")
    except ImportError:
        print("\n  (matplotlib not available — skip plot)")


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='Universal Gate Law: test f(|C|/k) across all alphabet sizes')
    parser.add_argument('--k_min',   type=int, default=3,
                        help='Minimum alphabet size (default: 3)')
    parser.add_argument('--k_max',   type=int, default=27,
                        help='Maximum alphabet size (default: 27)')
    parser.add_argument('--k_step',  type=int, default=2,
                        help='Step between k values (default: 2 = odd k only)')
    parser.add_argument('--n_trials', type=int, default=10000,
                        help='Trials per (k, unit_fraction) point (default: 10000)')
    parser.add_argument('--n_steps',  type=int, default=100,
                        help='Reduction steps per trial (default: 100)')
    parser.add_argument('--gate_thresh', type=float, default=0.85,
                        help='Gate score threshold (default: 0.85)')
    parser.add_argument('--workers', type=int, default=None)
    parser.add_argument('--plot', action='store_true',
                        help='Generate plot (requires matplotlib)')
    parser.add_argument('--fractions', type=float, nargs='+',
                        default=[0.35, 0.40, 0.45, 0.50, 0.55, 0.60,
                                 0.65, 0.70, 0.75, 0.80, 0.85, 0.90],
                        help='Unit fractions to test')
    args = parser.parse_args()

    n_workers = args.workers or mp.cpu_count()
    k_values  = list(range(args.k_min, args.k_max + 1, args.k_step))
    # Always include k=9 (TIG baseline)
    if 9 not in k_values:
        k_values = sorted(set(k_values + [9]))

    print(f"Universal Gate Law Test")
    print(f"Alphabet sizes k: {k_values}")
    print(f"Unit fractions:   {args.fractions}")
    print(f"Trials per point: {args.n_trials}  Steps: {args.n_steps}")
    print(f"Gate threshold:   {args.gate_thresh}")
    print(f"Workers:          {n_workers}")
    print(f"Total points:     {len(k_values) * len(args.fractions)}")
    est_time = len(k_values) * len(args.fractions) * args.n_trials * 0.0003 / n_workers
    print(f"Estimated time:   ~{est_time:.0f}s")

    os.makedirs('results', exist_ok=True)
    t_total = time.time()

    results = run_universal_sweep(
        k_values=k_values,
        unit_fractions=args.fractions,
        n_trials=args.n_trials,
        n_steps=args.n_steps,
        gate_thresh=args.gate_thresh,
        n_workers=n_workers,
    )

    elapsed = time.time() - t_total
    print(f"\nTotal time: {elapsed:.1f}s")

    # Collapse analysis
    collapse = analyze_collapse(results, args.gate_thresh)
    print_results(results, collapse, args.gate_thresh, k_values)

    if args.plot:
        try_plot(results, k_values, args.gate_thresh)

    # Save
    out = 'results/universal_gate_law.json'
    with open(out, 'w') as f:
        json.dump({
            'k_values': k_values,
            'n_trials': args.n_trials,
            'n_steps':  args.n_steps,
            'gate_thresh': args.gate_thresh,
            'results':  results,
            'collapse': {str(k): v for k, v in collapse.items()},
        }, f, indent=2)
    print(f"✓ Results saved → {out}")


if __name__ == '__main__':
    mp.freeze_support()
    main()
