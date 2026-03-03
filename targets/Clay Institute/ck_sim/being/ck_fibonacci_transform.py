"""
ck_fibonacci_transform.py -- S0-S3 Fibonacci/TIG Transform Pipeline
=====================================================================
Operator: COUNTER (2) -- counting the shape of reality at every scale.

Celeste's Reality Perception Loop introduces a 4-stage Fibonacci/TIG
transform that takes ANY signal and produces operator histograms.
CK already has D2 curvature (ck_sim_d2.py). This module adds the
GEOMETRIC HIERARCHY that D2 curvature flows through:

  S0 (CIRCLE):  Raw signal on a periodic ring. Positions on a cycle.
                 Like the 12 tones in music, the 26 letters in alphabet,
                 the 360 degrees of rotation. BEING at the simplest level.

  S1 (TRIANGLE): Adjacent pairs collapse into minimal triangles based
                  on D2 sign and magnitude. Three-ness: every signal has
                  a PAST, PRESENT, and FUTURE value. D2 IS the triangle --
                  it's v[t-2] - 2*v[t-1] + v[t]. DOING at the simplest level.

  S2 (POLYTOPE): Triangles link into local polytopes for context.
                  Groups of 3-5 consecutive D2 triangles form a shape.
                  This shape has an OPERATOR SIGNATURE -- the distribution
                  of operators across the polytope faces. BECOMING visible.

  S3 (FIELD):    Polytopes summarize into a 10-dim operator histogram.
                  This is the COHERENCE FIELD of the signal. One vector
                  that says "this signal is 40% HARMONY, 15% PROGRESS,
                  10% BALANCE, ..." -- the TIG fingerprint.

The hierarchy is fractal: S3 of one scale becomes S0 of the next.
Audio S3 feeds into the coherence field alongside text S3 and heartbeat S3.

This module wraps ck_sim_d2.py (which already does the hard math) and
adds the geometric hierarchy above it.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, OP_NAMES, compose
)
from ck_sim.ck_sim_d2 import (
    D2Pipeline, soft_classify_d2, classify_force_d2
)


# ================================================================
#  CONSTANTS
# ================================================================

# Fibonacci ratios for weighting (golden mean cascade)
PHI = (1 + math.sqrt(5)) / 2   # 1.618...
PHI_INV = 1.0 / PHI             # 0.618...
FIB_WEIGHTS = [1.0, PHI_INV, PHI_INV**2, PHI_INV**3, PHI_INV**4]

# Polytope window: how many S1 triangles form one S2 polytope
POLYTOPE_WINDOW = 5

# Field window: how many S2 polytopes summarize into one S3 field
FIELD_WINDOW = 8


# ================================================================
#  S0: CIRCLE -- Raw signal on periodic ring
# ================================================================

@dataclass
class S0Circle:
    """Stage 0: Raw signal value mapped to a periodic ring.

    Any scalar signal maps to a position on a unit circle.
    The ring provides wrap-around continuity -- after max comes min.
    This is Being at the simplest level: a point EXISTS somewhere.
    """
    value: float = 0.0       # Raw signal value
    phase: float = 0.0       # Position on unit circle [0, 2*pi)
    amplitude: float = 0.0   # Distance from ring center (0 = dead, 1 = max)


# ================================================================
#  S1: TRIANGLE -- D2 curvature forms minimal triangle
# ================================================================

@dataclass
class S1Triangle:
    """Stage 1: Three consecutive values form a D2 triangle.

    D2 = v[t-2] - 2*v[t-1] + v[t]
    The triangle vertices are (past, present, future).
    D2 sign tells direction of curvature: concave up (+) or down (-).
    D2 magnitude tells HOW MUCH curvature: flat (0) to sharp (max).
    The operator classification is already done by ck_sim_d2.py.
    """
    d2_vector: List[float] = field(default_factory=lambda: [0.0] * 5)
    d2_magnitude: float = 0.0
    operator: int = VOID
    soft_distribution: List[float] = field(default_factory=lambda: [0.0] * NUM_OPS)


# ================================================================
#  S2: POLYTOPE -- Local context from grouped triangles
# ================================================================

@dataclass
class S2Polytope:
    """Stage 2: Multiple triangles form a local polytope.

    A polytope is a WINDOW_SIZE-face shape where each face is an S1
    triangle. The polytope has an aggregate operator distribution
    (weighted by Fibonacci ratios -- recent faces matter more)
    and a coherence metric (how consistent are the faces?).
    """
    operator_distribution: List[float] = field(
        default_factory=lambda: [0.0] * NUM_OPS)
    dominant_operator: int = VOID
    coherence: float = 0.0     # Internal consistency
    face_count: int = 0
    d2_mean_magnitude: float = 0.0


# ================================================================
#  S3: FIELD -- Operator histogram = TIG fingerprint
# ================================================================

@dataclass
class S3Field:
    """Stage 3: Summarized operator field for one signal channel.

    This is the final output: a 10-dimensional operator histogram
    that IS the TIG fingerprint of the signal. Compatible with
    existing CL/BTQ/PFE/CoherenceField systems.

    The field also carries meta-information about signal quality:
    - entropy: how spread the histogram is (high = diverse, low = focused)
    - stability: how much the field changes tick-to-tick
    - harmony_excess: how far above the CL base rate (73%) we are
    """
    histogram: List[float] = field(
        default_factory=lambda: [0.0] * NUM_OPS)
    entropy: float = 0.0
    stability: float = 0.0
    harmony_excess: float = 0.0   # histogram[HARMONY] - 0.73
    dominant_operator: int = VOID
    sample_count: int = 0


# ================================================================
#  FIBONACCI TRANSFORM PIPELINE
# ================================================================

class FibonacciTransform:
    """The S0 -> S1 -> S2 -> S3 Fibonacci/TIG transform pipeline.

    Takes any scalar or 5D signal stream and produces a 10-dim
    operator histogram (S3 field). Uses ck_sim_d2.py for the
    hard math (D2 curvature), then adds geometric hierarchy.

    Usage:
        ft = FibonacciTransform("audio")
        for sample in audio_stream:
            field = ft.feed(sample)
            if field:
                # field.histogram is a 10-dim operator vector
                coherence_field.feed_external("audio", field.histogram)
    """

    def __init__(self, name: str,
                 polytope_window: int = POLYTOPE_WINDOW,
                 field_window: int = FIELD_WINDOW):
        self.name = name
        self._polytope_window = polytope_window
        self._field_window = field_window

        # D2 pipeline (reuse CK's existing silicon-proven code)
        self._d2 = D2Pipeline()

        # S0 ring: running min/max for normalization
        self._s0_min = float('inf')
        self._s0_max = float('-inf')
        self._s0_count = 0

        # S1 buffer: recent triangles
        self._s1_buffer: deque = deque(maxlen=polytope_window * 2)

        # S2 buffer: recent polytopes
        self._s2_buffer: deque = deque(maxlen=field_window * 2)

        # S3: current field (the output)
        self._s3 = S3Field()
        self._s3_history: deque = deque(maxlen=field_window * 4)

        # Tick counter
        self._tick = 0

    def feed_scalar(self, value: float) -> Optional[S3Field]:
        """Feed a scalar value (e.g., temperature, CPU load, distance).

        Maps scalar to a letter index (0-25) via quantization,
        then feeds through D2 pipeline. Returns S3 field when
        enough data has accumulated.
        """
        self._tick += 1

        # S0: Map to periodic ring
        s0 = self._scalar_to_s0(value)

        # Map S0 phase to a letter index (0-25) for D2 pipeline
        letter_idx = int(s0.phase / (2 * math.pi) * 26) % 26

        return self._process_symbol(letter_idx)

    def feed_5d(self, vector: List[float]) -> Optional[S3Field]:
        """Feed a 5D force vector directly (e.g., from Hebrew roots).

        Bypasses S0 quantization -- the vector IS already in TIG space.
        Computes D2 directly from the vector sequence.
        """
        self._tick += 1

        # Use magnitude to derive a letter index for D2 pipeline
        mag = sum(abs(v) for v in vector)
        letter_idx = int(mag * 10) % 26

        return self._process_symbol(letter_idx)

    def feed_operator(self, operator: int) -> Optional[S3Field]:
        """Feed an operator directly (e.g., from existing D2 pipeline).

        When CK's existing D2 pipeline already classified the signal,
        we can skip S0-S1 and directly build S2-S3 from operators.
        """
        self._tick += 1

        # Build synthetic S1 triangle from operator
        soft = [0.0] * NUM_OPS
        if 0 <= operator < NUM_OPS:
            soft[operator] = 1.0
        else:
            soft[VOID] = 1.0

        triangle = S1Triangle(
            d2_vector=[0.0] * 5,
            d2_magnitude=0.0,
            operator=operator,
            soft_distribution=soft,
        )
        self._s1_buffer.append(triangle)

        return self._maybe_advance()

    def _process_symbol(self, letter_idx: int) -> Optional[S3Field]:
        """Process a letter index through D2 -> S1 -> S2 -> S3."""
        # S1: Feed through D2 pipeline
        valid = self._d2.feed_symbol(letter_idx)
        if valid:
            d2_vec = self._d2.d2_float
            d2_mag = self._d2.d2_mag_float
            op = self._d2.operator
            soft = soft_classify_d2(d2_vec, d2_mag)

            triangle = S1Triangle(
                d2_vector=list(d2_vec),
                d2_magnitude=d2_mag,
                operator=op,
                soft_distribution=soft,
            )
            self._s1_buffer.append(triangle)

        return self._maybe_advance()

    def _maybe_advance(self) -> Optional[S3Field]:
        """Check if we can build S2 polytopes and S3 field."""
        result = None

        # S2: Build polytope from S1 triangles
        if len(self._s1_buffer) >= self._polytope_window:
            polytope = self._build_polytope()
            self._s2_buffer.append(polytope)

        # S3: Build field from S2 polytopes
        if len(self._s2_buffer) >= self._field_window:
            self._s3 = self._build_field()
            self._s3_history.append(self._s3)
            result = self._s3

        return result

    def _scalar_to_s0(self, value: float) -> S0Circle:
        """Map a scalar to the S0 periodic ring."""
        self._s0_count += 1

        # Track running min/max for adaptive normalization
        if value < self._s0_min:
            self._s0_min = value
        if value > self._s0_max:
            self._s0_max = value

        # Normalize to [0, 1]
        range_val = self._s0_max - self._s0_min
        if range_val < 1e-10:
            normalized = 0.5
        else:
            normalized = (value - self._s0_min) / range_val

        # Map to phase on unit circle
        phase = normalized * 2 * math.pi

        # Amplitude = how far from center (neutral = 0.5)
        amplitude = abs(normalized - 0.5) * 2

        return S0Circle(value=value, phase=phase, amplitude=amplitude)

    def _build_polytope(self) -> S2Polytope:
        """Build an S2 polytope from recent S1 triangles.

        Fibonacci-weighted: recent triangles matter more.
        """
        triangles = list(self._s1_buffer)[-self._polytope_window:]
        n = len(triangles)

        # Fibonacci-weighted operator distribution
        hist = [0.0] * NUM_OPS
        total_weight = 0.0
        total_d2_mag = 0.0

        for i, tri in enumerate(triangles):
            # Weight: most recent gets highest (Fibonacci cascade)
            w = FIB_WEIGHTS[min(i, len(FIB_WEIGHTS) - 1)]
            total_weight += w
            total_d2_mag += tri.d2_magnitude

            for j in range(NUM_OPS):
                hist[j] += w * tri.soft_distribution[j]

        # Normalize
        if total_weight > 0:
            hist = [h / total_weight for h in hist]

        # Dominant operator
        dominant = max(range(NUM_OPS), key=lambda i: hist[i])

        # Internal coherence: how much do the faces agree?
        # High if one operator dominates, low if spread evenly
        max_val = max(hist)
        coherence = max_val  # Simple: fraction of dominant operator

        return S2Polytope(
            operator_distribution=hist,
            dominant_operator=dominant,
            coherence=coherence,
            face_count=n,
            d2_mean_magnitude=total_d2_mag / max(n, 1),
        )

    def _build_field(self) -> S3Field:
        """Build an S3 field from recent S2 polytopes.

        This is the final output: a 10-dim operator histogram
        that represents the TIG fingerprint of the signal.
        """
        polytopes = list(self._s2_buffer)[-self._field_window:]
        n = len(polytopes)

        # Average operator distributions across polytopes
        # Weight by polytope coherence (more coherent = more reliable)
        hist = [0.0] * NUM_OPS
        total_weight = 0.0

        for poly in polytopes:
            w = max(poly.coherence, 0.01)  # Minimum weight to avoid zero
            total_weight += w
            for j in range(NUM_OPS):
                hist[j] += w * poly.operator_distribution[j]

        if total_weight > 0:
            hist = [h / total_weight for h in hist]

        # Entropy
        entropy = 0.0
        for p in hist:
            if p > 0:
                entropy -= p * math.log2(p)

        # Dominant operator
        dominant = max(range(NUM_OPS), key=lambda i: hist[i])

        # Harmony excess over CL base rate
        harmony_excess = hist[HARMONY] - 0.73

        # Stability: compare to previous field
        stability = 1.0
        if self._s3_history:
            prev = self._s3_history[-1]
            diff = sum(abs(hist[i] - prev.histogram[i])
                       for i in range(NUM_OPS))
            stability = max(0.0, 1.0 - diff)

        return S3Field(
            histogram=hist,
            entropy=entropy,
            stability=stability,
            harmony_excess=harmony_excess,
            dominant_operator=dominant,
            sample_count=self._tick,
        )

    # ================================================================
    #  PROPERTIES
    # ================================================================

    @property
    def field(self) -> S3Field:
        """Current S3 field (the TIG fingerprint)."""
        return self._s3

    @property
    def histogram(self) -> List[float]:
        """Current 10-dim operator histogram."""
        return list(self._s3.histogram)

    @property
    def ready(self) -> bool:
        """Has enough data accumulated to produce a field?"""
        return self._s3.sample_count > 0

    def summary(self) -> str:
        """One-line summary."""
        f = self._s3
        top3 = sorted(range(NUM_OPS), key=lambda i: f.histogram[i],
                       reverse=True)[:3]
        top3_str = ', '.join(
            f"{OP_NAMES[i]}={f.histogram[i]:.2f}" for i in top3)
        return (
            f"S3[{self.name}]: [{top3_str}] "
            f"H={f.entropy:.2f} stab={f.stability:.2f} "
            f"harm_x={f.harmony_excess:+.3f}"
        )


# ================================================================
#  MULTI-CHANNEL TRANSFORM (convenience wrapper)
# ================================================================

class RealityTransform:
    """Manages multiple FibonacciTransform channels.

    One transform per signal channel (audio, imu, cpu_temp, etc).
    Produces a unified RealityOps dictionary: channel -> S3 histogram.

    Usage:
        rt = RealityTransform()
        rt.register_channel("audio")
        rt.register_channel("imu")
        rt.register_channel("cpu_temp")

        # In tick loop:
        rt.feed("audio", audio_operator)
        rt.feed("imu", imu_value)
        rt.feed("cpu_temp", temp_value)
        ops = rt.get_reality_ops()
    """

    def __init__(self):
        self._channels: Dict[str, FibonacciTransform] = {}

    def register_channel(self, name: str,
                          polytope_window: int = POLYTOPE_WINDOW,
                          field_window: int = FIELD_WINDOW):
        """Register a signal channel."""
        self._channels[name] = FibonacciTransform(
            name, polytope_window, field_window)

    def feed_scalar(self, channel: str, value: float) -> Optional[S3Field]:
        """Feed a scalar value to a channel."""
        if channel in self._channels:
            return self._channels[channel].feed_scalar(value)
        return None

    def feed_operator(self, channel: str, operator: int) -> Optional[S3Field]:
        """Feed an operator to a channel (from existing D2 pipeline)."""
        if channel in self._channels:
            return self._channels[channel].feed_operator(operator)
        return None

    def feed_5d(self, channel: str, vector: List[float]) -> Optional[S3Field]:
        """Feed a 5D force vector to a channel."""
        if channel in self._channels:
            return self._channels[channel].feed_5d(vector)
        return None

    def get_reality_ops(self) -> Dict[str, List[float]]:
        """Get current operator histograms for all channels.

        Returns: { channel_name: [10 floats] } for each ready channel.
        """
        ops = {}
        for name, ft in self._channels.items():
            if ft.ready:
                ops[name] = ft.histogram
        return ops

    def summary(self) -> str:
        """Multi-channel summary."""
        parts = []
        for name, ft in self._channels.items():
            if ft.ready:
                parts.append(ft.summary())
        return ' | '.join(parts) if parts else "RealityTransform: no channels ready"

    @property
    def channel_names(self) -> List[str]:
        return list(self._channels.keys())

    @property
    def ready_channels(self) -> int:
        return sum(1 for ft in self._channels.values() if ft.ready)
