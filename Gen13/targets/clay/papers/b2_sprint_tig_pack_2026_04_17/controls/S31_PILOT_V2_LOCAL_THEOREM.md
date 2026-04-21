# S31 Pilot v2 — Local Theorem Path, Z/10 Recovery
## Frozen Spec

---

## Scope Declaration

**Path:** Local Theorem
**Attractor convention:** $h_{\text{thm}} = 7$
**Claim class:** theorem-level (specifically: validates the low-$N$ mode-extractor with persistence filter on the published Z/10 TSML construction)
**Canonical construction source:** published Z/10 TSML (as specified in `THEOREM_SPINE.md` and `WORKED_RECONSTRUCTION.md`)
**Relation to prior sprints:** Inherits from B1 (Path 1) as structural reference for the published TSML. Does not inherit from Sprints 21, 25, 26, 28, 29, 30, 30b (all Path 2). Does not inherit from S31-pilot-v1.0 (cross-path error, FAIL recorded separately).

---

**Status:** FROZEN pending user approval of this version.
**Version:** S31-pilot-v2.0.
**Relation to v1.0:** Replaces v1.0. The v1.0 FAIL verdict stands on the record as a convention-mismatch failure. v2.0 is a new sprint under correct scope, not a rescue.
**Change policy:** once any datum is scored against this spec, the spec cannot be edited. Amendments require v2.1+ and a fresh run.

---

## 1. Purpose

Test whether the low-$N$ mode-extractor with persistence filter recovers the planted seam of the **published Z/10 TSML theorem** when that seam is overlaid on canonical $C_0$ under $h_{\text{thm}} = 7$, across three noise levels and three overlay subsets.

This is a Path 1 (Local Theorem) recovery validation. A PASS confirms the extractor correctly identifies the theorem's seam cells. A FAIL indicates the extractor's architecture needs revision before use on any Path 1, Path 2, or Path 3 sprint.

No transport claim is made by this sprint. No invariant is promoted. No Path 2 object is touched.

---

## 2. Carrier

Z/10 only. $R_{10} = \mathbb{Z}/10\mathbb{Z}$.

Under Path 1:
- $h_{\text{thm}} = 7$.
- $U(10) = \{1, 3, 7, 9\}$.
- Shell partition $\sigma(u) = v_2(3u+1)$: $\{1 \to 2, 3 \to 1, 7 \to 1, 9 \to 2\}$.
- Canonical core: $\{3, 7, 9\}$ (units minus identity).
- Canonical $C_0$ reconstructs the published TSML at 92/100 cells exactly.

---

## 3. Overlays (Frozen)

Exactly the published overlays, defined against the theorem's $h = 7$ construction. Four conditions as in v1.0, but now all compatible with the canonical under the same convention.

### 3.1 Overlay MAX

$S_{\text{MAX}} = \{(2,4), (4,2), (4,8), (8,4), (2,9), (9,2)\}$ — six ordered cells.

Rule: $T_\text{gen}(x, y) = \max(x, y)$.

Under $h = 7$, each of these cells has $C_0(x, y) = 7$ (default rule, since 2, 4, 8 are not in the core), but the MAX rule assigns $\max(x, y) \in \{4, 8, 9\}$. All six cells are detectable (canonical value 7 differs from planted MAX value).

### 3.2 Overlay ADD

$S_{\text{ADD}} = \{(1,2), (2,1)\}$ — two ordered cells.

Rule: $T_\text{gen}(x, y) = (x + y) \bmod 10 = 3$.

Under $h = 7$, both cells have $C_0(x, y) = 7$ (default), but ADD assigns 3. Both cells detectable.

### 3.3 Overlay MAX+ADD

Union: all 8 overlay cells. Reproduces the full published Z/10 TSML seam exactly.

All 8 cells detectable under $h = 7$.

### 3.4 Overlay NONE

No overlay. $T_\text{gen} = C_0$.

Control condition. Expected empty persistent seam at $p \in \{0.02, 0.10\}$.

---

