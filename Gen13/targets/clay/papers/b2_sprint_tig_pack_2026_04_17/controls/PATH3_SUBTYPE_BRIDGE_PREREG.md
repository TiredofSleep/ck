# Path 3 Subtype Bridge — Pre-Registration
## Internal Seam Structure Across Paths

---

## Scope Declaration

**Path:** Bridge Test (Path 3)
**Attractor convention:** cross-path (Path 1: $h_\text{thm}=7$; Path 2: $h_\text{ext}=\max$ odd unit)
**Claim class:** bridge-level
**Canonical construction source:** Path 1 published Z/10 TSML; Path 2 extended $C_0$ family under doubling-chain + identity-edge + attractor-involution overlay (inherited from P3AP)
**Relation to prior sprints:**
- Inherits object class from P3-BridgeA-Prime-v1.0 (Path 3, PASS at topology-family level).
- Uses the exact recovered seams from P3AP (stored in `P3AP_PATH2_GRAPHS.json`), with per-edge subtype labels inferred from the overlay-extension algorithm's edge classification (from `P3AP_OVERLAY_AUDIT.json`).
- Does NOT regenerate data. Operates on frozen artifacts.
- Does NOT introduce a new overlay-extension rule.

**Explicit bridging rule:** both sides are planted-recovery artifacts; each edge is classified MAX-type or ADD-type based on which generator rule produced the planted cell it recovered. Subtype-structural metrics are computed on both sides and compared against a null that preserves the recovered graphs but scrambles subtype labels.

---

**Status:** FROZEN pending user approval.
**Version:** P3-Subtype-v1.0.
**Change policy:** once any datum is scored against this spec, the spec cannot be edited. Amendments require v1.1+ and a fresh run.

---

## 1. Hypothesis Under Test (Exactly One)

**Hypothesis (P3S-H).** Under the same overlay-extension algorithm that produced P3-BridgeA-Prime-v1.0's PASS (doubling-chain + identity-edge + attractor-involution), the MAX/ADD partition of planted-recovery seams transports across paths — not only at the level of per-edge labeling but also in terms of count proportions and role-based placement in the seam graph — at significance exceeding a subtype-relabeling null on the same recovered graphs.

This is a bridge-level claim. Strongest permitted PASS sentence is stated in `SUBTYPE_BRIDGE_SCOPE_LIMITS.md` §"What a PASS Would Prove."

---

## 2. Input Objects (Frozen)

### 2.1 Path 1 reference edges

The Z/10 theorem seam's unordered edges with subtype labels:

| Edge | Subtype | Source rule |
|---|---|---|
| (1, 2) | ADD | $(x+y) \bmod 10 = 3$ |
| (2, 4) | MAX | $\max(2, 4) = 4$ |
| (2, 9) | MAX | $\max(2, 9) = 9$ |
| (4, 8) | MAX | $\max(4, 8) = 8$ |

**Path 1 counts:** 3 MAX, 1 ADD. Proportion: 75.0% MAX, 25.0% ADD.

### 2.2 Path 2 reference edges

Same 8 carriers as P3AP: {14, 22, 34, 42, 46, 58, 74, 94}.

Recovered persistent seams from P3AP's outputs. Each unordered edge is labeled:
- **MAX** if the underlying ordered cell(s) came from the doubling-chain or attractor-involution component of the overlay (i.e., planted value = $\max(x, y)$).
- **ADD** if the underlying ordered cell(s) came from the identity-edge component (i.e., planted value = $(x+y) \bmod n$).

Per-carrier counts from read-only inspection of P3AP artifacts:

| $n$ | $\|E\|$ | MAX edges | ADD edges | MAX% |
|---:|---:|---:|---:|---:|
| 14 | 3 | 2 | 1 | 66.7 |
| 22 | 6 | 5 | 1 | 83.3 |
| 34 | 6 | 5 | 1 | 83.3 |
| 42 | 6 | 5 | 1 | 83.3 |
| 46 | 6 | 5 | 1 | 83.3 |
| 58 | 6 | 5 | 1 | 83.3 |
| 74 | 6 | 5 | 1 | 83.3 |
| 94 | 6 | 5 | 1 | 83.3 |

