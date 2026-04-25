"""
DIFFERENT FRAMING.

Brayden's hypothesis: "structure remains where it flows through the gap, that 
appears to be operated by ck's tables"

So TSML isn't an envelope you stay inside. TSML is a GATE. Things that SURVIVE 
passage through TSML are coherent. Things that don't survive lose structure.

In matrix terms: passing W through TSML could be:
  W_passed = T @ W @ T (or T·W or W·T)
  or some iterated composition
  
If W is "coherent" relative to TSML, T·W·T preserves W's structure.
If W is incoherent, T·W·T destroys it.

Test: 
  - Pass random matrices through TSML many times.
  - Pass trained matrices through TSML many times.
  - Measure structural survival (do they keep their information?)
  - Compare.

The thing that matters: trained matrices should survive better than random.
If they do, TSML acts as a coherence filter — exactly Brayden's intuition.
"""
import numpy as np

np.random.seed(42)

TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
T = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=float)
T_norm = T / np.linalg.norm(T)  # normalized for repeated application

BHML_ROWS = [
    "0123456789",  "1234567266",  "2334567366",  "3444567466",  "4555567577",
    "5666667677",  "6777777777",  "7234567890",  "8666777978",  "9666777080",
]
B = np.array([[int(c) for c in row] for row in BHML_ROWS], dtype=float)
B_norm = B / np.linalg.norm(B)

# Use the sigma permutation as a structure-preserving operator
sigma_perm = np.array([0, 7, 1, 3, 2, 4, 5, 6, 8, 9])
P_sigma = np.zeros((10, 10))
for i in range(10): P_sigma[sigma_perm[i], i] = 1.0

def survival_score(W, gate, n_iterations=10):
    """
    Measure how much structure W retains after n applications of gate.
    
    Pass W through repeatedly: W_t+1 = (gate @ W_t @ gate) - normalize
    
    Track: does the leading eigenvalue / direction stabilize, or does it 
    decohere into noise?
    
    Returns: cosine similarity between dominant eigenvector at start and end
    """
    W_t = W.copy()
    # Initial dominant direction
    eigs_init, vecs_init = np.linalg.eig(W_t)
    idx_init = np.argmax(np.abs(eigs_init))
    v_init = np.real(vecs_init[:, idx_init])
    v_init = v_init / (np.linalg.norm(v_init) + 1e-12)
    
    # Iterate
    W_history = [W_t.copy()]
    for _ in range(n_iterations):
        W_t = gate @ W_t @ gate
        # Normalize to prevent blowup/collapse
        norm = np.linalg.norm(W_t)
        if norm > 1e-12:
            W_t = W_t / norm
        W_history.append(W_t.copy())
    
    # Final dominant direction
    eigs_final, vecs_final = np.linalg.eig(W_t)
    idx_final = np.argmax(np.abs(eigs_final))
    v_final = np.real(vecs_final[:, idx_final])
    v_final = v_final / (np.linalg.norm(v_final) + 1e-12)
    
    # Cosine similarity (with sign)
    cos_sim = np.dot(v_init, v_final)
    
    # Also: how much information is retained?
    # Use entropy of singular values as proxy
    sv_init = np.linalg.svd(W_history[0], compute_uv=False)
    sv_init = sv_init / (sv_init.sum() + 1e-12)
    sv_final = np.linalg.svd(W_history[-1], compute_uv=False)
    sv_final = sv_final / (sv_final.sum() + 1e-12)
    
    def entropy(p):
        p = p[p > 1e-12]
        return -np.sum(p * np.log(p))
    
    H_init = entropy(sv_init)
    H_final = entropy(sv_final)
    
    return {
        'cos_sim': abs(cos_sim),  # alignment of dominant direction
        'H_init': H_init,
        'H_final': H_final,
        'H_change': H_final - H_init,  # positive = more spread, negative = more concentrated
    }

# Train an AE
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
n_iter = 5

# Trained matrices
print("="*70)
print("PASSAGE THROUGH TSML — DOES STRUCTURE SURVIVE?")
print("="*70)
print()

print(f"Iterations of W → T_norm @ W @ T_norm: n_iter = {n_iter}")
print()

trained_results = []
for seed in range(n):
    W = train_AE(seed=seed)
    W = W / np.linalg.norm(W)  # normalize
    trained_results.append(survival_score(W, T_norm, n_iter))

random_g_results = []
for _ in range(n):
    W = np.random.randn(10, 10)
    W = W / np.linalg.norm(W)
    random_g_results.append(survival_score(W, T_norm, n_iter))

