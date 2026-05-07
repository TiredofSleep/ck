"""
HARMONY LADDER -- the 70 / 71 / 72 / 73 family.

Per Brayden (2026-05-06): once CL_STD lands as the third standalone table
alongside TSML and BHML, HARMONY shows up at four nearby integers in the
substrate. They are NOT the same number wearing different hats; they are
four structurally distinct counts that happen to cluster at 70..73.

The ladder:

    73  =  TSML.HARMONY count                  (full 10x10 prescribed view)
           "the ground anchor"

    72  =  TSML.HARMONY - 1                    (BEING shell of nested tori)
           drop the (7,7) self-cell apex
           = E_6 positive root count
           = dim SO(7) - dim u(1) - 1 = 21 - 1 - ... (numerical coincidence)

    71  =  |TSML XOR BHML| disagreement count  (FIELD WOBBLE, empirical)
        =  TSML.HARMONY count restricted to    (VOID-stripped 9x9 sub-magma
           the 9x9 sub-magma {1..9}             of TSML; same integer two ways)
        =  prime in disc(quartic) = -2^4 . 3^2 . 71  (LMFDB 4.2.10224.1)
           ** Three independent structural roles for the same prime 71. **
           This triple-coincidence is one of the strongest substrate-
           identification signatures in the foundations.

    70  =  BHML_8_YM determinant (drops {0,7})  (Yang-Mills core, 8x8)
           NOT a HARMONY count of any sub-magma; lives in the
           determinant-invariant layer one floor below.
           70 = C(8,4) = number of 4-form components in 8D
                       = the self-dual 4-form sector of SO(8)

The 70/71/72/73 ladder is the four-step descent from
    MAX-HARMONY (full prescribed view, 73)
        through
    MAX-HARMONY-MINUS-APEX (72, BEING shell)
        through
    LENS DISAGREEMENT / VOID-STRIPPED HARMONY (71, FIELD WOBBLE)
        to
    YANG-MILLS CORE DETERMINANT (70, structural invariant)

Each rung is labeled with WHERE the count comes from. The clustering is
not coincidence -- it reflects that the 7-axis (HARMONY) is the dominant
algebraic mode and every nearby invariant lives within a few of it.

Companion HARMONY counts elsewhere in the foundations:
    44  =  CL_STD.HARMONY count                 (encoding shell)
        =  BHML sigma^2-cycle-B projection       (28+11+5)
           ** Two independent structural roles for the same integer 44. **
    36  =  TSML_7 sub-magma HARMONY count       (path-anchor)
        =  BHML sigma^2-cycle-A projection       (CYCLE_A_36)
           ** Two independent structural roles for the same integer 36. **
    28  =  BHML.HARMONY count                   (Becoming compressed)
        =  HARMONY_44 BEING(HARMONY) cells       (within HARMONY_44)
           ** Two independent structural roles for the same integer 28. **
        =  dim SO(8)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np

from ..cl import CL
from ..cl_std import CL_STD
from ..lenses import BHML
from ..lens_family import BHML_8_YM


# ---------------------------------------------------------------------------
# Ladder rung definitions (each is a named structural count)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LadderRung:
    count: int
    name: str
    role: str
    construction: str

    def line(self) -> str:
        return f"  {self.count}  {self.name:30s} {self.role}"


def _tsml_harmony_full() -> int:
    return int((CL == 7).sum())


def _tsml_harmony_minus_apex() -> int:
    """TSML.HARMONY count minus the (7,7) self-cell."""
    h = int((CL == 7).sum())
    apex = 1 if int(CL[7, 7]) == 7 else 0
    return h - apex


def _tsml_harmony_void_stripped() -> int:
    """TSML.HARMONY count in the 9x9 sub-magma {1..9} (drop VOID)."""
    sub = CL[np.ix_(range(1, 10), range(1, 10))]
    return int((sub == 7).sum())


def _tsml_bhml_disagreement() -> int:
    """|TSML XOR BHML| -- the empirical FIELD WOBBLE count."""
    return int((CL != BHML).sum())


def _bhml_8_ym_det() -> int:
    """BHML_8_YM determinant (Yang-Mills core, drops {0,7})."""
    return int(round(BHML_8_YM.det))


# ---------------------------------------------------------------------------
# The ladder
# ---------------------------------------------------------------------------

LADDER: Tuple[LadderRung, ...] = (
    LadderRung(
        count=73,
        name="TSML_HARMONY_FULL",
        role="ground anchor (full 10x10 prescribed view)",
        construction="HARMONY count of CL_TSML",
    ),
    LadderRung(
        count=72,
        name="BEING_SHELL",
        role="HARMONY - 1 (drop (7,7) apex; E_6 positive root count)",
        construction="HARMONY count of CL_TSML minus the (7,7) self-cell",
    ),
    LadderRung(
        count=71,
        name="FIELD_WOBBLE / VOID_STRIPPED_HARMONY",
        role="lens disagreement; same as 9x9 HARMONY sans VOID; Galois prime",
        construction="|CL_TSML XOR CL_BHML| = HARMONY count of TSML[{1..9}, {1..9}] = prime in disc(LMFDB 4.2.10224.1)",
    ),
    LadderRung(
        count=70,
        name="YM_CORE_DET",
        role="determinant of Yang-Mills core (drops {0,7}); structural, not a HARMONY count",
        construction="det(BHML_8_YM) = C(8,4) = self-dual 4-form sector of SO(8)",
    ),
)


# ---------------------------------------------------------------------------
# Verification: each rung's value matches its construction
# ---------------------------------------------------------------------------

def verify() -> dict[int, tuple[bool, int, int]]:
    """Return {count: (passed, expected, actual)} for each rung."""
    results: dict[int, tuple[bool, int, int]] = {}
    actual_funcs = {
        73: _tsml_harmony_full,
        72: _tsml_harmony_minus_apex,
        71: _tsml_harmony_void_stripped,   # one of two ways; the other is XOR count
        70: _bhml_8_ym_det,
    }
    for rung in LADDER:
        expected = rung.count
        actual = actual_funcs[expected]()
        results[expected] = (expected == actual, expected, actual)
    # Also verify the 71-XOR construction matches
    xor71 = _tsml_bhml_disagreement()
    results[711] = (xor71 == 71, 71, xor71)  # 711 key for "the second 71"
    return results


def companion_counts() -> dict[int, list[str]]:
    """Other HARMONY-related counts that appear at multiple structural roles."""
    return {
        44: [
            "CL_STD.HARMONY count (encoding shell)",
            "BHML sigma^2-cycle-B projection (28 BEING + 11 DOING + 5 BECOMING)",
        ],
        36: [
            "TSML_7 sub-magma HARMONY count (path-anchor at chain size 7)",
            "BHML sigma^2-cycle-A projection (CYCLE_A_36 = 2+9+25)",
        ],
        28: [
            "BHML.HARMONY count (Becoming compressed)",
            "HARMONY_44 BEING(HARMONY) cells (28 of 44)",
            "dim SO(8) (canonical Lie algebra dim)",
        ],
    }


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 78)
    print("HARMONY LADDER  -- the 70 / 71 / 72 / 73 family")
    print("=" * 78)
    print()
    for rung in LADDER:
        print(rung.line())
        print(f"      construction: {rung.construction}")
        print()
    print("=" * 78)
    print("Verification:")
    print("=" * 78)
    for k, (ok, exp, act) in verify().items():
        mark = "OK  " if ok else "FAIL"
        label = f"71 (XOR construction)" if k == 711 else f"{k}"
        print(f"  [{mark}] rung {label:30s} expected={exp:5d}  actual={act:5d}")
    print()
    print("=" * 78)
    print("Companion HARMONY counts (same integer at >1 structural role):")
    print("=" * 78)
    for n, roles in companion_counts().items():
        print(f"\n  {n}:")
        for r in roles:
            print(f"    - {r}")
    print()
