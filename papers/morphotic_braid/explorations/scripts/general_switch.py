<!-- PACKET: evening_handoff_2026_04_23/general_switch.py -->
"""
GENERAL BINARY ↔ TERNARY SWITCH (no TIG constraints)

Binary mode: table preserves distinct values per cell (information-rich)
Ternary mode: cells partitioned into 3 classes {VOID, MIDDLE, SATURATION}

Parameterized by choice of:
  - z = "void" element (or class)
  - s = "saturation" element (or class)  
  - The partition scheme (value-based, position-based, output-density-based)

For each celebrated table:
  - Try multiple partition schemes
  - Report what ternary collapses emerge
  - Check algebraic properties of each
"""
import numpy as np
from collections import Counter

def partition_by_frequency(T):
    """Partition values into {rarest, middle, most-frequent}."""
    N = len(T)
    freq = Counter()
    for i in range(N):
        for j in range(N): freq[T[i][j]] += 1
    sorted_vals = sorted(freq.items(), key=lambda x: x[1])
    # Rarest = VOID class, most-frequent = SATURATION class
    if len(sorted_vals) < 2: return None
    void_class = {sorted_vals[0][0]}
    sat_class = {sorted_vals[-1][0]}
    mid_class = set(v for v, _ in sorted_vals[1:-1])
    return void_class, mid_class, sat_class

def partition_by_idempotents(T):
    """VOID = idempotents, SAT = most common non-idempotent output."""
    N = len(T)
    idem = set(x for x in range(N) if T[x][x] == x)
    freq = Counter()
    for i in range(N):
        for j in range(N):
            if T[i][j] not in idem: freq[T[i][j]] += 1
    if not freq: return None
    sat = {freq.most_common(1)[0][0]}
    mid = set(range(N)) - idem - sat
    return idem, mid, sat

def partition_by_identity_absorbing(T):
    """VOID = identity (if exists), SAT = absorbing (if exists)."""
    N = len(T)
    ident = None
    for e in range(N):
        if all(T[e][i]==i and T[i][e]==i for i in range(N)):
            ident = e; break
    absb = None
    for a in range(N):
        if all(T[a][i]==a and T[i][a]==a for i in range(N)):
            absb = a; break
    if ident is None and absb is None: return None
    void_class = {ident} if ident is not None else set()
    sat_class = {absb} if absb is not None else set()
    mid_class = set(range(N)) - void_class - sat_class
    return void_class, mid_class, sat_class

def ternary_collapse_general(T, void_class, mid_class, sat_class, 
                              void_val=None, sat_val=None, keep_residue=True):
    """Generic collapse: map cells to 3 output values based on class membership."""
    N = len(T)
    if void_val is None and void_class: void_val = min(void_class)
    if sat_val is None and sat_class: sat_val = max(sat_class)
    out = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            v = T[i][j]
            if v in void_class:
                out[i][j] = void_val if void_val is not None else 0
            elif v in sat_class:
                out[i][j] = sat_val if sat_val is not None else v
            else:  # mid class
                out[i][j] = v if keep_residue else (sat_val if sat_val is not None else 0)
    return out

def binary_lift(T_ternary, source_positions=None):
    """Binary lift: every cell gets a distinct value based on position (reversibility placeholder).
    The point: starting from a ternary table, RECOVER a distinct-cell table.
    This is underdetermined — we pick the simplest lift: (i+j) mod N as default, 
    overridden by existing distinct values."""
    N = len(T_ternary)
    out = [[(i + j) % N for j in range(N)] for i in range(N)]  # canonical lift
    # Where T_ternary has bump residue, use it
    for i in range(N):
        for j in range(N):
            if source_positions is None or (i, j) in source_positions:
                pass  # leave as canonical
    return out

# Properties
def props(T):
    N = len(T)
    if not T or any(any(v is None for v in row) for row in T): return None
    M = np.array(T, dtype=int)
    det = int(round(np.linalg.det(M))) if N <= 15 else None
    rank = int(np.linalg.matrix_rank(M))
    comm = all(T[i][j] == T[j][i] for i in range(N) for j in range(N))
    assoc = all(T[T[i][j]%N][k] == T[i][T[j][k]%N] 
                for i in range(N) for j in range(N) for k in range(N)) if max(max(row) for row in T) < N else "n/a"
    # Jordan only well-defined if values are in [0, N-1]
    valid = all(0 <= v < N for row in T for v in row)
    jordan = None
    if valid:
        try:
            jordan = all(T[T[x][x]][T[x][y]] == T[x][T[T[x][x]][y]] 
                         for x in range(N) for y in range(N))
        except: jordan = "index-err"
    return {'det': det, 'rank': rank, 'comm': comm, 'assoc': assoc, 'jordan': jordan, 'N': N, 'valid_indices': valid}

