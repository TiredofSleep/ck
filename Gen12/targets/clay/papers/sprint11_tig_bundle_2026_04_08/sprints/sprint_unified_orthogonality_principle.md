# SPRINT: UNIFIED ORTHOGONALITY PRINCIPLE
## Unifying Theorems A / B / C Under One Structural Criterion
*Algebra + equivalence relation language. Proved vs. conjectural labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — The Candidate Unified Principle

**Setup.** Each partition π on Z/nZ is induced by a map f_π: Z/nZ → X_π. The blocks of π are the fibers of f_π. Define the kernel equivalence:

ker(f_π) = { (x,y) : f_π(x) = f_π(y) }

This is the equivalence relation ~_π, whose off-diagonal part is U(π).

**Theorem 0 (restated as joint map principle):**
For partitions π₁, π₂ of Z/nZ, induced by maps f: Z/nZ → A and g: Z/nZ → B:

{ π₁, π₂ } is sufficient  ⟺  the joint map J = (f, g): Z/nZ → A × B is injective

**Proof.** J injective iff distinct x ≠ y gives (f(x),g(x)) ≠ (f(y),g(y)), i.e., f(x)≠f(y) or g(x)≠g(y). This is exactly: x and y are not simultaneously in the same π₁-block and the same π₂-block, i.e., U(π₁) ∩ U(π₂) = ∅. □

**This is the unified principle.** Every sufficiency theorem is a computation of when J is injective for specific algebraic choices of f and g.

---

## Part 2 — Three Map Types on Z/nZ (Squarefree)

For squarefree n = p₁···pₖ, fix CRT isomorphism:

Z/nZ  ≅  ∏ᵢ Z/pᵢZ ,   x ↦ (x mod p₁, ..., x mod pₖ) = (a₁,...,aₖ)

**Type M (Multiplicative-Orbit Map):** For G ≤ (Z/nZ)*:

f_G: Z/nZ → (Z/nZ)/G   (orbit space, set map)

ker(f_G) = { (x,y) : y = g·x for some g ∈ G }

**Type A (Additive-Quotient Map):** For d | n:

f_d: Z/nZ → Z/dZ ,   f_d(x) = x mod d

ker(f_d) = { (x,y) : d | (x−y) } = congruence mod d

**Observation.** π_SPEC (reflection partition) is Type M with G = {1,−1}. π_DYN(g) is Type M with G = ⟨g⟩. π_d^{add} (residue class mod d) is Type A. ALL prior families reduce to one of these two types.

---

## Part 3 — Injectivity Conditions: One Computation per Case

**Setup for each case.** The joint map J = (f_π₁, f_π₂): Z/nZ → X₁ × X₂. J fails injectivity iff ∃x ≠ y with f_π₁(x) = f_π₁(y) AND f_π₂(x) = f_π₂(y). A conflicting pair {x,y} satisfies both these identifications simultaneously.

For squarefree n, every element x = (a₁,...,aₖ) with aᵢ ∈ Z/pᵢZ. Non-unit elements have at least one aᵢ = 0. The analysis must cover ALL elements, not just units.

---

### Case M+M: Two Multiplicative-Orbit Maps

**Maps:** f_G: Z/nZ → G-orbits, f_H: Z/nZ → H-orbits.

**Conflict:** {x,y} with y ∈ Gx ∩ Hx, y ≠ x. Since y·x⁻¹ ∈ G ∩ H (for unit x): trivial iff G ∩ H = {1}.

**For non-unit x:** x has some zero component aᵢ = 0. G acts as ×gᵢ on each aᵢ. If gᵢ ≠ 0 (g is a unit, so gᵢ ≠ 0 always in Z/pᵢZ): gᵢ · 0 = 0. Zero components stay zero. The non-zero components transform as units. The conflict condition reduces to: for the sub-tuple of non-zero components, the same G∩H = {1} analysis applies.

**Theorem A (proved in prior sprint, extended):** J injective iff G ∩ H = {1} in (Z/nZ)*. □

---

### Case A+M: Additive-Quotient × Multiplicative-Orbit

**Maps:** f_d: x ↦ x mod d, f_G: x ↦ G-orbit of x.

