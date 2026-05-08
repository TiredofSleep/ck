# Referee Report: J3 / JCAP

**Manuscript:** "Freeze-Thaw Transit: Dual-Regime Scalar Dark Energy with Analytic Vacuum at $e^{-1}$ from a Logarithmic Potential"
**Authors:** B. R. Sanders, M. Gish, H. J. Johnson
**Submitted to:** Journal of Cosmology and Astroparticle Physics (JCAP)
**Reviewer:** External referee (anonymous), assigned by Editorial Board
**Date:** 2026-05-06

---

## 1. Summary of the manuscript

The authors propose a minimally coupled real positive dimensionless scalar $\Xi(x)$ with self-interaction $V(\Xi) = \Lambda^4 \Xi \log \Xi$ as a candidate quintessence dark-energy field. The action (Eq. 2) is the standard non-ghost canonical form in $(-,+,+,+)$ signature with kinetic term $-\tfrac{1}{2} M_\Pl^2 g^{\mu\nu}\partial_\mu\Xi\partial_\nu\Xi$.

The paper's three principal claims are:

(C1) **Analytic vacuum.** The potential has a unique stationary point at $\Xi_0 = e^{-1}$, with positive curvature $V''(\Xi_0) = \Lambda^4 e$, giving fluctuation mass $m_\Xi^2 = \Lambda^4 e / M_\Pl^2$. Setting $m_\Xi \sim H_0$ yields $\Lambda \approx 1.7$ meV (dark-energy scale).

(C2) **Dual-regime "freeze-thaw transit" trajectory.** On the rolling branch with outbound IC $\dot\Xi_i > 0$ at $z_i \approx 20$, the FRW solution traverses three dynamically distinct phases within a single physical history: Type-T thaw outbound from near the vacuum, Type-F instantaneous frozen turnaround at $z_\star \approx 1.3$ where $\dot\Xi = 0$ and $w_\Xi(z_\star) = -1$ momentarily, and Type-A asymptotic refreeze toward $\Xi_0 = e^{-1}$ as $z \to -1$. The observational signature is a non-monotone $w_{\rm DE}(z)$ with a local minimum at intermediate redshift.

