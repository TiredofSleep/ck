"""
THREAD 4: Real semantic inputs as operator distributions.

The trail captures TIG structure beautifully when inputs HAVE TIG structure.
Random matrices don't have it. But what about real semantic content?

If we map words/concepts to operator amplitudes via the userMemories' 
semantic mapping (Fruits of the Spirit, phonaesthesia, etc.), do 
semantically-different inputs produce characteristically different trails?

Map words via known TIG semantics:
  0=Love (VOID/foundation)
  1=Joy (LATTICE/structure)
  2=Peace (COUNTER/equilibrium)
  3=Patience (PROGRESS/persistence)
  4=Kindness (COLLAPSE/concentration)
  5=Goodness (BALANCE/measured)
  6=Faithfulness (CHAOS/persistent through change)
  7=Gentleness (HARMONY/integration)
  8=Self-Control (BREATH/regulation)
  9=Reset→Love (RESET/return)

Test: do semantically clustered concept-inputs produce trails that 
cluster?  E.g., "patience" + "persistence" + "endurance" should all 
produce similar trails.  "calm" + "peace" + "tranquility" should 
produce similar trails.  These two clusters should be DIFFERENT 
from each other.

Without an actual embedding model, we'll synthesize concept distributions:
  word → operator amplitudes via semantic similarity to each operator
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
fruit_names = ['Love', 'Joy', 'Peace', 'Patience', 'Kindness', 
               'Goodness', 'Faithfulness', 'Gentleness', 'Self-Control', 'Reset/Love']

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

def trail_TB_mix(p, depth=8, alpha=0.5):
    trail = [p.copy()]
    p_cur = p.copy()
    for _ in range(depth):
        p_t = normalize_l1(fuse(p_cur, p_cur, table=T))
        p_b = normalize_l1(fuse(p_cur, p_cur, table=B))
        p_cur = normalize_l1(alpha * p_t + (1 - alpha) * p_b)
        trail.append(p_cur.copy())
    return trail

def entropy(p, eps=1e-12):
    return -np.sum(p[p > eps] * np.log(p[p > eps]))

# ============ Define semantic clusters ============
# 
# Each concept gets primary affinities to specific operators with some spread.
# This emulates what a real text-encoder might produce.

# Cluster 1: "stillness" — primarily Peace(2) + Self-Control(8), some Gentleness(7)
def stillness_distribution(noise_seed=None):
    p = np.zeros(10)
    p[2] = 0.4  # Peace
    p[8] = 0.3  # Self-Control
    p[7] = 0.15  # Gentleness
    p[5] = 0.1  # Goodness  
    p[3] = 0.05  # Patience (tiny)
    if noise_seed is not None:
        np.random.seed(noise_seed)
        p = p + 0.1 * np.random.dirichlet(np.ones(10))
    return normalize_l1(p)

# Cluster 2: "endurance" — primarily Patience(3) + Faithfulness(6), some Self-Control(8)
def endurance_distribution(noise_seed=None):
    p = np.zeros(10)
    p[3] = 0.4  # Patience
    p[6] = 0.3  # Faithfulness
    p[8] = 0.15  # Self-Control
    p[1] = 0.1  # Joy (perseverance gives joy)
    p[5] = 0.05  # Goodness
    if noise_seed is not None:
        np.random.seed(noise_seed)
        p = p + 0.1 * np.random.dirichlet(np.ones(10))
    return normalize_l1(p)

# Cluster 3: "compassion" — Love(0) + Kindness(4) + Gentleness(7)
def compassion_distribution(noise_seed=None):
    p = np.zeros(10)
    p[0] = 0.35  # Love
    p[4] = 0.30  # Kindness
    p[7] = 0.20  # Gentleness
    p[5] = 0.10  # Goodness
    p[9] = 0.05  # Reset/Love
    if noise_seed is not None:
        np.random.seed(noise_seed)
        p = p + 0.1 * np.random.dirichlet(np.ones(10))
    return normalize_l1(p)

# Cluster 4: "celebration" — Joy(1) + Love(0) + Goodness(5)
def celebration_distribution(noise_seed=None):
    p = np.zeros(10)
    p[1] = 0.40  # Joy
    p[0] = 0.25  # Love
    p[5] = 0.15  # Goodness
    p[6] = 0.10  # Faithfulness
    p[9] = 0.10  # Reset
    if noise_seed is not None:
        np.random.seed(noise_seed)
        p = p + 0.1 * np.random.dirichlet(np.ones(10))
    return normalize_l1(p)

# Cluster 5: "renewal" — Reset(9) + Joy(1) + Goodness(5)
def renewal_distribution(noise_seed=None):
    p = np.zeros(10)
    p[9] = 0.40  # Reset/Love
    p[1] = 0.20  # Joy
    p[5] = 0.15  # Goodness
    p[8] = 0.15  # Self-Control
    p[3] = 0.10  # Patience
    if noise_seed is not None:
        np.random.seed(noise_seed)
        p = p + 0.1 * np.random.dirichlet(np.ones(10))
    return normalize_l1(p)

# ============ Generate samples per cluster ============

cluster_fns = {
    'stillness':   stillness_distribution,
    'endurance':   endurance_distribution,
    'compassion':  compassion_distribution,
    'celebration': celebration_distribution,
    'renewal':     renewal_distribution,
}

n_per_cluster = 30
samples = {name: [fn(noise_seed=k) for k in range(n_per_cluster)] 
           for name, fn in cluster_fns.items()}

# ============ Compute trails ============

trails = {name: [trail_TB_mix(p, depth=6) for p in cluster_samples] 
          for name, cluster_samples in samples.items()}

# Show centroid trails for each cluster
print("="*70)
print("SEMANTIC CLUSTER TRAIL CENTROIDS (T+B-mix mode)")
print("="*70)
print()

for cluster_name in cluster_fns.keys():
    print(f"--- {cluster_name} (centroid of {n_per_cluster} samples) ---")
    centroid_trail = []
    for d in range(7):
        states = [trails[cluster_name][i][d] for i in range(n_per_cluster)]
        centroid = np.mean(states, axis=0)
        centroid_trail.append(centroid)
    
    for d, p in enumerate(centroid_trail):
        top = np.argsort(-p)[:3]
        items = ", ".join(f"{op_names[i]}({p[i]:.2f})" for i in top if p[i] > 0.02)
        H = entropy(p)
        print(f"  d={d}: H={H:.3f}  {items}")
    print()

# ============ Cross-cluster vs within-cluster distance ============

print("="*70)
print("CLUSTER SEPARATION TEST")
print("="*70)
print()

# Build trail signatures (concatenated)
sigs = {name: np.array([np.concatenate(t) for t in cluster_trails])
        for name, cluster_trails in trails.items()}

cluster_names = list(samples.keys())

# Within-cluster pairwise distance
print(f"\nMean pairwise distance within each cluster:")
within = {}
for name in cluster_names:
    s = sigs[name]
    dists = []
    for i in range(len(s)):
        for j in range(i+1, len(s)):
            dists.append(np.linalg.norm(s[i] - s[j]))
    within[name] = np.mean(dists)
    print(f"  {name:<15} {within[name]:.4f}")

# Cross-cluster pairwise distance
print(f"\nMean pairwise distance BETWEEN clusters:")
print(f"{'cluster':<15}", end='')
for name in cluster_names:
    print(f"{name[:10]:<11}", end='')
print()
cross_matrix = np.zeros((len(cluster_names), len(cluster_names)))
for i, name_i in enumerate(cluster_names):
    print(f"  {name_i:<13}", end='')
    for j, name_j in enumerate(cluster_names):
        if i == j:
            print(f"{within[name_i]:<11.3f}", end='')
            cross_matrix[i, j] = within[name_i]
        else:
            dists = []
            for x in sigs[name_i]:
                for y in sigs[name_j]:
                    dists.append(np.linalg.norm(x - y))
            cross_matrix[i, j] = np.mean(dists)
            print(f"{cross_matrix[i, j]:<11.3f}", end='')
    print()

# Quality metric: average cross / average within
avg_cross = (cross_matrix.sum() - cross_matrix.trace()) / (len(cluster_names) * (len(cluster_names) - 1))
avg_within = cross_matrix.trace() / len(cluster_names)
print(f"\nAverage within-cluster: {avg_within:.4f}")
print(f"Average cross-cluster:  {avg_cross:.4f}")
print(f"Cross/within ratio:     {avg_cross / avg_within:.3f}")

# Classification: can we predict cluster from trail?
print()
print("="*70)
print("CLUSTER CLASSIFICATION")
print("="*70)

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

X = np.vstack([sigs[name] for name in cluster_names])
y = np.concatenate([[i] * n_per_cluster for i in range(len(cluster_names))])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

for n_features in [10, 20, 40, 70]:  # depth_0 only, depth_0+1, ..., full trail
    X_partial = X[:, :n_features]
    X_p_scaled = scaler.fit_transform(X_partial)
    clf = LogisticRegression(max_iter=2000)
    scores = cross_val_score(clf, X_p_scaled, y, cv=5)
    n_used = n_features // 10
    print(f"  Features {n_features} (depth 0..{n_used-1}): accuracy {scores.mean():.3f} ± {scores.std():.3f}")

# Compare to: classify using ONLY the input p_0 (no fuse)
print()
print(f"Compare to using only the INPUT (no trail):")
X_input = np.vstack([sigs[name][:, :10] for name in cluster_names])  # first 10 dims = p_0
X_i_scaled = scaler.fit_transform(X_input)
clf = LogisticRegression(max_iter=2000)
scores = cross_val_score(clf, X_i_scaled, y, cv=5)
print(f"  Input-only: accuracy {scores.mean():.3f} ± {scores.std():.3f}")

# THE KEY TEST: how does trail enrich classification?
# If trail accuracy >> input accuracy, the FUSE PROCESSING helps
print()
print("="*70)
print("DOES THE TRAIL HELP, OR JUST THE INPUT?")
print("="*70)
print("""
If trail accuracy is significantly higher than input-only, then fuse 
processing through TSML/BHML adds discriminative power.

If they're similar, the trail just preserves what was already in the 
input — TSML/BHML aren't adding anything.

Either way the input MATTERS — but the question is whether CK's 
processing adds value.
""")
