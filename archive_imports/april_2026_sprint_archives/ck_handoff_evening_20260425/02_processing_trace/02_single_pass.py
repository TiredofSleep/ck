"""
What CK actually does at runtime is NOT iterate to convergence.
It does a small number of fuse operations on operator amplitudes.

Let's look at one pass: v → T @ v (one composition), then maybe through BHML once.

The interesting question: what's PRESERVED about the input vs what's CHANGED?

Specifically:
  - Distance metric: how much does v change after one pass?
  - Information: how much can you reconstruct v from T @ v?
  - Selective amplification: which input directions get amplified, which suppressed?
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

print("="*70)
print("SINGLE-PASS CK PROCESSING")
print("="*70)
print()

# What does T @ e_i look like for each unit basis vector?
print("T @ e_i for each operator (first column = VOID is special):")
print()
print(f"{'Input':<10} → {'T @ e_input (which operators get mass)':<60}")
for i in range(10):
    e_i = np.zeros(10)
    e_i[i] = 1.0
    Tv = T @ e_i
    # Show top 3 nonzero outputs
    indices = np.argsort(-np.abs(Tv))[:3]
    output_str = ", ".join(f"{op_names[j]}({Tv[j]:.1f})" for j in indices if abs(Tv[j]) > 0.01)
    if not output_str:
        output_str = "<all zero>"
    print(f"{op_names[i]:<10} → {output_str}")

print()
print("Note: T @ e_i = column i of T = the row 'i' of TSML composition table")
print("So T @ e_VOID = column 0 of T, which is column 0 of the table = all zeros")
print("(except T[7,0] = 7 from the third row, etc.)")
print()

# Wait — actually I need to reread. T @ e_i picks out column i of T.
# Column i of T is [T[0,i], T[1,i], ..., T[9,i]]
# This is the vector of values T[k][i] for k = 0..9
# That's "what each operator does TO operator i"
print("Actually: T @ e_i gives column i of T = 'how each operator sees operator i in the composition table'")
print()

# Let's understand what TSML's column structure actually is
print("Column 0 (e_VOID column) of T:")
for k in range(10):
    if T[k, 0] != 0:
        print(f"  T[{op_names[k]}, VOID] = {int(T[k,0])} = {op_names[int(T[k,0])]}")

print()
print("Column 7 (e_HARMONY column) of T:")
for k in range(10):
    if T[k, 7] != 0:
        print(f"  T[{op_names[k]}, HARMONY] = {int(T[k,7])} = {op_names[int(T[k,7])]}")

# Now: what about ROW i of T applied to v? That's T_row · v = sum over j of T[i,j] * v[j]
# This is "what operator i sees when fusing with v"
# 
# Actually, the NATURAL CK operation isn't matrix-vector multiplication on the
# composition table at all! It's: given two operators a, b, output T[a,b].
# That's looking up the table cell, not doing matrix multiplication.

print()
print("="*70)
print("CK'S NATURAL OPERATION: TABLE LOOKUP, NOT MATRIX MULT")
print("="*70)
print("""
The TSML table T[a, b] = c means: composing operator a with operator b
gives operator c. This is NOT a matrix transformation of vectors; it's a
binary operation on indices.

If CK has a "state" represented as a probability distribution over 
operators (a 10-vector p with sum 1), then composing state p with state q
should give a NEW distribution over operators where:
  
  P(c | a, b) is determined by T[a, b]
  
The composed distribution is:
  
  r[c] = Σ_{a,b: T[a,b] = c} p[a] q[b]

