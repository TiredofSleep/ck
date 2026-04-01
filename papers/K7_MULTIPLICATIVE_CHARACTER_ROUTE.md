# K7 — Multiplicative and Kloosterman Character Route
*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Status

**Tier: mixed** — Sections 1–5 (additive route failure, Kloosterman definition, sequence deviation, equidistribution): Tier D (proved). Section 6 (A3 Dirichlet series): Tier B (structural candidate). Section 7 (RH bridge): Tier A (speculative, deeply open).

---

## Purpose

The additive character route (K7_ADDITIVE_CHARACTER_EXPANSION.md) reaches a wall: complete sums over the prime-field orbit reduce to -(1/(p-1)), independent of the generator g. This document follows the multiplicative route — asking what prime-specific, generator-dependent arithmetic information is genuinely present in the orbit, and where it lives.

The answer is in the Kloosterman sums. This document establishes that fact precisely, defines the correct sequence deviation, connects it to the Hecke-Maass spectral theory, and gives the honest status of the resulting Dirichlet series A3 as a bridge candidate.

---

## 1. Why Additive Routes Fail

### 1.1 The Complete Sum Obstruction

The prime-field orbit of a primitive root g mod p is the set:

```
Omega_p(g) = {g^0 mod p, g^1 mod p, ..., g^{p-2} mod p} = {1, 2, ..., p-1}
```

as a SET. The orbit equals all of F_p* for every primitive root g. Therefore, any function that depends only on the set (not the ordering) of orbit values is g-independent.

In particular, the additive character sum over the orbit (as a set) is a COMPLETE character sum:

```
sum_{j=0}^{p-2} psi_a(g^j) = sum_{k=1}^{p-1} psi_a(k) = sum_{k=1}^{p-1} e^{2*pi*i*a*k/p}
```

For a not divisible by p, this evaluates to -1 (complete sum over F_p* = complete sum over F_p minus the k=0 term = 0 - 1 = -1). For a = 0, it evaluates to p-1.

**Result:** For a ≠ 0 mod p:
```
sum_{j=0}^{p-2} e^{2*pi*i*a*g^j/p}  =  -1
```

This is independent of g. The additive character sum over the full orbit carries zero information about which generator was used.

### 1.2 Consequence for D_p^PSD

The PSD of the orbit is determined by the absolute value of the additive character sum:

```
S_p(xi) = (1/(p-1)^2) * |sum_{j=0}^{p-2} e^{-2*pi*i*xi*g^j/p}|^2
         = (1/(p-1)^2) * |sum_{k=1}^{p-1} e^{-2*pi*i*xi*k/p}|^2
```

This is a complete sum, g-independent, evaluable in closed form. The deviation D_p^PSD(xi) = p*(S_p(xi) - sinc^2(xi)) is therefore g-independent at every order in 1/p. The additive route produces no generator-sensitive arithmetic.

### 1.3 What Must Fail for g-Dependence to Appear

For a quantity to depend on g (not just on p), it must be sensitive to the ORDER in which the orbit elements appear — i.e., to the sequence g^0, g^1, g^2, ... rather than the set {g^0, g^1, ...}. The additive character sum sums over all elements of the set with equal weight, obliterating the ordering. Order-sensitivity requires either:

- A weight that varies with the position j in the sequence (not just with the value g^j mod p), or
- A product or nonlinear combination of orbit values at different positions.

The Kloosterman structure provides the second option.

---

## 2. The Nonlinear Pairing: How Kloosterman Sums Arise

### 2.1 Sequence Autocorrelation at Lag m

Consider the sequence x_j = g^j / p (mod 1) for j = 0, ..., p-2. The autocorrelation at lag m is:

```
C_p(m) = (1/(p-1)) * sum_{j=0}^{p-3} (x_j - 1/2)(x_{j+m} - 1/2)
```

(centered). After normalization, the relevant exponential sum at lag m and frequency (alpha, beta) is:

```
T_p(m; alpha, beta) = (1/(p-1)) * sum_{j=0}^{p-2} e^{2*pi*i*(alpha*g^j + beta*g^{j+m})/p}
                    = (1/(p-1)) * sum_{j=0}^{p-2} e^{2*pi*i*(alpha*g^j + beta*g^m*g^j)/p}
                    = (1/(p-1)) * sum_{j=0}^{p-2} e^{2*pi*i*(alpha + beta*g^m)*g^j/p}
```

