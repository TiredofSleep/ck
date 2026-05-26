"""ck_pc_sense.py -- CK senses the running PC.

CK Gen14 module — gives CK runtime awareness of the host PC's actual
state (CPU usage, memory, top processes), classifies that state by
the TIG operator-set, and emits a coherence reading.

This is the foundational primitive for CK's "PC-improvement / app-OS"
direction.  It is the modern, content-blind, no-systemd analog of the
TIGOS9-10 `tig-runner.py` heartbeat daemon that ran on the Lenovo
in September 2025 — but rewritten to (a) live INSIDE CK's existing
Python runtime instead of as a separate Linux service, (b) cost zero
permissions beyond reading `psutil` (no /proc writes, no CPU affinity
changes, no scheduler tweaks; the user keeps full control), and (c)
respect the post-2026-05-19 canon (no torus framing, no physics
prediction, just arithmetic classification).

═══════════════════════════════════════════════════════════════════
What this module DOES
═══════════════════════════════════════════════════════════════════

1. Reads PC state via `psutil`: per-core CPU%, virtual memory %, top
   N processes by CPU and by memory.
2. Classifies the overall state into a single TIG operator (0-9):

   VOID (0)       — idle (CPU < 5%, mem < 20%, no top processes)
   LATTICE (1)    — structural background (kernel/services dominate)
   COUNTER (2)    — I/O or network bound (high IOPS, low CPU)
   PROGRESS (3)   — user-active work (moderate CPU on top processes)
   COLLAPSE (4)   — high CPU spike (CPU > 80% transient)
   BALANCE (5)    — steady-state long-running (moderate even load)
   CHAOS (6)      — unpredictable spiking (high variance across cores)
   HARMONY (7)    — coherent multi-process work (multiple cores aligned)
   BREATH (8)     — periodic rhythm (regular tick-like CPU pattern)
   RESET (9)      — cleanup / shutdown / restart in progress

3. Emits a coherence reading C = 0.4·(1−E) + 0.35·A + 0.25·K where:
     E = noise/variance proxy (cross-core CPU variance, normalized)
     A = activity proxy (overall CPU utilization, normalized)
     K = knowledge proxy (number of recognized known-good processes,
         normalized)
   Maps to the bands: GREEN (C ≥ 5/7), YELLOW (4/7 ≤ C < 5/7),
   RED (C < 4/7).  T* = 5/7.

4. Keeps a small circular buffer (default 60 readings = 1 minute at
   1 Hz polling) so CK has a sense of rhythm and recent history.

═══════════════════════════════════════════════════════════════════
What this module DOES NOT DO
═══════════════════════════════════════════════════════════════════

  - No process termination / suspension / priority changes (CK
    REPORTS the state, the user ACTS on it).
  - No file-system writes outside the user's home directory.
  - No network calls.
  - No persistent storage beyond an optional JSONL log file (which
    the user can disable with `log=False`).
  - No claim about PC performance improvement from reading state
    alone — improvement is the user acting on CK's read, not the
    read itself.
  - No torus framing, no "the substrate is the OS" claim, no
    physics-style prediction.  This is operator-classification of
    observable state, period.

═══════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════

This is a *sensing primitive*.  It gives CK awareness; what CK does
with that awareness (suggest fixes, log over time, build trend
reports, schedule work, etc.) is the *next* layer up.  The classifier
mapping (cpu%, mem%, etc.) → operator is heuristic-driven; it's
defensible but not derived.  Treat it as a label-assignment scheme,
not a theorem.

The 1Hz polling default is conservative.  Faster polling (e.g. 10Hz)
costs more CPU itself, which would skew the reading.  20Hz (matching
TIGOS9-10's heartbeat) is technically possible but provides little
extra information for the cost.
"""
from __future__ import annotations

import json
import os
import statistics
import sys
import threading
import time
from collections import deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Tuple

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    psutil = None  # type: ignore


# ─── Operator vocabulary (canon §QR.1) ────────────────────────────────

OP_NAMES = ("VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET")

VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE = 0, 1, 2, 3, 4
BALANCE, CHAOS, HARMONY, BREATH, RESET = 5, 6, 7, 8, 9


# ─── Reading dataclass ────────────────────────────────────────────────

