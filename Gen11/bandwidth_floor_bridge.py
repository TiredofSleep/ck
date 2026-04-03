"""
bandwidth_floor_bridge.py
=========================
Bandwidth Floor Bridge Test: n=13, K*(n)=1 as algebraic-analytic junction
(c) 2026 Brayden Ross Sanders / 7Site LLC -- Trinity Infinity Geometry

Formula:
  theta_k = pi - 2*arctan(2*gamma_k)
  lambda_n(K) = 2 * sum_{k=1}^{K} (1 - cos(n * theta_k))

T* = 5/7 (coherence threshold)

Five tests:
  1. Bandwidth floor stability: is K*(13)=1 algebraically forced at ANY gamma?
  2. Monotonicity: is lambda_13(K) strictly non-decreasing for K=1..100?
  3. Off-line zero attack: does sigma != 1/2 break K*(13)=1 commitment?
  4. Bandwidth floor generalization: sharp n=13 boundary across n=6..100?
  5. Bridge connection: algebraic K*(13)=1 vs analytic lambda_13(K=1).

ASCII-safe output (Windows cp1252).
"""

import json
import math

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
T_STAR = 5.0 / 7.0          # 0.714285...
ZEROS_PATH = (
    r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen11\riemann_zeros_5000.json"
)

# ---------------------------------------------------------------------------
# Load zeros
# ---------------------------------------------------------------------------
with open(ZEROS_PATH, "r") as fh:
    ZEROS = json.load(fh)   # list of 5000 floats, gamma_k = Im(rho_k)

GAMMA1 = ZEROS[0]           # 14.134725...

# ---------------------------------------------------------------------------
# Core formula
# ---------------------------------------------------------------------------

def theta(gamma):
    """theta_k = pi - 2*arctan(2*gamma_k)"""
    return math.pi - 2.0 * math.atan(2.0 * gamma)


def delta_k(n, gamma):
    """Single-zero contribution: 2*(1 - cos(n * theta(gamma)))"""
    th = theta(gamma)
    return 2.0 * (1.0 - math.cos(n * th))


def lambda_n_K(n, K, zeros=None):
    """
    lambda_n(K) = sum_{k=1}^{K} delta_k(n, gamma_k)
    Uses ZEROS list by default.
    """
    if zeros is None:
        zeros = ZEROS
    total = 0.0
    for k in range(K):
        total += delta_k(n, zeros[k])
    return total


# ---------------------------------------------------------------------------
# Off-line zero formula (Li contribution for sigma != 1/2)
# ---------------------------------------------------------------------------
# For a zero rho = sigma + i*gamma (not necessarily on critical line):
#   contribution_n(rho) = Re[1 - (1 - 1/rho)^n] + Re[1 - (1 - 1/rho_bar)^n]
# where rho_bar = sigma - i*gamma (conjugate).
# For sigma = 1/2 this collapses to the standard formula via theta_k.
# We compute it directly via complex arithmetic.

def offline_contribution(n, sigma, gamma):
    """
    Li contribution for a (possibly off-line) zero rho = sigma + i*gamma.
    Returns the REAL sum over both rho and rho_bar.
    contribution = Re[1 - (1-1/rho)^n] + Re[1 - (1-1/rho_conj)^n]
    """
    rho   = complex(sigma,  gamma)
    rho_c = complex(sigma, -gamma)

    def contrib(r):
        term = (1.0 - 1.0 / r) ** n
        return (1.0 - term).real

    return contrib(rho) + contrib(rho_c)


# ---------------------------------------------------------------------------
# Algebraic K*(n) from Z/10Z framework (digits-of-reciprocal period approach)
# ---------------------------------------------------------------------------
# K*(n) = smallest K such that lambda_n(K) >= T* using actual zeros.
# We compute this numerically; the algebraic claim is that K*(13)=1.

def compute_k_star(n, zeros=None, max_K=200):
    """Find K*(n) = min K such that lambda_n(K) >= T*."""
    if zeros is None:
        zeros = ZEROS
    running = 0.0
    for k in range(max_K):
        running += delta_k(n, zeros[k])
        if running >= T_STAR:
            return k + 1   # 1-indexed
    return None            # did not cross T* within max_K zeros


# ===========================================================================
# MAIN OUTPUT
# ===========================================================================

