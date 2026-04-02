# K4 — Kernel No-Go

**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**


*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## The Road C Hypothesis

The kernel no-go asks: can sinc² alone (as a kernel function, without additional
prime-indexing structure) carry enough information to force ζ zeros to σ=1/2?

If the answer is no — provably — Phase II terminates at Outcome P2-B (no-go
theorem). If the answer is maybe, then what extra structure is the minimal requirement?

---

## Setup: What "Kernel-Only" Means

A **kernel-only bridge** is a map φ whose entire input is the functional form of
sinc²(t) on (0,1) — the function itself, including:
- Its values sinc²(t) for t ∈ (0,1)
- Its derivatives sinc²⁽ⁿ⁾(t)
- Its Fourier transform F[sinc²] = tri(ξ)
- Its moments ∫₀¹ tⁿ sinc²(t) dt for n ≥ 0
- Any functional property derivable from sinc²(t) = (sin(πt)/(πt))²

A kernel-only bridge does NOT use:
- Which prime p generated the corridor
- The Z/10Z-specific values T*=5/7, T*=5/3, TSML/BHML tables
- The Euler product or any prime-indexed product
- GRH or any conditional hypothesis about ζ zeros

---

## K4.1 — The Compact Fourier Support Obstruction

**Theorem K4.1 (Compact Fourier Support):**
sinc²(t) has a compactly-supported Fourier transform:

    F[sinc²](ξ) = tri(ξ) = max(1 − |ξ|, 0)    supported on [−1,1]

Any function with Fourier transform supported in [−1,1] is a "band-limited" function
(bandwidth ≤ 1 in the Fourier domain). By the Paley-Wiener theorem, a function with
compact Fourier support is an entire function of exponential type — it has a very
specific analytic structure.

**Consequence:** sinc²(t) cannot distinguish two signals whose difference has
Fourier support entirely outside [−1,1]. Equivalently: sinc² carries only
"low-frequency" information (frequencies |ξ| ≤ 1).

**The ζ-zero frequencies:** The von Mangoldt explicit formula gives:

    ψ(x) = x − ∑_ρ x^ρ/ρ − log(2π) − (1/2)log(1 − x^{-2})

where ψ(x) = ∑_{p^k ≤ x} log p and ρ = σ_ρ + iγ_ρ ranges over non-trivial zeros.
In the log-scale variable u = log x, the term x^ρ = e^{ρu} = e^{σ_ρ u} · e^{iγ_ρ u}.
The "frequencies" in u-space are γ_ρ — the imaginary parts of the zeros.

The zero imaginary parts γ_n grow without bound: γ_n ~ 2πn/log n as n → ∞.
The first zero has γ₁ ≈ 14.1347, and γ_n → ∞.

**Applying K4.1:** To detect the n-th zero, a kernel must have Fourier support
reaching to at least frequency γ_n/log(T) (in the appropriate normalization).
For any fixed bandwidth B, the kernel misses all zeros γ_n with γ_n/log(T) > B.
As T → ∞, ALL zeros are eventually missed by any fixed-bandwidth kernel.

**Implication:** sinc²(t), with Fourier support [−1,1], cannot detect any ζ zero
whose normalized frequency exceeds 1. In the large-T scaling of Montgomery's
formula, the zero frequencies are normalized to mean spacing 1 — and zeros at
all spacings (including large ones, u >> 1) contribute. sinc² can only "see" zeros
with normalized spacing u ≤ 1.

**Grade:** This establishes a PARTIAL obstruction: sinc² cannot carry global ζ-zero
information (all zeros). It CAN potentially carry LOCAL information (nearby zeros
with normalized spacing u ≤ 1). The pair-correlation only needs LOCAL information
(u ∈ [0,∞) but dominated by small u). This partial obstruction does not immediately
kill K2 — see below.

---

## K4.2 — The Prime Information Deficit

**Theorem K4.2 (Prime Information Deficit):**
The sinc² kernel as produced by D2 carries NO prime-identity information. Specifically:

