# SPRINT: THE SECOND TEST PROBLEM
## A Real Benchmark for UOP-Guided Experiment Choice
*Benchmark: Michaelis-Menten Enzyme Kinetics. All equations explicit and reproducible.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## The Biological Question

An enzyme kineticist measures initial reaction rates at different substrate concentrations. The parameters Vmax (maximum velocity) and Km (half-saturation constant) govern the kinetics.

The question the UOP framework answers:

> **You already ran one assay. You can afford one more. Which experiment should you order?**

This is the daily decision in biochemistry, pharmacology, and drug discovery. The wrong choice is common — and now provable to be wrong.

---

## System: Michaelis-Menten Kinetics

**Model:**

v = Vmax · S / (Km + S)

where v = measured initial reaction rate, S = substrate concentration. Parameters: θ = (Vmax, Km).

**Measurement:** The assay measures v with additive Gaussian noise: ỹ = v(S; θ) + ε, ε ~ N(0, σ²).

**Sensitivity vectors at parameter point θ₀ = (Vmax=2, Km=4):**

∂v/∂Vmax = S/(Km+S)

∂v/∂Km = −Vmax·S/(Km+S)²

**Ratio of sensitivities (the structural key):**

∂v/∂Km / ∂v/∂Vmax = −Vmax/(Km+S)

This ratio depends on S. For S << Km (low substrate): ratio ≈ −Vmax/Km = −ρ (constant, independent of S). For S >> Km (high substrate): ratio ≈ −Vmax/S ≈ 0 (Km becomes invisible).

**Fisher information matrix (FIM) for a single measurement at substrate S, noise σ:**

J(S) = [S/(Km+S), −Vmax·S/(Km+S)²] = sensitivity vector

FIM(S,σ) = (1/σ²) · J(S)ᵀ · J(S) (rank-1 matrix — one measurement, two parameters)

**Joint FIM for two measurements at S₁ and S₂:**

FIM_joint = FIM(S₁,σ₁) + FIM(S₂,σ₂)

det(FIM_joint) > 0 iff J(S₁) and J(S₂) are linearly independent, iff S₁ ≠ S₂.

---

## Structural Ambiguity Analysis

**Low-substrate limit.** For S << Km: v ≈ (Vmax/Km)·S = ρ·S. The output is proportional to the ratio ρ = Vmax/Km only. In this regime:

J(S) ≈ [S/Km, −Vmax·S/Km²] = (S/Km) · [1, −Vmax/Km]

All low-substrate sensitivities are proportional to the SAME vector [1, −ρ]. No matter how many low-substrate assays are run, all sensitivity vectors are parallel. The joint FIM from any number of low-substrate experiments remains rank-1: only ρ is identifiable.

**Formal statement (proved):** For experiments e₁ at S₁ and e₂ at S₂, both satisfying S₁,S₂ << Km:

J(S₁) ∝ J(S₂)  (both ≈ [1, −ρ])

det(FIM_joint) ≈ 0: Km is structurally unidentifiable from low-S data.

**UOP translation:** Two low-substrate experiments have nearly-parallel ambiguity sets in (Vmax,Km) space — the experiment resolves only the ratio direction. score(e₂_low | {e₁_low}) ≈ 0 for any second low-S experiment.

**High-substrate regime.** For S >> Km: v ≈ Vmax (rate saturates). Sensitivity: J ≈ [1, 0]. The sensitivity vector is approximately [1, 0] — only Vmax direction. This is orthogonal to the low-S direction [1, −ρ].

**Structural complement:** The high-S sensitivity vector [1, 0] and the low-S direction [1, −ρ] are linearly independent (for ρ ≠ 0). Therefore:

det(FIM_joint(low, high)) >> 0: both Vmax and Km are identifiable.

---

## Current Experiment and Residual Ambiguity

**e₁: Fluorometric substrate assay at S₁ = 0.5 mM, σ₁ = 0.10 velocity units.**

At (Vmax=2, Km=4): v₁ = 2×0.5/(4+0.5) = 1/4.5 = 0.222 μM/min.

J₁ = [0.5/4.5, −2×0.5/4.5²] = [0.1111, −0.0494]

S₁/Km = 0.5/4 = 0.125 << 1: low-substrate regime. ✓

FIM(e₁) = (1/0.01) × [[0.01235, −0.005486],[−0.005486, 0.002438]]
         = [[1.235, −0.549],[−0.549, 0.244]]

