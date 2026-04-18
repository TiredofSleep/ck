# Path 3 Subtype Adjacency v1.2 — Pre-Registration
## L-Metric Bridge — Leaf-Edge Placement Transport

---

## Scope Declaration

**Path:** Bridge Test (Path 3)
**Attractor convention:** cross-path (Path 1: $h_\text{thm}=7$; Path 2: $h_\text{ext}$ under P3AP extension)
**Claim class:** bridge-level
**Canonical construction source:** Path 1 published TSML; Path 2 extended $C_0$ via P3AP algorithm
**Relation to prior sprints:**
- Operates on P3-BridgeA-Prime-v1.0's recovered seams as-is.
- Subtype labels from P3AP's overlay audit records.
- Successor to P3-Subtype-v1.0 (UNCLEAR) and v1.1 (PASS on identity-edge).
- Does NOT re-use v1.0's (MM, MA, AA) adjacency ratio metric (shape-entangled).
- Does NOT re-score v1.1's I metric (already on record at +6.06σ).
- Does NOT score M (structurally redundant on chain topology; may appear only diagnostically).
- Does NOT run count transport (closed under P3AP generator; see `WHY_COUNT_IS_NOT_LIVE_UNDER_P3AP.md`).
- Does NOT introduce a new generator family or hub-extension.

**Explicit bridging rule:** same object class on both paths (planted-recovery artifacts under same extractor). Metric is a single binary role attribute (L) designed to be topology-invariant across the chain-vs-hub asymmetry. Null is subtype-label scrambling on the same recovered graphs, preserving counts per carrier.

---

**Status:** FROZEN pending user approval of this version.
**Version:** P3-Subtype-v1.2-adj.
**Change policy:** once any datum is scored against this spec, the spec cannot be edited. Amendments require v1.2.1+ and a fresh run.

---

## 1. Hypothesis Under Test (Exactly One)

**Hypothesis (P3SAL-H).** Under the P3AP overlay-extension algorithm, recovered ADD-subtype edges on the Path 2 family {14, 22, 34, 42, 46, 58, 74, 94} consistently have at least one degree-1 endpoint (i.e., are leaf edges of the recovered seam graph) at a rate significantly exceeding the rate produced by subtype-label scrambling on the same recovered seam graphs.

This is a bridge-level claim at the role-attribute level. It is *not* a re-test of v1.1's identity-element attachment; it is a test of the prior structural attribute "the ADD edge is a leaf edge" that v1.1 implicitly presupposed.

---

## 2. Input Objects (Frozen)

### 2.1 Path 1 reference (for context only, not scored)

Z/10 ADD edge: $(1, 2)$. Endpoint degrees: 1 (vertex 1), 3 (vertex 2). $L = 1$.

This is a reference data point; Path 1 is not scored.

### 2.2 Path 2 inputs

Same 8 carriers as P3AP: $\{14, 22, 34, 42, 46, 58, 74, 94\}$. Recovered persistent seams from P3AP as-is. Per-carrier ADD edges inherited from P3AP's overlay audit: $(1, 2)$ on every carrier.

---

## 3. Primary Metric (Frozen)

### 3.1 L — Leaf-edge attribute

For each Path 2 carrier's recovered seam graph $G_n$ with labeling:
$L_n = 1$ iff the ADD-labeled edge in $G_n$ has at least one endpoint of degree 1 in $G_n$; else $L_n = 0$.

**Family metric:** $\mu_L = $ fraction of Path 2 carriers with $L_n = 1$.

### 3.2 M and I — Diagnostic only, NOT scored

$M_n$ (main-component attachment) and $I_n$ (identity attachment) are computed and reported per carrier for completeness and to preserve inheritance from v1.1. Neither contributes to pass/fail. $I$ values are reported with an explicit note that they are inherited from v1.1's +6.06σ result, not scored as new evidence in v1.2.

---

## 4. Null Model (Frozen)

**N1 — Subtype-label scrambling preserving counts per carrier.** Same null methodology as v1.1.

For each Path 2 carrier's recovered seam graph:
- Keep graph structure (vertices, edges) unchanged.
- Preserve MAX count and ADD count for that carrier (from overlay audit: 1 ADD, $|E|-1$ MAX).
- Randomly select 1 edge uniformly at random to receive the ADD label; remaining edges receive MAX.
- Compute $L_n$ on the null-labeled graph.

**100 null replicates per carrier.** Family null metric: $\mu_L^\text{null}$ computed per replicate, then mean and std across 100 replicates.

**Null seed:** $33{,}400$.

---

## 5. Pass / Fail Criteria (Frozen)

### 5.1 Primary

Sprint passes if BOTH of:

1. **$\mu_L \geq 0.75$** — at least 6 of 8 Path 2 carriers have ADD edges with at least one degree-1 endpoint.
2. **Null separation:** real $\mu_L$ exceeds null mean $\mu_L^\text{null}$ by $\geq 2\sigma$.

### 5.2 Fail triggers

Either primary threshold violated.

### 5.3 Unclear

$\mu_L \geq 0.75$ but null separation is between $1\sigma$ and $2\sigma$.

