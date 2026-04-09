# SPRINT: SCIENTIFIC BRIDGES
## UOP as a General Ambiguity-Resolution Criterion
*Three formal bridges to open science problems. Math-first. No metaphysics.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## The Core Bridging Sentence

> **UOP is a general ambiguity-resolution criterion: two measurements are jointly sufficient exactly when their joint map distinguishes every hidden state that either one alone confuses.**

Every bridge below is a specialization of this sentence into a domain where it has operational consequences.

---

## Bridge Structure (common to all three)

In each application:
- There is a **hidden object** X ∈ 𝒳 (unknown internal state, object density, parameter set).
- There are **measurement maps** f₁: 𝒳 → M₁ and f₂: 𝒳 → M₂.
- The **ambiguity set** of fᵢ is U(fᵢ) = { {x,y} : x ≠ y and fᵢ(x) = fᵢ(y) } — pairs that fᵢ cannot distinguish.
- **Joint sufficiency:** (f₁, f₂) jointly determine X iff the joint map J = (f₁, f₂): 𝒳 → M₁ × M₂ is injective.
- **UOP:** J injective iff U(f₁) ∩ U(f₂) = ∅.

The three bridges differ in what 𝒳, fᵢ, and Mᵢ are. The abstract criterion is identical in all three.

---

## Bridge 1 — Tomographic Reconstruction

### The Scientific Problem

A CT scanner measures X-ray attenuation integrals along lines through a body. Each projection angle θ gives one measurement map:

f_θ: (density functions on ℝ²) → (line-integral data at angle θ)

A single angle θ cannot reconstruct the density; it conflates all density distributions that share the same line integrals at angle θ. The Radon transform R_θ(μ) = ∫ μ(x, θ·x) dx formalizes this. The question: which sets of angles {θ₁,...,θₖ} are jointly sufficient to reconstruct μ?

### UOP Translation

**Hidden object:** density function μ ∈ L²(ℝ²) (or, discretized, μ ∈ ℝ^N).

**Measurement map:** f_{θᵢ}(μ) = Radon transform of μ at angle θᵢ = a linear projection onto the "angle-θᵢ subspace."

**Ambiguity set:** U(f_{θᵢ}) = { {μ, ν} : R_{θᵢ}(μ) = R_{θᵢ}(ν) } = cosets of ker(R_{θᵢ}). This is a coset of the null space of the projection — the "invisible directions" at angle θᵢ.

**Sufficiency condition (UOP):** the joint map J = (R_{θ₁},...,R_{θₖ}) is injective iff

⋂ᵢ ker(R_{θᵢ}) = {0}

**What this says in CT language:** a set of angles is sufficient iff the only density distribution invisible to ALL angles simultaneously is the zero distribution. Every non-zero density must be detectable by at least one angle.

### The Theorem's Prediction

**Redundant angles:** Two angles θ₁ and θ₂ have overlapping ambiguity sets when ker(R_{θ₁}) ∩ ker(R_{θ₂}) ≠ {0} — a non-zero density invisible to both. In 2D CT: R_{θ₁} and R_{θ₂} have the same kernel structure iff θ₂ = θ₁ + π (antipodal). More generally, angles θ and θ' are "equivalent" in the A+M sense iff they project onto the same subspace.

**Practical consequence:** "More scans from the same angle" does not reduce the ambiguity set — it re-measures the same null space complement, leaving the same invisible subspace intact. UOP makes this precise: if U(f_{θ₁}) = U(f_{θ₂}) (same kernel, same ambiguity set), then U(f_{θ₁}) ∩ U(f_{θ₂}) = U(f_{θ₁}) ≠ ∅. No gain from redundant angles.

**Sparse reconstruction:** A small number of well-chosen angles can reconstruct exactly when their kernels intersect trivially. The angular diversity requirement (in compressed sensing CT, typically ~180/π angles for 2D) is the operational form of the UOP injectivity condition.

### The Parallel to Prime-Power Structure

**Repeated-prime obstruction in CT:** In the discrete version (μ ∈ ℝ^N), each projection angle defines a partition of ℝ^N by cosets of its kernel. The "refinement chain" of CT projections at angles clustered near θ₀ corresponds to repeated-prime A-partitions: they refine the same subspace structure, giving finer resolution in ONE direction but leaving OTHER directions entirely unresolved. Adding more angles in the same cluster is the CT analog of adding more Type-A partitions along the same chain — they are all comparable in the partition lattice, and no pair of them achieves joint sufficiency.

