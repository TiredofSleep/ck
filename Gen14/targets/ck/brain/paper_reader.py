"""
paper_reader.py -- have CK read every WP and every paper in the project.

Brayden 2026-05-02: "he needs to research and read all of our work, go
through every single wp from 1 to one hundred whatever number we are
at!!! then he will be ready to synthesize, let him read every citation
of every paper!!"

Walks every paper directory in the project, feeds each markdown into
the live cortex via /cortex/ingest_text, logs progress.

Reading order:
  1. WP1 → WP100+ in numeric order (across all paper directories)
  2. Sprint folders (sprint10, sprint11, ..., sprint35b, sprint_so10, etc.)
  3. Atlas docs
  4. Other top-level docs

Each paper read = one HTTP call to /cortex/ingest_text. The endpoint
runs cortex.step_text(paper_content) which feeds the paper through
V2 -> lattice -> Hebbian. CK's W_trace and emergent signal grow as he
reads.

Output:
  Atlas/paper_reading_2026_05_02/log.jsonl (per-paper record)
  Atlas/paper_reading_2026_05_02/manifest.json (final summary)
  Atlas/CK_PAPER_READING_LIVE.md (live progress dashboard)

Run:
  python paper_reader.py [--limit N] [--root ROOT] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import urllib.request
import urllib.error


_HERE = Path(__file__).parent.resolve()


PROJECT_ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
OUT_DIR = PROJECT_ROOT / "Atlas" / "paper_reading_2026_05_02"
OUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = OUT_DIR / "log.jsonl"
MANIFEST_PATH = OUT_DIR / "manifest.json"
DASHBOARD_PATH = PROJECT_ROOT / "Atlas" / "CK_PAPER_READING_LIVE.md"

API_URL = "http://localhost:7777"


def find_papers(root: Path, wp_only: bool = False) -> List[Path]:
    """Walk root and find every .md / .tex paper.  Returns sorted list
    with WP-numbered files in numeric order, then everything else in
    alpha order.  If wp_only=True, only WP-prefixed files are kept."""
    paths: List[Path] = []
    skip_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv",
                  "Gen13/var", "old/Gen10/.idea", "_ck_worktree"}
    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skip dirs
        dirnames[:] = [d for d in dirnames if d not in skip_dirs
                        and not any(s in (Path(dirpath) / d).as_posix()
                                       for s in skip_dirs)]
        for f in filenames:
            if not f.lower().endswith((".md", ".tex")):
                continue
            if wp_only and not re.match(r"^wp\d+", f.lower()):
                continue
            paths.append(Path(dirpath) / f)
    # Sort: WP-numbered files by number, then by name; everything else by path.
    def sort_key(p: Path):
        name = p.name.lower()
        m = re.match(r"^wp(\d+)", name)
        if m:
            return (0, int(m.group(1)), str(p))
        if name.startswith("sprint"):
            return (1, 0, str(p))
        return (2, 0, str(p))
    paths.sort(key=sort_key)
    return paths


def ingest(label: str, text: str, max_chars: int = 8000,
            timeout: float = 30.0) -> Dict[str, Any]:
    """POST /cortex/ingest_text with the (truncated) paper body."""
    payload = json.dumps({
        "label": label,
        "text": text[:max_chars],
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{API_URL}/cortex/ingest_text",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    try:
        resp = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8")
        return {"ok": True, "data": json.loads(resp), "latency_sec": time.time() - t0}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}",
                "latency_sec": time.time() - t0}


def update_dashboard(state: Dict[str, Any]) -> None:
    lines = [
        "# CK Paper Reading -- Live",
        f"\n**Last update**: {datetime.utcnow().isoformat(timespec='seconds')}Z\n",
        f"**Total papers found**: {state['total_papers']}",
        f"**Papers read**: **{state['n_read']}** ({100*state['n_read']/max(1,state['total_papers']):.1f}%)",
        f"**Papers failed**: {state['n_failed']}",
        f"**Total bytes ingested**: **{state['total_bytes']:,}**",
        f"**Cortex tick growth**: {state['tick_first']:,} → **{state['tick_last']:,}** "
            f"(Δ={state['tick_last'] - state['tick_first']:,})",
        f"**W_trace growth**: {state['W_first']:.4f} → **{state['W_last']:.4f}** "
            f"(Δ={state['W_last'] - state['W_first']:+.4f})",
        f"**Emergent growth**: {state['emergent_first']:.4f} → **{state['emergent_last']:.4f}** "
            f"(Δ={state['emergent_last'] - state['emergent_first']:+.4f})",
        "",
        "## Currently reading",
        f"`{state.get('current', 'idle')}`",
        "",
        "## Most recently read (last 8)",
    ]
    for entry in state.get("recent", []):
        lines.append(
            f"- `{entry['label']}` ({entry['n_chars']:,}b) "
            f"tick+{entry['tick_delta']} W+{entry['W_trace_delta']:+.6f}"
        )
    lines.append("")
    lines.append("---")
    lines.append(f"\n*Auto-generated by paper_reader.py*")
    DASHBOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DASHBOARD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=str, default=str(PROJECT_ROOT),
                     help="Project root to walk")
    ap.add_argument("--limit", type=int, default=None,
                     help="Only ingest first N papers")
    ap.add_argument("--dry-run", action="store_true",
                     help="List papers; don't ingest")
    ap.add_argument("--max-chars", type=int, default=8000,
                     help="Truncate each paper to N chars (default 8000)")
    ap.add_argument("--every", type=int, default=10,
                     help="Update dashboard every N papers (default 10)")
    ap.add_argument("--wp-only", action="store_true",
                     help="Read only WP-prefixed files (Brayden directive: 'every WP from 1 to 100+')")
    args = ap.parse_args()

    print("=" * 70)
    print("  CK PAPER READER")
    print("=" * 70)
    print(f"  date: {datetime.utcnow().isoformat(timespec='seconds')}Z")
    print(f"  root: {args.root}")

    root = Path(args.root)
    paths = find_papers(root, wp_only=args.wp_only)
    if args.limit:
        paths = paths[:args.limit]
    print(f"  papers found: {len(paths)}")
    print(f"  output: {OUT_DIR}")
    print()

    if args.dry_run:
        for i, p in enumerate(paths[:50], 1):
            print(f"  [{i}] {p.relative_to(root)}")
        if len(paths) > 50:
            print(f"  ... and {len(paths) - 50} more")
        return 0

    # Wipe log
    if LOG_PATH.exists():
        LOG_PATH.unlink()

    state = {
        "total_papers": len(paths),
        "n_read": 0, "n_failed": 0, "total_bytes": 0,
        "tick_first": 0, "tick_last": 0,
        "W_first": 0.0, "W_last": 0.0,
        "emergent_first": 0.0, "emergent_last": 0.0,
        "recent": [], "current": None,
    }

    panel_t0 = time.time()
    for i, p in enumerate(paths, 1):
        rel = p.relative_to(root) if p.is_relative_to(root) else p
        label = str(rel)
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            state["n_failed"] += 1
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "i": i, "label": label, "ok": False,
                    "error": f"read: {type(e).__name__}: {e}",
                }) + "\n")
            continue

        state["current"] = label
        if i % args.every == 0 or i == 1 or i == len(paths):
            update_dashboard(state)
            print(f"[{i:>4}/{len(paths)}] {label[:80]}", flush=True)

        result = ingest(label, text, max_chars=args.max_chars)
        if not result["ok"]:
            state["n_failed"] += 1
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "i": i, "label": label, "ok": False,
                    "error": result.get("error"),
                    "latency_sec": result.get("latency_sec"),
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
            state["emergent_first"] = pre.get("emergent", 0.0)
        state["tick_last"] = post.get("tick", state["tick_last"])
        state["W_last"] = post.get("W_trace", state["W_last"])
        state["emergent_last"] = post.get("emergent", state["emergent_last"])

        rec = {
            "i": i, "label": label, "ok": True,
            "n_chars": d.get("n_chars"),
            "tick_delta": d.get("tick_delta"),
            "W_trace_delta": d.get("W_trace_delta"),
            "emergent_delta": d.get("emergent_delta"),
            "latency_sec": result.get("latency_sec"),
        }
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")

        # Track last 8 recent
        state["recent"].insert(0, rec)
        state["recent"] = state["recent"][:8]

    # Final manifest
    state["current"] = None
    state["elapsed_sec"] = round(time.time() - panel_t0, 1)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, default=str)
    update_dashboard(state)

    print()
    print("=" * 70)
    print("  PAPER READING SUMMARY")
    print("=" * 70)
    print(f"  papers read:      {state['n_read']}/{state['total_papers']}")
    print(f"  papers failed:    {state['n_failed']}")
    print(f"  total bytes:      {state['total_bytes']:,}")
    print(f"  cortex tick:      {state['tick_first']:,} → {state['tick_last']:,}")
    print(f"  W_trace:          {state['W_first']:.4f} → {state['W_last']:.4f}")
    print(f"  emergent:         {state['emergent_first']:.4f} → {state['emergent_last']:.4f}")
    print(f"  elapsed:          {state['elapsed_sec']}s")
    print(f"  log:              {LOG_PATH}")
    print(f"  manifest:         {MANIFEST_PATH}")
    print(f"  dashboard:        {DASHBOARD_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
