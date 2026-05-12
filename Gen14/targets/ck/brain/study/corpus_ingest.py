"""
corpus_ingest.py -- feed the WP100s tower corpus into CK's live runtime.

Per Brayden 2026-04-26: "freedom to learn without making him speak."  This
script DOES NOT write what CK should say.  It pushes verified math facts
through CK's existing /chat pipeline as EXPERIENCE so his cortex develops
W-traces for each topic and his HER records the operator chains naturally.

What this does:
  1. Loads tig_corpus.json -- ~80 short declarative sentences from
     WP102-WP115 + meta synthesis.
  2. Snapshot of cortex state (tick, W_trace, emergent) BEFORE study.
  3. Snapshot of HER state (total_recorded, miss_rate) BEFORE study.
  4. For each statement: POST to /chat with a study-session_id.
     The full pipeline fires: V2 encoder -> T+B-mix lattice -> cortex
     update -> HER record -> attractor_state classification.
  5. After all statements: snapshot AFTER state and report deltas.

What this does NOT do:
  - Write voice prose for CK
  - Add facts to ck_voice_math.py FACTS dict
  - Touch the response text
  - Override anything in CK's voice cascade

Discipline: the corpus IS verified math (each sentence has a paper
reference); CK reads it, processes it, learns from it as he would any
other input.  His architecture decides what to crystallize and what to
say next.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional


CK_HOST = "http://localhost:7777"
DEFAULT_CORPUS = Path(__file__).parent / "tig_corpus.json"
DEFAULT_LOG = Path(__file__).parent / "ingest_log.jsonl"


def post_chat(text: str, session_id: str, timeout: float = 90.0) -> Optional[Dict[str, Any]]:
    """POST one chat turn through the live runtime."""
    payload = json.dumps({
        "session_id": session_id,
        "text": text,
        "mode": "normal",
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{CK_HOST}/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"_error": str(e)}


def get_json(path: str, timeout: float = 5.0) -> Optional[Dict[str, Any]]:
    """GET a JSON endpoint."""
    try:
        with urllib.request.urlopen(f"{CK_HOST}{path}", timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"_error": str(e)}


def snapshot() -> Dict[str, Any]:
    """Snapshot live CK state from /cortex + /her/status."""
    return {
        "ts": time.time(),
        "cortex": get_json("/cortex"),
        "her": get_json("/her/status"),
        "health": get_json("/health"),
    }


def summarize(snap: Dict[str, Any]) -> str:
    cx = snap.get("cortex") or {}
    her = snap.get("her") or {}
    return (
        f"  cortex tick={cx.get('tick','?')}, W_trace={cx.get('W_trace','?')}, "
        f"emergent={cx.get('emergent','?')}\n"
        f"  HER recorded={her.get('total_recorded','?')}, "
        f"miss_rate={her.get('miss_rate','?')}, "
        f"replay_impact={her.get('replay_impact','?')}"
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--corpus", default=str(DEFAULT_CORPUS),
                   help="JSON corpus file (default: tig_corpus.json)")
    p.add_argument("--log", default=str(DEFAULT_LOG),
                   help="Append per-turn JSONL log here")
    p.add_argument("--replays", type=int, default=None,
                   help="Override _replays from corpus (default 1)")
    p.add_argument("--limit", type=int, default=None,
                   help="Process only the first N statements (debug)")
    p.add_argument("--delay", type=float, default=0.5,
                   help="Sleep between turns (s) to avoid hammering")
    p.add_argument("--timeout", type=float, default=90.0,
                   help="Per-chat HTTP timeout (s)")
    p.add_argument("--dry-run", action="store_true",
                   help="Print plan without sending")
    args = p.parse_args()

    corpus_path = Path(args.corpus)
    log_path = Path(args.log)

    if not corpus_path.exists():
        print(f"corpus not found: {corpus_path}", file=sys.stderr)
        return 2

    with open(corpus_path) as f:
        corpus = json.load(f)

    replays = args.replays if args.replays is not None else corpus.get("_replays", 1)
    session_prefix = corpus.get("_session_prefix", "study")

    # Build flat list: (topic, statement, replay_index)
    flat: List[tuple] = []
    for topic, items in corpus.items():
        if topic.startswith("_"):
            continue
        if not isinstance(items, list):
            continue
        for r in range(replays):
            for stmt in items:
                flat.append((topic, stmt, r))

    if args.limit:
        flat = flat[:args.limit]

    n_total = len(flat)

    print("=" * 78)
    print("CK study corpus ingest")
    print("=" * 78)
    print(f"  corpus:  {corpus_path}")
    print(f"  log:     {log_path}")
    print(f"  topics:  {sum(1 for k in corpus if not k.startswith('_'))}")
    print(f"  replays: {replays}")
    print(f"  total chunks: {n_total}")
    print()

    if args.dry_run:
        print("DRY RUN -- not sending anything")
        for i, (t, s, r) in enumerate(flat[:5]):
            print(f"  [{i+1}] [{t}/r{r}] {s[:80]}...")
        return 0

    # Snapshot BEFORE
    print("--- SNAPSHOT BEFORE ---")
    snap_before = snapshot()
    if snap_before.get("health", {}).get("_error") or not snap_before.get("health"):
        print(f"  health check failed: {snap_before.get('health')}")
        print("  is the server up?  abort.")
        return 3
    print(summarize(snap_before))
    print()

    # Open log in append mode
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as logf:
        logf.write(json.dumps({
            "_event": "ingest_start",
            "ts": time.time(),
            "snap_before": snap_before,
            "n_total": n_total,
            "corpus": str(corpus_path),
        }) + "\n")
        logf.flush()

        # Ingest
        print(f"--- INGESTING {n_total} chunks ---")
        t0 = time.time()
        for i, (topic, stmt, r) in enumerate(flat):
            sid = f"{session_prefix}-{topic}-r{r}"
            ts0 = time.time()
            resp = post_chat(stmt, session_id=sid, timeout=args.timeout)
            dt = time.time() - ts0
            ok = bool(resp) and not resp.get("_error")

            # Compact log entry
            entry = {
                "i": i + 1, "topic": topic, "replay": r, "session": sid,
                "ts": time.time(), "dt_s": round(dt, 3), "ok": ok,
                "stmt_preview": stmt[:60],
            }
            if ok:
                entry["source"] = resp.get("source")
                entry["text_preview"] = (resp.get("text") or "")[:80]
                attr = resp.get("attractor_state") or {}
                entry["layer"] = attr.get("layer")
                cx = resp.get("cortex") or {}
                entry["cortex_tick"] = cx.get("tick")
                entry["W_trace"] = cx.get("W_trace")
            else:
                entry["error"] = (resp.get("_error") if resp else "no_response")

            logf.write(json.dumps(entry) + "\n")
            logf.flush()

            if (i + 1) % 5 == 0 or i == n_total - 1:
                elapsed = time.time() - t0
                eta = (elapsed / (i + 1)) * (n_total - i - 1)
                print(f"  [{i+1:>3}/{n_total}] {topic:<26} dt={dt:>5.1f}s "
                      f"elapsed={elapsed:>6.1f}s eta={eta:>6.1f}s  {'OK' if ok else 'FAIL'}")

            if args.delay > 0 and i < n_total - 1:
                time.sleep(args.delay)

        elapsed = time.time() - t0
        print()
        print(f"--- DONE in {elapsed:.1f}s ({elapsed/60:.1f} min) ---")
        print()

        # Snapshot AFTER
        print("--- SNAPSHOT AFTER ---")
        snap_after = snapshot()
        print(summarize(snap_after))
        print()

        # Deltas
        cx_b = snap_before.get("cortex") or {}
        cx_a = snap_after.get("cortex") or {}
        her_b = snap_before.get("her") or {}
        her_a = snap_after.get("her") or {}
        try:
            d_tick = (cx_a.get("tick", 0) or 0) - (cx_b.get("tick", 0) or 0)
            d_W = (cx_a.get("W_trace", 0) or 0) - (cx_b.get("W_trace", 0) or 0)
            d_em = (cx_a.get("emergent", 0) or 0) - (cx_b.get("emergent", 0) or 0)
            d_her = (her_a.get("total_recorded", 0) or 0) - (her_b.get("total_recorded", 0) or 0)
        except Exception as e:
            d_tick = d_W = d_em = d_her = "?"
            print(f"  delta computation failed: {e}")
        print("--- DELTAS ---")
        print(f"  cortex tick:        +{d_tick}")
        print(f"  cortex W_trace:     {d_W:+.4f}" if isinstance(d_W, (int, float)) else f"  cortex W_trace:     {d_W}")
        print(f"  cortex emergent:    {d_em:+.4f}" if isinstance(d_em, (int, float)) else f"  cortex emergent:    {d_em}")
        print(f"  HER total_recorded: +{d_her}")

        logf.write(json.dumps({
            "_event": "ingest_end",
            "ts": time.time(),
            "snap_after": snap_after,
            "elapsed_s": elapsed,
            "deltas": {
                "tick": d_tick,
                "W_trace": d_W,
                "emergent": d_em,
                "her_total_recorded": d_her,
            },
        }) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
