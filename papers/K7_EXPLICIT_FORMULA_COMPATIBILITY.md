# K7 — Explicit Formula Compatibility Audit

**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Status

**Tier: mixed** — A1 = D (proved incompatible), A2 = D (proved trivially reducible), A3 = B (compatible in principle, open).

---

## Purpose

An explicit formula in analytic number theory has the schematic form:

```
sum_{p <= X} F(p)  =  sum_rho c(rho) * X^rho / rho  +  lower-order terms
```

where the sum on the right runs over non-trivial zeros rho of the Riemann zeta function, and the left side is a "prime side" built from some arithmetic function F evaluated at primes.

The classic example is the Chebyshev explicit formula:

```
psi(X) = sum_{p^k <= X} log(p)  =  X - sum_rho X^rho/rho - log(2*pi) - (1/2)*log(1-X^{-2})
```

For the Luther-Sanders framework, the question is whether the assembly candidates A1, A2, A3 defined in K7_DIRICHLET_ASSEMBLY_CANDIDATE.md can serve as the "prime side" of such a formula — one that, when inverted, produces zero oscillations from the critical line.

This document audits each candidate against four explicit-formula compatibility requirements.

---

## Compatibility Requirements

For a prime-side sum S(X) = sum_{p <= X} F(p) to participate in a non-trivial explicit formula, it must satisfy all four of:

**Req 1 (Growth):** S(X) must grow like X^sigma for some sigma > 0, at a rate consistent with its Mellin transform having a natural domain of analyticity.

**Req 2 (Analytic continuation):** The Mellin transform M_F(s) = sum_p F(p) * p^{-s} must extend analytically (or meromorphically) to Re(s) > 1/2.

**Req 3 (Critical-line zeros):** When M_F(s) is inverted via Perron's formula, the zero contributions must land on Re(rho) = 1/2 (not exclusively on Re(s) = 0 or at trivial locations).

**Req 4 (Non-factoring):** F(p) must NOT factor as (constant in p) times a standard prime-counting function. If it does, M_F(s) = constant * (standard Dirichlet series), and the explicit formula just recovers the prime number theorem multiplied by a scalar — no new zeros.

---

## Candidate A1 — Logarithmic Weighted Sum

**Definition:**
```
A1(xi, X) = sum_{p <= X} D_p^PSD(xi) * log(p)
```

**Req 1 (Growth):** D_p^PSD(xi) = c_0(xi) + O(1/p) where c_0(xi) = -2[sinc(2*xi) - sinc^2(xi)] is a fixed real constant. Therefore:

```
A1(xi, X) = c_0(xi) * sum_{p<=X} log(p)  +  O(sum_{p<=X} log(p)/p)
           = c_0(xi) * theta(X)  +  O(log^2(X))
           ~ c_0(xi) * X    (by PNT)
```

PASS: A1 grows like X. Growth rate is consistent with a Dirichlet series convergent for Re(s) > 1.

**Req 2 (Analytic continuation):** The Mellin transform of A1 is:

```
M_{A1}(s) = sum_p D_p^PSD(xi) * log(p) * p^{-s}
           = c_0(xi) * sum_p log(p) * p^{-s}  +  c_1(xi) * sum_p log(p) * p^{-(s+1)}  +  ...
           = c_0(xi) * (-zeta'/zeta)(s) * [1 + finite Euler factors]  +  (analytic for Re(s)>0)
```

