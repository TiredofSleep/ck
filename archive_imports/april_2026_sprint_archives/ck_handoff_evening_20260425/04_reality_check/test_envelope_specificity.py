"""
The signal: trained matrices have trace_conc in [0.474, 3.407] (TSML/BHML envelope).
Random Gaussian matrices: only 8% inside this envelope.

Question: is this signal SPECIFIC to TSML's anchor positions, or would 
ANY positive-trace anchor give the same result?

If it's specific → TSML carves a meaningful gap
If it's generic → we just rediscovered "trained matrices have positive trace"

Test: try multiple anchor sets and see whether TSML's envelope is special.
"""
import numpy as np

np.random.seed(42)

def coherence_metrics(W):
    eigs = np.linalg.eigvals(W)
    abs_eigs = sorted([abs(e) for e in eigs], reverse=True)
    if abs_eigs[0] > 1e-12:
        gap_ratio = abs_eigs[1] / abs_eigs[0]
    else:
        gap_ratio = 0
    sv = np.linalg.svd(W, compute_uv=False)
    sv2 = sv**2
    if sv2.sum() > 1e-12:
        eff_rank = (sv2.sum())**2 / (sv2**2).sum()
    else:
        eff_rank = 0
    A = (W - W.T) / 2
    total = np.linalg.norm(W) + 1e-12
    antisym_frac = np.linalg.norm(A)**2 / total**2
    tr = np.trace(W)
    trace_concentration = tr / total
    return {'gap_ratio': gap_ratio, 'eff_rank': eff_rank,
            'antisym_frac': antisym_frac, 'trace_conc': trace_concentration}

def train_AE(seed=0, n_iter=3000, lr=0.01):
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

# Generate samples
n = 200
trained = [train_AE(seed=s) for s in range(n)]
random_g = [np.random.randn(10, 10) for _ in range(n)]

trained_m = [coherence_metrics(W) for W in trained]
random_m = [coherence_metrics(W) for W in random_g]

# ============ TEST 1: TSML+BHML vs alternative anchors ============

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
print("TEST: trace_conc envelope from various anchors")
print("="*70)
print()
print("For each anchor set, report:")
print("  - envelope on trace_conc")
print("  - % of trained inside envelope")  
print("  - % of random Gaussian inside envelope")
print("  - separation (trained% - random%)")
print()

def test_envelope(anchors, name, padding=0.1):
    """Test the gap hypothesis for a given anchor set."""
    vals = [coherence_metrics(M)['trace_conc'] for M in anchors]
    lo, hi = min(vals), max(vals)
    pad = padding * (hi - lo) if hi > lo else 0.05
    lo, hi = lo - pad, hi + pad
    
    t_inside = sum(1 for m in trained_m if lo <= m['trace_conc'] <= hi) / len(trained_m)
    r_inside = sum(1 for m in random_m if lo <= m['trace_conc'] <= hi) / len(random_m)
    sep = t_inside - r_inside
    
    print(f"{name:<35} envelope=[{lo:+.2f}, {hi:+.2f}]  trained:{t_inside*100:.0f}% random:{r_inside*100:.0f}%  sep={sep*100:+.0f}%")
    return sep

# (1) TSML + BHML alone
print("CANONICAL TIG ANCHORS:")
test_envelope([T, B], "TSML+BHML")
test_envelope([T, B, np.eye(10)], "TSML+BHML+Identity")
print()

# (2) Random integer matrices as anchors
print("RANDOM INTEGER ANCHORS (control):")
np.random.seed(100)
for trial in range(5):
    anchors = [np.random.randint(0, 10, size=(10, 10)).astype(float) for _ in range(3)]
    test_envelope(anchors, f"3 random integer matrices (trial {trial})")
print()

# (3) Random Gaussian matrices as anchors
print("RANDOM GAUSSIAN ANCHORS (control):")
np.random.seed(200)
for trial in range(5):
    anchors = [np.random.randn(10, 10) for _ in range(3)]
    test_envelope(anchors, f"3 random Gaussian matrices (trial {trial})")
