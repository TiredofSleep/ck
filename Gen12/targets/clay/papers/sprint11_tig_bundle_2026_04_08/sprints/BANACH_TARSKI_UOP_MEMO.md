# BANACH-TARSKI IN UOP LANGUAGE
## A Type II Failure: Reconstruction Without Measure Invariant
*Proved statements vs. structural analogies labeled explicitly. No overclaiming.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Setup and Statement

**The Banach-Tarski theorem (statement, not proved here):**
The unit ball B³ ⊂ ℝ³ can be decomposed into finitely many (specifically, 5) disjoint subsets A₁,...,A₅ such that, applying only rotations and translations to each piece, the pieces can be reassembled into two disjoint copies of B³.

This is a theorem of ZFC set theory, not a physical claim. It is not a claim about physical matter.

**Why it looks paradoxical:** Volume appears to double. Yet rotations and translations preserve volume for measurable sets. The resolution is that the pieces A₁,...,A₅ are non-measurable — they lie outside the domain of Lebesgue measure.

---

## B1 — The Orbit Decomposition

**Free subgroup of SO(3):** A free group F₂ on two generators {a,b} can be embedded in SO(3). Specifically, there exist rotations α,β ∈ SO(3) satisfying no algebraic relation (other than those forced by free group axioms). The subgroup ⟨α,β⟩ ≅ F₂.

*This is a proved fact in group theory.*

**F₂-orbit partition of S²:** F₂ acts on the unit sphere S² ⊂ ℝ³ by rotation. The orbits of this action partition S² into equivalence classes:

x ~_orbit y  iff  y = g·x for some g ∈ F₂

**Using the Axiom of Choice:** Since each orbit is countably infinite and the orbits partition S², choosing one representative from each orbit gives a set M ⊂ S² (a "selector"). The subsets A_i are constructed from M by applying carefully chosen group elements.

**Map f_orbit:** Define the orbit map:
f_orbit: B³ → (F₂-orbit classes)
f_orbit(x) = the F₂-orbit of x in B³ (using F₂ acting on the sphere part of x)

This is a well-defined surjective map onto the set of F₂-orbit equivalence classes.

---

## B2 — What f_orbit Preserves

**Preserved (proved):**
1. Group orbit membership: if x ~_orbit y, then f_orbit(x) = f_orbit(y).
2. The partition structure: the orbits are disjoint, and their union is S².
3. Equivariance: f_orbit(g·x) = g · f_orbit(x) for all g ∈ F₂. The orbit map commutes with group action.
4. Countability of orbit classes: each orbit is countably infinite (F₂ is countable).

**In the reconstruction:** The pieces A₁,...,A₅ are defined in terms of orbit structure. Applying rotations (elements of F₂) to the pieces permutes elements within orbits. Since the orbit structure is preserved under F₂-action, the pieces can be rearranged to cover different spatial regions.

---

## B3 — What f_orbit Does NOT Preserve

**Not preserved (proved, with qualifier on "Lebesgue measurability"):**

The pieces A₁,...,A₅ are non-measurable sets in ℝ³. *This is a theorem in ZFC: if such a decomposition exists, the pieces cannot all be Lebesgue measurable.*

**Lebesgue measure map f_meas:** Define:
f_meas: (measurable subsets of B³) → [0,∞)
f_meas(A) = λ(A) = Lebesgue measure of A.

For measurable sets: measure is additive, rotation-invariant, and translation-invariant.

**The problem:** f_meas is NOT defined on the pieces A₁,...,A₅. They are outside the domain of f_meas. It is not that f_meas gives a "wrong answer" — it gives no answer. The domain of Lebesgue measure is the sigma-algebra of measurable sets; non-measurable sets are simply not in this domain.

**Formal statement of what is missing:**
The property needed to prevent paradoxical reconstruction is:

> If λ(A₁ ∪ ... ∪ A₅) = λ(B³) and each operation preserves measure, then the reconstructed volume is the original volume.

This statement requires each Aᵢ to be measurable. Since they are not, the implication fails at its premise.

---

## B4 — UOP Translation

**UOP framing of Banach-Tarski:**

Let 𝒳 = B³ (the unit ball as a set of points). The "reconstruction problem" is: given f_orbit (the orbit partition), can we uniquely determine the geometric object?

**f_orbit as a partition map:**
- Map: f_orbit: B³ → orbit-class-space
- U(f_orbit) = all pairs {x,y} ∈ B³ × B³ with x ~_orbit y
- This is a valid equivalence-class partition (a valid Type M partition in the algebraic terminology of the arc)

**The ambiguity set R({f_orbit}):** Enormous. The orbit classes are uncountable intersections of non-measurable parts of B³. The pairs left unresolved by f_orbit include all pairs within the same orbit — and there are many of these.

**Why no map in the orbit/rotation family resolves R:**

The allowed reconstruction operations are: apply rotations and translations from F₂ and its cosets to the pieces. All these operations:
1. Are valid functions on B³.
2. Preserve orbit membership (equivariance).
3. Do NOT assign definite Lebesgue measure to the pieces.