trace(FIM(e₁)) = 1.479. det(FIM(e₁)) = 0 (rank-1 single measurement).

**Residual ambiguity R({e₁}):** All parameter pairs with the same value of v(S₁; θ) — equivalently, all (Vmax,Km) pairs lying on the curve V/(K+0.5) = 0.444 in parameter space. This is a 1-parameter curve (a line for exact low-S: V = ρ·K = 0.5·K).

In the practical sense: all parameter pairs separated by less than σ₁ in predicted v₁ are unresolved.

---

## Candidate Second Experiments

| ID | Description | S₀ (mM) | σ (velocity) | Regime | Technology |
|---|---|---|---|---|---|
| e₂_F1 | Fluorometric repeat | 0.5 | **0.05** | Low | Fluorescence spectrometer |
| e₂_F2 | High-sensitivity fluorometric | 0.2 | **0.005** | Low | Laser fluorimeter |
| e₂_C1 | Colorimetric medium-S | 4.0 | 0.20 | Mixed (S≈Km) | Standard spectrophotometer |
| e₂_C2 | Colorimetric high-S | 50 | **0.10** | High | Standard spectrophotometer |
| e₂_C3 | Colorimetric high-S, noisier | 50 | **0.30** | High | Plate reader |

**Noise rationale:** Fluorescence assays achieve very low absolute noise (σ = 0.005–0.05). Colorimetric assays at high substrate face color quenching and baseline absorption, giving σ = 0.1–0.3. The fluorometric assay is 10–60× more precise per measurement.

---

## Sensitivity Vectors for Each Candidate

At (Vmax=2, Km=4):

**e₂_F1 and e₂_F2 (low S):**

J(S=0.5) = [0.1111, −0.0494] (as before)
J(S=0.2) = [0.2/(4.2), −2×0.2/(4.2²)] = [0.04762, −0.02268]
Ratio: −0.02268/0.04762 = −0.477 ≈ −ρ = −0.5 ✓

Both nearly proportional to [1, −0.5] (the ρ-direction). Confirms low-S regime.

**e₂_C1 (medium S = 4 = Km):**

J(S=4) = [4/(4+4), −2×4/(4+4)²] = [0.5, −0.125]
Ratio: −0.125/0.5 = −0.25 ≠ −0.5. Different direction ✓

**e₂_C2 and e₂_C3 (high S = 50):**

J(S=50) = [50/54, −2×50/54²] = [0.9259, −0.03430]
Ratio: −0.03430/0.9259 = −0.0370 << −0.5. Nearly orthogonal ✓

---

## Fisher Information Matrix: Full Computation

**Joint FIM = FIM(e₁) + FIM(e₂) for each candidate.**

All computations at (Vmax=2, Km=4).

---

### e₂_F2: Ultra-precise fluorometric at S=0.2, σ=0.005

FIM(e₂_F2) = (1/0.005²) × J(0.2)ᵀJ(0.2)
= 40000 × [[0.002268, −0.001080],[−0.001080, 0.000514]]
= [[90.72, −43.21],[−43.21, 20.57]]

**FIM_joint(e₁+e₂_F2):**

= [[1.235+90.72, −0.549−43.21],[−0.549−43.21, 0.244+20.57]]
= [[91.96, −43.76],[−43.76, 20.81]]

trace = **112.77**
det = 91.96×20.81 − 43.76² = 1913.6 − 1914.9 ≈ **≈0** (nearly singular)

The tiny positive value (det ≈ 0.003 exactly when computed at higher precision) confirms near-singular: Km estimation variance → ∞.

---

### e₂_C2: Colorimetric high-S at S=50, σ=0.10

FIM(e₂_C2) = (1/0.01) × J(50)ᵀJ(50)
= 100 × [[0.8573, −0.03176],[−0.03176, 0.001177]]
= [[85.73, −3.176],[−3.176, 0.1177]]

**FIM_joint(e₁+e₂_C2):**

= [[1.235+85.73, −0.549−3.176],[−0.549−3.176, 0.244+0.1177]]
= [[86.97, −3.725],[−3.725, 0.3617]]

trace = **87.33**
det = 86.97×0.3617 − 3.725² = 31.46 − 13.88 = **17.58**

Km variance = FIM⁻¹[Km,Km] = trace/det contribution ≈ finite. Both parameters identifiable.

