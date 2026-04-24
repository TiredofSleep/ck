<!-- PACKET: evening_handoff_2026_04_23/analyze_tsml_bumps.py -->
"""
TSML CRT-fiber analysis: do TSML's 8 bump cells sit at specific positions
in the CRT decomposition Z/10 ~ Z/2 x Z/5?

Earlier CRT audit (TSML_CRT_DECOMPOSITION_EXPLORATION.md) showed TSML does NOT
factor as a direct product. But the 8 bump cells (S_MAX + S_ADD) might still
sit at specific fiber positions even if the full table doesn't factor.

Let me check.
"""

# CRT coordinates for Z/10: x -> (x mod 2, x mod 5) = (eps, y)
def crt(x):
    return (x % 2, x % 5)

# TSML bump cells (from FORMULAS §7)
S_MAX = [(2,4), (4,2), (2,9), (9,2), (4,8), (8,4)]  # output: max(a,b)
S_ADD = [(1,2), (2,1)]                               # output: (a+b) mod 10

# TIG operator labels
labels = {0:'VOID', 1:'LATTICE', 2:'COUNTER', 3:'PROGRESS', 4:'COLLAPSE',
          5:'BALANCE', 6:'CHAOS', 7:'HARMONY', 8:'BREATH', 9:'RESET'}

# Creation cycle and Dissolution cycle
CREATION = {1, 3, 7, 9}
DISSOLUTION = {2, 4, 6, 8}
NEUTRAL = {0, 5}  # VOID, BALANCE (y=0 fiber)

def cycle_of(x):
    if x in CREATION: return "C"
    if x in DISSOLUTION: return "D"
    if x in NEUTRAL: return "N"
    return "?"

print("="*80)
print("TSML BUMP CELLS IN CRT COORDINATES")
print("="*80)
print()
print("S_MAX cells (output = max(a,b)):")
print(f"{'cell':12s} {'CRT(a)':10s} {'CRT(b)':10s} {'labels':35s} {'cycle_a,b':10s} {'output':12s}")
print("-"*90)
for (a, b) in S_MAX:
    ca, cb = crt(a), crt(b)
    out = max(a, b)
    print(f"({a:2d},{b:2d})      {str(ca):10s} {str(cb):10s} {labels[a]+'·'+labels[b]:35s} {cycle_of(a)+','+cycle_of(b):10s} {out}={labels[out]}")

print()
print("S_ADD cells (output = (a+b) mod 10):")
print(f"{'cell':12s} {'CRT(a)':10s} {'CRT(b)':10s} {'labels':35s} {'cycle_a,b':10s} {'output':12s}")
print("-"*90)
for (a, b) in S_ADD:
    ca, cb = crt(a), crt(b)
    out = (a + b) % 10
    print(f"({a:2d},{b:2d})      {str(ca):10s} {str(cb):10s} {labels[a]+'·'+labels[b]:35s} {cycle_of(a)+','+cycle_of(b):10s} {out}={labels[out]}")

# ===============================================
# Pattern analysis
# ===============================================
print()
print("="*80)
print("PATTERN ANALYSIS")
print("="*80)

# 1. Epsilon-pair distribution
print()
print("1. EPSILON (mod 2) pair distribution:")
eps_pairs = {}
for (a,b) in S_MAX + S_ADD:
    key = (a%2, b%2)
    eps_pairs.setdefault(key, []).append((a,b))
for key in sorted(eps_pairs.keys()):
    cells = eps_pairs[key]
    print(f"  eps={key}: {len(cells)} cells  {cells}")

# 2. Y-pair distribution
print()
print("2. Y (mod 5) pair distribution:")
y_pairs = {}
for (a,b) in S_MAX + S_ADD:
    key = (a%5, b%5)
    y_pairs.setdefault(key, []).append((a,b))
for key in sorted(y_pairs.keys()):
    cells = y_pairs[key]
    print(f"  y={key}: {len(cells)} cells  {cells}")

# 3. Cycle-pair distribution
print()
print("3. Cycle-pair distribution (C=Creation, D=Dissolution, N=Neutral):")
cycle_pairs = {}
for (a,b) in S_MAX + S_ADD:
    key = tuple(sorted([cycle_of(a), cycle_of(b)]))
    cycle_pairs.setdefault(key, []).append((a,b))
for key in sorted(cycle_pairs.keys()):
    cells = cycle_pairs[key]
    print(f"  {key}: {len(cells)} cells  {cells}")

# 4. Check: do bumps avoid element 7?
print()
print("4. Do S_MAX / S_ADD cells involve element 7?")
involves_7 = [(a,b) for (a,b) in S_MAX + S_ADD if a == 7 or b == 7]
print(f"  Cells involving element 7: {len(involves_7)}")
if not involves_7:
    print("  CONFIRMED: No TSML bump cell touches HARMONY (element 7).")

# 5. Check: do bumps avoid VOID axis?
print()
print("5. Do S_MAX / S_ADD cells involve element 0?")
involves_0 = [(a,b) for (a,b) in S_MAX + S_ADD if a == 0 or b == 0]
print(f"  Cells involving element 0: {len(involves_0)}")

# 6. Check: position in Creation/Dissolution lattice
print()
print("6. All bump cells relative to cycles:")
print("  S_MAX cells:")
for (a,b) in S_MAX:
    print(f"    ({a},{b}): {cycle_of(a)}-{cycle_of(b)} interaction, both in cycle subset? {a in CREATION or a in DISSOLUTION and b in CREATION or b in DISSOLUTION}")
print("  S_ADD cells:")
for (a,b) in S_ADD:
    print(f"    ({a},{b}): {cycle_of(a)}-{cycle_of(b)} interaction")

# 7. Multiplicative structure mod 5
print()
print("7. Multiplicative structure: is a·b mod 5 preserved?")
print("  For each bump cell, compute (a·b) mod 5 and compare to (output) mod 5:")
for (a,b) in S_MAX:
    out = max(a,b)
    prod5 = (a*b) % 5
    out5 = out % 5
    print(f"  ({a},{b}) -> {out}: a·b mod 5 = {prod5}, output mod 5 = {out5}, {'match' if prod5 == out5 else 'differ'}")
for (a,b) in S_ADD:
    out = (a+b) % 10
    sum5 = (a+b) % 5
    out5 = out % 5
    print(f"  ({a},{b}) -> {out}: a+b mod 5 = {sum5}, output mod 5 = {out5}, {'match' if sum5 == out5 else 'differ'}")

# 8. Sigma-class analysis
print()
print("8. Sigma-class analysis (sigma(u) = nu_2(3u+1) for units):")
def nu2(n):
    if n == 0: return float('inf')
    k = 0
    while n % 2 == 0: n //= 2; k += 1
    return k
for u in range(1, 10):
    s = nu2(3*u+1) if u not in [0, 2, 4, 5, 6, 8] else "—"  # units only
    print(f"  sigma({u}) = {s}")

print()
print("  S_MAX and S_ADD cells by sigma-classes of inputs:")
for (a,b) in S_MAX + S_ADD:
    from math import gcd
    sa = nu2(3*a+1) if gcd(a,10)==1 else "—"
    sb = nu2(3*b+1) if gcd(b,10)==1 else "—"
    print(f"  ({a},{b}): sigma classes ({sa}, {sb})")

