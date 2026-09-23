"""
bench_extensions.py -- ablations and extensions of the RGD bench.

After the 30k run identified "RGD d=2 vs DP eps=0.1" as the
scale-stable real win on UCI Adult, the natural research questions
are:

  E1.  Is the d=2 win STRUCTURAL (the canonical 4-core shell
       {V,H,Br,R}) or would ANY size-4 shell work?
       (4-core ablation -- the headline scientific question.)

  E2.  DP results use a single fixed seed.  What are the error bars?
       (Multi-seed DP at each epsilon; mean +/- std.)

  E3.  Does the win hold at the FULL Adult sample (32 562 rows)?
       (Sanity check.)

  E4.  What does the RGD trajectory look like at d=7, d=8 (shells of
       size 9, 10 = nearly-no-suppression)?  (Extended grid.)

  E5.  The current attacker is k-anon-style 1/K re-identification.
       What does an ATTRIBUTE-DISCLOSURE attacker (predict the
       sensitive value, not re-id the row) say?

This module runs E1-E5 against the same datasets used by the main
bench harness.  Output: bench_extensions_results.jsonl + a markdown
summary.

Copyright (c) 2026 Brayden Ross Sanders / 7SiTe LLC.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import statistics
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Set, Tuple

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)

import bench_rgd_vs_dp_kanon as bm  # noqa: E402


# =====================================================================
# E1 -- 4-core ablation
# =====================================================================
def rgd_tabular_custom_shell(
    rows: List[List[str]],
    shell: Set[int],
) -> List[List[str]]:
    """Same as bm.rgd_tabular but uses an explicit shell instead of
    the canonical CHAIN_SUBMAGMAS[d].  Lets us compare structurally-
    chosen shells vs random ones."""
    out = []
    for row in rows:
        new_row = []
        for c, v in enumerate(row[:-1]):
            h = (hash((c, v)) % 10 + 10) % 10
            if h in shell:
                new_row.append(v)
            else:
                new_row.append("*")
        new_row.append(row[-1])
        out.append(new_row)
    return out


def _random_size4_shells(n_trials: int, seed: int = 7) -> List[Set[int]]:
    rng = random.Random(seed)
    seen: Set[frozenset] = set()
    shells: List[Set[int]] = []
    while len(shells) < n_trials:
        s = frozenset(rng.sample(range(10), 4))
        if s in seen:
            continue
        seen.add(s)
        shells.append(set(s))
    return shells


def run_e1_ablation(rows: List[List[str]], n_random: int = 5) -> Dict[str, Any]:
    """E1: compare canonical 4-core shell vs N random size-4 shells."""
    canonical = {0, 7, 8, 9}  # the 4-core {VOID, HARMONY, BREATH, RESET}
    randoms = _random_size4_shells(n_random)

    results: List[Dict[str, Any]] = []
    # canonical
    priv = rgd_tabular_custom_shell(rows, canonical)
    a = bm.attacker_tabular(rows, priv)
    u = bm.utility_tabular(rows, priv)
    results.append({
        "shell":      sorted(canonical),
        "label":      "canonical 4-core (V,H,Br,R)",
        "attacker":   a,
        "utility":    u,
    })

    for sh in randoms:
        priv = rgd_tabular_custom_shell(rows, sh)
        a = bm.attacker_tabular(rows, priv)
        u = bm.utility_tabular(rows, priv)
        results.append({
            "shell":    sorted(sh),
            "label":    f"random size-4 {sorted(sh)}",
            "attacker": a,
            "utility":  u,
        })

    # Stats over random shells
    rand_attacks = [r["attacker"] for r in results[1:]]
    rand_utils = [r["utility"] for r in results[1:]]
    canon = results[0]
    summary = {
        "n_random_shells":  n_random,
        "canonical_attacker": canon["attacker"],
        "canonical_utility":  canon["utility"],
        "random_attacker_mean":  statistics.mean(rand_attacks),
        "random_attacker_std":   statistics.stdev(rand_attacks) if len(rand_attacks) >= 2 else 0.0,
        "random_attacker_min":   min(rand_attacks),
        "random_attacker_max":   max(rand_attacks),
        "random_utility_mean":   statistics.mean(rand_utils),
        "random_utility_std":    statistics.stdev(rand_utils) if len(rand_utils) >= 2 else 0.0,
        "random_utility_min":    min(rand_utils),
        "random_utility_max":    max(rand_utils),
        "canonical_uniquely_dominant":
            canon["attacker"] < min(rand_attacks) and canon["utility"] >= statistics.mean(rand_utils),
    }

    return {"per_shell": results, "summary": summary}


# =====================================================================
# E2 -- Multi-seed DP error bars
# =====================================================================
def run_e2_dp_seeds(rows: List[List[str]], eps_grid: List[float], n_seeds: int = 10) -> List[Dict[str, Any]]:
    """E2: at each epsilon, run DP with n_seeds and report mean/std."""
    results: List[Dict[str, Any]] = []
    for eps in eps_grid:
        attackers: List[float] = []
        utils: List[float] = []
        for seed in range(n_seeds):
            rng = random.Random(1000 + seed)
            priv = bm.dp_tabular(rows, eps, rng)
            a = bm.attacker_tabular(rows, priv)
            u = bm.utility_tabular(rows, priv)
            attackers.append(a)
            utils.append(u)
        results.append({
            "epsilon":       eps,
            "n_seeds":       n_seeds,
            "attacker_mean": statistics.mean(attackers),
            "attacker_std":  statistics.stdev(attackers) if n_seeds >= 2 else 0.0,
            "utility_mean":  statistics.mean(utils),
            "utility_std":   statistics.stdev(utils) if n_seeds >= 2 else 0.0,
            "attacker_raw":  attackers,
            "utility_raw":   utils,
        })
    return results


# =====================================================================
# E3 -- Full Adult run
# =====================================================================
# (Just use bm.* directly with all rows; lives in main())


# =====================================================================
# E4 -- Extended depth grid (d=7, d=8)
# =====================================================================
def run_e4_extended_depths(rows: List[List[str]], depths: List[int]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for d in depths:
        priv = bm.rgd_tabular(rows, d)
        a = bm.attacker_tabular(rows, priv)
        u = bm.utility_tabular(rows, priv)
        results.append({
            "depth":    d,
            "attacker": a,
            "utility":  u,
        })
    return results


# =====================================================================
# E5 -- Attribute-disclosure attacker
# =====================================================================
def attribute_disclosure_attacker(orig: List[List[str]], priv: List[List[str]]) -> float:
    """
    Attribute-disclosure attack: the attacker has the released priv
    rows and tries to guess the sensitive value of a target orig row
    by linking via QID.  Score = fraction of target rows for which the
    attacker correctly predicts the sensitive value.

    Stronger than the 1/K re-id attacker because it specifically
    targets the sensitive attribute, not row identity.
    """
    if not priv:
        return float("nan")
    # Build priv-QID -> Counter(sensitive) lookup
    groups: Dict[Tuple[str, ...], Counter] = defaultdict(Counter)
    for r in priv:
        groups[tuple(r[:-1])][r[-1]] += 1
    # For each orig row, the attacker's best guess = majority sensitive
    # of the priv group matching the orig's (true) QID (treating "*"
    # in priv-QID as wildcard match)
    correct = 0
    for r in orig:
        true_sens = r[-1]
        qid = tuple(r[:-1])
        # exact match
        candidate = groups.get(qid)
        # wildcard match
        if not candidate:
            combined: Counter = Counter()
            for pk, dist in groups.items():
                if "*" in pk and bm._qid_matches(pk, qid):
                    combined.update(dist)
            candidate = combined if combined else None
        if candidate:
            pred, _ = candidate.most_common(1)[0]
            if pred == true_sens:
                correct += 1
    return correct / max(len(orig), 1)


def run_e5_attribute_attacker(rows: List[List[str]], knobs: Dict[str, List]) -> List[Dict[str, Any]]:
    """E5: re-evaluate all methods/knobs under attribute-disclosure attack."""
    out: List[Dict[str, Any]] = []
    rng = random.Random(2026)
    # RGD
    for d in knobs["rgd"]:
        priv = bm.rgd_tabular(rows, d)
        a_reid = bm.attacker_tabular(rows, priv)
        a_attr = attribute_disclosure_attacker(rows, priv)
        u = bm.utility_tabular(rows, priv)
        out.append({"method": "RGD", "knob": f"d={d}", "attacker_reid": a_reid, "attacker_attr": a_attr, "utility": u})
    # DP
    for eps in knobs["dp"]:
        priv = bm.dp_tabular(rows, eps, rng)
        a_reid = bm.attacker_tabular(rows, priv)
        a_attr = attribute_disclosure_attacker(rows, priv)
        u = bm.utility_tabular(rows, priv)
        out.append({"method": "DP", "knob": f"eps={eps}", "attacker_reid": a_reid, "attacker_attr": a_attr, "utility": u})
    # k-anon
    for k in knobs["kanon"]:
        priv = bm.kanon_tabular(rows, k)
        a_reid = bm.attacker_tabular(rows, priv)
        a_attr = attribute_disclosure_attacker(rows, priv)
        u = bm.utility_tabular(rows, priv)
        out.append({"method": "k-anon", "knob": f"k={k}", "attacker_reid": a_reid, "attacker_attr": a_attr, "utility": u})
    return out


# =====================================================================
# Main
# =====================================================================
def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="RGD bench extensions")
    parser.add_argument("--tabular", default="bench_data/adult.data")
    parser.add_argument("--max-rows", type=int, default=30000)
    parser.add_argument("--out-jsonl", default="bench_extensions_results.jsonl")
    parser.add_argument("--out-md", default="bench_extensions_verdict.md")
    parser.add_argument("--skip", default="", help="comma-separated experiments to skip: e1,e2,e3,e4,e5")
    args = parser.parse_args(argv)

    skip = {s.strip() for s in args.skip.split(",") if s.strip()}

    print("=== Bench extensions ===")
    tabular = bm.load_tabular(args.tabular)
    all_rows = tabular[0]
    print(f"Loaded {len(all_rows)} rows from {tabular[3]}")
    if args.max_rows and len(all_rows) > args.max_rows:
        rows = all_rows[:args.max_rows]
        print(f"Using first {args.max_rows} for E1/E2/E4/E5")
    else:
        rows = all_rows

    results: Dict[str, Any] = {}

    if "e1" not in skip:
        print("\n--- E1: 4-core ablation (canonical vs 5 random size-4 shells) ---")
        t0 = time.time()
        e1 = run_e1_ablation(rows, n_random=5)
        results["e1"] = e1
        for row in e1["per_shell"]:
            print(f"  {row['label']:40s}  attacker={row['attacker']:.4f}  utility={row['utility']:.4f}")
        s = e1["summary"]
        print(f"  canonical (V,H,Br,R):       attacker={s['canonical_attacker']:.4f}  utility={s['canonical_utility']:.4f}")
        print(f"  random size-4 mean +/- std: attacker={s['random_attacker_mean']:.4f} +/- {s['random_attacker_std']:.4f}  utility={s['random_utility_mean']:.4f} +/- {s['random_utility_std']:.4f}")
        print(f"  canonical uniquely dominant: {s['canonical_uniquely_dominant']}")
        print(f"  ({time.time() - t0:.1f}s)")

    if "e2" not in skip:
        print("\n--- E2: Multi-seed DP error bars (10 seeds per epsilon) ---")
        t0 = time.time()
        e2 = run_e2_dp_seeds(rows, eps_grid=[0.1, 1.0, 10.0], n_seeds=10)
        results["e2"] = e2
        for r in e2:
            print(f"  DP eps={r['epsilon']:5.2f}:  attacker={r['attacker_mean']:.4f} +/- {r['attacker_std']:.4f}  utility={r['utility_mean']:.4f} +/- {r['utility_std']:.4f}")
        print(f"  ({time.time() - t0:.1f}s)")

    if "e3" not in skip and len(all_rows) > args.max_rows:
        print(f"\n--- E3: Full Adult sample ({len(all_rows)} rows, max-rows={args.max_rows} ignored) ---")
        t0 = time.time()
        # Just run RGD d=2, DP eps=0.1, k-anon k=25 at full sample for comparison
        priv = bm.rgd_tabular(all_rows, 2)
        e3_rgd = {
            "method": "RGD", "knob": "d=2",
            "attacker": bm.attacker_tabular(all_rows, priv),
            "utility":  bm.utility_tabular(all_rows, priv),
            "n_rows":   len(all_rows),
        }
        rng = random.Random(1729)
        priv = bm.dp_tabular(all_rows, 0.1, rng)
        e3_dp = {
            "method": "DP", "knob": "eps=0.1",
            "attacker": bm.attacker_tabular(all_rows, priv),
            "utility":  bm.utility_tabular(all_rows, priv),
            "n_rows":   len(all_rows),
        }
        priv = bm.kanon_tabular(all_rows, 25)
        e3_ka = {
            "method": "k-anon", "knob": "k=25",
            "attacker": bm.attacker_tabular(all_rows, priv),
            "utility":  bm.utility_tabular(all_rows, priv),
            "n_rows":   len(all_rows),
        }
        results["e3"] = [e3_rgd, e3_dp, e3_ka]
        for r in [e3_rgd, e3_dp, e3_ka]:
            print(f"  {r['method']:7s} {r['knob']:10s}  attacker={r['attacker']:.4f}  utility={r['utility']:.4f}  (n={r['n_rows']})")
        # Dominance check
        rgd_dom_dp = e3_rgd["attacker"] < e3_dp["attacker"] and e3_rgd["utility"] > e3_dp["utility"]
        print(f"  RGD d=2 strictly dominates DP eps=0.1 at full sample: {rgd_dom_dp}")
        print(f"  ({time.time() - t0:.1f}s)")

    if "e4" not in skip:
        print("\n--- E4: Extended depth grid (d=7, d=8) ---")
        t0 = time.time()
        e4 = run_e4_extended_depths(rows, depths=[7, 8])
        results["e4"] = e4
        for r in e4:
            print(f"  RGD d={r['depth']}:  attacker={r['attacker']:.4f}  utility={r['utility']:.4f}")
        print(f"  ({time.time() - t0:.1f}s)")

    if "e5" not in skip:
        print("\n--- E5: Attribute-disclosure attacker (predict sensitive given QID) ---")
        t0 = time.time()
        knobs = {"rgd": [1, 2, 3, 4, 5, 6], "dp": [0.1, 1.0, 10.0], "kanon": [5, 10, 25]}
        e5 = run_e5_attribute_attacker(rows, knobs)
        results["e5"] = e5
        # Baseline: predict majority sensitive
        sens_counter = Counter(r[-1] for r in rows)
        baseline = sens_counter.most_common(1)[0][1] / max(len(rows), 1)
        results["e5_baseline"] = baseline
        print(f"  Baseline (predict majority {sens_counter.most_common(1)[0][0]!r}): {baseline:.4f}")
        for r in e5:
            adv = r["attacker_attr"] - baseline
            print(f"  {r['method']:7s} {r['knob']:10s}  attr_attack={r['attacker_attr']:.4f}  ({adv:+.4f} vs baseline)  reid={r['attacker_reid']:.4f}  utility={r['utility']:.4f}")
        print(f"  ({time.time() - t0:.1f}s)")

    # Persist
    with open(args.out_jsonl, "w", encoding="utf-8") as f:
        for k, v in results.items():
            f.write(json.dumps({"experiment": k, "result": v}) + "\n")

    print(f"\nWrote {args.out_jsonl}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
