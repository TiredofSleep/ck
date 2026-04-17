# B1 Curve Analysis Addendum v1.0
## Deformation Layer on Top of the Frozen Benchmark Spec

---

## Purpose and Scope

**What this is.** A second analysis track that runs on top of B1-v1.0. It asks a different question from the core benchmark: when exact recovery bends under noise, does it bend lawfully or break arbitrarily?

**What this is not.** A modification of B1-v1.0. The benchmark spec, pass/fail criteria, anti-leakage rules, and low-noise strict failure condition are all unchanged. This addendum produces diagnostic output alongside the core benchmark output.

**Relation to B1-v1.0.**

- All B1-v1.0 requirements remain binding.
- All B1-v1.0 outputs remain required.
- Low-noise seed failure still produces overall FAIL.
- Curve metrics are computed and reported regardless of pass/fail outcome.
- Curve metrics do not affect the pass/fail verdict.

**The core intuition, translated.** The consistency may live in the curve. Even if pointwise exact recovery degrades, the trajectory of degradation itself can be structured: monotone, smooth, preserving class ratios, maintaining layer ordering. A structured degradation curve is evidence that the instrument has structural coherence, independently of the exact-recovery pass/fail.

---

## 1. Additional Per-Configuration Metrics

These are computed in addition to the B1-v1.0 metrics (A_h, A_σ, R_seam, P_seam, F_seam, A_rule, A_T, Z_null). They describe properties of the fitter's output, independent of ground truth where possible.

### 1.1 Properties of the recovered operator $\hat{T}$

| Metric | Definition |
|---|---|
| `attractor_fraction` | $\|\{(x,y) : \hat{T}(x,y) = \hat{h}\}\| / 100$ |
| `seam_density` | $\|\hat{S}\| / 100$ |
| `max_domain_fraction` | $\|\hat{S}_{\text{MAX}}\| / \|\hat{S}\|$ (0 if $\hat{S} = \emptyset$) |
| `add_domain_fraction` | $\|\hat{S}_{\text{ADD}}\| / \|\hat{S}\|$ (0 if $\hat{S} = \emptyset$) |

### 1.2 Seam topology summary

Construct the unordered seam graph $G_{\hat{S}}$ on vertex set $\{0, \ldots, 9\}$ with edges $\{x, y\}$ for each pair $(x, y) \in \hat{S}$ (ignoring direction; self-loops allowed if $(x, x) \in \hat{S}$).

| Metric | Definition |
|---|---|
| `seam_edges` | Number of unordered unique edges in $G_{\hat{S}}$ |
| `seam_vertices` | Number of vertices with at least one incident edge |
| `seam_components` | Number of connected components of $G_{\hat{S}}$ (excluding isolated vertices) |
| `seam_max_degree` | Maximum vertex degree in $G_{\hat{S}}$ |
| `seam_is_tree` | `true` if `seam_components == 1` AND `seam_edges == seam_vertices - 1` |
| `seam_is_forest` | `true` if `seam_edges == seam_vertices - seam_components` |
| `seam_diameter` | Longest shortest-path between any two vertices in the largest component (undefined if empty) |

### 1.3 Per-layer recovery counts

These use the ground-truth partition of $R \times R$ into the three layers ($D_0 = R^2 \setminus S_{\text{true}}$, $D_1 = S_{\text{MAX,true}}$, $D_2 = S_{\text{ADD,true}}$). They are computed by the scoring process.

| Metric | Definition |
|---|---|
| `C0_cells_recovered` | $\|\{(x,y) \in D_0 : \hat{T}(x,y) = T_{\text{true}}(x,y)\}\|$ — max 92 |
| `C1_cells_recovered` | $\|\{(x,y) \in D_1 : \hat{T}(x,y) = T_{\text{true}}(x,y)\}\|$ — max 6 |
| `C2_cells_recovered` | $\|\{(x,y) \in D_2 : \hat{T}(x,y) = T_{\text{true}}(x,y)\}\|$ — max 2 |
| `rho_C0` | `C0_cells_recovered / 92` |
| `rho_C1` | `C1_cells_recovered / 6` |
| `rho_C2` | `C2_cells_recovered / 2` |

