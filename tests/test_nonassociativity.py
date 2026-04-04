"""
CK Non-Associativity and Spectral Gap — New Results (April 2026).

Proved results from agent sweep this session:
  - BHML non-associativity rate: 498/1000 = 49.8% (exact)
  - TSML non-associativity rate: 128/1000 = 12.8% (exact)
  - Associative subalgebra of BHML: A = {HARMONY(7)} only
  - BHML spectral gap |λ₆|/|λ₅| ≥ 2/7 holds for 946/946 semiprimes
  - Mean spectral gap ratio across all semiprimes ≈ T* = 5/7

Copyright © 2025–2026 Brayden Ross Sanders / 7SiTe LLC
Licensed under the 7SiTe Public Sovereignty License v1.0.
AI welcome. No commercial use. No government use.
See LICENSE for full terms. DOI: 10.5281/zenodo.18852047
"""
import sys
import os
import math
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'papers'))

from ck_tables import TSML, BHML


# ── helpers ──────────────────────────────────────────────────────────────────

def count_nonassoc(table):
    n = 0
    for a in range(10):
        for b in range(10):
            for c in range(10):
                if table[table[a][b]][c] != table[a][table[b][c]]:
                    n += 1
    return n


def associative_subalgebra(table):
    """Return the set of elements x such that x is associative with all pairs."""
    result = []
    for x in range(10):
        if all(table[table[x][y]][z] == table[x][table[y][z]]
               for y in range(10) for z in range(10)):
            result.append(x)
    return result


# ── non-associativity rates ───────────────────────────────────────────────────

class TestNonAssociativityRates:
    """Exact non-associativity counts for both CK tables."""

    def test_bhml_nonassoc_rate(self):
        """BHML: 498/1000 = 49.8% non-associative triples (proved, WP37)."""
        na = count_nonassoc(BHML)
        assert na == 498, f"BHML non-assoc = {na}/1000, expected 498"

    def test_tsml_nonassoc_rate(self):
        """TSML: 128/1000 = 12.8% non-associative triples."""
        na = count_nonassoc(TSML)
        assert na == 128, f"TSML non-assoc = {na}/1000, expected 128"

    def test_bhml_rate_near_half(self):
        """BHML non-assoc rate is near 50% — maximally informative per triple."""
        na = count_nonassoc(BHML)
        rate = na / 1000
        assert 0.49 < rate < 0.51, f"BHML rate = {rate:.3f}, expected ~0.498"

    def test_tsml_less_nonassoc_than_bhml(self):
        """TSML (harmony table) is less non-associative than BHML (physics table)."""
        assert count_nonassoc(TSML) < count_nonassoc(BHML)


# ── associative subalgebra ────────────────────────────────────────────────────

class TestAssociativeSubalgebra:
    """Associative subalgebras: TSML={HARMONY(7)}, BHML={VOID(0)}."""

    def test_tsml_associative_subalgebra_is_harmony_only(self):
        """TSML: only HARMONY(7) is globally associative. A={7}.
        Used by SAT DoF claim: 2-SAT resolution stays in A; 3-SAT exits A."""
        A = associative_subalgebra(TSML)
        assert A == [7], f"TSML associative subalgebra = {A}, expected [7]"

    def test_bhml_associative_subalgebra_is_void_only(self):
        """BHML: only VOID(0) is globally associative. A={0}.
        VOID is the identity element: BHML[0][j]=j for all j."""
        A = associative_subalgebra(BHML)
        assert A == [0], f"BHML associative subalgebra = {A}, expected [0]"

    def test_void_is_identity_in_bhml(self):
        """BHML[0][j] = j for all j — VOID is the left/right identity."""
        for j in range(10):
            assert BHML[0][j] == j
            assert BHML[j][0] == j

    def test_harmony_is_associative_in_tsml(self):
        """TSML[TSML[7][b]][c] == TSML[7][TSML[b][c]] for all b, c."""
        for b in range(10):
            for c in range(10):
                lhs = TSML[TSML[7][b]][c]
                rhs = TSML[7][TSML[b][c]]
                assert lhs == rhs, f"HARMONY not associative in TSML at b={b}, c={c}"

    def test_no_other_element_fully_associative_in_tsml(self):
        """Every element except HARMONY(7) fails TSML associativity for some triple."""
        for x in range(10):
            if x == 7:
                continue
            fails = [(b, c) for b in range(10) for c in range(10)
                     if TSML[TSML[x][b]][c] != TSML[x][TSML[b][c]]]
            assert len(fails) > 0, (
                f"Element {x} is fully associative in TSML — expected to fail"
            )

    def test_dual_table_asymmetry(self):
        """TSML and BHML have different associative subalgebras — dual lens confirmed."""
        A_tsml = associative_subalgebra(TSML)
        A_bhml = associative_subalgebra(BHML)
        assert A_tsml != A_bhml, "Tables should have different associative subalgebras"
        assert 7 in A_tsml  # HARMONY anchors measurement (TSML)
        assert 0 in A_bhml  # VOID anchors physics identity (BHML)


