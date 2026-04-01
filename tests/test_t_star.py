"""
T* = 5/7 — Coherence threshold derived from b=35 (minimal strong semiprime).

Copyright © 2025–2026 Brayden Ross Sanders / 7SiTe LLC
Licensed under the 7SiTe Public Sovereignty License v1.0.
Human use only. No commercial use. No government use.
No military, intelligence, policing, or surveillance use.
See LICENSE for full terms. DOI: 10.5281/zenodo.18852047

T* = (q - floor(q/p) - 1) / q. For b=35: (7 - 1 - 1)/7 = 5/7.
"""
import pytest
from fractions import Fraction
from tig_algebra import TIGSemiprime, T_STAR_EXACT


class TestTStarDerivation:
    """T* = 5/7 is the coherence threshold at the minimal balanced semiprime."""

    def test_t_star_exact_value(self):
        """T* = 5/7 as an exact fraction."""
        assert T_STAR_EXACT == Fraction(5, 7), (
            f"T_STAR_EXACT = {T_STAR_EXACT}, expected 5/7"
        )

    def test_t_star_at_b35(self):
        """T* = 5/7 derived from b=35 (p=5, q=7)."""
        s = TIGSemiprime(35)
        assert s.unit_frac() == Fraction(5, 7)

    def test_unit_frac_formula(self):
        """unit_frac = (q - floor(q/p) - 1) / q for several semiprimes."""
        cases = [
            (15,   3,  5,  Fraction(3, 5)),
            (35,   5,  7,  Fraction(5, 7)),    # T* = 5/7
            (77,   7, 11,  Fraction(9, 11)),
            (143, 11, 13,  Fraction(11, 13)),
            (221, 13, 17,  Fraction(15, 17)),
        ]
        for b, p, q, expected in cases:
            s = TIGSemiprime(b)
            assert s.unit_frac() == expected, (
                f"unit_frac({b}={p}×{q}) = {s.unit_frac()}, expected {expected}"
            )

    def test_t_star_float_precision(self):
        """T* ≈ 0.71428571 — float representation."""
        import math
        assert abs(float(T_STAR_EXACT) - 5/7) < 1e-14

    def test_b35_is_minimal_strong_semiprime(self):
        """b=35 is the minimal semiprime with q/p ratio closest to 1 among small cases."""
        # For b=35: q/p = 7/5 = 1.4 (more balanced than b=15 at 5/3=1.667)
        b15 = TIGSemiprime(15)
        b35 = TIGSemiprime(35)
        assert b35.q / b35.p < b15.q / b15.p, (
            "b=35 should be more balanced (smaller q/p ratio) than b=15"
        )
        assert b35.unit_frac() == Fraction(5, 7)
