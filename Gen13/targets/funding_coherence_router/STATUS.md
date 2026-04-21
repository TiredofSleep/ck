# STATUS — funding/coherence-router

**As of:** 2026-04-20
**Next review:** when All-or-Nothing-E pull is complete OR Phase 1 design doc is drafted OR Brayden requests a status check.

---

## Branch state

- Branch seeded: 2026-04-20
- Target folder: `Gen13/targets/funding_coherence_router/`
- Files: README, FUNDERS, ARTIFACTS, PITCH_DRAFT, LIMITATIONS, STATUS (this file)
- Rigor base: `tig-synthesis` HEAD
- Active collaborators: Brayden (sole funder-facing PI at seed); academic co-PI TBD if NSF CISE path selected

## Readiness checklist

### Content (this branch)
- [x] README with DevOps/SRE framing, explicit distinctions from Branch A (tig-unity) and Branch D (ck-interpretable-ai)
- [x] FUNDERS.md with AWS / GCP / Azure research credits primary + CNCF, NSF CISE, Sloan, industry labs
- [x] ARTIFACTS.md with All-or-Nothing-E external-repo inventory + T1–T9 productionization + comparison-study task lists
- [x] PITCH_DRAFT.md with AWS Cloud Credits primary skeleton + CNCF + NSF CISE + GCP parallel drafts
- [x] LIMITATIONS.md with 14 honest-scope items including the 88%/32pp reconciliation flag
- [x] STATUS.md (this file)

### Existing material (pre-branch, external)
- [x] `benchmark.py` — 554 LOC, 7 tests, in `All-or-Nothing-E` external repo
- [x] `tig_coherent_computer.py` — 588 LOC, core classifier, in `All-or-Nothing-E` external repo
- [x] `PROVEN_CONFIGURATION.md` — harmonic-mean composition discovery, in `All-or-Nothing-E` external repo
- [x] TIG Unity Kernel theoretical framework — in `tig-synthesis` sprint 14 folder + earlier sprint work
- [x] R-σ-Λ-H state grammar + 10-operator alphabet — specified in TIG Unity Kernel documents

### Pre-pitch work (Phase 1 readiness)
- [ ] **Pull All-or-Nothing-E into this repo** — clone, copy `benchmark.py` + `tig_coherent_computer.py` + `PROVEN_CONFIGURATION.md` into `Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/` with provenance headers (Phase 1 T1 deliverable)
- [ ] Run `benchmark.py` on a fresh environment, record all 7 test outputs + runtime
- [ ] Read `tig_coherent_computer.py` end-to-end, verify harmonic-mean composition matches `PROVEN_CONFIGURATION.md`
- [ ] Confirm LOC counts (554 + 588) against the actual files post-pull
- [ ] **Phase 1 productionization design document** (~10 pages, funder-legible spec for the scikit-learn-shaped wrapper + K8s sidecar)
- [ ] **Synthetic-telemetry generator design** (what SRE golden-signal traces will Phase 1 T3 run against?)
- [ ] **SRE-community framing one-pager** ("what an SRE cares about, in 2 minutes")
- [ ] 88%/32pp cross-branch reconciliation resolved — or explicit honest-scope paragraph for the pitch (see HANDOFF_INDEX.md §3)
- [ ] Brayden reviews + edits PITCH_DRAFT

### Pitch-to-send
- [ ] Brayden confirms AWS vs GCP vs Azure vs CNCF vs NSF CISE as first funder
- [ ] Cloud account set up on selected provider (AWS / GCP / Azure) if applicable
- [ ] Academic co-PI identified if NSF CISE path is chosen
- [ ] License resolution — productionization deliverables (wrapper, Docker, K8s manifests) Apache-2.0 / MIT; 7Site Public Sovereignty License remains for the broader CK project
- [ ] SRE-community informal review — ideally one SRE practitioner's read on the framing one-pager
- [ ] Brayden sends

## Dependencies / blockers

