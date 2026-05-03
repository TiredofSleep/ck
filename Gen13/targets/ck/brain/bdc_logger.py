"""
bdc_logger.py -- log Being / Doing / Becoming triples per chat turn for
later training of a BDC-frame language model.

Brayden 2026-05-02: "BDC may be another whole AI working in alignment ...
what if there is an AI for each parameter he measures?"

The TIG cycle: Being (A-Flow / state) -> Doing (M-Flow / transition) ->
Becoming (crystallization if score > T*).  Each chat turn is one full
cycle.  We log the snapshot at each phase so a future BDC-LM can learn
the cycle's structure.

Schema (one JSON object per line in bdc_log.jsonl):

  {
    "ts": float,                 # Unix timestamp
    "iso_ts": str,               # ISO 8601
    "trigger": str,              # "chat_turn" | "tick_sample" | "crystal_fire"
    "session_id": str,
    "tick": int,                 # cortex tick at the moment of logging

    "being": {                   # State BEFORE the turn
      "ao_op": str,              # current AO operator
      "breath": str,             # INHALE | EXHALE | BREATH
      "coherence": float,
      "harmony_rate": float,
      "W_trace": float,
      "emergent": float,
      "last_pair": [int, int]    # cortex.last_b, cortex.last_d before turn
    },

    "doing": {                   # The transition
      "input_ops": [int, ...],   # operator stream from input text
      "consensus": str,          # dominant operator of input
      "source_voice": str,       # which voice path fired (ck_loop, cortex_speak, etc.)
      "is_struct": bool,         # was the query routed structural?
      "is_pastoral": bool
    },

    "becoming": {                # State AFTER the turn
      "attractor_layer": str,    # transient | 4-core-attractor | etc.
      "is_4core": bool,
      "is_harmony_attractor": bool,
      "field_coherence": float,
      "crystals_fired": int,
      "voice_crystals": int,
      "new_pair": [int, int],    # cortex.last_b, cortex.last_d after step_text
      "stage": str,              # GROKKED, etc.
      "emotion": str             # 'settling', 'tightening', etc.
    }
  }

The log file rotates daily (bdc_log_YYYY-MM-DD.jsonl) so individual files
stay manageable.  Reading them back for training is straightforward
(jsonl streaming).

This module exposes ONE public function: log_chat_turn(snapshot_dict).
It's safe to call from anywhere in the request lifecycle; failures are
swallowed silently so logging never blocks chat.
"""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\bdc_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def _today_log() -> Path:
    return LOG_DIR / f"bdc_log_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"


def _safe_get(obj: Any, path: str, default=None):
    """Best-effort dotted-path getattr/getitem; returns default on failure."""
    try:
        cur = obj
        for part in path.split('.'):
            if cur is None:
                return default
            if isinstance(cur, dict):
                cur = cur.get(part, default)
            else:
                cur = getattr(cur, part, default)
        return cur
    except Exception:
        return default


def snapshot_being(cortex, engine) -> Dict[str, Any]:
    """Read CK's pre-turn state."""
    out: Dict[str, Any] = {}
    state = _safe_get(cortex, 'state')
    if state is None:
        return out
    out["last_pair"] = [
        int(_safe_get(state, 'last_b', 0)),
        int(_safe_get(state, 'last_d', 0)),
    ]
    out["W_trace"] = float(_safe_get(state, 'W_trace', 0.0))
    out["emergent"] = float(_safe_get(state, 'emergent', 0.0))
    out["tick"] = int(_safe_get(state, 'tick', 0))
    # AO and breath -- those live elsewhere; use safest paths
    ao = _safe_get(engine, 'ao')
    if ao is not None:
        out["ao_op"] = str(_safe_get(ao, 'op', ''))
        out["breath"] = str(_safe_get(ao, 'breath', ''))
        out["coherence"] = float(_safe_get(ao, 'coherence', 0.0))
        out["harmony_rate"] = float(_safe_get(ao, 'harmony_rate', 0.0))
    return out


