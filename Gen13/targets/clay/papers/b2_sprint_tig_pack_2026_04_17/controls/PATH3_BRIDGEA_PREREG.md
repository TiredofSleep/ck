# Path 3 Bridge A — Pre-Registration
## Theorem Seam vs Discovered Seams, Topology-Level Comparison

---

## Scope Declaration

**Path:** Bridge Test (Path 3)
**Attractor convention:** cross-path. Path 1 theorem seam on Z/10 uses $h_{\text{thm}} = 7$. Path 2 discovered seams on other carriers use $h_{\text{ext}} = \max$ odd unit.
**Claim class:** bridge-level. The sprint's strongest possible outcome is a relational claim between Path 1 and Path 2 objects at the topology level. No theorem-level or observation-level claims.
**Canonical construction source:** combination. Path 1 uses published Z/10 TSML. Path 2 uses extended $C_0$ family as defined in `ATTRACTOR_RECONCILIATION.md` §2 Convention B.
**Relation to prior sprints:** Inherits the published TSML seam from Path 1 (B1 confirmed reconstruction). Inherits the prior-free discovery protocol from Sprint 21 (Path 2) — see §3.2 for the full frozen protocol, since Sprint 21's output files are not available in this execution context and the seams must be regenerated deterministically from a pre-registered procedure.

**Explicit bridging rule:** seams from both paths are compared at the graph-topology level only. No cell-identity correspondence is asserted. No rule-type mapping is assumed. Each seam is converted to a graph on its own carrier's vertex set, and topology-class features are extracted and compared across carriers.

---

**Status:** FROZEN pending user approval.
**Version:** P3-BridgeA-v1.0.
**Change policy:** once any datum is scored against this spec, the spec cannot be edited. Amendments require v1.1+ and a fresh run.

---

## 1. Hypothesis Under Test (Exactly One)

**Hypothesis (P3A-H).** The topology signature of the Path 1 theorem seam on Z/10 and the topology signatures of Path 2 prior-free discovered seams on other carriers share structural features (low component count, forest-ness, low maximum degree, majority-low-degree profile) that are not reproducible by an edge-count-preserving random-graph null.

The hypothesis is about *topology family resemblance*, not about cell identity or rule subtype.

---

## 2. Input Objects

### 2.1 Path 1 seam (fixed reference)

The published Z/10 TSML seam, 8 ordered cells:

$S_1 = \{(2,4), (4,2), (4,8), (8,4), (2,9), (9,2), (1,2), (2,1)\}$

As an unordered graph on vertices $V_1 = \{0, 1, \ldots, 9\}$: 4 unordered edges $\{\{2,4\}, \{4,8\}, \{2,9\}, \{1,2\}\}$. 5 non-isolated vertices $\{1, 2, 4, 8, 9\}$. Topology: 1 connected component, forest (specifically a tree on 5 vertices), $d_{\max} = 3$ (vertex 2 has neighbors 1, 4, 9), $\rho = 4/5 = 0.80$ (4 of 5 non-isolated vertices have degree ≤ 2).

### 2.2 Path 2 seam family (regenerated per frozen protocol)

Sprint 21's prior-free discovery was executed on 39 datasets across 4 carriers, but the output files are not present in the current execution context. To avoid pretending to import data that is not accessible, the Path 2 seams are **regenerated deterministically** from a frozen protocol. If prior Sprint 21 artifacts are located and verified equivalent, they can be substituted without spec change (subject to equivalence check in §3.3).

---

## 3. Input Generation (Frozen Protocol)

### 3.1 Path 2 carriers (frozen)

Same 4 carriers as Sprint 21 plus 4 additional compatible carriers for stability of the comparison:

$\{14, 22, 34, 42, 46, 58, 74, 94\}$

Rationale: Sprint 21's original four were 10, 14, 22, 34. Z/10 is excluded here (it belongs to Path 1 in this bridge). The original set minus Z/10 = {14, 22, 34}. Add {42, 46, 58, 74, 94} for a total of 8 carriers, giving $|U(n)|$ range from 6 (Z/14, Z/18) up to 46 (Z/94). Doubling chains exist and are non-degenerate on all 8.

