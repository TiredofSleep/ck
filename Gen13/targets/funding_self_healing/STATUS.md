# STATUS — funding/self-healing

**As of:** 2026-04-20
**Next review:** when Phase 1 integration completes OR Brayden requests a status check.

---

## Branch state

- Branch seeded: 2026-04-20
- Target folder: `Gen13/targets/funding_self_healing/`
- Files: README, FUNDERS, ARTIFACTS, PITCH_DRAFT, LIMITATIONS, STATUS (this file)
- Rigor base: `tig-synthesis` HEAD

## Readiness checklist

### Content (this branch)
- [x] README with track framing + relationship to Branches A and B
- [x] FUNDERS.md with AFRL primary + NASA JPL NIAC, ONR, NSF CISE RI, DARPA
- [x] ARTIFACTS.md with external repo integration + A1–A4 authoring tasks
- [x] PITCH_DRAFT.md with AFRL + NASA JPL NIAC + ONR parallel skeletons
- [x] LIMITATIONS.md with 13 honest-scope items incl safety criticality
- [x] STATUS.md (this file)

### Integration (Phase 1 gating)
- [ ] Verify `Dual-Lattice-Self-Healing` external repo is cloned into `_brayden_repos/`
- [ ] Copy verbatim into `docs/archive_dual_lattice/` with provenance header
- [ ] Mark any superseded content `[HISTORICAL]` in place

### Authoring (Phase 1 deliverables)
- [ ] **A1**: Architectural writeup (15–20 pp)
- [ ] **A2**: Literature-positioning section (5–8 pp, includes NASA MDS, FDI, FDIR, soft-robotics, fault-tolerant distributed-systems classics)
- [ ] **A3**: Target-domain specification (3–5 pp) — chooses Phase 2 benchmark
- [ ] **A4**: Safety envelope specification (3–5 pp)

### Pre-pitch work
- [ ] Autonomous-systems specialist has read an early draft
- [ ] If NASA JPL NIAC path: spacecraft fault-management subject-matter expert consulted
- [ ] If AFRL path: autonomy-capability program manager identified
- [ ] Brayden reviews + edits PITCH_DRAFT

### Pitch-to-send
- [ ] Brayden confirms AFRL vs NASA JPL NIAC vs ONR as first funder
- [ ] Attachment bundle assembled (A1–A4 + integrated archive)
- [ ] Brayden sends

## Dependencies / blockers

- **Blocker 1**: Phase 1 integration + writeup. A1 is the single largest gap.
- **Blocker 2**: Target-domain selection (A3). Without a named domain, every funder conversation stalls.
- **Blocker 3**: Safety envelope (A4). No autonomous-systems funder will engage without this.
- **Blocker 4**: Academic or industrial collaborator (soft blocker, hard for NSF CISE RI path specifically)

## Recent activity

| Date | Event |
|---|---|
| 2026-04-20 | Branch seeded from `tig-synthesis`; target folder + 6 files committed |

## Cross-references

- Plan: `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`
- External repo: `github.com/TiredofSleep/Dual-Lattice-Self-Healing` (cloned to `_brayden_repos/`)
- Sibling branches: `funding/tig-unity` (reliability), `funding/tig-snowflake` (detection), `funding/civilization-coherence` (large-scale)
- Coherence gate reference: `Gen12/targets/ck_desktop/ck_sim/being/ck_coherence_gate.py`
- Operator tables: `papers/ck_tables.py`
- Trunk story: `MASTER_TRUNK_STORY_2026_04_19.md` (on master)

---

*Update freely on this branch. Changes here do NOT require master cherry-pick unless they materially change ARTIFACTS or FUNDERS inventories.*
