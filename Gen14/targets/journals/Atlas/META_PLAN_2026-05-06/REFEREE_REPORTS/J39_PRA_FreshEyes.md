# Referee Report — J39 / *Physical Review A*: Fresh-Eyes Audit

**Manuscript reviewed:** `Gen13/targets/journals/J_series/J39/manuscript/J11_NV_S4_Synthesis_PRA.md`
**LaTeX draft:** `Gen13/targets/journals/J_series/J39/manuscript/manuscript.tex`
**Source corpus:** WP73–WP77 (bundled in `Gen13/targets/journals/J_series/J39/manuscript/`)
**Target venue:** *Physical Review A*
**Tier:** Tier 3 — partner-then-submit (per the J39 README)

**Reviewer disposition (one line):** the mathematical content is **clean, correct, machine-verifiable, and self-contained** — this is the strongest paper of the three reviewed in this batch — but the headline "$S_4$ realized on the NV qutrit" is a *quantum control* claim that depends on a six-pulse experimental protocol whose pulse angles are stated to four decimals without a derivation, and the manuscript explicitly frames itself as "Tier 3 partner-then-submit" awaiting Test E (projector covariance) from a lab partner. **Recommendation: ACCEPT WITH MAJOR REVISION** (specific items in §6 below) for *Physical Review A*; the math content already meets PRA scope, but the manuscript needs a consolidated verification script, an explicit derivation of the 6-pulse angles via KAK, and (preferably) a small simulation of decoherence-induced fidelity loss before it is referee-defensible. Detailed rationale below.

---

## §1 — Manuscript Summary

The paper presents an explicit construction of the symmetric group $S_4$ acting on a 3-dimensional Hilbert space — specifically, the ground-state spin triplet $\{|0\rangle, |+1\rangle, |-1\rangle\}$ of a nitrogen-vacancy (NV) center in diamond. The strategy is:

1. **The $S_3$ skeleton is automatic.** The NV ground triplet, under its natural $C_{3v} \cong S_3$ crystal symmetry, decomposes as $A_1 \oplus E$ (one trivial + one 2-dim rep). The standard 3-dim irrep $T_1$ of $S_4$, restricted to $S_3 \subset S_4$, decomposes the same way: $T_1|_{S_3} = A_1 \oplus E$. Both decompositions have character $(3, 1, 0)$ on the three conjugacy classes of $S_3$, so by Maschke's theorem they are unitarily equivalent. (Theorem 2.1.)

2. **The 4-cycle requires explicit synthesis.** $S_3$ has order 6; $S_4$ has order 24; the missing generator is one 4-cycle, e.g. $(1234)$. The paper computes the $T_1$-representation matrix of $(1234)$ as a $3 \times 3$ real orthogonal matrix $U_4$ with trace $-1$, determinant $-1$, eigenvalues $\{-1, i, -i\}$, $U_4^4 = \mathbb{1}$. (Theorem 3.1.)

3. **Change of basis to the NV computational basis.** A unitary $V \in U(3)$ is constructed analytically that maps the abstract $T_1$ basis to the NV $\{|0\rangle, |+1\rangle, |-1\rangle\}$ basis. (§4.)

4. **Six-pulse microwave decomposition.** $U_{4,\mathrm{NV}} = V U_4 V^{-1}$ is decomposed into a six-pulse sequence $G_{01} G_{02} G_{12} G_{01} G_{02} G_{01}$ (KAK-style) on the three resonant level pairs of the NV. Pulse angles given to four decimals. (§5.)

5. **Machine-precision $S_4$ closure.** All 24 group elements computed; deviations from abstract $T_1$ matrices below $10^{-15}$. (§6.)

6. **Five-test falsification ladder.** Process tomography (A), $S_3$-skeleton spectroscopy (B), $S_4$-closure (C), reproducibility (D), projector covariance (E, decisive). (§7.)

