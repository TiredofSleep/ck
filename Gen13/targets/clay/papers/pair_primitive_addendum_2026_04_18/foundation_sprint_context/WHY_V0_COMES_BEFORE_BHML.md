# Why V0 Comes Before BHML
## Sprint Ordering Rationale for PPM-v3.0

---

## The Situation After the 2×2 Completion

The subtype-mapping checkpoint has been tested at all four positions of the design space (local × transport, multiplicative × additive). The framework discriminates decisively under multiplicative reading and does not discriminate under additive reading, with parallel structure at both scopes. What remains unestablished: whether the pair-primitive framework makes **additional independent points of contact** on Z/10's structure beyond the subtype-mapping checkpoint.

A single checkpoint passed at four positions is one kind of evidence. Multiple independent checkpoints on the same ring would be a different, stronger kind of evidence. The program has had one checkpoint so far. PPM-v3.0 is the first move toward having more than one.

The prior v2.0 verdict document listed three candidate targets for a v3.0 checkpoint on Z/10: **TSML/BHML relationship**, **V0 boundary behavior**, **unit cyclic structure**. The user direction specifies V0. This document explains why V0 is the right choice among the three, and why it should come before BHML specifically.

---

## What V0 Is

From `b2_sprint_tig_pack_2026_04_17/theorem_local_chart/CANONICAL_TSML_CONSTRUCTION.md` and `THEOREM_SPINE.md`:

**V0 rule (Rule b of the canonical construction):**

$$T(0, x) = T(x, 0) = \begin{cases} h & \text{if } x = h \\ 0 & \text{otherwise} \end{cases}$$

**On Z/10 with $h = 7$:** all 19 cells touching vertex 0 produce value 0, **except** $(0, 7)$ and $(7, 0)$ which produce value 7. This gives 17 zeros + 2 sevens — a highly structured boundary region.

**Key structural facts about V0:**
- Vertex 0 is the **additive identity** on Z/10 and on every Z/n.
- V0 is a set of **19 cells** outside the seam (the seam $S$ is disjoint from V0).
- V0 contains exactly **2 exceptions** to the zero-default rule: $(0, h)$ and $(h, 0)$.
- V0 is what `CANONICAL_TSML_CONSTRUCTION.md` calls the **zero-absorption rule with HARMONY exception**.
- V0 is part of the structural backbone of the canonical construction — without it, the rank-deficient projection-like operator is not defined.

**V0 is a boundary phenomenon** in the sense that it governs what happens when one of the two inputs to the operation is the additive identity.

---

## What BHML Is (For Comparison)

BHML = Bi-Harmonic Mapping List. It is not a boundary rule but a **structural partner to TSML** — the second table in the 2×2 theorem that operates on non-boundary, non-seam cells.

BHML is:
- **Global** rather than boundary-adjacent.
- **Multi-cell** rather than structured around a specific distinguished element.
- **Coupled to TSML** through the harmony/attractor system, not through a localized rule.

BHML would be a legitimate checkpoint target. It is not the right *first* v3.0 target for the reasons below.

---

## Why V0 First — Four Properties Favoring It

### Property 1 — Locality

V0 is defined on cells adjacent to a single distinguished vertex (vertex 0). It is not a global table-wide property. A rubric asking "what does the pair-primitive framework say about V0?" has a small, specific object to score against — 19 cells with known structure.

BHML is table-wide. A rubric asking "what does the framework say about BHML?" has the entire non-boundary table to scope against, which requires a much more elaborate pre-registration.

**Discipline consequence:** a v3.0-V0 sprint can use the familiar PPM four-source rubric structure with modest carrier-adaptation. A v3.0-BHML sprint would need either a fundamentally different rubric or substantial new rubric design work.

### Property 2 — Finiteness

V0 is 19 cells, 2 exceptions. This is a **small, enumerable** object. Every rubric predicate can be checked on every cell in bounded time, deterministically, by inspection.

