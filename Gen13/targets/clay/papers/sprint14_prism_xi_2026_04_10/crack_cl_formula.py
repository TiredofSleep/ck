"""
CRACK: Find the algebraic formula that reproduces the TSML table on Z/10Z
Sprint 15 — Blocker 1 | 2026-04-10

If we can find a closed-form formula f(a, b, N) that reproduces TSML[a][b]
for all 100 entries on Z/10Z, we can extend it to Z/30Z, Z/210Z, etc.

Copyright (c) 2026 Brayden Ross Sanders / 7Site LLC
"""

import math

TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],
]

N = 10
HARMONY = 7

# =====================================================================
# ANALYSIS: What are the non-HARMONY entries?
# =====================================================================
print("=" * 70)
print("TSML TABLE ANALYSIS — FINDING THE FORMULA")
print("=" * 70)

print("\nNon-HARMONY entries:")
non_harmony = []
for a in range(N):
    for b in range(N):
        if TSML[a][b] != HARMONY:
            non_harmony.append((a, b, TSML[a][b]))
            print(f"  TSML[{a}][{b}] = {TSML[a][b]}")

print(f"\nTotal non-HARMONY: {len(non_harmony)}/100")
print(f"HARMONY entries: {100 - len(non_harmony)}/100")

# =====================================================================
# PATTERN ANALYSIS of non-HARMONY entries
# =====================================================================
print("\n--- Pattern Analysis ---")

# Group by rule
print("\nV0 (row 0, all j != 7): TSML[0][j] = 0")
v0 = [(a,b,v) for a,b,v in non_harmony if a == 0]
print(f"  Count: {len(v0)}, all value 0: {all(v==0 for _,_,v in v0)}")

print("\nV1 (col 0, all i != 7): TSML[i][0] = 0")
v1 = [(a,b,v) for a,b,v in non_harmony if b == 0 and a != 0]
print(f"  Count: {len(v1)}, all value 0: {all(v==0 for _,_,v in v1)}")

print("\nECHO pairs (the remaining non-HARMONY entries):")
echo = [(a,b,v) for a,b,v in non_harmony if a != 0 and b != 0]
for a, b, v in echo:
    # Check various formulas
    add = (a + b) % N
    mul = (a * b) % N
    maxab = max(a, b)
    minab = min(a, b)
    print(f"  TSML[{a}][{b}] = {v}  | a+b={add} a*b={mul} max={maxab} min={minab}")

# =====================================================================
# TEST: Is the ECHO value always (a+b) % 10?
# =====================================================================
print("\n--- Testing: ECHO = (a+b) % 10? ---")
echo_is_sum = all(v == (a + b) % N for a, b, v in echo)
print(f"  All ECHO = (a+b)%10: {echo_is_sum}")

if not echo_is_sum:
    for a, b, v in echo:
        expected = (a + b) % N
        if v != expected:
            print(f"  FAIL: TSML[{a}][{b}] = {v}, but (a+b)%10 = {expected}")

# =====================================================================
# TEST: Is the ECHO value always max(a,b)?
# =====================================================================
print("\n--- Testing: ECHO = max(a,b)? ---")
echo_is_max = all(v == max(a, b) for a, b, v in echo)
print(f"  All ECHO = max(a,b): {echo_is_max}")

if not echo_is_max:
    for a, b, v in echo:
        expected = max(a, b)
        if v != expected:
            print(f"  FAIL: TSML[{a}][{b}] = {v}, but max = {expected}")

# =====================================================================
# DEEPER: What IS the ECHO rule?
# =====================================================================
print("\n--- ECHO entries detailed ---")
for a, b, v in echo:
    gcd_ab = math.gcd(a, b)
    lcm_ab = (a * b) // gcd_ab if gcd_ab > 0 else 0
    print(f"  ({a},{b})->{v}: a+b={a+b}, a*b={a*b}, gcd={gcd_ab}, "
          f"lcm={lcm_ab}, |a-b|={abs(a-b)}, (a+b)%10={(a+b)%10}, "
          f"(a*b)%10={(a*b)%10}")

# =====================================================================
# TEST: ECHO pairs are exactly the "resistance pairs"
# where specific operator identities persist
# =====================================================================
print("\n--- ECHO as operator identity persistence ---")
echo_pairs = {(a,b): v for a,b,v in echo}
# Known ECHO pairs from ck_tables.py:
known_echo = {
    (1, 2): 3,   # BEING x DOING = BECOMING (1+2=3)
    (2, 1): 3,   # symmetric
    (2, 4): 4,   # DOING x COLLAPSE = COLLAPSE
    (4, 2): 4,   # symmetric
    (2, 9): 9,   # DOING x RESET = RESET
    (9, 2): 9,   # symmetric
    (3, 9): 3,   # BECOMING x RESET = BECOMING
    (9, 3): 3,   # symmetric
    (4, 8): 8,   # COLLAPSE x BREATH = BREATH
    (8, 4): 8,   # symmetric
}

