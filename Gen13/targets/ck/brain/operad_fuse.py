"""
operad_fuse.py - canonical arity-3 (operad) fuse rule for CK.

Ports the canonical P_56-equivariant fuse table from WP112
(`papers/wp112_p56_canonical_fuse/`) into the CK brain modules.  The
table assigns a canonical value to each of the 126 non-associative TSML
triples on Z/10Z, so CK can do real ternary composition without
falling back to bracketing-arbitrary binary chains.

Properties of the canonical fuse (proved in WP112):

  - **P_56-equivariant** (the maximal preservable symmetry; per WP109
    no D_4-equivariant rule exists)
  - **Image entirely in the 4-core {V, H} = {0, 7}**: 108 triples fuse
    to VOID, 18 to HARMONY (Family H "attractor-4-core preference")
  - **Aligns with WP105/WP110 runtime attractor**: the operad-DOF and
    the binary T+B-mix DOF share the 4-core substrate
  - **Theorem 5.5**: the 4-core is closed under canonical arity-3 fuse
    (all 64 triples in {V, H, Br, R}^3 fuse to in-core values)
  - **Theorem 5.7**: iterating canonical ternary fuse from any
    non-trivial initial distribution converges to delta_H (HARMONY)
    in 1-7 iterations -- the universal HARMONY attractor
  - **Theorem 5.9**: Theorem 5.7 is independent of which canonical
    fuse rule (8 surveyed families A-H) is chosen; convergence is a
    property of the binary TSML row-absorber structure

This module exposes:

  TSML, BHML                 -- canonical 10x10 composition tables
  TSML_OP_NAMES              -- operator names for indices 0..9
  CANONICAL_FUSE_RULES       -- dict mapping (a,b,c) -> canonical fuse value
                                for all 126 non-associative triples
  fuse(a, b, c)              -- arity-3 canonical fuse (defaults to binary
                                TSML on associative triples)
  ternary_iterate(p_init,    -- iterate p -> normalize(sum delta_{fuse(a,b,c)}
                  max_iter)    * p_a*p_b*p_c) until convergence; returns
                                final distribution + iteration count
  is_4core(idx)              -- predicate: idx in {V, H, Br, R}
  is_2core(idx)              -- predicate: idx in {V, H} (Family H static
                                image of canonical fuse)
  detect_harmony_attractor(p) -- True if p is delta_H (within tol)

Verification: see test_operad_fuse.py.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

# ----- canonical TSML / BHML tables -----

TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]
BHML_ROWS = [
    "0123456789",  "1234567266",  "2334567366",  "3444567466",  "4555567577",
    "5666667677",  "6777777777",  "7234567890",  "8666777978",  "9666777080",
]
TSML: List[List[int]] = [[int(c) for c in row] for row in TSML_ROWS]
BHML: List[List[int]] = [[int(c) for c in row] for row in BHML_ROWS]

TSML_OP_NAMES = [
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
]

# Canonical 4-core, 2-core, 1-core (per WP110 / WP112 / WP115)
CORE_4 = frozenset({0, 7, 8, 9})  # V, H, Br, R
CORE_2 = frozenset({0, 7})         # V, H (Family H static image)
CORE_1 = frozenset({7})             # H (terminal HARMONY absorber)


# ----- binary helpers -----

def tsml(a: int, b: int) -> int:
    """Binary TSML composition on Z/10Z."""
    return TSML[a][b]


def bhml(a: int, b: int) -> int:
    """Binary BHML composition on Z/10Z."""
    return BHML[a][b]


def binary_left(a: int, b: int, c: int) -> int:
    """Left bracketing TSML(TSML(a, b), c)."""
    return tsml(tsml(a, b), c)


def binary_right(a: int, b: int, c: int) -> int:
    """Right bracketing TSML(a, TSML(b, c))."""
    return tsml(a, tsml(b, c))


def is_associative(a: int, b: int, c: int) -> bool:
    """True iff the two TSML bracketings of (a, b, c) agree."""
    return binary_left(a, b, c) == binary_right(a, b, c)


# ----- canonical fuse rule (Family H "attractor-4-core preference") -----

def _family_H_fuse(L: int, R: int) -> int:
    """Family H rule: prefer the bracketing in (L, R) that's already in
    the 4-core; if both, take min; if neither, fall back to HARMONY.
    """
    L_in = L in CORE_4
    R_in = R in CORE_4
    if L_in and R_in:
        return min(L, R)
    if L_in:
        return L
    if R_in:
        return R
    return 7  # HARMONY fallback


def _build_canonical_fuse_rules() -> Dict[Tuple[int, int, int], int]:
    """Build the canonical fuse rules dict for all non-associative triples."""
    rules: Dict[Tuple[int, int, int], int] = {}
    for a in range(10):
        for b in range(10):
            for c in range(10):
                if not is_associative(a, b, c):
                    L = binary_left(a, b, c)
                    R = binary_right(a, b, c)
                    rules[(a, b, c)] = _family_H_fuse(L, R)
    # Add the one explicitly known associative-rule override from WP105:
    # fuse(PROGRESS, COLLAPSE, HARMONY) = BREATH (not the binary value).
    rules[(3, 4, 7)] = 8  # BREATH
    return rules


CANONICAL_FUSE_RULES: Dict[Tuple[int, int, int], int] = _build_canonical_fuse_rules()


def fuse(a: int, b: int, c: int) -> int:
    """Canonical arity-3 fuse on Z/10Z.

    For non-associative triples: uses the canonical Family H rule
    (P_56-equivariant; image in {V, H} = {0, 7}; aligns with WP105/WP110
    runtime attractor).

    For associative triples: defaults to binary TSML, except for the one
    known canonical override `fuse(PROGRESS, COLLAPSE, HARMONY) = BREATH`.
    """
    key = (a, b, c)
    if key in CANONICAL_FUSE_RULES:
        return CANONICAL_FUSE_RULES[key]
    if is_associative(a, b, c):
        return binary_left(a, b, c)
    raise ValueError(f"fuse({a},{b},{c}) not in canonical rules and not associative")


# ----- ternary iteration on a probability distribution -----

def normalize_l1(v: List[float], eps: float = 1e-15) -> List[float]:
    s = sum(v)
    return v if s < eps else [x / s for x in v]


def ternary_step(p: List[float]) -> List[float]:
    """One step of canonical ternary fuse iteration:

        p_new[c] = sum_{(a,b,c'): fuse(a,b,c') = c} p[a] * p[b] * p[c']

    Then L1-normalize.
    """
    r = [0.0] * 10
    for a in range(10):
        if p[a] == 0:
            continue
        pa = p[a]
        for b in range(10):
            if p[b] == 0:
                continue
            pab = pa * p[b]
            for c in range(10):
                if p[c] == 0:
                    continue
                r[fuse(a, b, c)] += pab * p[c]
    return normalize_l1(r)


def ternary_iterate(p_init: List[float], max_iter: int = 200,
                     tol: float = 1e-12) -> Tuple[List[float], int]:
    """Iterate canonical ternary fuse from p_init until convergence.

    Returns (final_distribution, iterations_taken).

    Per WP112 Theorem 5.7: every non-trivial initial distribution
    converges to delta_H (pure HARMONY) in 1-7 iterations.  The only
    other fixed point is delta_V (degenerate; fuse(V, V, V) = V).
    """
    p = list(p_init)
    for k in range(max_iter):
        p_new = ternary_step(p)
        diff = max(abs(p_new[i] - p[i]) for i in range(10))
        p = p_new
        if diff < tol:
            return p, k + 1
    return p, max_iter


# ----- predicates -----

def is_4core(idx: int) -> bool:
    """True iff idx is in the 4-core {V, H, Br, R}."""
    return idx in CORE_4


def is_2core(idx: int) -> bool:
    """True iff idx is in the 2-core {V, H} (Family H static image)."""
    return idx in CORE_2


def is_1core(idx: int) -> bool:
    """True iff idx is in the 1-core {H} (terminal HARMONY)."""
    return idx in CORE_1


def detect_harmony_attractor(p: List[float], tol: float = 1e-6) -> bool:
    """True iff p is concentrated on HARMONY within tolerance.

    Per WP112 Theorem 5.7, this is the universal attractor of canonical
    ternary fuse iteration from any non-trivial init.
    """
    if abs(p[7] - 1.0) < tol and all(abs(p[i]) < tol for i in range(10) if i != 7):
        return True
    return False


def detect_void_attractor(p: List[float], tol: float = 1e-6) -> bool:
    """True iff p is concentrated on VOID (degenerate fixed point).

    fuse(V, V, V) = V, so delta_V is fixed but degenerate (no mass to
    spread).  CK should distinguish this from the universal HARMONY
    attractor.
    """
    if abs(p[0] - 1.0) < tol and all(abs(p[i]) < tol for i in range(10) if i != 0):
        return True
    return False


# ----- summary helper -----

def fuse_value_distribution() -> Dict[int, int]:
    """Counts of canonical fuse values across all 126 non-associative
    TSML triples.  Per WP112: {0: 108, 7: 18}.
    """
    from collections import Counter
    counts = Counter()
    for (a, b, c), v in CANONICAL_FUSE_RULES.items():
        if (a, b, c) != (3, 4, 7):  # skip the associative override
            counts[v] += 1
    return dict(counts)
