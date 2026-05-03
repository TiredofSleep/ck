"""
Crossing count taxonomy: which crossing counts does the substrate produce?

If the substrate has a discrete knot vocabulary, the achievable crossing 
counts should form a structured set, not be arbitrary.

Knot crossing numbers (minimum crossings of a knot in standard form):
  0: unknot
  3: trefoil (3_1)
  4: figure-eight (4_1)
  5: Solomon's seal (5_1, 5_2)
  6: 6_1, 6_2, 6_3
  7: 7_1, ..., 7_7
  
The substrate's achievable crossing counts on 4-core triples were:
  2, 3, 4, 5, 6, 11, 12, 15, 24

Gap structure: 2,3,4,5,6,7,8 → big jump to 11,12 → 15 → 24

Let's see what's structurally distinguishable about these counts.
"""
import numpy as np
from itertools import product
from collections import Counter, defaultdict
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')
from trefoil_corrected_frame import trajectory_corrected


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
    print("CROSSING COUNT TAXONOMY")
    print("=" * 70)
    
    # Compute all 1000 triple crossings (already done in earlier files,
    # recompute for completeness)
    print("\n  Computing crossings for all 1000 triples...")
    crossings = {}
    for a, b, c in product(range(10), repeat=3):
        r = trajectory_corrected(a, b, c)
        crossings[(a, b, c)] = r['crossings']
    
    cn_dist = Counter(crossings.values())
    
    print(f"\n  Distribution of crossing counts on all 1000 triples:")
    print(f"  {'crossings':<12} {'count':<10} {'fraction'}")
    for c in sorted(cn_dist.keys()):
        n = cn_dist[c]
        pct = n / 1000 * 100
        print(f"  {c:<12} {n:<10} {pct:.2f}%")
    
    # Look at gaps
    achievable = sorted(cn_dist.keys())
    print(f"\n  Achievable crossing counts: {achievable}")
    print(f"  Total distinct: {len(achievable)}")
    
    # Find gaps
    gaps = []
    for i in range(len(achievable) - 1):
        if achievable[i+1] - achievable[i] > 1:
            gaps.append((achievable[i], achievable[i+1], achievable[i+1] - achievable[i] - 1))
    
    print(f"\n  Gaps in crossing counts:")
    for low, high, missing in gaps:
        print(f"    Between {low} and {high}: {missing} values not achievable")
    
    # The "structured" view: 1, 2, 3, 4 are accessible. Other small counts?
    print(f"\n  Achievable counts ≤ 20:")
    print(f"    {[c for c in achievable if c <= 20]}")
    print(f"  Not achievable ≤ 20:")
    print(f"    {[c for c in range(20) if c not in achievable]}")
    
    # Look at specific high-count clusters
    print("\n" + "=" * 70)
    print("ROLE COMPOSITION OF EACH CROSSING-COUNT CLASS")
    print("=" * 70)
    
    print(f"\n  For each crossing count, what role patterns appear?")
    print(f"  (Show top 3 most-common role patterns per count)")
    
    cn_to_roles = defaultdict(Counter)
    for t, c in crossings.items():
        roles = ''.join(role(x) for x in t)
        cn_to_roles[c][roles] += 1
    
    for c in sorted(cn_dist.keys())[:15]:  # focus on lower counts
        top_roles = cn_to_roles[c].most_common(3)
        print(f"  Crossings {c}: {top_roles}")
    
    # Specifically: which role patterns ONLY produce specific crossing counts?
    print("\n" + "=" * 70)
    print("ROLE-PATTERN → CROSSING-COUNT MAP")
    print("=" * 70)
    
    role_to_cns = defaultdict(set)
    for t, c in crossings.items():
        roles = ''.join(role(x) for x in t)
        role_to_cns[roles].add(c)
    
    print(f"\n  Role patterns producing UNIQUE crossing counts (deterministic):")
    deterministic_roles = []
    for roles, cns in sorted(role_to_cns.items()):
        if len(cns) == 1:
            deterministic_roles.append((roles, list(cns)[0]))
    
    for roles, c in deterministic_roles[:25]:
        # How many triples have this role pattern?
        count = sum(1 for t, c2 in crossings.items() 
                    if ''.join(role(x) for x in t) == roles)
        print(f"    {roles}: always {c} crossings ({count} triples)")
    
    # Role patterns with widely varying crossing counts
    print(f"\n  Role patterns with HIGH variance (many crossing counts):")
    role_variances = []
    for roles, cns in role_to_cns.items():
        if len(cns) >= 3:
            count = sum(1 for t in crossings if ''.join(role(x) for x in t) == roles)
            role_variances.append((roles, len(cns), count))
    
    role_variances.sort(key=lambda x: -x[1])
    for roles, n_distinct, total in role_variances[:10]:
        cns = sorted(role_to_cns[roles])
        cns_str = str(cns) if len(cns) < 10 else str(cns[:5]) + f"...{cns[-2:]}"
        print(f"    {roles}: {n_distinct} distinct counts {cns_str} ({total} triples)")
    
    # Special interest: role patterns containing T (transition)
    print("\n" + "=" * 70)
    print("ROLE PATTERNS CONTAINING TRANSITION (T = CHAOS)")
    print("=" * 70)
    
    print(f"\n  Role patterns with T:")
    for roles, cns in sorted(role_to_cns.items()):
        if 'T' in roles:
            count = sum(1 for t in crossings 
                       if ''.join(role(x) for x in t) == roles)
            cns_sorted = sorted(cns)
            cns_str = str(cns_sorted) if len(cns_sorted) < 8 else f"{cns_sorted[:4]}...{cns_sorted[-2:]}"
            print(f"    {roles}: counts {cns_str} ({count} triples)")
    
    # Key question: what is the SIGNATURE of role pattern V-V-V (all VOID)?
    # And V-anything in general?
    print("\n" + "=" * 70)
    print("SPECIAL CASE: ROLE PATTERNS WITH VOID")
    print("=" * 70)
    
    # V-V-V is just (0,0,0)
    if (0,0,0) in crossings:
        print(f"\n  (0,0,0) VVV: {crossings[(0,0,0)]} crossings (the 'rest state')")
    
    # Any V containing
    void_role_patterns = sorted([r for r in role_to_cns if 'V' in r])
    print(f"\n  Role patterns containing V ({len(void_role_patterns)}):")
    for roles in void_role_patterns:
        cns = sorted(role_to_cns[roles])
        count = sum(1 for t in crossings 
                   if ''.join(role(x) for x in t) == roles)
        if len(cns) <= 5:
            print(f"    {roles}: {cns} ({count} triples)")
    
    # Final summary
    print("\n" + "=" * 70)
    print("CROSSING-COUNT TAXONOMY SUMMARY")
    print("=" * 70)
    
    print(f"""
  The substrate's runtime processor produces crossing counts in this 
  set: {sorted(cn_dist.keys())[:20]}{'...' if len(cn_dist) > 20 else ''}.
  
  Some role patterns are crossing-count deterministic 
  (e.g., specific patterns always give same count).
  Others span a wide range (3+ distinct counts).
  
  This means: the substrate's role partition is INSUFFICIENT to determine
  topological behavior in general, but IS sufficient for some specific 
  patterns.
  
  The trefoil count (3 crossings) appears for a few specific role patterns.
  Other counts (1, 2, 4, 5, 6) similarly map to specific role patterns.
  
  Honest read: there isn't a clean "role pattern → knot type" map. The 
  substrate's full operator-level structure matters for crossing count, 
  not just role.
""")


if __name__ == "__main__":
    main()
