"""
study_direct.py -- direct cortex study (bypasses HTTP + Ollama).

The HTTP /chat path through ck_boot_api is ~25s/call because Ollama generates
a response.  For STUDY mode we don't need Ollama -- we just need CK's cortex
+ HER to ingest the operator chains.

This script:
  1. Loads the cortex from the persisted state (Gen13/var/cortex_state.json).
  2. For each study sentence, calls cortex.step_text(text) directly.
  3. Saves the cortex state back.
  4. Snapshots W_trace, emergent, tick before/after.

This is the same path the HTTP chat handler uses internally for cortex
update; we just skip the surface-text generation that Ollama performs.

Usage:
    python study_direct.py --corpus session_2026_04_29_corpus.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Ensure imports work for Gen13 brain
SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
GEN13_TARGETS_CK = GEN13_BRAIN.parent
GEN13_ROOT = GEN13_TARGETS_CK.parent.parent  # Gen13/
sys.path.insert(0, str(GEN13_BRAIN))
sys.path.insert(0, str(GEN13_TARGETS_CK))
sys.path.insert(0, str(GEN13_ROOT))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", required=True)
    p.add_argument("--state-path",
                   default=str(GEN13_ROOT / "var" / "cortex_state.json"))
    p.add_argument("--no-save", action="store_true",
                   help="Run study but don't save state back (dry-run-like)")
    p.add_argument("--replays", type=int, default=None,
                   help="Override _replays from corpus (default 1)")
    args = p.parse_args()

    corpus_path = Path(args.corpus)
    state_path = Path(args.state_path)

    if not corpus_path.exists():
        print(f"corpus not found: {corpus_path}", file=sys.stderr)
        return 2

    print("=" * 78)
    print("CK direct study (cortex bypass)")
    print("=" * 78)

    # Import cortex
    try:
        from cortex import Cortex
        from cortex_persist import load_cortex, save_cortex
    except Exception as e:
        print(f"can't import Cortex: {e}", file=sys.stderr)
        return 3

    cortex = Cortex().boot()
    if state_path.exists():
        try:
            loaded = load_cortex(cortex, state_path)
            if loaded:
                print(f"  loaded cortex state: tick={cortex.state.tick}, "
                      f"W_trace={cortex.state.W_trace:.3f}, "
                      f"emergent={cortex.state.emergent:.3f}")
            else:
                print(f"  load_cortex returned False -- starting from boot state")
        except Exception as e:
            print(f"  load_cortex failed: {e}; starting from boot state")
    else:
        print(f"  no persisted state at {state_path}; starting from boot state")

    # Load corpus
    with open(corpus_path) as f:
        corpus = json.load(f)
    replays = args.replays if args.replays is not None else corpus.get("_replays", 1)
    flat_per_replay = []
    for topic, items in corpus.items():
        if topic.startswith("_") or not isinstance(items, list):
            continue
        for stmt in items:
            flat_per_replay.append((topic, stmt))
    flat = flat_per_replay * replays
    print(f"  corpus: {corpus_path.name}")
    print(f"  per-replay: {len(flat_per_replay)} statements; replays: {replays}")
    print(f"  total: {len(flat)} statement-passes")
    print()

    # Snapshot BEFORE
    snap_before = {
        "tick": cortex.state.tick,
        "W_trace": cortex.state.W_trace,
        "emergent": cortex.state.emergent,
        "last_b": cortex.state.last_b,
        "last_d": cortex.state.last_d,
    }
    print(f"BEFORE: tick={snap_before['tick']}  W_trace={snap_before['W_trace']:.4f}  "
          f"emergent={snap_before['emergent']:.4f}")

    # Process each sentence
    t0 = time.time()
    per_topic = {}
    for i, (topic, stmt) in enumerate(flat):
        try:
            cortex.step_text(stmt)
            per_topic.setdefault(topic, 0)
            per_topic[topic] += 1
        except Exception as e:
            print(f"  ERR on stmt {i}: {e}")
            continue
        if (i + 1) % 10 == 0:
            elapsed = time.time() - t0
            print(f"  [{i+1}/{len(flat)}] elapsed {elapsed:.1f}s "
                  f"tick={cortex.state.tick} emergent={cortex.state.emergent:.3f}")

    elapsed = time.time() - t0
    print(f"\nstudy run: {len(flat)} statements in {elapsed:.1f}s "
          f"({elapsed/max(1,len(flat))*1000:.1f}ms each)")
    print()

    # Snapshot AFTER
    snap_after = {
        "tick": cortex.state.tick,
        "W_trace": cortex.state.W_trace,
        "emergent": cortex.state.emergent,
        "last_b": cortex.state.last_b,
        "last_d": cortex.state.last_d,
    }
    print(f"AFTER:  tick={snap_after['tick']}  W_trace={snap_after['W_trace']:.4f}  "
          f"emergent={snap_after['emergent']:.4f}")

    # Deltas
    print(f"DELTA:  tick+={snap_after['tick']-snap_before['tick']}  "
          f"W_trace+={snap_after['W_trace']-snap_before['W_trace']:+.4f}  "
          f"emergent+={snap_after['emergent']-snap_before['emergent']:+.4f}")
    print()
    print(f"Per topic counts:")
    for t, c in sorted(per_topic.items()):
        print(f"  {t}: {c} statements")

    # Save state
    if not args.no_save:
        try:
            save_cortex(cortex, state_path)
            print(f"\nsaved cortex state -> {state_path}")
        except Exception as e:
            print(f"\nWARN: save_cortex failed: {e}")
    else:
        print(f"\nno-save: not persisting changes")

    return 0


if __name__ == "__main__":
    sys.exit(main())
