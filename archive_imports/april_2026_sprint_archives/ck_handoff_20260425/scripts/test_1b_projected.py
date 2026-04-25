"""
Test 1 deeper: the anticommutators are NOT scalar but they're highly structured.
Index 7 (HARMONY) keeps producing anomalous large values. Let's see if there's
a Clifford-like structure when we project away the HARMONY direction.
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

# Project out index 7 (HARMONY) — drop row 7 and col 7
def proj(M):
    """Drop row and column 7."""
    keep = [0,1,2,3,4,5,6,8,9]
    return M[np.ix_(keep, keep)]

print("="*70)
print("Anticommutators of A_i WITH index-7 (HARMONY) projected out")
print("="*70)
print()
print("Sub-matrices are 9x9. Check if anticommutator is scalar*I_9 now.")
print()

for i, j in combinations(flow_indices, 2):
    anti = A[i] @ A[j] + A[j] @ A[i]
    proj_anti = proj(anti)
    diag = np.diag(proj_anti)
    off_diag = proj_anti - np.diag(diag)
    is_diagonal = np.all(off_diag == 0)
    is_const_diag = len(set(diag)) == 1
    print(f"  ({i},{j}): diag = {list(diag)}  diagonal: {is_diagonal}  const: {is_const_diag}")

print()
print("Self-anticommutators projected:")
for i in flow_indices:
    A_sq = A[i] @ A[i]
    proj_sq = proj(A_sq)
    diag = np.diag(proj_sq)
    off_diag = proj_sq - np.diag(diag)
    is_diagonal = np.all(off_diag == 0)
    is_const_diag = len(set(diag)) == 1
    print(f"  i={i}: A_{i}^2 proj diag = {list(diag)}  diagonal: {is_diagonal}  const: {is_const_diag}")

# Also try: anticommutators WITHOUT projection but mod 2 (binary)
print()
print("="*70)
print("Anticommutators MOD 2 (treating L_i as F_2 matrices)")
print("="*70)

L_F2 = [Li % 2 for Li in L]
A_F2 = [(Li - Li.T) % 2 for Li in L]

print("\nAnticommutator { L_i, L_j } mod 2 (looking for sparse structure):")
for i, j in combinations(flow_indices, 2):
    anti = (L_F2[i] @ L_F2[j] + L_F2[j] @ L_F2[i]) % 2
    diag = np.diag(anti)
    off_diag = anti - np.diag(diag)
    is_diagonal = np.all(off_diag == 0)
    is_const = len(set(diag)) == 1
    nz = np.count_nonzero(anti)
    print(f"  ({i},{j}): nonzero count = {nz}, diagonal = {is_diagonal}, const diag = {is_const}")

# Now the actually interesting test: full anticommutator MATRIX inner product
# with identity - is it close to scalar?
print()
print("="*70)
print("Frobenius inner product of {A_i, A_j} with identity")
print("="*70)
print("If {A_i, A_j} = c * I, then <{A_i, A_j}, I> = c * 10 and ")
print("<{A_i, A_j}, off-diag-ones> = 0.")
print()

I9 = np.eye(10)
for i, j in combinations(flow_indices, 2):
    anti = A[i] @ A[j] + A[j] @ A[i]
    fro_with_I = np.sum(anti * I9)  # Frobenius inner product with I
    fro_squared = np.sum(anti * anti)
    # If anti = c*I, then fro_with_I = 10c and fro_squared = 10*c^2 → ratio = c
    if fro_with_I != 0:
        ratio = fro_squared / fro_with_I
    else:
        ratio = float('nan')
    # is it close to scalar*I? Compute the scalar that best fits and check residual
    c_best = fro_with_I / 10
    residual = anti - c_best * I9
    res_fro = np.sqrt(np.sum(residual * residual))
    anti_fro = np.sqrt(np.sum(anti * anti)) if np.sum(anti * anti) > 0 else 1
    rel_residual = res_fro / anti_fro if anti_fro > 0 else 0
    print(f"  ({i},{j}): c_best = {c_best:.3f}  rel_residual = {rel_residual:.3f}")
