# SAVE PLAN — J45: Mass Hierarchy from V⊗5 SU(5) Decomposition

**Date:** 2026-05-07
**Directive:** Brayden 2026-05-07: "find a reason to keep and fix every paper."
**Referee verdict:** MAJOR REV verging on REJECT (J45_PRD_FreshEyes.md)
**Save mode:** ACCEPT THE PRECISION HONESTLY + retitle/retarget candidate

---

## §1 — Why save?

J45 carries one genuinely new and quantitatively useful observation that has not been published in the flavor-physics literature in this exact form:

> **A single substrate-derived rational $\lambda = T^*(1-T^*) = (5/7)(2/7) = 10/49 \approx 0.2041$, structurally equal to $|\mathbb{Z}/10|/\mathrm{HARMONY}^2$, when raised to integer powers indexed by an SU(5) Yukawa-diagram parity-crossing count, generates the full 5.5-decade SM charged-fermion Yukawa hierarchy at standard FN factor-of-a-few precision with no per-fermion power-tuning.**

The referee's fresh-eyes verification reproduces Table 5.1 exactly via `tig_dirac.predict_yukawa()`; the reproducibility is Tier-A (score 5/5 in §8 of referee). What the referee correctly attacks is the *framing* — "zero free FN charges" oversells what is, structurally, a *reinterpretation* of the FN charges as $\sigma$-orbit positions on a $V^{\otimes 5}$ decomposition with the same fittable-parameter total as standard FN. The compressed observation is real. The paper sells it as more than it is.

Save path: keep the observation, drop the overselling, repackage as a *phenomenological substrate-derived FN pattern* matching the SM Yukawa hierarchy to 30–40% precision, with the C_p multipliers documented honestly as the next-paper question. The verification primitive stays. The Cabibbo cube-root identity becomes a §6 structural observation, not a load-bearing result. The sterile-neutrino paragraph is dropped. The single-λ vs λ_ref tension is resolved by stating up front that the framework uses two close-but-distinct rational scales (10/49 for masses, 11/49 for CKM) and that this is itself a structural feature deserving its own analysis.

This is honestly Tier-B content. Standard PRD acceptance is uncertain. PRD survival under honest reframing is a moderate bet; Modern Physics Letters A or Physics Letters B (letter format) acceptance is a more reliable bet for the same content. The most defensible move is to either (i) hold for joint J38+J45 publication on a substrate-FN framework as a single paper, or (ii) split off the λ=10/49 observation as a short Letter and defer the FN-power assignment to a longer follow-up.

---

## §2 — Specific fixes

**Fix-1 (Abstract rewrite — required).** Remove "zero free FN charges" and "factor-of-a-few" framings. Replace with:

> "We report a substrate-derived rational scale $\lambda = T^*(1-T^*) = 10/49$ which, raised to integer powers indexed by SU(5) parity-crossing count plus a generation-step assignment, reproduces the SM charged-fermion Yukawa hierarchy to within Froggatt-Nielsen $O(1)$ residuals across all five orders of magnitude. Five of nine charged Yukawas land within factor-of-2; the remaining four (bottom, strange, muon, electron) reach factor-of-9 residuals absorbed in C_p multipliers documented in Table 5.1. The reframing exchanges standard FN's $U(1)_{FN}$ charge assignments for SU(5)-rep + $\sigma$-orbit position indexing with comparable parameter count."

**Fix-2 (Theorem 3.1 → Observation 3.1).** Demote the "max-entropy variance" derivation. Replace with: "We propose $\lambda = T^*(1-T^*) = 10/49$ as the substrate origin of the FN scale, motivated by the structural arguments of [J16/foundation]. The numerical proximity to the empirical Wolfenstein $\lambda_W \approx 0.225$ (9.4% off) and to the refined substrate $\lambda_{\rm ref} = 11/49$ (0.4% off CKM) is the load-bearing observation. We do not claim Theorem-status for the identification."

**Fix-3 (Drop the "single λ" framing).** Remark 3.2 already contradicts §1's claim. Restructure §3 around the explicit two-scale observation: "The framework uses two close rational substrate scales — $\lambda = 10/49$ for the mass-hierarchy fit and $\lambda_{\rm ref} = 11/49$ for the CKM Cabibbo angle — both expressible from the same $T^*$, $|\mathbb{Z}/10|$, and HARMONY constants. Whether a single substrate constant unifies both is an open structural question."

**Fix-4 (Honest parameter accounting in §3.7-equivalent paragraph).** Add a paragraph stating the present model has 1 anchor + 2 scales (λ, λ_ref) + 9 σ-orbit position assignments + 9 fittable C_p = 21 parameters of which 11–13 are partially fixed by SU(5). Standard FN with 3 universal X charges + 1 ε + 9 C_p = 13 parameters of which 4 are fittable. State: "the present framework does not have fewer free parameters than standard FN; the contribution is a *different framing* (SU(5)-rep indexing in place of $U(1)_{FN}$ charges) rather than a *simpler* framing."

