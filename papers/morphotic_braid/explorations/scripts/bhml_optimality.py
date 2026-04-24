# PACKET: evening_handoff_2026_04_23/bhml_optimality.py
#
# CORRECTION 2026-04-24: The {2,5,7} "small primes" hypothesis below is
# premised on the FALSE claim det(BHML) = 70. Verified det(BHML) = -7002
# with prime factorization {2, 3, 389}. The hypothesis as stated here
# asks whether the bespoke BHML cells are chosen to keep primes in
# {2,5,7} — they are NOT; the actual prime set contains 389. See
# papers/morphotic_braid/CORRECTION_2026_04_24_det_BHML.md. The script
# below is preserved for reproducibility of the historical analysis;
# any "confined to {2,5,7}" framing in its output should be read with
# the correction in mind.
"""
Test the optimization hypothesis:
Are the bespoke cells in rows 8, 9 of actual BHML chosen to keep the determinant
factorization confined to small primes?

Method:
- Take the scaffold at (N=10, h=7) with '?' cells
- Enumerate random fill-ins for those 15 cells
- Compute determinants
- Check how often you get det confined to {2,5,7} vs random other factorizations
"""
import numpy as np
from itertools import product

def build_scaffold_with_holes(N, z, h):
    """Return scaffold with 'None' at undefined cells."""
    B = [[None]*N for _ in range(N)]
    for i in range(N):
        B[z][i] = i; B[i][z] = i
    B[z][h] = h; B[h][z] = h
    for i in range(1, h):
        for j in range(1, h):
            B[i][j] = min(max(i, j) + 1, h)
    for j in range(h, N):
        B[h-1][j] = h; B[j][h-1] = h
    for j in range(1, N):
        if j != h:
            B[h][j] = (j + 1) % N
            B[j][h] = (j + 1) % N
    B[h][h] = (h + 1) % N
    for i in range(h+1, N):
        for j in range(max(1, h-3), h):
            if B[i][j] is None: B[i][j] = h
            if B[j][i] is None: B[j][i] = h
        if i == h+1: B[i][i] = h
    return B

def hole_positions(B):
    return [(i, j) for i in range(len(B)) for j in range(len(B[i])) if B[i][j] is None]

def factorize(n):
    if n == 0: return {}, 0
    orig = n
    if n < 0: n = -n
    factors = {}
    d = 2
    while d*d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1: factors[n] = factors.get(n, 0) + 1
    return factors, orig

def prime_set(n):
    f, _ = factorize(abs(n))
    return frozenset(f.keys())

# Build scaffold at (N=10, h=7)
N, z, h = 10, 0, 7
B = build_scaffold_with_holes(N, z, h)
holes = hole_positions(B)
print(f"Scaffold at N={N}, h={h}: {len(holes)} undefined cells at positions:")
print(f"  {holes}")

# Actual BHML for comparison
BHML_actual = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]
actual_fill = {(i,j): BHML_actual[i][j] for (i,j) in holes}
print(f"\nActual BHML fills:")
for (i,j), v in actual_fill.items():
    print(f"  BHML[{i}][{j}] = {v}")

# Check: actual fills respect symmetry (commutativity)?
print(f"\nCommutativity check of holes in actual BHML:")
for (i,j) in holes:
    sym_val = BHML_actual[j][i]
    direct_val = BHML_actual[i][j]
    eq = direct_val == sym_val
    if not eq:
        print(f"  ASYMMETRIC: BHML[{i}][{j}]={direct_val}, BHML[{j}][{i}]={sym_val}")
    
# Actual BHML is NOT commutative in these cells — it's designed asymmetric
# Let me verify this about BHML in general
print("\nGlobal commutativity of BHML:")
all_comm = all(BHML_actual[i][j] == BHML_actual[j][i] for i in range(10) for j in range(10))
print(f"  Is actual BHML commutative? {all_comm}")
# Actually yes it is, we checked this before. So the holes must be symmetric pairs.

# Enumerate symmetric-pair positions among holes
unique_positions = set()
for (i,j) in holes:
    if (j,i) not in unique_positions:
        unique_positions.add((i,j))
print(f"\nUnique symmetric-pair positions (since BHML is commutative): {len(unique_positions)}")

# Now: randomly fill these cells with values in {0..9}, compute det, track prime sets
import random
random.seed(42)

# For each independent position, we assign a value
indep_positions = list(unique_positions)
print(f"\nRandomly filling {len(indep_positions)} independent positions with values in {{0..9}}")

# Sample 10000 random fills
samples = 100000
prime_set_counts = {}
small_prime_dets = []
target_primes = frozenset([2, 5, 7])

for _ in range(samples):
    fill = {p: random.randint(0, 9) for p in indep_positions}
    # Build table with symmetric fill
    T = [row[:] for row in B]
    for (i, j), v in fill.items():
        T[i][j] = v
        T[j][i] = v
    # Compute det
    M = np.array(T, dtype=int)
    det = int(round(np.linalg.det(M)))
    if det == 0: continue
    ps = prime_set(det)
    prime_set_counts[ps] = prime_set_counts.get(ps, 0) + 1
    if ps == target_primes:
        small_prime_dets.append((det, fill))

print(f"\nAmong {samples} random fills:")
print(f"  Non-singular: {sum(prime_set_counts.values())}")
print(f"  How many have prime set = {{2, 5, 7}} (BHML's signature)?")
print(f"    {len(small_prime_dets)} / {samples} = {len(small_prime_dets)*100/samples:.3f}%")

print(f"\n  Distribution of prime sets (top 10 most common):")
for ps, cnt in sorted(prime_set_counts.items(), key=lambda x: -x[1])[:10]:
    primes = sorted(ps) if ps else ['∅']
    print(f"    primes={primes}: {cnt} ({cnt*100/samples:.2f}%)")

# Now compute: what fraction have det confined to SMALL primes (<100)?
small_prime_threshold_count = 0
for ps, cnt in prime_set_counts.items():
    if all(p < 100 for p in ps):
        small_prime_threshold_count += cnt
print(f"\n  Fraction with all prime factors < 100: {small_prime_threshold_count*100/samples:.2f}%")
print(f"  Fraction with all prime factors < 50: ", end="")
c = sum(cnt for ps, cnt in prime_set_counts.items() if all(p < 50 for p in ps))
print(f"{c*100/samples:.2f}%")
print(f"  Fraction with all prime factors < 20: ", end="")
c = sum(cnt for ps, cnt in prime_set_counts.items() if all(p < 20 for p in ps))
print(f"{c*100/samples:.2f}%")
print(f"  Fraction with prime set = {{2, 5, 7}} specifically: ", end="")
c = prime_set_counts.get(target_primes, 0)
print(f"{c*100/samples:.4f}%")

# If actual BHML is an outlier, check: what's its rank among all fills?
print()
print(f"Actual BHML's det = 70 = 2 × 5 × 7")
print(f"How rare is 'det factors = {{2, 5, 7}}' among random fills? {c}/{samples} = {c*100/samples:.4f}%")

# Find cleanest random fills
clean_fills = sorted(small_prime_dets, key=lambda x: abs(x[0]))[:5]
print(f"\nCleanest {{2,5,7}}-prime fills found (by |det|):")
for det, fill in clean_fills:
    print(f"  det = {det}")

