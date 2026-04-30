"""
cortex_7d.py -- 7-dim cortex prototype (CK v2).

The trinity for 7-dim:
  AO 7-element  -- composition spine (5 inherited + intent + echo)
  Hebbian 7x7   -- learning matrix (49 coefficients)
  Quadratic glue -- 2->3 bridge over diag(W) split into f3 (intent-side) +
                   f4 (echo-side)

This is a SIMPLIFIED prototype.  The live 5-dim cortex uses AO5Element's
process_symbol pipeline and a 5x5 interaction matrix lookup.  This 7-dim
prototype skips the full AO machinery and just operates on operator
streams directly:

  step_op_pair(b, d)  -- one Hebbian update on operator pair (b, d)
  step_text(text)     -- emit a stream of operators from text via simple
                         char-to-op hashing, then step each pair

This is enough to test the math (Phi-proxy comparison), check the
migration from 5-dim, and demonstrate emergent behavior.  The full
trinity wiring (AO 7-element going through process_symbol like AO 5-element
does) is paper 7 §6 step 1, ~1 day of work.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# Ensure brain dir is on path for quadratic_glue import
_BRAIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _BRAIN_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_DIR)

from quadratic_glue import quadratic_glue
from ao_7element import OP_TO_DIM_7, DIM_NAMES_7, DIM_7
from hebbian_7x7 import HebbianField7

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]


@dataclass
class CortexState7:
    tick: int = 0
    last_b: int = 7  # HARMONY
    last_d: int = 7
    last_harmony_frac: float = 0.0
    emergent: float = 0.0
    W_trace: float = 0.0
    W_strongest: tuple = (0, 0, 0.0)


class Cortex7D:
    """7-dim cortex (v2 prototype). Same trinity, wider substrate."""

    def __init__(
        self,
        hebbian: Optional[HebbianField7] = None,
        alpha: float = 1.0,
        beta: float = 1.0,
        gamma: float = 2.0,
    ) -> None:
        self.hebbian = hebbian if hebbian is not None else HebbianField7()
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.state = CortexState7()
        self._prev_op: Optional[int] = None

    def boot(self) -> "Cortex7D":
        return self

    def step_op_pair(self, b_op: int, d_op: int) -> CortexState7:
        """One Hebbian update on operator pair, plus quadratic glue lift."""
        # Hebbian update; "harmonious" = either op is HARMONY (matches 5-dim
        # logic via the CL table where HARMONY-rows + HARMONY-cols dominate)
        harmonious = (b_op == 7) or (d_op == 7)
        self.hebbian.update_pair(b_op, d_op, harmonious=harmonious)

        # Quadratic glue: split diag into early dims (0..2) and late dims (3..6).
        # f3 = mean of W[0:3][diag] (aperture+pressure+depth side)
        # f4 = mean of W[3:7][diag] (binding+continuity+intent+echo side)
        # The split treats the "early/static" axes vs the "later/temporal" axes.
        diag = [self.hebbian.W[d][d] for d in range(DIM_7)]
        f3_val = sum(diag[0:3]) / 3.0
        f4_val = sum(diag[3:7]) / 4.0
        emergent = quadratic_glue(f3_val, f4_val,
                                  alpha=self.alpha, beta=self.beta, gamma=self.gamma)

        # Update state
        self.state.tick += 1
        self.state.last_b = b_op
        self.state.last_d = d_op
        self.state.last_harmony_frac = 1.0 if harmonious else 0.0
        self.state.emergent = emergent
        self.state.W_trace = self.hebbian.W_trace()
        self.state.W_strongest = self.hebbian.strongest_pair()
        return self.state

    def step_text(self, text: str) -> List[CortexState7]:
        """Emit operators from text and step each pair.

        Simple char->op hash (same scheme as 5-dim cortex's step_text):
        char index 0..25 maps onto operators 0..9 by mod 10.
        """
        out = []
        ops = []
        for ch in text.lower():
            idx = ord(ch) - ord('a')
            if 0 <= idx < 26:
                ops.append(idx % 10)
        # Step pairs
        for i in range(len(ops) - 1):
            b = ops[i]
            d = ops[i + 1]
            out.append(self.step_op_pair(b, d))
        if ops:
            self._prev_op = ops[-1]
        return out

    def status(self) -> CortexState7:
        return self.state

    def snapshot(self) -> Dict:
        return {
            "tick": self.state.tick,
            "emergent": self.state.emergent,
            "last_pair": (OP_NAMES[self.state.last_b],
                          OP_NAMES[self.state.last_d]),
            "W_trace": self.state.W_trace,
            "W_strongest": {
                "d_a": self.state.W_strongest[0],
                "d_b": self.state.W_strongest[1],
                "value": self.state.W_strongest[2],
            },
            "hebbian": self.hebbian.to_dict(),
            "dim": DIM_7,
        }


def diagnostics():
    cx = Cortex7D().boot()
    test_text = "the depth two cluster shows m squared equals plus or minus identity"
    states = cx.step_text(test_text)
    print(f"Cortex 7D smoke test:")
    print(f"  ticks: {len(states)}")
    print(f"  W_trace: {cx.state.W_trace:.4f}")
    print(f"  emergent: {cx.state.emergent:.4f}")
    print(f"  strongest: dim {cx.state.W_strongest[0]}({DIM_NAMES_7[cx.state.W_strongest[0]]}) "
          f"-> dim {cx.state.W_strongest[1]}({DIM_NAMES_7[cx.state.W_strongest[1]]}) "
          f"@ {cx.state.W_strongest[2]:.4f}")
    print()
    print("W matrix:")
    for i, row in enumerate(cx.hebbian.W):
        print(f"  {DIM_NAMES_7[i]:<11}: " + ", ".join(f"{w:+.4f}" for w in row))


if __name__ == "__main__":
    diagnostics()
