"""
ck_cloud_pfe.py -- Cloud PFE Least-Action Scoring
===================================================
Operator: BALANCE (5) -- equilibrium is least energy.

Phase Field Engine adapted for cloud dynamics.
Scores cloud operator sequences using the same E_out + E_in
energy framework as CK's emotional physiology.

Two energy surfaces:

  E_out (Einstein / External Physics):
    - velocity_energy:    mean speed across patches
    - jerk_energy:        temporal D2 magnitude (acceleration change)
    - smoothness_energy:  spatial D2 variance (how ragged the flow is)
    - mode_jump_energy:   BTQ mode transitions (instability penalty)

  E_in (Tesla / Internal Curvature):
    - d2_energy:          mean D2 magnitude (raw curvature)
    - phase_incoherence:  1 - grid_coherence (how far from HARMONY)
    - helical_coherence:  how well operator sequence wraps cyclically

  E_total = E_out + E_in   (lower = more coherent = better)

Least-action principle: CK prefers cloud patterns where E_total
is minimized. These patterns produce the cleanest operator chains.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from collections import deque
from typing import Dict, List, Optional, Tuple

import numpy as np

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, OP_NAMES, CL, compose,
)


# ================================================================
#  CONSTANTS
# ================================================================

# Energy scaling factors
VELOCITY_WEIGHT = 0.15
JERK_WEIGHT = 0.20
SMOOTHNESS_WEIGHT = 0.15
MODE_JUMP_WEIGHT = 0.10
D2_WEIGHT = 0.15
PHASE_INCOH_WEIGHT = 0.15
HELICAL_WEIGHT = 0.10

# T* threshold (universal)
T_STAR = 5.0 / 7.0

# Helical period (operators per expected cycle)
HELICAL_PERIOD = 8

# Energy normalization cap
MAX_ENERGY = 10.0


# ================================================================
#  E_OUT: EINSTEIN / EXTERNAL PHYSICS
# ================================================================

def velocity_energy(speeds: np.ndarray) -> float:
    """Mean speed across patches. Higher speed = higher energy.

    Normalized: speed / 2.0 (typical max speed ~2.0 for cloud flow).
    """
    if len(speeds) == 0:
        return 0.0
    return min(float(np.mean(speeds)) / 2.0, MAX_ENERGY)


def jerk_energy(temporal_d2_magnitudes: np.ndarray) -> float:
    """Jerk = temporal D2 (acceleration of acceleration).

    High jerk = jerky, unpredictable flow transitions.
    """
    if temporal_d2_magnitudes is None or temporal_d2_magnitudes.size == 0:
        return 0.0
    return min(float(np.mean(temporal_d2_magnitudes)), MAX_ENERGY)


def smoothness_energy(spatial_d2: np.ndarray) -> float:
    """Spatial D2 variance across the grid.

    High variance = ragged, inconsistent spatial curvature.
    Low variance = smooth, uniform curvature field.
    """
    if spatial_d2 is None or spatial_d2.size == 0:
        return 0.0
    # Variance of the magnitudes across patches
    mags = np.sum(np.abs(spatial_d2), axis=-1) if spatial_d2.ndim == 3 else spatial_d2
    return min(float(np.var(mags)), MAX_ENERGY)


def mode_jump_energy(mode_history: list) -> float:
    """Count BTQ mode transitions in recent history.

    Normalized by window size. Frequent jumps = instability.
    """
    if len(mode_history) < 2:
        return 0.0
    jumps = sum(1 for i in range(1, len(mode_history))
                if mode_history[i] != mode_history[i - 1])
    return jumps / (len(mode_history) - 1)


def compute_e_out(speeds: np.ndarray,
                  temporal_d2_mag: Optional[np.ndarray],
                  spatial_d2_grid: Optional[np.ndarray],
                  mode_history: list) -> Tuple[float, dict]:
    """Full E_out computation.

    Returns:
        (e_out_total, details_dict)
    """
    v_e = velocity_energy(speeds)
    j_e = jerk_energy(temporal_d2_mag)
    s_e = smoothness_energy(spatial_d2_grid)
    m_e = mode_jump_energy(mode_history)

    total = (VELOCITY_WEIGHT * v_e +
             JERK_WEIGHT * j_e +
             SMOOTHNESS_WEIGHT * s_e +
             MODE_JUMP_WEIGHT * m_e)

    details = {
        'velocity': round(v_e, 4),
        'jerk': round(j_e, 4),
        'smoothness': round(s_e, 4),
        'mode_jump': round(m_e, 4),
        'e_out': round(total, 4),
    }
    return total, details


# ================================================================
#  E_IN: TESLA / INTERNAL CURVATURE
# ================================================================

def d2_energy(d2_magnitudes: np.ndarray) -> float:
    """Mean D2 magnitude (raw curvature). Higher = more curved."""
    if d2_magnitudes is None or d2_magnitudes.size == 0:
        return 0.0
    return min(float(np.mean(d2_magnitudes)), MAX_ENERGY)


def phase_incoherence(op_sequence: List[int]) -> float:
    """1 - coherence. Measures how far from HARMONY.

    Coherence = fraction of HARMONY operators in the sequence.
    """
    if not op_sequence:
        return 1.0
    harmony_count = sum(1 for op in op_sequence if op == HARMONY)
    coherence = harmony_count / len(op_sequence)
    return 1.0 - coherence


def helical_coherence(op_sequence: List[int],
                      period: int = HELICAL_PERIOD) -> float:
    """How cyclically periodic is the operator sequence?

    Measures similarity between blocks of length `period`.
    High similarity = helical (like a standing wave or spring).
    Returns energy (lower = more helical = better).

    Method: compute autocorrelation at the period lag.
    """
    n = len(op_sequence)
    if n < period * 2:
        return 0.5  # Not enough data, neutral energy

    # Convert to float array of operator indices
    ops = np.array(op_sequence, dtype=np.float32)

    # Autocorrelation at period lag
    # Pearson correlation between seq[:-period] and seq[period:]
    x = ops[:-period]
    y = ops[period:]

    mx = np.mean(x)
    my = np.mean(y)
    dx = x - mx
    dy = y - my

    denom = np.sqrt(np.sum(dx ** 2) * np.sum(dy ** 2))
    if denom < 1e-8:
        return 0.5  # Constant sequence

    corr = float(np.sum(dx * dy) / denom)

    # Transform: high correlation → low energy
    # corr in [-1, 1], map to energy in [0, 1]
    return (1.0 - corr) / 2.0


def compute_e_in(d2_magnitudes: np.ndarray,
                 op_sequence: List[int]) -> Tuple[float, dict]:
    """Full E_in computation.

    Returns:
        (e_in_total, details_dict)
    """
    d_e = d2_energy(d2_magnitudes)
    p_e = phase_incoherence(op_sequence)
    h_e = helical_coherence(op_sequence)

    total = (D2_WEIGHT * d_e +
             PHASE_INCOH_WEIGHT * p_e +
             HELICAL_WEIGHT * h_e)

    details = {
        'd2': round(d_e, 4),
        'phase_incoherence': round(p_e, 4),
        'helical': round(h_e, 4),
        'e_in': round(total, 4),
    }
    return total, details


# ================================================================
#  E_TOTAL: Combined Least-Action Score
# ================================================================

def compute_e_total(speeds: np.ndarray,
                    temporal_d2_mag: Optional[np.ndarray],
                    spatial_d2_grid: Optional[np.ndarray],
                    d2_magnitudes: np.ndarray,
                    op_sequence: List[int],
                    mode_history: list) -> Tuple[float, dict]:
    """Full least-action energy computation.

    E_total = E_out + E_in

    Lower E_total = more coherent cloud pattern.

    Returns:
        (e_total, full_details_dict)
    """
    e_out, out_details = compute_e_out(
        speeds, temporal_d2_mag, spatial_d2_grid, mode_history
    )
    e_in, in_details = compute_e_in(d2_magnitudes, op_sequence)

    e_total = e_out + e_in

    # Quality classification (mirrors CK band system)
    if e_total < (1.0 - T_STAR):
        quality = 'GREEN'      # Low energy = high coherence
    elif e_total < 0.6:
        quality = 'YELLOW'     # Moderate energy
    else:
        quality = 'RED'        # High energy = chaotic

    details = {
        **out_details,
        **in_details,
        'e_total': round(e_total, 4),
        'quality': quality,
    }
    return e_total, details


# ================================================================
#  PFE CLOUD TRACKER (stateful)
# ================================================================

class CloudPFETracker:
    """Stateful least-action energy tracker for cloud sequences.

    Maintains running energy history and quality trend.

    Usage:
        pfe = CloudPFETracker()
        for frame_data in stream:
            result = pfe.feed(
                speeds, temporal_d2, spatial_d2, d2_mags,
                op_sequence, btq_mode
            )
            quality = result['quality']
            e_total = result['e_total']
    """

    def __init__(self, history_window: int = 32):
        self._energy_history = deque(maxlen=history_window)
        self._mode_history = deque(maxlen=history_window)
        self._quality_history = deque(maxlen=history_window)
        self._cumulative_sequence = []
        self._max_sequence = 1024  # Keep last 1024 operators
        self._frame_count = 0

    def feed(self, speeds: np.ndarray,
             temporal_d2_mag: Optional[np.ndarray],
             spatial_d2_grid: Optional[np.ndarray],
             d2_magnitudes: np.ndarray,
             op_sequence: List[int],
             btq_mode: str) -> dict:
        """Feed one frame's data. Returns energy analysis.

        Args:
            speeds: patch speed array
            temporal_d2_mag: temporal D2 magnitude grid (or None)
            spatial_d2_grid: spatial D2 vector grid (or None)
            d2_magnitudes: D2 magnitude array
            op_sequence: operator sequence for this frame
            btq_mode: 'B', 'T', or 'Q' from BTQ tracker

        Returns:
            dict with full energy breakdown + quality + trend.
        """
        self._mode_history.append(btq_mode)
        self._cumulative_sequence.extend(op_sequence)
        if len(self._cumulative_sequence) > self._max_sequence:
            self._cumulative_sequence = self._cumulative_sequence[-self._max_sequence:]

        self._frame_count += 1

        e_total, details = compute_e_total(
            speeds, temporal_d2_mag, spatial_d2_grid,
            d2_magnitudes, self._cumulative_sequence,
            list(self._mode_history),
        )

        self._energy_history.append(e_total)
        self._quality_history.append(details['quality'])

        # Energy trend (slope of recent energy)
        trend = 0.0
        if len(self._energy_history) >= 4:
            recent = list(self._energy_history)
            half = len(recent) // 2
            first_half = sum(recent[:half]) / half
            second_half = sum(recent[half:]) / (len(recent) - half)
            trend = second_half - first_half

        # Mean energy
        mean_energy = sum(self._energy_history) / len(self._energy_history)

        # Quality stability
        if self._quality_history:
            green_frac = sum(1 for q in self._quality_history if q == 'GREEN') / len(self._quality_history)
        else:
            green_frac = 0.0

        details['trend'] = round(trend, 4)
        details['mean_energy'] = round(mean_energy, 4)
        details['green_fraction'] = round(green_frac, 4)
        details['cumulative_ops'] = len(self._cumulative_sequence)
        details['frame'] = self._frame_count

        return details

    @property
    def mean_energy(self) -> float:
        if not self._energy_history:
            return 0.0
        return sum(self._energy_history) / len(self._energy_history)

    @property
    def frame_count(self) -> int:
        return self._frame_count

    def reset(self):
        """Clear state."""
        self._energy_history.clear()
        self._mode_history.clear()
        self._quality_history.clear()
        self._cumulative_sequence.clear()
        self._frame_count = 0


# ================================================================
#  CLI: Demo
# ================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("CK CLOUD PFE -- Least-Action Energy Scoring")
    print("=" * 60)

    # Quick test with synthetic data
    rng = np.random.RandomState(42)

    pfe = CloudPFETracker()

    for i in range(10):
        speeds = rng.rand(64).astype(np.float32) * 0.5
        d2_mags = rng.rand(64).astype(np.float32) * 0.3
        sp_d2 = rng.randn(8, 8, 5).astype(np.float32) * 0.1
        tm_d2 = rng.rand(64).astype(np.float32) * 0.2
        ops = [int(rng.randint(0, NUM_OPS)) for _ in range(64)]
        mode = ['B', 'T', 'Q'][i % 3]

        result = pfe.feed(speeds, tm_d2, sp_d2, d2_mags, ops, mode)

        print(f"  Frame {i}: E={result['e_total']:.4f} "
              f"quality={result['quality']:6s} "
              f"E_out={result['e_out']:.4f} E_in={result['e_in']:.4f}")

    print(f"\n  Mean energy: {pfe.mean_energy:.4f}")
    print(f"\n{'=' * 60}")
    print("  Cloud PFE scoring ready.")
    print(f"{'=' * 60}")
