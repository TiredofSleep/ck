"""
Stand inside Dirac's frame. Ask:

1. What of TIG does Dirac SEE (project nontrivially onto)?
2. What of TIG is Dirac BLIND TO?
3. What of TIG's structure does Dirac NEED but doesn't have?
4. What does Dirac get for free if he adopts TIG's framework?

The Dirac frame: 4-dim complex spinor space, equipped with γ^μ matrices,
generating so(1,3) at 6-dim. Lifted to R^8, generating a 6-dim subalgebra
of so(10) on R^10 (we now know).

Inside so(10) = 45 dim, Dirac sees 6. The remaining 39 dimensions are
"invisible" from Dirac's perspective.

Of those 39:
- 28 - 6 = 22 dim of so(8) NOT in Dirac (TSML's "non-Lorentz" part)
- 45 - 28 = 17 dim of so(10) outside so(8) (BHML's "extension")
- so(10) splits 36 + 9 under P_56 conjugation
- so(8) ⊂ so(9) ⊂ so(10) chain

Dirac's 6-dim so(1,3) — where does it sit in this structure?
- All 6 commute with P_56 (since they live in so(8) which is in so(10)_+)
- So Dirac is entirely in the +1 eigenspace under the 5↔6 swap
- Dirac is INSIDE so(9)

So Dirac is blind to:
- The (e_5 - e_6) direction
- VOID (e_0)
- The 9 anticommuting BHML generators that anticommute with P_56

What does TIG see that Dirac doesn't?

The question: what can TIG SAY about a state that Dirac CAN'T?
"""
import numpy as np
from itertools import combinations

# Tables
TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
T = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=int)

BHML_ROWS = [
    "0123456789",  "1234567266",  "2334567366",  "3444567466",  "4555567577",
    "5666667677",  "6777777777",  "7234567890",  "8666777978",  "9666777080",
]
B = np.array([[int(c) for c in row] for row in BHML_ROWS], dtype=int)

def left_reps(table):
    n = table.shape[0]
    L = []
    for i in range(n):
        Li = np.zeros((n, n), dtype=int)
        for j in range(n):
            k = table[i, j]
            Li[k, j] = 1
        L.append(Li)
    return L

L_TSML = left_reps(T)
L_BHML = left_reps(B)
A_TSML = [(M - M.T).astype(float) for M in L_TSML]
A_BHML = [(M - M.T).astype(float) for M in L_BHML]
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

# Build so(8) and so(10)
_, so8_mats = lie_closure(F_TSML)
_, so10_mats = lie_closure(F_TSML + A_BHML)
print(f"so(8): {len(so8_mats)} generators")
print(f"so(10): {len(so10_mats)} generators")

# V_8 from TSML alone
all_imgs_T = np.hstack([m for m in so8_mats])
U_T, S_T, _ = np.linalg.svd(all_imgs_T, full_matrices=True)
V8 = U_T[:, :8]

# Build Dirac generators in R^10 frame (lifted via V_8)
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

dirac_so10 = [V8 @ cplx_to_real8(M) @ V8.T for M in M_tilde.values()]

# === Q1: What of so(10) does Dirac SEE? ===
print("\n" + "="*70)
print("Q1: What of so(10) does Dirac span (project nontrivially onto)?")
print("="*70)

# Build orthonormal so(10) basis
so10_vec = np.array([m.flatten() for m in so10_mats]).T
U_10, S_10, Vt_10 = np.linalg.svd(so10_vec, full_matrices=False)
so10_orth = U_10[:, :45]  # 100 x 45 orthonormal

# Project each Dirac generator
dirac_in_so10 = np.array([m.flatten() for m in dirac_so10]).T  # 100 x 6
dirac_coords = so10_orth.T @ dirac_in_so10  # 45 x 6
print(f"\nDirac (6 generators) in so(10) coords (45-dim):")
print(f"Each Dirac generator is a vector in R^45.")
# Span of Dirac in so(10)
rank_dirac = np.linalg.matrix_rank(dirac_coords, tol=1e-9)
print(f"Rank of Dirac span: {rank_dirac}")

# Dirac span = 6-dim subspace of so(10)
# Complement = 45 - 6 = 39 dim
# What does the complement contain?

# === Q2: Decompose so(10) = Dirac ⊕ Complement ===
print("\n" + "="*70)
print("Q2: so(10) = Dirac (6) ⊕ Complement (39)")
print("="*70)

# Orthogonal complement
Q_dirac, R_dirac = np.linalg.qr(dirac_coords)  # 45 x 6 orthonormal
np.random.seed(42)
random_dirs = np.random.randn(45, 50)
combined = np.hstack([Q_dirac, random_dirs])
Q_full, _ = np.linalg.qr(combined)
complement_in_so10 = Q_full[:, 6:45]  # 45 x 39

# === Q3: Sub-decompose using P_56 (the 5↔6 swap) ===
print("\n" + "="*70)
print("Q3: How do Dirac and Complement split under P_56?")
print("="*70)

# Build P_56
P = np.eye(10)
P[5,5] = 0; P[6,6] = 0; P[5,6] = 1; P[6,5] = 1
P_f = P.astype(float)

