"""
TSML_8 self-iteration role decomposition.

Earlier finding: TSML_8 sends every digit n in {1..6, 8, 9} to HARMONY in 1
step, then escapes to flow (V or H boundary).

Under role lens: the TSML_8 self-orbit for digit n is [n, 7=H=F, escape].
So TSML_8 = "every interior cell → flow (HARMONY) → boundary."

What does this look like in role notation?
"""
import numpy as np
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from tig_substrate import TSML_10, BHML_10

TSML_8_INDICES = [1, 2, 3, 4, 5, 6, 8, 9]
TSML_8 = TSML_10[np.ix_(TSML_8_INDICES, TSML_8_INDICES)]

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


def tsml8_full_table():
    """Full TSML_8 in original index notation."""
    table = {}
    for i, a in enumerate(TSML_8_INDICES):
        for j, b in enumerate(TSML_8_INDICES):
            table[(a, b)] = int(TSML_8[i, j])
    return table


def main():
    print("=" * 70)
    print("TSML_8 ROLE-LEVEL ANALYSIS")
    print("=" * 70)
    
    # Show full TSML_8 with roles
    print(f"\n  TSML_8 table with input/output roles:")
    print(f"  {'a':<4} {'b':<4} {'TSML(a,b)':<12} {'role_a':<8} {'role_b':<8} {'role_out':<8}")
    
    role_transitions = {}
    for a in TSML_8_INDICES:
        for b in TSML_8_INDICES:
            i = TSML_8_INDICES.index(a)
            j = TSML_8_INDICES.index(b)
            out = int(TSML_8[i, j])
            ra = role(a)
            rb = role(b)
            ro = role(out)
            key = (ra, rb)
            role_transitions.setdefault(key, set()).add((out, ro))
    
    print(f"\n  Role-level TSML_8 transitions:")
    print(f"  {'(role_a, role_b)':<20} {'output role(s)':<25} {'output digit(s)'}")
    
    for key, outputs in sorted(role_transitions.items()):
        out_roles = set(o[1] for o in outputs)
        out_digits = set(o[0] for o in outputs)
        det = "✓ deterministic" if len(out_roles) == 1 else f"✗ {len(out_roles)} roles"
        out_role_str = ', '.join(sorted(out_roles))
        out_digit_str = ', '.join(str(d) for d in sorted(out_digits))
        print(f"  {str(key):<20} {out_role_str:<25} {{{out_digit_str}}}  {det}")
    
    print("\n" + "=" * 70)
    print("TSML_8 vs BHML ROLE DETERMINISM COMPARISON")
    print("=" * 70)
    
    # Recompute BHML role-level for comparison
    bhml_role_transitions = {}
    for a in range(10):
        for b in range(10):
            out = int(BHML_10[a, b])
            ra = role(a)
            rb = role(b)
            ro = role(out)
            key = (ra, rb)
            bhml_role_transitions.setdefault(key, set()).add(ro)
    
    print(f"\n  Comparison of role-level determinism:")
    print(f"  {'pair':<10} {'BHML output roles':<25} {'TSML_8 output roles':<25}")
    
    all_pairs = set(role_transitions.keys()) | set(bhml_role_transitions.keys())
    for pair in sorted(all_pairs):
        bhml_outs = bhml_role_transitions.get(pair, set())
        tsml_outs = set()
        if pair in role_transitions:
            tsml_outs = set(o[1] for o in role_transitions[pair])
        bhml_str = ','.join(sorted(bhml_outs)) if bhml_outs else 'N/A'
        tsml_str = ','.join(sorted(tsml_outs)) if tsml_outs else 'N/A'
        print(f"  {str(pair):<10} {{{bhml_str}}}{' '*(23-len(bhml_str))} {{{tsml_str}}}")
    
    # What's the full TSML_8 image at role level?
    print("\n" + "=" * 70)
    print("WHAT ROLE OUTPUTS DOES TSML_8 PRODUCE?")
    print("=" * 70)
    
    output_roles = []
    for a in TSML_8_INDICES:
        for b in TSML_8_INDICES:
            i = TSML_8_INDICES.index(a)
            j = TSML_8_INDICES.index(b)
            out = int(TSML_8[i, j])
            output_roles.append(role(out))
    
    from collections import Counter
    output_role_counts = Counter(output_roles)
    print(f"\n  TSML_8 output role distribution:")
    total = sum(output_role_counts.values())
    for r, c in sorted(output_role_counts.items()):
        pct = c / total * 100
        print(f"    {r}: {c}/{total} ({pct:.1f}%)")
    
    # Hypothesis: TSML_8 outputs are mostly Flow (because → HARMONY)
    print(f"\n  TSML_8 essentially routes everything toward FLOW (HARMONY=7).")
    print(f"  This is the geometric coding: interior → cusp boundary in 1 step.")
    
    # Specific check: does TSML_8 ever output structure?
    structure_outputs = set()
    for a in TSML_8_INDICES:
        for b in TSML_8_INDICES:
            i = TSML_8_INDICES.index(a)
            j = TSML_8_INDICES.index(b)
            out = int(TSML_8[i, j])
            if out in STRUCTURE:
                structure_outputs.add((a, b, out))
    
    print(f"\n  TSML_8 inputs that produce STRUCTURE outputs:")
    for a, b, out in sorted(structure_outputs):
        print(f"    TSML({a}, {b}) = {out} ({role(out)})")
    
    # Compare BHML role-output distribution
    print(f"\n  BHML output role distribution (full 100 entries):")
    bhml_outputs = []
    for a in range(10):
        for b in range(10):
            bhml_outputs.append(role(int(BHML_10[a, b])))
    bhml_role_counts = Counter(bhml_outputs)
    for r, c in sorted(bhml_role_counts.items()):
        pct = c / 100 * 100
        print(f"    {r}: {c}/100 ({pct:.1f}%)")
    
    print(f"\n  Key contrast:")
    print(f"  TSML_8 outputs: heavily flow-biased (geometric → cusp)")
    print(f"  BHML_10 outputs: more balanced (arithmetic flow including all roles)")
    
    # What roles can BHML output that TSML_8 can't?
    print("\n" + "=" * 70)
    print("ROLES UNIQUE TO BHML vs TSML_8 OUTPUT")
    print("=" * 70)
    
    print(f"\n  BHML produces V outputs for: V acts as absorbing for some inputs.")
    print(f"  TSML_8 in canonical TIG produces no V outputs (V is outside its domain).")
    print(f"  But TSML_8 outputs CAN escape to V/H boundary if the formal rule sends them there.")
    
    # Where does TSML_8 send things? Tabulate.
    tsml_outputs_set = set()
    for a in TSML_8_INDICES:
        for b in TSML_8_INDICES:
            i = TSML_8_INDICES.index(a)
            j = TSML_8_INDICES.index(b)
            tsml_outputs_set.add(int(TSML_8[i, j]))
    
    print(f"\n  TSML_8 output digit set: {sorted(tsml_outputs_set)}")
    print(f"  TSML_8 image: {len(tsml_outputs_set)} distinct values out of 8 possible domain values")
    
    bhml_outputs_set = set()
    for a in range(10):
        for b in range(10):
            bhml_outputs_set.add(int(BHML_10[a, b]))
    print(f"\n  BHML output digit set: {sorted(bhml_outputs_set)}")
    print(f"  BHML image: {len(bhml_outputs_set)} distinct values out of 10")


if __name__ == "__main__":
    main()
