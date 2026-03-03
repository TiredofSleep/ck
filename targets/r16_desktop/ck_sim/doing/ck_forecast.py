# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_forecast.py -- Forward Simulation: CK Imagines What Might Happen
====================================================================
Operator: COUNTER (2) -- counting forward into possibility.

CK's forward simulation engine. Uses the Transition Lattice (TL) as a
generative model to predict operator sequences N ticks into the future.

This is NOT planning. Planning requires goals (ck_goals.py).
This is IMAGINATION: "if I'm in state X and I choose action A,
what will my coherence trajectory look like?"

Architecture:
  TLPredictor     -- Sample operator sequences from TL probabilities
  CoherenceOracle -- Predict coherence trajectory from operator sequence
  FutureState     -- One predicted future moment
  Forecast        -- Complete N-tick prediction with confidence
  Comparator      -- Score and rank multiple forecasts (for BTQ integration)

The key insight: the TL already IS a generative model. Every row in the
10x10 matrix is a probability distribution over next operators. Sampling
from it produces plausible futures. D2 curvature on those futures
predicts coherence.

Memory: ~200 bytes per forecast (10 FutureStates × 20 bytes each).
CPU: trivial — N matrix lookups + N CL compositions per forecast.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS, BREATH,
    BALANCE, COUNTER, LATTICE, RESET, CL, compose, OP_NAMES
)


# ================================================================
#  CONSTANTS
# ================================================================

DEFAULT_HORIZON = 10        # Default prediction depth (ticks)
MAX_HORIZON = 50            # Maximum prediction depth
N_TRAJECTORIES = 8          # Number of Monte Carlo trajectories per forecast
T_STAR_F = 5.0 / 7.0       # Coherence threshold (GREEN band)
HARMONY_FRACTION = 0.73     # CL table natural HARMONY rate


# ================================================================
#  TL PREDICTOR: Sample Future Operators from Transition Lattice
# ================================================================

class TLPredictor:
    """Generates plausible operator sequences by sampling the TL.

    Each row of the 10x10 TL matrix is a probability distribution:
    P(next_op | current_op) = TL[current][next] / sum(TL[current][:])

    Sampling from this distribution produces operator sequences that
    are consistent with CK's learned experience patterns.
    """

    def __init__(self, lfsr_seed: int = 0xCAFEBEEF):
        self._lfsr = lfsr_seed

    def _lfsr_next(self) -> int:
        """LFSR pseudo-random (matches CK's LFSR everywhere)."""
        self._lfsr ^= (self._lfsr << 13) & 0xFFFFFFFF
        self._lfsr ^= (self._lfsr >> 17)
        self._lfsr ^= (self._lfsr << 5) & 0xFFFFFFFF
        self._lfsr &= 0xFFFFFFFF
        return self._lfsr

    def _build_row_distribution(self, tl_row_counts: List[int]) -> List[float]:
        """Convert raw TL counts to probability distribution."""
        total = sum(tl_row_counts)
        if total == 0:
            # Uniform if no data
            return [1.0 / NUM_OPS] * NUM_OPS
        return [c / total for c in tl_row_counts]

    def sample_next(self, current_op: int, tl_entries) -> int:
        """Sample one next operator from TL distribution.

        Args:
            current_op: Current operator (0-9)
            tl_entries: 10x10 TL matrix (list of lists of TLEntry or counts)
        """
        if current_op >= NUM_OPS:
            current_op = HARMONY

        # Extract counts for this row
        counts = []
        for j in range(NUM_OPS):
            entry = tl_entries[current_op][j]
            if hasattr(entry, 'count'):
                counts.append(entry.count)
            else:
                counts.append(int(entry))

        dist = self._build_row_distribution(counts)

        # Weighted random sample via LFSR
        r = (self._lfsr_next() % 10000) / 10000.0
        cumulative = 0.0
        for i, p in enumerate(dist):
            cumulative += p
            if r <= cumulative:
                return i
        return NUM_OPS - 1  # fallback

    def predict_sequence(self, start_op: int, tl_entries,
                         horizon: int = DEFAULT_HORIZON) -> List[int]:
        """Generate a predicted operator sequence of length `horizon`.

        Returns list of predicted operators starting from start_op.
        """
        horizon = min(horizon, MAX_HORIZON)
        sequence = [start_op]
        current = start_op

        for _ in range(horizon - 1):
            next_op = self.sample_next(current, tl_entries)
            sequence.append(next_op)
            current = next_op

        return sequence


