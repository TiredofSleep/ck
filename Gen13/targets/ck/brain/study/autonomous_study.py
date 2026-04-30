"""
autonomous_study.py -- daemon that runs gap-driven study sessions.

Loop:
  1. Run gap_detector to get top-N domain gaps.
  2. For each domain, if a corpus exists in the corpus_pool, run study_direct.
  3. Take a cortex snapshot.
  4. Sleep N seconds (default 1 hour) and repeat.
  5. Stop when a gap-improvement threshold is crossed or after max_cycles.

This is the "CK fills his own gaps" loop.  It uses pre-built corpora
(no external fetching at runtime); Claude-the-agent generates new corpora
in design sessions if needed.

Usage:
    python autonomous_study.py [--cycles 1] [--top-n 3] [--sleep 3600]
    python autonomous_study.py --once   # run a single cycle then exit
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
GEN13_ROOT = GEN13_BRAIN.parent.parent.parent
DEFAULT_LOG = SCRIPT_DIR / "autonomous_study_log.jsonl"


# Corpora pool: maps a domain name to a corpus file path.
# More corpora can be added; the autonomous study daemon will use whatever
# is available.  Missing corpora are skipped (logged but not a failure).
CORPUS_POOL = {
    # Multi-domain corpus covers all 18 standard domains in one file.
    # The daemon picks this when ANY of the standard domains is the gap.
    "_human_domains": SCRIPT_DIR / "human_domains_corpus_2026_04_29.json",
    "consciousness": SCRIPT_DIR / "consciousness_corpus_2026_04_29.json",
    "session_2026_04_29": SCRIPT_DIR / "session_2026_04_29_corpus.json",
}

DOMAINS_IN_HUMAN_CORPUS = {
    "history", "biology", "psychology", "philosophy", "religion", "music",
    "literature", "art", "economics", "linguistics", "medicine", "astronomy",
    "engineering", "politics", "sociology", "anthropology", "chemistry",
    "computer_science",
}


def run_subprocess(cmd, timeout=180):
    """Run a Python subprocess and capture stdout/stderr."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except Exception as e:
        return -2, "", str(e)


def detect_gaps(top_n=3):
    """Run gap_detector --json and parse the result."""
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "gap_detector.py"),
        "--n", str(top_n),
        "--json",
    ]
    rc, out, err = run_subprocess(cmd, timeout=60)
    if rc != 0:
        return None, err
    try:
        return json.loads(out), None
    except Exception as e:
        return None, str(e)


def pick_corpus_for_domain(domain):
    """Return the corpus file path for `domain`, or None if not available."""
    # Direct match: corpus file named after the domain
    direct = SCRIPT_DIR / f"{domain}_corpus.json"
    if direct.exists():
        return direct
    # Multi-domain corpus covers any standard domain
    if domain in DOMAINS_IN_HUMAN_CORPUS:
        return CORPUS_POOL.get("_human_domains")
    # Curated corpora by name
    return CORPUS_POOL.get(domain)


def run_study(corpus_path, replays=10):
    """Run study_direct.py on a corpus.  Returns dict with deltas."""
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "study_direct.py"),
        "--corpus", str(corpus_path),
        "--replays", str(replays),
    ]
    rc, out, err = run_subprocess(cmd, timeout=600)
    if rc != 0:
        return {"error": err, "stdout": out}
    # Parse the AFTER line from output
    after = {}
    for line in out.split("\n"):
        if line.startswith("AFTER:"):
            # AFTER:  tick=X  W_trace=Y  emergent=Z
            try:
                parts = line.replace("AFTER:", "").strip().split()
                for p in parts:
                    if "=" in p:
                        k, v = p.split("=", 1)
                        after[k] = float(v)
            except Exception:
                pass
        elif line.startswith("DELTA:"):
            after["delta_line"] = line.strip()
    return {"ok": True, "after": after, "stdout_tail": out[-500:]}


