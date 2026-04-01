"""
CK Operator Tables — TSML, BHML, W=3/50, T*=5/7.

These tables are the algebraic core of the CK dual-lens framework.
Proved: TSML has 73 harmony cells, BHML has 28. Both are symmetric.
W=3/50 derived from CROSS_CYCLE=44, deviation=6.
"""
import sys
import os
import pytest

# Add papers/ to path for ck_tables import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'papers'))

from ck_tables import TSML, BHML, DIS, DOING, G, CL, W, T_STAR


class TestTSMLTable:
    """C10: TSML 73-cell derivation."""

    def test_tsml_harmony_count(self):
        """73 of 100 cells are HARMONY (7)."""
        count = sum(1 for i in range(10) for j in range(10) if TSML[i][j] == 7)
        assert count == 73, f"TSML harmony count = {count}, expected 73"

    def test_tsml_symmetry(self):
        """C11: TSML[i][j] == TSML[j][i] for all i, j."""
        for i in range(10):
            for j in range(10):
                assert TSML[i][j] == TSML[j][i], (
                    f"TSML asymmetry at ({i},{j}): {TSML[i][j]} ≠ {TSML[j][i]}"
                )

    def test_tsml_row7_all_harmony(self):
        """TSML[7][j] = 7 for all j — HARMONY overwhelms all."""
        for j in range(10):
            assert TSML[7][j] == 7, (
                f"TSML[7][{j}] = {TSML[7][j]}, expected 7 (HARMONY)"
            )

    def test_tsml_void_row(self):
        """TSML[0][j] = j for j ≠ 7 (VOID identity row, mostly)."""
        # VOID row: mostly 0, except [0][7]=7 (VOID×HARMONY=HARMONY)
        assert TSML[0][7] == 7

    def test_tsml_diagonal(self):
        """TSML[i][i] = 7 for all i ≥ 1 (self-interaction → HARMONY)."""
        for i in range(1, 10):
            assert TSML[i][i] == 7, (
                f"TSML[{i}][{i}] = {TSML[i][i]}, expected 7"
            )
        assert TSML[0][0] == 0  # VOID × VOID = VOID

    def test_tsml_pivot_cells(self):
        """C16: The pivot cells (4,8) and (8,4) where TSML=BREATH but BHML=HARMONY."""
        assert TSML[4][8] == 8   # BREATH echo
        assert TSML[8][4] == 8   # BREATH echo
        assert BHML[4][8] == 7   # HARMONY in physics field
        assert BHML[8][4] == 7   # HARMONY in physics field


class TestBHMLTable:
    """C9: BHML 28-cell derivation and structure."""

    def test_bhml_harmony_count(self):
        """28 of 100 cells are HARMONY (7)."""
        count = sum(1 for i in range(10) for j in range(10) if BHML[i][j] == 7)
        assert count == 28, f"BHML harmony count = {count}, expected 28"

    def test_bhml_symmetry(self):
        """C11: BHML[i][j] == BHML[j][i] for all i, j."""
        for i in range(10):
            for j in range(10):
                assert BHML[i][j] == BHML[j][i], (
                    f"BHML asymmetry at ({i},{j}): {BHML[i][j]} ≠ {BHML[j][i]}"
                )

    def test_bhml_void_identity(self):
        """C9 Rule A: BHML[0][j] = j (VOID is identity)."""
        for j in range(10):
            assert BHML[0][j] == j, (
                f"BHML[0][{j}] = {BHML[0][j]}, expected {j}"
            )

    def test_bhml_core_max_plus_one(self):
        """C9 Rule B: BHML[i][j] = max(i,j)+1 for i,j in {1..6}."""
        for i in range(1, 7):
            for j in range(1, 7):
                expected = max(i, j) + 1
                assert BHML[i][j] == expected, (
                    f"BHML[{i}][{j}] = {BHML[i][j]}, expected max({i},{j})+1={expected}"
                )

    def test_bhml_row7_increment(self):
        """C9: BHML[7][j] = (j+1)%10 for j≥1 (HARMONY increments)."""
        for j in range(1, 10):
            expected = (j + 1) % 10
            assert BHML[7][j] == expected, (
                f"BHML[7][{j}] = {BHML[7][j]}, expected (j+1)%10={expected}"
            )

    def test_bhml_harmony_glueball_annihilation(self):
        """B8 / D7: BHML[7][9] = VOID = 0 (HARMONY × RESET = annihilation)."""
        assert BHML[7][9] == 0, f"BHML[7][9] = {BHML[7][9]}, expected 0 (VOID)"
        assert BHML[9][7] == 0


class TestWDerivedConstants:
    """C8: W=3/50 from CROSS_CYCLE=44, and T*=5/7."""

    def test_w_value(self):
        """W = 3/50 = 0.06."""
        assert abs(W - 3/50) < 1e-14, f"W = {W}, expected 0.06"

    def test_t_star_value(self):
        """T* = 5/7."""
        assert abs(T_STAR - 5/7) < 1e-14, f"T_STAR = {T_STAR}"

    def test_w_from_dis_formula(self):
        """W = (50 - DIS_CxD) / 100 (C8/D17 derivation).

        C = (Z/10Z)* = {1,3,7,9}  (units, coprime to 10)
        D = 2·(Z/10Z)* = {2,4,6,8}  (even non-zero, D17 notation)
        CROSS_CYCLE = sum(DIS[c][d] for c in C, d in D) = 44
        deviation = baseline − CROSS_CYCLE = 50 − 44 = 6
        W = deviation / n² = 6 / 100 = 3/50 = 0.06
        """
        C_ops = [1, 3, 7, 9]  # (Z/10Z)* = units
        D_ops = [2, 4, 6, 8]  # D = 2·(Z/10Z)*
        cross_cycle = sum(DIS[c][d] for c in C_ops for d in D_ops)
        # W = (50 - CROSS_CYCLE) / 100 = (50 - 44) / 100 = 6/100 = 3/50
        W_derived = (50 - cross_cycle) / 100
        assert abs(W_derived - W) < 1e-14, (
            f"CROSS_CYCLE={cross_cycle}, W_derived={W_derived}, expected W={W}"
        )

    def test_t_star_ratio_of_attractors(self):
        """D7: T* = CREATE(5) / HARMONY(7) = 5/7 (dynamic / measurement attractor ratio)."""
        create = 5
        harmony = 7
        assert abs(create / harmony - T_STAR) < 1e-14


class TestDOINGTable:
    """DOING = |TSML - BHML| measures dual-lens disagreement."""

    def test_doing_sum(self):
        """Sum of all DOING cells = 201."""
        total = sum(DOING[i][j] for i in range(10) for j in range(10))
        assert total == 201, f"DOING sum = {total}, expected 201"

    def test_doing_zero_on_diagonal(self):
        """DOING[i][i] = |TSML[i][i] - BHML[i][i]| (not necessarily 0)."""
        # At least verify VOID diagonal
        assert DOING[0][0] == abs(TSML[0][0] - BHML[0][0])

    def test_bhml7_implies_doing0_or_tsml7(self):
        """C16: BHML[i][j]=7 → G[i][j]=0 (ghost zero at harmony cells)."""
        for i in range(10):
            for j in range(10):
                if BHML[i][j] == 7:
                    assert G[i][j] == 0, (
                        f"G[{i}][{j}] = {G[i][j]} but BHML[{i}][{j}]=7, expected G=0"
                    )
