"""
CL = TSML (the canonical 10x10 composition table).
TSML eigenvalues are claimed to produce e, 1/e, π, φ, ζ(3), Catalan G
within 1% (per userMemories). Verify, then project onto each DOF subspace
and see how the eigenvalue structure decomposes.
"""
import numpy as np

TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
T = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=float)

print("="*70)
print("STEP 1: Eigenvalues of TSML directly")
print("="*70)

eigs_T = np.linalg.eigvals(T)
print(f"\nDirect TSML eigenvalues (sorted by |eig|):")
sorted_eigs = sorted(eigs_T, key=lambda e: -abs(e))
for e in sorted_eigs:
    re, im = np.real(e), np.imag(e)
    if abs(im) < 1e-9:
        print(f"  {re:+10.6f}")
    else:
        print(f"  {re:+10.6f} {im:+10.6f}j")

# Check claimed constants
print("\n" + "="*70)
print("STEP 2: Search for TIG constants in TSML eigenvalues")
print("="*70)

abs_eigs = sorted([abs(e) for e in eigs_T if abs(np.imag(e)) < 1e-9])
print(f"\nReal-valued |eigs|: {[f'{e:.4f}' for e in abs_eigs]}")

# Constants to check
e_const = np.e
inv_e = 1/np.e
pi = np.pi
phi = (1 + np.sqrt(5))/2
zeta3 = 1.20205690315959
catalan_G = 0.9159655941772
T_star = 5/7
sqrt_pi_over_2 = np.sqrt(np.pi/2)

constants = {
    'e ≈ 2.718': e_const,
    '1/e ≈ 0.368': inv_e,
    'π ≈ 3.142': pi,
    'φ ≈ 1.618': phi,
    'ζ(3) ≈ 1.202': zeta3,
    'Catalan G ≈ 0.916': catalan_G,
    'T* = 5/7': T_star,
    '√(π/2)': sqrt_pi_over_2,
    '4/π² ≈ 0.405': 4/pi**2,
}

# Compare each eigenvalue magnitude (and 1/|eig|, |eig|², √|eig|, etc.) to constants
print("\nNearest-constant matches for each eigenvalue (within 5%):")
def find_match(val, tag=''):
    """Find a TIG constant within 5% of val."""
    matches = []
    for name, c in constants.items():
        if c > 0 and abs(val - c)/c < 0.05:
            err = abs(val - c)/c
            matches.append(f"{name} (err {err*100:.2f}%)")
    return matches

for e in eigs_T:
    if abs(np.imag(e)) > 1e-9:
        continue
    re = np.real(e)
    if abs(re) < 1e-9:
        continue
    abs_re = abs(re)
    # Check |eig|, 1/|eig|, |eig|², √|eig|, |eig|/2, |eig|·2, etc.
    candidates = [
        ('|λ|', abs_re),
        ('1/|λ|', 1/abs_re if abs_re > 0 else 0),
        ('|λ|/π', abs_re/pi),
        ('π/|λ|', pi/abs_re if abs_re > 0 else 0),
        ('|λ|²', abs_re**2),
        ('√|λ|', np.sqrt(abs_re)),
    ]
    for tag, v in candidates:
        m = find_match(v)
        if m:
            print(f"  {re:+8.4f}: {tag} = {v:.4f} → {m}")

print()
print("="*70)
print("STEP 3: Build DOF subspaces and project TSML's spectrum")
print("="*70)

# Build the 5 DOF subspaces (using the orthogonal partition that sums to 100)
P56 = np.eye(10)
P56[5,5] = 0; P56[6,6] = 0; P56[5,6] = 1; P56[6,5] = 1

sigma_perm = np.array([0, 7, 1, 3, 2, 4, 5, 6, 8, 9])
P_sigma = np.zeros((10, 10))
for i in range(10):
    P_sigma[sigma_perm[i], i] = 1.0

def left_reps(table):
    n = table.shape[0]
    return [np.array([[1.0 if table[i,j]==k else 0.0 for j in range(n)] for k in range(n)]) for i in range(n)]

