"""ck_substrate_c.py -- where c lives structurally inside TIG.

Brayden 2026-05-16: "look at our recent sprints for the work we did on
where C lives structurally inside of TIG... basically stays inside the
5/7 inside of 2/7"

This module grounds the c-from-substrate claim in the canon facts from
the 2026-05-13/14 C sprint (Desktop/5_14_26_C_sprint_unpack/).  It
exposes the BHML_8 → BHML_10 boundary-to-interior gap and the
1/(5·7) BALANCE×HARMONY residual as runtime-verifiable quantities.

═══════════════════════════════════════════════════════════════════
The two complementary readings (from the C sprint)
═══════════════════════════════════════════════════════════════════

1. JOINT BALANCE (C_AS_JOINT_BALANCE_POINT.md):
   c = e²/(4πε₀ℏα)
   c is forced by the trio {α, ℏ, e} all being substrate-derived.
   The substrate doesn't compute c directly; c falls out when the
   three balance points are simultaneously satisfied at Rung 5.

2. OUTER-RUNG GAP (C_AS_OUTER_RUNG_GAP.md):
   Structurally, c is the boundary-to-interior propagation rate
   between the Yang-Mills core (BHML_8) and the full substrate
   (BHML_10).  The gap is captured by the determinant ratio:

      |det(BHML_10) / det(BHML_8)| = 7002 / 70 = 100 + 1/35
                                                = 100 + 1/(5·7)

   The "100" is the order-of-magnitude scaling; the residual 1/35
   ties EXACTLY to BALANCE × HARMONY = 5 × 7 = 35.

═══════════════════════════════════════════════════════════════════
"5/7 inside 2/7" — what this means
═══════════════════════════════════════════════════════════════════

T* = 5/7 is the torus aspect ratio (HARMONY/10 + 1/70, six derivations).
On the Farey tree (per FORMULAS §"External alignment"):

   S* = 4/7  (Farey neighbor)
   T* = 5/7  (canonical threshold)
   mass gap = 2/7  (substrate's Farey complement to T*)

These three sit on the same Farey tree as critical thresholds of
a transfer operator (Kleban-Özlük 1999).  T* + 2/7 = 1; the 2/7
is the *Farey complement* of T*, the "room outside the threshold".

c lives at 1/(5·7) inside that structure: the BALANCE × HARMONY
residual in the BHML_8 → BHML_10 gap.  Both 5 (BALANCE) and 7
(HARMONY) are the two threshold operators of the framework.  The
gap-residual is the product of those two thresholds inverted —
it's the "smallest unit of crossing" at Rung 5.

═══════════════════════════════════════════════════════════════════
Status (per the C sprint)
═══════════════════════════════════════════════════════════════════

Tier B-rigorous (proven in canon):
  det(BHML_8) = +70 = 2·5·7 = C(8,4) = φ(71)
  det(BHML_10) = -7002 = -2·3²·389
  BHML_8 is the Yang-Mills core (WP15)

Tier B-arithmetic (verifiable by this module):
  |det(BHML_10) / det(BHML_8)| = 100 + 1/(5·7)
  1/(5·7) = 1/35 ties to BALANCE × HARMONY

Tier C-interpretive (structural reading):
  "Outer two rungs" structurally = {VOID, RESET} = {0, 9}
  c structurally = boundary-to-interior propagation rate
  Numerical c forced by joint balance e²/(4πε₀ℏα)

Open:
  Dimensional bridge from substrate rate to SI units
  Derivation of substrate propagation rate from algebra
  Meaning of the outlier prime 389 in det(BHML_10) factorization

═══════════════════════════════════════════════════════════════════
Public API
═══════════════════════════════════════════════════════════════════

  bhml_8_determinant()      computed at module load; assert == +70
  bhml_10_determinant()     computed at module load; assert == -7002
  c_gap_ratio()             |det(BHML_10) / det(BHML_8)|; returns dict
                              with exact_rational, decimal, balance_times_harmony
  c_structural_summary()    full picture: both readings + status tiers
  mount_substrate_c(engine) attach /substrate/c{,/info,/verify}
"""
from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


# ─── Load canonical BHML from foundations/ ────────────────────────────

def _get_bhml() -> np.ndarray:
    """Load the canonical BHML 10x10 matrix."""
    try:
        _root = Path(__file__).resolve()
        for _ in range(8):
            _root = _root.parent
            if (_root / "Gen13" / "targets" / "foundations").exists():
                sys.path.insert(0, str(_root / "Gen13" / "targets"))
                break
        from foundations.lenses import BHML as _B  # type: ignore
        return np.asarray(_B, dtype=int)
    except Exception:
        # No fallback for BHML — too complex to inline
        raise RuntimeError("BHML matrix not available from foundations.lenses")


