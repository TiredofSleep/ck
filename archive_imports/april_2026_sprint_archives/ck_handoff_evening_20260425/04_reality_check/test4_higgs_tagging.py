"""
TEST 4: Is the 9-vector Higgs direction useful for tagging weight matrices?

Proposed by Gemini: "tag layers by proximity to the 9-vector Higgs direction"

The 9-vector Higgs lives in a specific 9-dim subspace of R^10. To "tag" a
weight matrix W by its proximity, we'd need:
  - W to live in a 10-dim space (so we can project)
  - A meaningful sense of "proximity"

For weight matrices in R^{N×M} with N, M ≠ 10, this isn't obvious.
For 10×10 weight matrices, we can project to the 9-vector and see what 
fraction of W aligns with it.

But: WHY would alignment with this direction be meaningful for ML?
The 9-vector is the symmetry-breaking direction in TIG. ML weight matrices
don't have this symmetry to break. So projecting onto the 9-vector is 
applying a TIG-internal coordinate to objects that don't have TIG-internal
content.

Let me check anyway. Maybe there's a surprise.
"""
import numpy as np

np.random.seed(42)

# The 9-vector Higgs direction
higgs_9vec = np.zeros(10)
higgs_9vec[0] = -1/np.sqrt(2)
higgs_9vec[1] = -1/np.sqrt(2)
higgs_9vec[2] = -1/np.sqrt(2)
higgs_9vec[3] = -1/np.sqrt(2)
higgs_9vec[4] = -1/np.sqrt(2)
higgs_9vec[7] = -1/np.sqrt(2)
higgs_9vec[5] = -1/(2*np.sqrt(2))
higgs_9vec[6] = -1/(2*np.sqrt(2))
# higgs_9vec[8] and [9] are 0 (BREATH and RESET excluded)
higgs_9vec_normalized = higgs_9vec / np.linalg.norm(higgs_9vec)

print(f"Higgs 9-vector (normalized):")
print(f"  {higgs_9vec_normalized}")
print(f"  Norm: {np.linalg.norm(higgs_9vec_normalized):.4f}")

# To project a 10x10 matrix onto this direction, we view it as a vector in R^100
# But the 9-vector is in R^10. So we need to extend it.
# 
# Natural extension: outer product. Higgs direction as 10x10 matrix is
# v ⊗ v^T where v is the 9-vector.

higgs_matrix = np.outer(higgs_9vec_normalized, higgs_9vec_normalized)
print(f"\nHiggs as 10×10 outer product matrix, shape: {higgs_matrix.shape}")
print(f"Frobenius norm: {np.linalg.norm(higgs_matrix):.4f}")  # Should be 1

def higgs_alignment(W):
    """Inner product of W with the Higgs outer-product matrix, normalized."""
    W_norm = np.linalg.norm(W)
    if W_norm < 1e-12:
        return 0.0
    return np.sum(W * higgs_matrix) / W_norm

# Reference: TSML and BHML
TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
T = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=float)
BHML_ROWS = [
    "0123456789",  "1234567266",  "2334567366",  "3444567466",  "4555567577",
    "5666667677",  "6777777777",  "7234567890",  "8666777978",  "9666777080",
]
B = np.array([[int(c) for c in row] for row in BHML_ROWS], dtype=float)

print(f"\nHiggs alignment of TSML: {higgs_alignment(T):.4f}")
print(f"Higgs alignment of BHML: {higgs_alignment(B):.4f}")
print(f"  (BHML should align more strongly since the Higgs IS BHML's breaking direction)")

# Random baselines
N = 1000
align_random = []
for _ in range(N):
    W = np.random.randn(10, 10)
    align_random.append(higgs_alignment(W))
print(f"\nRandom Gaussian: alignment mean {np.mean(align_random):+.4f} ± {np.std(align_random):.4f}")

align_random_int = []
for _ in range(N):
    W = np.random.randint(0, 10, size=(10, 10)).astype(float)
    align_random_int.append(higgs_alignment(W))
print(f"Random Int [0,9]: alignment mean {np.mean(align_random_int):+.4f} ± {np.std(align_random_int):.4f}")