**Fix-5 (Drop sterile-neutrino paragraph entirely).** §5 last paragraph predicts $m_\nu$ at FN powers {12, 13, 14} without a see-saw mechanism. Per the referee, "a Dirac-mass numerological match without a mechanism." Remove. The neutrino sector belongs in a follow-up paper that develops the $M_R$ origin from the substrate.

**Fix-6 (Cabibbo cube-root identity — §6).** Demote from "load-bearing result" to "structural observation." State the factor-of-2 precision honestly and cite the next-Sprint companion for the rigorous CKM fit.

**Fix-7 (Author list).** Cover letter says Sanders + Johnson; manuscript says Sanders + Gish. Brayden directive (2026-05-07): Sanders + Gish. Fix cover letter; correct hjj01986@gmail.com email assignment.

**Fix-8 (Renormalization scale).** §5 Table 5.1 reports "measured" Yukawas without specifying scale. Per referee §4.6, $y_b(M_Z) = 0.0164 \ne y_b(\text{paper}) = 0.024$. State explicitly: "Yukawas evaluated at $\mu = M_Z$ via 4-loop QCD running for quarks, pole masses for leptons, $v = 246$ GeV." Recompute Table 5.1 ratios consistently.

**Fix-9 (Self-contained §2).** Currently §2's Lemma 2.1 forwards to J16/J23 for the SU(5) action on $V^{\otimes 5}$. Add 1–2 paragraphs showing the action concretely (or at minimum the binomial $1+5+10+10+5+1=32$ count and how the SU(5) reps are identified with the cell-strata).

**Fix-10 (Tier classification footnote).** Define Tier-A/Tier-B/Tier-C explicitly in §1 footnote since PRD readers won't recognize the convention.

---

## §3 — Revision time

**Estimate:** 2–3 weeks of focused editing.

