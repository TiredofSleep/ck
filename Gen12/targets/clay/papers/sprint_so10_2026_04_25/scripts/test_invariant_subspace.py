"""
Brayden's hypothesis: Dirac is a CONDENSED FORM of TSML.

The right test: does there exist a 4-dim subspace V of R^10 (or C^10)
that is invariant under some so(1,3) subalgebra of so(8) (which we have),
AND on which the so(1,3) generators act via standard Dirac matrices?

Approach:
1. Find a so(1,3) subalgebra inside our so(8). 
   so(1,3) needs: 6 generators, with structure constants matching Lorentz.
2. For each candidate so(1,3) subalgebra, find its invariant subspaces.
3. Check whether the 4-dim ones admit a Dirac-style action.

But I notice something simpler first: the Killing eigenvalue spectrum
[-71.27, -8.20, -4.00, -2.92, -2.73, -0.88] has unusual structure.
The largest eigenvalue is ~9x the next; there's clearly a "principal"
direction. Let me see if dropping that principal direction gives a
cleaner sub-structure.

Also: notice the ratio -71.27 / -8.20 = 8.69 (not clean).
But -71.27 + (other 5) = trace = -90. The other 5 sum to -18.73.
  -8.20 - 4.00 - 2.92 - 2.73 - 0.88 = -18.73 ✓
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
F = [A[i].astype(float) for i in flow_indices]

# Diagonalize Killing form
K = np.zeros((6, 6))
for i in range(6):
    for j in range(6):
        K[i, j] = np.trace(F[i] @ F[j])

eigvals, eigvecs = np.linalg.eigh(K)
print(f"Killing eigenvalues: {eigvals}")
B = []
for k in range(6):
    Bk = sum(eigvecs[i, k] * F[i] for i in range(6))
    # Normalize so Killing form has ±1 entries
    norm = np.sqrt(np.abs(np.trace(Bk @ Bk)))
    Bk = Bk / norm
    B.append(Bk)

# Verify normalized Killing
K_norm = np.zeros((6, 6))
for i in range(6):
    for j in range(6):
        K_norm[i, j] = np.trace(B[i] @ B[j])
print(f"\nNormalized Killing diagonal: {np.diag(K_norm)}")
# Should be -1 for all (compact signature)

# Now ask: is there a 4-dim subspace V of R^10 such that 6 of these B_k
# preserve V and act on V like Dirac generators of so(1,3)?

# Strategy: look at common eigenspaces.
# Better: for each B_k, find its kernel and image. The KERNEL of B_k
# is a B_k-invariant subspace. If multiple B_k share a common kernel
# of dim 4, that's a candidate V.

print("\nKernels of B_k:")
for k in range(6):
    # SVD to find kernel
    U, S, Vt = np.linalg.svd(B[k])
    rank = np.sum(S > 1e-9)
    kernel_dim = 10 - rank
    # kernel is span of last rows of Vt
    kernel = Vt[rank:].T  # 10 x kernel_dim
    print(f"  B_{k}: rank={rank}, kernel dim={kernel_dim}")

# Each B_k has rank ~9 (since they're antisymmetric integer matrices
# from a finite table — likely rank 8 in general).
# Let me check for *common* invariant subspaces by looking at simultaneous
# block structure.

# An invariant subspace V of dim 4 means: B_k V ⊆ V for all selected k.
# If V is a 4-dim subspace, choose 4 basis vectors v_1, ..., v_4.
# B_k v_i must be a linear combination of v_1, ..., v_4.

# Check: is there an obvious 4-dim invariant subspace?
# The table T has VOID column 0 (acts trivially on column 0).
# That suggests the subspace where x_0 is the "anchor" might be
# special. But that's only 1-dim.

# Try: what's the span of B_k @ e_1, B_k @ e_2, ..., for various e?
# Generate all images:
print("\nPushing standard basis through {B_k}:")
ranks_per_subset = {}
for subset_size in [3, 4, 5, 6]:
    for subset in combinations(range(6), subset_size):
        # Apply all B_k in subset to all basis vectors, compute total rank
        all_vecs = []
        for k in subset:
            for i in range(10):
                v = B[k][:, i]
                if np.linalg.norm(v) > 1e-10:
                    all_vecs.append(v)
        if len(all_vecs) == 0:
            continue
        M = np.array(all_vecs).T
        rank = np.linalg.matrix_rank(M, tol=1e-9)
        ranks_per_subset.setdefault(subset_size, []).append((subset, rank))

for size, items in ranks_per_subset.items():
    items.sort(key=lambda x: x[1])
    print(f"  subsets of size {size}: smallest combined rank = {items[0][1]}, largest = {items[-1][1]}")

# If rank for some subset = 4, we have an invariant 4-dim subspace
# spanned by the images of {B_k}. Let's check more carefully.

# Search for INVARIANT 4-dim subspaces using simultaneous block-diagonalization
print("\nSearching for common invariant subspaces of B_k's...")

# Approach: take a random vector v, compute orbit closure under all B_k.
# If orbit closure is exactly 4-dim, that's an invariant subspace.

np.random.seed(42)
for trial in range(20):
    v0 = np.random.randn(10)
    orbit = [v0]
    for _ in range(20):  # iterate
        new_orbit = list(orbit)
        for k in range(6):
            for w in orbit:
                Bw = B[k] @ w
                if np.linalg.norm(Bw) > 1e-10:
                    new_orbit.append(Bw)
        # Compute rank
        M = np.array(new_orbit).T
        rank = np.linalg.matrix_rank(M, tol=1e-9)
        if rank == len(orbit):
            break  # closed
        # Take first `rank` independent
        Q, R = np.linalg.qr(M)
        orbit = [Q[:, i] for i in range(rank)]
    if rank < 10:
        print(f"  Trial {trial}: orbit closure dim = {rank}")
        if rank == 4:
            print(f"    !!! 4-dim invariant subspace found !!!")

# If no proper invariant subspaces, the rep is irreducible on R^10.
# But R^10 is the natural rep of SO(10)... and we have so(8) ⊂ so(10)
# acting. so(8) acting on R^10 should DECOMPOSE: R^10 = R^1 + R^1 + R^8
# (the two "extra" directions plus the 8-dim vector rep of so(8)).

# Let's check if our B_k stabilize the index-0 and index-7 directions
# (VOID and HARMONY).
print("\nChecking VOID (e_0) and HARMONY (e_7) stability:")
for k in range(6):
    e0 = np.zeros(10); e0[0] = 1
    e7 = np.zeros(10); e7[7] = 1
    B_e0 = B[k] @ e0
    B_e7 = B[k] @ e7
    e0_stable = np.linalg.norm(B_e0 - B_e0[0]*e0) < 1e-9  # only e_0 component nonzero
    e7_stable = np.linalg.norm(B_e7 - B_e7[7]*e7) < 1e-9
    print(f"  B_{k} e_0: norm = {np.linalg.norm(B_e0):.3f}, e_0-only: {e0_stable}")
    print(f"  B_{k} e_7: norm = {np.linalg.norm(B_e7):.3f}, e_7-only: {e7_stable}")
