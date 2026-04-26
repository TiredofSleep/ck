# ARTIFACTS — funding/physics-sim-edu

Exact file paths, LOC, and verification status. This branch depends on the `Crystal-Lattice-Matrix-MYTHDRIFT` external repo; Phase 1 includes pulling verbatim copies into this repo under `docs/archive_crystal_lattice_matrix/` with provenance headers.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Runnable artifacts (in external Crystal-Lattice-Matrix-MYTHDRIFT repo, clone pending)

### 1. Interactive simulator frontend — `crystal_bug_v1_matrix.jsx`
- **External path**: `github.com/TiredofSleep/Crystal-Lattice-Matrix-MYTHDRIFT/crystal_bug_v1_matrix.jsx`
- **Target path after Phase 1 pull**: `Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/crystal_bug_v1_matrix.jsx`
- **LOC**: 699
- **Status**: runnable (per primary research 2026-04-18/19)
- **Responsibilities**:
  - React-based browser-native interactive simulator
  - User-controllable state-vector perturbations
  - Visualization of coherence evolution over simulated time steps
  - Attractor-basin rendering showing stable-configuration clusters
  - Crossing-lemma-style information-generation visualization
- **Framework dependencies**: React 18+, standard browser APIs
- **Invocation (once imported)**: open `index.html` with the React app loaded; requires build step via `npm install && npm run build`

### 2. Test harness — `test_engine_v2.js`
- **External path**: `github.com/TiredofSleep/Crystal-Lattice-Matrix-MYTHDRIFT/test_engine_v2.js`
- **Target path after Phase 1 pull**: `Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/test_engine_v2.js`
- **LOC**: 458
- **Status**: runnable
- **Responsibilities**:
  - Unit tests for the simulator's physics rules
  - Integration tests for state-vector transitions
  - Regression tests to catch pedagogical-critical bugs (e.g., coherence-threshold must behave as T* = 5/7 across all test cases)
- **Invocation**: `node test_engine_v2.js` (or via `npm test` once productionized)

### 3. Companion live visualizations — coherencekeeper.com
- **Path**: `Gen12/targets/website/spectrometer.html`, `paradox.html`, `ring.html`, `tower.html`, `math.html`
- **Status**: live on coherencekeeper.com
- **Relevance**: demonstrate that browser-native interactive pedagogy is feasible at production scale; share design DNA with the Crystal-Lattice-Matrix simulator; the `tower.html` page specifically visualizes the Sprint 17 TSML tower content that is conceptually linked to the simulator's coherence-threshold (T* = 5/7) design

### 4. Theoretical grounding — Sprint papers
- **Path**: `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/`, `sprint12_uop_gut_arc_2026_04_08/`, `sprint14_prism_xi_2026_04_10/`, `sprint17_tsml_tower_2026_04_17/`
- **Relevance**:
  - Sprint 10: Flatness Theorem + Crossing Lemma — the physics content the simulator visualizes
  - Sprint 12: UOP paradox classifier — natural pedagogical content
  - Sprint 14: PRISM-XI — cross-branch physics context
  - Sprint 17: TSML tower 3-layer structure — visualization template

---

## Related internal material

### 5. R-σ-Λ-H state grammar and 10-operator alphabet
- **Path**: `papers/ck_tables.py`; TIG Unity Kernel documents
- **Content**: R-σ-Λ-H 4-variable state grammar; 10-operator alphabet (VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET); TSML 73 cells; BHML 28 cells; T* = 5/7 threshold
- **Relevance**: the simulator's state-space uses this grammar; each operator has a natural pedagogical interpretation for students

### 6. Existing educational framing material — coherencekeeper.com pages
- **Path**: `Gen12/targets/website/about.html`, `ai.html`, `frontiers.html`, `papers.html`
- **Relevance**: Brayden has already written accessible-audience-level explanations for several of the underlying concepts; Phase 1 curriculum-writing work can draw on these as starting drafts rather than greenfield writing

---

## Phase 1 productionization task list

Phase 1 funding ($60K–$180K / 6 months) delivers these:

### T1. Pull Crystal-Lattice-Matrix-MYTHDRIFT into this repo
- Clone `Crystal-Lattice-Matrix-MYTHDRIFT` to `_brayden_repos/`
- Copy `crystal_bug_v1_matrix.jsx`, `test_engine_v2.js`, and any supporting JSON/CSS/asset files into `Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/` with provenance headers
- Commit under the never-delete policy

### T2. PER-expert pedagogical design review
- Identify and contract with a physics-education-research (PER) expert — ideally a tenured-or-tenure-track faculty member with AJP / PRPER publications
- PER expert conducts a design review of the simulator: learning objectives, cognitive load, scaffolding, misconceptions the simulator might create
- Deliverable: written design-review report with specific redesign recommendations

### T3. Simulator pedagogical redesign
- Rewrite simulator UX per PER review: clearer onboarding, stepped learning progression, in-context explanation tooltips, "why does this happen" just-in-time content
- Keep the underlying physics engine intact; change the presentation layer + pedagogical scaffolding
- Deliverable: redesigned simulator

