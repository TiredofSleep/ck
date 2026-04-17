"""
nstress.py -- N-stress: subsample B1 and B2 datasets at decreasing N
and watch which structural invariants break first.

The 6 invariants we tracked in Sprint 21 (all 100% stable at N >= 100k):
    I1: h_hat correct
    I2: image_T closure stable
    I3: corridor menu closure (only MAX/MIN/ADD)
    I4: discovered units = canonical \\ {1, h}
    I5: discovered core = canonical \\ {h}-residue (the 'image \\ {0, h}')
    I6: partition = singletons (signature uniqueness)

If we drop N to 50, 100, 500, ... when does each invariant first fail?
That failure pattern IS the collapse signature.
"""

import os, sys, json, csv, random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SPRINT_DIR = os.path.dirname(HERE)
PAPERS_DIR = os.path.dirname(SPRINT_DIR)
RESULTS_DIR = os.path.join(SPRINT_DIR, "results")

# Reuse the prior-free fitter from Sprint 21
SP21_IMPL = os.path.normpath(os.path.join(
    PAPERS_DIR, "sprint21_structural_discovery_2026_04_17", "impl"))
sys.path.insert(0, SP21_IMPL)
from discovery_fitter import discover, fingerprint  # noqa: E402

B1_DATA = os.path.normpath(os.path.join(
    PAPERS_DIR, "sprint18_b1_nscg_benchmark_2026_04_17", "impl", "data"))
B2_DATA = os.path.normpath(os.path.join(
    PAPERS_DIR, "sprint19_b2_wrg_benchmark_2026_04_17", "impl", "data"))


N_TARGETS = [25, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000]


