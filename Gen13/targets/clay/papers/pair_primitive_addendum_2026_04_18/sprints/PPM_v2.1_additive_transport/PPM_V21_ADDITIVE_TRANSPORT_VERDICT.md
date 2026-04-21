# PPM-v2.1 Additive Transport — Verdict
## Final Determination

---

## Verdict: **FAIL (Uniform)**

---

## One-Paragraph Justification

Under the pre-registered criteria of PPM-v2.1 §9.2, the PASS thresholds are not met: $N_B = 0$ and $N_A = 0$, neither reaching the required ≥ 6 of 8 carriers. Per-carrier rubric scoring returned Map A = −2 and Map B = +2 on every carrier, with cleanness gap = 4 across all 8 carriers — but no carrier reached the per-carrier winner threshold of +3. Sources 1 and 2 scored 0/0 on every carrier (Source 1: no subtype meets strict AND of majority plus native-additive alignment; Source 2: vertex 1 is the additive generator not the additive identity, and substitute arguments are prohibited per §5.2). Sources 3 and 4 (topology-neutral) scored −1/+1 on every carrier, producing Map B's +2 lead uniformly. The sub-pattern classification per §9.2 is Uniform FAIL ($N_B = N_A = 0$). The §12 pilot prediction matched the rubric-scored result at the per-source, per-carrier, and family-verdict levels; one mismatch occurred at the sub-pattern label, where the §12 prose prediction said "Below-threshold FAIL" but the §9.2 strict definition triggers Uniform FAIL on the observed $N_B = N_A = 0$ configuration. The frozen pre-reg's definitions take precedence per anti-tuning rule §11. The prohibited substitutions (§16 item 8) were honored in scoring — no rubric relaxation, no substitute Source 2 argument. The verdict is FAIL with Uniform sub-pattern.

---

## The Verdict Sentence (Pre-Registered in §10)

> **Under the pair-primitive framework's additive operationalization applied per carrier to 8 P3AP Path 2 carriers, neither map reaches the pre-registered family-level transport threshold. Sub-pattern (Uniform FAIL: $N_B = N_A = 0$) is documented per §9.2. The additive operationalization does not cash out decisively at family level on the tested carriers.**

This is the entirety of the verdict's content.

---

## What This FAIL Establishes

Per the `TRANSPORT_PASS_FAIL_SCOPE_NOTE.md` Transport FAIL scope (inherited into v2.1 by discipline):

The additive operationalization of the pair-primitive framework does not discriminate decisively at family level on the 8 P3AP Path 2 carriers. Specifically:

- Sources 1 (structural backbone) and 2 (identity-edge) score 0/0 on every carrier under additive reading.
- Sources 3 (leaf-edge) and 4 (topology-family) score −1/+1 on every carrier, as in PPM-v2.0, but this topology-neutral lean is not sufficient to clear the per-carrier winner threshold of +3.
- Every carrier's aggregate is Map A = −2, Map B = +2, cleanness gap = 4 — substantial but sub-threshold.
- Family-level: $N_B = 0$, $N_A = 0$, $N_I = 8$. Uniform indecisive pattern across carriers.