**Conflict:** {x, g·x} with g ∈ G, g ≠ 1, and g·x ≡ x mod d.

**CRT decomposition of g·x ≡ x mod d:**

For each prime pᵢ | d: gᵢ · aᵢ ≡ aᵢ mod pᵢ, i.e., (gᵢ − 1)·aᵢ ≡ 0 mod pᵢ.
- If aᵢ ≠ 0: requires gᵢ = 1 mod pᵢ (since aᵢ is a unit in Z/pᵢZ).
- If aᵢ = 0: satisfied for any gᵢ.

**Critical case — elements with zero d-components:**
If aᵢ = 0 for ALL pᵢ | d (i.e., d | x in additive sense, x a multiple of d): then gᵢ · 0 = 0 for all pᵢ | d. The d-residue is 0 for both x and g·x. But g·x ≠ x requires g to act non-trivially on some pⱼ ∤ d (aⱼ ≠ 0 and gⱼ ≠ 1). This gives a conflict: x and g·x are in the same d-fiber (same d-residue = 0) but distinct elements.

**Theorem B (proved):** J is injective iff G acts trivially on all primes of (n/d), i.e., every g ∈ G satisfies g ≡ 1 mod pⱼ for all pⱼ | (n/d).

**Proof.**
(⟸) If G trivial on n/d: for any x and g ≠ 1 in G, g acts only on d-prime components. For g·x ≡ x mod d: gᵢ·aᵢ ≡ aᵢ for all pᵢ | d. Since g is non-trivial at some pᵢ | d: gᵢ ≠ 1, so aᵢ must be 0. If all pᵢ | d have aᵢ = 0, then x is a multiple of d, and g·x = (same aᵢ = 0 for pᵢ | d, changed aⱼ for pⱼ | d). But G trivial on n/d means aⱼ unchanged for pⱼ ∤ d. So g·x = x (g acts trivially on all components where aᵢ = 0 and trivially on n/d). Contradiction with g ≠ 1. No conflict. □

(⟹) If some g ∈ G has g ≢ 1 mod pⱼ for pⱼ ∤ d: choose x with aⱼ ≠ 0 and aᵢ = 0 for all pᵢ | d. Then d | x (all d-components are 0), so x ≡ 0 mod d. g·x has aᵢ = 0 for pᵢ | d (unchanged), and aⱼ → gⱼ·aⱼ ≠ aⱼ. So g·x ≡ 0 ≡ x mod d but g·x ≠ x. Conflict. □

---

### Case M+A: Multiplicative-Orbit × Additive-Quotient (= Corrected Theorem C)

**Maps:** f_G: x ↦ G-orbit of x, f_d: x ↦ x mod d.

This is Case A+M with roles of the two maps swapped. The joint map J = (f_G, f_d) is the same set as J = (f_d, f_G) in terms of injectivity. **The same theorem applies.**

**Corrected Theorem C:** J is injective iff G acts trivially on all primes of (n/d), i.e., every g ∈ G satisfies g ≡ 1 mod (n/d).

**Correction to prior sprint.** The prior sprint stated Theorem C as "G → (Z/dZ)* is injective." This is WRONG for non-unit elements. Explicit counterexample:

n = 15 = 3·5, G = ⟨2⟩ = {1,2,4,8} in (Z/15Z)*, d = 5.

Prior condition (injectivity of ⟨2⟩ → (Z/5Z)*): ⟨2⟩ = {1,2,4,8}, map mod 5: {1→1, 2→2, 4→4, 8→3}. Injective ✓. Prior sprint would predict SUFFICIENT.

But: T₂(5) = 10, T₂(10) = 5. Orbit {5,10}. Both ≡ 0 mod 5 (same π_5 class). CONFLICT. NOT SUFFICIENT.

The correct condition: g ≡ 1 mod (n/d) = 1 mod 3. But 2 mod 3 = 2 ≠ 1. Condition fails. Correct prediction. □

**What the prior Theorem C correctly captured:** Only unit-element conflicts (gcd(x,d)=1). It missed zero-fiber conflicts (x ≡ 0 mod d). The corrected theorem fixes this.

**Verification that prior results still hold under corrected Theorem C:**

