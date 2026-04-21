"""
walk_recovery.py -- Try to recover the canonical sigma partition from T_emp
by walking dynamics on the empirical operator.

Sprint 21 result (signature equality on T_emp[u][.]): partition collapses
to singletons. The full row signature is unique per unit -> no recovery.

Sprint 23 question: do COARSER equivalences -- which still come purely from
T_emp without canonical knowledge -- recover the canonical partition?

Strategies tested:
    W1  multiset of outputs T_emp[u][v] for all v
    W2  set of outputs T_emp[u][v] (image of u-row)
    W3  output frequency profile (histogram of values)
    W4  unary self-trajectory: u_{k+1} = T_emp[u_k][u_k]; cluster by orbit length
    W5  unary self-trajectory: cluster by (orbit length, terminal value)
    W6  fixed-b trajectory: u_{k+1} = T_emp[u_k][1]; cluster by terminal value
    W7  fixed-b trajectory: u_{k+1} = T_emp[u_k][h_hat]; cluster by orbit
    W8  pair commutator: cluster u by sorted tuple of T_emp[u][v] - T_emp[v][u] mod n

For each strategy, compare discovered partition vs canonical partition
(adjusted Rand index = 1.0 means perfect recovery).
"""

import os, sys, json
from collections import Counter, defaultdict
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
SPRINT_DIR = os.path.dirname(HERE)
PAPERS_DIR = os.path.dirname(SPRINT_DIR)
RESULTS_DIR = os.path.join(SPRINT_DIR, "results")

SP21_IMPL = os.path.normpath(os.path.join(
    PAPERS_DIR, "sprint21_structural_discovery_2026_04_17", "impl"))
sys.path.insert(0, SP21_IMPL)
from discovery_fitter import discover  # noqa: E402

B1_DATA = os.path.normpath(os.path.join(
    PAPERS_DIR, "sprint18_b1_nscg_benchmark_2026_04_17", "impl", "data"))
B2_DATA = os.path.normpath(os.path.join(
    PAPERS_DIR, "sprint19_b2_wrg_benchmark_2026_04_17", "impl", "data"))


# ============================================================
# Canonical (used ONLY for after-the-fact comparison)
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
    return [u for u in range(1, n) if gcd(u, n) == 1]


def canonical_partition(n):
    by = defaultdict(list)
    for u in canonical_units(n):
        by[v2(3 * u + 1)].append(u)
    return sorted([sorted(v) for v in by.values()])


# ============================================================
# Partition utilities
# ============================================================

def partition_from_labels(items, labels):
    """labels: dict item -> any hashable; return list-of-lists partition."""
    by = defaultdict(list)
    for i in items:
        by[labels[i]].append(i)
    return sorted([sorted(v) for v in by.values()])


def adjusted_rand(part_a, part_b, universe):
    """Adjusted Rand Index between two partitions on the same universe."""
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
    # Restrict to common universe
    items = [x for x in universe if x in label_a and x in label_b]
    if len(items) < 2:
        return None
    # Contingency
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
# Walk strategies (no canonical priors used to define them)
# ============================================================

def w1_multiset(T, units):
    return {u: tuple(sorted(T[u][v] for v in range(len(T)))) for u in units}


def w2_set(T, units):
    return {u: tuple(sorted(set(T[u][v] for v in range(len(T))))) for u in units}


def w3_freq(T, units):
    return {u: tuple(sorted(Counter(T[u][v] for v in range(len(T))).values()))
            for u in units}


def _orbit(T, start, get_next, max_steps=64):
    seen = []
    seen_set = set()
    cur = start
    while cur not in seen_set and len(seen) < max_steps:
        seen.append(cur)
        seen_set.add(cur)
        cur = get_next(cur)
    return seen, cur  # trajectory + the value that closes the cycle


def w4_self_orbit_len(T, units):
    out = {}
    for u in units:
        orb, term = _orbit(T, u, lambda x: T[x][x])
        out[u] = len(orb)
    return out


def w5_self_orbit(T, units):
    out = {}
    for u in units:
        orb, term = _orbit(T, u, lambda x: T[x][x])
        out[u] = (len(orb), term)
    return out


def w6_fixed_b(T, units, b):
    out = {}
    for u in units:
        orb, term = _orbit(T, u, lambda x: T[x][b])
        out[u] = (len(orb), term)
    return out


def w8_commutator(T, units, n):
    out = {}
    for u in units:
        sig = tuple(sorted((T[u][v] - T[v][u]) % n for v in units))
        out[u] = sig
    return out


