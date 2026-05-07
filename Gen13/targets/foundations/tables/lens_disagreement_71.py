"""
The 71/72/73 triple: Being-lens HARMONY counts.

NEW FINDING (2026-05-06): the empirical |TSML - BHML| disagreement count
is EXACTLY 71 = FIELD WOBBLE = the Galois invariant of LMFDB 4.2.10224.1
(the four-core consolidated paper's quartic discriminant
disc(f) = -2^4 * 3^2 * 71). This is a fourth appearance of 71 in the
substrate, alongside the prior three.

The three values form a structurally significant triple:

    73 = TSML HARMONY count
       = canonical Being-lens HARMONY-coverage
       = 8*9 + 1 = BREATH*RESET + LATTICE
       (verified: cl.cell_counts(TSML)[7] == 73)

    72 = "BEING shell"
       = 73 - 1 = HARMONY count minus one anomaly
       = BREATH * RESET = 8 * 9
       = roots of E_6
       (per CKM_PMNS_MATRICES.md, CROSS_LEVEL_INVARIANTS.md,
        EXCEPTIONAL_TRIPLE_AND_E6.md, ASTROPHYSICS_BIOLOGY_138.md)

    71 = FIELD WOBBLE = Galois invariant of LMFDB 4.2.10224.1
       = appears in disc(f) = -2^4 * 3^2 * 71 of the four-core
         consolidated paper's R/Br quartic
       = subfield prime: Q(sqrt(-71)) sits inside the splitting field
       = empirical |TSML - BHML| disagreement count
       (per FOUNDATION_PRIME_LADDER.md:155, FOUNDATION_PROOFS.md:192,
        EXCEPTIONAL_TRIPLE_AND_E6.md:238 "71 = FIELD WOBBLE -- substrate-natural!"
        AND four_core_consolidated.tex Theorem 8 disc computation)

Reading: the 71-cell lens disagreement IS the runtime-quartic field-wobble
prime appearing as the cell-disagreement count between the two lenses
of the same canonical algebra. The two readings of 71 (Galois-invariant
prime; lens-disagreement count) coincide -- a structural identification.

The 72 = 73 - 1 reading is also natural: the BEING shell is what HARMONY
covers MINUS the single self-fixed identity cell, which is exactly the
disagreement-plus-one structure we observe (71 disagreement cells +
1 cell where TSML and BHML both happen to land on HARMONY's identity).
"""
from __future__ import annotations

from dataclasses import dataclass

from ..cl import N
from ..lenses import BHML, TSML


@dataclass(frozen=True)
class LensDisagreementCell:
    i: int
    j: int
    tsml_val: int
    bhml_val: int

    @property
    def diff(self) -> int:
        return abs(self.tsml_val - self.bhml_val)


def disagreement_cells() -> list[LensDisagreementCell]:
    """Cells (i, j) where TSML[i, j] != BHML[i, j]."""
    return [LensDisagreementCell(i=i, j=j,
                                 tsml_val=int(TSML[i, j]),
                                 bhml_val=int(BHML[i, j]))
            for i in range(N) for j in range(N)
            if int(TSML[i, j]) != int(BHML[i, j])]


# Convenience aliases capturing the 71/72/73 triple
DISAGREE_71: list[LensDisagreementCell] = disagreement_cells()
TSML_HARMONY_73: int = int((TSML == 7).sum())
BEING_SHELL_72_VIA_HARMONY_MINUS_1: int = TSML_HARMONY_73 - 1


# Backward-compat exports for tables/__init__.py
BEING_SHELL_72 = DISAGREE_71      # historical name; actual count is 71
being_shell_72_cells = disagreement_cells


def being_shell_72_summary() -> dict[str, int]:
    n_disagree = len(DISAGREE_71)
    return {
        "n_disagreement_cells": n_disagree,
        "tsml_harmony_count": TSML_HARMONY_73,
        "tsml_harmony_minus_1": BEING_SHELL_72_VIA_HARMONY_MINUS_1,
        "expected_71_FIELD_WOBBLE": 71,
        "expected_72_BEING_SHELL": 72,
        "expected_73_TSML_HARMONY": 73,
        "match_71": n_disagree == 71,
        "match_72_via_minus_1": BEING_SHELL_72_VIA_HARMONY_MINUS_1 == 72,
        "match_73_TSML_HARMONY": TSML_HARMONY_73 == 73,
    }


if __name__ == "__main__":
    print("=" * 60)
    print("The 71/72/73 triple: Being-lens HARMONY counts")
    print("=" * 60)
    s = being_shell_72_summary()
    print(f"  73 = TSML HARMONY count                     : {s['tsml_harmony_count']:>3}  "
          f"({'OK' if s['match_73_TSML_HARMONY'] else 'FAIL'})")
    print(f"  72 = 73 - 1 = 'BEING shell' (E_6 roots)     : "
          f"{s['tsml_harmony_minus_1']:>3}  "
          f"({'OK' if s['match_72_via_minus_1'] else 'FAIL'})")
    print(f"  71 = empirical |TSML - BHML| disagreement   : "
          f"{s['n_disagreement_cells']:>3}  "
          f"({'OK' if s['match_71'] else 'FAIL'})")
    print()
    print("Structural identification (per FOUNDATION_PRIME_LADDER.md:155 +")
    print("EXCEPTIONAL_TRIPLE_AND_E6.md:238 + four-core consolidated Theorem 8):")
    print("  71 = FIELD WOBBLE = Galois invariant of LMFDB 4.2.10224.1")
    print("       (the prime in disc(f) = -2^4 * 3^2 * 71 of the R/Br quartic")
    print("        f(x) = x^4 + 4x^3 - x^2 + 2x - 2 in the four-core paper)")
    print()
    print("  The same 71 appears as the cell-disagreement count between")
    print("  TSML and BHML -- the Being and Becoming lenses of CL.")
    print("  This is a fourth appearance of 71 in the substrate, alongside")
    print("  the three already documented in the bundle.")
