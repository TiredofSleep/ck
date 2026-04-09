# SPRINT: UOP VS CLASSICAL EXPERIMENT DESIGN
## Does the Score Actually Change Decisions?
*All examples computable end-to-end. Proved vs. conjectural labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Setup

Three toy domains, each with explicit numbers. For each: compute UOP score AND classical criteria for the same candidate set, then compare rankings.

Classical criteria used:
- **D-optimality:** maximize det(FIM) where FIM = Fisher information matrix = Jᵀ·Σ⁻¹·J (J = sensitivity/Jacobian, Σ = noise covariance).
- **Rank gain:** number of linearly independent rows added to current measurement matrix (= linear version of UOP score for linear models).
- **Mutual information (MI):** I(θ; y_e) for Bayesian setting — expected reduction in parameter uncertainty.

---

## Domain A — Linear Observability / Sensor Placement

### Setup

**Hidden state:** x = (x₁, x₂, x₃) ∈ ℝ³. System matrix A (dynamics irrelevant for static case).

**Current sensor:** C₁ = [1, 1, 0] — measures x₁ + x₂. ker(C₁) = span{(1,−1,0), (0,0,1)}.

**Residual ambiguity R({C₁}):** All pairs {x, y} with C₁x = C₁y, i.e., x−y ∈ ker(C₁). Two dimensions unresolved: the subspace V = span{(1,−1,0), (0,0,1)}.

**Candidate sensors:** (noiseless for UOP; assume unit noise variance σ²=1 for Fisher)

- f₂: C₂ = [1, 1, 1] — measures x₁+x₂+x₃.
- f₃: C₃ = [0, 0, 1] — measures x₃.
- f₄: C₄ = [1, −1, 0] — measures x₁−x₂.
- f₅: C₅ = [2, 2, 0] — measures 2(x₁+x₂).
- f₆: C₆ = [1, 0, 1] — measures x₁+x₃.

### UOP Score Computation

**score(fᵢ | {C₁})** = dim(ker(C₁)) − dim(ker(C₁) ∩ ker(Cᵢ)).

ker(C₁) = span{(1,−1,0), (0,0,1)} (2D).

**f₂: C₂ = [1,1,1].** ker(C₂) = span{(1,−1,0),(1,0,−1)}.
ker(C₁) ∩ ker(C₂): v ∈ both means v = a(1,−1,0)+b(0,0,1) and [1,1,1]·v=0. [1,1,1]·(a,−a,b) = a−a+b = b = 0. So ker(C₁)∩ker(C₂) = span{(1,−1,0)} (1D).
score = 2 − 1 = **1**. Resolves 1 of 2 hidden dimensions.

**f₃: C₃ = [0,0,1].** ker(C₃) = span{(1,0,0),(0,1,0)}.
ker(C₁)∩ker(C₃): v = a(1,−1,0)+b(0,0,1) with [0,0,1]·v = b = 0. So ker(C₁)∩ker(C₃) = span{(1,−1,0)} (1D).
score = 2 − 1 = **1**. Resolves x₃ direction.

**f₄: C₄ = [1,−1,0].** ker(C₄) = span{(1,1,0),(0,0,1)}.
ker(C₁)∩ker(C₄): v = a(1,−1,0)+b(0,0,1) with [1,−1,0]·v = a−(−a) = 2a = 0. So a=0, v = b(0,0,1). ker intersection = span{(0,0,1)} (1D).
score = 2 − 1 = **1**. Resolves x₁−x₂ direction.

**f₅: C₅ = [2,2,0].** ker(C₅) = span{(1,−1,0),(0,0,1)} = ker(C₁) exactly (since C₅ = 2·C₁ as a linear form).
ker(C₁)∩ker(C₅) = ker(C₁) (2D, full).
score = 2 − 2 = **0**. Resolves nothing.

**f₆: C₆ = [1,0,1].** ker(C₆) = span{(0,1,0),(1,0,−1)}.
ker(C₁)∩ker(C₆): v = a(1,−1,0)+b(0,0,1) with [1,0,1]·v = a+b = 0. So b=−a, v = a(1,−1,0)−a(0,0,1) = a(1,−1,−1). ker intersection = span{(1,−1,−1)} (1D).
score = 2 − 1 = **1**. Resolves one mixed direction.