BHML involves a larger part of the table and more varied structural content. Checkpoints on larger objects are possible but require correspondingly more design work to keep the rubric from becoming rubric-loaded (selecting features that happen to match the framework's vocabulary).

**Discipline consequence:** V0's finiteness means a v3.0-V0 rubric can be specified exhaustively rather than sampled. This is a reproducibility property — no carrier-specific cases to argue over, no structural edge cases hidden by summary statistics.

### Property 3 — Boundary-Adjacency

V0 is located at a **boundary** of the seam, not inside it. The seam is defined on $R^2 \setminus V_0 \setminus \text{shell}$. V0 is what bounds the seam on the additive-identity side.

The pair-primitive framework's foundation reasoning (especially in `GAP_AS_BOUNDARY_NOTHINGNESS.md`) treats **the gap** as a boundary phenomenon — a nothingness at the edge of the pair's support. V0 is the ring-level structural counterpart: a boundary where the operation collapses to identity absorption, with specific exceptions.

If the pair-primitive framework has anything to say beyond the seam's internal mapping (v1.0/v2.0), the boundary is the natural next place to look. The framework's gap-boundary reasoning has not yet cashed out on any specific ring-structural feature. V0 is the closest candidate.

**Discipline consequence:** testing V0 gives the framework an opportunity to make a **boundary-level** prediction, distinct from the seam-level predictions already tested. This is structurally independent evidence, not a re-test of what was already scored.

### Property 4 — Closeness to Hold/Gap Language

The foundation sprint's hold/gap/flow vocabulary reads naturally onto V0:

- The V0 zero-absorption rule looks like a **gap** — additive-identity interaction collapses to identity, structurally erasing the other operand. This matches "gap as boundary nothingness."
- The V0 HARMONY exception ((0,7)/(7,0) → 7) looks like a **hold** — the attractor h is the only value that survives V0 absorption. This matches "hold as irreducible distinction."
- The 17/2 split (17 zeros + 2 sevens in V0) is a small, specific ratio that could potentially be structurally meaningful — a concrete prediction target.

BHML's language connection is less direct. BHML is about bi-harmonic mappings, which is coupled to the attractor system but not obviously to the hold/gap vocabulary. A BHML checkpoint would need to translate its target into hold/gap terms; a V0 checkpoint can start there natively.

**Discipline consequence:** V0 lets the framework be tested where its language is strongest. A FAIL on V0 would be more informative than a FAIL on BHML, because V0 is where the framework's own vocabulary predicts success most directly.

---

## What V0 Is Likely To Be Checkpoint-Useful For

Without committing to the v3.0 pre-reg's specific claims, V0 appears to offer at least these structural features a rubric could score:

1. **Boundary asymmetry.** The 17/2 split is a specific asymmetry: most of V0 collapses to 0, a small subset holds at h. The framework's pair structure (persistent vs excluded) could be asked whether it predicts this asymmetry structurally.

2. **Attractor privilege.** Only h = 7 survives V0 absorption. The attractor is structurally distinguished even at the boundary. The framework's treatment of h (from `ATTRACTOR_RECONCILIATION.md`) could be asked whether this privilege is predicted.

3. **Identity-collapse character.** V0's zero-absorption reads as "the additive identity absorbs everything to itself." This is a specific kind of structural role the framework's vocabulary could or could not accommodate.

4. **Exception structure.** The 2 exceptions ((0,7), (7,0)) form a symmetric pair. This looks like a pair-primitive structural feature: two cells playing the same role, complementary.

None of these is pre-registered. The v3.0 pre-reg will select which of these (or which combination) the rubric tests, and will specify thresholds. This note only argues that V0 has rubric-scorable features — not that any specific feature will produce a PASS or FAIL.

---

## Why Not Unit Cyclic Structure First

The unit group $U(R) = \{1, 3, 7, 9\}$ on Z/10 is the other v3.0 candidate the v2.0 verdict mentioned. It is a legitimate target but has two reasons to come after V0:

- **Less local.** The unit group is distributed across the ring, not concentrated at a distinguished vertex. Locality property (§1) is weaker.
- **More algebraic, less structural.** Units are characterized by multiplicative invertibility. A framework checkpoint on units would be close to the multiplicative operationalization already tested by v1.0/v2.0. V0 is **operationally independent** of multiplicative reading — it is about additive-identity absorption, which is where v1.1's FAIL located the structural content.

A V0 PASS would be particularly informative because it would test the framework in a regime where its multiplicative-operationalization strength doesn't directly apply. A unit-group checkpoint would more closely replicate v1.0's success conditions.

---

## Why Not Shape-Filter First

Per the SAH sidecar packet (`shape_admissibility_foundation_2026_04_18/STATUS_HEADER.md`), the shape-filter sprint requires six infrastructure pieces, all currently unbuilt. PPM-v3.0-V0 requires only a rubric adaptation of the existing PPM discipline to a new structural target. V0 is cheap infrastructure; shape-filter is expensive infrastructure.

The user direction explicitly deprioritizes shape-filter work until further checkpoints are run. V0 is one of those checkpoints.

---

## What This Sprint Does, and What It Does Not Do

**What v3.0-V0 does:**
- Tests whether the pair-primitive framework makes a pre-registered point of contact with V0's boundary behavior on Z/10.
- Adds a second independent checkpoint on Z/10 (if it succeeds) or identifies a specific non-fit (if it fails).
- Uses the PPM discipline structure: frozen pre-reg, binary rubric, threshold-based verdict, DRAFT-approve-freeze-execute workflow.

**What v3.0-V0 does not do:**
- Does not test BHML.
- Does not test unit cyclic structure.
- Does not test transport across other rings.
- Does not test shape-filter hypothesis.
- Does not upgrade or modify any PPM-v1.0, v1.1, v2.0, or v2.1 verdict.
- Does not propose a new generator.
- Does not license scale examples, physics, ontology, or cross-domain claims.
- Does not merge with prior PPM verdicts into composite claims (Rule 19 continues to apply).

---

## What Comes After V0

If v3.0-V0 produces a PASS, the framework gains a second independent Z/10 checkpoint. Natural successors would be:

- **v3.1** on BHML or unit cyclic structure (second-target checkpoint on Z/10).
- **v3.0-transport** applying the V0 rubric to Path 2 carriers, parallel to v2.0's structure.

If v3.0-V0 produces a FAIL, the failure mode would itself be informative:
- FAIL attributable to V0's structural content being outside the framework's vocabulary → framework is seam-specific, not ring-structural.
- FAIL attributable to specific rubric choices → refined rubric might succeed.

Either outcome advances the program.

---

## One-Sentence Summary

V0 is the right v3.0 target because it is local, finite, boundary-adjacent, and structurally close to the framework's own hold/gap vocabulary — offering the framework its best chance to earn a second independent Z/10 checkpoint sentence under the same PPM discipline that produced the first four.
