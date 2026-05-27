"""verify_J58.py -- machine-precision verification of all six theorems of J58.

CC-BY-4.0. (c) 2026 Brayden Ross Sanders / 7Site LLC. M. Gish co-author.

Verifies:
  A. The Lo Shu D_4 orbit has 8 distinct elements.
  B. The mod-3 reductions of the 8 orbit elements yield exactly 4 distinct
     magma tables, each appearing twice in the orbit.
  C. The two non-commutative tables T_1 and T_3 are opposite magmas
     (T_3[x][y] = T_1[y][x] for all x, y).
  D. All four tables are quasigroups (every row and every column is a
     permutation of {0, 1, 2}).
  E. The matrix cumulant kappa(M) = Tr(M^2) - Tr(M)^2 takes exactly two
     values across the 8 orbit elements: -48 for the 4 elements whose
     mod-3 reduction is commutative, +48 for the 4 elements whose mod-3
     reduction is non-commutative.
  F. T_2 (one of the commutative tables) is exactly Z/3 (the cyclic
     group: T_2[x][y] = (x + y) mod 3).

Run:  python verify_J58.py
Runtime: under 1 second on a 2020-era laptop.
"""
from itertools import product
import numpy as np


# The Lo Shu magic square.
LO_SHU = np.array([
    [2, 7, 6],
    [9, 5, 1],
    [4, 3, 8],
], dtype=int)


def d4_orbit(M):
    """Generate the 8 elements of the D_4 orbit of M (as a list of np arrays).

    D_4 = {e, r, r^2, r^3, f, rf, r^2 f, r^3 f}, where r = 90-deg rotation
    and f = horizontal flip. We use numpy's rot90 and fliplr.
    """
    orbit = []
    seen = set()
    for k in range(4):
        for flip in (False, True):
            B = np.rot90(M, k)
            if flip:
                B = np.fliplr(B)
            key = tuple(B.flatten().tolist())
            if key not in seen:
                seen.add(key)
                orbit.append(B.copy())
    return orbit


def magma_table_of(M):
    """Return the 3x3 mod-3 magma table of M as a tuple of tuples."""
    return tuple(tuple(int(M[x][y]) % 3 for y in range(3)) for x in range(3))


def is_commutative(table):
    n = len(table)
    return all(table[x][y] == table[y][x]
               for x in range(n) for y in range(n))


def is_quasigroup(table):
    n = len(table)
    s = set(range(n))
    rows_ok = all(set(table[x]) == s for x in range(n))
    cols_ok = all(set(table[x][y] for x in range(n)) == s
                  for y in range(n))
    return rows_ok and cols_ok


def cumulant(M):
    """Tr(M^2) - Tr(M)^2 for a real square matrix M."""
    A = np.array(M, dtype=float)
    A2 = A @ A
    return float(np.trace(A2) - np.trace(A) ** 2)


def opposite_magma(table):
    """Return T'[x][y] = T[y][x]."""
    n = len(table)
    return tuple(tuple(table[y][x] for y in range(n)) for x in range(n))


# ============================================================================

