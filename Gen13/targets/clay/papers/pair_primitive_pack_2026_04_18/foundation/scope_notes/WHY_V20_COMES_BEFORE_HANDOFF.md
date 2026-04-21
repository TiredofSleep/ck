# Why PPM-v2.0 Comes Before Handoff
## Sprint Ordering Rationale

---

## The Program's State After v1.1

Two checkpoints of the pair-primitive framework have landed on Z/10:

- **PPM-v1.0 PASS** under multiplicative operationalization: Map B (MAX = persistent, ADD = excluded) produces a coherent structural fit at +4/−4, cleanness gap 8.
- **PPM-v1.1 FAIL** under additive operationalization: neither map reaches +3; Map B retains +2 lead from topology-neutral sources but operation-specific sources lose discriminating power.

The FAIL is diagnostic rather than refutational — it attributes the non-discrimination to the seam's multiplicative loading, not to framework failure. Together the two results say: *the pair-primitive framework's rubric-level discrimination on Z/10's seam is multiplicatively anchored.*

What those two findings cannot say, and what a handoff package cannot honestly claim without this next sprint, is whether the v1.0 mapping transports beyond Z/10.

---

## What Handoff Without v2.0 Would Claim vs. What It Should Claim

If the archive were handed off now, the narrowest honest framing of the pair-primitive framework's status would be:

> Two checkpoints run on Z/10. One PASS under multiplicative reading with Map B; one FAIL under additive reading. The framework is multiplicatively anchored on Z/10's seam. Untested on other rings.

"Untested on other rings" is the load-bearing phrase. It means any reader of the handoff has to treat the Map B finding as a single-ring observation. The framework's next checkpoint — "does Map B hold across the tested Path 2 family?" — is structurally the most natural question to ask of the handoff, and its absence will be visible.

Running v2.0 before handoff shifts the framing to something specific:

> Map B either holds across the 8 Path 2 carriers (with pre-registered cleanness), or it does not (with specific attribution). Either way, the handoff contains the result.

This is the same discipline that made the B2 pack's 11 sprints each narrow but informative: the findings earn specific sentences, and the archive presents those sentences rather than open questions that a reader would ask next.

---

## Why v2.0 Specifically, and Not Another Successor

The successors authorized after v1.1 were:

- **PPM-v1.1.1** (refined additive rubric): the user has declined this. The pilot analysis in v1.1's verdict already showed that even with relaxed Source 1 criterion, the aggregate would reach at most +1 — still FAIL. Running it would confirm the analytical prediction, not discover new structure.
- **PPM-v2.0-multiplicative** (extension to Path 2 carriers): tests transport of the v1.0 finding across the carrier family. Highest information yield among successors because the answer is not pilot-predictable in the way v1.1.1's is.
- **PPM-v3.0** (different Z/10 checkpoint): would produce a second independent point of contact on Z/10 but without extending beyond the ring. Lower information per sprint slot than v2.0.
- **Scale-example sprints**: remain explicitly unauthorized regardless of other results.

v2.0 is the highest-yield next move because:

1. **It is the only successor whose outcome is not pilot-predictable.** v1.1.1's outcome is already analytically knowable. v3.0's outcome is predictable in broad terms (MAX dominates topology-neutral features on any ring). v2.0 has genuine uncertainty: the P3AP extension on Path 2 carriers produces chain topology different from Z/10's hub topology, and whether Map B's structural signature survives that topology shift is an open question.

2. **It reuses existing data and infrastructure.** The 8 Path 2 carriers from P3AP are on record with validated recovered seams. No new extraction is needed. The rubric from PPM-v1.0 translates directly under multiplicative operationalization — only the data sources per carrier change.

3. **It operates at Path 3 (bridge test), which is where the framework's bridge claims would be tested.** A Path 1 finding that does not transport to Path 2 carriers under bridge discipline would remain a Z/10-specific observation. A Path 1 finding that does transport earns the stronger sentence "the framework's multiplicative-operationalization Map B holds across the tested compatibility family."

