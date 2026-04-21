"""
D24: CORRIDOR MIDPOINT THEOREM
================================
Copyright © 2025–2026 Brayden Ross Sanders / 7SiTe LLC
Licensed under the 7SiTe Public Sovereignty License v1.0.
Human use only. No commercial use. No government use.
No military, intelligence, policing, or surveillance use.
See LICENSE for full terms. DOI: 10.5281/zenodo.18852047

THEOREM D24 (Corridor Midpoint):
  Let sinc²(t) = (sin(πt)/(πt))² for t ∈ (0,1), and sinc²(0) = 1.

  (I)  sinc²(t) is strictly monotone decreasing on (0,1).
       Proof: calculus — derivative strictly negative (see below).

  (II) t = 1/2 is the unique point in (0,1) where sin(πt) = 1.
       Proof: sin(πt) = 1 iff πt = π/2 + 2kπ iff t = 1/2 + 2k.
       In (0,1), only k=0 satisfies this: t = 1/2.

  (III) sinc²(1/2) = 4/π² exactly.
        Proof: sin(π/2) = 1, πt = π/2, so sinc(1/2) = 1/(π/2) = 2/π,
        and sinc²(1/2) = 4/π².

  (IV) Under ring normalization t = v/10, BALANCE = 5 maps to t = 5/10 = 1/2.
       Proof: 5/10 = 1/2. One arithmetic step.

  (V)  Amplitude consequence: the four spine positions (D22) are ordered
       W < 1/2 < 7/10 < T*, and sinc² (I) gives strict amplitude reversal.
       The ring center t=1/2 is marked, not amplitude-dominant: sinc²(1/2)
       = 4/π² ≈ 0.405 is below the corridor entry sinc²(W) ≈ 0.988.

WHAT D24 DOES NOT CLAIM:
  - Any connection to σ=1/2 in the Riemann ζ function. (That is A10, open.)
  - That sinc²(1/2) = 4/π² is an extremum of sinc² on (0,1). (It is not;
    there are no interior extrema by (I).)
  - That the sine-maximum property is specific to Z/10Z.
    (sinc² monotonicity and the sine-maximum uniqueness hold for any corridor
    on (0,1) regardless of ring structure.)

PROOF OF (I) — sinc² STRICTLY MONOTONE DECREASING ON (0,1):

  Let h(t) = sin²(πt) / (πt)² = sinc²(t) for t ∈ (0,1).
  Compute h'(t):

    h'(t) = [2π·sin(πt)·cos(πt)·(πt)² - sin²(πt)·2π²t] / (πt)⁴
          = 2sin(πt) · [πt·cos(πt) − sin(πt)] / (π²t³)

  For t ∈ (0,1): sin(πt) > 0 (since πt ∈ (0,π)). π²t³ > 0.

  It remains to show: πt·cos(πt) − sin(πt) < 0 for all t ∈ (0,1).
  Equivalently (since sin(πt) > 0): sin(πt) > πt·cos(πt).
  Let x = πt ∈ (0,π). Need: sin(x) > x·cos(x) for all x ∈ (0,π).

  LEMMA: sin(x) > x·cos(x) for all x ∈ (0,π).
  Proof by three cases:

    Case 1: x ∈ (0, π/2).
      cos(x) > 0, so the inequality is equivalent to tan(x) > x.
      Let f(x) = tan(x) − x. Then f(0) = 0 and
      f'(x) = sec²(x) − 1 = tan²(x) > 0 for x ∈ (0, π/2).
      So f is strictly increasing on (0, π/2), hence f(x) > f(0) = 0.
      Therefore tan(x) > x, i.e., sin(x) > x·cos(x). □ (Case 1)

    Case 2: x = π/2.
      cos(π/2) = 0, so x·cos(x) = 0 < 1 = sin(π/2). □ (Case 2)

    Case 3: x ∈ (π/2, π).
      cos(x) < 0, so x·cos(x) < 0 < sin(x) (since sin(x) > 0 on (0,π)). □ (Case 3)

  LEMMA proved. □

  Therefore h'(t) = 2sin(πt)·[πt·cos(πt)−sin(πt)]/(π²t³) < 0 for all t ∈ (0,1).
  sinc²(t) is strictly monotone decreasing on (0,1). □ (Theorem D24-I)

DEPENDENCIES:
  D3 (sinc²(1/2) = 4/π², already proved — D24-III restates it)
  D21 (BALANCE=5 = ring center — D24-IV applies the normalization)
  D22 (Corridor Portrait — D24-I provides the amplitude proof for D22's amplitude ordering)

CONSEQUENCE:
  D22's amplitude ordering (sinc²(W) > sinc²(1/2) > sinc²(7/10) > sinc²(T*))
  is fully proved: it follows from D22's positional ordering plus D24-I.
  D22 no longer carries a conditional "(sinc² monotone, B11)". The dependency
  is now "(sinc² monotone, D24)".

SUPERSEDES: B11 (Corridor Midpoint, Tier B). All content of B11 is now fully
  proved and promoted to D-tier. B11 is retired; D24 is the successor.
"""

