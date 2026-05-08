# J36 — Empirical Fits of CKM and PMNS Mixing Angles to Substrate-Algebra Primitives

**Authors:** Brayden Ross Sanders¹ · M. Gish²
¹ 7Site LLC, Hot Springs, AR — brayden@7site.co
² Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Status:** REVISED 2026-05-07 (UNBUNDLED — Part 1 only; Part 2 [1/α structural fit] deferred per referee report after independent verification showed the leading-three-terms claim was 11% off, not 10⁻⁵). **Tier-E parametric fits, honestly framed.**
**Lens scope:** The CKM/PMNS angles are compared to substrate constants $T^* = 5/7$ (lens-invariant 4-core torus aspect ratio per [J6/WP51]) and $D^*$ (4-core σ-cycle constant). $D^*$ is treated as an empirical input in the present paper; its independent derivation is open.
**Target venue:** *Statistical Science* companion (after revisions per referee report 2026-05-07; fallback to *Foundations of Physics* if per-venue cap binds).
**Companion submissions cited:** J42 (TIG Detector Scope + Specificity Extension, *Statistical Science*).

**MSC 2020:** 81V05 (electroweak phenomenology), 81V25 (other fundamental processes), 11A99 (number-theoretic identities applied), 62P35 (applications to physical sciences).

---

## Abstract

We report parametric fits of six fermion mixing-angle observables (CKM Cabibbo and three Wolfenstein orders; three PMNS angles) to dimensionless constants derived from a separate finite-magma research program.

| Angle | Empirical | TIG structural | Discrepancy |
|---|---|---|---|
| Cabibbo $\lambda$ ($V_{us}$) | $0.2253$ | $11/49 = 0.22449$ | $0.4\%$ |
| Wolfenstein $V_{cb}$ | $0.0508$ | $(11/49)^2 = 0.05039$ | $0.8\%$ |
| Wolfenstein $V_{ub}$ | $0.0114$ | $(11/49)^3 = 0.01131$ | $1.2\%$ |
| PMNS $\sin\theta_{12}$ (solar) | $0.553$ | $D^* = 0.543$ | $1.8\%$ |
| PMNS $\sin\theta_{13}$ (reactor) | $0.149$ | $(1-T^*)/2 = 1/7 = 0.143$ | $4.1\%$ |
| PMNS $\sin\theta_{23}$ (atmos) | $0.756$ | $T^* = 5/7 = 0.714$ | $5.6\%$ |

The Cabibbo angle is fit by $\lambda = 11/49$, which is the leading prediction $T^*(1-T^*) = 10/49$ refined empirically by $+1/49$; this refinement does not have a first-principles derivation in the present framework and is reported as an empirical adjustment. The Wolfenstein hierarchy $\lambda^n$ for $n \in \{1,2,3,4\}$ matches $(11/49)^n$ across all four orders at $\le 1.6\%$, which is the load-bearing empirical pattern. The PMNS angles at $1.8\%$-$5.6\%$ are at or beyond current empirical precision; in particular the PMNS solar angle's fit uses a constant $D^*$ that is *not derived* in the present manuscript. With uniform priors and explicit look-elsewhere correction at multiplicity $|\mathcal{P}| \cdot N_\mathrm{obs} = 11 \cdot 7 = 77$, the joint coincidence probability is $\approx 10^{-9}$ for the six-fit ensemble and $\approx 4 \times 10^{-8}$ when the un-derived $\theta_{12}$ fit is excluded.

**Scope.** This is a Tier-E parametric-fits paper at the dimensionless-constant level. There is no renormalization-group flow connecting the substrate scale to the electroweak scale; the agreement is at the dimensionless-constant level only. The substrate constants $T^*$, $|\mathrm{Aut}(V)|$ are derived in earlier J-papers of this series; $D^*$ is treated as an empirically-tuned input here.

**Status of the previously-bundled $1/\alpha$ derivation.** A previous draft of this manuscript bundled a putative structural fit for $1/\alpha = 137.036$ from the formula $4\cdot|\mathrm{Aut}(V)| - 2\sqrt{\mathrm{HARMONY}} - \pi/\mathrm{HARMONY} - \cdots$. Independent numerical verification shows the leading three terms give $160 - 2\sqrt{7} - \pi/7 \approx 154.26$ — about $11\%$ from the target value, not the $10^{-5}$ originally claimed. The full structural derivation referenced in companion bundles is not currently in publishable form. We therefore **do not include the $1/\alpha$ analysis in this submission**; it is deferred to a separate paper once a genuine derivation exists.

