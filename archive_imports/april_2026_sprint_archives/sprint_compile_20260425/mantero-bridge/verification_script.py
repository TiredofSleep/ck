"""
verification_script.py

Verifies the structural claim posted on MathOverflow:

    Let G = ⟨P_56, σ³⟩ ⊂ O(10) where:
      • P_56 = single transposition swapping indices 5 ↔ 6
      • σ³ = product of three disjoint transpositions: (1↔5)(7↔4)(6↔2)
        with four fixed indices {0, 3, 8, 9}.
    
    G has order 8 (≅ D_4). Acting by conjugation on so(10), the 
    trivial-isotypic component is a 16-dim Lie subalgebra with 
    Killing spectrum (−4)^15 ⊕ (0)^1, identifying it as su(4) ⊕ u(1).

This script reproduces all claims at machine precision. Pure numpy, 
no external dependencies.
"""
import numpy as np

# ---------------------------------------------------------------------
# The two involutions
# ---------------------------------------------------------------------

# P_56: single transposition swapping 5 and 6
P56 = np.eye(10)
P56[5, 5] = 0; P56[6, 6] = 0
P56[5, 6] = 1; P56[6, 5] = 1

# σ³: product of three disjoint transpositions
# σ has 6-cycle (1, 7, 6, 5, 4, 2) and 4 fixed points {0, 3, 8, 9}
# σ³ swaps: (1,5), (7,4), (6,2); fixes {0, 3, 8, 9}
sigma_perm = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
P_sigma = np.zeros((10, 10))
for i in range(10):
    P_sigma[sigma_perm[i], i] = 1.0
sigma3 = np.linalg.matrix_power(P_sigma, 3)

# Both are involutions
assert np.allclose(P56 @ P56, np.eye(10))
assert np.allclose(sigma3 @ sigma3, np.eye(10))

# They do NOT commute
assert not np.allclose(P56 @ sigma3, sigma3 @ P56)

# ---------------------------------------------------------------------
# Generate the group G = ⟨P_56, σ³⟩
# ---------------------------------------------------------------------

group_mats = [np.eye(10)]
seen_keys = {tuple(np.eye(10).flatten())}
queue = [np.eye(10)]
while queue:
    g = queue.pop()
    for s in [P56, sigma3]:
        h = g @ s
        key = tuple(np.round(h.flatten(), 6))
        if key not in seen_keys:
            seen_keys.add(key)
            group_mats.append(h)
            queue.append(h)

assert len(group_mats) == 8, f"Group has {len(group_mats)} elements, expected 8"
print(f"✓ Group G = ⟨P_56, σ³⟩ has order {len(group_mats)} (D_4)")

# ---------------------------------------------------------------------
# Build so(10) basis
# ---------------------------------------------------------------------

so10_basis = []
for i in range(10):
    for j in range(i+1, 10):
        E = np.zeros((10, 10))
        E[i, j] = 1
        E[j, i] = -1
        so10_basis.append(E)
assert len(so10_basis) == 45

# ---------------------------------------------------------------------
# Project onto G-invariants (trivial isotypic component)
# ---------------------------------------------------------------------

invariants = []
for E in so10_basis:
    avg = sum(g @ E @ g.T for g in group_mats) / len(group_mats)
    if np.linalg.norm(avg) > 1e-9:
        invariants.append(avg)

# Get an orthonormal basis for the invariant subspace
flat = np.array([P.flatten() for P in invariants]).T
U, S, _ = np.linalg.svd(flat, full_matrices=False)
inv_dim = int(np.sum(S > 1e-9 * S[0]))
inv_basis = [U[:, k].reshape(10, 10) for k in range(inv_dim)]

assert inv_dim == 16, f"Invariant subspace has dim {inv_dim}, expected 16"
print(f"✓ Trivial-isotypic component has dim {inv_dim}")

# ---------------------------------------------------------------------
# Verify it closes under bracket (is a Lie subalgebra)
# ---------------------------------------------------------------------

def lie_closure_dim(generators, max_iters=15):
    if not generators:
        return 0
    shape = generators[0].shape
    bv = [g.flatten() for g in generators if np.linalg.norm(g) > 1e-9]
    if not bv:
        return 0
    M = np.array(bv).T
    U, S, _ = np.linalg.svd(M, full_matrices=False)
    rank = int(np.sum(S > 1e-9 * S[0]))
    bv = [U[:, i] for i in range(rank)]
    for _ in range(max_iters):
        N = len(bv)
        mats = [v.reshape(shape) for v in bv]
        new = []
        for i in range(N):
            for j in range(i + 1, N):
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
    return len(bv)

closure = lie_closure_dim(inv_basis)
assert closure == 16, f"Closure has dim {closure}, expected 16"
print(f"✓ Subspace closes under Lie bracket (Lie subalgebra of dim {closure})")

# ---------------------------------------------------------------------
# Compute the Killing form of the 16-dim subalgebra
# ---------------------------------------------------------------------

n = 16
K = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        # ad_i: matrix of Lie bracket [X_i, ·] in the basis
        ad_i = np.zeros((n, n))
        for k in range(n):
            commk = inv_basis[i] @ inv_basis[k] - inv_basis[k] @ inv_basis[i]
            for l in range(n):
                ad_i[l, k] = np.sum(commk * inv_basis[l])
        ad_j = np.zeros((n, n))
        for k in range(n):
            commk = inv_basis[j] @ inv_basis[k] - inv_basis[k] @ inv_basis[j]
            for l in range(n):
                ad_j[l, k] = np.sum(commk * inv_basis[l])
        K[i, j] = np.trace(ad_i @ ad_j)

eigs = sorted(np.linalg.eigvalsh(K))
n_at_minus4 = sum(1 for e in eigs if abs(e + 4) < 1e-6)
n_at_zero = sum(1 for e in eigs if abs(e) < 1e-6)

assert n_at_minus4 == 15, f"Got {n_at_minus4} eigenvalues at −4, expected 15"
assert n_at_zero == 1, f"Got {n_at_zero} zero eigenvalues, expected 1"
print(f"✓ Killing form: 15 eigenvalues at exactly −4, 1 at exactly 0")

# ---------------------------------------------------------------------
# Verify the center is 1-dimensional
# ---------------------------------------------------------------------

# Z is central iff [Z, X_j] = 0 for all j
# Build the linear constraint matrix
M_constraint = np.zeros((100 * n, n))
for j in range(n):
    for k in range(n):
        commk = inv_basis[k] @ inv_basis[j] - inv_basis[j] @ inv_basis[k]
        M_constraint[j*100:(j+1)*100, k] = commk.flatten()

U_c, S_c, _ = np.linalg.svd(M_constraint, full_matrices=True)
center_dim = n - int(np.sum(S_c > 1e-9))
assert center_dim == 1, f"Center has dim {center_dim}, expected 1"
print(f"✓ Center is exactly {center_dim}-dimensional")

# ---------------------------------------------------------------------
# Conclusion
# ---------------------------------------------------------------------

print()
print("=" * 60)
print("All claims verified at machine precision.")
print()
print("The trivial-isotypic component of so(10) under D_4 = ⟨P_56, σ³⟩")
print("is a 16-dim Lie subalgebra with structure:")
print()
print("    su(4) ⊕ u(1)")
print()
print("    (15-dim simple part: so(6) ≅ su(4) ≅ A_3)")
print("    (1-dim center: u(1))")
print("=" * 60)
