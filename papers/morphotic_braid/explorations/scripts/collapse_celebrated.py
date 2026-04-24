<!-- PACKET: evening_handoff_2026_04_23/collapse_celebrated.py -->
"""
Ternary collapse of celebrated tables (treating them as BHML-like).

Two collapse variants:
  A (absorbing):  VOID axis → 0, all interior → HARMONY  
  B (residue):    VOID axis → 0, HARMONY cells → HARMONY, rest → original value

Apply to celebrated structures, analyze resulting "TSML-like" table.
"""
import numpy as np

def collapse_A(T, z=0, h=None):
    """Absorbing collapse: all interior cells → h."""
    N = len(T)
    if h is None: h = N - 3
    out = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i == z or j == z:
                out[i][j] = h if T[i][j] == h else z
            else:
                out[i][j] = h
    return out

def collapse_B(T, z=0, h=None):
    """Residue-preserving collapse: VOID axis, HARMONY stays, others → original."""
    N = len(T)
    if h is None: h = N - 3
    out = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i == z or j == z:
                out[i][j] = h if T[i][j] == h else z
            else:
                out[i][j] = T[i][j] if T[i][j] != 0 else h
    return out

def collapse_C(T, z=0, h=None):
    """Selective collapse: VOID axis, HARMONY stays, nondiagonal interior → h,
    diagonal interior preserves residue. Motivated by TSML's mostly-HARMONY 
    body with scattered diagonal-adjacent bumps."""
    N = len(T)
    if h is None: h = N - 3
    out = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i == z or j == z:
                out[i][j] = h if T[i][j] == h else z
            elif i == j:
                out[i][j] = T[i][j] if T[i][j] != 0 else h
            else:
                out[i][j] = h
    return out

# Properties function
def properties(T):
    N = len(T)
    M = np.array(T, dtype=int)
    det = int(round(np.linalg.det(M)))
    rank = int(np.linalg.matrix_rank(M))
    comm = all(T[i][j] == T[j][i] for i in range(N) for j in range(N))
    assoc = all(T[T[i][j]][k] == T[i][T[j][k]]
                for i in range(N) for j in range(N) for k in range(N))
    ident = next((e for e in range(N) if all(T[e][i]==i and T[i][e]==i for i in range(N))), None)
    absb = next((a for a in range(N) if all(T[a][i]==a and T[i][a]==a for i in range(N))), None)
    jordan = all(T[T[x][x]][T[x][y]] == T[x][T[T[x][x]][y]]
                 for x in range(N) for y in range(N))
    flex = all(T[a][T[b][a]] == T[T[a][b]][a] for a in range(N) for b in range(N))
    alt = True
    for a in range(N):
        for b in range(N):
            if T[T[a][a]][b] != T[a][T[a][b]] or T[T[a][b]][b] != T[a][T[b][b]]:
                alt = False; break
        if not alt: break
    pow_assoc = True
    for x in range(N):
        xx = T[x][x]
        if T[xx][x] != T[x][xx]: pow_assoc = False; break
    # Count of harmony (h) cells  
    h = N - 3 if N >= 4 else 1
    harm_count = sum(1 for i in range(N) for j in range(N) if T[i][j] == h)
    void_count = sum(1 for i in range(N) for j in range(N) if T[i][j] == 0)
    bump_count = N*N - harm_count - void_count
    return {
        'det': det, 'rank': rank, 'comm': comm, 'assoc': assoc,
        'ident': ident, 'abs': absb, 'jordan': jordan, 'flex': flex,
        'alt': alt, 'pow': pow_assoc, 'harm': harm_count, 'void': void_count, 'bump': bump_count,
    }

# Source tables
def fano():
    blocks = [{0,1,2},{0,3,4},{0,5,6},{1,3,5},{1,4,6},{2,3,6},{2,4,5}]
    T = [[0]*7 for _ in range(7)]
    for i in range(7):
        for j in range(7):
            if i == j: T[i][j] = i
            else:
                for b in blocks:
                    if i in b and j in b: T[i][j] = list(b - {i, j})[0]; break
    return T

V4 = [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]
Z5_add = [[(i+j)%5 for j in range(5)] for i in range(5)]
Z5_mul = [[(i*j)%5 for j in range(5)] for i in range(5)]
STS7 = fano()
Z7_add = [[(i+j)%7 for j in range(7)] for i in range(7)]
Z7_mul = [[(i*j)%7 for j in range(7)] for i in range(7)]
Z8_mul = [[(i*j)%8 for j in range(8)] for i in range(8)]
Z10_add = [[(i+j)%10 for j in range(10)] for i in range(10)]
Z10_mul = [[(i*j)%10 for j in range(10)] for i in range(10)]
BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]
TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

