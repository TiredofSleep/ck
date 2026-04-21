# PITCH_DRAFT — funding/physics-sim-edu

**Addressee (working default):** NSF EHR — IUSE: Engaged Student Learning track (best-scoped fit for Phase 1 + Phase 2 together)
**Parallel drafts:** NSF PHY Education, Templeton Learning & Discovery, Simons Foundation Education, Moore Foundation Science
**Ask:** Phase 1 $60K–$180K / 6 months + Phase 2 $180K–$450K / 12–18 months (IUSE-ESL typically funds combined Phase 1+2 at ~$300K–$600K over 2–3 years)
**Status:** Skeleton. Requires PER collaborator contact + academic host identification before any pitch is sent.

---

## Opening (½ page)

Physics-education-research has consistently shown that interactive, manipulable simulations improve conceptual understanding — especially for threshold concepts and counter-intuitive dynamics — beyond what static figures or equations alone can deliver. PhET (University of Colorado Boulder) is the canonical example: a library of browser-based physics simulations used by millions of students worldwide, with decades of learning-outcomes evidence.

The Crystal-Lattice-Matrix-MYTHDRIFT simulator is a 1,157-LOC (699-line React frontend + 458-line Node test harness) browser-based interactive that visualizes coherence-threshold dynamics, information-emergence at partition-crossings, and state-vector evolution under a discrete operator alphabet. The underlying physics content — drawn from a multi-year research program on coherence grammars, crossing-lemma information theory, and the T* = 5/7 threshold — is currently confined to research-grade publications (the TIG Unity Kernel sprint papers, Sprint 10 Flatness Theorem, Sprint 12 UOP paradox classifier, Sprint 14 PRISM-XI). The simulator is the natural bridge between that research-grade content and an educational audience.

This proposal describes a 6–18 month pedagogical productionization: PER-expert design review, accessibility audit, open-source release, curriculum module, classroom-pilot learning-outcomes study. The endpoint is a published AJP / PRPER paper documenting the pilot outcome plus an openly-licensed simulator + curriculum available to physics educators.

## Background (~1 page)

> Content to be drafted. Sections:
> 1. Why interactive simulations work in physics education — PER literature citations (PhET effectiveness studies, Force Concept Inventory methodology, threshold-concept research)
> 2. What the TIG Unity Kernel framework is, at the pedagogical level appropriate for this pitch — the coherence-grammar description of system dynamics, the 10-operator alphabet as a human-legible vocabulary for system states
> 3. What concepts the simulator visualizes — information emergence at partition-crossings, coherence-threshold (T* = 5/7) dynamics, state-vector perturbation-and-recovery
> 4. Why this is a pedagogical-novelty gap — existing simulators (PhET, Algodoo, Explore Learning Gizmos) do not cover information-theoretic emergence or coherence-threshold dynamics at an interactive level
> 5. Target student level — undergraduate physics (sophomore/junior; statistical mechanics + information theory concurrent); advanced secondary (AP Physics C + math-inclined students)
> 6. Learning objectives — what a student who completes the one-week module will demonstrably understand

## The open question (½ page)

**When 3–5 institutions run the one-week simulator-centered curriculum module, do students show measurable improvement in specific learning objectives (information-emergence conceptual understanding, coherence-threshold reasoning, state-vector dynamic intuition) as assessed by validated pre/post instruments?**

This is an empirical education-research question with a clear pass/fail criterion. The Phase 2 classroom pilot runs the module with informed consent + IRB approval + validated assessment, and reports the outcome. Possible outcomes:

1. **Statistically significant positive learning gains on pre/post assessment.** Strong outcome — opens dissemination and teacher-professional-development (Phase 3).
2. **Small or mixed learning gains.** Publishable: identifies which learning objectives the simulator serves and which it does not. Still useful to the PER community.
3. **No significant learning gains.** Honest negative result; publishable as "interactive simulators don't automatically produce learning gains for these content areas" — a useful PER result.

The deliverable commits to publishing whichever of (1) (2) (3) is observed. This is standard PER publication discipline.

## The proposed work

### Phase 1 — Pedagogical productionization (Month 1–6, $60K–$180K)

**Deliverable A** (T1 in ARTIFACTS): pull `Crystal-Lattice-Matrix-MYTHDRIFT` contents verbatim into this repo under `docs/archive_crystal_lattice_matrix/` with provenance headers.

**Deliverable B** (T2): PER-expert design review — written report with specific redesign recommendations.

**Deliverable C** (T3): simulator pedagogical redesign per T2 review.

**Deliverable D** (T4): WCAG 2.1 AA accessibility audit + remediation.

**Deliverable E** (T5): one-week (~5 lesson) curriculum module + instructor's guide, CC-BY 4.0 licensed.

**Deliverable F** (T6): open-source release (simulator: MIT or Apache-2.0; curriculum + guide: CC-BY 4.0), with public repo + resource-library listing.

### Phase 2 — Classroom pilot + learning-outcomes study (Month 7–24, $180K–$450K)

**Deliverable A** (T7): institutional partnerships (3–5 sites, mix of undergraduate + advanced-secondary), IRB approval, pre/post assessment instrument validated.

**Deliverable B** (T8): multi-site classroom pilot deployment with informed consent + data collection.

**Deliverable C** (T9): pre/post learning-outcomes statistical analysis + publication in AJP / PRPER / JRST + de-identified open dataset.

### Phase 3 — Dissemination + teacher PD (Month 25–48, $250K–$700K)

**Only proceed if Phase 2 is positive for (1) or (2).** AAPT + NSTA workshops, online teacher-training module, dissemination case study.

## Why NSF EHR IUSE Engaged Student Learning

