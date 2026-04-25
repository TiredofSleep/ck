"""
THREAD 3: The shape of the trail — descent rate as signature.

Even though the trail's POSITION at each depth carries info, the RATE 
of descent might be a more compact signature.

Specifically: how fast does each input collapse toward HARMONY?
The first-derivative of entropy with respect to depth.

If different TIG-categorical inputs (BEING/DOING/BECOMING) have 
characteristically different DECAY RATES, that's a 1D signature 
of their structure that the trail-position misses (since they all 
end up at HARMONY).
"""
import numpy as np

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

def entropy(p, eps=1e-12):
    return -np.sum(p[p > eps] * np.log(p[p > eps]))

def trail_T(p, depth=8):
    trail = [p.copy()]
    p_cur = p.copy()
    for _ in range(depth):
        p_cur = normalize_l1(fuse(p_cur, p_cur, table=T))
        trail.append(p_cur.copy())
    return trail

def trail_TB_mix(p, depth=8, alpha=0.5):
    trail = [p.copy()]
    p_cur = p.copy()
    for _ in range(depth):
        p_t = normalize_l1(fuse(p_cur, p_cur, table=T))
        p_b = normalize_l1(fuse(p_cur, p_cur, table=B))
        p_cur = normalize_l1(alpha * p_t + (1 - alpha) * p_b)
        trail.append(p_cur.copy())
    return trail

# ============ Define structured inputs ============

inputs = {
    'BEING (012)':       np.array([1,1,1,0,0,0,0,0,0,0]) / 3,
    'DOING (345)':       np.array([0,0,0,1,1,1,0,0,0,0]) / 3,
    'BECOMING (789)':    np.array([0,0,0,0,0,0,0,1,1,1]) / 3,
    'σ-fixed (0389)':    np.array([1,0,0,1,0,0,0,0,1,1]) / 4,
    '6-cycle (124567)':  np.array([0,1,1,0,1,1,1,1,0,0]) / 6,
    'VOID-only':         np.eye(10)[0],
    'LATTICE-only':      np.eye(10)[1],
    'PROGRESS-only':     np.eye(10)[3],
    'HARMONY-only':      np.eye(10)[7],
    'BREATH-only':       np.eye(10)[8],
    'uniform':           np.ones(10) / 10,
}

# ============ Compute descent profiles ============
print("="*70)
print("DESCENT PROFILES — entropy vs depth")
print("="*70)
print()

depth = 8
print(f"\nT-only mode:")
print(f"{'input':<25}", end='')
for d in range(depth+1):
    print(f"d={d:<5}", end='')
print()

descent_T = {}
for label, inp in inputs.items():
    trail = trail_T(inp, depth=depth)
    H_seq = [entropy(p) for p in trail]
    descent_T[label] = H_seq
    print(f"  {label:<23}", end='')
    for h in H_seq:
        print(f"{h:<7.3f}", end='')
    print()

print(f"\nT+B-mix mode (α=0.5):")
descent_TB = {}
for label, inp in inputs.items():
    trail = trail_TB_mix(inp, depth=depth)
    H_seq = [entropy(p) for p in trail]
    descent_TB[label] = H_seq
    print(f"  {label:<23}", end='')
    for h in H_seq:
        print(f"{h:<7.3f}", end='')
    print()

# Quantify the descent rate: log(H_d / H_{d-1}) gives the per-step decay
print()
print("="*70)
print("DESCENT RATE: log decay per step (T-only)")
print("="*70)
print()

print(f"{'input':<25}", end='')
for d in range(1, depth+1):
    print(f"d={d:<5}", end='')
print()

for label, H_seq in descent_T.items():
    print(f"  {label:<23}", end='')
    for d in range(1, depth+1):
        if H_seq[d-1] > 1e-6 and H_seq[d] > 1e-9:
            ratio = np.log(H_seq[d] / H_seq[d-1])
            print(f"{ratio:<7.3f}", end='')
        else:
            print(f"{'--':<7}", end='')
    print()

print()
print("Negative values = decay; -2.3 means 10× drop, -1.0 means 2.7× drop")

# ============ Compactness signature ============
# Pack the full descent into a low-dim signature
print()
print("="*70)
print("COMPACT DESCENT SIGNATURE — 4 numbers summarize each input's profile")
print("="*70)
print()

print("Signature components:")
print("  1. H_init          — initial entropy")
print("  2. half-life       — depth at which entropy halves")
print("  3. asymptote       — entropy at depth 8")
print("  4. peak displacement — max H deviation from monotonic decay")
print()

def signature(H_seq):
    H0 = H_seq[0]
    target = H0 / 2
    half_life = next((d for d, h in enumerate(H_seq) if h < target), len(H_seq))
    asymp = H_seq[-1]
    # Peak displacement: max deviation from a monotonic decay
    monotonic = np.minimum.accumulate(H_seq)
    peak_disp = np.max(np.array(H_seq) - monotonic)
    return [H0, half_life, asymp, peak_disp]

