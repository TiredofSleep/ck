# STATUS — funding/civilization-coherence

**As of:** 2026-04-20
**Next review:** when Phase 1 integration + A1 simulator documentation is drafted OR Brayden requests a status check.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Branch state

- Branch seeded: 2026-04-20
- Target folder: `Gen13/targets/funding_civilization_coherence/`
- Files: README, FUNDERS, ARTIFACTS, PITCH_DRAFT, LIMITATIONS, STATUS (this file)
- Rigor base: `tig-synthesis` HEAD

## Readiness checklist

### Content (this branch)
- [x] README with strict-scope framing
- [x] FUNDERS.md with SFI primary + NSF SBE DISES, Templeton, Schmidt, Allen
- [x] ARTIFACTS.md with runnable simulators + authoring tasks A1–A4
- [x] PITCH_DRAFT.md with SFI working-group + DISES + Templeton parallel skeletons
- [x] LIMITATIONS.md with 13 honest-scope items and failure-mode table
- [x] STATUS.md (this file)

### Integration (Phase 1 gating)
- [ ] Verify TIME-FOR-HELP-AND-SCRUTINY repo cloned in `_brayden_repos/`
- [ ] Copy tig_civilization_v5.py and v7.py into `docs/archive_civilization/` with provenance
- [ ] Copy related architectural context (subset of the 10,836 LOC repo) with CONJECTURAL/STRUCTURAL/PROVED flags preserved
- [ ] Run both simulators on R16, confirm execution, record output format

### Authoring (Phase 1 deliverables)
- [ ] **A1**: Simulator documentation (10–15 pp)
- [ ] **A2**: Empirical-fit specification with pre-registration (8–12 pp)
- [ ] **A3**: Literature positioning (5–8 pp)
- [ ] **A4**: Framing cleanup — consciousness-anchored language removed from thread-facing materials

### Pre-pitch work
- [ ] SFI affiliate or academic co-PI engaged
- [ ] If NSF DISES path: academic co-PI identified
- [ ] If Templeton path: LOI submitted
- [ ] Brayden reviews + edits PITCH_DRAFT

### Thread framing-to-send
- [ ] Dataset chosen (V-Dem vs Seshat vs WVS vs ANES vs Pew)
- [ ] Pre-registration of empirical-fit metric submitted (OSF or similar)
- [ ] Brayden confirms SFI vs DISES vs Templeton as first funder
- [ ] Brayden sends

## Dependencies / blockers

- **Blocker 1**: Phase 1 A1 simulator documentation. Requires line-by-line reading of tig_civilization_v5.py and v7.py.
- **Blocker 2**: A2 empirical-fit pre-registration. Requires choosing dataset and fixing metric.
- **Blocker 3**: A4 framing cleanup. Mandatory before any funder sees materials.
- **Blocker 4** (soft): academic collaborator or SFI affiliate. Not strictly required for Templeton LOI but preferred.

## Recent activity

| Date | Event |
|---|---|
| 2026-04-20 | Branch seeded from `tig-synthesis`; target folder + 6 files committed |

## Cross-references

- Plan: `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`
- External repo: `github.com/TiredofSleep/TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT`
- Sibling: `funding/self-healing` (mid-scale single-system version of dual-lattice); `funding/tig-unity` (infrastructure-scale); `funding/tig-snowflake` (security-specific)
- V20 doc (for framing-cleanup reference, not for funder use as-is): commit `ed8ef620` per `JAN2026_RECOVERY_MANIFEST.md`
- Trunk story: `MASTER_TRUNK_STORY_2026_04_19.md` (on master)

---

*Update freely on this branch. Changes here do NOT require master cherry-pick unless they materially change ARTIFACTS or FUNDERS inventories.*
