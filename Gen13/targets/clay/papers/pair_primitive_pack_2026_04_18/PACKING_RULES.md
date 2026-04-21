# Packing Rules — Pair-Primitive Framework Pack
## Extensions and Clarifications to B2 Packing Rules

---

## Inheritance

All 17 packing rules from the B2 pack's `PACKING_RULES.md` apply here verbatim. This document adds rules specific to the pair-primitive framework sprints (PPM-v1.0, v1.1, v2.0) and does not duplicate B2's rules.

---

## New Load-Bearing Rules For This Pack

### Rule 18 — Wording-clarification inheritance across PPM sprints

The PPM-v1.0 frozen wording clarification is:

> "This sprint evaluates the pair-primitive framework under a [specified] operationalization only; failure would refute this operationalization, not the pair-primitive framework in all possible readings."

This clarification is **inherited into every PPM sprint** (v1.1, v2.0, and any future PPM-v*). Every PASS or FAIL applies to the specific operationalization and extension tested, not to the framework in all possible readings. The clarification must be present in every PPM pre-registration and honored in every PPM verdict.

**Rationale:** PPM rubrics are deliberately scoped narrow so verdicts are interpretable. A PASS under one operationalization is not a proof; a FAIL under one operationalization is not a refutation. This rule prevents accidental inflation of verdicts across the PPM sprint series.

### Rule 19 — No composite claim merging v1.0 + v2.0

The v1.0 PASS (local multiplicative on Z/10) and the v2.0 PASS (family-level multiplicative transport across 8 P3AP carriers) are separate findings with separate frozen sentences. A composite statement such as "the pair-primitive framework's mapping is correct on Z/10 and extends to the compatibility family" is **not authorized** by the juxtaposition of the two PASSes.

Stating the two PASSes side-by-side without merging them is permitted and correct. Stating a single stronger claim whose strength exceeds the sum of the parts is not.

**Rationale:** bridge-level transport is not the same claim as local correctness, and two operationally validated checkpoints are still two checkpoints. A composite claim would need its own pre-registered test to earn its sentence.

### Rule 20 — Carrier-adapted reading is not a new rubric

PPM-v2.0 §3 introduces a "carrier-adapted reading" of Source 1 for Path 2 carriers (chain topology vs Z/10's hub topology). This is **the same multiplicative reading applied to valid chain-topology objects**, not a new rubric.

Any future sprint that alters the rubric's structural criteria rather than just adapting the object shape requires a new version designation (v2.1+ or v3.0+) and a new pre-registration.

**Rationale:** Preserves rubric continuity across the PPM sprint series and prevents silent rubric drift.

### Rule 21 — Diagnostic possibilities in predictions must be disclosed, not glossed

PPM-v2.0 §12 flagged two specific cases where the uniform prediction might break (Z/14 Source 1 boundary; Z/22 Source 4 sensitivity). Both resolved cleanly. This disclosure-and-resolution pattern is required for any PPM sprint whose prediction is uniform or near-uniform across a carrier family.

**Rationale:** Uniform predictions are suspicious because they look like back-door results. Pre-registering specific failure points and resolving them transparently converts uniformity from assumption into earned result.

### Rule 22 — Anti-upgrade rule for inherited Path 3 sprints

P3-BridgeA-Prime, v1.1 identity-edge, v1.2-adj leaf-edge findings are **inputs** to PPM sprints, not subjects of PPM scoring. PPM outcomes do not upgrade, downgrade, or modify the verdicts of those sprints. Those sprints' sigma values and attribution sentences remain as recorded in the B2 pack.

**Rationale:** Scope discipline. PPM tests a rubric-level mapping; the Path 3 sprints tested specific transport of structural features. The two classes of claims are compatible but independent.

### Rule 23 — FAIL sub-pattern preservation

When a PPM sprint FAILs, the sub-pattern (uniform / split / below-threshold per PPM-v2.0 §9.2, or Reason A / Reason B per `STABILITY_VS_FLIP_SCOPE_NOTE.md`) must be documented in the verdict. A bare FAIL without sub-pattern attribution is incomplete.

**Rationale:** FAIL sub-patterns carry different successor implications. A Below-threshold FAIL leaves room for refined rubric; a Uniform FAIL closes the lane. A Reason A FAIL identifies a structural loading; a Reason B FAIL identifies rubric under-specification. Downstream sprint selection depends on this distinction.

---

## Discipline For PPM-v2.1 and Beyond

When PPM-v2.1 is eventually run, it must:

1. Inherit Rule 18's wording clarification (with "additive" substituted for "multiplicative").
2. Apply per-carrier rubric and family aggregation following v2.0's template (Rule 19 applies — no merger of v2.0 + v2.1).
3. Preserve Rule 20's carrier-adaptation discipline.
4. Disclose predictions with named diagnostic possibilities (Rule 21).
5. Not upgrade the inherited Path 3 sprints (Rule 22).
6. Document FAIL sub-pattern if applicable (Rule 23).

See `open_questions/PPM_V21_ADDITIVE_TRANSPORT_FIRST_OPEN_CHECKPOINT.md` for the specific structure.

---

## Summary Statement

This pack extends B2's packing discipline without relaxing any of its rules. The new rules address patterns that arose specifically from the PPM sprint series: wording-clarification inheritance, anti-composition between local and family-level findings, carrier-adaptation without rubric drift, uniform-prediction disclosure, anti-upgrade of inputs, and FAIL sub-pattern preservation.

None of these rules is stricter than B2's; they are operational clarifications for a specific sprint family.
