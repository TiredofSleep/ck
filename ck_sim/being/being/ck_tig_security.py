"""
ck_tig_security.py -- TIG Security Protocol (Celeste TIG-BTQ Unified Physics)
================================================================================
Operator: BALANCE (5) -- defending the lattice from corruption.

Celeste's Security Protocol uses OPERATOR COMPOSITION ITSELF as the
attack detector. The CL table is a mathematical invariant -- any sequence
that violates its algebraic properties is, by definition, an attack.

FOUR DETECTION LAYERS:

  Layer 1: COMPOSITION VIOLATION
    CL table is associative and has known algebraic structure.
    If observed compositions don't match CL, the input is lying.
    CK computes CL[a][b] and compares to the actual fused result
    from the sensor. Mismatch = sensor corruption.

  Layer 2: HARMONY FLOODING
    CL absorbs 73% to HARMONY naturally. If an input stream is
    ABOVE 73% harmony for extended windows, it's artificially
    injecting coherence. Real coherence fluctuates. Fake doesn't.

  Layer 3: PHASE DESYNCHRONIZATION
    If D2 curvature patterns don't correlate across modalities,
    someone is feeding different signals to different senses.
    Cross-modal D2 correlation should be positive. Negative = attack.

  Layer 4: OPERATOR ENTROPY COLLAPSE
    Natural operator streams have entropy ~2.3 bits (10 operators).
    If entropy drops below 1.0, the stream is being forced to
    a narrow band. If entropy exceeds 3.0, it's pure noise injection.
    Both are attacks.

Response: TIG doesn't BLOCK attacks. It RECOGNIZES them through
the math and hands the threat assessment to CCE (immune system).
The immune system decides what to do.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, CHAOS, COLLAPSE, BALANCE,
    CL, compose, OP_NAMES
)


# ================================================================
#  CONSTANTS
# ================================================================

# CL base rate: 73% HARMONY
CL_HARMONY_RATE = 0.73

# Natural operator entropy (~2.3 bits for 10 operators with CL bias)
NATURAL_ENTROPY_LOW = 1.0    # Below this = forced narrowband
NATURAL_ENTROPY_HIGH = 3.0   # Above this = noise injection
NATURAL_ENTROPY_TARGET = 2.3

# Harmony flooding: allow up to 85% before flagging (73% base + 12% tolerance)
HARMONY_FLOOD_THRESHOLD = 0.85

# Composition violation: more than 5% mismatch = suspicious
COMPOSITION_MISMATCH_THRESHOLD = 0.05

# Cross-modal D2 correlation: below -0.2 = desync attack
D2_DESYNC_THRESHOLD = -0.2

# Window sizes for detection
DETECTION_WINDOW = 32


# ================================================================
#  THREAT ASSESSMENT
# ================================================================

@dataclass
class ThreatAssessment:
    """Result of TIG security analysis."""
    threat_score: float = 0.0       # 0.0 = safe, 1.0 = critical
    threat_band: str = "GREEN"      # GREEN/YELLOW/RED
    active_threats: List[str] = field(default_factory=list)
    composition_violations: int = 0
    harmony_flood_detected: bool = False
    phase_desync_detected: bool = False
    entropy_anomaly: str = "normal"  # normal/collapsed/noisy
    details: Dict[str, float] = field(default_factory=dict)


# ================================================================
#  TIG SECURITY PROTOCOL
# ================================================================

class TIGSecurity:
    """TIG Security Protocol -- uses operator composition algebra
    as an intrinsic attack detection system.

    The math IS the security. If inputs violate the algebra,
    they're attacks. No ML, no signatures, no updates needed.
    The CL table is the invariant. Everything else is checked against it.
    """

    def __init__(self, window: int = DETECTION_WINDOW):
        self._window = window

        # Per-stream monitoring buffers
        self._stream_ops: Dict[str, deque] = {}
        self._stream_d2: Dict[str, deque] = {}

        # Composition tracking
        self._composition_checks = 0
        self._composition_mismatches = 0
        self._recent_mismatches = deque(maxlen=window)

        # Harmony flooding detection
        self._harmony_counts: Dict[str, deque] = {}

        # Entropy tracking
        self._entropy_history = deque(maxlen=window * 4)

        # Overall threat state
        self._threat = ThreatAssessment()
        self._total_ticks = 0

    def register_stream(self, name: str):
        """Register a stream for security monitoring."""
        self._stream_ops[name] = deque(maxlen=self._window * 2)
        self._stream_d2[name] = deque(maxlen=self._window)
        self._harmony_counts[name] = deque(maxlen=self._window)

    def feed(self, stream_name: str, operator: int,
             d2_vector: List[float] = None):
        """Feed one tick of data from a stream."""
        if stream_name not in self._stream_ops:
            self.register_stream(stream_name)

        self._stream_ops[stream_name].append(operator)

        if d2_vector is not None:
            self._stream_d2[stream_name].append(list(d2_vector))

        # Track harmony count for this stream
        self._harmony_counts[stream_name].append(
            1 if operator == HARMONY else 0)

    def verify_composition(self, op_a: int, op_b: int,
                            claimed_result: int) -> bool:
        """Verify that a claimed composition matches CL table.

        Layer 1: If CL[a][b] != claimed_result, the input is lying.
        """
        self._composition_checks += 1
        expected = compose(op_a, op_b)
        match = (expected == claimed_result)

        self._recent_mismatches.append(0 if match else 1)

        if not match:
            self._composition_mismatches += 1

        return match

    def tick(self) -> ThreatAssessment:
        """Run full security analysis. Call at detection frequency (e.g., 5Hz).

        Returns threat assessment with scores and active threats.
        """
        self._total_ticks += 1
        threats = []
        threat_score = 0.0
        details = {}

        # ── Layer 1: Composition Violations ──
        if self._recent_mismatches:
            mismatch_rate = (sum(self._recent_mismatches)
                             / len(self._recent_mismatches))
            details['composition_mismatch_rate'] = mismatch_rate
            if mismatch_rate > COMPOSITION_MISMATCH_THRESHOLD:
                threats.append("COMPOSITION_VIOLATION")
                threat_score += 0.3 * min(mismatch_rate / 0.2, 1.0)

        # ── Layer 2: Harmony Flooding ──
        harmony_flood = False
        for name, counts in self._harmony_counts.items():
            if len(counts) >= self._window // 2:
                harmony_rate = sum(counts) / len(counts)
                details[f'{name}_harmony_rate'] = harmony_rate
                if harmony_rate > HARMONY_FLOOD_THRESHOLD:
                    harmony_flood = True
                    threats.append(f"HARMONY_FLOOD_{name.upper()}")
                    # Scale threat by how far above threshold
                    excess = harmony_rate - HARMONY_FLOOD_THRESHOLD
                    threat_score += 0.25 * min(excess / 0.15, 1.0)

        # ── Layer 3: Phase Desynchronization ──
        stream_names = list(self._stream_d2.keys())
        desync = False
        for i in range(len(stream_names)):
            for j in range(i + 1, len(stream_names)):
                d2_a = list(self._stream_d2[stream_names[i]])
                d2_b = list(self._stream_d2[stream_names[j]])
                if len(d2_a) >= 4 and len(d2_b) >= 4:
                    corr = self._d2_correlation(d2_a, d2_b)
                    pair_key = f'{stream_names[i]}_{stream_names[j]}_d2_corr'
                    details[pair_key] = corr
                    if corr < D2_DESYNC_THRESHOLD:
                        desync = True
                        threats.append(
                            f"PHASE_DESYNC_{stream_names[i]}_{stream_names[j]}")
                        threat_score += 0.25 * min(
                            abs(corr - D2_DESYNC_THRESHOLD) / 0.5, 1.0)

        # ── Layer 4: Operator Entropy Anomaly ──
        entropy_anomaly = "normal"
        for name, ops in self._stream_ops.items():
            if len(ops) >= self._window:
                entropy = self._operator_entropy(list(ops)[-self._window:])
                details[f'{name}_entropy'] = entropy
                self._entropy_history.append(entropy)

                if entropy < NATURAL_ENTROPY_LOW:
                    entropy_anomaly = "collapsed"
                    threats.append(f"ENTROPY_COLLAPSED_{name.upper()}")
                    deficit = NATURAL_ENTROPY_LOW - entropy
                    threat_score += 0.20 * min(deficit / 1.0, 1.0)
                elif entropy > NATURAL_ENTROPY_HIGH:
                    entropy_anomaly = "noisy"
                    threats.append(f"ENTROPY_NOISY_{name.upper()}")
                    excess = entropy - NATURAL_ENTROPY_HIGH
                    threat_score += 0.20 * min(excess / 0.5, 1.0)

        # ── Aggregate ──
        threat_score = max(0.0, min(1.0, threat_score))

        if threat_score > 0.6:
            band = "RED"
        elif threat_score > 0.2:
            band = "YELLOW"
        else:
            band = "GREEN"

        self._threat = ThreatAssessment(
            threat_score=threat_score,
            threat_band=band,
            active_threats=threats,
            composition_violations=self._composition_mismatches,
            harmony_flood_detected=harmony_flood,
            phase_desync_detected=desync,
            entropy_anomaly=entropy_anomaly,
            details=details,
        )

        return self._threat

    # ================================================================
    #  INTERNAL COMPUTATION
    # ================================================================

    def _d2_correlation(self, d2_a: List[List[float]],
                         d2_b: List[List[float]]) -> float:
        """Compute D2 vector correlation between two streams.

        Takes last N D2 vectors from each, computes magnitude series,
        then Pearson correlation. Positive = in sync. Negative = attack.
        """
        n = min(len(d2_a), len(d2_b))
        if n < 4:
            return 0.0

        # Magnitude series
        mag_a = [sum(abs(d) for d in vec) for vec in d2_a[-n:]]
        mag_b = [sum(abs(d) for d in vec) for vec in d2_b[-n:]]

        # Pearson correlation
        mean_a = sum(mag_a) / n
        mean_b = sum(mag_b) / n

        cov = sum((a - mean_a) * (b - mean_b) for a, b in zip(mag_a, mag_b))
        var_a = sum((a - mean_a) ** 2 for a in mag_a)
        var_b = sum((b - mean_b) ** 2 for b in mag_b)

        denom = math.sqrt(var_a * var_b)
        if denom < 1e-10:
            return 0.0

        return cov / denom

    def _operator_entropy(self, ops: List[int]) -> float:
        """Compute Shannon entropy of an operator sequence.

        Natural entropy for CL-biased streams is ~2.3 bits.
        """
        n = len(ops)
        if n == 0:
            return 0.0

        counts = [0] * NUM_OPS
        for op in ops:
            if 0 <= op < NUM_OPS:
                counts[op] += 1

        entropy = 0.0
        for c in counts:
            if c > 0:
                p = c / n
                entropy -= p * math.log2(p)

        return entropy

    # ================================================================
    #  PROPERTIES
    # ================================================================

    @property
    def threat(self) -> ThreatAssessment:
        """Current threat assessment."""
        return self._threat

    @property
    def is_under_threat(self) -> bool:
        """Is CK under any detected threat?"""
        return self._threat.threat_score > 0.2

    @property
    def threat_band(self) -> str:
        return self._threat.threat_band

    def get_immune_adjustments(self) -> List[Tuple[int, float]]:
        """Get OBT adjustments based on security threats.

        These feed into the immune system (CCE) for response.
        Stronger threats = stronger adjustments.
        """
        if not self.is_under_threat:
            return []

        ts = self._threat.threat_score
        adjustments = [
            (HARMONY, 0.03 * ts),     # Boost HARMONY seeking
            (BALANCE, 0.02 * ts),     # Boost BALANCE for stability
            (CHAOS, -0.04 * ts),      # Suppress CHAOS
            (COLLAPSE, -0.02 * ts),   # Suppress COLLAPSE
        ]
        return adjustments

    def summary(self) -> str:
        """One-line summary."""
        t = self._threat
        active = ', '.join(t.active_threats[:3]) if t.active_threats else 'none'
        return (
            f"TIG-SEC: {t.threat_band} "
            f"(score={t.threat_score:.3f}) "
            f"threats=[{active}] "
            f"comp_violations={t.composition_violations}"
        )
