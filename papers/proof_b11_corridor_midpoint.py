"""
B11: CORRIDOR MIDPOINT THEOREM
Luther-Sanders Research Framework | April 1 2026

THEOREM B11 (Corridor Midpoint — Three Convergences):
  In the sinc² arithmetic corridor (t = k/p, p prime, k ∈ {1..p-1}),
  the point t = 1/2 is uniquely characterized by THREE independent properties:

  (1) GEOMETRIC: t=1/2 is the additive midpoint of the valid corridor (0,1).

  (2) ANALYTIC: t=1/2 is the UNIQUE point in (0,1) where sin(πt) = 1.
      This gives sinc²(1/2) = (sin(π/2) / (π/2))² = (2/π)² = 4/π².
      The sine achieves full amplitude exactly once in the corridor,
      at the midpoint.

  (3) ALGEBRAIC: Under the ring normalization t = v/n (v ∈ Z/10Z, n=10),
      BALANCE = 5 maps to t = 5/10 = 1/2.
      The algebraic center of Z/10Z (D21: centroid of (Z/10Z)* and ODD)
      maps to the geometric center of the corridor.

  The three characterizations identify the same object independently:
    midpoint of (0,1) = sine-maximum point = image of ring center.

  This overdetermination (three independent routes to 1/2) mirrors the
  overdetermination of BALANCE=5 (D21: ring centroid, ODD centroid,
  σ-fixed-point, additive midpoint).

  VALUE: sinc²(1/2) = 4/π² ≈ 0.4053 is the unique corridor amplitude
  at the sine-maximum point. This is the CANONICAL SIDELOBE ANCHOR:
  the value the corridor takes at the single point where the sine's
  oscillating numerator is fully saturated.

WHAT B11 DOES NOT CLAIM:
  (1) That 4/π² is an extremum of sinc² — sinc² is monotone decreasing
      on (0,1), with no interior critical point.
  (2) That t=1/2 is the unique rational with a "nice" corridor value —
      t=1/4 gives 8/π², t=1/6 gives 9/π² (also integer multiples of 1/π²).
  (3) Any connection to σ=1/2 in the Riemann zeta function. That remains
      a speculative external analogy, not proved here.

TIER: B — analytical facts fully proved; the "canonical sidelobe anchor"
     interpretation is the conjecture pending C/D promotion.
     Upgrade path: show that sinc²(1/2) = 4/π² appears as a universal
     constant in the corridor atlas (predicted amplitude at the midpoint
     for all large primes p, confirmed empirically in D2/D3 work).
"""

import sys, io, os, math
from fractions import Fraction
sys.path.insert(0, os.path.dirname(__file__))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sep = "=" * 72
def section(t): print(f"\n{sep}\n  {t}\n{sep}\n")

def sinc2(t):
    if abs(t) < 1e-15: return 1.0
    return (math.sin(math.pi * t) / (math.pi * t)) ** 2

print("B11: CORRIDOR MIDPOINT THEOREM")
print("Luther-Sanders Research Framework | April 1 2026")
print()
print("  Three independent routes to t=1/2 as the canonical midpoint object.")

# ============================================================
# SECTION 1: THE SINC² CORRIDOR
# ============================================================
section("SECTION 1: THE CORRIDOR — sinc²(k/p) FOR PRIME p")

print("  DEFINITION: For prime p and k ∈ {1..p-1}, the corridor value is")
print("    R(k,p) = sinc²(k/p) = (sin(πk/p) / (πk/p))²")
print("  The corridor variable is t = k/p ∈ (0,1).")
print("  As p→∞, the grid {k/p} becomes dense on (0,1).")
print()
print("  KEY PROPERTIES (proved in D2):")
print("  - R(k,p) starts near 1 for small k/p (D2: near-1 head)")
print("  - R(k,p) = 0 at k=p (t=1) — forced null")
print("  - sinc² is strictly monotone decreasing on (0,1)")
print()

# Verify monotone decreasing
print("  Verification: sinc²(t) is strictly decreasing on (0,1):")
prev = 1.0
strictly_dec = True
for i in range(1, 100):
    t = i / 100.0
    v = sinc2(t)
    if v >= prev:
        strictly_dec = False
        print(f"    FAILED at t={t}: sinc2={v} >= prev={prev}")
    prev = v
