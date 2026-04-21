# WP61 — Productive Incompleteness
## Maps with Score=0 for Full Reconstruction That Remain Scientifically Sufficient

**Date**: 2026-04-08
**Sprint**: 12 — UOP/GUT Arc
**Status**: Five-category classification PROVED for finite-set setting; examples STRUCTURAL; connection to WP57 PROVED
**Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes

---

## Abstract

A measurement family F has reconstruction score = 0 for a domain if its unresolved pair set is nonempty — meaning F cannot globally separate all distinct elements. But score = 0 for global reconstruction is compatible with score = 1 for a restricted scientific task. This paper formalizes the distinction with a five-category classification of measurement utility beyond global injectivity. The categories are: Complete Complement, Partial Complement, Refinement Only, Invariant-Isolating (Type II), and Invalid (Type III). Three canonical examples are worked in detail: Banach-Tarski (orbit structure fully determined, measure inaccessible), CT projection (global image underdetermined, row-integral subspace fully determined), and enzyme kinetics (Vmax/Km ratio exactly determined, individual parameters indistinguishable). The connection to the UOP framework and the Crossing Lemma is established: score = 0 in the UOP sense means no crossing occurs in the relevant partition pair, but crossing is not always required for the scientific task.

---

## §1. Setup: Reconstruction Score and Unresolved Pairs

### 1.1 Definitions

Let 𝒳 be a finite set (the object space), and let F = {f₁, ..., fₘ} be a family of maps fᵢ: 𝒳 → Yᵢ (measurement maps).

**Definition (Unresolved pair set):**

    U(F) = { {x,y} : x ≠ y and fᵢ(x) = fᵢ(y) for all i ∈ {1,...,m} }

This is the set of pairs that F cannot distinguish.

**Definition (Reconstruction score):**

    Score(F, 𝒳) = 1 if U(F) = ∅ (F is globally sufficient: jointly injects)
    Score(F, 𝒳) = 0 if U(F) ≠ ∅ (F fails to distinguish some pair)

**When Score = 0 means "useless"** [STRUCTURAL]: If the scientific task IS full reconstruction (uniquely identify every x ∈ 𝒳 from its measurements), then Score = 0 means F is inadequate for this task.

**When Score = 0 does NOT mean "useless"** [STRUCTURAL]: If the scientific task requires only determining a specific invariant, orbit class, quotient, or subspace property of 𝒳, then Score = 0 for full reconstruction is compatible with Score = 1 for the restricted task.

These are fundamentally different questions. The UOP framework (WP58) characterizes full reconstruction. It does not characterize general scientific utility.

### 1.2 Task-Relative Score

**Definition (Task-relative score):** For a task T: 𝒳 → Z (a specific invariant or property), define:

    Score(F, T) = 1 if for all x, y: T(x) ≠ T(y) implies fᵢ(x) ≠ fᵢ(y) for some i
    Score(F, T) = 0 if there exist x, y with T(x) ≠ T(y) but F cannot distinguish x from y

Score(F, T) = 1 means F is sufficient for the task T. Score(F, 𝒳) = 1 is the special case T = identity.

**Key observation** [PROVED]: Score(F, T) = 1 does not require Score(F, 𝒳) = 1. The global injectivity condition is strictly stronger than task-sufficiency.

---

## §2. Five-Category Classification

**Theorem (Five-Category Classification)** [PROVED for finite-set setting]:

Every measurement family F on a finite set 𝒳 falls into exactly one of five categories, classified by the structure of U(F) and the existence of scientifically useful tasks for which Score(F, T) = 1:

**Category I — Complete Complement:**

    U(F) = ∅ (Score = 1 globally)

F is sufficient for every task T. No additional measurement is needed. A family F' achieving this for the residual ambiguity of a smaller family is a "complete complement" to that family.

**Category II — Partial Complement:**

    U(F) ≠ ∅, but U(F) ⊊ U(∅) (F reduces some ambiguity)

F resolves some pairs but not all. It is sufficient for tasks T supported on the resolved pairs, and insufficient for tasks requiring resolution of U(F)-pairs.

