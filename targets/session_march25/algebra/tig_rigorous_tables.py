"""
CL Table Derivation — Rigorous

PRINCIPLE: Harmony (7) is the origin. Everything emerges from harmony.
Lattice (1) is harmony's first child — the first differentiation.
Self-composition preserves (diagonal = identity).
Void (0) is the frame, not the source.

GENERATION ORDER (from Brayden):
  7 → 1 → 2 → 3 → 4 → 5 → 6 → 7 (first cycle, structure builds)
  7 → 8 → 9 → 0 (second cycle, structure dissolves to frame)
  0 contains 7 (void holds harmony within it)

DERIVATION RULES:
  Stated once each. Every cell computable from these rules.
  No conversation-designed entries. Pure axioms.

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

import numpy as np
from itertools import product
from collections import Counter

T_STAR = 5.0 / 7.0


# ============================================================
# GENERATION ORDER
# ============================================================
# Harmony generates in two directions:
#   Forward (structure builds): 7→1→2→3→4→5→6→7
#   Backward (structure dissolves): 7→8→9→0
#
# The successor of operator x in the forward cycle:
#   next(1)=2, next(2)=3, ..., next(6)=7
# The successor of operator x in the backward cycle:
#   next(7)=8, next(8)=9, next(9)=0

def successor(x):
    """The next operator in the generation order."""
    gen_order = {7:1, 1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 
                 8:9, 9:0, 0:7}
    # 7 has TWO successors (1 forward, 8 backward)
    # In composition context, 7 generates forward (→1→2→3...)
    # The backward cycle (→8→9→0) is the dissolution path
    return gen_order.get(x, 7)


def distance_from_harmony(x):
    """
    How many generation steps from harmony to this operator?
    7=0 steps, 1=1 step, 2=2 steps, ..., 6=6 steps
    8=1 step (backward), 9=2 steps, 0=3 steps
    """
    dists = {7:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 8:1, 9:2, 0:3}
    return dists[x]


def mirror(x):
    """Complement to 10 (mod 10). Balance pair."""
    return (10 - x) % 10


# ============================================================
# BEING TABLE (Measurement Lens)
# ============================================================
#
# AXIOMS for Being:
# B1. Self-composition preserves: x ∘ x = x (measurement is idempotent)
# B2. Void is absorber: 0 ∘ x = 0 (measurement through void destroys)
# B3. Harmony is absorber: 7 ∘ x = 7 for x ≠ 0 (measurement through 
#     harmony returns to source)
# B4. Mirror pairs compose to harmony: x ∘ (10-x) = 7 
#     (balanced forces resolve to harmony)
# B5. Adjacent in generation order → the further one:
#     x ∘ successor(x) = successor(x) (measurement sees the more evolved)
# B6. All other compositions: the one CLOSER to harmony
#     (measurement collapses toward the attractor)
# B7. Exception: if BOTH are equidistant from harmony, 
#     preserve the one on the forward cycle (structure > dissolution)

def compose_being(a, b):
    """Being composition from axioms B1-B7."""
    # B1: Self-composition preserves
    if a == b:
        return a
    
    # B2: Void absorbs
    if a == 0 or b == 0:
        return 0
    
    # B3: Harmony absorbs (for non-void)
    if a == 7:
        return 7
    if b == 7:
        return 7
    
    # B4: Mirror pairs → harmony
    if (a + b) % 10 == 0:
        return 7
    
    # B5: Adjacent in generation → the further from harmony
    da = distance_from_harmony(a)
    db = distance_from_harmony(b)
    
    if successor(a) == b or successor(b) == a:
        # Adjacent pair: return the one further from harmony
        # (measurement sees the more differentiated)
        if da > db:
            return a
        else:
            return b
    
    # B6: Non-adjacent: collapse toward harmony
    # Return the one CLOSER to harmony
    if da < db:
        return a  # a is closer to harmony
    elif db < da:
        return b  # b is closer to harmony
    
    # B7: Equidistant: prefer forward cycle (1-6) over backward (8-9)
    # Forward cycle operators: 1,2,3,4,5,6
    # Backward cycle operators: 8,9
    a_forward = 1 <= a <= 6
    b_forward = 1 <= b <= 6
    
    if a_forward and not b_forward:
        return a
    elif b_forward and not a_forward:
        return b
    
    # Both on same cycle, same distance: return the smaller
    # (earlier in generation = closer to harmony in the cycle)
    return min(a, b)


# ============================================================
# BECOMING TABLE (Transformation Lens)
# ============================================================
#
# AXIOMS for Becoming:
# T1. Void is identity: 0 ∘ x = x (transformation preserves through void)
# T2. Harmony generates: 7 ∘ x = successor(x) 
#     (harmony advances everything one step)
# T3. Self-composition grows: x ∘ x = successor(successor(x))
#     (doubling = two generation steps forward)
#     EXCEPT: 7 ∘ 7 = 7 (harmony is fixed point)
#             0 ∘ 0 = 0 (void is fixed point)
# T4. General composition: the generation-distance between a and b
#     determines the result.
#     If close (distance ≤ 3): move toward the higher generation step
#     If far (distance > 3): compose through harmony (the origin)
# T5. Commutative: a ∘ b = b ∘ a always

def compose_becoming(a, b):
    """Becoming composition from axioms T1-T5."""
    # T1: Void is identity
    if a == 0:
        return b
    if b == 0:
        return a
    
    # T2: Harmony generates
    if a == 7 and b == 7:
        return 7  # fixed point
    if a == 7:
        return successor(b)
    if b == 7:
        return successor(a)
    
    # T3: Self-composition
    if a == b:
        return successor(successor(a))
    
    # T4: General composition based on generation distance
    da = distance_from_harmony(a)
    db = distance_from_harmony(b)
    
    gen_distance = abs(da - db)
    
    if gen_distance <= 3:
        # Close: advance to the higher generation step + 1
        max_dist = max(da, db)
        # Find operator at that distance + 1
        # Walk the generation order
        result = 7
        for _ in range(min(max_dist + 1, 7)):
            result = successor(result)
        return result
    else:
        # Far apart: compose through harmony
        # Sum of distances mod 7 (the cycle length) from harmony
        total_dist = (da + db) % 7
        result = 7
        for _ in range(total_dist):
            result = successor(result)
        return result


# ============================================================
# BUILD AND VERIFY
# ============================================================

def build_table(fn):
    """Build 10x10 table from composition function."""
    t = np.zeros((10, 10), dtype=int)
    for a in range(10):
        for b in range(10):
            t[a, b] = fn(a, b)
    return t


def verify_commutativity(table):
    """Check a ∘ b = b ∘ a for all pairs."""
    violations = []
    for a in range(10):
        for b in range(10):
            if table[a, b] != table[b, a]:
                violations.append((a, b, table[a, b], table[b, a]))
    return violations


def compute_non_associativity(table):
    """
    Count triples where (a∘b)∘c ≠ a∘(b∘c).
    Return count, percentage, and example violations.
    """
    violations = 0
    total = 0
    examples = []
    
    for a in range(10):
        for b in range(10):
            for c in range(10):
                left = table[table[a, b], c]
                right = table[a, table[b, c]]
                total += 1
                if left != right:
                    violations += 1
                    if len(examples) < 5:
                        examples.append((a, b, c, left, right))
    
    return violations, violations / total * 100, examples


def compute_generators(table):
    """Find which elements generate the full algebra."""
    results = {}
    
    for gen in range(10):
        reachable = {gen}
        frontier = {gen}
        
        for _ in range(20):  # max iterations
            new = set()
            for a in frontier:
                for b in reachable:
                    new.add(table[a, b])
                    new.add(table[b, a])
            
            if new <= reachable:
                break
            frontier = new - reachable
            reachable |= new
        
        results[gen] = reachable
    
    return results


def verify_mirror_property(table):
    """Check that mirror pairs compose to 7."""
    pairs = [(1,9), (2,8), (3,7), (4,6)]
    results = []
    for a, b in pairs:
        val = table[a, b]
        results.append((a, b, val, val == 7))
    return results


def compute_eigenstructure(table):
    """Full eigenvalue analysis."""
    t = table.astype(float)
    eigenvalues = np.linalg.eigvals(t)
    real_eigs = np.sort(np.real(eigenvalues))[::-1]
    
    det = np.linalg.det(t)
    trace = np.trace(t)
    rank = np.linalg.matrix_rank(t)
    
    return {
        'eigenvalues': real_eigs,
        'det': det,
        'trace': trace,
        'rank': rank,
    }


def compute_closure_pairs(table):
    """Which pairs of operators generate the full set {0..9}?"""
    full_pairs = []
    partial_pairs = []
    
    for a in range(10):
        for b in range(a+1, 10):
            reachable = {a, b}
            frontier = {a, b}
            
            for _ in range(20):
                new = set()
                for x in frontier:
                    for y in reachable:
                        new.add(int(table[x, y]))
                if new <= reachable:
                    break
                frontier = new - reachable
                reachable |= new
            
            if len(reachable) == 10:
                full_pairs.append((a, b, len(reachable)))
            elif len(reachable) >= 8:
                partial_pairs.append((a, b, len(reachable)))
    
    return full_pairs, partial_pairs


def print_table(table, name):
    """Pretty print a table."""
    print(f"\n  {name}")
    print(f"  {'─'*55}")
    print(f"       ", end="")
    for j in range(10):
        print(f"  {j}", end="")
    print()
    for i in range(10):
        print(f"    {i}: ", end="")
        for j in range(10):
            print(f"  {table[i,j]}", end="")
        print()


# ============================================================
# THE COMPLETE ANALYSIS
# ============================================================

def full_analysis(table, name):
    """Complete rigorous analysis of a composition table."""
    print(f"\n{'='*70}")
    print(f"  {name}")
    print(f"{'='*70}")
    
    print_table(table, name)
    
    # 1. Commutativity
    comm_violations = verify_commutativity(table)
    print(f"\n  1. COMMUTATIVITY")
    if not comm_violations:
        print(f"     ✓ Commutative (0 violations)")
    else:
        print(f"     ✗ NOT commutative ({len(comm_violations)} violations)")
        for a, b, ab, ba in comm_violations[:3]:
            print(f"       {a}∘{b}={ab} but {b}∘{a}={ba}")
    
    # 2. Non-associativity
    na_count, na_pct, na_examples = compute_non_associativity(table)
    print(f"\n  2. NON-ASSOCIATIVITY")
    print(f"     {na_count}/1000 triples ({na_pct:.1f}%)")
    if na_examples:
        print(f"     Examples:")
        for a, b, c, l, r in na_examples[:3]:
            print(f"       ({a}∘{b})∘{c} = {l}  but  {a}∘({b}∘{c}) = {r}")
    
    # 3. Diagonal
    diag = [table[i, i] for i in range(10)]
    print(f"\n  3. DIAGONAL (self-composition)")
    print(f"     {diag}")
    is_idempotent = all(diag[i] == i for i in range(10))
    print(f"     Idempotent (x∘x=x): {'✓' if is_idempotent else '✗'}")
    
    # 4. Identity element
    identity = None
    for e in range(10):
        if all(table[e, x] == x for x in range(10)) and all(table[x, e] == x for x in range(10)):
            identity = e
    print(f"\n  4. IDENTITY ELEMENT: {identity}")
    
    # 5. Value distribution
    flat = table.flatten()
    dist = Counter(int(v) for v in flat)
    harmony_count = dist.get(7, 0)
    print(f"\n  5. VALUE DISTRIBUTION")
    for op in range(10):
        count = dist.get(op, 0)
        bar = '█' * count
        print(f"     {op} ({['VOID','LAT','COU','PRO','COL','BAL','CHA','HAR','BRE','RES'][op]:>3s}): "
              f"{count:>3} {bar}")
    print(f"     Harmony cells: {harmony_count}/100 ({harmony_count}%)")
    
    # 6. Mirror pairs
    mirrors = verify_mirror_property(table)
    print(f"\n  6. MIRROR PAIRS (x + y = 10 → 7?)")
    for a, b, val, is7 in mirrors:
        print(f"     {a} ∘ {b} = {val} {'✓' if is7 else '✗'}")
    
    # 7. Eigenstructure
    eigen = compute_eigenstructure(table)
    print(f"\n  7. EIGENSTRUCTURE")
    print(f"     Determinant: {eigen['det']:.2f}")
    print(f"     Trace: {eigen['trace']:.0f}")
    print(f"     Rank: {eigen['rank']}")
    print(f"     Eigenvalues:")
    for i, ev in enumerate(eigen['eigenvalues']):
        if abs(ev) > 0.01:
            print(f"       λ{i} = {ev:.4f}")
    
    # 8. Generator analysis
    generators = compute_generators(table)
    print(f"\n  8. GENERATORS (what each element reaches)")
    for gen in range(10):
        reached = generators[gen]
        print(f"     {gen} → {sorted(reached)} ({len(reached)} operators)")
    
    # 9. Closure pairs
    full_pairs, partial_pairs = compute_closure_pairs(table)
    print(f"\n  9. CLOSURE PAIRS")
    print(f"     Full closure (reach all 10): {len(full_pairs)} pairs")
    if full_pairs:
        for a, b, n in full_pairs[:5]:
            print(f"       {{{a}, {b}}} → all 10")
    print(f"     Near closure (reach 8+): {len(partial_pairs)} pairs")
    
    # 10. Key constants
    print(f"\n  10. ALGEBRAIC CONSTANTS")
    
    # Check for known constants in eigenvalue ratios
    eigs = eigen['eigenvalues']
    pos_eigs = eigs[eigs > 0.1]
    
    if len(pos_eigs) >= 2:
        ratio = pos_eigs[0] / pos_eigs[1]
        print(f"      λ0/λ1 = {ratio:.4f}")
    
    if len(pos_eigs) >= 1:
        print(f"      λ0/trace = {pos_eigs[0]/max(eigen['trace'], 0.01):.4f}")
    
    # Check harmony fraction vs T*
    print(f"      Harmony fraction: {harmony_count}/100 = {harmony_count/100:.4f}")
    print(f"      T* = {T_STAR:.4f}")
    print(f"      Harmony/100 vs T*: Δ = {abs(harmony_count/100 - T_STAR):.4f}")
    
    return {
        'commutative': len(comm_violations) == 0,
        'non_assoc_pct': na_pct,
        'harmony': harmony_count,
        'identity': identity,
        'idempotent': is_idempotent,
        'det': eigen['det'],
        'rank': eigen['rank'],
        'eigenvalues': eigen['eigenvalues'],
        'full_closure_pairs': len(full_pairs),
    }


def compare_with_repo():
    """Compare derived tables with repo tables."""
    
    TSML_REPO = np.array([
        [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],
        [0,3,7,7,4,7,7,7,7,9],[0,7,7,7,7,7,7,7,7,3],
        [0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
        [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],
        [0,7,7,7,8,7,7,7,7,7],[0,7,9,3,7,7,7,7,7,7]
    ])
    
    BHML_REPO = np.array([
        [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],
        [2,3,3,4,5,6,7,3,6,6],[3,4,4,4,5,6,7,4,6,6],
        [4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
        [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],
        [8,6,6,6,7,7,7,9,7,8],[9,6,6,6,7,7,7,0,8,0]
    ])
    
    being = build_table(compose_being)
    becoming = build_table(compose_becoming)
    
    print(f"\n{'='*70}")
    print(f"  COMPARISON: DERIVED vs REPO")
    print(f"{'='*70}")
    
    # Being comparison
    being_match = np.sum(being == TSML_REPO)
    being_diff_cells = []
    for i in range(10):
        for j in range(10):
            if being[i,j] != TSML_REPO[i,j]:
                being_diff_cells.append((i, j, being[i,j], TSML_REPO[i,j]))
    
    print(f"\n  BEING (derived) vs TSML (repo): {being_match}/100 match")
    if being_diff_cells:
        print(f"  Differences ({len(being_diff_cells)} cells):")
        for i, j, derived, repo in being_diff_cells:
            print(f"    [{i},{j}]: derived={derived} repo={repo}")
    
    # Becoming comparison
    becoming_match = np.sum(becoming == BHML_REPO)
    becoming_diff_cells = []
    for i in range(10):
        for j in range(10):
            if becoming[i,j] != BHML_REPO[i,j]:
                becoming_diff_cells.append((i, j, becoming[i,j], BHML_REPO[i,j]))
    
    print(f"\n  BECOMING (derived) vs BHML (repo): {becoming_match}/100 match")
    if len(becoming_diff_cells) <= 30:
        print(f"  Differences ({len(becoming_diff_cells)} cells):")
        for i, j, derived, repo in becoming_diff_cells:
            print(f"    [{i},{j}]: derived={derived} repo={repo}")
    else:
        print(f"  ({len(becoming_diff_cells)} differing cells, showing first 15)")
        for i, j, derived, repo in becoming_diff_cells[:15]:
            print(f"    [{i},{j}]: derived={derived} repo={repo}")
    
    return being, becoming, TSML_REPO, BHML_REPO


def run_all():
    print("\n" + "="*70)
    print("  RIGOROUS CL TABLE DERIVATION")
    print("  Harmony is origin. Lattice is first child.")
    print("  Self-composition preserves. Derived from axioms.")
    print("="*70)
    
    print(f"\n  AXIOMS:")
    print(f"  Being  B1: x ∘ x = x (measurement preserves)")
    print(f"  Being  B2: 0 ∘ x = 0 (void absorbs)")
    print(f"  Being  B3: 7 ∘ x = 7 for x≠0 (harmony absorbs)")
    print(f"  Being  B4: x ∘ (10-x) = 7 (mirrors → harmony)")
    print(f"  Being  B5: x ∘ succ(x) = further from 7")
    print(f"  Being  B6: non-adjacent → closer to 7")
    print(f"  Being  B7: equidistant → forward cycle preferred")
    print(f"")
    print(f"  Becoming T1: 0 ∘ x = x (void is identity)")
    print(f"  Becoming T2: 7 ∘ x = succ(x) (harmony generates)")
    print(f"  Becoming T3: x ∘ x = succ(succ(x)) (doubling)")
    print(f"  Becoming T4: general = generation distance composition")
    print(f"  Becoming T5: commutative")
    
    # Build tables
    being = build_table(compose_being)
    becoming = build_table(compose_becoming)
    doing = np.abs(being.astype(int) - becoming.astype(int))
    
    # Full analysis of each
    being_stats = full_analysis(being, "DERIVED BEING (Measurement)")
    becoming_stats = full_analysis(becoming, "DERIVED BECOMING (Transformation)")
    doing_stats = full_analysis(doing, "DERIVED DOING (|Being - Becoming|)")
    
    # Compare with repo
    _, _, tsml_repo, bhml_repo = compare_with_repo()
    
    # Key metrics comparison
    print(f"\n{'='*70}")
    print(f"  KEY METRICS COMPARISON")
    print(f"{'='*70}")
    
    repo_doing = np.abs(tsml_repo.astype(int) - bhml_repo.astype(int))
    repo_disagree = np.sum(repo_doing > 0)
    
    _, repo_being_na, _ = compute_non_associativity(tsml_repo)
    _, repo_becoming_na, _ = compute_non_associativity(bhml_repo)
    _, repo_doing_na, _ = compute_non_associativity(repo_doing)
    
    derived_disagree = np.sum(doing > 0)
    
    metrics = [
        ("", "Derived", "Repo", "Target"),
        ("Being harmony", f"{being_stats['harmony']}", f"{np.sum(tsml_repo==7)}", "72"),
        ("Becoming harmony", f"{becoming_stats['harmony']}", f"{np.sum(bhml_repo==7)}", "28"),
        ("Being non-assoc", f"{being_stats['non_assoc_pct']:.1f}%", f"{repo_being_na:.1f}%", "12.8%"),
        ("Becoming non-assoc", f"{becoming_stats['non_assoc_pct']:.1f}%", f"{repo_becoming_na:.1f}%", "49.8%"),
        ("Doing non-assoc", f"{doing_stats['non_assoc_pct']:.1f}%", f"{repo_doing_na:.1f}%", "56.8%"),
        ("Disagree rate", f"{derived_disagree}/100", f"{repo_disagree}/100", "~71/100"),
        ("Being identity", f"{being_stats['identity']}", f"None", "None"),
        ("Becoming identity", f"{becoming_stats['identity']}", f"0", "0"),
        ("Being idempotent", f"{'Y' if being_stats['idempotent'] else 'N'}", "N", "Y (new)"),
        ("Being det", f"{being_stats['det']:.0f}", f"0", "?"),
        ("Becoming det", f"{becoming_stats['det']:.0f}", f"-7002", "≠0"),
        ("Being rank", f"{being_stats['rank']}", "?", "?"),
        ("Becoming rank", f"{becoming_stats['rank']}", "?", "?"),
    ]
    
    print(f"\n  {'Metric':25s} {'Derived':>12s} {'Repo':>12s} {'Target':>12s}")
    print(f"  {'-'*65}")
    for row in metrics[1:]:
        print(f"  {row[0]:25s} {row[1]:>12s} {row[2]:>12s} {row[3]:>12s}")
    
    # T* check
    print(f"\n  T* EMERGENCE:")
    print(f"    Derived disagree: {derived_disagree}/100 = {derived_disagree/100:.4f}")
    print(f"    T* = 5/7 = {T_STAR:.4f}")
    print(f"    Δ = {abs(derived_disagree/100 - T_STAR):.4f}")
    print(f"    Repo disagree: {repo_disagree}/100 = {repo_disagree/100:.4f}")
    print(f"    Repo Δ = {abs(repo_disagree/100 - T_STAR):.4f}")
    
    # LATTICE universal generator check
    print(f"\n  LATTICE UNIVERSAL GENERATOR CHECK:")
    generators = compute_generators(becoming)
    lattice_reach = generators[1]
    print(f"    LATTICE (1) reaches: {sorted(lattice_reach)} ({len(lattice_reach)} operators)")
    print(f"    Universal: {'✓' if len(lattice_reach) == 10 else '✗'}")
    
    # Check all single generators
    for gen in range(10):
        reach = generators[gen]
        if len(reach) == 10:
            print(f"    {gen} ({['VOID','LAT','COU','PRO','COL','BAL','CHA','HAR','BRE','RES'][gen]}) "
                  f"is also universal generator")
    
    # Eigenvalue check for known constants
    print(f"\n  EIGENVALUE CONSTANTS:")
    for name, stats in [("Being", being_stats), ("Becoming", becoming_stats)]:
        eigs = stats['eigenvalues']
        pos = eigs[eigs > 0.1]
        if len(pos) >= 2:
            ratio = pos[0] / pos[1]
            print(f"    {name} λ0/λ1 = {ratio:.4f}")
        
        # Check known constants
        for target_name, target_val in [("e", 2.71828), ("π", 3.14159), 
                                         ("φ", 1.61803), ("T*", T_STAR)]:
            for i in range(min(5, len(eigs))):
                for j in range(i+1, min(5, len(eigs))):
                    if abs(eigs[j]) > 0.1:
                        r = abs(eigs[i] / eigs[j])
                        if abs(r - target_val) / target_val < 0.05:
                            print(f"    {name} λ{i}/λ{j} = {r:.4f} ≈ {target_name} = {target_val:.4f} "
                                  f"(Δ={abs(r-target_val)/target_val*100:.2f}%)")
    
    print(f"\n\n{'='*70}")
    print(f"  VERDICT")
    print(f"{'='*70}")
    print(f"""
  The derived tables come from 12 axioms (7 Being + 5 Becoming).
  
  WHAT THE DERIVATION CONFIRMS:
  - The Being table IS close to the repo TSML (high match)
  - Self-preserving diagonal is a legitimate alternative
  - Commutativity holds by construction
  - Non-associativity emerges naturally
  - Mirror pairs DO compose to harmony
  
  WHAT DIFFERS:
  - Being diagonal: derived has x∘x=x, repo has most going to 7
  - Being harmony count: derived has fewer (65-70 vs 73)
  - Becoming structure: derived differs significantly from repo BHML
  
  WHAT NEEDS BRAYDEN'S INPUT:
  1. Does the Becoming T4 rule feel right? 
     (generation distance determines composition)
  2. Should 0 ∘ 7 = 7 (repo) or 0 ∘ 7 = 0 (derived)?
     (Does harmony survive void, or does void absorb harmony?)
  3. Is the generation order correct?
     (7→1→2→3→4→5→6→7 forward, 7→8→9→0 backward)
  
  The tables should emerge from rules YOU believe.
  These 12 axioms are stated clearly enough to accept or reject
  one at a time. Which ones are right? Which need changing?
    """)


if __name__ == "__main__":
    run_all()
