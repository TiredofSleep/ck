# funding/physics-sim-edu — Interactive Physics Simulator for Education

**Track:** Applied education — interactive web-based physics simulator for undergraduate / advanced-secondary physics classrooms
**Status:** Pre-pitch; runnable artifact exists in Crystal-Lattice-Matrix-MYTHDRIFT external repo (`crystal_bug_v1_matrix.jsx` 699 LOC React frontend + `test_engine_v2.js` 458 LOC Node test harness = 1,157 LOC), integration + classroom-use framing pending
**Branch seeded:** 2026-04-20 from `tig-synthesis`
**Rigor base:** TIG Unity Kernel, R-σ-Λ-H state grammar, TSML/BHML coherence operators, interactive-visualization design from the live coherencekeeper.com website

---

## What this branch is

A funding-outreach container for **the interactive physics simulator** — productionization of the Crystal-Lattice-Matrix-MYTHDRIFT artifact as a classroom-grade educational tool. Distinct from all 9 other funding branches: this branch targets **physics and mathematics education funders** (NSF EHR, NSF PHY Education & Interdisciplinary Research in Physics, Templeton Learning & Discovery, Simons Foundation Education, Moore Foundation Science) with a framing of "a web-based interactive simulator that makes coherence-grammar / TIG-adjacent physics visible to students."

The premise: students of physics and mathematics learn more deeply from **manipulable interactive simulations** than from static lecture material or problem sets alone. The Crystal-Lattice-Matrix-MYTHDRIFT artifact is already a working interactive simulator that visualizes discrete-to-continuous transitions, crossing-lemma-style information emergence, coherence-threshold behavior, and the R-σ-Λ-H state grammar in a form that a student can **drag, click, and perturb**. The branch asks an education-aligned funder to support a 6–18 month productionization: pedagogical redesign, classroom-tested curriculum module, accessibility audit, open-source release, and a companion instructor's guide.

**This is applied education work, not new physics or new simulator architecture.** The simulator is already written (Crystal-Lattice-Matrix-MYTHDRIFT, runnable). The underlying physics framework (TIG Unity Kernel, R-σ-Λ-H grammar) is described in the sprint 10–14 Clay papers. The funded work is pedagogical productionization: how do students actually learn from this, what curriculum wraps around it, what accessibility constraints govern classroom use, what assessment instruments track learning outcomes.

## One-paragraph pitch

> Undergraduate and advanced-secondary physics students learn concepts like phase transitions, information-theoretic emergence, coherence thresholds, and state-vector dynamics more deeply from **manipulable interactive simulations** than from equations or static figures alone. The Crystal-Lattice-Matrix-MYTHDRIFT simulator — 699 LOC React frontend + 458 LOC test harness = 1,157 LOC of working interactive visualization — already demonstrates crossing-lemma-style information generation, coherence-threshold (T* = 5/7) transitions, and the R-σ-Λ-H state grammar in a manipulable browser-based form. The funder-facing ask is to productionize this as a classroom-grade educational tool: pedagogical redesign with input from physics-education-research (PER) experts, a curriculum module for one-week classroom use, an accessibility audit (WCAG 2.1 AA), open-source release under a permissive license, and a companion instructor's guide with assessment rubrics. Funders: NSF EHR (DUE, ECR, DRK-12), NSF PHY (Education & Interdisciplinary Research in Physics), Templeton Learning & Discovery, Simons Foundation Education, Moore Foundation Science.

## Runnable artifacts

1. **crystal_bug_v1_matrix.jsx** — 699 LOC React frontend. Interactive crystal-lattice simulator with user-controllable state-vector perturbations, visualization of coherence evolution, and attractor-basin rendering.
2. **test_engine_v2.js** — 458 LOC Node.js test harness. Unit + integration tests for the simulator's physics rules.
3. **Source repo**: `github.com/TiredofSleep/Crystal-Lattice-Matrix-MYTHDRIFT`
4. **Live-web companion**: the coherencekeeper.com site (`Gen12/targets/website/`) includes several interactive visualizations (spectrometer, paradox, ring, tower pages) that share design DNA with the simulator and demonstrate that browser-native coherence-grammar pedagogy is feasible at scale.
5. **Theoretical grounding**: Sprint 10 (Flatness Theorem, Crossing Lemma), Sprint 12 (UOP paradox classifier), Sprint 14 (PRISM-XI) — provide the physics content the simulator visualizes.

