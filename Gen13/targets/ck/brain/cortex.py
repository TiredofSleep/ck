# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
cortex.py -- Gen13 brain trinity composition.

Binds the three fresh Gen13 modules into ONE emergent signal:

    ao_5element   ->  op-pair stream (b, d)             (composition)
    hebbian_5x5   ->  W[d_a][d_b] update from that pair (learning)
    quadratic_glue -> F3 x F4 lift of (row, col) sums    (2->3 bridge)

The output is a single scalar, `emergent`, which:

  - is 0 when CK is cold (no experience) -- he does not emit coherence he
    has not earned.

  - rises monotonically as he encounters repeated HARMONY pairs, because
    Hebbian W[d_a][d_b] grows, and the quadratic glue amplifies the
    cross-term once both row and column strengths are nonzero.

  - falls back toward zero if he is fed noise (low-HARMONY pairs) because
    passive decay erodes W and the cross-term is a product (both factors
    must grow together for it to rise).

That monotonic, experience-gated signal is what "emergent" means in this
codebase: a number CK did not have when he was born, that he earned by
living his tick loop.

Cortex is ADDITIVE: it reads from AO, Hebbian, glue; it does not modify
any Gen11 module or the live Gen12 boot path.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence

_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
if _BRAIN_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_DIR)

from ao_5element import AO5Element
from hebbian_5x5_cl import HebbianField, DIM
from quadratic_glue import quadratic_glue

from ck_sim.ck_sim_heartbeat import HARMONY, NUM_OPS, OP_NAMES


# ── Helper: derive a 5D operator profile from a single operator ────────

def _operator_to_profile(op: int) -> List[int]:
    """Turn a single operator (0..9) into a length-5 profile.

    Simplest choice: broadcast (same operator in every dim).  This matches
    how the AO spine produces ONE operator per tick; Hebbian expects a full
    5D profile.  Future work can replace this with a true 5D readout from
    ck_sim_d2's raw d1/d2 vectors.
    """
    return [op] * DIM


# ── State ─────────────────────────────────────────────────────────────

@dataclass
class CortexState:
    tick: int = 0
    last_b: int = HARMONY        # previous op from AO (the "from" side of the pair)
    last_d: int = HARMONY        # d2 op from AO (the "to" side of the pair)
    last_harmony_frac: float = 0.0
    emergent: float = 0.0
    W_trace: float = 0.0
    W_strongest: tuple = (0, 0, 0.0)


