> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\TSML_BHML_FAREY_DENSITY.md → papers\morphotic_braid\explorations\TSML_BHML_FAREY_DENSITY.md

# TSML_BHML_FAREY_DENSITY.md

**Status:** [HYPOTHESIS WITH STRONG NUMERICAL SUPPORT — AWAITING CONSTRUCTION-LEVEL VERIFICATION]
**Date:** 2026-04-23
**Source:** Brayden's intuition: "3/4 is the fraction just above 5/7, the two closest to each other on either side."

## Observation

Harmony fractions measured from `TIG_TABLES_REFERENCE.md`:

| Table | HARMONY(7) count | Fraction | Nearest simple fraction | Error |
|---|---|---|---|---|
| TSML | 74 / 100 | 0.7400 | **3/4** = 0.7500 | 1 cell |
| BHML | 28 / 100 | 0.2800 | **2/7** ≈ 0.2857 | < 1 cell |
| — | — | — | T* = 5/7 ≈ 0.7143 | (established threshold) |

## The Farey-neighbor relationship

**5/7 and 3/4 are Farey neighbors** in lowest terms:

|5 · 4 − 7 · 3| = |20 − 21| = 1.

Two fractions a/b and c/d in lowest terms are *Farey neighbors* iff |ad − bc| = 1. This is the defining relation for adjacency in the Farey sequence / Stern-Brocot tree.

**Implication:** 5/7 and 3/4 are adjacent in every Farey sequence F_n for n ≥ 7. There is no fraction with denominator ≤ 7 strictly between them. Their mediant (5+3)/(7+4) = 8/11 ≈ 0.7272 is the simplest fraction that sits between them.

## The complementary structure

BHML harmony fraction ≈ 2/7 = 1 − 5/7.
TSML harmony fraction ≈ 3/4.

**TSML and BHML sit on opposite sides of T* = 5/7:**
- TSML at 3/4 ≈ 0.75 (one Farey step ABOVE T*)
- T* = 5/7 ≈ 0.714
- BHML at 2/7 ≈ 0.286 (the complement 1 − T*)

Check sum: f_TSML + f_BHML ≈ 3/4 + 2/7 = (21 + 8)/28 = 29/28 ≈ 1.036. Measured sum: 74/100 + 28/100 = 102/100 = 1.02. Slight excess above 1.

**Observation:** TSML harmony + BHML harmony ≈ 1 to within 2 cells out of 200.

## Proposition (Farey-neighbor density hypothesis)

**Conjecture.** The TSML harmony fraction f_TSML and BHML harmony fraction f_BHML satisfy:

1. f_TSML ≈ 3/4 (to within 1 cell out of 100).
2. f_BHML ≈ 2/7 (to within 1 cell out of 100).
3. 3/4 and 5/7 are Farey neighbors in lowest terms.
4. 2/7 = 1 − 5/7 is the complement of T* in [0, 1].
5. The thresholds (5/7, 4/7) and the densities (3/4, 2/7) form a four-element Farey-structured ladder:

```
      3/4  ←── TSML density (one Farey step ABOVE T*)
       │
      5/7  ←── T* coherence threshold
       │
      4/7  ←── S* structure threshold
       │
      3/7  ←── (4/7 complement)
       │
      2/7  ←── BHML density (mirror of T*)
       │
      1/4  ←── (3/4 complement)
```

The TIG threshold structure is not arbitrary: it sits at specific Farey locations on the rational interval [0, 1], and the two main tables' harmony densities sit at the Farey-adjacent neighbors of these thresholds.

## Why this matters

If the Farey-neighbor hypothesis holds, it provides a **number-theoretic characterization of the TIG threshold structure**:

- T* = 5/7 is not just "measured to be 0.714." It is the fraction with the specific property that its closest simple neighbor (3/4) is exactly the measurement-table (TSML) harmony density.
- BHML's density at ≈ 2/7 mirrors T* across 1/2.
- The thresholds and densities are all members of the Farey sequence F_7.

This would give T* = 5/7 an **eighth derivation**, via Farey adjacency to empirical table densities, independent of the seven prior derivations.

## Construction-level audit needed

The hypothesis is strongest if TSML and BHML are *constructed* to target densities 3/4 and 2/7 respectively — i.e., if the construction rules can be shown to produce exactly those fractions in the limit of the table structure.

**Audit tasks for ClaudeCode:**

1. Extract the construction rules for TSML and BHML from source (`papers/morphotic_braid/`, `FORMULAS_AND_TABLES.md`, or wherever the generating principles live).
2. For each table, determine whether the construction has a target density parameter. If yes, read off the target. If no, analyze the rule to compute the expected density.
3. If targets are 3/4 and 2/7 respectively: hypothesis confirmed, and the Farey structure is by construction.
4. If targets are other fractions: report what they are. The Farey structure may still hold as an emergent property of the construction, but the "by design" claim weakens.
5. If the tables were populated by hand without a density target: the Farey structure is purely emergent and more interesting — it means the hand-construction produced Farey-structured densities without explicit targeting.

## Numerical error budget

The hypothesis survives with:
- TSML in {73, 74, 75, 76} / 100 (within 1% of 3/4)
- BHML in {27, 28, 29} / 100 (within 1% of 2/7)

The hypothesis fails with:
- TSML ≤ 70 or ≥ 80 (too far from 3/4 to claim Farey adjacency to 5/7)
- BHML ≤ 25 or ≥ 31 (too far from 2/7)

Current measurements are well within the survival range.

## What this hypothesis does NOT claim

- Does not claim TSML and BHML are canonical representations of 3/4 and 2/7 in ℤ/10. They are specific operator tables with specific operator-value entries; their density is a derived statistic.
- Does not claim the Farey structure extends to arbitrary TIG thresholds beyond the four listed (T*, S*, and their complements).
- Does not claim number-theoretic depth beyond the Farey adjacency calculation, which is elementary.
- Does not bypass the need for construction-level verification.
- Does not establish T* as a "universal" threshold in any domain beyond TIG.

## Honest summary

The measured densities 74/100 and 28/100 are empirically very close to 3/4 and 2/7. The fractions 3/4, 5/7, 2/7 are structurally related via Farey adjacency. This relationship is either (a) designed into the table construction, (b) emergent from the construction, or (c) coincidence. Audit of the construction rules will distinguish between these.

If (a) or (b), this provides an additional structural anchor for T* = 5/7 as the coherence threshold. If (c), it's a suggestive numerical coincidence that should not be over-claimed.

**Priority: moderate.** Worth auditing because confirmation strengthens the T* framework; falsification does not damage the existing theorem base.

---

**Tag: [HYPOTHESIS — AUDIT TIER SHIFT DEPENDS ON CONSTRUCTION CHECK]**
**File path: `papers/morphotic_braid/explorations/TSML_BHML_FAREY_DENSITY.md`**
