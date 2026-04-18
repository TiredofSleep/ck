# Pair-Primitive Mapping — Verdict
## PPM-v1.0 Final Determination

---

## Verdict: **PASS (Map B)**

---

## One-Paragraph Justification

Under the pre-registered criteria of PPM-v1.0 §7.1, all three PASS conditions are met and exactly one map wins. Per-source rubric scoring returned unambiguous values on all four data sources: Source 1 (seam-graph structural split) scored $-1/+1$ with MAX forming 3 of 4 unordered edges and containing both the doubling chain $2\text{–}4\text{–}8$ and the attractor-involution edge $2\text{–}9$; Source 2 (v1.1 identity-edge finding) scored $-1/+1$ under the §5.2 key criterion that identity is a multiplicative-absence point where excluded content must surface; Source 3 (v1.2-adj leaf-edge finding) scored $-1/+1$ with ADD unambiguously at the graph boundary; Source 4 (P3AP topology-family finding) scored $-1/+1$ with persistent-side MAX carrying the forest spine, low-degree profile, and low-degree-vertex dominance. Aggregate scores were Map A $= -4$ and Map B $= +4$, with cleanness gap $8$ — substantially exceeding the $\geq 2$ threshold. Winner score $+4 \geq +3$; loser score $-4 \leq +1$. The rubric-scored result matches the PPM-v1.0 §12 pilot prediction exactly. Per anti-tuning rule §8, no post-hoc adjustment has been made. The verdict is PASS with Map B as the winner.

---

## The Verdict Sentence (Pre-Registered in §9)

> **Under the pair-primitive framework's vocabulary applied to Z/10's multiplicative operation structure with the operational interpretation in PPM-v1.0 §3, Map B (MAX = persistent, ADD = excluded) produces a coherent structural fit across the four pre-registered data sources at cleanness gap ≥ 2.**

This is the entirety of the verdict's content. It does not extend beyond its exact statement.

---

## What This PASS Establishes

The pair-primitive framework's first rigorous checkpoint returns a coherent structural fit under the operationalization fixed in PPM-v1.0 §3:

- The 6 MAX seam cells on Z/10 form the persistent-side reading of the pair — the multiplicative backbone carrying the doubling-chain flow and the attractor-involution.
- The 2 ADD seam cells form the excluded-side reading — localized departures from the multiplicative rule, surfacing at the multiplicative-absence point (identity) and at the graph boundary (leaf position).
- The three inherited Path 3 findings (P3AP, v1.1, v1.2-adj) all read coherently under Map B, consistent with MAX-as-persistent / ADD-as-excluded on Z/10.

This is the narrow sentence the sprint earns. The framework has its first point of contact with the program's rigorous register.

---

## What This PASS Explicitly Does NOT Establish

Per the scope discipline locked in `PASS_MEANING_SCOPE_NOTE.md` before the sprint ran, a PASS does NOT carry beyond its exact statement. Specifically:

### Not framework correctness in general

A single checkpoint PASS is consistency with one specific data point under one specific operationalization. It is not proof that the pair primitive is the correct framework. Multiple independent points of contact, under different operational lenses, would be needed before framework correctness could be claimed.

### Not validity of the framework under alternative operationalizations

Per the wording clarification locked into the frozen spec: this sprint evaluates the pair-primitive framework under a multiplicative operationalization only. A passage confirms the framework under this operationalization, not in all possible readings. Additive, dual, or other operationalizations are not tested. Whether Map B remains the winner under an additive operationalization, or whether a different mapping appears under a different operational lens, is entirely untested by this sprint.

### Not extension to rings outside Z/10

The sprint operates on Z/10's 8 seam cells. The P3AP extension tested Path 2 carriers but that is inherited context, not the scored data of this sprint. Whether the same Map B assignment holds when the framework's vocabulary is applied to seam graphs on Z/14, Z/22, and other compatibility-family rings is a separate question requiring its own pre-registration.

### Not upgrade of Path 3 findings

The v1.1 identity-edge PASS ($+6.06\sigma$), the v1.2-adj leaf-edge PASS ($+3.73\sigma$), and the P3AP topology-family PASS ($+12.56\sigma$) stand as originally recorded in the B2 pack. This sprint did not re-score those findings; it used them as inherited context for a different structural claim. The verdicts of those sprints are unchanged.

### Not license for scale-example sprints

The foundation note's five-feature schema for scale realizations (neutron, atom, cell, body, planet, solar system, galaxy, black hole) was explicitly a compatibility check, not a prediction. A PASS on the subtype mapping does not carry over to the schema. No scale-example sprint is authorized by this result.

### Not closure or reopening of prior lanes

The count-transport lane remains closed under the P3AP generator. The hub-extension question remains deferred. The raw-adjacency-ratio lane remains abandoned. This PASS does not change any of those statuses.

### Not theorem-level content

This is a structural-fit claim under a specific operationalization of a framework. It is not a theorem on Z/10 and does not alter the Z/10 TSML 3-layer tower theorem's status or content.

---