print()

# (4) Hand-crafted POSITIVE-TRACE matrices (control for "positive trace" alone)
print("CONTROL: matrices with positive trace, otherwise random:")
np.random.seed(300)
for trial in range(5):
    anchors = []
    for _ in range(3):
        M = np.random.randn(10, 10)
        # Force positive trace by adding identity multiple
        M += np.eye(10) * abs(np.random.randn() * 2)
        anchors.append(M)
    test_envelope(anchors, f"random + positive trace (trial {trial})")
print()

# (5) Hand-crafted NEGATIVE-TRACE matrices (anti-control)
print("CONTROL: matrices with negative trace:")
np.random.seed(400)
for trial in range(5):
    anchors = []
    for _ in range(3):
        M = np.random.randn(10, 10)
        M -= np.eye(10) * abs(np.random.randn() * 2)
        anchors.append(M)
    test_envelope(anchors, f"random + negative trace (trial {trial})")
print()

# (6) Try a variety of hand-picked anchors
print("MIXED CONTROLS:")
test_envelope([np.eye(10), np.eye(10) * 7, np.diag([7]*10)], "diagonal-ish anchors")
test_envelope([np.ones((10, 10)), np.eye(10), np.diag(range(10))], "structured anchors")

# ============ Now: 2D envelope (trace_conc x antisym_frac) ============
print()
print("="*70)
print("2D ENVELOPE TEST: (trace_conc, antisym_frac)")  
print("="*70)
print()

# TSML: trace_conc ≈ 1.00, antisym ≈ 0.004
# BHML: trace_conc ≈ 0.72, antisym ≈ 0.00
# Both have HIGH trace_conc and LOW antisym
# Gaussian random: low trace, high antisym

# Joint envelope: rectangle around TSML+BHML+Identity
def test_2d_envelope(anchors, name, m_keys=['trace_conc', 'antisym_frac'], padding=0.1):
    bounds = {}
    for k in m_keys:
        vals = [coherence_metrics(M)[k] for M in anchors]
        lo, hi = min(vals), max(vals)
        pad = padding * (hi - lo) if hi > lo else 0.05
        bounds[k] = (lo - pad, hi + pad)
    
    def inside(m):
        return all(bounds[k][0] <= m[k] <= bounds[k][1] for k in m_keys)
    
    t_inside = sum(1 for m in trained_m if inside(m)) / len(trained_m)
    r_inside = sum(1 for m in random_m if inside(m)) / len(random_m)
    
    bound_str = ", ".join(f"{k}: [{bounds[k][0]:+.2f}, {bounds[k][1]:+.2f}]" for k in m_keys)
    print(f"{name:<30} {bound_str}")
    print(f"   trained inside: {t_inside*100:.0f}%   random inside: {r_inside*100:.0f}%   sep: {(t_inside-r_inside)*100:+.0f}%")
    print()

print("(trace_conc, antisym_frac) joint envelope:")
test_2d_envelope([T, B], "TSML+BHML")
test_2d_envelope([T, B, np.eye(10)], "TSML+BHML+I")

# Random anchor controls
print()
print("Control with random Gaussian anchors:")
np.random.seed(999)
for trial in range(3):
    anchors = [np.random.randn(10, 10) for _ in range(3)]
    test_2d_envelope(anchors, f"random Gaussians (trial {trial})")

# ============ The Bigger Question ============
print("="*70)
print("THE BIGGER QUESTION")  
print("="*70)
print("""
If TSML/BHML define a SPECIFIC envelope that's both:
  (a) Tight (trained matrices fit inside)
  (b) Selective (random matrices don't fit)
  
And if random anchors do NOT give equally tight+selective envelopes,

then TSML/BHML are tracking something real about coherence.

The 2D test (trace_conc × antisym_frac) is more discriminating than 1D.
""")
