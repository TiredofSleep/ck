# ML SYMMETRY AND NON-IDENTIFIABILITY MEMO
## How Type I and Type II Failures Appear in Machine Learning
*Proved statements vs. structural analogies labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Overview

Two distinct structural failure types appear in machine learning and parameter inference:

- **Type I (Injectivity failure):** The measurement family is valid but insufficient. Adding orthogonal measurements resolves the ambiguity. This appears in ML as redundant features, repeated assays in the same experimental regime, and duplicate sensor readings.

- **Type II (Missing invariant):** The observation map is valid but the allowed model class has a symmetry group that maps multiple parameter settings to the same output. No observation in the current family breaks the symmetry. This appears in ML as permutation symmetry in neural networks, scaling symmetry in matrix factorization, and latent-variable non-identifiability.

These are structurally distinct. Type I is resolved by adding new measurements from a different direction. Type II is resolved by adding a constraint (gauge-fixing, normalization, ordering, anchor variable) external to the observation family.

---

## C1 — Symmetry and Non-Identifiability (Type II)

### Setup

A parametric model is a map:
F: Θ × 𝒳 → 𝒴,   F(θ, x) = predicted output for parameter θ and input x.

**The observation map** is: f_obs(θ) = {F(θ, x) : x ∈ training data} — the set of predictions over training inputs.

**Ambiguity set:** U(f_obs) = { {θ, θ'} : f_obs(θ) = f_obs(θ') for all x } — parameter pairs that produce identical predictions everywhere.

A model has a symmetry group G if there is a group action G × Θ → Θ, θ ↦ g·θ, such that F(g·θ, x) = F(θ, x) for all x, for all g ∈ G.

Under symmetry: U(f_obs) ⊇ { {θ, g·θ} : g ∈ G \ {id} }. The observation map cannot distinguish θ from any group-equivalent parameter.

**This is Type II:** f_obs is a valid map on a valid domain. The ambiguity set is non-empty. And no observation of the form F(θ, x) can cut the ambiguity — because by definition, F(g·θ, x) = F(θ, x) for all x. No additional observation in the model-output family can have positive score for distinguishing θ from g·θ.

---

### Example C1-A: Neural Network Permutation Symmetry

**Model:**
f(x; W₁, W₂) = W₂ · σ(W₁ · x)

where W₁ ∈ ℝ^{H×d}, W₂ ∈ ℝ^{n×H}, σ is applied elementwise, H = number of hidden units.

**Symmetry group:** For any permutation matrix P ∈ S_H (the symmetric group on H elements, viewed as H×H permutation matrices):

W₂ · σ(W₁ · x) = (W₂P) · σ(Pᵀ W₁ · x) = (W₂P) · σ((PW₁) · x)   (since σ is applied elementwise and permutation commutes with elementwise functions)

So (W₁, W₂) and (PW₁, W₂P) produce identical outputs for all x.

**Ambiguity set (proved):**
U(f_obs) ⊇ { {(W₁,W₂), (PW₁,W₂P)} : P ∈ S_H, P ≠ I }

The H! permutations of hidden units produce H! parameter settings giving identical function values.

**Type II diagnosis:** The observation map f_obs = {F(θ,x) : x ∈ data} cannot distinguish the H! permuted versions of θ. No training data point can have positive score for this ambiguity, because the data-generating function is symmetric.

**UOP fix (structural analogy — not the only fix):**

Add a second map f_gauge: θ ↦ canonical_ordering(θ) that selects a unique representative from each symmetry orbit. For example:

f_lex(W₁, W₂) = "sort hidden units by lexicographic order of their rows in W₁"

This gauge-fixing map has positive score: it distinguishes (W₁,W₂) from (PW₁,W₂P) by the ordering of rows. Combining f_obs and f_lex makes the joint map injective on the ordered-representative subspace.

**In ML practice:** Gauge-fixing for permutation symmetry is typically handled by:
1. Using architectures that break permutation symmetry by construction (e.g., specific initialization, tied weights).
2. Canonicalization post-hoc (sorting units by some criterion).
3. Symmetry-aware optimization (taking gradients modulo symmetry orbits).

