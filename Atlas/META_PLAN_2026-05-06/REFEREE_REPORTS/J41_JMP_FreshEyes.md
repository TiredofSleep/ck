# Referee Report: J41 / JMP

**Manuscript:** "The Yang-Mills Mass Gap Bridge: Substrate-Algebra Predictions from Separability-Forced Spectral Floor"
**Authors:** B. R. Sanders, H. J. Johnson
**Submitted to:** Journal of Mathematical Physics (companion to J40)
**Reviewer:** External referee (anonymous), fresh eyes
**Date:** 2026-05-07

---

## 1. Summary of the manuscript

The authors propose to apply the Bialynicki-Birula (BB) bridge developed in the companion paper J40 to the Yang-Mills (YM) mass gap problem. The structural argument has three steps.

(C1) **Spectral floor of the BB-lifted theory (Proposition 2.1).** From the companion J40, the BB-forced potential is $V(\Xi) = \kappa\,\Xi \log \Xi$. The authors observe (by direct calculation) that this potential has unique minimum at $\Xi_0 = e^{-1}$ with $V''(\Xi_0) = \kappa/\Xi_0 = \kappa e > 0$. Hence the fluctuation field $\delta\Xi$ has tree-level mass $m_\Xi^2 = \kappa e$ — a positive spectral floor "forced by separability."

(C2) **Confinement as effective infrared separability (Proposition 3.1, heuristic).** YM is not directly in the BB class because the gauge self-coupling $g f^{abc} A_\mu^b A_\nu^c$ violates separability. The authors invoke the standard physics intuition that confinement realizes effective infrared separability — color singlets in the long-distance theory factor approximately as composite operators, and a glueball "in Tokyo" and a glueball "in New York" decouple in cluster decomposition.

(C3) **Conjecture 3.2 and a falsifiable numerical prediction.** From (C1) plus (C2), the authors propose that the YM mass gap arises by the same separability-forcing mechanism. The numerical prediction is

$$\Delta_{\rm YM} = C \cdot \Lambda_{\rm QCD} \cdot e$$

with $C$ an $O(1)$ constant. The lattice value $m_G \approx 1.7$ GeV for the lightest SU(3) glueball gives $C = m_G / (\Lambda_{\rm QCD} \cdot e) \approx 1.7 / (0.3 \times 2.718) \approx 2.08$, which the authors argue is "consistent with the Casimir factor $C_2(\mathrm{adj}) = N_c = 3$ for SU(3) (factor of $N_c / (\sqrt{N_c} \cdot \mathrm{normalization})$ depending on convention)."

Three Prerequisites (5.1 Wightman in 4D for the log theory; 5.2 effective IR separability of confined YM; 5.3 gauge-fixing-compatible BB) are listed as the open content. The §6 status table classifies this as Tier 4 framework.

