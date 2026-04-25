"""
Cycle through tower levels properly.

Two distinct operations to check at each level:

  (a) BRACKET-IMAGE: span of {[X, Y] : X, Y in input set}
      = single application of the Lie bracket
      = produces antisymmetric matrices regardless of input
      = the "Lie-content extracted via one bracket"
      
  (b) BRACKET-CLOSURE: smallest subspace containing input AND closed under bracket
      = iterative; can include the inputs themselves
      = if inputs aren't antisymmetric, this isn't a Lie subalgebra; it's the
        smallest subspace (under bracket) containing them
        
For Lie subalgebra generation, we use (a) when the inputs are arbitrary
(possibly symmetric), and (b) when the inputs are antisymmetric.
        
The KEY question: at each tower level, working from the +1 side and the -1
side separately, what's the bracket-image dimension?
"""
import numpy as np

TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
T = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=int)

BHML_ROWS = [
    "0123456789",  "1234567266",  "2334567366",  "3444567466",  "4555567577",
    "5666667677",  "6777777777",  "7234567890",  "8666777978",  "9666777080",
]
B = np.array([[int(c) for c in row] for row in BHML_ROWS], dtype=int)

P56 = np.eye(10)
P56[5,5] = 0; P56[6,6] = 0; P56[5,6] = 1; P56[6,5] = 1

sigma = np.array([0, 7, 1, 3, 2, 4, 5, 6, 8, 9])
P_sigma = np.zeros((10, 10))
for i in range(10):
    P_sigma[sigma[i], i] = 1.0

sigma3 = np.linalg.matrix_power(P_sigma, 3)

def left_reps(table):
    n = table.shape[0]
    return [np.array([[1.0 if table[i,j]==k else 0.0 for j in range(n)] for k in range(n)]) for i in range(n)]

def bracket_image(generators):
    """Span of [X, Y] for all X, Y in generators. One round of brackets."""
    images = []
    n = len(generators)
    for i in range(n):
        for j in range(i+1, n):
            C = generators[i] @ generators[j] - generators[j] @ generators[i]
            if np.linalg.norm(C) > 1e-9:
                images.append(C.flatten())
    if not images:
        return 0
    M = np.array(images).T
    U, S, _ = np.linalg.svd(M, full_matrices=False)
    return int(np.sum(S > 1e-9 * S[0]))

def linear_span(generators):
    """Just the linear span dim."""
    if not generators:
        return 0
    flat = np.array([g.flatten() for g in generators if np.linalg.norm(g) > 1e-9]).T
    if flat.size == 0:
        return 0
    U, S, _ = np.linalg.svd(flat, full_matrices=False)
    return int(np.sum(S > 1e-9 * S[0]))

def lie_closure_dim(generators, max_iters=12):
    """Iterative bracket closure dim."""
    if not generators:
        return 0
    shape = generators[0].shape
    bv = [g.flatten() for g in generators if np.linalg.norm(g) > 1e-9]
    if not bv:
        return 0
    M = np.array(bv).T
    U, S, _ = np.linalg.svd(M, full_matrices=False)
    rank = int(np.sum(S > 1e-9 * S[0]))
    bv = [U[:, i] for i in range(rank)]
    for _ in range(max_iters):
        N = len(bv)
        mats = [v.reshape(shape) for v in bv]
        new = []
        for i in range(N):
            for j in range(i+1, N):
                C = mats[i] @ mats[j] - mats[j] @ mats[i]
                v = C.flatten()
                if np.linalg.norm(v) > 1e-9:
                    new.append(v)
        all_v = bv + new
        M = np.array(all_v).T
        U, S, _ = np.linalg.svd(M, full_matrices=False)
        new_rank = int(np.sum(S > 1e-9 * S[0]))
        if new_rank == len(bv):
            break
        bv = [U[:, i] for i in range(new_rank)]
    return len(bv)

EPS = 1e-9
L_T = left_reps(T)
L_B = left_reps(B)
all_L = L_T + L_B
labels = [f"T{i}" for i in range(10)] + [f"B{i}" for i in range(10)]

# Three involutions
involutions = [
    ('τ_1 transposition', lambda M: M.T),
    ('τ_2 P_56 conjugation', lambda M: P56 @ M @ P56.T),
    ('τ_3 σ³ conjugation', lambda M: sigma3 @ M @ sigma3.T),
]

