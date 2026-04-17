"""
generate_wrg.py -- B2 Wobble-Reset Generator (WRG) per
SHELL_NATIVE_BENCHMARKS.md §B2.

Carriers:    n in {10, 14, 22, 34}  (compatibility family)
Wobble:      p_w in {0.05, 0.20}
Seeds:       3 per (n, p_w)  ->  4 * 2 * 3 = 24 configurations.

Each config produces:
  - data/wrg_n{n}_pw{pw_pct}_s{seed}.csv  with columns x,y,z_T,z_B
  - sealed/truth_n{n}_pw{pw_pct}_s{seed}.json  (truth_h, truth_sigma,
    units, core, reset_edges, transport_op = "(x+y) mod n")
  - manifest/data_hashes.json  -- sha256 of every CSV
  - manifest/sealed_hashes.json
  - manifest/first5_triples.json  -- determinism check

Sample size N = max(100_000, 500 * n^2):
  n=10  -> 100,000   (1000 obs/cell)
  n=14  -> 100,000   (~510 obs/cell)
  n=22  ->  242,000  (~500 obs/cell)
  n=34  ->  578,000  (~500 obs/cell)

This makes per-cell coverage ~500-1000 (well below B1's 1000-10000),
so the mode operator is no longer trivially noise-immune at p_w=0.20.
"""

import os, json, hashlib, csv
from typing import Dict, List, Tuple
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
SEALED_DIR = os.path.join(ROOT, "sealed")
MANIFEST_DIR = os.path.join(ROOT, "manifest")

CARRIERS = [10, 14, 22, 34]
WOBBLE_LEVELS = [0.05, 0.20]
SEEDS = [0, 1, 2]

# Pre-verified attractors (largest shell-1 element where shell = v_2(3u+1))
H_TRUE = {10: 7, 14: 11, 22: 19, 34: 31}


def v2(k: int) -> int:
    """2-adic valuation."""
    if k == 0:
        return 0
    n = 0
    while k % 2 == 0:
        k //= 2
        n += 1
    return n


def units(n: int) -> List[int]:
    """U(Z/nZ) = {u in 1..n-1 : gcd(u,n)=1}."""
    from math import gcd
    return [u for u in range(1, n) if gcd(u, n) == 1]


def sigma_map(n: int) -> Dict[int, int]:
    """sigma(u) = v_2(3u + 1) for u in U(Z/nZ)."""
    return {u: v2(3 * u + 1) for u in units(n)}


def core_set(n: int) -> List[int]:
    """Core = units \\ {1} (per Q-series)."""
    return [u for u in units(n) if u != 1]


def reset_edges(n: int) -> List[Tuple[int, int]]:
    """
    Reset edges per spec: include (h, 0), (0, h) plus 2-4 additional pairs.

    We add (1, 0), (0, 1), (3, 9), (9, 3). These are chosen so that the
    canonical C_0 does NOT already return h there:
      - (1, 0), (0, 1):  C_0 returns 0    (zero-row/col, not the (h,0) case)
      - (3, 9), (9, 3):  C_0 returns 3    (both in core, sigma(3)=1 < sigma(9)=2)

    This makes the reset edges OBSERVABLE -- they force z = h where C_0
    would otherwise produce a different value. The required pairs (h, 0)
    and (0, h) are also included for spec compliance, even though C_0
    already returns h there (so they have no observable effect).
    """
    h = H_TRUE[n]
    edges = [(h, 0), (0, h), (1, 0), (0, 1), (3, 9), (9, 3)]
    seen = set()
    uniq = []
    for e in edges:
        if e not in seen:
            seen.add(e)
            uniq.append(e)
    return uniq


def C0(x: int, y: int, n: int, h: int, sigma: Dict[int, int],
       core: List[int]) -> int:
    """
    Generalized canonical construction C_0(R_n, h, sigma).

    1. If x = 0 or y = 0:
         if (x,y) in {(0,h),(h,0)}: return h
         else: return 0
    2. Else if x in Core and y in Core and sigma(x) != sigma(y):
         return x if sigma(x) < sigma(y) else y
    3. Else: return h
    """
    if x == 0 or y == 0:
        if (x, y) == (0, h) or (x, y) == (h, 0):
            return h
        return 0
    if x in core and y in core and sigma.get(x) != sigma.get(y):
        return x if sigma[x] < sigma[y] else y
    return h


def K_c(x: int, y: int, n: int, h: int, sigma: Dict[int, int],
        core: List[int], r_edges: set) -> int:
    """
    Collapse kernel = C_0 with reset edges overlaid.
    Reset edges force z = h regardless of C_0.
    """
    if (x, y) in r_edges:
        return h
    return C0(x, y, n, h, sigma, core)