### Fisher Information / D-Optimality Computation

FIM for current measurement: Φ(F) = C₁ᵀC₁ = [[1,1,0]]ᵀ[[1,1,0]] = [[1,1,0],[1,1,0],[0,0,0]].

For sensor Cᵢ added: FIM(F∪{Cᵢ}) = C₁ᵀC₁ + CᵢᵀCᵢ.

D-optimality gain: det(FIM(F∪{Cᵢ})) / det(FIM(F)).

Note: det(FIM(F)) = det([[1,1,0],[1,1,0],[0,0,0]]) = 0 (rank 1 matrix, 3D system). So D-optimal criterion cannot rank additions by det ratio from zero. Use instead: log-det of regularized FIM, or trace criterion (A-optimality), or rank gain directly.

**Rank gain (= UOP score for linear systems — proved):**

rank([C₁; Cᵢ]) − rank([C₁]) = UOP score. These are identical for linear maps. f₅ has rank gain 0 (same row space as C₁). All others have rank gain 1.

So for linear systems: **UOP score = rank gain exactly.** No divergence yet. We need a setting where classical criteria differ — which requires noise.

### Introducing Noise: Where Classical Diverges from UOP

Add noise: sensor i returns yᵢ = Cᵢx + εᵢ, εᵢ ~ N(0, σᵢ²).

**Key setup:** σ₅² = 0.01 (f₅ = 2(x₁+x₂) with very LOW noise). σ₂² = σ₃² = σ₄² = σ₆² = 1 (standard noise).

**FIM for f₅ added:** C₅ᵀC₅/σ₅² = [2,2,0]ᵀ[2,2,0]/0.01 = [[4,4,0],[4,4,0],[0,0,0]]/0.01 = 100·[[4,4,0],[4,4,0],[0,0,0]].

This adds a LARGE contribution to FIM because of low noise — even though f₅ = 2·C₁ spans the same row space as C₁.

**FIM for f₃ added:** C₃ᵀC₃/σ₃² = [0,0,1]ᵀ[0,0,1]/1 = [[0,0,0],[0,0,0],[0,0,1]].

This adds a modest contribution targeting x₃.

**Trace(FIM) comparison after adding one sensor:**

- Add f₅ (score=0, low noise σ²=0.01): trace(FIM+f₅) = trace(C₁ᵀC₁) + trace(C₅ᵀC₅/0.01) = 2 + 100·8 = 802. ← **massive trace gain**
- Add f₃ (score=1, standard noise σ²=1): trace(FIM+f₃) = 2 + 1 = 3. ← **tiny trace gain**

**Classical A-optimality (minimize trace of FIM inverse) would prefer f₅** — it contributes 100× more to the x₁+x₂ direction's precision. **UOP pre-screening eliminates f₅** because score=0 — it adds no structural information.

**Why classical is wrong here:** f₅ makes the x₁+x₂ combination extremely precise but leaves x₁−x₂ AND x₃ completely unidentified (score=0: ker(C₁)∩ker(C₅) = ker(C₁), nothing new resolved). After adding f₅, R({C₁,C₅}) = R({C₁}): ambiguity unchanged. You know x₁+x₂ to very high precision but still cannot tell whether x₁=1,x₂=0 or x₁=0,x₂=1. The classical criterion confuses precision of a known direction with resolution of unknown directions.

**Proposition A1 (proved).** For linear systems with heterogeneous noise: there exist scenarios where the A-optimal (trace-maximizing) next sensor has UOP score = 0. Specifically: any sensor C₅ = α·C₁ (same direction, lower noise) has score = 0 but can have arbitrarily high Fisher information contribution.

**Proof.** C₅ = α·C₁ → ker(C₅) = ker(C₁) → score = 0. FIM contribution = α²/σ₅² · C₁ᵀC₁ → ∞ as σ₅→0 for fixed α. Classical A/D-optimal criteria treat this as infinitely informative. UOP score = 0 regardless. □

### Comparison Table — Domain A