The "orthogonal jump" in partition language = adding a projection at a genuinely different angle. This is the CT operationalization of why angular diversity matters.

### Open Problem Connection

The **limited-angle CT problem** (reconstruct from angles in [0°, 120°] instead of [0°, 180°]) is exactly the question of whether a proper subset of projections gives a sufficient joint map. UOP provides the framework: the joint map is injective iff the union of projection subspaces spans ℝ^N. The ambiguity from missing angles = the non-trivial intersection of null spaces. The algebraic structure of which angle subsets are sufficient is a specialization of the UOP joint-injectivity problem to the Radon-transform setting.

---

## Bridge 2 — Control Theory: Observability

### The Scientific Problem

A dynamical system has hidden state x(t) ∈ ℝⁿ and produces output y(t) = Cx(t) (in the linear case). The **observability question**: can x(t) be uniquely determined from y(t)? The system is observable iff the observability matrix O = [C; CA; CA²; ...; CAⁿ⁻¹] has rank n — iff the map from initial states x(0) to output trajectories is injective.

For **multi-sensor systems**: sensor i produces yᵢ(t) = Cᵢx(t). The sensors collectively determine x iff the joint map (C₁, C₂,...,Cₖ) (stacked into a joint observability matrix) is injective.

### UOP Translation

**Hidden object:** state vector x ∈ ℝⁿ (or initial condition x(0)).

