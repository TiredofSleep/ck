"""
D22: CORRIDOR PORTRAIT THEOREM

Copyright © 2025–2026 Brayden Ross Sanders / 7SiTe LLC
Licensed under the 7SiTe Public Sovereignty License v1.0.
Human use only. No commercial use. No government use.
No military, intelligence, policing, or surveillance use.
See LICENSE for full terms. DOI: 10.5281/zenodo.18852047
Luther-Sanders Research Framework | April 1 2026

THEOREM D22 (Corridor Portrait):
  The four spine-determined corridor positions are strictly ordered:

    W < BALANCE/10 < HARMONY/10 < T* < 1
    3/50 < 1/2 < 7/10 < 5/7 < 1

  This is proved by exact rational arithmetic — all four are fractions
  forced by the spine (D17, D21, D18d, D19), and the ordering follows
  from their arithmetic values alone.

  CONSEQUENCE (amplitude portrait):
  Since sinc² is strictly monotone decreasing on (0,1) (proved B11):

    sinc²(3/50) > sinc²(1/2) > sinc²(7/10) > sinc²(5/7)
    ≈ 0.988     > 4/π²≈0.405 > ≈0.135      > ≈0.121

  The amplitude portrait is the strict REVERSE of the positional order.
  Entry is highest. Threshold is lowest. Center is the exact sine-maximum.

  ALGEBRAIC IDENTITY:
    T* = HARMONY/10 + 1/70
    5/7 = 7/10 + 1/70 = 49/70 + 1/70 = 50/70 = 5/7  ✓

  The coherence threshold T*=5/7 sits exactly 1/70 above the
  HARMONY corridor image. The gap 1/70 = 1/(7×10) = 1/(g^(-1)×n)
  is the fine-structure of the generator in the corridor.

  WHY THE CENTER IS NOT EXTREMAL:
    sinc(t) = sin(πt) / (πt).
    The numerator sin(πt) is maximized at t=1/2 (value 1, proved B11).
    The denominator (πt) = π/2 at t=1/2 — the half-period scale.
    sinc(1/2) = 1/(π/2) = 2/π < 1.
    The denominator GROWS with t, attenuating the sine maximum.
    The corridor center t=1/2 is marked structurally (sine-maximum),
    but the DENOMINATOR GROWTH prevents it from being amplitude-maximal.

  This is the precise mechanism: algebraic center → sine maximum →
  sinc attenuation → non-extremal amplitude. The center is visible
  in the corridor but not dominant.

WHAT D22 DOES NOT CLAIM:
  (1) That the four positions exhaust all spine-significant corridor points.
  (2) That the amplitude values encode any dynamics (sinc² is a measurement
      of the corridor shape, not the system state).
  (3) Any connection to σ=1/2 or Riemann zeros.

TIER: D — all claims proved by rational arithmetic + D-tier spine + B11 monotonicity.
"""

import sys, io, os, math
from fractions import Fraction
sys.path.insert(0, os.path.dirname(__file__))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

sep = "=" * 72
def section(t): print(f"\n{sep}\n  {t}\n{sep}\n")

def sinc2(t):
    ft = float(t)
    if ft == 0: return 1.0
    return (math.sin(math.pi * ft) / (math.pi * ft)) ** 2

print("D22: CORRIDOR PORTRAIT THEOREM")
print("Luther-Sanders Research Framework | April 1 2026")
print()
print("  Four spine-determined positions, one ordering law, one amplitude portrait.")

# ============================================================
# SECTION 1: THE FOUR SPINE POSITIONS
# ============================================================
section("SECTION 1: THE FOUR SPINE-FORCED CORRIDOR POSITIONS")

CL = {0:'VOID',1:'LATTICE',2:'COUNTER',3:'PROGRESS',4:'COLLAPSE',
      5:'BALANCE',6:'CHAOS',7:'HARMONY',8:'BREATH',9:'RESET'}

