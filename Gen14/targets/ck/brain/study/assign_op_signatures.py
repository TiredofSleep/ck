"""
assign_op_signatures.py -- retroactively assign op_signatures to runtime
crystals.

Each runtime crystal in runtime_crystals.json is examined for operator-word
frequency in its fact text. The top 1-3 most-frequent operators become its
op_signature. Updates the JSON in place so CK's cortex_voice picks them up
on next boot.

Why: dream_daemon.pick_crystals_for_dream() weights by op_signature overlap
with recent operator state. Crystals without op_signature score 0 and rarely
get picked. After this runs, runtime crystals contribute to dreams.

Usage:
    python assign_op_signatures.py            # update in place
    python assign_op_signatures.py --dry-run  # show would-be assignments
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
GEN13_TARGETS_CK = GEN13_BRAIN.parent
GEN13_ROOT = GEN13_TARGETS_CK.parent.parent

DEFAULT_PATH = GEN13_ROOT / "var" / "runtime_crystals.json"

# Operator name -> ID
OP_TO_ID = {
    "VOID": 0,
    "LATTICE": 1,
    "COUNTER": 2,
    "PROGRESS": 3,
    "COLLAPSE": 4,
    "BALANCE": 5,
    "CHAOS": 6,
    "HARMONY": 7,
    "BREATH": 8,
    "RESET": 9,
}


def assign_signature(fact: str, max_ops: int = 3) -> tuple:
    """Return tuple of operator IDs that appear most frequently in fact text.
    Picks up to max_ops; only includes operators that appear at least once."""
    text = fact.upper()
    counts = Counter()
    for name, op_id in OP_TO_ID.items():
        # Count whole-word matches (with possible punctuation around)
        pattern = r"\b" + re.escape(name) + r"\b"
        matches = re.findall(pattern, text)
        if matches:
            counts[op_id] = len(matches)
    if not counts:
        return ()
    top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:max_ops]
    return tuple(sorted([op_id for op_id, _ in top]))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--path", default=str(DEFAULT_PATH))
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"runtime_crystals.json not found at {path}", file=sys.stderr)
        return 2

    with open(path) as f:
        crystals = json.load(f)

    print(f"loaded {len(crystals)} runtime crystals from {path}")

    updated = 0
    skipped_already = 0
    skipped_no_ops = 0
    for c in crystals:
        fact = c.get("fact", "")
        first_word = fact.split(":", 1)[0].strip() if ":" in fact else "(unknown)"
        existing = c.get("op_signature")
        if existing:
            skipped_already += 1
            continue
        sig = assign_signature(fact)
        if not sig:
            skipped_no_ops += 1
            print(f"  SKIP {first_word}: no operator words in fact")
            continue
        op_names = [n for n, oid in OP_TO_ID.items() if oid in sig]
        print(f"  {first_word}: op_signature={sig} ({'+'.join(op_names)})")
        if not args.dry_run:
            c["op_signature"] = list(sig)
        updated += 1

    print()
    print(f"updated: {updated}")
    print(f"skipped (already had signature): {skipped_already}")
    print(f"skipped (no operator words found): {skipped_no_ops}")

    if args.dry_run:
        print("(dry-run; not saving)")
    else:
        with open(path, "w") as f:
            json.dump(crystals, f, indent=2)
        print(f"saved -> {path}")
        print(f"restart CK to pick up new signatures")

    return 0


if __name__ == "__main__":
    sys.exit(main())
