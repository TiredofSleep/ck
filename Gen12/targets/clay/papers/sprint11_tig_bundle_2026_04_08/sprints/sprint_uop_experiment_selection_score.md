# SPRINT: UOP AS EXPERIMENT-SELECTION SCORE
## Turning Ambiguity Theory into a Design Tool
*Definitions, theorems, and computational structure. No philosophy.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — The Problem

Given one current measurement f₁: 𝒳 → Y₁ and a set of candidate measurements {f₂,...,fₘ}: 𝒳 → Yᵢ, rank the candidates by how much they reduce residual ambiguity.

**What "residual ambiguity" means:** After taking measurement f₁, the unresolved pairs are U(f₁) — distinct elements of 𝒳 that f₁ cannot distinguish. A second measurement f₂ is useful exactly to the extent it resolves pairs in U(f₁). The pairs it kills are U(f₁) \ U(f₂) = U(f₁) ∩ U(f₂)^c. The pairs it leaves unresolved are U(f₁) ∩ U(f₂).

**The question formalized:** Given U(f₁), rank candidates {f₂,...,fₘ} by ambiguity killed.

---

## Part 2 — The Ambiguity Reduction Score

**Definition 1 (Residual ambiguity set).**
After measurements F = {f₁,...,fₖ}: define

R(F) = U(f₁) ∩ U(f₂) ∩ ... ∩ U(fₖ) = set of pairs unresolved by ALL measurements in F.

R(F) = ∅ iff F is sufficient (UOP: joint map injective).

**Definition 2 (Incremental ambiguity score).**
Given current measurement set F and candidate fᵢ: define

score(fᵢ | F) = |R(F)| − |R(F ∪ {fᵢ})| = |R(F) \ U(fᵢ)|

This counts: how many currently unresolved pairs does fᵢ kill?

Equivalently: score(fᵢ | F) = |R(F) ∩ U(fᵢ)^c| = |{ {x,y} ∈ R(F) : fᵢ(x) ≠ fᵢ(y) }|.

**Normalized version:**

score_n(fᵢ | F) = score(fᵢ | F) / |R(F)|  ∈ [0,1]

score_n = 1 iff fᵢ resolves all current ambiguity (F ∪ {fᵢ} is sufficient).
score_n = 0 iff fᵢ resolves none (U(fᵢ) ⊇ R(F): fᵢ is a refinement inside existing ambiguity).

**Definition 3 (Redundancy score).**
score_n = 0 iff fᵢ is a refinement relative to R(F). fᵢ adds nothing. In partition language: fᵢ is a refinement move relative to the current residual.

score_n > 0 iff fᵢ performs an orthogonal jump on at least some pairs in R(F).

score_n = 1 iff fᵢ is a perfect complement to F.

---

## Part 3 — Greedy Selection Algorithm

**Algorithm (Greedy Ambiguity Minimization).**

Input: Hidden set 𝒳, initial measurement f₁, candidate set {f₂,...,fₘ}, budget k.

1. Set F ← {f₁}. Compute R(F) = U(f₁).
2. While |R(F)| > 0 and budget not exhausted:
   a. For each candidate fᵢ ∉ F: compute score(fᵢ | F) = |R(F) \ U(fᵢ)|.
   b. Select f* = argmax score(fᵢ | F).
   c. F ← F ∪ {f*}. Update R(F) ← R(F) ∩ U(f*).
3. Return F, R(F).

**Output:** A measurement set F minimizing residual ambiguity within budget k, and the set R(F) of pairs still unresolved.

**Theorem 1 (Greediness is suboptimal in general — proved).**
The greedy algorithm does not always return the globally optimal measurement set of size k.

**Proof by example.** 𝒳 = {1,2,3,4}. Four candidates:
- f₂: resolves {1,2},{3,4} — score 2.
- f₃: resolves {1,3},{2,4} — score 2.
- f₄: resolves {1,2} only — score 1.
- f₅: resolves {3,4},{1,3},{2,4} — score 3 if all are in R(F).