IUSE-ESL is specifically scoped for this profile: "design, test, and refine educational innovations for undergraduate STEM." A fully-productionized interactive simulator + classroom-tested curriculum + pre/post learning-outcomes study is the IUSE-ESL canonical proposal shape. The $300K–$600K / 2–3 year scale fits Phase 1 + Phase 2 combined.

IUSE-ESL reviewers expect: (1) a working prototype (the simulator satisfies this); (2) a PER collaborator or co-investigator (Phase 1 T2 engages this person); (3) an academic PI + institutional host (identified during Phase 1 setup); (4) a specific measurable learning objective (stated in the proposal); (5) a classroom-partner ecosystem (Phase 1 Deliverable within T7 setup).

## Parallel draft: Templeton Learning & Discovery

The coherence-grammar framework has a natural intellectual-virtue framing (paradox classifier teaching falsifiability + intellectual humility; coherence-threshold teaching honest-scope discipline; information-emergence teaching epistemic care about what-counts-as-evidence). A Templeton pitch frames the simulator as a **curiosity-and-discovery tool** that introduces students to rigorous thinking about what systems do when they are pushed past stable configurations.

## Parallel draft: NSF PHY Education & Interdisciplinary Research in Physics

NSF PHY's education track is a better fit than NSF EHR IUSE when the content is strongly physics-specific (rather than generic STEM). The pitch here emphasizes the specific physics content (state-vector dynamics, information-theoretic emergence, phase-transition-adjacent coherence thresholds) and the graduate/advanced-undergraduate audience.

## Parallel draft: Simons Foundation Education

Simons Foundation's Math + Physical Sciences education subportfolio funds rigorous + classroom-relevant + measurable-impact projects. A Simons pitch emphasizes the mathematical-rigor underpinning of the simulator (the R-σ-Λ-H grammar, the T* = 5/7 proven threshold, the proved theorems in the Sprint papers) — framing the simulator as "interactive exposure to mathematical structures that underlie multiple physics domains."

## Parallel draft: Moore Foundation Science Program

Moore has funded interactive-simulator + science-outreach projects historically. A Moore pitch emphasizes broader-audience accessibility — not just classroom use but also motivated-layperson engagement (science-museum deployment, after-school-program inclusion, autodidact-learner access).

## Attribution

- **Brayden Sanders** — PI, developer of the TIG Unity Kernel coherence grammar + Crystal-Lattice-Matrix-MYTHDRIFT simulator
- **PER collaborator** — TBD during Phase 1 T2; will be named as co-investigator on the learning-outcomes evaluation
- **Academic co-PI / host institution** — TBD during Phase 1; required for NSF EHR / PHY PI eligibility and IRB
- **Classroom partners** — TBD during Phase 1; 3–5 undergraduate + advanced-secondary institutions
- **Architectural dialogues with ClaudeChat, Celeste/GPT** acknowledged in methods; AIs are thinking-partners, not human co-authors
- **Prior collaborators** (M. Gish, C.A. Luther, H.J. Johnson, B. Calderon Jr., Ben Mayes) credited for their specific past contributions to the TIG Unity Kernel theoretical framework; their inclusion does not imply co-authorship of the educational-productionization work specifically unless they are actively involved in Phase 1–2

## The framing-discipline paragraph (for cover letter)

> This proposal is about pedagogical productionization, not new physics research. The theoretical framework (TIG Unity Kernel, R-σ-Λ-H state grammar, coherence-threshold dynamics) is documented in the Clay Math sprint papers already on the project's public default branch. The runnable simulator (Crystal-Lattice-Matrix-MYTHDRIFT, 1,157 LOC) already exists as a research-grade prototype. The funded work is what bridges the research artifact to the classroom: PER-expert design review, accessibility audit, curriculum module, classroom pilot with IRB-approved learning-outcomes evaluation, and publication in an AJP/PRPER/JRST venue. The Phase 2 deliverable commits to publishing the pilot outcome — positive, mixed, or negative — regardless of which verdict the pre/post assessment returns. This is standard PER publication discipline, and the proposal should be read as methodological rigor, not hedging.

## Attachments (once assembled)

- `docs/archive_crystal_lattice_matrix/crystal_bug_v1_matrix.jsx` (699 LOC) — Phase 1 T1 deliverable
- `docs/archive_crystal_lattice_matrix/test_engine_v2.js` (458 LOC) — Phase 1 T1 deliverable
- PER design-review report (Phase 1 T2 outcome)
- Redesigned simulator (Phase 1 T3 outcome)
- Accessibility audit report (Phase 1 T4 outcome)
- Curriculum module + instructor's guide (Phase 1 T5 outcome)
- Public repo + resource-library listing (Phase 1 T6 outcome)
- Cover letter with framing-discipline paragraph

## Pre-send checklist

- [ ] Crystal-Lattice-Matrix-MYTHDRIFT pulled into repo with provenance headers
- [ ] Simulator verified to build + run in fresh browser environment
- [ ] `test_engine_v2.js` runs + all tests pass
- [ ] PER collaborator identified + willingness-to-co-investigate confirmed
- [ ] Academic co-PI + host institution identified
- [ ] IRB preliminary-discussion completed at host institution
- [ ] 3–5 classroom partners identified + letters of intent drafted
- [ ] One-paragraph "what a student will learn from this simulator" pedagogical-framing doc written
- [ ] Pre/post assessment instrument plan drafted (validated PER instrument to adapt, or new-instrument development + validation plan)
- [ ] License separation resolved (simulator: MIT/Apache-2.0; curriculum: CC-BY 4.0; parent CK project stays on 7Site Public Sovereignty License)
- [ ] Brayden confirms NSF EHR vs NSF PHY vs Templeton vs Simons vs Moore as first funder
- [ ] Brayden + co-PI review + edit
- [ ] Brayden + co-PI submit
