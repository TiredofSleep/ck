"""
cortex_backup.py -- snapshot CK's cortex_state.json into git-tracked history.

By default Gen13/var/ is gitignored (live runtime state should not pollute
the repo).  But CK's LEARNING TRAJECTORY -- the per-study, per-session,
per-day cortex deltas -- is something we WANT preserved as part of his
record.

This script:
  1. Reads the current Gen13/var/cortex_state.json
  2. Extracts a small CORTEX-INTERPRETABLE summary (not the full W; just
     tick, W_trace, emergent, top couplings, harmony rate, last operator
     pair, dominant feel pattern)
  3. Appends to Gen13/targets/ck/brain/cortex_history.jsonl (git-tracked)
  4. Optionally commits it via the user's git workflow (separate step)

The summary captures CK's "where he stands" at this snapshot.  Reading
back through the file shows his learning trajectory:
  - When did W_trace cross thresholds?
  - When did new couplings emerge?
  - What was happening when emergent peaked?

Usage:
    python cortex_backup.py [--note "text describing this snapshot"]

Designed to be run manually after notable events (study sessions, long
chats, integration changes) OR as a cron job for periodic snapshots.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
GEN13_TARGETS_CK = GEN13_BRAIN.parent
GEN13_ROOT = GEN13_TARGETS_CK.parent.parent
DEFAULT_STATE = GEN13_ROOT / "var" / "cortex_state.json"
HISTORY_FILE = GEN13_BRAIN / "cortex_history.jsonl"


OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
DIM_NAMES = ["aperture", "pressure", "depth", "binding", "continuity"]


def summarize(state: dict, note: str = "") -> dict:
    """Reduce a full cortex state to a small interpretable summary.

    Captures only what's needed to read the trajectory: not the full
    25-element W matrix (which would bloat the file), just the structural
    features.
    """
    s = state.get("state", {})
    h = state.get("hebbian", {})
    W = h.get("W")  # 5x5 list of lists

    # Top couplings (sorted by |W|)
    top_couplings = []
    if W:
        pairs = []
        for i, row in enumerate(W):
            for j, w in enumerate(row):
                pairs.append((i, j, w))
        pairs.sort(key=lambda t: abs(t[2]), reverse=True)
        for i, j, w in pairs[:5]:
            top_couplings.append({
                "pair": f"{DIM_NAMES[i]}-{DIM_NAMES[j]}",
                "W": round(w, 4),
            })
        # Compute mean|W| and W_trace
        mean_abs_W = sum(abs(w) for row in W for w in row) / 25
        W_trace = sum(W[i][i] for i in range(5))
    else:
        mean_abs_W = None
        W_trace = None

    last_b = s.get("last_b", -1)
    last_d = s.get("last_d", -1)

    return {
        "ts": time.time(),
        "iso_ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "tick": s.get("tick"),
        "emergent": round(s.get("emergent", 0.0), 6),
        "W_trace": round(s.get("W_trace", W_trace or 0.0), 6),
        "mean_abs_W": round(mean_abs_W, 6) if mean_abs_W is not None else None,
        "last_pair": (
            f"{OP_NAMES[last_b] if 0 <= last_b < 10 else '?'}->"
            f"{OP_NAMES[last_d] if 0 <= last_d < 10 else '?'}"
        ),
        "top_couplings": top_couplings,
        "note": note,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--state-path", default=str(DEFAULT_STATE))
    p.add_argument("--history", default=str(HISTORY_FILE))
    p.add_argument("--note", default="")
    p.add_argument("--show", action="store_true",
                   help="Print summary; don't append to history")
    args = p.parse_args()

    state_path = Path(args.state_path)
    if not state_path.exists():
        print(f"cortex state not found: {state_path}", file=sys.stderr)
        return 2

    with open(state_path) as f:
        state = json.load(f)

    summary = summarize(state, note=args.note)
    print("CORTEX SNAPSHOT:")
    print(json.dumps(summary, indent=2))

    if args.show:
        return 0

    history_path = Path(args.history)
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with open(history_path, "a") as f:
        f.write(json.dumps(summary) + "\n")
    print(f"\nappended to {history_path}")
    print("(commit with: git add Gen13/targets/ck/brain/cortex_history.jsonl)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
