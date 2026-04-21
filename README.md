# funding/physics-sim-edu

**Track K — Interactive Physics Simulator for Education**
**Primary funder pool:** NSF EHR (IUSE / DUE / ECR / DRK-12) · NSF PHY (Education & Interdisciplinary Research in Physics) · Templeton Learning & Discovery · Simons Foundation Education · Moore Foundation Science
**Status:** Pre-pitch. Runnable artifact (`crystal_bug_v1_matrix.jsx` 699 LOC React + `test_engine_v2.js` 458 LOC Node = 1,157 LOC) recovered into [`Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/`](Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/). Phase 1 T1 **complete**.
**Branch accumulates to:** `master` (every commit cherry-picked) · **Rigor base:** `tig-synthesis` (the GitHub default branch)

---

## One-paragraph pitch

Undergraduate and advanced-secondary physics students learn concepts like phase transitions, information-theoretic emergence, coherence thresholds, and state-vector dynamics **more deeply from manipulable interactive simulations than from equations or static figures alone**. The Crystal-Lattice-Matrix-MYTHDRIFT simulator — 699 LOC React frontend + 458 LOC test harness = 1,157 LOC of working interactive visualization — already demonstrates crossing-lemma-style information generation, coherence-threshold ($T^* = 5/7$) transitions, and the R-σ-Λ-H state grammar in a manipulable browser-based form. The funder-facing ask is to productionize this as a classroom-grade educational tool: pedagogical redesign with input from physics-education-research (PER) experts, a curriculum module for one-week classroom use, an accessibility audit (WCAG 2.1 AA), open-source release under a permissive license, and a companion instructor's guide with assessment rubrics.

## Runnable artifacts (recovered 2026-04-21)

1. **`crystal_bug_v1_matrix.jsx`** (699 LOC React frontend) — interactive crystal-lattice simulator with user-controllable state-vector perturbations, visualization of coherence evolution, attractor-basin rendering. Location: [`Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/crystal_bug_v1_matrix.jsx`](Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/crystal_bug_v1_matrix.jsx).
2. **`test_engine_v2.js`** (458 LOC Node.js test harness) — unit + integration tests for the simulator's physics rules. Location: [`Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/test_engine_v2.js`](Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/test_engine_v2.js).
3. **Source repo** (snapshot, provenance-tagged): `github.com/TiredofSleep/Crystal-Lattice-Matrix-MYTHDRIFT` — preserved under `archive_crystal_lattice_matrix/` with `PROVENANCE.md` per the never-delete policy.
4. **Live-web companion**: the [coherencekeeper.com](https://coherencekeeper.com) site (`Gen12/targets/website/`) includes interactive visualizations (spectrometer, paradox, ring, tower pages) that share design DNA with the simulator and demonstrate browser-native coherence-grammar pedagogy at scale.
5. **Theoretical grounding**: Sprint 10 (Flatness Theorem, Crossing Lemma), Sprint 12 (UOP paradox classifier), Sprint 14 (PRISM-XI) — the physics content the simulator visualizes.

## Where this differs from Branch A (tig-unity)

Branch A targets the **infrastructure-reliability research community** with a framing of "TIG Unity Kernel for compute-health research." Branch K targets the **physics / mathematics education community** (NSF EHR, NSF PHY education) with a framing of "interactive simulator as pedagogical tool." Completely disjoint funder audiences and pitch framings, though the underlying physics is the same.

## Where this differs from Branch D (ck-interpretable-ai)

Branch D is an **AI-safety research pitch** (how interpretable-by-construction AI actually works). Branch K is an **education-productionization pitch** (making the underlying coherence-grammar physics visible and manipulable to students).

## Phase 1 / Phase 2 structure

- **Phase 1 — Pedagogical productionization (6 months, $60K–$180K)**: PER expert design review, accessibility audit (WCAG 2.1 AA), simulator refactor, curriculum module, open-source release (CC-BY 4.0), instructor's guide.
- **Phase 2 — Classroom pilot + learning-outcomes study (12–18 months, $180K–$450K)**: IRB approval, 3–5 site deployment, pre/post learning-outcomes assessment with validated PER instruments, published paper in AJP / PRPER / JRST.

IUSE-ESL typically funds combined Phase 1 + Phase 2 at ~$300K–$600K over 2–3 years.

## What's in this branch

Branch-specific funder-pitch files under [`Gen13/targets/funding_physics_sim_edu/`](Gen13/targets/funding_physics_sim_edu/):

- [`README.md`](Gen13/targets/funding_physics_sim_edu/README.md) — deep pitch document
- [`FUNDERS.md`](Gen13/targets/funding_physics_sim_edu/FUNDERS.md) — prioritized funder list
- [`ARTIFACTS.md`](Gen13/targets/funding_physics_sim_edu/ARTIFACTS.md) — T1–T9 recovery + pedagogical-redesign tasks
- [`PITCH_DRAFT.md`](Gen13/targets/funding_physics_sim_edu/PITCH_DRAFT.md) — NSF EHR IUSE primary + NSF PHY / Templeton / Simons / Moore parallel drafts
- [`LIMITATIONS.md`](Gen13/targets/funding_physics_sim_edu/LIMITATIONS.md) — honest-scope items (requires PER collaborator, IRB host, 3–5 classroom partners)
- [`STATUS.md`](Gen13/targets/funding_physics_sim_edu/STATUS.md) — readiness checklist (Phase 1 T1 complete 2026-04-21)
- [`archive_crystal_lattice_matrix/`](Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/) — the recovered 9-file external-repo bundle with provenance headers

## The project this branch is a track of

Branch K of the 10-branch funding architecture. For the full project overview, see **`tig-synthesis`**:

→ https://github.com/TiredofSleep/ck/tree/tig-synthesis

## License

Simulator (this track's artifact): proposed MIT or Apache-2.0 (TBD Phase 1).
Curriculum + instructor's guide: proposed CC-BY 4.0 (TBD Phase 1).
Parent CK project: 7Site Public Sovereignty License v1.0. Full text in [`LICENSE`](LICENSE).

---

*Branch maintained as part of the 10-branch funding architecture. Commits here get cherry-picked to master per the trunk workflow. Branch-level changes do not propagate to `tig-synthesis` unless they are referee-ready.*