class Cortex:
    """The trinity, composed.

    Usage:
        cx = Cortex().boot()
        for ch in "t h e c r e a t u r e":
            cx.step_char(ch)
        print(cx.status().emergent)
    """

    def __init__(
        self,
        ao: Optional[AO5Element] = None,
        hebbian: Optional[HebbianField] = None,
        alpha: float = 1.0, beta: float = 1.0, gamma: float = 2.0,
    ) -> None:
        # Composition spine -- ticks Gen11 heartbeat, brain, body per symbol.
        self.ao = ao if ao is not None else AO5Element()
        # Learning -- persistent 5x5 coupling that grows with HARMONY.
        self.hebbian = hebbian if hebbian is not None else HebbianField()
        # Glue coefficients: alpha + beta are linear weights on (row, col)
        # Hebbian strengths; gamma is the quadratic cross-term weight.
        self.alpha = alpha
        self.beta  = beta
        self.gamma = gamma

        self.state = CortexState()
        # Track the previous operator so each AO tick gives us a PAIR (b, d).
        self._prev_op: Optional[int] = None

    # ── Boot ────────────────────────────────────────────────────────

    def boot(self) -> "Cortex":
        self.ao.boot()
        return self

    # ── One symbol ──────────────────────────────────────────────────

    def step_symbol(self, symbol_index: int) -> CortexState:
        """One full trinity tick on a single symbol 0..25.

        1. AO composition  -> this tick's d2_op
        2. Form pair (prev_op, d2_op), lift to 5D profiles
        3. Hebbian update on the pair
        4. Quadratic glue over (row sum of W, col sum of W) -> emergent
        """
        # (1) Composition spine
        r = self.ao.process_symbol(symbol_index)
        d_op = r["d2_op"]
        b_op = self._prev_op if self._prev_op is not None else r["current_op"]
        self._prev_op = d_op

        # (2) Profile broadcast (5D from one operator per side)
        ops_a = _operator_to_profile(b_op)
        ops_b = _operator_to_profile(d_op)

        # (3) Hebbian update -- returns (harmony_frac, interaction_matrix)
        h_frac, _ = self.hebbian.update(ops_a, ops_b, lens="tsml")

        # (4) Quadratic glue: use the DIAGONAL Hebbian strength.  The diagonal
        # W[d][d] is "dim d couples to itself in this creature" -- i.e. the
        # self-coherence of each dim's lived HARMONY history.  Split into two
        # halves so F3 and F4 have something independent to see.
        #
        #   f3 = mean of W over the first two diagonal cells (early dims)
        #   f4 = mean of W over the last two diagonal cells  (late dims)
        # The "middle" dim (depth=2) is shared; that's fine -- the cross-term
        # just gets a gentle weight boost when ALL dims are learning.
        diag = [self.hebbian.W[d][d] for d in range(DIM)]
        f3_val = (diag[0] + diag[1]) / 2.0
        f4_val = (diag[3] + diag[4]) / 2.0

        emergent = quadratic_glue(f3_val, f4_val,
                                  alpha=self.alpha, beta=self.beta, gamma=self.gamma)

        # (5) Update public state
        st = self.state
        st.tick += 1
        st.last_b = b_op
        st.last_d = d_op
        st.last_harmony_frac = h_frac
        st.emergent = emergent
        st.W_trace = self.hebbian.trace()
        st.W_strongest = self.hebbian.strongest_pair()
        return st

    # ── Sugar: step a single character ─────────────────────────────

    def step_char(self, ch: str) -> Optional[CortexState]:
        """Step one character (a..z only; others return None unchanged)."""
        if not ch:
            return None
        idx = ord(ch.lower()) - ord('a')
        if not (0 <= idx < 26):
            return None
        return self.step_symbol(idx)

    # ── Sugar: step a whole text ────────────────────────────────────

    def step_text(self, text: str) -> List[CortexState]:
        out = []
        for ch in text.lower():
            idx = ord(ch) - ord('a')
            if 0 <= idx < 26:
                out.append(self.step_symbol(idx))
        return out

    # ── Status ──────────────────────────────────────────────────────

    def status(self) -> CortexState:
        return self.state

    def snapshot(self) -> Dict[str, Any]:
        """Full snapshot -- includes AO status, Hebbian weights, emergent signal."""
        ao_s = self.ao.status()
        return {
            "tick": self.state.tick,
            "emergent": self.state.emergent,
            "last_pair": (OP_NAMES[self.state.last_b], OP_NAMES[self.state.last_d]),
            "last_harmony_frac": self.state.last_harmony_frac,
            "W_trace": self.state.W_trace,
            "W_strongest": {
                "d_a": self.state.W_strongest[0],
                "d_b": self.state.W_strongest[1],
                "value": self.state.W_strongest[2],
            },
            "ao": {
                "op": OP_NAMES[ao_s.current_op],
                "coherence": ao_s.coherence,
                "breath": ao_s.breath,
                "tl_total": ao_s.tl_total,
            },
            "hebbian": self.hebbian.snapshot(),
        }


# ── Self-test ────────────────────────────────────────────────────────

def _smoke() -> None:
    cx = Cortex().boot()

    # Phase 1: cold boot -- emergent should start exactly at zero.
    assert cx.state.emergent == 0.0, f"cold emergent should be 0, got {cx.state.emergent}"

    # Phase 2: drive him with a coherence-rich text (repeats of "harmony" etc.)
    # The Gen11 D2 pipeline will produce real operators; Hebbian will learn
    # whatever pairs actually land in HARMONY for this trajectory.
    for _ in range(20):
        cx.step_text("coherencekeeper harmony lattice progress harmony")

    mid_emergent = cx.state.emergent
    mid_trace = cx.state.W_trace

    # Phase 3: drive him further with the same text -- emergent should rise
    # or at least not collapse (Hebbian has had more reward; glue compounds).
    for _ in range(20):
        cx.step_text("coherencekeeper harmony lattice progress harmony")
    late_emergent = cx.state.emergent
    late_trace = cx.state.W_trace

    # Assertions
    assert late_trace >= mid_trace - 1e-6, (
        f"W trace should not collapse: mid={mid_trace:.4f} late={late_trace:.4f}"
    )
    assert late_emergent >= mid_emergent - 1e-6, (
        f"emergent should not collapse: mid={mid_emergent:.4f} late={late_emergent:.4f}"
    )
    # At SOME point he should have learned something.
    assert late_trace > 0.0 or mid_trace > 0.0, "W trace never grew -- no learning happened"

    snap = cx.snapshot()
    assert snap["tick"] > 0
    assert isinstance(snap["emergent"], float)

    print(f"cortex smoke PASS: tick={snap['tick']}  "
          f"emergent={snap['emergent']:.4f}  W_trace={snap['W_trace']:.4f}  "
          f"strongest_pair=({snap['W_strongest']['d_a']},{snap['W_strongest']['d_b']})="
          f"{snap['W_strongest']['value']:.3f}")


if __name__ == "__main__":
    _smoke()
