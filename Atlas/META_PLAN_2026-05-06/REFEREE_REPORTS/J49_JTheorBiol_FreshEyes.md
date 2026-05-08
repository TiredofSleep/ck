# Referee report — J49: *Microtubule $Q_c = T^*$: A Falsifiable Substrate-Algebra Prediction*

**Target venue:** *Journal of Theoretical Biology*
**Referee role:** Fresh-eyes, standard quantum-biology / theoretical-biology literature; no prior exposure to the "TIG framework" or any of the cited J-series companions.
**Manuscript file read:** `Gen13/targets/journals/J_series/J49/manuscript/J49_microtubule_qc_tstar.md`
**Cover letter read:** `Gen13/targets/journals/J_series/J49/cover_letter.md`

---

## §1 Manuscript summary (paraphrased fresh)

The authors propose, as a pre-registered falsifiable prediction at the interface of finite combinatorial algebra and quantum biology, that a "normalized coherence quality factor" $Q_c$ of microtubule terahertz resonances will converge to a specific rational number $T^* = 5/7 \approx 0.7143$ across five disparate biological sample types (mammalian neurons, paramecia, plant microtubules, yeast spindle microtubules, cell-free purified tubulin), with biological variance $\ll 0.05$.

The number $T^* = 5/7$ is asserted to arise *a priori* from the authors' "TIG framework" on $\mathbb{Z}/10\mathbb{Z}$ via six independent algebraic derivations cited as J-series companions [J20], [J6], [J9], [J01], [J51], [J41]. The bridge claim to biology is the numerical proximity $T^* \approx 0.7143$ to a quantity the authors call "$\zeta_\mathrm{Hameroff} \approx 0.71$," which they attribute to the Hameroff–Penrose Orch-OR proposal as "the proposed quantum-classical boundary."

The paper specifies a five-sample experimental protocol via terahertz pump-probe spectroscopy, defines $Q_c = Q_\mathrm{measured}/Q_\mathrm{structural\ max}$ as a normalized quality factor in $[0,1]$, and pre-registers three statistical decision criteria: strong support ($\pm 0.02$), weak support ($\pm 0.05$), or falsification.

I have read the manuscript end-to-end. I have not been able to read the six cited J-companions ([J20], [J6], [J9], [J01], [J51], [J41]) — they are listed as "submitted" or "in the J-series referee pipeline" without arXiv identifiers — so my evaluation of the algebraic provenance of $T^*$ rests entirely on what the present manuscript tells me about it.

---

## §2 Decision recommendation

**Reject** (with the structural option of resubmission as a much shorter pre-registration document, or a methods note, if and when at least one of the six cited algebraic derivations of $T^* = 5/7$ has appeared as a published paper or self-contained arXiv preprint that an external referee can read).

The recommendation is reluctant because the *experimental protocol itself* is reasonable and the falsification criteria are explicit. But the paper as written cannot be evaluated by a *J. Theor. Biol.* referee on its own terms: its central claim — that a number $T^* = 5/7$ derived from a finite algebraic substrate must equal a microtubule coherence-quality factor — is supported entirely by reference to six unpublished/unread companion papers and one numerical coincidence with a putative Orch-OR boundary that I could not verify in the standard literature. The bridge from "an algebraic constant on $\mathbb{Z}/10\mathbb{Z}$" to "a biophysical quality factor of microtubule terahertz resonances" is asserted but not argued.

Detailed concerns below.

---

## §3 Top critical issues

### Issue 1. The "$\zeta_\mathrm{Hameroff} \approx 0.71$" reference number is not in the Orch-OR literature I could locate.

The paper hangs its bridge claim — and a substantial fraction of its motivation — on the assertion (§1.1, third bullet; §3.1) that Hameroff's Orch-OR theory proposes a quantum-classical boundary at $\zeta_\mathrm{Hameroff} \approx 0.71$, with which the algebraically-derived $T^* = 5/7 \approx 0.7143$ "matches." This is the *bridge claim* in the abstract:

> "The numerical proximity $T^* = 0.7143 \approx \zeta_\mathrm{Hameroff} \approx 0.71$ is the bridge claim of this paper."