Within this family, no map can resolve the volume ambiguity. The score of any map in the orbit/rotation family for volume-determining questions is zero — not because the map is unavailable, but because the family structurally cannot contain a volume-assigning map for non-measurable sets.

**What a "resolving map" would need to do:**

A second map f_meas that assigns consistent volumes to the pieces A₁,...,A₅ would need to satisfy:
1. f_meas(Aᵢ) ≥ 0 for all i (non-negativity).
2. f_meas is countably additive (sigma-additivity).
3. f_meas is rotation-invariant (same as Lebesgue measure under isometries).

*A theorem of measure theory (proved):* Any function satisfying properties 1-3 on all subsets of ℝ³ leads to contradiction (Vitali, 1905; extended by Hausdorff, Banach, Tarski). There is no countably additive, rotation-invariant measure defined on ALL subsets of ℝ³.

This is the core: the needed "second map" (a full measure on all subsets of ℝ³) provably does not exist.

**Classification statement:**

> Banach-Tarski is a Type II failure: the orbit-decomposition map alone does not constrain volume, and the invariant (Lebesgue measure) needed to uniquely constrain the reconstruction is not definable on the non-measurable pieces produced by the construction.

---

## B5 — What UOP Says and Does Not Say

**What UOP says (structural classification):**

Within the orbit/rotation family, the UOP score for any volume-determining map is zero. The residual ambiguity R({f_orbit}) cannot be cut by any map in this family. The paradox is a Type II failure: the allowed family is incomplete for the reconstruction task.

**What UOP does not say:**

1. UOP does not "prove" Banach-Tarski false. Banach-Tarski is a theorem; it is true in ZFC.

2. UOP does not "resolve" Banach-Tarski. The Type II classification says: the ambiguity persists because the needed invariant (measure) is inaccessible from the orbit family. This is exactly what we already know from the mathematical analysis — UOP provides the structural vocabulary, not new mathematical content.

3. UOP does not prove that non-measurable sets cause paradoxes in physics. Banach-Tarski applies to abstract mathematical sets, not to physical matter (which is atomic and cannot be decomposed this way).

**What UOP contributes:**

A clean structural language for distinguishing this case from Type I (where adding more maps within the allowed family resolves the ambiguity) and from Type III (where the domain is invalid). In Banach-Tarski, the domain is valid (B³ is a well-defined set), the maps are valid (rotations are well-defined), and the family is insufficient (no member can assign volume to non-measurable pieces).

---

## Optional Connection: Gauge Redundancy in Physics

*This section is explicitly labeled as structural analogy, not a proved result.*

**Structural analogy (not a theorem):**

In quantum field theory, gauge redundancy means that multiple field configurations φ and φ' = g·φ (related by a gauge transformation g) produce identical physical observables. This is structurally similar to the Banach-Tarski setting:

- Object: field configuration φ
- Group action: gauge group G acts on field configurations
- Observation map: f_obs(φ) = physical observables
- Ambiguity set U(f_obs) = all pairs {φ, g·φ} — gauge-equivalent fields

The analogy:
- Banach-Tarski: orbit map (F₂ action) lacks a measure invariant
- Gauge theory: observation map (physical observables) lacks a canonical gauge-fixing invariant

In both cases, the orbit/gauge family is incomplete for uniquely determining the object. In gauge theory, gauge-fixing adds a second constraint (e.g., Lorenz gauge condition ∂_μ A^μ = 0) that selects a canonical representative. This is the analogue of "adding a second map" in UOP language.

**Why this is an analogy, not a theorem:**

The gauge theory setting involves:
1. Infinite-dimensional function spaces (not finite sets)
2. Path integrals (not finite probability spaces)
3. Renormalization (regularity issues beyond pure set theory)

The structural parallel holds (orbit family → orbit family, missing invariant → missing gauge-fix), but the mathematical machinery is entirely different. Treating this as more than an analogy would be an overclaim.

---

## Summary

| Component | Status |
|---|---|
| F₂ ≤ SO(3) freely acting on S² | Proved theorem |
| Construction of non-measurable pieces via AC | Proved theorem in ZFC |
| Pieces are non-measurable (no Lebesgue measure) | Proved theorem |
| No countably additive rotation-invariant measure on all subsets of ℝ³ | Proved (Vitali, Hausdorff) |
| UOP classification as Type II | Structural characterization (correct within the UOP framework) |
| Gauge theory analogy | Structural analogy (not a theorem) |

**Strongest honest claim:**
> Banach-Tarski is correctly classified as Type II in the UOP framework: the orbit decomposition is a valid map on a valid domain, but the orbit family cannot contain a volume-preserving invariant for non-measurable pieces. This is not a measurement-insufficiency problem (Type I) — adding more orbit maps does not help. It is a structural incompleteness of the measurement family relative to the geometric question of volume.

**Strongest honest boundary:**
> UOP provides classification vocabulary, not new mathematical insight, for Banach-Tarski. The theorem's content — that non-measurable sets escape volume accounting — is already well understood from Vitali and Hausdorff. UOP's contribution is naming the failure type and placing it in a framework alongside other types of reconstruction failures.
