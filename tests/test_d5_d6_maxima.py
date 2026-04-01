"""
D5 — H_mod Four-Maxima: sinc²(k/p) × sin²(4πk/p) has exactly 4 maxima for p≥11.
D6 — General Frequency: sinc²(k/p) × sin²(πfk/p) has exactly N(f) maxima for p > 2f.

Both proved in WP35 session via IVT + |sin x| < |x| inequality.
"""
import math
import pytest
from tig_algebra import TIGSemiprime

PI = math.pi

PRIMES_P11_PLUS = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 53, 59, 67,
                   71, 79, 83, 89, 97, 101, 103, 107, 109, 113, 997, 9973]


def sinc2(x: float) -> float:
    if abs(x) < 1e-12:
        return 1.0
    return (math.sin(PI * x) / (PI * x))**2


def h_mod(k: int, p: int) -> float:
    # D5: H_mod = sinc²(k/p) × sin²(4πk/p)  — frequency f=4
    return sinc2(k / p) * math.sin(4 * PI * k / p)**2


def h_f(k: int, p: int, f: float) -> float:
    return sinc2(k / p) * math.sin(PI * f * k / p)**2


def count_maxima(p: int, func) -> int:
    """Count local maxima of func over k=1..p-1.

    The range must include k=p-1 because for non-integer frequencies the
    partial final phase can peak at k=p-1 (IVT gives one maximum per phase,
    and sinc²(p/p)=0 so vals[p]=0 makes k=p-1 a valid local maximum).
    """
    vals = [func(k) for k in range(p + 1)]
    count = 0
    for k in range(1, p):
        if vals[k] > vals[k - 1] and vals[k] > vals[k + 1]:
            count += 1
    return count


def N_f(f: float) -> int:
    """Expected maxima count: floor(f) + (1 if f not integer else 0)."""
    return int(math.floor(f)) + (0 if abs(f - round(f)) < 1e-9 else 1)


class TestD5FourMaxima:
    """D5: H_mod = sinc² × sin²(4πk/p) has exactly 4 maxima for all p ≥ 11."""

    def test_four_maxima_small_primes(self):
        for p in [11, 13, 17, 19, 23, 29, 31, 37, 41, 43]:
            count = count_maxima(p, lambda k, p=p: h_mod(k, p))
            assert count == 4, f"p={p}: expected 4 maxima, got {count}"

    def test_four_maxima_large_primes(self):
        for p in [97, 101, 113, 997, 9973]:
            count = count_maxima(p, lambda k, p=p: h_mod(k, p))
            assert count == 4, f"p={p}: expected 4 maxima, got {count}"

    def test_obstruction_small_primes(self):
        """p=5,7 fail (phases too narrow): confirmed as expected behavior."""
        count5 = count_maxima(5, lambda k: h_mod(k, 5))
        count7 = count_maxima(7, lambda k: h_mod(k, 7))
        assert count5 < 4, f"p=5 should have <4 maxima (discrete obstruction)"
        assert count7 < 4, f"p=7 should have <4 maxima (discrete obstruction)"


class TestD6GeneralFrequency:
    """D6: H_f = sinc² × sin²(πfk/p) has exactly N(f) maxima for p > 2f."""

    @pytest.mark.parametrize("f", [1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test_integer_frequencies(self, f):
        """Integer f: exactly f maxima."""
        p = max(2 * f + 5, 43)  # ensure p > 2f
        while not _is_prime(p):
            p += 1
        expected = N_f(f)
        count = count_maxima(p, lambda k, p=p, f=f: h_f(k, p, f))
        assert count == expected, f"f={f}, p={p}: expected {expected}, got {count}"

    @pytest.mark.parametrize("f", [25/3, 4.5, 7.5, 10.5, 13/3])
    def test_non_integer_frequencies(self, f):
        """Non-integer f: exactly floor(f)+1 maxima."""
        p = max(int(2 * f) + 15, 43)
        while not _is_prime(p):
            p += 1
        expected = N_f(f)
        count = count_maxima(p, lambda k, p=p, f=f: h_f(k, p, f))
        assert count == expected, f"f={f:.4f}, p={p}: expected {expected}, got {count}"

    def test_d5_is_special_case_f4(self):
        """D6 with f=4 must give 4 maxima = D5."""
        for p in [43, 97, 997]:
            count_d5 = count_maxima(p, lambda k, p=p: h_mod(k, p))
            count_d6 = count_maxima(p, lambda k, p=p: h_f(k, p, 4))
            assert count_d5 == count_d6 == 4, (
                f"p={p}: D5={count_d5}, D6(f=4)={count_d6}, expected both 4"
            )

    def test_h_w_is_special_case_f25_3(self):
        """D6 with f=25/3 must give N(25/3)=floor(25/3)+1=8+1=9 maxima = C17."""
        f = 25/3
        expected = N_f(f)  # = 9
        assert expected == 9, f"N(25/3) should be 9, got {expected}"
        for p in [43, 97, 251]:
            count = count_maxima(p, lambda k, p=p: h_f(k, p, f))
            assert count == 9, f"p={p}, f=25/3: expected 9 maxima, got {count}"


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