def subsample_csv(src_path: str, dst_path: str, n_rows: int, seed: int):
    """Take the first n_rows after a deterministic seed-shuffle of
    the source CSV (header preserved)."""
    with open(src_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    rng = random.Random(seed)
    rng.shuffle(rows)
    rows = rows[:n_rows]
    with open(dst_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def reference_fingerprint(data_dir: str, sample_file: str, n: int,
                          z_T_col: int = 2):
    """Use the full-N discovery as the reference invariant set."""
    full = discover(os.path.join(data_dir, sample_file), n=n,
                    z_T_col=z_T_col)
    return fingerprint(full), full


def diff_invariants(ref_fp, test_fp):
    """Which of the comparable fields differ?"""
    fields = ["h_hat", "image_T", "core_outputs", "units_hat",
              "partition_hat", "seam_cell_count", "seam_by_rule_counts"]
    diffs = {}
    for f in fields:
        diffs[f] = (ref_fp[f] != test_fp[f])
    return diffs


def stress_one_source(src_path: str, n: int, ref_fp, label: str,
                      tmp_root: str, z_T_col: int = 2):
    """For one CSV, run discovery at each N_target with multiple subsamples."""
    rows = []
    for N in N_TARGETS:
        for seed in range(3):  # 3 subsamples per N
            tmp = os.path.join(tmp_root, f"sub_N{N}_s{seed}.csv")
            subsample_csv(src_path, tmp, N, seed=seed * 7 + 1)
            disc = discover(tmp, n=n, z_T_col=z_T_col)
            fp = fingerprint(disc)
            d = diff_invariants(ref_fp, fp)
            rows.append({
                "source": label,
                "N": N,
                "subsample_seed": seed,
                "fp": fp,
                "diffs_vs_ref": d,
                "n_diffs": sum(1 for v in d.values() if v),
            })
            os.remove(tmp)
    return rows


def collapse_threshold(rows, field):
    """Smallest N at which 'field' is correct in all 3 subsamples."""
    by_N = defaultdict(list)
    for r in rows:
        by_N[r["N"]].append(r["diffs_vs_ref"][field])
    for N in sorted(by_N.keys()):
        if not any(by_N[N]):
            return N
    return None


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    tmp_root = os.path.join(HERE, "_tmp_subsamples")
    os.makedirs(tmp_root, exist_ok=True)

    summary = {}
    all_runs = {}

    # ====== B1 stress (n=10) ======
    print("=== B1 N-stress (n=10) ===")
    sources_b1 = [
        ("nscg_N1000000_p030_s0.csv", 0.30, B1_DATA),
        ("nscg_N100000_p005_s0.csv",  0.05, B1_DATA),
        ("nscg_N500000_p015_s0.csv",  0.15, B1_DATA),
    ]
    for fn, pn, data_dir in sources_b1:
        ref_fp, _ = reference_fingerprint(data_dir, fn, n=10)
        label = f"B1_p{int(pn*100):03d}"
        print(f"  source: {fn}  noise={pn}  ref={label}")
        rows = stress_one_source(os.path.join(data_dir, fn), 10, ref_fp,
                                 label, tmp_root)
        all_runs[label] = {"reference_fingerprint": ref_fp, "stress": rows}
        per_field = {}
        for field in ["h_hat", "image_T", "core_outputs", "units_hat",
                      "partition_hat", "seam_cell_count",
                      "seam_by_rule_counts"]:
            per_field[field] = collapse_threshold(rows, field)
        summary[label] = {
            "noise": pn,
            "first_correct_N": per_field,
        }
        for fld, n_first in per_field.items():
            tag = f"N>={n_first}" if n_first is not None else "never (>50k)"
            print(f"    {fld:25s} stable at {tag}")

    # ====== B2 stress (n in {10,14,22,34}) ======
    print("\n=== B2 N-stress ===")
    sources_b2 = [
        ("wrg_n10_pw5_s0.csv",  10, 0.05),
        ("wrg_n10_pw20_s0.csv", 10, 0.20),
        ("wrg_n14_pw5_s0.csv",  14, 0.05),
        ("wrg_n14_pw20_s0.csv", 14, 0.20),
        ("wrg_n22_pw5_s0.csv",  22, 0.05),
        ("wrg_n22_pw20_s0.csv", 22, 0.20),
        ("wrg_n34_pw5_s0.csv",  34, 0.05),
        ("wrg_n34_pw20_s0.csv", 34, 0.20),
    ]
    for fn, n, pw in sources_b2:
        ref_fp, _ = reference_fingerprint(B2_DATA, fn, n=n)
        label = f"B2_n{n}_pw{int(pw*100):02d}"
        print(f"  source: {fn}  carrier=n{n}  wobble={pw}")
        rows = stress_one_source(os.path.join(B2_DATA, fn), n, ref_fp,
                                 label, tmp_root)
        all_runs[label] = {"reference_fingerprint": ref_fp, "stress": rows}
        per_field = {}
        for field in ["h_hat", "image_T", "core_outputs", "units_hat",
                      "partition_hat", "seam_cell_count",
                      "seam_by_rule_counts"]:
            per_field[field] = collapse_threshold(rows, field)
        summary[label] = {
            "carrier_n": n,
            "wobble": pw,
            "first_correct_N": per_field,
        }
        for fld, n_first in per_field.items():
            tag = f"N>={n_first}" if n_first is not None else "never (>50k)"
            print(f"    {fld:25s} stable at {tag}")

    with open(os.path.join(RESULTS_DIR, "nstress_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    with open(os.path.join(RESULTS_DIR, "nstress_full.json"), "w") as f:
        json.dump(all_runs, f, indent=2)

    # ====== Cross-source synthesis ======
    print("\n=== Collapse signature: smallest stable N per invariant ===")
    print("(median across all sources)")
    fields = ["h_hat", "image_T", "core_outputs", "units_hat",
              "partition_hat", "seam_cell_count", "seam_by_rule_counts"]
    for field in fields:
        vals = [s["first_correct_N"][field] for s in summary.values()
                if s["first_correct_N"][field] is not None]
        if not vals:
            print(f"  {field:25s} NEVER stable in tested range")
            continue
        median = sorted(vals)[len(vals) // 2]
        print(f"  {field:25s} median first-stable N = {median}  "
              f"(min={min(vals)}, max={max(vals)})")

    # Cleanup tmp dir
    try:
        os.rmdir(tmp_root)
    except OSError:
        pass

    print(f"\nWrote results to {RESULTS_DIR}/")


if __name__ == "__main__":
    main()