### 1.4 Distance metrics

| Metric | Definition |
|---|---|
| `hamming_distance` | $\|\{(x,y) : \hat{T}(x,y) \neq T_{\text{true}}(x,y)\}\|$ — ranges 0 to 100 |
| `normalized_hamming` | `hamming_distance / 100` — equals $1 - A_T$ |

---

## 2. Curve Aggregation

For each noise level $p \in \{0.05, 0.15, 0.30\}$, aggregate across the 5 seeds.

For each metric $m$ listed in §1, compute:

| Aggregate | Definition |
|---|---|
| `mean_m@p` | arithmetic mean across seeds |
| `std_m@p` | sample standard deviation across seeds |
| `min_m@p` | minimum across seeds |
| `max_m@p` | maximum across seeds |

This produces three data points per metric (one per noise level), forming a three-point curve.

### 2.1 Curve representations

For each metric, produce two representations:

- **Table form:** 3 rows (p = 0.05, 0.15, 0.30), columns (mean, std, min, max).
- **Plot form:** x-axis = p_noise, y-axis = metric value, with mean line and min/max whiskers.

Plot files: PNG format, saved to `plots/` directory. Naming: `plots/curve_{metric_name}.png`.

---

## 3. Curve-Consistency Meta-Metrics

These are defined on the three-point curves and quantify how "lawful" the degradation is.

### 3.1 Monotonicity

For a metric $m$ expected to decrease with noise (e.g., `A_T`, `R_seam`, `rho_C0`):

$$\text{Monotonic}(m) := \begin{cases} 1 & \text{if } \overline{m}_{\text{low}} \geq \overline{m}_{\text{med}} \geq \overline{m}_{\text{high}} \\ 0 & \text{otherwise} \end{cases}$$

(using mean across seeds). An analogous definition with reversed inequalities applies to metrics expected to increase (e.g., `hamming_distance`, `seam_density` if the fitter over-flags).

**Report:** monotonicity score for `A_T`, `R_seam`, `P_seam`, `F_seam`, `rho_C0`, `rho_C1`, `rho_C2`, `A_rule`, `attractor_fraction`, `seam_density`, `hamming_distance`.

**Aggregate:** mean monotonicity score across the listed metrics.

### 3.2 Smoothness (Lipschitz-like ratio)

For a metric $m$ with values $(\bar{m}_{0.05}, \bar{m}_{0.15}, \bar{m}_{0.30})$:

$$s_1 = \frac{|\bar{m}_{0.15} - \bar{m}_{0.05}|}{0.10}, \quad s_2 = \frac{|\bar{m}_{0.30} - \bar{m}_{0.15}|}{0.15}$$

**Smoothness ratio:**

$$\text{Smoothness}(m) := \frac{\min(s_1, s_2)}{\max(s_1, s_2)} \in [0, 1]$$

(with `Smoothness = 1` if both slopes are 0; `Smoothness = 0` if one slope is 0 and the other is not).

A value near 1 indicates "smooth" degradation. A value near 0 indicates "kinked" or bifurcation-like behavior.

**Threshold:** Smoothness $\geq 0.30$ is "acceptably smooth." Below 0.30: flag as potential bifurcation.

### 3.3 Attractor persistence

$$\text{AttractorPersistence} := \frac{|\{(p, s) : \hat{h}_{p,s} = 7\}|}{15}$$

Across all 15 configurations. Expected value: 1.0 in lawful degradation.

### 3.4 Seam class ratio persistence

Let $r_{p,s} = |\hat{S}_{\text{MAX},p,s}| / |\hat{S}_{p,s}|$ (the MAX-domain fraction of the seam at config $(p, s)$). True value: 6/8 = 0.75.

$$\text{RatioPersistence} := 1 - \sqrt{\frac{1}{15} \sum_{p, s} (r_{p,s} - 0.75)^2}$$

(Root-mean-square deviation from the true ratio, flipped to a [0, 1] score.) Higher is better. A value $\geq 0.8$ indicates lawful preservation; lower indicates the fitter is mixing layer classifications.

