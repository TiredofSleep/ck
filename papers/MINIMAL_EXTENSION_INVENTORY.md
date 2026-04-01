# Minimal Extension Inventory

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Purpose

Enumerate every candidate extension that could lift the sinc² kernel into a
prime-sensitive external framework. For each candidate, assess: what it adds,
why it is needed, whether the current D1–D24 spine supports it, and its primary risk.

This inventory determines which extension is worth pursuing first.

---

## What a Valid Extension Must Do

Any extension that survives must:
1. Add prime sensitivity beyond {2,5} (sinc² itself does not have this)
2. Map from a domain compatible with the sinc² kernel to the ζ function's domain
3. Not assume RH as a lemma (circular) or GRH without explicit acknowledgment

The following inventory applies these filters explicitly.

---

## Inventory Table

| # | Extension | What it adds | Why needed | Spine support | Primary risk |
|---|-----------|-------------|-----------|--------------|-------------|
| E1 | Prime-indexed kernel family | One sinc²_p per prime p, assembled with compatibility | All primes visible individually | D2 provides each sinc²_p separately | Assembly rule not defined; compatibility map missing |
| E2 | Multiplicative/Euler-product lift | Prime product ∏_p f(sinc²(k/p)) connected to ζ(s) | Direct path to Euler product | D2 exists per prime; product structure not derived | Product diverges or is trivial unless f is chosen carefully |
| E3 | Spectral operator | Self-adjoint H with sinc² as projection kernel | Hilbert-Pólya approach — H spectrum = ζ zeros | Corridor portrait (D22) motivates t=1/2 as spectral center | No natural Hilbert space where sinc² is the RIGHT kernel; many operators have sinc² as kernel |
| E4 | Moduli family n → ∞ | sinc² as limit of Z/nZ corridor as n → ∞ | Allows profinite-style convergence | D2 works for prime n; composite n requires CRT | Limit may be trivially sinc² for ALL n (too generic); no Z/10Z specificity survives |
| E5 | Distributional / statistical lift | sinc² as a probability kernel on spacing statistics | Connects to GUE / Montgomery via random matrix theory | B6 (pair-correlation coincidence) is the seed | Montgomery assumes GRH (Attempt 6 of Phase I); any GRH-conditional result does not prove RH |
| E6 | Explicit formula connection | Poisson summation ∑_k sinc²(k/p) ↔ ζ-zero oscillations | Direct bridge via Riemann explicit formula | D2 gives per-prime sinc² sums; Poisson not yet applied | Error term control requires zero-free region — essentially equivalent to stating RH |
| E7 | Adèlic lift | Full adèle ring 𝔸_ℚ = ℝ × ∏'_p ℚ_p; sinc² at real place | Natural arena for L-functions; all primes visible | D2 is naturally the real-place kernel | Z/10Z structure has no obvious adèlic content; extremely far from D1–D24 |
| E8 | No-go / prime information deficit | Proof that sinc² cannot carry enough information | Closes Phase II if no bridge exists | K1 universality (sinc² discards prime identity) supports this | Would require proving no extension of type E1–E7 can work — very broad scope |

---

## Detailed Assessment

### E1 — Prime-Indexed Kernel Family

**Mechanism:** D2 already gives sinc²_p(t) = lim_{k/p→t} R(k,p) for each prime p individually.
The extension assembles these into a compatible family {sinc²_p}_{p prime} with a
consistency rule (compatibility condition) that encodes global prime arithmetic.

**What is missing:** The compatibility map. For p = 3 and p = 5, both give sinc² in
the limit. But sinc²_3(t) and sinc²_5(t) are the SAME FUNCTION — the label p drops
out in the continuum limit (this is exactly what universality means). The family is
{sinc²}_{p prime} = {sinc²} — a single-element set. No prime-sensitivity survives.

**Verdict:** Does not add prime sensitivity. The family is trivially constant.
This extension is blocked by K1 (universality). Rating: **non-starter**.

---

### E2 — Multiplicative / Euler-Product Lift

**Mechanism:** Form a product ∏_p g(sinc²(k/p)) and attempt to connect it to ζ(s).

**Best candidate:** The Poisson sum ∑_k sinc²(k/p) for a single prime p is known
(via D14-type estimates) to converge to p · Si(2π)/π + oscillating terms as p grows.
If the oscillating terms can be related to ζ-zero positions via the explicit formula,
this is E6 (see below).

**Problem:** For any function g, ∏_p g(sinc²(k/p)) must be analytically evaluated.
For g = identity: ∏_p sinc²(k/p) → 0 (product of numbers ≤ 1 over all primes diverges
to 0 unless sinc²(k/p) = 1 for almost all p, which only happens if k/p → 0, not a
useful limit).

