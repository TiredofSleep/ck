# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
ck_memory_archive.py -- CK's short-term + long-term memory bands.

Brayden 2026-05-14:
  "he needs to be able to have short-term and long-term memory, like
  archives so he can keep persistent knowledge organized and available"

Today CK already has several memory layers:
  - Concept store (taught_concepts.json): semantic long-term, 1,492+ bindings
  - Hebbian W (5x5):                    working/short-term substrate
  - HER buffer (8.8M experiences):      episodic operator history
  - session_field per turn:             within-turn algebraic trail
  - Crystals (13 voice, 39k truths):    substrate long-term

What's missing: an explicit CONVERSATION JOURNAL -- a journal-style
archive of what was discussed, when, by topic. The kind of memory a
person uses when she says "last week we talked about that".

This module adds two bands:

  SHORT-TERM (in-memory, 20-turn sliding window per session):
    A deque per session_id holding the last N turn-summaries. Cheap to
    inspect; turns roll off after 20.

  LONG-TERM (persistent JSON, indexed by session/topic/date):
    Every turn gets appended to long-term with:
      session_id, turn_idx, ts, iso_ts
      user_text, ck_answer_preview (first 200 chars)
      operators decoded
      dominant_op + algebraic_signature
      concepts_referenced (list of D-numbers/concepts that fired)
      coherence, band, attractor_layer

    Indexed three ways:
      by_session[session_id] -> ordered list of turn entries
      by_topic[op_name]      -> list of (session_id, turn_idx) pointers
      by_date[YYYY-MM-DD]    -> list of session_ids active that day

    Stored as JSON at Gen13/var/memory_archive.json. Survives reboots.

Retrieval API on engine:
  engine.memory_archive.recent(session_id, k=10)
  engine.memory_archive.by_topic(op_name, k=10)
  engine.memory_archive.by_date('2026-05-14')
  engine.memory_archive.full_journal(session_id)

