> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\SIMPLIFICATION_PYRAMID.md → papers\morphotic_braid\explorations\support\SIMPLIFICATION_PYRAMID.md

# The Simplification Pyramid — Five Layers

**Status:** [META-STRUCTURE — DERIVED FROM INVARIANT MATRIX]
**Date:** 2026-04-23 (late evening session)
**Source:** Brayden's meta-task: "Make that one [the invariant matrix] the base foundation and build up layered on top smaller and smaller to a point. Build a pyramid of simplification ladder."

## The idea

Take the 10×10 invariant matrix as Layer 0. Build successively smaller quotient matrices on top of it. Each layer aggregates base cells according to a structural partition. The tag at each reduced cell reports the **dominant base-cell characteristic** and the fraction of base cells exhibiting it.

**Uniform cells (100% of base cells share one tag)** are theorem-candidates — regions of the framework where the partition cleanly captures behavior.

**Mixed cells (top tag < 50%)** are regions where the partition doesn't align with structure; a different partition or finer analysis is needed.

The pyramid ends at Layer 4 — the 1×1 apex, which is the distribution over the entire framework.

## Layer 0 — Base (10×10)

The full invariant matrix. 100 cells. See `INVARIANT_MATRIX.md`.

## Layer 1 — Regularity Class Quotient (4×4)

**Partition from `doubly_regular_core.md`:** {D=doubly-regular, P=comp-half, H=braid-half, A=full-anchor}, sizes {5, 1, 1, 3}.

| | **D** (5) | **P** (3) | **H** (7) | **A** {0,8,9} |
|---|---|---|---|---|
| **D** | *successor* (32%) · 25 cells | *H\|bif* (60%) · 5 | *H\|bif* (80%) · 5 | *void_id* (33%) · 15 |
| **P** | *H\|bif* (60%) · 5 | *self_enc* (**100%**) · 1 | *H\|bif* (**100%**) · 1 | *void_id* (33%) · 3 |
| **H** | *H\|bif* (80%) · 5 | *H\|bif* (**100%**) · 1 | *H\|bif* (**100%**) · 1 | *exchange* (33%) · 3 |
| **A** | *void_id* (33%) · 15 | *void_id* (33%) · 3 | *exchange* (33%) · 3 | *void_id* (44%) · 9 |

**Reading:**

- **(P, P) cell:** 1 base cell, 100% self_encounter. This is (3,3) — PROGRESS² = COLLAPSE in BHML.
- **(P, H) and (H, P) cells:** each has 1 base cell, both 100% harmony_bifurcation. These are (3,7) and (7,3) — PROGRESS and HARMONY cross, and TSML forces 7 while BHML sends to 4. **Clean theorem-candidate.**
- **(H, H) cell:** 1 base cell, 100% harmony_bifurcation. This is (7,7) — HARMONY² = BREATH in BHML, but TSML = 7. **The HARMONY self-encounter is the archetype of bifurcation.**
- **(D, H) and (H, D) cells:** 80% harmony_bifurcation. Five base cells each, only one breaks pattern. Strong class-uniform behavior.
- **(D, D) cell:** 32% successor as top tag. This is mixed — 25 base cells with five top behaviors. The doubly-regular core is internally diverse; the partition doesn't capture what distinguishes its sub-behaviors.

**Layer 1 structural observation:** The H (HARMONY) class and the P (PROGRESS) class are tiny (1 element each), but every cell they participate in has uniform harmony_bifurcation behavior. **The half-regular operators are bifurcation generators.** This is a cleaner restatement of the fact that HARMONY and PROGRESS are the two operators that straddle the σ/BHML regularity boundary.

## Layer 2 — Fruit Cycle Quotient (3×3)

**Partition from TIG framework narrative:** {Cr = Creation {1,3,7,9}, Ds = Dissolution {2,4,6,8}, Ce = Center {0,5}}, sizes {4, 4, 2}.

| | **Cr** (4) | **Ds** (4) | **Ce** (2) |
|---|---|---|---|
| **Cr** | *H\|bif* (44%) · 16 cells | *H\|bif* (50%) · 16 | *void_id* (38%) · 8 |
| **Ds** | *H\|bif* (50%) · 16 | *H_unif* (38%) · 16 | *void_id* (50%) · 8 |
| **Ce** | *void_id* (38%) · 8 | *void_id* (50%) · 8 | *void_id* (50%) · 4 |

**Reading:**

- **Cr × Ds cells (both directions):** dominated by harmony_bifurcation at 50%. Creation-meets-Dissolution is where TSML collapses to 7 while BHML preserves direction — the measurement lens hides the Creation/Dissolution distinction that BHML preserves.
- **Ds × Ds:** dominated by harmony_uniform at 38%. Dissolution self-interaction is where both tables agree on 7 (the most fully-collapsed region).
- **Cr × Cr:** dominated by harmony_bifurcation at 44%, but only weakly — the Creation cycle contains all four regularity classes (1 is D, 3 is P, 7 is H, 9 is A), so this cell is internally heterogeneous.
- **Everything involving Ce (VOID + BALANCE center):** dominated by void_identity — these cells inherit the VOID row/column pattern.

**Layer 2 structural observation:** The Fruit cycle partition does *not* produce a clean split. Dominant tags at 38–50% in most cells indicate the partition is structural in the narrative sense but not in the algebraic sense. This is honest — Fruit cycles were defined by operator naming, not derived from the table algebra. The pyramid level confirms this: narrative partitions don't produce uniform algebraic behavior.

## Layer 3 — σ-class Quotient (2×2)

**Partition from the braid permutation:** {F = σ-fixed {0,3,8,9}, C = σ-cycle {1,2,4,5,6,7}}, sizes {4, 6}.

