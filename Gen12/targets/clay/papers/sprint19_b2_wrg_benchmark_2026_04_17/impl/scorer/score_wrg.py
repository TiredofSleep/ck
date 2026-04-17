"""
score_wrg.py -- B2 Wobble-Reset scorer.

For each of 24 configs, compute the four B2-spec recoveries:

    A_h         = 1.0 if h_hat == h_true else 0.0
    A_sigma     = 1.0 if sigma_hat == sigma_true (on units) else 0.0
    A_reset     = F1 score of reset_edges_hat vs reset_edges_true
                  (precision = |hat AND true| / |hat|,
                   recall    = |hat AND true| / |true|,
                   F1 = harmonic mean)
                  -- restricted to "observable" resets (cells where C_0 != h)
    A_B         = transport_op_match (fraction of (x,y) where
                  B_emp[x][y] == (x+y) mod n)

Per-config pass:
    p_w = 0.05  -> all four >= 0.90
    p_w = 0.20  -> all four >= 0.80

Aggregate verdict:
    Per (n, p_w): pass-rate across seeds
    Overall: PASS if all 24 configs pass; otherwise FAIL with diagnosis

Outputs:
    scores/per_config/<config>.score.json   (24 files)
    scores/B2_summary.json
    B2_RESULTS.md  (auto-generated report)

Verifies data + sealed hashes against manifest before scoring.
"""

import os, sys, json, hashlib, csv, argparse
from math import gcd
from typing import Dict, List, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
SEALED_DIR = os.path.join(ROOT, "sealed")
MANIFEST_DIR = os.path.join(ROOT, "manifest")
RESULTS_DIR = os.path.join(ROOT, "results")
SCORES_DIR = os.path.join(ROOT, "scores")
PER_CONFIG_DIR = os.path.join(SCORES_DIR, "per_config")
SPRINT_ROOT = os.path.dirname(ROOT)


def v2(k):
    if k == 0:
        return 0
    n = 0
    while k % 2 == 0:
        k //= 2
        n += 1
    return n


def units(n):
    return [u for u in range(1, n) if gcd(u, n) == 1]


def core_set(n):
    return [u for u in units(n) if u != 1]


def C0(x, y, n, h, sigma, core):
    if x == 0 or y == 0:
        if (x, y) == (0, h) or (x, y) == (h, 0):
            return h
        return 0
    if x in core and y in core and sigma.get(x) != sigma.get(y):
        return x if sigma[x] < sigma[y] else y
    return h


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_hashes():
    """Check data + sealed files against manifest. Raises on mismatch."""
    with open(os.path.join(MANIFEST_DIR, "data_hashes.json")) as f:
        data_h = json.load(f)
    with open(os.path.join(MANIFEST_DIR, "sealed_hashes.json")) as f:
        sealed_h = json.load(f)
    for name, expected in data_h.items():
        actual = sha256_file(os.path.join(DATA_DIR, name))
        if actual != expected:
            raise RuntimeError(f"data hash mismatch: {name}")
    for name, expected in sealed_h.items():
        actual = sha256_file(os.path.join(SEALED_DIR, name))
        if actual != expected:
            raise RuntimeError(f"sealed hash mismatch: {name}")
    return len(data_h), len(sealed_h)


def f1_score(hat: List[Tuple[int, int]],
             true: List[Tuple[int, int]]) -> Dict[str, float]:
    """Compute precision, recall, F1 for two sets of ordered pairs."""
    hat_set = set(tuple(p) for p in hat)
    true_set = set(tuple(p) for p in true)
    if not hat_set and not true_set:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0,
                "tp": 0, "fp": 0, "fn": 0}
    tp = len(hat_set & true_set)
    fp = len(hat_set - true_set)
    fn = len(true_set - hat_set)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return {"precision": precision, "recall": recall, "f1": f1,
            "tp": tp, "fp": fp, "fn": fn}


