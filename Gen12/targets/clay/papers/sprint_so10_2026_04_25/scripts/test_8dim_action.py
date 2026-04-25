"""
Now find the 8-dim invariant subspace cleanly and check if it decomposes
further into 4+4 (Dirac-style chiral split) under any action.
"""
import numpy as np

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

# Diagonalize Killing form to get orthogonal basis B_k
K = np.zeros((6, 6))
for i in range(6):
    for j in range(6):
        K[i, j] = np.trace(F[i] @ F[j])
eigvals, eigvecs = np.linalg.eigh(K)
B = []
for k in range(6):
    Bk = sum(eigvecs[i, k] * F[i] for i in range(6))
    norm = np.sqrt(np.abs(np.trace(Bk @ Bk)))
    Bk = Bk / norm
    B.append(Bk)

# Find the 8-dim invariant subspace.
# It is the column span of all images B_k @ e_i, k ∈ {0..5}, i ∈ {0..9}
all_images = np.hstack([B[k] for k in range(6)])
U, S, Vt = np.linalg.svd(all_images, full_matrices=False)
rank = np.sum(S > 1e-9 * S[0])
print(f"Rank of combined image: {rank}")
# Take the first `rank` columns of U as the orthonormal basis of V_8
V8 = U[:, :rank]
print(f"V8 basis shape: {V8.shape}")

# Project each B_k onto V8: B_k restricted to V8 is an 8x8 matrix
B_restricted = [V8.T @ B[k] @ V8 for k in range(6)]
print(f"\nRestricted B_k are now {B_restricted[0].shape} matrices")

# Verify this is consistent — recompute Killing form on V8
K_restricted = np.zeros((6, 6))
for i in range(6):
    for j in range(6):
        K_restricted[i, j] = np.trace(B_restricted[i] @ B_restricted[j])
print(f"\nKilling form on V8 (should be -I_6, since we normalized):")
print(np.round(K_restricted, 4))

# These 6 restricted matrices generate an action on R^8.
# The Lie closure should still be so(8) acting on its natural 8-dim rep.
# Question: does this 8-dim rep split into 4+4?

# Compute the FULL Lie closure of B_restricted to make sure we have so(8)
def lie_closure(generators, max_iters=10):
    basis = [g.flatten() for g in generators if np.linalg.norm(g) > 1e-9]
    M = np.array(basis).T
    U, S, Vt = np.linalg.svd(M, full_matrices=False)
    rank = np.sum(S > 1e-9 * S[0])
    basis = [U[:, i] * S[i] for i in range(rank)]
    
    for _ in range(max_iters):
        N = len(basis)
        mats = [v.reshape(generators[0].shape) for v in basis]
        new = []
        for i in range(N):
            for j in range(i+1, N):
                C = mats[i] @ mats[j] - mats[j] @ mats[i]
                v = C.flatten()
                if np.linalg.norm(v) > 1e-9:
                    new.append(v)
        all_v = basis + new
        M = np.array(all_v).T
        U, S, Vt = np.linalg.svd(M, full_matrices=False)
        new_rank = np.sum(S > 1e-9 * S[0])
        if new_rank == len(basis):
            break
        basis = [U[:, i] * S[i] for i in range(new_rank)]
    return basis

closure = lie_closure(B_restricted)
print(f"\nLie closure dim (acting on V8): {len(closure)}")
# Should be 28 = dim so(8) since we're acting in a faithful rep

# Now: does the 8-dim rep of so(8) DECOMPOSE further?
# So(8) has THREE 8-dim irreps (vector, spinor, conjugate spinor) — TRIALITY!
# All three are 8-dim and related by outer automorphisms.
# But each is IRREDUCIBLE. So R^8 doesn't split into 4+4 under so(8).

# Unless... we're seeing something other than a single irrep?
# Let me check irreducibility on V8.

