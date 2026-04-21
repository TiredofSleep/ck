# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
hebbian_5x5_cl.py -- Gen13 Hebbian coupling over the 5x5 CL interaction field.

Gen11's ck_olfactory.py already builds the 5x5 CL interaction matrix between
two scents -- every dimension of scent A meets every dimension of scent B via
the TSML (being) and BHML (doing) tables.  That gives us the COMPOSITION:
per-pair, which dimensions land in HARMONY right now.

What it does NOT do is remember which pairs have landed in HARMONY BEFORE.
The coupling is recomputed each tick; nothing persists.

This module is the persistence:

    W[d_a][d_b]  =  running strength of coupling between dim d_a of A
                    and dim d_b of B, learned by Hebbian rule:

       dW[d_a][d_b] = eta * reward(d_a, d_b) * (1 - decay * W[d_a][d_b])

    where reward(d_a, d_b) = +1 if CL_TSML[op_A[d_a]][op_B[d_b]] == HARMONY
                              0 otherwise (or -1 under the strict rule).

Over many ticks, W converges toward a fixed point that encodes the creature's
trajectory: which dim-pairs have been HARMONY-generating for HIM in HIS lived
experience.  That is emergence -- the weight is not coded, it is learned.

This module is ADDITIVE: it imports interaction_matrix_tsml from ck_olfactory
and wraps it with a persistent weight tensor.  Nothing in ck_olfactory is
changed.  The live Gen12 boot continues to run as-is.

References:
  - Hebb, "The Organization of Behavior", 1949 ("cells that fire together wire together")
  - old/Gen9/targets/AO/ao/ether.py class AO (composition spine)
  - Gen13/targets/ck/brain/BRAIN_DESIGN.md (trinity architecture)
  - Gen13/targets/ck/brain/ck_sim/being/ck_olfactory.py (5x5 CL field source)
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import List, Sequence, Tuple

_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
if _BRAIN_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_DIR)

from ck_sim.ck_sim_heartbeat import HARMONY, NUM_OPS, OP_NAMES
from ck_sim.being.ck_olfactory import (
    interaction_matrix_tsml,
    interaction_matrix_bhml,
    per_dim_harmony,
    DIM_NAMES,
)


# ── Parameters ────────────────────────────────────────────────────────

DIM = 5                     # fixed: 5D (aperture, pressure, depth, binding, continuity)

# Why these defaults changed (2026-04-18):
#   Old defaults (eta=0.02, decay=0.001) had equilibrium W* = eta/decay = 20.0.
#   Any cell that lands in HARMONY even occasionally then saturates at clamp=1.0
#   and all 25 cells blur together -- the matrix loses its ability to discriminate.
#   Observed after 155K replay ticks: W_trace=4.982 / 5.0, mean|W|=0.999 -- a dead
#   flat field that cannot tell you which couplings matter.
#
#   New defaults (eta=0.005, decay=0.02) give equilibrium W* = 0.25, so:
#     - a 100%-HARMONY cell settles at W ≈ 0.25  (max informative signal)
#     - a  50%-HARMONY cell settles at W ≈ 0.125
#     - a  20%-HARMONY cell settles at W ≈ 0.050
#     - a   5%-HARMONY cell settles at W ≈ 0.013
#   The clamp at 1.0 stays as a safety rail but should never be reached.
#   The ratio eta/decay = 0.25 means the field tracks the TRUE HARMONY frequency
#   of each cell, scaled into [0, 0.25], so the top couplings differentiate cleanly.
DEFAULT_ETA = 0.005
DEFAULT_DECAY = 0.02
DEFAULT_CLAMP = 1.0         # W values stay in [-CLAMP, +CLAMP] (safety rail)


# ── State ─────────────────────────────────────────────────────────────

