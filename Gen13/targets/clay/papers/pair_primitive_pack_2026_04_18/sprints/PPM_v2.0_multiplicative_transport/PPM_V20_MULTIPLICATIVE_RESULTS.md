# PPM-v2.0 Multiplicative Transport — Results
## Per-Carrier v1.0 Rubric Applied to 8 P3AP Path 2 Carriers

---

## Scope Declaration (Reproduced)

**Path:** Path 3 Bridge Test.
**Operationalization:** Multiplicative, carrier-adapted for Source 1.
**Data:** P3AP recovered seams for 8 Path 2 carriers as-is.
**Inherited clarification:** Verdict applies to the multiplicative operationalization under the P3AP extension only; does not refute or confirm the framework in all possible readings.

---

## Per-Carrier Scoring

Scoring proceeded carrier-by-carrier per §11 anti-tuning rules. Each carrier was scored on all four sources before moving to the next.

### Full per-carrier score matrix

| Carrier | S1 A | S1 B | S2 A | S2 B | S3 A | S3 B | S4 A | S4 B | Agg A | Agg B | Gap | Per-carrier verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| Z/14 | −1 | +1 | −1 | +1 | −1 | +1 | −1 | +1 | **−4** | **+4** | 8 | **SUPPORTS_B** |
| Z/22 | −1 | +1 | −1 | +1 | −1 | +1 | −1 | +1 | **−4** | **+4** | 8 | **SUPPORTS_B** |
| Z/34 | −1 | +1 | −1 | +1 | −1 | +1 | −1 | +1 | **−4** | **+4** | 8 | **SUPPORTS_B** |
| Z/42 | −1 | +1 | −1 | +1 | −1 | +1 | −1 | +1 | **−4** | **+4** | 8 | **SUPPORTS_B** |
| Z/46 | −1 | +1 | −1 | +1 | −1 | +1 | −1 | +1 | **−4** | **+4** | 8 | **SUPPORTS_B** |
| Z/58 | −1 | +1 | −1 | +1 | −1 | +1 | −1 | +1 | **−4** | **+4** | 8 | **SUPPORTS_B** |
| Z/74 | −1 | +1 | −1 | +1 | −1 | +1 | −1 | +1 | **−4** | **+4** | 8 | **SUPPORTS_B** |
| Z/94 | −1 | +1 | −1 | +1 | −1 | +1 | −1 | +1 | **−4** | **+4** | 8 | **SUPPORTS_B** |

### Per-Source Rationale Across Carriers

