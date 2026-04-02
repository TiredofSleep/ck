"""
k10_eisenstein_compute.py
Compute the Eisenstein bridge quantities for the Kloosterman-Dirichlet series.

Produces:
  1. Kloosterman partial sums A3_N(s) at specified s values
  2. Eisenstein coefficient |rho_E(1, 1/2+it)|^2 = 1/|zeta(1+2it)|^2 * (gamma factor)
  3. Kernel K(s,t) values and its growth rate verification
  4. Spectral matching: fit A3_N(s) against model sum over candidate gamma_k

Prerequisites: mpmath for high-precision Gamma and Zeta evaluation
  pip install mpmath
"""

import math
import cmath

try:
    import mpmath
    mpmath.mp.dps = 25  # 25 decimal places
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False
    print("WARNING: mpmath not installed. Using stdlib math only (limited precision).")

# ── Kloosterman sum Kl(1,1;p) ──────────────────────────────────────────────────

def kloosterman(p: int) -> float:
    """Kl(1,1;p) = sum_{k=1}^{p-1} cos(2*pi*(k + k^{-1})/p)."""
    total = 0.0
    for k in range(1, p):
        kinv = pow(k, -1, p)
        total += math.cos(2 * math.pi * (k + kinv) / p)
    return total


def sieve_primes(N: int) -> list[int]:
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, N+1, i):
                sieve[j] = False
    return [i for i in range(2, N+1) if sieve[i]]


# ── A3 partial sum ──────────────────────────────────────────────────────────────

def a3_partial(primes: list[int], s: complex) -> complex:
    """A3_N(s) = sum_{p in primes} Kl(1,1;p) * p^{-s}."""
    total = complex(0)
    for p in primes:
        kl = kloosterman(p)
        total += kl * (p ** (-s))
    return total


# ── Eisenstein coefficient |rho_E(1, 1/2+it)|^2 ────────────────────────────────

def eisenstein_coeff_sq(t: float) -> float:
    """
    |rho_E(1, 1/2+it)|^2 = (2*pi) / |Gamma(1/2+it)|^2 / |zeta(1+2*i*t)|^2

    Using mpmath for high precision.
    """
    if not HAS_MPMATH:
        # Rough approximation: |Gamma(1/2+it)|^2 ~ pi/cosh(pi*t) for large t
        gamma_sq = math.pi / math.cosh(math.pi * abs(t)) if abs(t) > 0.1 else math.pi
        # |zeta(1+2it)|: no good closed form, skip
        return 2 * math.pi / gamma_sq

    s_val = mpmath.mpc(0.5, t)
    gamma_sq = abs(mpmath.gamma(s_val))**2
    zeta_val = mpmath.zeta(1 + 2j * t)
    zeta_sq = abs(zeta_val)**2

    if zeta_sq < 1e-30:
        return float('inf')  # Shouldn't happen on Re=1

    return float(2 * math.pi / (gamma_sq * zeta_sq))


# ── Kernel K(s,t) ───────────────────────────────────────────────────────────────

def kernel_K(s: complex, t: float) -> complex:
    """
    K(s, t) = (2*pi)^{1-2s} * (4*pi)^{2s-2} * |Gamma(s-1/2+it)|^2
              / (|Gamma(1/2+it)|^2 * Gamma(2s-1))

    Only valid for Re(s) > 1.
    """
    if not HAS_MPMATH:
        return complex(float('nan'))

    s_mp = mpmath.mpc(s.real, s.imag)
    t_mp = mpmath.mpf(t)

    g1 = mpmath.gamma(s_mp - 0.5 + 1j * t_mp)
    g2 = mpmath.gamma(s_mp - 0.5 - 1j * t_mp)
    g3 = mpmath.gamma(mpmath.mpc(0.5, t_mp))
    g4 = mpmath.gamma(mpmath.mpc(0.5, -t_mp))
    g5 = mpmath.gamma(2 * s_mp - 1)

    numerator = (2 * mpmath.pi)**(1 - 2*s_mp) * (4 * mpmath.pi)**(2*s_mp - 2) * g1 * g2
    denominator = g3 * g4 * g5

    if abs(denominator) < 1e-30:
        return complex(float('nan'))

    return complex(numerator / denominator)


# ── Kernel growth rate verification ────────────────────────────────────────────

def verify_kernel_growth(s: complex, t_values: list[float]) -> None:
    """Verify K(s,t) ~ C * |t|^{2*Re(s)-2} for large t."""
    exponent = 2 * s.real - 2
    print(f"\n  Kernel growth at s={s}: expected |t|^{exponent:.2f}")
    print(f"  {'t':>8}  {'|K(s,t)|':>14}  {'|t|^exp':>14}  {'ratio':>10}")

    prev_K = None
    prev_t = None
    for t in t_values:
        if abs(t) < 0.1:
            continue
        K_val = kernel_K(s, t)
        if math.isnan(abs(K_val)):
            continue
        K_abs = abs(K_val)
        expected = abs(t) ** exponent
        ratio = K_abs / expected if expected > 1e-15 else float('inf')
        print(f"  {t:>8.1f}  {K_abs:>14.6e}  {expected:>14.6e}  {ratio:>10.4f}")


