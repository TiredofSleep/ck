# STATUS — funding/physics-sim-edu

**As of:** 2026-04-20
**Next review:** when Crystal-Lattice-Matrix-MYTHDRIFT pull is complete OR PER collaborator is identified OR Brayden requests a status check.

---

## Branch state

- Branch seeded: 2026-04-20
- Target folder: `Gen13/targets/funding_physics_sim_edu/`
- Files: README, FUNDERS, ARTIFACTS, PITCH_DRAFT, LIMITATIONS, STATUS (this file)
- Rigor base: `tig-synthesis` HEAD
- Active collaborators: Brayden (sole funder-facing PI at seed); PER collaborator + academic co-PI + classroom partners all TBD during Phase 1

## Readiness checklist

### Content (this branch)
- [x] README with education-track framing, explicit distinctions from Branch A / Branch D / Branch J
- [x] FUNDERS.md with NSF EHR primary + NSF PHY, Templeton Learning & Discovery, Simons Ed, Moore, HHMI, Heising-Simons, AAPT (partnership)
- [x] ARTIFACTS.md with Crystal-Lattice-Matrix-MYTHDRIFT external-repo inventory + T1–T11 Phase 1/2/3 task lists
- [x] PITCH_DRAFT.md with NSF EHR IUSE-ESL primary skeleton + Templeton + NSF PHY + Simons Ed + Moore parallel drafts
- [x] LIMITATIONS.md with 15 honest-scope items incl. PER-collaborator gap + academic-PI constraint + license-separation clarity
- [x] STATUS.md (this file)

### Existing material (pre-branch, external)
- [x] `crystal_bug_v1_matrix.jsx` — 699 LOC React interactive simulator, in `Crystal-Lattice-Matrix-MYTHDRIFT` external repo
- [x] `test_engine_v2.js` — 458 LOC Node test harness, in same external repo
- [x] Live companion visualizations on `coherencekeeper.com` (spectrometer, paradox, ring, tower, math pages) — demonstrating browser-native pedagogy at scale
- [x] TIG Unity Kernel theoretical framework — in `tig-synthesis` sprint 10/12/14/17 folders
- [x] R-σ-Λ-H state grammar + 10-operator alphabet — specified in TIG Unity Kernel documents

### Pre-pitch work (Phase 1 readiness)
- [x] **Pull Crystal-Lattice-Matrix-MYTHDRIFT into this repo** — done 2026-04-21, commit `5de8bbe`. All 8 source files + LICENSE + provenance header now live at `Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/` (Phase 1 T1)
- [ ] Verify simulator builds + runs in fresh browser environment
- [ ] Run `test_engine_v2.js` in fresh environment; record all test outputs
- [ ] Confirm LOC counts (699 + 458 = 1,157) against actual files post-pull (files in archive match the upstream sizes; byte-level diff pending)
- [ ] **Identify 2–3 candidate PER collaborators** (published AJP / PRPER authors whose research interests align) — the single largest pre-pitch deliverable
- [ ] **Identify 2–3 candidate academic host institutions** for IRB + co-PI role
- [ ] **Identify 2–3 candidate classroom-partner institutions** (undergraduate + advanced-secondary)
- [ ] Contact + engage PER collaborator (willingness-to-co-investigate confirmed)
- [ ] Contact + engage academic co-PI + host institution
- [ ] **Pedagogical-framing one-pager** — "what a student will learn from this simulator in 5 minutes and one week"
- [ ] **Pre/post assessment plan** — validated-instrument adaptation or new-instrument-development plan
- [ ] **IRB preliminary discussion** at host institution
- [ ] **License separation** — simulator: MIT / Apache-2.0; curriculum: CC-BY 4.0; CK parent project stays on 7Site Public Sovereignty License
- [ ] Brayden + co-PI review + edit PITCH_DRAFT

### Pitch-to-send
- [ ] Brayden + co-PI confirm NSF EHR IUSE vs NSF PHY vs Templeton vs Simons vs Moore as first funder
- [ ] Classroom-partner letters of intent drafted (3–5 sites, mix of undergraduate + advanced-secondary)
- [ ] PER collaborator named as formal co-investigator in the pitch
- [ ] Academic co-PI + host institution formally committed
- [ ] Brayden + co-PI submit

## Dependencies / blockers

