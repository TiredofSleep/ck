"""
prove_corridor_closure.py -- Algebraic / exhaustive proof that the
canonical TSML/WRG operator's seam classifies entirely under
{MAX, MIN, ADD} for every n in the compatibility family.

Empirical observation (Sprint 21): across 39 datasets, every seam cell of
T_emp falls under one of MAX, MIN, or ADD. Sprint 25 closes that loop:
prove the canonical generator C_0(R_n, h, sigma) (no reset overlay)
satisfies the same closure for every n in a wider family by *exhaustive
case analysis* on the n^2 cells.

For each n, we:
    1. Construct C_0 as defined in B2 (Sprint 19, generate_wrg.py).
    2. Compute image_T = sorted set of distinct C_0 values.
    3. Compute core_outputs = image_T \\ {0, h_n}.
    4. Iterate every (x, y) cell whose output is in core_outputs.
    5. Test which rule from the menu matches:
         {MAX, MIN, ADD, SUB_xy, SUB_yx, MUL, X, Y}
    6. Assert every seam cell matches at least one of {MAX, MIN, ADD}.

This is a per-n finite proof. For each n, the proof either passes
(closure holds, no rule outside {MAX,MIN,ADD} ever needed) or fails
(some seam cell needs MUL/SUB/X/Y, in which case the closure thesis is
falsified for that n).

We test n in the original family {10, 14, 22, 34} plus extensions
{38, 46, 58, 62, 74, 82, 94, 106, 118, 122, 134, 142}.
"""

import os, sys, json
from collections import defaultdict
from math import gcd
from typing import Dict, List, Tuple


HERE = os.path.dirname(os.path.abspath(__file__))
SPRINT_DIR = os.path.dirname(HERE)
RESULTS_DIR = os.path.join(SPRINT_DIR, "results")


# ============================================================
# Canonical construction (mirrors B2 generate_wrg.py)
# ============================================================

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


def attractor_h(n: int):
    """h_n = max element of {u in units : sigma(u) = 1}, or None if empty."""
    sig = sigma_map(n)
    s1 = [u for u, s in sig.items() if s == 1]
    return max(s1) if s1 else None


def C0(x: int, y: int, n: int, h: int,
       sigma: Dict[int, int], core: List[int]) -> int:
    if x == 0 or y == 0:
        if (x, y) == (0, h) or (x, y) == (h, 0):
            return h
        return 0
    if x in core and y in core and sigma.get(x) != sigma.get(y):
        return x if sigma[x] < sigma[y] else y
    return h


# ============================================================
# Rule menu (same as Sprint 21 discovery_fitter)
# ============================================================

def rules(n: int):
    return [
        ("MAX",    lambda x, y: max(x, y)),
        ("MIN",    lambda x, y: min(x, y)),
        ("ADD",    lambda x, y: (x + y) % n),
        ("SUB_xy", lambda x, y: (x - y) % n),
        ("SUB_yx", lambda x, y: (y - x) % n),
        ("MUL",    lambda x, y: (x * y) % n),
        ("X",      lambda x, y: x),
        ("Y",      lambda x, y: y),
    ]


CORRIDOR = {"MAX", "MIN", "ADD"}


# ============================================================
# Per-n exhaustive proof
# ============================================================

