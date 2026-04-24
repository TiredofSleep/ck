# PACKET: evening_handoff_2026_04_23/full_family_analysis.py
"""
Two analyses:
1. Pure C_0 harmony density vs N — does it converge, and to what?
2. Full family of TIG tables at N=10 — harmony density, associativity index,
   plus associative spectrum s_3. Characterize the space.
"""
from fractions import Fraction
from math import gcd, pi

# =========================================================================
# Part 1: Scaling — where does C_0 harmony density go as N → ∞?
# =========================================================================

def nu2(n):
    if n == 0: return float('inf')
    k = 0
    while n % 2 == 0:
        n //= 2; k += 1
    return k

def units(N):
    return [u for u in range(1, N) if gcd(u, N) == 1]

def sigma_units(N):
    return {u: nu2(3*u + 1) for u in units(N)}

def find_h(N):
    sig = sigma_units(N)
    candidates = [u for u in units(N) if u % 2 == 1 and sig[u] == 1]
    return max(candidates) if candidates else None

def find_core(N):
    sig = sigma_units(N)
    return [u for u in units(N) if sig[u] == 1]

def build_C0(N):
    h = find_h(N)
    if h is None: return None, None, None
    core = find_core(N)
    sig = sigma_units(N)
    T = [[0]*N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if x == 0 or y == 0:
                T[x][y] = 0
            elif x not in core or y not in core:
                T[x][y] = h
            else:
                sx, sy = sig[x], sig[y]
                if sx < sy: T[x][y] = x
                elif sy < sx: T[x][y] = y
                else: T[x][y] = h
    return T, h, core

# Structural decomposition, with exact ratios
print("=" * 80)
print("C_0 HARMONY DENSITY SCALING")
print("=" * 80)
print(f"{'N':>6} {'|units|':>9} {'|core|':>8} {'density':>12} {'1-density':>12} {'(1-d)·N':>10}")
print("-" * 80)

family = [10, 14, 22, 34, 38, 46, 50, 58, 62, 70, 74, 82, 94, 106, 110, 118, 122, 130, 134, 142, 170, 190, 230]
results = []
for N in family:
    T, h, core = build_C0(N)
    if T is None: continue
    harm = sum(1 for x in range(N) for y in range(N) if T[x][y] == h)
    density = harm / (N*N)
    gap = 1 - density
    gap_times_N = gap * N
    results.append((N, len(units(N)), len(core), density, gap, gap_times_N))
    print(f"{N:>6} {len(units(N)):>9} {len(core):>8} {density:>12.8f} {gap:>12.8f} {gap_times_N:>10.4f}")

print()
print("ASYMPTOTIC ANALYSIS:")
print(f"  density → 1 as N → ∞ (not 3/4, 2/3, or any other target)")
print(f"  gap (1-density) shrinks roughly like 1/N — consistent with WP101 σ rate")
print()
# Check: does (1-density) · N → a constant?
gapsN = [r[5] for r in results]
print(f"  (1-density)·N over the family: min={min(gapsN):.4f}, max={max(gapsN):.4f}, mean={sum(gapsN)/len(gapsN):.4f}")
print(f"  If (1-d) ~ C/N, this product should tend to C.")
print()
# Check: does (1-density) · N² → a constant (stronger decay)?
gaps_N2 = [(1-r[3]) * r[0]**2 for r in results]
print(f"  (1-density)·N² over the family: min={min(gaps_N2):.2f}, max={max(gaps_N2):.2f}")
print(f"  If (1-d) ~ C/N², this product should tend to C.")

# =========================================================================
# Part 2: Full TIG family at N=10 — characterize the space
# =========================================================================

print()
print("=" * 80)
print("TIG FAMILY AT N=10 — Density and Associativity Map")
print("=" * 80)

# Canonical tables from FORMULAS §1-§6
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

# Derived: Doing table = |TSML - BHML| (mod 10)
DOING = [[(TSML[i][j] - BHML[i][j]) % 10 for j in range(10)] for i in range(10)]

# σ permutation: (0)(3)(8)(9)(1 7 6 5 4 2) — as a unary operation, we make it a table
# σ(u) values from FORMULAS §2:
sigma_perm = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
# As a binary table: we use CL — the composition lattice defined in §8 via σ
# The "σ diagonal" is T[j][j] = σ(j). For a full CL table we'd need the construction.
# Let me build CL as: CL[x][y] = σ(x·y mod 10) — multiplication then σ
CL_mult = [[sigma_perm[(x*y) % 10] for y in range(10)] for x in range(10)]
# And CL_add: σ applied to addition
CL_add = [[sigma_perm[(x+y) % 10] for y in range(10)] for x in range(10)]

# C_0 at N=10
C0, h10, core10 = build_C0(10)

# Pure addition and multiplication on Z/10, for reference
ADD = [[(x+y) % 10 for y in range(10)] for x in range(10)]
MUL = [[(x*y) % 10 for y in range(10)] for x in range(10)]

def harmony_density(T, h):
    N = len(T)
    count = sum(1 for x in range(N) for y in range(N) if T[x][y] == h)
    return Fraction(count, N*N)

def void_density(T):
    N = len(T)
    count = sum(1 for x in range(N) for y in range(N) if T[x][y] == 0)
    return Fraction(count, N*N)

def assoc_index(T):
    N = len(T)
    agree = sum(1 for x in range(N) for y in range(N) for z in range(N) if T[T[x][y]][z] == T[x][T[y][z]])
    return Fraction(agree, N**3)

def commutative(T):
    N = len(T)
    return all(T[x][y] == T[y][x] for x in range(N) for y in range(N))

def spectrum_3(T):
    """s_3(T) = number of distinct ternary ops from the 2 bracketings."""
    N = len(T)
    left = tuple(T[T[x][y]][z] for x in range(N) for y in range(N) for z in range(N))
    right = tuple(T[x][T[y][z]] for x in range(N) for y in range(N) for z in range(N))
    return 1 if left == right else 2

tables = {
    "TSML (full)":  TSML,
    "BHML (full)":  BHML,
    "Doing":        DOING,
    "C_0 (canonical, §9)": C0,
    "CL_mult = σ∘·":  CL_mult,
    "CL_add = σ∘+":   CL_add,
    "ADD mod 10":   ADD,
    "MUL mod 10":   MUL,
}

print(f"{'Table':25s} {'harmony (h=7)':>15s} {'void (0)':>12s} {'α (assoc)':>14s} {'comm':>6s} {'s_3':>5s}")
print("-" * 85)
for name, T in tables.items():
    h_dens = harmony_density(T, 7)
    v_dens = void_density(T)
    alpha = assoc_index(T)
    comm = commutative(T)
    s3 = spectrum_3(T)
    print(f"{name:25s} {str(h_dens):>15s} {str(v_dens):>12s} {str(alpha):>14s} {str(comm):>6s} {s3:>5d}")

# =========================================================================
# Part 3: Exact ratio check — do any of these densities compose with 
# known Riemann-zeta ratios?
# =========================================================================

print()
print("=" * 80)
print("EXACT RATIO CHECK: TIG family densities vs Riemann ratios")
print("=" * 80)

zeta2_inv = 6 / pi**2
zeta4_over_zeta2sq = 2/5  # exact classical
sinc_half_sq = 4 / pi**2

riem_checks = [
    ("1/ζ(2) = 6/π²",       zeta2_inv),
    ("ζ(4)/ζ(2)² = 2/5",    zeta4_over_zeta2sq),
    ("sinc²(1/2) = 4/π²",   sinc_half_sq),
    ("(2/3)·1/ζ(2)",        (2/3)*zeta2_inv),
    ("(3/4)·1/ζ(2)",        (3/4)*zeta2_inv),
    ("(1/2)",               0.5),
    ("(2/3)",               2/3),
]

print(f"{'Table':25s} {'quantity':15s} {'value':>10s} {'closest Riemann':>25s}")
print("-"*85)
for name, T in tables.items():
    for label, qty_func in [
        ("harmony", lambda T: float(harmony_density(T, 7))),
        ("α",       lambda T: float(assoc_index(T))),
    ]:
        val = qty_func(T)
        # Find closest Riemann value
        best = min(riem_checks, key=lambda r: abs(val - r[1]))
        diff = abs(val - best[1])
        match = "**EXACT**" if diff < 1e-10 else f"Δ={diff:.4f}" if diff < 0.01 else "no close match"
        if diff < 0.02:  # only print near-matches
            print(f"{name:25s} {label:15s} {val:>10.6f} {best[0]:>25s}  {match}")