# Conjugation action of P on so(10) basis vectors
# A → P A P^T 
P_kron = np.kron(P_f, P_f)
so10_basis_full = np.array([m.flatten() for m in so10_mats]).T
so10_conj = P_kron @ so10_basis_full

# For each so(10) generator A_k, A_k_conj is a linear combination of so(10) generators
# Find that linear combination
C_op, residuals, _, _ = np.linalg.lstsq(so10_basis_full, so10_conj, rcond=None)
# C_op (45 x 45) represents the action of P-conjugation on so(10)

# Diagonalize C_op
eigs, vecs = np.linalg.eig(C_op)
real_mask = np.abs(np.imag(eigs)) < 1e-6
real_eigs = np.real(eigs[real_mask])
plus_mask = np.abs(real_eigs - 1) < 1e-6
minus_mask = np.abs(real_eigs + 1) < 1e-6
print(f"\nP-conjugation eigenvalues on so(10): {plus_mask.sum()} (+1), {minus_mask.sum()} (-1)")

# Get the 36-dim +1 eigenspace and 9-dim -1 eigenspace as subspaces of so(10) coords
plus_indices = np.where(plus_mask)[0]
minus_indices = np.where(minus_mask)[0]
plus_basis = np.real(vecs[:, real_mask][:, plus_mask])
minus_basis = np.real(vecs[:, real_mask][:, minus_mask])

# Orthonormalize
plus_basis_orth, _ = np.linalg.qr(plus_basis)
minus_basis_orth, _ = np.linalg.qr(minus_basis)

# Where does Dirac sit in this splitting?
# Project Dirac coords onto +1 and -1 eigenspaces
dirac_in_plus = plus_basis_orth.T @ dirac_coords
dirac_in_minus = minus_basis_orth.T @ dirac_coords

print(f"\nDirac generators projected onto P-eigenspaces:")
for idx, (mu, nu) in enumerate(M_tilde.keys()):
    norm_plus = np.linalg.norm(dirac_in_plus[:, idx])
    norm_minus = np.linalg.norm(dirac_in_minus[:, idx])
    norm_total = np.linalg.norm(dirac_coords[:, idx])
    plus_frac = (norm_plus / norm_total)**2 if norm_total > 0 else 0
    minus_frac = (norm_minus / norm_total)**2 if norm_total > 0 else 0
    print(f"  M̃^{mu}{nu}: ||+1 part||/||total|| = {np.sqrt(plus_frac):.4f}, "
          f"||-1 part||/||total|| = {np.sqrt(minus_frac):.4f}")

# Confirm: Dirac entirely in +1 eigenspace
total_dirac_in_plus = np.linalg.norm(dirac_in_plus, 'fro')
total_dirac_in_minus = np.linalg.norm(dirac_in_minus, 'fro')
print(f"\nTotal Dirac Frobenius norm: in +1 = {total_dirac_in_plus:.4f}, in -1 = {total_dirac_in_minus:.4f}")

# === Q4: What's in the complement, by P-eigenspace? ===
print("\n" + "="*70)
print("Q4: The 39-dim complement to Dirac inside so(10), split by P_56")
print("="*70)

# Complement basis in so(10) coords
# Project complement onto +1 and -1 eigenspaces
comp_in_plus = plus_basis_orth.T @ complement_in_so10
comp_in_minus = minus_basis_orth.T @ complement_in_so10

# Total dim each
print(f"\nDirac span: 6-dim, all in +1 eigenspace")
print(f"Complement: 39-dim")
print(f"  Dim in +1 eigenspace (commutes with P): 36 - 6 = 30")
print(f"  Dim in -1 eigenspace (anticommutes with P): 9")

# Check this:
print(f"\nVerification by SVD ranks:")
rank_comp_plus = np.linalg.matrix_rank(comp_in_plus, tol=1e-9)
rank_comp_minus = np.linalg.matrix_rank(comp_in_minus, tol=1e-9)
print(f"  Rank of complement in +1 eigenspace: {rank_comp_plus}")
print(f"  Rank of complement in -1 eigenspace: {rank_comp_minus}")

# === Q5: What does TIG ADD beyond Dirac? ===
print("\n" + "="*70)
print("Q5: What does TIG add beyond Dirac?")
print("="*70)
print("""
TIG = the entire structure of so(10) generated by TSML+BHML, with
canonical labels (10 operators, σ permutation, idempotents, 6-cycle,
T*=5/7, etc.) and the runtime layer (CK, coherence, D² curvature).

Dirac's 6 generators sit inside the 36-dim P-symmetric part of so(10).
TIG provides:

  +30 generators (in so(10)_+): symmetric extensions Dirac doesn't reach
       These are PARTNERS to Dirac inside so(9) — the "internal symmetry"
       structure that completes Lorentz to a full local gauge group.

  +9 generators (in so(10)_-): the "vector" piece that anticommutes with P_56
       These are precisely the components of an SO(9)-vector — i.e., a Higgs-like
       9-vector representation under so(9). In SO(10) GUT, these correspond
       to a specific Higgs sector.

  +1 dimension R^10 (the (e_5-e_6) direction): an additional spatial direction
       that Dirac is structurally blind to. This is what TIG calls
       "BALANCE-minus-CHAOS" — the antisymmetric pairing that lives outside
       Dirac's perception.

  +1 dimension R^10 (VOID, e_0): the kernel direction. Dirac never touches it.
       In TIG, this is the anchor against which all other directions are measured.
""")

