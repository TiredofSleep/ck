"""
TIG flow/structure binary analysis.

Flow states:       {1, 3, 5, 7, 9} (odd, transformative)
Structure states:  {2, 4, 8}        (even, stabilizing)
Transition:        {6}              (chaos, the bridge)
VOID/boundary:     {0}              (flow boundary cell)

5 and 6 interchangeable (BALANCE ↔ CHAOS at the threshold)

This is a FUNCTIONAL partition by dynamical role, distinct from σ-cycle 
structure (which crosses the flow/structure boundary).

Bridge tests redone with this lens.
"""
import numpy as np
from itertools import product
from collections import Counter
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10, SIGMA_PERMUTATION

FLOW = {1, 3, 5, 7, 9}
STRUCTURE = {2, 4, 8}
TRANSITION = {6}
VOID = {0}

# 5 and 6 are interchangeable
FLOW_PLUS_TRANSITION = FLOW | TRANSITION  # {1, 3, 5, 6, 7, 9}
STRUCTURE_PLUS_TRANSITION = STRUCTURE | TRANSITION  # {2, 4, 6, 8}

OPERATOR_NAMES = {
    0: 'VOID', 1: 'LATTICE', 2: 'COUNTER', 3: 'PROGRESS', 4: 'COLLAPSE',
    5: 'BALANCE', 6: 'CHAOS', 7: 'HARMONY', 8: 'BREATH', 9: 'RESET'
}


def classify(n):
    if n in FLOW: return 'F'
    if n in STRUCTURE: return 'S'
    if n in TRANSITION: return 'T'
    if n in VOID: return 'V'
    return '?'


