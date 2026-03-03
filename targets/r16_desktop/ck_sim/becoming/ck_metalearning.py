# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_metalearning.py -- Meta-Learning: CK Learns How to Learn
============================================================
Operator: HARMONY (7) -- meta-learning seeks the harmony of learning itself.

CK's meta-learning system. Not gradient descent -- operator algebra.
Tracks which learning strategies produce higher coherence over time,
then adapts parameters slowly (EMA alpha=0.01) to amplify what works
and dampen what doesn't.

Four subsystems:
  LearningRateAdapter  -- Adjusts trauma/success conviction multipliers
  ThresholdTuner       -- Adjusts coherence band boundaries
  CurriculumTracker    -- Tracks complexity progression
  MetaLearner          -- Integrates all, provides adaptive parameters

Safety invariant: ALL parameters are hard-clamped to safe bounds.
No adaptation can make the system unstable.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from collections import deque
from typing import Dict, List, Optional

from ck_sim.ck_sim_heartbeat import NUM_OPS, HARMONY, OP_NAMES


# ================================================================
#  CONSTANTS
# ================================================================

# Learning rate multipliers (conviction weights for trauma vs success)
DEFAULT_TRAUMA_MULT = 3.0
DEFAULT_SUCCESS_MULT = 1.0
MIN_TRAUMA_MULT = 1.5
MAX_TRAUMA_MULT = 5.0
MIN_SUCCESS_MULT = 0.5
MAX_SUCCESS_MULT = 2.0

# Adaptation dynamics
ADAPTATION_ALPHA = 0.01       # Slow exponential moving average
EVALUATION_WINDOW = 200       # Ticks between evaluations

# Coherence band thresholds
GREEN_THRESHOLD_DEFAULT = 5.0 / 7.0   # T* = 0.714285...
YELLOW_THRESHOLD_DEFAULT = 0.5
MIN_GREEN_THRESHOLD = 0.65
MAX_GREEN_THRESHOLD = 0.80
MIN_YELLOW_THRESHOLD = 0.40
MAX_YELLOW_THRESHOLD = 0.60

# Curriculum
MAX_COMPLEXITY = 1.0

# Bands
RED = 0
YELLOW = 1
GREEN = 2

# Mode thresholds (from ck_sim_brain: OBSERVE=0, CLASSIFY=1, CRYSTALLIZE=2, SOVEREIGN=3)
MODE_CLASSIFY = 1


# ================================================================
#  LEARNING RATE ADAPTER
# ================================================================

