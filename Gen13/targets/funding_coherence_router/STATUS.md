# STATUS — funding/coherence-router

**As of:** 2026-04-20
**Next review:** when All-or-Nothing-E pull is complete OR Phase 1 design doc is drafted OR Brayden requests a status check.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Branch state

- Branch seeded: 2026-04-20
- Target folder: `Gen13/targets/funding_coherence_router/`
- Files: README, FUNDERS, ARTIFACTS, PITCH_DRAFT, LIMITATIONS, STATUS (this file)
- Rigor base: `tig-synthesis` HEAD
- Active collaborators: Brayden (sole thread-facing PI at seed); academic co-PI TBD if NSF CISE path selected

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
- [x] **Pull All-or-Nothing-E into this repo** — done 2026-04-21, commit `60ecd38`. 45 files (text + binary provenance) under `Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/`, including `benchmark.py` (~554 LOC), `tig_coherent_computer.py` (~588 LOC), `PROVEN_CONFIGURATION.md`, `THEORY.md`, `OPERATOR_SPEC.md`, full test harness, paper drafts (Phase 1 T1 complete)
- [ ] Run `benchmark.py` on a fresh environment, record all 7 test outputs + runtime
- [ ] Read `tig_coherent_computer.py` end-to-end, verify harmonic-mean composition matches `PROVEN_CONFIGURATION.md`
- [ ] Confirm LOC counts (554 + 588) against the actual files post-pull
- [ ] **Phase 1 productionization design document** (~10 pages, funder-legible spec for the scikit-learn-shaped wrapper + K8s sidecar)
- [ ] **Synthetic-telemetry generator design** (what SRE golden-signal traces will Phase 1 T3 run against?)
- [ ] **SRE-community framing one-pager** ("what an SRE cares about, in 2 minutes")
- [x] 88%/32pp cross-branch reconciliation — **partially resolved.** 36.4→4.2% drop rate = both 32.2pp absolute and 88.5% relative; same number, two units. See `Atlas/HANDOFF_3_2_BENCHMARK_RECONCILIATION.md` (2026-04-21). **GAP**: the discrete-event simulator that produced the P99 / recovery-time / resource-utilization / cascade-failure metrics has NOT been located; `benchmark.py` measures lattice coherence not cluster load-balancing. Pitch must constrain to drop-rate only until the source simulator is found, OR mark expanded metrics `[PENDING §3.2 GAP]`.
- [ ] Brayden reviews + edits PITCH_DRAFT

### Thread framing-to-send
- [ ] Brayden confirms AWS vs GCP vs Azure vs CNCF vs NSF CISE as first funder
- [ ] Cloud account set up on selected provider (AWS / GCP / Azure) if applicable
- [ ] Academic co-PI identified if NSF CISE path is chosen
- [ ] License resolution — productionization deliverables (wrapper, Docker, K8s manifests) Apache-2.0 / MIT; 7Site Public Sovereignty License remains for the broader CK project
- [ ] SRE-community informal review — ideally one SRE practitioner's read on the framing one-pager
- [ ] Brayden sends

## Dependencies / blockers

- **Blocker 1**: ~~All-or-Nothing-E pull into this repo.~~ **CLOSED 2026-04-21 (commit `60ecd38`).** Archive now at `Gen13/targets/funding_coherence_router/archive_all_or_nothing_e/` under in-repo never-delete + provenance discipline. Phase 1 T1 complete. Pitch send-readiness no longer gated on this item; reopened gating responsibilities belong to Blockers 2/3 (design doc + SRE one-pager) and the §3.2-GAP clarification.
- **Blocker 2**: Phase 1 productionization design document. ~10 pages. A funder expects to see the T2 wrapper design (scikit-learn-shaped interface vs K8s sidecar vs both) spec'd at 10-page-PDF rigor before committing Phase 1 money. Draft-then-iterate.
- **Blocker 3**: SRE-community framing one-pager. The pitch's persuasiveness to an AWS / GCP / CNCF reviewer depends entirely on how legibly the coherence grammar is framed for an SRE audience. A paragraph that talks about "operator alphabets" and "R-σ-Λ-H state grammars" without SRE-legible translation will lose the pitch.
- **Blocker 4**: Cross-branch 88%/32pp reconciliation. **Partially resolved 2026-04-21** — the two figures are the same number (36.4→4.2 drop rate, 32.2pp absolute = 88.5% relative). The pitch may quote the drop-rate freely with both units. **REMAINING GAP**: the expanded P99 / recovery-time / resource / cascade-failure metrics cited in HANDOFF §3.2 are NOT reproducible from the archived `benchmark.py` as of today's sweep — that file measures lattice coherence, not distributed-system load-balancing. Pitch either (a) constrains claims to drop-rate only, or (b) tags expanded metrics `[PENDING §3.2 GAP]`. See `Atlas/HANDOFF_3_2_BENCHMARK_RECONCILIATION.md`.
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
| 2026-04-21 | **Phase 1 T1 complete** — All-or-Nothing-E pulled into `archive_all_or_nothing_e/` (commit `60ecd38`). Blocker 1 CLOSED. HANDOFF §3.2 partially reconciled (drop-rate numbers are two units of one number); §3.2 GAP remains on the discrete-event simulator source. |

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
