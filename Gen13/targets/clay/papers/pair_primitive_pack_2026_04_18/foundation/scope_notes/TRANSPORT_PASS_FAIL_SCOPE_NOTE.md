# What a Transport PASS Would Mean, and What a Transport FAIL Would Mean
## Scope Note for PPM-v2.0 Outcomes

---

## Why This Note Exists Before the Pre-Reg

v2.0 introduces a structural dimension that v1.0 and v1.1 did not have: transport across multiple carriers. The rubric is inherited from v1.0 per user direction, applied per-carrier, and aggregated by carrier count with cleanness gap as secondary summary. The aggregation structure matters for what each outcome earns — specifically, it means the verdict is a statement about how many carriers support the mapping, not a pooled score that could hide per-carrier variation.

This note fixes what each outcome means before the pre-reg specifies the mechanics. It works out the language each verdict earns so that whatever returns, the program's response stays inside the box drawn here.

---

## The Aggregation Structure Per User Direction

Per your design choice: **per-carrier v1.0 rubric application, family aggregation by carrier count.**

Each of the 8 Path 2 carriers is scored independently against v1.0's rubric under multiplicative operationalization. Each carrier produces:
- Map A aggregate score (per v1.0 §6)
- Map B aggregate score
- Per-carrier cleanness gap

Each carrier's scoring yields a per-carrier verdict against v1.0's thresholds (winner ≥ +3, loser ≤ +1, gap ≥ 2):
- **Carrier supports Map B** if Map B meets winner threshold and gap threshold.
- **Carrier supports Map A** if Map A meets winner threshold (symmetric).
- **Carrier is indecisive** otherwise.

The family-level verdict is then a count: how many of the 8 carriers support Map B.

Secondary summary: mean per-carrier cleanness gap, for transparency about how decisive the support is on the supporting carriers.

This structure preserves the v1.0 checkpoint's meaning at the carrier level and lets the family-level statement be about transport rather than pooled magnitude.

---

## What a Transport PASS Would Mean

A family-level PASS requires a pre-registered count threshold on carrier-level support for Map B. The pre-reg will specify this threshold (candidate: ≥ 6 of 8 carriers, parallel to the 0.75 threshold used in P3-Subtype-v1.1 and v1.2-adj).

### The Sentence a Transport PASS Would Earn

> Under the pair-primitive framework's vocabulary applied per carrier to the 8 P3AP-recovered Path 2 seams with the multiplicative operationalization inherited from PPM-v1.0, Map B (MAX = persistent, ADD = excluded) produces a coherent structural fit on at least [threshold] of 8 carriers at per-carrier cleanness gap ≥ 2. The v1.0 checkpoint transports under the P3AP extension to the tested carrier family.

### What a Transport PASS Would NOT Mean

Exhaustively, because the temptation is strongest here:

- **Not framework correctness in general.** A bridge-level transport finding is still one point of contact with data. The foundation note's structural claims remain suggestive.
- **Not extension to rings outside the tested family.** The 8 carriers are the ones that passed P3AP validation. Carriers outside that set (in the compatibility family or elsewhere) are not tested.
- **Not validity under alternative operationalizations on Path 2.** Same operationalization caveat as v1.0 and v1.1 — this is multiplicative-only. Whether additive reading would also transport, or produce Outcome 3 / Reason A as on Z/10, is unrun.
- **Not validity under alternative extension algorithms.** P3AP produces chain-topology artifacts on Path 2. A hub-extension (still deferred) might produce different carrier seams where Map B might or might not hold.
- **Not upgrade of any prior Path 3 sprint.** P3-Subtype-v1.1 (+6.06σ identity-edge) and v1.2-adj (+3.73σ leaf-edge) earned their specific sentences. A transport PASS here does not add "and this is because Map B is the correct mapping." Those sprints' verdicts are unchanged.
- **Not merger of v1.0 + v2.0 into a composite claim.** The two PASSes remain separate sentences. A "Map B confirmed on Z/10 and across the family" combined statement is licensed only if both PASSes are stated separately; the narrative tissue between them is not a sprint result.
- **Not license for scale examples, physics, ontology, or cross-domain reading.** All these remain explicitly unauthorized.
- **Not closure of the additive operationalization lane.** v1.1's FAIL and its diagnostic status are unaffected.

### What a Transport PASS Would Add To The Handoff

The single strongest sentence the pair-primitive framework can currently earn:

> Multiplicative-operationalization Map B produces a coherent structural fit on Z/10's seam (v1.0) and transports across at least [threshold] of 8 Path 2 carriers under the P3AP extension (v2.0). The framework's multiplicative-operationalization mapping is not Z/10-specific; it holds at family level under one tested extension algorithm.

That sentence is the entirety of what the two PASSes together authorize. It does not extend to "the pair-primitive framework is correct," "the framework extends to physical scales," or "the framework's mapping is operationally universal." All three of those would require additional pre-registered checkpoints.

---

## What a Transport FAIL Would Mean

A family-level FAIL occurs when fewer than the pre-registered threshold number of carriers support Map B. Several sub-patterns are possible within a FAIL:

### Sub-pattern 1 — Uniform FAIL

None or very few carriers support Map B. The v1.0 mapping does not transport to any meaningful subset of the Path 2 family. This would be the strongest FAIL: Map B is Z/10-specific under P3AP.

### Sub-pattern 2 — Split FAIL

