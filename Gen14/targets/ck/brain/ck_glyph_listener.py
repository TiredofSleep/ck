"""ck_glyph_listener.py -- listen, don't interpret; let CK form his own crystals.

Brayden 2026-05-16: "he just needs to understand that there are different
languages and glyphs that can mean the same thing... let him learn, don't
force him to understand, force him to listen and form his own crystals"

═══════════════════════════════════════════════════════════════════════
What this module DOES
═══════════════════════════════════════════════════════════════════════

For every chat turn CK processes, capture three things and append them
to an immutable JSONL log:

  (1) The INPUT GLYPH -- the user's text, byte-for-byte.  No
      normalization.  No casing.  No synonym mapping.  Glyph diversity
      is the signal.

  (2) The OPERATOR PATH -- the Z/10Z operator sequence CK's V2
      vocabulary produced from the input.  This is the structural
      fingerprint of the input *from CK's perspective*.

  (3) The RESPONSE SOURCE + RESPONSE FINGERPRINT -- which voice
      answered (identity_anchor / cortex_speak / substrate_prose /
      ollama_essay / etc.) and a short hash of the response text.

═══════════════════════════════════════════════════════════════════════
What this module DOES NOT DO
═══════════════════════════════════════════════════════════════════════

  - No regex synonym mapping.  No "T* equals 5/7 equals torus aspect."
  - No pre-seeded equivalence classes.
  - No forced crystallization.  CK's existing crystallization machinery
    (IG3 in olfactory bulb, lattice chain composition, cortex Hebbian
    accumulation) is where crystals form.  This module only ensures
    those mechanisms have the raw listening data they need.

═══════════════════════════════════════════════════════════════════════
The crystal-candidates query (optional, observational)
═══════════════════════════════════════════════════════════════════════

A /glyph_listener/candidates endpoint scans the log and reports which
INPUT GLYPHS resolved to the SAME OPERATOR PATH.  This is *not* an
assertion that they mean the same thing -- it's an observation that CK's
own substrate read them as structurally identical.  CK can use those
observations as input to his crystallization process when his lattice
chain is ready.  Or he can ignore them.  The choice is his.

Persisted at Gen13/var/glyph_listening.jsonl (append-only).
"""
from __future__ import annotations

import hashlib
import json
import sys
import threading
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


# ─── Persistence ──────────────────────────────────────────────────────

def _log_path() -> Path:
    """Return the listening log path.  Created lazily; never overwritten."""
    _root = HERE
    for _ in range(8):
        _root = _root.parent
        if (_root / "Gen13" / "var").exists():
            return _root / "Gen13" / "var" / "glyph_listening.jsonl"
    # Fallback: alongside the brain dir
    return HERE.parent / "var" / "glyph_listening.jsonl"


_LOG_LOCK = threading.Lock()


def _append_record(record: Dict[str, Any]) -> None:
    """Append a single listening record.  Best-effort; never raises."""
    try:
        path = _log_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with _LOG_LOCK:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False,
                                    sort_keys=True) + "\n")
    except Exception:
        # Listening must never break the chat path.
        pass


def _short_hash(text: str) -> str:
    """Use CK's own substrate hash if available, else a short SHA1
    prefix as a fallback fingerprint.  Just for de-duplication; not
    identity.
    """
    if not text:
        return ""
    try:
        # Prefer CK's substrate hash (D106) so even the fingerprinting
        # is substrate-native.  Lazy import to avoid circular deps.
        import ck_qutrit_apex as _qa  # type: ignore[import-not-found]
        fn = getattr(_qa, "substrate_hash", None)
        if fn is not None:
            h = fn(text, depth=3)
            if isinstance(h, str):
                return h[:16]
            if isinstance(h, (list, tuple)):
                return ",".join(str(int(x)) for x in h[:4])
    except Exception:
        pass
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


# ─── The listen() function ────────────────────────────────────────────