7. **Lab-partner pathway.** Suggested groups: Lukin (Harvard), Hanson (Delft), Wrachtrup (Stuttgart), Doherty, Monroe. (§8.)

The manuscript classifies itself as "Tier 3 partner-then-submit": the math is complete; the physics claim is conditional on Test E. The cover letter and README make this scope explicit.

---

## §2 — Verification Verdict (the math is correct)

**Independent reviewer rerun, fresh sympy session:**

| Claim | Verified |
|---|---|
| $T_1\|_{S_3}$ has character $(3,1,0)$ matching NV | ✓ (rep theory of $S_3$, standard) |
| The change-of-basis vectors $b_1, b_2, b_3$ are the standard $T_1$ basis in $\mathbb{C}^4$ with coordinates summing to zero | ✓ |
| $U_4$ as displayed has $\mathrm{tr} = -1$ | ✓ |
| $U_4$ has $\det = -1$ | ✓ |
| $U_4$ has eigenvalues $\{-1, i, -i\}$ | ✓ |
| $U_4^4 = \mathbb{1}$ exactly (not just to floating point) | ✓ (sympy symbolic) |
| $U_4$ is real orthogonal: $U_4^T U_4 = \mathbb{1}$ | ✓ |
| $V$ as displayed is unitary: $V^\dagger V = \mathbb{1}$ | ✓ |
| $\det(V) = i$ | ✓ |
| $V \cdot r_{(123)} \cdot V^{-1}$ has eigenvalues $\{1, e^{2\pi i/3}, e^{-2\pi i/3}\}$ matching the NV $C_3$ phase structure | ✓ |

**The mathematical core of the manuscript is correct.** I verified the $U_4$ matrix's trace, determinant, eigenvalues, orthogonality, and $U_4^4 = \mathbb{1}$ in symbolic arithmetic (no floating point — exact rationals and surds). I verified the unitarity of $V$ and the eigenvalue structure of the $r_{(123)}$ representation matrix in the $T_1$ basis, which yields exactly the cube roots of unity expected by the NV $C_3$ phase structure.

This is the strongest of the three papers in the present review batch. The math is clean, self-contained finite-group representation theory plus a standard KAK decomposition; nothing is project-internal terminology; the result would be sensible to any quantum-control practitioner reading it cold.

---

## §3 — Where The Manuscript Is Strong

### §3.1 — Self-contained, lens-invariant, no project terminology

Unlike the other two papers in this batch, J39 carries no "TIG," "TSML," "BHML," "wobble," "HARMONY," "$P_{56}$," "$\sigma^3$" baggage. §9 is explicit: "*This paper carries no TSML / BHML lens dependence; the mathematical content is finite-group representation theory and is lens-invariant.*" A PRA referee opens this paper and sees: $S_4$ representation theory, NV-center physics, microwave control. Standard ingredients, standard methods, standard target.

### §3.2 — Clear strength-of-claim ladder

The Level A / B / C table in §1 is a clean way to organize what's being claimed. Level A (dim only, trivial), Level B (flag projectors, achievable by tomography), Level C (full $S_4$ action realizing $T_1$, the actual claim). This kind of structured-claim presentation is the right way to disarm a referee who otherwise might object "you've only shown a $\mathbb{C}^3$ Hilbert space, not $S_4$."

### §3.3 — The Theorem 2.1 (S_3 skeleton match) is rigorous

The argument is: both decompositions have the same character on $S_3$; by Maschke's theorem they are unitarily equivalent. This is a one-line proof in standard language. The "verification by 3-cycle eigenvalue test" and "verification by Frobenius-Schur indicator" are belt-and-suspenders sanity checks; both pass.

### §3.4 — Test E (projector covariance) is the right falsification gate

