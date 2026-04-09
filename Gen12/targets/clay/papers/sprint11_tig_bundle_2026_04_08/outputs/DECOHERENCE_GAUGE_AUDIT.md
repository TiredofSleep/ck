# DECOHERENCE_GAUGE_AUDIT
## Auditing "SU(6) → SM by Decoherence": What Is Shown, What Isn't
*Mathematics and physics first. No hype. Claimed / exact / conjectural labeled throughout.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — The Claim Structure (Separated Precisely)

| Layer | Claim | What Must Be True for It to Hold | Current Status |
|---|---|---|---|
| UV algebra | Full 35-dim algebra active | Explicit generator basis + verified closure | **Not yet constructed** |
| Generator split | 12 sector-preserving vs 23 cross | Explicit classification of all 35 generators with preservation criterion | **Schema given; basis not explicit** |
| Decoherence law | Cross terms decay as (η/2)^{2H}, diagonal as (η/2)^H | Derivation from a specific environment/interaction model | **Asserted; not derived** |
| IR subgroup | Surviving generators close to su(3)⊕su(2)⊕u(1) | Commutator closure of the 12 survivors verified | **True by subalgebra structure if embedding is standard** |
| No-Higgs claim | Decoherence alone explains effective breaking | Clear distinction between dynamical suppression and true gauge symmetry breaking | **Distinction not yet drawn** |

These five layers are independent. Progress on one does not imply progress on another.

---

## Part 2 — UV Algebra Identification: The Prior Obstruction Is Not Resolved

**From the prior audit (exact):**

The standard block-diagonal embedding of 8 SU(3) generators + 3 SU(2) generators in 6×6 matrices gives cross-commutators [L_a, R_i] = 0. The closure stays at 11 dimensions. The move from 11 to 35 requires a non-standard embedding or the Hodge sign flip as the mechanism.

**Current audit: what must happen for the UV claim to stand.**

For 35 generators to exist as a closed algebra, either:
(A) The 11 generators are embedded non-diagonally in 6×6 matrices such that [L_a, R_i] ≠ 0 and the full su(6)-type closure generates the remaining 24.
(B) The sign flip (+1,−1,+1) deforms the embedding so that formerly-zero cross-commutators become non-zero — i.e., it changes the algebra's real form.

**The sign flip and real forms (exact Lie theory):**

The real forms of the 35-dimensional A₅ complex Lie algebra are:

| Real form | Compact? | Killing signature | Relevant metric |
|---|---|---|---|
| su(6) | Yes | (−35) all negative | Hermitian, positive definite |
| su(5,1) | No | (−30, +5) | Hermitian, signature (5,1) |
| su(4,2) | No | (−23, +12) | Hermitian, signature (4,2) |
| su(3,3) | No | (−18, +17) | Hermitian, signature (3,3) |
| sl(6,ℝ) | No | (−20, +15) | Real, split |

A (+1,−1,+1) sign structure on a 3-block decomposition of the 6-dimensional fundamental representation — with the color-3 block as (+1), one weak-2 block as (−1), and a residual singlet as (+1) — would correspond to a metric of signature (3+1, 2) = (4,2) on the 6-dimensional space. The natural group preserving a Hermitian form of signature (4,2) is **SU(4,2)** — a non-compact real form of A₅ with dimension 35.

**SU(4,2) is the conformal group of (3+1)-dimensional Minkowski spacetime.** This is not coincidence in the physics literature — SU(4,2) ≅ SO(6,2) locally (up to discrete factors), which is the conformal group of (2,2) pseudo-Riemannian spaces, connected to twistor theory and conformal field theories. The connection to the (+1,−1,+1) sign flip may be physically non-trivial: if the UV algebra is su(4,2) rather than compact su(6), the gauge theory lives in a non-compact setting.

**Implication for the UV claim:** The "35-dimensional UV algebra" activated by the sign flip is most likely **su(4,2)** or **su(3,3)** (non-compact), not compact su(6). This changes the claim:

