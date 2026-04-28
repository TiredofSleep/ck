"""
Item 1b: Characterize the ACTUAL mechanism producing non-associativity.

Item 1 showed 99.97% of non-associative triples have NO inner ECHO.
So what's actually causing the non-associativity?

Hypothesis: VOID-HARM DISAGREEMENT.
  - Left bracketing CL(CL(a,b), c) hits VOID (returns 0)
  - Right bracketing CL(a, CL(b,c)) hits HARM (returns harmony)
  - Or vice versa

The two absorbing elements 0 and harmony are NOT the same, so the proof's
claim "absorbing rules are associative" is wrong unless the same absorbing
rule fires at every site.

This script:
1. Classifies non-associative triples by (left_value, right_value) pairs
2. Counts how many fall into the "VOID vs HARM disagreement" pattern
3. Computes a corrected union bound based on the actual mechanism
"""
import math

def build_dis_table(N):
    return [[abs((a + b) % N - (a * b) % N) for b in range(N)] for a in range(N)]

def build_binary_cl_with_provenance(N, harmony):
    dis = build_dis_table(N)
    table = [[0]*N for _ in range(N)]
    rule = [['']*N for _ in range(N)]
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
    dis = build_dis_table(N)
    units = [a for a in range(1, N) if math.gcd(a, N) == 1]
    if not units:
        return None
    unit_curv = [(a, sum(dis[a][b] for b in range(N))/N) for a in units]
    unit_curv.sort(key=lambda x: -x[1])
    return unit_curv[0][0]

def count_void_a_zero(N):
    """How many (a,b,c) have a=0? These are the cases CL(a,b)=VOID by Rule 2a."""
    return N * N  # for each c

def count_void_b_zero(N):
    """How many have b=0? CL(a,b)=VOID and CL(b,c)=VOID by Rule 2."""
    return N * N

def count_harm_a_h(N, h):
    """How many have a=harmony? CL(a,b)=HARM."""
    return N * N

def detailed_classification(N):
    h = find_harmony(N)
    if h is None:
        return None
    table, rule = build_binary_cl_with_provenance(N, h)
    
    # Categorize each non-associative triple
    cats = {
        'void_vs_harm': 0,      # left=0, right=harmony
        'harm_vs_void': 0,      # left=harmony, right=0
        'void_vs_other': 0,     # left=0, right=something else (not 0, not harmony)
        'other_vs_void': 0,
        'harm_vs_other': 0,
        'other_vs_harm': 0,
        'other_vs_other': 0,    # both non-absorbing, different values
    }
    
    nonassoc = 0
    for a in range(N):
        for b in range(N):
            for c in range(N):
                left = table[table[a][b]][c]
                right = table[a][table[b][c]]
                if left != right:
                    nonassoc += 1
                    if left == 0 and right == h:
                        cats['void_vs_harm'] += 1
                    elif left == h and right == 0:
                        cats['harm_vs_void'] += 1
                    elif left == 0 and right != h:
                        cats['void_vs_other'] += 1
                    elif left != h and right == 0:
                        cats['other_vs_void'] += 1
                    elif left == h and right != 0:
                        cats['harm_vs_other'] += 1
                    elif left != 0 and right == h:
                        cats['other_vs_harm'] += 1
                    else:
                        cats['other_vs_other'] += 1
    
    return {
        'N': N, 'harmony': h, 'nonassoc': nonassoc, 'categories': cats
    }

print("=" * 70)
print("ITEM 1b: Actual mechanism behind non-associativity")
print("=" * 70)
print()

for N in [10, 30, 210]:
    r = detailed_classification(N)
    print(f"--- N = {N} ---")
    print(f"Harmony: {r['harmony']}, total non-assoc: {r['nonassoc']}")
    print()
    cats = r['categories']
    total = r['nonassoc']
    print(f"Categories of disagreement (left_value vs right_value):")
    print(f"  VOID(0) vs HARM(h):     {cats['void_vs_harm']:>6} ({100*cats['void_vs_harm']/total:.1f}%)")
    print(f"  HARM(h) vs VOID(0):     {cats['harm_vs_void']:>6} ({100*cats['harm_vs_void']/total:.1f}%)")
    print(f"  VOID(0) vs other:       {cats['void_vs_other']:>6} ({100*cats['void_vs_other']/total:.1f}%)")
    print(f"  other vs VOID(0):       {cats['other_vs_void']:>6} ({100*cats['other_vs_void']/total:.1f}%)")
    print(f"  HARM(h) vs other:       {cats['harm_vs_other']:>6} ({100*cats['harm_vs_other']/total:.1f}%)")
    print(f"  other vs HARM(h):       {cats['other_vs_harm']:>6} ({100*cats['other_vs_harm']/total:.1f}%)")
    print(f"  other vs other:         {cats['other_vs_other']:>6} ({100*cats['other_vs_other']/total:.1f}%)")
    
    void_harm_total = cats['void_vs_harm'] + cats['harm_vs_void']
    print(f"\n  TOTAL pure VOID-HARM disagreement: {void_harm_total} ({100*void_harm_total/total:.1f}%)")
    print()