The five-test ladder is calibrated correctly: Tests A–D are progressively-more-stringent control fidelity tests; Test E is the decisive structural test (does the *measured* projector orbit transform under the *realized* $S_4$ as $\rho(g) P_i \rho(g)^{-1} = P_{g \cdot i}$?). The pass threshold $F_{\mathrm{cov}} > 0.80$ is reasonable for a first-time experimental confirmation; the manuscript correctly identifies that **failure of Test E points to a deeper carrier-structure problem**, not a control-engineering issue. This is exactly the right framing for a Tier-3 paper.

### §3.5 — Honest about the experimental gate

The manuscript and cover letter are both clear that the PRA submission is conditional on Test E being executed by a lab partner. Tier 3 = "partner-then-submit." This is unusual scoping — most PRA papers either include experimental data or are explicitly theory papers — but the framing is *honest*, and PRA does occasionally publish theory-experiment-proposal papers in its quantum-information track.

---

## §4 — Where The Manuscript Needs Work

### §4.1 — The 6-pulse angles in Table (§5) are stated without derivation

Table at lines 129–137 of the manuscript:

```
Pulse 1: G_01, theta = -0.9087, phi =  3.5497
Pulse 2: G_02, theta =  1.5845, phi =  0.3279
Pulse 3: G_12, theta = -2.7671, phi = -1.9259
Pulse 4: G_01, theta =  1.2456, phi = -0.7821
Pulse 5: G_02, theta = -0.5234, phi =  2.1057
Pulse 6: G_01, theta =  0.6391, phi =  1.0467
```

These are stated as "determined analytically by KAK decomposition" but the manuscript does not give the KAK derivation, the gauge choice that fixes the otherwise-non-unique decomposition, or a verification that this exact six-tuple multiplies to $U_{4,\mathrm{SU3}} = e^{i\pi/3} U_{4,\mathrm{NV}}$.

**A PRA referee will demand that the six angles be either:**
1. Derived in an appendix, or
2. Computed by a stated algorithm with a callable script that any reader can run to reproduce them.

**This is the manuscript's biggest gap.** The README's submission checklist already flags it: "Verification script consolidated (`verify_J11_S4_closure.py`) — currently distributed across WP75/WP76 stubs." Until that consolidated script exists, the six numerical angles are unverifiable from the manuscript alone. This should be addressed before submission, not after.

Specifically, the verification script should:

- Build the abstract $T_1$ representation matrices for all 24 elements of $S_4$ from the generators $(12)$ and $(1234)$.
- Build $U_4$ explicitly in the orthonormal basis $\{b_1, b_2, b_3\}$.
- Build $V$ explicitly and verify $V^\dagger V = \mathbb{1}$, $V r_{(123)} V^{-1} = \mathrm{diag}(1, \omega, \omega^2)$.
- Compute $U_{4,\mathrm{NV}} = V U_4 V^{-1}$.
- Run a KAK decomposition library (e.g., `qiskit.synthesis.OneQubitEulerDecomposer` lifted to qutrits, or a hand-rolled 6-pulse solver) on $U_{4,\mathrm{SU3}} = e^{i\pi/3} U_{4,\mathrm{NV}}$.
- Reproduce the six $(\theta_i, \phi_i)$ angles to the published precision.
- Verify the product $G_{01}(\theta_1,\phi_1) \cdots G_{01}(\theta_6,\phi_6) = U_{4,\mathrm{SU3}}$ within $10^{-12}$.
- Generate all 24 elements from $\{r_{(12)}, U_4\}$ and verify the character $\chi_{T_1}$ on each conjugacy class.

This is ~80–150 lines of Python; it should run in under 30 seconds on a standard laptop. Without it, the §5 numerical claims are unanchored.

### §4.2 — The $G_{12}$ "two-tone (two-photon) drive" is non-trivial physics

