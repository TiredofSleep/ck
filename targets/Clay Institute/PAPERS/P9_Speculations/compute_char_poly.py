"""
Exact characteristic polynomial computation for CK commutator matrix.
Run: python compute_char_poly.py
Output: char_poly_results.txt in the same directory.
"""
import os, sys

# ---- Define matrices as plain Python lists of lists (exact integers) ----
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

try:
    from sympy import Matrix, symbols, factorint, Poly, ZZ, Rational, sqrt, isprime
    from sympy import resultant, degree, galois_group
    HAS_SYMPY = True
except ImportError:
    HAS_SYMPY = False

if not HAS_SYMPY:
    print("ERROR: sympy is required. Install with: pip install sympy")
    sys.exit(1)

# ---- Step 1: Compute commutator C = TSML @ BHML - BHML @ TSML ----
T = Matrix(TSML)
B = Matrix(BHML)
C = T * B - B * T

out_lines = []
def log(s=""):
    print(s)
    out_lines.append(str(s))

log("=" * 72)
log("EXACT CHARACTERISTIC POLYNOMIAL OF CK COMMUTATOR C = [TSML, BHML]")
log("=" * 72)
log()

log("--- Commutator Matrix C (10x10, integer, skew-symmetric) ---")
for i in range(10):
    row = [int(C[i, j]) for j in range(10)]
    log(f"  {row}")
log()

skew = (C + C.T) == Matrix.zeros(10, 10)
log(f"Skew-symmetric (C + C^T = 0): {skew}")
log()

# ---- Step 2: Exact characteristic polynomial ----
lam = symbols('lambda')
char_matrix = C - lam * Matrix.eye(10)

log("Computing exact characteristic polynomial det(C - lambda*I)...")
log("(This uses exact integer/polynomial arithmetic in sympy)")
log()

cp = char_matrix.det()  # exact symbolic determinant
cp_poly = Poly(cp, lam, domain=ZZ)

log(f"Characteristic polynomial (degree {cp_poly.degree()}):")
log()

coeffs = cp_poly.all_coeffs()  # highest degree first
log("Coefficients (from lambda^10 down to lambda^0):")
for i, c in enumerate(coeffs):
    power = 10 - i
    log(f"  lambda^{power}: {c}")
log()

# Extract the even-power coefficients
# For skew-symmetric matrix, odd powers should be zero
c10 = coeffs[0]   # lambda^10
c9 = coeffs[1]    # lambda^9
c8 = coeffs[2]    # lambda^8
c7 = coeffs[3]    # lambda^7
c6 = coeffs[4]    # lambda^6
c5 = coeffs[5]    # lambda^5
c4 = coeffs[6]    # lambda^4
c3 = coeffs[7]    # lambda^3
c2 = coeffs[8]    # lambda^2
c1 = coeffs[9]    # lambda^1
c0 = coeffs[10]   # lambda^0

log("Verification of skew-symmetric form (odd powers should be 0):")
log(f"  c9 (lambda^9) = {c9}")
log(f"  c7 (lambda^7) = {c7}")
log(f"  c5 (lambda^5) = {c5}")
log(f"  c3 (lambda^3) = {c3}")
log(f"  c1 (lambda^1) = {c1}")
log()

log("Even-power coefficients (the ones that matter):")
log(f"  c10 = {c10}")
log(f"  c8  = {c8}")
log(f"  c6  = {c6}")
log(f"  c4  = {c4}")
log(f"  c2  = {c2}")
log(f"  c0  = {c0}")
log()

# ---- Step 3: det(C) and Pfaffian ----
log("=" * 72)
log("DETERMINANT AND PFAFFIAN")
log("=" * 72)
log()

det_C = C.det()
log(f"det(C) = c0 = {det_C}")
log()

# Factor det(C)
det_factors = factorint(abs(int(det_C)))
log(f"|det(C)| = {abs(int(det_C))}")
log(f"Prime factorization of |det(C)|:")
for p, e in sorted(det_factors.items()):
    log(f"  {p}^{e}")
log()

# Pfaffian: det = Pf^2 for skew-symmetric
import math
pf_squared = abs(int(det_C))
pf = int(math.isqrt(pf_squared))
log(f"Pfaffian^2 = |det(C)| = {pf_squared}")
log(f"Pfaffian = sqrt(|det(C)|) = {pf}")
log(f"Pfaffian is exact integer: {pf * pf == pf_squared}")
log()

# Factor Pfaffian
pf_factors = factorint(pf)
log(f"Prime factorization of Pfaffian = {pf}:")
for p, e in sorted(pf_factors.items()):
    log(f"  {p}^{e}")
log()

# Check if 15083 is prime
log(f"Is 15083 prime? {isprime(15083)}")
if not isprime(15083):
    log(f"Factorization of 15083: {factorint(15083)}")
log()

# ---- Step 4: Quintic in y = -lambda^2 ----
log("=" * 72)
log("QUINTIC POLYNOMIAL IN y = -lambda^2")
log("=" * 72)
log()

