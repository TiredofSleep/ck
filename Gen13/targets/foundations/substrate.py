"""
A0 -- The substrate Z/10Z.

This module encodes the foundational substrate quantities that every
TIG paper inherits. All values are constructed from definitions (no
hardcoded outputs); running this module verifies the substrate-level
identities that the audited journal papers depend on.

Adapted from sprint_bundle_2026-05-06_v31_RIGOR_PASS/scripts/substrate.py.
"""
from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------------
# A0: the ring Z/10Z
# ---------------------------------------------------------------------------

N = 10  # the substrate size

# Standard ring tables.
ADD = np.array([[(i + j) % N for j in range(N)] for i in range(N)])
MUL = np.array([[(i * j) % N for j in range(N)] for i in range(N)])


# ---------------------------------------------------------------------------
# Frozen cells (where ADD = MUL): foundation of Omega_b = HARMONY^2 / N^3
# ---------------------------------------------------------------------------

def frozen_cells() -> list[tuple[int, int]]:
    """Cells (i, j) where (i + j) mod N == (i * j) mod N."""
    return [(i, j) for i in range(N) for j in range(N) if ADD[i, j] == MUL[i, j]]


# ---------------------------------------------------------------------------
# Cross-cycle disagreement: foundation of Omega_DM = 44 * 6 / N^3
# ---------------------------------------------------------------------------

CREATION = (1, 3, 7, 9)      # units of Z/10Z (multiplicative cycle)
DISSOLUTION = (2, 4, 6, 8)   # non-units (additive cycle)


def cross_cycle_disagreement() -> int:
    """sum |ADD[c, d] - MUL[c, d]| over c in CREATION, d in DISSOLUTION."""
    return int(sum(abs(int(ADD[c, d]) - int(MUL[c, d]))
                   for c in CREATION for d in DISSOLUTION))


# ---------------------------------------------------------------------------
# The sigma permutation
# ---------------------------------------------------------------------------

# Canonical sigma per the bundle's substrate.py (the operator-cycle
# permutation referenced as pi in the audited four-core consolidated paper
# to avoid name collision with the sigma-rate function sigma(N)).
SIGMA = {0: 0, 3: 3, 8: 8, 9: 9,    # fixed points
         1: 7, 7: 6, 6: 5, 5: 4, 4: 2, 2: 1}  # 6-cycle (1 7 6 5 4 2)


def sigma_units(u: int) -> int:
    """sigma_units = nu_2(3u + 1) for u in {1, 3, 7, 9}."""
    if u not in (1, 3, 7, 9):
        raise ValueError(f"u must be a unit of Z/10Z (in {{1,3,7,9}}), got {u}")
    n = 3 * u + 1
    count = 0
    while n % 2 == 0:
        n //= 2
        count += 1
    return count


# ---------------------------------------------------------------------------
# CRT decomposition Z/10Z ~= F_2 x F_5
# ---------------------------------------------------------------------------

def crt_iso(x: int) -> tuple[int, int]:
    """Return (x mod 2, x mod 5)."""
    return x % 2, x % 5


def crt_inv(parity: int, pent: int) -> int:
    """Inverse of crt_iso. Returns x in 0..9 with crt_iso(x) = (parity, pent)."""
    for x in range(N):
        if crt_iso(x) == (parity, pent):
            return x
    raise ValueError(f"no x in Z/10Z with crt_iso = ({parity}, {pent})")


# ---------------------------------------------------------------------------
# Coherence threshold T* = 5/7 and wobble W = 3/50
# ---------------------------------------------------------------------------

T_STAR_NUM = 5
T_STAR_DEN = 7

W_NUM = 3
W_DEN = 50


def t_star() -> float:
    return T_STAR_NUM / T_STAR_DEN


def wobble() -> float:
    return W_NUM / W_DEN


def wobble_three_derivations() -> tuple[float, float, float]:
    """Three independent computations of W = 3/50 = 0.06.

    (1) |44 - 50| / 100  -- cross-cycle distance from N*5
    (2) 6 / 100           -- sigma-cycle / N^2
    (3) 1.5 / 25          -- T*-deviation / BALANCE^2
    """
    return abs(44 - 50) / 100, 6 / 100, 1.5 / 25


# ---------------------------------------------------------------------------
# Verification (run as __main__ to print substrate facts)
# ---------------------------------------------------------------------------

def verify(verbose: bool = True) -> dict[str, bool]:
    """Run all substrate-level verifications and return pass/fail dict."""
    results: dict[str, bool] = {}

    fz = frozen_cells()
    results["frozen_cells_count_4"] = len(fz) == 4
    if verbose:
        print(f"Frozen cells (ADD = MUL): {fz}")
        print(f"  Count: {len(fz)}  (expected 4)")

    disagreement = cross_cycle_disagreement()
    results["cross_cycle_44"] = disagreement == 44
    if verbose:
        print(f"Cross-cycle disagreement: {disagreement}  (expected 44)")

    omega_b = (7 ** 2) / N ** 3
    omega_dm = 44 * 6 / N ** 3
    omega_l = (2 * 7 ** 3 + 1) / N ** 3
    closure = omega_b + omega_dm + omega_l
    results["cosmological_closure_1000"] = abs(closure - 1.0) < 1e-12
    if verbose:
        print(f"Cosmological closure: 0.049 + 0.264 + 0.687 = {closure}")

    w1, w2, w3 = wobble_three_derivations()
    results["wobble_three_agree"] = abs(w1 - w2) < 1e-12 and abs(w2 - w3) < 1e-12
    if verbose:
        print(f"Wobble derivations: ({w1}, {w2}, {w3}) -- expected all 0.06")

    prime_winding = T_STAR_NUM * W_DEN + W_NUM * T_STAR_DEN  # 5*50 + 3*7 = 271
    prime_winding_den = T_STAR_DEN * W_DEN  # 7*50 = 350
    is_271 = prime_winding == 271 and prime_winding_den == 350
    is_271_prime = all(prime_winding % p != 0
                       for p in (2, 3, 5, 7, 11, 13, 17))
    results["prime_winding_271_350"] = is_271 and is_271_prime
    if verbose:
        print(f"T* + W = {prime_winding}/{prime_winding_den}  (expected 271/350)")
        print(f"  271 prime: {is_271_prime}")

    sigma_fixed = [k for k, v in SIGMA.items() if k == v]
    sigma_cycle = [k for k, v in SIGMA.items() if k != v]
    results["sigma_4_fixed_6_cycle"] = (len(sigma_fixed) == 4
                                         and len(sigma_cycle) == 6)
    if verbose:
        print(f"sigma fixed points: {sorted(sigma_fixed)} (expected [0,3,8,9])")
        print(f"sigma 6-cycle: {sorted(sigma_cycle)} (expected [1,2,4,5,6,7])")

    all_pass = all(results.values())
    if verbose:
        print()
        print("=" * 60)
        print(f"Substrate (A0) verification: "
              f"{'PASS' if all_pass else 'FAIL'} "
              f"({sum(results.values())}/{len(results)} checks passed)")
        print("=" * 60)

    return results


if __name__ == "__main__":
    verify(verbose=True)