def main():
    print("=" * 70)
    print("TIG FLOW/STRUCTURE/TRANSITION PARTITION")
    print("=" * 70)
    print(f"\n  Flow F = {sorted(FLOW)} (transformative)")
    print(f"  Structure S = {sorted(STRUCTURE)} (stabilizing)")
    print(f"  Transition T = {sorted(TRANSITION)} (bridge)")
    print(f"  Void V = {sorted(VOID)} (boundary)")
    print(f"\n  5↔6 interchangeable (BALANCE ↔ CHAOS)")
    
    print(f"\n  Operator | role | name")
    for n in range(10):
        role = classify(n)
        print(f"     {n}    |  {role}   | {OPERATOR_NAMES[n]}")
    
    # Compare to σ-orbit structure
    print("\n" + "=" * 70)
    print("FLOW/STRUCTURE vs σ-ORBIT STRUCTURE")
    print("=" * 70)
    print(f"\n  σ orbits: (0)(3)(8)(9)(1 7 6 5 4 2)")
    print(f"  σ-fixed: {{0, 3, 8, 9}}")
    print(f"  σ-6-cycle: {{1, 7, 6, 5, 4, 2}}")
    
    print(f"\n  σ-fixed by role:")
    for n in [0, 3, 8, 9]:
        print(f"    {n} ({OPERATOR_NAMES[n]}): role {classify(n)}")
    
    print(f"\n  σ-6-cycle by role:")
    for n in [1, 7, 6, 5, 4, 2]:
        print(f"    {n} ({OPERATOR_NAMES[n]}): role {classify(n)}")
    
    # σ-fixed: {0, 3, 8, 9} = V + F(3) + S(8) + F(9). Mixed.
    # σ-6-cycle: {1,7,6,5,4,2} = F+F+T+F+S+S. Mostly flow with structure mixed in.
    
    print("""
Observations:
  - σ-fixed set has 1 V, 2 F (3, 9), 1 S (8)
  - σ-6-cycle has 3 F (1, 5, 7), 1 T (6), 2 S (2, 4)
  - σ-cycle structure does NOT respect flow/structure partition
  - But the 6-cycle has the 5↔6 interchangeability boundary built in:
    σ takes 6→5 (transition→flow) and 5→4 (flow→structure)
    σ⁻¹ takes 5→6 and 6→7. So the 5↔6 pair sits at a σ-edge.
""")
    
    # Trefoil-9 corrected frame: {V,H,Br} ∪ {V,Br,Br}
    print("=" * 70)
    print("CORRECTED TREFOIL SET UNDER FLOW/STRUCTURE LENS")
    print("=" * 70)
    
    TREFOIL_9 = [
        (0,7,8), (0,8,7), (0,8,8),
        (7,0,8), (7,8,0),
        (8,0,7), (8,0,8), (8,7,0), (8,8,0),
    ]
    
    print(f"\n  9 trefoil triples (corrected frame): {{V, H, Br}} and {{V, Br, Br}}")
    print(f"  In role notation: V H Br = V F S, V Br Br = V S S")
    
    print(f"\n  By role:")
    for t in TREFOIL_9:
        roles = [classify(x) for x in t]
        print(f"    {t} = {roles}")
    
    # All trefoils have role pattern V-S-S or V-S-F (with S=Br)
    print(f"\n  All trefoils have role pattern containing V (VOID) + S(Br) + (F or S)")
    print(f"  Specifically: trefoil ⟺ multiset = {{V, F(7), S(8)}} or {{V, S(8), S(8)}}")
    
    # Canonical grammar
    print("\n" + "=" * 70)
    print("CANONICAL PROPAGATION GRAMMAR UNDER FLOW/STRUCTURE LENS")
    print("=" * 70)
    
    canonical = [(0,1,2), (0,7,1), (5,6,7), (7,8,9), (7,8,8)]
    print(f"\n  Triple    | role pattern    | interpretation")
    
    for t in canonical:
        roles = ''.join(classify(x) for x in t)
        names = ', '.join(OPERATOR_NAMES[x] for x in t)
        print(f"  {str(t):<10} | {roles:<15} | {names}")
    
    print("""
Pattern recognition:
  (0,1,2) = V-F-S  : VOID → flow → structure (initiation)
  (0,7,1) = V-F-F  : VOID → flow → flow (sustained flow)
  (5,6,7) = F-T-F  : flow → transition → flow (BALANCE-CHAOS-HARMONY)
                    Uses the 5↔6 interchangeable pair!
  (7,8,9) = F-S-F  : flow → structure → flow (recovery cycle)
  (7,8,8) = F-S-S  : flow → structure → structure (crystallization)

The grammar is a sequence of flow/structure transitions.
Each canonical triple is a SPECIFIC role-pattern.

Notice that (5,6,7) is the ONLY triple involving the transition state 6.
That's because 6 is the unique bridge — it appears in grammar exactly
once, and exactly between two flow states.

5↔6 interchangeability: in (5,6,7), if we swap 5 and 6, we get (6,5,7)
which is F-F-F all flow. The semantics of (5,6,7) is "BALANCE acts as
CHAOS for one step before reaching HARMONY" — and the swap (6,5,7) is
"CHAOS acts as BALANCE before HARMONY." Both are valid grammar paths.
""")
    
    # BHML composition under flow/structure
    print("=" * 70)
    print("BHML COMPOSITION TABLE UNDER FLOW/STRUCTURE/TRANSITION ROLES")
    print("=" * 70)
    
    role_transition_count = Counter()
    for a in range(10):
        for b in range(10):
            ra = classify(a)
            rb = classify(b)
            out = int(BHML_10[a, b])
            ro = classify(out)
            role_transition_count[(ra, rb, ro)] += 1
    
    print(f"\n  Role-level transition table (BHML):")
    print(f"  {'in_a':<5} {'in_b':<5} {'out':<5} count")
    for k, v in sorted(role_transition_count.items(), key=lambda x: -x[1])[:15]:
        print(f"  {k[0]:<5} {k[1]:<5} {k[2]:<5} {v}")
    
    # What are the rules at role level?
    print(f"\n  Are role-level transitions deterministic?")
    role_pair_outputs = {}
    for a in range(10):
        for b in range(10):
            ra = classify(a)
            rb = classify(b)
            out = int(BHML_10[a, b])
            ro = classify(out)
            key = (ra, rb)
            role_pair_outputs.setdefault(key, set()).add(ro)
    
    print(f"\n  (in_a, in_b) → set of possible outputs (role level):")
    for (ra, rb), outs in sorted(role_pair_outputs.items()):
        det = "✓ deterministic" if len(outs) == 1 else f"✗ {len(outs)} outputs"
        print(f"    ({ra}, {rb}) → {outs}  {det}")


if __name__ == "__main__":
    main()
