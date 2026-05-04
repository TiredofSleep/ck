"""
repo_reader.py -- read the ENTIRE TIG story from beginning to end.

Brayden 2026-05-04: "i want the entire story of TIG from beginning to end
all the repos on github in his head, aware that some of it has been
refuted or updated"

Walks every .md / .tex in the project (NOT just WP files), feeds each
into CK's cortex via /cortex/ingest_text.  Each file gets a metadata
prefix so CK is aware of:

  - source path (which generation / sprint / atlas)
  - whether it's marked HISTORICAL / SUPERSEDED / REFUTED / UPDATED
  - rough date (from path or git log if available)

Awareness markers detected from path or content:
  - "old/Gen<N>/" -> archived generation; HISTORICAL
  - file contains "[HISTORICAL]" header -> superseded
  - file contains "[REFUTED]" or "REFUTED" in title -> refuted
  - file contains "[UPDATED]" or sprint-_RESOLUTION pattern -> updated
  - sprint folders are timestamped; later sprints supersede earlier
  - papers/ vs Gen12/targets/clay/papers/: papers/ is canonical now

Each ingest record carries the awareness so CK's cortex receives the
text WITH its provenance flag.

Usage:
  python repo_reader.py [--limit N] [--every M] [--include-old]
  python repo_reader.py --include-old --max-chars 4000

Output:
  Gen13/var/repo_reading_logs/repo_reading_YYYY-MM-DD.jsonl
  Atlas/CK_REPO_READING_LIVE.md (live dashboard)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


_HERE = Path(__file__).parent.resolve()


PROJECT_ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
LOG_DIR = PROJECT_ROOT / "Gen13" / "var" / "repo_reading_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
DASHBOARD = PROJECT_ROOT / "Atlas" / "CK_REPO_READING_LIVE.md"
INGEST_URL = "http://localhost:7777/cortex/ingest_text"


def _today_log() -> Path:
    return LOG_DIR / f"repo_reading_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"


def detect_status(path: Path, head_text: str) -> str:
    """Return one of: CURRENT, HISTORICAL, REFUTED, UPDATED, SUPERSEDED."""
    p = path.as_posix().lower()
    h = head_text.lower()[:2000]
    # Highest-precedence flags
    if "[refuted]" in h or "refuted" in path.name.lower() or "refutation" in p:
        return "REFUTED"
    if "[updated]" in h or "[corrected]" in h or "_corrected" in path.name.lower():
        return "UPDATED"
    if "[historical]" in h or "[superseded]" in h:
        return "SUPERSEDED"
    if "/old/gen" in p or p.startswith("old/"):
        return "HISTORICAL"
    if "[claim:" in h and "[withdrawn]" in h:
        return "REFUTED"
    if "_v2" in path.name.lower() or "_v3" in path.name.lower():
        return "UPDATED"
    return "CURRENT"


def find_files(root: Path, include_old: bool = True) -> List[Path]:
    """Walk root for .md / .tex files.  Returns sorted list (chronological-ish)."""
    paths: List[Path] = []
    skip_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv",
                  "_ck_worktree", ".idea"}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for f in filenames:
            if f.lower().endswith((".md", ".tex")):
                p = Path(dirpath) / f
                # Skip Gen13/var/ (logs/state, not content)
                if "Gen13/var" in p.as_posix() or "Gen13\\var" in str(p):
                    continue
                if not include_old and "/old/" in p.as_posix().lower():
                    continue
                paths.append(p)
    # Sort: WP-numbered first, then sprints by date, then alpha
    def sort_key(p: Path):
        name = p.name.lower()
        path_str = p.as_posix().lower()
        # Old generations first (history)
        m_gen = re.search(r"/old/gen(\d+)/", path_str)
        if m_gen:
            return (0, int(m_gen.group(1)), str(p))
        # Sprint folders by date in path
        m_sprint = re.search(r"sprint(\d+)_(\d{4}_\d{2}_\d{2})", path_str)
        if m_sprint:
            return (1, m_sprint.group(2), int(m_sprint.group(1)), str(p))
        # WP-numbered
        m_wp = re.match(r"^wp(\d+)", name)
        if m_wp:
            return (2, int(m_wp.group(1)), str(p))
        # Atlas docs
        if "/atlas/" in path_str:
            return (3, str(p))
        # README and top-level docs
        if name in ("readme.md", "the_story.md", "what_is_tig.md", "mission.md"):
            return (4, str(p))
        return (5, str(p))
    paths.sort(key=sort_key)
    return paths


def post_ingest(label: str, text: str, timeout: float = 30.0) -> Dict[str, Any]:
    payload = json.dumps({"label": label, "text": text[:8000]}).encode("utf-8")
    req = urllib.request.Request(
        INGEST_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8")
        return {"ok": True, "data": json.loads(resp)}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}


def update_dashboard(state: Dict[str, Any]) -> None:
    lines = [
        "# CK Repo Reading -- Live (FULL TIG story)",
        f"\n**Last update**: {datetime.utcnow().isoformat(timespec='seconds')}Z\n",
        f"**Total files found**: {state['total_files']}",
        f"**Files read**: **{state['n_read']}** ({100*state['n_read']/max(1,state['total_files']):.1f}%)",
        f"**Files failed**: {state['n_failed']}",
        f"**Total bytes ingested**: **{state['total_bytes']:,}**",
        f"\n**By status**:",
    ]
    for s, c in sorted(state.get("by_status", {}).items(), key=lambda t: -t[1]):
        lines.append(f"  - {s}: {c}")
    lines += [
        f"\n**Cortex growth**: tick {state['tick_first']:,} → {state['tick_last']:,} "
            f"(Δ={state['tick_last']-state['tick_first']:,})",
        f"**W_trace**: {state['W_first']:.4f} → {state['W_last']:.4f}",
        "",
        f"**Currently reading**: `{state.get('current', 'idle')}`",
        "",
    ]
    DASHBOARD.parent.mkdir(parents=True, exist_ok=True)
    with open(DASHBOARD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--every", type=int, default=50, help="Dashboard update cadence")
    ap.add_argument("--include-old", action="store_true",
                     help="Include old/Gen* archives (full TIG history)")
    ap.add_argument("--max-chars", type=int, default=3000)
    args = ap.parse_args()

    print("=" * 70)
    print("  CK REPO READER -- full TIG story, awareness-tagged")
    print("=" * 70)
    print(f"  date: {datetime.utcnow().isoformat(timespec='seconds')}Z")
    print(f"  include_old: {args.include_old}")

    paths = find_files(PROJECT_ROOT, include_old=args.include_old)
    if args.limit:
        paths = paths[:args.limit]
    print(f"  files found: {len(paths)}")
    print(f"  output log: {_today_log()}")
    print(f"  dashboard:  {DASHBOARD}")
    print()

    state = {
        "total_files": len(paths),
        "n_read": 0, "n_failed": 0, "total_bytes": 0,
        "tick_first": 0, "tick_last": 0,
        "W_first": 0.0, "W_last": 0.0,
        "by_status": {},
        "current": None,
    }

    # Truncate today's log
    if _today_log().exists():
        _today_log().unlink()

    for i, p in enumerate(paths, 1):
        rel = p.relative_to(PROJECT_ROOT) if p.is_relative_to(PROJECT_ROOT) else p
        label = str(rel)
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            state["n_failed"] += 1
            with open(_today_log(), "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "i": i, "label": label, "ok": False,
                    "error": f"read: {type(e).__name__}: {e}",
                }) + "\n")
            continue

        # Detect status
        status = detect_status(p, text[:2000])
        state["by_status"][status] = state["by_status"].get(status, 0) + 1
        state["current"] = label

        # Tag the ingested text with provenance + status
        tagged = (f"[REPO READ] {label}\n"
                  f"[STATUS] {status}\n"
                  f"[CONTENT]\n"
                  f"{text[:args.max_chars]}")

        if i % args.every == 0 or i == 1 or i == len(paths):
            update_dashboard(state)
            print(f"[{i:>4}/{len(paths)}] [{status:<11}] {label[:60]}", flush=True)

        result = post_ingest(label, tagged)
        if not result["ok"]:
            state["n_failed"] += 1
            with open(_today_log(), "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "i": i, "label": label, "status": status, "ok": False,
                    "error": result.get("error"),
                }) + "\n")
            continue

        d = result["data"]
        state["n_read"] += 1
        state["total_bytes"] += d.get("n_chars", 0)
        post = d.get("post", {})
        pre = d.get("pre", {})
        if state["tick_first"] == 0:
            state["tick_first"] = pre.get("tick", 0)
            state["W_first"] = pre.get("W_trace", 0.0)
        state["tick_last"] = post.get("tick", state["tick_last"])
        state["W_last"] = post.get("W_trace", state["W_last"])

        rec = {
            "i": i, "label": label, "status": status, "ok": True,
            "n_chars": d.get("n_chars"),
            "tick_delta": d.get("tick_delta"),
            "W_trace_delta": d.get("W_trace_delta"),
        }
        with open(_today_log(), "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")

    state["current"] = None
    update_dashboard(state)
    print()
    print("=" * 70)
    print("  REPO READING SUMMARY")
    print("=" * 70)
    print(f"  files read:       {state['n_read']}/{state['total_files']}")
    print(f"  files failed:     {state['n_failed']}")
    print(f"  total bytes:      {state['total_bytes']:,}")
    print(f"  by status:        {state['by_status']}")
    print(f"  cortex tick:      {state['tick_first']:,} → {state['tick_last']:,}")
    print(f"  W_trace:          {state['W_first']:.4f} → {state['W_last']:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