class LearningRateAdapter:
    """Adjusts trauma and success conviction multipliers based on outcomes.

    Core question: "When trauma happens, does the current multiplier
    actually help coherence recover? If not, adjust."

    Uses operator algebra, not gradient descent. Tracks rolling windows
    of (is_trauma, delta_coherence) pairs and computes whether the
    current multipliers are correlated with coherence improvement.

    Adaptation is slow (EMA alpha=0.01) and hard-clamped to safe bounds.
    """

    def __init__(self):
        self.trauma_mult: float = DEFAULT_TRAUMA_MULT
        self.success_mult: float = DEFAULT_SUCCESS_MULT

        # Rolling windows of delta-coherence after trauma / success events
        self._trauma_deltas: deque = deque(maxlen=EVALUATION_WINDOW)
        self._success_deltas: deque = deque(maxlen=EVALUATION_WINDOW)

        # EMA of mean delta for each type
        self._trauma_ema: float = 0.0
        self._success_ema: float = 0.0

    def feed_outcome(self, is_trauma: bool, coherence_before: float,
                     coherence_after: float):
        """Record the coherence delta from a learning event.

        Args:
            is_trauma: True if this was a trauma event, False for success.
            coherence_before: Coherence immediately before the event.
            coherence_after: Coherence after the event was processed.
        """
        delta = coherence_after - coherence_before

        if is_trauma:
            self._trauma_deltas.append(delta)
        else:
            self._success_deltas.append(delta)

    def adapt(self):
        """Adjust multipliers based on outcome trends.

        If trauma events are followed by coherence IMPROVEMENT (positive delta),
        the trauma multiplier is working -- nudge it up slightly.
        If trauma events are followed by coherence DEGRADATION (negative delta),
        the multiplier may be too aggressive -- nudge it down.

        Same logic for success multiplier.
        """
        # Trauma adaptation
        if len(self._trauma_deltas) >= 10:
            mean_delta = sum(self._trauma_deltas) / len(self._trauma_deltas)
            # EMA update
            self._trauma_ema = (
                (1.0 - ADAPTATION_ALPHA) * self._trauma_ema +
                ADAPTATION_ALPHA * mean_delta
            )

            # Positive EMA = trauma learning helps -> increase multiplier
            # Negative EMA = trauma learning hurts -> decrease multiplier
            if self._trauma_ema > 0:
                adjustment = ADAPTATION_ALPHA * 0.1
            else:
                adjustment = -ADAPTATION_ALPHA * 0.1

            self.trauma_mult += adjustment
            self.trauma_mult = max(MIN_TRAUMA_MULT,
                                   min(MAX_TRAUMA_MULT, self.trauma_mult))

        # Success adaptation
        if len(self._success_deltas) >= 10:
            mean_delta = sum(self._success_deltas) / len(self._success_deltas)
            self._success_ema = (
                (1.0 - ADAPTATION_ALPHA) * self._success_ema +
                ADAPTATION_ALPHA * mean_delta
            )

            if self._success_ema > 0:
                adjustment = ADAPTATION_ALPHA * 0.1
            else:
                adjustment = -ADAPTATION_ALPHA * 0.1

            self.success_mult += adjustment
            self.success_mult = max(MIN_SUCCESS_MULT,
                                    min(MAX_SUCCESS_MULT, self.success_mult))

    @property
    def stats(self) -> Dict:
        """Current adapter state."""
        return {
            'trauma_mult': self.trauma_mult,
            'success_mult': self.success_mult,
            'trauma_ema': self._trauma_ema,
            'success_ema': self._success_ema,
            'trauma_samples': len(self._trauma_deltas),
            'success_samples': len(self._success_deltas),
        }


# ================================================================
#  THRESHOLD TUNER
# ================================================================