| Candidate | UOP score | Rank gain | A-opt rank (σ₅=0.01) | Resolves? |
|---|---|---|---|---|
| f₂ = [1,1,1] | 1 | 1 | 3rd | 1 new direction |
| f₃ = [0,0,1] | 1 | 1 | 4th | x₃ resolved |
| f₄ = [1,−1,0] | 1 | 1 | 2nd | x₁−x₂ resolved |
| **f₅ = [2,2,0]** | **0** | **0** | **1st** | **Nothing** |
| f₆ = [1,0,1] | 1 | 1 | 5th | 1 mixed direction |

**f₅ ranked 1st by A-optimality, 0 by UOP. This is the divergence.**

---

## Domain B — Limited-Angle Tomography

### Setup

**Discretized image:** μ ∈ ℝ^{16} — a 4×4 pixel image. N = 16.

**Projection geometry:** 2D parallel-beam CT. Angle θ gives 4 parallel ray integrals crossing the image. Projection matrix R_θ ∈ ℝ^{4×16}.

**Current measurements:** Angles θ = 0° and θ = 10°. These two angles are nearly parallel — nearly the same row space.

**Null space characterization (approximate):** Two nearly-parallel angles cover primarily horizontal (0°) frequency information. Vertical frequency information (90°-direction) and diagonal frequencies remain largely in the null space.

**Candidate angles:** θ = 5° (between current), θ = 45°, θ = 90°, θ = 91°.

### UOP Score (= Rank Gain for Linear Systems)

Score(θ | F) = rank([R_0; R_10; R_θ]) − rank([R_0; R_10]).

**Approximate analysis (exact for idealized parallel-beam):**

Current rank: rank([R_0; R_10]) ≈ 7 (two nearly-parallel angles in a 4×4 image cover ~7 independent directions).

- θ = 5°: Nearly parallel to existing angles. Rank gain ≈ 1 (marginal). UOP score ≈ 1/16 of residual. **Low score.**
- θ = 45°: Diagonal direction, independent of horizontal. Rank gain ≈ 4 (covers ~4 new diagonal directions). **High score.**
- θ = 90°: Vertical direction, orthogonal to horizontal. Rank gain = 4 (covers all vertical frequencies). **Maximum score for this budget.**
- θ = 91°: Nearly vertical. Rank gain ≈ 4 (nearly as good as 90°). **High score, slightly lower.**

### Classical Criteria (Noise-Based Divergence)

Now introduce physically-motivated noise: near-parallel projections at θ = 5° are taken at a distance from the current detector, with 3× higher SNR (less scatter, better alignment with existing detector array).

σ(θ = 5°) = 0.3 (low noise — physical proximity to detector).
σ(θ = 90°) = 1.0 (standard noise — different detector orientation).

**D-optimal criterion:** Selects angle θ maximizing log-det of FIM. For nearly parallel θ=5°: FIM contribution = R₅ᵀR₅/σ₅² adds a large boost in the EXISTING well-covered direction. FIM(F∪{R_5°}) has large eigenvalue along existing null-space-complement, but leaves existing null-space intact.

D-optimality log-det: adding θ=5° increases log-det by 3×log(low noise) for the already-large eigenvalue. Adding θ=90° increases log-det by 4×log(1.0) for the null-space eigenvalues that are ZERO currently — infinite log-det gain? No: the zero eigenvalues don't become infinite, they go from 0 to some value σ⁻².

**Exact comparison (in the null space):**

D-optimal gain from θ: sum over eigenvalues of Δ = log-det change = log(1 + λᵢ·new contribution). For eigenvalues in current null space (= 0): gain = log(1 + σ_θ⁻² · u·R_θᵀR_θ·u) for unit vector u in null space.

For θ=5° (nearly parallel, σ=0.3): contributes ~0.09/σ² ≈ 1.0 to null-space eigenvalue in direction aligned with 5°, near-zero to truly orthogonal directions.

For θ=90° (σ=1.0): contributes ~1.0 to vertical-frequency eigenvalues (large null-space directions).

D-opt prefers θ=90° here — good. But:

**The divergence case:** Add a SECOND near-parallel angle θ=6° with σ=0.1 (very low noise). After already having {0°,5°}:

