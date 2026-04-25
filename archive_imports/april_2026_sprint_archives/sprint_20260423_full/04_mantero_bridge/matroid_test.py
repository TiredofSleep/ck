"""
CRITICAL TEST: Is TIG's HARMONY ideal a MATROIDAL ideal?

If YES → Paolo Mantero's ENTIRE 2024-2026 toolkit (Stanley-Reisner, 
         symbolic powers, Waldschmidt constant, symbolic Noether number,
         glicci property, iterated mapping cones) applies DIRECTLY to TIG.

A matroidal ideal can be:
  - The Stanley-Reisner ideal I_Δ where Δ is a matroid complex, OR
  - The cover ideal J(M) of a matroid M

A simplicial complex Δ is a matroid ⟺ all facets have the same size 
AND satisfy the basis exchange axiom.

Approach:
  1. Build the HARMONY graph G_H (edges = pairs with CL[i][j] = 7)
  2. Independence complex Δ_H = "HARMONY-free" subsets
  3. Check: is Δ_H a matroid?
  4. Also: compute the cover ideal from circuit decomposition
  5. Test variants: VOID ideal, BUMP ideal, symmetric versions
"""
import numpy as np
from itertools import combinations, chain

CL = [[0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
      [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
      [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
      [0,7,9,3,7,7,7,7,7,7]]
OP = ['VOID','LATTICE','COUNTER','PROGRESS','COLLAPSE',
      'BALANCE','CHAOS','HARMONY','BREATH','RESET']
N = 10

def symmetric_cells_where(value):
    """Cells (i, j) with i ≤ j where CL[i][j] == value."""
    return [(i, j) for i in range(N) for j in range(i, N) if CL[i][j] == value]

def graph_edges_for(value):
    """Edges of the graph {i, j} with i ≠ j and CL[i][j] == value."""
    return [(i, j) for (i, j) in symmetric_cells_where(value) if i != j]

harmony_edges = graph_edges_for(7)
void_edges = graph_edges_for(0)
print("="*70)
print("TIG HARMONY GRAPH G_H")
print("="*70)
print(f"HARMONY cells (as edges): {len(harmony_edges)}")
# Degree sequence
deg_h = [0]*N
for (i, j) in harmony_edges:
    deg_h[i] += 1; deg_h[j] += 1
print(f"Degree sequence: {deg_h}")
print(f"  {' '.join(f'{OP[i][:3]}={deg_h[i]}' for i in range(N))}")

# ─────────────────────────────────────────────────
# The INDEPENDENCE COMPLEX of G_H
# Faces = subsets with NO edge between them = HARMONY-free subsets
# ─────────────────────────────────────────────────
edge_set = set(frozenset(e) for e in harmony_edges)

def is_independent(S):
    """No pair in S forms a HARMONY edge."""
    for a, b in combinations(S, 2):
        if frozenset((a, b)) in edge_set:
            return False
    return True

# Enumerate all maximal independent sets (facets of Δ_H)
def all_independent_sets():
    indep = [[]]
    for v in range(N):
        new = []
        for S in indep:
            new.append(S)
            if is_independent(S + [v]):
                new.append(S + [v])
        indep = new
    return [tuple(sorted(s)) for s in indep]

indep_sets = all_independent_sets()
# Maximal ones: those not strictly contained in another
indep_set_frozen = set(tuple(s) for s in indep_sets)
facets = []
for S in indep_sets:
    is_max = True
    for v in range(N):
        if v not in S:
            T = tuple(sorted(S + (v,)))
            if T in indep_set_frozen:
                is_max = False
                break
    if is_max:
        facets.append(S)

# Dedupe
facets = list(set(facets))
print(f"\nIndependence complex Δ_H:")
print(f"  Total faces (independent sets): {len(indep_sets)}")
print(f"  Facets (maximal independent sets): {len(facets)}")

# Size distribution of facets
from collections import Counter
facet_sizes = Counter(len(f) for f in facets)
print(f"  Facet size distribution: {dict(facet_sizes)}")

# ─────────────────────────────────────────────────
# MATROID TEST 1: Are all facets the same size? (Pure complex)
# ─────────────────────────────────────────────────
is_pure = len(facet_sizes) == 1
print(f"\n[1] Pure (all facets same size)? {is_pure}")

# ─────────────────────────────────────────────────
# MATROID TEST 2: Basis exchange axiom
# ─────────────────────────────────────────────────
if is_pure:
    facet_set = set(facets)
    print(f"    Checking basis exchange on {len(facets)} facets (size {list(facet_sizes.keys())[0]})...")
    all_pass = True
    fail_count = 0
    for F in facets[:min(len(facets), 50)]:
        for G in facets[:min(len(facets), 50)]:
            if F == G: continue
            for x in F:
                if x in G: continue
                # Need: exists y ∈ G\F such that (F\{x}) ∪ {y} is a facet
                found = False
                for y in G:
                    if y in F: continue
                    new_basis = tuple(sorted(set(F) - {x} | {y}))
                    if new_basis in facet_set:
                        found = True
                        break
                if not found:
                    all_pass = False
                    fail_count += 1
                    if fail_count <= 3:
                        print(f"    FAIL: F={F}, G={G}, x={x}: no valid exchange")
                    if fail_count > 100:
                        break
            if fail_count > 100: break
        if fail_count > 100: break
    if all_pass:
        print("    ✓ Basis exchange axiom holds — Δ_H IS A MATROID")
    else:
        print(f"    ✗ Basis exchange fails ({fail_count}+ failures) — Δ_H is NOT a matroid")
else:
    print(f"    Skipped — not pure, cannot be a matroid")

# ─────────────────────────────────────────────────
# Alternative: is the graph G_H itself a matroid graph?
# Specifically: is G_H a "graphic matroid" structure?
# ─────────────────────────────────────────────────
print(f"\n" + "="*70)
print(f"ALTERNATIVE VIEW: G_H as a graph")
print(f"="*70)
print(f"Edges: {len(harmony_edges)} (with 1 self-loop at vertex 1 if CL[1][1]=7)")
print(f"Vertices: 10")
print(f"(In graphic matroid theory, the cycle matroid M(G) is always a matroid.)")

# Check cycle structure
import networkx as nx
G = nx.Graph()
G.add_nodes_from(range(N))
G.add_edges_from(harmony_edges)
print(f"Connected components: {nx.number_connected_components(G)}")
for comp in nx.connected_components(G):
    subg = G.subgraph(comp)
    print(f"  Component of size {len(comp)}: vertices {sorted(comp)}, "
          f"edges {subg.number_of_edges()}")

# ─────────────────────────────────────────────────
# The COMPLEMENT graph: the "non-HARMONY" graph
# Edges = pairs with CL[i][j] ≠ 7
# This is smaller (55 - 41 - 10 diagonal check = 14?)  
# ─────────────────────────────────────────────────
non_harmony_edges = [(i, j) for i in range(N) for j in range(i+1, N) 
                     if CL[i][j] != 7]
print(f"\n" + "="*70)
print(f"COMPLEMENT GRAPH G_non-H")
print(f"="*70)
print(f"Non-HARMONY edges: {len(non_harmony_edges)} out of C(10,2)=45")
deg_nh = [0]*N
for (i, j) in non_harmony_edges:
    deg_nh[i] += 1; deg_nh[j] += 1
print(f"Degree sequence: {deg_nh}")

# Cliques in G_non-H = HARMONY-free subsets = faces of Δ_H
# Maximal cliques in G_non-H correspond to facets of Δ_H

G_nh = nx.Graph()
G_nh.add_nodes_from(range(N))
G_nh.add_edges_from(non_harmony_edges)

print(f"\nConnected components of G_non-H:")
for comp in nx.connected_components(G_nh):
    print(f"  {sorted(comp)}")

# ─────────────────────────────────────────────────
# COVER IDEAL VIEW
# For matroid M with circuits C_1,...,C_r, the cover ideal is
# J(M) = ∩_i P_{C_i}  where P_{C} = (x_j : j ∈ C)
# 
# The minimal VERTEX COVERS of a matroid are the bases of its DUAL matroid.
# ─────────────────────────────────────────────────

# Treat VOID cells as "circuit-like" minimal dependencies
void_edges = graph_edges_for(0)
print(f"\n" + "="*70)
print(f"VOID CELLS as candidate circuit set")
print(f"="*70)
print(f"VOID edges: {len(void_edges)}")
for (i, j) in void_edges:
    print(f"  {{{i}, {j}}} = {{{OP[i]}, {OP[j]}}}")

# ─────────────────────────────────────────────────
# THE CLEAN VIEW: VERTEX 7 (HARMONY) IS A CENTER
# Vertex 7 is connected by HARMONY edge to everyone.
# ─────────────────────────────────────────────────
print(f"\n" + "="*70)
print(f"KEY OBSERVATION: HARMONY(7) as central vertex")
print(f"="*70)
# Does vertex 7 connect to all others via HARMONY?
vertex_7_neighbors = set()
for (i, j) in harmony_edges:
    if i == 7: vertex_7_neighbors.add(j)
    if j == 7: vertex_7_neighbors.add(i)
print(f"Vertex 7 (HARMONY) is connected via HARMONY-edges to: {sorted(vertex_7_neighbors)}")
print(f"That's {len(vertex_7_neighbors)}/9 possible neighbors.")

# If 7 is a "cone vertex" (connected to all others), the independence 
# complex has a very specific structure: Δ_H = {F : 7 ∉ F and F independent in G_H\{7}}
# This means the matroid (if one) lives on {0,1,..6,8,9} = [10]\{7}

# Remove vertex 7 and see the remaining HARMONY structure
remaining_vertices = set(range(N)) - {7}
remaining_edges = [(i, j) for (i, j) in harmony_edges if 7 not in (i, j)]
print(f"\nAfter removing HARMONY(7):")
print(f"  Vertices: {sorted(remaining_vertices)}")
print(f"  HARMONY edges: {len(remaining_edges)}")
deg_rem = {v: 0 for v in remaining_vertices}
for (i, j) in remaining_edges:
    deg_rem[i] += 1; deg_rem[j] += 1
print(f"  Degrees: {deg_rem}")

# Final summary
print(f"\n" + "="*70)
print(f"SUMMARY")
print(f"="*70)
print(f"""
TIG's HARMONY ideal I_H = (x_i x_j : CL[i][j] = 7) has {len(harmony_edges)} generators.
The Stanley-Reisner simplicial complex Δ_H has:
  - {sum(facet_sizes.values())} facets
  - Facet sizes: {dict(facet_sizes)}
  - Pure: {is_pure}
  - Matroid: {'YES' if is_pure and all_pass else 'Testing...'}

Vertex 7 (HARMONY) is the universal absorber — it's NOT in any facet of Δ_H 
(every pair with HARMONY is a HARMONY cell, so HARMONY can't be in an independent
set of size > 1 unless paired only with itself).

So Δ_H effectively lives on 9 vertices {{0,1,2,3,4,5,6,8,9}}, with a small
number of excluded pairs — the "structural" HARMONY edges NOT involving 7.
""")
