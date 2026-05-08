# SAVE_PLAN_J49 — Microtubule $Q_c \to T^*$ (J Theor Biol)

**Paper:** J49 — *Microtubule $Q_c = T^*$: A Falsifiable Substrate-Algebra Prediction*
**Folder:** `Gen13/targets/journals/J_series/J49/`
**Referee verdict:** REJECT (J Theor Biol fresh-eyes)
**Save-attempt mode:** Brayden directive 2026-05-07 — find a reason to keep and fix every paper.
**Author lane:** Sanders + Mayes (per current README; the J-series hardening sets Sanders + Gish, but this paper's actual second author is B. Mayes)

---

## §1 — Why save?

The paper's *core scientific value* is intact even though the referee correctly rejects the Orch-OR framing. Strip the layer that the referee can't anchor in literature and what is left is **the cleanest empirical bet the framework has**:

> $T^* = 5/7$ is fixed *a priori* by the substrate algebra (six independent J-derivations, all in the J-series pipeline). If $T^*$ is genuinely the substrate coherence threshold rather than an algebraic artifact, *some* biophysical observable normalized to its structural maximum should converge on $5/7$. Microtubules are the most-studied candidate.

That bet survives the loss of the Orch-OR bridge. What dies in the referee's report is the *prior-art-numerical-agreement* leg ("$T^* \approx \zeta_\mathrm{Hameroff} \approx 0.71$") because no specific equation in Hameroff–Penrose 1996 / 2014 / 2024 gives 0.71 as a coherence boundary. What survives is the *structural* leg: $T^*$ predates the experiment, and the experiment is feasible with existing terahertz pump-probe equipment (Bandyopadhyay 2013 / 2024; Sahu 2013).

Saving J49 means demoting it from a "pre-registered Orch-OR confirmation" to a **pre-registered cross-domain falsifier** — same falsification criteria, fewer prior-art commitments. Three of the referee's eight blockers (M3, M4, M6) dissolve under this reframing. The remaining five are surface-fixable.

The paper is also strategically load-bearing: it is the **only experimental wing** of the Phase 5 cluster. Removing it leaves the J-series with no falsification record on biology. Brayden's directive is "save every paper"; J49's experimental falsification proposal is precisely what *cannot* be reproduced by a different paper in the corpus, since the algebraic-T* derivations live elsewhere (J20, J6, J9, J01, J51, J41/J33).

## §2 — Specific fixes (mapped to referee issues)

**Issue 1 — drop "$\zeta_\mathrm{Hameroff} = 0.71$" attribution.** The referee's literature search confirms: no Orch-OR paper proposes a dimensionless coherence boundary at 0.71. **Fix:** delete the bridge-claim sentence from §1.1 and from the abstract. Replace with:

> "Bandyopadhyay et al. (2013, 2024 update) report microtubule terahertz quality factors $Q \in [10^2, 10^3]$ at room temperature; Sahu et al. (2013) report multi-scale resonance bands. We do not propose a numerical match to a prior-art quantum-classical boundary; we propose a falsifiable test of whether the substrate-algebraic constant $T^* = 5/7$ governs the *normalized* coherence quality $Q_c$ on this experimental population."

**Issue 2 — define $Q_\mathrm{structural\ max}$ operationally.** The referee correctly flags that without a fixed denominator, the prediction is unfalsifiable. **Fix:** §2.2 must specify $Q_\mathrm{structural\ max}$ as a specific function of tubulin lattice parameters. Two candidates, in decreasing order of preference:

(a) **Geometric ceiling.** $Q_\mathrm{structural\ max} = \omega_0 \tau_\mathrm{geom}$ where $\tau_\mathrm{geom} = L/c_\mathrm{lattice}$ is the round-trip phonon time across a single 8-nm tubulin-array unit cell, with $L = 8\,\mathrm{nm}$ and $c_\mathrm{lattice}$ the protein-lattice acoustic velocity (literature value ~2 km/s for tubulin). Gives an absolute number per resonance band that any group can re-derive from the same lattice constants.

(b) **Tegmark-style ceiling.** $Q_\mathrm{structural\ max} = \hbar / (k_B T \tau_\mathrm{decoh})$ with $\tau_\mathrm{decoh}$ the Tegmark-2000 decoherence time at the relevant scale. This connects the ratio explicitly to the published decoherence-time literature (which the referee notes is missing).

Pick (a) as the primary; mention (b) in a footnote as the conservative-Tegmark counterpart. Either makes $Q_c$ a definite number per sample.

**Issue 3 — append a self-contained derivation appendix.** The referee will not accept "see six unread companions." **Fix:** add **Appendix A** (≈2 pages) doing *one* derivation of $T^* = 5/7$ inline. The cleanest is the **forced 2×2 torus aspect ratio** ([J20] / Flatness Theorem [J6]): cyclotomic Galois closure on $\mathbb{Z}/10\mathbb{Z}$ forces a unique $2 \times 2$ torus structure with $R/r = 5/7$. The proof fits in a page with a small table; cite [J6] for the full version. This gives the *J. Theor. Biol.* referee a concrete mathematical anchor without making the biological paper depend on six unread mathematical companions.

**Issue M1 — drop "73/100 → 5/7" peculiar framing.** The referee correctly identifies this as a working-backwards rationalization. **Fix:** delete §4.2; it is not load-bearing once Appendix A supplies the cyclotomic derivation. Cite [J9] for the 73-cell HARMONY count as a separate empirical observation about TSML, not as a bridge to $T^*$.

**Issue M2 — variance budget.** The referee notes Bandyopadhyay's $Q$ values span $10^2$–$10^3$, which after normalization could give intra-sample spread $> 0.1$. **Fix:** §2.4 gets a new paragraph computing the implied $Q_c$ variance from published Bandyopadhyay scatter under the (a)-ceiling normalization. If the implied $\sigma(Q_c)$ exceeds 0.05, *widen* the falsification window to $\pm 0.1$ honestly rather than insisting on $\pm 0.05$. The prediction is still falsifiable — the value $T^* = 5/7$ is far enough from 0.5 or 1.0 that even $\pm 0.1$ separates the claim from a null.

**Issues M4, M5, M6 — "wager" rhetoric, undefined "framework", scope-creep.** **Fix:** delete the "wager" sentence from the abstract; move the §5.2 scope-disclaimer paragraph into §1.1 before any Orch-OR-adjacent content; add a 4-line "What is the TIG framework?" paragraph as §1.0 that names TSML, BHML, the 4-core, and the role of $T^*$ as the substrate coherence threshold (not a consciousness threshold).

**Issues M3, M7 — strong falsifiability and self-contained framework intro.** Reframe the abstract's "strongly falsifiable" to **"falsifiable in principle, awaiting laboratory partner"**, and explicitly position the paper as a **proposal** in the J. Theor. Biol. proposal register, not as a deposited pre-registration. The §5.3 outreach materials become §6 *Outreach status*.

**Issue M8 — Tegmark 2000 decoherence critique.** **Fix:** add a §3.2 paragraph engaging Tegmark 2000 *Phys. Rev. E* and Reimers et al. 2009 directly. The standard quantum-biology critique is that decoherence times in microtubules are too short for biological function. The framework's response: $T^* = 5/7$ does *not* require room-temperature long-lived coherence; it predicts the *normalized* quality factor's structural ceiling. A short-decoherence-time microtubule with $Q_\mathrm{measured} / Q_\mathrm{structural\ max} \to 5/7$ is *consistent* with Tegmark and with the framework's prediction.

## §3 — Revision time

Estimate: **15–20 person-hours**, plus a co-author pass. Decomposition:

- Issue 1 (delete + rewrite bridge claim): 1 hour
- Issue 2 (operational $Q_\mathrm{structural\ max}$): 4 hours (literature on tubulin-lattice acoustic velocity + decision between ceiling forms)
- Issue 3 (Appendix A self-contained derivation): 4 hours (compress [J20] cyclotomic proof to 2 pages, no new math)
- M1, M2, M4–M8 (surface fixes, variance budget, framework intro, Tegmark engagement): 4 hours
- Coordination with Bandyopadhyay / Hameroff / Penrose Foundation outreach: out of scope for the paper itself but flagged in §6
- Brayden's referee-rigor pass: 2 hours

This is a one-week revision under normal pace.

## §4 — PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN** (in this paper, via Appendix A): $\mathbb{Z}/10\mathbb{Z}$ admits a unique $2 \times 2$ torus structure with aspect ratio $5/7$, by cyclotomic Galois closure (full proof from [J20]; compressed in Appendix A).
- **COMPUTED** (verified via the J-series companions, cited): six independent derivations converge on $T^* = 5/7$ from cyclotomic forcing (J20), the Flatness Theorem (J6), TSML cell counts (J9), the $\sigma$-rate theorem (J01 / D71), the gate-rate distribution (J51), and the runtime attractor (J41 / D78).
- **STRUCTURAL RHYME**: $T^*$ also surfaces in particle-physics mixing (CKM Cabibbo refinement, PMNS atmospheric — J46) and in cosmology (5/7 horizon ratio in freeze-thaw transit — J3 / J16). These are cited as motivation for the cross-domain bet, *not* as derivations.
- **OPEN**: Whether $T^*$ governs the microtubule $Q_c$ ratio under the (a)-ceiling normalization, with biological variance $\ll \sigma(Q_c)$. This is the experimental question the paper proposes. **Status: awaiting laboratory partner.**

## §5 — Lens-ownership

J49 does not directly read TSML lens variants. The paper sits at the **lens-invariant** layer of the family — $T^* = 5/7$ is invariant across RAW / SYM / SYM_lower (J20 / J6 derivations are torus-structural, not cell-bit-dependent). Cite this explicitly in the lens-ownership paragraph (§0):

> *Lens and substrate.* The constant $T^* = 5/7$ predicted in this paper is **lens-invariant** on the canonical $\mathbb{Z}/10\mathbb{Z}$ substrate: it follows from the cyclotomic Galois closure (a structural, not table-bit-level, property), not from any specific lens choice (RAW / SYM_upper / SYM_lower) of the TSML composition table. The empirical bet is that this invariant governs a normalized biophysical observable.

The 4-core $\{V, H, Br, R\}$ at $\alpha_M = 1/2$ is *not* directly invoked in J49's prediction — the connection runs through J41's runtime attractor, not through the closed-form $H/Br = 1+\sqrt{3}$. Note in §6 (Citation chain): "J41's closed-form attractor and the $T^* = 5/7$ threshold are companion structural facts — different invariants of the same substrate."

## §6 — Retitle / retarget

**Title.** Drop "Substrate-Algebra Prediction" (the referee called it opaque). New title: **"Microtubule terahertz coherence quality $Q_c \to 5/7$: a pre-registered prediction from finite algebraic combinatorics"** (referee's exact suggestion, kept verbatim).

**Venue.** Stay at *Journal of Theoretical Biology* — the referee's *Reject* with "path to resubmission" is genuinely a *Major Revision* if Issues 1–3 are addressed. JTB *does* accept proposals, *does* engage cross-domain mathematical biology, and the experimental protocol is JTB-appropriate.

**Alternative if JTB redirects:** the *Bulletin of Mathematical Biology* would accept a tighter-scoped version; *Theoretical Biology and Medical Modelling* would also be open. *PLOS Computational Biology* is wrong (no computation); *Physics of Life Reviews* is wrong (review venue, not pre-registration).

**Retarget timing.** Hold for Phase 6 alongside lab-collaboration outreach (Bandyopadhyay group at NIMS-Tsukuba; Hameroff group at U Arizona; Penrose Foundation). Do not submit to JTB until at least one of (J20, J6, J9, J01, J51, J41) is on arXiv. This addresses Issue 3 directly: when the JTB referee asks "where can I read the algebraic provenance?", at least one J-companion will have an arXiv ID.

**Submission gate:** (a) Appendix A drafted; (b) one of J20 / J6 / J33 (the cleanest cyclotomic / flatness / forcing-axiom derivations) on arXiv; (c) initial conversation with at least one of the three target labs.
