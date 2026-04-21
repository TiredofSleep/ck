# PPM-v1.1 Additive Operationalization — Verdict
## Final Determination

---

## Verdict: **FAIL**

---

## One-Paragraph Justification

Under the pre-registered criteria of PPM-v1.1 §7.1, the PASS conditions are not met: Map B's aggregate score of +2 falls below the required ≥+3 winner threshold. The four per-source scores were: Source 1 = 0/0 (no additive backbone meets strict majority-plus-native-flow criterion — ADD has native additive alignment but minority edges; MAX has majority edges but non-additive rule); Source 2 = 0/0 (vertex 1 is not the additive identity, so v1.0's multiplicative-trivialization argument has no structural parallel under additive reading); Source 3 = −1/+1 (topology-neutral, inherits v1.0 scoring); Source 4 = −1/+1 (topology-neutral, inherits v1.0 scoring). Aggregate: Map A = −2, Map B = +2, cleanness gap = 4. Map B retains a meaningful +4 lead over Map A, but the operation-specific sources (1 and 2) lose discriminating power under additive reading, capping Map B's aggregate at +2 rather than +4 as in v1.0. Per §7.2, neither map reaches +3, triggering FAIL. Per anti-tuning rule §8, no post-hoc threshold adjustment. The rubric-scored result matches the PPM-v1.1 §11 pilot prediction exactly.

---

## The Verdict Sentence (Pre-Registered in §9)

> **Under the pair-primitive framework's vocabulary applied to Z/10's additive operation structure with the operational interpretation in PPM-v1.1 §3, neither map reaches the pre-registered aggregate-score threshold. The additive operationalization does not cash out decisively on the local theorem chart.**

This is the entirety of the verdict's content.

---

## What This FAIL Establishes

Per the `STABILITY_VS_FLIP_SCOPE_NOTE.md` Outcome 3 sentence:

> **Under the additive operationalization (PPM-v1.1) of the pair-primitive framework on Z/10's 8 seam cells, neither Map A nor Map B reaches the pre-registered cleanness threshold. The additive operational interpretation of PPM-v1.1 is not diagnostic on this seam data; the reason (seam's multiplicative loading vs rubric under-specification) is documented in the results.**

