#!/usr/bin/env sage
"""
Full Prym pipeline for the canonical triple (sqrt(2), sqrt(3), sqrt(5)).
Run with SageMath >= 9.5.
"""

from sage.all import *

print("=" * 70)
print("CANONICAL TRIPLE: (sqrt(2), sqrt(3), sqrt(5))")
print("=" * 70)

# Work over the number field Q(sqrt(2), sqrt(3), sqrt(5))
# Construct as tower: Q(sqrt(2))(sqrt(3))(sqrt(5)) then flatten

K1.<s2> = NumberField(x^2 - 2)
K2.<s3> = K1.extension(x^2 - 3)
K3.<s5> = K2.extension(x^2 - 5)
K.<a> = K3.absolute_field()
# a generates K over Q; identify s2, s3, s5 in K
to_K = K3.structure()[1]
S2 = to_K(s2)
S3 = to_K(s3)
S5 = to_K(s5)

print(f"\nWorking in K = Q(a) of degree {K.degree()}")
print(f"sqrt(2) = {S2}")
print(f"sqrt(3) = {S3}")
print(f"sqrt(5) = {S5}")

# Curve equation
R.<x> = PolynomialRing(K)
lam, mu, nu = S2, S3, S5
f = x * (x - 1) * (x - lam)^3 * (x - mu)^2 * (x - nu)^2
print(f"\nf has degree {f.degree()}")

# ============================================================
# Build curve
# ============================================================

R2.<xx, yy> = PolynomialRing(K, 2)
# Substitute x -> xx in f
f_xx = sum(f.monomial_coefficient(x^i) * xx^i for i in range(f.degree() + 1))
F = yy^4 - f_xx
print(f"\nCurve equation: y^4 = f(x)")

# Construct affine curve
try:
    C = Curve(F, AffineSpace(2, K))
    print(f"Curve constructed over K. Genus: {C.genus()}")
    assert C.genus() == 5
except Exception as e:
    print(f"Curve construction issue: {e}")

# ============================================================
# Riemann surface - this is the main work
# ============================================================

# SageMath's RiemannSurface usually works over CC or QQ.
# For number-field curves, may need to specialize to a specific embedding of K.

# Pick the all-positive embedding: sqrt(2), sqrt(3), sqrt(5) -> positive reals
phi = K.complex_embeddings()[0]
for ph in K.complex_embeddings():
    # Find the one where sqrt(2), sqrt(3), sqrt(5) all go to positive reals
    if ph(S2).real() > 0 and ph(S3).real() > 0 and ph(S5).real() > 0 \
       and abs(ph(S2).imag()) < 1e-10:
        phi = ph
        break

print(f"\nUsing embedding: sqrt(2) -> {phi(S2):.6f}, sqrt(3) -> {phi(S3):.6f}, sqrt(5) -> {phi(S5):.6f}")

# Convert f to C[x] via phi
f_CC = CC['x']([phi(c) for c in f.coefficients(sparse=False)])
print(f"f over CC (first few coefficients): {f_CC}")

# Now build the Riemann surface
try:
    from sage.schemes.riemann_surfaces.riemann_surface import RiemannSurface
    F_CC = yy^4 - f_CC.subs(x=xx)
    # This may need to be adapted based on SageMath version
    RS = RiemannSurface(F_CC, prec=300)  # 300 bits ~ 90 decimal digits
    print(f"Riemann surface constructed. Genus: {RS.genus}")
    
    print("\nComputing period matrix...")
    PM = RS.period_matrix()
    print(f"Period matrix: {PM.nrows()} x {PM.ncols()}")
    
    # Save to file for further analysis
    with open('canonical_period_matrix.txt', 'w') as ff:
        ff.write(str(PM.numerical_approx(60)))
    print("Period matrix saved to canonical_period_matrix.txt")
    
except Exception as e:
    print(f"Riemann surface construction failed: {e}")
    print("The Sage RiemannSurface class may not handle this specific curve structure.")
    print("Alternative: use PARI/GP's periods for hyperelliptic approximation, or")
    print("implement Molin-Neurohr directly for y^n = f(x).")

# ============================================================
# Psi-action, Prym projection, End^0, Hodge field, det(Y)
# ============================================================

print("""
============================================================
CANONICAL TRIPLE: EXPECTED OUTPUTS FROM FULL PIPELINE
============================================================

1. Period matrix Omega: 5 x 10 complex matrix.
2. iota-action on H_1: order-2 automorphism with specific eigenvalue pattern.
3. Prym = iota-anti-invariant sublattice: 4 x 8 matrix.
4. Psi-action on Prym H^{1,0}: eigenvalues (+i, +i, -i, -i).
   -> Weil signature = (2, 2). (Structurally guaranteed.)
5. End^0(Prym): 
   - Expected: Q(i) exactly.
   - Alternative: quartic CM field containing Q(i) if canonical sits on specialization.
6. Hodge field:
   - Expected: Q(i, sqrt(2), sqrt(3), sqrt(5)), degree 16.
   - Key test: PSLQ on specific Weil-type Hodge class period.
   - If smaller: canonical doesn't activate full field (unlikely given parameter positions).
   - If larger: accidental algebraic relation producing extraneous radicals.
7. det(Y):
   - Target: 2086 + 462*sqrt(15) + 498*sqrt(10) + 730*sqrt(6)
   - If Hodge field matches but det differs: canonical is in correct subspace 
     but at wrong point; try nearby admissible parameters.
   - If Hodge field wrong: lane may be dead.

DECISION TREE:
  All of 1-5 as expected, 6 matches, 7 matches target: FOUND.
  All of 1-5 as expected, 6 matches, 7 wrong value: canonical not final answer;
    try T4.4 (1+sqrt(2), 1+sqrt(3), 1+sqrt(5)), T5.1 (sqrt(6), sqrt(10), sqrt(15)).
  6 fails: bounce back to ClaudeChat for family rethink.
""")