### 3.5 Layer ordering stability

For each configuration $(p, s)$:
- Check whether $\rho_{C_0}(p, s) \geq \rho_{C_1}(p, s) \geq \rho_{C_2}(p, s)$.

$$\text{LayerOrdering} := \frac{|\{(p, s) : \rho_{C_0} \geq \rho_{C_1} \geq \rho_{C_2}\}|}{15}$$

Expected value: 1.0 if layer ordering is preserved across configurations. The interpretation is that larger-domain rules ($C_0$ covers 92 cells, $C_1$ covers 6, $C_2$ covers 2) remain more accurately recovered even under perturbation, consistent with their structural prominence.

### 3.6 Composite curve-consistency score

A single summary number:

$$\text{CCS} := \frac{1}{5}(\text{MeanMonotonicity} + \text{MeanSmoothness} + \text{AttractorPersistence} + \text{RatioPersistence} + \text{LayerOrdering})$$

CCS $\in [0, 1]$. Interpretation bands:
- $\text{CCS} \geq 0.85$: **Lawful degradation.** Even where exact recovery fails, the curve shape is consistent.
- $0.60 \leq \text{CCS} < 0.85$: **Partially lawful.** Some structural properties preserved; others not.
- $\text{CCS} < 0.60$: **Unstructured degradation.** No clear lawful pattern in how recovery fails.

**Note:** CCS is a diagnostic number, NOT a pass/fail criterion. The B1 pass/fail verdict follows the core spec.

---

## 4. Interpretation Guide

### 4.1 What "lawful degradation" looks like

A structurally coherent instrument, applied to data with increasing noise, produces:
- Monotone decrease in exact-recovery metrics.
- Smooth (bounded slope ratio) transitions between noise levels.
- Stable attractor identification across all configurations.
- Preserved seam class ratio (MAX vs ADD pairs in consistent proportions).
- Preserved layer ordering (larger-domain rules more robustly recovered).

If all of these hold: the instrument is "structurally coherent" even where exact recovery falters.

### 4.2 What "chaotic collapse" looks like

An instrument with fragile internal consistency produces:
- Non-monotone recovery (accuracy increases then decreases then increases).
- Sharp kinks or bifurcations in the curves.
- Attractor identification flipping between noise levels.
- Seam class ratio swinging widely across configurations.
- Layer ordering violated (e.g., ADD-layer recovery better than canonical recovery).

If these patterns appear: the instrument is memorizing, not detecting structure.

### 4.3 Specific diagnostic patterns

| Pattern | Likely cause |
|---|---|
| Monotone, smooth, CCS > 0.85 | Lawful degradation; instrument is structurally coherent |
| Monotone but kinked (low smoothness) | Threshold-driven bifurcation in fitter |
| Non-monotone $A_T$ | Fitter uses variance-sensitive decision rule; noise can help or hurt |
| `attractor_fraction` drifts from 0.73 | Fitter mis-classifies seam vs default |
| `seam_density` grows rapidly | Fitter over-flags under noise |
| `seam_density` stays small but $R_{\text{seam}}$ drops | Fitter too conservative under noise |
| `rho_C0 < rho_C2` at any noise level | Fitter preferentially detects tiny domains over dominant ones — suspicious |
| `seam_is_tree` holds at all levels | Topology preserved; strong structural evidence |
| `seam_is_tree` false at med/high noise | Topology distorts with noise (expected beyond some level) |

---

## 5. Required Outputs

### 5.1 Data products

- `scores/per_config_metrics.json` — one row per configuration, all metrics from §1 plus B1-v1.0 metrics.
- `scores/curves.json` — aggregated curves per metric, three data points each.
- `scores/curve_consistency.json` — all meta-metrics from §3.
- `plots/curve_{metric}.png` — one plot per metric (at minimum: `A_T`, `R_seam`, `P_seam`, `rho_C0`, `rho_C1`, `rho_C2`, `attractor_fraction`, `seam_density`, `seam_edges`, `hamming_distance`).

