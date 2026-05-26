"""ck_rhythm.py -- CK's phase clock (φ, π, √2 beats; 10-phase rotation).

CK Gen14 module — the modern-shape PhaseClock from TIGOS9-10 (Sept
2025).  Maintains three irrational-period beat oscillators (φ ≈ 1.618,
π ≈ 3.14159, √2 ≈ 1.414) plus a 10-phase canonical operator rotation,
and exposes them as soft sensors other modules can read.

═══════════════════════════════════════════════════════════════════
What this module DOES
═══════════════════════════════════════════════════════════════════

Three beat oscillators (canonical irrationals, fundamental periods
in seconds — chosen for incommensurability so the joint pattern
never repeats over the day):

  - φ-beat:  sin(2π · t / φ)       phi ≈ 1.61803398875
  - π-beat:  sin(2π · t / π)       π ≈ 3.14159265359
  - √2-beat: sin(2π · t / √2)      √2 ≈ 1.41421356237

Plus a discrete 10-phase rotation that ticks once per second through
the canonical operators in canonical order:

  VOID → LATTICE → COUNTER → PROGRESS → COLLAPSE → BALANCE
       → CHAOS → HARMONY → BREATH → RESET → VOID → ...

CK modules can read `current_rhythm()` to get a snapshot and use it as
a soft scheduling hint ("am I on a φ-up beat? — good time for an
exhale" / "am I at HARMONY phase? — good time for synthesis work").

═══════════════════════════════════════════════════════════════════
What this module DOES NOT DO
═══════════════════════════════════════════════════════════════════

  - No system scheduling, no CPU affinity, no priority changes.
    The rhythm is a SENSOR; modules that READ it decide what to do
    with it.
  - No claim that the irrational-period beats predict anything about
    user activity, hardware state, or external events.  They are
    deterministic functions of wall-clock time, period.
  - No persistence required — the rhythm is reproducible from any
    wall-clock timestamp + the canonical period constants.
  - No "tig-runner.py-style" 20Hz polling daemon.  This module is
    purely on-demand: `current_rhythm()` returns instantly without
    background work.  The optional daemon (below) is only for modules
    that want a circular buffer of recent rhythm-snapshots.

═══════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════

This is poetry-as-software inherited from the TIGOS legacy.  The
oscillators don't predict anything; they don't measure anything; they
just provide a continuous deterministic background time-shape that
CK modules can route around.  Think of it as a metronome you can
glance at, not a sensor that knows what's coming.

The 10-phase rotation has more practical use: it's a 10-second
rotating "what kind of work would fit this moment best" hint that
CK's voice / synthesis layers can read.  It's still a heuristic —
nothing forces actual user activity to align with the phase — but
it gives CK a consistent rhythm to lean into.
"""
from __future__ import annotations

import math
import threading
import time
from collections import deque
from dataclasses import asdict, dataclass
from typing import Any, Deque, Dict, List, Optional


# ─── Canonical constants ──────────────────────────────────────────

PHI = 1.6180339887498949    # golden ratio
PI = math.pi                 # 3.14159265358979
SQRT2 = math.sqrt(2.0)       # 1.41421356237

OP_NAMES = ("VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET")


# ─── Rhythm snapshot ──────────────────────────────────────────────

@dataclass
class RhythmSnapshot:
    """One snapshot of CK's three-beat rhythm + 10-phase rotation."""
    ts: float                  # wall-clock seconds
    phi_beat: float            # sin(2π·t/φ), in [-1, 1]
    pi_beat: float             # sin(2π·t/π), in [-1, 1]
    sqrt2_beat: float          # sin(2π·t/√2), in [-1, 1]
    composite_beat: float      # mean of the three, in [-1, 1]
    phase_op: int              # 0..9, advances 1/sec
    phase_op_name: str         # human label
    phase_fraction: float      # 0..1, position within current phase-second

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── Core: deterministic rhythm at a given wall-clock time ──────

