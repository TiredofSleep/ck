# Path 3 Subtype v1.1 — Identity-Edge Bridge — Pre-Registration
## Narrow Successor to v1.0

---

## Scope Declaration

**Path:** Bridge Test (Path 3)
**Attractor convention:** cross-path (Path 1: $h_\text{thm}=7$; Path 2: $h_\text{ext}=\max$ odd unit under P3AP extension)
**Claim class:** bridge-level
**Canonical construction source:** Path 1 published TSML; Path 2 extended $C_0$ under doubling-chain + identity-edge + attractor-involution
**Relation to prior sprints:**
- Inherits object class from P3-BridgeA-Prime-v1.0 (Path 3 topology-family PASS).
- Operates on the exact recovered seams from P3AP (`P3AP_PATH2_GRAPHS.json`) and subtype labels from P3AP's overlay audit.
- Successor to P3-Subtype-v1.0 (Path 3, UNCLEAR), isolating that sprint's strongest surviving finding.
- Does NOT bundle count (M1) or adjacency (M3) metrics from v1.0; both methodologically inadequate.
- Does NOT regenerate data. No new extractor run.

**Explicit bridging rule:** both sides are planted-recovery artifacts under the P3AP extension. Each unordered edge is labeled MAX or ADD per the overlay audit. The sprint asks one binary question per carrier: does the ADD edge attach the ring's identity element (vertex 1)?

---

**Status:** FROZEN pending user approval.
**Version:** P3-Subtype-v1.1.
**Change policy:** once any datum is scored against this spec, the spec cannot be edited. Amendments require v1.2+ and a fresh run.

---

## 1. Hypothesis Under Test (Exactly One)

**Hypothesis (P3S11-H).** Under the P3AP overlay extension algorithm, recovered ADD-subtype edges on Path 2 carriers attach to the ring's multiplicative identity (vertex 1) at a rate significantly exceeding the rate produced by subtype-label scrambling on the same recovered seam graphs.

Strongest permitted PASS sentence: see `WHY_IDENTITY_EDGE_COMES_NEXT.md` §"What v1.1 Gains By Being Narrow."

---

## 2. Input Objects (Frozen)

### 2.1 Path 1 reference (for context only, not scored)

Z/10 ADD edge: $(1, 2)$. Touches vertex 1. This is a reference data point, not a scored Path 1 input — v1.1 asks about Path 2 transport only; Path 1 provides the hypothesis origin.

### 2.2 Path 2 inputs

Same 8 carriers as P3AP: $\{14, 22, 34, 42, 46, 58, 74, 94\}$.

Per-carrier ADD edges inherited from P3AP overlay audit:

- All 8 carriers have exactly one ADD edge after the pre-flight audit: $(1, 2)$.

This is observed data from the inherited artifacts. The sprint does NOT take this as a given for the test — it computes the identity-edge attachment metric from the recovered seams and compares it to a null on those same seams.

---

## 3. Metric (Frozen)

### 3.1 M4 — Identity-edge attachment (primary, sole)

For each Path 2 carrier $R_n$ with recovered persistent seam $S$:

- Let $L$ be the subtype labeling of $S$'s edges: each unordered edge labeled MAX or ADD per the overlay audit.
- **Per-carrier indicator:** $I_n(L) = 1$ if at least one ADD-labeled edge in $S$ is incident to vertex 1 (the multiplicative identity); else $I_n(L) = 0$.

**Family metric:** $\mu_\text{ID} = $ fraction of Path 2 carriers with $I_n(L) = 1$.

This is a strict subset of v1.0's M2 adapted rule. v1.0's rule accepted any external degree-1 vertex; v1.1's rule requires specifically vertex 1.

### 3.2 No secondary metrics

v1.1 does not include count, adjacency, role-pair classification, or hub-concentration metrics. Only the identity-edge indicator. This is a deliberate narrowing per `WHY_IDENTITY_EDGE_COMES_NEXT.md`.

---

## 4. Null Model (Frozen)

**N1 — Subtype-label scrambling** (same null as v1.0).