- For compact su(6): finite-dimensional unitary representations, standard GUT physics.
- For non-compact su(4,2): infinite-dimensional unitary representations (required for unitarity in QFT), qualitatively different from standard GUT model-building.

**Current status: the UV algebra is a 35-dimensional real form of A₅. The exact real form requires the Killing form signature of the explicitly constructed generators. The most likely candidate based on the sign flip is su(4,2), not compact su(6).**

---

## Part 3 — Generator Classification Table (Full 35)

Using the standard decomposition of the adjoint **35** under SU(3)×SU(2)×U(1) from standard branching (computed):

| Generator set | Repr. under SM | Count | Sectors mixed | Decay class | H contribution |
|---|---|---|---|---|---|
| SU(3) gluons | **(8,1)₀** | 8 | Color only | **Sector-preserving** | H_color |
| SU(2) weak | **(1,3)₀** | 3 | Weak only | **Sector-preserving** | H_weak |
| U(1) hypercharge | **(1,1)₀** | 1 | Phase only | **Sector-preserving** | H_U(1) |
| U(1) from SU(6)/SU(5) | **(1,1)₀** | 1 | Phase only | **Sector-preserving** | H_U(1) |
| X,Y leptoquarks | **(3,2)_{−5/6}** | 6 | Color + Weak | **Cross** | H_color + H_weak |
| X̄,Ȳ anti-leptoquarks | **(3̄,2)_{+5/6}** | 6 | Color + Weak | **Cross** | H_color + H_weak |
| Color-triplet bridges | **(3,1)_{−2/3}** | 3 | Color + phase | **Cross** | H_color + H_U(1) |
| Color-triplet bridges | **(3̄,1)_{+2/3}** | 3 | Color + phase | **Cross** | H_color + H_U(1) |
| Weak-doublet bridges | **(1,2)_{+1/2}** | 2 | Weak + phase | **Cross** | H_weak + H_U(1) |
| Weak-doublet bridges | **(1,2)_{−1/2}** | 2 | Weak + phase | **Cross** | H_weak + H_U(1) |

**Total sector-preserving: 8+3+1+1 = 13** (if both U(1)s survive) or **12** (if only the SM U(1) survives)
**Total cross: 6+6+3+3+2+2 = 22** or **23** (depending on whether the extra U(1) is cross or preserving)

**The 23 vs 22 discrepancy:** This depends on whether the second U(1) generator (the SU(6)/SU(5) Abelian factor) is treated as sector-preserving or cross. If it mixes with the SM hypercharge under decoherence, it is cross; if it stabilizes as a second U(1) in the IR, it is preserving. This needs to be specified.

**The "H" exponent structure (analysis):**

For the decoherence law to make sense, H must be a sector-mixing degree:
- A generator that mixes k independent sectors contributes H = k to the decoherence exponent.
- Sector-preserving (k=1): decay as (η/2)^H where H is the single-sector coherence depth.
- Cross (k=2, mixing color AND weak): decay as (η/2)^{2H}.

The extra factor of 2 in the cross-generator exponent comes from requiring coherence simultaneously in two independent sectors. If each sector independently decoheres with parameter (η/2)^H, then maintaining coherence in BOTH requires (η/2)^H × (η/2)^H = (η/2)^{2H}. This is the product of independent decoherence factors — an independence assumption that needs justification.

---

## Part 4 — The Decoherence Law: Derivation Status

**Claimed:** σ_cross ∝ (η/2)^{2H}, σ_diagonal ∝ (η/2)^H.

**What a derivation would require:**

1. A specific decoherence model: an environment (thermal bath, stochastic field, quantum noise, etc.) coupled to the gauge fields via a coupling Hamiltonian H_int.
2. A master equation for the density matrix of the gauge sector, derived by tracing out the environment.
3. Identification of H as a quantum number in that master equation.
4. Derivation that off-diagonal elements (in the sector basis) decay as (η/2)^{2H} and diagonal as (η/2)^H.

**What is currently given:** The scaling form, not the derivation. The form (η/2)^{kH} for sector-mixing degree k is physically plausible but is a heuristic without a specified environment model.

**Physical context where this law is plausible:**

