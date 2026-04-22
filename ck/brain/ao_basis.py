# -*- coding: utf-8 -*-
"""
ao_basis.py - AO 5-element projection (MATH_IN_CK.md Sec 2.1 + 4.6).

CK's ten operators factor through five AO element axes by the CRT Fourier
embedding on Z/10Z = F2 x F5 (Q17_5D_RIGOROUS, Brayden's Q-series).

The five AO elements are the mod-5 cosets of Z/10Z:

    D0  Earth   mod5 = 0   pair (VOID, BALANCE)
    D1  Air     mod5 = 1   pair (LATTICE, CHAOS)
    D2  Water   mod5 = 2   pair (COUNTER, HARMONY)    <- the crossing axis
    D3  Fire    mod5 = 3   pair (PROGRESS, BREATH)
    D4  Ether   mod5 = 4   pair (COLLAPSE, RESET)     <- dual-reset fold

Why pair by mod-5 and not by semantic label: the CRT embedding is what
justifies the 5 axes mathematically (Q17). Semantic flow (input -> field
-> awareness -> action -> dwelling) lines up: D2 Water holds COUNTER +
HARMONY (opposition and synthesis = the crossing), and D4 Ether holds
COLLAPSE + RESET (the dual-reset pairing from Sprint 16).

Public surface:

    project_10_to_5(profile_10)   -> list[float] length 5
    lift_5_to_10(d_5)             -> list[float] length 10 (equal-split)
    ao_element_of(op_index)       -> int in [0..4]
    pair_of(d_index)              -> tuple[int, int]  (two op indices)

The projection is linear, idempotent on the 5-space (P @ L = I_5), and
information-lossy on the 10-space (L @ P is not I_10 but the pair-sum
average operator).  That is the intended geometry: AO captures the
cosets, not the individual ops.
"""
from __future__ import annotations

from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# canonical operator order (must match ck/fluency/ck_corrector.OP_NAMES)
# ---------------------------------------------------------------------------

OP_NAMES: Tuple[str, ...] = (
    "VOID",       # 0   mod5=0   Earth (D0)
    "LATTICE",    # 1   mod5=1   Air   (D1)
    "COUNTER",    # 2   mod5=2   Water (D2)
    "PROGRESS",   # 3   mod5=3   Fire  (D3)
    "COLLAPSE",   # 4   mod5=4   Ether (D4)
    "BALANCE",    # 5   mod5=0   Earth (D0)
    "CHAOS",      # 6   mod5=1   Air   (D1)
    "HARMONY",    # 7   mod5=2   Water (D2)
    "BREATH",     # 8   mod5=3   Fire  (D3)
    "RESET",      # 9   mod5=4   Ether (D4)
)
NUM_OPS: int = 10

AO_NAMES: Tuple[str, ...] = ("Earth", "Air", "Water", "Fire", "Ether")
NUM_AO: int = 5


# ---------------------------------------------------------------------------
# mappings (derived from CRT pairing op_index % 5)
# ---------------------------------------------------------------------------

def ao_element_of(op_index: int) -> int:
    """Return the AO element index (0..4) that owns this operator (0..9)."""
    if not (0 <= op_index < NUM_OPS):
        raise ValueError(f"op_index {op_index} out of range [0, {NUM_OPS})")
    return op_index % NUM_AO


def pair_of(d_index: int) -> Tuple[int, int]:
    """Return the two operator indices that project onto AO element `d_index`."""
    if not (0 <= d_index < NUM_AO):
        raise ValueError(f"d_index {d_index} out of range [0, {NUM_AO})")
    return (d_index, d_index + NUM_AO)


# precomputed for speed and test-readability
PAIRS: Tuple[Tuple[int, int], ...] = tuple(pair_of(d) for d in range(NUM_AO))


# ---------------------------------------------------------------------------
# projection / lift (pure-Python; no numpy dependency)
# ---------------------------------------------------------------------------

