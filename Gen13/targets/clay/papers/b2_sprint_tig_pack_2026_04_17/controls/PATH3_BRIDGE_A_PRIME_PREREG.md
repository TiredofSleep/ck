# Path 3 Bridge A-Prime — Pre-Registration
## Planted-Recovery Topology Comparison Across Paths

---

## Scope Declaration

**Path:** Bridge Test (Path 3)
**Attractor convention:** cross-path. Path 1 side uses $h_\text{thm} = 7$ on Z/10. Path 2 side uses $h_\text{ext}(R_n) = \max$ odd unit on each Path 2 carrier.
**Claim class:** bridge-level. Strongest possible outcome is a relational claim between planted-recovery artifacts across paths at the topology level. No theorem-level or observation-level claims produced by this sprint.
**Canonical construction source:** Path 1 uses published Z/10 TSML under $h_\text{thm}$. Path 2 uses extended $C_0$ family under $h_\text{ext}$.
**Relation to prior sprints:**
- Inherits extractor architecture from S31-pilot-v2.0 (Path 1, extractor ceiling-validated on Z/10).
- Inherits Path 1 theorem planted overlay from published TSML (B1-confirmed).
- Does NOT inherit P3-BridgeA's Path 2 input (noise-union seam); that was the object-type mismatch that caused P3A's FAIL.
- Does NOT inherit Sprint 21's discovered seams; this sprint uses *planted* recovery, not prior-free discovery.

**Explicit bridging rule:** both sides are planted-recovery artifacts produced by the same extractor applied to $(C_0 + S_\text{planted})$ data under moderate noise, with persistence filtering. Topology metrics are computed on both sides and compared against matched-density random null.

---

**Status:** FROZEN pending user approval.
**Version:** P3-BridgeA-Prime-v1.0.
**Change policy:** once any datum is scored against this spec, the spec cannot be edited. Amendments require v1.1+ and a fresh run.

---

## 1. Hypothesis Under Test (Exactly One)

**Hypothesis (P3A'-H).** The recovered planted seam from Z/10 (under $h_\text{thm} = 7$ with the theorem's published overlay) and the recovered planted seams from Path 2 carriers (under $h_\text{ext}$ with the algorithmically-extended overlay) share topology features — forest-ness, small component count, low max degree, low-degree-profile dominance — that are not reproducible by random graphs of matched edge count.

This is a bridge-level claim. Under PASS, the minimal permitted sentence is reproduced in `WHY_A_PRIME_IS_NOW_VALID.md` §"The Honest Scope of A-Prime."

---

## 2. Family and Anchor

**Path 1 anchor:** Z/10. The reference planted seam is the theorem's published overlay:
$S_\text{planted,1} = \{(2,4), (4,2), (4,8), (8,4), (2,9), (9,2), (1,2), (2,1)\}$ — 8 ordered cells, 4 unordered edges.

**Path 2 tested carriers (frozen):**
$\{14, 22, 34, 42, 46, 58, 74, 94\}$ — 8 carriers.

Same carrier set as P3-BridgeA for continuity. Z/10 excluded from Path 2 side (it is the Path 1 anchor).

---

## 3. Overlay Extension Algorithm (Frozen)

For each Path 2 carrier $R_n$:

### 3.1 MAX overlay on $R_n$

1. **Doubling chain:** starting from 2, compute $2, 4, 8, 16, \ldots \bmod n$ until a value repeats or a value is a duplicate of the starting position. Let chain $= [c_1, c_2, \ldots, c_\ell]$ where $c_1 = 2$, $c_{i+1} = 2 c_i \bmod n$.

2. **Chain pairs:** all adjacent pairs in the chain, both orderings:
   $P_\text{chain}(R_n) = \{(c_i, c_{i+1}), (c_{i+1}, c_i) : 1 \leq i < \ell\}$

3. **Attractor-involution pairs:** the pair $(c_1, h_\text{ext}(R_n))$ and its reverse:
   $P_\text{inv}(R_n) = \{(2, h_\text{ext}(R_n)), (h_\text{ext}(R_n), 2)\}$
   if $h_\text{ext}(R_n) \in U(R_n)$ (always true by definition of $h_\text{ext}$).

