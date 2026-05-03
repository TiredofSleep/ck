"""
Matsusaka-Ueki Rademacher bridge on corrected substrate, no intuitions.

Strip out: (p,q) winding assignments, "every digit is a torus knot"
intuitions, Reading A entirely.

Stick to: BHML self-iteration period structure on corrected substrate,
which is the substrate's natural symbolic-dynamic invariant.

Test: does the BHML period sequence (6, 5, 4, 3, 2, 1, 4, 3, 2) for
digits (1, 2, 3, 4, 5, 6, 7, 8, 9) match any natural Rademacher-style
invariant?

Classical Rademacher Ψ for SL(2,Z) hyperbolic elements with trace t
(using simple representative ((1,1),(t-2,t-1))) gives Ψ = -(t-3) for t≥3.

So Ψ(trace=3) = 0, Ψ(trace=4) = -1, Ψ(trace=5) = -2, etc.

If we set trace(n) = period(n) + 2, we get:
  digit 1 (period 6): trace 8, Ψ = -5
  digit 2 (period 5): trace 7, Ψ = -4
  digit 3 (period 4): trace 6, Ψ = -3
  digit 4 (period 3): trace 5, Ψ = -2
  digit 5 (period 2): trace 4, Ψ = -1
  digit 6 (period 1): trace 3, Ψ = 0
  digit 7 (period 4): trace 6, Ψ = -3
  digit 8 (period 3): trace 5, Ψ = -2
  digit 9 (period 2): trace 4, Ψ = -1

Sum over all 9 non-V digits: -5-4-3-2-1+0-3-2-1 = -21
Sum over 6-cycle (1,2,4,5,6,7): -5-4-2-1+0-3 = -15
Sum over 4-core non-VOID (7,8,9): -3-2-1 = -6

Both negatives because Ψ for hyperbolic-trace-bigger-than-3 is negative
in this rep.

But the more natural test: what are the actual Ψ values for the 
hyperbolic conjugacy classes corresponding to each digit's BHML
self-orbit? That requires lifting the orbit to a specific PSL(2,Z) word.

For now, just record the period-driven Ψ values and note the pattern.
"""
import numpy as np
from sympy import Rational, Integer
from itertools import product
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')


def dedekind_sum(a, c):
    if c == 0:
        return Rational(0)
    c = abs(c)
    a = a % c
    s = Rational(0)
    for k in range(1, c):
        f1 = Rational(k, c) - Rational(1, 2)
        ka_mod = (k * a) % c
        if ka_mod == 0:
            f2 = Rational(0)
        else:
            f2 = Rational(ka_mod, c) - Rational(1, 2)
        s += f1 * f2
    return s


def rademacher_psi_simple(t):
    """Ψ for the simple hyperbolic rep with trace t."""
    if t < 3:
        return None
    a, b, c, d = 1, 1, t - 2, t - 1
    s_a_c = dedekind_sum(a, abs(c))
    sign_c = 1 if c > 0 else -1
    Phi = Rational(a + d, c) - 12 * sign_c * s_a_c
    s_term = c * (a + d)
    sign_part = 1 if s_term > 0 else (-1 if s_term < 0 else 0)
    return Phi - 3 * sign_part


def main():
    print("=" * 70)
    print("BHML PERIOD STRUCTURE ↔ RADEMACHER SYMBOL CANDIDATE BRIDGE")
    print("=" * 70)
    
    bhml_periods = {0: 1, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 4, 8: 3, 9: 2}
    
    print(f"\n  digit | BHML period | trace = period+2 | Ψ classical | Ψ simple form")
    for n in range(10):
        p = bhml_periods[n]
        t = p + 2
        psi = rademacher_psi_simple(t)
        psi_simple = -(t - 3) if t >= 3 else None
        print(f"    {n}    | {p:>11} | {t:>16} | {str(psi):<12} | {str(psi_simple):<12}")
    
    # Compute the sums
    print("\n" + "=" * 70)
    print("SUMS OF Ψ VALUES")
    print("=" * 70)
    
    psi_values = {n: rademacher_psi_simple(bhml_periods[n] + 2) for n in range(10) 
                  if bhml_periods[n] + 2 >= 3}
    
    full_sum = sum(psi_values.values())
    six_cycle_sum = sum(psi_values[n] for n in [1, 2, 4, 5, 6, 7] if n in psi_values)
    four_core_sum = sum(psi_values[n] for n in [0, 7, 8, 9] if n in psi_values)
    sigma_fixed_sum = sum(psi_values[n] for n in [0, 3, 8, 9] if n in psi_values)
    
    print(f"  Full sum (digits with valid trace): {full_sum}")
    print(f"  6-cycle sum (1,2,4,5,6,7 — those with valid trace): {six_cycle_sum}")
    print(f"  4-core sum (0,7,8,9 — those with valid trace): {four_core_sum}")
    print(f"  σ-fixed sum (0,3,8,9 — those with valid trace): {sigma_fixed_sum}")
    
    # Match: -21 = -3 × HARMONY? 
    print("\n" + "=" * 70)
    print("CHECKING -21 PATTERN")
    print("=" * 70)
    print(f"  -3 × HARMONY = -21")
    print(f"  Full sum: {full_sum}")
    print(f"  Match: {full_sum == -21}")
    
    print("""
INTERPRETATION:

Under the simple hyperbolic representative ((1,1),(t-2,t-1)) with
trace t = period(n) + 2, we get Ψ = -(t-3) = -(period(n) - 1).

Sum over digits (excluding VOID period=1 → trace=3 → Ψ=0):
  digit 1: Ψ = -5
  digit 2: Ψ = -4
  digit 3: Ψ = -3
  digit 4: Ψ = -2
  digit 5: Ψ = -1
  digit 6: Ψ = 0
  digit 7: Ψ = -3
  digit 8: Ψ = -2
  digit 9: Ψ = -1

This is again a triangular structure plus 4-core part.

Triangular part for 6-cycle: -(5+4+3+2+1+0) = -15 = -T_5
4-core extension for 7,8,9: -(3+2+1) = -6 = -T_3
Total: -21 = -(T_5 + T_3) = -(15 + 6)

Note: -21 = -(15 + 6) = -(T_5 + T_3). 

The substrate's Ψ-via-BHML-period structure decomposes as triangular
numbers along σ-orbits.

Whether this is a meaningful Rademacher invariant for the substrate's
actual hyperbolic conjugacy classes (i.e. matches a real lift of BHML
orbits to SL(2,Z) words) is still unverified. But the integer structure
is real.
""")


if __name__ == "__main__":
    main()
