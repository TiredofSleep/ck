# Sprint 30 Pre-Registration — FROZEN
## Observed Seam Graph Topology Transport Under Carrier Change

---

**Status:** FROZEN pending user approval of this revised version.
**Version:** S30-v1.0.
**Change policy:** once any datum is scored against this spec, the spec cannot be edited. Amendments require S30-v1.1+ with explicit justification and full re-run.
**Relation to S28/S29:** S30 tests a different invariant family (graph topology rather than scalar curve). S28 and S29 FAIL verdicts remain independently recorded. No rehabilitation of prior sprints.

---

## 1. Hypothesis Under Test (Exactly One)

For each carrier $R_n$ in the tested family, the **observed seam** is the set of pairs where a reference empirical operator disagrees with canonical $C_0$. Building the observed seam graph $G(R_n)$:

- **Vertex set:** $V(G(R_n)) = \{0, 1, \ldots, n-1\}$ — full carrier.
- **Edge set:** $E(G(R_n)) = \{\{x, y\} : (x, y) \in S^{\text{obs}}(R_n) \text{ or } (y, x) \in S^{\text{obs}}(R_n)\}$.

where $S^{\text{obs}}(R_n)$ is the observed seam set from the prior-free discovery input (see §3).

**Hypothesis (S30-H).** The topology type of the observed seam graph $G(R_n)$ preserves a common structural class across the 29-carrier compatible family, distinguishable from scrambled-seam nulls that preserve vertex set and edge count.

"Common structural class" is operationalized via four topology metrics (§4). "Distinguishable" means null separation ≥ 2σ on the aggregate metrics.

---

## 2. Family and Anchor

**Tested family:** same 29 compatible carriers as S28/S29:
```
10, 14, 18, 20, 22, 26, 28, 30, 34, 36, 38, 42, 44, 46, 50,
54, 58, 62, 66, 68, 70, 74, 78, 82, 86, 90, 94, 98, 100
```

**Reference carrier:** $R_{10} = \mathbb{Z}/10\mathbb{Z}$. Its seam graph (from the verified theorem spine) has: 8 ordered pairs → 4 unordered edges, 5 non-isolated vertices $\{1, 2, 4, 8, 9\}$, tree topology with hub at 2 and 3 branches, $d_{\max} = 3$, 1 connected component.

---

## 3. Input Source: Observed Seams

### 3.1 Principle

S30 uses empirically observed seam sets as the primary input object, NOT a synthetic overlay construction. This avoids introducing a heuristic generator into the theorem path.

### 3.2 Observed-seam generation protocol (frozen)

For each carrier $R_n$:

1. **Compute canonical $C_0(R_n, h_n, \sigma_n)$** with $h_n = \max$ odd unit and $\sigma_n(u) = v_2(3u+1)$.
2. **Generate empirical operator $T^{\text{emp}}_n$** via the same protocol as Sprint 21's prior-free discovery: generate data from a noised version of the canonical construction (using the same generator used in Sprint 21), compute the mode operator from the data.
3. **Compute observed seam** $S^{\text{obs}}(R_n) := \{(x, y) \in R_n \times R_n : T^{\text{emp}}_n(x, y) \neq C_0(x, y)\}$.

### 3.3 Data generation parameters (frozen)

- $N = 200{,}000$ samples per carrier.
- Noise level $p_{\text{noise}} = 0.10$ (moderate, matches Sprint 21 range).
- Sampling seed: 30 (distinct from S28's 28 and S29's 29).
- Uniform replacement noise.
- Mode operator: majority vote per $(x, y)$ pair.

### 3.4 Why generated data and not "true" observed data

No reference TSML exists for carriers other than Z/10. To keep the protocol uniform across carriers, S30 generates empirical data on each carrier using a fixed (noised) canonical construction. This means the observed seam is a property of *how noise-robust the canonical construction is on each carrier*, not a property of a physically observed system.

This is a known scope limitation. S30 tests whether the noise-induced seam graphs preserve topology type, which is a legitimate transport question even though it does not test "true TSML seam" transport (no such data exists for non-Z/10 carriers).

### 3.5 What S30 does NOT do

- Does not use a synthetic overlay generator (doubling-chain rule, shell-involution rule, etc.) — those are not in the theorem path.
- Does not use the Z/10-specific seam $\{(1,2), (2,4), (2,9), (4,8)\}$ as a template to extend to other carriers.
- Does not use prime-orbit graphs or any multi-anchor add-on.

---

## 4. Topology Metrics (Frozen)

Exactly four metrics. No alternatives, no substitutions.

### 4.1 Metric M1 — Component count

Let $V'(G(R_n))$ = non-isolated vertices (vertices with degree ≥ 1).
Let $k(R_n)$ = number of connected components of the induced subgraph on $V'(G(R_n))$.

**Hypothesis:** $k(R_n)$ is small and bounded across the family. Concretely: $k(R_n) \leq 3$ for all carriers.

**Aggregate:** fraction of carriers with $k(R_n) \leq 3$, denoted $K_{\text{pass}}$.

