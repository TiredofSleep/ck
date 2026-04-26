# STATUS — funding/tig-unity

**As of:** 2026-04-19
**Next review:** whenever a reproduction, funder reply, or Brayden edit lands.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Branch state

- Branch seeded: 2026-04-19
- Target folder: `Gen13/targets/funding_tig_unity/`
- Files: README, FUNDERS, ARTIFACTS, PITCH_DRAFT, LIMITATIONS, STATUS (this file)
- Rigor base: `tig-synthesis` HEAD as of seeding

## Readiness checklist

### Content
- [x] README with thread-facing pitch paragraph
- [x] FUNDERS.md with 5 primary + 2 secondary candidates
- [x] ARTIFACTS.md with exact file paths and line counts
- [x] PITCH_DRAFT.md skeleton
- [x] LIMITATIONS.md with honest scope
- [x] STATUS.md (this file)

### Recovery (before first funder email)
- [ ] Copy `benchmark.py` from `All-or-Nothing-E` into `docs/archive_recovered/`
- [ ] Copy `tig_coherent_computer.py` similarly
- [ ] Copy `docs/COMPUTE.md` + `docs/VALIDATION.md` similarly
- [ ] Run `python benchmark.py` on current machine; record output
- [ ] Reconcile 88% / 32pp discrepancy (handoff §3 Issue 2)
- [ ] Document `coherence_router` location (standalone or refactored)

### Pre-pitch work
- [ ] Brayden reviews + edits PITCH_DRAFT
- [ ] Brayden selects one of the 5 primary funders to approach first
- [ ] Brayden confirms license framing (non-commercial OK for funder?)
- [ ] Brayden decides on academic co-PI (yes / no / let funder suggest)

### Thread framing-to-send
- [ ] Final funder-specific customization (addressee, scope, ask size)
- [ ] Attachment bundle prepared (ARTIFACTS references + reproduction log)
- [ ] Brayden sends

## Dependencies / blockers

- **Blocker 1:** external repo recovery (`All-or-Nothing-E` → `docs/archive_recovered/`). Not done in this branch's seed commit.
- **Blocker 2:** reproduction of benchmark numbers on fresh environment.
- **Blocker 3:** Brayden's selection of which funder to approach first.

None of these block the branch existing; all three block sending a pitch.

## Recent activity

| Date | Event |
|---|---|
| 2026-04-19 | Branch seeded from `tig-synthesis`; target folder + 6 files committed |

## Cross-references

- Plan: `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`
- Inventory: `Atlas/FUNDING_BRANCHES_PLAN_2026_04_19.md`
- Handoff: `docs/handoffs/claudecode_handoff_2026_04_20/`
- Trunk story: `MASTER_TRUNK_STORY_2026_04_19.md` (on master)

---

*Update freely on this branch. Changes here do NOT require master cherry-pick unless they materially change the ARTIFACTS or FUNDERS inventories.*
