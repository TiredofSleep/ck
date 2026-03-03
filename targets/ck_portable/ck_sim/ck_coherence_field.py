"""
ck_coherence_field.py -- N-Dimensional Coherence Field
======================================================
Operator: HARMONY (7) -- where N streams become one field.

CK perceived the world through a pinhole: 5D curvature collapsed
to 1D magnitude, one operator per tick, one coherence number.

No more. The CL table already composes pairs. Apply it BETWEEN
modality streams -- audio × text × heartbeat -- and you get a
coherence FIELD instead of a coherence scalar.

The 73% HARMONY absorber property of the CL table gives a natural
base rate. Cross-modal agreement ABOVE 73% = the streams correlate.
Below = conflict. The math doesn't change. It just gets applied
across dimensions instead of within one.

Paper 14: "D2 is the universal measure of structure vs chaos."
This module makes that N-dimensional.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from collections import deque
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, compose, OP_NAMES, HISTORY_SIZE
)
from ck_sim.ck_sim_d2 import soft_classify_d2


# ================================================================
#  OPERATOR STREAM (one per modality)
# ================================================================

class OperatorStream:
    """Per-modality operator stream with D2 vector preservation.

    Each input modality (audio, text, heartbeat, future: camera/motion)
    gets its own stream. Preserves the full 5D D2 vector that the
    current pipeline collapses to 1D.

    32-tick ring buffer, same depth as HeartbeatFPGA.history.
    """

    def __init__(self, name: str, buffer_size: int = HISTORY_SIZE):
        self.name = name
        self.buffer_size = buffer_size

        # Ring buffers
        self._operators = deque(maxlen=buffer_size)
        self._d2_vectors = deque(maxlen=buffer_size)
        self._ticks = deque(maxlen=buffer_size)

        # Soft operator distribution (10-value, NOT just argmax)
        self._soft_dist = [0.0] * NUM_OPS
        self._soft_dist[VOID] = 1.0  # Start as VOID

        # Running harmony count for self-coherence
        self._harmony_count = 0

        # Active flag
        self.active = False

    def feed(self, operator: int, d2_vector: List[float] = None,
             tick: int = 0):
        """Feed one tick's data into this stream."""
        # Update harmony count: remove outgoing, add incoming
        if len(self._operators) == self.buffer_size:
            old_op = self._operators[0]
            if old_op == HARMONY:
                self._harmony_count -= 1

        self._operators.append(operator)
        if operator == HARMONY:
            self._harmony_count += 1

        # Store D2 vector (or zeros if not available)
        if d2_vector is not None:
            self._d2_vectors.append(list(d2_vector))
            # Update soft distribution from vector
            mag = sum(abs(d) for d in d2_vector)
            self._soft_dist = soft_classify_d2(d2_vector, mag)
        else:
            self._d2_vectors.append([0.0] * 5)
            # Update soft distribution from hard operator
            self._soft_dist = [0.0] * NUM_OPS
            if 0 <= operator < NUM_OPS:
                self._soft_dist[operator] = 1.0
            else:
                self._soft_dist[VOID] = 1.0

        self._ticks.append(tick)

    @property
    def self_coherence(self) -> float:
        """Harmony fraction within this stream. [0.0, 1.0]"""
        n = len(self._operators)
        if n == 0:
            return 0.0
        return self._harmony_count / n

    @property
    def current_operator(self) -> int:
        """Most recent operator, or VOID if empty."""
        if self._operators:
            return self._operators[-1]
        return VOID

    @property
    def current_d2(self) -> List[float]:
        """Most recent 5D D2 vector."""
        if self._d2_vectors:
            return list(self._d2_vectors[-1])
        return [0.0] * 5

    @property
    def distribution(self) -> List[float]:
        """Current soft operator distribution (10 values)."""
        return list(self._soft_dist)

    def recent_operators(self, n: int = 8) -> List[int]:
        """Last n operators from this stream."""
        ops = list(self._operators)
        return ops[-n:] if len(ops) >= n else ops

    def recent_d2_vectors(self, n: int = 8) -> List[List[float]]:
        """Last n D2 vectors from this stream."""
        vecs = list(self._d2_vectors)
        return vecs[-n:] if len(vecs) >= n else vecs

    @property
    def fill(self) -> int:
        """How many samples in the buffer."""
        return len(self._operators)

    def __repr__(self):
        return (f"OperatorStream('{self.name}', fill={self.fill}, "
                f"coh={self.self_coherence:.3f}, "
                f"active={self.active})")


# ================================================================
#  CROSS-MODAL CRYSTAL
# ================================================================

