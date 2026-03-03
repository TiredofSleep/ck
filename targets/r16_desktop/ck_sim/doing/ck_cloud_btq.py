# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_cloud_btq.py -- BTQ Mode Inference from Cloud Dynamics
==========================================================
Operator: HARMONY (7) -- the attractor state for all decisions.

Infers CK's Binary/Ternary/Quaternary decision mode from cloud
optical flow statistics.

Mode detection via dimensionless ratio:

    Θ = σ² / (|D2| · R + ε)

Where:
    σ²  = variance of speed across patches (turbulence)
    |D2| = mean D2 magnitude (curvature strength)
    R   = mean resultant length (directional coherence)
    ε   = small constant to prevent division by zero

Thresholds (from Celeste's spec, refined):
    Θ < 0.3  → Binary  (B) : stable, laminar, predictable
    Θ ∈ [0.3, 1.2) → Ternary (T) : balancing, transitional
    Θ ≥ 1.2  → Quaternary (Q) : turbulent, exploratory

This maps exactly onto CK's existing BTQ decision architecture.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from collections import deque
from typing import Dict, List, Optional, Tuple

import numpy as np

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, OP_NAMES,
)


# ================================================================
#  CONSTANTS
# ================================================================

# BTQ mode labels
MODE_BINARY = 'B'
MODE_TERNARY = 'T'
MODE_QUATERNARY = 'Q'

# Θ thresholds
THETA_B_MAX = 0.3              # Below this → Binary (stable/reactive)
THETA_T_MAX = 1.2              # Below this → Ternary (balancing)
                                # Above → Quaternary (exploring)

# Epsilon for division safety
THETA_EPSILON = 1e-6

# Smoothing for mode tracking
MODE_SMOOTH_WINDOW = 8         # Frames to average for mode stability
MODE_TRANSITION_THRESHOLD = 0.6  # 60% agreement needed for mode switch


# ================================================================
#  THETA COMPUTATION
# ================================================================

def compute_theta(speeds: np.ndarray, d2_magnitudes: np.ndarray,
                  coherences: np.ndarray) -> float:
    """Compute the dimensionless BTQ mode ratio Θ.

    Θ = σ²(speed) / (mean(|D2|) · mean(R) + ε)

    Args:
        speeds: (N,) array of patch speeds
        d2_magnitudes: (N,) array of D2 magnitudes per patch
        coherences: (N,) array of directional coherence per patch [0,1]

    Returns:
        Θ ratio (0 to ∞, typically 0-5)
    """
    if len(speeds) == 0:
        return 0.0

    sigma2 = float(np.var(speeds))
    mean_d2 = float(np.mean(d2_magnitudes))
    mean_R = float(np.mean(coherences))

    denom = mean_d2 * mean_R + THETA_EPSILON
    return sigma2 / denom


def classify_theta(theta: float) -> str:
    """Classify Θ ratio to BTQ mode.

    Args:
        theta: Θ ratio

    Returns:
        'B' (Binary), 'T' (Ternary), or 'Q' (Quaternary)
    """
    if theta < THETA_B_MAX:
        return MODE_BINARY
    elif theta < THETA_T_MAX:
        return MODE_TERNARY
    else:
        return MODE_QUATERNARY


# ================================================================
#  PATCH-LEVEL MODE ANALYSIS
# ================================================================

def patch_theta_grid(patches: list, d2_magnitudes: np.ndarray
                     ) -> np.ndarray:
    """Compute per-patch Θ values using local neighborhoods.

    For each patch, uses its speed variance in a 3x3 neighborhood
    relative to its D2 magnitude and coherence.

    Args:
        patches: list of FlowPatch objects
        d2_magnitudes: (rows, cols) D2 magnitude grid

    Returns:
        (rows, cols) Θ value array
    """
    if not patches:
        return np.zeros((0, 0), dtype=np.float32)

    max_r = max(p.row for p in patches)
    max_c = max(p.col for p in patches)
    rows, cols = max_r + 1, max_c + 1

    # Build speed and coherence grids
    speed_grid = np.zeros((rows, cols), dtype=np.float32)
    coh_grid = np.zeros((rows, cols), dtype=np.float32)
    for p in patches:
        speed_grid[p.row, p.col] = p.speed
        coh_grid[p.row, p.col] = p.coherence

    theta_grid = np.zeros((rows, cols), dtype=np.float32)

    for r in range(rows):
        for c in range(cols):
            # 3x3 neighborhood
            r0 = max(0, r - 1)
            r1 = min(rows, r + 2)
            c0 = max(0, c - 1)
            c1 = min(cols, c + 2)

            neighborhood = speed_grid[r0:r1, c0:c1]
            sigma2 = float(np.var(neighborhood))

            d2_val = float(d2_magnitudes[r, c]) if (
                r < d2_magnitudes.shape[0] and c < d2_magnitudes.shape[1]
            ) else 0.0
            R = float(coh_grid[r, c])

            denom = d2_val * R + THETA_EPSILON
            theta_grid[r, c] = sigma2 / denom

    return theta_grid


def mode_distribution(theta_grid: np.ndarray) -> Dict[str, float]:
    """Fraction of patches in each BTQ mode.

    Returns dict: {'B': 0.6, 'T': 0.3, 'Q': 0.1}
    """
    total = theta_grid.size
    if total == 0:
        return {MODE_BINARY: 1.0, MODE_TERNARY: 0.0, MODE_QUATERNARY: 0.0}

    b_count = int(np.sum(theta_grid < THETA_B_MAX))
    q_count = int(np.sum(theta_grid >= THETA_T_MAX))
    t_count = total - b_count - q_count

    return {
        MODE_BINARY: b_count / total,
        MODE_TERNARY: t_count / total,
        MODE_QUATERNARY: q_count / total,
    }


