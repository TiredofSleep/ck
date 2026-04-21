"""
COMPUTATION: T* for Primorial Rings Z/NZ
Sprint 15 — Task 1 | 2026-04-10

Computes the coherence threshold T* for Z/NZ where N runs through
the primorial sequence: 10, 30, 210, 2310, ...

T* on Z/10Z = 5/7 (from the TSML composition table: 73 of 100 cells
output HARMONY, and T* = first cyclotomic closure / first obstruction
= p_closure / p_obstruction = 5/7).

The generalization: for squarefree N = p1*p2*...*pk, T* is determined
by the cyclotomic structure of Z/NZ. Specifically:

  T*(N) = p_{k-1} / p_k

where p_{k-1} is the second-largest prime factor (first complete closure)
and p_k is the largest prime factor (first obstruction).

This is because:
- The cyclotomic polynomial Phi_p(x) has degree p-1
- Full closure in (Z/pZ)* requires all p-1 elements
- The ratio of successive prime closures gives T*

For the primorial sequence:
  N = 10 = 2*5:     T* = 5/7?  Wait -- 7 is NOT a factor of 10.

Actually, let me re-derive T* from first principles.

On Z/10Z, T* = 5/7 came from:
  - 5 = first prime where cyclotomic closure is COMPLETE
  - 7 = first prime where full closure is OBSTRUCTED
  - T* = 5/7 = closure/obstruction ratio

The primes involved are 5 and 7 -- the closure prime and the
obstruction prime. These are consecutive primes, NOT factors of 10.

So T* depends on the PRIMES AROUND the structure, not just the
factors of N.

For general N, the cyclotomic threshold should be:
  T*(N) = p_last_closed(N) / p_first_obstructed(N)

On Z/10Z: units (Z/10Z)* = {1, 3, 7, 9}, order 4 = phi(10).
  - p = 2: Phi_2 has degree 1. Closure trivial.
  - p = 3: Phi_3 has degree 2. Closure in (Z/10Z)*? Check.
  - p = 5: Phi_5 has degree 4 = phi(10). Full closure.
  - p = 7: Phi_7 has degree 6 > phi(10) = 4. OBSTRUCTED.
  - T* = 5/7.

Let me compute this for each primorial.

Copyright (c) 2026 Brayden Ross Sanders / 7Site LLC
"""

import math
from functools import reduce

def euler_phi(n):
    """Euler totient function."""
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result

def cyclotomic_degree(p):
    """Degree of the p-th cyclotomic polynomial = phi(p) = p-1 for prime p."""
    return p - 1

def find_tstar(N):
    """
    Find T* for Z/NZ.

    T* = p_closure / p_obstruction where:
    - p_closure = largest prime p such that deg(Phi_p) <= phi(N)
    - p_obstruction = smallest prime p such that deg(Phi_p) > phi(N)

    For prime p: deg(Phi_p) = p - 1.
    So: p_closure = largest prime <= phi(N) + 1
        p_obstruction = smallest prime > phi(N) + 1
    Wait, that's not right either. Let me think more carefully.

    On Z/10Z: phi(10) = 4. The unit group has order 4.
    - A single generator g in (Z/10Z)* has order dividing 4.
    - For g to "close" (generate the full group), need ord(g) = 4.
    - The obstruction at prime p means: there's no element of order p-1
      in (Z/10Z)* if p-1 > 4.

    So the threshold is determined by which cyclotomic polynomials
    can be fully realized in (Z/NZ)*.

    phi(N) = |(Z/NZ)*|.

    Closure prime p_c: largest prime with p-1 | phi(N) AND p-1 <= phi(N)
    Actually: largest prime p with p-1 <= phi(N).

    Obstruction prime p_o: smallest prime p with p-1 > phi(N).

    For p prime: deg(Phi_p) = p-1. Full closure requires p-1 <= phi(N).

    p_c = largest prime <= phi(N) + 1
    p_o = smallest prime > phi(N) + 1
    """
    phi_N = euler_phi(N)

    # Find p_closure: largest prime p with p - 1 <= phi_N
    # i.e., largest prime p <= phi_N + 1
    p_closure = None
    for p in range(phi_N + 1, 1, -1):
        if is_prime(p):
            p_closure = p
            break

    # Find p_obstruction: smallest prime p with p - 1 > phi_N
    # i.e., smallest prime p > phi_N + 1
    p_obstruction = phi_N + 2
    while not is_prime(p_obstruction):
        p_obstruction += 1

    return p_closure, p_obstruction, phi_N

