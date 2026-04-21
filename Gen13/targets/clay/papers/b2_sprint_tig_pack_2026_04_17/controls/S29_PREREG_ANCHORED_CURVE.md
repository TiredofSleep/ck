# Sprint 29 Pre-Registration
## Anchored Deviation Curve of Basin Ratio Across the Compatible Ring Family

---

**Status:** FROZEN before data collection.
**Version:** S29-v1.0.
**Change policy:** once any Sprint 29 datum is scored against this spec, the spec cannot be edited. Amendments require S29-v1.1+ with a written justification.
**Relation to S28:** S29 tests a different hypothesis with a different metric. S28's FAIL verdict stands independently. If S29 passes, S29's outcome is the evidence for transport; no retroactive re-classification of S28 occurs.

---

## 1. Hypothesis Under Test (Exactly One)

The invariant tested in S29 is the **anchored deviation curve** of the basin ratio across the compatible ring family.

**Precise statement.**

Let $R_{\text{anchor}} = \mathbb{Z}/10\mathbb{Z}$ (see `ANCHOR_DISTANCE_DEFINITION.md` §1).

For each carrier $R_n$ in the tested family:
- $d_1(R_n) = |U(n)| - 4$ is the **depth** from the anchor.
- $D(R_n) = |\beta(R_n) - \beta(R_{10})| = |\beta(R_n) - 0.79|$ is the **deviation** of the basin ratio from the anchor.
- The response variable is $D(R_n)$ as a function of $d_1(R_n)$.

**Hypothesis (S29-H).** The deviation $D(R_n)$ is a well-behaved, monotonically non-decreasing function of $d_1(R_n)$, with bounded residual wobble around a monotone trend.

Equivalently: "the rope has lawful wobble." The far end (large $d_1$) has more deviation than the near end (small $d_1$), and the deviation grows predictably with depth.

---

## 2. Family and Anchor

**Anchor:** $R_{\text{anchor}} = \mathbb{Z}/10\mathbb{Z}$ (frozen in `ANCHOR_DISTANCE_DEFINITION.md`).

**Tested family:** the same 29 carriers as S28:
```
10, 14, 18, 20, 22, 26, 28, 30, 34, 36, 38, 42, 44, 46, 50,
54, 58, 62, 66, 68, 70, 74, 78, 82, 86, 90, 94, 98, 100
```

Keeping the family identical to S28 allows direct comparison of a different metric on the same data. No carrier additions or exclusions are permitted.

---

## 3. Primary Metrics (Frozen)

All metrics computed on the 29-carrier family using canonical $C_0$ and canonical attractor rule $h = \max$ odd unit.

### 3.1 Metric M1 — Monotonicity of Deviation with Depth

Sort carriers by $d_1(R_n)$ (ties broken by $n$ ascending). Let $(D^*_1, D^*_2, \ldots, D^*_{29})$ be the deviations in this order.

**Kendall's tau** of the sorted sequence measures monotonicity:

$$\tau = \frac{C - D}{\binom{29}{2}}$$

where $C$ is the number of concordant pairs ($D^*_i < D^*_j$ when $d_i < d_j$) and $D$ is discordant. $\tau \in [-1, +1]$.

**Pass threshold:** $\tau \geq 0.35$ (moderate positive monotonic relationship; standard interpretation in rank-correlation literature).

**Why Kendall's tau and not Spearman's ρ or linear correlation:** tau is robust to tied depth values (of which S29 has several — e.g., three carriers at $d_1 = 8$). Spearman's ρ inflates tied ranks; linear correlation assumes a specific functional form not committed by the hypothesis.

### 3.2 Metric M2 — Residual Compactness Around Trend

Fit a simple linear regression $\hat{D}(d_1) = a + b \cdot d_1$ to the 29 $(d_1, D)$ pairs. Compute residuals $r_i = D(R_{n_i}) - \hat{D}(d_1(R_{n_i}))$.

**Coefficient of determination** $R^2$ of the fit.

**Pass threshold:** $R^2 \geq 0.40$.