For a single additive frequency alpha, this reduces again to a complete sum (g-independent). The cross-frequency term (alpha ≠ 0, beta ≠ 0) also reduces to a complete sum because alpha + beta*g^m is a single element of F_p.

### 2.2 The Nonlinear Pairing

Generator-dependent, bounded, prime-specific content requires pairing g^j with its multiplicative inverse g^{-j}. Define:

```
Kl_{g,m}(a, b; p) = sum_{j=0}^{p-2} e^{2*pi*i*(a*g^j + b*g^{-j})/p}
```

For a = b = 1 and m = 0 (no lag):

```
Kl_{g,0}(1, 1; p) = sum_{j=0}^{p-2} e^{2*pi*i*(g^j + g^{-j})/p}
```

Substituting k = g^j (which runs over all of F_p* as j ranges over 0,...,p-2):

```
Kl_{g,0}(1, 1; p) = sum_{k=1}^{p-1} e^{2*pi*i*(k + k^{-1})/p}  =  Kl(1, 1; p)
```

This is the standard Kloosterman sum. It does NOT depend on g (the substitution k = g^j is a bijection from {g^0,...,g^{p-2}} to {1,...,p-1} regardless of g). So Kl(1,1;p) itself is g-independent for a=b=1.

### 2.3 G-Dependent Kloosterman Sums via Lag

For nonzero lag m, the natural cross-term from the sequence is:

```
Kl_{g,m}(1, 1; p) = sum_{j=0}^{p-2} e^{2*pi*i*(g^j + g^{-(j+m)})/p}
                  = sum_{j=0}^{p-2} e^{2*pi*i*(g^j + g^{-m} * g^{-j})/p}
                  = Kl(1, g^{-m}; p)
```

Here g^{-m} mod p is a specific element of F_p* that depends on both m and g (since g is the generator, g^{-m} mod p for fixed m depends on which g is being used). The sum Kl(1, g^{-m}; p) is g-dependent for m ≠ 0 mod (p-1).

This is the key: the lag-m Kloosterman sum Kl(1, g^{-m}; p) is genuinely g-dependent. Different primitive roots g and g' give different values g^{-m} and g'^{-m} mod p (in general), hence different Kloosterman sum values.

---

## 3. The Correct Sequence Deviation D_p^{seq}

### 3.1 Definition

For each prime p, generator g, and lag m in {0, ..., p-2}, define the sequence Kloosterman deviation:

```
D_p^{Kl}(m) = Kl(1, g^{-m}; p) / (2*sqrt(p))
```

This is O(1) by the Weil bound. It is genuinely prime-specific (varies with p) and generator-specific (varies with g through the lag argument g^{-m}).

### 3.2 Properties of D_p^{Kl}

**Boundedness:** |D_p^{Kl}(m)| <= 1 for all p, g, m. (From Weil: |Kl(a,b;p)| <= 2*sqrt(p).)

**Generator-dependence:** For a fixed prime p and fixed lag m ≠ 0, distinct primitive roots g and g' give Kl(1, g^{-m}; p) and Kl(1, g'^{-m}; p). These are equal if and only if g^{-m} ≡ g'^{-m} (mod p), i.e., if (g/g')^m ≡ 1 (mod p). For generic m and g ≠ g', these values differ.

**Mean over the full sequence:** The average of D_p^{Kl}(m) over m = 0, ..., p-2 is:

```
(1/(p-1)) * sum_{m=0}^{p-2} Kl(1, g^{-m}; p) / (2*sqrt(p))
= (1/(2*sqrt(p)*(p-1))) * sum_{b in F_p*} Kl(1, b; p)
```

The inner sum sum_{b in F_p*} Kl(1,b;p) = sum_{b=1}^{p-1} sum_{k=1}^{p-1} e^{2*pi*i*(k+b*k^{-1})/p}. Exchanging the b and k sums and using that sum_{b=1}^{p-1} e^{2*pi*i*b*k^{-1}/p} = -1 for k^{-1} ≠ 0 (i.e., for all k in F_p*):