## 4. Generator (Frozen)

For each (overlay, noise, seed):

1. Compute $C_0(R_{10}, h_{\text{thm}} = 7, \sigma)$ using the theorem's canonical rules.
2. Apply overlay (NONE, MAX, ADD, or MAX+ADD) to produce $T_\text{gen}$. On MAX+ADD, $T_\text{gen}$ exactly equals the published Z/10 TSML table (bit-exact, verified by audit).
3. Generate $N = 10 \cdot 10^2 = 1{,}000$ samples:
   - $(x, y)$ uniform in $\{0, \ldots, 9\}^2$.
   - Output $z = T_\text{gen}(x, y)$ with probability $1 - p$, else uniform in $\{0, \ldots, 9\}$.
4. Compute per-cell mode, tie-break by smallest $z$. This is the empirical operator $T^\text{emp}$.
5. Extract per-run seam as disagreement with $C_0$: $S_r = \{(x, y) : T^\text{emp}(x, y) \neq C_0(x, y)\}$.

---

## 5. Extractor Parameters (Frozen)

| Parameter | Value |
|---|---|
| Carrier | Z/10 |
| Attractor | $h_{\text{thm}} = 7$ |
| $N$ per run | 1,000 |
| Noise levels | $\{0.02, 0.10, 0.20\}$ |
| Overlays | NONE, MAX, ADD, MAX+ADD |
| Seeds per (overlay, noise) | 10 |
| Persistence threshold $\pi$ | 0.50 |
| Mode tie-break | smallest $z$ |
| Data seed base | 31100 (distinct from v1.0's 31000) |
| Per-run seed | $31100 + 10000 \cdot \text{overlay\_idx} + 100 \cdot \text{noise\_idx} + r$ |

Overlay indexing: NONE = 0, MAX = 1, ADD = 2, MAX+ADD = 3.
Noise indexing: 0.02 = 0, 0.10 = 1, 0.20 = 2.

Total extractions: 4 × 3 × 10 = 120.

---

## 6. Persistence Filter (Frozen)

For each (overlay, noise) condition:
- Collect 10 per-run seam sets.
- Count appearances per ordered pair across the 10 runs.
- Persistent seam: pairs appearing in $\geq 5$ runs (i.e., $\pi K = 0.50 \times 10 = 5$).

---

## 7. Recovery Metrics (Frozen)

Per (overlay, noise) condition, compute against ground truth $S_\text{planted}$:

### M1 — Jaccard
$J = |S_\text{persistent} \cap S_\text{planted}| / |S_\text{persistent} \cup S_\text{planted}|$, with $J = 1.0$ if both empty.

### M2 — Recall
$R = |S_\text{persistent} \cap S_\text{planted}| / |S_\text{planted}|$ if $|S_\text{planted}| > 0$, else undefined.

### M3 — Precision
$P = |S_\text{persistent} \cap S_\text{planted}| / |S_\text{persistent}|$ if $|S_\text{persistent}| > 0$, else 1.0.

### M4 — Type agreement
For each recovered cell, check whether the modal empirical value across seeds matches the planted overlay rule:
- MAX cells: expected $\max(x, y)$.
- ADD cells: expected $(x + y) \bmod 10$.

$A$ = fraction of recovered cells with matching modal value.

---

## 8. Pass / Fail Criteria (Frozen)

### 8.1 Clean regime ($p = 0.02$)

For each non-NONE overlay:
- $J \geq 0.90$
- $R \geq 0.95$
- $P \geq 0.90$
- $A \geq 0.90$

NONE at $p = 0.02$: persistent seam must be empty.

### 8.2 Reference regime ($p = 0.10$)

For each non-NONE overlay:
- $J \geq 0.70$
- $A \geq 0.80$

NONE at $p = 0.10$: persistent seam must be empty.

### 8.3 Stress regime ($p = 0.20$)

For each non-NONE overlay:
- $J \geq 0.30$.

No type-agreement threshold. NONE at $p = 0.20$ reported but does not auto-fail.

### 8.4 Overall

Sprint **passes** if all sub-conditions 8.1, 8.2, 8.3 hold AND both NONE control requirements at $p \in \{0.02, 0.10\}$ hold.

**Fail** if any sub-condition violated.

**Unclear** if all sub-conditions pass but at least one is within 10% of its threshold.

---

## 9. Anti-Tuning Rules

1. Carrier (Z/10) and attractor ($h = 7$) frozen.
2. Overlay definitions (§3) frozen.
3. Extractor parameters (§5) frozen.
4. Persistence threshold ($\pi = 0.50$) frozen.
5. Metric definitions (§7) frozen.
6. Thresholds (§8) frozen.
7. Seed scheme frozen.
8. Mode tie-break frozen.
9. If FAIL, no parameter adjustment and re-run as v2.0. Next iteration must be v2.1+ with a new pre-registration.

---

## 10. Deliverables

Written to `/home/claude/sprint31_pilot_v2/`:

- `S31Pv2_PER_SEED.csv` — per (overlay, noise, seed): seam size, seam edges.
- `S31Pv2_PERSISTENT.json` — per (overlay, noise): planted seam, persistent seam, intersection, metrics.
- `S31Pv2_SCORES.json` — aggregated metrics, thresholds, sub-conditions, verdict.
- `S31Pv2_RESULTS.md` — per-condition table.
- `S31Pv2_VERDICT.md` — one-paragraph determination.
- `S31Pv2_REPRO.md` — reproducibility notes.

---

## 11. Three-Way Outcome

**PASS.** Extractor validated for Local Theorem Path recovery on Z/10 at low $N$. Earns the right to run a subsequent Path 3 sprint testing whether the overlay-extension algorithm (or a declared alternative bridging rule) produces recoverable seams on carriers under Path 2 canonicals. Does not promote any invariant.

**FAIL.** Extractor architecture does not recover the published Z/10 seam at low $N$ even with the correct convention. This is a stronger FAIL than v1.0's — it would indicate a real tool problem, not a spec-design issue. Diagnostic required: candidate issues are $N$ too low, $\pi$ too strict, tie-breaking interacting with a specific cell. Blocks all downstream recovery sprints.

**UNCLEAR.** Passes but marginally. Report finding, flag condition. User judgment on whether to proceed to Path 3.

---

## 12. What PASS Does Not Establish

- Anything about non-Z/10 carriers.
- Anything about Path 2 canonical constructions.
- Any transport claim.
- Any bridge claim.

A PASS means: the extractor finds what the theorem planted, on the theorem's own ring, under the theorem's own convention. That is exactly the question this sprint asks.

---

## 13. Expected Result (Prediction, Not Target)

Under $h = 7$, all 8 overlay cells are detectable (audit confirmed). At $p = 0.02$ with 10 observations per cell, mode recovery is statistically near-certain for any planted cell whose canonical value is 7 and planted value is something else. Prediction: Jaccard near 1.0 at all three noise levels, type agreement near 1.0 at clean and reference, with some degradation possible at $p = 0.20$.

If the prediction fails, the extractor has a real problem. If it passes, the extractor is validated for the narrow question asked. Predictions are diagnostic expectations only and do not modify pass/fail thresholds.

---

## 14. Integrity Commitment

Sprint runs once. Deterministic. No parameter sweep within the sprint. No adjustment based on observed data. Verdict is whatever the frozen thresholds produce.

This is a Path 1 sprint. Its results belong to the Local Theorem project. Under Path C reconciliation (`ATTRACTOR_RECONCILIATION.md`, `PATH_C_RECOMMENDATION.md`), this is the cleanest possible recovery test: one path, one convention, one question, one verdict.

---

## 15. Awaiting Approval

This spec is frozen pending user confirmation. The scope declaration is clean, the convention is unambiguous, the audit has verified overlay detectability under $h = 7$, and the failure mode of v1.0 cannot recur because the convention mismatch is structurally impossible under this declaration.

Execute or revise.
