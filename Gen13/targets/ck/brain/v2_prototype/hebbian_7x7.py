"""
hebbian_7x7.py -- 7x7 Hebbian field (CK v2 cortex prototype).

Generalizes Gen13/targets/ck/brain/hebbian_5x5_cl.py from DIM=5 to DIM=7.
The math is identical; only the dimension changes.

W[d_a][d_b] in [-CLAMP, +CLAMP] for d_a, d_b in {0..6}.
Hebbian update: dW = eta * reward - decay * W (Oja-style).

For the prototype, the "reward" is a simple HARMONY signal: when an
operator pair (b, d) projects to dim_a, dim_b such that the CL table
returns HARMONY, reward = 1; else 0.  This matches the 5-dim semantics.

The actual TSML/BHML interaction matrices for 7-dim profiles aren't
defined in the existing code (they're 10x10 over operators on Z/10Z).
This prototype just uses single-operator -> single-dim projection (via
OP_TO_DIM_7) and updates the corresponding W entry; future work will
extend the interaction-matrix generalization.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import List, Sequence, Tuple

from ao_7element import OP_TO_DIM_7, DIM_NAMES_7, DIM_7

DEFAULT_ETA = 0.005
DEFAULT_DECAY = 0.02
DEFAULT_CLAMP = 1.0


@dataclass
class HebbianField7:
    """7x7 Hebbian field for the v2 cortex prototype."""
    W: List[List[float]] = field(
        default_factory=lambda: [[0.0] * DIM_7 for _ in range(DIM_7)]
    )
    eta: float = DEFAULT_ETA
    decay: float = DEFAULT_DECAY
    clamp: float = DEFAULT_CLAMP
    ticks: int = 0
    harmony_hits: int = 0

    def update_pair(self, op_b: int, op_d: int, harmonious: bool = None) -> None:
        """One Hebbian update on the operator pair (op_b, op_d).

        harmonious: optional override.  If None, defaults to True only if
        either op equals HARMONY=7 (simple proxy for the 5-dim CL table
        check).
        """
        d_a = OP_TO_DIM_7.get(op_b, 0)
        d_b = OP_TO_DIM_7.get(op_d, 0)

        if harmonious is None:
            harmonious = (op_b == 7) or (op_d == 7)

        reward = 1.0 if harmonious else 0.0
        dw = self.eta * reward - self.decay * self.W[d_a][d_b]
        self.W[d_a][d_b] += dw
        # Clamp
        if self.W[d_a][d_b] > self.clamp:
            self.W[d_a][d_b] = self.clamp
        elif self.W[d_a][d_b] < -self.clamp:
            self.W[d_a][d_b] = -self.clamp

        # Decay all other entries (passive)
        for d_i in range(DIM_7):
            for d_j in range(DIM_7):
                if (d_i, d_j) == (d_a, d_b):
                    continue
                self.W[d_i][d_j] *= (1.0 - self.decay * 0.1)  # 10x slower decay off-target
                if self.W[d_i][d_j] > self.clamp:
                    self.W[d_i][d_j] = self.clamp
                elif self.W[d_i][d_j] < -self.clamp:
                    self.W[d_i][d_j] = -self.clamp

        self.ticks += 1
        if harmonious:
            self.harmony_hits += 1

    def W_trace(self) -> float:
        return sum(self.W[i][i] for i in range(DIM_7))

    def mean_abs_W(self) -> float:
        total = sum(abs(self.W[i][j]) for i in range(DIM_7) for j in range(DIM_7))
        return total / (DIM_7 * DIM_7)

    def harmony_rate(self) -> float:
        if self.ticks == 0:
            return 0.0
        return self.harmony_hits / self.ticks

    def strongest_pair(self) -> Tuple[int, int, float]:
        best = (0, 0, 0.0)
        for d_a in range(DIM_7):
            for d_b in range(DIM_7):
                if abs(self.W[d_a][d_b]) > abs(best[2]):
                    best = (d_a, d_b, self.W[d_a][d_b])
        return best

    def to_dict(self) -> dict:
        return {
            "W": [row[:] for row in self.W],
            "eta": self.eta,
            "decay": self.decay,
            "clamp": self.clamp,
            "ticks": self.ticks,
            "harmony_hits": self.harmony_hits,
            "dim": DIM_7,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "HebbianField7":
        f = cls(
            W=[row[:] for row in d.get("W", [[0.0] * DIM_7 for _ in range(DIM_7)])],
            eta=d.get("eta", DEFAULT_ETA),
            decay=d.get("decay", DEFAULT_DECAY),
            clamp=d.get("clamp", DEFAULT_CLAMP),
        )
        f.ticks = d.get("ticks", 0)
        f.harmony_hits = d.get("harmony_hits", 0)
        return f

    @classmethod
    def from_5x5_embedding(cls, W_5x5: List[List[float]]) -> "HebbianField7":
        """Migration helper: embed an existing 5x5 W matrix in the
        top-left of a new 7x7.  Preserves the 5-dim learning while
        adding 2 new dimensions starting at zero."""
        if len(W_5x5) != 5 or len(W_5x5[0]) != 5:
            raise ValueError("W_5x5 must be 5x5")
        f = cls()
        for i in range(5):
            for j in range(5):
                f.W[i][j] = W_5x5[i][j]
        return f


def diagnostics():
    f = HebbianField7()
    f.update_pair(7, 7, harmonious=True)  # HARMONY-HARMONY
    f.update_pair(3, 7, harmonious=True)  # PROGRESS-HARMONY
    f.update_pair(0, 0, harmonious=False) # VOID-VOID
    print(f"After 3 updates:")
    print(f"  W_trace = {f.W_trace():.4f}")
    print(f"  mean|W| = {f.mean_abs_W():.4f}")
    print(f"  strongest = {f.strongest_pair()}")
    print(f"  harmony_rate = {f.harmony_rate():.4f}")
    print(f"\nW matrix:")
    for i, row in enumerate(f.W):
        print(f"  {DIM_NAMES_7[i]:<11}: " + ", ".join(f"{w:+.4f}" for w in row))


if __name__ == "__main__":
    diagnostics()
