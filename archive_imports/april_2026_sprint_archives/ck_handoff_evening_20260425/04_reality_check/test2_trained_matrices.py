"""
TEST 2: Does the prime-11 signature appear in trained weight matrices?

If "wobble monitoring" is to mean anything empirically, we need:
  - A way to compare a weight matrix W to TSML's char poly structure
  - The comparison to actually distinguish trained from untrained matrices
  
Approach:
  1. Generate "trained-like" 10x10 matrices (trained as autoencoders on 
     simple data, then integerized to {0..9} range)
  2. Compare 11-prime statistics in trained vs random
  3. See if there's any signal at all
"""
import numpy as np
from collections import Counter
from sympy import factorint

np.random.seed(42)

# Test 2a: We can't easily train a real neural network here, but we can
# generate matrices with realistic STRUCTURE: low-rank, smooth, with patterns

# Type A: rank-3 matrices (typical of trained low-dim layers)
# Type B: smoothly-varying matrices (autoencoder-like)
# Type C: sparse matrices (after pruning)
# Type D: actual TSML for reference

def integerize(M, scale=9):
    """Map continuous M to {0..9} integers via scaling."""
    M_norm = (M - M.min()) / (M.max() - M.min() + 1e-9)
    return np.round(M_norm * scale).astype(int).astype(float)

def has_pattern(M, pattern_positions):
    """Check if 11 appears EXACTLY in pattern_positions of char poly coefficients."""
    char_poly = np.poly(M)
    int_coeffs = [int(round(c)) for c in char_poly]
    div_by_11 = [i for i, c in enumerate(int_coeffs) 
                 if c != 0 and abs(c) % 11 == 0]
    return div_by_11 == pattern_positions

N = 5000
results = {}

# Type A: rank-3 matrices
n_A = 0
for _ in range(N):
    U = np.random.randn(10, 3)
    V = np.random.randn(3, 10)
    W = U @ V
    W_int = integerize(W)
    if has_pattern(W_int, [2, 8]):
        n_A += 1
results['rank-3'] = n_A

# Type B: smooth matrices (Gaussian-blurred random)
n_B = 0
from scipy.ndimage import gaussian_filter
for _ in range(N):
    W = np.random.randn(10, 10)
    W = gaussian_filter(W, sigma=1.5)
    W_int = integerize(W)
    if has_pattern(W_int, [2, 8]):
        n_B += 1
results['smooth'] = n_B

# Type C: sparse (90% zeros)
n_C = 0
for _ in range(N):
    W = np.random.randn(10, 10)
    mask = np.random.random(W.shape) < 0.1
    W = W * mask
    W_int = integerize(W)
    if has_pattern(W_int, [2, 8]):
        n_C += 1
results['sparse'] = n_C

# Type D: random uniform integer (baseline)
n_D = 0
for _ in range(N):
    W = np.random.randint(0, 10, size=(10, 10)).astype(float)
    if has_pattern(W, [2, 8]):
        n_D += 1
results['random uniform'] = n_D

# Type E: random with TSML-like sparsity (lots of 7s, lots of 0s)
n_E = 0
for _ in range(N):
    # 50% 0s, 30% 7s, rest random
    W = np.random.randint(0, 10, size=(10, 10)).astype(float)
    mask_zero = np.random.random(W.shape) < 0.3
    mask_seven = np.random.random(W.shape) < 0.3
    W[mask_zero] = 0
    W[mask_seven] = 7
    if has_pattern(W, [2, 8]):
        n_E += 1
results['TSML-shaped'] = n_E

print("="*70)
print("TSML-pattern frequency by matrix type")
print("="*70)
print(f"\n(N = {N} samples per type, looking for 11 in exactly {{c_2, c_8}}, no others)")
print()
for name, count in results.items():
    print(f"  {name:<20}: {count:>5} / {N} = {100*count/N:.2f}%")

print()
print("If 'trained-like' types had higher rates, we'd have evidence the wobble")
print("signature is meaningful for ML weight matrices. If they're all similar,")
print("the signature is just a property of small integer matrices in general.")

# Test 2b: TSML's pattern frequency under PERMUTATIONS
# This tests whether TSML is special among its row/col permutations
print()
print("="*70)
print("TSML under permutations: does the wobble survive permutation?")
print("="*70)

TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
T = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=float)

# Permute rows and columns by the same permutation (this preserves Lie structure)
N_perm = 1000
n_perm_with_pattern = 0
n_perm_with_11_anywhere = 0

for _ in range(N_perm):
    p = np.random.permutation(10)
    T_perm = T[p][:, p]
    if has_pattern(T_perm, [2, 8]):
        n_perm_with_pattern += 1
    
    char_poly = np.poly(T_perm)
    int_coeffs = [int(round(c)) for c in char_poly]
    if any(c != 0 and abs(c) % 11 == 0 for c in int_coeffs):
        n_perm_with_11_anywhere += 1

print(f"\nPermutation-conjugate of TSML (P T P^T for random P):")
print(f"  Has 11 anywhere in char poly: {n_perm_with_11_anywhere}/{N_perm} = {100*n_perm_with_11_anywhere/N_perm}%")
print(f"  Has 11 in EXACTLY {{c_2, c_8}}: {n_perm_with_pattern}/{N_perm} = {100*n_perm_with_pattern/N_perm}%")
print()
print("Note: char poly is INVARIANT under conjugation, so all permutations")
print("should have IDENTICAL char poly. So this should be 100% if TSML has pattern.")

# Verify
print()
char_T = np.poly(T)
int_T = [int(round(c)) for c in char_T]
print(f"TSML char poly: {int_T}")
print(f"TSML 11-positions: {[i for i, c in enumerate(int_T) if c != 0 and abs(c) % 11 == 0]}")