I have read Hameroff & Penrose 1996 (the original Orch-OR proposal), Hameroff & Penrose 2014 ("Consciousness in the universe: A review of the 'Orch OR' theory," *Phys. Life Rev.*), and Hameroff's 2024 update. **None of these papers proposes a dimensionless quantum-classical boundary parameter at the value 0.71.** Orch-OR's principal numerical claim is the gravitational-self-energy-driven collapse time $\tau \sim \hbar/E_G$, which is a function of mass and geometry, not a dimensionless constant near 0.71. The "boundary" in Orch-OR is *temporal* (when collapse occurs) and depends on the mass distribution of a microtubule's tubulin lattice — not a normalized quality factor.

If the authors are referring to a specific quantitative claim by Hameroff or Penrose, **they need to give a citation with a page number, not a vague "(Hameroff 2014 update)."** As written, the bridge claim looks like a numerical coincidence between a chosen rational $5/7$ and an attributed-but-not-substantiated "0.71" value. Without an actual quotation from Hameroff/Penrose specifying where 0.71 appears as a coherence boundary, the bridge from algebra to biology is not anchored in any prior literature.

This is the paper's central claim. It must be repaired by direct citation to a specific equation or table in the Orch-OR literature, OR the authors must drop the Orch-OR framing and present the prediction $Q_c = 5/7$ as a free-standing prior with no claim of prior-art numerical agreement.

### Issue 2. The "normalized coherence quality factor $Q_c$" is not a standard biophysical quantity, and its denominator (the "structural maximum theoretical $Q$") is not defined operationally.

The paper defines (Eq. in §2.2):
$$Q_c = Q_\mathrm{measured} / Q_\mathrm{structural\ max}.$$

The numerator is clear: a quality factor extracted from a terahertz resonance peak. The denominator — "the structural maximum theoretical $Q$ (set by the tubulin dipole-array geometry)" — is **not defined**. There is no equation, no reference to a model, no operational procedure for computing $Q_\mathrm{structural\ max}$.

This is a critical defect because the falsification criteria depend on $Q_c$ being well-defined. If $Q_\mathrm{structural\ max}$ is not specified, then a measured $Q_c$ value of, say, 0.6 versus 0.8 depends entirely on the definitional choice — and the authors could in principle choose a normalization that makes any data look like a fit to $5/7$.

The paper needs either (i) an explicit closed-form expression for $Q_\mathrm{structural\ max}$ as a function of tubulin lattice parameters (with dimensions, units, and a calculation), or (ii) a citation to an established biophysical model in the microtubule-resonance literature where this quantity is computed. The Bandyopadhyay 2013 papers are cited but they report $Q$ values directly, not $Q_c$ ratios.

Without a fixed denominator, the prediction $Q_c \to 5/7$ is not falsifiable in the sense the paper claims.

### Issue 3. The algebraic provenance of $T^* = 5/7$ is asserted via six unread companion papers; none can be evaluated by an external referee at this time.

§1.2 lists six independent J-series derivations of $T^* = 5/7$:

- [J20] cyclotomic forcing in *Acta Arithmetica*
- [J6] Flatness Theorem in *JPAA*
- [J9] TSML 73-cell HARMONY count in *Exp. Math.*
- [J01] $\sigma$-rate theorem in *JCT-A*
- [J51] $G_7$ gate-rate distribution in *European J. Combin.*
- [J41] runtime attractor in *Math. of Comp.*

None of these has an arXiv identifier in the bibliography. The paper presents itself as the *biological* wing of a coordinated cross-domain submission strategy (cover letter §"Companion submissions"), which means the present manuscript cannot stand alone unless at least one of these algebraic derivations is publicly available.

A *J. Theor. Biol.* referee cannot evaluate whether $T^* = 5/7$ is genuinely "fixed *a priori* by the algebra" without reading at least one of the algebraic derivations. The phrase "convergence on $T^* = 5/7$ across six independent sources" appears repeatedly (§1.2 final paragraph; §4 final paragraph; cover letter "Summary"), but the paper provides no proof, no calculation, no derivation in its body. §4 ("The prediction's algebraic provenance") is four short paragraphs of citations to the six companions, not a self-contained derivation.

