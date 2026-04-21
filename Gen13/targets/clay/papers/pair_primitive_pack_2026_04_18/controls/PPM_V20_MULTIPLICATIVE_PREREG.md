# PPM-v2.0 — Multiplicative Operationalization Transport Pre-Registration
## Per-Carrier v1.0 Rubric Applied to 8 P3AP Path 2 Carriers

---

## Scope Declaration

**Path:** Bridge Test (Path 3).
**Attractor convention:** cross-path (Path 1: $h_\text{thm} = 7$; Path 2: $h_\text{ext}$ under P3AP extension).
**Claim class:** bridge-level transport claim at family level, conditional on multiplicative operationalization and the P3AP extension.
**Canonical construction source:** Path 1 published Z/10 TSML; Path 2 recovered seams from P3-BridgeA-Prime-v1.0.
**Relation to prior sprints:**
- Inherits rubric verbatim from PPM-v1.0 (multiplicative operationalization).
- Applies per-carrier; aggregates family-level by carrier count.
- Uses P3AP recovered seams as-is; does not regenerate.
- Does NOT re-score PPM-v1.0 (Z/10) or PPM-v1.1 (additive).
- Does NOT re-score any Path 3 sprint.
- Treats P3AP, v1.1, v1.2-adj as inherited context defining the data sources per carrier.

**Inherited wording clarification:** This sprint evaluates the pair-primitive framework under multiplicative operationalization only; the verdict refutes or confirms that operationalization's transport property, not the framework in all possible readings.

---

**Status:** DRAFT awaiting approval.
**Version:** PPM-v2.0 (multiplicative transport).
**Change policy:** once any carrier is scored, the spec cannot be edited. Revisions require v2.1+.

---

## 1. Hypothesis Under Test

**Hypothesis (PPM-v2.0-H).** Under the pair-primitive framework's multiplicative operationalization applied per carrier to the 8 P3AP Path 2 carriers, Map B (MAX = persistent, ADD = excluded) produces a coherent structural fit on at least 6 of 8 carriers at per-carrier cleanness gap ≥ 2. The v1.0 checkpoint transports under the P3AP extension at family level.

Null: fewer than 6 carriers support Map B at per-carrier cleanness, or carriers split among Map B / Map A / indecisive without reaching the threshold.

---

## 2. Candidate Mappings (Inherited from v1.0)

- **Map A:** ADD = persistent-side, MAX = excluded-side.
- **Map B:** MAX = persistent-side, ADD = excluded-side.

---

## 3. Operational Interpretation — Multiplicative, Carrier-Adapted (FROZEN)

**Core interpretation (inherited from v1.0 §3):** Persistent-side = structural backbone under multiplicative operation structure. Excluded-side = localized departure from multiplicative structure.

**Carrier-adapted reading (added for v2.0):** Under the P3AP extension, each Path 2 carrier's seam has a doubling-chain-dominated MAX substructure rather than Z/10's hub-and-spokes. The carrier-adapted reading is **the same multiplicative reading applied to valid chain-topology object shapes** — not a new rubric. Specifically:

- On Z/10, the multiplicative backbone is the doubling chain 2→4→8 plus the attractor-involution edge 2–9.
- On a Path 2 carrier Z/n, the multiplicative backbone is the doubling chain 2→4→8→16→... (up to the carrier-specific termination) plus any attractor-involution edges that survive the P3AP audit.
- In both cases, the backbone is a connected multiplicative-flow substructure of the seam graph.

The shape differs (hub on Z/10 vs chain on Path 2) but the category does not: both are connected multiplicative-flow substructures.

---

## 4. Data Sources Per Carrier (Frozen From P3AP Audit)

Inspected from P3AP overlay audit records:

