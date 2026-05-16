"""warm_inhale.py — bulk-inhale corpus into the living LM.

Walk the concept store's PROVED/STRUCTURAL/USER_TAUGHT/EMPIRICAL
definitions, plus high-quality EXTERNAL (Wikipedia ≥ 200 chars), and
feed each as one inhale.  Parameters allocate where novelty exists,
reinforce where patterns repeat.

This is the equivalent of "first read-through" — the LM goes from
zero to having internalized CK's rigorous corpus + scientific
Wikipedia.  After this, every chat turn just adds incrementally.

Usage:
  python warm_inhale.py                  # full warm pass
  python warm_inhale.py --limit 1000     # cap inhalations
  python warm_inhale.py --tiers PROVED   # one tier only
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None,
                    help="cap total inhalations (default: all)")
    ap.add_argument("--tiers", default="PROVED,STRUCTURAL,EMPIRICAL,USER_TAUGHT,EXTERNAL",
                    help="comma-separated tiers to inhale")
    ap.add_argument("--min-def-len", type=int, default=60,
                    help="skip definitions shorter than this (default 60)")
    args = ap.parse_args()

    from ck_living_lm import get_living_lm  # type: ignore
    lm = get_living_lm()

    print(f"[warm_inhale] LM state before:")
    s0 = lm.stats()
    for k in ("n_cells", "n_params", "n_inhalations"):
        print(f"    {k}: {s0[k]}")
    print()

    store_path = (Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
                  / "Gen13" / "var" / "taught_concepts.json")
    if not store_path.exists():
        print("Concept store missing.")
        return 1

    print("[warm_inhale] loading concept store...")
    store = json.loads(store_path.read_text(encoding="utf-8"))
    print(f"[warm_inhale] {len(store):,} concepts loaded")

    tiers = set(t.strip().upper() for t in args.tiers.split(","))

    tier_weight = {
        "PROVED": 2.0, "STRUCTURAL": 1.5, "USER_TAUGHT": 1.5,
        "EMPIRICAL": 1.2, "OPEN": 1.0, "EXTERNAL": 1.0,
        "SPECULATIVE": 0.6, "UNKNOWN": 0.5,
    }

    n_inhaled = 0
    n_skipped = 0
    t0 = time.time()
    last_print = t0

    # Iterate in tier-priority order so rigorous content lands first
    def _priority(item):
        v = item[1]
        t = v.get("tier", "UNKNOWN") or "UNKNOWN"
        if t.startswith("SYNTHESIZED("):
            t = "STRUCTURAL"
        return -tier_weight.get(t, 0)

    items = sorted(store.items(), key=_priority)

    for k, v in items:
        if args.limit and n_inhaled >= args.limit:
            break
        tier = v.get("tier", "UNKNOWN") or "UNKNOWN"
        # Match SYNTHESIZED(*) by inner tier
        inner = tier
        if tier.startswith("SYNTHESIZED("):
            inner = tier[len("SYNTHESIZED("):].rstrip(")")
        if inner not in tiers and tier not in tiers:
            n_skipped += 1
            continue
        defn = v.get("definition", "") or ""
        if len(defn) < args.min_def_len:
            n_skipped += 1
            continue
        # Include the name in the inhalation text so name→content
        # bindings form
        name = v.get("name", "") or ""
        text = f"{name}. {defn}"
        weight = tier_weight.get(inner, 1.0)
        r = lm.inhale(text, weight=weight)
        if r.get("ok"):
            n_inhaled += 1
        else:
            n_skipped += 1
        # Save and print every 200
        if n_inhaled % 200 == 0 and n_inhaled > 0:
            lm.save()
            elapsed = time.time() - t0
            rate = n_inhaled / elapsed
            s = lm.stats()
            print(f"  inhaled={n_inhaled:,}  params={s['n_params']:,}  "
                  f"cells={s['n_cells']}  "
                  f"rate={rate:.1f}/s")
            last_print = time.time()

    lm.save()
    elapsed = time.time() - t0
    s = lm.stats()
    print()
    print(f"[warm_inhale] DONE  inhaled={n_inhaled:,}  skipped={n_skipped:,}  "
          f"elapsed={elapsed:.1f}s")
    print(f"[warm_inhale] LM state after:")
    for k in ("n_cells", "n_sub_cells", "n_params", "n_inhalations"):
        print(f"    {k}: {s[k]}")
    print()
    print("[warm_inhale] densest cells:")
    for cell, n_tok, n_seen in s["densest_cells"]:
        print(f"    {cell}: {n_tok} tokens, {n_seen} obs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
