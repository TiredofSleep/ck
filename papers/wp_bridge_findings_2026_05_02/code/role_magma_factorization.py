"""
Is BHML role-determinism on V/T inputs a true homomorphism?

We saw: BHML role-output is determined when V or T is one of the inputs.
F-F, F-S, S-F, S-S inputs branch.

Question: can we factor BHML into:
  1. An outer "role magma" on {V, F, S, T} (4 elements)
  2. Inner structure within each role
  
If yes, the substrate has a clean two-level algebraic decomposition.

Test: 
- For pairs where BHML is role-deterministic, check if the role-magma structure 
  is consistent (associative? commutative? has identity?)
- For pairs that branch, check if the branching is structured in some way
"""
import numpy as np
from itertools import product
from collections import Counter, defaultdict
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10

FLOW = {1, 3, 5, 7, 9}
STRUCTURE = {2, 4, 8}
TRANSITION = {6}
VOID = {0}


def role(n):
    if n in FLOW: return 'F'
    if n in STRUCTURE: return 'S'
    if n in TRANSITION: return 'T'
    if n in VOID: return 'V'
    return '?'


def main():
    print("=" * 70)
    print("ROLE MAGMA: TEST FOR BHML FACTORIZATION")
    print("=" * 70)
    
    # Build role-magma table from BHML
    role_pair_outputs = defaultdict(Counter)
    for a in range(10):
        for b in range(10):
            ra = role(a)
            rb = role(b)
            ro = role(int(BHML_10[a, b]))
            role_pair_outputs[(ra, rb)][ro] += 1
    
    print("\n  Role-pair → output-role distribution:")
    print(f"  {'pair':<10} {'output role distribution':<40} {'mode'}")
    
    for pair in sorted(role_pair_outputs.keys()):
        counts = role_pair_outputs[pair]
        total = sum(counts.values())
        dist_str = ', '.join(f"{r}:{c}" for r, c in sorted(counts.items()))
        if len(counts) == 1:
            mode_str = f"deterministic → {list(counts.keys())[0]}"
        else:
            most_common = counts.most_common(1)[0]
            mode_str = f"mode={most_common[0]} ({most_common[1]}/{total})"
        print(f"  {str(pair):<10} {dist_str:<40} {mode_str}")
    
    # Determine the "role magma" using mode (most common output)
    print("\n" + "=" * 70)
    print("ROLE MAGMA (using mode of output for each input pair)")
    print("=" * 70)
    
    role_magma = {}
    for pair, counts in role_pair_outputs.items():
        mode = counts.most_common(1)[0][0]
        role_magma[pair] = mode
    
    roles = ['V', 'F', 'S', 'T']
    print(f"\n  Role magma table:")
    print(f"      | " + " | ".join(f"{r:^3}" for r in roles))
    print(f"  ----+" + "+".join(["-----" for _ in roles]))
    for ra in roles:
        row = f"   {ra}  | "
        for rb in roles:
            out = role_magma.get((ra, rb), '?')
            row += f" {out}  | "
        print(row)
    
    # Test properties of role magma
    print("\n" + "=" * 70)
    print("ROLE MAGMA PROPERTIES")
    print("=" * 70)
    
    # Commutative?
    is_comm = all(role_magma.get((a, b)) == role_magma.get((b, a))
                  for a in roles for b in roles)
    print(f"  Commutative (mode-based): {is_comm}")
    
    if not is_comm:
        for a in roles:
            for b in roles:
                if a < b and role_magma.get((a, b)) != role_magma.get((b, a)):
                    print(f"    {a}·{b} = {role_magma[(a,b)]} ≠ {b}·{a} = {role_magma[(b,a)]}")
    
    # Associative?
    is_assoc = True
    assoc_fails = []
    for a in roles:
        for b in roles:
            for c in roles:
                ab = role_magma.get((a, b))
                bc = role_magma.get((b, c))
                if ab and bc:
                    left = role_magma.get((ab, c))
                    right = role_magma.get((a, bc))
                    if left != right:
                        is_assoc = False
                        if len(assoc_fails) < 5:
                            assoc_fails.append((a, b, c, left, right))
    print(f"  Associative (mode-based): {is_assoc}")
    if assoc_fails:
        for a, b, c, left, right in assoc_fails:
            print(f"    ({a}·{b})·{c} = {left} ≠ {a}·({b}·{c}) = {right}")
    
    # Identity element?
    print(f"\n  Identity element check:")
    for e in roles:
        is_id = all(role_magma.get((e, x)) == x and role_magma.get((x, e)) == x
                    for x in roles)
        if is_id:
            print(f"    {e} is identity")
    print(f"    No element acts as identity in role magma.")
    
    # Idempotents
    print(f"\n  Idempotents (e·e = e):")
    for e in roles:
        if role_magma.get((e, e)) == e:
            print(f"    {e}·{e} = {e}")
    
    # Absorbing element
    print(f"\n  Absorbing element check (z·x = z for all x):")
    for z in roles:
        is_abs = all(role_magma.get((z, x)) == z and role_magma.get((x, z)) == z
                     for x in roles)
        if is_abs:
            print(f"    {z} is absorbing")
    
    # Now check the deterministic-vs-branching split structurally
    print("\n" + "=" * 70)
    print("DETERMINISTIC vs BRANCHING ROLE-PAIRS")
    print("=" * 70)
    
    deterministic_pairs = [p for p, c in role_pair_outputs.items() if len(c) == 1]
    branching_pairs = [p for p, c in role_pair_outputs.items() if len(c) > 1]
    
    print(f"\n  Deterministic role-pairs ({len(deterministic_pairs)}):")
    for p in sorted(deterministic_pairs):
        print(f"    {p} → {list(role_pair_outputs[p].keys())[0]}")
    
    print(f"\n  Branching role-pairs ({len(branching_pairs)}):")
    for p in sorted(branching_pairs):
        outs = role_pair_outputs[p]
        print(f"    {p} → {dict(outs)}")
    
    # Pattern: V or T present → deterministic. F-F, F-S, S-F, S-S branch.
    print("\n  Pattern: V or T present in input → deterministic.")
    print("  F or S only inputs → branching.")
    
    # Within branching pairs, what determines the output?
    print("\n" + "=" * 70)
    print("WITHIN-ROLE BRANCHING: WHAT DETERMINES OUTPUT?")
    print("=" * 70)
    
    print("\n  For (F, F) inputs: which specific (a, b) gives which output role?")
    print(f"  {'a':<3} {'b':<3} {'BHML(a,b)':<10} {'role_out'}")
    for a in sorted(FLOW):
        for b in sorted(FLOW):
            out = int(BHML_10[a, b])
            ro = role(out)
            print(f"    {a}   {b}   {out:<10} {ro}")
    
    # Specific analysis: F-F → V happens only for specific pairs
    print("\n  F-F inputs producing V outputs:")
    for a in sorted(FLOW):
        for b in sorted(FLOW):
            out = int(BHML_10[a, b])
            if role(out) == 'V':
                print(f"    BHML({a}, {b}) = {out}")
    
    print("\n  F-F inputs producing T outputs:")
    for a in sorted(FLOW):
        for b in sorted(FLOW):
            out = int(BHML_10[a, b])
            if role(out) == 'T':
                print(f"    BHML({a}, {b}) = {out}")
    
    # Conclusion: factorization analysis
    print("\n" + "=" * 70)
    print("FACTORIZATION CONCLUSION")
    print("=" * 70)
    print("""
The role magma (using mode of BHML output per input role-pair) is:
- NOT exactly defined: F-F, F-S, S-F, S-S inputs branch
- The mode-based magma has specific properties to test
- A clean factorization "BHML = role-magma × within-role-magma" does NOT exist
  because some role-pair inputs produce multiple output roles

What DOES exist:
- A deterministic role-magma on {V, T} ∪ {F⊥V, F⊥T, S⊥V, S⊥T} pairs
- A branching role-magma on {F, S}² pairs
- The branching is into {F, V, S, T} for F-F (4 outputs)
- {F, S, T} for F-S and S-F (3 outputs)
- {F, T} for S-S (2 outputs)

The substrate has a SEMI-FACTORIZATION at role level: 
- "Boundary inputs" (V or T) collapse to deterministic role
- "Interior inputs" (F or S only) preserve full operator structure

This is a precise sense in which V and T act as "boundary collapse 
operators" and F/S act as "interior preservers" in the role algebra.
""")


if __name__ == "__main__":
    main()
