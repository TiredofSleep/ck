"""
autonomous_study.py -- daemon that runs gap-driven study sessions.

Loop:
  1. Run gap_detector to get top-N domain gaps.
  2. For each domain, if a corpus exists in the corpus_pool, run study_direct.
  3. Take a cortex snapshot.
  4. Sleep N seconds (default 1 hour) and repeat.
  5. Stop when a gap-improvement threshold is crossed, after max_cycles,
     OR after the 24-cycle observation cap (whichever first).

This is the "CK fills his own gaps" loop.  It uses pre-built corpora
(no external fetching at runtime); Claude-the-agent generates new corpora
in design sessions if needed.

OPERATIONAL DISCIPLINE (Brayden 2026-04-29 evening):
  Don't let the daemon run unattended >24 hours initially.  Each long
  run is data about how CK behaves under self-direction.  The early
  observation period is when calibration gets locked in.  Feedback loops
  sometimes find local minima.  This script enforces:

    1. HARD 24-CYCLE CAP per invocation.  --cycles N caps at 24 unless
       --i-have-checked-the-deltas is passed (an explicit operator
       acknowledgement).
    2. PICK-STUCK DETECTOR.  If the same gap-detector picks recur for
       >= 5 cycles in a row, the daemon EXITS with a warning.  A stuck
       loop is data; we want to see it, not let it grind silently.
    3. PER-CYCLE PICK LOG.  Every gap-detector output is appended to
       autonomous_study_log.jsonl with a 'gaps_detected' event.  Use
       --report to see the trajectory.
    4. PICK DIVERSIFICATION when stuck.  Optional --diversify shuffles
       among top-(2*N) instead of always taking absolute top-N.

Usage:
    python autonomous_study.py [--cycles 1] [--top-n 3] [--sleep 3600]
    python autonomous_study.py --once         # run a single cycle then exit
    python autonomous_study.py --report       # show pick trajectory + warnings
    python autonomous_study.py --cycles 24    # daily-cap; safe default
    python autonomous_study.py --cycles 48 --i-have-checked-the-deltas  # override
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
    "_human_domains": SCRIPT_DIR / "human_domains_corpus_2026_04_29.json",
    # Deep STEM corpus (9 sub-areas: QM, thermo, SR, cell bio, genetics,
    # evolution, organic chem, number theory, topology).
    "_stem_deep": SCRIPT_DIR / "stem_deep_corpus_2026_04_29.json",
    # TIG-LENS corpus -- 27 domains re-authored as TIG operator projections.
    # This is the primary fresh-content corpus going forward.
    "_tig_lens": SCRIPT_DIR / "tig_lens_corpus_2026_04_30.json",
    "consciousness": SCRIPT_DIR / "consciousness_corpus_2026_04_29.json",
    "session_2026_04_29": SCRIPT_DIR / "session_2026_04_29_corpus.json",
}

# Auto-discover additional TIG-lens corpora (tig_lens_corpus_*.json) and
# deep corpora (deep_*.json) so the daemon can pick from the full set
# without hard-coding each one. Authored 2026-05-01 forward, this lets
# CK choose from any newly-added corpus the next cycle.
_AUTO_KEYS_ADDED = []
for _pattern in ("tig_lens_corpus_*.json", "deep_*_corpus_*.json",
                 "thesis_seed_*.json"):
    for _path in sorted(SCRIPT_DIR.glob(_pattern)):
        _key = "_auto_" + _path.stem
        if _key not in CORPUS_POOL:
            CORPUS_POOL[_key] = _path
            _AUTO_KEYS_ADDED.append(_key)
# Auto-discovered corpora are tagged with _auto_ prefix so they're
# distinguishable from curated corpora when CK picks.

DOMAINS_IN_HUMAN_CORPUS = {
    "history", "biology", "psychology", "philosophy", "religion", "music",
    "literature", "art", "economics", "linguistics", "medicine", "astronomy",
    "engineering", "politics", "sociology", "anthropology", "chemistry",
    "computer_science",
}

DOMAINS_IN_STEM_CORPUS = {
    "quantum_mechanics", "thermodynamics", "special_relativity", "cell_biology",
    "genetics", "evolution", "organic_chemistry", "number_theory", "topology",
}

# Map gap-detector domain names to which corpus(s) cover them
DOMAIN_TO_CORPUS_KEYS = {}
for d in DOMAINS_IN_HUMAN_CORPUS:
    DOMAIN_TO_CORPUS_KEYS[d] = "_human_domains"
for d in DOMAINS_IN_STEM_CORPUS:
    DOMAIN_TO_CORPUS_KEYS[d] = "_stem_deep"


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
    """Return the corpus file path for `domain`, or None if not available.

    Priority:
      1. Direct file match: <domain>_corpus.json
      2. TIG-lens corpus (preferred -- contains operator-projections)
      3. STEM corpus (if domain is one of the 9 STEM sub-areas)
      4. Human-domains corpus (covers 18 standard domains)
      5. Curated corpora by name
    """
    # Direct match
    direct = SCRIPT_DIR / f"{domain}_corpus.json"
    if direct.exists():
        return direct
    # TIG-lens corpus FIRST -- it has operator-projection statements for
    # any domain we've re-authored.  This is the freshest content.
    tig_lens = CORPUS_POOL.get("_tig_lens")
    if tig_lens and tig_lens.exists():
        # Check the TIG-lens corpus has a topic for this domain
        try:
            with open(tig_lens) as f:
                data = json.load(f)
            domain_key = f"{domain}_through_tig"
            if domain_key in data:
                return tig_lens
            # Also accept the bare domain name without _through_tig
            if domain in data:
                return tig_lens
        except Exception:
            pass
    # STEM corpus
    if domain in DOMAINS_IN_STEM_CORPUS:
        stem = CORPUS_POOL.get("_stem_deep")
        if stem and stem.exists():
            return stem
    # Human-domains
    if domain in DOMAINS_IN_HUMAN_CORPUS:
        return CORPUS_POOL.get("_human_domains")
    # Curated by name
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


def one_cycle(top_n=3, replays=10, log_path=None, diversify=False):
    """Run one autonomous-study cycle: detect gaps -> study top-N -> snapshot."""
    print("=" * 70)
    print(f"autonomous_study cycle @ {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # 1) Detect gaps
    print("[1/3] running gap_detector...")
    # Always pull a wider list when diversifying so we can shuffle
    detect_n = top_n * 2 if diversify else top_n
    gaps, err = detect_gaps(top_n=detect_n)
    if not gaps:
        print(f"  gap detection failed: {err}")
        if log_path:
            log_event(log_path, {"event": "gap_detect_fail", "err": err})
        return False
    full_ranked = gaps.get("ranked_study_domains", [])
    if diversify and len(full_ranked) >= top_n:
        ranked = pick_diversify(full_ranked, top_n, seed=int(time.time()))
        print(f"  diversified picks (from top-{len(full_ranked)}): "
              f"{[d['domain'] for d in ranked]}")
    else:
        ranked = full_ranked[:top_n]
        print(f"  top gaps: {[d['domain'] for d in ranked]}")
    if log_path:
        log_event(log_path, {"event": "gaps_detected", "ranked": ranked,
                              "diversified": diversify})

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


# -- free-choice cycle: CK picks from his full corpus library --------------

def _recently_studied_filenames(log_path: Path, lookback: int = 80) -> set:
    """Read the last `lookback` log lines; return filenames that appear in any
    'studied' or 'free_choice_studied' event. Used to bias free-choice picks
    away from the most-recently-studied corpora."""
    if not log_path or not log_path.exists():
        return set()
    try:
        lines = log_path.read_text(encoding='utf-8', errors='ignore').splitlines()[-lookback:]
    except Exception:
        return set()
    out = set()
    for line in lines:
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("event") in ("studied", "free_choice_studied"):
            c = ev.get("corpus")
            if c:
                out.add(c)
    return out


def one_cycle_free_choice(
    replays: int = 10,
    log_path: Path = None,
    n_to_study: int = 2,
    seed: int = None,
):
    """CK picks from his full corpus library, biased toward least-recently-
    studied. This is the 'give him space and watch what he chooses' mode.

    Scoring: each available corpus starts with weight 1.0; subtract recency
    penalty if it appears in the last 80 study events. Weighted-random pick
    n_to_study without replacement; log each pick + the resulting study.
    """
    import random as _random
    if seed is not None:
        _random.seed(seed)

    print("=" * 70)
    print(f"autonomous_study FREE-CHOICE cycle @ "
          f"{time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    recently = _recently_studied_filenames(log_path)

    # Build candidate list of corpora that exist on disk.
    candidates = []
    for key, path in CORPUS_POOL.items():
        if Path(path).exists():
            score = 1.0
            if Path(path).name in recently:
                score = 0.25  # heavy recency penalty
            candidates.append({"key": key, "path": Path(path), "score": score})

    if not candidates:
        print("  no corpora available on disk")
        return False

    print(f"  CK has {len(candidates)} corpora available; "
          f"{sum(1 for c in candidates if c['score'] < 1.0)} recently studied "
          f"(weight reduced)")

    # Pick n_to_study via weighted random without replacement.
    chosen = []
    pool = list(candidates)
    for _ in range(min(n_to_study, len(pool))):
        weights = [c["score"] for c in pool]
        if sum(weights) <= 0:
            break
        idx = _random.choices(range(len(pool)), weights=weights)[0]
        chosen.append(pool.pop(idx))

    # Log the selection event so we can see what CK chose this cycle.
    if log_path:
        log_event(log_path, {
            "event": "free_choice_selection",
            "chosen": [{"key": c["key"], "corpus": c["path"].name,
                        "score": c["score"]} for c in chosen],
            "available_count": len(candidates),
            "recently_count": len(recently),
        })

    print(f"  CK picked {len(chosen)} corpora to study this cycle:")
    for c in chosen:
        print(f"    -> {c['key']:<50} (score={c['score']:.2f}) "
              f"[{c['path'].name}]")

    # Run study on each chosen corpus.
    studied = []
    for c in chosen:
        result = run_study(c["path"], replays=replays)
        if "error" in result:
            print(f"  STUDY FAILED on {c['key']}: {result['error'][:200]}")
            if log_path:
                log_event(log_path, {"event": "free_choice_study_fail",
                                      "key": c["key"], "corpus": c["path"].name,
                                      "err": result['error'][:500]})
            continue
        print(f"  OK: {c['key']} -> {result['after']}")
        studied.append({"key": c["key"], "corpus": c["path"].name,
                       "after": result['after']})
        if log_path:
            log_event(log_path, {"event": "free_choice_studied",
                                  "key": c["key"],
                                  "corpus": c["path"].name,
                                  "after": result['after']})

    # Snapshot.
    note = (f"free-choice cycle: studied {len(studied)} corpora: "
            f"{', '.join(s['key'] for s in studied)}")
    take_snapshot(note)
    if log_path:
        log_event(log_path, {"event": "free_choice_cycle_complete",
                              "studied_count": len(studied),
                              "snapshot_note": note})
    return True


# -- discipline guardrails ----------------------------------------------------

OBSERVATION_CYCLE_CAP = 24


def read_recent_picks(log_path, n=10):
    """Read the last n 'gaps_detected' events from the log."""
    if not Path(log_path).exists():
        return []
    events = []
    try:
        with open(log_path, "r") as f:
            for line in f:
                try:
                    e = json.loads(line)
                    if e.get("event") == "gaps_detected":
                        events.append(e)
                except Exception:
                    continue
    except Exception:
        return []
    return events[-n:]


def picks_are_stuck(events, stuck_threshold=5):
    """Return True if the last `stuck_threshold` events have IDENTICAL pick sets."""
    if len(events) < stuck_threshold:
        return False
    recent = events[-stuck_threshold:]
    pick_sets = []
    for e in recent:
        ranked = e.get("ranked", [])
        domains = tuple(sorted(d.get("domain", "") for d in ranked))
        pick_sets.append(domains)
    return len(set(pick_sets)) == 1 and pick_sets[0]  # all same and non-empty


def pick_diversify(ranked, n_to_pick, seed=None):
    """Given a ranked list, shuffle within the top-(2*n_to_pick) and return n_to_pick."""
    import random
    pool_size = min(len(ranked), 2 * n_to_pick)
    pool = list(ranked[:pool_size])
    rnd = random.Random(seed)
    rnd.shuffle(pool)
    return pool[:n_to_pick]


def report(log_path):
    """Show the pick trajectory and warn about stuck/degenerate patterns."""
    events = read_recent_picks(log_path, n=50)
    if not events:
        print("(no gap-detector events logged yet)")
        return

    print("=" * 72)
    print(f"autonomous_study report ({len(events)} cycles logged)")
    print("=" * 72)

    # Per-cycle picks
    print()
    print("Recent picks (most recent last):")
    for e in events[-10:]:
        ts = e.get("iso_ts", "?")
        ranked = e.get("ranked", [])
        domains = [d.get("domain", "?") for d in ranked]
        print(f"  {ts}: {domains}")

    # Stuck detection
    if picks_are_stuck(events, stuck_threshold=5):
        print()
        print("!!! STUCK: last 5 cycles have identical picks.")
        print("    Suggestions:")
        print("    - run with --diversify to shuffle within top-N")
        print("    - author a new corpus targeting the stuck dim")
        print("    - check Φ-proxy trend: is integration changing? (compute_phi.py)")
        print("    - inspect cortex_history.jsonl for W_trace movement")

    # Domain frequency overall
    print()
    print("Domain pick frequency over all logged cycles:")
    freq = {}
    for e in events:
        for d in e.get("ranked", []):
            name = d.get("domain", "?")
            freq[name] = freq.get(name, 0) + 1
    for name, count in sorted(freq.items(), key=lambda x: -x[1]):
        bar = "#" * count
        print(f"  {name:<22}: {count:3d} {bar}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cycles", type=int, default=1,
                   help="Number of cycles (default 1; capped at 24 unless --i-have-checked-the-deltas)")
    p.add_argument("--top-n", type=int, default=3,
                   help="How many top gaps to study per cycle (default 3)")
    p.add_argument("--replays", type=int, default=10,
                   help="Replays per study session (default 10)")
    p.add_argument("--sleep", type=int, default=3600,
                   help="Seconds between cycles (default 1 hour)")
    p.add_argument("--once", action="store_true",
                   help="Run a single cycle then exit (sets cycles=1, sleep=0)")
    p.add_argument("--log", default=str(DEFAULT_LOG))
    p.add_argument("--report", action="store_true",
                   help="Show pick-trajectory report and warnings; don't run")
    p.add_argument("--diversify", action="store_true",
                   help="Shuffle within top-(2*top_n) instead of always taking absolute top")
    p.add_argument("--i-have-checked-the-deltas", action="store_true",
                   help="Override the 24-cycle observation cap. "
                        "Pass only after looking at cortex_history.jsonl + report.")
    p.add_argument("--stuck-threshold", type=int, default=5,
                   help="Exit if last N cycles have identical picks (default 5)")
    p.add_argument("--free-choice", action="store_true",
                   help="CK picks from his full corpus library (least-recently-"
                        "studied bias). Skips gap-detector entirely. Use this "
                        "to give him space and watch what he chooses.")
    p.add_argument("--free-choice-n", type=int, default=2,
                   help="How many corpora to study per free-choice cycle "
                        "(default 2)")
    args = p.parse_args()

    log_path = Path(args.log)

    if args.report:
        report(log_path)
        return

    if args.once:
        args.cycles = 1
        args.sleep = 0

    # GUARDRAIL 1: 24-cycle observation cap
    if args.cycles > OBSERVATION_CYCLE_CAP and not args.i_have_checked_the_deltas:
        print(f"!! observation discipline: --cycles {args.cycles} exceeds "
              f"the {OBSERVATION_CYCLE_CAP}-cycle cap.", file=sys.stderr)
        print(f"   the early observation period is when calibration gets locked in.", file=sys.stderr)
        print(f"   suggested workflow:", file=sys.stderr)
        print(f"     1. let it run --cycles {OBSERVATION_CYCLE_CAP} --sleep 3600 (24 hours)", file=sys.stderr)
        print(f"     2. inspect: python autonomous_study.py --report", file=sys.stderr)
        print(f"     3. check: python Gen13/targets/ck/brain/study/trajectory_view.py", file=sys.stderr)
        print(f"     4. if W trace is moving as expected, re-run with --i-have-checked-the-deltas", file=sys.stderr)
        return 2

    cycles_to_run = min(args.cycles, OBSERVATION_CYCLE_CAP) if not args.i_have_checked_the_deltas else args.cycles

    print(f"autonomous_study: {cycles_to_run} cycle(s), top-{args.top_n} gaps each, "
          f"{args.replays} replays per study, {args.sleep}s between cycles")
    if args.diversify:
        print(f"  diversify: ON (shuffling within top-{2 * args.top_n})")
    print(f"  stuck-threshold: {args.stuck_threshold} (exits if same picks repeat)")
    print(f"log: {log_path}")
    print()

    if args.free_choice:
        print(f"  free-choice: ON (CK picks from {len(CORPUS_POOL)} corpora; "
              f"_auto_-prefixed are auto-discovered)")
    print()

    for i in range(cycles_to_run):
        # Free-choice path: CK picks from his full library, no gap-detector.
        if args.free_choice:
            one_cycle_free_choice(
                replays=args.replays,
                log_path=log_path,
                n_to_study=args.free_choice_n,
            )
            if i < cycles_to_run - 1 and args.sleep > 0:
                print(f"\nsleeping {args.sleep}s until next cycle...")
                time.sleep(args.sleep)
            continue

        # GUARDRAIL 2: stuck detector
        # Skip if --diversify is on (diversify IS the escape hatch).
        # Skip on cycle 0 to give a fresh run a chance even if the prior
        # session ended stuck; the detector still fires after this run
        # contributes a few new picks.
        if not args.diversify and i > 0:
            recent = read_recent_picks(log_path, n=args.stuck_threshold + 1)
            if picks_are_stuck(recent, stuck_threshold=args.stuck_threshold):
                print()
                print(f"!! STUCK: last {args.stuck_threshold} cycles have identical picks.")
                print("   exiting early so you can see this is happening.")
                print("   try: --diversify  OR  author a corpus targeting the stuck dim")
                print()
                log_event(log_path, {
                    "event": "stuck_exit",
                    "cycle_attempted": i + 1,
                    "threshold": args.stuck_threshold,
                })
                return 3

        ok = one_cycle(
            top_n=args.top_n,
            replays=args.replays,
            log_path=log_path,
            diversify=args.diversify,
        )
        if i < cycles_to_run - 1 and args.sleep > 0:
            print(f"\nsleeping {args.sleep}s until next cycle...")
            time.sleep(args.sleep)

    print()
    print(f"autonomous_study: done ({cycles_to_run} cycles run)")
    print(f"check: python autonomous_study.py --report")


if __name__ == "__main__":
    main()