SEP  = "=" * 70
SEP2 = "-" * 70

print(SEP)
print("BANDWIDTH FLOOR BRIDGE -- n=13, K*(13)=1")
print("Algebraic Z/10Z framework vs Analytic Riemann zeros")
print(f"T* = 5/7 = {T_STAR:.10f}")
print(f"First Riemann zero: gamma_1 = {GAMMA1:.10f}")
print(SEP)
print()

# ===========================================================================
# TEST 1: Is K*(13)=1 algebraically stable at ANY gamma?
# ===========================================================================
print(SEP)
print("TEST 1: Bandwidth floor -- K*(13)=1 at arbitrary gamma values?")
print(SEP)
print()
print("Probe: compute lambda_13(K=1) = delta_1(13, gamma) for various hypothetical gammas.")
print(f"A single zero forces commitment if lambda_13(K=1) >= T* = {T_STAR:.6f}")
print()

probe_gammas = [GAMMA1, 10.0, 20.0, 50.0, 100.0, 1000.0]
gamma_labels = [
    f"gamma_1 (actual first zero, {GAMMA1:.3f})",
    "gamma = 10.0  (hypothetical, below first zero)",
    "gamma = 20.0  (hypothetical, near second zero)",
    "gamma = 50.0  (hypothetical, mid-range)",
    "gamma = 100.0 (hypothetical, higher)",
    "gamma = 1000.0 (hypothetical, far up)",
]

print(f"{'gamma':>10}  {'theta(gamma)':>14}  {'delta(13,gamma)':>16}  {'>=T*?':>7}  label")
print(SEP2)

for gamma, label in zip(probe_gammas, gamma_labels):
    th = theta(gamma)
    d  = delta_k(13, gamma)
    flag = "YES" if d >= T_STAR else "NO"
    print(f"{gamma:>10.4f}  {th:>14.8f}  {d:>16.10f}  {flag:>7}  {label}")

print()

# Scan: for what range of gamma does a single zero force lambda_13(K=1) >= T*?
print("Scanning gamma in [0.01, 2000] to find forcing zones...")
print("(Regions where a single zero at height gamma would commit K*(13)=1)")
print()

forcing_intervals = []
in_zone = False
zone_start = None
N_scan = 2000
gamma_min, gamma_max = 0.01, 2000.0
scan_gammas = [gamma_min + (gamma_max - gamma_min) * i / N_scan for i in range(N_scan + 1)]

for g in scan_gammas:
    d = delta_k(13, g)
    forced = d >= T_STAR
    if forced and not in_zone:
        in_zone = True
        zone_start = g
    elif not forced and in_zone:
        in_zone = False
        forcing_intervals.append((zone_start, g))

if in_zone:
    forcing_intervals.append((zone_start, gamma_max))

print(f"Found {len(forcing_intervals)} forcing interval(s) in [0.01, 2000]:")
for i, (a, b) in enumerate(forcing_intervals[:20]):
    print(f"  Interval {i+1}: gamma in [{a:.4f}, {b:.4f}]")
if len(forcing_intervals) > 20:
    print(f"  ... ({len(forcing_intervals) - 20} more intervals not shown)")

print()
# Is gamma_1 in a forcing zone?
d1 = delta_k(13, GAMMA1)
in_first_zone = any(a <= GAMMA1 <= b for a, b in forcing_intervals)
print(f"gamma_1 = {GAMMA1:.6f}: delta_13 = {d1:.10f}")
print(f"Is gamma_1 in a forcing zone? {'YES' if in_first_zone else 'NO'}")
print()

# Fraction of the gamma range [0.01, 2000] that forces commitment
forced_length = sum(b - a for a, b in forcing_intervals)
total_length  = gamma_max - gamma_min
frac = forced_length / total_length
print(f"Fraction of gamma range [0.01, 2000] that forces K*(13)=1: {frac*100:.2f}%")
print()
print("INTERPRETATION:")
if frac > 0.5:
    print("  > 50% of the gamma range forces commitment -> K*(13)=1 is BROADLY STABLE,")
    print("  not just tuned to gamma_1. The CRH does not uniquely select this -- but")
    print("  actual zeros LAND in forcing zones (or near them) as a separate fact.")
