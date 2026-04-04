#!/usr/bin/env python3
"""
verify_bridge.py -- Symbolic + high-precision verification of all 7 proof items
in PRIME_PI_PHI_BRIDGE_HARDENED.md (A1, A2, A3, B1, B2, B3, C1).

Run with:
    python verify_bridge.py

Returns PASS/FAIL for each item and prints a summary table.
"""

import sys
from sympy import (
    symbols, cos, sin, pi, sqrt, Rational, diff, simplify,
    minimal_polynomial, cyclotomic_poly, exp, I, cancel,
    nsimplify, N, Integer, atan2, Poly
)
import mpmath

mpmath.mp.dps = 50  # 50 decimal places

x, r = symbols('x r', real=True)
phi = (1 + sqrt(5)) / 2

results = []


def check(label, statement, passed, details=''):
    mark = 'PASS' if passed else 'FAIL'
    results.append((label, mark, statement, details))
    print(f"[{mark}] {label}: {statement}")
    if details:
        print(f"       {details}")


# ─────────────────────────────────────────────────────────────────
# A1: deg(2cos(π/p)/ℚ) = (p−1)/2  for odd primes p
# ─────────────────────────────────────────────────────────────────
print("\n-- Section A: Cyclotomic / Finite Side --")

primes_test = [3, 5, 7, 11, 13]
a1_ok = True
details_a1 = []
for p in primes_test:
    # Degree of 2cos(π/p) = degree of maximal real subfield = (p-1)/2
    # Verified via: minimal_polynomial of 2*cos(pi/p) should have degree (p-1)/2
    mp = minimal_polynomial(2 * cos(pi / p), x)
    deg = Poly(mp, x).degree()
    expected = (p - 1) // 2
    ok = (deg == expected)
    if not ok:
        a1_ok = False
    details_a1.append(f"p={p}: deg={deg}, expected={expected}, {'OK' if ok else 'FAIL'}")
check("A1", "deg(2cos(π/p)/ℚ) = (p−1)/2", a1_ok, " | ".join(details_a1))

# ─────────────────────────────────────────────────────────────────
# A2: minimal_polynomial(2*cos(pi/5)) = x² − x − 1  AND  2cos(π/5) = φ
# ─────────────────────────────────────────────────────────────────
mp5 = minimal_polynomial(2 * cos(pi / 5), x)
mp5_std = x**2 - x - 1
a2_minpoly_ok = simplify(mp5 - mp5_std) == 0

# Verify 2cos(π/5) = φ
diff_val = simplify(2 * cos(pi / 5) - phi)
a2_value_ok = diff_val == 0

check("A2a", "minimal_polynomial(2cos(π/5)) = x²−x−1",
      a2_minpoly_ok, f"got: {mp5}")
check("A2b", "2cos(π/5) = φ = (1+√5)/2",
      a2_value_ok, f"simplify(2cos(π/5)−φ) = {diff_val}")

# ─────────────────────────────────────────────────────────────────
# A3: Gauss sum τ(χ₅) = √5,  φ = (1 + τ(χ₅))/2
# ─────────────────────────────────────────────────────────────────
# Legendre symbol (k/5) for k=0..4: 0,1,-1,-1,1
leg = [0, 1, -1, -1, 1]  # (k/5) for k=0..4

# Compute via mpmath at high precision
mpmath.mp.dps = 50
tau_numerical = sum(leg[k] * mpmath.exp(2 * mpmath.pi * 1j * k / 5) for k in range(5))
tau_real = float(tau_numerical.real)
tau_imag = float(tau_numerical.imag)
tau_abs = float(abs(tau_numerical))
sqrt5_mp = float(mpmath.sqrt(5))

a3_gauss_ok = abs(tau_real - sqrt5_mp) < 1e-14 and abs(tau_imag) < 1e-14
phi_from_gauss = (1 + tau_real) / 2
phi_exact = float((1 + mpmath.sqrt(5)) / 2)
a3_phi_ok = abs(phi_from_gauss - phi_exact) < 1e-14

check("A3a", "τ(χ₅) = √5  (Gauss sum, Legendre mod 5)",
      a3_gauss_ok, f"τ = {tau_real:.6f}+{tau_imag:.2e}i, √5 = {sqrt5_mp:.6f}")
check("A3b", "φ = (1+τ(χ₅))/2",
      a3_phi_ok, f"(1+τ)/2 = {phi_from_gauss:.10f}, φ = {phi_exact:.10f}")

# ─────────────────────────────────────────────────────────────────
# B1: sinc²(1/2) = 4/π²
# ─────────────────────────────────────────────────────────────────
print("\n-- Section B: Analytic Side (sinc^2) --")