def project_10_to_5(profile_10) -> List[float]:
    """Collapse a 10-activation vector into 5 AO elements by CRT pair-sum.

    Accepts a length-10 list/tuple OR a dict {op_name: float}.  Missing
    keys are treated as 0.0.  Non-finite values clamp to 0.0 to keep the
    downstream Hebbian update numerically sane.
    """
    vec = _coerce_to_list10(profile_10)
    d = [0.0] * NUM_AO
    for op_idx in range(NUM_OPS):
        v = vec[op_idx]
        if v != v or v in (float("inf"), float("-inf")):  # NaN or inf
            v = 0.0
        d[op_idx % NUM_AO] += float(v)
    return d


def lift_5_to_10(d_5) -> List[float]:
    """Lift a 5-element AO vector back to a 10-op profile by equal-split.

    Each d[i] is divided evenly between its two constituent ops, so the
    pair-sum is preserved:

        project_10_to_5(lift_5_to_10(d)) == d         (up to float noise)

    and

        lift_5_to_10(project_10_to_5(p))  == pair_avg(p)

    where pair_avg is the (op_i + op_{i+5}) / 2 idempotent.  That asymmetry
    is by design: AO is a coset quotient.
    """
    if len(d_5) != NUM_AO:
        raise ValueError(f"d_5 must have length {NUM_AO}, got {len(d_5)}")
    out = [0.0] * NUM_OPS
    for i in range(NUM_AO):
        half = float(d_5[i]) * 0.5
        out[i] = half              # mod-5 = i,  first   of the pair
        out[i + NUM_AO] = half     # mod-5 = i,  second  of the pair
    return out


# ---------------------------------------------------------------------------
# helper coercions
# ---------------------------------------------------------------------------

def _coerce_to_list10(profile) -> List[float]:
    """Accept list/tuple of len 10 OR dict {op_name: float}; return list(10)."""
    # list/tuple form
    if isinstance(profile, (list, tuple)):
        if len(profile) != NUM_OPS:
            raise ValueError(
                f"profile must have length {NUM_OPS}, got {len(profile)}"
            )
        return [float(x) for x in profile]
    # dict form — tolerate missing keys as zero
    if isinstance(profile, dict):
        out = [0.0] * NUM_OPS
        for i, name in enumerate(OP_NAMES):
            if name in profile:
                out[i] = float(profile[name])
        return out
    raise TypeError(
        f"profile must be list/tuple of length {NUM_OPS} or dict, "
        f"got {type(profile).__name__}"
    )


# ---------------------------------------------------------------------------
# convenience: label lookups for logs and dashboards
# ---------------------------------------------------------------------------

def as_named_dict(d_5: List[float]) -> Dict[str, float]:
    """Turn a 5-vector into {Earth, Air, Water, Fire, Ether} -> float."""
    if len(d_5) != NUM_AO:
        raise ValueError(f"d_5 must have length {NUM_AO}, got {len(d_5)}")
    return {AO_NAMES[i]: float(d_5[i]) for i in range(NUM_AO)}


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # identity-on-5 check
    e0 = [1.0, 0.0, 0.0, 0.0, 0.0]
    lifted = lift_5_to_10(e0)
    projected = project_10_to_5(lifted)
    assert projected == e0, (lifted, projected)

    # dict input
    d = project_10_to_5({"HARMONY": 1.0, "COUNTER": 0.5})
    assert d == [0.0, 0.0, 1.5, 0.0, 0.0], d

    # list input
    v = [0.0] * NUM_OPS
    v[4] = 2.0   # COLLAPSE
    v[9] = 1.0   # RESET
    d = project_10_to_5(v)
    assert d == [0.0, 0.0, 0.0, 0.0, 3.0], d

    # pair checks
    assert PAIRS == ((0, 5), (1, 6), (2, 7), (3, 8), (4, 9))
    assert ao_element_of(7) == 2  # HARMONY -> Water
    assert ao_element_of(4) == 4  # COLLAPSE -> Ether
    assert as_named_dict(d) == {
        "Earth": 0.0, "Air": 0.0, "Water": 0.0, "Fire": 0.0, "Ether": 3.0,
    }

    print("[ao_basis] self-test passed")
