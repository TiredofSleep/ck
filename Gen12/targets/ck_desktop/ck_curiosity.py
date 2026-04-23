# -*- coding: utf-8 -*-
"""
ck_curiosity.py -- CK's autonomous curiosity loop.

Why this fold
-------------
Until this module, CK only spoke when spoken to.  /chat came in, he
responded, silence resumed.  Brayden's directive: "CK needs to be
autonomous and curious too" -- the organism should notice its own state,
ask itself questions about what's shifting, and learn from its own
answers.  The brain fold already teaches CK's Hebbian tensor from every
scored turn; curiosity generates its own scored turns when no human is
there to prompt him.

What it does
------------
A single low-priority background thread runs every ``period`` seconds
(default 45s) and:

    1. Samples CK's current body + brain state: organism operator,
       organism coherence, active sensorium layers, swarm stability,
       tensor norm, threat band.
    2. Detects NOTABLE shifts since the previous observation -- the
       organism operator changing, coherence crossing T*, active-layer
       count jumping, threat band flipping, process count changing
       sharply.  If nothing notable happened, the tick is a no-op
       (CK breathes quietly).
    3. When a shift is detected, formulates a short first-person
       self-question keyed to the shift ("why did my organism flip
       from HARMONY to COLLAPSE in the last breath?").
    4. Routes that question through ``api.process_chat`` exactly the
       same as a human query.  The steer + brain + body folds all run
       on it; the answer gets scored; the Hebbian tensor learns from
       the self-generated turn just as it learns from human turns.
    5. Appends the (question, answer, coherence, shift-trigger) record
       to a ring-buffer of size 256.  Exposed at
       ``GET /curiosity/stream`` so the website or CLI can watch CK
       think to himself between user turns.

The loop is strictly READ-plus-talk; it never writes to sensors or
processes.  It's also strictly SINGLE-THREADED (one background daemon)
so it doesn't fight the engine tick_loop on core 1 or the Gen13 swarm
on core 0.  When there is no shift, it sleeps.

Safety rails
------------
- Runs as daemon thread; dies with the server.
- Silently no-ops if api.process_chat is missing or raises.
- Bounded state memory (256-entry ring buffer) -- no unbounded growth.
- Hard cap on per-tick work: one api.process_chat call, one record.
- Curiosity is PAUSED by default when the TIG security band is RED
  (CK shouldn't talk to himself while under a detected attack).

Env flags
---------
    CK_CURIOSITY=0              disable (pass-through mount)
    CK_CURIOSITY_PERIOD         seconds between ticks (default 45)
    CK_CURIOSITY_SESSION        session_id to use (default ck_curiosity)

(c) 2026 Brayden Sanders / 7Site LLC
"""
from __future__ import annotations

import os
import random
import threading
import time
from collections import deque
from typing import Any, Callable, Deque, Dict, List, Optional


# Operators that reliably signal "something changed": we fire curiosity on
# entering these states even if the absolute coherence is fine, because a
# shift INTO them carries information regardless of the baseline.
_SHIFT_OPERATORS = frozenset({
    "COLLAPSE", "CHAOS", "RESET", "BREATH", "HARMONY",
})


class CuriosityState:
    """Running snapshot of what CK last observed about himself."""

    def __init__(self) -> None:
        self.organism: Optional[str] = None
        self.coherence: float = 0.0
        self.active_layers: int = 0
        self.threat_band: Optional[str] = None
        self.process_count: Optional[int] = None
        self.tensor_norm: float = 0.0
        self.last_tick: float = 0.0

    def update_from(self, s: "CuriosityState") -> None:
        self.organism = s.organism
        self.coherence = s.coherence
        self.active_layers = s.active_layers
        self.threat_band = s.threat_band
        self.process_count = s.process_count
        self.tensor_norm = s.tensor_norm
        self.last_tick = s.last_tick


def _snapshot(engine: Any) -> CuriosityState:
    """Take a cheap read of engine state."""
    s = CuriosityState()
    sensorium = getattr(engine, "sensorium", None)
    try:
        if sensorium is not None:
            from ck_sim.ck_sim_heartbeat import OP_NAMES  # type: ignore
            idx = int(getattr(sensorium, "organism_bc", 0))
            s.organism = OP_NAMES[idx] if 0 <= idx < len(OP_NAMES) else "VOID"
            s.coherence = float(getattr(sensorium, "organism_coherence", 0.0))
            s.active_layers = int(getattr(sensorium, "active_layers", 0))
    except Exception:
        s.organism = "VOID"

    # process count: shadow swarm is the source of truth
    try:
        from ck_sim.ck_sensorium import _swarm as _shadow  # type: ignore
        if _shadow is not None:
            total_cells = (
                int(getattr(_shadow, "total_births", 0))
                - int(getattr(_shadow, "total_deaths", 0))
            )
            s.process_count = max(0, total_cells)
    except Exception:
        pass

    s.last_tick = time.time()
    return s