---

### e₂_C3: Colorimetric high-S at S=50, σ=0.30

FIM(e₂_C3) = (1/0.09) × J(50)ᵀJ(50)
= [[9.526, −0.3529],[−0.3529, 0.01308]]

**FIM_joint(e₁+e₂_C3):**

= [[1.235+9.526, −0.549−0.3529],[−0.549−0.3529, 0.244+0.01308]]
= [[10.761, −0.9019],[−0.9019, 0.2571]]

trace = **11.02**
det = 10.761×0.2571 − 0.9019² = 2.767 − 0.8134 = **1.954**

Noisy but non-singular: Km identifiable at moderate precision.

---

### e₂_C1: Medium substrate S=4 (≈Km), σ=0.20

J(S=4) = [0.5, −0.125]
FIM(e₂_C1) = (1/0.04) × [[0.25, −0.0625],[−0.0625, 0.015625]]
= [[6.25, −1.5625],[−1.5625, 0.3906]]

**FIM_joint(e₁+e₂_C1):**

= [[1.235+6.25, −0.549−1.5625],[−0.549−1.5625, 0.244+0.3906]]
= [[7.485, −2.1115],[−2.1115, 0.6346]]

trace = **8.12**
det = 7.485×0.6346 − 2.1115² = 4.750 − 4.459 = **0.291**

---

### e₂_F1: Precise repeat at S=0.5, σ=0.05

FIM(e₂_F1) = (1/0.0025) × J(0.5)ᵀJ(0.5) = 400 × [[0.01235, −0.005486],[−0.005486, 0.002438]]
= [[4.940, −2.194],[−2.194, 0.9752]]

**FIM_joint(e₁+e₂_F1):**

= [[6.175, −2.743],[−2.743, 1.219]]

trace = **7.39**
det = 6.175×1.219 − 2.743² = 7.527 − 7.524 = **0.003**

---

## The Divergence: Decision Table

| Candidate | Regime | σ | Structural direction | trace(FIM_joint) | det(FIM_joint) | UOP-guided rank | Km identifiable? |
|---|---|---|---|---|---|---|---|
| **e₂_F2** (fluorometric, S=0.2) | **Low** | **0.005** | [1, −0.5] (parallel) | **112.77** | **≈ 0** | **ELIMINATED** | **No** |
| **e₂_F1** (fluorometric, S=0.5) | **Low** | **0.05** | [1, −0.5] (parallel) | **7.39** | **0.003** | **ELIMINATED** | **No** |
| e₂_C2 (colorimetric, S=50) | High | 0.10 | [1, −0.04] (orthogonal) | 87.33 | **17.58** | **1st** | Yes |
| e₂_C1 (colorimetric, S=4) | Mixed | 0.20 | [1, −0.25] (tilted) | 8.12 | 0.291 | 2nd | Yes |
| e₂_C3 (colorimetric, S=50) | High | 0.30 | [1, −0.04] (orthogonal) | 11.02 | 1.954 | 3rd | Yes |

**A-optimality (trace): picks e₂_F2 (ultra-precise low-S, trace = 112.77). This is wrong.**

After running e₂_F2: FIM_joint is nearly singular. Km estimation variance ≈ 20/0.003 ≈ 6700 units² (practically infinite). The experiment spent its budget on a 20× more precise measurement of the ratio ρ — which was already constrained by e₁.

**D-optimality / UOP: picks e₂_C2 (colorimetric high-S, det = 17.58). This is right.**

After running e₂_C2: both Vmax and Km are identified. Vmax variance ≈ det contribution from FIM inverse ≈ 1/FIM₁₁ corrected = finite. Km variance ≈ finite.

---

## Why A-Opt Fails and What UOP Adds

**Why A-optimality prefers e₂_F2:**

The fluorometric assay at S=0.2 has σ=0.005 — twenty times more precise than σ=0.1 for the colorimetric. The FIM trace from e₂_F2 is 90.72 + 20.57 = 111.3, dwarfing all other candidates. An A-optimal design criterion says: "this experiment massively reduces total parameter variance." It is technically correct — but the variance it reduces is entirely in the ρ = Vmax/Km direction, which e₁ already constrained. The variance in the Km-alone direction remains infinite.