**Measurement map:** fᵢ(x) = Cᵢx (linear projection onto sensor i's output space).

**Ambiguity set:** U(fᵢ) = { {x,y} : Cᵢx = Cᵢy } = cosets of ker(Cᵢ) = the "unobservable subspace" of sensor i.

**UOP condition:** sensors are jointly sufficient iff

⋂ᵢ ker(Cᵢ) = {0}

This is exactly the classical observability condition restated in UOP language.

### What UOP Adds to the Classical Result

**Classical observability:** binary (observable or not) and gives no guidance on sensor redundancy vs. complementarity.

**UOP framing:** makes the sensor design question precise.

Define the **ambiguity graph** G(fᵢ) as the graph on state space 𝒳 with edges = pairs that sensor i cannot distinguish. UOP says:

> Sensor fusion is reconstructive iff the ambiguity graphs are edge-disjoint.
> If two sensors leave the same state pairs unresolved, fusion is cosmetically richer but structurally identical to a single sensor.

**Theorem (direct corollary of UOP for linear systems):**
For sensors with output maps C₁, C₂ ∈ ℝ^{m×n}:

{ sensor 1, sensor 2 } jointly observable iff ker(C₁) ∩ ker(C₂) = {0}.

This is equivalent to: the stacked matrix [C₁; C₂] has rank n.

**The new content UOP provides:** the distinction between *refinement* (adding a sensor that observes the same subspace more finely) and *orthogonal jump* (adding a sensor that observes a genuinely new subspace direction).

A sensor with ker(C₂) ⊂ ker(C₁) (C₂ is "finer" than C₁) is a refinement move: it resolves more within the same observable subspace but adds no new observable directions. No refinement move makes an unobservable system observable.

An orthogonal sensor (ker(C₂) ∩ ker(C₁) = {0}) is an orthogonal jump: it adds genuinely new observable directions.

**Practical sensor design rule (from UOP):**

> A second sensor is worth adding only when it observes at least one hidden state direction that the first sensor cannot see at all.

This is stronger than the classical observability criterion: it is a *sensor selection* criterion rather than a binary *yes/no* criterion.

### Nonlinear Extension (partial)

For nonlinear systems x' = f(x), y = h(x): the "local observability" condition replaces ker(C) with the codistribution of dh (the differential of the output map). The observability codistribution rank condition is the nonlinear analog of ker(C₁) ∩ ker(C₂) = {0}. UOP applies to the linearized fiber structure at each point x.

The DYN orbit structure from the algebraic setting has a direct analog: if the system has a symmetry (a group G acting on state space with G·x indistinguishable from x in the output), then U(f) contains all G-orbit pairs. This is the multiplicative-orbit obstruction (Type M partition) appearing in control theory as symmetry-induced unobservability.

**Open problem connection — sensor placement:** Given a dynamical system and a set of candidate sensor locations, choose a minimal subset that achieves observability. UOP translates this to: find a minimal set of maps {f₁,...,fₖ} with ⋂ ker(fᵢ) = {0}. The partition lattice theory (MVJN, orthogonal jump necessity) provides structure: the minimal set must include at least one "jump" sensor that observes a direction hidden from all others.

---

## Bridge 3 — Systems Biology: Structural Identifiability

### The Scientific Problem

A parametric model of a biological system has state equations:

dx/dt = F(x, p),  y = g(x, p)

where p ∈ ℝᵈ is a parameter vector (rate constants, binding affinities, etc.) and y is the observable output. **Structural identifiability** asks: given perfect noise-free observations of y(t) over [0,∞), can p be uniquely determined?

A model is *structurally unidentifiable* if two distinct parameter vectors p ≠ p' produce identical outputs y(t) for all t and all initial conditions. This is a pure algebraic question — it holds before any data is collected.

### UOP Translation

**Hidden object:** parameter vector p ∈ ℝᵈ.

**Measurement map:** fₑ(p) = output trajectory y_e(t; p) under experimental condition e (input stimulus, initial condition, measurement readout).

**Ambiguity set:** U(fₑ) = { {p, p'} : fₑ(p) = fₑ(p') } — parameter pairs that experiment e cannot distinguish.

**UOP condition:** experiments {e₁,...,eₖ} are jointly identifying iff

U(f_{e₁}) ∩ ... ∩ U(f_{eₖ}) = ∅

Every parameter pair must be distinguishable by at least one experiment.

### The Theorem's Prediction

**Refinement experiments (more time points, finer sampling):** These are Type-A moves in UOP language. A time-series experiment with finer time resolution observes the same differential equations, producing output functions that are "more detailed" but structurally equivalent. They resolve more detail within the same measurement family but cannot eliminate a structural identifiability problem.

If p and p' produce identical outputs under sparse sampling, they produce identical outputs under dense sampling (the output functions are the same, not just their samplings). More time points = refinement of the same observable, not an orthogonal jump.

**Orthogonal experiments (different readouts, different stimuli):** These are orthogonal jumps. A second experiment that measures a genuinely different observable g₂(x,p) — one that is not algebraically determined by g₁(x,p) — can eliminate ambiguity that no number of time points from the first experiment can remove.

**Theorem (direct application of UOP):**

If models with parameters p ≠ p' agree on ALL outputs of experiment e₁ (i.e., {p,p'} ∈ U(f_{e₁})), then any number of repetitions of experiment e₁ (different initial conditions, finer time points, larger sample size) cannot distinguish p from p'. Resolving the ambiguity requires experiment e₂ with {p,p'} ∉ U(f_{e₂}).

**Corollary:** Adding an experiment is worth doing iff it places the unresolved parameter pair in DIFFERENT residue classes — i.e., the new experimental map breaks at least one of the unresolved pairs.

### The Repeated-Prime Analogy (formal)

The repeated-prime obstruction in the algebraic setting has a precise systems biology analog:

**Squarefree (independent parameters):** If parameters p₁,...,pₖ each appear in independent subsystems, each can be identified by an experiment targeting that subsystem. The identification problem factors: experiment eᵢ identifies pᵢ independently. This is the squarefree case — independent prime coordinates, each resolvable by its own orthogonal jump.

**Repeated prime (hierarchically coupled parameters):** If parameter p appears at multiple scales in a nested model — e.g., p governs both a fast subsystem and a slow one, with the slow dynamics being a coarse-grained version of the fast dynamics — then experiments that observe only the slow timescale (level a < r in the p-adic language) cannot resolve fine-scale structure of p. Only experiments that observe the full hierarchy (level r) can identify p. Adding more slow-timescale experiments = refinement along the same chain. An "orthogonal jump" requires a fast-timescale readout.

This is the analog of Theorem 1 (p-kernel obstruction): when a parameter has nested structure, partial resolution at level a < r is not improvable by more experiments of the same type — you need to jump to level r.