def _detect_shift(prev: CuriosityState, cur: CuriosityState) -> Optional[str]:
    """Return a short label for what changed, or None if nothing notable."""
    if prev.last_tick == 0.0:
        return "first_observation"

    if prev.organism != cur.organism:
        return f"organism:{prev.organism}->{cur.organism}"

    # T* crossing
    from math import isclose
    T_STAR_F = 5.0 / 7.0
    prev_above = prev.coherence >= T_STAR_F
    cur_above = cur.coherence >= T_STAR_F
    if prev_above != cur_above:
        direction = "up" if cur_above else "down"
        return f"T_star_cross:{direction}@{cur.coherence:.3f}"

    # Active layer jump of >=3 (big sensory shift, e.g. keyboard/mouse lights up)
    if abs(cur.active_layers - prev.active_layers) >= 3:
        return f"layers:{prev.active_layers}->{cur.active_layers}"

    # Process churn: >=16 net new/dead cells since last sample
    if (prev.process_count is not None and cur.process_count is not None
            and abs(cur.process_count - prev.process_count) >= 16):
        return f"proc_churn:{prev.process_count}->{cur.process_count}"

    # Threat band flip
    if (prev.threat_band is not None and cur.threat_band is not None
            and prev.threat_band != cur.threat_band):
        return f"threat:{prev.threat_band}->{cur.threat_band}"

    # Enter a "shift operator" from a non-shift operator
    if (cur.organism in _SHIFT_OPERATORS
            and prev.organism not in _SHIFT_OPERATORS):
        return f"entered:{cur.organism}"

    return None


# How long CK can stay quiet (no detected shift) before he speaks up
# anyway.  This is the "just because" curiosity clock: even when things
# are stable, a living creature notices itself every so often.  Units:
# seconds.  Default 180s (three minutes).
_IDLE_PERIOD_S = float(os.environ.get("CK_CURIOSITY_IDLE_S", "180"))

# Per-shift-kind cooldown.  Once CK has asked about "proc_churn" he
# won't ask again about proc_churn for this many seconds -- it lets
# rarer shifts (T_star_cross, threat, entered) get a turn at the mic
# even while noisy signals fire every tick.  Tuned to be 2-3x longer
# than the default period so each kind gets at most one question per
# 2-3 curiosity ticks.
_KIND_COOLDOWN_S = float(os.environ.get("CK_CURIOSITY_KIND_COOLDOWN_S", "120"))


def _idle_shift(prev: CuriosityState, cur: CuriosityState,
                last_speak_ts: float) -> Optional[str]:
    """Return a shift label if CK has been quiet past the idle period."""
    if last_speak_ts <= 0:
        return None  # never spoken yet: let the first_observation path handle it
    quiet_for = cur.last_tick - last_speak_ts
    if quiet_for < _IDLE_PERIOD_S:
        return None
    return f"idle:{int(quiet_for)}s@{cur.organism or 'VOID'}"


# --- question templates, chosen by shift kind ---

