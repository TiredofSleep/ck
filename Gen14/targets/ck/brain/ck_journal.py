"""ck_journal.py -- CK's append-only notes / journal with operator-path tags.

CK Gen14 module — gives the user a structured place to dump thoughts,
tagged with operator-path signatures so they can be searched semantically
later.  Lives on the user's disk (default `~/.ck/journal.jsonl`),
append-only, never auto-syncs anywhere.

═══════════════════════════════════════════════════════════════════
What this module DOES
═══════════════════════════════════════════════════════════════════

1. `note(text, tags=None, mood=None)` — append a journal entry.
   CK auto-computes:
     - operator_path: byte-mod-10 path over the text (first 64 bytes)
     - dominant_op: the most-frequent operator in the path
     - signature_hash: short content-blind fingerprint (first 16 hex)
     - timestamp: epoch + ISO string
   User-provided:
     - text: the actual note (stored in full — this is the user's own
       data, not third-party content)
     - tags: optional list of strings
     - mood: optional string (e.g. "tired", "flow", "frustrated")

2. `search(query, n=10)` — fuzzy match query against entry text + tags
   + mood.  Returns top-N hits ranked by score.

3. `recent(n=20)` — last N entries chronologically.

4. `today()` — all entries from today (00:00 user-local).

5. `by_dominant_op(op)` — all entries where the dominant_op matches.
   Useful for "what was I writing when I was in COLLAPSE mode?"

═══════════════════════════════════════════════════════════════════
What this module DOES NOT DO
═══════════════════════════════════════════════════════════════════

  - Never sends notes anywhere.  Lives on the user's disk only.
  - Never modifies existing entries (append-only; if you want to
    "edit," append a new entry referencing the old).
  - Never auto-summarizes / auto-categorizes / auto-anything with
    LLM.  The operator-path tagging is deterministic (byte-mod-10).
    Pure heuristic.
  - No outbound network calls.
  - No cloud sync (use Git / Syncthing / Dropbox at the file level
    if you want it on multiple machines).

═══════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════

A small personal-knowledge primitive.  The "operator-path tagging"
is content-blind in the same way `ck_anomaly_detector` is — it lets
the user search across mood/state/operator without CK having to
interpret meaning.  For real semantic search use a vector-embedding
library (sentence-transformers, OpenAI embeddings, etc.); this
module is the small-arch alternative that stays inside CK's
arithmetic-substrate discipline.
"""
from __future__ import annotations

import json
import re
import time
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# ─── Constants ─────────────────────────────────────────────────────

OP_NAMES = ("VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET")

DEFAULT_JOURNAL_PATH = Path.home() / ".ck" / "journal.jsonl"


# ─── Entry dataclass ──────────────────────────────────────────────

@dataclass
class JournalEntry:
    """One journal entry with metadata + user content."""
    ts: float                  # epoch seconds
    iso: str                   # ISO 8601 string for human eyes
    text: str                  # the user's note
    tags: List[str] = field(default_factory=list)
    mood: Optional[str] = None
    operator_path: List[int] = field(default_factory=list)
    dominant_op: int = 0
    dominant_op_name: str = "VOID"
    signature_hash: str = ""   # short content-blind fingerprint

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─── Helpers ──────────────────────────────────────────────────────

def _compute_signature(text: str, max_bytes: int = 64) -> Dict[str, Any]:
    """Compute operator-path + dominant_op + signature_hash for text."""
    raw = text.encode("utf-8", errors="replace")[:max_bytes]
    op_path = [b % 10 for b in raw]
    if not op_path:
        return {
            "operator_path": [],
            "dominant_op": 0,
            "dominant_op_name": "VOID",
            "signature_hash": "",
        }
    counts = Counter(op_path)
    dominant = counts.most_common(1)[0][0]
    # signature_hash: hex-encode first 8 bytes of operator path
    h = "".join(f"{b:x}" for b in raw[:8])
    return {
        "operator_path": op_path,
        "dominant_op": dominant,
        "dominant_op_name": OP_NAMES[dominant],
        "signature_hash": h,
    }


def _iso_now() -> str:
    return datetime.now().isoformat(timespec="seconds")


# ─── Journal class ────────────────────────────────────────────────