The paper is short (3 pages of mathematical content + 1 page of prerequisite sub-section + references), with no dedicated verification script (the calibration $C \approx 2.08$ is computable in one line; structural claims defer to J40's `proof_separability_bridge.py`).

I have read the manuscript end-to-end and re-derived the calibration (a one-liner; details in §5 below).

---

## 2. Decision recommendation

**Major revisions** (close to "Reject in current form, encourage resubmission to a more appropriate venue" — the paper is too short and too schematic for JMP standard, the central conjecture (3.2) is loosely stated, the Casimir / "$C \approx 2$" justification is hand-wave, and the manuscript leans heavily on the companion J40 for any actual mathematical content).

The honest reading of this manuscript: it is a 3-page "structural commentary" applying J40's BB-bridge framework to the YM problem. The genuine mathematical content is one direct calculation (Proposition 2.1: $V''(e^{-1}) = \kappa e$, two lines), one heuristic statement (Proposition 3.1: confinement = effective IR separability), one conjecture (3.2: YM mass gap via separability mechanism), and one numerical comparison (Section 4: $C \approx 2.08$). Everything else is interpretive prose, references to the companion paper, or open-problem statements.

JMP can publish framework / commentary papers, but typically expects substantially more technical development than is provided here. As written, the manuscript reads more like a *commentary* on J40 than a stand-alone JMP submission. Consider:

- **The calibration $C \approx 2.08$ is sensitive to inputs.** With $\Lambda_{\rm QCD} = 0.25$ GeV (a defensible choice in some schemes), $C = 2.50$. With $\Lambda_{\rm QCD} = 0.4$ GeV, $C = 1.56$. With $m_G = 1.5$ or $1.85$ GeV (the lattice 0$^{++}$ glueball is known to ~10–15%), $C$ ranges from $1.84$ to $2.27$. The "consistent with $C_2(\rm adj) = 3$" comparison depends on which combination of inputs is used. A single-number prediction of $2.08$ is not justified by the lattice and theoretical inputs available.

- **The Casimir argument is hand-wave.** The text says "consistent with the Casimir factor $C_2(\mathrm{adj}) = N_c = 3$ for SU(3) (factor of $N_c/(\sqrt{N_c} \cdot \mathrm{normalization})$ depending on convention)." With the convention factor unspecified, *any* $O(1)$ value can be declared "consistent." The argument as written is unfalsifiable: there is no specific normalization that would predict $C = 2.08$ from $C_2(\mathrm{adj}) = 3$ in advance.

- **A non-trivial test would be the gauge-group dependence.** SU(2), SU(3), SO(N) glueball masses have been computed on the lattice [Lucini-Teper-Wenger 2004, Morningstar-Peardon 1999]. If the BB-bridge prediction is $\Delta_{\rm YM} = C(G) \cdot \Lambda(G) \cdot e$ with $C(G)$ a function of the Casimir, then the *ratio* $C(\rm SU(3)) / C(\rm SU(2))$ is a parameter-free prediction that the manuscript could test. As written, the manuscript fits one number ($C(\rm SU(3))$) and declares the calibration "consistent." This is not the same as a falsifiable prediction.

- **Conjecture 3.2 is conceptual, not mathematical.** It states "the YM mass gap … arises from the same mechanism as the BB-lifted-theory mass gap: separability forces a spectral floor." This is a *physics interpretive statement*, not a precise mathematical conjecture. JMP-grade conjectures usually have the form "Statement X about object Y in space Z holds under hypotheses W." Conjecture 3.2 has none of these specifications.

- **Prerequisite 5.1 is a 50-year-old open problem.** Wightman axioms for the $\log$ theory in 4D would imply, *inter alia*, the existence of a strongly-coupled scalar QFT in 4D with non-trivial spectral measure — i.e., a constructive QFT on which the entire 1970s/80s Glimm-Jaffe / Fröhlich program was unable to make decisive progress. Citing this as a "Prerequisite" without commentary on its status (no progress in 50 years) makes the framework look unattainable.

None of these issues is fatal *in principle* — the manuscript could survive revision as a JMP framework note if M1–M3 below are addressed. But the current form is too thin for JMP. Recommendation:

- (Path A) **Substantial expansion + technical development**: extend Section 4 to a multi-gauge-group prediction, with $C(G)$ computed from the assumed mechanism; add a serious sub-section on what "effective IR separability" would mean in cluster-decomposition language (Strocchi 2013 framework); reformulate Conjecture 3.2 with precise hypotheses on the YM theory and the BB bridge. This brings the paper closer to JMP-standard.

- (Path B) **Move to a more appropriate venue**: *Letters in Mathematical Physics* or *Communications in Mathematical Physics* "Physics Letters" section would be more appropriate venues for a short structural commentary of this length and depth. JCAP would also accept this if the cosmological connection (J03) is stated.

- (Path C) **Merge with J40**: the 3 pages of YM commentary could naturally be a §7 "An application to the YM mass gap problem" of J40, with the YM-specific Conjecture 3.2 and prediction sitting alongside the NS-specific Conjecture 5.2. A single 30-page JMP paper covering BB-bridge + NS + YM would be a stronger contribution than the current J40 + J41 split.

The author's choice between A, B, and C is a judgment call, but the current J41 standalone is too short for JMP.

---

## 3. Major comments

### M1. The numerical prediction $C \approx 2.08$ is sensitive to inputs (CRITICAL)

The claimed calibration $C = m_G / (\Lambda_{\rm QCD} \cdot e) \approx 2.08$ uses $m_G = 1.7$ GeV (lattice SU(3) 0$^{++}$ glueball, central value) and $\Lambda_{\rm QCD} = 0.3$ GeV (a choice from the asymptotic-freedom $\overline{\rm MS}$ scheme). Both inputs have substantial uncertainty:

- **$m_G$.** The 0$^{++}$ glueball on the lattice has been computed by Morningstar-Peardon (1999), Chen *et al.* (2006), and many follow-ups. Recent values are in the range $1.6$–$1.9$ GeV depending on the lattice action, scale-setting choice, and continuum extrapolation. The $\sim 10$\% spread is well-documented.

- **$\Lambda_{\rm QCD}$.** Even within $\overline{\rm MS}$, the value of $\Lambda_{\rm QCD}^{(N_f=3)}$ at the relevant scale ranges from $0.2$ to $0.4$ GeV depending on the coupling-constant input used. The lattice $\Lambda$ is itself scheme-dependent.

Together, the calibration $C$ has a range of roughly $1.5$ to $3.0$, *not* "$\approx 2.08$." The manuscript should report this range and interpret the calibration as falsifiability bounds, not as a fit to a specific number.

A more honest formulation: "The BB-bridge framework predicts $\Delta_{\rm YM} = C \cdot \Lambda_{\rm QCD} \cdot e$ with $C = O(1)$. The lattice 0$^{++}$ glueball mass and standard $\Lambda_{\rm QCD}$ scale-setting yield $C$ in the range $1.5$–$3.0$, consistent with $O(1)$. A more demanding test would require a parameter-free prediction of $C(G)$ as a function of the gauge group $G$." This is the appropriate level of confidence for a single calibration with substantial input uncertainty.

**Recommended fix.** Replace the "$C \approx 2.08$" headline with a range. Add a brief sensitivity analysis. Either propose a parameter-free $C(G)$ prediction (preferred) or acknowledge that the present calibration is consistent with O(1) but not a precise prediction.

### M2. The "Casimir argument" is unfalsifiable as written

§4 says the calibration $C \approx 2$ is "not fine-tuned" and is "consistent with the Casimir factor $C_2(\mathrm{adj}) = N_c = 3$ for SU(3) (factor of $N_c / (\sqrt{N_c} \cdot \mathrm{normalization})$ depending on convention)." The convention dependence makes this an unfalsifiable claim: with normalization unspecified, any $O(1)$ value of $C$ is "consistent."

A mathematical statement on which the framework would stand or fall: from the BB-bridge mechanism, identify a specific function $C(C_2(\mathrm{adj}))$ — perhaps $C \propto C_2$, or $C \propto \sqrt{C_2}$, or $C \propto C_2 / \mathrm{rank}$, etc. — and predict that ratio for two gauge groups (SU(2) vs SU(3) is the cleanest pair). If the predicted ratio matches lattice data within the uncertainty, the framework is supported. If not, falsified.

As currently written, no such specific Casimir formula is given. The framework cannot be tested.

**Recommended fix.** Either (a) commit to a specific Casimir formula and test it against lattice glueball ratios across SU(N) for $N = 2, 3, 4, 5$ (lattice data exists); or (b) acknowledge that the gauge-group dependence is an open question, and downgrade the "$C \approx 2$ consistent with Casimir = 3" remark to a heuristic observation.

### M3. Conjecture 3.2 is a physics-interpretive statement, not a mathematical conjecture

Conjecture 3.2 reads: "The YM mass gap $\Delta_{\rm YM}$ is the energy cost of creating a color-singlet excitation from the vacuum, and arises from the same mechanism as the BB-lifted-theory mass gap: separability forces a spectral floor."

This is a verbal claim about *mechanism*, not a mathematical conjecture about objects. To be a JMP-grade conjecture, it should be of the form:

> Conjecture 3.2'. Let $G$ be a compact simple gauge group. Let $\mathcal{T}_{\rm YM}(G)$ be the (conjectural) Wightman QFT of pure $G$ Yang-Mills in $\mathbb{R}^{1+3}$. Let $H$ be the Hamiltonian. Let $\Omega$ be the unique (conjectural) vacuum vector. Then $\inf \{\mathrm{spec}(H) \setminus \{0\}\} = \Delta_{\rm YM}(G) > 0$, and there exists a (conjectural) confinement-induced map $\mathcal{T}_{\rm YM}(G) \to \mathcal{T}_{\rm IR}(G)$ to an effective infrared theory in the BB class such that $\Delta_{\rm YM}(G) = m_\Xi(\mathcal{T}_{\rm IR}(G))$.

This is the actual mathematical structure that Conjecture 3.2 is hinting at. The manuscript should either commit to a precise formulation along these lines, or explicitly downgrade the "Conjecture" to a "Heuristic" or "Conceptual claim."

**Recommended fix.** Either reformulate Conjecture 3.2 as a precise mathematical statement (Conjecture 3.2' above is one option, modulo the Wightman-axioms-for-YM bottleneck), or relabel as a heuristic.

### M4. Prerequisites 5.1, 5.2, 5.3 are framed without indicating their difficulty

§5 lists three prerequisites for a rigorous proof of the YM mass gap via the BB bridge:

- **5.1 Wightman in 4D for the log theory.** This is a 50-year-old open problem in constructive QFT. The Glimm-Jaffe program established $\Phi^4_2$ and $\Phi^4_3$, made partial progress on $\exp(\Phi)_2$ and $(\sin \Phi)_2$, and stalled at 4D for any non-trivial scalar theory other than $\Phi^4_4$ (which is conjecturally trivial). The manuscript states 5.1 as if it were a tractable open problem; it is not.

- **5.2 Effective IR separability of YM.** Cluster decomposition in confined gauge theory is a standard result in heuristic confinement physics, but a *rigorous* statement compatible with the BB framework is an open problem at the level of fundamental constructive QFT and would require (5.1) as a prerequisite.

- **5.3 Gauge-fixing-compatible BB.** This is also non-trivial: BB's theorem is for unconstrained wave functions, while gauge theory has a constrained Hilbert space modulo gauge transformations. A gauge-invariant BB-style uniqueness result on the moduli space of connections is unknown.

The manuscript's "5.1 + 5.2 + 5.3 = proof of YM mass gap" framing makes this look like a tractable program, but the actual difficulty is "5.1 alone has been open since 1980." This should be made explicit.

**Recommended fix.** Add a §5.4 "On the difficulty of the prerequisites" that explicitly notes that Prerequisite 5.1 is the central open problem of constructive QFT in 4D, that 5.2 has had partial rigorous results since the 1980s but remains incomplete, and that 5.3 is a new mathematical question not explicitly studied in the literature. The reader should leave §5 with a calibrated estimate of the program's difficulty.

### M5. The "confinement = effective infrared separability" intuition needs a citation

§3.2 invokes the standard physics intuition that confinement realizes effective IR separability: hadrons / glueballs decouple in the long-distance theory. This is a real physics statement, well-known in the QCD pedagogical literature (Ellis-Stirling-Webber; Peskin-Schroeder; Weinberg vol 2), but the manuscript provides no specific citation. The cited references [Strocchi 2013] and [GlimmJaffe 1987] are standard but do not address the specific "BB-compatible separability" statement made.

**Recommended fix.** Cite a specific cluster-decomposition theorem in the confined phase. The Streater-Wightman 1964 framework, the Haag-Kastler 1964 algebraic framework, or Strocchi's *Symmetry Breaking* textbook §6–7 would be appropriate. A reader should be able to look up "what is being assumed" in §3.2.

### M6. The relationship to J40 is heavy enough that J41 cannot stand alone

The manuscript depends on J40 for: (i) the BB-bridge framework, (ii) the regularity of the BB-lifted theory, (iii) the verification script, (iv) the discrete-side discussion. J41 contributes: (i) Proposition 2.1 (a two-line calculation), (ii) Conjecture 3.2 (a verbal claim), (iii) the calibration $C \approx 2.08$ (a one-line arithmetic).

For JMP submission, J41 should either be expanded to stand on its own, or merged into J40. The "companion" framing assumes the reader has J40 in hand, but a JMP referee will expect J41 to be a complete contribution.

**Recommended fix.** Either expand J41 with substantial original technical content (suggested in M1–M3 above), or merge with J40 and submit as a single longer paper.

---

## 4. Minor comments

### m1. Title is wordy
"The Yang-Mills Mass Gap Bridge: Substrate-Algebra Predictions from Separability-Forced Spectral Floor." Consider tightening to "Yang-Mills Mass Gap and the BB-Bridge: A Separability-Forced Spectral Floor" or "BB-Bridge Predictions for the Yang-Mills Mass Gap." The current title has three concept-laden phrases ("substrate-algebra predictions," "separability-forced," "spectral floor") that overlap.

### m2. Abstract length and detail
The abstract is substantive (1 paragraph, 14 lines) and is appropriate. But the final sentence "**The paper does not claim to prove the YM mass gap**" is bold-faced in the abstract. Tone the bold; the §6 status table already makes the point clearly.

### m3. "Glueball $m_G \approx 1.7$ GeV"
Use the actual lattice value from Morningstar-Peardon 1999 (the cited source): $m_{0^{++}} \approx 1.71 \pm 0.05$ GeV at $a^{-1} \approx 2$ GeV. The $\pm 0.05$ matters for the calibration sensitivity (M1).

### m4. Footnote "depending on convention"
The "(factor of $N_c / (\sqrt{N_c} \cdot \mathrm{normalization})$ depending on convention)" parenthetical in §4 is doing too much work. Either commit to a specific convention or remove the parenthetical (and reframe as "C is consistent with O(1) Casimir factors but the precise convention is unspecified").

### m5. Proposition 3.1 should be Heuristic 3.1
The label "Proposition" in mathematics implies a proved statement. "Confinement = effective infrared separability" is a heuristic / standard physics intuition, not a proved proposition. Relabel.

### m6. "$\Box \Xi = \kappa(1 + \log \Xi)$" notation conflict
The companion J40 manuscript writes the equation with $\kappa$ as the coupling. In J41, both $\kappa$ and $\kappa_{\rm eff}$ appear (the latter in §2.3 of WP92, line 73). Consolidate notation.

### m7. References to companion submissions
[J01], [J03], [J05], [J40] are cited as "Submitted to" specific journals (JCT-A, JCAP, JCT-A, JMP). For the published version, these should be updated with status (under review / revised / accepted).

### m8. The "no dedicated verification script required" claim is awkward
The §2 of the README defends the absence of a J41-specific script by citing J40's `proof_separability_bridge.py`. But J40's script does not test the J41-specific claim "$C \approx 2.08$." A simple `verify_J14_glueball.py` (one-line $C = m_G / (\Lambda \cdot e)$) would close this gap and is suggested by the README itself. Add it.

### m9. Suggested reviewers
The cover letter (not seen by this referee, but mentioned in the README) suggests Witten, Jaffe, and others. These are appropriate for the YM connection but may not be deeply engaged with the BB-bridge framework. Consider adding (in order of relevance) Bialynicki-Birula (if available), Glimm or one of his living students, Strocchi (cluster decomposition), and a working lattice glueball expert (Morningstar or Peardon themselves).

### m10. The Casimir-of-adjoint formula
"$C_2(\mathrm{adj}) = N_c = 3$ for SU(3)." More precisely, $C_2(\mathrm{adj}) = N_c$ in the standard convention where the fundamental has $C_2(\mathrm{fund}) = (N_c^2 - 1)/(2 N_c)$. Whether this convention is the relevant one depends on the BB-bridge derivation, which the manuscript does not provide. The convention should be made explicit.

---

## 5. Specific verifications performed

(V1) **Calibration $C = m_G / (\Lambda_{\rm QCD} \cdot e)$.** Independent computation:

| $\Lambda_{\rm QCD}$ (GeV) | $m_G$ (GeV) | $C$ |
|---|---|---|
| 0.30 | 1.50 | 1.84 |
| 0.30 | 1.70 | 2.08 |
| 0.30 | 1.85 | 2.27 |
| 0.25 | 1.70 | 2.50 |
| 0.35 | 1.70 | 1.79 |
| 0.40 | 1.70 | 1.56 |

The "$C \approx 2.08$" headline corresponds to one cell of this table; the manuscript should report the range. ✓ (calculation correct; range understated)

(V2) **Proposition 2.1 ($V''(\Xi_0) = \kappa e$).** $V(\Xi) = \kappa \Xi \log \Xi$, $V'(\Xi) = \kappa(1 + \log \Xi)$, $V''(\Xi) = \kappa / \Xi$. At $\Xi_0 = e^{-1}$: $V''(\Xi_0) = \kappa e$. ✓

(V3) **Lattice 0$^{++}$ glueball value.** Morningstar-Peardon (PRD 60:034509, 1999) reports the SU(3) 0$^{++}$ glueball at $1.730(50)(80)$ GeV. ✓ (manuscript value $1.7$ GeV is appropriate; uncertainty is omitted from the calibration)

(V4) **Bialynicki-Birula 1976 statement.** As verified in the J40 referee report, BB's uniqueness theorem holds for non-relativistic Schrödinger evolution; its extension to wave / Klein-Gordon settings requires care. Inherits the same scope concerns as J40.

(V5) **Wightman axioms for $\log \Xi$ theory in 4D.** This is unsolved. No claim is made by the manuscript that it is solved; the manuscript correctly lists this as Prerequisite 5.1. ✓ (correctly flagged; difficulty understated — see M4.)

(V6) **Cluster decomposition in confined YM.** A theorem in the heuristic-physics literature; rigorous results exist for specific limits (Wilson 1974 lattice strong coupling, Seiler 1982, Fröhlich-Spencer 1982). The manuscript's reliance on "confinement = effective separability" is consistent with the standard physics intuition but is not a theorem in the BB-compatible sense. ✓ (consistent with literature; rigorous status correctly flagged; specific citation missing — see M5.)

(V7) **No dedicated verification script for J41.** The companion J40 script verifies elementary numerical facts about the BB potential; it does not verify the J41-specific claim "$C \approx 2.08$." The latter is a one-line arithmetic, computable independently. ✓ (consistent with manuscript claim; a J41 mini-script would be a small improvement.)

---

## 6. Questions to the authors

Q1. **What is the predicted gauge-group dependence of $C$?** I.e., is $C(\mathrm{SU}(2)) = C(\mathrm{SU}(3))$ as a function of the BB-bridge mechanism, or does it differ by a Casimir factor? Lattice data for SU(2)$_{0^{++}}$ and SU(3)$_{0^{++}}$ glueballs is available [Lucini-Teper-Wenger 2004]. The ratio is a parameter-free test of the framework.

Q2. **What "convention" in the parenthetical "$N_c / (\sqrt{N_c} \cdot \mathrm{normalization})$" is intended?** Without specification, the Casimir comparison is unfalsifiable.

Q3. **What does Conjecture 3.2 say about non-confining gauge theories?** $\mathcal{N} = 4$ super-YM and the Banks-Zaks fixed-point theory have YM-like Lagrangians but no mass gap. Does the BB-bridge framework predict that these theories are *not* in the BB class, or that they are in the BB class with $\Delta = 0$, or something else?

Q4. **What is the precise content of "effective infrared separability" (Proposition 3.1)?** Cluster decomposition is the standard candidate; is the manuscript's "effective separability" identical to cluster decomposition, or is it a stronger / weaker condition?

Q5. **Has any progress been made on Prerequisite 5.1 (Wightman in 4D for $\log \Xi$ theory) since the 1971/1980 era?** I am unaware of any, but a reference to recent literature (if any) would be useful.

Q6. **Is the BB theorem itself (Theorem 2.1 of J40, restated in J41) compatible with the gauge-constrained Hilbert space of YM?** The BB theorem is for unconstrained wave functions; YM has Gauss's-law-constrained states. Prerequisite 5.3 acknowledges this, but the magnitude of the issue is not discussed. Do the authors expect 5.3 to require a substantial new uniqueness theorem on the moduli space of connections?

---

## 7. Originality and significance for JMP

The application of J40's BB-bridge framework to YM is a natural follow-up. The Proposition 2.1 calculation is correct but elementary (two lines). Conjecture 3.2 is a verbal restatement of "BB mechanism applies to YM," which is the implicit suggestion of J40 made explicit.

**Originality.** The "BB bridge applied to YM mass gap" framing is, to the referee's knowledge, novel — though it is largely a restatement of J40's framework with one change of subject (NS → YM). The substantive new content is the calibration $C \approx 2.08$, which is one number sensitive to inputs.

**Significance for JMP.** As a *companion* to J40, this paper has interest. As a *standalone* JMP submission, it is too thin: 3 pages of mathematical content, mostly interpretive, with one elementary calculation and one verbal conjecture. JMP papers typically span 15–30 pages with substantial technical development; this manuscript is in the 5-page range.

**Comparison to existing YM mass-gap literature.** The Witten 1988 chiral-lagrangian sketch, the Faddeev-Niemi 1999 monopole / instanton lines, the Greensite 2003 dual-superconductor / center-vortex frameworks, and the more recent 't Hooft 2018 anomaly-driven approaches all propose different mechanistic readings of the YM mass gap. The BB-bridge reading is novel — it does not appear in this literature — and would be a contribution if developed to comparable depth. Currently it is much thinner.

The manuscript's "honesty" — the §6 status table, the explicit Tier 4 framework classification, the listing of three Prerequisites — is appropriate. The reader is not misled; the issue is not over-claiming, the issue is under-developing.

---

## 8. Reproducibility

The numerical claim "$C = m_G / (\Lambda_{\rm QCD} \cdot e) \approx 2.08$" is reproducible by hand calculation in 30 seconds. ✓

The manuscript correctly defers structural claims to J40's verification script. The companion script `proof_separability_bridge.py` does include a Section 3 ("YM — Mass Gap from Log Potential") that tests $m^2 = \kappa \cdot e \approx 2.71828$, the calibration $C \approx 2.08$, and the consistency $0.5 < C < 5.0$. This is a slim verification but covers the J41-specific arithmetic. ✓

Suggested addition: a `verify_J14_glueball.py` standalone script (~ 10 lines) that prints the calibration sensitivity table from V1 above. This would close the README's "TBD" gap and provide a J41-specific verification.

The lattice glueball value $m_G$ is from the cited Morningstar-Peardon 1999; the $\Lambda_{\rm QCD}$ value is a standard input; both are independently verifiable from the published literature.

---

Sincerely,
External Referee, JMP
