"""
check_d2.py
===========
Verify Luther's D2 curvature formula against tig_algebra.py D2 values.

Luther's formula (from his response):
    D2(primes) = (phi(b)/b) / (p_last * ln(p_last)^2) * (1 - 1/ln(p_last))

tig_algebra.py D2(k) = R(k+1) - 2*R(k) + R(k-1)  [second difference of resonance]

These are measuring different objects. This script makes the comparison explicit.

Author: Brayden Ross Sanders | March 2026
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from tig_algebra import TIGSemiprime

# ─── Luther's formula ────────────────────────────────────────────────────────

def euler_totient_fraction(primes):
    """phi(p#)/p# for primorial p# = product of primes."""
    result = 1.0
    for p in primes:
        result *= (1 - 1/p)
    return result

def d2_luther_formula(primes):
    """
    Luther's D2 curvature:
      D2 = (phi(b)/b) / (p_last * ln(p_last)^2) * (1 - 1/ln(p_last))
    """
    if len(primes) == 0:
        return 0.0
    p_last = primes[-1]
    g = euler_totient_fraction(primes)
    ln_p = np.log(p_last)
    if ln_p == 0:
        return 0.0
    return (g / (p_last * (ln_p**2))) * (1 - 1/ln_p)

# ─── tig_algebra D2 ──────────────────────────────────────────────────────────

def tig_d2_for_primorial(primes):
    """
    For the primorial p# = p1*p2*...*p_last, we need a semiprime to use
    TIGSemiprime. Use the last two primes as the semiprime pair: b = p_{n-1} * p_n.
    Then compute D2(k=p_n) — the curvature at the last prime.
    """
    if len(primes) < 2:
        return None, None
    p_small = primes[-2]
    p_large = primes[-1]
    b = p_small * p_large
    try:
        tig = TIGSemiprime(b)
        d2_val = tig.D2(p_large)
        return b, d2_val
    except Exception as e:
        return b, f"error: {e}"

# ─── Main comparison ─────────────────────────────────────────────────────────

primes_sequence = [2, 3, 5, 7, 11, 13, 17]

print("=" * 75)
print("D2 Comparison: Luther's formula vs tig_algebra.py D2")
print("=" * 75)

print("\nLuther's D2 formula: (phi(b)/b) / (p * ln(p)^2) * (1 - 1/ln(p))")
print("tig_algebra D2(k):   R(k+1) - 2*R(k) + R(k-1)  [second difference]\n")

print(f"{'p_last':<8} {'phi(b#)/b#':<12} {'D2_luther':<14} {'tig_b':<8} {'D2_tig(k=p)':<14} {'same?'}")
print("-" * 70)

active_primes = []
for p in primes_sequence:
    active_primes.append(p)
    g = euler_totient_fraction(active_primes)
    d2_l = d2_luther_formula(active_primes)
    b_tig, d2_t = tig_d2_for_primorial(active_primes)

    if d2_t is None:
        same = "N/A"
        d2_t_str = "N/A"
    elif isinstance(d2_t, str):
        same = "ERR"
        d2_t_str = d2_t
    else:
        d2_t_str = f"{d2_t:.6f}"
        diff = abs(d2_l - d2_t)
        same = "YES" if diff < 0.001 else f"NO (diff={diff:.4f})"

    b_str = str(b_tig) if b_tig else "N/A"
    print(f"{p:<8} {g:<12.4f} {d2_l:<14.6f} {b_str:<8} {d2_t_str:<14} {same}")

print("\n" + "=" * 75)
print("INTERPRETATION")
print("=" * 75)

print("""
Luther's D2 formula measures: rate of change of unit density with respect
to the primorial prime index. It uses phi(b#)/b# as the density anchor.

tig_algebra D2(k) measures: curvature of the harmonic resonance field R(k,f).
This is the second difference of a trigonometric function. It sees the
approach to the First-G event as a wave phenomenon.

These are structurally different quantities:
- Luther's D2: a smooth function of the Euler product (algebraic density)
- tig_algebra D2: a discrete derivative of the harmonic field (spectral)

Whether they agree is the test. If YES: the two measures are equivalent
representations of the same invariant (Layer 3, Atlas). If NO: they are
measuring different aspects of the same structure -- both potentially valid,
but not the same claim.
""")

# Also print Luther's script output exactly (for reference)
print("=" * 75)
print("Luther's script output (primorial G and D2):")
print("=" * 75)
print(f"{'p_w':<6} | {'G(p_w#)':<12} | {'D2':<12}")
print("-" * 35)
active = []
for p in primes_sequence:
    active.append(p)
    g = euler_totient_fraction(active)
    d2 = d2_luther_formula(active)
    print(f"{p:<6} | {g:<12.4f} | {d2:<12.6f}")