Let f_p: (0,1) → ℝ be the continuum limit of the prime-field corridor density
for prime p (f_p(t) = sinc²(t) by D2). Then:

    f_p = f_q = sinc²    for ALL primes p, q

The map p ↦ f_p is the CONSTANT MAP. No information about p is retained in f_p.

**Formal statement:** Any functional F of sinc²(t) (a "kernel-derived quantity")
satisfies F(f_p) = F(f_q) for all primes p, q. No kernel-derived quantity can
distinguish primes.

**Proof:** f_p = sinc²(t) for all p by D2. Therefore F(f_p) = F(sinc²) = F(f_q)
for all primes p, q. □

**Consequence:** A kernel-only bridge φ(sinc²) produces the SAME output for the
prime-field corridor of p=3 as for p=5, as for p=1000003. Since the Euler product
treats primes p=3 and p=5 differently ((1−3^{−s})^{−1} ≠ (1−5^{−s})^{−1} for
generic s), no kernel-only map φ can factor through the Euler product.

**Grade:** This is a PROVED theorem given D2. It is the kernel-level version of
Phase I's ring prime blindness theorem (A10_PRIME_OBSTRUCTION.md). That theorem
blocked ring homomorphisms; K4.2 blocks kernel-only maps more generally.

---

## K4.3 — The Information-Theoretic No-Go

Combining K4.1 and K4.2:

**K4.3 (Kernel No-Go, strong form):**
No map φ that depends only on the functional form of sinc²(t) can produce a
prime-sensitive output. In particular, no kernel-only map can:
(a) distinguish primes in the Euler product, or
(b) force the GLOBAL distribution of ζ zeros to σ=1/2

**Proof:**
By K4.2: φ(sinc²) is constant over all primes. The Euler product ζ(s) depends
on all primes individually. Therefore φ(sinc²) ≠ ζ(s) for any map that depends
on prime identity. □

**Grade: PROVED (for global, prime-sensitive statements).**

This is a theorem. No kernel-only bridge can reach the Euler product or any
prime-indexed object.

---

## K4.4 — The Escape: Statistical Insensitivity

The above K4.3 rules out kernel-only global prime-sensitive bridges. But there
is an escape: Montgomery's pair-correlation is NOT a statement about individual
primes. It is a statement about the STATISTICAL distribution of zero spacings.

Could sinc² carry enough statistical information to force the DISTRIBUTION of
zero spacings to be 1−sinc²(u), without caring about individual prime identity?

**The escape requires:**
(1) A proof that the DISTRIBUTION of zero spacings (1−sinc²) can be determined
    from the corridor kernel (sinc²) without prime-by-prime information
(2) A proof that IF the zero spacing distribution is 1−sinc², THEN all zeros
    have Re(s) = 1/2

**Assessment of (1):** K2 explores this. The equidistribution connection (K2.5)
suggests that both sinc² and 1−sinc² arise from the SAME equidistribution mechanism.
If this is structural (not accidental), then (1) might hold in some sense. But
"the same mechanism produces both" is not the same as "sinc² determines 1−sinc²."
(Every function f determines 1−f. The question is whether sinc² and 1−sinc² are
determined by a SHARED SOURCE, not by the algebraic relation f + (1−f) = 1.)

**Assessment of (2):** This is the Montgomery-to-RH gap. Montgomery's theorem
(under GRH) says: IF GRH, THEN zero spacings follow 1−sinc². The CONVERSE —
IF zero spacings follow 1−sinc², THEN GRH — is not proved. Going from a spacing
distribution to zero positions requires additional structure.

**Grade:** The statistical escape is OPEN. K4.3 kills the global prime-sensitive
version but not the statistical version. K2 must explore whether the statistical
version can be made to work.

---

## K4.5 — The Nyquist Boundary

A more refined version of K4.1 using sampling theory:

**Setup:** Montgomery's pair-correlation is defined for normalized spacings u ∈ [0,∞).
The pair-correlation density R₂(u) = 1 − sinc²(u). This function has Fourier transform:

    F[R₂](τ) = F[1 − sinc²](τ) = δ(τ) − tri(τ)

