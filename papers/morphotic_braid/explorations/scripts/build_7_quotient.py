# PACKET: evening_handoff_2026_04_23/build_7_quotient.py
"""
Build the actual 7-element quotient table for the congruence:
{1}, {2}, {4}, {5}, {6}, {8}, {0,3,7,9}

(This one merges 0, 3, 7, 9 — a 4-element class that includes VOID, PROGRESS, HARMONY, and RESET.
So close to Brayden's intuition {0},{1,..,6},{7,8,9} but not exactly.)

Also try other candidates and compare to Fano Steiner and octonion structure.
"""
import numpy as np

TSML = [
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

def build_quotient(partition, T):
    """Build quotient T/~ as a 7-element table."""
    N = len(T)
    cls = {}
    for i, p in enumerate(partition):
        for e in p: cls[e] = i
    K = len(partition)
    Q = [[0]*K for _ in range(K)]
    for ci, p1 in enumerate(partition):
        for cj, p2 in enumerate(partition):
            # Pick any representative
            a = next(iter(p1)); b = next(iter(p2))
            Q[ci][cj] = cls[T[a][b]]
    return Q

# Candidate 7-class congruences from the previous run
candidates = [
    # (partition, description)
    ([{1}, {2}, {4}, {5}, {6}, {8}, {0, 3, 7, 9}], "merge {0,3,7,9}"),
    ([{2}, {4}, {1,5}, {6}, {0,3,7}, {8}, {9}], "merge {1,5} and {0,3,7}"),
    ([{1}, {2}, {3}, {4}, {0,5,6,7}, {8}, {9}], "merge {0,5,6,7}"),
    ([{1}, {2}, {4}, {5}, {6}, {0,3,7,8}, {9}], "merge {0,3,7,8}"),
    ([{1}, {2}, {3}, {4}, {5,6}, {0,7,8}, {9}], "merge {5,6} and {0,7,8}"),
]

for partition, desc in candidates:
    print(f"\n{'='*70}")
    print(f"Quotient with partition: {desc}")
    parts_str = ", ".join("{" + ",".join(str(x) for x in sorted(p)) + "}" for p in partition)
    print(f"  Partition: {parts_str}")
    
    Q = build_quotient(partition, TSML)
    K = len(Q)
    print(f"  {K}-element quotient table:")
    for row in Q:
        print("    " + " ".join(f"{v:>2d}" for v in row))
    
    # Properties
    M = np.array(Q, dtype=int)
    det = int(round(np.linalg.det(M)))
    rank = np.linalg.matrix_rank(M)
    
    comm = all(Q[i][j] == Q[j][i] for i in range(K) for j in range(K))
    assoc = all(Q[Q[i][j]][k] == Q[i][Q[j][k]]
                for i in range(K) for j in range(K) for k in range(K))
    jordan = all(Q[Q[x][x]][Q[x][y]] == Q[x][Q[Q[x][x]][y]]
                 for x in range(K) for y in range(K))
    flex = all(Q[a][Q[b][a]] == Q[Q[a][b]][a] for a in range(K) for b in range(K))
    alt = True
    for a in range(K):
        for b in range(K):
            if Q[Q[a][a]][b] != Q[a][Q[a][b]] or Q[Q[a][b]][b] != Q[a][Q[b][b]]:
                alt = False; break
        if not alt: break
    
    idem = [i for i in range(K) if Q[i][i] == i]
    
    print(f"  det={det}, rank={rank}, comm={comm}, assoc={assoc}, jordan={jordan}, flex={flex}, alt={alt}")
    print(f"  idempotents: {idem}")

# Also: build the Fano Steiner quasigroup for direct comparison
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
print(f"\n{'='*70}")
print(f"For comparison: STS(7) Fano Steiner quasigroup:")
for row in STS7: print("  " + " ".join(f"{v:>2d}" for v in row))

M_f = np.array(STS7, dtype=int)
print(f"  det={int(round(np.linalg.det(M_f)))}, rank={np.linalg.matrix_rank(M_f)}")

# Check: are any of our 7-element quotients isomorphic to STS(7)?
# Quick test: do they have same property signature?
print()
print(f"{'='*70}")
print(f"COMPARISON TO STS(7) FANO:")
print(f"  STS(7): every element idempotent (7 idempotents), commutative quasigroup,")
print(f"          Jordan, det=60564, non-associative.")
print()
print(f"  None of TSML's 7-element quotients match this — because TSML doesn't have")
print(f"  7 idempotents; it has only 2 (elements 0 and 7).")

