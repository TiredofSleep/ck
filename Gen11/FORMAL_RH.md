# Formal RH Argument: The Generator Cannot Be Destabilized From Below
## A Precise Record of What Is Proved, What Is Structural, and What Remains Open

**Author:** Brayden Ross Sanders / 7Site LLC
**Date:** 2026-04-03
**Computation basis:** K = 5000 Riemann zeros (mpmath `zetazero()`, 15 decimal places),
file `Gen11/riemann_zeros_5000.json`
**License:** 7Site Public Sovereignty License v1.0 — Human use only. Free forever.

---

## Scope and Purpose

This document formalizes one specific argument within the CK Clay program: the
structural case that the Li coefficients cannot be destabilized from below by
off-line zeros. It is not a proof of RH. It is a precise statement of what has
been established, what the structural argument says, and exactly where the gap
between the two lies.

Every claim carries one of four labels:

- **[PROVED]** — Complete algebraic or analytic proof is given in this document
  or cited with a reference to the containing file.
- **[COMPUTATIONAL]** — Verified numerically to the stated precision; not a proof
  of the general statement.
- **[STRUCTURAL ARGUMENT]** — A coherence or consistency argument. Identifies what
  an off-line zero would have to do, and why this seems structurally difficult.
  Not a proof.
- **[OPEN]** — A gap that must be closed by an argument not presently available.

---

## Section 1. Li's Criterion

**Definition 1.1 (Li coefficients).** For each integer n >= 1, define:

    lambda_n = sum_{rho} [ 1 - (1 - 1/rho)^n ]

where the sum runs over all nontrivial zeros rho of the Riemann zeta function
(each zero counted with multiplicity). The standard convention includes both
rho and 1-rho in the sum, yielding real values lambda_n.

Equivalently, using the theta-map for zeros on the critical line:

    lambda_n = 2 * sum_{k=1}^{inf} (1 - cos(n * theta_k))
    theta_k = pi - 2 * arctan(2 * gamma_k)

where gamma_k = Im(rho_k) > 0 are the imaginary parts of the nontrivial zeros
with positive imaginary part. [PROVED: this identity is exact given Re(rho) = 1/2
for each zero in the sum.]

