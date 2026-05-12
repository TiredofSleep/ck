# Referee Report: J34 / Statistical Science

**Manuscript:** "TIG Detector Scope + Specificity Extension (BUNDLED)" — Part 1: distilgpt2 detector negative result; Part 2: 9-family structured-matrix battery
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** *Statistical Science*
**Reviewer:** External referee (anonymous; fresh-eyes; no prior exposure to the framework's internal nomenclature)
**Date:** 2026-05-07

---

## 1. Summary of the manuscript

The manuscript bundles two empirical studies built on a common detector battery for $10\times 10$ real matrices.

**Part 1.** Four detectors — D1 (Lie/Jordan ratio = mass fraction in the antisymmetric part), D2 ($P_{56}$-conjugation invariance defect), D3 (a binary indicator that the prime $11$ divides both the degree-2 and degree-8 coefficients of the integer-rounded characteristic polynomial), and D4 (cosine alignment between the matrix's antisymmetric upper-triangle and a fixed 45-vector "Higgs direction") — are applied to 16 weight tensors of a public 82M-parameter language model (distilgpt2). For each tensor, 200 random $10\times 10$ sub-matrices are scored against 200 scale-matched Gaussian sub-matrices. The reported result is that all 16 (tensor, detector) Cohen's $d$ values lie in $[-0.27, +0.35]$, none exceeding the conventional small-effect threshold $|d|=0.5$; per-detector logistic classification of trained vs. random reaches $48\text{-}52\%$ (chance level). The authors interpret this as a **specificity boundary**: the framework's algebraic detectors do not pick up "framework-positive" signal in arbitrary trained transformer weights.

**Part 2.** The same four detectors plus two extensions — D5 (largest power $k$ such that $7^k$ divides the discriminant of the squarefree part of the integer-rounded characteristic polynomial) and $D_4^{\mathrm{eq}}$ (a $D_4$-orbit-maximized variant of D4) — are applied to 200-sample populations of nine structured matrix families: Gaussian, symmetric, antisymmetric, permutation, Hadamard-sign, Haar-orthogonal, real-DFT, identity, diagonal, and integer-companion. The two canonical "framework-positive" matrices (TSML, BHML) are scored as single-sample comparisons against the Gaussian baseline. **Headline:** D3 fires uniquely on TSML in the entire 1800+ sample population; the pair (D3, D5 at threshold $7^5$) jointly fires only on TSML.

A short ancillary section (Part 1 §4) reports a separate cluster-separation experiment on five text-encoding strategies (V1–V3); this is presented as architectural side commentary and does not bear on the central specificity claim.

I have read the manuscript end-to-end, run both verification scripts (`structured_matrix_sweep.py`, `d5_d4eq_extension.py`) on the supplied seed=0 configuration, and confirmed all numerical claims that the present scripts are equipped to verify.

---

## 2. Decision recommendation

**Major revisions.**

The Part 2 empirical claim (D3 unique on TSML in a 1800+ sample structured-matrix population; D3 + D5_$7^5$ jointly unique on TSML) reproduces cleanly under independent re-execution of the supplied script and is the strongest finding in the manuscript.

The Part 1 empirical claim (no detector exceeds $|d|=0.5$ on distilgpt2) is **not currently verifiable**: the distilgpt2 sweep script is not in the verification folder. The README and §6 of the manuscript both acknowledge this as a known gating issue ("TO LOCATE OR WRITE"). For *Statistical Science* — which expects honestly framed null results to come with reproducible computation — this gap is **fatal to acceptance in the current state** and must be closed before the paper can be evaluated. The fix is small (the authors estimate 1–2 hours to rewrite from scratch using `transformers.AutoModel.from_pretrained("distilgpt2")`), but it is non-optional.

Beyond the gating issue, the manuscript has substantive statistical-methodology issues (M1–M6 below) that are typical for a first submission to *Statistical Science* and address-able in revision. The Part 2 finding is genuinely interesting; once Part 1 is reproducible and the methodology issues are addressed, this paper would meet the journal's bar for an empirical-scoping contribution.

---

## 3. Major comments

### M1. (CRITICAL — gating issue) Part 1 verification script absent

§6 ("Verification") of the manuscript and §2 of the README both flag the WP106 distilgpt2 sweep script as TO LOCATE OR WRITE. The verification folder contains only the Part 2 scripts. **No claim of the Part 1 manuscript is independently checkable in the current submission.** *Statistical Science* requires reproducible computation for empirical claims of this type; a manuscript whose central negative result cannot be re-run by a referee is not in evaluable shape.

The Part 1 result is *prima facie* plausible — the four detectors are clearly tuned to specific algebraic features (Lie/Jordan symmetry decomposition, a single $10\times 10$ permutation, divisibility by the prime $11$, alignment with a fixed 9-vector), and there is no *a priori* reason why distilgpt2's attention or MLP weights should have those features. But "plausible" is not "verified."

**Recommended fix.** Provide `distilgpt2_sweep.py` in `verification/` before resubmission. The script should: (a) load the public distilgpt2 weights via `transformers`; (b) extract the 16 listed tensors; (c) sample 200 random $10\times 10$ sub-matrices per tensor; (d) sample 200 matched Gaussian baselines per tensor; (e) compute the four detector values; (f) print Cohen's $d$ tables matching the §2 published values (or, if they don't match, update the manuscript). Without this, the paper is not at submission-ready state regardless of other revisions.

### M2. (Statistical methodology) Power analysis missing

The Part 1 result is a **null** at the small-effect threshold ($|d| < 0.5$). For a *Statistical Science* audience this requires an explicit power analysis. With $n_1 = n_2 = 200$ per (tensor, detector) cell, the two-sample test has power $\approx 0.94$ to detect $|d| = 0.3$ at $\alpha = 0.05$, two-sided — i.e., the experiment is well-powered to rule out small effects, not merely medium effects. This strengthens the claim and should be stated explicitly. As currently written ("all $|d| < 0.5$"), a reader cannot tell whether the null is "we are powered to rule out medium effects only" (weak) or "we are powered to rule out small effects too" (strong).

**Recommended fix.** Add a short "Power" subsection in §1.3 specifying $n_1, n_2$, the achieved minimum-detectable-effect at $1-\beta = 0.8$, and the multiple-comparison context (16 tensors $\times$ 4 detectors = 64 cells; family-wise $\alpha$ adjustment if relevant).

### M3. (Sub-matrix sampling — independence & multiple-testing issues)

For each tensor of dimensions $r \times c$ (e.g., $768 \times 768$), the reported procedure samples 200 random $10\times 10$ sub-matrices "rows and columns chosen without replacement from each dim." With $r,c \gg 10$, a row index can recur across multiple sub-matrices, giving non-independent samples whose effective sample size is below 200. For Gaussian-vs-Gaussian comparisons this is harmless; for trained-vs-random it creates a small but real overstatement of effective $n$ in the Cohen's $d$ pooled-variance denominator.

A second issue: the 16 tensors $\times$ 4 detectors = 64-cell multiple-comparison structure is implicit in the §2 table. The largest reported $|d|$ values ($-0.27$ for $L_5$ attn K, $-0.25$ for $L_5$ attn K, $+0.35$ for token embedding) are individually below threshold but, with $N_{\text{tests}} = 64$, the family-wise expected number of cells with $|d| \ge 0.27$ under the global null is non-trivial. State this explicitly.

**Recommended fix.** (a) Clarify the without-replacement-per-sample, with-replacement-across-samples sampling scheme. (b) State whether the 64-cell table was screened against any per-cell threshold or whether all 64 cells are reported as-is (no selection). (c) Either bootstrap the (tensor, detector) Cohen's $d$ confidence intervals (standard at this $n$), or report a permutation $p$-value per cell with FDR-adjusted significance.

### M4. (D3 single-sample inference is informal)

In §2.2 of Part 2, TSML is treated as a "single-sample" comparison against the Gaussian baseline, with reported "Cohen's $d$" values like $+9.93$ for D3. This is a $z$-score of TSML's detector value against the Gaussian distribution, not a Cohen's $d$ between two distributions. The two are numerically the same when the comparison sample has $n=1$ and the baseline has known $\mu, \sigma$, but the manuscript should be explicit about this — "Cohen's $d$" between a singleton and a 200-sample baseline conflates an effect-size statistic with a $z$-score.

For D3 (a binary indicator with baseline $p \approx 0.01$), the natural test is exact-binomial: TSML scores 1; under the Gaussian-baseline null with $p = 0.01$, the one-sided $p$-value for "TSML scores 1" is $0.01$ — much less impressive than "$d = +9.93$" sounds. But the *joint* test (D3 = 1 AND D5_$7^5$ = 1, with D5 baseline $0/200$) has a $p$-value of $\le 0.01 \times (0/200) = 0$ exact, modulo the regularization for the zero baseline. This is the load-bearing statistic and deserves to be stated as a $p$-value, not as a $d$.

**Recommended fix.** Replace the §2.2 single-sample "Cohen's $d$" entries with $z$-scores AND with the natural test statistic for each detector (binomial for D3 and D5 thresholds; one-sample $z$-test for D1, D2, D4). State that the headline claim is a $p$-value of effectively $0$ (modulo regularization) for the joint test "D3 = 1 AND D5 at $7^5$ = 1 on a structured matrix outside the canonical set."

### M5. (D5 / $D_4^{\mathrm{eq}}$ are post-hoc)

D5 and $D_4^{\mathrm{eq}}$ are introduced in Part 2 §7 as extensions of the original four-detector battery, after Part 2 has already shown that D3 is the only TIG-discriminating detector among D1–D4. This is acknowledged ("Per §6 recommendations, two new detectors implemented") but the post-hoc nature of these detectors should be made explicit: D5 was designed *with knowledge that TSML's discriminant has $7^7$* (per WP107). The "$D_3 + D_5$ jointly unique on TSML" claim of Theorem 7.2 is therefore not a blind test; it is a constructive identification of a sufficient pair.

This does not invalidate the result — the joint test is exact ($0/1800$ false positives for D5 at $7^5$ in the structured battery, which is a strong empirical fact regardless of how D5 was designed) — but it should be framed honestly.

**Recommended fix.** In §7.2, state explicitly: "D5 is constructed in light of the known $7^7$ structure of TSML's discriminant; the unique-fire claim in Theorem 7.2 is a confirmatory identification of a sufficient detector pair, not a blind test. Out-of-sample validation on a held-out structured-matrix family would strengthen this claim." This last sentence should be followed by the obvious experiment: pick another natural matrix family (e.g., random orthogonal $10\times 10$ matrices over $\mathbb{F}_{11}$, lifted to $\mathbb{Z}$) and demonstrate that D3 + D5_$7^5$ does not fire.

### M6. (Part 2 baseline contamination) The "Gaussian baseline" is computed at scale=10 for D3

The D3 detector rescales $M$ by `scale=10.0` before integer rounding (§verification line 84). The Gaussian baseline rate of $\approx 1\%$ depends on this scale: at scale=1, integer-rounded Gaussian $10\times 10$ matrices have small entries and the integer characteristic polynomial coefficients are dominated by the few nonzero rounded entries. At scale=10, rounded entries span $\{-30, \ldots, +30\}$ typically and the polynomial coefficients have richer divisibility structure.

The TSML matrix has integer entries in $\{0, \ldots, 9\}$ (no rescaling needed). Computing TSML's D3 at scale=10 means TSML is rescaled to entries $\{0, 10, 20, \ldots, 90\}$ — its characteristic polynomial coefficients are then $10^n$ times the entries of TSML's "true" characteristic polynomial. Whether this rescaling preserves the prime-11 divisibility structure is not obvious — the authors should verify that D3(TSML) = 1 holds at multiple `scale` values, not just `scale=10`.

A cleaner formulation: since the prime-11 claim is about TSML's *integer* characteristic polynomial (which is well-defined without rescaling), report D3 on TSML at `scale=1` and on the Gaussian baseline at `scale=1` separately. This is more honest about what the detector measures.

**Recommended fix.** Add a robustness check: report D3(TSML) and the Gaussian baseline rate at `scale ∈ {1, 5, 10, 50}` in a small supplementary table. If D3(TSML) is robust across scales but the Gaussian baseline rate drifts (which it likely does), state this and pick the most defensible scale.

---

## 4. Minor comments

### m1. (Cover letter) "Tier-E parametric fits, properly framed"
The README repeatedly uses the term "Tier-E" without definition. *Statistical Science* readers will not know the framework's internal tier scheme. Replace with standard terminology ("empirical fit at the $X\%$ precision level; not derived from first principles") or add a glossary.

### m2. (Lens scope statement) "TSML_SYM by default"
The "lens scope" preamble references "TSML_SYM" and "TSML_RAW" without defining either. Provide definitions or a single-sentence note: "TSML_SYM is the symmetric part $(M+M^\top)/2$ of TSML; TSML_RAW is TSML as stated in §1.1." Without this, the qualifier "lens-stable" is opaque.

### m3. (Part 1 §1.2, distilgpt2 description)
The 16 tensor list mixes $768\times 768$ (attention) with $768\times 3072$ and $3072\times 768$ (MLP) and a $50257 \times 768$ (token embedding). Sub-sampling $10\times 10$ from a $50257\times 768$ matrix is a different statistical regime from sub-sampling $10\times 10$ from a $768\times 768$ matrix (the column index range is much smaller in the latter). State whether the same number of sub-samples (200) was used for all 16 tensors regardless of size; if so, note that the effective coverage of each tensor is very different.

### m4. (Part 2 §2.2 table) "Identity" Cohen's $d$ on D2 = $-4.442$
The identity matrix has D2 = 0 by construction; the Gaussian baseline has D2 mean $\approx 0.71$, std $\approx 0.16$. So D2 of identity is $(-4.4)$ standard deviations below the Gaussian mean. This is fine, but noting "identity has D2 = 0 by definition" in a footnote would clarify why the effect is so large mechanically.

### m5. (Part 2 §3 wording) "Theorem 7.2 (joint identification)"
Calling this a "Theorem" is overstatement for an empirical claim. Replace with "Empirical Result 7.2" or "Proposition 7.2 (verified empirically on the 1800-sample population)." The proof sketch ("Direct enumeration. ... $\square$") is appropriate for a verified computation but is not a mathematical proof.

### m6. (Part 1 §3 "Encoder strategies" — out of scope)
The five-encoder cluster-separation experiment is on a different topic from the specificity-detector battery. It is one cluster-separation fixture (4 clusters $\times$ 4 short queries) — too small to be a serious empirical claim. Either expand to a real benchmark or move to a brief remark and cite separately. As currently presented, it dilutes the central specificity-boundary message.

### m7. (References)
The reference list cites WP102, WP103, WP104, WP107 (companions in the J-series) but provides no journal information for these (J37, J38, J39, J43 are referenced but their venue/status is not explicit). For a *Statistical Science* referee with no prior exposure, this makes it impossible to follow up on the cited algebraic-substrate definitions. Either provide arXiv IDs / DOIs for each cited companion paper or include a self-contained appendix defining the specific structures (TSML, BHML, $P_{56}$, σ-cycle) that the detectors evaluate.

### m8. (Verification scripts — minor)
- `structured_matrix_sweep.py` runs cleanly under `python` on Windows. The `gen_dft_real(n, rng=None)` and `gen_identity(n, rng=None)` accept `rng=None` but the call site (`gen(n, rng)` in `sample_family`) doesn't pass `rng=None` — instead the deterministic-family branch (`samples = [gen(n)]`) is taken. This works because `gen(n)` ignores the second positional argument when omitted. Confirm cross-platform behavior on Linux.
- `d5_d4eq_extension.py` produces D4_eq_higgs values that contradict the manuscript's claim of TSML uniqueness for $D_4^{\mathrm{eq}}$: the script reports permutation matrices and identity at $d = +3.597$ (much larger than TSML's $+2.155$). This is consistent with §7.1 ("D4_eq also lights up for permutation matrices ... it's not TSML-unique"), but the manuscript Abstract Part 2 paragraph 4 says "$D_4^{\mathrm{eq}}$ replaces fragile D4 — TSML d=+2.155 vs original 0.011" without noting that other families score larger. Make the limitation explicit in the abstract.

