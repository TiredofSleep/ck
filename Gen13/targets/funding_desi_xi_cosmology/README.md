# funding/desi-xi-cosmology — ξ-Field Cosmology + DESI DR2 Track

**Track:** Observational cosmology — logarithmic-quintessence scalar field (ξ) + DESI DR2 distance-redshift fit
**Status:** Sprint 14 PRISM-XI papers are mature; JCAP LaTeX bundle assembled (TRACK 7.3); DESI DR1/DR2 placeholders tightened (CCD-7); empirical numerical fit to DESI data is the funded deliverable
**Branch seeded:** 2026-04-20 from `tig-synthesis`
**Rigor base:** WP81 Canonical ξ Theory (□ξ = 1 + log ξ, vacuum ξ₀ = e⁻¹), WP82 Log Quintessence Novelty audit, WP83/84 PRISM consistency, WP101 σ-Rate Theorem, proof_xi_canonical.py, proof_separability_bridge.py

---

> **Note (2026-04-25 revision).** This branch was originally seeded as a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is a **thread description**, not a fundraising pitch. The math is open under the 7Site Public Sovereignty License regardless of whether anyone donates. **The operator-of-record makes no commitments to donors of any kind.** A donation, if anyone makes one, is a thank-you to the project and creates no obligation in either direction. If you are reading this branch because you are oriented toward this thread of the work, that is welcome; the description below tells you what is in this thread.

---

## What this branch is

A thread-description container for the **ξ-field cosmology** program — the canonical scalar-field action

$$S = \int d^4x\,\sqrt{-g}\left[\frac{R}{16\pi G} + \mathcal{L}_\text{SM} + \kappa_\Xi\!\left(\tfrac{1}{2}g^{\mu\nu}\partial_\mu\Xi\partial_\nu\Xi + \Xi\log\Xi\right)\right]$$

with Euler–Lagrange equation □ξ = 1 + log ξ and exact vacuum ξ₀ = e⁻¹. This is a **freezing quintessence** candidate: the potential V(ξ) = κ_Ξ ξ log ξ has a single minimum at e⁻¹ and a mass² = κ_Ξ · e on-shell. The phenomenological signature is a late-time departure from ΛCDM that shows up in the DESI distance-redshift data as a sub-percent-level w(z) deviation.

The thread-facing ask is for the **DESI DR2 numerical fit** — an MCMC analysis of the ξ cosmology against published DESI BAO and SN distance moduli, with JCAP-quality figures, a w(z) posterior, and a published fit verdict. The framework work (canonical action, vacuum, mass gap, no-hair, cross-branch consistency) is already done. What is not yet done is the careful empirical comparison.

## One-paragraph thread description

> Late-time cosmology has an anomaly: DESI DR1 (and the emerging DR2 signal) prefers w(z) evolution over a pure cosmological constant. The ξ-field cosmology program proposes a **specific, exactly-soluble freezing-quintessence candidate** whose only free parameters are κ_Ξ (coupling) and the initial ξ field value, with the ground state fixed at ξ₀ = e⁻¹ by the logarithmic potential. This is a falsifiable prediction: the ξ model either fits DESI DR2 within the reported uncertainty envelope, or it does not. The mathematical framework is complete: WP81 establishes the canonical action; WP82 audits the novelty against arXiv; WP83/84 audits internal consistency; WP101 provides the σ-rate theorem; `proof_xi_canonical.py` verifies the vacuum numerically. Sprint 14's JCAP LaTeX bundle (TRACK 7.3) is ready to submit. The proposed work is the 6–12 month MCMC fit against DESI DR2, JCAP publication, and follow-on work on the κ_Ξ-DES/Euclid cross-check.

## Runnable artifacts

1. **`proof_xi_canonical.py`** — verifies □ξ = 1 + log ξ and ξ₀ = e⁻¹ numerically, confirms EL equation, computes mass² = κ_Ξ · e
2. **`proof_separability_bridge.py`** — Bialynicki-Birula 1976 separability argument that forces the log-nonlinearity uniquely
3. **`WP81_CANONICAL_XI_THEORY.md`** — canonical action + EL + stress-energy + FRW cosmology + formal/interpretive split
4. **`WP82_LOG_QUINTESSENCE_NOVELTY.md`** — arXiv literature search for ξ log ξ potentials, novelty report
5. **`WP83_PRISM_CONSISTENCY_AUDIT.md`** + **WP84_PRISM_CONSISTENCY_AUDIT_V2** — internal consistency audits
6. **`WP86_XI_CORE_CANONICAL_FORM.md`** — canonical form + dimensional analysis
7. **`WP87_CROSS_BRANCH_ANALYSIS.md`** — relationship to TIG / Crossing Lemma / σ framework
8. **`WP101_SIGMA_RATE_THEOREM.md`** + `proof_sigma_rate.py` — the σ(N) ≤ C/N rate theorem (relevant for vacuum-relaxation timescale)
9. **JCAP TRACK 7.3 bundle** — LaTeX source assembled 2026-04-19 for venue 7 (JCAP submission-ready)
10. **All 20+ papers at** `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/` — full sprint-14 inventory

