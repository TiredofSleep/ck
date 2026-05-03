"""
Lacasa-style bridge on corrected substrate.

Lacasa et al. (2018): residues of primes mod k have non-trivial Renyi
entropy spectrum but lack forbidden patterns; prime gap residues have
forbidden patterns linked to divisibility.

Substrate analog: TSML_8 + BHML_10 self-iteration produces symbolic
sequences. What's their forbidden-pattern structure, and does it
relate to substrate divisibility (factor structure of Z/10Z = Z/2Z × Z/5Z)?
"""
import numpy as np
from itertools import product
from collections import Counter
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10

TSML_8_INDICES = [1, 2, 3, 4, 5, 6, 8, 9]
TSML_8 = TSML_10[np.ix_(TSML_8_INDICES, TSML_8_INDICES)]
FLOW_CELLS = {0, 7}


def gather_full_substrate_2grams():
    """All 2-grams (a, BHML(a, b)) and (a, TSML(a, b)) over all (a, b)."""
    bhml_pairs = []
    tsml_pairs = []
    
    # BHML 2-grams: for every (a, b), record (a, BHML(a, b))
    for a in range(10):
        for b in range(10):
            out = int(BHML_10[a, b])
            bhml_pairs.append((a, out))
    
    # TSML_8 2-grams: only for (a, b) both in TSML_8 domain
    for a in TSML_8_INDICES:
        for b in TSML_8_INDICES:
            a_l, b_l = TSML_8_INDICES.index(a), TSML_8_INDICES.index(b)
            out = int(TSML_8[a_l, b_l])
            tsml_pairs.append((a, out))
    
    return bhml_pairs, tsml_pairs


def divisibility_class(n):
    """Z/10Z = Z/2Z × Z/5Z. Each digit n has (n mod 2, n mod 5)."""
    return (n % 2, n % 5)