(C3) **DESI consistency.** A documented best-fit configuration $(\Lambda^4/\rho_{c,0}, \Xi_i, \Xi'_i) = (0.231, 0.925, +0.470)$ at $z_i \approx 20$ (Eq. 31) yields $w_0 = -0.791$, $w_a = -0.492$, with $\chi^2_{\rm Gauss} = 1.24$ (1.1$\sigma$) against the published DESI 2024 DR1 marginal Gaussian summary $(w_0, w_a) = (-0.827 \pm 0.063, -0.75 \pm 0.27)$, while $\Lambda$CDM has $\chi^2_{\rm Gauss} = 15.26$ under the same approximation.

The authors are careful to label (C3) as a "Gaussian-on-summary proximity check, not a joint-likelihood goodness-of-fit," and explicitly defer the BAO+CMB+SN joint likelihood to a companion numerical paper.

Five falsifiability criteria $(F_1)$–$(F_5)$ are stated, with $(F_5)$ being the dual-regime non-monotone $w_{\rm DE}(z)$ signature that requires non-parametric reconstruction beyond CPL.

I have read the manuscript end-to-end and independently executed the verification scripts `desi_xi_optimize_v2.py`, `compute_zstar_v2.py`, and `compute_zstar_v3.py` that the authors cite as electronic supplementary material. **The script results do not reproduce the documented $z_\star \approx 1.3$ claim; this is the dominant issue and is addressed in §3 below.**

---

## 2. Decision recommendation

**Major revisions.**

JCAP referees rarely accept on first round, and this paper has both (i) one disqualifying numerical-reproducibility problem that, on independent execution of the supplied scripts, contradicts the central claim of the paper's empirical section, and (ii) several methodological issues that would be flagged at first reading by any cosmology referee — Friedmann normalization, IC tuning, and the Gaussian-on-summary versus joint-likelihood distinction. The theoretical content (the action, the analytic vacuum, the EoS, the late-time attractor) is solid and standard. The dual-regime classification is genuinely novel and is an honest contribution to the quintessence-trajectory taxonomy. The bibliography handles Caldwell-Linder, Chavanis, and the Bialynicki-Birula–Mycielski lineage with appropriate citation discipline.

But on the empirical side, the paper as written is not yet ready. The numerical reproducibility issue alone would compel major revisions; the IC-tuning naturalness gap is severable but flagged honestly already; the Friedmann normalization documentation in §5 ("the implicit Friedmann equation in the script reads $H^2(1 - \tfrac{1}{2}\Xi'^2) = \ldots$") is acceptable but minimal; and the missing prior-art citations on logarithmic dark-energy potentials (Boisseau et al., Tsujikawa-Sami exponential survey, the Albrecht-Skordis logotropic predecessor) need adding to bring the bibliography to JCAP standard.

With a focused round of revisions — primarily reconciling the scripts and the documented $(z_\star, w_0, \chi^2)$ values — this could become an acceptable JCAP submission. As written, it cannot be accepted.

---

## 3. Major comments

### 3.1 Numerical reproducibility: documented $z_\star \approx 1.3$ is not reproduced by the supplied scripts

This is the most serious issue and would alone compel major revisions.

**The paper claims (Eq. 31, §6.2 table, §6.3, $(F_5)$):** at the documented best-fit IC $(\Lambda^4/\rho_{c,0}, \Xi_i, \Xi'_i) = (0.231, 0.925, +0.470)$ at $z_i \approx 20$, the trajectory has $z_\star \approx 1.3$, with the tabulated profile $w(0) = -0.791$, $w(0.3) = -0.918$, $w(0.5) = -0.952$, $w(0.8) = -0.978$, $w(1.0) = -0.992$, $w(1.3) = -0.999$, $w(2.0) = -0.957$. The Type-F turnaround is asserted to lie at $z_\star \approx 1.3$ with $w(z_\star) \approx -1$.

**On running `compute_zstar_v3.py` with the documented IC** $(0.231, 0.925, +0.470)$ — by passing them directly to `reproduce_documented_fit(Lambda4=0.231, xi_init=0.925, xi_dot=0.470)` — I reproduce the present-epoch values $w(0) \approx -0.786$ and $\Xi(0) \approx 1.17$ (consistent with the paper). But the trajectory I obtain has its $w$-minimum at $z_\star \approx 2.13$, not $z_\star \approx 1.3$. Specifically:
- $w(z=2.0) = -0.9998$ (paper claims $-0.957$)
- $w(z=2.5) = -0.998$ (interpolated)
- $w(z=1.5) = -0.995$ (paper claims $-0.992$ at $z=1.0$, $-0.999$ at $z=1.3$)
- $w(z=1.0) = -0.981$ (paper claims $-0.992$)
- $w(z=0.5) = -0.943$ (paper claims $-0.952$)
- The zero-crossing of $\Xi'$ (the actual Type-F turnaround condition) sits at $z_\star = 2.131$.

**On running `compute_zstar_v3.py` with the script's hardcoded "documented best fit"** `(Lambda4=2.0, xi_init=2.05, xi_dot=0.005)` — the values that appear in the script's docstring as reproducing the documented fit at "$w_0 = -0.793, w_a = -0.451, \chi^2 = 1.52$" — I obtain $w_0 = -0.860$, $z_\star = 5.997$, completely off from both the paper's table and the paper's Eq. 31 IC values.

**On running the optimize script `desi_xi_optimize_v2.py`** end-to-end (the script the authors describe as producing Eq. 31): the grid-search best fit is $\Lambda^4 = 0.300$, $\xi_{\rm init} = 1.026$ at $z\sim 54$, $\xi_{\rm dot} = 0.357$, with $w_0 = -0.785$, $w_a = -0.459$, $\chi^2 = 1.615$ (1.3$\sigma$). These are 30% off the paper's claimed Eq. 31 values $\Lambda^4 = 0.231, \xi_i = 0.925, \xi'_i = 0.470, \chi^2 = 1.24$.

**On running `compute_zstar_v2.py`** (the older, "superseded" cosmic-time variant the authors flag as not the operative script): with $z_i = 20$ and $(\Xi_i, \pi_i) = (0.925, 0.429)$, the trajectory crashes through $w = -1$ very rapidly and reaches $w(0) = -1.51$ — phantom regime — contradicting the paper's $(F_1)$ rolling-branch criterion.

The four scripts, the paper's tabulated $w(z)$ profile, the paper's Eq. 31 IC values, and the paper's $z_\star \approx 1.3$ claim are not mutually consistent. This is not a scope question or a methodological-framing question; it is a reproducibility failure.

The footnote on p. 12 attempts to reconcile the conventions ("the supplementary script `desi_xi_optimize_v2.py` integrates from an earlier matter-era starting point at $N_{\rm start} = -4$ (corresponding to $z \approx 54$), then reads off the trajectory state at $z = 20$ to define the documented initial-condition values $(\Xi_i, \dot\Xi_i)$"), but I cannot confirm this round-trip. The numbers do not close.

**Required action:** the authors must (i) supply a single canonical script that, run with the IC values stated in Eq. 31, reproduces the tabulated $w(z)$ profile and the claimed $z_\star \approx 1.3$ and $\chi^2 = 1.24$ to four-digit accuracy; (ii) clearly mark all superseded/auxiliary scripts as such; and (iii) state the IC convention (e-folds vs cosmic time, in $H_0$ units or $\sqrt{\rho_{c,0}}$ units) unambiguously enough that an external referee can run the verification in under five minutes.

The paper's central numerical claim ($z_\star \approx 1.3$ and $\chi^2_{\rm Gauss} = 1.24$ at the IC of Eq. 31) is, on the supplied evidence, not reproducible. This must be fixed before publication.

### 3.2 Friedmann normalization is documented but only minimally

§6.2 contains a one-paragraph reconciliation between the script's $\Omega$-unit form $H^2(1 - \tfrac{1}{2}\Xi'^2) = \Omega_m a^{-3} + \Omega_r a^{-4} + \Lambda^4 \Xi \log \Xi$ and the standard form $3H^2 = \rho_m + \rho_r + \tfrac{1}{2} M_\Pl^2 \dot\Xi^2 + V(\Xi)$. This is the right rewrite up to factor-of-3 absorption, and the equivalence is correct. But the documentation is too brief to satisfy a careful JCAP referee.

The paper would benefit from an explicit sub-paragraph (in §5 or a small appendix) showing:
- the e-folds derivative convention $\Xi' = d\Xi/dN$ versus cosmic-time $\dot\Xi$;
- the relation $\dot\Xi = H \Xi'$;
- the definition of $\Lambda^4/\rho_{c,0}$ in dimensionless $\Omega$-units (the paper uses $\Lambda^4$ in script and $\Lambda^4/\rho_{c,0}$ in Eq. 31; these differ by a factor of $\rho_{c,0} = 3 H_0^2 M_\Pl^2$);
- the explicit check that $\Omega_\Xi(z=0) = \Omega_{\Xi,0}$ in the documented fit. The script does NOT enforce $\Omega_\Xi(0) = 1 - \Omega_m - \Omega_r$ as an external constraint; instead, the documented best-fit $\Lambda^4$ value is read off from the grid search. This means the model parameters $(\Lambda, \Xi_i, \Xi'_i)$ are jointly fit to (i) approximate $\Omega_\Xi$ today and (ii) DESI $(w_0, w_a)$. The reader cannot tell from §6.2 alone whether the documented configuration also satisfies the closure relation $\Omega_m + \Omega_r + \Omega_\Xi = 1$ exactly or approximately. This needs to be stated.

The kinetic backreaction in the implicit Friedmann denominator $(1 - \tfrac{1}{2}\Xi'^2)$ is correct but worth pointing out is non-standard: in canonical units with $\dot\Xi$ rather than $\Xi'$, the kinetic energy enters as $\tfrac{1}{2} M_\Pl^2 \dot\Xi^2 = \tfrac{1}{2} M_\Pl^2 H^2 \Xi'^2$, which is implicit in $H^2$ and gives the $1 - \tfrac{1}{2}\Xi'^2$ factor when solved. The reader should be told explicitly, not left to back-derive it from the script.

### 3.3 Initial-condition tuning, naturalness, and the missing attractor mechanism

The paper acknowledges (p. 14, "Initial-condition tuning") that $(\Xi_i, \Xi'_i) = (0.925, +0.470)$ at $z_i \approx 20$ are tuned, not predicted, and that "There is no naturalness or attractor argument in the present minimal theory that singles out these values; the rolling-branch restriction selects solutions, it does not derive them." This is honest and is more transparent than many quintessence papers.

However, the IC tuning is a 2D family at fixed $\Lambda$ (for $(\Xi_i, \Xi'_i)$ at fixed $z_i$), and combined with the choice of $\Lambda$ this is effectively a 3D parameter space that is being mapped against the DESI 2D $(w_0, w_a)$ Gaussian. The model is being fit through the data, not predicting it. JCAP referees are notoriously demanding on this point: the standard tracker quintessence literature (Steinhardt-Wang-Zlatev 1999, Zlatev-Wang-Steinhardt 1999) was developed precisely because the $\Lambda$CDM coincidence problem cannot be addressed by IC tuning. A paper that proposes a new quintessence model and acknowledges no IC attractor is, for a careful referee, asking the question "why this paper rather than a simpler 1-parameter quintessence with the same $w_0$?"

The honest paragraph on p. 14 is enough to head off rejection on this ground, but the paper would be substantially stronger if §6.2 included a brief tracker analysis: does the model admit a slow-roll regime in the matter era that erases IC memory, the way axion or PNGB quintessence does? The Caldwell-Linder thawing-class trajectories all share this IC sensitivity, and the present model's distinguishing feature is the dual-regime traversal — but that traversal itself may or may not be IC-robust. The "sensitivity scan" in §6.3 ("varying $\Xi'_i$ in $[0.43, 0.50]$ moves $z_\star$ from $\approx 1.7$ to $\approx 1.25$") is a useful start but is too narrow: what fraction of IC space (with the same $\Omega$-budget) realizes a Type-F turnaround at all? Is the dual-regime trajectory generic on the rolling branch, or does it require the IC to be in a tuned neighborhood?

This is severable from the main content but the paper is weaker without it. I would not require a tracker analysis for acceptance, but the IC-sensitivity scan should be expanded to a 2D scan in $(\Xi_i, \Xi'_i)$ at fixed $\Lambda$, with the fraction of IC space producing a Type-F turnaround on $0 < z_\star < 5$ explicitly reported.

### 3.4 The "Gaussian-on-summary" versus "joint-likelihood" distinction

The paper labels the $\chi^2_{\rm Gauss} = 1.24$ figure as a Gaussian-on-summary proximity check rather than a joint-likelihood goodness-of-fit, and the disclaimer is repeated several times (Abstract, §6.2 opening paragraph, "Methodological scope" paragraph p. 14, Summary §8 item 6, footnotes). This is correct and is already the right call.

But the claim in the Summary (item 6) that "$\chi^2_{\rm Gauss} = 1.52$" (1.2$\sigma$) — note the discrepancy with the body's $\chi^2 = 1.24$ — and the comparison to $\Lambda$CDM at $\chi^2_{\rm Gauss} = 15.26$ ($3.9\sigma$) is too easily readable as a model-vs-$\Lambda$CDM Bayes-factor-equivalent statement. **The Summary should explicitly state that $\Lambda$CDM has DESI joint-likelihood chi-square 15.3 BUT IS NOT 3.9$\sigma$ disfavored in the joint analysis** — the joint DR1 likelihood is consistent with $\Lambda$CDM (this is in Section 6.1 of DESI 2024 VI, arXiv:2404.03002; the BAO data alone are consistent with flat $\Lambda$CDM). The Gaussian-on-summary number $\Delta\chi^2 \sim 14$ between $\xi$-model and $\Lambda$CDM substantially overstates the actual evidence preference, which appears only in the BAO+CMB+SN joint chains (DR1: 2.6$\sigma$; DR2: 2.8–4.2$\sigma$ depending on SN sample).

**The numerical discrepancy between the body's $\chi^2 = 1.24$ and the Summary's $\chi^2 = 1.52$ should also be reconciled** — these are presented as the same quantity but differ by 23%. This needs explanation or correction.

### 3.5 Dual-regime trajectory: classification correct, but "Type-F at $z_\star$" needs more rigor

§6.3 (Type-T/F/A classification) is the paper's most original contribution and is well-written. The claim that the dual-regime trajectory is outside the Caldwell-Linder freezing/thawing dichotomy is correct: Caldwell-Linder 2005 explicitly classifies monotone $w(z)$ trajectories, and a single-history non-monotone trajectory with intermediate-redshift turnaround does not fit either class. The Type-T/F/A nomenclature is reasonable.

However, the Type-F regime is defined by the instantaneous condition $\dot\Xi = 0$ at a single redshift $z_\star$. This is a measure-zero point on the trajectory, not a physical regime. The "Type-F turnaround" is a descriptive label for a specific point, not a phase. The paper should either (i) rename Type-F to something like "Type-F point" or "F-locus," reflecting that it is an instant rather than an extended regime, or (ii) define Type-F as a finite neighborhood around $z_\star$ where $|\dot\Xi|$ is below some threshold, in which case the threshold and the resulting redshift width must be specified.

The numerical claim that "the residual $\sim 10^{-4}$ deviation from $-1$ in the tabulated value reflects finite numerical sampling near the turnaround rather than physical departure from the analytic Type-F condition $\dot\Xi(z_\star) = 0$" (p. 16) is plausible and is consistent with $w \to -1$ exactly at $\dot\Xi = 0$, but the paper does not verify this by, e.g., comparing the tabulated $w(z_\star)$ to the analytic limit at four-digit precision. With higher-resolution numerical integration (the script uses 5000 e-folds steps over an 8-decade-of-redshift integration; this is on the edge of underresolution), one should be able to confirm that the residual is indeed numerical.

### 3.6 Length and JCAP scope

JCAP papers in the quintessence-model line typically run 25–40 pages with appendices. The present manuscript is 17 pages without appendices, which is short for JCAP. The dual-regime classification deserves an extended discussion that the present length does not provide. Specifically, the following sections are too brief:

- **§7.4 Perturbations** (3 paragraphs). JCAP referees on quintessence papers typically demand a perturbation-theory analysis: $c_s^2 = 1$ is stated as the rest-frame sound speed for a canonical scalar, but this is a single line. The ISW signature of the dual-regime trajectory is deferred to a "companion numerical paper" — but if the dual-regime $w_{\rm DE}(z)$ has a local minimum at $z_\star \approx 1.3$, that's directly in the redshift range where ISW is sensitive. The paper should at minimum include a back-of-envelope estimate of the ISW signal modification from the local-minimum feature, even if a full Boltzmann-code analysis is deferred.

- **§7.3 EFT validity** is two paragraphs and is honest about the transplanckian field excursion, but the discussion of UV completion (or its absence) is thin. The paper should either commit to a tree-level statement explicitly ("we treat the action as a tree-level EFT and do not address UV completion in this paper") or include a paragraph on what kind of UV completion would be compatible with the logarithmic potential. The current text tries to do both and ends up doing neither well.

- **§5 (FRW Cosmology)** — only the background equations are given. There is no analytic expansion of $w(z)$ around either the vacuum or the Type-F point that would let the reader check the qualitative features without running the script. A first-order perturbative expansion of $w(z)$ around $\Xi_0 = e^{-1}$ in the late-time limit, and around $\Xi_{\rm max}$ in the Type-F neighborhood, would significantly strengthen §5.

A "letter-style" framing at 17 pages is in principle acceptable for JCAP, but the paper does not declare itself a letter, and the depth of the dual-regime analysis warrants more space.

### 3.7 Bibliography: missing prior art on logarithmic dark energy

The bibliography handles the major chains well: Caldwell-Dave-Steinhardt 1998, Zlatev-Wang-Steinhardt 1999, Sahni-Starobinsky 2000, Padmanabhan 2003, Peebles-Ratra 2003, Frieman-Turner-Huterer 2008, Tsujikawa 2013, Joyce-Jain-Khoury-Trodden 2015 are all present and correctly cited. The Bialynicki-Birula–Mycielski 1976, Hefter 1985, Weinberg 1989 + Bollinger 1989 lineage in nonlinear QM is honestly acknowledged. Chavanis 2015 / 2021 / 2022 logotropic program is discussed at length in §8 (Comparison) and §4.3 (loglineage), with the three structural distinctions (real vs complex field, dark-energy-only vs unified, dual-regime vs $\Lambda$CDM-equivalent) clearly stated.

However, several adjacent prior-art entries are missing:

- **Boisseau, Esposito-Farese, Polarski, Starobinsky 2000** (Phys. Rev. Lett. 85, 2236; arXiv:gr-qc/0001066), "Reconstruction of a scalar-tensor theory of gravity in an accelerating universe." This is the canonical reference for scalar-field reconstruction from $w(z)$ and is missing from the paper.

- **Albrecht and Skordis 2000** (Phys. Rev. Lett. 84, 2076; arXiv:astro-ph/9908085), "Phenomenology of a realistic accelerating universe using only Planck-scale physics." Albrecht-Skordis introduce a quintessence potential with both a tracking and a freezing regime, with intermediate-redshift behavior similar in spirit to the dual-regime trajectory studied here. This is a direct adjacent precedent that should be cited.

- **Boisseau 2000** and **Starobinsky 2007** on quintessence reconstruction from $w(z)$, in particular the constraint that any monotone $w(z) \to -1$ from above forces a freezing potential. The dual-regime trajectory presented here violates this monotonicity condition in a specific way (intermediate-redshift turnaround), and the paper should explicitly relate to the reconstruction theorems.

- **Caldwell, Kamionkowski, Weinberg 2003** ("Phantom energy: dark energy with $w < -1$ causes a cosmic doomsday") in addition to the Caldwell 2002 phantom paper that is cited. The CKW 2003 reference clarifies the future-singularity structure that the present model's $w \geq -1$ rolling branch evades.

- **Frieman, Hill, Stebbins, Waga 1995** is cited (Frieman1995), but the full PNGB literature including **Hill, Schramm, Walker 1989** (the first PNGB DE paper) and **Kim 1999** PNGB review is missing.

- **Tsujikawa-Sami 2007** "Comparing thawing and freezing dark energy parameterizations" (Phys. Lett. B 651, 224; arXiv:0709.1391) is the canonical reference for distinguishing thawing and freezing classes empirically. Missing.

- The DESI DR2 reconstruction papers in the bibliography (`Wang2026QReconstruction` arXiv:2603.21125, `Adil2026Analytic` arXiv:2603.14693) are dated after April 2026 and may be future-citing — please verify the arXiv IDs and publication status. If these are pre-prints in preparation, mark them as such.

- Logotropic dark fluid: **Ferreira-Avelino 2018** (Phys. Rev. D 97, 044030; arXiv:1801.00099) and **Wang-Wei 2017** (arXiv:1709.05550) on logarithmic dark-fluid equations of state are missing from the §8 comparison. These are the closest direct prior-art entries on logarithmic dark-energy phenomenology and should be in the comparison table.

### 3.8 The "structural rhyme" framing of the BBM connection

§4.1–4.2 frame the relation $V(\Xi) = -\Lambda^4 H_{\rm Gibbs}(\Xi)$ and the BBM uniqueness theorem as "structural rhymes," not derivations. This is honest and is the right framing — the BBM theorem applies to the wave-equation nonlinearity in $|\psi|^2 \log |\psi|^2$ on a probability density, while the present setting is a classical scalar potential in $\Xi \log \Xi$ on an unbounded real field. The two are formally similar but operationally distinct.

The paper makes this distinction clearly. However, the title of the section ("Structural Connections to Information-Theoretic Functionals") and the subsection title ("Bialynicki-Birula–Mycielski nonlinearity") may give the reader the impression that there is a derivational chain from BBM to the present action. The "Where the analogy breaks" remarks are honest but are visually subordinate.

I would recommend (i) renaming the section to "Functional-form precedents" to remove the implicit suggestion of derivational content, and (ii) elevating the "Where the analogy breaks" remarks from \remark environments to standalone subsections so they receive the rhetorical weight they deserve.

### 3.9 The companions/synthesis program framing

The paragraph on p. 5 ("Companions in the synthesis program") cites two companion papers — Sanders & Gish 2026 on $\sigma(N) \le 2/N$ (J1, JCT-A) and Sanders & Gish 2026 on the four-core attractor (J2, Algebraic Combinatorics) — and states that the cosmological action is NOT derived from the companions. The paragraph closes with "Forward synthesis to a unified framework is the subject of separate work in preparation." This is honest and severable from the empirical content of the present paper.

For a JCAP referee, however, the companion-paper reference is a distraction. The combinatorial $\sigma(N) \le 2/N$ rate theorem and the four-core attractor at $h/\beta = 1+\sqrt{3}$ have no operational connection to the cosmological action $V(\Xi) = \Lambda^4 \Xi \log \Xi$ that I can verify from the present manuscript. The phrase "is the combinatorial-side input that, combined with the Bialynicki-Birula separability uniqueness theorem, motivates the logarithmic functional form $\Xi \log \Xi$" is suggestive but not load-bearing — the paper itself states (Scope §9) that "no derivation of the cosmological action from the algebraic-combinatorial structure" is claimed.

I would recommend either (i) deleting the "Companions in the synthesis program" paragraph from §1 entirely, on the grounds that it has no load-bearing role in the paper's argument, or (ii) moving it to an appendix or footnote so that it does not interrupt the introduction's argumentative flow. Cosmology referees will read the paragraph and ask "where is the derivation?" and not finding one will downgrade the paper's perceived rigor.

---

## 4. Minor comments

- **p. 1, abstract, line 14:** "the field thaws outbound (Type-T), reaches an instantaneous frozen turnaround at intermediate redshift $z_\star \approx 2$" — the abstract still says $z_\star \approx 2$ while the body claims $z_\star \approx 1.3$. The abstract should be updated to match.

- **p. 1, abstract, line 21:** "on the dual-regime physical rolling branch ... where $\dot\Xi = 0$ and $w_\Xi(z_\star) = -1$ momentarily" — the bare scalar EoS reaches $-1$ momentarily, but the combined-sector $w_{\rm DE}$ does not exactly reach $-1$ because $\Omega_m$ and $\Omega_r$ contribute. The Abstract should distinguish $w_\Xi(z_\star)$ from $w_{\rm DE}(z_\star)$.

- **Eq. 1 (Abstract; defines $V$):** the paper uses both $V(\Xi) = \Lambda^4 \Xi \log \Xi$ (Eq. 1, body Eq. 4) and $V(\xi) = \kappa \xi \log \xi$ (proof_xi_canonical.py and historical sprint14 files) interchangeably. The reader should be told that $\kappa = \Lambda^4$ in the matching script, or a fully consistent notation should be used throughout.

- **§2.1, "field domain":** "configurations leading to $\Xi \to 0^+$ during cosmic evolution are outside the field domain considered in this effective theory and are not considered." This is a major restriction. The paper should state what happens dynamically when an IC lies in the basin of attraction of $\Xi \to 0^+$: does the field hit the boundary in finite cosmic time? The footnote on the $\psi = \log \Xi \in \mathbb{R}$ reparametrization is helpful but does not resolve the dynamical question. A 2D phase-portrait in $(\Xi, \Xi')$ at fixed $a$ would be useful.

- **Eq. 3 (Action):** the kinetic term is written as $-\tfrac{1}{2} M_\Pl^2 g^{\mu\nu} \partial_\mu \Xi \partial_\nu \Xi$. With $\Xi$ dimensionless and $g^{\mu\nu}$ inverse-metric, the kinetic term has dimensions $[M_\Pl^2 \cdot \partial^2] = [M^4]$. The paper notes this on p. 6 ("Both $\Xi$-dependent terms in the bracket have mass dimension 4...") but the $M_\Pl^2$ prefactor on the kinetic term is non-standard in the canonical scalar-field literature, where $M_\Pl$ is usually absorbed into a canonically-normalized field $\phi = M_\Pl \Xi$. The footnote on p. 5 mentions this. I would prefer the paper to commit to one convention from the start, ideally the canonical $\phi$ convention with $V(\phi) = \Lambda^4 (\phi/M_\Pl) \log(\phi/M_\Pl)$, since that is what the EFT reader expects.

- **§3.1, Eq. 8:** "$M_\Pl^2 \Box \Xi = \Lambda^4 (1 + \log \Xi)$" — the sign convention $\Box = g^{\mu\nu}\nabla_\mu\nabla_\nu$ in $(-,+,+,+)$ gives $\Box \Xi = -\ddot\Xi - 3H\dot\Xi$ for homogeneous $\Xi$, hence the FRW EoM Eq. 23 is correct: $M_\Pl^2 (\ddot\Xi + 3H\dot\Xi) = -\Lambda^4(1 + \log\Xi)$. Confirm signs.

- **§3.4, Eq. 12:** $m_\Xi^2 = \Lambda^4 e / M_\Pl^2$, and the paper states $\Lambda \approx 1.7$ meV for $m_\Xi \sim H_0 \sim 10^{-33}$ eV. Sanity: $\Lambda^4 = m_\Xi^2 M_\Pl^2 / e \sim (10^{-33})^2 (10^{18})^2 / e \sim 10^{-30} / e \sim 10^{-30.4}$ eV$^4$, $\Lambda \sim 10^{-7.6}$ eV $\sim 25$ meV. The paper claims 1.7 meV. There is a factor-of-15 discrepancy with my sanity estimate; this is consistent with the "geometric factor relating $m_\Xi^2$ to $\rho_{c,0} = 3 H_0^2 M_\Pl^2$" mentioned on p. 8, but the paper should give the explicit relation rather than handwave.

- **§5.3, Late-time attractor:** "the damping term $3H\dot\Xi$ drives $\dot\Xi \to 0$ as $H$ remains positive." This relies on $H > 0$ in the asymptotic future. With a logarithmic potential bounded below, the late-time geometry approaches a de Sitter limit with $H_\infty^2 = -V(\Xi_0)/(3 M_\Pl^2) > 0$ — but $V(\Xi_0) = -\Lambda^4/e < 0$, so the contribution to $H^2$ from the bare scalar at the vacuum is negative. The renormalization by $\Lambda_{\rm bare}$ to give $\Lambda_{\rm obs} > 0$ is mentioned in §3.3 but not propagated through the late-time attractor argument. The reader needs to be told: in the freezing limit, what is $H_\infty$? Is it set by $\Lambda_{\rm obs}$? This needs a sentence.

- **§6.2, Eq. 31:** "$\Xi'_i = +0.470$, where the prime denotes $d/dN$ (e-folds derivative; the e-folds convention is used throughout the integration script)." This is the convention statement, but the paper's Eq. 17 ($\dot\Xi = H\Xi'$) and the corresponding cosmic-time IC $\dot\Xi_i = H(z_i) \Xi'_i$ should be derived explicitly so the reader can convert.

- **§6.3, "Sensitivity of $z_\star$ to fit parameters":** "varying $\Xi'_i$ in the range $[0.43, 0.50]$ moves $z_\star$ from $\approx 1.7$ to $\approx 1.25$ while keeping $w_0$ within $[-0.76, -0.81]$ and $\chi^2_{\rm Gauss}$ below 2." This suggests $z_\star \approx 1.3$ is achievable in this range, but my own runs do not reproduce $z_\star \approx 1.3$ at the documented IC. The sensitivity scan needs to be re-run and tabulated explicitly.

- **§6.4, fifth-force:** the paper states the minimal theory has no observable fifth force because $\Xi$ has no direct matter coupling. This is correct, but the fact that $\Xi$ is dimensionless and minimally coupled means that any operator linking $\Xi$ to the matter sector at the EFT scale would naturally be Planck-suppressed. A one-line quantitative estimate of the fifth-force suppression scale (e.g., "any conformal coupling $\beta \Xi T^{\rm SM}$ is suppressed by $1/M_\Pl$, giving fifth-force range $\sim 1/m_\Xi \sim H_0^{-1}$") would strengthen this section.

- **§7.4, Perturbations:** "the contribution of $\delta\Xi$ to the late-time matter power spectrum at $k \sim 0.1\,h/\rm Mpc$ is therefore at the percent level and below current Stage-IV sensitivity." This is the standard quintessence-perturbation result for $c_s^2 = 1$ canonical fields, but the paper should cite a specific reference for the quoted "percent level" and the "Stage-IV sensitivity" claim. Hu 1998, Bean-Doré 2004, Sapone-Kunz 2009, or the CMB-S4 forecast literature are appropriate.

- **§8 (Comparison Table):** the table should include $w_a$ for each potential, not just the late-time $w \to$ asymptote. Also, the "Notes" column for $V \propto \phi^p (\log \phi)^q$ Barrow-Parsons cites only the inflation application; please add a note that the $(p,q) = (1,1)$ subcase corresponds to the present model after dimensionless redefinition, and that this is acknowledged in the present paper as the closest structural relative.

- **§9 (Scope):** the bullet list is honest and is a model of disciplinary self-restraint. I commend the authors for it.

- **Bibliography:** typo in `Holsclaw2010GP`: "Sansó" should be rendered with the LaTeX `\'{o}` or the input text accent. Verify rendering.

- **Bibliography:** `AdamEtAl2025` is dated September 2025 (arXiv:2509.13302) — verify.

- **Bibliography:** `KouwnOh2012` has publication year 2014 in JKPS but ID-style "2012" — flag the inconsistency.

---

## 5. Line-by-line comments (selected)

- **Line 84 (abstract):** "Expanding about $\Xi_0$ gives a stable massive scalar with $m_\Xi^2 = \Lambda^4 e / M_\Pl^2$" — should be "stable, real, massive scalar."

- **Line 92 (abstract):** "$z_\star \approx 2$" — should be updated to $\approx 1.3$ to match the body, OR this sentence can be left as $\approx 2$ if the body is corrected to match. The two are inconsistent.

- **Lines 109-115 (abstract):** "The functional form $-\Xi\log\Xi$ coincides with the per-bin Gibbs integrand on a normalized probability distribution and with the Bialynicki-Birula–Mycielski nonlinearity in nonlinear quantum mechanics; both connections are structural rhymes (the present $\Xi$ is unbounded and unnormalized, not a probability density), cited as motivation for studying this functional form rather than as derivations." — this is a long sentence. Suggest splitting into two.

- **Line 156:** "this is generic for any dimensionless-field potential of the form $\Lambda^4 f(\Xi)$ and is not a feature peculiar to $\Xi\log\Xi$." Good clarity.

- **Line 167:** "the FRW trajectory is dual-regime" — define "dual-regime" on first occurrence (the abstract uses it without definition).

- **Line 188:** "having passed through the Type-F turnaround near $z \approx 1.3$" — should match Abstract.

- **Line 226 (§1, organization):** "Section §6 presents the observational program ..." — there is no §6 numbered explicitly; please verify section numbering matches the LaTeX file.

- **Lines 253–255:** "configurations leading to $\Xi \to 0^+$ during cosmic evolution are outside the field domain considered in this effective theory and are not considered." Repeated phrase "considered ... considered." Edit.

- **Line 350 (Eq. 11):** "$\Xi_0 = e^{-1} \approx 0.36788$" — give one more digit (e^{-1} = 0.367879441) so the reader can verify.

- **Lines 468–470 (Prop. 5.1):** "On the monotone rolling solutions studied numerically, with $\Xi > \Xi_0$ and $\rho_\Xi > 0$ over the fitted redshift range, the kinetic term decreases as the field approaches the minimum" — confirm "monotone rolling" includes the inbound leg of the dual-regime trajectory; clarify whether the proposition applies to the full trajectory or only $z < z_\star$.

- **Lines 475–479 (remark, "Bare vs renormalized"):** important and well-placed. Keep.

- **Lines 481–492 (remark, "On phantom crossing"):** the disclaimer "we treat the absence of phantom crossing as a property of the fitted branch rather than a global theorem" is honest. Good.

- **Lines 696–714 (§6.2 opening):** the IC convention discussion is the right content but is buried in a footnote. Move to main text.

- **Line 731:** "to be compared with $\chi^2_{\rm Gauss, \Lambda CDM} = 15.26$ for $(w_0, w_a) = (-1, 0)$" — give the reference for this $\Lambda$CDM Gaussian-summary chi-square, since the DESI 2024 VI paper uses different conventions. Verify by self-computation.

- **Lines 746–757 (table):** the $w(z)$ profile is the centerpiece. As noted in §3.1, my reproductions do not match this table. The table needs to be re-run from the canonical script and the script-paper cross-check tightened.

- **Lines 779–800:** the IC tuning paragraph is honest. Good.

- **Line 824:** "Total runtime is under 30 seconds on a standard laptop." Verified — `desi_xi_optimize_v2.py` runs in ~25 seconds on my system.

- **Lines 871–891 (Geometric anchor):** "The vacuum value $\Xi_0 = e^{-1}$ plays three independent roles in the model" — this paragraph is genuinely interesting and is the kind of structural observation that distinguishes the paper from a generic quintessence parameterization. Keep.

- **Lines 925–984 (F1–F5 falsifiability):** the criteria are well-stated. $(F_5)$ is the genuinely novel one and is correctly identified as requiring non-parametric reconstruction. Stage-IV reach citations are appropriate.

- **Lines 1041–1067 (EFT validity):** the transplanckian-field discussion is honest. The paper acknowledges no UV completion. This will be flagged by a careful referee but is severable.

- **Lines 1179–1209 (Comparison Table notes):** the discussion of distinctions from Chavanis 2022 logotropic is appropriate and is the right comparison to draw.

- **Lines 1213–1247 (§9 Scope):** the explicit "does not claim" list is excellent disciplinary practice. Recommend keeping.

---

## 6. Questions to the authors

1. **Reproducibility of $z_\star$.** Please supply a single canonical script that, when run with the IC of Eq. 31, reproduces the tabulated $w(z)$ profile and $z_\star \approx 1.3$ to four-digit accuracy. As described in §3.1, my own runs do not reproduce the documented $z_\star$ at the documented IC. Please reconcile.

2. **Convention round-trip.** The footnote on p. 12 claims that the script integrates from $z \approx 54$ and reads off the trajectory state at $z = 20$ to define $(\Xi_i, \Xi'_i) = (0.925, +0.470)$. Please supply the explicit upstream IC at $z = 54$ that yields these values at $z = 20$. My runs starting from `(xi_init=0.925, xi_dot=0.470)` at $z = 54$ do NOT produce $(\Xi, \Xi') = (0.925, +0.470)$ at $z = 20$ — they produce $(\Xi, \Xi') = (1.16, +0.11)$.

3. **Dimensional reconciliation.** Please supply the explicit relation between $\Lambda$ in physical units (meV) and $\Lambda^4/\rho_{c,0}$ in $\Omega$-units. The dimensional sanity check $\Lambda \sim (m_\Xi^2 M_\Pl^2/e)^{1/4}$ gives $\sim 25$ meV for $m_\Xi = H_0$, but the paper claims $\Lambda \approx 1.7$ meV. Please give the explicit factor of $\sqrt{3} \cdot e^{1/4} \cdot \ldots$ that maps these.

4. **Closure of $\Omega$ today.** Does the documented best-fit configuration $(\Lambda^4/\rho_{c,0}, \Xi_i, \Xi'_i) = (0.231, 0.925, +0.470)$ exactly satisfy $\Omega_m + \Omega_r + \Omega_\Xi = 1$ at $z = 0$, or is it approximately satisfied? If approximate, what is the residual?

5. **IC space of dual-regime trajectories.** What fraction of the $(\Xi_i, \Xi'_i)$ initial-condition space (at fixed $\Lambda$) realizes a Type-F turnaround on $0 < z_\star < 5$? Is the dual-regime traversal generic on the rolling branch, or does it require IC fine-tuning?

6. **Late-time $H_\infty$.** In the asymptotic Type-A regime ($z \to -1$, $\Xi \to \Xi_0 = e^{-1}$), what is the physical $H_\infty$? It cannot be set by $V(\Xi_0) = -\Lambda^4/e < 0$ alone, since that gives $H^2 < 0$. Please clarify the relation to the renormalized $\Lambda_{\rm obs}$.

7. **Phantom crossing on adjacent IC branches.** §5.2 Remark on phantom crossing notes that "the numerical solution exhibits $w_\Xi(z) \geq -1$ at all redshifts" on the rolling branch. What about adjacent branches (different IC)? The compute_zstar_v2.py script (older convention) shows trajectories that cross into phantom rapidly. Is this a numerical artifact of the older script's convention, or are there genuine phantom-crossing IC branches in the model that should be acknowledged?

8. **ISW signature of the dual-regime trajectory.** The local minimum of $w_{\rm DE}(z)$ near $z_\star \approx 1.3$ is in a redshift range where the integrated Sachs-Wolfe effect contributes to the late-time CMB. A back-of-envelope estimate of the ISW signature modification (without a full Boltzmann-code analysis) would significantly strengthen §7.4. Can the authors provide one?

9. **Companion-paper load-bearing.** The introduction's "Companions in the synthesis program" paragraph suggests that the combinatorial $\sigma(N) \le 2/N$ result and the $h/\beta = 1+\sqrt{3}$ four-core attractor are "the combinatorial-side input that, combined with the BBM separability uniqueness theorem, motivates the logarithmic functional form." Could the authors elaborate on the operational chain — what specifically does the $\sigma(N) \to 2/N$ rate contribute to the cosmological action? At present this reads as motivational framing rather than a substantive derivation, and §9 (Scope) explicitly states no derivation is claimed. If no operational chain exists, I recommend deleting the companion-paper paragraph from §1.

10. **The "Type-F regime" terminology.** Type-F as defined is an instantaneous condition ($\dot\Xi = 0$ at $z = z_\star$), not a phase. Could the authors clarify whether Type-F should be understood as a measure-zero point (in which case the terminology should reflect this) or as a finite neighborhood (in which case the threshold defining the neighborhood needs to be stated)?

11. **Literature framing of Albrecht-Skordis.** Albrecht and Skordis 2000 introduce a quintessence model with a tracking-to-freezing transition that is structurally similar in spirit to the present dual-regime traversal (different potential, different mechanism, but a single trajectory passing through two regimes). Could the authors comment on the similarities and differences to the present model?

12. **Citation of DR2 reconstruction papers.** `Wang2026QReconstruction` (arXiv:2603.21125) and `Adil2026Analytic` (arXiv:2603.14693) are dated 2026 and 2603 (?) respectively — please verify the arXiv IDs and confirm publication status. If these are in preparation, the citation should be marked accordingly.

---

## 7. Summary

The paper proposes a logarithmic-potential quintessence with an analytic vacuum at $\Xi_0 = e^{-1}$ and a genuinely novel dual-regime trajectory taxonomy (Type-T → Type-F → Type-A) that is outside the Caldwell-Linder freezing/thawing dichotomy. The theoretical content (action, vacuum, EoS, attractor) is solid and standard. The bibliography handles the major prior art well, with a few notable omissions (Boisseau et al., Albrecht-Skordis, Tsujikawa-Sami).

The empirical section (§6.2 DESI consistency check) has one disqualifying problem: the documented $z_\star \approx 1.3$ at the IC of Eq. 31 is not reproduced by any of the supplied verification scripts on independent execution. My runs at the documented IC give $z_\star \approx 2.13$, not 1.3. This must be reconciled before publication.

The IC tuning is honestly acknowledged but is a 2D family at fixed $\Lambda$, with no attractor mechanism. The $\chi^2_{\rm Gauss} = 1.24$ vs $\chi^2_{\rm Gauss, \Lambda CDM} = 15.26$ comparison is correctly disclaimed as Gaussian-on-summary, but the paper-internal numerical inconsistency between $\chi^2 = 1.24$ (body) and $\chi^2 = 1.52$ (Summary) needs to be reconciled.

I recommend **major revisions**, with the priority issues being:
1. Reproducibility of $z_\star \approx 1.3$ at the documented IC
2. Internal consistency of the $\chi^2$ value across body and Summary
3. Expanded IC-sensitivity scan to establish the dual-regime trajectory as generic on the rolling branch
4. Adding the missing prior-art citations (Boisseau et al., Albrecht-Skordis, Tsujikawa-Sami)
5. Updating the abstract to match the body's $z_\star \approx 1.3$

With a focused round of revisions on these points, this would meet JCAP's bar for a quintessence-model contribution with a novel trajectory taxonomy and a well-defined falsification program.

---

*Submitted to the JCAP Editorial Board, 2026-05-06.*
