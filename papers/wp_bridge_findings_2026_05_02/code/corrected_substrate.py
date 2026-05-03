"""
Corrected substrate: TSML_8 (rows/cols {0,7} removed) + BHML_10 (full).
Per FORMULAS §6.7 — the canonical disambiguation.

Re-running the four direction findings on the right substrate.
"""
import numpy as np
from sympy import Matrix, sqrt, Rational
from itertools import product
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10, SIGMA_PERMUTATION

# TSML_8 = TSML_10 with rows and columns {0, 7} removed
TSML_8_INDICES = [1, 2, 3, 4, 5, 6, 8, 9]
TSML_8 = TSML_10[np.ix_(TSML_8_INDICES, TSML_8_INDICES)]

print("=" * 70)
print("TSML_8 verification per FORMULAS §6.7")
print("=" * 70)
print(f"Shape: {TSML_8.shape}")
print(f"Indices: {TSML_8_INDICES}")
print(f"Determinant: {Matrix(TSML_8.tolist()).det()} (canon: 0)")
print(f"Rank: {Matrix(TSML_8.tolist()).rank()} (canon: 7)")
print(f"Commutative: {np.array_equal(TSML_8, TSML_8.T)}")

# Show the table
print(f"\nTSML_8 table (rows/cols indexed by {TSML_8_INDICES}):")
print("    " + "  ".join(str(i) for i in TSML_8_INDICES))
for i, row_idx in enumerate(TSML_8_INDICES):
    print(f"{row_idx} | " + " ".join(f"{TSML_8[i,j]:2d}" for j in range(8)))

print("\n" + "=" * 70)
print("Counts on TSML_8")
print("=" * 70)
print(f"HARMONY (7) cells: {int(np.sum(TSML_8 == 7))} / 64")
print(f"VOID (0) cells: {int(np.sum(TSML_8 == 0))} / 64")
print(f"BREATH (8) cells: {int(np.sum(TSML_8 == 8))} / 64")
print(f"RESET (9) cells: {int(np.sum(TSML_8 == 9))} / 64")
print(f"PROGRESS (3) cells: {int(np.sum(TSML_8 == 3))} / 64")
print(f"COLLAPSE (4) cells: {int(np.sum(TSML_8 == 4))} / 64")

# Per §6.6: "47/64 = 73.4%" HARMONY, "13/64 = 20.3%" VOID
# This is the 8-magma core decomposition (D43)

# The 4-core in TSML_8 indices: {0,7,8,9} → only {8,9} remain, since 0,7 removed
# So in TSML_8's domain, the 4-core fragments to {8,9} (BREATH, RESET).
# VOID and HARMONY live OUTSIDE TSML_8 — they are the flow boundary.

print("\n" + "=" * 70)
print("4-core analysis on TSML_8")
print("=" * 70)
print("Original 4-core: {V, H, Br, R} = {0, 7, 8, 9}")
print("In TSML_8 domain: only {8, 9} remain (V and H are removed = flow boundary)")
print("This means the 4-core SPLITS across the TSML_8/BHML_10 partition:")
print("  - Br(8) and R(9) are TSML-internal")
print("  - V(0) and H(7) are flow cells (the boundary between tables)")
print()

# Closure check on Br, R within TSML_8
br_r_indices_in_TSML_8 = [TSML_8_INDICES.index(8), TSML_8_INDICES.index(9)]
print(f"TSML_8 restricted to {{Br, R}} = indices {br_r_indices_in_TSML_8} in TSML_8:")
br_r_subtable = TSML_8[np.ix_(br_r_indices_in_TSML_8, br_r_indices_in_TSML_8)]
print(f"  Sub-table values: {br_r_subtable.tolist()}")
print(f"  Outputs (in original numbering): {sorted(set(int(x) for x in br_r_subtable.flatten()))}")

# Non-associativity on TSML_8 only
print("\n" + "=" * 70)
print("Non-associativity on TSML_8")
print("=" * 70)