**What is proved:** The permutation symmetry is an exact symmetry of the neural net function class (proved above). The ambiguity set contains H! parameter pairs for each function. Gauge-fixing reduces this to 1 per orbit. These are facts about the function class, not approximations.

**What is structural analogy:** The UOP framing (add a second map f_gauge with positive score) is the structural vocabulary. The specific gauge-fixing strategies in ML practice are engineering choices, not direct applications of the UOP score formula.

---

### Example C1-B: Matrix Factorization Scaling Symmetry

**Model:** Approximate a target matrix M̂ ∈ ℝ^{n×m} by a low-rank factorization:

M(U,V) = UV^T,   where U ∈ ℝ^{n×k}, V ∈ ℝ^{m×k}

**Symmetry group:** For any invertible diagonal matrix D = diag(λ₁,...,λₖ) ∈ GL(k, diagonal):

(UD)(VD)^T = UD · D^T V^T = U · (DD^T) · V^T

Wait: (UD)(VD)^T = UD(D^T V^T) = U · (D D^T) · V^T. For diagonal D: D D^T = D² (a diagonal matrix with entries λᵢ²). This doesn't give UV^T unless D = I.

Let me correct: the scaling symmetry is:

(U D)(V D⁻¹)^T = U D (D⁻¹)^T V^T = U D D^{-T} V^T = U V^T = M   [for diagonal D: D^{-T} = D⁻¹]

So (U,V) and (UD, VD⁻¹) give the same product M.

**Formal statement:** For any invertible diagonal D: M(UD, VD⁻¹) = (UD)(VD⁻¹)^T = U(D · D⁻T) V^T = U · I · V^T = UV^T = M(U,V).

*Proved:* The diagonal scaling group D = {diag(λ₁,...,λₖ): λᵢ ≠ 0} is an exact symmetry of the factorization M = UV^T. Two parameter pairs (U,V) and (UD, VD⁻¹) always produce identical M.

**Ambiguity set (proved):**
U(f_obs) ⊇ { {(U,V), (UD, VD⁻¹)} : D ∈ diagonal invertible group }

For k factors: a continuous (k-parameter) family of equivalent parameter settings per matrix M.

**Type II diagnosis:** The observation map f_M: (U,V) ↦ UV^T cannot distinguish (U,V) from (UD, VD⁻¹). No low-rank matrix M can separate them (they give the same M by construction). No observation in the "low-rank reconstruction" family can kill the ambiguity.

**UOP fix:** Add a normalization map:
f_norm(U,V) = (normalized_U, normalized_V) where ‖uᵢ‖₂ = 1 for all columns uᵢ of U.

This selects D = diag(‖u₁‖,‖u₂‖,...,‖uₖ‖) canonically. The joint map (f_M, f_norm) is injective (up to sign and permutation of columns).

**ML consequence:** Parameter recovery in matrix factorization (as in recommender systems, PCA, NMF) requires additional constraints beyond just fitting M. Without normalization (or sparsity, or orthogonality constraints), the factorization is under-constrained even with perfect data. This is a known identifiability issue in the MF literature.

---

### Example C1-C: Latent Variable Models

*Structural analogy section — more abbreviated.*

In a Gaussian mixture model: p(x) = Σᵢ πᵢ 𝒩(x; μᵢ, Σᵢ). Parameters: mixing weights πᵢ, means μᵢ, covariances Σᵢ.

The observation map f: (π,μ,Σ) ↦ density p(x) is invariant under permutation of mixture components:

p(x; π, μ, Σ) = p(x; P·π, P·μ, P·Σ) for any permutation P.

This is the same permutation symmetry as neural networks (Type II, missing invariant). Add a component-ordering constraint to break it.

---

## C2 — Redundant Measurement (Type I)

### Setup

Consider a parameter θ ∈ ℝᵈ to be estimated from measurements y₁ = f₁(θ) + ε₁, y₂ = f₂(θ) + ε₂ with noise. The residual ambiguity R({f₁}) is the set of parameter pairs θ ≠ θ' with f₁(θ) = f₁(θ').

A second measurement f₂ is valuable iff score(f₂ | {f₁}) > 0 — it resolves at least one pair in R({f₁}).

