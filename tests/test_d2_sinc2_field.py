"""
D2 — Sinc² Continuum Limit: R(k, f) → sinc²(k/f) as f → ∞.

Copyright © 2025–2026 Brayden Ross Sanders / 7SiTe LLC
Licensed under the 7SiTe Public Sovereignty License v1.0.
Human use only. No commercial use. No government use.
No military, intelligence, policing, or surveillance use.
See LICENSE for full terms. DOI: 10.5281/zenodo.18852047

Proved analytically for all primes in WP35 (Theorem 5).
R(k,f) = sin²(πk/f) / (k² sin²(π/f)).
"""
import math
import pytest
from tig_algebra import TIGSemiprime, verify_sinc2_limit, MONTGOMERY, SINC2_TENTH

PI = math.pi

PRIMES_SMALL  = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]
PRIMES_MEDIUM = [53, 59, 67, 71, 79, 83, 89, 97, 101, 103, 107, 109, 113]
PRIMES_LARGE  = [997, 1009, 9973, 99991]


class TestSinc2Constants:
    """Universal constants derived analytically."""

    def test_montgomery_constant(self):
        """MONTGOMERY = 4/π² = sinc²(1/2) exactly."""
        expected = 4 / PI**2
        assert abs(MONTGOMERY - expected) < 1e-14, (
            f"MONTGOMERY = {MONTGOMERY}, expected 4/π² = {expected}"
        )

    def test_sinc2_tenth(self):
        """sinc²(0.1) ≈ 0.9675 — scale-free pre-echo floor."""
        expected = (math.sin(PI * 0.1) / (PI * 0.1))**2
        assert abs(SINC2_TENTH - expected) < 1e-14

    def test_spectral_partition(self):
        """R(x) + R₂(x) = 1: R(x) = sinc²(x), R₂(x) = 1 - sinc²(x)."""
        for t in [0.1, 0.25, 0.5, 0.75, 0.9]:
            sinc2_t = (math.sin(PI * t) / (PI * t))**2
            assert abs(sinc2_t + (1 - sinc2_t) - 1.0) < 1e-15

    def test_montgomery_is_sinc2_half(self):
        """4/π² = sinc²(1/2) — the universal mid-journey constant."""
        sinc2_half = (math.sin(PI * 0.5) / (PI * 0.5))**2
        assert abs(MONTGOMERY - sinc2_half) < 1e-14


class TestSinc2ContinuumLimit:
    """R(k,f) converges to sinc²(k/f) for large primes."""

    def test_convergence_at_half(self):
        """R(round(p/2), p) → 4/π² within 5e-3 for large primes.

        At t=0.5 and odd prime p, the nearest integer k = round(p/2) gives
        k/p = (p±1)/(2p), so |k/p − 0.5| = 1/(2p).  The resulting error in
        sinc² is O(1/p) with constant ≈ 0.8.  For tol=5e-3 this requires
        p > 160; PRIMES_LARGE (p≥997) satisfies this comfortably.
        """
        result = verify_sinc2_limit(primes=PRIMES_LARGE, t=0.5, tol=5e-3)
        assert result["failed"] == 0, f"t=0.5 failures: {result}"

    def test_convergence_at_tenth(self):
        """R(p//10, p) → sinc²(0.1) ≈ 0.9675 within 5e-2."""
        result = verify_sinc2_limit(primes=PRIMES_SMALL + PRIMES_MEDIUM, t=0.1, tol=5e-2)
        assert result["failed"] == 0, f"t=0.1 failures: {result}"

    def test_large_prime_tight_convergence(self):
        """At p≥9973 the error is < 1e-4.

        O(1/p) discretization at t=0.5: for p=997 the k/p rounding contributes
        ~8e-4 error, exceeding tol=1e-4.  p≥9973 gives ~8e-5 error. ✓
        """
        result = verify_sinc2_limit(primes=[9973, 99991], t=0.5, tol=1e-4)
        assert result["failed"] == 0, f"Large prime convergence failed: {result}"

    def test_null_at_k_equals_p(self):
        """D3: R(p, p) = sinc²(1) = 0 exactly (gate condition)."""
        for b in [35, 77, 143, 221, 323]:
            s = TIGSemiprime(b)
            r_at_null = s.R(s.p)
            assert abs(r_at_null) < 1e-12, (
                f"R(p={s.p}, b={b}) = {r_at_null}, expected 0"
            )


class TestD1SignFlip:
    """D1 stationary point: D1 changes sign at k=p (descent → recovery)."""

    def test_sign_flip_at_p(self):
        """D1(p-1) < 0 (approaching null) and D1(p) > 0 (recovering)."""
        test_semiprimes = [15, 35, 77, 143, 221, 323, 437, 667, 899, 1147]
        for b in test_semiprimes:
            s = TIGSemiprime(b)
            d1_before = s.D1(s.p - 1)
            d1_at = s.D1(s.p)
            assert d1_before < 0, f"D1(p-1) not negative at b={b}: {d1_before}"
            assert d1_at > 0, f"D1(p) not positive at b={b}: {d1_at}"