# Aggregate
def agg(results, key):
    return np.mean([r[key] for r in results]), np.std([r[key] for r in results])

print("Through TSML gate:")
print()
print(f"  cos similarity (dominant direction preserved):")
m, s = agg(trained_results, 'cos_sim')
print(f"    trained: {m:.3f} ± {s:.3f}")
m, s = agg(random_g_results, 'cos_sim')
print(f"    random:  {m:.3f} ± {s:.3f}")

print()
print(f"  Singular value entropy change (positive = info loss):")
m, s = agg(trained_results, 'H_change')
print(f"    trained: {m:+.3f} ± {s:.3f}")
m, s = agg(random_g_results, 'H_change')
print(f"    random:  {m:+.3f} ± {s:.3f}")

# Compare against BHML gate
print()
print("Through BHML gate (for comparison):")
print()
trained_results_b = []
random_g_results_b = []
for seed in range(n):
    W = train_AE(seed=seed)
    W = W / np.linalg.norm(W)
    trained_results_b.append(survival_score(W, B_norm, n_iter))
for _ in range(n):
    W = np.random.randn(10, 10)
    W = W / np.linalg.norm(W)
    random_g_results_b.append(survival_score(W, B_norm, n_iter))

m, s = agg(trained_results_b, 'cos_sim')
print(f"  cos similarity (trained): {m:.3f} ± {s:.3f}")
m, s = agg(random_g_results_b, 'cos_sim')
print(f"  cos similarity (random):  {m:.3f} ± {s:.3f}")

# Compare against random matrix gate (control)
print()
print("Through RANDOM matrix gate (control):")
print()
np.random.seed(123)
random_gate = np.random.randn(10, 10)
random_gate = random_gate / np.linalg.norm(random_gate)

trained_rg = []
random_rg = []
for seed in range(n):
    W = train_AE(seed=seed)
    W = W / np.linalg.norm(W)
    trained_rg.append(survival_score(W, random_gate, n_iter))
for _ in range(n):
    W = np.random.randn(10, 10)
    W = W / np.linalg.norm(W)
    random_rg.append(survival_score(W, random_gate, n_iter))

m, s = agg(trained_rg, 'cos_sim')
print(f"  cos similarity (trained): {m:.3f} ± {s:.3f}")
m, s = agg(random_rg, 'cos_sim')
print(f"  cos similarity (random):  {m:.3f} ± {s:.3f}")

# Through Identity (no gate)
print()
print("Through IDENTITY (no gate, sanity check):")
print()
for seed in [0, 1, 2]:
    W = train_AE(seed=seed)
    W = W / np.linalg.norm(W)
    r = survival_score(W, np.eye(10), n_iter)
    print(f"  trained seed {seed}: cos_sim = {r['cos_sim']:.4f}, H_change = {r['H_change']:+.4f}")

# THE KEY TEST: separation (trained - random) under each gate
print()
print("="*70)
print("KEY METRIC: Separation between trained and random matrices")
print("="*70)
print()

def sep(t_results, r_results, key):
    t_mean = np.mean([r[key] for r in t_results])
    r_mean = np.mean([r[key] for r in r_results])
    pooled_std = np.sqrt((np.std([r[key] for r in t_results])**2 + 
                          np.std([r[key] for r in r_results])**2) / 2)
    if pooled_std > 1e-12:
        return (t_mean - r_mean) / pooled_std
    return 0

print(f"Cohen's d for cos_sim difference (trained - random):")
print(f"  TSML gate:        {sep(trained_results, random_g_results, 'cos_sim'):+.3f}")
print(f"  BHML gate:        {sep(trained_results_b, random_g_results_b, 'cos_sim'):+.3f}")
print(f"  Random gate:      {sep(trained_rg, random_rg, 'cos_sim'):+.3f}")

print()
print(f"Cohen's d for H_change (trained - random):")
print(f"  TSML gate:        {sep(trained_results, random_g_results, 'H_change'):+.3f}")
print(f"  BHML gate:        {sep(trained_results_b, random_g_results_b, 'H_change'):+.3f}")
print(f"  Random gate:      {sep(trained_rg, random_rg, 'H_change'):+.3f}")

print()
print("Interpretation:")
print(" - If TSML gate has |d| > 0.5 and random gate has |d| < 0.3, TSML is special")
print(" - If all gates give similar |d|, the signal is just 'matrices iterated lose structure'")
print(" - If random gate gives BIGGER |d| than TSML, TSML is preserving structure better")
