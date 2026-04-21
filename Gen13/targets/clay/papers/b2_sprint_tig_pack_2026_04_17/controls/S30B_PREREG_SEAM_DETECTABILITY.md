# Sprint 30b Pre-Registration
## Seam Detectability Under Low-N Sampling + Persistence Extraction

---

**Status:** FROZEN pending user approval.
**Version:** S30b-v1.0.
**Change policy:** once any datum is scored against this spec, the spec cannot be edited. Amendments require S30b-v1.1+ with explicit justification and full re-run.
**Relation to prior sprints:** S30b tests whether a seam can be extracted at all from noised data. It is a prerequisite to any future transport test. S30-v1.0's vacuous PASS is recorded separately.

---

## 1. Question Under Test

S30-v1.0 returned empty observed seams because mode-equality at high $N$ and moderate noise is noise-immune. This sprint does NOT test transport. It tests:

**S30b-Q:** Under what extraction regime does the observed seam of noised canonical $C_0$ data become:
1. Non-empty on at least a specified fraction of carriers,
2. Stable across seeds (persistent edges recur across independent runs),
3. Tied to the canonical backbone (edges do not appear as symmetric uniform noise)?

This is a pilot-level detectability question, not a transport claim. Passing S30b means "we have a working extractor." Failing means "under this parameter range, no extractor produces stable seam edges."

---

## 2. Family

Same 29 compatible carriers as S28, S29, S30:
```
10, 14, 18, 20, 22, 26, 28, 30, 34, 36, 38, 42, 44, 46, 50,
54, 58, 62, 66, 68, 70, 74, 78, 82, 86, 90, 94, 98, 100
```

---

## 3. Extractor (Frozen)

**Method:** E6 (low-$N$ sampling regime) combined with E3 (persistence across seeds). See `SEAM_EXTRACTION_OPTIONS.md` for rationale.

### 3.1 Per-run extraction (E1 at low $N$)

For each carrier $R_n$ and each seed $r$:
1. Generate $N(n)$ samples using the frozen generator from S30-v1.0 §3.3, but with parameters below.
2. Compute per-cell counts $c_{xy}(z)$.
3. Compute mode operator $T^\text{emp}_r(x, y) = \arg\max_z c_{xy}(z)$ with ties broken by smallest $z$.
4. Compute per-run seam:
$$S_r(R_n) := \{(x, y) : T^\text{emp}_r(x, y) \neq C_0(x, y)\}$$

### 3.2 Persistence filter (E3)

For each carrier, compute the persistence count for each cell:
$$\phi(R_n, (x, y)) := |\{r \in 1..K : (x, y) \in S_r(R_n)\}|$$

A cell is in the **persistent seam** iff $\phi(R_n, (x, y)) \geq \pi K$:
$$S^\text{persistent}(R_n) := \{(x, y) : \phi(R_n, (x, y)) \geq \pi K\}$$

### 3.3 Frozen parameters

| Parameter | Value |
|---|---|
| $N(n)$ per carrier | $N(n) = 10 \cdot n^2$ |
| $p_\text{noise}$ | $0.10$ |
| Number of seeds $K$ | 20 |
| Persistence threshold $\pi$ | 0.50 (10 of 20 runs) |
| Data seed base | 30{,}000 |
| Tie-breaking in mode | smallest $z$ |

**Rationale for $N(n) = 10 \cdot n^2$:** each cell receives approximately 10 observations on average. At this density, sampling variance dominates noise immunity on cells near the mode margin. Concretely:
- $n = 10$: $N = 1{,}000$, ~10 obs/cell.
- $n = 100$: $N = 100{,}000$, ~10 obs/cell.

This parameterization is designed to produce genuine cell-level mode-flipping.

---

## 4. Primary Metrics (Frozen)

Four metrics, computed on the persistent seam for each carrier.

### 4.1 Metric M1 — Non-emptiness rate

Let $E(R_n) := |S^\text{persistent}(R_n)|$ (number of ordered seam pairs).

**Aggregate:** $\mu_\text{ne} := |\{n : E(R_n) \geq 1\}| / 29$ (fraction of carriers with at least one persistent seam edge).

### 4.2 Metric M2 — Mean persistent seam size

$\mu_\text{size} := \text{mean}_n E(R_n)$.

### 4.3 Metric M3 — Per-seed stability