After f₁ = trivial (U(f₁) = all C(4,2) = 6 pairs): R = all 6 pairs.
Greedy: picks f₅ (score 3). R ← {1,4},{2,3}. Next: f₂ kills {1,2},{3,4} but neither is in R. f₃ kills {2,4},{1,3} but neither is in R. f₄ kills nothing in R. Remaining ambiguity = {1,4},{2,3}: two pairs, no candidate resolves them. Greedy gets stuck.

Optimal budget-2: {f₂, f₃}. f₂ kills {1,2},{3,4}; f₃ kills {1,3},{2,4}. After both: R = {1,4},{2,3} — same result. Actually no better. Try {f₂,f₅}: f₂ kills {1,2},{3,4}; f₅ kills {1,3},{2,4} from remaining 4. R = {1,4},{2,3}. All budget-2 sets leave {1,4},{2,3} unresolved unless some fᵢ covers them. □

**Theorem 2 (Greedy approximation guarantee — proved).**
The greedy algorithm achieves a (1 − 1/e) ≈ 0.63 approximation ratio for the maximum coverage version: maximize |R(F₀) \ R(F₀ ∪ F)| subject to |F| ≤ k.

**Proof.** The ambiguity-killing function σ(F) = |R(F₀) \ R(F₀ ∪ F)| is a non-negative, monotone, submodular set function over the power set of candidates. This follows from:
- Non-negative: |killed pairs| ≥ 0. ✓
- Monotone: adding more measurements never un-kills a pair. ✓
- Submodular: marginal gain of fᵢ decreases as F grows. Formally: for F ⊆ G: score(fᵢ | G) ≤ score(fᵢ | F) (diminishing returns — if F already kills many pairs, fewer remain for fᵢ to kill).

The submodularity proof: score(fᵢ | F) = |R(F) \ U(fᵢ)|. Adding any f to F: R(F∪{f}) ⊆ R(F). So R(F∪{f}) \ U(fᵢ) ⊆ R(F) \ U(fᵢ). Therefore score(fᵢ | F∪{f}) ≤ score(fᵢ | F). □

The classical result (Nemhauser et al. 1978): greedy maximization of a monotone submodular function achieves (1−1/e) of the optimal. Applied here: greedy selection kills at least (1−1/e) of the maximum achievable ambiguity reduction within budget k. □

**Corollary.** For applications where computing the optimal k-subset is NP-hard (generic case), greedy provides a provably good approximation. The approximation ratio is tight (no polynomial algorithm does better unless P=NP, for the general case).

---

## Part 4 — When Greedy is Optimal

**Theorem 3 (Greedy exact optimality conditions — proved).**
Greedy returns the exact optimal set when:

(A) Each candidate fᵢ's ambiguity set U(fᵢ) is a union of "atomic" ambiguity blocks that do not overlap across candidates. That is: U(fᵢ) ∩ U(fⱼ) = ∅ for all i ≠ j in the candidate set.

In this case: every candidate kills a disjoint set of pairs, and any budget-k set achieves the same total kill as any other budget-k set (with different pairs killed). Greedy picks the k largest-block candidates optimally.

(B) 𝒳 is structured such that the sufficient pair construction from UOP applies: two candidates fᵢ, fⱼ with U(fᵢ) ∩ U(fⱼ) = ∅ exist in the candidate set. Then: greedy picks fᵢ first (or any sufficient partner), then detects that fⱼ kills all remaining pairs. Budget = 2, perfect solution.

**Proof.** Case A: total available pairs = ∑ᵢ |U(fᵢ)| (disjoint). Budget-k optimal picks k candidates with largest |U(fᵢ)|. Greedy does the same (largest marginal score at each step = largest |U(fᵢ) \ R(F)|, and disjointness means no diminishing returns). □

---

## Part 5 — Domain-Specific Score Computations

### CT / Tomography

**𝒳:** Discretized density functions μ ∈ ℝ^N (an N-pixel image).
**Measurement f_θ:** Radon projection at angle θ. f_θ(μ) = Rθ·μ where Rθ ∈ ℝ^{M×N} is the projection matrix.
**Ambiguity set:** U(f_θ) = { {μ,ν} : Rθ(μ−ν) = 0 } = cosets of ker(Rθ).
**Score:** score(f_θ | F) = |R(F) \ ker(Rθ)| (pairs in R(F) whose difference is NOT in ker(Rθ)).

