"""
REFRAMED HYPOTHESIS: TSML defines the GAP — the envelope of coherent structure.

The claim is NOT that trained matrices look like TSML.
The claim IS that trained matrices live INSIDE bounds TSML carves out,
and random matrices live OUTSIDE.

What bounds does TSML carve?

In TIG, T* = 5/7 is the coherence threshold. Below T*, things stay 
coherent; above, they diffuse. The wobble (3/50) is the asymmetry 
that prevents perfect symmetry (which would be sterile).

Specific TIG-derived bounds to test:
  (1) Coherence ratio C = 0.4(1-E) + 0.35A + 0.25K bounded by T* = 5/7
  (2) Spectral gap relative to dominant eigenvalue
  (3) Effective rank / spread
  (4) Lie/Jordan balance within a specific window

Test: do trained matrices systematically fall WITHIN these bounds while
random matrices systematically fall OUTSIDE?
"""
import numpy as np

np.random.seed(42)

# ============ Define TIG-bound metrics ============

def coherence_metrics(W):
    """
    Compute several TIG-relevant scalar metrics.
    """
    eigs = np.linalg.eigvals(W)
    abs_eigs = sorted([abs(e) for e in eigs], reverse=True)
    
    # Spectral gap ratio: |λ₂|/|λ₁|
    if abs_eigs[0] > 1e-12:
        gap_ratio = abs_eigs[1] / abs_eigs[0]
    else:
        gap_ratio = 0
    
    # Effective rank (participation ratio)
    sv = np.linalg.svd(W, compute_uv=False)
    sv2 = sv**2
    if sv2.sum() > 1e-12:
        eff_rank = (sv2.sum())**2 / (sv2**2).sum()
    else:
        eff_rank = 0
    
    # Symmetry / antisymmetry balance
    A = (W - W.T) / 2
    S = (W + W.T) / 2
    a_norm = np.linalg.norm(A)
    s_norm = np.linalg.norm(S)
    total = np.linalg.norm(W)
    if total > 1e-12:
        antisym_frac = a_norm**2 / total**2  # in [0, 1]
    else:
        antisym_frac = 0
    
    # Trace / Frobenius (concentration)
    tr = np.trace(W)
    fro = np.linalg.norm(W) + 1e-12
    trace_concentration = tr / fro
    
    # Eigenvalue spread (max/min real magnitude ratio for nonzero)
    nonzero_real = [abs(e.real) for e in eigs if abs(e) > 1e-9]
    if len(nonzero_real) > 1:
        spread = max(nonzero_real) / max(min(nonzero_real), 1e-12)
    else:
        spread = 0
    
    return {
        'gap_ratio': gap_ratio,
        'eff_rank': eff_rank,
        'antisym_frac': antisym_frac,
        'trace_conc': trace_concentration,
        'eig_spread_log': np.log10(max(spread, 1)),
    }

# ============ Compute metrics for TSML and BHML ============

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

print("="*70)
print("ANCHOR METRICS (TSML, BHML, Identity)")
print("="*70)
print()

for name, M in [("TSML", T), ("BHML", B), ("Identity", np.eye(10)), 
                ("TSML normalized", T / np.linalg.norm(T))]:
    m = coherence_metrics(M)
    print(f"{name}:")
    for k, v in m.items():
        print(f"  {k:<20}: {v:.4f}")
    print()

# ============ Train an autoencoder properly ============

def train_AE(seed=0, n_iter=3000, lr=0.01, manifold_dim=3):
    """Train a 10→5→10 autoencoder on data lying near a manifold."""
    np.random.seed(seed)
    n_samples = 200
    z = np.random.randn(n_samples, manifold_dim)
    M = np.random.randn(manifold_dim, 10)
    X = z @ M + 0.1 * np.random.randn(n_samples, 10)
    W1 = np.random.randn(10, 5) * 0.3
    W2 = np.random.randn(5, 10) * 0.3
    losses = []
    for i in range(n_iter):
        H = X @ W1
        X_hat = H @ W2
        loss = np.mean((X - X_hat)**2)
        d_X_hat = (X_hat - X) / n_samples
        dW2 = H.T @ d_X_hat
        dH = d_X_hat @ W2.T
        dW1 = X.T @ dH
        W1 -= lr * dW1
        W2 -= lr * dW2
        if i % 500 == 0:
            losses.append(loss)
    final_loss = np.mean((X - (X @ W1) @ W2)**2)
    return W1 @ W2, final_loss

