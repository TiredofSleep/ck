# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_cloud_curvature.py -- Cloud D2 Curvature Encoding
=====================================================
Operator: COUNTER (2) -- measuring curvature in cloud dynamics.

Multi-scale D2 curvature from optical flow fields:

  Spatial D2:   Second derivative of force vectors across patch grid.
                ∇²F = F[r-1,c] + F[r+1,c] + F[r,c-1] + F[r,c+1] - 4·F[r,c]
                Measures how a patch's dynamics differ from neighbors.

  Temporal D2:  v[t-2] - 2·v[t-1] + v[t]  (same formula as all CK D2)
                Measures acceleration/deceleration of flow per patch.

  Operator classification:  5D D2 vector → argmax + sign → operator (0-9)
                            Exact same D2_OP_MAP as ck_sim_d2.py.

The output: one operator per patch per frame.  These form operator
sequences that CK can learn from -- exactly as if reading text or
processing game telemetry.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from collections import deque
from typing import Dict, List, Optional, Tuple

import numpy as np

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET, OP_NAMES,
    CL, compose,
)
from ck_sim.ck_sim_d2 import D2_OP_MAP


# ================================================================
#  CONSTANTS
# ================================================================

D2_EPSILON = 0.01               # Below this magnitude → VOID
TEMPORAL_WINDOW = 3             # Frames needed for temporal D2
MAX_HISTORY = 64                # Max frames of patch history


# ================================================================
#  SPATIAL D2: Curvature across the patch grid
# ================================================================

def spatial_d2(force_grid: np.ndarray) -> np.ndarray:
    """Compute spatial second derivative (Laplacian) of 5D force vectors.

    Args:
        force_grid: (rows, cols, 5) array of force vectors from patches.

    Returns:
        (rows, cols, 5) array of spatial D2 vectors.
        Interior uses 4-connectivity Laplacian.
        Boundary clamps to zero.
    """
    rows, cols, dims = force_grid.shape
    assert dims == 5, f"Expected 5D force vectors, got {dims}D"

    d2 = np.zeros_like(force_grid)

    if rows < 3 or cols < 3:
        return d2

    # Laplacian: sum of 4 neighbors minus 4× center
    d2[1:-1, 1:-1, :] = (
        force_grid[:-2, 1:-1, :] +   # up
        force_grid[2:, 1:-1, :] +     # down
        force_grid[1:-1, :-2, :] +    # left
        force_grid[1:-1, 2:, :] -     # right
        4.0 * force_grid[1:-1, 1:-1, :]  # center
    )

    return d2


def spatial_d2_magnitude(d2_grid: np.ndarray) -> np.ndarray:
    """Magnitude of spatial D2 at each patch: sum of absolute values.

    Args:
        d2_grid: (rows, cols, 5) spatial D2 vectors

    Returns:
        (rows, cols) magnitude array
    """
    return np.sum(np.abs(d2_grid), axis=2)


# ================================================================
#  TEMPORAL D2: Curvature across frames
# ================================================================

def temporal_d2(force_t0: np.ndarray, force_t1: np.ndarray,
                force_t2: np.ndarray) -> np.ndarray:
    """Temporal second derivative: v[t-2] - 2·v[t-1] + v[t].

    Same D2 formula used everywhere in CK. Applied per-patch.

    Args:
        force_t0: (rows, cols, 5) force grid at time t-2
        force_t1: (rows, cols, 5) force grid at time t-1
        force_t2: (rows, cols, 5) force grid at time t (current)

    Returns:
        (rows, cols, 5) temporal D2 vectors.
    """
    return force_t0 - 2.0 * force_t1 + force_t2


def temporal_d2_magnitude(d2_temporal: np.ndarray) -> np.ndarray:
    """Magnitude of temporal D2: sum of abs per patch."""
    return np.sum(np.abs(d2_temporal), axis=2)


# ================================================================
#  OPERATOR CLASSIFICATION
# ================================================================

