"""
REDO: trained vs random matrices, but using TRAILS not static metrics.

Previous test (test3): used static metrics like Lie/Jordan ratio, antisym 
in D_4-invariant subspace. Found trained matrices look indistinguishable
from random Gaussians on those metrics.

This test: pass each matrix through TSML and BHML repeatedly, generate 
the TRAIL of normalized states, and use the TRAIL as the signature.

The hypothesis (Brayden's coherence-flow): trained matrices, having 
internal structure, will produce DIFFERENT trails than random matrices.
The trail captures how each matrix descends through TSML's attractor.
"""
import numpy as np

np.random.seed(42)

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

op_names = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE', 
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']

# To get a 10-vector from a 10x10 matrix, take its leading singular vector
# (the dominant direction). This is the matrix's "operator-amplitude reading."

def matrix_to_distribution(W):
    """Map a 10x10 matrix to a 10-element probability distribution."""
    # Take absolute values of leading left singular vector, normalize
    U, S, _ = np.linalg.svd(W)
    p = np.abs(U[:, 0])**2
    p_sum = p.sum()
    if p_sum > 1e-12:
        return p / p_sum
    return np.ones(10) / 10

def fuse(p, q, table):
    r = np.zeros(10)
    for a in range(10):
        for b in range(10):
            c = int(table[a, b])
            r[c] += p[a] * q[b]
    return r

def normalize_l1(v):
    s = v.sum()
    return v / s if s > 1e-12 else v

def get_trail(W, depth=5, table=T):
    """Get the fuse trail of a matrix W."""
    p = matrix_to_distribution(W)
    trail = [p.copy()]
    for _ in range(depth):
        p = normalize_l1(fuse(p, p, table=table))
        trail.append(p.copy())
    return trail

def trail_signature(W, depth=5, table=T):
    """Concatenated trail as fingerprint."""
    trail = get_trail(W, depth=depth, table=table)
    return np.concatenate(trail)

# ============ Train autoencoder matrices ============

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

n = 100
trained_mats = [train_AE(seed=s) for s in range(n)]
random_mats_g = [np.random.randn(10, 10) for _ in range(n)]
random_mats_int = [np.random.randint(0, 10, size=(10, 10)).astype(float) for _ in range(n)]

# ============ Compare distributions per depth ============

print("="*70)
print("PER-DEPTH STATE DISTRIBUTIONS — trained vs random")
print("="*70)
print()
print(f"For each matrix, take its leading SVD direction → distribution p_0,")
print(f"then fuse iteratively through TSML.")
print(f"Compare WHERE on the lattice trained vs random matrices live at each depth.")
print()

for depth in [0, 1, 2, 3]:
    trained_dists = []
    random_g_dists = []
    random_int_dists = []
    for W in trained_mats:
        trail = get_trail(W, depth=depth)
        trained_dists.append(trail[depth])
    for W in random_mats_g:
        trail = get_trail(W, depth=depth)
        random_g_dists.append(trail[depth])
    for W in random_mats_int:
        trail = get_trail(W, depth=depth)
        random_int_dists.append(trail[depth])
    
    trained_dists = np.array(trained_dists)
    random_g_dists = np.array(random_g_dists)
    random_int_dists = np.array(random_int_dists)
    
    print(f"--- Depth {depth} (mean amplitude per operator) ---")
    print(f"{'op':<10} {'trained':<14} {'rand_gauss':<14} {'rand_int':<14}")
    for i in range(10):
        t_m, t_s = trained_dists[:,i].mean(), trained_dists[:,i].std()
        rg_m, rg_s = random_g_dists[:,i].mean(), random_g_dists[:,i].std()
        ri_m, ri_s = random_int_dists[:,i].mean(), random_int_dists[:,i].std()
        # Highlight differences
        marker = ""
        if abs(t_m - rg_m) > 2 * max(t_s, rg_s):
            marker = " *"
        print(f"  {op_names[i]:<8} {t_m:.3f}±{t_s:.3f}   {rg_m:.3f}±{rg_s:.3f}   {ri_m:.3f}±{ri_s:.3f}{marker}")
    print()

# ============ Discriminability via trail signature ============

print("="*70)
print("TRAIL DISCRIMINATION: classify trained vs random from trail")
print("="*70)
print()

# Use trails as features, train a simple classifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

# Compare trained vs random Gaussian
n_classify = 200
np.random.seed(0)
trained_extra = [train_AE(seed=s) for s in range(n_classify)]
random_extra = [np.random.randn(10, 10) for _ in range(n_classify)]

