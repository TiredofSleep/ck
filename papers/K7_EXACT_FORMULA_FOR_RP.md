# K7 — Exact Formula for R_p


*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## The Object

The prime-field orbit is:
    Ω_p = { g^j mod p / p  :  j = 0, 1, ..., p−2 }  ⊂  (0, 1)

Since g is a primitive root mod p, this is a permutation of { 1/p, 2/p, ..., (p−1)/p }.
As a point set, it is IDENTICAL to the regular lattice { k/p : k = 1,...,p−1 }
regardless of which primitive root g is chosen.

The empirical measure is:
    μ_p = (1/(p−1)) Σ_{k=1}^{p−1} δ_{k/p}

This measure is the same for all generators g.

---

## Exact Formula: The PSD of the Orbit

The power spectral density (PSD) is:
    Ŝ_p(ξ) = |μ̂_p(ξ)|²    where μ̂_p(ξ) = (1/(p−1)) Σ_{k=1}^{p−1} e^{−2πiξk/p}

### Step 1 — Compute μ̂_p(ξ) exactly

For general ξ, the sum Σ_{k=1}^{p−1} e^{−2πiξk/p} is a geometric series:

    Σ_{k=1}^{p−1} e^{−2πiξk/p}
        = e^{−2πiξ/p} · (1 − e^{−2πiξ(p−1)/p}) / (1 − e^{−2πiξ/p})    (ξ/p ∉ Z)

Using the identity (e^{iα} − e^{iβ}) = 2i e^{i(α+β)/2} sin((β−α)/2):

    Numerator:    e^{−2πiξ/p} − e^{−2πiξ}
                = −2i · e^{−iπξ(p+1)/p} · sin(πξ(p−1)/p)

    Denominator:  1 − e^{−2πiξ/p}
                = −2i · e^{−iπξ/p} · sin(πξ/p)

Therefore:

    Σ_{k=1}^{p−1} e^{−2πiξk/p} = e^{−iπξ} · sin(πξ(p−1)/p) / sin(πξ/p)

And:

    μ̂_p(ξ) = (e^{−iπξ} / (p−1)) · sin(πξ(p−1)/p) / sin(πξ/p)

### Step 2 — The exact PSD

    Ŝ_p(ξ) = |μ̂_p(ξ)|² = (1/(p−1)²) · sin²(πξ(p−1)/p) / sin²(πξ/p)

**This is an exact closed-form formula, valid for all ξ not an integer multiple of p.**

### Step 3 — Limiting cases

At ξ = 0:
    lim_{ξ→0} sin(πξ(p−1)/p)/sin(πξ/p) = (πξ(p−1)/p)/(πξ/p) = p−1
    Ŝ_p(0) = 1  ✓

At integer ξ = n (with p ∤ n):
    sin(πn(p−1)/p) = sin(πn − πn/p) = sin(πn)cos(πn/p) − cos(πn)sin(πn/p)
                   = 0 − (−1)^n sin(πn/p)  =  (−1)^{n+1} sin(πn/p)
    Ŝ_p(n) = (1/(p−1)²) · sin²(πn/p) / sin²(πn/p) = 1/(p−1)²

At ξ = kp (integer multiple of p):
    sin(πkp(p−1)/p) = sin(πk(p−1)) = 0
    Ŝ_p(kp) is ill-defined (limit needed); the limit = 1 by L'Hôpital.

---

## Continuum Limit and the sinc² Emergence

As p → ∞ with ξ fixed, let u = πξ/p → 0:

    sin(πξ(p−1)/p) = sin(πξ − u) = sin(πξ)cos(u) − cos(πξ)sin(u)
                   → sin(πξ)    (since u → 0)

    sin(πξ/p) = sin(u) → u = πξ/p

    (1/(p−1)²) · sin²(πξ(p−1)/p) / sin²(πξ/p)
        → (1/p²) · sin²(πξ) / (πξ/p)²
        = sin²(πξ) / (πξ)²
        = sinc²(ξ)

This confirms D2: Ŝ_p(ξ) → sinc²(ξ) as p → ∞.

---

## The Exact Correction

Define:
    Δ_p(ξ) = Ŝ_p(ξ) − sinc²(ξ)
            = (1/(p−1)²) · sin²(πξ(p−1)/p) / sin²(πξ/p) − sin²(πξ)/(πξ)²

**First key observation:** This formula depends only on p, not on the generator g.
For every prime p, the PSD correction is the SAME regardless of which primitive root is used.

### Leading-order expansion

Write u = πξ/p (small):

    sin((p−1)u) = sin(pu − u) = sin(pu)cos(u) − cos(pu)sin(u)

    Ŝ_p(ξ) = [sin(pu)cos(u) − cos(pu)sin(u)]² / ((p−1)²sin²(u))

For u → 0:
    sin(u) = u − u³/6 + ...
    cos(u) = 1 − u²/2 + ...

Expanding to order u² = O(ξ²/p²):

    Ŝ_p(ξ) = [sin(pu)(1 − u²/2) − cos(pu)·u(1 − u²/6)]²
              / ((p−1)²(u − u³/6)²(1+...))

At leading order in 1/p (keeping terms O(1/p)):

    Ŝ_p(ξ) = sinc²(ξ·(1 − 1/p)) · (1 + O(1/p²))

Using sinc²(ξ(1−1/p)) = sinc²(ξ) + (−ξ/p) · 2sinc(ξ) · (d sinc/dξ) + O(1/p²):

    d sinc(ξ)/dξ = [cos(πξ) − sinc(ξ)] / ξ

Therefore:

    Δ_p(ξ) = (−ξ/p) · 2sinc(ξ) · [cos(πξ) − sinc(ξ)]/ξ + O(1/p²)
            = (−2/p) sinc(ξ)[cos(πξ) − sinc(ξ)] + O(1/p²)