def classify_d2_vector(d2_vec: np.ndarray) -> int:
    """Classify a single 5D D2 vector to an operator (0-9).

    Same argmax + sign logic as ck_sim_d2.py.

    Args:
        d2_vec: length-5 array

    Returns:
        operator index (0-9)
    """
    mag = float(np.sum(np.abs(d2_vec)))
    if mag < D2_EPSILON:
        return VOID

    max_abs = 0.0
    max_dim = 0
    for dim in range(5):
        a = abs(float(d2_vec[dim]))
        if a > max_abs:
            max_abs = a
            max_dim = dim

    sign_idx = 0 if d2_vec[max_dim] >= 0 else 1
    return D2_OP_MAP[max_dim][sign_idx]


def classify_grid(d2_grid: np.ndarray) -> np.ndarray:
    """Classify every patch in a D2 grid to operators.

    Args:
        d2_grid: (rows, cols, 5) D2 vectors

    Returns:
        (rows, cols) int array of operator indices.
    """
    rows, cols, _ = d2_grid.shape
    ops = np.zeros((rows, cols), dtype=np.int32)

    for r in range(rows):
        for c in range(cols):
            ops[r, c] = classify_d2_vector(d2_grid[r, c])

    return ops


def operator_sequence_from_grid(op_grid: np.ndarray) -> List[int]:
    """Flatten operator grid to sequence (row-major).

    This produces a sequence CK can process exactly like text operators.
    """
    return op_grid.flatten().tolist()


# ================================================================
#  COMBINED D2: Spatial + Temporal → Operator Sequence
# ================================================================

def combined_d2(spatial: np.ndarray, temporal: np.ndarray,
                spatial_weight: float = 0.5) -> np.ndarray:
    """Weighted combination of spatial and temporal D2.

    Args:
        spatial: (rows, cols, 5) spatial D2
        temporal: (rows, cols, 5) temporal D2
        spatial_weight: 0.0 = all temporal, 1.0 = all spatial

    Returns:
        (rows, cols, 5) combined D2
    """
    tw = 1.0 - spatial_weight
    return spatial_weight * spatial + tw * temporal


# ================================================================
#  CURVATURE TRACKER (stateful, multi-frame)
# ================================================================

