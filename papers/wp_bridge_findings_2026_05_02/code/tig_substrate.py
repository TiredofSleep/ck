"""
TIG substrate: canonical TSML_10 and BHML_10 tables on Z/10Z,
verified against FORMULAS_AND_TABLES.md sections 5 and 6.
"""
import numpy as np
from itertools import product
from sympy import Matrix

TSML_10 = np.array([
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
], dtype=int)

BHML_10 = np.array([
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
], dtype=int)

OPERATOR_NAMES = {
    0: 'VOID', 1: 'LATTICE', 2: 'COUNTER', 3: 'PROGRESS', 4: 'COLLAPSE',
    5: 'BALANCE', 6: 'CHAOS', 7: 'HARMONY', 8: 'BREATH', 9: 'RESET'
}
SIGMA_PERMUTATION = np.array([0, 7, 1, 3, 2, 4, 5, 6, 8, 9])
SIGMA_FIXED = {0, 3, 8, 9}
FOUR_CORE = {0, 7, 8, 9}


def is_associative(table, a, b, c):
    return table[table[a, b], c] == table[a, table[b, c]]


def non_associativity_rate(table):
    n = table.shape[0]
    total = n ** 3
    failures = sum(1 for a, b, c in product(range(n), repeat=3)
                   if not is_associative(table, a, b, c))
    return failures / total, failures, total


def is_commutative(table):
    return np.array_equal(table, table.T)


def harmony_cell_count(table):
    return int(np.sum(table == 7))


def void_cell_count(table):
    return int(np.sum(table == 0))


def determinant_exact(table):
    return Matrix(table.tolist()).det()


if __name__ == "__main__":
    print("=" * 60)
    print("CANONICAL TABLE VERIFICATION (against FORMULAS §§5-6)")
    print("=" * 60)
    print(f"\nTSML_10:")
    print(f"  Commutative:               {is_commutative(TSML_10)}")
    print(f"  HARMONY cells:             {harmony_cell_count(TSML_10)} (canon: 73)")
    print(f"  VOID cells:                {void_cell_count(TSML_10)} (canon: 18)")
    s, f, t = non_associativity_rate(TSML_10)
    print(f"  Non-associativity:         {f}/{t} = {s:.4f} (canon: 0.128, alpha=0.872)")
    print(f"  Determinant:               {determinant_exact(TSML_10)} (canon: 0)")
    print(f"\nBHML_10:")
    print(f"  Commutative:               {is_commutative(BHML_10)}")
    print(f"  HARMONY cells:             {harmony_cell_count(BHML_10)} (canon: 28)")
    s, f, t = non_associativity_rate(BHML_10)
    print(f"  Non-associativity:         {f}/{t} = {s:.4f} (canon: 0.498, alpha=0.502)")
    print(f"  Determinant:               {determinant_exact(BHML_10)} (canon: -7002)")