print(f"  Monotone decreasing on grid {{0.01,0.02,...,0.99}}: {strictly_dec}  ✓")
print()
print("  COROLLARY: sinc² has NO interior critical point on (0,1).")
print("  t=1/2 is NOT an extremum of sinc². Its special role is different.")

# ============================================================
# SECTION 2: PROPERTY 1 — GEOMETRIC MIDPOINT
# ============================================================
section("SECTION 2: PROPERTY 1 — GEOMETRIC MIDPOINT OF THE CORRIDOR")

print("  The valid corridor is t ∈ (0,1).")
print("  The geometric midpoint is t* = (0+1)/2 = 1/2.")
print("  This is the unique t satisfying: t = 1-t (symmetric about t*).")
print()

# Verify: sinc2 is NOT symmetric about 1/2
print("  Verify sinc² is NOT symmetric about t=1/2:")
print("  (sinc² is not a symmetric function — it is monotone decreasing)")
for t in [0.1, 0.2, 0.3, 0.4]:
    v_t = sinc2(t)
    v_comp = sinc2(1 - t)
    print(f"    sinc²({t:.1f})={v_t:.6f}  ≠  sinc²({1-t:.1f})={v_comp:.6f}")
print()
print("  The midpoint t=1/2 is the GEOMETRIC center of the domain, not a")
print("  symmetry center of the function values.")

# ============================================================
# SECTION 3: PROPERTY 2 — UNIQUE SINE MAXIMUM
# ============================================================
section("SECTION 3: PROPERTY 2 — UNIQUE POINT WHERE sin(πt) = 1 IN (0,1)")

print("  THEOREM: t=1/2 is the UNIQUE t ∈ (0,1) where sin(πt) = 1.")
print()
print("  PROOF:")
print("    sin(πt) = 1  ⟺  πt = π/2 + 2πk  for some integer k")
print("                  ⟺  t = 1/2 + 2k")
print("    For t ∈ (0,1): only k=0 satisfies 0 < 1/2+2(0) < 1.")
print("    Therefore t = 1/2 is the unique solution. □")
print()
print("  CONSEQUENCE: sinc(1/2) = sin(π/2) / (π/2) = 1 / (π/2) = 2/π")
print("               sinc²(1/2) = (2/π)² = 4/π²")
print()

v_half = sinc2(0.5)
four_pi2 = 4 / math.pi**2
print(f"  Computed: sinc²(1/2) = {v_half:.15f}")
print(f"  4/π²              = {four_pi2:.15f}")
print(f"  Match:              {abs(v_half - four_pi2) < 1e-14}  ✓")
print()
print("  WHY THIS IS THE CANONICAL ANCHOR:")
print("  sinc(t) = sin(πt) / (πt) is the ratio of the sine to its first-order")
print("  linear approximation (πt). At t=1/2, the sine achieves its global")
print("  maximum (=1) within the corridor. Everywhere else in (0,1),")
print("  sin(πt) < 1. The sinc value at t=1/2 is therefore 2/π — the ratio of")
print("  the full sine amplitude to the half-period scale factor π/2.")
print("  This is the unique point where 'the corridor saturates the sine'.")
print()

# Check other rational points for sin(pi*t) = 1
print("  All rational t=m/n with n≤12, checking sin(πt):")
max_sine = 0.0
max_t = None
for n in range(2, 13):
    for m in range(1, n):
        if math.gcd(m, n) == 1:
            t = m / n
            sv = math.sin(math.pi * t)
            if sv > max_sine:
                max_sine = sv
                max_t = (m, n)
            if abs(sv - 1.0) < 1e-10:
                print(f"  sin(π·{m}/{n}) = 1  ← MAXIMUM (t=1/2)")
print(f"  Maximum sin(πt) over rationals t=m/n, n≤12: sin(π·{max_t[0]}/{max_t[1]}) = {max_sine:.10f}")
print(f"  Only t=1/2 gives sin(πt) = 1 exactly.  ✓")

# ============================================================
# SECTION 4: PROPERTY 3 — RING CENTER MAP
# ============================================================
section("SECTION 4: PROPERTY 3 — BALANCE=5 MAPS TO CORRIDOR MIDPOINT")