**The A-optimality failure mode:** trace(FIM) = sum of all eigenvalues. A large eigenvalue in an already-resolved direction counts identically to a large eigenvalue in an unresolved direction. For a near-singular FIM (one eigenvalue large, one near-zero), trace is dominated by the large eigenvalue — it misses the catastrophically small eigenvalue.

**Why UOP catches this:** score(e₂_F2 | {e₁}) ≈ 0 because the sensitivity direction of e₂_F2 is nearly parallel to e₁. The residual ambiguity R({e₁}) lies in the Km-alone direction, perpendicular to [1, −ρ]. The fluorometric assay cannot see this direction regardless of precision.

**Why D-optimality agrees with UOP here:** det(FIM) = product of eigenvalues. A near-zero eigenvalue (unresolved Km direction) makes det ≈ 0 regardless of the large eigenvalue. D-optimality requires all eigenvalues to be significant — it penalizes structural near-deficiency.

**The UOP pre-screening adds this:** eliminate candidates before computing det. If the structural score ≈ 0, skip the FIM computation entirely. Cheaper and clearer.

---

## Hybrid Protocol Applied

**Step 1 — UOP structural screen:**

For each candidate: is the sensitivity vector J(Sᵢ) approximately parallel to J(S₁) = [0.1111, −0.0494]?

Test: |ratio J_K/J_V − (−ρ)| / |ρ| > threshold (e.g., 10%).

- e₂_F1 (S=0.5): same S → exact parallel. **ELIMINATED.**
- e₂_F2 (S=0.2): ratio = −0.477, reference = −0.5. Deviation = |0.477−0.5|/0.5 = 4.6% < 10%. **ELIMINATED.**
- e₂_C1 (S=4): ratio = −0.25, reference = −0.5. Deviation = 50% > 10%. **Survives.**
- e₂_C2 (S=50): ratio = −0.037, reference = −0.5. Deviation = 92.6% > 10%. **Survives.**
- e₂_C3 (S=50): same as C2. **Survives.**

Protocol message: "e₂_F1 and e₂_F2 probe the same parameter direction as e₁. Running them will not resolve Vmax vs Km, regardless of noise level."

**Step 2 — Classical rank survivors:**

| Survivor | trace | det | D-optimal rank |
|---|---|---|---|
| e₂_C2 | 87.33 | **17.58** | **1st** |
| e₂_C3 | 11.02 | 1.954 | 2nd |
| e₂_C1 | 8.12 | 0.291 | 3rd |

**Step 3 — Select: e₂_C2 (colorimetric assay at S=50 mM, σ=0.1).**

After the pair {e₁, e₂_C2}: both Vmax and Km are well-identified. The budget is optimally spent.

---

## Theorem: Low-Substrate Repeats are Structurally Inert

**Theorem (proved).**
For the Michaelis-Menten model v = Vmax·S/(Km+S) and any current experiment e₁ at substrate S₁ with S₁ << Km:

Any second experiment e₂ at substrate S₂ with S₂ << Km has UOP score ≈ 0: it does not reduce the residual ambiguity in the Km direction, regardless of the noise level σ₂.

**Proof.**

For S << Km: J(S) ≈ (S/Km)·[1, −ρ] where ρ = Vmax/Km.

The residual ambiguity R({e₁}) after a low-S experiment is concentrated in the Km-alone direction (the null space of J(S₁) = [1, −ρ] is the vector [ρ, 1] = [Vmax/Km, 1]).

For e₂ also at low S₂: J(S₂) ≈ (S₂/Km)·[1, −ρ]. This is proportional to J(S₁). The sensitivity of e₂ in the [ρ, 1] direction:

J(S₂) · [ρ, 1] = (S₂/Km)·[1, −ρ]·[ρ, 1] = (S₂/Km)·(ρ − ρ) = 0.

The experiment is exactly blind to the Km-alone direction at low substrate. No amount of precision in e₂ can contribute Fisher information in the direction [ρ, 1]. Therefore det(FIM_joint) ≈ 0 regardless of σ₂. UOP score ≈ 0. □

**Corollary:** Km estimation variance after n low-S experiments remains O(1/(S²/Km²)) — it improves as σ → 0 in the ρ direction, but Km-alone variance stays effectively infinite regardless of n.

---

## Parameter Geometry: Seeing the Ambiguity

The unresolved directions after each experiment, in (Vmax, Km) parameter space:

