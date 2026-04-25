"""
TEST 3: Is there ANY TSML-derived structural property that's meaningful 
for actual neural network weights?

The wobble (prime 11 in c_2, c_8) doesn't distinguish trained from random.

But there are OTHER TSML properties we could test:
  (a) Concentration of antisymmetric content in σ_outer-fixed subspace
  (b) Coherence with the 9-vector Higgs direction
  (c) Lie/Jordan ratio (stability of Hermitian/anti-Hermitian decomposition)
  (d) Distance to the 16-dim D_4-invariant subalgebra
  
Each is mathematically well-defined. Let's see which (if any) actually
distinguishes ML-style matrices from random.

Specifically: take a real small trained model (we'll use a simple
autoencoder trained on MNIST-style data) and project its weight matrices
onto these subspaces. Compare to random baseline.
"""
import numpy as np

np.random.seed(42)

TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
T = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=float)

# ========== Setup: build the structural reference subspaces ==========

# σ_outer-fixed indices (excluding 5, 6 which P_56 swaps): {0,1,2,3,4,7,8,9}
sigma_outer_fixed = [0, 1, 2, 3, 4, 7, 8, 9]

# D_4-invariant 16-dim subspace (built earlier from intersection)
P56 = np.eye(10)
P56[5,5] = 0; P56[6,6] = 0; P56[5,6] = 1; P56[6,5] = 1

sigma_perm = np.array([0, 7, 1, 3, 2, 4, 5, 6, 8, 9])
P_sigma = np.zeros((10, 10))
for i in range(10): P_sigma[sigma_perm[i], i] = 1.0
sigma3 = np.linalg.matrix_power(P_sigma, 3)

group_mats = [np.eye(10)]
seen = {tuple(np.eye(10).flatten())}
queue = [np.eye(10)]
while queue:
    g = queue.pop()
    for s in [P56, sigma3]:
        h = g @ s
        key = tuple(np.round(h.flatten(), 4))
        if key not in seen:
            seen.add(key)
            group_mats.append(h)
            queue.append(h)

# Build 16-dim D_4-invariant Lie subalgebra
basis_so10 = []
for i in range(10):
    for j in range(i+1, 10):
        E = np.zeros((10, 10))
        E[i,j] = 1; E[j,i] = -1
        basis_so10.append(E)

invariants = []
for E in basis_so10:
    avg = sum(g @ E @ g.T for g in group_mats) / len(group_mats)
    if np.linalg.norm(avg) > 1e-9:
        invariants.append(avg)

flat = np.array([P.flatten() for P in invariants]).T
U_inv, S_inv, _ = np.linalg.svd(flat, full_matrices=False)
inv_dim = int(np.sum(S_inv > 1e-9 * S_inv[0]))
inv_basis = U_inv[:, :inv_dim]  # 100 x 16

# ========== Define the structural metrics ==========

def antisym_in_d4_invariant_fraction(W):
    """How much of W's antisymmetric content lives in the 16-dim D_4-invariant?"""
    A = (W - W.T) / 2
    A_flat = A.flatten()
    proj = inv_basis @ (inv_basis.T @ A_flat)
    A_norm_sq = np.linalg.norm(A_flat)**2
    proj_norm_sq = np.linalg.norm(proj)**2
    if A_norm_sq < 1e-12:
        return 0.0
    return proj_norm_sq / A_norm_sq

def lie_jordan_ratio(W):
    """Antisymmetric energy / Symmetric energy."""
    A = (W - W.T) / 2
    S = (W + W.T) / 2
    A_norm = np.linalg.norm(A)
    S_norm = np.linalg.norm(S)
    if S_norm < 1e-12:
        return float('inf')
    return A_norm / S_norm

def p56_invariant_fraction(W):
    """Fraction of W invariant under P_56 conjugation."""
    W_conj = P56 @ W @ P56.T
    W_sym_p56 = (W + W_conj) / 2
    W_anti_p56 = (W - W_conj) / 2
    sym_norm = np.linalg.norm(W_sym_p56)
    total = np.linalg.norm(W)
    if total < 1e-12:
        return 0.0
    return sym_norm**2 / total**2

# Compute these for TSML
print("="*70)
print("STRUCTURAL METRICS FOR REFERENCE")
print("="*70)
print()
print(f"TSML metrics:")
print(f"  antisym in D_4-inv fraction:  {antisym_in_d4_invariant_fraction(T):.4f}")
print(f"  Lie/Jordan ratio:             {lie_jordan_ratio(T):.4f}")
print(f"  P_56-invariant fraction:      {p56_invariant_fraction(T):.4f}")

BHML_ROWS = [
    "0123456789",  "1234567266",  "2334567366",  "3444567466",  "4555567577",
    "5666667677",  "6777777777",  "7234567890",  "8666777978",  "9666777080",
]
B = np.array([[int(c) for c in row] for row in BHML_ROWS], dtype=float)
print(f"\nBHML metrics:")
print(f"  antisym in D_4-inv fraction:  {antisym_in_d4_invariant_fraction(B):.4f}")
print(f"  Lie/Jordan ratio:             {lie_jordan_ratio(B):.4f}")
print(f"  P_56-invariant fraction:      {p56_invariant_fraction(B):.4f}")