match = echo_pairs == known_echo
print(f"  Matches known ECHO set: {match}")

# =====================================================================
# THE FORMULA (complete)
# =====================================================================
print("\n" + "=" * 70)
print("COMPLETE FORMULA FOR TSML[a][b] ON Z/10Z")
print("=" * 70)

def tsml_formula(a, b, N=10):
    """
    The TSML composition rule on Z/NZ.

    Rule 1 (HARMONY override): if a == 7 or b == 7, return 7
    Rule 2 (VOID row): if a == 0, return 0
    Rule 3 (VOID col): if b == 0, return 0
    Rule 4 (ECHO): if (a,b) is a resistance pair, return the specific value
    Rule 5 (DEFAULT): return 7 (HARMONY)
    """
    HARMONY = N - 3  # 7 for N=10

    # Rule 1: HARMONY overwhelms everything
    if a == HARMONY or b == HARMONY:
        return HARMONY

    # Rule 2: VOID row
    if a == 0:
        return 0

    # Rule 3: VOID col
    if b == 0:
        return 0

    # Rule 4: ECHO pairs (operator identity persistence)
    # These are the pairs where the composition has a specific non-HARMONY value
    echo = {
        (1, 2): 3, (2, 1): 3,
        (2, 4): 4, (4, 2): 4,
        (2, 9): 9, (9, 2): 9,
        (3, 9): 3, (9, 3): 3,
        (4, 8): 8, (8, 4): 8,
    }
    if (a, b) in echo:
        return echo[(a, b)]

    # Rule 5: DEFAULT = HARMONY
    return HARMONY

# Verify against actual table
print("\nVerification against actual TSML table:")
errors = 0
for a in range(N):
    for b in range(N):
        computed = tsml_formula(a, b, N)
        actual = TSML[a][b]
        if computed != actual:
            errors += 1
            print(f"  ERROR: tsml_formula({a},{b}) = {computed}, actual = {actual}")

if errors == 0:
    print("  100/100 MATCH. Formula reproduces the table exactly.")
else:
    print(f"  {errors}/100 errors.")

# =====================================================================
# ANALYSIS: Can the ECHO rule be expressed algebraically?
# =====================================================================
print("\n--- Can ECHO be expressed without enumeration? ---")

# Pattern in ECHO pairs:
# (1,2)->3: a+b = 3 (additive)
# (2,4)->4: max(a,b) = 4 (max rule)
# (2,9)->9: max(a,b) = 9 (max rule)
# (3,9)->3: min(a,b) = 3 (min rule)
# (4,8)->8: max(a,b) = 8 (max rule)

# Check: is ECHO value always either a+b or max(a,b) or min(a,b)?
print("\nECHO value analysis:")
for a, b, v in echo:
    is_sum = (v == (a + b) % N)
    is_max = (v == max(a, b))
    is_min = (v == min(a, b))
    rule = "SUM" if is_sum else ("MAX" if is_max else ("MIN" if is_min else "OTHER"))
    print(f"  ({a},{b})->{v}: {rule}")

# Pattern:
# (1,2)->3: SUM (1+2=3)
# (2,1)->3: SUM
# (2,4)->4: MAX
# (4,2)->4: MAX
# (2,9)->9: MAX
# (9,2)->9: MAX
# (3,9)->3: MIN
# (9,3)->3: MIN
# (4,8)->8: MAX
# (8,4)->8: MAX

print("\n--- ECHO RULE PATTERN ---")
print("  Pairs involving DOING (2): SUM if partner is 1, MAX otherwise")
print("  Pair (3,9): MIN (BECOMING persists over RESET)")
print("  Pair (4,8): MAX (BREATH dominates COLLAPSE)")
print("\n  The ECHO rules are SEMANTIC, not purely algebraic.")
print("  They encode operator identity: which operator 'wins' in composition.")
print("  This means the CL cannot be expressed as a single closed-form formula.")
print("  It is a HYBRID: algebraic default (HARMONY) + semantic exceptions (ECHO).")
print("\n  IMPLICATION: Generalizing to Z/30Z requires defining what the 'operators'")
print("  and their 'identities' are on the larger ring. The ECHO set is specific to")
print("  the 10-operator TIG system. On Z/30Z there would be 30 operators with")
print("  different identity-persistence rules.")