def main():
    print("=" * 64)
    print(" J58 verification -- Lo Shu D_4 orbit mod 3")
    print("=" * 64)
    print()

    orbit = d4_orbit(LO_SHU)
    checks = []

    # CHECK 1 (Theorem A: orbit has 8 distinct elements)
    n_orbit = len(orbit)
    checks.append(("Theorem A (orbit has 8 distinct elements)",
                   n_orbit == 8))

    # Compute the four-table refinement
    tables_seen = {}
    for i, M in enumerate(orbit):
        t = magma_table_of(M)
        if t not in tables_seen:
            tables_seen[t] = {
                "indices": [],
                "is_commutative": is_commutative(t),
                "is_quasigroup": is_quasigroup(t),
                "cumulants": [],
            }
        tables_seen[t]["indices"].append(i)
        tables_seen[t]["cumulants"].append(cumulant(M))

    # CHECK 2 (Theorem B: 4 distinct tables, each appearing twice)
    n_tables = len(tables_seen)
    multiplicities = sorted(len(info["indices"])
                            for info in tables_seen.values())
    checks.append((
        "Theorem B (4 distinct mod-3 tables, each x2)",
        n_tables == 4 and multiplicities == [2, 2, 2, 2]
    ))

    # Sort tables for stable labeling: T_2 = Z/3 first by convention,
    # then by (is_commutative_desc, table_lex_order)
    Z3_table = tuple(tuple((x + y) % 3 for y in range(3))
                     for x in range(3))

    # Find T_2 = Z/3
    z3_present = Z3_table in tables_seen
    # CHECK 6 (Theorem F: Z/3 is in the orbit)
    checks.append(("Theorem F (Z/3 cyclic group is one of the tables)",
                   z3_present))

    # CHECK 4 (Theorem D: all 4 tables are quasigroups)
    all_quasi = all(info["is_quasigroup"]
                    for info in tables_seen.values())
    checks.append(("Theorem D (all 4 tables are quasigroups)", all_quasi))

    # CHECK 5 (Theorem E: cumulant +/-48 separates commutativity)
    epsilon = 1e-9
    correlation_ok = True
    for info in tables_seen.values():
        for c in info["cumulants"]:
            if info["is_commutative"]:
                if abs(c - (-48.0)) > epsilon:
                    correlation_ok = False
            else:
                if abs(c - 48.0) > epsilon:
                    correlation_ok = False
    checks.append((
        "Theorem E (cumulant +/-48 separates commutativity)",
        correlation_ok
    ))

    # CHECK 3 (Theorem C: the two non-commutative tables are opposites)
    non_comm_tables = [t for t, info in tables_seen.items()
                       if not info["is_commutative"]]
    if len(non_comm_tables) == 2:
        T_a, T_b = non_comm_tables
        opposite_pair = (opposite_magma(T_a) == T_b)
    else:
        opposite_pair = False
    checks.append((
        "Theorem C (two non-comm tables are opposite magmas)",
        opposite_pair
    ))

    # Print results
    n_pass = 0
    print("Detailed checks:")
    for i, (name, ok) in enumerate(checks, start=1):
        status = "PASS" if ok else "FAIL"
        if ok:
            n_pass += 1
        print(f"  CHECK {i} ({name}): {status}")

    print()
    print(f"  Overall: {'PASS' if n_pass == len(checks) else 'FAIL'} "
          f"({n_pass}/{len(checks)})")

    # Display the 4 tables for the manuscript appendix
    print()
    print("-" * 64)
    print(" Detailed orbit information")
    print("-" * 64)
    print()
    print(f"  Orbit size: {n_orbit}")
    print(f"  Distinct mod-3 tables: {n_tables}")
    print()
    for j, (t, info) in enumerate(tables_seen.items(), start=1):
        cums = set(round(c, 6) for c in info["cumulants"])
        is_z3 = (t == Z3_table)
        labels = []
        labels.append("COMMUTATIVE" if info["is_commutative"]
                      else "NON-COMMUTATIVE")
        labels.append("QUASIGROUP" if info["is_quasigroup"]
                      else "NOT-QUASIGROUP")
        if is_z3:
            labels.append("== Z/3")
        labels_s = ", ".join(labels)
        print(f"  Table T{j}  ({labels_s})")
        print(f"    orbit indices: {info['indices']}")
        print(f"    cumulants: {sorted(cums)}")
        for row in t:
            print("    " + "  ".join(f"{v}" for v in row))
        print()

    # The full kappa table across orbit elements
    print("  Per-orbit-element cumulants:")
    for i, M in enumerate(orbit):
        t = magma_table_of(M)
        com_tag = "C" if tables_seen[t]["is_commutative"] else "N"
        print(f"    orbit[{i}]: cumulant = {cumulant(M):+.0f} ({com_tag})")

    return n_pass == len(checks)


if __name__ == "__main__":
    ok = main()
    raise SystemExit(0 if ok else 1)