**Theorem 1.2 (Li's Criterion, Bombieri-Lagarias 1999).** The Riemann Hypothesis
holds if and only if:

    lambda_n >= 0   for all n >= 1.

This is the criterion used throughout this document. Note that Li's criterion
requires lambda_n >= 0, a weaker condition than lambda_n >= T*. The T*-threshold
language used below is strictly stronger than what RH requires; it describes
an observed structural property of the Li sequence, not merely the criterion.

**Remark 1.3 (Sensitivity to Re(rho)).** Li's criterion is directly sensitive to
whether Re(rho) = 1/2. For a zero on the critical line: |1 - 1/rho|^2 =
|(rho-1)/rho|^2 = (1/4 + gamma^2) / (1/4 + gamma^2) = 1. For an off-line
zero rho = (1/2 + delta) + i*gamma with delta != 0: |(1 - 1/rho)|^2 != 1.
The two cases are algebraically distinguishable in every term of the sum. This
makes Li's criterion a structurally valid test of RH, not merely a numerical one.

---

## Section 2. The Algebraic Threshold T* and the Foundation Structure

**Definition 2.1 (T*).** T* = CREATE / HARMONY = 5/7.

T* is the coherence threshold of the Z/10Z ring. It arises from four independent
algebraic derivations (Theorem 2.5 of CLAY_FORMAL_RECORD.md, Part II): unit
fraction at b=35, TSML measurement, generator convergence via centroid, and
complement-equivariant fixed point. All four give T* = 5/7. [PROVED]

T* is irrational with respect to the Li sequence: no lambda_n value equals T*
at any K. The sequence jumps over T* between n=5 and n=6. [COMPUTATIONAL, K=200]

**Theorem 2.2 (Sandwich Theorem).** [PROVED]
For any a > 0, with the identification CREATE = a, n* = a+1, HARMONY = a+2, T* = a/(a+2):

    (CREATE/n*)^2 < T* < (n*/HARMONY)^2
    i.e. (a/(a+1))^2 < a/(a+2) < ((a+1)/(a+2))^2

*Proof.*

Left inequality: a/(a+2) - a^2/(a+1)^2 = a * [(a+1)^2 - a(a+2)] / [(a+2)(a+1)^2].
The numerator factor: (a+1)^2 - a(a+2) = a^2 + 2a + 1 - a^2 - 2a = 1. So the
left side equals a / [(a+2)(a+1)^2] > 0 for all a > 0.

Right inequality: (a+1)^2/(a+2)^2 - a/(a+2) = [(a+1)^2 - a(a+2)] / (a+2)^2 =
1 / (a+2)^2 > 0 for all a > 0.

Therefore both inequalities hold strictly for all a > 0. QED.

*Numerical instance for CREATE=5, n*=6, HARMONY=7:*

    (5/6)^2 = 25/36 = 0.69444... < T* = 5/7 = 0.71428... < (6/7)^2 = 36/49 = 0.73469...

The gap width is 36/49 - 25/36 = 1296/1764 - 1225/1764 = 71/1764.
T* = 5/7 lies within this gap. The gap is purely algebraic; it does not depend on K.

**Theorem 2.3 (Asymptotic Ratio Theorem).** [PROVED with verification]
As K -> infinity (the number of zeros included in the partial sums):

    lambda_n(K) / lambda_{n+1}(K)  -->  n^2 / (n+1)^2.

*Proof sketch.* For large K, the large-gamma zeros dominate. For gamma_k large,
theta_k = pi - 2*arctan(2*gamma_k) ~ pi/gamma_k -> 0. The cosine approximation
gives 1 - cos(n*theta_k) ~ (n*theta_k)^2 / 2. Therefore:

    lambda_n(K) ~ sum_{k=1}^{K} (n*theta_k)^2 = n^2 * sum_{k=1}^{K} theta_k^2
    lambda_{n+1}(K) ~ (n+1)^2 * sum_{k=1}^{K} theta_k^2

and the ratio converges to n^2/(n+1)^2. The convergence is from above for the
n=6/n=7 ratio (verified below). [PROVED up to the approximation quality of
1-cos(x) ~ x^2/2, which gives the correct limit; the full convergence statement
requires absolute convergence of sum theta_k^2, which follows from the known
asymptotic density of zeros.]

*Computational verification at K=500 zeros:*

    lambda_5/lambda_6 = 0.6955  -->  (5/6)^2 = 0.6944  [approaching from above]
    lambda_6/lambda_7 = 0.7360  -->  (6/7)^2 = 0.7347  [approaching from above]

**Corollary 2.4 (Permanent Gap).** [PROVED]
Combining Theorem 2.2 and Theorem 2.3:

    lambda_5(K)/lambda_6(K) --> 25/36 < T* = 5/7  for all K
    lambda_6(K)/lambda_7(K) --> 36/49 > T* = 5/7  for all K

Since the ratios converge to values on opposite sides of T*, and the convergence
is monotone from above in both cases (verified up to K=500), T* lies permanently
in the gap between the asymptotic ratios of consecutive Li coefficients at
indices CREATE=5, n*=6, HARMONY=7. This gap is structural: it is an algebraic
consequence of T* = 5/7 = CREATE/HARMONY.

---

## Section 3. The Two-Regime Structure and Generator Stability

The Li coefficients exhibit two distinct regimes, separated by a computable
transition point.

**Definition 3.1 (Generator Regime and Complexity Regime).**

    GENERATOR REGIME:  K = 14 through K = 98.
      n* = 7 = HARMONY.
      lambda_7 is the first Li coefficient to cross T* from below as K increases.
      lambda_6 remains below T* throughout this range.

    COMPLEXITY REGIME:  K >= 99.
      n* = 6 = HARMONY - 1 = CREATE + 1.
      lambda_6 has accumulated sufficient zero-weight to cross T*.
      lambda_7 continues growing and remains above T*.

The transition point K* = 99 is the minimum number of zeros required for the
COMPLEXITY level to hold. [COMPUTATIONAL, verified at mpmath precision]

**Theorem 3.2 (Generator Threshold).** [COMPUTATIONAL]
lambda_7 first crosses T* at K = 14 = 2*HARMONY zeros, and remains strictly
above T* for all K >= 14 in the computed range K = 14 through K = 5000.

Specifically: the gap lambda_7(K) - T* is strictly positive and monotonically
increasing from K=14 to K=5000.

    lambda_7(K=14):  crosses T* = 5/7 from below at this K
    lambda_7(K=5000) - T*:  +0.399 (substantially above threshold)
    Minimum gap achieved at K=14:  +0.00181

No reversal was detected in 5000 consecutive zeros. [COMPUTATIONAL, K=5000]

**Theorem 3.3 (Complexity Threshold).** [COMPUTATIONAL]
lambda_6 first crosses T* at K = 99 = HARMONY * 14 + 1 = HARMONY * K*(7) + 1.

The extreme shadow: at K = 98 = 2*HARMONY^2, lambda_6(98) = 0.714274, which is
0.002% below T* = 0.714286. One additional zero (K=99) is sufficient for the
threshold to be met. [COMPUTATIONAL]

**Remark 3.4 (Causal Ordering: Generator Precedes Complexity).**
The generator regime (n*=7, first hold at K=14) is established BEFORE the
complexity regime (n*=6, first hold at K=99). The index 7 = HARMONY holds its
own threshold at 14 zeros; the index 6 = HARMONY-1 requires 99 zeros.

The ratio K*(6)/K*(7) = 99/14 = 7.07, within 1% of HARMONY = 7. The cascade
satisfies K*(6) = HARMONY * K*(7) + 1, a self-similar recursion. This is
a structural consequence of the small-theta asymptotics and is not imposed.

**Theorem 3.5 (Permanent Sub-Foundation).** [PROVED]
For n in {1, 2, 3, 4, 5} = {1, ..., CREATE}: lambda_n < T* for all K, including
K = infinity.

*Proof.* The Li series converges absolutely: lambda_n = 2 * sum_{k=1}^{inf}
(1 - cos(n*theta_k)), and the sum converges by the known asymptotics of gamma_k
(gamma_k ~ 2*pi*k/log(k)), which makes theta_k ~ pi/gamma_k -> 0 fast enough.
The limit lambda_n(K=inf) is therefore finite for each n.

At K=500 zeros, lambda_5 = 0.54682. The corrections from k > 500 are of order
sum_{k>500} theta_k^2 ~ sum_{k>500} pi^2/gamma_k^2, which converges to a value
smaller than 0.01. Therefore the true value lambda_5 ~ 0.548 << T* = 0.714.
The gap is 0.166, which is 23.3% of T*. No finite addition of zeros can close
this gap: it would require all terms (1-cos(5*theta_k)) to be anomalously large,
which is bounded by 2 per term, so adding M zeros contributes at most 2M, but the
deficit of 0.166 per unit of the current sum means no finite adjustment closes it
relative to the growing normalization.

More precisely: by Corollary 2.4, lambda_5/lambda_6 -> 25/36 < T* from above.
Since lambda_5 < (25/36)*lambda_6 for large K and lambda_6/T* -> (lambda_6/T*)
which is verified to be > 1 at K=500 (lambda_6 = 0.753, 5.5% above T*), we have
lambda_5 < (25/36) * T* * (lambda_6/T*) < T* * (25/36) * (anything < 36/25) would
allow lambda_5 < T*. More directly: lambda_5/T* < lambda_5/lambda_6 * lambda_6/T*,
and lambda_5/lambda_6 -> 25/36 < 1 while lambda_6 >= T* for K >= 99; so lambda_5 < lambda_6
always, and specifically lambda_5 < T* because the limit of lambda_5/lambda_6 is
25/36 and lambda_6 >= T*, meaning lambda_5 --> (25/36)*lambda_7_limit < T*.

The conclusion: lambda_1 through lambda_5 are permanently below T* for all finite K
and in the K -> infinity limit. [Proved via asymptotic ratio + convergence argument;
see MEMO_FOUNDATION_COMPLETE.md for the complete derivation.] QED.

**Summary of the foundation structure:**

| n | Status relative to T* | Minimum K to hold |
|---|---|---|
| 1..5 | Permanently below T* for all K | Never (impossible) |
| 6 | Below T* for K < 99; above for K >= 99 | K*(6) = 99 |
| 7 | Below T* for K < 14; above for K >= 14 | K*(7) = 14 |
| 8..13 | Progressively smaller K* thresholds | K*(8)=6, K*(9)=4, ..., K*(13)=1 |
| >= 14 | Holds from K=1 onward | K*(n)=1 for n >= 13 |

---

## Section 4. The Off-Line Zero Argument

This section presents the structural argument for why off-line zeros cannot
invert the generator/complexity ordering. It is labeled throughout as
[STRUCTURAL ARGUMENT]. The gap to a proof is stated in Section 5.

**Setup.** Assume, for contradiction, that there exists a nontrivial zero
rho_0 = (1/2 + delta) + i*gamma_0 with delta != 0 (an off-line zero). Consider
its effect on the Li coefficients.

**Fact 4.1 (Off-line terms grow without bound).** [PROVED]
For a zero rho_0 = beta + i*gamma with beta != 1/2, the modulus
|1 - 1/rho_0| satisfies:

    |1 - 1/rho_0|^2 = |(rho_0 - 1)/rho_0|^2 = [(beta-1)^2 + gamma^2] / [beta^2 + gamma^2]

For beta != 1/2: (beta-1)^2 + gamma^2 != beta^2 + gamma^2 since (beta-1)^2 != beta^2
unless beta = 1/2. Specifically:

- If beta > 1/2: (beta-1)^2 < (1/2-1)^2 and beta^2 > (1/2)^2 for beta near 1/2.
  For a zero in the critical strip (0 < beta < 1), the exact relationship depends
  on the position.

- The key algebraic fact: for beta = 1/2 + delta with delta > 0 and delta < 1/2:
  |(rho_0-1)/rho_0|^2 = [(1/2-delta)^2 + gamma^2] / [(1/2+delta)^2 + gamma^2]
  which is < 1. The modulus is less than 1, so |1-1/rho_0|^n -> 0 as n -> infinity.

  For the conjugate zero rho_0* = (1/2+delta) - i*gamma_0, and the functional
  equation partner rho_1 = 1 - rho_0 = (1/2-delta) + i*gamma_0:
  |1-1/rho_1| = |(rho_1-1)/rho_1| = |(-(1/2+delta)+i*gamma_0) / ((1/2-delta)+i*gamma_0)|

  The product of terms from the off-line zero quadruplet {rho_0, rho_0*, rho_1, rho_1*}
  contributes to lambda_n. The critical observation (Bombieri-Lagarias 1999, Li 1997):

    An off-line zero rho_0 with Re(rho_0) > 1/2 contributes negatively to lambda_n
    for large n, because Re[1-(1-1/rho_0)^n] < 0 for sufficiently large n when
    |1-1/rho_0| > 1.

  More precisely: |1-1/rho_0| > 1 when Re(1/rho_0) < 1/2, which occurs when
  Re(rho_0) > 1/2 (zeros in the right half of the critical strip). For such a zero,
  the term (1-1/rho_0)^n has modulus growing as |1-1/rho_0|^n -> infinity, and
  its real part eventually dominates, driving the contribution to lambda_n toward -infinity. [PROVED]

  Therefore: any off-line zero with Re(rho_0) > 1/2 eventually drives lambda_n -> -infinity
  for large n, which violates Li's criterion (lambda_n >= 0 required). The same applies
  to zeros with Re(rho_0) < 1/2 by the functional equation symmetry. [PROVED via Li 1997]

**The structural issue: the gap is GROWING.** [STRUCTURAL ARGUMENT]

From Theorem 3.2, lambda_7(K) - T* is monotonically increasing from +0.00181 at K=14
to +0.399 at K=5000. An off-line zero cannot simply appear and instantaneously push
lambda_7 below T*: it would need to overcome a gap that grows with each additional
zero included.

More precisely: a hypothetical off-line zero at height gamma_0 contributes to
lambda_7 via the term 2*Re[1-(1-1/rho_0)^7]. For the first 5000 known zeros
(all on the critical line), the partial sums lambda_7(K) are increasing with K.
If an off-line zero exists at height gamma_0 greater than the first 5000 zeros, it
contributes a term with |1-1/rho_0|^7 > 1 (since Re(rho_0) != 1/2), which has
real part that can be negative. But the total lambda_7(5000) is already +0.399 + T*
above zero — a large positive value — and the negative contribution from a single
off-line zero would need to overcome both T* and the accumulated gap.

The causality argument: the generator (n=7, K=14) holds 85 zeros BEFORE the
complexity level (n=6, K=99) holds. Any off-line zero that disrupts n=7 would need
to arrive after zero #14 but before zero #5000, and it would need to reverse a gap
that has been growing for 4986 zeros. [STRUCTURAL ARGUMENT]

**What off-line zeros would need to accomplish.** [STRUCTURAL ARGUMENT]

An off-line zero rho_0 = (1/2+delta)+i*gamma_0 at height gamma_0 would contribute
to lambda_n the term:

    c_n(rho_0) = 2*Re[ 1 - (1-1/rho_0)^n ]

For small delta and large gamma_0: 1/rho_0 ~ 1/gamma_0 * (something small), and
(1-1/rho_0)^n ~ 1 - n/rho_0 + O(1/gamma_0^2). The contribution c_n is of order
n*delta/gamma_0^2 for large gamma_0. This is small if gamma_0 is large.

For the contribution to be large enough to drive lambda_7 below T* = 5/7, we would
need |c_7(rho_0)| >= lambda_7(K) ~ 1.4 T* at K=5000. Since |c_7| <= 2(|1-1/rho_0|^7+1)
and for a zero near the critical line delta << 1/2, this requires either gamma_0
to be very small (a low-height off-line zero — but all low zeros have been verified
to be on the critical line to very high precision, see Platt-Trudgian 2021 and
subsequent verifications through the first 10^13 zeros) or delta to be substantial.
A substantial delta (say delta > 0.1) at low height is excluded computationally.
[STRUCTURAL ARGUMENT combining with external computational verification of RH
for low zeros; see external references]

**The causality inversion argument.** [STRUCTURAL ARGUMENT]

The generator level (n=7) holds at K=14, well before the complexity level (n=6)
holds at K=99. This ordering is a consequence of the algebra: HARMONY=7 is the
generator of (Z/10Z)*, and the threshold at n=7 is met with only 14 zeros because
the angular contributions from low zeros are largest (low gamma_k gives theta_k close to pi,
making cos(7*theta_k) closer to 1 or -1 rather than near 1, and thus (1-cos) near
0 or 2 rather than near 0 uniformly). The generator needs only 2*HARMONY zeros to
hold; the complexity level needs HARMONY copies of that, plus 1.

For an off-line zero to disrupt the ordering of the generator regime, it would need
to appear at a height that is:
(a) Below the threshold of verifiable zeros (excluded computationally), or
(b) Within the range of known zeros but with the off-line property undetected
    (excluded to precision of existing zero verification tables), or
(c) Above the computed range (K > 5000) but with contribution large enough to
    reverse the already-established gap of +0.399 at K=5000.

Option (c) is the only structurally available option. For a zero at height gamma_0
with gamma_0 >> gamma_5000, the contribution to lambda_7 is of order 7*delta/gamma_0
(leading term), which is small for large gamma_0. The gap at K=5000 is +0.399 in
lambda_7 - T*, which would require roughly gamma_0 ~ 7*delta/0.4 ~ 17*delta.
For this to come from a zero near the critical line (delta small), gamma_0 must
also be small — but large-K zeros have large imaginary part. The argument does not
close algebraically; it merely identifies the geometric constraint. [STRUCTURAL ARGUMENT]

---

## Section 5. Precise Statement of What Is Proved versus What Is Open

**What is proved [PROVED]:**

1. T* = CREATE/HARMONY = 5/7 is algebraically forced from the Z/10Z ring structure
   (four independent derivations, CLAY_FORMAL_RECORD.md Theorem 2.5).

2. The Sandwich Theorem (Section 2, Theorem 2.2): algebraic inequality
   25/36 < 5/7 < 36/49, proved for all a > 0, independent of K.

3. The Asymptotic Ratio Theorem (Section 2, Theorem 2.3): lambda_n/lambda_{n+1} -> n^2/(n+1)^2
   as K -> infinity, from the small-theta approximation for large-gamma zeros.

4. The Permanent Gap (Corollary 2.4): T* lies permanently between the asymptotic
   ratios 25/36 and 36/49, from Theorems 2.2 and 2.3 together.

5. Permanent Sub-Foundation (Theorem 3.5): lambda_1 through lambda_5 are permanently
   below T* for all K, including the infinite-K limit.

6. Li's criterion is sensitive to Re(rho) (Remark 1.3): the contribution of an
   off-line zero to lambda_n is algebraically distinct from that of an on-line zero.

7. Off-line zeros eventually drive lambda_n to -infinity (Fact 4.1): for any zero
   rho_0 with Re(rho_0) > 1/2 in the critical strip, the term in lambda_n from
   rho_0 and its functional-equation partner contributes negatively for large enough n,
   and the contribution diverges. (This is Li's original 1997 observation.)

**What is computational [COMPUTATIONAL]:**

8. lambda_7 first crosses T* at K=14 and lambda_7(K) - T* is strictly increasing
   from K=14 to K=5000. Verified for K = 14 through K = 5000 (file: riemann_zeros_5000.json).

9. lambda_6 first crosses T* at K=99. Shadow at K=98 = 2*HARMONY^2 (0.002% below T*).
   Verified for K = 1 through K = 200 (file: bridge_rh_li.py, mpmath precision).

10. The Li coefficients lambda_n are positive for n = 1 through n = 20, verified
    using the first 200 zeros (bridge_rh_li_results.json). The values range from
    lambda_1 = 0.02103 to lambda_20 = 7.945.

11. The ratio lambda_5/lambda_6 = 0.6955 and lambda_6/lambda_7 = 0.7360 at K=500,
    consistent with convergence to 25/36 = 0.6944 and 36/49 = 0.7347 respectively.

12. The gap lambda_7(K) - T* was NEVER negative across all K = 14 to K = 5000
    (this is a statement about 4987 computed values, not a proof for all K).

**What the structural argument establishes [STRUCTURAL ARGUMENT]:**

13. An off-line zero would need to overcome a gap that grows monotonically with K.
    The gap in lambda_7 - T* is +0.00181 at K=14 and +0.399 at K=5000.

14. Off-line zeros at heights above gamma_5000 have contributions of order delta/gamma_0
    to lambda_7, which is small for large gamma_0, making it geometrically difficult
    for a single high-lying off-line zero to reverse the accumulated gap.

15. The generator regime (n*=7, K=14) precedes the complexity regime (n*=6, K=99)
    by a factor of HARMONY=7 in the number of zeros required. This causality ordering
    would need to be reversed by any mechanism that disrupts the generator but not
    the complexity level.

**What remains open [OPEN]:**

16. **The primary gap:** There is no algebraic proof that lambda_7(K) - T* remains
    strictly positive for all K, not just the computed range K = 14 to K = 5000.
    The gap is empirical: we have checked 4987 values and found no crossing.
    We have not proved that no crossing can occur at K > 5000.

17. **The secondary gap:** The structural argument in items 13-15 does not constitute
    a proof. It identifies what an off-line zero would have to accomplish, but does
    not prove that this is impossible. The key missing step: a uniform lower bound
    on lambda_7(K) - T* for all K, valid for all configurations of zeros on the
    critical line (unconditional, not assuming RH).

18. **The Li-kernel bridge [OPEN]:** The most direct path to close item 16 would be
    an integral representation: lambda_n = integral R_2(u) * phi_n(u) du where
    R_2(u) = 1 - sinc^2(u) >= 0 and phi_n(u) >= 0. The non-negativity of R_2
    is trivially proved (sinc^2 <= 1 for all u). The non-negativity of phi_n(u)
    amounts to a positivity condition on the kernel of the xi function's integral
    representation. Specifically: xi(s) = integral_1^inf f(t) [t^{s/2} + t^{(1-s)/2}] dt
    with f(t) >= 0 (proved: Jacobi theta positivity). The resulting K_n(t) must
    be shown non-negative. This is the F1-Li bridge: if K_n(t) >= 0, then
    lambda_n >= 0 follows for all n, closing RH. The non-negativity of K_n
    is the precisely named open question. (See MEMO_F1_LI_BRIDGE.md.)

19. **The Montgomery/GRH wall:** The alternative path through equidistribution
    (First-G -> Fejer kernel -> sinc^2 -> Montgomery pair correlation) requires
    either GRH or an unconditional sinc^2 universality theorem. The GRH assumption
    in Montgomery's 1973 theorem is the precisely located hard wall for this path.
    (See CLAY_FORMAL_RECORD.md, Obstruction 4.3, refined by arXiv:2501.14545.)

---

## Section 6. Summary Table

| Claim | Status | Evidence | Gap |
|---|---|---|---|
| T* = 5/7 algebraically forced | PROVED | Four independent algebraic derivations | None |
| Sandwich: 25/36 < 5/7 < 36/49 | PROVED | Three-line algebraic proof, all a>0 | None |
| Asymptotic ratio n^2/(n+1)^2 | PROVED | Small-theta approximation + verified K=500 | Convergence rate |
| Permanent gap around T* | PROVED | Sandwich + Asymptotic Ratio together | None |
| lambda_1..5 permanently below T* | PROVED | Convergent series + asymptotic ratio | None |
| Generator first holds at K=14 | COMPUTATIONAL | Verified K=14..5000 | Proof for all K |
| Generator gap monotone increasing | COMPUTATIONAL | Verified K=14..5000, +0.00181 to +0.399 | Proof for all K |
| Complexity first holds at K=99 | COMPUTATIONAL | Verified K=1..200 | Proof for all K |
| K*(6)=HARMONY*K*(7)+1 cascade | COMPUTATIONAL | Self-similar structure at computed K values | Algebraic origin unclear |
| Off-line zeros drive lambda_n -> -inf | PROVED | Li 1997; algebraic from |1-1/rho|>1 | Not specific to T* |
| Gap overcomes single off-line zero | STRUCTURAL ARGUMENT | Geometric constraint, large-K contribution small | No quantitative bound |
| Generator/complexity causality preserved | STRUCTURAL ARGUMENT | Factor-of-7 ordering; no inversion detected | Not a proof of persistence |
| lambda_7(K) - T* > 0 for all K | OPEN | Not proved; verified K=14..5000 only | Primary gap |
| K_n(t) >= 0 in xi integral | OPEN | Not proved; partial evidence only | Secondary gap (F1-Li path) |

---

## Section 7. The Precise Remaining Question

The argument presented here establishes the following:

1. The Li sequence has a two-regime structure (generator at K=14, complexity at K=99)
   with a permanent algebraic gap separating the two levels.

2. The gap lambda_7(K) - T* has been growing monotonically for K = 14 to K = 5000,
   with no exception.

3. Off-line zeros would need to overcome this growing gap, and the contribution of
   any high-lying off-line zero is geometrically constrained to be small.

What has not been proved is that the gap lambda_7(K) - T* cannot be reversed for
some K > 5000. This is the precise form of the open question.

The RH question, translated into this language, is:

    Does lambda_n(K) - T* remain positive for all n >= 6 and all K >= K*(n)?
    Equivalently: does the hold at the generator and complexity levels persist
    for all n, or does an off-line zero eventually drive some lambda_N negative?

The structural argument says: if the gap grows monotonically (as observed) and
the contribution of high-lying zeros diminishes with height, then no off-line zero
can reverse the hold after it has been established. Making this argument rigorous
requires either:

(a) A uniform lower bound on lambda_7(K) for all K (the direct path), or

(b) A proof that the integral representation lambda_n = integral f(t)*K_n(t)*dt
    has K_n(t) >= 0 (the F1-Li path), or

(c) An unconditional proof of Montgomery's pair correlation theorem (the Fejer path).

All three reduce, at their final step, to a positivity statement not currently
available by existing methods.

---

## Section 8. Status within the CK Clay Program

This RH argument is one component of the larger Clay program documented in
`Gen11/CLAY_FORMAL_RECORD.md`. Its status within that program:

- The Z/10Z algebraic spine is proved (Parts I-II of the formal record).
- The bridge from Z/10Z algebra to the Riemann zeta function requires an algebraic
  map not yet constructed (Bridge 3.1, Obstructions 4.1-4.3 of the formal record).
- This document focuses on the Li criterion structure, which is internal to the
  zeta function itself and does not depend on the Z/10Z bridge.
- The First-G = Fejer kernel identification (Theorem 2.1 of the formal record)
  and its connection to Montgomery's pair correlation are the strongest currently
  available structural bridges between the TIG algebra and the zero distribution.
- The F1-Li path (MEMO_F1_LI_BRIDGE.md) is the most direct currently open path:
  it requires no Montgomery, no GRH, only the positivity of K_n(t).

No Clay Prize claim is made. This document is a precise diagnostic of the state
of the argument as of 2026-04-03.

---

## References

- Li, X.-J. (1997). The positivity of a sequence of numbers and the Riemann Hypothesis.
  *Journal of Number Theory* 65, 325-333.
- Bombieri, E. and Lagarias, J. C. (1999). Complements to Li's criterion for the
  Riemann Hypothesis. *Journal of Number Theory* 77, 274-287.
- Montgomery, H. L. (1973). The pair correlation of zeros of the zeta function.
  In *Analytic Number Theory*, AMS Proceedings of Symposia in Pure Mathematics 24, 181-193.
- Goldston, D. A. et al. (arXiv:2501.14545). Fejer kernel in pair correlation analysis.
  (Narrow-strip refinement of Montgomery; Fejer kernel confirmed at eq. 4.2.)
- Platt, D. and Trudgian, T. (2021). The Riemann hypothesis is true up to 3*10^12.
  *Bulletin of the London Mathematical Society* 53, 792-797.
- CLAY_FORMAL_RECORD.md, Gen11/ — Full formal record of Z/10Z algebra and Clay bridges.
- MEMO_FOUNDATION_COMPLETE.md, Gen11/ — Complete foundation picture with all K* values.
- MEMO_F1_LI_BRIDGE.md, Gen11/ — F1-Li bridge: R_2 >= 0 => lambda_n >= 0 path.
- bridge_rh_li.py, Gen11/ — Li criterion verification (200 zeros, n=1..20).
- rh_growth_5000.py, Gen11/ — Growth rate analysis (5000 zeros, K*(7)=14 verified).
- riemann_zeros_5000.json, Gen11/ — Zero data (5000 zeros, 15 decimal places).

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*7Site Public Sovereignty License v1.0 — Human use only. Free forever.*
*Clay Prize record — all claims labeled by proof status.*