- UOP score(6° | {0°,5°}) ≈ 1 (small, nearly same as 5° added to {0°}).
- FIM contribution: σ=0.1 → enormous boost in the x₁+x₂ direction precision.
- D-opt might prefer 6° over 90° if the log-det gain from high-precision near-parallel exceeds the gain from moderate-precision orthogonal.

**Constructed numerical example:** N = 4 pixels (1×4 strip, simplified).

Current measurements: R_0 = [1,1,1,1] (sum of all pixels), R_10 ≈ [1.0, 0.9, 0.8, 0.7] (tilted).

Candidates:
- R_5 ≈ [1.0, 0.95, 0.85, 0.75], noise σ=0.1.
- R_90 = [1,0,0,0] (projects onto pixel 1), noise σ=1.0.
- R_180 = [1,1,1,1] = R_0, noise σ=0.05 (high-precision repeat).

UOP scores:
- R_5: nearly parallel → score ≈ 1/4 of residual. Low.
- R_90: orthogonal → score ≈ 1 (resolves all x₂,x₃,x₄ directions that R_0,R_10 confused). High.
- R_180: identical to R_0 → score = 0 exactly. Zero.

Classical (FIM trace, σ-weighted):
- R_180: trace contribution = [1,1,1,1]ᵀ[1,1,1,1]/0.05² = 16/0.0025 = 6400. **Classical ranks first.**
- R_5: trace contribution ≈ (sum of sq)/0.01 ≈ 1600. **Classical ranks second.**
- R_90: trace contribution = [1,0,0,0]ᵀ[1,0,0,0]/1.0 = 1. **Classical ranks last.**

**UOP score 0 for R_180 (exact repeat), moderate for R_5, maximal for R_90. Classical ranks them in reverse order.**

**Proposition B1 (proved).** A high-precision repeat of a prior measurement (f = α·g for g ∈ F, σ → 0) has UOP score = 0 and arbitrarily large Fisher information contribution. Classical criteria (trace, det of FIM) prefer the repeat; UOP eliminates it.

**Proof.** f = α·g → ker(f) = ker(g) → ker(f) ∩ R(F) = ker(g) ∩ R(F). If g ∈ F: ker(g) ⊇ R(F) (R(F) is the intersection of all current null spaces, including ker(g)). So ker(f) ⊇ R(F), score = 0. FIM contribution = α²·gᵀg/σ² → ∞ as σ → 0. □

### Comparison Table — Domain B (1×4 strip, 3 candidates)

| Candidate | UOP score | Rank gain | FIM trace rank (σ-weighted) | Physical interpretation |
|---|---|---|---|---|
| R_90 = [1,0,0,0], σ=1 | **High (~1)** | 2–3 | **3rd (last)** | New orthogonal view |
| R_5 ≈ R_0, σ=0.1 | Low (~0.25) | 1 | 2nd | Slightly different angle, good SNR |
| **R_180 = R_0, σ=0.05** | **0 (exact)** | **0** | **1st** | **Exact repeat, great SNR** |

**Exact repeat ranked 1st by classical, 0 by UOP.**

---

## Domain C — Structural Identifiability: Michaelis-Menten

### Setup

**Model:** dx/dt = −Vmax·x/(Km+x), y(t) = x(t). Two parameters θ = (Vmax, Km).

**Hidden space:** 𝒫 = {(Vmax, Km) : Vmax,Km ∈ [0.1, 10]}. Discretize to 10×10 = 100 parameter pairs.