**Type I:** f₁ is valid, R({f₁}) ≠ ∅, and the question is whether f₂ reduces R. Score = 0 iff f₂ is parallel to f₁ (structurally redundant).

---

### Example C2-A: Nearly Duplicate Feature

**Setting:** Linear regression. Response y = β₁x₁ + β₂x₂ + ε. True parameters θ = (β₁, β₂).

**Current features:** x₁ only. Map f₁(β₁,β₂) = β₁·x₁. Ambiguity: U(f₁) = all pairs {(β₁,β₂), (β₁,β₂')} — β₂ is completely invisible.

**Candidate feature x₂:** Two options:
- x₂^A = x₁ + noise (near-duplicate of x₁, σ_noise = 0.05).
- x₂^B = x₃ (a genuinely new feature, orthogonal to x₁ in the data matrix).

**UOP score:**

score(x₂^A | {x₁}):
Map f_{x₂^A}(β₁,β₂) = β₁·x₂^A + β₂·x₂^A = (β₁+β₂)·(x₁+noise). Since x₂^A ≈ x₁: the new measurement nearly equals β₁·x₁ again. The ambiguity about β₂ (which direction is β₂'s contribution to x₂^A?) is minimal. Technically: U(f_{x₂^A}) ≈ U(f₁) for x₂^A ≈ x₁. score ≈ 0.

score(x₂^B | {x₁}):
Map f_{x₂^B}(β₁,β₂) = β₂·x₃. This directly observes β₂ (if x₃ contains β₂ signal). U(f_{x₂^B}) = pairs with same β₂, which is orthogonal to U(f₁) (pairs with same β₁). score = full residual of R({f₁}).

**FIM comparison:**

FIM contribution of x₂^A: (1/σ_noise²) × x₂^A · (x₂^A)ᵀ ≈ (1/0.0025) × x₁ · x₁ᵀ = 400 × FIM(x₁).

FIM contribution of x₂^B: (1/σ²) × x₃ · x₃ᵀ = standard contribution.

If σ_noise for x₂^A is 0.05 (laser-precision duplicator) and σ for x₂^B is 1.0: FIM trace(x₂^A addition) = 400 × trace, while FIM trace(x₂^B addition) = trace/1. Classical prefers x₂^A by 400×.

**The divergence:** x₂^A has trace advantage 400× over x₂^B. But x₂^A score ≈ 0 (adds nothing about β₂). x₂^B score = full (resolves all remaining β₂ ambiguity).

*This is the same divergence pattern as the second-sensor benchmark (Domain A) from prior sprints. Proved there; structural analogy here.*

---

### Example C2-B: Active Learning with Repeated Query Region

**Setting:** A classifier is queried at data points to reduce uncertainty about decision boundary θ. Two query strategies:

- Strategy A: Query k new points near the same dense cluster already well-characterized.
- Strategy B: Query 1 new point near the boundary of the ambiguous region.

**UOP framing:**
- Current measurement set F = {labeled points seen so far}.
- R(F) = region of parameter space compatible with all labeled points.
- score(query A | F) = |R(F) pairs distinguished by A|. For queries in the already-well-characterized region: A is nearly equivalent to existing queries. score(A | F) ≈ 0.
- score(query B | F) = |R(F) pairs distinguished by B|. B resolves pairs near the decision boundary. score > 0.

**Classical active learning criterion:** Query where uncertainty is highest (entropy sampling, margin sampling, etc.). In the dense cluster region: uncertainty may be low but the query IS near existing labeled points (refinement, not orthogonal jump). Near the decision boundary: uncertainty is high AND the query is orthogonal to existing information.

In this setting, classical uncertainty-based criteria and UOP tend to agree (uncertain regions = unresolved regions). The divergence arises specifically when a region has low uncertainty but high overlap with the existing measurement family (Type I: measurements cover the same direction, just precisely). In active learning, this is the "near-duplicate query" problem — querying k points near an existing labeled point adds little score despite being cheap.

---

## C3 — Synthesis: Failure Types in ML

| Failure type | ML manifestation | Example | Resolution |
|---|---|---|---|
| Type I (injectivity) | Redundant feature / near-duplicate query | x₂ ≈ x₁, same-regime assay repeat, near-duplicate sensor | Add orthogonal feature / new experimental regime / different sensor direction |
| Type II (missing invariant) | Parameter symmetry / gauge redundancy | Neural net permutation, matrix factorization scaling, GMM label ambiguity | Gauge-fixing (normalization, ordering, anchor variable, regularization with symmetry-breaking term) |
| Type III (admissibility) | Ill-posed objective / circular self-reference | Self-referential reward in RL (reward depending on the policy being learned), circular definition of fairness constraint | Restrict to well-posed objective class; break circularity |
| Type IV (time-consistency) | Non-stationary active learning / bandit feedback | Adaptive queries where the data distribution changes in response to the querying policy | Dynamic observer-state model; account for distribution shift |

**Notes on Types III and IV in ML:**

Type III (structural analogy): In reinforcement learning with reward shaping, a circular definition like "the reward is the difference in policy value" can lead to objectives that are not well-posed (the policy evaluation depends on the very objective being optimized). This has structural similarity to Russell's paradox: the domain (valid rewards) does not include self-referential ones.

Type IV (structural analogy): In online learning or bandit settings, the learner's queries change the data-generating distribution (e.g., A/B testing where showing variant A changes user behavior for future exposures). The "observation map" is no longer fixed — it changes as a function of the observer's actions. UOP applies only if the map is static.

Both Type III and Type IV labels in ML are structural analogies, not formal theorems.

---

## C4 — The Unified Failure Table for ML

**Type I in ML:** Redundant measurement. Score-0 measurements that add precision to already-constrained directions. Resolved by orthogonal measurements.

Canonical examples: duplicate features, repeated assay in same regime, same-direction sensor addition with lower noise. All have high FIM trace, zero UOP score.

**Type II in ML:** Symmetry-induced non-identifiability. Multiple parameter settings are observationally equivalent. Score-0 for all observations within the model-output family. Resolved by gauge-fixing.

Canonical examples: neural net permutation symmetry (H! per function), matrix factorization scaling (continuous group), GMM label permutation. All have provable ambiguity sets that no training data point can resolve.

**Key distinction between Type I and Type II in ML:**

Type I: The observation family is insufficient. Adding a new measurement type (different direction) with positive score resolves it.

Type II: The observation family is structurally complete for the given model class, but the model class itself has a symmetry. Adding more observations of any type does not break the symmetry — only adding a constraint external to the observation family (normalization, ordering, auxiliary regularizer) resolves it.

**Test for Type I vs. Type II:**

Ask: "Does there exist ANY measurement of the form F(θ,x) that would distinguish θ from g·θ?"

- If YES: the issue is Type I (we haven't taken that measurement yet).
- If NO: the issue is Type II (no measurement in the model-output family can distinguish them, by definition of the symmetry g).

For neural net permutation: NO — F(θ,x) = F(g·θ, x) for all x by construction. Type II.
For missing feature β₂: YES — measuring x₂ (a feature related to β₂) distinguishes (β₁,β₂) from (β₁,β₂'). Type I.

---

## Strongest Honest Claim

> Two structural failure types appear in ML: Type I (redundant measurement, resolved by adding orthogonal measurements) and Type II (model symmetry, resolved by gauge-fixing). They are distinguishable by whether any observation in the model-output family can break the ambiguity. For Type I, the answer is yes (positive-score measurement exists). For Type II, the answer is no (symmetry is exact, all observations are symmetric). The permutation symmetry of neural networks and the scaling symmetry of matrix factorization are exact Type II failures, provable from the model definitions. The redundant-feature problem is an exact Type I failure. Types III and IV appear in ML as structural analogies (circular objectives, adaptive distribution shift), not formal theorems in the current arc.

## Strongest Honest Boundary

> The ML symmetry examples (neural networks, matrix factorization) are proved facts about those model classes. The UOP classification (Type II, resolved by gauge-fixing) is a structural vocabulary applied to these models — correct and informative, but not adding new mathematical content beyond what is already known in the ML identifiability literature. The value added is: a unified language placing neural-net symmetry, matrix-factorization scaling, and GMM label-switching in the same structural class as Banach-Tarski's missing-measure problem, distinguishing them from the measurement-insufficiency problems of the sensor-placement and CT benchmarks.