| $n$ | $h_\text{ext}$ | Total edges | MAX edges (unordered) | ADD edges (unordered) | ADD edge | $\deg_\text{seam}(1)$ |
|---:|---:|---:|---|---|---|---:|
| 14 | 13 | 3 | (2,4), (4,8) | (1,2) | (1,2) | 1 |
| 22 | 21 | 6 | (2,4), (4,8), (8,16), (10,16), (10,20) | (1,2) | (1,2) | 1 |
| 34 | 33 | 6 | (2,4), (4,8), (8,16), (16,32), (30,32) | (1,2) | (1,2) | 1 |
| 42 | 41 | 6 | (2,4), (4,8), (8,16), (16,32), (22,32) | (1,2) | (1,2) | 1 |
| 46 | 45 | 6 | (2,4), (4,8), (8,16), (16,32), (18,32) | (1,2) | (1,2) | 1 |
| 58 | 57 | 6 | (2,4), (4,8), (6,32), (8,16), (16,32) | (1,2) | (1,2) | 1 |
| 74 | 73 | 6 | (2,4), (4,8), (8,16), (16,32), (32,64) | (1,2) | (1,2) | 1 |
| 94 | 93 | 6 | (2,4), (4,8), (8,16), (16,32), (32,64) | (1,2) | (1,2) | 1 |

Universal properties confirmed from the audit:
- Every carrier has $|E_\text{ADD}| = 1$ (the identity edge).
- Every carrier has ADD edge = (1,2).
- Every carrier has vertex 1 with degree 1 in the seam graph.
- Every carrier's MAX subgraph contains the doubling chain 2→4→8 (minimum); most extend further.
- Every carrier's MAX subgraph is connected.
- Z/14 has $|E_\text{MAX}| = 2$ (attractor-involution audit-removed); other carriers have $|E_\text{MAX}| = 5$.

---

## 5. Scoring Rubric (Inherited From v1.0 §5, Carrier-Adapted)

Applied per carrier. Each source scores in $\{-1, 0, +1\}$ per v1.0 criteria. Carrier-adapted reading specified where the carrier's structure differs from Z/10.

### Source 1 — Structural backbone (carrier-adapted)

**Question:** Does the map's persistent-side subtype form the multiplicative backbone on this carrier?

**Carrier-adapted backbone criterion:** majority (≥50%) of seam edges AND connected multiplicative-flow substructure containing the carrier's doubling chain starting from vertex 2.

**Scoring (applies per carrier):**
- +1 if persistent-side forms the backbone on this carrier.
- −1 if persistent-side does NOT form the backbone (excluded-side does).
- 0 if neither subtype clearly dominates.

### Source 2 — Identity-edge reading (inherited verbatim)

**Question:** On this carrier, does the map's reading of "ADD at vertex 1" cohere with §3?

**Key criterion (unchanged from v1.0 §5.2):** vertex 1 is the multiplicative identity on every Z/n. Identity is a multiplicative-trivialization point. ADD surfacing at identity = excluded content surfacing at multiplicative-absence.

**Scoring:** +1 if map's reading coheres with §3; −1 if it contradicts; 0 if ambiguous.

### Source 3 — Leaf-edge placement (inherited verbatim)

**Question:** On this carrier, does the map's excluded-side sit at the graph boundary?

**Scoring:** +1 if excluded-side at leaf; −1 if persistent-side at leaf; 0 otherwise.

### Source 4 — Topology-feature dominance (inherited verbatim)

**Question:** On this carrier, does the map's persistent-side carry the majority of topology features?

**Scoring:** +1 if persistent-side carries majority; −1 if excluded-side carries majority; 0 if equal.

---

## 6. Per-Carrier Verdict Rule

For each of the 8 carriers, compute Map A aggregate and Map B aggregate (each in $[-4, +4]$), plus per-carrier cleanness gap.

Per-carrier classification:

- **Supports Map B** if Map B ≥ +3 AND Map A ≤ +1 AND gap ≥ 2.
- **Supports Map A** if Map A ≥ +3 AND Map B ≤ +1 AND gap ≥ 2.
- **Indecisive** otherwise.

The per-carrier criteria are exactly v1.0's PASS criteria applied on that carrier's data.

---

## 7. Family Aggregation (Primary)

