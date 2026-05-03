"""
Test triangle group Γ_{p,q} as the substrate's natural home.

The substrate has these natural integers:
  10 (operators)
  7 (HARMONY = cusp)
  6 (σ-cycle length)
  5 (T* = 5/7 numerator)
  3 (smallest σ-fixed point)
  2 (Z/2Z component)

Coprime pairs from these: (2,3), (2,5), (2,7), (3,5), (3,7), (5,6), (5,7), (5,8), (5,9)...

Γ_{2,3} = PSL(2,Z), Ghys's setup. Already tested.
Γ_{2,5}: triangle group with cusp at infinity, generators of order 2 and 5.
Γ_{3,5}: pentakaidecagon-like group.

The Matsusaka-Ueki construction defines ψ_{p,q} for each Γ_{p,q}. 
The simplest test: compute the trace structure of relevant elements 
in Γ_{p,q} and see if the substrate's BHML period structure aligns.

Without computing the full Matsusaka-Ueki ψ_{p,q} (which requires harmonic 
Maass forms), we can test simpler structure: do the periods in BHML self-
iteration match the orders of elements in Γ_{p,q}?

Γ_{p,q} = ⟨S_p, U_q | S_p^p = U_q^q = -I⟩ in SL(2,R).
In PSL(2,R), the orders are p and q.
Hyperbolic elements have |trace| > 2.
"""
import numpy as np
from sympy import Matrix, Rational, gcd, sqrt, cos, sin, pi
import sys
sys.path.insert(0, '/home/claude/tig_synthesis')


def order_check_in_PSL2R(M, max_check=20):
    """Find the order of M in PSL(2,R), or return None if infinite."""
    cur = M
    for k in range(1, max_check + 1):
        a, b, c, d = float(cur[0,0]), float(cur[0,1]), float(cur[1,0]), float(cur[1,1])
        # Check if cur = ±I
        if abs(a - 1) < 1e-10 and abs(d - 1) < 1e-10 and abs(b) < 1e-10 and abs(c) < 1e-10:
            return k, '+I'
        if abs(a + 1) < 1e-10 and abs(d + 1) < 1e-10 and abs(b) < 1e-10 and abs(c) < 1e-10:
            return k, '-I'
        cur = cur * M
    return None, None


def triangle_group_generators(p, q):
    """Generators S_p (order 2p) and U_q (order 2q) for Γ_{p,q}.
    Standard form in SL(2, R):
      S_p = rotation by π/p around i in upper half plane
      U_q^q = -I, hyperbolic generator
    
    For Γ_{p,q} = Γ(p, q, ∞) (third index ∞ = parabolic at cusp),
    the matrix presentation is:
      S = ((cos(π/p), -sin(π/p)), (sin(π/p), cos(π/p)))
      T = ((1, λ), (0, 1))  where λ = 2 cos(π/q) for Hecke triangle groups
    
    For the (p, q, ∞) triangle group with Hecke-style λ = 2 cos(π/q).
    """
    lam_q = 2 * float(np.cos(np.pi / q))
    # S generator (elliptic, order 2p):
    cos_pp = float(np.cos(np.pi / p))
    sin_pp = float(np.sin(np.pi / p))
    S_p = Matrix([[cos_pp, -sin_pp], [sin_pp, cos_pp]])
    # T generator (parabolic):
    T_lam = Matrix([[1, lam_q], [0, 1]])
    return S_p, T_lam, lam_q