That's a quadratic operation on (p, q), not linear. Let me trace this.
""")

def fuse(p, q, table=T):
    """Quadratic composition: given state distributions p and q, produce r."""
    r = np.zeros(10)
    for a in range(10):
        for b in range(10):
            c = int(table[a, b])
            r[c] += p[a] * q[b]
    return r

# Test single fuse operations
print("Single fuse operations p ⊕_TSML q:")
print()

def normalize(v):
    n = np.sum(v)  # L1 normalize since these are probabilities
    return v / n if n > 1e-12 else v

# Fuse uniform with itself
p_uniform = np.ones(10) / 10
print(f"uniform ⊕ uniform:")
r = fuse(p_uniform, p_uniform)
print(f"  result distribution:")
for i in sorted(range(10), key=lambda j: -r[j]):
    if r[i] > 0.001:
        print(f"    {op_names[i]:<10}: {r[i]:.4f}")

# Fuse VOID with anything
print()
print(f"VOID (delta) ⊕ uniform:")
p_void = np.zeros(10); p_void[0] = 1.0
r = fuse(p_void, p_uniform)
print(f"  result:")
for i in sorted(range(10), key=lambda j: -r[j]):
    if r[i] > 0.001:
        print(f"    {op_names[i]:<10}: {r[i]:.4f}")

# Fuse HARMONY with itself
print()
print(f"HARMONY ⊕ HARMONY:")
p_h = np.zeros(10); p_h[7] = 1.0
r = fuse(p_h, p_h)
for i in sorted(range(10), key=lambda j: -r[j]):
    if r[i] > 0.001:
        print(f"    {op_names[i]:<10}: {r[i]:.4f}")

print(f"\nT[HARMONY, HARMONY] = {int(T[7,7])} = {op_names[int(T[7,7])]} ← exact lookup")

# Now the interesting question: ITERATING fuse(p, p)
print()
print("="*70)
print("ITERATED FUSE: p_{n+1} = fuse(p_n, p_n) — what's the fixed point?")
print("="*70)

def trace_fuse(p_init, n_steps=15, table=T):
    history = [p_init.copy()]
    p = p_init.copy()
    for _ in range(n_steps):
        p = fuse(p, p, table=table)
        p = normalize(p)
        history.append(p.copy())
    return history

# Start from various distributions
print("\nIterated fuse with TSML, starting from uniform:")
hist = trace_fuse(p_uniform, n_steps=12)
print(f"Final distribution:")
final = hist[-1]
for i in sorted(range(10), key=lambda j: -final[j]):
    if final[i] > 0.001:
        print(f"    {op_names[i]:<10}: {final[i]:.4f}")

print("\nIterated fuse with TSML, starting from VOID:")
hist = trace_fuse(p_void, n_steps=12)
final = hist[-1]
for i in sorted(range(10), key=lambda j: -final[j]):
    if final[i] > 0.001:
        print(f"    {op_names[i]:<10}: {final[i]:.4f}")

print("\nIterated fuse with TSML, starting from HARMONY:")
hist = trace_fuse(p_h, n_steps=12)
final = hist[-1]
for i in sorted(range(10), key=lambda j: -final[j]):
    if final[i] > 0.001:
        print(f"    {op_names[i]:<10}: {final[i]:.4f}")

print("\nIterated fuse with TSML, starting from random:")
np.random.seed(42)
p_rand = normalize(np.random.rand(10))
hist = trace_fuse(p_rand, n_steps=12)
final = hist[-1]
for i in sorted(range(10), key=lambda j: -final[j]):
    if final[i] > 0.001:
        print(f"    {op_names[i]:<10}: {final[i]:.4f}")

# Convergence depends on starting state — does it have multiple fixed points?
print()
print("="*70)
print("DOES TSML's FUSE HAVE MULTIPLE FIXED POINTS?")
print("="*70)

n_tests = 50
final_states = []
for seed in range(n_tests):
    np.random.seed(seed)
    p = normalize(np.random.rand(10))
    for _ in range(20):
        p = normalize(fuse(p, p))
    final_states.append(p)

# Check for distinct final states
final_states = np.array(final_states)
print(f"\nFrom {n_tests} random initial distributions:")
print(f"Final distributions converged. Looking at variance per operator:")

mean_final = final_states.mean(axis=0)
std_final = final_states.std(axis=0)
print(f"\n{'Operator':<10} {'mean':<8} {'std':<8}")
for i in range(10):
    print(f"  {op_names[i]:<10} {mean_final[i]:<8.4f} {std_final[i]:<8.4f}")

# If std is uniformly small, there's one fixed point
# If std is larger, there are multiple basins of attraction
total_std = std_final.sum()
print(f"\nTotal variance: {total_std:.4f}")
if total_std < 0.05:
    print("→ Single fixed point: all random inputs converge to same distribution")
elif total_std < 0.2:
    print("→ Mostly one fixed point with small variations")
else:
    print("→ Multiple basins of attraction!")

# Show final distribution
print(f"\nMean fixed-point distribution:")
for i in sorted(range(10), key=lambda j: -mean_final[j]):
    if mean_final[i] > 0.001:
        print(f"  {op_names[i]:<10}: {mean_final[i]:.4f}")
