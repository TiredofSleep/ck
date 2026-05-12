"""
migrate_cortex_5to7_live.py -- migrate live cortex_state.json (5-dim,
ck_gen13_cortex_state magic format) into a 7-dim file in the SAME magic
format that cortex_persist.load_cortex can read directly.

Embeds the live 5x5 W in the top-left of a new 7x7 W. Dims 5 and 6
(intent, echo) start at zero. Tick counter, ticks, harmony_hits all
preserved. _prev_profile expanded from length 5 -> length 7 by appending
[profile_5d[2], profile_5d[0]] (intent seeded from depth, echo from
aperture; matches cortex_v2._profile_7d_from_5d).

Output: Gen13/var/cortex_state_7d.json (the file ck_boot_api.py reads
when CK_CORTEX_DIM=7).

The live cortex_state.json is NOT touched.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_ROOT = SCRIPT_DIR.parent.parent.parent
DEFAULT_5D = GEN13_ROOT / "var" / "cortex_state.json"
DEFAULT_7D = GEN13_ROOT / "var" / "cortex_state_7d.json"

CORTEX_STATE_VERSION = 1
CORTEX_STATE_MAGIC = "ck_gen13_cortex_state"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default=str(DEFAULT_5D))
    p.add_argument("--output", default=str(DEFAULT_7D))
    p.add_argument("--force", action="store_true",
                   help="overwrite output if it exists")
    args = p.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    if not in_path.exists():
        print(f"input not found: {in_path}", file=sys.stderr)
        return 2
    if out_path.exists() and not args.force:
        print(f"output already exists: {out_path}", file=sys.stderr)
        print(f"use --force to overwrite", file=sys.stderr)
        return 3

    with open(in_path) as f:
        state_5 = json.load(f)

    if state_5.get("magic") != CORTEX_STATE_MAGIC:
        print(f"input is not a {CORTEX_STATE_MAGIC} file", file=sys.stderr)
        print(f"  got magic={state_5.get('magic')!r}", file=sys.stderr)
        return 4

    h5 = state_5.get("hebbian", {})
    W_5 = h5.get("W")
    if not isinstance(W_5, list) or len(W_5) != 5:
        print(f"input doesn't have a 5x5 W matrix", file=sys.stderr)
        return 5

    # Build 7x7 with top-left 5x5 = old W
    W_7 = [[0.0] * 7 for _ in range(7)]
    for i in range(5):
        for j in range(5):
            W_7[i][j] = float(W_5[i][j])

    # Cortex section
    c5 = state_5.get("cortex", {})
    prev_profile_5 = c5.get("prev_profile")
    if isinstance(prev_profile_5, list) and len(prev_profile_5) == 5:
        # Expand to 7-dim: dims 5,6 seeded from dims 2,0 (matches
        # cortex_v2._profile_7d_from_5d).
        prev_profile_7 = list(prev_profile_5) + [
            int(prev_profile_5[2]), int(prev_profile_5[0])
        ]
    else:
        prev_profile_7 = None

    # Use the same magic + version as the live file format.
    state_7 = {
        "magic": CORTEX_STATE_MAGIC,
        "version": CORTEX_STATE_VERSION,
        "saved_at": time.time(),
        "saved_at_iso": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
        "hebbian": {
            "W": W_7,
            "ticks": int(h5.get("ticks", 0)),
            "harmony_hits": int(h5.get("harmony_hits", 0)),
            "eta": float(h5.get("eta", 0.005)),
            "decay": float(h5.get("decay", 0.02)),
            "clamp": float(h5.get("clamp", 1.0)),
        },
        "cortex": {
            "tick": int(c5.get("tick", 0)),
            "last_b": int(c5.get("last_b", 7)),
            "last_d": int(c5.get("last_d", 7)),
            "last_harmony_frac": float(c5.get("last_harmony_frac", 0.0)),
            # emergent recomputed on first step under 7-dim's own glue split.
            "emergent": 0.0,
            "W_trace": sum(W_7[i][i] for i in range(7)),
            "W_strongest": c5.get("W_strongest"),
            "prev_op": c5.get("prev_op"),
            "prev_profile": prev_profile_7,
        },
        "_migration": {
            "from_dim": 5,
            "to_dim": 7,
            "from_path": str(in_path),
            "preserved_W_top_left_5x5": True,
            "new_dims_zero_init": ["intent (5)", "echo (6)"],
            "prev_profile_7d_seed": (
                "dim 5 = depth(2); dim 6 = aperture(0)"
                if prev_profile_7 else "none"
            ),
        },
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(state_7, f, indent=2)

    print(f"migrated 5-dim -> 7-dim cortex state:")
    print(f"  input:  {in_path}")
    print(f"  output: {out_path}")
    print(f"  W_trace (5-dim): {sum(W_5[i][i] for i in range(5)):.4f}")
    print(f"  W_trace (7-dim): {sum(W_7[i][i] for i in range(7)):.4f}")
    print(f"  ticks: {state_7['cortex']['tick']}")
    print(f"  hebbian.ticks: {state_7['hebbian']['ticks']}")
    print(f"  prev_profile: {prev_profile_7}")
    print()
    print("the live cortex_state.json was NOT modified.")
    print(f"to use: set CK_CORTEX_DIM=7 in ck_boot_api environment")
    return 0


if __name__ == "__main__":
    sys.exit(main())
