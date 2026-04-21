# PPM-v2.1 — Additive Operationalization Transport
## First Open Next Checkpoint After the 2026-04-18 Handoff

---

## Status

**Not yet executed.** This document describes the sprint's expected shape so any future executor (including a later session of this program, or ClaudeCode acting on the user's direction) has a starting point.

**The sprint is not frozen.** The specifics below are candidate design choices, not pre-registered commitments. A real PPM-v2.1 pre-reg would be written, reviewed, and frozen before execution per this pack's discipline rules.

---

## Why PPM-v2.1 Is The First Open Next Checkpoint

After v1.0 (local multiplicative PASS on Z/10), v1.1 (local additive FAIL on Z/10), and v2.0 (family multiplicative transport PASS on 8 P3AP carriers), the natural pair to v2.0 is the additive operationalization test on the same 8 carriers.

The existing verdicts leave a specific asymmetry: multiplicative operationalization has been tested both locally and at family-transport level, with PASS in both cases. Additive operationalization has been tested only locally (FAIL with diagnostic attribution). Whether the additive FAIL is Z/10-specific or transports to the family is an open question.

This is the natural first checkpoint after handoff because it closes the $2 \times 2$ design space (local/transport × multiplicative/additive) over the existing data infrastructure, using only the P3AP recovered seams already validated in the B2 pack.

---

## Expected Scope

**Path:** Path 3 Bridge Test.
**Operationalization:** Additive, carrier-adapted.
**Data:** Same 8 P3AP Path 2 carriers used by PPM-v2.0.
**Rubric:** inherit PPM-v1.1's additive operationalization of v1.0's four sources, applied per carrier.
**Aggregation:** per-carrier verdict, count of supports_B carriers, same threshold $N_B \geq 6$ as v2.0 (parallel discipline).

## Pilot Expectation (From Structural Reasoning, Not Pre-Registered)

Every Path 2 carrier has the same rubric-relevant structure under additive reading as Z/10 did under v1.1:

- ADD edge = (1, 2) on every carrier. Vertex 1 is the multiplicative identity (not the additive identity) on every carrier.
- MAX forms majority of edges on every carrier but is not native to additive operation.
- Additive identity is 0 on every carrier; 0 is outside the seam graph (V0 boundary).

Under v1.1's strict-AND criterion for Source 1 (majority + native-additive-flow alignment) and v1.1's Source 2 key-criterion reading (vertex 1 not being additive identity):

- **Source 1:** predicted 0/0 on every carrier (neither subtype meets both conditions).
- **Source 2:** predicted 0/0 on every carrier (vertex 1 is multiplicative identity, not additive identity; the v1.0 key argument has no additive parallel).
- **Source 3:** predicted −1/+1 on every carrier (topology-neutral, inherits from v2.0's per-carrier scoring).
- **Source 4:** predicted −1/+1 on every carrier (topology-neutral).

Predicted per-carrier aggregate: Map A = −2, Map B = +2, cleanness gap = 4. Predicted per-carrier verdict: **INDECISIVE** on every carrier (Map B leads but doesn't clear +3).

Predicted family verdict: $N_B = 0$, $N_A = 0$, $N_I = 8$. **Predicted: Below-threshold Family FAIL.**

## Why The Pilot-Predictable Outcome Is Still Worth Running

Unlike v1.1.1 (where the analytical prediction derives straightforwardly from v1.1's already-executed scoring), v2.1's pilot expectation is derived from structural uniformity of the 8 P3AP carriers. The sprint would:

1. **Earn the uniform result per-carrier rather than assume it.** Following v2.0's pattern — diagnostic possibilities named in advance, resolved transparently under rubric application.
2. **Produce the exact family-level count.** A Below-threshold Family FAIL with $N_I = 8$ is a different finding than $N_I = 7$ with one supporting carrier. The sprint earns which of these is the case.
3. **Complete the $2 \times 2$ design space.** With v2.1 executed, the program has: multiplicative local PASS, multiplicative transport PASS, additive local FAIL, additive transport FAIL. Four specific sentences rather than three sentences and one open question.

The value is diagnostic symmetry, not major new ground. The user's direction at handoff time was explicit on this point: "its likely value is diagnostic symmetry, not major new ground."

## What PPM-v2.1 Would Not Do

- Would not upgrade any prior verdict.
- Would not introduce new rubric structure.
- Would not widen scope to carriers outside P3AP 8.
- Would not test alternative additive rubrics (that would be v2.1.1 or similar).
- Would not license any scale-example, physics, or cross-domain claim regardless of outcome.

## Deliverable Pattern

Following the PPM template:
1. `PPM_V21_ADDITIVE_TRANSPORT_PREREG.md` — frozen per-carrier rubric under additive reading.
2. `PPM_V21_ADDITIVE_TRANSPORT_RESULTS.md` — per-carrier table, family aggregation.
3. `PPM_V21_ADDITIVE_TRANSPORT_VERDICT.md` — one paragraph + narrow sentence.
4. `PPM_V21_ADDITIVE_TRANSPORT_REPRO.md` — how to rerun.
5. `PPM_V21_PER_CARRIER_SCORES.json` — per-carrier scores from deterministic script.
6. `ppm_v21_score.py` — scoring script (adapted from `ppm_v20_score.py`).

## How To Approach Running v2.1

When the program returns to this checkpoint:

1. Open this document and confirm the scope.
2. Write the pre-reg as DRAFT, sending for user approval (don't auto-freeze).
3. Apply the three load-bearing discipline rules from `PACKING_RULES.md`:
   - **Rule 18** (wording clarification): inherit v1.0's clarification with "additive" substituted in.
   - **Rule 19** (no composition): v2.1's verdict is a separate sentence; do not merge with v1.1 or v2.0 into composite claims.
   - **Rule 21** (disclose diagnostic possibilities): name specific cases where the uniform prediction might break; resolve them transparently in scoring.
4. On approval, freeze and execute.
5. Write deliverables per the pattern above.
6. Either add to this pack (if user reopens it) or start a new pack with cross-references.

---

## Note On Priority

The user's handoff direction was explicit: **package current state before running v2.1**. The sprint is authorized but deferred. Executing v2.1 before packaging would risk inflating the handoff with work that has not yet earned its sentence.

This document exists so the v2.1 checkpoint is **named and scoped** in the pack, not forgotten. It is not a pre-registration; it is a placeholder indicating that v2.1 is the first real sprint to run after handoff, whenever the user directs that work to begin.
