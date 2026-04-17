"""
B1 Reference Instrument Fitter
Per B1_NSCG_SPEC_v1.0 §7-§8 and Appendix C.

Algorithm (frozen at v1.0.0):
  1. Read CSV; build empirical mode operator T_emp[x,y] = argmax_z count(x,y,z),
     with deterministic tie-break on smallest z.
  2. Carrier size n = 10 (the only announced parameter, spec §7).
  3. units_hat   = {u in {0..n-1} : gcd(u,n) = 1}                  (canonical)
  4. sigma_hat   = {u : v2(3u+1)} for u in units_hat               (canonical)
  5. core_hat    = units_hat \ {1}                                 (canonical)
  6. h_hat       = mode of T_emp across all 100 cells              (data-driven)
  7. Build C_0(x,y; n, h_hat, sigma_hat).
  8. seam_candidates = {(x,y) : T_emp[x,y] != C_0[x,y]}.
  9. For each (x,y) in seam_candidates:
        - if T_emp[x,y] == max(x,y) and T_emp[x,y] != (x+y)%n  -> MAX
        - elif T_emp[x,y] == (x+y)%n and T_emp[x,y] != max(x,y) -> ADD
        - elif T_emp[x,y] == max(x,y) == (x+y)%n               -> MAX (deterministic preference)
        - else                                                   -> drop (treat as C_0 noise)
 10. Reassemble T_hat per the consistency rule in spec §8.

Hard rules:
  - The fitter does NOT read sealed/, manifest/, or generator source.
  - Determinism: no randomness used. Same data -> same output.
  - No tuning after seeing results.

Usage:
    python fit_nscg.py --data <path/to/data.csv> --output <path/to/fit.json>
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from math import gcd
from pathlib import Path

ALGORITHM_NAME = "ReferenceInstrumentFitter"
ALGORITHM_VERSION = "1.0.0"
SPEC_VERSION = "B1-v1.0"

N_RING = 10  # announced per spec §7


# ---------------------------------------------------------------------------
# Canonical helpers (no data needed)
# ---------------------------------------------------------------------------


def v2(n: int) -> int:
    """2-adic valuation of a non-zero integer."""
    if n == 0:
        return 0
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def canonical_units(n: int) -> list[int]:
    return [u for u in range(n) if gcd(u, n) == 1]


def canonical_sigma(units: list[int]) -> dict[int, int]:
    return {u: v2(3 * u + 1) for u in units}


def canonical_core(units: list[int]) -> list[int]:
    return [u for u in units if u != 1]


def C0(x: int, y: int, n: int, h: int, sigma: dict[int, int], core: list[int]) -> int:
    """Canonical construction (n, h, sigma)."""
    if x == 0 or y == 0:
        if (x, y) in {(0, h), (h, 0)}:
            return h
        return 0
    if x in core and y in core and sigma.get(x, -1) != sigma.get(y, -1):
        return x if sigma[x] < sigma[y] else y
    return h


# ---------------------------------------------------------------------------
# Empirical mode operator
# ---------------------------------------------------------------------------


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def empirical_mode(data_path: Path, n: int):
    """Returns (T_emp, support) where T_emp[x,y] is the mode (deterministic
    smallest-z tie-break) and support[x,y] is the number of observations."""
    counts = [[[0] * n for _ in range(n)] for _ in range(n)]  # [x][y][z]
    support = [[0] * n for _ in range(n)]
    with data_path.open("r", encoding="utf-8") as f:
        rdr = csv.reader(f)
        header = next(rdr)
        if header != ["x", "y", "z"]:
            raise SystemExit(f"Bad header in {data_path}: {header}")
        for row in rdr:
            x = int(row[0])
            y = int(row[1])
            z = int(row[2])
            counts[x][y][z] += 1
            support[x][y] += 1
    T_emp = [[0] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            best_z = 0
            best_c = -1
            for z in range(n):
                c = counts[x][y][z]
                if c > best_c:
                    best_c = c
                    best_z = z
            T_emp[x][y] = best_z
    return T_emp, support


# ---------------------------------------------------------------------------
# Fitter
# ---------------------------------------------------------------------------


def fit(data_path: Path, n: int = N_RING):
    T_emp, support = empirical_mode(data_path, n)

    # 3-5: canonical inferences (depend only on n)
    units = canonical_units(n)
    sigma = canonical_sigma(units)
    core = canonical_core(units)

    # 6: attractor h_hat from data
    val_count = [0] * n
    for x in range(n):
        for y in range(n):
            val_count[T_emp[x][y]] += 1
    h_hat = max(range(n), key=lambda v: (val_count[v], -v))  # tie-break smallest v

    # 7-9: seam detection and classification
    seam_max: list[list[int]] = []
    seam_add: list[list[int]] = []

    for x in range(n):
        for y in range(n):
            c0 = C0(x, y, n, h_hat, sigma, core)
            t = T_emp[x][y]
            if t == c0:
                continue
            mx = max(x, y)
            ad = (x + y) % n
            if t == mx and t != ad:
                seam_max.append([x, y])
            elif t == ad and t != mx:
                seam_add.append([x, y])
            elif t == mx and t == ad:
                # ambiguous; deterministic preference for MAX
                seam_max.append([x, y])
            else:
                # neither MAX nor ADD explains the deviation; drop
                # (treat as C_0 noise)
                continue

    seam = sorted([tuple(p) for p in seam_max] + [tuple(p) for p in seam_add])
    seam_max_set = {tuple(p) for p in seam_max}
    seam_add_set = {tuple(p) for p in seam_add}

    # 10: reassemble T_hat per spec §8 consistency rule
    T_hat = [[0] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if (x, y) in seam_max_set:
                T_hat[x][y] = max(x, y)
            elif (x, y) in seam_add_set:
                T_hat[x][y] = (x + y) % n
            else:
                T_hat[x][y] = C0(x, y, n, h_hat, sigma, core)

    return {
        "spec_version": SPEC_VERSION,
        "algorithm_name": ALGORITHM_NAME,
        "algorithm_version": ALGORITHM_VERSION,
        "h_hat": h_hat,
        "sigma_hat": {str(k): v for k, v in sigma.items()},
        "units_hat": units,
        "core_hat": core,
        "S_hat": [list(p) for p in seam],
        "max_domain_hat": sorted(seam_max),
        "add_domain_hat": sorted(seam_add),
        "T_hat_matrix": T_hat,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    data_path = Path(args.data).resolve()
    out_path = Path(args.output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if not data_path.exists():
        print(f"Data file not found: {data_path}", file=sys.stderr)
        return 2

    data_sha = _sha256_file(data_path)
    fit_obj = fit(data_path)
    fit_obj["data_file"] = f"data/{data_path.name}"
    fit_obj["data_sha256"] = data_sha

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(fit_obj, f, indent=2)
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