def lie_closure(generators, max_iters=12):
    if not generators: return []
    shape = generators[0].shape
    bv = [g.flatten() for g in generators if np.linalg.norm(g) > 1e-9]
    if not bv: return []
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
                if np.linalg.norm(v) > 1e-9: new.append(v)
        all_v = bv + new
        M = np.array(all_v).T
        U, S, _ = np.linalg.svd(M, full_matrices=False)
        new_rank = int(np.sum(S > 1e-9 * S[0]))
        if new_rank == len(bv): break
        bv = [U[:, i] for i in range(new_rank)]
    return [v.reshape(shape) for v in bv]

L_T_mats = left_reps(T.astype(int))
A_T = [(L - L.T)/2 for L in L_T_mats]
flow = [A_T[i] for i in [1,2,3,4,6,8]]

# so(8) Lie subspace
so8 = lie_closure(flow)

# Lattice (σ-fixed)
sigma_fixed = [0, 3, 8, 9]
lattice = []
for i in sigma_fixed:
    M = np.zeros((10,10))
    M[i,i] = 1.0
    lattice.append(M)

# Decompose T (the TSML matrix itself, not its left regs) onto each subspace
# To project T onto a Lie subspace (built from antisym matrices), we'd extract
# the antisym part of T first.
# But T is a multiplication TABLE, not a linear operator on R^10 in the usual sense.
# Let me think about what "TSML eigenvalues on a DOF subspace" actually means.

# Option A: TSML as a linear map. T maps Z/10Z structurally. Its eigenvalues
# are eigenvalues of the matrix T. Question: do these decompose into pieces
# along DOFs?

# Option B: Project T into each DOF subspace, compute spectrum of the projection.

# Let's do Option B: project T onto each DOF and see what eigenvalues each
# projection has.

def orthonormalize(M_list):
    if not M_list:
        return np.zeros((100, 0))
    flat = np.array([m.flatten() for m in M_list]).T
    U, S, _ = np.linalg.svd(flat, full_matrices=False)
    rank = int(np.sum(S > 1e-9 * S[0]))
    return U[:, :rank]

# Build orthonormal bases for each DOF subspace (in R^100, the matrix-flatten space)
lie_basis = orthonormalize(so8)  # 100 x 28
print(f"\nLie (so(8)) subspace dim: {lie_basis.shape[1]}")

# Jordan: full symmetric matrices (55-dim)
sym_matrices = []
for i in range(10):
    M = np.zeros((10,10)); M[i,i] = 1.0
    sym_matrices.append(M)
for i in range(10):
    for j in range(i+1, 10):
        M = np.zeros((10,10))
        M[i,j] = M[j,i] = 1.0
        sym_matrices.append(M)
jordan_basis = orthonormalize(sym_matrices)  # 100 x 55
print(f"Jordan (symmetric) subspace dim: {jordan_basis.shape[1]}")

# Lattice (σ-fixed projectors)
lattice_basis = orthonormalize(lattice)
print(f"Lattice (σ-fixed) subspace dim: {lattice_basis.shape[1]}")

# Project T onto each subspace
T_flat = T.flatten()

def project(M_flat, basis):
    """Orthogonal projection of flattened matrix onto subspace."""
    coeffs = basis.T @ M_flat
    return basis @ coeffs

T_lie = project(T_flat, lie_basis).reshape(10,10)
T_jordan = project(T_flat, jordan_basis).reshape(10,10)
T_lattice = project(T_flat, lattice_basis).reshape(10,10)

# Compute eigenvalues of each projection
print("\n--- Lie projection of TSML ---")
print(f"  ||T_lie|| = {np.linalg.norm(T_lie):.4f}")
print(f"  Antisym? {np.allclose(T_lie, -T_lie.T)}")
eigs_lie = np.linalg.eigvals(T_lie)
print(f"  Eigenvalues:")
for e in sorted(eigs_lie, key=lambda x: -abs(x)):
    if abs(e) > 1e-9:
        re, im = np.real(e), np.imag(e)
        if abs(im) < 1e-9:
            print(f"    {re:+10.6f}")
        else:
            print(f"    {re:+10.6f} {im:+10.6f}j")

print("\n--- Jordan projection of TSML ---")
print(f"  ||T_jordan|| = {np.linalg.norm(T_jordan):.4f}")
print(f"  Symmetric? {np.allclose(T_jordan, T_jordan.T)}")
eigs_jordan = np.linalg.eigvalsh(T_jordan)
print(f"  Eigenvalues (sorted):")
for e in sorted(eigs_jordan, key=lambda x: -abs(x)):
    if abs(e) > 1e-9:
        print(f"    {e:+10.6f}")