For each carrier, compute seed-pair agreement: for each pair of seeds $(r, r')$, the Jaccard similarity of their seams:
$$J_{r,r'}(R_n) = \frac{|S_r(R_n) \cap S_{r'}(R_n)|}{|S_r(R_n) \cup S_{r'}(R_n)|}$$

(defined as 1 if both are empty, 0 if exactly one is empty).

**Aggregate per carrier:** $\bar{J}(R_n) := \text{mean over all}\binom{K}{2}\text{ pairs}$.

**Overall:** $\mu_J := \text{mean}_n \bar{J}(R_n)$.

### 4.4 Metric M4 — Canonical-tie fraction

For each persistent seam edge $(x, y)$, check whether the cell has structural relationship to the canonical attractor $h_n$ or to unit-group generators. Specifically: does the cell satisfy at least one of:
- $x = 0$ or $y = 0$ (V0 adjacent);
- $x = h_n$ or $y = h_n$ (attractor adjacent);
- $\{x, y\} \cap U(R_n) \neq \emptyset$ (involves a unit);
- $\{x, y\}$ are both non-units (both in zero-divisor set).

**Aggregate:** $\mu_\text{tied} := $ fraction of all persistent seam edges across all carriers satisfying at least one of the above.

The four categories above are exhaustive — *every* cell satisfies at least one of them. So $\mu_\text{tied} = 1.0$ by construction and M4 is a tautology.

**M4 is therefore replaced:** $\mu_\text{tied} := $ fraction of persistent seam edges whose cell has $\{x, y\} \subseteq U(R_n) \cup \{0, h_n\}$, i.e., the cell involves only units, zero, or the attractor. This is a more restrictive condition tied to the canonical construction's active domain.

---

## 5. Pass / Fail Criteria

### 5.1 Primary pass criteria

Sprint passes if ALL of:

1. **$\mu_\text{ne} \geq 0.70$** — at least 70% of carriers (≥ 21 of 29) have at least one persistent seam edge.
2. **$\mu_\text{size} \geq 2.0$** — persistent seams average at least 2 ordered edges per carrier.
3. **$\mu_J \geq 0.30$** — average cross-seed Jaccard similarity across carriers is at least 0.30 (seeds agree more than they disagree).
4. **$\mu_\text{tied} \geq 0.60$** — at least 60% of persistent seam edges lie in the canonical active domain.

### 5.2 Fail criteria

Any of the four primary thresholds violated.

### 5.3 Unclear outcome

All four aggregate metrics pass on their own thresholds, but at least one metric is within 10% of its threshold.

In this case: report as UNCLEAR, flag which thresholds were marginal.

---

## 6. Anti-Tuning Rules

1. $N(n) = 10 \cdot n^2$ is frozen.
2. $p_\text{noise} = 0.10$ is frozen.
3. $K = 20$ seeds is frozen.
4. $\pi = 0.50$ persistence threshold is frozen.
5. Mode tie-breaking is frozen (smallest $z$).
6. Seed base is frozen (30{,}000).
7. The four metric thresholds (0.70, 2.0, 0.30, 0.60) are frozen.
8. No alternative extractor may be substituted if the sprint produces a FAIL.
9. No parameter sweep within the sprint. A single run with frozen parameters.

---

## 7. Null Model

This sprint does NOT include a null model.

S30b is a detectability sprint, not a transport sprint. The question is whether the extractor produces a non-empty, stable, structurally-tied seam at all. No null is needed to answer that; the metrics are calibrated against absolute thresholds.

**A null model would be required for S30c or later transport sprints** that build on S30b's extractor. Those are out of scope here.

---

## 8. Deliverables

Written to `/home/claude/sprint30b/`:

- `S30B_PERSISTENT_SEAMS.json` — per-carrier: edges in persistent seam, size, canonical-tie fraction.
- `S30B_PER_SEED_SEAMS.csv` — per (carrier, seed): seam size, list of ordered pairs.
- `S30B_STABILITY.json` — per-carrier mean Jaccard, overall $\mu_J$.
- `S30B_SCORES.json` — aggregates, thresholds, sub-conditions, verdict.
- `S30B_RESULTS.md` — per-carrier table.
- `S30B_VERDICT.md` — one-paragraph determination.
- `S30B_REPRO.md` — reproducibility notes.

---

## 9. Three-Way Outcome Interpretation

**Outcome 1: PASS.** The low-$N$ + persistence extractor produces non-empty, stable, structurally-tied seams on the compatible family. A working seam extractor exists. Transport tests using this extractor become possible (to be specified in S30c or later, with their own pre-registration).

**Outcome 2: FAIL.** No extractor combination from S30b's frozen parameter set produces a working seam. Either:
- Seam signal is undetectable at these parameters (need different noise model or generator).
- The extractor is too conservative (persistence threshold too high).
- The canonical backbone on non-Z/10 carriers is so dominant that no reasonable noise regime produces detectable structural seam.

All three would need follow-up sprints with different parameter commitments.

**Outcome 3: UNCLEAR.** Metrics pass but marginally. Report finding, flag marginal thresholds, pause before committing to a transport sprint.

---

## 10. What S30b Does Not Test

- Transport of seam topology across carriers.
- Recovery of a "true" physical seam.
- Whether the persistent seams correspond to meaningful algebraic structures.
- Any multi-anchor, prime-orbit, or $\beta$-based hypothesis.

The scope is deliberately narrow: *can the extractor see anything at all?*

---

## 11. Status Effects on Outcomes

- **PASS:** the extractor is validated for use in downstream transport sprints. No invariant is promoted. No existing verdict is modified.
- **FAIL:** the extractor is not validated. Transport tests using this extractor are blocked. Record as "extractor validation failed under S30b-v1.0 parameters."
- **UNCLEAR:** extractor is provisionally usable; transport tests may proceed but must carry the marginal-detection caveat.

---

## 12. Integrity Commitment

S30b runs once. One frozen spec, one deterministic run, one verdict. No parameter sweeps within the sprint. If FAIL, we do not auto-retry with different parameters; we pause and decide with human judgment.

This sprint is explicitly scoped as "do we have a working tool?" Not "what does the tool say about the world?" That second question requires a working tool first.