Diagnostic attribution: **Reason A** (seam's multiplicative loading), transporting from Z/10 to the entire P3AP family. The TSML's multiplicative framing propagates through the P3AP extension to every Path 2 carrier, producing the same additive-reading non-discrimination that v1.1 observed on Z/10.

This transport of the additive-FAIL from Z/10 to the family is itself a finding: the multiplicative loading is a **carrier-family property under the P3AP extension**, not a Z/10-specific property.

---

## Completing the 2×2 Design Space

With PPM-v2.1 executed, the pair-primitive framework has now been tested under all four combinations of (local / transport) × (multiplicative / additive):

| | Multiplicative | Additive |
|---|---|---|
| **Local (Z/10)** | PPM-v1.0: PASS (Map B, +4/−4, gap 8) | PPM-v1.1: FAIL (aggregate +2/−2, gap 4, winner sub-threshold) |
| **Transport (8 P3AP carriers)** | PPM-v2.0: PASS uniform ($N_B = 8/8$, gap 8) | PPM-v2.1: FAIL Uniform ($N_B = N_A = 0$, gap 4) |

The 2×2 pattern is now specific:
- Multiplicative operationalization: PASS at both local and family-transport levels.
- Additive operationalization: FAIL at both local and family-transport levels, with matching diagnostic structure.

Per Rule 19, these four verdicts are not merged into a composite claim. Each stands as its own sentence.

---

## What This FAIL Explicitly Does NOT Establish

### Does not refute the pair-primitive framework

Per the inherited wording clarification (Rule 18): failure refutes the operationalization, not the framework. The framework's vocabulary and foundation reasoning remain unchanged.

### Does not refute Map B under multiplicative operationalization

PPM-v1.0 (local) and PPM-v2.0 (transport) stand unchanged. Map B fits Z/10's seam and transports across 8 P3AP carriers under multiplicative reading.

### Does not refute Map A

No carrier supported Map A, but no carrier supported Map B either. The additive rubric does not discriminate between the maps on these carriers — it does not establish that one map is wrong while the other is right.

### Does not prove seam is multiplicatively loaded at theorem level

The Reason A attribution is a diagnostic hypothesis consistent with the score pattern. Proving "Z/n's seam under P3AP is multiplicatively loaded" at theorem level would require a structural proof separate from this rubric-level result.

### Does not close the additive operationalization permanently

Two future moves remain available, each requiring separate pre-registration:
- **PPM-v2.1.1:** relaxed Source 1 AND criterion (e.g., "majority OR native-alignment"). Pilot analysis from v1.1's verdict §"What Is Now Authorized Next" suggests relaxation would give aggregate at most +1 — still FAIL. Running it would make this explicit rather than diagnostic.
- **PPM-v2.2:** additive test on rings outside P3AP's 8-carrier family (if such rings with additive-loaded seams exist).

Neither is authorized here. The v2.1 verdict stands as FAIL under the pre-registered rubric.

### Does not extend to other rings

The tested family is the 8 P3AP carriers. Rings outside this set are not tested.

### Does not validate or refute SAH

SAH (Shape-Admissibility Hypothesis) is at foundation register in the sidecar packet `shape_admissibility_foundation_2026_04_18/`. It is not operationalized and not tested by any PPM sprint. This FAIL neither supports nor refutes SAH.

### Does not merge with v2.0 into a composite claim

Per Rule 19 (explicitly flagged in the pre-reg §13), the multiplicative-transport PASS (v2.0) and additive-transport FAIL (v2.1) are separate sentences. A "framework is operationalization-asymmetric across transport" composite claim is **not authorized** by the juxtaposition. The 2×2 table above shows the four verdicts side by side without merging them.

### Does not license any broader claim

No scale examples, no physics, no ontology, no cross-framework synthesis, no upgrades of prior findings.

---

## Relationship to v1.1

v1.1 established the additive FAIL on Z/10 with Reason A attribution. v2.1 extends this per-carrier to 8 Path 2 carriers.

The relationship is direct: v2.1's per-carrier scores replicate v1.1's Z/10 scores exactly at every source (0/0 for operation-specific sources; −1/+1 for topology-neutral sources; aggregate −2/+2; gap 4). The Z/10 situation was not a local anomaly — it transports structurally through the P3AP extension.

v1.1's verdict unchanged. v2.1 adds the family-level extension as a separate sentence, not as an upgrade.

---

## Pilot Prediction Honesty

The §12 pilot prediction had an internal inconsistency between prose and label: it described "uniform indecisive pattern" (which matches §9.2's Uniform FAIL definition) but labeled the expected sub-pattern as "Below-threshold FAIL" (which requires $N_B > 0$ or $N_A > 0$).

The rubric-scored result followed §9.2's strict definitions, classifying the observed $N_B = N_A = 0$ configuration as Uniform FAIL. Per anti-tuning rule §11, the frozen pre-reg's definitions take precedence over prose predictions.

This is recorded as earned rather than retrofitted:
- The per-source scores match prediction exactly.
- The per-carrier verdicts match prediction exactly.
- The family-level FAIL matches prediction exactly.
- The sub-pattern label mismatches prediction.

The mismatch is a pre-reg authoring issue, not a scoring issue. Future PPM sprints should ensure the prose prediction and the sub-pattern label align with the §9.2 definitions.

---

## What Is Now Authorized Next

Each requires its own pre-registration:

### Priority 1 — PPM-v3.0 on Z/10 (different checkpoint)

Apply the framework's vocabulary to a different aspect of Z/10's structure (TSML/BHML relationship, V0 boundary, unit cyclic structure) to test whether the framework has additional points of contact beyond the subtype-mapping checkpoint. The 2×2 design space (local/transport × multiplicative/additive) is now complete for the subtype-mapping checkpoint; a second independent checkpoint would strengthen or weaken the framework's overall status.

### Priority 2 — Packaging

With PPM-v2.1 resolved, the pair-primitive pack's first open checkpoint is closed. The next packaging move would be an update to the PPM pack (adding v2.1) or a new sidecar packet for v2.1 artifacts. Per user's prior discipline (frozen packs are frozen), this would be a new small packet, not a merge.

### Priority 3 — PPM-v2.1.1 (optional)

Only if explicit test of "relaxed rubric" behavior is needed. Pilot analysis suggests outcome is predictable (still FAIL). Low information yield.

### Explicitly not authorized

- No shape-filter sprint. SAH infrastructure remains unbuilt.
- No scale-example, physics, or ontology sprints.
- No composite claim sprints.
- No upgrades of any prior finding.
- No reopening of closed lanes.
- No extension beyond the 8 P3AP carrier family.

---

## Program State After PPM-v2.1

### Sprint ledger addition

| # | Sprint | Path | Verdict | Attribution |
|---|---|---|---|---|
| 15 | PPM-v2.1 | 3 (bridge test) | **FAIL (Uniform)** | $N_B = N_A = 0$, $N_I = 8$; per-carrier +2/−2, gap 4; Sources 1 and 2 score 0/0 under additive reading on every carrier; v1.1's Reason A transports uniformly from Z/10 to the P3AP family. |

### Framework status update

The pair-primitive framework on the subtype-mapping checkpoint:
- **Local multiplicative (Z/10):** PASS (v1.0).
- **Local additive (Z/10):** FAIL (v1.1).
- **Transport multiplicative (8 P3AP carriers):** PASS uniform (v2.0).
- **Transport additive (8 P3AP carriers):** FAIL Uniform (v2.1).

The 2×2 design space is now complete. The framework discriminates decisively under multiplicative reading at both scopes and does not discriminate under additive reading at both scopes. The asymmetry is a carrier-family property under the P3AP extension.

### Closed lanes (unchanged)

Count transport under P3AP generator. Raw adjacency ratios. Noise-union seam topology bridge. Basin-ratio smoothness transport. Anchored basin-ratio curve. Empty-seam detectability on pure $C_0$.

### Open questions (updated)

**Previously open, now closed:**
- Additive operationalization transport on P3AP carriers → FAIL Uniform (v2.1).

**Remaining open:**
- PPM-v3.0 (different Z/10 checkpoint).
- Hub-extension overlay rules.
- Subtype transport for carriers outside the tested 8.
- SAH at foundation register.

---

## Integrity Statement

The FAIL is recorded honestly under pre-registered criteria. All 32 per-carrier-per-source scores (8 carriers × 4 sources) were computed deterministically from the frozen rubric applied to the frozen P3AP data under the frozen additive operational interpretation. Prohibited substitutions (§16 item 8) were honored: no rubric relaxation, no substitute Source 2 argument.

The sub-pattern classification mismatch between §12's prose prediction and §9.2's strict definitions was resolved in favor of the frozen pre-reg (per anti-tuning rule §11) and documented transparently in both RESULTS and this VERDICT. No post-hoc threshold adjustment. No scope widening. No composite claim with v2.0 (Rule 19).

The narrow question the spec committed to test has been answered cleanly: under additive operationalization with carrier-adapted Source 1 reading under strict AND, neither map transports across the 8 P3AP Path 2 carriers at pre-registered per-carrier cleanness. The additive non-discrimination on Z/10 (v1.1) is a carrier-family property under the P3AP extension, not a Z/10-specific property — which is what v2.1 earned.
