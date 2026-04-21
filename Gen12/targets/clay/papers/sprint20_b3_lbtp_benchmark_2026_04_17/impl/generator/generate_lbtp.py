"""
generate_lbtp.py -- B3 Layered Basin-Transport Pair generator.

Per SHELL_NATIVE_BENCHMARKS.md §B3:

  Carrier:   R = Z/10Z
  T_true:    the published Z/10Z TSML (same as B1)
  B_true:    B(x, y) = max(x, y) if xy != 0 else min(x, y)
  Noise:     5% uniform replacement on EACH stream independently
  Streams:   collapse stream (x, y, z_T) and transport stream (x, y, z_B)

We produce a single CSV per config with both streams interleaved:
  x, y, z_T, z_B  (one row per sample)

Configurations: 5 seeds (no parameter sweep beyond seed -- noise is fixed).

Sample size: N = 200,000.  At Z/10Z with 100 cells, that's ~2000 obs/cell.
"""

import os, json, csv, hashlib
from typing import Dict, List
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
SEALED_DIR = os.path.join(ROOT, "sealed")
MANIFEST_DIR = os.path.join(ROOT, "manifest")

N_CARRIER = 10
N_SAMPLES = 200_000
P_NOISE = 0.05
SEEDS = [0, 1, 2, 3, 4]

# Z/10Z TSML reference table (from B1 spec §1.2)
TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],
]


def T_true(x: int, y: int) -> int:
    return TSML[x][y]


def B_true(x: int, y: int) -> int:
    """B(x, y) = max(x, y) if xy != 0 else min(x, y)."""
    if x * y != 0:
        return max(x, y)
    return min(x, y)


def build_B_table() -> List[List[int]]:
    return [[B_true(x, y) for y in range(N_CARRIER)] for x in range(N_CARRIER)]


def generate_one(seed: int):
    rng = np.random.default_rng(seed=seed * 7919 + 1)
    xs = rng.integers(0, N_CARRIER, size=N_SAMPLES)
    ys = rng.integers(0, N_CARRIER, size=N_SAMPLES)
    # Independent noise draws for each stream
    noise_T = rng.random(size=N_SAMPLES)
    noise_B = rng.random(size=N_SAMPLES)
    rand_T = rng.integers(0, N_CARRIER, size=N_SAMPLES)
    rand_B = rng.integers(0, N_CARRIER, size=N_SAMPLES)

    z_T = np.zeros(N_SAMPLES, dtype=np.int64)
    z_B = np.zeros(N_SAMPLES, dtype=np.int64)
    for i in range(N_SAMPLES):
        x, y = int(xs[i]), int(ys[i])
        zT = T_true(x, y) if noise_T[i] >= P_NOISE else int(rand_T[i])
        zB = B_true(x, y) if noise_B[i] >= P_NOISE else int(rand_B[i])
        z_T[i] = zT
        z_B[i] = zB

    csv_name = f"lbtp_s{seed}.csv"
    csv_path = os.path.join(DATA_DIR, csv_name)
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["x", "y", "z_T", "z_B"])
        for i in range(N_SAMPLES):
            w.writerow([int(xs[i]), int(ys[i]), int(z_T[i]), int(z_B[i])])

    truth = {
        "seed": seed,
        "n": N_CARRIER,
        "N": N_SAMPLES,
        "p_noise": P_NOISE,
        "T_true": TSML,
        "B_true": build_B_table(),
    }
    sealed_name = f"truth_s{seed}.json"
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
    print(f"B3 LBTP generator -- {len(SEEDS)} seeds, N={N_SAMPLES}, "
          f"p_noise={P_NOISE}")

    data_hashes, sealed_hashes, first5_dump = {}, {}, {}
    for seed in SEEDS:
        csv_path, sealed_path, csv_name, sealed_name, first5 = generate_one(seed)
        data_hashes[csv_name] = sha256_file(csv_path)
        sealed_hashes[sealed_name] = sha256_file(sealed_path)
        first5_dump[csv_name] = first5
        size_mb = os.path.getsize(csv_path) / 1024 / 1024
        print(f"  seed={seed}  {csv_name}  ({size_mb:.1f} MB)")

    with open(os.path.join(MANIFEST_DIR, "data_hashes.json"), "w") as f:
        json.dump(data_hashes, f, indent=2)
    with open(os.path.join(MANIFEST_DIR, "sealed_hashes.json"), "w") as f:
        json.dump(sealed_hashes, f, indent=2)
    with open(os.path.join(MANIFEST_DIR, "first5_triples.json"), "w") as f:
        json.dump(first5_dump, f, indent=2)
    print(f"\nWrote {len(data_hashes)} data + sealed hashes.")


if __name__ == "__main__":
    main()