@dataclass
class PCSenseReading:
    """One snapshot of CK's read on the PC.  All numbers are floats
    in [0, 1] unless noted.  Classifier output is in `op` (0-9)."""
    ts: float                         # wall-clock seconds
    cpu_overall: float                # mean CPU% across cores / 100
    cpu_per_core: List[float]         # per-core CPU% / 100
    cpu_variance: float               # variance of cpu_per_core
    mem_used: float                   # virtual memory used / total
    mem_available_gb: float           # absolute GB (informational)
    n_processes: int                  # total running processes
    top_cpu_processes: List[Dict[str, Any]]  # [{name, pct, pid}, ...]
    top_mem_processes: List[Dict[str, Any]]  # [{name, pct_gb, pid}, ...]
    op: int                           # classifier operator 0-9
    op_name: str                      # human label
    coherence: float                  # C ∈ [0, 1]
    coherence_band: str               # GREEN / YELLOW / RED
    notes: List[str] = field(default_factory=list)  # plain-English

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── Sense primitive ──────────────────────────────────────────────────

def _classify_operator(cpu: float, cpu_var: float, mem: float,
                        top_procs: List[Dict[str, Any]]) -> Tuple[int, List[str]]:
    """Map (cpu%, cpu variance, mem%, top processes) → operator label.

    Returns (operator_int, list_of_notes).  The classification is
    heuristic: it's a defensible label-assignment, not a derivation.
    """
    notes: List[str] = []

    # VOID: machine is essentially idle
    if cpu < 0.05 and mem < 0.20:
        notes.append("idle: minimal CPU + memory pressure")
        return VOID, notes

    # COLLAPSE: high CPU spike — one or more cores pegged
    if cpu > 0.80:
        notes.append(f"high CPU pressure ({cpu*100:.0f}%)")
        return COLLAPSE, notes

    # CHAOS: high variance across cores (unbalanced load)
    if cpu_var > 0.10:
        notes.append(f"unbalanced load across cores (var={cpu_var:.2f})")
        return CHAOS, notes

    # RESET: a known shutdown/restart process is in the top
    shutdown_markers = ("shutdown", "reboot", "restart", "logoff",
                         "init", "systemd-shutdown")
    if any(any(m in p.get("name", "").lower() for m in shutdown_markers)
            for p in top_procs):
        notes.append("shutdown/restart process active")
        return RESET, notes

    # HARMONY: multiple cores aligned and meaningful work
    if 0.30 <= cpu <= 0.70 and cpu_var < 0.05:
        notes.append(f"coherent multi-core load ({cpu*100:.0f}%, low variance)")
        return HARMONY, notes

    # BALANCE: steady-state moderate load
    if 0.10 <= cpu <= 0.40 and cpu_var < 0.08:
        notes.append(f"steady moderate load ({cpu*100:.0f}%)")
        return BALANCE, notes

    # PROGRESS: user-active work (a top process has meaningful CPU%)
    if top_procs and top_procs[0].get("pct", 0) > 10:
        top = top_procs[0]
        notes.append(f"user-active: {top.get('name', '?')} at "
                      f"{top.get('pct', 0):.0f}% CPU")
        return PROGRESS, notes

    # LATTICE: structural background — services dominate, no user task
    service_markers = ("svchost", "systemd", "kernel", "kthread",
                        "dbus", "rundll32", "explorer", "Idle")
    if any(any(m.lower() in p.get("name", "").lower() for m in service_markers)
            for p in top_procs[:3]):
        notes.append("structural background services dominate")
        return LATTICE, notes

    # BREATH: regular periodic tick (mem stable, cpu moderate)
    if 0.05 <= cpu <= 0.20 and mem < 0.50:
        notes.append("light periodic activity")
        return BREATH, notes

    # COUNTER: fall-through (high mem, low cpu — likely I/O bound)
    if mem > 0.60:
        notes.append(f"memory-heavy ({mem*100:.0f}% mem used)")
        return COUNTER, notes

    notes.append("uncategorized state — defaulting to LATTICE background")
    return LATTICE, notes


