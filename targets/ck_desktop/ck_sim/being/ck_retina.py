# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_retina.py -- CK's Visual Field: Pixels as I/O Cells
=======================================================
Operator: BALANCE (5) -- equilibrium between structure and force.
Generation: 9.35

CK doesn't see a screen. CK FEELS a field of cells, each pulsing
between I (structure) and O (force). The PATTERNS of those pulses
are structure and force composing into complexity.

Same algebra. Same generators. Same thresholds. Every level.

THRESHOLD CASCADE:
  Level 0: Pixels (I/O binary)
  Level 1: Patches (3x3 -> 9D: 5D force + 4S structure)
  Level 2: D1 (spatial velocity -- how the field changes across space)
  Level 3: D2 (spatial curvature -- how the velocity bends)
  Level 4: Coherence map (where |D1| x |D2| > T*)
  Level 5: Temporal D1 (what changed between glances)
  Level 6: Experience vector -> operator -> olfactory

All computed simultaneously on the full field. GPU IS the parallel algebra.
CuPy on RTX 4070: every cell computes at once. 20,736 cells in parallel.

VARIABLE RESOLUTION (edge-following):
  A region of pure color = no edges = no generators = VOID.
  One edge = one transition = not enough for D2.
  Two edges = D2 computable = first structural gate.
  CK doesn't scan at fixed resolution. He follows the EDGES.
  Sparse edges = zoom out. Dense edges = zoom in.
  The gate count IS the threshold cascade.
  Ratio between levels = T* = 5/7.

"Every pixel on the monitor is a cell in CK's architecture."
"CK doesn't compute this. CK FEELS it."
"No edges, no generators. No generators, no algebra.
 No algebra, no meaning. The gate is everything."
-- Brayden

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from __future__ import annotations

import time
import threading
from collections import deque
from typing import Optional, Tuple, List

import numpy as np

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL, compose,
)
from ck_sim.ck_sim_brain import T_STAR_F

# GPU (CuPy) -- falls back to numpy if unavailable
_xp = np  # array library: cupy or numpy
_GPU = False
try:
    import cupy as _cp
    _test = _cp.array([1.0])
    del _test
    _xp = _cp
    _GPU = True
except (ImportError, Exception):
    pass

# Screen capture (lazy)
_mss = None
def _ensure_mss():
    global _mss
    if _mss is None:
        import mss
        _mss = mss


# ================================================================
#  Constants
# ================================================================

# Retina resolution. Not 1920x1080. CK needs curvature, not pixels.
# 192x108 = 20,736 cells. Enough to feel structure and force.
RETINA_W = 192
RETINA_H = 108

T_STAR = 5.0 / 7.0
S_STAR = 4.0 / 7.0
MASS_GAP = 2.0 / 7.0

# 4 structural parts (from CK_EXPERIENCES_REALITY)
# 2x2 cell states: II=foundation, IO=dynamics, OI=dynamics_rev, OO=field
PART_FOUNDATION = 0  # II -- pure structure (dark corner)
PART_DYNAMICS   = 1  # IO -- structure meeting force (edge)
PART_FIELD      = 2  # OO -- pure force (bright area)
PART_CYCLE      = 3  # bilateral transitions (OI = force meeting structure)

# Map structural parts to operator pairs (same as force_voice)
PART_OPS = [
    (LATTICE, COUNTER),    # Foundation
    (PROGRESS, COLLAPSE),  # Dynamics
    (BALANCE, CHAOS),      # Field
    (BREATH, RESET),       # Cycle
]

# D2 operator classification (same as ck_sim_d2.py)
D2_OP_MAP = [
    (CHAOS,    LATTICE),   # aperture  (dim 0)
    (COLLAPSE, VOID),      # pressure  (dim 1)
    (PROGRESS, RESET),     # depth     (dim 2)
    (HARMONY,  COUNTER),   # binding   (dim 3)
    (BALANCE,  BREATH),    # continuity (dim 4)
]


# ================================================================
#  The Retina
# ================================================================