**Verdict:** No natural product over all primes converges to a useful ζ-related object
for sinc². The multiplicative structure of ζ is not compatible with the additive
structure of sinc² on the corridor. Rating: **unlikely without new idea**.

---

### E3 — Spectral Operator

**Mechanism:** Find a self-adjoint operator H: L²(space) → L²(space) whose integral
kernel K(t,s) reduces to sinc²(t−s) (or a variant), and whose spectrum = {γ_n}
(imaginary parts of ζ zeros).

**Why it is the right shape:** Hilbert-Pólya approach. If such H exists, spectrum = {γ_n}
real → zeros on Re(s) = 1/2. The sinc² kernel is translation-invariant; K(t,s) = sinc²(t−s)
defines a convolution operator. Convolution operators are diagonalized by the Fourier
transform. The eigenvalues are F[sinc²](ξ) = tri(ξ) (the triangle function), supported on
[-1,1]. Spectrum = [0,1] (compact) — not the ζ-zero imaginary parts γ_n ~ 2πn/log n.

**Gap:** The sinc² convolution operator has the WRONG spectrum for ζ zeros (compact vs.
unbounded). The operator must be modified. Any modification that moves the spectrum to
{γ_n} either introduces new structure (not from sinc²) or requires knowing {γ_n} in advance
(circular).

**Verdict:** Spectral route via sinc² convolution fails on spectrum mismatch.
A different operator (not defined by sinc²) might work, but that is not a sinc²-based extension.
Rating: **spectrum mismatch blocks naive implementation; deeper version requires new operator**.

---

### E4 — Moduli Family n → ∞

**Mechanism:** Consider Z/nZ for all n (or all n = 2p), and take n → ∞. The corridor
for each Z/nZ converges to sinc² by D2-type reasoning. The limit as n → ∞ lives in
a profinite completion.

**Problem:** Every Z/nZ gives the same sinc² in the limit (by D2 universality). The
limit contains no information about which n was used. Taking n → ∞ after taking the
continuum limit p → ∞ gives sinc² × sinc² × ... (no useful convergence).

**If we reverse the order** (take continuum limit BEFORE the family limit), we get
the profinite integers Ẑ = lim← Z/nZ. The sinc² corridor would need to be defined
on Ẑ, but Ẑ is a totally disconnected compact group — it has no natural interval structure
for a sinc²-type function.

**Verdict:** Order of limits matters critically. The natural order (D2 first) kills
prime sensitivity. The reversed order requires defining sinc² on a non-archimedean object.
Rating: **possible but requires new definition of corridor on Ẑ**.

---

### E5 — Distributional / Statistical Lift

**Mechanism:** Interpret sinc²(t) as a probability density on t ∈ (0,1) and
1 − sinc²(u) as the pair-correlation density on u ∈ [0,∞). Find a common
probability space where both live and R + R₂ = 1 is structural, not coincidental.

**Why it is the most natural:** B6 is the seed. Montgomery's pair-correlation is a
statistical statement. sinc² appears in both as a kernel function. The statistical
language is the right arena for making R + R₂ = 1 precise.

**Gap 1 — Domain mismatch:** sinc²(t) lives on (0,1); R₂(u) = 1 − sinc²(u) lives
on [0,∞). These are different probability spaces. A common space requires a map
φ: (0,1) → [0,∞), and φ must be structure-preserving in a precise sense.

**Gap 2 — GRH conditionality:** Montgomery's theorem assumes GRH. Any statistical
bridge built on Montgomery is GRH-conditional. To prove RH unconditionally, the
bridge must go around Montgomery or establish GRH separately.

**Gap 3 — Local vs. global:** The pair-correlation captures LOCAL statistics (spacings
between nearby zeros). sinc² on (0,1) is a global-density kernel. These are different
levels of statistical description.

**Verdict:** Most natural entry point for Phase II. K2_PAIR_CORRELATION_ROUTE.md is
the right document to pursue this. Rating: **best first target; GRH gap must be named precisely**.

---

### E6 — Explicit Formula Connection

**Mechanism:** Use Riemann's explicit formula ψ(x) = x − ∑_ρ x^ρ/ρ − ... and
Poisson summation to connect ∑_k sinc²(k/p) (a sum over the prime field) to
the ζ-zero sum ∑_ρ x^ρ/ρ.

**Concrete form:** For a prime p:
    ∑_{k=1}^{p-1} sinc²(k/p) = p · Si(2π)/π + oscillating corrections