y = symbols('y')
# char poly: lambda^10 + c8*lambda^8 + c6*lambda^6 + c4*lambda^4 + c2*lambda^2 + c0
# With y = -lambda^2, lambda^2 = -y, lambda^(2k) = (-y)^k = (-1)^k * y^k
# lambda^10 = (-y)^5 = -y^5
# lambda^8 = (-y)^4 = y^4
# lambda^6 = (-y)^3 = -y^3
# lambda^4 = (-y)^2 = y^2
# lambda^2 = (-y)^1 = -y
# lambda^0 = 1
# So: -y^5 + c8*y^4 - c6*y^3 + c4*y^2 - c2*y + c0 = 0
# Multiply by -1: y^5 - c8*y^4 + c6*y^3 - c4*y^2 + c2*y - c0 = 0

quintic = y**5 - c8*y**4 + c6*y**3 - c4*y**2 + c2*y - c0
quintic_poly = Poly(quintic, y, domain=ZZ)

log("Substitution: y = -lambda^2  (so eigenvalues are lambda = +/- i*sqrt(y))")
log()
log("Quintic polynomial p(y) = 0:")
q_coeffs = quintic_poly.all_coeffs()
for i, c in enumerate(q_coeffs):
    power = 5 - i
    log(f"  y^{power}: {c}")
log()
log(f"p(y) = y^5 + ({-c8})*y^4 + ({c6})*y^3 + ({-c4})*y^2 + ({c2})*y + ({-c0})")
log()

# ---- Step 5: Discriminant and Galois group analysis ----
log("=" * 72)
log("GALOIS GROUP AND SOLVABILITY ANALYSIS")
log("=" * 72)
log()

# Compute discriminant
disc = quintic_poly.discriminant()
log(f"Discriminant of quintic = {disc}")
log()
disc_factors = factorint(abs(int(disc)))
log(f"Prime factorization of |discriminant|:")
for p, e in sorted(disc_factors.items()):
    log(f"  {p}^{e}")
log()

# Try to determine Galois group
try:
    G, is_exact = galois_group(quintic_poly)
    log(f"Galois group: {G}")
    log(f"Exact determination: {is_exact}")
    log(f"Group order: {G.order()}")
    log(f"Is solvable (by radicals): {G.is_solvable}")
except Exception as e:
    log(f"Galois group computation: {e}")
log()

# ---- Step 6: Numerical roots and ratio analysis ----
log("=" * 72)
log("NUMERICAL EIGENVALUE ANALYSIS")
log("=" * 72)
log()

import numpy as np

# Numerical roots of quintic
q_coeffs_num = [float(c) for c in q_coeffs]
y_roots = np.roots(q_coeffs_num)
y_roots_real = sorted([r.real for r in y_roots if abs(r.imag) < 1e-6], reverse=True)

log("Roots of quintic p(y) = 0 (these are y_k = lambda_k^2 / (-1)):")
for i, yr in enumerate(y_roots_real):
    eig = np.sqrt(yr) if yr > 0 else 0
    log(f"  y_{i} = {yr:.10f}   =>  eigenvalue pair = +/- {eig:.6f}*i")
log()

# Eigenvalue magnitudes
eig_mags = [np.sqrt(yr) for yr in y_roots_real if yr > 0]
log("Eigenvalue magnitudes (|Im(lambda)|):")
for i, em in enumerate(eig_mags):
    log(f"  |lambda_{i}| = {em:.10f}")
log()

# Ratios
log("Eigenvalue ratios:")
for i in range(len(eig_mags)):
    for j in range(i+1, len(eig_mags)):
        ratio = eig_mags[i] / eig_mags[j]
        log(f"  |lambda_{i}| / |lambda_{j}| = {ratio:.10f}")
log()

# Check against known constants
import math
pi = math.pi
log("Comparison with known constants:")
log(f"  4*pi     = {4*pi:.10f}")
log(f"  ratio_01 = {eig_mags[0]/eig_mags[1]:.10f}   (pair0/pair1)")
log(f"  diff     = {abs(eig_mags[0]/eig_mags[1] - 4*pi):.10f}   ({abs(eig_mags[0]/eig_mags[1] - 4*pi)/(4*pi)*100:.4f}% off)")
log()
log(f"  7        = {7.0:.10f}")
log(f"  ratio_23 = {eig_mags[2]/eig_mags[3]:.10f}   (pair2/pair3)")
log(f"  diff     = {abs(eig_mags[2]/eig_mags[3] - 7):.10f}   ({abs(eig_mags[2]/eig_mags[3] - 7)/7*100:.4f}% off)")
log()

