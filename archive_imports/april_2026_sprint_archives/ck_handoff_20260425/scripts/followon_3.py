"""
Follow-on 3: extend the analysis to TSML + BHML giving so(10).

BHML transcribed from screenshot:
Row 0: 0 1 2 3 4 5 6 7 8 9
Row 1: 1 2 3 4 5 6 7 2 6 6
Row 2: 2 3 3 4 5 6 7 3 6 6
Row 3: 3 4 4 4 5 6 7 4 6 6
Row 4: 4 5 5 5 5 6 7 5 7 7
Row 5: 5 6 6 6 6 6 7 6 7 7
Row 6: 6 7 7 7 7 7 7 7 7 7
Row 7: 7 2 3 4 5 6 7 8 9 0
Row 8: 8 6 6 6 7 7 7 9 7 8
Row 9: 9 6 6 6 7 7 7 0 8 0

TSML (= CL, top of screenshot, what we've been using):
Row 0: 0 0 0 0 0 0 0 7 0 0
Row 1: 0 7 3 7 7 7 7 7 7 7
Row 2: 0 3 7 7 4 7 7 7 7 9
Row 3: 0 7 7 7 7 7 7 7 7 3
Row 4: 0 7 4 7 7 7 7 7 8 7
Row 5: 0 7 7 7 7 7 7 7 7 7
Row 6: 0 7 7 7 7 7 7 7 7 7
Row 7: 7 7 7 7 7 7 7 7 7 7
Row 8: 0 7 7 7 8 7 7 7 7 7
Row 9: 0 7 9 3 7 7 7 7 7 7

WP12 says CL+BHML antisymmetrizations close at so(10) = D_5, dim 45.
"""
import numpy as np

# TSML
TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
TSML = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=int)

# BHML from screenshot
BHML_ROWS = [
    "0123456789",
    "1234567266",
    "2334567366",
    "3444567466",
    "4555567577",
    "5666667677",
    "6777777777",
    "7234567890",
    "8666777978",
    "9666777080",
]
BHML = np.array([[int(c) for c in row] for row in BHML_ROWS], dtype=int)

print("BHML verification:")
print(f"  Shape: {BHML.shape}")
print(f"  Number of HARMONY (7) cells: {(BHML == 7).sum()}")
print(f"  Number of VOID (0) cells: {(BHML == 0).sum()}")

# Build left-regular reps for both
def left_reps(T):
    n = T.shape[0]
    L = []
    for i in range(n):
        Li = np.zeros((n, n), dtype=int)
        for j in range(n):
            k = T[i, j]
            Li[k, j] = 1
        L.append(Li)
    return L

L_TSML = left_reps(TSML)
L_BHML = left_reps(BHML)

A_TSML = [(M - M.T).astype(float) for M in L_TSML]
A_BHML = [(M - M.T).astype(float) for M in L_BHML]

# Per WP11, TSML flow ops are indices [1,2,3,4,6,8]
# For BHML, we need to determine which produce so(10) when combined with TSML.
# Default to: try ALL antisymmetrized BHML rows + TSML flow ops.

flow_indices = [1, 2, 3, 4, 6, 8]
F_TSML = [A_TSML[i] for i in flow_indices]

def lie_closure(generators, max_iters=15):
    shape = generators[0].shape
    bv = [g.flatten() for g in generators if np.linalg.norm(g) > 1e-9]
    if not bv:
        return [], []
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

# Closure of TSML alone (re-confirm)
_, so8_mats = lie_closure(F_TSML)
print(f"\nTSML so(8) closure dim: {len(so8_mats)}")

# Closure of BHML rows alone
_, bhml_lie = lie_closure(A_BHML)
print(f"BHML alone closure dim: {len(bhml_lie)}")

# Closure of TSML + BHML (all rows)
combined = F_TSML + A_BHML
_, so10_mats = lie_closure(combined)
print(f"TSML + BHML combined closure dim: {len(so10_mats)} (expect 45 for so(10))")

# Try smaller subsets to see what's needed
# Just TSML flow + BHML flow:
F_BHML = [A_BHML[i] for i in flow_indices]
_, combined_flow = lie_closure(F_TSML + F_BHML)
print(f"TSML flow + BHML flow only: {len(combined_flow)}")

# Find the invariant subspace for combined so(10)
all_imgs = np.hstack([m for m in so10_mats])
U, S, _ = np.linalg.svd(all_imgs, full_matrices=True)
rank = int(np.sum(S > 1e-9 * S[0]))
print(f"\nCombined image rank (V_? dimension): {rank}")
V_basis = U[:, :rank]
V_perp = U[:, rank:]
print(f"V_perp dimension: {V_perp.shape[1]}")

# Where does VOID go now?
e_0 = np.eye(10)[:, 0]
delta_56 = (np.eye(10)[:, 5] - np.eye(10)[:, 6]) / np.sqrt(2)

print("\n--- Critical: is VOID still annihilated by EVERY combined generator? ---")
all_gens_TSML_only = F_TSML
all_gens_combined = F_TSML + A_BHML

