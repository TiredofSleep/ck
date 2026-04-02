# K7 — Dirichlet Assembly Candidate

**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Status

**Tier: mixed** — A1 = D (proved dead end), A2 = C (weak, log singularity only), A3 = B (structural candidate, open).

---

## Purpose

Given the prime-field deviation

```
D_p^PSD(xi) = p * (S_p(xi) - sinc^2(xi))
```

which converges to the deterministic limit c_0(xi) = -2[sinc(2*xi) - sinc^2(xi)], we ask: can a sum over primes assemble these per-prime deviations into an object with explicit-formula shape — that is, an object whose analytic structure reflects the non-trivial zeros of the Riemann zeta function?

This document defines three assembly candidates, analyzes each, and ranks them by structural viability.

---

## Setup

Throughout, xi is a fixed real parameter in (0, 1), s is a complex variable, X is a real cutoff, and g denotes a primitive root mod p (fixed for each p). The notation D_p = D_p^PSD(xi) abbreviates the g-independent PSD deviation.

The target form for an "explicit-formula-shaped" object is an expression of the form:

```
sum_rho f(rho) * X^rho  (for a sum over zeros rho of zeta)
```

or equivalently a Dirichlet series with a meromorphic continuation to Re(s) < 1 whose poles are at the zeros of zeta.

---

## Candidate A1 — Logarithmic Weighted Sum

### Definition

```
A1(xi, X) = sum_{p <= X} D_p^PSD(xi) * log(p)
```

### Analysis

Since D_p^PSD(xi) -> c_0(xi) = -2[sinc(2*xi) - sinc^2(xi)] as p -> infinity, we have for large p:

```
D_p^PSD(xi) * log(p) = c_0(xi) * log(p) + O(log(p) / p)
```

Summing over p <= X:

```
A1(xi, X) = c_0(xi) * sum_{p<=X} log(p)  +  sum_{p<=X} O(log(p)/p)
```

The prime number theorem gives:

```
theta(X) = sum_{p<=X} log(p) ~ X
```

The error sum converges absolutely (since sum log(p)/p^s converges for Re(s) > 1, and at s=1 the sum over log(p)/p diverges only logarithmically; the O(1/p) correction gives sum log(p)/p which diverges, contributing a sub-leading term of size O(log^2(X)) relative to X). Therefore:

```
A1(xi, X) ~ c_0(xi) * X    as X -> infinity
```

### Assessment

A1 grows linearly in X, multiplied by a fixed constant c_0(xi) that depends only on the deterministic limit, not on any prime-by-prime structure. This is NOT explicit-formula-shaped. The explicit formula for a sum over zeros would produce oscillations of size ~X^{1/2} (assuming RH) or X^{beta} where beta is the real part of a zero, not monotone growth of size X. A1 has no pole structure, no oscillatory terms, and carries no information about zeros of zeta.

**Verdict: DEAD END.**

**Tier: D** (proved).

---

## Candidate A2 — Dirichlet Series in s

### Definition

```
A2(xi, s) = sum_p D_p^PSD(xi) * log(p) * p^{-s}
```

### Analysis

**Convergence:** Since D_p^PSD(xi) = O(1) uniformly in xi (it converges to a bounded limit), we have:

```
|D_p^PSD(xi) * log(p) * p^{-s}| = O(log(p) * p^{-Re(s)})
```

The series sum_p log(p) * p^{-sigma} converges absolutely for sigma = Re(s) > 1, so A2 converges absolutely for Re(s) > 1.

**Behavior near s = 1:** Substituting D_p ~ c_0(xi) + c_1(xi)/p:

```
A2(xi, s) = c_0(xi) * sum_p log(p) * p^{-s}  +  c_1(xi) * sum_p log(p) * p^{-(s+1)}  +  ...
```

The leading sum is -zeta'(s)/zeta(s) up to a finite Euler-product correction. Near s = 1, zeta(s) has a simple pole with residue 1, so -zeta'/zeta has a simple pole at s=1 with residue 1. Therefore:

```
sum_p log(p) * p^{-s}  ~  1/(s-1)    as s -> 1
```

(This follows from -d/ds log zeta(s) = sum_p log(p)*p^{-s} + corrections from prime powers, and log zeta(s) ~ log(1/(s-1)) near s=1.)

Therefore:

```
A2(xi, s) ~ c_0(xi) * 1/(s-1)   as s -> 1 from Re(s) > 1
```