```
sum_{b=1}^{p-1} Kl(1,b;p) = sum_{k=1}^{p-1} e^{2*pi*i*k/p} * (-1) = (-1)*(-1) = 1
```

So the mean of D_p^{Kl}(m) over the full sequence is 1/(2*sqrt(p)*(p-1)) * 1 -> 0 as p -> infty. The sequence has mean zero in the large-p limit, consistent with genuine oscillatory behavior.

### 3.3 Contrast with D_p^PSD

The set-based deviation D_p^PSD(xi) is a function of a continuous frequency xi. The sequence-based deviation D_p^{Kl}(m) is a function of integer lag m. They measure different aspects of the orbit:

- D_p^PSD: how the spectral density of the orbit (as a uniform measure on [0,1]) deviates from sinc^2. This is g-independent.
- D_p^{Kl}: how the sequence autocorrelation structure (at lag m, using the nonlinear phase k + k^{-1}) deviates from zero. This is g-dependent.

These are complementary, not competing. D_p^PSD closes (proved prime-blind). D_p^{Kl} opens.

---

## 4. The Kloosterman Sequence and Its Statistics

The Kloosterman sequence at prime p and generator g is:

```
K_p(g) = { Kl(1, g^{-m}; p) / (2*sqrt(p)) : m = 0, 1, ..., p-2 }
```

This is a sequence of p-1 real numbers in [-1, 1], indexed by lag.

### 4.1 Individual Values

For m = 0: Kl(1, 1; p) / (2*sqrt(p)). This is the normalized standard Kloosterman sum at (1,1).

For m = 1: Kl(1, g^{-1}; p) / (2*sqrt(p)). This depends on g.

For m = p-2: Kl(1, g^{-(p-2)}; p) = Kl(1, g; p) / (2*sqrt(p)). This involves g as the second argument.

### 4.2 Equidistribution (Katz 1988)

Fix a, b ∈ F_p*. As p -> infty over primes, the sequence:

```
Kl(a, b; p) / (2*sqrt(p))
```

equidistributes on [-1, 1] with respect to the Sato-Tate measure dmu = (2/pi)*sqrt(1-t^2) dt. This is the semicircle law.

More precisely: for any continuous test function phi on [-1, 1]:

```
(1/pi(X)) * sum_{p <= X} phi(Kl(1,1;p)/(2*sqrt(p)))  ->  integral_{-1}^{1} phi(t) * (2/pi)*sqrt(1-t^2) dt
```

as X -> infty.

This equidistribution was proved by Katz (Gauss Sums, Kloosterman Sums, and Monodromy Groups, 1988) using the monodromy of the Kloosterman sheaf over F_p. The equidistribution is a consequence of the monodromy group being SU(2) (or Sp(2) in the general case).

### 4.3 What Equidistribution Means for D_p^{Kl}

Equidistribution implies that D_p^{Kl}(0) = Kl(1,1;p)/(2*sqrt(p)) has no preferred sign, no preferred scale within [-1,1], and no arithmetic bias (e.g., it is not systematically positive or negative for primes in a given congruence class). This is consistent with D_p^{Kl} being a genuinely arithmetically rich object — its values are not determined by any simple function of p.

The variance of D_p^{Kl}(0) over primes p is:

```
lim_{X->infty} (1/pi(X)) * sum_{p<=X} |Kl(1,1;p)|^2 / (4*p) = integral_{-1}^{1} t^2 * (2/pi)*sqrt(1-t^2) dt = 1/2
```

So the r.m.s. value of the normalized Kloosterman sum is 1/sqrt(2). This is the natural variance of the Sato-Tate distribution.

---

## 5. Connection to Hecke Operators and Automorphic Forms

### 5.1 The Kuznetsov Trace Formula

The Kuznetsov formula relates sums of Kloosterman sums to the spectral data of the hyperbolic Laplacian on the modular surface SL(2,Z)\H. The schematic form is:

```
sum_{c >= 1} (Kl(m, n; c) / c) * W(c/Y)
=  (spectral sum over Maass forms)
   + (continuous spectrum integral)
   + (holomorphic form contribution)
```

where W is a smooth weight function, Y is a cutoff, and the spectral sum on the right involves the Fourier coefficients a_f(m) and a_f(n) of Hecke-Maass forms f, weighted by the Gamma factors 1/||f||^2. The precise form of the kernel function involves Bessel functions J_{...} and K_{...}.