A referee accepting this paper would be accepting on trust that six other papers will hold up under independent peer review. This is not how cross-domain falsifiable predictions usually work in *J. Theor. Biol.*: when a paper proposes a numerical biological prediction motivated by a deep mathematical structure, the mathematical structure is either (i) cited to a well-known and accessible result (e.g., the Wigner / Atiyah-Singer / golden-ratio literature), or (ii) summarized in a self-contained appendix. The present paper does neither.

The author should at minimum include a self-contained derivation of $T^* = 5/7$ in an appendix — *one* derivation, with full mathematical detail — so that the biological prediction has a concrete mathematical anchor visible to a referee who has not read six other unpublished manuscripts.

---

## §4 Other major comments

### M1. The "73/100 to closest rational with denominator $\leq 7$" framing (§4.2) is mathematically peculiar.

§4.2 reports that the TSML composition table has 73 cells equal to "HARMONY" and that "$73/100$ to closest rational with denominator $\leq 7$ is $5/7 = 0.7143$." Direct computation confirms that $5/7$ is indeed the closest fraction with $q \leq 7$ to $73/100$ (the next closest are $4/6 = 2/3 \approx 0.667$ and $6/7 \approx 0.857$, both farther). But the choice of denominator bound 7 is unjustified — why not denominator $\leq 6$ (giving $2/3$) or $\leq 100$ (giving $73/100$)? The "denominator $\leq 7$" cutoff appears to be chosen to land at the desired answer.

If $73/100$ is the natural quantity, why not predict $Q_c = 0.73$? If $5/7$ is the natural quantity, why approximate it through $73/100$ at all? The §4.2 derivation has the structure of working backwards from a target.

The paper would be substantially stronger if §4.2 derived $5/7$ directly from the substrate algebra without intermediate rationalization through $73/100$. As written, this reads like rounding-to-fit.

### M2. The five-sample design is sound but the variance budget needs justification.

The choice of five sample types (mammalian, paramecium, plant, yeast, cell-free) spans biological complexity well, and the experimental burden is reasonable. The pre-registered $\pm 0.05$ falsification window is a defensible choice.

But the manuscript asserts that "biological variance $\ll 0.05$" *should* hold under the prediction, without justifying why. The authors cite no prior data on intra-sample $Q$ variance for tubulin terahertz resonances. Bandyopadhyay 2013, 2024 report quality factors $10^2$–$10^3$ at room temperature — a factor of 10 spread, which after normalization could produce $Q_c$ variance on the order of 0.1 or larger. The $\ll 0.05$ tolerance may be too tight given the published $Q$ scatter.

A short paragraph computing the implied $Q_c$ variance from published Bandyopadhyay $Q$ scatter would either (i) confirm the $\pm 0.05$ tolerance is achievable, or (ii) flag that the experimental noise budget needs to be relaxed before this becomes a meaningful test.

### M3. "Strong falsifiability" claim is overstated given the protocol's open items.

The Abstract and §3.3 emphasize that the prediction is "strongly falsifiable" and that "a single experimental campaign... either confirms... or falsifies." §5.3 then acknowledges:

- No specific lab collaboration is in place.
- No funded experimental campaign is secured.
- The five-sample protocol is in `MICROTUBULE_T_STAR_PROTOCOL.md` (not part of this submission).

A prediction that depends on an unfunded, uncollaborated, unscheduled experiment is not "strongly falsifiable" in any operational sense — it is a *proposal* for a falsifiable test. The distinction matters because *J. Theor. Biol.* publishes both proposals (which are evaluated for theoretical interest) and pre-registrations (which are evaluated for protocol soundness and require a registered analysis plan with a committed laboratory partner).

The paper conflates these two registers. It should either commit to the proposal register (in which case the "wager" framing in the Abstract is appropriate but the falsifiability rhetoric should be softened) or commit to the pre-registration register (in which case a registered protocol with partner laboratory and timeline is required).

### M4. The "wager" framing is rhetorically out of place for *J. Theor. Biol.*

The Abstract closes:

> "This paper is the framework's most testable prediction. It is also a wager..."