Wait — this would suggest A2 has a simple pole at s=1 with residue c_0(xi). However, the pole structure of -zeta'/zeta at the zeros of zeta is also relevant: -zeta'/zeta has simple poles at the non-trivial zeros rho with residue 1 (multiplicity 1) and at s=0 and the trivial zeros. So A2 inherits these poles from -zeta'/zeta.

**The difficulty:** A2 is essentially c_0(xi) * (-zeta'/zeta)(s) plus a corrective series from the 1/p terms. The term c_0(xi) * (-zeta'/zeta)(s) has the explicit-formula poles at zeros of zeta — but c_0(xi) is a fixed constant, not a function of the zeros. The resulting explicit formula for A2 would be:

```
A2(xi, s) = c_0(xi) * [1/(s-1) + sum_rho 1/(s-rho) + ... ]  +  error
```

This is not an interesting new object. It is just a scalar multiple of the logarithmic derivative of zeta. The xi dependence factors out completely as a constant c_0(xi). There is no coupling between the spectral information (zeros of zeta) and the spatial information (xi). Equivalently, if one took the inverse Mellin transform to get an explicit formula in X, the result would be:

```
inverse Mellin [A2(xi, s)] ~ c_0(xi) * [X + sum_rho X^rho / rho + ...]
```

which is c_0(xi) times the standard prime counting explicit formula. This is not new mathematics.

**Note on log singularity at s=1:** More precisely, the pole is simple (not logarithmic). The word "log singularity" in the status refers to the behavior of the *generating function* of A1 (the zeta logarithm), not a logarithmic branch point. The key point is that A2 reduces to a known object (scalar * log-derivative of zeta) and provides no structural advance.

**Verdict: WEAK.** A2 converges and has the right singularity structure, but the xi dependence factors out as a constant, making A2 a trivial scalar multiple of an already-known Dirichlet series. No new L-function.

**Tier: C** (weak; log-singularity-level, no structural advance).

---

## Candidate A3 — Kloosterman-Weighted Dirichlet Series

### Definition

The Kloosterman sum at prime p is:

```
Kl(a, b; p) = sum_{k=1}^{p-1} exp(2*pi*i * (a*k + b*k^{-1}) / p)
```

where k^{-1} is the multiplicative inverse of k mod p. For a = b = 1:

```
Kl(1, 1; p) = sum_{k=1}^{p-1} exp(2*pi*i * (k + k^{-1}) / p)
```

The Kloosterman Dirichlet series is:

```
A3(s) = sum_p Kl(1, 1; p) * p^{-s}
```

(The xi dependence has dropped: A3 is a pure number-theoretic object, not a spectral object in xi. This is a feature, not a defect — it means A3 is asking a different question.)

### Structural Analysis

**Generator dependence:** The Kloosterman sum Kl(1, g; p) with g replaced by a primitive root involves the specific generator g only through the residue class of g mod p. For Kl(1, 1; p), the argument b=1 does not refer to a primitive root — it is the constant 1. This sum is well-defined and g-independent in the sense that it does not require knowing g. However, its analytic properties are distinct from D_p^PSD.

**Weil bound:** |Kl(1,1;p)| <= 2*sqrt(p), so Kl(1,1;p)*p^{-s} = O(p^{1/2 - Re(s)}). The series A3(s) converges absolutely for Re(s) > 3/2.

**L-function connection:** Kloosterman sums are related to coefficients of automorphic forms. Specifically, by the Petersson trace formula and Kuznetsov formula, sums of Kloosterman sums over primes are connected to spectral data of GL(2) automorphic forms. The series sum_p Kl(1,1;p) * p^{-s} is not a standard L-function, but it can be expressed in terms of the symmetric square L-function L(s, Sym^2 f) and related objects via the theory of Kloosterman sums and their connection to Bessel functions and Kuznetsov's formula.

More precisely: the Kloosterman sum Kl(m, n; p) for prime p equals sum_{chi mod p} chi(m)*chi_bar(n)*tau(chi)^2 / phi(p) where tau(chi) is the Gauss sum — an expression that decomposes the Kloosterman sum into a sum over Dirichlet characters. This multiplicative character decomposition connects A3 to Dirichlet L-functions and their products.

**Ramanujan sum connection:** The Ramanujan sum c_q(n) = sum_{k: gcd(k,q)=1} exp(2*pi*i*k*n/q) is a special case of generalized Kloosterman sums. For prime p, c_p(1) = -1 = Kl(1,0;p) - 1, while Kl(1,1;p) is a full two-variable Kloosterman sum. These are structurally distinct: Ramanujan sums are multiplicative and appear in the Fourier expansion of arithmetic functions; Kloosterman sums with two nontrivial arguments are non-multiplicative but satisfy the deep Weil bound and equidistribution.

