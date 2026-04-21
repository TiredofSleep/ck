# PPM-v2.1 Additive Transport — Results
## Per-Carrier v1.1 Rubric Applied to 8 P3AP Path 2 Carriers

---

## Scope Declaration (Reproduced)

**Path:** Path 3 Bridge Test.
**Operationalization:** Additive, carrier-adapted for Source 1 under strict AND.
**Data:** P3AP recovered seams for 8 Path 2 carriers as-is.
**Inherited clarification:** Verdict applies to the additive operationalization under the P3AP extension only; does not refute or confirm the framework in all possible readings.

---

## Per-Carrier Scoring

Scoring proceeded carrier-by-carrier per §11 anti-tuning rules. Prohibited substitutions (§16 item 8) honored: no rubric relaxation, no substitute Source 2 argument.

### Full per-carrier score matrix

| Carrier | S1 A | S1 B | S2 A | S2 B | S3 A | S3 B | S4 A | S4 B | Agg A | Agg B | Gap | Per-carrier verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| Z/14 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | **−2** | **+2** | 4 | **INDECISIVE** |
| Z/22 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | **−2** | **+2** | 4 | **INDECISIVE** |
| Z/34 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | **−2** | **+2** | 4 | **INDECISIVE** |
| Z/42 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | **−2** | **+2** | 4 | **INDECISIVE** |
| Z/46 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | **−2** | **+2** | 4 | **INDECISIVE** |
| Z/58 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | **−2** | **+2** | 4 | **INDECISIVE** |
| Z/74 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | **−2** | **+2** | 4 | **INDECISIVE** |
| Z/94 | 0 | 0 | 0 | 0 | −1 | +1 | −1 | +1 | **−2** | **+2** | 4 | **INDECISIVE** |

### Per-Source Rationale Across Carriers

**Source 1 — Structural backbone under additive reading (strict AND).** On every carrier: ADD has native-additive alignment (ADD cells apply the additive rule) but is in the minority (17–33% of unordered edges); MAX has majority (67–83%) but is non-additive (max rule is order-based, not aligned with additive flow). Strict AND criterion (majority AND native-additive-flow alignment) is met by neither subtype. No additive backbone present under the frozen criterion.
- Map A (persistent=ADD): ADD is not backbone. Score: **0**.
- Map B (persistent=MAX): MAX is not backbone. Score: **0**.

**Source 2 — Identity-edge reading under additive reading.** On every carrier: additive identity on Z/n is 0, located in V0 boundary outside the seam graph. ADD does NOT touch vertex 0 on any carrier. ADD touches vertex 1 on every carrier, but vertex 1 is the additive generator, not the additive identity. The v1.0 multiplicative-trivialization argument ("identity is a multiplicative-absence point where excluded content must surface") has no clean additive parallel because vertex 1 plays a productive role under addition (generator of the cyclic group), not a trivialization role. Per §5.2, substitute arguments are prohibited — no reading of "ADD at additive-generator = persistent at flow origin" may be introduced.
- Map A: no coherent additive parallel. Score: **0**.
- Map B: no coherent additive parallel. Score: **0**.

**Source 3 — Leaf-edge placement (topology-neutral).** On every carrier: ADD edge is (1,2), vertex 1 has degree 1 in full seam graph, ADD is at the leaf.
- Map A (persistent=ADD): persistent at leaf, inverting expected role. Score: **−1**.
- Map B (excluded=ADD): excluded at leaf, matching expected role. Score: **+1**.

**Source 4 — Topology-feature dominance (topology-neutral).** On every carrier: MAX carries 67–83% of edges, MAX-only subgraph is connected, forest spine is MAX-dominated.
- Map A (persistent=ADD): persistent does not carry majority. Score: **−1**.
- Map B (persistent=MAX): persistent carries majority. Score: **+1**.

---

## Family Aggregation (Primary)

| Metric | Value | Threshold | Met? |
|---|---:|---:|:---:|
| $N_B$ (carriers supporting Map B) | **0** | ≥ 6 | ✗ |
| $N_A$ (carriers supporting Map A) | **0** | ≥ 6 | ✗ |
| $N_I$ (indecisive carriers) | **8** | — | — |

Neither PASS-B ($N_B \geq 6$) nor PASS-A ($N_A \geq 6$) threshold met.

## Family Aggregation (Secondary, Reported Not Scored)

| Metric | Value |
|---|---:|
| Mean per-carrier cleanness gap across all 8 carriers | 4.00 |

Every carrier produced cleanness gap 4 (Map B lead of +2 over Map A = −2). The gap is meaningful but uniformly sub-threshold at the per-carrier winner level.

---

## Pass / Fail / Unclear Evaluation

Per §9.2: neither $N_B$ nor $N_A$ reaches 6. **FAIL**.

**Sub-pattern classification per §9.2:**
- Uniform FAIL: $N_B = N_A = 0$ → **MATCH** ($N_B = 0$ AND $N_A = 0$).
- Split FAIL: $N_B > 0$ AND $N_A > 0$ → does not match.
- Below-threshold FAIL: one of $N_B, N_A > 0$ but below 6, other = 0, $N_I > 0$ → does not match.

**Sub-pattern: Uniform FAIL.**

UNCLEAR condition (§9.3) checked: $N_B = 5$ with $N_A = 0$ and $N_I = 3$ (or symmetric) — does not match. Neither UNCLEAR condition fires.

---

## Cross-Check With Pilot Prediction (Rule 21)

