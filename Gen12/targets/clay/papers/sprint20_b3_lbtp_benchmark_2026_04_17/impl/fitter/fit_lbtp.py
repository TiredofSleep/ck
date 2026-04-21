"""
fit_lbtp.py -- B3 LBTP fitter. Fits three models on the same data:

  T_only:   for each (x,y), predict z_T as mode of z_T at (x,y); ignores z_B
  B_only:   for each (x,y), predict z_B as mode of z_B at (x,y); ignores z_T
  Paired:   for each (x,y), predict (z_T, z_B) as the joint mode of the
            pair, using cross-stream consistency to break ties

Train on the first 80% of samples, test on the last 20% (held-out).
Compute prediction accuracy on the held-out set:

  acc_T(model)  = fraction of held-out where model predicts z_T correctly
  acc_B(model)  = fraction of held-out where model predicts z_B correctly
  acc_joint     = fraction where BOTH correct (paired-model only is meaningful)

Spec discrimination criterion: paired must outperform max(T_only, B_only)
by >= 5 percentage points on prediction accuracy.

We compute three figures of merit so the comparison is unambiguous:
  paired vs T_only on z_T accuracy
  paired vs B_only on z_B accuracy
  paired joint accuracy (single number)

Usage:
    python fitter/fit_lbtp.py --data data/lbtp_s0.csv --output results/lbtp_s0.fit.json
"""

import os, json, csv, argparse
from collections import Counter, defaultdict
from typing import Dict, List, Tuple

N_CARRIER = 10


def mode_with_smallest_z_tiebreak(c: Counter) -> int:
    if not c:
        return -1
    max_count = max(c.values())
    return min(z for z, cnt in c.items() if cnt == max_count)


def fit(data_path: str, output_path: str = None, train_frac: float = 0.8) -> Dict:
    rows = []
    with open(data_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append((int(row[0]), int(row[1]), int(row[2]), int(row[3])))

    N = len(rows)
    n_train = int(N * train_frac)
    train, test = rows[:n_train], rows[n_train:]

    # Per-cell counts on training set
    counts_T = [[Counter() for _ in range(N_CARRIER)] for _ in range(N_CARRIER)]
    counts_B = [[Counter() for _ in range(N_CARRIER)] for _ in range(N_CARRIER)]
    counts_joint = [[Counter() for _ in range(N_CARRIER)] for _ in range(N_CARRIER)]

    for x, y, zT, zB in train:
        counts_T[x][y][zT] += 1
        counts_B[x][y][zB] += 1
        counts_joint[x][y][(zT, zB)] += 1

    # Build prediction tables
    pred_T_only = [[mode_with_smallest_z_tiebreak(counts_T[x][y])
                    for y in range(N_CARRIER)] for x in range(N_CARRIER)]
    pred_B_only = [[mode_with_smallest_z_tiebreak(counts_B[x][y])
                    for y in range(N_CARRIER)] for x in range(N_CARRIER)]

    def joint_mode(c: Counter) -> Tuple[int, int]:
        if not c:
            return (-1, -1)
        max_count = max(c.values())
        # tie-break: smallest (zT, zB) lexicographic
        return min(pair for pair, cnt in c.items() if cnt == max_count)

    pred_paired = [[joint_mode(counts_joint[x][y])
                    for y in range(N_CARRIER)] for x in range(N_CARRIER)]

    # Held-out evaluation
    acc_T_from_T_only, acc_T_from_paired = 0, 0
    acc_B_from_B_only, acc_B_from_paired = 0, 0
    acc_joint_paired = 0

    for x, y, zT, zB in test:
        if pred_T_only[x][y] == zT:
            acc_T_from_T_only += 1
        if pred_B_only[x][y] == zB:
            acc_B_from_B_only += 1
        pT, pB = pred_paired[x][y]
        if pT == zT:
            acc_T_from_paired += 1
        if pB == zB:
            acc_B_from_paired += 1
        if pT == zT and pB == zB:
            acc_joint_paired += 1

    n_test = len(test)
    metrics = {
        "n_train": n_train,
        "n_test": n_test,
        "acc_T_from_T_only":  round(acc_T_from_T_only / n_test, 6),
        "acc_T_from_paired":  round(acc_T_from_paired / n_test, 6),
        "acc_B_from_B_only":  round(acc_B_from_B_only / n_test, 6),
        "acc_B_from_paired":  round(acc_B_from_paired / n_test, 6),
        "acc_joint_paired":   round(acc_joint_paired / n_test, 6),
    }

    # Spec criterion: paired prediction accuracy > max(T-only, B-only) + 5pp
    # Interpret "paired prediction accuracy" as joint accuracy
    paired_vs_max_singleton = (
        metrics["acc_joint_paired"] -
        max(metrics["acc_T_from_T_only"], metrics["acc_B_from_B_only"])
    )
    metrics["paired_minus_max_singleton_pp"] = round(
        paired_vs_max_singleton * 100, 4)
    metrics["spec_paired_outperforms_by_5pp"] = paired_vs_max_singleton >= 0.05

    # Recovery accuracy (training-set match against truth would require sealed;
    # here we just emit the predicted tables)
    result = {
        "data_file": os.path.basename(data_path),
        "T_predicted": pred_T_only,
        "B_predicted": pred_B_only,
        "paired_predicted": [[list(p) for p in row] for row in pred_paired],
        "metrics": metrics,
    }

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = fit(args.data, args.output)
    m = result["metrics"]
    print(f"  {os.path.basename(args.data):20s}  "
          f"T_only={m['acc_T_from_T_only']:.4f}  "
          f"B_only={m['acc_B_from_B_only']:.4f}  "
          f"joint={m['acc_joint_paired']:.4f}  "
          f"paired-max(singleton)={m['paired_minus_max_singleton_pp']:+.2f}pp")


if __name__ == "__main__":
    main()