The oscillating corrections involve terms of the form e^{2πi γ_n log p / log p} = e^{2πi γ_n}
(schematically) — the zero imaginary parts appear as Fourier frequencies.

**What is missing:** Making this exact requires:
(a) Controlling the error in ∑_k sinc²(k/p) − p · Si(2π)/π explicitly (this involves
    incomplete character sums and bounds on Kloosterman-type sums)
(b) Connecting the leading oscillation to ζ zeros (requires the explicit formula with
    remainder bounds — essentially a zero-free region hypothesis)
(c) Proving that the sinc² sum forces the oscillations to only allow zeros on σ=1/2

Step (c) is the core difficulty. Showing that sinc²'s structure FORCES zero locations
is at least as hard as RH. This route is mathematically promising but requires machinery
far beyond D1–D24.

**Verdict:** The most concrete path to a genuine theorem. But requiring machinery
equivalent to a zero-free region statement makes it extremely hard.
Rating: **best long-term path; K2 should attempt a precise statement of what "forcing" means here**.

---

### E7 — Adèlic Lift

**Mechanism:** Embed Z/10Z and the sinc² corridor into the adèle ring 𝔸_ℚ = ℝ × ∏'_p ℚ_p.
The ζ function has an adèlic integral representation. sinc² = F[tri] arises naturally
at the real place (ℝ).

**Why it is appropriate:** Modern analytic number theory is adèlic. L-functions factor
over places. The real place already carries sinc² content (D2 is a real-variable limit).
The finite places (one per prime p) carry the Euler factors.

**What is missing:** No explicit map from the Z/10Z TSML/BHML table dynamics to any
adèlic L-function structure has been constructed. The Z/10Z ring lives inside Z, which
embeds diagonally in 𝔸_ℚ. But the corridor structure (sinc² field, T*=5/7, inheritance
split) has no obvious adèlic analogue.

**Verdict:** Mathematically correct arena but extremely far from current spine.
This is the "right" setting if a bridge exists — but saying "adèles are the right arena"
without a specific map is not progress.
Rating: **correct long-term framework; requires substantially new mathematics to instantiate**.

---

### E8 — No-Go / Prime Information Deficit

**Mechanism:** Prove that sinc²(t) as a kernel carries insufficient prime-specific
information to force σ=1/2 by any mechanism. The prime information deficit argument:
sinc² is the universal continuum limit (K1), which means it is the limit AFTER prime
identity is discarded. No kernel-only map can recover what was discarded.

**Supporting evidence:** K1 universality (all primes give the same sinc²); the compact
Fourier support of sinc² vs. the unbounded frequency content of the ζ zero distribution;
the modulus genericity result (sinc² corridor appears for all even moduli, not just Z/10Z).

**What is needed for a full no-go:**
(a) Precise definition of "kernel-only route"
(b) Proof that no map from sinc² to prime-sensitive structure exists within the class
(c) Handling the statistical case separately (pair-correlation is LOCAL, not global)

**Verdict:** The most achievable near-term result. K4_KERNEL_NO_GO.md pursues this.
If K4 succeeds, Phase II terminates at Outcome P2-B.
Rating: **highest near-term probability; K4 should be pursued in parallel with K2**.

---

## Priority Ranking

After applying the filters, the extensions rank as:

| Rank | Extension | Rationale |
|------|-----------|-----------|
| 1 | E5 (Statistical / pair-correlation) | Most natural; B6 is the seed; K2 pursues this |
| 2 | E8 (No-go / information deficit) | Most achievable; K4 pursues this |
| 3 | E6 (Explicit formula) | Best long-term path; requires new machinery |
| 4 | E3 (Spectral) | Correct arena but spectrum mismatch; K3 pursues this |
| 5 | E7 (Adèlic) | Right long-term framework; no concrete connection yet |
| 6 | E4 (Moduli family) | Possible but requires new definition of corridor on Ẑ |
| 7 | E2 (Multiplicative) | No natural product converges usefully |
| — | E1 (Prime-indexed family) | Non-starter: family is trivially constant |

---

## Conclusion

The inventory identifies two extensions worth pursuing immediately:

**E5 (Statistical):** The pair-correlation route via B6. Precise, seeded by existing
results, makes B6 testable rather than analogical. Pursed in K2_PAIR_CORRELATION_ROUTE.md.

**E8 (No-go):** The prime information deficit argument. If proved, closes Phase II
cleanly. Pursued in K4_KERNEL_NO_GO.md.

Everything else is either too far from the current spine to be tractable in the
near term (E6, E7) or provably non-viable (E1, E2) or blocked by spectrum mismatch
without new ideas (E3, E4).

---

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