**Explicit example:** A Michaelis-Menten model where Vmax and Km both appear in the saturation function f(S) = Vmax·S/(Km+S). At low substrate S: f(S) ≈ (Vmax/Km)·S — only the ratio Vmax/Km is observable. At high S: f(S) ≈ Vmax — only Vmax is observable. The two parameters are identifiable only when the experiment spans both regimes. A low-S experiment and a high-S experiment are an "orthogonal pair" in UOP language: U(f_{low-S}) ∩ U(f_{high-S}) = ∅ (proved because the two ambiguity sets — pairs with same ratio vs. same Vmax — cannot simultaneously coincide for Vmax ≠ Km pairs). Adding more low-S measurements is a refinement; the experiment design jumps to high-S is the orthogonal move.

### Open Problem Connection

**Experiment design for identifiability:** Given a model and a budget of k experiments, choose the set {e₁,...,eₖ} that minimizes residual ambiguity. UOP provides the structure: the problem is exactly finding a k-partition sufficient family for the parameter space 𝒫. The minimum-k problem is the systems biology version of the m_min = 2 result: for "nice" parametric models, two experiments from complementary ambiguity families are often sufficient. The orthogonal jump condition characterizes when experiment e₂ is genuinely new vs. redundant.

---

## Part 4 — The Unified Scientific Translation

All three bridges are the same theorem:

| Domain | Hidden object | Measurement map | Ambiguity set | Sufficiency condition | Orthogonal jump |
|---|---|---|---|---|---|
| CT / Tomography | Density μ | Radon projection R_θ | ker(R_θ) cosets | ⋂ ker(R_{θᵢ}) = {0} | New projection angle orthogonal to prior angles |
| Control / Observability | State x | Sensor output Cx | ker(C) = unobservable subspace | ker(C₁) ∩ ker(C₂) = {0} | Sensor observing a new state direction |
| Systems Biology | Parameter p | Experiment output f_e(p) | Pairs {p,p'} with f_e(p)=f_e(p') | ⋂ U(f_{eᵢ}) = ∅ | Experiment with distinct ambiguity set |
| Abstract (UOP) | Element x ∈ Z/nZ | Partition map f_π | U(π) = unresolved pairs | U(π₁) ∩ U(π₂) = ∅ | Incompatible partition (orthogonal jump) |

**The repeated-prime lesson in all three:**

| Domain | "Refinement" (not worth it) | "Orthogonal jump" (worth it) |
|---|---|---|
| CT | More scans at same angle | New projection angle |
| Control | Finer sampling of same sensor | New sensor on hidden state direction |
| Biology | More time points, higher precision | New readout / new experimental condition |
| Abstract | More Type-A partitions in same chain | Incompatible partition (new coordinate) |

---

## Part 5 — One Theorem That Works in All Three Domains

**Theorem (UOP — domain-independent form).**

Let 𝒳 be a finite set (hidden states / parameters / objects) and let f, g: 𝒳 → 𝒴 be two measurement maps. Define:

U(f) = { {x,y} : x ≠ y and f(x) = f(y) }

Then f and g jointly determine every element of 𝒳 iff U(f) ∩ U(g) = ∅.