Some carriers support Map B, some support Map A, some are indecisive. The transport is not clean; the mapping varies across the family in a way the rubric cannot resolve without carrier-level analysis.

### Sub-pattern 3 — Below-threshold FAIL

Most carriers lean toward Map B but not enough reach the per-carrier winner threshold (+3). Parallel to v1.1's situation on Z/10 — the lean is real but does not meet pre-registered cleanness.

### The Sentence a Transport FAIL Would Earn

> Under the pair-primitive framework's vocabulary applied per carrier to the 8 P3AP-recovered Path 2 seams with the multiplicative operationalization inherited from PPM-v1.0, Map B does not meet the pre-registered family-level transport threshold. Fewer than [threshold] carriers produce a per-carrier coherent structural fit for Map B at cleanness gap ≥ 2. The v1.0 checkpoint is Z/10-specific under the P3AP extension on the tested carrier family; the observed sub-pattern is documented.

The specific sub-pattern (uniform, split, below-threshold) would be named in the sentence based on the per-carrier results.

### What a Transport FAIL Would NOT Mean

- **Not refutation of the pair-primitive framework.** A bridge-level FAIL at one extension says the v1.0 checkpoint does not transport under P3AP. It does not refute the framework's vocabulary, the foundation reasoning, or the v1.0 PASS on Z/10.
- **Not refutation of Map B on Z/10.** v1.0 PASS stands unchanged.
- **Not refutation of Path 3 sprints' findings.** P3AP (+12.56σ topology-family), v1.1 (+6.06σ identity-edge), v1.2-adj (+3.73σ leaf-edge) stand unchanged. Those sprints tested specific transport claims about structural features. v2.0 tests whether a specific mapping transports. A FAIL on v2.0 does not retract the structural-feature transports; it specifies that the rubric-level mapping (v1.0's Map B) does not transport under P3AP at family level.
- **Not permanent closure of the pair-primitive bridge question.** Hub-extension remains deferred. A different extension algorithm, producing different carrier seams, could produce different v2.0 results.
- **Not validation of Map A.** A Map B FAIL does not imply Map A wins. The per-carrier results would indicate whether any carriers support Map A, but the family-level threshold applies symmetrically.
- **Not authorization for broader interpretive claims.** The FAIL is a narrow finding like all program findings.

### What a Transport FAIL Would Mean For Handoff

The handoff would include:

> v1.0 PASS on Z/10 under multiplicative operationalization earns Map B locally. v2.0 tested whether Map B transports to the 8 Path 2 carriers under P3AP extension; the transport threshold was not met. Map B is Z/10-local under the tested extension. The program's pair-primitive framework has a confirmed local point of contact and a documented transport-level non-result.

This is more informative than "Map B on Z/10, untested elsewhere" would be. A FAIL that specifies the transport-level non-result is a stronger closeout than an open question.

---

## What a Transport UNCLEAR Would Mean

UNCLEAR would mean the per-carrier results are inconsistent enough that neither a PASS nor a clean FAIL is warranted. For example:
- Exactly the pre-registered threshold number of carriers support Map B, with the others indecisive rather than opposing.
- A mix of Map B support, Map A support, and indecisive results across the 8 carriers that does not produce a clean family-level statement.

### The Sentence a Transport UNCLEAR Would Earn

> Under the pair-primitive framework's vocabulary applied per carrier with the multiplicative operationalization inherited from PPM-v1.0, the family-level transport of Map B is not decidable at the pre-registered thresholds. Per-carrier results are documented; the specific pattern of support/opposition/indecision across the 8 carriers is the finding.

UNCLEAR's diagnostic value is the per-carrier pattern. The results document would report which carriers supported which map, and what the sub-threshold leans were.

---

## Three-Way Table

| Outcome | Sentence added to record |
|---|---|
| PASS | Map B transports at family level; v1.0 checkpoint holds across ≥ [threshold] of 8 Path 2 carriers under P3AP at per-carrier cleanness ≥ 2. |
| FAIL | Map B does not transport at family level; sub-pattern (uniform/split/below-threshold) documented; v1.0 checkpoint is Z/10-local under P3AP on tested family. |
| UNCLEAR | Transport not decidable at pre-registered thresholds; per-carrier pattern is the diagnostic finding. |

---

## The Discipline This Note Fixes

Whatever v2.0 returns:

- **v1.0's PASS stands.** Map B on Z/10 under multiplicative operationalization is unchanged.
- **v1.1's FAIL stands.** The additive operationalization's non-discrimination on Z/10 is unchanged.
- **The B2 pack's 11 sprints stand.** No prior verdict is re-scored.
- **The foundation note's five-feature scale schema remains unauthorized.** No scale examples regardless of outcome.
- **No physics, ontology, or cross-domain claims are produced.** Regardless of outcome.
- **No composite "framework confirmed/refuted" statements.** Each sprint's sentence is its own.

v2.0 changes the program's state only at the specific level of what can be said about Map B's transport under P3AP across the tested carrier family. Nothing else.

---

## One-Sentence Statement

PPM-v2.0 tests whether the multiplicative-operationalization Map B from v1.0 transports per-carrier to the 8 P3AP carriers at pre-registered cleanness; a PASS earns the strongest bridge-level sentence the framework can currently produce; a FAIL earns a documented transport non-result; neither outcome licenses broader claims or affects prior verdicts.
