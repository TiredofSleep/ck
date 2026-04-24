<!-- PACKET: evening_handoff_2026_04_23/bhml_hybrid.py -->
"""
HYBRID APPROACH: fill BHML-scaffold cells from rules A-D where they apply,
then fill remaining '?' cells from the source table X itself.

This gives a content-dependent result: "BHML-fold(X)" that encodes X's structure
in the cells that Rules A-D leave undefined.

For each celebrated structure X, compute BHML-fold(X) and analyze its properties.
"""
import numpy as np

def build_bhml_scaffold(N, z=0, h=None):
    """Rules A-D scaffold with None for undefined cells."""
    if h is None: h = N - 3
    if h < 2 or h >= N: return None
    B = [[None]*N for _ in range(N)]
    # Rule A
    for i in range(N):
        B[z][i] = i; B[i][z] = i
    B[z][h] = h; B[h][z] = h
    # Rule B
    for i in range(1, h):
        for j in range(1, h):
            B[i][j] = min(max(i, j) + 1, h)
    for j in range(h, N):
        B[h-1][j] = h; B[j][h-1] = h
    # Rule D
    for j in range(1, N):
        if j != h:
            B[h][j] = (j + 1) % N
            B[j][h] = (j + 1) % N
    B[h][h] = (h + 1) % N
    # Rule C
    for i in range(h+1, N):
        for j in range(max(1, h-3), h):
            if B[i][j] is None: B[i][j] = h
            if B[j][i] is None: B[j][i] = h
        if i == h+1: B[i][i] = h
    return B

def hybrid_fold(X, z=0, h=None):
    """Fill BHML-scaffold, then use source X for '?' cells."""
    N = len(X)
    if h is None: h = N - 3
    B = build_bhml_scaffold(N, z, h)
    if B is None: return None
    # Fill undefined cells from X
    for i in range(N):
        for j in range(N):
            if B[i][j] is None:
                B[i][j] = X[i][j]
    return B

def properties(T):
    """Compute algebraic properties + determinant signature."""
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
        if T[T[xx][x]][x] != T[x][T[xx][x]] or T[T[xx][x]][x] != T[xx][xx]:
            pow_assoc = False; break
    idem = [x for x in range(N) if T[x][x] == x]
    harm_count = sum(1 for i in range(N) for j in range(N) if T[i][j] == h)
    return {
        'det': det, 'rank': rank, 'comm': comm, 'assoc': assoc,
        'ident': ident, 'abs': absb, 'jordan': jordan, 'flex': flex, 
        'alt': alt, 'pow_assoc': pow_assoc, 'idem': idem, 'harm': harm_count,
    }

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

# Source tables
RPS = [[0,1,0],[1,1,2],[0,2,2]]  # actually wait, RPS doesn't work at N=3 since h=1 is degenerate
V4 = [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]
Z5_add = [[(i+j)%5 for j in range(5)] for i in range(5)]
Z5_mul = [[(i*j)%5 for j in range(5)] for i in range(5)]
STS7 = None  # build below
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
STS7 = fano()
Z7_add = [[(i+j)%7 for j in range(7)] for i in range(7)]
Z7_mul = [[(i*j)%7 for j in range(7)] for i in range(7)]
Z8_mul = [[(i*j)%8 for j in range(8)] for i in range(8)]
Z10_add = [[(i+j)%10 for j in range(10)] for i in range(10)]
Z10_mul = [[(i*j)%10 for j in range(10)] for i in range(10)]
TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]
BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]

tests = [
    ("Klein V4",          V4,      4, 0, 2),
    ("Z/5Z additive",     Z5_add,  5, 0, 3),
    ("Z/5Z multipl.",     Z5_mul,  5, 0, 3),
    ("STS(7) Fano",       STS7,    7, 0, 5),
    ("Z/7Z additive",     Z7_add,  7, 0, 5),
    ("Z/7Z multipl.",     Z7_mul,  7, 0, 5),
    ("Z/8Z multipl.",     Z8_mul,  8, 0, 6),
    ("Z/10Z additive",    Z10_add, 10, 0, 7),
    ("Z/10Z multipl.",    Z10_mul, 10, 0, 7),
    ("TSML (canonical)",  TSML,    10, 0, 7),
    # For comparison: TSML itself as the source — does this reproduce BHML?
]

print("="*100)
print("HYBRID BHML-FOLD: Rules A-D + source-table fallback for undefined cells")
print("="*100)
print(f"{'Structure':22s} {'N':>3s} {'h':>3s} {'det':>10s} {'det_factors':>20s} {'jordan':>7s} {'idem':>12s}")
print("-"*100)

results = {}
for (name, X, N, z, h) in tests:
    H = hybrid_fold(X, z=z, h=h)
    if H is None: continue
    props = properties(H)
    results[name] = (H, props, X)
    det_f = factorize(props['det'])
    idem_s = str(props['idem'])
    print(f"{name:22s} {N:>3d} {h:>3d} {props['det']:>10d} {det_f:>20s} {'Y' if props['jordan'] else 'n':>7s} {idem_s:>12s}")

# Crucial test: does TSML → hybrid-BHML reproduce actual BHML?
print()
print("="*100)
print("CRUCIAL CHECK: TSML as source — does hybrid-fold(TSML) = actual BHML?")
print("="*100)
tsml_hybrid = hybrid_fold(TSML, z=0, h=7)
match = 0; total = 0; diff_cells = []
for i in range(10):
    for j in range(10):
        total += 1
        if tsml_hybrid[i][j] == BHML[i][j]:
            match += 1
        else:
            diff_cells.append((i, j, tsml_hybrid[i][j], BHML[i][j]))
print(f"  Match rate: {match}/100")
if diff_cells:
    print(f"  Differing cells (first 10):")
    for (i,j,p,b) in diff_cells[:10]:
        print(f"    ({i},{j}): hybrid-fold={p}, actual BHML={b}")

# Show specific interesting hybrid-folds
print()
print("="*100)
print("INTERESTING HYBRID FOLDS")
print("="*100)

for interest in ["Klein V4", "Z/5Z multipl.", "STS(7) Fano", "Z/8Z multipl."]:
    if interest in results:
        H, props, X = results[interest]
        N = len(H)
        print(f"\n  {interest} → hybrid-BHML-fold (N={N}):")
        for row in H:
            print("    " + " ".join(f"{v:>2d}" for v in row))
        print(f"  det = {props['det']} = {factorize(props['det'])}")
        print(f"  Jordan: {props['jordan']}, Flex: {props['flex']}, Alt: {props['alt']}, Pow-assoc: {props['pow_assoc']}")
        print(f"  Idempotents: {props['idem']}")