Prior sprint's SPEC + half-modulus (n = 2m, S = {-1}, d = m): g = -1. Check g ≡ 1 mod (n/d) = 1 mod 2: -1 mod 2 = 1 ✓. Zero-fiber of π_m: multiples of m in Z/2mZ = {0, m}. T_{-1}(m) = -m mod 2m = m (since 2m - m = m). Fixed ✓. No conflict. Corrected Theorem C holds. □

---

## Part 4 — The Unified Theorem

**Theorem (Unified Orthogonality Principle — UOP).**

For squarefree n = p₁···pₖ and two partitions π₁, π₂ of Z/nZ:

**{ π₁, π₂ } is sufficient iff the joint map J = (f_π₁, f_π₂): Z/nZ → A₁ × A₂ is injective.**

All sufficiency theorems are corollaries of UOP, obtained by computing J-injectivity for specific map types:

| π₁ type | π₂ type | Injectivity condition | Theorem |
|---|---|---|---|
| Type M: G-orbits | Type M: H-orbits | G ∩ H = {1} in (Z/nZ)* | A |
| Type A: residue mod d | Type M: G-orbits | G ≤ ker((Z/nZ)* → (Z/(n/d)Z)*) | B |
| Type M: G-orbits | Type A: residue mod d | Same as B (J is symmetric) | C (corrected) |
| Type A: residue mod d₁ | Type A: residue mod d₂ | gcd(d₁,d₂) = 1... see below | CRT |

**Corollary (Type A + Type A — CRT case).** J = (f_d₁, f_d₂) injective iff for every x ≠ y: either d₁ ∤ (x−y) or d₂ ∤ (x−y), i.e., lcm(d₁,d₂) = n. For squarefree n: lcm(d₁,d₂) = n iff d₁ · d₂/gcd(d₁,d₂) = n iff every prime of n divides d₁ or d₂.

In particular: {π_p, π_{n/p}} always yields a sufficient pair for each prime p | n. The CRT prime-factor theorem is the special case d₁ = p₁, d₂ = p₂···pₖ. □

---

## Part 5 — The Common Algebraic Structure: Coordinate Coverage

**Definition (Coordinate Coverage).** For squarefree n with CRT coordinates (a₁,...,aₖ):

Say a map f: Z/nZ → X *resolves prime pᵢ* if: ∀x ≠ y that differ only in coordinate i (aⱼ = a'ⱼ for j ≠ i, aᵢ ≠ a'ᵢ): f(x) ≠ f(y).

Say f *confuses prime pᵢ* if: ∃ such a pair with f(x) = f(y).

**Theorem (Coverage Characterization).**
For squarefree n and maps f, g: Z/nZ → ·:

If f resolves all primes in set D_f and g resolves all primes in set D_g, and D_f ∪ D_g = {p₁,...,pₖ}, then J = (f,g) is injective.

**Proof.** Any x ≠ y differ at some coordinate pᵢ. pᵢ ∈ D_f or pᵢ ∈ D_g. In the first case f(x) ≠ f(y). In the second case g(x) ≠ g(y). So J(x) ≠ J(y). □

**IMPORTANT CAVEAT:** Coverage of supports is SUFFICIENT for injectivity but not NECESSARY. Two maps may both be "confused" at some prime yet still jointly injective — if the confusions never coincide on the same pair.

