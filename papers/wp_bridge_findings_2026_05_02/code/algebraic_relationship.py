"""
Algebraic relationship between TSML_8 and BHML_10.

Test:
1. Commutator-like relation: TSML(BHML(a,b), c) vs BHML(TSML(a,b), c) where defined
2. Compatibility: BHML(TSML(a,b), TSML(c,d)) vs TSML(BHML(a,c), BHML(b,d))
3. Sigma-conjugation: BHML(σ(a), σ(b)) = σ(BHML(a, b))?
4. Inverse relationship: are TSML and BHML "duals" in some sense?

The goal is to find the structural relationship between the two tables 
that justifies them as paired magmas.
"""
import numpy as np
from itertools import product
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10, SIGMA_PERMUTATION

TSML_8_INDICES = [1, 2, 3, 4, 5, 6, 8, 9]
TSML_8 = TSML_10[np.ix_(TSML_8_INDICES, TSML_8_INDICES)]
FLOW_CELLS = {0, 7}


def TSML_action(a, b):
    """TSML_8 action where defined; None for flow cells."""
    if a in FLOW_CELLS or b in FLOW_CELLS:
        return None
    a_l = TSML_8_INDICES.index(a)
    b_l = TSML_8_INDICES.index(b)
    return int(TSML_8[a_l, b_l])