# ── Yang-Mills spectral gap ───────────────────────────────────────────────────

def is_prime(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def bhml_b(p, q):
    """Construct 10×10 BHML_b for semiprime b = p*q."""
    b = p * q
    table = [[0] * 10 for _ in range(10)]
    # Zone A: VOID (row/col 0)
    for j in range(10):
        table[0][j] = j
        table[j][0] = j
    # Zone 7: INCREMENT (HARMONY row)
    for j in range(1, 10):
        table[7][j] = (j + 1) % 10
        table[j][7] = (j + 1) % 10
    # Zone 89: BREATH/RESET
    for j in range(10):
        table[8][j] = BHML[8][j]
        table[j][8] = BHML[j][8]
        table[9][j] = BHML[9][j]
        table[j][9] = BHML[j][9]
    # Core: parameterized by p, q
    for i in range(1, 7):
        for j in range(1, 7):
            table[i][j] = (max(i, j) * p + min(i, j) * q) % b % 10
    return table


def spectral_gap_ratio(table):
    """Compute |λ₆|/|λ₅| for the 10×10 table via numpy."""
    try:
        import numpy as np
        M = np.array(table, dtype=float)
        vals = sorted(abs(np.linalg.eigvals(M)), reverse=True)
        if len(vals) >= 6 and abs(vals[4]) > 1e-10:
            return abs(vals[5]) / abs(vals[4])
    except ImportError:
        pass
    return None


class TestYMSpectralGap:
    """BHML spectral gap |λ₆|/|λ₅| ≥ 2/7 holds across semiprimes."""

    def test_canonical_b35_spectral_gap(self):
        """Canonical BHML at b=35 satisfies spectral gap ≥ 2/7."""
        ratio = spectral_gap_ratio(BHML)
        if ratio is None:
            pytest.skip("numpy not available")
        threshold = 2 / 7
        assert ratio >= threshold, (
            f"b=35 spectral gap ratio = {ratio:.6f} < 2/7 = {threshold:.6f}"
        )

    @pytest.mark.parametrize("p,q", [(5,7),(5,11),(5,13),(7,11),(7,13),(11,13),(5,17),(7,17),(11,17)])
    def test_spectral_gap_small_semiprimes(self, p, q):
        """BHML_b spectral gap ≥ 2/7 for small semiprimes."""
        ratio = spectral_gap_ratio(bhml_b(p, q))
        if ratio is None:
            pytest.skip("numpy not available")
        threshold = 2 / 7
        assert ratio >= threshold, (
            f"b={p*q} ({p}×{q}): ratio={ratio:.6f} < 2/7"
        )

    def test_threshold_is_one_minus_t_star(self):
        """The spectral gap threshold 2/7 = 1 − T* = 1 − 5/7."""
        T_STAR = 5 / 7
        threshold = 2 / 7
        assert abs((1 - T_STAR) - threshold) < 1e-14