## Relationship to Prior Sprints

This sprint does not affect the record of the B2 closeout pack. The 11 sprints in that pack stand with their original verdicts unchanged. PPM-v1.0 is a new sprint, scoped at Path 1 on the local theorem chart, testing a framework-level structural claim with a different kind of rubric (structural evaluation, not numerical null-comparison) than the prior bridge sprints used.

The relationship to the three inherited Path 3 findings is one-way: PPM-v1.0 uses them as already-recorded data about Z/10's seam and about Path 2 carrier behavior. PPM-v1.0 does not add to them. The inherited findings' sentences are unchanged.

---

## What Is Authorized Next

A PASS on the first framework checkpoint makes several successor directions legitimate, **each requiring its own pre-registration under the scope-tag discipline**:

### PPM-v1.1 — Additive operationalization check (same sprint structure, different operation structure)

The current sprint committed to multiplicative operationalization. A natural follow-up: under an additive operationalization of the framework's vocabulary, does the mapping flip to Map A (ADD = persistent under additive flow, MAX = excluded under additive flow)? This would test whether the framework's pair primitive is symmetric between the 2×2 theorem's two structures, or whether one operation structure dominates. Requires its own pre-reg with frozen rubric.

### PPM-v2.0 — Other rings in the compatibility family

Does Map B assignment hold on Z/14, Z/22, Z/34, Z/42, Z/46, Z/58, Z/74, Z/94 under the P3AP extension? The 8 Path 2 carriers from the B2 pack provide the data infrastructure. A separate sprint would apply the PPM-v1.0 rubric to each carrier's ADD/MAX structure and test whether the multiplicative operationalization extends.

### PPM-v3.0 — Third data source test

The checkpoint passed on four data sources. A stronger test would identify additional specific structural claims the framework makes, each with binary consequences, and score them separately. Candidates: the TSML/BHML relationship, the V0 boundary of the Z/10 table, the cyclic structure of the ring's units. Each would need its own rubric.

### Explicitly not authorized

- No scale-example sprints (foundation schema remains a compatibility check).
- No physics, ontology, or cross-domain sprints.
- No "pair + 2×2 synthesis" sprint without its own pre-reg.
- No upgrade of the framework to theorem status based on this or any accumulation of checkpoints.
- No reopening of closed lanes.

---

## Program State After PPM-v1.0

### Sprint ledger addition

Adding to the B2 pack's 11-sprint record:

| # | Sprint | Path | Verdict | Attribution |
|---|---|---|---|---|
| 12 | PPM-v1.0 | 1 (local theorem chart) | **PASS (Map B)** | Aggregate $+4$/$-4$ under multiplicative operationalization; cleanness gap $8$; all four data sources score unambiguously; framework's first checkpoint consistent. |

### Framework status

The pair-primitive framework, as specified in the foundation sprint documents (`WHY_THE_WHOLE_INTERACTION_MUST_BE_SEEN_AT_ONCE.md`, `THREE_ASPECTS_OF_HOLD.md`, `GAP_AS_BOUNDARY_NOTHINGNESS.md`, `HOLD_GAP_FLOW_FOUNDATION.md`), has its first confirmation of consistency under one operationalization. It remains:

- **Suggestive**, not proven.
- **Untested** under additive or dual operationalizations.
- **Untested** on rings outside Z/10.
- **Untested** on any scale-example realization.

The framework's status in the exact/suggestive/research-direction taxonomy (foundation note §"What Is Exact, Suggestive, Research Direction") is updated to: **one checkpoint passed under one operationalization; remaining structural claims still suggestive or research-direction.**

### Closed lanes (unchanged)

Count transport under P3AP generator. Raw adjacency ratios. Noise-union seam topology bridge. Basin-ratio smoothness transport. Anchored basin-ratio curve. Empty-seam detectability on pure $C_0$.

### Open questions (unchanged)

Hub-extension overlay rules. Identity-element attachment under alternative extensions. Leaf-edge placement under alternative extensions. Subtype transport for carriers outside the tested 8-carrier family. Five-feature schema validity at any scale. Parameterized generator family for count transport.

### Now-authorized question classes (new)

Additional pair-primitive framework checkpoints at Path 1 or bridge-scope, each requiring separate pre-registration.

---

## Integrity Statement

The PASS is recorded honestly with full scope boundaries. All four per-source scores were computed deterministically from the frozen rubric applied to the frozen data sources under the frozen operational interpretation. The aggregate result matches the §12 pilot prediction exactly, which is a cross-check rather than a tuning signal — the rubric was specified before pilot analysis was performed and the pilot's predictions were made public in the pre-reg. No source required post-hoc interpretation; no threshold was adjusted; no data source was substituted.

The narrow question the spec committed to test has been answered cleanly: under the multiplicative operationalization of the pair-primitive framework on Z/10's 8 seam cells, Map B (MAX = persistent, ADD = excluded) produces a coherent structural fit at pre-registered cleanness, and Map A does not.

This is the entirety of what the sprint earned. Nothing beyond it.
