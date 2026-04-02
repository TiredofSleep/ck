# K8_SATO_TATE_DISTRIBUTION.md

## Equidistribution of Kloosterman Angles: The Sato-Tate Law

**Program position:** This document establishes the statistical behavior of the normalized
Kloosterman sums α_p = Kl(1,1;p)/(2√p). The Sato-Tate law is a proved D-tier theorem (Katz 1988).
This document gives the statement, proof sketch, numerical predictions, and what the law implies
for the A3 Dirichlet series.

---

## 1. The Kloosterman Angle

### Definition

For each prime p ≥ 2, define:

```
α_p = Kl(1, 1; p) / (2√p) ∈ [−1, 1]   (by Weil bound)
θ_p ∈ [0, π] such that α_p = cos(θ_p)
```

The angle θ_p is the **Kloosterman angle** of the prime p.

### Arithmetic interpretation

The Weil bound |Kl(1,1;p)| ≤ 2√p comes from writing Kl(1,1;p) as the trace of Frobenius
on the cohomology of a certain algebraic variety over F_p. Specifically:

Consider the affine curve C: u + v = 0 in F_p^* × F_p^*, with uv = 1 (so v = u^{-1}).
Then Kl(1,1;p) = Σ_{u ∈ F_p^*} ψ(u + u^{-1}) where ψ(x) = e^{2πix/p}.

This is the trace of Frobenius on H^1_c of a sheaf on P^1_{F_p}. The Weil bound follows
from the fact that this H^1 is 2-dimensional (genus 1 curve analog), giving at most 2 roots
of absolute value √p.

Write the two Frobenius eigenvalues as √p · e^{±iθ_p}. Then:

```
Kl(1,1;p) = √p · (e^{iθ_p} + e^{-iθ_p}) = 2√p · cos(θ_p)
```

The angle θ_p ∈ [0,π] is the **canonical parameter** encoding the prime p's Kloosterman value.

---

## 2. The Sato-Tate Theorem for Kloosterman Sums

### Theorem (Katz 1988, D-tier)

The sequence {θ_p : p prime} is equidistributed on [0, π] with respect to the measure:

```
dμ_ST = (2/π) sin²(θ) dθ
```

That is, for any continuous function f: [0,π] → ℝ:

```
(1/π(X)) Σ_{p ≤ X} f(θ_p)  →  ∫_0^π f(θ) (2/π) sin²(θ) dθ    as X → ∞
```

### Proof sketch

The monodromy group G_Kl of the Kloosterman sheaf Kl_2 on P^1_{F_p} (as a family over Spec(Z))
is G = SU(2) (Katz, "Gauss Sums, Kloosterman Sums, and Monodromy Groups," 1988).

The Frobenius at each prime p gives a conjugacy class in SU(2), parametrized by the eigenvalue
angle θ_p. Equidistribution of conjugacy classes in a compact Lie group (here SU(2)) follows
from the Weyl equidistribution theorem: the characters of irreducible representations of SU(2)
are orthogonal, and L-function theory forces each L(s, Sym^k Kl_2) to be entire and nonvanishing
on Re(s) = 1. This is the Chebotarev-type density theorem for the Kloosterman family.

The Haar measure on conjugacy classes of SU(2) is precisely the semicircle measure (2/π)sin²(θ)dθ.

### Key point: this is NOT the elliptic curve Sato-Tate

The classical Sato-Tate conjecture (now theorem, Taylor et al. 2008) is for elliptic curves
over Q: the angles of a_p(E)/2√p are equidistributed by the same semicircle measure.
The Kloosterman Sato-Tate is a different but structurally parallel result, proved earlier (1988)
because the Kloosterman sheaf family has explicit monodromy group structure.

---

## 3. Moments of the Distribution

The semicircle measure (2/π)sin²(θ)dθ on [0,π], equivalently ρ(t) = (2/π)√(1−t²) on [−1,1]:

| Moment | Formula | Value |
|--------|---------|-------|
| Mean E[α_p] | ∫_{-1}^1 t · (2/π)√(1−t²) dt | 0 (odd function) |
| Second moment E[α_p²] | ∫_{-1}^1 t² · (2/π)√(1−t²) dt | 1/2 |
| Fourth moment E[α_p⁴] | | 3/8 |
| E[cos(kθ)] (Chebyshev) | (2/π) ∫_0^π cos(kθ) sin²(θ) dθ | δ_{k,0}/2 − δ_{k,2}/2? |

Actually, the Chebyshev polynomials of the second kind U_k(cos θ) = sin((k+1)θ)/sin(θ) form
an orthogonal basis for the semicircle measure. The orthogonality gives:

```
(2/π) ∫_0^π U_j(cos θ) U_k(cos θ) sin²(θ) dθ = δ_{jk}
```

