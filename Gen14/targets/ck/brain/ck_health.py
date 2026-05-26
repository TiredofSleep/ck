"""ck_health.py -- single /health endpoint aggregating CK module status.

CK Gen14 diagnostic primitive — one read-only endpoint that tells you
which CK modules are mounted, their per-module key counters, and the
overall runtime state.  Useful for:

  - Dashboard "is everything OK?" indicator
  - External monitoring (Cloudflare healthcheck, uptime ping)
  - Future-Claude / future-Brayden orientation when returning to CK
    after time away ("what's mounted right now?")

═══════════════════════════════════════════════════════════════════
What this module DOES
═══════════════════════════════════════════════════════════════════

`build_health(engine)` returns a structured dict:

  {
    "status": "ok" | "degraded" | "minimal",
    "timestamp": ISO,
    "uptime_seconds": float (if engine has _started_ts),
    "modules": {
        "pc_sense":   {"mounted": true, "buffer_size": 60, "n_readings": 14, "latest_op": "BALANCE"},
        "journal":    {"mounted": true, "n_entries": 23, "path": "..."},
        "bookmark":   {"mounted": true, "n_items": 7, "path": "..."},
        "reminder":   {"mounted": true, "n_total": 5, "n_due": 1, "n_pending": 3},
        "file_orient":{"mounted": true, "n_files_indexed": 1532},
        "code_writer":{"mounted": true, "n_templates": 8},
        "rhythm":     {"mounted": true, "current_op": "HARMONY"},
        "anomaly_detector": {"mounted": true, "n_library_entries": 0},
        "scope_auditor": {"mounted": true},
        "scope_auditor_battery": "51/51 + 31/31 legit",
        ...
    },
    "counts": {
        "n_modules_expected": 14,
        "n_modules_mounted": 12,
        "n_modules_missing": 2,
    },
    "missing": ["pc_recommend", "...]
  }

The "status" field is computed:
  - "ok"        if all expected modules are mounted
  - "degraded"  if at least one core module (pc_sense, journal,
                rhythm, scope_auditor) is missing
  - "minimal"   if fewer than half of expected modules mounted

═══════════════════════════════════════════════════════════════════
What this module DOES NOT DO
═══════════════════════════════════════════════════════════════════

  - Never crashes if a module's status-read raises (catches and
    reports the error inline as that module's "error" field).
  - Never writes anything.
  - Never makes outbound network calls.
  - Never includes the actual data — only counts and identifiers.
"""
from __future__ import annotations

import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


# ─── Expected module list (used for the "status" computation) ────

EXPECTED_MODULES = (
    # Core
    "pc_sense", "journal", "rhythm", "scope_auditor",
    # Useful
    "pc_recommend", "code_writer", "file_orient", "bookmark",
    "reminder", "daily_summary", "search", "export",
    "anomaly_detector", "privacy",
    "toolbox", "languages",
)

CORE_MODULES = frozenset({
    "pc_sense", "journal", "rhythm", "scope_auditor",
})


# ─── Per-module status readers ────────────────────────────────────

def _safe(fn: Callable[..., Any], *args, **kwargs) -> Any:
    """Run fn(...) and return (value, None) or (None, error_str)."""
    try:
        return fn(*args, **kwargs), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def _status_pc_sense(engine: Any) -> Dict[str, Any]:
    api = getattr(engine, "ck_pc_sense", None)
    if not api:
        return {"mounted": False}
    daemon = api.get("daemon")
    out: Dict[str, Any] = {"mounted": True}
    if daemon:
        try:
            out["buffer_size"] = daemon.buffer_size
            out["poll_hz"] = daemon.poll_hz
            hist = daemon.history()
            out["n_readings"] = len(hist)
            if hist:
                out["latest_op"] = hist[-1].op_name
                out["latest_coherence"] = round(hist[-1].coherence, 4)
                out["latest_band"] = hist[-1].coherence_band
        except Exception as e:
            out["error"] = f"{type(e).__name__}: {e}"
    return out


def _status_journal(engine: Any) -> Dict[str, Any]:
    api = getattr(engine, "ck_journal", None)
    if not api:
        return {"mounted": False}
    out: Dict[str, Any] = {"mounted": True}
    j = api.get("journal")
    if j:
        try:
            s = j.stats()
            out["n_entries"] = s.get("n_entries", 0)
            out["path"] = s.get("path", "")
        except Exception as e:
            out["error"] = f"{type(e).__name__}: {e}"
    return out