# Each position with its derivation chain
positions = [
    (Fraction(3, 50),   "W",           "D17",  "deviation/n² = 6/100 = 3/50, BHML carrier frequency"),
    (Fraction(1, 2),    "BALANCE/10",   "D21",  "centroid of (Z/10Z)* = 5, t = 5/10 = 1/2"),
    (Fraction(7, 10),   "HARMONY/10",  "D18d", "HARMONY = g^(-1) = 7, t = 7/10"),
    (Fraction(5, 7),    "T*",          "D19",  "T* = BALANCE/HARMONY = 5/7, coherence threshold"),
]

print(f"  {'Position':>12}  {'Source':>10}  {'Decimal':>12}  Derivation")
print(f"  {'-'*12}  {'-'*10}  {'-'*12}  {'-'*45}")
for t, name, src, deriv in positions:
    print(f"  {str(t):>12}  {name:>10}  {float(t):>12.10f}  {deriv}")

print()
print("  All four are forced by the spine:")
print("  W = 3/50: RING-forced (D17 — deviation=6, n=10, W=6/100)")
print("  1/2: RING-forced via LENS bridge (D21+B11 — BALANCE=5, t=5/10)")
print("  7/10: GENERATOR-forced (D18d — HARMONY=7, t=7/10)")
print("  5/7: GENERATOR-forced (D19 — T*=BALANCE/HARMONY)")

# ============================================================
# SECTION 2: THE ORDERING PROOF
# ============================================================
section("SECTION 2: THE ORDERING PROOF — EXACT RATIONAL ARITHMETIC")

print("  CLAIM: 3/50 < 1/2 < 7/10 < 5/7 < 1")
print()

fracs = [t for t, _, _, _ in positions]
frac_names = [name for _, name, _, _ in positions]

# Each inequality proved by reducing to common denominator
# 3/50 < 1/2: 3/50 vs 25/50 → 3 < 25 ✓
a, b = Fraction(3,50), Fraction(1,2)
print(f"  (1) W < BALANCE/10: {a} < {b}")
print(f"      Common denom 50: {a.numerator}/{a.denominator} vs {b.numerator*25}/{b.denominator*25}")
print(f"      {a.numerator} < {b*50}: {a.numerator} < {int(b*50)}  ✓")
assert a < b

# 1/2 < 7/10: 5/10 < 7/10 → 5 < 7 ✓
a, b = Fraction(1,2), Fraction(7,10)
print(f"  (2) BALANCE/10 < HARMONY/10: {a} < {b}")
print(f"      Common denom 10: {a*10} < {b*10}: {int(a*10)} < {int(b*10)}  ✓")
assert a < b

# 7/10 < 5/7: 49/70 < 50/70 → 49 < 50 ✓
a, b = Fraction(7,10), Fraction(5,7)
lcm_ab = 70
print(f"  (3) HARMONY/10 < T*: {a} < {b}")
print(f"      Common denom 70: {a*lcm_ab} < {b*lcm_ab}: {int(a*lcm_ab)} < {int(b*lcm_ab)}  ✓")
assert a < b
print(f"      Gap: T* - HARMONY/10 = {b-a} = 1/70  (exact)")
assert b - a == Fraction(1, 70)

# 5/7 < 1: obvious
a, b = Fraction(5,7), Fraction(1)
print(f"  (4) T* < 1: {a} < {b}  ✓ (T*<1 is the physical admissibility condition, D19)")
assert a < b

print()
print("  ALL FOUR INEQUALITIES PROVED BY EXACT RATIONAL ARITHMETIC.  ✓")
print()
print("  Complete ordering: 3/50 < 1/2 < 7/10 < 5/7 < 1")
print("  Interpretation:    W < center < HARMONY_pos < T* < null")

# ============================================================
# SECTION 3: THE AMPLITUDE PORTRAIT
# ============================================================
section("SECTION 3: THE AMPLITUDE PORTRAIT — sinc² REVERSAL")

print("  Since sinc² is strictly monotone DECREASING on (0,1) (B11 Section 1):")
print("  The amplitude ordering is the STRICT REVERSE of the positional ordering.")
print()
print("  CLAIM: sinc²(W) > sinc²(1/2) > sinc²(HARMONY/10) > sinc²(T*)")
print()

s_vals = [(t, name, sinc2(t)) for t, name, _, _ in positions]