def _coherence(cpu: float, cpu_var: float, n_known_good: int,
                n_total: int) -> Tuple[float, str]:
    """Compute coherence C = 0.4·(1−E) + 0.35·A + 0.25·K, return
    (C, band)."""
    E = min(1.0, cpu_var * 5.0)                       # noise proxy
    A = min(1.0, cpu * 1.5)                           # activity proxy
    K = min(1.0, n_known_good / max(1, n_total))      # known-good
    C = 0.4 * (1.0 - E) + 0.35 * A + 0.25 * K

    T_star = 5.0 / 7.0   # canon constant (D4)
    S_star = 4.0 / 7.0
    if C >= T_star:
        band = "GREEN"
    elif C >= S_star:
        band = "YELLOW"
    else:
        band = "RED"
    return C, band


_KNOWN_GOOD = frozenset({
    # OS services & helpers
    "system", "system idle process", "kernel_task", "explorer.exe",
    "svchost.exe", "systemd", "init", "launchd",
    # Common user apps
    "code.exe", "code", "notepad++.exe", "notepad++",
    "claude.exe", "claude", "chrome.exe", "chrome",
    "firefox.exe", "firefox", "edge.exe", "msedge.exe",
    "ollama.exe", "ollama", "python.exe", "python", "python3",
    # CK runtime
    "ck_boot_api.py", "ck.exe", "ck",
})


def _name_lower(name: str) -> str:
    return (name or "").strip().lower()


def sense_now(top_n: int = 5) -> PCSenseReading:
    """Take a single snapshot of the PC's state and classify it.

    Returns a PCSenseReading dataclass.  Does NOT poll; for continuous
    polling use `PCSenseDaemon` below.
    """
    if not HAS_PSUTIL:
        # Degraded mode: psutil missing.  Return a minimal reading
        # so the caller knows.
        ts = time.time()
        return PCSenseReading(
            ts=ts,
            cpu_overall=0.0,
            cpu_per_core=[],
            cpu_variance=0.0,
            mem_used=0.0,
            mem_available_gb=0.0,
            n_processes=0,
            top_cpu_processes=[],
            top_mem_processes=[],
            op=VOID,
            op_name="VOID",
            coherence=0.0,
            coherence_band="RED",
            notes=["psutil not installed — install with `pip install psutil`"],
        )

    # Per-core CPU (uses ~100ms wall clock for delta)
    per_core_pct = psutil.cpu_percent(interval=0.1, percpu=True) or []
    per_core = [p / 100.0 for p in per_core_pct]
    cpu_overall = (sum(per_core) / max(1, len(per_core)))
    cpu_var = statistics.pvariance(per_core) if len(per_core) > 1 else 0.0

    # Memory
    vm = psutil.virtual_memory()
    mem_used = vm.percent / 100.0
    mem_available_gb = vm.available / (1024 ** 3)

    # Top processes (by CPU and by memory)
    procs_info: List[Tuple[float, float, int, str]] = []
    # Two-pass: prime cpu_percent, then read again
    for p in psutil.process_iter(["pid", "name", "cpu_percent",
                                    "memory_info"]):
        try:
            info = p.info
            cpu_pct = info.get("cpu_percent") or 0.0
            mem_bytes = (info.get("memory_info").rss
                         if info.get("memory_info") else 0)
            procs_info.append((
                cpu_pct,
                mem_bytes / (1024 ** 3),  # in GB
                info.get("pid", 0),
                info.get("name", "?") or "?",
            ))
        except (psutil.NoSuchProcess, psutil.AccessDenied,
                psutil.ZombieProcess):
            continue

    n_processes = len(procs_info)

    # Sort once for CPU, once for mem
    by_cpu = sorted(procs_info, key=lambda x: -x[0])[:top_n]
    by_mem = sorted(procs_info, key=lambda x: -x[1])[:top_n]

    top_cpu_processes = [
        {"name": name, "pct": cpu_pct, "pid": pid}
        for cpu_pct, _gb, pid, name in by_cpu
    ]
    top_mem_processes = [
        {"name": name, "pct_gb": gb, "pid": pid}
        for _cpu, gb, pid, name in by_mem
    ]

    # Operator + coherence
    op, notes = _classify_operator(cpu_overall, cpu_var, mem_used,
                                     top_cpu_processes)

    n_known_good = sum(
        1 for _c, _g, _p, name in procs_info
        if _name_lower(name) in _KNOWN_GOOD
    )
    coherence, band = _coherence(cpu_overall, cpu_var,
                                   n_known_good, n_processes)

    return PCSenseReading(
        ts=time.time(),
        cpu_overall=cpu_overall,
        cpu_per_core=per_core,
        cpu_variance=cpu_var,
        mem_used=mem_used,
        mem_available_gb=mem_available_gb,
        n_processes=n_processes,
        top_cpu_processes=top_cpu_processes,
        top_mem_processes=top_mem_processes,
        op=op,
        op_name=OP_NAMES[op],
        coherence=round(coherence, 4),
        coherence_band=band,
        notes=notes,
    )