### 4.2 Metric M2 — Acyclicity (tree-ness / forest-ness)

Let $|E(G(R_n))|$ = number of unordered edges.
Let $|V'(G(R_n))|$ = number of non-isolated vertices.
Let $k(R_n)$ = component count (as in M1).

**Forest indicator:** $F(R_n) := \mathbb{1}[|E(G(R_n))| = |V'(G(R_n))| - k(R_n)]$.

(A forest of $k$ components on $n$ vertices has exactly $n - k$ edges.)

**Aggregate:** fraction of carriers that are forests, denoted $F_{\text{pass}}$.

### 4.3 Metric M3 — Maximum degree

$d_{\max}(R_n) := \max_{v \in V'(G(R_n))} \deg_G(v)$.

**Hypothesis:** $d_{\max}(R_n)$ is bounded small. Z/10 has $d_{\max} = 3$.

**Aggregate:** fraction of carriers with $d_{\max}(R_n) \leq 4$, denoted $D_{\text{pass}}$. (Threshold $\leq 4$, not $\leq 3$, to allow one-step relaxation from Z/10's value.)

### 4.4 Metric M4 — Compact branch descriptor

The **branch profile** $B(R_n)$ is the sorted tuple of degrees of non-isolated vertices (degree sequence).

Z/10 branch profile: $(3, 1, 1, 1, 2)$ sorted → $(1, 1, 1, 2, 3)$.

**Hypothesis:** the branch profile is dominated by low-degree vertices (degrees 1 and 2), with at most one or two higher-degree hub vertices.

**Specific test:** define $\rho(R_n) := \text{fraction of non-isolated vertices with degree} \leq 2$.

**Aggregate:** fraction of carriers with $\rho(R_n) \geq 0.70$, denoted $P_{\text{pass}}$.

---

## 5. Pass / Fail Criteria

### 5.1 Primary pass criteria

Sprint **passes** if ALL of:

1. $K_{\text{pass}} \geq 0.85$ — at least 25 of 29 carriers have component count $\leq 3$.
2. $F_{\text{pass}} \geq 0.80$ — at least 24 of 29 carriers are forests.
3. $D_{\text{pass}} \geq 0.85$ — at least 25 of 29 carriers have $d_{\max} \leq 4$.
4. $P_{\text{pass}} \geq 0.85$ — at least 25 of 29 carriers have $\rho \geq 0.70$.
5. **Null separation on $F_{\text{pass}}$**: real $F_{\text{pass}}$ exceeds null mean by ≥ 2σ.
6. **Null separation on $P_{\text{pass}}$**: real $P_{\text{pass}}$ exceeds null mean by ≥ 2σ.

### 5.2 Fail criteria

- Any of the four aggregate metrics ($K, F, D, P$) below its threshold.
- Null separation on $F_{\text{pass}}$ below 2σ.
- Null separation on $P_{\text{pass}}$ below 2σ.

### 5.3 Unclear

- All four aggregate metrics pass on their own thresholds.
- Null separation is between 1σ and 2σ on $F_{\text{pass}}$ or $P_{\text{pass}}$.

---

## 6. Null Model

**Null N1 — Edge-count-preserving scramble.**

For each carrier $R_n$ with observed seam graph $G(R_n)$:
- Let $m = |E(G(R_n))|$.
- For each of 100 scrambles (seed-controlled, §6.2):
  - Draw a uniform random graph on the same vertex set $V = \{0, 1, \ldots, n-1\}$ with exactly $m$ edges. (Erdős–Rényi $G(n, m)$ model.)
  - Compute the four metrics $K^{\text{scr}}, F^{\text{scr}}, D^{\text{scr}}, P^{\text{scr}}$ on the scrambled graph.
- Aggregate: null distributions of $K_{\text{pass}}^{\text{scr}}, F_{\text{pass}}^{\text{scr}}, D_{\text{pass}}^{\text{scr}}, P_{\text{pass}}^{\text{scr}}$ across 100 scrambles.

This null preserves:
- Vertex set: $\{0, 1, \ldots, n-1\}$.
- Edge count: $m$ per carrier.

It does NOT preserve:
- Specific edges.
- Vertex positions of hubs.
- Any structure beyond the count.

**Rationale:** the tested hypothesis is that the *specific* edges in the observed seam produce a distinctive topology. The null asks: would $m$ edges chosen uniformly at random also produce this topology? If yes, the observed structure is not a transport signal. If no, the observed structure carries information beyond edge count.

### 6.2 Null seed

`NULL_SEED = 3000` (distinct from S28's 28, S29's 29, S30's data-gen seed 30).

Scrambles are deterministic given this seed.

---

## 7. Anti-Tuning Rules

1. The 29-carrier family is frozen. No exclusions, no additions.
2. The four topology metrics M1–M4 are frozen. No substitutions.
3. The four aggregate thresholds (0.85, 0.80, 0.85, 0.85) are frozen.
4. The 2σ null separation requirement is frozen on $F_{\text{pass}}$ and $P_{\text{pass}}$.
5. The data-generation parameters ($N = 200{,}000$, $p_{\text{noise}} = 0.10$, seed 30) are frozen.
6. The null model (edge-count-preserving Erdős–Rényi) is frozen.
7. No alternative graph invariant (girth, clustering coefficient, diameter) may be substituted if the frozen metrics yield unclear results.
8. Fitter determinism is required; given the same data and seeds, output must be bit-reproducible.

---

## 8. Deliverables

Required outputs written to `/home/claude/sprint30/`:

- `S30_SEAM_GRAPHS.json` — one entry per carrier: $n$, vertex list, edge list, component count, forest flag, $d_{\max}$, degree sequence, $\rho$.
- `S30_NULL_DATA.csv` — one row per (carrier, scramble_id): $n$, scramble_id, $k^{\text{scr}}$, $F^{\text{scr}}$, $d^{\text{scr}}_{\max}$, $\rho^{\text{scr}}$.
- `S30_SCORES.json` — aggregate metrics (real), null statistics, sigma separations, sub-conditions, verdict.
- `S30_RESULTS.md` — per-carrier topology table.
- `S30_NULL_COMPARISON.md` — null distributions and sigma separations.
- `S30_VERDICT.md` — one-paragraph determination.
- `S30_REPRO.md` — reproducibility notes.

---

## 9. Three-Way Outcome Interpretation

**Outcome 1: PASS.** Observed seam topology preserves type across the compatible family, distinguishable from edge-count-preserving random graphs at 2σ. The invariant "seam graph topology preserves type under carrier change" is added to `INVARIANTS_BEYOND_TSML.md` in the "Confirmed transport in tested settings" tier. Does NOT affect the S28/S29 demotions.

**Outcome 2: FAIL.** Seam topology does not preserve type across the family at the pre-registered thresholds, OR the observed pattern is not distinguishable from random-edge-count nulls. Adds a line to `LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md` under "Attempted transport, not confirmed." No further action within the sprint.

**Outcome 3: UNCLEAR.** Aggregate metrics pass but null separation is marginal. Report finding without movement on the split document.

---

## 10. What S30 Tests and Does Not Test

**Tests:**
- One invariant: observed seam graph topology.
- One input: generated empirical seam per carrier (uniform noise model, fixed seed).
- One family: 29 compatible carriers from prior sprints.
- One null: edge-count-preserving Erdős–Rényi scramble.

**Does not test:**
- Prime-orbit graph structure (deferred to S31 per user instruction).
- Synthetic overlay operator topology (removed from this sprint).
- Multi-anchor tension metric.
- Non-ring carriers.
- Physics, STD bridge, ontology claims.

---

## 11. What S30 Cannot Establish (Even Under Full PASS)

- That the observed seam reflects "true" TSML structure on carriers beyond Z/10 — no such reference data exists.
- That seam topology survives under non-uniform noise, correlated noise, or adversarial perturbation.
- That the specific generative model ($C_0$ + uniform replacement noise) produces seams that represent any real-world finite system.
- That the invariant transports beyond the compatible family.

A PASS means: within the specific test conditions, observed seam graphs on the 29-carrier family share topology properties (forest-like, low-degree, small component count) that are distinguishable from random graphs of matching density. That claim is narrow and internally consistent with the discipline.

---

## 12. Integrity Commitment

S30 runs once against this frozen spec. The verdict is computed from pre-registered thresholds applied to pre-registered metrics. No interpretation beyond the frozen hypothesis is written into `S30_VERDICT.md`. Observations about the data that would suggest follow-up sprints go into a separate `S30_FOLLOWUPS.md` file, logged but not acted upon within S30.

---

## 13. Ready-to-Run Summary

| Component | Value |
|---|---|
| Carrier family | 29 compatible carriers from S28/S29 |
| Primary object | Observed seam graphs from noised-$C_0$ generation |
| Data-gen seed | 30 |
| Data-gen $N$ | 200,000 per carrier |
| Data-gen noise | $p = 0.10$, uniform replacement |
| Topology metrics | $K, F, D, P$ (four frozen) |
| Pass thresholds | 0.85, 0.80, 0.85, 0.85 |
| Null model | Edge-count-preserving Erdős–Rényi, 100 scrambles |
| Null seed | 3000 |
| Sigma threshold | 2σ on $F_{\text{pass}}$ and $P_{\text{pass}}$ |
| Anti-tuning rules | 8 enumerated in §7 |

---

## 14. Awaiting Approval

This is the revised frozen version per user direction:
- Observed seams (generated via noised-$C_0$), not synthetic overlay algorithm.
- Graph topology only; no prime-orbit graph.
- Same 29-carrier family as S28/S29.
- Four topology metrics, four aggregate thresholds.

If approved: freeze as S30-v1.0, execute in next sprint.
If edits requested: revise specific fields, return here for confirmation before execution.

Discipline maintained: no rescue of S28 or S29, no interpretation beyond the frozen hypothesis, no alternate metrics substituted after results are visible.
