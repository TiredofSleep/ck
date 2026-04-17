"""
run_discovery.py -- Run prior-free discovery on every B1 + B2 dataset.

Produces:
    results/b1_5_fingerprints.json   (15 configs, n=10, varying noise)
    results/b2_5_fingerprints.json   (24 configs, n in {10,14,22,34})
    results/invariants_b1_5.json     (what's constant across noise/seeds at n=10?)
    results/invariants_b2_5.json     (what's constant across carriers/wobble?)
    results/canonical_vs_discovered.json  (side-by-side compare)

Then prints a console summary of the structural invariants found.
"""

import os, json, sys
from collections import defaultdict
from typing import Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from discovery_fitter import discover, fingerprint  # noqa: E402

SPRINT_DIR = os.path.dirname(HERE)  # ...sprint21
PAPERS_DIR = os.path.dirname(SPRINT_DIR)  # ...papers
RESULTS_DIR = os.path.join(SPRINT_DIR, "results")

B1_DATA = os.path.normpath(os.path.join(
    PAPERS_DIR, "sprint18_b1_nscg_benchmark_2026_04_17",
    "impl", "data"))
B2_DATA = os.path.normpath(os.path.join(
    PAPERS_DIR, "sprint19_b2_wrg_benchmark_2026_04_17",
    "impl", "data"))


# ============================================================
# Canonical structures (used ONLY for after-the-fact comparison)
# ============================================================

def v2(k):
    if k == 0:
        return 0
    n = 0
    while k % 2 == 0:
        k //= 2
        n += 1
    return n


def canonical_units(n):
    from math import gcd
    return [u for u in range(1, n) if gcd(u, n) == 1]


def canonical_sigma(n):
    return {u: v2(3 * u + 1) for u in canonical_units(n)}


def canonical_partition(n):
    """Group units by canonical sigma value."""
    sig = canonical_sigma(n)
    by = defaultdict(list)
    for u, s in sig.items():
        by[s].append(u)
    return sorted([sorted(v) for v in by.values()])


def canonical_core(n):
    """Core = units \\ {1}."""
    return [u for u in canonical_units(n) if u != 1]


# ============================================================
# Run on B1
# ============================================================

def run_b1():
    print(f"=== B1.5: prior-free discovery on B1 data (n=10) ===")
    print(f"B1 data dir: {B1_DATA}")
    fps = []
    full = []
    for fn in sorted(os.listdir(B1_DATA)):
        if not fn.endswith(".csv"):
            continue
        path = os.path.join(B1_DATA, fn)
        disc = discover(path, n=10, z_T_col=2)
        fp = fingerprint(disc)
        fp["file"] = fn
        # also extract noise level from filename
        # nscg_N100000_p005_s0.csv  -> p_noise=0.05
        if "p005" in fn:    fp["p_noise"] = 0.05
        elif "p015" in fn:  fp["p_noise"] = 0.15
        elif "p030" in fn:  fp["p_noise"] = 0.30
        else:               fp["p_noise"] = None
        fps.append(fp)
        full.append({"file": fn, "discovery": disc})
        print(f"  {fn:30s}  h={fp['h_hat']}  core={fp['core_outputs']}  "
              f"|seam|={fp['seam_cell_count']}  units={fp['units_hat']}")
    with open(os.path.join(RESULTS_DIR, "b1_5_fingerprints.json"), "w") as f:
        json.dump(fps, f, indent=2)
    return fps, full


def run_b2():
    print(f"\n=== B2.5: prior-free discovery on B2 data (n in {{10,14,22,34}}) ===")
    print(f"B2 data dir: {B2_DATA}")
    fps = []
    full = []
    for fn in sorted(os.listdir(B2_DATA)):
        if not fn.endswith(".csv"):
            continue
        path = os.path.join(B2_DATA, fn)
        disc = discover(path, n=None, z_T_col=2)  # z_T col 2 of x,y,z_T,z_B
        fp = fingerprint(disc)
        fp["file"] = fn
        # extract pw from filename: wrg_n14_pw20_s0
        if "_pw5_" in fn:    fp["p_wobble"] = 0.05
        elif "_pw20_" in fn: fp["p_wobble"] = 0.20
        else:                fp["p_wobble"] = None
        fps.append(fp)
        full.append({"file": fn, "discovery": disc})
        print(f"  {fn:25s}  h={fp['h_hat']}  core={fp['core_outputs']}  "
              f"|seam|={fp['seam_cell_count']}  units={fp['units_hat']}")
    with open(os.path.join(RESULTS_DIR, "b2_5_fingerprints.json"), "w") as f:
        json.dump(fps, f, indent=2)
    return fps, full


# ============================================================
# Invariant analysis
# ============================================================