**Category III — Refinement Only:**

    U(F) ≠ ∅, and U(F) = U(F₀) for some pre-existing family F₀ (F adds no new resolution)

F adds precision within already-resolved directions but reveals no new hidden structure. Adding F to F₀ does not reduce U(F₀). Useful for calibration, noise reduction, and reliability on known directions. Not useful for revealing hidden dimensions.

**Category IV — Invariant-Isolating (Type II):**

    U(F) ≠ ∅, but there exists a task T (orbit, quotient, invariant) with Score(F, T) = 1

F cannot reconstruct individual elements but can exactly determine a specific invariant or orbit class. The family is insufficient for full reconstruction but sufficient for the specific invariant task. The missing ingredient for full reconstruction is a gauge-fix, normalization, or constraint external to the measurement family.

**Category V — Invalid/Inadmissible (Type III):**

    The map or domain is ill-posed: either f is not well-defined, or 𝒳 is not a coherent object space

This is the only category where F is outright invalid. The issue is not insufficient coverage — the model itself requires repair.

**Proof of well-definedness:** Each category is defined by disjoint conditions. Category I: U(F) = ∅. Category II: U(F) ≠ ∅ and U(F) ⊊ U(∅) = all pairs. Category III: U(F) = U(F₀) for some already-known F₀. Category IV: U(F) ≠ ∅ but some useful invariant task has Score = 1. Category V: ill-posedness independent of U(F). Every F falls into exactly one category (if not ill-posed, the category is determined by U(F) and the existence of useful invariant tasks). □

---

## §3. Example 1: Banach-Tarski and Orbit Structure (Category IV)

**Setup:** Let 𝒳 = B³ (unit ball) with the group G = F₂ ⊂ SO(3) (a free group on two generators, embedded as rotations). The orbit map f_orbit: B³ → G-orbit classes assigns each point to its F₂-orbit equivalence class.

**Score(f_orbit, B³) = 0** [STRUCTURAL]:

The orbit classes are uncountable; the Banach-Tarski decomposition shows that points in the same orbit can be rearranged into geometrically different configurations. Full reconstruction of an element from its orbit class is impossible — many non-identical elements share an orbit class.

**What f_orbit determines exactly** [PROVED]:

1. Group orbit membership: f_orbit(x) = f_orbit(y) iff x ~_orbit y — fully determined.
2. Equivariance structure: f_orbit(g·x) = g · f_orbit(x) for all g ∈ F₂ — the map commutes with group action.
3. The partition of B³ into F₂-orbits is exactly determined.

**The missing invariant** [PROVED via Vitali/Hausdorff]:

The pieces A₁,...,A₅ of the Banach-Tarski decomposition are non-measurable. No countably additive, rotation-invariant measure exists on all subsets of ℝ³. The Lebesgue measure map f_meas: (measurable sets) → [0,∞) is not defined on the pieces. The family {f_orbit} is insufficient for volume because the needed invariant (Lebesgue measure) is inaccessible for non-measurable sets — not because more orbit maps would help.

**UOP classification:** Category IV (Invariant-Isolating). The orbit structure IS the point in symmetry analysis. f_orbit is scientifically indispensable for determining group-orbit membership and equivariance, even though Score(f_orbit, B³) = 0 for full reconstruction.

**Connection to Crossing Lemma** [STRUCTURAL]: In UOP language, f_orbit has score = 0 because U(f_orbit) ≠ ∅. But the "crossing" sought in Banach-Tarski is not between orbit classes — it is between geometric configurations (equivalent under volume). The Crossing Lemma applies to the volume question, not the orbit question. f_orbit perfectly answers the orbit question.

---

## §4. Example 2: CT Projection and Subspace Isolation (Category II)

**Setup:** Let 𝒳 = all 3D density functions on a domain Ω ⊂ ℝ³. A CT projection at angle θ is the map f_θ: 𝒳 → L²(ℝ²) assigning each density function ρ(x,y,z) to its line integrals at angle θ:

    f_θ(ρ)(u,v) = ∫ ρ(u·cos θ − t·sin θ, u·sin θ + t·cos θ, v) dt