class CloudCurvatureTracker:
    """Stateful D2 curvature processor for cloud flow sequences.

    Maintains force grid history for temporal D2 computation.
    Produces both spatial and temporal D2, classifies to operators.

    Usage:
        tracker = CloudCurvatureTracker()
        for patches in flow_tracker_output:
            result = tracker.feed(patches)
            if result:
                ops = result['operators']       # operator grid
                seq = result['sequence']         # flattened sequence
                sp_d2 = result['spatial_d2']     # spatial D2 grid
                tm_d2 = result['temporal_d2']    # temporal D2 grid
    """

    def __init__(self, spatial_weight: float = 0.5,
                 max_history: int = MAX_HISTORY):
        self.spatial_weight = spatial_weight
        self._force_history = deque(maxlen=max_history)
        self._rows = 0
        self._cols = 0
        self._frame_count = 0

    def feed(self, patches: list) -> Optional[dict]:
        """Feed one frame's patches. Returns result when D2 is computable.

        Args:
            patches: list of FlowPatch objects from decompose_flow()

        Returns:
            dict with keys: operators, sequence, spatial_d2, temporal_d2,
            combined_d2, spatial_mag, temporal_mag, force_grid.
            Or None if not enough frames yet.
        """
        if not patches:
            return None

        # Determine grid dimensions
        max_r = max(p.row for p in patches)
        max_c = max(p.col for p in patches)
        rows = max_r + 1
        cols = max_c + 1

        # Build force grid from patches
        force_grid = np.zeros((rows, cols, 5), dtype=np.float32)
        for p in patches:
            force_grid[p.row, p.col] = p.force_vector

        self._force_history.append(force_grid)
        self._rows = rows
        self._cols = cols
        self._frame_count += 1

        # Spatial D2 is always available
        sp = spatial_d2(force_grid)
        sp_mag = spatial_d2_magnitude(sp)

        # Temporal D2 needs 3+ frames
        if len(self._force_history) < TEMPORAL_WINDOW:
            # Only spatial available
            ops = classify_grid(sp)
            seq = operator_sequence_from_grid(ops)
            return {
                'operators': ops,
                'sequence': seq,
                'spatial_d2': sp,
                'temporal_d2': None,
                'combined_d2': sp,
                'spatial_mag': sp_mag,
                'temporal_mag': None,
                'force_grid': force_grid,
                'frame': self._frame_count,
            }

        # Temporal D2
        t0 = self._force_history[-3]
        t1 = self._force_history[-2]
        t2 = self._force_history[-1]

        # Handle grid size changes (clip to minimum)
        min_r = min(t0.shape[0], t1.shape[0], t2.shape[0])
        min_c = min(t0.shape[1], t1.shape[1], t2.shape[1])
        t0 = t0[:min_r, :min_c, :]
        t1 = t1[:min_r, :min_c, :]
        t2 = t2[:min_r, :min_c, :]
        sp = sp[:min_r, :min_c, :]

        tm = temporal_d2(t0, t1, t2)
        tm_mag = temporal_d2_magnitude(tm)

        # Combined
        comb = combined_d2(sp, tm, self.spatial_weight)

        # Classify
        ops = classify_grid(comb)
        seq = operator_sequence_from_grid(ops)

        return {
            'operators': ops,
            'sequence': seq,
            'spatial_d2': sp,
            'temporal_d2': tm,
            'combined_d2': comb,
            'spatial_mag': sp_mag[:min_r, :min_c],
            'temporal_mag': tm_mag,
            'force_grid': force_grid,
            'frame': self._frame_count,
        }

    @property
    def frame_count(self) -> int:
        return self._frame_count

    @property
    def grid_shape(self) -> Tuple[int, int]:
        return (self._rows, self._cols)

    def reset(self):
        """Clear state for new video."""
        self._force_history.clear()
        self._frame_count = 0
        self._rows = 0
        self._cols = 0


# ================================================================
#  COHERENCE COMPUTATION (from operator grid)
# ================================================================

def grid_coherence(op_grid: np.ndarray) -> float:
    """Compute coherence of an operator grid: harmony_count / total.

    Same definition as heartbeat coherence but spatial.
    """
    total = op_grid.size
    if total == 0:
        return 0.0
    harmony_count = int(np.sum(op_grid == HARMONY))
    return harmony_count / total


def sequence_coherence(seq: List[int], window: int = 32) -> float:
    """Coherence of operator sequence over a sliding window."""
    if not seq:
        return 0.0
    chunk = seq[-window:]
    harmony_count = sum(1 for op in chunk if op == HARMONY)
    return harmony_count / len(chunk)


# ================================================================
#  CLI: Demo
# ================================================================

if __name__ == '__main__':
    from ck_sim.ck_cloud_flow import (
        generate_cloud_frame_pair, horn_schunck, decompose_flow
    )

    print("=" * 60)
    print("CK CLOUD CURVATURE -- D2 from Cloud Dynamics")
    print("=" * 60)

    H, W = 64, 64
    tracker = CloudCurvatureTracker(spatial_weight=0.5)

    for i in range(5):
        # Generate frames with evolving flow
        f1, f2 = generate_cloud_frame_pair(
            H, W, 'vortex', strength=0.3 + i * 0.1, seed=i
        )
        u, v = horn_schunck(f1, f2, iterations=30)
        patches = decompose_flow(u, v, patch_size=8)

        result = tracker.feed(patches)
        if result:
            ops = result['operators']
            seq = result['sequence']
            coh = grid_coherence(ops)

            # Count operators
            op_counts = {}
            for op in seq:
                name = OP_NAMES[op]
                op_counts[name] = op_counts.get(name, 0) + 1

            print(f"\n  Frame {i}: grid={ops.shape}, "
                  f"coherence={coh:.3f}")
            print(f"    operators: {op_counts}")

    print(f"\n{'=' * 60}")
    print("  Cloud curvature encoding ready.")
    print(f"{'=' * 60}")
