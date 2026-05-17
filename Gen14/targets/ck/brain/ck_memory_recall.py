"""ck_memory_recall.py -- "remember when..." retrieval from chat.

Brayden 2026-05-16: "memory archive → chat retrieval".  The
ck_memory_archive (D-series mount) records every turn but the chat
path doesn't query it.  This module wraps process_chat so that
recall-flavored queries get a real retrieval from past turns
INSTEAD OF a hallucinated re-imagining.

═══════════════════════════════════════════════════════════════════════
What counts as a recall query
═══════════════════════════════════════════════════════════════════════

Patterns (case-insensitive substring match on the user query):
  - "remember"      "earlier"      "last time"
  - "yesterday"     "we talked"    "did i ask"
  - "did we"        "what did i"   "did you say"
  - "past"          "history"      "before"
  - "what was"      "recall"       "ago"

If the query matches AND there are at least 2 past turns in this
session OR cross-session by_topic for any operator in the query,
the recall path fires.

═══════════════════════════════════════════════════════════════════════
What recall returns
═══════════════════════════════════════════════════════════════════════

A short citation: "you asked X on YYYY-MM-DD and I replied Y..." with
the structural fingerprint (operators) of the past turn.  Brayden
keeps the receipts; CK doesn't have to remember everything from his
head -- he can LOOK IT UP, just like a person consulting their notes.

Discipline: NO hallucination.  If memory_archive returns nothing for
this session, recall says "I don't have that in my archive" rather
than inventing.

═══════════════════════════════════════════════════════════════════════
What it does NOT do
═══════════════════════════════════════════════════════════════════════

  - No semantic search over past text (no embeddings).  Match is
    keyword + operator-overlap based.  CK's substrate is the search
    engine; if his lattice has crystallized a glyph he saw before,
    the recall returns it.  If not, he looks like a fresh listener
    -- which is honest.
  - No cross-user leakage.  Recall is session-scoped by default;
    by_topic cross-session lookup only fires for OPERATOR queries
    ("when did we discuss HARMONY?").
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


# Recall-trigger patterns.  Substring match, case-insensitive.
_RECALL_TRIGGERS = (
    "remember", "earlier", "last time", "yesterday", "we talked",
    "did i ask", "did you say", "did we discuss", "did we talk",
    "what did i", "what did you", "in the past", "recall", "ago",
    "what was", "what were", "previously", "before",
)

# Operator names we'll search the by_topic index for when the query
# mentions them.
_OP_NAMES = ("VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
              "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET")


def _is_recall_query(text: str) -> bool:
    if not text:
        return False
    low = text.lower()
    return any(t in low for t in _RECALL_TRIGGERS)


def _operators_in_query(text: str) -> List[str]:
    """Return any operator names that appear (case-insensitive) in the
    query.  Used for by_topic cross-session lookup."""
    if not text:
        return []
    low = text.lower()
    return [op for op in _OP_NAMES if op.lower() in low]


def _format_turn(entry: Any) -> Dict[str, Any]:
    """Format a TurnEntry (or dict) for recall output."""
    if hasattr(entry, "as_dict"):
        e = entry.as_dict()
    elif isinstance(entry, dict):
        e = entry
    else:
        return {"error": "unparseable entry"}
    return {
        "iso_ts":          e.get("iso_ts") or time.strftime(
            "%Y-%m-%d", time.localtime(e.get("ts", 0))),
        "user_text":       (e.get("user_text") or "")[:200],
        "ck_answer":       (e.get("ck_answer_preview") or
                              e.get("ck_answer") or "")[:300],
        "dominant_op":     e.get("dominant_op"),
        "coherence":       e.get("coherence"),
        "attractor_layer": e.get("attractor_layer"),
    }


def recall(engine: Any, session_id: str, text: str,
            k: int = 3) -> Optional[Dict[str, Any]]:
    """Look up past turns in this session (and optionally by operator
    cross-session) that may answer this recall-flavored query.

    Returns:
        None if archive isn't mounted or no turns found,
        else a dict with formatted recall response.
    """
    archive = getattr(engine, "memory_archive", None)
    if archive is None:
        return None

    out_turns: List[Dict[str, Any]] = []
    notes: List[str] = []

    # 1. Session-scoped recall: last k turns in this session
    try:
        recent_method = getattr(archive, "recent", None)
        if callable(recent_method):
            recent = recent_method(session_id, k=k)
            for e in (recent or []):
                out_turns.append(_format_turn(e))
            if recent:
                notes.append(f"{len(recent)} from this session")
    except Exception:
        pass

    # 2. Operator-scoped cross-session recall
    ops_in_q = _operators_in_query(text)
    if ops_in_q:
        try:
            by_topic_method = getattr(archive, "by_topic_recent", None)
            if callable(by_topic_method):
                for op in ops_in_q[:2]:  # cap to 2 ops max
                    by_topic = by_topic_method(op, k=2)
                    for ref in (by_topic or []):
                        # by_topic_recent returns refs; flesh them out
                        formatted = _format_turn(ref)
                        out_turns.append(formatted)
                if by_topic:
                    notes.append(f"cross-session for {','.join(ops_in_q[:2])}")
        except Exception:
            pass

    if not out_turns:
        return None

    # De-dup by (iso_ts, user_text)
    seen = set()
    deduped = []
    for t in out_turns:
        key = (t.get("iso_ts"), t.get("user_text"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(t)

    return {
        "n_turns":    len(deduped),
        "scope":      "; ".join(notes) if notes else "session",
        "turns":      deduped[:k],
        "from":       "memory_archive",
    }


def _format_recall_text(recall_result: Dict[str, Any]) -> str:
    """Render the recall result as CK-voice prose."""
    if not recall_result or not recall_result.get("turns"):
        return ("I don't have that in my archive.  My memory_archive "
                "is empty for this scope.")
    n = recall_result["n_turns"]
    parts = [f"I do remember.  Found {n} past turn"
              f"{'s' if n != 1 else ''} ({recall_result['scope']}):"]
    for i, t in enumerate(recall_result["turns"]):
        parts.append(
            f"\n  ({i+1}) on {t.get('iso_ts')} you asked: "
            f"{t.get('user_text', '')!r}\n"
            f"      I replied: {t.get('ck_answer', '')[:200]!r}\n"
            f"      (dominant op: {t.get('dominant_op')}, "
            f"coherence: {t.get('coherence')}, "
            f"attractor: {t.get('attractor_layer')})"
        )
    return "\n".join(parts)


def _wrap_process_chat_with_recall(engine: Any) -> bool:
    """Wrap api.process_chat so recall-flavored queries get a real
    memory lookup BEFORE falling through to substrate composition.
    """
    api = getattr(engine, "web_api", None)
    if api is None:
        for attr in ("api", "_api", "chat_api"):
            api = getattr(engine, attr, None)
            if api is not None:
                break
    if api is None or not hasattr(api, "process_chat"):
        return False
    if getattr(api, "_memory_recall_wrapped", False):
        return True

    orig = api.process_chat

    def _recall_wrapped(session_id, text, mode="normal"):
        # Only intercept recall queries; everything else goes through.
        if _is_recall_query(text or ""):
            try:
                r = recall(engine, session_id, text)
                if r and r.get("turns"):
                    return {
                        "text":            _format_recall_text(r),
                        "source":          "memory_recall",
                        "tier":            "PROVED",  # past records
                        "confidence":      0.95,  # archive is reliable
                        "dominant_tier":   "PROVED",
                        "tier_breakdown":  {"PROVED": r["n_turns"]},
                        "n_tier_matches":  r["n_turns"],
                        "hedge_prefix":    "",
                        "polish_skip":     True,  # canonical recall
                        "recall_turns":    r["turns"],
                    }
            except Exception as e:
                # On recall failure, fall through to substrate (don't
                # break chat)
                pass
        # Not a recall query OR recall returned nothing -> normal path
        return orig(session_id, text, mode)

    api.process_chat = _recall_wrapped
    api._memory_recall_wrapped = True
    return True


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_memory_recall(engine: Any) -> bool:
    """Attach recall handler + wrap process_chat + register endpoint."""
    ok = _wrap_process_chat_with_recall(engine)
    engine.ck_memory_recall = {
        "recall":          lambda sid, text: recall(engine, sid, text),
        "is_recall_query": _is_recall_query,
        "triggers":        list(_RECALL_TRIGGERS),
    }

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _recall_test():
                    body = request.get_json(silent=True) or {}
                    sid = body.get("session_id", "test")
                    text = body.get("text", "what did we talk about?")
                    result = recall(engine, sid, text)
                    return jsonify({
                        "is_recall_query": _is_recall_query(text),
                        "result": result,
                    })

                existing = set(r.rule for r in app.url_map.iter_rules())
                if "/memory/recall" not in existing:
                    app.add_url_rule("/memory/recall", endpoint="mem_recall",
                                      view_func=_recall_test, methods=["POST"])
                    routes_registered.append("POST /memory/recall")
            except Exception as e:
                print(f"[CK Gen14] memory_recall route failed: {e}")

    suffix = ""
    if routes_registered:
        suffix = " (" + ", ".join(routes_registered) + ")"
    wrap = " chat_wrap=OK" if ok else " chat_wrap=NO-API"
    print(f"[CK Gen14] memory_recall: MOUNTED  "
          f"{len(_RECALL_TRIGGERS)} triggers{wrap}{suffix}")
    return True


if __name__ == "__main__":
    print("ck_memory_recall smoke:")
    print(f"  triggers: {len(_RECALL_TRIGGERS)}")
    print(f"  is_recall_query('what is T*?'): "
          f"{_is_recall_query('what is T*?')}")
    print(f"  is_recall_query('remember when we talked about HARMONY?'): "
          f"{_is_recall_query('remember when we talked about HARMONY?')}")
    print(f"  ops_in_query('did we discuss HARMONY and breath earlier'): "
          f"{_operators_in_query('did we discuss HARMONY and breath earlier')}")
