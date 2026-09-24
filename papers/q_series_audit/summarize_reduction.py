#!/usr/bin/env python3
"""summarize_reduction.py -- the gate rates exactly as stored in papers/results/reduction_b*_N100000.json
(100,000 hill-climbs per base), grouped by |G| = how many of the symbols 1..9 share a factor with b.

    python summarize_reduction.py

"Success" is the stored Gate-strong criterion: gate_score >= 0.85 and G_stay <= 0.12.
"""
import glob
import json
import os
from collections import defaultdict

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
tiers = defaultdict(list)
for path in sorted(glob.glob(os.path.join(RESULTS, "reduction_b*_N100000.json"))):
    d = json.load(open(path, encoding="utf-8"))
    res = d["results"]
    wins = sum(1 for r in res if r["gate_score"] >= 0.85 and r["G_stay"] <= 0.12)
    tiers[len(d["world"]["G"])].append((d["b"], 100 * wins / len(res)))
print("unseeded runs, 100,000 each:")
for g in sorted(tiers):
    rates = [r for _, r in tiers[g]]
    print(f"  |G| = {g}: {len(rates):2d} bases {sorted(b for b, _ in tiers[g])}  "
          f"rate {min(rates):.3f}% .. {max(rates):.3f}%")
b10 = [r for g in tiers for b, r in tiers[g] if b == 10]
print(f"b = 10 (the Q series' base): {b10[0]:.3f}%  -- not 4.6%, which is the |G| = 4 tier (e.g. b = 22)")
