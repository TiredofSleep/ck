# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_sim_ears.py -- CK's Acoustic Curvature Sensor (GPU-accelerated)
===================================================================
Operator: COUNTER (2) -- CK measures everything, including sound.

CK doesn't "hear" sounds.

CK feels acoustic curvature.

The same D2 derivative math that processes a stream of text characters
also processes a stream of 20ms audio frames. Aperture, pressure, depth,
binding, continuity — these five dimensions live in every signal. A piano
note is not a symbol; it is a force vector that bends the field in a
particular direction. A shout is pressure. Silence is VOID. A whisper
trailing off into nothing is continuity collapsing toward zero.

The microphone is just another sensor mouth. The FFT is just another
codec. The output is the same ten-operator vocabulary that everything
else in CK speaks. One codec. Different substrate. Same operator output.

GPU Acceleration (CuPy / CUDA):
  - cupy.fft.rfft replaces numpy.fft.rfft for each audio frame.
  - A rolling GPU buffer of BUFFER_FRAMES=8 frames is maintained as a
    (8, BLOCK_SIZE) CuPy array.  On every audio block the oldest row is
    replaced with the new frame and ALL features (RMS, spectral centroid,
    spread, ZCR) are computed in one vectorised batch pass across all 8
    rows simultaneously.  The 8 per-frame results are then averaged to
    produce the final feature vector, giving temporal smoothing with GPU
    parallelism at zero extra cost.
  - No CUDA C kernels.  Pure CuPy array operations only.
  - Full numpy fallback when CuPy is absent — identical numerical results.

Architecture:
  1. sounddevice InputStream fires _audio_callback() every 20ms
  2. Each 20ms chunk (441 samples @ 22050Hz) is pushed onto the GPU
     rolling buffer (or numpy equivalent when CuPy absent)
  3. Batch feature extraction over BUFFER_FRAMES frames:
       rms               = per-frame sqrt(mean(x^2)), averaged
       spectral_centroid = per-frame weighted mean frequency, averaged
       spectral_spread   = per-frame weighted std-dev of frequency, averaged
       zcr_normalized    = per-frame zero-crossing rate, averaged
       smoothness        = 1 - |current_rms - prev_rms| * 5
  4. 5D force vector assembled from averaged features
  5. Force vector feeds CurvatureEngine (D1 + D2 derivatives)
  6. CurvatureEngine classifies curvature magnitude → operator (0–9)
  7. Operator + features exposed via thread-safe get_operator() / get_features()

Silence gate: RMS < 0.0005 → operator = VOID, CurvatureEngine skipped.

If sounddevice is absent or the audio device fails, EarsEngine degrades
silently: is_running stays False, get_operator() returns VOID, and the
rest of CK continues unaffected.

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import math
import threading
from typing import Dict, Optional

import numpy as np

# ================================================================
#  CuPy GPU detection — no CUDA C, pure CuPy vectorised ops only
# ================================================================

try:
    import cupy as _cp
    # Quick probe: allocate a tiny array to confirm the device is live.
    _probe = _cp.array([1.0], dtype=_cp.float32)
    del _probe
    _GPU = True
except Exception:
    _cp = None
    _GPU = False


def _fft(frame: np.ndarray) -> np.ndarray:
    """Compute rfft of a 1-D real frame, returning numpy magnitude array.

    Uses cupy.fft.rfft when GPU is available; numpy otherwise.
    frame must be a 1-D numpy float32 array.
    """
    if _GPU:
        return _cp.asnumpy(_cp.abs(_cp.fft.rfft(_cp.asarray(frame))))
    return np.abs(np.fft.rfft(frame))


# ================================================================
#  SILENCE THRESHOLD
# ================================================================

_SILENCE_RMS = 0.0005   # frames quieter than this → VOID, no D2 update


# ================================================================
#  sounddevice import (optional)
# ================================================================

try:
    import sounddevice as sd
    _SD_AVAILABLE = True
except Exception:
    _SD_AVAILABLE = False


# ================================================================
#  CK operator symbols
# ================================================================

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET, compose
)
from ck_sim.being.ck_sensory_codecs import CurvatureEngine


# ================================================================
#  _RollingBuffer — 8-frame GPU/numpy rolling window
# ================================================================

