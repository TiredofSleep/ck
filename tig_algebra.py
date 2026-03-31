"""
tig_algebra.py -- Canonical TIG Semiprime Algebra
==================================================
Brayden Ross Sanders / 7Site LLC
DOI: 10.5281/zenodo.18852047

Implements the algebraic structures proved in WP34 (First-G Law) and
WP35 (Prime Phase Transition / Sinc2 Field).

Core objects
------------
TIGSemiprime(b)              -- construct from a semiprime integer b = p x q
TIGSemiprime.from_params(p, q)  -- construct from factors directly

Core methods
------------
.R(k)          -- harmonic pre-echo resonance  sin2(pi*k/f) / (k2*sin2(pi/f))
.sinc2(t)      -- continuum sinc2(t) = (sin(pi*t)/(pi*t))2
.D1(k)         -- first difference R(k+1) - R(k)   [approach velocity]
.D2(k)         -- second difference R(k+1)-2R(k)+R(k-1)  [curvature]
.C(k)          -- coprime set {x in {1..k} : gcd(x,b)=1}
.G(k)          -- gate set    {x in {1..k} : gcd(x,b)>1}
.first_g()     -- First-G event: min k s.t. |G(k)| > 0  (= p, always)
.interleave(k) -- Luther interleave score in [0,1]
.unit_frac()   -- T* formula (q - floor(q/p) - 1) / q
.dispersion(k) -- Luther dispersion: |G(k)| x interleave(k)

Constants
---------
MONTGOMERY    = 4/pi2  -- sinc2(1/2) = Universal Sidelobe Amplitude
SINC2_TENTH   ~= 0.9675 -- sinc2(0.1) = scale-free pre-echo floor

Attribution
-----------
R(k,f), D1, D2, First-G Law, unit_frac, T*=5/7: Sanders / 7Site LLC
Interleave / dispersion conjecture: C.A. Luther
"""

import math
from fractions import Fraction
from typing import List, Tuple, Optional


# ---------------------------------------------------------------------------
# Module-level constants (WP35 §9, Theorem 5)
# ---------------------------------------------------------------------------

PI = math.pi

def _sinc2(t):
    """sinc2(t) = (sin(pi*t) / pi*t)2.  Returns 1.0 at t=0."""
    if abs(t) < 1e-15:
        return 1.0
    v = math.sin(PI * t) / (PI * t)
    return v * v

MONTGOMERY   = _sinc2(0.5)          # 4/pi2 ~= 0.405284 -- Universal Sidelobe Amplitude
SINC2_TENTH  = _sinc2(0.1)          # ~= 0.967531 -- scale-free pre-echo floor
T_STAR_EXACT = Fraction(5, 7)       # T* = 5/7 at b=35 (minimal strong semiprime)
T_STAR       = float(T_STAR_EXACT)  # ~= 0.714286


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _smallest_prime_factor(n):
    if n < 2:
        raise ValueError(f"n must be > 1, got {n}")
    if n % 2 == 0:
        return 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return i
        i += 2
    return n


def _factor_semiprime(b):
    if b < 6:
        raise ValueError(f"b={b} is too small to be a semiprime (minimum is 6 = 2x3)")
    p = _smallest_prime_factor(b)
    if p == b:
        raise ValueError(f"b={b} is prime, not a semiprime")
    q, rem = divmod(b, p)
    if rem != 0:
        raise ValueError(f"b={b}: p={p} does not divide b exactly")
    if _smallest_prime_factor(q) != q:
        raise ValueError(f"b={b} = {p} x {q} but {q} is not prime; b is not a semiprime")
    return p, q


def _is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def _next_prime(n):
    k = n + 1
    while not _is_prime(k):
        k += 1
    return k


# ---------------------------------------------------------------------------
# TIGSemiprime
# ---------------------------------------------------------------------------

