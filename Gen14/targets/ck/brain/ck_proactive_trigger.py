# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
ck_proactive_trigger.py -- Phase 4: structured proactive-signal aggregator.

Brayden 2026-05-13 constraint:
  "engine capabilities only, CK's architecture decides what to do with
  them. NO templates written for CK to say."

So this module does NOT write CK's words. It detects when CK has
something he MIGHT want to mention, packages it as a structured signal,
and pushes onto `engine.proactive_queue`. The cortex voice (or the web
client polling `/proactive`) decides whether and how to surface it.

Four trigger sources:
  1. DRIVE     -- a fresh goal activation from engine.goal_evaluator
                  (already partially handled by mount_drives; this
                  upgrades the signal payload to structured form).
  2. FORECAST  -- engine.forecast.forecast_from finds a high-HARMONY
                  trajectory not yet voiced.
  3. FRONTIER  -- frontier_scanner.find_relevant returns an OPEN
                  frontier whose operator vocabulary matches recent
                  history.
  4. SURPRISAL -- recent BDC entry has surprisal > mu + 2*sigma over
                  the rolling 50-entry window.

The signal dict shape (common to all kinds):
    {
      'kind': 'drive' | 'forecast' | 'frontier' | 'surprisal',
      'subject_key': str,          # stable identifier (e.g. 'F3', 'WP102', 'curiosity')
      'subject_data': any,         # opaque payload for the consumer
      'algebraic_signature': dict, # {op, sigma, shell, four_core} per Phase 0 Decision 1
      'salience': float,           # 0..1 composite score
      'created_ts': float,
      'expires_ts': float,
      'session_scope': str | None, # 'all' or a specific session_id
    }