Count the number of carriers supporting Map B ($N_B$), Map A ($N_A$), and indecisive ($N_I$). $N_B + N_A + N_I = 8$.

**Primary family metric:** $N_B$.

**PASS threshold:** $N_B \geq 6$ of 8 carriers.

This is parallel to the 0.75 family threshold used in P3-Subtype-v1.1 and v1.2-adj (≥6/8).

---

## 8. Family Aggregation (Secondary, Not Scored)

**Secondary summary:** mean per-carrier cleanness gap (across all 8 carriers, including indecisive ones) and mean per-carrier cleanness gap across carriers supporting Map B.

This is reported for transparency but does NOT contribute to the family-level verdict. Primary metric is carrier count.

---

## 9. Pass / Fail / Unclear Criteria (Frozen)

### 9.1 PASS (Transport)

$N_B \geq 6$.

### 9.2 FAIL (Transport)

$N_B < 6$. Sub-pattern named in verdict:
- **Uniform FAIL:** $N_B = 0$ or $1$ (Map B holds on no or nearly no carriers).
- **Split FAIL:** $N_B < 6$ but $N_A > 0$ (carriers divide between maps).
- **Below-threshold FAIL:** $N_B < 6$, $N_A = 0$, $N_I > 0$ (carriers lean Map B but don't clear per-carrier thresholds, parallel to v1.1's Z/10 situation).

### 9.3 UNCLEAR

Reserved for boundary cases not cleanly fitting PASS/FAIL. Specifically: $N_B = 5$ with $N_I = 3$, or any configuration where the carrier count is exactly at or just below threshold with no clear majority pattern.

---

## 10. Verdict Sentences (Frozen)

| Outcome | Sentence |
|---|---|
| PASS | Under the pair-primitive framework's multiplicative operationalization applied per carrier to 8 P3AP Path 2 carriers, Map B (MAX = persistent, ADD = excluded) produces a coherent structural fit on $N_B$ of 8 carriers ($N_B \geq 6$) at per-carrier cleanness gap ≥ 2. The v1.0 checkpoint transports under the P3AP extension at family level. |
| FAIL | Under the same framework and rubric, Map B produces a coherent structural fit on only $N_B$ of 8 carriers ($N_B < 6$). The v1.0 checkpoint is Z/10-specific under P3AP; sub-pattern (uniform/split/below-threshold) is documented per §9.2. |
| UNCLEAR | Under the same framework and rubric, carrier-level support for Map B is at the threshold boundary ($N_B = 5$ with indecisive configuration). The transport is not decidable at pre-registered cleanness; per-carrier pattern is the diagnostic finding. |

---

## 11. Anti-Tuning Rules (Inherited From v1.0 §8)

1. Rubric in §5 frozen; carrier-adapted reading in §3 frozen.
2. P3AP audit records are sole source of per-carrier seam data.
3. No per-carrier threshold adjustment post-hoc.
4. Family threshold $N_B \geq 6$ frozen.
5. Secondary summary is reported but cannot be promoted to scoring post-hoc.
6. Scoring proceeds carrier-by-carrier; scorer does NOT see family progress before all 8 carriers are scored.
7. If FAIL, no re-run with adjusted rubric; successor requires v2.1+.

---

## 12. Honest Prediction (Narrow, Per User Specification)

Pilot inspection of P3AP audit data (§4) shows uniform structure across the 8 carriers:

### Strong carriers expected

All 8 carriers have:
- ADD edge = (1,2), vertex 1 = multiplicative identity.
- Vertex 1 has degree 1 (ADD is at leaf on every carrier).
- MAX majority (5/6 on seven carriers; 2/3 on Z/14).
- MAX connected, contains doubling chain starting from vertex 2.

Under verbatim inheritance of v1.0 rubric with carrier-adapted reading for Source 1, every rubric criterion is met the same way on each carrier. Predicted per-carrier score: Map A = −4, Map B = +4, cleanness gap = 8.

### Ambiguous carriers expected

None identified from the P3AP audit data. The 8 carriers are structurally uniform under the relevant rubric criteria.