For each Path 2 carrier's recovered seam graph:
- Keep the graph structure (vertices, edges) unchanged.
- Preserve the MAX count and ADD count for that carrier.
- Randomly assign which edges are ADD (choosing $|E_\text{ADD}(R_n)|$ edges at uniform random without replacement to receive the ADD label; remaining edges receive MAX).
- Compute $I_n(L')$ on the null-labeled graph.

**100 null replicates per carrier.** Family null metric: $\mu_\text{ID}^\text{null} = $ mean fraction of carriers with $I_n(L') = 1$, across replicates.

**Null seed:** $33{,}300$.

---

## 5. Pass / Fail Criteria (Frozen)

### 5.1 Primary

Sprint passes if BOTH of:

1. **$\mu_\text{ID} \geq 0.75$** — at least 6 of 8 Path 2 carriers have the ADD edge attach vertex 1.
2. **Null separation:** real $\mu_\text{ID}$ exceeds null mean $\mu_\text{ID}^\text{null}$ by $\geq 2\sigma$.

### 5.2 Fail triggers

Either primary threshold violated.

### 5.3 Unclear

$\mu_\text{ID} \geq 0.75$ but null separation is between $1\sigma$ and $2\sigma$.

Ceiling values (1.0 on real, with non-zero null std) do NOT trigger UNCLEAR (lesson learned from S31-pilot-v2.0).

---

## 6. Anti-Tuning Rules

1. Carrier list (§2) frozen; inherited from P3AP.
2. P3AP overlay audit records are the sole source of subtype labels.
3. P3AP recovered seams used as-is.
4. Metric M4 is the sole scored metric.
5. Null N1 (subtype-label scrambling) is the sole null.
6. Thresholds (§5) frozen.
7. No other metrics, no diagnostic promotions to scored status.
8. If FAIL, no re-run with adjusted parameters. Successor requires v1.2+.

---

## 7. Deliverables

Written to `/home/claude/path3_subtype_v11/`:

- `P3S11_IDENTITY_ATTACHMENT.json` — per Path 2 carrier: ADD edge, endpoint vertices, identity-attachment indicator, vertex 1 degree in recovered seam.
- `P3S11_NULL_STATS.csv` — per (carrier, null replicate): which edge received ADD, identity-attachment indicator.
- `P3S11_SCORES.json` — family aggregate, null statistics, sigma separation, sub-conditions, verdict.
- `PATH3_SUBTYPE_V11_RESULTS.md` — per-carrier table, family aggregate, null comparison.
- `PATH3_SUBTYPE_V11_VERDICT.md` — one-paragraph determination.
- `PATH3_SUBTYPE_V11_REPRO.md` — reproducibility notes.

---

## 8. Three-Way Outcome

**PASS.** Identity-edge transport confirmed at pre-registered significance. Upgrades v1.0's role-placement finding from "any external low-degree vertex attachment" to "specifically the ring's identity element." Permits subsequent v1.2 sprints for the other v1.0 questions (count transport under different null; adjacency transport under chain-aware metric) as independent sprints.

**FAIL.** Identity-edge attachment not distinguishable from label scrambling. This would mean v1.0's $+3.80\sigma$ finding rested on graph-shape properties (any low-degree external vertex being labeled ADD) rather than on algebraic properties (the ring's identity element being the ADD-attached vertex). The role-placement result would downgrade.

**UNCLEAR.** Primary threshold met but null separation marginal. Report and pause.

---

## 9. Scope Boundaries

**Tests:**
- Single binary question about Path 2 recovered seams.
- Whether the ring's identity element is preferentially attached by ADD-subtype edges.
- Significance against subtype-label scrambling null on the same graphs.

**Does not test:**
- Count proportion transport (deferred to v1.2-count).
- Adjacency pattern transport (deferred to v1.2-adj).
- Hub-and-spokes structural transport (deferred indefinitely, requires new extension algorithm).
- Any Path 1 theorem on non-Z/10 carriers.
- Whether identity-edge attachment holds under a different overlay-extension algorithm (it's tested only under P3AP's).
- Any physical, ontological, or real-world claim.

---

## 10. Integrity Check Against Comparison Law

Per `COMPARISON_LAW.md`:

- **Test 1 — path/convention coherence:** different paths → bridge required → ✓ (Path 3 declared).
- **Test 2 — generator type commensurability:** reuses v1.0's inputs which are planted-recovery artifacts on both sides → ✓.
- **Test 3 — metric-object match:** identity-edge attachment is a well-defined graph property of small designed seam artifacts with labeled edges. Legitimate metric for this object type per sprint selector § on Path 3 bridges.

All three tests pass. Spec eligible for freezing.

---

## 11. Prediction (Not a Target)

From `WHY_IDENTITY_EDGE_COMES_NEXT.md` §"Honest Disclosure About Prediction": all 8 P3AP carriers have ADD edge = (1, 2), so real $\mu_\text{ID} = 1.0$. Null expected: for a carrier with edge count $|E|$ and $|E_\text{ADD}| = 1$, the probability that random assignment places the ADD label on a vertex-1-incident edge is $\deg_S(1) / |E|$. P3AP gives $\deg_S(1) = 1$ on all carriers. So per-carrier null probability is $1/|E|$: $1/3$ for Z/14, $1/6$ for the others. Expected $\mu_\text{ID}^\text{null} \approx (1/3 + 7 \cdot 1/6)/8 \approx 0.188$. Standard deviation across 100 replicates: manageable. Predicted separation: $\gg 5\sigma$.

Prediction does not modify thresholds. The run decides.

---

## 12. Awaiting Approval

Three frozen choices for review:

1. Sole primary metric (identity-edge attachment, binary per carrier). Acceptable?
2. Null model (subtype-label scrambling preserving counts per carrier). Acceptable?
3. Thresholds ($\mu_\text{ID} \geq 0.75$, 2σ null separation). Acceptable?

If approved: freeze as P3-Subtype-v1.1 and execute.
If revised: note changes, refreeze under new version, then execute.