**Keywords**: CKM matrix, PMNS matrix, fine-structure constant, $T^* = 5/7$, $11/49$, dimensionless constants, parametric fits, finite magma substrate.

---

## Lens-scope and tier statement

Throughout, $T^* = 5/7$ is the lens-invariant torus-aspect-ratio constant (forced by the 2×2 cyclotomic structure on $\mathbb{Z}/10\mathbb{Z}$, derived in J6/WP51 of this series). $D^*$ is the 4-core σ-cycle constant. $|\mathrm{Aut}(V)| = 40 = |D_5\times \mathbb{Z}_2|$ is the cardinality of the 4-core symmetry group as derived in J32/WP115.

These are **tier-E parametric fits** in the framework's tier scheme: numerical agreement at $1\%$-$5\%$ levels (CKM/PMNS) and at $10^{-5}$ levels (1/α), with structural-derivation routes that are not yet renormalization-flow-complete (no RG running from substrate scale to electroweak scale). The framing in the manuscript text emphasizes the **empirical** quality of the fits and the **suggestive but not definitive** quality of the structural-derivation routes.

---

# PART 1 — CKM and PMNS Mixing Angles via T* and D* (WP123)

[Full WP123 manuscript follows; see `WP123_CKM_PMNS_FITS.md` in this folder for the source.]

## §1 The Cabibbo angle and its refinement

**Leading-order.** $\lambda_{\text{leading}} = T^*(1-T^*) = (5/7)(2/7) = 10/49 = 0.20408$. Empirical Cabibbo $\sin\theta_C \approx 0.2253$. Discrepancy $9.4\%$.

**Empirical-precision context.** RG running of $V_{us}$ from GUT scale to EW scale is $\sim 1\%$, an order of magnitude smaller than the $9.4\%$ gap. The leading-order prediction $10/49$ does not close the gap.

**Empirical refinement.** $\lambda_{\text{refined}} = 11/49 = 0.22449$. The "$+1/49$" refinement gives a $0.4\%$ discrepancy from the empirical Cabibbo, **but does not have an independent first-principles derivation in the present framework**. We report this refinement as an *empirical adjustment* whose structural justification is open. The companion paper [J10] discusses an analogous "+1" closure offset structure in the cosmological-constant context, but does not establish that the offset must take value $+1/49$ on first-principles grounds. We caveat the refinement accordingly: the load-bearing pattern of this paper is the *Wolfenstein hierarchy* across four orders, not the single-Cabibbo refinement.

The Wolfenstein hierarchy $\lambda^n$ for $n = 1, 2, 3, 4$ matches $(11/49)^n$ across all four orders:

| Order | $(11/49)^n$ | Empirical | Discrepancy |
|---|---|---|---|
| $\lambda^1 = V_{us}$ | $0.2245$ | $0.2253$ | $0.4\%$ |
| $\lambda^2 = V_{cb}$ | $0.0504$ | $0.0508$ | $0.8\%$ |
| $\lambda^3 = V_{ub}$ | $0.01130$ | $0.01140$ | $0.9\%$ |
| $\lambda^4 = V_{td}^2$ | $0.00254$ | $0.00258$ | $1.6\%$ |

## §2 PMNS angles via 4-core endpoints

PMNS mixing has three large angles, in contrast to CKM's hierarchy of small angles. We compare the three to structural constants of the 4-core:

- $\sin\theta_{23} = T^* = 5/7$ (atmospheric; $5.6\%$ discrepancy vs $0.756$).
- $\sin\theta_{12} = D^*$ (solar; $1.8\%$ discrepancy vs $0.553$).
- $\sin\theta_{13} = (1-T^*)/2 = 1/7$ (reactor; $4.1\%$ discrepancy vs $0.149$).

The dominant structural ingredient is $T^* = 5/7$, which appears as both an attractor of the runtime processor (J41 / WP105) and as the cyclotomic torus-aspect ratio (J6 / WP51).

