"""
ck_sim_ears.py -- Port of ck_ears.c
=====================================
Operator: COUNTER (2) -- measuring the physics of sound.

Mic input → audio features → 5D force vector → D2 curvature → operator.
Same math as text D2, different input modality.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import threading
import numpy as np
from collections import deque

from ck_sim.ck_sim_heartbeat import (
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET
)

MIC_SAMPLE_RATE = 48000
FRAME_SIZE = 512   # ~10.7ms at 48kHz
FORCE_HISTORY = 8  # ring buffer size for D2

# D2 operator classification map (matches ck_ears.c lines 160-167)
# [dimension][0=positive, 1=negative]
D2_OP_MAP = [
    [CHAOS,    LATTICE],   # aperture
    [COLLAPSE, VOID],      # pressure
    [PROGRESS, RESET],     # depth
    [HARMONY,  COUNTER],   # binding
    [BALANCE,  BREATH],    # continuity
]


class ForceVector:
    """5D force vector. Matches CK_ForceVector."""
    __slots__ = ('aperture', 'pressure', 'depth', 'binding', 'continuity')

    def __init__(self, a=0.0, p=0.0, d=0.0, b=0.0, c=0.0):
        self.aperture = a
        self.pressure = p
        self.depth = d
        self.binding = b
        self.continuity = c

    def as_list(self):
        return [self.aperture, self.pressure, self.depth,
                self.binding, self.continuity]


# ── Audio Feature Extraction (matches ck_ears.c) ──

def compute_rms(samples):
    """RMS energy. Matches compute_rms()."""
    if len(samples) == 0:
        return 0.0
    return float(np.sqrt(np.mean(samples ** 2)))


def compute_zcr(samples):
    """Zero-crossing rate. Matches compute_zcr()."""
    if len(samples) < 2:
        return 0.0
    signs = np.sign(samples)
    crossings = np.sum(np.abs(np.diff(signs)) > 0)
    return float(crossings / len(samples))


def compute_centroid(samples):
    """Spectral centroid approximation via ZCR. Matches compute_centroid()."""
    zcr = compute_zcr(samples)
    return min(zcr * 2.0, 1.0)


def compute_autocorrelation(samples):
    """Autocorrelation at lag=len/4. Matches compute_autocorrelation()."""
    n = len(samples)
    if n < 4:
        return 0.0
    lag = n // 4
    a = samples[:n - lag].astype(np.float64)
    b = samples[lag:n].astype(np.float64)
    denom = float(np.sum(a * a))
    if denom < 1e-10:
        return 0.0
    num = float(np.sum(a * b))
    return max(-1.0, min(1.0, num / denom))


# ── Force Vector from Features (matches features_to_force()) ──

def features_to_force(rms, zcr, centroid, autocorr, prev_rms):
    """Convert audio features to 5D force vector."""
    f = ForceVector()

    # Aperture: spectral bandwidth
    f.aperture = (1.0 - autocorr) * zcr

    # Pressure: energy level (scaled up, mic signals are quiet)
    f.pressure = min(rms * 10.0, 1.0)

    # Depth: spectral centroid
    f.depth = centroid

    # Binding: periodicity
    f.binding = max(autocorr, 0.0)

    # Continuity: frame-to-frame stability
    energy_change = abs(rms - prev_rms)
    f.continuity = 1.0 - min(energy_change * 20.0, 1.0)

    return f


# ── D2 Curvature (matches compute_d2()) ──

def compute_d2(v0, v1, v2):
    """Second derivative of force vectors: d2 = v0 - 2*v1 + v2."""
    return ForceVector(
        a=v0.aperture - 2.0 * v1.aperture + v2.aperture,
        p=v0.pressure - 2.0 * v1.pressure + v2.pressure,
        d=v0.depth - 2.0 * v1.depth + v2.depth,
        b=v0.binding - 2.0 * v1.binding + v2.binding,
        c=v0.continuity - 2.0 * v1.continuity + v2.continuity,
    )


def d2_magnitude(d2):
    """Magnitude of D2 vector."""
    return math.sqrt(d2.aperture ** 2 + d2.pressure ** 2 +
                     d2.depth ** 2 + d2.binding ** 2 +
                     d2.continuity ** 2)


# ── Operator Classification (matches classify_d2()) ──

def classify_d2(d2, magnitude):
    """Classify D2 curvature into an operator."""
    if magnitude < 0.01:
        return VOID

    dims = d2.as_list()
    max_abs = 0.0
    max_dim = 0
    for i, val in enumerate(dims):
        a = abs(val)
        if a > max_abs:
            max_abs = a
            max_dim = i

    sign_idx = 0 if dims[max_dim] >= 0.0 else 1
    return D2_OP_MAP[max_dim][sign_idx]


# ── Ears Engine ──

class EarsEngine:
    """CK ears: mic input → features → force → D2 → operator.

    Port of CK_Ears + ck_ears_process().
    Uses sounddevice InputStream for mic capture.
    """

    def __init__(self):
        self.operator = VOID
        self.d2_mag = 0.0

        # Feature state
        self.rms_energy = 0.0
        self.zero_cross_rate = 0.0
        self.spectral_centroid = 0.0
        self.autocorrelation = 0.0

        # Force history
        self._forces = [ForceVector() for _ in range(FORCE_HISTORY)]
        self._force_idx = 0
        self._frames_processed = 0

        # Latest force and D2
        self.force = ForceVector()
        self.d2 = ForceVector()

        # Stream
        self._stream = None
        self._running = False
        self._lock = threading.Lock()

        # Accumulation buffer (mic may deliver variable-size chunks)
        self._buf = np.zeros(0, dtype=np.float32)
        self._prev_rms = 0.0

    def _process_frame(self, frame):
        """Process one frame of audio. Matches ck_ears_feed_sample loop."""
        # 1. Features
        prev_rms = self._prev_rms
        self.rms_energy = compute_rms(frame)
        self.zero_cross_rate = compute_zcr(frame)
        self.spectral_centroid = compute_centroid(frame)
        self.autocorrelation = compute_autocorrelation(frame)
        self._prev_rms = self.rms_energy

        # 2. Force vector
        force = features_to_force(
            self.rms_energy, self.zero_cross_rate,
            self.spectral_centroid, self.autocorrelation,
            prev_rms
        )
        self.force = force

        # 3. Store in ring
        self._forces[self._force_idx] = force
        self._force_idx = (self._force_idx + 1) % FORCE_HISTORY

        # 4. D2 curvature (need >= 3 frames)
        if self._frames_processed >= 2:
            i2 = (self._force_idx + FORCE_HISTORY - 1) % FORCE_HISTORY
            i1 = (self._force_idx + FORCE_HISTORY - 2) % FORCE_HISTORY
            i0 = (self._force_idx + FORCE_HISTORY - 3) % FORCE_HISTORY

            self.d2 = compute_d2(
                self._forces[i0], self._forces[i1], self._forces[i2]
            )
            self.d2_mag = d2_magnitude(self.d2)

            # 5. Classify
            self.operator = classify_d2(self.d2, self.d2_mag)

        self._frames_processed += 1

    def _mic_callback(self, indata, frames, time_info, status):
        """sounddevice InputStream callback."""
        # Accumulate samples
        samples = indata[:, 0].copy()

        with self._lock:
            self._buf = np.concatenate([self._buf, samples])

            # Process complete frames
            while len(self._buf) >= FRAME_SIZE:
                frame = self._buf[:FRAME_SIZE]
                self._buf = self._buf[FRAME_SIZE:]
                self._process_frame(frame)

    def start(self):
        """Open mic input stream."""
        if self._running:
            return

        try:
            import sounddevice as sd
        except ImportError:
            print("[EARS] sounddevice not installed. pip install sounddevice")
            return

        try:
            self._stream = sd.InputStream(
                samplerate=MIC_SAMPLE_RATE,
                blocksize=FRAME_SIZE,
                channels=1,
                dtype='float32',
                callback=self._mic_callback,
            )
            self._stream.start()
            self._running = True
            print(f"[EARS] Mic stream started: {MIC_SAMPLE_RATE}Hz, "
                  f"frame={FRAME_SIZE}")
        except Exception as e:
            print(f"[EARS] Failed to start mic: {e}")

    def stop(self):
        """Close mic stream."""
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
            self._stream = None
        self._running = False

    @property
    def is_running(self):
        return self._running

    def get_operator(self):
        """Thread-safe read of current ear operator."""
        with self._lock:
            return self.operator

    def get_force_list(self):
        """Thread-safe read of latest force vector as list."""
        with self._lock:
            return self.force.as_list()

    def get_features(self):
        """Thread-safe read of audio features."""
        with self._lock:
            return {
                'rms': self.rms_energy,
                'zcr': self.zero_cross_rate,
                'centroid': self.spectral_centroid,
                'autocorr': self.autocorrelation,
                'd2_mag': self.d2_mag,
                'operator': self.operator,
            }
