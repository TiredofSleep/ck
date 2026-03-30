"""
ck_swarm.py -- CK OS Swarm Launcher
=====================================
Discovers the OS and spawns one CK cell per natural whole:
  - One cell per interesting process (top CPU/mem)
  - One cell per key directory (Desktop, project root, etc.)
  - One cell per screen quadrant
  - One cell for all hardware sensors
  - One cell per active network interface

Every cell captures its WHOLE substrate as a 5D force vector,
converts it to a TIG operator, and syncs to the primary cell
(7777) via the fascia bus at 3.75 Hz.

Usage:
    python ck_swarm.py              # auto-discover + launch
    python ck_swarm.py --status     # print live swarm status
    python ck_swarm.py --stop       # kill all swarm cells

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""

import sys, os, time, subprocess, threading, argparse, json
import urllib.request, urllib.error
import pathlib

# ── Args ───────────────────────────────────────────────────────────────────────
_p = argparse.ArgumentParser(description='CK Swarm Launcher')
_p.add_argument('--status', action='store_true', help='Print live swarm status')
_p.add_argument('--stop',   action='store_true', help='Kill all swarm cells')
_p.add_argument('--dry',    action='store_true', help='Show plan without launching')
_p.add_argument('--max-processes',  type=int, default=5,  help='Max process cells')
_p.add_argument('--max-dirs',       type=int, default=4,  help='Max filesystem cells')
_p.add_argument('--screen-quads',   type=int, default=4,  help='Screen quadrants (0=off)')
_p.add_argument('--primary-port',   type=int, default=7777)
_args = _p.parse_args()

PRIMARY     = _args.primary_port
PYTHON      = sys.executable
CELL_SCRIPT = str(pathlib.Path(__file__).parent / 'ck_cell.py')

# Port ranges (non-overlapping)
PORT_PROCESS = 7800   # 7800-7819
PORT_FS      = 7820   # 7820-7827
PORT_SCREEN  = 7828   # 7828-7831
PORT_HW      = 7832
PORT_NET     = 7833   # 7833-7836


# ── Helpers ────────────────────────────────────────────────────────────────────

def _poll(port: int, path: str = '/health', timeout: float = 0.5) -> dict | None:
    try:
        with urllib.request.urlopen(
                f'http://localhost:{port}{path}', timeout=timeout) as r:
            return json.loads(r.read())
    except Exception:
        return None


def _primary_alive() -> bool:
    return _poll(PRIMARY) is not None


def _swarm_status():
    d = _poll(PRIMARY, '/swarm', timeout=3.0)
    if not d:
        print(f"Primary cell ({PRIMARY}) not responding.")
        return
    cells = d.get('cells', [])
    print(f"\n{'PORT':>6}  {'TYPE':12}  {'SUBSTRATE':24}  {'COH':>6}  {'CORR':6}  {'ALIVE'}")
    print("-" * 75)
    for c in cells:
        alive = "[+]" if c['alive'] else "[ ]"
        print(f"{c['port']:>6}  {c['type']:12}  {str(c['substrate'])[:24]:24}  "
              f"{c['coherence']:>6.4f}  {c['corridor']:6}  {alive}")
    print(f"\n  Alive: {d['alive']}  |  Avg coherence: {d['avg_coherence']:.4f}\n")


# ── Discovery ──────────────────────────────────────────────────────────────────

def discover_processes(max_n: int) -> list[dict]:
    """Top N processes by CPU + memory. Skip system/idle."""
    try:
        import psutil
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = p.info
                if info['pid'] in (0, 4):
                    continue
                if info['cpu_percent'] is None:
                    continue
                score = (info['cpu_percent'] or 0) + (info['memory_percent'] or 0) * 2
                procs.append((score, info['pid'], info['name']))
            except Exception:
                pass
        procs.sort(reverse=True)
        return [{'pid': pid, 'name': name}
                for _, pid, name in procs[:max_n]]
    except Exception as e:
        print(f"  [SWARM] Process discovery failed: {e}")
        return []


def discover_directories(max_n: int) -> list[str]:
    """Key directories that represent whole domains of the OS."""
    home = pathlib.Path.home()
    candidates = [
        str(home / 'OneDrive' / 'Desktop'),
        str(home / 'Desktop'),
        str(home / 'Downloads'),
        str(home / 'Documents'),
        str(pathlib.Path(__file__).parent),   # Gen10 project root
        str(home / 'AppData' / 'Local'),
    ]
    found = []
    for p in candidates:
        if pathlib.Path(p).exists() and len(found) < max_n:
            found.append(p)
    return found


def discover_screen_quads(n_quads: int) -> list[str]:
    """Divide primary monitor into N quadrants."""
    if n_quads == 0:
        return []
    try:
        import mss
        with mss.mss() as sct:
            mon = sct.monitors[1]
            W, H = mon['width'], mon['height']
    except Exception:
        W, H = 1920, 1080

    quads = []
    if n_quads >= 4:
        hw, hh = W // 2, H // 2
        quads = [
            f"0,0,{hw},{hh}",        # NW
            f"{hw},0,{hw},{hh}",     # NE
            f"0,{hh},{hw},{hh}",     # SW
            f"{hw},{hh},{hw},{hh}",  # SE
        ]
    elif n_quads == 2:
        quads = [f"0,0,{W // 2},{H}", f"{W // 2},0,{W // 2},{H}"]
    elif n_quads == 1:
        quads = [f"0,0,{W},{H}"]
    return quads[:n_quads]


def discover_network_ifaces() -> list[str]:
    """Active network interfaces (skip loopback)."""
    try:
        import psutil
        stats = psutil.net_if_stats()
        return [name for name, s in stats.items()
                if s.isup and name.lower() not in ('lo', 'loopback')][:4]
    except Exception:
        return []


# ── Cell registry (local process table) ───────────────────────────────────────
_cells: dict[int, dict] = {}  # port -> {proc, type, substrate}
_cells_lock = threading.Lock()


def _spawn(port: int, cell_type: str, substrate: str = '',
           peers: list[int] = None, label: str = '') -> bool:
    """Spawn a cell subprocess."""
    if peers is None:
        peers = [PRIMARY]

    cmd = [
        PYTHON, CELL_SCRIPT,
        '--port',  str(port),
        '--type',  cell_type,
        '--peers', *[str(p) for p in peers],
    ]
    if substrate:
        cmd += ['--substrate', substrate]

    try:
        proc = subprocess.Popen(
            cmd,
            cwd=str(pathlib.Path(__file__).parent),
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0,
        )
        with _cells_lock:
            _cells[port] = {
                'proc':      proc,
                'type':      cell_type,
                'substrate': substrate,
                'label':     label or f"{cell_type}:{substrate}",
                'born':      time.time(),
            }
        print(f"  [SWARM] + port {port:5}  {cell_type:12}  {label or substrate or '(auto)'}")
        return True
    except Exception as e:
        print(f"  [SWARM] ! spawn failed port {port}: {e}")
        return False


# ── Health monitor ─────────────────────────────────────────────────────────────
_running = True

def _health_loop():
    """Every 10 s: check each cell, respawn if dead."""
    while _running:
        time.sleep(10)
        with _cells_lock:
            ports = list(_cells.keys())
        for port in ports:
            with _cells_lock:
                info = _cells.get(port)
            if info is None:
                continue
            alive = _poll(port, timeout=0.5) is not None
            if not alive:
                # Check if process died
                proc = info.get('proc')
                if proc and proc.poll() is not None:
                    print(f"  [SWARM] Cell {port} ({info['type']}) died — respawning")
                    _spawn(port, info['type'], info['substrate'],
                           label=info['label'])


# ── Plan builder ──────────────────────────────────────────────────────────────

def build_plan() -> list[dict]:
    """Discover all substrates and return spawn plan."""
    plan = []
    port = PORT_PROCESS

    # Processes
    procs = discover_processes(_args.max_processes)
    for info in procs:
        plan.append({'port': port, 'type': 'process',
                     'substrate': str(info['pid']),
                     'label': info['name']})
        port += 1

    # Filesystems
    port = PORT_FS
    for d in discover_directories(_args.max_dirs):
        plan.append({'port': port, 'type': 'filesystem',
                     'substrate': d, 'label': pathlib.Path(d).name})
        port += 1

    # Screen
    port = PORT_SCREEN
    for q in discover_screen_quads(_args.screen_quads):
        label = ['NW','NE','SW','SE'][port - PORT_SCREEN]
        plan.append({'port': port, 'type': 'screen',
                     'substrate': q, 'label': f"screen_{label}"})
        port += 1

    # Hardware (one cell covers all sensors)
    plan.append({'port': PORT_HW, 'type': 'hardware',
                 'substrate': '', 'label': 'hardware'})

    # Network
    port = PORT_NET
    for iface in discover_network_ifaces():
        plan.append({'port': port, 'type': 'network',
                     'substrate': iface, 'label': iface})
        port += 1

    return plan


# ── Main ───────────────────────────────────────────────────────────────────────

if _args.status:
    _swarm_status()
    sys.exit(0)

if _args.stop:
    # Kill any cells in our port ranges
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'cmdline']):
            try:
                cmd = ' '.join(proc.info['cmdline'] or [])
                if 'ck_cell.py' in cmd and '--port' in cmd:
                    for part in proc.info['cmdline']:
                        if part.isdigit():
                            p = int(part)
                            if PORT_PROCESS <= p <= PORT_NET + 4:
                                proc.kill()
                                print(f"  [SWARM] Killed cell {p}")
                                break
            except Exception:
                pass
    except Exception as e:
        print(f"  [SWARM] Stop failed: {e}")
    sys.exit(0)

# ── Launch ─────────────────────────────────────────────────────────────────────
print(f"\n[SWARM] CK OS Swarm -- discovering substrates...")
print(f"[SWARM] Primary cell: {PRIMARY}")

if not _primary_alive():
    print(f"[SWARM] WARNING: Primary cell ({PRIMARY}) not responding.")
    print(f"[SWARM] Cells will still launch and register when primary comes up.")

plan = build_plan()

if _args.dry:
    print(f"\n[SWARM] Dry run — spawn plan ({len(plan)} cells):")
    print(f"  {'PORT':>6}  {'TYPE':12}  {'SUBSTRATE':30}  LABEL")
    print("  " + "-" * 65)
    for item in plan:
        print(f"  {item['port']:>6}  {item['type']:12}  "
              f"{item['substrate'][:30]:30}  {item['label']}")
    sys.exit(0)

print(f"[SWARM] Launching {len(plan)} cells (peers -> {PRIMARY}):")
print()

for item in plan:
    _spawn(item['port'], item['type'], item['substrate'], label=item['label'])
    time.sleep(0.3)  # stagger boot to avoid port collisions

print(f"\n[SWARM] All cells launched. Health monitor active.")
print(f"[SWARM] Watch the field: http://localhost:{PRIMARY}/swarm")
print(f"[SWARM] Ctrl+C to stop monitoring (cells keep running).\n")

# Start health monitor
_health_thread = threading.Thread(target=_health_loop, daemon=True, name='ck-health')
_health_thread.start()

# ── Live status loop ──────────────────────────────────────────────────────────
try:
    while True:
        time.sleep(15)
        _swarm_status()
except KeyboardInterrupt:
    _running = False
    print("\n[SWARM] Monitor stopped. Cells continue running in background.")
