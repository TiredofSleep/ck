# PARADOX CLASSIFICATION MEMO
## Injectivity Failure vs. Admissibility Failure vs. Time-Consistency Failure
*Exact structural distinctions only. Proved statements vs. analogies labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — Four Structural Failure Types: Formal Definitions

Let 𝒳 be a set of objects to be distinguished (the "hidden state space"), and let F = {f₁,...,fₖ} be a family of maps from 𝒳 to measurement spaces Y₁,...,Yₖ.

**Definition (Sufficient family).** F is *sufficient* for 𝒳 iff the joint map J = (f₁,...,fₖ): 𝒳 → Y₁×...×Yₖ is injective: every distinct pair {x,y} ⊂ 𝒳 is separated by at least one fᵢ.

**Definition (Ambiguity set).** U(fᵢ) = { {x,y} ⊂ 𝒳 : x ≠ y and fᵢ(x) = fᵢ(y) }.

**Definition (Residual ambiguity).** R(F) = ⋂ᵢ U(fᵢ) — pairs unresolved by all maps in F.

Failures arise in four structurally distinct ways:

---

**Type I — Injectivity Failure (Insufficient Coverage).**

The maps in F are valid (each fᵢ is a well-defined function on 𝒳) but R(F) ≠ ∅.

*Cause:* The current measurement family does not cover enough directions in 𝒳. Some distinct objects x ≠ y are not separated by any fᵢ.

*Resolution:* Add a map fₖ₊₁ with U(fₖ₊₁) ∩ R(F) ≠ U(fₖ₊₁) — a map that separates at least one currently unresolved pair. Repeat until R(F ∪ {new maps}) = ∅.

*UOP applies directly:* The framework of ambiguity sets, scores, and joint injectivity is the exact tool.

---

**Type II — Missing Invariant (Coverage-Invariant Mismatch).**

The maps in F are valid but R(F) ≠ ∅, AND no map in the *allowed class* can cut R(F). The residual ambiguity persists because the required "cutting" map lies outside the allowed measurement family.

*Cause:* The allowed observation family preserves a structural property (e.g., group-orbit membership) but does not constrain a different quantity (e.g., volume) needed to uniquely determine the object. Adding more maps from the same family does not help.

*Resolution:* Either (a) add a map from a different structural class (a new type of invariant), or (b) recognize that the object class 𝒳 is genuinely non-unique under the allowed maps (the ambiguity is structural, not observational).

*UOP classifies but does not resolve:* UOP identifies the obstruction (R(F) is non-empty and no score-positive candidate exists within the allowed family). Resolution requires stepping outside the family.

---

**Type III — Admissibility Failure (Invalid Domain).**

The proposed map f does not define a valid function on the proposed domain 𝒳 — either the domain is ill-defined or f produces a contradiction when applied to certain inputs.