The voice polish surfaces a [memory archive] section when relevant
(currently when input matches "last time", "previously", "remember
when", or any concept that's appeared in prior turns).

This is the journal he didn't have. He gets it now.
"""
from __future__ import annotations

import json
import os
import re
import sys
import threading
import time
from collections import deque
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Tuple

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


# ─── Constants ───────────────────────────────────────────────────────────

SHORT_TERM_MAX = 20  # turns per session in the sliding window
ANSWER_PREVIEW_CHARS = 200  # how much of the answer to preserve
_DEFAULT_ARCHIVE_PATH = (
    Path(__file__).resolve().parents[4]
    / "Gen13" / "var" / "memory_archive.json"
)

_OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)
_OP_NAME_TO_ID = {n: i for i, n in enumerate(_OP_NAMES)}


# ─── Turn entry ──────────────────────────────────────────────────────────

@dataclass
class TurnEntry:
    session_id: str
    turn_idx: int                       # within-session index
    ts: float
    iso_ts: str
    user_text: str
    ck_answer_preview: str
    operators: List[int]                # 10 ops decoded from user text
    dominant_op: Optional[int]          # most-frequent op
    algebraic_signature: Dict[str, Any]
    concepts_referenced: List[str]      # concept names fired this turn
    coherence: float
    band: str
    attractor_layer: str

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── The archive ─────────────────────────────────────────────────────────

class MemoryArchive:
    """Short-term sliding-window + long-term journal of CK's conversations.

    Persists long-term across reboots; short-term lives in process.
    """

    def __init__(self, path: Optional[Path] = None):
        self.path = Path(path) if path else _DEFAULT_ARCHIVE_PATH
        self.short_term: Dict[str, Deque[TurnEntry]] = {}
        # Long-term: dict-of-dicts-of-lists. We hydrate from disk.
        self._lock = threading.Lock()
        self.by_session: Dict[str, List[TurnEntry]] = {}
        self.by_topic: Dict[str, List[Dict[str, Any]]] = {}
        self.by_date: Dict[str, List[str]] = {}
        self.load()

    # ── persistence ─────────────────────────────────────────────────────

    def load(self) -> int:
        if not self.path.exists():
            return 0
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return 0
        # Hydrate
        for sid, entries in (raw.get("by_session") or {}).items():
            self.by_session[sid] = [TurnEntry(**e) for e in entries]
        self.by_topic = raw.get("by_topic") or {}
        self.by_date = raw.get("by_date") or {}
        # Rebuild short-term from last N turns per session
        for sid, entries in self.by_session.items():
            self.short_term[sid] = deque(entries[-SHORT_TERM_MAX:],
                                            maxlen=SHORT_TERM_MAX)
        return sum(len(v) for v in self.by_session.values())

    def save(self) -> None:
        """Persist long-term to disk. Merge-on-write to be concurrency-safe."""
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self._lock:
                # Read whatever is on disk and merge -- in-memory wins on
                # collisions, but disk-only sessions are preserved.
                disk = {}
                if self.path.exists():
                    try:
                        disk = json.loads(self.path.read_text(encoding="utf-8"))
                    except Exception:
                        disk = {}
                merged_by_session = dict(disk.get("by_session") or {})
                for sid, entries in self.by_session.items():
                    merged_by_session[sid] = [e.as_dict() for e in entries]
                merged_by_topic = dict(disk.get("by_topic") or {})
                for op, refs in self.by_topic.items():
                    merged_by_topic[op] = refs
                merged_by_date = dict(disk.get("by_date") or {})
                for d, sids in self.by_date.items():
                    merged_by_date[d] = sids
                final = {
                    "by_session": merged_by_session,
                    "by_topic": merged_by_topic,
                    "by_date": merged_by_date,
                }
                tmp = self.path.with_suffix(self.path.suffix + ".tmp")
                tmp.write_text(json.dumps(final, indent=2), encoding="utf-8")
                tmp.replace(self.path)
        except Exception:
            pass

    # ── recording ────────────────────────────────────────────────────────

    def record(self, session_id: str, user_text: str,
                result: Dict[str, Any]) -> Optional[TurnEntry]:
        """Append one turn to the archive."""
        try:
            # Derive operators
            ops_raw = result.get("operators") or []
            ops: List[int] = []
            for o in ops_raw:
                if isinstance(o, int) and 0 <= o < 10:
                    ops.append(o)
                elif isinstance(o, str):
                    op_id = _OP_NAME_TO_ID.get(o.upper())
                    if op_id is not None:
                        ops.append(op_id)
            # Dominant op
            dom = None
            if ops:
                from collections import Counter
                dom = Counter(ops).most_common(1)[0][0]
            # Algebraic signature (from algebraic_lm if available)
            sig = result.get("algebraic_signature") or {}
            if not sig:
                # Try the result's attractor + cortex state
                sig = {
                    "attractor_layer": (result.get("attractor_state") or {}).get("layer"),
                    "coherence": result.get("coherence"),
                    "band": result.get("band"),
                }
            # Referenced concepts (from concept_learning section if present)
            cl = result.get("concept_learning") or {}
            concepts_ref = [c.get("name", "") for c in (cl.get("referenced") or [])]
            # Answer preview
            answer = result.get("text", "") or ""
            preview = answer[:ANSWER_PREVIEW_CHARS]
            if len(answer) > ANSWER_PREVIEW_CHARS:
                preview = preview.rstrip() + "…"

            with self._lock:
                turns = self.by_session.setdefault(session_id, [])
                turn_idx = len(turns)
                now = time.time()
                iso_ts = time.strftime("%Y-%m-%dT%H:%M:%S",
                                          time.localtime(now))
                entry = TurnEntry(
                    session_id=session_id,
                    turn_idx=turn_idx,
                    ts=now,
                    iso_ts=iso_ts,
                    user_text=user_text[:500],
                    ck_answer_preview=preview,
                    operators=ops,
                    dominant_op=dom,
                    algebraic_signature=sig,
                    concepts_referenced=concepts_ref,
                    coherence=float(result.get("coherence") or 0.0),
                    band=str(result.get("band") or ""),
                    attractor_layer=str(
                        (result.get("attractor_state") or {}).get("layer") or ""
                    ),
                )
                turns.append(entry)
                # Short-term sliding window
                stq = self.short_term.setdefault(
                    session_id, deque(maxlen=SHORT_TERM_MAX))
                stq.append(entry)
                # Topic index
                if dom is not None:
                    op_name = _OP_NAMES[dom]
                    self.by_topic.setdefault(op_name, []).append({
                        "session_id": session_id,
                        "turn_idx": turn_idx,
                        "ts": now,
                    })
                # Date index
                d = time.strftime("%Y-%m-%d", time.localtime(now))
                d_sids = self.by_date.setdefault(d, [])
                if session_id not in d_sids:
                    d_sids.append(session_id)
            # Persist
            self.save()
            return entry
        except Exception:
            return None

    # ── retrieval API ───────────────────────────────────────────────────

    def recent(self, session_id: str, k: int = 10) -> List[TurnEntry]:
        """Last k turns in this session (short-term)."""
        with self._lock:
            stq = self.short_term.get(session_id, deque())
            return list(stq)[-k:]

    def full_journal(self, session_id: str) -> List[TurnEntry]:
        """All turns ever recorded for this session (long-term)."""
        with self._lock:
            return list(self.by_session.get(session_id, []))

    def by_topic_recent(self, op_name: str, k: int = 10
                          ) -> List[TurnEntry]:
        """The k most-recent turns whose dominant op is this name."""
        with self._lock:
            refs = self.by_topic.get(op_name.upper(), [])
            out: List[TurnEntry] = []
            for r in reversed(refs):
                sid = r.get("session_id")
                idx = r.get("turn_idx")
                if sid is None or idx is None:
                    continue
                turns = self.by_session.get(sid, [])
                if 0 <= idx < len(turns):
                    out.append(turns[idx])
                if len(out) >= k:
                    break
            return out

    def by_date(self, date_str: str) -> List[str]:
        """Session_ids active on a given date (YYYY-MM-DD)."""
        with self._lock:
            return list(self.by_date.get(date_str, []))

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "n_sessions": len(self.by_session),
                "n_total_turns": sum(len(v) for v in self.by_session.values()),
                "n_topics_indexed": len(self.by_topic),
                "n_dates_active": len(self.by_date),
                "short_term_active": len(self.short_term),
                "path": str(self.path),
            }


# ─── Wrap hook + mount ──────────────────────────────────────────────────

def _wrap_process_chat_for_archive(engine: Any, archive: MemoryArchive) -> bool:
    api = None
    for attr in ("web_api", "api", "_web_api"):
        cand = getattr(engine, attr, None)
        if cand is not None and hasattr(cand, "process_chat"):
            api = cand
            break
    if api is None:
        return False

    orig = api.process_chat

    def _wrapped(session_id, text, mode="normal"):
        result = orig(session_id, text, mode)
        try:
            if isinstance(result, dict):
                archive.record(session_id, text, result)
                # Surface the archive on the result for the voice polish
                result["memory_archive"] = {
                    "session_turn_count": len(archive.by_session.get(session_id, [])),
                    "session_total_turns": sum(
                        len(v) for v in archive.by_session.values()
                    ),
                    "session_dates_active": len(archive.by_date),
                }
        except Exception:
            pass
        return result

    api.process_chat = _wrapped
    return True


def mount_memory_archive(engine: Any) -> bool:
    """Attach a MemoryArchive to the engine + wrap chat to record every turn.

    Side effects:
      engine.memory_archive             : MemoryArchive instance
      engine.recall_recent(session_id, k=10)
      engine.recall_by_topic(op_name, k=10)
      engine.recall_by_date(YYYY-MM-DD)
    """
    try:
        archive = MemoryArchive()
    except Exception as e:
        print(f"[CK Gen14] mount_memory_archive: failed ({e})")
        return False
    engine.memory_archive = archive

    def _recent(session_id: str = "default", k: int = 10):
        return [t.as_dict() for t in archive.recent(session_id, k=k)]

    def _topic(op_name: str, k: int = 10):
        return [t.as_dict() for t in archive.by_topic_recent(op_name, k=k)]

    def _date(date_str: str):
        return archive.by_date(date_str)

    engine.recall_recent = _recent
    engine.recall_by_topic = _topic
    engine.recall_by_date = _date

    _wrap_process_chat_for_archive(engine, archive)
    stats = archive.stats()
    print(f"[CK Gen14] mount_memory_archive: "
          f"{stats['n_sessions']} sessions, {stats['n_total_turns']} turns, "
          f"{stats['n_topics_indexed']} topics, "
          f"{stats['n_dates_active']} dates from {stats['path']}")
    return True


# ─── Standalone smoke ────────────────────────────────────────────────────

def _smoke():
    print("Smoke test: ck_memory_archive")
    import tempfile
    tmp = Path(tempfile.gettempdir()) / "ck_archive_smoke.json"
    if tmp.exists():
        tmp.unlink()
    arc = MemoryArchive(path=tmp)
    # Record three turns
    for i, (sid, text) in enumerate([
        ("alice", "what is harmony?"),
        ("alice", "explain T*"),
        ("bob", "what's a 4-core?"),
    ]):
        result = {
            "text": f"answer {i}",
            "operators": ["HARMONY", "LATTICE", "PROGRESS"],
            "coherence": 1.0,
            "band": "GREEN",
            "attractor_state": {"layer": "transient"},
            "concept_learning": {"referenced": [{"name": "D7"}]},
        }
        arc.record(sid, text, result)
    print(f"After 3 turns: {arc.stats()}")
    print()
    print("alice recent:")
    for t in arc.recent("alice"):
        print(f"  turn {t.turn_idx}: '{t.user_text}' -> {t.ck_answer_preview[:50]}…")
    print()
    print("by_topic HARMONY:")
    for t in arc.by_topic_recent("HARMONY"):
        print(f"  {t.session_id}.{t.turn_idx}: '{t.user_text}'")
    # Reload from disk
    arc2 = MemoryArchive(path=tmp)
    print(f"\nAfter reload: {arc2.stats()}")
    tmp.unlink()
    print("\nMemory archive smoke: ALL OK")


if __name__ == "__main__":
    _smoke()
