"""
discovery_fitter.py -- Prior-free structural discovery on T_emp.

The premise (per Brayden, 2026-04-17): "TSML may be a close artifact of
structure that only lives in curves through shells." We test this by
forbidding the fitter from using ANY canonical formula -- no gcd, no
v_2(3u+1), no foreknowledge of the unit group. The fitter sees only the
mode-recovered operator T_emp on Z/nZ and asks:

    What structural invariants emerge from T_emp alone?
    Do those invariants match the canonical (units, sigma, core)?
    What survives across noise levels and across carriers?

Pipeline:

    1. Build T_emp via per-cell mode (single allowed inductive step).
    2. Discover h_hat = global mode of T_emp values (data-driven).
    3. Discover image_T = set of distinct values appearing in T_emp.
    4. Discover ZERO behavior: which (x, y) collapse to 0?
    5. Discover ATTRACTOR behavior: which (x, y) collapse to h_hat?
    6. Discover CORE outputs = image_T \\ {0, h_hat} (the "non-default" values).
    7. Discover SEAM cells = cells whose output is in CORE.
    8. Classify each seam cell against a fixed candidate-rule menu:
         MAX(x,y), MIN(x,y), (x+y) mod n, (x-y) mod n, (y-x) mod n,
         (x*y) mod n, x, y, h_hat, 0
       Each cell gets the lexicographically-first rule that matches.
    9. Discover input UNITS = inputs participating in seam cells.
   10. Discover sigma_hat partition by signature clustering on units:
         sig(u) = sorted tuple of T_emp(u, v) for v in units, mod relabel.
         Two units share a partition class iff their signatures match
         under any consistent relabeling.

The output is a "structural fingerprint" per dataset, suitable for
cross-carrier comparison. Compared against the canonical (units, sigma,
core) which are NOT used in fitting -- only in scoring afterwards.

Usage:
    from discovery_fitter import discover
    fingerprint = discover(data_csv_path, n=10)

    # n is read from filename if not supplied (looks for _n<int>_)
"""

import os, csv, re, json
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional


def carrier_from_path(path: str) -> int:
    m = re.search(r"_n(\d+)_", os.path.basename(path))
    if not m:
        return 10  # default for B1 files which don't have _n10_ in name
    return int(m.group(1))


