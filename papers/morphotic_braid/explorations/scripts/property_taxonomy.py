# PACKET: evening_handoff_2026_04_23/property_taxonomy.py
"""
Property-based taxonomy for finite commutative binary operations on Z/10Z.

Test each table in the TIG family against a battery of algebraic properties.
Map results into a property grid. Identify which property combinations are
occupied by TIG's tables and which are not.
"""
from itertools import product, permutations
from math import gcd
import numpy as np

N = 10

# ================= Build the family of tables ====================

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

DOING = [[(TSML[i][j] - BHML[i][j]) % 10 for j in range(N)] for i in range(N)]
ADD = [[(i+j) % N for j in range(N)] for i in range(N)]
MUL = [[(i*j) % N for j in range(N)] for i in range(N)]

sigma_perm = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
CL_mult = [[sigma_perm[(i*j) % N] for j in range(N)] for i in range(N)]
CL_add  = [[sigma_perm[(i+j) % N] for j in range(N)] for i in range(N)]

# Build canonical C_0
def nu2(n):
    if n == 0: return 999
    k = 0
    while n % 2 == 0: n //= 2; k += 1
    return k
core10 = [u for u in range(1,N) if gcd(u,N)==1 and nu2(3*u+1)==1]

def build_C0():
    T = [[0]*N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if x == 0 or y == 0: T[x][y] = 0
            elif x not in core10 or y not in core10: T[x][y] = 7
            else:
                sx, sy = nu2(3*x+1), nu2(3*y+1)
                if sx < sy: T[x][y] = x
                elif sy < sx: T[x][y] = y
                else: T[x][y] = 7
    return T

C0 = build_C0()

# Trivial absorbing semigroup at h=7
T_abs_7 = [[0 if (i==0 or j==0) else 7 for j in range(N)] for i in range(N)]

# ================= Property tests ====================

def is_commutative(T):
    return all(T[i][j] == T[j][i] for i in range(N) for j in range(N))

def is_associative(T):
    return all(T[T[i][j]][k] == T[i][T[j][k]] for i in range(N) for j in range(N) for k in range(N))

def is_idempotent(T):
    """Every element is idempotent: T[x][x] = x for all x."""
    return all(T[i][i] == i for i in range(N))

def has_identity(T):
    """Does there exist e such that e·x = x·e = x for all x?"""
    for e in range(N):
        if all(T[e][i] == i and T[i][e] == i for i in range(N)):
            return e
    return None

def absorbing_element(T):
    """Does there exist a such that a·x = x·a = a for all x?"""
    for a in range(N):
        if all(T[a][i] == a and T[i][a] == a for i in range(N)):
            return a
    return None

def all_idempotents(T):
    """Set of elements x with x·x = x."""
    return [x for x in range(N) if T[x][x] == x]

def is_band(T):
    """Band = associative + every element idempotent."""
    return is_associative(T) and is_idempotent(T)

def left_cancellative(T):
    """a·x = a·y ⟹ x = y for all a."""
    for a in range(N):
        for x in range(N):
            for y in range(N):
                if x != y and T[a][x] == T[a][y]: return False
    return True

def quasigroup(T):
    """Each row and column is a permutation."""
    for i in range(N):
        row = [T[i][j] for j in range(N)]
        col = [T[j][i] for j in range(N)]
        if sorted(row) != list(range(N)): return False
        if sorted(col) != list(range(N)): return False
    return True

def left_distributive(T):
    """a·(b·c) = (a·b)·(a·c) for all a,b,c."""
    return all(T[a][T[b][c]] == T[T[a][b]][T[a][c]] 
               for a in range(N) for b in range(N) for c in range(N))

def flexible(T):
    """a·(b·a) = (a·b)·a for all a,b."""
    return all(T[a][T[b][a]] == T[T[a][b]][a] for a in range(N) for b in range(N))

def alternative(T):
    """(a·a)·b = a·(a·b) AND (a·b)·b = a·(b·b) for all a,b."""
    for a in range(N):
        for b in range(N):
            if T[T[a][a]][b] != T[a][T[a][b]]: return False
            if T[T[a][b]][b] != T[a][T[b][b]]: return False
    return True

def power_associative(T):
    """Every element generates an associative subgroupoid. 
    For finite ops, check: x·x, (x·x)·x vs x·(x·x), etc., up to order 4."""
    for x in range(N):
        xx = T[x][x]
        xxx_L = T[xx][x]
        xxx_R = T[x][xx]
        if xxx_L != xxx_R: return False
        xxxx_1 = T[xxx_L][x]
        xxxx_2 = T[x][xxx_L]
        xxxx_3 = T[xx][xx]
        if xxxx_1 != xxxx_2 or xxxx_2 != xxxx_3: return False
    return True

def medial(T):
    """(a·b)·(c·d) = (a·c)·(b·d) — medial/entropic law."""
    for a in range(N):
        for b in range(N):
            for c in range(N):
                for d in range(N):
                    if T[T[a][b]][T[c][d]] != T[T[a][c]][T[b][d]]: return False
    return True

def has_zero_divisors(T, abs_elem):
    """If abs_elem is the absorbing/zero element, are there x,y ≠ abs with x·y = abs?"""
    if abs_elem is None: return None
    for x in range(N):
        if x == abs_elem: continue
        for y in range(N):
            if y == abs_elem: continue
            if T[x][y] == abs_elem: return True
    return False

def number_of_idempotents(T):
    return len([x for x in range(N) if T[x][x] == x])

def harmony_density(T, h=7):
    return sum(1 for i in range(N) for j in range(N) if T[i][j] == h)

def void_density(T):
    return sum(1 for i in range(N) for j in range(N) if T[i][j] == 0)

# ================= Analyze each table ====================

tables = {
    "TSML":     TSML,
    "BHML":     BHML,
    "Doing":    DOING,
    "C_0":      C0,
    "T_abs_7":  T_abs_7,
    "CL_mult":  CL_mult,
    "CL_add":   CL_add,
    "ADD":      ADD,
    "MUL":      MUL,
}

print("="*110)
print("PROPERTY MATRIX FOR TIG FAMILY (and cousins)")
print("="*110)
headers = ["Table", "comm", "assoc", "idempot", "identity", "absorb", "band", "quasi", "flex", "alt", "pow.assoc", "medial", "left-dist", "#idem"]
print(f"{'':12s}" + "".join(f"{h:>9s}" for h in headers[1:]))
print("-"*110)

for name, T in tables.items():
    row = [name]
    row.append("Y" if is_commutative(T) else "n")
    row.append("Y" if is_associative(T) else "n")
    row.append("Y" if is_idempotent(T) else "n")
    e = has_identity(T)
    row.append(str(e) if e is not None else "-")
    a = absorbing_element(T)
    row.append(str(a) if a is not None else "-")
    row.append("Y" if is_band(T) else "n")
    row.append("Y" if quasigroup(T) else "n")
    row.append("Y" if flexible(T) else "n")
    row.append("Y" if alternative(T) else "n")
    row.append("Y" if power_associative(T) else "n")
    row.append("Y" if medial(T) else "n")
    row.append("Y" if left_distributive(T) else "n")
    row.append(str(number_of_idempotents(T)))
    print(f"{row[0]:12s}" + "".join(f"{v:>9s}" for v in row[1:]))

print()
print("="*110)
print("PROPERTY SIGNATURE (as tuple of booleans, for clustering)")
print("="*110)
print("Signature: (comm, assoc, has_id, has_abs, medial, flexible, alt, pow_assoc)")
print()

signatures = {}
for name, T in tables.items():
    sig = (
        is_commutative(T),
        is_associative(T),
        has_identity(T) is not None,
        absorbing_element(T) is not None,
        medial(T),
        flexible(T),
        alternative(T),
        power_associative(T),
    )
    signatures[name] = sig
    print(f"  {name:10s}: {sig}")

print()
# Group by signature
from collections import defaultdict
grouped = defaultdict(list)
for name, sig in signatures.items():
    grouped[sig].append(name)

print("="*110)
print("CLUSTERS BY IDENTICAL PROPERTY SIGNATURE")
print("="*110)
for sig, members in grouped.items():
    print(f"  Signature {sig}")
    print(f"    Members: {members}")

