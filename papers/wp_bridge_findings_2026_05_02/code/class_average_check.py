"""
Average candidate invariants over σ-orbits to get class functions.
Then check what those class-averaged values mean structurally.
"""
import numpy as np
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10, SIGMA_PERMUTATION
from rademacher_search import (
    substrate_class_invariant_v1, substrate_class_invariant_v2,
    substrate_class_invariant_v3, substrate_class_invariant_v4
)

def sigma_orbit(n):
    sigma = SIGMA_PERMUTATION
    seen = []
    cur = n
    while cur not in seen:
        seen.append(cur)
        cur = int(sigma[cur])
    return seen


def class_average(invariant_fn, n):
    orbit = sigma_orbit(n)
    return sum(invariant_fn(x) for x in orbit) / len(orbit)


def class_sum(invariant_fn, n):
    orbit = sigma_orbit(n)
    return sum(invariant_fn(x) for x in orbit)


if __name__ == "__main__":
    print("=" * 70)
    print("σ-ORBIT CLASS AVERAGES OF EACH INVARIANT")
    print("=" * 70)
    
    invariants = {
        'v1: BHML period': substrate_class_invariant_v1,
        'v2: TSML-BHML asymmetry': substrate_class_invariant_v2,
        'v3: row-7 count diff': substrate_class_invariant_v3,
        'v4: signed σ-distance': substrate_class_invariant_v4,
    }
    
    # Distinct σ-orbits
    orbits_seen = set()
    orbits_list = []
    for n in range(10):
        orb = tuple(sorted(sigma_orbit(n)))
        if orb not in orbits_seen:
            orbits_seen.add(orb)
            orbits_list.append(orb)
    
    print(f"\nσ-orbits: {orbits_list}")
    
    for name, fn in invariants.items():
        print(f"\n  {name}:")
        for orb in orbits_list:
            n = orb[0]
            avg = class_average(fn, n)
            sm = class_sum(fn, n)
            print(f"    orbit {orb}: avg = {avg:+.3f}, sum = {sm:+}")
    
    print("\n" + "=" * 70)
    print("INTERPRETATION: 6-CYCLE CLASS-SUM IS THE GHYS-ANALOG TOTAL")
    print("=" * 70)
    print("\nThe 6-cycle (1,2,4,5,6,7) has classical Ghys-analog sum:")
    print("  v2: 6 + 4 + 4 + 5 - 1 + 4 = 22")
    print("\nWait — earlier I said sum was +21 over ALL 10 digits.")
    print("Let me recount.")
    
    full_sum = sum(substrate_class_invariant_v2(n) for n in range(10))
    six_cycle_sum = sum(substrate_class_invariant_v2(n) for n in [1,2,4,5,6,7])
    fixed_sum = sum(substrate_class_invariant_v2(n) for n in [0,3,8,9])
    
    print(f"\n  Sum over all 10 digits: {full_sum}")
    print(f"  Sum over 6-cycle (1,2,4,5,6,7): {six_cycle_sum}")
    print(f"  Sum over σ-fixed (0,3,8,9): {fixed_sum}")
    
    # Recompute the per-digit values for sanity
    print(f"\n  Per-digit v2:")
    for n in range(10):
        print(f"    {n}: {substrate_class_invariant_v2(n):+}")
    print(f"\n  Sum check: {sum(substrate_class_invariant_v2(n) for n in range(10))}")
    
    print("\n" + "=" * 70)
    print("CHECK: the +21 = 3×HARMONY claim")
    print("=" * 70)
    print(f"  21 = 3 × 7 = 3 × HARMONY")
    print(f"  Actual sum: {full_sum}")
    print(f"  3 × HARMONY = 21")
    print(f"  Match? {full_sum == 21}")
    
    if full_sum != 21:
        print(f"\n  Original claim was wrong. Re-examining:")
        print(f"  Sum is {full_sum}.")
        print(f"  Alternative: {full_sum} = ?")
        # Try various decompositions
        if full_sum == 22:
            print(f"  22 = 2 × 11 (eleven bumps in 22-shell?)")
            print(f"  22 = 11 × 2 (this is the wobble denominator)")
        if abs(full_sum) % 7 == 0:
            print(f"  {full_sum} = {full_sum // 7} × HARMONY")