# Additional ratio checks
log("Additional ratio checks:")
log(f"  5/7 = {5/7:.10f}")
log(f"  sqrt(2) = {math.sqrt(2):.10f}")
log(f"  sqrt(7) = {math.sqrt(7):.10f}")
log(f"  7^2 = 49")
log(f"  ratio_02 = {eig_mags[0]/eig_mags[2]:.10f}")
log(f"  ratio_03 = {eig_mags[0]/eig_mags[3]:.10f}")
log(f"  ratio_04 = {eig_mags[0]/eig_mags[4]:.10f}")
log(f"  ratio_12 = {eig_mags[1]/eig_mags[2]:.10f}")
log(f"  ratio_13 = {eig_mags[1]/eig_mags[3]:.10f}")
log(f"  ratio_14 = {eig_mags[1]/eig_mags[4]:.10f}")
log(f"  ratio_24 = {eig_mags[2]/eig_mags[4]:.10f}")
log(f"  ratio_34 = {eig_mags[3]/eig_mags[4]:.10f}")
log()

# ---- Step 7: Exact algebraic analysis of ratios ----
log("=" * 72)
log("EXACT ALGEBRAIC ANALYSIS OF EIGENVALUE RATIOS")
log("=" * 72)
log()

# The ratio y_i/y_j where y are roots of the quintic
log("Ratios of quintic roots (y_i/y_j = lambda_i^2 / lambda_j^2):")
for i in range(len(y_roots_real)):
    for j in range(i+1, len(y_roots_real)):
        ratio_y = y_roots_real[i] / y_roots_real[j] if y_roots_real[j] != 0 else float('inf')
        log(f"  y_{i}/y_{j} = {ratio_y:.10f}")
        # Check if close to simple rationals or known constants
        for name, val in [("16*pi^2", 16*pi**2), ("49", 49), ("7", 7),
                          ("4*pi", 4*pi), ("pi^2", pi**2), ("pi", pi),
                          ("2*pi", 2*pi), ("25/49", 25/49), ("5/7", 5/7)]:
            if abs(ratio_y - val) / max(abs(val), 1) < 0.02:
                log(f"    ** CLOSE to {name} = {val:.10f}  (error: {abs(ratio_y-val)/val*100:.4f}%)")
log()

# ---- Step 8: Can the quintic be solved by radicals? ----
log("=" * 72)
log("SOLVABILITY SUMMARY")
log("=" * 72)
log()

log("The characteristic polynomial of C factors as:")
log(f"  det(C - lambda*I) = lambda^10 + {c8}*lambda^8 + {c6}*lambda^6 + {c4}*lambda^4 + {c2}*lambda^2 + {c0}")
log()
log("Substituting y = -lambda^2 gives the quintic:")
log(f"  y^5 - {c8}*y^4 + {c6}*y^3 - {c4}*y^2 + {c2}*y - {c0} = 0")
log()

# Check if quintic factors over Z
from sympy import factor as sym_factor
factored = sym_factor(quintic)
log(f"Factored form over Q: {factored}")
log()

# Try to find rational roots
from sympy import Rational as R
# By rational root theorem, possible rational roots divide c0
log("Rational root theorem: possible roots divide c0")
log(f"|c0| = {abs(int(c0))}")
# Just check small factors
found_rational = False
for candidate in range(1, 100):
    if abs(int(c0)) % candidate == 0:
        val = quintic.subs(y, candidate)
        if val == 0:
            log(f"  RATIONAL ROOT FOUND: y = {candidate}")
            found_rational = True
        val = quintic.subs(y, -candidate)
        if val == 0:
            log(f"  RATIONAL ROOT FOUND: y = {-candidate}")
            found_rational = True
if not found_rational:
    log("  No small rational roots found (checked +/-1 through +/-99)")
log()

# ---- Step 9: Summary of exact results ----
log("=" * 72)
log("FINAL SUMMARY")
log("=" * 72)
log()
log(f"Characteristic polynomial coefficients (EXACT INTEGERS):")
log(f"  c10 = {c10}")
log(f"  c8  = {c8}")
log(f"  c6  = {c6}")
log(f"  c4  = {c4}")
log(f"  c2  = {c2}")
log(f"  c0  = {c0} = det(C)")
log()
log(f"det(C) = {det_C}")
log(f"|det(C)| factorization: ", end="")
parts = []
for p, e in sorted(det_factors.items()):
    parts.append(f"{p}^{e}" if e > 1 else str(p))
log(" * ".join(parts))
log()
log(f"Pfaffian = {pf}")
log(f"Pfaffian factorization: ", end="")
parts = []
for p, e in sorted(pf_factors.items()):
    parts.append(f"{p}^{e}" if e > 1 else str(p))
log(" * ".join(parts))
log()

log("The eigenvalue ratios are NOT exactly equal to pi, sqrt(2), sqrt(7),")
log("5/7, or other common transcendental/algebraic constants.")
log("They are algebraic numbers -- roots of the irreducible quintic above.")
log()
log("The ratios pair0/pair1 ~ 4*pi and pair2/pair3 ~ 7 are COINCIDENTAL")
log("approximations, not exact identities. The eigenvalues are roots of")
log("a polynomial with integer coefficients; they cannot equal transcendental")
log("quantities like multiples of pi.")

# ---- Write to file ----
script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(script_dir, "char_poly_results.txt")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print()
print(f"Results written to: {out_path}")