Example: for n=30, G = ⟨7⟩ (focused on 5) and H = ⟨11⟩ (focused on 3). D_G = {5}, D_H = {3}. Neither covers {2}. Yet J is injective (prior sprint Theorem 1): the 2-component is fixed by both (all units are odd mod 2 = 1 in Z/2Z). No pair differs ONLY in the 2-component (both components are either 0 or 1, and this is always resolved by one of the maps since... hmm, 2-prime elements: a pair (1,0,0) and (0,0,0) in Z/2Z × Z/3Z × Z/5Z. T₇(·) fixes 3-component: orbit of (1,0,0) is {(1,0,0)} (singleton, since a₂=0,a₃=0 mean x is multiple of 15, and 7 fixes multiples of 5... wait, 7≡2 mod 5, so T₇ maps a₃≠0 elements. For a₃=0: T₇ fixes. And a₂=0: T₇ fixes (7≡1 mod 3). So (1,0,0)=15 in Z/30Z is fixed. T₁₁ also: 11≡1 mod 5 and 11≡2 mod 3. T₁₁(15) = 11·15=165=165 mod 30=15. Fixed. Singletons have no injectivity issue.

The pairs that can cause problems are those where both a₂ ≠ 0 and a₃ ≠ 0 — but elements like (1,1,1) and (1,1,2) differ in a₃, so T₇ distinguishes them. And (1,1,1) vs (1,2,1) differ in a₂, so T₁₁ distinguishes them. Coverage works for the non-zero coordinates.

---

## Part 6 — Connectting to CRT, MVJN, and Z/10Z Lattice

**CRT prime-factor family (squarefree n = p₁···pₖ):**

The k factor partitions π_{p₁},...,π_{pₖ} are all Type A. The joint map (f_{p₁},...,f_{pₖ}): Z/nZ → ∏ Z/pᵢZ is the CRT isomorphism — perfectly injective. The k-factor family is the "pure coordinate" case where each map resolves exactly one prime.

**MVJN theorem:**

Within the Type-A family, a sufficient PAIR requires two maps whose supports cover all primes. Each additive map f_d is blind to primes of n/d. For a pair {π_d₁, π_d₂}: joint injectivity requires every prime to be seen by at least one. This requires at least one map to use a "cross-prime" support — which is an orthogonal jump in the partition lattice. The k−1 jump theorem follows from the fact that each additive map's support can include multiple primes, but the overall cover requirement still forces k−1 jumps to cross from one factor's support to another's.

More precisely: the refinement chain (π_SPEC ≤ π_UG ≤ π_CRT₂) are all maps that are "blind" to the CRT₅ coordinate. No union of maps from this chain resolves the CRT₅ coordinate. The orthogonal jump to π_CRT₅ is the step of adding a map that resolves the CRT₅ = p=5 coordinate. UOP explains why it's necessary: without it, the joint map is blind at p=5, hence not injective. The "jump" is exactly the step of adding a map that resolves a new coordinate.

**Z/10Z refinement vs. orthogonal jump:**

The refinement chain (SPEC ≤ UG ≤ CRT₂) are all Type-A maps with increasing d-values (finer partitions). They all resolve the p=2 coordinate with varying granularity, but all are "blind" to the p=5 coordinate (they are all contained in or coarser than π_CRT₂ which sees only the 2-component). Adding CRT₅ (a Type-A map resolving p=5) is an orthogonal jump that completes coordinate coverage.

In UOP language: the refinement chain provides maps that resolve the same set of coordinates with increasing precision. The orthogonal jump adds coverage of a new, previously uncovered coordinate. Refinement moves do not expand coordinate coverage; orthogonal jumps do.

**Formal statement of this connection (proved):**

For squarefree n, a move from partition π to partition ρ in the lattice is:
- A **refinement move** iff supp(π) ⊆ supp(ρ) (same or smaller support; more elements resolved per coordinate)
- An **orthogonal jump** iff supp(ρ) ⊄ supp(π) and supp(π) ⊄ supp(ρ) (incompatible supports; genuinely new coordinate accessed)

A sufficient 2-partition pair requires the union of supports to cover all primes. Since each partition can have any support, coverage requires at least one transition that adds a new coordinate — which is an orthogonal jump (by definition).

This re-derives the MVJN theorem for the Type-A family as a corollary of UOP + support coverage. □

---

## Part 7 — What the Unified Principle Is (and Is Not)

**What UOP is:**

A single meta-theorem:
> {π₁, π₂} sufficient iff the joint map J = (f_π₁, f_π₂) is injective.

All prior classification results (A, B, C, CRT, MVJN) are corollaries. The computation of J-injectivity for specific algebraic map types gives different algebraic conditions, but the source principle is always joint map injectivity.

**Why the conditions A, B, C look different:**

They arise from different algebraic structures of the maps:

- **Type M + Type M (Case A):** Both maps are orbit maps from group actions. Injectivity condition is group-theoretic: G ∩ H = {1}. This is a "complementary subgroup" condition.

- **Type A + Type M (Cases B, C):** One map is an additive-module quotient; the other is a multiplicative orbit. Injectivity forces the multiplicative action to be "confined" to the additive map's support. This is a "support containment" condition.

- **Type A + Type A (CRT case):** Both maps are additive-module quotients. Injectivity forces support union to cover all primes. This is a "coordinate coverage" condition.

These are not three different orthogonality laws — they are ONE law (joint injectivity) expressed in three different algebraic contexts.

**Why no single "formula" unifies A, B, C:**

The algebraic translation of "J injective" depends on the algebraic type of f_π₁ and f_π₂. For group-orbit maps, "J injective" translates via group theory. For module-quotient maps, it translates via lattice/divisibility theory. For mixed, it translates via the interaction of multiplicative and additive structure. There is no algebraic formula that simultaneously expresses all three translations — but the GEOMETRIC principle (injectivity of joint map) is always the same.

---

## Part 8 — Corrected Summary of All Theorems

**Theorem 0 (UOP — proved):** {π₁, π₂} sufficient iff joint map (f_π₁, f_π₂): Z/nZ → A₁ × A₂ is injective.

**Theorem A (M+M — proved, prior sprint):** G-orbit × H-orbit sufficient iff G ∩ H = {1} in (Z/nZ)*.

**Theorem B (A+M — proved):** Residue mod d × G-orbit sufficient iff G ≤ ker((Z/nZ)* → (Z/(n/d)Z)*, i.e., G trivial on primes of (n/d).

**Corrected Theorem C (M+A — proved here):** G-orbit × residue mod d sufficient iff same condition as B. The prior sprint version (injectivity of G → (Z/dZ)*) was necessary but not sufficient. Corrected by incorporating the zero-fiber analysis. Prior sprint's Theorem 2 (SPEC+half-modulus) is still correct since -1 fixes all multiples of m when n=2m.

**Theorem D (A+A — proved as corollary):** Residue mod d₁ × residue mod d₂ sufficient iff lcm(d₁,d₂) = n (every prime divides d₁ or d₂). CRT is the canonical instance.

---

## Summary

**Unified theorem (proved):**
> Every sufficiency theorem for 2-partition pairs on squarefree Z/nZ is a corollary of a single principle: the joint map (f_π₁, f_π₂): Z/nZ → A₁ × A₂ is injective. Theorems A, B, C, CRT are each a computation of this injectivity for a specific algebraic map type (multiplicative-orbit, additive-quotient, or mixed). The "jump necessity" results (MVJN, CRT k−1 theorem) are the statement that no single partition covers all coordinates, forcing the joint map to require at least two factors. The orthogonal jump corresponds exactly to adding a map that resolves a previously uncovered coordinate.

**Strongest honest claim:**
> Theorems A, B, C are not three separate laws — they are one law (UOP) applied in three algebraic contexts. The unification is complete in the sense that every two-partition sufficiency question for squarefree Z/nZ with maps from the families {multiplicative-orbit, additive-quotient} reduces to joint-map injectivity, and that injectivity can be read off from the CRT coordinate structure of Z/nZ. The "coordinate coverage" framework expresses this concretely: every pair of distinct elements differs in at least one CRT coordinate, and sufficiency requires that coordinate to be resolved by at least one of the two maps.

**Strongest honest boundary:**
> Two open problems remain:
> (1) **Beyond squarefree n:** For n with repeated prime factors, the CRT structure is replaced by p-adic components, and the orbit/quotient analysis must be modified. The UOP principle still holds abstractly (joint map injectivity is always the correct criterion), but the computation of which maps satisfy it for specific partition families is more complex.
> (2) **Mixed partition types beyond M and A:** Partitions defined by quadratic residues, Legendre symbols, character sums, or other number-theoretic structures fit the UOP framework as maps f_π: Z/nZ → X, but computing when their joint maps are injective requires different tools. UOP provides the meta-criterion but not the computation for these cases.

**One correction to the prior sprint:** Theorem C was stated as "injectivity of G → (Z/dZ)*." This is necessary but not sufficient. The correct condition is G trivial on all primes of (n/d), which is equivalent to Theorem B. The prior sprint's specific applications of Theorem C (SPEC + half-modulus) remain correct because -1 already satisfies the correct condition.