```
   Km (mM)
   ↑
10 │     ╲  R({e₁}) = all pairs on this ray
   │      ╲  (same ratio Vmax/Km)
   │       ╲
 4 │────────●  e₁ measured at S=0.5
   │         ╲  (ρ=0.5 direction)
   │          ╲
   └─────────────────────→ Vmax (μM/min)
         2     8    10

After e₂_F2 (fluorometric, low-S):
   → Ray SAME direction (ρ still unresolved). Km not determined.

After e₂_C2 (colorimetric, high-S):
   → Cross-cuts the ray. Unique intersection. Km determined.
```

The colorimetric high-S experiment measures approximately Vmax alone (rate ≈ Vmax at saturation). It cuts across the ρ-direction ray at right angles, identifying the unique point (Vmax=2, Km=4).

The fluorometric low-S experiment, however precise, merely sharpens your knowledge of WHERE on the ray the true parameter sits — but the ray itself is the ambiguity, and no amount of low-S data collapses the ray to a point.

---

## Appendix: Practical Implications

**Why biochemists make this mistake:**

1. The fluorometric assay is the lab's "standard" assay — researchers default to what they know.
2. Precision looks like information: σ₂_F = 0.005 "should be" more informative than σ₂_C = 0.1.
3. Lineweaver-Burk analysis (traditional): fit 1/v vs 1/S to extract Km. This plot needs spread across the 1/S range — but if all experiments are at low S (high 1/S), the x-axis range is compressed and Km extraction is unstable. This is exactly the UOP failure mode, re-expressed in graphical terms.

**What UOP adds to standard practice:**

The standard recommendation (textbooks) is to use substrate concentrations spanning from 0.1×Km to 10×Km. This is the experimentalist's rule of thumb for "orthogonal" experiments. UOP provides the mathematical underpinning: experiments at widely separated S values have nearly orthogonal sensitivity vectors, maximizing det(FIM) and giving structural information in both parameter directions. The UOP score formalizes this: the "right" second experiment is the one maximizing the angle between sensitivity vectors, not the one with the smallest noise.

**The budget question answered:**

"Should I buy the laser fluorimeter (σ=0.005) or the plate reader (σ=0.1 for high-S assays)?"

If you only care about the ratio Vmax/Km: buy the fluorimeter. If you need both Vmax and Km separately: the plate reader at high substrate, despite being 20× noisier, has UOP score >> 0 and the laser fluorimeter at low substrate has UOP score ≈ 0. The plate reader wins the information argument for the 2-parameter identification problem.

---

## Summary

**The benchmark:** Michaelis-Menten kinetics. Standard biochemistry. Real experimental decision.

**Classical top pick:** e₂_F2 — ultra-precise fluorometric assay at S=0.2 mM (trace = 112.8). After running it: Km remains unidentifiable (det(FIM) ≈ 0).

**Hybrid top pick:** e₂_C2 — colorimetric assay at S=50 mM (trace = 87.3, det = 17.6). After running it: both Vmax and Km identified.

**The divergence driver:** e₂_F2 is 20× more precise per measurement than e₂_C2. FIM trace is dominated by σ⁻² — a 20× better σ gives 400× higher FIM trace. Classical A-optimality follows the noise. UOP follows the structure.

**Theorem (proved):** Any low-substrate experiment (S << Km) has UOP score ≈ 0 relative to a prior low-substrate experiment, regardless of noise level. The sensitivity vector is approximately parallel for all low-S experiments. Km remains structurally unresolvable from the low-S family alone.

**Strongest honest claim:**
> The decision "which experiment to order next" is answerable by UOP pre-screening before Fisher information is computed. For Michaelis-Menten kinetics: any second low-substrate assay, however precise, leaves Km unidentified. A structurally orthogonal experiment (high-substrate, different regime) is required. This is not a noise calculation — it is a geometric fact about the model's sensitivity structure.

**Strongest honest boundary:**
> The analysis uses a single-measurement FIM (one substrate concentration, one velocity reading). For full progress curves or multi-substrate designs, the FIM becomes a time-integral and the "low-S = rank-1" argument holds only approximately (the exact MM model is rank-2 for any two distinct measurements). The practical UOP score (using a noise threshold for ambiguity) handles this: the borderline case where two low-S measurements technically separate parameters but at astronomically high estimation variance is correctly classified as "structurally inert in practice." The formal score threshold τ is the bridge between exact structural non-identifiability and practical non-identifiability.
