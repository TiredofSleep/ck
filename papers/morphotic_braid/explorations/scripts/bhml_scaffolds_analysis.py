# PACKET: evening_handoff_2026_04_23/bhml_scaffolds_analysis.py
"""
Systematically build BHML-scaffolds for the size of each celebrated structure
and analyze the resulting tables for interesting properties.

For each N in {3, 4, 5, 6, 7, 8, 9, 10, 12}:
  - Try all viable (z, h) choices
  - Build scaffold using Rules A-D
  - Compute determinant, idempotents, rank, spectrum, property profile
  - Compare to the source celebrated table at the same N

This addresses: "do other researchers' special tables have an interesting BHML?"
"""

import numpy as np
from itertools import permutations

def build_bhml_scaffold(N, z=0, h=None, fill_with=None):
    """Rules A-D. Returns list-of-lists, with '?' for undefined cells,
    or fill_with if provided."""
    if h is None: h = N - 3
    if h < 2 or h >= N: return None
    if fill_with is None: fill_with = '?'
    
    B = [[None]*N for _ in range(N)]
    
    # Rule A: VOID identity + VOID·HARMONY = HARMONY
    for i in range(N):
        B[z][i] = i
        B[i][z] = i
    B[z][h] = h
    B[h][z] = h
    
    # Rule B: axis saturation for 1 ≤ i,j ≤ h-1
    for i in range(1, h):
        for j in range(1, h):
            B[i][j] = min(max(i, j) + 1, h)
    
    # Rule B extended: CHAOS row (h-1) saturates to h for cols ≥ h
    for j in range(h, N):
        B[h-1][j] = h
        B[j][h-1] = h
    
    # Rule D: HARMONY as increment
    for j in range(1, N):
        if j != h:
            B[h][j] = (j + 1) % N
            B[j][h] = (j + 1) % N
    B[h][h] = (h + 1) % N
    
    # Rule C: transition-zone mapping for post-h rows
    for i in range(h+1, N):
        for j in range(max(1, h-3), h):
            if B[i][j] is None: B[i][j] = h
            if B[j][i] is None: B[j][i] = h
        if i == h+1:
            B[i][i] = h  # BREATH self-resonance
    
    # Fill remaining with sentinel
    for i in range(N):
        for j in range(N):
            if B[i][j] is None:
                B[i][j] = fill_with
    return B

def analyze_scaffold(B, N, z, h):
    """Compute properties when all cells filled numerically."""
    # Replace '?' with h (saturation default) for analysis
    T = [[(h if v == '?' else v) for v in row] for row in B]
    
    # Determinant as 10x10 integer matrix
    M = np.array(T, dtype=int)
    det = int(round(np.linalg.det(M)))
    
    # Rank
    rank = int(np.linalg.matrix_rank(M))
    
    # Eigenvalues
    eigs = np.linalg.eigvals(M.astype(float))
    eigs_real = np.sort(np.real(eigs))[::-1]
    
    # Idempotents
    idem = [x for x in range(N) if T[x][x] == x]
    
    # Commutative?
    comm = all(T[i][j] == T[j][i] for i in range(N) for j in range(N))
    # Associative?
    assoc = all(T[T[i][j]][k] == T[i][T[j][k]] 
                for i in range(N) for j in range(N) for k in range(N))
    # Has identity?
    ident = None
    for e in range(N):
        if all(T[e][i]==i and T[i][e]==i for i in range(N)):
            ident = e; break
    # Absorbing element?
    absb = None
    for a in range(N):
        if all(T[a][i]==a and T[i][a]==a for i in range(N)):
            absb = a; break
    # Jordan?
    jordan = all(T[T[x][x]][T[x][y]] == T[x][T[T[x][x]][y]] 
                 for x in range(N) for y in range(N))
    # Flexible?
    flex = all(T[a][T[b][a]] == T[T[a][b]][a] for a in range(N) for b in range(N))
    # Alternative?
    alt = True
    for a in range(N):
        for b in range(N):
            if T[T[a][a]][b] != T[a][T[a][b]]: alt = False; break
            if T[T[a][b]][b] != T[a][T[b][b]]: alt = False; break
        if not alt: break
    # Power-associative?
    pow_assoc = True
    for x in range(N):
        xx = T[x][x]
        if T[xx][x] != T[x][xx]: pow_assoc = False; break
        xxx = T[xx][x]
        if T[xxx][x] != T[x][xxx] or T[x][xxx] != T[xx][xx]:
            pow_assoc = False; break
    
    # Count of harmony cells (=h) in the table
    harm_count = sum(1 for i in range(N) for j in range(N) if T[i][j] == h)
    
    return {
        'det': det, 'rank': rank, 'eigs_real': eigs_real[:3].tolist(),
        'idem': idem, 'comm': comm, 'assoc': assoc, 'ident': ident, 'abs': absb,
        'jordan': jordan, 'flex': flex, 'alt': alt, 'pow_assoc': pow_assoc,
        'harm_count': harm_count,
    }