results = []

for name, tau in involutions:
    plus_parts = [(L + tau(L)) / 2 for L in all_L]
    minus_parts = [(L - tau(L)) / 2 for L in all_L]
    
    pure_plus = sum(1 for i in range(20) if np.linalg.norm(minus_parts[i]) < EPS)
    pure_minus = sum(1 for i in range(20) if np.linalg.norm(plus_parts[i]) < EPS)
    crossings = sum(1 for i in range(20)
                   if np.linalg.norm(plus_parts[i]) > EPS
                   and np.linalg.norm(minus_parts[i]) > EPS)
    
    plus_span = linear_span(plus_parts)
    minus_span = linear_span(minus_parts)
    
    plus_image = bracket_image(plus_parts)
    minus_image = bracket_image(minus_parts)
    
    # Count active (nonzero) generators on each side
    n_plus_active = sum(1 for p in plus_parts if np.linalg.norm(p) > EPS)
    n_minus_active = sum(1 for p in minus_parts if np.linalg.norm(p) > EPS)
    
    results.append({
        'name': name,
        'pure_plus': pure_plus,
        'pure_minus': pure_minus,
        'crossings': crossings,
        'n_plus_active': n_plus_active,
        'n_minus_active': n_minus_active,
        'plus_span': plus_span,
        'minus_span': minus_span,
        'plus_image': plus_image,
        'minus_image': minus_image,
    })

# Display
print("="*94)
print("UNIFIED TOWER TABLE — bracket-image dimensions both sides of the coin")
print("="*94)
print()
print(f"{'level':<22} {'+pure':<6} {'-pure':<6} {'crs':<5} "
      f"{'#+act':<6} {'#-act':<6} {'+span':<6} {'-span':<6} "
      f"{'+brkim':<7} {'-brkim':<7}")
print("-"*94)

for r in results:
    print(f"{r['name']:<22} "
          f"{r['pure_plus']:<6} "
          f"{r['pure_minus']:<6} "
          f"{r['crossings']:<5} "
          f"{r['n_plus_active']:<6} "
          f"{r['n_minus_active']:<6} "
          f"{r['plus_span']:<6} "
          f"{r['minus_span']:<6} "
          f"{r['plus_image']:<7} "
          f"{r['minus_image']:<7}")

print()
print("Legend:")
print("  +pure: number of L_i lying entirely in +1 eigenspace (pure on +side)")
print("  -pure: number of L_i lying entirely in -1 eigenspace (pure on -side)")
print("  crs: crossings (L_i with both parts nonzero)")
print("  #±act: number of nonzero ± parts among 20 L_i")
print("  ±span: linear span dim of ± parts")
print("  ±brkim: bracket-image dim (one round of [X,Y] for X,Y in ± side)")

print()
print("="*94)
print("THE PATTERN")
print("="*94)
print("""
Reading the table:

τ_1 (Lie/Jordan):
  +Jordan side has 1 pure-sym generator (B0 = identity row)
  -Lie side has 0 pure (every generator has a sym part)
  19 crossings: every other L_i has both parts
  +brkim = 45: Jordan side commutators span all of so(10)
  -brkim = 45: Lie side commutators ALSO span all of so(10)
  → BOTH sides regenerate so(10) via single round of brackets

τ_2 (Clifford/Permutation):
  +Clifford (P_56-fixed) side has 11 pure-fixed generators
    (10 TSML + B0, since they all commute with P_56)
  -Permutation (P_56-broken) side has 0 pure
  9 crossings: only the 9 BHML rows that break P_56 are crossings
  +brkim = ?: how many dims do the P_56-fixed parts generate?
  -brkim = ?: how many dims do the P_56-broken parts generate?

τ_3 (σ³):
  +σ³-fixed side has 1 pure (just B0)
  -σ³-broken side has 0 pure
  19 crossings (same pattern as τ_1!)

Now THE TWIST:

L_B[0] = identity row [0,1,...,9] is the ONE generator pure under
  τ_1 (it's symmetric)
  τ_3 (σ³ fixes it because it's the identity)
  And under τ_2 it's also pure (commutes with P_56 since it's diag-numbering)

So L_B[0] is the UNIVERSAL "label" generator — pure under EVERY involution.
It's the only generator that's left fixed by every coin-flip.
""")