def B_true(x: int, y: int, n: int) -> int:
    """Transport companion: (x + y) mod n."""
    return (x + y) % n


def n_for_carrier(n: int) -> int:
    """Sample count: max(100_000, 500 * n^2)."""
    return max(100_000, 500 * n * n)


def generate_one(n: int, p_w: float, seed: int):
    """Generate one config; return (csv_path, sealed_path, first5)."""
    h = H_TRUE[n]
    sigma = sigma_map(n)
    core = core_set(n)
    r_edges_list = reset_edges(n)
    r_edges_set = set(r_edges_list)

    N = n_for_carrier(n)
    rng = np.random.default_rng(seed=seed * 7919 + int(round(p_w * 100)) * 101 + n)

    # Sample x, y uniformly from {0..n-1}
    xs = rng.integers(0, n, size=N)
    ys = rng.integers(0, n, size=N)

    # Wobble draws: prob p_w of perturbation, delta uniform in {-1, 0, +1}
    wobble_draws = rng.random(size=N)
    wobble_deltas = rng.integers(-1, 2, size=N)  # -1, 0, +1 inclusive

    z_T = np.zeros(N, dtype=np.int64)
    z_B = np.zeros(N, dtype=np.int64)
    for i in range(N):
        x, y = int(xs[i]), int(ys[i])
        z = K_c(x, y, n, h, sigma, core, r_edges_set)
        if wobble_draws[i] < p_w:
            z = (z + int(wobble_deltas[i])) % n
        z_T[i] = z
        z_B[i] = B_true(x, y, n)

    pw_pct = int(round(p_w * 100))
    csv_name = f"wrg_n{n}_pw{pw_pct}_s{seed}.csv"
    csv_path = os.path.join(DATA_DIR, csv_name)
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x", "y", "z_T", "z_B"])
        for i in range(N):
            w.writerow([int(xs[i]), int(ys[i]), int(z_T[i]), int(z_B[i])])

    truth = {
        "n": n,
        "p_wobble": p_w,
        "seed": seed,
        "N": N,
        "h_true": h,
        "units_true": units(n),
        "core_true": core,
        "sigma_true": {str(k): int(v) for k, v in sigma.items()},
        "reset_edges": [[a, b] for a, b in r_edges_list],
        "transport_op": "(x + y) mod n",
    }
    sealed_name = f"truth_n{n}_pw{pw_pct}_s{seed}.json"
    sealed_path = os.path.join(SEALED_DIR, sealed_name)
    with open(sealed_path, "w") as f:
        json.dump(truth, f, indent=2)

    first5 = [[int(xs[i]), int(ys[i]), int(z_T[i]), int(z_B[i])]
              for i in range(5)]
    return csv_path, sealed_path, csv_name, sealed_name, first5


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    print(f"B2 WRG generator -- {len(CARRIERS)} carriers x "
          f"{len(WOBBLE_LEVELS)} wobble x {len(SEEDS)} seeds = "
          f"{len(CARRIERS)*len(WOBBLE_LEVELS)*len(SEEDS)} configs")

    data_hashes = {}
    sealed_hashes = {}
    first5_dump = {}

    for n in CARRIERS:
        for p_w in WOBBLE_LEVELS:
            for seed in SEEDS:
                csv_path, sealed_path, csv_name, sealed_name, first5 = \
                    generate_one(n, p_w, seed)
                data_hashes[csv_name] = sha256_file(csv_path)
                sealed_hashes[sealed_name] = sha256_file(sealed_path)
                first5_dump[csv_name] = first5
                size_mb = os.path.getsize(csv_path) / 1024 / 1024
                print(f"  n={n:2d} pw={p_w:.2f} s={seed}  N={n_for_carrier(n):>7d}  "
                      f"{csv_name}  ({size_mb:.1f} MB)")

    with open(os.path.join(MANIFEST_DIR, "data_hashes.json"), "w") as f:
        json.dump(data_hashes, f, indent=2)
    with open(os.path.join(MANIFEST_DIR, "sealed_hashes.json"), "w") as f:
        json.dump(sealed_hashes, f, indent=2)
    with open(os.path.join(MANIFEST_DIR, "first5_triples.json"), "w") as f:
        json.dump(first5_dump, f, indent=2)
    print(f"\nWrote {len(data_hashes)} data hashes, {len(sealed_hashes)} "
          f"sealed hashes, {len(first5_dump)} first-5 triples.")


if __name__ == "__main__":
    main()
