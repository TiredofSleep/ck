"""
TSML_8 associativity on the 9 corrected-frame trefoils.

TSML_8 only acts on indices {1,2,3,4,5,6,8,9}. Triples involving V (0) or H (7)
need V/H treated as flow boundary — TSML_8 doesn't have output values for them.

The 9 corrected-frame trefoils all involve V (0) and most involve H (7).
So associativity in the strict TSML_8 sense doesn't directly apply.

What does apply: BHML_10 associativity on the full 10-element set.
And: TSML_8 associativity on triples that stay entirely in TSML_8's domain.
"""
import numpy as np
from itertools import product
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10

TSML_8_INDICES = [1, 2, 3, 4, 5, 6, 8, 9]
TSML_8 = TSML_10[np.ix_(TSML_8_INDICES, TSML_8_INDICES)]
FLOW_CELLS = {0, 7}

# 9 corrected-frame trefoils
TREFOIL_9 = [
    (0,7,8), (0,8,7), (0,8,8),
    (7,0,8), (7,8,0),
    (8,0,7), (8,0,8), (8,7,0), (8,8,0),
]


def tsml8_associative(t):
    """Is (a,b,c) TSML_8-associative? Requires all elements + intermediate
    products to be in TSML_8's domain."""
    a, b, c = t
    if a in FLOW_CELLS or b in FLOW_CELLS or c in FLOW_CELLS:
        return None  # not in TSML_8 domain
    a_l, b_l, c_l = (TSML_8_INDICES.index(x) for x in t)
    ab = int(TSML_8[a_l, b_l])
    bc = int(TSML_8[b_l, c_l])
    if ab in FLOW_CELLS or bc in FLOW_CELLS:
        return None  # intermediate escapes domain
    ab_l = TSML_8_INDICES.index(ab)
    bc_l = TSML_8_INDICES.index(bc)
    left = int(TSML_8[ab_l, c_l])
    right = int(TSML_8[a_l, bc_l])
    return left == right


def bhml_associative(t):
    a, b, c = t
    left = int(BHML_10[int(BHML_10[a, b]), c])
    right = int(BHML_10[a, int(BHML_10[b, c])])
    return left == right


def main():
    print("=" * 70)
    print("ASSOCIATIVITY ANALYSIS ON CORRECTED FRAME")
    print("=" * 70)
    
    print("\n  9 trefoil triples (corrected frame):")
    print("  All involve V (0); most involve H (7) or B (8)")
    print(f"\n  {'Triple':<10} {'TSML_8':<10} {'BHML_10':<10}")
    
    for t in TREFOIL_9:
        ts8 = tsml8_associative(t)
        bh = bhml_associative(t)
        ts8_str = "N/A (flow)" if ts8 is None else ("✓" if ts8 else "✗")
        bh_str = "✓" if bh else "✗"
        print(f"  {str(t):<10} {ts8_str:<10} {bh_str:<10}")
    
    # All 9 trefoils involve V (0), so TSML_8-associativity is N/A for all of them
    # Check BHML_10 status only
    bhml_assoc_count = sum(1 for t in TREFOIL_9 if bhml_associative(t))
    print(f"\n  BHML_10-associative trefoils: {bhml_assoc_count}/9")
    
    # Check the 9 trefoils' multiset structure
    from collections import Counter
    multisets = Counter(tuple(sorted(t)) for t in TREFOIL_9)
    print(f"\n  Multiset classes:")
    for ms, count in sorted(multisets.items()):
        print(f"    {ms}: {count} permutations")
    
    # Are these the (V, H, Br) and (V, Br, Br) multisets?
    print(f"\n  Element distribution in 9 trefoils:")
    elem_count = Counter()
    for t in TREFOIL_9:
        for x in t:
            elem_count[x] += 1
    for e, c in sorted(elem_count.items()):
        names = {0: 'VOID', 7: 'HARMONY', 8: 'BREATH'}
        print(f"    {e} ({names.get(e, '?')}): {c}")
    
    # All 27 cells: VOID 9, HARMONY 6, BREATH 12
    # So trefoils on corrected frame are V/H/Br-only, with BREATH dominant
    
    print("\n" + "=" * 70)
    print("STRUCTURAL CHARACTERIZATION ATTEMPT")
    print("=" * 70)
    
    # Hypothesis: trefoils on corrected frame are EXACTLY the triples whose
    # multiset is {V, H, Br} or {V, Br, Br}
    print("""
The 9 trefoils on the corrected frame form 2 multiset classes:
  {V, H, Br} = (0, 7, 8) — all 6 permutations
  {V, Br, Br} = (0, 8, 8) — all 3 permutations

ELEMENT distribution: 
  VOID (0): 9 occurrences (in every trefoil)
  HARMONY (7): 6 occurrences (in 6 of 9)
  BREATH (8): 12 occurrences (in every trefoil, 1.33 per triple)

Conjecture: Trefoils on corrected substrate are triples where:
  - VOID is in every triple (the puncture)
  - BREATH appears at least once (the dynamic operator)
  - Either HARMONY (cusp) or another BREATH appears
  - No element from {1, 2, 3, 4, 5, 6, 9} appears

This is structurally:
  trefoil = V × {H, Br} × {Br}
  
The corrected-frame trefoil set is the V × Br × {H or Br} structure.
"""
    )
    
    # Test the conjecture
    test_triples = []
    for a in [0]:
        for b in [7, 8]:
            for c in [8]:
                test_triples.extend([(a,b,c), (a,c,b), (b,a,c), (b,c,a), (c,a,b), (c,b,a)])
    test_triples = list(set(test_triples))
    
    expected_set = set(TREFOIL_9)
    test_set = set(test_triples)
    print(f"\n  Conjecture predicts {len(test_set)} triples; actual trefoils: {len(expected_set)}")
    print(f"  Conjecture set: {sorted(test_set)}")
    print(f"  Trefoil set:    {sorted(expected_set)}")
    print(f"  Match: {test_set == expected_set}")


if __name__ == "__main__":
    main()
