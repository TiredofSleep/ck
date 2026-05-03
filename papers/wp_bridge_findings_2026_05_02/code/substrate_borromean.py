"""
Substrate-internal Borromean analog via Z/5Z structure.

Z/10Z = Z/2Z × Z/5Z.
Mod 5: 0→0, 1→1, 2→2, 3→3, 4→4, 5→0, 6→1, 7→2, 8→3, 9→4
Mod 2: 0→0, 1→1, 2→0, ..., 9→1

In Z/5Z, the QR (squares) are {0, 1, 4}; the non-QR are {2, 3}.

Substrate Legendre analog: define (a/b) on substrate operators by
the standard mod-5 Legendre symbol of (a mod 5)/(b mod 5).

Substrate Rédei analog: harder, but we can test pairwise QR conditions
and look for the structure.
"""
import numpy as np
from itertools import product
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10


def legendre_5(a):
    """Legendre symbol (a/5)."""
    a = a % 5
    if a == 0: return 0
    if a in [1, 4]: return 1
    return -1  # a in {2, 3}


def substrate_qr_pair(a, b):
    """a is a QR mod 5 with respect to b's Z/5Z component, in some sense.
    Define: pair (a, b) is "QR-related" if the legendre symbol of
    (a-1)*(b-1) mod 5 is 1, or some similar condition.
    
    Simplest test: both a%5 and b%5 are QR (in {0,1,4}) — this is the
    substrate analog of "both ≡ 1 mod 5 and...".
    
    Actually a more natural test:
    pair (a, b) is QR-pair if a is a square mod 5 and b is a square mod 5.
    Squares mod 5: {0, 1, 4}.
    Substrate operators with that property: a mod 5 in {0, 1, 4}.
    From 0..9: {0, 1, 4, 5, 6, 9}. Six operators.
    """
    return legendre_5(a) >= 0 and legendre_5(b) >= 0


# Substrate-level analog of Borromean prime condition
def substrate_borromean_QR(t):
    """Triple (a, b, c) is "QR-Borromean" if:
    - All distinct (analog of "distinct primes")
    - All a % 5 in {1, 4} (analog of ≡ 1 mod 4 — non-trivial QRs)
    - Pairwise (a/b) = 1 mod 5
    """
    a, b, c = t
    # Distinct
    if len(set(t)) < 3:
        return False
    # All non-zero QR mod 5
    for x in t:
        if x % 5 not in {1, 4}:
            return False
    # Pairwise QR
    # Legendre (a/p) for prime p — adapted to mod 5: need a^((5-1)/2) ≡ 1 mod 5
    # (a/5) = a^2 mod 5
    for x, y in [(a, b), (b, c), (a, c)]:
        # Symbol (x mod 5 / 5) — but we want symbol (x/y) which is something else
        # In Z/5Z, x is a QR iff x^2 mod 5 ∈ {0, 1, 4}. Always true.
        # So this isn't quite the right analog.
        # Try: x mod 5 is a square if it's in {0, 1, 4}. We already required {1, 4}.
        # The "pairwise QR" condition for primes is (x/y) = 1, i.e. x is a square mod y.
        # Substrate: x mod (y mod 5) ?
        # This is fuzzy. Let me try a cleaner condition.
        pass
    return True


