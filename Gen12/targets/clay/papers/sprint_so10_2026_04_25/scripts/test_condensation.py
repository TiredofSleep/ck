"""
TEST: is Dirac a condensed form of TSML+BHML?

Plan:
1. Build TSML's flow operators A_1, A_2, A_3, A_4, A_6, A_8 (6 generators)
2. so(8) closure has dim 28; this is 10x10 matrices.
3. so(1,3) has dim 6 and is a subalgebra of so(8).
4. Find the so(1,3) subalgebra inside the so(8) we already have.
5. Compute its representation: is there a 4-dim subspace V of R^10 stable
   under so(1,3), where so(1,3) acts via Dirac-like generators?

If yes: Dirac IS a condensed form. The "condensation" is restriction
to a 4-dim subspace.

If the natural 4-dim subspace acts via genuine Dirac matrices (with
anticommutator = 2η × I), the claim is verified. If not, we'll see
what kind of object it actually is.
"""
import numpy as np
from itertools import combinations

# --- Build TSML and its operators ---
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
F = [A[i] for i in flow_indices]  # 6 antisymmetric matrices

# Step 1: build the so(8) closure and check we get dim 28
def collect_lie_closure(generators, max_iters=10):
    """Collect generators + commutators iteratively until closed."""
    basis = []
    # Start with generators (vectorized)
    for g in generators:
        v = g.flatten().astype(float)
        if np.linalg.norm(v) > 1e-10:
            basis.append(v)
    
    # Reduce to linearly independent set
    M = np.array(basis).T
    Q, R = np.linalg.qr(M)
    rank = np.sum(np.abs(np.diag(R)) > 1e-9)
    
    for it in range(max_iters):
        # Compute all commutators of current basis
        new_vecs = []
        N = len(basis)
        # Reconstruct matrices from vectors
        mats = [v.reshape(10, 10) for v in basis]
        for i in range(N):
            for j in range(i+1, N):
                C = mats[i] @ mats[j] - mats[j] @ mats[i]
                v = C.flatten()
                if np.linalg.norm(v) > 1e-10:
                    new_vecs.append(v)
        
        # Add to basis if independent
        all_vecs = basis + new_vecs
        M = np.array(all_vecs).T
        # Use SVD for stable rank
        U, S, Vt = np.linalg.svd(M, full_matrices=False)
        new_rank = np.sum(S > 1e-9 * S[0])
        
        if new_rank == len(basis):
            break  # closed
        
        # Take new_rank independent columns
        # Use QR with pivoting (or just pick largest singular vectors)
        # Simpler: pick columns by Gram-Schmidt
        new_basis = []
        for v in all_vecs:
            # Project against existing
            r = v.copy()
            for b in new_basis:
                r = r - np.dot(r, b) / np.dot(b, b) * b
            if np.linalg.norm(r) > 1e-10:
                new_basis.append(r)
        basis = new_basis
        if len(basis) >= n*n:  # max possible dim
            break
    
    return basis

so8_basis = collect_lie_closure(F)
print(f"Closed Lie algebra dimension: {len(so8_basis)}")

# Should be 28 if WP11 is correct
# (with our specific A_i, the closure may be slightly different —
# verify against expected so(8) dim)

# Step 2: find so(1,3) subalgebra — three rotations + three boosts
# In so(n), a so(p,q) subalgebra is identified by a basis where 
# certain pairs of generators commute, others anticommute under bilinear form.
# 
# Simplest approach: find three commuting pairs among our generators,
# representing rotations and boosts in 4-dim Minkowski space.

# Reconstruct flow matrices
F_mats = F.copy()

# Compute the Killing form (we already know it's 6x6, neg def, det 16384)
print("\nKilling form among flow generators:")
K = np.zeros((6, 6))
for i in range(6):
    for j in range(6):
        K[i, j] = np.trace(F_mats[i] @ F_mats[j])
print(K)
print(f"Eigenvalues: {sorted(np.linalg.eigvals(K).real)}")

# Step 3: Diagonalize K to find orthogonal basis
eigvals, eigvecs = np.linalg.eigh(K)
print(f"\nEigenvalues (sorted): {eigvals}")
print(f"Eigenvalue ratios: {eigvals / eigvals[0]}")

# Build orthogonal basis: B_k = sum_i eigvecs[i,k] * F_mats[i]
# Each B_k satisfies tr(B_k B_l) = eigvals[k] * delta_{kl}
B = []
for k in range(6):
    Bk = sum(eigvecs[i, k] * F_mats[i] for i in range(6))
    B.append(Bk)

# Verify orthogonalization
print("\nDiagonalized Killing form (should be diagonal with eigvals):")
for i in range(6):
    for j in range(6):
        val = np.trace(B[i] @ B[j])
        print(f"{val:8.2f}", end=" ")
    print()

# Step 4: check anticommutators of the diagonalized basis
print("\nAnticommutators {B_i, B_j} of diagonalized basis:")
print("(if Dirac-like, these should be diagonal, with eigvals on diagonal)")
print()

for i in range(6):
    for j in range(i, 6):
        anti = B[i] @ B[j] + B[j] @ B[i]
        # Check: is it close to scalar * I?
        diag = np.diag(anti)
        offdiag = anti - np.diag(diag)
        diag_constant = np.std(diag)
        offdiag_norm = np.linalg.norm(offdiag)
        anti_norm = np.linalg.norm(anti)
        if anti_norm > 1e-9:
            scalar_quality = 1 - (offdiag_norm + diag_constant * np.sqrt(10)) / anti_norm
        else:
            scalar_quality = 1.0
        if i == j:
            mean_diag = np.mean(diag)
            print(f"  {{B_{i},B_{i}}} = 2*B_{i}^2: mean diag={mean_diag:.3f}, "
                  f"std diag={diag_constant:.3f}, off-diag norm={offdiag_norm:.3f}")
        else:
            print(f"  {{B_{i},B_{j}}}: max abs={np.max(np.abs(anti)):.3f}, "
                  f"std diag={diag_constant:.3f}, off-diag norm={offdiag_norm:.3f}")

# If even after diagonalization the anticommutators aren't clean,
# it confirms TSML is genuinely an adjoint-rep object, not spinor.
# Let's see.