### 5.2 Hecke Eigenvalues

In the Kuznetsov formula, the dominant contribution from a single Maass form f comes from the product of its Fourier coefficients:

```
a_f(1) * a_f(p) / ||f||^2
```

where a_f(p) is the p-th Fourier coefficient of f (normalized as a Hecke eigenvalue: T(p)f = lambda_f(p)*f, and lambda_f(p) = a_f(p) for a normalized Hecke form). The Ramanujan conjecture predicts |lambda_f(p)| <= 2 for Maass forms (analogue of Deligne's theorem for holomorphic forms).

### 5.3 The Petersson Trace Formula

The Petersson formula (for holomorphic forms) gives a similar relation:

```
delta_{m,n} + 2*pi*i^k * sum_{c >= 1} Kl(m,n;c)/c * J_{k-1}(4*pi*sqrt(mn)/c)
= sum_{f of weight k} a_f(m) * bar(a_f(n)) / ||f||^2
```

where the sum on the right runs over a Hecke eigenbasis of cusp forms of weight k. For m = n = 1, this gives a formula for sum_c Kl(1,1;c)/c in terms of the squares of the first Fourier coefficients of cusp forms, weighted by their Petersson norms.

### 5.4 Implication for A3

The Dirichlet series A3(s) = sum_p Kl(1,1;p) * p^{-s} is a PRIME-RESTRICTED version of the fuller series sum_c Kl(1,1;c) * c^{-s} (where c runs over all positive integers, not just primes). The fuller series factors over primes (since Kl(1,1;n) is multiplicative in n) and can be expressed in terms of symmetric square L-functions L(s, Sym^2 pi) for appropriate GL(2) automorphic representations pi.

The connection: at the prime p, the local factor of the Kloosterman L-function involves alpha_p^2, alpha_p*beta_p, beta_p^2 (the symmetric square factors) where alpha_p + beta_p = Kl(1,1;p)/(sqrt(p)) (at the normalized level). So:

```
Z_{Kl}(s) ~ L(s - 1/2, Sym^2 pi)  (schematically, at the level of Euler factors)
```

where pi is the automorphic representation associated to the Kloosterman sheaf's monodromy. This is consistent with A3(s) being related to the L-function of a degree-3 object (the symmetric square of a degree-2 form) with functional equation relating s to 2 - s (or similar).

---

## 6. The Dirichlet Series A3(s)

### 6.1 Definition and Convergence

```
A3(s) = sum_p Kl(1, 1; p) * p^{-s}
```

**Absolute convergence:** For Re(s) > 3/2, |Kl(1,1;p) * p^{-s}| <= 2*p^{1/2-Re(s)}, and sum_p p^{1/2-sigma} converges for sigma > 3/2 by comparison with sum_p p^{-1-epsilon}. So A3 converges absolutely for Re(s) > 3/2.

**Conditional convergence:** Whether A3 converges conditionally in a wider half-plane depends on cancellation among the oscillating Kloosterman sums. Partial summation gives:

```
A3(s) = s * integral_2^infty [sum_{p<=X} Kl(1,1;p)] * X^{-(s+1)} dX
```

If sum_{p<=X} Kl(1,1;p) = O(X^{3/2-delta}) for some delta > 0 (i.e., better than trivial cancellation), then A3 would converge for Re(s) > 3/2 - delta. The equidistribution theorem implies RMS cancellation of order X^{3/2}/sqrt(log X) (random walk heuristic), which would give conditional convergence for Re(s) > 3/2 marginally. Strong cancellation bounds are open.

### 6.2 Likely Analytic Properties

Assuming the Euler product structure Z_{Kl}(s) (full series over all n, not just primes):

- Converges absolutely for Re(s) > 3/2.
- Has a functional equation relating s to 3 - s (for the symmetric square, centered at Re(s) = 3/2).
- Has a meromorphic continuation to all of C.
- Satisfies a Riemann hypothesis (all zeros on Re(s) = 3/2 after normalizing away the root number) — this is the Generalized Riemann Hypothesis for the symmetric square L-function L(s, Sym^2 pi).

The restriction A3(s) (primes only) inherits the analytic continuation but not the Euler product factorization. It can be written:

```
A3(s) = sum_p Kl(1,1;p) * p^{-s} = Z_{Kl}(s) / (product_p [local factor at composites])
```

which requires understanding the local factors at prime powers to extract A3 from Z_{Kl}.

### 6.3 Pole Structure

The full Kloosterman L-function Z_{Kl}(s) is expected to be entire (no poles) after removing a possible pole at s=1 (from the trivial representation contribution) and poles at s=2 (from the Sym^2 of trivial). For the non-trivial Kloosterman sums (a = b = 1, non-degenerate), the L-function is expected to be entire of order 1 with functional equation and zeros on the critical line Re(s) = 3/2 (in the un-normalized convention) or Re(s) = 1/2 (in the normalized convention after a shift by 3/2).

The zeros of Z_{Kl}(s) correspond to the eigenvalues 1/4 + t_j^2 of the hyperbolic Laplacian on SL(2,Z)\H (via the Kuznetsov formula spectral expansion). These are the spectral resonances of the modular surface.

---

## 7. What Would Be Needed for an RH Bridge

This is the genuinely hard open question. What is proved (Tier D/C) and what remains (Tier A):

### 7.1 What Is Proved

- (D) The Weil bound: |Kl(1,1;p)| <= 2*sqrt(p). A3 converges for Re(s) > 3/2.
- (D) Sato-Tate equidistribution for Kl: Katz 1988. The normalized sums are semicircle-distributed.
- (D) The Kuznetsov formula exists and connects sums of Kloosterman sums to Maass form eigenvalues.
- (D) D_p^{Kl} is genuinely g-dependent (different generators give different lag-m Kloosterman sums).
- (D) A3 does not factor as (constant) times (standard prime Dirichlet series) — proved by the non-multiplicative structure at the prime level (Kl(1,1;p) is not a Hecke eigenvalue in a trivial representation).

### 7.2 What Is Open (Tier B)

- (B) Analytic continuation of A3(s) (equivalently, of Z_{Kl}(s)) to Re(s) > 1/2 with controlled growth.
- (B) The precise identification of Z_{Kl}(s) as a named symmetric square L-function L(s, Sym^2 f) for some explicit Maass or Eisenstein form f.
- (B) The explicit formula for sum_{p<=X} Kl(1,1;p) in terms of the spectral zeros of Z_{Kl}.

### 7.3 What Is Speculative (Tier A)

- (A) The zeros of Z_{Kl}(s) lie on the same line (or same arithmetic object) as the zeros of zeta(s). No known result or heuristic predicts this. The zeros of Z_{Kl} are automorphic (indexed by eigenvalues of Delta on SL(2,Z)\H); the zeros of zeta are arithmetic (related to the distribution of primes via PNT). A correspondence between these two spectral families would require a Langlands-type functoriality from GL(2) (where Z_{Kl} lives) to GL(1) (where zeta lives). Such functoriality would go from a higher-rank group to a lower-rank group, which is unusual (Langlands functoriality typically goes the other direction or between equal ranks).

- (A) An explicit formula expressing sum_{rho of zeta} X^rho / rho in terms of the spectral data of A3 or Z_{Kl}. No such formula is known.

- (A) A bridge in which the orbit structure of F_p* (through the Kloosterman sequence D_p^{Kl}) contributes to an RH-type zero free region for zeta. This would require a new connection between orbit geometry in F_p* and the zero distribution of the Riemann zeta function.

### 7.4 Honest Summary

The Kloosterman route is the only surviving structural candidate from the K7 program. It is Tier B: genuinely prime-specific, genuinely bounded, genuinely connected to automorphic L-functions, and not reducible to known dead ends. But the distance from "connected to automorphic L-functions" to "connected to zeta zeros" is large — it crosses the most difficult open terrain in analytic number theory.

The A3 program is real mathematics. The claim that A3 bridges to zeta is speculative.

---

*Prerequisite: K7_DIRICHLET_ASSEMBLY_CANDIDATE.md, K7_ADDITIVE_CHARACTER_EXPANSION.md*
*Feeds: K7_EXPLICIT_FORMULA_COMPATIBILITY.md, K7_NO_GO_ATTEMPT.md*

---

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