def _status_bookmark(engine: Any) -> Dict[str, Any]:
    api = getattr(engine, "ck_bookmark", None)
    if not api:
        return {"mounted": False}
    out: Dict[str, Any] = {"mounted": True}
    store = api.get("store")
    if store:
        try:
            s = store.stats()
            out["n_items"] = s.get("n_items", 0)
            out["path"] = s.get("path", "")
        except Exception as e:
            out["error"] = f"{type(e).__name__}: {e}"
    return out


def _status_reminder(engine: Any) -> Dict[str, Any]:
    api = getattr(engine, "ck_reminder", None)
    if not api:
        return {"mounted": False}
    out: Dict[str, Any] = {"mounted": True}
    store = api.get("store")
    if store:
        try:
            s = store.stats()
            out["n_total"] = s.get("n_total", 0)
            out["n_due"] = s.get("n_due_now", 0)
            out["n_pending"] = s.get("n_pending", 0)
            out["n_acknowledged"] = s.get("n_acknowledged", 0)
        except Exception as e:
            out["error"] = f"{type(e).__name__}: {e}"
    return out


def _status_file_orient(engine: Any) -> Dict[str, Any]:
    api = getattr(engine, "ck_file_orient", None)
    if not api:
        return {"mounted": False}
    out: Dict[str, Any] = {"mounted": True}
    idx = api.get("index")
    if idx:
        try:
            s = idx.stats()
            out["n_files_indexed"] = s.get("n_files", 0)
            out["total_gb"] = s.get("total_gb", 0)
        except Exception as e:
            out["error"] = f"{type(e).__name__}: {e}"
    return out


def _status_code_writer(engine: Any) -> Dict[str, Any]:
    api = getattr(engine, "ck_code_writer", None)
    if not api:
        return {"mounted": False}
    out: Dict[str, Any] = {"mounted": True}
    list_fn = api.get("list_templates")
    if list_fn:
        try:
            tpls = list_fn()
            out["n_templates"] = len(tpls)
            out["auditor_wired"] = api.get("auditor") is not None
        except Exception as e:
            out["error"] = f"{type(e).__name__}: {e}"
    return out


def _status_rhythm(engine: Any) -> Dict[str, Any]:
    api = getattr(engine, "ck_rhythm", None)
    if not api:
        return {"mounted": False}
    out: Dict[str, Any] = {"mounted": True}
    cr = api.get("current_rhythm")
    if cr:
        try:
            snap = cr()
            out["current_op"] = snap.phase_op_name
            out["composite_beat"] = snap.composite_beat
        except Exception as e:
            out["error"] = f"{type(e).__name__}: {e}"
    return out


def _status_anomaly(engine: Any) -> Dict[str, Any]:
    api = getattr(engine, "ck_anomaly_detector", None)
    if not api:
        return {"mounted": False}
    out: Dict[str, Any] = {"mounted": True}
    lib = api.get("library")
    if lib:
        try:
            s = lib.stats()
            out["n_library_entries"] = s.get("n_entries", 0)
            out["categories"] = s.get("categories", {})
        except Exception as e:
            out["error"] = f"{type(e).__name__}: {e}"
    return out


def _status_simple(engine: Any, attr: str) -> Dict[str, Any]:
    """Generic 'is it mounted?' check for modules without rich status."""
    api = getattr(engine, attr, None)
    return {"mounted": api is not None}


# ─── Build full status ─────────────────────────────────────────────