### Likely-indecisive carriers expected

None identified.

### Predicted family verdict

$N_B = 8$, $N_A = 0$, $N_I = 0$. **Predicted PASS** at threshold $N_B \geq 6$.

### Honesty note

The prediction is uniform across carriers because the P3AP extension produces structurally similar seams on every carrier by design (same overlay rules, audit preserves the identity edge, doubling chain is universal). The sprint's value is confirming uniform prediction against actual rubric application — a real test rather than a documentation claim. Any carrier scoring differently than predicted would be the diagnostic finding.

### Diagnostic possibilities not ruled out by the pilot

1. Per-carrier application may reveal that one or more carriers' Source 4 topology features score differently if the forest-spine attribution is sensitive to extension-edge details (e.g., the (10,16)+(10,20) pair on Z/22 vs the simpler chain on Z/74).
2. Source 1 on Z/14 is the closest to a boundary case because $|E_\text{MAX}| = 2$ and the attractor-involution is missing; the criterion "contains doubling chain" still holds but the backbone is minimal.

These are mentioned for transparency, not as threshold adjustments.

Prediction does not modify thresholds. The rubric decides.

---

## 13. Scope Boundaries

**Tests:** whether Map B transports at family level across the 8 P3AP carriers under multiplicative operationalization and the P3AP extension.

**Does NOT test:**
- Additive operationalization on Path 2 (separate sprint).
- Carriers outside the 8 P3AP carrier family.
- Hub-extension (still deferred).
- Any new generator.
- Upgrade of prior Path 3 sprints.
- Scale examples, physics, ontology.
- v1.0 Z/10 result (stands unchanged).
- v1.1 additive FAIL (stands unchanged).

---

## 14. Integrity Check Against Comparison Law

- **Test 1 — path/convention coherence:** Path 3 bridge test with cross-path convention declared (Path 1 $h_\text{thm}=7$, Path 2 $h_\text{ext}$). ✓
- **Test 2 — generator type commensurability:** all per-carrier data comes from the same P3AP extension (planted-recovery artifacts). Within-sprint commensurability holds. ✓
- **Test 3 — metric-object match:** inherited v1.0 rubric applied per carrier; carrier-adapted reading for Source 1 preserves the criterion on valid chain-topology objects. ✓

---

## 15. Deliverables (Post-Execution, If Approved)

Written to `/home/claude/foundation_sprint/ppm_v20/`:

- `PPM_V20_PER_CARRIER_SCORES.json` — per-carrier (Map A agg, Map B agg, gap, verdict classification).
- `PPM_V20_MULTIPLICATIVE_RESULTS.md` — per-carrier table, family aggregation, sub-pattern diagnosis if FAIL.
- `PPM_V20_MULTIPLICATIVE_VERDICT.md` — one-paragraph determination per §10 table.
- `PPM_V20_MULTIPLICATIVE_REPRO.md` — reproducibility notes.

---

## 16. Awaiting Approval

Frozen choices for review:

1. **Operational interpretation** — multiplicative inherited from v1.0, with carrier-adapted reading for Source 1 (same reading, translated to chain-topology objects). Acceptable?
2. **Per-carrier data sources** — §4 table, directly from P3AP audit records. Acceptable?
3. **Rubric** — v1.0 §5 inherited verbatim for Sources 2, 3, 4; Source 1 with carrier-adapted backbone criterion. Acceptable?
4. **Per-carrier verdict rule** — v1.0 thresholds applied per carrier (winner ≥+3, loser ≤+1, gap ≥2). Acceptable?
5. **Family threshold** — $N_B \geq 6$ of 8. Acceptable?
6. **Three-way per-carrier classification** — supports B / supports A / indecisive. Acceptable?
7. **FAIL sub-patterns** (§9.2) — uniform / split / below-threshold. Acceptable?

If approved: freeze as PPM-v2.0 and execute carrier-by-carrier scoring.
If revised: note changes, re-freeze under new version, then execute.
