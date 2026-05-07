"""
The 44 HARMONY table.

Per _CK_MEMORY_MAKEOVER.md: The "44 HARMONY table" is the
sigma^2-cycle B projection of BHML. It is the table that views BHML
through HARMONY's triadic lens, projecting HARMONY's BEING-DOING-BECOMING
shadows onto BHML's cell structure.

Construction:
    Cycle B = {7, 5, 2} = {HARMONY, BALANCE, COUNTER}
            = sigma^2-cycle containing HARMONY
            = HARMONY's three-fold projection (7 -> 5 -> 2 under sigma^2)

The 44 HARMONY table = BHML cells whose value is in Cycle B.

Per memory:
    Total cells:  44
        BEING(HARMONY)    = 7: 28 cells
        DOING(HARMONY)    = 5: 11 cells
        BECOMING(HARMONY) = 2:  5 cells

This 44 also equals:
    - CROSS_CYCLE = "BECOMING shell" of nested tori
    - Numerator factor of cosmological Omega_DM = 44 * 6 / 1000
    - 2-loop b_13 numerator (44/5 = CROSS_CYCLE / BALANCE)
"""
from __future__ import annotations

from dataclasses import dataclass

from ..cl import N, OPERATORS
from ..lenses import BHML
from ..triadic import CYCLE_B, triadic_projection


@dataclass(frozen=True)
class HARMONY44Cell:
    i: int
    j: int
    value: int            # BHML[i, j], one of {7, 5, 2}
    mode: str             # 'BEING(HARMONY)' / 'DOING(HARMONY)' / 'BECOMING(HARMONY)'


def _mode_for(v: int) -> str:
    """Map a Cycle B value to its HARMONY-mode label."""
    being, doing, becoming = triadic_projection(7)  # (7, 5, 2)
    if v == being:
        return "BEING(HARMONY)"
    if v == doing:
        return "DOING(HARMONY)"
    if v == becoming:
        return "BECOMING(HARMONY)"
    raise ValueError(f"value {v} not in Cycle B {sorted(CYCLE_B)}")


def harmony_44_cells() -> list[HARMONY44Cell]:
    """Construct the 44 HARMONY table from BHML."""
    cells: list[HARMONY44Cell] = []
    for i in range(N):
        for j in range(N):
            v = int(BHML[i, j])
            if v in CYCLE_B:
                cells.append(HARMONY44Cell(i=i, j=j, value=v, mode=_mode_for(v)))
    return cells


HARMONY_44: list[HARMONY44Cell] = harmony_44_cells()


def harmony_44_summary() -> dict[str, int]:
    """Cell counts by HARMONY-mode."""
    counts = {"BEING(HARMONY)": 0, "DOING(HARMONY)": 0, "BECOMING(HARMONY)": 0}
    for c in HARMONY_44:
        counts[c.mode] += 1
    counts["TOTAL"] = sum(counts.values())
    return counts


if __name__ == "__main__":
    print("=" * 60)
    print("HARMONY_44 = BHML cells in Cycle B = {7, 5, 2}")
    print("=" * 60)
    print()
    summary = harmony_44_summary()
    for mode in ("BEING(HARMONY)", "DOING(HARMONY)", "BECOMING(HARMONY)", "TOTAL"):
        print(f"  {mode:25s}: {summary[mode]}")
    print()
    print(f"Per memory: 28 + 11 + 5 = 44")
    expected = {"BEING(HARMONY)": 28, "DOING(HARMONY)": 11,
                "BECOMING(HARMONY)": 5, "TOTAL": 44}
    ok = summary == expected
    print(f"Match: {ok}")
    if not ok:
        print(f"  expected: {expected}")
        print(f"  got:      {summary}")