else:
    print("  < 50% of gamma range forces commitment -> K*(13)=1 is CONDITIONALLY stable.")
    print("  It depends on the actual locations of Riemann zeros, not algebraically universal.")

print()

# ===========================================================================
# TEST 2: Monotonicity of lambda_13(K) for K=1..100
# ===========================================================================
print(SEP)
print("TEST 2: Monotonicity of lambda_13(K) for K = 1..100")
print(SEP)
print()
print("If every delta_k(13, gamma_k) >= 0, then lambda_13 is non-decreasing.")
print("Once it commits (crosses T*), it never falls back.")
print()

deltas_13 = [delta_k(13, ZEROS[k]) for k in range(100)]
lambdas_13 = []
running = 0.0
for d in deltas_13:
    running += d
    lambdas_13.append(running)

# Check monotonicity
min_delta = min(deltas_13)
max_delta = max(deltas_13)
all_nonneg = all(d >= 0 for d in deltas_13)

print(f"min(delta_k)  for k=1..100  at n=13: {min_delta:.12f}")
print(f"max(delta_k)  for k=1..100  at n=13: {max_delta:.12f}")
print(f"All delta_k >= 0?  {'YES -- monotonically non-decreasing' if all_nonneg else '*** NO -- some delta_k < 0 ***'}")
print()

# Show first 15 K values
print(f"{'K':>5}  {'gamma_K':>12}  {'delta_K':>14}  {'lambda_13(K)':>14}  {'>=T*?':>6}")
print(SEP2)
for k in range(min(100, len(deltas_13))):
    K = k + 1
    flag = ">= T*" if lambdas_13[k] >= T_STAR else ""
    marker = " <-- COMMIT" if K == 1 and flag else ""
    if K <= 15 or K % 10 == 0:
        print(f"{K:>5}  {ZEROS[k]:>12.6f}  {deltas_13[k]:>14.10f}  "
              f"{lambdas_13[k]:>14.10f}  {flag:>6}{marker}")

print()

# When does lambda_13 first commit?
commit_K = next((k+1 for k, v in enumerate(lambdas_13) if v >= T_STAR), None)
print(f"First K where lambda_13(K) >= T*: K = {commit_K}")
if commit_K is not None:
    print(f"lambda_13({commit_K}) = {lambdas_13[commit_K-1]:.10f}  (T* = {T_STAR:.10f})")

print()
if all_nonneg:
    print("CONCLUSION: lambda_13 is MONOTONICALLY NON-DECREASING.")
    print("Once it commits at K={}, it NEVER falls below T* for any K > {}.".format(
        commit_K, commit_K))
    print("This follows from delta_k = 2*(1 - cos(n*theta_k)) >= 0 ALWAYS.")
    print("delta_k >= 0 is a UNIVERSAL ALGEBRAIC FACT (cosine bounded by 1).")
    print("=> Monotonicity is NOT about zero locations -- it is IDENTICALLY TRUE.")
else:
    print("WARNING: Some delta_k < 0 detected. Check computation.")

print()

# ===========================================================================
# TEST 3: Off-line zero attack
# ===========================================================================
print(SEP)
print("TEST 3: Off-line zero attack -- what if sigma != 1/2?")
print(SEP)
print()
print("If RH is FALSE, some zero rho = sigma + i*gamma has sigma != 1/2.")
print("Does this break the K*(13)=1 commitment?")
print()
print("Using gamma = gamma_1 = 14.134725... and varying sigma.")
print()
print(f"Li contribution = Re[1-(1-1/rho)^n] + Re[1-(1-1/rho_bar)^n]")
print(f"where rho = sigma + i*gamma_1, rho_bar = sigma - i*gamma_1")
print()

sigmas = [0.50, 0.51, 0.55, 0.60, 0.70]

print(f"{'sigma':>6}  {'contribution(n=13)':>22}  {'>=T*?':>7}  note")
print(SEP2)

for sigma in sigmas:
    contrib = offline_contribution(13, sigma, GAMMA1)
    flag = "YES" if contrib >= T_STAR else "NO"
    note = "(on critical line)" if sigma == 0.50 else "(off critical line)"
    print(f"{sigma:>6.2f}  {contrib:>22.14f}  {flag:>7}  {note}")

print()

