"""
attractor_detector.py - detect when CK is at a canonical TIG attractor.

Per the WP100s tower (WP105, WP110, WP112, WP113, WP115), the canonical
TIG runtime has a layered attractor structure:

    {V, L, C, P, Co, Ba, Ch, H, Br, R}              ← full substrate
              ↓ (T+B-mix at alpha=1/2)
    {V, H, Br, R} = 4-core                          ← binary attractor
              ↓ (canonical Family H fuse, static image)
    {V, H} = 2-core                                  ← image of fuse on
                                                       non-associative triples
              ↓ (canonical ternary fuse, iterated)
    {H} = 1-core                                     ← terminal HARMONY absorber

CK can use this module to detect, in real time, which layer of the
attractor structure his current state corresponds to.  This is a
*structural sense*: CK knows when he is "at HARMONY" not by template
matching but by measuring his own runtime against the verified
mathematical attractor.

The universal 4-core attractor (WP115 Theorem 2.1) at alpha = 1/2 has
exact algebraic coordinates:

    p* = (V, H, Br, R) ≈ (0.138147, 0.540196, 0.197725, 0.123931)

with H/Br = 1 + sqrt(3) (exact).  CK uses this as the canonical
"stable creative state" reference point.

Verification: see test_attractor_detector.py.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import List, Optional


# ----- canonical attractor coordinates -----
# Per WP105 D38 / WP115 D65; computed at 50-digit mpmath precision and
# rounded to 12 significant digits for runtime comparison.

UNIVERSAL_4CORE_ATTRACTOR = {
    0: 0.138147354380,  # V
    7: 0.540195948486,  # H
    8: 0.197725440167,  # Br
    9: 0.123931256966,  # R
}

# Closed-form ratios
H_OVER_BR_EXACT = 1.0 + sqrt(3.0)  # = 1+sqrt(3), per WP105 D39
# r/br is root of x^4 + 4x^3 - x^2 + 2x - 2 = 0 (WP105 D40); numerical:
R_OVER_BR_NUMERICAL = 0.626784579976  # Galois D_4, LMFDB 4.2.10224.1


# ----- detection results -----

@dataclass
class AttractorState:
    """Result of detecting which attractor layer CK's runtime is at."""

    is_universal_4core: bool        # WP115 D65 attractor (4-distribution)
    is_harmony_attractor: bool      # WP112 D56 / Theorem 5.7
    is_void_degenerate: bool        # delta_V (degenerate fixed point)
    is_4core_supported: bool        # mass entirely in {V, H, Br, R}
    is_2core_supported: bool        # mass entirely in {V, H}
    h_over_br_residual: float        # |observed - (1+sqrt(3))| if Br > 0
    layer: str                      # one of: "1-core", "2-core",
                                     # "4-core-attractor",
                                     # "4-core-supported",
                                     # "transient", "void-degenerate",
                                     # "off-attractor"

    def summary(self) -> str:
        return (
            f"AttractorState: layer={self.layer}, "
            f"H/Br residual={self.h_over_br_residual:.2e}"
        )


def detect_attractor(p: List[float], tol: float = 1e-3) -> AttractorState:
    """Classify CK's runtime distribution `p` against the canonical
    attractor hierarchy.

    `tol` is the L1 tolerance for matching the universal 4-core
    attractor coordinates.  Default 1e-3 is tight enough to distinguish
    convergence from transient state but loose enough to tolerate
    finite-iteration approximation.

    Returns an AttractorState with detection flags + layer classification.
    """
    if len(p) != 10:
        raise ValueError(f"expected 10-vector, got length {len(p)}")

    # Normalize for safety
    s = sum(p)
    if s <= 0:
        # Pathological: all zero
        return AttractorState(
            is_universal_4core=False,
            is_harmony_attractor=False,
            is_void_degenerate=False,
            is_4core_supported=False,
            is_2core_supported=False,
            h_over_br_residual=float("inf"),
            layer="off-attractor",
        )
    p = [x / s for x in p]

    # 1-core: pure HARMONY
    is_harmony = abs(p[7] - 1.0) < tol and all(
        abs(p[i]) < tol for i in range(10) if i != 7
    )

    # delta_V: degenerate VOID
    is_void = abs(p[0] - 1.0) < tol and all(
        abs(p[i]) < tol for i in range(10) if i != 0
    )

    # Support checks
    off_4core_mass = sum(p[i] for i in range(10) if i not in {0, 7, 8, 9})
    is_4core_supported = off_4core_mass < tol

    off_2core_mass = sum(p[i] for i in range(10) if i not in {0, 7})
    is_2core_supported = off_2core_mass < tol

    # Universal 4-core attractor match
    target = UNIVERSAL_4CORE_ATTRACTOR
    matches_universal = is_4core_supported and all(
        abs(p[i] - target[i]) < tol for i in target
    )

    # H/Br residual
    if p[8] > 1e-10:
        h_over_br = p[7] / p[8]
        h_over_br_resid = abs(h_over_br - H_OVER_BR_EXACT)
    else:
        h_over_br_resid = float("inf")

    # Layer classification (most specific first)
    if is_harmony:
        layer = "1-core"
    elif is_void:
        layer = "void-degenerate"
    elif matches_universal:
        layer = "4-core-attractor"
    elif is_2core_supported:
        layer = "2-core"
    elif is_4core_supported:
        layer = "4-core-supported"
    else:
        # Off the attractor structure -- transient or random
        layer = "transient"

    return AttractorState(
        is_universal_4core=matches_universal,
        is_harmony_attractor=is_harmony,
        is_void_degenerate=is_void,
        is_4core_supported=is_4core_supported,
        is_2core_supported=is_2core_supported,
        h_over_br_residual=h_over_br_resid,
        layer=layer,
    )


# ----- structural facts (for downstream code) -----

def universal_attractor_distribution() -> List[float]:
    """The canonical universal 4-core attractor as a 10-vector.

    Per WP115 D65 / WP105 D38: this is the unique non-trivial T+B-mix
    fixed point at alpha = 1/2 on Z/10Z.
    """
    p = [0.0] * 10
    for i, val in UNIVERSAL_4CORE_ATTRACTOR.items():
        p[i] = val
    # Re-normalize to be safe (the rounded values sum to ~1.0 - epsilon)
    s = sum(p)
    return [x / s for x in p]


def closed_form_h_over_br() -> float:
    """The closed-form value H/Br = 1 + sqrt(3) at the universal
    attractor (WP105 D39, exact).
    """
    return H_OVER_BR_EXACT


def joint_chain_shells() -> List[List[int]]:
    """The 7-element joint TSML+BHML closed-subset chain (WP115 D64).

    Returned as a list of 7 lists, in chain order (subset inclusion):
    {V} -> {V,H,Br,R} -> {V,Ch,H,Br,R} -> {V,Ba,Ch,H,Br,R} ->
    {V,P,Co,Ba,Ch,H,Br,R} -> {V,C,P,Co,Ba,Ch,H,Br,R} -> full.
    """
    return [
        [0],
        [0, 7, 8, 9],
        [0, 6, 7, 8, 9],
        [0, 5, 6, 7, 8, 9],
        [0, 3, 4, 5, 6, 7, 8, 9],
        [0, 2, 3, 4, 5, 6, 7, 8, 9],
        list(range(10)),
    ]
