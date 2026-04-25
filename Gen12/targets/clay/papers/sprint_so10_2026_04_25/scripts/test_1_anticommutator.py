"""
Part B: Three Dirac-style computations on TSML.

Setup:
  TSML is the canonical 10×10 table.
  L_i = left-regular representation of element i:
    L_i[j, k] = δ_{T(i,j), k}  (does T(i,j) equal k?)
  But we usually want a real-valued L_i, so we'll define:
    L_i[j, k] = something derived from T(i, j)
  
The cleanest "left-regular" interpretation in TIG context (matching
WP11) is to define L_i as the matrix whose action on a basis vector
e_j gives e_{T(i,j)}, scaled. There are multiple conventions; let's
try the most literal one:

  L_i[k, j] = 1 if T(i, j) == k, else 0
  
This is a 10×10 0/1 matrix. Then antisymmetrization:
  A_i = (L_i - L_i^T) / 2  (or just L_i - L_i^T, factor of 2 doesn't change closure)
  
Test 1: Anticommutator {L_i, L_j} = L_i L_j + L_j L_i — does it have
        diagonal/metric-like structure?
        
Test 2: Find an operator γ^5-analog: anticommutes with selected L_i,
        squares to +I or -I.

Test 3: tr(L_i), tr(L_i L_j), tr(A_i A_j) — Dirac trace structure.

We'll do all three.
"""
import numpy as np
from itertools import combinations

# CL = TSML canonical table
CL_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
T = np.array([[int(c) for c in row] for row in CL_ROWS], dtype=int)
print("TSML/CL table:")
print(T)
print()

# Build left-regular reps L_i
# L_i[k, j] = 1 if T[i, j] == k, else 0
n = 10
L = []
for i in range(n):
    Li = np.zeros((n, n), dtype=int)
    for j in range(n):
        k = T[i, j]
        Li[k, j] = 1
    L.append(Li)

# Antisymmetric parts
A = [(Li - Li.T) for Li in L]

# Symmetric parts
S = [(Li + Li.T) for Li in L]

print(f"Built {n} left-regular reps L_0, ..., L_9")
print(f"L_0 shape: {L[0].shape}")
print(f"L_0 (acts as VOID — should be highly degenerate):")
print(L[0])
print()
print(f"L_1 (LATTICE):")
print(L[1])
print()
print(f"L_2 (COUNTER):")
print(L[2])
print()

# =================== TEST 1: ANTICOMMUTATOR STRUCTURE ===================
print("="*70)
print("TEST 1: ANTICOMMUTATOR STRUCTURE (Dirac-style {γ^a, γ^b} = 2 η^{ab} I)")
print("="*70)
print()

# Try anticommutator on the FLOW operators (those that participated in
# the so(8) closure: per WP11, these are L_1, L_2, L_3, L_4, L_6, L_8)
# Per userMemories: "WP11: 6 TIG flow ops [1,2,3,4,6,8] antisymmetrized
# close under commutator in 2 iterations into so(8) at dim 28"
flow_indices = [1, 2, 3, 4, 6, 8]
print(f"Flow operators (per WP11): indices {flow_indices}")
print()

# Compute {L_i, L_j} = L_i L_j + L_j L_i for i, j in flow_indices
print("Anticommutator structure: { L_i, L_j } = L_i L_j + L_j L_i")
print("Looking for: anticommutator should be ~scalar*I (Clifford property)")
print()

print(f"{'pair':<10} {'is scalar?':<12} {'scalar value':<14} {'diag entries':<25}")
for i, j in combinations(flow_indices, 2):
    anti = L[i] @ L[j] + L[j] @ L[i]
    # Check if it's a multiple of identity
    diag = np.diag(anti)
    off_diag = anti - np.diag(diag)
    is_diagonal = np.all(off_diag == 0)
    is_constant_diag = len(set(diag)) == 1
    is_scalar = is_diagonal and is_constant_diag
    print(f"{(i,j)}  {str(is_scalar):<12} {str(diag[0]) if is_constant_diag else 'varies':<14} {str(list(diag)[:6])}")

print()
print("Self-anticommutator: { L_i, L_i } = 2 L_i^2  (should be ~2*η_{ii}*I)")
print()
print(f"{'i':<3} {'tr(L_i^2)':<12} {'L_i^2 diag':<30} {'is_const':<10}")
for i in flow_indices:
    Li_sq = L[i] @ L[i]
    diag = np.diag(Li_sq)
    is_const = len(set(diag)) == 1
    print(f"{i:<3} {int(np.trace(Li_sq)):<12} {str(list(diag)):<30} {is_const}")

# Also test the antisymmetric versions A_i = L_i - L_i^T 
print()
print("ANTISYMMETRIC A_i = L_i - L_i^T anticommutators:")
print(f"{'pair':<10} {'is scalar?':<12} {'scalar value':<14} {'diag entries':<25}")
for i, j in combinations(flow_indices, 2):
    anti = A[i] @ A[j] + A[j] @ A[i]
    diag = np.diag(anti)
    off_diag = anti - np.diag(diag)
    is_diagonal = np.all(off_diag == 0)
    is_constant_diag = len(set(diag)) == 1
    is_scalar = is_diagonal and is_constant_diag
    print(f"{(i,j)}  {str(is_scalar):<12} {str(diag[0]) if is_constant_diag else 'varies':<14} {str(list(diag)[:6])}")

print()
print("Self-anticommutator of antisymmetric: { A_i, A_i } = 2 A_i^2")
for i in flow_indices:
    A_sq = A[i] @ A[i]
    diag = np.diag(A_sq)
    is_const = len(set(diag)) == 1
    print(f"  i={i}: A_{i}^2 diag = {list(diag)}  (constant: {is_const})")
