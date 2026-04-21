"""
ari_scaling.py -- Sprint 26: Asymptotic ARI scan.

Sprint 23 finding: W3 freq (output histogram) partially recovers the
canonical sigma partition with ARI growing in n:
    n=10 -> -0.500    n=14 -> 0.000    n=22 -> 0.263    n=34 -> 0.728

Sprint 26 question: at higher n, does ARI -> 1.0 (full recovery in the
asymptotic limit), or does it saturate below 1?

We use the analytic C_0 directly (no data generation needed) since
Sprint 25 proved C_0 is exhaustively constructible. The T matrix is
computed from C_0; W3-freq cluster is built from T. ARI is measured
against canonical sigma partition.

Test n in the full extended carrier set up to n=230.
"""

import os, sys, json
from collections import Counter, defaultdict
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
SPRINT_DIR = os.path.dirname(HERE)
PAPERS_DIR = os.path.dirname(SPRINT_DIR)
RESULTS_DIR = os.path.join(SPRINT_DIR, "results")

# Reuse canonical from sprint 25 proof
SP25_IMPL = os.path.normpath(os.path.join(
    PAPERS_DIR, "sprint25_corridor_closure_proof_2026_04_17", "impl"))
sys.path.insert(0, SP25_IMPL)
from prove_corridor_closure import (  # noqa: E402
    units, sigma_map, core_set, attractor_h, C0)


# ============================================================
# Partition + ARI utilities (from sprint 23)
# ============================================================

def canonical_partition(n):
    sig = sigma_map(n)
    by = defaultdict(list)
    for u, s in sig.items():
        by[s].append(u)
    return sorted([sorted(v) for v in by.values()])


def partition_from_labels(items, labels):
    by = defaultdict(list)
    for i in items:
        by[labels[i]].append(i)
    return sorted([sorted(v) for v in by.values()])


def adjusted_rand(part_a, part_b, universe):
    if not universe:
        return None
    label_a = {}
    for i, cls in enumerate(part_a):
        for x in cls:
            label_a[x] = i
    label_b = {}
    for i, cls in enumerate(part_b):
        for x in cls:
            label_b[x] = i
    items = [x for x in universe if x in label_a and x in label_b]
    if len(items) < 2:
        return None
    cont = defaultdict(int)
    for x in items:
        cont[(label_a[x], label_b[x])] += 1
    a_marg = Counter(label_a[x] for x in items)
    b_marg = Counter(label_b[x] for x in items)

    def comb2(k):
        return k * (k - 1) // 2

    n = len(items)
    sum_cont = sum(comb2(v) for v in cont.values())
    sum_a = sum(comb2(v) for v in a_marg.values())
    sum_b = sum(comb2(v) for v in b_marg.values())
    expected = sum_a * sum_b / comb2(n) if comb2(n) > 0 else 0
    max_idx = 0.5 * (sum_a + sum_b)
    if max_idx == expected:
        return 1.0 if sum_cont == expected else 0.0
    return (sum_cont - expected) / (max_idx - expected)


# ============================================================
# Compute T_emp = C_0 analytically, then run W3-freq partition
# ============================================================

def t_matrix(n):
    h = attractor_h(n)
    if h is None:
        return None, None, None, None
    sigma = sigma_map(n)
    core = core_set(n)
    T = [[C0(x, y, n, h, sigma, core) for y in range(n)] for x in range(n)]
    return T, h, sigma, core


def discovery_units(T, h):
    """units_hat = inputs participating in seam cells (cells with output
    in image \\ {0, h})."""
    n = len(T)
    flat = [v for row in T for v in row]
    image_T = sorted(set(flat))
    core_outputs = set(v for v in image_T if v != 0 and v != h)
    units_in = set()
    for x in range(n):
        for y in range(n):
            if T[x][y] in core_outputs:
                units_in.add(x)
                units_in.add(y)
    return sorted(units_in)


def w3_freq_labels(T, units_hat):
    """Label each unit by its sorted output frequency profile."""
    return {u: tuple(sorted(Counter(T[u][v] for v in range(len(T))).values()))
            for u in units_hat}


def w1_multiset_labels(T, units_hat):
    return {u: tuple(sorted(T[u][v] for v in range(len(T)))) for u in units_hat}


def w2_set_labels(T, units_hat):
    return {u: tuple(sorted(set(T[u][v] for v in range(len(T)))))
            for u in units_hat}


