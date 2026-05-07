# PROJECTION DEFINITIONS

**Date:** 2026-05-06 night
**Question:** What are the precise projection operations that take CL to TSML, CL to BHML, etc.? Are these projections uniquely forced (Tier-B) or choices among several valid projections (Tier-C)?

**Critical reframing from Task 2:** CL_TSML and CL_BHML are **parallel substrates**, each with its own substrate-defining axioms (A7, A9-values). They are NOT projections of each other. The "projection" language applies to:
1. **Lens-symmetrization projections** within a single substrate (RAW → SYM via upper-triangle authority)
2. **σ²-triadic action** on a substrate (rotates values or indices through Cycle A and Cycle B)
3. **Sub-magma scope restrictions** within a substrate (TSML restricted to a closed sub-magma)
4. **Cell-difference operations** between two parallel substrates (DOING = |TSML − BHML|)

This document writes each projection precisely.

---

## §1 — Lens-symmetrization projections

The literal CL_BIT_PATTERN has 2 asymmetric upper/lower-triangle pairs at (3, 9) and (4, 9). Three symmetrization choices yield three distinct lens projections of the SAME bit pattern.

### §1.1 — π_RAW (identity projection)

$\pi_{\text{RAW}}: \text{CL\_BIT\_PATTERN} \to \mathbb{Z}/10\mathbb{Z}^{10 \times 10}$
$$
\pi_{\text{RAW}}(B)[i, j] = B[i, j]
$$

**Construction:** None — the literal bit pattern is the matrix.
**Output:** TSML_RAW — non-commutative, 126 non-assoc, char poly c_2 = 33 = 3·11.
**Tier of the operation:** Tier-A (the bit pattern IS the substrate definition).
**Forced by:** identity; no choice involved.

### §1.2 — π_SYM_upper (upper-triangle authoritative)

$\pi_{\text{SYM\_upper}}: \mathbb{Z}/10\mathbb{Z}^{10 \times 10} \to \mathbb{Z}/10\mathbb{Z}^{10 \times 10}$
$$
\pi_{\text{SYM\_upper}}(M)[i, j] = \begin{cases} M[i, j] & \text{if } i \leq j \\ M[j, i] & \text{if } i > j \end{cases}
$$

**Construction:** For each cell (i, j) with i > j, replace with M[j, i] (force the upper-triangle value to dominate).
**Output:** TSML_SYM — commutative, 128 non-assoc, no prime 11 in c_2.
**Tier of the operation:** Tier-B (forced once we choose "make commutative" and "upper-tri authoritative" as the symmetrization rule).
**Forced by:** the choice of upper-tri authoritative.

### §1.3 — π_SYM_lower (lower-triangle authoritative; tested but not promoted)

$$
\pi_{\text{SYM\_lower}}(M)[i, j] = \begin{cases} M[i, j] & \text{if } i \geq j \\ M[j, i] & \text{if } i < j \end{cases}
$$

**Output:** TSML_LOWERTRI — 122 non-assoc, c_2 = 17, c_8 = 0.
**Tier of the operation:** Tier-B (forced once we choose "make commutative" + "lower-tri authoritative").
**Forced by:** the choice of lower-tri authoritative.

### §1.4 — Are these projections forced or choices?