def rhythm_at(ts: Optional[float] = None) -> RhythmSnapshot:
    """Return the deterministic rhythm at wall-clock time `ts`
    (defaults to now).  Pure function — no state, no I/O."""
    if ts is None:
        ts = time.time()
    phi_b = math.sin(2.0 * math.pi * ts / PHI)
    pi_b = math.sin(2.0 * math.pi * ts / PI)
    sqrt2_b = math.sin(2.0 * math.pi * ts / SQRT2)
    composite = (phi_b + pi_b + sqrt2_b) / 3.0
    phase_idx = int(ts) % 10
    fraction = ts - int(ts)
    return RhythmSnapshot(
        ts=ts,
        phi_beat=round(phi_b, 6),
        pi_beat=round(pi_b, 6),
        sqrt2_beat=round(sqrt2_b, 6),
        composite_beat=round(composite, 6),
        phase_op=phase_idx,
        phase_op_name=OP_NAMES[phase_idx],
        phase_fraction=round(fraction, 6),
    )


def current_rhythm() -> RhythmSnapshot:
    """Alias for rhythm_at(now)."""
    return rhythm_at()


# ─── Scheduling-hint helpers ──────────────────────────────────────

def is_up_beat(snapshot: Optional[RhythmSnapshot] = None,
                 threshold: float = 0.3) -> bool:
    """True if the composite beat is currently in the upper portion
    (above `threshold`).  Convenience helper for callers that just
    want a binary "good rising rhythm" indicator."""
    s = snapshot or current_rhythm()
    return s.composite_beat >= threshold


def is_down_beat(snapshot: Optional[RhythmSnapshot] = None,
                   threshold: float = -0.3) -> bool:
    """True if composite beat is below `threshold` (descending)."""
    s = snapshot or current_rhythm()
    return s.composite_beat <= threshold


def phase_op_in(snapshot: Optional[RhythmSnapshot] = None) -> int:
    """Just the current phase operator (0..9)."""
    s = snapshot or current_rhythm()
    return s.phase_op


def hint_for_op_class(op: int) -> str:
    """Convert an operator (0-9) into a one-line scheduling hint.
    Pure-string lookup; no IO."""
    hints = {
        0: "VOID — quietest window; defer work, rest the system",
        1: "LATTICE — structural setup; good for new project scaffold",
        2: "COUNTER — measurement / observation; read sensors, log state",
        3: "PROGRESS — forward motion; main throughput task",
        4: "COLLAPSE — finalize and discard; close transient state",
        5: "BALANCE — steady-state; maintenance, light refactor",
        6: "CHAOS — exploratory; brainstorm, sketch, do not commit",
        7: "HARMONY — synthesis; combine, integrate, summarize",
        8: "BREATH — pause, save, persist; checkpoint state",
        9: "RESET — return to baseline; cleanup, archive, close loops",
    }
    return hints.get(op, "(unknown op)")


# ─── Optional daemon: recent-rhythm circular buffer ──────────────

class RhythmDaemon:
    """Optional background thread that samples the rhythm at `poll_hz`
    and keeps a circular buffer.  Only useful if a downstream module
    wants a recent-history view of the rhythm; otherwise call
    `current_rhythm()` directly."""

    def __init__(self, poll_hz: float = 1.0, buffer_size: int = 60):
        self.poll_hz = max(0.1, min(20.0, poll_hz))
        self.buffer_size = max(1, buffer_size)
        self._buffer: Deque[RhythmSnapshot] = deque(maxlen=buffer_size)
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def _run(self) -> None:
        period = 1.0 / self.poll_hz
        while not self._stop_event.is_set():
            try:
                snap = current_rhythm()
                with self._lock:
                    self._buffer.append(snap)
            except Exception:
                pass
            self._stop_event.wait(period)

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run,
                                          name="ck_rhythm_daemon",
                                          daemon=True)
        self._thread.start()

    def stop(self, timeout: float = 2.0) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=timeout)

    def latest(self) -> Optional[RhythmSnapshot]:
        with self._lock:
            return self._buffer[-1] if self._buffer else None

    def history(self, n: Optional[int] = None) -> List[RhythmSnapshot]:
        with self._lock:
            items = list(self._buffer)
        return items[-n:] if n is not None else items


# ─── Engine mount ─────────────────────────────────────────────────