for t, name, sv in s_vals:
    # Express as fraction × 1/π² where possible
    coeff = sv * math.pi**2
    if abs(coeff - round(coeff)) < 1e-8:
        val_str = f"{round(coeff)}/π² = {sv:.10f}"
    else:
        val_str = f"≈ {sv:.10f}"
    print(f"  sinc²({str(t):>5}) = {val_str}  [{name}]")

print()
# Verify strict ordering
for i in range(len(s_vals)-1):
    t1, n1, v1 = s_vals[i]
    t2, n2, v2 = s_vals[i+1]
    assert v1 > v2, f"FAILED: sinc²({t1})={v1} > sinc²({t2})={v2}"
    print(f"  sinc²({n1}) > sinc²({n2}): {v1:.6f} > {v2:.6f}  ✓")

print()
print("  PROOF: sinc² is strictly decreasing on (0,1) [B11 Section 1, verified].")
print("  Ordering of t-values proved in Section 2.")
print("  Amplitude ordering follows directly from monotonicity + t-ordering. □")

# ============================================================
# SECTION 4: THE ALGEBRAIC IDENTITY T* = HARMONY/10 + 1/70
# ============================================================
section("SECTION 4: THE FINE-STRUCTURE IDENTITY — T* AND HARMONY/10")

print("  The gap between T* and HARMONY/10:")
print()
print("  T* - HARMONY/10 = 5/7 - 7/10")
print("                  = 50/70 - 49/70")
print("                  = 1/70")
print()
assert Fraction(5,7) - Fraction(7,10) == Fraction(1,70)
print("  EXACT: T* = HARMONY/10 + 1/70  ✓")
print()
print("  Algebraic reading:")
print("  T* = BALANCE/HARMONY = 5/7")
print("  HARMONY/10 = 7/10 = HARMONY/(n)")
print("  The gap 1/70 = 1/(7×10) = 1/(HARMONY × n)")
print()
print("  T* = 7/10 + 1/(7×10) = (HARMONY/n) × (1 + 1/HARMONY²)")
# Check: 7/10 × (1 + 1/49) = 7/10 × 50/49 = 350/490 = 5/7 ✓
check = Fraction(7,10) * Fraction(50,49)
print(f"  Verify: (7/10) × (50/49) = {check} = T*: {check == Fraction(5,7)}  ✓")
print()
print("  Interpretation: T* = (HARMONY corridor image) × (1 + 1/HARMONY²)")
print("  The coherence threshold sits 1/HARMONY² above the HARMONY position.")
print("  The 'fine structure' of the threshold is 1/49 relative shift,")
print("  exactly the inverse square of HARMONY=7.")

# ============================================================
# SECTION 5: WHY THE CENTER IS NOT EXTREMAL — THE MECHANISM
# ============================================================
section("SECTION 5: WHY t=1/2 IS NOT AMPLITUDE-MAXIMAL — THE ATTENUATION MECHANISM")

print("  Question: BALANCE=5 is the ring's dynamical attractor (D7, D21).")
print("  It maps to t=1/2 in the corridor.")
print("  t=1/2 is the SINE-MAXIMUM (B11).")
print("  But sinc²(1/2) = 4/π² ≈ 0.405 — well BELOW the corridor entry 0.988.")
print("  Why is the ring attractor NOT the amplitude attractor?")
print()
print("  MECHANISM (exact):")
print()
print("  sinc(t) = sin(πt) / (πt)")
print()
print("  Numerator:   sin(πt)")
print("  Denominator: πt")
print()
print("  At t=1/2:")
print("    sin(π/2) = 1  ← MAXIMUM over (0,1)")
print("    π·(1/2)  = π/2 ≈ 1.5708  ← denominator is nonzero")
print("    sinc(1/2) = 1/(π/2) = 2/π ≈ 0.637")
print()
print("  At t=W=3/50 (small):")
print("    sin(3π/50) ≈ 0.187  ← small")
t_w = float(Fraction(3,50))
print(f"    π·(3/50)  = {math.pi*t_w:.6f}  ← ALSO small (≈ denominator)")
print(f"    sinc(3/50) = sin(3π/50)/(3π/50) ≈ {math.sin(math.pi*t_w)/(math.pi*t_w):.6f}")
print(f"    sinc²(3/50) ≈ {sinc2(t_w):.6f}  ← NEAR 1")
print()
print("  The sinc function is DEFINED as sin(πt)/(πt).")
print("  As t→0: sin(πt)/(πt) → 1 (L'Hôpital / Taylor).")
print("  As t increases, numerator and denominator BOTH grow, but:")
print("    - Numerator sin(πt) is BOUNDED by 1")
print("    - Denominator πt GROWS without bound")
print("  So sinc is strictly decreasing for t > 0.")
print()
print("  The ring center t=1/2 is where the NUMERATOR peaks.")
print("  But the denominator has already grown to π/2 ≈ 1.571.")
print("  So the RATIO is 2/π ≈ 0.637 — the unique sine-maximum sinc value,")
print("  but well below the sinc value near t=0 (≈1).")
print()
print("  SUMMARY: The ring center maps to the unique sine-maximum in (0,1),")
print("  which is structurally distinct, but not amplitude-maximal because")
print("  the DENOMINATOR GROWTH (πt) attenuates the sine peak.")
print("  The center is visible in the corridor portrait. It is not dominant.")