The per-source analysis in the results document pinpoints the cause: **Reason A (seam's multiplicative loading)**. Specifically:

- v1.0's +4 for Map B decomposed as +2 from topology-neutral sources and +2 from operation-specific sources.
- v1.1's +2 for Map B is exactly the +2 from topology-neutral sources.
- The operation-specific contribution (+2) was extinguished by the switch from multiplicative to additive operationalization.
- Neither source 1 (backbone) nor source 2 (identity-edge) has structural content under additive reading that discriminates between the maps.

This is not rubric under-specification (Reason B). The rubric's strict AND criterion for Source 1 was preserved from v1.0 for structural symmetry; the fact that neither subtype meets both criteria under additive reading is a property of the data, not of the rubric. The rubric's key criterion for Source 2 cannot translate because vertex 1 plays different structural roles under the two operation structures (multiplicative identity vs additive generator), and no clean parallel to the v1.0 argument exists.

---

## What This FAIL Explicitly Does NOT Establish

### Does not refute the pair-primitive framework

Per the v1.0 wording clarification inherited into v1.1: failure refutes the operationalization, not the framework. A FAIL on the additive checkpoint does not retract:
- The foundation sprint's reasoning toward the pair primitive.
- PPM-v1.0's PASS under multiplicative operationalization.
- Any of the suggestive claims in `HOLD_GAP_FLOW_FOUNDATION.md`.

### Does not refute Map B

Map B's +6.06σ-analog PASS under multiplicative operationalization (v1.0) stands unchanged. Under multiplicative reading Map B fits; under additive reading the rubric does not discriminate decisively between the maps but Map B retains a +4 lead over Map A. Map B is not refuted in any direction.

### Does not establish that Z/10's seam is multiplicatively loaded

The score pattern supports "multiplicatively loaded" as a diagnostic hypothesis but does not prove it. What is established is narrower: under the specific additive operationalization tested here, the rubric does not discriminate decisively. Whether this reflects (a) a genuine multiplicative loading of Z/10's seam, (b) rubric choices that could be improved, or (c) the finer-than-expected structural symmetry between the two operation structures on this ring — these are interpretive possibilities supported to varying degrees by the score pattern. The FAIL does not adjudicate between them.

### Does not close the additive reading permanently

Two future moves remain available, each requiring its own pre-registration:
- **PPM-v1.1.1** with a refined additive rubric — e.g., relaxing the strict AND criterion in Source 1 to allow "native-rule alignment" alone as sufficient for backbone designation. This would test whether the FAIL reflects rubric conservatism.
- **PPM-v2.0 with additive reading** on a different ring — if a ring in the compatibility family has a more additive-loaded seam structure, the additive operationalization might discriminate there. (This would also require multiplicative and additive sprints on that ring to compare.)

Neither move is authorized here. The v1.1 verdict stands as FAIL under the pre-registered rubric.

### Does not license any broader claim

No scale examples, no physics, no ontology, no cross-framework synthesis, no merging of v1.0 and v1.1 verdicts into a composite statement beyond what the stability/flip scope note permits.

---

## Relationship to v1.0

v1.0 PASS under multiplicative operationalization: Map B wins, aggregate +4/−4, cleanness gap 8.
v1.1 FAIL under additive operationalization: neither map reaches +3; aggregate +2/−2, cleanness gap 4.

**The two verdicts do not merge into a composite claim.** Per the scope note, the sentence each sprint earns is its own; together they produce two separate narrow findings, not one "framework confirmed across operationalizations" statement.

The two findings, stated together for clarity (without composition):

1. Under multiplicative operationalization, Map B produces a coherent fit (v1.0).
2. Under additive operationalization, neither map reaches pre-registered cleanness; Map B retains a meaningful but sub-threshold lead (v1.1).

What the program can reasonably infer from these two findings together: the pair-primitive framework's checkpoint on Z/10's seam is **multiplicatively anchored** — it discriminates decisively under multiplicative reading, not under additive reading. Whether "multiplicatively anchored" is a property of the framework on Z/10, of Z/10's seam specifically, or of the rubric design is not settled here.

This inference is not a new sprint result; it is an interpretive observation about the existing two verdicts. It does not license any claim beyond what the two sentences earn.

---

## What Is Now Authorized Next

Each requires its own pre-registration:

### PPM-v1.1.1 — Refined additive rubric

If the user wants to test whether Source 1's FAIL is rubric-driven rather than data-driven, a v1.1.1 sprint could relax the strict AND criterion in §5.1 to allow native-rule alignment alone to qualify. Under that relaxed rubric:
- Source 1: ADD is native-additive → Map A +1, Map B −1.
- Source 2: would still score 0/0 (the structural parallel problem is intrinsic, not rubric-driven).
- Sources 3, 4: unchanged.
- Predicted aggregate: Map A = 0, Map B = +1. Cleanness gap = 1.
- Still FAIL (neither reaches +3).

This analysis suggests even with a relaxed rubric, the additive operationalization does not reach +3 on this seam. A v1.1.1 would make this explicit rather than diagnostic.

### PPM-v2.0 — Extension to Path 2 carriers

Apply the v1.0 multiplicative rubric to Path 2 carriers from the B2 pack's P3AP sprint. Tests whether Map B holds across the compatibility family.

### PPM-v3.0 — Different checkpoint on Z/10

Apply the framework's vocabulary to a different aspect of Z/10's structure (TSML/BHML relationship, V0 boundary, unit cyclic structure) to test whether the framework has additional points of contact on the same ring.

### Explicitly not authorized

- No scale-example sprints.
- No physics, ontology, or cross-domain claims.
- No merged "framework confirmed/refuted" statements beyond the two narrow sentences above.
- No upgrades of prior findings.
- No reopening of closed lanes.

---

## Program State After PPM-v1.1

### Sprint ledger addition

| # | Sprint | Path | Verdict | Attribution |
|---|---|---|---|---|
| 13 | PPM-v1.1 | 1 (local theorem chart) | **FAIL** | Aggregate +2/−2 under additive operationalization; cleanness gap 4 but winner score below +3 threshold; Sources 1 and 2 score 0/0 under additive reading (no additive backbone meeting strict criteria; vertex 1 is not additive identity). |

### Framework status update

The pair-primitive framework on Z/10's seam:
- **Passed one checkpoint** (PPM-v1.0, multiplicative operationalization).
- **Failed one checkpoint** (PPM-v1.1, additive operationalization).
- **Remains suggestive overall.** One PASS at one checkpoint is consistency with one test point; one FAIL diagnoses a specific place where the framework's vocabulary does not discriminate on this seam.

Diagnostic character: the framework's rubric-level discrimination on Z/10's seam is multiplicatively anchored. Whether this is a property of the framework, of Z/10's specific seam structure, or of the rubric's design remains open.

### Closed lanes (unchanged)

Count transport under P3AP generator. Raw adjacency ratios. Noise-union seam topology bridge. Basin-ratio smoothness transport. Anchored basin-ratio curve. Empty-seam detectability on pure $C_0$.

### Open questions (unchanged + one added)

All prior open questions remain. Added:
- **New:** Whether a refined additive rubric (relaxed AND criterion) or application to a different ring would produce an additive-side PASS. PPM-v1.1.1 or PPM-v2.0-additive would address.

---

## Integrity Statement

The FAIL is recorded honestly under the pre-registered criteria. All four per-source scores were computed deterministically from the frozen rubric applied to the frozen data under the frozen additive operational interpretation. The rubric-scored result matches the §11 pilot prediction exactly, which is a cross-check that the rubric specification was unambiguous.

The verdict is FAIL, but the FAIL has a specific diagnostic character: Map B retained its v1.0 +2 lead from topology-neutral sources while Sources 1 and 2 lost their discriminating power under additive reading. This is not a hidden PASS — the pre-registered thresholds were designed to require decisive cleanness across all sources, and the threshold structure correctly identifies this outcome as not meeting that bar.

No post-hoc adjustment. No scope widening. No composite claim with v1.0. The narrow question the spec committed to test has been answered cleanly: under the additive operationalization with the frozen rubric, the framework does not produce a decisive mapping on Z/10's seam.