print("  The ring Z/10Z has a canonical normalization: t = v/n = v/10.")
print("  This maps each operator v ∈ Z/10Z to a corridor position t ∈ [0,1).")
print()

CL = {0:'VOID', 1:'LATTICE', 2:'COUNTER', 3:'PROGRESS', 4:'COLLAPSE',
      5:'BALANCE', 6:'CHAOS', 7:'HARMONY', 8:'BREATH', 9:'RESET'}

print(f"  {'v':>3}  {'CL[v]':>12}  {'t=v/10':>8}  {'sinc²(t)':>12}  {'note'}")
print(f"  {'-'*3}  {'-'*12}  {'-'*8}  {'-'*12}  {'-'*30}")
for v in range(10):
    t = v / 10
    s2 = sinc2(t) if t > 0 else 1.0
    note = ''
    if v == 5: note = '← BALANCE = corridor midpoint t=1/2'
    if v == 0: note = '← VOID = corridor start (sinc²=1)'
    print(f"  {v:>3}  {CL[v]:>12}  {t:>8.3f}  {s2:>12.6f}  {note}")

print()
print("  BALANCE = 5 maps to t = 5/10 = 1/2 = corridor midpoint.  ✓")
print()

# Cross-reference with spine results
print("  Cross-reference with spine:")
print("  D21: BALANCE=5 is the centroid of (Z/10Z)* AND of ODD={1,3,5,7,9}")
print("  D21: 5 is the unique ODD fixed point of σ: v↦10-v (complement map)")
print("  D21: 5 is the additive midpoint of Z/10Z (10//2 = 5)")
print()
print("  B11: t=1/2 is the geometric midpoint of (0,1) (corridor domain)")
print("  B11: t=1/2 is the unique sine-maximum point in (0,1)")
print()
print("  BRIDGE: v=5 and t=1/2 are the SAME midpoint object,")
print("  viewed at two scales: ring scale (Z/10Z, integer v=5) vs")
print("                        corridor scale (real t=k/p, t→1/2 as p→∞).")
print()
print("  The normalization t=v/10 is the explicit bridge.")
print("  It maps the ring's algebraic center to the corridor's geometric center.")

# ============================================================
# SECTION 5: THE THREE ROUTES — INDEPENDENCE VERIFICATION
# ============================================================
section("SECTION 5: INDEPENDENCE OF THE THREE CHARACTERIZATIONS")

print("  Are the three routes genuinely independent?")
print()
print("  Route 1 (Geometric): t=1/2 as midpoint of (0,1)")
print("  Uses only: real interval arithmetic. No ring, no sine, no spine.")
print("  Dependency: NONE. Purely geometric.")
print()
print("  Route 2 (Analytic): t=1/2 as unique sine-maximum in (0,1)")
print("  Uses only: sinc² = sin²(πt)/(πt)² and standard analysis.")
print("  Dependency: the sinc² lens (D2). Does NOT require ring.")
print()
print("  Route 3 (Algebraic): t = BALANCE/10 = 5/10 = 1/2")
print("  Uses only: Z/10Z ring structure and normalization t=v/n.")
print("  Dependency: D21 (ring center), D19 (Z/10Z as substrate).")
print("  Does NOT require sinc² or real analysis.")
print()
print("  The three routes use disjoint mathematical objects.")
print("  None depends on the other. They converge to the same t=1/2.")
print()
print("  This mirrors D21's finding for BALANCE=5:")
print("  Ring centroid, ODD centroid, σ-fixed-point, additive midpoint —")
print("  four independent characterizations of the same algebraic object.")
print("  B11 adds a fifth: it is the corridor midpoint in the sinc² lens.")

# ============================================================
# SECTION 6: THE CANONICAL SIDELOBE VALUE
# ============================================================
section("SECTION 6: sinc²(1/2) = 4/π² — THE CANONICAL SIDELOBE ANCHOR")