def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            if d not in factors:
                factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

# =====================================================================
# MAIN COMPUTATION
# =====================================================================

print("=" * 70)
print("T* COMPUTATION FOR PRIMORIAL RINGS")
print("=" * 70)

# Primorial sequence
primorials = {
    "2*5": 10,
    "2*3*5": 30,
    "2*3*5*7": 210,
    "2*3*5*7*11": 2310,
    "2*3*5*7*11*13": 30030,
}

results = []

for label, N in primorials.items():
    phi_N = euler_phi(N)
    p_c, p_o, _ = find_tstar(N)
    T_star = p_c / p_o
    factors = prime_factors(N)

    print(f"\n--- Z/{N}Z = Z/{label}Z ---")
    print(f"  Prime factors: {factors}")
    print(f"  phi({N}) = {phi_N}")
    print(f"  p_closure = {p_c} (largest prime <= phi(N)+1 = {phi_N+1})")
    print(f"  p_obstruction = {p_o} (smallest prime > phi(N)+1)")
    print(f"  T* = {p_c}/{p_o} = {T_star:.10f}")

    results.append((N, phi_N, p_c, p_o, T_star))

# =====================================================================
# CONVERGENCE ANALYSIS
# =====================================================================

print("\n" + "=" * 70)
print("CONVERGENCE TABLE")
print("=" * 70)

print(f"\n{'N':>8} {'phi(N)':>8} {'p_c':>6} {'p_o':>6} {'T*':>14} {'|T*-1/e|':>14}")
print("-" * 70)

xi_0 = math.exp(-1)

for N, phi_N, p_c, p_o, T_star in results:
    diff = abs(T_star - xi_0)
    print(f"{N:>8} {phi_N:>8} {p_c:>6} {p_o:>6} {T_star:>14.10f} {diff:>14.10f}")

print(f"\n{'e^{-1}':>8} {'':>8} {'':>6} {'':>6} {xi_0:>14.10f} {'0':>14}")

# =====================================================================
# ANALYSIS: Does T* converge?
# =====================================================================

print("\n" + "=" * 70)
print("ANALYSIS")
print("=" * 70)

T_values = [r[4] for r in results]

print(f"\nT* sequence: {[f'{t:.6f}' for t in T_values]}")
print(f"e^{{-1}} = {xi_0:.6f}")
print(f"1/2 = {0.5:.6f}")

# Check: are they approaching e^{-1}?
diffs_from_einv = [abs(t - xi_0) for t in T_values]
print(f"\n|T* - e^{{-1}}| sequence: {[f'{d:.6f}' for d in diffs_from_einv]}")

# Check: are they approaching any other constant?
# By prime number theorem: p_c ~ phi(N), p_o ~ phi(N) + O(phi(N)/log(phi(N)))
# So T* ~ phi(N) / (phi(N) + gap) ~ 1 - gap/phi(N) -> 1 as N -> inf
# This means T* -> 1, NOT e^{-1}!

print("\n--- Key Finding ---")
print("As N grows through primorials:")
print(f"  phi(N) grows rapidly (phi(N)/N -> product(1-1/p) = 0 asymptotically)")
print(f"  But p_c and p_o both grow ~ phi(N)")
print(f"  By PNT: p_o - p_c ~ phi(N)/log(phi(N))")
print(f"  So T* = p_c/p_o ~ 1 - 1/log(phi(N)) -> 1")
print(f"\n  T* does NOT converge to e^{{-1}}.")
print(f"  T* converges to 1.")
print(f"\n  This means the cyclotomic T* is NOT the right generalization")
print(f"  for the N->infinity limit. The discrete gap CLOSES as N grows.")
print(f"  The continuous xi_0 = e^{{-1}} must arise from a DIFFERENT")
print(f"  limit procedure -- not the cyclotomic ratio.")
print(f"\n  The BB bridge is structural, not numerical.")
print(f"  The N->infinity construction needs the JKO/Wasserstein framework,")
print(f"  not the cyclotomic ratio.")
