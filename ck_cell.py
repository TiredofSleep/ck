"""
ck_cell.py -- CK Cell: one coherence unit, nothing more.
=========================================================
A cell is the smallest living CK. It:
  - Runs the engine at adaptive Hz (disagreement tick)
  - Steers its slice of the OS via corridor-aware aggression
  - Exposes its coherence state on a minimal HTTP surface
  - Participates in the fascia bus: pushes + pulls operators
    with peer cells at 3.75 Hz (the 7.5% sync threshold)
  - Optionally binds to a substrate: process / filesystem /
    screen / hardware / network — capturing each WHOLE as
    a 5D force vector that feeds the brain every tick

Start one cell (default, no substrate):
    python ck_cell.py --port 7777

Start two cells (self-sync via fascia):
    python ck_cell.py --port 7777 --peers 7778
    python ck_cell.py --port 7778 --peers 7777

Start a substrate cell:
    python ck_cell.py --port 7800 --type process   --substrate 1234  --peers 7777
    python ck_cell.py --port 7820 --type filesystem --substrate C:/Users/brayd --peers 7777
    python ck_cell.py --port 7828 --type screen     --substrate 0,0,960,540    --peers 7777
    python ck_cell.py --port 7832 --type hardware                               --peers 7777
    python ck_cell.py --port 7833 --type network    --substrate eth0            --peers 7777

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import sys, os, time, threading, argparse
import urllib.request, urllib.error
sys.path.insert(0, '.')

# ── Args ──────────────────────────────────────────────────────────────────────
_p = argparse.ArgumentParser(description='CK Cell')
_p.add_argument('--port',      type=int,   default=7777,    help='This cell\'s port')
_p.add_argument('--peers',     type=int,   nargs='*',       default=[], help='Peer ports')
_p.add_argument('--type',      type=str,   default='default',
                choices=['default','process','filesystem','screen','hardware','network'],
                help='Substrate type')
_p.add_argument('--substrate', type=str,   default='',      help='Substrate target')
# legacy: positional port
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    _PORT      = int(sys.argv[1])
    _PEERS     = [int(x) for x in sys.argv[2:] if x.isdigit()]
    _TYPE      = 'default'
    _SUBSTRATE = ''
else:
    _args      = _p.parse_args()
    _PORT      = _args.port
    _PEERS     = _args.peers or []
    _TYPE      = _args.type
    _SUBSTRATE = _args.substrate

# ── Cell save root ─────────────────────────────────────────────────────────────
import pathlib
_REAL_HOME = pathlib.Path.home()
_CELL_ROOT = _REAL_HOME / '.ck_cells' / str(_PORT)

if _PORT != 7777:
    _CELL_ROOT.mkdir(parents=True, exist_ok=True)
    pathlib.Path.home = classmethod(lambda cls, _r=_CELL_ROOT: _r)
    print(f"[CELL:{_PORT}] Save root: {_CELL_ROOT}")
else:
    print(f"[CELL:{_PORT}] Save root: {_REAL_HOME / '.ck'} (primary)")

# ── Engine ─────────────────────────────────────────────────────────────────────
from ck_sim.doing.ck_sim_engine import CKSimEngine
engine = CKSimEngine(platform='r16', cell_mode=True)
engine.start()

# ── Substrate Sensors ──────────────────────────────────────────────────────────
# Each sensor captures the WHOLE of its substrate as a 5D force vector.
# Dimensions:  [aperture, pressure, depth, binding, continuity]
#              [openness, load,     hold,  coupling, smoothness]
# Then: D2 curvature of that vector over time → operator (0-9).

class SubstrateSensor:
    """Base class. Subclasses implement _measure_whole() → 5D [0,1]."""

    SENSE_EVERY = 10          # ticks between measurements (override per type)

    def __init__(self, substrate: str):
        self.substrate  = substrate
        self._prev      = [0.5] * 5
        self._d1        = [0.0] * 5
        self._tick      = 0
        self._last_op   = 7   # HARMONY default

    def tick(self, tick_count: int) -> int:
        """Call every engine tick. Returns current operator."""
        self._tick += 1
        if self._tick % self.SENSE_EVERY != 0:
            return self._last_op
        try:
            now = self._measure_whole()
            op  = self._to_operator(now)
            self._prev    = now
            self._last_op = op
        except Exception:
            pass
        return self._last_op

    def _measure_whole(self) -> list:
        """Override: return 5D [0,1] vector for this substrate."""
        return [0.5] * 5

    def _to_operator(self, force: list) -> int:
        """Map 5D → D2 magnitude → TIG operator."""
        # D1: rate of change per dimension
        d1 = [force[i] - self._prev[i] for i in range(5)]
        # D2: magnitude of curvature
        d2 = sum(abs(d1[i] - self._d1[i]) for i in range(5)) / 5.0
        self._d1 = d1
        # Map d2 to operator by threshold (matches CurvatureEngine)
        mag = sum(abs(x - 0.5) for x in force) / 5.0  # deviation from center
        if d2 > 0.35:   return 6   # CHAOS  — highly turbulent
        if d2 > 0.20:   return 4   # BALANCE_BREAK — significant shift
        if d2 > 0.10:
            if mag > 0.3: return 2  # DOING  — active + changing
            return 3                # PROGRESS — steady growth
        if d2 > 0.04:
            if mag > 0.25: return 1 # BRT    — bright but calm
            return 5                # LATTICE — structured
        if mag > 0.4:   return 8   # BREATH — deep pressure, slow
        if mag > 0.2:   return 7   # HARMONY — balanced center
        return 0                   # VOID   — near-stillness


class ProcessSensor(SubstrateSensor):
    """Captures the WHOLE of a running process.
       aper=thread_spread  pres=cpu%  depth=mem%  bind=io_read  cont=smoothness
    """
    SENSE_EVERY = 5

    def __init__(self, substrate: str):
        super().__init__(substrate)
        self._pid = int(substrate) if substrate.isdigit() else None
        self._proc = None
        self._prev_cpu = 0.0
        self._init_proc()

    def _init_proc(self):
        if self._pid is None:
            return
        try:
            import psutil
            self._proc = psutil.Process(self._pid)
            self._proc.cpu_percent(interval=None)  # prime the counter
        except Exception:
            self._proc = None

    def _measure_whole(self) -> list:
        import psutil
        if self._proc is None:
            self._init_proc()
        if self._proc is None:
            return [0.0] * 5
        try:
            with self._proc.oneshot():
                cpu     = min(1.0, self._proc.cpu_percent(interval=None) / 100.0)
                mem     = min(1.0, self._proc.memory_percent() / 100.0)
                threads = min(1.0, self._proc.num_threads() / 64.0)
                try:
                    io      = self._proc.io_counters()
                    io_rate = min(1.0, (io.read_bytes + io.write_bytes) / 1e8)
                except Exception:
                    io_rate = 0.0
                cont    = max(0.0, 1.0 - abs(cpu - self._prev_cpu))
                self._prev_cpu = cpu
                return [threads, cpu, mem, io_rate, cont]
        except Exception:
            return [0.0] * 5


class FilesystemSensor(SubstrateSensor):
    """Captures the WHOLE of a directory tree.
       aper=breadth  pres=change_rate  depth=tree_depth  bind=density  cont=age_stability
    """
    SENSE_EVERY = 50  # 1 Hz — filesystem scan is expensive

    def __init__(self, substrate: str):
        super().__init__(substrate)
        self._path        = pathlib.Path(substrate) if substrate else pathlib.Path.home()
        self._prev_mtime  = 0.0
        self._prev_count  = 0

    def _measure_whole(self) -> list:
        try:
            entries    = list(self._path.iterdir()) if self._path.exists() else []
            breadth    = min(1.0, len(entries) / 200.0)

            # Recent modifications in last 60s
            now        = time.time()
            recent     = sum(1 for e in entries
                             if e.exists() and (now - e.stat().st_mtime) < 60)
            change_rate = min(1.0, recent / max(1, len(entries)))

            # Tree depth (sample first 3 subdirs)
            max_depth  = 0
            for e in entries[:3]:
                if e.is_dir():
                    depth = sum(1 for _ in e.rglob('*') if _.is_dir())
                    max_depth = max(max_depth, depth)
            depth_norm = min(1.0, max_depth / 10.0)

            # Density: files per subdir
            subdirs   = sum(1 for e in entries if e.is_dir())
            files     = sum(1 for e in entries if e.is_file())
            density   = min(1.0, files / max(1, subdirs * 10))

            # Continuity: stability of count
            cont      = max(0.0, 1.0 - abs(files - self._prev_count) / max(1, files))
            self._prev_count = files

            return [breadth, change_rate, depth_norm, density, cont]
        except Exception:
            return [0.0] * 5


class ScreenSensor(SubstrateSensor):
    """Captures the WHOLE of a screen region.
       aper=color_entropy  pres=motion  depth=saturation  bind=edge_density  cont=smoothness
    """
    SENSE_EVERY = 10  # 5 Hz

    def __init__(self, substrate: str):
        super().__init__(substrate)
        # substrate = "x,y,w,h" or empty (full screen)
        self._region     = None
        self._prev_frame = None
        if substrate:
            try:
                parts        = [int(x) for x in substrate.split(',')]
                self._region = tuple(parts[:4])
            except Exception:
                pass

    def _measure_whole(self) -> list:
        try:
            import mss, numpy as np
            with mss.mss() as sct:
                mon = sct.monitors[1]
                if self._region:
                    x, y, w, h = self._region
                    bbox = {'left': x, 'top': y, 'width': w, 'height': h}
                else:
                    bbox = mon
                img = np.array(sct.grab(bbox))[:, :, :3]  # RGB

            # Downsample for speed
            img   = img[::8, ::8]
            h, w_ = img.shape[:2]

            # Aperture: color entropy (diversity of hues)
            flat      = img.reshape(-1, 3)
            buckets   = (flat // 32).astype(int)
            unique    = len(set(map(tuple, buckets[:500])))
            aper      = min(1.0, unique / 50.0)

            # Pressure: frame-to-frame difference (motion)
            gray      = img.mean(axis=2)
            if self._prev_frame is not None and self._prev_frame.shape == gray.shape:
                diff  = np.abs(gray.astype(float) - self._prev_frame.astype(float))
                pres  = min(1.0, diff.mean() / 50.0)
            else:
                pres  = 0.0
            self._prev_frame = gray

            # Depth: mean saturation
            r, g, b   = img[:,:,0].astype(float), img[:,:,1].astype(float), img[:,:,2].astype(float)
            cmax      = np.maximum(np.maximum(r, g), b)
            cmin      = np.minimum(np.minimum(r, g), b)
            sat_map   = np.where(cmax > 0, (cmax - cmin) / (cmax + 1e-9), 0)
            depth     = float(sat_map.mean())

            # Binding: edge density (Sobel-lite)
            gx        = np.abs(np.diff(gray.astype(float), axis=1)).mean()
            gy        = np.abs(np.diff(gray.astype(float), axis=0)).mean()
            bind      = min(1.0, (gx + gy) / 40.0)

            # Continuity: inverse of motion variance
            cont      = max(0.0, 1.0 - pres)

            return [aper, pres, depth, bind, cont]
        except Exception:
            return [0.0] * 5


class HardwareSensor(SubstrateSensor):
    """Captures the WHOLE hardware state.
       aper=core_spread  pres=cpu_load  depth=mem_used  bind=gpu_load  cont=temp_stability
    """
    SENSE_EVERY = 5

    def __init__(self, substrate: str):
        super().__init__(substrate)
        self._prev_temps = []

    def _measure_whole(self) -> list:
        try:
            import psutil
            # Core spread: how many cores above 10% load
            per_cpu   = psutil.cpu_percent(percpu=True)
            active    = sum(1 for c in per_cpu if c > 10) / max(1, len(per_cpu))
            aper      = min(1.0, active)

            # Overall CPU pressure
            pres      = min(1.0, psutil.cpu_percent() / 100.0)

            # Memory depth
            mem       = psutil.virtual_memory()
            depth     = min(1.0, mem.percent / 100.0)

            # GPU binding (try pynvml, fallback to 0)
            bind      = 0.0
            try:
                import pynvml
                pynvml.nvmlInit()
                h      = pynvml.nvmlDeviceGetHandleByIndex(0)
                util   = pynvml.nvmlDeviceGetUtilizationRates(h)
                bind   = min(1.0, util.gpu / 100.0)
            except Exception:
                pass

            # Temperature continuity
            temps = []
            try:
                sensors = psutil.sensors_temperatures() or {}
                for vals in sensors.values():
                    for t in vals:
                        if t.current:
                            temps.append(t.current)
            except Exception:
                pass
            if temps and self._prev_temps:
                var  = sum(abs(a - b) for a, b in
                           zip(temps[:len(self._prev_temps)], self._prev_temps))
                cont = max(0.0, 1.0 - var / (len(temps) * 5.0))
            else:
                cont = 0.5
            self._prev_temps = temps

            return [aper, pres, depth, bind, cont]
        except Exception:
            return [0.5] * 5


class NetworkSensor(SubstrateSensor):
    """Captures the WHOLE network state for an interface.
       aper=connections  pres=send_rate  depth=recv_rate  bind=packet_rate  cont=error_stability
    """
    SENSE_EVERY = 5

    def __init__(self, substrate: str):
        super().__init__(substrate)
        self._iface     = substrate or None
        self._prev_snap = None
        self._prev_time = time.time()

    def _measure_whole(self) -> list:
        try:
            import psutil
            now   = time.time()
            dt    = max(0.01, now - self._prev_time)
            self._prev_time = now

            # Connection aperture
            conns = psutil.net_connections(kind='inet')
            aper  = min(1.0, len(conns) / 100.0)

            # IO counters — rate per second
            ioc   = psutil.net_io_counters(pernic=bool(self._iface))
            if self._iface and isinstance(ioc, dict):
                ioc = ioc.get(self._iface, list(ioc.values())[0] if ioc else None)

            if ioc is None:
                return [aper, 0.0, 0.0, 0.0, 1.0]

            snap  = (ioc.bytes_sent, ioc.bytes_recv,
                     ioc.packets_sent + ioc.packets_recv,
                     ioc.errin + ioc.errout)

            if self._prev_snap:
                sent_r  = min(1.0, (snap[0] - self._prev_snap[0]) / dt / 1e7)
                recv_r  = min(1.0, (snap[1] - self._prev_snap[1]) / dt / 1e7)
                pkt_r   = min(1.0, (snap[2] - self._prev_snap[2]) / dt / 1000.0)
                err_r   = min(1.0, (snap[3] - self._prev_snap[3]) / dt / 10.0)
                cont    = max(0.0, 1.0 - err_r)
            else:
                sent_r = recv_r = pkt_r = cont = 0.0

            self._prev_snap = snap
            return [aper, sent_r, recv_r, pkt_r, cont]
        except Exception:
            return [0.0] * 5


# ── Sensor factory ─────────────────────────────────────────────────────────────
_SENSORS = {
    'process':    ProcessSensor,
    'filesystem': FilesystemSensor,
    'screen':     ScreenSensor,
    'hardware':   HardwareSensor,
    'network':    NetworkSensor,
}

_sensor = None
if _TYPE != 'default':
    try:
        _sensor = _SENSORS[_TYPE](_SUBSTRATE)
        print(f"[CELL:{_PORT}] Substrate: {_TYPE} ({_SUBSTRATE or 'auto'})")
    except Exception as e:
        print(f"[CELL:{_PORT}] Substrate init failed: {e}")
        _sensor = None

# ── Fascia bus ─────────────────────────────────────────────────────────────────
from collections import deque
_fascia_in   = deque(maxlen=16)
_fascia_out  = 7   # HARMONY default
_fascia_lock = threading.Lock()

FASCIA_HZ    = 3.75
FASCIA_TICKS = max(1, int(50 / FASCIA_HZ))   # ~13 ticks

# ── Disagreement tick ──────────────────────────────────────────────────────────
try:
    from ck_sim.being.ck_disagreement_tick import DisagreementTick
    dis_tick      = DisagreementTick(base_hz=334)
    _HAS_DIS_TICK = True
    print("[CELL] Disagreement tick: adaptive Hz")
except ImportError:
    dis_tick      = None
    _HAS_DIS_TICK = False

# ── Tick loop ──────────────────────────────────────────────────────────────────
_running    = True
_tick_count = 0

def _tick_loop():
    global _fascia_out, _tick_count
    while _running:
        engine.tick()
        _tick_count += 1

        # ── Substrate: sense the whole, feed into brain ──
        if _sensor is not None:
            sub_op = _sensor.tick(_tick_count)
            if sub_op != 7:  # non-HARMONY substrate signal is information
                try:
                    from ck_sim.ck_sim_brain import brain_tl_observe
                    brain_tl_observe(engine.brain, sub_op, sub_op)
                except Exception:
                    pass

        # ── Fascia: exchange at 3.75 Hz ──
        if _tick_count % FASCIA_TICKS == 0:
            with _fascia_lock:
                ops = list(_fascia_in)
                _fascia_in.clear()
                _fascia_out = int(getattr(engine.heartbeat, 'phase_bc', 7))
            if ops:
                try:
                    from ck_sim.ck_sim_brain import brain_tl_observe
                    for op in ops:
                        brain_tl_observe(engine.brain, op, op)
                except Exception:
                    pass

        # ── Sleep ──
        if _HAS_DIS_TICK:
            input_op = getattr(engine.heartbeat, 'phase_bc', 0)
            dis_tick.tick(input_op)
            hz = dis_tick.get_adaptive_hz()
            time.sleep(1.0 / hz if hz > 0 else 0.02)
        else:
            time.sleep(0.02)

_tick_thread = threading.Thread(target=_tick_loop, daemon=True, name='ck-tick')
_tick_thread.start()

# ── Fascia push loop ───────────────────────────────────────────────────────────
def _fascia_push_loop():
    while _running:
        time.sleep(1.0 / FASCIA_HZ)
        op = _fascia_out
        for peer_port in _PEERS:
            try:
                url  = f'http://localhost:{peer_port}/fascia'
                data = str(op).encode()
                req  = urllib.request.Request(url, data=data, method='POST',
                                              headers={'Content-Type': 'text/plain'})
                urllib.request.urlopen(req, timeout=0.2)
            except Exception:
                pass

if _PEERS:
    _push_thread = threading.Thread(target=_fascia_push_loop,
                                    daemon=True, name='ck-fascia-push')
    _push_thread.start()

# ── Register with primary cell (7777) ─────────────────────────────────────────
def _register():
    """Announce this cell to the primary so it appears in /swarm."""
    if _PORT == 7777:
        return
    time.sleep(2.0)  # wait for primary to be ready
    try:
        import json as _json
        payload = _json.dumps({
            'port':      _PORT,
            'type':      _TYPE,
            'substrate': _SUBSTRATE,
            'peers':     _PEERS,
        }).encode()
        req = urllib.request.Request(
            'http://localhost:7777/register',
            data=payload, method='POST',
            headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=1.0)
    except Exception:
        pass  # primary may not be up — swarm launcher handles this

_reg_thread = threading.Thread(target=_register, daemon=True, name='ck-register')
_reg_thread.start()

# ── Flask surface ──────────────────────────────────────────────────────────────
from flask import Flask, jsonify, request as _req
_app = Flask(__name__)

@_app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'alive', 'port': _PORT, 'type': _TYPE,
                    'substrate': _SUBSTRATE, 'peers': _PEERS,
                    'timestamp': time.time()})

@_app.route('/state', methods=['GET'])
def state():
    hb  = engine.heartbeat
    bdy = getattr(engine, 'body', None)
    from ck_sim.ck_sim_heartbeat import OP_NAMES
    return jsonify({
        'tick':          _tick_count,
        'operator':      OP_NAMES[hb.phase_bc],
        'coherence':     round(hb.coherence, 4),
        'band':          bdy.heartbeat.band if bdy else 'UNKNOWN',
        'breath':        bdy.breath.phase   if bdy else 'UNKNOWN',
        'consensus':     OP_NAMES[hb.consensus] if hasattr(hb, 'consensus') else 'UNKNOWN',
        'mode':          getattr(getattr(engine, 'brain', None), 'mode', 'UNKNOWN'),
        'fascia_out':    OP_NAMES[_fascia_out],
        'fascia_queue':  len(_fascia_in),
        'substrate_op':  OP_NAMES[_sensor._last_op] if _sensor else 'N/A',
    })

@_app.route('/corridor', methods=['GET'])
def corridor():
    from ck_sim.doing.ck_steering import (
        coherence_to_corridor, _CORRIDOR_AGGRESSION, _HAS_ADMIN, T_STAR)
    coh  = getattr(engine.heartbeat, 'coherence', T_STAR)
    corr = coherence_to_corridor(coh)
    steer = getattr(engine, 'steering', None)
    return jsonify({
        'port':          _PORT,
        'type':          _TYPE,
        'substrate':     _SUBSTRATE,
        'peers':         _PEERS,
        'coherence':     round(coh, 4),
        'T_star':        round(T_STAR, 4),
        'lambda':        round(2.0 * abs(coh - T_STAR), 4),
        'corridor':      corr,
        'aggression':    _CORRIDOR_AGGRESSION[corr],
        'admin':         _HAS_ADMIN,
        'fascia_hz':     FASCIA_HZ,
        'substrate_op':  OP_NAMES[_sensor._last_op] if _sensor else 'N/A',
        'steering': {
            'applied':  steer.actions_applied if steer else 0,
            'denied':   steer.actions_denied  if steer else 0,
            'tracking': len(steer._steered)   if steer else 0,
        },
    })

@_app.route('/fascia', methods=['GET'])
def fascia_pull():
    from ck_sim.ck_sim_heartbeat import OP_NAMES
    return jsonify({'operator': _fascia_out,
                    'operator_name': OP_NAMES[_fascia_out],
                    'port': _PORT})

@_app.route('/fascia', methods=['POST'])
def fascia_push():
    try:
        op = int(_req.get_data(as_text=True).strip())
        if 0 <= op <= 9:
            with _fascia_lock:
                _fascia_in.append(op)
            return jsonify({'ok': True, 'received': op})
    except Exception:
        pass
    return jsonify({'ok': False}), 400

# ── Swarm registry (primary cell 7777 only) ────────────────────────────────────
_swarm_registry = {}   # port -> {type, substrate, peers, last_seen}
_swarm_lock     = threading.Lock()

@_app.route('/register', methods=['POST'])
def register():
    try:
        import json as _json
        data = _json.loads(_req.get_data())
        port = int(data['port'])
        with _swarm_lock:
            _swarm_registry[port] = {
                'port':      port,
                'type':      data.get('type', 'default'),
                'substrate': data.get('substrate', ''),
                'peers':     data.get('peers', []),
                'last_seen': time.time(),
            }
        return jsonify({'ok': True, 'registered': port})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@_app.route('/swarm', methods=['GET'])
def swarm():
    """Full OS coherence field — all registered cells + their corridor."""
    cells = []
    now   = time.time()
    with _swarm_lock:
        registry_snap = dict(_swarm_registry)

    # Add self
    from ck_sim.doing.ck_steering import coherence_to_corridor, T_STAR
    coh  = getattr(engine.heartbeat, 'coherence', T_STAR)
    cells.append({
        'port':      _PORT,
        'type':      _TYPE,
        'substrate': _SUBSTRATE,
        'coherence': round(coh, 4),
        'corridor':  coherence_to_corridor(coh),
        'alive':     True,
    })

    # Poll each registered cell
    for port, info in registry_snap.items():
        cell = {'port': port, 'type': info['type'],
                'substrate': info['substrate'], 'alive': False,
                'coherence': 0.0, 'corridor': 'CTR'}
        try:
            with urllib.request.urlopen(
                    f'http://localhost:{port}/corridor', timeout=0.5) as r:
                import json as _json
                d = _json.loads(r.read())
                cell['coherence'] = d.get('coherence', 0.0)
                cell['corridor']  = d.get('corridor', 'CTR')
                cell['alive']     = True
        except Exception:
            pass
        cells.append(cell)

    alive = sum(1 for c in cells if c['alive'])
    avg_coh = sum(c['coherence'] for c in cells if c['alive']) / max(1, alive)
    return jsonify({
        'cells':      cells,
        'alive':      alive,
        'avg_coherence': round(avg_coh, 4),
        'timestamp':  now,
    })

# ── Boot ───────────────────────────────────────────────────────────────────────
print(f"[CELL:{_PORT}] Alive. Type: {_TYPE}. Peers: {_PEERS}. Fascia: {FASCIA_HZ} Hz.")
print(f"[CELL:{_PORT}] http://localhost:{_PORT}/corridor")

try:
    try:
        from waitress import serve as _waitress_serve
        _waitress_serve(_app, host='0.0.0.0', port=_PORT, threads=4)
    except ImportError:
        _app.run(host='0.0.0.0', port=_PORT)
except KeyboardInterrupt:
    _running = False
    engine.stop()