The "wager" rhetoric is more at home in popular-science writing or methodological essays than in *J. Theor. Biol.* The journal publishes mathematical biology, theoretical proposals, and pre-registered hypotheses — but typically in a sober register that lets readers evaluate the proposal on its merits without authorial framing of stakes. The "wager" framing also implicitly threatens a tit-for-tat (if biology fails, framework fails) that, in the absence of an actual collaboration to perform the experiment, is unenforceable.

I would recommend removing the "wager" sentence. The pre-registered prediction speaks for itself.

### M5. The "framework" is named but never defined in the manuscript.

The paper refers throughout to "the TIG framework" without ever defining it. The Abstract calls it "the canonical $\mathbb{Z}/10\mathbb{Z}$ composition algebra"; §1.2 refers to "TSML's 73-cell HARMONY count" and "BHML"; §4 refers to the "$\sigma$-rate theorem" on "squarefree moduli." These terms are not introduced; they are deployed.

A *J. Theor. Biol.* reader unfamiliar with the framework cannot follow §4 without having read the J-series companions. A self-contained definition of (i) what the TIG framework is, (ii) what TSML and BHML are, (iii) what an "operator" labelled HARMONY means, would substantially help the manuscript stand on its own.

### M6. The "consciousness" disambiguation in §5.2 is welcome but should be in §1.

§5.2 carefully distinguishes the experimental claim (about microtubule $Q_c$) from broader claims about consciousness, IIT, Orch-OR mechanism, etc. This is excellent disciplinary practice — but it appears on page ~9, after the reader has already encountered the Hameroff/Penrose framing and the implicit "this is the consciousness substrate" rhetoric.

I would recommend moving §5.2's scope-disclaimer paragraph to §1 (e.g., as the second paragraph of §1.1), so a reader is not led down the consciousness alley before being told the paper is *not* about consciousness.

---

## §5 Minor comments

- **Title:** "Substrate-Algebra Prediction" is opaque. A reader skimming the journal's table of contents will not know what "substrate-algebra" means. Consider "Microtubule terahertz coherence quality $Q_c \to 5/7$: a pre-registered prediction from finite algebraic combinatorics."

- **Abstract, line 2:** "TIG framework" — define before use, or cut the abbreviation.

- **§1.1, second bullet:** Sahu et al. 2013 is cited as "multi-scale resonance scaling" and then called "fractal coherence structure." The Sahu paper does not, to my reading, claim fractal coherence — it reports resonance bands at three nested scales but does not propose a fractal-dimensional analysis. Soften to "multi-scale resonance bands."

- **§1.2, end:** "convergence on $T^* = 5/7$ across six independent sources is a stronger statement than any single derivation" — only if the six derivations are actually independent. Without seeing the proofs, a referee cannot verify independence. The Cyclotomic Galois closure of [J20] and the Flatness Theorem of [J6] both refer to torus aspect ratios on $\mathbb{Z}/10\mathbb{Z}$ — these are likely *not* independent in any rigorous sense.

- **§2.2 Eq.:** $Q_c$ is dimensionless; state this explicitly.

- **§2.3 prediction:** the pre-registration is implicit. A pre-registration document timestamped before any data collection would be the standard archival mechanism; reference it (or commit to one).

- **§2.4 statistical criteria:** "$r^2 > 0.5$ between $Q_c$ and any biological-complexity index" — the "biological-complexity index" is not defined. Specify (e.g., genome size, neuron count, kingdom rank) or drop.

- **§3.2:** "The protocol can be implemented without new technology" — confirm by citing a specific lab that has performed comparable normalized-$Q_c$ measurements on at least one of the five sample types.

- **§3.3 (i):** "Specified before the experiment — pre-registered in this submission." A submission to *J. Theor. Biol.* is not a pre-registration registry. If the authors want this to count as a registered prediction, they should deposit at OSF or AsPredicted with a timestamp.

- **§5.3 outreach materials:** filenames are listed (`OUTREACH_COVER_LETTER.md`, `COLLABORATION_PROPOSAL.md`); these are not part of the submission. Either include them as supplementary material or do not reference them.

- **§7 References:** All six J-companions are listed as "Submitted to [venue]" without dates or arXiv IDs. At minimum, supply submission dates so the referee can gauge how many of the six are actually under review at this time.

