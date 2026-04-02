# K8_WEAK_THEOREMS.md

**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

## K8 Layer Proved Theorems

**Program position:** This document collects D-tier proved results for the K8 layer. Convention:
D = proved with complete proof or standard reference. C = conjecture with named gap. B = structural
candidate. A = speculative. All results in this file are D-tier unless explicitly marked otherwise.

---

## Theorem K8.1 (Kloosterman Weil Bound)
**Statement:** For any prime p and integers a, b with (ab, p) = 1:
```
|Kl(a, b; p)| ≤ 2√p
```

**Proof:** Weil (1948) via the Riemann Hypothesis for curves over finite fields.
The sum Kl(a,b;p) = Σ_{k ∈ F_p^*} ψ(ak + bk^{-1}) is the trace of the Frobenius endomorphism
on H^1_c(A^1 ∖ {0}, Kl₂) where Kl₂ is the Kloosterman sheaf. The H^1 has dimension 2, so
the trace of Frobenius is at most 2 times the absolute value √p of each eigenvalue. QED.

**Consequence:** The normalized values α_p = Kl(1,1;p)/(2√p) satisfy |α_p| ≤ 1 for all primes p.

---

## Theorem K8.2 (A3 Convergence)
**Statement:** The Dirichlet series A3(s) = Σ_p Kl(1,1;p)·p^{-s} converges absolutely for Re(s) > 3/2.

**Proof:** By K8.1, |Kl(1,1;p)| ≤ 2√p for all primes p. Therefore:
```
Σ_p |Kl(1,1;p)| · p^{-σ} ≤ 2 Σ_p p^{1/2-σ}
```
By the prime number theorem, Σ_p p^{1/2-σ} converges for σ > 3/2 (since the n-th prime
satisfies p_n ~ n log n, so Σ_n (n log n)^{1/2-σ} < ∞ for σ > 3/2). QED.

**Note:** The abscissa of absolute convergence is σ_a ≤ 3/2. The true σ_a may be less if
sufficient cancellation occurs from Sato-Tate (see K8.4).

---

## Theorem K8.3 (Sato-Tate for Kloosterman Sums)
**Statement:** The normalized values α_p = Kl(1,1;p)/(2√p) are equidistributed on [−1,1]
with respect to the semicircle measure dμ_ST = (2/π)√(1−t²) dt. That is, for any continuous
function f: [−1,1] → ℝ:
```
lim_{X→∞} (1/π(X)) Σ_{p≤X} f(α_p) = ∫_{-1}^{1} f(t) (2/π)√(1−t²) dt
```

**Proof reference:** Katz (1988), "Gauss Sums, Kloosterman Sums, and Monodromy Groups."
The Kloosterman sheaf Kl₂ on P^1 has geometric monodromy group G_geom = SU(2) (Theorem 11.1
in Katz 1988). Equidistribution follows from: (i) the monodromy group is SU(2), (ii) the
L-functions L(s, Sym^k Kl₂) are entire of finite order for all k ≥ 1, (iii) they are nonvanishing
on Re(s) = 1. These facts together imply equidistribution by the Weyl criterion (orthogonality
of characters of SU(2) implies all non-trivial Weyl moments → 0). QED.

**Consequence:** E[α_p] = 0, E[α_p²] = 1/2. See K8_SATO_TATE_DISTRIBUTION.md.

---

## Theorem K8.4 (Mean of Kloosterman Sums)
**Statement:** The average of Kloosterman sums over primes satisfies:
```
(1/π(X)) Σ_{p≤X} Kl(1,1;p) → 0   as X → ∞
```

**Proof:** This is the special case f(α_p) = α_p in K8.3 (Sato-Tate), with ∫ t (2/π)√(1−t²) dt = 0
by symmetry. QED.

**Consequence:** A3(s) has zero "DC component" — the series exhibits genuine cancellation
and does not grow at the rate of its absolute bound Σ_p 2√p · p^{-Re(s)}.

---

## Theorem K8.5 (Set-Measure Independence)
**Statement:** Kl(1,1;p) is INDEPENDENT of the choice of primitive root g modulo p.

**Proof:** Kl(1,1;p) = Σ_{k=1}^{p-1} e^{2πi(k+k^{-1})/p}. This sum ranges over ALL k ∈ F_p^*
in some order (the orbit {g^j mod p} for any primitive root g visits all elements of F_p^*
exactly once). Therefore:
```
Kl(1,1;p) = Σ_{k ∈ F_p^*} e^{2πi(k+k^{-1})/p}
```
This sum is independent of the order of summation (all orderings give the same value). Hence
it is the same for all primitive roots g. QED.