print("  WHY 4/π² is 'canonical':")
print()
print("  sinc²(1/2) = (2/π)² = 4/π²")
print()
print("  The 2/π constant appears in:")
print("  - Wallis product: 2/π = ∏(1 - 1/4k²)  (Wallis 1655)")
print("  - Euler's Basel: 2/π ≈ sin-amplitude at half-period")
print("  - sinc sampling: sinc(1/2) = 2/π is the first non-trivial sinc value")
print()
print(f"  Numerically: 4/π² = {4/math.pi**2:.15f}")
print(f"  Compare:   Si(2π)/π = {0.45141166:.10f}  (D14 spectral mean)")
print(f"   Ratio sinc²(1/2) / mean = {sinc2(0.5)/0.45141166:.10f}")
print()
print("  sinc²(1/2) is BELOW the corridor mean — the corridor is front-weighted.")
print("  The midpoint value 4/π² is the unique closed-form anchor at the geometric center.")
print()

# Compute corridor values at ring-special points
print("  Corridor values at spine-significant t positions:")
spine_pts = [
    (3/50,  "W = 3/50 (D17)"),
    (5/7,   "T* = 5/7 (D18d/D19)"),
    (1/2,   "BALANCE/10 = 5/10 (B11)"),
    (7/10,  "HARMONY/10 = 7/10"),
    (3/10,  "PROGRESS/10 = 3/10"),
]
for t, label in spine_pts:
    print(f"  sinc²({t:.4f}) = {sinc2(t):.10f}  ← {label}")

print()
print("  The sinc² value at W=3/50 (near the start) is ≈0.988 — very high.")
print("  The sinc² value at T*=5/7 (near end) is ≈0.121 — much lower.")
print("  The sinc² value at t=1/2 (midpoint) is 4/π²≈0.405 — the exact middle.")
print()
print("  4/π² sits between the W-entry value and the T*-exit value.")
print("  It is the corridor amplitude at the ring center.")

# ============================================================
# SECTION 7: UNIQUENESS AUDIT
# ============================================================
section("SECTION 7: UNIQUENESS AUDIT — WHAT IS AND IS NOT UNIQUE ABOUT t=1/2")

print("  Claim: 'sinc²(1/2) = 4/π² is the UNIQUE integer multiple of 1/π² at a")
print("  rational midpoint of any sub-interval of (0,1).'")
print()
print("  TEST: Which rational t=m/n give sinc²(t) = integer/π²?")
print("  sinc²(m/n) = n²sin²(πm/n)/(π²m²)")
print("  = integer/π² iff n²sin²(πm/n)/m² is an integer.")
print()
print("  Known cases:")
special_rationals = []
for n in range(2, 25):
    for m in range(1, n):
        if math.gcd(m, n) == 1:
            t = m / n
            sv = math.sin(math.pi * t)
            val = (n * sv / m) ** 2
            is_int = abs(val - round(val)) < 1e-8
            if is_int:
                special_rationals.append((m, n, round(val), t))
                print(f"  sinc²({m}/{n}) = {round(val)}/π²  (sin(π·{m}/{n}) = {sv:.6f})")

print()
print("  These are t where sin(πm/n) has a 'nice' algebraic form:")
print("  t=1/2: sin(π/2)=1  → 4/π² (trivial: unit sine)")
print("  t=1/4: sin(π/4)=√2/2 → 8/π² (√2 squared away)")
print("  t=1/6: sin(π/6)=1/2 → 9/π² (half-integer sine)")
print()
print("  The uniqueness of t=1/2 is NOT 'only rational with integer/π² value'.")
print("  It IS 'unique rational with sin(πt)=1 in (0,1)'.")
print("  The other cases involve algebraic values of sine, not the maximum.")
print()
print("  REFINED CLAIM (strongest true version):")
print("  t=1/2 is the unique t ∈ (0,1) where:")
print("    (a) sin(πt) = 1  (sine maximum, not just algebraic)")
print("    (b) sinc(t) = 2/π  (reciprocal of the half-period scale)")
print("    (c) sinc²(t) = 4/π²  (square of the fundamental sinc amplitude)")
print("  This is the SINE-MAXIMUM CHARACTERIZATION — not shared by t=1/4 or t=1/6.")

# ============================================================
# SECTION 8: SPINE CONNECTION — OVERDETERMINATION MAP
# ============================================================
section("SECTION 8: OVERDETERMINATION MAP — t=1/2 IN THE INHERITANCE STACK")

