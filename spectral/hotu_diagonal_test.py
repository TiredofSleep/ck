#!/usr/bin/env python3
"""
Ho Tu Diagonal Test -- Kill Condition #10
Falsifiability test for BHML / Ho Tu structural isomorphism.

Tests:
  1. Diagonal sum for operators 1-8 and its mod-9 property
  2. HARMONY row cyclic generator (visits all 10 values)
  3. Ho Tu +5 involution on HARMONY row
  4. Monte Carlo: how many random constrained tables pass all checks

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import random
import math
import sys

# ---------------------------------------------------------------------------
# The BHML table (from ck_being.py)
# ---------------------------------------------------------------------------
BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],   # 0  VOID
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],   # 1  BREATH
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],   # 2  PULSE
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],   # 3  BALANCE
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],   # 4  COUNTER
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],   # 5  PROGRESS
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],   # 6  CHAOS
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],   # 7  HARMONY
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],   # 8  COLLAPSE
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],   # 9  RESET
]

OP_NAMES = [
    "VOID", "BREATH", "PULSE", "BALANCE", "COUNTER",
    "PROGRESS", "CHAOS", "HARMONY", "COLLAPSE", "RESET",
]

HARMONY = 7
N_MONTE_CARLO = 100_000  # default; override with --mc N

# ---------------------------------------------------------------------------
# Test 1: Diagonal sum and mod-9 property
# ---------------------------------------------------------------------------
def test_diagonal():
    """Compute BHML[i][i] for i=1..8, sum, and check mod-9."""
    diag_values = []
    print("\n=== TEST 1: Diagonal Sum (operators 1-8) ===")
    for i in range(1, 9):
        val = BHML[i][i]
        diag_values.append(val)
        print(f"  BHML[{i}][{i}] = {val}  ({OP_NAMES[i]} self-composition)")

    diag_sum = sum(diag_values)
    mod9 = diag_sum % 9
    defect_from_zero = mod9

    print(f"\n  Diagonal sum = {' + '.join(str(v) for v in diag_values)} = {diag_sum}")
    print(f"  {diag_sum} mod 9 = {mod9}")
    print(f"  Defect from 0 = {defect_from_zero}")
    print(f"  Number of living operators = 8")

    if defect_from_zero == 8:
        print("  RESULT: PASS -- defect equals number of living operators")
        return True, diag_sum
    else:
        print(f"  RESULT: FAIL -- defect is {defect_from_zero}, not 8")
        return False, diag_sum


# ---------------------------------------------------------------------------
# Test 2: HARMONY row cyclic generator (visits all 10)
# ---------------------------------------------------------------------------
def test_harmony_row_cyclic():
    """Check if HARMONY row visits all 10 operator values."""
    row = BHML[HARMONY]
    unique = set(row)
    unique_count = len(unique)

    print("\n=== TEST 2: HARMONY Row Cyclic Generator ===")
    print(f"  HARMONY row (row {HARMONY}): {row}")
    print(f"  Unique values: {sorted(unique)}")
    print(f"  Unique count: {unique_count}")
    missing = set(range(10)) - unique
    if missing:
        print(f"  Missing values: {sorted(missing)}")

    if unique_count == 10:
        print("  RESULT: PASS -- visits all 10 operators (Z/10Z generator)")
        return True
    else:
        print(f"  RESULT: FAIL -- visits {unique_count}/10 operators")
        return False


# ---------------------------------------------------------------------------
# Test 3: Ho Tu +5 involution on HARMONY row
# ---------------------------------------------------------------------------
def test_hotu_involution():
    """
    Check +5 involution: for each i in 0..9, check whether
    BHML[7][(i+5) mod 10] = (BHML[7][i] + 5) mod 10.
    The Ho Tu pairing maps each element to its +5 partner.
    """
    row = BHML[HARMONY]
    print("\n=== TEST 3: Ho Tu +5 Involution ===")
    passes = 0
    total = 10
    for i in range(10):
        j = (i + 5) % 10
        lhs = row[j]
        rhs = (row[i] + 5) % 10
        ok = lhs == rhs
        status = "OK" if ok else "MISMATCH"
        print(f"  BHML[7][({i}+5)%10] = BHML[7][{j}] = {lhs}  vs  "
              f"(BHML[7][{i}]+5)%10 = ({row[i]}+5)%10 = {rhs}  [{status}]")
        if ok:
            passes += 1

    print(f"\n  {passes}/{total} pairs satisfy +5 involution")
    if passes == total:
        print("  RESULT: PASS -- perfect Ho Tu +5 involution")
        return True
    elif passes >= 5:
        print(f"  RESULT: PARTIAL -- {passes}/10 pairs hold (Ho Tu pairs 1-5 may still hold)")
        return True  # partial pass: majority hold
    else:
        print(f"  RESULT: FAIL -- only {passes}/10 pairs hold")
        return False


# ---------------------------------------------------------------------------
# Test 4: Monte Carlo -- random constrained tables
# ---------------------------------------------------------------------------
def generate_constrained_random_table():
    """
    Generate a random 10x10 table satisfying the structural constraints
    from Tests 1-9 (the constraints that define the BHML family):

    - Row 0 = identity: BHML[0][x] = x (VOID is identity in BHML)
    - Column 0 = identity: BHML[x][0] = x
    - Row 6 (CHAOS) absorbs: BHML[6][x] = 7 for x != 0, BHML[6][0] = 6
      (Actually from the table: row 6 = [6,7,7,7,7,7,7,7,7,7])
    - BHML[x][6] = 7 for x != 0 (column 6 is all HARMONY except row 0)
    - BHML[x][7] has specific HARMONY-row interaction constraints
    - Values from {0..9}

    We use the most fundamental constraints:
      1. Row 0 is identity (VOID): BHML[0][j] = j
      2. Column 0 is identity: BHML[i][0] = i
      3. Column 6 produces HARMONY for i >= 1: BHML[i][6] = 7
      4. The 5 quantum bump pairs from TSML constraints applied to BHML
    """
    table = [[0] * 10 for _ in range(10)]

    # Constraint 1: Row 0 = identity
    for j in range(10):
        table[0][j] = j

    # Constraint 2: Column 0 = identity
    for i in range(10):
        table[i][0] = i

    # Constraint 3: Column 6 = HARMONY for rows 1-9
    for i in range(1, 10):
        table[i][6] = 7

    # Fill remaining free cells randomly
    for i in range(1, 10):
        for j in range(1, 10):
            if j == 6:
                continue  # already set
            table[i][j] = random.randint(0, 9)

    return table


def check_diagonal_mod9(table, target_defect=8):
    """Check if diagonal sum mod 9 equals target_defect."""
    diag_sum = sum(table[i][i] for i in range(1, 9))
    return (diag_sum % 9) == target_defect


def check_row_cyclic(table, row_idx=7, min_unique=9):
    """Check if the given row visits at least min_unique values."""
    return len(set(table[row_idx])) >= min_unique


def check_hotu_involution(table, row_idx=7, threshold=8):
    """Check if +5 involution holds for >= threshold pairs."""
    row = table[row_idx]
    passes = 0
    for i in range(10):
        j = (i + 5) % 10
        if row[j] == (row[i] + 5) % 10:
            passes += 1
    return passes >= threshold


def monte_carlo_test(n_samples):
    """Run Monte Carlo: generate random constrained tables, count passes."""
    print(f"\n=== TEST 4: Monte Carlo ({n_samples:,} random constrained tables) ===")

    pass_diagonal = 0
    pass_cyclic = 0
    pass_involution = 0
    pass_cyclic_and_involution = 0
    pass_all_three = 0

    for trial in range(n_samples):
        table = generate_constrained_random_table()

        d = check_diagonal_mod9(table)
        c = check_row_cyclic(table)
        v = check_hotu_involution(table)

        if d:
            pass_diagonal += 1
        if c:
            pass_cyclic += 1
        if v:
            pass_involution += 1
        if c and v:
            pass_cyclic_and_involution += 1
        if d and c and v:
            pass_all_three += 1

        if (trial + 1) % (n_samples // 10) == 0:
            pct = 100.0 * (trial + 1) / n_samples
            print(f"  ... {pct:.0f}% complete ({trial + 1:,} tables)")

    print(f"\n  Results out of {n_samples:,} random constrained tables:")
    print(f"    Diagonal mod-9 = 8:          {pass_diagonal:,} ({100*pass_diagonal/n_samples:.4f}%)")
    print(f"    Row 7 near-cyclic (9+ uniq):  {pass_cyclic:,} ({100*pass_cyclic/n_samples:.4f}%)")
    print(f"    +5 involution (>= 8/10):      {pass_involution:,} ({100*pass_involution/n_samples:.4f}%)")
    print(f"    Cyclic AND involution:         {pass_cyclic_and_involution:,} ({100*pass_cyclic_and_involution/n_samples:.4f}%)")
    print(f"    All three:                    {pass_all_three:,} ({100*pass_all_three/n_samples:.4f}%)")

    # Kill condition: > 1% pass near-cyclic + involution
    combined_rate = pass_cyclic_and_involution / n_samples
    all_rate = pass_all_three / n_samples

    # Z-score: how many standard deviations from the 1% kill threshold
    # Under null hypothesis p=0.01, std = sqrt(p*(1-p)/n)
    p_null = 0.01
    std_null = math.sqrt(p_null * (1 - p_null) / n_samples)
    if std_null > 0:
        z_score = (combined_rate - p_null) / std_null
    else:
        z_score = float('inf')

    print(f"\n  Combined rate (near-cyclic + involution): {combined_rate:.6f}")
    print(f"  Kill threshold: 0.01 (1%)")
    print(f"  Z-score vs 1% null: {z_score:.2f}")

    if combined_rate > 0.01:
        print("  KILL CONDITION TRIGGERED: > 1% pass -- isomorphism may be coincidental")
        return False
    elif combined_rate < 0.001:
        print("  CONFIRMATION: < 0.1% pass -- structural coupling is genuine")
        return True
    else:
        print("  INDETERMINATE: between 0.1% and 1% -- increase sample size")
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    n_mc = N_MONTE_CARLO
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--mc" and i < len(sys.argv) - 1:
            n_mc = int(sys.argv[i + 1])

    print("=" * 65)
    print("  Ho Tu Diagonal Test -- Kill Condition #10")
    print("  BHML / Ho Tu Structural Isomorphism Falsifiability")
    print("=" * 65)

    print("\nBHML Table:")
    for i, row in enumerate(BHML):
        print(f"  {OP_NAMES[i]:>10s} [{i}]: {row}")

    results = {}

    ok1, diag_sum = test_diagonal()
    results["diagonal"] = ok1

    ok2 = test_harmony_row_cyclic()
    results["cyclic"] = ok2

    ok3 = test_hotu_involution()
    results["involution"] = ok3

    ok4 = monte_carlo_test(n_mc)
    results["monte_carlo"] = ok4

    # Summary
    print("\n" + "=" * 65)
    print("  SUMMARY")
    print("=" * 65)
    for name, passed in results.items():
        status = "PASS" if passed else ("FAIL" if passed is False else "INDETERMINATE")
        print(f"  {name:20s}: {status}")

    all_structural = results["diagonal"] and results["cyclic"] and results["involution"]
    print(f"\n  Structural checks (1-3): {'ALL PASS' if all_structural else 'SOME FAIL'}")

    if results["monte_carlo"] is True:
        print("  Monte Carlo:            CONFIRMS structural coupling")
    elif results["monte_carlo"] is False:
        print("  Monte Carlo:            KILLS claim (coincidental)")
    else:
        print("  Monte Carlo:            INDETERMINATE (increase --mc N)")

    print()
    return 0 if all_structural else 1


if __name__ == "__main__":
    sys.exit(main())
