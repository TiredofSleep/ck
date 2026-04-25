"""
The last step: 5↔6 swap as a structural symmetry.

If 5 and 6 are completely interchangeable, then the permutation
matrix P_56 (swap indices 5 and 6) should be a SYMMETRY of:
  - TSML's table T: P_56 T P_56^T = T  (or maybe T composed with swap)
  - BHML's table B: P_56 B P_56^T = B
  - The whole so(10) action: every generator commutes with P_56

If P_56 commutes with the entire so(10), then P_56 is in the CENTRALIZER
of so(10) inside O(10). The centralizer of so(10) inside O(10) is just
{±I} for the irrep — UNLESS the action splits.

If P_56 is a non-trivial central element, it splits the action into
±1 eigenspaces. That's a CHIRAL split.

Let me actually test this.
"""
import numpy as np

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

# Build P_56: swap indices 5 and 6
P = np.eye(10)
P[5, 5] = 0
P[6, 6] = 0
P[5, 6] = 1
P[6, 5] = 1
P = P.astype(int)

print("="*70)
print("Test 1: Is the TABLE itself invariant under 5↔6 swap?")
print("="*70)

# Two versions of "invariance":
# (a) Indexing only: T[π(i), π(j)] = T[i, j]  — relabel rows AND columns
# (b) Indexing + value: T[π(i), π(j)] = π(T[i, j])  — also swap values 5 and 6

# Version (a): pure index swap
T_swapped_idx = P @ T @ P.T  # swap rows AND columns
print("\nVersion (a): T_swapped[π(i), π(j)] = T[i, j]")
print("Does swapping rows 5↔6 and cols 5↔6 give back T?")
print(f"  T == P T P^T: {np.array_equal(T, T_swapped_idx)}")

if not np.array_equal(T, T_swapped_idx):
    diff = T - T_swapped_idx
    print(f"  Differences at (i,j): ", end="")
    for i in range(10):
        for j in range(10):
            if diff[i, j] != 0:
                print(f"({i},{j})", end=" ")
    print()

# Version (b): swap rows, cols, AND VALUES 5 and 6
def swap_values_56(M):
    M2 = M.copy()
    M2 = np.where(M == 5, 99, M2)  # temp marker
    M2 = np.where(M2 == 6, 5, M2)
    M2 = np.where(M2 == 99, 6, M2)
    return M2

T_swapped_full = swap_values_56(P @ T @ P.T)
print("\nVersion (b): T_swapped includes value-swap 5↔6 in entries")
print(f"  T == swap_values_56(P T P^T): {np.array_equal(T, T_swapped_full)}")

print("\n--- BHML: Test the same ---")
B_swapped_idx = P @ B @ P.T
print(f"\nBHML: B == P B P^T: {np.array_equal(B, B_swapped_idx)}")
if not np.array_equal(B, B_swapped_idx):
    diff = B - B_swapped_idx
    diff_count = np.sum(diff != 0)
    print(f"  Cells that differ: {diff_count}")
    if diff_count < 30:
        print(f"  Differences:")
        for i in range(10):
            for j in range(10):
                if diff[i, j] != 0:
                    print(f"    ({i},{j}): B[{i},{j}]={B[i,j]} vs (P B P^T)[{i},{j}]={B_swapped_idx[i,j]}")

B_swapped_full = swap_values_56(P @ B @ P.T)
print(f"\nBHML with value-swap: B == swap_values_56(P B P^T): {np.array_equal(B, B_swapped_full)}")
if not np.array_equal(B, B_swapped_full):
    diff = B - B_swapped_full
    diff_count = np.sum(diff != 0)
    print(f"  Cells that differ: {diff_count}")

print("\n" + "="*70)
print("Test 2: Does P_56 commute with the so(8) generators?")
print("="*70)

# Build flow operators of TSML
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
A_TSML = [(M - M.T).astype(float) for M in L_TSML]
flow_indices = [1, 2, 3, 4, 6, 8]
F_TSML = [A_TSML[i] for i in flow_indices]

P_f = P.astype(float)

print("\nFor each TSML flow operator, check [P_56, A_i] = 0:")
all_commute_TSML = True
for i, A in zip(flow_indices, F_TSML):
    comm = P_f @ A - A @ P_f
    norm = np.linalg.norm(comm)
    if norm > 1e-9:
        all_commute_TSML = False
        print(f"  A_TSML[{i}]: ||[P, A]|| = {norm:.4f} -- DOES NOT COMMUTE")
    else:
        print(f"  A_TSML[{i}]: ||[P, A]|| = 0 (commutes)")

print(f"\nP_56 commutes with all TSML flow ops: {all_commute_TSML}")

# Build flow operators of BHML
L_BHML = left_reps(B)
A_BHML = [(M - M.T).astype(float) for M in L_BHML]

print("\nFor each BHML row antisymmetrized, check [P_56, A_i] = 0:")
all_commute_BHML = True
for i, A in enumerate(A_BHML):
    comm = P_f @ A - A @ P_f
    norm = np.linalg.norm(comm)
    if norm > 1e-9:
        all_commute_BHML = False
        print(f"  A_BHML[{i}]: ||[P, A]|| = {norm:.4f}")
    else:
        print(f"  A_BHML[{i}]: ||[P, A]|| = 0 (commutes)")

