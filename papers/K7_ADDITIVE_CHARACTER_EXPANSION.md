# K7 — Additive Character Expansion

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Setup

From K7_EXACT_FORMULA_FOR_RP.md: the PSD of the prime-field orbit is

    Ŝ_p(ξ) = (1/(p−1)²) · sin²(πξ(p−1)/p) / sin²(πξ/p)

which is independent of the generator g. The PSD route is prime-blind (only encodes p,
not g). This document follows the ADDITIVE CHARACTER route — attempting to represent
D_p as a finite oscillatory sum over additive characters of F_p — and determines how far
this route carries before hitting the same prime-blindness wall.

---

## Additive Characters of F_p

The additive characters of F_p = Z/pZ are:
    ψ_a : k ↦ e^{2πi ak/p}    for a ∈ {0, 1, ..., p−1}

The trivial character is ψ_0 = 1.

**Key identity (additive orthogonality):**
    Σ_{k=0}^{p−1} ψ_a(k) = p · 1_{a ≡ 0 (mod p)}

**Finite Fourier expansion over F_p:**
Any function f : F_p → C admits the expansion:
    f(k) = (1/p) Σ_{a=0}^{p−1} f̂(a) ψ_a(k)
    f̂(a) = Σ_{k=0}^{p−1} f(k) ψ_{-a}(k)  =  Σ_{k=0}^{p−1} f(k) e^{-2πi ak/p}

---

## Expanding D_p via Additive Characters

### The PSD as a double character sum

    Ŝ_p(ξ) = |μ̂_p(ξ)|² = (1/(p-1)²) |Σ_{k=1}^{p-1} e^{-2πiξk/p}|²

Define the exponential sum S_p(ξ) = Σ_{k=1}^{p-1} e^{-2πiξk/p}.

By the geometric series formula (derived in K7_EXACT_FORMULA_FOR_RP.md):
    S_p(ξ) = e^{-iπξ} · sin(πξ(p-1)/p) / sin(πξ/p)

This is a COMPLETE additive character sum over F_p* = {1,...,p-1}. It is NOT a Gauss sum
(which would involve a multiplicative character ×additive character). It is purely additive.

### Is D_p naturally an incomplete character sum?

An incomplete character sum would be Σ_{k∈A} e^{-2πiξk/p} for a proper subset A ⊂ F_p*.

The orbit Ω_p = {g^0 mod p, ..., g^{p-2} mod p} = {1,...,p-1} as a SET. So summing over
the orbit (as a set) gives a COMPLETE sum S_p(ξ).

**Finding:** The additive character sum over the prime-field orbit is a COMPLETE sum,
not an incomplete one. There is no window or restriction on which elements are summed.
This is why it evaluates to a closed-form expression independent of g.

### The sinc² main term from zero frequency

At frequency a = 0 (the trivial character ψ_0):
    f̂(0) = Σ_{k=0}^{p-1} f(k) · 1 = Σ f(k)    (= (p-1) if f is the indicator of F_p*)

The zero-frequency contribution to μ̂_p(ξ):
The orbit indicator 1_{orbit}(k) = 1 for all k ∈ {1,...,p-1}.

At ξ → 0: S_p(ξ) → p-1 (sum of (p-1) ones), μ̂_p(0) = 1. ✓

**Does sinc² come from the zero mode?**

For continuous ξ, the sum S_p(ξ) = Σ_{k=1}^{p-1} e^{-2πiξk/p} is an evaluation of the
finite Fourier transform at a CONTINUOUS argument ξ (not restricted to F_p).

As ξ varies continuously, the sum interpolates between the discrete evaluations:
- At ξ = 0: sum = p-1 (peak)
- At ξ = n/2 for small integer n: sum ≈ (p-1)sinc(n)/(something)

The sinc² ENVELOPE comes from the continuous interpolation of the discrete sum.
It is not a "zero mode" in the usual discrete sense — it is the continuum limit of
the sum as a function of continuous ξ.

**Precise statement:** The sinc²(ξ) main term comes from the UNIFORM DENSITY of the
orbit over {1,...,p-1}. Any set of p-1 uniformly spaced points in (0,1) produces the
same PSD → sinc². This is the universal K5.1 content, not additive character content.

**D_p is NOT naturally an incomplete additive character sum.**

---

## The Additive Fourier Decomposition of the Autocorrelation

Write the empirical autocorrelation in additive character language:

    A_p(τ) = (μ_p * μ̃_p)(τ) = (1/(p-1)²) Σ_{a,b=1}^{p-1} δ_{(a-b)/p}(τ)

The Fourier transform:
    Â_p(ξ) = F[A_p](ξ) = (1/(p-1)²) Σ_{a,b=1}^{p-1} e^{-2πiξ(a-b)/p}
           = |S_p(ξ)/(p-1)|² = Ŝ_p(ξ)

In additive character modes, decompose:
    A_p(τ) = (1/p) Σ_{n=0}^{p-1} Â_p(n/p) e^{2πi n τ/p} · (1/(p-1))

Wait — the natural mode expansion for a function on the discrete grid {m/p : m ∈ Z/(p)} is:
    A_p(m/p) = (1/p) Σ_{n=0}^{p-1} c_n e^{2πi mn/p}
    c_n = Σ_{m=0}^{p-1} A_p(m/p) e^{-2πi mn/p}