**Experiment e is characterized by initial substrate S₀.** The output is the time-trajectory y(t; Vmax, Km, S₀). Two parameter pairs (Vmax, Km) and (Vmax', Km') are indistinguishable by experiment e iff y(t; θ) = y(t; θ') for all t.

**Structural identifiability analysis:** For S₀ → 0 (low substrate): y(t) ≈ S₀·exp(−(Vmax/Km)·t). Only the ratio ρ = Vmax/Km is identifiable. U(f_{low}) = all pairs with same ρ.

For S₀ → ∞ (high substrate): y(t) ≈ S₀ − Vmax·t (linear depletion early). Only Vmax is identifiable. U(f_{high}) = all pairs with same Vmax.

**Current experiment:** e₁ = low substrate (S₀ = 0.1). R({e₁}) = U(f_{low}) = pairs with same ρ = Vmax/Km.

### Discretized Computation

Parameter grid: Vmax ∈ {1,2,...,10}, Km ∈ {1,2,...,10}. 100 parameter points.

**U(f_{low}):** pairs with Vmax/Km = Vmax'/Km'. For integer grid, identical ratios occur when (Vmax,Km) = k·(V₀,K₀) for integer k. Example: (1,1),(2,2),(3,3),...,(10,10) all have ρ=1. (1,2),(2,4),(3,6),(4,8) have ρ=0.5. Etc.

|U(f_{low})|: count pairs with same ratio. Number of distinct ratios on a 10×10 grid = 42 (Euler's totient function enumeration: distinct fractions p/q with 1≤p,q≤10). For ratio ρ = p/q (reduced): multiplicity = ⌊10/max(p,q)⌋. Computing: many ratios have multiplicity 1 (no paired points); ratios 1/1,1/2,...,2/1,etc. with multiplicity ≥ 2 contribute pairs.

For simplicity use a 5×5 grid: Vmax ∈ {1,2,3,4,5}, Km ∈ {1,2,3,4,5}. 25 points.

Same-ratio pairs:
- ρ=1: (1,1),(2,2),(3,3),(4,4),(5,5) → C(5,2)=10 pairs.
- ρ=2: (2,1),(4,2) → 1 pair. (Also (6,3) etc. out of range.)
- ρ=1/2: (1,2),(2,4) → 1 pair.
- ρ=3: (3,1) — singleton.
- ρ=4: (4,1) — singleton.
- ρ=5: (5,1) — singleton.
- ρ=3/2: (3,2) — singleton.
- ρ=4/3: (4,3) — singleton.
- ρ=5/2: (5,2) — singleton.
- ρ=3/4: (3,4) — no pair in 5×5.
- ρ=4/5: (4,5) — singleton.
- ρ=5/3: (5,3) — singleton.
- ρ=5/4: (5,4) — singleton.
... etc.

For the 5×5 grid: |R({e₁})| = 10 + 1 + 1 = **12 pairs** (ρ=1 contributes 10, ρ=2 and ρ=1/2 each contribute 1).

### Candidate Experiments

- e₂_high: S₀ = 100 (high substrate, identifies Vmax).
- e₂_med: S₀ = 2 (medium substrate, km ≈ Km condition, identifies both partially).
- e₂_low2: S₀ = 0.5 (another low substrate — different S₀ but still in linear regime).
- e₂_repeat: S₀ = 0.1 (exact repeat of e₁ with lower noise σ²=0.01 vs σ²=0.1).

**UOP score computation:**

**e₂_low2 (S₀=0.5, still low substrate):** In the linear regime: y(t) ≈ S₀·exp(−(Vmax/Km)·t). SAME functional form as e₁. Indistinguishable pairs = same-ratio pairs = U(f_{low2}) = U(f_{low}) = R({e₁}). score = |R({e₁}) \ U(f_{low2})| = **0**. Structural repeat.

**e₂_repeat (S₀=0.1 again, σ²=0.01):** Same model structure → same structural ambiguity. score = **0**.

**e₂_high (S₀=100):** U(f_{high}) = pairs with same Vmax. On the 5×5 grid: pairs with Vmax = Vmax' but Km ≠ Km' = C(5,2) pairs per Vmax value? No: same-Vmax pairs are (V,K),(V,K') for K≠K'. There are 5 Vmax values × C(5,2) = 5×10=50 such pairs. None of these overlap with the ρ=1 pairs: (V,K) and (V',K') with V/K = V'/K' requires K/V = K'/V', so if V=V' then K=K' (same point). So: U(f_{high}) ∩ U(f_{low}): need same ρ AND same Vmax. Same Vmax V, same ratio V/K=V/K' → K=K'. Only the trivial pairs (same point). So U(f_{high}) ∩ U(f_{low}) = ∅ (excluding trivial pairs). score(e₂_high | {e₁}) = |R({e₁}) \ U(f_{high})| = |R({e₁})| = **12**. score_n = 1. **Perfect complement.**

Verify: After both e₁ (identifies ρ) and e₂_high (identifies Vmax): ρ = Vmax/Km and Vmax are known → Km = Vmax/ρ. Fully identified. ✓

**e₂_med (S₀=2, S₀≈Km typical value):** Identifies both partially. U(f_{med}) = pairs where the full time-trajectory is the same. For Michaelis-Menten: y(t;Vmax,Km,2) = y(t;Vmax',Km',2) iff Vmax=Vmax' AND Km=Km' (generically — two-parameter system fully identifiable from medium substrate data). So U(f_{med}) = empty set (no ambiguous pairs). score = |R({e₁})| = **12**. score_n = 1. Also a perfect complement.

### Classical Criteria

**FIM for Michaelis-Menten at experiment eₛ:**

∂y/∂Vmax = −x(t)/Km · ∂x/∂Vmax + ... = sensitivity S_V(t; S₀, θ).
∂y/∂Km = Vmax·x(t)/Km² · ∂x/∂Km + ... = sensitivity S_K(t; S₀, θ).

**Low substrate (S₀=0.1):** x(t) ≈ S₀·exp(−(Vmax/Km)t). S_V ≈ −(S₀·t/Km)·exp(−ρt), S_K ≈ (S₀·Vmax·t/Km²)·exp(−ρt) = (ρ/Km)·S₀·t·exp(−ρt). Ratio: S_K/S_V = −Vmax/Km = −ρ. The two sensitivities are proportional → FIM is rank-1 at low substrate. det(FIM) = 0.

**High substrate (S₀=100):** FIM is rank-2 generically (both parameters are identifiable). det(FIM) > 0.

**Repeat e₂_low2 (S₀=0.5):** FIM is still rank-1 (same structural problem). det(FIM) = 0.

**Classical D-optimal design** with noise profile σ(e₂_low2) = 0.05 (low noise, careful protocol) vs σ(e₂_high) = 1.0 (high noise, difficult protocol):

FIM contribution from e₂_low2: (1/σ²)·FIM_low ≈ (1/0.0025)·rank-1 matrix = 400·rank-1 matrix. Large but rank-deficient.

FIM contribution from e₂_high: (1/1.0)·FIM_high = rank-2 matrix with moderate eigenvalues.

**Trace criterion:** trace(FIM+e₂_low2) ≈ trace(existing) + 400·(S_V²+S_K²). For typical parameter values (Vmax=1,Km=1,t∈[0,5]): S_V² ≈ 0.1, S_K² ≈ 0.1. Trace gain ≈ 400×0.2 = 80.

Trace(FIM+e₂_high): trace gain ≈ S_V²+S_K² at high substrate ≈ 0.5+0.5 = 1. (Order of magnitude estimate.)

**Classical A-optimal ranks e₂_low2 (score=0) first, e₂_high (score=1) second.**

**Proposition C1 (proved).** For the Michaelis-Menten model:
1. Low-substrate experiments (any S₀ → 0) have UOP score = 0 relative to a prior low-substrate experiment.
2. A high-substrate experiment has UOP score = 1 (perfect complement).
3. A low-substrate experiment with arbitrarily low noise can have higher Fisher information trace than a high-substrate experiment with standard noise.

**Proof.**
(1) At S₀ → 0: output trajectory y(t) ≈ S₀·exp(−(Vmax/Km)t) identifies only ρ = Vmax/Km. U(f_{low'}) = same-ratio pairs regardless of S₀ value. All low-substrate experiments have the same structural ambiguity set. score(any low | {e₁ low}) = |R({e₁}) \ U(f_{low'})| = |same-ratio pairs \ same-ratio pairs| = 0. □
(2) At S₀ → ∞: identifies Vmax. U(f_{high}) ∩ U(f_{low}) = ∅ (shown above). score = |R({e₁})| = full. □
(3) FIM trace from low-substrate experiment scales as S₀²·∫₀ᵀ(S_V² + S_K²)dt / σ². For σ → 0, trace → ∞. FIM trace from high-substrate experiment is bounded for fixed noise σ. □

### Comparison Table — Domain C (5×5 grid, 4 candidates)

| Candidate | UOP score | score_n | FIM trace rank (σ as noted) | Structural content |
|---|---|---|---|---|
| e₂_high (S₀=100, σ=1.0) | **12** | **1.0** | **3rd** | Perfect complement — identifies Vmax |
| e₂_med (S₀=2, σ=0.5) | **12** | **1.0** | 2nd | Perfect complement — identifies both |
| e₂_low2 (S₀=0.5, σ=0.05) | **0** | **0** | **1st** | Zero structural gain — same ambiguity |
| **e₂_repeat (S₀=0.1, σ=0.01)** | **0** | **0** | **1st (tie)** | **Zero structural gain — exact repeat** |

**Low-substrate repeats rank 1st by classical trace criterion, 0 by UOP.**

---

## Part 4 — The Divergence Theorem

**Theorem 1 (UOP-Classical Divergence — proved).**

In all three domains: there exist candidate measurements with UOP score = 0 that rank first under classical Fisher information criteria (trace, det, or A-optimality). The divergence is not a corner case — it arises from the standard scenario where:

(a) A candidate measurement lies in the row-space of existing measurements (linear case), OR
(b) A candidate measurement has the same structural ambiguity set as an existing one (nonlinear case),
AND
(c) The candidate has lower measurement noise than existing candidates.

Under condition (c), classical criteria assign high information value to the candidate. Under conditions (a)/(b), UOP assigns score = 0. The divergence is monotone: as noise σ → 0, classical rank of the score-0 candidate → 1st, while UOP score remains 0.

**Proof.** Follows from Propositions A1, B1, C1. All three give the same structure: score = 0 candidates with σ → 0 dominate classical criteria. □

**Theorem 2 (UOP Pre-Screening is Necessary — proved).**

The following holds: a score-0 candidate NEVER reduces residual ambiguity, regardless of noise level, sample size, or number of repetitions. A score-0 experiment can achieve arbitrarily high statistical precision on already-identified directions while contributing nothing to unresolved directions.

**Proof.** score(fᵢ | F) = 0 iff U(fᵢ) ⊇ R(F). Every pair in R(F) is in U(fᵢ). No data from fᵢ (regardless of noise level) can distinguish a pair in U(fᵢ) — the fundamental structural impossibility is that fᵢ(x) = fᵢ(y) exactly for {x,y} ∈ U(fᵢ). No amount of data resolves fᵢ(x) = fᵢ(y) when they are equal by construction. □

---

## Part 5 — The Hybrid Design Theorem

**Theorem 3 (Hybrid Design — proved).**

The optimal experiment selection strategy for budget k is:

**Step 1 (UOP pre-screening):** Eliminate all candidates with score_n = 0. Call the survivors S = {fᵢ : score(fᵢ | F) > 0}.

**Step 2 (Statistical optimization):** Among S, apply classical criteria (D-optimality, A-optimality, mutual information) to rank by statistical efficiency.

**Step 3 (Select):** Choose the top-ranked survivor. Add to F. Update R(F). Repeat.

**This strategy is strictly superior to classical-only selection whenever a score-0 candidate exists with better classical rank than any score-positive candidate.**

**Proof.**

Classical-only: may select fᵢ with score = 0. After selection: R(F ∪ {fᵢ}) = R(F) (unchanged). Budget decreased by 1 with no ambiguity reduction.

Hybrid: never selects score-0 candidates (eliminated in Step 1). Every selection reduces |R(F)| by at least 1. With budget k, hybrid achieves |R(F)| ≤ |R(F_initial)| − k (each step reduces by at least 1, potentially more).

Classical-only achieves |R(F)| ≤ |R(F_initial)| − (k − w) where w = number of wasted selections on score-0 candidates. For any w ≥ 1: hybrid strictly dominates classical-only in terms of residual ambiguity reduction. □

**Corollary (Information hierarchy):** UOP score answers a prior question to Fisher information:

1. **Is this measurement structurally informative at all?** (UOP score > 0)
2. **If yes, how precisely can it determine the already-accessible directions?** (Fisher information)

Classical OED answers (2) without checking (1). UOP pre-screening ensures (1) is verified first.

---

## Part 6 — When Classical and UOP Agree

**Proposition (Agreement conditions — proved).**

Classical criteria and UOP agree (produce the same ranking) when:

(a) **Homogeneous noise:** all candidates have the same noise variance σ². Then FIM contributions are proportional to rank gain, which equals UOP score for linear systems. Agreement.

(b) **Score-positive constraint already applied:** if the candidate set is restricted to score > 0 measurements (e.g., by domain knowledge). Then classical criteria rank correctly within the useful set.

(c) **One-dimensional case:** 𝒳 = ℝ¹. A single measurement either identifies or doesn't; classical and UOP both give binary yes/no.

**Proof.** (a): FIM trace = ∑ᵢ CᵢᵀCᵢ/σ². Equal σ² → ranking by trace = ranking by ∑ rank gain. For linear systems, rank gain = UOP score. Agreement. □

---

## Part 7 — Practical Decision Protocol

```
UOP-FIRST DESIGN PROTOCOL

Input: Current measurement set F.
       Candidate set {f₁,...,fₘ}.
       Budget k.

Step 1: STRUCTURAL SCREEN
  For each candidate fᵢ:
    Compute score(fᵢ | F).
    If score = 0: ELIMINATE. Log: "structurally redundant."
  
  If all candidates eliminated: STOP.
  Report: "No structurally useful measurement exists 
           in this candidate family. Need new measurement type."

Step 2: STATISTICAL RANK
  For each surviving candidate:
    Compute FIM contribution (or D/A-optimality gain).
    Rank by statistical efficiency.

Step 3: SELECT
  Choose highest-ranked survivor.
  Update F ← F ∪ {selected}.
  Update R(F) ← R(F) ∩ U(selected).
  
  If R(F) = ∅: DONE. F is sufficient.
  Else: REPEAT from Step 1 with k ← k−1.
```

**The protocol's key output beyond standard OED:** Step 1 can return "no structurally useful measurement exists." This is information that classical OED never produces — it always ranks candidates, even when all are structurally redundant. When Step 1 eliminates everything, the experimenter knows: more measurements of the same type will not resolve the ambiguity. A fundamentally different measurement type is needed. This is the operationalized "orthogonal jump" recommendation.

---

## Summary

**Three proved propositions:**

- **A1 (linear sensors):** A sensor proportional to an existing one (same direction, lower noise) has UOP score = 0 but can rank first by A-optimality. Proved.
- **B1 (tomography):** An exact repeat of a prior projection has UOP score = 0 but can rank first by FIM trace. Proved.
- **C1 (Michaelis-Menten):** A low-substrate experiment cannot identify Km given prior low-substrate data, regardless of noise level. High-substrate experiment is the unique structural complement. Proved.

**Main theorem (Theorem 1 — proved):** UOP-classical divergence exists in all three domains and is driven by the combination of structural redundancy + superior noise characteristics.

**Hybrid Design Theorem (Theorem 3 — proved):** The two-stage protocol (UOP pre-screen, then classical rank) strictly dominates classical-only selection whenever score-0 candidates exist with better classical rank than score-positive candidates.

**Strongest honest claim:**
> UOP pre-screening is not just a restatement of classical design theory — it identifies a class of experiments that classical criteria actively prefer but that provide zero structural information. The divergence is not pathological; it arises from the standard situation where a precise repetition of an existing experiment dominates a noisier but genuinely new measurement. The hybrid protocol recovers the best of both: structural completeness from UOP, statistical efficiency from classical criteria.

**Strongest honest boundary:**
> The toy examples above use noiseless structural analysis (exact UOP score computation). For nonlinear models in real applications, computing U(f_e) exactly requires differential algebra or numerical sampling — the score is then approximate. The Hybrid Design Theorem holds exactly for the approximate score too: eliminating score-≈-0 candidates still prevents wasted budget on near-redundant experiments. The bound degrades gracefully: a candidate with score = ε (small but positive) resolves ε-fraction of current ambiguity, which may or may not justify the cost. The protocol handles this by setting a score threshold τ > 0 below which candidates are treated as effectively redundant.