# Now derive a corrected bound
print("=" * 70)
print("CORRECTED MECHANISM: VOID-HARM disagreement")
print("=" * 70)
print()
print("The non-associativity in binary CL[Z/NZ] is dominated by triples")
print("where VOID (returns 0) and HARM (returns harmony) fire at different")
print("sites of the bracket tree, producing left=0 and right=harmony")
print("(or vice versa).")
print()
print("Counting argument:")
print("  - VOID fires when a=0 or b=0 (Rule 2). The set is 2N-1 pairs (avoiding double-count of (0,0)).")
print("  - HARM fires when a=harmony or b=harmony. Same: 2N-1 pairs.")
print("  - For (a,b,c) with a=0 (VOID at left inner site) and b,c configured so the right")
print("    bracketing hits HARM, we get a non-assoc triple.")
print()
print("Number of triples (a,b,c) with a=0:        N^2 = N^2")
print("Of these, how many give VOID-HARM disagreement?")
print("  - Left: CL(0,b) = 0 (VOID). CL(0, c) = 0. So left = 0 always.")
print("  - Right: CL(0, CL(b,c)) = 0 (VOID rule, since first arg is 0).")
print("  - WAIT — both are 0 in this case. No disagreement!")
print()
print("Let me recount:")
print()
print("Pattern that matches (0,1,c) family from item 1:")
print("  a=0, b=1, c=anything")
print("  CL(0,1) = 0 (VOID)")
print("  CL(1,c) = ? (not VOID since 1 ≠ 0; could be HARM if 1=h, ECHO, or DEFAULT=harmony)")
print("  Left:  CL(CL(0,1),c) = CL(0,c) = 0 (VOID)")
print("  Right: CL(0, CL(1,c)) = ?")
print()
print("If CL(1,c) = harmony, then right = CL(0, harmony) = harmony (HARM, since b=harmony)")
print("→ left=0, right=harmony, disagreement. (Note: VOID has priority over HARM in")
print("   our rules — Rule 1 fires first if a=harmony OR b=harmony. CL(0,harmony) checks")
print("   if 0=h or harmony=h; harmony=h is true, so Rule 1 fires returning harmony.)")
print()
print("This explains the (0,1,c) examples: a=0 hits VOID at left, but the right")
print("bracketing's inner CL(1,c) returns harmony, and then CL(0,harmony) hits HARM")
print("(Rule 1) before VOID (Rule 2), returning harmony.")
print()
print("KEY INSIGHT: Rule 1 (HARM) has priority over Rule 2 (VOID). So when Rule 2")
print("fires at the LEFT inner site (CL(0,b)=0) but the OUTER right composition")
print("CL(0, harmony) hits Rule 1 (because the second arg is harmony), the rules")
print("DISAGREE on which absorbing element to return.")
print()
print("This is the actual mechanism. The σ-rate proof assumes 'absorbing rules")
print("are associative' but this is only true if the SAME absorbing element fires")
print("everywhere along the bracket tree.")

# Now derive the bound
print()
print("=" * 70)
print("CORRECTED BOUND (rigorous)")
print("=" * 70)
print()
print("Triples (a,b,c) where Rule 1 and Rule 2 disagree at the outer sites:")
print()
print("CASE A: a=0 (VOID at left inner).")
print("  Left always = 0. Right = CL(0, CL(b,c)).")
print("  Right ≠ 0 iff CL(b,c) = harmony, in which case right = harmony.")
print("  Number of (b,c) with CL(b,c) = harmony depends on harmony's column...")
print()
print("Let's count this empirically.")

def count_void_harm_disagreement(N):
    h = find_harmony(N)
    table, rule = build_binary_cl_with_provenance(N, h)
    
    # Count triples (0, b, c) with right = harmony (so disagreement with left=0)
    count_a0_disagree = 0
    for b in range(N):
        for c in range(N):
            inner = table[b][c]
            right = table[0][inner]
            if right == h:  # disagreement: left=0, right=harmony
                count_a0_disagree += 1
    
    # Count triples (a, b, 0) with left disagreement?
    count_c0_disagree = 0
    for a in range(N):
        for b in range(N):
            inner = table[a][b]
            left = table[inner][0]
            right = table[a][table[b][0]]  # = table[a][0] = 0 (VOID)
            if left == h:
                count_c0_disagree += 1
    
    return count_a0_disagree, count_c0_disagree

print()
print(f"{'N':>4} {'a=0 disagreement':>20} {'c=0 disagreement':>20} {'sum':>8} {'observed nonassoc':>18}")
for N in [10, 30, 210]:
    a0, c0 = count_void_harm_disagreement(N)
    r = detailed_classification(N)
    print(f"{N:>4} {a0:>20} {c0:>20} {a0+c0:>8} {r['nonassoc']:>18}")