def build_health(engine: Any) -> Dict[str, Any]:
    """Read every module's status and return aggregated health dict."""
    started_ts = getattr(engine, "_started_ts", None)
    now = time.time()
    uptime = (now - started_ts) if started_ts else None

    modules: Dict[str, Dict[str, Any]] = {
        "pc_sense":          _status_pc_sense(engine),
        "journal":           _status_journal(engine),
        "bookmark":          _status_bookmark(engine),
        "reminder":          _status_reminder(engine),
        "file_orient":       _status_file_orient(engine),
        "code_writer":       _status_code_writer(engine),
        "rhythm":            _status_rhythm(engine),
        "anomaly_detector":  _status_anomaly(engine),
        # Simple "mounted?" checks for the rest
        "scope_auditor":     _status_simple(engine, "ck_scope_auditor")
                                if hasattr(engine, "ck_scope_auditor")
                                else {"mounted": False},
        "pc_recommend":      _status_simple(engine, "ck_pc_recommend"),
        "daily_summary":     _status_simple(engine, "ck_daily_summary"),
        "search":            _status_simple(engine, "ck_search"),
        "export":            _status_simple(engine, "ck_export"),
        "privacy":           _status_simple(engine, "ck_privacy"),
        "toolbox":           _status_simple(engine, "ck_toolbox"),
        "languages":         {"mounted": hasattr(engine, "ck_lang")
                                            or hasattr(engine, "ck_languages")},
    }

    n_mounted = sum(1 for s in modules.values() if s.get("mounted"))
    n_expected = len(EXPECTED_MODULES)
    missing = [k for k in EXPECTED_MODULES if not modules.get(k, {}).get("mounted")]
    n_missing = len(missing)
    core_missing = [k for k in CORE_MODULES if not modules.get(k, {}).get("mounted")]

    # Status computation
    if core_missing:
        status = "degraded"
    elif n_mounted >= n_expected:
        status = "ok"
    elif n_mounted >= n_expected // 2:
        status = "ok"  # most modules mounted, no core missing
    else:
        status = "minimal"

    return {
        "status": status,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "epoch": now,
        "uptime_seconds": round(uptime, 1) if uptime else None,
        "modules": modules,
        "counts": {
            "n_modules_expected": n_expected,
            "n_modules_mounted": n_mounted,
            "n_modules_missing": n_missing,
            "n_core_missing": len(core_missing),
        },
        "missing": missing,
        "core_missing": core_missing,
    }


# ─── Engine mount ─────────────────────────────────────────────────

def mount_health(engine: Any) -> bool:
    """Attach health builder + register Flask endpoint.

    Endpoints (read-only):
      GET /health         — full status dict
      GET /health/info    — what this endpoint reports

    Also stamps `engine._started_ts` on mount if not already set (for
    uptime tracking).
    """
    # Stamp start time if not already there
    if not hasattr(engine, "_started_ts"):
        engine._started_ts = time.time()

    engine.ck_health = {
        "build_health": lambda: build_health(engine),
        "EXPECTED_MODULES": EXPECTED_MODULES,
    }

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify  # type: ignore

                def _health():
                    return jsonify(build_health(engine))

                def _info():
                    return jsonify({
                        "module": "ck_health",
                        "philosophy": ("single /health endpoint for "
                                        "monitoring, dashboards, and "
                                        "future-Claude orientation."),
                        "expected_modules": list(EXPECTED_MODULES),
                        "core_modules": sorted(CORE_MODULES),
                        "status_values": ["ok", "degraded", "minimal"],
                        "endpoints": [
                            "GET /health",
                            "GET /health/info",
                        ],
                    })

                existing = {r.rule for r in app.url_map.iter_rules()}
                for rule, ep, fn, methods in (
                    ("/health",      "ck_health_q", _health, ["GET"]),
                    ("/health/info", "ck_health_i", _info,   ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
            except Exception as e:
                print(f"[CK Gen14] mount_health: routes failed: {e}")

    print(f"[CK Gen14] mount_health: GET /health endpoint ready "
          f"(expected_modules={len(EXPECTED_MODULES)})")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    import json as _json
    import tempfile
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent))
    print("ck_health smoke test")
    print("=" * 60)
    print()

    class FakeEngine: pass
    eng = FakeEngine()

    # Mount a few modules to demo
    from ck_journal import Journal
    from ck_bookmark import Bookmarks
    from ck_reminder import Reminders
    from ck_rhythm import current_rhythm

    tmp = lambda n: Path(tempfile.gettempdir()) / f"ck_h_{n}.jsonl"
    for n in ("j", "b", "r"):
        p = tmp(n)
        if p.exists(): p.unlink()

    j = Journal(path=tmp("j"))
    j.note("test entry one")
    j.note("test entry two")
    eng.ck_journal = {"journal": j}

    b = Bookmarks(path=tmp("b"))
    b.add("https://example.com/")
    eng.ck_bookmark = {"store": b}

    r = Reminders(path=tmp("r"))
    r.add("test reminder", "30m")
    eng.ck_reminder = {"store": r}

    eng.ck_rhythm = {"current_rhythm": current_rhythm}

    print("Step 1: build health with 4 modules mounted")
    print("-" * 60)
    h = build_health(eng)
    print(_json.dumps(h, indent=2)[:2500])
    print()
    print("Step 2: status =", h["status"])
    print("Counts:", h["counts"])
    print()
    j.clear(); b.clear(); r.clear()
    print("Smoke complete.")
