# PPM-v2.1 — Additive Operationalization Transport Pre-Registration
## Per-Carrier v1.1 Rubric Applied to 8 P3AP Path 2 Carriers

---

## Scope Declaration

**Path:** Bridge Test (Path 3).
**Attractor convention:** cross-path (Path 1: $h_\text{thm} = 7$; Path 2: $h_\text{ext}$ under P3AP extension).
**Claim class:** bridge-level transport claim at family level, conditional on **additive** operationalization and the P3AP extension.
**Canonical construction source:** Path 1 published Z/10 TSML (inherited context); Path 2 recovered seams from P3-BridgeA-Prime-v1.0.
**Relation to prior sprints:**
- Inherits rubric verbatim from PPM-v1.1 (additive operationalization).
- Applies per-carrier; aggregates family-level by carrier count. Structure parallel to PPM-v2.0.
- Uses P3AP recovered seams as-is; does not regenerate.
- Does NOT re-score PPM-v1.0, v1.1, or v2.0.
- Does NOT re-score any Path 3 sprint.
- Treats P3AP, v1.1, v1.2-adj as inherited context defining the data sources per carrier.

**Inherited wording clarification (Rule 18):** This sprint evaluates the pair-primitive framework under **additive** operationalization only; the verdict refutes or confirms that operationalization's transport property, not the framework in all possible readings.

---

**Status:** DRAFT awaiting approval.
**Version:** PPM-v2.1 (additive transport).
**Change policy:** once any carrier is scored, the spec cannot be edited. Revisions require v2.1.1+.

---

## 1. Hypothesis Under Test

**Hypothesis (PPM-v2.1-H).** Under the pair-primitive framework's additive operationalization applied per carrier to the 8 P3AP Path 2 carriers, either Map A (ADD = persistent, MAX = excluded) or Map B (MAX = persistent, ADD = excluded) produces a coherent structural fit on at least 6 of 8 carriers at per-carrier cleanness gap ≥ 2.

**Null:** fewer than 6 carriers support either map at per-carrier cleanness; carriers either split among A / B / indecisive or uniformly fall below the per-carrier winner threshold.

---

## 2. Candidate Mappings (Inherited from v1.0/v1.1)

- **Map A:** ADD = persistent-side, MAX = excluded-side.
- **Map B:** MAX = persistent-side, ADD = excluded-side.

---

## 3. Operational Interpretation — Additive, Carrier-Adapted (FROZEN)

**Core interpretation (inherited from v1.1 §3):** Persistent-side = structural backbone under additive operation structure, connected substructure aligning with additive flow (cyclic addition mod n, additive-flow elements). Excluded-side = localized departure from additive operation structure, imports a non-additive rule, surfaces at boundary positions relative to additive structure.

**Carrier-adapted reading (added for v2.1):** Under the P3AP extension, each Path 2 carrier's seam has a doubling-chain-dominated MAX substructure. The carrier-adapted reading is **the same additive reading applied to valid chain-topology object shapes** — not a new rubric, parallel to Rule 20's discipline established in PPM-v2.0.

**Key structural facts under additive reading on Path 2 carriers:**
- The additive identity on every Z/n is **0**, not 1. Vertex 0 is in V0 boundary, outside the seam graph, on every carrier.
- Vertex 1 is the additive generator of Z/n on every carrier (generates cyclic group under addition).
- The ADD rule $T(x,y) = (x+y) \bmod n$ is the native additive operation on every carrier.
- The MAX rule $T(x,y) = \max(x,y)$ is order-based, does not align with additive structure, on every carrier.

---

## 4. Data Sources Per Carrier (Frozen From P3AP Audit)

Inspected from P3AP overlay audit. Same underlying data as PPM-v2.0 §4; additive-rubric-relevant facts highlighted:

| $n$ | MAX edges | ADD edges | ADD at vertex 0? | ADD at vertex 1? |
|---:|---:|---:|:---:|:---:|
| 14 | 2 (67%) | 1 (33%) | No | **Yes** |
| 22 | 5 (83%) | 1 (17%) | No | **Yes** |
| 34 | 5 (83%) | 1 (17%) | No | **Yes** |
| 42 | 5 (83%) | 1 (17%) | No | **Yes** |
| 46 | 5 (83%) | 1 (17%) | No | **Yes** |
| 58 | 5 (83%) | 1 (17%) | No | **Yes** |
| 74 | 5 (83%) | 1 (17%) | No | **Yes** |
| 94 | 5 (83%) | 1 (17%) | No | **Yes** |

