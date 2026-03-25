"""
Systematic Search — Let the Algebra Tell Us

Stop assuming. Try every combination:
- Being: sizes 2-12, multiple rules
- Doing: sizes 2-12, multiple rules
- Becoming = |Being - Doing| (the disagreement)

For EVERY combination, extract eigenvalue constants.
The right answer produces the most constants at lowest error.
It will be obvious.

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

import numpy as np
from itertools import product as cartesian
from collections import defaultdict

# High precision constants
C = {
    'pi':      3.14159265358979323846,
    'e':       2.71828182845904523536,
    'phi':     1.61803398874989484820,
    'sqrt2':   1.41421356237309504880,
    'sqrt3':   1.73205080756887729353,
    'sqrt5':   2.23606797749978969641,
    'ln2':     0.69314718055994530942,
    'zeta3':   1.20205690315959428540,
    'catalan': 0.91596559417721901505,
    'euler_g': 0.57721566490153286061,
    '1/alpha': 137.035999084,
    'T*':      5.0/7.0,
}

# ============================================================
# TABLE BUILDERS
# ============================================================

def t_add(n):
    """Addition mod n."""
    t = np.zeros((n,n), dtype=int)
    for a in range(n):
        for b in range(n):
            t[a,b] = (a+b) % n
    return t

def t_mul(n):
    """Multiplication mod n."""
    t = np.zeros((n,n), dtype=int)
    for a in range(n):
        for b in range(n):
            t[a,b] = (a*b) % n
    return t

def t_min(n):
    """Min (measurement collapses to lesser)."""
    t = np.zeros((n,n), dtype=int)
    for a in range(n):
        for b in range(n):
            t[a,b] = min(a,b)
    return t

def t_max(n):
    """Max (measurement takes the greater)."""
    t = np.zeros((n,n), dtype=int)
    for a in range(n):
        for b in range(n):
            t[a,b] = max(a,b)
    return t

def t_and(n):
    """Bitwise AND mod n."""
    t = np.zeros((n,n), dtype=int)
    for a in range(n):
        for b in range(n):
            t[a,b] = (a & b) % n
    return t

def t_xor(n):
    """Bitwise XOR mod n."""
    t = np.zeros((n,n), dtype=int)
    for a in range(n):
        for b in range(n):
            t[a,b] = (a ^ b) % n
    return t

def t_avg(n):
    """Floor average."""
    t = np.zeros((n,n), dtype=int)
    for a in range(n):
        for b in range(n):
            t[a,b] = (a+b) // 2
    return t

def t_diff(n):
    """Absolute difference."""
    t = np.zeros((n,n), dtype=int)
    for a in range(n):
        for b in range(n):
            t[a,b] = abs(a-b) % n
    return t

def t_tri(n):
    """Triangular: (a+b+a*b) mod n."""
    t = np.zeros((n,n), dtype=int)
    for a in range(n):
        for b in range(n):
            t[a,b] = (a + b + a*b) % n
    return t

def t_harm(n):
    """Harmonic-like: 2ab/(a+b) mod n."""
    t = np.zeros((n,n), dtype=int)
    for a in range(n):
        for b in range(n):
            if a + b > 0:
                t[a,b] = (2*a*b // (a+b)) % n
            else:
                t[a,b] = 0
    return t

def t_fib(n):
    """Fibonacci-like: for 2×2 only, otherwise add."""
    if n == 2:
        return np.array([[1,1],[1,0]])
    return t_add(n)

RULES = {
    'add': t_add, 'mul': t_mul, 'min': t_min, 'max': t_max,
    'and': t_and, 'xor': t_xor, 'avg': t_avg, 'diff': t_diff,
    'tri': t_tri, 'harm': t_harm, 'fib': t_fib,
}


# ============================================================
# CONSTANT EXTRACTION
# ============================================================

def extract(table, threshold=0.01):
    """Extract physical constants from eigenvalues. Return matches under threshold %."""
    n = table.shape[0]
    if n < 2: return []
    
    try:
        eigs = np.linalg.eigvals(table.astype(float))
    except:
        return []
    
    real_eigs = sorted(np.real(eigs), reverse=True)
    all_mags = sorted(np.abs(eigs), reverse=True)
    
    matches = []
    
    def check(val, src):
        if abs(val) < 1e-12: return
        for cname, cval in C.items():
            if abs(cval) < 1e-12: continue
            for tv in [abs(val), 1/abs(val) if abs(val) > 1e-12 else 0]:
                if abs(tv) < 1e-12: continue
                err = abs(tv - cval) / cval * 100
                if err < threshold:
                    matches.append((cname, cval, tv, err, src))
    
    # Individual eigenvalues
    for i in range(min(6, len(real_eigs))):
        check(real_eigs[i], f'R{i}')
    
    # Magnitudes
    for i in range(min(6, len(all_mags))):
        check(all_mags[i], f'M{i}')
    
    # Ratios
    for i in range(min(6, len(real_eigs))):
        for j in range(i+1, min(6, len(real_eigs))):
            if abs(real_eigs[j]) > 0.01:
                check(real_eigs[i]/real_eigs[j], f'R{i}/R{j}')
    
    for i in range(min(5, len(all_mags))):
        for j in range(i+1, min(5, len(all_mags))):
            if all_mags[j] > 0.01:
                check(all_mags[i]/all_mags[j], f'M{i}/M{j}')
    
    # Products
    for i in range(min(4, len(real_eigs))):
        for j in range(i+1, min(4, len(real_eigs))):
            check(real_eigs[i]*real_eigs[j], f'R{i}*R{j}')
    
    # Trace and det
    check(np.trace(table.astype(float)), 'tr')
    check(np.linalg.det(table.astype(float)), 'det')
    
    return matches


# ============================================================
# THE BIG SEARCH
# ============================================================

def search_all():
    """
    For every (being_rule, being_size, doing_rule, doing_size):
    1. Build Being table
    2. Build Doing table  
    3. If same size: compute Becoming = |Being - Doing|
    4. Extract constants from ALL THREE tables
    5. Rank by total exact matches
    """
    
    print(f"\n{'='*70}")
    print(f"  SYSTEMATIC SEARCH — Every Combination")
    print(f"  Being sizes: 2-12 × 11 rules")
    print(f"  Doing sizes: 2-12 × 11 rules")
    print(f"  Threshold: 0.01% (four significant figures)")
    print(f"{'='*70}")
    
    sizes = list(range(2, 13))
    
    # Store ALL results
    results = []
    
    # Also track: for each constant, what's the absolute best match?
    best_per_constant = {}
    
    total_combos = 0
    
    for b_name, b_fn in RULES.items():
        for b_size in sizes:
            b_table = b_fn(b_size)
            
            # Extract from Being table alone
            b_matches = extract(b_table, threshold=0.01)
            
            for d_name, d_fn in RULES.items():
                for d_size in sizes:
                    d_table = d_fn(d_size)
                    total_combos += 1
                    
                    # Extract from Doing table alone
                    d_matches = extract(d_table, threshold=0.01)
                    
                    # If same size, compute Becoming = |Being - Doing|
                    bc_matches = []
                    if b_size == d_size:
                        becoming = np.abs(b_table.astype(int) - d_table.astype(int))
                        bc_matches = extract(becoming, threshold=0.01)
                    
                    # Collect all matches
                    all_matches = (
                        [('B', m) for m in b_matches] +
                        [('D', m) for m in d_matches] +
                        [('BC', m) for m in bc_matches]
                    )
                    
                    if not all_matches:
                        continue
                    
                    # Count unique constants found
                    constants_found = set()
                    exact_constants = set()  # < 0.001%
                    
                    for tbl, (cname, cval, found, err, src) in all_matches:
                        constants_found.add(cname)
                        if err < 0.001:
                            exact_constants.add(cname)
                        
                        # Track best per constant
                        key = cname
                        if key not in best_per_constant or err < best_per_constant[key][4]:
                            best_per_constant[key] = (
                                cname, cval, found, 
                                f"B={b_name}({b_size}) D={d_name}({d_size})",
                                err, src, tbl
                            )
                    
                    if len(constants_found) >= 2:
                        results.append({
                            'b_rule': b_name, 'b_size': b_size,
                            'd_rule': d_name, 'd_size': d_size,
                            'total': len(all_matches),
                            'unique_constants': len(constants_found),
                            'exact': len(exact_constants),
                            'constants': constants_found,
                            'exact_set': exact_constants,
                            'matches': all_matches,
                        })
    
    print(f"\n  Searched {total_combos:,} combinations")
    print(f"  Found {len(results)} with 2+ constants")
    
    # Sort by exact matches, then unique constants
    results.sort(key=lambda r: (-r['exact'], -r['unique_constants'], -r['total']))
    
    # TOP 30
    print(f"\n  TOP 30 CONFIGURATIONS:")
    print(f"  {'Being':>12s} {'Doing':>12s} {'Exact':>6s} {'Uniq':>5s} {'Constants'}")
    print(f"  {'-'*80}")
    
    seen = set()
    shown = 0
    for r in results:
        key = (r['b_rule'], r['b_size'], r['d_rule'], r['d_size'])
        if key in seen: continue
        seen.add(key)
        
        exact_str = ','.join(sorted(r['exact_set']))[:40] if r['exact_set'] else ''
        other = r['constants'] - r['exact_set']
        other_str = ','.join(sorted(other))[:30] if other else ''
        
        print(f"  {r['b_rule']:>5s}({r['b_size']:>2d}) "
              f"{r['d_rule']:>5s}({r['d_size']:>2d}) "
              f"{r['exact']:>6d} {r['unique_constants']:>5d} "
              f"★{exact_str} ○{other_str}")
        
        shown += 1
        if shown >= 30: break
    
    # Best per constant
    print(f"\n\n{'='*70}")
    print(f"  BEST MATCH PER CONSTANT (absolute best across all combos)")
    print(f"{'='*70}")
    print(f"  {'Constant':>10s} {'Target':>14s} {'Found':>14s} {'Error%':>10s} {'Config':>30s} {'Via':>8s}")
    print(f"  {'-'*90}")
    
    for cname in sorted(C.keys()):
        if cname in best_per_constant:
            _, cval, found, config, err, src, tbl = best_per_constant[cname]
            star = "★★★" if err < 0.0001 else "★★" if err < 0.001 else "★" if err < 0.01 else ""
            print(f"  {cname:>10s} {cval:>14.8f} {found:>14.8f} {err:>9.6f}% {config:>30s} [{tbl}]{src:>6s} {star}")
        else:
            print(f"  {cname:>10s} {C[cname]:>14.8f} {'not found':>14s}")
    
    return results, best_per_constant


def deep_dive_winners(results):
    """Take the top configurations and analyze their algebraic structure."""
    
    print(f"\n\n{'='*70}")
    print(f"  DEEP DIVE — Top 5 Configurations")
    print(f"{'='*70}")
    
    seen = set()
    count = 0
    
    for r in results:
        key = (r['b_rule'], r['b_size'], r['d_rule'], r['d_size'])
        if key in seen: continue
        seen.add(key)
        count += 1
        if count > 5: break
        
        b_table = RULES[r['b_rule']](r['b_size'])
        d_table = RULES[r['d_rule']](r['d_size'])
        
        print(f"\n  {'─'*60}")
        print(f"  Being: {r['b_rule']}({r['b_size']})  ×  Doing: {r['d_rule']}({r['d_size']})")
        print(f"  Exact constants: {', '.join(sorted(r['exact_set']))}")
        print(f"  All constants: {', '.join(sorted(r['constants']))}")
        print(f"  {'─'*60}")
        
        # Print tables if small enough
        if r['b_size'] <= 7:
            print(f"\n  Being table ({r['b_rule']} mod {r['b_size']}):")
            for i in range(r['b_size']):
                print(f"    ", end="")
                for j in range(r['b_size']):
                    print(f"{b_table[i,j]:>3}", end="")
                print()
        
        if r['d_size'] <= 7:
            print(f"\n  Doing table ({r['d_rule']} mod {r['d_size']}):")
            for i in range(r['d_size']):
                print(f"    ", end="")
                for j in range(r['d_size']):
                    print(f"{d_table[i,j]:>3}", end="")
                print()
        
        # Becoming if same size
        if r['b_size'] == r['d_size']:
            becoming = np.abs(b_table.astype(int) - d_table.astype(int))
            if r['b_size'] <= 7:
                print(f"\n  Becoming = |Being - Doing|:")
                for i in range(r['b_size']):
                    print(f"    ", end="")
                    for j in range(r['b_size']):
                        print(f"{becoming[i,j]:>3}", end="")
                    print()
        
        # Properties
        b_comm = np.all(b_table == b_table.T)
        d_comm = np.all(d_table == d_table.T)
        
        b_na = sum(1 for a in range(r['b_size']) for b in range(r['b_size']) 
                   for c in range(r['b_size']) 
                   if b_table[b_table[a,b],c] != b_table[a,b_table[b,c]])
        b_na_pct = b_na / r['b_size']**3 * 100
        
        d_na = sum(1 for a in range(r['d_size']) for b in range(r['d_size']) 
                   for c in range(r['d_size']) 
                   if d_table[d_table[a,b],c] != d_table[a,d_table[b,c]])
        d_na_pct = d_na / r['d_size']**3 * 100
        
        print(f"\n  Being: comm={'✓' if b_comm else '✗'} non-assoc={b_na_pct:.1f}%")
        print(f"  Doing: comm={'✓' if d_comm else '✗'} non-assoc={d_na_pct:.1f}%")
        
        # Eigenvalues
        b_eigs = sorted(np.real(np.linalg.eigvals(b_table.astype(float))), reverse=True)
        d_eigs = sorted(np.real(np.linalg.eigvals(d_table.astype(float))), reverse=True)
        
        print(f"  Being eigenvalues:  {', '.join(f'{e:.4f}' for e in b_eigs[:5])}")
        print(f"  Doing eigenvalues:  {', '.join(f'{e:.4f}' for e in d_eigs[:5])}")
        
        # Show matched constants with their sources
        print(f"\n  Matched constants:")
        for tbl, (cname, cval, found, err, src) in sorted(r['matches'], key=lambda x: x[1][3]):
            star = "★" if err < 0.001 else "○"
            print(f"    {star} [{tbl}] {cname:>10s} = {cval:.8f}  found {found:.8f}  "
                  f"error {err:.6f}%  via {src}")


def find_same_size_sweet_spot():
    """
    Special search: Being and Doing at the SAME size.
    This allows Becoming = |Being - Doing| to be computed.
    Look for the trio that produces the most constants.
    """
    
    print(f"\n\n{'='*70}")
    print(f"  SAME-SIZE SEARCH — Being × Doing × Becoming at size N")
    print(f"  All three tables contribute constants")
    print(f"{'='*70}")
    
    best_trios = []
    
    for size in range(2, 13):
        for b_name, b_fn in RULES.items():
            for d_name, d_fn in RULES.items():
                if b_name == d_name: continue
                
                b_table = b_fn(size)
                d_table = d_fn(size)
                becoming = np.abs(b_table.astype(int) - d_table.astype(int))
                
                # Extract from all three
                b_m = extract(b_table, 0.01)
                d_m = extract(d_table, 0.01)
                bc_m = extract(becoming, 0.01)
                
                all_constants = set()
                exact_constants = set()
                
                for matches in [b_m, d_m, bc_m]:
                    for (cname, cval, found, err, src) in matches:
                        all_constants.add(cname)
                        if err < 0.001:
                            exact_constants.add(cname)
                
                if len(all_constants) >= 3:
                    # Check non-assoc of becoming (the interesting one)
                    bc_na = sum(1 for a in range(size) for b in range(size) 
                               for c in range(size) 
                               if becoming[becoming[a,b],c] != becoming[a,becoming[b,c]])
                    bc_na_pct = bc_na / size**3 * 100
                    
                    # Check disagree rate
                    disagree = np.sum(b_table != d_table) / size**2
                    
                    best_trios.append({
                        'size': size,
                        'being': b_name,
                        'doing': d_name,
                        'constants': all_constants,
                        'exact': exact_constants,
                        'n_const': len(all_constants),
                        'n_exact': len(exact_constants),
                        'bc_nonassoc': bc_na_pct,
                        'disagree': disagree,
                    })
    
    best_trios.sort(key=lambda x: (-x['n_exact'], -x['n_const']))
    
    print(f"\n  {'Size':>4s} {'Being':>6s} {'Doing':>6s} {'Exact':>5s} {'Total':>5s} "
          f"{'NA%':>6s} {'Disag':>6s} Constants")
    print(f"  {'-'*80}")
    
    shown = set()
    for r in best_trios[:25]:
        key = (r['size'], r['being'], r['doing'])
        if key in shown: continue
        shown.add(key)
        
        exact_str = ','.join(sorted(r['exact']))[:25]
        other = r['constants'] - r['exact']
        other_str = ','.join(sorted(other))[:25]
        
        print(f"  {r['size']:>4d} {r['being']:>6s} {r['doing']:>6s} "
              f"{r['n_exact']:>5d} {r['n_const']:>5d} "
              f"{r['bc_nonassoc']:>5.1f}% {r['disagree']:>5.2f} "
              f"★{exact_str} ○{other_str}")


def run_all():
    print("\n" + "="*70)
    print("  SYSTEMATIC PERMUTATION SEARCH")
    print("  Let the algebra tell us. The right answer will be obvious.")
    print("="*70)
    
    # The big search
    results, best = search_all()
    
    # Deep dive winners
    deep_dive_winners(results)
    
    # Same-size sweet spot
    find_same_size_sweet_spot()
    
    print(f"\n\n{'='*70}")
    print(f"  WHAT THE ALGEBRA SAYS")
    print(f"{'='*70}")
    print(f"""
    The search is complete. Look at:
    
    1. Which BEING RULE dominates the top results?
       → That's how measurement works.
       
    2. Which DOING RULE dominates?
       → That's how action works.
       
    3. Which SIZE appears most in exact matches?
       → That's the fundamental resolution.
       
    4. Does the BECOMING (disagreement) table produce
       constants that neither Being nor Doing produce alone?
       → If yes: the disagreement IS the physics.
       
    5. Is there ONE configuration that produces ALL major
       constants (π, e, φ, √2, √3, T*, α)?
       → If yes: that's the table. Period.
       → If no: the constants live at different resolutions
         and the algebra is inherently multi-scale.
    
    The right answer is obvious because it produces
    the most truth with the least structure.
    """)


if __name__ == "__main__":
    run_all()