# Now: random matrices baseline
print()
print("="*70)
print("BASELINE: random matrices")
print("="*70)

N = 1000
metrics_random_int = {'A_in_inv': [], 'lj': [], 'p56_inv': []}
for _ in range(N):
    W = np.random.randint(0, 10, size=(10, 10)).astype(float)
    metrics_random_int['A_in_inv'].append(antisym_in_d4_invariant_fraction(W))
    metrics_random_int['lj'].append(lie_jordan_ratio(W))
    metrics_random_int['p56_inv'].append(p56_invariant_fraction(W))

metrics_random_gauss = {'A_in_inv': [], 'lj': [], 'p56_inv': []}
for _ in range(N):
    W = np.random.randn(10, 10)
    metrics_random_gauss['A_in_inv'].append(antisym_in_d4_invariant_fraction(W))
    metrics_random_gauss['lj'].append(lie_jordan_ratio(W))
    metrics_random_gauss['p56_inv'].append(p56_invariant_fraction(W))

print(f"\nRandom integer matrices (N={N}):")
print(f"  antisym in D_4-inv: mean {np.mean(metrics_random_int['A_in_inv']):.4f} ± {np.std(metrics_random_int['A_in_inv']):.4f}")
print(f"  Lie/Jordan ratio:   mean {np.mean(metrics_random_int['lj']):.4f} ± {np.std(metrics_random_int['lj']):.4f}")
print(f"  P_56-invariant:     mean {np.mean(metrics_random_int['p56_inv']):.4f} ± {np.std(metrics_random_int['p56_inv']):.4f}")

print(f"\nRandom Gaussian matrices (N={N}):")
print(f"  antisym in D_4-inv: mean {np.mean(metrics_random_gauss['A_in_inv']):.4f} ± {np.std(metrics_random_gauss['A_in_inv']):.4f}")
print(f"  Lie/Jordan ratio:   mean {np.mean(metrics_random_gauss['lj']):.4f} ± {np.std(metrics_random_gauss['lj']):.4f}")
print(f"  P_56-invariant:     mean {np.mean(metrics_random_gauss['p56_inv']):.4f} ± {np.std(metrics_random_gauss['p56_inv']):.4f}")

# Train a tiny autoencoder to get realistic weight matrices
print()
print("="*70)
print("ACTUAL TRAINED 10×10 MATRICES (autoencoder bottleneck weights)")
print("="*70)

# Simple autoencoder: 10 → 5 → 10, train on random low-dim data
# This produces 10x5 and 5x10 matrices; we'll combine to 10x10

def train_simple_autoencoder(n_iter=2000, lr=0.01, seed=0):
    np.random.seed(seed)
    # Simulated low-dim data
    D = 10
    h = 5
    # Generate data on a 3-dim manifold
    n_samples = 200
    z = np.random.randn(n_samples, 3)
    M = np.random.randn(3, D)  # embedding matrix
    X = z @ M + 0.1 * np.random.randn(n_samples, D)
    
    W1 = np.random.randn(D, h) * 0.3
    W2 = np.random.randn(h, D) * 0.3
    
    for i in range(n_iter):
        # Forward
        H = X @ W1
        X_hat = H @ W2
        # Loss
        loss = np.mean((X - X_hat)**2)
        # Backward
        d_X_hat = (X_hat - X) / n_samples
        dW2 = H.T @ d_X_hat
        dH = d_X_hat @ W2.T
        dW1 = X.T @ dH
        # Update
        W1 -= lr * dW1
        W2 -= lr * dW2
    
    return W1 @ W2  # 10x10 matrix that the autoencoder applies overall

n_trained = 100
trained_metrics = {'A_in_inv': [], 'lj': [], 'p56_inv': []}
for seed in range(n_trained):
    W = train_simple_autoencoder(seed=seed)
    trained_metrics['A_in_inv'].append(antisym_in_d4_invariant_fraction(W))
    trained_metrics['lj'].append(lie_jordan_ratio(W))
    trained_metrics['p56_inv'].append(p56_invariant_fraction(W))

print(f"\nTrained autoencoder bottleneck (10x10, N={n_trained}):")
print(f"  antisym in D_4-inv: mean {np.mean(trained_metrics['A_in_inv']):.4f} ± {np.std(trained_metrics['A_in_inv']):.4f}")
print(f"  Lie/Jordan ratio:   mean {np.mean(trained_metrics['lj']):.4f} ± {np.std(trained_metrics['lj']):.4f}")
print(f"  P_56-invariant:     mean {np.mean(trained_metrics['p56_inv']):.4f} ± {np.std(trained_metrics['p56_inv']):.4f}")

print()
print("="*70)
print("INTERPRETATION")
print("="*70)
print("""
The structural metrics derived from TSML are mathematically well-defined
for any 10×10 matrix. But they don't necessarily MEAN anything for trained
matrices unless we see a systematic difference between trained and random.

If trained matrices have SYSTEMATICALLY different structural metric values
from random, the metrics are picking up something real about training.

If they're statistically indistinguishable, the metrics are just numerical
features that don't carry training-relevant information.

The baseline test above will tell us which case we're in.
""")