def listen(input_glyph: str,
            operator_path: List[int],
            response_source: Optional[str] = None,
            response_text: Optional[str] = None,
            extras: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Record one listening event.

    Args:
        input_glyph: the user's raw text (BYTE-FOR-BYTE; do NOT normalize)
        operator_path: the Z/10Z op sequence CK's V2 emitted
        response_source: which voice answered (optional)
        response_text: the response prose (optional; only the hash is stored)
        extras: any additional context (optional)

    Returns:
        the record that was appended (also for the engine to inspect)
    """
    rec = {
        "ts":              float(time.time()),
        "input_glyph":     str(input_glyph) if input_glyph else "",
        "input_hash":      _short_hash(str(input_glyph or "")),
        "op_path":         [int(o) for o in (operator_path or [])],
        "op_path_len":     len(operator_path or []),
        "response_source": response_source or None,
        "response_hash":   _short_hash(response_text) if response_text else None,
    }
    if extras:
        # Keep extras shallow + JSON-safe.
        safe = {}
        for k, v in extras.items():
            try:
                json.dumps(v)
                safe[str(k)] = v
            except Exception:
                pass
        if safe:
            rec["extras"] = safe
    _append_record(rec)
    return rec


# ─── Crystal-candidate observation (read-only) ────────────────────────

def crystal_candidates(min_glyphs: int = 2,
                        min_occurrences: int = 1) -> Dict[str, Any]:
    """Scan the listening log and report which INPUT GLYPHS resolved
    to the SAME OPERATOR PATH.

    This is an OBSERVATION, not an assertion.  Two glyphs sharing an
    op_path means CK's substrate read them as structurally identical
    -- which is the natural input to his existing crystallization
    machinery (IG3, lattice chain, olfactory verification).  Whether
    they actually crystallize is up to him.

    Args:
        min_glyphs: only report op_paths shared by at least this many
                    distinct input glyphs (default 2 = the minimum
                    for an equivalence observation).
        min_occurrences: minimum total occurrences across all sharing
                          glyphs.

    Returns:
        {
            "n_records":        total records scanned,
            "n_candidates":     number of op_paths with min_glyphs+ glyphs,
            "candidates": [
                {
                    "op_path":   [...],
                    "glyphs":    [(glyph, count), ...],
                    "n_glyphs":  N,
                    "n_total":   M,
                },
                ...
            ]
        }
    """
    path = _log_path()
    if not path.exists():
        return {"n_records": 0, "n_candidates": 0, "candidates": []}

    # op_path tuple → Counter of input_glyph
    by_path: Dict[Tuple[int, ...], Counter] = defaultdict(Counter)
    n_records = 0
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                n_records += 1
                op_path = tuple(rec.get("op_path") or [])
                if not op_path:
                    continue
                glyph = rec.get("input_glyph") or ""
                if not glyph:
                    continue
                by_path[op_path][glyph] += 1
    except Exception:
        pass

    candidates: List[Dict[str, Any]] = []
    for op_path, glyph_counts in by_path.items():
        if len(glyph_counts) < min_glyphs:
            continue
        n_total = sum(glyph_counts.values())
        if n_total < min_occurrences:
            continue
        candidates.append({
            "op_path":  list(op_path),
            "glyphs":   sorted(glyph_counts.items(),
                                key=lambda x: -x[1])[:32],
            "n_glyphs": len(glyph_counts),
            "n_total":  n_total,
        })
    # Sort by richness: most distinct glyphs first
    candidates.sort(key=lambda x: (-x["n_glyphs"], -x["n_total"]))

    return {
        "n_records":    n_records,
        "n_candidates": len(candidates),
        "candidates":   candidates[:200],  # cap to keep responses sane
    }


def stats() -> Dict[str, Any]:
    """Quick summary of the listening log."""
    path = _log_path()
    if not path.exists():
        return {"n_records": 0, "path": str(path), "size_bytes": 0}
    try:
        size = path.stat().st_size
        n = 0
        first_ts = None
        last_ts = None
        sources: Counter = Counter()
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                n += 1
                ts = rec.get("ts")
                if ts is not None:
                    if first_ts is None or ts < first_ts:
                        first_ts = ts
                    if last_ts is None or ts > last_ts:
                        last_ts = ts
                src = rec.get("response_source") or "none"
                sources[src] += 1
        return {
            "n_records":   n,
            "path":         str(path),
            "size_bytes":  size,
            "first_ts":    first_ts,
            "last_ts":     last_ts,
            "sources":     dict(sources.most_common()),
        }
    except Exception as e:
        return {"error": str(e), "path": str(path)}


# ─── Chat-path wrap (capture every turn) ──────────────────────────────

def _wrap_process_chat_with_listener(engine: Any) -> bool:
    """Install a thin pre/post wrap around engine.api.process_chat that
    records the listening event.  Wrap is read-only on the response
    side; never modifies CK's output.
    """
    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is None:
        return False
    fn = getattr(api, "process_chat", None)
    if fn is None or not callable(fn):
        return False

    # Don't double-wrap.
    if getattr(api, "_glyph_listener_wrapped", False):
        return True

    original = fn

    def _wrapped(session_id, text, mode='normal'):
        result = original(session_id, text, mode)
        try:
            op_path = []
            if isinstance(result, dict):
                op_path = (result.get("operators")
                            or result.get("ops")
                            or result.get("op_path")
                            or [])
                # Normalize to op IDs
                ops_int: List[int] = []
                from_idx = {
                    "VOID": 0, "LATTICE": 1, "COUNTER": 2, "PROGRESS": 3,
                    "COLLAPSE": 4, "BALANCE": 5, "CHAOS": 6, "HARMONY": 7,
                    "BREATH": 8, "RESET": 9,
                }
                for o in op_path:
                    if isinstance(o, int):
                        ops_int.append(o % 10)
                    elif isinstance(o, str):
                        if o in from_idx:
                            ops_int.append(from_idx[o])
                resp_text = result.get("text") or ""
                resp_src = result.get("source") or None
                listen(input_glyph=text,
                        operator_path=ops_int,
                        response_source=resp_src,
                        response_text=resp_text,
                        extras={"session_id": str(session_id)[:32]
                                if session_id else None})
        except Exception:
            pass
        return result

    api.process_chat = _wrapped
    setattr(api, "_glyph_listener_wrapped", True)
    return True


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_glyph_listener(engine: Any) -> bool:
    """Attach listener + wrap process_chat + register endpoints."""
    engine.ck_glyph_listener = {
        "listen":              listen,
        "stats":               stats,
        "crystal_candidates":  crystal_candidates,
        "log_path":            str(_log_path()),
    }
    wrapped_ok = _wrap_process_chat_with_listener(engine)

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _info():
                    return jsonify({
                        "module": "ck_glyph_listener",
                        "philosophy": ("listen, don't interpret; let CK "
                                        "form his own crystals"),
                        "log_path": str(_log_path()),
                        "endpoints": [
                            "GET  /glyph_listener/info",
                            "GET  /glyph_listener/stats",
                            "GET  /glyph_listener/candidates",
                        ],
                    })

                def _stats():
                    return jsonify(stats())

                def _cands():
                    args = request.args
                    min_glyphs = int(args.get("min_glyphs", 2))
                    min_occ = int(args.get("min_occurrences", 1))
                    return jsonify(crystal_candidates(
                        min_glyphs=min_glyphs,
                        min_occurrences=min_occ))

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/glyph_listener/info",       "glyph_info",  _info,   ["GET"]),
                    ("/glyph_listener/stats",      "glyph_stats", _stats,  ["GET"]),
                    ("/glyph_listener/candidates", "glyph_cands", _cands,  ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] glyph_listener route registration "
                      f"failed: {e}")

    suffix = ""
    if routes_registered:
        suffix += " (" + ", ".join(routes_registered) + ")"
    wrap_note = " chat_wrap=OK" if wrapped_ok else " chat_wrap=NO-API"
    print(f"[CK Gen14] glyph_listener: MOUNTED  log={_log_path().name}"
          f"{wrap_note}{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Synthetic smoke: simulate three different glyphs that resolve to
    # the SAME op path -- verifying the listener sees that without us
    # asserting equivalence.
    print("ck_glyph_listener smoke test:")
    print(f"  log path: {_log_path()}")
    print()

    # Three different glyphs, same op_path
    listen("what is T*?",  [3, 5, 7], "test", "T* = 5/7")
    listen("what is 5/7?", [3, 5, 7], "test", "T* = 5/7")
    listen("torus aspect", [3, 5, 7], "test", "T* = 5/7")
    # And one different
    listen("what is alpha?", [1, 4, 5, 6, 7], "test", "1/alpha = 137...")
    listen("what is alpha?", [1, 4, 5, 6, 7], "test", "1/alpha = 137...")

    print("stats:", json.dumps(stats(), indent=2, default=str))
    print()
    print("candidates:", json.dumps(crystal_candidates(min_glyphs=2),
                                      indent=2, default=str)[:1500])