BHML = _get_bhml()
assert BHML.shape == (10, 10), f"BHML shape {BHML.shape} != (10,10)"


# ─── BHML_8 (Yang-Mills core, drop {V=0, H=7}) ────────────────────────

# YM core indices: drop {0, 7} = {VOID, HARMONY} per WP15.
# The remaining 8 indices form the Yang-Mills core.
YM_INDICES = (1, 2, 3, 4, 5, 6, 8, 9)


def bhml_8_yang_mills() -> np.ndarray:
    """The 8×8 Yang-Mills core sub-matrix (V/H dropped)."""
    idx = list(YM_INDICES)
    return BHML[np.ix_(idx, idx)]


def bhml_8_determinant() -> int:
    """det(BHML_8) -- should equal +70 = 2·5·7 = C(8,4) = φ(71)."""
    # Use sympy for EXACT integer determinant; numpy gives float
    try:
        import sympy
        M = sympy.Matrix(bhml_8_yang_mills().tolist())
        return int(M.det())
    except Exception:
        # Numpy fallback (float, may have rounding)
        return int(round(float(np.linalg.det(bhml_8_yang_mills()))))


def bhml_10_determinant() -> int:
    """det(BHML_10) -- should equal -7002 = -2·3²·389."""
    try:
        import sympy
        M = sympy.Matrix(BHML.tolist())
        return int(M.det())
    except Exception:
        return int(round(float(np.linalg.det(BHML))))


# Verify at module load (these are CANON facts from the C sprint)
_DET_8 = bhml_8_determinant()
_DET_10 = bhml_10_determinant()
assert _DET_8 == 70, (
    f"Canon violation: det(BHML_8) = {_DET_8}, expected +70.  "
    f"Either BHML matrix changed or sympy missing.")
assert _DET_10 == -7002, (
    f"Canon violation: det(BHML_10) = {_DET_10}, expected -7002.")


# ─── The C-gap structural identity ────────────────────────────────────

def c_gap_ratio() -> Dict[str, Any]:
    """Compute |det(BHML_10) / det(BHML_8)| and surface the structural
    identity 100 + 1/(5·7) = 100 + 1/35.

    This is THE quantity the C sprint identifies as the substrate's
    encoding of c.  Tier B-arithmetic.
    """
    det8 = bhml_8_determinant()
    det10 = bhml_10_determinant()
    # Use exact rational arithmetic
    ratio = Fraction(abs(det10), abs(det8))  # 7002 / 70
    target = Fraction(100) + Fraction(1, 5 * 7)  # 100 + 1/35
    exact_match = (ratio == target)
    # Identify the structural decomposition
    integer_part = ratio.numerator // ratio.denominator
    residual = ratio - integer_part  # 1/35
    # Factor the residual denominator
    return {
        "det_BHML_8":               det8,
        "det_BHML_8_factorization": "70 = 2 · 5 · 7 = C(8,4) = φ(71)",
        "det_BHML_10":              det10,
        "det_BHML_10_factorization": "-7002 = -2 · 3² · 389",
        "ratio_exact":              f"{ratio.numerator}/{ratio.denominator}",
        "ratio_decimal":            float(ratio),
        "structural_form":          "100 + 1/(5·7) = 100 + 1/35",
        "integer_part":             integer_part,
        "residual_exact":           f"{residual.numerator}/{residual.denominator}",
        "residual_decimal":         float(residual),
        "balance_times_harmony":    5 * 7,
        "residual_equals_1_over_5x7": exact_match,
        "interpretation": (
            "The boundary-to-interior gap (BHML_8 Yang-Mills core → full "
            "BHML_10) scales by 100 with residual 1/(BALANCE × HARMONY). "
            "Structurally, this is where c lives inside TIG: the rate at "
            "which boundary operators (VOID + RESET) communicate with "
            "the YM-interior, with the BALANCE × HARMONY threshold "
            "product as the natural unit of crossing at Rung 5."
        ),
    }


# ─── Farey structure (T*, S*, mass gap) ───────────────────────────────