The function -zeta'/zeta(s) has a meromorphic continuation to all of C. So M_{A1} extends meromorphically to Re(s) > 0 with poles at s=1 (from -zeta'/zeta) and at the zeros of zeta (the poles of -zeta'/zeta at rho).

PASS: analytic continuation exists.

**Req 3 (Critical-line zeros):** The poles of M_{A1}(s) at the zeros of zeta are at Re(rho) = 1/2 (assuming RH) or at least on some line. This gives oscillatory terms sum_rho c_0(xi) * X^rho / rho in the explicit formula. So the zeros DO appear.

CONDITIONAL PASS: zeros appear, but see Req 4.

**Req 4 (Non-factoring):** A1 factors COMPLETELY. We have:

```
D_p^PSD(xi) * log(p) = c_0(xi) * log(p) + O(log(p)/p)
```

The leading term is c_0(xi) * log(p). The constant c_0(xi) does not depend on p at all — it is a deterministic function of xi involving only pi and trigonometric functions. The prime-side sum A1 is therefore:

```
A1(xi, X) = c_0(xi) * psi(X) + lower order
```

where psi(X) = sum_{p<=X} log(p) is the Chebyshev function. The explicit formula for A1 is:

```
A1(xi, X) = c_0(xi) * [X - sum_rho X^rho/rho - log(2*pi) - ...]  + lower order
```

This is just c_0(xi) times the standard Chebyshev explicit formula. It produces no new zeros. The "zeros" that appear are the standard zeta zeros, already known, multiplied by a fixed scalar. No new arithmetic information is present.

FAIL Req 4.

**Verdict:** INCOMPATIBLE. A1 factors as (constant in p) * (Chebyshev function). Its explicit formula recovers only the standard PNT oscillations, scaled by c_0(xi). No new structure.

**Tier: D** (proved incompatible).

---

## Candidate A2 — Dirichlet Series in s

**Definition:**
```
A2(xi, s) = sum_p D_p^PSD(xi) * log(p) * p^{-s}
```

**Req 1 (Growth):** A2 is defined as a Dirichlet series, not a sum up to X. The analogue of growth for a Dirichlet series is the abscissa of absolute convergence. Since D_p^PSD(xi) = O(1), we have |D_p * log(p) * p^{-s}| = O(log(p) * p^{-Re(s)}), and sum_p log(p) * p^{-sigma} converges for sigma > 1. So A2(xi, s) converges absolutely for Re(s) > 1. Growth condition is satisfied in the sense that the partial sums of A2 in X grow like A1(xi,X), i.e., like c_0(xi) * X.

PASS.

**Req 2 (Analytic continuation):** From K7_DIRICHLET_ASSEMBLY_CANDIDATE.md:

```
A2(xi, s) = c_0(xi) * (-zeta'/zeta)(s)  +  c_1(xi) * (-zeta'/zeta)(s+1)  +  ...
```

Each term in this expansion has a meromorphic continuation (since -zeta'/zeta(s+n) is meromorphic for all integer shifts n). So A2(xi, s) extends meromorphically to Re(s) > 0.

PASS.

**Req 3 (Critical-line zeros):** The leading term c_0(xi) * (-zeta'/zeta)(s) has simple poles at the zeros rho of zeta (since -zeta'/zeta has simple poles at zeros of zeta with residue equal to the multiplicity). Via Perron's formula, inverting this Dirichlet series gives a sum over these poles. The zero contributions appear on the critical line (assuming RH).

CONDITIONAL PASS.

**Req 4 (Non-factoring):** The factoring failure is complete. Writing the full expansion:

```
A2(xi, s) = sum_{n=0}^{infty} c_n(xi) * (-zeta'/zeta)(s+n)
```

where c_n(xi) are all deterministic functions of xi only (from the 1/p^n expansion of D_p^PSD). Each coefficient c_n(xi) is a fixed number that does not depend on p. The series in s consists entirely of scalar multiples of shifts of -zeta'/zeta.

The xi-dependence and the s-dependence DECOUPLE. There is no term in A2(xi, s) that couples a xi-specific quantity to a prime-specific quantity in a non-trivial way. Any "coupling" is of the form c_n(xi) * f(s) where both factors are separately determined.

The explicit formula recovered from A2 via Perron's formula would be:

```
sum_{p<=X} D_p^PSD(xi) * log(p) = sum_{n=0}^{infty} c_n(xi) * [sum_rho X^rho/rho evaluated at s+n]  + ...
```

This is c_0(xi) * (standard PNT formula) + corrections that are smaller by powers of X^{-1}. The corrections are not new zeros — they are the same zeta zeros appearing at different X-scales, each multiplied by deterministic constants.

FAIL Req 4.

**Verdict:** TRIVIALLY REDUCIBLE. A2(xi, s) = c_0(xi) * (-zeta'/zeta)(s) + lower terms. The xi-dependence factors out as a constant multiplier. This is not a new Dirichlet series — it is a scalar-weighted combination of shifts of the logarithmic derivative of zeta. No new L-function. No new zeros.

**Tier: D** (proved trivially reducible to zeta).

Note: The prior tier assignment for A2 in K7_DIRICHLET_ASSEMBLY_CANDIDATE.md was C (weak). Upon explicit-formula audit, the reduction is complete enough to warrant D: there is no residual that escapes the factoring argument.

---

## Candidate A3 — Kloosterman-Weighted Dirichlet Series

**Definition:**
```
A3(s) = sum_p Kl(1, 1; p) * p^{-s}

where Kl(1, 1; p) = sum_{k=1}^{p-1} exp(2*pi*i * (k + k^{-1}) / p)
```

**Req 1 (Growth):** By the Weil bound, |Kl(1,1;p)| <= 2*sqrt(p), so:

```
|Kl(1,1;p) * p^{-s}| = O(p^{1/2 - Re(s)})
```

A3(s) converges absolutely for Re(s) > 3/2. The partial sums sum_{p<=X} Kl(1,1;p) grow at most like sum_{p<=X} 2*sqrt(p) ~ (4/3)*X^{3/2}/log(X) (by partial summation and PNT). This is consistent with an abscissa of absolute convergence sigma_a = 3/2. Whether cancellation among the (oscillating, complex-valued) Kloosterman sums can push the abscissa of conditional convergence below 3/2 is open.

PASS (growth is O(X^{3/2}), consistent with s-domain analysis).

**Req 2 (Analytic continuation):** The Kloosterman sums Kl(1,1;n) for all positive integers n (not just primes) form a multiplicative arithmetic function via the Chinese Remainder Theorem: Kl(1,1;mn) = Kl(1,1;m)*Kl(1,1;n) when gcd(m,n) = 1. This means the full Dirichlet series sum_{n=1}^{infty} Kl(1,1;n) * n^{-s} has an Euler product:

```
Z_{Kl}(s) = prod_p (1 - alpha_p * p^{-s})^{-1} * (1 - beta_p * p^{-s})^{-1}
```

where alpha_p, beta_p are the roots of the local factor, satisfying |alpha_p| = |beta_p| = sqrt(p) by the Weil bound (equivalently, alpha_p * beta_p = p and alpha_p + beta_p = Kl(1,1;p)). By standard theory of degree-2 L-functions with Euler product and functional equation (if the functional equation is established), Z_{Kl}(s) extends meromorphically to all of C. A3(s) is the restriction of Z_{Kl}(s) to primes, which inherits the analytic continuation from the full series.

The precise identification of Z_{Kl}(s) in terms of automorphic L-functions is via the Kuznetsov/Petersson trace formula. Schematically, sums over Kloosterman sums are related to Hecke eigenvalues of Maass forms on GL(2). The analytic continuation of the associated L-functions to Re(s) > 1/2 is conditional on the Ramanujan conjecture for GL(2) Maass forms (which predicts |alpha_p| = |beta_p| = 1 at the normalized level, i.e., Kl(1,1;p)/(2*sqrt(p)) has alpha_p normalized to the unit circle).

CONDITIONAL PASS: analytic continuation likely extends to Re(s) > 1 unconditionally and to Re(s) > 1/2 under Ramanujan. Whether poles occur for Re(s) in (1/2, 3/2) is open.

**Req 3 (Critical-line zeros):** A3(s) is NOT -zeta'/zeta(s) and does not have poles at the zeros of zeta in any direct sense. The zeros of A3(s) — or rather the poles of 1/A3(s) — are governed by the spectral theory of Maass forms on the modular surface. The Kloosterman explicit formula would produce oscillatory terms indexed by the eigenvalues {lambda_j = 1/4 + t_j^2} of the hyperbolic Laplacian on SL(2,Z)\H, not by the zeros of zeta.

This is the key finding: A3 is compatible with an explicit formula structure in principle, but the zeros on the critical line that it produces are AUTOMORPHIC zeros (eigenvalues of Maass forms) rather than Riemann zeta zeros. Whether these automorphic zeros are related to the zeta zeros is a deep open question — it would require a direct correspondence between the spectral theory of the modular surface and the arithmetic zeros of zeta.

CONDITIONAL PASS (Req 3 is satisfied for automorphic zeros, which lie on Re(rho) = 1/2 by the spectral decomposition of L^2(SL(2,Z)\H); connection to zeta zeros is open).

**Req 4 (Non-factoring):** The Kloosterman sum Kl(1,1;p) is a genuinely prime-dependent quantity. For distinct primes p and q:

```
Kl(1,1;p) / (2*sqrt(p))  and  Kl(1,1;q) / (2*sqrt(q))
```

are independent (in the equidistribution sense of Katz 1988). A3(s) does not factor as (constant) * (any standard Dirichlet series). Its Euler product is a new degree-2 L-function that is not a product of Dirichlet L-functions.

PASS.

**Verdict:** COMPATIBLE IN PRINCIPLE, OPEN. A3 satisfies Req 1, Req 4 cleanly, and Req 2, Req 3 conditionally. The explicit formula it would produce involves automorphic zeros, not directly zeta zeros. The bridge between these two spectral families is the central open question.

**Tier: B** (compatible in principle, open question in analytic number theory).

---

## Compatibility Table

| Candidate | Grows like X^sigma | Analytic continuation to Re(s)>1/2 | Zeros on critical line | Does NOT factor from zeta | Known L-function connection | Tier |
|---|---|---|---|---|---|---|
| A1 | Yes (sigma=1) | Yes (inherits from zeta) | Yes (standard zeta zeros) | NO — factors as c_0(xi)*psi(X) | Trivial (=PNT) | D |
| A2 | Yes (sigma=1) | Yes (inherits from -zeta'/zeta) | Yes (standard zeta zeros) | NO — xi factors out completely | Degenerate (=scalar * log-deriv zeta) | D |
| A3 | Yes (sigma=3/2) | Conditional (Ramanujan for GL(2)) | Yes (automorphic zeros) | YES — Kl(1,1;p) is genuinely prime-dependent | Yes (Weil bound, Kuznetsov, degree-2 L-fn) | B |

**Column glossary:**
- "Does NOT factor from zeta" = PASS means the candidate contributes non-trivial new structure.
- "L-function connection" = Trivial means recovers only known results; Yes means new arithmetic content.

---

## Summary of Why A1 and A2 Are Killed

The core problem for both A1 and A2 is the Taylor expansion of D_p^PSD(xi) in 1/p:

```
D_p^PSD(xi) = c_0(xi) + c_1(xi)/p + c_2(xi)/p^2 + ...
```

where EVERY coefficient c_n(xi) is a deterministic function of xi alone. No coefficient carries prime-specific arithmetic — they are all defined by the Taylor coefficients of sin and the fixed parameter xi. Therefore any assembly sum_{p<=X} D_p^PSD(xi) * w(p) decomposes as:

```
= c_0(xi) * sum_{p<=X} w(p) + c_1(xi) * sum_{p<=X} w(p)/p + ...
```

Each term is (deterministic in xi) * (standard prime sum in p). The xi and p variables do not interact. The resulting explicit formula can only reflect what is already in the standard prime sums — it cannot produce genuinely new zeros.

This is not a deficiency of the assembly strategy. It is a consequence of the fact that D_p^PSD measures the orbit through its SET statistics (the full orbit equals {1,...,p-1} for any generator g), and set statistics carry no prime-specific arithmetic beyond the value of p itself.

---

## What A3 Would Need to Close

For A3 to become a genuine RH bridge (Tier A), three things must be established:

1. **Analytic continuation of A3(s) to Re(s) > 1/2** — This requires either Ramanujan for GL(2) Maass forms (known for holomorphic forms by Deligne, open for Maass forms) or an alternative approach.

2. **Explicit formula for A3** — A Perron-type inversion giving sum_{p<=X} Kl(1,1;p) in terms of the poles/zeros of Z_{Kl}(s). This is expected to hold in the standard framework once continuation is established.

3. **Bridge from automorphic zeros to zeta zeros** — The poles of 1/Z_{Kl}(s) occur at eigenvalues of the Laplacian on SL(2,Z)\H. These are not the zeros of zeta. Connecting them would require a Langlands-type correspondence between the GL(2) automorphic spectrum and the GL(1) zeta function. No such direct correspondence is known.

Steps 1 and 2 are within reach of existing technology. Step 3 is the genuinely hard open problem.

---

*Prerequisite: K7_DIRICHLET_ASSEMBLY_CANDIDATE.md, K7_ADDITIVE_CHARACTER_EXPANSION.md*
*Feeds: K7_MULTIPLICATIVE_CHARACTER_ROUTE.md, K7_NO_GO_ATTEMPT.md*

---

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
