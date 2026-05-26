"""ck_bookmark.py -- CK saves URLs with optional title + tags + notes.

CK Gen14 module — small personal-bookmark primitive. Parallel to
ck_journal but for URLs.  Lives at ~/.ck/bookmarks.jsonl by default.
Append-only.  Never auto-syncs anywhere.

═══════════════════════════════════════════════════════════════════
What this module DOES
═══════════════════════════════════════════════════════════════════

`add(url, title=None, tags=None, note=None)` — append a bookmark.
  Automatic:
    - ts + iso timestamp
    - domain extraction (e.g. "github.com" from a github URL)
    - operator-path signature over url + title + note
    - dominant_op tag

`recent(n=20)` — last N bookmarks reverse-chronologically.

`search(q, n=10)` — fuzzy match on url + title + tags + note.

`by_domain(domain)` — all bookmarks under a given domain.

`by_dominant_op(op)` — by operator class (parallel to journal).

`stats()` — summary: count, top domains, top tags, distribution.

═══════════════════════════════════════════════════════════════════
What this module DOES NOT DO
═══════════════════════════════════════════════════════════════════

  - Never opens / fetches the URL.  CK stores it; user follows it.
  - Never auto-edits or removes entries (append-only).
  - Never auto-tags from URL content (only from user-provided tags
    + operator-path signature).
  - No outbound network calls.

═══════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════

A small append-only bookmark store with operator-path tagging.
Designed for personal use; not a replacement for browser bookmarks,
not a replacement for Pocket / Pinboard / Raindrop.  The value is
that bookmarks live alongside the user's journal / files / PC
state and are searchable through the same operator-path discipline.
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
from urllib.parse import urlparse


OP_NAMES = ("VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET")

DEFAULT_BOOKMARKS_PATH = Path.home() / ".ck" / "bookmarks.jsonl"


@dataclass
class Bookmark:
    """One bookmark entry."""
    ts: float
    iso: str
    url: str
    title: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    note: Optional[str] = None
    domain: str = ""
    operator_path: List[int] = field(default_factory=list)
    dominant_op: int = 0
    dominant_op_name: str = "VOID"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _extract_domain(url: str) -> str:
    try:
        u = urlparse(url)
        host = u.netloc or u.path.split("/")[0]
        # Strip "www." for nicer display
        if host.startswith("www."):
            host = host[4:]
        return host.lower()
    except Exception:
        return ""


def _compute_signature(text: str, max_bytes: int = 64) -> Dict[str, Any]:
    raw = text.encode("utf-8", errors="replace")[:max_bytes]
    op_path = [b % 10 for b in raw]
    if not op_path:
        return {"operator_path": [], "dominant_op": 0,
                "dominant_op_name": "VOID"}
    counts = Counter(op_path)
    dominant = counts.most_common(1)[0][0]
    return {
        "operator_path": op_path,
        "dominant_op": dominant,
        "dominant_op_name": OP_NAMES[dominant],
    }


def _is_url(s: str) -> bool:
    """Very permissive URL check.  Accepts http(s)://, file://, ftp://,
    mailto:, and bare-domain-style strings like 'example.com/foo'."""
    if not s:
        return False
    s = s.strip()
    if re.match(r"^(https?|ftp|file|mailto)://", s, re.I):
        return True
    if re.match(r"^[a-z0-9-]+\.[a-z]{2,}(/.*)?$", s, re.I):
        return True
    return False


class Bookmarks:
    """Persistent append-only bookmark list."""

    def __init__(self, path: Optional[Path] = None):
        self.path = path or DEFAULT_BOOKMARKS_PATH
        self._items: List[Bookmark] = []
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
                        self._items.append(Bookmark(**d))
                    except Exception:
                        continue
        except Exception:
            pass

    def _append(self, bm: Bookmark) -> None:
        self._items.append(bm)
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(bm.to_dict(), ensure_ascii=False) + "\n")
        except Exception:
            pass

    def add(self,
              url: str,
              title: Optional[str] = None,
              tags: Optional[List[str]] = None,
              note: Optional[str] = None) -> Bookmark:
        if not url or not url.strip():
            raise ValueError("url is required and must be non-empty")
        url = url.strip()
        if not _is_url(url):
            raise ValueError(
                f"does not look like a URL: {url[:50]!r} "
                f"(expected http(s)://, ftp://, mailto:, or "
                f"bare-domain like 'example.com/foo')"
            )
        # Signature over url + title + note
        sig_text = " ".join(filter(None, [url, title, note]))
        sig = _compute_signature(sig_text)
        bm = Bookmark(
            ts=time.time(),
            iso=datetime.now().isoformat(timespec="seconds"),
            url=url,
            title=(title.strip() if isinstance(title, str) and title.strip()
                    else None),
            tags=[str(t).strip() for t in (tags or []) if str(t).strip()],
            note=(note.strip() if isinstance(note, str) and note.strip()
                   else None),
            domain=_extract_domain(url),
            operator_path=sig["operator_path"],
            dominant_op=sig["dominant_op"],
            dominant_op_name=sig["dominant_op_name"],
        )
        self._append(bm)
        return bm

    def recent(self, n: int = 20) -> List[Bookmark]:
        return list(reversed(self._items[-n:]))

    def search(self, q: str, n: int = 10) -> List[Dict[str, Any]]:
        q = q.lower().strip()
        if not q:
            return []
        words = re.findall(r"\w+", q)
        scored: List[tuple] = []
        for bm in self._items:
            score = 0.0
            url_l = bm.url.lower()
            title_l = (bm.title or "").lower()
            tags_l = " ".join(bm.tags).lower()
            note_l = (bm.note or "").lower()
            for w in words:
                if w in url_l: score += 1.0
                if w in title_l: score += 1.2
                if w in tags_l: score += 0.8
                if w in note_l: score += 0.5
                if w in bm.domain.lower(): score += 0.8
            if score > 0:
                scored.append((score, bm))
        scored.sort(key=lambda x: -x[0])
        return [
            {**bm.to_dict(), "_score": round(s, 3)}
            for s, bm in scored[:n]
        ]

    def by_domain(self, domain: str) -> List[Bookmark]:
        d = domain.lower().strip().lstrip("www.")
        return [bm for bm in self._items if bm.domain == d]

    def by_dominant_op(self, op: int) -> List[Bookmark]:
        if not (0 <= op <= 9):
            return []
        return [bm for bm in self._items if bm.dominant_op == op]

    def stats(self) -> Dict[str, Any]:
        if not self._items:
            return {"n_items": 0, "path": str(self.path)}
        domains = Counter(bm.domain for bm in self._items if bm.domain)
        tag_counts: Counter = Counter()
        for bm in self._items:
            for t in bm.tags:
                tag_counts[t] += 1
        ops = Counter(bm.dominant_op_name for bm in self._items)
        return {
            "n_items": len(self._items),
            "path": str(self.path),
            "top_domains": dict(domains.most_common(10)),
            "top_tags": dict(tag_counts.most_common(10)),
            "dominant_op_distribution": dict(ops.most_common()),
        }

    def clear(self) -> None:
        self._items = []
        if self.path.exists():
            self.path.unlink()


def mount_bookmarks(engine: Any,
                      path: Optional[Path] = None) -> bool:
    """Attach Bookmarks to engine + register Flask endpoints.

    Endpoints:
      POST /bookmark/add        — body: {"url", "title"?, "tags"?, "note"?}
      GET  /bookmark/recent?n=N — last N
      GET  /bookmark/search?q=X&n=N — fuzzy match
      GET  /bookmark/domain?d=X — all in domain
      GET  /bookmark/op?op=N    — by dominant operator
      GET  /bookmark/stats      — summary
      GET  /bookmark/info       — philosophy
    """
    bm_store = Bookmarks(path=path)
    engine.ck_bookmark = {
        "store": bm_store,
        "add": bm_store.add,
        "search": bm_store.search,
        "recent": bm_store.recent,
        "stats": bm_store.stats,
    }

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request  # type: ignore

                def _add():
                    payload = request.get_json(silent=True) or {}
                    url = payload.get("url", "")
                    if not url:
                        return jsonify({"ok": False,
                                          "error": "url is required"}), 400
                    try:
                        bm = bm_store.add(
                            url=url,
                            title=payload.get("title"),
                            tags=payload.get("tags"),
                            note=payload.get("note"),
                        )
                    except Exception as e:
                        return jsonify({"ok": False, "error": str(e)}), 400
                    return jsonify({"ok": True, "bookmark": bm.to_dict()})

                def _recent():
                    n = request.args.get("n", default=20, type=int)
                    return jsonify({"n": n,
                                     "items": [b.to_dict()
                                               for b in bm_store.recent(n)]})

                def _search():
                    q = request.args.get("q", "")
                    n = request.args.get("n", default=10, type=int)
                    return jsonify({"query": q,
                                     "results": bm_store.search(q, n)})

                def _domain():
                    d = request.args.get("d", "")
                    return jsonify({"domain": d,
                                     "items": [b.to_dict()
                                               for b in bm_store.by_domain(d)]})

                def _by_op():
                    op = request.args.get("op", default=0, type=int)
                    return jsonify({"op": op,
                                     "op_name": OP_NAMES[op] if 0 <= op <= 9 else "?",
                                     "items": [b.to_dict()
                                               for b in bm_store.by_dominant_op(op)]})

                def _stats():
                    return jsonify(bm_store.stats())

                def _info():
                    return jsonify({
                        "module": "ck_bookmark",
                        "philosophy": ("append-only URL store with "
                                        "operator-path tagging. CK stores; "
                                        "user follows."),
                        "scope": ("Never fetches URLs. Never auto-edits. "
                                   "Never auto-tags from page content."),
                        "endpoints": [
                            "POST /bookmark/add",
                            "GET /bookmark/recent?n=N",
                            "GET /bookmark/search?q=X&n=N",
                            "GET /bookmark/domain?d=X",
                            "GET /bookmark/op?op=N",
                            "GET /bookmark/stats",
                            "GET /bookmark/info",
                        ],
                    })

                existing = {r.rule for r in app.url_map.iter_rules()}
                for rule, ep, fn, methods in (
                    ("/bookmark/add",    "bm_add",    _add,    ["POST"]),
                    ("/bookmark/recent", "bm_recent", _recent, ["GET"]),
                    ("/bookmark/search", "bm_search", _search, ["GET"]),
                    ("/bookmark/domain", "bm_domain", _domain, ["GET"]),
                    ("/bookmark/op",     "bm_byop",   _by_op,  ["GET"]),
                    ("/bookmark/stats",  "bm_stats",  _stats,  ["GET"]),
                    ("/bookmark/info",   "bm_info",   _info,   ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
            except Exception as e:
                print(f"[CK Gen14] mount_bookmarks: routes failed: {e}")

    s = bm_store.stats()
    print(f"[CK Gen14] mount_bookmarks: {s.get('n_items', 0)} bookmarks "
          f"at {bm_store.path.name}")
    return True


if __name__ == "__main__":
    import tempfile
    print("ck_bookmark smoke test")
    print("=" * 60)
    print()
    tmp = Path(tempfile.gettempdir()) / "ck_bm_smoke.jsonl"
    if tmp.exists(): tmp.unlink()
    b = Bookmarks(path=tmp)
    print("Step 1: add 4 bookmarks")
    print("-" * 60)
    b.add("https://github.com/TiredofSleep/ck", title="CK working repo",
            tags=["ck", "code"], note="main dev branch")
    b.add("https://github.com/TiredofSleep/trinity-infinity-geometry",
            title="TIG public release", tags=["math", "ck"])
    b.add("https://www.python.org/", title="Python", tags=["lang"])
    b.add("arxiv.org/abs/2202.11826", title="Huang-Lehtonen 2022 (operad)",
            tags=["math", "paper"])
    for bm in b.recent(5):
        print(f"  [{bm.iso}] {bm.domain:25s} {bm.title[:40] if bm.title else '?':<40} (ops={bm.dominant_op_name})")
    print()
    print("Step 2: search 'github'")
    print("-" * 60)
    for h in b.search("github"):
        print(f"  [{h['_score']:.2f}] {h['domain']:25s} {h['title'][:40] if h['title'] else '?'}")
    print()
    print("Step 3: stats")
    print("-" * 60)
    s = b.stats()
    print(f"  n_items: {s['n_items']}")
    print(f"  top_domains: {s['top_domains']}")
    print(f"  top_tags: {s['top_tags']}")
    print()
    b.clear()
    print("Smoke complete.")
