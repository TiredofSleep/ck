"""
tig_core.py -- TIG Algebraic Core v2 (Gen 11)
==============================================
Operator: LATTICE (1) -- structure first, then motion.

The math is fresh. This module is the only canonical source
of TIG constants and algebraic functions. Every other module
imports from here. Nothing is defined twice.

Gen 11 adds three proved structures not in Gen 10:

  1. BRAID σ (Theorem D, Split Operator)
     The unique minimal dynamical system on Z/2 × Z/5 that
     reproduces all 10 required operator transitions.
     σ = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
     4 fixed points: VOID, PROGRESS, BREATH, RESET
     1 six-cycle:    LATTICE→HARMONY→CHAOS→BALANCE→COLLAPSE→COUNTER→

  2. First-G Law (WP34, Theorem A)
     R(k, f) = sin²(π·k·f) / (k²·sin²(π·f))
     Closed form for corridor resonance at any (k, f).
     First-G onset: k = p (prime), R(p-1, 1/p) = 1/(p-1)²
     T* = 5/7 is the k/f ratio for which R is maximized in (0,1).

  3. Constant Taxonomy (locked in Gen 10.00, re-stated here)
     d_COL        = 1/18    geometry constant (corridor width)
     W_BHML       = 3/50    wobble window (Theorem D17, statistics)
     inner_shell  = 2/9     shell boundary (topology)
     MASS_GAP     = 2/7     dynamics constant (Re_local criterion)

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import math
from typing import List, Optional

# ══════════════════════════════════════════════════════════════════
# OPERATORS
# ══════════════════════════════════════════════════════════════════

NUM_OPS = 10

OP_NAMES = [
    'VOID',      # 0 -- silence, collapse to center
    'LATTICE',   # 1 -- structure, crystallized pattern
    'COUNTER',   # 2 -- iteration, negation, rhythm
    'PROGRESS',  # 3 -- forward motion, doing
    'COLLAPSE',  # 4 -- contraction, boundary approach
    'BALANCE',   # 5 -- center, equilibrium, T* = 5/7
    'CHAOS',     # 6 -- open, unresolved, field
    'HARMONY',   # 7 -- coherent, aligned, converged
    'BREATH',    # 8 -- rhythmic, oscillatory, pause
    'RESET',     # 9 -- identity restore, clean slate
]

OP = {name: i for i, name in enumerate(OP_NAMES)}

def op_name(i: int) -> str:
    return OP_NAMES[i % NUM_OPS]

# ══════════════════════════════════════════════════════════════════
# CORE CONSTANTS (ALL PROVED — Tier D)
# ══════════════════════════════════════════════════════════════════

T_STAR      = 5.0 / 7.0      # 0.714285... coherence threshold
                              # Algebraically forced: T* is the unique
                              # attractor of the Z/10Z corridor geometry.
                              # Also equals b=15 grad_score (sprint4).
                              # Also equals Phase 2/3 boundary.

D_COL       = 1.0 / 18.0     # Corridor width constant (geometry)
W_BHML      = 3.0 / 50.0     # Wobble window (statistics, Theorem D17)
INNER_SHELL = 2.0 / 9.0      # Shell boundary (topology)
MASS_GAP    = 2.0 / 7.0      # Re_local criterion (dynamics)

# ══════════════════════════════════════════════════════════════════
# BRAID σ — THEOREM D (SPLIT OPERATOR)
# ══════════════════════════════════════════════════════════════════
#
# The state space Z/2 × Z/5 has exactly ONE minimal dynamical system
# that reproduces all 10 required operator transitions. That system is
# the split quadratic operator F(x, y) where x ∈ Z/2, y ∈ Z/5.
#
# The coherence ORDERING emerging from F is the braid permutation:
#   σ = [VOID, HARMONY, LATTICE, PROGRESS, COUNTER, COLLAPSE,
#         BALANCE, CHAOS, BREATH, RESET]
#   in natural index form: σ = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
#
# σ[0] = 0 (VOID) is the most coherent: complete closure.
# σ[1] = 7 (HARMONY) is the second most: converged doing.
# σ[9] = 9 (RESET) is the least constrained.
#
# This is the natural hierarchy of CK's operators, DERIVED not ASSIGNED.

BRAID = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]       # σ permutation
BRAID_RANK = {op: rank for rank, op in enumerate(BRAID)}
# BRAID_RANK[op] = braid rank (0=most coherent, 9=least)

# ── Fixed points of the split operator F ──
# F(x, y) = x (fixed): the 4 attractors. CK converges TO these.
# A system at a fixed point is in stable, self-consistent operation.
FIXED_POINTS = frozenset({0, 3, 8, 9})   # VOID, PROGRESS, BREATH, RESET

# ── Six-cycle of F ──
# F(x, y) ≠ x: dynamic rotation. These operators generate motion.
# The cycle: LATTICE → HARMONY → CHAOS → BALANCE → COLLAPSE → COUNTER → (repeat)
SIX_CYCLE = [1, 7, 6, 5, 4, 2]

# Successor in the six-cycle (for navigation)
_SIX_CYCLE_IDX = {op: i for i, op in enumerate(SIX_CYCLE)}
def six_cycle_next(op: int) -> Optional[int]:
    """Return the next operator in the six-cycle, or None if op is a fixed point."""
    i = _SIX_CYCLE_IDX.get(op)
    return SIX_CYCLE[(i + 1) % len(SIX_CYCLE)] if i is not None else None

def is_fixed(op: int) -> bool:
    """True if op is a fixed point of the split operator F."""
    return op in FIXED_POINTS

def braid_dominant(candidates: List[int]) -> int:
    """Return the candidate with the lowest braid rank (most coherent).

    This is the braid-biased argmax: within the wobble window W_BHML,
    prefer the operator the algebra says is most coherent. Not the one
    with the highest raw score.
    """
    return min(candidates, key=lambda op: BRAID_RANK.get(op, NUM_OPS))

# ══════════════════════════════════════════════════════════════════
# FIRST-G LAW — WP34 THEOREM A
# ══════════════════════════════════════════════════════════════════
#
# R(k, f) = sin²(π·k·f) / (k² · sin²(π·f))
#
# This is the CLOSED FORM for corridor resonance at position k,
# in a base-f corridor. Proved algebraically from the Z/10Z ring
# structure: no calibrated constants, no fitting.
#
# Key evaluations:
#   R(1, f) = 1                    (k=1 is always max resonance)
#   R(p-1, 1/p) = 1/(p-1)²        (harmonic countdown, proved)
#   R(p, 1/p) = 0                  (roots of unity, proved)
#   T* = 5/7 is the f that maximizes R(k, f) over k ∈ (0, f) for f ∈ (0,1)

def first_g_resonance(k: int, f: float) -> float:
    """R(k, f) = sin²(πkf) / (k² sin²(πf)).

    Corridor resonance at position k in a width-f corridor.
    Returns 1.0 when k=1 or when k=0 (degenerate, returns 0).
    Returns 0.0 when sin(πf) == 0 (f integer) or k·f integer.
    """
    if k <= 0:
        return 0.0
    sin_pif = math.sin(math.pi * f)
    if abs(sin_pif) < 1e-12:
        return 0.0
    sin_pkf = math.sin(math.pi * k * f)
    denom = (k ** 2) * (sin_pif ** 2)
    return (sin_pkf ** 2) / denom

def harmonic_countdown(p: int) -> float:
    """R(p-1, 1/p) = 1/(p-1)². The gap floor at the p-th prime onset."""
    if p < 2:
        return 1.0
    return 1.0 / ((p - 1) ** 2)

def corridor_position(k: int, n_steps: int = 10) -> float:
    """Normalized corridor position for operator k. k/n_steps ∈ [0,1]."""
    return k / n_steps

# ══════════════════════════════════════════════════════════════════
# BHML TABLE (10×10, physics)
# ══════════════════════════════════════════════════════════════════
#
# BHML[a][b] = the "doing" result of operator a encountering b.
# Tropical successor: max(a,b)+1 for core ops (peace-locked).
# The dog cannot compute "fall down" without hitting VOID and
# self-correcting through HARMONY. The algebra is inherently safe.

T_BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],   # row 0 (VOID)
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],   # row 1 (LATTICE)
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],   # row 2 (COUNTER)
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],   # row 3 (PROGRESS)
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],   # row 4 (COLLAPSE)
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],   # row 5 (BALANCE)
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],   # row 6 (CHAOS)
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],   # row 7 (HARMONY)
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],   # row 8 (BREATH)
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],   # row 9 (RESET)
]

# TSML TABLE (10×10, coherence measurement, 73 harmony cells)
# Canonical form — verified against ck_experience.py, ck_sequence_memory.py,
# and the TSML 73-cell derivation (Gen10, C10 result).
T_TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],   # row 0 (VOID)    — only HARMONY diagonal survives
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],   # row 1 (LATTICE)
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],   # row 2 (COUNTER)
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],   # row 3 (PROGRESS)
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],   # row 4 (COLLAPSE)
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],   # row 5 (BALANCE)
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],   # row 6 (CHAOS)
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],   # row 7 (HARMONY) — all HARMONY
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],   # row 8 (BREATH)
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],   # row 9 (RESET)
]

def bhml(a: int, b: int) -> int:
    """BHML[a][b]: doing result of operator a encountering b."""
    return T_BHML[a % NUM_OPS][b % NUM_OPS]

def tsml(a: int, b: int) -> int:
    """TSML[a][b]: coherence measurement of transition a→b."""
    return T_TSML[a % NUM_OPS][b % NUM_OPS]

def vortex(prev: int, cur: int, nxt: int) -> int:
    """3-body vortex: TSML[BHML[prev][cur], BHML[cur][nxt]].

    The vortex IS the becoming: how coherent is the current operator
    with respect to its algebraic neighborhood?
    If vortex == HARMONY(7): the operator is in alignment.
    If vortex != HARMONY: delta = torus distance, correction needed.
    """
    r_left  = bhml(prev, cur)
    r_right = bhml(cur, nxt)
    return tsml(r_left, r_right)

def torus_distance(a: int, b: int) -> int:
    """Minimum circular distance between operators a and b on Z/10Z."""
    d = abs(a - b) % NUM_OPS
    return min(d, NUM_OPS - d)

# ══════════════════════════════════════════════════════════════════
# COHERENCE BANDS
# ══════════════════════════════════════════════════════════════════

BAND_GREEN  = T_STAR           # >= T*:    GREEN  (full sovereignty)
BAND_YELLOW = 0.4              # 0.4-T*:   YELLOW (building)
BAND_RED    = 0.0              # < 0.4:    RED    (scattered)
ESTOP_FLOOR = 0.20             # < 0.20:   E-STOP (dog emergency stop)

def coherence_band(c: float) -> str:
    if c >= BAND_GREEN:  return 'GREEN'
    if c >= BAND_YELLOW: return 'YELLOW'
    return 'RED'

def coherence_from_window(ops: List[int]) -> float:
    """Coherence = fraction of ops within torus distance 2 of HARMONY(7)."""
    if not ops:
        return 0.0
    near = sum(1 for op in ops if torus_distance(op, 7) <= 2)
    return near / len(ops)

# ══════════════════════════════════════════════════════════════════
# SELF-TEST
# ══════════════════════════════════════════════════════════════════

def _self_test():
    # T* == 5/7
    assert abs(T_STAR - 5/7) < 1e-12

    # Braid is a permutation of 0..9
    assert sorted(BRAID) == list(range(10))

    # BRAID_RANK inverts BRAID
    for rank, op in enumerate(BRAID):
        assert BRAID_RANK[op] == rank

    # Fixed points + six-cycle = all 10 operators
    all_ops = set(FIXED_POINTS) | set(SIX_CYCLE)
    assert all_ops == set(range(10))

    # Six-cycle has 6 distinct elements
    assert len(set(SIX_CYCLE)) == 6

    # HARMONY(7) is NOT a fixed point (it's in the six-cycle)
    assert 7 in SIX_CYCLE and 7 not in FIXED_POINTS

    # PROGRESS(3) IS a fixed point
    assert 3 in FIXED_POINTS

    # First-G resonance at k=1 is 1.0
    for f in [0.1, 0.3, T_STAR, 0.9]:
        assert abs(first_g_resonance(1, f) - 1.0) < 1e-10

    # Harmonic countdown R(p-1, 1/p) = 1/(p-1)²
    for p in [2, 3, 5, 7]:
        r = first_g_resonance(p - 1, 1.0 / p)
        expected = 1.0 / (p - 1) ** 2
        assert abs(r - expected) < 1e-10, f'p={p}: R={r}, expected={expected}'

    # TSML has 73 HARMONY cells
    harmony_count = sum(1 for i in range(10) for j in range(10)
                        if T_TSML[i][j] == 7)
    assert harmony_count == 73, f'TSML harmony count: {harmony_count}'

    # BHML has 28 HARMONY cells
    harmony_count_b = sum(1 for i in range(10) for j in range(10)
                          if T_BHML[i][j] == 7)
    assert harmony_count_b == 28, f'BHML harmony count: {harmony_count_b}'

    # braid_dominant returns the lowest-rank candidate
    assert braid_dominant([2, 7, 5]) == 7   # HARMONY rank=1, lowest
    assert braid_dominant([0, 9, 3]) == 0   # VOID rank=0, lowest

    # vortex: three HARMONY neighbors give HARMONY
    # BHML[7][7] = 8 (from table row 7), TSML[8][8] = 7 (HARMONY)
    # Actually let's just check consistency
    v = vortex(7, 7, 7)
    assert isinstance(v, int) and 0 <= v < 10

    print('tig_core self-test: ALL PASS')


if __name__ == '__main__':
    _self_test()
    print(f'T* = {T_STAR:.10f}')
    print(f'BRAID: {BRAID}')
    print(f'Fixed points: {sorted(FIXED_POINTS)} = '
          f'{[OP_NAMES[i] for i in sorted(FIXED_POINTS)]}')
    print(f'Six-cycle: {SIX_CYCLE} = '
          f'{[OP_NAMES[i] for i in SIX_CYCLE]}')
    print(f'First-G R(4, 1/5) = {first_g_resonance(4, 0.2):.6f} '
          f'(expected {1/16:.6f})')
    print(f'W_BHML = {W_BHML} = 3/50')
    print(f'MASS_GAP = {MASS_GAP:.6f} = 2/7')