# ================================================================
#  BTQ MODE TRACKER (stateful, smooth transitions)
# ================================================================

class CloudBTQTracker:
    """Stateful BTQ mode tracker across frames.

    Smooths mode transitions to prevent rapid flickering.
    Tracks mode history and transition events.

    Usage:
        btq = CloudBTQTracker()
        for patches, d2_mags in frame_stream:
            result = btq.feed(patches, d2_mags)
            mode = result['mode']         # 'B', 'T', or 'Q'
            theta = result['theta']       # global Θ ratio
    """

    def __init__(self, smooth_window: int = MODE_SMOOTH_WINDOW):
        self._theta_history = deque(maxlen=smooth_window)
        self._mode_history = deque(maxlen=smooth_window)
        self._current_mode = MODE_BINARY
        self._transitions = 0
        self._frame_count = 0

    def feed(self, patches: list, d2_magnitudes: np.ndarray) -> dict:
        """Feed one frame's data. Returns BTQ analysis.

        Args:
            patches: list of FlowPatch objects
            d2_magnitudes: (rows, cols) or flat array of D2 magnitudes

        Returns:
            dict with: mode, theta, theta_smooth, distribution,
            transitions, confidence, frame
        """
        # Extract arrays from patches
        speeds = np.array([p.speed for p in patches], dtype=np.float32)
        coherences = np.array([p.coherence for p in patches], dtype=np.float32)
        d2_flat = d2_magnitudes.flatten() if isinstance(d2_magnitudes, np.ndarray) else np.array(d2_magnitudes)

        # Ensure same length
        n = min(len(speeds), len(d2_flat))
        speeds = speeds[:n]
        coherences = coherences[:n]
        d2_flat = d2_flat[:n]

        # Global Θ
        theta = compute_theta(speeds, d2_flat, coherences)
        raw_mode = classify_theta(theta)

        self._theta_history.append(theta)
        self._mode_history.append(raw_mode)
        self._frame_count += 1

        # Smoothed theta
        theta_smooth = sum(self._theta_history) / len(self._theta_history)

        # Mode voting (most common in window)
        mode_votes = {MODE_BINARY: 0, MODE_TERNARY: 0, MODE_QUATERNARY: 0}
        for m in self._mode_history:
            mode_votes[m] += 1
        total_votes = len(self._mode_history)

        # Find winner
        best_mode = max(mode_votes, key=mode_votes.get)
        confidence = mode_votes[best_mode] / total_votes

        # Only switch if confidence exceeds threshold
        if confidence >= MODE_TRANSITION_THRESHOLD and best_mode != self._current_mode:
            self._current_mode = best_mode
            self._transitions += 1

        # Patch-level distribution
        if patches:
            max_r = max(p.row for p in patches) + 1
            max_c = max(p.col for p in patches) + 1
            d2_grid = d2_magnitudes if d2_magnitudes.ndim == 2 else d2_magnitudes.reshape(max_r, max_c)
            t_grid = patch_theta_grid(patches, d2_grid)
            dist = mode_distribution(t_grid)
        else:
            dist = {MODE_BINARY: 1.0, MODE_TERNARY: 0.0, MODE_QUATERNARY: 0.0}

        return {
            'mode': self._current_mode,
            'theta': theta,
            'theta_smooth': theta_smooth,
            'raw_mode': raw_mode,
            'distribution': dist,
            'confidence': confidence,
            'transitions': self._transitions,
            'frame': self._frame_count,
        }

    @property
    def current_mode(self) -> str:
        return self._current_mode

    @property
    def transitions(self) -> int:
        return self._transitions

    def reset(self):
        """Clear state."""
        self._theta_history.clear()
        self._mode_history.clear()
        self._current_mode = MODE_BINARY
        self._transitions = 0
        self._frame_count = 0


# ================================================================
#  CLI: Demo
# ================================================================

if __name__ == '__main__':
    from ck_sim.ck_cloud_flow import (
        generate_cloud_frame_pair, horn_schunck, decompose_flow
    )
    from ck_sim.ck_cloud_curvature import (
        CloudCurvatureTracker, spatial_d2_magnitude
    )

    print("=" * 60)
    print("CK CLOUD BTQ -- Mode Inference from Cloud Dynamics")
    print("=" * 60)

    H, W = 64, 64
    curv_tracker = CloudCurvatureTracker()
    btq_tracker = CloudBTQTracker()

    for flow_type, label in [('uniform', 'Stable'), ('vortex', 'Balanced'),
                              ('turbulent', 'Chaotic')]:
        curv_tracker.reset()
        btq_tracker.reset()

        for i in range(5):
            f1, f2 = generate_cloud_frame_pair(
                H, W, flow_type, strength=0.5, seed=i
            )
            u, v = horn_schunck(f1, f2, iterations=30)
            patches = decompose_flow(u, v, patch_size=8)

            curv = curv_tracker.feed(patches)
            if curv:
                sp_mag = curv['spatial_mag']
                btq = btq_tracker.feed(patches, sp_mag)
                print(f"  {label:8s} frame {i}: mode={btq['mode']}, "
                      f"Θ={btq['theta']:.4f}, dist={btq['distribution']}")

    print(f"\n{'=' * 60}")
    print("  Cloud BTQ mode inference ready.")
    print(f"{'=' * 60}")