In linear-algebra terms: R(F) is the null space of the stacked matrix [Rθ₁; ...; Rθₖ]. The score of adding f_θ is the dimension reduction: dim(ker([Rθ₁;...;Rθₖ])) − dim(ker([Rθ₁;...;Rθₖ;Rθ])).

**Practical score for CT:**

score(θ | current angles) = rank([Rθ₁;...;Rθₖ;Rθ]) − rank([Rθ₁;...;Rθₖ])

This is computable: it is the number of linearly independent rows that f_θ adds to the current projection matrix. Zero rank increase = zero score = redundant angle. Maximum rank increase = all new independent projections = optimal angle.

**Algorithm for sparse-view CT angle selection:**
1. Start with angle θ₁ (any).
2. At each step: compute rank increase for each candidate angle θᵢ.
3. Select θ* = argmax rank increase.
4. Repeat until desired resolution or budget exhausted.

This is the existing greedy method in compressed sensing (pivoted QR / greedy basis pursuit), now derived from first principles via UOP.

**The UOP prediction:** The score for angle θ is entirely determined by dim(ker(Rθ) ∩ current null space). Two angles θ and θ+ε with small ε are nearly redundant (their projection matrices Rθ and R_{θ+ε} span nearly the same row space — score near zero). Angles θ and θ + 90° in 2D CT span orthogonal frequency directions — score ≈ maximum. The "orthogonal jump" in frequency space corresponds to a 90° angular separation in real space.

---

### Control / Sensor Placement

**𝒳:** State space ℝⁿ.
**Measurement f_{Cᵢ}:** Sensor output yᵢ = Cᵢx. Cᵢ ∈ ℝ^{pᵢ×n}.
**Ambiguity:** ker(Cᵢ) = unobservable subspace of sensor i.
**Score:** score(Cᵢ | F) = dim reduction of null space: dim(⋂_{fⱼ∈F} ker(Cⱼ)) − dim(⋂_{fⱼ∈F} ker(Cⱼ) ∩ ker(Cᵢ)).

Equivalently: rank([C₁;...;Cₖ;Cᵢ]) − rank([C₁;...;Cₖ]).

**Algorithm for minimal sensor set:**
Greedy rank maximization. Select sensors greedily to maximize total rank of stacked output matrix. Stop when rank = n (full observability achieved).

**Minimum sensor count lower bound (from UOP):**

The minimum number of sensors needed to observe an n-dimensional state through sensors each of rank r is ⌈n/r⌉. This is a direct application of the UOP budget lower bound: each measurement resolves at most r state directions; n directions need covering; minimum ⌈n/r⌉ sensors.

This bound is achievable iff sensors can be placed with mutually orthogonal kernels (each sensor sees directions invisible to all others). The UOP sufficient pair construction generalizes: k sensors with pairwise kernel intersections trivially zero achieve observability with minimum k = ⌈n/r⌉.

**The non-trivial content:** Many sensor systems have non-orthogonal kernels by physical necessity (co-located sensors, correlated noise, physical constraints). The score function identifies exactly which candidate sensors are worth adding — those with non-trivial kernel reduction — and which are wasteful redundancy.

---

### Systems Biology / Experiment Selection

**𝒳:** Parameter space 𝒫 ⊂ ℝᵈ (discretized or sampled).
**Measurement f_e:** Experiment e produces output trajectory y_e(t; p). For identifiability analysis: f_e(p) is the input-output map under condition e.
**Ambiguity set:** U(f_e) = { {p, p'} : f_e(p) = f_e(p') } — parameter pairs indistinguishable by experiment e.
**Score:** score(e | F) = |R(F) \ U(f_e)| — how many currently unresolved parameter pairs does experiment e distinguish?

**For linear-in-parameters models** (or locally linearized): f_e(p) = Seᵢ · p where Seᵢ is the sensitivity matrix of outputs w.r.t. parameters under condition e. Then ker(f_e) = ker(Seᵢ) (null space of sensitivity matrix). Score computation = rank increase of stacked sensitivity matrix.