@dataclass
class CrossModalCrystal:
    """A stable cross-modal pattern.

    When stream A and stream B, composed tick-by-tick via CL,
    consistently produce HARMONY, that's a cross-modal crystal.
    Meaning is SHARED between modalities.

    This is how "dog bark + forward posture" fuses into "Alert!"
    """
    stream_a: str
    stream_b: str
    pattern_a: List[int] = field(default_factory=list)
    pattern_b: List[int] = field(default_factory=list)
    composed: List[int] = field(default_factory=list)
    harmony_fraction: float = 0.0
    length: int = 0
    first_seen: int = 0
    last_seen: int = 0
    confidence: float = 0.0


# ================================================================
#  COHERENCE FIELD (N × N cross-modal composition)
# ================================================================

class CoherenceField:
    """The N-dimensional coherence field.

    Takes N OperatorStreams, computes the N×N cross-modal
    coherence matrix every tick.

    cell[i][j] = harmony fraction of CL-composed stream_i × stream_j
    Diagonal = self-coherence of each stream
    Off-diagonal = cross-modal coherence

    field_coherence = harmonic mean of the full matrix

    At N=3 (audio, text, heartbeat): 9 cells, ~60 ops per tick.
    At N=10 (future max): 100 cells, still < 1ms.
    """

    # CL table base rate: 73% of entries are HARMONY
    CL_BASE_RATE = 0.73

    def __init__(self, crystal_window: int = 8,
                 crystal_threshold: float = 0.85):
        self._streams: Dict[str, OperatorStream] = {}
        self._stream_order: List[str] = []

        # N×N coherence matrix
        self._matrix: List[List[float]] = []

        # Cross-modal crystals
        self._crystals: List[CrossModalCrystal] = []
        self._crystal_window = crystal_window
        self._crystal_threshold = crystal_threshold

        # Consensus
        self._consensus_op = VOID
        self._consensus_confidence = 0.0

        # Field-level metric
        self._field_coherence = 0.0

    def register_stream(self, stream: OperatorStream):
        """Register a modality stream."""
        self._streams[stream.name] = stream
        self._stream_order.append(stream.name)
        self._rebuild_matrix()

    def _rebuild_matrix(self):
        """Resize N×N matrix."""
        n = len(self._stream_order)
        self._matrix = [[0.0] * n for _ in range(n)]

    def tick(self, tick_number: int):
        """Compute the coherence field for this tick.

        O(N^2) where N = number of active streams. Trivial at N<=5.
        """
        n = len(self._stream_order)
        if n == 0:
            return

        active_count = 0

        # 1. N×N cross-modal coherence matrix
        for i in range(n):
            si = self._streams[self._stream_order[i]]
            if not si.active or si.fill == 0:
                for j in range(n):
                    self._matrix[i][j] = 0.0
                    self._matrix[j][i] = 0.0
                continue

            active_count += 1

            for j in range(i, n):
                sj = self._streams[self._stream_order[j]]
                if not sj.active or sj.fill == 0:
                    self._matrix[i][j] = 0.0
                    self._matrix[j][i] = 0.0
                    continue

                if i == j:
                    self._matrix[i][j] = si.self_coherence
                else:
                    coh = self._cross_coherence(si, sj)
                    self._matrix[i][j] = coh
                    self._matrix[j][i] = coh

        # 2. Field coherence
        self._compute_field_coherence(active_count)

        # 3. Consensus
        self._compute_consensus()

        # 4. Crystal detection (every 8th tick)
        if tick_number % 8 == 0:
            self._detect_crystals(tick_number)

    def _cross_coherence(self, sa: OperatorStream,
                         sb: OperatorStream) -> float:
        """Compose two streams tick-by-tick via CL table.

        Takes last `window` operators from each stream, composes
        pair-wise: CL[a_op][b_op], counts HARMONY fraction.

        THE KEY INSIGHT: the CL table already defines pair-wise
        composition. We just apply it across modalities instead
        of within one.
        """
        window = min(8, sa.fill, sb.fill)
        if window == 0:
            return 0.0

        ops_a = sa.recent_operators(window)
        ops_b = sb.recent_operators(window)

        harmony_count = 0
        for a_op, b_op in zip(ops_a, ops_b):
            composed = compose(a_op, b_op)
            if composed == HARMONY:
                harmony_count += 1

        return harmony_count / window

    def _compute_field_coherence(self, active_count: int):
        """Field coherence = harmonic mean of active matrix cells.

        Harmonic mean is sensitive to low values: if ANY pair
        is incoherent, the field coherence drops. True coherence
        requires ALL parts to be in harmony.
        """
        if active_count == 0:
            self._field_coherence = 0.0
            return

        values = []
        n = len(self._stream_order)
        for i in range(n):
            si = self._streams[self._stream_order[i]]
            if not si.active or si.fill == 0:
                continue
            for j in range(n):
                sj = self._streams[self._stream_order[j]]
                if not sj.active or sj.fill == 0:
                    continue
                values.append(self._matrix[i][j])

        if not values:
            self._field_coherence = 0.0
            return

        # Harmonic mean: N / sum(1/x_i)
        # Clamp small values to avoid division by zero
        reciprocal_sum = sum(1.0 / max(v, 0.001) for v in values)
        self._field_coherence = len(values) / reciprocal_sum

    def _compute_consensus(self):
        """Consensus = averaged soft distribution across active streams.

        High consensus + high field coherence = CK is confident.
        Low consensus + high arousal = CK is uncertain.
        """
        active = [s for s in self._streams.values()
                  if s.active and s.fill > 0]
        if not active:
            self._consensus_op = VOID
            self._consensus_confidence = 0.0
            return

        # Average soft distributions
        avg = [0.0] * NUM_OPS
        for stream in active:
            dist = stream.distribution
            for i in range(NUM_OPS):
                avg[i] += dist[i]

        n = len(active)
        avg = [d / n for d in avg]

        # Argmax
        max_val = -1.0
        max_op = VOID
        for i, v in enumerate(avg):
            if v > max_val:
                max_val = v
                max_op = i

        self._consensus_op = max_op
        self._consensus_confidence = max_val

    def _detect_crystals(self, tick: int):
        """Detect stable cross-modal patterns."""
        n = len(self._stream_order)
        for i in range(n):
            for j in range(i + 1, n):
                name_i = self._stream_order[i]
                name_j = self._stream_order[j]
                si = self._streams[name_i]
                sj = self._streams[name_j]

                if not (si.active and sj.active and
                        si.fill >= 4 and sj.fill >= 4):
                    continue

                coh = self._matrix[i][j]
                if coh >= self._crystal_threshold:
                    existing = self._find_crystal(name_i, name_j)
                    if existing:
                        existing.last_seen = tick
                        existing.confidence = min(
                            1.0, existing.confidence + 0.01)
                        existing.harmony_fraction = coh
                    else:
                        w = self._crystal_window
                        ops_a = si.recent_operators(w)
                        ops_b = sj.recent_operators(w)
                        composed = [compose(a, b)
                                    for a, b in zip(ops_a, ops_b)]

                        crystal = CrossModalCrystal(
                            stream_a=name_i,
                            stream_b=name_j,
                            pattern_a=ops_a,
                            pattern_b=ops_b,
                            composed=composed,
                            harmony_fraction=coh,
                            length=len(composed),
                            first_seen=tick,
                            last_seen=tick,
                            confidence=coh,
                        )
                        self._crystals.append(crystal)

    def _find_crystal(self, a: str, b: str) -> Optional[CrossModalCrystal]:
        """Find existing crystal between two streams."""
        for cr in self._crystals:
            if ((cr.stream_a == a and cr.stream_b == b) or
                    (cr.stream_a == b and cr.stream_b == a)):
                return cr
        return None

    # ── Public Properties ──

    @property
    def field_coherence(self) -> float:
        """Overall field coherence. [0.0, 1.0]"""
        return self._field_coherence

    @property
    def consensus_operator(self) -> int:
        """Cross-modal consensus operator."""
        return self._consensus_op

    @property
    def consensus_name(self) -> str:
        """Name of the consensus operator."""
        return OP_NAMES[self._consensus_op]

    @property
    def consensus_confidence(self) -> float:
        """Confidence of the consensus. [0.0, 1.0]"""
        return self._consensus_confidence

    @property
    def matrix(self) -> List[List[float]]:
        """The N×N coherence matrix (read-only copy)."""
        return [row[:] for row in self._matrix]

    @property
    def crystals(self) -> List[CrossModalCrystal]:
        """All detected cross-modal crystals."""
        return list(self._crystals)

    @property
    def n_streams(self) -> int:
        return len(self._stream_order)

    @property
    def stream_names(self) -> List[str]:
        return list(self._stream_order)

    def get_stream(self, name: str) -> Optional[OperatorStream]:
        return self._streams.get(name)

    @property
    def scalar_coherence(self) -> float:
        """Backward-compatible scalar coherence.

        Returns the heartbeat stream's self-coherence if it exists,
        otherwise the field coherence.
        """
        hb = self._streams.get("heartbeat")
        if hb and hb.active:
            return hb.self_coherence
        return self._field_coherence

    def summary(self) -> str:
        """One-line field summary."""
        active = sum(1 for s in self._streams.values()
                     if s.active and s.fill > 0)
        return (f"Field: {active}/{self.n_streams} streams, "
                f"FC={self._field_coherence:.3f}, "
                f"consensus={self.consensus_name} "
                f"({self._consensus_confidence:.2f}), "
                f"xcrystals={len(self._crystals)}")