# ================================================================
#  COHERENCE ORACLE: Predict Coherence from Operator Sequence
# ================================================================

class CoherenceOracle:
    """Predicts coherence trajectory from an operator sequence.

    Coherence = fraction of HARMONY results in a sliding window.
    Given a predicted operator sequence, we can compute what the
    coherence window would look like by running CL composition
    on consecutive pairs.

    This is exact (not approximate) because CL is deterministic.
    """

    def __init__(self, window_size: int = 32):
        self.window_size = window_size

    def predict_coherence(self, operator_sequence: List[int],
                          initial_coherence: float = 0.5,
                          initial_window: Optional[List[int]] = None) -> List[float]:
        """Predict coherence trajectory for an operator sequence.

        Args:
            operator_sequence: Predicted operators (length N)
            initial_coherence: Current coherence value
            initial_window: Recent operator history (for windowed average)

        Returns:
            List of coherence values, one per tick.
        """
        if not operator_sequence:
            return []

        # Initialize window with existing history or fill with HARMONY
        if initial_window is not None:
            window = list(initial_window[-self.window_size:])
        else:
            # Estimate window contents from initial coherence
            n_harmony = int(initial_coherence * self.window_size)
            window = [HARMONY] * n_harmony + [PROGRESS] * (self.window_size - n_harmony)

        trajectory = []
        for i in range(len(operator_sequence)):
            op = operator_sequence[i]

            # Compose with previous (simulates Being x Doing -> Becoming)
            if i > 0:
                composed = compose(operator_sequence[i-1], op)
            else:
                composed = op

            window.append(composed)
            if len(window) > self.window_size:
                window = window[-self.window_size:]

            # Coherence = HARMONY fraction in window
            harmony_count = sum(1 for x in window if x == HARMONY)
            coh = harmony_count / len(window) if window else 0.0
            trajectory.append(coh)

        return trajectory

    def predict_band(self, coherence: float) -> int:
        """Predict band from coherence value."""
        if coherence >= T_STAR_F:
            return 2  # GREEN
        elif coherence >= 0.5:
            return 1  # YELLOW
        else:
            return 0  # RED


# ================================================================
#  FUTURE STATE: One Predicted Moment
# ================================================================

@dataclass
class FutureState:
    """A single predicted future moment.

    Like EventSnapshot but for imagination, not memory.
    """
    tick_offset: int = 0        # Ticks into the future
    operator: int = HARMONY     # Predicted operator
    composed: int = HARMONY     # Predicted CL composition result
    coherence: float = 0.0      # Predicted coherence
    band: int = 0               # Predicted band (0=RED, 1=YELLOW, 2=GREEN)
    confidence: float = 0.0     # How confident is this prediction

    @property
    def is_dangerous(self) -> bool:
        """Predict if this state is dangerous (RED band, low coherence)."""
        return self.band == 0 and self.coherence < 0.3

    @property
    def is_stable(self) -> bool:
        """Predict if this state is stable (GREEN band)."""
        return self.band == 2


# ================================================================
#  FORECAST: Complete N-Tick Prediction
# ================================================================

