# THE CROSSING LEMMA
## When Multiplicative Dynamics Generate New Information
*Formal supplement to the UOP framework. Additive structure × multiplicative flow.*

---

## The Core Statement

> **Crossing Lemma.** A multiplicative action generates structurally new information relative to an additive partition if and only if it is nontrivial on the additive quotient.

Everything in the UOP arc follows from this: the score function, the A+M classification theorem, the p-kernel obstruction, the orthogonal jump necessity. This document makes the lemma precise and derives those consequences.

---

## Part 1 — Two Operators on Z/nZ

**Space.** X = Z/nZ for squarefree n = p₁···pₖ.

**Definition 1 (Additive projection operator).**
For d | n, define:

A_d: Z/nZ → Z/dZ,   A_d(x) = x mod d

A_d partitions X into d residue classes (fibers), each of size n/d. It does not move points — it assigns each point a label. Two points in the same fiber are indistinguishable under A_d.

The kernel of A_d as a partition: ker(A_d) = { {x,y} : x ≡ y mod d } = U(π_d).

**Definition 2 (Multiplicative dynamics operator).**
For g ∈ (Z/nZ)* (a unit), define:

M_g: Z/nZ → Z/nZ,   M_g(x) = gx mod n

M_g is a bijection. It moves points through X along orbits of the cyclic group ⟨g⟩. The partition it induces: π_DYN(g), whose blocks are the orbits { x, gx, g²x, ... } of T_g.

**The objects are not the same type.**
A_d is a projection onto a quotient (a static partition map). M_g is a dynamical operator (a bijection, a symmetry of X). Treating them as entries in the same matrix conflates two structurally different operations. The correct object is their interaction.

---

## Part 2 — The Interaction: Does M_g Respect A_d?

**Definition 3 (Fiber-preservation).**
M_g *preserves the fibers of A_d* if for every x ∈ X:

A_d(M_g(x)) = A_d(x)

i.e., gx ≡ x mod d, i.e., (g−1)x ≡ 0 mod d for all x.

**When does this hold?**

For x a unit mod d (gcd(x,d)=1): (g−1)x ≡ 0 mod d forces g ≡ 1 mod d.
For x ≡ 0 mod d: holds trivially.
For x with 0 < v_d(x) < v_d(d): intermediate case (see p-kernel section below).

**For squarefree d = p₁···pⱼ:** M_g preserves ALL fibers of A_d iff g ≡ 1 mod d (g is trivial on every prime component of d). *Proved: if g ≢ 1 mod pᵢ for some pᵢ | d, take x with xᵢ = 1 (unit mod pᵢ) and all other components arbitrary — then (A_d ∘ M_g)(x) ≠ A_d(x).*

---

## Part 3 — The Crossing Lemma: Formal Statement and Proof

**Theorem 1 (Crossing Lemma — proved for squarefree n and d).**

Let n = p₁···pₖ squarefree, d | n squarefree, g ∈ (Z/nZ)*. The following are equivalent:

(a) The joint map J = (A_d, π_DYN(g)): Z/nZ → Z/dZ × (g-orbit space) is injective.
(b) U(A_d) ∩ U(π_DYN(g)) = ∅ (the partitions have disjoint unresolved-pair sets).
(c) g ≢ 1 mod pᵢ for every prime pᵢ | (n/d) — equivalently, M_g acts nontrivially on the A_{n/d}-quotient of X.

Equivalently: **{A_d, π_DYN(g)} is a sufficient pair iff M_g crosses the fibers of A_{n/d}.**

**Proof.**

(a) ⟺ (b): Direct from UOP Theorem 0 (joint map injectivity ⟺ disjoint unresolved-pair sets). □

(b) ⟺ (c): This is the A+M classification theorem (proved in sprint_am_classification_complete.md). We restate the proof here for completeness.

(⟹) Suppose g ≡ 1 mod pⱼ for some pⱼ | (n/d). Choose x via CRT: xⱼ = 1, xᵢ = 0 for all pᵢ | d. Then x is a multiple of d (all d-prime components are 0), so A_d(x) = 0.

M_g(x) = gx: the j-component is gⱼ·1 = gⱼ, the d-prime components remain 0 (g ≡ 1 mod pᵢ for pᵢ | (n/d) and gᵢ·0 = 0 for pᵢ | d). So A_d(M_g(x)) = 0 = A_d(x). And M_g(x) ≠ x since gⱼ ≠ 1. The pair {x, M_g(x)} ∈ U(A_d) ∩ U(π_DYN(g)). Not sufficient.