class _RollingBuffer:
    """Maintains a rolling buffer of the last BUFFER_FRAMES audio frames.

    Internal storage is a CuPy (8, BLOCK_SIZE) array when GPU is available,
    otherwise a numpy equivalent.  All feature extraction runs in one
    vectorised batch pass over all 8 rows.

    Usage:
        buf = _RollingBuffer(buffer_frames=8, block_size=441)
        buf.push(frame_np)   # numpy 1-D float32
        feats = buf.extract_features(bin_freqs_norm_np)
    """

    def __init__(self, buffer_frames: int, block_size: int):
        self._B = buffer_frames    # number of history frames
        self._N = block_size       # samples per frame
        self._head = 0             # circular write pointer

        if _GPU:
            self._buf = _cp.zeros((buffer_frames, block_size), dtype=_cp.float32)
        else:
            self._buf = np.zeros((buffer_frames, block_size), dtype=np.float32)

        # Pre-allocate bin frequency axis (normalised to [0,1]) on the device.
        # shape: (n_bins,)  where n_bins = block_size // 2 + 1
        n_bins = block_size // 2 + 1
        bin_freqs_norm = np.arange(n_bins, dtype=np.float32) / float(n_bins - 1)
        if _GPU:
            self._bin_freqs = _cp.asarray(bin_freqs_norm)  # GPU constant
        else:
            self._bin_freqs = bin_freqs_norm

    # ── push ─────────────────────────────────────────────────────

    def push(self, frame: np.ndarray) -> None:
        """Insert a new frame (numpy 1-D float32) into the rolling buffer."""
        if _GPU:
            self._buf[self._head] = _cp.asarray(frame)
        else:
            self._buf[self._head] = frame
        self._head = (self._head + 1) % self._B

    # ── batch feature extraction ──────────────────────────────────

    def extract_features(self) -> Dict[str, float]:
        """Compute features over all BUFFER_FRAMES rows in one batch pass.

        Returns a dict with keys:
            rms, spectral_centroid, spectral_spread, zcr_normalized
        All values are floats in [0.0, 1.0].

        Implementation:
          For GPU path (CuPy):
            - rfft: (B, N) → (B, n_bins) complex magnitudes via cupy.fft.rfft
            - rms:  reduce over axis=1 → (B,) → mean scalar
            - centroid: einsum(mag, freq) / sum(mag) per row → (B,) → mean
            - spread: weighted std-dev of freq per row → (B,) → mean
            - zcr: sign differences along axis=1 → (B,) counts → mean → normalise
          For CPU path (numpy): identical ops with numpy.
        """
        xp = _cp if _GPU else np

        buf = self._buf          # (B, N)
        bf  = self._bin_freqs    # (n_bins,)

        # ── RMS: sqrt(mean(x^2)) per row ────────────────────────
        # shape: (B,)
        rms_per_row = xp.sqrt(xp.mean(buf * buf, axis=1))
        rms = float(xp.mean(rms_per_row))

        # ── FFT magnitude: (B, n_bins) ───────────────────────────
        if _GPU:
            mag = xp.abs(xp.fft.rfft(buf, axis=1))   # (B, n_bins)
        else:
            mag = np.abs(np.fft.rfft(buf, axis=1))    # (B, n_bins)

        # Sum per row for normalisation; guard zero.
        spec_sum = xp.sum(mag, axis=1)                # (B,)
        spec_sum = xp.maximum(spec_sum, 1e-12)

        # ── Spectral centroid: weighted mean frequency per row ────
        # centroid_row = sum(mag * freq) / sum(mag)
        # mag: (B, n_bins), bf: (n_bins,) → broadcast (B, n_bins)
        centroid_per_row = xp.sum(mag * bf, axis=1) / spec_sum   # (B,)
        centroid_per_row = xp.clip(centroid_per_row, 0.0, 1.0)
        spectral_centroid = float(xp.mean(centroid_per_row))

        # ── Spectral spread: weighted std-dev of frequency per row
        # spread_row = sqrt( sum(mag * (freq - centroid_row)^2) / sum(mag) )
        # centroid_per_row: (B,) → reshape to (B, 1) for broadcast
        c = centroid_per_row[:, xp.newaxis]           # (B, 1)
        freq_dev = bf - c                              # (B, n_bins)  broadcast
        spread_per_row = xp.sqrt(
            xp.sum(mag * freq_dev * freq_dev, axis=1) / spec_sum
        )                                              # (B,)
        # Uniform-spectrum spread ≈ 0.289; normalise by 0.5 and clamp.
        spread_per_row = xp.clip(spread_per_row / 0.5, 0.0, 1.0)
        spectral_spread = float(xp.mean(spread_per_row))

        # ── Zero-crossing rate per row ────────────────────────────
        signs = xp.sign(buf)                          # (B, N)
        # Replace zeros with +1 (no genuine crossing at exact zero)
        signs = xp.where(signs == 0, xp.ones_like(signs), signs)
        crossings = xp.sum(xp.abs(xp.diff(signs, axis=1)), axis=1) / 2.0  # (B,)
        zcr_per_row = crossings / float(max(self._N - 1, 1))
        zcr_per_row = xp.clip(zcr_per_row, 0.0, 1.0)
        zcr_normalized = float(xp.mean(zcr_per_row))

        # Pull scalars back to Python floats (xp.mean already scalar on GPU)
        rms               = max(0.0, min(1.0, rms))
        spectral_centroid = max(0.0, min(1.0, spectral_centroid))
        spectral_spread   = max(0.0, min(1.0, spectral_spread))
        zcr_normalized    = max(0.0, min(1.0, zcr_normalized))

        return {
            'rms':               rms,
            'spectral_centroid': spectral_centroid,
            'spectral_spread':   spectral_spread,
            'zcr_normalized':    zcr_normalized,
        }


