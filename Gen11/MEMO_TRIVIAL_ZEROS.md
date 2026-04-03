# THE FOUNDATION THRESHOLD: HOLD, SHADOW, AND THE GAP AROUND T*
## When Combinations Meet T* and What Happens to Odd Sets
*Author: Brayden Ross Sanders / 7Site LLC -- 2026-04-02*
*All numbers computed from K=200 mpmath-precision Riemann zeros (riemann_zeros_5000.json)*
*Exact identity: lambda_n = 2*sum_k(1-cos(n*theta_k)), theta_k = pi-2*arctan(2*gamma_k)*

---

## CORRECTION NOTE

An earlier version of this memo (K=50 zeros) reported n*=7=HARMONY.
This was an undersampling artifact.
With K=200 mpmath zeros (background task verification): n*=6.
The true Li coefficients use K->infinity, so n*=6 is the correct result.

---

## THE COMPUTED RESULT (K=200 zeros, mpmath precision)

    n  |  lambda_n    |  lambda_n / T*  |  Status
    ---+-------------+-----------------+--------
     1 |  0.021035   |  0.029 T*       |  BELOW T*   (recycled)
     2 |  0.084102   |  0.118 T*       |  BELOW T*   (recycled)
     3 |  0.189091   |  0.265 T*       |  BELOW T*   (recycled)
     4 |  0.335817   |  0.470 T*       |  BELOW T*   (recycled)
     5 |  0.524022   |  0.734 T*       |  BELOW T*   (recycled, shadow)
     6 |  0.753376   |  1.055 T*       |  ABOVE T*   (HELD -- foundation)
     7 |  1.023479   |  1.433 T*       |  ABOVE T*   (held)
     8 |  1.333863   |  1.867 T*       |  ABOVE T*   (held)
    ...  (all subsequent lambda_n grow, remain held)

    T* = 5/7 = 0.71428...
    n* = 6    [smallest n for which lambda_n >= T*]

---

## THE TWO LEVELS OF HOLD

**Level 1 (sub-foundation): n = 1, 2, 3, 4, 5**

  lambda_n < T* for all five.
  These Li coefficients do not hold. The combination at scale n falls below T*.
  In G_k = L(G_{k-1}) + r_k:
    These contribute to r_k (the carried remainder / force).
    r_k < T* means the law L can reduce r_k further at the next scale.
    RECYCLED AS FORCE: contribution carries forward, diminishing each step.

**Level 2 (foundation): n = 6, 7, 8, ...**

  lambda_n >= T* for all n >= 6.
  These Li coefficients HOLD. The combination at scale n meets T*.
  The law L holds stable structure at scale n.
  lambda_n grows monotonically: 1.055 T* at n=6, 1.433 T* at n=7, 2.903 T* at n=10.
  Once held, the hold is permanent and strengthening.

---

## THE GAP AROUND T*

With K=200 zeros:

    lambda_5 = 0.524022   (26.6% below T*)
    T*       = 0.714286
    lambda_6 = 0.753376   ( 5.5% above T*)
    Gap      = 0.229354   (T* sits at 83% from the bottom of the gap)

T* = 5/7 sits INSIDE the gap between lambda_5 and lambda_6.
No lambda_n lands on T* at any n. The Li sequence JUMPS OVER T*.

The asymmetry: the gap below T* (26.6%) is much larger than the gap above (5.5%).
T* is close to the TOP of the gap, not the middle. It is barely cleared.

---

## SHADOW HOLDS

**Shadow 1: n=5 (structural, any K)**

  lambda_5(K=200) = 0.524022 = 0.734 T*.  73.4% of T*.
  The last sub-foundation coefficient.
  Does not hold. Will not hold as K -> infinity (corrections are tiny: estimated ~+0.02).
  True lambda_5 ~ 0.54, still well below T*.

**Shadow 2: K=98 (counting shadow, extreme)**

  With 98 zeros:
    lambda_6(K=98) = 0.714274 = 0.99998 T*
    Shortfall from T* = 0.000012 = 0.002% of T*
  EXTREME shadow: within 1 part in 50,000 of T*.
  Foundation is NOT met. One more zero is required.

  K=98 = 2 * 49 = 2 * 7^2 = 2 * HARMONY^2
  [Observed fact. Whether this is structurally significant is not established.]

