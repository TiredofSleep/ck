#!/usr/bin/env sage
"""
Full Prym pipeline for the canonical triple (sqrt 2, sqrt 3, sqrt 5) — v2.

Differences from full_pipeline_canonical.sage:
  1. Builds K = Q(s2, s3, s5) via NumberField([list]) then .absolute_field() —
     avoids the broken K3.structure()[1] coercion in v1.
  2. Rebuilds K with explicit real embedding baked in, so RiemannSurface
     consumes polynomial coefficients correctly (not raw CC).
  3. Supplies the 5 holomorphic differentials explicitly, bypassing Singular's
     genus() which does not support extension fields.
  4. Targets det(Y) = Im(tau) det, compares to
        2086 + 462*sqrt(15) + 498*sqrt(10) + 730*sqrt(6)

Runtime: ~5-30 min on a modern machine at prec=200 (60 decimal digits).
Requires SageMath >= 9.5.

Usage:
    sage full_pipeline_canonical_v2.sage
"""

from sage.all import *
import time

print("=" * 70)
print("CANONICAL TRIPLE v2: (sqrt 2, sqrt 3, sqrt 5)")
print("=" * 70)

# ============================================================
# §1. Number field K = Q(sqrt 2, sqrt 3, sqrt 5)
# ============================================================

R = PolynomialRing(QQ, 't')
t = R.gen()
Krel = NumberField([t**2 - 2, t**2 - 3, t**2 - 5], names=['s2', 's3', 's5'])
s2, s3, s5 = Krel.gens()
Kabs = Krel.absolute_field('a')
a = Kabs.gen()
to_abs = Kabs.structure()[1]  # Krel -> Kabs  (this is the correct direction)
S2_abs = to_abs(s2); S3_abs = to_abs(s3); S5_abs = to_abs(s5)

print(f"\nAbs field K: {Kabs}")
print(f"deg K / Q = {Kabs.degree()}")
# Expected: degree 8 (NOT 16 — 16 is Q(i, sqrt 2, sqrt 3, sqrt 5))