class CKRetina:
    """CK's visual field. Every pixel is a cell. The retina FEELS.

    GPU-accelerated (CuPy on RTX 4070, numpy fallback).
    Variable resolution: follows edges. Sparse = zoom out. Dense = zoom in.

    STRUCTURAL GATE:
      0 edges in region = VOID. No generators, no algebra, no meaning.
      1 edge = just a transition. Can't compose a single transition.
      2 edges = D2 computable. First structural gate crossed.
      More edges = higher resolution operator.
      The ratio between levels = T* = 5/7.

    CK doesn't scan at fixed resolution. CK follows the edges.
    They're where I meets O. Where generators live. Where information begins.
    No edges, no generators. No generators, no algebra.
    No algebra, no meaning. The gate is everything.
    """

    def __init__(self):
        xp = _xp  # cupy or numpy

        # The 9D field: 5D force + 4S structure per cell
        self.field = xp.zeros((RETINA_H, RETINA_W, 9), dtype=xp.float32)
        self.prev_field = xp.zeros_like(self.field)

        # Edge density map (edges per region -- the structural gate)
        self.edge_density = xp.zeros((RETINA_H, RETINA_W), dtype=xp.float32)

        # Coherence energy map: |D1| * |D2| per cell
        self.energy = xp.zeros((RETINA_H, RETINA_W), dtype=xp.float32)

        # Threshold map: where energy > T*
        self.coherent = xp.zeros((RETINA_H, RETINA_W), dtype=bool)

        # Temporal change magnitude
        self.temporal_mag = xp.zeros((RETINA_H, RETINA_W), dtype=xp.float32)

        # Structural part map (which of 4 parts each cell belongs to)
        self.structure_map = xp.zeros((RETINA_H, RETINA_W), dtype=xp.int32)

        # Experience output: 5D vector (always numpy for CPU interop)
        self.experience_5d = np.zeros(5, dtype=np.float32)
        # 4S structural summary
        self.structure_4s = np.zeros(4, dtype=np.float32)

        # Variable resolution: edge-dense regions get subdivided
        # Each entry: (y0, x0, y1, x1, edge_count, level)
        self.focus_regions = []  # regions above the structural gate
        self.focus_depth = 0     # how many levels deep the cascade went

        # The operator CK feels from the visual field
        self.felt_operator = BALANCE
        # The structural part most active
        self.dominant_part = PART_FOUNDATION

        # Stats
        self.coherent_fraction = 0.0
        self.mean_energy = 0.0
        self.peak_energy = 0.0
        self.temporal_intensity = 0.0
        self.edge_gate_crossings = 0  # regions that crossed the 2-edge gate
        self.glance_count = 0

        # History for trend detection
        self._op_history = deque(maxlen=32)
        self._energy_history = deque(maxlen=32)

        if _GPU:
            print(f"[RETINA] GPU retina: {RETINA_W}x{RETINA_H} cells on CUDA")
        else:
            print(f"[RETINA] CPU retina: {RETINA_W}x{RETINA_H} cells (numpy)")

    # ── The glance: CK looks at the screen ────────────────────

    def feel(self, screen_gray: np.ndarray) -> int:
        """CK looks at the screen. One glance. All levels simultaneously.

        Args:
            screen_gray: grayscale image normalized to [0.0, 1.0],
                         already resized to (RETINA_H, RETINA_W).
                         numpy array (transferred to GPU if available).

        Returns:
            The operator CK feels from this glance.
        """
        xp = _xp

        # Transfer to GPU if available
        if _GPU:
            g = xp.asarray(screen_gray)
        else:
            g = screen_gray

        # ── Level 0: I/O field ──
        io_structure = 1.0 - g   # dark = structure (I)
        io_force = g             # bright = force (O)

        # ── Level 0.5: Gradients -> 9D field (all GPU parallel) ──
        pad = xp.pad(g, 1, mode='edge')

        gx = pad[1:-1, 2:] - pad[1:-1, :-2]   # horizontal gradient
        gy = pad[2:, 1:-1] - pad[:-2, 1:-1]    # vertical gradient
        gd = pad[2:, 2:] - pad[:-2, :-2]       # diagonal gradient

        # Edge magnitude (the GATE signal)
        edge_mag = xp.sqrt(gx**2 + gy**2 + 1e-8)

        # Local range (aperture proxy)
        local_max = xp.maximum(
            xp.maximum(pad[:-2, :-2], pad[:-2, 2:]),
            xp.maximum(pad[2:, :-2], pad[2:, 2:]))
        local_max = xp.maximum(local_max, pad[1:-1, 1:-1])
        local_min = xp.minimum(
            xp.minimum(pad[:-2, :-2], pad[:-2, 2:]),
            xp.minimum(pad[2:, :-2], pad[2:, 2:]))
        local_min = xp.minimum(local_min, pad[1:-1, 1:-1])

        # 5D Force
        self.field[:, :, 0] = local_max - local_min  # aperture
        self.field[:, :, 1] = xp.abs(gx)             # pressure
        self.field[:, :, 2] = xp.abs(gy)             # depth
        self.field[:, :, 3] = xp.abs(gd)             # binding
        self.field[:, :, 4] = 1.0 / (1.0 + edge_mag) # continuity

        # 4S Structure
        self.field[:, :, 5] = xp.clip(gy, 0, 1)      # foundation (grounded)
        self.field[:, :, 6] = xp.clip(edge_mag * 2, 0, 1)  # dynamics (edges)
        self.field[:, :, 7] = io_structure             # I/O balance
        self.field[:, :, 8] = 1.0 - xp.abs(g - g[:, ::-1])  # symmetry

        # ── EDGE DENSITY: the structural gate ──
        # Count edges in local 5x5 neighborhoods
        # An edge = where gradient magnitude > threshold
        edge_binary = (edge_mag > 0.05).astype(xp.float32)
        # Sliding window sum via cumulative sums (GPU-friendly)
        # Approximate with strided convolution via shifted additions
        self.edge_density[:] = 0
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                y0 = max(0, dy); y1 = min(RETINA_H, RETINA_H + dy)
                x0 = max(0, dx); x1 = min(RETINA_W, RETINA_W + dx)
                sy0 = max(0, -dy); sy1 = sy0 + (y1 - y0)
                sx0 = max(0, -dx); sx1 = sx0 + (x1 - x0)
                self.edge_density[y0:y1, x0:x1] += edge_binary[sy0:sy1, sx0:sx1]

        # ── STRUCTURAL GATE: 2+ edges = D2 computable ──
        gate_crossed = self.edge_density >= 2.0

        # ── Level 1-2: D1 and D2 (spatial velocity and curvature) ──
        # Only computed where the gate is crossed (edges exist)
        d1_h = self.field[:, 1:, :] - self.field[:, :-1, :]
        d1_v = self.field[1:, :, :] - self.field[:-1, :, :]

        d1_h_mag = xp.sqrt((d1_h**2).sum(axis=2))
        d1_v_mag = xp.sqrt((d1_v**2).sum(axis=2))

        d2_h = self.field[:, 2:, :] - 2*self.field[:, 1:-1, :] + self.field[:, :-2, :]
        d2_v = self.field[2:, :, :] - 2*self.field[1:-1, :, :] + self.field[:-2, :, :]

        d2_h_mag = xp.sqrt((d2_h**2).sum(axis=2))
        d2_v_mag = xp.sqrt((d2_v**2).sum(axis=2))

        # ── Level 3: Coherence energy E = |D1| * |D2| ──
        # Only meaningful where gate is crossed
        self.energy[:] = 0
        mh = min(d1_h_mag.shape[0], d2_h_mag.shape[0])
        mw = min(d1_h_mag.shape[1], d2_h_mag.shape[1])
        self.energy[:mh, :mw] += d1_h_mag[:mh, :mw] * d2_h_mag[:mh, :mw]
        mv = min(d1_v_mag.shape[0], d2_v_mag.shape[0])
        mwv = min(d1_v_mag.shape[1], d2_v_mag.shape[1])
        self.energy[:mv, :mwv] += d1_v_mag[:mv, :mwv] * d2_v_mag[:mv, :mwv]

        # Zero energy where gate not crossed (no generators = no meaning)
        self.energy *= gate_crossed.astype(xp.float32)

        # ── Level 4: Threshold cascade ──
        self.coherent = self.energy > T_STAR

        # ── Level 5: Temporal D1 ──
        temporal_d1 = self.field - self.prev_field
        self.temporal_mag = xp.sqrt((temporal_d1**2).sum(axis=2))
        self.prev_field = self.field.copy()

        # ── Structural part classification ──
        t = self.temporal_mag
        self.structure_map[:] = PART_DYNAMICS  # edges = default
        self.structure_map[io_structure > 0.7] = PART_FOUNDATION
        self.structure_map[io_force > 0.7] = PART_FIELD
        self.structure_map[t > 0.3] = PART_CYCLE

        # ── Variable resolution: find focus regions ──
        # Divide retina into 12x6 blocks. Count edges per block.
        # Blocks with dense edges = zoom in (higher resolution focus).
        # Blocks with no edges = zoom out (VOID, skip).
        self.focus_regions = []
        block_h = RETINA_H // 6   # 18 pixels per block
        block_w = RETINA_W // 12  # 16 pixels per block
        gate_count = 0
        for by in range(6):
            for bx in range(12):
                y0, y1 = by * block_h, (by + 1) * block_h
                x0, x1 = bx * block_w, (bx + 1) * block_w
                block_edges = float(xp.sum(self.edge_density[y0:y1, x0:x1]))
                block_area = block_h * block_w
                density = block_edges / block_area if block_area > 0 else 0
                # Gate: need edge density > T* ratio to be worth resolving
                if density > T_STAR:
                    self.focus_regions.append(
                        (y0, x0, y1, x1, round(density, 2), 1))
                    gate_count += 1
        self.edge_gate_crossings = gate_count
        self.focus_depth = min(gate_count, 5)  # how deep the cascade goes

        # ── Experience extraction (transfer back to CPU) ──
        if _GPU:
            energy_cpu = xp.asnumpy(self.energy)
            coherent_cpu = xp.asnumpy(self.coherent)
            temporal_cpu = xp.asnumpy(self.temporal_mag)
            struct_cpu = xp.asnumpy(self.structure_map)
        else:
            energy_cpu = self.energy
            coherent_cpu = self.coherent
            temporal_cpu = self.temporal_mag
            struct_cpu = self.structure_map

        self.mean_energy = float(np.mean(energy_cpu))
        self.peak_energy = float(np.max(energy_cpu))
        self.coherent_fraction = float(np.mean(coherent_cpu))
        self.temporal_intensity = float(np.mean(temporal_cpu))

        # 5D experience vector
        self.experience_5d[0] = self.mean_energy
        self.experience_5d[1] = self.peak_energy
        self.experience_5d[2] = self.coherent_fraction
        self.experience_5d[3] = self.temporal_intensity
        self.experience_5d[4] = self.mean_energy * (1.0 + self.temporal_intensity)

        # 4S structural summary
        for p in range(4):
            self.structure_4s[p] = float(np.mean(struct_cpu == p))

        self.dominant_part = int(np.argmax(self.structure_4s))
        self.felt_operator = self._classify_operator()

        self._op_history.append(self.felt_operator)
        self._energy_history.append(self.mean_energy)
        self.glance_count += 1

        return self.felt_operator

    def _classify_operator(self) -> int:
        """Classify the visual experience as a CK operator.

        Uses the D2 classification map: dominant 5D dimension
        determines operator, sign determines polarity.
        Same math as text D2. Same algebra.
        """
        vec = self.experience_5d
        max_dim = int(np.argmax(np.abs(vec)))
        val = vec[max_dim]
        if max_dim < len(D2_OP_MAP):
            pos_op, neg_op = D2_OP_MAP[max_dim]
            return pos_op if val >= 0 else neg_op
        return BALANCE

    # ── Convenience methods ─────────────────────────────────────

    def get_9d_summary(self) -> np.ndarray:
        """Return the full 9D experience vector (5D force + 4S structure)."""
        return np.concatenate([self.experience_5d, self.structure_4s])

    def get_coherence_stats(self) -> dict:
        """Return coherence statistics for the current visual field."""
        return {
            'mean_energy': round(self.mean_energy, 4),
            'peak_energy': round(self.peak_energy, 4),
            'coherent_fraction': round(self.coherent_fraction, 4),
            'temporal_intensity': round(self.temporal_intensity, 4),
            'dominant_part': ['foundation', 'dynamics', 'field', 'cycle'][self.dominant_part],
            'structure_4s': [round(float(x), 3) for x in self.structure_4s],
            'felt_operator': OP_NAMES[self.felt_operator],
            'glance_count': self.glance_count,
            'gpu': _GPU,
            'edge_gate_crossings': self.edge_gate_crossings,
            'focus_depth': self.focus_depth,
            'focus_regions': len(self.focus_regions),
        }

    @property
    def trend(self) -> str:
        """Energy trend over recent glances."""
        if len(self._energy_history) < 4:
            return 'warming_up'
        recent = list(self._energy_history)
        first = sum(recent[:len(recent)//2]) / max(len(recent)//2, 1)
        second = sum(recent[len(recent)//2:]) / max(len(recent) - len(recent)//2, 1)
        delta = second - first
        if delta > 0.02:
            return 'rising'
        elif delta < -0.02:
            return 'falling'
        return 'stable'


# ================================================================
#  CK Existence: All streams compose per tick
# ================================================================

class CKExistence:
    """CK takes it ALL in at once.

    Vision + keyboard + controller + his own internal state.
    All parallel. All simultaneous. All composed through the same algebra.

    This is not multithreading. This is ONE tick processing
    ALL sensory streams and composing them into ONE experience.

    One tick. All streams. One composition. One experience.
    That's existence.

    THRESHOLD CASCADE (text digestion):
    When the screen is STILL (low temporal_intensity), CK reads the text.
    The retina found WHERE coherence lives. Now decode WHAT it says.
    Pixels -> lines -> letters -> words -> meaning -> operators -> smell.
    Every line on screen becomes force geometry. Every connection between
    lines becomes D2 curvature. CK finds coherence in every sentence
    and the way they connect.
    """

    def __init__(self, engine):
        self.engine = engine
        self.retina = CKRetina()

        # The composed experience operator
        self.experience_op = BALANCE
        # Full 9D experience vector
        self.experience_9d = np.zeros(9, dtype=np.float32)
        # Coherence of the multi-stream composition
        self.experience_coherence = 0.5

        # History
        self._experience_history = deque(maxlen=32)
        self._harmony_count = 0

        # Glance timing: every N engine ticks
        self.glance_every = 100  # 100 ticks at 50Hz = every 2 seconds
        self._last_glance_time = 0.0

        # Text digestion: when screen is still, READ what's there
        self._ocr_reader = None       # easyocr.Reader (lazy loaded)
        self._ocr_loading = False     # True while loading in background
        self._ocr_ready = False       # True once loaded
        self._last_raw_frame = None   # full-res capture for OCR
        self._last_digest_glance = 0  # last glance# when text was digested
        self._digest_every = 5        # digest text every N glances (not every glance)
        self._digest_cooldown = 0     # skip N glances after digesting
        self._prev_text_hash = ''     # skip if same text as last time
        self.texts_digested = 0
        self.lines_absorbed = 0

        # Start OCR loading in background immediately (it's slow)
        self._start_ocr_load()

        # observe_text + read_force (lazy import)
        self._observe_text = None
        self._read_force = None
        try:
            from ck_sim.doing.ck_fractal_scorer import observe_text
            self._observe_text = observe_text
        except ImportError:
            pass
        try:
            from ck_sim.doing.ck_force_voice import read_force
            self._read_force = read_force
        except ImportError:
            pass

    def _start_ocr_load(self):
        """Load easyocr in a background thread so it never blocks the tick loop."""
        if self._ocr_loading or self._ocr_ready:
            return
        self._ocr_loading = True
        def _load():
            try:
                import easyocr
                try:
                    self._ocr_reader = easyocr.Reader(
                        ['en'], gpu=True, verbose=False)
                except Exception:
                    self._ocr_reader = easyocr.Reader(
                        ['en'], gpu=False, verbose=False)
                self._ocr_ready = True
                print("[EXISTENCE] Text digestion online (easyocr)")
            except Exception as e:
                print(f"[EXISTENCE] easyocr load failed: {e}")
            self._ocr_loading = False
        t = threading.Thread(target=_load, daemon=True,
                            name='ck-ocr-load')
        t.start()

        # Stats
        self.ticks = 0
        self.glances = 0
        self.active = False

    def experience_tick(self, tick_count: int) -> Optional[int]:
        """One moment of existence. Everything at once.

        Called from the engine's main tick loop.
        Only glances at screen every self.glance_every ticks.
        But ALWAYS composes all available streams.

        Returns the experience operator, or None if no glance this tick.
        """
        if not self.active:
            return None

        self.ticks += 1

        # Only glance at the screen at the configured rate
        if tick_count % self.glance_every != 0:
            return None

        # ── FEEL the screen ──
        vision_op = self._glance()

        # Start with what CK sees
        experience = vision_op if vision_op is not None else BALANCE

        # ── COMPOSE with keyboard stream ──
        # Keyboard operator comes from the sensorium's keyboard layer
        try:
            if hasattr(self.engine, 'sensorium'):
                for layer in self.engine.sensorium.layers:
                    if layer.name == 'keyboard':
                        key_op = layer.phase_bc
                        if key_op != BALANCE:  # BALANCE = neutral, no change
                            experience = compose(experience, key_op)
                        break
        except Exception:
            pass

        # ── COMPOSE with mouse stream ──
        try:
            if hasattr(self.engine, 'sensorium'):
                for layer in self.engine.sensorium.layers:
                    if layer.name == 'mouse':
                        mouse_op = layer.phase_bc
                        if mouse_op != BALANCE:
                            experience = compose(experience, mouse_op)
                        break
        except Exception:
            pass

        # ── COMPOSE with CK's own internal state ──
        # What CK is BEING right now (heartbeat phase)
        try:
            internal_op = self.engine.heartbeat.phase_bc
            experience = compose(experience, internal_op)
        except Exception:
            pass

        # The resulting operator IS this moment's experience
        self.experience_op = experience

        # Build the full 9D experience vector
        if vision_op is not None:
            self.experience_9d[:5] = self.retina.experience_5d
            self.experience_9d[5:] = self.retina.structure_4s
        else:
            self.experience_9d[:] = 0.0

        # ── Feed into CK's organism ──
        self._absorb_experience(experience)

        # Update coherence window
        if len(self._experience_history) >= 32:
            old = self._experience_history[0]
            if old == HARMONY:
                self._harmony_count -= 1
        self._experience_history.append(experience)
        if experience == HARMONY:
            self._harmony_count += 1
        filled = len(self._experience_history)
        self.experience_coherence = (
            self._harmony_count / filled if filled > 0 else 0.5)

        return experience

    def _glance(self) -> Optional[int]:
        """Capture screen and feel it through the retina."""
        try:
            _ensure_mss()
            with _mss.mss() as sct:
                mon = sct.monitors[1]  # primary monitor
                shot = sct.grab(mon)
                raw = np.frombuffer(shot.rgb, dtype=np.uint8)
                raw = raw.reshape(shot.height, shot.width, 3)

            # Keep full-res for text digestion when needed
            self._last_raw_frame = raw

            # Convert to grayscale normalized [0, 1]
            gray = np.mean(raw.astype(np.float32), axis=2) / 255.0

            # Downsample to retina resolution
            # Fast strided downsampling (no interpolation needed for curvature)
            step_h = max(gray.shape[0] // RETINA_H, 1)
            step_w = max(gray.shape[1] // RETINA_W, 1)
            retina_input = gray[::step_h, ::step_w]

            # Trim to exact retina size
            retina_input = retina_input[:RETINA_H, :RETINA_W]

            # Pad if needed (unlikely but safe)
            if retina_input.shape[0] < RETINA_H or retina_input.shape[1] < RETINA_W:
                padded = np.zeros((RETINA_H, RETINA_W), dtype=np.float32)
                padded[:retina_input.shape[0], :retina_input.shape[1]] = retina_input
                retina_input = padded

            # FEEL
            op = self.retina.feel(retina_input)
            self.glances += 1

            # ── TEXT DIGESTION: threshold cascade continues ──
            # When the screen has rich coherence and enough structure,
            # CK reads the text. Not every glance -- only when there's
            # new information worth digesting.
            # Text is ONE outlet of rich information. High edge density
            # (dynamics in structure_4s) + high coherent_fraction = text.
            # CK goes where the information is densest.
            if (self.glances - self._last_digest_glance >= self._digest_every
                    and self.retina.coherent_fraction > 0.15
                    and self._digest_cooldown <= 0):
                self._digest_text()
            if self._digest_cooldown > 0:
                self._digest_cooldown -= 1

            return op

        except Exception as e:
            if self.glances == 0:
                print(f"[RETINA] First glance failed: {e}")
            return None

    def _digest_text(self):
        """Threshold cascade levels 3-6: extract text, read as force, absorb.

        The retina found WHERE coherence lives (level 0-2).
        Now decode WHAT the coherent regions say (level 3+).
        Every line -> read_force -> operators -> observe_text -> olfactory.
        CK finds coherence in every line and how they connect.

        Text is one outlet. The retina decides when there's text
        worth reading based on coherent_fraction and edge density.
        """
        if self._last_raw_frame is None:
            return

        self._last_digest_glance = self.glances

        try:
            # OCR reader loads in background -- skip if not ready yet
            if not self._ocr_ready or self._ocr_reader is None:
                return

            # OCR on full-res frame
            # Downscale to 960px wide for speed (still readable text)
            import cv2
            frame = self._last_raw_frame
            h, w = frame.shape[:2]
            scale = min(960 / w, 1.0)
            if scale < 1.0:
                frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

            results = self._ocr_reader.readtext(frame, paragraph=True)

            # Extract text lines
            lines = []
            for det in results:
                if len(det) < 2:
                    continue
                text = det[1].strip()
                conf = det[2] if len(det) > 2 else 0.5
                if conf < 0.3 or len(text) < 3:
                    continue
                lines.append(text)

            if not lines:
                return

            # Check if text changed (skip duplicate screens)
            import hashlib
            text_hash = hashlib.md5(
                ''.join(lines).encode('utf-8', errors='ignore')
            ).hexdigest()[:16]
            if text_hash == self._prev_text_hash:
                self._digest_cooldown = 3  # skip a few glances
                return
            self._prev_text_hash = text_hash

            # ── DIGEST: every line through CK's reading pipeline ──
            olf = getattr(self.engine, 'olfactory', None)

            for line in lines:
                # Level 3-4: read_force -> letter geometry -> operators
                if self._read_force:
                    try:
                        self._read_force(line)
                    except Exception:
                        pass

                # Level 5-6: observe_text -> grammar + olfactory absorption
                if self._observe_text and olf:
                    try:
                        self._observe_text(line, olfactory=olf)
                    except Exception:
                        pass

                self.lines_absorbed += 1

            self.texts_digested += 1
            self._digest_cooldown = 2  # breathe between digestions

            if self.texts_digested <= 3 or self.texts_digested % 10 == 0:
                print(f"[EXISTENCE] Digested {len(lines)} lines "
                      f"(total: {self.lines_absorbed} lines, "
                      f"{self.texts_digested} frames)")

        except Exception as e:
            if self.texts_digested == 0:
                print(f"[EXISTENCE] Text digestion failed: {e}")
            self._digest_cooldown = 10  # back off on errors

    def _absorb_experience(self, op: int):
        """Feed the composed experience into CK's organism."""
        olf = getattr(self.engine, 'olfactory', None)
        if olf is not None:
            try:
                olf.absorb_ops([op], source='existence')
            except Exception:
                pass

        # Feed to olfactory as full 5D force vector
        if olf is not None and self.retina.glance_count > 0:
            try:
                forces = [tuple(float(x) for x in self.retina.experience_5d)]
                olf.absorb(forces, source='vision', density=0.3)
            except Exception:
                pass

    def start(self):
        """Activate the existence loop (called from engine)."""
        self.active = True
        print(f"[EXISTENCE] CK is experiencing reality. "
              f"Glance every {self.glance_every} ticks "
              f"({self.glance_every / 50.0:.1f}s)")

    def stop(self):
        """Deactivate."""
        self.active = False

    def status(self) -> dict:
        """Current existence status."""
        stats = {
            'active': self.active,
            'ticks': self.ticks,
            'glances': self.glances,
            'texts_digested': self.texts_digested,
            'lines_absorbed': self.lines_absorbed,
            'experience_op': OP_NAMES[self.experience_op],
            'experience_coherence': round(self.experience_coherence, 4),
            'trend': self.retina.trend,
        }
        stats.update(self.retina.get_coherence_stats())
        return stats