def invariants(fps, group_key=None):
    """
    Identify which fingerprint fields are constant across the set.
    If group_key is given, group first and report invariants per group.
    """
    fields = ["h_hat", "image_T", "core_outputs", "units_hat",
              "partition_hat", "seam_cell_count", "seam_by_rule_counts",
              "ratio_attractor", "ratio_zero", "ratio_seam"]

    def constant_across(rows, field):
        vals = [json.dumps(r[field], sort_keys=True) for r in rows]
        return len(set(vals)) == 1

    def value_summary(rows, field):
        vals = [json.dumps(r[field], sort_keys=True) for r in rows]
        from collections import Counter
        c = Counter(vals)
        return [{"value": json.loads(k), "count": v} for k, v in c.most_common()]

    if group_key is None:
        result = {"global": {}}
        for f in fields:
            result["global"][f] = {
                "constant": constant_across(fps, f),
                "values": value_summary(fps, f),
            }
        return result

    by_group = defaultdict(list)
    for r in fps:
        key = json.dumps(r[group_key])
        by_group[key].append(r)
    result = {}
    for k, rows in by_group.items():
        result[f"{group_key}={k}"] = {
            "n_configs": len(rows),
        }
        for f in fields:
            result[f"{group_key}={k}"][f] = {
                "constant": constant_across(rows, f),
                "values": value_summary(rows, f),
            }
    return result


# ============================================================
# Canonical vs discovered comparison
# ============================================================

def compare_canonical(fps):
    """
    For each unique n in fps, compare canonical (units, sigma partition,
    core) against the discovered (units_hat, partition_hat, core_outputs)
    consensus across configs.
    """
    out = {}
    by_n = defaultdict(list)
    for r in fps:
        by_n[r["n"]].append(r)

    for n, rows in sorted(by_n.items()):
        # Take the most common discovered values
        from collections import Counter
        units_c = Counter(json.dumps(r["units_hat"]) for r in rows).most_common(1)[0]
        core_c = Counter(json.dumps(r["core_outputs"]) for r in rows).most_common(1)[0]
        part_c = Counter(json.dumps(r["partition_hat"]) for r in rows).most_common(1)[0]
        sb_c = Counter(json.dumps(r["seam_by_rule_counts"], sort_keys=True)
                       for r in rows).most_common(1)[0]

        out[f"n={n}"] = {
            "configs_used": len(rows),
            "canonical": {
                "units":     canonical_units(n),
                "sigma":     {str(k): v for k, v in canonical_sigma(n).items()},
                "partition": canonical_partition(n),
                "core":      canonical_core(n),
            },
            "discovered_consensus": {
                "units":          json.loads(units_c[0]),
                "core_outputs":   json.loads(core_c[0]),
                "partition":      json.loads(part_c[0]),
                "seam_by_rule":   json.loads(sb_c[0]),
                "consensus_rate_units":     units_c[1] / len(rows),
                "consensus_rate_core":      core_c[1] / len(rows),
                "consensus_rate_partition": part_c[1] / len(rows),
            },
            "agreement": {
                "units_match_canonical":
                    set(json.loads(units_c[0])) == set(canonical_units(n)),
                "core_match_canonical":
                    set(json.loads(core_c[0])) == set(canonical_core(n)),
                "partition_match_canonical":
                    sorted(json.loads(part_c[0])) ==
                    sorted(canonical_partition(n)),
            },
        }
    return out


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    fps_b1, full_b1 = run_b1()
    fps_b2, full_b2 = run_b2()

    print("\n=== B1.5 invariants across noise + seeds (n=10) ===")
    inv_b1 = invariants(fps_b1)
    with open(os.path.join(RESULTS_DIR, "invariants_b1_5.json"), "w") as f:
        json.dump(inv_b1, f, indent=2)
    for field, info in inv_b1["global"].items():
        flag = "INVARIANT" if info["constant"] else "varies"
        if info["constant"]:
            v = info["values"][0]["value"]
            v_str = json.dumps(v) if not isinstance(v, dict) else json.dumps(v, sort_keys=True)
            v_str = v_str[:80]
            print(f"  [{flag:>10}]  {field:25s}  = {v_str}")
        else:
            print(f"  [{flag:>10}]  {field:25s}  ({len(info['values'])} distinct)")

    print("\n=== B2.5 invariants per carrier (across wobble + seeds) ===")
    inv_b2 = invariants(fps_b2, group_key="n")
    with open(os.path.join(RESULTS_DIR, "invariants_b2_5.json"), "w") as f:
        json.dump(inv_b2, f, indent=2)
    for grp, info in sorted(inv_b2.items()):
        print(f"\n-- {grp} ({info['n_configs']} configs) --")
        for field in ["h_hat", "image_T", "core_outputs", "units_hat",
                      "partition_hat", "seam_cell_count",
                      "seam_by_rule_counts"]:
            d = info[field]
            flag = "INVARIANT" if d["constant"] else "varies"
            if d["constant"]:
                v = d["values"][0]["value"]
                v_str = json.dumps(v, sort_keys=True)[:80]
                print(f"  [{flag:>10}]  {field:25s}  = {v_str}")
            else:
                print(f"  [{flag:>10}]  {field:25s}")

    print("\n=== Canonical vs discovered: B1 (n=10) ===")
    cmp_b1 = compare_canonical(fps_b1)
    print(json.dumps(cmp_b1, indent=2))

    print("\n=== Canonical vs discovered: B2 (4 carriers) ===")
    cmp_b2 = compare_canonical(fps_b2)
    print(json.dumps(cmp_b2, indent=2))

    with open(os.path.join(RESULTS_DIR, "canonical_vs_discovered.json"), "w") as f:
        json.dump({"b1_n10": cmp_b1, "b2_compatibility_family": cmp_b2}, f, indent=2)

    print(f"\nWrote results to {RESULTS_DIR}/")


if __name__ == "__main__":
    main()
