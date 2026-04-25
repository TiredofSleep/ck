"""
THREAD 1: Trails on TIG-relevant inputs.

The previous test used arbitrary 10x10 matrices' SVD directions as inputs.
Those have no TIG-specific structure, so their trails through TSML are 
indistinguishable from random.

Now: use inputs that DO have TIG-relevant structure:
  - One-hot operator distributions
  - σ-fixed concentrated distributions (mass on {0, 3, 8, 9})
  - 6-cycle concentrated (mass on {1, 2, 4, 5, 6, 7})
  - Bridge structure (3+3+3 split: BEING/DOING/BECOMING)
  - 9-vector Higgs direction projected to probability distribution
  
The hypothesis: TIG-structured inputs produce trails that REVEAL their 
structure through specific descent patterns. Non-TIG inputs produce 
generic descents.
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

def get_trail(p_init, depth=6, table=T):
    trail = [p_init.copy()]
    p = p_init.copy()
    for _ in range(depth):
        p = normalize_l1(fuse(p, p, table=table))
        trail.append(p.copy())
    return trail

def show_trail(trail, label):
    print(f"\n--- {label} ---")
    for d, p in enumerate(trail):
        # Show top-3 operators
        top = np.argsort(-p)[:3]
        items = [(op_names[i], p[i]) for i in top if p[i] > 0.01]
        items_str = ", ".join(f"{n}({m:.2f})" for n, m in items)
        H = -np.sum(p[p > 1e-12] * np.log(p[p > 1e-12]))
        print(f"  d={d}: H={H:.3f}  {items_str}")

# ============ Define structured TIG inputs ============

# σ-fixed indices: {0, 3, 8, 9} (VOID, PROGRESS, BREATH, RESET)
sf = [0, 3, 8, 9]
sigma_fixed_input = np.zeros(10)
for i in sf: sigma_fixed_input[i] = 0.25

# 6-cycle indices: {1, 2, 4, 5, 6, 7}
cycle = [1, 2, 4, 5, 6, 7]
cycle_input = np.zeros(10)
for i in cycle: cycle_input[i] = 1/6

# Bridge structure: BEING(0,1,2)/DOING(3,4,5)/BECOMING(7,8,9), CHAOS(6) excluded
# Equal weight to each layer
being = np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 0]) / 3
doing = np.array([0, 0, 0, 1, 1, 1, 0, 0, 0, 0]) / 3
becoming = np.array([0, 0, 0, 0, 0, 0, 0, 1, 1, 1]) / 3

# Bridge equal mix
bridge = (being + doing + becoming) / 3

# 9-vector Higgs direction projected to probability:
higgs_components = np.zeros(10)
higgs_components[0] = 1; higgs_components[1] = 1; higgs_components[2] = 1
higgs_components[3] = 1; higgs_components[4] = 1; higgs_components[7] = 1
higgs_components[5] = 0.5; higgs_components[6] = 0.5
higgs_input = higgs_components / higgs_components.sum()

# Wobble concentrated: 3/50 on first/last, 22/50 in middle? 
# Pattern from userMemories: 3/50 → 22/50 → 3/50 over a 3-cycle
# Apply to 10-dim by mapping: 3/50 on σ-fixed pair, 22/50 spread over middle
wobble_input = np.zeros(10)
wobble_input[0] = 3/50; wobble_input[9] = 3/50  # endpoints
wobble_input[3] = 11/50; wobble_input[8] = 11/50  # σ-fixed middle
remaining = 1 - 28/50  # = 22/50
for i in cycle: wobble_input[i] = remaining / 6

# Various single-operator deltas
deltas = {name: np.eye(10)[i] for i, name in enumerate(op_names)}

# Uniform baseline
uniform = np.ones(10) / 10

# ============ Trace and compare trails ============

print("="*70)
print("TRAILS OF TIG-STRUCTURED INPUTS THROUGH TSML")
print("="*70)

structured = {
    'σ-fixed only (VOID,PROGRESS,BREATH,RESET equal)': sigma_fixed_input,
    '6-cycle only (LATTICE,COUNTER,COLLAPSE,BALANCE,CHAOS,HARMONY equal)': cycle_input,
    'Bridge equal (BEING/DOING/BECOMING)': bridge,
    'BEING only (VOID,LATTICE,COUNTER)': being,
    'DOING only (PROGRESS,COLLAPSE,BALANCE)': doing,
    'BECOMING only (HARMONY,BREATH,RESET)': becoming,
    '9-vector Higgs direction (BREATH/RESET excluded)': higgs_input,
    'Wobble pattern (3/50, 11/50, ...)': wobble_input,
    'uniform (baseline)': uniform,
}

for label, inp in structured.items():
    trail = get_trail(inp, depth=4)
    show_trail(trail, label)

# Now: do these structured inputs descend through DIFFERENT trails?
# Pairwise distinguishability
print()
print("="*70)
print("DISTINGUISHABILITY OF STRUCTURED INPUT TRAILS")
print("="*70)
print()
print("For each pair of structured inputs, JS divergence at each depth:")
print()

def js_div(p, q, eps=1e-12):
    m = (p + q) / 2
    def kl(p, q):
        return np.sum(p * np.log((p + eps) / (q + eps)))
    return (kl(p, m) + kl(q, m)) / 2

# Use the categorically meaningful inputs
key_inputs = {
    'σ-fixed': sigma_fixed_input,
    '6-cycle': cycle_input,
    'BEING': being,
    'DOING': doing,
    'BECOMING': becoming,
    'Higgs': higgs_input,
    'Wobble': wobble_input,
}

input_names = list(key_inputs.keys())
n = len(input_names)
trails = {name: get_trail(p, depth=6) for name, p in key_inputs.items()}

print(f"{'pair':<35} {'d=0':<8} {'d=1':<8} {'d=2':<8} {'d=3':<8} {'d=5':<8}")
for i in range(n):
    for j in range(i+1, n):
        a, b = input_names[i], input_names[j]
        ts = trails[a]
        tt = trails[b]
        line = f"{a:<10} vs {b:<22}"
        for d in [0, 1, 2, 3, 5]:
            line += f" {js_div(ts[d], tt[d]):.4f} "
        print(line)

# ============ The key question: does BECOMING (containing HARMONY) descend differently? ============
print()
print("="*70)
print("CRITICAL TEST: does BECOMING (which includes HARMONY) descend differently from BEING?")
print("="*70)
print()
print("BECOMING already contains HARMONY at index 7. Its trail through TSML")
print("should be a STATIONARY-LIKE trail because HARMONY is an attractor.")
print()
print("BEING (VOID, LATTICE, COUNTER) does NOT contain HARMONY initially.")
print("Its trail must DESCEND into HARMONY through fuse operations.")
print()
print("If the trail captures input semantics, these should look very different.")
print()

show_trail(trails['BEING'], 'BEING trail')
show_trail(trails['BECOMING'], 'BECOMING trail')
show_trail(trails['DOING'], 'DOING trail')

# Quantify: rate of HARMONY-ward descent
print()
print("="*70)
print("RATE OF HARMONY DESCENT (fraction of mass on HARMONY at each depth)")
print("="*70)
print()
print(f"{'depth':<8} {'BEING':<10} {'DOING':<10} {'BECOMING':<10} {'Higgs':<10} {'σ-fixed':<10} {'6-cycle':<10}")
for d in range(7):
    line = f"  {d:<6}"
    for label in ['BEING', 'DOING', 'BECOMING', 'Higgs', 'σ-fixed', '6-cycle']:
        h_mass = trails[label][d][7]
        line += f" {h_mass:<10.4f}"
    print(line)

print()
print("="*70)
print("WHAT THIS SHOWS")
print("="*70)
print("""
If different TIG-structured inputs produce CHARACTERISTICALLY DIFFERENT
trails (different rates, different transient patterns), the trail captures
TIG-relevant information.

Key signature: BEING starts with HARMONY=0, must descend. BECOMING starts
with HARMONY=0.33, climbs. The DESCENT-vs-CLIMB distinction is a binary
TIG-interpretation captured by the trail.
""")