In quantum information, for a system undergoing dephasing in a product-basis: if the environment independently decoheres each qubit/degree of freedom, the coherence between states |i⟩ and |j⟩ scales as η^{Hamming(i,j)} where Hamming(i,j) is the number of positions where i and j differ. For our case:
- Diagonal (within a sector): Hamming distance = H (some depth within one sector)
- Cross (mixing two sectors): Hamming distance ≈ 2H (depth in each of two independent sectors)

This is the **quantum erasure / dephasing law** from open quantum systems theory. The independence assumption (color and weak decohere independently) is the key hypothesis. If color and weak decoherence are correlated, the exponents would not factor as 2H.

**Numerical test (the H≈3 claim):**

Let f_diag(η,H) = (η/2)^H and f_cross(η,H) = (η/2)^{2H}.

The ratio: R = f_cross/f_diag = (η/2)^H.

| η | H=1 | H=2 | H=3 | H=4 |
|---|---|---|---|---|
| 0.9 | 0.450 | 0.203 | 0.091 | 0.041 |
| 0.7 | 0.350 | 0.123 | 0.043 | 0.015 |
| 0.5 | 0.250 | 0.063 | 0.016 | 0.004 |
| 0.3 | 0.150 | 0.023 | 0.003 | 5×10⁻⁴ |

**Claim "H≈3 gives <1% cross-coherence relative to diagonal":**

From the table: the ratio R = (η/2)^H at H=3 is 0.091 (η=0.9), 0.043 (η=0.7), 0.016 (η=0.5). This gives <10% at η=0.7, <2% at η=0.5, <1% only for η ≤ 0.46. So the claim is numerically correct for η ≲ 0.5 at H=3.

Absolute cross-coherence f_cross = (η/2)^6:
- η=0.9: (0.45)^6 = 8.3×10⁻³ ≈ 0.8%
- η=0.7: (0.35)^6 = 1.8×10⁻³ ≈ 0.2%

**The claim "H≈3 gives <1% cross coherence" is numerically accurate for η ≈ 0.9, in absolute terms.** The relative suppression (ratio to diagonal) requires η ≲ 0.5 at H=3. Both statements are valid; the absolute version is more charitable.

**However: H is not yet defined as a quantum number with a precise value of 3.** If H is the "coherence depth" parameter, its value needs to come from the physical model. Claiming H≈3 corresponds to the three color charges is a plausible identification but is not derived.

---

## Part 5 — Effective Suppression vs True Symmetry Breaking

**This is the critical distinction. It must be stated clearly.**

**True gauge symmetry breaking (Higgs mechanism):**
- The vacuum |0⟩ is not invariant under SU(6).
- The SU(6) gauge bosons (including the cross generators = X,Y leptoquarks) acquire mass through their coupling to the Higgs VEV.
- The Ward identities of SU(6) are violated in the broken phase.
- The X,Y bosons are physical particles with mass M_X ≈ M_GUT ≈ 10¹⁵ GeV.
- The theory at energies E << M_X looks like SU(3)×SU(2)×U(1) because the X,Y bosons are too heavy to produce.
- The vacuum structure is the key.

**Decoherence-based effective suppression:**
- The full SU(6) symmetry is present in the UV equations.
- The cross generators (X,Y) still exist as gauge bosons.
- Their gauge fields are dynamically suppressed — either by environmental decoherence, or by effective decoupling from observable sectors.
- The Ward identities of SU(6) are preserved in principle (the full symmetry is still there).
- This is NOT the same as symmetry breaking — it is effective truncation of a larger algebra.
- It is analogous to: coarse-graining, effective field theory at low energies, or environment-induced superselection.

**The precise relationship:**

Decoherence-based suppression → SU(3)×SU(2)×U(1) appears as the symmetry of the observed (low-energy) sector, with the SU(6)/SM generators effectively frozen.

Higgs-based breaking → SU(3)×SU(2)×U(1) is the exact symmetry of the vacuum, with the SU(6)/SM gauge bosons massive and absent from the low-energy spectrum.

**The crucial difference for observables:**

