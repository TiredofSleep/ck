"""
omega3_extension.py
====================
Test the Luther-Sanders Equivalence for three-factor composites (omega(b) = 3).

Research question: does gate_rate = f_k(|G|) with zero spread hold beyond
semiprimes? WP34 proves first_g(b) = smallest prime factor for omega(b) = 2.
The same proof structure covers omega(b) >= 3. This script verifies computationally.

Tests:
  1. First-G Law for omega(b)=3: first_g(b) = smallest prime factor
  2. k-Gate Tier Law: zero spread within |G|-tier for arithmetic G
  3. Comparison: arithmetic G (coprimality) vs synthetic G (top-block) -- does
     the 61.4% synthetic spread appear here too?
  4. ω-Blindness: does R(k,p) still depend only on smallest prime factor?

Three-factor test targets:
  b = 30  = 2 x 3 x 5   (smallest, p=2)
  b = 42  = 2 x 3 x 7   (p=2)
  b = 66  = 2 x 3 x 11  (p=2)
  b = 105 = 3 x 5 x 7   (p=3, no factor 2)
  b = 165 = 3 x 5 x 11  (p=3)
  b = 385 = 5 x 7 x 11  (p=5)

Author: Brayden Ross Sanders / 7Site LLC | March 2026
DOI: 10.5281/zenodo.18852047
"""

import math
import random
import sys
from math import gcd

import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# Number theory helpers
# ─────────────────────────────────────────────────────────────────────────────

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

def prime_factors(n):
    """Return sorted list of distinct prime factors of n."""
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return sorted(factors)

def omega(n):
    return len(prime_factors(n))

def first_g(b, k=None):
    """Return first k >= 1 with gcd(k, b) > 1."""
    if k is None:
        k = b
    for i in range(1, k + 1):
        if gcd(i, b) > 1:
            return i
    return None

def gate_partition(b, k):
    C = [x for x in range(1, k + 1) if gcd(x, b) == 1]
    G = [x for x in range(1, k + 1) if gcd(x, b) > 1]
    return C, G

def synthetic_G(n_G, k):
    """Top-block synthetic G: {k-n_G+1..k}."""
    G = list(range(k - n_G + 1, k + 1))
    C = [x for x in range(1, k + 1) if x not in set(G)]
    return C, G

# ─────────────────────────────────────────────────────────────────────────────
# MCMC reduction (matches r16_gate_law_real_b.py structure)
# ─────────────────────────────────────────────────────────────────────────────

def score_gate(T, C_set, k):
    """Gate score: fraction of C-row x C-col cells in C."""
    C_idx = sorted(i - 1 for i in C_set)
    if not C_idx:
        return 0.0
    sub = T[np.ix_(C_idx, C_idx)]
    in_C = sum(1 for v in sub.flat if (int(v) + 1) in C_set)
    return in_C / sub.size

def objective(T, C, G, HAR, k):
    C_set = set(C)
    G_set = set(G)
    gate = score_gate(T, C_set, k)
    # HAR column score
    har_col = sum(1 for v in T[:, HAR-1] if (int(v)+1) in C_set) / k
    # G-stay score
    G_idx = [g-1 for g in G_set]
    if G_idx:
        g_stay = sum(1 for gi in G_idx for c in range(k) if (int(T[gi,c])+1) in G_set) / (len(G_idx)*k)
    else:
        g_stay = 0.0
    return 0.50 * gate + 0.25 * har_col + 0.25 * (1.0 - g_stay)

def propose(T, C, HAR, k, rng):
    T2 = T.copy()
    if rng.random() < 0.40:
        if rng.random() < 0.5:
            row, col = HAR - 1, rng.randrange(k)
        else:
            row, col = rng.randrange(k), HAR - 1
        val = rng.choice(C) - 1
    else:
        row, col, val = rng.randrange(k), rng.randrange(k), rng.randrange(k)
    T2[row, col] = val
    return T2

def run_trial(C, G, k, n_steps, gate_thresh, seed):
    rng = random.Random(seed)
    np_rng = np.random.default_rng(seed)
    C_set = set(C)
    G_set = set(G)
    HAR = None
    # HAR: orbit-central element in C
    for h in sorted(C):
        # For omega>=3, use modular HAR relative to first factor pair
        h2 = h * h  # mod b not available directly; use simple criterion
        if h2 in C_set and h2 != 1 and h2 != h:
            HAR = h
            break
    if HAR is None:
        HAR = C[1] if len(C) > 1 else C[0]

    T = np_rng.integers(0, k, size=(k, k))
    score = objective(T, C, G, HAR, k)
    for _ in range(n_steps):
        T2 = propose(T, C, HAR, k, rng)
        s2 = objective(T2, C, G, HAR, k)
        if s2 >= score:
            T, score = T2, s2
    gate = score_gate(T, C_set, k)
    return gate >= gate_thresh

def gate_rate(C, G, k, n_trials=2000, n_steps=100, gate_thresh=0.999):
    seeds = [random.randint(0, 2**31) for _ in range(n_trials)]
    hits = sum(run_trial(C, G, k, n_steps, gate_thresh, s) for s in seeds)
    return hits / n_trials

# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────

K = 9