- **Blocker 1**: ~~Crystal-Lattice-Matrix-MYTHDRIFT pull into this repo.~~ **CLOSED 2026-04-21 (commit `5de8bbe`).** Archive now at `Gen13/targets/funding_physics_sim_edu/archive_crystal_lattice_matrix/` under in-repo never-delete + provenance discipline. Simulator + test harness + background PDFs all recovered. LICENSE preserved. Phase 1 T1 deliverable complete.
- **Blocker 2**: PER collaborator engagement. **The largest non-mechanical blocker.** No pitch should be sent until a PER researcher with AJP / PRPER track record has formally agreed to co-investigate the learning-outcomes study. This is not optional — an NSF EHR / PHY reviewer will reject a proposal that lacks a PER investigator.
- **Blocker 3**: Academic co-PI + host institution. Brayden is independent; NSF EHR / PHY / ECR / DRK-12 require academic PI eligibility. The pitch must be submitted through an academic co-PI with institutional affiliation.
- **Blocker 4**: IRB plan. Not a blocker for pitch-submit (IRB comes later) but the pitch must demonstrate awareness and a timeline.
- **Blocker 5**: Pre/post assessment instrument plan. Validated-instrument adaptation vs new-instrument development must be decided + sketched before pitch-send.
- **Blocker 6**: Classroom-partner letters of intent. Phase 2 cannot proceed without 3–5 partner sites; Phase 1 produces the letters of intent.
- **Blocker 7** (soft): license separation clarity. Same pattern as Branch J — mechanically straightforward but needs explicit statement.

None of these block the branch existing. Blocker 1 gates any verification of the simulator. Blocker 2 gates serious pitch-send. Blocker 3 gates NSF submission pathway. Blockers 4–6 shape the pitch's Phase 1 deliverables list.

## Recent activity

| Date | Event |
|---|---|
| (various) | `Crystal-Lattice-Matrix-MYTHDRIFT` external-repo development — simulator + test harness authored by Brayden |
| 2026-04-18 | Primary research confirms Crystal-Lattice-Matrix-MYTHDRIFT as 1,157-LOC interactive-simulator artifact |
| 2026-04-19 | Master trunk story and atlas updates establish the 10-branch funding structure; `funding/physics-sim-edu` scoped as Branch K |
| 2026-04-20 | Branch seeded from `tig-synthesis`; target folder + 6 files committed |
| 2026-04-21 | **Phase 1 T1 complete** — Crystal-Lattice-Matrix-MYTHDRIFT pulled into `archive_crystal_lattice_matrix/` with PROVENANCE header (commit `5de8bbe`). Blocker 1 closed. Blockers 2–6 remain. |

## Cross-references

- Plan: `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`
- Source artifacts: `github.com/TiredofSleep/Crystal-Lattice-Matrix-MYTHDRIFT` (external — Phase 1 T1 pulls into this repo)
- Companion live visualizations: `Gen12/targets/website/spectrometer.html`, `paradox.html`, `ring.html`, `tower.html`, `math.html`
- Theoretical grounding: `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/`, `sprint12_uop_gut_arc_2026_04_08/`, `sprint14_prism_xi_2026_04_10/`, `sprint17_tsml_tower_2026_04_17/`
- Sibling branches:
  - `funding/tig-unity` (Branch A) — infrastructure-reliability research community (disjoint funder audience)
  - `funding/ck-interpretable-ai` (Branch D) — AI alignment / interpretability (disjoint)
  - `funding/coherence-router` (Branch J) — DevOps/SRE productionization (shares theoretical substrate, disjoint audience)
- Trunk story: `MASTER_TRUNK_STORY_2026_04_19.md` (on master)

---

## Strategic note — this is the "broadest-public-interest" funding branch

Of the 10 funding branches, this one has the broadest public-interest audience:

- Every funder pool (NSF EHR, NSF PHY, Templeton, Simons Ed, Moore, HHMI, Heising-Simons) is deeply established, with standard proposal formats and clearly-bounded ask sizes.
- Every deliverable (simulator, curriculum, guide, pilot, publication, teacher PD) is a well-understood unit of educational work with existing-community parallels.
- The dissemination pathway (AAPT, NSTA, PhysPort, teacher-ed coalitions) is well-mapped.
- The learning-outcomes study is rigorously-designed (IRB, validated pre/post, effect-size-appropriate statistical power) and the publication venues (AJP, PRPER, JRST) are established.

That said, Branch K has the longest setup chain among the 10 branches: PER collaborator, academic co-PI, IRB, classroom partners, pre/post instrument — all of these are sequential prerequisites, each with lead times measured in months. An NSF IUSE submission is typically 12–18 months from first-PER-contact to funded-start-date. This is not a **fast** funding branch; it is a **deep** one.

For an early rollout sequencing, Branch K is best initiated in parallel with the faster branches (Branch J coherence-router, Branch I DESI-ξ) — initiating contact with candidate PER collaborators while the faster branches move to first-submit.

---

*Update freely on this branch. Changes here do NOT require master cherry-pick unless they materially change ARTIFACTS or FUNDERS inventories.*