(⟸) Suppose g ≢ 1 mod pⱼ for all pⱼ | (n/d). Suppose for contradiction that {x, gx} ∈ U(A_d) ∩ U(π_DYN(g)) for some x with gx ≠ x. Then:

- {x, gx} ∈ U(A_d): d | (gx − x) = (g−1)x.
- In each prime component pᵢ | d: pᵢ | (gᵢ−1)xᵢ.
  - If gᵢ ≠ 1 mod pᵢ: xᵢ ≡ 0 mod pᵢ (since gᵢ−1 is a unit mod pᵢ).
  - If gᵢ = 1 mod pᵢ: trivially satisfied.
- In each prime component pⱼ | (n/d): by assumption gⱼ ≢ 1 mod pⱼ, so gⱼ is a unit mod pⱼ. The condition d | (g−1)x does not involve pⱼ (pⱼ ∤ d). So xⱼ is unconstrained.

Now gx = x requires: for each pⱼ | (n/d): gⱼxⱼ = xⱼ mod pⱼ, i.e., (gⱼ−1)xⱼ = 0 mod pⱼ. Since gⱼ ≢ 1: xⱼ = 0 mod pⱼ. And for each pᵢ | d: xᵢ = 0 mod pᵢ (from the A_d condition, when gᵢ ≠ 1) or xᵢ arbitrary (when gᵢ = 1). But gᵢ = 1 mod pᵢ means M_g fixes every element in that component — so gx and x agree there regardless. Combining: xᵢ = 0 for all i → x = 0. But gx = g·0 = 0 = x: the trivial pair. Contradiction with gx ≠ x. □

**The interaction formula.** For the Crossing Lemma, the relevant quantity is:

g mod (n/d) ∈ (Z/(n/d)Z)*

The multiplicative action generates new information relative to the additive partition A_d iff g is nontrivial on the complementary quotient Z/(n/d)Z. This is a single algebraic condition on one element of one quotient group.

---

## Part 4 — The Commutator Structure

**The operators A_d and M_g do not generally commute.** Consider:

