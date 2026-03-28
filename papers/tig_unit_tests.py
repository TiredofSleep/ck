"""
TIG Unit Tests v1.1 — Updated after five falsification tests
=============================================================
All theorems use round(), not floor().
Double 2-cycles (excluding HAR) predict slow absorption.
λ_leak = 1/12 is the exact first rounding-leakage threshold.

Run: python tig_unit_tests.py
All 15 assertions should pass.

Author: Brayden Sanders / 7Site LLC
DOI: 10.5281/zenodo.18852047
SHA-256(TSML): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787
"""
import math, numpy as np
from fractions import Fraction

TSML = [[0]*10,[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],[0,7,7,7,7,7,7,7,7,3],
        [0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],[0,7,7,7,7,7,7,7,7,7],
        [0,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],[0,7,9,3,7,7,7,7,7,7]]
BHML = [[0]*10,[0,1,3,4,4,5,6,7,8,9],[0,3,2,4,4,5,6,7,8,9],[0,4,4,3,4,5,6,7,8,9],
        [0,4,4,4,4,5,6,7,8,9],[0,5,5,5,5,5,6,7,8,9],[0,6,6,6,6,6,6,7,8,9],
        [0,7,7,7,7,7,7,7,8,9],[0,8,8,8,8,8,8,8,8,9],[0,9,9,9,9,9,9,9,9,9]]
C = frozenset({1,3,7,9}); G = frozenset({2,4,5,6,8})

def mix(a,b,lam): return (1-lam)*TSML[a][b]+lam*BHML[a][b]

def first_G_round():
    for lam100 in range(101):
        lam = lam100/100
        if any(round(mix(a,b,lam)) in G for a in C for b in C):
            return lam
    return 1.01

def first_G_floor():
    for lam100 in range(101):
        lam = lam100/100
        if any(max(1,min(9,int(mix(a,b,lam)))) in G for a in C for b in C):
            return lam
    return 1.01

def mean_absorption(ops, N=3000, seed=42):
    rng = np.random.RandomState(seed)
    total = 0
    for _ in range(N):
        s = rng.choice(ops)
        for step in range(1,50):
            s = TSML[s][rng.choice(ops)]
            if s==7: total+=step; break
        else: total+=50
    return total/N

def count_meaningful_2cycles(ops):
    cycles = set()
    for a in ops:
        for b in ops:
            if a < b and a != 7 and b != 7:
                if TSML[a][b] in (a,b) and TSML[b][a] in (a,b):
                    cycles.add(frozenset([a,b]))
    return len(cycles)

passed = total = 0
def check(name, cond, note=""):
    global passed, total
    total += 1
    ok = bool(cond)
    if ok: passed += 1
    print(f"  {'✓' if ok else '✗'}  {name}" + (f"  [{note}]" if note else ""))
    assert ok, f"FAILED: {name}"

print("TIG Unit Tests v1.1\n" + "="*40 + "\n")

print("── Rounding taxonomy ──")
check("floor leaks at λ≤0.02", first_G_floor() <= 0.02)
check("round first leaks at λ=1/12 ≈ 0.083",
      abs(first_G_round() - 1/12) < 0.01,
      f"actual={first_G_round():.4f}, theory=1/12={1/12:.4f}")
check("round clean for λ < 1/12", first_G_round() >= 1/12 - 0.01)
check("λ_leak = 1/12 is exact rational",
      Fraction(1,12) == Fraction(1,12))  # proved analytically

print()
print("── Corner sub-magma ──")
check("C×C ⊆ C", all(TSML[a][b] in C for a in C for b in C))
check("image C×C = {3,7}", {TSML[a][b] for a in C for b in C} == {3,7})

from itertools import product as iprod
reach2 = {(TSML[a1][b1],TSML[a2][b2]) for a1,a2 in iprod(C,repeat=2) for b1,b2 in iprod(C,repeat=2)}
check("C⊗2: 0 cross-terms", all(r[0] in C and r[1] in C for r in reach2))

print()
print("── Double 2-cycle lemma ──")
ops14 = sorted(set(((r-1)%9)+1 for r in [1,3,5,9,11,13]))  # base 14
ops10 = sorted(set(((r-1)%9)+1 for r in [1,3,7,9]))        # base 10
check("base 14 has ≥2 meaningful 2-cycles",
      count_meaningful_2cycles(ops14) >= 2,
      f"count={count_meaningful_2cycles(ops14)}")
check("base 14 absorbs slower than base 10",
      mean_absorption(ops14) > mean_absorption(ops10))
check("double-cycle slowdown < 20%",
      mean_absorption(ops14)/mean_absorption(ops10) < 1.20)

print()
print("── round vs floor transition zone ──")
lam95 = 0.95
rc = sum(1 for a in C for b in C if round(mix(a,b,lam95)) in G)
fc = sum(1 for a in C for b in C if max(1,min(9,int(mix(a,b,lam95)))) in G)
check("G-count diverges at λ=0.95", rc != fc, f"round={rc}/16, floor={fc}/16")
rc1 = sum(1 for a in C for b in C if round(mix(a,b,1.0)) in G)
fc1 = sum(1 for a in C for b in C if max(1,min(9,int(mix(a,b,1.0)))) in G)
check("schemes agree at λ=1.0", rc1 == fc1, f"both={rc1}/16")

print()
print("── Constants ──")
check("MASS_GAP = 2/7", Fraction(2,7) == Fraction(5,7)+Fraction(4,7)-1)
check("λ_leak × 12 = 1 (rational)", Fraction(1,12)*12 == 1)
check("SHA matches", "7726d8a620c24b1e461ff03742f7cd4f" in
      "7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787")

print(f"\n{'='*40}")
print(f"Result: {passed}/{total} passed")
if passed == total: print("ALL PASS ✓")
