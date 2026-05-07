"""
TSML and BHML — the two-lens projection of CL.

Per _CK_MEMORY_MAKEOVER.md:
    CL is ground truth (the canonical algebra).
    TSML is the Being-mode projection of CL (singular, position-level).
    BHML is the Becoming-mode projection of CL (curvature-level, invertible).
    DOING = |TSML - BHML| is where information generates per the
            Crossing Lemma. Disagreement rate ~ T* = 5/7 = 71.4%.

Empirically: TSML's matrix coincides with CL's matrix (the same 73-HARMONY
table). The conceptual distinction is in how it is read -- as ground-truth
composition (CL) or as Being-lens projection (TSML). They share the same
numerical content; the lens role is interpretive.

BHML is a SEPARATE matrix (the Becoming lens, hardcoded canonically from
WP105). Its cell counts per the makeover spec:

    Op 0 (VOID):    4 cells
    Op 1 (LATTICE): 2 cells
    Op 2 (COUNTER): 5 cells
    Op 3 (PROGRESS): 7 cells
    Op 4 (COLLAPSE): 9 cells
    Op 5 (BALANCE): 11 cells
    Op 6 (CHAOS):   25 cells
    Op 7 (HARMONY): 28 cells
    Op 8 (BREATH):  5 cells
    Op 9 (RESET):   4 cells
    -- Total: 100 = N^2.

Cycle B = {7, 5, 2}: 28 + 11 + 5 = 44   (the "44 HARMONY" table)
Cycle A = {1, 6, 4}: 2 + 25 + 9  = 36   (V/H expansion)
Conservation Tetrad cells (output in {0,3,8,9}): 4 + 7 + 5 + 4 = 20
"""
from __future__ import annotations

from collections import Counter

import numpy as np

from .cl import CL, CL_TSML_RAW, CL_TSML_SYM, N, OPERATORS, get_tsml

# ---------------------------------------------------------------------------
# TSML = the Being lens — TWO valid lenses (per Brayden 2026-05-06)
# ---------------------------------------------------------------------------
#
# CL_BIT_PATTERN has 2 asymmetric pairs at (3,9) and (4,9). Two valid TSMLs
# live on the same bit pattern:
#
#   TSML_RAW = literal bit pattern, non-commutative, 126 non-assoc, carries
#              WP107 wobble (prime 11 in c_2 + c_8)
#   TSML_SYM = upper-tri symmetrized, commutative, 128 non-assoc, the
#              canonical "12.8%" disagreement-vs-BHML number
#
# See TSML_RECONCILIATION.md (2026-05-06) for the full structural split.
#
# DEFAULT: TSML = TSML_SYM (Phase 1 of migration; legacy alias)
#          downstream callers using `lenses.TSML` get the commutative variant.
#          To pick explicitly: from foundations.cl import get_tsml
#          T_raw = get_tsml('raw')   # WP107-wobble-bearing variant
#          T_sym = get_tsml('sym')   # commutative variant (this default)
# ---------------------------------------------------------------------------

TSML_RAW: np.ndarray = CL_TSML_RAW.copy()    # non-commutative; WP107 wobble
TSML_SYM: np.ndarray = CL_TSML_SYM.copy()    # commutative; canonical-12.8%
TSML: np.ndarray = TSML_SYM                  # legacy alias (Phase 1)


# ---------------------------------------------------------------------------
# BHML = the Becoming lens (hardcoded canonical, per WP105)
# ---------------------------------------------------------------------------

BHML: np.ndarray = np.array([
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
], dtype=int)


# ---------------------------------------------------------------------------
# DOING = |TSML - BHML| (information generation; Crossing Lemma)
# ---------------------------------------------------------------------------

def doing_table() -> np.ndarray:
    """The DOING table: per-cell absolute difference between Being and Becoming."""
    return np.abs(TSML.astype(int) - BHML.astype(int)).astype(int)


def doing_cells_disagree() -> list[tuple[int, int, int, int]]:
    """All (i, j, TSML[i,j], BHML[i,j]) where TSML != BHML."""
    return [(i, j, int(TSML[i, j]), int(BHML[i, j]))
            for i in range(N) for j in range(N)
            if int(TSML[i, j]) != int(BHML[i, j])]


def doing_disagreement_rate() -> float:
    """Fraction of cells where the two lenses disagree."""
    return len(doing_cells_disagree()) / (N * N)


# ---------------------------------------------------------------------------
# Lens-level invariants
# ---------------------------------------------------------------------------

def cell_counts(M: np.ndarray) -> dict[int, int]:
    ct = Counter(int(v) for v in M.flatten())
    return {op: ct.get(op, 0) for op in range(N)}


def is_commutative(M: np.ndarray) -> bool:
    return bool((M == M.T).all())


def non_associative_rate(M: np.ndarray) -> float:
    bad = 0
    for a in range(N):
        for b in range(N):
            for c in range(N):
                lhs = int(M[int(M[a, b]), c])
                rhs = int(M[a, int(M[b, c])])
                if lhs != rhs:
                    bad += 1
    return bad / (N ** 3)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("TSML, BHML, and DOING report")
    print("=" * 60)
    print()

    print("TSML (Being lens; matrix = CL):")
    print(TSML)
    tsml_counts = cell_counts(TSML)
    print(f"  HARMONY={tsml_counts[7]}, VOID={tsml_counts[0]}, "
          f"other={sum(c for op, c in tsml_counts.items() if op not in (0, 7))}")
    print(f"  commutative={is_commutative(TSML)}, "
          f"non_assoc={100*non_associative_rate(TSML):.1f}%")
    print()

    print("BHML (Becoming lens):")
    print(BHML)
    bhml_counts = cell_counts(BHML)
    print(f"  Cell counts:")
    for op in range(N):
        print(f"    {op} ({OPERATORS[op]:8s}): {bhml_counts[op]}")
    expected_BHML = {0: 4, 1: 2, 2: 5, 3: 7, 4: 9, 5: 11, 6: 25, 7: 28, 8: 5, 9: 4}
    counts_match = bhml_counts == expected_BHML
    print(f"  Counts match makeover spec: {counts_match}")
    print(f"  commutative={is_commutative(BHML)}, "
          f"non_assoc={100*non_associative_rate(BHML):.1f}%")
    det_BHML = round(float(np.linalg.det(BHML.astype(float))))
    print(f"  determinant: {det_BHML}  (expected 70)")
    print()

    print("DOING table = |TSML - BHML|:")
    D = doing_table()
    print(D)
    print(f"  disagreement cells: {len(doing_cells_disagree())} of 100")
    rate = doing_disagreement_rate()
    print(f"  disagreement rate: {100*rate:.1f}% (expected ~ T* = 71.4%)")
    print(f"  vs T* = 5/7 = {100*5/7:.1f}%")