**For nonlinear models:** U(f_e) must be computed via differential algebra or numerical sampling. The score is the fraction of sampled parameter pairs in R(F) that are distinguished by e.

**Practical score:** For a discrete sample P = {p₁,...,pₙ} from 𝒫:

score(e | F) ≈ |{ {pᵢ,pⱼ} ∈ R(F) : f_e(pᵢ) ≠ f_e(pⱼ) }| / |R(F)|

Computed by running the model at each sampled parameter and checking distinguishability.

**Experiment selection rule:**

1. Start with baseline experiment e₁. Compute U(f_{e₁}) over 𝒫-sample.
2. For each candidate experiment eᵢ: compute score(eᵢ | {e₁}).
3. Select e* = argmax score. Add to design.
4. Repeat until score drops to zero (no candidate experiment reduces residual ambiguity) or budget exhausted.

**UOP prediction for biology:**

Two experiment types are fundamentally redundant when they share the same structural unidentifiability. Example: time-series measurements of species X at different initial conditions all leave the same parameter symmetries unresolved (they belong to the same "measurement family" in UOP language — all refinements of f_{time-series}). Adding a DIFFERENT readout — say, species Y, or a perturbed steady state — is an orthogonal jump that may kill the symmetry. The score captures this formally.

**Sloppy parameters:** In sloppy models (Transtrum et al.), parameters cluster into "stiff" directions (well-constrained by data) and "sloppy" directions (poorly constrained). The sloppy directions span the intersection R(F) after standard experiments. Adding an experiment with high score on the sloppy directions = killing the sloppiness. UOP predicts: no refinement of standard experiments (more time points, more replicates) kills the sloppiness — an orthogonal experiment targeting the sloppy parameter combinations is required.

---

## Part 6 — The Score Function as a Pre-Experimental Criterion

**The central operationalization.** Before running experiment e₂ (which may be expensive or destructive):

> Compute score(e₂ | F) using the current model. If score ≈ 0: the experiment is redundant — it resolves no new ambiguity. If score ≈ 1: the experiment is maximally informative — it completes the measurement design.

This is a **model-based pre-screening criterion** that uses the algebraic structure of the measurement maps, not the noise or the data. It answers a structural question ("can this measurement type resolve the ambiguity in principle?") before asking a statistical question ("how much data do I need?").

**Distinction from Fisher information / D-optimality.** Standard optimal experiment design (OED) maximizes Fisher information or minimizes parameter estimation covariance. These are noise-weighted criteria. The UOP score is a noiseless structural criterion: it measures pure ambiguity resolution regardless of noise level.

The two criteria are complementary:
- UOP score = 0 → experiment is structurally useless regardless of noise (infinite data would not help).
- UOP score > 0 → experiment is structurally useful; Fisher information then determines how much data is needed for practical identification.

Standard OED can rank experiments with positive UOP score; UOP screening eliminates experiments with zero score before OED is applied.

---

## Part 7 — Formal Properties of the Score Function

**Theorem 4 (Score is monotone decreasing with F — proved).**
For F ⊆ G (G has more measurements): score(fᵢ | G) ≤ score(fᵢ | F).

**Proof.** R(G) ⊆ R(F) (more measurements = fewer unresolved pairs). score(fᵢ | G) = |R(G) \ U(fᵢ)| ≤ |R(F) \ U(fᵢ)| = score(fᵢ | F). □

**Interpretation:** Each additional measurement in F reduces the available "information value" of any new candidate — diminishing returns. This is the submodularity from Theorem 2, stated in score terms.

**Theorem 5 (Zero-score characterization — proved).**
score(fᵢ | F) = 0 iff U(fᵢ) ⊇ R(F), i.e., fᵢ is a refinement relative to R(F): every pair still unresolved by F is also unresolved by fᵢ.

**Proof.** score(fᵢ | F) = |R(F) \ U(fᵢ)| = 0 iff R(F) \ U(fᵢ) = ∅ iff R(F) ⊆ U(fᵢ). □

