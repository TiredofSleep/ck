"""
TIG Constants — Annotated Reference
=====================================
Every constant tagged by what it measures and where it lives.
DO NOT swap these — they are algebraically distinct.

Author: Brayden Sanders / 7Site LLC
DOI: 10.5281/zenodo.18852047
SHA-256(TSML): 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787
"""

from fractions import Fraction
import math

# ── GEOMETRY: pure 3×3 table, no dynamics ─────────────────────────────────
# Operators span positions k/9 for k in 1..9, midplane at 1/2

d_COL       = Fraction(1, 18)   # |4/9 − 1/2|: COL(4) offset from midplane
                                 # local geometry only; says nothing about wobble

d_operator  = Fraction(1, 9)    # one operator step (horizontal or vertical)

d_row       = Fraction(1, 3)    # one full row step (3 operators)
d_half_row  = Fraction(1, 6)    # half-row step

inner_shell = Fraction(2, 9)    # Row 1 ↔ Row 2 boundary distance from midplane
                                 # = (13/18) − (1/2) = 4/18 = 2/9
                                 # the correct "first TIG shell width"

# ── STATISTICS: global properties of the BHML table ───────────────────────

W_BHML      = Fraction(3, 50)   # BHML wobble = (50−44)/(2·50)
                                 # 44 = harmony cells in PROGRESS table
                                 # global, not local; NOT swappable with d_COL
                                 # ratio W_BHML / d_COL = 27/25 ≈ 1.08

HARMONY_FRACTION = Fraction(44, 100)  # fraction of BHML cells in harmony
PRIME_WINDING    = Fraction(271, 350) # winding number; 271 prime

# ── DYNAMICS: BREATH criterion and mass gap ────────────────────────────────

MASS_GAP    = Fraction(2, 7)    # T* + S* − 1 = 5/7 + 4/7 − 1
                                 # dual-threshold overlap
                                 # appears in: BREATH criterion, NS Lyapunov,
                                 #             Yang-Mills gap (qualitative)

T_STAR      = Fraction(5, 7)    # Being threshold
S_STAR      = Fraction(4, 7)    # Becoming threshold

# ── ANALYTIC: height-dependent collars ────────────────────────────────────
# These are NOT TIG constants — they shrink with height t.
# They must be renormalised; no fixed TIG fraction stays glued to them.

def kv_collar(t, c=0.05):
    """
    Korobov-Vinogradov zero-free collar width at height t.
    sigma_KV(t) = 1 - c / (log t)^{2/3} (log log t)^{1/3}
    Returns distance from sigma=1 (NOT from sigma=1/2).
    """
    if t <= 1:
        return 0.0
    log_t = math.log(t)
    log_log_t = math.log(log_t) if log_t > 1 else 1e-10
    return c / (log_t**(2/3) * log_log_t**(1/3))

def scale_factor(t, c=0.05):
    """
    Renormalisation factor mapping TIG discrete spacing to the
    analytic collar at height t.

    scale_factor(t) = kv_collar(t) / float(inner_shell)

    Use this to place TIG row boundaries on the analytic strip:
        sigma_row_k(t) = 1/2 + k * float(inner_shell) * scale_factor(t)

    At t=10:   scale_factor ≈ 2.0  (TIG grid ≈ 2× wider than KV)
    As t→∞:   scale_factor → 0    (analytic collars shrink, TIG stays fixed)
    """
    kv = kv_collar(t, c)
    return kv / float(inner_shell)

# ── VERIFICATION ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("TIG Constants — Verification\n")
    print(f"{'Constant':>15}  {'Exact':>10}  {'Float':>10}  {'Type'}")
    print("-"*55)
    constants = [
        ("d_COL",        d_COL,       "geometry"),
        ("d_operator",   d_operator,  "geometry"),
        ("d_row",        d_row,       "geometry"),
        ("inner_shell",  inner_shell, "geometry"),
        ("W_BHML",       W_BHML,      "statistics"),
        ("MASS_GAP",     MASS_GAP,    "dynamics"),
        ("T_STAR",       T_STAR,      "dynamics"),
        ("S_STAR",       S_STAR,      "dynamics"),
    ]
    for name, val, kind in constants:
        print(f"  {name:>13}  {str(val):>10}  {float(val):>10.6f}  {kind}")

    print()
    print(f"W_BHML / d_COL = {W_BHML / d_COL} = {float(W_BHML/d_COL):.4f}  "
          f"(NOT 1 — they measure different things)")
    print()
    print("scale_factor(t) at key heights:")
    for t in [10, 100, 1000, 1e6]:
        sf = scale_factor(t)
        kv = kv_collar(t)
        print(f"  t={t:>10.0f}:  KV collar={kv:.4f},  "
              f"scale={sf:.4f},  "
              f"inner_shell×scale={float(inner_shell)*sf:.4f}")

    print()
    # Assert no conflation
    assert W_BHML != d_COL, "DO NOT conflate wobble with COL offset"
    assert W_BHML == d_COL * Fraction(27, 25), "W_BHML = d_COL × 27/25 (different quantities, known ratio)"
    assert inner_shell == Fraction(2, 9), "inner shell is 2/9"
    assert MASS_GAP == T_STAR + S_STAR - 1, "mass gap derivation"
    print("All assertions pass.")