**Why A3 is the promising candidate:** The PSD route (A1, A2) produces objects that depend on xi only through the deterministic constant c_0(xi), and depend on primes only through the standard zeta logarithm. The Kloosterman route separates the xi-spectral information from the character-sum information, placing the latter in a space where genuine L-function theory applies. The assembly A3(s) has a wider abscissa of convergence (3/2 vs 1) but potentially richer pole structure once expressed in terms of automorphic L-functions. The question of whether A3(s) has a meromorphic continuation to Re(s) < 3/2 with poles related to zeta zeros is open and structurally nontrivial.

**Verdict: OPEN.** A3 is the structural candidate. It lives in character-sum space, satisfies the Weil bound, connects to automorphic L-functions via the Kuznetsov formula, and is not reducible to a scalar multiple of any known object.

**Tier: B** (structural candidate, open question).

---

## Candidate Ranking Table

| Candidate | Assembly | Growth type | Explicit-formula shape? | L-function connection? | Tier |
|---|---|---|---|---|---|
| A1 | sum_{p<=X} D_p * log(p) | Linear in X | No (monotone growth ~ X) | No (PNT only) | D |
| A2 | sum_p D_p * log(p) * p^{-s} | Meromorphic, Re(s)>1 | Trivial (scalar * log-deriv zeta) | Degenerate (xi factors out) | C |
| A3 | sum_p Kl(1,1;p) * p^{-s} | Convergent Re(s)>3/2 | Open (pole structure unknown) | Yes (Weil, Kuznetsov, Sym^2) | B |

---

## What Is Proved vs. What Is Conjectural

**Proved (Tier D):**
- A1 grows as c_0(xi) * X + lower order. This is exact given D_p -> c_0(xi) and the PNT. A1 is a dead end.

**Proved (Tier C):**
- A2 converges for Re(s) > 1 and its leading behavior near s=1 is c_0(xi) * [1/(s-1) + sum_rho ...]. The xi factoring is exact. A2 carries no new information.

**Weil bound (classical result, not ours):**
- |Kl(1,1;p)| <= 2*sqrt(p). A3 converges for Re(s) > 3/2.

**Sato-Tate equidistribution for Kloosterman sums (Katz, classical):**
- Kl(1,1;p)/(2*sqrt(p)) equidistributes with respect to (2/pi)*sqrt(1-t^2) dt on [-1,1].

**Conjectural / Open (Tier B):**
- Whether A3(s) has meromorphic continuation beyond Re(s) = 3/2.
- Whether the poles of A3(s) are related to zeros of zeta or to eigenvalues of automorphic forms.
- Whether A3 can be expressed as a linear combination of standard automorphic L-functions.
- Whether the Kuznetsov formula gives a usable spectral expansion of A3(s) in terms of Maass form Fourier coefficients.

---

## Next Steps for A3

1. Compute A3(s) numerically for real s in (3/2, 3) using k7_character_probe.py output. Look for evidence of the abscissa of convergence exceeding 3/2 (suggesting cancellation beyond the Weil bound) or equal to 3/2.

2. Write out the Kuznetsov formula expansion of sum_{p<=X} Kl(1,1;p) and identify the dominant automorphic spectrum contribution.

3. Investigate whether the generating Dirichlet series for Kl(1,1;p) over all integers (not just primes) is known. The full sum sum_{n=1}^{infty} Kl(1,1;n) * n^{-s} has an Euler product if Kl is multiplicative, but Kl(1,1;n) for composite n is defined via the Chinese Remainder Theorem and is multiplicative in n, making the Euler product structure accessible.

4. If the Euler product factors as product_p (1 - alpha_p * p^{-s})^{-1} * (1 - beta_p * p^{-s})^{-1} with |alpha_p| = |beta_p| = 1, then A3 is a degree-2 L-function and standard analytic continuation applies.

---

## Relationship Between A3 and D_p^PSD

A3 discards D_p^PSD entirely and works directly with Kloosterman sums. The connection to the prime-field orbit is through the structure:

- D_p^PSD measures the PSD deviation of the orbit {g^m mod p} / p — a real, spectral, g-independent quantity.
- Kl(1,1;p) measures a character sum over the full residue orbit {k mod p} — a complex, algebraic, character-weighted quantity.

These are two genuinely different projections of the same underlying combinatorial object (the orbit of multiplication by g in Z/pZ). The PSD route sees the orbit through its spectral density. The Kloosterman route sees the orbit through its exponential sums. They are not redundant; they are complementary. The PSD route closes (A1, A2 both dead ends or trivial). The Kloosterman route opens.

---

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
