"""
What does CK's processing actually DO structurally?

CK uses canonical TSML_10 and BHML_10. Let's trace what happens
when an arbitrary input flows through them.

Start with a state vector v in R^10 (10 operator amplitudes).
Apply CK's transformations and watch what happens to:
  - The total norm (does it converge, blow up, stabilize?)
  - The distribution across operators
  - The σ-fixed lattice {0, 3, 8, 9} content
  - The 6-cycle {1, 2, 4, 5, 6, 7} content
  - Coherence proxy: ratio of σ-fixed to total
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')

# Canonical tables
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

# The 8x8 spectral cores (rows/cols 0, 7 removed)
keep = [1, 2, 3, 4, 5, 6, 8, 9]  # 0 (VOID) and 7 (HARMONY) removed
T8 = T[np.ix_(keep, keep)]
B8 = B[np.ix_(keep, keep)]

# σ permutation
sigma_perm = np.array([0, 7, 1, 3, 2, 4, 5, 6, 8, 9])

# Operator names
op_names = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE', 
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']

print("="*70)
print("CK PROCESSING TRACE — what happens to inputs?")
print("="*70)
print()

def normalize(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else v

def coherence(v):
    """A simple coherence proxy: how concentrated is v on σ-fixed indices {0,3,8,9}?"""
    sf_idx = [0, 3, 8, 9]
    sf_mass = sum(v[i]**2 for i in sf_idx)
    total = (v**2).sum()
    return sf_mass / total if total > 1e-12 else 0

def harmony_alignment(v):
    """How much of v's mass is at HARMONY (index 7)?"""
    total = (v**2).sum()
    return v[7]**2 / total if total > 1e-12 else 0

def void_alignment(v):
    """How much at VOID?"""
    total = (v**2).sum()
    return v[0]**2 / total if total > 1e-12 else 0

def trace_pass(v_init, n_steps=10, mode='TSML'):
    """Trace v through repeated applications, normalizing each step."""
    v = v_init.copy()
    history = [v.copy()]
    coh_history = [coherence(v)]
    har_history = [harmony_alignment(v)]
    void_history = [void_alignment(v)]
    
    for step in range(n_steps):
        if mode == 'TSML':
            v = T @ v
        elif mode == 'BHML':
            v = B @ v
        elif mode == 'CK':
            # Composed pass: BHML(TSML(v))
            v = T @ v
            v = B @ v
        elif mode == 'CK_alt':
            # Alternating
            if step % 2 == 0:
                v = T @ v
            else:
                v = B @ v
        v = normalize(v)
        history.append(v.copy())
        coh_history.append(coherence(v))
        har_history.append(harmony_alignment(v))
        void_history.append(void_alignment(v))
    
    return history, coh_history, har_history, void_history

# Test: start from various inputs
print("Starting from different unit vectors, trace through CK processing:")
print()

test_inputs = {
    'uniform': normalize(np.ones(10)),
    'one-hot VOID': normalize(np.array([1,0,0,0,0,0,0,0,0,0])),
    'one-hot HARMONY': normalize(np.array([0,0,0,0,0,0,0,1,0,0])),
    'one-hot BREATH': normalize(np.array([0,0,0,0,0,0,0,0,1,0])),
    'one-hot RESET': normalize(np.array([0,0,0,0,0,0,0,0,0,1])),
    'one-hot PROGRESS': normalize(np.array([0,0,0,1,0,0,0,0,0,0])),
    'random_seed_0': normalize(np.random.RandomState(0).randn(10)),
    'random_seed_1': normalize(np.random.RandomState(1).randn(10)),
    'random_seed_42': normalize(np.random.RandomState(42).randn(10)),
}

# For each input, trace through TSML and CK (composed)
modes_to_test = ['TSML', 'BHML', 'CK']