print(f"\nP_56 commutes with all BHML antisymmetrized rows: {all_commute_BHML}")

print("\n" + "="*70)
print("Test 3: Spectrum of P_56 — does it split R^10 into ±1 eigenspaces?")
print("="*70)

eigvals, eigvecs = np.linalg.eigh(P_f)
print(f"\nEigenvalues of P_56: {eigvals}")
print(f"  +1 eigenvalues: {(eigvals > 0.5).sum()}")
print(f"  -1 eigenvalues: {(eigvals < -0.5).sum()}")

# +1 eigenspace: 9-dim (everything except (e_5 - e_6)/√2)
# -1 eigenspace: 1-dim (just (e_5 - e_6)/√2)

print("\nEigenvectors:")
for i in range(10):
    v = eigvecs[:, i]
    # Show non-zero components
    print(f"  λ = {eigvals[i]:+.0f}:  ", end="")
    for j in range(10):
        if abs(v[j]) > 1e-6:
            print(f"e_{j}({v[j]:+.3f}) ", end="")
    print()

print("\n" + "="*70)
print("Test 4: P_56 acts on so(10) by conjugation — what's the structure?")
print("="*70)

# For each so(10) generator, compute P A P^T - A and see how many flip sign
# vs stay the same.

# First build full so(10) basis from TSML flow + BHML rows
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

_, so10_mats = lie_closure(F_TSML + A_BHML)
print(f"\nso(10) closure dim: {len(so10_mats)}")

# For each so(10) generator A, compute P A P^T
# Check: how many satisfy P A P^T = +A (commute), how many = -A (anticommute)?

plus_count = 0
minus_count = 0
mixed_count = 0
for A in so10_mats:
    A_conj = P_f @ A @ P_f.T
    # Decompose: A_conj = c+ * A + c- * (something else)
    # Easiest: check if A_conj == A or A_conj == -A
    if np.allclose(A_conj, A):
        plus_count += 1
    elif np.allclose(A_conj, -A):
        minus_count += 1
    else:
        mixed_count += 1

print(f"\nso(10) generators classified by P_56 conjugation action:")
print(f"  PAP^T = +A (commute): {plus_count}")
print(f"  PAP^T = -A (anticommute): {minus_count}")
print(f"  PAP^T mixed: {mixed_count}")

# Total = 45 = dim so(10). Plus + Minus = 45 if P acts by ±1 on each generator.
# In fact: P_56 is order 2 (P^2 = I), so by spectral theorem of conjugation,
# the so(10) Lie algebra splits into +1 and -1 eigenspaces under conjugation by P.

# Compute eigenvalues of "conjugation by P" as a linear map on so(10)
print("\nFully analyzing the conjugation action of P on so(10):")
# Build the linear map: A → P A P^T - A in the 45-dim so(10) basis
so10_basis = np.array([m.flatten() for m in so10_mats]).T  # 100 x 45
# Action: A → P A P^T = (P ⊗ P) vec(A) where vec is row-major... 
# Actually: vec(P A P^T) = (P^T^T ⊗ P) vec(A) = (P ⊗ P) vec(A)  
# (using row-major flatten and the identity vec(BAC) = (C^T ⊗ B) vec(A))
# But since P^T = P (P is symmetric), it's (P ⊗ P) vec(A).

P_kron = np.kron(P_f, P_f)
# Apply to so(10) basis
so10_basis_conj = P_kron @ so10_basis  # 100 x 45

# Express the conjugated basis in original basis
# so10_basis is 100 x 45 with rank 45
# Find coefficients C such that so10_basis_conj = so10_basis @ C
C, residuals, _, _ = np.linalg.lstsq(so10_basis, so10_basis_conj, rcond=None)
print(f"\nConjugation matrix C (45x45) shape: {C.shape}")
# Eigenvalues of C
eigs_C = np.linalg.eigvals(C)
real_eigs = np.real(eigs_C[np.abs(np.imag(eigs_C)) < 1e-9])
print(f"\nEigenvalues of conjugation map (real ones):")
print(f"  +1 eigenvalues (commute with P): {np.sum(np.abs(real_eigs - 1) < 1e-6)}")
print(f"  -1 eigenvalues (anticommute):    {np.sum(np.abs(real_eigs + 1) < 1e-6)}")
print(f"  total:                            {len(real_eigs)}")

print("\n" + "="*70)
print("Test 5: How does this compare to so(8) ⊂ so(10)?")
print("="*70)

# so(8) generated by TSML alone has dim 28
# so(10) has dim 45
# 45 - 28 = 17 generators "added" by BHML
# Question: do these 17 split between +1 and -1 differently than the so(8) part?

_, so8_mats = lie_closure(F_TSML)
print(f"\nso(8) (TSML alone) generators: {len(so8_mats)}")

# Classify so(8) generators
so8_plus = 0
so8_minus = 0
so8_mixed = 0
for A in so8_mats:
    A_conj = P_f @ A @ P_f.T
    if np.allclose(A_conj, A):
        so8_plus += 1
    elif np.allclose(A_conj, -A):
        so8_minus += 1
    else:
        so8_mixed += 1

print(f"  so(8) generators: +1={so8_plus}, -1={so8_minus}, mixed={so8_mixed}")
print(f"  so(10) generators: +1={plus_count}, -1={minus_count}, mixed={mixed_count}")