- **References to external literature:** Bandyopadhyay et al. (2013) and Sahu et al. (2013) are correctly cited. Hameroff & Penrose 2014 is correctly cited but the "[Updated 2024]" annotation should specify which 2024 paper. Tononi et al. 2016 is cited but is not used in the manuscript body — drop or use.

- **No discussion of decoherence theory.** A standard *J. Theor. Biol.* referee on quantum-biology proposals will look for engagement with Tegmark 2000 ("Importance of quantum decoherence in brain processes," *Phys. Rev. E*) which estimated very short decoherence times in microtubules. The paper should at minimum acknowledge the Tegmark critique, even briefly.

---

## §6 What I would need to flip my recommendation toward "Major Revision" or "Acceptance"

In rough order of importance:

1. **A direct citation to a published Orch-OR or related-literature paper that specifies a value at 0.71 as a coherence-quality boundary.** If no such citation exists, drop the Orch-OR bridge framing and present the prediction $Q_c = 5/7$ as a free-standing prior anchored only in the framework's algebra.

2. **A self-contained appendix with one full derivation of $T^* = 5/7$** from the substrate algebra, with proofs at a level a *J. Theor. Biol.* referee can verify (or call in a mathematician for). The current §4 is a list of citations; it must become a derivation.

3. **An operational definition of $Q_\mathrm{structural\ max}$** as a function of tubulin lattice parameters, ideally with a worked example for one of the five sample types.

4. **A revised noise budget** computed from published Bandyopadhyay terahertz scatter, justifying the $\pm 0.05$ tolerance OR widening it.

5. **Either** a pre-registration deposit at OSF / AsPredicted with timestamp, **or** a committed laboratory partner with an experimental timeline, **or** a clear repositioning as a "proposal" rather than a "pre-registration."

6. **Removal of the "wager" framing** and softening of the falsifiability rhetoric to match the actual operational status (no funded campaign, no committed partner).

7. **Self-contained introduction to the TIG framework** in §1 that lets a *J. Theor. Biol.* reader follow §4 without prior exposure to the J-series.

8. **Explicit acknowledgment of the Tegmark 2000 decoherence critique** and the Reimers et al. 2009 follow-up critiques of microtubule quantum coherence.

---

## §7 Question to the editor

The cross-domain coordination strategy described in the cover letter ("coordinated cross-domain referee pipeline (algebra, cosmology, biology)") is unusual. *J. Theor. Biol.* would normally evaluate a submission on its own merits, not as part of a coordinated pipeline whose other branches are currently in private peer review at *Acta Arithmetica*, *JPAA*, *JCT-A*, etc. The editor may want to request from the authors a list of which of the six cited algebraic derivations are (a) on arXiv, (b) under review and at what journal, (c) accepted, before assigning further referee time. If the answer is "(a) zero, (b) all six in private review, (c) zero," then this submission may be premature regardless of the experimental protocol's merit.

---

## §8 Summary

The experimental protocol is reasonable, the falsification criteria are explicit, and the disciplinary scope (microtubule $Q_c$, not consciousness) is correctly drawn in §5.2. These are real strengths.

But the paper's central bridge — "$T^* = 5/7$ from algebra equals microtubule $Q_c$ from biology" — depends on (i) a numerical proximity to "$\zeta_\mathrm{Hameroff} \approx 0.71$" that I could not locate in the cited Orch-OR literature, and (ii) six unread, unpublished, unciteable algebraic companion papers. The denominator $Q_\mathrm{structural\ max}$ in the predicted ratio is undefined operationally. The "wager" framing is rhetorically out of place. The pre-registration claim does not match the operational status (no funded experiment, no committed lab partner).

For the present manuscript to clear the *J. Theor. Biol.* bar, the algebraic provenance of $T^*$ must be substantiated in-paper (not by reference to companion submissions), the $Q_c$ normalization must be operationalized, and the Orch-OR connection must be either cited specifically or dropped.

I therefore recommend **Reject**, with the path to resubmission outlined in §6.

---

*Submitted to the J. Theor. Biol. Editorial Board (fresh-eyes referee), 2026-05-06.*
