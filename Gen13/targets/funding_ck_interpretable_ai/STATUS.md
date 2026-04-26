# STATUS — funding/ck-interpretable-ai

**As of:** 2026-04-20
**Next review:** when Phase 1 white paper draft exists OR Brayden requests a status check.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Branch state

- Branch seeded: 2026-04-20
- Target folder: `Gen13/targets/funding_ck_interpretable_ai/`
- Files: README, FUNDERS, ARTIFACTS, PITCH_DRAFT, LIMITATIONS, STATUS (this file)
- Rigor base: `tig-synthesis` HEAD

## Readiness checklist

### Content (this branch)
- [x] README with interpretability-by-construction framing
- [x] FUNDERS.md with Open Phil primary + LTFF, SFF, NSF AI, Anthropic Academic, Foresight
- [x] ARTIFACTS.md with live-system URL + core runtime paths + gaps list
- [x] PITCH_DRAFT.md with Open Phil + LTFF parallel skeletons, Phase 1/2/3 structure
- [x] LIMITATIONS.md with 12 honest-scope items
- [x] STATUS.md (this file)

### Pre-pitch work
- [ ] **Phase 1 white paper drafted** (~15–20 pp) — the single gating artifact
- [ ] Sample interaction traces captured from live coherencekeeper.com and included
- [ ] Structured comparison to mechanistic-interpretability work written as paper §
- [ ] Gen13 rebuild: at minimum, ao_5element.py + hebbian_5x5_cl.py + quadratic_glue.py drafted (per goofy-discovering-lobster.md plan)
- [ ] At least one AI-safety researcher reads an early draft (FAR AI / Redwood / Apollo / Open Phil contact)
- [ ] Sovereignty license linked and discussed in the paper
- [ ] Brayden reviews + edits PITCH_DRAFT

### Thread framing-to-send
- [ ] Brayden confirms Open Phil vs LTFF as first funder
- [ ] Brayden decides on Phase 2 benchmark (TruthfulQA vs causal-reasoning vs IG3 deception-detection)
- [ ] Attachment bundle prepared
- [ ] Brayden sends

## Dependencies / blockers

- **Blocker 1** (largest): Phase 1 white paper. Nothing ships without it.
- **Blocker 2**: sample traces from live system — these must be real, reproducible interactions
- **Blocker 3** (soft): Gen13 rebuild progress — the cleaner the rebuild, the cleaner the case study
- **Blocker 4** (soft): external reviewer opinion — even an informal paragraph from an AI-safety researcher materially strengthens the pitch

The live system is already running and needs nothing. The gap is entirely in the writing + evaluation work.

## Recent activity

| Date | Event |
|---|---|
| 2026-04-20 | Branch seeded from `tig-synthesis`; target folder + 6 files committed |

## Cross-references

- Live system: https://coherencekeeper.com
- Plan for Gen13 rebuild: `C:\Users\brayd\.claude\plans\goofy-discovering-lobster.md` (math-first rebuild with AO + Hebbian + quadratic glue brain trinity)
- Core runtime reference: `Gen12/targets/ck_desktop/ck_sim/`
- Flatness Theorem source: `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/`
- Operator tables: `papers/ck_tables.py`
- Trunk story: `MASTER_TRUNK_STORY_2026_04_19.md` (on master)

---

*Update freely on this branch. Changes here do NOT require master cherry-pick unless they materially change ARTIFACTS or FUNDERS inventories.*