4. **MAX domain:** $S_\text{MAX}(R_n) = P_\text{chain}(R_n) \cup P_\text{inv}(R_n)$.

5. **MAX rule:** $T_\text{gen}(x, y) = \max(x, y)$ on this domain.

**Worked example at $n=14$:** doubling chain is $[2, 4, 8]$ (next would be 16 ≡ 2, stop). $P_\text{chain} = \{(2,4), (4,2), (4,8), (8,4)\}$ (4 ordered cells). $h_\text{ext}(14) = 13$. $P_\text{inv} = \{(2, 13), (13, 2)\}$. $S_\text{MAX}(R_{14}) = 6$ ordered cells.

**Worked example at $n=22$:** doubling chain is $[2, 4, 8, 16]$ (next is 32 ≡ 10, not in U(22) and not 2, continue: $20, 40 \equiv 18, 36 \equiv 14, 28 \equiv 6$ — these are all even non-units in $R_{22}$, chain continues through non-units). **Frozen rule:** chain stops when $c_i = c_j$ for some $j < i$, OR when chain length reaches 6, whichever comes first. For Z/22: $[2, 4, 8, 16, 10, 20]$ (length 6, stop). Adjacent pairs: 5 pairs × 2 orderings = 10 cells.

**General frozen constraint:** chain length capped at 6 for tractability and to keep the planted overlay small enough to test against Z/10's 4-edge benchmark.

### 3.2 ADD overlay on $R_n$

**Identity-edge pairs:** $S_\text{ADD}(R_n) = \{(1, 2), (2, 1)\}$ — 2 ordered cells. Same on every carrier.

**ADD rule:** $T_\text{gen}(x, y) = (x + y) \bmod n$ on this domain.

### 3.3 Full planted overlay

$S_\text{planted,2}(R_n) = S_\text{MAX}(R_n) \cup S_\text{ADD}(R_n)$.

Size ranges from 6 to 12 ordered cells depending on chain length at carrier.

### 3.4 Audit requirement

**Before running the sprint, compute and verify:**

- For each Path 2 carrier, the specific cells in $S_\text{planted,2}$ under the overlay extension.
- For each carrier and each planted cell $(x,y)$: verify that the planted value $T_\text{gen}(x,y)$ *differs* from the canonical value $C_0(x,y)$. If they coincide (as happened for $(2,9)$ in S31-pilot-v1.0 under $h = 9$), that cell is structurally undetectable and must be removed from $S_\text{planted,2}$ as a spec-design step, not a runtime discovery.

The audit runs as a pre-flight check within the sprint script. If any cell is undetectable under its carrier, the cell is removed from the overlay before data generation, and the removal is logged in the results document. This prevents an S31-pilot-v1.0-style invisible-cell issue.

---

## 4. Generator and Extractor (Frozen)

For each (Path 2 carrier, seed $r$) combination:

1. Compute $C_0(R_n, h_\text{ext}(R_n), \sigma_n)$.
2. Compute $S_\text{planted,2}(R_n)$ per §3.
3. Apply overlay audit per §3.4; remove undetectable cells.
4. Construct $T_\text{gen} = C_0 + S_\text{planted,2}$.
5. Generate $N(n) = 10 \cdot n^2$ samples under uniform replacement noise at $p = 0.10$.
6. Compute mode operator with tie-break smallest $z$.
7. Extract per-run seam against $C_0$: $S_r(R_n) = \{(x, y) : T^\text{emp}(x, y) \neq C_0(x, y)\}$.

Repeat for $K = 10$ seeds. Compute persistent seam: $S_\text{persistent}(R_n) = \{(x, y) : \text{present in} \geq 5 \text{ of } 10 \text{ seeds}\}$.

**Path 1 side (for reference):** use the existing S31-pilot-v2.0 outputs at $p = 0.10$ with MAX+ADD overlay. Persistent seam on Z/10 at $p = 0.10$ from v2.0 is exactly the planted set of 8 ordered cells (ceiling recovery).