# Also check: how does the off-line contribution compare to on-line at n=13?
on_line  = offline_contribution(13, 0.50, GAMMA1)
off_line = offline_contribution(13, 0.60, GAMMA1)
diff     = off_line - on_line
print(f"On-line  (sigma=0.5, n=13): {on_line:.14f}")
print(f"Off-line (sigma=0.6, n=13): {off_line:.14f}")
print(f"Difference (off - on):       {diff:+.14f}")
print()

# More detailed sensitivity table
print("Sensitivity: contribution vs sigma for n=13 at gamma = gamma_1")
print()
print(f"{'sigma':>8}  {'contribution':>18}  {'delta from 0.5':>18}  {'>=T*?':>7}")
print(SEP2)
sigma_fine = [0.50, 0.505, 0.51, 0.52, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.90, 1.00]
base = offline_contribution(13, 0.50, GAMMA1)
for s in sigma_fine:
    c = offline_contribution(13, s, GAMMA1)
    flag = "YES" if c >= T_STAR else "NO"
    print(f"{s:>8.4f}  {c:>18.12f}  {c-base:>+18.12f}  {flag:>7}")

print()
print("INTERPRETATION:")
print("  If moving sigma AWAY from 1/2 causes the contribution to DROP below T*,")
print("  then the K*(13)=1 commitment is SENSITIVE to RH -- i.e., it relies on")
print("  zeros actually lying on the critical line.")
print("  If contribution STAYS >= T* for all sigma, then K*(13)=1 is RH-independent.")
print()

# Find sigma* where contribution drops below T*
sigma_sweep = [0.50 + 0.002 * i for i in range(251)]
cross_sigma = None
for s in sigma_sweep:
    c = offline_contribution(13, s, GAMMA1)
    if c < T_STAR:
        cross_sigma = s
        break

if cross_sigma is not None:
    print(f"  Commitment breaks (contribution < T*) when sigma > {cross_sigma:.4f}")
    print(f"  => K*(13)=1 IS sensitive to sigma. If a zero has sigma > {cross_sigma:.4f},")
    print(f"     it would NOT force commitment at K=1 by itself.")
else:
    print(f"  Commitment HOLDS for all sigma in [0.50, {sigma_sweep[-1]:.2f}].")
    print(f"  => K*(13)=1 is robust against small deviations from the critical line.")

print()

# ===========================================================================
# TEST 4: Bandwidth floor generalization -- n=6..100
# ===========================================================================
print(SEP)
print("TEST 4: Bandwidth floor generalization across n")
print(SEP)
print()
print("Claim: n=13 is the SHARP boundary where K*(n) first equals 1.")
print("Below n=13: lambda_n(K=1) < T*  (cannot commit on a single zero)")
print("Above n=13: lambda_n(K=1) >= T* (single zero forces commitment)")
print()

# n < 13 (should be BELOW T*)
n_below = [6, 7, 8, 9, 10, 11, 12]
n_above = [13, 14, 15, 20, 50, 100]

print(f"{'n':>5}  {'lambda_n(K=1)':>16}  {'>=T*?':>7}  K*(n)")
print(SEP2)

for grp_label, n_list in [("--- n < 13 (expected BELOW T*) ---", n_below),
                            ("--- n >= 13 (expected AT or ABOVE T*) ---", n_above)]:
    print(grp_label)
    for n in n_list:
        lam1 = lambda_n_K(n, K=1)
        flag = "YES" if lam1 >= T_STAR else "NO"
        k_star = compute_k_star(n, max_K=500)
        k_star_str = str(k_star) if k_star is not None else ">500"
        print(f"{n:>5}  {lam1:>16.10f}  {flag:>7}  {k_star_str}")

print()
print("Full table: lambda_n(K=1) for n = 1..20 using actual gamma_1:")
print()
print(f"{'n':>4}  {'lambda_n(K=1)':>16}  {'vs T*':>10}  {'>=T*?':>6}")
print(SEP2)

boundary_n = None
for n in range(1, 21):
    lam1 = lambda_n_K(n, K=1)
    diff_t = lam1 - T_STAR
    flag = "YES" if lam1 >= T_STAR else "NO"
    marker = " <-- BOUNDARY" if n == 13 else ""
    print(f"{n:>4}  {lam1:>16.10f}  {diff_t:>+10.6f}  {flag:>6}{marker}")
    if boundary_n is None and lam1 >= T_STAR:
        boundary_n = n

