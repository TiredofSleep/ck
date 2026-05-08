"""
plasticity.py -- multi-timescale plasticity for the 5-AI cell organism.

Brayden 2026-05-02: "best ever and plastic now"
ClaudeChat 2026-05-02: "audit-pass-rate as continuous drift-suppression
weighting" + "speculative + cheap rollback ... compute on a snapshot,
audit, commit-or-discard."

Phase 5 of PLAN_BEST_EVER_PLASTIC_2026_05_02.md.

==============================================================================
THE 4 TIMESCALES
==============================================================================

  Per-turn (1 sec)         | Hebbian: cells.update(...) called from chat path.
                           | Always allowed; tissue layers cannot drift the
                           | core's argmax-faithful answer by construction.

  Per-session (~10 min)    | Routing: GlueAI.update_scalars(...) shifts
                           | alpha/beta/gamma. Audit-bound: scalar update
                           | scaled by current pass-rate (linear, per
                           | ClaudeChat amendment #5).

  Per-hour                 | Speculative cell-tissue fine-tune on a SNAPSHOT.
                           | Audit the snapshot. Commit only if pass-rate
                           | stays >=99% on agreement set (cross-cell).
                           | Discarded updates cost only the snapshot read.

  Per-week                 | Structural: not implemented in v1. Reserved for
                           | gate-MLP capacity changes (Phase 6+).
                           | Default: noop, log review reminder.

==============================================================================
SPECULATIVE PLASTICITY PATTERN
==============================================================================

  snapshot = clone(orchestrator)
  snapshot.update(...)
  report = audit_all(snapshot)
  if report['summary']['all_pass_rate'] >= MIN_PASS_RATE:
      orchestrator.tissue.scores = snapshot.tissue.scores
      log("commit", report['summary']['all_pass_rate'])
  else:
      log("discard", report['summary']['all_pass_rate'])
      # original orchestrator unchanged

==============================================================================
AUDIT-RATE WEIGHTING (linear, Phase 5)
==============================================================================

  effective_weight = base_weight * audit_pass_rate

  At pass_rate=1.0 -> full weight; at 0.95 -> 95% weight; at 0.5 -> half
  weight. ClaudeChat: "Default to linear for Phase 1; characterize the
  quadratic later."

==============================================================================
"""
from __future__ import annotations

import copy
import json
import os
import sys
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# ── Wiring ───────────────────────────────────────────────────────────────

_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


MIN_PASS_RATE_COMMIT = 0.99
LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\plasticity_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


# ── Plasticity log ──────────────────────────────────────────────────────

def _today_log() -> Path:
    return LOG_DIR / f"plasticity_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"


