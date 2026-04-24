# PACKET: evening_handoff_2026_04_23/taxonomy_placement.py
"""
TASK 2: Forget TSML and place it via standard taxonomic axes.

Using the classification parameters from Huang, Lehtonen, Csákány, Waldhauser,
Bremner, and standard non-associative algebra:

Axes:
1. Associativity
2. Commutativity
3. Idempotency (every element idempotent vs not)
4. Identity element
5. Absorbing element (zero)
6. Alternative law
7. Flexibility
8. Jordan identity
9. Power-associativity
10. Mediality (entropic)
11. Left/Right distributivity
12. Quasigroup (Latin square)
13. ac-spectrum behavior

Then classify each celebrated structure and compare with TSML.
"""

from math import gcd
from itertools import permutations

N = 10

# ================ PROPERTY BATTERY ================
def is_comm(T, n=None): 
    n = n or len(T)
    return all(T[i][j] == T[j][i] for i in range(n) for j in range(n))
def is_assoc(T, n=None):
    n = n or len(T)
    return all(T[T[i][j]][k] == T[i][T[j][k]] for i in range(n) for j in range(n) for k in range(n))
def is_idemp_all(T, n=None):
    n = n or len(T)
    return all(T[i][i] == i for i in range(n))
def has_id(T, n=None):
    n = n or len(T)
    for e in range(n):
        if all(T[e][i]==i and T[i][e]==i for i in range(n)): return e
    return None
def has_abs(T, n=None):
    n = n or len(T)
    for a in range(n):
        if all(T[a][i]==a and T[i][a]==a for i in range(n)): return a
    return None
def is_jordan(T, n=None):
    n = n or len(T)
    return all(T[T[x][x]][T[x][y]] == T[x][T[T[x][x]][y]] for x in range(n) for y in range(n))
def is_flex(T, n=None):
    n = n or len(T)
    return all(T[a][T[b][a]] == T[T[a][b]][a] for a in range(n) for b in range(n))
def is_alt(T, n=None):
    n = n or len(T)
    for a in range(n):
        for b in range(n):
            if T[T[a][a]][b] != T[a][T[a][b]]: return False
            if T[T[a][b]][b] != T[a][T[b][b]]: return False
    return True
def is_pow(T, n=None):
    n = n or len(T)
    for x in range(n):
        xx = T[x][x]
        if T[xx][x] != T[x][xx]: return False
        xxx = T[xx][x]
        if T[xxx][x] != T[x][xxx]: return False
        if T[xxx][x] != T[xx][xx]: return False
    return True
def is_medial(T, n=None):
    n = n or len(T)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    if T[T[a][b]][T[c][d]] != T[T[a][c]][T[b][d]]: return False
    return True
def is_quasi(T, n=None):
    n = n or len(T)
    for i in range(n):
        if sorted([T[i][j] for j in range(n)]) != list(range(n)): return False
        if sorted([T[j][i] for j in range(n)]) != list(range(n)): return False
    return True

def profile(T):
    n = len(T)
    c = is_comm(T, n); a = is_assoc(T, n)
    return {
        'n': n, 'comm': c, 'assoc': a,
        'idemp': is_idemp_all(T, n),
        'id': has_id(T, n), 'abs': has_abs(T, n),
        'flex': is_flex(T, n),
        'alt': is_alt(T, n),
        'jordan': is_jordan(T, n),
        'pow': is_pow(T, n),
        'medial': is_medial(T, n),
        'quasi': is_quasi(T, n),
    }

def classify(p):
    """Assign a genus/species label based on the property profile."""
    labels = []
    if p['comm'] and p['assoc']:
        if p['id'] is not None and p['quasi']:
            labels.append("ABELIAN GROUP")
        elif p['id'] is not None and p['abs'] is not None:
            labels.append("COMMUTATIVE MONOID-WITH-ZERO (ring-like)")
        elif p['id'] is not None:
            labels.append("COMMUTATIVE MONOID")
        elif p['abs'] is not None:
            labels.append("COMMUTATIVE SEMIGROUP WITH ABSORBING")
        else:
            labels.append("COMMUTATIVE SEMIGROUP")
        if p['idemp']:
            labels.append("SEMILATTICE (idempotent)")
    elif p['comm'] and not p['assoc']:
        if p['jordan'] and p['pow']:
            if p['quasi']:
                labels.append("JORDAN QUASIGROUP")
            elif p['abs'] is not None:
                labels.append("JORDAN-type MAGMA with absorbing (TSML-cell)")
            else:
                labels.append("JORDAN-type commutative magma")
        elif p['idemp'] and p['quasi']:
            labels.append("STEINER QUASIGROUP")
        elif p['quasi']:
            labels.append("COMMUTATIVE QUASIGROUP (non-Jordan)")
        elif p['medial']:
            labels.append("MEDIAL commutative magma")
        else:
            labels.append("COMMUTATIVE MAGMA (non-Jordan, non-Steiner)")
    elif not p['comm'] and p['assoc']:
        if p['quasi'] and p['id'] is not None:
            labels.append("NON-ABELIAN GROUP")
        else:
            labels.append("NON-COMMUTATIVE SEMIGROUP")
    else:
        labels.append("NON-COMM NON-ASSOC MAGMA")
    if p['alt'] and not p['assoc']:
        labels.append("ALTERNATIVE")
    return " / ".join(labels)