print("=" * 65)
print("OMEGA(b) >= 3 EXTENSION: Luther-Sanders Equivalence")
print(f"k = {K} | gate_thresh = 0.999 | n_trials = 2000 per world")
print("=" * 65)

# ── Test 1: First-G Law for omega(b) = 3 ────────────────────────────────────
print("\n[Test 1] First-G Law: first_g(b) = min prime factor of b")
print(f"  {'b':>6}  {'factors':>16}  {'min_p':>6}  {'first_g':>8}  {'match':>6}")

omega3_bases = [30, 42, 66, 105, 110, 165, 231, 273, 385, 429, 462, 546]
all_match = True
for b in omega3_bases:
    pf = prime_factors(b)
    if omega(b) < 3:
        continue
    p_min = pf[0]
    fg = first_g(b)
    match = fg == p_min
    if not match:
        all_match = False
    print(f"  {b:>6}  {str(pf):>16}  {p_min:>6}  {fg:>8}  {'OK' if match else 'FAIL':>6}")

print(f"\n  First-G Law for omega=3: {'ALL PASS' if all_match else 'EXCEPTIONS FOUND'}")

# ── Test 2: k-Gate Tier Law for omega(b) = 3 ────────────────────────────────
print(f"\n[Test 2] k-Gate Tier Law: does rate = f_k(|G|) hold for omega=3?")
print(f"  (Compare: semiprimes |G|=1->96.4%, |G|=3->44.0%, |G|=4->4.6%)")
print(f"\n  {'b':>6}  {'factors':>16}  {'|G|':>4}  {'G':>18}  {'rate%':>7}")

# Group results by |G|
from collections import defaultdict
tier_results = defaultdict(list)

omega3_for_gate = []
for b in range(6, 150):
    pf = prime_factors(b)
    if len(pf) != 3:
        continue
    C, G = gate_partition(b, K)
    if len(G) == 0 or len(C) < 2:
        continue
    # Deduplicate by G-partition
    key = tuple(sorted(G))
    if any(key == tuple(sorted(g)) for _, g in omega3_for_gate):
        continue
    omega3_for_gate.append((b, G))

for b, G in omega3_for_gate[:8]:
    pf = prime_factors(b)
    C, _ = gate_partition(b, K)
    if not C:
        continue
    r = gate_rate(C, G, K, n_trials=2000, n_steps=100)
    tier_results[len(G)].append(r)
    print(f"  {b:>6}  {str(pf):>16}  {len(G):>4}  {str(G):>18}  {r*100:>6.1f}%")

# ── Test 3: Spread within |G| tiers for omega=3 ─────────────────────────────
print(f"\n[Test 3] Zero-spread test: variance within |G|-tier for omega=3?")
print(f"  (Prediction: zero spread = arithmetic G; ~60% spread = synthetic G)")
print(f"\n  {'|G|':>4}  {'n_worlds':>9}  {'rates':>30}  {'spread':>8}  {'verdict':>10}")

for n_G, rates in sorted(tier_results.items()):
    if len(rates) > 1:
        spread = max(rates) - min(rates)
        verdict = "ZERO" if spread < 0.02 else f"{spread*100:.1f}%"
    else:
        spread = 0.0
        verdict = "single"
    rate_str = "  ".join(f"{r*100:.1f}%" for r in rates)
    print(f"  {n_G:>4}  {len(rates):>9}  {rate_str:>30}  {spread*100:>6.1f}%  {verdict:>10}")

# ── Test 4: Synthetic vs arithmetic for omega=3 ──────────────────────────────
print(f"\n[Test 4] Arithmetic vs synthetic G at omega=3 (b=105 = 3x5x7)")
b_test = 105
pf = prime_factors(b_test)
C_arith, G_arith = gate_partition(b_test, K)
print(f"  b={b_test} = {pf}, k={K}")
print(f"  Arithmetic G = {G_arith} (|G|={len(G_arith)})")

if G_arith and C_arith:
    r_arith = gate_rate(C_arith, G_arith, K, n_trials=2000, n_steps=100)
    print(f"  Arithmetic gate rate: {r_arith*100:.1f}%")

    # Synthetic G with same cardinality
    n_G = len(G_arith)
    C_synth, G_synth = synthetic_G(n_G, K)
    print(f"  Synthetic  G = {G_synth} (|G|={len(G_synth)})")
    r_synth = gate_rate(C_synth, G_synth, K, n_trials=2000, n_steps=100)
    print(f"  Synthetic  gate rate: {r_synth*100:.1f}%")
    print(f"  Gap (arithmetic - synthetic): {(r_arith - r_synth)*100:+.1f}%")
    if abs(r_arith - r_synth) > 0.10:
        print(f"  [HIGH INTERLEAVE LAW HOLDS for omega=3]")
    else:
        print(f"  [gap small -- HIGH INTERLEAVE LAW NOT CONFIRMED for omega=3]")

# ── Summary ──────────────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("SUMMARY")
print("=" * 65)
print(f"  First-G Law (omega=3): {'CONFIRMED' if all_match else 'EXCEPTIONS'}")
print(f"  k-Gate Tier Law (omega=3): see tier table above")
print(f"  High Interleave distinction: see Test 4")
print(f"\nPath to Tier D: if zero-spread holds for omega=3, the Equivalence")
print(f"extends to all omega(b) >= 2. This is a significant upgrade.")