### The naturally normalized correction

The natural normalization in frequency space is multiplication by p (not √p):

    D_p^{PSD}(ξ) := p · Δ_p(ξ)

This gives:

    D_p^{PSD}(ξ)  →  −2 sinc(ξ)[cos(πξ) − sinc(ξ)]

as p → ∞. Using sinc(ξ)cos(πξ) = sin(πξ)cos(πξ)/(πξ) = sin(2πξ)/(2πξ) = sinc(2ξ):

**Leading-order PSD correction:**

    lim_{p→∞} D_p^{PSD}(ξ)  =  −2[sinc(2ξ) − sinc²(ξ)]

This limit is DETERMINISTIC — the same function of ξ regardless of p.

---

## Critical Finding: SET-BASED PSD IS G-INDEPENDENT AND DETERMINISTIC

**Two facts that determine the character of K7:**

**Fact 1 (G-independence):**
Since the orbit is a permutation of {1/p,...,(p−1)/p}, the empirical measure μ_p is
IDENTICAL for all generators g. Therefore Ŝ_p(ξ) = |μ̂_p(ξ)|² is independent of g.

**Fact 2 (Analytic in 1/p):**
The exact formula Ŝ_p(ξ) = (1/(p−1)²)sin²(πξ(p−1)/p)/sin²(πξ/p) is a real-analytic
function of 1/p for fixed ξ. Its Taylor expansion in 1/p has deterministic coefficients
involving only π, ξ, and integer arithmetic — no prime-specific content at any order.

**Consequence:**
The PSD-based D_p^{PSD}(ξ) = p · Δ_p(ξ) is NOT a prime-sensitive object. It is a smooth,
deterministic function of p (via 1/p expansion) that takes essentially the same value for
large primes. Its limit −2[sinc(2ξ) − sinc²(ξ)] is a universal curve.

**The PSD route is not the correct home for prime-specific information.**

---

## What IS Prime-Specific?

The prime-specific information must live in SEQUENCE statistics — statistics that depend
on the ORDER of orbit elements g^0/p, g^1/p, g^2/p, ... — not just the SET.

**The lag-m sequence autocorrelation:**

    B_p(m, t) = (1/(p−1)) Σ_{j=0}^{p−2} e^{2πit g^j/p} · e^{−2πit g^{j+m}/p}
              = (1/(p−1)) Σ_{j=0}^{p−2} e^{2πit g^j(1 − g^m)/p}
              = (1/(p−1)) Σ_{k=1}^{p−1} e^{2πit k(1 − g^m)/p}   (orbit = permutation)
              = complete exponential sum at t(1 − g^m)

For 1 − g^m ≢ 0 (mod p): this = −1/(p−1).
For 1 − g^m ≡ 0 (mod p): this = 1.

**The g-dependence enters ONLY through whether g^m ≡ 1 (mod p)**, i.e., whether m is a
multiple of the order of g. Since g is a primitive root, this happens only when p−1 | m.
For 0 < m < p−1: B_p(m, t) = −1/(p−1) always.

So pure lag-m sequence autocorrelation (linear phase) reduces to a complete sum → constant.
No g-dependence for 0 < m < p−1. Still no prime-specific signal.

**The correct candidate: nonlinear pairings of orbit elements.**

The only way to get g-dependence (generator-specific, hence prime-arithmetic-specific)
is through NONLINEAR functions of two orbit elements at different lags:

    K_p(m, a, b) = (1/(p−1)) Σ_{j=0}^{p−2} e^{2πi(a g^j + b g^{−j+m})/p}

For a = b = 1, this gives a KLOOSTERMAN SUM:
    Kl(1, g^m; p) = Σ_{k=1}^{p−1} e^{2πi(k + g^m/k)/p}

Kloosterman sums satisfy:
- |Kl(a, b; p)| ≤ 2√p (Weil bound for Kloosterman sums)
- They depend genuinely on both g^m (mod p) and p
- They are NOT reducible to complete character sums

This is the correct prime-sensitive object. See K7_MULTIPLICATIVE_CHARACTER_ROUTE.md.

---

## Summary

| Object | Formula | G-dependent? | Prime-specific? | O(1) after √p? |
|--------|---------|-------------|-----------------|----------------|
| μ̂_p(ξ) | e^{-iπξ}sin(πξ(p-1)/p)/((p-1)sin(πξ/p)) | No | Only via p | Yes |
| Ŝ_p(ξ) | sin²(πξ(p-1)/p)/((p-1)²sin²(πξ/p)) | No | Only via p (analytic in 1/p) | No |
| D_p^{PSD}(ξ) = p·(Ŝ_p−sinc²) | → −2[sinc(2ξ)−sinc²(ξ)] | No | No (deterministic) | Yes |
| B_p(m, t) | −1/(p−1) always for 0<m<p−1 | No | No | — |
| Kl(1, g^m; p) | Σ e^{2πi(k+g^m/k)/p} | **Yes** | **Yes** | **Yes (Weil: |Kl|≤2√p)** |

**The Kloosterman route is the only place where genuine prime-arithmetic specificity survives.**
The PSD route — however clean its exact formula — is prime-blind after the deterministic
leading term is subtracted.

See K7_MULTIPLICATIVE_CHARACTER_ROUTE.md for the Kloosterman development.
See K7_NO_GO_ATTEMPT.md for the formal proof that the PSD route is blocked.

---

*Feeds: K7_ADDITIVE_CHARACTER_EXPANSION.md, K7_MULTIPLICATIVE_CHARACTER_ROUTE.md,*
*K7_NO_GO_ATTEMPT.md, k7_compute_dp.py*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