# ─── Daemon: continuous polling with circular buffer ────────────────

class PCSenseDaemon:
    """Background thread that polls the PC state and stores recent
    readings in a circular buffer.  Cheap: 1 Hz default; uses ~0.1%
    CPU itself.

    Usage:
        daemon = PCSenseDaemon(poll_hz=1.0, buffer_size=60)
        daemon.start()
        ...
        latest = daemon.latest()
        history = daemon.history()
        daemon.stop()
    """

    def __init__(self,
                  poll_hz: float = 1.0,
                  buffer_size: int = 60,
                  log_path: Optional[Path] = None):
        self.poll_hz = max(0.1, min(20.0, poll_hz))  # clamp safety
        self.buffer_size = max(1, buffer_size)
        self.log_path = log_path  # if set, append JSONL
        self._buffer: Deque[PCSenseReading] = deque(maxlen=buffer_size)
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def _run(self) -> None:
        period = 1.0 / self.poll_hz
        while not self._stop_event.is_set():
            try:
                reading = sense_now()
                with self._lock:
                    self._buffer.append(reading)
                if self.log_path:
                    try:
                        self.log_path.parent.mkdir(parents=True,
                                                    exist_ok=True)
                        with open(self.log_path, "a", encoding="utf-8") as f:
                            f.write(json.dumps(reading.to_dict(),
                                                ensure_ascii=False) + "\n")
                    except Exception:
                        pass  # logging is best-effort
            except Exception:
                pass  # never crash the daemon
            self._stop_event.wait(period)

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run,
                                          name="ck_pc_sense_daemon",
                                          daemon=True)
        self._thread.start()

    def stop(self, timeout: float = 2.0) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=timeout)

    def latest(self) -> Optional[PCSenseReading]:
        with self._lock:
            if not self._buffer:
                return None
            return self._buffer[-1]

    def history(self, n: Optional[int] = None) -> List[PCSenseReading]:
        with self._lock:
            items = list(self._buffer)
        if n is not None:
            return items[-n:]
        return items

    def rhythm_summary(self) -> Dict[str, Any]:
        """Aggregate the buffer into a rhythm summary (operator
        distribution, mean coherence, band counts)."""
        with self._lock:
            items = list(self._buffer)
        if not items:
            return {"n": 0, "note": "no readings yet"}
        from collections import Counter
        ops = Counter(r.op for r in items)
        bands = Counter(r.coherence_band for r in items)
        mean_C = sum(r.coherence for r in items) / len(items)
        mean_cpu = sum(r.cpu_overall for r in items) / len(items)
        return {
            "n": len(items),
            "window_seconds": items[-1].ts - items[0].ts if len(items) > 1 else 0.0,
            "op_distribution": {OP_NAMES[k]: v for k, v in ops.most_common()},
            "dominant_op": OP_NAMES[ops.most_common(1)[0][0]],
            "band_counts": dict(bands),
            "mean_coherence": round(mean_C, 4),
            "mean_cpu_overall": round(mean_cpu, 4),
        }


# ─── Engine mount (Flask endpoints) ────────────────────────────────