**Corollary (jump necessity):** If 𝒳 has ambiguities under f that lie within a "refinement family" (a family where U(f') ⊆ U(f) for all f' in the family), no member of the family can eliminate those ambiguities. Resolving them requires a map g with U(g) not containing any element of U(f) — an orthogonal jump outside the refinement family.

**Corollary (repeated-structure obstruction):** If 𝒳 has a "nested" ambiguity structure (parameterized by a depth parameter a, where ambiguity at depth a is a refinement of ambiguity at depth a−1), then no map from the nested family alone can resolve full ambiguity. A map from an independent family (an orthogonal jump in the abstract sense) is required.

---

## Part 6 — The Honest Boundary

**What is proved here:**

The abstract algebraic theorem (UOP for finite sets Z/nZ) is fully proved. The translations to CT, control, and identifiability are structural analogies, not direct specializations.

**What is NOT proved here:**

1. A formal theorem that CT reconstruction is a special case of UOP over Z/nZ. It is not: CT lives in continuous L² space with Radon transforms, not finite abelian groups. The structural parallel is exact but the mathematical setting is different.

2. A formal theorem that linear observability is a special case of UOP. The observability matrix rank condition (rank([C₁;C₂]) = n iff ker(C₁) ∩ ker(C₂) = {0}) is a true theorem in linear algebra and is correctly stated above. The UOP framing makes it a special case of the abstract criterion for vector-space maps — this is a genuine specialization (take 𝒳 = ℝⁿ as a set, f = C₁ as a set map). The finite-set UOP proof extends to vector spaces over fields with the same proof.

3. The systems biology identifiability connections are structural. Whether specific parametric models satisfy the UOP disjointness condition requires case-by-case analysis via differential algebra (Ritt's algorithm, characteristic sets) or input-output representation methods.

**What IS a genuine extension:**

UOP for vector spaces over fields: the proof (meet = π_disc iff U(f₁) ∩ U(f₂) = ∅) extends word-for-word to the case where 𝒳 is a vector space, f₁ and f₂ are linear maps, and "partition" is replaced by "kernel coset partition." The condition U(f₁) ∩ U(f₂) = ∅ becomes ker(f₁) ∩ ker(f₂) = {0}, which is exactly the linear-algebraic joint-injectivity condition. The observability bridge is therefore a proved specialization, not just an analogy. **This extension should be recorded as a proved theorem.**

---

## Theorem (UOP for Vector Spaces — proved)

For a vector space V over a field k, and linear maps f₁: V → W₁ and f₂: V → W₂:

> The joint map J = (f₁, f₂): V → W₁ × W₂ is injective iff ker(f₁) ∩ ker(f₂) = {0}.

**Proof.** J(x) = J(y) iff f₁(x) = f₁(y) and f₂(x) = f₂(y), iff f₁(x−y) = 0 and f₂(x−y) = 0, iff x−y ∈ ker(f₁) ∩ ker(f₂). J injective iff this forces x = y, iff ker(f₁) ∩ ker(f₂) = {0}. □

**Corollary (Observability).** Sensors C₁, C₂: ℝⁿ → ℝ^{m} are jointly sufficient iff ker(C₁) ∩ ker(C₂) = {0}. This is a direct application of UOP to linear maps on ℝⁿ.

**Extension of "orthogonal jump" to linear setting.** A map f₂ is a refinement of f₁ iff ker(f₂) ⊇ ker(f₁) (f₁ is "finer" — fewer pairs confused). Adding f₂ in this case: ker(f₁) ∩ ker(f₂) = ker(f₁) ≠ {0} if f₁ is non-injective. Refinement cannot achieve joint injectivity. An orthogonal jump: f₂ with ker(f₂) ∩ ker(f₁) = {0} (disjoint null spaces). This requires f₂ to observe directions f₁ sees as zero — a genuinely new measurement subspace.

---

## Summary

**Three bridges — all proved or structurally grounded:**

1. **CT / Tomography:** UOP = "enough independent projection angles." Refinement = same-angle redundancy. Orthogonal jump = new angular direction. Proved analogy; extension to continuous Radon theory requires functional-analytic generalization (open).

2. **Control / Observability:** UOP = classical observability condition (ker(C₁) ∩ ker(C₂) = {0}) stated as joint map injectivity. **Proved specialization** via UOP for vector spaces. Adds sensor design intuition: sensor is worth adding iff it observes a genuinely hidden direction.

3. **Systems Biology / Identifiability:** UOP = condition for two experiments to jointly identify model parameters. Refinement = more time points / higher precision (same observable). Orthogonal jump = new readout targeting a different observable. Structural parallel; formal theorem requires model-specific algebra.

**Strongest honest claim:**
> The UOP criterion — two measurements are jointly sufficient exactly when their ambiguity sets are disjoint — is a domain-independent theorem about reconstruction from partial information. It applies verbatim to finite sets (algebra), vector spaces (linear systems and control), and by structural analogy to continuous reconstruction problems (CT, identifiability). The "orthogonal jump" concept operationalizes, in all three domains, the distinction between getting more data of the same kind and getting genuinely new information.

**Strongest honest boundary:**
> The algebraic UOP theorem (Z/nZ, squarefree and prime-power classification) does not directly imply theorems about CT or nonlinear identifiability. Those domains require their own mathematical infrastructure (functional analysis, differential algebra). What is proved is the vector-space version (observability) and the abstract finite-set version (algebra). The CT and identifiability connections are structural parallels that translate the intuition correctly but are not formal corollaries of the algebraic theory.