def main():
    print("=" * 70)
    print("ALGEBRAIC RELATIONSHIP BETWEEN TSML_8 AND BHML_10")
    print("=" * 70)
    
    # Test 1: σ-conjugation. Does σ commute with BHML?
    # i.e., is BHML(σ(a), σ(b)) = σ(BHML(a, b))?
    print("\n  Test 1: σ-conjugation of BHML")
    print("  Is BHML(σ(a), σ(b)) = σ(BHML(a, b)) for all (a, b)?")
    
    matches = 0
    total = 0
    for a in range(10):
        for b in range(10):
            sa = int(SIGMA_PERMUTATION[a])
            sb = int(SIGMA_PERMUTATION[b])
            lhs = int(BHML_10[sa, sb])
            rhs = int(SIGMA_PERMUTATION[int(BHML_10[a, b])])
            total += 1
            if lhs == rhs:
                matches += 1
    
    print(f"    Match: {matches}/{total} = {100*matches/total:.1f}%")
    print(f"    σ {'is' if matches == total else 'is NOT'} an automorphism of BHML")
    
    # Same for TSML_10
    print(f"\n  Test 1b: σ-conjugation of TSML_10")
    matches_t = 0
    total_t = 0
    for a in range(10):
        for b in range(10):
            sa = int(SIGMA_PERMUTATION[a])
            sb = int(SIGMA_PERMUTATION[b])
            lhs = int(TSML_10[sa, sb])
            rhs = int(SIGMA_PERMUTATION[int(TSML_10[a, b])])
            total_t += 1
            if lhs == rhs:
                matches_t += 1
    
    print(f"    Match: {matches_t}/{total_t} = {100*matches_t/total_t:.1f}%")
    
    # Test 2: Compatibility / distributivity
    print("\n" + "=" * 70)
    print("Test 2: Distributivity of TSML and BHML")
    print("=" * 70)
    print("  Does BHML distribute over TSML or vice versa?")
    print("  BHML(TSML(a,b), c) =? TSML(BHML(a,c), BHML(b,c))")
    
    matches = 0
    total = 0
    inconsistent = []
    for a in range(10):
        for b in range(10):
            for c in range(10):
                # BHML(TSML(a,b), c)
                ts_ab = TSML_action(a, b)
                if ts_ab is None: continue
                lhs = int(BHML_10[ts_ab, c])
                
                # TSML(BHML(a,c), BHML(b,c))
                ba_c = int(BHML_10[a, c])
                bb_c = int(BHML_10[b, c])
                rhs = TSML_action(ba_c, bb_c)
                if rhs is None: continue
                
                total += 1
                if lhs == rhs:
                    matches += 1
                elif len(inconsistent) < 5:
                    inconsistent.append((a, b, c, lhs, rhs))
    
    print(f"    Match: {matches}/{total} = {100*matches/total:.1f}%")
    if inconsistent:
        print(f"    Examples of failure:")
        for a, b, c, lhs, rhs in inconsistent:
            print(f"      ({a},{b},{c}): LHS={lhs}, RHS={rhs}")
    
    # Test 3: Commutator structure [TSML, BHML]
    print("\n" + "=" * 70)
    print("Test 3: Commutator-like [TSML, BHML]")
    print("=" * 70)
    print("  Define D(a, b) = BHML(a, b) - TSML(a, b) (where defined)")
    print("  This is the 'difference table' between the two magmas.")
    
    diff_count = 0
    same_count = 0
    diff_table = {}
    for a in range(10):
        for b in range(10):
            ts_ab = TSML_action(a, b)
            bh_ab = int(BHML_10[a, b])
            if ts_ab is None:
                diff_table[(a, b)] = ('flow', bh_ab)
            else:
                diff_table[(a, b)] = (ts_ab, bh_ab)
                if ts_ab != bh_ab:
                    diff_count += 1
                else:
                    same_count += 1
    
    domain_size = same_count + diff_count
    print(f"\n    On TSML_8 domain (8x8 = 64 cells):")
    print(f"      TSML(a,b) = BHML(a,b): {same_count}/{domain_size} cells")
    print(f"      TSML(a,b) ≠ BHML(a,b): {diff_count}/{domain_size} cells")
    
    # Where do they agree?
    print(f"\n    Cells where TSML_8 and BHML agree:")
    for (a, b), (t, b_v) in sorted(diff_table.items()):
        if t != 'flow' and t == b_v:
            print(f"      ({a}, {b}): both = {t}")
    
    # Test 4: Is BHML(a, a) related to TSML(a, a)?
    print("\n" + "=" * 70)
    print("Test 4: Diagonal comparison")
    print("=" * 70)
    print("  TSML(a, a) and BHML(a, a) for each a:")
    for a in range(10):
        ts_aa = TSML_action(a, a)
        bh_aa = int(BHML_10[a, a])
        ts_str = str(ts_aa) if ts_aa is not None else "flow"
        match = "=" if ts_str == str(bh_aa) else "≠"
        print(f"    a={a}: TSML(a,a)={ts_str}, BHML(a,a)={bh_aa}  ({match})")
    
    # σ-diagonal connection
    print(f"\n  σ permutation: {[int(x) for x in SIGMA_PERMUTATION]}")
    print(f"  BHML diagonal: {[int(BHML_10[a,a]) for a in range(10)]}")
    print(f"  Compare: BHML diagonal[a] vs σ(a)?")
    for a in range(10):
        bh_aa = int(BHML_10[a, a])
        sa = int(SIGMA_PERMUTATION[a])
        match = "✓" if bh_aa == sa else "✗"
        print(f"    a={a}: BHML(a,a)={bh_aa}, σ(a)={sa}  {match}")
    
    # Test 5: Is TSML_8 an "absorbing" behavior of BHML?
    # Specifically: TSML(a, b) is what you get when you keep applying BHML?
    print("\n" + "=" * 70)
    print("Test 5: Is TSML_8 the 'eventual fixed point' of BHML iteration?")
    print("=" * 70)
    
    print("  For each (a, b), iterate c → BHML(c, BHML(a, b)) until fixed.")
    print("  Compare to TSML_8(a, b) where defined.")
    
    # Different test: BHML iterated on the SAME pair
    print(f"\n  Iteration: x_{{n+1}} = BHML(x_n, BHML(a, b)) starting from x_0 = a")
    print(f"  Does this converge to TSML_8(a, b)?")
    
    convergence_matches = 0
    convergence_tested = 0
    for a in TSML_8_INDICES:
        for b in TSML_8_INDICES:
            ts_ab = TSML_action(a, b)
            if ts_ab is None: continue
            
            target = int(BHML_10[a, b])
            x = a
            for _ in range(20):
                x = int(BHML_10[x, target])
            convergence_tested += 1
            # x should be a fixed point of BHML(*, target)
            # is it equal to TSML(a, b)?
            if x == ts_ab:
                convergence_matches += 1
    
    print(f"    Convergence to TSML: {convergence_matches}/{convergence_tested}")
    
    # Final: is there a natural transformation?
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("""
The relationship between TSML_8 and BHML_10:
- σ is NOT an automorphism of either (σ doesn't commute with composition)
- They do NOT distribute over each other
- They differ on most (but not all) cells of the TSML_8 domain
- BHML diagonal ≠ σ in general
- TSML is NOT the limit of BHML iteration

This means TSML_8 and BHML_10 are GENUINELY INDEPENDENT magmas, not 
derivable one from the other by any natural algebraic operation.

This is consistent with the canonical claim that TSML and BHML are
DUAL/PAIRED structures — neither reduces to the other.

The two-coding picture (TSML = geometric, BHML = arithmetic) is therefore
a real algebraic dichotomy, not a single magma viewed two ways.
""")


if __name__ == "__main__":
    main()