**Universal properties relevant to additive rubric:**
- Every carrier: ADD edge = (1,2). ADD does NOT touch vertex 0 (additive identity); ADD DOES touch vertex 1 (additive generator).
- Every carrier: ADD rule is native additive operation (minority of edges).
- Every carrier: MAX rule is non-additive (majority of edges).
- Every carrier: MAX subgraph connected.
- Every carrier: vertex 1 has degree 1 in seam graph (leaf).

These facts exactly replicate Z/10's situation under additive reading (v1.1 §4).

---

## 5. Scoring Rubric (Inherited From v1.1 §5, Carrier-Adapted)

Applied per carrier. Each source scores in $\{-1, 0, +1\}$ per v1.1 criteria.

### Source 1 — Structural backbone under additive reading (carrier-adapted)

**Question:** Does the map's persistent-side subtype form the additive backbone on this carrier?

**Additive backbone criterion (§3-consistent, inherited verbatim from v1.1 §5.1):** the connected subgraph carrying the majority (≥ 50%) of the seam's edges AND containing the ring's additive-flow elements (cells where the additive rule produces the table value, edges within the additive cyclic structure).

**Strict AND criterion:** both conditions required.

**Scoring per carrier:**
- +1 if persistent-side forms the additive backbone.
- −1 if persistent-side does NOT (excluded-side does).
- 0 if neither subtype meets both conditions.

### Source 2 — Identity-edge reading under additive reading (inherited verbatim)

**Question:** Under §3 (additive operationalization), does the map's reading of "ADD at vertex 1" cohere on this carrier?

**Key criterion (v1.1 §5.2):** Vertex 1 is **not** the additive identity on any Z/n. The additive identity is 0, located in V0 boundary outside the seam. The v1.0 key argument — "identity is a multiplicative-absence point where excluded content must surface" — depends on a structural role (multiplicative trivialization) that does not translate to vertex 1 under additive reading.

**Scoring:** 0 when original finding's structural anchor has no clean additive parallel; non-zero only when a clear structural parallel exists.

**No substitute argument permitted:** per v1.1 §5.2's explicit stance, introducing a new structural argument (e.g., "ADD at additive-generator = persistent at flow origin") is not a rubric translation but a different rubric requiring its own pre-registration.

### Source 3 — Leaf-edge placement (topology-neutral, inherited verbatim)

**Question:** On this carrier, does the map's excluded-side sit at the graph boundary?

**Scoring (topology-neutral, same as v1.0 §5.3 and v2.0 §5.3):** +1 if excluded-side at leaf; −1 if persistent-side at leaf; 0 otherwise.

### Source 4 — Topology-feature dominance (topology-neutral, inherited verbatim)

**Question:** On this carrier, does the map's persistent-side carry the majority of topology features?

**Scoring (topology-neutral, same as v1.0 §5.4 and v2.0 §5.4):** +1 if persistent-side carries majority (≥50% edges + connected subgraph); −1 if excluded-side carries majority; 0 if equal.

---

## 6. Per-Carrier Verdict Rule (Inherited from v2.0 §6)

For each of the 8 carriers, compute Map A aggregate and Map B aggregate (each in $[-4, +4]$), plus per-carrier cleanness gap.

**Per-carrier classification:**
- **Supports Map B** if Map B ≥ +3 AND Map A ≤ +1 AND gap ≥ 2.
- **Supports Map A** if Map A ≥ +3 AND Map B ≤ +1 AND gap ≥ 2.
- **Indecisive** otherwise.

---

## 7. Family Aggregation (Primary)

Count carriers supporting Map B ($N_B$), Map A ($N_A$), and indecisive ($N_I$). $N_B + N_A + N_I = 8$.

**Primary family metrics:** $N_B$ and $N_A$.

**PASS threshold (inherited from v2.0 §7):**
- **PASS-B:** $N_B \geq 6$.
- **PASS-A:** $N_A \geq 6$.
- Symmetric threshold reflects that under additive reading, either mapping could in principle win — unlike v2.0 where Map B was the only hypothesis of interest given v1.0's PASS.

---

## 8. Family Aggregation (Secondary, Not Scored)

**Secondary summary:** mean per-carrier cleanness gap across all 8 carriers, plus per-carrier score breakdown. Reported for transparency but does NOT contribute to the family-level verdict.

---

## 9. Pass / Fail / Unclear Criteria (Frozen, Following v2.0 §9)

### 9.1 PASS

$N_B \geq 6$ OR $N_A \geq 6$. Named as PASS-B or PASS-A respectively.

### 9.2 FAIL

