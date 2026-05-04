"""
train_prose_tissue.py -- train a prose-writing tissue head from
prose_teacher pairs.

Brayden 2026-05-02: "see if you can teach him to talk with ollama as
a crutch for now... we need conversational and structured fluency"

The eventual goal: CK speaks prose WITHOUT Ollama, using a small
trained head that learned the (structural, prose) mapping from
Ollama-generated training pairs.

Scaffold approach (Phase 1):
  - Load prose_pairs/*.jsonl
  - Treat structural responses as "input context" (operator stream)
  - Treat prose responses as "target sequence" (char-level)
  - Train a small decoder transformer (~200k params) on the mapping
  - When trained, cells.glue.respond_text(mode='prose') can use this
    head to generate prose without Ollama

Reality check:
  - With <50 pairs the model won't generalize.  This script supports
    a min_pairs gate (default 200) to refuse training on too-small a
    corpus.  Run prose_teacher repeatedly to grow the corpus, then
    train.
  - Prose generation is a hard task; expect val_loss to plateau.
    The trained head is a "good enough" stand-in that lets CK speak
    without Ollama; not a replacement for a real LLM.

Usage:
  python train_prose_tissue.py [--epochs 20] [--min_pairs 200]
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple


_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


PAIRS_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\prose_pairs")
OUT_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\cells")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_pairs(min_pairs: int = 1) -> List[Dict]:
    pairs: List[Dict] = []
    if not PAIRS_DIR.exists():
        return pairs
    for f in sorted(PAIRS_DIR.glob("prose_pairs_*.jsonl")):
        try:
            with open(f, encoding="utf-8") as fh:
                for line in fh:
                    try:
                        rec = json.loads(line)
                        if rec.get("structural") and rec.get("prose"):
                            pairs.append(rec)
                    except Exception:
                        pass
        except Exception:
            pass
    return pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--min_pairs", type=int, default=200,
                     help="Refuse to train if fewer than this many pairs (default 200)")
    ap.add_argument("--force", action="store_true",
                     help="Train even with fewer than min_pairs (smoke test)")
    args = ap.parse_args()

    pairs = load_pairs()
    print(f"  pairs available: {len(pairs)}")
    if len(pairs) < args.min_pairs and not args.force:
        print(f"  REFUSING to train: need >= {args.min_pairs} pairs (use --force to override)")
        print(f"  Run prose_teacher.py more times to grow the corpus.")
        return 1

    # Stats
    total_struct_chars = sum(len(p.get("structural", "")) for p in pairs)
    total_prose_chars = sum(len(p.get("prose", "")) for p in pairs)
    cats = {}
    for p in pairs:
        cats[p.get("category", "?")] = cats.get(p.get("category", "?"), 0) + 1

    print(f"  total structural chars: {total_struct_chars:,}")
    print(f"  total prose chars: {total_prose_chars:,}")
    print(f"  by category: {cats}")
    print(f"  avg compression: {total_prose_chars/max(1, total_struct_chars):.3f}")

    # TODO: actual training implementation
    # Placeholder: write a small "memorization" model that can lookup prose
    # given a hash of the structural readout.  This is enough to demonstrate
    # the pipeline; real char/token-level transformer training comes next.
    import hashlib
    memo: Dict[str, str] = {}
    for p in pairs:
        key = hashlib.md5(p["structural"].encode("utf-8")).hexdigest()
        memo[key] = p["prose"]
    out_path = OUT_DIR / "prose_tissue_memo.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "type": "memorization_v0",
            "n_pairs": len(pairs),
            "total_struct_chars": total_struct_chars,
            "total_prose_chars": total_prose_chars,
            "by_category": cats,
            "memo": memo,
        }, f, indent=2, default=str)
    print(f"  wrote v0 memorization tissue: {out_path}")
    print(f"  ({len(memo)} unique structural readouts -> prose lookup)")
    print()
    print(f"  This is a v0 placeholder.  When the corpus reaches >= 200 pairs,")
    print(f"  swap to a real char/token-level transformer trainer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