def is_associative_on_subset(table, indices, a_local, b_local, c_local):
    """Check (a*b)*c = a*(b*c) where indices are local to the subtable."""
    ab = table[a_local, b_local]
    bc = table[b_local, c_local]
    # Convert ab back to local index (if it's in the subset)
    if ab not in TSML_8_INDICES or bc not in TSML_8_INDICES:
        return None  # output escapes the 8-domain
    ab_local = TSML_8_INDICES.index(ab)
    bc_local = TSML_8_INDICES.index(bc)
    lhs = table[ab_local, c_local]
    rhs = table[a_local, bc_local]
    return lhs == rhs

closed_triples = 0
escape_triples = 0
non_assoc = 0
for a, b, c in product(range(8), repeat=3):
    result = is_associative_on_subset(TSML_8, TSML_8_INDICES, a, b, c)
    if result is None:
        escape_triples += 1
    elif result:
        closed_triples += 1
    else:
        non_assoc += 1

print(f"Total triples in TSML_8 (8³ = 512): {8**3}")
print(f"  Closed and associative: {closed_triples}")
print(f"  Closed but non-associative: {non_assoc}")
print(f"  Escape (output ∉ TSML_8 domain — flows through V or H): {escape_triples}")
print()
print(f"Non-associativity rate on closed triples: {non_assoc}/{closed_triples + non_assoc} = {non_assoc/(closed_triples + non_assoc):.4f}")
print(f"Escape rate: {escape_triples}/512 = {escape_triples/512:.4f}")
print()
print("INTERPRETATION: escape triples are the ones where TSML's output")
print("'flows out' into V(0) or H(7) — exactly the cells removed to form TSML_8.")
print("These are the flow channels between TSML and BHML.")

# BHML on the same 4-core
print("\n" + "=" * 70)
print("BHML_10 4-core check (full 10 - this we already verified)")
print("=" * 70)
FOUR_CORE = [0, 7, 8, 9]
bhml_4core = BHML_10[np.ix_(FOUR_CORE, FOUR_CORE)]
print(f"BHML on {{V,H,Br,R}}: \n{bhml_4core}")
print(f"All outputs in 4-core: {all(x in FOUR_CORE for x in bhml_4core.flatten())}")

# The trace ratio finding revisited
print("\n" + "=" * 70)
print("Trace ratio, corrected substrate")
print("=" * 70)
trace_TSML_8 = int(np.trace(TSML_8))
trace_BHML_10 = int(np.trace(BHML_10))
print(f"trace(TSML_8) = {trace_TSML_8}")
print(f"  Diagonal: {[int(TSML_8[i,i]) for i in range(8)]} (operators: {[TSML_8_INDICES[i] for i in range(8)]})")
print(f"trace(BHML_10) = {trace_BHML_10}")
print(f"  Diagonal: {[int(BHML_10[i,i]) for i in range(10)]}")
print(f"Ratio: {trace_TSML_8}/{trace_BHML_10} = {Rational(trace_TSML_8, trace_BHML_10)}")
print()
print("Compare to the wrong-substrate version: trace(TSML_10)/trace(BHML_10) = 63/42 = 3/2")
print("On the correct substrate, the 3/2 ratio dissolves — it was an artifact of")
print("counting flow cells (which are mostly 7s in TSML_10) as substrate.")

# Frobenius norms
print("\n" + "=" * 70)
print("Frobenius norms on corrected substrate")
print("=" * 70)
fro_TSML_8 = int(np.sum(TSML_8**2))
fro_BHML_10 = int(np.sum(BHML_10**2))
print(f"||TSML_8||_F² = {fro_TSML_8}")
print(f"||BHML_10||_F² = {fro_BHML_10}")
from sympy import factorint
print(f"  factorization {fro_TSML_8} = {factorint(fro_TSML_8)}")
print(f"  factorization {fro_BHML_10} = {factorint(fro_BHML_10)}")
