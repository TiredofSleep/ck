"""
A3 -- Generator triples.

The three foundational generator triples encoding the
BEING / DOING / BECOMING decomposition. These are the minimal seeds
whose iterative closure under the lens projections (A5) generates the
canonical pair.

Generator triples:
    {0, 1, 2} = BEING     (VOID + LATTICE + COUNTER)        -- structure axis
    {0, 7, 1} = DOING     (VOID + HARMONY + LATTICE)        -- action axis
    {1, 2, 3} = BECOMING  (LATTICE + COUNTER + PROGRESS)    -- flow axis

Plus the structurally distinguished trinity-genesis seed:
    {1, 4, 9} = LATTICE + COLLAPSE + RESET
    -- closes BHML to all of Z/10Z in exactly 2 steps
       (minimum cardinality for algebraic genesis)
"""
from __future__ import annotations

from typing import Iterable

import numpy as np

# ---------------------------------------------------------------------------
# Generator triples
# ---------------------------------------------------------------------------

BEING = frozenset({0, 1, 2})
DOING = frozenset({0, 7, 1})
BECOMING = frozenset({1, 2, 3})

UNION_BEING_DOING_BECOMING = BEING | DOING | BECOMING  # = {0, 1, 2, 3, 7}

TRINITY_GENESIS = frozenset({1, 4, 9})

ALL_TRIPLES = {
    "BEING": BEING,
    "DOING": DOING,
    "BECOMING": BECOMING,
    "UNION_BEING_DOING_BECOMING": UNION_BEING_DOING_BECOMING,
    "TRINITY_GENESIS": TRINITY_GENESIS,
}


# ---------------------------------------------------------------------------
# Closure under a binary table
# ---------------------------------------------------------------------------

def closure(seed: Iterable[int], table: np.ndarray, max_steps: int = 50
            ) -> tuple[set[int], int]:
    """Iterative closure of `seed` under the binary operation `table`.

    Returns (closed_set, n_steps).
    """
    S = set(int(x) for x in seed)
    for step in range(max_steps):
        new = set(S)
        for a in S:
            for b in S:
                new.add(int(table[a, b]))
        if new == S:
            return S, step
        S = new
    return S, max_steps  # bailed out


def closes_to(seed: Iterable[int], table: np.ndarray, target: Iterable[int]
              ) -> bool:
    """True iff `seed` closes under `table` to exactly `target`."""
    closed, _ = closure(seed, table)
    return closed == set(int(x) for x in target)
