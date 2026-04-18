# PPM-v1.1 Additive Operationalization — Results
## Rubric Evaluation on Z/10's 8 Seam Cells Under Additive Reading

---

## Scope Declaration (Reproduced)

**Path:** Local Theorem Chart (Path 1), $h_\text{thm} = 7$.
**Operationalization:** Additive (Z/10's additive operation structure).
**Data:** Same 8 seam cells, same 3 inherited Path 3 findings as PPM-v1.0.
**Inherited clarification:** Verdict applies to the additive operationalization only; does not refute or confirm the framework in all possible readings.

---

## Per-Source Scoring Under Additive Reading

Scoring proceeded source-by-source per §8 anti-tuning rules.

### Source 1 — Structural backbone under additive reading

**Data recap.** MAX: 3 unordered edges on {2,4,8,9}. ADD: 1 edge on {1,2}.

**Rubric (§5.1 as rewritten for additive).** Persistent-side forms backbone requires: majority edges (≥50%) AND contains additive-flow elements.

**Evaluation.**
- ADD: minority (25%), native additive flow ✓. Meets native-flow but fails majority. Not backbone.
- MAX: majority (75%), non-additive ✗. Meets majority but fails native-flow. Not backbone.

Neither subtype meets both conditions. No additive backbone is present in the seam under strict AND criterion.

**Scores.**
- Map A: persistent-side (ADD) not backbone. Score: **0**.
- Map B: persistent-side (MAX) not backbone. Score: **0**.

### Source 2 — v1.1 identity-edge finding under additive reading

**Data recap.** ADD attaches vertex 1 at +6.06σ on 8 P3AP carriers. On Z/10, ADD edge is (1,2).

**Rubric (§5.2 as rewritten).** Requires coherent additive-structural reading of "ADD at vertex 1."

**Evaluation.** On Z/10, vertex 1 is **not** the additive identity. The additive identity is 0, located in the V0 boundary outside the seam. Vertex 1 is the additive generator. The v1.0 rubric's key argument — "identity is a multiplicative-absence point where excluded content must surface" — depends on a specific structural role (multiplicative trivialization) that does not translate to vertex 1 under additive reading.

Alternative candidate readings under additive operationalization were considered and rejected per §5.2 because introducing a new structural argument (e.g., "persistent at flow origin") is not a translation of v1.0's argument but a different claim requiring its own pre-registration.

**Scores.**
- Map A: no coherent additive parallel. Score: **0**.
- Map B: no coherent additive parallel. Score: **0**.

### Source 3 — Leaf-edge placement (topology-neutral)

**Data recap.** ADD is a leaf edge at +3.73σ. On Z/10, vertex 1 has degree 1.

**Rubric (§5.3 inherited).** Unchanged; leaf status is a graph-topological fact.

**Evaluation.** ADD edge (1,2) has degree-1 endpoint (vertex 1). ADD is unambiguously at the leaf.

**Scores.**
- Map A (persistent = ADD): persistent at leaf, inverting expected role. Score: **-1**.
- Map B (excluded = ADD): excluded at leaf, matching expected role. Score: **+1**.

### Source 4 — Topology-feature dominance (topology-neutral)

**Data recap.** Forest + single-component + low max degree at +12.56σ.

**Rubric (§5.4 inherited).** Unchanged; topology features attributed by edge-count majority and structural spine.

**Evaluation.** MAX carries 3 of 4 unordered edges, forest spine on {2,4,8,9}, low-degree profile. ADD contributes single-component connectivity.

**Scores.**
- Map A (persistent = ADD): persistent does not carry majority. Score: **-1**.
- Map B (persistent = MAX): persistent carries majority. Score: **+1**.

---

## Aggregate Scores

| Source | Map A | Map B |
|---|---:|---:|
| 1. Additive backbone | 0 | 0 |
| 2. Identity-edge (additive) | 0 | 0 |
| 3. Leaf-edge (topology-neutral) | −1 | +1 |
| 4. Topology-family (topology-neutral) | −1 | +1 |
| **Aggregate** | **−2** | **+2** |

**Cleanness gap:** $|(-2) - (+2)| = 4$.

---

## Pass / Fail / Unclear Evaluation

| Condition | Threshold | Value | Met? |
|---|---|---|:---:|
| Winner score | ≥ +3 | Map B: +2 | ✗ |
| Loser score | ≤ +1 | Map A: −2 | ✓ |
| Cleanness gap | ≥ 2 | 4 | ✓ |

**Winner score fails threshold.** Neither map reaches +3. Per §7.2: **FAIL**.

UNCLEAR conditions (§7.3) checked: neither map has ≥+3; Map A (−2) is not in {+2,+3}. Neither UNCLEAR condition fires.

---

## Cross-Check With Pilot Analysis

PPM-v1.1 §11 predicted:
- Source 1: 0 / 0
- Source 2: 0 / 0
- Source 3: −1 / +1
- Source 4: −1 / +1
- Aggregate: −2 / +2
- Gap: 4
- Predicted: FAIL

Rubric-scored result matches pilot prediction exactly. No source produced a different score than predicted.

---

## Diagnostic Character of the FAIL

The FAIL is not symmetric collapse — Map B retains a +2 lead over Map A, with cleanness gap 4 exceeding the ≥2 threshold. What fails is the winner-score threshold: Map B reaches +2 but not +3.

The structural reason is precisely localized:
- **Topology-neutral sources (3, 4):** score identically to v1.0. Map B lead of +1 each = +2 total.
- **Operation-specific sources (1, 2):** score 0 / 0 under additive reading. Under multiplicative reading these contributed +1 each for Map B = +2 total.

v1.0's +4 for Map B decomposed as +2 from topology-neutral + +2 from operation-specific. v1.1's +2 is exactly the +2 from topology-neutral. The +2 from operation-specific was extinguished by the switch from multiplicative to additive operationalization.

This matches the scope note's **Outcome 3 / Reason A**: Z/10's seam is multiplicatively loaded. The TSML is multiplicatively framed; the seam's structural anchors for Sources 1 and 2 (doubling-chain backbone, multiplicative identity) have no clean additive analogs. Additive reading finds the seam's discriminating signals on topology-neutral features only.

The FAIL is diagnostic, not refutational. It refutes the additive operationalization's ability to decisively discriminate on this seam, not the framework broadly.

---

## What the Data Shows

Under the frozen spec of PPM-v1.1:

1. All four sources score deterministically under the frozen rubric.
2. Sources 1 and 2 score 0/0 under additive reading — the rubric criteria fail to discriminate because Z/10's seam does not contain an additive backbone meeting strict criteria, and vertex 1 is not the additive identity.
3. Sources 3 and 4 score identically to v1.0 (−1/+1) because they are topology-neutral.
4. Aggregate: Map A = −2, Map B = +2, cleanness gap = 4.
5. Map B retains a meaningful lead but fails to clear the ≥+3 winner threshold.
6. Verdict: **FAIL**.

---

## What the Data Does NOT Say

- Does NOT refute the pair-primitive framework.
- Does NOT refute Map B under multiplicative operationalization (v1.0 PASS stands).
- Does NOT prove Z/10's seam is multiplicatively loaded (this is a diagnostic hypothesis supported by the score pattern, not a confirmed property).
- Does NOT close the additive operationalization permanently — a v1.1.1 with refined additive rubric or a different ring with additive-native seam structure could revisit.
- Does NOT extend to other rings.
- Does NOT authorize scale examples, physics, or ontology.

Verdict follows in `PPM_V11_ADDITIVE_VERDICT.md`.