# ============================================================
# Sweep
# ============================================================

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    CARRIERS = [10, 14, 22, 34, 38, 46, 50, 58, 62, 70, 74, 82, 94,
                106, 110, 118, 122, 130, 134, 142, 158, 166, 170, 178,
                190, 194, 202, 206, 214, 218, 226, 230]

    print(f"Sprint 26: ARI scaling on canonical T_emp = C_0\n")
    print(f"{'n':>4}  {'h':>4}  {'units':>5}  {'canon_classes':>13}  "
          f"{'ARI_W1':>8}  {'ARI_W2':>8}  {'ARI_W3':>8}")

    rows = []
    for n in CARRIERS:
        T, h, sigma, core = t_matrix(n)
        if T is None:
            continue
        units_hat = discovery_units(T, h)
        canonical = canonical_partition(n)
        canon_units = set(units(n))
        test_universe = sorted(canon_units & set(units_hat))

        labels_w1 = w1_multiset_labels(T, units_hat)
        labels_w2 = w2_set_labels(T, units_hat)
        labels_w3 = w3_freq_labels(T, units_hat)

        part_w1 = partition_from_labels(units_hat, labels_w1)
        part_w2 = partition_from_labels(units_hat, labels_w2)
        part_w3 = partition_from_labels(units_hat, labels_w3)

        ari_w1 = adjusted_rand(part_w1, canonical, test_universe)
        ari_w2 = adjusted_rand(part_w2, canonical, test_universe)
        ari_w3 = adjusted_rand(part_w3, canonical, test_universe)

        rows.append({
            "n": n, "h": h,
            "n_canonical_units": len(units(n)),
            "n_units_hat": len(units_hat),
            "n_canonical_classes": len(canonical),
            "n_w3_classes": len(part_w3),
            "ari_w1_multiset": ari_w1,
            "ari_w2_set": ari_w2,
            "ari_w3_freq": ari_w3,
        })

        def fmt(x):
            return f"{x:.4f}" if x is not None else "  N/A "

        print(f"{n:4d}  {h:4d}  {len(units_hat):5d}  "
              f"{len(canonical):13d}  {fmt(ari_w1):>8}  "
              f"{fmt(ari_w2):>8}  {fmt(ari_w3):>8}")

    # Aggregate
    summary = {
        "carriers": [r["n"] for r in rows],
        "ari_w1_by_n": {r["n"]: r["ari_w1_multiset"] for r in rows},
        "ari_w2_by_n": {r["n"]: r["ari_w2_set"] for r in rows},
        "ari_w3_by_n": {r["n"]: r["ari_w3_freq"] for r in rows},
    }

    # Best W3 ARI achieved
    w3_vals = [r["ari_w3_freq"] for r in rows
               if r["ari_w3_freq"] is not None]
    if w3_vals:
        max_w3 = max(w3_vals)
        max_w3_n = next(r["n"] for r in rows if r["ari_w3_freq"] == max_w3)
        summary["max_ari_w3"] = round(max_w3, 4)
        summary["max_ari_w3_at_n"] = max_w3_n
        n_perfect = sum(1 for v in w3_vals if v == 1.0)
        summary["w3_perfect_recoveries"] = n_perfect
        print(f"\nMax W3 ARI = {max_w3:.4f} at n={max_w3_n}")
        print(f"W3 perfect (ARI=1.0): {n_perfect} / {len(w3_vals)}")

    # Trend
    print(f"\nTrend (W3 ARI as a function of n):")
    monotonic = True
    prev = -2.0
    last_increase_n = None
    for r in rows:
        if r["ari_w3_freq"] is None:
            continue
        if r["ari_w3_freq"] >= prev:
            last_increase_n = r["n"]
        else:
            monotonic = False
        prev = r["ari_w3_freq"]
    summary["w3_monotonic"] = monotonic
    summary["w3_last_increase_at_n"] = last_increase_n

    if monotonic:
        print(f"  W3 ARI is monotonic non-decreasing in n.")
    else:
        print(f"  W3 ARI is NOT monotonic.")

    with open(os.path.join(RESULTS_DIR, "ari_scaling.json"), "w") as f:
        json.dump({"per_n": rows, "summary": summary}, f, indent=2)

    print(f"\nWrote results to {RESULTS_DIR}/")


if __name__ == "__main__":
    main()