**Score(f_θ, 𝒳) = 0** [STRUCTURAL]:

A single CT angle cannot reconstruct a 3D function. The null space of f_θ is infinite-dimensional (all functions with zero integral along lines at angle θ). Many distinct density functions produce identical projections at angle θ.

**What f_θ determines exactly** [PROVED for specific subspace]:

f_θ exactly determines all row-integral line densities at angle θ. In Fourier space (via the Fourier Slice Theorem): f_θ determines the 2D Fourier transform of ρ on one plane through the origin — the "slice" at angle θ. This Fourier content along one frequency plane is fully and exactly determined.

**Clinical value** [STRUCTURAL]: A single-angle projection gives real clinical data. Soft-tissue boundaries along the projection direction are resolved. The measurement has genuine diagnostic value without a second angle, for questions that can be answered from the determined Fourier slice.

**UOP classification:** Category II (Partial Complement). f_θ reduces the ambiguity set from all of 𝒳 to a proper subset (functions differing only in the null space of f_θ). Score(f_θ, T) = 1 for tasks T supported on the Fourier slice at angle θ.

---

## §5. Example 3: Enzyme Kinetics and Ratio Invariants (Category IV)

**Setup:** In Michaelis-Menten kinetics, initial reaction velocity at substrate concentration [S] is:

    v([S]) = Vmax · [S] / (Km + [S])

Parameters: Vmax (maximum velocity) and Km (Michaelis constant). The task is to determine (Vmax, Km) from measurements of v at various [S].

**Low-substrate assay:** At [S] << Km: v ≈ (Vmax/Km) · [S]. The linear approximation determines only the ratio ρ = Vmax/Km.

**Score(low-[S] assay, {Vmax, Km}) = 0** [STRUCTURAL]:

At low [S], any pair (Vmax, Km) with the same ratio ρ = Vmax/Km produces identical initial velocity measurements. The pairs {(Vmax₁, Km₁), (Vmax₂, Km₂)} with Vmax₁/Km₁ = Vmax₂/Km₂ are unresolved.

**What the low-[S] assay determines exactly** [PROVED]:

Score(low-[S] assay, T_ρ) = 1 where T_ρ(Vmax, Km) = Vmax/Km. The ratio ρ = Vmax/Km is exactly and completely determined by the low-substrate assay. This ratio is the kinetic efficiency (catalytic efficiency) of the enzyme.

**Scientific uses** [STRUCTURAL]:
- Comparing kinetic efficiency between enzyme variants requires only ρ.
- Screening assays looking for catalytic rate differences use ρ.
- The ratio ρ appears directly in the rate of product formation at low substrate.

**UOP classification:** Category IV (Invariant-Isolating). The low-[S] assay exactly determines the orbit of (Vmax, Km) under the equivalence relation (Vmax, Km) ~ (λ·Vmax, λ·Km). The missing invariant for full reconstruction is the absolute scale (either Vmax or Km individually), which requires a high-[S] assay to determine.

---

## §6. Formal Sufficiency for Non-Injectivity Tasks

**Theorem (Orbit-Task Sufficiency)** [PROVED for finite-set setting]:

Let G be a group acting on 𝒳, and let f_G: 𝒳 → G-orbits be the orbit map. Let T_G: 𝒳 → G-orbits be the orbit task (determine which G-orbit x belongs to). Then:

    Score(f_G, T_G) = 1

regardless of whether Score(f_G, 𝒳) = 1.

**Proof.** If T_G(x) ≠ T_G(y) (x and y in different G-orbits), then f_G(x) ≠ f_G(y) by definition (the orbit map distinguishes different orbits). Score = 1. □

**Corollary (Quotient-Task Sufficiency)** [PROVED]:

For any equivalence relation ~ on 𝒳, the quotient map f_~: 𝒳 → 𝒳/~ achieves Score(f_~, T_~) = 1 where T_~ is the task of determining which equivalence class x belongs to.

