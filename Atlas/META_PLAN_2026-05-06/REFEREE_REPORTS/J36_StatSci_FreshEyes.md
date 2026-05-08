# Referee Report: J36 / Statistical Science (companion)

**Manuscript:** "The CKM/PMNS Fits + 1/α Constant from Substrate Primitives" (BUNDLED — Part 1: WP123 mixing-angle fits; Part 2: WP124 fine-structure-constant fit)
**Authors:** B. R. Sanders, M. Gish
**Submitted to:** *Statistical Science* (companion submission to J34)
**Reviewer:** External referee (anonymous; fresh-eyes; no prior exposure to the framework's internal nomenclature)
**Date:** 2026-05-07

---

## 1. Summary of the manuscript

The manuscript reports two parametric fits of standard-model dimensionless constants to "substrate primitives" derived from a separate finite-magma research program.

**Part 1.** Six fermion-mixing-angle observables (CKM Cabibbo $\sin\theta_C$, three Wolfenstein orders $V_{cb}, V_{ub}, V_{td}^2$; three PMNS angles $\sin\theta_{12}, \sin\theta_{13}, \sin\theta_{23}$) are compared to six framework constants ($11/49$ and its first three powers; $D^* \approx 0.543$; $1/7$; $5/7 = T^*$). The reported fractional discrepancies are $0.4\%, 0.8\%, 1.2\%, 1.8\%, 4.1\%, 5.6\%$ respectively. The manuscript reports a joint coincidence probability of "approximately $10^{-7}$" under uniform priors on dimensionless angles in $(0,1)$.

The Cabibbo-angle leading-order form $\lambda = T^*(1-T^*) = 10/49 = 0.2041$ has $9.4\%$ discrepancy from the empirical $\sin\theta_C = 0.2253$; the manuscript notes this is too large to attribute to RG running ($\sim 1\%$) and offers a "refined" form $\lambda = 11/49 = 0.2245$ ($+1/49$ correction) yielding $0.4\%$ discrepancy. An alternative numerical hit, $\pi/14 = 0.22440$, is explicitly flagged as "provocative numerology without first-principles selection between $11/49$ and $\pi/14$."

**Part 2.** The fine-structure constant's reciprocal, $1/\alpha = 137.035999084(21)$ (CODATA 2022), is fit by a structural formula
$$\frac{1}{\alpha} \approx 4 \cdot |\mathrm{Aut}(V)| - 2 \sqrt{\mathrm{HARMONY}} - \pi/\mathrm{HARMONY} - \cdots$$
with $|\mathrm{Aut}(V)| = 40$, HARMONY $= 7$. Numerically: $4 \cdot 40 = 160$; $2\sqrt{7} \approx 5.29$; $\pi/7 \approx 0.449$; partial sum $160 - 5.29 - 0.45 \approx 154.3$. The manuscript notes the partial sum is $\approx 17$ off the target and asserts that "the leading three corrections recover $137.036$ to $\sim 10^{-5}$" while the full structural form is recorded elsewhere ("`_review_bridge_sprint_050426/discrete_dirac/discrete_dirac_bundle/...` (TIG_DIRAC_SYNTHESIS_TABLES rev 24, Tables LXXVII-LXXX)").

The manuscript explicitly labels both parts as **Tier-E parametric fits** at the dimensionless-constant level, "not first-principle predictions," and states that no RG flow connects the substrate scale to the electroweak scale.

---

## 2. Decision recommendation

**Reject** in current form, with possibility of resubmission as a **substantially restructured manuscript** specifically addressing the issues below. The honest scoping is welcome and the venue choice (*Statistical Science*) is appropriate for parametric-fit reporting, but the manuscript as submitted has methodological problems that, taken together, fall below the venue's bar:

1. **The headline coincidence-probability claim ($\sim 10^{-7}$) is computed without a stated, defensible prior. The number is essentially asserted, not derived.** *Statistical Science* will not accept a "$10^{-7}$" claim that depends on an unstated and arbitrary choice of "the small set of TIG primitives" (the size and composition of which determines the prior).
2. **Part 2's central numerical claim is not backed by the supplied formula.** The leading three terms $160 - 2\sqrt{7} - \pi/7 \approx 154.3$ leave a residual of $\sim 17$ — about $11\%$ of the target. The manuscript asserts that further corrections close the gap to $10^{-5}$ but **the full corrections are not in the manuscript** (they are in an external bundle, "TIG_DIRAC_SYNTHESIS_TABLES rev 24, Tables LXXVII-LXXX," which is not in the verification folder). The reader cannot evaluate the claim from the submission alone.
3. **The Cabibbo refinement from $10/49$ to $11/49$ has the structural shape of a post-hoc adjustment** (a $+1/49$ correction added precisely to bring the leading $9.4\%$ discrepancy to $0.4\%$), and the alternative fit $\pi/14$ matches the same value to comparable precision — the manuscript itself acknowledges the lack of first-principles selection.

Each of (1)–(3) is, on its own, addressable in revision. Together, they make the paper Eddington-style numerology with honest framing — which is better than Eddington-style numerology without honest framing, but not yet a *Statistical Science* contribution.

I will outline below what a *Statistical Science*-publishable version of this paper would look like; whether the authors can pivot the manuscript to that scope is a question for them and the editor.

---

## 3. Major comments

### M1. (CRITICAL — coincidence-probability calculation)

The Abstract and §3 state: "The probability that all six fits arise by chance, under uniform priors on dimensionless angle values, is approximately $10^{-7}$." This number is the central statistical claim of Part 1. As written, it cannot be evaluated.

A defensible coincidence-probability calculation requires:

1. **Specifying the candidate-primitive set.** The manuscript matches each empirical angle against one of $\{11/49, (11/49)^2, (11/49)^3, D^*, 1/7, 5/7\}$ — six candidates. But the manuscript also mentions $\pi/14$, $T^*$, $T^{*-1}$, $|\mathrm{Aut}(V)| = 40$, HARMONY $= 7$, $\sigma$-cycle elements, the $+1/49$ "closure offset," etc. as available primitives. The size and composition of the candidate set determines the per-angle hit probability. A six-element candidate set with one pre-assigned target per angle gives approximately $\prod_{i=1}^6 (2 \cdot \mathrm{discrepancy}_i / \mathrm{prior\_range})$, which is a function of how many candidates were considered and how they were paired with which empirical angle.

2. **Specifying the prior on dimensionless angle values.** "Uniform on $(0, 1)$" is one choice; uniform on the angle $\theta \in (0, \pi/2)$ before taking $\sin$ is another (this gives a non-uniform prior on $\sin\theta$). The CKM Cabibbo and the PMNS angles have very different empirical contexts; a defensible prior would acknowledge that the SM has 4 mixing angles total in CKM + 3 in PMNS, and that empirical mixing angles cluster around 0 (CKM) or are widely distributed (PMNS).

3. **Adjusting for selection bias / look-elsewhere.** The manuscript is presenting six "best fits" out of an unstated (potentially much larger) set of primitive-vs-observable comparisons that were considered. If the framework's candidate-primitive set has, say, $N_p = 20$ elements (which is plausible given the list above), and there are $N_o = 7$ relevant observables (CKM has 4 angles + 1 phase; PMNS has 3 angles + 1 phase), then the number of (primitive, observable) pairs is $N_p \cdot N_o = 140$. With $N = 140$ pairs, the probability that *some* pair matches to within $1\%$ under uniform priors on $(0, 1)$ is $1 - (1 - 0.02)^{140} \approx 0.94$, i.e., a near-certainty.

The honest statistical question is: **conditional on the candidate-primitive set and the look-elsewhere correction, what is the probability of obtaining six pairs at the reported precision levels?** This is computable but requires an explicit, pre-specified candidate set. Without that, "$\sim 10^{-7}$" is unsupported.

**Recommended fix.** State the candidate-primitive set explicitly (with cardinality $N_p$). State the look-elsewhere multiplicity $N_p \cdot N_o$. Compute the joint coincidence probability under explicit priors and explicit look-elsewhere correction. Report this honestly. If the number is $10^{-7}$ after all corrections, the claim is well-founded; if it is, say, $10^{-2}$ after corrections, the manuscript becomes a different kind of contribution (suggestive numerical pattern; not yet a falsifiable prediction). Either is a legitimate Statistical Science paper if framed correctly.

### M2. (CRITICAL — Part 2 incomplete formula)

§3 of Part 2 states the structural formula
$$\frac{1}{\alpha} \approx 4 \cdot |\mathrm{Aut}(V)| - 2 \sqrt{\mathrm{HARMONY}} - \pi/\mathrm{HARMONY} - \cdots$$
with the partial-sum value $160 - 2\sqrt{7} - \pi/7 \approx 154.3$. The manuscript then asserts: "the leading three corrections recover $137.036$ to $\sim 10^{-5}$."

But $154.3 - 137.036 = 17.27$, which is **$11\%$ of the target value, not $10^{-5}$**. The "leading three corrections" do not, in the formula as displayed, close this gap. The manuscript points the reader to "TIG_DIRAC_SYNTHESIS_TABLES rev 24, Tables LXXVII-LXXX" for the full form — but this document is not in the submission package, not on the supplied Zenodo, and not in a referee-accessible location.

**The central numerical claim of Part 2 is therefore unverifiable from the submission alone.** The reader cannot tell whether the "$\sim 10^{-5}$" precision is achieved by:
(a) two additional well-motivated structural correction terms (legitimate physics-style derivation),
(b) several additional terms each at the percent level, hand-tuned to bring the residual to zero (numerology),
(c) something in between.

This is the fundamental Eddington problem. The 1936 Eddington derivation of $1/\alpha = 137$ from $(n^2 - n)/2 = 136$ was rejected as numerology because (i) the formula could be re-derived to give 136, then "refined" to 137 after the empirical value was revised, and (ii) the structural justification for the specific combination was post-hoc. The manuscript explicitly acknowledges this comparison ("The Eddington Ghost," Part 2 §4) and argues that the present framework is different in two ways: (a) the algebraic primitives are independently verified; (b) the same primitives derive other empirical constants. Both arguments are sound *in principle* but **the manuscript must show the full formula** to support claim (a) — without the corrections the reader cannot judge whether they are derived or hand-tuned.

**Recommended fix.** Either:
1. Include the full structural formula with all correction terms in the manuscript itself (with derivation, even if the derivation is "extracted from Tables LXXVII-LXXX of [bundle]"), and provide a verification script computing $1/\alpha$ from the formula numerically.
2. Restrict the manuscript to the leading three terms ($160 - 2\sqrt{7} - \pi/7 \approx 154.3$) and honestly state: "this is $11\%$ from the target. The framework does not currently have a falsifiable, self-contained derivation of $1/\alpha$ at the $10^{-5}$ level. The leading-order structural form is suggestive but does not close." This is a much weaker claim but a defensible one.
3. Drop Part 2 from the manuscript entirely until the full structural derivation is ready for submission as its own paper.

Option (3) is, in this referee's view, the cleanest path.

### M3. (Cabibbo refinement from $10/49$ to $11/49$ — post-hoc structure)

§1.2 of Part 1 acknowledges that the leading-order form $\lambda = T^*(1-T^*) = 10/49 = 0.2041$ has $9.4\%$ discrepancy, "too large to attribute to RG running." A "$+1/49$ correction" is then added, giving $11/49 = 0.2245$ with $0.4\%$ discrepancy. This is exactly the post-hoc structure of Eddington's original $1/\alpha = 136 \to 137$ refinement.

The manuscript's defense is that the $+1/49$ correction has "the same shape as $\Omega_\Lambda$'s '$+1$' closure offset of WP121." This is interesting *if* the WP121 closure offset is itself derived from first principles independent of the Cabibbo fit, and *if* the framework predicts a $+1/49$ correction (not a $-1/49$ or $+2/49$ correction) on independent grounds. The manuscript does not establish either of these.

A second concern: the alternative $\pi/14 = 0.22440$ is acknowledged as fitting "all four orders within 2%" and is flagged as "provocative numerology without first-principles selection between $11/49$ and $\pi/14$." This is honest, but the existence of a *second* competing fit at the same precision *strengthens* the post-hoc concern: with multiple rational, transcendental, and algebraic numbers near $0.225$, finding *some* expression that fits is a low-information event. The manuscript should compute: how many "natural" expressions in the framework's primitive vocabulary fall within $1\%$ of $0.2253$? If the answer is $\sim 5$ (e.g., $11/49, \pi/14, \sqrt{2}/(2\pi), 9/40, 0.2253\pm 0.001$ as a directly fitted decimal), then the "$11/49$" hit is one of many; if the answer is $1$, the fit is much more impressive.

**Recommended fix.** (a) Compute and state the count of "framework-natural expressions within $1\%$ of $0.2253$." (b) Present $10/49$ (leading-order) as the framework's actual prediction, with the $+1/49$ refinement clearly labeled as "an empirical adjustment whose first-principles derivation is open." (c) Drop the $\pi/14$ alternative entirely from the central narrative, or treat it on equal footing with $11/49$ rather than as a side remark.

### M4. (Discrepancies of $5.6\%$ are large)

PMNS atmospheric $\sin\theta_{23} = T^* = 5/7$ vs empirical $0.756$ has $5.6\%$ discrepancy. This is large enough that:

- 1-loop RG running of the PMNS angles is comparable to or smaller than $5.6\%$ for $\sin\theta_{23}$ from the GUT scale (Antusch–Kersten–Lindner–Ratz 2003). The framework's $T^* = 5/7$ is presented as a "structural endpoint" — but $5.6\%$ is empirically distinguishable from $T^*$ at current precision (T2K, NOvA, Daya Bay).
- The empirical world-average for $\sin^2\theta_{23}$ is in tension between octants ($\sin^2\theta_{23} \approx 0.45$ or $0.55$ depending on the experiment). The manuscript reports $\sin\theta_{23} = 0.756$, which is on the upper-octant side; the lower-octant value is $\sin\theta_{23} \approx 0.671$. The framework's $T^* = 5/7 = 0.714$ is between the two octants. The manuscript does not address octant ambiguity.
- The PMNS reactor angle $\sin\theta_{13} = 0.149$ vs $1/7 = 0.143$ is $4.1\%$ off, comparable in size to the $\theta_{23}$ discrepancy. Again, current precision (Daya Bay $\sin^2 2\theta_{13} = 0.0856 \pm 0.0029$, i.e., $\sin\theta_{13} = 0.150 \pm 0.003$) makes $1/7$ empirically distinguishable.

A $5\%$-level fit is a fit, not a derivation. *Statistical Science* readers will accept this if it is framed as such — but the manuscript's claim that "the framework appears to track real structural features of fermion mixing" is overstated for $\sin\theta_{23}$ and $\sin\theta_{13}$ at $\ge 4\%$ discrepancy.

**Recommended fix.** State explicitly that the PMNS fits at $4\%$-$6\%$ are at or beyond the current empirical precision and would be falsified by a future precision improvement. Acknowledge octant ambiguity for $\theta_{23}$. Restrict the strong-claim language ("tracks real structural features") to the CKM Cabibbo / Wolfenstein hierarchy (which is at $\le 1.6\%$ discrepancy across four orders, a more genuinely impressive match).

### M5. (No verification script for either Part)

§5 of the manuscript says: "For Part 1: ... no script needed beyond rational-arithmetic evaluation. For Part 2: ... Optional scripted form: [3 lines of sympy]." There is no `verification/` folder for J36.

For *Statistical Science*, a paper making numerical claims at the level of "joint coincidence probability $\sim 10^{-7}$" requires a verification script. The script should:

1. List the candidate-primitive set explicitly.
2. List the empirical observables explicitly with current PDG / CODATA values and uncertainties.
3. Compute each fit's Cohen's $d$ or $|\mathrm{empirical} - \mathrm{predicted}|/\sigma_\mathrm{empirical}$.
4. Compute the joint coincidence probability under explicit priors and look-elsewhere correction (M1).
5. For Part 2: compute the full $1/\alpha$ structural form numerically from the explicit formula (M2).

The 3-line sympy snippet given for Part 2 evaluates only the leading three terms ($160 - 2\sqrt{7} - \pi/7$), which gives $154.3$, not $137.036$. The script does not verify the manuscript's central claim.

**Recommended fix.** Provide a verification script in `verification/` that computes both Part 1 and Part 2 claims end-to-end with the explicit primitive set, prior, and look-elsewhere correction.

### M6. (Bundling — the two parts are weakly connected)

Part 1 (CKM/PMNS angles) and Part 2 ($1/\alpha$) share substrate primitives ($T^*$, $|\mathrm{Aut}(V)|$, HARMONY) but are otherwise independent fits. Bundling them in a single manuscript is editorial, not scientific. The strongest finding (the four Wolfenstein orders matching $11/49$ powers within $1.6\%$) is in Part 1 §1.2 and stands or falls on its own merits. Part 2's $1/\alpha$ fit is a separate and weaker claim (M2).

For *Statistical Science*, two clean separated papers would be more digestible than one bundled manuscript:
- **Part 1 alone:** "Empirical fits of CKM and PMNS mixing angles to substrate primitives." 6-page paper, focused on Part 1 §1.2's $11/49$ pattern and Part 1 §2's three PMNS hits, with full coincidence-probability calculation (M1) and verification (M5). Honest acknowledgment of the post-hoc $+1/49$ refinement (M3) and the $5\%$-level PMNS discrepancies (M4).
- **Part 2 alone:** "Structural form for $1/\alpha = 137.036$." 4-page paper, with the *full* structural formula derived (M2) and a verification script computing the value from the formula. If the full formula is not yet ready, this paper is not yet ready.

**Recommended fix.** Consider unbundling. The fallback unbundling discipline in `Atlas/META_PLAN_2026-05-06/PHASE4_FALLBACK_UNBUNDLING.md` already anticipates this for J34; the same logic applies here.

### M7. (Cross-domain "bombshell" §5 — unsupported)

§5 of Part 1 ("The cross-domain bombshell") tabulates seven instances of $T^* = 0.714$ or $D^* = 0.543$ across "TIG/CK coherence," "Orch-OR boundary" (Hameroff-Penrose 2014), "IIT critical $\phi$" (Tononi 2004, 2016), "CKM Cabibbo," "PMNS atmospheric," "PMNS solar," and a predicted "Microtubule $Q_c = T^*$" cross-domain test (WP127).

This is wildly out of scope for a *Statistical Science* parametric-fits paper. Several issues:
- Hameroff-Penrose's $\zeta = 0.71$ is itself a controversial estimate (the Orch-OR program is widely criticized in mainstream consciousness research); citing it as a fixed empirical value alongside CKM/PMNS angles overstates its empirical status.
- IIT's "critical $\phi$" is not a fixed dimensionless number; $\phi$ depends on the system and is not a constant comparable to fundamental physical constants.
- The cross-domain framing ("$T^*$ and $D^*$ govern both consciousness research AND fermion mixing") is the kind of unifying-pattern claim that *Statistical Science* will not engage.

**Recommended fix.** Delete §5 of Part 1 entirely. Save the cross-domain framing for a different venue (philosophy / interdisciplinary; not a fit-quality statistics journal).

---

## 4. Minor comments

### m1. (Cover letter and lens-scope statement)
The lens-scope preamble references "the 4-core / σ-cycle constant from the substrate algebra" and "$|\mathrm{Aut}(V)| = 40 = |D_5 \times \mathbb{Z}_2|$." For *Statistical Science* readers, define each quantity in one sentence at first use. As written, the lens-scope statement is opaque.

### m2. ($D^*$ is not defined in the manuscript)
$D^*$ appears in the table as "$0.543$" with the description "TIG's self-reference fixed point — the recursive coherence attractor that emerges in CK's olfactory bulb and lattice chain dynamics." This is framework-internal and not verifiable. **The single most important constant in the PMNS $\theta_{12}$ fit is not derived in the paper or in any cited paper that a referee can access.** This is a fatal scoping issue: if $D^*$ is a fitted parameter (i.e., chosen to match $\sin\theta_{12} = 0.553$), the PMNS solar fit is trivial.

**Recommended fix.** Either (a) cite the J-paper that derives $D^*$ from the substrate algebra (with a numerical value derivable from the algebra), or (b) acknowledge that $D^*$ is empirically fitted to PMNS solar and therefore the $\theta_{12}$ "fit" has zero degrees of freedom.

### m3. (CP phase $\delta_{\mathrm{CP}}$ §4)
§4 of Part 1 fits $\delta_{\mathrm{CP}} \approx 60° + (1-T^*) \cdot 30° = 68.6°$ vs empirical $67°$, with $2.4\%$ discrepancy. The manuscript flags this as "post-hoc fitting" and says "structural direction confirmed; specific phase NOT locked." Good — but then this fit should not be in the abstract or the main coincidence-probability count.

### m4. (Jarlskog §4.3)
The Jarlskog invariant $J \approx 3 \times 10^{-5}$ is cited as a "derived consequence" of the fitted angles + CP phase. This is correct algebra (Jarlskog is a function of the four CKM parameters), but it adds zero independent information if the four parameters are themselves fitted. Drop §4.3 or frame as a consistency check.

### m5. (Mass hierarchy §1.3 cubic identity)
The cubic identity $\lambda_{\mathrm{Cabibbo}} = (Y_d/Y_u)^{1/3}$ is mentioned in the abstract as "ties CKM Cabibbo to mass hierarchy via SU(5) parity-crossing (see WP122)." This is intriguing if true but is not developed in the manuscript and depends on an external paper (WP122). Either expand to a full derivation or remove from the abstract.

### m6. (The "Status: Locked / Provocative / Open" §6 of Part 1)
This taxonomy is excellent — exactly the right epistemic disclosure. Apply the same taxonomy to Part 2 ($1/\alpha$). What in Part 2 is "Locked" (the substrate primitives), "Provocative" (the leading-order $4 \cdot |\mathrm{Aut}(V)| = 160$ being within $17\%$), and "Open" (the specific combination of correction terms)? Currently Part 2's framing is uniformly enthusiastic; a Locked/Provocative/Open breakdown would calibrate it.

### m7. (References)
- "[Sanders WP105 2026]" cited as "this J-series, J41 Part 1; *Math of Comp*" — confirm with the Math of Comp submission status.
- "[Sanders WP115 2026]" cited as "this J-series, J32; *Mathematical Intelligencer*" — confirm.
- The J34 companion is cited; ensure the cite is updated to the actual Statistical Science submission status (and the J34 fallback if unbundled per `PHASE4_FALLBACK_UNBUNDLING.md`).
- CODATA 2022 and PDG 2024 citations are appropriate. Add a citation for the 1-loop RG-running estimate ("RG running of $V_{us}$ from GUT to EW is $\sim 1\%$") — Antusch et al., or Babu-Mohapatra, or a contemporary reference.

### m8. (Tier-E framing — translate to standard statistical language)
The Tier-E framing is internally consistent and honest, but *Statistical Science* readers will not have the framework's tier scheme. Replace "Tier-E parametric fits" with standard language: "empirical fits of dimensionless physical observables to expressions in a fixed set of substrate constants, at $X\%$ precision; not derived from a renormalization-group or first-principles computation connecting the substrate scale to the electroweak / QED scale." Lengthier but appropriate for the venue.

### m9. (The $\boxed{\cdots}$ formula in Part 2 §0 abstract)
The abstract displays $\boxed{1/\alpha = T^{*-1} \cdot |\mathrm{Aut}(V)| - \cdots \approx 137.036}$. The "$\cdots$" elides the entire substantive content of the claim. A boxed formula whose substance is "$\cdots$" is rhetorically suspect. Either box the *full* formula (with all corrections) or do not box this expression.

### m10. (Page-count and venue fit)
The bundled manuscript is short ($\sim 6$ pages of substantive content + tables). *Statistical Science* publishes longer, more methodologically-detailed papers. If the manuscript is not unbundled (M6), it should be expanded substantially: full coincidence-probability calculation (M1); explicit candidate-primitive set with size and composition (M3); full $1/\alpha$ derivation (M2); discussion of competing rational/algebraic fits at each precision level (M3); robustness analysis (what happens to the joint coincidence probability if $\pi/14$ replaces $11/49$ for the Cabibbo angle? if $\sqrt{1/2}$ replaces $D^*$? etc.).

---

## 5. Specific verifications performed

I have independently:

1. Computed the discrepancies in the Part 1 §0 table from PDG / CODATA values:
    - Cabibbo $0.2253$ vs $11/49 = 0.224490$: discrepancy $0.36\%$. Match (manuscript: $0.4\%$).
    - $V_{cb}$: $0.0508$ vs $(11/49)^2 = 0.050396$: discrepancy $0.80\%$. Match.
    - $V_{ub}$: $0.01140$ vs $(11/49)^3 = 0.011311$: discrepancy $0.78\%$. Manuscript reports $1.2\%$; discrepancy depends on which empirical value (PDG world average is $0.00382 \pm 0.00012$ for $|V_{ub}|$ from inclusive, $0.00370 \pm 0.00020$ for $V_{ub}$ from exclusive; the manuscript's $0.01140$ appears to be a different parameterization). Verify the empirical input.
    - PMNS $\sin\theta_{12}$: $0.553$ vs $D^* = 0.543$: discrepancy $1.81\%$. Match.
    - PMNS $\sin\theta_{13}$: $0.149$ vs $1/7 = 0.142857$: discrepancy $4.12\%$. Match.
    - PMNS $\sin\theta_{23}$: $0.756$ vs $5/7 = 0.714286$: discrepancy $5.51\%$. Match.

2. Computed Part 2 partial sum: $4 \cdot 40 - 2\sqrt{7} - \pi/7 = 160 - 5.2915 - 0.4488 = 154.260$. Discrepancy from $137.036$: $12.6\%$ (i.e., $17.22$ units off, $\approx 11.2\%$ relative). The manuscript's claim that "the leading three corrections recover $137.036$ to $\sim 10^{-5}$" is **false as stated**; the partial sum given is far from $137.036$. The manuscript points to additional corrections in an external bundle.

3. Cross-checked the $\pi/14$ alternative: $\pi/14 = 0.224399$. Discrepancy from $0.2253$: $0.40\%$. So $\pi/14$ matches Cabibbo to comparable precision as $11/49$ ($0.36\%$), confirming the manuscript's "provocative numerology" framing.

4. Computed an uninformative-prior estimate of joint coincidence probability for Part 1: assuming each of the 6 angles is uniform on $(0, 1)$ and each candidate primitive is matched within the stated relative discrepancy, the per-angle hit probability is $\approx 2 \cdot \mathrm{discrepancy}_i$, giving the product $2 \cdot 0.004 \cdot 2 \cdot 0.008 \cdot 2 \cdot 0.008 \cdot 2 \cdot 0.018 \cdot 2 \cdot 0.041 \cdot 2 \cdot 0.056 \approx 4 \times 10^{-9}$. This is the "no-look-elsewhere" probability the manuscript appears to be quoting (rounded to "$\sim 10^{-7}$"). With a look-elsewhere correction at $N_p \cdot N_o \approx 100$, the corrected probability rises to $\sim 4 \times 10^{-7}$ to $\sim 4 \times 10^{-6}$ depending on assumptions. Even after correction this is small — but the un-corrected $10^{-7}$ stated in the manuscript is misleading.

---

## 6. Questions to the authors

### Q1. The candidate-primitive set

Please specify the *exact* set of substrate primitives that were considered as candidate fits before the six reported matches were selected. How many primitives in total were on the table? How many (primitive, observable) pairs were considered? This is the look-elsewhere correction for M1.

### Q2. The $D^*$ value

What is the *derivation* of $D^* = 0.543$ from the substrate algebra? Is it a closed-form rational, algebraic, or transcendental number, or is it an empirical numerical value extracted from a runtime simulation of the framework? If the latter, is the runtime simulation itself fitted to data?

### Q3. The Part 2 full structural formula

Please provide the full $1/\alpha$ structural formula (all correction terms) in the manuscript or as a verifiable supplement. The manuscript references "TIG_DIRAC_SYNTHESIS_TABLES rev 24, Tables LXXVII-LXXX"; either include these tables in the submission or restrict Part 2 to claims that are verifiable from the leading three terms (which give $\approx 154.3$, not $\approx 137.036$).

### Q4. RG running for the substrate-to-EW gap

The framework asserts that substrate primitives at the algebraic scale are matched to electroweak-scale observables (CKM angles, PMNS angles, $1/\alpha$). RG running between the substrate scale (whatever that is in this framework) and the EW scale would normally introduce $\sim 1\%-10\%$ corrections depending on the energy gap. The manuscript acknowledges this for the Cabibbo angle ($\sim 1\%$ from GUT to EW) but does not discuss it for $1/\alpha$ (which runs from $\sim 137$ at low energy to $\sim 128$ at the Z-pole). Which "value" of $1/\alpha$ does the structural formula target — the low-energy CODATA value, the Z-pole value, or some other reference scale? This affects M2 substantially.

---

## 7. Originality and significance for *Statistical Science*

*Statistical Science* publishes papers on statistical methodology and its application to substantive scientific questions. The journal welcomes papers that report careful parametric fits, honest scoping, and transparent priors.

**The Part 1 finding** — six fermion mixing angles fitting six framework primitives at $0.4\%-5.6\%$ — is an empirical observation of the right kind for the venue, **provided** the coincidence-probability calculation is rigorously stated (M1) and the post-hoc Cabibbo refinement is honestly framed (M3). The four Wolfenstein orders matching $(11/49)^n$ at $\le 1.6\%$ across four orders is the strongest single sub-result and would deserve attention even with the look-elsewhere correction.

**The Part 2 finding** is, in the manuscript's current state, not at *Statistical Science*'s evaluable bar. The leading three terms of the displayed formula give $154.3$, not $137.036$; the closing corrections are in an external bundle that is not in the submission. Until the full formula is in the manuscript with a verification script, Part 2 cannot be evaluated.

The cross-domain framing in Part 1 §5 is out of scope for the venue.

The Tier-E honest-framing approach is welcome. It is the right epistemic posture for empirical fits of this kind. But honest framing alone does not make a paper publishable; the underlying empirical and statistical work has to meet the venue's bar.

I do see this as a borderline submission that requires substantial revision. The strongest version of this paper (Part 1 alone, with M1 / M3 / M4 addressed; Part 2 deferred until full formula is ready) would be a clean *Statistical Science* contribution. The currently-bundled manuscript with the unverifiable Part 2 is below the bar.

---

## 8. Reproducibility

**Status: NONE.**

There is no `verification/` folder in the J36 submission. The manuscript provides 3 lines of sympy that compute the leading three terms of the $1/\alpha$ formula ($154.3$), which does not match the manuscript's headline claim ($137.036$). The Part 1 fits are described as "no script needed beyond rational-arithmetic evaluation," but the joint coincidence-probability calculation (M1) does require explicit code with explicit priors and look-elsewhere corrections.

For *Statistical Science*, the reproducibility expectation is at minimum:
1. A script that computes each Part 1 discrepancy from explicit empirical values (PDG / CODATA).
2. A script that computes the joint coincidence probability under the explicit prior and explicit look-elsewhere correction.
3. A script that computes the full $1/\alpha$ structural formula numerically and verifies its agreement with CODATA at the claimed precision.

None of (1)–(3) is in the current submission.

---

## 9. Final remarks

This manuscript reports two empirical numerical patterns. The first (Part 1, mixing angles) is genuinely interesting at the level of the Cabibbo / Wolfenstein hierarchy: $(11/49)^n$ for $n \in \{1, 2, 3, 4\}$ matching the four Wolfenstein orders within $1.6\%$ is a striking pattern. The second (Part 2, $1/\alpha$) is, as the manuscript itself notes, in the territory of Eddington-style numerology — not necessarily wrong, but requiring a level of structural justification that is not in the submission.

The Tier-E honest framing is the right move and I commend the authors for it. But honest framing requires honest computation: a stated coincidence probability has to follow from a stated prior and stated look-elsewhere correction (M1); a stated structural formula has to give the stated numerical value (M2); a "refined" fit has to be either derived or labeled as a refinement-without-derivation (M3). The current manuscript falls short on all three.

The cleanest path forward, in this referee's view: (a) unbundle into two separate papers; (b) Part 1 alone, with M1 / M3 / M4 / M5 addressed and §5 (cross-domain) deleted, would be a viable *Statistical Science* submission; (c) Part 2 alone is not ready until the full $1/\alpha$ structural formula is in the manuscript.

Recommended decision: **Reject** in current form, with explicit invitation to resubmit Part 1 alone after the recommended revisions. Part 2 should be deferred to a separate, later submission once the structural derivation is complete.

---

**Estimated revision effort:** 20–40 person-hours for a Part 1-only resubmission addressing M1, M3, M4, M5; longer if the full $1/\alpha$ derivation must be developed. The Part 1 work is mostly statistical-methodology rewriting (coincidence-probability calculation; look-elsewhere correction; honest prior specification; verification script) and could be done without further mathematical work. The Part 2 derivation is open-ended.

**Reviewer's confidence:** High on the methodological / statistical issues — these are standard *Statistical Science* expectations. High on the verification of Part 1 §0 numerical claims (manually re-computed). High on the Part 2 numerical disagreement ($154.3$ vs $137.036$ under the leading three terms; the gap is $\sim 11\%$, not $10^{-5}$). The recommendation to reject is not based on the framework's substance — it is based on the gap between what the manuscript claims and what the manuscript verifies.