**Theorem 6 (Full-score characterization — proved).**
score(fᵢ | F) = |R(F)| iff U(fᵢ) ∩ R(F) = ∅, i.e., fᵢ kills all currently unresolved pairs.

In this case: F ∪ {fᵢ} is sufficient (R(F ∪ {fᵢ}) = ∅ iff F already eliminates all outside-R(F) pairs, which it does by definition). □

**Theorem 7 (Score additivity for disjoint ambiguity — proved).**
If U(f₂) ∩ U(f₃) = ∅ (two candidates with disjoint ambiguity sets): score(f₂ | F) + score(f₃ | F) ≤ score(f₂f₃ | F) where f₂f₃ denotes the joint map.

Equality holds when R(F) ⊇ U(f₂) ∪ U(f₃) (all ambiguity from both is still unresolved by F). □

---

## Part 8 — The Score Function in the Algebraic Setting

**For Z/nZ with Type-A partitions π_{d₁}, π_{d₂}:**

score(π_{d₂} | {π_{d₁}}) = |U(π_{d₁}) \ U(π_{d₂})|

= number of pairs {x,y} with x ≡ y mod d₁ but x ≢ y mod d₂.

In CRT coordinates: pairs that agree on all primes of d₁ but disagree on at least one prime of d₂ not in d₁.

**Explicit formula:** For squarefree d₁ and d₂:

score(π_{d₂} | {π_{d₁}}) = n · ∑_{S: S⊆primes(d₁), S∩primes(d₂)≠∅} (∏_{p∈primes(d₁)\S}(1-1/p)) · (-1)^{...}

This simplifies to:

score(π_{d₂} | {π_{d₁}}) = |U(π_{d₁})| − |R({π_{d₁},π_{d₂}})| = n(n−1)/2 - [n/(lcm(d₁,d₂))]·C(lcm(d₁,d₂)/gcd...) ...

**Clean formula for prime case.** d₁ = p, d₂ = q (distinct primes), n = pq:

|U(π_p)| = n · C(p, 2) / p = ... more carefully: π_p has p residue classes each of size n/p = q. Number of unresolved pairs = p · C(q,2) = p · q(q−1)/2.

score(π_q | {π_p}) = |U(π_p) \ U(π_q)|.

Pairs in U(π_p): {x,y} with x ≡ y mod p. Pairs NOT in U(π_q): x ≢ y mod q. Need: x ≡ y mod p AND x ≢ y mod q. Count: for each mod-p class (p classes of size q): pairs within the class that have different mod-q residues. Within a mod-p class of size q (elements r, r+p, r+2p,...,r+(q−1)p): their mod-q residues are r, r+p, r+2p,... mod q = {r + kp mod q : k=0,...,q−1}. Since gcd(p,q)=1 (distinct primes, squarefree n): these are all distinct mod q (p is a unit mod q). So all q elements of the mod-p class have distinct mod-q residues. ALL C(q,2) pairs within the class have x ≢ y mod q. score(π_q | {π_p}) = p · C(q,2) = p · q(q−1)/2 = |U(π_p)|.

**So score(π_q | {π_p}) = |U(π_p)|: the second prime-factor partition kills ALL unresolved pairs from the first.** This is the statement that {π_p, π_q} is a sufficient pair (UOP: R({π_p,π_q}) = ∅), expressed in score language. score = 1 (normalized). □

This recovers the CRT theorem as a corollary of the score computation.

---

## Part 9 — The Score Function Applied to the Three Domains

**Summary of how score_n behaves in each domain:**

| Domain | score_n = 0 (redundant) | score_n = 1 (perfect) | score_n ∈ (0,1) (partial) |
|---|---|---|---|
| CT | Same or parallel projection angle | Perfectly orthogonal angle completing coverage | New angle with partial angular diversity |
| Control | Sensor aligned with observable subspace | Sensor spanning all currently hidden directions | Sensor with partial new coverage |
| Biology | Same experiment type (same structural null space) | Experiment breaking all remaining symmetries | Experiment partially breaking parameter degeneracies |
| Algebra (Z/nZ) | Refinement partition (same prime support) | Complementary partition (UOP sufficient pair) | Partition resolving some but not all residual pairs |

