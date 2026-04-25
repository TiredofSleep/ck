"""
Test 2 and Test 3.

Test 2: find an operator that anticommutes with all flow operators
        (analog of γ^5)

Test 3: trace structure of L_i and L_i L_j
"""
import numpy as np
from itertools import combinations

CL_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
T = np.array([[int(c) for c in row] for row in CL_ROWS], dtype=int)

n = 10
L = []
for i in range(n):
    Li = np.zeros((n, n), dtype=int)
    for j in range(n):
        k = T[i, j]
        Li[k, j] = 1
    L.append(Li)
A = [(Li - Li.T) for Li in L]

flow_indices = [1, 2, 3, 4, 6, 8]
non_flow = [0, 5, 7, 9]

# =============================================================
# TEST 2: γ^5 analog
# =============================================================
print("="*70)
print("TEST 2: searching for a γ^5 analog")
print("Need: operator G such that {G, A_i} = 0 for all flow i,")
print("      and G^2 = ±I (or scalar*I)")
print("="*70)
print()

# First: try the non-flow operators
print("Candidate: each non-flow A_i (indices 0, 5, 7, 9):")
for cand in non_flow:
    G = A[cand]
    G_sq = G @ G
    G_sq_diag = np.diag(G_sq)
    is_const = len(set(G_sq_diag)) == 1
    
    anticomm_with_flow = []
    for i in flow_indices:
        ac = G @ A[i] + A[i] @ G
        anticomm_zero = np.all(ac == 0)
        anticomm_with_flow.append((i, anticomm_zero, np.sum(np.abs(ac))))
    
    all_anti = all(z for _, z, _ in anticomm_with_flow)
    print(f"\n  A_{cand}: G^2 diag = {list(G_sq_diag)[:5]}..., const: {is_const}")
    print(f"    Anticommutes with all flow ops: {all_anti}")
    if not all_anti:
        for i, z, mag in anticomm_with_flow:
            print(f"      with A_{i}: zero = {z}, |sum| = {mag}")

# Try: product of all flow operators (analog of γ^5 = i γ^0γ^1γ^2γ^3)
print()
print("Candidate: product A_1 * A_2 * A_3 * A_4 * A_6 * A_8")
G_prod = np.eye(10, dtype=int)
for i in flow_indices:
    G_prod = G_prod @ A[i]
print(f"  G_prod = product. shape = {G_prod.shape}")
print(f"  G_prod^2 trace = {np.trace(G_prod @ G_prod)}")
print(f"  G_prod^2 diag = {list(np.diag(G_prod @ G_prod))}")

anti_with_flow = []
for i in flow_indices:
    ac = G_prod @ A[i] + A[i] @ G_prod
    anti_with_flow.append((i, np.all(ac == 0), np.sum(np.abs(ac))))
    
print(f"  anticommutes with each flow A_i?")
for i, z, mag in anti_with_flow:
    print(f"    A_{i}: zero={z}, |sum|={mag}")

# Try: COMMUTATOR with each flow op
print()
print("Does G_prod COMMUTE with all flow A_i? (alternative interpretation)")
for i in flow_indices:
    com = G_prod @ A[i] - A[i] @ G_prod
    print(f"  [G_prod, A_{i}]: zero = {np.all(com == 0)}, |sum| = {np.sum(np.abs(com))}")

# Mod 2 versions: search for anticommuting elements
print()
print()
print("="*70)
print("γ^5 search MOD 2:")
print("Looking for G in F_2 with {G, A_i mod 2} = 0 for all flow i")
print("="*70)
print()

A_F2 = [(Li - Li.T) % 2 for Li in L]
# Try non-flow A_i mod 2
for cand in non_flow:
    G = A_F2[cand]
    anti_with_flow = []
    for i in flow_indices:
        ac = (G @ A_F2[i] + A_F2[i] @ G) % 2
        anti_with_flow.append((i, np.all(ac == 0)))
    all_anti = all(z for _, z in anti_with_flow)
    print(f"  A_{cand} mod 2: anticommutes with all flow? {all_anti}")
    if not all_anti:
        bad = [i for i,z in anti_with_flow if not z]
        print(f"    fails on: {bad}")

# Try product mod 2
print()
print("Product G = A_1*A_2*A_3*A_4*A_6*A_8 mod 2:")
G_F2 = np.eye(10, dtype=int)
for i in flow_indices:
    G_F2 = (G_F2 @ A_F2[i]) % 2
G_F2 = G_F2 % 2
print(f"  G mod 2 nonzero count = {np.count_nonzero(G_F2)}")
print(f"  G^2 mod 2 = identity? {np.all((G_F2 @ G_F2) % 2 == np.eye(10, dtype=int))}")

for i in flow_indices:
    ac = (G_F2 @ A_F2[i] + A_F2[i] @ G_F2) % 2
    com = (G_F2 @ A_F2[i] - A_F2[i] @ G_F2) % 2
    print(f"  vs A_{i}: anticomm zero = {np.all(ac == 0)}, comm zero = {np.all(com == 0)}")

# =============================================================
# TEST 3: TRACE STRUCTURE
# =============================================================
print()
print()
print("="*70)
print("TEST 3: TRACE STRUCTURE (Dirac: tr(γ) = 0, tr(γγ') = 4η)")
print("="*70)
print()

# tr(L_i)
print("tr(L_i):")
for i in range(10):
    tr = np.trace(L[i])
    print(f"  L_{i}: tr = {tr}")

# tr(A_i) — by construction antisymmetric, so trace = 0
print()
print("tr(A_i) (antisymmetrized — should be 0 by construction):")
for i in range(10):
    print(f"  A_{i}: tr = {np.trace(A[i])}")

# tr(L_i L_j) — bilinear form
print()
print("tr(L_i L_j) for flow indices — bilinear form:")
print(f"{'':4} ", end="")
for j in flow_indices:
    print(f"{j:>6}", end="")
print()
for i in flow_indices:
    print(f"  L_{i}: ", end="")
    for j in flow_indices:
        tr = np.trace(L[i] @ L[j])
        print(f"{tr:>6}", end="")
    print()

# tr(A_i A_j) — Killing form on flow generators
print()
print("tr(A_i A_j) for flow indices — KILLING FORM analog:")
print(f"{'':4} ", end="")
for j in flow_indices:
    print(f"{j:>6}", end="")
print()
killing = np.zeros((6, 6), dtype=int)
for ii, i in enumerate(flow_indices):
    print(f"  A_{i}: ", end="")
    for jj, j in enumerate(flow_indices):
        tr = np.trace(A[i] @ A[j])
        killing[ii, jj] = tr
        print(f"{tr:>6}", end="")
    print()

print()
print("Killing form matrix (should be symmetric):")
print(killing)
print(f"\nIs symmetric? {np.all(killing == killing.T)}")
print(f"Eigenvalues of Killing: {sorted(np.linalg.eigvals(killing.astype(float)).real)}")
print(f"det(Killing) = {np.linalg.det(killing.astype(float)):.3f}")
print(f"trace(Killing) = {np.trace(killing)}")

# Compare to Dirac's pattern: tr(γμγν) = 4η^μν
# For our case, if it's Dirac-like, we'd expect:
#   tr(A_i A_j) = c * δ_ij for some constant c (compact signature)
# i.e., diagonal Killing form
print()
print("Is Killing diagonal (would be Dirac-like for compact signature)?")
killing_offdiag = killing - np.diag(np.diag(killing))
print(f"  Off-diagonal elements all zero? {np.all(killing_offdiag == 0)}")
print(f"  Off-diagonal max absolute value: {np.max(np.abs(killing_offdiag))}")