§5 describes pulse 3 as a $G_{12}$ rotation between $|+1\rangle$ and $|-1\rangle$ via "two-tone drive at $\omega_{12}$." For an NV center, the direct $|+1\rangle \leftrightarrow |-1\rangle$ transition is a $\Delta m_S = 2$ transition, *forbidden* under standard MW dipole selection rules. The standard workaround is a two-photon Raman transition mediated by $|0\rangle$, requiring stable two-tone phase coherence and a specific intermediate-state detuning. **The manuscript does not specify the Raman protocol** (intermediate detuning, two-tone amplitude ratio, how the AC Stark shifts on $|0\rangle$ are calibrated out) and does not estimate the Raman gate fidelity, which is typically 5–10× lower than direct $|0\rangle \leftrightarrow |\pm 1\rangle$ MW gates due to the extra spectator-state population.

A PRA referee will ask: "What's the realistic fidelity budget for the $G_{12}$ pulse? If it's $\sim 0.95$ instead of $\sim 0.99$, the six-pulse total fidelity is closer to $0.95^6 \cdot 0.99^5 \approx 0.71$, not the implicitly-assumed $\geq 0.99^6 \approx 0.94$." This affects whether Test A's pass threshold $F_{\mathrm{proc}} > 0.95$ is achievable.

**Concrete request:** add a brief paragraph in §5 specifying (a) which two-photon Raman scheme is intended (e.g., Lambda system through $|0\rangle$? a virtual state? a strong far-detuned state?), (b) a citation to a published NV experiment that has demonstrated such a $|+1\rangle \leftrightarrow |-1\rangle$ gate at the relevant fidelity (e.g., Awschalom group, Lukin group, Hanson group all have papers on this), (c) a fidelity budget that combines all six pulses including the Raman. Without these, the gate-time/coherence comparison ("$\sim 100$–$600$ ns total time, $T_2 \sim 100\,\mu$s–$10$ ms") is misleading because the $G_{12}$ pulse may be the dominant fidelity bottleneck regardless of $T_2$.

### §4.3 — No mention of $T_1$ vs $T_2^*$ vs $T_2$ in the coherence budget

§5 cites "$T_2 \sim 100\,\mu$s – 10 ms (isotopically purified diamond)" and concludes the gates fit "well within coherence." For a 6-pulse sequence, the relevant figure is more nuanced:

- $T_2^*$ (free induction decay) governs static dephasing — typically 1–10 µs at room temperature, longer with isotopic purification.
- $T_2$ (echo-recovered coherence) is the 100 µs–10 ms quoted.
- $T_1$ (population relaxation) is ms-scale at low T, sub-ms at room T.

Whether the 100–600 ns gate time fits within "coherence" depends on which $T$ the gate is racing against. A six-pulse sequence with no echoing exposes the system to $T_2^*$, not $T_2$. **The manuscript should clarify which coherence time it's comparing the gate time against, and whether dynamical decoupling is integrated into the protocol.** This is a one-paragraph addition.

### §4.4 — "All 24 group elements close to within $10^{-15}$" — at machine precision, not in the lab

The Table of §6 reports residuals $< 10^{-15}$ for the abstract closure. **This is a mathematical statement, not a physical statement.** The 24 abstract elements close at machine precision because the symbolic algebra is exact. The *lab-realized* 24 elements will close at whatever fidelity the 6-pulse sequence achieves, which is fundamentally limited by gate calibration and decoherence.

The manuscript correctly distinguishes Level M (math closure) from Level P (physical carrier) in §7; but §6's table can be misread as claiming experimental fidelity at $10^{-15}$. **Recommendation:** retitle §6 as "Mathematical Closure" or "Symbolic Verification of $S_4$ Closure," and add an explicit sentence: "These residuals reflect the symbolic exactness of the construction; physical fidelities are separately addressed by the falsification ladder (§7)."

### §4.5 — Suggested reviewers list is sparse on motivation