**Fixed list:** $\{14, 22, 34, 42, 46, 58, 74, 94\}$ — 8 carriers, frozen.

### 3.2 Seam generation protocol per carrier (frozen)

For each carrier $R_n$ in the Path 2 family:

1. Compute canonical $C_0(R_n, h_{\text{ext}}(R_n), \sigma_n)$ where $h_{\text{ext}}(R_n) = \max$ odd unit of $U(R_n)$ and $\sigma_n(u) = v_2(3u+1)$.
2. For each of the 20 seeds indexed $r \in \{0, \ldots, 19\}$:
   - Generate synthetic data using the noised canonical construction: $N(n) = 10 \cdot n^2$ samples, each with $(x, y)$ uniform on $R_n \times R_n$, output $z = C_0(x, y)$ with probability $1 - p$, else uniform on $R_n$, with $p = 0.10$ (continuity with Sprint 21 regime).
   - Compute mode operator $T^{\text{emp}}_r(x, y)$ per cell, tie-break smallest $z$.
   - Extract per-run seam $S_r(R_n) = \{(x, y) : T^{\text{emp}}_r(x, y) \neq C_0(x, y)\}$.
3. Union across seeds: $S_2(R_n) = \bigcup_{r=0}^{19} S_r(R_n)$.

**Important:** This is different from S30b's persistence filter. Sprint 21 reported seam *union* (any cell that ever appeared), not intersection. The union gives a superset of the "true" seam; it is the most generous Path 2 seam definition, consistent with Sprint 21's framing.

**Frozen parameters:**
- $N(n) = 10 \cdot n^2$.
- $p = 0.10$ uniform replacement.
- $K = 20$ seeds.
- Seed formula: `DATA_SEED_BASE + 1000 * n + r`.
- `DATA_SEED_BASE = 32000` (distinct from all prior sprints).

### 3.3 Substitution with prior artifacts (optional)

If at execution time, verified Sprint 21 per-carrier seam union files are located in accessible storage, they may substitute for §3.2's regenerated seams **on condition**: each substituted seam must have been generated with $h_{\text{ext}}$, uniform replacement noise at $p \in [0.05, 0.15]$, and $N \geq 5 \cdot n^2$ per seed. If substitution occurs, the script logs the substitution and both seams (regenerated + substituted) are reported; only one is used for primary metrics per user decision. If conditions are not met or files are not located, §3.2's regenerated seams are used.

This clause exists to permit clean inheritance from Sprint 21 without forcing it when artifacts are missing.

---

## 4. Primary Metrics (Frozen)

All metrics are topology-level and are computed on both Path 1's $S_1$ graph (once, fixed) and each Path 2 carrier's $S_2(R_n)$ graph.

### 4.1 M1 — Component count

$k(R) := $ number of connected components on non-isolated vertices of the seam graph.

Path 1 reference: $k_1 = 1$.

**Family metric:** $\mu_k = \text{mean}_n k(R_n)$ across the 8 Path 2 carriers.

### 4.2 M2 — Forest-ness

$F(R) := \mathbb{1}[|E_{\text{simple}}| = |V_{\text{non-iso}}| - k]$, where $E_{\text{simple}}$ excludes self-loops if any.

Path 1 reference: $F_1 = 1$ (tree).

**Family metric:** $\mu_F = $ fraction of Path 2 carriers with $F(R_n) = 1$.

### 4.3 M3 — Maximum degree

$d_{\max}(R) := $ max vertex degree in the seam graph.

Path 1 reference: $d_{\max,1} = 3$.