class TIGSemiprime:
    """
    Algebraic structure for a semiprime b = p x q, p <= q both prime.
    All WP34 / WP35 quantities are available as methods or properties.
    """

    def __init__(self, b):
        p, q = _factor_semiprime(b)
        self._init(b, p, q)

    @classmethod
    def from_params(cls, p, q):
        if not _is_prime(p):
            raise ValueError(f"p={p} is not prime")
        if not _is_prime(q):
            raise ValueError(f"q={q} is not prime")
        if p > q:
            p, q = q, p
        obj = cls.__new__(cls)
        obj._init(p * q, p, q)
        return obj

    def _init(self, b, p, q):
        self.b = b
        self.p = p
        self.q = q
        self.f = p  # WP35 notation: f = p

    # ------------------------------------------------------------------
    # Sinc2 / R field  (WP35 Theorem 5)
    # ------------------------------------------------------------------

    def R(self, k):
        """
        Harmonic pre-echo resonance (WP35 Theorem 1):
            R(k, f) = sin2(pi*k/f) / (k2 * sin2(pi/f))
        where f = p (smallest prime factor of b).
        Verified: R(p, p) = 0 [the First-G sink]
                  R(k, p) -> sinc2(k/p) as p -> inf [Theorem 5]
        """
        f = self.f
        if k == 0:
            return 1.0
        num = math.sin(PI * k / f) ** 2
        den = (k ** 2) * (math.sin(PI / f) ** 2)
        if den == 0:
            return 0.0
        return num / den

    def sinc2(self, t):
        """sinc2(t) = (sin(pi*t)/(pi*t))2 -- the continuum limit of R(k,f)."""
        return _sinc2(t)

    def D1(self, k):
        """
        First difference (approach velocity): D1(k) = R(k+1) - R(k).
        Note: D1(p-1) < 0 (approaching null), D1(p) > 0 (recovery).
        The sign flip at k=p is the discrete-field analog of the stationary
        point in the continuum sinc2 function.
        """
        return self.R(k + 1) - self.R(k)

    def D2(self, k):
        """Second difference (curvature): D2(k) = R(k+1) - 2*R(k) + R(k-1)."""
        if k <= 0:
            return 0.0
        return self.R(k + 1) - 2 * self.R(k) + self.R(k - 1)

    # ------------------------------------------------------------------
    # Gate sets  (WP34)
    # ------------------------------------------------------------------

    def C(self, k):
        """Coprime set: {x in {1..k} : gcd(x, b) = 1}."""
        return [x for x in range(1, k + 1) if math.gcd(x, self.b) == 1]

    def G(self, k):
        """Gate set: {x in {1..k} : gcd(x, b) > 1}."""
        return [x for x in range(1, k + 1) if math.gcd(x, self.b) > 1]

    def first_g(self):
        """
        First-G event: smallest k such that G(k) is non-empty.
        WP34 Theorem: first_g() = p for every semiprime b = p x q.
        """
        for k in range(1, self.b + 1):
            if math.gcd(k, self.b) > 1:
                return k
        return self.b

    # ------------------------------------------------------------------
    # Luther dispersion  (WP34 §5 -- Conjecture, C.A. Luther)
    # ------------------------------------------------------------------

    def interleave(self, k):
        """
        Luther interleave score at position k:
            interleave(b, k) = transitions(C, G in sequence 1..k)
                               / (2 * min(|C_k|, |G_k|))
        Returns 0.0 if G is empty (k < p) or either set is empty.
        Attribution: interleave as a dispersion metric -- C.A. Luther.
        """
        seq = [math.gcd(x, self.b) > 1 for x in range(1, k + 1)]
        n_G = sum(seq)
        n_C = k - n_G
        if n_G == 0 or n_C == 0:
            return 0.0
        transitions = sum(1 for i in range(len(seq) - 1) if seq[i] != seq[i + 1])
        return transitions / (2 * min(n_C, n_G))

    def dispersion(self, k):
        """
        Luther dispersion at k: |G(k)| x interleave(b, k).
        gate_rate ~= F_k(|G| x dispersion) -- functional form open (WP34 §5).
        """
        return len(self.G(k)) * self.interleave(k)

    def dispersion_profile(self):
        """Return [(k, |G_k|, interleave_k, dispersion_k)] for k = 1..q."""
        rows = []
        for k in range(1, self.q + 1):
            g = len(self.G(k))
            iv = self.interleave(k)
            rows.append((k, float(g), iv, g * iv))
        return rows

    # ------------------------------------------------------------------
    # T* / unit fraction  (WP35 §1A)
    # ------------------------------------------------------------------

    def unit_frac(self):
        """
        T* formula (exact, as a Fraction):
            unit_frac(b) = (q - floor(q/p) - 1) / q
        At b=35 (p=5, q=7): (7-1-1)/7 = 5/7 = T* exactly.
        Returns a Fraction for exact arithmetic.
        """
        p, q = self.p, self.q
        return Fraction(q - (q // p) - 1, q)

    def t_star(self):
        """T* as a float. Exact at b=35: 5/7 ~= 0.714286."""
        return float(self.unit_frac())

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(self):
        """Return a dict of key quantities for this semiprime."""
        p, q, b = self.p, self.q, self.b
        fg = self.first_g()
        uf = self.unit_frac()

        return {
            "b": b,
            "p": p,
            "q": q,
            "q_over_p": round(q / p, 6),
            "first_g": fg,
            "first_g_is_p": fg == p,
            "unit_frac": str(uf),
            "t_star": float(uf),
            "R_at_1": round(self.R(1), 6),
            "R_at_p_minus_1": round(self.R(p - 1), 6),
            "R_at_p_sink": round(self.R(p), 8),
            "D1_sign_flip_at_p": self.D1(p - 1) < 0 and self.D1(p) > 0,
            "interleave_at_q": round(self.interleave(q), 6),
            "dispersion_at_q": round(self.dispersion(q), 6),
            "MONTGOMERY_4_over_pi2": round(MONTGOMERY, 6),
            "SINC2_TENTH": round(SINC2_TENTH, 6),
        }

    def __repr__(self):
        return f"TIGSemiprime(b={self.b}, p={self.p}, q={self.q})"


# ---------------------------------------------------------------------------
# Batch verifiers
# ---------------------------------------------------------------------------

def verify_first_g(semiprimes=None):
    """
    Verify WP34 Theorem (First-G = p) for a list of semiprimes.
    Returns {"passed": int, "failed": int, "failures": list}.
    """
    if semiprimes is None:
        semiprimes = [
            6, 10, 14, 15, 21, 22, 26, 33, 34, 35,
            38, 39, 46, 51, 55, 57, 58, 62, 65, 74,
        ]
    passed, failed, failures = 0, 0, []
    for b in semiprimes:
        try:
            s = TIGSemiprime(b)
            fg = s.first_g()
            if fg == s.p:
                passed += 1
            else:
                failed += 1
                failures.append({"b": b, "p": s.p, "first_g": fg})
        except ValueError as e:
            failed += 1
            failures.append({"b": b, "error": str(e)})
    return {"passed": passed, "failed": failed, "failures": failures}


def verify_sinc2_limit(primes=None, t=0.5, tol=0.02):
    """
    Verify WP35 Theorem 5: R(floor(t*p), p) -> sinc2(t) as p grows.
    Convergence is O(1/p) so use p >= 97 with tol=0.02 for reliable tests.
    """
    if primes is None:
        primes = [97, 101, 127, 131, 149, 151, 997, 1009, 9973]
    target = _sinc2(t)
    passed, failed = 0, 0
    max_err = 0.0
    for p in primes:
        b = p * _next_prime(p)
        s = TIGSemiprime(b)
        k = max(1, round(t * p))
        val = s.R(k)
        err = abs(val - target)
        max_err = max(max_err, err)
        if err < tol:
            passed += 1
        else:
            failed += 1
    return {
        "t": t,
        "target_sinc2": round(target, 8),
        "passed": passed,
        "failed": failed,
        "max_error": round(max_err, 8),
        "tolerance": tol,
    }


def dispersion_comparison(b1=15, b2=35):
    """Compare Luther dispersion profiles for two semiprimes."""
    s1, s2 = TIGSemiprime(b1), TIGSemiprime(b2)
    return {
        f"b={b1}": {"summary": s1.summary(), "profile": s1.dispersion_profile()},
        f"b={b2}": {"summary": s2.summary(), "profile": s2.dispersion_profile()},
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json, sys
    args = sys.argv[1:]
    if args:
        for arg in args:
            s = TIGSemiprime(int(arg))
            print(json.dumps(s.summary(), indent=2))
    else:
        for b in (15, 35):
            s = TIGSemiprime(b)
            print(f"\n{'='*50}")
            print(json.dumps(s.summary(), indent=2))
