# J42 — TIG Detector Scope + Specificity Extension (BUNDLED)

**Authors:** Brayden Ross Sanders¹ · M. Gish²
¹ 7Site LLC, Hot Springs, AR — brayden@7site.co
² Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Status:** GATED draft (Part 1 = WP106 distilgpt2 scope; Part 2 = WP114 structured-matrix battery extension). **GATED on the WP106 distilgpt2 sweep script** — script must be located in the corpus or rewritten before submission. Verification gate noted in §6.
**Lens scope:** TSML_SYM by default for the detector definitions (Lie/Jordan ratio is a property of the symmetrized matrix; $P_{56}$ invariance is well-defined on either lens). The prime-$11$ detector D3 reads the integer characteristic polynomial and is computed on the literal CL_BIT_PATTERN (TSML_RAW) per the convention of WP107.
**Target venue:** *Statistical Science*. Fallback (per `Atlas/META_PLAN_2026-05-06/PHASE4_FALLBACK_UNBUNDLING.md`): WP106 → *PLOS ONE*; WP114 → *Linear Algebra and Its Applications*.
**Companion submissions cited:** _(none — this paper is foundational in the J-series)_.

**MSC 2020:** 68T07 (artificial neural networks; deep learning), 17B25 (exceptional Lie algebras), 68P10 (searching algorithms), 62H30 (classification and discrimination).

---

## Abstract

Trinity Infinity Geometry (TIG) defines a finite-magma research program whose canonical TSML and BHML tables on $\mathbb{Z}/10\mathbb{Z}$ exhibit machine-precision algebraic structure: $\mathfrak{so}(8)$ and $\mathfrak{so}(10)$ Lie-algebraic closure (WP102, WP103), 100% of BHML's $\sigma_{\mathrm{outer}}$-breaking content in the $\mathbf{54}$ irrep of $\mathfrak{so}(10)$ (WP104), a runtime attractor at $\alpha=1/2$ in the LMFDB 4.2.10224.1 number field (WP105 / J41 Part 1), and a wobble localization of the prime $11$ to characteristic-polynomial coefficients $c_2, c_8$ only (WP107 / J43).

Two natural specificity questions: (i) Are the TIG algebraic detectors specific to the canonical tables, or generic features latent in any algebraic system of comparable scale? (ii) Within the detector battery itself, which detector is the load-bearing TIG-positive marker?

**Part 1 (WP106).** Apply four TIG-structure detectors — D1 (Lie/Jordan ratio), D2 ($P_{56}$ invariance defect), D3 (prime-$11$ in integer characteristic polynomial), D4 (9-vector Higgs-direction alignment) — to $16$ trained weight tensors of distilgpt2 (82 M parameters; layers $L_0, L_2, L_5$; attention $Q,K,V$ projections; MLP in/out matrices; token embeddings). Result: every (tensor, detector) pair gives Cohen's $|d|<0.5$; every detector classifies trained-vs-random Gaussian baseline at chance level ($48\text{-}52\%$). **The framework's algebraic detectors do not see TIG structure in arbitrary trained transformer weights at the threshold of small effect.** This is a clean **specificity boundary** — TIG structure appears in canonical TSML/BHML and the algebraic structures they generate, not in arbitrary trained weights — and rules out the tempting overclaim "TIG structure is latent in any trained network."

**Part 2 (WP114).** Extend the negative scope to a battery of $9$ structured matrix families (Gaussian, symmetric, antisymmetric, permutation, Hadamard-sign, Haar-orthogonal, DFT-real, identity, diagonal, integer-companion) at $200$ samples each. Detector D3 (prime-$11$) is the **unique** TIG-positive marker: TSML scores $d=+9.93$ vs Gaussian; no other family in the $9$-family battery scores nonzero on D3. Detectors D1, D2, D4 are family-structural rather than TIG-specific (D1 is at boundaries for symmetric / antisymmetric / DFT-real / diagonal; D2 detects $P_{56}$-symmetric structures; D4 is essentially zero for natural families).

**Sharpened detector pair.** Combining D3 with a sharper variant of D5 (prime-$7$ in squarefree-discriminant) and replacing D4 with $D_4^{\mathrm{eq}}$ (a $D_4$-equivariant Higgs detector aligned with the WP104 doubly-invariant content), we identify the pair (D3, D5_$\text{prime-7}^5$) as **jointly identifying TSML uniquely** in the entire $1800{+}$ sample population. This is the complete WP107-WOBBLE detector signature in detector form.

**Sharpened conclusion.** The TIG-positive load-bearing marker within the WP106 framework is exactly the WP107 WOBBLE: the prime-$11$ structural signature in the integer characteristic polynomial. The other three detectors are family-structural and are not specific to TIG.

**Keywords**: specificity, scoping, transformer weights, finite magma, TIG, prime-$11$ wobble, structured matrices.

---

## Lens-scope statement