class ThresholdTuner:
    """Adjusts coherence band boundaries based on performance.

    If CK spends too much time in RED, the thresholds might be too
    demanding -- lower them slightly to be more forgiving.

    If CK stays in GREEN easily, raise the bar -- higher standards
    mean more growth.

    Safety: thresholds are hard-clamped and green > yellow always.
    """

    def __init__(self):
        self.green_threshold: float = GREEN_THRESHOLD_DEFAULT
        self.yellow_threshold: float = YELLOW_THRESHOLD_DEFAULT

        # Band time tracking (rolling window)
        self._band_history: deque = deque(maxlen=EVALUATION_WINDOW)

    def feed_coherence(self, coherence: float, band: int):
        """Record a coherence observation and its band."""
        self._band_history.append(band)

    def adapt(self):
        """Adjust thresholds based on band distribution.

        Too much RED (>60% of window) -> lower both thresholds (more forgiving).
        Easy GREEN (>80% of window) -> raise both thresholds (higher standards).
        """
        if len(self._band_history) < 50:
            return  # Not enough data

        n = len(self._band_history)
        red_frac = sum(1 for b in self._band_history if b == RED) / n
        green_frac = sum(1 for b in self._band_history if b == GREEN) / n

        # Too much RED -> lower thresholds (be more forgiving)
        if red_frac > 0.60:
            step = ADAPTATION_ALPHA * 0.5
            self.green_threshold -= step
            self.yellow_threshold -= step

        # Easy GREEN -> raise thresholds (demand more)
        elif green_frac > 0.80:
            step = ADAPTATION_ALPHA * 0.5
            self.green_threshold += step
            self.yellow_threshold += step

        # Clamp to safe bounds
        self.green_threshold = max(MIN_GREEN_THRESHOLD,
                                   min(MAX_GREEN_THRESHOLD,
                                       self.green_threshold))
        self.yellow_threshold = max(MIN_YELLOW_THRESHOLD,
                                    min(MAX_YELLOW_THRESHOLD,
                                        self.yellow_threshold))

        # Invariant: green > yellow (at least 0.05 gap)
        if self.green_threshold <= self.yellow_threshold + 0.05:
            self.green_threshold = self.yellow_threshold + 0.05
            # Re-clamp green after fixing invariant
            self.green_threshold = max(MIN_GREEN_THRESHOLD,
                                       min(MAX_GREEN_THRESHOLD,
                                           self.green_threshold))

    def get_band(self, coherence: float) -> int:
        """Classify coherence into a band using adapted thresholds.

        Returns:
            0 = RED, 1 = YELLOW, 2 = GREEN
        """
        if coherence >= self.green_threshold:
            return GREEN
        elif coherence >= self.yellow_threshold:
            return YELLOW
        else:
            return RED

    @property
    def stats(self) -> Dict:
        """Current tuner state."""
        n = len(self._band_history)
        red_frac = sum(1 for b in self._band_history if b == RED) / n if n > 0 else 0.0
        yellow_frac = sum(1 for b in self._band_history if b == YELLOW) / n if n > 0 else 0.0
        green_frac = sum(1 for b in self._band_history if b == GREEN) / n if n > 0 else 0.0

        return {
            'green_threshold': self.green_threshold,
            'yellow_threshold': self.yellow_threshold,
            'red_fraction': red_frac,
            'yellow_fraction': yellow_frac,
            'green_fraction': green_frac,
            'samples': n,
        }


# ================================================================
#  CURRICULUM TRACKER
# ================================================================

class CurriculumTracker:
    """Tracks complexity progression: simple -> complex.

    CK starts with simple patterns (complexity=0.0) and graduates to
    harder material (complexity=1.0) as it demonstrates competence:
      - Sustained coherence > 0.7
      - Crystals forming
      - Mode >= CLASSIFY

    If CK is struggling (sustained coherence < 0.4), complexity backs off.

    The complexity value can be used by the engine to control:
      - Input noise level
      - Pattern complexity
      - Environmental challenge
    """

    def __init__(self):
        self.complexity_level: float = 0.0

        # Performance tracking (rolling window)
        self._coherence_window: deque = deque(maxlen=EVALUATION_WINDOW)
        self._crystal_window: deque = deque(maxlen=EVALUATION_WINDOW)
        self._mode_window: deque = deque(maxlen=EVALUATION_WINDOW)

    def feed_performance(self, coherence: float, crystals_formed: int,
                         mode: int):
        """Record one tick of performance data.

        Args:
            coherence: Current coherence value [0, 1].
            crystals_formed: Number of crystals formed this tick (cumulative ok).
            mode: Current mode (0=OBSERVE, 1=CLASSIFY, 2=CRYSTALLIZE, 3=SOVEREIGN).
        """
        self._coherence_window.append(coherence)
        self._crystal_window.append(crystals_formed)
        self._mode_window.append(mode)

    def _mean_coherence(self) -> float:
        """Mean coherence over the evaluation window."""
        if not self._coherence_window:
            return 0.0
        return sum(self._coherence_window) / len(self._coherence_window)

    def _any_crystals(self) -> bool:
        """Whether any crystals formed in the window."""
        return any(c > 0 for c in self._crystal_window)

    def _mean_mode(self) -> float:
        """Mean mode over the window."""
        if not self._mode_window:
            return 0.0
        return sum(self._mode_window) / len(self._mode_window)

    def adapt(self):
        """Adjust complexity based on sustained performance.

        Increase when: coherence > 0.7 AND crystals forming AND mode >= CLASSIFY
        Decrease when: coherence < 0.4
        """
        if len(self._coherence_window) < 50:
            return  # Not enough data

        mean_coh = self._mean_coherence()
        has_crystals = self._any_crystals()
        mean_mode = self._mean_mode()

        # Increase complexity: doing well
        if mean_coh > 0.7 and has_crystals and mean_mode >= MODE_CLASSIFY:
            step = ADAPTATION_ALPHA * 0.5
            self.complexity_level += step

        # Decrease complexity: struggling
        elif mean_coh < 0.4:
            step = ADAPTATION_ALPHA * 0.5
            self.complexity_level -= step

        # Clamp to [0, MAX_COMPLEXITY]
        self.complexity_level = max(0.0, min(MAX_COMPLEXITY,
                                             self.complexity_level))

    def get_complexity(self) -> float:
        """Current complexity level [0.0, 1.0]."""
        return self.complexity_level

    @property
    def stats(self) -> Dict:
        """Current tracker state."""
        return {
            'complexity': self.complexity_level,
            'mean_coherence': self._mean_coherence(),
            'has_crystals': self._any_crystals(),
            'mean_mode': self._mean_mode(),
            'samples': len(self._coherence_window),
        }


