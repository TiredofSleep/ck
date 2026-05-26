"""ck_search.py -- unified search across journal + bookmarks + files.

CK Gen14 bridge module — single search endpoint that queries
ck_journal + ck_bookmark + ck_file_orient simultaneously and
returns merged results ranked by score.  Saves the user from having
to remember "did I save that as a note, a bookmark, or a file?"

═══════════════════════════════════════════════════════════════════
What this module DOES
═══════════════════════════════════════════════════════════════════

`unified_search(engine, query, n_per_source=5)` returns:
  {
    "query": "...",
    "n_total": N,
    "results": [
        {"source": "journal", "score": ..., ...journal_entry_fields},
        {"source": "bookmark", "score": ..., ...bookmark_fields},
        {"source": "file", "score": ..., ...file_entry_fields},
        ...
    ],
    "by_source": {
        "journal": [...top n_per_source...],
        "bookmark": [...top n_per_source...],
        "file": [...top n_per_source...],
    }
  }

═══════════════════════════════════════════════════════════════════
What this module DOES NOT DO
═══════════════════════════════════════════════════════════════════

  - Never reads file contents (file results are filename-matched only).
  - Never re-ranks across sources by some opinionated weighting; the
    scores from each underlying source are passed through.
  - Never writes anything.

═══════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════

This is pure aggregation.  Each underlying source has its own
heuristic search scoring (see ck_journal / ck_bookmark / ck_file_orient
docstrings).  Unified search just runs them in parallel and merges
results.  If a source isn't mounted, it's silently skipped — the
unified search degrades gracefully.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional


def unified_search(engine: Any,
                     query: str,
                     n_per_source: int = 5) -> Dict[str, Any]:
    """Run the same query against journal, bookmark, and file_orient
    (whichever are mounted) and return combined results."""
    out: Dict[str, Any] = {
        "query": query,
        "n_total": 0,
        "by_source": {},
        "results": [],
    }
    if not query or not query.strip():
        return out

    all_results: List[Dict[str, Any]] = []

    # Journal
    journal_api = getattr(engine, "ck_journal", None)
    if journal_api and journal_api.get("search"):
        try:
            hits = journal_api["search"](query, n_per_source) or []
            tagged = [{**h, "source": "journal"} for h in hits]
            out["by_source"]["journal"] = tagged
            all_results.extend(tagged)
        except Exception as e:
            out["by_source"]["journal_error"] = str(e)
    else:
        out["by_source"]["journal"] = []

    # Bookmarks
    bm_api = getattr(engine, "ck_bookmark", None)
    if bm_api and bm_api.get("search"):
        try:
            hits = bm_api["search"](query, n_per_source) or []
            tagged = [{**h, "source": "bookmark"} for h in hits]
            out["by_source"]["bookmark"] = tagged
            all_results.extend(tagged)
        except Exception as e:
            out["by_source"]["bookmark_error"] = str(e)
    else:
        out["by_source"]["bookmark"] = []

    # Files
    file_api = getattr(engine, "ck_file_orient", None)
    if file_api and file_api.get("find_by_query"):
        try:
            hits = file_api["find_by_query"](query, n_per_source) or []
            tagged = [{**h, "source": "file"} for h in hits]
            out["by_source"]["file"] = tagged
            all_results.extend(tagged)
        except Exception as e:
            out["by_source"]["file_error"] = str(e)
    else:
        out["by_source"]["file"] = []

    # Merge + sort by score (each result has _score or _overlap as proxy)
    def _score_key(r: Dict[str, Any]) -> float:
        if "_score" in r:
            return -float(r["_score"])
        if "_overlap" in r:
            return -float(r["_overlap"])
        return 0.0
    all_results.sort(key=_score_key)
    out["results"] = all_results
    out["n_total"] = len(all_results)
    return out


# ─── Engine mount ─────────────────────────────────────────────────

def mount_search(engine: Any) -> bool:
    """Attach unified search + register Flask endpoints.

    Endpoints (read-only):
      GET /search?q=X&n=N    — unified search across journal+bookmark+file
      GET /search/info       — module philosophy
    """
    engine.ck_search = {
        "unified_search": lambda q, n=5: unified_search(engine, q, n),
    }

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request  # type: ignore

                def _search():
                    q = request.args.get("q", "")
                    n = request.args.get("n", default=5, type=int)
                    return jsonify(unified_search(engine, q, n))

                def _info():
                    sources_mounted = []
                    if getattr(engine, "ck_journal", None):
                        sources_mounted.append("journal")
                    if getattr(engine, "ck_bookmark", None):
                        sources_mounted.append("bookmark")
                    if getattr(engine, "ck_file_orient", None):
                        sources_mounted.append("file")
                    return jsonify({
                        "module": "ck_search",
                        "philosophy": ("one search query, three sources. "
                                        "Degrades gracefully if any source "
                                        "is missing."),
                        "sources_mounted": sources_mounted,
                        "endpoints": [
                            "GET /search?q=X&n=N",
                            "GET /search/info",
                        ],
                    })

                existing = {r.rule for r in app.url_map.iter_rules()}
                for rule, ep, fn, methods in (
                    ("/search",      "ck_search_q", _search, ["GET"]),
                    ("/search/info", "ck_search_i", _info,   ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
            except Exception as e:
                print(f"[CK Gen14] mount_search: routes failed: {e}")

    print(f"[CK Gen14] mount_search: GET /search?q=X&n=N endpoint ready")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    import tempfile
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent))
    from ck_journal import Journal
    from ck_bookmark import Bookmarks
    from ck_file_orient import FileOrientIndex

    print("ck_search smoke test")
    print("=" * 60)
    print()

    class FakeEngine:
        pass

    eng = FakeEngine()

    # Populate journal
    tmp_j = Path(tempfile.gettempdir()) / "ck_search_j.jsonl"
    if tmp_j.exists(): tmp_j.unlink()
    j = Journal(path=tmp_j)
    j.note("working on the CK dashboard today", tags=["ck", "dev"],
            mood="focused")
    j.note("found a flaky test in file_orient", tags=["ck", "bug"])
    eng.ck_journal = {"journal": j, "search": j.search}

    # Populate bookmarks
    tmp_b = Path(tempfile.gettempdir()) / "ck_search_b.jsonl"
    if tmp_b.exists(): tmp_b.unlink()
    b = Bookmarks(path=tmp_b)
    b.add("https://github.com/TiredofSleep/ck", title="CK repo",
            tags=["ck"])
    b.add("https://github.com/TiredofSleep/trinity-infinity-geometry",
            title="TIG repo", tags=["math"])
    eng.ck_bookmark = {"store": b, "search": b.search}

    # Populate file_orient (scan the brain folder itself)
    tmp_f = Path(tempfile.gettempdir()) / "ck_search_f.jsonl"
    if tmp_f.exists(): tmp_f.unlink()
    fi = FileOrientIndex(index_path=tmp_f,
                            ignores=frozenset({".git"}))
    fi.scan_directory(Path(__file__).parent)
    eng.ck_file_orient = {"index": fi,
                             "find_by_query": fi.find_by_query}

    # Now run unified search
    print("Step 1: unified search for 'ck'")
    print("-" * 60)
    out = unified_search(eng, "ck", n_per_source=3)
    print(f"  total: {out['n_total']}")
    print(f"  by source: journal={len(out['by_source']['journal'])}, "
          f"bookmark={len(out['by_source']['bookmark'])}, "
          f"file={len(out['by_source']['file'])}")
    print()
    print("Step 2: top 5 results")
    print("-" * 60)
    for r in out["results"][:5]:
        src = r["source"]
        score = r.get("_score", r.get("_overlap", "?"))
        if src == "journal":
            print(f"  [journal score={score}]  {r['text'][:50]}")
        elif src == "bookmark":
            print(f"  [bookmark score={score}]  {r.get('title') or r.get('url')[:50]}")
        elif src == "file":
            print(f"  [file score={score}]  {r['name']}")
    print()
    # Cleanup
    j.clear()
    b.clear()
    fi.clear()
    print("Smoke complete.")