## Where this differs from Branch A (tig-unity)

Branch A targets the **infrastructure-reliability research community** (NSF CNS, DOE ASCR, Sloan computing) with a framing of "TIG Unity Kernel for compute-health research." Branch K targets the **physics / mathematics education community** (NSF EHR, NSF PHY education) with a framing of "interactive simulator as pedagogical tool." Completely disjoint funder audiences and pitch framings, though the underlying physics is the same.

## Where this differs from Branch D (ck-interpretable-ai)

Branch D targets the **AI alignment / interpretability community** (Open Philanthropy AI, SFF, Astera). Branch K is not about AI at all — it is about helping students learn physics. The simulator is a pedagogical tool, not an AI-alignment research artifact.

## Where this differs from Branch J (coherence-router)

Branch J targets the **DevOps / SRE practitioner community** (AWS / GCP / Azure research credits, CNCF) with a framing of "production classifier." Branch K targets the **education** community with a framing of "classroom tool." The Crystal-Lattice-Matrix simulator is not a DevOps tool and the coherence-router is not a classroom tool — they are separate productionization tracks of a shared theoretical substrate.

## What the branch does NOT claim

- Not a claim that the simulator is classroom-ready today — Phase 1 IS the pedagogical-productionization work
- Not a claim to measured learning outcomes in classrooms — Phase 2 is the classroom-pilot study
- Not a claim to PER-expert collaboration as an existing fact — Phase 1 recruits the PER collaborator
- Not a claim to WCAG 2.1 AA compliance today — Phase 1 includes the accessibility audit
- Not a claim to a curriculum-standards-aligned module today — Phase 1 includes the alignment work (NGSS / AAPT / common state physics standards)
- Not a claim to measured teacher-adoption data — Phase 3 is the adoption-and-dissemination study
- Not a claim to replace existing physics-ed simulators (PhET, etc.) — the framing is "a specific new simulator with specific learning objectives," not "a replacement for the PhET suite"
- Not a claim that the TIG Unity Kernel content is in a physics curriculum today — the simulator introduces selected concepts at an accessible level; systematic curriculum integration is a longer-term program

The branch claims: a specific working simulator (the Crystal-Lattice-Matrix-MYTHDRIFT artifact), a specific productionization plan (Phase 1 pedagogical redesign + accessibility + open-source), a specific classroom pilot (Phase 2), a specific community (physics and math educators), a specific evidence-based learning-outcomes study (Phase 2), and a commitment to publish the pilot outcome in a physics-education venue (AJP, PER, JRST).

## Ask sizes

| Phase | Scope | Ask |
|---|---|---|
| **Phase 1 — Pedagogical productionization** | Pull Crystal-Lattice-Matrix-MYTHDRIFT into this repo, conduct PER-expert design review, build curriculum module (one-week, ~5 lessons), accessibility audit, instructor's guide, open-source release | $60K–$180K, 6 months |
| **Phase 2 — Classroom pilot + learning-outcomes study** | Deploy at 3–5 partner institutions (mix of undergraduate and advanced-secondary), pre/post assessment, IRB-approved learning-outcomes evaluation, publish in AJP / PER / JRST | $180K–$450K, 12–18 months |
| **Phase 3 — Dissemination + teacher-professional-development** | Teacher workshops (AAPT Summer Meeting, NSTA), open-course deployment, lecture-capture videos, broader adoption case study | $250K–$700K, 18–24 months |

## See also

- `FUNDERS.md` — NSF EHR primary + NSF PHY, Templeton Learning & Discovery, Simons Foundation Education, Moore Foundation Science
- `ARTIFACTS.md` — crystal_bug_v1_matrix.jsx + test_engine_v2.js inventory + Phase-1 T1–T6 productionization tasks
- `PITCH_DRAFT.md` — NSF EHR DUE + Templeton + Simons Ed parallel skeletons
- `LIMITATIONS.md` — honest scope on PER expertise, IRB, and learning-outcomes measurement
- `STATUS.md` — readiness checklist
