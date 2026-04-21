"""
B1 Nested Shell Collapse Generator
Reference implementation per B1_NSCG_SPEC_v1.0 §1-§5.

Produces:
  data/nscg_N{N}_p{p:03d}_s{s}.csv             (15 files)
  sealed/nscg_N{N}_p{p:03d}_s{s}.truth.json    (15 files)
  manifest/data_hashes.json
  manifest/sealed_hashes.json
  manifest/first5_triples.json

Usage:
    python generate_nscg.py [--root <dir>]

If --root is omitted, the script's parent directory is used (so the
'data/', 'sealed/', and 'manifest/' folders sit next to 'generator/').
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

SPEC_VERSION = "B1-v1.0"

# ---------------------------------------------------------------------------
# Ground-truth definitions (spec §1.2)
# ---------------------------------------------------------------------------

H_TRUE = 7
SIGMA_TRUE = {1: 2, 3: 1, 7: 1, 9: 2}
UNITS_TRUE = [1, 3, 7, 9]
CORE_TRUE = [3, 7, 9]
S_MAX_TRUE = [(2, 4), (4, 2), (2, 9), (9, 2), (4, 8), (8, 4)]
S_ADD_TRUE = [(1, 2), (2, 1)]
S_TRUE = list(S_ADD_TRUE) + list(S_MAX_TRUE)

REFERENCE_TABLE = [
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


def C0(x: int, y: int) -> int:
    """Canonical construction (spec §1.2 step 'C_0')."""
    if x == 0 or y == 0:
        if (x, y) in {(0, 7), (7, 0)}:
            return 7
        return 0
    if (
        x in CORE_TRUE
        and y in CORE_TRUE
        and SIGMA_TRUE[x] != SIGMA_TRUE[y]
    ):
        return x if SIGMA_TRUE[x] < SIGMA_TRUE[y] else y
    return H_TRUE


_S_MAX_SET = set(S_MAX_TRUE)
_S_ADD_SET = set(S_ADD_TRUE)


def T_true(x: int, y: int) -> int:
    """Full operator (spec §1.2)."""
    if (x, y) in _S_MAX_SET:
        return max(x, y)
    if (x, y) in _S_ADD_SET:
        return (x + y) % 10
    return C0(x, y)


def _build_table() -> list[list[int]]:
    return [[T_true(x, y) for y in range(10)] for x in range(10)]


def _verify_reference_table() -> None:
    table = _build_table()
    for x in range(10):
        for y in range(10):
            if table[x][y] != REFERENCE_TABLE[x][y]:
                raise SystemExit(
                    f"Generator FAILED reference-table check at "
                    f"({x},{y}): got {table[x][y]} expected {REFERENCE_TABLE[x][y]}"
                )


# ---------------------------------------------------------------------------
# Generation (spec §3.2)
# ---------------------------------------------------------------------------


def generate_one(N: int, p_noise: float, seed: int):
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(N):
        x = int(rng.integers(0, 10))
        y = int(rng.integers(0, 10))
        u = float(rng.random())
        if u < p_noise:
            z = int(rng.integers(0, 10))
        else:
            z = T_true(x, y)
        rows.append((x, y, z))
    return rows


def write_csv(rows, path: Path) -> str:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["x", "y", "z"])
        for r in rows:
            w.writerow(r)
    return _sha256_file(path)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_truth(
    out_path: Path, N: int, p_noise: float, seed: int, data_filename: str, data_sha: str
) -> str:
    truth = {
        "spec_version": SPEC_VERSION,
        "config": {"n": 10, "N": N, "p_noise": p_noise, "seed": seed},
        "h_true": H_TRUE,
        "sigma_true": {str(k): v for k, v in SIGMA_TRUE.items()},
        "units_true": UNITS_TRUE,
        "core_true": CORE_TRUE,
        "S_MAX_true": [list(p) for p in S_MAX_TRUE],
        "S_ADD_true": [list(p) for p in S_ADD_TRUE],
        "S_true": [list(p) for p in S_TRUE],
        "T_true_matrix": REFERENCE_TABLE,
        "data_file": f"data/{data_filename}",
        "data_sha256": data_sha,
    }
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(truth, f, indent=2)
    return _sha256_file(out_path)


# ---------------------------------------------------------------------------
# Run (spec §2)
# ---------------------------------------------------------------------------

CONFIGS = [
    (100_000, 0.05),
    (500_000, 0.15),
    (1_000_000, 0.30),
]
SEEDS = [0, 1, 2, 3, 4]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="benchmark root directory")
    args = ap.parse_args()

    if args.root is None:
        root = Path(__file__).resolve().parent.parent
    else:
        root = Path(args.root).resolve()

    data_dir = root / "data"
    sealed_dir = root / "sealed"
    manifest_dir = root / "manifest"
    for d in (data_dir, sealed_dir, manifest_dir):
        d.mkdir(parents=True, exist_ok=True)

    print(f"Generator root: {root}")
    print(f"Spec version : {SPEC_VERSION}")
    print("Verifying reference table ... ", end="")
    _verify_reference_table()
    print("OK (100/100)")

    data_hashes: dict[str, str] = {}
    sealed_hashes: dict[str, str] = {}
    first5: dict[str, list[list[int]]] = {}

    for N, p in CONFIGS:
        p_pct = int(round(p * 100))
        for s in SEEDS:
            cfg_id = f"N{N}_p{p_pct:03d}_s{s}"
            data_name = f"nscg_{cfg_id}.csv"
            truth_name = f"nscg_{cfg_id}.truth.json"
            data_path = data_dir / data_name
            truth_path = sealed_dir / truth_name

            print(f"  generating {cfg_id} ... ", end="", flush=True)
            rows = generate_one(N, p, s)
            data_sha = write_csv(rows, data_path)
            sealed_sha = write_truth(truth_path, N, p, s, data_name, data_sha)
            data_hashes[data_name] = f"sha256:{data_sha}"
            sealed_hashes[truth_name] = f"sha256:{sealed_sha}"

            if (N, p, s) == (100_000, 0.05, 0):
                first5[cfg_id] = [list(r) for r in rows[:5]]
            print(f"OK  data={data_sha[:12]}...")

    with (manifest_dir / "data_hashes.json").open("w", encoding="utf-8") as f:
        json.dump(data_hashes, f, indent=2)
    with (manifest_dir / "sealed_hashes.json").open("w", encoding="utf-8") as f:
        json.dump(sealed_hashes, f, indent=2)
    with (manifest_dir / "first5_triples.json").open("w", encoding="utf-8") as f:
        json.dump({"spec_version": SPEC_VERSION, "configs": first5}, f, indent=2)

    print(f"\nWrote {len(data_hashes)} data files, {len(sealed_hashes)} sealed files.")
    print(f"Manifest in {manifest_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