The moments of cos(θ) under the semicircle are:

```
E[cos^n(θ)] = (1/2^n) C(n, n/2)    for n even, 0 for n odd
```

**Numerical predictions for k8_sato_tate_test.py:**
- Sample mean of α_p should be near 0 (converges to 0)
- Sample variance should be near 1/2 (converges to 1/2)
- Kolmogorov-Smirnov test against semicircle CDF F(t) = (1/2) + t√(1−t²)/π + arcsin(t)/π
  should not reject at p=0.05 for N ≥ 1000 primes

---

## 4. Implications for A3(s)

### 4.1 Mean behavior of A3

Since E[Kl(1,1;p)] = 0 by Sato-Tate, the partial sums Σ_{p≤X} Kl(1,1;p) exhibit
cancellation. The growth rate is governed by the central limit theorem analog:

By Sato-Tate variance (E[|Kl(1,1;p)|²/p] = E[4α_p²] = 2), the partial sums

```
Σ_{p ≤ X} Kl(1,1;p) = O(√(Σ_{p≤X} p))   "on average"
```

More precisely, by the law of iterated logarithm analog (conjectural for primes),

```
Σ_{p ≤ X} Kl(1,1;p) / √(X/log X) → N(0, 2)   [conjectural, C-tier]
```

### 4.2 The A3(s) partial sums

For real s > 3/2:

```
A3_X(s) = Σ_{p ≤ X} Kl(1,1;p) · p^{-s}
```

Since Kl(1,1;p) = O(√p), each term is O(p^{1/2−s}). For s > 3/2, terms decay as p^{−1},
summing to O(log X). But WITH cancellation from Sato-Tate (mean zero), the partial sums
should exhibit convergence much faster than the absolute bound suggests.

**Expected behavior (C-tier, from Sato-Tate + square-root cancellation hypothesis):**
```
A3_X(s) = A3(∞, s) + O(X^{1/2−s+ε})   for s > 1
```

This would give convergence for s > 1, conditional on square-root cancellation
(analogous to the Lindelöf hypothesis for GL(2) L-functions).

**Unconditional:** A3(σ+it) is absolutely convergent for σ > 3/2.

### 4.3 What Sato-Tate does NOT give

Sato-Tate is an equidistribution result — it says the DISTRIBUTION of α_p is semicircular.
It does NOT say:
- Whether A3(s) has zeros on a specific vertical line
- Whether A3(s) has analytic continuation beyond Re(s)=3/2 (unconditionally)
- How A3(s) behaves near s = 3/2 (the boundary of absolute convergence)
- Any relation between A3's analytic properties and ζ(s)'s analytic properties

---

## 5. Numerical Test Protocol

Implemented in k8_sato_tate_test.py. Pre-registered predictions:

**P1 (D-tier prediction from Katz 1988):** KS-test of α_p distribution against semicircle
will NOT reject at significance level 0.05 for 500+ primes.

**P2 (D-tier from Corollary K8.C1):** Sample mean of α_p over primes p ≤ 10,000
satisfies |mean| < 0.05.

**P3 (D-tier from Corollary K8.C1):** Sample variance of α_p over primes p ≤ 10,000
satisfies |var − 0.5| < 0.05.

**P4 (C-tier prediction, verifiable numerically):** Partial sums Σ_{p≤X} α_p / √(π(X))
show O(1) fluctuation — consistent with O(1) standard deviation growth.

**Surprise conditions:**
- S1: |mean(α_p)| > 0.1 → arithmetic bias in Kloosterman sums, contradicts Sato-Tate
- S2: var(α_p) far from 0.5 (e.g., < 0.3 or > 0.7) → monodromy group is not SU(2)
- S3: KS-test rejects against semicircle at p < 0.001 → major anomaly, re-check computation
- S4: Partial sums grow as O(X^c) for c > 0 → no Sato-Tate cancellation

---

## 6. Summary Table

| Property | Value | Tier | Source |
|----------|-------|------|--------|
| Range of α_p | [−1, 1] | D | Weil bound |
| Distribution | Semicircle (2/π)sin²θ dθ | D | Katz 1988 |
| Mean E[α_p] | 0 | D | Symmetry + equidistribution |
| Variance E[α_p²] | 1/2 | D | Sato-Tate moments |
| Kl(1,1;p) mean | 0 | D | Same |
| Kl(1,1;p) variance | p/2 per prime | D | Same |
| A3(s) convergence | Absolute Re(s)>3/2 | D | Weil |
| A3(s) cancellation rate | O(X^{1/2−s+ε}) | C | Square-root conjecture |
| A3(s) continuation to Re(s)>1 | Unknown unconditionally | B | Kuznetsov (see K8_KUZNETSOV) |
