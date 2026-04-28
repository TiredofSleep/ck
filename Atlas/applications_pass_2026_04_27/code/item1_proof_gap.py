"""
Item 1: Empirical test of the σ-rate proof gap.

QUESTION: Do non-associative triples in binary CL[Z/NZ] have:
  (a) Always >=1 inner ECHO composition (CL(a,b) or CL(b,c) is ECHO-derived)
      → the paper's union bound logic is empirically defensible
  (b) Sometimes 0 inner ECHO compositions (only outer-site ECHO contributing)
      → the proof gap is real and needs joint-event argument

For each non-associative triple (a,b,c), classify by:
  inner_ab_is_echo: was CL(a,b) produced by Rule 3 (ECHO)?
  inner_bc_is_echo: was CL(b,c) produced by Rule 3 (ECHO)?
  outer_left_is_echo: was CL(CL(a,b), c) produced by Rule 3?
  outer_right_is_echo: was CL(a, CL(b,c)) produced by Rule 3?
"""
import math
import json

def build_dis_table(N):
    return [[abs((a + b) % N - (a * b) % N) for b in range(N)] for a in range(N)]

def build_binary_cl_with_provenance(N, harmony):
    """Build binary CL and track which rule fired at each cell."""
    dis = build_dis_table(N)
    table = [[0]*N for _ in range(N)]
    rule = [['']*N for _ in range(N)]  # which rule fired

    for a in range(N):
        for b in range(N):
            if a == harmony or b == harmony:
                table[a][b] = harmony
                rule[a][b] = 'HARM'
            elif a == 0:
                table[a][b] = 0
                rule[a][b] = 'VOID'
            elif b == 0:
                table[a][b] = 0
                rule[a][b] = 'VOID'
            elif dis[a][b] == 0:
                table[a][b] = (a + b) % N
                rule[a][b] = 'ECHO'
            else:
                table[a][b] = harmony
                rule[a][b] = 'DEFAULT'
    return table, rule

def find_harmony(N):
    """Find the highest-curvature unit in Z/NZ."""
    dis = build_dis_table(N)
    units = [a for a in range(1, N) if math.gcd(a, N) == 1]
    if not units:
        return None
    unit_curv = [(a, sum(dis[a][b] for b in range(N))/N) for a in units]
    unit_curv.sort(key=lambda x: -x[1])
    return unit_curv[0][0]

def classify_nonassoc_triples(N):
    """For each non-associative triple, classify by which rules fired where."""
    h = find_harmony(N)
    if h is None:
        return None
    table, rule = build_binary_cl_with_provenance(N, h)
    
    classification = {
        'total_triples': N**3,
        'nonassoc_triples': 0,
        'inner_ab_echo': 0,
        'inner_bc_echo': 0,
        'inner_either_echo': 0,
        'inner_both_echo': 0,
        'inner_neither_echo': 0,
        'outer_left_echo': 0,
        'outer_right_echo': 0,
        'outer_either_echo': 0,
        # Most important: how many non-assoc triples have ZERO inner ECHO?
        'nonassoc_with_no_inner_echo': 0,
        'nonassoc_with_one_inner_echo': 0,
        'nonassoc_with_two_inner_echo': 0,
    }
    
    examples_no_inner_echo = []
    
    for a in range(N):
        for b in range(N):
            for c in range(N):
                inner_ab = table[a][b]
                inner_bc = table[b][c]
                left = table[inner_ab][c]
                right = table[a][inner_bc]
                
                if left != right:
                    classification['nonassoc_triples'] += 1
                    
                    ab_is_echo = (rule[a][b] == 'ECHO')
                    bc_is_echo = (rule[b][c] == 'ECHO')
                    left_is_echo = (rule[inner_ab][c] == 'ECHO')
                    right_is_echo = (rule[a][inner_bc] == 'ECHO')
                    
                    inner_count = int(ab_is_echo) + int(bc_is_echo)
                    
                    if ab_is_echo:
                        classification['inner_ab_echo'] += 1
                    if bc_is_echo:
                        classification['inner_bc_echo'] += 1
                    if ab_is_echo or bc_is_echo:
                        classification['inner_either_echo'] += 1
                    if ab_is_echo and bc_is_echo:
                        classification['inner_both_echo'] += 1
                    if not ab_is_echo and not bc_is_echo:
                        classification['inner_neither_echo'] += 1
                        if len(examples_no_inner_echo) < 5:
                            examples_no_inner_echo.append({
                                'triple': (a, b, c),
                                'CL(a,b)': inner_ab, 'rule_ab': rule[a][b],
                                'CL(b,c)': inner_bc, 'rule_bc': rule[b][c],
                                'CL(CL(a,b),c)': left, 'rule_left': rule[inner_ab][c],
                                'CL(a,CL(b,c))': right, 'rule_right': rule[a][inner_bc],
                            })
                    
                    if left_is_echo:
                        classification['outer_left_echo'] += 1
                    if right_is_echo:
                        classification['outer_right_echo'] += 1
                    if left_is_echo or right_is_echo:
                        classification['outer_either_echo'] += 1
                    
                    if inner_count == 0:
                        classification['nonassoc_with_no_inner_echo'] += 1
                    elif inner_count == 1:
                        classification['nonassoc_with_one_inner_echo'] += 1
                    elif inner_count == 2:
                        classification['nonassoc_with_two_inner_echo'] += 1
    
    classification['harmony'] = h
    classification['examples_no_inner_echo'] = examples_no_inner_echo
    return classification