# Test VOID under each generator
print("\nVOID annihilation test:")
print("  By TSML flow:")
for i, g in zip(flow_indices, F_TSML):
    norm = np.linalg.norm(g @ e_0)
    print(f"    A_TSML[{i}] @ e_0: norm = {norm:.6f}")

print("  By BHML rows (anti-sym):")
for i, g in enumerate(A_BHML):
    norm = np.linalg.norm(g @ e_0)
    if norm > 1e-9:
        print(f"    A_BHML[{i}] @ e_0: norm = {norm:.6f} *** NOT ANNIHILATED ***")
    else:
        print(f"    A_BHML[{i}] @ e_0: norm = 0 (annihilated)")

# Test (e_5 - e_6) under each
print("\n(e_5 - e_6) annihilation test:")
print("  By TSML flow (we already know all = 0):")
for i, g in zip(flow_indices, F_TSML):
    norm = np.linalg.norm(g @ delta_56)
    print(f"    A_TSML[{i}] @ delta_56: norm = {norm:.6f}")

print("  By BHML rows (anti-sym):")
any_breaks = False
for i, g in enumerate(A_BHML):
    norm = np.linalg.norm(g @ delta_56)
    if norm > 1e-9:
        print(f"    A_BHML[{i}] @ delta_56: norm = {norm:.6f} *** WAKES UP DELTA_56 ***")
        any_breaks = True
    else:
        print(f"    A_BHML[{i}] @ delta_56: norm = 0")

# Where are the "quiet directions" now?
print("\n--- V_perp basis: which directions are STILL invisible to so(10)? ---")
for i in range(V_perp.shape[1]):
    v = V_perp[:, i]
    print(f"  v_{i}: ", end="")
    for j in range(10):
        if abs(v[j]) > 1e-6:
            print(f"e_{j}({v[j]:+.3f}) ", end="")
    print()

# How much of e_0 sits in V_perp now?
proj_perp_e0 = V_perp @ V_perp.T @ e_0 if V_perp.shape[1] > 0 else np.zeros(10)
proj_perp_delta = V_perp @ V_perp.T @ delta_56 if V_perp.shape[1] > 0 else np.zeros(10)
print(f"\n||proj_Vperp(e_0)|| = {np.linalg.norm(proj_perp_e0):.4f}")
print(f"||proj_Vperp(e_5 - e_6)/√2|| = {np.linalg.norm(proj_perp_delta):.4f}")

# Now build Dirac and project onto so(10)
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

# Lift to 10x10 via V_basis (which now might be 10-dim if so(10) acts on full R^10)
print(f"\n--- Lifting Dirac to so(10) frame (V dim = {rank}) ---")

if rank == 10:
    # Full action on R^10. We need to embed Dirac's 8x8 into 10x10 via choosing
    # an 8-dim subspace. The natural choice would be the original V_8 (where
    # TSML alone was acting). Let's use that.
    V8_basis_TSML = U[:, :8]  # First 8 columns are most likely the V_8
    
    # Actually, for so(10) acting on full R^10, Dirac's so(1,3) should sit
    # somewhere inside as a sub-action on a 4-dim subspace. We'll project.
    pass

# Project each Dirac generator onto so(10) basis
so10_vec_basis = np.array([m.flatten() for m in so10_mats]).T
U_so10, S_so10, _ = np.linalg.svd(so10_vec_basis, full_matrices=False)
so10_orthonorm = U_so10[:, :len(so10_mats)]

# For each Dirac generator, lift to R^10 in some way and project
# Try the same V_8 we had before (from TSML alone)
_, so8_mats_TSML = lie_closure(F_TSML)
all_imgs_T = np.hstack([m for m in so8_mats_TSML])
U_T, S_T, _ = np.linalg.svd(all_imgs_T, full_matrices=True)
V8_T = U_T[:, :8]

print(f"\nProjecting Dirac (lifted via TSML's V_8) onto so(10):")
print(f"so(10) dim: {len(so10_mats)}, V_8 from TSML (10x8)")
total_dirac_in_so10 = np.zeros((10, 10))
for (mu, nu), M_8 in M_real8.items():
    M_10 = V8_T @ M_8 @ V8_T.T  # lift to 10x10 via TSML's V_8
    total_dirac_in_so10 += np.abs(M_10)
    M_vec = M_10.flatten()
    coeffs = so10_orthonorm.T @ M_vec
    proj = so10_orthonorm @ coeffs
    res = np.linalg.norm(M_vec - proj)
    M_norm = np.linalg.norm(M_vec)
    print(f"  M̃^{mu}{nu}: ||proj||={np.linalg.norm(proj):.3f}, residual frac={res/M_norm:.4e}")

# Now: per-index footprint comparison TSML-only vs TSML+BHML
print("\n--- Per-index Dirac footprint in so(10) frame ---")
v_contrib_so10 = (V_basis ** 2).sum(axis=1)
for i in range(10):
    weight = total_dirac_in_so10[i, :].sum() + total_dirac_in_so10[:, i].sum()
    print(f"  index {i}: V contribution = {v_contrib_so10[i]:.4f}, Dirac weight = {weight:.4f}")
