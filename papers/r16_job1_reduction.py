"""
r16_job1_reduction.py
======================
R16 Atlas Job 1 — Semiprime Reduction Survey

Runs N reduction trials at base b. Measures native TSML-like rate, gate
strength, HAR_mass, spectral gap, G-reach, and order alignment for each trial.
Outputs full results JSON for clustering (job3).

Usage:
    python r16_job1_reduction.py --b 55 --n_start 10000 --n_steps 100
    python r16_job1_reduction.py --b 35 --n_start 10000 --n_steps 100 --seeded
    python r16_job1_reduction.py --b 14 --n_start 1000 --n_steps 200 --seeded

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
import copy
import json
import math
import multiprocessing as mp
import os
import random
import time
from math import gcd
from typing import Dict, List, Optional, Tuple

import numpy as np

# ── B=10 known seed cells (BHML residual, for reference + seeded mode) ─────────
# These are cells where the b=10 TSML agrees with max(s,c).
# Derived from sprint4 CONSTRUCTION_HIERARCHY.md.
B10_SEED_CELLS: Dict[Tuple[int,int], int] = {
    # (row, col): max(row, col)
    # BHML residual cells at b=10 (6-cell seed)
    (2,9): 9, (3,9): 9, (7,9): 9,
    (9,2): 9, (9,3): 9, (9,7): 9,
}

# B=14 residual seed cells (from sprint4 CONSTRUCTION_HIERARCHY.md)
B14_SEED_CELLS: Dict[Tuple[int,int], int] = {
    (s,c): max(s,c)
    for (s,c) in [(2,7),(4,6),(4,8),(4,9),(5,9),(6,8),(6,9),(7,8),(7,9)]
}


# ═══════════════════════════════════════════════════════════════════════════════
#  WORLD GEOMETRY
# ═══════════════════════════════════════════════════════════════════════════════

def compute_world(b: int) -> dict:
    """Compute C, G, HAR, orbit_depth, gate_ease, grad_score for base b.

    Returns:
        dict with keys: b, p, q, C, G, HAR, phi, orbit_depth, gate_ease,
                        grad_score, score, order_seed (cells matching max(s,c))
    """
    # Factorise b as semiprime
    p, q = _factorise(b)

    # C = units mod b, intersected with {1..9}
    C = sorted(x for x in range(1, 10) if gcd(x, b) == 1)
    G = sorted(x for x in range(1, 10) if x not in C)
    phi = len(C)  # Euler totient restricted to {1..9}

    if len(C) < 2:
        raise ValueError(f"b={b} is degenerate (|C|={len(C)} < 2)")

    # HAR = min orbit-central element
    HAR = _find_har(C, b)

    # Orbit depth of HAR under multiplication mod b
    orbit_depth = _orbit_depth(HAR, b)

    # Residual pairs: (s, c) where s∈G, c∈C (pairs that test gate)
    res_pairs = len(G) * len(C)

    # Gate ease: higher = easier to enforce one-way gate
    # Proxy: HAR's position advantage — how many G elements lie ABOVE HAR
    # (elements above HAR create weaker leak channels)
    if G:
        g_above = sum(1 for g in G if g > HAR)
        gate_ease = (g_above + 1) / (len(G) + 1)
    else:
        gate_ease = 1.0  # No G → trivially gated

    # Score = construction cost formula (SEMIPRIME_ATLAS.md)
    total_cells = 9 * 9
    if res_pairs > 0:
        score = (phi * res_pairs * orbit_depth * gate_ease) / total_cells
    else:
        score = 0.0

    # Grad score: max dist of non-orbit C-element from HAR / C-range
    C_range = max(C) - min(C) if len(C) > 1 else 1
    orbit = _full_orbit(HAR, b, C)
    non_orbit_C = [c for c in C if c not in orbit and c != 1]
    if non_orbit_C and C_range > 0:
        grad_score = max(abs(c - HAR) for c in non_orbit_C) / C_range
    else:
        grad_score = 0.0

    # Order endpoint: T_max(s,c) = max(s,c) for all s,c ∈ {1..9}
    # Order seed cells: where a candidate table should match max(s,c)
    order_seed = {(s, c): max(s, c)
                  for s in range(1, 10) for c in range(1, 10)}

    return {
        'b': b, 'p': p, 'q': q,
        'C': C, 'G': G, 'HAR': HAR,
        'phi': phi, 'orbit_depth': orbit_depth,
        'gate_ease': gate_ease, 'grad_score': round(grad_score, 4),
        'score': round(score, 4),
        'order_seed': order_seed,
    }


def _factorise(b: int) -> Tuple[int, int]:
    """Return (p, q) for semiprime b = p*q."""
    for p in range(2, int(b**0.5) + 1):
        if b % p == 0:
            return p, b // p
    raise ValueError(f"{b} is prime, not a semiprime")


def _find_har(C: List[int], b: int) -> int:
    """Find HAR using revised orbit-central rule.

    HAR = min{h∈C : h²%b ∈ C, h²%b ≠ 1, h²%b ≠ h}
    (sprint4 ATLAS_LAW_SET.md — min orbit-central, not max orbit-size)
    """
    candidates = []
    for h in C:
        if h == 1:
            continue
        sq = (h * h) % b
        if sq in C and sq != 1 and sq != h:
            candidates.append(h)
    if not candidates:
        # Fallback: pick middle non-1 C element (degenerate case)
        non_one = [c for c in C if c != 1]
        return non_one[len(non_one) // 2] if non_one else C[0]
    return min(candidates)


def _full_orbit(h: int, b: int, C: List[int]) -> List[int]:
    """Compute multiplication orbit of h under mod b within C."""
    C_set = set(C)
    orbit = []
    cur = h
    for _ in range(20):
        if cur not in C_set:
            break
        orbit.append(cur)
        cur = (cur * h) % b
        if cur in orbit:
            break
    return orbit


def _orbit_depth(h: int, b: int) -> int:
    """Length of multiplication orbit of h mod b before revisiting."""
    seen = set()
    cur = h
    depth = 0
    while cur not in seen and depth < 100:
        seen.add(cur)
        cur = (cur * h) % b
        depth += 1
    return depth


# ═══════════════════════════════════════════════════════════════════════════════
#  TABLE SCORING
# ═══════════════════════════════════════════════════════════════════════════════

def score_metrics(T: List[List[int]], C: List[int], G: List[int],
                  HAR: int) -> dict:
    """Compute all metrics for a candidate 9×9 table T (1-indexed).

    Returns dict: gate_score, G_reach, G_stay, HAR_mass, gap, order_align, objective

    G_reach = fraction of (s∈G, c) pairs where T[s][c] ∈ C
              (how strongly G flows into C; high = G funnels to C attractor)

    G_stay  = fraction of (s∈G, c) pairs where T[s][c] ∈ G
              (how strongly G stays in G; low = G drains to C quickly)
              Used for cross-base comparison: G_stay is calibrated per |G|.
    """
    C_set = set(C)
    n = 9

    # Gate score: fraction of (s,c) for s∈C where T[s][c] ∈ C
    if C:
        gate_hits = sum(1 for s in C for c in range(1, 10)
                        if T[s][c] in C_set)
        gate_score = gate_hits / (len(C) * 9)
    else:
        gate_score = 0.0

    # G-reach: fraction of (s,c) for s∈G where T[s][c] ∈ C
    # G-stay:  fraction where T[s][c] ∈ G (complement)
    if G:
        g_c_hits  = sum(1 for s in G for c in range(1, 10) if T[s][c] in C_set)
        g_g_hits  = sum(1 for s in G for c in range(1, 10) if T[s][c] in set(G))
        G_reach = g_c_hits / (len(G) * 9)
        G_stay  = g_g_hits / (len(G) * 9)
    else:
        G_reach = 0.0
        G_stay  = 0.0

    # Transfer matrix P[s-1][t-1] = |{c∈C: T[s][c]==t}| / |C|
    P = np.zeros((n, n))
    if C:
        for s in range(1, 10):
            for c in C:
                t = T[s][c]
                P[s-1][t-1] += 1.0 / len(C)

    # Spectral gap: 1 - |second eigenvalue| of P
    try:
        eigvals = np.linalg.eigvals(P)
        abs_eigs = sorted(abs(e) for e in eigvals)[::-1]
        gap = 1.0 - abs_eigs[1] if len(abs_eigs) > 1 else 1.0
    except Exception:
        gap = 0.0

    # HAR_mass: empirical — run chains from every state, count fraction → HAR
    HAR_mass = _empirical_har_mass(T, HAR, n_steps=30, n_start=9*5)

    # Order alignment: fraction of cells matching max(s,c)
    order_hits = sum(1 for s in range(1, 10) for c in range(1, 10)
                     if T[s][c] == max(s, c))
    order_align = order_hits / 81.0

    # Composite objective (gate-weighted reduction, sprint4)
    # G_stay penalty: high G_stay means G loops in itself (bad for attractor)
    objective = (0.50 * gate_score
                 + 0.25 * HAR_mass
                 + 0.15 * gap
                 + 0.10 * (1.0 - G_stay))

    return {
        'gate_score':   round(gate_score, 4),
        'G_reach':      round(G_reach, 4),
        'G_stay':       round(G_stay, 4),
        'HAR_mass':     round(HAR_mass, 4),
        'gap':          round(gap, 4),
        'order_align':  round(order_align, 4),
        'objective':    round(objective, 4),
    }


def _empirical_har_mass(T: List[List[int]], HAR: int,
                        n_steps: int = 30, n_start: int = 45) -> float:
    """Empirical HAR_mass: fraction of random walks ending at HAR."""
    hits = 0
    cols = list(range(1, 10))
    for _ in range(n_start):
        state = random.randint(1, 9)
        for _ in range(n_steps):
            c = random.choice(cols)
            state = T[state][c]
        if state == HAR:
            hits += 1
    return hits / n_start


def _fast_objective(T: List[List[int]], C: List[int], G: List[int],
                    HAR: int, C_set: set) -> float:
    """Fast objective for inner reduction loop (no full eigenvalue)."""
    G_set = set(G)

    # Gate score
    gate_hits = sum(1 for s in C for c in range(1, 10) if T[s][c] in C_set)
    gate_score = gate_hits / (len(C) * 9) if C else 0.0

    # G_stay penalty: G staying in G (bad — G should drain to HAR)
    if G:
        g_stay_hits = sum(1 for s in G for c in range(1, 10)
                          if T[s][c] in G_set)
        G_stay = g_stay_hits / (len(G) * 9)
    else:
        G_stay = 0.0

    # HAR column mass: fraction of cells in HAR's column that equal HAR
    har_col = sum(1 for s in range(1, 10) if T[s][HAR] == HAR)
    har_col_f = har_col / 9.0

    return 0.50 * gate_score + 0.25 * har_col_f + 0.25 * (1.0 - G_stay)


# ═══════════════════════════════════════════════════════════════════════════════
#  REDUCTION ALGORITHM
# ═══════════════════════════════════════════════════════════════════════════════

def make_seed_table(C: List[int], G: List[int], HAR: int,
                    seed_cells: Optional[Dict] = None) -> List[List[int]]:
    """Generate a random starting table with optional seed cell pre-fixing."""
    # T is 1-indexed; T[0] and T[s][0] are unused (0-padding)
    T = [[0] + [random.randint(1, 9) for _ in range(9)] for _ in range(10)]
    T[0] = [0] * 10  # row 0 unused

    # Seed: fix cells to max(s,c) for known residual cells
    if seed_cells:
        for (s, c), v in seed_cells.items():
            if 1 <= s <= 9 and 1 <= c <= 9:
                T[s][c] = v

    return T


def run_one_trial(args: tuple) -> dict:
    """Run one reduction trial. Called by multiprocessing pool.

    Args:
        args: (world, n_steps, seed_cells, trial_idx, rng_seed)

    Returns:
        dict with metrics + trial metadata
    """
    world, n_steps, seed_cells, trial_idx, rng_seed = args
    random.seed(rng_seed)

    C = world['C']
    G = world['G']
    HAR = world['HAR']
    C_set = set(C)

    # Initialize
    T = make_seed_table(C, G, HAR, seed_cells)
    best_obj = _fast_objective(T, C, G, HAR, C_set)
    best_T = [row[:] for row in T]

    # Greedy random descent
    for step in range(n_steps):
        # Pick random non-padded cell
        s = random.randint(1, 9)
        c = random.randint(1, 9)
        old_v = T[s][c]

        # Bias: with prob 0.4, propose HAR (attractor bias)
        if random.random() < 0.4:
            new_v = HAR
        else:
            new_v = random.randint(1, 9)

        if new_v == old_v:
            continue

        T[s][c] = new_v
        new_obj = _fast_objective(T, C, G, HAR, C_set)

        if new_obj >= best_obj:
            best_obj = new_obj
            best_T = [row[:] for row in T]
        else:
            T[s][c] = old_v  # revert

    # Final full scoring on best table
    metrics = score_metrics(best_T, C, G, HAR)
    metrics['trial'] = trial_idx
    return metrics


def _classify_trial(m: dict, HAR_mass_thresh: float = 0.55,
                    gate_thresh: float = 0.85,
                    G_stay_thresh: float = 0.12,
                    order_thresh: float = 0.30) -> str:
    """Classify a trial result into one of three classes.

    Three-class landscape (sprint4 THREE_CLASS_LANDSCAPE.md):
      Oracle:      freely reached by gradient descent (high HAR_mass, looser gate)
      Gate-strong: strong one-way gate (C closed), G drains to attractor
      TSML-like:   gate-strong + order crystallized (high order_align + HAR_mass)

    Note: Uses G_stay (G→G fraction) instead of G_reach (G→C fraction).
    G_stay is calibrated per-base naturally: near-zero means G drains fully to C.
    """
    gate_ok    = m['gate_score'] >= gate_thresh
    g_stay_ok  = m.get('G_stay', 1.0) <= G_stay_thresh
    har_ok     = m['HAR_mass'] >= HAR_mass_thresh
    order_ok   = m['order_align'] >= order_thresh

    if gate_ok and g_stay_ok and har_ok and order_ok:
        return 'TSML-like'
    elif gate_ok and g_stay_ok:
        return 'Gate-strong'
    elif har_ok:
        return 'Oracle'
    else:
        return 'Other'


# ═══════════════════════════════════════════════════════════════════════════════
#  PARALLEL RUNNER
# ═══════════════════════════════════════════════════════════════════════════════

def run_atlas_job(b: int, n_trials: int, n_steps: int,
                  seeded: bool = False,
                  n_workers: Optional[int] = None) -> dict:
    """Run full atlas job for base b.

    Args:
        b:        Semiprime base
        n_trials: Number of reduction trials
        n_steps:  Reduction steps per trial
        seeded:   If True, use known residual seed cells (base-specific)
        n_workers: CPU cores (default: all available)

    Returns:
        Results dict with metadata + per-trial results
    """
    if n_workers is None:
        n_workers = mp.cpu_count()

    print(f"\n{'='*60}")
    print(f"R16 Atlas Job 1 — Base b={b}")
    print(f"Trials={n_trials}  Steps/trial={n_steps}  "
          f"Seeded={seeded}  Workers={n_workers}")
    print(f"{'='*60}")

    # Compute world geometry
    world = compute_world(b)
    print(f"\nWorld geometry:")
    print(f"  C = {world['C']}  (φ={world['phi']})")
    print(f"  G = {world['G']}")
    print(f"  HAR = {world['HAR']}")
    print(f"  orbit_depth = {world['orbit_depth']}")
    print(f"  gate_ease   = {world['gate_ease']:.4f}")
    print(f"  grad_score  = {world['grad_score']:.4f}")
    print(f"  score       = {world['score']:.4f}  (predicted ease rank)")

    # Determine seed cells for seeded mode
    seed_cells = None
    if seeded:
        if b == 10:
            seed_cells = B10_SEED_CELLS
            print(f"  Seed: b=10 BHML residual ({len(seed_cells)} cells)")
        elif b == 14:
            seed_cells = B14_SEED_CELLS
            print(f"  Seed: b=14 residual ({len(seed_cells)} cells)")
        else:
            # General: bias HAR-adjacent max(s,c) cells
            seed_cells = _derive_seed_cells(world)
            print(f"  Seed: derived max(s,c) cells ({len(seed_cells)} cells)")

    # Build task list
    base_seed = int(time.time())
    tasks = [
        (world, n_steps, seed_cells, i, base_seed + i)
        for i in range(n_trials)
    ]

    # Run in parallel
    t0 = time.time()
    print(f"\nRunning {n_trials} trials on {n_workers} cores...")

    if n_workers == 1:
        results = [run_one_trial(t) for t in tasks]
    else:
        chunksize = max(1, n_trials // (n_workers * 4))
        with mp.Pool(n_workers) as pool:
            results = list(pool.imap_unordered(
                run_one_trial, tasks, chunksize=chunksize))

    elapsed = time.time() - t0
    print(f"Done in {elapsed:.1f}s ({elapsed/n_trials*1000:.1f}ms/trial)")

    # Classify trials
    classes = [_classify_trial(r) for r in results]
    class_counts = {c: classes.count(c)
                    for c in ['TSML-like', 'Gate-strong', 'Oracle', 'Other']}

    # Summary statistics
    def stat(key):
        vals = [r[key] for r in results]
        return {
            'mean': round(float(np.mean(vals)), 4),
            'std':  round(float(np.std(vals)), 4),
            'max':  round(float(np.max(vals)), 4),
            'min':  round(float(np.min(vals)), 4),
        }

    print(f"\n{'─'*60}")
    print(f"Results summary (b={b}, {n_trials} trials):")
    print(f"{'─'*60}")
    for cls, cnt in class_counts.items():
        pct = 100 * cnt / n_trials
        print(f"  {cls:12s}: {cnt:5d}  ({pct:5.1f}%)")
    print(f"{'─'*60}")
    print(f"  HAR_mass  : mean={stat('HAR_mass')['mean']:.4f}  "
          f"max={stat('HAR_mass')['max']:.4f}")
    print(f"  gate_score: mean={stat('gate_score')['mean']:.4f}  "
          f"max={stat('gate_score')['max']:.4f}")
    print(f"  gap       : mean={stat('gap')['mean']:.4f}  "
          f"max={stat('gap')['max']:.4f}")
    print(f"  G_stay    : mean={stat('G_stay')['mean']:.4f}  "
          f"min={stat('G_stay')['min']:.4f}  "
          f"(0=G drains fully to C; calibrated per |G|)")
    print(f"  order_align: mean={stat('order_align')['mean']:.4f}  "
          f"max={stat('order_align')['max']:.4f}")

    # Best TSML-like trial (if any)
    tsml_results = [r for r, c in zip(results, classes) if c == 'TSML-like']
    best_tsml = None
    if tsml_results:
        best_tsml = max(tsml_results, key=lambda r: r['HAR_mass'])
        print(f"\n  Best TSML-like: HAR_mass={best_tsml['HAR_mass']:.4f}  "
              f"gate={best_tsml['gate_score']:.4f}  "
              f"gap={best_tsml['gap']:.4f}  "
              f"order={best_tsml['order_align']:.4f}")

    # Assemble output
    output = {
        'b': b,
        'n_trials': n_trials,
        'n_steps': n_steps,
        'seeded': seeded,
        'n_workers': n_workers,
        'elapsed_s': round(elapsed, 2),
        'world': {k: v for k, v in world.items() if k != 'order_seed'},
        'class_counts': class_counts,
        'tsml_like_rate': round(class_counts['TSML-like'] / n_trials, 4),
        'gate_strong_rate': round(class_counts['Gate-strong'] / n_trials, 4),
        'oracle_rate': round(class_counts['Oracle'] / n_trials, 4),
        'stats': {key: stat(key)
                  for key in ['HAR_mass', 'gate_score', 'gap',
                               'G_reach', 'G_stay', 'order_align', 'objective']},
        'best_tsml': best_tsml,
        'results': results,
    }

    return output


def _derive_seed_cells(world: dict) -> Dict[Tuple[int,int], int]:
    """Derive seed cells for a new base: HAR-row and HAR-column biases.

    For bases without a known residual, use the max(s,c) endpoint for
    cells where max(s,c) is consistent with HAR being the attractor.
    Strategy: seed the HAR row (T[HAR][c] = HAR for all c ∈ G)
    and seed cells where max(s,c) == HAR.
    """
    HAR = world['HAR']
    G = world['G']
    seed = {}
    # Seed: G-rows → HAR (G can always flow toward HAR)
    for s in G:
        for c in range(1, 10):
            seed[(s, c)] = HAR
    # Seed: cells where max(s,c) == HAR
    for s in range(1, 10):
        for c in range(1, 10):
            if max(s, c) == HAR:
                seed[(s, c)] = HAR
    return seed


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='R16 Atlas Job 1: Semiprime reduction survey')
    parser.add_argument('--b', type=int, default=55,
                        help='Semiprime base (default: 55)')
    parser.add_argument('--n_start', type=int, default=10000,
                        help='Number of reduction trials (default: 10000)')
    parser.add_argument('--n_steps', type=int, default=100,
                        help='Reduction steps per trial (default: 100)')
    parser.add_argument('--seeded', action='store_true',
                        help='Use seeded reduction (residual pre-alignment)')
    parser.add_argument('--workers', type=int, default=None,
                        help='Number of worker processes (default: all CPUs)')
    parser.add_argument('--output', type=str, default=None,
                        help='Output JSON path (default: results/reduction_b{b}_N{n}.json)')
    args = parser.parse_args()

    # Output path
    if args.output:
        out_path = args.output
    else:
        os.makedirs('results', exist_ok=True)
        suffix = '_seeded' if args.seeded else ''
        out_path = f'results/reduction_b{args.b}_N{args.n_start}{suffix}.json'

    # Run job
    output = run_atlas_job(
        b=args.b,
        n_trials=args.n_start,
        n_steps=args.n_steps,
        seeded=args.seeded,
        n_workers=args.workers,
    )

    # Save results
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    print(f"\n✓ Results saved → {out_path}")
    print(f"  Next: python r16_job3_clustering.py --input {out_path}")

    # Quick atlas law check
    world = output['world']
    rate = output['tsml_like_rate']
    print(f"\n── Atlas Law Check (b={args.b}) ──────────────────────────")
    print(f"  Construction score = {world['score']:.3f}  "
          f"(> 7.057 → easier than b=15)")
    print(f"  Random TSML-like rate = {rate*100:.1f}%  "
          f"(b=15: 78.6%, b=10: 4.0%)")
    if world['score'] > 7.057 and rate > 0.786:
        print("  ✓ Prediction confirmed: easier than b=15")
    elif world['score'] > 7.057 and rate > 0.04:
        print("  ✓ Easier than b=10; prediction partially confirmed")
    elif rate == 0.0:
        print("  → TSML-like not found randomly; try --seeded mode")


if __name__ == '__main__':
    mp.freeze_support()
    main()