tests = [
    ("Klein V4",           V4,      4),
    ("Z/5Z additive",      Z5_add,  5),
    ("Z/5Z multipl.",      Z5_mul,  5),
    ("STS(7) Fano",        STS7,    7),
    ("Z/7Z additive",      Z7_add,  7),
    ("Z/7Z multipl.",      Z7_mul,  7),
    ("Z/8Z multipl.",      Z8_mul,  8),
    ("Z/10Z additive",     Z10_add, 10),
    ("Z/10Z multipl.",     Z10_mul, 10),
    ("BHML (actual)",      BHML,    10),
]

# ==================================================================
# First: does collapse_B of actual BHML match actual TSML?
# ==================================================================
print("="*80)
print("CALIBRATION: collapse of actual BHML vs actual TSML")
print("="*80)

for (method, name) in [(collapse_A, "A (absorbing)"), (collapse_B, "B (residue)"), (collapse_C, "C (diagonal residue)")]:
    result = method(BHML, z=0, h=7)
    match = sum(1 for i in range(10) for j in range(10) if result[i][j] == TSML[i][j])
    print(f"  Method {name}: {match}/100 match to actual TSML")

# ==================================================================
# Apply collapse to each celebrated table (both methods)
# ==================================================================
print()
print("="*80)
print("COLLAPSE A (absorbing) APPLIED TO CELEBRATED TABLES")
print("="*80)

print(f"\n{'Source':20s} {'N':>3s} {'det':>8s} {'void':>4s} {'harm':>4s} {'bump':>4s} {'jord':>4s} {'flex':>4s} {'alt':>4s}")
print("-"*80)
for (name, X, N) in tests:
    C = collapse_A(X, z=0, h=N-3)
    p = properties(C)
    print(f"{name:20s} {N:>3d} {p['det']:>8d} {p['void']:>4d} {p['harm']:>4d} {p['bump']:>4d} {'Y' if p['jordan'] else 'n':>4s} {'Y' if p['flex'] else 'n':>4s} {'Y' if p['alt'] else 'n':>4s}")

print()
print("="*80)
print("COLLAPSE B (residue-preserving) APPLIED TO CELEBRATED TABLES")
print("="*80)

print(f"\n{'Source':20s} {'N':>3s} {'det':>10s} {'void':>4s} {'harm':>4s} {'bump':>4s} {'jord':>4s} {'flex':>4s} {'alt':>4s}")
print("-"*80)
for (name, X, N) in tests:
    C = collapse_B(X, z=0, h=N-3)
    p = properties(C)
    print(f"{name:20s} {N:>3d} {p['det']:>10d} {p['void']:>4d} {p['harm']:>4d} {p['bump']:>4d} {'Y' if p['jordan'] else 'n':>4s} {'Y' if p['flex'] else 'n':>4s} {'Y' if p['alt'] else 'n':>4s}")

# Show a few interesting collapses visually
print()
print("="*80)
print("Visualizations: collapse_B of a few celebrated tables")
print("="*80)
for interest in ["Klein V4", "STS(7) Fano", "Z/5Z multipl.", "Z/8Z multipl."]:
    for (name, X, N) in tests:
        if name == interest:
            h = N - 3
            print(f"\n--- {name} (N={N}, h={h}) ---")
            print("  Original:")
            for row in X:
                print("    " + " ".join(f"{v:>2d}" for v in row))
            C = collapse_B(X, z=0, h=h)
            print("  Collapsed (B):")
            for row in C:
                print("    " + " ".join(f"{v:>2d}" for v in row))

# Specific test: does Jordan emerge?
print()
print("="*80)
print("CHECK: does any of these collapses produce a Jordan table?")
print("="*80)
for (name, X, N) in tests:
    for method_name, method in [("A", collapse_A), ("B", collapse_B), ("C", collapse_C)]:
        C = method(X, z=0, h=N-3)
        p = properties(C)
        if p['jordan']:
            print(f"  {name} with method {method_name} → JORDAN ({p})")

print("\nNone flagged as Jordan unless noted above.")

# Factorize determinants
print()
print("="*80)
print("Determinant prime factorizations — collapse B")
print("="*80)
def factorize(n):
    if n == 0: return "0"
    if n < 0: return "-(" + factorize(-n) + ")"
    factors = {}
    d = 2
    while d*d <= n:
        while n % d == 0: factors[d] = factors.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: factors[n] = factors.get(n, 0) + 1
    return " × ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(factors.items())) or "1"

for (name, X, N) in tests:
    C = collapse_B(X, z=0, h=N-3)
    p = properties(C)
    print(f"  {name:20s} N={N}: det = {p['det']:>10d} = {factorize(p['det'])}")