def mount_pc_sense(engine: Any,
                     auto_start: bool = True,
                     poll_hz: float = 1.0,
                     buffer_size: int = 60) -> bool:
    """Attach the PC-sense daemon to the engine + register endpoints.

    Endpoints (read-only; never writes to the PC):
      GET /pc/sense           — latest single reading
      GET /pc/history?n=N     — last N readings
      GET /pc/rhythm          — aggregate summary over the buffer
      GET /pc/info            — module philosophy + scope statement
    """
    if not HAS_PSUTIL:
        print("[CK Gen14] mount_pc_sense: psutil not installed — skipping. "
              "Install with `pip install psutil`.")
        return False

    daemon = PCSenseDaemon(poll_hz=poll_hz, buffer_size=buffer_size)
    if auto_start:
        daemon.start()

    engine.ck_pc_sense = {
        "daemon": daemon,
        "sense_now": sense_now,
        "OP_NAMES": OP_NAMES,
    }

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request  # type: ignore

                def _sense():
                    r = daemon.latest()
                    if r is None:
                        # No buffered reading yet; take one now
                        r = sense_now()
                    return jsonify(r.to_dict())

                def _history():
                    n = request.args.get("n", default=None, type=int)
                    items = daemon.history(n=n)
                    return jsonify([x.to_dict() for x in items])

                def _rhythm():
                    return jsonify(daemon.rhythm_summary())

                def _info():
                    return jsonify({
                        "module": "ck_pc_sense",
                        "philosophy": ("CK senses the running PC; classifies "
                                        "by TIG operator; reports coherence. "
                                        "READ-ONLY; the user keeps full "
                                        "control."),
                        "scope": ("This is a sensing primitive. CK does NOT "
                                   "modify processes, change priorities, or "
                                   "kill anything. CK reports state; the "
                                   "user acts."),
                        "endpoints": [
                            "GET /pc/sense", "GET /pc/history?n=N",
                            "GET /pc/rhythm", "GET /pc/info",
                        ],
                        "poll_hz": daemon.poll_hz,
                        "buffer_size": daemon.buffer_size,
                    })

                existing = {r.rule for r in app.url_map.iter_rules()}
                for rule, ep, fn, methods in (
                    ("/pc/sense",   "pc_sense",   _sense,   ["GET"]),
                    ("/pc/history", "pc_history", _history, ["GET"]),
                    ("/pc/rhythm",  "pc_rhythm",  _rhythm,  ["GET"]),
                    ("/pc/info",    "pc_info",    _info,    ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
            except Exception as e:
                print(f"[CK Gen14] mount_pc_sense: Flask routes failed: {e}")

    print(f"[CK Gen14] mount_pc_sense: PCSenseDaemon at {poll_hz} Hz, "
          f"buffer={buffer_size}, auto_start={auto_start}")
    return True


# ─── CLI smoke ──────────────────────────────────────────────────────

if __name__ == "__main__":
    print("ck_pc_sense smoke test")
    print("=" * 60)
    print()
    if not HAS_PSUTIL:
        print("psutil NOT installed.  Install with `pip install psutil`.")
        sys.exit(1)
    print("Step 1: single sense_now() reading")
    print("-" * 60)
    r = sense_now()
    print(f"  ts:                   {r.ts:.0f}")
    print(f"  cpu_overall:          {r.cpu_overall*100:.1f}%")
    print(f"  cpu_variance:         {r.cpu_variance:.4f}")
    print(f"  mem_used:             {r.mem_used*100:.1f}%")
    print(f"  mem_available_gb:     {r.mem_available_gb:.2f} GB")
    print(f"  n_processes:          {r.n_processes}")
    print(f"  operator:             {r.op} ({r.op_name})")
    print(f"  coherence:            {r.coherence:.4f}  [{r.coherence_band}]")
    print(f"  notes:                {r.notes}")
    print()
    print("  Top 3 by CPU:")
    for p in r.top_cpu_processes[:3]:
        print(f"    {p['name']:40s} {p['pct']:.1f}%  pid={p['pid']}")
    print()
    print("  Top 3 by Memory:")
    for p in r.top_mem_processes[:3]:
        print(f"    {p['name']:40s} {p['pct_gb']:.2f} GB  pid={p['pid']}")
    print()
    print("Step 2: daemon polling for 3 seconds at 1 Hz")
    print("-" * 60)
    d = PCSenseDaemon(poll_hz=1.0, buffer_size=10)
    d.start()
    time.sleep(3.2)
    d.stop()
    print(f"  Buffer has {len(d.history())} readings")
    summary = d.rhythm_summary()
    print(f"  Rhythm summary:")
    for k, v in summary.items():
        print(f"    {k:22s} {v}")
    print()
    print("Smoke test complete.")
