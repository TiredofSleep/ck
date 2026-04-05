# PRIME–π–φ BRIDGE — FINAL TIGHTENING
## The Reduction Test C_p ∈ ℚ + ℚA_p as the Central Object

**Document type:** Mathematical tightening. Replaces loose wording in prior addendum. Does not rewrite the memo.  
**Scope:** Exact proof skeleton for the reduction test. Nothing else added.  
**Date:** 2026-04-04  

---

## THE CANONICAL CHAIN

Three layers, defined explicitly.

**Layer 1 — Finite cyclotomic generator:**
$$A_p := 2\cos(\pi/p) \in \mathbb{Q}(\zeta_{2p})^+, \quad \deg(A_p/\mathbb{Q}) = \frac{p-1}{2}$$

**Layer 2 — Complementary closure:**
$$C_p := 4 - A_p^2 = 4 - 4\cos^2(\pi/p) = 4\sin^2(\pi/p)$$

This is the Pythagorean complement of A_p within the same angle π/p. It requires no additional choices.

**Layer 3 — Analytic normalization:**
$$S_p := \operatorname{sinc}^2(1/p) = \frac{\sin^2(\pi/p)}{(\pi/p)^2} = \frac{p^2}{4\pi^2}\,C_p$$

The sinc² operator is the minimal scale-normalization of C_p by the same angle. It separates the algebraic content (C_p, a polynomial in A_p) from the transcendental factor 1/π².

---

## THE REDUCTION TEST

**Definition.** A prime p passes the first-order reduction test if
$$C_p \in \mathbb{Q} + \mathbb{Q}A_p.$$
That is: the complementary closure term reduces to a linear expression in the same generator A_p.

**Key equivalence (exact).** The following are equivalent:
$$C_p \in \mathbb{Q} + \mathbb{Q}A_p$$
$$\iff \quad A_p^2 \in \mathbb{Q} + \mathbb{Q}A_p$$
$$\iff \quad A_p^2 = \alpha + \beta A_p \text{ for some } \alpha, \beta \in \mathbb{Q}$$
$$\iff \quad A_p \text{ satisfies a degree-2 polynomial over } \mathbb{Q}$$
$$\iff \quad \deg(A_p/\mathbb{Q}) \leq 2.$$

The test therefore reduces entirely to the algebraic degree of A_p.

---

## PROPOSITION: p = 5 IS THE UNIQUE FIRST NONTRIVIAL CLOSURE

**Proposition.** For odd primes p, let A_p = 2cos(π/p) and C_p = 4 − A_p². Then p = 5 is the smallest prime for which:
1. A_p is irrational, and
2. C_p ∈ ℚ + ℚA_p.

**Proof.**

**Case p = 2, 3.**  
A_2 = 0, A_3 = 1. Both rational. Condition (1) fails. These cases are trivially closed but algebraically empty.

**Case p = 5.**  
A_5 = φ = (1+√5)/2, with minimal polynomial x² − x − 1 over ℚ. So deg(A_5) = 2.  
Condition (1): φ ∉ ℚ. ✓  
Condition (2): Since deg(φ) = 2, the equivalence chain gives C_5 ∈ ℚ + ℚφ. Explicitly: φ² = φ+1, therefore
$$C_5 = 4 - \varphi^2 = 4 - (\varphi + 1) = 3 - \varphi \in \mathbb{Q} + \mathbb{Q}\varphi. \checkmark$$
Both conditions satisfied. □

**Case p ≥ 7.**  
deg(A_p) = (p−1)/2 ≥ 3.  
Suppose for contradiction that C_p ∈ ℚ + ℚA_p. Then A_p² = α + βA_p for some α, β ∈ ℚ, so A_p satisfies the polynomial t² − βt − α = 0 of degree 2 over ℚ. This contradicts deg(A_p) ≥ 3. Therefore C_p ∉ ℚ + ℚA_p for all p ≥ 7.  
Condition (2) fails. Obstruction persists at every prime p ≥ 7. □

---

## CLOSURE TABLE

| p | deg(A_p) | deg ≤ 2? | C_p ∈ ℚ + ℚA_p? | S_p = sinc²(1/p) | Closure class |
|---|----------|----------|-----------------|-----------------|---------------|
| 2 | 1 | yes | yes (trivially) | 0.405285 | trivial rational |
| 3 | 1 | yes | yes (trivially) | 0.683918 | trivial rational |
| **5** | **2** | **yes** | **yes: 3−φ** | **0.875140** | **first nontrivial closure** |
| 7 | 3 | no | no | 0.934637 | obstructed |
| 11 | 5 | no | no | 0.973105 | obstructed |
| 13 | 6 | no | no | 0.980350 | obstructed |

---

## THE STRUCTURAL CLAIM

The significance of p = 5 is not merely that 2cos(π/5) = φ, but that p = 5 is the first prime for which the complementary closure term C_p = 4 − A_p² reduces to first order in the same cyclotomic generator.

The true structural statement: the canonical chain A_p ↦ C_p ↦ S_p first closes nontrivially at p = 5, because C_p = 4 − A_p² reduces to a linear expression in A_p only in the degree-2 case, and p = 5 is the first prime achieving degree 2.

---

## TANGENT RESULT — EXACT POSITION

$$\operatorname{sinc}^2(1/2) = \frac{4}{\pi^2}, \qquad \left|\frac{d}{dr}\operatorname{sinc}^2(r)\right|_{r=1/2} = \frac{16}{\pi^2} = 4 \cdot \frac{4}{\pi^2}$$

Both identities are exact. The factor 4 comes from the logarithmic derivative at r = 1/2: since cot(π/2) = 0, the log-derivative equals −4 exactly.

The numerical proximity 16/π² ≈ φ (relative error 0.19%) is downstream of this exact geometry and is approximate. It is not the primary structural identity.

---

## BOUNDARY (FINAL)

What is not yet established is whether the exact p = 5 closure mechanism and the sinc² critical-line geometry are connected by a deeper arithmetic or operator-theoretic principle, rather than meeting only through one exact mixed formula and one notable approximation.