PPM-v2.1 §12 predicted:
- Every source scoring as observed (S1 = 0/0, S2 = 0/0, S3 = −1/+1, S4 = −1/+1).
- Every carrier aggregate: Map A = −2, Map B = +2, gap = 4.
- Every carrier verdict: INDECISIVE.
- Family aggregation: $N_B = 0$, $N_A = 0$, $N_I = 8$.
- Predicted verdict: FAIL.
- **Predicted sub-pattern: Below-threshold FAIL.**

Rubric-scored result matches pilot prediction exactly at the per-source, per-carrier, and family-level verdict layers. **One mismatch: sub-pattern classification.**

### Sub-pattern mismatch — honest recording

The §12 prediction expected "Below-threshold FAIL (specifically: uniform indecisive pattern)." The rubric-scored result triggers Uniform FAIL per the strict definition in §9.2 ($N_B = N_A = 0$).

The mismatch arose because:
- §9.2 defines Uniform FAIL as "$N_B = N_A = 0$ (no carrier supports either map)."
- §9.2 defines Below-threshold FAIL as "one of $N_B, N_A > 0$ but below 6, other = 0, $N_I > 0$."
- §12's prose prediction described "uniform indecisive pattern" and attached it to "Below-threshold FAIL" — but the uniform indecisive pattern ($N_I = 8$) actually satisfies the Uniform FAIL definition, not Below-threshold FAIL.

The §12 prediction had an internal inconsistency between its prose description ("uniform indecisive") and the sub-pattern label ("Below-threshold"). The frozen pre-reg's §9.2 definitions are authoritative; the script classified correctly per those definitions.

Per anti-tuning rule §11 and user discipline ("record it as earned rather than assumed"), the recorded verdict follows the rubric-scored classification. The §12 prediction mismatch is documented here and not retrofitted.

---

## Diagnostic Character of the Uniform FAIL

The FAIL is structurally precise and carrier-uniform:

- **Topology-neutral sources (3, 4):** score identically on every carrier ( Map A −1, Map B +1), matching PPM-v2.0's topology-neutral scoring. This produces Map B's +2 lead across all carriers.
- **Operation-specific sources (1, 2):** score 0/0 on every carrier under additive reading. Source 1 fails because no subtype meets strict AND (majority + native-additive-alignment); Source 2 fails because vertex 1 is additive generator, not additive identity, and substitute arguments are prohibited.

The per-carrier aggregate +2/−2 is the maximum cleanness gap achievable from only the topology-neutral sources. The operation-specific sources contributed nothing discriminating under additive reading.

This matches Z/10's v1.1 result exactly at the per-carrier level. The additive non-discrimination transports from Z/10 to the entire P3AP family, confirming that **Reason A** (seam's multiplicative loading, per `STABILITY_VS_FLIP_SCOPE_NOTE.md`) is a carrier-family property, not a Z/10-specific property. The TSML's multiplicative framing transports through the P3AP extension to every Path 2 carrier, producing the same additive-reading non-discrimination.

---

## What the Data Shows

Under the frozen spec of PPM-v2.1:

1. All 8 Path 2 carriers were scored deterministically against v1.1's rubric under additive operationalization with carrier-adapted Source 1 reading.
2. Every carrier produced Map A = −2, Map B = +2, cleanness gap = 4.
3. Every carrier classified as INDECISIVE under the per-carrier verdict rule.
4. Family aggregation: $N_B = 0$, $N_A = 0$, $N_I = 8$.
5. Neither PASS threshold met.
6. Verdict: **FAIL, sub-pattern Uniform FAIL per §9.2 definitions**.

---

## What the Data Does NOT Say

- Does NOT refute the pair-primitive framework. Refutes only the additive operationalization's decisive discrimination at family level on these carriers.
- Does NOT refute Map B under multiplicative operationalization. v1.0 PASS and v2.0 PASS stand.
- Does NOT refute Map A. No carrier supported Map A, but no carrier supported Map B either — the rubric does not discriminate, regardless of which map might eventually prove correct under a different reading.
- Does NOT prove the seam is multiplicatively loaded in general. Supports "Reason A is a carrier-family property" as a diagnostic finding under the tested rubric; does not prove the property at the level of a theorem.
- Does NOT close the additive operationalization permanently. A v2.1.1 with relaxed Source 1 criterion or alternative Source 2 substitute could be pre-registered, but each would be a different sprint requiring separate approval.
- Does NOT extend to rings outside the 8 P3AP carriers.
- Does NOT merge with v2.0 into a composite claim (Rule 19).
- Does NOT authorize scale examples, physics, ontology, or cross-domain reading.
- Does NOT validate or refute SAH. SAH remains a hypothesis at foundation register in the sidecar packet.

---

## Earned, Not Assumed

Per user discipline: "if the result is the predicted uniform indecisive pattern, record it as earned rather than assumed."

The uniformity is earned by:
1. Explicit per-carrier rubric application in deterministic code (`ppm_v21_score.py`).
2. Explicit per-source rationale for each carrier, traceable to frozen §5.
3. Prohibited substitutions (§16 item 8) honored in the scoring script — no rubric relaxation, no substitute Source 2 argument.
4. The sub-pattern classification mismatch between §12 prediction and §9.2 definitions recorded transparently, with the frozen pre-reg's definition taking precedence (anti-tuning rule).
5. Pilot prediction cross-check recorded honestly, including the mismatch point.

The result is not a documentation derivation. It is an executed rubric application producing per-carrier scores that, uniformly, produced the indecisive classification — and the frozen §9.2 definitions classify that as Uniform FAIL, not Below-threshold FAIL.

Verdict follows in `PPM_V21_ADDITIVE_TRANSPORT_VERDICT.md`.