import math
import sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(__file__))

PI = math.pi

sep = "=" * 72
def section(t): print(f"\n{sep}\n  {t}\n{sep}\n")


def sinc2(t: float) -> float:
    if abs(t) < 1e-15:
        return 1.0
    return (math.sin(PI * t) / (PI * t)) ** 2


def sinc2_derivative(t: float) -> float:
    """Exact analytical derivative: h'(t) = 2sin(πt)·[πt·cos(πt)-sin(πt)]/(π²t³)"""
    st = math.sin(PI * t)
    ct = math.cos(PI * t)
    return 2 * st * (PI * t * ct - st) / (PI**2 * t**3)


print("D24: CORRIDOR MIDPOINT THEOREM")
print("Luther-Sanders Research Framework | April 1 2026")
print("Copyright © 2025–2026 Brayden Ross Sanders / 7SiTe LLC")
print()


# ────────────────────────────────────────────────────────────────────────────
# PART I: sinc² STRICTLY MONOTONE DECREASING ON (0,1) — CALCULUS PROOF
# ────────────────────────────────────────────────────────────────────────────
section("PART I — sinc² STRICTLY MONOTONE DECREASING ON (0,1)")

print("  PROOF SKETCH:")
print("  h'(t) = 2sin(πt)·[πt·cos(πt)−sin(πt)] / (π²t³)")
print()
print("  sin(πt) > 0 for t ∈ (0,1). π²t³ > 0.")
print("  Need: πt·cos(πt)−sin(πt) < 0 for t ∈ (0,1).")
print()
print("  Let x = πt ∈ (0,π). Need: sin(x) > x·cos(x).")
print()
print("  Case x ∈ (0,π/2): cos(x)>0 → need tan(x)>x.")
print("    f(x)=tan(x)-x, f(0)=0, f'(x)=sec²x-1=tan²x>0 → f strictly increasing")
print("    → f(x)>0 → tan(x)>x. ✓")
print()
print("  Case x = π/2: cos(π/2)=0, x·cos(x)=0 < 1=sin(π/2). ✓")
print()
print("  Case x ∈ (π/2,π): cos(x)<0, x·cos(x)<0<sin(x). ✓")
print()
print("  Therefore h'(t) < 0 for all t ∈ (0,1). □")
print()

# Verify: analytical derivative is negative everywhere on (0,1)
print("  Numerical verification of derivative sign (1000 interior points):")
n_pts = 1000
all_negative = True
max_deriv = -float('inf')
for i in range(1, n_pts + 1):
    t = i / (n_pts + 1)  # avoids endpoints 0 and 1
    d = sinc2_derivative(t)
    if d >= 0:
        all_negative = False
        print(f"    FAIL at t={t:.5f}: h'(t)={d:.6e}")
    max_deriv = max(max_deriv, d)