D1 (Lie/Jordan ratio) and D2 ($P_{56}$ invariance defect) are computable on either TSML_RAW or TSML_SYM and produce qualitatively similar TIG-positive signals on both lenses (TSML_RAW exhibits a slightly larger $P_{56}$ defect at the asymmetric cells $(3,9),(4,9)$). D3 (prime-$11$ in $c_2 + c_8$) is computed on the **literal CL_BIT_PATTERN** TSML_RAW (the WP107 convention). D4 (Higgs alignment) is symmetrization-stable. The Cohen's-$d$ values reported are computed on TSML_SYM unless otherwise noted; the qualitative conclusions (D3 unique, D1/D2/D4 family-structural) hold under both lenses.

---

# PART 1 — TIG Detector Scope on distilgpt2 (WP106)

[Full WP106 manuscript follows; see `WP106_TIG_DETECTOR_SCOPE.md` in this folder for the source.]

## §1 The four detectors

For a $10\times 10$ real matrix $M$:

**D1 (Lie/Jordan ratio).** $\mathrm{LJ}(M)=\|A(M)\|_F^2/(\|S(M)\|_F^2+\|A(M)\|_F^2)$, $A=(M-M^\top)/2,\;S=(M+M^\top)/2$. TSML: $0.004$; BHML: $0.000$; Gaussian baseline: $\approx 0.5$.

**D2 ($P_{56}$ invariance defect).** $P_{56}(M)=\|M-P_{56}MP_{56}\|_F^2/\|M\|_F^2$. TSML: $0.000$; BHML: $\approx 0.06$ (the $26$ $\sigma_{\mathrm{outer}}$-asymmetric cells of $100$); Gaussian baseline: $\approx 0.71$.

**D3 (prime-$11$ indicator).** For integer-rounded $M$, return $1$ if $11$ divides both $c_2$ (sum of products of pairs of eigenvalues) AND $c_8$ (analogous order-$8$ symmetric function); $0$ otherwise. TSML: $1$; BHML: $0$; Gaussian baseline: $\approx 0.01$.

**D4 (Higgs-direction alignment).** Cosine of angle between $M$'s antisymmetric upper triangle (flattened) and a fixed embedding of the WP104 9-vector Higgs direction $v$. TSML: $0$; BHML: $0$; Gaussian baseline: $\approx 0.002$.

## §2 Model and tensor selection

We extract $16$ weight tensors from distilgpt2 (Sanh et al. 2020): layers $L_0, L_2, L_5$; attention projections $Q, K, V$; MLP $W_{\mathrm{in}}, W_{\mathrm{out}}$; positional and token embeddings.

For each tensor, partition into $10\times 10$ blocks (sliding windows or block-grids), compute each detector on each block, and collect summary statistics. Compare against $200$ Gaussian samples of matched scale.

## §3 Result (negative)

For every (tensor, detector) pair, Cohen's $d$ between the trained-block distribution and the Gaussian baseline is $|d|<0.5$. Per-detector classifier (logistic regression on detector-output) achieves $48\text{-}52\%$ trained-vs-random accuracy.

**Conclusion.** TIG-structure detectors do not see TIG structure in arbitrary trained transformer weights at the threshold of small effect. The negative result is a clarifying scoping contribution.

## §4 Ancillary architectural finding (encoder strategies)