# ================================================================
#  META-LEARNER: Integration Layer
# ================================================================

class MetaLearner:
    """Integrates all meta-learning subsystems.

    Called once per tick by the engine. Returns a dict of adaptive
    parameters that the engine uses to modulate its behavior.

    Adaptation runs every EVALUATION_WINDOW ticks. Between evaluations,
    the MetaLearner just feeds data to the subsystems and returns
    the current (stable) parameters.
    """

    def __init__(self):
        self.learning_rate = LearningRateAdapter()
        self.thresholds = ThresholdTuner()
        self.curriculum = CurriculumTracker()

        self._last_evaluation_tick: int = 0

    def tick(self, tick: int, coherence: float, band: int,
             is_trauma: bool, crystals: int, mode: int) -> Dict:
        """Process one tick and return adaptive parameters.

        Args:
            tick: Current tick number.
            coherence: Current coherence value [0, 1].
            band: Current coherence band (0=RED, 1=YELLOW, 2=GREEN).
            is_trauma: Whether this tick involved a trauma event.
            crystals: Number of crystals formed (cumulative).
            mode: Current mode (0-3).

        Returns:
            Dict with keys:
                trauma_mult, success_mult,
                green_threshold, yellow_threshold,
                complexity, band
        """
        # Feed data to subsystems
        self.thresholds.feed_coherence(coherence, band)
        self.curriculum.feed_performance(coherence, crystals, mode)

        # Feed learning rate adapter (only on actual events)
        # Use the band transition as a proxy for coherence change
        # The engine calls feed_outcome directly for real events

        # Periodic adaptation
        if tick - self._last_evaluation_tick >= EVALUATION_WINDOW:
            self.learning_rate.adapt()
            self.thresholds.adapt()
            self.curriculum.adapt()
            self._last_evaluation_tick = tick

        # Compute adapted band using tuned thresholds
        adapted_band = self.thresholds.get_band(coherence)

        return {
            'trauma_mult': self.learning_rate.trauma_mult,
            'success_mult': self.learning_rate.success_mult,
            'green_threshold': self.thresholds.green_threshold,
            'yellow_threshold': self.thresholds.yellow_threshold,
            'complexity': self.curriculum.get_complexity(),
            'band': adapted_band,
        }

    def feed_learning_outcome(self, is_trauma: bool,
                              coherence_before: float,
                              coherence_after: float):
        """Feed a learning outcome to the rate adapter.

        Called by the engine when an actual trauma/success event occurs,
        with the coherence before and after.
        """
        self.learning_rate.feed_outcome(
            is_trauma, coherence_before, coherence_after)

    def stats(self) -> Dict:
        """Full meta-learning state for diagnostics."""
        return {
            'learning_rate': self.learning_rate.stats,
            'thresholds': self.thresholds.stats,
            'curriculum': self.curriculum.stats,
            'last_evaluation_tick': self._last_evaluation_tick,
        }