**Family metric:** $\mu_d = $ fraction of Path 2 carriers with $d_{\max}(R_n) \leq d_{\max,1} + 2 = 5$. (Band of $\pm 2$ around Path 1's value.)

### 4.4 M4 — Low-degree profile

$\rho(R) := $ fraction of non-isolated vertices with degree $\leq 2$.

Path 1 reference: $\rho_1 = 0.80$.

**Family metric:** $\mu_\rho = $ fraction of Path 2 carriers with $\rho(R_n) \geq 0.60$. (20-percentage-point tolerance from Path 1's 0.80.)

### 4.5 M5 — Subtype mix (optional diagnostic, NOT part of pass/fail)

For each Path 2 cell $(x, y)$ in the seam, compute the modal empirical value $T^{\text{emp}}(x, y)$. Classify:
- MAX-like: modal value equals $\max(x, y)$.
- ADD-like: modal value equals $(x + y) \bmod n$.
- Other: any other mode.

Path 1 subtype mix: 6 MAX + 2 ADD = 0.75 MAX, 0.25 ADD.

**Family metric (diagnostic only):** for each carrier, report MAX-fraction and ADD-fraction of its seam cells. Compare to Path 1's profile narratively; do NOT use for pass/fail.

This is included because subtype classification requires a computable value-matching rule that may not cleanly apply across carriers. Its status is diagnostic to avoid overclaiming if results are messy.

---

## 5. Null Model (Frozen)

**Null N1 — Edge-count-preserving uniform random graph.**

For each Path 2 carrier $R_n$:
- Let $m = |E(S_2(R_n))|$ be the unordered-edge count.
- For each of 100 null replicates:
  - Draw $m$ edges uniformly at random from $\binom{n}{2} + n$ unordered pairs including self-loops. (Sprint 21 seams may contain self-loops in principle; we permit them in null for fairness.)
  - Compute $k, F, d_{\max}, \rho$ on the null graph.
- Aggregate: null distributions of $\mu_k^{\text{null}}, \mu_F^{\text{null}}, \mu_d^{\text{null}}, \mu_\rho^{\text{null}}$ across 100 replicates, each aggregated across the 8 carriers.

**Null seed:** `NULL_SEED = 32100`.

This null preserves vertex set and edge count per carrier, randomizes everything else.

---

## 6. Pass / Fail Criteria

### 6.1 Primary pass

Sprint passes if ALL of:

1. **$\mu_F \geq 0.75$** — at least 6 of 8 Path 2 carriers have forest seam graphs.
2. **$\mu_d \geq 0.75$** — at least 6 of 8 Path 2 carriers have $d_{\max} \leq 5$.
3. **$\mu_\rho \geq 0.75$** — at least 6 of 8 Path 2 carriers have $\rho \geq 0.60$.
4. **$\mu_k \leq 3.0$** — mean component count across the family is at most 3.
5. **Null separation on $\mu_F$:** real $\mu_F$ exceeds null mean by ≥ 2σ.
6. **Null separation on $\mu_\rho$:** real $\mu_\rho$ exceeds null mean by ≥ 2σ.

### 6.2 Fail triggers

Any of the four family-metric thresholds violated, or null separation below 2σ on either $\mu_F$ or $\mu_\rho$.

### 6.3 Unclear

All four family-metric thresholds met, but null separation is between 1σ and 2σ on $\mu_F$ or $\mu_\rho$.

**UNCLEAR rule clarification (learned from v2.0):** the within-threshold check is one-sided only — values exceeding a threshold by less than $0.10 \cdot (\text{ceiling} - \text{threshold})$ trigger a marginal-pass note. Ceiling values do not trigger UNCLEAR.

---

## 7. Anti-Tuning Rules

1. Path 2 carrier list (§3.1) is frozen.
2. Data-generation protocol (§3.2) is frozen.
3. Prior-artifact substitution (§3.3) is permitted only under stated conditions.
4. Primary metrics M1–M4 are frozen.
5. Null model N1 is frozen.
6. Thresholds (§6.1) are frozen.
7. M5 subtype mix is diagnostic only and cannot be promoted to pass/fail post-hoc.
8. No alternative topology metric may be substituted if primary metrics are unclear.
9. Scope declaration is frozen: Bridge Test, cross-path, bridge-level claim class.

---

## 8. Deliverables

Written to `/home/claude/path3_bridgeA/`:

- `P3A_PATH1_GRAPH.json` — the fixed Path 1 seam graph with computed metrics.
- `P3A_PATH2_GRAPHS.json` — per Path 2 carrier: seam edges, topology metrics, subtype mix.
- `P3A_PER_SEED_PATH2.csv` — per (carrier, seed): seam edges contributing to union.
- `P3A_NULL_DATA.csv` — per (carrier, null_replicate): topology metrics on scrambled graph.
- `P3A_SCORES.json` — family aggregates, null statistics, sigma separations, sub-conditions, verdict.
- `P3A_RESULTS.md` — per-carrier table with comparison to Path 1 reference.
- `P3A_VERDICT.md` — one-paragraph determination.
- `P3A_REPRO.md` — reproducibility notes.

---

## 9. Three-Way Outcome

**PASS.** Path 1 theorem seam and Path 2 discovered seams share topology-family signature (forest-ness, low max degree, low-degree profile, small component count) at 2σ separation from matched-density random graphs. Minimal claim: structural resemblance exists. Does NOT promote any invariant to "confirmed transport." Earns the right to design a subsequent Path 3 sprint testing finer resemblance (subtype mix, degree sequences as distributions, Bridge B with overlay extension).

**FAIL.** Topology signatures do not share measurable features beyond density. The minimal bridge between Path 1 and Path 2 at the seam-topology level is not supported. Alternative bridge objects (shell partition, corridor closure, attractor identification) remain to be tested; but seam-topology Bridge A is closed.

**UNCLEAR.** Family metrics pass but null separation is marginal. Report, do not commit to stronger claim.

---

## 10. Scope — What P3A Tests and Does Not Test

**Tests:**
- Structural overlap at graph-topology level between one fixed Path 1 object (published Z/10 seam) and a family of 8 Path 2 objects (discovered seams on specified carriers).
- Specific topology features: component count, forest-ness, max degree, low-degree profile.
- Distinguishability from matched-density random graphs.

**Does not test:**
- Cell-identity correspondence between Path 1 and Path 2 seams.
- Rule-subtype transport (MAX/ADD classification on Path 2 carriers; M5 is diagnostic only).
- Any Path 1 theorem on Path 2 carriers.
- Bridge B's overlay-extension hypothesis.
- Transport of basin ratio, shell partition, or any other invariant besides seam topology.
- Physical, ontological, or real-system claims.

---

## 11. Expected Result (Prediction, Not Target)

Prediction: PASS is plausible. Path 1's seam is a tree on 5 vertices with $d_{\max} = 3$. Sprint 21's prior-free extraction reportedly produces seams that cluster on small subsets of cells near the attractor and identity-edges. If the Path 2 seams are similarly small and sparse relative to their carriers' total cell count, tree-like structure is likely. Null separation depends on density — at 4 edges in a vertex set of 10 or 14 or more, random graphs are often also forest-like. The test will therefore probably hinge on the combination of low max degree AND low-degree profile AND small component count being jointly non-random.

Prediction does not modify thresholds. If PASS: modest bridge-level claim earned. If FAIL: Bridge A closed, design next bridge object.

---

## 12. Integrity Commitment

Sprint runs once. One frozen spec, one deterministic run, one verdict. Three-way outcome follows frozen rules. No interpretation beyond the scope declaration. No rescue of prior sprints. No rescue of Bridge A if it fails — FAIL means FAIL, and the program moves to a different bridge object.

This is the first Path 3 sprint. It sets the precedent for how bridge claims are framed and evaluated under the scope discipline. Narrow is correct. Minimal is correct. The scope declaration's "bridge-level claim class" is the ceiling, not a floor.

---

## 13. Awaiting Approval

Six frozen choices for review:

1. Path 2 carriers: $\{14, 22, 34, 42, 46, 58, 74, 94\}$ — 8 carriers. Acceptable?
2. Seam-generation protocol: union across 20 seeds at $N = 10 n^2$, $p = 0.10$. Acceptable?
3. Prior-artifact substitution clause: optional, under stated conditions. Acceptable?
4. Thresholds: 6 of 8 Path 2 carriers must be forest-like / low-degree / low-profile; $\mu_k \leq 3$; 2σ null separation on $\mu_F$ and $\mu_\rho$. Acceptable?
5. Subtype mix (M5) as diagnostic only, not pass/fail. Acceptable?
6. Null model: edge-count-preserving uniform random. Acceptable?

Once these are confirmed (or revised), this document is frozen as P3-BridgeA-v1.0 and executed.
