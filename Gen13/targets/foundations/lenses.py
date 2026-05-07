"""
A5 -- The two-lens projection.

Construct TSML and BHML FROM RULES (not hardcoded). Constructing from
rules catches axiom drift: if you change the rule for the C_0 absorb
behavior or the BHML successor row, the table changes accordingly,
and downstream verifications either still pass (rule was equivalent)
or fail (rule was not the canonical one).

CONSTRUCTION:

TSML (Being lens, measurement projection):
  The C_0 rule defines TSML's bare backbone, with two perturbation
  patches (S_MAX = sigma-MAX overrides; S_ADD = closure-completing
  cells) added to satisfy the canonical-pair axioms. Inside this
  module we construct only the C_0 backbone explicitly; the
  S_MAX / S_ADD perturbations are an open derivation
  (sprint_bundle's SPRINT_FACTOR_6_DARK_MATTER explores them).

BHML (Becoming lens, transformation projection):
  Built from four explicit rules:
    Rule 0:  BHML[0, j] = j           (VOID is identity)
    Rule 1:  BHML[i, j] = (max(i,j)+1) mod N for i, j in {1..6}
    Rule 7:  BHML[7, j] = (j + 1) mod N    (HARMONY-row successor)
    Rule 89: BHML[i, j] = (i + j) mod N for i, j in {8, 9}
  Plus commutativity: BHML[i, j] = BHML[j, i]. The remaining
  outer-x-inner cells (i in {8,9}, j in {1..6}) are filled with
  (i + j) mod N as a placeholder; the canonical rule for these is
  open (see SPRINT_V1_V2_CLOSURE.md note).
"""
from __future__ import annotations

import numpy as np

from .substrate import N, sigma_units

CORE = frozenset({0, 7, 8, 9})    # the 4-core
UNITS = frozenset({1, 3, 7, 9})   # multiplicative units of Z/10Z
HARMONY = 7
VOID = 0


# ---------------------------------------------------------------------------
# TSML's C_0 rule (bare backbone, before S_MAX / S_ADD perturbations)
# ---------------------------------------------------------------------------

def build_C0() -> np.ndarray:
    """Build the C_0 backbone for TSML.

    Rules (in priority order):
        1. VOID absorbs:        if i == 0 or j == 0 -> 0.
        2. HARMONY absorbs:     if (i == HARMONY or j == HARMONY) AND
                                neither is VOID -> HARMONY.
        3. Off-Core -> HARMONY:  if i not in CORE or j not in CORE -> HARMONY.
        4. On-Core, non-units -> HARMONY (default).
        5. On-Core units, smaller sigma_units wins;
           sigma-tie -> HARMONY.
    """
    C0 = np.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            if i == VOID or j == VOID:
                C0[i, j] = VOID
            elif i == HARMONY or j == HARMONY:
                C0[i, j] = HARMONY
            elif i not in CORE or j not in CORE:
                C0[i, j] = HARMONY
            elif i not in UNITS or j not in UNITS:
                C0[i, j] = HARMONY
            else:
                si, sj = sigma_units(i), sigma_units(j)
                if si < sj:
                    C0[i, j] = i
                elif sj < si:
                    C0[i, j] = j
                else:
                    C0[i, j] = HARMONY
    return C0


# ---------------------------------------------------------------------------
# BHML construction (four-rule)
# ---------------------------------------------------------------------------

def build_BHML() -> np.ndarray:
    """Build BHML from its four canonical rules.

    Note: the outer-x-inner cells (i in {8,9}, j in {1..6}) use
    (i + j) mod N as the default, which the bundle's V1V2 sprint flags
    as needing canonical-rule confirmation.
    """
    B = np.full((N, N), -1, dtype=int)

    # Rule 0: VOID is identity (rows and columns)
    for k in range(N):
        B[0, k] = k
        B[k, 0] = k

    # Rule 1: max(i,j)+1 on inner 6x6 (operators 1..6)
    for i in range(1, 7):
        for j in range(1, 7):
            B[i, j] = (max(i, j) + 1) % N

    # Rule 7: HARMONY row = successor (j + 1) mod N
    for k in range(N):
        B[7, k] = (k + 1) % N
        B[k, 7] = (k + 1) % N  # commutativity

    # Rule 89: BREATH/RESET wrap
    for i in (8, 9):
        for j in (8, 9):
            B[i, j] = (i + j) % N

    # Outer x inner default placeholder (i in {8,9}, j in {1..6})
    for i in (8, 9):
        for j in range(1, 7):
            if B[i, j] < 0:
                B[i, j] = (i + j) % N
                B[j, i] = (i + j) % N

    assert (B >= 0).all(), "BHML construction left some cells unfilled"
    return B


def fuse_axiom_holds_on(table: np.ndarray) -> bool:
    """Verify A4: fuse(3, 4, 7) = 8 -- equivalently table[7, 7] = 8 here.

    Rationale: in the 4-rule BHML, rule 7 forces table[7, 7] =
    (7 + 1) mod 10 = 8, satisfying the fuse axiom directly on the
    diagonal. TSML's C_0 backbone does NOT satisfy this (table[7, 7] =
    7 by the HARMONY-absorbs rule), which distinguishes the lenses.
    """
    return int(table[7, 7]) == 8


if __name__ == "__main__":
    print("=" * 60)
    print("Lenses (A5) self-test")
    print("=" * 60)

    C0 = build_C0()
    print("C_0 (TSML backbone):")
    print(C0)
    print(f"  C_0[7, 7] = {C0[7, 7]}  -- HARMONY (fuse axiom NOT on TSML, expected)")

    B = build_BHML()
    print()
    print("BHML:")
    print(B)
    print(f"  BHML[7, 7] = {B[7, 7]}  -- expected 8 (fuse axiom holds)")

    print()
    print(f"fuse axiom on C_0:  {fuse_axiom_holds_on(C0)}  (expected False)")
    print(f"fuse axiom on BHML: {fuse_axiom_holds_on(B)}  (expected True)")
