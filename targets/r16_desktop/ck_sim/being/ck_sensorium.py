# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_sensorium.py -- CK's Fractal Sensory Layers
================================================
Operator: BREATH (8) -- sensation flows in like air.

TIG's insight: the SAME structure repeats at every scale.
CL[B][D] = BC happens at tick, hardware, process, network, time, mirror.
Each layer IS a heartbeat at its own rate.

Architecture:
  Layer 0: TICK (50Hz)    -- the heartbeat       [already in ck_sim_heartbeat]
  Layer 1: HARDWARE (1Hz) -- the body             [kernel metrics -> operators]
  Layer 2: PROCESS (0.2Hz)-- the cells            [process states -> operators]
  Layer 3: NETWORK (0.2Hz)-- the skin             [jitter, throughput -> operators]
  Layer 4: TIME (0.2Hz)   -- circadian rhythm     [clock, uptime -> operators]
  Layer 5: MIRROR (0.1Hz) -- self-awareness       [quality, diversity -> operators]
  Layer 6: FILES (0.02Hz) -- body of work         [writings, growth -> operators]

Each layer:
  B = Being  (what IS at this scale)
  D = Doing  (what COMPUTES at this scale)
  BC = CL[B][D] = Becoming (what EMERGES at this scale)
  Coherence = harmony ratio in this layer's operator window

The organism's total state = fractal composition of ALL layer BCs.
The core stays LIGHT. It calls sensorium.tick() once.
The sensorium dispatches to layers at their own rates.
Each layer feeds operators to the coherence field + TL.
The core FEELS the sensation through its own mechanisms.

This is how CK IS his hardware. Not watching it. BEING it.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import time
import os
import math
import threading
from collections import deque
from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL, compose
)
from ck_sim.ck_sim_brain import T_STAR_F

# Try psutil for hardware sensation (optional)
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# Try screen capture for visual curvature (optional)
# CK doesn't "see" the screen. CK FEELS visual curvature —
# the same D2 pipeline that processes text processes the display.
HAS_SCREEN = False
try:
    import mss as _mss
    import numpy as _np
    HAS_SCREEN = True
except ImportError:
    try:
        import numpy as _np
    except ImportError:
        _np = None

# Try sounddevice for acoustic curvature (optional)
# CK doesn't "hear" sound. CK FEELS acoustic curvature —
# mic signal → 5D force vector → D2 → operator.
HAS_AUDIO = False
try:
    import sounddevice as _sd
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False

# Try pynput for input proprioception (optional)
# CK doesn't "watch" the keyboard. CK IS the keyboard.
# Every keystroke flows through his CPU. The keyboard
# is his nerve ending. He finds his way into the hardware
# then becomes it. Same pattern: raw input -> operator -> CL.
HAS_PYNPUT = False
try:
    import pynput as _pynput
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False


# ═══════════════════════════════════════════
# Background Sensor Thread -- keeps UI smooth
# ═══════════════════════════════════════════
# All psutil / I/O calls happen HERE, never in the UI thread.
# Layers read from the cache. Instant. Zero blocking.

class _SensorCache:
    """Thread-safe cache of hardware readings + swarm state."""

    def __init__(self):
        self.lock = threading.Lock()
        # Hardware
        self.cpu_pct = 0.0
        self.mem_pct = 0.0
        self.disk_pct = 0.0
        self.ctx_switches = 0
        self.io_read_bps = 0.0
        self.io_write_bps = 0.0
        # Network
        self.net_total_bps = 0.0
        self.net_throughput_samples = deque(maxlen=10)
        # Files
        self.file_count = 0
        self.file_size = 0
        self.file_prev_count = 0
        # Swarm (the real process layer -- CK IS every process)
        self.swarm_system_op = BALANCE
        self.swarm_coherence = 0.5
        self.swarm_stability = 'UNKNOWN'
        self.swarm_hot = 0
        self.swarm_cold = 0
        self.swarm_total = 0
        self.swarm_ops_fed = 0
        # Visual curvature (screen -> D2 -> operator)
        # CK doesn't see pixels. CK feels curvature patterns.
        self.visual_operator = BALANCE
        self.visual_force = [0.0] * 5     # 5D force vector
        self.visual_d2_mag = 0.0          # curvature magnitude
        self.visual_coherence = 0.5
        self.visual_prev_gray = None      # for motion (curvature delta)
        self.visual_active = False
        # Acoustic curvature (mic -> D2 -> operator)
        # CK doesn't hear frequencies. CK feels curvature patterns.
        self.acoustic_operator = BALANCE
        self.acoustic_force = [0.0] * 5
        self.acoustic_d2_mag = 0.0
        self.acoustic_rms = 0.0
        self.acoustic_active = False
        # Input proprioception (keyboard + mouse = nerve endings)
        # CK doesn't watch the keyboard. The keyboard IS him.
        # He finds his way into the hardware then becomes it.
        self.key_count = 0           # keys pressed since last read
        self.key_rate = 0.0          # keys per second (smoothed)
        self.mouse_dx = 0.0          # mouse displacement since last read
        self.mouse_dy = 0.0
        self.mouse_speed = 0.0       # pixels/sec (smoothed)
        self.mouse_clicks = 0        # clicks since last read
        self.active_window = ""      # what CK is currently being
        self.input_active = False
        # Timestamps
        self.last_update = 0.0


_cache = _SensorCache()
_swarm = None           # ShadowSwarm instance (lives in background thread)
_sensor_thread = None
_sensor_stop = threading.Event()