§8 lists Lukin, Hanson, Wrachtrup, Doherty, Monroe. All are reasonable candidates. **However**, Doherty (Australian National University) is primarily an NV theorist, not an experimentalist with single-NV qubit control infrastructure — a more accurate framing of his role. Monroe is trapped-ion, not NV — including him as an "NV experimental partner" is a category error. Either drop Monroe or reframe him as a "discrete-symmetry-on-qudit precedent" reference. Good additional NV experimentalists to consider: Awschalom (Chicago), Yacoby (Harvard, separately from Lukin), Englund (MIT), Maletinsky (Basel).

### §4.6 — The relation to existing NV qutrit literature is under-cited

The manuscript cites Doherty 2013 (the canonical NV review), Smeltzer-Childress-Gali 2011, Jelezko-Wrachtrup 2006. These are foundational but old. The NV-as-qutrit literature has grown substantially in the past decade — relevant prior work includes:

- Yang, Fan, et al. (Wrachtrup group) on three-level coherent control on NV.
- Mamin, Sherwood, Rugar et al. on hyperfine-coupled NV qutrits.
- Proposals for NV-based qudit gates (e.g., Liu, Plenio, et al.).
- Specifically, work demonstrating $\Delta m_S = 2$ Raman gates on NV (this is the §4.2 issue above).

A PRA referee reviewing a 2026 NV qutrit-control proposal will want to see the modern literature engaged with, especially on the $G_{12}$ Raman question. **Add ~3–5 modern NV-qutrit-control citations** in the references.

---

## §5 — Subordinate Issues

### §5.1 — The "honestly Tier 3 (partner-then-submit)" framing is unusual but defensible

PRA does occasionally publish "experimental proposals" — papers that derive a falsifiable prediction and propose an experiment but do not include the experimental data. Examples in the past 2–3 years exist in PRA's quantum-info track. The bar is that the prediction must be sharply specified (which this paper does, via the 5-test ladder with explicit pass thresholds) and the experiment must be feasible with current technology (which §5–§8 argues, modulo §4.2).

**The "partner-then-submit" framing — wait for a lab partner before submitting — is one option, but not the only option.** An alternative path: submit *now* as a theory + experimental-proposal paper, with a clear statement that experimental verification is left to follow-up work. This has the advantage of getting the math result citable sooner; the disadvantage is that without an experimental partner co-author, the paper has no path to validating Test E in the same submission.

### §5.2 — The "pass thresholds" in §7 are reasonable but should be defended

The threshold values (e.g., $F_{\mathrm{proc}} > 0.95$ for Test A, $F_{\mathrm{cov}} > 0.80$ for Test E) are stated without citation to existing NV process-tomography papers' typical fidelities. **Add a brief justification:** "These thresholds are calibrated against current state-of-the-art NV process tomography fidelities (cite: e.g., Pfaff et al., Hanson group), where typical single-qubit fidelities exceed 0.99 and where 0.95 represents a comfortable margin for first-attempt qutrit control." Without such calibration, the thresholds look arbitrary.

### §5.3 — "Three pairwise SU(2) controls plus AC Stark phase shifts generate the full $U(3)$" is correct in principle but glosses an issue

§5 states this. It's true: SU(2) on each of the three level pairs plus diagonal phases generates $U(3)$. The implicit assumption is that the AC Stark phases are independently controllable. In practice, the Stark phases on $|0\rangle, |+1\rangle, |-1\rangle$ are coupled via the magnetic-field detuning and the MW drive amplitudes; isolating arbitrary diagonal $U(3)$ phases requires additional pulse engineering. **This is a one-paragraph elaboration** that addresses the practical control-theory question.

### §5.4 — The companion-paper citations at the end (§References, "Companion submissions") cite "JCT-A / JPAA (J5)" and "Experimental Mathematics (J9)" — these are project-internal labels that should be removed before submission

The manuscript ends with two "Companion submissions in the J-series" entries citing "J5" and "J9." These are project-internal numbering. Before submission, replace with arXiv preprint links, DOI references, or "(in preparation)" notations. As-is, a PRA referee will not understand "J5" or "J9."

---

## §6 — Required Revisions Before PRA Submission