---

## Why "Before Handoff" Specifically

The user's prior instructions on handoff packaging (B2 pack, scope note, rules document) emphasized that a handoff should contain closeout-quality sentences, not open questions. The B2 pack's 11 sprints each had frozen verdicts with attributed causes. The pair-primitive framework's two checkpoints are also on record with verdicts.

But the framework's testable structural claim — "the multiplicative-operationalization mapping on Z/10 transports" — is currently unrun. A handoff that includes v1.0 and v1.1 without v2.0 leaves the most obvious next question explicitly open.

The precedent in the B2 pack was: *run the narrow checkpoint, then hand off.* Path 3 sprints (P3-BridgeA-Prime, v1.1, v1.2-adj) each ran specific bridge tests before the pack closed. The pair-primitive checkpoints should follow the same pattern: run the bridge test, then hand off.

This is not about forcing a finding. It is about ensuring the handoff is complete at the level of questions that can be answered with existing data.

---

## What v2.0 Will Test

The sprint applies the v1.0 rubric's multiplicative operationalization to each of the 8 Path 2 carriers. Specifically:

- Source 1 (structural backbone): does MAX form the multiplicative backbone on each carrier's recovered seam under P3AP?
- Source 2 (identity-edge): does ADD attach vertex 1 (multiplicative identity) on each carrier?
- Source 3 (leaf-edge): does ADD sit at the graph boundary on each carrier?
- Source 4 (topology-family): does MAX carry the majority of topology features on each carrier?

The per-carrier rubric would produce per-carrier scores. An aggregate across the 8 carriers would then test whether Map B fits at threshold on the family level, parallel to how P3-Subtype-v1.1 and v1.2-adj aggregated their findings across the same 8 carriers.

The specific rubric design, null model (if any), and thresholds belong to the pre-reg, not to this ordering note.

---

## Three Outcomes, Each Informative

**Transport PASS.** Map B holds across the Path 2 family at pre-registered cleanness. The framework's multiplicative-operationalization mapping is not Z/10-specific; it transports under the P3AP extension to the tested carriers. This would be the strongest handoff sentence the framework can currently earn.

**Transport FAIL.** Map B does not hold at family-level cleanness. The v1.0 PASS becomes Z/10-specific; the framework's mapping does not transport under P3AP. The handoff documents this clearly, and the program's next question becomes whether a different extension algorithm (hub-extension, deferred) or a different operational interpretation would transport.

**Transport UNCLEAR.** Map B partially transports (e.g., scores above threshold on some carriers, below on others). The handoff identifies the specific carrier-level variation, which is itself diagnostic.

Each outcome produces a specific narrow sentence. None of them authorizes broader claims than its exact content. The scope-note companion specifies what each outcome earns the program.

---

## What v2.0 Does Not Do

- Does not test additive operationalization on Path 2 carriers (separate sprint).
- Does not test rings outside the P3AP carrier set.
- Does not test hub-extension (still deferred).
- Does not re-score v1.0 or v1.1.
- Does not re-score any prior Path 3 sprint.
- Does not license scale examples, physics, ontology, or cross-framework synthesis regardless of outcome.
- Does not introduce new generators or new object classes.

The rubric-level structure is inherited from v1.0. The object class (P3AP recovered seams) is inherited from prior Path 3 sprints. The scope is narrow by design: one operationalization, one carrier set, four sources per carrier, aggregated across 8 carriers.

---

## Summary

Running v2.0-multiplicative before handoff:

- Closes the most structurally obvious next question about the pair-primitive framework.
- Uses only existing data and infrastructure.
- Returns a narrow sentence regardless of verdict (PASS, FAIL, or UNCLEAR).
- Preserves the program's discipline: test what can be tested before packaging.
- Makes the handoff cleaner because "untested on other rings" becomes either "tested and transports" or "tested and does not transport at family level."

The sprint is narrow and cheap, and its outcome is not pilot-predictable the way v1.1.1's is. That makes it the right next move before any handoff action.