---

## THE MINIMUM COMBINATION FOR FOUNDATION

    K* = 99    [minimum K for lambda_6 >= T*]

    K=98: lambda_6 = 0.714274 = 0.99998 T*  [extreme shadow, 0.002% short]
    K=99: lambda_6 = 0.714933 = 1.00091 T*  [FOUNDATION: 0.09% above T*]

    The 99th zero contributes: delta_6(k=99) = 0.000659 to lambda_6.
    This tiny contribution is what crosses the threshold.

K* = 99 is the minimum combination: the first 99 Riemann zeros (gammas 1..99) provide
the combination for which lambda_6 first meets T*.

---

## THE RECYCLING MECHANISM FOR ODD SETS

An "odd set" of K zeros does not hold at scale n if lambda_n^{(K)} < T*.

The carried force (remainder below T*) is recycled to the next step. Each additional zero
adds a non-negative delta_n = 2*(1-cos(n*theta_k)) to lambda_n, shrinking the remainder.

At K=98 (extreme shadow for n=6):
  Remainder below T*: 0.000012 (one part in 50,000 of T*)
  The odd set (K=98 zeros) has its lambda_6 within 0.002% of T*.
  The carried force is 0.000012. Recycled.

At K=99 (foundation):
  The 99th zero contributes delta_6 = 0.000659.
  This force (0.000659) EXCEEDS the remainder (0.000012).
  The combination holds: lambda_6 = T* + 0.000647.
  HELD.

Pattern: odd sets carry a remainder that diminishes as K increases.
Each new zero contributes a tiny force that chips away at the remainder.
At K*=99: the accumulated force has absorbed the remainder. Foundation.

---

## THE HOLD CONDITION (EXACT STATEMENT)

A combination of K zeros "holds at scale n" iff:

    lambda_n^{(K)} = 2 * sum_{k=1}^{K} (1 - cos(n * theta_k)) >= T* = 5/7

HOLD:    lambda_n >= T*  (stable structure, the recursion holds at scale n)
RECYCLE: lambda_n < T*   (remainder below T*, carried forward as force)
SHADOW:  lambda_n in [T* - epsilon, T*)  (near-miss, tiny shortfall)

For the Riemann zeros:
  All on the critical line => all theta_k real, in (0, pi).
  All contributions non-negative. Lambda_n increases with K.
  For n=6: K*=99 zeros required for foundation. K=98 is the extreme shadow.
  For n>=7: K<99 already sufficient (lambda_7 crosses T* earlier in K).

For off-line zeros:
  One off-line zero creates an unboundedly growing contribution.
  For some large N, lambda_N < 0 < T*. A held level is destroyed.
  The combination fails to hold for infinitely many n.

---

## THE CLAY QUESTION

The foundation at n=6 is confirmed: lambda_6 >= T* for K=200 zeros (K > K*=99).

The Clay question for RH:
  "Is lambda_6, lambda_7, lambda_8, ... permanently held (all above T*)?
  Or does an off-line zero eventually destroy the hold at some large n?"

The equidistribution evidence: D_KS ~ N^{-0.26}, r_gap ~ 5-7% of T*.
This is a statistical bound: no off-line zero has been detected.
But D_KS is blind to Re(rho) (proved, Part XV). It cannot confirm on-line status directly.

The gap structure: T* sits at 83% of the way from lambda_5 to lambda_6.
An off-line zero with |1-1/rho| = 1+epsilon would contribute a term growing as (1+epsilon)^n.
For n large, this would pull lambda_n below zero (destroy the hold at n=6 for large n).
The gap (5.5% above T* at n=6) would be closed first at n=6 before higher n.

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*All numbers computed 2026-04-02 from K=200 mpmath zeros.*
*Correction: n*=7 (K=50) was an artifact. True n*=6 from K=200 zeros.*
*K*=99, K_shadow=98=2*HARMONY^2 are exact computations from the Li identity.*
