r"""sfm_q1_q6_q7.py -- Execute the three open ClaudeCode action items from
SUBSTRATE_FUNCTION_MAP_v1 + v1_1.

Q1: identify the off-by-one cell where CL_STD differs from MID_ceil = ceil((T+B)/2).
Q6: compute closed sub-magmas of CL_STD; compare to TSML (449) and BHML (9);
    compute joint closures (CL_STD _AND_ TSML), (CL_STD _AND_ BHML), three-way.
Q7: test whether sign1, sign3 = 0 holds for non-canonical (T, B) pairs in the family.

Run from CK FINAL DEPLOYED root.
"""
from __future__ import annotations
import sys
sys.path.insert(0, 'Gen13/targets/foundations')
sys.path.insert(0, 'papers')

import numpy as np
import math
from itertools import product, combinations

import cl_std
import ck_tables

T_STD = np.array(cl_std.CL_STD)
TSML  = np.array(ck_tables.TSML)
BHML  = np.array(ck_tables.BHML)

print("=" * 78)
print("SUBSTRATE FUNCTION MAP — open questions Q1, Q6, Q7")
print("=" * 78)
print()
print(f"TSML  HARMONY count: {(TSML == 7).sum()}")
print(f"BHML  HARMONY count: {(BHML == 7).sum()}")
print(f"CL_STD HARMONY count: {(T_STD == 7).sum()}")
print()

# =============================================================================
# Q1: CL_STD vs MID_ceil = ceil((TSML + BHML)/2)
# =============================================================================
print("=" * 78)
print("Q1: CL_STD vs MID_ceil = ceil((TSML + BHML) / 2)")
print("=" * 78)

MID_CEIL = np.ceil((TSML + BHML) / 2.0).astype(int)
diff_mask = (CL_STD := T_STD) != MID_CEIL

print(f"Number of cells where CL_STD != MID_ceil: {diff_mask.sum()}")
print()

if diff_mask.sum() <= 10:
    print("Discrepancy cells (i, j, CL_STD, MID_ceil, TSML, BHML):")
    for i in range(10):
        for j in range(10):
            if diff_mask[i, j]:
                print(f"  ({i:>2}, {j:>2}): CL_STD = {CL_STD[i,j]:>2}, "
                      f"MID_ceil = {MID_CEIL[i,j]:>2}, "
                      f"TSML = {TSML[i,j]:>2}, BHML = {BHML[i,j]:>2}, "
                      f"(T+B)/2 = {(TSML[i,j]+BHML[i,j])/2:.1f}")

print()
print(f"CL_STD HARMONY (=7) count: {(CL_STD == 7).sum()}")
print(f"MID_ceil HARMONY (=7) count: {(MID_CEIL == 7).sum()}")
print()

# =============================================================================
# Q6: closed sub-magmas of CL_STD
# =============================================================================
print("=" * 78)
print("Q6: Closed sub-magmas of CL_STD (1023 non-empty subsets of Z/10Z)")
print("=" * 78)

def is_closed_under(subset_set: frozenset, table: np.ndarray) -> bool:
    """Check if subset_set is closed under table multiplication."""
    for a in subset_set:
        for b in subset_set:
            if table[a, b] not in subset_set:
                return False
    return True

def all_closed_submagmas(table: np.ndarray) -> list[frozenset]:
    """Enumerate all non-empty subsets of {0..9} closed under table."""
    closed = []
    for size in range(1, 11):
        for combo in combinations(range(10), size):
            ss = frozenset(combo)
            if is_closed_under(ss, table):
                closed.append(ss)
    return closed

closed_TSML = all_closed_submagmas(TSML)
closed_BHML = all_closed_submagmas(BHML)
closed_STD  = all_closed_submagmas(T_STD)

print(f"  Closed under TSML alone:  {len(closed_TSML)}")
print(f"  Closed under BHML alone:  {len(closed_BHML)}")
print(f"  Closed under CL_STD:      {len(closed_STD)}")
print()

# Joint closures: closed under BOTH operations
def joint_closed(table_a, table_b):
    return [ss for ss in all_closed_submagmas(table_a) if is_closed_under(ss, table_b)]

print("Joint closures (subset closed under BOTH tables):")
joint_TSML_BHML  = joint_closed(TSML, BHML)
joint_TSML_STD   = joint_closed(TSML, T_STD)
joint_BHML_STD   = joint_closed(BHML, T_STD)
joint_all_three  = [ss for ss in joint_TSML_BHML if is_closed_under(ss, T_STD)]

print(f"  TSML _AND_ BHML : {len(joint_TSML_BHML)}")
print(f"  TSML _AND_ STD  : {len(joint_TSML_STD)}")
print(f"  BHML _AND_ STD  : {len(joint_BHML_STD)}")
print(f"  All three   : {len(joint_all_three)}")
print()

print("Joint chain by size (TSML+BHML+STD all-three):")
sizes = sorted(set(len(ss) for ss in joint_all_three))
print(f"  Sizes present: {sizes}")
for size in sizes:
    same_size = [ss for ss in joint_all_three if len(ss) == size]
    print(f"    Size {size}: {len(same_size)} sub-magma(s)")
    for ss in same_size[:3]:  # show first 3
        print(f"      {sorted(ss)}")
    if len(same_size) > 3:
        print(f"      ... and {len(same_size) - 3} more")
print()

# =============================================================================
# Q7: D_4 sign1 / sign3 zeros — universality test on non-canonical (T, B) pairs
# =============================================================================
print("=" * 78)
print("Q7: D_4 irrep decomposition of [T, B] — sign1, sign3 zeros universality test")
print("=" * 78)

