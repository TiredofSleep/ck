"""
Compute [P_56, σ^3] acting on so(10) by conjugation.

If Brayden's intuition is right, this commutator should:
1. Have nontrivial structure (P_56 and σ^3 don't commute - already known)
2. Land in a specific isotypic component that has interpretive weight

The D_4 = <P_56, σ^3> action on so(10) has decomposition:
  - 16-dim trivial-isotypic (su(4) ⊕ u(1)) — both fixed
  - 1-dim sign(P_56) × trivial(σ^3)
  - 12-dim trivial(P_56) × sign(σ^3)
  - 16-dim 2-d irrep (8 copies)

The COMMUTATOR [P_56, σ^3] X = P_56 σ^3 X σ^-3 P_56^-1 - σ^3 P_56 X P_56^-1 σ^-3
acts as a linear map on so(10). We want its image and kernel.

Specifically, the question: does the commutator preserve or break the
σ-fixed lattice {0, 3, 8, 9} substructure?

If 5↔6 carries one kind of asymmetry and 2↔3 carries another, we'd expect
the commutator to "see" the interaction between them — i.e., to act
nontrivially specifically on subspaces that mix the two axes.
"""

import numpy as np

# so(10) basis
def E(a, b, n=10):
    M = np.zeros((n, n))
    M[a, b] = 1
    M[b, a] = -1
    return M

so10_basis = []
so10_indices = []  # (a, b) pairs with a < b
for a in range(10):
    for b in range(a+1, 10):
        so10_basis.append(E(a, b))
        so10_indices.append((a, b))

# Permutations
P56 = np.eye(10)
P56[[5, 6]] = P56[[6, 5]]

sigma3_indices_list = list(range(10))
sigma3_indices_list[1], sigma3_indices_list[5] = 5, 1
sigma3_indices_list[7], sigma3_indices_list[4] = 4, 7
sigma3_indices_list[6], sigma3_indices_list[2] = 2, 6
sigma3 = np.zeros((10, 10))
for i, j in enumerate(sigma3_indices_list):
    sigma3[i, j] = 1

# Action on so(10): X -> P X P^T (= P X P^-1 since P is orthogonal)
def conj_P56(X):
    return P56 @ X @ P56.T

def conj_sigma3(X):
    return sigma3 @ X @ sigma3.T

# COMMUTATOR action: C(X) = (P56 ∘ σ3 - σ3 ∘ P56)(X)
# = P56(σ3(X)) - σ3(P56(X))
# These are linear maps on so(10)
def commutator_action(X):
    return conj_P56(conj_sigma3(X)) - conj_sigma3(conj_P56(X))

# Build the commutator as a 45×45 matrix on so(10) basis
basis_vecs = np.array([B.flatten() for B in so10_basis])

C_matrix = np.zeros((45, 45))
for i, B in enumerate(so10_basis):
    img = commutator_action(B)
    coeffs = np.linalg.lstsq(basis_vecs.T, img.flatten(), rcond=None)[0]
    C_matrix[:, i] = coeffs

print("Commutator [P_56, σ^3] acting on so(10):")
print(f"  Frobenius norm: {np.linalg.norm(C_matrix):.4f}")
print(f"  Rank: {np.linalg.matrix_rank(C_matrix, tol=1e-9)}")
print(f"  Kernel dim: {45 - np.linalg.matrix_rank(C_matrix, tol=1e-9)}")
print()

# What's in the kernel? These are X such that P_56 σ_3 X = σ_3 P_56 X
# i.e., X commutes with the commutator = elements that "see" the swap structure
# the same way regardless of order.

# Find kernel basis
U, S, Vt = np.linalg.svd(C_matrix)
tol = 1e-9
ker_dim = np.sum(S < tol)
print(f"Kernel dimension (via SVD): {ker_dim}")

# What's in the image?
img_dim = np.sum(S >= tol)
print(f"Image dimension: {img_dim}")
print()

# Now decompose by which (a,b) generators are in the image vs kernel
# This tells us which so(10) directions are "felt" by the asymmetry
print("Generators E_{a,b} mapped under commutator (norm of image):")
for i, (a, b) in enumerate(so10_indices):
    img_vec = C_matrix[:, i]
    norm = np.linalg.norm(img_vec)
    if norm > 1e-9:
        # Find dominant components in image
        sorted_idx = np.argsort(-np.abs(img_vec))[:3]
        components = ", ".join(f"{img_vec[idx]:+.2f}·E_{{{so10_indices[idx][0]},{so10_indices[idx][1]}}}"
                              for idx in sorted_idx if abs(img_vec[idx]) > 1e-9)
        print(f"  E_{{{a},{b}}}: ||img|| = {norm:.3f}  →  {components}")