Neither $N_B$ nor $N_A$ reaches 6. Sub-pattern named in verdict:
- **Uniform FAIL:** $N_B = N_A = 0$ (no carrier supports either map).
- **Split FAIL:** $N_B > 0$ AND $N_A > 0$, neither reaching 6.
- **Below-threshold FAIL:** one of $N_B, N_A > 0$ but below 6, other = 0, $N_I > 0$.

### 9.3 UNCLEAR

Boundary configuration: $N_B = 5$ with $N_A = 0$ and $N_I = 3$ (or symmetric), where the carrier count is exactly at or just below threshold without a clear family pattern.

---

## 10. Verdict Sentences (Frozen)

| Outcome | Sentence |
|---|---|
| PASS-B | Under the pair-primitive framework's additive operationalization applied per carrier to 8 P3AP Path 2 carriers, Map B produces a coherent structural fit on $N_B$ of 8 carriers ($N_B \geq 6$) at per-carrier cleanness gap ≥ 2. |
| PASS-A | Under the same framework and rubric, Map A produces a coherent structural fit on $N_A$ of 8 carriers ($N_A \geq 6$) at per-carrier cleanness gap ≥ 2. |
| FAIL | Under the same framework and rubric, neither map reaches the pre-registered family-level transport threshold. Sub-pattern (uniform / split / below-threshold) is documented per §9.2. The additive operationalization does not cash out decisively at family level on the tested carriers. |
| UNCLEAR | Under the same framework and rubric, carrier-level support is at the threshold boundary. Per-carrier pattern is the diagnostic finding. |

---

## 11. Anti-Tuning Rules (Inherited)

1. Rubric in §5 frozen; carrier-adapted reading in §3 frozen.
2. P3AP audit records are sole source of per-carrier seam data.
3. No per-carrier threshold adjustment post-hoc.
4. Family threshold $N_B \geq 6$ OR $N_A \geq 6$ frozen.
5. Secondary summary reported but cannot be promoted to scoring post-hoc.
6. Scoring proceeds carrier-by-carrier; scorer does NOT see family progress before all 8 carriers are scored.
7. If FAIL, no re-run with adjusted rubric; successor requires v2.1.1+.

---

## 12. Honest Prediction (Narrow, Per Rule 21)

Pilot inspection of P3AP audit data (§4) shows **structural uniformity across the 8 carriers identical to Z/10's additive-reading situation** (v1.1's §4).

### Predicted per-source scoring on every carrier

**Source 1 (strict AND criterion):**
- ADD: native-additive ✓, minority (17-33%) ✗. Not backbone.
- MAX: majority (67-83%) ✓, non-additive ✗. Not backbone.
- **Predicted: 0/0 on every carrier.** No additive backbone under strict AND, parallel to v1.1's Z/10 result.

**Source 2 (additive identity reading):**
- Vertex 1 is additive generator on every carrier, not additive identity.
- v1.0's multiplicative-trivialization argument has no additive parallel.
- **Predicted: 0/0 on every carrier.** Parallel to v1.1's Z/10 result.

**Source 3 (leaf-edge, topology-neutral):**
- ADD at vertex 1 (degree 1) on every carrier.
- **Predicted: Map A −1, Map B +1 on every carrier.** Parallel to v2.0's Source 3 per-carrier result.

**Source 4 (topology-family, topology-neutral):**
- MAX carries majority of edges on every carrier.
- **Predicted: Map A −1, Map B +1 on every carrier.** Parallel to v2.0's Source 4 per-carrier result.

### Predicted per-carrier aggregate

**Map A = −2, Map B = +2, cleanness gap = 4 on every carrier.**

Per §6 per-carrier classification:
- Map B (+2) does NOT meet ≥+3 winner threshold.
- Map A (−2) does NOT meet ≥+3 winner threshold.
- **Per-carrier verdict: INDECISIVE on every carrier.**

### Predicted family verdict

- $N_B = 0$, $N_A = 0$, $N_I = 8$.
- Per §9.2, this is a **Below-threshold FAIL** (specifically: uniform indecisive pattern).
- **Predicted verdict: FAIL.**

### Diagnostic possibilities (Rule 21 disclosure)

Specific cases where the uniform prediction might break:

1. **Z/14 Source 4 sensitivity:** with $|E_\text{MAX}| = 2$ (audit-removed attractor-involution), MAX majority is still 67% but closer to boundary. The connected-subgraph check is still met (MAX is connected). No expected deviation.

2. **Substitute argument for Source 2:** a scorer could in principle argue that "ADD at additive generator = excluded at flow origin" introduces a coherent reading for Map B. The pre-reg explicitly prohibits this per §5.2. Any scorer adopting the substitute argument would be deviating from the frozen rubric.