# ================ CELEBRATED STRUCTURES ================

# RPS (Rock-Paper-Scissors): canonical 3-element commutative non-associative magma
# 0=rock, 1=paper, 2=scissors; x beats y: x*y = x if x beats y else y
# Paper beats rock (1 beats 0), Scissors beats paper (2 beats 1), Rock beats scissors (0 beats 2)
# So: x*y = the winner of (x,y), and x*x = x
RPS = [
    [0, 1, 0],  # rock beats scissors, paper beats rock
    [1, 1, 2],  # paper self, scissors beats paper
    [0, 2, 2],  # rock beats scissors, scissors self
]

# Z/2Z additive
Z2 = [
    [0, 1],
    [1, 0],
]

# Z/3Z additive
Z3_add = [
    [0, 1, 2],
    [1, 2, 0],
    [2, 0, 1],
]

# Z/3Z multiplicative (not a group since 0 is absorbing)
Z3_mul = [
    [0, 0, 0],
    [0, 1, 2],
    [0, 2, 1],
]

# Klein four-group V
V4 = [
    [0, 1, 2, 3],
    [1, 0, 3, 2],
    [2, 3, 0, 1],
    [3, 2, 1, 0],
]

# Steiner quasigroup on 7 elements (Fano plane, STS(7))
# Blocks of the Fano plane: {0,1,2},{0,3,4},{0,5,6},{1,3,5},{1,4,6},{2,3,6},{2,4,5}
# Steiner quasigroup: x*y = the third element in the block containing {x,y}; x*x = x
def fano_steiner():
    blocks = [{0,1,2},{0,3,4},{0,5,6},{1,3,5},{1,4,6},{2,3,6},{2,4,5}]
    T = [[0]*7 for _ in range(7)]
    for i in range(7):
        for j in range(7):
            if i == j: T[i][j] = i
            else:
                for b in blocks:
                    if i in b and j in b:
                        T[i][j] = list(b - {i, j})[0]
                        break
    return T

STS7 = fano_steiner()

# Z/5Z additive (prime cyclic group)
Z5_add = [[(i+j) % 5 for j in range(5)] for i in range(5)]

# Z/4Z multiplicative (Z/4Z is a ring, but units are only {1,3}, not a group under mul mod 4)
Z4_mul = [[(i*j) % 4 for j in range(4)] for i in range(4)]

# Z/10Z additive and multiplicative (for comparison with TSML)
Z10_add = [[(i+j) % 10 for j in range(10)] for i in range(10)]
Z10_mul = [[(i*j) % 10 for j in range(10)] for i in range(10)]

# TSML (for reference)
TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],
]

# BHML
BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
]

celebrated = [
    ("Rock-Paper-Scissors (n=3)", RPS),
    ("Z/2Z additive (n=2)", Z2),
    ("Z/3Z additive (n=3)", Z3_add),
    ("Z/3Z multiplicative (n=3)", Z3_mul),
    ("Klein four-group V4 (n=4)", V4),
    ("STS(7) Steiner quasigroup / Fano (n=7)", STS7),
    ("Z/5Z additive (n=5)", Z5_add),
    ("Z/4Z multiplicative (n=4)", Z4_mul),
    ("Z/10Z additive (n=10)", Z10_add),
    ("Z/10Z multiplicative (n=10)", Z10_mul),
    ("TSML (n=10)", TSML),
    ("BHML (n=10)", BHML),
]

print("=" * 100)
print(f"TAXONOMIC CLASSIFICATION OF CELEBRATED TABLES")
print("=" * 100)
print(f"{'Structure':40s} {'comm':>5s} {'assoc':>5s} {'id':>4s} {'abs':>4s} {'flex':>5s} {'alt':>4s} {'jor':>4s} {'pow':>4s} {'med':>4s} {'qs':>4s}")
print("-" * 100)
for name, T in celebrated:
    p = profile(T)
    print(f"{name:40s} "
          f"{'Y' if p['comm'] else 'n':>5s} "
          f"{'Y' if p['assoc'] else 'n':>5s} "
          f"{str(p['id']) if p['id'] is not None else '-':>4s} "
          f"{str(p['abs']) if p['abs'] is not None else '-':>4s} "
          f"{'Y' if p['flex'] else 'n':>5s} "
          f"{'Y' if p['alt'] else 'n':>4s} "
          f"{'Y' if p['jordan'] else 'n':>4s} "
          f"{'Y' if p['pow'] else 'n':>4s} "
          f"{'Y' if p['medial'] else 'n':>4s} "
          f"{'Y' if p['quasi'] else 'n':>4s}")

print()
print("=" * 100)
print("GENUS / SPECIES CLASSIFICATION")
print("=" * 100)
for name, T in celebrated:
    p = profile(T)
    cat = classify(p)
    print(f"  {name:40s} → {cat}")

