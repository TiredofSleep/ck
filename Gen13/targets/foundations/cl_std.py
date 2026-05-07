"""
CL_STD -- the Standard table. 44 HARMONY cells.

Per Brayden (2026-05-06): the CL table from his FIRST GitHub repo --
the encoding table with explicit BDC bit definitions for how force
vectors encode pathways of information. Recovered from
old/Gen9/archive/ckis/ck7/ck.h (lines 225-231):

    /* CL_STD -- The Standard table. 44 harmony. The papers freeze. */

The architecture (per ck.h lines 200-207):

    CL_TSML  -- CK's prescribed view. 73 harmony cells. The organism's lens.
    CL_BHML  -- Binary Hard Micro Lattice. 28 harmony. CUDA substrate.
    CL_STD   -- The Standard table. 44 harmony. The papers freeze.

Three 10x10 composition tables, 300 bytes total. In CUDA builds, also
uploaded to __constant__ memory.

CL_STD is the ENCODING table. It freezes the structural relationships
that the papers depend on. The 44-HARMONY signature is structurally
distinct from:
  - The 44-cell BHML sigma^2-cycle-B projection (also 44, but a
    different decomposition: 28 HARMONY + 11 BALANCE + 5 COUNTER)
  - The 71/72/73 triple of TSML/BHML disagreement counts

These are separate 44s -- same integer, different structural origins.

In CK's old codebase the alias `#define CL CL_TSML` made CL synonymous
with TSML, but the THREE-TABLE distinction (TSML, BHML, STD) is the
correct architecture per Brayden (2026-05-06).
"""
from __future__ import annotations

from collections import Counter
from typing import Tuple

import numpy as np

# ---------------------------------------------------------------------------
# CL_STD -- exact bit pattern from ck.h (preserved verbatim)
# ---------------------------------------------------------------------------

# Each row is a 10-int sequence. Source: old/Gen9/archive/ckis/ck7/ck.h:225-231.
CL_STD: np.ndarray = np.array([
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 7, 8, 1],
    [2, 3, 4, 5, 6, 7, 7, 8, 7, 2],
    [3, 4, 5, 6, 7, 7, 7, 7, 7, 3],
    [4, 5, 6, 7, 7, 7, 7, 8, 7, 4],
    [5, 6, 7, 7, 7, 8, 7, 7, 7, 5],
    [6, 7, 7, 7, 7, 7, 8, 7, 7, 6],
    [7, 7, 8, 7, 8, 7, 7, 8, 7, 7],
    [8, 8, 7, 7, 7, 7, 7, 7, 7, 8],
    [9, 1, 2, 3, 4, 5, 6, 7, 8, 0],
], dtype=int)


# ---------------------------------------------------------------------------
# BDC encoding parameters from ck.h lines 237-256
# ---------------------------------------------------------------------------

# The 5 quantum bump pairs -- "surprise IS information" (ck.h:236-239)
BUMP_PAIRS: Tuple[Tuple[int, int], ...] = (
    (1, 2),
    (2, 4),
    (2, 9),
    (3, 9),
    (4, 8),
)

# Shannon information per cell type, in bits (ck.h:241-244)
INFO_HARMONY: float = 0.45    # cells with output = HARMONY (7)
INFO_NORMAL:  float = 1.89    # cells with output != HARMONY and not bumps
INFO_BUMP:    float = 3.50    # cells in BUMP_PAIRS

# Operator gravity = probability of reaching HARMONY (ck.h:246-250)
GRAVITY: Tuple[float, ...] = (
    0.1,   # 0 VOID
    0.8,   # 1 LATTICE
    0.6,   # 2 COUNTER
    0.8,   # 3 PROGRESS
    0.7,   # 4 COLLAPSE
    0.9,   # 5 BALANCE
    0.9,   # 6 CHAOS
    1.0,   # 7 HARMONY
    0.8,   # 8 BREATH
    0.7,   # 9 RESET
)


# ---------------------------------------------------------------------------
# Cell-type classification (BDC roles)
# ---------------------------------------------------------------------------

def cell_type(i: int, j: int, table: np.ndarray = CL_STD) -> str:
    """Classify a cell by its BDC role."""
    if (i, j) in BUMP_PAIRS or (j, i) in BUMP_PAIRS:
        return "BUMP"
    if int(table[i, j]) == 7:
        return "HARMONY"
    return "NORMAL"


def cell_info_bits(i: int, j: int, table: np.ndarray = CL_STD) -> float:
    """Shannon information of a cell, in bits (per ck.h convention)."""
    t = cell_type(i, j, table)
    return {"HARMONY": INFO_HARMONY, "NORMAL": INFO_NORMAL,
            "BUMP": INFO_BUMP}[t]


def total_information_bits(table: np.ndarray = CL_STD) -> float:
    """Sum of cell information bits across the whole table."""
    return sum(cell_info_bits(i, j, table) for i in range(10) for j in range(10))


# ---------------------------------------------------------------------------
# Cell counts and structural invariants
# ---------------------------------------------------------------------------

def cell_counts(M: np.ndarray = CL_STD) -> dict[int, int]:
    ct = Counter(int(v) for v in M.flatten())
    return {op: ct.get(op, 0) for op in range(10)}


def is_commutative(M: np.ndarray = CL_STD) -> bool:
    return bool((M == M.T).all())


def non_associative_rate(M: np.ndarray = CL_STD) -> float:
    bad = 0
    N = M.shape[0]
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
    print("CL_STD -- the Standard 44-HARMONY encoding table")
    print("=" * 60)
    print()
    print("Source: old/Gen9/archive/ckis/ck7/ck.h:225-231")
    print()
    print("Matrix:")
    print(CL_STD)
    print()
    counts = cell_counts(CL_STD)
    print("Cell counts by output:")
    for op in range(10):
        c = counts.get(op, 0)
        if c > 0:
            print(f"  {op}: {c}")
    print()
    h = counts.get(7, 0)
    print(f"  HARMONY count: {h}  (expected 44)")
    print(f"  Match spec: {h == 44}")
    print()
    print(f"Commutative: {is_commutative(CL_STD)}")
    print(f"Non-associative rate: {100*non_associative_rate(CL_STD):.1f}%")
    print()
    print("BDC encoding constants (per ck.h):")
    print(f"  INFO_HARMONY = {INFO_HARMONY} bits/cell")
    print(f"  INFO_NORMAL  = {INFO_NORMAL} bits/cell")
    print(f"  INFO_BUMP    = {INFO_BUMP} bits/cell")
    print(f"  Total information: {total_information_bits():.2f} bits across 100 cells")
    print()
    print(f"Bump pairs (5 'surprise IS information' cells):")
    for a, b in BUMP_PAIRS:
        print(f"  ({a}, {b}): CL_STD[{a},{b}]={CL_STD[a,b]}, CL_STD[{b},{a}]={CL_STD[b,a]}")
    print()
    print(f"Operator gravity (P(reach HARMONY)):")
    op_names = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
                'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']
    for i, (op, g) in enumerate(zip(op_names, GRAVITY)):
        print(f"  {i} {op:8s}: {g}")