# Trained autoencoder
def train_AE(seed=0, n_iter=2000, lr=0.01):
    np.random.seed(seed)
    n_samples = 200
    z = np.random.randn(n_samples, 3)
    M = np.random.randn(3, 10)
    X = z @ M + 0.1 * np.random.randn(n_samples, 10)
    W1 = np.random.randn(10, 5) * 0.3
    W2 = np.random.randn(5, 10) * 0.3
    for i in range(n_iter):
        H = X @ W1
        X_hat = H @ W2
        d_X_hat = (X_hat - X) / n_samples
        dW2 = H.T @ d_X_hat
        dH = d_X_hat @ W2.T
        dW1 = X.T @ dH
        W1 -= lr * dW1
        W2 -= lr * dW2
    return W1 @ W2

n_trained = 100
align_trained = []
for seed in range(n_trained):
    W = train_AE(seed=seed)
    align_trained.append(higgs_alignment(W))
print(f"\nTrained AE (N={n_trained}): alignment mean {np.mean(align_trained):+.4f} ± {np.std(align_trained):.4f}")

print()
print("="*70)
print("INTERPRETATION")
print("="*70)
print(f"""
TSML alignment: {higgs_alignment(T):+.4f}
BHML alignment: {higgs_alignment(B):+.4f}
Random Gauss:   {np.mean(align_random):+.4f} ± {np.std(align_random):.4f}
Random Int:     {np.mean(align_random_int):+.4f} ± {np.std(align_random_int):.4f}
Trained AE:     {np.mean(align_trained):+.4f} ± {np.std(align_trained):.4f}

If TSML/BHML were OUTLIERS in alignment compared to random/trained, 
the alignment would be a meaningful tag.

If trained matrices show a SYSTEMATIC shift in alignment vs random, 
the tag picks up training-relevant content.

Otherwise, it's a numerical feature without ML meaning.
""")

# Now: a more careful test. Can we PREDICT the trained-vs-random distinction 
# from these features?

# Take all metrics together and see if they form a separable cloud
print("="*70)
print("SEPARABILITY: can structural metrics distinguish trained from random?")
print("="*70)

# Train more samples, compute all metrics, check separation
import sys

def all_metrics(W):
    A = (W - W.T) / 2
    S = (W + W.T) / 2
    A_norm = np.linalg.norm(A) + 1e-12
    S_norm = np.linalg.norm(S) + 1e-12
    return [
        np.sum(W * higgs_matrix) / np.linalg.norm(W),  # higgs alignment
        A_norm / S_norm,                                # lie/jordan
        np.trace(W) / 10,                              # mean diagonal
        np.linalg.norm(W),                             # frobenius
        np.linalg.eigvals(W).max().real,               # max eigenvalue real part
    ]

n = 200
random_features = []
trained_features = []

for _ in range(n):
    W_rand = np.random.randn(10, 10)
    random_features.append(all_metrics(W_rand))

for seed in range(n):
    W_train = train_AE(seed=seed)
    trained_features.append(all_metrics(W_train))

random_features = np.array(random_features)
trained_features = np.array(trained_features)

print(f"\nMean +/- std for each metric:")
metric_names = ['Higgs alignment', 'Lie/Jordan', 'Mean diag', 'Frobenius', 'Max eig']
for i, name in enumerate(metric_names):
    rm, rs = random_features[:,i].mean(), random_features[:,i].std()
    tm, ts = trained_features[:,i].mean(), trained_features[:,i].std()
    # Effect size (Cohen's d)
    pooled_std = np.sqrt((rs**2 + ts**2) / 2)
    d = (tm - rm) / (pooled_std + 1e-12)
    print(f"  {name:<20}: random {rm:+.3f}±{rs:.3f}  trained {tm:+.3f}±{ts:.3f}  Cohen's d = {d:+.2f}")

print(f"""
Cohen's d interpretation:
  |d| < 0.2: negligible difference
  |d| < 0.5: small
  |d| < 0.8: medium  
  |d| > 0.8: large

If Higgs alignment has |d| < 0.5, it's NOT meaningfully distinguishing 
trained from random.
""")