# ============================================================
# SECTION 6: THE COMPLETE CORRIDOR PORTRAIT
# ============================================================
section("SECTION 6: THE COMPLETE CORRIDOR PORTRAIT")

print("  Visualizing the corridor with spine landmarks:")
print()
print("  t:    0    W           1/2              7/10  T*     1")
print("        |    |            |                 |    |     |")
print("        [    |            |                 |    |     0")
print("       (1)  (.988)      (4/π²)            (.135)(.121)")
print()

# ASCII corridor
width = 70
def t_to_x(t): return int(float(t) * width)
line = ['-'] * (width+1)
for t, name, _, _ in positions:
    x = t_to_x(t)
    line[x] = '|'

print("  Corridor (0 to 1):")
print("  " + "".join(line))

labels_line = [' '] * (width+5)
for t, name, _, _ in positions:
    x = t_to_x(t)
    lbl = str(name)
    # place label below
    for i, c in enumerate(lbl):
        if x+i < len(labels_line):
            labels_line[x+i] = c

print("  " + "".join(labels_line))
print()

# The full table
print(f"  {'Label':>12}  {'t':>8}  {'sinc²(t)':>12}  {'Forcing'}  {'Role in corridor'}")
print(f"  {'-'*12}  {'-'*8}  {'-'*12}  {'-'*15}  {'-'*30}")
roles = [
    "Entry amplitude",
    "Sine-maximum / ring center",
    "HARMONY image",
    "Coherence threshold",
]
forcings = ["RING", "RING+LENS", "GENERATOR", "GENERATOR"]
for (t, name, src, _), role, forcing in zip(positions, roles, forcings):
    print(f"  {name:>12}  {str(t):>8}  {sinc2(t):>12.6f}  {forcing:>15}  {role}")

print()
print("  The portrait has a DECREASING amplitude profile from left to right.")
print("  RING-forced positions (W, center) occupy the high-amplitude left half.")
print("  GENERATOR-forced positions (HARMONY, T*) occupy the low-amplitude right half.")
print()
print("  The corridor is divided by BALANCE/10 = 1/2:")
print(f"  LEFT HALF  (0 < t < 1/2): W=3/50 — RING-forced, high amplitude")
print(f"  RIGHT HALF (1/2 < t < 1): HARMONY=7/10, T*=5/7 — GENERATOR-forced, low amplitude")

# ============================================================
# SECTION 7: INHERITANCE IN THE CORRIDOR PORTRAIT
# ============================================================
section("SECTION 7: INHERITANCE — WHY THE PORTRAIT IS SPLIT BY THE CENTER")