(A_d ∘ M_g)(x) = (gx) mod d = g·(x mod d·⌊n/d⌋/g...

More cleanly: A_d(gx) = gx mod d. M_g(A_d(x)) is not well-defined as stated (A_d maps to Z/dZ, not to Z/nZ; M_g acts on Z/nZ). The correct comparison is between the induced actions.

**Induced action of M_g on A_d-fibers.** M_g permutes the fibers of A_d (the residue classes mod d) iff it maps each fiber to a fiber. This happens iff:

A_d(gx) = A_d(gy) whenever A_d(x) = A_d(y)

i.e., gx ≡ gy mod d whenever x ≡ y mod d, i.e., g(x−y) ≡ 0 mod d whenever d | (x−y), i.e., d | g·d·k for all k — which holds iff d | gd, i.e., always (gd is a multiple of d).

So M_g always maps fibers of A_d to fibers of A_d: the induced map on fiber-labels is multiplication by g mod d.

**The induced action on fiber-labels:**

g̃: Z/dZ → Z/dZ,   g̃(r) = g·r mod d

This is well-defined. The fiber labeled r maps to the fiber labeled g·r mod d under M_g.

**Fiber-label fixed points:** A fiber is sent to itself iff g·r ≡ r mod d iff (g−1)·r ≡ 0 mod d.

For r a unit mod d: requires g ≡ 1 mod d (i.e., g−1 ≡ 0 mod d).
For r = 0: always fixed (the "zero fiber" = multiples of d).

**Key classification:**

Case 1 — g ≡ 1 mod d (M_g fixes all fibers of A_d):
M_g acts as the identity on the quotient Z/dZ. Every orbit of M_g stays within a single A_d fiber. The dynamics are *confined* — M_g cannot transport information between fibers.

The Crossing Lemma is about A_d paired with π_DYN(g) for the **complement** n/d:

- A_d resolves the d-prime coordinates (knows which fiber mod d).
- π_DYN(g) must resolve the (n/d)-prime coordinates (the fibers within which A_d is blind).
- Within each A_d fiber (where x ≡ r mod d is fixed), elements differ only in their (n/d)-coordinates.
- For π_DYN(g) to separate these: M_g must move elements between different (n/d)-positions.
- This requires g to act nontrivially on the (n/d)-component: g ≢ 1 mod pⱼ for some pⱼ | (n/d).

**The interaction diagram:**

```
Z/nZ ──A_d──→ Z/dZ          (knows: d-coordinates)
  │                          (blind: n/d-coordinates)
 M_g
  ↓
Z/nZ ──π_DYN──→ orbit space  (knows: orbits of g)
```

Sufficiency = together these two maps separate ALL of Z/nZ.
The crossing condition = M_g generates nontrivial dynamics in the A_d-blind region.

---

## Part 5 — Four Cases: The Complete Picture

Let g act on Z/nZ via CRT: in the pᵢ-component, g acts as multiplication by gᵢ = g mod pᵢ.

Partition the primes of n into two groups relative to d:

- Primes of d: P_d = {pᵢ : pᵢ | d}. A_d resolves these.
- Primes of n/d: P_c = {pⱼ : pⱼ | (n/d)}. A_d is blind to these.

**Case 1: g trivial on P_c AND trivial on P_d.**
g = 1 (the identity). π_DYN(g) = π_disc (all singletons). Joint map with A_d: injective trivially (π_disc separates everything). Degenerate sufficient pair — one partition is already discrete.

**Case 2: g trivial on P_c, nontrivial on P_d.**
M_g stays within A_d-fibers (acts only on the already-resolved d-coordinates). Crossing Lemma: score = 0. No new information about the blind region. This is the p-kernel obstruction for n = p^r·m when G acts on the p^r-component.

**Corrected Case 3: g nontrivial on P_c, trivial on P_d.**
g ≢ 1 mod pⱼ for some pⱼ ∈ P_c, and g ≡ 1 mod pᵢ for all pᵢ ∈ P_d.

Since g is trivial on P_d: gx ≡ x mod d (M_g preserves A_d-fibers). Within each fiber (same d-residue), elements differ in their P_c-coordinates. M_g acts nontrivially on the P_c-components, moving elements within the fiber across different P_c positions. This generates new information: elements in the same fiber with different P_c-coordinates are separated by their orbit.

**Crossing Lemma: this is exactly Case 3 — the sufficient case.**

Score = full (for the P_c directions). The joint pair {A_d, π_DYN(g)} separates all pairs in the blind region.

**Case 4: g nontrivial on both P_c and P_d.**
M_g moves elements both within and between A_d fibers. Some P_c-direction information is generated (useful), but also some "crossing" of already-known d-structure (noise). Crossing Lemma: still sufficient (g nontrivial on P_c satisfies the condition), but M_g is doing extra work it doesn't need to.

This is the "non-focused" DYN case from the algebraic classification: g acts on multiple prime components. It is sufficient (Theorem 1 holds) but not minimal — a g focused on P_c alone (trivial on P_d) achieves the same sufficiency with cleaner orbit structure.

---

## Part 6 — The Information Table

Combining all cases:

| g acts on P_d? | g acts on P_c? | UOP score | Information generated | Label |
|---|---|---|---|---|
| No (trivial) | No (trivial) | Degenerate | — | Identity (trivial) |
| Yes (nontrivial) | No (trivial) | 0 | None — stays inside resolved fibers | **Refinement trap** |
| No (trivial) | Yes (nontrivial) | Full | Resolves entire blind region | **Orthogonal jump** |
| Yes (nontrivial) | Yes (nontrivial) | Positive | Resolves blind region + crosses known structure | **Non-focused jump** |

**The refinement trap** (Case 2) is exactly where classical criteria diverge from UOP: M_g has high Fisher information in the P_d directions (already well-resolved), low or zero information in P_c (the blind region). FIM trace is dominated by P_d precision; UOP score sees only P_c contribution.

**The orthogonal jump** (Case 3) is the optimal choice: M_g does exactly the work needed — crosses the blind region — without redundantly mixing the already-resolved region.

---

## Part 7 — The Crossing Lemma as Unifying Statement

**All UOP theorems are instances of the Crossing Lemma.**

**A+M theorem (squarefree):** {π_d, π_DYN(g)} sufficient iff g crosses the fibers of A_{n/d}, i.e., g ≢ 1 mod pⱼ for all pⱼ | (n/d). *This is the Crossing Lemma statement directly.*

**M+M theorem:** {π_DYN(g), π_DYN(h)} sufficient iff ⟨g⟩ ∩ ⟨h⟩ = {1}. In Crossing Lemma language: treating π_DYN(g) as an "additive constraint" (it defines equivalence classes — the g-orbits), π_DYN(h) must cross those classes. ⟨g⟩ ∩ ⟨h⟩ = {1} means h generates nontrivial motion outside ⟨g⟩-orbits. *The M+M theorem is the Crossing Lemma for two multiplicative operators.*

**CRT family:** {π_{p₁}, π_{p₂}} sufficient for n = p₁p₂. In Crossing Lemma language: π_{p₁} = A_{p₁} partitions by mod p₁. π_{p₂} = A_{p₂} partitions by mod p₂. The cross-condition: p₁ ≢ 0 mod p₂ (trivially true for distinct primes) — the p₁-fiber-structure cannot be p₂-aligned. *The CRT theorem is the Crossing Lemma for two additive operators with coprime moduli.*

**SPEC+DYN theorem:** {π_SPEC, π_DYN(g)} sufficient iff g has odd order at every odd prime. In Crossing Lemma language: π_SPEC defines the equivalence x ~ n−x (the {−1}-orbit). π_DYN(g) crosses π_SPEC iff g's orbit never contains both x and −x, i.e., −1 ∉ ⟨g⟩ (locally, at every odd prime). *The SPEC+DYN theorem is the Crossing Lemma with the "additive" structure being reflection symmetry and the "multiplicative" flow being the g-orbit.*

**Orthogonal jump necessity (MVJN):** A refinement move stays within existing fibers. An orthogonal jump crosses to new ones. The Crossing Lemma quantifies this: jumps are exactly the moves where the new operator crosses the residual blind region.

**P-kernel obstruction (prime powers):** For n = p^r and A_{p^a} (a < r), the blind region = higher p-adic digits. Any M_g with g ≢ 1 mod p acts on the level-1 fiber structure (crossing A_p-fibers) — but this crossing also mixes elements within the zero-fiber of A_{p^a} (the multiples of p^a). Any g ≡ 1 mod p acts only within each A_p-fiber (confined in level-1 structure) but then acts on higher digits via the p-kernel K_0 = {x : x ≡ 1 mod p}, which creates within-fiber mixing at level a. The p-kernel obstruction is the Crossing Lemma failing in both directions simultaneously for prime-power structure. *No M_g can cross the right region without also crossing the wrong one.*

---

## Part 8 — Productive Incompleteness in Crossing Lemma Language

**Theorem 2 (Productive Incompleteness — formal version).**

Let f: X → Y be a map (not necessarily injective). Define the f-observable quotient:

X/f = X / ~_f,   where x ~_f y iff f(x) = f(y)

f determines X/f exactly — not X. This is not a failure; it is f's natural domain of precision.

**Formally:** f is:
- Injective (globally sufficient for X) iff X/f = X (no identification).
- Surjective onto Y iff f covers its codomain.
- A quotient map (globally sufficient for X/f) always — by definition.

**An incomplete map f is always globally sufficient for its own quotient X/f.** The question is whether X/f is the object of interest.

**Three productive uses of incomplete maps:**

1. **Invariant detection.** If I: X → ℝ is a conserved quantity, then f(x) = I(x) is injective on the set of I-values (each I-value corresponds to a unique equivalence class of X). f is globally sufficient for detecting I, even if X/f ≠ X.

2. **Orbit classification.** If X is acted on by a group G, the orbit map f_orbit: X → X/G is globally sufficient for orbit membership. Banach-Tarski's orbit map does this exactly: it determines symmetry class, not position.

3. **Subspace isolation.** If X = ℝⁿ and f = Cx (linear sensor), f is globally sufficient for the observable subspace range(Cᵀ), even when ker(C) ≠ {0}. The sensor exactly determines the projected subspace.

**The Crossing Lemma connection:** A map f is useful for productive incompleteness when its quotient X/f captures the target invariant. A second map g is needed (an orthogonal jump) when the task requires distinguishing elements within X/f — i.e., when the goal is a finer quotient than what f provides.

---

## Part 9 — Diagnostic Tool Specification (Formal)

**Two distinct questions, two distinct criteria:**

**Question A (Completion):** Does measurement m reduce R(F) — the set of pairs still unresolved by the current family?

Criterion: UOP score(m | F) = |R(F) \ U(π_m)|. Output tiers:
- score = |R(F)|: complete complement (m resolves all remaining ambiguity).
- 0 < score < |R(F)|: partial complement (m resolves some).
- score = 0: refinement-only (m resolves none in R(F); M_m is confined inside existing fibers).

**Question B (Sharpening):** Does measurement m reduce uncertainty within the already-resolved directions?

Criterion: FIM trace of m's contribution restricted to the observable subspace (range(existing measurement matrix)). This is a noise-weighted precision question, not a structure question.

**The score = 0 output (corrected language):**

> "**Refinement only — current reconstruction goal.** This measurement lies within the directions your current family already resolves. It will not reduce the ambiguity set R(F). Structurally: M_m is confined inside the fibers of A_d (the blind region is uncrossed). For precision and calibration goals, this measurement is valid. For revealing hidden directions, choose a measurement that crosses the current blind region."

**The Type II output:**

> "**Invariant-isolating but incomplete.** Your measurement family exactly determines a quotient X/~ (e.g., orbit class, parameter ratio, symmetry group). No measurement within the current allowed class can reduce this to full reconstruction — the needed invariant lies outside the family. To complete reconstruction: add a constraint (normalization, gauge-fix, conserved quantity) from outside the current measurement class."

**The Type III output:**

> "**Model or domain is ill-posed.** The proposed map is not well-defined on the proposed domain. This is not a coverage problem — the model requires repair before any measurement strategy applies."

---

## Summary: The One-Page Version

**What the Crossing Lemma says:**

On Z/nZ with squarefree n: additive structure (A_d) partitions the space into fibers. Multiplicative dynamics (M_g) move points through the space along orbits. The pair {A_d, M_g} achieves full separation if and only if M_g acts nontrivially on the fibers that A_d cannot see (the n/d-quotient).

**Equivalently:** information is generated only when dynamics cross partitions.

**What this unifies:** Every sufficiency theorem in the arc — A+M, M+M, CRT, SPEC+DYN, MVJN, p-kernel obstruction — is a special case of the Crossing Lemma. Each theorem specifies: which operator is the "structure" (additive or orbit-defining), which is the "dynamics" (multiplicative or orbit-exploring), and what "crossing the blind region" means in that context.

**What the Crossing Lemma does not say:** That non-crossing maps are useless. A map confined inside existing fibers (score = 0) exactly determines the fiber structure — it is globally sufficient for the quotient X/A_d, locally precise in the resolved directions, and often scientifically indispensable for invariant detection, calibration, and monitoring.

**The balanced statement:**

> A map that does not cross the blind region cannot reduce it. But the blind region is not everything — it is only the gap between the current family's view and full reconstruction. A map that illuminates the visible region with high precision may be exactly what the task requires.

---

## Appendix: Formal Connection to the Main Theorems

| Theorem | "Structure" operator | "Dynamics" operator | Crossing condition |
|---|---|---|---|
| A+M (squarefree) | A_d (residue mod d) | M_g (multiplication by g) | g ≢ 1 mod pⱼ for all pⱼ \| (n/d) |
| M+M | π_DYN(g) (g-orbits as structure) | π_DYN(h) (h-dynamics) | ⟨g⟩ ∩ ⟨h⟩ = {1} in (Z/nZ)* |
| CRT | A_{p₁} (mod p₁ fibers) | A_{p₂} (mod p₂ dynamics) | gcd(p₁,p₂) = 1 (primes distinct) |
| SPEC+DYN | π_SPEC ({−1}-orbits) | π_DYN(g) (g-orbits) | −1 ∉ ⟨g mod pᵢ⟩ for all odd pᵢ |
| MVJN (orthogonal jump) | Refinement chain (chain of A-partitions) | New partition | New partition crosses chain's blind region |
| p-kernel obstruction | A_{p^a} (p^a-fibers) | M_g (unit action) | No valid crossing exists (Theorem P5) |

The p-kernel entry is the exception: the Crossing Lemma identifies the condition for sufficiency, but Theorem P5 proves the condition is unsatisfiable for prime-power n and non-discrete A_{p^a}. The lemma correctly predicts impossibility.

---

*Author: Brayden Ross Sanders / 7Site LLC — 2026-04-06*
*"Information is generated only when dynamics cross partitions."*