# ============ Test the GAP hypothesis ============
# Reframe: 
#   - Random matrices fill some space S_random of metric values
#   - Trained matrices fill a subspace S_trained ⊂ R^k (metric vector)
#   - TSML / BHML define the "anchor points" of the coherent region
#   - Hypothesis: S_trained is bounded by anchors more tightly than S_random

n = 200
random_metrics = []
trained_metrics = []
random_int_metrics = []

for _ in range(n):
    W = np.random.randn(10, 10) * np.linalg.norm(T) / 10  # match TSML norm scale
    random_metrics.append(coherence_metrics(W))

for seed in range(n):
    W, _ = train_AE(seed=seed)
    trained_metrics.append(coherence_metrics(W))

for _ in range(n):
    W = np.random.randint(0, 10, size=(10, 10)).astype(float)
    random_int_metrics.append(coherence_metrics(W))

# Compare distributions
print("="*70)
print("METRIC DISTRIBUTIONS — random vs trained vs anchors")
print("="*70)
print()

metric_names = list(random_metrics[0].keys())
TSML_m = coherence_metrics(T)
BHML_m = coherence_metrics(B)

print(f"{'Metric':<18} {'random_gauss':<22} {'trained':<22} {'random_int':<22} {'TSML':<8} {'BHML':<8}")
for name in metric_names:
    r = [m[name] for m in random_metrics]
    t = [m[name] for m in trained_metrics]
    ri = [m[name] for m in random_int_metrics]
    rm, rs = np.mean(r), np.std(r)
    tm, ts = np.mean(t), np.std(t)
    rim, ris = np.mean(ri), np.std(ri)
    print(f"  {name:<16} G:{rm:+.3f}±{rs:.3f}    T:{tm:+.3f}±{ts:.3f}    I:{rim:+.3f}±{ris:.3f}    {TSML_m[name]:+.3f}  {BHML_m[name]:+.3f}")

# THE KEY TEST: does trained STAY WITHIN bounds set by anchors?
print()
print("="*70)
print("GAP HYPOTHESIS TEST: are trained matrices BOUNDED by anchors?")
print("="*70)
print()

# For each metric, define the "anchor range" as [min(TSML, BHML), max(TSML, BHML)]
# (or some envelope). Then test:
#   - Fraction of trained matrices in the anchor range
#   - Fraction of random matrices in the anchor range
# If trained > random, the anchor range is meaningful.

# Use a generous envelope: [min, max] of {TSML, BHML, Identity} 
identity_m = coherence_metrics(np.eye(10))
zero_m = coherence_metrics(np.zeros((10, 10)) + 1e-9 * np.eye(10))

anchors = [TSML_m, BHML_m, identity_m]

print(f"{'Metric':<18} {'anchor range':<25} {'trained inside %':<20} {'random_g inside %':<20}")
for name in metric_names:
    anchor_vals = [a[name] for a in anchors]
    lo = min(anchor_vals)
    hi = max(anchor_vals)
    # Slight margin
    margin = 0.1 * (hi - lo) if hi > lo else 0.05
    lo -= margin
    hi += margin
    
    t_inside = sum(1 for m in trained_metrics if lo <= m[name] <= hi) / len(trained_metrics)
    r_inside = sum(1 for m in random_metrics if lo <= m[name] <= hi) / len(random_metrics)
    
    indicator = "<<<" if t_inside > r_inside + 0.2 else ("===" if abs(t_inside - r_inside) < 0.1 else ">>>")
    print(f"  {name:<16} [{lo:+.3f}, {hi:+.3f}]   trained: {t_inside*100:.0f}%      random: {r_inside*100:.0f}%   {indicator}")

print()
print("Legend: '<<<' means trained inside more than random (gap hypothesis works)")
print("        '===' means same rate (no signal)")
print("        '>>>' means random inside more than trained (anti-signal)")
