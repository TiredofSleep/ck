"""
D1 — First-G Law: first_g(b) = p for all semiprimes b = p*q.

Copyright © 2025–2026 Brayden Ross Sanders / 7SiTe LLC
Licensed under the 7SiTe Public Sovereignty License v1.0.
Human use only. No commercial use. No government use.
No military, intelligence, policing, or surveillance use.
See LICENSE for full terms. DOI: 10.5281/zenodo.18852047

Proved algebraically in WP34. The smallest k where gcd(k, b) > 1
equals p (the smaller prime factor) for every semiprime.
"""
import pytest
from fractions import Fraction
from tig_algebra import TIGSemiprime, verify_first_g


# Semiprimes organized by smallest prime factor
SEMIPRIMES_SPF2  = [6, 10, 14, 22, 26, 34, 38, 46, 58, 62, 74, 82, 86, 94]
SEMIPRIMES_SPF3  = [15, 21, 33, 39, 51, 57, 69, 87, 93, 111, 123, 129, 141, 159]
SEMIPRIMES_SPF5  = [35, 55, 65, 77, 85, 95, 115, 119, 143, 155, 161]
SEMIPRIMES_SPF7  = [77, 91, 119, 133, 161, 203, 217, 287, 301]
SEMIPRIMES_SPF11 = [121, 143, 187, 209, 253, 319, 341, 377, 407]
SEMIPRIMES_LARGE = [999983 * 999979, 9973 * 9967]  # large primes


class TestFirstGLaw:
    """D1: first_g(b) = p (smallest prime factor) for all semiprimes."""

    def test_spf2_family(self):
        result = verify_first_g(SEMIPRIMES_SPF2)
        assert result["failed"] == 0, f"SPF=2 failures: {result['failures']}"

    def test_spf3_family(self):
        result = verify_first_g(SEMIPRIMES_SPF3)
        assert result["failed"] == 0, f"SPF=3 failures: {result['failures']}"

    def test_spf5_family(self):
        result = verify_first_g(SEMIPRIMES_SPF5)
        assert result["failed"] == 0, f"SPF=5 failures: {result['failures']}"

    def test_spf7_family(self):
        result = verify_first_g(SEMIPRIMES_SPF7)
        assert result["failed"] == 0, f"SPF=7 failures: {result['failures']}"

    def test_spf11_family(self):
        result = verify_first_g(SEMIPRIMES_SPF11)
        assert result["failed"] == 0, f"SPF=11 failures: {result['failures']}"

    def test_canonical_cases(self):
        """Key anchor cases explicitly verified."""
        cases = [(15, 3), (35, 5), (77, 7), (143, 11), (221, 13), (323, 17)]
        for b, expected_p in cases:
            s = TIGSemiprime(b)
            assert s.first_g() == expected_p, (
                f"first_g({b}) = {s.first_g()}, expected {expected_p}"
            )
            assert s.p == expected_p, f"s.p({b}) = {s.p}, expected {expected_p}"

    def test_first_g_equals_smallest_factor(self):
        """first_g(b) = p always, not q, not any k < p."""
        for b in [6, 15, 35, 77, 143, 221, 323, 437, 667, 899]:
            s = TIGSemiprime(b)
            fg = s.first_g()
            assert fg == s.p, f"first_g({b}) = {fg}, but p = {s.p}"
            # Confirm no k < p has gcd > 1
            import math
            for k in range(1, fg):
                assert math.gcd(k, b) == 1, (
                    f"b={b}: gcd({k},{b})={math.gcd(k,b)} but first_g={fg}"
                )
