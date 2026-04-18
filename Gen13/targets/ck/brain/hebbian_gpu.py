# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
hebbian_gpu.py -- GPU-backed Hebbian 5x5 CL field with clean NumPy fallback.

Why this exists
---------------
The CPU hebbian_5x5_cl.py iterates `for d_a in range(5): for d_b in range(5):`
inside the tick.  That's fine for throughput (25 cells is nothing) but it
KEEPS the learning substrate stuck on the CPU bus while the "doing" side
(becoming_device.cu / doing.cu / force9_cuda.cu) lives on the GPU.

The swarm vision is that doing runs on the GPU and brain runs on the same
bus so the outer product + decay tensor ops are just another kernel call
alongside the doing kernels.  This module delivers that:

    dW = eta * reward - decay * W          # fully vectorized
    W  = clip(W + dW, -clamp, +clamp)

with a single xp.where() doing the reward mask and xp being CuPy when
available or NumPy when not.  The CPU path is bit-for-bit consistent with
hebbian_5x5_cl.py so a swarm on a GPU-less machine behaves identically.

Invariants:
  * snapshot().backend reports which bus did the work ('cupy' | 'numpy').
  * Values match the CPU implementation to within float round-off.
  * No global state; multiple fields can run side-by-side on different
    lenses (TSML / BHML) without interfering.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Any, List, Optional, Sequence, Tuple

# Choose backend.  We try CuPy; if it isn't importable or the runtime has
# no working device, we silently fall back to NumPy.  This is resolved
# once at module import time.
_BACKEND_NAME = "numpy"
try:
    import cupy as _xp
    # Touch a tiny array to make sure CUDA actually works (driver present,
    # device visible).  If this raises, fall back to NumPy.
    _ = _xp.asarray([0.0], dtype=_xp.float32).sum()
    _BACKEND_NAME = "cupy"
except Exception:
    import numpy as _xp  # type: ignore
    _BACKEND_NAME = "numpy"


# ── Reuse lens tables from the CPU module ───────────────────────────

_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
if _BRAIN_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_DIR)

from ck_sim.ck_sim_heartbeat import HARMONY  # noqa: E402
from ck_sim.being.ck_olfactory import (       # noqa: E402
    interaction_matrix_tsml,
    interaction_matrix_bhml,
    DIM_NAMES,
)


# ── Parameters (mirror hebbian_5x5_cl.py) ───────────────────────────

DIM = 5
DEFAULT_ETA = 0.005
DEFAULT_DECAY = 0.02
DEFAULT_CLAMP = 1.0


# ── GPU / CPU field ─────────────────────────────────────────────────