# ============================================================
# Run on one source
# ============================================================

def run_source(data_path: str, n: int, label: str, z_T_col: int = 2):
    disc = discover(data_path, n=n, z_T_col=z_T_col)
    T = disc["T_emp"]
    h_hat = disc["h_hat"]
    units_hat = disc["units_hat"]
    canonical = canonical_partition(n)

    # Universe to score on: intersection of canonical units and units_hat
    canon_units = set(canonical_units(n))
    test_universe = sorted(canon_units & set(units_hat))

    strategies = [
        ("W1_multiset",       w1_multiset(T, units_hat)),
        ("W2_set",            w2_set(T, units_hat)),
        ("W3_freq",           w3_freq(T, units_hat)),
        ("W4_self_orbit_len", w4_self_orbit_len(T, units_hat)),
        ("W5_self_orbit",     w5_self_orbit(T, units_hat)),
        ("W6_fixed_b1",       w6_fixed_b(T, units_hat, b=1)),
        ("W6_fixed_b_h",      w6_fixed_b(T, units_hat, b=h_hat)),
        ("W8_commutator",     w8_commutator(T, units_hat, n)),
    ]

    results = {"label": label, "n": n, "h_hat": h_hat,
               "units_hat": units_hat,
               "canonical_partition": canonical,
               "strategies": {}}
    for name, labels in strategies:
        part = partition_from_labels(units_hat, labels)
        ari = adjusted_rand(part, canonical, test_universe)
        results["strategies"][name] = {
            "discovered_partition": part,
            "n_classes": len(part),
            "adjusted_rand_vs_canonical": ari,
            "perfect_recovery":
                (ari == 1.0 if ari is not None else False),
        }
    return results


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    sources = [
        ("nscg_N1000000_p030_s0.csv",  10, B1_DATA, "B1_n10_p030"),
        ("nscg_N100000_p005_s0.csv",   10, B1_DATA, "B1_n10_p005"),
        ("wrg_n14_pw5_s0.csv",         14, B2_DATA, "B2_n14_pw05"),
        ("wrg_n14_pw20_s0.csv",        14, B2_DATA, "B2_n14_pw20"),
        ("wrg_n22_pw5_s0.csv",         22, B2_DATA, "B2_n22_pw05"),
        ("wrg_n22_pw20_s0.csv",        22, B2_DATA, "B2_n22_pw20"),
        ("wrg_n34_pw5_s0.csv",         34, B2_DATA, "B2_n34_pw05"),
        ("wrg_n34_pw20_s0.csv",        34, B2_DATA, "B2_n34_pw20"),
    ]

    all_results = {}
    summary = {"strategies": defaultdict(list)}

    print("=== Sprint 23: curve recovery -- can walks on T_emp recover the canonical sigma partition? ===\n")

    for fn, n, data_dir, label in sources:
        path = os.path.join(data_dir, fn)
        r = run_source(path, n, label)
        all_results[label] = r
        canon = r["canonical_partition"]
        print(f"-- {label}  n={n}  canonical sigma partition: {canon}")
        for sname, sinfo in r["strategies"].items():
            ari = sinfo["adjusted_rand_vs_canonical"]
            ari_str = f"{ari:.3f}" if ari is not None else "N/A"
            star = " <-- PERFECT" if sinfo["perfect_recovery"] else ""
            print(f"    {sname:18s} ARI={ari_str}  "
                  f"n_classes={sinfo['n_classes']}{star}")
            summary["strategies"][sname].append(ari)
        print()

    # Aggregate
    print("=== Cross-source ARI summary (mean) ===")
    agg = {}
    for sname, ari_list in summary["strategies"].items():
        good = [x for x in ari_list if x is not None]
        if not good:
            continue
        mean = sum(good) / len(good)
        n_perfect = sum(1 for x in good if x == 1.0)
        agg[sname] = {
            "mean_ari": round(mean, 4),
            "n_perfect": n_perfect,
            "n_sources": len(good),
        }
        print(f"  {sname:18s} mean ARI = {mean:.3f}  "
              f"perfect on {n_perfect}/{len(good)} sources")

    with open(os.path.join(RESULTS_DIR, "walk_recovery_full.json"), "w") as f:
        json.dump(all_results, f, indent=2)
    with open(os.path.join(RESULTS_DIR, "walk_recovery_summary.json"), "w") as f:
        json.dump(agg, f, indent=2)

    print(f"\nWrote results to {RESULTS_DIR}/")


if __name__ == "__main__":
    main()