These counts are *observed* from inherited data; they are NOT targets for this sprint. The sprint asks whether these counts, placements, and adjacencies exceed a subtype-relabeling null at pre-registered thresholds.

---

## 3. Metrics (Frozen)

Four metrics, all primary. No diagnostic-only metrics in this sprint — if a metric is worth computing it is worth scoring.

### 3.1 M1 — Subtype count vector similarity

For each object, compute the pair $(f_\text{MAX}, f_\text{ADD})$ where $f_\text{MAX} = |E_\text{MAX}| / |E|$ and $f_\text{ADD} = |E_\text{ADD}| / |E|$.

**Path 1 reference:** $(0.75, 0.25)$.

**Per-carrier metric:** absolute difference between carrier's MAX-fraction and Path 1's:
$\Delta_n = |f_\text{MAX}(R_n) - 0.75|$.

**Family metric:** $\mu_\Delta = $ mean $\Delta_n$ across the 8 Path 2 carriers.

### 3.2 M2 — ADD placement by graph role

For each edge, identify the role of its vertices:
- **Leaf vertex:** degree 1 in the seam graph.
- **Internal vertex:** degree 2 (chain interior).
- **Hub vertex:** degree ≥ 3.
- **Attached-to-hub:** a leaf whose sole neighbor has degree ≥ 3.

Classify each edge by its role pair:
- **leaf-to-hub:** connects a leaf vertex to a hub vertex.
- **leaf-to-internal:** connects a leaf vertex to an internal vertex.
- **internal-to-internal:** chain-interior edge.
- **internal-to-hub:** connects an internal vertex to a hub.
- **hub-to-hub:** both endpoints degree ≥ 3.

**Path 1 reference:** ADD edge (1, 2) is leaf-to-hub (vertex 1 has degree 1; vertex 2 has degree 3).

**Per-carrier metric:** for each carrier, for each of the carrier's ADD edges, classify its role pair. Compute the fraction of ADD edges whose role pair matches Path 1's (leaf-to-hub OR leaf-to-internal if the chain has no hub, i.e., when $d_\max = 2$).

**Adapted matching rule for chain-topology carriers:** P3AP showed that Path 2 carriers produce chains (no hub, $d_\max = 2$). For these carriers, "leaf-to-hub" collapses to "leaf-to-internal" (attaching an outside vertex to the chain-start vertex). The match rule therefore is: **ADD edge attaches a degree-1 external vertex to a vertex of the main connected component.** This is the Path 1 structural feature tested for transport to chain topology.

**Convention disclosure (per user caution).** The adapted role-matching rule is a *bridge convention* required by the shape mismatch between Path 1 (hub) and Path 2 (chain) observed in P3AP. It is not an independently established structural law. Specifically:

- It is a comparison device chosen so that the Path 1 ADD-edge role has a well-defined Path 2 analog despite the coarse topology difference.
- It collapses "leaf-to-hub" and "leaf-to-internal" to a shared structural feature — a degree-1 external vertex connected to the main component — which is present on Path 1 (where the main component has a hub) and on Path 2 (where the main component is a chain).
- A PASS under this rule should not be read as "ADD edges occupy a universal structural position across all rings." It should be read as "ADD edges attach an external low-degree vertex to the main-component body, under the specified overlay-extension algorithm on the tested carrier family."
- If a future sprint produces Path 2 artifacts with different coarse topology (e.g., hub-structured under an alternative overlay rule), the adapted rule must be revisited, because its collapse was calibrated to the chain-vs-hub case. The rule is Path 3-specific and object-class-specific, not a general structural invariant.

With this scoping, the adapted rule is frozen for this sprint only.

**Family metric:** $\mu_\text{ADDrole} = $ fraction of Path 2 carriers where the ADD edge matches this role pattern.

### 3.3 M3 — Subtype adjacency