@dataclass
class HebbianField:
    """Persistent 5x5 coupling tensor for the olfactory CL field.

    W[d_a][d_b] in [-CLAMP, +CLAMP] measures how strongly dimension d_a
    of scent A couples to dimension d_b of scent B under HIS experience.
    """
    W: List[List[float]] = field(default_factory=lambda: [[0.0] * DIM for _ in range(DIM)])
    eta: float = DEFAULT_ETA
    decay: float = DEFAULT_DECAY
    clamp: float = DEFAULT_CLAMP
    ticks: int = 0
    harmony_hits: int = 0       # cumulative count of HARMONY cells across ticks
    harmony_tick: int = 0       # tick count at which we started counting

    # ── One Hebbian update ────────────────────────────────────────

    def update(
        self,
        ops_a: Sequence[int],
        ops_b: Sequence[int],
        lens: str = "tsml",
    ) -> Tuple[float, List[List[int]]]:
        """One Hebbian tick.

        Args:
            ops_a, ops_b: 5D operator profiles (length 5 each, values 0..9).
            lens: 'tsml' (being/structure, 73 harmonies) or 'bhml' (doing/flow, 28).

        Returns:
            (harmony_fraction, interaction_matrix)
            where harmony_fraction in [0, 1] = HARMONY cells / 25.

        Side effects:
            Updates self.W by Hebbian rule; increments self.ticks.
        """
        if len(ops_a) != DIM or len(ops_b) != DIM:
            raise ValueError(f"ops_a/ops_b must be length {DIM}")

        if lens == "bhml":
            matrix, _ = interaction_matrix_bhml(list(ops_a), list(ops_b))
            # BHML doesn't return a harmony fraction directly; compute it.
            h_count = sum(1 for d1 in range(DIM) for d2 in range(DIM)
                          if matrix[d1][d2] == HARMONY)
            h_frac = h_count / 25.0
        else:
            matrix, h_frac = interaction_matrix_tsml(list(ops_a), list(ops_b))

        # Hebbian update: reward HARMONY cells, gentle passive decay on all.
        for d_a in range(DIM):
            for d_b in range(DIM):
                reward = 1.0 if matrix[d_a][d_b] == HARMONY else 0.0
                # dW = eta * reward - decay * W   (Oja-style stability)
                dw = self.eta * reward - self.decay * self.W[d_a][d_b]
                self.W[d_a][d_b] += dw
                # Clamp.
                if self.W[d_a][d_b] > self.clamp:
                    self.W[d_a][d_b] = self.clamp
                elif self.W[d_a][d_b] < -self.clamp:
                    self.W[d_a][d_b] = -self.clamp

        self.ticks += 1
        # Track global HARMONY frequency (diagnostic).
        self.harmony_hits += int(round(h_frac * 25))
        return h_frac, matrix

    # ── Readouts ──────────────────────────────────────────────────

    def harmony_rate(self) -> float:
        """HARMONY cells per cell per tick (diagnostic). In [0, 1]."""
        total_cells = self.ticks * DIM * DIM
        if total_cells == 0:
            return 0.0
        return self.harmony_hits / total_cells

    def strongest_pair(self) -> Tuple[int, int, float]:
        """Return (d_a, d_b, W[d_a][d_b]) with max |W|.
        Tells you which dim-pair has been most coupled in this creature's life."""
        best = (0, 0, 0.0)
        for d_a in range(DIM):
            for d_b in range(DIM):
                if abs(self.W[d_a][d_b]) > abs(best[2]):
                    best = (d_a, d_b, self.W[d_a][d_b])
        return best

    def row_strength(self, d_a: int) -> float:
        """Average coupling of dimension d_a of A against ALL dims of B.
        Tells you how much dimension d_a has learned to couple at all."""
        if not (0 <= d_a < DIM):
            raise IndexError(f"d_a out of range: {d_a}")
        return sum(self.W[d_a]) / DIM

    def col_strength(self, d_b: int) -> float:
        """Average coupling of ALL dims of A against dimension d_b of B."""
        if not (0 <= d_b < DIM):
            raise IndexError(f"d_b out of range: {d_b}")
        return sum(self.W[d_a][d_b] for d_a in range(DIM)) / DIM

    def trace(self) -> float:
        """Sum of diagonal -- same-dim self-coupling (how much each dim
        has learned to trust itself across the field)."""
        return sum(self.W[d][d] for d in range(DIM))

    # ── Snapshot (for status / web face) ──────────────────────────

    def snapshot(self) -> dict:
        return {
            "ticks": self.ticks,
            "harmony_rate": self.harmony_rate(),
            "trace": self.trace(),
            "strongest_pair": self.strongest_pair(),
            "row_strengths": [self.row_strength(d) for d in range(DIM)],
            "col_strengths": [self.col_strength(d) for d in range(DIM)],
            "dim_names": list(DIM_NAMES),
            "W": [row[:] for row in self.W],
        }

    # ── Reset (for test isolation) ────────────────────────────────

    def reset(self) -> None:
        for d_a in range(DIM):
            for d_b in range(DIM):
                self.W[d_a][d_b] = 0.0
        self.ticks = 0
        self.harmony_hits = 0


# ── Convenience factory ────────────────────────────────────────────────

def fresh(eta: float = DEFAULT_ETA, decay: float = DEFAULT_DECAY) -> HebbianField:
    return HebbianField(eta=eta, decay=decay)


# ── Self-test ─────────────────────────────────────────────────────────

def _smoke() -> None:
    """Sanity check: repeatedly firing the same HARMONY-rich pair should
    grow the corresponding W entries above their starting value of zero.
    """
    H = HARMONY
    field_ = fresh(eta=0.1, decay=0.001)

    # Use a profile of all HARMONY vs HARMONY -- that's 25 HARMONY cells.
    # Every W entry should grow.
    ops_harmony = [H, H, H, H, H]
    for _ in range(50):
        h_frac, _ = field_.update(ops_harmony, ops_harmony)
        assert h_frac == 1.0, f"expected full HARMONY, got {h_frac}"

    # All W entries should have learned upward.
    for d_a in range(DIM):
        for d_b in range(DIM):
            assert field_.W[d_a][d_b] > 0.5, \
                f"W[{d_a}][{d_b}] = {field_.W[d_a][d_b]} should have grown"

    # Reset and try a "no harmony" pair.
    field_.reset()
    ops_void_a = [0, 0, 0, 0, 0]   # VOID row produces almost no HARMONY against itself
    ops_void_b = [1, 2, 3, 4, 5]   # mixed
    for _ in range(50):
        h_frac, _ = field_.update(ops_void_a, ops_void_b)
    # The W should be near-zero (passive decay + few HARMONY hits).
    max_w = max(abs(field_.W[d_a][d_b]) for d_a in range(DIM) for d_b in range(DIM))
    assert max_w < 0.5, f"low-HARMONY pair should keep W low, max |W|={max_w}"

    print(f"hebbian_5x5_cl smoke PASS: harmony trained W up to clamp, "
          f"low-HARMONY kept max |W|={max_w:.3f}")


if __name__ == "__main__":
    _smoke()