@dataclass
class Forecast:
    """Complete prediction of N ticks into the future.

    A forecast contains multiple trajectories (Monte Carlo sampling)
    and summary statistics for decision-making.
    """
    start_operator: int = HARMONY
    horizon: int = DEFAULT_HORIZON
    states: List[FutureState] = field(default_factory=list)

    # Summary statistics (computed after generation)
    mean_coherence: float = 0.0
    min_coherence: float = 0.0
    final_coherence: float = 0.0
    final_band: int = 0
    collapse_risk: float = 0.0        # P(hitting RED band)
    harmony_fraction: float = 0.0     # Fraction of HARMONY in predicted sequence
    trajectory_variance: float = 0.0  # How uncertain is this prediction
    confidence: float = 0.0           # Overall forecast confidence

    def compute_summary(self):
        """Compute summary statistics from states."""
        if not self.states:
            return

        coherences = [s.coherence for s in self.states]
        self.mean_coherence = sum(coherences) / len(coherences)
        self.min_coherence = min(coherences)
        self.final_coherence = coherences[-1]
        self.final_band = self.states[-1].band

        # Collapse risk: fraction of states in RED band
        red_count = sum(1 for s in self.states if s.band == 0)
        self.collapse_risk = red_count / len(self.states)

        # Harmony fraction
        harmony_count = sum(1 for s in self.states if s.operator == HARMONY)
        self.harmony_fraction = harmony_count / len(self.states)

        # Variance
        mean = self.mean_coherence
        var = sum((c - mean) ** 2 for c in coherences) / len(coherences)
        self.trajectory_variance = var

        # Confidence decreases with variance and distance
        self.confidence = max(0.0, 1.0 - self.trajectory_variance * 4.0)
        # Further reduce confidence for longer horizons
        decay = 0.95 ** len(self.states)
        self.confidence *= decay

    @property
    def is_safe(self) -> bool:
        """Is this forecast safe (low collapse risk)?"""
        return self.collapse_risk < 0.2 and self.min_coherence > 0.3

    @property
    def improves_coherence(self) -> bool:
        """Does this forecast predict improving coherence?"""
        if len(self.states) < 2:
            return False
        return self.states[-1].coherence > self.states[0].coherence


# ================================================================
#  FORECAST ENGINE: Generate and Compare Predictions
# ================================================================