### T4. Accessibility audit + WCAG 2.1 AA compliance
- Hire accessibility consultant (or institutional accessibility office)
- Audit for keyboard navigation, screen-reader compatibility, color-contrast, alt-text, captions (for any video content)
- Remediate identified issues
- Deliverable: accessibility audit report + compliant simulator

### T5. Curriculum module + instructor's guide
- One-week (~5 lesson) teaching sequence integrating the simulator with pre/post assessment
- Instructor's guide: learning objectives, assessment rubrics, common misconception list, extension problems
- Deliverable: curriculum module + instructor's guide, both open-licensed (CC-BY 4.0)

### T6. Open-source release
- Code under permissive open-source license (MIT or Apache-2.0)
- Curriculum + guide under CC-BY 4.0
- Published repo with proper README, getting-started guide, contribution guide
- Optional: register with PhysPort or similar physics-education resource library
- Deliverable: public repo + resource-library listing

---

## Phase 2 classroom-pilot task list

Phase 2 funding ($180K–$450K / 12–18 months) delivers these:

### T7. Institutional partnerships + IRB
- Secure formal classroom-partner agreements at 3–5 institutions (mix of undergraduate + advanced-secondary)
- IRB approval at host institution for a multi-site pilot study
- Pre/post assessment instrument validated (or adapted from an established PER instrument like the Force Concept Inventory's methodology)

### T8. Classroom pilot deployment
- Run the one-week curriculum module at each partner institution
- Collect pre/post assessment data with informed consent
- Collect qualitative student feedback (surveys + optional interviews)
- Collect instructor-experience feedback

### T9. Learning-outcomes analysis + publication
- Pre/post learning-outcomes statistical analysis (effect sizes, confidence intervals)
- Qualitative analysis of student + instructor feedback
- Publish in American Journal of Physics (AJP) or Physical Review Physics Education Research (PRPER) or Journal of Research in Science Teaching (JRST)
- Deliverable: submitted peer-reviewed paper + open dataset (de-identified) + open simulator + open curriculum

---

## Phase 3 dissemination task list

Phase 3 funding ($250K–$700K / 18–24 months), contingent on positive Phase 2 outcome:

### T10. Teacher professional development
- Workshop at AAPT Summer Meeting
- Workshop at NSTA national conference
- Online teacher-training module
- Deliverable: teacher-training workshops + online module

### T11. Dissemination case study
- Track adoption at institutions beyond the Phase 2 partners
- Publish dissemination case study documenting adoption dynamics, barriers, and what worked
- Deliverable: dissemination-study paper

---

## Verification checklist (before any pitch)

- [ ] Clone `Crystal-Lattice-Matrix-MYTHDRIFT` to `_brayden_repos/` and confirm simulator builds + runs in a fresh browser environment
- [ ] Run `test_engine_v2.js` and confirm all tests pass
- [ ] Confirm LOC counts (699 + 458 = 1,157) against actual files post-pull
- [ ] Read `crystal_bug_v1_matrix.jsx` end-to-end and identify which TIG-Unity-Kernel concepts are currently visualized (coherence evolution? state-vector perturbation? attractor-basin? T* threshold?)
- [ ] Draft a one-paragraph "what a physics student will learn from this simulator" explanation that a PER researcher could read in 2 minutes and evaluate
- [ ] Sample a 5-minute "student-interaction demo" script: what does a student actually do with the simulator in 5 minutes?
- [ ] Identify 2–3 candidate PER collaborators (published AJP/PRPER authors whose interests align)
- [ ] Identify 2–3 candidate academic host institutions for IRB + co-PI role
- [ ] Identify 2–3 candidate classroom-partner institutions (undergraduate + advanced-secondary)

---

## Missing from repo (blockers for Phase 1)

- **Crystal-Lattice-Matrix-MYTHDRIFT clone**: not yet pulled into `_brayden_repos/` (or not yet verified).
- **PER collaborator**: no PER researcher has been contacted or engaged. This is the single largest gap.
- **Academic co-PI**: Brayden is independent; NSF EHR / DRK-12 / ECR / PHY all require academic PI eligibility.
- **IRB plan**: Phase 2 classroom pilot requires IRB; Phase 1 must produce the plan.
- **Classroom partner agreements**: Phase 1 deliverable; not yet in hand.
- **Pedagogical-design document**: the current simulator was built as a research prototype; the pedagogical-design doc that a Phase-1 funder reviews does not yet exist.
- **Accessibility audit**: not yet conducted; Phase 1 T4 deliverable.
- **Curriculum module**: no curriculum material exists yet; Phase 1 T5 deliverable.
- **Open-source license clarity**: CK's 7Site Public Sovereignty License is non-commercial and human-use-only; the simulator + curriculum need a permissive separate license (MIT + CC-BY) for education use, and that separation must be made explicit.