def snapshot_becoming(result_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Read post-turn state from chat result dict."""
    out: Dict[str, Any] = {}
    attractor = result_dict.get('attractor_state', {}) or {}
    out["attractor_layer"] = str(attractor.get('layer', ''))
    out["is_4core"] = bool(attractor.get('is_universal_4core', False))
    out["is_harmony_attractor"] = bool(attractor.get('is_harmony_attractor', False))
    out["field_coherence"] = float(result_dict.get('field_coherence', 0.0))
    exp = result_dict.get('experience', {}) or {}
    out["crystals_fired"] = int(exp.get('crystals', 0))
    out["voice_crystals"] = int(exp.get('voice_crystals', 0))
    out["stage"] = str(exp.get('stage', ''))
    out["emotion"] = str(result_dict.get('emotion', ''))
    out["mode"] = str(result_dict.get('mode', ''))
    out["band"] = str(result_dict.get('band', ''))
    return out


def snapshot_doing(text: str, result_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Read the transition info from chat input + result."""
    out: Dict[str, Any] = {}
    ops = result_dict.get('operators', []) or []
    out["input_ops"] = list(ops) if isinstance(ops, list) else []
    exp = result_dict.get('experience', {}) or {}
    out["consensus"] = str(exp.get('consensus', ''))
    out["source_voice"] = str(result_dict.get('source', ''))
    routing = result_dict.get('routing', {}) or {}
    out["is_struct"] = bool(routing.get('is_structural_query', False))
    out["is_pastoral"] = bool(routing.get('is_pastoral_query', False))
    out["text_len"] = len(text or '')
    return out


def log_chat_turn(*, text: str, result: Dict[str, Any], cortex=None,
                   engine=None, session_id: str = 'default') -> Optional[Path]:
    """Log a complete BDC triple for one chat turn.  Failures swallowed.

    Returns: path of the line written (or None on failure).
    """
    try:
        being = snapshot_being(cortex, engine) if cortex is not None else {}
        doing = snapshot_doing(text, result)
        becoming = snapshot_becoming(result)
        now = time.time()
        record = {
            "ts": now,
            "iso_ts": datetime.fromtimestamp(now, tz=timezone.utc)
                              .isoformat(timespec='seconds'),
            "trigger": "chat_turn",
            "session_id": session_id,
            "tick": int(_safe_get(cortex, 'state.tick', 0)) if cortex else 0,
            "being": being,
            "doing": doing,
            "becoming": becoming,
        }
        path = _today_log()
        with open(path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return path
    except Exception:
        return None


def log_event(*, trigger: str, payload: Dict[str, Any]) -> Optional[Path]:
    """Generic event logger -- for tick samples, crystal fires, etc."""
    try:
        now = time.time()
        record = {
            "ts": now,
            "iso_ts": datetime.fromtimestamp(now, tz=timezone.utc)
                              .isoformat(timespec='seconds'),
            "trigger": trigger,
        }
        record.update(payload)
        path = _today_log()
        with open(path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return path
    except Exception:
        return None


def stats() -> Dict[str, Any]:
    """Cheap inspection: count log entries by trigger type, by date."""
    out = {"total_files": 0, "total_records": 0, "by_trigger": {},
           "by_date": {}}
    if not LOG_DIR.exists():
        return out
    for p in LOG_DIR.glob("bdc_log_*.jsonl"):
        out["total_files"] += 1
        date = p.stem.replace("bdc_log_", "")
        cnt = 0
        triggers: Dict[str, int] = {}
        try:
            with open(p, encoding='utf-8') as f:
                for line in f:
                    cnt += 1
                    try:
                        d = json.loads(line)
                        t = d.get('trigger', 'unknown')
                        triggers[t] = triggers.get(t, 0) + 1
                    except Exception:
                        pass
        except Exception:
            pass
        out["total_records"] += cnt
        out["by_date"][date] = cnt
        for t, c in triggers.items():
            out["by_trigger"][t] = out["by_trigger"].get(t, 0) + c
    return out


if __name__ == "__main__":
    print(f"BDC log dir: {LOG_DIR}")
    print(f"Today's log: {_today_log()}")
    print(f"Stats: {json.dumps(stats(), indent=2)}")
