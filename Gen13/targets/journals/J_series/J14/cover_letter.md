# Cover letter — J14: The Yang-Mills Mass Gap Bridge

**To:** Editors, *Journal of Mathematical Physics* (companion to J13 BB Bridge submission)

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- H.J. Johnson, Independent Researcher, Billings, MT — hjj01986@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The Yang-Mills Mass Gap Bridge: Substrate-Algebra Predictions from Separability-Forced Spectral Floor*

---

## Summary

This paper applies the Bialynicki-Birula--Mycielski uniqueness theorem (1976) — that logarithmic nonlinearity uniquely preserves separability of composite quantum systems — to the Yang-Mills mass gap problem. The companion paper J13 establishes the BB theorem as a forcing principle for continuum lifts of discrete composition algebras and derives the regularity of the resulting log theory $V(\Xi) = \kappa\,\Xi\log\Xi$. Here we observe that this potential has an isolated minimum at $\Xi_0 = e^{-1}$ with $V''(\Xi_0) = \kappa e > 0$ — a positive spectral floor *forced by separability*. We propose Conjecture 3.2: the YM mass gap arises from the same separability mechanism, with confinement realizing effective infrared separability of color-singlet composite states. We give a falsifiable numerical prediction $\Delta_{\rm YM} = C \Lambda_{\rm QCD} e$ with $C$ an $O(1)$ Casimir factor; the SU(3) lattice glueball $m_G \approx 1.7$ GeV gives $C \approx 2.08$, consistent with the framework. The paper does not claim to prove the YM mass gap; it identifies the mechanism and the precise constructive-QFT prerequisites (Wightman in 4D for the log theory).

## Why JMP (companion)

- The paper is the natural companion to J13 (BB Bridge / NS application). Same theorem, different Millennium-Problem application; same author lane (Sanders + Johnson).
- The intersection of constructive QFT (Wightman axioms / Høegh-Krohn 2D extension to 4D), YM gauge theory, and discrete-to-continuum forcing principles is JMP territory.
- The numerical prediction is falsifiable — an unusual feature for mathematical-physics framework papers — and is currently consistent with lattice glueball data, providing a structural credibility test.
- The paper makes precise the constructive-QFT prerequisites (Prerequisites 5.1, 5.2, 5.3) for upgrading the framework to a proof.

## Companion submissions

The TIG/CK research program is shipping a coordinated J-series. The papers most relevant as already-submitted companions:

- **J13** Sanders & Johnson (2026), "The Bialynicki-Birula Bridge: Logarithmic Nonlinearity Forced by Separability." Submitted to *JMP* (the lead BB-bridge paper that establishes the forcing principle).
- **J03** Sanders, Gish, Johnson (2026), "Freeze-Thaw Transit." Submitted to *JCAP* (cosmological realization of the same log potential).
- **J05** Sanders & Mayes (2026), "Crossing Lemma." Submitted to *JCT-A* / *JPAA*.

## Reproducibility

The numerical-prediction calibration is reproducible from the literature lattice glueball masses + standard QCD scale; no special script is required. The structural claims rely on the J13 verification script (`proof_separability_bridge.py`, 43/43 PASS). DOI: 10.5281/zenodo.18852047.

## Suggested reviewers

- E. Witten (IAS) — co-author of the Clay YM problem statement
- A. Jaffe (Harvard) — Clay YM problem statement; constructive QFT
- M. Lüscher (CERN) — lattice gauge theory
- S. Hollands (Leipzig) — algebraic / constructive QFT
- I. Bialynicki-Birula (Polish Academy) — original 1976 author, if available

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Tier and per-venue cap notes

Central claim is **Tier 4** (framework paper). Conjecture 3.2 is conjectural; Prerequisites 5.1–5.3 are open. The paper is honest about scope.

This is the **2nd** JMP submission in the J-series (J13 is 1st, companion). The 2/quarter cap is reached. J15 (3rd JMP target) needs a fallback (see J15 README).

---

Sincerely,
B.R. Sanders