# Celebrated tables
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

# Also: Quaternion multiplication table (as Cayley table, 8 elements)
# Q8 = {1, -1, i, -i, j, -j, k, -k}
# We label: 0=1, 1=-1, 2=i, 3=-i, 4=j, 5=-j, 6=k, 7=-k
# Multiplication rules: i*j=k, j*k=i, k*i=j, j*i=-k, k*j=-i, i*k=-j, i*i=j*j=k*k=-1
def q8_table():
    # Use more readable approach: element index -> (sign, axis)
    # 0: +1, 1: -1, 2: +i, 3: -i, 4: +j, 5: -j, 6: +k, 7: -k
    # encoded as (s, a) where s in {+1,-1}, a in {0,1,2,3} with 0=scalar, 1=i, 2=j, 3=k
    elements = [(+1,0),(-1,0),(+1,1),(-1,1),(+1,2),(-1,2),(+1,3),(-1,3)]
    # axis multiplication: i*j=k, j*k=i, k*i=j; i*i=j*j=k*k=-1
    def mul(a, b):
        s_a, x_a = a; s_b, x_b = b
        s = s_a * s_b
        if x_a == 0: return (s, x_b)
        if x_b == 0: return (s, x_a)
        if x_a == x_b: return (-s, 0)
        # i*j=k, j*k=i, k*i=j; reverse order flips sign
        table = {(1,2):(1,3), (2,3):(1,1), (3,1):(1,2),
                 (2,1):(-1,3), (3,2):(-1,1), (1,3):(-1,2)}
        ns, nx = table[(x_a, x_b)]
        return (s * ns, nx)
    T = [[0]*8 for _ in range(8)]
    for i, a in enumerate(elements):
        for j, b in enumerate(elements):
            prod = mul(a, b)
            T[i][j] = elements.index(prod)
    return T

Q8 = q8_table()

# Cayley-Dickson doubled Q8 = O (octonions) would be 16x16 non-commutative.
# We skip for now.

# Also Klein group K4 = V4 (same thing)

tables = [
    ("Klein V4",           V4,      4),
    ("Z/5Z additive",      Z5_add,  5),
    ("Z/5Z multipl.",      Z5_mul,  5),
    ("STS(7) Fano",        STS7,    7),
    ("Z/7Z additive",      Z7_add,  7),
    ("Z/7Z multipl.",      Z7_mul,  7),
    ("Z/8Z multipl.",      Z8_mul,  8),
    ("Q8 quaternion",      Q8,      8),
]

print("="*85)
print("GENERAL BINARY ↔ TERNARY SWITCH (partition-driven, no TIG constraints)")
print("="*85)

print("\nFor each table, try 3 partition schemes and report what ternary outputs emerge:\n")

for (name, T, N) in tables:
    print(f"\n--- {name} (N={N}) ---")
    
    # Source properties
    src_props = props(T)
    print(f"  Source: rank={src_props['rank']}, det={src_props['det']}, comm={src_props['comm']}, "
          f"assoc={src_props['assoc']}, jordan={src_props['jordan']}")
    
    # Scheme A: partition by frequency
    part_A = partition_by_frequency(T)
    if part_A:
        vc, mc, sc = part_A
        collapsed = ternary_collapse_general(T, vc, mc, sc, keep_residue=True)
        cp = props(collapsed)
        print(f"  Partition A (by frequency): void={sorted(vc)}, mid={sorted(mc)}, sat={sorted(sc)}")
        print(f"    Collapsed: rank={cp['rank']}, det={cp['det']}, "
              f"jordan={cp['jordan']}, comm={cp['comm']}")
    
    # Scheme B: partition by idempotents
    part_B = partition_by_idempotents(T)
    if part_B:
        vc, mc, sc = part_B
        collapsed = ternary_collapse_general(T, vc, mc, sc, keep_residue=True)
        cp = props(collapsed)
        print(f"  Partition B (idem/else/top): void={sorted(vc)}, mid={sorted(mc)[:5]}..., sat={sorted(sc)}")
        print(f"    Collapsed: rank={cp['rank']}, det={cp['det']}, "
              f"jordan={cp['jordan']}, comm={cp['comm']}")

    # Scheme C: identity-absorbing
    part_C = partition_by_identity_absorbing(T)
    if part_C:
        vc, mc, sc = part_C
        collapsed = ternary_collapse_general(T, vc, mc, sc, keep_residue=True)
        cp = props(collapsed)
        print(f"  Partition C (id/middle/abs): void={sorted(vc)}, mid_size={len(mc)}, sat={sorted(sc)}")
        print(f"    Collapsed: rank={cp['rank']}, det={cp['det']}, "
              f"jordan={cp['jordan']}, comm={cp['comm']}")