*Cause:* The proposed object x ∈ 𝒳 is not well-formed (e.g., x is a set that contains itself and doesn't), or the proposed operation f(x) leads to a logical contradiction regardless of what value is assigned.

*Resolution:* Restrict 𝒳 to a well-formed domain on which f is valid. UOP cannot apply because UOP presupposes a well-defined function on a well-defined set.

*UOP does not apply:* UOP requires f: 𝒳 → Y to be a function. If 𝒳 is ill-defined, UOP is not the right tool. The correct tool is domain restriction (type theory, axiomatic set theory, etc.).

---

**Type IV — Time-Consistency Failure (Observer-State Dependence).**

The object 𝒳, the maps F, or the ambiguity set R(F) changes as a function of the observer's state, reasoning stage, or prior commitments. The static UOP framework does not apply because the "fixed object" assumption is violated.

*Cause:* The observation problem is self-referential or interactive: the act of reasoning about which pairs are ambiguous changes what the observer believes is possible, which changes the effective ambiguity set.

*Resolution:* A dynamic observer-state model is required. The system must be recast as a sequence of states (belief state, reasoning stage), each with its own 𝒳_t and F_t.

*UOP does not directly apply:* The static UOP setting presupposes 𝒳 and F are fixed. Type IV failures require a dynamic framework.

---

**Theorem 1 (Mutual Distinctness of Failure Types — proved for Types I, III; structural claim for II, IV).**

Types I, II, III, and IV are mutually exclusive structural regimes under the following conditions:

- Type I: F ⊂ Valid(𝒳) (all maps valid), R(F) ≠ ∅, ∃ valid fₙₑ_ₓₜ with score(fₙₑₓₜ | F) > 0.
- Type II: F ⊂ Valid(𝒳), R(F) ≠ ∅, ∀ valid fₙₑₓₜ ∈ Allowed: score(fₙₑₓₜ | F) = 0.
- Type III: The proposed 𝒳 or f is not well-defined; the map is inadmissible.
- Type IV: 𝒳 or F is observer-state-dependent; the static setting does not hold.

**Distinctness:**

- I ≠ II: In Type I, adding maps from the allowed family eventually achieves sufficiency. In Type II, no such addition is possible within the family.
- II ≠ III: In Type II, the maps and domain are valid, just insufficient. In Type III, validity itself fails.
- I ≠ III, II ≠ III: UOP applies (Type I, II) vs. does not apply (Type III).
- I,II,III ≠ IV: Types I, II, III admit static analysis. Type IV requires dynamic treatment.

*Proof of distinctness for Types I and III:* Type I assumes F ⊂ Valid(𝒳): each fᵢ is a function on a well-defined 𝒳. Type III asserts that some element of the proposed setup is not a valid function or not a valid domain. These are logically incompatible conditions. □

*Types II and IV: structural classification, not formal theorem.* The distinction between "no scoring map exists within the allowed class" (Type II) and "the object set itself changes" (Type IV) is definitional and requires specifying what counts as the "allowed class" and the "static object."

---

## Part 2 — Four Paradox Analyses

---

### Zeno's Paradox → Type I

**Object set 𝒳:** The interval [0,1] ⊂ ℝ, representing positions along a path from start to finish. The relevant question is whether a runner reaches position 1.

**Proposed representation f_discrete:** Represent the motion as an enumerated sequence of steps: step k covers the interval [1 − 1/2^{k-1}, 1 − 1/2^k]. Map: k ↦ step_k.

**Failure mechanism:**

Zeno's inference: "there are infinitely many steps, therefore infinite time." This conflates cardinality with measure. The map f_discrete counts steps (gives a bijection with ℕ) but does not compute the sum of step durations. Two representations are conflated:
- f_count: motion ↦ step count (= ∞, since there are countably many steps)
- f_duration: motion ↦ total elapsed time (= ∑_{k=1}^∞ 1/2^k = 1 < ∞)

**Ambiguity:** If only f_count is used, "infinitely many steps" appears to imply "infinite time." This is U(f_count) non-trivial: f_count does not separate "finite total duration" from "infinite total duration" (both are compatible with countably many steps).

**Resolution:** Add f_duration to the measurement family. The joint map (f_count, f_duration) resolves the ambiguity: total duration is 1, not ∞. The "paradox" disappears.

**Classification: Type I.** Both f_count and f_duration are valid, well-defined maps on the well-defined object (a convergent sequence of intervals). The failure is that f_count alone is insufficient: it does not constrain the sum of step lengths. Adding the duration map (geometric series sum) resolves R.

**UOP applies directly:** score(f_duration | {f_count}) > 0 (the duration map separates the "finite vs. infinite duration" distinction that f_count cannot make).

**The mathematical resolution is not "paradox disappears by magic":** The rigorous fix is simply that ∑_{k=1}^∞ 1/2^k = 1. Zeno's error is using only the cardinality map while ignoring the measure map. In UOP language: a single map (cardinality) is insufficient to determine position; the duration map (measure) is the missing orthogonal measurement.

---

### Banach-Tarski Paradox → Type II

**Object set 𝒳:** The unit ball B³ ⊂ ℝ³ (with boundary).

**Proposed map f_orbit:** Partition B³ into equivalence classes under the action of a free subgroup F₂ ≤ SO(3) (a subgroup generated by two rotations satisfying no algebraic relations). Map f_orbit: B³ → F₂-orbit classes.

**What f_orbit preserves:** Group-orbit membership. Two points are in the same f_orbit class iff they are related by an element of F₂.

**What f_orbit does NOT preserve:** Lebesgue measure. The orbit equivalence classes (constructed using the Axiom of Choice) are non-measurable subsets of B³. No well-defined volume is assigned to them.

**The paradox:** Using only orbit structure (and the group action of rotations and translations), B³ can be decomposed into 5 pieces and reassembled into two copies of B³. This is a valid theorem in ZFC.

**Failure mechanism (Type II):** The orbit map f_orbit is a valid function on a valid domain (B³). But:

1. The "allowed reconstruction family" consists of maps that track orbit membership and apply rotations/translations.
2. No map within this family is a volume-preserving invariant for the constructed pieces (they are non-measurable).
3. A Lebesgue measure map f_measure: (piece) ↦ volume is NOT in the allowed family — it is simply undefined on non-measurable sets.
4. Therefore no map within the orbit/rotation family can kill the ambiguity: the same orbit structure is compatible with two different total volumes (1 and 2 times the original).

**Classification: Type II.** The maps are valid (f_orbit is a well-defined partition; rotation maps are valid bijections on ℝ³). The domain is well-defined (B³ is a standard mathematical object). The failure is that the allowed map family (orbit + rotation) does not include a measure-preserving invariant, so volume is not constrained by the reconstruction.

**UOP does not resolve Banach-Tarski:** It classifies the obstruction. The orbit map alone does not achieve injectivity for geometric questions (volume). Adding a measure map would constrain volume — but cannot be added because the pieces are non-measurable (f_measure doesn't exist on them). This is Type II: resolution requires either (a) restricting to measurable pieces (staying outside the paradoxical regime) or (b) recognizing that within non-measurable set theory, volume is not preserved.

**UOP's contribution:** Banach-Tarski is not "magic duplication." It is reconstruction under a representation family that does not preserve volume. The ambiguity persists because the needed invariant (Lebesgue measure) is not accessible from the orbit partition.

---

### Russell's Paradox → Type III

**Proposed object:** The set R = { x : x ∉ x } — "the set of all sets that do not contain themselves."

**Proposed map f:** Membership test: f(R) = "is R ∈ R?"

**Failure mechanism:**

If R ∈ R: by definition of R, R ∉ R. Contradiction.
If R ∉ R: by definition of R, R ∈ R. Contradiction.

f(R) cannot be consistently defined to be either "yes" or "no."

**Classification: Type III.** The proposed domain — the object R itself — is not a well-formed set in any consistent set theory. The problem is not insufficient coverage or a missing invariant. The proposed operation f cannot be defined consistently on R. No amount of additional maps resolves this: the issue is with the domain, not the measurement family.

**UOP does not apply:** UOP requires a well-defined function f: 𝒳 → Y. Here, the domain 𝒳 contains an object (R) for which no consistent value of f exists. The failure precedes the question of sufficient coverage.

**Resolution:** Restrict 𝒳 to collections in a well-formed type hierarchy (Russell's type theory) or to sets defined in ZF set theory (where the axiom schema of specification prevents the definition of R as a set). In ZF, R is not a set — it is a proper class or simply not a well-defined object.

**The key distinction:** Type III is a domain validity problem. The failure is not "we cannot observe enough" (Type I) or "the invariant is inaccessible" (Type II) — it is "the object does not consistently exist."

---

### The Unexpected Hanging Paradox → Type IV

**Setup:** A judge tells a prisoner: "You will be hanged on one day next week, but you will not know which day until the morning of your hanging." The prisoner reasons: Friday is impossible (if I survive to Thursday, I'd know it was Friday). But then Thursday is impossible (knowing Friday is impossible, if I survive to Wednesday I'd know it was Thursday). Iterating backward, no day is possible. Conclusion: the judge cannot carry out the sentence. But the execution does occur, catching the prisoner by surprise.

**Why static UOP analysis fails here:**

The "object set" 𝒳 = {Monday, Tuesday, Wednesday, Thursday, Friday} (possible execution days) is not fixed. It depends on the prisoner's belief state at each stage of reasoning.

Formally: at reasoning stage t, the prisoner has belief set 𝒳_t = days not yet eliminated. The map f_t: day → "can I predict this?" depends on 𝒳_t. But 𝒳_t depends on the results of f_{t-1}. The map is self-referential: applying f eliminates elements from 𝒳, which changes f.

**The observer-state dependency:**

- f_prisoner(day | 𝒳_t) = "would I know this is the hanging day if 𝒳_t is the remaining possible set?" 
- Each application of f changes 𝒳_t.
- The backward induction eliminates all days — but only under the assumption that the judge's statement is true AND that the prisoner has correct beliefs AND that the analysis is common knowledge.

**Classification: Type IV.** The "object set" changes as a function of the prisoner's reasoning. The backward induction argument is valid within its own assumptions, but those assumptions create a dynamic system where the "ambiguity set" R(F) changes at each step. The judge can execute the sentence because the prisoner's prediction model is not self-consistent at the time of execution.

**UOP does not apply directly:** UOP requires a static 𝒳 and F. Here, F changes as a function of reasoning stage. The paradox requires a game-theoretic or epistemic logic framework where observer beliefs are explicitly tracked.

**The Type IV signature:** The paradox is not about insufficient observations (Type I), inaccessible invariants (Type II), or invalid domains (Type III). It is about an observer whose belief update process is entangled with the object being observed.

---

## Part 3 — Summary Table

| Paradox | Object set 𝒳 | Map(s) f | Failure type | Resolution | UOP status |
|---|---|---|---|---|---|
| Zeno | [0,1] with step sequence | f_count (step enumeration) | Type I: f_count misses f_duration | Add geometric series sum map | Applies directly |
| Banach-Tarski | Unit ball B³ | f_orbit (free group action) | Type II: orbit family lacks measure invariant | Restrict to measurable pieces or add measure map (impossible on these pieces) | Classifies obstruction; does not resolve |
| Russell | Naive set universe | f_membership on R = {x:x∉x} | Type III: R is not a well-defined set | Restrict to ZF/type-theoretic domain | Does not apply |
| Unexpected Hanging | Days of week (belief-dependent) | f_prisoner(day | 𝒳_t) | Type IV: 𝒳 changes under reasoning | Dynamic observer-state model | Does not apply |

---

## Strongest Honest Claim

> UOP directly handles Type I failures: insufficiently many observations of a fixed, well-defined hidden object. It classifies (but cannot resolve) Type II failures: the ambiguity set persists because no map in the allowed family has positive score. It identifies (but cannot repair) Type III failures: the domain is ill-defined. It does not apply to Type IV: the static object-set assumption breaks down.

## Strongest Honest Boundary

> The four-type classification is a structural schema, not a formal theorem in its current form. Types I and III admit formal separation (valid maps on valid domain vs. invalid construction). Types II and IV require specifying what counts as the "allowed family" (Type II) and what counts as "observer-state independence" (Type IV), which are context-dependent. A fully formal version would require fixing these definitions for each application domain.