class Journal:
    """Append-only journal persisted to a JSONL file."""

    def __init__(self, path: Optional[Path] = None):
        self.path = path or DEFAULT_JOURNAL_PATH
        self._entries: List[JournalEntry] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            with open(self.path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                        self._entries.append(JournalEntry(**d))
                    except Exception:
                        continue
        except Exception:
            pass

    def _append(self, entry: JournalEntry) -> None:
        self._entries.append(entry)
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry.to_dict(),
                                    ensure_ascii=False) + "\n")
        except Exception:
            pass

    def note(self,
              text: str,
              tags: Optional[List[str]] = None,
              mood: Optional[str] = None) -> JournalEntry:
        """Append a new entry. text is REQUIRED; tags + mood optional."""
        if not text or not text.strip():
            raise ValueError("text is required and must be non-empty")
        sig = _compute_signature(text)
        ts = time.time()
        entry = JournalEntry(
            ts=ts,
            iso=_iso_now(),
            text=text.strip(),
            tags=[str(t).strip() for t in (tags or []) if str(t).strip()],
            mood=(mood.strip() if isinstance(mood, str) and mood.strip()
                   else None),
            operator_path=sig["operator_path"],
            dominant_op=sig["dominant_op"],
            dominant_op_name=sig["dominant_op_name"],
            signature_hash=sig["signature_hash"],
        )
        self._append(entry)
        return entry

    def recent(self, n: int = 20) -> List[JournalEntry]:
        """Last N entries in reverse-chronological order."""
        return list(reversed(self._entries[-n:]))

    def today(self) -> List[JournalEntry]:
        """All entries from today (local time, 00:00 onward)."""
        from datetime import date, datetime as _dt
        start_of_day = _dt.combine(date.today(),
                                     _dt.min.time()).timestamp()
        return [e for e in self._entries if e.ts >= start_of_day]

    def by_dominant_op(self, op: int) -> List[JournalEntry]:
        """All entries where the dominant operator matches."""
        if not (0 <= op <= 9):
            return []
        return [e for e in self._entries if e.dominant_op == op]

    def search(self, query: str, n: int = 10) -> List[Dict[str, Any]]:
        """Fuzzy match query against text + tags + mood. Returns
        top-N scored hits."""
        q = query.lower().strip()
        if not q:
            return []
        words = re.findall(r"\w+", q)
        if not words:
            return []
        scored: List[tuple] = []
        for entry in self._entries:
            score = 0.0
            text_l = entry.text.lower()
            tags_l = " ".join(entry.tags).lower()
            mood_l = (entry.mood or "").lower()
            for w in words:
                if w in text_l:
                    # weight: longer match in text = higher
                    score += 1.0 + 0.1 * text_l.count(w)
                if w in tags_l:
                    score += 0.8
                if w in mood_l:
                    score += 0.5
            if score > 0:
                scored.append((score, entry))
        scored.sort(key=lambda x: -x[0])
        return [
            {**e.to_dict(), "_score": round(s, 3)}
            for s, e in scored[:n]
        ]

    def stats(self) -> Dict[str, Any]:
        """Summary of journal contents."""
        if not self._entries:
            return {"n_entries": 0, "path": str(self.path)}
        ops = Counter(e.dominant_op_name for e in self._entries)
        moods = Counter(e.mood for e in self._entries if e.mood)
        tag_counts: Counter = Counter()
        for e in self._entries:
            for t in e.tags:
                tag_counts[t] += 1
        total_chars = sum(len(e.text) for e in self._entries)
        oldest = min(e.ts for e in self._entries)
        newest = max(e.ts for e in self._entries)
        return {
            "n_entries": len(self._entries),
            "path": str(self.path),
            "oldest_ts": oldest,
            "newest_ts": newest,
            "total_chars": total_chars,
            "dominant_op_distribution": dict(ops.most_common()),
            "top_moods": dict(moods.most_common(5)),
            "top_tags": dict(tag_counts.most_common(10)),
        }

    def clear(self) -> None:
        """Wipe in-memory + on-disk. Use carefully."""
        self._entries = []
        if self.path.exists():
            self.path.unlink()


# ─── Engine mount ─────────────────────────────────────────────────

