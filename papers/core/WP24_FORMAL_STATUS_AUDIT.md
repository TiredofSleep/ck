# TIG/RH Framework — Formal Status Audit
## What Is Proved, What Is Structural, What Is Open

*Brayden Sanders — 7Site LLC | DOI: 10.5281/zenodo.18852047*
*Version: March 2026 sprint.*

---

## Purpose

This document is a standing logical audit of every claim made across the TIG
Clay Battery papers. Claims are sorted into four bins: PROVED (exact algebraic
result), STRUCTURAL (new language for a known fact), EMPIRICAL (observed in
data, stated with falsification test), and OPEN (the Clay gap). Nothing is
presented as proved that is not.

---

## Bin 1: PROVED (exact algebraic results)

| Claim | Proof | Location |
|-------|-------|----------|
| TSML has exactly 4 residual operators {PRG, COL, BRT, RST} | Table enumeration, 0 exceptions in 81 pairs | tsml_ag23_verify.py, 76 assertions |
| Residuals exist only in anchor columns {CTR, COL, RST} | Table enumeration | Same |
| Corner-word collapse: every w ∈ C* evaluates to {3,7} | Induction on Lemma 2.2 + corner multiplication sub-table | WP20_RH_PRIME_CORNER_COLLAPSE |
| Gap inaccessibility: C-words never enter G = {2,4,5,6,8} | Corollary of corner-word collapse | Same |
| The 3-9 chain: 3∘9ⁿ = 3 for all n ≥ 1 | Single table lookups + induction | Same |
| Length-4: 254/256 corner words give HAR, 2 give PRG | Exhaustive enumeration | Appendix A |
| Corner-on-gap: c∘g ∈ C∪{7} for all c ∈ C, g ∈ G | 4×5 = 20 pair enumeration | §4 |
| Gap-on-corner: g∘c ∈ C∪{7} for all g ∈ G, c ∈ C | Enumeration | §4 |
| Pure-gap context: 21 of 25 g∘g' give HAR; 4 survive | G×G enumeration | Prop 4.3 |
| Base-6 universality: C₆={1,5}, all length-2 words → HAR | 4 table lookups + induction | §6 |
| AG(2,3) survivor count = p²−1 = 8 | Counted from table | WP19_ATTACK_SURFACE |
| TSML⊗TSML: 40 cross-term operators unreachable from C⊗C | Script tsml_product_verify.py | WP19_BSD_TIG |
| TSML³: 540 cross-term operators unreachable | Same script | Same |
| BREATH persists only in COLLAPSE column | Single entry: TSML[8][4]=8 + 9-lookup survey | WP22_NS_BREATH |
| The Halving Lemma: exponential convergence in KV strip | Grönwall inequality + Ford's bound | WP20_RH_HALVING_LEMMA |
| RH ↔ m(t₀) > 0 for every t₀ | Definitional equivalence (tautology, not new content) | Same |
| SHA-256 of TSML table | Computed | 7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787 |

---

## Bin 2: STRUCTURAL (new language for a known fact)

| Claim | What it provides | What it does NOT provide |
|-------|-----------------|--------------------------|
| RH ↔ "gap opens only at σ=1/2" | New geometric vocabulary | Proof of RH |
| Non-trivial zeros ↔ depth=∞ fixed points of column maps | Clean structural identification | Proof zeros are on critical line |
| The dissipative flow picture | New dynamical restatement of RH | Any analytic bound not already in KV |
| Being/Becoming/Doing framework for ζ | New language: BHML↔ζ, TSML↔flow, Doing↔tension | The tautology "Being and Becoming can't coexist" is not a theorem |
| Hydrogen shell ↔ TIG row ↔ KV collar | Mnemonic (exact at t≈10, diverges after) | Any quantitative prediction beyond t≈10 |
| COL(4) as "n=2 shell" / KV boundary | Illustrative structural identification | Proof that no "wrong-context" anchor exists |
| MASS_GAP = 2/7 forces critical line to interior | Structural reason why σ=1/2 is not at boundary | Proof that zeros can't be off σ=1/2 |