def empirical_T(data_path: str, n: int,
                z_T_col: int = 2) -> List[List[int]]:
    """
    Build T_emp[x][y] = mode of z values at cell (x, y).
    z_T_col = 2 for B1 (3 cols: x,y,z), B2 (4 cols: x,y,z_T,z_B).
    Tie-break: smallest z value.
    """
    counts = [[Counter() for _ in range(n)] for _ in range(n)]
    with open(data_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # header
        for row in reader:
            x, y = int(row[0]), int(row[1])
            z = int(row[z_T_col])
            counts[x][y][z] += 1

    def mode(c: Counter) -> int:
        if not c:
            return -1
        m = max(c.values())
        return min(z for z, cnt in c.items() if cnt == m)

    return [[mode(counts[x][y]) for y in range(n)] for x in range(n)]


# ============================================================
# Candidate rule menu
# ============================================================

def _rules(n: int):
    return [
        ("MAX",      lambda x, y: max(x, y)),
        ("MIN",      lambda x, y: min(x, y)),
        ("ADD",      lambda x, y: (x + y) % n),
        ("SUB_xy",   lambda x, y: (x - y) % n),
        ("SUB_yx",   lambda x, y: (y - x) % n),
        ("MUL",      lambda x, y: (x * y) % n),
        ("X",        lambda x, y: x),
        ("Y",        lambda x, y: y),
    ]


def classify_cell(x: int, y: int, z: int, n: int) -> str:
    """Return the lexicographically-first matching rule, or UNCLASSIFIED."""
    for name, fn in _rules(n):
        if fn(x, y) == z:
            return name
    return "UNCLASSIFIED"


# ============================================================
# Discovery
# ============================================================

def discover(data_path: str, n: Optional[int] = None,
             z_T_col: int = 2) -> Dict:
    """Build the structural fingerprint of T_emp -- no canonical priors."""
    if n is None:
        n = carrier_from_path(data_path)

    T = empirical_T(data_path, n, z_T_col=z_T_col)

    # Step 2: h_hat = mode of all values in T
    flat = [v for row in T for v in row]
    cnt = Counter(flat)
    max_count = max(cnt.values())
    h_hat = min(z for z, c in cnt.items() if c == max_count)

    # Step 3: image
    image_T = sorted(set(flat))

    # Step 4-5: zero / attractor cells
    zero_cells = [(x, y) for x in range(n) for y in range(n) if T[x][y] == 0]
    attractor_cells = [(x, y) for x in range(n) for y in range(n)
                       if T[x][y] == h_hat]

    # Step 6: core outputs
    core_outputs = sorted(v for v in image_T if v != 0 and v != h_hat)

    # Step 7: seam cells
    seam_cells = [(x, y, T[x][y]) for x in range(n) for y in range(n)
                  if T[x][y] in core_outputs]

    # Step 8: classify each seam cell
    seam_by_rule = defaultdict(list)
    for x, y, z in seam_cells:
        rule = classify_cell(x, y, z, n)
        seam_by_rule[rule].append([x, y, z])

    # Also classify zero and attractor cells against rules (informational)
    cell_freq_h_constant = sum(1 for x in range(n) for y in range(n)
                               if T[x][y] == h_hat)
    cell_freq_0_constant = sum(1 for x in range(n) for y in range(n)
                               if T[x][y] == 0)

    # Step 9: input units = inputs participating in seam cells
    units_in = set()
    for x, y, z in seam_cells:
        units_in.add(x)
        units_in.add(y)
    units_hat = sorted(units_in)

    # Step 10: sigma partition by signature on units
    # signature(u) = sorted tuple of T[u][v] for v in units_hat
    # cluster by exact-equality on signature (no relabeling -- conservative).
    sigs = {u: tuple(T[u][v] for v in units_hat) for u in units_hat}
    sig_to_class = {}
    next_label = 0
    sigma_hat = {}
    for u in units_hat:
        s = sigs[u]
        if s not in sig_to_class:
            sig_to_class[s] = next_label
            next_label += 1
        sigma_hat[u] = sig_to_class[s]

    # Group: partition_hat = list of sets of units with same sigma class
    by_class = defaultdict(list)
    for u, c in sigma_hat.items():
        by_class[c].append(u)
    partition_hat = sorted([sorted(v) for v in by_class.values()])

    return {
        "data_file": os.path.basename(data_path),
        "n": n,
        "T_emp": T,
        "h_hat": h_hat,
        "image_T": image_T,
        "image_size": len(image_T),
        "zero_cell_count": len(zero_cells),
        "attractor_cell_count": len(attractor_cells),
        "core_outputs": core_outputs,
        "core_count": len(core_outputs),
        "seam_cell_count": len(seam_cells),
        "seam_cells": [[x, y, z] for x, y, z in seam_cells],
        "seam_by_rule_counts": {k: len(v) for k, v in seam_by_rule.items()},
        "seam_by_rule_cells": {k: v for k, v in seam_by_rule.items()},
        "units_hat": units_hat,
        "units_count": len(units_hat),
        "sigma_hat": {str(u): c for u, c in sigma_hat.items()},
        "partition_hat": partition_hat,
        "partition_class_count": len(partition_hat),
    }


def fingerprint(disc: Dict) -> Dict:
    """Compact 'structural fingerprint' — the comparable signature."""
    return {
        "n": disc["n"],
        "h_hat": disc["h_hat"],
        "image_T": disc["image_T"],
        "core_outputs": disc["core_outputs"],
        "units_hat": disc["units_hat"],
        "partition_hat": disc["partition_hat"],
        "seam_cell_count": disc["seam_cell_count"],
        "seam_by_rule_counts": disc["seam_by_rule_counts"],
        "ratio_attractor": round(disc["attractor_cell_count"] / (disc["n"] ** 2), 4),
        "ratio_zero": round(disc["zero_cell_count"] / (disc["n"] ** 2), 4),
        "ratio_seam": round(disc["seam_cell_count"] / (disc["n"] ** 2), 4),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("data", help="path to *.csv")
    parser.add_argument("--n", type=int, default=None)
    parser.add_argument("--z-col", type=int, default=2,
                        help="column index of z value (2 for B1, 2 for B2 z_T)")
    parser.add_argument("--full", action="store_true",
                        help="print full discovery, not just fingerprint")
    args = parser.parse_args()
    disc = discover(args.data, n=args.n, z_T_col=args.z_col)
    if args.full:
        print(json.dumps(disc, indent=2))
    else:
        print(json.dumps(fingerprint(disc), indent=2))