def main():
    print("=" * 70)
    print("LACASA-STYLE FORBIDDEN-PATTERN ANALYSIS ON CORRECTED SUBSTRATE")
    print("=" * 70)
    
    bhml_pairs, tsml_pairs = gather_full_substrate_2grams()
    
    # All possible pairs in respective domains
    all_bhml_pairs = set(product(range(10), repeat=2))
    all_tsml_pairs = set(product(TSML_8_INDICES, repeat=2))
    
    bhml_seen = set(bhml_pairs)
    tsml_seen = set(tsml_pairs)
    
    bhml_forbidden = all_bhml_pairs - {(a, BHML_10[a, b]) for a in range(10) for b in range(10)}
    
    print(f"\n  BHML_10 (a, BHML(a,b)) image: {len(bhml_seen)} unique pairs out of 100")
    print(f"  TSML_8  (a, TSML(a,b)) image: {len(tsml_seen)} unique pairs out of 64")
    print(f"\n  Forbidden BHML output pairs: {100 - len(bhml_seen)}")
    print(f"  Forbidden TSML_8 output pairs: {64 - len(tsml_seen)}")
    
    # The "forbidden" set is what the substrate cannot produce as (input, output) pairs
    print("\n" + "=" * 70)
    print("DIVISIBILITY ANALYSIS — Z/10Z = Z/2Z × Z/5Z")
    print("=" * 70)
    
    print("\n  Each digit n has divisibility class (n mod 2, n mod 5):")
    for n in range(10):
        c = divisibility_class(n)
        print(f"    {n}: ({c[0]}, {c[1]})")
    
    # Group digits by divisibility class
    classes = {}
    for n in range(10):
        c = divisibility_class(n)
        classes.setdefault(c, []).append(n)
    
    print(f"\n  Divisibility classes:")
    for c, members in sorted(classes.items()):
        print(f"    ({c[0]}, {c[1]}): {members}")
    
    # Are the forbidden 2-grams correlated with divisibility classes?
    print("\n" + "=" * 70)
    print("DO FORBIDDEN PATTERNS RESPECT DIVISIBILITY?")
    print("=" * 70)
    
    # BHML forbidden pairs: which divisibility class transitions are forbidden?
    # i.e., for each (class_a → class_b) transition, what fraction of (a, b) pairs in 
    # those classes produce forbidden output pairs?
    
    bhml_class_trans = Counter()
    for a in range(10):
        for b in range(10):
            ca = divisibility_class(a)
            cb = divisibility_class(int(BHML_10[a, b]))
            bhml_class_trans[(ca, cb)] += 1
    
    print(f"\n  BHML class-transition counts (input class → output class):")
    print(f"  {'in_class':<10} → {'out_class':<10} count")
    all_classes = sorted(set(divisibility_class(n) for n in range(10)))
    
    # Count how many transitions occur per class pair
    in_class_total = Counter()
    for a in range(10):
        for b in range(10):
            ca = divisibility_class(a)
            in_class_total[ca] += 1
    
    # Transitions that occur
    trans_seen = set()
    for trans, count in bhml_class_trans.items():
        trans_seen.add(trans)
    
    # Which class transitions never occur?
    all_trans = set()
    for c1 in all_classes:
        for c2 in all_classes:
            all_trans.add((c1, c2))
    
    forbidden_trans = all_trans - trans_seen
    print(f"\n  Total possible class transitions: {len(all_trans)}")
    print(f"  BHML-realized class transitions: {len(trans_seen)}")
    print(f"  BHML-forbidden class transitions: {len(forbidden_trans)}")
    
    if forbidden_trans:
        print(f"\n  Forbidden transitions:")
        for ft in sorted(forbidden_trans):
            print(f"    {ft[0]} → {ft[1]}")
    
    # Now look at the MOST COMMON transitions
    print(f"\n  Most common BHML class transitions:")
    for trans, count in sorted(bhml_class_trans.items(), key=lambda x: -x[1])[:8]:
        print(f"    {trans[0]} → {trans[1]}: {count} times")
    
    # Specific check: does (n mod 2, n mod 5) of BHML(a, b) factor through (a mod 2, a mod 5)?
    print("\n" + "=" * 70)
    print("DOES BHML RESPECT Z/2 × Z/5 DECOMPOSITION?")
    print("=" * 70)
    
    print("\n  Check: is BHML(a, b) mod 2 determined only by (a mod 2, b mod 2)?")
    bhml_mod2_consistent = True
    bhml_mod2_table = {}
    for a in range(10):
        for b in range(10):
            out = int(BHML_10[a, b])
            key = (a % 2, b % 2)
            actual = out % 2
            if key in bhml_mod2_table:
                if bhml_mod2_table[key] != actual:
                    bhml_mod2_consistent = False
                    print(f"    Inconsistent: a={a}, b={b}, expected {bhml_mod2_table[key]} mod 2, got {actual}")
                    break
            else:
                bhml_mod2_table[key] = actual
        if not bhml_mod2_consistent:
            break
    
    print(f"  BHML respects mod 2 structure: {bhml_mod2_consistent}")
    if bhml_mod2_consistent:
        print(f"  Induced mod 2 table:")
        for (a2, b2), out2 in sorted(bhml_mod2_table.items()):
            print(f"    BHML({a2}, {b2}) mod 2 = {out2}")
    
    print("\n  Check: is BHML(a, b) mod 5 determined only by (a mod 5, b mod 5)?")
    bhml_mod5_consistent = True
    bhml_mod5_table = {}
    for a in range(10):
        for b in range(10):
            out = int(BHML_10[a, b])
            key = (a % 5, b % 5)
            actual = out % 5
            if key in bhml_mod5_table:
                if bhml_mod5_table[key] != actual:
                    bhml_mod5_consistent = False
                    print(f"    Inconsistent: a={a}, b={b}, BHML({a},{b})={out} mod 5 = {actual}, "
                          f"but expected {bhml_mod5_table[key]}")
                    break
            else:
                bhml_mod5_table[key] = actual
        if not bhml_mod5_consistent:
            break
    
    print(f"  BHML respects mod 5 structure: {bhml_mod5_consistent}")
    
    # Same for TSML_10
    print("\n  Same checks for TSML_10:")
    tsml_mod2_consistent = True
    tsml_mod5_consistent = True
    tsml_mod2_table = {}
    tsml_mod5_table = {}
    for a in range(10):
        for b in range(10):
            out = int(TSML_10[a, b])
            key2 = (a % 2, b % 2)
            actual2 = out % 2
            if key2 in tsml_mod2_table and tsml_mod2_table[key2] != actual2:
                tsml_mod2_consistent = False
            else:
                tsml_mod2_table[key2] = actual2
            
            key5 = (a % 5, b % 5)
            actual5 = out % 5
            if key5 in tsml_mod5_table and tsml_mod5_table[key5] != actual5:
                tsml_mod5_consistent = False
            else:
                tsml_mod5_table[key5] = actual5
    
    print(f"  TSML_10 respects mod 2: {tsml_mod2_consistent}")
    print(f"  TSML_10 respects mod 5: {tsml_mod5_consistent}")


if __name__ == "__main__":
    main()