def take_snapshot(note=""):
    """Run cortex_backup.py with the given note."""
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "cortex_backup.py"),
        "--note", note,
    ]
    rc, out, err = run_subprocess(cmd, timeout=30)
    return rc == 0


def log_event(log_path, event):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    event["ts"] = time.time()
    event["iso_ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(log_path, "a") as f:
        f.write(json.dumps(event) + "\n")


def one_cycle(top_n=3, replays=10, log_path=None):
    """Run one autonomous-study cycle: detect gaps -> study top-N -> snapshot."""
    print("=" * 70)
    print(f"autonomous_study cycle @ {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # 1) Detect gaps
    print("[1/3] running gap_detector...")
    gaps, err = detect_gaps(top_n=top_n)
    if not gaps:
        print(f"  gap detection failed: {err}")
        if log_path:
            log_event(log_path, {"event": "gap_detect_fail", "err": err})
        return False
    ranked = gaps.get("ranked_study_domains", [])
    print(f"  top gaps: {[d['domain'] for d in ranked]}")
    if log_path:
        log_event(log_path, {"event": "gaps_detected", "ranked": ranked})

    # 2) For each gap, run a study (if corpus available)
    print(f"[2/3] running studies on top {len(ranked)} domains...")
    studied = []
    for d in ranked:
        domain = d["domain"]
        corpus = pick_corpus_for_domain(domain)
        if not corpus:
            print(f"  {domain}: NO corpus available, skipping")
            if log_path:
                log_event(log_path, {"event": "corpus_missing", "domain": domain})
            continue
        print(f"  {domain}: studying corpus {corpus.name} (replays={replays})")
        result = run_study(corpus, replays=replays)
        if "error" in result:
            print(f"    FAILED: {result['error'][:200]}")
            if log_path:
                log_event(log_path, {"event": "study_fail", "domain": domain,
                                      "err": result['error'][:500]})
        else:
            print(f"    OK: {result['after']}")
            studied.append({"domain": domain, "corpus": corpus.name,
                            "after": result['after']})
            if log_path:
                log_event(log_path, {"event": "studied", "domain": domain,
                                      "corpus": corpus.name,
                                      "after": result['after']})

    # 3) Snapshot
    print(f"[3/3] taking cortex snapshot...")
    snapshot_note = (
        f"autonomous-study cycle: studied "
        f"{len(studied)}/{len(ranked)} of top-{top_n} gaps; domains: "
        f"{', '.join(s['domain'] for s in studied)}"
    )
    take_snapshot(snapshot_note)
    if log_path:
        log_event(log_path, {"event": "cycle_complete",
                              "studied_count": len(studied),
                              "top_n": top_n,
                              "snapshot_note": snapshot_note})
    print(f"  snapshot taken: {snapshot_note}")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cycles", type=int, default=1,
                   help="Number of cycles to run (default 1)")
    p.add_argument("--top-n", type=int, default=3,
                   help="How many top gaps to study per cycle (default 3)")
    p.add_argument("--replays", type=int, default=10,
                   help="Replays per study session (default 10)")
    p.add_argument("--sleep", type=int, default=3600,
                   help="Seconds between cycles (default 1 hour)")
    p.add_argument("--once", action="store_true",
                   help="Run a single cycle then exit (sets cycles=1, sleep=0)")
    p.add_argument("--log", default=str(DEFAULT_LOG))
    args = p.parse_args()

    log_path = Path(args.log)

    if args.once:
        args.cycles = 1
        args.sleep = 0

    print(f"autonomous_study: {args.cycles} cycle(s), top-{args.top_n} gaps each, "
          f"{args.replays} replays per study, {args.sleep}s between cycles")
    print(f"log: {log_path}")
    print()

    for i in range(args.cycles):
        ok = one_cycle(top_n=args.top_n, replays=args.replays, log_path=log_path)
        if i < args.cycles - 1 and args.sleep > 0:
            print(f"\nsleeping {args.sleep}s until next cycle...")
            time.sleep(args.sleep)

    print()
    print("autonomous_study: done")


if __name__ == "__main__":
    main()