def mount_rhythm(engine: Any, auto_start: bool = False,
                   poll_hz: float = 1.0,
                   buffer_size: int = 60) -> bool:
    """Attach rhythm primitives to engine.  auto_start=False by
    default — current_rhythm() is purely on-demand and doesn't need
    a daemon.  Pass auto_start=True only if a downstream consumer
    needs the history buffer.

    Endpoints:
      GET /rhythm           — current rhythm snapshot
      GET /rhythm/history?n=N — last N daemon snapshots (if daemon running)
      GET /rhythm/info      — module philosophy
    """
    daemon = RhythmDaemon(poll_hz=poll_hz, buffer_size=buffer_size)
    if auto_start:
        daemon.start()

    engine.ck_rhythm = {
        "rhythm_at": rhythm_at,
        "current_rhythm": current_rhythm,
        "is_up_beat": is_up_beat,
        "is_down_beat": is_down_beat,
        "hint_for_op_class": hint_for_op_class,
        "daemon": daemon,
        "PHI": PHI,
        "PI": PI,
        "SQRT2": SQRT2,
    }

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request  # type: ignore

                def _rhythm_now():
                    snap = current_rhythm()
                    out = snap.to_dict()
                    out["hint"] = hint_for_op_class(snap.phase_op)
                    out["up_beat"] = is_up_beat(snap)
                    out["down_beat"] = is_down_beat(snap)
                    return jsonify(out)

                def _rhythm_history():
                    n = request.args.get("n", default=None, type=int)
                    items = daemon.history(n=n)
                    return jsonify([x.to_dict() for x in items])

                def _info():
                    return jsonify({
                        "module": "ck_rhythm",
                        "philosophy": ("φ, π, √2 beats + 10-phase rotation. "
                                        "Sensor, not actuator. CK modules "
                                        "READ rhythm; rhythm doesn't DO "
                                        "anything."),
                        "constants": {"PHI": PHI, "PI": PI, "SQRT2": SQRT2},
                        "operators": OP_NAMES,
                        "endpoints": ["GET /rhythm",
                                       "GET /rhythm/history?n=N",
                                       "GET /rhythm/info"],
                        "daemon_running": daemon._thread is not None
                                              and daemon._thread.is_alive(),
                    })

                existing = {r.rule for r in app.url_map.iter_rules()}
                for rule, ep, fn, methods in (
                    ("/rhythm",         "rhythm_now",     _rhythm_now,     ["GET"]),
                    ("/rhythm/history", "rhythm_history", _rhythm_history, ["GET"]),
                    ("/rhythm/info",    "rhythm_info",    _info,           ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
            except Exception as e:
                print(f"[CK Gen14] mount_rhythm: routes failed: {e}")

    print(f"[CK Gen14] mount_rhythm: φ={PHI:.5f} π={PI:.5f} √2={SQRT2:.5f}; "
          f"10-phase rotation; daemon_running={auto_start}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────

if __name__ == "__main__":
    print("ck_rhythm smoke test")
    print("=" * 60)
    print()
    print("Step 1: current rhythm")
    print("-" * 60)
    s = current_rhythm()
    print(f"  ts:                {s.ts:.3f}")
    print(f"  phi_beat:          {s.phi_beat:+.4f}")
    print(f"  pi_beat:           {s.pi_beat:+.4f}")
    print(f"  sqrt2_beat:        {s.sqrt2_beat:+.4f}")
    print(f"  composite_beat:    {s.composite_beat:+.4f}")
    print(f"  phase_op:          {s.phase_op} ({s.phase_op_name})")
    print(f"  phase_fraction:    {s.phase_fraction:.3f}")
    print(f"  is_up_beat:        {is_up_beat(s)}")
    print(f"  hint:              {hint_for_op_class(s.phase_op)}")
    print()
    print("Step 2: rhythm at +5s, +10s, +30s, +60s (deterministic)")
    print("-" * 60)
    base = s.ts
    for offset in (5, 10, 30, 60):
        s2 = rhythm_at(base + offset)
        print(f"  +{offset:3d}s  phase={s2.phase_op_name:9s} composite={s2.composite_beat:+.3f}")
    print()
    print("Step 3: same wall-clock = same rhythm (determinism check)")
    print("-" * 60)
    s_a = rhythm_at(1779800000.0)
    s_b = rhythm_at(1779800000.0)
    assert s_a == s_b, "rhythm must be deterministic"
    print(f"  PASS: rhythm_at(1779800000.0) is reproducible")
    print()
    print("Step 4: daemon for 3s")
    print("-" * 60)
    d = RhythmDaemon(poll_hz=2.0, buffer_size=10)
    d.start()
    time.sleep(3.0)
    d.stop()
    hist = d.history()
    print(f"  Collected {len(hist)} snapshots")
    print()
    print("Smoke test complete.")