**Parameters inherited from S31-pilot-v2.0:**
- $N(n) = 10 \cdot n^2$.
- $p = 0.10$ uniform replacement (single noise level; A-Prime is a bridge, not a noise-degradation sprint).
- $K = 10$.
- $\pi = 0.50$.
- Tie-break smallest $z$.

**New parameters:**
- Data seed base: `DATA_SEED_BASE = 33000`.
- Per-run seed: `33000 + 1000 * n + r`.
- Null seed: `NULL_SEED = 33100`.

---

## 5. Graph Construction (Frozen)

For each recovered persistent seam:

1. Treat each ordered pair $(x, y)$ in $S_\text{persistent}$ as a contribution to edge $\{x, y\}$ (unordered).
2. Seam graph has vertex set $\{0, 1, \ldots, n-1\}$ and edge set = set of unordered pairs derived from $S_\text{persistent}$, self-loops permitted but none expected for these planted overlays.
3. Metrics computed on non-isolated vertices only.

---

## 6. Metrics (Frozen — Per `A_PRIME_METRIC_SET.md`)

Four primary metrics, one diagnostic. All applied to both Path 1 reference graph and each Path 2 recovered seam graph.

**M1 — Forest-ness.** $F(R) = \mathbb{1}[|E| = |V_\text{ni}| - k]$.

**M2 — Component count.** $k(R)$.

**M3 — Max degree.** $d_\text{max}(R)$.

**M4 — Low-degree profile.** $\rho(R)$ = fraction of non-isolated vertices with degree $\leq 2$.

**M5 — Hub concentration (diagnostic).** $H(R)$ = fraction of edges incident to the max-degree vertex.

**Family aggregates over Path 2:**
- $\mu_F = $ fraction of Path 2 carriers with $F = 1$.
- $\mu_k = $ mean component count across carriers.
- $\mu_d = $ fraction of Path 2 carriers with $d_\text{max} \in \{2, 3, 4\}$.
- $\mu_\rho = $ fraction of Path 2 carriers with $\rho \geq 0.70$.

---

## 7. Null Model (Frozen)

**N1 — Edge-count-preserving uniform random graph** on the same vertex set.

For each Path 2 carrier, 100 null replicates: draw $|E(S_\text{persistent}(R_n))|$ edges uniformly at random without replacement from $\binom{n}{2}$ unordered pairs (no self-loops in null). Compute metrics.

Null seed 33100. 100 replicates × 8 carriers = 800 null graphs.

---

## 8. Pass / Fail Criteria (Frozen)

### 8.1 Primary pass criteria

Sprint passes if ALL of:

1. **$\mu_F \geq 0.75$** — at least 6/8 Path 2 carriers have forest seams.
2. **$\mu_k \leq 1.5$** — mean component count ≤ 1.5.
3. **$\mu_d \geq 0.75$** — at least 6/8 carriers with $d_\text{max} \in \{2, 3, 4\}$.
4. **$\mu_\rho \geq 0.75$** — at least 6/8 carriers with $\rho \geq 0.70$.
5. **Null separation on $\mu_F$:** real $\mu_F$ exceeds null mean by $\geq 2\sigma$.
6. **Null separation on $\mu_k$:** real $\mu_k$ is *below* null mean by $\geq 2\sigma$ (fewer components than random — the active structural signal).

### 8.2 Fail triggers

Any primary threshold violated, or either null separation below 2σ.

### 8.3 Unclear

