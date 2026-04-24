<!-- PACKET: evening_handoff_2026_04_23/ternary_collapse.py -->
"""
TERNARY COLLAPSE OPERATOR (BHML → TSML direction)

Definition:
  Given a table T on N elements with designated void z and harmony h:
  
  TSML[i][j] = 
    0 (void)       if T[i][j] == z
    h (harmony)    if T[i][j] == h
    T[i][j]        otherwise   (bump — preserve residue)

The third clause ("preserve residue") is what makes this interesting.
Simple version: just keep non-void non-harmony cells as-is.
Stronger version: apply a specific "bump flavor" rule.

Test:
1. Does this reproduce TSML when applied to actual BHML?
2. Apply to celebrated tables (treating them as BHML-analogs).
"""
import numpy as np

N = 10
HARMONY = 7
VOID = 0

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

BHML = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7],
    [5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],
    [7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]

def ternary_collapse_naive(T, z=0, h=None):
    """Naive version: keep void, keep harmony, preserve non-(z,h) values."""
    N = len(T)
    if h is None: h = N - 3
    return [[T[i][j] if T[i][j] in {z, h} else T[i][j] for j in range(N)] for i in range(N)]

def ternary_collapse_absorbing(T, z=0, h=None):
    """Absorbing version: void stays, harmony stays, everything else → harmony."""
    N = len(T)
    if h is None: h = N - 3
    return [[z if T[i][j] == z else (h if T[i][j] != z else z) for j in range(N)] for i in range(N)]

def ternary_collapse_with_residue(T, z=0, h=None):
    """
    Collapse that preserves a specific 'bump residue' pattern.
    
    For each cell (i,j) where T[i][j] != z and T[i][j] != h:
    - If TSML would have harmony at (i,j), output harmony
    - Otherwise output the original residue
    
    But that requires knowing TSML... which defeats the purpose.
    
    Let's try: collapse if not in {z, h}, preserve residue value.
    """
    N = len(T)
    if h is None: h = N - 3
    out = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            v = T[i][j]
            if v == z: out[i][j] = z
            elif v == h: out[i][j] = h
            else: out[i][j] = v  # preserve residue
    return out

# TEST 1: does naive collapse of BHML reproduce TSML?
print("="*75)
print("TEST 1: Naive ternary collapse of actual BHML vs actual TSML")
print("="*75)

collapse_simple = ternary_collapse_absorbing(BHML, z=0, h=7)
print("\nNaive absorbing collapse (everything non-z becomes h):")
print(f"{'Match to TSML:':30s}", end='')
match = sum(1 for i in range(10) for j in range(10) if collapse_simple[i][j] == TSML[i][j])
print(f" {match}/100")

# Structured collapse with residue
collapse_residue = ternary_collapse_with_residue(BHML, z=0, h=7)
print("\nResidue-preserving collapse of BHML:")
for row in collapse_residue:
    print("  " + " ".join(f"{v:>2d}" for v in row))
print("\nActual TSML:")
for row in TSML:
    print("  " + " ".join(f"{v:>2d}" for v in row))

match = sum(1 for i in range(10) for j in range(10) if collapse_residue[i][j] == TSML[i][j])
print(f"\nMatch rate: {match}/100")

diffs = [(i, j, collapse_residue[i][j], TSML[i][j]) 
         for i in range(10) for j in range(10) 
         if collapse_residue[i][j] != TSML[i][j]]
print(f"Differing cells: {len(diffs)}")
if diffs[:15]:
    print("First 15 differences (i, j, collapse, TSML):")
    for (i,j,c,t) in diffs[:15]:
        print(f"  ({i},{j}): residue-collapse={c}, actual TSML={t}")

# So the naive residue-preserving collapse doesn't exactly reproduce TSML.
# There's a more specific rule. Let me analyze:
print()
print("="*75)
print("Where does TSML have 7 but BHML has non-7 non-0?")
print("="*75)
absorbed_cells = []
for i in range(10):
    for j in range(10):
        if TSML[i][j] == 7 and BHML[i][j] not in {0, 7}:
            absorbed_cells.append((i, j, BHML[i][j]))
print(f"Cells where TSML absorbs BHML value to 7: {len(absorbed_cells)}")
for (i, j, v) in absorbed_cells[:15]:
    print(f"  ({i},{j}): BHML={v} → TSML=7")

# Cells where TSML preserved BHML's non-(0,7) value:
preserved = []
for i in range(10):
    for j in range(10):
        if TSML[i][j] not in {0, 7} and BHML[i][j] not in {0, 7}:
            preserved.append((i, j, BHML[i][j], TSML[i][j]))
print(f"\nCells where TSML preserves BHML residue: {len(preserved)}")
for (i, j, b, t) in preserved:
    same = "(same)" if b == t else f"(BHML={b}, TSML={t})"
    print(f"  ({i},{j}): BHML={b}, TSML={t} {same}")