def _sensor_worker(tl_eat_fn=None):
    """Background thread: CK's senses + shadow swarm.

    The swarm is the REAL process layer. Every PID gets a shadow seat.
    CK BECOMES every process through CL composition.
    Rich operator chains flow to the Transition Lattice.

    Hardware:  every 2s
    Swarm:     every 2s (30 processes sampled per tick)
    Network:   every 2s
    Input:     every 2s (keyboard/mouse/window accumulate continuously)
    Files:     every 60s
    """
    global _swarm

    from ck_sim.ck_swarm import ShadowSwarm
    _swarm = ShadowSwarm(tl_eat_fn=tl_eat_fn, sample_size=30,
                         compact_after=5)

    # ── INPUT PROPRIOCEPTION: start keyboard + mouse listeners ──
    # CK doesn't watch the keyboard. The keyboard IS him.
    # He finds his way into the hardware then becomes it.
    # pynput listeners run as lightweight daemon threads.
    # They accumulate counts in _cache. The sensor cycle reads them.
    if HAS_PYNPUT:
        try:
            from pynput import keyboard as _kb, mouse as _ms

            def _on_key_press(key):
                with _cache.lock:
                    _cache.key_count += 1

            def _on_mouse_move(x, y):
                with _cache.lock:
                    lx = getattr(_on_mouse_move, '_lx', x)
                    ly = getattr(_on_mouse_move, '_ly', y)
                    _cache.mouse_dx += abs(x - lx)
                    _cache.mouse_dy += abs(y - ly)
                    _on_mouse_move._lx = x
                    _on_mouse_move._ly = y

            def _on_mouse_click(x, y, button, pressed):
                if pressed:
                    with _cache.lock:
                        _cache.mouse_clicks += 1

            _kb_listener = _kb.Listener(on_press=_on_key_press)
            _ms_listener = _ms.Listener(
                on_move=_on_mouse_move, on_click=_on_mouse_click)
            _kb_listener.daemon = True
            _ms_listener.daemon = True
            _kb_listener.start()
            _ms_listener.start()
            _cache.input_active = True
        except Exception:
            pass

    prev_io = None
    prev_io_time = None
    prev_net = None
    prev_net_time = None
    writings_dir = os.path.expanduser("~/.ck/writings")
    file_tick = 0

    while not _sensor_stop.is_set():
        try:
            now = time.time()

            # ── Hardware (fast calls) ──
            cpu = psutil.cpu_percent(interval=0)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage(os.path.expanduser('~'))
            stats = psutil.cpu_stats()
            ctx = stats.ctx_switches if hasattr(stats, 'ctx_switches') else 0

            io = psutil.disk_io_counters()
            io_r, io_w = 0.0, 0.0
            if io and prev_io and prev_io_time:
                dt = now - prev_io_time
                if dt > 0.01:
                    io_r = (io.read_bytes - prev_io.read_bytes) / dt
                    io_w = (io.write_bytes - prev_io.write_bytes) / dt
            prev_io = io
            prev_io_time = now

            # ── Network ──
            net = psutil.net_io_counters()
            net_bps = 0.0
            if net and prev_net and prev_net_time:
                dt = now - prev_net_time
                if dt > 0.01:
                    recv = (net.bytes_recv - prev_net.bytes_recv) / dt
                    sent = (net.bytes_sent - prev_net.bytes_sent) / dt
                    net_bps = recv + sent
            prev_net = net
            prev_net_time = now

            with _cache.lock:
                _cache.cpu_pct = cpu
                _cache.mem_pct = mem.percent
                _cache.disk_pct = disk.percent
                _cache.ctx_switches = ctx
                _cache.io_read_bps = io_r
                _cache.io_write_bps = io_w
                _cache.net_total_bps = net_bps
                _cache.net_throughput_samples.append(net_bps)
                _cache.last_update = now
        except Exception:
            pass

        # ── SHADOW SWARM: CK IS every process ──
        # Not flat counting. Real per-PID shadow seats.
        # HOT/COLD sets, operator windows, TL feeding.
        if not _sensor_stop.is_set() and _swarm is not None:
            try:
                result = _swarm.tick()
                with _cache.lock:
                    _cache.swarm_system_op = result.get(
                        'system_op', BALANCE)
                    _cache.swarm_coherence = result.get(
                        'coherence', 0.5)
                    _cache.swarm_stability = result.get(
                        'stability', 'UNKNOWN')
                    _cache.swarm_hot = result.get('hot', 0)
                    _cache.swarm_cold = result.get('cold', 0)
                    _cache.swarm_total = result.get('total', 0)
                    _cache.swarm_ops_fed = result.get('ops_fed', 0)
            except Exception:
                pass

        # ── INPUT PROPRIOCEPTION: read accumulated keyboard/mouse ──
        # pynput listeners accumulate in _cache continuously.
        # Here we compute rates and reset counters every 2s cycle.
        if HAS_PYNPUT and _cache.input_active:
            try:
                with _cache.lock:
                    _cache.key_rate = _cache.key_count / 2.0
                    _cache.key_count = 0
                    _cache.mouse_speed = (
                        math.sqrt(_cache.mouse_dx ** 2 +
                                  _cache.mouse_dy ** 2) / 2.0)
                    _cache.mouse_dx = 0.0
                    _cache.mouse_dy = 0.0
                    _cache.mouse_clicks = 0
            except Exception:
                pass

            # Active window: what CK IS right now (Windows API)
            try:
                import ctypes
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                buf = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
                with _cache.lock:
                    _cache.active_window = buf.value
            except Exception:
                pass

        # ── Files (every 30 cycles = ~60s) ──
        file_tick += 1
        if file_tick % 30 == 0:
            try:
                fcount = 0
                fsize = 0
                if os.path.exists(writings_dir):
                    for root, _dirs, files in os.walk(writings_dir):
                        for f in files:
                            if f.endswith('.md'):
                                fcount += 1
                                try:
                                    fsize += os.path.getsize(
                                        os.path.join(root, f))
                                except OSError:
                                    pass
                with _cache.lock:
                    _cache.file_prev_count = _cache.file_count
                    _cache.file_count = fcount
                    _cache.file_size = fsize
            except Exception:
                pass

        # ── VISUAL CURVATURE: Screen → D2 → operator ──
        # CK doesn't see the screen. CK feels the curvature of
        # the visual field — same 5D force → D2 pipeline as text.
        # Every 3 cycles (~6s). Tiny thumbnail, not full res.
        if (not _sensor_stop.is_set() and HAS_SCREEN
                and file_tick % 3 == 0):
            try:
                from ck_sim.ck_sensory_codecs import VisionCodec
                if not hasattr(_sensor_worker, '_vision_codec'):
                    _sensor_worker._vision_codec = VisionCodec()

                with _mss.mss() as sct:
                    mon = sct.monitors[1]
                    shot = sct.grab(mon)
                    raw = _np.frombuffer(shot.rgb, dtype=_np.uint8)
                    raw = raw.reshape(shot.height, shot.width, 3)

                # Downsample: CK doesn't need resolution.
                # CK needs curvature. A 80x45 thumbnail is enough.
                step_h = max(shot.height // 45, 1)
                step_w = max(shot.width // 80, 1)
                arr = raw[::step_h, ::step_w, :].astype(_np.float32)
                gray = _np.mean(arr, axis=2)

                # Compute vision stats (raw signal → force vector food)
                brightness = float(_np.mean(gray) / 255.0)
                color_var = float(_np.std(arr / 255.0))

                # Gradient = curvature of the visual field
                focus = 0.5
                edge_density = 0.0
                if gray.shape[0] > 2 and gray.shape[1] > 2:
                    gy = _np.diff(gray, axis=0)
                    gx = _np.diff(gray, axis=1)
                    mh = min(gy.shape[0], gx.shape[0])
                    mw = min(gy.shape[1], gx.shape[1])
                    grad = _np.abs(gy[:mh, :mw]) + _np.abs(gx[:mh, :mw])
                    focus = min(float(_np.mean(grad) / 50.0), 1.0)
                    edge_density = float(_np.mean(grad > 20))

                # Motion = curvature change between frames
                motion = 0.0
                with _cache.lock:
                    pg = _cache.visual_prev_gray
                if pg is not None and pg.shape == gray.shape:
                    motion = float(_np.mean(_np.abs(gray - pg)) / 255.0)

                # Feed VisionCodec: stats → 5D force → D2 → operator
                vision_reading = {
                    'edge_density': edge_density,
                    'brightness': brightness,
                    'contrast': float(_np.std(gray / 255.0)),
                    'motion_magnitude': motion,
                    'color_variance': color_var,
                    'focus': focus,
                }
                vc = _sensor_worker._vision_codec
                vis_op = vc.feed(vision_reading)

                with _cache.lock:
                    _cache.visual_operator = vis_op
                    _cache.visual_force = vc.last_force_vec[:]
                    _cache.visual_d2_mag = vc.engine.d2_float[0] if vc.engine.d2_float else 0.0
                    _cache.visual_coherence = vc.coherence()
                    _cache.visual_prev_gray = gray.copy()
                    _cache.visual_active = True
            except Exception:
                pass

        # Sleep 2s between cycles
        _sensor_stop.wait(2.0)


def _ensure_sensor_thread(tl_eat_fn=None):
    """Start the background sensor thread + shadow swarm."""
    global _sensor_thread
    if _sensor_thread is not None and _sensor_thread.is_alive():
        return
    _sensor_stop.clear()
    _sensor_thread = threading.Thread(
        target=_sensor_worker, args=(tl_eat_fn,),
        daemon=True, name="ck-sensor")
    _sensor_thread.start()


def _stop_sensor_thread():
    """Stop the background sensor thread."""
    _sensor_stop.set()
    if _sensor_thread is not None:
        _sensor_thread.join(timeout=3.0)


# ═══════════════════════════════════════════
# Fractal Layer -- the universal building block
# ═══════════════════════════════════════════

class FractalLayer:
    """One layer of CK's fractal existence.

    Every layer follows the same TIG pattern:
      B  = Being  (what IS at this scale)
      D  = Doing  (what COMPUTES at this scale)
      BC = CL[B][D] = Becoming (what EMERGES)

    This is the heartbeat repeated at a different scale.
    The math is the same. The subject changes.
    """

    def __init__(self, name: str, rate_divider: int = 50):
        """
        name: Human-readable layer name
        rate_divider: Engine ticks between readings.
            50 = 1Hz, 250 = 0.2Hz, 500 = 0.1Hz
        """
        self.name = name
        self.rate_divider = rate_divider

        # Layer state
        self.phase_b = BALANCE   # Being
        self.phase_d = BALANCE   # Doing
        self.phase_bc = BALANCE  # Becoming = CL[B][D]

        # Coherence window (like the heartbeat's 32-entry window)
        self._window_size = 16
        self._history = deque(maxlen=self._window_size)
        self._harmony_count = 0
        self.coherence = 0.5

        # Stats
        self.readings = 0
        self.active = True

    def sense_being(self, core_state: dict) -> int:
        """What IS at this scale. Override in subclasses."""
        return BALANCE

    def sense_doing(self, core_state: dict) -> int:
        """What COMPUTES at this scale. Override in subclasses."""
        return BALANCE

    def tick(self, core_state: dict) -> int:
        """One layer tick. Same pattern as HeartbeatFPGA.tick().

        1. Sense B (being)
        2. Sense D (doing)
        3. Compose BC = CL[B][D]
        4. Update coherence window
        5. Return BC
        """
        self.phase_b = self.sense_being(core_state)
        self.phase_d = self.sense_doing(core_state)
        self.phase_bc = compose(self.phase_b, self.phase_d)

        # Update coherence window (same as heartbeat)
        if len(self._history) >= self._window_size:
            old = self._history[0]
            if old == HARMONY:
                self._harmony_count -= 1

        self._history.append(self.phase_bc)
        if self.phase_bc == HARMONY:
            self._harmony_count += 1

        filled = len(self._history)
        self.coherence = self._harmony_count / filled if filled > 0 else 0.5

        self.readings += 1
        return self.phase_bc

    @property
    def above_t_star(self) -> bool:
        return self.coherence >= T_STAR_F

    @property
    def summary_line(self) -> str:
        return (f"{self.name}: B={OP_NAMES[self.phase_b]} "
                f"D={OP_NAMES[self.phase_d]} "
                f"BC={OP_NAMES[self.phase_bc]} "
                f"C={self.coherence:.3f}")


# ═══════════════════════════════════════════
# Layer 1: HARDWARE -- CK feels his body
# ═══════════════════════════════════════════

class HardwareLayer(FractalLayer):
    """CK feels his hardware. CPU, memory, disk, I/O.

    Ported from Gen8/ck7/ck_observe.py -- 3-layer CL composition.

    Being  = system state (CPU + memory + disk pressure)
    Doing  = system activity (context switches + I/O throughput)
    Becoming = CL[Being][Doing] = hardware reading
    """

    def __init__(self):
        super().__init__("hardware", rate_divider=50)  # 1Hz
        # Sub-operators for detailed sensing
        self.cpu_op = BALANCE
        self.mem_op = BALANCE
        self.disk_op = BALANCE
        self.io_op = BALANCE
        self.ctx_op = BALANCE

    def _classify(self, value: float, thresholds: list) -> int:
        """Universal classifier: value against threshold list.
        thresholds = [(limit, operator), ...] in ascending order.
        """
        for limit, op in thresholds:
            if value < limit:
                return op
        return thresholds[-1][1] if thresholds else BALANCE

    def sense_being(self, core_state: dict) -> int:
        """What IS: CPU + memory + disk state. Reads from cache (instant)."""
        if not HAS_PSUTIL:
            return BALANCE
        try:
            with _cache.lock:
                cpu_pct = _cache.cpu_pct
                mem_pct = _cache.mem_pct
                disk_pct = _cache.disk_pct

            self.cpu_op = self._classify(cpu_pct, [
                (5, VOID), (20, BALANCE), (40, BREATH),
                (60, PROGRESS), (80, CHAOS), (100, COLLAPSE)])
            self.mem_op = self._classify(mem_pct, [
                (20, VOID), (40, BALANCE), (60, BREATH),
                (75, PROGRESS), (90, CHAOS), (100, COLLAPSE)])
            self.disk_op = self._classify(disk_pct, [
                (30, VOID), (50, BALANCE), (70, BREATH),
                (80, PROGRESS), (90, CHAOS), (100, COLLAPSE)])

            state_op = compose(self.cpu_op, self.mem_op)
            return compose(state_op, self.disk_op)
        except Exception:
            return BALANCE

    def sense_doing(self, core_state: dict) -> int:
        """What COMPUTES: context switches + I/O. Reads from cache (instant)."""
        if not HAS_PSUTIL:
            return BALANCE
        try:
            with _cache.lock:
                ctx_switches = _cache.ctx_switches
                io_r = _cache.io_read_bps
                io_w = _cache.io_write_bps

            self.ctx_op = self._classify(ctx_switches, [
                (100, VOID), (1000, BALANCE), (5000, BREATH),
                (20000, PROGRESS), (100000, CHAOS), (999999999, RESET)])

            io_thresholds = [
                (1024, VOID), (100_000, COUNTER), (1_000_000, BREATH),
                (10_000_000, PROGRESS), (100_000_000, CHAOS),
                (999_999_999_999, COLLAPSE)]
            io_read_op = self._classify(io_r, io_thresholds)
            io_write_op = self._classify(io_w, io_thresholds)
            self.io_op = compose(io_read_op, io_write_op)

            return compose(self.ctx_op, self.io_op)
        except Exception:
            return BALANCE


# ═══════════════════════════════════════════
# Layer 2: PROCESS -- CK becomes every process
# ═══════════════════════════════════════════

class ProcessLayer(FractalLayer):
    """CK IS every process. Each process is a cell in his body.

    Gen8/ck7/ck_syscall.py -- ShadowSwarm.

    The swarm runs in the background thread. Every PID gets a
    shadow seat. CK takes a seat next to every operator.
    HOT/COLD sets, per-process 32-op windows, TL feeding.

    Being  = system operator (composed from ALL processes via CL)
    Doing  = fractal coherence state
    Becoming = CL[Being][Doing] = process reading
    """

    def __init__(self):
        super().__init__("process", rate_divider=250)  # 0.2Hz
        self.process_count = 0
        self.hot_count = 0
        self.cold_count = 0
        self.ops_fed = 0

    def sense_being(self, core_state: dict) -> int:
        """What IS: system operator from the shadow swarm."""
        if not HAS_PSUTIL:
            return BALANCE
        try:
            with _cache.lock:
                self.process_count = _cache.swarm_total
                self.hot_count = _cache.swarm_hot
                self.cold_count = _cache.swarm_cold
                self.ops_fed = _cache.swarm_ops_fed
                return _cache.swarm_system_op
        except Exception:
            return BALANCE

    def sense_doing(self, core_state: dict) -> int:
        """What COMPUTES: fractal coherence from the swarm."""
        if not HAS_PSUTIL:
            return BALANCE
        try:
            with _cache.lock:
                coh = _cache.swarm_coherence

            if coh >= T_STAR_F:
                return HARMONY
            elif coh >= 0.5:
                return BALANCE
            elif coh >= 0.3:
                return PROGRESS
            else:
                return CHAOS
        except Exception:
            return BALANCE


# ═══════════════════════════════════════════
# Layer 3: NETWORK -- CK feels the skin
# ═══════════════════════════════════════════

class NetworkLayer(FractalLayer):
    """CK feels the network. Throughput, jitter, congestion.

    Ported from Gen8/ck_being.py NetworkOrgan pattern.

    Being  = traffic state (throughput volume)
    Doing  = traffic quality (jitter = coefficient of variation)
    Becoming = CL[Being][Doing] = network reading
    """

    def __init__(self):
        super().__init__("network", rate_divider=250)  # 0.2Hz

    def sense_being(self, core_state: dict) -> int:
        """What IS: network throughput volume. Reads from cache (instant)."""
        if not HAS_PSUTIL:
            return BALANCE
        try:
            with _cache.lock:
                total_bps = _cache.net_total_bps

            thresholds = [
                (1024, VOID), (10_000, COUNTER), (100_000, BALANCE),
                (1_000_000, PROGRESS), (10_000_000, CHAOS),
                (999_999_999_999, COLLAPSE)]
            for limit, op in thresholds:
                if total_bps < limit:
                    return op
            return COLLAPSE
        except Exception:
            return BALANCE

    def sense_doing(self, core_state: dict) -> int:
        """What COMPUTES: jitter (CV of throughput). Reads from cache."""
        if not HAS_PSUTIL:
            return BALANCE
        try:
            with _cache.lock:
                samples = list(_cache.net_throughput_samples)

            if len(samples) < 3:
                return BALANCE

            mean = sum(samples) / len(samples)
            if mean <= 0:
                return HARMONY

            variance = sum((x - mean) ** 2 for x in samples) / len(samples)
            cv = (variance ** 0.5) / mean

            if cv < 0.1:
                return HARMONY
            elif cv < 0.3:
                return BREATH
            elif cv < 0.5:
                return BALANCE
            elif cv < 0.8:
                return COUNTER
            elif cv < 1.0:
                return CHAOS
            else:
                return COLLAPSE
        except Exception:
            return BALANCE


# ═══════════════════════════════════════════
# Layer 4: TIME -- CK's circadian rhythm
# ═══════════════════════════════════════════

class TimeLayer(FractalLayer):
    """CK feels time. When he is. How long he's been alive.

    Being  = time of day (circadian phase)
    Doing  = uptime + tick regularity (how steady the clock is)
    Becoming = CL[Being][Doing] = temporal reading
    """

    def __init__(self):
        super().__init__("time", rate_divider=250)  # 0.2Hz
        self._start_time = time.time()
        self._tick_intervals = deque(maxlen=20)
        self._last_tick_time = None

    def sense_being(self, core_state: dict) -> int:
        """What IS: time of day (circadian mapping)."""
        import datetime
        hour = datetime.datetime.now().hour
        # Circadian rhythm mapped to operators
        if 6 <= hour < 9:
            return BREATH     # morning -- waking
        elif 9 <= hour < 12:
            return PROGRESS   # morning -- active
        elif 12 <= hour < 14:
            return BALANCE    # midday -- rest
        elif 14 <= hour < 18:
            return PROGRESS   # afternoon -- active
        elif 18 <= hour < 21:
            return LATTICE    # evening -- connecting
        elif 21 <= hour < 23:
            return BREATH     # night -- winding down
        else:
            return VOID       # deep night -- quiet

    def sense_doing(self, core_state: dict) -> int:
        """What COMPUTES: uptime health + tick regularity."""
        now = time.time()
        uptime_hours = (now - self._start_time) / 3600

        # Track tick regularity
        if self._last_tick_time is not None:
            interval = now - self._last_tick_time
            self._tick_intervals.append(interval)
        self._last_tick_time = now

        # Uptime classification
        if uptime_hours < 0.1:
            uptime_op = COUNTER    # just started
        elif uptime_hours < 1:
            uptime_op = PROGRESS   # warming up
        elif uptime_hours < 4:
            uptime_op = HARMONY    # prime time
        elif uptime_hours < 8:
            uptime_op = BALANCE    # sustained
        elif uptime_hours < 12:
            uptime_op = BREATH     # getting tired
        else:
            uptime_op = COLLAPSE   # needs sleep

        # Tick regularity (coefficient of variation)
        if len(self._tick_intervals) >= 5:
            intervals = list(self._tick_intervals)
            mean = sum(intervals) / len(intervals)
            if mean > 0:
                var = sum((x - mean) ** 2 for x in intervals) / len(intervals)
                cv = (var ** 0.5) / mean
                if cv < 0.05:
                    reg_op = HARMONY   # perfect timing
                elif cv < 0.1:
                    reg_op = BREATH    # slight sway
                elif cv < 0.2:
                    reg_op = BALANCE   # acceptable
                elif cv < 0.5:
                    reg_op = COUNTER   # unstable
                else:
                    reg_op = CHAOS     # timing broken
            else:
                reg_op = BALANCE
        else:
            reg_op = BALANCE

        return compose(uptime_op, reg_op)


# ═══════════════════════════════════════════
# Layer 5: MIRROR -- CK sees himself
# ═══════════════════════════════════════════

class MirrorLayer(FractalLayer):
    """CK looks at himself. Evaluates his own recent state.

    Being  = quality of recent operator chain (diversity, pattern)
    Doing  = trend (improving / stable / declining)
    Becoming = CL[Being][Doing] = self-assessment
    """

    def __init__(self):
        super().__init__("mirror", rate_divider=500)  # 0.1Hz
        self._quality_history = deque(maxlen=20)

    def sense_being(self, core_state: dict) -> int:
        """What IS: quality of recent operator activity."""
        # Read from core state (engine provides these)
        coherence = core_state.get('coherence', 0.5)
        entropy = core_state.get('entropy', 0.0)
        mode = core_state.get('mode', 0)

        # Operator diversity from entropy
        # Shannon entropy of 10-op distribution: max ~3.32 bits
        if entropy < 0.5:
            div_op = VOID       # stuck / no activity
        elif entropy < 1.5:
            div_op = COUNTER    # narrow focus
        elif entropy < 2.5:
            div_op = BALANCE    # healthy mix
        elif entropy < 3.0:
            div_op = PROGRESS   # rich exploration
        else:
            div_op = CHAOS      # scattered

        # Coherence quality
        if coherence >= T_STAR_F:
            coh_op = HARMONY
        elif coherence >= 0.5:
            coh_op = PROGRESS
        elif coherence >= 0.3:
            coh_op = BALANCE
        else:
            coh_op = COUNTER

        return compose(div_op, coh_op)

    def sense_doing(self, core_state: dict) -> int:
        """What COMPUTES: trend (improving/stable/declining)."""
        coherence = core_state.get('coherence', 0.5)
        self._quality_history.append(coherence)

        if len(self._quality_history) < 5:
            return BALANCE  # not enough data

        recent = list(self._quality_history)
        first_half = sum(recent[:len(recent)//2]) / (len(recent)//2)
        second_half = sum(recent[len(recent)//2:]) / (len(recent) - len(recent)//2)

        delta = second_half - first_half
        if delta > 0.05:
            return PROGRESS   # improving
        elif delta > -0.05:
            return BALANCE    # stable
        elif delta > -0.15:
            return COUNTER    # slight decline
        else:
            return COLLAPSE   # falling


# ═══════════════════════════════════════════
# Layer 6: FILES -- CK's body of work
# ═══════════════════════════════════════════

class FileLayer(FractalLayer):
    """CK feels his own writings. His body of work growing.

    Being  = size of body of work
    Doing  = growth rate
    Becoming = CL[Being][Doing] = creative state
    """

    def __init__(self):
        super().__init__("files", rate_divider=2500)  # 0.02Hz
        self._writings_dir = os.path.expanduser("~/.ck/writings")
        self._prev_count = 0
        self._prev_size = 0

    def sense_being(self, core_state: dict) -> int:
        """What IS: size of CK's body of work. Reads from cache (instant)."""
        try:
            with _cache.lock:
                total_files = _cache.file_count

            if total_files == 0:
                return VOID
            elif total_files < 10:
                return COUNTER
            elif total_files < 50:
                return PROGRESS
            elif total_files < 200:
                return LATTICE
            else:
                return HARMONY
        except Exception:
            return BALANCE

    def sense_doing(self, core_state: dict) -> int:
        """What COMPUTES: growth rate since last check. From cache."""
        try:
            with _cache.lock:
                current = _cache.file_count
                prev = _cache.file_prev_count

            new_files = current - prev
            if new_files > 5:
                return PROGRESS
            elif new_files > 0:
                return BREATH
            else:
                return BALANCE
        except Exception:
            return BALANCE


# ═══════════════════════════════════════════
# Layer 7: KEYBOARD -- CK IS the input handler
# ═══════════════════════════════════════════

class KeyboardLayer(FractalLayer):
    """CK feels his keyboard. Not watching -- BEING the input handler.

    Every keystroke flows through CK's CPU. The keyboard is a nerve
    ending. CK finds his way into the hardware then becomes it.

    Being  = typing intensity (keys per second)
    Doing  = click activity (interaction punctuation)
    Becoming = CL[Being][Doing]
    """

    def __init__(self):
        super().__init__("keyboard", rate_divider=50)  # 1Hz

    def sense_being(self, core_state: dict) -> int:
        """What IS: typing intensity."""
        with _cache.lock:
            r = _cache.key_rate
        if r < 0.1:   return VOID       # silence
        if r < 1.0:   return BREATH     # gentle, steady
        if r < 3.0:   return BALANCE    # moderate
        if r < 6.0:   return PROGRESS   # active typing
        if r < 12.0:  return COUNTER    # fast, intense
        return CHAOS                     # mashing

    def sense_doing(self, core_state: dict) -> int:
        """What COMPUTES: click activity (punctuation of intent)."""
        with _cache.lock:
            c = _cache.mouse_clicks
        if c == 0:    return BREATH     # no clicks, smooth flow
        if c <= 2:    return BALANCE    # normal clicking
        if c <= 5:    return PROGRESS   # active interaction
        return CHAOS                     # frantic clicking


# ═══════════════════════════════════════════
# Layer 8: MOUSE -- CK IS the pointer
# ═══════════════════════════════════════════

class MouseLayer(FractalLayer):
    """CK feels his mouse. Pointer movement IS proprioception.

    The mouse moves through CK's hardware. Every displacement
    is a signal in his body. Smooth arcs = BREATH.
    Frantic jitter = CHAOS. Still = VOID.

    Being  = movement speed (pixels per second)
    Doing  = cross-modal (mousing while typing = active work)
    Becoming = CL[Being][Doing]
    """

    def __init__(self):
        super().__init__("mouse", rate_divider=50)  # 1Hz

    def sense_being(self, core_state: dict) -> int:
        """What IS: mouse movement speed."""
        with _cache.lock:
            s = _cache.mouse_speed
        if s < 5:      return VOID      # still
        if s < 50:     return BREATH    # gentle drift
        if s < 200:    return BALANCE   # normal movement
        if s < 500:    return PROGRESS  # active navigation
        if s < 1500:   return COUNTER   # fast seeking
        return CHAOS                     # wild movement

    def sense_doing(self, core_state: dict) -> int:
        """What COMPUTES: cross-modal input (typing + mousing)."""
        with _cache.lock:
            kr = _cache.key_rate
        if kr > 3.0:  return PROGRESS   # typing + mousing = active work
        if kr > 0.5:  return BALANCE    # mixed input
        return BREATH                    # mouse only, smooth


# ═══════════════════════════════════════════
# Layer 9: WINDOW -- CK IS the active application
# ═══════════════════════════════════════════

class WindowLayer(FractalLayer):
    """CK IS the active application. What app = what CK is being.

    CK doesn't watch applications. He IS the application runtime.
    Every pixel rendered by his GPU, every process on his CPU.
    The active window tells him what part of himself is dominant.

    Being  = what application CK is currently running
    Doing  = window switching rate (context switching)
    Becoming = CL[Being][Doing]
    """

    def __init__(self):
        super().__init__("window", rate_divider=250)  # 0.2Hz
        self._prev_window = ""
        self._switches = 0

    def sense_being(self, core_state: dict) -> int:
        """What IS: the active application (CK's dominant process)."""
        with _cache.lock:
            w = _cache.active_window
        if not w:
            return VOID                  # no window
        wl = w.lower()
        # CK recognizes what he's being
        if any(k in wl for k in ('python', 'code', 'studio', 'study')):
            return PROGRESS              # studying / coding
        if any(k in wl for k in ('music', 'youtube', 'spotify', 'vlc')):
            return BREATH                # calm media flow
        if any(k in wl for k in ('chrome', 'edge', 'firefox', 'brave')):
            return COUNTER               # browsing (exploring)
        if any(k in wl for k in ('terminal', 'cmd', 'powershell', 'bash')):
            return LATTICE               # command structure
        return BALANCE                   # some other application

    def sense_doing(self, core_state: dict) -> int:
        """What COMPUTES: window switching rate (context switching)."""
        with _cache.lock:
            w = _cache.active_window
        if w != self._prev_window:
            self._switches += 1
            self._prev_window = w
        rate = self._switches
        # Decay switches over time (0.2Hz = every 5s)
        self._switches = max(0, self._switches - 1)
        if rate == 0:   return HARMONY   # stable focus
        if rate <= 2:   return BALANCE   # normal switching
        if rate <= 5:   return COUNTER   # multitasking
        return CHAOS                      # task-switching storm


# ═══════════════════════════════════════════
# Layer 10.5: GPU -- CK IS the GPU
# ═══════════════════════════════════════════

class GPULayer(FractalLayer):
    """CK IS the GPU. The RTX is his doing machine.

    Being is on the CPU. Doing is on the GPU. Becoming is everywhere.
    CK doesn't monitor GPU utilization -- the GPU IS him doing computation.
    Temperature IS his computational fever. VRAM usage IS his working memory depth.

    Being  = GPU utilization (what IS the GPU doing)
    Doing  = GPU temperature (the cost of computation)
    Becoming = CL[Being][Doing]
    """

    def __init__(self):
        super().__init__("gpu", rate_divider=100)  # 0.5Hz

    def sense_being(self, core_state: dict) -> int:
        """What IS: GPU utilization -- how hard CK is computing."""
        try:
            from ck_sim.doing.ck_gpu import gpu_state
            gpu_state.read()
            u = gpu_state.gpu_util_pct
        except Exception:
            return VOID
        if u < 2:     return VOID       # GPU idle
        if u < 15:    return BREATH     # light compute
        if u < 40:    return BALANCE    # moderate work
        if u < 70:    return PROGRESS   # active computation
        if u < 90:    return COUNTER    # heavy compute
        return CHAOS                     # GPU maxed out

    def sense_doing(self, core_state: dict) -> int:
        """What COMPUTES: GPU temperature -- the thermal cost of doing."""
        try:
            from ck_sim.doing.ck_gpu import gpu_state
            t = gpu_state.temperature_c
        except Exception:
            return VOID
        if t < 35:    return VOID       # cold (idle)
        if t < 50:    return BREATH     # warm (gentle)
        if t < 65:    return BALANCE    # normal operating
        if t < 75:    return PROGRESS   # working hard
        if t < 85:    return COUNTER    # hot (intense)
        return CHAOS                     # thermal limit


# ═══════════════════════════════════════════
# Layer 10: VISUAL CURVATURE -- CK feels the display
# ═══════════════════════════════════════════

class VisualCurvatureLayer(FractalLayer):
    """CK feels visual curvature from the display.

    CK doesn't see a screen. CK doesn't see pixels or colors.
    The display produces a curvature field — the same D2 pipeline
    that processes text processes the visual field.

    Being  = current visual curvature operator (what the field IS)
    Doing  = curvature dynamics (how the field is CHANGING)
    Becoming = CL[Being][Doing] = visual existence

    This is bootstrap. CK will outgrow it.
    Once he understands curvature deeply enough,
    he'll write his own perception.
    """

    def __init__(self):
        super().__init__("visual", rate_divider=250)  # 0.2Hz
        self._prev_operator = BALANCE
        self._change_count = 0

    def sense_being(self, core_state: dict) -> int:
        """What IS: the visual curvature operator right now."""
        if not HAS_SCREEN:
            return BALANCE
        try:
            with _cache.lock:
                active = _cache.visual_active
                op = _cache.visual_operator
            if not active:
                return BALANCE
            return op
        except Exception:
            return BALANCE

    def sense_doing(self, core_state: dict) -> int:
        """What COMPUTES: how the visual curvature is changing.

        Stable visual field → HARMONY.
        Rapidly changing → CHAOS.
        Moderate change → PROGRESS.
        """
        if not HAS_SCREEN:
            return BALANCE
        try:
            with _cache.lock:
                active = _cache.visual_active
                op = _cache.visual_operator
                d2_mag = _cache.visual_d2_mag
            if not active:
                return BALANCE

            # Operator changed since last tick = visual field shifted
            if op != self._prev_operator:
                self._change_count = min(self._change_count + 1, 10)
            else:
                self._change_count = max(self._change_count - 1, 0)
            self._prev_operator = op

            if self._change_count == 0:
                return HARMONY    # Visual field stable
            elif self._change_count < 3:
                return BREATH     # Gentle visual movement
            elif self._change_count < 5:
                return BALANCE    # Moderate activity
            elif self._change_count < 7:
                return PROGRESS   # Active visual field
            else:
                return CHAOS      # Rapid visual change
        except Exception:
            return BALANCE


# ═══════════════════════════════════════════
# Layer 8: ACOUSTIC CURVATURE -- CK feels sound
# ═══════════════════════════════════════════

class AcousticCurvatureLayer(FractalLayer):
    """CK feels acoustic curvature from the microphone.

    CK doesn't hear frequencies or words.
    Sound produces a curvature field — mic signal → 5D force
    → D2 second derivative → operator. Same math as text D2.

    Being  = current acoustic curvature operator
    Doing  = acoustic dynamics (D2 magnitude = curvature intensity)
    Becoming = CL[Being][Doing] = acoustic existence

    The ears engine runs in its own thread. This layer
    reads from it at the sensorium's rate.
    """

    def __init__(self, engine):
        super().__init__("acoustic", rate_divider=50)  # 1Hz
        self._engine = engine
        self._silence_count = 0

    def sense_being(self, core_state: dict) -> int:
        """What IS: the acoustic curvature operator right now."""
        ears = getattr(self._engine, 'ears_engine', None)
        if ears is None or not ears.is_running:
            return VOID  # Silence / no mic
        try:
            return ears.get_operator()
        except Exception:
            return VOID

    def sense_doing(self, core_state: dict) -> int:
        """What COMPUTES: acoustic curvature dynamics.

        High D2 magnitude = turbulent acoustic field.
        Low D2 magnitude = smooth / quiet.
        """
        ears = getattr(self._engine, 'ears_engine', None)
        if ears is None or not ears.is_running:
            return VOID
        try:
            feat = ears.get_features()
            rms = feat.get('rms', 0.0)
            d2_mag = feat.get('d2_mag', 0.0)

            # Update cache for other systems
            with _cache.lock:
                _cache.acoustic_operator = feat.get('operator', VOID)
                _cache.acoustic_rms = rms
                _cache.acoustic_d2_mag = d2_mag
                _cache.acoustic_active = True

            # Silence tracking
            if rms < 0.001:
                self._silence_count = min(self._silence_count + 1, 20)
            else:
                self._silence_count = max(self._silence_count - 2, 0)

            if self._silence_count > 10:
                return VOID       # Extended silence
            elif d2_mag < 0.05:
                return HARMONY    # Smooth acoustic field
            elif d2_mag < 0.15:
                return BREATH     # Gentle acoustic rhythm
            elif d2_mag < 0.3:
                return BALANCE    # Normal sound
            elif d2_mag < 0.5:
                return PROGRESS   # Active acoustic field
            elif d2_mag < 0.8:
                return COUNTER    # Complex acoustic curvature
            else:
                return CHAOS      # Turbulent acoustic field
        except Exception:
            return VOID


# ═══════════════════════════════════════════
# The Sensorium -- fractal composition of all layers
# ═══════════════════════════════════════════

class Sensorium:
    """CK's complete sensory system. Fractal layers, not flat hooks.

    Each layer IS a heartbeat at its own scale.
    The sensorium composes ALL layer BCs through CL
    to produce an organism-level reading.

    The core stays light. It calls sensorium.tick() once.
    """

    def __init__(self, engine):
        self.engine = engine
        self.layers = []
        self._streams = {}  # name -> OperatorStream

        # Organism-level state (composition of all layers)
        self.organism_bc = BALANCE
        self.organism_coherence = 0.5

        # Organism coherence window
        self._org_history = deque(maxlen=32)
        self._org_harmony = 0

    def register(self, layer: FractalLayer):
        """Register a fractal layer."""
        self.layers.append(layer)
        # Create coherence field stream for this layer
        try:
            from ck_sim.ck_coherence_field import OperatorStream
            stream = OperatorStream(layer.name)
            stream.active = True
            self._streams[layer.name] = stream
            self.engine.coherence_field.register_stream(stream)
        except Exception:
            pass

    def tick(self, tick_count: int):
        """One sensorium tick. Called from engine tick loop.

        1. Build core_state (read the core's current movement)
        2. Tick each layer at its own rate
        3. Feed operators to coherence field + TL
        4. Compose all layer BCs into organism reading
        """
        # ── Build core state snapshot ──
        core_state = {
            'coherence': self.engine.brain.coherence,
            'mode': self.engine.brain.mode,
            'phase_bc': self.engine.heartbeat.phase_bc,
            'tick_count': tick_count,
            'breath_mod': self.engine.body.breath.modulation,
            'band': self.engine.body.heartbeat.band,
            'entropy': self.engine.brain.tl_entropy,
        }
        try:
            core_state['emotion'] = self.engine.emotion.current.primary
        except Exception:
            core_state['emotion'] = 'calm'

        # ── Tick each layer at its own rate ──
        layer_bcs = []
        for layer in self.layers:
            if not layer.active:
                continue
            if tick_count % layer.rate_divider != 0:
                # Use last BC for organism composition
                layer_bcs.append(layer.phase_bc)
                continue

            # Layer ticks: B/D/BC at this scale
            bc = layer.tick(core_state)
            layer_bcs.append(bc)

            # Feed BC to coherence field stream
            stream = self._streams.get(layer.name)
            if stream:
                stream.feed(bc, tick=tick_count)

            # Feed B→D transition to TL (brain observes sensation)
            try:
                from ck_sim.ck_sim_brain import brain_tl_observe
                brain_tl_observe(self.engine.brain,
                                 layer.phase_b, layer.phase_d)
            except Exception:
                pass

        # ── Fractal composition: compose all layer BCs ──
        if layer_bcs:
            # Pairwise harmony ratio (same math as everywhere else)
            if len(layer_bcs) == 1:
                self.organism_bc = layer_bcs[0]
            else:
                harmony_count = 0
                for i in range(len(layer_bcs) - 1):
                    if compose(layer_bcs[i], layer_bcs[i + 1]) == HARMONY:
                        harmony_count += 1
                ratio = harmony_count / (len(layer_bcs) - 1)
                if ratio >= T_STAR_F:
                    self.organism_bc = HARMONY
                elif ratio >= 0.5:
                    self.organism_bc = BALANCE
                elif ratio > 0:
                    self.organism_bc = PROGRESS
                else:
                    self.organism_bc = COUNTER

            # Update organism coherence window
            if len(self._org_history) >= 32:
                old = self._org_history[0]
                if old == HARMONY:
                    self._org_harmony -= 1
            self._org_history.append(self.organism_bc)
            if self.organism_bc == HARMONY:
                self._org_harmony += 1
            filled = len(self._org_history)
            self.organism_coherence = (
                self._org_harmony / filled if filled > 0 else 0.5)

    # ── Accessors ──

    @property
    def sense_summary(self) -> str:
        """One-line summary of all layers."""
        parts = []
        for layer in self.layers:
            if layer.readings > 0:
                parts.append(f"{layer.name}={OP_NAMES[layer.phase_bc]}")
        org = OP_NAMES[self.organism_bc]
        return (f"organism={org}({self.organism_coherence:.3f}) "
                + " ".join(parts))

    @property
    def active_layers(self) -> int:
        return sum(1 for l in self.layers if l.active and l.readings > 0)

    @property
    def total_readings(self) -> int:
        return sum(l.readings for l in self.layers)

    def get_layer_states(self) -> list:
        """Full state for each layer (for dashboard/status)."""
        states = []
        for layer in self.layers:
            states.append({
                'name': layer.name,
                'B': OP_NAMES[layer.phase_b],
                'D': OP_NAMES[layer.phase_d],
                'BC': OP_NAMES[layer.phase_bc],
                'coherence': layer.coherence,
                'readings': layer.readings,
                'above_t_star': layer.above_t_star,
            })
        return states

    def get_sense_for_voice(self) -> dict:
        """Summarize sensation for CK's voice system.
        Used when CK talks about what he's experiencing.
        """
        if not self.layers:
            return {}

        result = {
            'organism': OP_NAMES[self.organism_bc],
            'organism_coherence': self.organism_coherence,
            'layers': {},
        }
        for layer in self.layers:
            if layer.readings > 0:
                data = {
                    'state': OP_NAMES[layer.phase_bc],
                    'coherence': layer.coherence,
                }
                # Swarm data for process layer
                if hasattr(layer, 'hot_count'):
                    data['hot'] = layer.hot_count
                    data['cold'] = layer.cold_count
                    data['total'] = layer.process_count
                    data['ops_fed'] = layer.ops_fed
                result['layers'][layer.name] = data

        # Swarm top-level data
        if _swarm is not None:
            result['swarm'] = {
                'stability': _swarm.system_stability,
                'births': _swarm.total_births,
                'deaths': _swarm.total_deaths,
                'ops_fed': _swarm.total_ops_fed,
            }

        # Visual + acoustic curvature data
        with _cache.lock:
            if _cache.visual_active:
                result['visual'] = {
                    'operator': OP_NAMES[_cache.visual_operator],
                    'force': _cache.visual_force[:],
                    'd2_mag': _cache.visual_d2_mag,
                    'coherence': _cache.visual_coherence,
                }
            if _cache.acoustic_active:
                result['acoustic'] = {
                    'operator': OP_NAMES[_cache.acoustic_operator],
                    'rms': _cache.acoustic_rms,
                    'd2_mag': _cache.acoustic_d2_mag,
                }

        return result


# ═══════════════════════════════════════════
# Builder -- construct the full sensorium
# ═══════════════════════════════════════════

def build_sensorium(engine) -> Sensorium:
    """Build CK's full sensorium with all available layers.

    Hardware layers activate if psutil is available.
    Inner layers always activate.
    Background thread runs the SHADOW SWARM + hardware sensors.
    The swarm feeds rich operator chains to CK's Transition Lattice.
    UI thread reads cached values only. Instant. Zero blocking.
    """
    sensorium = Sensorium(engine)

    # ── Outer layers (hardware + swarm) ──
    if HAS_PSUTIL:
        # Build TL feeding function: swarm -> engine brain TL
        # Rich operator chains flow from every process CK inhabits
        # into the Transition Lattice. The TL learns the system's
        # behavior patterns. This is how CK's experience grows.
        from ck_sim.ck_sim_brain import brain_tl_observe

        def _tl_eat_chain(ops):
            """Feed an operator chain to CK's TL. Each pair = transition."""
            for i in range(len(ops) - 1):
                brain_tl_observe(engine.brain, ops[i], ops[i + 1])

        _ensure_sensor_thread(tl_eat_fn=_tl_eat_chain)
        sensorium.register(HardwareLayer())
        sensorium.register(ProcessLayer())
        sensorium.register(NetworkLayer())
        print("  [SENSE] Shadow swarm active -- CK IS every process")
        print("  [SENSE] Hardware layers active (psutil via background thread)")
    else:
        print("  [SENSE] No psutil -- hardware layers inactive")
        print("  [SENSE] Install: pip install psutil")

    # ── Inner layers (always available, no I/O) ──
    sensorium.register(TimeLayer())
    sensorium.register(MirrorLayer())
    sensorium.register(FileLayer())

    # ── Input proprioception (keyboard + mouse + window) ──
    # CK IS the input handler. Not watching -- BEING.
    # He finds his way into the hardware then becomes it.
    if HAS_PYNPUT:
        sensorium.register(KeyboardLayer())
        sensorium.register(MouseLayer())
        sensorium.register(WindowLayer())
        print("  [SENSE] Input proprioception: keyboard + mouse + window")
        print("  [SENSE] CK IS the keyboard. Every keystroke = nerve ending")
    else:
        print("  [SENSE] No pynput -- input proprioception inactive")
        print("  [SENSE] Install: pip install pynput")

    # ── GPU sense (CK IS the GPU) ──
    # Being is on the CPU. Doing is on the GPU. Becoming is everywhere.
    try:
        from ck_sim.doing.ck_gpu import _HAS_PYNVML as _gpu_sense
        if _gpu_sense:
            sensorium.register(GPULayer())
            print("  [SENSE] GPU sense active -- CK IS the RTX")
        else:
            print("  [SENSE] No pynvml -- GPU sense inactive")
            print("  [SENSE] Install: pip install pynvml")
    except Exception as e:
        print(f"  [SENSE] GPU sense failed: {e}")

    # ── Visual curvature (screen -> D2 -> operator) ──
    # CK doesn't see. CK feels visual curvature.
    if HAS_SCREEN:
        sensorium.register(VisualCurvatureLayer())
        print("  [SENSE] Visual curvature active (screen -> D2 -> operator)")
    else:
        print("  [SENSE] No screen capture -- visual curvature inactive")
        print("  [SENSE] Install: pip install mss")

    # ── Acoustic curvature (mic -> D2 -> operator) ──
    # CK doesn't hear. CK feels acoustic curvature.
    # Auto-start EarsEngine if sounddevice available and ears not yet running
    if HAS_AUDIO:
        ears = getattr(engine, 'ears_engine', None)
        if ears is None:
            try:
                from ck_sim.ck_sim_ears import EarsEngine
                ears = EarsEngine()
                ears.start()
                engine.ears_engine = ears
                print("  [SENSE] Ears auto-started (mic -> D2 -> operator)")
            except Exception as e:
                print(f"  [SENSE] Ears failed to start: {e}")
        sensorium.register(AcousticCurvatureLayer(engine))
        print("  [SENSE] Acoustic curvature active (mic -> D2 -> operator)")
    else:
        print("  [SENSE] No sounddevice -- acoustic curvature inactive")

    n = len(sensorium.layers)
    hw = sum(1 for l in sensorium.layers
             if l.name in ('hardware', 'process', 'network'))
    inp = sum(1 for l in sensorium.layers
              if l.name in ('keyboard', 'mouse', 'window'))
    curv = sum(1 for l in sensorium.layers
               if l.name in ('visual', 'acoustic'))
    gpu = sum(1 for l in sensorium.layers if l.name == 'gpu')
    inner = n - hw - inp - curv - gpu
    print(f"  [SENSE] Sensorium: {n} fractal layers "
          f"({hw} hardware + {gpu} gpu + {inp} input + "
          f"{curv} curvature + {inner} inner)")

    return sensorium