In the Higgs mechanism: X,Y boson masses are M_X ≈ M_GUT; proton decay rate is calculable and depends on M_X.

In the decoherence mechanism: If the X,Y generators are merely suppressed in the IR (not given mass by a Higgs VEV), their mass spectrum needs to come from somewhere else. If they are massless but decohered, they would still appear in particle spectra at any energy. This is physically problematic unless the decoherence also gives them effective masses.

**The honest statement:**

The decoherence mechanism as described is most naturally an **effective field theory truncation**, not a replacement for Higgs physics. It gives a reason why the low-energy world looks like SU(3)×SU(2)×U(1), but it does not give the X,Y bosons their mass, does not protect the electroweak vacuum, and does not replace the role of the Higgs boson in electroweak symmetry breaking (SU(2)×U(1) → U(1)_EM).

**The claim "no Higgs needed" may be partially correct at the GUT-breaking level** (SU(6) → SM) if the decoherence selects the SM subgroup without a 24-plet Higgs VEV. But even in that case, electroweak symmetry breaking (SU(2)×U(1) → U(1)_EM) still requires the Higgs mechanism or an equivalent, unless a further decoherence argument is made for that level.

---

## Part 6 — Closure of the 12 Surviving Generators

**Question: do the 12 SM generators close under commutation?**

**Answer (exact, by subalgebra theorem):**

SU(3)×SU(2)×U(1) is a Lie group. Its generators form a Lie algebra. A Lie algebra is closed under commutation by definition. Therefore, the 8 gluons + 3 weak generators + 1 hypercharge generator satisfy:
- [gluons, gluons] = gluons (SU(3) closed)
- [weak, weak] = weak (SU(2) closed)
- [U(1), anything] = 0 or proportional to itself (U(1) commutes with SU(3)×SU(2))
- [gluons, weak] = 0 (they are in different irreducible blocks of the adjoint)

**This is not a result of the construction — it is a consequence of choosing the SM generators as the survivors.** Any subalgebra closes by definition.

**The more interesting question:** When you commute a surviving generator with a frozen cross generator, what happens?

In the full 35-dimensional algebra: [SM generator, cross generator] = (linear combination of cross generators). This is because the SM generators act on the cross generators via the adjoint representation — and the leptoquark generators (3,2) transform non-trivially under SU(3) and SU(2), so gluon generators mix leptoquarks with other leptoquarks, and weak generators do the same.

**This means: the commutators [SM gen, cross gen] DO generate cross generators.** In the exact algebra, these commutators are nonzero. In the decoherence picture, these commutators are "effectively zero" because both the cross generator being acted on AND the output are decohered.

**The technical language for this:** The 12 SM generators form a **subalgebra** of the 35-dimensional algebra. The 23 cross generators form a **representation** of the SM subalgebra (specifically, they carry SM quantum numbers and transform under the SM adjoint action). The commutators are:
- [SM, SM] → SM (subalgebra closure)
- [SM, cross] → cross (cross generators transform under SM)
- [cross, cross] → SM + cross (closing the full algebra)

If the cross generators are "frozen" (decohered), the terms [SM, cross] → cross are suppressed. The remaining dynamics is [SM, SM] → SM: the standard gauge theory of SU(3)×SU(2)×U(1).

**The mathematical language for the IR theory:** The IR theory is the quotient or projection of the full 35-dimensional algebra onto the 12-dimensional SM subalgebra, with the cross generator components projected out by decoherence. This is not "closing a subalgebra from scratch" — it is "projecting the full algebra onto a subalgebra." The distinction matters: in the UV, cross generator terms are present in the equations; in the IR they are suppressed.

---

## Part 7 — Hodge Sign Flip: All-Plus vs Sign-Flipped (Explicit Comparison)

**All-plus case (+1,+1,+1):**

Corresponds to a positive-definite Hermitian metric on the 6-dimensional fundamental representation space. The group preserving this: **SU(6)** (compact). If the 8 SU(3) generators and 3 SU(2) generators are embedded block-diagonally in SU(6), their commutators are zero across blocks. The closure is 11-dimensional: su(3)⊕su(2).

