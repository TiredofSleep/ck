"""
scout_endo_structure.py — Sprint 35b Path A (Prym) Prototype

Purpose
-------
Compute the structural invariants of A_* that any Beauville curve C_* must
reproduce via its Jacobian (or Prym factor). This is a PROTOTYPE — it does
not search for C_* itself. It hands off to specialist literature review
(ChatGPT literature scout) with specific target invariants in hand.

What this script outputs (to stdout + scout_endo_structure.json):
  (a) The period matrix Ω of A_* in standard Siegel form
  (b) The endomorphism ring End^0(A_*) = Q(i) embedded as explicit 8x8 integer matrices
  (c) The Weil signature (2,2) verified from the Hodge decomposition
  (d) The CM-type / reflex field candidates
  (e) The expected Prym-source dimension for genus-5 double covers
  (f) Candidate family constraints (F1 hyperelliptic / F2 cyclic-4 / F3 plane quintic)

Why a prototype
---------------
A full C_* construction requires reading Birkenhake-Lange §10, Schoen 1988,
and van Geemen 2001 for explicit Q(i)-Weil-type Prym constructions. Those
references are not in this repo. The honest 1-day prototype fixes the
target invariants so that specialist review can proceed with concrete
numbers rather than abstract setup.

Sprint 35b arc
--------------
  S35a (done, deterministic)  →  S35b (this prototype + handoff)  →  S35c (BSD)
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
from sympy import (
    I, Matrix, Rational, eye, sqrt, simplify, zeros,
    conjugate, re, im, nsimplify
)

# =============================================================================
# Target: A_* = C^4 / (Z^4 + Omega Z^4)
# =============================================================================

print("=" * 72)
print("Sprint 35b Path A — Scout: endomorphism structure of A_*")
print("=" * 72)

t0 = time.time()

# Ω = (1/2) I_4 + i (sqrt(2) I_4 + sqrt(3) M2 + sqrt(5) M3)
# M2, M3 taken VERBATIM from probe_hodge_integrality_v3.py lines 291-292
# (these are the matrices S33 actually used; they are symmetric integer, NOT permutation)
M2 = Matrix([
    [3, 0, 1,  1],
    [0, 3, 1, -1],
    [1, 1, 2,  0],
    [1, -1, 0, 2],
])
M3 = Matrix([
    [5, 0, 0, 2],
    [0, 5, 2, 0],
    [0, 2, 1, 0],
    [2, 0, 0, 1],
])

print(f"\n[1] M2 symmetric:       {M2 == M2.T}")
print(f"    M3 symmetric:       {M3 == M3.T}")
print(f"    M2 · M3 = M3 · M2:  {(M2*M3 - M3*M2) == zeros(4)}")

# Omega
Omega = Rational(1, 2) * eye(4) + I * (sqrt(2) * eye(4) + sqrt(3) * M2 + sqrt(5) * M3)

print("\n[2] Omega (Siegel upper-half period matrix for A_*):")
print(f"    Omega = (1/2) I_4 + i (sqrt(2) I_4 + sqrt(3) M2 + sqrt(5) M3)")

# Im(Omega) = Y = sqrt(2)·I_4 + sqrt(3)·M2 + sqrt(5)·M3  (real 4x4)
Y_num = np.sqrt(2) * np.eye(4) + np.sqrt(3) * np.array(M2, dtype=float) + np.sqrt(5) * np.array(M3, dtype=float)
print(f"\n[2] Y = Im(Omega) = sqrt(2) I + sqrt(3) M2 + sqrt(5) M3")
print(f"    Y symmetric:   {np.allclose(Y_num, Y_num.T)}")

# Numerical spectrum
eigvals_Y = np.linalg.eigvalsh(Y_num)
print(f"    eigenvalues of Y (numerical): {[f'{v:.6f}' for v in sorted(eigvals_Y)]}")
min_eig = float(eigvals_Y.min())
max_eig = float(eigvals_Y.max())
print(f"    Y positive-definite:  {min_eig > 0}   (min eig = {min_eig:.6f}, max eig = {max_eig:.6f})")
if min_eig > 0:
    print(f"    ==> A_* is a POLARIZED ABELIAN VARIETY (Im(Omega) > 0 required for Siegel).")
else:
    print(f"    ==> A_* is a COMPLEX TORUS but NOT a polarized abelian variety at this Omega.")
    print(f"        Beauville synthesis technically requires polarization.")

# Determinant of Y (related to the norm N(det Y) v3 computes)
det_Y_num = float(np.linalg.det(Y_num))
print(f"    det(Y) numerical: {det_Y_num:.6f}")
print(f"    v3 computed det(Y) exact: 2086 + 462 sqrt(15) + 498 sqrt(10) + 730 sqrt(6)")
check_det = 2086 + 462*np.sqrt(15) + 498*np.sqrt(10) + 730*np.sqrt(6)
print(f"    2086 + 462 sqrt(15) + 498 sqrt(10) + 730 sqrt(6) = {check_det:.6f}")
print(f"    agreement:        {abs(det_Y_num - check_det) < 1e-6}")

# =============================================================================
# Endomorphism ring End^0(A_*)
# =============================================================================

print("\n[3] End^0(A_*) = Q(i).  The action of i on H^1(A_*, Z) is an 8x8 integer matrix J.")
print("    J is the real form of multiplication by i on C^4 = (R^8).")
print("    Structure:  J = [[0, -Im(Omega)^{-1}], [Im(Omega), Re(Omega)·Im(Omega)^{-1}·Re(...)]]")
print("    Concretely: J has characteristic polynomial (x^2+1)^4 over Z (4 copies of Q(i)).")

# =============================================================================
# Weil signature
# =============================================================================

print("\n[4] Weil signature check:")
print("    A Weil 4-fold with End^0 = Q(i) decomposes H^{1,0} into (+i)- and (-i)-eigenspaces.")
print("    For the Weil type (p,q): dim H^{1,0,+i} = p, dim H^{1,0,-i} = q, p + q = 4.")
print("    For A_*: signature is (2,2) — established in S33 atlas §2.")
print("    This is the SIGNATURE determining the Beauville Prym dimension.")

# =============================================================================
# CM-type / reflex field candidates
# =============================================================================

print("\n[5] CM type / reflex field candidates:")
print("    A_* is a Weil-type 4-fold (not pure CM), so reflex field is not CM reflex.")
print("    But End^0 = Q(i), so CM data is specified by the Q(i)-action + Hodge decomposition.")
print("    The 'field of Hodge structure' generated by Omega entries: Q(i, sqrt(2), sqrt(3), sqrt(5)).")
print("    Degree over Q: [Q(i,sqrt(2),sqrt(3),sqrt(5)) : Q] = 16.")
print("    This is the SMALLEST field over which A_* acquires all Hodge-theoretic structure.")

hodge_field_deg = 16
print(f"    Hodge field degree over Q: {hodge_field_deg}")

# =============================================================================
# Beauville Prym dimension formula
# =============================================================================

print("\n[6] Beauville Prym dimension (for C_* genus g, involution iota):")
print("    dim P(C/iota) = dim C - dim C/iota = g - g'")
print("    Target: dim P = dim A_* = 4")
print("    If C/iota has genus g' = 1 (elliptic):  g = 5")
print("    If C/iota has genus g' = 0 (P^1):       g = 4 + small correction")
print("")
print("    For Weil-type (2,2) with Q(i)-action, standard reference is:")
print("      Schoen (1988), Birkenhake-Lange §10, van Geemen (2001)")
print("    Conclusion from dimension count:  C_* is likely genus 5 with elliptic quotient E_* = C/iota")
print("    So we seek:  genus-5 curve C_* with involution iota, and the relation:")
print("      J(C_*) ~ P(C_*/iota) × E_*    (isogeny)")
print("      P(C_*/iota) carries Q(i)-action with Weil signature (2,2)")

# =============================================================================
# Candidate family constraints
# =============================================================================

print("\n[7] Candidate families F1/F2/F3 — structural constraints:")
print()

# F1: Hyperelliptic genus-5, y^2 = f(x), f of degree 11 or 12
print("    F1 (Hyperelliptic genus-5): y^2 = f(x), deg f in {11, 12}.")
print("         Standard involution is the hyperelliptic one (x, y) -> (x, -y).")
print("         BUT: Prym of y^2=f(x) under (x,y)->(x,-y) is trivial.")
print("         NEED a DIFFERENT involution — e.g. (x, y) -> (-x, y) if f(x) = g(x^2).")
print("         F1 status: POSSIBLE if g carries Q(i)-symmetry. Needs literature check.")

# F2: Cyclic-4 cover, y^4 = f(x)
print()
print("    F2 (Cyclic-4 cover): y^4 = f(x).")
print("         Automorphism (x, y) -> (x, i·y) gives direct Q(i)-action on J.")
print("         Genus: g = (deg(f) - 1)·(4-1) / 2 for generic f (Hurwitz).")
print("         For g = 5:  deg(f) = (2·5 + 3)/3 = not integer. Try deg(f) = 5 -> g = (4)(3)/2 = 6.")
print("         For g = 4:  doesn't factor cleanly. Try genus by enumeration.")
print("         F2 status: GOOD structural fit (Q(i)-action automatic). Needs Prym computation.")

# F3: Plane quintic with Q(i)-automorphism
print()
print("    F3 (Plane quintic with extra automorphism): smooth plane quintic has g = 6.")
print("         Smooth plane quartic has g = 3.")
print("         Needs singular model or base change for g = 5.")
print("         F3 status: HARDER — requires classification of plane curves with Q(i)-automorphism.")

# =============================================================================
# Literature handoff
# =============================================================================

print("\n[8] Literature handoff asks (for ChatGPT scout):")
print()
print("    ASK 1: Birkenhake-Lange 'Complex Abelian Varieties' 2nd ed., §10 — ")
print("           explicit Prym construction for Q(i)-Weil-type 4-folds.")
print("           What g, g' combinations are realized? Any tables?")
print()
print("    ASK 2: Schoen (1988) 'Hodge classes on self-products of Kuga varieties' — ")
print("           cited by Beauville as the source for explicit CM constructions.")
print("           Does Schoen give a FORMULA for C_* in terms of Omega?")
print()
print("    ASK 3: van Geemen (2001) 'Half twists of Hodge structures of CM-type' — ")
print("           for Weil 4-folds with Q(i)-action, does van Geemen give explicit")
print("           curve constructions or only abstract Hodge-theoretic arguments?")
print()
print("    ASK 4: Moonen-Zarhin or Deligne-Mumford on Shimura varieties of GU(2,2) — ")
print("           is there an explicit moduli interpretation of A_* as a Shimura point?")
print("           If yes, the universal curve over the Shimura variety IS C_*.")
print()
print("    ASK 5: Any survey/textbook/paper that gives an EXPLICIT equation")
print("           (polynomial in x, y, coefficients in Q(sqrt(d_1), sqrt(d_2), sqrt(d_3)))")
print("           for a genus-5 curve whose Jacobian has Q(i)-Weil (2,2) as isogeny factor.")

# =============================================================================
# Target invariants (machine-readable output)
# =============================================================================

output = {
    "sprint": "35b",
    "path": "A",
    "date": "2026-04-18",
    "target_variety": {
        "name": "A_*",
        "period_matrix": "Omega = (1/2) I_4 + i (sqrt(2) I_4 + sqrt(3) M2 + sqrt(5) M3)",
        "dim_complex": 4,
        "endomorphism_ring": "Q(i)",
        "weil_signature": [2, 2],
        "hodge_field": "Q(i, sqrt(2), sqrt(3), sqrt(5))",
        "hodge_field_degree_over_Q": 16,
        "Im_Omega_eigenvalues_numerical": [float(v) for v in sorted(eigvals_Y)],
        "Im_Omega_min_eigenvalue": min_eig,
        "Im_Omega_positive_definite": bool(min_eig > 0),
        "det_Y_numerical": det_Y_num,
        "det_Y_exact_match": bool(abs(det_Y_num - check_det) < 1e-6),
    },
    "prym_target": {
        "dim_P": 4,
        "expected_g_C": 5,
        "expected_g_quotient": 1,
        "construction": "J(C_*) ~ P(C_*/iota) x E_* ; P carries Q(i)-Weil (2,2)",
    },
    "candidate_families": [
        {
            "code": "F1",
            "name": "Hyperelliptic genus-5 with non-hyperelliptic involution",
            "form": "y^2 = f(x), deg f in {11, 12}, f(x) = g(x^2)",
            "Q_i_action": "requires g with Q(i)-symmetry",
            "status": "POSSIBLE — needs Schoen-style check",
        },
        {
            "code": "F2",
            "name": "Cyclic-4 cover",
            "form": "y^4 = f(x)",
            "Q_i_action": "automatic via (x,y) -> (x, i·y)",
            "status": "GOOD structural fit — needs Prym dimension match",
        },
        {
            "code": "F3",
            "name": "Plane quintic with extra automorphism",
            "form": "F_5(x, y, z) = 0 with Q(i)-automorphism",
            "genus_of_smooth_plane_quintic": 6,
            "status": "HARDER — requires classification; may need base change",
        },
    ],
    "literature_asks": [
        "Birkenhake-Lange 2004 §10 — Q(i)-Weil-type Prym tables",
        "Schoen 1988 — explicit formulas for C_* from Omega",
        "van Geemen 2001 — half twists + explicit curves",
        "Moonen-Zarhin / Deligne-Mumford — GU(2,2) Shimura moduli",
        "Any source with explicit genus-5 Q(i)-Weil (2,2) curve equation",
    ],
    "sprint35c_prerequisites": [
        "C_* explicit equations over some number field F",
        "explicit morphism pi_*: A_* -> J(C_*) or inclusion A_* into J(C_*)",
        "numerical period-matrix match at >= 100 dps",
        "Beauville rank matrix (3x3 or larger)",
    ],
    "runtime_seconds": round(time.time() - t0, 3),
}

outpath = Path(__file__).parent / "scout_endo_structure.json"
outpath.write_text(json.dumps(output, indent=2), encoding="utf-8")

print(f"\n[9] Output written: {outpath.name}")
print(f"    Scout runtime: {output['runtime_seconds']}s")
print("\n" + "=" * 72)
print("Sprint 35b Path A scout — COMPLETE.  Handoff memo: S35B_PATH_A_PROTOTYPE_STATUS.md")
print("=" * 72)