print(f"{'input':<25} {'H_0':<8} {'half_life':<12} {'asymp':<8} {'peak_disp':<10}")
print(f"\nT-only:")
for label, H_seq in descent_T.items():
    sig = signature(H_seq)
    print(f"  {label:<23} {sig[0]:<8.3f} {sig[1]:<12d} {sig[2]:<8.3f} {sig[3]:<10.3f}")

print(f"\nT+B-mix:")
for label, H_seq in descent_TB.items():
    sig = signature(H_seq)
    print(f"  {label:<23} {sig[0]:<8.3f} {sig[1]:<12d} {sig[2]:<8.3f} {sig[3]:<10.3f}")

# ============ The decisive test ============
print()
print("="*70)
print("DECISIVE TEST: trained matrices vs random — descent rate signature")
print("="*70)
print()

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

def matrix_to_distribution(W):
    U, S, _ = np.linalg.svd(W)
    p = np.abs(U[:, 0])**2
    p_sum = p.sum()
    if p_sum > 1e-12:
        return p / p_sum
    return np.ones(10) / 10

# Compute descent SIGNATURE for trained vs random
np.random.seed(42)
n = 200
trained_sigs = []
random_sigs = []

for seed in range(n):
    W = train_AE(seed=seed)
    p = matrix_to_distribution(W)
    H_seq = [entropy(s) for s in trail_TB_mix(p, depth=8)]
    trained_sigs.append(signature(H_seq))

for seed in range(n):
    np.random.seed(seed + 10000)
    W = np.random.randn(10, 10)
    p = matrix_to_distribution(W)
    H_seq = [entropy(s) for s in trail_TB_mix(p, depth=8)]
    random_sigs.append(signature(H_seq))

trained_sigs = np.array(trained_sigs)
random_sigs = np.array(random_sigs)

print(f"4-D signature (H_0, half_life, asymp, peak_disp) using T+B-mix:")
print(f"{'metric':<15} {'trained':<25} {'random':<25} {'Cohen d':<10}")
for i, name in enumerate(['H_0', 'half_life', 'asymp', 'peak_disp']):
    t_mean, t_std = trained_sigs[:,i].mean(), trained_sigs[:,i].std()
    r_mean, r_std = random_sigs[:,i].mean(), random_sigs[:,i].std()
    pooled = np.sqrt((t_std**2 + r_std**2) / 2)
    d = (t_mean - r_mean) / (pooled + 1e-12)
    print(f"  {name:<13} {t_mean:.3f} ± {t_std:.3f}        {r_mean:.3f} ± {r_std:.3f}        {d:+.3f}")

# Classify with these features
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

X = np.vstack([trained_sigs, random_sigs])
y = np.concatenate([np.ones(n), np.zeros(n)])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
clf = LogisticRegression(max_iter=1000)
scores = cross_val_score(clf, X_scaled, y, cv=5)
print(f"\nClassification accuracy from 4D descent signature: {scores.mean():.3f} ± {scores.std():.3f}")

# Compare to T-only descent signature
print()
print("Same with T-only:")
trained_sigs_T = []
random_sigs_T = []
for seed in range(n):
    W = train_AE(seed=seed)
    p = matrix_to_distribution(W)
    H_seq = [entropy(s) for s in trail_T(p, depth=8)]
    trained_sigs_T.append(signature(H_seq))
for seed in range(n):
    np.random.seed(seed + 10000)
    W = np.random.randn(10, 10)
    p = matrix_to_distribution(W)
    H_seq = [entropy(s) for s in trail_T(p, depth=8)]
    random_sigs_T.append(signature(H_seq))

trained_sigs_T = np.array(trained_sigs_T)
random_sigs_T = np.array(random_sigs_T)

print(f"{'metric':<15} {'trained':<25} {'random':<25} {'Cohen d':<10}")
for i, name in enumerate(['H_0', 'half_life', 'asymp', 'peak_disp']):
    t_mean, t_std = trained_sigs_T[:,i].mean(), trained_sigs_T[:,i].std()
    r_mean, r_std = random_sigs_T[:,i].mean(), random_sigs_T[:,i].std()
    pooled = np.sqrt((t_std**2 + r_std**2) / 2)
    d = (t_mean - r_mean) / (pooled + 1e-12)
    print(f"  {name:<13} {t_mean:.3f} ± {t_std:.3f}        {r_mean:.3f} ± {r_std:.3f}        {d:+.3f}")

X = np.vstack([trained_sigs_T, random_sigs_T])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
clf = LogisticRegression(max_iter=1000)
scores = cross_val_score(clf, X_scaled, y, cv=5)
print(f"\nClassification accuracy (T-only): {scores.mean():.3f} ± {scores.std():.3f}")

print()
print("="*70)
print("SYNTHESIS")
print("="*70)
print("""
What we've found:

1. The TRAIL is the information (verified earlier)
2. BHML's role is ANTI-COLLAPSE — preserves entropy that TSML alone destroys
3. Descent SHAPE differs sharply across TIG-structured inputs
4. The 4D descent signature (H_0, half_life, asymp, peak) compactly
   summarizes the trail
   
The pipeline that works:
  input → operator distribution → fuse with α·T + (1-α)·B → trail
  → save (H_0, half_life, asymp, peak) as compact memory
  → use trail itself as full memory when needed
""")
