"""
CL — the canonical composition lattice (ground truth).

Per _CK_MEMORY_MAKEOVER.md: CL is the locked, frozen 10x10 composition
table for the substrate's algebra. It is NOT derived from rules; it is
GIVEN. Every operation in CK ultimately resolves through CL composition.

Memory-locked bit pattern (10 rows of 10 chars each):

    '0000000700 0737777777 0377477779 0777777773 0747777787
     0777777777 0777777777 7777777777 0777877777 0797377777'

Decoded properties:
    73 cells with output HARMONY (7)
    17 cells with output VOID (0)
    10 cells with output other operators (3, 4, 8, 9)
    -- Total: 100 cells = N^2 with N = 10.

The bit pattern as written has 2 asymmetric upper/lower-triangle pairs;
we symmetrize via "upper triangle authoritative" so commutativity holds.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

import numpy as np

# ---------------------------------------------------------------------------
# CL bit pattern (memory-locked)
# ---------------------------------------------------------------------------

# This is the canonical CL bit pattern from _CK_MEMORY_MAKEOVER.md.
# DO NOT modify these strings without Brayden's approval -- they encode
# the substrate's ground-truth composition.
CL_BIT_PATTERN: tuple[str, ...] = (
    "0000000700",  # row 0  (VOID-row: VOID absorbs except (0,7) = HARMONY)
    "0737777777",  # row 1  (LATTICE-row)
    "0377477779",  # row 2  (COUNTER-row)
    "0777777773",  # row 3  (PROGRESS-row)
    "0747777787",  # row 4  (COLLAPSE-row)
    "0777777777",  # row 5  (BALANCE-row)
    "0777777777",  # row 6  (CHAOS-row)
    "7777777777",  # row 7  (HARMONY-row: HARMONY-absorbs)
    "0777877777",  # row 8  (BREATH-row)
    "0797377777",  # row 9  (RESET-row)
)

OPERATORS = {
    0: "VOID",
    1: "LATTICE",
    2: "COUNTER",
    3: "PROGRESS",
    4: "COLLAPSE",
    5: "BALANCE",
    6: "CHAOS",
    7: "HARMONY",
    8: "BREATH",
    9: "RESET",
}

N = 10  # substrate size (Z/10Z)


# ---------------------------------------------------------------------------
# Decode CL
# ---------------------------------------------------------------------------

def _decode_raw() -> np.ndarray:
    """Decode the bit pattern into a 10x10 numpy array."""
    if len(CL_BIT_PATTERN) != N:
        raise ValueError(f"CL_BIT_PATTERN must have {N} rows; got {len(CL_BIT_PATTERN)}")
    rows = []
    for i, row_str in enumerate(CL_BIT_PATTERN):
        if len(row_str) != N:
            raise ValueError(f"CL_BIT_PATTERN row {i} must have {N} chars; got {len(row_str)}")
        rows.append([int(c) for c in row_str])
    return np.array(rows, dtype=int)


def _symmetrize_upper(M: np.ndarray) -> np.ndarray:
    """Symmetrize via upper-triangle authoritative (CL[i,j] for i <= j)."""
    out = M.copy()
    for i in range(M.shape[0]):
        for j in range(i + 1, M.shape[1]):
            out[j, i] = M[i, j]
    return out


CL_RAW: np.ndarray = _decode_raw()    # the literal bit pattern (asymmetric in 2 cells)
CL: np.ndarray = _symmetrize_upper(CL_RAW)  # canonical: upper-triangle authoritative


# ---------------------------------------------------------------------------
# Cell-count accessors
# ---------------------------------------------------------------------------

def cell_counts(M: np.ndarray = CL) -> dict[int, int]:
    """Count cells by output operator."""
    ct = Counter(int(v) for v in M.flatten())
    return {op: ct.get(op, 0) for op in range(N)}


def cells_with_output(target: int, M: np.ndarray = CL) -> list[tuple[int, int]]:
    """Return all (i, j) with M[i, j] == target."""
    return [(i, j) for i in range(N) for j in range(N) if int(M[i, j]) == target]


# ---------------------------------------------------------------------------
# Composition primitive
# ---------------------------------------------------------------------------

def compose(a: int, b: int, table: np.ndarray = CL) -> int:
    """Single CL composition step. Returns table[a, b]."""
    return int(table[a, b])


def is_commutative(M: np.ndarray = CL) -> bool:
    return bool((M == M.T).all())


def is_associative(M: np.ndarray = CL) -> bool:
    """Check whether (a*b)*c == a*(b*c) for all (a,b,c)."""
    for a in range(N):
        for b in range(N):
            for c in range(N):
                if int(M[int(M[a, b]), c]) != int(M[a, int(M[b, c])]):
                    return False
    return True


def non_associative_triples(M: np.ndarray = CL) -> list[tuple[int, int, int, int, int]]:
    """Return all (a, b, c, lhs, rhs) where (a*b)*c != a*(b*c)."""
    bad = []
    for a in range(N):
        for b in range(N):
            for c in range(N):
                lhs = int(M[int(M[a, b]), c])
                rhs = int(M[a, int(M[b, c])])
                if lhs != rhs:
                    bad.append((a, b, c, lhs, rhs))
    return bad


def non_associative_rate(M: np.ndarray = CL) -> float:
    """Fraction of triples where the composition is non-associative."""
    return len(non_associative_triples(M)) / (N ** 3)


# ---------------------------------------------------------------------------
# Self-test (run as __main__)
# ---------------------------------------------------------------------------

@dataclass
class CLReport:
    counts: dict[int, int]
    commutative: bool
    associative: bool
    non_assoc_rate: float
    asymmetric_cells: list[tuple[int, int, int, int]]


def report() -> CLReport:
    asym = []
    for i in range(N):
        for j in range(i + 1, N):
            if int(CL_RAW[i, j]) != int(CL_RAW[j, i]):
                asym.append((i, j, int(CL_RAW[i, j]), int(CL_RAW[j, i])))
    return CLReport(
        counts=cell_counts(CL),
        commutative=is_commutative(CL),
        associative=is_associative(CL),
        non_assoc_rate=non_associative_rate(CL),
        asymmetric_cells=asym,
    )


if __name__ == "__main__":
    r = report()
    print("=" * 60)
    print("CL ground-truth report")
    print("=" * 60)
    print()
    print("CL (after upper-triangle symmetrization):")
    print(CL)
    print()
    print("Cell counts (output operator -> count):")
    for op in range(N):
        c = r.counts.get(op, 0)
        if c > 0:
            print(f"  {op} ({OPERATORS[op]:8s}): {c}")
    print(f"  Total: {sum(r.counts.values())}  (expected 100)")
    print()
    h = r.counts.get(7, 0)
    v = r.counts.get(0, 0)
    other = sum(c for op, c in r.counts.items() if op not in (0, 7))
    print(f"  HARMONY={h}  VOID={v}  other={other}  (expected 73 + 17 + 10)")
    ok_count = (h == 73 and v == 17 and other == 10)
    print(f"  Counts match _CK_MEMORY_MAKEOVER spec: {ok_count}")
    print()
    print(f"Commutative (after symmetrization): {r.commutative}")
    print(f"Associative: {r.associative}")
    print(f"Non-associative triple rate: {100*r.non_assoc_rate:.1f}%")
    print()
    if r.asymmetric_cells:
        print(f"Asymmetric cells in raw bit pattern (resolved by upper-triangle):")
        for i, j, up, lo in r.asymmetric_cells:
            print(f"  ({i},{j})={up}  vs  ({j},{i})={lo}  -> kept {up}")
    else:
        print("Bit pattern was already symmetric.")