print("  The point t=1/2 / value 4/π² appears across multiple inheritance levels:")
print()
print("  RING-forced:")
print("    BALANCE=5 = centroid of (Z/10Z)* (D18d)")
print("    BALANCE=5 = centroid of ODD={1,3,5,7,9} (D21)")
print("    5 = additive midpoint of Z/10Z (D21)")
print("    5 → t=5/10=1/2 via ring normalization")
print()
print("  LENS-forced:")
print("    sinc²(1/2) = 4/π² (D3 — sinc² corridor value at midpoint)")
print("    sinc² monotone on (0,1), no interior extremum (B11)")
print("    t=1/2 is unique sine-maximum in (0,1) (B11)")
print()
print("  BRIDGE (B11 new):")
print("    Ring normalization t=v/10 explicitly maps BALANCE=5 → t=1/2.")
print("    The RING-forced centroid and the LENS-forced sine-maximum")
print("    are the SAME point, connected by the natural normalization.")
print()
print("  WHAT CHANGES IF THE RING CHANGES:")
print("  In Z/nZ, BALANCE would be n/2 (midpoint) if n is even.")
print("  The normalization t=v/n maps n/2 → 1/2 regardless of n.")
print("  The sine-maximum property of t=1/2 is universal (independent of n).")
print("  So B11 is not specific to Z/10Z — it holds for any ring Z/nZ")
print("  where the midpoint n/2 is the ring center.")

# ============================================================
# CONCLUSION
# ============================================================
section("CONCLUSION: THEOREM B11 AND WHAT IS LEFT OPEN")

print("  THEOREM B11 (Corridor Midpoint — Three Convergences):")
print()
print("  The point t=1/2 is characterized by three independent routes:")
print("  (1) Geometric: midpoint of valid corridor (0,1)")
print("  (2) Analytic:  unique t ∈ (0,1) where sin(πt)=1 → sinc²=4/π²")
print("  (3) Algebraic: BALANCE=5 maps to t=5/10=1/2 under ring normalization")
print()
print("  The value 4/π² = (2/π)² is the corridor amplitude at the sine-maximum,")
print("  the unique point in (0,1) where the sinc numerator is fully saturated.")
print()
print("  OVERDETERMINATION: t=1/2 carries five characterizations of the midpoint:")
print("  - Geometric center of (0,1)")
print("  - Image of ring centroid under t=v/10 normalization")
print("  - Unique sine-maximum locus in (0,1)")
print("  - sinc²-value = 4/π² = square of fundamental sinc constant 2/π")
print("  - Limit of grid midpoint k=p//2 as p→∞")
print()
print("  WHAT IS NOT PROVED:")
print("  - That 4/π² is 'universal' in any statistical sense beyond the midpoint")
print("  - Any connection to σ=1/2 in the Riemann zeta function")
print("  - That the midpoint VALUE controls corridor geometry (sinc² is monotone)")
print()
print("  TIER: B — all three characterizations proved; 'canonical sidelobe anchor'")
print("  interpretation is the conjecture (not yet proved as a formal theorem).")
print("  Upgrade path to C: show sinc²(1/2)=4/π² appears as a universal constant")
print("  in the prime-averaged corridor (verified empirically in D2/D3 work).")
print()

# Final assertions
assert abs(sinc2(0.5) - 4/math.pi**2) < 1e-14
assert strictly_dec
# Unique sine max
sine_maxes = [m/n for n in range(2,100) for m in range(1,n)
              if math.gcd(m,n)==1 and abs(math.sin(math.pi*m/n)-1.0) < 1e-8]
assert sine_maxes == [0.5], f"Expected only t=0.5, got {sine_maxes}"
# Ring map
assert 5/10 == 0.5
print("  ALL ASSERTIONS PASSED.")
print()
print("  CHAINS FROM: D2 (corridor), D3 (4/π²), D14 (spectral mean), D21 (ring center).")
print("  RELATION TO A10: B11 is the internal object A10 pointed at.")
print("    A10's external claim (σ=1/2 analogy) remains speculative.")
print("    B11's internal claim (t=1/2 triple convergence) is proved.")