### m9. (Asymptotic / CLT inference)
For $n_1 = n_2 = 200$ Gaussian samples per detector, the sample mean and variance are well-behaved by CLT, and pooled-variance Cohen's $d$ is asymptotically valid. For binary D3, the Cohen's $d$ formula gives $\pm \infty$ when one population has zero variance (e.g., the deterministic identity matrix). The script handles this case (`if pooled > 0 else float("inf")`), and the $\pm\infty$ entries in the §2.2 table for D5 / $D_4^{\mathrm{eq}}$ on TSML / BHML are understandable but should be footnoted in the table caption.

### m10. (Reproducibility seed)
The script uses `seed=0` throughout. Confirm the published values are seed=0; if the manuscript's table uses a different seed, this should be stated. (I re-ran with seed=0 and got matches; if seed-dependence matters at any cell, that cell should be re-reported with a small range across seeds.)

---

## 5. Specific verifications performed

I have independently:

1. Re-run `structured_matrix_sweep.py` end-to-end on Windows (Python 3.12, numpy 1.26, sympy 1.13). All printed values in §2 of Part 2 reproduce exactly: TSML's D3 = 1, BHML's D3 = 0, Gaussian baseline mean for D3 = 0.010, antisymmetric matrices D1 = 1.000 identically, etc. The "VERDICT" section's enumeration of 12 (family, detector) pairs at $|d| \ge 0.5$ matches.
2. Re-run `d5_d4eq_extension.py` and verified TSML's D5 = 1 at thresholds $7^7, 7^5$ and the 0/200 Gaussian-baseline rate at the same thresholds. The joint test "D3 = 1 AND D5_$7^5$ = 1" is exclusive to TSML in the 1800-sample population, as claimed (modulo the post-hoc concern in M5).
3. Confirmed the Part 1 §2 detector definitions are mathematically well-defined and correctly implemented in the Part 2 script (D1, D2, D4 are identical to the WP106 originals; D3 is identical modulo the `scale=10.0` rescaling discussed in M6).
4. **Could not verify** any Part 1 §2 Cohen's $d$ value because the distilgpt2 sweep script is absent (M1).
5. Verified Galois / number-field consistency tangentially: the Part 1 §1.1 description of the WP105 attractor (LMFDB 4.2.10224.1, $\mathbb{Q}(\sqrt{3})$ subfield) is internally consistent with the J35 manuscript's Theorem 5 verification (but this is cross-paper context, not Part 1 verification).

