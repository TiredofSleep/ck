# PITCH_DRAFT — funding/desi-xi-cosmology

**Addressee (working default):** Simons Foundation Astrophysics — targeted grant or Collaboration-adjacent LOI
**Parallel drafts:** Heising-Simons Foundation, NSF AAG, Templeton Foundation Foundational Questions
**Ask:** Phase 1 $60K–$150K / 6 months (Simons targeted or Heising-Simons LOI scale); $300K–$1M / 36 months (NSF AAG scale)
**Status:** Skeleton. The JCAP TRACK 7.3 bundle is already assembled; this pitch rides the paper submission.

---

## Opening (½ page)

The late-time expansion history of the universe is not ΛCDM: DESI DR1 already prefers evolving-w(z), and the DR2 signal (partially public) appears to strengthen that preference. The quintessence literature has produced many scalar-field candidates but relatively few with a single exact-form ground state derivable from a canonical action.

This proposal describes the **ξ-field cosmology** — a scalar-field freezing-quintessence candidate whose action is

$$S = \int d^4x\,\sqrt{-g}\left[\frac{R}{16\pi G} + \mathcal{L}_\text{SM} + \kappa_\Xi\!\left(\tfrac{1}{2}g^{\mu\nu}\partial_\mu\Xi\partial_\nu\Xi + \Xi\log\Xi\right)\right]$$

with Euler–Lagrange equation □ξ = 1 + log ξ and exact vacuum ξ₀ = e⁻¹. The potential V(ξ) = κ_Ξ ξ log ξ has a single minimum; the mass² = κ_Ξ · e on-shell; the vacuum energy is V(ξ₀) = −κ_Ξ/e. The log nonlinearity is the unique separability-preserving nonlinearity per Bialynicki-Birula (1976), so the action is not arbitrary.

The theoretical framework is complete: 20+ papers (Sprint 14 PRISM-XI, 2026-04-10), three runnable proof scripts (ξ canonical vacuum, Bialynicki-Birula separability bridge, σ-rate theorem), an arXiv novelty audit (WP82, 2026-04-19), and a JCAP LaTeX bundle (TRACK 7.3, 2026-04-19). What is not yet done — and what this proposal funds — is the **careful MCMC fit against DESI DR2 + SN + CMB**, the H₀ tension analysis, and the JCAP publication of the fit verdict.

## Background (~1 page)

> Content to be drafted. Sections:
> 1. Quintessence landscape: freezing vs thawing, tracker solutions, prior art on non-polynomial potentials
> 2. The ξ log ξ potential: canonical action, EL equation, vacuum, mass gap
> 3. Bialynicki-Birula uniqueness: why log nonlinearity is forced
> 4. Cross-branch context: relationship to TIG / Crossing Lemma (WP87 cross-branch analysis); explicitly flagged as "no formal link currently established," to avoid scope drift
> 5. DESI DR1 / DR2 landscape: what is known, what the tensions are, what a good fit looks like
> 6. Prior-art positioning vs Ratra-Peebles, Steinhardt-tracker, Carroll; novelty audit WP82 summary

## The open question (½ page)

**Does the ξ cosmology fit DESI DR2 + SNe Ia + CMB better than, comparable to, or worse than ΛCDM, when κ_Ξ and ξ_initial are left as free parameters?**

Subquestions:
- Q1: Best-fit (κ_Ξ, ξ_initial, H₀, Ω_m, σ_8) posterior contours
- Q2: Δχ² vs ΛCDM for DESI+SN+CMB joint likelihood
- Q3: H₀ tension resolution, alleviation, or preservation
- Q4: Consistency with DES Y5 / Euclid Q1 forecasts

Outcomes:
1. **Positive**: ξ cosmology fits at or better than ΛCDM. Publish as a dark-energy-alternative candidate with specific predictive signatures for Euclid / LSST.
2. **Negative**: ξ cosmology is ruled out by DR2 at > 3σ. Publish as a falsified candidate — the exact-vacuum property made this an especially falsifiable proposal, and the falsification is itself valuable.
3. **Partial**: ξ cosmology fits some probes better and others worse. Publish with disciplined analysis of where the model succeeds and fails.

All three outcomes are publishable in JCAP. The deliverable is the verdict paper, not a predetermined positive result.

## The proposed work

