# Sprint 28 Pre-Registration
## Curve Recovery of Shell/Basin Structure Under Controlled Deformation

---

**Status:** FROZEN before data collection.
**Version:** S28-v1.0.
**Authored:** prior to any runs, analyses, or exploratory fits.
**Change policy:** once any datum is scored against this spec, the spec cannot be edited. Amendments require a version bump (S28-v1.1) and a written note stating what changed and why. Results scored against v1.0 must be reported against v1.0.

---

## 1. Invariant Being Tested (Exactly One)

**Invariant under test:** *attractor and basin ratio across the compatible-ring family form a structured curve.*

**Precise statement.** For each ring $R = \mathbb{Z}/n\mathbb{Z}$ in the tested subfamily, define:

- $h(R) :=$ the largest odd unit of $R$ (the structural attractor candidate).
- $B(R) := \{(x, y) \in R \times R : C_0(x, y; R, h(R), \sigma_R) = h(R)\}$ where $C_0$ is the canonical construction and $\sigma_R(u) = v_2(3u+1)$ is the shell partition.
- $\beta(R) := |B(R)| / n^2$ — the **basin ratio**.

The invariant is the joint structure: $(h(R), \beta(R))$ as $n$ varies over the tested carrier family.

**What "curve" means here.** The invariant is tested at the level of the curve $n \mapsto (h(R_n), \beta(R_n))$, not at the level of specific values. Specifically, we test whether:

- **(a)** $h(R_n)$ follows a stated structural rule across carriers (monotone as a function of $n$, with a specific local formula).
- **(b)** $\beta(R_n)$ stays within a pre-specified band across the family.
- **(c)** $\beta(R_n)$ varies lawfully (monotone trend or bounded deviation) rather than chaotically.

This is a **single narrow test.** No other invariant is evaluated in this sprint. Shell partition recovery, residue-tower depth, seam topology, and paired-operator tests are out of scope.

---

## 2. Deformation Family

**Family:** the **compatible ring subfamily** — the 35-member divisibility-compatibility family established in `RING_RANKING_TABLE.md`, restricted to the subset where:
- $n$ is even (excludes no family members; all 35 are even by property);
- $|U(n)| \geq 4$ (excludes trivial cases Z/4, Z/6 which have $|U| = 2$);
- $n \leq 300$ (the set bounded by the original survey).

**Tested carriers (fixed list, frozen):**
```
10, 14, 18, 20, 22, 26, 28, 30, 34, 36, 38, 42, 44, 46, 50,
54, 58, 62, 66, 68, 70, 74, 78, 82, 86, 90, 94, 98, 100
```

*Note:* This subset is 29 even integers between 10 and 100. The full 35-member family up to $n = 300$ is larger; the sprint restricts to this subset for tractability and to avoid over-weighting large-$n$ tail.

**Why this family:** the canonical construction $C_0(R, h, \sigma)$ is well-defined on every ring in the compatibility family without needing a reference TSML table. The "deformation" here is "change of local chart by changing the ring" — which is precisely what the framing reset identified as the relevant kind of deformation.

**What is NOT the deformation family:**
- Noise deformation (covered in B1 and the B1 curve addendum).
- Wobble deformation (covered in B2).
- Synthetic shell-native systems (covered in B1 benchmark).

This sprint tests deformation under **carrier change**, which is the cleanest test of grammar transport because it changes the object the instrument is looking at.

---

## 3. Recovery Metric (Exact)

Three sub-metrics, combined into one pass/fail vector.

### 3.1 Attractor rule concordance

**Pre-specified hypothesis:** for every $R_n$ in the tested family, $h(R_n) = \max\{u \in U(n) : u \text{ odd}\}$.

**Score:**
$$
A := \frac{|\{n \in \text{family} : h(R_n) = \max \text{ odd unit of } U(n)\}|}{|\text{family}|}
$$

Requires $A = 1.0$ to pass. Any single failure disqualifies this sub-metric.

### 3.2 Basin ratio band

**Pre-specified hypothesis:** for every $R_n$ in the tested family, $\beta(R_n) \in [0.60, 0.95]$. The band is chosen to exclude trivial (all-collapse: $\beta = 1$) and degenerate (no-collapse: $\beta = 0$) regimes, and to bracket Z/10's observed $\beta = 0.73$ generously on both sides.

**Score:**
$$
B_{\text{band}} := \frac{|\{n \in \text{family} : 0.60 \leq \beta(R_n) \leq 0.95\}|}{|\text{family}|}
$$

