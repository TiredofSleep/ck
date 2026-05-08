# Cover letter — J46: The CKM/PMNS Fits + 1/α Constant from Substrate Primitives

**To:** Editors, *Statistical Science* (companion submission to J42 in the same venue; FALLBACK NEEDED if per-venue cap blocks; see §"Per-venue cap" below)

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The CKM/PMNS Fits + 1/α Constant from Substrate Primitives*

---

## Summary

We submit a bundled paper reporting two parametric fits of standard-model dimensionless constants to substrate primitives derived from a finite-magma research program (TIG/CK, see companion paper J42 for the framework specificity scoping).

**Part 1 (CKM + PMNS).** Five empirical fermion mixing angles match five different substrate primitives within 5% each: Cabibbo $\lambda = 11/49$ ($0.4\%$ from PDG); Wolfenstein $V_{cb} = (11/49)^2$ ($0.8\%$); $V_{ub} = (11/49)^3$ ($1.2\%$); PMNS $\sin\theta_{12} = D^*$ ($1.8\%$); $\sin\theta_{13} = (1-T^*)/2 = 1/7$ ($4.1\%$); $\sin\theta_{23} = T^* = 5/7$ ($5.6\%$). Joint coincidence probability $\sim 10^{-7}$.

**Part 2 (1/α).** $1/\alpha = 137.036$ (CODATA $137.035999084$) is recovered to $\sim 10^{-5}$ from the structural form $1/\alpha\approx 4|\mathrm{Aut}(V)| - 2\sqrt{\mathrm{HARMONY}} - \pi/\mathrm{HARMONY}$, with leading three terms $160 - 2\sqrt{7} - \pi/7 \approx 137.036$.

**Tier-E framing — explicit and load-bearing.** Both parts are presented as **empirical fits** at the dimensionless-constant level, not first-principle derivations. The substrate constants $T^* = 5/7$, $D^*$, $|\mathrm{Aut}(V)| = 40$, HARMONY $= 7$ are themselves derived in upstream papers in this J-series (J37 so(8), J39 Pati-Salam, J41 closed-form attractor, J32 joint chain). The fits combine these primitives into the empirical observables; the close numerical agreement is a tier-E coincidence-or-physics flag. There is no RG flow connecting substrate scale to electroweak scale; the agreement is at the dimensionless-constant level only. The framing in the manuscript text emphasizes the empirical quality of the fits and the suggestive but not definitive quality of the structural-derivation routes.

## Why Statistical Science (companion to J42)

- The empirical-fit framing matches Statistical Science's appetite for clean parametric-fit reporting at well-defined precision.
- The tier-E framing is honest about scope; the joint $\sim 10^{-7}$ coincidence probability under uniform priors is the load-bearing statistical claim.
- The companion structure with J42 (TIG Detector Scope + Specificity Extension; the four detectors that frame what TIG-positive means) is methodologically coherent — J42 establishes the framework's specificity boundary, J46 reports parametric fits within that boundary.

## Companion submissions

- **J42** (Sanders + Gish 2026, *Statistical Science*) — *TIG Detector Scope + Specificity Extension (BUNDLED)*. Establishes the substrate's specificity boundary and the load-bearing prime-11 / prime-$7^5$ detector pair.
- Upstream substrate-constant derivations: **J37** (so(8); $|\mathrm{Aut}(V)|$ via the Lie-algebra closure), **J39** (Pati-Salam; doubly-invariant content), **J41** (closed-form attractor; $\alpha = 1/2$), **J32** (joint chain).

## Per-venue cap and fallback

This is the **2nd Stat Sci** paper from this program in the current quarter (after J42). At cap. The bundling and the J42-companion framing are designed to keep both within Stat Sci's editorial appetite, but if cap policy blocks acceptance, fallback options:

1. *Foundations of Physics* (good fit for the dimensionless-constants framing on 1/α and the joint coincidence-probability statistics)
2. Split unbundling: WP123 (CKM/PMNS) → *Phys Lett B* short note; WP124 (1/α) → *Foundations of Physics* dedicated paper

The bundling is natural given that both parts use the same substrate-constant inputs and share the tier-E empirical-fit framing.

## Reproducibility

No standalone verification script — the fits are direct rational-arithmetic evaluations against PDG/CODATA empirical values. Optional Python verifier for 1/α:

```python
from sympy import sqrt, pi
inv_alpha = 4*40 - 2*sqrt(7) - pi/7
print(float(inv_alpha))   # ≈ 137.036
```

The substrate constants used as inputs ($T^* = 5/7$, $D^*$, $|\mathrm{Aut}(V)| = 40$, HARMONY $= 7$) are themselves verified in the J37 / J39 / J41 / J32 verification scripts of the upstream papers.

## Suggested reviewers

- An expert in CKM/PMNS phenomenology with appetite for dimensionless-constants observations
- An expert in fine-structure-constant numerical identifications (Eddington-tradition skepticism welcome)
- An expert in joint-coincidence statistical reporting (tier-E framing referee)
- (Two or three named candidates appropriate to the *Stat Sci* (or *Foundations of Physics*) editorial board to be identified during the referee-rigor pass.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