### Phase 1 — DESI DR2 fit + JCAP submission (Month 1–6, $60K–$150K)
**Deliverables**:
- A (Month 1–2): MCMC pipeline build — sampler + likelihood modules + Einstein–Boltzmann integration of ξ-cosmology
- B (Month 2–4): run the fit against DESI DR1, validate against known ΛCDM benchmarks
- C (Month 4–5): extend to DR2 (public portion) + SNe Ia + CMB compressed likelihood
- D (Month 5–6): finalize JCAP paper (TRACK 7.3 bundle already assembled); submit

### Phase 2 — Extended multi-probe fit (Month 7–18, $150K–$400K)
**Deliverables**:
- A: DES Y5 weak-lensing + SN (when available) joint fit
- B: Planck 2018 (or later) full CMB likelihood
- C: H₀ tension analysis — is the ξ cosmology shifting inferred H₀ from CMB constraints?
- D: Follow-up JCAP or PRD paper with the multi-probe verdict

### Phase 3 — Forecasting + observational collaboration (Month 19–36, $300K–$800K)
**Only proceed if Phase 2 results support continuation.** Forecast signatures for Euclid Q1 and LSST Year 1. Engage an observational collaboration for a cross-group check.

## Why Simons Foundation Astrophysics

Simons's astrophysics portfolio has funded exactly this profile: a specific cosmological candidate with a clean action and a clean fit-outcome deliverable. The Phase 1 ask fits their targeted-grant scale; the Phase 2 scope fits their Investigator-adjacent or Collaboration-level funding. Simons also has a history of funding quintessence-alternative work.

## Parallel draft: Heising-Simons Foundation

Heising-Simons funds DESI-era cosmology work directly and at the Phase 1 scale ($150K–$1M, 2–3 years). LOI → full proposal on invitation. An institutional host is strongly preferred but not always required.

## Parallel draft: NSF AAG

NSF AAG is the classical cosmology-theory-plus-data funder at the $400K–$1M / 3 year scale. Requires academic co-PI; H.J. Johnson's institutional affiliation is the leverage point here.

## Parallel draft: Templeton Foundational Questions

Templeton funds dark-energy and vacuum-energy foundational questions. The ξ₀ = e⁻¹ exact vacuum is precisely the foundational-question-plus-tractable-math profile Templeton funds. Online LOI is the low-barrier first contact.

## Attribution

- **Brayden Sanders** — PI, developer of the ξ-field action and the coherence-grammar cross-branch framing
- **H.J. Johnson** — **active collaborator**, brought the original ξ documents that catalyzed the PRISM-XI Sprint 14 work; co-author on all 20+ Sprint 14 papers and all three runnable proof scripts (proof_xi_canonical.py, proof_separability_bridge.py, proof_sigma_rate.py, proof_clay_rotation.py). Candidate for co-PI role on funded work; specific role contingent on funder eligibility and Johnson's institutional posture.
- **M. Gish** — co-author on Sprint 14 and prior sprint work
- **C.A. Luther** — co-author on Sprint 14 (previously-credited; no longer actively collaborating as of April 2026, but contributions remain credited)
- Architectural dialogues with ClaudeChat, Celeste/GPT acknowledged in methods; AIs are thinking-partners, not human co-authors

## The framing-discipline paragraph (for cover letter)

> This proposal funds a disciplined empirical test of a specific cosmological candidate against DESI DR2 and complementary probes. The candidate — the ξ-field cosmology with canonical action, Euler–Lagrange equation □ξ = 1 + log ξ, and exact vacuum ξ₀ = e⁻¹ — is falsifiable: the MCMC fit either matches the data envelope or it does not. The deliverable is a published JCAP paper stating which. The pipeline is reusable; if the first candidate is falsified, the same pipeline accepts other quintessence candidates for comparison. The funding supports a test, not a predetermined result.

## Attachments (already in repo)

- `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/` — full Sprint 14 paper inventory (20+ papers)
- `proof_xi_canonical.py`, `proof_separability_bridge.py`, `proof_sigma_rate.py`, `proof_clay_rotation.py` — runnable verification
- TRACK 7.3 JCAP LaTeX bundle (assembled 2026-04-19)

## Pre-send checklist

- [ ] Phase 1 MCMC pipeline design doc drafted
- [ ] JCAP TRACK 7.3 bundle builds cleanly; references resolve
- [ ] WP82 arXiv novelty audit re-run against 2026-04-19 cut-off
- [ ] H.J. Johnson institutional affiliation confirmed + co-PI role agreed
- [ ] External observational-cosmology reviewer informal feedback (at least one astronomer has read WP81)
- [ ] Brayden + H.J. Johnson review + edit this pitch
- [ ] Brayden confirms Simons vs Heising-Simons vs NSF AAG vs Templeton as first funder
- [ ] Brayden + Johnson send