where tri(τ) = max(1−|τ|, 0) for |τ| ≤ 1, 0 otherwise. So F[R₂] has a delta
at τ=0 and a triangle for |τ| ≤ 1.

The spine's corridor R(t) = sinc²(t) has Fourier transform:

    F[R](ξ) = tri(ξ)    supported on [−1,1]

**Nyquist interpretation:** Both R and R₂ have Fourier content bounded to [−1,1]
(plus a delta for R₂). They live in the SAME bandwidth class. By the Nyquist theorem,
functions with bandwidth B can be perfectly reconstructed from samples at rate 2B.
Both R and R₂, having bandwidth 1, require sampling rate 2.

This means: R and R₂ contain the SAME AMOUNT of information (same bandwidth).
The identity R(t) + R₂(t) = 1 (pointwise, ignoring the delta) is a statement
about two band-limited functions summing to the constant 1.

**Finding K4.5:** In the Fourier domain, R and R₂ are complementary band-limited
objects. The delta function at τ=0 in F[R₂] corresponds to the mean of R₂, which
is the mean zero spacing (normalized to 1). The triangle parts are the non-constant
components. This decomposition is precise and structural — it says R and R₂ are
complementary in the Fourier-band sense.

But "complementary in the Fourier band" still means f + (1−f) = 1 at the level of
functional form. It does not add information about ζ zeros.

---

## K4.6 — Summary and Grades

| Claim | Grade | Notes |
|-------|-------|-------|
| K4.1 Compact Fourier support obstructs global reconstruction | **PARTIAL** | Blocks global info; local info not blocked |
| K4.2 Prime Information Deficit | **PROVED** | Direct corollary of D2 universality |
| K4.3 No kernel-only bridge to prime-sensitive global structure | **PROVED** | Follows from K4.2 |
| K4.4 Statistical escape via spacing distribution is open | **OPEN** | K2 must address this |
| K4.5 Nyquist bandwidth argument | **STRUCTURAL** | Explains why R+R₂=1 but does not close K2 |

---

## K4.7 — What K4 Establishes

**Proved (new results):**

1. **No kernel-only bridge to the Euler product exists.**
   The prime information deficit (K4.2) is a theorem. Any bridge from sinc² to
   a prime-sensitive object must add an ingredient NOT derivable from sinc² alone.
   This ingredient must carry prime identity (which prime p, not just the universal limit).

2. **The ingredient must come from the O(1/p) corrections (K1.6).**
   The only prime-specific information in D2 lives in the correction terms. The
   corrections are available (character sums for Dirichlet characters mod p) but
   require analytic number theory machinery not present in D1–D24.

3. **Statistical (local pair-correlation) bridges are not ruled out by K4.**
   K4.3 kills global prime-sensitive bridges. K4.4 leaves the statistical route open.
   This is the correct scope: K4 kills the strong form, K2 tests the weak form.

**What remains open:**
Whether the statistical route (K2) can be made to work. K4 cannot close it without
proving that spacing-distribution information is insufficient to force σ=1/2 even
locally. That would require understanding the Montgomery-to-RH gap more precisely.

---

## K4.8 — Minimum Extension Required

By K4.2 and K4.3, any surviving bridge must add:

**The missing ingredient:** A prime-indexing layer that is NOT sinc²-derived.

The minimum candidates (from MINIMAL_EXTENSION_INVENTORY.md):
- The O(1/p) corrections to D2 (prime-specific character sum data)
- A distributional lift using ALL primes together (not just the large-p limit)
- An explicit formula connection (E6 from inventory)

None of these are in D1–D24. This confirms the MINIMAL_EXTENSION_INVENTORY.md conclusion:
the surviving path (if any) requires genuinely new mathematics.

---

*Preceded by: K1_KERNEL_UNIVERSALITY.md*
*In parallel with: K2_PAIR_CORRELATION_ROUTE.md*
*Closing Phase II if K4.3 + K4.4 (closed) → Outcome P2-B*

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