def observable_resets(reset_edges: List[Tuple[int, int]], n: int,
                      h: int, sigma: Dict[int, int],
                      core: List[int]) -> List[Tuple[int, int]]:
    """Filter reset_edges to only those where C_0(x,y) != h (observable)."""
    return [(x, y) for x, y in reset_edges
            if C0(x, y, n, h, sigma, core) != h]


def per_config(truth_path: str, fit_path: str) -> Dict:
    with open(truth_path) as f:
        truth = json.load(f)
    with open(fit_path) as f:
        fit = json.load(f)

    n = truth["n"]
    p_w = truth["p_wobble"]
    seed = truth["seed"]
    h_true = truth["h_true"]
    sigma_true = {int(k): v for k, v in truth["sigma_true"].items()}
    core_true = truth["core_true"]
    reset_true = [tuple(p) for p in truth["reset_edges"]]

    # Filter reset_true to observable (those where C_0 != h)
    reset_true_obs = observable_resets(reset_true, n, h_true, sigma_true,
                                       core_true)

    # A_h
    A_h = 1.0 if fit["h_hat"] == h_true else 0.0

    # A_sigma: compare sigma_hat to sigma_true on units
    sigma_hat = {int(k): v for k, v in fit["sigma_hat"].items()}
    units_true = sorted(sigma_true.keys())
    sigma_match = all(sigma_hat.get(u) == sigma_true.get(u)
                      for u in units_true)
    A_sigma = 1.0 if sigma_match else 0.0

    # A_reset: F1 of reset_edges_hat vs observable reset_true
    reset_hat = [tuple(p) for p in fit["reset_edges_hat"]]
    reset_metrics = f1_score(reset_hat, reset_true_obs)
    A_reset = reset_metrics["f1"]

    # A_B
    A_B = fit["transport_op_match"]

    threshold = 0.90 if p_w == 0.05 else 0.80
    pass_per_metric = {
        "A_h":     A_h     >= threshold,
        "A_sigma": A_sigma >= threshold,
        "A_reset": A_reset >= threshold,
        "A_B":     A_B     >= threshold,
    }
    config_pass = all(pass_per_metric.values())

    return {
        "n": n,
        "p_wobble": p_w,
        "seed": seed,
        "threshold": threshold,
        "metrics": {
            "A_h":     A_h,
            "A_sigma": A_sigma,
            "A_reset": A_reset,
            "A_B":     A_B,
        },
        "reset_detail": reset_metrics,
        "reset_true_observable": [list(p) for p in reset_true_obs],
        "reset_hat":              [list(p) for p in reset_hat],
        "pass_per_metric": pass_per_metric,
        "config_pass": config_pass,
    }