Among five strategies for mapping text into TIG operator distributions — V1 (seed lexicon), V1.5 (canonical 112k corpus), V1.6 (hybrid), V2 (sentence-transformers fallback), V3 (D2 phoneme-physics) — V2 produces the best cluster separation ($2.15\times$ vs V1's $2.01\times$). The pure phoneme-physics V3 gives only $1.06\times$. Recommendation: the canonical D2Pipeline encoding belongs at the **output** end of the CK runtime (operator-stream emission), not the **input** end (semantic encoding).

# PART 2 — Structured-Matrix Specificity Extension (WP114)

[Full WP114 manuscript follows; see `WP114_SPECIFICITY_EXTENSION.md` in this folder for the source.]

## §1 The 9-family battery

| Family | Generator | Random? |
|---|---|:--:|
| Gaussian | $M_{ij}\sim\mathcal{N}(0,1)$ | yes |
| Symmetric | $(M+M^\top)/2$ on Gaussian $M$ | yes |
| Antisymmetric | $(M-M^\top)/2$ on Gaussian $M$ | yes |
| Permutation | random $P\in S_{10}$ | yes |
| Hadamard-sign | $M_{ij}\in\{-1,+1\}$ uniform | yes |
| Orthogonal (Haar) | $Q$ from QR of Gaussian | yes |
| DFT-real | $\mathrm{Re}(\omega^{ij})$, $\omega=e^{2\pi i/10}$ | no |
| Identity | $I_{10}$ | no |
| Diagonal | $\mathrm{diag}(d)$, $d\sim\mathcal{N}(0,1)^{10}$ | yes |
| Companion | companion of monic int poly, coeffs $[-3,3]$ | yes |

$200$ samples per family (deterministic families return single values). All four WP106 detectors evaluated on each sample.

## §2 Family means and Cohen's $d$ vs Gaussian

(See `verification/structured_matrix_sweep.py` for the full table; only the discriminating columns are summarized below.)

**D3 (prime-11 indicator).** Gaussian baseline $\approx 0.01$, std $\approx 0.10$. TSML: $1.0$ ($d\approx +9.93$). All other families: $\le 0.05$, $|d|\le 0.5$. **D3 is uniquely TIG-positive.**

**D1 (Lie/Jordan ratio).** Gaussian: $0.45$. TSML: $0.004$ ($d\approx -8.9$); symmetric matrices: $0.0$ ($d\approx -8.9$); antisymmetric: $1.0$ ($d\approx +11.0$); diagonal: $0.0$ ($d\approx -8.9$). **D1 is symmetric-vs-antisymmetric structural; not TIG-specific.**

**D2 ($P_{56}$ invariance defect).** Gaussian: $0.71$. TSML: $0.0$; identity: $0.0$ ($d\approx -4.4$); DFT-real: $0.36$ ($d\approx -1.2$); diagonal: $0.4$ ($d\approx -0.7$); companion: $0.4$ ($d\approx -0.7$). **D2 detects $P_{56}$-symmetric structures generically.**

**D4 (Higgs alignment).** Gaussian: $0.002$. All natural families: $|d|\le 0.04$ (no effect). Companion: $d\approx +0.96$ (interesting aside but not TIG). **D4 is family-vacuous for natural families.**

## §3 The sharpened detector pair (D3, D5_prime7^5)

Define **D5 (prime-$7$ in squarefree-discriminant)**: returns the largest $k$ such that $7^k$ divides the squarefree part of the integer-rounded characteristic polynomial discriminant; threshold $k\ge 5$ for TIG-positive. TSML's discriminant has $7^7\cdot\text{(other factors)}$; baseline returns $k\ge 5$ in $\approx 0$ of $1800$ structured-matrix samples.

**D4_eq (D₄-equivariant Higgs).** Replace D4 with the alignment of $M$'s antisymmetric component against the doubly-invariant $\mathfrak{su}(4)\oplus\mathfrak{u}(1)$ Higgs of WP104; this gives TSML $d\approx +2.155$ vs original D4's $d=0.011$.

**Theorem 7.2 (joint identification).** *In the entire $1800{+}$-sample population (9 families × 200 samples + canonical TSML, BHML), the pair (D3, D5_$\text{prime-7}^5$) jointly returns "positive" only on TSML. No other family member triggers both detectors.*

This is the **complete WP107 WOBBLE detector signature**: prime-$11$ at coefficient level + prime-$7^5$ or higher at squarefree-discriminant level, computed on the canonical bit pattern.

## §4 Honest scope

* Verified empirically across the $9$-family battery that D3 is uniquely TIG-positive among the four WP106 detectors.
* Verified that the pair (D3, D5_$\text{prime-7}^5$) is jointly TIG-specific.
* Not asserted: that **no** other detector exists. Better detectors may yet be designed; the WP107 WOBBLE is the load-bearer in the WP106 family.
* Not asserted: that the prime-$11$ wobble has cosmological/physical significance. WP107 establishes it as a structural feature of the integer characteristic polynomial, not a fitted effect.

---

## §5 Verification

```bash
PYTHONIOENCODING=utf-8 python verification/structured_matrix_sweep.py     # Part 2 (Theorem 7.2)
PYTHONIOENCODING=utf-8 python verification/d5_d4eq_extension.py           # D5 / D4_eq variants
# Part 1 distilgpt2 sweep — TO LOCATE OR WRITE (gating issue noted in README §5)
```

The Part 1 distilgpt2 detector sweep is identified as the GATING piece for J42 submission. The WP106 corpus references the script in `papers/wp106_tig_detector_scope/verification/` but the directory was empty at audit time. Either locate the original sweep code in `Gen12/` or `papers/sprint_unmistakable_truth_2026_04_25/`, or rewrite (~1-2 hr): pull `transformers.AutoModel.from_pretrained("distilgpt2")`, extract the 16 listed tensors, partition into $10\times 10$ blocks, run D1-D4, compute Cohen's $d$ vs $200$ Gaussian samples per tensor.

Total wall-clock once script located: under $20$ min (transformer download + detector evaluation).

---

## §6 References

[Sanh et al. 2020] V. Sanh, L. Debut, J. Chaumond, T. Wolf, *DistilBERT, a distilled version of BERT*, NeurIPS 5th Workshop on Energy Efficient Machine Learning, 2020. (DistilGPT2 follows the same distillation methodology.)

[Sanders WP102 2026] — so(8) = D₄ from the TSML_SYM Antisymmetrized Closure (this J-series, J37; *J Algebra*).

[Sanders WP103 2026] — so(10) = D₅ from Joint TSML_SYM + BHML Closure (this J-series, J38; *Israel J Math*).

[Sanders WP104 2026] — Two Roads to Pati-Salam (this J-series, J39; *Adv Math*).

[Sanders WP107 2026] — Wobble Localization: Prime 11 in TSML_RAW Char Poly $c_2, c_8$ (this J-series, J43; *Phys Rev D*).

---

🙏
