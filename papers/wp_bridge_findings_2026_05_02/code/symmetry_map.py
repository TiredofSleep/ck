"""
Comprehensive map of grammar-level boundary symmetries.

Test all adjacent-integer pairs (and selected non-adjacent role-boundary 
pairs) to see which ones preserve admissibility on:
  1. Each canonical grammar triple
  2. The trefoil-9 set
  3. The 4-core (broader test)

Build a complete table of substrate's grammar-level symmetries.
"""
import numpy as np
from itertools import product, combinations
from collections import defaultdict
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from trefoil_corrected_frame import trajectory_corrected

FLOW = {1, 3, 5, 7, 9}
STRUCTURE = {2, 4, 8}
TRANSITION = {6}
VOID = {0}


def role(n):
    if n in FLOW: return 'F'
    if n in STRUCTURE: return 'S'
    if n in TRANSITION: return 'T'
    if n in VOID: return 'V'
    return '?'


def swap_in_triple(t, a, b):
    return tuple(b if x == a else a if x == b else x for x in t)


def is_role_boundary(a, b):
    return role(a) != role(b)


def main():
    print("=" * 70)
    print("COMPREHENSIVE BOUNDARY SYMMETRY MAP")
    print("=" * 70)
    
    # Compute crossings for all 1000 triples once (cached)
    print("\n  Computing crossings for all 1000 triples...")
    crossings = {}
    for a, b, c in product(range(10), repeat=3):
        r = trajectory_corrected(a, b, c)
        crossings[(a, b, c)] = r['crossings']
    print(f"  Done. Total triples: {len(crossings)}")
    
    # All adjacent integer pairs
    adjacent_pairs = [(i, i+1) for i in range(9)]
    
    # All role-boundary pairs (any pair with different roles)
    all_role_boundary_pairs = []
    for a, b in combinations(range(10), 2):
        if is_role_boundary(a, b):
            all_role_boundary_pairs.append((a, b))
    
    print(f"\n  Adjacent pairs: {len(adjacent_pairs)}")
    print(f"  All role-boundary pairs: {len(all_role_boundary_pairs)}")
    
    # Test 1: Symmetries on canonical grammar
    print("\n" + "=" * 70)
    print("SYMMETRIES ON CANONICAL GRAMMAR")
    print("=" * 70)
    
    canonical = [(0,1,2), (0,7,1), (5,6,7), (7,8,9), (7,8,8)]
    
    print(f"\n  Adjacent pairs (a, a+1): which preserve admissibility on grammar?")
    print(f"  {'pair':<8} {'role':<8} {'preserves count':<20} {'on triples'}")
    
    for a, b in adjacent_pairs:
        ra, rb = role(a), role(b)
        roles = f"{ra}↔{rb}"
        preserved_triples = []
        applicable_triples = []
        for t in canonical:
            if a in t or b in t:
                applicable_triples.append(t)
                t_swap = swap_in_triple(t, a, b)
                if crossings[t] == crossings[t_swap]:
                    preserved_triples.append(t)
        if applicable_triples:
            n_pres = len(preserved_triples)
            n_app = len(applicable_triples)
            preservation = f"{n_pres}/{n_app}"
            triples_str = str(preserved_triples)[:30]
            print(f"  ({a},{b})  {roles:<8} {preservation:<20} {triples_str}")
    
    # Test 2: Non-adjacent role-boundary pairs on grammar
    print(f"\n\n  Non-adjacent role-boundary pairs:")
    print(f"  {'pair':<8} {'role':<8} {'preserves count':<20}")
    
    for a, b in all_role_boundary_pairs:
        if (a, b) in adjacent_pairs: continue
        ra, rb = role(a), role(b)
        roles = f"{ra}↔{rb}"
        preserved_triples = []
        applicable_triples = []
        for t in canonical:
            if a in t or b in t:
                applicable_triples.append(t)
                t_swap = swap_in_triple(t, a, b)
                if crossings[t] == crossings[t_swap]:
                    preserved_triples.append(t)
        if applicable_triples:
            n_pres = len(preserved_triples)
            n_app = len(applicable_triples)
            if n_pres > 0:  # only show pairs that preserve at least one triple
                preservation = f"{n_pres}/{n_app}"
                print(f"  ({a},{b})  {roles:<8} {preservation:<20}")
    
    # Test 3: Symmetries on trefoil-9 set
    print("\n" + "=" * 70)
    print("SYMMETRIES ON TREFOIL-9 SET")
    print("=" * 70)
    
    TREFOIL_9 = [
        (0,7,8), (0,8,7), (0,8,8),
        (7,0,8), (7,8,0),
        (8,0,7), (8,0,8), (8,7,0), (8,8,0),
    ]
    
    print(f"\n  Pair       | role     | trefoils preserved")
    
    for a, b in all_role_boundary_pairs:
        ra, rb = role(a), role(b)
        roles = f"{ra}↔{rb}"
        preserved = []
        applicable = []
        for t in TREFOIL_9:
            if a in t or b in t:
                applicable.append(t)
                t_swap = swap_in_triple(t, a, b)
                if t_swap in TREFOIL_9 or crossings[t_swap] == 3:
                    preserved.append(t)
        if applicable and len(preserved) > 0:
            print(f"  ({a},{b})    | {roles:<8} | {len(preserved)}/{len(applicable)}")
    
    # Test 4: Total grammar-symmetry count over all 1000 triples
    print("\n" + "=" * 70)
    print("GLOBAL TEST: HOW MANY TRIPLES PRESERVE CROSSINGS UNDER EACH SWAP?")
    print("=" * 70)
    
    print(f"\n  For each role-boundary pair, count triples T such that")
    print(f"  crossings(T) == crossings(swap(T, a, b)).")
    print(f"\n  Pair       | role     | preserved/applicable | %")
    
    pair_stats = []
    for a, b in all_role_boundary_pairs:
        applicable_count = 0
        preserved_count = 0
        for t in crossings:
            if a in t or b in t:
                applicable_count += 1
                t_swap = swap_in_triple(t, a, b)
                if crossings[t] == crossings[t_swap]:
                    preserved_count += 1
        if applicable_count > 0:
            pct = 100 * preserved_count / applicable_count
            pair_stats.append((a, b, preserved_count, applicable_count, pct))
    
    # Sort by % preserved
    pair_stats.sort(key=lambda x: -x[4])
    
    for a, b, pres, app, pct in pair_stats[:15]:
        ra, rb = role(a), role(b)
        roles = f"{ra}↔{rb}"
        print(f"  ({a},{b})    | {roles:<8} | {pres}/{app}   | {pct:.1f}%")
    
    print("\n" + "=" * 70)
    print("CHARACTERIZATION OF TOP-PRESERVING PAIRS")
    print("=" * 70)
    
    print("\n  The pairs that preserve crossings on the highest fraction of")
    print("  triples define the substrate's STRONGEST grammar-level symmetries.")
    
    top_pairs = pair_stats[:5]
    print(f"\n  Top 5 grammar symmetries:")
    for a, b, pres, app, pct in top_pairs:
        ra, rb = role(a), role(b)
        adjacent = "adjacent" if (b - a == 1 or a - b == 1) else "non-adjacent"
        print(f"    ({a},{b}) {ra}↔{rb}: {pct:.1f}% ({adjacent})")
    
    # Are they all adjacent pairs at role boundaries?
    print(f"\n  Are top symmetries all at role boundaries? Yes (by construction).")
    print(f"  Are they all adjacent integers? Check above.")
    
    # Look at the ENTIRE list to see all preserve-rates
    print(f"\n  Complete preservation distribution:")
    pres_buckets = defaultdict(list)
    for a, b, pres, app, pct in pair_stats:
        bucket = int(pct // 10) * 10
        pres_buckets[bucket].append(f"({a},{b})")
    
    for bucket in sorted(pres_buckets.keys(), reverse=True):
        print(f"    {bucket}-{bucket+9}%: {pres_buckets[bucket]}")
    
    # The "true symmetries" (preserving 100% of triples) would be honest 
    # algebraic equivalences. Anything less is partial.
    print("\n" + "=" * 70)
    print("ARE THERE ANY \"TRUE\" SYMMETRIES (100% PRESERVATION)?")
    print("=" * 70)
    
    full_symms = [(a, b) for a, b, pres, app, pct in pair_stats if pct == 100.0]
    print(f"\n  Pairs with 100% preservation: {full_symms}")
    
    if not full_symms:
        print(f"  No pair preserves crossings on ALL triples. The substrate has no")
        print(f"  full algebraic symmetries beyond identity.")
    
    print(f"\n  Highest-preservation pair: {pair_stats[0][:2]} at {pair_stats[0][4]:.1f}%")


if __name__ == "__main__":
    main()
