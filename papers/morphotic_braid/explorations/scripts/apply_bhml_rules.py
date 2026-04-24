# PACKET: evening_handoff_2026_04_23/apply_bhml_rules.py
"""
Apply the BHML construction rules (Rules A-D) to celebrated tables.

Parameters per table:
  N = table size
  z = VOID element (the zero of the structure)
  h = HARMONY element (the saturation target; here, maximal element of "structure band")

This constructs a "BHML-type" version of each structure using the 4-rule scaffold.

HONEST LABEL: This applies the RULES we derived for TIG's N=10 case. Whether
these rules produce a "meaningful BHML" for other structures is an open question.
What we get is a well-defined derived table; whether it has interesting properties
is a separate empirical question.
"""
from itertools import permutations

def build_bhml_scaffold(N, z=0, h=None):
    """Construct a BHML-scaffold using Rules A-D for given (N, z, h).
    
    If h is None, use h = N-3 (mirroring TIG's choice of h=7 at N=10).
    """
    if h is None:
        h = N - 3  # mirrors TIG: N=10, h=7, so h is 2nd-from-last "main band"
    if h < 2 or h >= N:
        return None
    
    B = [[None]*N for _ in range(N)]
    
    # Rule A: VOID identity + VOID/HARMONY
    for i in range(N):
        B[z][i] = i
        B[i][z] = i
    B[z][h] = h
    B[h][z] = h
    
    # Rule B: axis saturation for 1 ≤ i,j ≤ h-1
    for i in range(1, h):
        for j in range(1, h):
            B[i][j] = min(max(i, j) + 1, h)
    
    # Rule B extended: row h-1 extends via CHAOS saturation to columns > h
    for j in range(h, N):
        B[h-1][j] = h  # CHAOS saturation
        B[j][h-1] = h
    # Actually in our case h=7, h-1=6 (CHAOS), and rule was row 6 cols 7,8,9 = 7
    
    # Rule D: HARMONY as increment
    for j in range(1, N):
        if j != h:  # except h itself, handled below
            B[h][j] = (j + 1) % N
            B[j][h] = (j + 1) % N
    B[h][h] = (h + 1) % N  # 7·7 = 8 in TIG
    
    # Rule C: post-HARMONY functional operators (rows h+1 ... N-1)
    # BHML[8][4,5,6] = 7 and BHML[9][4,5,6] = 7 (transition-zone mapping)
    # BHML[8][8] = 7 (BREATH self-resonance)
    # Generalize: for i > h and j in {h-3, h-2, h-1} = transition zone
    for i in range(h+1, N):
        # Map transition zone to h
        for j in range(max(1, h-3), h):
            B[i][j] = h
            B[j][i] = h
        # Self-resonance: BHML[i][i] for i > h, specifically BREATH (h+1)
        if i == h+1:
            B[i][i] = h  # BREATH self-resonance
    
    # Fill remaining cells with "unknown" marker to flag
    # These are the cells Rule A-D don't cover (the "bespoke" cells)
    for i in range(N):
        for j in range(N):
            if B[i][j] is None:
                B[i][j] = '?'
    return B

def pretty_print(B, name):
    N = len(B)
    print(f"  {name} (n={N}):")
    for row in B:
        print("    " + " ".join(f"{str(v):>3s}" for v in row))

# ==================================================================
# Apply to celebrated tables with matched parameters
# ==================================================================

print("="*70)
print("APPLYING BHML CONSTRUCTION RULES TO CELEBRATED STRUCTURES")
print("="*70)

# TIG baseline: N=10, h=7
print("\n--- Baseline: TIG (N=10, h=7) — should reproduce most of BHML ---")
B_tig = build_bhml_scaffold(N=10, z=0, h=7)
pretty_print(B_tig, "BHML-TIG scaffold")

# Compare to actual BHML
BHML_actual = [
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

# Score match at cells where scaffold is defined (not '?')
match = 0
total = 0
misses = []
for i in range(10):
    for j in range(10):
        if B_tig[i][j] != '?':
            total += 1
            if B_tig[i][j] == BHML_actual[i][j]:
                match += 1
            else:
                misses.append((i, j, B_tig[i][j], BHML_actual[i][j]))
print(f"\n  Scaffold match to actual BHML: {match}/{total} defined cells")
if misses:
    print(f"  Misses: {misses[:5]}")

# Small structures now
print("\n--- N=3 (minimal non-trivial): z=0, h=1 ---")
B3 = build_bhml_scaffold(N=3, z=0, h=1)
if B3:
    pretty_print(B3, "N=3 scaffold")
else:
    print("  (h=1 too small for Rule B to operate; degenerate)")

# Apply to size 5 (could be Z/5Z or STS-like)
print("\n--- N=5: z=0, h=3 ---")
B5 = build_bhml_scaffold(N=5, z=0, h=3)
pretty_print(B5, "N=5, h=3 scaffold")

# Apply to size 7 (Fano/STS(7))
print("\n--- N=7 (Fano context): z=0, h=5 ---")
B7 = build_bhml_scaffold(N=7, z=0, h=5)
pretty_print(B7, "N=7, h=5 scaffold")

# Apply to size 8 (octonion-size)  
print("\n--- N=8 (octonion context): z=0, h=6 ---")
B8 = build_bhml_scaffold(N=8, z=0, h=6)
pretty_print(B8, "N=8, h=6 scaffold")

# Apply to size 12 (to see parameter behavior)
print("\n--- N=12 (for dodecahedral context): z=0, h=9 ---")
B12 = build_bhml_scaffold(N=12, z=0, h=9)
pretty_print(B12, "N=12, h=9 scaffold")

# Now check: the scaffold is DEFINED uniformly. What properties does it have?
def analyze_scaffold(B, name, z=0, h=None):
    """If B has no '?' cells, check its algebraic properties."""
    N = len(B)
    if any('?' in row for row in B):
        # Replace '?' with h for analysis purposes (saturation default)
        B = [[(h if v == '?' else v) for v in row] for row in B]
    # Check properties
    comm = all(B[i][j] == B[j][i] for i in range(N) for j in range(N))
    assoc = all(B[B[i][j]][k] == B[i][B[j][k]] for i in range(N) for j in range(N) for k in range(N))
    # Check identity
    ident = None
    for e in range(N):
        if all(B[e][i]==i and B[i][e]==i for i in range(N)):
            ident = e; break
    return {'n':N, 'comm':comm, 'assoc':assoc, 'ident':ident, 'name':name}

print()
print("="*70)
print("Algebraic properties of BHML-scaffold (with '?' filled by h for analysis)")
print("="*70)
for (B, n, h) in [(B3, 3, 1), (B5, 5, 3), (B7, 7, 5), (B8, 8, 6), (B12, 12, 9), (B_tig, 10, 7)]:
    if B is not None:
        props = analyze_scaffold(B, f"N={n},h={h}", h=h)
        print(f"  N={n}, h={h}: comm={props['comm']}, assoc={props['assoc']}, identity={props['ident']}")