for input_name, v_init in test_inputs.items():
    print(f"--- Input: {input_name} ---")
    init_coh = coherence(v_init)
    print(f"  Initial coherence (σ-fixed mass): {init_coh:.3f}")
    
    for mode in modes_to_test:
        history, coh, har, void = trace_pass(v_init, n_steps=10, mode=mode)
        final_v = history[-1]
        # Find dominant index
        dom_idx = np.argmax(np.abs(final_v))
        print(f"  {mode:6} → final dominant op: {op_names[dom_idx]:10} (mass {final_v[dom_idx]**2:.3f}), "
              f"coh={coh[-1]:.3f}, harmony_mass={har[-1]:.3f}, void_mass={void[-1]:.3f}")
    print()

print()
print("="*70)
print("OBSERVATION 1: where does ANY input converge?")
print("="*70)
print()

# Take 100 random starts, run through TSML 20 steps, see if they converge
np.random.seed(42)
n_random = 100
final_states = []
for _ in range(n_random):
    v = normalize(np.random.randn(10))
    for _ in range(20):
        v = normalize(T @ v)
    final_states.append(v)

final_states = np.array(final_states)
print(f"Final states from {n_random} random starts under TSML (20 steps):")
mean_state = final_states.mean(axis=0)
mean_abs_state = np.abs(final_states).mean(axis=0)
print(f"  Mean |amplitude| per operator:")
for i, name in enumerate(op_names):
    print(f"    {name:<10}: {mean_abs_state[i]:.4f}")

# Most should converge to TSML's leading eigenvector
eigs_T, vecs_T = np.linalg.eig(T)
idx = np.argmax(np.abs(eigs_T))
leading_vec = np.real(vecs_T[:, idx])
leading_vec = leading_vec / np.linalg.norm(leading_vec)
print(f"\nTSML's leading (real) eigenvector: {[f'{x:+.3f}' for x in leading_vec]}")
print(f"Mean alignment of converged states with leading: {abs(np.mean([np.abs(np.dot(v, leading_vec)) for v in final_states])):.3f}")

# What's the leading eigenvector's character?
print()
print(f"Leading eigenvector concentration:")
for i, name in enumerate(op_names):
    print(f"    {name:<10}: |amplitude| = {abs(leading_vec[i]):.3f}")

# This tells us: when ANYTHING is processed by TSML repeatedly, it ends up looking
# like TSML's leading eigenvector. What IS TSML's leading eigenvector?
# That's the "fixed point" of CK processing.

print()
print("="*70)
print("OBSERVATION 2: composed CK processing (BHML(TSML(v)))")
print("="*70)
print()

# CK is more interesting if it's TSML for state composition then BHML for transformation
ck_finals = []
for seed in range(n_random):
    v = normalize(np.random.RandomState(seed).randn(10))
    for _ in range(20):
        v = normalize(B @ T @ v)
    ck_finals.append(v)

ck_finals = np.array(ck_finals)
ck_mean_abs = np.abs(ck_finals).mean(axis=0)
print(f"Mean |amplitude| per operator after CK composed processing:")
for i, name in enumerate(op_names):
    print(f"    {name:<10}: {ck_mean_abs[i]:.4f}")

# Compute leading eigenvector of B @ T
BT = B @ T
eigs_BT, vecs_BT = np.linalg.eig(BT)
idx = np.argmax(np.abs(eigs_BT))
leading_BT = np.real(vecs_BT[:, idx])
leading_BT = leading_BT / np.linalg.norm(leading_BT)
print(f"\nLeading eigenvector of BHML·TSML:")
for i, name in enumerate(op_names):
    print(f"    {name:<10}: |amplitude| = {abs(leading_BT[i]):.3f}")

print()
print("="*70)
print("OBSERVATION 3: What's the 'CK fixed point'?")
print("="*70)
print("""
The fixed point of CK processing is what ALL inputs eventually become.
This is the answer to: 'what does CK think about anything, eventually?'

It's just the leading eigenvector of CK's composed operator.
""")