3. **Relaxed Source 1 criterion:** a scorer could relax the strict AND to "majority OR native-alignment." This would give ADD as backbone on every carrier (native-additive alignment alone). Relaxed-criterion scoring would be a different rubric and a different sprint; explicitly prohibited here.

### Expected value of running this sprint

Per the scope note (`open_questions/PPM_V21_ADDITIVE_TRANSPORT_FIRST_OPEN_CHECKPOINT.md`): the sprint's value is **diagnostic symmetry with v2.0**, not major new ground. The pilot prediction closely matches the v1.1 Z/10 result transported across the carrier family.

What the sprint earns if the prediction holds:
1. The uniform indecisive pattern is verified per-carrier, not assumed from the carrier structural uniformity.
2. The additive operationalization's non-discrimination becomes a **carrier-family property**, not a Z/10-specific property — a specific finding with attributed cause (seam's multiplicative loading transports to the family).
3. Completes the 2×2 design space (local/transport × multiplicative/additive) with four specific sentences.
4. Any carrier scoring differently than predicted would be the diagnostic finding worth isolating.

Prediction does not modify thresholds. The rubric decides.

---

## 13. Scope Boundaries

**Tests:** whether either map transports at family level across the 8 P3AP carriers under additive operationalization and the P3AP extension.

**Does NOT test:**
- Multiplicative operationalization on Path 2 (already tested by PPM-v2.0).
- Carriers outside the 8 P3AP carrier family.
- Alternative additive rubrics with relaxed criteria (would be v2.1.1 or later).
- Hub-extension (still deferred).
- Any new generator.
- SAH or any shape-admissibility claim.
- Upgrade of prior Path 3 or PPM sprints.
- Scale examples, physics, ontology.
- v1.0, v1.1, v2.0 verdicts (all stand unchanged).

**Rule 19 reminder:** the v2.1 verdict is a separate sentence from v2.0. No composite claim merging multiplicative and additive transport results is authorized, regardless of v2.1's outcome.

---

## 14. Integrity Check Against Comparison Law

- **Test 1 — path/convention coherence:** Path 3 bridge test with cross-path convention declared (Path 1 $h_\text{thm}=7$, Path 2 $h_\text{ext}$). ✓
- **Test 2 — generator type commensurability:** all per-carrier data comes from the same P3AP extension. Within-sprint commensurability holds. ✓
- **Test 3 — metric-object match:** inherited v1.1 rubric applied per carrier; carrier-adapted reading for Source 1 preserves the criterion on valid chain-topology objects. ✓

---

## 15. Deliverables (Post-Execution, If Approved)

Written to `/home/claude/foundation_sprint/ppm_v21/`:

- `PPM_V21_PER_CARRIER_SCORES.json` — per-carrier scoring data.
- `PPM_V21_ADDITIVE_TRANSPORT_RESULTS.md` — per-carrier table, family aggregation, sub-pattern diagnosis.
- `PPM_V21_ADDITIVE_TRANSPORT_VERDICT.md` — one-paragraph determination per §10 table.
- `PPM_V21_ADDITIVE_TRANSPORT_REPRO.md` — reproducibility notes.
- `ppm_v21_score.py` — deterministic scoring script (adapted from `ppm_v20_score.py`).

---

## 16. Awaiting Approval

Frozen choices for review:

1. **Operational interpretation** — additive inherited from v1.1, carrier-adapted for Source 1 (same reading, translated to chain-topology objects, parallel to v2.0's discipline). Acceptable?
2. **Per-carrier data sources** — §4 table, directly from P3AP audit records. Acceptable?
3. **Rubric** — v1.1 §5 inherited verbatim for Sources 2, 3, 4; Source 1 with carrier-adapted backbone criterion under strict AND. Acceptable?
4. **Per-carrier verdict rule** — v1.0/v2.0 thresholds applied per carrier (winner ≥+3, loser ≤+1, gap ≥2). Acceptable?
5. **Family threshold** — $N_B \geq 6$ OR $N_A \geq 6$ (symmetric because additive reading is a priori open between the two maps). Acceptable?
6. **Three-way per-carrier classification** — supports B / supports A / indecisive. Acceptable?
7. **FAIL sub-patterns** (§9.2) — uniform / split / below-threshold. Acceptable?
8. **Prohibited substitutions** — no relaxation of Source 1's strict AND, no substitute argument for Source 2. Acceptable?

If approved: freeze as PPM-v2.1 and execute carrier-by-carrier scoring.
If revised: note changes, re-freeze under new version, then execute.