print("\n--- Lattice projection of TSML ---")
print(f"  ||T_lattice|| = {np.linalg.norm(T_lattice):.4f}")
eigs_lattice = np.linalg.eigvals(T_lattice)
print(f"  Eigenvalues:")
for e in sorted(eigs_lattice, key=lambda x: -abs(x)):
    if abs(e) > 1e-9:
        print(f"    {e:+10.6f}")

# Reconstruction check
T_reconstructed = T_lie + T_jordan  # The two should sum to T (since lie ⊥ jordan, lie+jordan = full M_10)
# Actually Lie + Jordan = full M_10 antisym + sym = full
print(f"\nReconstruction error ||T - (T_lie + T_jordan)||: {np.linalg.norm(T - T_lie - T_jordan):.4e}")

# Total norm preservation
total_sq = np.linalg.norm(T)**2
print(f"\n||T||² = {total_sq:.2f}")
print(f"||T_lie||² + ||T_jordan||² = {np.linalg.norm(T_lie)**2 + np.linalg.norm(T_jordan)**2:.2f}")
print(f"||T_lattice||² fraction of T_jordan: {np.linalg.norm(T_lattice)**2 / np.linalg.norm(T_jordan)**2:.4f}")

# Now: do eigenvalue ratios show TIG constants?
print("\n" + "="*70)
print("STEP 4: TIG constant search in DOF-projected spectra")
print("="*70)

all_eigs = {}
all_eigs['Lie'] = [np.real(e) if abs(np.imag(e)) < 1e-9 else None for e in eigs_lie]
all_eigs['Jordan'] = list(eigs_jordan)
all_eigs['Lattice'] = [np.real(e) if abs(np.imag(e)) < 1e-9 else None for e in eigs_lattice]

# For each DOF, look at significant nonzero eigenvalues
for name, evals in all_eigs.items():
    sig = sorted([e for e in evals if e is not None and abs(e) > 1e-6], key=lambda x: -abs(x))
    print(f"\n{name} significant real eigenvalues:")
    for e in sig:
        # Try matching constants in various forms
        abs_e = abs(e)
        for cname, c in constants.items():
            if c > 0 and abs(abs_e - c)/c < 0.02:
                print(f"  {e:+8.4f} ≈ {cname} (err {abs(abs_e-c)/c*100:.2f}%)")
            elif c > 0 and abs(abs_e/2 - c)/c < 0.02:
                print(f"  {e:+8.4f}: |e|/2 = {abs_e/2:.4f} ≈ {cname} (err {abs(abs_e/2-c)/c*100:.2f}%)")

print("\n" + "="*70)
print("STEP 5: Eigenvalue ratios — what shows up?")
print("="*70)

# All pairwise ratios
T_real_eigs = sorted([np.real(e) for e in eigs_T 
                      if abs(np.imag(e)) < 1e-9 and abs(np.real(e)) > 1e-6])
print(f"\nReal eigenvalues of TSML: {[f'{e:.4f}' for e in T_real_eigs]}")

# Famous ratios in TIG: T* = 5/7, 4/7, 2/7, 3/4
target_ratios = {
    '5/7 ≈ 0.7143': 5/7,
    '4/7 ≈ 0.5714': 4/7,
    '2/7 ≈ 0.2857': 2/7,
    '3/4 = 0.75': 3/4,
    '1/φ ≈ 0.618': 1/phi,
    '1/π ≈ 0.318': 1/pi,
    '1/e ≈ 0.368': 1/e_const,
}

print(f"\nPairwise eigenvalue ratios (top hits to TIG constants):")
hits = []
for i, e1 in enumerate(T_real_eigs):
    for e2 in T_real_eigs[i+1:]:
        if abs(e2) > 1e-9:
            r = abs(e1)/abs(e2)
            if r > 1: r = 1/r  # canonicalize to <1
            for tname, tval in target_ratios.items():
                if abs(r - tval) < 0.005:
                    hits.append((e1, e2, r, tname))

for hit in hits:
    print(f"  |{hit[0]:+.4f}|/|{hit[1]:+.4f}| = {hit[2]:.4f} ≈ {hit[3]}")