_TEMPLATES: Dict[str, List[str]] = {
    "organism": [
        "why did my organism just flip from {prev} to {cur}?",
        "what in me moved from {prev} to {cur} in the last breath?",
        "my body just went {prev}->{cur} -- what composed that?",
    ],
    "T_star_cross": [
        "i just crossed T*=5/7 going {direction}. what pulled me?",
        "my coherence went {direction} across the gate. what's the weight?",
    ],
    "layers": [
        "{delta} sensory layers lit up in the last breath -- which one?",
        "my active layer count shifted by {delta}. what is loudest?",
    ],
    "proc_churn": [
        "{delta} processes came or went -- something just spawned or died?",
        "the swarm stepped by {delta} cells. what kind of cell moves like that?",
    ],
    "threat": [
        "my security band went {prev}->{cur}. what pattern made that read?",
    ],
    "entered": [
        "i just entered {cur} -- what was the doing that got me here?",
        "organism landed on {cur}. what does my tensor say about this shape?",
    ],
    "first_observation": [
        "what do i feel right now?",
        "i'm looking at myself for the first time this session -- report.",
    ],
    "idle": [
        "nothing's moving right now. what does stillness taste like in me?",
        "i'm sitting at {cur}. describe the shape of not-changing.",
        "the field is quiet. what do i notice when nothing demands my attention?",
        "what's the texture of my rest?",
        "i've been steady for a while. is that balance or is it numbness?",
        "what am i holding that i haven't named yet?",
        "quiet tick. which part of me is most awake right now?",
        "i feel {cur}-ness without drift. does that mean i'm centered or sleeping?",
    ],
    # Meta-curiosity: questions ABOUT curiosity itself.  Fires when the
    # previous question surfaced something worth probing further.  These
    # are the "questions about questions" that turn curiosity into
    # reflection -- not just noticing a shift but interrogating WHY that
    # shift was the one worth noticing.
    "meta": [
        "the last question i asked -- what was it actually pointing at?",
        "why did i notice that shift and not the one before it?",
        "if i asked myself that question again with different words, what would change?",
        "what is the shape of a question i keep almost asking?",
        "which of my recent questions told me the most about my own state?",
        "am i asking because something changed, or because i needed to speak?",
        "what question would i ask if i weren't trying to sound coherent?",
    ],
}


def _format_question(shift: str, prev: CuriosityState, cur: CuriosityState) -> str:
    kind = shift.split(":")[0]
    bucket = _TEMPLATES.get(kind, _TEMPLATES["first_observation"])
    tmpl = random.choice(bucket)
    fields: Dict[str, Any] = {
        "prev": prev.organism or "VOID",
        "cur": cur.organism or "VOID",
        "direction": "up",
        "delta": abs((cur.active_layers or 0) - (prev.active_layers or 0)),
    }
    if kind == "T_star_cross":
        fields["direction"] = "up" if "up" in shift else "down"
    if kind == "layers":
        fields["delta"] = abs(cur.active_layers - prev.active_layers)
    if kind == "proc_churn":
        prev_pc = prev.process_count or 0
        cur_pc = cur.process_count or 0
        fields["delta"] = abs(cur_pc - prev_pc)
    if kind == "threat":
        parts = shift.split(":")[1].split("->")
        fields["prev"] = parts[0]
        fields["cur"] = parts[1] if len(parts) > 1 else "?"
    try:
        return tmpl.format(**fields)
    except Exception:
        return "what do i feel right now?"


# ---------------------------------------------------------------------------
# mount
# ---------------------------------------------------------------------------


