#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
J22 / HARMONY ladder — Yang-Mills 8x8 determinant verification
(70-rung).

Verifies Theorem 6.1 (manuscript §5): det(B_YM) = 70 = C(8, 4),
where B_YM is the canonical BHML companion table restricted to the
index set {1, 2, 3, 4, 5, 6, 8, 9} (i.e., B with the VOID and
HARMONY rows/columns dropped).

Usage:
    PYTHONIOENCODING=utf-8 python bhml_8_ym_det.py

Dependencies: numpy.
Wall-clock: under 1 second.
License: CC-BY-4.0.
"""

import math

import numpy as np


# Canonical BHML composition table (manuscript §2).
# Source: Gen13/targets/foundations/tables/canonical_tables.py
B = np.array([
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 7, 3, 7, 5, 6, 7, 8, 9, 0],
    [2, 3, 7, 5, 6, 7, 8, 9, 0, 1],
    [3, 7, 5, 7, 7, 8, 9, 0, 1, 7],
    [4, 5, 6, 7, 7, 9, 0, 1, 2, 7],
    [5, 6, 7, 8, 9, 7, 1, 2, 3, 4],
    [6, 7, 8, 9, 0, 1, 7, 3, 4, 5],
    [7, 8, 9, 0, 1, 2, 3, 7, 5, 6],
    [8, 9, 0, 1, 2, 3, 4, 5, 7, 7],
    [9, 0, 1, 7, 7, 4, 5, 6, 7, 7],
])


def main():
    idx = [1, 2, 3, 4, 5, 6, 8, 9]
    B_YM = B[np.ix_(idx, idx)]
    det = int(round(np.linalg.det(B_YM.astype(float))))
    c84 = math.comb(8, 4)
    print(f"det(B_YM) = {det}")
    print(f"C(8, 4)   = {c84}")
    if det == c84 == 70:
        print("[PASS] det(B_YM) == C(8, 4) == 70")
        return 0
    # If the embedded BHML differs from canonical_tables.py source, reload.
    print(f"[NOTE] expected det(B_YM) == 70; got {det} from the embedded matrix.")
    print("       For canonical verification, import from")
    print("       Gen13/targets/foundations/tables/canonical_tables.py")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