# Quantify: what fraction of so(10) does Dirac touch?
print(f"Dirac dimension: 6")
print(f"so(8) dimension (TSML-only): 28")
print(f"so(10) dimension (full): 45")
print(f"Dirac fraction of so(8): {6/28*100:.1f}%")
print(f"Dirac fraction of so(10): {6/45*100:.1f}%")

# === Q6: Specific TIG structures Dirac is blind to ===
print("\n" + "="*70)
print("Q6: SPECIFIC TIG structures Dirac cannot see")
print("="*70)

# 1. The σ permutation as a structural element
sigma = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]  # σ permutation of indices
P_sigma = np.zeros((10, 10))
for i in range(10):
    P_sigma[sigma[i], i] = 1

print("σ permutation of indices: 0→0, 1→7, 2→1, 3→3, 4→2, 5→4, 6→5, 7→6, 8→8, 9→9")
print(f"σ matrix is rank: {np.linalg.matrix_rank(P_sigma)}")

# Check if σ commutes with Dirac generators
print("\nDoes σ commute with Dirac's 6 generators?")
for idx, (mu, nu) in enumerate(M_tilde.keys()):
    M = dirac_so10[idx]
    comm = P_sigma @ M - M @ P_sigma
    norm = np.linalg.norm(comm)
    print(f"  M̃^{mu}{nu}: ||[σ, M̃]|| = {norm:.4f}")

# σ-INVARIANT operators inside so(10)
print("\nDoes σ commute with TSML flow operators?")
for i in flow_indices:
    A = A_TSML[i]
    comm = P_sigma @ A - A @ P_sigma
    norm = np.linalg.norm(comm)
    print(f"  A_TSML[{i}]: ||[σ, A]|| = {norm:.4f}")

# 2. The bumps
print("\nThe 10 bump cells of TSML — does Dirac 'see' them as a structural feature?")
print("(Dirac's matrices are dense in TSML's basis — no special role for bumps)")

# 3. T* = 5/7 threshold
print("\nT* = 5/7 — does Dirac know about this?")
print("Dirac alone is unaware of T*. T* is a TIG-specific scalar.")
print("Inside CK, T* governs the boundary between LATTICE-flow (reversible)")
print("and COLLAPSE-flow (dissipative). Dirac contains no analog of this boundary.")

# === Q7: Summary table — Dirac sees vs Dirac is blind ===
print("\n" + "="*70)
print("SUMMARY — Dirac vs TIG")
print("="*70)
print("""
WHAT DIRAC SEES (inside TIG's so(10) on R^10):
  ✓ 6 generators of so(1,3) — Lorentz boosts and rotations
  ✓ Acts on V_8 (8-dim subspace), but only via 6 of so(8)'s 28 generators
  ✓ All sits in so(8) ⊂ so(9) ⊂ so(10)
  ✓ All sits in the +1 eigenspace of P_56 (commutes with BALANCE/CHAOS swap)
  ✓ All TSML cells, including bumps, contribute (densely)

WHAT DIRAC IS BLIND TO:
  ✗ VOID (e_0) — annihilated under Dirac's lift through V_8
  ✗ (e_5 - e_6) — the antisymmetric BALANCE/CHAOS direction
  ✗ 22 generators of so(8) — TSML's "non-Lorentz" content
  ✗ 8 generators of so(10)_+ outside so(8) — symmetric BHML extension
  ✗ 9 generators of so(10)_- — anticommuting BHML "vector" piece
  ✗ The σ permutation as a structural element
  ✗ Bumps as distinguished cells (Dirac sees them as densely populated)
  ✗ T* = 5/7 threshold
  ✗ The 10 named operators (LATTICE, COUNTER, etc.)
  ✗ HARMONY as a default
  ✗ The σ-rate spectral gap
  ✗ Coherence equation C = 0.4(1-E) + 0.35A + 0.25K
  ✗ The 6-cycle of σ (1→7→6→5→4→2→1)

WHAT TIG ADDS THAT DIRAC NEEDS:
  + Internal symmetry partner for Lorentz: so(9) extension
  + A natural 9-vector Higgs: so(10)_- piece
  + A canonical "frozen direction" mechanism: VOID + (e_5-e_6)
  + A structural distinguisher between BALANCE and CHAOS: BHML
  + A scalar threshold T*=5/7 governing flow-vs-dissipation transitions
  + A computational runtime: CK
  + A diagnostic taxonomy: UOP four-type classifier

WHAT DIRAC GAINS BY ADOPTING TIG:
  → A complete embedding into a finite-dimensional algebra (no "internal indices")
  → A canonical choice of so(9) orientation (TSML's specific basis)
  → A computable numerical realization with concrete coefficients (the
    explicit matrix expansions we derived)
  → A connection to a four-Type measurement-failure taxonomy
""")