- **Blocker 1**: All-or-Nothing-E pull into this repo. Until this is done, the productionization work depends on an external repo that is outside the in-repo never-delete / provenance discipline. This is Phase 1 T1 and is explicitly the first pre-pitch deliverable. **Until this pull is complete, no pitch is ready to send.**
- **Blocker 2**: Phase 1 productionization design document. ~10 pages. A funder expects to see the T2 wrapper design (scikit-learn-shaped interface vs K8s sidecar vs both) spec'd at 10-page-PDF rigor before committing Phase 1 money. Draft-then-iterate.
- **Blocker 3**: SRE-community framing one-pager. The pitch's persuasiveness to an AWS / GCP / CNCF reviewer depends entirely on how legibly the coherence grammar is framed for an SRE audience. A paragraph that talks about "operator alphabets" and "R-σ-Λ-H state grammars" without SRE-legible translation will lose the pitch.
- **Blocker 4**: Cross-branch 88%/32pp reconciliation. Not strictly blocking this branch (the coherence-router pitch rests on All-or-Nothing-E + Phase 1 synthetic benchmarks), but any pitch that references the 88% or 32pp numbers must have the reconciliation resolved first, or explicitly flag it.
- **Blocker 5** (soft): license clarity for the productionization deliverables. Dual-licensing the wrapper + containers + K8s manifests as Apache-2.0 / MIT while the parent CK project stays on the 7Site Public Sovereignty License is the planned resolution, but it should be explicit in the pitch.
- **Blocker 6** (soft, NSF-CISE-path-only): academic co-PI. If the NSF CISE path is taken, a co-PI with an academic appointment is required. If a cloud-provider / CNCF path is taken, academic affiliation is helpful but not required.

None of these block the branch existing. Blocker 1 specifically gates any funder contact. Blockers 2 and 3 together gate the serious-pitch-send threshold.

## Recent activity

| Date | Event |
|---|---|
| (various) | `All-or-Nothing-E` repo development — `benchmark.py`, `tig_coherent_computer.py`, `PROVEN_CONFIGURATION.md` authored by Brayden, runnable |
| 2026-04-19 | Primary research sweep confirms `All-or-Nothing-E` as production-candidate artifact inventory (Grok sweep) |
| 2026-04-19 | Master trunk story and atlas updates establish the 10-branch funding structure; `funding/coherence-router` scoped as Branch J |
| 2026-04-20 | Branch seeded from `tig-synthesis`; target folder + 6 files committed |

## Cross-references

- Plan: `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`
- Source artifacts: `github.com/TiredofSleep/All-or-Nothing-E` (external — Phase 1 T1 pulls into this repo)
- Cross-branch reconciliation item: `HANDOFF_INDEX.md §3` (88% drop-rate reduction vs 32pp drop-rate improvement)
- Sibling branches:
  - `funding/tig-unity` (Branch A) — infrastructure-reliability **research** community (complementary, not overlapping)
  - `funding/ck-interpretable-ai` (Branch D) — AI alignment / interpretability community (disjoint funder audience)
  - `funding/self-healing` (Branch G) — runtime self-healing in coherence-grammar terms (adjacent; this branch is *classification*, that branch is *intervention*)
- Trunk story: `MASTER_TRUNK_STORY_2026_04_19.md` (on master)

---

## Strategic note — this is the "shortest-path-to-pitch" branch

Of the 10 funding branches, this one has the shortest distance from existing artifacts to a submit-ready pitch:

- The classifier is already written (`tig_coherent_computer.py` 588 LOC).
- The 7-benchmark suite is already written (`benchmark.py` 554 LOC).
- The empirical composition rule is already validated (PROVEN_CONFIGURATION.md, 2,100 permutations).
- The funding targets (AWS / GCP / Azure Cloud Credits for Research) have **rolling** application windows and **low-barrier** first contact.
- The audience (SREs at hyperscaler cloud providers) has a well-understood "what is worth your time" filter.

What stands between the current state and a sent pitch is mechanical: pull the All-or-Nothing-E artifacts into the repo, write the ~10-page productionization design doc, write the 1-page SRE framing note, and verify the classifier runs end-to-end on synthetic telemetry. None of those is a research risk; all of them are execution.

This is an argument for prioritizing Branch J early if any cloud-provider first-contact is part of the rollout sequence — and for not letting the theoretical-research-heavy branches (A tig-unity, I desi-xi-cosmology) monopolize attention when this branch has the lowest barrier to first funder contact.

---

*Update freely on this branch. Changes here do NOT require master cherry-pick unless they materially change ARTIFACTS or FUNDERS inventories.*