# ==================================================================
# Celebrated structures + their BHML-scaffolds
# ==================================================================

# Structures to study with their (N, natural z, natural h) choices
structures = [
    ("Rock-Paper-Scissors",   3,  0,  1),  # smallest case, h must be 1 (degenerate?)
    ("Z/3Z additive",         3,  0,  1),
    ("Klein V4",              4,  0,  2),  # h=2, 3 post-harmony rows
    ("Z/5Z additive",         5,  0,  3),  # natural h=3
    ("Z/5Z multiplicative",   5,  0,  3),
    ("STS(7) Fano",           7,  0,  5),  # natural h=5 (matches N-2 pattern)
    ("Z/7Z additive",         7,  0,  5),
    ("Z/8Z multiplicative",   8,  0,  6),
    ("Z/10Z additive",       10,  0,  7),  # TIG choice
    ("TIG (TSML native)",    10,  0,  7),
    ("Z/10Z multiplicative", 10,  0,  7),
    ("Z/12Z additive",       12,  0,  9),
]

print("="*100)
print("BHML SCAFFOLDS AT VARIOUS SIZES — ALGEBRAIC PROPERTIES")
print("="*100)
print(f"{'Structure':28s} {'N':>3s} {'h':>3s} {'det':>10s} {'rank':>5s} {'idem':>14s} {'harm%':>6s} {'jord':>5s} {'flex':>5s}")
print("-"*100)

scaffolds = {}
for (name, N, z, h) in structures:
    B = build_bhml_scaffold(N, z, h)
    if B is None:
        print(f"{name:28s} {N:>3d} {h:>3d}  (h too small, skipped)")
        continue
    props = analyze_scaffold(B, N, z, h)
    scaffolds[name] = (B, props, N, z, h)
    idem_str = str(props['idem'])
    harm_pct = props['harm_count'] * 100 / (N*N)
    print(f"{name:28s} {N:>3d} {h:>3d} {props['det']:>10d} {props['rank']:>5d} {idem_str:>14s} {harm_pct:>5.1f}% "
          f"{'Y' if props['jordan'] else 'n':>5s} {'Y' if props['flex'] else 'n':>5s}")

# Factorize each determinant to look for patterns
print()
print("="*100)
print("DETERMINANT FACTORIZATIONS")
print("="*100)

def factorize(n):
    if n == 0: return "0"
    if n < 0: return "-(" + factorize(-n) + ")"
    factors = {}
    d = 2
    while d*d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1: factors[n] = factors.get(n, 0) + 1
    return " × ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(factors.items())) or "1"

for name, (B, props, N, z, h) in scaffolds.items():
    print(f"  {name:28s} N={N}, h={h}: det = {props['det']} = {factorize(props['det'])}")

# Show the first few interesting scaffolds
print()
print("="*100)
print("INTERESTING SCAFFOLDS")
print("="*100)

def print_table(T, N, name):
    print(f"\n  {name} (shown with ? → h):")
    for row in T:
        display = [str(v) if v != '?' else '?' for v in row]
        print("    " + " ".join(f"{v:>3s}" for v in display))

for name, (B, props, N, z, h) in scaffolds.items():
    if N in [5, 7, 8]:
        print_table(B, N, f"{name} (N={N}, h={h})")