# Pick the embedding sending sqrt 2, sqrt 3, sqrt 5 all to positive reals.
PREC_EMB = 200  # bits for embedding
CCp = ComplexField(PREC_EMB)
embs = Kabs.embeddings(CCp)
def all_pos(ph):
    try:
        return all(ph(x).real() > 0 and abs(ph(x).imag()) < CCp(10)**(-PREC_EMB//2)
                   for x in (S2_abs, S3_abs, S5_abs))
    except Exception:
        return False
phi = [ph for ph in embs if all_pos(ph)][0]
print(f"\nphi(a) = {phi(a).n(40)}")
print(f"phi(sqrt 2) = {phi(S2_abs).n(40)}")
print(f"phi(sqrt 3) = {phi(S3_abs).n(40)}")
print(f"phi(sqrt 5) = {phi(S5_abs).n(40)}")

# Rebuild K with embedding baked in — this is what RiemannSurface needs.
Kemb = NumberField(Kabs.defining_polynomial(), 'b', embedding=phi(a))
b = Kemb.gen()
iota = Kabs.hom([b], Kemb)
Sb2 = iota(S2_abs); Sb3 = iota(S3_abs); Sb5 = iota(S5_abs)

# ============================================================
# §2. Curve F = Y^4 - f(X) and holomorphic differentials
# ============================================================

R2 = PolynomialRing(Kemb, 2, names=['X', 'Y'])
X, Y = R2.gens()
f_poly = X * (X - 1) * (X - Sb2)**3 * (X - Sb3)**2 * (X - Sb5)**2
F = Y**4 - f_poly
print(f"\nF = Y^4 - f(X),  deg_X f = {f_poly.degree()}")

# Holomorphic differentials: omega = g(X,Y) dX / (dF/dY) = g dX / (4 Y^3).
# So dX/Y^r  <->  g = Y^{3-r} (scalar factor omitted).
#
# Canonical Prym-graded basis (from CSTAR + sprint35b):
#   j=1 (psi-eigenvalue -i): dX/Y,  X dX/Y
#   j=2 (psi-eigenvalue -1, iota-invariant, NOT in Prym):
#        (X-lam)(X-mu)(X-nu) dX/Y^2
#   j=3 (psi-eigenvalue +i): (X-lam)^2 (X-mu)(X-nu) dX/Y^3,
#                            X (X-lam)^2 (X-mu)(X-nu) dX/Y^3
diffs = [
    Y**2,                                          # dX/Y
    X * Y**2,                                      # X dX/Y
    (X - Sb2) * (X - Sb3) * (X - Sb5) * Y,         # (x-l)(x-m)(x-n) dX/Y^2  (ι-invariant)
    (X - Sb2)**2 * (X - Sb3) * (X - Sb5),          # (x-l)^2(x-m)(x-n) dX/Y^3
    X * (X - Sb2)**2 * (X - Sb3) * (X - Sb5),      # X (x-l)^2(x-m)(x-n) dX/Y^3
]
print(f"Supplied {len(diffs)} explicit differentials (bypasses Singular genus call)")

# ============================================================
# §3. Build RiemannSurface and compute period matrix
# ============================================================

from sage.schemes.riemann_surfaces.riemann_surface import RiemannSurface

PREC = 200  # bits of working precision — adjust as needed
print(f"\nBuilding RiemannSurface at prec={PREC} bits...")
t0 = time.time()
RS = RiemannSurface(F, prec=PREC, differentials=diffs)
print(f"RS built in {time.time()-t0:.2f}s. genus = {RS.genus}")
print(f"branch_locus size = {len(RS.branch_locus)}  (expect 5: 0, 1, sqrt 2, sqrt 3, sqrt 5)")

print("\nComputing period matrix (this is the long step)...")
t0 = time.time()
PM = RS.period_matrix()
print(f"period_matrix in {time.time()-t0:.2f}s. Shape: {PM.nrows()}x{PM.ncols()}")

# Normalized Riemann matrix tau (symmetric, Im positive definite)
print("\nComputing Riemann matrix tau = Pi_b Pi_a^-1 ...")
t0 = time.time()
tau = RS.riemann_matrix()
print(f"riemann_matrix in {time.time()-t0:.2f}s. Shape: {tau.nrows()}x{tau.ncols()}")

# ============================================================
# §4. det(Y) where Y = Im(tau)
# ============================================================

Y_imag = tau.apply_map(lambda z: z.imag())
detY = Y_imag.det()
print(f"\n=== det(Y) where Y = Im(tau) of the FULL Jacobian ===")
print(f"det(Y) = {detY}")
print(f"det(Y) numerical = {detY.n(60)}")

# Target from Sprint 35b CSTAR target:
#   det(Y)_target = 2086 + 462*sqrt(15) + 498*sqrt(10) + 730*sqrt(6)
#
# BUT this target was derived for the *Prym factor* det(Y), not the full Jacobian.
# To get the Prym det(Y), we need to restrict to the iota-anti-invariant
# 4-dim subspace. This is done by the psi-eigenvalue projection.

from sage.rings.real_mpfr import RealField
RRf = RealField(PREC)
target = 2086 + 462 * RRf(15).sqrt() + 498 * RRf(10).sqrt() + 730 * RRf(6).sqrt()
print(f"\nTarget det(Y)_Prym = 2086 + 462 sqrt(15) + 498 sqrt(10) + 730 sqrt(6)")
print(f"                   = {target}")

# ============================================================
# §5. Prym projection via psi-eigenvalues
# ============================================================

# psi: (x, y) -> (x, i*y). On differentials:
#   dx/y^j  ->  i^{-j} dx/y^j
# For j = 1: eigenvalue 1/i = -i
#     j = 2: eigenvalue -1 (iota-invariant, NOT in Prym)
#     j = 3: eigenvalue 1/i^3 = i
# So our differentials have psi-action diagonal with eigenvalues (-i, -i, -1, +i, +i).
# Prym = iota-anti-invariant (iota = psi^2); iota-eigenvalues are psi^2 = (-1, -1, +1, -1, -1).
# Prym H^{1,0} = the -1 iota-eigenspace on H^{1,0} = span of diffs 0,1,3,4 (indices).

prym_indices = [0, 1, 3, 4]  # skip index 2 (iota-invariant)
print(f"\nPrym H^{{1,0}} basis: differentials at indices {prym_indices}")
# Prym period matrix: 4 rows, 10 cols (need to project cycles too).
# For the FULL jacobian period_matrix is 5 x 10, rows indexed by diffs,
# columns indexed by 2g = 10 cycles in some basis.
PM_prym_rows = PM.matrix_from_rows(prym_indices)
print(f"Prym-rows period matrix shape: {PM_prym_rows.nrows()} x {PM_prym_rows.ncols()}")

# To get the 4 x 8 Prym period matrix, we need to project the cycle side onto
# the iota-anti-invariant homology. This requires knowing iota's action on H_1,
# which RiemannSurface does not give directly. Skipped here; noted as next step.
print("\n[NOTE] Restriction of cycle side to iota-anti-invariant homology not implemented.")
print("[NOTE] The full-Jacobian det(Y) above is one useful invariant;")
print("[NOTE] the Prym det(Y) requires the 4x4 Riemann matrix after projection.")

# ============================================================
# §6. Save results
# ============================================================

with open('canonical_period_matrix_v2.txt', 'w') as out:
    out.write(f"# Canonical triple (sqrt 2, sqrt 3, sqrt 5) at prec={PREC} bits\n")
    out.write(f"# Generated {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n\n")
    out.write(f"K = Q(sqrt 2, sqrt 3, sqrt 5), abs degree {Kabs.degree()}\n\n")
    out.write(f"phi(a) = {phi(a)}\n\n")
    out.write(f"genus = {RS.genus}\n")
    out.write(f"branch_locus size = {len(RS.branch_locus)}\n\n")
    out.write("=== Period matrix Pi (5 x 10) ===\n")
    out.write(str(PM.numerical_approx(60)) + "\n\n")
    out.write("=== Riemann matrix tau (5 x 5) ===\n")
    out.write(str(tau.numerical_approx(60)) + "\n\n")
    out.write(f"=== det(Y) where Y = Im(tau) of full Jacobian ===\n")
    out.write(f"{detY.n(80)}\n\n")
    out.write(f"Target Prym det(Y) = 2086 + 462*sqrt 15 + 498*sqrt 10 + 730*sqrt 6 = {target}\n")
print("\nResults saved to canonical_period_matrix_v2.txt")
print("\n=== DONE ===")