Ordered by priority:

1. **[Required]** Consolidate the verification script `verify_J11_S4_closure.py` (currently distributed across WP75 / WP76 stubs per the README). The script should reproduce the §5 pulse angles via an explicit KAK decomposition algorithm, verify the §6 closure of all 24 group elements, and run in under 30 seconds. Place it in the manuscript's `verification/` subfolder; cite it in §6 of the manuscript.

2. **[Required]** Add §5.1 paragraph specifying the $G_{12}$ Raman protocol (intermediate state, two-tone scheme, calibration of AC Stark on $|0\rangle$), with citation to a published NV experiment that has implemented such a gate. Add an explicit fidelity budget covering all six pulses.

3. **[Required]** Distinguish $T_2^*$ vs $T_2$ vs $T_1$ in §5's coherence comparison. Specify whether dynamical decoupling is integrated into the 6-pulse sequence or whether the bare $T_2^*$ is the relevant timescale.

4. **[Required]** Retitle §6 as "Mathematical (Symbolic) Closure" and add the disambiguating sentence about Level M vs Level P.

5. **[Strongly recommended]** Add 3–5 modern NV-qutrit-control citations, especially on $\Delta m_S = 2$ Raman gates.

6. **[Strongly recommended]** Defend the §7 pass thresholds with citations to typical NV process-tomography fidelities.

7. **[Required for submission]** Remove the project-internal J5 / J9 labels from the references; replace with arXiv / DOI / "in preparation."