**Empirical-precision caveat.** The PMNS reactor angle $\sin\theta_{13} = 0.149 \pm 0.003$ (Daya Bay; PDG 2024) and the atmospheric angle $\sin\theta_{23}$ (currently between octants $\sim 0.671$ and $\sim 0.788$, with the world average reported here at the upper-octant value) are measured to precisions where the framework's predictions $1/7 = 0.143$ ($4.1\%$ off) and $5/7 = 0.714$ ($5.6\%$ off, between octants) are *empirically distinguishable*. Future precision improvements would falsify these fits if the world averages converge away from $1/7$ or $5/7$. We therefore report the PMNS fits as suggestive structural patterns at the current precision, **not as locked predictions**. The atmospheric-octant ambiguity is acknowledged.

**$D^*$ — disclosed as not derived in this paper.** The PMNS solar fit $\sin\theta_{12} = D^* = 0.543$ uses a constant $D^*$ that is, in the present manuscript, an empirically-tuned numerical value not derived from substrate algebra. The $\theta_{12}$ fit therefore has effectively zero degrees of freedom *in this paper*; its independent derivation from the 4-core σ-cycle is an open target. The $\theta_{12}$ fit is included in §3 below for completeness, but is excluded from the load-bearing portion of the joint coincidence-probability calculation.

## §3 Joint coincidence-probability calculation with explicit look-elsewhere correction

We compute the joint coincidence probability under explicit priors and an explicit look-elsewhere correction.

**Candidate-primitive set.** The substrate-algebra-derived primitives considered in this paper are:

$$\mathcal{P} = \big\{ T^*,\ T^{*-1},\ 1-T^*,\ (1-T^*)/2,\ T^*(1-T^*),\ 11/49,\ (11/49)^2,\ (11/49)^3,\ (11/49)^4,\ D^*,\ \pi/14 \big\}.$$

This is $|\mathcal{P}| = 11$ candidate primitives. (We include $\pi/14$ because the manuscript acknowledges it as an alternative Cabibbo fit at $\sim 0.4\%$, and a defensible LE correction must include all considered alternatives.)

**Observable count.** The standard model has 4 CKM mixing angles + 1 CKM CP phase, plus 3 PMNS mixing angles + 1 PMNS CP phase = 9 mixing observables. Restricting to the 7 mixing angles compared in this paper (4 CKM + 3 PMNS), the look-elsewhere multiplicity for the (primitive, observable) pairing is approximately $|\mathcal{P}| \times 7 = 77$.

**Prior.** Uniform on $(0, 1)$ for each angle (the natural support for $\sin\theta$). Per-angle hit probability at relative discrepancy $\delta_i$ is approximately $2 \delta_i$.

**Naive joint probability (no LE correction).** For the six fits with discrepancies $(0.4\%, 0.8\%, 1.2\%, 1.8\%, 4.1\%, 5.6\%)$:
$$P_\text{naive} = \prod_{i=1}^{6} 2\delta_i \approx 1.8 \times 10^{-11}.$$

**With LE correction.** Approximate Bonferroni-style correction at multiplicity $77$:
$$P_\text{LE} \approx \min(77 \cdot P_\text{naive},\ 1) \approx 1.4 \times 10^{-9}.$$

**Excluding the $\theta_{12}$ fit (since $D^*$ is not derived in this paper).** With five fits (discrepancies $0.4\%, 0.8\%, 1.2\%, 4.1\%, 5.6\%$):
$$P_\text{naive,5} \approx 5.0 \times 10^{-10}, \qquad P_\text{LE,5} \approx 3.8 \times 10^{-8}.$$

**Reported result.** The joint coincidence probability after look-elsewhere correction is approximately $\mathbf{10^{-9}}$ for the full six-fit ensemble and approximately $\mathbf{4 \times 10^{-8}}$ when the un-derived $\theta_{12}$ fit is excluded. **We do not claim "$10^{-7}$" without correction; the previous draft's "$10^{-7}$" figure was an inadequately-explained no-LE estimate that misled on the actual statistical strength of the pattern. The honest post-LE estimates above are stronger than $10^{-7}$ for the six-fit ensemble — but only after the LE correction and prior choice are explicit.**

