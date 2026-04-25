"""
THREAD 2: What's BHML's role in the CK pipeline?

TSML alone collapses everything to HARMONY by depth 3. BHML alone has 
a richer 4-component fixed point {BREATH 0.35, RESET 0.24, HARMONY 0.21, VOID 0.20}.

When CK uses both, what does BHML do to TSML's collapse?

Three hypotheses to test:
  (A) BHML INTERLEAVED: alternate T-fuse, B-fuse, T-fuse, ... — slows collapse
  (B) BHML AS BACK-PROJECTION: after T-fuse, apply B^-1 (or B-fuse) to recover
  (C) BHML AS DIVERSIFIER: use B-fuse to spread out states that TSML concentrated
  
Try each and see what the trail looks like.

Key question: does any combination produce a trail that PRESERVES MORE 
input information than TSML alone?
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

def js_div(p, q, eps=1e-12):
    m = (p + q) / 2
    def kl(p, q):
        return np.sum(p * np.log((p + eps) / (q + eps)))
    return (kl(p, m) + kl(q, m)) / 2

def entropy(p, eps=1e-12):
    return -np.sum(p[p > eps] * np.log(p[p > eps]))

# ============ Define the three pipeline modes ============

def trail_T_only(p, depth=6):
    """Pure TSML iteration."""
    trail = [p.copy()]
    p_cur = p.copy()
    for _ in range(depth):
        p_cur = normalize_l1(fuse(p_cur, p_cur, table=T))
        trail.append(p_cur.copy())
    return trail

def trail_TB_alternating(p, depth=6):
    """Alternate T-fuse, B-fuse."""
    trail = [p.copy()]
    p_cur = p.copy()
    for d in range(depth):
        if d % 2 == 0:
            p_cur = normalize_l1(fuse(p_cur, p_cur, table=T))
        else:
            p_cur = normalize_l1(fuse(p_cur, p_cur, table=B))
        trail.append(p_cur.copy())
    return trail

def trail_T_then_B(p, depth=6):
    """T-fuse for half the depth, then B-fuse."""
    trail = [p.copy()]
    p_cur = p.copy()
    half = depth // 2
    for _ in range(half):
        p_cur = normalize_l1(fuse(p_cur, p_cur, table=T))
        trail.append(p_cur.copy())
    for _ in range(depth - half):
        p_cur = normalize_l1(fuse(p_cur, p_cur, table=B))
        trail.append(p_cur.copy())
    return trail

def trail_T_with_B_correction(p, depth=6):
    """After each T-fuse, mix in some B-fuse for diversification."""
    trail = [p.copy()]
    p_cur = p.copy()
    for _ in range(depth):
        p_t = normalize_l1(fuse(p_cur, p_cur, table=T))
        p_b = normalize_l1(fuse(p_cur, p_cur, table=B))
        p_cur = 0.5 * p_t + 0.5 * p_b
        p_cur = normalize_l1(p_cur)
        trail.append(p_cur.copy())
    return trail

def trail_T_cross_B(p, depth=6):
    """fuse(T, B): use mixed table T·B (a cross-fuse)."""
    trail = [p.copy()]
    p_cur = p.copy()
    for _ in range(depth):
        # cross-fuse: use TSML to compose, BHML to transform
        # r[c] = sum over a, b: T[a,b] = c, then B's transformation
        # Or: r[c] = sum over a,b such that B[T[a,b], q] = c -- complex
        # Simpler: alternating composition with both tables
        r = np.zeros(10)
        for a in range(10):
            for b in range(10):
                c_t = int(T[a, b])
                c_b = int(B[a, b])
                r[c_t] += 0.5 * p_cur[a] * p_cur[b]
                r[c_b] += 0.5 * p_cur[a] * p_cur[b]
        p_cur = normalize_l1(r)
        trail.append(p_cur.copy())
    return trail

# ============ Use diverse inputs ============

inputs = {}
np.random.seed(42)
for i in range(50):
    inputs[f'random_{i}'] = normalize_l1(np.random.dirichlet(np.ones(10)))
# Add structured inputs too
for i, name in enumerate(op_names):
    inputs[f'one-hot_{name}'] = np.eye(10)[i]
inputs['BEING'] = np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 0]) / 3
inputs['DOING'] = np.array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0]) / 3
inputs['BECOMING'] = np.array([0, 0, 0, 0, 0, 0, 0, 1, 1, 1]) / 3

# ============ Compare modes ============

modes = {
    'T-only':       trail_T_only,
    'TB-alternate': trail_TB_alternating,
    'T-then-B':     trail_T_then_B,
    'T+B-mix':      trail_T_with_B_correction,
    'T-cross-B':    trail_T_cross_B,
}

print("="*70)
print("PIPELINE MODE COMPARISON")
print("="*70)
print()

# For each mode, compute:
#   1. Mean entropy at each depth (high = info preserved)
#   2. Pairwise input distinguishability at each depth  
#   3. Where the fixed point lies

depths_to_check = [0, 1, 2, 3, 4, 6]

input_list = list(inputs.values())
input_names_list = list(inputs.keys())

# Compute trails for each mode
all_trails = {mode: [fn(p, depth=6) for p in input_list] 
              for mode, fn in modes.items()}

print(f"\n{'mode':<15} ", end='')
for d in depths_to_check:
    print(f"{f'd={d}':<10} ", end='')
print()
print("=" * 100)

print(f"\nMEAN ENTROPY at each depth (high = inputs spread, low = collapsed):")
for mode, trails in all_trails.items():
    print(f"  {mode:<13}", end='')
    for d in depths_to_check:
        H_mean = np.mean([entropy(t[d]) for t in trails])
        print(f" {H_mean:<10.4f}", end='')
    print()

print(f"\nMEAN PAIRWISE DISTINGUISHABILITY (JS div) at each depth:")
for mode, trails in all_trails.items():
    print(f"  {mode:<13}", end='')
    for d in depths_to_check:
        # Sample 50 pairs
        n_pairs = 0
        sum_js = 0
        for i in range(min(30, len(trails))):
            for j in range(i+1, min(30, len(trails))):
                sum_js += js_div(trails[i][d], trails[j][d])
                n_pairs += 1
        mean_js = sum_js / n_pairs if n_pairs > 0 else 0
        print(f" {mean_js:<10.4f}", end='')
    print()

# Where is the fixed point for each mode?
print(f"\nFIXED POINT (mean state at depth 6):")
for mode, trails in all_trails.items():
    final = np.mean([t[6] for t in trails], axis=0)
    top = np.argsort(-final)[:3]
    items = ", ".join(f"{op_names[i]}({final[i]:.2f})" for i in top if final[i] > 0.05)
    print(f"  {mode:<13} → {items}")

# ============ The information preservation question ============
print()
print("="*70)
print("INFORMATION PRESERVATION: which mode keeps inputs distinguishable longest?")
print("="*70)
print()

# Reconstruction test: from full trail at given depth, can we predict input?
from numpy.linalg import lstsq

n_train = 200
n_test = 100
np.random.seed(7)
train_inputs = [normalize_l1(np.random.dirichlet(np.ones(10))) for _ in range(n_train)]
np.random.seed(8)  
test_inputs_set = [normalize_l1(np.random.dirichlet(np.ones(10))) for _ in range(n_test)]

print(f"{'mode':<15} {'reconstruction error (lower = better preserved)':<30}")
for mode, fn in modes.items():
    train_trails = [fn(p, depth=4) for p in train_inputs]
    test_trails_data = [fn(p, depth=4) for p in test_inputs_set]
    
    # Use trail [p_1..p_4] to predict p_0
    X_train = np.array([np.concatenate(t[1:]) for t in train_trails])
    y_train = np.array(train_inputs)
    W, _, _, _ = lstsq(X_train, y_train, rcond=None)
    
    X_test = np.array([np.concatenate(t[1:]) for t in test_trails_data])
    y_test = np.array(test_inputs_set)
    y_pred = X_test @ W
    err = np.linalg.norm(y_pred - y_test, axis=1).mean()
    
    print(f"  {mode:<13} {err:<10.4f}")

baseline_err = np.linalg.norm(np.tile(np.mean(train_inputs, axis=0), (n_test, 1)) - 
                              np.array(test_inputs_set), axis=1).mean()
print(f"  baseline (no info): {baseline_err:.4f}")

print()
print("="*70)
print("STRUCTURED INPUT TRAIL COMPARISON ACROSS MODES")
print("="*70)
print()
print("How does each mode handle BEING vs DOING vs BECOMING?")

structured_test = {'BEING': inputs['BEING'], 'DOING': inputs['DOING'], 'BECOMING': inputs['BECOMING']}

for label, inp in structured_test.items():
    print(f"\n--- {label} ---")
    for mode, fn in modes.items():
        trail = fn(inp, depth=4)
        H_at_each = [entropy(p) for p in trail]
        # Top operator at depth 2
        top_at_2 = op_names[np.argmax(trail[2])]
        top_at_4 = op_names[np.argmax(trail[4])]
        H_str = " → ".join(f"{h:.2f}" for h in H_at_each)
        print(f"  {mode:<13} H: {H_str}    d=2:{top_at_2}, d=4:{top_at_4}")

print()
print("="*70)
print("WHAT BHML DOES")
print("="*70)
print("""
If T+B-mix or TB-alternate preserves MORE information at depth 3+ than 
T-only, BHML's role is anti-collapse: it prevents premature HARMONY 
attraction.

If T-then-B looks like a "phase transition" — T builds the trail, B then
diversifies — that suggests CK uses them sequentially, not simultaneously.

If T-cross-B (combined operator) is best, the natural processing fuses 
both at once.
""")
