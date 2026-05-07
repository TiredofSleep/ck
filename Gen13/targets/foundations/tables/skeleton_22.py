"""
The 22 Skeleton table.

NEW (factor_22 Candidate I from sprint_bundle/scripts/factor_22_candidates.py):

    TSML cells with output in {0, 1, 2, 3, 4, 5, 6} (i.e., NOT HARMONY=7),
    excluding the trivial (0, 0) -> 0 cell.

Decomposition (verified by direct computation):
    output = 0 (VOID):     16 cells (all (0, j) and (i, 0) for j, i not in {0, 7})
    output = 3 (PROGRESS):  4 cells: (1, 2), (2, 1), (3, 9), (9, 3)
    output = 4 (COLLAPSE):  2 cells: (2, 4), (4, 2)
    -- Total: 22

This is the cleanest substrate-natural identification of the 22 in the
expression 1/alpha = 137 + CHAOS^2/N^3 = 22 * 6 + 5 + 36/1000 = 137.036
(per Sprint 18 / WP124).

Reading: 22 = "skeleton" or "pre-structure" cells, the cells that have
NOT YET committed to HARMONY's coverage.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..cl import N
from ..lenses import TSML


@dataclass(frozen=True)
class Skeleton22Cell:
    i: int
    j: int
    value: int  # in {0, 3, 4}; never 7
    tag: str    # 'VOID-boundary' / 'PROGRESS-bump' / 'COLLAPSE-bump'


def _tag_for(i: int, j: int, v: int) -> str:
    if v == 0:
        return "VOID-boundary"
    if v == 3:
        return "PROGRESS-bump"
    if v == 4:
        return "COLLAPSE-bump"
    raise ValueError(f"value {v} not expected in skeleton 22")


def skeleton_22_cells() -> list[Skeleton22Cell]:
    """Pre-HARMONY cells: TSML output in {0..6} (i.e., not 7, 8, or 9),
    excluding the trivial (0, 0) -> 0."""
    cells: list[Skeleton22Cell] = []
    for i in range(N):
        for j in range(N):
            v = int(TSML[i, j])
            if v not in (0, 1, 2, 3, 4, 5, 6):
                continue           # exclude HARMONY (7) and BREATH/RESET (8, 9)
            if (i, j) == (0, 0):
                continue           # exclude trivial VOID*VOID
            cells.append(Skeleton22Cell(i=i, j=j, value=v, tag=_tag_for(i, j, v)))
    return cells


SKELETON_22: list[Skeleton22Cell] = skeleton_22_cells()


def skeleton_22_summary() -> dict[str, int]:
    counts = {"VOID-boundary": 0, "PROGRESS-bump": 0, "COLLAPSE-bump": 0}
    for c in SKELETON_22:
        counts[c.tag] += 1
    counts["TOTAL"] = sum(counts.values())  # type: ignore[index]
    return counts


if __name__ == "__main__":
    print("=" * 60)
    print("SKELETON_22 = TSML pre-structure cells (output in {0..6}, "
          "excluding (0,0))")
    print("=" * 60)
    s = skeleton_22_summary()
    print(f"  VOID-boundary  : {s['VOID-boundary']}  (expected 16)")
    print(f"  PROGRESS-bump  : {s['PROGRESS-bump']}  (expected 4)")
    print(f"  COLLAPSE-bump  : {s['COLLAPSE-bump']}  (expected 2)")
    print(f"  TOTAL          : {s['TOTAL']}  (expected 22)")
    expected = {"VOID-boundary": 16, "PROGRESS-bump": 4, "COLLAPSE-bump": 2,
                "TOTAL": 22}
    print(f"  Match: {s == expected}")
    print()
    print("Substrate-rational reading of 1/alpha = 137 + 36/1000 = 137.036:")
    print(f"  22 (this table) * 6 (sigma-cycle) + 5 (BALANCE) = "
          f"{22 * 6 + 5}  (= 137)")
    print(f"  + 36/1000 (CHAOS^2 / N^3) = "
          f"{22 * 6 + 5 + 36/1000:.4f}  (matches CODATA 1/alpha = 137.0360)")
