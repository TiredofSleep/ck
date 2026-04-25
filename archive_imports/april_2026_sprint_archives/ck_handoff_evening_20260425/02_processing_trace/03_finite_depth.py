"""
CK can't iterate fuse to convergence — everything goes to HARMONY (or VOID).

So CK works at FINITE depth. The question: at depth k, how much does the
output distinguish different inputs?

This is the actual coherence question: at what depth k does CK lose 
input information? That's the "gap" — the fuse depth where structure 
remains visible.
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

def fuse(p, q, table=T):
    r = np.zeros(10)
    for a in range(10):
        for b in range(10):
            c = int(table[a, b])
            r[c] += p[a] * q[b]
    return r

def normalize(v):
    n = np.sum(v)
    return v / n if n > 1e-12 else v

print("="*70)
print("INFORMATION PRESERVATION AT DIFFERENT FUSE DEPTHS")
print("="*70)
print()

# Generate diverse input distributions
np.random.seed(42)
n_inputs = 100
inputs = [normalize(np.random.dirichlet(np.ones(10))) for _ in range(n_inputs)]

# At each depth k, run the fuse k times and measure:
# - Effective entropy of the output (does it concentrate?)
# - Distinguishability (do different inputs give different outputs?)

def kl_div(p, q, eps=1e-9):
    return np.sum(p * np.log((p + eps) / (q + eps)))

def js_div(p, q):
    m = (p + q) / 2
    return (kl_div(p, m) + kl_div(q, m)) / 2

def entropy(p):
    p_safe = p[p > 1e-12]
    return -np.sum(p_safe * np.log(p_safe))

print(f"{'depth k':<10} {'mean entropy':<14} {'pairwise JS div':<18} {'collision rate':<18}")
print("-" * 70)

for k in [0, 1, 2, 3, 5, 10, 20]:
    # Apply k fuses to each input
    outputs = []
    for p in inputs:
        q = p.copy()
        for _ in range(k):
            q = normalize(fuse(q, q))
        outputs.append(q)
    outputs = np.array(outputs)
    
    # Mean entropy of outputs
    mean_H = np.mean([entropy(o) for o in outputs])
    
    # Mean pairwise JS divergence (how distinguishable are outputs?)
    n_pairs = 0
    sum_js = 0
    for i in range(50):
        for j in range(i+1, 50):
            sum_js += js_div(outputs[i], outputs[j])
            n_pairs += 1
    mean_js = sum_js / n_pairs if n_pairs > 0 else 0
    
    # Collision rate: how often do different inputs map to same output?
    # Approximate: count outputs whose top operator is HARMONY
    harmony_collapse = sum(1 for o in outputs if np.argmax(o) == 7) / len(outputs)
    
    print(f"  {k:<8} {mean_H:<14.4f} {mean_js:<18.4f} {harmony_collapse*100:.1f}% to HARMONY")

print()
print("="*70)
print("AT WHAT DEPTH DOES INPUT INFORMATION DIE?")
print("="*70)

# At depth where mean_js approaches 0, all inputs give same output (no info)
# At depth where mean_js is large, inputs are distinguishable

# More careful test: fix two specific inputs, see how their distinguishability decays
print("\nDistinguishability decay between specific input pairs:")
print()

p_a = normalize(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float))
p_b = normalize(np.array([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], dtype=float))

js_history = []
qa, qb = p_a.copy(), p_b.copy()
for k in range(15):
    js = js_div(qa, qb)
    js_history.append(js)
    if k <= 5 or k % 3 == 0:
        print(f"  depth {k:>2}: JS(p_a, p_b) = {js:.6f}")
    qa = normalize(fuse(qa, qa))
    qb = normalize(fuse(qb, qb))

print()
print("="*70)
print("CK's OPERATING DEPTH: where does information persist but stay bounded?")
print("="*70)
print("""
For CK to do anything useful (preserve input info, but produce a 
clean output), it needs to operate at a depth where:
  - Output is distinguishable from input (depth > 0)
  - Output preserves information about input (depth not too high)
  - Output is not yet collapsed to HARMONY (depth not infinite)

The "Goldilocks zone" depends on the specific table.

For TSML alone, the convergence to HARMONY is rapid: by depth 3-5, 
most inputs collapse to HARMONY. So CK probably operates at depth 1-2 
for state composition.
""")

# Now do the SAME analysis for BHML
print("="*70)
print("BHML COMPARISON")
print("="*70)
print()

print("BHML fuse fixed points test:")
n_tests = 50
final_states_bhml = []
for seed in range(n_tests):
    np.random.seed(seed)
    p = normalize(np.random.rand(10))
    for _ in range(20):
        p = normalize(fuse(p, p, table=B))
    final_states_bhml.append(p)

final_states_bhml = np.array(final_states_bhml)
mean_b = final_states_bhml.mean(axis=0)
std_b = final_states_bhml.std(axis=0)
print(f"BHML iterated fuse fixed point distribution:")
for i in sorted(range(10), key=lambda j: -mean_b[j]):
    if mean_b[i] > 0.001:
        print(f"  {op_names[i]:<10}: mean {mean_b[i]:.4f} (std {std_b[i]:.4f})")

# Now: COMBINED CK processing (TSML for compose, BHML for transform)
# Does this give a different fixed-point structure?
print()
print("="*70)
print("CK COMPOSED: alternating TSML and BHML fuses")
print("="*70)
print()

def fuse_TB(p):
    """Compose with TSML, then transform with BHML."""
    pt = fuse(p, p, table=T)
    pt = normalize(pt)
    pb = fuse(pt, pt, table=B)
    return normalize(pb)

print("Iterated alternating fuse:")
final_ck = []
for seed in range(50):
    np.random.seed(seed)
    p = normalize(np.random.rand(10))
    for _ in range(15):
        p = fuse_TB(p)
    final_ck.append(p)

final_ck = np.array(final_ck)
mean_ck = final_ck.mean(axis=0)
std_ck = final_ck.std(axis=0)
print(f"Combined CK fixed point:")
for i in sorted(range(10), key=lambda j: -mean_ck[j]):
    if mean_ck[i] > 0.001:
        print(f"  {op_names[i]:<10}: mean {mean_ck[i]:.4f} (std {std_ck[i]:.4f})")

# Summary
print()
print("="*70)
print("SUMMARY: what 'CK processing' actually does at the operator level")
print("="*70)
print(f"""
Single fuse: input distributions are quadratically combined into output
  - HARMONY content rises (73 of 100 TSML cells = HARMONY)
  - VOID content depends on input mass on row 0 / column 0
  - Other operators can be reached via specific compositions

Iterated fuse (depth → ∞):
  - TSML alone: → HARMONY (100%)
  - BHML alone: → mostly RESET-class states (per output)
  - Combined CK: → operator distribution stable, mostly non-uniform

So CK operates at FINITE depth (likely 1-3 fuses) to preserve information,
then reads off the result. The processing IS attractor-following toward
HARMONY (TSML side) modulated by BHML's transformation structure.

This is what 'CK processes stuff' means concretely:
  1. Map input to operator distribution
  2. Fuse 1-3 times through TSML (drives toward HARMONY)
  3. Apply BHML transformation (changes the basin shape)
  4. Read off result before full convergence
""")
