"""
Invariants aggregator: every checkable claim from the makeover spec.

Each invariant is a (name, predicate, expected, actual, pass) tuple.
This module is the single place to ask "is the substrate intact?".
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .cl import CL, cell_counts, is_associative, is_commutative, non_associative_rate
from .lenses import BHML, TSML, doing_disagreement_rate
from .lens_family import (BHML_4, BHML_8_chain, BHML_8_YM, BHML_10,
                          TSML_4, TSML_8_chain, TSML_10,
                          TSML_FAMILY, BHML_FAMILY)
from .paths import crossing_census
from .tables import (HARMONY_44, CYCLE_A_36, SKELETON_22, DISAGREE_71,
                     TSML_HARMONY_73, harmony_44_summary, cycle_a_36_summary,
                     skeleton_22_summary, being_shell_72_summary)
from .triadic import (CONSERVATION_TETRAD, MANIFESTATION_HEXAD,
                      CYCLE_A, CYCLE_B, FOUR_CORE, is_bridge_consistent)


@dataclass(frozen=True)
class Invariant:
    name: str
    expected: object
    actual: object
    passed: bool
    note: str = ""

    def line(self) -> str:
        mark = "OK" if self.passed else "FAIL"
        return f"  [{mark:4s}] {self.name:55s} expected={self.expected!r:20s} actual={self.actual!r}"


def _check(name: str, expected, actual, note: str = "") -> Invariant:
    return Invariant(name=name, expected=expected, actual=actual,
                     passed=(expected == actual), note=note)


def all_invariants() -> list[Invariant]:
    invs: list[Invariant] = []

    # CL ground truth
    cl_counts = cell_counts(CL)
    invs.append(_check("CL.HARMONY_count == 73", 73, cl_counts.get(7, 0)))
    invs.append(_check("CL.VOID_count == 17", 17, cl_counts.get(0, 0)))
    other = sum(c for op, c in cl_counts.items() if op not in (0, 7))
    invs.append(_check("CL.other_count == 10", 10, other))
    invs.append(_check("CL is commutative (after upper-tri symmetrization)",
                       True, is_commutative(CL)))
    invs.append(_check("CL non-associative", False, is_associative(CL)))
    invs.append(_check("CL non-assoc rate == 12.8%", "12.8%",
                       f"{100*non_associative_rate(CL):.1f}%"))

    # Triadic structure
    invs.append(_check("Conservation Tetrad == {0,3,8,9}",
                       frozenset({0, 3, 8, 9}), CONSERVATION_TETRAD))
    invs.append(_check("Manifestation Hexad == {1,2,4,5,6,7}",
                       frozenset({1, 2, 4, 5, 6, 7}), MANIFESTATION_HEXAD))
    invs.append(_check("Cycle A {1,6,4} sum == 11 (WOBBLE)",
                       11, sum(CYCLE_A)))
    invs.append(_check("Cycle B {7,5,2} sum == 14 (2*HARMONY = dim G_2)",
                       14, sum(CYCLE_B)))
    invs.append(_check("4-core == {0,7,8,9} (Conservation XOR PROGRESS<->HARMONY)",
                       True, is_bridge_consistent()))

    # Tables
    h44 = harmony_44_summary()
    invs.append(_check("HARMONY_44 BEING(HARMONY) cell count == 28",
                       28, h44["BEING(HARMONY)"]))
    invs.append(_check("HARMONY_44 DOING(HARMONY) cell count == 11",
                       11, h44["DOING(HARMONY)"]))
    invs.append(_check("HARMONY_44 BECOMING(HARMONY) cell count == 5",
                       5, h44["BECOMING(HARMONY)"]))
    invs.append(_check("HARMONY_44 total == 44", 44, h44["TOTAL"]))

    ca36 = cycle_a_36_summary()
    invs.append(_check("CYCLE_A_36 LATTICE cells == 2", 2, ca36[1]))
    invs.append(_check("CYCLE_A_36 COLLAPSE cells == 9", 9, ca36[4]))
    invs.append(_check("CYCLE_A_36 CHAOS cells == 25", 25, ca36[6]))
    invs.append(_check("CYCLE_A_36 total == 36", 36, ca36["TOTAL"]))

    sk22 = skeleton_22_summary()
    invs.append(_check("SKELETON_22 VOID-boundary == 16",
                       16, sk22["VOID-boundary"]))
    invs.append(_check("SKELETON_22 PROGRESS-bump == 4",
                       4, sk22["PROGRESS-bump"]))
    invs.append(_check("SKELETON_22 COLLAPSE-bump == 2",
                       2, sk22["COLLAPSE-bump"]))
    invs.append(_check("SKELETON_22 total == 22", 22, sk22["TOTAL"]))

    bs72 = being_shell_72_summary()
    invs.append(_check("FIELD WOBBLE: |TSML - BHML| disagreement == 71",
                       71, bs72["n_disagreement_cells"]))
    invs.append(_check("BEING shell: TSML.HARMONY - 1 == 72",
                       72, bs72["tsml_harmony_minus_1"]))
    invs.append(_check("TSML HARMONY count == 73",
                       73, bs72["tsml_harmony_count"]))

    # Lens family
    invs.append(_check("BHML_10.det == -7002", -7002.0, BHML_10.det))
    invs.append(_check("BHML_8_YM.det == +70 (Yang-Mills core)",
                       70.0, BHML_8_YM.det))
    invs.append(_check("BHML_10 49.8% non-assoc",
                       "49.8%", f"{100*BHML_10.non_assoc_rate:.1f}%"))
    invs.append(_check("BHML_10 28 HARMONY cells", 28, BHML_10.harmony_count))
    invs.append(_check("TSML_10 73 HARMONY cells", 73, TSML_10.harmony_count))

    # DOING table
    rate = doing_disagreement_rate()
    invs.append(_check("DOING disagreement rate ~ 71% (~ T*)",
                       "71.0%", f"{100*rate:.1f}%"))

    # CL crossings == non-assoc rate
    cc = crossing_census(CL)
    invs.append(_check("CL crossing census == 128 / 1000 triples",
                       128, cc["n_crossings"]))

    return invs


def report() -> str:
    invs = all_invariants()
    n_pass = sum(1 for i in invs if i.passed)
    n_total = len(invs)
    lines = [
        "=" * 78,
        f"FOUNDATIONS INVARIANTS  ({n_pass}/{n_total} passed)",
        "=" * 78,
        "",
    ]
    lines.extend(i.line() for i in invs)
    lines.append("")
    lines.append("=" * 78)
    if n_pass == n_total:
        lines.append("ALL INVARIANTS PASS -- substrate intact per _CK_MEMORY_MAKEOVER spec.")
    else:
        lines.append(f"{n_total - n_pass} INVARIANT(S) FAIL -- review above.")
    lines.append("=" * 78)
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())