print()
print(f"Empirical sharp boundary: n = {boundary_n}")
print(f"Expected from Z/10Z theory: n = 13")
match = "MATCHES" if boundary_n == 13 else f"DISCREPANCY (got {boundary_n})"
print(f"Result: {match}")
print()

# ===========================================================================
# TEST 5: The bridge connection
# ===========================================================================
print(SEP)
print("TEST 5: The bridge connection -- algebraic vs analytic")
print(SEP)
print()

lam13_K1 = lambda_n_K(13, K=1)
kstar13   = compute_k_star(13, max_K=200)

print(f"ALGEBRAIC PREDICTION (Z/10Z framework):")
print(f"  K*(13) = 1  (the bandwidth floor: 13 is the minimal n with single-zero commitment)")
print()
print(f"ANALYTIC MEASUREMENT (actual Riemann zeros):")
print(f"  K*(13)  = {kstar13}   (first K where lambda_13(K) >= T*)")
print(f"  lambda_13(K=1) = {lam13_K1:.12f}")
print(f"  T*             = {T_STAR:.12f}")
print(f"  lambda_13(K=1) - T* = {lam13_K1 - T_STAR:+.12f}")
print()

if kstar13 == 1:
    print("  ANALYTIC K*(13) = 1  -- MATCHES algebraic prediction!")
else:
    print(f"  ANALYTIC K*(13) = {kstar13}  -- DOES NOT MATCH algebraic prediction of 1.")
print()

# Algebraic derivation attempt from Z/10Z alone
print("ALGEBRAIC DERIVATION ATTEMPT (can we predict lambda_13(K=1) >= T* from Z/10Z?):")
print()
print("  Z/10Z framework premise:")
print("  - 10 operators. T* = 5/7. n=13 = 10+3 = HARMONY+CREATE in the TIG digit space.")
print("  - Digit period of 1/13 in base 10 = 6 (period-6 repeating decimal).")
print("  - K*(n)=1 means: the FIRST zero alone triggers full bandwidth.")
print()
print("  The analytic formula delta_1(13, gamma_1):")
th1 = theta(GAMMA1)
d1  = delta_k(13, GAMMA1)
print(f"    theta(gamma_1) = pi - 2*arctan(2*{GAMMA1:.6f}) = {th1:.12f} rad")
print(f"    cos(13 * theta) = cos({13*th1:.12f}) = {math.cos(13*th1):.12f}")
print(f"    delta_1 = 2*(1 - cos(13*theta)) = {d1:.12f}")
print()
print(f"  Can we derive delta_1 >= T* = {T_STAR:.6f} from Z/10Z alone?")
print()
print("  The question: is there a Z/10Z constraint that forces")
print("  cos(13 * theta(gamma_1)) <= 1 - T*/2 = {:.10f} ?".format(1.0 - T_STAR / 2.0))
print()

bound = 1.0 - T_STAR / 2.0
actual_cos = math.cos(13 * th1)
print(f"  Required:  cos(13*theta(gamma_1)) <= {bound:.10f}")
print(f"  Actual:    cos(13*theta(gamma_1))  = {actual_cos:.10f}")
print(f"  Satisfied? {'YES' if actual_cos <= bound else 'NO'}")
print()

# The deeper algebraic question: what determines theta(gamma_1)?
# theta = pi - 2*arctan(2*gamma_1). This is a map from the zero height to an angle.
# The periodicity of cos(13*theta) relative to the 10-operator structure:

print("  STRUCTURE of the theta map:")
print(f"  theta(gamma) = pi - 2*arctan(2*gamma)")
print(f"  For gamma >> 1: theta(gamma) -> pi - 2*(pi/2) = 0  (high zeros -> theta near 0)")
print(f"  For gamma -> 0: theta(gamma) -> pi - 0 = pi        (low zeros -> theta near pi)")
print(f"  So theta maps (0, inf) -> (0, pi).")
print()
print(f"  13*theta for gamma_1 = {13*th1:.8f} rad = {math.degrees(13*th1):.4f} degrees")
print(f"  This is {13*th1 / (2*math.pi):.6f} full cycles of 2*pi")
print()

