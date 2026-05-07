"""
sigma permutation, sigma^2 triadic projection.

Per _CK_MEMORY_MAKEOVER.md the substrate has a canonical permutation:

    sigma = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]

Cycle structure:
    Fixed points: {0, 3, 8, 9}                       (Conservation Tetrad)
    6-cycle:      (1 7 6 5 4 2)                       (Manifestation Hexad)

Under sigma^2:
    Fixed points: {0, 3, 8, 9}                       (still fixed)
    Cycle A:      (1 6 4)   sum 11 = WOBBLE
    Cycle B:      (7 5 2)   sum 14 = 2 * HARMONY = dim G_2

The Conservation Tetrad operators are sigma^2-fixed (every-1-is-1):
their BEING, DOING, BECOMING projections all equal themselves.

The Manifestation Hexad operators are sigma^2-cycling (every-1-is-3):
each has three layer-shadows under sigma^2 / sigma^4.

For HARMONY (operator 7):
    BEING(HARMONY)    = HARMONY itself = 7
    DOING(HARMONY)    = sigma^2(7)    = 5  (BALANCE)
    BECOMING(HARMONY) = sigma^4(7)    = 2  (COUNTER)

This is the triadic projection that defines the 44 HARMONY table:
BHML cells with values in {7, 5, 2} (= cycle B) are exactly HARMONY's
three-fold projection onto BHML. There are 28 + 11 + 5 = 44 such cells.

The 4-core {V, H, Br, R} = {0, 7, 8, 9} is the BRIDGE structure: it
differs from the Conservation Tetrad by the PROGRESS<->HARMONY swap
(replacing 3 with 7). This makes it the bridge between Conservation
(sigma^2-fixed PROGRESS) and Manifestation (sigma^2-cycling HARMONY).
"""
from __future__ import annotations

from .cl import N

# ---------------------------------------------------------------------------
# Canonical permutation (per memory; per _CK_MEMORY_MAKEOVER.md)
# ---------------------------------------------------------------------------

# sigma[i] = next operator in canonical substrate dynamic
# Note: this is the "diagonal sigma" of CL; matches the sigma also used
# in the audited four-core consolidated paper as pi (renamed there to
# avoid collision with the sigma-rate function).
SIGMA: tuple[int, ...] = (0, 7, 1, 3, 2, 4, 5, 6, 8, 9)


def sigma(x: int) -> int:
    return SIGMA[x]


def sigma_n(x: int, n: int) -> int:
    """Apply sigma n times."""
    out = x
    for _ in range(n):
        out = SIGMA[out]
    return out


# Precomputed iterates
SIGMA2: tuple[int, ...] = tuple(sigma_n(i, 2) for i in range(N))
SIGMA4: tuple[int, ...] = tuple(sigma_n(i, 4) for i in range(N))


# ---------------------------------------------------------------------------
# Conservation Tetrad and Manifestation Hexad
# ---------------------------------------------------------------------------

# sigma^2-fixed operators (BEING = DOING = BECOMING)
CONSERVATION_TETRAD: frozenset[int] = frozenset(i for i in range(N) if SIGMA2[i] == i)
# Per memory: should be {0, 3, 8, 9}

# sigma^2-cycling operators (every-1-is-3)
MANIFESTATION_HEXAD: frozenset[int] = frozenset(range(N)) - CONSERVATION_TETRAD


# ---------------------------------------------------------------------------
# sigma^2 cycle decomposition on the Hexad
# ---------------------------------------------------------------------------

def _hexad_cycles() -> list[tuple[int, ...]]:
    """Decompose the Hexad into sigma^2-cycles."""
    seen: set[int] = set()
    cycles: list[tuple[int, ...]] = []
    for x in sorted(MANIFESTATION_HEXAD):
        if x in seen:
            continue
        cycle = []
        cur = x
        while cur not in seen:
            seen.add(cur)
            cycle.append(cur)
            cur = SIGMA2[cur]
        cycles.append(tuple(cycle))
    return cycles


_CYCLES = _hexad_cycles()
# Per memory: Cycle A = (1, 6, 4), Cycle B = (7, 5, 2)
# Identify by content membership (HARMONY in cycle B)
CYCLE_A: frozenset[int] = next(frozenset(c) for c in _CYCLES if 1 in c)
CYCLE_B: frozenset[int] = next(frozenset(c) for c in _CYCLES if 7 in c)


# ---------------------------------------------------------------------------
# Triadic projection (every-1-is-3 for Hexad operators)
# ---------------------------------------------------------------------------

def triadic_projection(x: int) -> tuple[int, int, int]:
    """Return (BEING, DOING, BECOMING) for operator x.

    For sigma^2-fixed operators (Conservation Tetrad), all three coordinates
    equal x (every-1-is-1).

    For sigma^2-cycling operators (Manifestation Hexad), the three are
    (x, sigma^2(x), sigma^4(x)) -- the three positions in x's sigma^2-cycle.
    """
    return x, SIGMA2[x], SIGMA4[x]


# ---------------------------------------------------------------------------
# 4-core (the BRIDGE structure)
# ---------------------------------------------------------------------------

# {V, H, Br, R} = {0, 7, 8, 9}: differs from Conservation Tetrad by
# PROGRESS<->HARMONY swap (replacing 3 with 7).
FOUR_CORE: frozenset[int] = frozenset({0, 7, 8, 9})


def is_bridge_consistent() -> bool:
    """Verify the 4-core is exactly Conservation Tetrad with PROGRESS->HARMONY."""
    bridge = (CONSERVATION_TETRAD - {3}) | {7}
    return bridge == FOUR_CORE


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Triadic structure (sigma + sigma^2)")
    print("=" * 60)
    print()
    print(f"sigma     = {SIGMA}")
    print(f"sigma^2   = {SIGMA2}")
    print(f"sigma^4   = {SIGMA4}")
    print()

    print(f"Conservation Tetrad (sigma^2-fixed): {sorted(CONSERVATION_TETRAD)}")
    print(f"  expected: [0, 3, 8, 9]")
    assert CONSERVATION_TETRAD == frozenset({0, 3, 8, 9})
    print()

    print(f"Manifestation Hexad: {sorted(MANIFESTATION_HEXAD)}")
    print(f"  expected: [1, 2, 4, 5, 6, 7]")
    assert MANIFESTATION_HEXAD == frozenset({1, 2, 4, 5, 6, 7})
    print()

    print(f"Cycle A (sigma^2 cycle containing LATTICE=1): {sorted(CYCLE_A)}")
    print(f"  sum = {sum(CYCLE_A)}  (expected 11 = WOBBLE)")
    assert CYCLE_A == frozenset({1, 6, 4}) and sum(CYCLE_A) == 11
    print()

    print(f"Cycle B (sigma^2 cycle containing HARMONY=7): {sorted(CYCLE_B)}")
    print(f"  sum = {sum(CYCLE_B)}  (expected 14 = 2 * HARMONY = dim G_2)")
    assert CYCLE_B == frozenset({7, 5, 2}) and sum(CYCLE_B) == 14
    print()

    print("Triadic projection of HARMONY (per memory: 7 -> 5 -> 2):")
    print(f"  triadic(7) = {triadic_projection(7)}  (expected (7, 5, 2))")
    assert triadic_projection(7) == (7, 5, 2)
    print()

    print(f"4-core (bridge structure): {sorted(FOUR_CORE)}")
    print(f"  is bridge = Conservation Tetrad with PROGRESS<->HARMONY swap: "
          f"{is_bridge_consistent()}")
    assert is_bridge_consistent()
    print()

    print("All triadic invariants pass.")