def mount_journal(engine: Any,
                    path: Optional[Path] = None) -> bool:
    """Attach Journal to engine + register Flask endpoints.

    Endpoints (read-mostly; only POST /note writes):
      POST /journal/note         — body: {"text", "tags"?, "mood"?}
      GET  /journal/recent?n=N   — last N entries
      GET  /journal/today        — today's entries
      GET  /journal/search?q=X&n=N — fuzzy search
      GET  /journal/op?op=N      — by dominant operator (0-9)
      GET  /journal/stats        — summary
      GET  /journal/info         — philosophy
    """
    j = Journal(path=path)
    engine.ck_journal = {
        "journal": j,
        "note": j.note,
        "search": j.search,
        "recent": j.recent,
        "today": j.today,
        "by_dominant_op": j.by_dominant_op,
        "stats": j.stats,
    }

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request  # type: ignore

                def _note():
                    payload = request.get_json(silent=True) or {}
                    text = payload.get("text", "")
                    if not text or not str(text).strip():
                        return jsonify({"ok": False,
                                          "error": "text is required"}), 400
                    try:
                        entry = j.note(
                            text=text,
                            tags=payload.get("tags"),
                            mood=payload.get("mood"),
                        )
                    except Exception as e:
                        return jsonify({"ok": False,
                                          "error": str(e)}), 400
                    return jsonify({"ok": True, "entry": entry.to_dict()})

                def _recent():
                    n = request.args.get("n", default=20, type=int)
                    return jsonify({
                        "n": n,
                        "entries": [e.to_dict() for e in j.recent(n)],
                    })

                def _today():
                    return jsonify({
                        "entries": [e.to_dict() for e in j.today()],
                    })

                def _search():
                    q = request.args.get("q", "")
                    n = request.args.get("n", default=10, type=int)
                    return jsonify({"query": q,
                                     "results": j.search(q, n=n)})

                def _by_op():
                    op = request.args.get("op", default=0, type=int)
                    return jsonify({
                        "op": op,
                        "op_name": OP_NAMES[op] if 0 <= op <= 9 else "?",
                        "entries": [e.to_dict()
                                    for e in j.by_dominant_op(op)],
                    })

                def _stats():
                    return jsonify(j.stats())

                def _info():
                    return jsonify({
                        "module": "ck_journal",
                        "philosophy": ("append-only personal journal "
                                        "with operator-path tagging. "
                                        "Lives on user's disk. Never "
                                        "auto-syncs anywhere."),
                        "scope": ("Append-only. Never edits. Never "
                                   "auto-summarizes. Operator-path "
                                   "tagging is byte-mod-10 deterministic, "
                                   "not LLM-derived."),
                        "endpoints": [
                            "POST /journal/note",
                            "GET /journal/recent?n=N",
                            "GET /journal/today",
                            "GET /journal/search?q=X&n=N",
                            "GET /journal/op?op=N",
                            "GET /journal/stats",
                            "GET /journal/info",
                        ],
                    })

                existing = {r.rule for r in app.url_map.iter_rules()}
                for rule, ep, fn, methods in (
                    ("/journal/note",   "j_note",   _note,   ["POST"]),
                    ("/journal/recent", "j_recent", _recent, ["GET"]),
                    ("/journal/today",  "j_today",  _today,  ["GET"]),
                    ("/journal/search", "j_search", _search, ["GET"]),
                    ("/journal/op",     "j_byop",   _by_op,  ["GET"]),
                    ("/journal/stats",  "j_stats",  _stats,  ["GET"]),
                    ("/journal/info",   "j_info",   _info,   ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
            except Exception as e:
                print(f"[CK Gen14] mount_journal: routes failed: {e}")

    s = j.stats()
    print(f"[CK Gen14] mount_journal: {s.get('n_entries', 0)} entries "
          f"at {j.path.name}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────

if __name__ == "__main__":
    import tempfile
    print("ck_journal smoke test")
    print("=" * 60)
    print()
    tmp = Path(tempfile.gettempdir()) / "ck_journal_smoke.jsonl"
    if tmp.exists():
        tmp.unlink()
    j = Journal(path=tmp)

    print("Step 1: add 5 entries")
    print("-" * 60)
    j.note("started working on ck_journal module",
            tags=["dev", "ck"], mood="focused")
    j.note("ran tests, all green",
            tags=["dev", "ck"], mood="satisfied")
    j.note("brief lunch break, walked the dog",
            tags=["personal"], mood="rested")
    j.note("debugged a flaky test in file_orient — Windows mtime issue",
            tags=["dev", "bug", "windows"], mood="annoyed")
    j.note("fixed the flake, ready to push",
            tags=["dev"], mood="ready")
    for e in j.recent(5):
        print(f"  [{e.iso}]  ({e.dominant_op_name:8s})  {e.text[:50]}")
    print()
    print("Step 2: search for 'flaky'")
    print("-" * 60)
    hits = j.search("flaky", n=3)
    for h in hits:
        print(f"  [{h['_score']:.2f}]  {h['text'][:60]}")
    print()
    print("Step 3: stats")
    print("-" * 60)
    s = j.stats()
    for k in ("n_entries", "dominant_op_distribution",
                "top_moods", "top_tags"):
        print(f"  {k}: {s[k]}")
    print()
    print("Step 4: cleanup")
    print("-" * 60)
    j.clear()
    print(f"  cleared; file exists: {tmp.exists()}")
    print()
    print("Smoke test complete.")