**Why linear:** simplest monotone-trend assumption; does not privilege any specific functional form. If the true relationship is nonlinear, $R^2$ will be modest but nonzero. The test asks whether depth *predicts* deviation, not whether it predicts it via a specific curve.

**Note on R² threshold:** 0.40 is modest. It asks for "depth explains at least 40% of deviation variance." If depth explains less than 40%, the rope hypothesis is not supported; wobble is larger than trend.

### 3.3 Metric M3 — Bounded Anchor-Relative Deviation

For all carriers, $D(R_n) \leq 0.25$.

**Rationale:** the rope model predicts that even at maximum depth ($d_1 \approx 42$), the deviation from the anchor basin ratio is bounded. A carrier whose $\beta$ differs from $\beta_{\text{anchor}}$ by more than 25 percentage points is "off the rope."

**Pass threshold:** at least 27 of 29 carriers (93%) satisfy $D(R_n) \leq 0.25$.

---

## 4. Null Model (Frozen in NULLS_V2.md)

**Primary null:** Null N1 — unit-valued attractor scramble.
- 100 scrambles per carrier, seed 29, category-preserving.
- For each scramble, compute $\beta^\text{scr}(R_n)$ with random $h^\text{scr} \in U(n)$.
- For each scramble, compute $D^\text{scr}(R_n) = |\beta^\text{scr}(R_n) - \beta^\text{scr}(R_{10})|$ (note: null deviation is computed relative to the *same scramble*'s Z/10 value, to preserve fairness).
- For each scramble, compute M1 ($\tau^\text{scr}$), M2 ($R^{2,\text{scr}}$), M3 (fraction of carriers with $D^\text{scr} \leq 0.25$).

**Null distribution:** 100 values each of $\tau^\text{scr}$, $R^{2,\text{scr}}$, M3$^\text{scr}$.

**Secondary nulls:** N2 (shell permutation) and N3 (trend resample) reported but not part of pass/fail.

---

## 5. Pass / Fail Criteria (Frozen)

### 5.1 Primary pass criteria

The sprint **passes** if ALL of:

1. **Real $\tau \geq 0.35$** (monotonicity threshold met).
2. **Real $R^2 \geq 0.40$** (trend explains 40% of deviation variance).
3. **At least 27 of 29 carriers satisfy $D(R_n) \leq 0.25$** (deviation bounded).
4. **Real $\tau$ exceeds null $\tau$ mean by $\geq 2$ std deviations** (discrimination from N1).
5. **Real $R^2$ exceeds null $R^2$ mean by $\geq 2$ std deviations** (discrimination from N1).

### 5.2 Fail criteria

The sprint **fails** if ANY of:

- $\tau < 0.35$.
- $R^2 < 0.40$.
- More than 2 carriers have $D(R_n) > 0.25$.
- Null $\tau$ separation $< 2\sigma$.
- Null $R^2$ separation $< 2\sigma$.

### 5.3 Unclear outcome

- All three primary metrics (M1, M2, M3) pass on their own thresholds, but null separation for $\tau$ or $R^2$ is between 1σ and 2σ.

In this case: report as UNCLEAR, no invariant movement, note what a subsequent sprint would test.

---

## 6. Sigma Threshold Justification

S29 uses 2σ rather than S28's 3σ because:

- The anchored metric is a different kind of quantity from pointwise smoothness. Monotonicity and $R^2$ are aggregate statistics over 29 data points, not adjacent-pair summaries.
- The null model is tighter (category-preserving), so the null distribution is expected to be narrower — making the 2σ threshold comparable in statistical strength to S28's 3σ under a looser null.
- 2σ corresponds roughly to $p < 0.05$ one-tailed, which is an accepted threshold for primary-test significance in most fields.

This is frozen, not adjustable.

---

## 7. Anti-Tuning Rules

1. No parameter change after the first datum is scored.
2. No substitution of primary distance ($d_1$) with secondary ($d_2$) if $d_1$ fails.
3. No alternative attractor rule if the canonical $h = \max$ odd unit yields poor results.
4. No re-weighting of carriers or exclusions based on observed deviations.
5. No swapping Null N1 for Null N2 as the primary null.
6. No replacing Kendall's tau with Spearman's rho, Pearson's r, or any other monotonicity statistic.
7. The $R^2$ fit is linear; no alternative functional form (log, power, exponential) is substituted.
8. If $d_1$ ties exist (which they do), the tau calculation uses the standard tie-handling formula. No ad hoc grouping.

---

## 8. Deliverables

- `S29_CURVE_DATA.csv`: 29 rows; columns $n$, $\|U(n)\|$, $d_1$, $\beta$, $D$, in-bound $[D \leq 0.25]$.
- `S29_NULL_DATA.csv`: 29 × 100 = 2900 rows; columns $n$, scramble_id, $h^\text{scr}$, $\beta^\text{scr}$.
- `S29_SCORES.json`: real metrics M1/M2/M3, null distributions, sigma separations, sub-condition pass/fail, overall verdict.
- `S29_VERDICT.md`: one-paragraph determination.
- `S29_ANCHORED_ANALYSIS.md`: carrier-sorted-by-depth table, null comparison summary, residual discussion.

---

## 9. Three-Way Outcome Interpretation

**Outcome 1: PASS.** The anchored deviation curve hypothesis is supported. Basin ratio deviation grows lawfully with distance from the anchor, with monotonicity and reasonable linear-fit $R^2$, distinguishable from a unit-valued attractor scramble. The entry "attractor emerges as structural position, anchored" can be added to `INVARIANTS_BEYOND_TSML.md`. Note: this does NOT reverse S28's demotion; S29 is independent evidence of a different claim.

**Outcome 2: FAIL.** The rope-like structure is not present at the basin-ratio level, either because deviation is not monotone in depth ($\tau < 0.35$), or the fit is too poor ($R^2 < 0.40$), or deviations exceed the boundedness cap, or the null model reproduces similar behavior. The anchored-curve hypothesis does not apply to basin ratios on this family. Alternative invariants or alternative depth coordinates could be tested in a new sprint.

**Outcome 3: UNCLEAR.** Metrics pass, nulls are marginal. Finding reported without invariant movement. A follow-up sprint might extend the family or use tighter nulls.

---

## 10. Scope Boundaries

**What S29 tests:**
- One invariant (basin ratio).
- One depth coordinate ($d_1 = |U(n)| - 4$).
- One functional form class (monotone, linearly fittable).
- One null family (unit-valued attractor scramble).

**What S29 does not test:**
- Shell partition recovery under depth (separate invariant).
- Seam topology under depth (separate invariant).
- Non-ring carriers (not in the family).
- Alternative depth coordinates (frozen to $d_1$ for this sprint).
- Nonlinear functional forms (tested implicitly via modest $R^2$ threshold, but a separate sprint would explicitly fit nonlinear).

---

## 11. What S29 Cannot Establish (Even Under Full PASS)

- That the invariant transports to non-ring settings.
- That the deviation has physical meaning.
- That the specific functional form (linear $\hat{D}(d_1)$) is the "correct" description.
- That S28's original invariant claim is rehabilitated.

S29's outcome is narrow: does basin ratio grow lawfully with depth from the anchor? PASS says yes, FAIL says no, UNCLEAR says we can't tell. That is all.

---

## 12. What Moves On Outcome

- **PASS:** add new entry to `INVARIANTS_BEYOND_TSML.md` section "Confirmed transport in tested settings" reading: *Anchored deviation curve of basin ratio grows monotonically with unit-group-size depth, in the 29-carrier compatible subfamily, distinct from unit-scrambled null at 2σ.* S28's demotion for "attractor emerges" is NOT reversed — S28 and S29 tested different claims.
- **FAIL:** `LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md` gains a line under "Attempted transport, not confirmed" documenting this specific failure.
- **UNCLEAR:** note added to `LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md` but no column movement.

---

## 13. Integrity Commitment

S29 is run once against this frozen spec. The results are reported exactly as the spec computes them. No interpretation beyond the pre-registered outcomes is written into `S29_VERDICT.md`. If a genuinely novel observation appears during the run (e.g., a specific functional form emerges clearly), it is logged separately in `S29_FOLLOWUPS.md` for consideration in a new sprint, not acted on within S29.