class ForecastEngine:
    """Generates and compares forecasts for different action choices.

    Integrates with BTQ: for each candidate action, generate a forecast,
    then score the forecast. The action with the best forecast wins.

    This is how CK "imagines" before acting:
      1. For each possible next operator (or small set of candidates):
      2. Run TL-sampled trajectory forward N ticks
      3. Predict coherence via CL composition
      4. Score the trajectory (coherence, stability, safety)
      5. Pick the action with the best predicted future
    """

    def __init__(self, horizon: int = DEFAULT_HORIZON,
                 n_trajectories: int = N_TRAJECTORIES):
        self.horizon = min(horizon, MAX_HORIZON)
        self.n_trajectories = n_trajectories
        self.predictor = TLPredictor()
        self.oracle = CoherenceOracle()

    def forecast_from(self, start_op: int, tl_entries,
                      initial_coherence: float = 0.5,
                      initial_window: Optional[List[int]] = None) -> Forecast:
        """Generate a forecast starting from a specific operator.

        Runs multiple Monte Carlo trajectories and averages them.
        """
        all_coherence_trajectories = []
        all_sequences = []

        for _ in range(self.n_trajectories):
            seq = self.predictor.predict_sequence(
                start_op, tl_entries, self.horizon)
            coh_traj = self.oracle.predict_coherence(
                seq, initial_coherence, initial_window)
            all_sequences.append(seq)
            all_coherence_trajectories.append(coh_traj)

        # Average across trajectories
        forecast = Forecast(
            start_operator=start_op,
            horizon=self.horizon,
        )

        for t in range(self.horizon):
            # Average coherence across trajectories at time t
            coh_values = []
            op_counts = [0] * NUM_OPS

            for traj_idx in range(self.n_trajectories):
                if t < len(all_coherence_trajectories[traj_idx]):
                    coh_values.append(all_coherence_trajectories[traj_idx][t])
                if t < len(all_sequences[traj_idx]):
                    op = all_sequences[traj_idx][t]
                    if op < NUM_OPS:
                        op_counts[op] += 1

            mean_coh = sum(coh_values) / len(coh_values) if coh_values else 0.5
            dominant_op = op_counts.index(max(op_counts))

            # Confidence decays with time
            confidence = 0.95 ** (t + 1)
            # Further reduce if high variance across trajectories
            if len(coh_values) > 1:
                var = sum((c - mean_coh) ** 2 for c in coh_values) / len(coh_values)
                confidence *= max(0.0, 1.0 - var * 3.0)

            state = FutureState(
                tick_offset=t,
                operator=dominant_op,
                composed=compose(start_op, dominant_op) if t == 0 else compose(
                    forecast.states[-1].operator if forecast.states else start_op,
                    dominant_op
                ),
                coherence=mean_coh,
                band=self.oracle.predict_band(mean_coh),
                confidence=confidence,
            )
            forecast.states.append(state)

        forecast.compute_summary()
        return forecast

    def compare_actions(self, candidate_ops: List[int], tl_entries,
                        initial_coherence: float = 0.5,
                        initial_window: Optional[List[int]] = None) -> List[Tuple[int, Forecast]]:
        """Generate forecasts for multiple candidate actions and rank them.

        Returns list of (operator, forecast) sorted best-first.
        Best = highest mean_coherence, lowest collapse_risk.
        """
        results = []
        for op in candidate_ops:
            forecast = self.forecast_from(
                op, tl_entries, initial_coherence, initial_window)
            results.append((op, forecast))

        # Score: coherence good, collapse bad, stability good
        def score(item):
            op, fc = item
            return (
                fc.mean_coherence * 0.4 +
                (1.0 - fc.collapse_risk) * 0.3 +
                fc.confidence * 0.2 +
                fc.harmony_fraction * 0.1
            )

        results.sort(key=score, reverse=True)
        return results

    def should_act(self, forecast: Forecast,
                   current_coherence: float) -> bool:
        """Decide whether to proceed with an action based on its forecast.

        Returns True if the forecast suggests the action is safe.
        Returns False if the forecast predicts danger.
        """
        # If already in trouble, lower the bar
        if current_coherence < 0.3:
            return forecast.final_coherence > current_coherence

        # Normal: proceed if safe and not worse than current
        return forecast.is_safe and forecast.final_coherence >= current_coherence * 0.8

    def get_avoidance_operator(self, tl_entries,
                               initial_coherence: float,
                               initial_window: Optional[List[int]] = None) -> int:
        """Find the safest operator to choose right now.

        Used when CK needs to avoid danger: "what should I do to
        maximize my coherence in the near future?"
        """
        all_ops = list(range(NUM_OPS))
        ranked = self.compare_actions(
            all_ops, tl_entries, initial_coherence, initial_window)

        if ranked:
            return ranked[0][0]
        return HARMONY  # Default safe choice


# ================================================================
#  SIMPLE TL: Utility for creating test TL matrices
# ================================================================

def make_simple_tl(dominant_transitions: Optional[Dict[Tuple[int,int], int]] = None) -> list:
    """Create a simple TL matrix for testing.

    Returns 10x10 list of lists with count values.
    Default: slight bias toward HARMONY.
    """
    tl = [[1 for _ in range(NUM_OPS)] for _ in range(NUM_OPS)]

    # Default bias: HARMONY transitions are more common
    for i in range(NUM_OPS):
        tl[i][HARMONY] = 5  # HARMONY is 5x more likely

    if dominant_transitions:
        for (from_op, to_op), count in dominant_transitions.items():
            tl[from_op][to_op] = count

    return tl