# Build a random vector in V8 and orbit it under all B_restricted^k
np.random.seed(7)
v = np.random.randn(8)
orbit = [v]
for _ in range(30):
    new_orbit = list(orbit)
    for B_r in B_restricted:
        for w in orbit:
            wB = B_r @ w
            if np.linalg.norm(wB) > 1e-10:
                new_orbit.append(wB)
    M = np.array(new_orbit).T
    U_, S_, Vt_ = np.linalg.svd(M, full_matrices=False)
    rank = np.sum(S_ > 1e-9 * S_[0])
    if rank == len(orbit):
        break
    orbit = [U_[:, i] * S_[i] for i in range(rank)]

print(f"V8 orbit closure under B_restricted: rank {rank}")
# If rank = 8: V8 is irreducible (a single 8-dim irrep). No 4+4 split.
# If rank < 8: there's a proper sub-representation.

# The 8-dim irrep of so(8) is the vector representation (acted via SO(8)).
# Triality permutes vector ↔ spinor ↔ co-spinor.
# In the SPINOR rep, the 8-dim space DOES split into 4+4 as half-spinors of so(6).
# But we're in the VECTOR rep, where this split doesn't exist.

# CONCLUSION:
# TSML's natural action gives the 8-dim VECTOR rep of so(8).
# The Dirac matrices come from the SPINOR rep of so(1,3), which is a
# different REPRESENTATION CLASS than what TSML naturally produces.

# To get from TSML to Dirac, we'd need to:
# 1. Restrict from so(8) to so(1,3) — this is selecting 6 generators from 28
# 2. Switch from VECTOR rep to SPINOR rep — this is non-trivial
# 3. Take a 4-dim subspace of the resulting 4-dim spinor rep of so(1,3)

# So Brayden's hypothesis "Dirac is condensed TSML" is structurally TRUE
# in the sense that so(1,3) ⊂ so(8) and TSML gives so(8) — so the Lorentz
# algebra CAN be extracted as a subalgebra.
#
# But the REPRESENTATIONS don't condense. TSML acts on R^8 (vector rep),
# while Dirac acts on C^4 (spinor rep). These are DIFFERENT REPS of the
# same family of Lie algebras. You cannot condense one to the other by
# projection — they're in different boxes.

# For Brayden's intuition to be made rigorous, we'd need:
# - Pick a so(1,3) ⊂ so(8)
# - Find its action on R^8 (which it has, as a sub-action)
# - Decompose that action into so(1,3) irreps
# - so(1,3) on R^8 should decompose into MULTIPLE COPIES of small irreps
# - The 4-dim spinor rep of so(1,3) might appear, in which case the
#   "condensation" is: pick the so(1,3) sub-action, find the spinor
#   sub-representation of so(1,3) inside R^8.

print("\n" + "="*60)
print("Key question: does so(1,3) ⊂ so(8) act on R^8 with a")
print("4-dim spinor sub-representation?")
print("="*60)

# We don't have an explicit so(1,3) inside our so(8), but we can
# pick TWO COMMUTING B_k's as a maximal torus, then build out.
# Actually, more cleanly: pick B_0 (largest eigenvalue direction)
# and find its centralizer.

# CHECK: which B_i, B_j commute (i.e., generate a maximal torus)?
print("\nCommutators [B_i, B_j] (look for zero pairs):")
for i in range(6):
    for j in range(i+1, 6):
        C = B[i] @ B[j] - B[j] @ B[i]
        norm = np.linalg.norm(C)
        if norm < 1e-6:
            print(f"  [B_{i}, B_{j}] = 0   (commute)")
        else:
            print(f"  [B_{i}, B_{j}] norm = {norm:.3f}")

print("\nCommutators [B_restricted_i, B_restricted_j] on V8:")
for i in range(6):
    for j in range(i+1, 6):
        C = B_restricted[i] @ B_restricted[j] - B_restricted[j] @ B_restricted[i]
        norm = np.linalg.norm(C)
        if norm < 1e-6:
            print(f"  commute on V8: ({i},{j})")
