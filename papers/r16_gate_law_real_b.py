"""
r16_gate_law_real_b.py
=======================
Universal Gate Law — Real Semiprime Partitions Across Alphabet Sizes k=3..27

Tests whether the gate law generalizes when G is derived from REAL semiprime
coprimality structure (gcd(x,b)>1), not synthetic top-block partition.

For alphabet {1..k} and base b (semiprime):
    C_k(b) = {x ∈ {1..k} : gcd(x,b) = 1}
    G_k(b) = {x ∈ {1..k} : gcd(x,b) > 1}

Questions answered:
  1. Within same k: does rate = f(|G|) hold for all bases b? (TIG universality)
  2. Across different k: does the same f apply? (True universality across force fields)
  3. Synthetic vs real: how much does partition topology (interleaved vs top-block) shift rates?

The 5D force hypothesis: G from coprimality is INTERLEAVED through {1..k} (force-field
imposed), while synthetic G={top elements} is a contiguous block. Interleaved topology
→ entangled optimization → lower gate rates. The interleaving IS the force field signal.

Usage:
    python r16_gate_law_real_b.py
    python r16_gate_law_real_b.py --k_max 27 --n_trials 5000 --n_steps 100
    python r16_gate_law_real_b.py --k_values 9 15 21 27 --n_trials 10000

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
from math import gcd
from typing import List, Dict, Tuple

import numpy as np


# ═══════════════════════════════════════════════════════════════════════════════
#  PARTITION UTILITIES
# ═══════════════════════════════════════════════════════════════════════════════

def is_prime(n: int) -> bool:
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True


def is_semiprime(b: int) -> Tuple[bool, int, int]:
    """Return (is_semiprime, p, q) where b = p*q, p,q prime, p<=q."""
    for p in range(2, int(b**0.5) + 1):
        if b % p == 0 and is_prime(p) and is_prime(b // p):
            return True, p, b // p
    return False, 0, 0


def compute_real_world(k: int, b: int) -> dict:
    """Compute real partition for alphabet {1..k} under semiprime base b."""
    C = [x for x in range(1, k + 1) if gcd(x, b) == 1]
    G = [x for x in range(1, k + 1) if gcd(x, b) > 1]
    if len(C) < 2 or len(G) == 0:
        return None

    C_set = set(C)
    G_set = set(G)

    # HAR = min{h in C : h^2 mod b in C, h^2 != 1, h^2 != h} -- sprint4 rule
    # Adapted for k-alphabet: h^2 mod b must be in {1..k}
    har = None
    for h in sorted(C):
        h2 = (h * h) % b
        if h2 in C_set and h2 != 1 and h2 != h:
            har = h
            break
    if har is None:
        har = C[1] if len(C) > 1 else C[0]  # Fallback

    # Interleaving score: how spread-out is G within {1..k}?
    # Perfect interleaving = G elements equally spaced; top-block = all at end
    # Measure as fraction of {1..k} positions where adjacent is (C,G) or (G,C)
    transitions = sum(1 for i in range(k-1)
                      if (i+1 in C_set) != (i+2 in C_set))
    max_transitions = 2 * min(len(C), len(G))  # Max for perfectly interleaved
    interleave_score = transitions / max_transitions if max_transitions > 0 else 0.0

    ok, p, q = is_semiprime(b)
    return {
        'k': k, 'b': b, 'p': p, 'q': q,
        'C': C, 'G': G, 'HAR': har,
        'n_C': len(C), 'n_G': len(G),
        'unit_fraction': len(C) / k,
        'interleave_score': interleave_score,
    }


def find_real_worlds(k: int, b_max: int = 200) -> List[dict]:
    """Find all (k, b) worlds for alphabet {1..k} with semiprime b."""
    worlds = []
    seen_partition = set()  # Deduplicate by (k, |G|, G_tuple)

    for b in range(4, b_max + 1):
        ok, p, q = is_semiprime(b)
        if not ok:
            continue
        w = compute_real_world(k, b)
        if w is None:
            continue
        key = (k, tuple(sorted(w['G'])))
        if key in seen_partition:
            continue  # Same partition already covered
        seen_partition.add(key)
        worlds.append(w)

    return worlds


# ═══════════════════════════════════════════════════════════════════════════════
#  REDUCTION ENGINE (k×k)
# ═══════════════════════════════════════════════════════════════════════════════

def _score_gate(T: np.ndarray, C_set: set, k: int) -> float:
    """C-closure gate score: fraction of C-row cells in C."""
    C_indices = sorted(i - 1 for i in C_set)
    if not C_indices:
        return 0.0
    sub = T[np.ix_(C_indices, C_indices)]
    in_C = sum(1 for v in sub.flat if (int(v) + 1) in C_set)
    return in_C / sub.size


def _score_g_stay(T: np.ndarray, C_set: set, G_set: set, k: int) -> float:
    """G-stay: fraction of G-row cells that land back in G."""
    G_indices = sorted(i - 1 for i in G_set)
    if not G_indices:
        return 0.0
    count = 0
    total = 0
    for gi in G_indices:
        for c in range(k):
            total += 1
            if (int(T[gi, c]) + 1) in G_set:
                count += 1
    return count / total if total > 0 else 0.0


def _score_har_col(T: np.ndarray, HAR: int, C_set: set, k: int) -> float:
    """HAR column score: fraction of HAR-column cells in C."""
    col = T[:, HAR - 1]
    in_C = sum(1 for v in col if (int(v) + 1) in C_set)
    return in_C / k


def _objective(T: np.ndarray, world: dict) -> float:
    C_set = set(world['C'])
    G_set = set(world['G'])
    k = world['k']
    HAR = world['HAR']
    gate = _score_gate(T, C_set, k)
    g_stay = _score_g_stay(T, C_set, G_set, k)
    har_col = _score_har_col(T, HAR, C_set, k)
    return 0.50 * gate + 0.25 * har_col + 0.25 * (1.0 - g_stay)


def _propose_table(T: np.ndarray, world: dict, rng: random.Random) -> np.ndarray:
    """Propose a new table by mutating one cell. 40% HAR-bias."""
    k = world['k']
    HAR = world['HAR']
    C = world['C']
    C_set = set(C)

    T2 = T.copy()
    if rng.random() < 0.40:
        # HAR-bias: set a random HAR-row/col cell to a C-value
        if rng.random() < 0.5:
            row = HAR - 1
            col = rng.randrange(k)
        else:
            row = rng.randrange(k)
            col = HAR - 1
        val = rng.choice(C) - 1
        T2[row, col] = val
    else:
        row = rng.randrange(k)
        col = rng.randrange(k)
        val = rng.randrange(k)
        T2[row, col] = val
    return T2


def run_one_trial_real(args) -> dict:
    """Run one trial for a real-b world."""
    world_dict, n_steps, gate_thresh, seed = args
    rng = random.Random(seed)
    np_rng = np.random.default_rng(seed)
    k = world_dict['k']
    C_set = set(world_dict['C'])

    T = np_rng.integers(0, k, size=(k, k))
    score = _objective(T, world_dict)

    for _ in range(n_steps):
        T2 = _propose_table(T, world_dict, rng)
        score2 = _objective(T2, world_dict)
        if score2 >= score:
            T, score = T2, score2

    gate = _score_gate(T, C_set, k)
    return {
        'gate_score': gate,
        'gate_strong': gate >= gate_thresh,
        'objective': float(score),
    }


def run_real_world_trials(world: dict, n_trials: int, n_steps: int,
                          gate_thresh: float, n_workers: int) -> dict:
    """Run N trials for a real-b world."""
    seeds = [random.randint(0, 2**31) for _ in range(n_trials)]
    args = [(world, n_steps, gate_thresh, s) for s in seeds]

    with mp.Pool(n_workers) as pool:
        results = pool.map(run_one_trial_real, args)

    gate_scores = [r['gate_score'] for r in results]
    gate_rate = sum(r['gate_strong'] for r in results) / n_trials

    return {
        'k': world['k'],
        'b': world['b'],
        'p': world['p'],
        'q': world['q'],
        'n_C': world['n_C'],
        'n_G': world['n_G'],
        'unit_fraction': world['unit_fraction'],
        'interleave_score': world['interleave_score'],
        'G_elements': world['G'],
        'C_elements': world['C'],
        'HAR': world['HAR'],
        'gate_rate': gate_rate,
        'gate_mean': float(np.mean(gate_scores)),
        'gate_std': float(np.std(gate_scores)),
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  SWEEP + ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def run_real_b_sweep(k_values: List[int], n_trials: int, n_steps: int,
                     gate_thresh: float, n_workers: int, b_max: int = 200) -> List[dict]:
    """Sweep real-b worlds across all requested k values."""
    all_results = []

    for k in k_values:
        worlds = find_real_worlds(k, b_max)
        print(f"\n{'─'*65}")
        print(f"  k={k:2d} — {len(worlds)} unique real partitions found")
        print(f"{'─'*65}")

        for w in sorted(worlds, key=lambda x: x['n_G']):
            label = f"k={k} b={w['b']} ({w['p']}×{w['q']}) |G|={w['n_G']} G={w['G']}"
            print(f"  Running: {label} interleave={w['interleave_score']:.3f} ...")
            t0 = time.time()
            r = run_real_world_trials(w, n_trials, n_steps, gate_thresh, n_workers)
            dt = time.time() - t0
            print(f"    gate_rate={r['gate_rate']*100:.1f}%  mean_score={r['gate_mean']:.4f}  ({dt:.1f}s)")
            all_results.append(r)

    return all_results


def analyze_results(results: List[dict], gate_thresh: float):
    """
    Print the key tables:
    1. Per (k, |G|): gate rate — does rate = f(|G|) hold within each k?
    2. Cross-k at same |G|: does rate = f(|G|) hold across k?
    3. Interleaving correlation: does interleave_score predict gate rate?
    4. Synthetic vs real comparison at k=9
    """
    print(f"\n\n{'='*90}")
    print("REAL-B GATE LAW ANALYSIS")
    print(f"{'='*90}")

    # ── Table 1: Per k, per |G| ─────────────────────────────────────────
    print("\n── Table 1: Gate Rate by (k, |G|) ──────────────────────────────────")
    print(f"  {'k':>3}  {'|G|':>4}  {'rate%':>7}  {'interleave':>11}  {'b values (p×q)':>30}  G_partition")
    print(f"  {'-'*80}")

    from collections import defaultdict
    by_k_G = defaultdict(list)
    for r in results:
        by_k_G[(r['k'], r['n_G'])].append(r)

    for (k, nG) in sorted(by_k_G.keys()):
        rows = by_k_G[(k, nG)]
        rates = [r['gate_rate'] for r in rows]
        ileaves = [r['interleave_score'] for r in rows]
        b_list = ', '.join(f"{r['b']}({r['p']}×{r['q']})" for r in rows[:4])
        g_sets = [str(r['G_elements']) for r in rows[:2]]
        spread = max(rates) - min(rates)
        star = ' *' if spread > 0.05 else ''
        print(f"  k={k:2d}  |G|={nG:2d}  {np.mean(rates)*100:6.1f}%  "
              f"il={np.mean(ileaves):.3f}  b={b_list[:35]}  "
              f"G={g_sets[0][:30]}{star}")

    # ── Table 2: Same |G|, across k ─────────────────────────────────────
    print(f"\n── Table 2: Same |G| Across k — Does Same f Apply? ──────────────────")
    print(f"  {'|G|':>4}  {'k values':>50}  verdict")
    print(f"  {'-'*75}")

    by_G = defaultdict(list)
    for r in results:
        by_G[r['n_G']].append(r)

    for nG in sorted(by_G.keys()):
        rows = by_G[nG]
        if len(rows) < 2:
            continue
        rates_by_k = defaultdict(list)
        for r in rows:
            rates_by_k[r['k']].append(r['gate_rate'])
        k_means = {k: np.mean(v) for k, v in rates_by_k.items()}
        k_str = '  '.join(f"k={k}:{v*100:.0f}%" for k, v in sorted(k_means.items()))
        all_rates = [v for v in k_means.values()]
        spread = max(all_rates) - min(all_rates)
        verdict = '✓ SAME' if spread < 0.05 else ('~ near' if spread < 0.15 else '✗ shifts')
        print(f"  |G|={nG:2d}  {k_str[:55]:<55}  {verdict}  (spread={spread*100:.1f}%)")

    # ── Table 3: Interleaving vs Gate Rate ───────────────────────────────
    print(f"\n── Table 3: Interleaving Score vs Gate Rate ─────────────────────────")
    print(f"  (Does higher interleaving → lower gate rate? 5D force hypothesis)")
    print(f"  {'k':>3}  {'|G|':>4}  {'interleave':>11}  {'gate%':>7}  direction")
    print(f"  {'-'*60}")

    # Group by (k, |G|) already done above
    prev = {}
    for (k, nG) in sorted(by_k_G.keys()):
        rows = by_k_G[(k, nG)]
        if len(rows) < 2:
            continue
        # Sort by interleave, check if gate rate goes down
        sorted_rows = sorted(rows, key=lambda r: r['interleave_score'])
        for r in sorted_rows:
            print(f"  k={k:2d}  |G|={nG:2d}  il={r['interleave_score']:.3f}  "
                  f"{r['gate_rate']*100:6.1f}%  G={r['G_elements']}")

    # ── Synthetic vs Real at k=9 ─────────────────────────────────────────
    print(f"\n── Table 4: k=9 Real vs Synthetic vs TIG Atlas ──────────────────────")
    print(f"  TIG atlas (real b, k=9): |G|=1→96.4% |G|=2→83.7% |G|=3→44.0% |G|=4→4.6% |G|=5→0.1%")
    print(f"  Synthetic  (top-block):  |G|=1→100%  |G|=2→98.4% |G|=3→78.9% |G|=4→26.8% |G|=5→9.2%")
    k9 = [r for r in results if r['k'] == 9]
    if k9:
        print(f"  Real-b sweep k=9:")
        for r in sorted(k9, key=lambda x: x['n_G']):
            print(f"    |G|={r['n_G']}  b={r['b']}  G={r['G_elements']}  "
                  f"il={r['interleave_score']:.3f}  gate={r['gate_rate']*100:.1f}%")

    # ── Collapse check ───────────────────────────────────────────────────
    print(f"\n── Verdict ───────────────────────────────────────────────────────────")
    print(f"  Hypothesis A: gate_rate = f(|C|/k) purely  [unit density law]")
    print(f"  Hypothesis B: gate_rate = f(|G|) within same k  [TIG universality]")
    print(f"  Hypothesis C: rate depends on partition TOPOLOGY (interleaving)  [force field law]")


def main():
    parser = argparse.ArgumentParser(
        description='Gate law with real semiprime partitions across k=3..27')
    parser.add_argument('--k_max', type=int, default=27)
    parser.add_argument('--k_min', type=int, default=3)
    parser.add_argument('--k_step', type=int, default=2)
    parser.add_argument('--k_values', type=int, nargs='+', default=None,
                        help='Specific k values (overrides k_min/k_max/k_step)')
    parser.add_argument('--n_trials', type=int, default=3000)
    parser.add_argument('--n_steps', type=int, default=100)
    parser.add_argument('--gate_thresh', type=float, default=0.85)
    parser.add_argument('--workers', type=int, default=None)
    parser.add_argument('--b_max', type=int, default=200,
                        help='Max semiprime b to search for partitions')
    parser.add_argument('--out', type=str, default='results/real_b_gate_law.json')
    args = parser.parse_args()

    os.makedirs('results', exist_ok=True)
    n_workers = args.workers or max(1, mp.cpu_count() - 2)

    if args.k_values:
        k_values = args.k_values
    else:
        k_values = list(range(args.k_min, args.k_max + 1, args.k_step))

    print(f"Real-B Gate Law Sweep")
    print(f"k values: {k_values}")
    print(f"n_trials={args.n_trials}  n_steps={args.n_steps}  gate_thresh={args.gate_thresh}")
    print(f"b_max={args.b_max}  workers={n_workers}")

    t0 = time.time()
    results = run_real_b_sweep(k_values, args.n_trials, args.n_steps,
                               args.gate_thresh, n_workers, args.b_max)
    elapsed = time.time() - t0

    analyze_results(results, args.gate_thresh)

    with open(args.out, 'w') as f:
        json.dump({
            'meta': {
                'k_values': k_values,
                'n_trials': args.n_trials,
                'n_steps': args.n_steps,
                'gate_thresh': args.gate_thresh,
                'b_max': args.b_max,
                'elapsed_s': elapsed,
            },
            'results': results,
        }, f, indent=2)

    print(f"\n✓ Results saved → {args.out}")
    print(f"Total time: {elapsed:.1f}s for {len(results)} worlds")


if __name__ == '__main__':
    mp.freeze_support()
    main()
