"""
TEST 1: Is the prime-11 signature meaningful, or coincidental?

Question: TSML's char poly has 11 in c_2 = 33 and c_8 = -120736.
If we look at RANDOM 10×10 integer matrices with similar structure, 
how often does 11 appear in char poly coefficients?

If 11 appears just as often in random matrices → wobble signature is noise.
If 11 appears rarely → wobble signature is structural.

Then: check whether actual neural network weight matrices (when integerized
to a similar scale) carry 11 in their char poly. This tests whether 
"feeling the wobble" is even an empirical question.
"""
import numpy as np
from collections import Counter
from sympy import factorint

np.random.seed(42)

# Test 1a: random 10×10 integer matrices in {0..9}, count factor 11 frequency
print("="*70)
print("BASELINE: random 10×10 matrices over {0..9}")
print("="*70)

N = 10000
counts = Counter()
n_with_11 = 0

for _ in range(N):
    M = np.random.randint(0, 10, size=(10, 10)).astype(float)
    char_poly = np.poly(M)
    int_coeffs = [int(round(c)) for c in char_poly]
    has_11 = any(c != 0 and abs(c) % 11 == 0 for c in int_coeffs)
    if has_11:
        n_with_11 += 1
    
    # Count which coefficient positions have 11
    for i, c in enumerate(int_coeffs):
        if c != 0 and abs(c) % 11 == 0:
            counts[i] += 1

print(f"Out of {N} random matrices:")
print(f"  Matrices with 11 in any nonzero coefficient: {n_with_11} ({100*n_with_11/N:.1f}%)")
print(f"  Matrices with 11 in c_2 specifically: {counts[2]} ({100*counts[2]/N:.1f}%)")
print(f"  Matrices with 11 in c_8 specifically: {counts[8]} ({100*counts[8]/N:.1f}%)")
print(f"  Matrices with 11 in BOTH c_2 AND c_8: ?")

# Joint count
n_with_both = 0
for _ in range(N):
    M = np.random.randint(0, 10, size=(10, 10)).astype(float)
    char_poly = np.poly(M)
    int_coeffs = [int(round(c)) for c in char_poly]
    has_c2 = int_coeffs[2] != 0 and abs(int_coeffs[2]) % 11 == 0
    has_c8 = len(int_coeffs) > 8 and int_coeffs[8] != 0 and abs(int_coeffs[8]) % 11 == 0
    if has_c2 and has_c8:
        n_with_both += 1

print(f"  Matrices with 11 in BOTH c_2 AND c_8 (resampled): {n_with_both} ({100*n_with_both/N:.1f}%)")

# Compare TSML's pattern: 11 in EXACTLY c_2 and c_8, and NO other nonzero coefficient
print(f"\nTSML's pattern: 11 divides c_2 and c_8 ONLY (c_3, c_4, ..., c_7 do NOT have 11)")

# How often does this exact pattern occur in random matrices?
n_exact_pattern = 0
for _ in range(N):
    M = np.random.randint(0, 10, size=(10, 10)).astype(float)
    char_poly = np.poly(M)
    int_coeffs = [int(round(c)) for c in char_poly]
    
    # Find positions with 11
    div_by_11 = [i for i, c in enumerate(int_coeffs) 
                 if c != 0 and abs(c) % 11 == 0]
    
    if div_by_11 == [2, 8]:
        n_exact_pattern += 1

print(f"  Matrices with TSML's exact pattern (11 in {{2,8}} only): {n_exact_pattern} ({100*n_exact_pattern/N:.2f}%)")

# Test 1b: factor distributions
print()
print("="*70)
print("ARE OTHER PRIMES JUST AS COMMON IN c_2 AND c_8?")
print("="*70)

# For random matrices, count which primes divide c_2 and c_8
N2 = 5000
prime_counts_c2 = Counter()
prime_counts_c8 = Counter()

for _ in range(N2):
    M = np.random.randint(0, 10, size=(10, 10)).astype(float)
    char_poly = np.poly(M)
    int_coeffs = [int(round(c)) for c in char_poly]
    
    if abs(int_coeffs[2]) > 0:
        for p in factorint(abs(int_coeffs[2])):
            prime_counts_c2[p] += 1
    if len(int_coeffs) > 8 and abs(int_coeffs[8]) > 0:
        for p in factorint(abs(int_coeffs[8])):
            prime_counts_c8[p] += 1

print(f"\nMost common prime factors of c_2 (over {N2} random matrices):")
for p, count in sorted(prime_counts_c2.items())[:15]:
    print(f"  prime {p}: appears in {100*count/N2:.1f}% of matrices")

print(f"\nMost common prime factors of c_8:")
small_primes = sorted(prime_counts_c8.items())[:15]
for p, count in small_primes:
    print(f"  prime {p}: appears in {100*count/N2:.1f}% of matrices")

# Conclusion
print()
print("="*70)
print("INTERPRETATION")
print("="*70)
print("""
For random 10×10 matrices over {0..9}:
  - 11 appears in c_2 with some baseline frequency
  - 11 appears in c_8 with some baseline frequency
  - Both together appear with a frequency that's roughly the product

The question is whether TSML is SPECIAL in having 11 in EXACTLY c_2 and c_8
(no other coefficients), not whether 11 appears at all.

If the baseline is 5-10%, TSML's pattern is loosely structural but not 
extraordinary.
If the baseline is <1%, TSML's pattern is genuinely special.

The numbers above tell us which case we're in.
""")