For each pair of edges sharing a vertex, classify the adjacency:
- **MAX-MAX:** both edges are MAX.
- **MAX-ADD:** one MAX, one ADD.
- **ADD-ADD:** both ADD.

**Path 1 reference:** vertex 2 is incident to (1,2)=ADD, (2,4)=MAX, (2,9)=MAX. The adjacencies at vertex 2 are: MAX-MAX (from (2,4) ∩ (2,9)), MAX-ADD (from (2,4) ∩ (1,2)), MAX-ADD (from (2,9) ∩ (1,2)). Total: 1 MAX-MAX, 2 MAX-ADD, 0 ADD-ADD. Similarly, vertex 4 has adjacency (2,4)-(4,8) = MAX-MAX. Summing across all vertices and counting each adjacency once: 2 MAX-MAX, 2 MAX-ADD, 0 ADD-ADD. Normalized: 50% MAX-MAX, 50% MAX-ADD, 0% ADD-ADD.

**Per-carrier metric:** compute the (MAX-MAX, MAX-ADD, ADD-ADD) proportion for each carrier's recovered seam. Compute Bhattacharyya-style similarity to Path 1's proportion vector: $\text{sim}(v_1, v_2) = \sum_i \sqrt{v_{1,i} \cdot v_{2,i}}$, ranging from 0 (disjoint) to 1 (identical).

**Family metric:** $\mu_\text{adj} = $ mean similarity across the 8 Path 2 carriers.

### 3.4 M4 — Null separation

**Null model:** subtype-label scrambling. For each Path 2 carrier's recovered seam graph:
- Keep the graph structure unchanged (same vertices, same edges).
- Randomly relabel edges as MAX or ADD with probability matching the carrier's observed MAX:ADD ratio.
- Compute M1, M2, M3 on the null-labeled graph.

**100 null replicates per carrier.** Null aggregates: $\mu_\Delta^\text{null}, \mu_\text{ADDrole}^\text{null}, \mu_\text{adj}^\text{null}$ as mean and std across replicates.

**Null sigma separations:**
- $\mu_\Delta$ below null mean by $\geq 2\sigma$ (real should have smaller label-deviation than random).
- $\mu_\text{ADDrole}$ above null mean by $\geq 2\sigma$.
- $\mu_\text{adj}$ above null mean by $\geq 2\sigma$.

Null seed: $33{,}200$.

---

## 4. Pass / Fail Criteria (Frozen)

### 4.1 Primary pass

Sprint passes if ALL of:

1. **$\mu_\Delta \leq 0.10$** — mean absolute deviation from Path 1's 0.75 MAX-fraction is at most 0.10 (i.e., Path 2 carriers cluster between 65% and 85% MAX on average).
2. **$\mu_\text{ADDrole} \geq 0.75$** — at least 6 of 8 Path 2 carriers have their ADD edge(s) in the Path-1-matching role pattern.
3. **$\mu_\text{adj} \geq 0.80$** — mean Bhattacharyya similarity to Path 1's adjacency proportion ≥ 0.80.
4. **Null separation on $\mu_\Delta$:** real $\mu_\Delta$ below null mean by $\geq 2\sigma$.
5. **Null separation on $\mu_\text{ADDrole}$:** real $\mu_\text{ADDrole}$ above null mean by $\geq 2\sigma$.
6. **Null separation on $\mu_\text{adj}$:** real $\mu_\text{adj}$ above null mean by $\geq 2\sigma$.

### 4.2 Fail triggers

Any primary threshold violated, or any required null separation below 2σ.

### 4.3 Unclear

All primary thresholds met, but at least one null separation is between 1σ and 2σ. Uses the one-sided within-threshold rule from S31-pilot-v2.0's lesson (ceiling values do not trigger UNCLEAR).

### 4.4 Predicted result (not a target)

From the read-only P3AP inspection: $\mu_\Delta \approx 0.083$ (below threshold 0.10), and every carrier's ADD edge matches Path 1's role pattern (attaches vertex 1 to chain-start vertex 2). Null separations are uncertain without running the null. Prediction: PASS is likely. If it fails, the failure will be on null separation, not on the primary metric thresholds. Prediction does not modify any threshold.