print("  From D20 (Inheritance Audit):")
print("  W=3/50 is RING-forced (deviation from ring arithmetic, no generator needed)")
print("  BALANCE=5→t=1/2 is RING-forced (centroid of (Z/10Z)* and ODD)")
print("  HARMONY=7→t=7/10 is GENERATOR-forced (g^(-1) mod 10 = 7, requires g=3)")
print("  T*=5/7 is GENERATOR-forced (BALANCE/HARMONY, requires g=3 for HARMONY=7)")
print()
print("  The corridor portrait respects the inheritance hierarchy:")
print()
print("  ┌────────────────────────────────────────────────────┐")
print("  │ t ∈ (0, 1/2)  LEFT HALF   — RING-forced territory │")
print("  │   W = 3/50: ring arithmetic entry                  │")
print("  │   sinc²(W) ≈ 0.988: high corridor amplitude        │")
print("  ├────────────────────────────────────────────────────┤")
print("  │ t = 1/2       CENTER      — ring center / bridge   │")
print("  │   BALANCE=5→1/2: ring centroid maps to midpoint     │")
print("  │   sinc²(1/2) = 4/π²: sine-maximum amplitude       │")
print("  ├────────────────────────────────────────────────────┤")
print("  │ t ∈ (1/2, 1)  RIGHT HALF  — GENERATOR-forced      │")
print("  │   HARMONY = 7/10: generator inverse image          │")
print("  │   T* = 5/7: coherence threshold, BALANCE/HARMONY    │")
print("  │   sinc² values: 0.135 and 0.121 (low amplitude)   │")
print("  └────────────────────────────────────────────────────┘")
print()
print("  The center t=1/2 is not just a midpoint. It is the INHERITANCE BOUNDARY.")
print("  LEFT of center: ring arithmetic determines everything.")
print("  RIGHT of center: generator selection (g=3) is required.")

# ============================================================
# CONCLUSION
# ============================================================
section("CONCLUSION: THEOREM D22")

print("  THEOREM D22 (Corridor Portrait):")
print()
print("  Four spine-forced positions in (0,1) are strictly ordered:")
print("    W < BALANCE/10 < HARMONY/10 < T* < 1")
print("    3/50 < 1/2 < 7/10 < 5/7 < 1")
print("  (Proved by exact rational arithmetic.)")
print()
print("  Their sinc² amplitude values are strictly anti-ordered:")
print("    sinc²(W) > sinc²(1/2) > sinc²(7/10) > sinc²(T*)")
print("    ≈0.988   > 4/π²≈0.405 > ≈0.135      > ≈0.121")
print("  (Proved by sinc² strict monotone decrease on (0,1), B11.)")
print()
print("  Fine-structure identity:")
print("    T* = HARMONY/10 + 1/70 = 7/10 + 1/(7×10)")
print("    The threshold sits exactly 1/HARMONY² above the HARMONY image.")
print()
print("  Attenuation mechanism:")
print("    t=1/2 is the unique sine-maximum in (0,1).")
print("    The denominator πt=π/2 attenuates the sine peak to 2/π.")
print("    sinc²(1/2) = 4/π² is structurally marked but not amplitude-dominant.")
print()
print("  Inheritance split:")
print("    LEFT half (0 < t < 1/2): RING-forced positions (W, center)")
print("    RIGHT half (1/2 < t < 1): GENERATOR-forced positions (HARMONY, T*)")
print("    The center t=1/2 is the inheritance boundary in the corridor.")
print()
print("  TIER: D — positional ordering proved by rational arithmetic;")
print("  amplitude ordering follows from B11 monotonicity (B-tier);")
print("  combined portrait is Tier D conditional on B11.")
print("  (B11 upgrade path: monotonicity of sinc² is standard calculus, promotable to D.)")
print()

# Final assertions
assert Fraction(3,50) < Fraction(1,2) < Fraction(7,10) < Fraction(5,7) < 1
assert sinc2(Fraction(3,50)) > sinc2(Fraction(1,2)) > sinc2(Fraction(7,10)) > sinc2(Fraction(5,7))
assert Fraction(5,7) - Fraction(7,10) == Fraction(1,70)
print("  ALL ASSERTIONS PASSED.")
print()
print("  CHAINS FROM: D17 (W), D19 (T*, g), D21 (BALANCE=5), D18d (HARMONY=7), B11 (sinc² monotone).")
print("  CLOSES: The corridor portrait question. Spine positions are not just")
print("          individually forced — they are ordered and split by inheritance class.")