**Source 1 — Structural backbone (carrier-adapted).** On every carrier, MAX meets the three required conditions: majority of unordered edges (≥50%), connected MAX-only subgraph, contains doubling chain starting from vertex 2. ADD meets only the "contains doubling chain" condition trivially (it doesn't, since ADD only has 1 edge; the doubling-chain check fails for ADD). Therefore MAX is the backbone on every carrier; ADD is not.
- Map A (persistent=ADD): persistent is not backbone → −1 on every carrier.
- Map B (persistent=MAX): persistent is backbone → +1 on every carrier.

Z/14's closest-to-boundary case: $|E_\text{MAX}|=2$ (attractor-involution audit-removed), so backbone is reduced to just the doubling chain 2-4-8. But majority ($2/3 = 67\% \geq 50\%$), connected, and contains doubling chain. Criterion still met. Score unchanged.

**Source 2 — Identity-edge reading (inherited verbatim).** On every carrier, ADD edge = (1,2), and vertex 1 is the multiplicative identity on every Z/n. The §5.2 key criterion applies identically: identity is a multiplicative-trivialization point; ADD surfacing at identity = excluded content surfacing at multiplicative-absence.
- Map A: contradicts §3 on every carrier → −1.
- Map B: coheres with §3 on every carrier → +1.

**Source 3 — Leaf-edge placement (inherited verbatim).** On every carrier, vertex 1 has degree 1 in the seam graph (ADD is the only edge touching it). ADD is unambiguously at the graph boundary.
- Map A (persistent=ADD): persistent at leaf → −1 on every carrier (inverts expected role).
- Map B (excluded=ADD): excluded at leaf → +1 on every carrier.

**Source 4 — Topology-feature dominance (inherited verbatim).** On every carrier, MAX carries the majority of unordered edges (5/6 on most, 2/3 on Z/14) and forms a connected substructure (doubling chain + extension edges). Forest spine is MAX-dominated; low-degree profile is MAX-driven. ADD contributes single-component connectivity via vertex 1.
- Map A (persistent=ADD): persistent does not carry majority → −1 on every carrier.
- Map B (persistent=MAX): persistent carries majority → +1 on every carrier.

---

## Family Aggregation (Primary)

| Metric | Value | Threshold | Met? |
|---|---:|---:|:---:|
| $N_B$ (carriers supporting Map B) | **8** | ≥ 6 | ✓ |
| $N_A$ (carriers supporting Map A) | 0 | — | — |
| $N_I$ (indecisive carriers) | 0 | — | — |

**$N_B = 8/8$. Family-level PASS threshold met with margin of 2.**

## Family Aggregation (Secondary, Reported Not Scored)

| Metric | Value |
|---|---:|
| Mean per-carrier cleanness gap across all 8 carriers | 8.00 |
| Mean per-carrier cleanness gap across SUPPORTS_B carriers | 8.00 |

Every carrier reached maximum possible cleanness gap (8) under the rubric, meaning no carrier showed partial support — each was decisively in the SUPPORTS_B category at the per-carrier level.

---

## Pass / Fail / Unclear Evaluation

Per §9.1: $N_B \geq 6$ → **PASS**.

Sub-pattern (from §9.2, reported for transparency even on PASS): the PASS is uniform — $N_B = 8/8$ with $N_A = N_I = 0$. No carrier-level variation.

---

## Cross-Check With Pilot Prediction

§12 of the pre-reg predicted:
- All 8 carriers as "strong carriers expected."
- No ambiguous carriers identified.
- No likely-indecisive carriers identified.
- Predicted $N_B = 8$, $N_A = 0$, $N_I = 0$. Predicted PASS.

Rubric-scored result matches pilot prediction exactly. The §12 note acknowledged that the uniform prediction arises from P3AP's design-level uniformity of carrier seams; the sprint confirms that prediction against actual rubric application.

Two diagnostic possibilities flagged in the pre-reg:
- **Z/14 Source 1 boundary case:** predicted uncertain due to $|E_\text{MAX}|=2$ and missing attractor-involution. Rubric-scored result: Z/14 passes Source 1 because the strict criterion (majority + connected + doubling-chain-present) is met even with the minimal backbone. No boundary issue in execution.
- **Z/22 Source 4 extension-edge sensitivity:** predicted uncertain due to (10,16)+(10,20) extension edges. Rubric-scored result: Z/22 passes Source 4 because topology-feature attribution is majority-driven, and MAX's 5/6 edges carry the majority regardless of which specific extension edges are included. No sensitivity in execution.

Both flagged possibilities resolved cleanly under the frozen rubric.

---

## What the Data Shows

Under the frozen spec of PPM-v2.0:

1. All 8 Path 2 carriers were scored deterministically against v1.0's rubric under multiplicative operationalization with carrier-adapted Source 1 reading.
2. Every carrier produced the maximum possible per-carrier score (Map A = −4, Map B = +4, cleanness gap = 8).
3. Every carrier classified as SUPPORTS_B under the per-carrier verdict rule (§6).
4. Family-level $N_B = 8$ meets the $\geq 6$ threshold with margin of 2.
5. Secondary summary confirms uniform maximum cleanness across carriers.
6. Verdict: **PASS**, uniform support pattern.

---

## What the Data Does NOT Say

- Does NOT refute the pair-primitive framework's limitations. It confirms transport under one specific operationalization on one specific extension.
- Does NOT extend Map B to carriers outside the 8 P3AP family. The tested family is fixed.
- Does NOT test additive operationalization on Path 2 (separate sprint). v1.1's FAIL on Z/10 stands; its additive implications for Path 2 are unknown.
- Does NOT authorize hub-extension or any new generator.
- Does NOT upgrade any prior Path 3 sprint's finding. v1.1 identity-edge (+6.06σ), v1.2-adj leaf-edge (+3.73σ), P3AP topology-family (+12.56σ) stand unchanged.
- Does NOT merge with v1.0 into a composite claim stronger than the two sentences together permit.
- Does NOT authorize scale examples, physics, ontology, or cross-domain reading.

---

## Earned, Not Assumed

Per the user's main discipline: "if the result is uniform as predicted, record it cleanly as earned rather than assumed."

The uniformity is earned by:
1. Explicit per-carrier rubric application in deterministic code.
2. Explicit per-source rationale for each carrier, traceable to the frozen §5 rubric.
3. Verification that the two pre-registered diagnostic possibilities (Z/14 Source 1 boundary, Z/22 Source 4 sensitivity) resolved cleanly under the rubric rather than being glossed over.
4. Cross-check with pilot prediction recorded transparently.

The result is not a documentation derivation. It is an executed rubric application producing per-carrier scores that, uniformly, cleared every pre-registered threshold.

Verdict follows in `PPM_V20_MULTIPLICATIVE_VERDICT.md`.