# ── Spectral matching: fit gamma_k candidates ──────────────────────────────────

def spectral_match(a3_vals: dict, s_values: list[complex],
                   gamma_candidates: list[float]) -> None:
    """
    Compare A3_N(s) to model sum over trial zeros.
    Model: A3^{Eis}(s) ~ sum_k c_k * integral_approx(s, gamma_k)

    This is a rough numerical illustration, not a proof.
    """
    if not HAS_MPMATH:
        print("  Skipping spectral match (mpmath required)")
        return

    print("\n  Spectral match: comparing A3_N(s) magnitudes to Eisenstein model")
    print(f"  {'s':>12}  {'|A3_N|':>12}  {'gamma_k fit':>12}")

    for s in s_values:
        a3_val = a3_vals.get(s, complex(0))
        # Model: sum over gamma_k of 1/(1 + (Im(s) - gamma_k/2)^2) as rough proxy
        model_terms = [1.0 / (1 + (s.imag - g/2)**2) for g in gamma_candidates]
        model_sum = sum(model_terms)
        print(f"  {s!r:>12}  {abs(a3_val):>12.6e}  {model_sum:>12.6e}")


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    PRIME_LIMIT = 500
    S_VALUES = [complex(2.0, 0), complex(1.75, 0), complex(1.6, 0)]
    T_GROWTH_VALS = [1.0, 5.0, 10.0, 20.0, 50.0, 100.0]

    # Known low ζ-zeros (imaginary parts), for spectral match illustration
    KNOWN_ZEROS = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351]

    print("=" * 60)
    print("K10 Eisenstein Bridge Computation")
    print("=" * 60)

    primes = sieve_primes(PRIME_LIMIT)
    print(f"\nPrimes up to {PRIME_LIMIT}: {len(primes)} primes")

    # ── 1. Kloosterman partial sums ──
    print("\n── 1. Kloosterman Partial Sums A3_N(s) ──")
    a3_dict = {}
    for s in S_VALUES:
        val = a3_partial(primes, s)
        a3_dict[s] = val
        # Weil bound: |A3_N| <= sum_p 2*sqrt(p) * p^{-Re(s)} = 2*sum_p p^{1/2-Re(s)}
        weil = sum(2 * p**(0.5 - s.real) for p in primes)
        print(f"  s={s}: A3_N = {val:.6f}   |A3_N|={abs(val):.4f}   Weil_bound={weil:.2f}")

    # ── 2. Eisenstein coefficient ──
    print("\n── 2. Eisenstein Coefficient |ρ_E(1, 1/2+it)|² ──")
    T_VALS = [0.5, 1.0, 5.0, 14.13, 21.02, 25.01, 50.0]
    print(f"  {'t':>8}  {'|rho_E|^2':>14}  {'note':>25}")
    for t in T_VALS:
        val = eisenstein_coeff_sq(t)
        note = ""
        if abs(t - 14.1347) < 0.05:
            note = "<-- near gamma_1/2"
        elif abs(t - 21.022) < 0.05:
            note = "<-- near gamma_2/2"
        print(f"  {t:>8.3f}  {val:>14.6e}  {note}")

    # Note: evaluate at t = gamma_k / 2 (not gamma_k!) since zeta(1+2it) at t = gamma_k/2
    print("\n  NOTE: zeros gamma_k appear at DOUBLE the t-values above (t = gamma_k/2)")
    print("  At t=gamma_k/2: zeta(1+2it) = zeta(1+i*gamma_k) -- NOT zero (non-vanishing on Re=1)")
    print("  So |rho_E|^2 is smooth everywhere -- NO poles at ζ-zero related t values. ✓")

    # ── 3. Kernel growth ──
    print("\n── 3. Kernel K(s,t) Growth Rate Verification ──")
    if HAS_MPMATH:
        verify_kernel_growth(complex(1.75, 0), T_GROWTH_VALS)
        verify_kernel_growth(complex(2.0, 0), T_GROWTH_VALS)
    else:
        print("  (mpmath required for kernel computation)")

    # ── 4. Spectral matching illustration ──
    print("\n── 4. Spectral Matching Illustration ──")
    spectral_match(a3_dict, S_VALUES, KNOWN_ZEROS)
    print("  (This is a rough illustration only; see K10_FREDHOLM_INVERSION.md §5)")

    # ── 5. Summary ──
    print("\n── 5. K10 Summary ──")
    print("  Theorem K10.1 (D): rho_E(1,1/2+it) = 1/zeta(1+2it) * gamma_factor")
    print("  Theorem K10.2 (D): Direct-pole route CLOSED (no poles on real t-axis)")
    print("  Theorem K10.5 (D): Fredholm T_K is NOT compact for Re(s)>1/2")
    print("  Claim K10.6 (C):   |zeta(1+2it)|^-2 oscillates at frequencies gamma_k/2")
    print("  Conjecture K10.C1 (B): Double Dirichlet Z(s,w) has functional equation")
    print()
    print("  Surviving path: K10.C1 double Dirichlet + K6 H3 Kloosterman kernel")


if __name__ == "__main__":
    main()