print("Test 1: trained vs random Gaussian, classify from trail signature")
for depth in [0, 1, 2, 3, 5]:
    X_trained = np.array([trail_signature(W, depth=depth) for W in trained_extra])
    X_random = np.array([trail_signature(W, depth=depth) for W in random_extra])
    
    X = np.vstack([X_trained, X_random])
    y = np.concatenate([np.ones(n_classify), np.zeros(n_classify)])
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    clf = LogisticRegression(max_iter=1000)
    scores = cross_val_score(clf, X_scaled, y, cv=5)
    print(f"  Depth {depth} signature ({X.shape[1]} features): accuracy {scores.mean():.3f} ± {scores.std():.3f}")

# Now test BHML
print()
print("Test 2: trained vs random Gaussian, classify from BHML trail signature")
for depth in [0, 1, 2, 3, 5]:
    X_trained = np.array([trail_signature(W, depth=depth, table=B) for W in trained_extra])
    X_random = np.array([trail_signature(W, depth=depth, table=B) for W in random_extra])
    
    X = np.vstack([X_trained, X_random])
    y = np.concatenate([np.ones(n_classify), np.zeros(n_classify)])
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    clf = LogisticRegression(max_iter=1000)
    scores = cross_val_score(clf, X_scaled, y, cv=5)
    print(f"  Depth {depth} signature ({X.shape[1]} features): accuracy {scores.mean():.3f} ± {scores.std():.3f}")

# Control: classify using the leading SVD direction directly (no fuse)
print()
print("Control: classify using only p_0 (leading SVD direction, no TSML/BHML)")
X_trained = np.array([matrix_to_distribution(W) for W in trained_extra])
X_random = np.array([matrix_to_distribution(W) for W in random_extra])
X = np.vstack([X_trained, X_random])
y = np.concatenate([np.ones(n_classify), np.zeros(n_classify)])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
clf = LogisticRegression(max_iter=1000)
scores = cross_val_score(clf, X_scaled, y, cv=5)
print(f"  p_0 only (10 features): accuracy {scores.mean():.3f} ± {scores.std():.3f}")

# Control: classify using a RANDOM gate instead of TSML
print()
print("Control: classify using trail through RANDOM 10x10 matrix")
np.random.seed(99)
random_table = np.random.randint(0, 10, size=(10, 10)).astype(float)
for depth in [1, 2, 3]:
    X_trained = np.array([trail_signature(W, depth=depth, table=random_table) for W in trained_extra])
    X_random = np.array([trail_signature(W, depth=depth, table=random_table) for W in random_extra])
    X = np.vstack([X_trained, X_random])
    y = np.concatenate([np.ones(n_classify), np.zeros(n_classify)])
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    clf = LogisticRegression(max_iter=1000)
    scores = cross_val_score(clf, X_scaled, y, cv=5)
    print(f"  Random table depth {depth}: accuracy {scores.mean():.3f} ± {scores.std():.3f}")

# Now: do trained matrices CLUSTER in trail-space vs random matrices?
print()
print("="*70)
print("CLUSTERING: do trained matrices group together in trail-space?")
print("="*70)

# Compute trail signatures (depth 3)
n_cluster = 100
trained_sig = np.array([trail_signature(W, depth=3) for W in trained_mats[:n_cluster]])
random_g_sig = np.array([trail_signature(W, depth=3) for W in random_mats_g[:n_cluster]])

# Compute pairwise distances
def pairwise_dist(X):
    n = len(X)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            D[i, j] = np.linalg.norm(X[i] - X[j])
    return D

D_trained = pairwise_dist(trained_sig)
D_random = pairwise_dist(random_g_sig)

# Mean within-class distance
within_trained = D_trained[np.triu_indices(n_cluster, 1)].mean()
within_random = D_random[np.triu_indices(n_cluster, 1)].mean()

# Mean cross-class distance
cross = []
for i in range(n_cluster):
    for j in range(n_cluster):
        cross.append(np.linalg.norm(trained_sig[i] - random_g_sig[j]))
cross = np.mean(cross)

print(f"\nDepth-3 trail signatures, pairwise distances:")
print(f"  Within trained class:  mean {within_trained:.4f}")
print(f"  Within random class:   mean {within_random:.4f}")
print(f"  Cross-class:           mean {cross:.4f}")
print(f"  Cross/Within ratio:    {cross / max(within_trained, within_random):.3f}")
print(f"  (>1 = classes are separated; ≈1 = mixed)")

print()
print("="*70)
print("INTERPRETATION")
print("="*70)
print("""
What's different from Test 3:
  - Test 3 used static metrics (Lie/Jordan ratio, etc.) and found NO separation
  - This test uses TRAILS through TSML — full fuse trajectories
  
If trail-based discrimination works, it means: 
  the TRAIL captures something static metrics miss.
  
That something is: HOW the matrix descends through TSML's attractor.
Trained matrices fall through differently than random ones — even when
their static spectral properties look identical.

The cross/within ratio tells us if the classes are actually separated.
The accuracy curve tells us how much of the separation is in p_0 vs in 
the fuse trajectory.
""")