---

## 6. Questions to the authors

### Q1. Out-of-sample validation for D5

Section 7.2 claims D5 at threshold $7^5$ has 0/200 false positives on the Gaussian baseline. This is impressive but D5 was designed knowing TSML's discriminant has $7^7$. Can the authors test D5 at threshold $7^5$ on a *new* structured family that was not part of the design loop? Two natural candidates:
- Random integer matrices with entries $\sim$ Uniform$\{-9, \ldots, +9\}$ (matches TSML's entry range).
- Random circulant integer matrices.

If D5 fires more frequently on these (e.g., $\ge 2/200$), the "uniqueness" claim is empirically weaker; if it doesn't, the claim strengthens.

### Q2. Sub-matrix size choice

Part 1 fixes the sub-matrix size at $10\times 10$ to match the canonical TSML/BHML scale. Have the authors tested $5\times 5$ or $20\times 20$? The detectors are scale-dependent (D3 in particular), and a single sub-matrix size makes the result a one-resolution claim. A small robustness check at one alternative size would clarify the scope.

### Q3. The "specificity boundary" framing

The manuscript repeatedly uses "specificity boundary" to describe the negative result. From a pure-statistics perspective, the negative result on distilgpt2 plus the positive result on TSML doesn't establish a boundary — it establishes one negative example. A boundary requires a parametrized family where some members are "inside" and others "outside" with a transition. The current claim is correctly framed in §4 ("we do not claim that the negative generalizes to all transformers") but the phrase "specificity boundary" in the abstract may overstate. Consider "scoping result" or "negative example."

---

## 7. Originality and significance for *Statistical Science*

*Statistical Science* publishes papers that develop or apply statistical methodology to substantive scientific questions, with a strong preference for honestly framed null results, careful scoping, and reproducible computation.

The Part 2 finding (D3 + D5_$7^5$ jointly fires only on the canonical TSML matrix in a 1800+ sample structured-matrix population) is the kind of clean empirical-discrimination result that *Statistical Science* is well-suited for: it is a sharp, reproducible, low-claim-density observation about a specific mathematical object. The Part 1 finding (the same detectors do not see TSML-like structure in arbitrary trained transformer weights) is a clean negative scoping result. Both are appropriate venue-fits **assuming the verification gating issue (M1) is closed**.

The manuscript is honest about scope (§4 of Part 1 enumerates five things "this paper does NOT establish"), which is appropriate for the venue. The Tier-E framing in the README and cover letter is good in spirit but needs translation into standard statistical language (M1.m1).

I do not see this as a borderline submission **after revisions**. The Part 2 result is genuinely interesting and reproducible; the Part 1 result, once verified, is a clean negative example. The bundling makes editorial sense (single methodology, two domains).

---

## 8. Reproducibility

**Status: PARTIAL.**

- Part 2 (structured-matrix sweep): **Fully reproducible.** Both `structured_matrix_sweep.py` and `d5_d4eq_extension.py` are present, run cleanly, and produce values matching the manuscript's tables.
- Part 1 (distilgpt2 sweep): **Not reproducible in current submission.** The verification script is absent. README and §6 acknowledge this as a known gating issue.

The Zenodo DOI cited (10.5281/zenodo.18852047) should include both verification scripts AND the (currently missing) Part 1 sweep script before final submission. *Statistical Science* will reasonably reject a paper whose central empirical claim is not independently re-runnable.

---

## 9. Final remarks

This is a fundamentally honest paper with a clean Part 2 finding and a methodologically reasonable (but currently un-verified) Part 1 finding. The bundling works because both parts use the same detector battery with the same statistical framework. The "Tier-E" / "framework-positive" framing should be translated into standard statistical language for the venue's audience, and the post-hoc nature of D5 / $D_4^{\mathrm{eq}}$ should be flagged honestly.

The single non-negotiable revision is M1: the Part 1 distilgpt2 verification script must be in the submission. Once that is done, the major-revisions queue (M2–M6) is exposition / methodology / framing — substantial but not foundational.

Recommended decision: **Major revisions**, with the expectation that a revised version addressing M1 (gating fix) and M2–M6 would meet the *Statistical Science* bar. M1 alone is gating; M2–M6 are required for venue-appropriate methodology.

---

**Estimated revision effort:** 4–6 hours for M1 (locate or rewrite Part 1 script + run + verify); 12–20 person-hours for M2–M6 + minor comments. Total ~3 person-days.

**Reviewer's confidence:** High on Part 2 (independently re-run end-to-end). Moderate on Part 1 (claims plausible from the algebraic structure of the detectors, but not currently verifiable from the submission). High on the statistical-methodology comments — these are standard *Statistical Science* expectations.