Ceiling real values with non-zero null std do NOT trigger UNCLEAR (lesson from S31-pilot-v2.0).

---

## 6. Anti-Tuning Rules

1. Carrier list (§2.2) frozen; inherited from P3AP.
2. P3AP overlay audit records are sole source of subtype labels.
3. P3AP recovered seams used as-is.
4. Metric $L$ is the sole scored metric.
5. $M$ and $I$ are diagnostic-only and cannot be promoted to scored status post-hoc.
6. Null N1 frozen.
7. Thresholds (§5) frozen.
8. If FAIL, no re-run with adjusted parameters; successor requires v1.2.1+.

---

## 7. Deliverables

Written to `/home/claude/path3_subtype_v12_adj/`:

- `P3SAL_LABELS_AND_ROLES.json` — per Path 2 carrier: recovered edges, subtype labels, ADD edge, endpoint degrees, computed $L/M/I$ values.
- `P3SAL_NULL_STATS.csv` — per (carrier, null replicate): which edge received ADD label, endpoint degrees, $L/M/I$.
- `P3SAL_SCORES.json` — family aggregate, null statistics, sigma separation, sub-conditions, verdict.
- `PATH3_SUBTYPE_ADJACENCY_V12_RESULTS.md` — per-carrier table, family aggregate, null comparison, inherited v1.1 context section.
- `PATH3_SUBTYPE_ADJACENCY_V12_VERDICT.md` — one-paragraph determination.
- `PATH3_SUBTYPE_ADJACENCY_V12_REPRO.md` — reproducibility notes.

---

## 8. Three-Way Outcome

**PASS.** Leaf-edge placement transports: ADD edges are consistently leaf edges across the Path 2 family, at significance exceeding label-scrambling null. Adds one narrow finding: the ADD edge's leaf-edge attribute is a transportable feature under the P3AP extension, independent of v1.1's identity-element finding.

**FAIL.** Leaf-edge placement is not distinguishable from label scrambling. v1.1's identity-element result stands unaffected. The v1.2 lane closes; whether leaf-edge placement is a meaningful feature cannot be established by this sprint under this null.

**UNCLEAR.** Primary threshold met but null separation marginal (1σ-2σ). Report and pause.

---

## 9. Scope Boundaries

**Tests:**
- Single binary question about Path 2 recovered seams.
- Whether the ADD edge has a degree-1 endpoint.
- Significance against subtype-label scrambling null on the same graphs.

**Does not test:**
- Identity-element attachment (v1.1 result; inherited, not re-scored).
- Main-component attachment (diagnostic only; structurally redundant on chain topology).
- Count transport (closed under P3AP generator).
- Raw adjacency ratios (v1.0 M3; shape-entangled, abandoned).
- Hub-and-spokes transport under a different extension.
- Any Path 1 theorem on non-Z/10 carriers.
- Physical, ontological, or real-world claims.

---

## 10. Integrity Check Against Comparison Law

- **Test 1 — path/convention coherence:** cross-path → bridge required → ✓ (Path 3 declared).
- **Test 2 — generator type commensurability:** same planted-recovery object class on both sides, same extractor → ✓.
- **Test 3 — metric-object match:** $L$ is a binary role attribute designed to be topology-invariant. It is meaningful on both hub (Path 1) and chain (Path 2) topologies without structural bias. ✓.

All three tests pass. Spec eligible for freezing.

---

## 11. Prediction (Not a Target)

From pilot inspection of P3AP data (documented in `CHAIN_AWARE_ADJACENCY_PRINCIPLES.md`): every Path 2 carrier has $L = 1$. Real $\mu_L$ will be 1.0. Expected null $\mu_L^\text{null}$ mean ≈ 0.375, corresponding to the theoretical probability $2/|E|$ averaged across carriers (chain graphs have 2 leaf edges out of $|E|$). Null std at 100 replicates: likely 0.10-0.15. Expected sigma separation: ~4-6σ.

Prediction does not modify thresholds. The sprint decides. A PASS at substantially less than 4σ would suggest the pilot computation was off; a PASS at substantially more than 6σ would suggest the null underestimates variance.

---

## 12. Integrity Statement

This spec is designed to isolate the single structural question that v1.1 did not test: whether the ADD edge has a leaf-edge placement at all. It does not re-score v1.1's identity finding. It does not bundle other metrics. It does not introduce a new generator. It does not use the v1.0 adjacency metric that was shape-entangled.

The null, the metric, and the object class have all been used successfully by prior sprints in this program. Nothing about v1.2-adj's methodology is new; what is new is isolating the one scope-appropriate question remaining to test.

---

## 13. Awaiting Approval

Three frozen choices for review:

1. Sole primary metric: $L$ (ADD edge has a degree-1 endpoint). Acceptable?
2. $M$ and $I$ reported diagnostically only, not scored. Acceptable?
3. Null: subtype-label scrambling (same as v1.1). Acceptable?
4. Thresholds: $\mu_L \geq 0.75$, null separation $\geq 2\sigma$. Acceptable?

If approved: freeze as P3-Subtype-v1.2-adj and execute.
If revised: note changes, refreeze under new version, then execute.