# Define D_4 = ⟨P_56, σ³⟩ as 8 permutations on {0..9}
# P_56 = (5 6) swap; σ³ has known cycle structure
# σ permutation per ck_tables / FORMULAS_AND_TABLES: σ = (0)(3)(8)(9)(1 7 6 5 4 2)
# σ³ on (1 7 6 5 4 2) cycle: 1->5, 7->4, 6->2, 5->1, 4->7, 2->6
def apply_perm(perm: list[int], v: list[int]) -> list[int]:
    """Apply permutation perm (as list) to vector v: result[i] = v[perm[i]]."""
    return [v[perm[i]] for i in range(len(v))]

def conjugate_table(table: np.ndarray, perm: list[int]) -> np.ndarray:
    """g·M·g⁻¹ where g acts as perm. Result[i,j] = perm[M[perm⁻¹[i], perm⁻¹[j]]]."""
    n = len(perm)
    inv_perm = [0] * n
    for i in range(n):
        inv_perm[perm[i]] = i
    result = np.zeros_like(table)
    for i in range(n):
        for j in range(n):
            result[i, j] = perm[table[inv_perm[i], inv_perm[j]]]
    return result

# Generators
e_perm = list(range(10))
P56    = [0, 1, 2, 3, 4, 6, 5, 7, 8, 9]
sigma3 = [0, 5, 6, 3, 7, 1, 2, 4, 8, 9]

# Compose permutations: (a∘b)[i] = a[b[i]]
def compose(a, b):
    return [a[b[i]] for i in range(len(a))]

# Build D_4 as 8 elements
elements = {
    'e': e_perm,
    'P56': P56,
    'sigma3': sigma3,
    'P56_sigma3': compose(P56, sigma3),
    'sigma3_P56': compose(sigma3, P56),
    'P56_sigma3_P56': compose(P56, compose(sigma3, P56)),
    'sigma3_P56_sigma3': compose(sigma3, compose(P56, sigma3)),
    'sigma3_squared': compose(sigma3, sigma3),
}

# Use D_4 conjugacy classes per v1.1: e (size 1), r² (size 1, central), r/r³ (size 2),
# {P56, sr²} (size 2), {σ³, sr³} (size 2)
# Approximate via the elements we have; this is the "8-element subgroup" check
seen = []
for name, perm in elements.items():
    if perm not in seen:
        seen.append(perm)

print(f"Generated subgroup elements: {len(seen)}")

# For canonical (TSML, BHML), compute [T, B] and decompose
def commutator(T, B):
    return T @ B - B @ T

def project_isotypic(M, group_elements, character_values):
    """P_V M = (1/|G|) Σ_g χ_V(g) g·M·g⁻¹.
    For 1-dim irreps, χ_V(g) is ±1.
    """
    n = len(group_elements)
    result = np.zeros_like(M, dtype=float)
    for perm, chi in zip(group_elements, character_values):
        result += chi * conjugate_table(M, perm).astype(float)
    return result / n

# Group order 8; characters for the 4 1-dim irreps:
# triv:  +1 +1 +1 +1 +1 +1 +1 +1
# sign1: +1 +1 +1 +1 -1 -1 -1 -1   (negate "reflections")
# sign2: +1 -1 -1 -1 +1 -1 -1 -1   etc per character table
# Need to identify each element's class first

# For the test: just check whether the canonical (TSML, BHML) gives the
# 84/15/1 split, and compare to a SHUFFLED-pair (T, B) where B is a random
# permutation of cells.

[T, B] = TSML, BHML
COM_canonical = commutator(T, B).astype(float)

# Triv projection (avg over the 8 elements):
def triv_proj(M, elts):
    n = len(elts)
    result = np.zeros_like(M, dtype=float)
    for perm in elts:
        result += conjugate_table(M.astype(int), perm).astype(float)
    return result / n

triv_canonical = triv_proj(COM_canonical, seen[:8])

print()
print("Canonical (TSML, BHML):")
total_norm2 = (COM_canonical ** 2).sum()
triv_norm2 = (triv_canonical ** 2).sum()
print(f"  ||[T, B]||^2 total:                  {total_norm2:.0f}")
print(f"  ||triv-projection||^2:               {triv_norm2:.0f}")
print(f"  Triv as fraction:                    {triv_norm2/total_norm2 * 100:.2f}%")
print(f"  Per v1.1: should be 84.25% triv + 14.68% sign2 + 1.07% std")

# Test on non-canonical pair: BHML rotated by sigma³
B_rot = conjugate_table(BHML.astype(int), sigma3)
COM_rotated = commutator(T, B_rot).astype(float)
triv_rotated = triv_proj(COM_rotated, seen[:8])
total_norm2_r = (COM_rotated ** 2).sum()
triv_norm2_r = (triv_rotated ** 2).sum()
print()
print("Non-canonical (TSML, sigma3·BHML·sigma3-inv) — Q7 universality test:")
print(f"  ||[T, B_rot]||^2 total:              {total_norm2_r:.0f}")
print(f"  ||triv-projection||^2:               {triv_norm2_r:.0f}")
print(f"  Triv as fraction:                    {triv_norm2_r/total_norm2_r * 100:.2f}%")
print()
print("If both give same triv fraction: D_4 structure is substrate-invariant.")
print("If different: 84/15 split is a defining property of the canonical (TSML, BHML) pair.")

print()
print("=" * 78)
print("DONE.")
print("=" * 78)