def main():
    parser = argparse.ArgumentParser(description="B2 WRG scorer")
    parser.add_argument("--skip-hash-check", action="store_true")
    args = parser.parse_args()

    if not args.skip_hash_check:
        nd, ns = verify_hashes()
        print(f"hash verification: {nd} data + {ns} sealed OK")

    os.makedirs(PER_CONFIG_DIR, exist_ok=True)

    truths = sorted([f for f in os.listdir(SEALED_DIR)
                     if f.startswith("truth_n") and f.endswith(".json")])
    all_results = []
    for t in truths:
        # truth_n10_pw5_s0.json -> wrg_n10_pw5_s0.fit.json
        config_id = t.replace("truth_", "wrg_").replace(".json", "")
        fit_path = os.path.join(RESULTS_DIR, f"{config_id}.fit.json")
        if not os.path.exists(fit_path):
            print(f"  SKIP: missing fit for {config_id}")
            continue
        result = per_config(os.path.join(SEALED_DIR, t), fit_path)
        with open(os.path.join(PER_CONFIG_DIR, f"{config_id}.score.json"), "w") as f:
            json.dump(result, f, indent=2)
        all_results.append(result)
        flag = "PASS" if result["config_pass"] else "FAIL"
        m = result["metrics"]
        print(f"  {config_id:30s}  A_h={m['A_h']:.3f}  "
              f"A_sigma={m['A_sigma']:.3f}  A_reset={m['A_reset']:.3f}  "
              f"A_B={m['A_B']:.3f}  -> {flag}")

    # Aggregate
    total = len(all_results)
    passes = sum(1 for r in all_results if r["config_pass"])
    by_carrier_wobble = {}
    for r in all_results:
        key = f"n={r['n']}_pw={r['p_wobble']}"
        by_carrier_wobble.setdefault(key, {"total": 0, "pass": 0})
        by_carrier_wobble[key]["total"] += 1
        if r["config_pass"]:
            by_carrier_wobble[key]["pass"] += 1

    summary = {
        "spec_version": "B2-v1.0 per SHELL_NATIVE_BENCHMARKS.md",
        "total_configs": total,
        "passes": passes,
        "verdict": "PASS" if passes == total else "FAIL",
        "by_carrier_wobble": by_carrier_wobble,
        "per_carrier_metric_means": {},
    }

    # Mean of each metric per carrier across all wobble + seeds
    for n in sorted(set(r["n"] for r in all_results)):
        rows = [r for r in all_results if r["n"] == n]
        means = {}
        for k in ["A_h", "A_sigma", "A_reset", "A_B"]:
            means[k] = sum(r["metrics"][k] for r in rows) / len(rows)
        summary["per_carrier_metric_means"][f"n={n}"] = means

    with open(os.path.join(SCORES_DIR, "B2_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nB2 verdict: {summary['verdict']}  ({passes}/{total} configs pass)")

    # Auto-write the markdown report
    write_report(summary, all_results)


def write_report(summary: Dict, all_results: List[Dict]):
    out = os.path.join(SPRINT_ROOT, "B2_RESULTS.md")
    lines = []
    lines.append("# B2 Wobble-Reset Generator -- Results\n")
    lines.append(f"**Spec:** {summary['spec_version']}")
    lines.append(f"**Configs:** {summary['total_configs']} "
                 f"(4 carriers x 2 wobble x 3 seeds)")
    lines.append(f"**Overall verdict:** **{summary['verdict']}**  "
                 f"({summary['passes']}/{summary['total_configs']} pass)\n")
    lines.append("---\n")

    lines.append("## Per-carrier metric means\n")
    lines.append("| Carrier | A_h | A_sigma | A_reset | A_B |")
    lines.append("|---|---|---|---|---|")
    for k, m in summary["per_carrier_metric_means"].items():
        lines.append(f"| {k} | {m['A_h']:.4f} | {m['A_sigma']:.4f} "
                     f"| {m['A_reset']:.4f} | {m['A_B']:.4f} |")
    lines.append("")

    lines.append("## Pass-rate per (carrier, wobble)\n")
    lines.append("| Group | Pass / Total |")
    lines.append("|---|---|")
    for k, v in sorted(summary["by_carrier_wobble"].items()):
        lines.append(f"| {k} | {v['pass']} / {v['total']} |")
    lines.append("")

    lines.append("## Per-config detail\n")
    lines.append("| Config | A_h | A_sigma | A_reset | A_B | Verdict |")
    lines.append("|---|---|---|---|---|---|")
    for r in all_results:
        cid = f"n={r['n']} pw={r['p_wobble']} s={r['seed']}"
        m = r["metrics"]
        verdict = "PASS" if r["config_pass"] else "FAIL"
        lines.append(f"| {cid} | {m['A_h']:.3f} | {m['A_sigma']:.3f} "
                     f"| {m['A_reset']:.3f} | {m['A_B']:.3f} | {verdict} |")
    lines.append("")

    lines.append("## Reset-edge detail (observable resets only)\n")
    for r in all_results[:6]:  # first few configs as worked examples
        cid = f"n={r['n']} pw={r['p_wobble']} s={r['seed']}"
        lines.append(f"**{cid}**: true={r['reset_true_observable']}  "
                     f"hat={r['reset_hat']}  "
                     f"tp={r['reset_detail']['tp']} fp={r['reset_detail']['fp']} "
                     f"fn={r['reset_detail']['fn']}\n")

    with open(out, "w") as f:
        f.write("\n".join(lines))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