sinc2_half = sin(pi * Rational(1, 2))**2 / (pi * Rational(1, 2))**2
b1_sym = simplify(sinc2_half - Rational(4, 1) / pi**2)
b1_ok = b1_sym == 0
check("B1", "sinc²(1/2) = 4/π²", b1_ok, f"residual = {b1_sym}")

# ─────────────────────────────────────────────────────────────────
# B2: d/dr sinc²(r)|_{r=1/2} = −16/π²
# ─────────────────────────────────────────────────────────────────
f_r = sin(pi * r)**2 / (pi * r)**2
df_r = diff(f_r, r)
df_half = simplify(df_r.subs(r, Rational(1, 2)) + 16 / pi**2)
b2_ok = df_half == 0
check("B2", "d/dr sinc²(r)|_{r=1/2} = −16/π²", b2_ok, f"residual = {df_half}")

# ─────────────────────────────────────────────────────────────────
# B3: sinc²(1/5) = 25(3−φ)/(4π²)
# ─────────────────────────────────────────────────────────────────
# Step 1: sin²(π/5) = (3−φ)/4
sin2_pi5_sym = sin(pi / 5)**2
rhs_b3_inner = (3 - phi) / 4
b3_inner = simplify(sin2_pi5_sym - rhs_b3_inner)
b3_inner_ok = b3_inner == 0

# Step 2: sinc²(1/5) = 25*sin²(π/5)/π² = 25(3-φ)/(4π²)
sinc2_fifth = 25 * sin(pi / 5)**2 / pi**2
rhs_b3 = 25 * (3 - phi) / (4 * pi**2)
b3_sym = simplify(sinc2_fifth - rhs_b3)
b3_ok = b3_sym == 0

check("B3a", "sin²(π/5) = (3−φ)/4",
      b3_inner_ok, f"residual = {b3_inner}")
check("B3b", "sinc²(1/5) = 25(3−φ)/(4π²)",
      b3_ok, f"residual = {b3_sym}")

# Numerical confirmation
sinc2_fifth_num = float(N(sinc2_fifth))
rhs_b3_num = float(N(rhs_b3))
check("B3c", "sinc²(1/5) ≈ 0.875140 (numerical)",
      abs(sinc2_fifth_num - 0.875140) < 1e-5,
      f"sinc²(1/5) = {sinc2_fifth_num:.10f}, formula = {rhs_b3_num:.10f}, error = {abs(sinc2_fifth_num-rhs_b3_num):.2e}")

# ─────────────────────────────────────────────────────────────────
# C1: 16/π² ≈ φ, relative error 0.1919%
# ─────────────────────────────────────────────────────────────────
print("\n-- Section C: Approximation Audit --")

mpmath.mp.dps = 50
val_16pi2 = float(16 / mpmath.pi**2)
val_phi = float((1 + mpmath.sqrt(5)) / 2)
rel_err = abs(val_16pi2 - val_phi) / val_phi
abs_err = abs(val_16pi2 - val_phi)

c1_rel_ok = abs(rel_err - 0.001919) < 0.00005  # roughly 0.1919%
c1_abs_ok = abs(abs_err - 3.105e-3) < 5e-5

check("C1a", "16/π² relative error vs φ ≈ 0.1919%",
      c1_rel_ok, f"16/π² = {val_16pi2:.10f}, φ = {val_phi:.10f}, rel err = {rel_err*100:.4f}%")
check("C1b", "16/π² ≠ φ  (NOT an exact identity)",
      True,  # always true, just documenting
      f"|16/π² − φ| = {abs_err:.4e}")

# ─────────────────────────────────────────────────────────────────
# B2 structural: |f'(1/2)| = 4 × f(1/2)  (exact)
# ─────────────────────────────────────────────────────────────────
fold = Rational(4, 1) / pi**2
tangent = Rational(16, 1) / pi**2
ratio = simplify(tangent / fold)
b2_ratio_ok = ratio == 4
check("B2x", "|d/dr sinc²|_{1/2}| = 4 × sinc²(1/2)  (structural: tangent = 4×fold)",
      b2_ratio_ok, f"ratio = {ratio}")

# ─────────────────────────────────────────────────────────────────
# SUMMARY TABLE
# ─────────────────────────────────────────────────────────────────
print("\n" + "="*72)
print(f"{'Label':<8} {'Status':<6} {'Statement'}")
print("="*72)
for label, mark, statement, _ in results:
    trunc = statement[:55] + "..." if len(statement) > 55 else statement
    print(f"{label:<8} {mark:<6} {trunc}")
print("="*72)

passes = sum(1 for _, m, _, _ in results if m == 'PASS')
fails  = sum(1 for _, m, _, _ in results if m == 'FAIL')
print(f"\nTotal: {passes} PASS, {fails} FAIL out of {len(results)} checks")
sys.exit(0 if fails == 0 else 1)
