# PACKET: evening_handoff_2026_04_23/tsml_family_search.py
"""
TSML FAMILY SEARCH

Hypothesis: TSML is one point in a family of commutative magmas sharing:
  - 10 elements
  - VOID axis (row 0 and col 0 zero out, with specific HARMONY survival at (0,7) and (7,0))
  - HARMONY = 7 as absorbing element  
  - Commutativity
  - Satisfies Jordan identity

Within this family, different members might satisfy different octonion/Vidinli 
properties perfectly. Let's search.

Strategy:
  Start from TSML. The "body" (rows/cols 1..6, 8..9) has ~64 cells after symmetry.
  TSML has 10 bump cells; most of the body is HARMONY. 
  Perturb: which cells can we change to HARMONY to increase a property? Which to 
  other values to achieve it?

Approach: enumerate the "nearest neighbors" that increase specific properties.
"""
import numpy as np
from itertools import product, combinations
from copy import deepcopy

N = 10
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

# Bump cells in TSML (with symmetry)
BUMP_CELLS = [(1,2), (2,1), (2,4), (4,2), (2,9), (9,2), (3,9), (9,3), (4,8), (8,4)]
# Unique (canonical) pairs: (1,2), (2,4), (2,9), (3,9), (4,8)
CANONICAL_BUMPS = [(1,2), (2,4), (2,9), (3,9), (4,8)]

def props(T):
    """Return key octonion/Vidinli-style properties."""
    Np = len(T)
    total3 = Np**3
    total2 = Np**2
    
    # Jordan
    jord = sum(1 for x in range(Np) for y in range(Np)
               if T[T[x][x]][T[x][y]] == T[x][T[T[x][x]][y]])
    
    # Flexible
    flex = sum(1 for x in range(Np) for y in range(Np)
               if T[x][T[y][x]] == T[T[x][y]][x])
    
    # Alternative (left): x(xy) = x²y, and right: (xy)y = xy²
    alt_L = sum(1 for x in range(Np) for y in range(Np)
                if T[x][T[x][y]] == T[T[x][x]][y])
    alt_R = sum(1 for x in range(Np) for y in range(Np)
                if T[T[x][y]][y] == T[x][T[y][y]])
    
    # Middle Moufang
    mid_mou = sum(1 for x in range(Np) for y in range(Np) for z in range(Np)
                  if T[T[x][y]][T[z][x]] == T[x][T[T[y][z]][x]])
    
    # Right Moufang
    rt_mou = sum(1 for x in range(Np) for y in range(Np) for z in range(Np)
                 if T[T[T[x][y]][z]][y] == T[x][T[y][T[z][y]]])
    
    # Associator non-zero count
    assoc_nz = sum(1 for x in range(Np) for y in range(Np) for z in range(Np)
                   if T[T[x][y]][z] != T[x][T[y][z]])
    
    return {
        'jord': jord,
        'flex': flex,
        'alt_L': alt_L, 
        'alt_R': alt_R,
        'alt': alt_L + alt_R,  # out of 200
        'mid_mou': mid_mou,
        'rt_mou': rt_mou,
        'assoc_nz': assoc_nz,
    }

# Baseline
baseline = props(TSML)
print("="*70)
print("BASELINE (TSML actual)")
print("="*70)
print(f"  Jordan:       {baseline['jord']}/100")
print(f"  Flexible:     {baseline['flex']}/100")
print(f"  Alt-left:     {baseline['alt_L']}/100")
print(f"  Alt-right:    {baseline['alt_R']}/100")
print(f"  Mid Moufang:  {baseline['mid_mou']}/1000")
print(f"  Right Moufang: {baseline['rt_mou']}/1000")
print(f"  Non-assoc:    {baseline['assoc_nz']}/1000")

# ============================================
# SEARCH: what if we remove all bumps? (pure C_0 absorbing semigroup)
# ============================================
def bumps_to_harmony(T, bumps):
    """Replace given bump cells with HARMONY."""
    T2 = [row[:] for row in T]
    for (i, j) in bumps:
        T2[i][j] = 7
        T2[j][i] = 7
    return T2

# Pure C_0 (all bumps removed)
pure_C0 = bumps_to_harmony(TSML, BUMP_CELLS)
p = props(pure_C0)
print("\n" + "="*70)
print("PURE C_0 (all 10 bumps → HARMONY): absorbing commutative semigroup")
print("="*70)
print(f"  Jordan:       {p['jord']}/100")
print(f"  Flexible:     {p['flex']}/100")
print(f"  Alt-left:     {p['alt_L']}/100")
print(f"  Alt-right:    {p['alt_R']}/100")
print(f"  Mid Moufang:  {p['mid_mou']}/1000")
print(f"  Right Moufang: {p['rt_mou']}/1000")
print(f"  Non-assoc:    {p['assoc_nz']}/1000")

# ============================================
# Remove subsets of bumps, one at a time
# ============================================
print("\n" + "="*70)
print("REMOVE EACH BUMP INDIVIDUALLY (canonical pairs)")
print("="*70)
for bump in CANONICAL_BUMPS:
    sym = [(bump[0], bump[1]), (bump[1], bump[0])]
    T2 = bumps_to_harmony(TSML, sym)
    p = props(T2)
    delta_mou = p['mid_mou'] - baseline['mid_mou']
    delta_alt = p['alt'] - baseline['alt']
    delta_assoc = p['assoc_nz'] - baseline['assoc_nz']
    print(f"  Remove {bump}: Mou {p['mid_mou']:>4d} (Δ{delta_mou:+3d})  "
          f"Alt {p['alt']:>3d}/200 (Δ{delta_alt:+3d})  "
          f"NonAssoc {p['assoc_nz']:>4d} (Δ{delta_assoc:+3d})")