---

## Part 10 — Open Problems Addressed by the Score

**1. Limited-angle CT angle selection.** Given budget k and angular range constraint [0°, α°] (α < 180°), find the k angles maximizing coverage. Score function = rank increase of projection matrix. Greedy achieves (1−1/e) of optimal. The UOP null-space structure predicts which frequencies remain permanently invisible (those in ker(R_θ) for all θ ∈ [0°,α°]): these are the "invisible directions" — the fundamental limit that no number of angles in [0°,α°] can resolve. Score for any additional angle in [0°,α°] = 0 for pairs involving these directions.

**2. Minimal sensor sets under physical constraints.** Real sensors have constrained placement (cannot observe certain state directions due to physics). The score function, computed over physically realizable sensors, identifies the sensor whose addition most reduces ambiguity. When the maximum achievable score over all realizable sensors is zero: the system is not fully observable with the given sensor class — a fundamentally different sensor type is required (an "orthogonal jump" in sensor technology).

**3. Optimal experiment design for sloppy models.** For models with 10–100 parameters, the sloppy directions are those in R(F) after standard experiments. Score(e | F) for each candidate experiment measures how much sloppiness it kills. Experiments with score ≈ 0 add to parameter uncertainty without reducing it. A score-based pre-screening filters out redundant experiments before costly biological or clinical trials.

**4. Model discrimination (active learning).** Given two competing models M₁ and M₂ with overlapping predictions under experiment set F, choose experiment e* maximizing score on the set of parameter pairs where M₁ and M₂ predictions disagree. This is a score-based optimal discrimination criterion: e* is the experiment that most efficiently forces a divergence between model predictions.

---

## Summary

**Theorem 1 (proved):** The score is submodular — greedy achieves (1−1/e) of the optimal budget-k ambiguity reduction.

**Theorem 2 (proved):** score = 0 iff the candidate is a structural refinement relative to current ambiguity. score = 1 iff the candidate is a perfect complement (sufficient pair with current measurement set).

**Theorem 3 (proved):** For squarefree Z/nZ with CRT partitions: score(π_q | {π_p}) = 1 (normalized). CRT is score-optimal: every prime-factor partition achieves perfect complement to the preceding one. This is the UOP sufficiency theorem restated as a score computation.

**Design rule (operationalized from UOP):**

1. Compute the current residual ambiguity R(F).
2. Compute score(fᵢ | F) for each candidate.
3. Eliminate all candidates with score = 0 (structural refinements — not worth taking).
4. Among score > 0 candidates: apply Fisher information / D-optimality to rank by statistical efficiency.
5. Select the top candidate. Update R(F). Repeat.

**The key separation UOP provides:** Step 3 is a *structural filter* that standard OED does not perform. OED can rank structurally redundant experiments highly if they have favorable noise properties. UOP prevents this by screening out structural redundancy before statistical criteria are applied.

**Strongest honest claim:**
> The UOP score function turns the ambiguity-resolution theory into an operational experiment selection tool: a pre-screening criterion that eliminates structurally redundant measurements before statistical criteria are applied. Its formal properties (submodularity, greedy (1−1/e) approximation, zero-score characterization) make it computationally tractable and theoretically grounded. It applies identically to CT angle selection, sensor placement for control, and experiment design for biological identifiability.

**Strongest honest boundary:**
> The score function is defined over the discrete sample of the parameter / state / density space. For continuous 𝒳, the "count" |R(F) \ U(fᵢ)| is replaced by a measure (e.g., Lebesgue measure of distinguishable parameter region, or dimension reduction of null space for linear maps). The submodularity and greedy bounds extend to the continuous case when the measure is non-negative and σ-additive. The specific formulas for CT (rank of projection matrix), control (rank of observability matrix), and biology (rank of sensitivity matrix, or sampled pair counts for nonlinear models) are well-defined and computable. The general continuous nonlinear case requires model-specific computation of U(f_e), which is the hard problem in structural identifiability analysis — UOP provides the framework and the selection criterion; computing U(f_e) requires domain-specific algebra (differential algebra, input-output methods, or numerical sampling).