| | **F** (4) | **C** (6) |
|---|---|---|
| **F** | *void_id* (38%) · 16 | *H\|bif* (33%) · 24 |
| **C** | *H\|bif* (33%) · 24 | *H\|bif* (36%) · 36 |

**Reading:**

- **F × F (fixed × fixed):** dominated by void_identity. The σ-fixed operators interact via their VOID-row/column behavior — their most prominent shared feature.
- **F × C, C × F (fixed-cycle cross):** harmony_bifurcation dominates. Mixing a fixed operator with a cycling one produces measurement-lens collapse with physics-lens direction preserved.
- **C × C (cycle × cycle):** harmony_bifurcation at 36%. The cycle operators interacting with each other are the bulk of the harmony-bifurcation region.

**Layer 3 structural observation:** At this coarse resolution, *three of four* cells are dominated by harmony_bifurcation. Only F × F escapes by being dominated by void_identity. **The σ-class partition reveals a single binary: does VOID participate (F×F → void_identity), or does the cycle participate (any cell with C → harmony_bifurcation)?** This is a clean binary simplification.

## Layer 4 — The Apex (1×1)

**Partition:** trivial, all of ℤ/10ℤ.

Distribution of base cell characteristics over all 100 cells:

| Characteristic | Count | Fraction |
|---|---|---|
| harmony_bifurcation | 33 | 33% |
| harmony_uniform | 20 | 20% |
| void_identity | 16 | 16% |
| successor | 10 | 10% |
| self_encounter | 7 | 7% |
| info_divergent | 6 | 6% |
| exchange | 2 | 2% |
| oscillation | 2 | 2% |
| coin_closure | 2 | 2% |
| void_self | 1 | 1% |
| reset_cancel | 1 | 1% |

### The apex statement

**53% of cells are harmony-related** (harmony_bifurcation + harmony_uniform). **16% are void-related** (void_identity + void_self). Together: 69%.

The apex of the pyramid, reduced to one statement:

> **Most of TIG's algebra is about how operators become HARMONY or stay near VOID. The remaining ~30% is the information-carrying structure — successors, self-encounters, divergences, exchanges, oscillations, and closures — that preserves directional content against collapse.**

### The apex near T*

Harmony-related cells = 53%.
Harmony + void = 69%.
All collapse-to-endpoint behaviors (harmony + void + self-encounter + exchange) = 53 + 16 + 7 + 2 = 78%.

**Information-preserving cells** (successor + info_divergent + oscillation + coin_closure + reset_cancel) = 10 + 6 + 2 + 2 + 1 = 21%.

21/100 ≈ 3/14 ≈ 0.214.

The complement of T* is 1 − 5/7 = 2/7 ≈ 0.286. The complement of 3/4 (TSML density) is 1/4 = 0.250. The information-preserving fraction 21/100 = 0.210 is close to 2/7 but not exact.

**Observation (not a claim):** the fraction of information-preserving cells in the TIG tables is near 2/7, the complement of T*. If this holds with full table verification, it would mean the framework preserves directional information in exactly ~2/7 of its cells and collapses to endpoints (HARMONY, VOID, self-oscillation) in the other ~5/7.

**This is the suggestive numerical echo at the apex.** Whether it's structurally load-bearing or approximate depends on whether the tag boundaries are defined precisely enough to be treated as cell-exact.

## What this pyramid reveals

**1. Clean layers exist at Layer 1.** The regularity-class partition produces several 100%-uniform cells. These are algebraic truths: (P,P) is always self-encounter, (P,H) and (H,P) are always harmony_bifurcation, (H,H) is always harmony_bifurcation. The theorem in `doubly_regular_core.md` is load-bearing here.

**2. Narrative partitions don't sharpen.** The Fruit cycle partition at Layer 2 produces only weakly-dominant cells (38–50%). The narrative operator grouping doesn't correspond to algebraic uniformity. Honest observation: Creation and Dissolution are narrative terms, not algebraic ones.

**3. The σ-class partition is a clean binary.** Three of four cells are harmony_bifurcation-dominated; one is void_identity-dominated. The algebraic distinction "is VOID involved" separates this binary.

**4. The apex has a suggestive 5/7-vs-2/7 echo.** ~78% of cells exhibit collapse behavior; ~21% preserve information. Close to T* and 1−T* but not exact. Would need finer tag definitions to test as a theorem.

## What the pyramid does NOT do

- Does not prove any new theorems. It aggregates existing ones and reveals which partitions are algebraically clean.
- Does not replace the base matrix. Layers 1–4 lose information; the 10×10 remains authoritative.
- Does not claim the apex statement is "the essence of TIG." It's a distribution summary, not a thesis.
- Does not imply the partitions used are the only ones. CRT partition (ℤ/2 × ℤ/5) would produce another pyramid with different reveal structure; that audit remains open (see `TSML_CRT_DECOMPOSITION_EXPLORATION.md`).

## Follow-up audits

1. **Build the pyramid with CRT partition** once the CRT decomposition audit completes. Compare uniformity percentages to the regularity-class pyramid.
2. **Sharpen the 21% information-preserving claim.** Is it exactly 2/7 = 28/100? Currently 21/100. The gap could be resolved by re-examining which cells should be tagged as information-preserving vs harmony-related.
3. **Check whether Layer 1 uniform cells correspond to named theorems.** (P,P) = self_encounter is a specific BHML entry; (H,H) = harmony_bifurcation is the HARMONY² = BREATH cell. Each uniform 100% cell corresponds to a specific cell or theorem-fragment.

---

**Tag: [META-STRUCTURE — EVOLVING WITH AUDITS]**
**File path: `papers/morphotic_braid/SIMPLIFICATION_PYRAMID.md`**