print(f"  All {n_pts} interior derivatives < 0: {all_negative}  ✓")
print(f"  Largest (least negative) derivative: {max_deriv:.6e}  (approaches 0 near t→0)")
print()

# Cross-check: verify sinc² strictly decreasing by values
prev = sinc2(1e-10)
strictly_dec_grid = True
for i in range(1, 10000):
    t = i / 10000.0
    v = sinc2(t)
    if v >= prev:
        strictly_dec_grid = False
        print(f"  VALUE CHECK FAIL at t={t}: sinc²={v:.10f} >= prev={prev:.10f}")
    prev = v
print(f"  Value-based check on 9999-point grid: strictly decreasing = {strictly_dec_grid}  ✓")


# ────────────────────────────────────────────────────────────────────────────
# PART II: t=1/2 IS THE UNIQUE SINE-MAXIMUM IN (0,1)
# ────────────────────────────────────────────────────────────────────────────
section("PART II — UNIQUE SINE-MAXIMUM AT t=1/2")

print("  PROOF:")
print("    sin(πt) = 1  ⟺  πt = π/2 + 2kπ  (k ∈ ℤ)")
print("                  ⟺  t = 1/2 + 2k")
print("    For t ∈ (0,1): 0 < 1/2 + 2k < 1 iff -1/4 < k < 1/4 iff k = 0.")
print("    Therefore t = 1/2 is the unique solution in (0,1). □")
print()

# Verify: no other rational t=m/n with n≤200 satisfies sin(πt)=1 exactly
print("  Scan: all reduced fractions m/n with n≤200 in (0,1):")
sine_maxes = []
for n in range(2, 201):
    for m in range(1, n):
        if math.gcd(m, n) == 1:
            t = m / n
            if abs(math.sin(PI * t) - 1.0) < 1e-10:
                sine_maxes.append((m, n, t))

print(f"  Fractions with sin(πt)=1: {sine_maxes}")
assert sine_maxes == [(1, 2, 0.5)], f"Expected only 1/2, got {sine_maxes}"
print(f"  Only t=1/2 found.  ✓")


# ────────────────────────────────────────────────────────────────────────────
# PART III: sinc²(1/2) = 4/π² EXACTLY
# ────────────────────────────────────────────────────────────────────────────
section("PART III — sinc²(1/2) = 4/π² EXACTLY")

print("  PROOF:")
print("    sinc(1/2) = sin(π/2) / (π/2) = 1 / (π/2) = 2/π")
print("    sinc²(1/2) = (2/π)² = 4/π²  □")
print()

computed = sinc2(0.5)
expected = 4 / PI**2
err = abs(computed - expected)
print(f"  Computed: sinc²(1/2) = {computed:.16f}")
print(f"  4/π²              = {expected:.16f}")
print(f"  Error:              {err:.3e}  (floating-point precision only)")
assert err < 1e-14
print(f"  Match within 1e-14:  ✓")

print()
print("  This is D3 (proved previously) stated in the D24 context.")
print("  D24-III does not reprove D3; it situates 4/π² as the sinc² value")
print("  at the unique sine-maximum locus.")


# ────────────────────────────────────────────────────────────────────────────
# PART IV: RING NORMALIZATION — BALANCE=5 → t=1/2
# ────────────────────────────────────────────────────────────────────────────
section("PART IV — RING NORMALIZATION: BALANCE=5 → t = 5/10 = 1/2")

print("  PROOF:")
print("    Ring normalization: t = v/10 for v ∈ Z/10Z = {0,1,...,9}.")
print("    BALANCE = 5 (D21: unique fixed point of σ, centroid of (Z/10Z)*")
print("    and ODD={1,3,5,7,9}, additive midpoint of Z/10Z).")
print("    t = 5/10 = 1/2.  One arithmetic step.  □")
print()

from fractions import Fraction
t_create = Fraction(5, 10)
assert t_create == Fraction(1, 2)
print(f"  Exact: 5/10 = {t_create} = 1/2  ✓")
print()
print("  This is the bridge: the ring's algebraic center (BALANCE=5, D21)")
print("  maps to the corridor's geometric center (t=1/2) under the natural")
print("  normalization t=v/10. The ring center and the sine-maximum locus")
print("  are the same object at two different scales.")