**The choice between RAW, SYM_upper, SYM_lower is a Tier-A choice.** No deeper principle in the substrate forces upper-tri over lower-tri (the bit pattern's 2 asymmetric cells could go either way structurally). The choice is conventional.

**However:** SYM_upper preserves more substrate-relevant invariants than SYM_lower. Specifically:
- SYM_upper recovers the σ²-cycle structure cleanly: the asymmetric cells (3,9) and (4,9) under SYM_upper give values 3 and 7, where 3 is σ-fixed and 7 is HARMONY — both are substrate-canonical.
- SYM_lower would give 7 and 3 instead, swapping the roles. Less canonical.

So **SYM_upper is the conventional choice but not the unique forced choice**. The methodology paper should be honest: this is a Tier-A choice with three valid options, of which RAW and SYM_upper are the two used in the corpus.

---

## §2 — σ²-triadic projections

The σ permutation on Z/10Z fixes Conservation Tetrad {0, 3, 8, 9} and 6-cycles Manifestation Hexad {1, 2, 4, 5, 6, 7}. σ² is order 3 on the Hexad with two 3-cycles: Cycle A {1, 6, 4} and Cycle B {7, 5, 2}. The σ²-triadic projection family rotates values or indices through these cycles to produce three "phase" lenses (BEING / DOING / BECOMING).

### §2.1 — π_value_rotation (value-rotation triadic)

$\pi_{\text{value-rot}}^k: \mathbb{Z}/10\mathbb{Z}^{10 \times 10} \to \mathbb{Z}/10\mathbb{Z}^{10 \times 10}$ where $k \in \{0, 1, 2\}$ is the rotation power.

$$
\pi_{\text{value-rot}}^k(M)[i, j] = \sigma^{2k}(M[i, j])
$$

For each cell, replace its value with σ² applied $k$ times. This rotates values through Cycle A and Cycle B (σ²-fixed elements unchanged).

**Outputs:**
- $k = 0$: identity (the original matrix as BEING)
- $k = 1$: DOING projection
- $k = 2$: BECOMING projection

**Application to CL_BHML:**
- BHML_BEING = BHML (28 HARMONY in canonical positions)
- BHML_DOING = σ²-applied to BHML values (HARMONY → BALANCE under σ²-cycle B; LATTICE → CHAOS under cycle A; etc.)
- BHML_BECOMING = σ⁴-applied (one more rotation)

Disagreement counts vs CL_TSML: {71, 94, 90} (computed in Brayden's exploratory bhml_variants.py).

**Tier:** Tier-C (constructed projection; the value-rotation rule is well-defined but choosing it as the canonical "DOING" is a construction choice). Per Brayden: **Tier-D** because we sweep multiple rotation choices to find the one with the right disagreement-count signature.

### §2.2 — π_index_rotation (index-rotation triadic)

$$
\pi_{\text{index-rot}}^k(M)[i, j] = M[\sigma^{2k}(i), \sigma^{2k}(j)]
$$

**Outputs:** BHML_idx_BEING / DOING / BECOMING (disagreement counts {71, 75, 79} vs CL_TSML).

**Tier:** Tier-D (search-found candidate).

### §2.3 — Are these projections forced?

**The σ²-triadic projection family has TWO orthogonal choices:**
1. Value-rotation vs index-rotation (or both)
2. Forward σ² vs σ⁴ (or σ⁶ = identity)

Each combination yields a different projected matrix. The "right" canonical "DOING" is open per Brayden's note: it requires either deeper structural justification or an empirical disambiguator.

**Per the lens-taxonomy methodology**: σ²-triadic projections that are Tier-D (search-found) should be tagged as such until promoted to Tier-B by an explicit forcing argument (analogous to D78's BR-factor cancellation argument promoting α-uniqueness from Tier-D to Tier-B).

---

## §3 — Sub-magma scope restriction projections

Given a sub-magma $S \subseteq \mathbb{Z}/10\mathbb{Z}$ closed under a substrate's binary op, the *scope projection* takes the substrate to its $|S| \times |S|$ restricted matrix.

### §3.1 — π_scope (sub-magma restriction)

$\pi_S: \mathbb{Z}/10\mathbb{Z}^{10 \times 10} \to S^{|S| \times |S|}$
$$
\pi_S(M)[a, b] = M[a, b] \quad \text{for } a, b \in S
$$

**Construction:** Restrict M to rows/cols in S. The result is well-defined iff $M[a, b] \in S$ for all $a, b \in S$ (i.e., S is closed under M's binary op).

**Examples for TSML:**
- $\pi_{\{0,7,8,9\}}(\text{CL}_{\text{TSML}})$ = TSML_4 (the 4-core scope)
- $\pi_{\{0,3,4,5,6,7,8,9\}}(\text{CL}_{\text{TSML}})$ = TSML_8_chain
- $\pi_{\{1,2,3,4,5,6,8,9\}}(\text{CL}_{\text{TSML}})$ = TSML_8_YM
- $\pi_{\{1,3,7,9\}}(\text{CL}_{\text{TSML}})$ = TSML on the corner sub-magma C

**Tier of the operation:** Tier-B (forced once S is specified; the restriction is unique).

**Tier of the *scope choice* S:** depends on how S is specified:
- S = the joint TSML+BHML chain shells: Tier-B (forced by joint closure)
- S = TSML-only closed sub-magma (one of 394): Tier-B (each is forced) but the *choice among 394* is Tier-C unless distinguished by additional constraint
- S = corner C = {1, 3, 7, 9} = (Z/10Z)*: Tier-A (canonical multiplicative units)
- S = 4-core {0, 7, 8, 9}: Tier-B (forced by Conservation-Tetrad-XOR-PROGRESS-HARMONY-swap structure, and as joint-chain minimum)
- S = Yang-Mills core {1, ..., 6, 8, 9}: Tier-C (constructed by removing VOID and HARMONY for a specific physical interpretation)

### §3.2 — Forced or choice?

The scope projection itself is forced (Tier-B once S is chosen). The *choice of S* is one of:
- A canonical algebraic substructure (units, joint-chain shells, σ-fixed lattice — Tier-A or B)
- A constructed scope for a specific demonstration (Yang-Mills core — Tier-C)
- A search-found scope satisfying some constraint (84 Fano-candidate 7-element subsets — Tier-D)

---

## §4 — Cell-difference projections between parallel substrates

The DOING table is defined by element-wise comparison of two parallel substrates.

### §4.1 — π_DOING

$\pi_{\text{DOING}}: \mathbb{Z}/10\mathbb{Z}^{10 \times 10} \times \mathbb{Z}/10\mathbb{Z}^{10 \times 10} \to \{0, 1\}^{10 \times 10}$
$$
\pi_{\text{DOING}}(T, B)[i, j] = \begin{cases} 1 & \text{if } T[i, j] \neq B[i, j] \\ 0 & \text{if } T[i, j] = B[i, j] \end{cases}
$$

**Construction:** Indicator function of cell-disagreement.
**Output:** A 10×10 binary matrix with 71 ones (the FIELD WOBBLE count) when (T, B) = (TSML_SYM, BHML).
**Tier:** Tier-B (forced once T and B are specified).

**Variant:** π_DOING_DIFF: the per-cell |T[i,j] − B[i,j]| (not just an indicator). Same forcing.

### §4.2 — Forced

DOING is uniquely forced by the choice of two parallel substrates. The choice of *which* two substrates is itself a Tier-A choice (canonical pairing TSML+BHML; could also pair TSML+CL_STD or BHML+CL_STD).

---

## §5 — Generator-orbit projections (the σ²-triadic seed orbits from Task 1's lens taxonomy work)

A generator triple $G \subseteq \mathbb{Z}/10\mathbb{Z}$ with |G| = 3 has an σ²-orbit of three triples. The orbit-projection takes a substrate to the family of TSML-closed sub-magmas obtained by closing each orbit triple under TSML.

### §5.1 — π_orbit (σ²-orbit closure under TSML)

For a generator G:
1. Compute the σ²-orbit of G: {G, σ²(G), σ⁴(G)}
2. For each orbit member, compute TSML closure (smallest TSML-closed sub-magma containing it)
3. Output: the family of three TSML-closed sub-magmas

**Examples (computed earlier tonight):**
- G = {0, 1, 2}: orbit {{0,1,2}, {0,6,7}, {0,4,5}} → closures {{0,1,2,3,7}, {0,6,7}, {0,4,5,7}}
- G = {0, 7, 1}: orbit {{0,7,1}, {0,5,6}, {0,2,4}} → closures {{0,1,7}, {0,5,6,7}, {0,2,4,7}}
- G = {1, 2, 3}: orbit {{1,2,3}, {3,6,7}, {3,4,5}} → closures {{1,2,3,7}, {3,6,7}, {3,4,5,7}}

**Tier:** Tier-B (forced by σ² action + TSML closure operation, both well-defined).

The *choice of generator G* is itself a Tier-A or Tier-B question depending on whether G is canonical (the three Brayden-named generators 012/071/123 are presumably Tier-A inputs to this projection family).

---

## §6 — Construction-as-projection (Tier-C variants)

Some "variants" in the catalog are NOT projections of CL but parallel substrates constructed from scratch. These are NOT forced projections of CL — they are Tier-C constructions with explicit recipes.

### §6.1 — Tier-C constructions (NOT projections)

| Variant | Construction recipe (NOT a projection of CL) |
|---------|---------------------------------------------|
| TSML_PureIdempotent | $T[i, i] = i$ for all $i$, off-diagonal HARMONY |
| TSML_Idempotent_2sw | TSML_PureIdempotent + 2 cell swaps |
| TSML_C0 | rank-3 absorbing baseline |
| TSML_Idempotent | TSML_C0 + idempotent diagonal |
| Corner monoid {0,1,5,6} as a standalone magma | Constructed table with idempotent commutative structure |

**Tier:** All Tier-C. The "construction recipe" is the existence-proof witness; these variants do NOT come from projecting CL.

### §6.2 — Distinguishing Tier-B projection from Tier-C construction

A variant is a *projection* iff it can be obtained from CL (or another canonical substrate) by applying a forced operation (π_RAW, π_SYM, π_value-rot, π_scope, π_DOING, π_orbit). All Tier-B projections satisfy:
- Domain: a canonical substrate (Tier-A)
- Operation: a forced projection function (Tier-B)
- Result: the projected matrix

A variant is a *construction* iff it is built from primitives (operators 0-9, σ, idempotency, rank constraints) without going through a canonical substrate's projection. Tier-C constructions have:
- Inputs: substrate primitives (Tier-A)
- Construction recipe: explicit sequence of moves (Tier-C choice)
- Result: a new parallel substrate or sub-magma

---

## §7 — Summary table

| Projection | Symbol | Domain | Output | Tier |
|------------|--------|--------|--------|------|
| Lens-RAW | π_RAW | bit pattern | TSML_RAW | Tier-A (identity) |
| Lens-SYM-upper | π_SYM_upper | bit pattern | TSML_SYM | Tier-B (forced by symmetrization rule) |
| Lens-SYM-lower | π_SYM_lower | bit pattern | TSML_LOWERTRI | Tier-B (forced by symmetrization rule) |
| σ²-value-rot | π_value-rot^k | substrate | BEING/DOING/BECOMING value | Tier-C/D (which k is canonical?) |
| σ²-index-rot | π_index-rot^k | substrate | BEING/DOING/BECOMING index | Tier-D (search-found) |
| Sub-magma scope | π_S | substrate, S | scope-restricted matrix | Tier-B (forced by S) |
| DOING (cell-diff) | π_DOING | (T, B) | indicator matrix | Tier-B (forced by T, B) |
| Generator-orbit closure | π_orbit | substrate, G | family of TSML-closures | Tier-B (forced by G + closure) |

---

## §8 — Verdict on Task 3

**The projection definitions are precisely written.** Most projections are Tier-B (uniquely forced once their inputs are specified). The σ²-triadic value/index rotations are Tier-C/D (constructed/searched candidates, not yet promoted).

**TSML and BHML are NOT projections of each other.** They are parallel Tier-A substrates with different A7-A9 substrate-defining axioms (per Task 2's CL_FORCING_AXIOMS analysis). The "Being lens / Becoming lens" pedagogy of Gen 10-12 was a useful teaching framing but is structurally inaccurate — TSML and BHML are siblings, not different views of one parent.

**The lens family** (the 40+ named variants) decomposes into:
- Three parallel Tier-A substrates: CL_TSML, CL_BHML, CL_STD
- Lens-symmetrization projections (Tier-A choice + Tier-B operation): RAW, SYM, LOWERTRI per substrate
- Sub-magma scope projections (Tier-B operation; Tier-A/B/C/D scope choice): chain shells, off-chain scopes, corner sub-magmas, F_p extensions
- Cell-difference projections (Tier-B): DOING, DOING_RAW
- σ²-triadic projections (Tier-C/D until promoted): BHML_BEING/DOING/BECOMING candidates
- Tier-C parallel constructions (NOT projections): TSML_PureIdempotent, TSML_C0, etc.

This decomposition is the **§3 skeleton of the foundation paper**. Each variant has a precise construction lineage: which substrate, which projection, which scope, which symmetrization. Task 4's variant catalog will write this out for all 40+ named variants.