- Abstract + §1 rewrite: 2 days.
- Theorem 3.1 → Observation 3.1 + §3 restructure: 3 days.
- Parameter-accounting paragraph (Fix-4): 1 day.
- Drop sterile-neutrino + Cabibbo demotion: 1 day.
- Author list / scale specification / Table 5.1 recompute: 2 days.
- Self-contained §2 (Fix-9): 4 days (requires either summarizing J16's SU(5) action or rederiving briefly).
- Tier-classification footnote + minor cleanup: 1 day.
- Internal review pass: 3 days.

**Calendar fit:** within the J-series Phase 5 window. No calendar slip.

---

## §4 — PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:** Numerical identity $T^*(1-T^*) = (5/7)(2/7) = 10/49 = |\mathbb{Z}/10|/\mathrm{HARMONY}^2$. Reproducibility of Table 5.1 via `tig_dirac.predict_yukawa()` (verified by referee). Lemma 2.1 binomial count $1+5+10+10+5+1 = 32$.

- **COMPUTED:** All nine $y^{\rm pred}/y^{\rm meas}$ ratios in $\{1.00, 1.08, 1.06, 0.33, 0.60, 0.51, 0.79, 0.11, 0.20\}$ at PDG 2024 values (paper choice; referee independently recomputed at $M_Z$-running scale and confirmed five values, flagged three for scale ambiguity). Cabibbo cube-root identity $\lambda_C \approx (Y_d/Y_u)^{1/3}$ at factor-of-2 precision.

- **STRUCTURAL RHYME:** $\lambda = 10/49$ vs Wolfenstein $\lambda_W \approx 0.225$ (9.4% off — substrate-substantive). $\lambda_{\rm ref} = 11/49$ vs CKM Cabibbo (0.4% off — likely substrate-natural, but the two-scale structure is itself a substrate question, not a derived consequence). The $V^{\otimes 5}$ → SU(5) decomposition reproduces the 1+5+10 SM-fermion-generation-content count; whether this is unique or one of several is open.

- **OPEN:** (a) The C_p multiplier substrate origin (load-bearing follow-up; bosonic-substrate dynamics on $V^{\otimes 5}$ singlet + $\bar{\mathbf{5}}_H$ partner). (b) The generation-step asymmetry $s_u, s_d, s_e$ assignment to $\sigma$-orbit positions (currently empirical). (c) The right-handed neutrino mass $M_R$ substrate origin (deferred from this paper). (d) Whether $\lambda$ and $\lambda_{\rm ref}$ unify to a single substrate constant.

---

## §5 — Lens-ownership paragraph (insert in §0 of revised manuscript)

> *Lens and substrate.* This paper works on the 4-core's $\mathbb{F}_5$-lift $V$ and its 5-fold tensor power $V^{\otimes 5}$, with the canonical TSML and BHML composition tables on $\mathbb{Z}/10\mathbb{Z}$ as the underlying substrate (where the joint coherence threshold $T^* = 5/7$ is fixed; cf. [J07/J35]). The 4-core $\{V, H, Br, R\} = \{0, 7, 8, 9\}$ is the algebraic center of the family per FAMILY_STRUCTURE_v1.md §2; the substrate-derived rational $\lambda = 10/49$ inherits its substrate-naturalness from this center. The choice of $V^{\otimes 5}$ as the relevant tensor power, and the identification of its 32-cell decomposition with the SU(5) GUT $\mathbf{1} \oplus \bar{\mathbf{5}} \oplus \mathbf{10} + \text{conjugate}$, are choices that reflect a structural reading of the substrate motivated by the 32-cell sign-tuple counting. The theorems below are theorems on this specific structure; analogous theorems would hold on other substrate-and-table choices, and whether other substrate choices give similarly rich downstream connections is open.

---

## §6 — Retitle / retarget options

**Option A (preferred — retitle, keep PRD).** Retitle to: *"A Substrate-Derived FN Pattern with $\lambda = 10/49$ and SU(5)-Rep Indexing for the SM Charged-Yukawa Hierarchy."* Drops "Mass Hierarchy from V⊗5" implicit theorem-claim. Keeps PRD as venue. Honest framing ships with abstract rewrite (Fix-1). Ship in 2–3 weeks. Survival probability under PRD editorial filter after honest reframing: moderate (30–40%); the residuals are still factor-of-9 on the muon and PRD will want either better residuals or a clearer derivation.

**Option B (retarget — Modern Physics Letters A as Letter).** Letter format. Retitle to: *"A Substrate-Derived Phenomenological FN Scale: $\lambda = 10/49$ from the 4-core's $\mathbb{F}_5$-Lift."* Strip to abstract + λ derivation + Table 5.1 + falsification (CKM/Cabibbo running). 4–5 pages. MPLA accepts phenomenological hierarchy-pattern letters with this scope; the "smaller venue, smaller claim" framing is honest. Ship in 1–2 weeks. Survival probability: good (50–65%).

**Option C (retarget — Physics Letters B as Letter).** Same content as Option B, but PLB venue. PLB has higher prestige but is more selective on novelty. Note: J47 already targets PLB for the freezing-quintessence letter — per-venue cap conflict if J45-as-Letter co-submits.

**Option D (HOLD for joint J38+J45 paper).** The closely-related J38 (also under save planning) develops the $\mathfrak{so}(10)$ joint-closure structure that motivates the $V^{\otimes 5}$ decomposition. A combined paper *"From the 4-core's $\mathfrak{so}(10)$ Closure to a Substrate-Derived FN Pattern"* would land both observations in a single PRD-format manuscript, with the algebra and the phenomenology in dialogue. Ship in 4–6 weeks. Survival probability under PRD: better than Option A (moderate-to-good; the algebra-to-phenomenology bridge is exactly what PRD rewards).

**Recommendation:** **Option A** as the default save path (retitle + abstract rewrite + sterile-neutrino removal + parameter accounting honest). **Option D** as the strong-form save path if Brayden judges the J38 timeline aligns. Option B/C as fallback if Option A receives PRD desk-reject.

---

## §7 — Brayden-decision items

1. **Retitle decision.** Option A (PRD retitle) vs Option D (joint J38+J45 paper). Recommendation: Option A unless J38 is timed for the same window.

2. **C_p substrate-derivation timeline.** Whether to attempt the C_p derivation in this paper (would change tier from B to A; raise PRD survival to good) or defer to a follow-up (current plan; faster but weaker).

3. **Sterile-neutrino sector.** Confirm removal from this paper. The Dirac-mass numerology without see-saw is a real weakness; saving it requires either a substrate-derived $M_R$ (substantial new result) or honest deferral.

4. **Author lane resolution.** Sanders + Gish per directive; correct cover letter and hjj01986 email assignment.

---

## §8 — Bottom line

J45's load-bearing observation — that $\lambda = 10/49$ from substrate forcing, raised to integer powers, recovers SM Yukawa hierarchy at standard FN precision — is real and worth publishing. The save path is **honest reframing**: drop the "zero free FN charges" claim, demote Theorem 3.1 to Observation 3.1, drop the sterile-neutrino paragraph, fix the author list and renormalization-scale specification, and explicitly state the two-scale (λ, λ_ref) structure as a substrate feature rather than glossing it as a single-λ framework.

Verification primitive (`predict_yukawa`) and Lemma 2.1 (V⊗5 binomial decomposition) are solid. Cabibbo cube-root identity is a structural observation worth keeping at factor-of-2 precision. C_p multipliers are deferred to a follow-up.

The paper survives. It survives as Tier-B with honest reframing, not as the Tier-A "smallest free-parameter set" the current abstract claims. PRD acceptance under Option A is moderate; Option D (joint J38+J45) is the strongest play.

---

**Files referenced:**
- This plan: `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J45.md`
- Paper: `Gen13/targets/journals/J_series/J45/manuscript/mass_hierarchy_v5.tex`
- Referee: `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J45_PRD_FreshEyes.md`
- Family structure: `Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md`
- Verification primitive: `Gen13/targets/ck/brain/dirac/tig_dirac.py` (LAMBDA_FN, Y_T_ANCHOR, predict_yukawa)