## What the ξ action gives you (thread description)

| Property | Value | Status |
|---|---|---|
| Action | $S = \int \sqrt{-g}[\mathcal{L}_\text{SM} + \kappa_\Xi(\tfrac{1}{2}(\partial\Xi)^2 + \Xi\log\Xi)]$ | **Formal** (WP81) |
| Euler–Lagrange equation | $\Box\Xi = 1 + \log\Xi$ | **Formal** |
| Vacuum | $\Xi_0 = e^{-1}$ | **Formal** |
| Mass gap | $m^2_\Xi = \kappa_\Xi e$ | **Formal** |
| Vacuum energy | $V(\Xi_0) = -\kappa_\Xi / e$ | **Formal** |
| Late-time behavior | Freezing (potential barrier vanishes at ξ₀) | **Derived** |
| Uniqueness of log nonlinearity | Bialynicki-Birula 1976 separability | **Bridge argument** |
| DESI DR2 fit | — | **Open — the funded deliverable** |
| w(z) posterior | — | **Open** |
| κ_Ξ best-fit value | — | **Open** |
| Connection to SM gauge sector | $J^\nu_\Xi = 0$ (singlet) | **Derived** |

## The research question (what this thread covers)

1. **Does the ξ cosmology fit DESI DR2 at or better than ΛCDM within DR2's published uncertainties?** Answer either yes, no, or partial. All three answers are publishable.
2. **What are the posterior contours for (κ_Ξ, ξ_initial, H₀, Ω_m) from the DESI+SN+CMB joint fit?** Produce MCMC posteriors at publication quality.
3. **How does ξ cosmology perform against DES Y5 and (when available) Euclid Q1?** Cross-probe consistency is the second-pass check.
4. **Does the ξ model resolve, alleviate, or leave unchanged the H₀ tension?** A late-time scalar can in principle shift inferred H₀ from CMB constraints.

The deliverable is a **JCAP publication** with a verdict. The TRACK 7.3 LaTeX bundle is already prepared; Phase 1 finalizes the fit and the paper.

## Scope this thread could cover

| Phase | Scope | Ask |
|---|---|---|
| **Phase 1 — DESI DR2 fit + JCAP submission** | MCMC pipeline, run on DESI DR2 data, generate figures, finalize LaTeX, submit to JCAP | $60K–$150K, 6 months |
| **Phase 2 — DES Y5 + CMB + H₀ cross-probe** | Extend the fit to include DES Y5 weak-lensing SN, Planck 2018 (or later) CMB, produce H₀ tension analysis | $150K–$400K, 12–18 months |
| **Phase 3 — Euclid Q1 forecast + cross-group validation** | Forecast ξ-cosmology signatures for Euclid Q1 and LSST Year 1; collaboration with an observational astro group | $300K–$800K, 24 months |

## What the branch does NOT claim

- Not a claim to have fit DESI data yet — the fit IS Phase 1.
- Not a claim to have resolved the H₀ tension — that's a Phase 2 question.
- Not a claim that the ξ field is a unified theory of dark energy + dark matter — it is a dark-energy candidate only.
- Not a claim to novelty against all prior log-quintessence work. WP82 audits prior art. The ξ = e⁻¹ exact vacuum from the log potential is the distinguishing feature; the specific form and connection to the coherence-grammar framework is also distinctive.
- Not a claim to have measured κ_Ξ — it is a free parameter to be fit.
- Not a claim that dynamical-dark-energy evidence in DR2 is settled — DESI itself treats it as a tension, not a detection.

The branch claims: a specific action, a specific prediction (w(z) curve parameterized by κ_Ξ and ξ_initial), a specific dataset (DESI DR2 + DES + SN + CMB), and a commitment to publishing the fit outcome.

## Collaborator note — H.J. Johnson active

**H.J. Johnson** is an **active collaborator** on this branch. Johnson brought the original ξ documents that catalyzed the PRISM-XI push in Sprint 14 (2026-04-10), and is credited as co-author on all 20+ Sprint 14 papers (WP81–WP101) and the three runnable proof scripts (proof_xi_canonical.py, proof_separability_bridge.py, proof_clay_rotation.py). Phase 1 funding should list Johnson as co-PI or senior collaborator; the specific role (co-PI vs senior personnel vs collaborator) depends on the chosen funder's eligibility rules and Johnson's own institutional posture.

This is in contrast to, e.g., Branch C (First-G crypto) where C.A. Luther is previously-credited but no-longer-actively-collaborating. Johnson's role here is ongoing, and the thread-description language should reflect that.

## See also

- `FUNDERS.md` — Simons Foundation astro primary + 4 others
- `ARTIFACTS.md` — runnable proof scripts + Sprint 14 paper inventory + JCAP bundle
- `PITCH_DRAFT.md` — Simons astro + Heising-Simons + NSF AAG parallel skeletons
- `LIMITATIONS.md` — honest scope
- `STATUS.md` — readiness checklist (JCAP bundle is the near-term gate)