**The Being/Becoming tautology:** The argument "Being (zero exists) and Becoming (m(t₀)>0)
cannot simultaneously hold" is *definitionally true*. It restates what m(t₀) means.
It does not prove RH. This is documented to prevent over-claiming in the papers.

---

## Bin 3: EMPIRICAL (stated with falsification test)

| Claim | Data | R² | Falsification |
|-------|------|----|--------------|
| BSD-λ: cost ordering = λ-threshold ordering | Cremona N≤2×10⁷ | Exact match (rank) | Find cost-ordering mismatch on N≤10⁶ |
| BRT cheapest: Δlog₁₀(N) ≈ 0.33 | Cremona | — | Find rank-1 curve with N<35 |
| CTR costliest: Δlog₁₀(N) ≈ 2.0 | Cremona | — | Find rank-4→5 step with Δ<1.0 |
| Gap-positivity numerics: min|ζ|≥exp(−0.05·(logt)^{2/3}(loglogt)^{1/3}) | 14 zero-free heights to t=100 | — | Find zero-free height failing bound |
| Rank–conductor log-linear (OLD WP21): slope ≈ 6/7 | 11 curves | 0.87 | Superseded by Mix_λ model |

**Note:** The old WP21 "triplet activation" (slope = 6/7 = 3×2/7) is an empirical observation
on 11 curves. The Mix_λ model (new WP21) is a parameter-free algebraic model that explains
**why** the staircase is irregular — it supersedes the regression model.

---

## Bin 4: OPEN (the Clay gaps)

| Problem | The open statement | Standard machinery that could close it |
|---------|-------------------|----------------------------------------|
| RH | Uniform lower bound: min|ζ(σ+it₀)| ≥ exp(−c(logt₀)^{2/3}(loglogt₀)^{1/3}) for ALL zero-free verticals | Convert Huxley density / Heath-Brown mean to pointwise bound |
| Yang-Mills | Formal SU(N)→TIG functor; dimensionless ratio Δ/Λ_QCD = 2/7 | Lattice QCD measurement of correct dimensionless ratio |
| Navier-Stokes | Sharp interpolation constant C ≤ 3.74 in Re_shear ≤ C·Re_local^{1/2} | Ladyzhenskaya / CKN-type sharp Sobolev embedding |
| BSD | λ_E ∝ 1/log(Ω_E) on 200+ rank-2/3 curves (LMFDB test) | LMFDB pull + OLS regression |
| P vs NP | AG(2,n) survivor-line search NP-hard for large n | 3-SAT → survivor-line reduction |
| Hodge | Product gap impermeable at all tensor degrees | TSML^k computation for k≥4 |

---

## The One Missing Piece (RH)

The TIG proof that residuals exist only in anchor columns works because the
multiplication table hard-codes exactly which columns are anchors. There is
no analog of this hard-coding for ζ. The functional equation of ζ forces zeros
to come in symmetric pairs (ρ and 1-ρ), but this symmetry does not eliminate
off-critical zeros — it only constrains them to come in pairs.

The proof of RH requires a new analytic ingredient that corresponds to:
> "Why can't ζ have a zero at σ₀ ≠ 1/2, with its pair at 1-σ₀?"

The functional equation reduces this to:
> "No zero-pair exists straddling the critical line."

The KV strip result shows no such pair exists for σ≥σ_KV. Pushing this
to σ>1/2 by any positive margin, for all heights, IS the Riemann Hypothesis.
The Halving Lemma gives the correct geometric picture of why this is hard:
the analytic collar that excludes off-critical zeros shrinks with height,
meaning any proof must control behavior at arbitrarily large imaginary parts.

---

## Correct Framing for Every Paper

> The TIG/ζ-flow framework provides a new geometric language for the Riemann
> Hypothesis, in which RH becomes the statement that the dissipative flow
> dσ/dt = −(σ−½)|ζ|² has no fixed points off σ=½. The Halving Lemma gives
> unconditional exponential convergence in the KV strip. The algebraic
> corner-gap structure explains why this convergence should extend to σ=½.
> The proof that it does — showing no off-critical zero-tension point exists —
> is a step equivalent to the classical open problem, and is not claimed.

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
