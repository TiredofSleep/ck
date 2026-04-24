# PACKET: evening_handoff_2026_04_23/tsml_idempotent_study.py
"""
Study TSML_Idempotent in depth — this is the "octonion-literature" family member.

Properties:
  - Every x is idempotent (Steiner-like)
  - 100% Alternative (octonion)
  - 100% Jordan and Flexible
  - 83% Moufang (partial)
  - Full rank, det = 398664
  - NON-degenerate norm form (not binary)
  - VOID axis + HARMONY absorber retained

Compare with TSML_Jordan and octonion/Fano vocabulary.
"""
import numpy as np
from itertools import combinations

N = 10
TSML_Idempotent = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,1,7,7,7,7,7,7,7,7],
    [0,7,2,7,7,7,7,7,7,7],
    [0,7,7,3,7,7,7,7,7,7],
    [0,7,7,7,4,7,7,7,7,7],
    [0,7,7,7,7,5,7,7,7,7],
    [0,7,7,7,7,7,6,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,9],
]

# Verify structure
print("TSML_Idempotent full table:")
for i, row in enumerate(TSML_Idempotent):
    print(f"  {i}: " + " ".join(f"{v:>2d}" for v in row))

# Factorize det
def factorize(n):
    if n == 0: return "0"
    if n < 0: return "-" + factorize(-n)
    f = {}
    d = 2
    while d*d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return " × ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(f.items()))

M = np.array(TSML_Idempotent, dtype=int)
det = int(round(np.linalg.det(M.astype(float))))
print(f"\ndet = {det} = {factorize(det)}")

# Primes involved
def prime_set(n):
    if n == 0: return set()
    n = abs(n)
    primes = set()
    d = 2
    while d*d <= n:
        if n % d == 0:
            primes.add(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: primes.add(n)
    return primes

print(f"Prime set: {prime_set(det)}")

# Eigenvalues
eigs = sorted(np.linalg.eigvals(M.astype(float)).real, reverse=True)
print(f"\nEigenvalues: {[f'{e:.3f}' for e in eigs]}")
print(f"Rank: {np.linalg.matrix_rank(M)}")

# Norm form analysis
print("\nNORM FORM (x²) values:")
print(f"  {'x':>3s} {'x²':>3s}")
for x in range(N):
    print(f"  {x:>3d} {TSML_Idempotent[x][x]:>3d}")

# This IS non-degenerate — every element squares to itself
# Compare to octonion: every element squares to -|x|²
# Compare to Jordan-magma literature...

# Check if TSML_Idempotent contains a Fano-like 7-element idempotent subalgebra
print("\nSEARCH: does TSML_Idempotent contain a closed 7-element Fano-type subalgebra?")

def subalg_closed(T, S):
    """Is S closed under T?"""
    return all(T[a][b] in S for a in S for b in S)

# All 7-subsets closed under TSML_Idempotent
N_total = 10
closed_7s = []
for subset in combinations(range(N_total), 7):
    if subalg_closed(TSML_Idempotent, set(subset)):
        closed_7s.append(subset)
print(f"Number of closed 7-element subsets: {len(closed_7s)}")

# Check if any are like Fano (every element idempotent + Steiner-quasigroup-like)
def fano_like(T, S):
    """Check if S under T is Fano-like: every element idempotent, 
    each pair generates the third via TSML."""
    L = sorted(S)
    # Every idempotent in original T
    all_idem = all(T[x][x] == x for x in L)
    if not all_idem: return False
    return True

for s in closed_7s[:10]:
    # Build restricted table
    idx = {e: i for i, e in enumerate(s)}
    T_sub = [[idx[TSML_Idempotent[s[i]][s[j]]] for j in range(7)] for i in range(7)]
    # Check properties
    all_idem = all(T_sub[i][i] == i for i in range(7))
    print(f"  {s}: all idempotent? {all_idem}")
    if all_idem:
        for row in T_sub:
            print(f"    " + " ".join(f"{v:>2d}" for v in row))

# Moufang analysis: where does TSML_Idempotent fail Moufang?
print("\nMIDDLE MOUFANG failures in TSML_Idempotent (first 20):")
mou_fails = []
for x in range(N):
    for y in range(N):
        for z in range(N):
            lhs = TSML_Idempotent[TSML_Idempotent[x][y]][TSML_Idempotent[z][x]]
            rhs = TSML_Idempotent[x][TSML_Idempotent[TSML_Idempotent[y][z]][x]]
            if lhs != rhs:
                mou_fails.append((x, y, z, lhs, rhs))
print(f"Total middle Moufang failures: {len(mou_fails)}/1000")
# Are the failures at specific locations?
locations = [(x,y,z) for (x,y,z,_,_) in mou_fails]
involved = {}
for (x,y,z) in locations:
    for e in (x, y, z):
        involved[e] = involved.get(e, 0) + 1
print(f"Element involvement in Moufang failures:")
for e in range(N):
    print(f"  {e}: {involved.get(e, 0)}")

# Compare with TSML_Jordan for Moufang failure distribution
TSML_Jordan = [
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

mou_fails_J = []
for x in range(N):
    for y in range(N):
        for z in range(N):
            lhs = TSML_Jordan[TSML_Jordan[x][y]][TSML_Jordan[z][x]]
            rhs = TSML_Jordan[x][TSML_Jordan[TSML_Jordan[y][z]][x]]
            if lhs != rhs:
                mou_fails_J.append((x, y, z))
print(f"\nTSML_Jordan Moufang failures: {len(mou_fails_J)}/1000")
involved_J = {}
for (x,y,z) in mou_fails_J:
    for e in (x, y, z):
        involved_J[e] = involved_J.get(e, 0) + 1
print(f"Element involvement in TSML_Jordan Moufang failures:")
for e in range(N):
    print(f"  {e}: {involved_J.get(e, 0)}")

# =========================================================
# Check TSML_Idempotent's automorphism group
# =========================================================
from itertools import permutations
print("\nAUTOMORPHISM GROUP of TSML_Idempotent (fixing 0 and 7):")
auts = []
for p in permutations(range(N)):
    if p[0] != 0 or p[7] != 7: continue
    is_aut = True
    for i in range(N):
        for j in range(N):
            if p[TSML_Idempotent[i][j]] != TSML_Idempotent[p[i]][p[j]]:
                is_aut = False; break
        if not is_aut: break
    if is_aut: auts.append(p)
print(f"|Aut fixing 0,7| = {len(auts)}")
for a in auts[:20]:
    moved = [(i, a[i]) for i in range(N) if a[i] != i]
    if not moved: print("  identity")
    else: print(f"  {moved}")

