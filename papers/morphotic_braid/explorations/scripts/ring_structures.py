# PACKET: evening_handoff_2026_04_23/ring_structures.py
"""
Check for RING-LIKE structures pairing TIG tables.

A ring requires (R, +) abelian group and (R, *) multiplicative + distributivity.
TIG has multiple tables that could play + or *:
- ADD mod 10: the canonical abelian group
- MUL mod 10: standard ring multiplication (already a ring with ADD)
- TSML, BHML, Doing, CL_mult, CL_add, C_0: candidates for *

Test: does TSML distribute over ADD? Does BHML distribute over ADD? etc.
If yes, we have non-associative rings — a studied category.
"""
N = 10

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
BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
]
DOING = [[(TSML[i][j] - BHML[i][j]) % 10 for j in range(N)] for i in range(N)]
ADD = [[(i+j) % N for j in range(N)] for i in range(N)]
MUL = [[(i*j) % N for j in range(N)] for i in range(N)]

def distributes(mul, add, T_name="*", A_name="+"):
    """Test: a*(b+c) = a*b + a*c AND (b+c)*a = b*a + c*a."""
    failures = 0
    asym_failures = 0
    for a in range(N):
        for b in range(N):
            for c in range(N):
                # left distributive: a*(b+c) = a*b + a*c
                lhs_L = mul[a][add[b][c]]
                rhs_L = add[mul[a][b]][mul[a][c]]
                if lhs_L != rhs_L: failures += 1
                # right distributive
                lhs_R = mul[add[b][c]][a]
                rhs_R = add[mul[b][a]][mul[c][a]]
                if lhs_R != rhs_R: asym_failures += 1
    return failures, asym_failures

print("="*70)
print("DISTRIBUTIVITY TESTS — pairing candidates for ring-like structure")
print("="*70)
print("Format: * over + means a*(b+c) = a*b + a*c")
print()

candidates = [
    (MUL,   "MUL"),
    (TSML,  "TSML"),
    (BHML,  "BHML"),
    (DOING, "DOING"),
]

print(f"{'mul/add':20s} {'left_fails':>12s} {'right_fails':>12s} {'ring?':>8s}")
print("-"*60)

for M, mname in candidates:
    for A, aname in [(ADD, "ADD")]:
        lf, rf = distributes(M, A, mname, aname)
        ring = "YES" if lf == 0 and rf == 0 else "no"
        total_pairs = N**3
        print(f"{mname}/{aname:12s}   {lf}/{total_pairs} ({lf*100/total_pairs:.1f}%) {rf}/{total_pairs} ({rf*100/total_pairs:.1f}%)  {ring}")

# Now try BHML as +, TSML as *
print()
print("Alternative: using BHML as '+' instead of ADD:")
for M, mname in candidates:
    if mname == "BHML": continue
    lf, rf = distributes(M, BHML, mname, "BHML")
    total_pairs = N**3
    ring = "YES" if lf == 0 and rf == 0 else "no"
    print(f"  {mname}/BHML  left={lf}/{total_pairs} ({lf*100/total_pairs:.1f}%)  right={rf}/{total_pairs} ({rf*100/total_pairs:.1f}%)")

# Also check ADD over TSML, etc.
print()
print("Reverse: multiplicative table as '+':")
for A, aname in [(TSML, "TSML"), (BHML, "BHML"), (DOING, "DOING")]:
    lf, rf = distributes(MUL, A, "MUL", aname)
    total_pairs = N**3
    print(f"  MUL/{aname}  left={lf}/{total_pairs} ({lf*100/total_pairs:.1f}%)")

# Partial distributivity — where does TSML/ADD distributive law hold?
print()
print("="*70)
print("PARTIAL DISTRIBUTIVITY: which elements DO satisfy the distributive law?")
print("="*70)
print("For each a in {0,...,9}, count how many (b,c) satisfy a*(b+c) = a*b+a*c for TSML over ADD")
print()
for a in range(N):
    good = 0
    for b in range(N):
        for c in range(N):
            if TSML[a][ADD[b][c]] == ADD[TSML[a][b]][TSML[a][c]]:
                good += 1
    print(f"  a={a}: {good}/100 pairs (b,c) distribute")