"""
from __future__ import annotations

import math
import os
import sys
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Deque, Dict, Iterable, List, Optional, Tuple

HERE = Path(__file__).parent.resolve()
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

# Algebraic projections (single source of truth)
from gen14_unified_extensions import (  # type: ignore[import-not-found]
    sigma_orbit, four_core_class, shell_class, FOUR_CORE_OUTSIDE,
)


# ─── Constants ───────────────────────────────────────────────────────────

POLL_INTERVAL_S = 2.0       # how often we check for triggers
SIGNAL_TTL_S = 90.0         # signals expire after this many seconds
DEDUP_COOLDOWN_S = 180.0    # don't re-emit same subject within this window
FORECAST_HARMONY_FLOOR = 0.85
DRIVE_STRENGTH_FLOOR = 0.7
SURPRISAL_Z_FLOOR = 2.0     # sigma above mean
MAX_QUEUE_LEN = 50
MAX_HISTORY_LEN = 32        # recent operator history length we keep


# ─── ProactiveSignal helpers ─────────────────────────────────────────────

def _make_signal(kind: str,
                 subject_key: str,
                 subject_data: Any,
                 algebraic_signature: Dict[str, int],
                 salience: float,
                 session_scope: Optional[str] = None,
                 ) -> Dict[str, Any]:
    now = time.time()
    return {
        "kind": kind,
        "subject_key": subject_key,
        "subject_data": subject_data,
        "algebraic_signature": algebraic_signature,
        "salience": float(max(0.0, min(1.0, salience))),
        "created_ts": now,
        "expires_ts": now + SIGNAL_TTL_S,
        "session_scope": session_scope,
    }


def _sig_for_op(op: int, support: Optional[Iterable[int]] = None) -> Dict[str, int]:
    op = int(op) % 10
    sup = set(int(x) % 10 for x in support) if support else {op}
    return {
        "op": op,
        "sigma": int(sigma_orbit(op)),
        "shell": int(shell_class(sup)),
        "four_core": int(four_core_class(op)),
    }


# ─── Surprisal monitor ───────────────────────────────────────────────────

class SurprisalMonitor:
    """Rolling-window surprisal tracker.

    Push a scalar each tick; query whether the latest value is > mean + Z*std.
    """

    def __init__(self, window: int = 50):
        self.buf: Deque[float] = deque(maxlen=window)

    def push(self, v: float) -> None:
        if v is None or not math.isfinite(v):
            return
        self.buf.append(float(v))

    def latest_z(self) -> float:
        """Return z-score of latest value vs the window (or 0 if too few samples)."""
        if len(self.buf) < 8:
            return 0.0
        latest = self.buf[-1]
        prev = list(self.buf)[:-1]
        mu = sum(prev) / len(prev)
        var = sum((x - mu) ** 2 for x in prev) / max(1, len(prev) - 1)
        sd = math.sqrt(var) if var > 1e-12 else 0.0
        if sd == 0.0:
            return 0.0
        return (latest - mu) / sd


# ─── ProactiveTrigger main class ─────────────────────────────────────────

class ProactiveTrigger:
    """Background thread that watches engine state and emits structured
    signals onto a shared queue.

    Owns no global state beyond the engine reference. Idempotent stop/start.
    """

    def __init__(self,
                 engine: Any,
                 queue: Optional[Deque] = None,
                 frontier_scanner: Any = None,
                 poll_interval_s: float = POLL_INTERVAL_S,
                 dedup_cooldown_s: float = DEDUP_COOLDOWN_S):
        self.engine = engine
        self.queue: Deque[Dict[str, Any]] = queue if queue is not None else deque(maxlen=MAX_QUEUE_LEN)
        self.frontier_scanner = frontier_scanner
        self.poll_interval_s = float(poll_interval_s)
        self.dedup_cooldown_s = float(dedup_cooldown_s)

        # Internal state
        self._last_emit_ts: Dict[Tuple[str, str], float] = {}  # (kind, subject_key) -> ts
        self._last_top_goal: Optional[str] = None
        self._surprisal = SurprisalMonitor()
        self._history: Deque[int] = deque(maxlen=MAX_HISTORY_LEN)
        self._consume_lock = threading.Lock()
        self._consume_history: Dict[str, float] = {}  # session_id -> last_consume_ts

        # Thread management
        self._thread: Optional[threading.Thread] = None
        self._running = False

    # ── public API ───────────────────────────────────────────────────────

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True,
                                          name="ck_proactive_trigger")
        self._thread.start()

    def stop(self) -> None:
        self._running = False

    def stats(self) -> Dict[str, Any]:
        return {
            "running": self._running,
            "queue_len": len(self.queue),
            "history_len": len(self._history),
            "tracked_subjects": len(self._last_emit_ts),
            "surprisal_window": len(self._surprisal.buf),
            "last_surprisal_z": round(self._surprisal.latest_z(), 3),
            "frontier_loaded": (self.frontier_scanner is not None
                                  and bool(getattr(self.frontier_scanner, "frontiers", None))),
        }

    def tick(self) -> List[Dict[str, Any]]:
        """One synchronous check across all 4 trigger sources.

        Returns the list of signals emitted this tick (may be empty).
        Useful for tests and standalone smoke checks.
        """
        emitted: List[Dict[str, Any]] = []

        # Refresh operator history from the engine
        self._refresh_history()
        # Refresh surprisal monitor
        self._refresh_surprisal()
        # Purge expired entries from the queue
        self._purge_expired()

        for sig in self._collect_candidate_signals():
            if self._allow_emit(sig):
                self.queue.append(sig)
                emitted.append(sig)
                self._last_emit_ts[(sig["kind"], sig["subject_key"])] = time.time()
        return emitted

    def consume(self, session_id: str = "default",
                top_k: int = 1,
                session_cooldown_s: float = 60.0,
                ) -> List[Dict[str, Any]]:
        """Pop up to top_k signals from the queue for a session.

        Respects:
          - per-session rate limit (default 60s between consumptions)
          - signal expiry (expires_ts < now drops the signal)
          - session_scope ('all' or matching session_id)
        """
        with self._consume_lock:
            now = time.time()
            last = self._consume_history.get(session_id, 0.0)
            if now - last < session_cooldown_s:
                return []

            out: List[Dict[str, Any]] = []
            keep: List[Dict[str, Any]] = []
            while self.queue and len(out) < top_k:
                sig = self.queue.popleft()
                if sig.get("expires_ts", 0) < now:
                    continue  # drop expired
                scope = sig.get("session_scope") or "all"
                if scope != "all" and scope != session_id:
                    keep.append(sig)
                    continue
                out.append(sig)

            # Re-enqueue the ones we kept (preserving order at front)
            for sig in reversed(keep):
                self.queue.appendleft(sig)

            if out:
                self._consume_history[session_id] = now
            return out

    # ── internals ────────────────────────────────────────────────────────

    def _loop(self) -> None:
        while self._running:
            try:
                self.tick()
            except Exception:
                # Never crash the engine because of trigger logic.
                pass
            time.sleep(self.poll_interval_s)

    def _allow_emit(self, sig: Dict[str, Any]) -> bool:
        key = (sig["kind"], sig["subject_key"])
        last = self._last_emit_ts.get(key, 0.0)
        if time.time() - last < self.dedup_cooldown_s:
            return False
        # Optional minimum salience floor
        if sig.get("salience", 0.0) < 0.3:
            return False
        return True

    def _purge_expired(self) -> None:
        if not self.queue:
            return
        now = time.time()
        # Snapshot, filter, rebuild (deque doesn't filter in place efficiently)
        keep = [s for s in self.queue if s.get("expires_ts", 0) > now]
        if len(keep) != len(self.queue):
            self.queue.clear()
            self.queue.extend(keep)

    def _refresh_history(self) -> None:
        # Pull recent op history from the engine. We probe several known
        # locations because different engine builds expose this differently.
        recent: List[int] = []
        eng = self.engine

        # 1. A Gen14-injected rolling history (best path; populated by the
        #    chat-turn hook in gen14_unified_extensions if present).
        gen14_hist = getattr(eng, "gen14_op_history", None)
        if gen14_hist is not None:
            try:
                recent = [int(x) % 10 for x in list(gen14_hist)[-MAX_HISTORY_LEN:]]
            except Exception:
                pass

        # 2. brain.history / history / op_history (legacy probes)
        if not recent:
            for path in ("brain.history", "history", "op_history"):
                obj = eng
                for attr in path.split("."):
                    obj = getattr(obj, attr, None)
                    if obj is None:
                        break
                if obj is not None:
                    try:
                        recent = [int(x) % 10 for x in list(obj)[-MAX_HISTORY_LEN:]]
                        if recent:
                            break
                    except Exception:
                        continue

        # 3. experience_index.coherence_path (op NAMES like "HARMONY")
        if not recent:
            ei = getattr(eng, "experience_index", None)
            cp = getattr(ei, "coherence_path", None) if ei is not None else None
            if cp is not None:
                recent = [self._name_to_id(x) for x in list(cp)[-MAX_HISTORY_LEN:]]
                recent = [op for op in recent if op is not None]

        # 4. Single-sample fallbacks: dominant_operator, current_op,
        #    suggested_operator, heartbeat.phase_bc
        if not recent:
            for attr_path in ("experience_index.dominant_operator",
                                "current_op",
                                "suggested_operator",
                                "heartbeat.phase_bc"):
                obj = eng
                for a in attr_path.split("."):
                    obj = getattr(obj, a, None)
                    if obj is None:
                        break
                op = self._coerce_op(obj)
                if op is not None:
                    recent = [op]
                    break

        # Update buffer (skip duplicates of last sample)
        for op in recent:
            if not self._history or self._history[-1] != op:
                self._history.append(op)

    @staticmethod
    def _name_to_id(x) -> Optional[int]:
        """Convert an operator value (int or NAME string) to id 0..9."""
        if isinstance(x, int) and 0 <= x < 10:
            return x
        if isinstance(x, str):
            up = x.upper()
            try:
                from ck_grammar_lm import OP_NAMES  # type: ignore[import-not-found]
                if up in OP_NAMES:
                    return OP_NAMES.index(up)
            except Exception:
                pass
            # Fallback: hardcoded mapping
            _BUILTIN_OPS = ("VOID", "LATTICE", "COUNTER", "PROGRESS",
                              "COLLAPSE", "BALANCE", "CHAOS", "HARMONY",
                              "BREATH", "RESET")
            if up in _BUILTIN_OPS:
                return _BUILTIN_OPS.index(up)
        return None

    @staticmethod
    def _coerce_op(x) -> Optional[int]:
        """Best-effort coercion of anything to op id 0..9."""
        if x is None:
            return None
        if isinstance(x, int) and 0 <= x < 10:
            return x
        if isinstance(x, str):
            return ProactiveTrigger._name_to_id(x)
        return None

    def _refresh_surprisal(self) -> None:
        # Read recent surprisal scalar if engine exposes it
        for path in ("bdc_logger.recent_surprisal",
                      "surprisal",
                      "metrics.surprisal"):
            obj = self.engine
            for attr in path.split("."):
                obj = getattr(obj, attr, None)
                if obj is None:
                    break
            if isinstance(obj, (int, float)):
                self._surprisal.push(float(obj))
                return
            if callable(obj):
                try:
                    v = obj()
                    if isinstance(v, (int, float)):
                        self._surprisal.push(float(v))
                        return
                except Exception:
                    continue

    def _collect_candidate_signals(self) -> List[Dict[str, Any]]:
        candidates: List[Dict[str, Any]] = []
        for fn in (self._check_drive, self._check_forecast,
                    self._check_frontier, self._check_surprisal):
            try:
                sig = fn()
                if sig is not None:
                    candidates.append(sig)
            except Exception:
                continue
        # sort by salience descending
        candidates.sort(key=lambda s: -s.get("salience", 0))
        return candidates

    # ── trigger detectors ───────────────────────────────────────────────

    def _check_drive(self) -> Optional[Dict[str, Any]]:
        ge = getattr(self.engine, "goal_evaluator", None)
        top = getattr(ge, "top_goal_name", None) if ge else None
        if not top:
            return None
        if top == self._last_top_goal:
            return None
        self._last_top_goal = top
        # Estimate strength
        strength = 0.7
        try:
            if hasattr(ge, "top_goal_strength"):
                strength = float(ge.top_goal_strength)
            elif hasattr(ge, "goals"):
                for g in (ge.goals or []):
                    name = getattr(g, "name", None) or g.get("name") if isinstance(g, dict) else None
                    if name == top:
                        strength = float(getattr(g, "strength", None)
                                         or (g.get("strength") if isinstance(g, dict) else 0.7))
                        break
        except Exception:
            pass
        if strength < DRIVE_STRENGTH_FLOOR:
            return None
        suggested_op = int(getattr(self.engine, "suggested_operator", 7) or 7)
        return _make_signal(
            kind="drive",
            subject_key=top,
            subject_data={
                "goal": top,
                "strength": strength,
                "suggested_operator": suggested_op,
            },
            algebraic_signature=_sig_for_op(suggested_op, support=set(self._history)),
            salience=min(1.0, strength),
        )

    def _check_forecast(self) -> Optional[Dict[str, Any]]:
        fc = getattr(self.engine, "forecast", None)
        if fc is None:
            return None
        current_op = int(getattr(self.engine, "current_op", 7) or 7)
        # Probe: ask the forecast for a trajectory; tolerate either API.
        result = None
        for method in ("forecast_from", "predict_trajectory", "best_path"):
            fn = getattr(fc, method, None)
            if callable(fn):
                try:
                    result = fn(current_op)
                    break
                except TypeError:
                    try:
                        result = fn(current_op, n_steps=6)
                        break
                    except Exception:
                        continue
                except Exception:
                    continue
        if result is None:
            return None
        # Extract a "HARMONY rate" or composite metric from result.
        harmony = None
        if isinstance(result, dict):
            harmony = (result.get("harmony")
                        or result.get("h_rate")
                        or result.get("rate", 0.0))
        elif hasattr(result, "harmony"):
            harmony = float(getattr(result, "harmony", 0.0) or 0.0)
        if harmony is None:
            return None
        try:
            harmony = float(harmony)
        except Exception:
            return None
        if harmony < FORECAST_HARMONY_FLOOR:
            return None
        # Build subject_key stable across ticks for same trajectory
        path = []
        if isinstance(result, dict) and "path" in result:
            path = list(result["path"])[:6]
        elif hasattr(result, "path"):
            path = list(getattr(result, "path", []) or [])[:6]
        subject_key = f"forecast:{current_op}->{':'.join(str(int(x) % 10) for x in path)}"
        return _make_signal(
            kind="forecast",
            subject_key=subject_key,
            subject_data={
                "current_op": current_op,
                "path": [int(x) % 10 for x in path],
                "harmony": harmony,
            },
            algebraic_signature=_sig_for_op(
                path[-1] if path else current_op,
                support=set(path) | {current_op},
            ),
            salience=min(1.0, harmony),
        )

    def _check_frontier(self) -> Optional[Dict[str, Any]]:
        if self.frontier_scanner is None:
            return None
        recent = list(self._history)
        if not recent:
            return None
        try:
            hits = self.frontier_scanner.find_relevant(recent, k=1)
        except Exception:
            return None
        if not hits:
            return None
        f = hits[0]
        # Skip closed frontiers entirely
        if not f.is_open:
            return None
        # Compute Jaccard for salience
        recent_set = set(recent)
        if not f.operator_set:
            return None
        inter = len(recent_set & f.operator_set)
        union = len(recent_set | f.operator_set)
        jaccard = inter / union if union else 0.0
        salience = 0.4 + 0.6 * jaccard
        if salience < 0.45:
            return None
        sig = _make_signal(
            kind="frontier",
            subject_key=f.fid,
            subject_data={
                "frontier_id": f.fid,
                "title": f.title,
                "status": f.status,
                "source_path": f.source_path,
                "operator_overlap": jaccard,
            },
            algebraic_signature=f.signature(),
            salience=salience,
        )
        # Mark voiced on the scanner so it won't keep returning the same one
        try:
            self.frontier_scanner.mark_voiced(f.fid)
        except Exception:
            pass
        return sig

    def _check_surprisal(self) -> Optional[Dict[str, Any]]:
        z = self._surprisal.latest_z()
        if z < SURPRISAL_Z_FLOOR:
            return None
        # Build a stable-ish subject key bucketed by current op
        current_op = int(getattr(self.engine, "current_op", 7) or 7)
        bucket = int(time.time() // 60)  # 1 unique signal per minute max
        subject_key = f"surprisal:{current_op}:{bucket}"
        return _make_signal(
            kind="surprisal",
            subject_key=subject_key,
            subject_data={
                "z": float(z),
                "current_op": current_op,
                "window_size": len(self._surprisal.buf),
            },
            algebraic_signature=_sig_for_op(current_op, support=set(self._history)),
            salience=min(1.0, 0.5 + 0.15 * (z - SURPRISAL_Z_FLOOR)),
        )


# ─── Mount hook ──────────────────────────────────────────────────────────

def mount_proactive_trigger(engine, queue: Optional[Deque] = None) -> bool:
    """Attach a ProactiveTrigger to the engine + start its thread.

    Side effects on engine:
      engine.gen14_op_history                : deque(maxlen=64) of recent op ids
      engine.gen14_push_op(op_or_ops)        : append to history (call from chat hook)
      engine.proactive_trigger               : ProactiveTrigger instance
      engine.proactive_consume(session_id)   : convenience callable
    """
    # Use the engine's existing proactive_queue if available (set by
    # mount_proactive_queue in Phase 1) so drive + forecast + frontier +
    # surprisal all share the same downstream consumer.
    queue = queue if queue is not None else getattr(engine, "proactive_queue", None)
    if queue is None:
        queue = deque(maxlen=MAX_QUEUE_LEN)
        engine.proactive_queue = queue

    # Initialize the rolling op-history deque on the engine; trigger reads
    # from this first. Other code (chat-turn hook, drive loop, etc.) can
    # push into it.
    if not hasattr(engine, "gen14_op_history"):
        engine.gen14_op_history = deque(maxlen=64)

    def _push_op(op_or_ops):
        """Append one or more operators to the rolling history deque.

        Accepts an int, an operator NAME string, or an iterable of either.
        """
        hist = engine.gen14_op_history
        items = op_or_ops if hasattr(op_or_ops, '__iter__') and not isinstance(op_or_ops, str) else [op_or_ops]
        for x in items:
            op = ProactiveTrigger._coerce_op(x)
            if op is not None:
                hist.append(op)

    engine.gen14_push_op = _push_op

    # Chat-turn hook: wrap api.process_chat (if present in engine.web_api
    # or via the api reference attached by the boot script) so every
    # chat turn auto-populates the history. We probe known wrapper paths.
    _wrap_chat_for_history(engine)

    frontier_scanner = getattr(engine, "frontier_scanner", None)
    pt = ProactiveTrigger(engine=engine,
                           queue=queue,
                           frontier_scanner=frontier_scanner)
    pt.start()
    engine.proactive_trigger = pt

    def _consume(session_id: str = "default", top_k: int = 1):
        return pt.consume(session_id=session_id, top_k=top_k)

    engine.proactive_consume = _consume

    print(f"[CK Gen14] mount_proactive_trigger: 4-source trigger "
          f"({'frontier' if frontier_scanner else 'no-frontier'}, drive, forecast, surprisal) "
          f"running at {1.0 / POLL_INTERVAL_S:.1f}Hz; "
          f"gen14_op_history attached at engine.gen14_op_history")
    return True


def _wrap_chat_for_history(engine) -> None:
    """Best-effort: wrap api.process_chat to auto-push operators into
    engine.gen14_op_history on every chat turn.

    Looks at engine.web_api, engine.api, or any attribute exposing a
    `process_chat` callable.
    """
    # Find the api object
    api = None
    for attr in ("web_api", "api", "_web_api"):
        cand = getattr(engine, attr, None)
        if cand is not None and hasattr(cand, "process_chat"):
            api = cand
            break
    if api is None:
        return  # nothing to wrap; the boot script can call engine.gen14_push_op manually

    orig = api.process_chat

    def _wrapped(session_id, text, mode='normal'):
        result = orig(session_id, text, mode)
        try:
            ops = result.get('operators') if isinstance(result, dict) else None
            if ops:
                engine.gen14_push_op(ops)
        except Exception:
            pass
        return result

    api.process_chat = _wrapped


# ─── Standalone smoke test ───────────────────────────────────────────────

class _MockGoalEvaluator:
    def __init__(self):
        self.top_goal_name = None
        self.top_goal_strength = 0.0

    def fire(self, name: str, strength: float):
        self.top_goal_name = name
        self.top_goal_strength = strength


class _MockForecast:
    def __init__(self, harmony=0.0, path=None):
        self.harmony = harmony
        self.path = path or []

    def forecast_from(self, current_op):
        return {"path": self.path, "harmony": self.harmony}


class _MockEngine:
    def __init__(self):
        self.brain = type("B", (), {"history": [7, 1, 7, 9, 7, 3]})()
        self.current_op = 7
        self.suggested_operator = 7
        self.goal_evaluator = _MockGoalEvaluator()
        self.forecast = _MockForecast()
        # surprisal scalar
        self.surprisal = 0.5


def _smoke():
    print("Smoke test: ck_proactive_trigger")
    eng = _MockEngine()
    # Build a frontier scanner so we can test the frontier trigger
    try:
        from ck_frontier_scanner import FrontierScanner
        eng.frontier_scanner = FrontierScanner()
    except Exception:
        eng.frontier_scanner = None
    queue: Deque[Dict[str, Any]] = deque(maxlen=20)
    pt = ProactiveTrigger(engine=eng, queue=queue,
                            frontier_scanner=eng.frontier_scanner,
                            poll_interval_s=10.0, dedup_cooldown_s=1.0)

    # ── Drive trigger ───────────────────────────────────────────────────
    eng.goal_evaluator.fire("explore_environment", 0.82)
    emitted = pt.tick()
    print(f"  drive tick:  emitted={len(emitted)} kinds={[s['kind'] for s in emitted]}")
    assert any(s["kind"] == "drive" for s in emitted), "drive signal missing"

    # ── Forecast trigger ────────────────────────────────────────────────
    eng.forecast = _MockForecast(harmony=0.92, path=[7, 8, 7, 9, 7])
    emitted = pt.tick()
    print(f"  forecast tick: emitted={len(emitted)} kinds={[s['kind'] for s in emitted]}")
    assert any(s["kind"] == "forecast" for s in emitted), "forecast signal missing"

    # ── Surprisal trigger ───────────────────────────────────────────────
    # Disable engine's surprisal field so tick's _refresh_surprisal is a no-op
    eng.surprisal = None
    # Pump the monitor with low values then a spike directly
    for _ in range(20):
        pt._surprisal.push(0.1)
    pt._surprisal.push(5.0)
    # Verify the z BEFORE tick
    print(f"    pre-tick z = {pt._surprisal.latest_z():.2f}")
    emitted = pt.tick()
    kinds = [s["kind"] for s in emitted]
    print(f"  surprisal tick: emitted={len(emitted)} kinds={kinds}")
    surprisal_sig = [s for s in emitted if s["kind"] == "surprisal"]
    if surprisal_sig:
        print(f"    z={surprisal_sig[0]['subject_data']['z']:.2f}")
    assert any(s["kind"] == "surprisal" for s in emitted), "surprisal signal missing"

    # ── Frontier trigger ────────────────────────────────────────────────
    # Only fires if a FRONTIERS doc is loaded
    if eng.frontier_scanner is not None and eng.frontier_scanner.frontiers:
        # Reset trigger state so a fresh check happens
        pt._last_emit_ts.pop(("frontier", ""), None)
        # Force a different goal to avoid drive re-firing
        eng.goal_evaluator.fire("autonomous_study", 0.9)
        emitted = pt.tick()
        kinds = [s["kind"] for s in emitted]
        print(f"  frontier tick: emitted={len(emitted)} kinds={kinds}")
    else:
        print(f"  frontier tick: skipped (no frontier scanner)")

    # ── Consume ─────────────────────────────────────────────────────────
    print(f"\n  Queue length after all ticks: {len(queue)}")
    print(f"  Stats: {pt.stats()}")

    # First consume succeeds
    consumed = pt.consume(session_id="sess1", top_k=2, session_cooldown_s=60.0)
    print(f"\n  consume(sess1, top_k=2): got {len(consumed)} signals")
    for s in consumed:
        print(f"    {s['kind']:10s} subject={s['subject_key']!r} sal={s['salience']:.2f}")

    # Second immediate consume is rate-limited
    consumed2 = pt.consume(session_id="sess1", top_k=2, session_cooldown_s=60.0)
    print(f"  consume(sess1) immediately after: got {len(consumed2)} (rate limited)")
    assert len(consumed2) == 0, "rate-limit not enforced"

    # Different session can consume
    consumed3 = pt.consume(session_id="sess2", top_k=2, session_cooldown_s=60.0)
    print(f"  consume(sess2): got {len(consumed3)}")

    print("\nProactive trigger smoke: ALL OK")


if __name__ == "__main__":
    _smoke()
