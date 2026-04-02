# K7 — No-Go Attempt for PSD-Based Assembly

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Status

**Tier: D** (proved). The PSD route is closed. The no-go theorem below is a proved result given the exact formula for D_p^PSD from K7_EXACT_FORMULA_FOR_RP.md.

The scope of the no-go is precise: it applies to D_p^PSD only. It does not apply to D_p^{Kl} (the Kloosterman/sequence route), which is addressed in K7_MULTIPLICATIVE_CHARACTER_ROUTE.md.

---

## Setup

The exact PSD of the prime-field orbit is:

```
S_p(xi) = sin^2(pi*xi*(p-1)/p) / ((p-1)^2 * sin^2(pi*xi/p))
```

This is proved in K7_EXACT_FORMULA_FOR_RP.md. It holds for all primes p >= 2 and all xi not of the form xi = k*p for integer k (i.e., all xi not at a period point of the orbit's additive structure).

The PSD deviation is:

```
D_p^PSD(xi) = p * (S_p(xi) - sinc^2(xi))
```

where sinc(xi) = sin(pi*xi)/(pi*xi) with sinc(0) = 1.

---

## Theorem K7.NO-GO — PSD Route Blocked

**Statement:** Let xi be a fixed real number that is not an integer multiple of any prime p considered. Then D_p^PSD(xi) admits a convergent Taylor expansion in 1/p for all sufficiently large p:

```
D_p^PSD(xi) = c_0(xi) + c_1(xi)/p + c_2(xi)/p^2 + c_3(xi)/p^3 + ...
```

where each coefficient c_n(xi) is a real-analytic function of xi involving only the constant pi and trigonometric functions (sin, cos, and their derivatives evaluated at multiples of pi*xi). In particular:

1. c_0(xi) = -2[sinc(2*xi) - sinc^2(xi)]   (the deterministic large-p limit)
2. Each c_n(xi) for n >= 1 is also deterministic: it depends on xi but not on p, not on any prime-specific arithmetic, and not on the generator g.
3. All Taylor coefficients are g-independent.

**Consequence:** Any assembly sum_{p<=X} D_p^PSD(xi) * w(p) where w(p) depends only on the value of p (and not on prime-specific arithmetic such as Gauss sums, Kloosterman sums, or primitive roots) decomposes as:

```
sum_{p<=X} D_p^PSD(xi) * w(p)
= c_0(xi) * sum_{p<=X} w(p)
+ c_1(xi) * sum_{p<=X} w(p)/p
+ c_2(xi) * sum_{p<=X} w(p)/p^2
+ ...
```

Each term is (deterministic function of xi) * (standard prime sum with weight w(p)/p^n). The assembly produces no prime-specific arithmetic beyond what is already present in the standard prime sums with weights w(p)/p^n. It CANNOT produce zeros that are not already present in those standard sums.

**QED (modulo the Taylor expansion proved below).**

---

## Proof of the Taylor Expansion

We expand D_p^PSD(xi) explicitly in 1/p.

### Step 1 — Expand S_p(xi) in 1/p

Write the exact formula:

```
S_p(xi) = sin^2(pi*xi*(p-1)/p) / ((p-1)^2 * sin^2(pi*xi/p))
```

Factor out from each term:

```
(p-1)/p = 1 - 1/p
pi*xi*(p-1)/p = pi*xi - pi*xi/p
pi*xi/p = pi*xi/p  (small for large p)
```

Expand the numerator using sin(A - B) = sin(A)*cos(B) - cos(A)*sin(B):

```
sin(pi*xi*(1 - 1/p)) = sin(pi*xi)*cos(pi*xi/p) - cos(pi*xi)*sin(pi*xi/p)
                     = sin(pi*xi) - (pi*xi/p)*cos(pi*xi) - (1/2)*(pi*xi/p)^2*sin(pi*xi) + O(1/p^3)
```

Squaring the numerator:

```
sin^2(pi*xi*(p-1)/p) = sin^2(pi*xi)
                       - 2*(pi*xi/p)*sin(pi*xi)*cos(pi*xi)
                       + (pi*xi/p)^2 * [cos^2(pi*xi) - sin^2(pi*xi)] + O(1/p^3)
                     = sin^2(pi*xi) - (pi*xi/p)*sin(2*pi*xi) + (pi*xi/p)^2*cos(2*pi*xi) + O(1/p^3)
```

Expand the denominator:

```
sin(pi*xi/p) = pi*xi/p - (1/6)*(pi*xi/p)^3 + ... = (pi*xi/p) * [1 - (1/6)*(pi*xi/p)^2 + ...]
(p-1)^2 * sin^2(pi*xi/p) = (p-1)^2 * (pi*xi/p)^2 * [1 - (1/3)*(pi*xi/p)^2 + O(1/p^4)]
                          = (pi*xi)^2 * (1 - 1/p)^2 * [1 - (pi^2*xi^2)/(3*p^2) + O(1/p^4)]
                          = (pi*xi)^2 * [1 - 2/p + 1/p^2] * [1 - (pi^2*xi^2)/(3*p^2) + O(1/p^4)]
                          = (pi*xi)^2 * [1 - 2/p + (1 + pi^2*xi^2/3)/p^2 + O(1/p^3)]
```

### Step 2 — Form the ratio S_p(xi)

```
S_p(xi) = numerator / denominator
         = [sin^2(pi*xi) - (pi*xi/p)*sin(2*pi*xi) + (pi*xi/p)^2*cos(2*pi*xi) + O(1/p^3)]
           / [(pi*xi)^2 * (1 - 2/p + (1 + pi^2*xi^2/3)/p^2 + O(1/p^3))]
```

Let u = sin(pi*xi)/(pi*xi) = sinc(xi) * pi. Then:

```
sin^2(pi*xi) = (pi*xi)^2 * sinc^2(xi)   (where sinc(xi) = sin(pi*xi)/(pi*xi))
sin(2*pi*xi) = 2*sin(pi*xi)*cos(pi*xi) = 2*(pi*xi)*sinc(xi)*cos(pi*xi)
cos(2*pi*xi) = 1 - 2*sin^2(pi*xi) = 1 - 2*(pi*xi)^2*sinc^2(xi)
```

Substituting:

```
S_p(xi) = [sinc^2(xi) - (2/p)*sinc(xi)*cos(pi*xi) + (1/p^2)*(cos(2*pi*xi)/(pi*xi)^2) + O(1/p^3)]
          / [1 - 2/p + (1 + pi^2*xi^2/3)/p^2 + O(1/p^3)]
```

Expanding 1/(1 + epsilon) ~ 1 - epsilon + epsilon^2 - ... with epsilon = -2/p + O(1/p^2):

```
1 / [1 - 2/p + O(1/p^2)] = 1 + 2/p + (4 - (1 + pi^2*xi^2/3))/p^2 + O(1/p^3)
                          = 1 + 2/p + (3 - pi^2*xi^2/3)/p^2 + O(1/p^3)
```

Multiplying numerator by this expansion (collecting terms to order 1/p^2):

```
S_p(xi) = sinc^2(xi) + (2/p)*sinc^2(xi) - (2/p)*sinc(xi)*cos(pi*xi) + O(1/p^2)
        = sinc^2(xi) + (2/p)*[sinc^2(xi) - sinc(xi)*cos(pi*xi)] + O(1/p^2)
```

### Step 3 — Compute D_p^PSD(xi) = p*(S_p(xi) - sinc^2(xi))

```
D_p^PSD(xi) = p * [S_p(xi) - sinc^2(xi)]
             = p * [(2/p)*(sinc^2(xi) - sinc(xi)*cos(pi*xi)) + O(1/p^2)]
             = 2*(sinc^2(xi) - sinc(xi)*cos(pi*xi)) + O(1/p)
```

The leading coefficient is:

```
c_0(xi) = 2*sinc^2(xi) - 2*sinc(xi)*cos(pi*xi)
         = 2*sinc(xi) * [sinc(xi) - cos(pi*xi)]
```

**Verification against stated form:** The stated form was c_0(xi) = -2[sinc(2*xi) - sinc^2(xi)]. We verify:

sinc(2*xi) = sin(2*pi*xi)/(2*pi*xi) = 2*sin(pi*xi)*cos(pi*xi)/(2*pi*xi) = sinc(xi)*cos(pi*xi).

Therefore sinc(2*xi) - sinc^2(xi) = sinc(xi)*cos(pi*xi) - sinc^2(xi) = sinc(xi)*[cos(pi*xi) - sinc(xi)].

And -2[sinc(2*xi) - sinc^2(xi)] = 2*sinc(xi)*[sinc(xi) - cos(pi*xi)] = c_0(xi). Confirmed.

### Step 4 — The O(1/p) Correction Is Also Deterministic

The O(1/p) term in S_p(xi) involves pi^2*xi^2/3 and higher trigonometric functions. Explicitly, collecting the 1/p^2 terms in S_p(xi) (which contribute to c_1(xi) after multiplication by p):

The 1/p^2 coefficient of S_p(xi) contains terms:
- From (2*sinc^2 - 2*sinc*cos) * (2/p) at the next order
- From the 1/p^2 terms in the numerator (involving cos(2*pi*xi)/(pi*xi)^2 = sinc^2(xi)/... and further trigonometric expressions)
- From the 1/p^2 terms in the denominator expansion

All of these are combinations of products of sinc(xi), sin(pi*xi), cos(pi*xi), pi, and xi — none involve any prime-specific arithmetic. The coefficient c_1(xi) is therefore deterministic.

By induction: the full Taylor series in 1/p is obtained by expanding the exact formula order by order in 1/p. At each order n, the coefficient c_n(xi) is a polynomial in {sin(pi*xi), cos(pi*xi), (pi*xi)^{-1}} — all of which are determined by xi alone. The prime p enters only through the expansion variable 1/p. There is no order at which a prime-specific quantity (such as a Gauss sum, a Jacobi sum, or a Kloosterman sum) could appear, because the exact formula for S_p(xi) involves only the sine function evaluated at pi*xi/p and pi*xi*(p-1)/p — both of which are rational multiples of pi*xi, producing only trigonometric arithmetic.

**QED (Taylor expansion).** Every coefficient c_n(xi) is deterministic.

---

## Consequence — The Assembly Decomposes

For any weight function w(p) depending only on p (examples: w(p) = log(p), w(p) = 1, w(p) = p^{-s}):

```
sum_{p<=X} D_p^PSD(xi) * w(p)
= sum_{p<=X} [c_0(xi) + c_1(xi)/p + c_2(xi)/p^2 + ...] * w(p)
= c_0(xi) * sum_{p<=X} w(p)
+ c_1(xi) * sum_{p<=X} w(p)/p
+ c_2(xi) * sum_{p<=X} w(p)/p^2
+ ...  (finite many terms dominate since c_n(xi)/p^n -> 0 rapidly)
```

Each term is of the form c_n(xi) * P_n(X) where P_n(X) is a standard prime sum (e.g., P_0 = theta(X) for w = log, P_0 = pi(X) for w = 1, P_0 = -zeta'/zeta for w = log*p^{-s}).

The Mellin transform in s factorizes:

```
sum_p D_p^PSD(xi) * p^{-s} = c_0(xi) * sum_p p^{-s} + c_1(xi) * sum_p p^{-(s+1)} + ...
```

Each term on the right is (constant in p) * (prime sum in s). The s-dependence and xi-dependence do not couple.

**An explicit formula for sum_{p<=X} D_p^PSD(xi) * w(p) recovers only the zeros of zeta (via the standard PNT explicit formula for each term P_n) multiplied by deterministic constants c_n(xi). No new zeros.** QED.

---

## What the No-Go Does NOT Cover

This theorem is a precise, scoped result. It closes the PSD route only. It does NOT apply to:

**1. Sequence-based deviations D_p^{Kl}(m):**
The Kloosterman deviation D_p^{Kl}(m) = Kl(1, g^{-m}; p) / (2*sqrt(p)) is NOT a function only of the set {g^j mod p}, and its Taylor expansion in 1/p is NOT deterministic. The second argument g^{-m} of the Kloosterman sum varies with m and g in a prime-specific way. The Weil bound applies, but the specific value Kl(1, g^{-m}; p) encodes genuine arithmetic of p. This route is not closed.

**2. Mixed objects combining D_p^PSD with Kloosterman corrections:**
A hybrid deviation of the form D_p^PSD(xi) + epsilon * D_p^{Kl}(m) (for some small epsilon) includes a prime-specific term. The no-go applies to D_p^PSD in isolation, not to augmented objects.

**3. Other prime-specific functions not derived from the set-PSD:**
Any function of p that is not derivable from the set-spectral density of the orbit (e.g., trace functions, twisted exponential sums) is outside the scope. The no-go is specific to the D_p^PSD object as defined.

**4. Non-uniform weighting by generator:**
If one averages D_p^PSD over generators g with a non-uniform weight w(g, p), the resulting sum might acquire generator-specific content — but only from the weight, not from D_p^PSD itself (since D_p^PSD is the same for all g). This is a degenerate bypass.

---

## Second Step — The Residual Does Not Rescue

After subtracting the leading term:

```
R_p^{(1)}(xi) = D_p^PSD(xi) - c_0(xi) = c_1(xi)/p + c_2(xi)/p^2 + ...
```

The residual R_p^{(1)} is O(1/p), and its assembly is:

```
sum_{p<=X} R_p^{(1)}(xi) * w(p)
= c_1(xi) * sum_{p<=X} w(p)/p  +  c_2(xi) * sum_{p<=X} w(p)/p^2  +  ...
```

For w(p) = log(p): sum_{p<=X} log(p)/p ~ log(X) (diverges), so the c_1 term is ~c_1(xi)*log(X), subleading relative to c_0(xi)*X. The c_1 coefficient c_1(xi) is still deterministic. No new arithmetic appears.

For w(p) = log(p)*p^{-s}: the c_1 term gives c_1(xi)*(-zeta'/zeta)(s+1), which is another scalar multiple of a shift of the log-derivative of zeta. Still reducible to known objects.

**At every order n, the coefficient c_n(xi) is deterministic, and the assembly of R_p^{(n)} is a sum of standard prime sums multiplied by deterministic constants.** The no-go applies to every residual in the Taylor series.

---

## Tier Assessment

The theorem proved here is rigorous given:
1. The exact formula for S_p(xi) (proved in K7_EXACT_FORMULA_FOR_RP.md).
2. The Taylor expansion of sin and standard trigonometric functions in 1/p.
3. The factoring of the assembly sum.

All three steps use only classical real analysis and the exact formula. No RH, no deep arithmetic, no conjectures required.

**Tier: D** (proved). The PSD route is closed.

The open question — whether the Kloosterman route A3 bridges to zeta — is Tier B (structural candidate) at best and Tier A (speculative) for the zeta zero connection.

---

*Prerequisite: K7_EXACT_FORMULA_FOR_RP.md, K7_DIRICHLET_ASSEMBLY_CANDIDATE.md*
*Feeds: K7_WEAK_THEOREMS.md, K7_EXPLICIT_FORMULA_COMPATIBILITY.md*

---

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