@dataclass
class HebbianGPU:
    """Persistent 5x5 coupling tensor, vectorized on CuPy or NumPy."""
    eta: float = DEFAULT_ETA
    decay: float = DEFAULT_DECAY
    clamp: float = DEFAULT_CLAMP
    ticks: int = 0
    harmony_hits: int = 0
    # W is stored on the selected backend.  We convert at snapshot time.
    _W: Any = None

    def __post_init__(self) -> None:
        if self._W is None:
            self._W = _xp.zeros((DIM, DIM), dtype=_xp.float32)

    @property
    def backend(self) -> str:
        """'cupy' if GPU, 'numpy' if CPU fallback."""
        return _BACKEND_NAME

    # ── One Hebbian update ──────────────────────────────────────────

    def update(
        self,
        ops_a: Sequence[int],
        ops_b: Sequence[int],
        lens: str = "tsml",
    ) -> Tuple[float, List[List[int]]]:
        """One vectorized Hebbian tick.  Same contract as HebbianField.update().

        Returns (harmony_fraction, interaction_matrix).
        """
        if len(ops_a) != DIM or len(ops_b) != DIM:
            raise ValueError(f"ops_a/ops_b must be length {DIM}")

        if lens == "bhml":
            matrix, _ = interaction_matrix_bhml(list(ops_a), list(ops_b))
            h_count = sum(1 for d1 in range(DIM) for d2 in range(DIM)
                          if matrix[d1][d2] == HARMONY)
            h_frac = h_count / 25.0
        else:
            matrix, h_frac = interaction_matrix_tsml(list(ops_a), list(ops_b))

        # Build reward tensor on backend.  matrix is Python list-of-lists; we
        # convert once per tick (cheap for 5x5).
        # HARMONY is an int code; matrix cells that equal it -> reward = 1, else 0.
        reward_host = [[1.0 if matrix[d_a][d_b] == HARMONY else 0.0
                        for d_b in range(DIM)] for d_a in range(DIM)]
        reward = _xp.asarray(reward_host, dtype=_xp.float32)

        # Vectorized Oja-style update.
        dW = self.eta * reward - self.decay * self._W
        self._W = self._W + dW
        # Clamp.
        self._W = _xp.clip(self._W, -self.clamp, self.clamp)

        self.ticks += 1
        self.harmony_hits += int(round(h_frac * 25))
        return h_frac, matrix

    # ── Readouts ────────────────────────────────────────────────────

    def harmony_rate(self) -> float:
        total_cells = self.ticks * DIM * DIM
        if total_cells == 0:
            return 0.0
        return self.harmony_hits / total_cells

    def trace(self) -> float:
        return float(_xp.trace(self._W).get() if _BACKEND_NAME == "cupy"
                     else _xp.trace(self._W))

    def strongest_pair(self) -> Tuple[int, int, float]:
        W = self._W.get() if _BACKEND_NAME == "cupy" else self._W
        flat = abs(W).argmax()
        d_a, d_b = int(flat // DIM), int(flat % DIM)
        return d_a, d_b, float(W[d_a, d_b])

    def row_strength(self, d_a: int) -> float:
        W = self._W.get() if _BACKEND_NAME == "cupy" else self._W
        return float(W[d_a].mean())

    def col_strength(self, d_b: int) -> float:
        W = self._W.get() if _BACKEND_NAME == "cupy" else self._W
        return float(W[:, d_b].mean())

    def W_as_list(self) -> List[List[float]]:
        W = self._W.get() if _BACKEND_NAME == "cupy" else self._W
        return [[float(W[d_a, d_b]) for d_b in range(DIM)] for d_a in range(DIM)]

    def snapshot(self) -> dict:
        return {
            "backend": _BACKEND_NAME,
            "ticks": self.ticks,
            "harmony_rate": self.harmony_rate(),
            "trace": self.trace(),
            "strongest_pair": self.strongest_pair(),
            "row_strengths": [self.row_strength(d) for d in range(DIM)],
            "col_strengths": [self.col_strength(d) for d in range(DIM)],
            "dim_names": list(DIM_NAMES),
            "W": self.W_as_list(),
        }

    def reset(self) -> None:
        self._W = _xp.zeros((DIM, DIM), dtype=_xp.float32)
        self.ticks = 0
        self.harmony_hits = 0


# ── Convenience factory ──────────────────────────────────────────────

def fresh(eta: float = DEFAULT_ETA, decay: float = DEFAULT_DECAY) -> HebbianGPU:
    return HebbianGPU(eta=eta, decay=decay)


# ── Self-test ────────────────────────────────────────────────────────

def _smoke() -> None:
    """Compare GPU/CPU field against CPU-only reference for numerical parity."""
    from hebbian_5x5_cl import HebbianField

    H = HARMONY
    gpu = HebbianGPU(eta=0.1, decay=0.001)
    ref = HebbianField(eta=0.1, decay=0.001)

    ops_harmony = [H, H, H, H, H]
    for _ in range(50):
        gpu.update(ops_harmony, ops_harmony)
        ref.update(ops_harmony, ops_harmony)

    Wg = gpu.W_as_list()
    Wr = ref.W
    max_diff = 0.0
    for d_a in range(DIM):
        for d_b in range(DIM):
            d = abs(Wg[d_a][d_b] - Wr[d_a][d_b])
            if d > max_diff:
                max_diff = d

    print(f"hebbian_gpu smoke: backend={_BACKEND_NAME} ticks={gpu.ticks} "
          f"strongest={gpu.strongest_pair()} max_diff_vs_cpu_ref={max_diff:.3e}")
    assert max_diff < 1e-3, f"GPU and CPU diverged: max|diff|={max_diff}"
    print("hebbian_gpu smoke PASS")


if __name__ == "__main__":
    _smoke()