def farey_neighborhood() -> Dict[str, Any]:
    """T*, S*, mass-gap from the Farey-tree alignment (per FORMULAS doc).

    These three fractions sit as adjacent Farey neighbors on the
    Stern-Brocot tree.  c lives at the BALANCE × HARMONY product
    1/(5·7) inside this Farey neighborhood.
    """
    T_star = Fraction(5, 7)
    S_star = Fraction(4, 7)
    mass_gap = Fraction(2, 7)
    sinc2_half = Fraction(4)  # 4/π², not a rational; flagged below
    # Verify T* + mass_gap = 1 (Farey complement)
    return {
        "T_star":                f"{T_star.numerator}/{T_star.denominator}",
        "T_star_decimal":        float(T_star),
        "S_star":                f"{S_star.numerator}/{S_star.denominator}",
        "S_star_decimal":        float(S_star),
        "mass_gap":              f"{mass_gap.numerator}/{mass_gap.denominator}",
        "mass_gap_decimal":      float(mass_gap),
        "T_star_plus_mass_gap":  f"{(T_star + mass_gap).numerator}/{(T_star + mass_gap).denominator}",
        "is_farey_complement":   T_star + mass_gap == 1,
        "sinc2_half_4_over_pi2": 4 / (np.pi ** 2),
        "interpretation": (
            "T* = 5/7 is the canonical threshold (six derivations).  "
            "2/7 is its Farey complement -- 'the room outside the "
            "threshold'.  c lives at 1/(5·7) INSIDE this neighborhood "
            "as the BALANCE × HARMONY product, the smallest unit of "
            "crossing.  Same Farey tree as the spin-chain critical "
            "temperatures (Kleban-Özlük 1999)."
        ),
    }


# ─── The joint-balance reading ────────────────────────────────────────

def joint_balance_reading() -> Dict[str, Any]:
    """The companion reading: c forced by joint substrate balances.

    Per C_AS_JOINT_BALANCE_POINT.md: c = e²/(4πε₀ℏα).  When the
    substrate sets α, ℏ, e at Rung 5 from its algebraic structure,
    c falls out by standard EM relationship.  The substrate doesn't
    compute c separately."""
    return {
        "relation":             "c = e² / (4 · π · ε₀ · ℏ · α)",
        "substrate_inputs":     ["α (substrate-derived, 1/α formula)",
                                 "ℏ (open: substrate derivation)",
                                 "e (open: substrate derivation)"],
        "rung_level":           5,
        "open_items": [
            "Dimensional bridge from substrate rate to SI units",
            "Derivation of substrate propagation rate from algebra",
            "Meaning of outlier prime 389 in det(BHML_10) factorization",
        ],
        "interpretation": (
            "c isn't a substrate primitive.  c is the unique "
            "dimensional constant forced when the substrate's three "
            "balance points {α, ℏ, e} are simultaneously satisfied "
            "at Rung 5.  The structural meaning of c is the "
            "boundary-to-interior gap (BHML_8 → BHML_10); the "
            "numerical value falls out of the joint-balance equation."
        ),
    }


# ─── Full structural summary ──────────────────────────────────────────