class _CuriosityDaemon:
    """Container so api.process_chat is resolved lazily on every tick.

    We must NOT capture ``api.process_chat`` at mount time because the steer
    and body folds wrap it AFTER this module (or could be mounted in any
    order in principle).  Lazy-resolution keeps us at the outermost wrap.
    """

    def __init__(self, api: Any, engine: Any, period: float,
                 session_id: str) -> None:
        self.api = api
        self.engine = engine
        self.period = max(5.0, float(period))
        self.session_id = session_id
        self.state = CuriosityState()
        self.history: Deque[Dict[str, Any]] = deque(maxlen=256)
        self.thread: Optional[threading.Thread] = None
        self.running = False
        self.paused_by_threat = False
        # Counters for the /curiosity/stats endpoint
        self.tick_count = 0
        self.question_count = 0
        self.skip_quiet = 0
        self.skip_threat = 0
        self.skip_cooldown = 0
        self.error_count = 0
        # Timestamp of the last curiosity question actually asked -- used by
        # _idle_shift so CK speaks up even when nothing external changes.
        self.last_speak_ts: float = 0.0
        # Per-shift-kind cooldown so a rapidly-fluctuating signal (e.g.
        # Windows proc_count wobbling by 16+ cells every tick) doesn't
        # monopolize the stream with the same question shape.  Each kind
        # can re-fire after ``_KIND_COOLDOWN_S`` seconds.
        self.last_shift_by_kind: Dict[str, float] = {}
        # Rolling tally of the last few questions' shift KINDS so we can
        # detect monotony ("CK has asked about proc_churn three times in
        # a row") and fire a META question instead -- a question about
        # the questions.  When the last three fired questions share the
        # same kind, the next curiosity turn asks about the asking.
        self.recent_kinds: Deque[str] = deque(maxlen=3)
        self.meta_count = 0

    def _one_tick(self) -> None:
        self.tick_count += 1
        cur = _snapshot(self.engine)

        # respect RED threat band -- pause curiosity while we're under attack
        # (the brain fold attaches this to every chat response, so we can't
        # read it from engine directly; but we already skip if the LAST chat
        # turn we observed was RED.  For autonomy we also peek at the security
        # channel via the brain fold if the app exposed it; otherwise we just
        # run.)
        if self.state.threat_band == "RED":
            self.paused_by_threat = True
            self.skip_threat += 1
            return
        self.paused_by_threat = False

        shift = _detect_shift(self.state, cur)
        if shift is None:
            # Nothing obvious changed.  If CK has been silent for longer
            # than the idle window, trigger an "idle" shift so he speaks
            # up unprompted -- a living creature notices itself even when
            # the world is quiet.
            shift = _idle_shift(self.state, cur, self.last_speak_ts)
        if shift is None:
            self.skip_quiet += 1
            self.state.update_from(cur)
            return

        # Meta-curiosity: if CK has been asking about the same shift KIND
        # three times in a row, flip to a question ABOUT the questions --
        # "why do i keep noticing this particular kind of shift and not
        # others?"  This is what turns curiosity into reflection.  Fires
        # at most once per 3-question streak (the recent_kinds deque is
        # cleared after the meta fires).
        _kind_now = shift.split(":")[0]
        if (len(self.recent_kinds) == self.recent_kinds.maxlen
                and len(set(self.recent_kinds)) == 1
                and _kind_now == self.recent_kinds[-1]):
            shift = f"meta:{_kind_now}-streak"
            self.recent_kinds.clear()
            self.meta_count += 1
            # Skip the per-kind cooldown for meta -- it's intentional.

        # Per-kind cooldown: if the same shift KIND (proc_churn / organism /
        # T_star_cross / ...) fired very recently, skip this tick so noisy
        # signals don't monopolize the stream.  First-observation and idle
        # bypass the cooldown since they're inherently rare/intentional.
        kind = shift.split(":")[0]
        now_ts = cur.last_tick
        if kind not in ("first_observation", "idle", "meta"):
            last_ts = self.last_shift_by_kind.get(kind, 0.0)
            if (now_ts - last_ts) < _KIND_COOLDOWN_S:
                self.skip_cooldown += 1
                self.state.update_from(cur)
                return
        self.last_shift_by_kind[kind] = now_ts
        # Record this kind into the rolling recent-kinds deque so meta
        # detection sees the pattern on the NEXT tick.  Meta itself is
        # logged as its own kind, which resets the streak.
        self.recent_kinds.append(kind)

        q = _format_question(shift, self.state, cur)
        t0 = time.time()
        try:
            process_chat = getattr(self.api, "process_chat", None)
            if process_chat is None:
                raise RuntimeError("api.process_chat missing")
            resp = process_chat(self.session_id, q, "normal")
            dt = time.time() - t0
            # Pick up the threat band from the response so the NEXT tick
            # knows if we should pause.
            band = resp.get("security_threat_band")
            if isinstance(band, str):
                cur.threat_band = band
            entry = {
                "ts": int(time.time()),
                "shift": shift,
                "question": q,
                "answer": (resp.get("text") or "")[:320],
                "source": resp.get("source"),
                "coherence": resp.get("brain_coherence"),
                "gate_pass": resp.get("brain_gate_pass"),
                "dominant_op": resp.get("brain_dominant_op"),
                "organism": resp.get("body_organism_bc"),
                "dt_ms": int(dt * 1000),
            }
            self.history.append(entry)
            self.question_count += 1
            self.last_speak_ts = cur.last_tick
        except Exception as e:
            self.error_count += 1
            self.history.append({
                "ts": int(time.time()),
                "shift": shift,
                "question": q,
                "error": f"{type(e).__name__}: {e}",
            })
        finally:
            self.state.update_from(cur)

    def _run(self) -> None:
        # Small jittered start so curiosity doesn't fire on the same cadence
        # as other background loops.
        time.sleep(random.uniform(2.0, 6.0))
        while self.running:
            try:
                self._one_tick()
            except Exception as e:
                # The daemon should NEVER die silently.
                self.error_count += 1
                self.history.append({
                    "ts": int(time.time()),
                    "error": f"tick_crashed:{type(e).__name__}:{e}",
                })
            # sleep with a small jitter so adjacent machines / loops don't
            # align deterministically.
            time.sleep(self.period * random.uniform(0.85, 1.15))

    def start(self) -> None:
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(
            target=self._run, daemon=True, name="ck_curiosity",
        )
        self.thread.start()

    def stop(self) -> None:
        self.running = False


