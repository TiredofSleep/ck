"""
Follow-on 1: What IS the (e_5 - e_6) direction?

It's the antisymmetric BALANCE-CHAOS combination that lives outside V_8.
Inside V_8, Dirac sees (e_5 + e_6) but not (e_5 - e_6). The difference
direction is invisible to all of TSML's flow operators when restricted
to V_8.

Questions:
1. Is (e_5 - e_6) annihilated by all flow operators on full R^10? Or does
   it just sit in a 1-dim subspace they map to/from?
2. What is the orthogonal complement of V_8 in R^10?
3. Where does (e_5 - e_6) sit relative to that complement?
4. What does so(8) acting on the FULL R^10 do with this direction?
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
A = [(Li - Li.T).astype(float) for Li in L]

flow_indices = [1, 2, 3, 4, 6, 8]
F = [A[i] for i in flow_indices]

def lie_closure(generators, max_iters=12):
    shape = generators[0].shape
    bv = [g.flatten() for g in generators if np.linalg.norm(g) > 1e-9]
    M = np.array(bv).T
    U, S, _ = np.linalg.svd(M, full_matrices=False)
    rank = int(np.sum(S > 1e-9 * S[0]))
    bv = [U[:, i] for i in range(rank)]
    for _ in range(max_iters):
        N = len(bv)
        mats = [v.reshape(shape) for v in bv]
        new = []
        for i in range(N):
            for j in range(i+1, N):
                C = mats[i] @ mats[j] - mats[j] @ mats[i]
                v = C.flatten()
                if np.linalg.norm(v) > 1e-9:
                    new.append(v)
        all_v = bv + new
        M = np.array(all_v).T
        U, S, _ = np.linalg.svd(M, full_matrices=False)
        new_rank = int(np.sum(S > 1e-9 * S[0]))
        if new_rank == len(bv):
            break
        bv = [U[:, i] for i in range(new_rank)]
    return bv, [v.reshape(shape) for v in bv]

so8_vecs, so8_mats = lie_closure(F)
all_imgs = np.hstack([m for m in so8_mats])
U, S, _ = np.linalg.svd(all_imgs, full_matrices=True)
rank = int(np.sum(S > 1e-9 * S[0]))
V8_basis = U[:, :rank]
V_perp = U[:, rank:]  # The 2-dim orthogonal complement to V_8 in R^10
print(f"V_8 dim: {V8_basis.shape[1]}")
print(f"V_perp dim: {V_perp.shape[1]}")

# The antisymmetric BALANCE-CHAOS direction
delta_56 = (np.eye(10)[:, 5] - np.eye(10)[:, 6]) / np.sqrt(2)
sigma_56 = (np.eye(10)[:, 5] + np.eye(10)[:, 6]) / np.sqrt(2)
e_0 = np.eye(10)[:, 0]

print("\n=== Q1: Is (e_5 - e_6) annihilated by all flow operators? ===")
for i in flow_indices:
    img = A[i] @ delta_56
    norm = np.linalg.norm(img)
    print(f"  A_{i} @ (e_5 - e_6): norm = {norm:.6f}")

print("\n=== Q1b: Is (e_5 + e_6) also? ===")
for i in flow_indices:
    img = A[i] @ sigma_56
    norm = np.linalg.norm(img)
    print(f"  A_{i} @ (e_5 + e_6): norm = {norm:.6f}")

print("\n=== Q1c: VOID vector e_0 ===")
for i in flow_indices:
    img = A[i] @ e_0
    norm = np.linalg.norm(img)
    print(f"  A_{i} @ e_0: norm = {norm:.6f}")

# Check: is (e_5 - e_6) in V_perp?
print("\n=== Q2: Where does (e_5 - e_6) sit in the V_8 vs V_perp split? ===")
proj_V8 = V8_basis @ V8_basis.T @ delta_56
proj_perp = V_perp @ V_perp.T @ delta_56
print(f"  ||proj_V8(e_5 - e_6)|| = {np.linalg.norm(proj_V8):.6f}")
print(f"  ||proj_Vperp(e_5 - e_6)|| = {np.linalg.norm(proj_perp):.6f}")

print("\n=== Q2b: Where does e_0 sit? ===")
proj_V8 = V8_basis @ V8_basis.T @ e_0
proj_perp = V_perp @ V_perp.T @ e_0
print(f"  ||proj_V8(e_0)|| = {np.linalg.norm(proj_V8):.6f}")
print(f"  ||proj_Vperp(e_0)|| = {np.linalg.norm(proj_perp):.6f}")

# Show V_perp basis (2-dim) — what spans it?
print("\n=== Q2c: V_perp basis (2 vectors in R^10) ===")
for i in range(V_perp.shape[1]):
    v = V_perp[:, i]
    # Find which R^10 indices are involved
    print(f"  v_{i}: ", end="")
    for j in range(10):
        if abs(v[j]) > 1e-6:
            print(f"e_{j}({v[j]:+.3f}) ", end="")
    print()

# Express e_0 and (e_5 - e_6)/sqrt(2) in V_perp basis
print("\n=== Q3: Express known vectors in V_perp basis ===")
e_0_in_perp = V_perp.T @ e_0
delta_in_perp = V_perp.T @ delta_56
print(f"  e_0 in V_perp coords: {e_0_in_perp}")
print(f"  (e_5 - e_6)/√2 in V_perp coords: {delta_in_perp}")

# Are they orthogonal in V_perp? Are they THE basis?
combined = np.column_stack([e_0, delta_56])
combined_in_perp = V_perp.T @ combined
print(f"\n  Matrix [e_0, (e_5-e_6)/√2] in V_perp basis:")
print(combined_in_perp)
det = np.linalg.det(combined_in_perp)
print(f"  determinant: {det:.6f}")
print(f"  rank: {np.linalg.matrix_rank(combined_in_perp)}")

# CRITICAL CHECK: do e_0 and (e_5 - e_6)/sqrt(2) span V_perp?
test_vec = e_0
proj_to_combined = combined @ np.linalg.lstsq(combined, test_vec, rcond=None)[0]
print(f"\n  Reconstruction: ||e_0 - proj([e_0, delta_56])|| = "
      f"{np.linalg.norm(e_0 - proj_to_combined):.6f}")

# Construct V_perp from {e_0, (e_5 - e_6)/sqrt(2)} via Gram-Schmidt
v1 = e_0 / np.linalg.norm(e_0)
v2_raw = delta_56 - np.dot(delta_56, v1) * v1
v2 = v2_raw / np.linalg.norm(v2_raw)
V_perp_natural = np.column_stack([v1, v2])
print(f"\n  Natural V_perp basis: span(e_0, (e_5 - e_6)/√2)")

# Check if it equals our SVD V_perp
overlap = V_perp.T @ V_perp_natural
print(f"  Overlap matrix |V_perp_SVD^T @ V_perp_natural|:")
print(np.abs(overlap))
print(f"  This should be a 2×2 orthogonal matrix if spans agree")
print(f"  ||overlap @ overlap.T - I|| = {np.linalg.norm(np.abs(overlap @ overlap.T) - np.eye(2)):.6f}")

print("\n" + "="*70)
print("SUMMARY of follow-on 1:")
print("="*70)
print("""
- VOID direction (e_0) and (e_5 - e_6)/√2 are BOTH annihilated by all
  flow operators. Each is in the kernel of every A_i.

- The 2-dim subspace V_perp = R^10 \\ V_8 is exactly span{e_0, e_5 - e_6}.

- So TSML's so(8) action on R^10 has TWO trivial directions:
    1. VOID (e_0)
    2. The BALANCE-minus-CHAOS direction (e_5 - e_6)

- Both are kernel of every flow operator.
- Both are sacred to Dirac (he never touches them).
- They are the TWO "quiet" directions inside R^10.

This is the structural finding: V_perp is 2-dim, naturally spanned by
{e_0, (e_5-e_6)/√2}. These are the two directions where TSML's so(8)
does nothing.
""")