def prove_for_n(n: int) -> Dict:
    h = attractor_h(n)
    if h is None:
        return {
            "n": n, "skipped": True,
            "reason": "no shell-1 unit (sigma(u) = 1 layer empty)"
        }
    sigma = sigma_map(n)
    core = core_set(n)

    # Build C_0 table
    T = [[C0(x, y, n, h, sigma, core) for y in range(n)] for x in range(n)]
    flat = [v for row in T for v in row]
    image_T = sorted(set(flat))
    core_outputs = sorted(v for v in image_T if v != 0 and v != h)

    # Walk every seam cell, classify against the full rule menu
    seam_classified = defaultdict(list)
    seam_unclassified = []
    seam_outside_corridor = []
    rule_list = rules(n)

    seam_cell_count = 0
    for x in range(n):
        for y in range(n):
            z = T[x][y]
            if z not in core_outputs:
                continue
            seam_cell_count += 1
            matches = [name for name, fn in rule_list if fn(x, y) == z]
            corridor_matches = [m for m in matches if m in CORRIDOR]
            if not matches:
                seam_unclassified.append((x, y, z))
            elif not corridor_matches:
                # Matched only outside-corridor rules
                seam_outside_corridor.append((x, y, z, matches))
            for m in matches:
                seam_classified[m].append([x, y, z])

    # Closure test
    corridor_closed = (len(seam_unclassified) == 0
                       and len(seam_outside_corridor) == 0)

    # Also classify zero and attractor cells (informational)
    zero_count = sum(1 for v in flat if v == 0)
    attractor_count = sum(1 for v in flat if v == h)

    return {
        "n": n,
        "h": h,
        "n_units": len(units(n)),
        "image_T": image_T,
        "core_outputs": core_outputs,
        "zero_cells": zero_count,
        "attractor_cells": attractor_count,
        "seam_cells": seam_cell_count,
        "seam_by_rule_counts": {k: len(v) for k, v in seam_classified.items()},
        "corridor_closed": corridor_closed,
        "n_unclassified": len(seam_unclassified),
        "n_outside_corridor": len(seam_outside_corridor),
        "outside_corridor_examples":
            [list(c) for c in seam_outside_corridor[:5]],
        "skipped": False,
    }


# ============================================================
# Sweep
# ============================================================

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Original compatibility family
    ORIGINAL = [10, 14, 22, 34]
    # Extensions: 2 * (odd prime), various
    EXTENSIONS = [38, 46, 58, 62, 74, 82, 94, 106, 118, 122, 134, 142]
    # Sanity inclusions: also some 2*p^2, 2*p*q, etc.
    OTHER = [50, 70, 110, 130, 170, 190, 230]

    all_n = sorted(set(ORIGINAL + EXTENSIONS + OTHER))

    print(f"Sprint 25: corridor-closure proof on n in {all_n}\n")

    results = {}
    pass_count = 0
    fail_count = 0
    skip_count = 0

    for n in all_n:
        r = prove_for_n(n)
        results[n] = r
        if r.get("skipped"):
            skip_count += 1
            print(f"  n={n:4d}  SKIP  ({r['reason']})")
            continue
        flag = "PASS" if r["corridor_closed"] else "FAIL"
        if r["corridor_closed"]:
            pass_count += 1
        else:
            fail_count += 1
        rules_str = " + ".join(f"{k}:{v}"
                               for k, v in sorted(r["seam_by_rule_counts"].items())
                               if k in CORRIDOR)
        outside_str = ""
        if not r["corridor_closed"]:
            outside_str = (f"  OUTSIDE: {r['n_outside_corridor']} cells, "
                           f"UNCLASSIFIED: {r['n_unclassified']}")
        print(f"  n={n:4d}  h={r['h']:>3}  units={r['n_units']:>3}  "
              f"seam={r['seam_cells']:>4}  [{rules_str}]  "
              f"{flag}{outside_str}")

    print(f"\nSummary: {pass_count} PASS, {fail_count} FAIL, "
          f"{skip_count} SKIP, {len(all_n)} total")

    summary = {
        "carriers_tested": all_n,
        "pass": pass_count,
        "fail": fail_count,
        "skip": skip_count,
        "all_pass": (fail_count == 0),
        "rule_menu_tested": [r[0] for r in rules(0)],
        "corridor_set": sorted(CORRIDOR),
    }
    with open(os.path.join(RESULTS_DIR, "corridor_closure_summary.json"),
              "w") as f:
        json.dump(summary, f, indent=2)
    with open(os.path.join(RESULTS_DIR, "corridor_closure_full.json"),
              "w") as f:
        json.dump({str(k): v for k, v in results.items()}, f, indent=2)

    print(f"\nWrote results to {RESULTS_DIR}/")
    if summary["all_pass"]:
        print(f"\nTHEOREM (empirical for tested n): for every n in the tested "
              f"family, the canonical C_0 operator's seam is classifiable "
              f"entirely by {{MAX, MIN, ADD}}. The corridor menu is closed.")
    else:
        print(f"\nFalsified for {fail_count} carriers. See full results.")


if __name__ == "__main__":
    main()