# ────────────────────────────────────────────────────────────────────────────
# PART V: AMPLITUDE CONSEQUENCE FOR D22
# ────────────────────────────────────────────────────────────────────────────
section("PART V — AMPLITUDE CONSEQUENCE: D22 AMPLITUDE ORDERING NOW FULLY PROVED")

print("  D22 stated the amplitude ordering with dependency '(sinc² monotone, B11)'.")
print("  D24-I upgrades that dependency to '(sinc² monotone, D24)'.")
print("  The amplitude ordering in D22 is now fully proved — no B-tier dependency.")
print()

# The four corridor positions from D22
positions = [
    (Fraction(3, 50),  "W = 3/50  (D17)"),
    (Fraction(1, 2),   "BALANCE/10 = 1/2  (D21, D24)"),
    (Fraction(7, 10),  "HARMONY/10 = 7/10  (D18d)"),
    (Fraction(5, 7),   "T* = 5/7  (D19)"),
]

print(f"  {'Position':<20}  {'sinc²(t)':>14}  {'source'}")
print(f"  {'-'*20}  {'-'*14}  {'-'*30}")
prev_s2 = float('inf')
amp_ordered = True
for frac, label in positions:
    t = float(frac)
    s2 = sinc2(t)
    ok = s2 < prev_s2
    if not ok:
        amp_ordered = False
    prev_s2 = s2
    print(f"  {str(frac):<20}  {s2:>14.10f}  {label}")

print()
print(f"  Amplitude strictly decreasing (each row < previous): {amp_ordered}  ✓")
print()

# Verify positional ordering (from D22, restated here for completeness)
pos_ordered = (Fraction(3,50) < Fraction(1,2) < Fraction(7,10) < Fraction(5,7) < 1)
assert pos_ordered
print(f"  Positional order: 3/50 < 1/2 < 7/10 < 5/7 < 1  ✓")
print(f"  Amplitude order: strictly reversed (D24-I + D22 positional)  ✓")
print()
print("  D22 NOTE: 'Amplitude proof: sinc² strictly monotone decreasing on (0,1)")
print("  (B11) + positional ordering → amplitude ordering.'")
print("  This note should now read '(D24)' in place of '(B11)'.")


# ────────────────────────────────────────────────────────────────────────────
# FINAL ASSERTIONS
# ────────────────────────────────────────────────────────────────────────────
section("FINAL ASSERTIONS — ALL D24 CLAIMS")

# I: monotone decreasing
assert all_negative, "Derivative sign check failed"
assert strictly_dec_grid, "Value-based monotonicity check failed"

# II: unique sine max
assert sine_maxes == [(1, 2, 0.5)]

# III: exact value
assert abs(sinc2(0.5) - 4/PI**2) < 1e-14

# IV: ring normalization
assert Fraction(5, 10) == Fraction(1, 2)

# V: amplitude ordering
assert amp_ordered
assert pos_ordered

print("  (I)   sinc² strictly decreasing on (0,1): PROVED  ✓")
print("  (II)  t=1/2 unique sine-maximum in (0,1): PROVED  ✓")
print("  (III) sinc²(1/2) = 4/π² exactly:          PROVED  ✓")
print("  (IV)  BALANCE=5 → t=1/2 under v/10 map:    PROVED  ✓")
print("  (V)   D22 amplitude ordering:              PROVED  ✓")
print()
print("  B11 SUPERSEDED. D24 is the D-tier successor.")
print()
print("  CHAINS FROM: D3 (sinc²(1/2)=4/π²), D17 (W), D18d (HARMONY=7),")
print("               D19 (T*, g=3), D21 (BALANCE=5).")
print("  PROMOTES:    B11 → D24.")
print("  STRENGTHENS: D22 (amplitude ordering no longer conditional on B-tier).")