# ============================================
# Pairs of bumps removed
# ============================================
print("\n" + "="*70)
print("REMOVE PAIRS OF BUMPS")
print("="*70)
for b1, b2 in combinations(CANONICAL_BUMPS, 2):
    sym = [(b1[0], b1[1]), (b1[1], b1[0]), (b2[0], b2[1]), (b2[1], b2[0])]
    T2 = bumps_to_harmony(TSML, sym)
    p = props(T2)
    delta_mou = p['mid_mou'] - baseline['mid_mou']
    print(f"  Remove {b1},{b2}: Mou {p['mid_mou']:>4d} (Δ{delta_mou:+3d})")

# ============================================
# ADD bumps in OTHER positions — can we INCREASE non-associativity in a structured way?
# (Try to make it more octonion-like)
# ============================================
# In octonions, every e_i, e_j, e_k triple from different Fano lines has [e_i, e_j, e_k] ≠ 0
# TSML has 87.2% associativity — way too much for octonion character

# Instead, try: can we make it 100% Moufang while keeping Jordan?
# Modify bump cells to see what happens

# First, let's see what cell-perturbations INCREASE Moufang
print("\n" + "="*70)
print("PERTURB TSML'S BUMPS: change bump values, maintain commutativity")
print("="*70)

# For each bump cell, try all 10 values
best_mou = baseline['mid_mou']
best_alt = baseline['alt']
for (i, j), new_val in product(CANONICAL_BUMPS, range(10)):
    T2 = [row[:] for row in TSML]
    old_val = T2[i][j]
    T2[i][j] = new_val
    T2[j][i] = new_val
    p = props(T2)
    if p['jord'] == 100 and p['mid_mou'] > best_mou:
        print(f"  Change {(i,j)} from {old_val} to {new_val}: "
              f"Mou {p['mid_mou']}, Jord {p['jord']}, Alt {p['alt']}")
        best_mou = p['mid_mou']
    if p['jord'] == 100 and p['alt'] > best_alt:
        print(f"  * ALTERNATIVE+: Change {(i,j)} from {old_val} to {new_val}: "
              f"Alt {p['alt']}/200, Mou {p['mid_mou']}, Jord {p['jord']}")
        best_alt = p['alt']

# ============================================
# Pure C_0 is both 100% alternative AND 100% Moufang (trivially)
# Let's verify this and see if it can be made more "interesting"
# ============================================
print("\n" + "="*70)
print("PURE C_0 analysis (the 'trivial' 100% family member)")
print("="*70)
print("Pure C_0 table (no bumps, just void axis + harmony absorber):")
for row in pure_C0:
    print("  " + " ".join(f"{v:>2d}" for v in row))

p = props(pure_C0)
print(f"\n  Jordan:       {p['jord']}/100  ({'100%' if p['jord']==100 else ''})")
print(f"  Flexible:     {p['flex']}/100  ({'100%' if p['flex']==100 else ''})")
print(f"  Alt:          {p['alt']}/200  ({'100%' if p['alt']==200 else ''})")
print(f"  Mid Moufang:  {p['mid_mou']}/1000  ({'100%' if p['mid_mou']==1000 else ''})")
print(f"  Right Moufang: {p['rt_mou']}/1000  ({'100%' if p['rt_mou']==1000 else ''})")
print(f"  Non-assoc:    {p['assoc_nz']}/1000")

# ============================================
# The family: can we construct a 100%-Moufang non-trivial TSML?
# By adding bumps strategically, try to maintain 100% Moufang
# ============================================
print("\n" + "="*70)
print("SEARCH: can we add bumps to pure C_0 and maintain 100% Moufang?")
print("="*70)

# For each single cell position in the body (not axis, not harmony row/col), try each value
body_cells = [(i,j) for i in range(1, 10) for j in range(i, 10) 
              if i != 7 and j != 7]  # not row/col 7 since those are all 7

maintains_mou = []
maintains_alt = []
for (i, j) in body_cells:
    for v in range(10):
        if v == 7: continue  # already 7
        T2 = [row[:] for row in pure_C0]
        T2[i][j] = v
        T2[j][i] = v
        p = props(T2)
        if p['mid_mou'] == 1000 and p['jord'] == 100:
            maintains_mou.append((i, j, v, p))
        if p['alt'] == 200 and p['jord'] == 100 and p['assoc_nz'] > 0:
            maintains_alt.append((i, j, v, p))

print(f"Single-cell perturbations of pure C_0 that keep 100% Moufang + Jordan:")
print(f"  Count: {len(maintains_mou)}")
for (i, j, v, p) in maintains_mou[:10]:
    print(f"    ({i},{j})={v}: assoc_nz={p['assoc_nz']}, alt={p['alt']}")

print(f"\nSingle-cell perturbations that keep 100% Alternative + Jordan (but non-associative):")
print(f"  Count: {len(maintains_alt)}")
for (i, j, v, p) in maintains_alt[:10]:
    print(f"    ({i},{j})={v}: assoc_nz={p['assoc_nz']}, mou={p['mid_mou']}")