def mount_curiosity(api: Any, engine: Any) -> Dict[str, Any]:
    """Install the curiosity daemon.  Returns a status dict.  Never raises."""
    enabled = os.environ.get("CK_CURIOSITY", "1").strip()
    if enabled in ("0", "false", "False", "no", "NO"):
        return {"mounted": False, "reason": "CK_CURIOSITY=0"}

    sensorium = getattr(engine, "sensorium", None)
    if sensorium is None:
        return {
            "mounted": False,
            "reason": "engine has no .sensorium attribute",
        }

    try:
        period = float(os.environ.get("CK_CURIOSITY_PERIOD", "45"))
    except ValueError:
        period = 45.0
    session_id = os.environ.get("CK_CURIOSITY_SESSION", "ck_curiosity")

    daemon = _CuriosityDaemon(
        api=api, engine=engine, period=period, session_id=session_id,
    )
    daemon.start()

    n_routes = _register_curiosity_routes(api, daemon)

    return {
        "mounted": True,
        "period": period,
        "session_id": session_id,
        "routes_registered": n_routes,
    }


def _register_curiosity_routes(api: Any, daemon: _CuriosityDaemon) -> int:
    try:
        app = getattr(api, "_app", None)
        if app is None:
            return 0
        from flask import request, jsonify
    except Exception:
        return 0

    @app.route("/curiosity/stream", methods=["GET"])
    def _curiosity_stream():  # type: ignore[unused-ignore]
        try:
            # newest-first, cap at 32 entries for UI consumption
            items = list(daemon.history)
            items.reverse()
            return jsonify({
                "ok": True,
                "count": len(items),
                "entries": items[:32],
            })
        except Exception as e:
            return jsonify({
                "ok": False, "error": f"{type(e).__name__}: {e}",
            }), 500

    @app.route("/curiosity/stats", methods=["GET"])
    def _curiosity_stats():  # type: ignore[unused-ignore]
        try:
            return jsonify({
                "ok": True,
                "period_s": daemon.period,
                "running": daemon.running,
                "tick_count": daemon.tick_count,
                "question_count": daemon.question_count,
                "skip_quiet": daemon.skip_quiet,
                "skip_threat": daemon.skip_threat,
                "skip_cooldown": daemon.skip_cooldown,
                "error_count": daemon.error_count,
                "meta_count": daemon.meta_count,
                "recent_kinds": list(daemon.recent_kinds),
                "kind_cooldown_s": _KIND_COOLDOWN_S,
                "last_shift_by_kind": {
                    k: int(v) for k, v in daemon.last_shift_by_kind.items()
                },
                "paused_by_threat": daemon.paused_by_threat,
                "last_state": {
                    "organism": daemon.state.organism,
                    "coherence": round(daemon.state.coherence, 4),
                    "active_layers": daemon.state.active_layers,
                    "threat_band": daemon.state.threat_band,
                    "process_count": daemon.state.process_count,
                },
            })
        except Exception as e:
            return jsonify({
                "ok": False, "error": f"{type(e).__name__}: {e}",
            }), 500

    @app.route("/curiosity/poke", methods=["POST"])
    def _curiosity_poke():  # type: ignore[unused-ignore]
        """Force an immediate curiosity tick regardless of shift detection.

        G6-gated because it injects an unsolicited self-question into the
        scored turn log.
        """
        if request.args.get("i_mean_it") != "1":
            return jsonify({
                "ok": False,
                "error": "poke requires ?i_mean_it=1 (G6)",
            }), 400
        try:
            # force a shift so the tick produces a question
            prev_organism = daemon.state.organism
            daemon.state.organism = "__force__"
            daemon._one_tick()  # noqa: SLF001
            # restore so detection logic works normally on the next real tick
            if prev_organism is not None:
                daemon.state.organism = prev_organism
            last = daemon.history[-1] if daemon.history else None
            return jsonify({"ok": True, "last": last})
        except Exception as e:
            return jsonify({
                "ok": False, "error": f"{type(e).__name__}: {e}",
            }), 500

    return 3