---

## 5. Anti-Tuning Rules

1. Carrier list (§2) frozen at the P3AP-inherited set.
2. P3AP's recovered seams used as-is. No regeneration.
3. Subtype labels assigned strictly from P3AP's overlay audit records.
4. Metric definitions (§3) frozen.
5. Null model (§3.4) frozen.
6. Thresholds (§4) frozen.
7. No alternative metric or null substitution.
8. If FAIL, no re-run as v1.0 with adjusted parameters.

---

## 6. Deliverables

Written to `/home/claude/path3_subtype/`:

- `P3S_EDGE_LABELS.json` — per carrier: each edge with its subtype label, vertex roles, and the adjacency classification at each vertex.
- `P3S_NULL_STATS.csv` — per (carrier, null replicate): computed metrics.
- `P3S_SCORES.json` — family aggregates, null statistics, sigma separations, sub-conditions, verdict.
- `P3S_RESULTS.md` — per-carrier table with all metrics.
- `P3S_VERDICT.md` — one-paragraph determination.
- `P3S_REPRO.md` — reproducibility notes.

---

## 7. Three-Way Outcome

**PASS.** MAX/ADD vocabulary transports at count and placement levels under the specified extension algorithm. Permits subsequent sprints testing finer subtype structural features (exact hub recovery via different extension, shell-native rules, alternative role taxonomies).

**FAIL.** Subtype partition does not transport at the tested level. Depending on which sub-condition fails, diagnostics point to: (a) proportions not transporting, (b) role placement not transporting, (c) adjacency patterns random given labels. Close the subtype-bridge lane; next sprint could test alternative subtypologies (coarser or richer than MAX/ADD) or hub-extension as a separate question.

**UNCLEAR.** Counts/placement transport but null separation is marginal on one dimension. Report with flag, pause for judgment.

---

## 8. Scope Boundaries

**Tests:**
- MAX/ADD label count proportion preservation across paths.
- ADD-edge role placement preservation.
- Subtype adjacency pattern preservation.
- All three above at significance exceeding a label-scrambling null on the same graphs.

**Does not test:**
- Cell identity across carriers.
- Specific numerical values of edges.
- Whether MAX/ADD is the "right" partition (it is the partition the theorem uses).
- Hub-and-spokes recovery under a different extension algorithm.
- Any Path 1 theorem on non-Z/10 carriers.
- Any physical, ontological, or real-world claim.

---

## 9. Integrity Check Against Comparison Law

Per `COMPARISON_LAW.md`:

- **Test 1 — path/convention coherence:** different paths, bridge required → ✓ (Path 3 bridge declared).
- **Test 2 — generator type commensurability:** both sides are planted-recovery artifacts via same extractor and same extension → ✓.
- **Test 3 — metric-object match:** subtype labels are ✓ for small recovered seams (ref: `SPRINT_SELECTOR.md` §11 allows subtype-mix as a primary metric for Path 3 bridges with matched object types).

All three tests pass. Spec eligible for freezing.

---

## 10. Awaiting Approval

Six frozen choices for review:

1. Using P3AP's recovered seams as-is without regeneration. Acceptable?
2. Subtype labels inferred from overlay audit records. Acceptable?
3. Three metrics (M1 count deviation, M2 ADD role placement, M3 adjacency similarity) + null separations. Acceptable?
4. Adapted role-matching rule for chain topology (ADD edge attaches external vertex to main-component vertex). Acceptable?
5. Subtype-relabeling null (same graph, scrambled labels). Acceptable?
6. Thresholds: $\mu_\Delta \leq 0.10$, $\mu_\text{ADDrole} \geq 0.75$, $\mu_\text{adj} \geq 0.80$, 2σ null separation on all three. Acceptable?

If approved: freeze as P3-Subtype-v1.0 and execute.
If revised: note changes, refreeze under new version, then execute.
