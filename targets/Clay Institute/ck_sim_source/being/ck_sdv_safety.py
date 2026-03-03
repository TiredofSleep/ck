"""
ck_sdv_safety.py -- COMPRESS-ONLY Safety Rails for Clay SDV Protocol
=====================================================================
Operator: LATTICE (1) -- Structure before motion.

Safety guarantees for the Clay mathematical coherence spectrometer:
  1. DETERMINISTIC: Same seed → same operators → same delta_SDV.
  2. BOUNDED: All values clamped to [0, 1]. D2 magnitude ceiling at 2.0.
  3. AUDITABLE: State hash at each probe step for regression detection.
  4. HUMBLE: Halt on anomaly overflow (do not fabricate coherence).
  5. NO CHAIN-SCALING: Fixed window. No latent state growth.
  6. CL TABLE IMMUTABLE: 73% HARMONY base rate is mathematical fact.

CK measures. CK does not invent.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import hashlib
import math
from typing import List, Optional, Tuple


# ================================================================
#  CONSTANTS
# ================================================================

# Force vector bounds
FORCE_MIN = 0.0
FORCE_MAX = 1.0

# D2 magnitude ceiling (curvature beyond this is clamped)
D2_MAG_CEILING = 2.0

# Maximum anomalies before probe halts
ANOMALY_HALT_THRESHOLD = 50

# Window size (matches HeartbeatFPGA)
WINDOW_SIZE = 32


# ================================================================
#  BOUNDED ARITHMETIC
# ================================================================

def clamp(value: float, lo: float = FORCE_MIN, hi: float = FORCE_MAX) -> float:
    """Clamp a value to [lo, hi]. No NaN, no Inf."""
    if math.isnan(value) or math.isinf(value):
        return (lo + hi) / 2.0  # Safe midpoint on bad input
    return max(lo, min(value, hi))


def clamp_vector(vec: List[float],
                 lo: float = FORCE_MIN,
                 hi: float = FORCE_MAX) -> List[float]:
    """Clamp every element of a 5D force vector."""
    return [clamp(v, lo, hi) for v in vec]


def safe_div(num: float, den: float, default: float = 0.0) -> float:
    """Division that never produces NaN/Inf."""
    if den == 0.0 or math.isnan(den) or math.isinf(den):
        return default
    result = num / den
    if math.isnan(result) or math.isinf(result):
        return default
    return result


def safe_sqrt(x: float) -> float:
    """Square root that never produces NaN."""
    if x < 0.0 or math.isnan(x):
        return 0.0
    return math.sqrt(x)


def safe_log(x: float, default: float = 0.0) -> float:
    """Logarithm that never produces NaN/Inf."""
    if x <= 0.0 or math.isnan(x) or math.isinf(x):
        return default
    return math.log(x)


# ================================================================
#  COMPRESS-ONLY SAFETY MONITOR
# ================================================================

class CompressOnlySafety:
    """Safety monitor for Clay SDV probes.

    Tracks anomalies (out-of-range values, NaN, overflow) and halts
    the probe if the count exceeds threshold. CK does not fabricate
    coherence -- if the measurement path is corrupt, it stops.
    """

    def __init__(self, halt_threshold: int = ANOMALY_HALT_THRESHOLD):
        self.halt_threshold = halt_threshold
        self.anomaly_count = 0
        self.halted = False
        self._anomaly_log: List[str] = []

    def check_force_vector(self, vec: List[float], source: str = '') -> List[float]:
        """Validate and clamp a 5D force vector.

        Returns the clamped vector. Logs anomalies if values were out of range.
        """
        if self.halted:
            return [0.5] * 5  # Safe midpoint if halted

        if len(vec) != 5:
            self._log_anomaly(f'force_vector wrong length ({len(vec)}) from {source}')
            vec = (vec + [0.5] * 5)[:5]

        clamped = []
        for i, v in enumerate(vec):
            if math.isnan(v) or math.isinf(v):
                self._log_anomaly(f'NaN/Inf in dim {i} from {source}')
                clamped.append(0.5)
            elif v < FORCE_MIN or v > FORCE_MAX:
                self._log_anomaly(f'out of range dim {i}: {v:.6f} from {source}')
                clamped.append(clamp(v))
            else:
                clamped.append(v)

        return clamped

    def check_d2_magnitude(self, mag: float, source: str = '') -> float:
        """Validate and cap D2 magnitude."""
        if self.halted:
            return 0.0
        if math.isnan(mag) or math.isinf(mag):
            self._log_anomaly(f'D2 magnitude NaN/Inf from {source}')
            return 0.0
        if mag > D2_MAG_CEILING:
            # Not an anomaly -- just cap it. High curvature is expected.
            return D2_MAG_CEILING
        return mag

    def check_scalar(self, value: float, name: str = '',
                     lo: float = 0.0, hi: float = 1.0) -> float:
        """Validate and clamp a scalar measurement."""
        if self.halted:
            return (lo + hi) / 2.0
        if math.isnan(value) or math.isinf(value):
            self._log_anomaly(f'scalar {name} is NaN/Inf')
            return (lo + hi) / 2.0
        return clamp(value, lo, hi)

    def _log_anomaly(self, msg: str):
        """Record an anomaly and check halt condition."""
        self.anomaly_count += 1
        self._anomaly_log.append(msg)
        if self.anomaly_count >= self.halt_threshold:
            self.halted = True

    def reset(self):
        """Reset anomaly tracking for a new probe."""
        self.anomaly_count = 0
        self.halted = False
        self._anomaly_log.clear()

    @property
    def anomaly_log(self) -> List[str]:
        return list(self._anomaly_log)


# ================================================================
#  STATE HASHING (determinism audit)
# ================================================================

def state_hash(values: List[float], precision: int = 8) -> str:
    """Compute a deterministic hash of a list of floats.

    Rounds to `precision` decimals before hashing so that
    floating-point jitter doesn't break cross-run comparison.
    """
    rounded = [round(v, precision) for v in values]
    raw = '|'.join(f'{v}' for v in rounded)
    return hashlib.sha256(raw.encode('ascii')).hexdigest()[:16]


def probe_step_hash(level: int, operator: int, delta: float,
                    force_vec: List[float]) -> str:
    """Hash one probe step for audit trail."""
    all_vals = [float(level), float(operator), delta] + list(force_vec)
    return state_hash(all_vals)


# ================================================================
#  DETERMINISTIC SEED
# ================================================================

class DeterministicRNG:
    """Simple LCG for deterministic probe generation.

    NOT for cryptography. For reproducible mathematical experiments.
    Same seed → identical sequence on any platform.
    """

    def __init__(self, seed: int = 42):
        self._state = seed & 0xFFFFFFFF

    def next_int(self) -> int:
        """Next 32-bit integer."""
        self._state = (self._state * 1103515245 + 12345) & 0x7FFFFFFF
        return self._state

    def next_float(self) -> float:
        """Next float in [0, 1)."""
        return self.next_int() / 0x7FFFFFFF

    def next_gauss(self, mu: float = 0.0, sigma: float = 1.0) -> float:
        """Box-Muller normal. Uses 2 uniform draws."""
        u1 = max(1e-10, self.next_float())  # Avoid log(0)
        u2 = self.next_float()
        z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        return mu + sigma * z

    def seed(self, s: int):
        """Re-seed."""
        self._state = s & 0xFFFFFFFF