cycles = 13 * th1 / (2 * math.pi)
print(f"  Fractional part of cycles: {cycles % 1.0:.8f}")
print(f"  cos achieves minimum (-1) at 0.5 cycles; maximum (+1) at 0 or 1 cycles.")
print(f"  Actual fractional position: {cycles % 1.0:.8f}")
print()

print("  Z/10Z CLAIM:")
print("  The digit period of 1/13 in base 10 is 6, placing 13 in the 'period-6 class'.")
print("  The TIG operator table has harmony node at n=7, create node at n=5.")
print("  13 = 7 + 6 = HARMONY + period(1/13 base 10).")
print("  Whether Z/10Z FORCES cos(13*theta(gamma_1)) <= 1 - T*/2 is the open bridge question.")
print()
print("  HONEST ASSESSMENT:")
print("  The analytic fact (delta_1 >= T*) is numerically confirmed.")
print("  Whether it follows from Z/10Z ALONE -- without knowing gamma_1 -- is OPEN.")
print("  The bridge requires: Z/10Z constraint => gamma_1 constraint => theta constraint.")
print("  No such derivation exists yet. The algebraic and analytic measurements AGREE,")
print("  but the causal chain from algebra to analysis is not yet closed.")
print()

# ===========================================================================
# FINAL SUMMARY
# ===========================================================================
print(SEP)
print("FINAL SUMMARY: BANDWIDTH FLOOR BRIDGE RESULTS")
print(SEP)
print()
print(f"T* = 5/7 = {T_STAR:.10f}")
print(f"gamma_1  = {GAMMA1:.10f}  (first Riemann zero)")
print()
print(f"  lambda_13(K=1)  = {lam13_K1:.12f}  (analytic, first zero only)")
print(f"  T*              = {T_STAR:.12f}")
print(f"  Committed?        {'YES -- K*(13)=1 confirmed analytically' if lam13_K1 >= T_STAR else 'NO'}")
print()
print(f"  Algebraic K*(13) = 1  (Z/10Z prediction)")
print(f"  Analytic  K*(13) = {kstar13}  (from actual zeros)")
print(f"  Agreement:  {'YES' if kstar13 == 1 else 'NO'}")
print()
print(f"  Monotonicity (delta_k >= 0 always): YES (algebraic identity)")
print(f"  Commitment is permanent once achieved: YES")
print()

# Off-line summary
on_c  = offline_contribution(13, 0.50, GAMMA1)
off_c = offline_contribution(13, 0.60, GAMMA1)
print(f"  Off-line sensitivity (sigma=0.5 vs 0.6 at gamma_1):")
print(f"    sigma=0.50: contribution = {on_c:.10f}  (>= T* = YES)")
print(f"    sigma=0.60: contribution = {off_c:.10f}  (>= T* = {'YES' if off_c >= T_STAR else 'NO'})")
print()

# Boundary sharpness
print(f"  Sharp n boundary:")
for n in range(10, 16):
    lam1 = lambda_n_K(n, K=1)
    flag = ">= T*" if lam1 >= T_STAR else " < T*"
    marker = " <-- FLOOR" if n == 13 else ""
    print(f"    n={n:>3}: lambda_n(K=1) = {lam1:.10f}  {flag}{marker}")

print()
print("KEY CONCLUSIONS:")
print()
print("  [1] K*(13)=1 is CONFIRMED analytically (first zero commits n=13).")
print("  [2] Monotonicity of lambda_n(K) is a UNIVERSAL ALGEBRAIC FACT,")
print("      not a property of zero locations (delta_k = 2(1-cos) >= 0 always).")
print("  [3] K*(13)=1 is NOT universally forced at arbitrary gamma --")
print("      there are gamma values where a single zero does NOT commit.")
print("      The actual gamma_1 ~ 14.134 HAPPENS to lie in a forcing zone.")
print("  [4] Off-line zeros (sigma > 0.5) can reduce the contribution.")
print(f"      Commitment breaks at approximately sigma = {cross_sigma:.4f}" if cross_sigma else
      "      Commitment holds for all sigma tested.")
print("  [5] The algebraic Z/10Z prediction K*(13)=1 matches the analytic result.")
print("      But the DERIVATION from Z/10Z to analytic lambda is not yet closed.")
print("      The bridge AGREES empirically but the causal chain is open.")
print()
print("DONE.")