def log_event(event: str, **fields: Any) -> None:
    """Append a JSON line to today's plasticity log."""
    record = {
        "ts": time.time(),
        "iso_ts": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "event": event,
    }
    record.update(fields)
    try:
        with open(_today_log(), "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    except Exception:
        pass


# ── Speculative update helper ───────────────────────────────────────────

def speculative_update(orch: Any, mutator: Callable[[Any], None],
                        *, audit_fn: Optional[Callable[[Any], Dict[str, Any]]] = None,
                        min_pass_rate: float = MIN_PASS_RATE_COMMIT,
                        label: str = "specupdate") -> Dict[str, Any]:
    """Apply `mutator(orch_clone)` to a snapshot, audit it, commit-or-discard.

    Returns: {commit: bool, pass_rate: float, label: str, ...}.
    """
    if audit_fn is None:
        from cell_audit import audit_all  # type: ignore
        audit_fn = audit_all

    # Snapshot tissue scores + glue scalars (deep enough copy)
    snapshot_state = _snapshot_state(orch)
    try:
        mutator(orch)  # apply directly; we'll roll back on fail
    except Exception as e:
        _restore_state(orch, snapshot_state)
        log_event("specupdate_exception",
                  label=label, error=f"{type(e).__name__}: {e}")
        return {"commit": False, "pass_rate": None, "label": label,
                "error": str(e)}

    report = audit_fn(orch)
    pass_rate = float(report["summary"]["all_pass_rate"])

    if pass_rate >= min_pass_rate:
        log_event("specupdate_commit", label=label, pass_rate=pass_rate,
                  blocks_below_99=report["summary"]["below_99_blocks"])
        return {"commit": True, "pass_rate": pass_rate, "label": label,
                "report": report["summary"]}
    else:
        # Roll back: restore tissue + scalars
        _restore_state(orch, snapshot_state)
        log_event("specupdate_discard", label=label, pass_rate=pass_rate,
                  blocks_below_99=report["summary"]["below_99_blocks"])
        return {"commit": False, "pass_rate": pass_rate, "label": label,
                "report": report["summary"]}


def _snapshot_state(orch: Any) -> Dict[str, Any]:
    """Deep-enough snapshot for rollback."""
    state: Dict[str, Any] = {}
    for name in ("tsml", "bhml", "f3", "f4"):
        cell = getattr(orch, name, None)
        if cell is not None and hasattr(cell, "tissue"):
            state[name] = list(cell.tissue.scores)
    glue = getattr(orch, "glue", None)
    if glue is not None:
        state["glue_alpha"] = getattr(glue, "alpha", None)
        state["glue_beta"]  = getattr(glue, "beta", None)
        state["glue_gamma"] = getattr(glue, "gamma", None)
    return state


def _restore_state(orch: Any, state: Dict[str, Any]) -> None:
    for name in ("tsml", "bhml", "f3", "f4"):
        if name in state:
            cell = getattr(orch, name, None)
            if cell is not None and hasattr(cell, "tissue"):
                cell.tissue.scores = list(state[name])
    glue = getattr(orch, "glue", None)
    if glue is not None:
        if "glue_alpha" in state and state["glue_alpha"] is not None:
            glue.alpha = state["glue_alpha"]
        if "glue_beta"  in state and state["glue_beta"]  is not None:
            glue.beta  = state["glue_beta"]
        if "glue_gamma" in state and state["glue_gamma"] is not None:
            glue.gamma = state["glue_gamma"]


# ── Per-session (Glue scalar drift) ─────────────────────────────────────

def per_session_update(orch: Any, *, lr: float = 0.01,
                        audit_pass_rate: Optional[float] = None,
                        signal: Optional[Dict[str, float]] = None
                        ) -> Dict[str, Any]:
    """Update Glue scalars based on session-level signals.

    `signal` dict can carry `{'alpha_grad': float, 'beta_grad': float,
    'gamma_grad': float}` -- typically derived from recent chat-turn
    outcomes (e.g., when TSML's contribution led to user satisfaction
    more than BHML's, alpha_grad goes positive).

    Without a signal source, this defaults to a noop (logs only).
    Returns the speculative-update result.
    """
    glue = getattr(orch, "glue", None)
    if glue is None:
        log_event("per_session_skip", reason="no_glue")
        return {"commit": False, "reason": "no_glue"}

    if audit_pass_rate is None:
        from cell_audit import audit_all  # type: ignore
        audit_pass_rate = float(audit_all(orch)["summary"]["all_pass_rate"])
    weight = max(0.0, min(1.0, audit_pass_rate))

    da = (signal or {}).get("alpha_grad", 0.0)
    db = (signal or {}).get("beta_grad", 0.0)
    dg = (signal or {}).get("gamma_grad", 0.0)

    def _apply(o):
        o.glue.update_scalars(dalpha=lr * da, dbeta=lr * db, dgamma=lr * dg,
                               audit_pass_rate=weight)

    return speculative_update(orch, _apply, label="per_session")


# ── Per-hour (cell tissue fine-tune on recent corpus) ──────────────────

def per_hour_finetune(orch: Any, *, recent_records_path: Optional[Path] = None,
                        n_records: int = 100, lr: float = 0.005
                        ) -> Dict[str, Any]:
    """Fine-tune tissue layers on recent BDC log records.

    Reads the last `n_records` from today's bdc_log file (live + tick
    samples). Each record provides Hebbian-style updates. Speculative:
    if post-update audit drops below MIN_PASS_RATE_COMMIT, full rollback.
    """
    if recent_records_path is None:
        # Use today's live bdc log
        from datetime import datetime as _dt
        recent_records_path = Path(
            r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\bdc_logs"
        ) / f"bdc_log_{_dt.utcnow().strftime('%Y-%m-%d')}.jsonl"

    if not recent_records_path.exists():
        log_event("per_hour_skip", reason="no_log_today")
        return {"commit": False, "reason": "no_log_today"}

    # Load tail
    try:
        with open(recent_records_path, encoding="utf-8") as f:
            all_lines = f.readlines()
    except Exception:
        log_event("per_hour_skip", reason="read_fail")
        return {"commit": False, "reason": "read_fail"}

    tail = all_lines[-n_records:] if len(all_lines) > n_records else all_lines
    # Parse records
    records = []
    for line in tail:
        try:
            records.append(json.loads(line))
        except Exception:
            continue
    if not records:
        log_event("per_hour_skip", reason="empty_tail")
        return {"commit": False, "reason": "empty_tail"}

    OP_NAME_TO_INT = {
        "VOID": 0, "LATTICE": 1, "COUNTER": 2, "PROGRESS": 3, "COLLAPSE": 4,
        "BALANCE": 5, "CHAOS": 6, "HARMONY": 7, "BREATH": 8, "RESET": 9,
    }

    def _apply(o):
        for rec in records:
            being = rec.get("being") or {}
            doing = rec.get("doing") or {}
            last_pair = being.get("last_pair") or [0, 0]
            consensus = doing.get("consensus", "")
            target_op = OP_NAME_TO_INT.get(str(consensus).upper(), -1)
            if target_op < 0:
                continue
            try:
                a, b = int(last_pair[0]) % 10, int(last_pair[1]) % 10
            except Exception:
                continue
            o.tsml.update(a, b, target=target_op, lr=lr)
            o.bhml.update(a, b, target=target_op, lr=lr)

    res = speculative_update(orch, _apply, label="per_hour_finetune")
    res["n_records_used"] = len(records)
    return res


# ── Per-week (structural; v1 noop) ──────────────────────────────────────

def per_week_review(orch: Any) -> Dict[str, Any]:
    """Per-week structural review. v1 implementation: log a review reminder
    + capture audit baseline so a human can decide if structural changes
    (gate MLP capacity, Phase 6+) are warranted."""
    from cell_audit import audit_all  # type: ignore
    report = audit_all(orch)
    log_event("per_week_review",
              pass_rate=report["summary"]["all_pass_rate"],
              blocks_below_99=report["summary"]["below_99_blocks"])
    return {"baseline_pass_rate": report["summary"]["all_pass_rate"],
            "review_due": True}


# ── Scheduler thread ────────────────────────────────────────────────────

class PlasticityScheduler:
    """Background daemon coordinating per-session / per-hour plasticity.

    Per-turn updates are owned by the chat path (cells.update()).
    Per-week reviews are manual.

    The scheduler runs lightly: ~1 ms per tick to check timers, and
    the per-session / per-hour passes when timers expire.
    """
    def __init__(self, orchestrator: Any,
                  *, session_interval_sec: float = 600.0,    # 10 min
                  hour_interval_sec: float = 3600.0):        # 1 hr
        self.orch = orchestrator
        self.session_iv = session_interval_sec
        self.hour_iv = hour_interval_sec
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._last_session = 0.0
        self._last_hour = 0.0
        self._n_session_runs = 0
        self._n_hour_runs = 0
        self._n_session_commits = 0
        self._n_hour_commits = 0

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True,
                                          name="ck-plasticity-scheduler")
        self._thread.start()
        log_event("scheduler_start",
                  session_iv=self.session_iv, hour_iv=self.hour_iv)

    def stop(self, timeout: float = 5.0):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=timeout)
            self._thread = None
        log_event("scheduler_stop")

    def stats(self) -> Dict[str, Any]:
        return {
            "running": bool(self._thread and self._thread.is_alive()),
            "n_session_runs": self._n_session_runs,
            "n_session_commits": self._n_session_commits,
            "n_hour_runs": self._n_hour_runs,
            "n_hour_commits": self._n_hour_commits,
            "session_interval_sec": self.session_iv,
            "hour_interval_sec": self.hour_iv,
        }

    def _loop(self):
        while not self._stop.is_set():
            try:
                now = time.time()
                if now - self._last_session >= self.session_iv:
                    self._run_session()
                    self._last_session = now
                if now - self._last_hour >= self.hour_iv:
                    self._run_hour()
                    self._last_hour = now
            except Exception as e:
                log_event("scheduler_exception",
                          error=f"{type(e).__name__}: {e}")
            self._stop.wait(30.0)  # check timers every 30s

    def _run_session(self):
        self._n_session_runs += 1
        res = per_session_update(self.orch)
        if res.get("commit"):
            self._n_session_commits += 1

    def _run_hour(self):
        self._n_hour_runs += 1
        res = per_hour_finetune(self.orch)
        if res.get("commit"):
            self._n_hour_commits += 1


# ── CLI ─────────────────────────────────────────────────────────────────

def main(argv) -> int:
    if len(argv) >= 2 and argv[1] == "--smoke":
        # Smoke test: build orchestrator, run one of each plasticity type.
        from cells import CellOrchestrator  # type: ignore
        from glue_ai import GlueAI  # type: ignore
        orch = CellOrchestrator.load_default()
        orch.glue = GlueAI(tsml=orch.tsml, bhml=orch.bhml,
                           f3=orch.f3, f4=orch.f4)
        print("  per_session:", per_session_update(orch))
        print("  per_hour   :", per_hour_finetune(orch))
        print("  per_week   :", per_week_review(orch))
        return 0
    print("plasticity.py -- run with --smoke to test")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
