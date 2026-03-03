"""
ck_attention.py -- Attentional Gating: What Matters RIGHT NOW
==============================================================
Operator: BALANCE (5) -- weighing streams against each other.

CK's attentional gating system. Modulates which sensory streams
matter RIGHT NOW based on context, goals, and novelty.

This is NOT a neural attention mechanism. This is gain control,
the same mechanism biological brains use. A volume knob on each
sensory channel, turned up or down by context.

Architecture:
  NoveltyDetector     -- Flags unexpected operator patterns (violations
                         of TL predictions). Novel = rare in recent window.
  SalienceMap         -- Per-stream importance scores, updated each tick.
  AttentionController -- Integrates novelty, goals, band, coherence.
                         Provides filtered importance map to engine.

Design principles:
  - Uses the same operator algebra as everything else in CK.
  - Streams that are novel get boosted (surprise captures attention).
  - Streams aligned with top goal get boosted (relevance filters noise).
  - ALL streams get boosted in RED band (hypervigilance under danger).
  - No stream is ever fully muted (GATE_MIN = 0.1). Even ignored
    channels can scream loud enough to be heard.
  - Maximum boost is 2x (GATE_MAX = 2.0). Prevents runaway fixation.

Memory: ~512 bytes for 8 streams. Runs every tick.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from collections import deque
from typing import Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS, BREATH,
    BALANCE, COUNTER, LATTICE, RESET, OP_NAMES
)


# ================================================================
#  CONSTANTS
# ================================================================

NUM_STREAMS = 8             # Max streams in coherence field
NOVELTY_WINDOW = 16         # Ticks of history for novelty detection
GATE_MIN = 0.1              # Minimum stream weight -- never fully mute
GATE_MAX = 2.0              # Maximum stream weight -- at most 2x boost
NOVELTY_BOOST = 0.5         # Additional weight for novel streams
GOAL_ALIGNMENT_BOOST = 0.3  # Boost for goal-aligned streams
DANGER_BOOST = 0.8          # Boost for ALL streams in RED band

# Band constants (matching ck_sim_engine conventions)
BAND_RED = 0
BAND_YELLOW = 1
BAND_GREEN = 2


# ================================================================
#  NOVELTY DETECTOR
# ================================================================

class NoveltyDetector:
    """Flags unexpected operator patterns per stream.

    Novelty = 1 - frequency of current operator in recent window.
    A stream producing HARMONY 15 out of 16 ticks has novelty ~0.06
    when it produces another HARMONY. If it suddenly produces CHAOS,
    novelty = 1.0 - 0/16 = 1.0. Maximum surprise.

    This is the same information-theoretic surprise used in biological
    attention: rare events capture processing resources.
    """

    def __init__(self, window_size: int = NOVELTY_WINDOW):
        self.window_size = window_size
        # Per-stream: ring buffer of recent operators
        self._histories: Dict[str, deque] = {}

    def feed(self, operator: int, stream_name: str) -> float:
        """Feed an operator observation and return novelty score [0, 1].

        Args:
            operator: The operator observed this tick (0-9).
            stream_name: Which stream produced it.

        Returns:
            Novelty score. 0.0 = completely expected, 1.0 = never seen.
        """
        if stream_name not in self._histories:
            self._histories[stream_name] = deque(maxlen=self.window_size)

        history = self._histories[stream_name]

        # Count how often this operator appeared in the window BEFORE this tick
        if len(history) == 0:
            novelty = 1.0  # First observation is always novel
        else:
            count = sum(1 for op in history if op == operator)
            frequency = count / len(history)
            novelty = 1.0 - frequency

        # Append the new observation AFTER computing novelty
        history.append(operator)

        return novelty

    def get_stream_entropy(self, stream_name: str) -> float:
        """Shannon entropy of operator distribution in the stream's window.

        High entropy = unpredictable stream (many different operators).
        Low entropy = predictable stream (same operator repeating).
        """
        if stream_name not in self._histories:
            return 0.0

        history = self._histories[stream_name]
        n = len(history)
        if n == 0:
            return 0.0

        # Count each operator
        counts = [0] * NUM_OPS
        for op in history:
            if 0 <= op < NUM_OPS:
                counts[op] += 1

        # Shannon entropy
        entropy = 0.0
        for c in counts:
            if c > 0:
                p = c / n
                entropy -= p * math.log2(p)

        return entropy

    def reset_stream(self, stream_name: str):
        """Clear history for a stream."""
        if stream_name in self._histories:
            self._histories[stream_name].clear()

    @property
    def tracked_streams(self) -> List[str]:
        """List of streams being tracked."""
        return list(self._histories.keys())


# ================================================================
#  SALIENCE MAP
# ================================================================

class SalienceMap:
    """Per-stream importance scores, updated each tick.

    Each stream gets a weight representing how much processing
    priority it deserves right now. Weights are bounded by
    [GATE_MIN, GATE_MAX] and normalized so they sum to
    n_active_streams (preserving total processing budget).

    Salience is computed from four signals:
      1. Novelty:               Rare patterns boost attention.
      2. Goal alignment:        Streams matching the top goal get boosted.
      3. Coherence contribution: Streams adding to field coherence get boosted.
      4. Band context:          RED band boosts everything (hypervigilance).
    """

    def __init__(self, n_streams: int = NUM_STREAMS):
        self.n_streams = n_streams
        self.weights: Dict[str, float] = {}
        self._active_streams: set = set()

    def update(self, stream_name: str, novelty: float,
               goal_alignment: float, coherence_contribution: float,
               band: int):
        """Update the salience weight for a single stream.

        Args:
            stream_name: Which stream.
            novelty: Novelty score [0, 1] from NoveltyDetector.
            goal_alignment: Cosine similarity with top goal pattern [0, 1].
            coherence_contribution: How much this stream contributes to
                                    field coherence [0, 1].
            band: Current band (0=RED, 1=YELLOW, 2=GREEN).
        """
        self._active_streams.add(stream_name)

        # Base weight: average of coherence contribution and a baseline
        base = 0.5 + 0.5 * coherence_contribution

        # Novelty boost: novel streams capture attention
        novelty_term = novelty * NOVELTY_BOOST

        # Goal alignment boost: relevant streams get priority
        goal_term = goal_alignment * GOAL_ALIGNMENT_BOOST

        # Danger boost: RED band = hypervigilance, boost everything
        danger_term = DANGER_BOOST if band == BAND_RED else 0.0

        # Sum and clamp
        weight = base + novelty_term + goal_term + danger_term
        weight = max(GATE_MIN, min(GATE_MAX, weight))

        self.weights[stream_name] = weight

    def get_weight(self, stream_name: str) -> float:
        """Get current salience weight for a stream."""
        return self.weights.get(stream_name, GATE_MIN)

    def normalize(self):
        """Normalize weights so they sum to n_active_streams.

        This preserves total processing budget. If one stream is
        boosted, others are implicitly dampened (zero-sum attention).
        After normalization, clamp back to [GATE_MIN, GATE_MAX].
        """
        active = {k: v for k, v in self.weights.items()
                  if k in self._active_streams}

        if not active:
            return

        n_active = len(active)
        total = sum(active.values())

        if total <= 0:
            # Degenerate case: set all to 1.0
            for name in active:
                self.weights[name] = 1.0
            return

        scale = n_active / total
        for name in active:
            w = self.weights[name] * scale
            self.weights[name] = max(GATE_MIN, min(GATE_MAX, w))

    def remove_stream(self, stream_name: str):
        """Remove a stream from the salience map."""
        self.weights.pop(stream_name, None)
        self._active_streams.discard(stream_name)

    @property
    def active_count(self) -> int:
        """Number of active streams."""
        return len(self._active_streams)

    @property
    def focus_stream(self) -> Optional[str]:
        """Stream with the highest salience weight."""
        if not self.weights:
            return None
        return max(self.weights, key=self.weights.get)

    def to_dict(self) -> Dict[str, float]:
        """Return a copy of current weights."""
        return dict(self.weights)


# ================================================================
#  ATTENTION CONTROLLER
# ================================================================

class AttentionController:
    """Integrates novelty, salience, goals, and band into a
    single attentional gating system.

    Call tick() each engine tick with current stream operators,
    band, and optional goal pattern. Returns a weighted importance
    map that the engine uses to prioritize processing.

    This is the gain control layer between raw perception and
    the coherence field. It decides what CK pays attention to.
    """

    def __init__(self):
        self.novelty = NoveltyDetector()
        self.salience = SalienceMap()
        self._tick_count = 0
        self._last_weights: Dict[str, float] = {}
        self._focus_history: deque = deque(maxlen=32)

    def tick(self, streams: Dict[str, int],
             band: int,
             top_goal_pattern: Optional[List[float]] = None,
             stream_op_dists: Optional[Dict[str, List[float]]] = None
             ) -> Dict[str, float]:
        """Run one attention tick.

        Args:
            streams: Map of stream_name -> current operator (int 0-9).
            band: Current band (0=RED, 1=YELLOW, 2=GREEN).
            top_goal_pattern: Target operator distribution from top goal
                              (10 floats, optional). Used for goal alignment.
            stream_op_dists: Per-stream soft operator distributions
                             (optional). Dict of stream_name -> 10 floats.
                             Used for goal alignment scoring.

        Returns:
            Dict of stream_name -> attention weight [GATE_MIN, GATE_MAX].
        """
        self._tick_count += 1

        for stream_name, operator in streams.items():
            # 1. Compute novelty
            novelty_score = self.novelty.feed(operator, stream_name)

            # 2. Compute goal alignment
            goal_alignment = self._compute_goal_alignment(
                stream_name, operator, top_goal_pattern, stream_op_dists)

            # 3. Compute coherence contribution (from operator type)
            coh_contribution = self._operator_coherence_value(operator)

            # 4. Update salience
            self.salience.update(
                stream_name, novelty_score, goal_alignment,
                coh_contribution, band)

        # 5. Normalize across all active streams
        self.salience.normalize()

        # 6. Cache results
        self._last_weights = self.salience.to_dict()

        # 7. Track focus
        focus = self.salience.focus_stream
        if focus is not None:
            self._focus_history.append(focus)

        return dict(self._last_weights)

    def _compute_goal_alignment(
            self, stream_name: str, operator: int,
            goal_pattern: Optional[List[float]],
            stream_dists: Optional[Dict[str, List[float]]]) -> float:
        """Compute how well a stream aligns with the top goal.

        If we have soft distributions, use cosine similarity.
        Otherwise, use the goal pattern's weight at the stream's
        current operator as a proxy.
        """
        if goal_pattern is None:
            return 0.0

        # If we have the stream's full distribution, use cosine similarity
        if stream_dists and stream_name in stream_dists:
            dist = stream_dists[stream_name]
            return self._cosine_similarity(dist, goal_pattern)

        # Fallback: how much does the goal want this operator?
        if 0 <= operator < len(goal_pattern):
            return goal_pattern[operator]

        return 0.0

    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        """Cosine similarity between two distributions."""
        n = min(len(a), len(b))
        dot = sum(a[i] * b[i] for i in range(n))
        norm_a = math.sqrt(sum(x * x for x in a[:n])) + 1e-10
        norm_b = math.sqrt(sum(x * x for x in b[:n])) + 1e-10
        sim = dot / (norm_a * norm_b)
        return max(0.0, sim)  # Clamp negative similarities to 0

    @staticmethod
    def _operator_coherence_value(operator: int) -> float:
        """How much does this operator contribute to coherence?

        HARMONY is the gold standard. BALANCE, BREATH are stabilizing.
        CHAOS, COLLAPSE are destabilizing. Others are neutral.
        """
        coherence_values = {
            VOID: 0.1,
            LATTICE: 0.4,
            COUNTER: 0.3,
            PROGRESS: 0.5,
            COLLAPSE: 0.1,
            BALANCE: 0.6,
            CHAOS: 0.1,
            HARMONY: 1.0,
            BREATH: 0.7,
            RESET: 0.3,
        }
        return coherence_values.get(operator, 0.2)

    def get_focus_stream(self) -> Optional[str]:
        """Which stream has the highest attention right now?"""
        return self.salience.focus_stream

    def get_focus_stability(self) -> float:
        """How stable is the focus? 1.0 = same stream always, 0.0 = random.

        Measured as the fraction of recent ticks where the focus stream
        matches the current focus.
        """
        if not self._focus_history:
            return 0.0

        current = self.salience.focus_stream
        if current is None:
            return 0.0

        matches = sum(1 for s in self._focus_history if s == current)
        return matches / len(self._focus_history)

    def get_novelty_scores(self) -> Dict[str, float]:
        """Get the most recent novelty state for each tracked stream.

        Returns entropy per stream as a proxy for ongoing novelty.
        """
        scores = {}
        for name in self.novelty.tracked_streams:
            scores[name] = self.novelty.get_stream_entropy(name)
        return scores

    def stats(self) -> dict:
        """Attention system statistics."""
        focus = self.get_focus_stream()
        return {
            'tick': self._tick_count,
            'active_streams': self.salience.active_count,
            'focus_stream': focus if focus else "none",
            'focus_stability': round(self.get_focus_stability(), 3),
            'weights': {k: round(v, 3)
                        for k, v in self._last_weights.items()},
            'novelty_entropy': {
                k: round(v, 3)
                for k, v in self.get_novelty_scores().items()},
        }