Requires $B_{\text{band}} \geq 0.80$ to pass (at least 24 of 29 carriers in-band).

### 3.3 Curve smoothness (monotonicity-in-trend)

**Pre-specified hypothesis:** $\beta(R_n)$ does not vary chaotically across the family — specifically, the mean absolute difference between consecutive $\beta$ values (in the sorted-by-$n$ family) is bounded.

Let $\beta_1 \leq \beta_2 \leq \ldots \leq \beta_{29}$ be $\beta(R_n)$ values indexed by the sorted carrier list. Define:
$$
\Delta := \frac{1}{28} \sum_{i=1}^{28} |\beta(R_{n_{i+1}}) - \beta(R_{n_i})|
$$

where the sum is over adjacent pairs in the carrier-order (not sorted by $\beta$).

**Score:** $C_{\text{smooth}} := \Delta$.

**Requirement:** $C_{\text{smooth}} \leq 0.10$ to pass. A mean step of 0.10 between adjacent-carrier $\beta$ values is the upper limit; above this, the curve is deemed unstructured.

---

## 4. Null Model

**Null model:** *scrambled-ring baseline.*

For each $n$ in the family, construct a **scrambled canonical operator** $C_0^\text{scr}(R_n)$:
- Use the same carrier $R_n$.
- Use a uniformly random permutation $\pi$ of $\{0, 1, \ldots, n-1\}$ as a "shell partition" — assign each non-zero element a shell label uniformly at random from $\{1, 2\}$.
- Choose the attractor $h^\text{scr}$ uniformly at random from $\{0, \ldots, n-1\}$.
- Compute the canonical construction with these scrambled inputs.
- Compute $\beta^\text{scr}(R_n) := |\{(x,y) : C_0^\text{scr}(x, y) = h^\text{scr}\}| / n^2$.

Repeat for 100 random scrambles per carrier. Report the null distribution of:
- Attractor rule concordance (expected: low, since random $h^\text{scr}$ rarely matches max-odd-unit).
- Mean basin ratio.
- Smoothness across carriers (expected: high $\Delta$, since scramble is independent across carriers).

**Why this null:** it answers the question "is the observed pattern just a consequence of doing any construction, or is it specific to the canonical grammar?" If a randomly-parameterized construction produces the same curve shape, the invariant is not transporting — it is a structural artifact of the construction type.

---

## 5. Pass / Fail Thresholds

### 5.1 Sprint-level pass criteria

The sprint **passes** if ALL of:

1. $A = 1.0$ (attractor rule holds for every carrier).
2. $B_{\text{band}} \geq 0.80$ (basin ratio within band for at least 80% of carriers).
3. $C_{\text{smooth}} \leq 0.10$ (mean step ≤ 0.10).
4. Real $C_{\text{smooth}}$ is at least 3 standard deviations below the null mean $C_{\text{smooth}}$.
5. Real $A$ is strictly greater than the mean null $A$ by at least 0.40.

### 5.2 Sprint-level fail criteria

The sprint **fails** if ANY of:

- $A < 1.0$ at any carrier.
- $B_{\text{band}} < 0.80$.
- $C_{\text{smooth}} > 0.10$.
- $C_{\text{smooth}}$ is within 3 std devs of the null mean.
- Real $A$ advantage over null $A$ is less than 0.40.

### 5.3 Unclear outcome

- $A = 1.0$ AND $B_{\text{band}} \geq 0.80$ AND $C_{\text{smooth}} \leq 0.10$, BUT the null comparison is marginal (real advantage is 0.40–0.50, or std-dev separation is 2–3σ). In this case: report the finding, flag as unclear, do NOT claim pass.

---

## 6. Anti-Tuning Rule

1. **No parameter of this spec may be changed after any datum has been scored against it.** This includes: the carrier list, the basin-ratio band [0.60, 0.95], the smoothness threshold 0.10, the pass thresholds in §5.1, the null model parameters.
2. **No carrier may be excluded from scoring for being "atypical."** All 29 listed carriers count. If a carrier's $\beta$ falls outside the band, it counts as out-of-band. The band threshold is not adjusted to accommodate.
3. **The attractor rule is frozen as "max odd unit of U(n)."** If the rule fails on a carrier, the sub-metric $A$ fails. Alternative rules may be tested in a *separate* sprint (S28-alt), not as a post-hoc rescue.
4. **Null comparisons must use the exact scrambling procedure in §4.** 100 scrambles per carrier, uniform random permutations, no conditional filtering.
5. **Fitter determinism is required.** Given the same ring $R_n$, the canonical construction $C_0$ must produce the same operator every run. No stochasticity within the fitter.
6. **No parallel "exploratory" tests may be run during the sprint.** Exploratory analyses go in a separate file (`S28_EXPLORATORY.md`) and are explicitly labeled as non-sprint. They do not affect pass/fail.