All primary thresholds met, but at least one null separation is 1σ–2σ. Report with marginal flag. Uses one-sided within-threshold rule (learned from S31-pilot-v2.0's ceiling-artifact issue): ceiling values do not trigger UNCLEAR.

---

## 9. Anti-Tuning Rules

1. Path 2 carrier list (§2) frozen.
2. Overlay extension algorithm (§3) frozen, including doubling-chain cap of 6.
3. Pre-flight audit removes undetectable cells (§3.4); this is part of the frozen algorithm, not a runtime adjustment.
4. Extractor parameters (§4) frozen.
5. Metric definitions (§6) frozen.
6. Null model (§7) frozen.
7. Thresholds (§8) frozen.
8. M5 hub-concentration stays diagnostic; cannot be promoted to pass/fail post-hoc.
9. No alternative metric or null substitution.
10. If FAIL, no re-run as v1.0 with adjusted parameters; successor is v1.1+ with new pre-reg.

---

## 10. Deliverables

Written to `/home/claude/path3_bridgeAprime/`:

- `P3AP_OVERLAY_AUDIT.json` — per Path 2 carrier: computed planted overlay, cells removed by audit (if any), final overlay used.
- `P3AP_PATH1_GRAPH.json` — Z/10 reference graph (from S31-pilot-v2.0's perfect recovery).
- `P3AP_PATH2_GRAPHS.json` — per Path 2 carrier: recovered persistent seam, edges, topology metrics.
- `P3AP_PER_SEED.csv` — per (carrier, seed) seam size.
- `P3AP_NULL_DATA.csv` — per (carrier, null replicate) metrics.
- `P3AP_SCORES.json` — family aggregates, nulls, sigma separations, sub-conditions, verdict.
- `P3AP_RESULTS.md` — per-carrier table with Path 1 reference in first row.
- `P3AP_VERDICT.md` — one-paragraph determination.
- `P3AP_REPRO.md` — reproducibility notes.

---

## 11. Three-Way Outcome

**PASS.** First confirmed Path 3 bridge. Recovered planted artifacts share topology signature across paths under the specified overlay extension. Permits a subsequent sprint testing finer features (subtype mix, degree-sequence distributional match) or extension to alternative overlay rules.

**FAIL.** Extended overlay artifacts do not share topology signature with Z/10 theorem-recovery artifact. Attribution per §"What Could Go Wrong" in `A_PRIME_METRIC_SET.md`: recovery quality drop, algorithmic difference per carrier, Z/10-uniqueness, or metric-hypothesis mismatch. Successor sprint may try a different overlay extension rule under new spec.

**UNCLEAR.** Primary metrics pass but null separation marginal. Report, flag specific marginal metric, pause for judgment.

---

## 12. Scope Boundaries

**Tests:**
- Topology-level similarity between Z/10 theorem-recovered seam and Path-2-extended-overlay-recovered seams.
- One overlay-extension algorithm (doubling-chain + identity-edge + attractor-involution).
- One noise level ($p = 0.10$), one persistence threshold ($\pi = 0.50$).

**Does not test:**
- Whether the overlay-extension algorithm is "correct" or "canonical" (it is frozen as one heuristic).
- Transport of any theorem.
- Cell identity correspondence.
- Rule-subtype transport (diagnostic only, if run at all).
- Any invariant other than seam topology.
- Physical or ontological claims.

---

## 13. Integrity Check Against Comparison Law

Per `COMPARISON_LAW.md` tests:

- **Test 1:** different paths → bridge required → ✓ (this is a Path 3 bridge sprint).
- **Test 2:** both sides are planted-recovery artifacts produced by the same extractor under the same noise regime → ✓ (same generator type).
- **Test 3:** topology metrics on small designed artifacts are ✓ in the compatibility matrix → ✓.

All three tests pass. Spec eligible for freezing.

---

## 14. Awaiting Approval

Frozen choices for review:

1. Path 2 carrier list {14, 22, 34, 42, 46, 58, 74, 94}. Acceptable?
2. Overlay extension algorithm: doubling-chain (capped at 6) + identity-edge + attractor-involution. Acceptable?
3. Pre-flight audit to remove undetectable cells. Acceptable?
4. Inheriting S31-pilot-v2.0 parameters ($N = 10n^2$, $p = 0.10$, $K = 10$, $\pi = 0.50$). Acceptable?
5. Thresholds: $\mu_F \geq 0.75$, $\mu_k \leq 1.5$ with 2σ null separation below null mean, $\mu_d \geq 0.75$, $\mu_\rho \geq 0.75$, 2σ null separation on $\mu_F$. Acceptable?
6. Null model: edge-count-preserving uniform random graph. Acceptable?

If approved: freeze as P3-BridgeA-Prime-v1.0 and execute.
If revised: note changes, refreeze under new version, then execute.