# Run for the verified N values from the paper
print("=" * 70)
print("ITEM 1: Empirical test of σ-rate proof gap")
print("=" * 70)
print()

results = {}
for N in [10, 30, 210]:
    print(f"--- N = {N} ---")
    c = classify_nonassoc_triples(N)
    results[N] = c
    
    nonassoc = c['nonassoc_triples']
    print(f"Harmony: {c['harmony']}")
    print(f"Total non-associative triples: {nonassoc}")
    print(f"σ(N) = {nonassoc/N**3:.6f}")
    print()
    print(f"Of these {nonassoc} non-associative triples:")
    print(f"  Inner CL(a,b) was ECHO:        {c['inner_ab_echo']:>6}  ({100*c['inner_ab_echo']/nonassoc:.1f}%)")
    print(f"  Inner CL(b,c) was ECHO:        {c['inner_bc_echo']:>6}  ({100*c['inner_bc_echo']/nonassoc:.1f}%)")
    print(f"  At least one inner ECHO:       {c['inner_either_echo']:>6}  ({100*c['inner_either_echo']/nonassoc:.1f}%)")
    print(f"  Both inner ECHO:               {c['inner_both_echo']:>6}  ({100*c['inner_both_echo']/nonassoc:.1f}%)")
    print(f"  ZERO inner ECHO (proof gap):   {c['inner_neither_echo']:>6}  ({100*c['inner_neither_echo']/nonassoc:.1f}%)")
    print()
    print(f"  Outer left was ECHO:           {c['outer_left_echo']:>6}")
    print(f"  Outer right was ECHO:          {c['outer_right_echo']:>6}")
    print()
    print(f"Distribution of inner ECHO counts:")
    print(f"  0 inner ECHO: {c['nonassoc_with_no_inner_echo']}")
    print(f"  1 inner ECHO: {c['nonassoc_with_one_inner_echo']}")
    print(f"  2 inner ECHO: {c['nonassoc_with_two_inner_echo']}")
    
    if c['examples_no_inner_echo']:
        print()
        print(f"Examples of non-associative triples with NO inner ECHO:")
        for ex in c['examples_no_inner_echo']:
            print(f"  triple {ex['triple']}: ", end='')
            print(f"CL(a,b)={ex['CL(a,b)']}({ex['rule_ab']}), CL(b,c)={ex['CL(b,c)']}({ex['rule_bc']})")
            print(f"    → CL(CL(a,b),c)={ex['CL(CL(a,b),c)']}({ex['rule_left']}), CL(a,CL(b,c))={ex['CL(a,CL(b,c))']}({ex['rule_right']})")
    print()

print("=" * 70)
print("VERDICT")
print("=" * 70)
total_nonassoc_no_inner = sum(results[N]['nonassoc_with_no_inner_echo'] for N in [10, 30, 210])
total_nonassoc = sum(results[N]['nonassoc_triples'] for N in [10, 30, 210])

if total_nonassoc_no_inner == 0:
    print()
    print("EMPIRICAL: Every non-associative triple in N ∈ {10, 30, 210} has")
    print("          at least one inner-site ECHO composition.")
    print()
    print("→ The paper's union bound on the two inner sites is empirically")
    print("  defensible. The proof's claim that 'non-associativity requires")
    print("  at least one ECHO inner composition' is verified for these N.")
    print()
    print("→ The 'proof gap' I flagged earlier is RESOLVED EMPIRICALLY:")
    print("  it doesn't manifest in the tested range. The proof's logic")
    print("  is correct as written; the formal tightening I suggested is")
    print("  unnecessary if (and this still needs proof) the property")
    print("  holds for all squarefree N.")
elif total_nonassoc_no_inner > 0:
    print()
    print(f"EMPIRICAL: {total_nonassoc_no_inner} non-associative triples across")
    print(f"          N ∈ {{10, 30, 210}} have NO inner-site ECHO.")
    print(f"          ({100*total_nonassoc_no_inner/total_nonassoc:.2f}% of non-assoc triples)")
    print()
    print("→ The proof gap is REAL. Outer-site ECHO can produce non-associativity")
    print("  even when neither inner composition is ECHO-derived.")
    print()
    print("→ The proof in §4 needs structural revision: either tighten to")
    print("  σ ≤ 2/N via joint-event argument, or concede σ ≤ 4/N with")
    print("  the union bound including outer sites.")
