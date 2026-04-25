"""
Reverse the lens: stand inside TSML's structure and ask what Dirac touches.

Concrete questions:
1. Of TSML's 10 operators, which are involved when we span the Dirac
   sub-space? Which are untouched?
2. Of TSML's 10 indices/positions, which directions are "live" under
   the Dirac sub-action? Which are fixed/annihilated/orthogonal?
3. Of TSML's table cells (100 cells with values 0,3,4,7,8,9), which
   contribute weight to the Dirac construction? Which don't?
4. Of TSML's structural features (idempotents, σ-permutation, 6-cycle,
   bumps), which intersect with Dirac's image and which sit outside?
5. What's the residue — the part of TSML's so(8) that is COMPLEMENTARY
   to Dirac's so(1,3)?
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
non_flow = [0, 5, 7, 9]

# --- Build so(8) on V_8 ---
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

F = [A[i] for i in flow_indices]
so8_vecs, so8_mats = lie_closure(F)
print(f"so(8) Lie closure on R^10: dim = {len(so8_mats)}")

all_imgs = np.hstack([m for m in so8_mats])
U, S, _ = np.linalg.svd(all_imgs, full_matrices=True)
rank = int(np.sum(S > 1e-9 * S[0]))
V8_basis = U[:, :rank]
print(f"V_8 basis (10 x 8) — projects R^10 onto invariant 8-dim subspace")

# Show which R^10 indices participate in V_8
V8_squared = V8_basis ** 2  # (10, 8)
contribution_per_index = V8_squared.sum(axis=1)  # length 10
print(f"\nHow much each R^10 basis vector e_i contributes to V_8:")
print(f"  (squared norm of projection onto V_8)")
for i in range(10):
    print(f"  e_{i}: {contribution_per_index[i]:.4f}")

# --- Build the Dirac sub-action on V_8 ---
sigma_1 = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_3 = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)
Z2 = np.zeros((2,2), dtype=complex)
gamma_0 = np.block([[Z2, I2], [I2, Z2]])
gamma_1 = np.block([[Z2, sigma_1], [-sigma_1, Z2]])
gamma_2 = np.block([[Z2, sigma_2], [-sigma_2, Z2]])
gamma_3 = np.block([[Z2, sigma_3], [-sigma_3, Z2]])
dirac = [gamma_0, gamma_1, gamma_2, gamma_3]

M_tilde = {}
for i in [1, 2, 3]:
    M_tilde[(0, i)] = (1j / 2) * gamma_0 @ dirac[i]
for i, j in [(1,2), (1,3), (2,3)]:
    M_tilde[(i, j)] = (1.0 / 4.0) * (dirac[i] @ dirac[j] - dirac[j] @ dirac[i])

def cplx_to_real8(M):
    return np.block([[np.real(M), -np.imag(M)], [np.imag(M), np.real(M)]])

M_real8 = {k: cplx_to_real8(M) for k, M in M_tilde.items()}

# Lift M_real8 from R^8 (Dirac's frame) back to R^10 (TIG's frame)
# This requires choosing the embedding R^8 → V_8 → R^10. We use V_8_basis.
# So Dirac's σ^μν as 10×10 matrices: V8_basis @ M_real8 @ V8_basis.T
M_in_R10 = {k: V8_basis @ M @ V8_basis.T for k, M in M_real8.items()}

# Now I have the 6 Dirac generators as 10x10 matrices in TIG's frame.
# Question 1: which TSML INDEX-pairs (i, j) participate in each Dirac generator?

print("\n" + "="*70)
print("Q1: Which R^10 indices participate in each Dirac generator?")
print("="*70)

for (mu, nu), M in M_in_R10.items():
    # Find which indices have nonzero entries
    abs_M = np.abs(M)
    threshold = 1e-6
    active_indices = set()
    for i in range(10):
        for j in range(10):
            if abs_M[i, j] > threshold:
                active_indices.add(i)
                active_indices.add(j)
    inactive = set(range(10)) - active_indices
    print(f"\n  M̃^{mu}{nu} (10x10):")
    print(f"    active indices: {sorted(active_indices)}")
    print(f"    inactive indices: {sorted(inactive)}")
    # Show distribution of weight by index
    weight_per_index = np.abs(M).sum(axis=1) + np.abs(M).sum(axis=0)  # row+col activity
    nonzero_weights = [(i, weight_per_index[i]) for i in range(10) if weight_per_index[i] > threshold]
    nonzero_weights.sort(key=lambda x: -x[1])
    print(f"    weight per index (top 5): {nonzero_weights[:5]}")

print("\n" + "="*70)
print("Q2: Which TSML CELLS (i,j positions) get weight from each Dirac gen?")
print("="*70)

# Sum |M_in_R10| across all 6 Dirac generators to see the cumulative footprint
total_dirac_footprint = np.zeros((10, 10))
for k, M in M_in_R10.items():
    total_dirac_footprint += np.abs(M)

# Threshold and visualize
print("\nCumulative |Dirac footprint| on R^10 (sum of |M̃^μν| over all 6):")
for i in range(10):
    row_str = ""
    for j in range(10):
        val = total_dirac_footprint[i, j]
        if val < 1e-6:
            row_str += "  . "
        else:
            row_str += f"{val:>4.2f}"
    print(f"  row {i}: {row_str}")

# Compare to TSML's actual structure
print("\nTSML cell values for comparison:")
for i in range(10):
    row_str = ""
    for j in range(10):
        v = T[i, j]
        if v == 0:
            row_str += "  . "
        elif v == 7:
            row_str += "  H "  # HARMONY
        else:
            row_str += f"{v:>3} "
    print(f"  row {i}: {row_str}")

# Question: which TSML "bump" cells (non-7, non-0) get nonzero Dirac weight?
print("\n" + "="*70)
print("Q3: Where do TSML's BUMPS sit relative to Dirac's footprint?")
print("="*70)
bumps = []
for i in range(10):
    for j in range(10):
        if T[i,j] not in [0, 7]:
            bumps.append((i, j, int(T[i,j])))
print(f"\nTSML has {len(bumps)} bump cells (non-0, non-7 values):")
for (i, j, v) in bumps:
    dirac_weight = total_dirac_footprint[i, j]
    touched = dirac_weight > 1e-6
    print(f"  T[{i},{j}] = {v} (bump):  Dirac weight = {dirac_weight:.4f}  {'TOUCHED' if touched else 'untouched'}")

# Q4: structural features intersection
print("\n" + "="*70)
print("Q4: Structural features — what does Dirac TOUCH and LEAVE ALONE?")
print("="*70)

# Idempotents: {0, 3, 8, 9}  (per σ permutation)
idempotents = [0, 3, 8, 9]
six_cycle = [1, 7, 6, 5, 4, 2]

print("\nIdempotents {0, 3, 8, 9} — fixed points of σ permutation:")
for idx in idempotents:
    # how much weight does Dirac place on row/col idx?
    weight = total_dirac_footprint[idx, :].sum() + total_dirac_footprint[:, idx].sum()
    in_v8 = contribution_per_index[idx]
    print(f"  index {idx}: V_8 contribution = {in_v8:.4f}, Dirac weight = {weight:.4f}")

print("\n6-cycle (1, 7, 6, 5, 4, 2) elements:")
for idx in six_cycle:
    weight = total_dirac_footprint[idx, :].sum() + total_dirac_footprint[:, idx].sum()
    in_v8 = contribution_per_index[idx]
    print(f"  index {idx}: V_8 contribution = {in_v8:.4f}, Dirac weight = {weight:.4f}")

# Q5: complementary subalgebra
print("\n" + "="*70)
print("Q5: What's the COMPLEMENT — what part of so(8) Dirac doesn't touch?")
print("="*70)

# so(8) is 28-dim. Dirac's so(1,3) inside it is 6-dim. The complement is 22-dim.
# Compute the orthogonal complement (in Frobenius inner product on so(8))

so8_vec_basis = np.array([m.flatten() for m in so8_mats]).T  # 100 x 28
U_so8, S_so8, Vt_so8 = np.linalg.svd(so8_vec_basis, full_matrices=False)
so8_orthonormal = U_so8[:, :28]  # 100 x 28

# Dirac generators as 100-vectors (now they live in R^10 frame)
dirac_vecs = np.array([M.flatten() for M in M_in_R10.values()]).T  # 100 x 6
# Project onto so(8) orthonormal basis
dirac_in_so8 = so8_orthonormal.T @ dirac_vecs  # 28 x 6
# Orthogonalize the 6 Dirac vectors in the so(8) coordinate system
Q_dirac, R_dirac = np.linalg.qr(dirac_in_so8)
print(f"Dirac so(1,3) sub-algebra: 6-dim inside so(8) of dim 28")
print(f"Dirac coefficients matrix shape: {dirac_in_so8.shape}")
print(f"Rank of Dirac span in so(8): {np.linalg.matrix_rank(dirac_in_so8)}")

# Build the 22-dim COMPLEMENT
# Q_dirac (28 x 6) is orthonormal in so(8) coordinates spanning Dirac
# Find 22 orthogonal directions
from numpy.linalg import qr
# Augment with random + Gram-Schmidt
np.random.seed(0)
random_dirs = np.random.randn(28, 30)
combined = np.hstack([Q_dirac, random_dirs])
Q_full, _ = qr(combined)
complement_basis = Q_full[:, 6:28]  # 28 x 22, orthogonal to Dirac
print(f"Complement basis shape (in so(8) coords): {complement_basis.shape}")

# Lift complement back to 10x10 matrix space
complement_in_R10 = []
for i in range(22):
    coeffs = complement_basis[:, i]  # 28 vector
    # Express in the original so(8) basis (column space of so8_orthonormal)
    M_vec = so8_orthonormal @ coeffs  # 100 vector
    M = M_vec.reshape(10, 10)
    complement_in_R10.append(M)

# Total weight of the complement on each index
complement_footprint = np.zeros((10, 10))
for M in complement_in_R10:
    complement_footprint += np.abs(M)

print("\nComplement (so(8) minus so(1,3)_Dirac) cumulative |footprint|:")
for i in range(10):
    row_str = ""
    for j in range(10):
        val = complement_footprint[i, j]
        if val < 1e-6:
            row_str += "  . "
        elif val < 0.5:
            row_str += "  ~ "
        else:
            row_str += f"{val:>4.1f}"
    print(f"  row {i}: {row_str}")

# Per-index activity for complement vs Dirac
print("\nPer-index footprint comparison (Dirac vs Complement):")
print(f"{'idx':<5} {'V_8 contrib':<14} {'Dirac':<10} {'Complement':<12} {'Ratio C/D':<10}")
for i in range(10):
    d = total_dirac_footprint[i, :].sum() + total_dirac_footprint[:, i].sum()
    c = complement_footprint[i, :].sum() + complement_footprint[:, i].sum()
    v8 = contribution_per_index[i]
    if d > 1e-6:
        ratio = c / d
        print(f"  {i:<5} {v8:<14.4f} {d:<10.3f} {c:<12.3f} {ratio:<10.2f}")
    else:
        print(f"  {i:<5} {v8:<14.4f} {d:<10.3f} {c:<12.3f} (Dirac=0)")

# What are the BUMP indices' complement footprints?
print("\nBump positions: Dirac weight vs Complement weight at each:")
for (i, j, v) in bumps:
    d_w = total_dirac_footprint[i, j]
    c_w = complement_footprint[i, j]
    print(f"  T[{i},{j}]={v}:  Dirac={d_w:.3f}  Complement={c_w:.3f}")