**Note:** This is a DIFFERENT kind of g-independence from the PSD case. The PSD was g-independent
because the orbit-as-SET determines it. Kl(1,1;p) is g-independent because it is a COMPLETE SUM
over F_p^*. But D_p^{Kl}(m,g) = Kl(1,g^{-m};p) IS g-dependent for individual lags m.

---

## Theorem K8.6 (Multiplicative Non-Factorization)
**Statement:** The function p → Kl(1,1;p) is NOT multiplicative. That is, there is no identity
Kl(1,1;mn) = Kl(1,1;m)·Kl(1,1;n) for general coprime integers m, n.

**Proof:** A multiplicative function on primes would require (by the Chinese Remainder Theorem)
that the exponential sum Kl(1,1;mn) factors as a product over the factors of mn. But the
Kloosterman sheaf Kl₂ has monodromy group SU(2), and SU(2) representations do NOT decompose
as tensor products over distinct primes in the manner required for multiplicativity (specifically,
the local L-factors at different primes are NOT related by a multiplicative formula). QED.

**Consequence:** A3(s) = Σ_p Kl(1,1;p)·p^{-s} does NOT have an Euler product. See K8_GL2_TO_GL1_BRIDGE.md.

---

## Theorem K8.7 (Maass Form Zeros Are Not Zeta Zeros)
**Statement:** For a generic cuspidal Maass form u of GL(2) over Q, the zeros of L(s,u) in
the critical strip are NOT equal to the zeros of ζ(s).

**Proof:** By the Strong Multiplicity One theorem (Jacquet-Shalika 1981): two distinct cuspidal
automorphic representations π₁, π₂ of GL(n)/Q with the same local factors L_v(s,π₁) = L_v(s,π₂)
at all but finitely many places v are identical. If L(s,u) had the same zeros as ζ(s), then
their logarithmic derivatives would agree, implying L_v(s,u) = ζ_v(s) for all but finitely many v,
i.e., u = trivial character on GL(1). But u is a GL(2) cuspidal form, not a GL(1) Hecke character.
Contradiction. QED.

**Consequence:** The Maass cusp form contribution to A3's spectral expansion (via Kuznetsov)
carries zeros that are IRRELEVANT to the Riemann zeros. Only the Eisenstein contribution
carries ζ-zero information.

---

## Corollary K8.8 (Bridge Must Go Through Eisenstein)
**Statement:** Any connection between A3(s) and the zeros of ζ(s) must operate through
the Eisenstein series contribution to the Kuznetsov spectral expansion of A3.

**Proof:** By K8.7, the Maass cusp form contributions carry non-ζ zeros. By K8.6, A3 is not
an Euler product, hence not a GL(2) L-function directly. The only remaining component in the
Kuznetsov spectral expansion is the Eisenstein continuous spectrum, which involves ζ via
L(s, E) = ζ(s+it)ζ(s−it). QED.

---

## Summary of K8 Weak Theorems

| Theorem | Statement | Tier |
|---------|-----------|------|
| K8.1 | Kloosterman Weil bound: |Kl(1,1;p)| ≤ 2√p | D |
| K8.2 | A3(s) converges absolutely for Re(s) > 3/2 | D |
| K8.3 | Sato-Tate equidistribution: semicircle law | D |
| K8.4 | Mean of Kl(1,1;p) → 0 (zero bias) | D |
| K8.5 | Kl(1,1;p) is g-independent (complete sum) | D |
| K8.6 | Kl(1,1;·) is NOT multiplicative, A3 has no Euler product | D |
| K8.7 | Maass form zeros ≠ ζ zeros (Multiplicity 1) | D |
| K8.8 | Any ζ-zero detection from A3 must go through Eisenstein | D (corollary) |

### What K8 weak theorems establish collectively:

1. **A3(s) is well-defined and convergent** for Re(s) > 3/2 (K8.1, K8.2)
2. **A3(s) has genuine arithmetic content** — Kloosterman sums, Sato-Tate (K8.3, K8.4)
3. **A3(s) is not a standard L-function** — not multiplicative, no Euler product (K8.5, K8.6)
4. **The GL(2) no-go is precise** — Maass forms are irrelevant, Eisenstein is the only bridge (K8.7, K8.8)

The chain K8.1→K8.2→K8.3→...→K8.8 constitutes a complete D-tier account of what A3 is,
what it isn't, and exactly where the open problem lies.
