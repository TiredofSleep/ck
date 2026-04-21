# STATUS — funding/first-g-crypto

**As of:** 2026-04-20
**Next review:** when Phase 1 literature-embedding is drafted OR Brayden requests a status check.

---

## Branch state

- Branch seeded: 2026-04-20
- Target folder: `Gen13/targets/funding_first_g_crypto/`
- Files: README, FUNDERS, ARTIFACTS, PITCH_DRAFT, LIMITATIONS, STATUS (this file)
- Rigor base: `tig-synthesis` HEAD

## Readiness checklist

### Content (this branch)
- [x] README with proved-theorem core summary + open question
- [x] FUNDERS.md with NSA MSP primary + NSF AF, Simons, academic partnerships, foundations
- [x] ARTIFACTS.md with runnable proof scripts + mathematical source inventory
- [x] PITCH_DRAFT.md with NSA MSP + NSF AF parallel skeletons, Phase 1/2/3 structure
- [x] LIMITATIONS.md with eleven honest-scope items + verdict framing
- [x] STATUS.md (this file)

### Pre-pitch work (Phase 1 readiness)
- [ ] Run all four proof scripts, record outputs in a reproduction log
- [ ] Exact LOC / file paths confirmed in ARTIFACTS.md
- [ ] Luther G6 writeup located in `old/Gen10/`, provenance confirmed
- [ ] Q10 / Q11 / Q17_5D_RIGOROUS filenames confirmed
- [ ] Sprint 35 theorem statement re-read, matches ARTIFACTS.md summary
- [ ] **Phase 1 literature-embedding report drafted** (the gating artifact)
- [ ] External cryptographer informal review (at least one academic reads the draft)
- [ ] Brayden reviews + edits PITCH_DRAFT

### Pitch-to-send
- [ ] Brayden confirms NSA MSP vs NSF AF as first funder
- [ ] Academic co-PI identified if NSF AF path taken
- [ ] License framing discussed explicitly
- [ ] Brayden sends

## Dependencies / blockers

- **Blocker 1**: Phase 1 literature-embedding report. This is the single largest gap between current state and pitch-ready. 15–25 pages, arXiv-preprint quality.
- **Blocker 2**: External cryptographer informal opinion. Even 2–3 email paragraphs from Boneh, Micciancio, or a similar figure dramatically strengthens the pitch and surfaces technical weaknesses before reviewers do.
- **Blocker 3**: Luther credit framing. G6 is part of the proved core; the wording must cite Luther's prior work cleanly without implying ongoing collaboration.
- **Blocker 4 (conditional)**: academic co-PI if NSF AF is chosen. Not needed for NSA MSP direct submission.

None of these block the branch existing; the branch serves as a permanent container for the cryptography track. Blocker 1 specifically gates any funder contact.

## Recent activity

| Date | Event |
|---|---|
| 2026-04-20 | Branch seeded from `tig-synthesis`; target folder + 6 files committed |

## Cross-references

- Plan: `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`
- Sprint 35 source: `Gen12/targets/clay/papers/sprint35_first_g_event_2026_04_17/`
- Q-series source: `old/Gen10/papers/` (Q10, Q11, Q17_5D_RIGOROUS)
- Luther spectral layer: `old/Gen10/` Luther archive
- Proof scripts: `papers/proof_first_g_law.py`, `papers/proof_d25_loop_closure.py`, `papers/proof_clay_rotation.py`, `Gen12/.../proof_sigma_rate.py`
- Trunk story: `MASTER_TRUNK_STORY_2026_04_19.md` (on master)

---

*Update freely on this branch. Changes here do NOT require master cherry-pick unless they materially change ARTIFACTS or FUNDERS inventories.*