### 5.2 Required document: `B1_CURVE_ANALYSIS.md`

Produced by the scoring pipeline after all B1 configurations are fit and scored.

**Required sections:**

1. **Header.** Spec version, run timestamp, fitter name+version, overall B1 verdict (from core spec).
2. **Curve tables.** For each of the listed metrics: 3-row table (p = 0.05, 0.15, 0.30) with mean, std, min, max.
3. **Plots.** Inline references to `plots/curve_*.png`.
4. **Meta-metrics table.** All §3 values with interpretations.
5. **Lawfulness paragraph.** ONE paragraph answering: **"Does the structure degrade lawfully, or collapse chaotically?"** The paragraph must cite specific numerical findings (monotonicity score, CCS, specific curve shapes). No interpretation beyond what the numbers support.
6. **Divergence from ground truth.** If CCS < 0.85, list which specific meta-metrics fell below threshold and what that indicates diagnostically.
7. **Note on independence from pass/fail.** Explicit statement that the curve analysis is diagnostic and does NOT alter the B1 pass/fail verdict.

### 5.3 Required short note: `B1_TOWER_STABILITY_NOTE.md`

One-page note answering: **"Is the recovered tower stable as a deformation family under noise?"**

Required content:
- Summary of CCS.
- Which meta-metrics were preserved; which degraded.
- One sentence on whether the instrument is "structurally coherent" per §4.1.
- Explicit separation from pass/fail.
- Recommendation for next step (proceed to B2, or diagnose before B2).

---

## 6. Integration with B1 Scoring Pipeline

The curve analysis runs as an additional step in the scorer process:

```
Step 1: generate  (as in B1-v1.0)
Step 2: seal      (as in B1-v1.0)
Step 3: fit       (as in B1-v1.0)
Step 4: score     (as in B1-v1.0) — produces per-config scores
Step 4b: curves   (NEW) — produces curves.json, curve_consistency.json, plots/
Step 5: report    (as in B1-v1.0) — produces summary.json
Step 5b: curve_report (NEW) — produces B1_CURVE_ANALYSIS.md and B1_TOWER_STABILITY_NOTE.md
```

Step 4b uses the same ground-truth files as Step 4. It does not require additional fitter runs. It only aggregates per-configuration outputs into curves.

---

## 7. Discipline Reminders

- **Do not change the frozen B1 spec.** This addendum is analysis on top of frozen inputs and outputs.
- **Do not tune the fitter to improve curve metrics.** Tuning to pass either pointwise metrics or curve metrics constitutes spec modification.
- **Curve metrics are diagnostic, not pass/fail.** A run with CCS = 0.95 but a low-noise seed failure is still overall FAIL per B1-v1.0.
- **Even in failure, report curves.** A failed run with lawful degradation is more informative than a failed run with chaotic collapse; both should be made visible.
- **No post-hoc narrative.** The lawfulness paragraph must cite the numerical results directly. If monotonicity is violated, say so. If CCS < 0.60, do not frame the degradation as "partially lawful" — call it unstructured.

---

## 8. What This Addendum Achieves

The core benchmark asks: **does the instrument recover exact structure at each noise level?**

The curve analysis asks: **does the instrument bend coherently when pushed?**

These are independent tests of structural validity. An instrument can pass pointwise exact recovery yet produce a chaotic curve (overfitting to specific data, brittle to noise). An instrument can fail pointwise recovery at high noise yet produce a lawful curve (structurally coherent but noise-limited).

**The combined result — pass/fail verdict plus curve-consistency score — gives a two-axis picture of instrument behavior that neither axis alone provides.**

Pass + high CCS: strongest case for structural validity.
Pass + low CCS: suspicious; instrument may be memorizing or overfit.
Fail + high CCS: instrument is structurally coherent but noise-limited; may need larger $N$ or different encoding.
Fail + low CCS: the instrument has a genuine structural defect, not just a resolution problem.

---

## Version Control

**Addendum version:** v1.0.
**Companion to:** B1-v1.0 spec.
**Both documents frozen.** Changes require version bump and full re-evaluation.