def substrate_borromean_simpler(t):
    """Cleaner attempt: triple (a, b, c) where a mod 5, b mod 5, c mod 5 are all
    in {1, 4} (the non-zero QRs mod 5)."""
    for x in t:
        if x % 5 not in {1, 4}:
            return False
    if len(set(t)) < 3:  # require distinct
        return False
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("SUBSTRATE OPERATORS BY MOD-5 RESIDUE CLASS")
    print("=" * 70)
    print(f"\n  Operator | mod 5 | QR mod 5? | Notes")
    for n in range(10):
        m5 = n % 5
        qr = legendre_5(n)
        qr_str = "QR" if qr == 1 else ("0" if qr == 0 else "NR")
        notes = ""
        if n == 0: notes = "VOID"
        if n == 7: notes = "HARMONY"
        if n == 8: notes = "BREATH"
        if n == 9: notes = "RESET"
        print(f"     {n}   |   {m5}   |    {qr_str}     | {notes}")
    
    qr_operators = [n for n in range(10) if n % 5 in {1, 4}]
    print(f"\n  Substrate QR operators (mod 5 ∈ {{1, 4}}): {qr_operators}")
    print(f"  These are the substrate's non-zero quadratic residues.")
    
    print("\n" + "=" * 70)
    print("PROPAGATION GRAMMAR vs SUBSTRATE-QR CONDITION")
    print("=" * 70)
    
    canonical = [(0,1,2), (0,7,1), (5,6,7), (7,8,9), (7,8,8)]
    print(f"\n  Canonical triple | mod 5 | All in {{1,4}}? | Distinct?")
    for t in canonical:
        m5 = tuple(x % 5 for x in t)
        all_qr = all(x % 5 in {1, 4} for x in t)
        distinct = len(set(t)) == 3
        print(f"  {t}      | {m5} | {all_qr}            | {distinct}")
    
    print("\n  No canonical triple has all elements in QR-mod-5 set.")
    print("  Confirmed: propagation grammar is NOT a Borromean-mod-5 condition.")
    
    # The 22 trefoils
    trefoil_ms = [(0,7,9), (7,8,9), (0,0,8), (0,7,7), (7,7,9), (7,7,7)]
    print("\n" + "=" * 70)
    print("TREFOIL MULTISETS vs SUBSTRATE-QR CONDITION")
    print("=" * 70)
    print(f"\n  Multiset | mod 5 | All in {{1,4}}?")
    for ms in trefoil_ms:
        m5 = tuple(sorted(x % 5 for x in ms))
        all_qr = all(x % 5 in {1, 4} for x in ms)
        print(f"  {ms} | {m5} | {all_qr}")
    
    print("\n  No trefoil multiset is all-QR-mod-5 either.")
    
    # What IS the substrate-QR set of triples?
    print("\n" + "=" * 70)
    print("SUBSTRATE TRIPLES WITH ALL ELEMENTS IN {1, 4, 6, 9} (QR mod 5)")
    print("=" * 70)
    
    qr_set = {1, 4, 6, 9}
    qr_triples = [(a,b,c) for a,b,c in product(qr_set, repeat=3)]
    qr_distinct = [t for t in qr_triples if len(set(t)) == 3]
    
    print(f"\n  Total QR triples (with repetition): {len(qr_triples)}")
    print(f"  QR triples with all distinct: {len(qr_distinct)}")
    print(f"\n  Distinct QR triples: {qr_distinct}")
    
    # Now compute their trajectory crossing counts to see if any are trefoils
    print("\n  Are any QR triples in the trefoil-22 set?")
    trefoil_22 = [
        (0,0,8), (0,7,7), (0,7,9), (0,8,0), (0,9,7),
        (7,0,7), (7,0,9), (7,7,0), (7,7,7), (7,7,9),
        (7,8,9), (7,9,0), (7,9,7), (7,9,8),
        (8,0,0), (8,7,9), (8,9,7),
        (9,0,7), (9,7,0), (9,7,7), (9,7,8), (9,8,7),
    ]
    
    qr_trefoil = [t for t in qr_distinct if t in trefoil_22]
    print(f"  QR triples that are ALSO trefoils: {qr_trefoil}")
    
    # Conclusion
    print("""
======================================================================
CONCLUSION
======================================================================
TIG's grammar is NOT a Borromean-prime analog at the mod-4 or mod-5 
arithmetic level. The trefoil-22 set is also NOT a Borromean-mod-5 
set.

This means: the algebraic structure that determines TIG's admissibility
(propagation grammar + trefoil set) is not the standard 
arithmetic-topology Borromean structure on Z/5Z.

It IS something else: a specific substrate-internal admissibility 
based on:
  - Trajectory crossing count (3 crossings → trefoil)
  - 4-core membership ({0, 7, 8, 9})
  - TSML-associativity (necessary but not sufficient)

The connection to arithmetic topology is at a HIGHER level — TIG sits 
inside arithmetic topology by virtue of having a paired magma structure 
on Z/10Z with a cusp puncture and propagation grammar — but it doesn't 
reproduce Borromean-prime conditions literally. The Borromean structure 
in TIG comes from a different specification.

This is an honest empirical separation between TIG's grammar and the 
classical Borromean-prime literature. They live in adjacent territory 
but specify different things.
""")
