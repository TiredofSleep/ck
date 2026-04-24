# PACKET: evening_handoff_2026_04_23/forcing_collapse.py
"""
Forcing variant: VOID stays, SAT stays, mid class → SAT value (absorbed).
This is what TIG actually does.

Run across partition choices to see which produce "interesting" collapsed tables.
"""
import numpy as np
from collections import Counter
from itertools import combinations

def ternary_force_collapse(T, void_class, sat_class, sat_val=None, void_val=None):
    N = len(T)
    if sat_val is None and sat_class: sat_val = list(sat_class)[0]
    if void_val is None and void_class: void_val = list(void_class)[0]
    if sat_val is None: sat_val = 0
    if void_val is None: void_val = 0
    out = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            v = T[i][j]
            if v in void_class: out[i][j] = void_val
            elif v in sat_class: out[i][j] = sat_val
            else: out[i][j] = sat_val  # force mid to sat
    return out

def props(T):
    N = len(T)
    M = np.array(T, dtype=int)
    det = int(round(np.linalg.det(M)))
    rank = int(np.linalg.matrix_rank(M))
    max_val = max(max(row) for row in T) if T else 0
    valid_indices = max_val < N
    comm = all(T[i][j] == T[j][i] for i in range(N) for j in range(N))
    
    if valid_indices:
        try:
            assoc = all(T[T[i][j]][k] == T[i][T[j][k]]
                       for i in range(N) for j in range(N) for k in range(N))
            jordan = all(T[T[x][x]][T[x][y]] == T[x][T[T[x][x]][y]]
                        for x in range(N) for y in range(N))
            flex = all(T[a][T[b][a]] == T[T[a][b]][a] for a in range(N) for b in range(N))
            alt = True
            for a in range(N):
                for b in range(N):
                    if T[T[a][a]][b] != T[a][T[a][b]] or T[T[a][b]][b] != T[a][T[b][b]]:
                        alt = False; break
                if not alt: break
        except:
            assoc = jordan = flex = alt = "err"
    else:
        assoc = jordan = flex = alt = "n/a"
    
    return {'det': det, 'rank': rank, 'comm': comm, 'assoc': assoc, 
            'jordan': jordan, 'flex': flex, 'alt': alt}

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
Z5_mul = [[(i*j)%5 for j in range(5)] for i in range(5)]
STS7 = fano()
Z7_mul = [[(i*j)%7 for j in range(7)] for i in range(7)]
Z8_mul = [[(i*j)%8 for j in range(8)] for i in range(8)]

# Q8 quaternion
def q8_table():
    elements = [(+1,0),(-1,0),(+1,1),(-1,1),(+1,2),(-1,2),(+1,3),(-1,3)]
    def mul(a, b):
        s_a, x_a = a; s_b, x_b = b
        s = s_a * s_b
        if x_a == 0: return (s, x_b)
        if x_b == 0: return (s, x_a)
        if x_a == x_b: return (-s, 0)
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

tables = [
    ("Klein V4", V4, 4),
    ("Z/5Z mul", Z5_mul, 5),
    ("STS(7) Fano", STS7, 7),
    ("Z/7Z mul", Z7_mul, 7),
    ("Z/8Z mul", Z8_mul, 8),
    ("Q8 quaternion", Q8, 8),
]

# For each table, try ALL 2-element partitions (z, s) for VOID/SAT
# and see which produce interesting results
print("="*95)
print("EXHAUSTIVE (z, s) PARTITION SEARCH — FORCE-COLLAPSE")
print("="*95)
print("For each celebrated table, try every (void, sat) pair and report collapse properties.")
print()

for (name, T, N) in tables:
    print(f"\n--- {name} (N={N}) ---")
    src = props(T)
    print(f"  Source: rank={src['rank']}, det={src['det']}, comm={src['comm']}, "
          f"assoc={src['assoc']}, jordan={src['jordan']}")
    
    jordan_hits = []
    non_singular_hits = []
    for z in range(N):
        for s in range(N):
            if z == s: continue
            C = ternary_force_collapse(T, {z}, {s}, sat_val=s, void_val=z)
            cp = props(C)
            if cp['jordan'] is True:
                jordan_hits.append((z, s, cp['det'], cp['rank']))
            if cp['det'] != 0:
                non_singular_hits.append((z, s, cp['det'], cp['jordan']))
    
    print(f"  (z, s) pairs giving Jordan-after-collapse: {len(jordan_hits)}")
    print(f"  (z, s) pairs giving non-singular collapse: {len(non_singular_hits)}")
    
    # Show non-singular Jordan hits (the most interesting ones)
    both = [(z, s, det, rank) for (z, s, det, rank) in jordan_hits if det != 0]
    if both:
        print(f"  Non-singular Jordan collapses:")
        for (z, s, det, rank) in both[:10]:
            print(f"    (z={z}, s={s}): det={det}, rank={rank}")
    
    # Interesting non-singular results regardless of Jordan
    if non_singular_hits:
        # Sort by |det| ascending
        non_singular_hits.sort(key=lambda x: abs(x[2]))
        print(f"  Smallest-|det| non-singular collapse(s):")
        for (z, s, det, jord) in non_singular_hits[:3]:
            print(f"    (z={z}, s={s}): det={det}, jordan={jord}")