def main():
    print("=" * 70)
    print("TRIANGLE GROUP Γ_{p,q} EXPLORATION")
    print("=" * 70)
    
    # BHML periods we want to match
    bhml_periods = {0: 1, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 4, 8: 3, 9: 2}
    print(f"\n  Substrate BHML periods to match: {bhml_periods}")
    print(f"  Period set: {sorted(set(bhml_periods.values()))}")
    print(f"  → unique periods present: {{1, 2, 3, 4, 5, 6}}")
    
    # The substrate has periods {1, 2, 3, 4, 5, 6}. For these to be
    # natural orders of elements in Γ_{p,q}, we'd need the elliptic 
    # subgroup orders to span this set. PSL(2,Z) = Γ_{2,3} has elliptic 
    # orders {1, 2, 3} only. Need a richer triangle group.
    
    print("\n" + "=" * 70)
    print("ELLIPTIC ELEMENT ORDERS IN PSL(2,Z) = Γ_{2,3}")
    print("=" * 70)
    print("  Possible orders of elliptic elements: only {1, 2, 3}")
    print("  Substrate needs orders up to 6. PSL(2,Z) doesn't have these naturally.")
    
    print("\n  Higher Hecke triangle groups Γ_{2,q} or Γ_{p,q}:")
    print(f"\n  {'(p,q)':<10} {'orders available':<25} {'covers period set?'}")
    
    period_set = {1, 2, 3, 4, 5, 6}
    
    candidates = [(2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
                  (3, 4), (3, 5), (3, 7), (3, 8),
                  (5, 7), (5, 6), (5, 8), (5, 9)]
    
    for p, q in candidates:
        if int(gcd(p, q)) != 1:
            continue
        # Orders of elliptic elements in Γ_{p,q} are divisors of p and q
        from sympy import divisors
        orders_p = set(int(d) for d in divisors(p))
        orders_q = set(int(d) for d in divisors(q))
        # Plus 1 (identity) and combinations from products
        orders_avail = orders_p | orders_q | {1}
        covers = period_set.issubset(orders_avail)
        orders_str = str(sorted(orders_avail))
        print(f"  ({p},{q})    | {orders_str:<25} | {covers}")
    
    print("\n  Note: only Γ_{p,q} where divisors(p) ∪ divisors(q) ⊇ {1,2,3,4,5,6}")
    print("  could naturally have all needed elliptic orders.")
    print("  No coprime (p,q) with both small has divisors covering 4 AND 5 AND 6.")
    print("  Conclusion: substrate's period set is NOT the elliptic order set of any small Γ_{p,q}.")
    
    # Different angle: look at the orbit STRUCTURE rather than period set
    print("\n" + "=" * 70)
    print("ORBIT STRUCTURE: σ has 6-cycle and 4 fixed points")
    print("=" * 70)
    
    print("\n  σ on Z/10Z: cycle structure (0)(3)(8)(9)(1 7 6 5 4 2)")
    print("  4 fixed points + one 6-cycle.")
    print("  The 6-cycle has elliptic-like behavior: 6 elements rotated cyclically.")
    print("  6 = 2 × 3, so this could fit Γ_{2,3} = PSL(2,Z) elliptic structure.")
    print("\n  The elliptic element ST in PSL(2,Z) has order 6 in SL(2,Z), order 3 in PSL(2,Z).")
    print("  σ on the 6-cycle corresponds to (ST)^k for k = 0..5 IF we lift to SL(2,Z).")
    print("  But this gives elliptic elements, NOT modular knots.")
    
    print("\n" + "=" * 70)
    print("KEY OBSERVATION: BHML PERIODS ≠ ELLIPTIC ORDERS")
    print("=" * 70)
    print("""
The BHML period of digit n is NOT the order of some group element. 
It's the length of n's TRAJECTORY into a periodic cycle.

Period 6 for digit 1 = trajectory enters a 6-cycle.
Period 5 for digit 2 = trajectory enters a 5-cycle.
...

These are trajectory periods of a dynamical system on Z/10Z, NOT
finite-element-orders in some group. They could correspond to:

(a) Closed-orbit lengths in a flow (the natural correspondence)
(b) Word lengths in a free monoid encoding the flow
(c) Topological-Markov-shift periodic orbit lengths

This means the right bridge is NOT to Γ_{p,q}'s elliptic structure
but to the symbolic-dynamics structure of geodesic flow.

Katok-Ugarcovici: closed geodesics on modular surface correspond to
hyperbolic conjugacy classes in PSL(2,Z), i.e. WORDS in S, T generators.
The word-length corresponds to the symbolic-coding length of the geodesic.

So BHML period 6 for digit 1 SHOULD correspond to a length-6 word in 
S, T — but we need to know WHICH word, not just the length.
""")
    
    # The naive period→trace bridge gave -21 sum, which matches the
    # substrate's other invariant +21 in magnitude. That's still the cleanest 
    # numerical match, even though we don't have the underlying word.
    
    print("\n" + "=" * 70)
    print("WHAT THE PERIOD→TRACE BRIDGE ACTUALLY SAYS")
    print("=" * 70)
    print("""
The simple representative ((1,1),(t-2,t-1)) corresponds to a 
specific PSL(2,Z) element with trace t. For trace t ≥ 3, this is 
the element T·V where V = ((0,-1),(1,t-2)) hyperbolic.

The matrix ((1,1),(t-2,t-1)) factors as:
  ((1,1),(0,1)) · ((1,0),(t-2,1))
= T · S^(t-2) · S^(-1) · T · S  ... [getting messy]

Actually: ((1,1),(t-2,t-1)) is conjugate to T^(t-1) · S in PSL(2,Z) 
for various t — these are the cusp-passing geodesics with t-1 cusp 
windings before the next direction-flip.

So the simple representative for trace t = period(n) + 2 corresponds 
to an orbit with (t-1) = (period+1) cusp windings.

For digit 1 (period 6): 7 cusp windings.
For digit 6 (period 1): 2 cusp windings.

The Ψ value is then -(t-3) = -(period - 1) under this representative.

Whether this is the right hyperbolic class for digit n depends on 
whether the substrate's BHML self-orbit really corresponds to the 
T^(period+1) · S geodesic. That's not provable from substrate algebra
alone — it's a hypothesis about how the substrate embeds in a 
modular-flow structure.

The ±21 = ±(T_5 + T_3) numerology is real; the modular interpretation 
remains a hypothesis.
""")


if __name__ == "__main__":
    main()