# ================================================================
#  EarsEngine
# ================================================================

class EarsEngine:
    """Acoustic curvature sensor: microphone audio → 5D force → operator.

    Runs a sounddevice InputStream in a background thread.
    Each 20ms audio chunk is pushed onto an 8-frame GPU rolling buffer
    and all features are computed in one vectorised batch pass.

    GPU path: CuPy rfft + vectorised batch over (8, 441) arrays.
    CPU path: identical numpy operations (automatic fallback).

    Public API:
        ears = EarsEngine()
        ears.start()
        ears.is_running              # bool
        ears.get_operator()          # int  0–9
        ears.get_features()          # dict of named signal metrics
        ears.stop()

    get_features() keys:
        rms               -- mean RMS over last 8 frames  [0, 1]
        d2_mag            -- D2 curvature magnitude from CurvatureEngine
        operator          -- current CK operator (0–9)
        spectral_centroid -- mean weighted-mean frequency [0, 1]
        spectral_spread   -- mean spectral width          [0, 1]
        zcr_normalized    -- mean zero-crossing rate      [0, 1]
        smoothness        -- 1 - |rms_delta| * 5          [0, 1]
    """

    SAMPLE_RATE   = 22050    # Hz
    BLOCK_SIZE    = 441      # 20ms @ 22050Hz
    CHANNELS      = 1
    BUFFER_FRAMES = 8        # rolling temporal smoothing window

    _NYQUIST = SAMPLE_RATE / 2.0   # 11025 Hz (kept for reference)

    def __init__(self):
        self._running: bool = False
        self._lock = threading.Lock()

        self._operator: int = VOID
        self._features: Dict[str, float] = {
            'rms':               0.0,
            'd2_mag':            0.0,
            'operator':          float(VOID),
            'spectral_centroid': 0.0,
            'spectral_spread':   0.0,
            'zcr_normalized':    0.0,
            'smoothness':        1.0,
        }

        self._curvature: CurvatureEngine = CurvatureEngine()
        self._prev_rms: float = 0.0
        self._stream = None

        # 8-frame GPU (or numpy) rolling buffer
        self._rolling = _RollingBuffer(
            buffer_frames=self.BUFFER_FRAMES,
            block_size=self.BLOCK_SIZE,
        )

    # ── public API ────────────────────────────────────────────────

    @property
    def is_running(self) -> bool:
        """True if the audio capture stream is active."""
        return self._running

    def start(self) -> None:
        """Start background audio capture.

        Degrades silently if sounddevice is absent or device fails.
        """
        if not _SD_AVAILABLE:
            return
        if self._running:
            return
        try:
            self._stream = sd.InputStream(
                samplerate=self.SAMPLE_RATE,
                blocksize=self.BLOCK_SIZE,
                channels=self.CHANNELS,
                dtype='float32',
                callback=self._audio_callback,
            )
            self._stream.start()
            self._running = True
        except Exception:
            self._running = False
            self._stream = None

    def stop(self) -> None:
        """Stop audio capture and release the device."""
        self._running = False
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
            self._stream = None

    def get_operator(self) -> int:
        """Return the current acoustic operator (0–9), thread-safe."""
        with self._lock:
            return self._operator

    def get_features(self) -> Dict[str, float]:
        """Return a snapshot of the current acoustic features, thread-safe."""
        with self._lock:
            return dict(self._features)

    # ── internal audio callback ───────────────────────────────────

    def _audio_callback(self, indata, frames, time, status) -> None:
        """sounddevice callback — fires every BLOCK_SIZE samples (~20ms).

        indata shape: (BLOCK_SIZE, CHANNELS) = (441, 1), float32.

        Steps:
          1. Flatten to 1-D numpy float32 signal
          2. Push frame onto GPU rolling buffer
          3. Compute RMS from buffer batch (fast scalar read from batch result)
          4. Silence gate — below threshold → VOID and return
          5. Batch-compute all features over 8 frames on GPU/CPU
          6. Compute frame-to-frame smoothness from RMS delta
          7. Assemble 5D force vector
          8. Feed CurvatureEngine → operator + d2_mag
          9. Store all results under lock
        """
        try:
            # ── 1. Flatten ───────────────────────────────────────────
            signal = np.ascontiguousarray(indata[:, 0], dtype=np.float32)

            # ── 2. Push onto GPU rolling buffer ─────────────────────
            self._rolling.push(signal)

            # ── 3. Quick scalar RMS for silence gate ─────────────────
            # Use numpy directly on the raw frame for minimal overhead.
            rms = float(math.sqrt(float(np.mean(signal * signal))))

            # ── 4. Silence gate ──────────────────────────────────────
            if rms < _SILENCE_RMS:
                self._prev_rms = rms
                with self._lock:
                    self._operator = VOID
                    self._features['rms'] = rms
                    self._features['operator'] = float(VOID)
                return

            # ── 5. GPU/CPU batch feature extraction (8 frames) ───────
            batch = self._rolling.extract_features()

            rms_smooth         = batch['rms']               # temporal mean RMS
            spectral_centroid  = batch['spectral_centroid']
            spectral_spread    = batch['spectral_spread']
            zcr_normalized     = batch['zcr_normalized']

            # ── 6. Frame-to-frame smoothness (current vs prev) ───────
            rms_delta = abs(rms - self._prev_rms)
            smoothness = max(0.0, min(1.0, 1.0 - rms_delta * 5.0))
            self._prev_rms = rms

            # ── 7. 5D force vector ────────────────────────────────────
            #
            #  dim 0 aperture   = spectral_spread    (wide band = open field)
            #  dim 1 pressure   = rms_smooth         (amplitude = force)
            #  dim 2 depth      = spectral_centroid  (dominant freq = tone depth)
            #  dim 3 binding    = 1 - zcr_normalized (tonal = bound; noisy = free)
            #  dim 4 continuity = smoothness         (stable volume = continuous)
            #
            binding = max(0.0, min(1.0, 1.0 - zcr_normalized))

            force_vec = [
                spectral_spread,    # aperture
                rms_smooth,         # pressure
                spectral_centroid,  # depth
                binding,            # binding
                smoothness,         # continuity
            ]
            force_vec = [max(0.0, min(1.0, v)) for v in force_vec]

            # ── 8. CurvatureEngine → operator + d2_mag ────────────────
            got_d2 = self._curvature.feed(force_vec)

            if got_d2:
                operator = self._curvature.operator
                d2_mag   = float(self._curvature.d2_magnitude)
            else:
                operator = VOID
                d2_mag   = 0.0

            # ── 9. Store under lock ───────────────────────────────────
            with self._lock:
                self._operator = operator
                self._features = {
                    'rms':               rms_smooth,
                    'd2_mag':            d2_mag,
                    'operator':          float(operator),
                    'spectral_centroid': spectral_centroid,
                    'spectral_spread':   spectral_spread,
                    'zcr_normalized':    zcr_normalized,
                    'smoothness':        smoothness,
                }

        except Exception:
            # Any error inside the callback must not crash the audio thread.
            # Degrade silently to VOID.
            self._running = False