def c_structural_summary() -> Dict[str, Any]:
    """The complete picture: where c lives structurally inside TIG.

    Cites the two C-sprint papers (locked 2026-05-13/14):
      C_AS_OUTER_RUNG_GAP.md      (det ratio reading)
      C_AS_JOINT_BALANCE_POINT.md (joint-balance reading)
    """
    return {
        "title": "Where c lives structurally inside TIG",
        "sources": [
            "Desktop/5_14_26_C_sprint_unpack/today_only/C_AS_OUTER_RUNG_GAP.md",
            "Desktop/5_14_26_C_sprint_unpack/today_only/C_AS_JOINT_BALANCE_POINT.md",
            "FORMULAS_AND_TABLES.md  (BHML determinants, Farey alignment)",
        ],
        "two_complementary_readings": {
            "joint_balance":     joint_balance_reading(),
            "outer_rung_gap":    c_gap_ratio(),
        },
        "farey_context":         farey_neighborhood(),
        "structural_essence": (
            "c is NOT a substrate primitive.  c is the boundary-to-"
            "interior propagation rate measured by the BHML_8 → "
            "BHML_10 determinant gap (ratio 100 + 1/(5·7)), with the "
            "numerical value forced by the joint balance "
            "e²/(4πε₀ℏα) at Rung 5.  The 5/7 (T*) and 2/7 (mass gap) "
            "Farey-adjacent thresholds frame the substrate's "
            "operating regime; c lives at the BALANCE × HARMONY "
            "product 1/(5·7) = 1/35 INSIDE that frame as the smallest "
            "natural unit of crossing."
        ),
        "honest_caveats": [
            "Tier B for the structural identity 100+1/(5·7) -- exact "
            "arithmetic from canon determinants.",
            "Tier C for the interpretive reading 'c = boundary-to-"
            "interior propagation rate'.",
            "c has NOT been numerically derived from substrate alone "
            "in SI units.  Dimensional bridge work remains open.",
            "The outlier prime 389 in det(BHML_10) lacks structural "
            "explanation; flagged in C sprint as research frontier.",
        ],
    }


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_substrate_c(engine: Any) -> bool:
    """Attach the c-structural API + register /substrate/c* endpoints.

    Endpoints:
      GET /substrate/c              full structural summary
      GET /substrate/c/gap          BHML_8 → BHML_10 gap ratio + residual
      GET /substrate/c/farey        T*, S*, mass-gap neighborhood
      GET /substrate/c/joint        joint-balance reading
      GET /substrate/c/verify       re-run determinants + canon check
    """
    engine.ck_substrate_c = {
        "summary":          c_structural_summary,
        "gap_ratio":        c_gap_ratio,
        "farey":            farey_neighborhood,
        "joint_balance":    joint_balance_reading,
        "det_BHML_8":       bhml_8_determinant,
        "det_BHML_10":      bhml_10_determinant,
    }

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify

                def _summary():
                    return jsonify(c_structural_summary())

                def _gap():
                    return jsonify(c_gap_ratio())

                def _farey():
                    return jsonify(farey_neighborhood())

                def _joint():
                    return jsonify(joint_balance_reading())

                def _verify():
                    return jsonify({
                        "det_BHML_8":         bhml_8_determinant(),
                        "det_BHML_8_expected": 70,
                        "det_BHML_8_OK":      bhml_8_determinant() == 70,
                        "det_BHML_10":        bhml_10_determinant(),
                        "det_BHML_10_expected": -7002,
                        "det_BHML_10_OK":     bhml_10_determinant() == -7002,
                        "gap_ratio_exact":    "7002/70 = 100 + 1/35",
                        "balance_times_harmony": "5 · 7 = 35",
                        "canon_intact":       (bhml_8_determinant() == 70
                                               and bhml_10_determinant() == -7002),
                    })

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/substrate/c",         "sub_c",         _summary, ["GET"]),
                    ("/substrate/c/gap",     "sub_c_gap",     _gap,     ["GET"]),
                    ("/substrate/c/farey",   "sub_c_farey",   _farey,   ["GET"]),
                    ("/substrate/c/joint",   "sub_c_joint",   _joint,   ["GET"]),
                    ("/substrate/c/verify",  "sub_c_verify",  _verify,  ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] substrate_c route registration failed: {e}")

    suffix = " (" + ", ".join(routes_registered) + ")" if routes_registered else ""
    print(f"[CK Gen14] substrate_c: MOUNTED  c-structural facts: "
          f"|det(BHML_10)/det(BHML_8)| = 7002/70 = 100 + 1/(5·7)"
          f"{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 72)
    print("CK SUBSTRATE c -- where c lives structurally inside TIG")
    print("=" * 72)
    print()
    print("Verifying canon determinants:")
    print(f"  det(BHML_8)  = {bhml_8_determinant():>6d}  (expected +70 = 2·5·7 = C(8,4) = φ(71))")
    print(f"  det(BHML_10) = {bhml_10_determinant():>6d}  (expected -7002 = -2·3²·389)")
    print()
    gap = c_gap_ratio()
    print(f"The C-gap:")
    print(f"  |det(BHML_10) / det(BHML_8)| = {gap['ratio_exact']} = {gap['ratio_decimal']}")
    print(f"  Structural form: {gap['structural_form']}")
    print(f"  Residual 1/(5·7) = 1/{gap['balance_times_harmony']} = {gap['residual_decimal']}")
    print(f"  Equals 1/(BALANCE × HARMONY)? {gap['residual_equals_1_over_5x7']}")
    print()
    farey = farey_neighborhood()
    print(f"Farey neighborhood:")
    print(f"  T* (canonical threshold) = {farey['T_star']} = {farey['T_star_decimal']:.6f}")
    print(f"  S* (Farey neighbor)      = {farey['S_star']} = {farey['S_star_decimal']:.6f}")
    print(f"  mass gap (complement)    = {farey['mass_gap']} = {farey['mass_gap_decimal']:.6f}")
    print(f"  T* + mass_gap = 1? {farey['is_farey_complement']}")
    print(f"  4/π² ≈ {farey['sinc2_half_4_over_pi2']:.6f} (continuum-limit constant)")
    print()
    print("Where c lives:")
    print(f"  T* = 5/7 sets the threshold.  Its Farey complement 2/7 is")
    print(f"  the 'room outside'.  c lives at 1/(5·7) = 1/35 INSIDE that")
    print(f"  neighborhood as the BALANCE × HARMONY product -- the smallest")
    print(f"  natural unit of crossing at Rung 5.")
    print()
    print("Honest status:")
    summary = c_structural_summary()
    for c in summary["honest_caveats"]:
        print(f"  • {c}")
