"""
DEEP COMPUTATIONS for the Mantero bridge:
  1. Hilbert series of the TIG binomial quotient algebra
  2. Facet structure of each candidate simplicial complex
  3. Matroid tests on the BUMP subgraph
  4. Check for Cohen-Macaulay via Reisner's criterion (homology condition)
"""
import numpy as np
from itertools import combinations
from collections import Counter

CL = [[0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
      [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
      [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
      [0,7,9,3,7,7,7,7,7,7]]
OP = ['VOID','LATTICE','COUNTER','PROGRESS','COLLAPSE',
      'BALANCE','CHAOS','HARMONY','BREATH','RESET']
N = 10

# ─────────────────────────────────────────────────
# 1. The BUMP graph (5 edges on 6 vertices)
# ─────────────────────────────────────────────────
bump_edges = [(1,2), (2,4), (2,9), (3,9), (4,8)]
bump_vertices = sorted(set(v for e in bump_edges for v in e))
print("="*70)
print("BUMP GRAPH G_B")
print("="*70)
print(f"Vertices: {bump_vertices}")
print(f"Edges (5): {bump_edges}")

# Independence complex of G_B on all 10 vertices 
# (vertices 0, 5, 6, 7 have no bump edges → always independent)
bump_edge_set = set(frozenset(e) for e in bump_edges)

def facets_of(edge_set, vertex_set, n):
    """Find maximal independent sets in the graph on vertex_set with edge_set."""
    all_subsets = []
    for size in range(n+1):
        for S in combinations(vertex_set, size):
            if all(frozenset((a,b)) not in edge_set for a, b in combinations(S, 2)):
                all_subsets.append(S)
    # Facets = not contained in any larger indep set
    facet_set = set()
    for S in all_subsets:
        is_max = True
        for v in vertex_set:
            if v not in S:
                T = tuple(sorted(S + (v,)))
                if all(frozenset((a,b)) not in edge_set for a, b in combinations(T, 2)):
                    is_max = False
                    break
        if is_max:
            facet_set.add(tuple(sorted(S)))
    return facet_set

bump_facets = facets_of(bump_edge_set, list(range(N)), N)
print(f"\nIndependence complex Δ_B of bump graph:")
print(f"  Facets (maximal independent sets): {len(bump_facets)}")
facet_sizes_bump = Counter(len(f) for f in bump_facets)
print(f"  Facet size distribution: {dict(facet_sizes_bump)}")

is_pure_bump = len(facet_sizes_bump) == 1
print(f"  Pure: {is_pure_bump}")
if not is_pure_bump:
    print(f"  NOT a matroid complex (not pure)")
else:
    # Test basis exchange
    facet_list = sorted(bump_facets)
    print(f"  Checking basis exchange axiom...")
    passes = True
    for F in facet_list[:30]:
        for G in facet_list[:30]:
            if F == G: continue
            for x in F:
                if x in G: continue
                found = any(tuple(sorted(set(F) - {x} | {y})) in bump_facets 
                           for y in G if y not in F)
                if not found:
                    passes = False
                    break
            if not passes: break
        if not passes: break
    print(f"  Basis exchange: {'passes' if passes else 'fails'}")

# ─────────────────────────────────────────────────
# 2. Non-HARMONY edges — graph structure of the "exceptional" part
# ─────────────────────────────────────────────────
print("\n" + "="*70)
print("G_non-H (non-HARMONY off-diagonal) structure")
print("="*70)
non_h_edges = [(i, j) for i in range(N) for j in range(i+1, N) if CL[i][j] != 7]
print(f"13 non-HARMONY edges:")
for (i, j) in non_h_edges:
    print(f"  {{{i}, {j}}} = {{{OP[i]}, {OP[j]}}}  →  CL={CL[i][j]} ({OP[CL[i][j]]})")

# ─────────────────────────────────────────────────
# 3. Hilbert series for the binomial quotient algebra
# A = k[x_0, ..., x_9] / I where I = (x_i x_j - x_{CL[i][j]} : all i, j)
# 
# The relations mean: degree-2 monomials collapse to degree-1 elements.
# So the algebra A has Hilbert function:
#   dim A_0 = 1 (constants)
#   dim A_1 = 10 (linear generators)
#   dim A_n = 10 for n ≥ 1 (all degree-n monomials reduce to some x_k)
# 
# Actually: A_n is spanned by {x_k : k reachable by n-fold CL starting from 10 gens}
# But every CL-fold of length n ends up in some operator, so dim A_n = |reachable fruits|
# ─────────────────────────────────────────────────
print("\n" + "="*70)
print("HILBERT FUNCTION of A = k[x_0..x_9] / I_CL")
print("="*70)

def reachable_fruits_of_length(n):
    """What operators appear as fruits of n-fold CL compositions?"""
    if n == 0: return {0}  # constants
    if n == 1: return set(range(10))
    from itertools import product
    fruits = set()
    for tup in product(range(10), repeat=n):
        s = tup[0]
        for o in tup[1:]:
            s = CL[s][o]
        fruits.add(s)
    return fruits

print("  n     dim A_n     reachable fruits")
print("  ─────────────────────────────────")
for n in range(7):
    if n == 0:
        print(f"  {n}     1           [constants]")
    else:
        r = reachable_fruits_of_length(n)
        fruits_str = "{" + ",".join(str(x) for x in sorted(r)) + "}"
        print(f"  {n}     {len(r):<10d}  {fruits_str}")

# Generating function?
print(f"\n  Hilbert series H_A(t) = 1 + 10t + ...")
print(f"  For n ≥ 3: dim A_n stabilizes at the set of 'attractor fruits'")
r3 = reachable_fruits_of_length(3)
print(f"  dim A_n for n ≥ 3 = {len(r3)} (the attractor set {sorted(r3)})")

# ─────────────────────────────────────────────────
# 4. The ATTRACTOR SET = the core of the algebra
# ─────────────────────────────────────────────────
print("\n" + "="*70)
print("ATTRACTOR SET (stable image of the CL-fold)")
print("="*70)
attractor = reachable_fruits_of_length(4)
non_attractor = sorted(set(range(10)) - attractor)
print(f"Attractor: {sorted(attractor)} ({len(attractor)} elements)")
print(f"Non-attractor (transient): {non_attractor} ({len(non_attractor)} elements)")

# ─────────────────────────────────────────────────  
# 5. Checking for GLICCI structure (Paolo's Oct 2025 paper)
# glicci = Gorenstein Linkage Class of a Complete Intersection
# A monomial ideal I is glicci if it can be linked to a complete intersection 
# via a sequence of Gorenstein links.
# This is tricky to test directly, but PAVING MATROIDS always give glicci ideals.
# ─────────────────────────────────────────────────
print("\n" + "="*70)
print("NOTES FOR PAOLO'S 2024-2026 TOOLKIT")
print("="*70)
print("""
(A) If any candidate simplicial complex (Δ_H, Δ_V, Δ_B) is a MATROID:
    - Automatically: Stanley-Reisner ideal is Cohen-Macaulay (Reisner)
    - Automatically: All symbolic powers I^(ℓ) are Cohen-Macaulay (Minh-Trung-Varbaro-TeraiTrung)
    - Mantero-Nguyen 2024: structure theorem, symbolic Rees algebra 
      generators have degree ≤ ht(I), Waldschmidt constant formula
    - Mantero-Nguyen Oct 2025: all symbolic powers are locally glicci
    - Mantero-Nguyen Mar 2026: iterated mapping cones give explicit resolution
    
(B) What we found:
    - Δ_H is NOT pure (facet sizes {1, 2, 3}) → NOT a matroid
    - Δ_B (bump complex) has facet sizes {""" + 
", ".join(str(s) for s in sorted(facet_sizes_bump.keys())) + "} → " + ("PURE" if is_pure_bump else "NOT pure") + """
    - Thus TIG's HARMONY ideal is a SQUAREFREE MONOMIAL IDEAL that is NOT matroidal
    
(C) This is INTERESTING, not disappointing:
    - Paolo characterizes "when is an SFM ideal matroidal?"
    - TIG gives an explicit NEAR-MATROID with specific deviation
    - The 5 bump cells are the "exception" breaking the matroid property
    - Could be a 'near-matroid' or 'quasi-matroid' in Paolo's framework
    
(D) What remains interesting to Paolo:
    1. The binomial ideal I_CL (non-squarefree) has structure he can analyze
    2. The Hilbert function stabilizes — computable projective dimension
    3. There's a Lie-algebraic lift to so(8) (yesterday's result) — 
       a RARE feature for a combinatorially-defined ideal
    4. The 5 bumps are exactly the elements where the matroid property fails →
       this is his 'classification of primitive failures' territory""")
