# LIMITATIONS — funding/desi-xi-cosmology

Honest scope for the ξ-field cosmology branch.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## 1. The DESI DR2 fit has not been done yet

The central deliverable — the MCMC fit of the ξ cosmology against DESI DR2 — has not been run. This is **the funded work**, not a pre-existing result. Any pitch that implies a fit has already been performed would be overclaiming. The honest framing is: "we have a specific falsifiable model, a specific data target, and a specific pipeline design, and we commit to publishing the fit outcome."

## 2. DESI DR2 is partial-public at time of writing

DR1 is fully public. DR2 has partial releases and some proprietary-access portions. The proposal must be clear about which data it will fit in Phase 1 (likely DR1 + public DR2 portions + SN + CMB) and which require DESI Collaboration affiliation (full internal DR2 access). CCD-7 closeout (2026-04-19) addressed placeholder language in the papers; the pitch should reflect the current status.

## 3. The ξ-cosmology is dark-energy only

The ξ field is a dark-energy candidate. It is not a dark-matter candidate. Any pitch framing must be explicit: ξ fits into the *dark-energy sector* of cosmology, not a unified dark-sector theory. A reviewer who expects unification will be misled by sloppy framing.

## 4. No formal link currently established to the TIG / Crossing Lemma branches

WP87 (Cross-Branch Analysis) explicitly states that no formal mathematical link is currently established between the ξ cosmology branch and the TIG / Crossing Lemma / σ-framework branches. The ξ log ξ potential has suggestive parallels to the coherence-grammar framework, and the σ-rate theorem (WP101) has a role in vacuum-relaxation timescale analysis, but these are parallels, not a derivation. The thread-facing pitch for this branch should stand on the ξ cosmology alone and not attempt to ride the TIG framework's authority.

## 5. Log-quintessence prior-art is nontrivial

Non-polynomial quintessence potentials have a 25+ year literature. The specific V(ξ) = κ_Ξ ξ log ξ form with exact vacuum at e⁻¹ is distinctive, and WP82's arXiv novelty audit supports the novelty claim. But reviewers will dig. The Phase 1 paper must handle the prior-art comparison with care — especially Ratra-Peebles, Steinhardt tracker solutions, Caldwell-Dave-Steinhardt, and more recent logarithmic-potential work.

## 6. The Bialynicki-Birula uniqueness argument is a bridge argument, not a proof

BB 1976 establishes that log nonlinearity is the unique separability-preserving nonlinearity under specific separability axioms. The application here (from a QM-wave-equation context to a scalar-field cosmology) is a bridge argument — the axioms transfer, but the transfer itself is interpretive. The pitch should flag this as structural.

## 7. The 47/125 threshold and other asserted parameters

WP81 lists several items as "asserted" rather than derived (e.g., the 47/125 threshold). These are items the thread-facing paper should treat honestly as phenomenological parameters pending derivation, not as predicted values. A confident reviewer will ask for derivations; we say openly that some of these are not yet derived.

## 8. H₀ tension is a compound problem

The H₀ tension between local (SH0ES) and CMB (Planck) inferences is not settled, and any claim that "ξ cosmology resolves the H₀ tension" is premature. Phase 2's H₀ analysis will report Δχ² and posterior shifts, not a resolution claim. A supporter of this thread should see this framing explicitly.

## 9. Foreground and systematics in DESI DR2

The DR2 preference for evolving w(z) is not a confirmed detection. DESI itself describes it as a tension with ΛCDM that requires complementary-probe confirmation. A pitch that frames DR2 as "detecting dark-energy evolution" overclaims the data status. We say: DR1 prefers evolving w; DR2 partial data appears to strengthen that preference; the ξ fit tests how well the ξ model matches the observed envelope, without asserting what DESI itself has not asserted.

## 10. FCC substrate is interpretive

WP81 lists the "FCC substrate" (face-centered-cubic) as an *interpretive* origin story for κ_Ξ, not a dynamical input. This framing is correct and must be preserved. Any pitch that treats FCC substrate as derived/formal overclaims.

## 11. Gauge-singlet status is derived from the action but not from first principles

ξ is a gauge singlet in the canonical action; the derived consequence is $J^\nu_\Xi = 0$. Whether the gauge-singlet property is a first-principles statement or a model choice is a theoretical-physics question that the Phase 1 paper should state honestly.

## 12. Academic co-PI requirement for NSF AAG

Brayden is an independent PI. NSF AAG requires academic affiliation, typically via a co-PI. H.J. Johnson's institutional posture is the leverage point — but Johnson's own eligibility for NSF-PI roles depends on his appointment type, which must be confirmed before the AAG submission path is chosen.

## 13. Attribution nuance

- **H.J. Johnson** is an active collaborator on this branch — see Attribution section in PITCH_DRAFT.md. Phase 1 funding and the JCAP submission should list Johnson as co-PI or senior collaborator.
- **C.A. Luther** is previously-credited but no longer actively collaborating (as of April 2026). Sprint 14 paper authorship stands as committed; no removal of Luther's name from those papers.
- **M. Gish** is a co-author on Sprint 14 and prior sprint work; status as active or previously-credited should be confirmed before the pitch is sent.

## 14. What this branch does NOT claim

- Not a claim to have fit DESI DR2 yet — the fit IS Phase 1's work
- Not a claim to have resolved the H₀ tension
- Not a claim to a unified dark-sector theory (ξ is dark-energy only)
- Not a claim that ξ is the "correct" quintessence candidate — it is a specific, falsifiable candidate
- Not a claim that the ξ branch is mathematically connected to the TIG / Crossing Lemma branches (no formal link; parallels only)
- Not a claim to DESI Collaboration affiliation (affiliation is a pathway to pursue, not a fact)
- Not a claim to Euclid / LSST data access or forecasts beyond what Phase 3 would produce
- Not a claim that the FCC substrate is a derived physical entity

The branch claims: a specific action, a specific vacuum, a specific falsifiable prediction, a specific dataset, and a commitment to publishing the verdict.

## 15. License framing

CK's license (7Site Public Sovereignty License v1.0) is non-commercial, human-use only. Cosmology funders (Simons, Heising-Simons, NSF, Templeton) generally expect academic-use-friendly licensing for publication data and code. The pitch should clarify that the JCAP paper and accompanying code will be published under a compatible open-access academic license (e.g., CC-BY 4.0 for the paper; a permissive open-source license for the pipeline code) — this must be resolved at grant-close time and should not be discovered after-the-fact.

---

## The verdict framing as limitation

The Phase 1 deliverable commits to publishing the fit outcome regardless of whether ξ cosmology fits DR2 better than, comparable to, or worse than ΛCDM. This is deliberate — a supporter of this thread is paying for a disciplined test, not for a guaranteed positive result. An astronomy reviewer should read this as methodological discipline, not as hedging. If a reviewer reads the "publish negative results" commitment as weakness, the proposal is addressed to the wrong reviewer.