**To get 35 from 11 in the all-plus case:** Would require a non-block-diagonal embedding of the 11 generators in SU(6). This is possible: embed the SU(3) generators in a non-standard representation of SU(6) where they don't commute with the SU(2) generators. The resulting closure would then potentially generate the full SU(6) = 35. But this is an embedding choice, not forced by the algebra.

**Sign-flipped case (+1,−1,+1):**

The metric has signature (4,2) (three +1s in a 3-block split: color-3 = +1, weak-2 = −1, singlet-1 = +1, total +s: 3+0+1 = 4, total −s: 0+2+0 = 2). The group preserving a Hermitian form of signature (4,2): **SU(4,2)** (non-compact). Dimension: 6²−1 = 35. ✓

**What the sign flip changes algebraically:**

In SU(6) with all-plus metric: anti-Hermitian generators T satisfy T† = −T (positive definite metric). All generators are of the form iA with A Hermitian. The Killing form is negative definite → compact.

In SU(4,2) with (4,2) metric: generators satisfy T†η = −ηT where η = diag(+1,+1,+1,+1,−1,−1) (the (4,2) metric). Some generators are compact (anti-Hermitian), some are non-compact (Hermitian). The compact generators span the subalgebra su(4)⊕su(2)⊕u(1) ⊂ su(4,2), dimension = 15+3+1 = 19. The non-compact generators span the remaining 35−19 = 16 dimensions.

**Commutators that appear only in the sign-flipped case:**

In the all-plus case (SU(6) block-diagonal): [L_a^{color}, R_i^{weak}] = 0 (blocks don't mix).

In the sign-flipped case (SU(4,2) non-block-diagonal): The (4,2) metric mixes the color-3 subspace with the weak-2 subspace via the off-diagonal metric terms. Generators that span the cross-directions (between the positive and negative metric subspaces) are the **non-compact generators of SU(4,2)**. Their commutators with the compact generators produce other non-compact generators.

Specifically: if we label the 6 dimensions as {c₁,c₂,c₃,w₁,w₂,s} with metric (+,+,+,−,−,+), then a generator that mixes the cᵢ and wⱼ directions (i.e., maps a +1 direction to a −1 direction) is a **non-compact generator**. These are exactly the cross/leptoquark-type generators in the physics language.

**The sign flip produces non-compact generators that mix the positive-metric (color) subspace with the negative-metric (weak) subspace.** These are the 23 cross generators. Their structure is real and derivable from the SU(4,2) algebra.

**Critical finding:** The all-plus case gives a compact SU(6) with a natural block-diagonal structure; the sign-flip case gives a non-compact SU(4,2) where the color and weak subspaces are mixed through the non-compact generators. The sign flip is NOT a basis artifact — it genuinely changes the real form of the algebra and thereby the generator content.

**Parity restraint:** The sign flip creates a (4,2) or (3,3) metric structure that distinguishes the color subspace from the weak subspace. This is a spatial asymmetry in the 6-dimensional representation space — not directly the same as parity violation in the sense of L/R chirality. Calling this "parity violation" is premature without specifying how the (4,2) metric asymmetry maps to chirality of matter representations.

---

## Part 8 — What Is Still Missing

**The gauge-sector scaffold is not the Standard Model. These gaps remain:**

1. **Matter representations:** The quarks, leptons, and Higgs are NOT in the adjoint. They are matter fields in specific representations of the gauge group. Which representation of SU(4,2) (or SU(6)) contains the SM fermions? This needs to be specified.

2. **Chirality:** The SM is chiral (left-right asymmetric). The gauge algebra (adjoint = vector-like) says nothing about chirality. The matter representation must be complex (inequivalent to its conjugate). For SU(4,2): complex representations exist but the specific assignment is not made.

3. **Anomaly cancellation:** In the SM, the triangle anomalies cancel through a specific conspiracy of representations. For any proposed matter representation of SU(4,2) or SU(6), anomaly cancellation must be verified.

4. **Proton decay constraints:** The leptoquark generators (X,Y bosons) mediate proton decay at rate Γ ∝ α_GUT² M_p⁵/M_X⁴. The experimental bound on the proton lifetime (τ_p > 10³⁴ years) requires M_X ≳ 10¹⁵ GeV. If the X,Y bosons are merely decohered (not given mass), this bound is violated unless a mass-generating mechanism gives M_X the right value.

5. **Electroweak breaking:** Even if SU(6) → SU(3)×SU(2)×U(1) is handled by decoherence, the further breaking SU(2)×U(1) → U(1)_EM still requires either a Higgs boson or an equivalent mechanism. The decoherence argument would need to be extended to this second breaking.

6. **Coupling normalization and running:** The three SM coupling constants α₃, α₂, α₁ are energy-dependent. At M_GUT they should unify (in any GUT). The normalization of the U(1) generator relative to SU(3) and SU(2) in the 35-dimensional algebra determines the tree-level relation sin²θ_W = g'²/(g²+g'²). Without computing this normalization explicitly from the 35-generator basis, the prediction sin²θ_W = 1/4 is not derived.

