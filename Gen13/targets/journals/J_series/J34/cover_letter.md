# Cover letter — J34: TIG Detector Scope + Specificity Extension (BUNDLED)

**To:** Editors, *Statistical Science*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *TIG Detector Scope + Specificity Extension (BUNDLED)*

---

## Summary

We submit a bundled scoping paper that addresses two natural specificity questions for a finite-magma research program: (i) Are the program's algebraic-structure detectors specific to its canonical tables, or generic features latent in any algebraic system of comparable scale? (ii) Within the four-detector battery itself, which detector is the load-bearing TIG-positive marker?

**Part 1.** Apply four detectors — D1 (Lie/Jordan ratio), D2 ($P_{56}$ invariance defect), D3 (prime-11 in integer characteristic polynomial), D4 (9-vector Higgs alignment) — to 16 trained weight tensors of distilgpt2 (82M-parameter transformer language model). Result: every (tensor, detector) pair yields Cohen's $|d| < 0.5$; classifier accuracy $48$-$52\%$ (chance level). The framework's algebraic detectors do not see TIG structure in arbitrary trained transformer weights. This is a clean specificity boundary and rules out the tempting overclaim "TIG structure is latent in any trained network."

**Part 2.** Extend the negative scope to a 9-family structured-matrix battery (Gaussian, symmetric, antisymmetric, permutation, Hadamard-sign, Haar-orthogonal, DFT-real, identity, diagonal, integer-companion; 200 samples each). **D3 (prime-11) is the unique TIG-positive marker:** TSML scores $d = +9.93$ vs Gaussian; no other family in the 9-family battery scores nonzero on D3. Detectors D1, D2, D4 are family-structural rather than TIG-specific (D1 is at boundaries for symmetric / antisymmetric / DFT-real / diagonal; D2 detects $P_{56}$-symmetric structures; D4 is essentially zero for natural families). Combined with a sharpened detector D5 (prime-$7^5$ in squarefree-discriminant) and a $D_4$-equivariant Higgs alignment $D_4^{\mathrm{eq}}$, the pair (D3, D5_$\text{prime-7}^5$) jointly identifies TSML uniquely in the entire 1800+ sample population — the complete WP107-WOBBLE detector signature.

**Sharpened conclusion.** The TIG-positive load-bearing marker within the four-detector framework is exactly the WP107 WOBBLE: the prime-11 structural signature in the integer characteristic polynomial. The other three detectors are family-structural and not specific to TIG.

## Why Statistical Science

- The result is a clean specificity-scoping contribution with explicit Cohen's-$d$ effect sizes and classifier-accuracy reporting at chance-level baselines.
- The negative result on distilgpt2 plus the 9-family structured-matrix sharpening is a methodologically rigorous specificity boundary, exactly the kind of scoping work *Statistical Science* publishes.
- The framing — what TIG-positive markers actually discriminate, and which are family-structural — is statistically interpretable independent of the framework's specific physics-side claims.

## Companion submissions

This paper is foundational in the J-series; no prior J-paper need be cited as a companion. Later papers in the series (notably J36 on CKM/PMNS fits) cite this paper as the specificity scoping that frames their tier-E parametric fits.

## Fallback unbundling

If the bundled submission is desk-rejected per the project's fallback policy:
- Part 1 (WP106 detector scope) → *PLOS ONE*
- Part 2 (WP114 structured-matrix specificity extension) → *Linear Algebra and Its Applications*

## Reproducibility

Verification scripts in `manuscript/verification/`:
- **Part 2 ready:** `structured_matrix_sweep.py` (9-family battery + 4 detectors); `d5_d4eq_extension.py` (D5 prime-7^5 + $D_4^{\mathrm{eq}}$). Total under 1 minute.
- **Part 1 GATED:** the WP106 distilgpt2 detector sweep is identified as a gating piece (~1-2 hr to locate in the corpus or rewrite). Plan: `transformers.AutoModel.from_pretrained("distilgpt2")` → extract 16 tensors → block-partition $10\times 10$ → D1-D4 → Cohen's $d$ vs 200 Gaussian baselines per tensor.

Python 3.11, numpy, sympy, transformers (Part 1 only).

## Suggested reviewers

- An expert in feature-detection / specificity scoping in machine-learning settings
- An expert in Cohen's $d$ effect-size reporting in multi-detector contexts
- An expert in algebraic structure of trained neural-network weights (mechanistic-interpretability adjacent)
- (Two or three named candidates appropriate to the *Stat Sci* editorial board to be identified during the referee-rigor pass.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