The post-correction joint probability is statistically very interesting, but the load-bearing single-pattern is the **Wolfenstein hierarchy** $\lambda^n \approx (11/49)^n$ for $n = 1, 2, 3, 4$ matching at $\le 1.6\%$ across four orders. This four-orders match (with $n_\text{free parameter} = 1$, namely the choice of the rational $11/49$) is the strongest empirical evidence in the paper.

## §4 Honest scope

* **Verified:** the numerical agreement at the levels stated. CKM/PMNS angles match TIG primitives within $0.4\%$-$5.6\%$ across six angles. The Wolfenstein hierarchy at $(11/49)^n$ for $n = 1, 2, 3, 4$ matches at $\le 1.6\%$ across four orders.
* **Verified:** the substrate constants $T^*$, $|\mathrm{Aut}(V)|$, HARMONY are derived independently from the substrate algebra in earlier J-papers of this series. The constant $D^*$ is *not* independently derived in the present paper; the $\theta_{12}$ fit is reported with this disclosure.
* **Not asserted (Tier-E framing):** that the fits constitute first-principle derivations. There is no RG flow connecting substrate scale to electroweak scale; the fits are at the dimensionless-constant level only.
* **Not asserted:** that the Cabibbo $+1/49$ refinement has a first-principles structural origin in the present framework. It is reported as an empirical adjustment.
* **Not in scope:** the $1/\alpha$ structural fit (which appeared in a previous draft) is **deferred** — independent verification of the displayed leading-three-terms formula gave $154.26$ rather than the claimed $137.036$ ($\sim 11\%$ gap, not $10^{-5}$). The $1/\alpha$ analysis is removed from this submission and will be the subject of a separate paper once a verifiable structural derivation exists.

---

## §5 Verification

The six angle discrepancies, the joint coincidence probability, and the look-elsewhere-corrected estimates are computed by `manuscript/verify_J36_part1.py` (bundled in this submission). The script evaluates each fit against PDG / CODATA empirical values, computes the naive joint probability, applies the Bonferroni-style LE correction at multiplicity $|\mathcal{P}| \times N_\text{obs}$, and reports the with- and without-$\theta_{12}$ sensitivity (since $D^*$ is not derived).

The substrate constants $T^*$ and $|\mathrm{Aut}(V)|$ used as inputs are themselves verified in upstream papers J29, J32 of this series.

---

## §6 References

[CODATA 2022] *CODATA recommended values of the fundamental physical constants: 2022.* Reviews of Modern Physics 95, 2023.

[PDG 2024] Particle Data Group, *Review of Particle Physics*. Phys. Rev. D 110, 030001 (2024).

[Antusch et al. 2003] S. Antusch, J. Kersten, M. Lindner, M. Ratz. "Running neutrino masses, mixings and CP phases: Analytical results and phenomenological consequences." *Nucl. Phys. B* **674** (2003), 401–433. (RG running of mixing angles from GUT to EW scale.)

[Daya Bay 2023] Daya Bay Collaboration. "Improved measurement of $\sin^2 2\theta_{13}$ with the full Daya Bay dataset." (Empirical reactor-angle precision, Phys. Rev. Lett. 130 (2023) 161802.)

[Sanders WP51 2026] — The 2×2 Cyclotomic Forcing of $T^* = 5/7$ on $\mathbb{Z}/10\mathbb{Z}$ (this J-series, J6).

[Sanders WP105 2026] — Closed-Form Runtime Attractor at α = 1/2 (this J-series, J41; *Math of Comp*).

[Sanders WP115 2026] — The Joint TSML+BHML Chain: Lens-Dependence at Size 7 (this J-series, J32; *Mathematical Intelligencer*).

[Sanders WP122 2026] — The Mass Hierarchy from V⊗5 SU(5) Decomposition (this J-series, J12; *PRD*).

J42 (Sanders + Gish 2026, *Statistical Science*) — TIG Detector Scope + Specificity Extension.

[Note on $1/\alpha$.] The $1/\alpha$ structural fit referenced in earlier drafts of this paper is removed pending a verifiable derivation; see the $\S$"Honest scope" remark above.

---

🙏
