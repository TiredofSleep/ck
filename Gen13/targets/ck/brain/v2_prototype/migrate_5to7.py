"""
migrate_5to7.py -- migrate live cortex_state.json (5x5) into a 7x7
                   prototype cortex.

Rule: top-left 5x5 of the new 7x7 W matrix = old 5x5 W.  Dims 5 and 6
(intent, echo) start at zero.  No learning is lost.

Output: a new file Gen13/var/cortex_state_7d_migrated.json that the
Cortex7D class can load.

The live 5x5 cortex_state.json is NOT touched.

Usage:
    python migrate_5to7.py [--input <5x5 path>] [--output <7x7 path>]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_ROOT = SCRIPT_DIR.parent.parent.parent.parent
DEFAULT_5D = GEN13_ROOT / "var" / "cortex_state.json"
DEFAULT_7D = GEN13_ROOT / "var" / "cortex_state_7d_migrated.json"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default=str(DEFAULT_5D))
    p.add_argument("--output", default=str(DEFAULT_7D))
    args = p.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    if not in_path.exists():
        print(f"input not found: {in_path}", file=sys.stderr)
        return 2

    with open(in_path) as f:
        state_5 = json.load(f)

    W_5 = state_5.get("hebbian", {}).get("W")
    if not W_5 or len(W_5) != 5:
        print(f"input doesn't have a 5x5 W matrix; skipping", file=sys.stderr)
        return 3

    # Build 7x7 W with top-left 5x5 = old W
    W_7 = [[0.0] * 7 for _ in range(7)]
    for i in range(5):
        for j in range(5):
            W_7[i][j] = W_5[i][j]

    # Other Hebbian fields
    state_7 = {
        "state": {
            "tick": state_5.get("state", {}).get("tick", 0),
            "last_b": state_5.get("state", {}).get("last_b", 7),
            "last_d": state_5.get("state", {}).get("last_d", 7),
            "last_harmony_frac": state_5.get("state", {}).get("last_harmony_frac", 0.0),
            "emergent": 0.0,  # recompute on first step
            "W_trace": sum(W_7[i][i] for i in range(7)),
        },
        "hebbian": {
            "W": W_7,
            "eta": state_5.get("hebbian", {}).get("eta", 0.005),
            "decay": state_5.get("hebbian", {}).get("decay", 0.02),
            "clamp": state_5.get("hebbian", {}).get("clamp", 1.0),
            "ticks": state_5.get("hebbian", {}).get("ticks", 0),
            "harmony_hits": state_5.get("hebbian", {}).get("harmony_hits", 0),
            "dim": 7,
        },
        "_migration": {
            "from_dim": 5,
            "to_dim": 7,
            "from_path": str(in_path),
            "preserved_W_top_left_5x5": True,
            "new_dims_zero_init": ["intent (5)", "echo (6)"],
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(state_7, f, indent=2)

    print(f"migrated 5x5 -> 7x7 cortex state:")
    print(f"  input:  {in_path}")
    print(f"  output: {out_path}")
    print(f"  W_trace (5x5): {sum(W_5[i][i] for i in range(5)):.4f}")
    print(f"  W_trace (7x7): {sum(W_7[i][i] for i in range(7)):.4f}")
    print(f"  ticks preserved: {state_7['state']['tick']}")
    print()
    print("the live cortex_state.json was NOT modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