Compute c_n:
    c_n = Σ_{m=0}^{p-1} (1/(p-1)²) #{(a,b): a-b ≡ m (mod p)} · e^{-2πimn/p}
        = (1/(p-1)²) Σ_{a,b=1}^{p-1} e^{-2πi(a-b)n/p}
        = (1/(p-1)²) |Σ_{a=1}^{p-1} e^{-2πian/p}|²

For n = 0: c_0 = (p-1)²/(p-1)² = 1.
For n ≠ 0: Σ_{a=1}^{p-1} e^{-2πian/p} = -1 (complete character sum minus trivial term).
    c_n = (-1)²/(p-1)² = 1/(p-1)²  for n ≠ 0.

**The additive Fourier modes of A_p are:**
- Mode 0: amplitude 1 (= tri(0))
- Mode n ≠ 0: amplitude 1/(p-1)² ≈ 1/p² (tiny, uniform)

**Finding:** The additive character decomposition of A_p is FLAT except at mode 0.
The correction D_p = √p(A_p − tri) has modes of size 1/(p-1)² × √p ≈ 1/p^{3/2} → 0.

This confirms: **in additive character space, D_p has NO structured mode content.**
All nonzero modes have the same tiny amplitude 1/(p-1)², with no prime-specific structure.

---

## Aliasing and Edge Corrections

**Aliasing:** The discrete measure μ_p is supported on {k/p : k=1,...,p-1}, so Ŝ_p(ξ) is
periodic with period p: Ŝ_p(ξ+p) = Ŝ_p(ξ). At each "alias frequency" ξ + np, the PSD
takes the same value. In the continuum limit this aliasing vanishes (period → ∞).

**Window edge corrections:** The orbit lies in (0,1) (open interval, missing 0 and 1).
The missing endpoints introduce edge corrections of order 1/p (since the orbit values
nearest 0 and 1 are 1/p and (p-1)/p). These corrections affect:
- The value of Ŝ_p at ξ near 0: Ŝ_p(0) = 1 exactly (no correction)
- The value of Ŝ_p for large ξ: controlled by the lattice spacing 1/p

**Aliasing + edge corrections are deterministic in 1/p.** They contribute to D_p^{PSD}
but not to any prime-specific structure.

---

## Kloosterman Correction: Nonlinear Additive Phase

To get prime-specific content, we need NONLINEAR additive characters:

    Kl(a, b; p) = Σ_{k=1}^{p−1} ψ_a(k) ψ_b(k^{-1}) = Σ_{k=1}^{p−1} e^{2πi(ak + bk^{-1})/p}

This is a SUM OVER THE ORBIT with a phase that depends on BOTH k and k^{-1} mod p.
It cannot be reduced to a complete character sum. The Weil bound gives |Kl| ≤ 2√p.

**Why Kloosterman sums appear here:**
In the sequence autocorrelation at lag m, the cross-term is:

    Σ_{j=0}^{p-2} e^{2πi α g^j/p} e^{−2πiβ g^{−j}/p}

For α, β ≠ 0: this involves both g^j and g^{-j} = g^{p-1-j} simultaneously,
giving a Kloosterman-type sum after a change of variables.

This is genuinely g-dependent and prime-specific. It lives OUTSIDE the scope of
pure additive character analysis — it requires the multiplicative structure of F_p*.

---

## Summary: What the Additive Route Delivers

| Object | Additive expansion | Prime-specific? | Bounded after normalization? |
|--------|-------------------|-----------------|------------------------------|
| Ŝ_p(ξ) | Complete sum — closed form | No (g-independent) | N/A (exact formula) |
| A_p(m/p) discrete modes | Mode 0 = 1, all others = 1/(p-1)² | No (uniform across modes) | No (→ 0 after √p) |
| D_p^{PSD}(ξ) | Smooth in 1/p | No | Yes (→ deterministic limit) |
| Kl(a, b; p) | Nonlinear additive phase | **Yes** | **Yes (|Kl|/p ≤ 2/√p, so √p·Kl/p = O(1))** |

**Finding: pure additive character expansion reaches a wall at the complete-sum boundary.**
No prime-specific, bounded, non-deterministic correction emerges from additive characters alone.

The additive route must be augmented by the MULTIPLICATIVE structure of F_p* (the group
of nonzero residues) to produce a prime-sensitive D_p. That is the Kloosterman / multiplicative
character route. See K7_MULTIPLICATIVE_CHARACTER_ROUTE.md.

---

## Positive Content: What the Additive Route Does Establish

1. **Exact formula for μ̂_p:** The additive character expansion gives μ̂_p(ξ) exactly
   (closed form). This is useful for computation. See k7_compute_dp.py.

2. **sinc² origin confirmed:** The sinc² main term comes from the UNIFORM DENSITY of
   the orbit, not from any specific additive character. It is truly universal (K5.1 content).

3. **Mode flatness:** The nonzero additive modes of A_p are all equal to 1/(p-1)².
   No mode is "special." The autocorrelation carries no structured additive harmonic content.

4. **Exact identification of the wall:** The additive route produces only complete sums,
   which reduce to ±1/(p-1). To get prime-specific O(√p)-amplitude content, we need
   the nonlinear Kloosterman structure.

---

*Prerequisite: K7_EXACT_FORMULA_FOR_RP.md*
*Feeds: K7_MULTIPLICATIVE_CHARACTER_ROUTE.md*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