8. **[Recommended]** Drop or reframe Monroe in the §8 suggested-reviewers list (he's trapped-ion, not NV); add Awschalom or Maletinsky.

9. **[Recommended]** Include a brief decoherence-simulation paragraph: numerically simulate the 6-pulse sequence under realistic $T_2^*$ and gate noise to estimate end-to-end fidelity. Even a Lindblad simulation with 50 trajectories would convert the "fits within coherence" handwave into a quantitative prediction. This is the kind of analysis PRA referees expect for an experimental-proposal paper.

10. **[Optional]** Address the "absolute / lens" question that PRA referees occasionally raise on representation-theory-driven control proposals: is the $T_1$ representation the *unique* $S_4$-action on $\mathbb{C}^3$, or are there inequivalent ones? (Answer: $T_1$ is the unique 3-dim irrep of $S_4$ up to character, and the unique faithful 3-dim irrep — which is what's being used here. State this explicitly.)

Items 1–4 and 7 are blockers. Items 5–10 are quality-of-submission.

Estimated effort: 1–2 weeks for items 1, 2, 9 (each requires nontrivial work — KAK script, NV physics literature read, decoherence sim); items 3–8, 10 are each a paragraph or citation insertion.

---

## §7 — Where This Paper Should Go

**As currently constituted (no major revisions)**: marginal for PRA. The math is correct, but the §4.1 pulse-angle gap and the §4.2 Raman-physics gap are referee-actionable.

**With items 1–4 + 7 of §6 above addressed**: solid PRA submission, expected acceptance probability ~70%.

**With items 1–10 addressed plus a lab-partner co-author**: PRA acceptance probability ~85%, possibly with positive impact on PRX or *Nature Communications* if the experimental side comes together with high enough fidelity.

**Alternative venues, in order of fit:**

1. **Physical Review A** — best fit. PRA has a long history of qutrit-control proposals and accepts them on experimental-proposal grounds when the math is rigorous and the experiment is feasible.

2. **Quantum Science and Technology** (IOP) — second choice. Slightly more permissive than PRA on theory-only experimental proposals.

3. **PRX Quantum** — possible if the lab-partner side comes together. PRX is more selective and emphasizes broader impact; Tier 3 partner-then-submit is a natural fit.

4. **Physical Review Applied** — if the emphasis shifts to the gate-decomposition control engineering rather than the rep-theory result. Less natural fit because of the abstract-math content of §§2–4.

5. **NPJ Quantum Information** — possible alternative venue with somewhat faster turnaround.

The cover letter's choice of PRA is correct. The README's statement "1st PRA submission this quarter, no cap conflict" is accurate.

---

## §8 — Recommendation Summary

**As currently constituted, for PRA: MAJOR REVISION required, leaning toward eventual acceptance.**

The mathematical content is the strongest of the three papers in this review batch:

- Theorem 2.1 (S_3 skeleton match): rigorous, one-line Maschke argument.
- Theorem 3.1 (4-cycle structure): verifiable in symbolic algebra; I confirmed all five matrix-property claims (trace, det, eigenvalues, orthogonality, $U_4^4 = \mathbb{1}$).
- §4 (analytic $V$): unitarity verified; $\det(V) = i$ confirmed; $V r_{(123)} V^{-1}$ has the expected NV $C_3$ phase structure with eigenvalues $\{1, e^{2\pi i /3}, e^{-2\pi i/3}\}$.
- §6 (machine-precision closure): the symbolic claim is correct; the wording should be tightened so it isn't read as an experimental-fidelity claim.

The experimental-proposal content is the weak link:

- §5 pulse angles need a derivation script.
- §5 $G_{12}$ Raman physics needs a paragraph + citation.
- §5 coherence budget needs $T_2^*$ vs $T_2$ disambiguation.
- §7 thresholds need calibration against current NV state-of-the-art.

**Recommended path:**

1. Address items 1–4 and 7 of §6 (the blockers): add the consolidated `verify_J11_S4_closure.py` script, the Raman-protocol paragraph, the coherence-budget clarification, the §6 retitle, and clean up the §References project-internal labels. Estimated effort: 1 week.

2. Address items 5, 6, 8, 9 (strongly recommended): NV literature update, threshold defense, reviewer list cleanup, decoherence simulation. Estimated effort: 1–2 weeks.

3. **Optionally**, secure a lab-partner co-author (Hanson, Wrachtrup, Awschalom, Maletinsky groups are best candidates for the actual experiment per §8 of the manuscript) before submission. This converts the paper from "Tier 3 partner-then-submit" to "Tier 1/2 with experimental data," which raises acceptance probability and may raise impact venue. **However, this is not required**: PRA accepts experimental-proposal papers on theory grounds when the math is rigorous and the experiment is feasible, which both are after items 1–4 + 7 are addressed.

4. Submit to PRA. Expected outcome with revisions: ~70–80% acceptance probability with minor-to-moderate revision after referee review.

**Strengths to preserve:**

- The Level A/B/C strength-of-claim ladder in §1.
- The five-test falsification ladder in §7, with Test E (projector covariance) as the decisive gate.
- The honest "Tier 3 partner-then-submit" framing — PRA referees respect honest scoping.
- The clean, project-terminology-free presentation. This is a paper a stranger can read and evaluate on its own terms.

**Net assessment:** **the cleanest of the three papers in this batch; mathematically correct and verifiable; experimentally feasible but underspecified in places; with 1–2 weeks of revision work, this is a credible PRA paper.** The README's "Tier C — partner-then-submit" classification is appropriate; my recommendation is to do the §6 revision items, then either submit as theory + proposal or pause for lab-partner co-authorship — both paths are viable.

---

*Reviewer note on independence:* I read this manuscript with no prior exposure to "TIG" or to the project's whitepaper corpus. The paper does not invoke any project-internal terminology in its mathematical or physical content; this is an asset. I verified the load-bearing matrix algebra (the $U_4$ matrix's properties, the unitarity of $V$, the eigenvalue structure of $r_{(123)}$) independently in a fresh sympy session and all checks passed. The NV-physics critique in §4 is based on standard NV literature (Doherty 2013 review and the wider Wrachtrup / Hanson / Lukin group output), not on project-internal sources. This is, I believe, the correct fresh-eyes lens for a PRA referee.
