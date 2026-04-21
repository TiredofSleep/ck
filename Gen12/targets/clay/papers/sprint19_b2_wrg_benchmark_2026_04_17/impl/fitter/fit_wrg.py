"""
fit_wrg.py -- B2 Wobble-Reset fitter.

The instrument under test. For one CSV at a time, recovers:

    h_hat        -- attractor (mode of all z_T values)
    sigma_hat    -- shell partition on units (computed from canonical formula)
    units_hat    -- units of Z/nZ (computed from gcd)
    core_hat     -- core = units \\ {1}
    reset_edges_hat -- cells where mode(z_T) = h_hat but C_0(x,y) != h_hat
    transport_op_match -- fraction of (x,y) where mode(z_B) == (x+y) mod n
    T_hat_matrix -- per-cell mode-recovered operator (n x n)
    B_hat_matrix -- per-cell mode-recovered transport (n x n)

Allowed knowledge per spec §B2 (mirrors B1 §7):
    - Carrier size n (from CSV filename or sealed only via N -- here we
      take it from the filename to avoid reading sealed)
    - Canonical formulas: gcd, v_2, units(n) = {u : gcd(u,n)=1},
      sigma(u) = v_2(3u+1), C_0 construction
    - General "fit a discrete operator from triples by mode" algorithm

Forbidden:
    - Reading sealed/*.json
    - Reading reset_edges from any source other than the data
    - Reading transport_op_match from any source other than the data

Usage:
    python fitter/fit_wrg.py --data data/wrg_n14_pw20_s0.csv \\
        --output results/wrg_n14_pw20_s0.fit.json
"""

import os, json, csv, argparse, re
from math import gcd
from collections import Counter
from typing import Dict, List, Tuple


def v2(k: int) -> int:
    if k == 0:
        return 0
    n = 0
    while k % 2 == 0:
        k //= 2
        n += 1
    return n


def units(n: int) -> List[int]:
    return [u for u in range(1, n) if gcd(u, n) == 1]


def sigma_map(n: int) -> Dict[int, int]:
    return {u: v2(3 * u + 1) for u in units(n)}


def core_set(n: int) -> List[int]:
    return [u for u in units(n) if u != 1]


def C0(x: int, y: int, n: int, h: int, sigma: Dict[int, int],
       core: List[int]) -> int:
    if x == 0 or y == 0:
        if (x, y) == (0, h) or (x, y) == (h, 0):
            return h
        return 0
    if x in core and y in core and sigma.get(x) != sigma.get(y):
        return x if sigma[x] < sigma[y] else y
    return h


def carrier_from_path(path: str) -> int:
    """Extract n from filename like wrg_n14_pw20_s0.csv."""
    m = re.search(r"_n(\d+)_", os.path.basename(path))
    if not m:
        raise ValueError(f"cannot extract carrier n from {path}")
    return int(m.group(1))


def empirical_modes(data_path: str, n: int) -> Tuple[List[List[int]],
                                                     List[List[int]]]:
    """
    Return (T_emp, B_emp) as n x n matrices of mode-recovered z values.

    Tie-break: smallest z value wins (deterministic).
    Cells with no observations: -1 (should not happen at our N values).
    """
    counts_T = [[Counter() for _ in range(n)] for _ in range(n)]
    counts_B = [[Counter() for _ in range(n)] for _ in range(n)]

    with open(data_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            x, y, z_T, z_B = int(row[0]), int(row[1]), int(row[2]), int(row[3])
            counts_T[x][y][z_T] += 1
            counts_B[x][y][z_B] += 1

    def mode_with_smallest_z_tiebreak(c: Counter) -> int:
        if not c:
            return -1
        max_count = max(c.values())
        return min(z for z, cnt in c.items() if cnt == max_count)

    T_emp = [[mode_with_smallest_z_tiebreak(counts_T[x][y]) for y in range(n)]
             for x in range(n)]
    B_emp = [[mode_with_smallest_z_tiebreak(counts_B[x][y]) for y in range(n)]
             for x in range(n)]
    return T_emp, B_emp


def fit(data_path: str, output_path: str = None) -> Dict:
    n = carrier_from_path(data_path)
    units_list = units(n)
    sigma = sigma_map(n)
    core = core_set(n)

    # Recover empirical mode operators
    T_emp, B_emp = empirical_modes(data_path, n)

    # h_hat: mode of all entries in T_emp
    flat = [v for row in T_emp for v in row if v >= 0]
    h_counter = Counter(flat)
    max_count = max(h_counter.values())
    h_hat = min(z for z, cnt in h_counter.items() if cnt == max_count)

    # Reset edges: cells where T_emp[x][y] != C_0(x,y;h_hat,sigma,core)
    # AND T_emp[x][y] == h_hat (i.e., the cell collapsed to attractor)
    # Wobble cells around the canonical also produce deviations -- but their
    # mode survives at the canonical value (wobble is symmetric and minority).
    reset_edges_hat = []
    deviations = []
    for x in range(n):
        for y in range(n):
            canonical = C0(x, y, n, h_hat, sigma, core)
            emp = T_emp[x][y]
            if emp != canonical:
                deviations.append((x, y, canonical, emp))
                if emp == h_hat:
                    reset_edges_hat.append([x, y])

    # Transport recovery: how often does B_emp[x][y] == (x+y) mod n?
    transport_match_count = 0
    transport_total = n * n
    for x in range(n):
        for y in range(n):
            if B_emp[x][y] == (x + y) % n:
                transport_match_count += 1
    transport_op_match = transport_match_count / transport_total

    # Sigma_hat: by spec, computed from canonical formula on units
    sigma_hat = {str(u): v2(3 * u + 1) for u in units_list}

    result = {
        "n": n,
        "data_file": os.path.basename(data_path),
        "h_hat": int(h_hat),
        "units_hat": units_list,
        "core_hat": core,
        "sigma_hat": sigma_hat,
        "reset_edges_hat": reset_edges_hat,
        "deviation_count": len(deviations),
        "transport_op_match": round(transport_op_match, 6),
        "T_hat_matrix": T_emp,
        "B_hat_matrix": B_emp,
    }

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

    return result


def main():
    parser = argparse.ArgumentParser(description="B2 WRG fitter (instrument under test)")
    parser.add_argument("--data", required=True, help="path to data/wrg_*.csv")
    parser.add_argument("--output", required=True, help="path to results/*.fit.json")
    args = parser.parse_args()

    result = fit(args.data, args.output)
    print(f"  n={result['n']}  h_hat={result['h_hat']}  "
          f"reset_edges={len(result['reset_edges_hat'])}  "
          f"deviations={result['deviation_count']}  "
          f"transport_match={result['transport_op_match']:.4f}")


if __name__ == "__main__":
    main()
