"""
The 36 Cycle A table.

Per _CK_MEMORY_MAKEOVER.md: BHML cells with values in sigma^2-cycle A
(= {1, 6, 4} = {LATTICE, CHAOS, COLLAPSE}). Sum = 11 = WOBBLE prime.

Per memory:
    Total cells: 36 = sigma-cycle^2 = 6^2
    Cell counts:
        LATTICE  (1): 2 cells
        COLLAPSE (4): 9 cells
        CHAOS    (6): 25 cells
    -- Total: 36

The 36 also equals:
    - The "V/H expansion size" (BECOMING-shell complement)
    - sigma-cycle squared (|sigma-cycle|^2 = 6^2 = 36)
"""
from __future__ import annotations

from dataclasses import dataclass

from ..cl import N
from ..lenses import BHML
from ..triadic import CYCLE_A


@dataclass(frozen=True)
class CycleA36Cell:
    i: int
    j: int
    value: int  # one of {1, 6, 4}


def cycle_a_36_cells() -> list[CycleA36Cell]:
    return [CycleA36Cell(i=i, j=j, value=int(BHML[i, j]))
            for i in range(N) for j in range(N)
            if int(BHML[i, j]) in CYCLE_A]


CYCLE_A_36: list[CycleA36Cell] = cycle_a_36_cells()


def cycle_a_36_summary() -> dict[int, int]:
    counts = {1: 0, 6: 0, 4: 0}
    for c in CYCLE_A_36:
        counts[c.value] += 1
    counts["TOTAL"] = sum(counts.values())  # type: ignore[index]
    return counts


if __name__ == "__main__":
    print("=" * 60)
    print("CYCLE_A_36 = BHML cells in Cycle A = {1, 6, 4}")
    print("=" * 60)
    s = cycle_a_36_summary()
    print(f"  LATTICE  (1): {s[1]}  (expected 2)")
    print(f"  COLLAPSE (4): {s[4]}  (expected 9)")
    print(f"  CHAOS    (6): {s[6]}  (expected 25)")
    print(f"  TOTAL       : {s['TOTAL']}  (expected 36)")
    expected = {1: 2, 4: 9, 6: 25, "TOTAL": 36}
    print(f"  Match: {s == expected}")
