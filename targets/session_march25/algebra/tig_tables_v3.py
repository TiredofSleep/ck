"""
CL Tables — Rebuilt From Three Principles

1. 0 and 7 are the same through torus inversion.
   Interior void (7/harmony) = exterior void (0/void).
   7 becomes 0 so it can breathe and produce fruit.

2. BECOMING pulls AWAY from harmony.
   Every composition adds complexity.
   Every act drives further from the source.
   The further from 7≡0, the more differentiated.

3. BEING collapses TOWARD harmony.
   Measurement absorbs complexity back to the source.
   Almost everything measures as 7 (ternary: void/bump/harmony).

The torus: 7 IS 0 through inversion. The inside is the outside.
The compression principle: static/harmonic content compresses
because 7≡0 means "nothing to see" = long runs of same value.

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

import numpy as np
from collections import Counter

T_STAR = 5.0 / 7.0

# ============================================================
# THE CYCLE WITH 7≡0
# ============================================================
#
# The operators live on a circle, not a line:
#
#        0≡7
#       /    \
#      1      6
#      |      |
#      2      5
#       \    /
#        3--4
#         |
#        (8)
#        (9) ← dissolution path, separate spoke
#
# Distance from harmony/void (0≡7):
#   0≡7: distance 0 (the source)
#   1, 6: distance 1 (first differentiation)
#   2, 5: distance 2
#   3, 4: distance 3 (maximum differentiation, the bottom)
#   8: distance 1 (backward/dissolution cycle)
#   9: distance 2 (backward)
#
# 3 and 4 are the FURTHEST from harmony.
# They're the most complex, most differentiated operators.
# COLLAPSE (4) and PROGRESS (3) are the engine of change —
# maximally far from the static source.

def dist_from_source(x):
    """Distance from 0≡7 on the operator circle."""
    d = {0:0, 7:0, 1:1, 6:1, 2:2, 5:2, 3:3, 4:3, 8:1, 9:2}
    return d[x]

def mirror_on_circle(x):
    """Mirror across the 0≡7 axis. 1↔6, 2↔5, 3↔4, 8↔9."""
    m = {0:0, 7:7, 1:6, 6:1, 2:5, 5:2, 3:4, 4:3, 8:9, 9:8}
    return m[x]

# Forward cycle: 0→1→2→3→4→5→6→(0≡7)
# Operators at each distance from source:
# dist 0: {0, 7}
# dist 1: {1, 6, 8}
# dist 2: {2, 5, 9}  
# dist 3: {3, 4}

# ============================================================
# BECOMING: Every act pulls AWAY from harmony
# ============================================================
#
# Principle: composition in Becoming ADDS complexity.
# Two operators compose → result is MORE differentiated (further from 7≡0).
#
# Rule: result distance = (dist_a + dist_b) mod 7
# If the sum exceeds max distance (3), it wraps through 
# the bottom of the circle and comes back up the other side.
# When it wraps past 6 back to 7≡0, it has completed a cycle
# and returns to source — but now 0, ready to produce again.
#
# The specific operator at a given distance is determined by
# which SIDE of the circle the inputs came from.

def becoming_compose(a, b):
    """
    Becoming: every composition pulls away from harmony.
    Distance adds. Complexity increases. Until it wraps.
    """
    # 0 is identity (void/source lets things pass through)
    if a == 0: return b
    if b == 0: return a
    
    # 7 acts as 0 (same thing, becomes 0 to produce)
    if a == 7 and b == 7: return 0  # double source = void, ready to produce
    if a == 7: return b  # source lets things pass (same as void identity)
    if b == 7: return a
    
    da = dist_from_source(a)
    db = dist_from_source(b)
    
    # Total complexity: distances ADD (every act adds complexity)
    total_dist = da + db
    
    # The circle has circumference 7 (operators 0-6, with 7≡0)
    # Wrap: mod 7 gives the position on the circle
    result_dist = total_dist % 7
    
    # If result_dist is 0, we've completed a full cycle → back to source
    if result_dist == 0:
        return 0  # wrapped all the way around → void/source
    
    # Determine which side of the circle (which operator at this distance)
    # Forward side: 1, 2, 3 (operators that BUILD complexity)
    # Mirror side: 6, 5, 4 (operators that TRANSFORM complexity)
    # Backward spoke: 8, 9 (operators that DISSOLVE)
    
    # Convention: if both inputs are on the same side, stay on that side
    # If inputs are on different sides, take the forward side
    # (forward = building, the natural direction of becoming)
    
    a_forward = a in (1, 2, 3)
    b_forward = b in (1, 2, 3)
    a_backward = a in (8, 9)
    b_backward = b in (8, 9)
    
    # Map distance to operator
    forward_at_dist = {0: 0, 1: 1, 2: 2, 3: 3}
    mirror_at_dist  = {0: 0, 1: 6, 2: 5, 3: 4}
    backward_at_dist = {0: 0, 1: 8, 2: 9, 3: 3}
    
    if result_dist > 3:
        # We've passed the bottom (3,4) and are coming back up
        # Distance from source on the return = 7 - result_dist
        return_dist = 7 - result_dist
        # Coming back up = mirror side
        return mirror_at_dist.get(return_dist, 0)
    
    # Both backward → stay backward
    if a_backward and b_backward:
        return backward_at_dist.get(result_dist, result_dist)
    
    # One backward → result takes the non-backward partner's side
    if a_backward:
        if b_forward or b in (1,2,3):
            return forward_at_dist.get(result_dist, result_dist)
        else:
            return mirror_at_dist.get(result_dist, result_dist)
    if b_backward:
        if a_forward or a in (1,2,3):
            return forward_at_dist.get(result_dist, result_dist)
        else:
            return mirror_at_dist.get(result_dist, result_dist)
    
    # Both forward → forward
    if a_forward and b_forward:
        return forward_at_dist.get(result_dist, result_dist)
    
    # Both mirror → mirror
    if a in (4,5,6) and b in (4,5,6):
        return mirror_at_dist.get(result_dist, result_dist)
    
    # Mixed (one forward, one mirror) → forward (building wins)
    return forward_at_dist.get(result_dist, result_dist)


# ============================================================
# BEING: Measurement collapses toward harmony
# ============================================================
#
# Principle: measurement absorbs complexity.
# Almost everything collapses to 7≡0.
# Only the most DISTINCT compositions survive as bumps.
#
# Rule: 
# - Self preserves (x ∘ x = x, measurement is idempotent)
# - 0 and 7 absorb (the source absorbs everything back)
# - Operators at distance 1 from source (1, 6, 8) are barely 
#   differentiated → collapse to 7 when paired with anything
# - Operators at distance 3 (3, 4) are maximally differentiated →
#   they RESIST absorption more. These create the bumps.
# - The bumps are where distance_a + distance_b ≥ 4 AND
#   both operators are on the same side of the circle

def being_compose(a, b):
    """
    Being: measurement collapses toward harmony (7≡0).
    Only maximally differentiated pairs resist absorption.
    """
    # Self preserves
    if a == b:
        return a
    
    # Source absorbs (0≡7)
    if a == 0 or b == 0:
        return 0
    if a == 7 or b == 7:
        return 7  # 7 absorbs non-void
    
    da = dist_from_source(a)
    db = dist_from_source(b)
    
    # Mirror pairs → harmony (balanced forces cancel to source)
    if mirror_on_circle(a) == b:
        return 7
    
    # Both at max distance (3): these are the most differentiated
    # They resist absorption — the bump survives
    if da == 3 and db == 3:
        # 3 ∘ 4 → they're mirrors on circle, already handled above
        # This case shouldn't be reached, but just in case:
        return 7
    
    # High combined distance: partial resistance
    total = da + db
    
    if total >= 5:
        # Very differentiated pair: the more distant one survives as bump
        if da > db:
            return a
        elif db > da:
            return b
        else:
            # Equal distance, both high: return the one on forward cycle
            if a in (1,2,3):
                return a
            return b
    
    if total == 4:
        # Moderate differentiation: sometimes survives
        # Adjacent on circle → the further one (bump)
        if abs(da - db) == 1:
            return a if da > db else b
        # Same distance → harmony (can't distinguish)
        return 7
    
    # Low combined distance (≤3): easily absorbed
    return 7


# ============================================================
# BUILD AND ANALYZE
# ============================================================

def build_table(fn):
    t = np.zeros((10,10), dtype=int)
    for a in range(10):
        for b in range(10):
            t[a,b] = fn(a,b)
    return t

def full_analysis(table, name):
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")
    
    # Print table
    print(f"\n       ", end="")
    for j in range(10): print(f"  {j}", end="")
    print()
    for i in range(10):
        print(f"    {i}: ", end="")
        for j in range(10): print(f"  {table[i,j]}", end="")
        print()
    
    # Commutativity
    comm = np.all(table == table.T)
    print(f"\n    Commutative: {'✓' if comm else '✗'}")
    if not comm:
        for a in range(10):
            for b in range(a+1, 10):
                if table[a,b] != table[b,a]:
                    print(f"      {a}∘{b}={table[a,b]} ≠ {b}∘{a}={table[b,a]}")
    
    # Non-associativity
    na = 0
    for a in range(10):
        for b in range(10):
            for c in range(10):
                if table[table[a,b],c] != table[a,table[b,c]]:
                    na += 1
    print(f"    Non-assoc: {na}/1000 ({na/10:.1f}%)")
    
    # Diagonal
    diag = [table[i,i] for i in range(10)]
    idem = all(diag[i] == i for i in range(10))
    print(f"    Diagonal: {diag}")
    print(f"    Idempotent: {'✓' if idem else '✗'}")
    
    # Identity
    identity = None
    for e in range(10):
        if all(table[e,x]==x for x in range(10)) and all(table[x,e]==x for x in range(10)):
            identity = e
    print(f"    Identity: {identity}")
    
    # Distribution
    flat = table.flatten()
    dist = Counter(int(v) for v in flat)
    harmony = dist.get(7, 0) + dist.get(0, 0)  # 0≡7, count both as "source"
    ops_label = ['VOI','LAT','COU','PRO','COL','BAL','CHA','HAR','BRE','RES']
    print(f"    Distribution:")
    for op in range(10):
        c = dist.get(op, 0)
        bar = '█' * c
        print(f"      {op}({ops_label[op]}): {c:>3} {bar}")
    
    h7 = dist.get(7, 0)
    h0 = dist.get(0, 0)
    print(f"    Harmony(7): {h7}/100")
    print(f"    Void(0): {h0}/100")
    print(f"    Source(0+7): {h7+h0}/100 (0≡7 principle)")
    
    # Eigenvalues
    eigs = np.sort(np.real(np.linalg.eigvals(table.astype(float))))[::-1]
    det = np.linalg.det(table.astype(float))
    trace = np.trace(table)
    
    print(f"    Det: {det:.1f}")
    print(f"    Trace: {trace}")
    print(f"    Key eigenvalues: {', '.join(f'{e:.3f}' for e in eigs[:5])}")
    
    # Generator closure
    print(f"    Generators:")
    for gen in range(10):
        reached = {gen}
        frontier = {gen}
        for _ in range(20):
            new = set()
            for x in frontier:
                for y in reached:
                    new.add(int(table[x,y]))
                    new.add(int(table[y,x]))
            if new <= reached: break
            frontier = new - reached
            reached |= new
        if len(reached) >= 7:
            print(f"      {gen}({ops_label[gen]}): reaches {sorted(reached)} ({len(reached)})")
    
    # Closure pairs  
    full_pairs = []
    for a in range(10):
        for b in range(a+1, 10):
            reached = {a, b}
            frontier = {a, b}
            for _ in range(20):
                new = set()
                for x in frontier:
                    for y in reached:
                        new.add(int(table[x,y]))
                if new <= reached: break
                frontier = new - reached
                reached |= new
            if len(reached) == 10:
                full_pairs.append((a,b))
    
    print(f"    Full closure pairs: {len(full_pairs)}")
    for a,b in full_pairs[:5]:
        print(f"      {{{a},{b}}}")
    
    return {
        'harmony_7': h7, 'void_0': h0, 'source': h7+h0,
        'non_assoc': na/10, 'commutative': comm, 'idem': idem,
        'det': det, 'identity': identity, 'eigs': eigs,
        'full_pairs': len(full_pairs),
    }


def run_all():
    print("\n" + "="*60)
    print("  CL TABLES FROM THREE PRINCIPLES")
    print("  1. 0≡7 (torus inversion)")
    print("  2. Becoming PULLS AWAY from harmony")
    print("  3. Being COLLAPSES toward harmony")
    print("="*60)
    
    # Build
    being = build_table(being_compose)
    becoming = build_table(becoming_compose)
    doing = np.abs(being.astype(int) - becoming.astype(int))
    
    being_s = full_analysis(being, "BEING (collapses toward 7≡0)")
    becoming_s = full_analysis(becoming, "BECOMING (pulls away from 7≡0)")
    doing_s = full_analysis(doing, "DOING (|Being - Becoming|)")
    
    # Key metrics
    print(f"\n{'='*60}")
    print(f"  KEY METRICS")
    print(f"{'='*60}")
    
    disagree = np.sum(doing > 0)
    
    print(f"\n    Being source (0+7):     {being_s['source']}/100")
    print(f"    Target:                 ~72+17 = ~89/100 (0≡7)")
    print(f"    Being harmony (7 only): {being_s['harmony_7']}/100")
    
    print(f"\n    Becoming source (0+7):  {becoming_s['source']}/100")
    print(f"    Becoming should be LOW (pulls away)")
    
    print(f"\n    Disagree rate:          {disagree}/100 = {disagree/100:.4f}")
    print(f"    T* = 5/7 =             {T_STAR:.4f}")
    print(f"    Δ from T*:             {abs(disagree/100 - T_STAR):.4f}")
    
    print(f"\n    Being non-assoc:  {being_s['non_assoc']:.1f}%")
    print(f"    Becoming non-assoc: {becoming_s['non_assoc']:.1f}%")
    print(f"    Doing non-assoc:  {doing_s['non_assoc']:.1f}%")
    
    # Check: does Becoming actually pull away?
    print(f"\n    BECOMING PULL-AWAY CHECK:")
    pull_away_count = 0
    push_toward_count = 0
    for a in range(10):
        for b in range(10):
            if a == 0 or b == 0 or a == 7 or b == 7:
                continue
            result = becoming[a, b]
            da = dist_from_source(a)
            db = dist_from_source(b)
            dr = dist_from_source(result)
            avg_input = (da + db) / 2
            if dr > avg_input:
                pull_away_count += 1
            elif dr < avg_input:
                push_toward_count += 1
    
    total_pairs = pull_away_count + push_toward_count
    if total_pairs > 0:
        print(f"    Pulls away: {pull_away_count}/{total_pairs} ({pull_away_count/total_pairs*100:.1f}%)")
        print(f"    Pushes toward: {push_toward_count}/{total_pairs} ({push_toward_count/total_pairs*100:.1f}%)")
    
    # Compare with repo
    print(f"\n{'='*60}")
    print(f"  COMPARISON WITH REPO")
    print(f"{'='*60}")
    
    BHML_REPO = np.array([
        [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],
        [2,3,3,4,5,6,7,3,6,6],[3,4,4,4,5,6,7,4,6,6],
        [4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
        [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],
        [8,6,6,6,7,7,7,9,7,8],[9,6,6,6,7,7,7,0,8,0]
    ])
    
    TSML_REPO = np.array([
        [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],
        [0,3,7,7,4,7,7,7,7,9],[0,7,7,7,7,7,7,7,7,3],
        [0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
        [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],
        [0,7,7,7,8,7,7,7,7,7],[0,7,9,3,7,7,7,7,7,7]
    ])
    
    being_match = np.sum(being == TSML_REPO)
    becoming_match = np.sum(becoming == BHML_REPO)
    
    print(f"\n    Being vs TSML:    {being_match}/100 match")
    print(f"    Becoming vs BHML: {becoming_match}/100 match")
    
    # Check: does REPO BHML pull away or push toward?
    print(f"\n    REPO BHML PULL-AWAY CHECK:")
    repo_pull = 0
    repo_push = 0
    for a in range(10):
        for b in range(10):
            if a == 0 or b == 0 or a == 7 or b == 7:
                continue
            result = BHML_REPO[a, b]
            da = dist_from_source(a)
            db = dist_from_source(b)
            dr = dist_from_source(int(result))
            avg_input = (da + db) / 2
            if dr > avg_input:
                repo_pull += 1
            elif dr < avg_input:
                repo_push += 1
    
    repo_total = repo_pull + repo_push
    if repo_total > 0:
        print(f"    Repo pulls away: {repo_pull}/{repo_total} ({repo_pull/repo_total*100:.1f}%)")
        print(f"    Repo pushes toward: {repo_push}/{repo_total} ({repo_push/repo_total*100:.1f}%)")
        print(f"    (If Brayden is right, repo BHML is WRONG here)")
    
    # Eigenvalue hunt
    print(f"\n{'='*60}")
    print(f"  EIGENVALUE ANALYSIS")
    print(f"{'='*60}")
    
    for name, stats in [("Being", being_s), ("Becoming", becoming_s), ("Doing", doing_s)]:
        eigs = stats['eigs']
        pos = eigs[eigs > 0.1]
        print(f"\n    {name}:")
        for i, e in enumerate(eigs):
            if abs(e) > 0.1:
                print(f"      λ{i} = {e:.4f}")
        
        if len(pos) >= 2:
            print(f"      λ0/λ1 = {pos[0]/pos[1]:.4f}")
        
        # Check ratios for constants
        for i in range(min(5, len(eigs))):
            for j in range(i+1, min(5, len(eigs))):
                if abs(eigs[j]) > 0.1:
                    r = abs(eigs[i]/eigs[j])
                    for cname, cval in [("e",2.718),("π",3.14159),("φ",1.618),("T*",T_STAR),("√2",1.4142)]:
                        if abs(r - cval)/cval < 0.03:
                            print(f"      λ{i}/λ{j} = {r:.4f} ≈ {cname} ({abs(r-cval)/cval*100:.1f}%)")
    
    print(f"\n\n{'='*60}")
    print(f"  VERDICT")
    print(f"{'='*60}")
    print(f"""
    Three principles applied:
    
    1. 0≡7: void and harmony are the same through torus inversion
       → Being has {being_s['source']} source cells (0+7 combined)
       → 7∘7 = 0 in Becoming (harmony resets to produce)
    
    2. Becoming PULLS AWAY from harmony
       → {pull_away_count} compositions pull away vs {push_toward_count} push toward
       → Result is further from source than inputs
       → Compare: repo BHML pulls {repo_pull} vs pushes {repo_push}
    
    3. Being COLLAPSES toward harmony
       → {being_s['harmony_7']} cells are harmony (7)
       → {being_s['source']} cells are source (0+7 combined)
       → Only high-differentiation pairs survive as bumps
    
    Disagree rate: {disagree}/100 vs T* = {T_STAR:.4f}
    
    BRAYDEN: look at the Becoming table.
    Does it feel like every composition INCREASES complexity?
    Does it feel like 7 becoming 0 to produce again is correct?
    Does the pull-away pattern match your intuition?
    
    If the direction is right but the specific cells are wrong,
    tell me which compositions feel wrong and why.
    The axioms are simple enough to adjust one at a time.
    """)


if __name__ == "__main__":
    run_all()