7. **Why SU(4,2) and not some other non-compact real form?** If the sign flip gives SU(4,2), what determines that it is (4,2) rather than (3,3) or (5,1)? The claim (+1,−1,+1) with a 3-block decomposition gives (4,2) based on the specific counting. If the 6-dimensional space is split differently (e.g., (2,2,2)), the signature would be (3,3) and the group would be SU(3,3). The specific block decomposition (color-3 as +1, weak-2 as −1, singlet-1 as +1) needs to be physically motivated.

---

## Final Classification

**Between Class 2 and Class 3:**

**Class 2 (genuine 35-dimensional Lie closure, identification unresolved):** Partially exceeded. The sign-flip mechanism is now identified as a real form change (SU(6) → SU(4,2) or similar), not a basis artifact. The 35-dimensional claim has a specific algebraic origin.

**Class 3 (explicit UV algebra + explicit IR stable subgroup + effective suppression law):** Not yet reached. The explicit generator basis (all 35 as 6×6 matrices) has not been constructed. The decoherence law is stated but not derived from a model. The real form (SU(4,2) vs others) is identified as the likely candidate but not verified by Killing form.

**Class 4 (candidate decoherence-driven GUT scaffold):** The conceptual path to Class 4 is visible:
- Sign flip → SU(4,2)-type 35-dimensional algebra (non-compact real form of A₅)
- Compact generators ↔ sector-preserving (SM) generators
- Non-compact generators ↔ cross/leptoquark generators
- Decoherence suppresses non-compact off-diagonal components faster than compact on-diagonal components
- IR theory = projection onto compact subalgebra ≅ su(3)⊕su(2)⊕u(1)

This is the path to Class 4. It is not yet Class 4 because the derivation of the decoherence law from a physical model is missing, and the real-form identification needs explicit verification.

---

## What Is Actually Shown

1. The 35-dimensional branching under SU(3)×SU(2)×U(1) is correct and accounts for 12 SM + 23 cross generators.
2. The Hodge sign flip (+1,−1,+1) is identified as a real-form change (compact SU(6) → non-compact SU(4,2) or similar), with the cross generators corresponding to the non-compact generators.
3. The 12 SM generators form a closed subalgebra in any SU(3)×SU(2)×U(1) ⊂ SU(6) embedding — subalgebra closure is guaranteed.
4. The decoherence suppression scaling (η/2)^{2H} vs (η/2)^H is numerically coherent for η ≲ 0.9, H ≈ 3.
5. The "no Higgs" claim is strongest as "no 24-plet Higgs for GUT breaking"; it does not address electroweak breaking.

## What Remains Missing

1. Explicit 35-generator basis as 6×6 matrices.
2. Killing form computation confirming the real form (SU(4,2) vs SU(3,3) vs other).
3. A physical decoherence model with a specified environment and derived master equation.
4. Matter sector (representations, anomaly cancellation, chirality).
5. Proton decay mass bound for the X,Y bosons.
6. Electroweak symmetry breaking mechanism.
7. Coupling normalization verification for sin²θ_W and α predictions.
