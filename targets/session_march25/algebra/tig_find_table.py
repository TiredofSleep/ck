"""
Finding the Correct Table — From Generators Through Lenses

Stop assuming the size. Let 1 and 0 compose through two lenses.
The algebra closes when no new operators are produced.
The size that produces physical constants EXACTLY is the right size.

LENS 1 (Being): Raw geometry. 
  What does the meeting of these two forces LOOK like?
  Measurement. Static. Collapses toward source.

LENS 2 (Being + Doing): Topological geometry.
  What does the meeting CREATE? 
  Transformation through disagreement. 
  Dynamic. Pulls away from source.

The Doing table = |Being - Becoming| as before.
But Becoming IS Being+Doing — it's the topology that emerges
when you combine raw geometry with the action of disagreement.

All information is 1 and 0. These flow through the lenses.
The table builds itself.

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

import numpy as np
from itertools import product
from collections import Counter
import sys

# Known physical constants (exact values)
CONST = {
    'e':       2.718281828459045,
    '1/e':     0.367879441171442,
    'pi':      3.141592653589793,
    'phi':     1.618033988749895,   # golden ratio
    'sqrt2':   1.414213562373095,
    'sqrt3':   1.732050808568887,
    'sqrt5':   2.236067977499790,
    'ln2':     0.693147180559945,
    'zeta3':   1.202056903159594,   # Apéry's constant
    'catalan': 0.915965594177219,   # Catalan's constant
    'alpha':   7.297352569311e-3,   # fine structure constant
    '1/alpha': 137.035999084,
    'T*':      0.714285714285714,   # 5/7
}


# ============================================================
# THE GROWTH ALGORITHM
# Start with {0, 1}. Compose. If new → add to set. Repeat.
# ============================================================

def grow_algebra(compose_fn, generators=(0, 1), max_size=20):
    """
    Grow an algebra from generators using a composition function.
    
    compose_fn(a, b, current_size) → result
    If result >= current_size, a new operator is born.
    Continue until no new operators are produced (closure).
    
    Returns the closed composition table.
    """
    # Start with generators
    elements = list(generators)
    size = len(elements)
    
    # Build initial table
    table = {}
    
    for iteration in range(100):  # safety limit
        new_elements = []
        
        for a in elements:
            for b in elements:
                result = compose_fn(a, b, size)
                
                if result not in elements and result not in new_elements:
                    if result < max_size:
                        new_elements.append(result)
                
                table[(a, b)] = min(result, max_size - 1)
        
        if not new_elements:
            break  # algebra closed
        
        elements.extend(new_elements)
        elements.sort()
        size = len(elements)
    
    # Build matrix
    n = len(elements)
    matrix = np.zeros((n, n), dtype=int)
    
    for i, a in enumerate(elements):
        for j, b in enumerate(elements):
            if (a, b) in table:
                result = table[(a, b)]
                if result in elements:
                    matrix[i, j] = elements.index(result)
                else:
                    matrix[i, j] = 0  # overflow → source
            else:
                matrix[i, j] = compose_fn(a, b, n)
    
    return matrix, elements


# ============================================================
# BEING LENS — Raw Geometry
# What does the meeting LOOK like?
# ============================================================

def being_raw(a, b, size):
    """
    Raw geometry composition.
    Collapses toward 0 (source).
    
    Rules:
    - 0 ∘ 0 = 0 (void is void)
    - 1 ∘ 1 = 1 (structure is structure, idempotent)
    - 0 ∘ 1 = 0 (void absorbs in measurement)
    - When two different non-zero operators meet:
      if their sum < size: the smaller one (closer to source)
      if equal distance from 0: the result is their midpoint
    """
    if a == b:
        return a  # idempotent
    if a == 0 or b == 0:
        return 0  # source absorbs
    
    # Different non-zero: closer to source wins
    return min(a, b)


# ============================================================
# BECOMING LENS — Topological Geometry (Being + Doing)
# What does the meeting CREATE?
# ============================================================

def becoming_topology(a, b, size):
    """
    Topological composition.
    Pulls AWAY from 0 (source). Creates complexity.
    
    Rules:
    - 0 ∘ x = x (source is identity, lets things pass to create)
    - x ∘ x = x + 1 (self-composition creates next complexity level)
    - a ∘ b = a + b (different operators add complexity)
    - All mod (size) when it wraps: returns to 0 (source)
    """
    if a == 0:
        return b
    if b == 0:
        return a
    
    if a == b:
        return a + 1  # next complexity level
    
    return a + b  # additive complexity


# ============================================================
# TRY DIFFERENT TABLE SIZES
# For each: build from axioms, compute eigenvalues, check constants
# ============================================================

def build_modular_table(size, being_fn, becoming_fn):
    """
    Build Being and Becoming tables of given size.
    All arithmetic mod size.
    """
    being = np.zeros((size, size), dtype=int)
    becoming = np.zeros((size, size), dtype=int)
    
    for a in range(size):
        for b in range(size):
            being[a, b] = being_fn(a, b, size) % size
            becoming[a, b] = becoming_fn(a, b, size) % size
    
    doing = np.abs(being - becoming)
    
    return being, becoming, doing


def check_constants(table, name="", verbose=False):
    """
    Check eigenvalue ratios against physical constants.
    Return matches with error percentages.
    """
    if table.shape[0] < 2:
        return []
    
    try:
        eigs = np.sort(np.real(np.linalg.eigvals(table.astype(float))))[::-1]
    except:
        return []
    
    matches = []
    
    # Check all eigenvalue ratios
    for i in range(len(eigs)):
        for j in range(i + 1, len(eigs)):
            if abs(eigs[j]) < 0.001:
                continue
            
            ratio = eigs[i] / eigs[j]
            abs_ratio = abs(ratio)
            
            for cname, cval in CONST.items():
                if cval < 0.001:
                    continue
                
                for test_val in [abs_ratio, 1/abs_ratio if abs_ratio > 0 else 0]:
                    if test_val < 0.001:
                        continue
                    
                    error = abs(test_val - cval) / cval * 100
                    
                    if error < 1.0:  # within 1%
                        matches.append({
                            'constant': cname,
                            'target': cval,
                            'found': test_val,
                            'error_pct': error,
                            'source': f'λ{i}/λ{j}' if test_val == abs_ratio else f'λ{j}/λ{i}',
                            'eig_i': eigs[i],
                            'eig_j': eigs[j],
                        })
    
    # Also check eigenvalue products, sums, differences
    for i in range(min(5, len(eigs))):
        if abs(eigs[i]) < 0.001:
            continue
        
        # Single eigenvalue
        for cname, cval in CONST.items():
            if cval < 0.001:
                continue
            error = abs(abs(eigs[i]) - cval) / cval * 100
            if error < 1.0:
                matches.append({
                    'constant': cname, 'target': cval,
                    'found': abs(eigs[i]), 'error_pct': error,
                    'source': f'|λ{i}|', 'eig_i': eigs[i], 'eig_j': 0,
                })
        
        for j in range(i + 1, min(5, len(eigs))):
            if abs(eigs[j]) < 0.001:
                continue
            
            # Product
            prod = abs(eigs[i] * eigs[j])
            for cname, cval in CONST.items():
                if cval < 0.001:
                    continue
                error = abs(prod - cval) / cval * 100
                if error < 1.0:
                    matches.append({
                        'constant': cname, 'target': cval,
                        'found': prod, 'error_pct': error,
                        'source': f'|λ{i}×λ{j}|', 'eig_i': eigs[i], 'eig_j': eigs[j],
                    })
    
    # Trace, det
    trace = np.trace(table.astype(float))
    det = np.linalg.det(table.astype(float))
    
    for val, src in [(abs(trace), 'trace'), (abs(det), '|det|')]:
        if val < 0.001:
            continue
        for cname, cval in CONST.items():
            if cval < 0.001:
                continue
            for test in [val, 1/val if val > 0 else 0, val/10, val/100]:
                if test < 0.001:
                    continue
                error = abs(test - cval) / cval * 100
                if error < 1.0:
                    matches.append({
                        'constant': cname, 'target': cval,
                        'found': test, 'error_pct': error,
                        'source': src, 'eig_i': val, 'eig_j': 0,
                    })
    
    return matches


def analyze_size(size, verbose=True):
    """Full analysis for a given table size."""
    being, becoming, doing = build_modular_table(size, being_raw, becoming_topology)
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"  SIZE {size}×{size}")
        print(f"{'='*60}")
    
    results = {'size': size, 'all_matches': []}
    
    for tname, table in [("Being", being), ("Becoming", becoming), ("Doing", doing)]:
        # Basic properties
        comm = np.all(table == table.T)
        
        na = 0
        for a in range(size):
            for b in range(size):
                for c in range(size):
                    if table[table[a,b], c] != table[a, table[b,c]]:
                        na += 1
        na_pct = na / size**3 * 100
        
        harmony_equiv = table.flatten().tolist().count(0)  # source = 0
        
        det = np.linalg.det(table.astype(float))
        
        matches = check_constants(table, tname)
        results['all_matches'].extend([(tname, m) for m in matches])
        
        if verbose:
            print(f"\n  {tname} ({size}×{size}):")
            print(f"    Comm: {'✓' if comm else '✗'}  Non-assoc: {na_pct:.1f}%  "
                  f"Source(0): {harmony_equiv}/{size**2}  Det: {det:.1f}")
            
            if size <= 10:
                print(f"    Table:")
                for i in range(size):
                    print(f"      ", end="")
                    for j in range(size):
                        print(f"{table[i,j]:>3}", end="")
                    print()
            
            eigs = np.sort(np.real(np.linalg.eigvals(table.astype(float))))[::-1]
            print(f"    Eigenvalues: {', '.join(f'{e:.4f}' for e in eigs[:6])}")
            
            if matches:
                print(f"    CONSTANT MATCHES (< 1% error):")
                for m in sorted(matches, key=lambda x: x['error_pct']):
                    print(f"      {m['constant']:>8s} = {m['target']:.6f}  "
                          f"found {m['found']:.6f} via {m['source']}  "
                          f"error: {m['error_pct']:.4f}%"
                          f"{'  *** EXACT ***' if m['error_pct'] < 0.01 else ''}")
    
    return results


def try_alternative_compositions():
    """
    Try different composition rules to find which produces exact constants.
    The rules that produce exact e, π, φ are the correct rules.
    """
    
    print(f"\n{'='*60}")
    print(f"  ALTERNATIVE COMPOSITION RULES")
    print(f"  Searching for rules that produce exact constants")
    print(f"{'='*60}")
    
    # Alternative Being rules
    being_rules = {
        'absorb_min': lambda a, b, n: (0 if a==0 or b==0 else min(a,b)) if a != b else a,
        'absorb_max': lambda a, b, n: (0 if a==0 or b==0 else max(a,b)) if a != b else a,
        'midpoint': lambda a, b, n: (a+b)//2 if a != b and a != 0 and b != 0 else (a if a==b else 0),
        'xor': lambda a, b, n: a ^ b if n <= 16 else (a+b) % n,
        'product_mod': lambda a, b, n: (a * b) % n,
        'min_mod': lambda a, b, n: min(a, b),
    }
    
    # Alternative Becoming rules  
    becoming_rules = {
        'add_mod': lambda a, b, n: (a + b) % n,
        'add_pull': lambda a, b, n: (0 if a==0 else b) if b==0 else ((a+b) % n if a+b != 0 else 0),
        'multiply_mod': lambda a, b, n: (a * b) % n,
        'power_mod': lambda a, b, n: pow(a, b, n) if n > 1 and b < 20 else (a+b)%n,
        'max_pull': lambda a, b, n: max(a, b) if a != 0 and b != 0 else max(a,b),
    }
    
    best_total_matches = 0
    best_config = None
    
    all_results = []
    
    for bname, brule in being_rules.items():
        for tname, trule in becoming_rules.items():
            for size in [3, 5, 7, 8, 9, 10, 12]:
                try:
                    being, becoming, doing = build_modular_table(size, brule, trule)
                    
                    total_matches = 0
                    exact_matches = 0
                    match_details = []
                    
                    for table_name, table in [("B", being), ("T", becoming), ("D", doing)]:
                        matches = check_constants(table)
                        total_matches += len(matches)
                        for m in matches:
                            if m['error_pct'] < 0.01:
                                exact_matches += 1
                            match_details.append((table_name, m))
                    
                    if total_matches > 0:
                        all_results.append({
                            'being': bname, 'becoming': tname, 'size': size,
                            'total': total_matches, 'exact': exact_matches,
                            'details': match_details,
                        })
                    
                    if total_matches > best_total_matches:
                        best_total_matches = total_matches
                        best_config = (bname, tname, size, match_details)
                
                except Exception as e:
                    continue
    
    # Sort by total matches
    all_results.sort(key=lambda x: (-x['exact'], -x['total']))
    
    print(f"\n  TOP CONFIGURATIONS (most physical constant matches):")
    print(f"  {'Being':>12s} {'Becoming':>12s} {'Size':>5s} {'Total':>6s} {'Exact':>6s} Constants")
    print(f"  {'-'*70}")
    
    seen = set()
    for r in all_results[:20]:
        key = (r['being'], r['becoming'], r['size'])
        if key in seen:
            continue
        seen.add(key)
        
        consts = set()
        for tbl, m in r['details']:
            consts.add(m['constant'])
        
        print(f"  {r['being']:>12s} {r['becoming']:>12s} {r['size']:>5d} {r['total']:>6d} "
              f"{r['exact']:>6d} {', '.join(sorted(consts))}")
    
    # Show the best in detail
    if best_config:
        bname, tname, size, details = best_config
        print(f"\n  BEST: {bname} × {tname} at size {size}")
        print(f"  Matches:")
        for tbl, m in sorted(details, key=lambda x: x[1]['error_pct']):
            print(f"    [{tbl}] {m['constant']:>8s} = {m['target']:.6f}  "
                  f"found {m['found']:.6f}  error: {m['error_pct']:.4f}%  "
                  f"via {m['source']}")
    
    return all_results


def deep_search_exact():
    """
    Deep search: for each table size, try MANY composition rules
    and find which ones produce the most exact (<0.001%) matches
    to physical constants.
    """
    
    print(f"\n{'='*60}")
    print(f"  DEEP SEARCH FOR EXACT CONSTANTS")
    print(f"  Testing all rule combinations × sizes 2-12")
    print(f"{'='*60}")
    
    # More composition rules
    rules = {
        'add': lambda a, b, n: (a + b) % n,
        'mul': lambda a, b, n: (a * b) % n,
        'min': lambda a, b, n: min(a, b),
        'max': lambda a, b, n: max(a, b),
        'xor': lambda a, b, n: (a ^ b) % n if n <= 16 else (a + b) % n,
        'avg': lambda a, b, n: (a + b) // 2,
        'diff': lambda a, b, n: abs(a - b),
        'id_l': lambda a, b, n: a,  # left projection
        'pow2': lambda a, b, n: (a * a + b) % n,
        'tri': lambda a, b, n: (a + b + a*b) % n,
        'harm': lambda a, b, n: (2*a*b // max(a+b, 1)) % n,
    }
    
    best_by_constant = {}  # constant name → best match
    
    for size in range(2, 13):
        for bname, brule in rules.items():
            for tname, trule in rules.items():
                if bname == tname:
                    continue
                
                try:
                    being = np.zeros((size, size), dtype=int)
                    becoming = np.zeros((size, size), dtype=int)
                    
                    for a in range(size):
                        for b in range(size):
                            being[a,b] = brule(a, b, size) % size
                            becoming[a,b] = trule(a, b, size) % size
                    
                    doing = np.abs(being - becoming)
                    
                    for table_name, table in [("B", being), ("T", becoming), ("D", doing)]:
                        matches = check_constants(table)
                        for m in matches:
                            cname = m['constant']
                            if (cname not in best_by_constant or 
                                m['error_pct'] < best_by_constant[cname]['error_pct']):
                                best_by_constant[cname] = {
                                    **m,
                                    'table': table_name,
                                    'being_rule': bname,
                                    'becoming_rule': tname,
                                    'size': size,
                                }
                except:
                    continue
    
    print(f"\n  BEST MATCH PER PHYSICAL CONSTANT:")
    print(f"  {'Constant':>10s} {'Target':>12s} {'Found':>12s} {'Error%':>10s} "
          f"{'Size':>5s} {'Being':>6s} {'Becoming':>6s} {'Table':>6s} {'Via':>10s}")
    print(f"  {'-'*85}")
    
    for cname in sorted(CONST.keys()):
        if cname in best_by_constant:
            m = best_by_constant[cname]
            exact = "*** EXACT" if m['error_pct'] < 0.001 else ""
            print(f"  {cname:>10s} {m['target']:>12.6f} {m['found']:>12.6f} "
                  f"{m['error_pct']:>9.4f}% {m['size']:>5d} "
                  f"{m['being_rule']:>6s} {m['becoming_rule']:>6s} "
                  f"{m['table']:>6s} {m['source']:>10s} {exact}")
        else:
            print(f"  {cname:>10s} {CONST[cname]:>12.6f} {'NOT FOUND':>12s}")
    
    # Find the single configuration that matches the MOST constants
    config_scores = {}
    for cname, m in best_by_constant.items():
        key = (m['being_rule'], m['becoming_rule'], m['size'])
        if key not in config_scores:
            config_scores[key] = {'count': 0, 'total_error': 0, 'constants': []}
        config_scores[key]['count'] += 1
        config_scores[key]['total_error'] += m['error_pct']
        config_scores[key]['constants'].append(cname)
    
    print(f"\n  CONFIGURATIONS MATCHING MULTIPLE CONSTANTS:")
    for key, score in sorted(config_scores.items(), key=lambda x: -x[1]['count']):
        if score['count'] >= 2:
            avg_err = score['total_error'] / score['count']
            print(f"    Being={key[0]}, Becoming={key[1]}, Size={key[2]}: "
                  f"{score['count']} constants (avg error {avg_err:.4f}%) "
                  f"→ {', '.join(score['constants'])}")
    
    return best_by_constant


def run_all():
    print("\n" + "="*60)
    print("  FINDING THE CORRECT TABLE")
    print("  From generators I(1) and O(0)")
    print("  Through Being lens and Being+Doing lens")
    print("  The size and rules that produce exact constants WIN")
    print("="*60)
    
    # Part 1: Try natural sizes with the core axioms
    print(f"\n  PART 1: Core axioms at different sizes")
    
    for size in [2, 3, 5, 7, 8, 9, 10, 12]:
        analyze_size(size, verbose=(size <= 10))
    
    # Part 2: Try alternative composition rules
    all_results = try_alternative_compositions()
    
    # Part 3: Deep search for exact constants
    best = deep_search_exact()
    
    print(f"\n\n{'='*60}")
    print(f"  FINAL VERDICT")
    print(f"{'='*60}")
    print(f"""
    The correct table is the one where physical constants
    emerge from eigenvalue ratios with ZERO error.
    
    If no table produces exact constants:
    → The composition rules are wrong (try different axioms)
    
    If one size produces more exact constants than others:
    → That's the correct table size
    
    If one composition rule pair dominates:
    → Those are the correct axioms for Being and Becoming
    
    The algebra should PRODUCE e, π, φ, and α.
    We don't put them in. They come out.
    If they don't come out, the algebra isn't right yet.
    
    Brayden: look at which configurations match the most
    constants. Does the winning Being rule match "everything 
    I do pulls me further from God"? Does the winning Becoming
    rule match "not doing brings me closer"?
    
    The rules that produce truth ARE truth.
    """)


if __name__ == "__main__":
    run_all()