---

## 7. Required Deliverables

- `S28_CURVE_DATA.csv` — one row per carrier, columns: $n$, $h(R_n)$, $\beta(R_n)$, is_in_band (0/1), adjacent-step $|\Delta\beta|$.
- `S28_NULL_DATA.csv` — one row per (carrier, scramble) pair, columns: $n$, scramble_id, $h^\text{scr}$, $\beta^\text{scr}$.
- `S28_SCORES.json` — final scores $A$, $B_{\text{band}}$, $C_{\text{smooth}}$; null statistics; pass/fail verdict.
- `S28_CURVE_ANALYSIS.md` — one page: summary table, three pre-registered hypotheses tested, pass/fail verdict per §5, explicit statement whether the invariant transports.

---

## 8. Three-Way Outcome Interpretation

**Outcome 1: PASS.** The $(h, \beta)$ curve across the compatible ring family is structured — attractor rule holds exactly, basin ratio stays in band, curve is smooth. Transport invariant confirmed for this deformation family. The invariant is tagged "confirmed in ≥ 2 settings" (Z/10 alone + compatible family).

**Outcome 2: FAIL.** One or more of: attractor rule doesn't generalize, basin ratios are out of band on too many carriers, curve is chaotic, null comparison is not strong enough. The invariant does NOT transport under this deformation family. It is demoted to "Z/10-local," and the INVARIANTS_BEYOND_TSML.md entry for "attractor emerges as structural position" is moved to left column of LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md.

**Outcome 3: UNCLEAR.** Real metrics pass per §5.1 but null separation is weak. Finding is reported with "unclear" tag. No movement on the local/transferred split. A follow-up sprint (S29) is proposed with either a stronger null model or an expanded carrier family.

---

## 9. Out-of-Scope (Explicit Deferrals)

These are NOT tested in Sprint 28. Attempting to evaluate them is out of scope.

- **Shell partition recovery.** Covered by Sprint 26 / future label-recovery sprint.
- **Residue tower depth.** Ring-specific (may be different depth on different rings).
- **Seam topology generalization.** Separate sprint.
- **Curve dynamics (iterative orbits).** Separate sprint (the "orbit-clustering Sprint 28b" previously discussed).
- **Transport to non-ring settings.** Not a ring-carrier family — out of scope.
- **STD bridge.** Explicitly deferred pending Moves 2, 3, 4 of the STD audit.

If during execution any of these become attractive to investigate, they are logged in `S28_FOLLOWUPS.md` and NOT acted upon within Sprint 28.

---

## 10. Run Protocol

1. Compute $h(R_n)$ and $\beta(R_n)$ for each of the 29 carriers.
2. Write `S28_CURVE_DATA.csv`.
3. Run 100 scrambles per carrier; compute null statistics.
4. Write `S28_NULL_DATA.csv`.
5. Apply §5 thresholds; compute verdict.
6. Write `S28_SCORES.json` and `S28_CURVE_ANALYSIS.md`.
7. Report.

Implementation should be a single script, deterministic, reproducible from the spec. No human judgment inside the run — only at the reporting step.

---

## 11. What This Sprint Does Not Establish

Even under full PASS, this sprint does NOT establish:

- That the invariant transports to non-ring settings.
- That the invariant has any physical interpretation.
- That the curve has any specific functional form beyond "bounded and smooth."
- That other TSML/BHML invariants transport (they are out of scope).

A PASS means only: *across this specific deformation family, this specific invariant behaves consistently under the pre-registered metric and beats the pre-registered null.* That is the narrow claim, which is exactly what the framing reset asked for.

---

## 12. What This Sprint Establishes Even Under FAIL

A FAIL would be a genuine finding:

- It would demote the "attractor emerges as structural position" invariant from the transportable-grammar column to the Z/10-local column.
- It would suggest that Sprint 21's observed pattern (attractor = max odd unit across 4 carriers) was small-sample coincidence, not a transport invariant.
- It would sharpen the question: *which* invariants actually transport, if not this one?

Either outcome moves the investigation forward. That is the point of pre-registration.