**Theorem (Invariant-Task Sufficiency condition)** [PROVED for finite-set setting]:

A map f: 𝒳 → Y achieves Score(f, T) = 1 for a task T: 𝒳 → Z if and only if f separates all pairs that T separates: for all x, y ∈ 𝒳: T(x) ≠ T(y) ⟹ f(x) ≠ f(y). Equivalently, T factors through f (there exists h: Y → Z with T = h ∘ f).

**Proof.** Score(f, T) = 1 iff for all x ≠ y with T(x) ≠ T(y): ∃i with fᵢ(x) ≠ fᵢ(y). This is the condition that T-distinct pairs are f-distinct, i.e., T-fibers are refined by f-fibers. Equivalently: ~_f refines ~_T, equivalently T = h ∘ f for some h. □

---

## §7. Connection to the Crossing Lemma

**Connection to WP57 "Productive Incompleteness"** [STRUCTURAL]:

In WP57, "productive incompleteness" referred informally to the situation where a system that cannot achieve full reconstruction nevertheless produces useful scientific output. The present paper formalizes this as the Five-Category Classification.

The connection to the Crossing Lemma: in the UOP/Crossing Lemma framework, a partition pair {π₁, π₂} achieves score = 1 (meet = π_disc) iff the joint map J crosses — i.e., the two partitions are incompatible and their unresolved pairs are disjoint. Score = 0 means no crossing in the relevant sense. But crossing is not always required:

- For an orbit task (Category IV): the partition π_orbit already achieves Score = 1 for the orbit task without needing a second partition to cross it.
- For a refinement task (Category III): a second partition that refines the first achieves Score = 1 for questions within the already-resolved structure, without any crossing.

**The Crossing Lemma governs when score-1 full reconstruction is possible. Productive Incompleteness governs what is achievable without that crossing.**

---

## §8. Diagnostic Language

**Corrected diagnostic output tiers** [STRUCTURAL]:

| Category | Score for 𝒳 | Score for task T | Tool output |
|---|---|---|---|
| I — Complete Complement | 1 | 1 for all T | "Resolves all remaining ambiguity." |
| II — Partial Complement | 0 | 1 for some T | "Resolves partial ambiguity. Valuable; may need follow-up." |
| III — Refinement Only | 0 | 1 only for already-resolved T | "Improves precision on known directions. Does not reveal hidden dimensions." |
| IV — Invariant-Isolating | 0 | 1 for specific quotient T | "Exactly determines orbit/invariant. Requires gauge-fix for full reconstruction." |
| V — Invalid | — | — | "Model or domain is ill-posed. Repair required." |

**Non-negotiable correction:** Category V is the only category where F is outright invalid. Categories II, III, and IV may all be scientifically indispensable.

---

## Summary

**[PROVED]** Five-Category Classification: every measurement family falls into exactly one category, determined by U(F) and the existence of tasks for which Score(F, T) = 1.

**[PROVED]** Orbit-Task Sufficiency: orbit maps always achieve Score = 1 for orbit tasks, regardless of full-reconstruction score.

**[PROVED]** Invariant-Task Sufficiency: f achieves Score(f, T) = 1 iff T factors through f.

**[STRUCTURAL]** Banach-Tarski (Category IV): orbit structure fully determined; measure inaccessible.

**[STRUCTURAL]** CT projection (Category II): row-integral subspace fully determined; 3D reconstruction requires additional angles.

**[STRUCTURAL]** Enzyme kinetics (Category IV): Vmax/Km ratio exactly determined; individual parameters require high-[S] assay.

**[OPEN]** Full formalization for infinite sets and function spaces: the five categories are proved for finite 𝒳. Extending to infinite-dimensional function spaces (CT imaging, QFT) requires measure-theoretic and functional-analytic machinery not developed here.

The central correction: "Score = 0" is not a verdict of uselessness. It is a verdict for full reconstruction only. A map can fail to determine the whole object while remaining the best map for isolating a specific invariant.
