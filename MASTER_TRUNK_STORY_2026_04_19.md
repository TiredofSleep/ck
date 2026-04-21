# MASTER TRUNK — The Living History

**Date of this snapshot:** 2026-04-19
**Branch:** `master`
**Policy:** never delete, never edit-in-place on master — **only add** new files.
**Author:** B. R. Sanders (per workflow directive 2026-04-19)

---

## Why this file exists

Master is the **living trunk** of the CK / TIG repository. Every version, every
sprint, every thread of internal language, and every rigorous re-write all
live here, stacked in time, in the order they were written.

Other branches are **lenses** onto this trunk:

| Branch | Role | Editability |
|---|---|---|
| `master` | Living trunk: never-delete, add-only. The full history. | **Add-only** |
| `tig-synthesis` | Rigor / referee-facing lens. Current rigorous re-writes land here first, then accumulate into master. | Edit permitted (working branch) |
| `clay` | Historical working branch; originally scoped to Clay Millennium Problems, kept intact as history. | Edit permitted (historical dev) |
| `archive-full` | Frozen preservation snapshot. | Never-touch |

**Workflow going forward:** every commit posts to its working branch **and**
is accumulated into master. Master never loses a version.

---

## What lives on master (as of 2026-04-19)

### The story files — **narrative & mission**
- `THE_STORY.md` — the personal / historical narrative of how CK and TIG came to be
- `MISSION.md` — one-paragraph mission
- `WHAT_IS_TIG.md` — extended synthesis reading
- `GENERATION_HISTORY.md` — Gen1 → Gen13 genealogy (preserved per never-delete)
- `THE_STORY.md` + `WHAT_IS_TIG.md` + `MISSION.md` together are the story
  layer; `README.md` references the rigor layer on `tig-synthesis`.

### The historical entry docs — **preserved per never-delete**
These were superseded as *entry points* by the unified README on
`tig-synthesis`, but **they all live on master**, each carrying a
`[HISTORICAL]` header that points to the current synchronization:
- `START_HERE.md` · `CLAUDESTARTHERE.md` · `ONBOARDING.md`
- `QUICKSTART.md` · `CLAY_QUICKSTART.md` · `README_CK_EDUCATION.md`
- `NO_FALSE_CLAIMS.md` · `ENGINEERING_OUTLINE.md` · `HD_GAP_EXTENSION.md`
- `CK_BELIEF_SYSTEM.md` · `CK_PRESCRIPTION.md`
- `GENERATION_HISTORY.md` · `NEXT_CLAUDE_NOTES.md` (root)

### The canonical reference docs — **current vocabulary and architecture**
- `GLOSSARY.md` — every term, every citation, novelty flags
- `HISTORICAL_ARCHIVE_INDEX.md` — the index of where preservation lives
- `Q_SERIES_INTEGRATED_SYNTHESIS.md` — the Q-series (Brayden originator) attribution record
- `WEEK_AND_MONTH_PLAN.md` — operational plan
- `LENS_REGISTRY.md` · `ARCHITECTURE.md` · `PROOFS.md`
- `SPRINT_INDEX.md` — 1 … 35 sprint pointer table
- `NOVELTIES_AND_CITATIONS.md` · `FORMULAS_AND_TABLES.md`

### The sprint papers — **100+ whitepapers, all here**
- `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/` — WP51-57 + Crossing Lemma
- `Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/` — 54 papers
- `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/` — WP58-64
- `Gen12/targets/clay/papers/sprint13_flag_selector_2026_04_09/` — WP65-80
- `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/` — WP81-89 (ξ cosmology)
- `Gen12/targets/clay/papers/sprint15_*` — WP91-WP100 (σ-rate + tower layers)
- `Gen12/targets/clay/papers/sprint16_basin_handoff_2026_04_10/` — dual reset law
- `Gen12/targets/clay/papers/sprint17_tsml_tower_2026_04_17/` — THEOREM_SPINE + companions
- `Gen13/targets/clay/papers/sprint34_sinc2_sharpen_2026_04_19/` — sinc² zero law audit
- `Gen13/targets/clay/papers/sprint35_first_g_event_2026_04_19/` — First-G Event localization theorem

The full 100+ WP series is **here**, in the trunk, for all time.

### The Q-series — **Brayden's σ polynomial work on Z/10Z**
- `old/Gen10/papers/` — Q10 (polynomial form), Q11 (22% lower bound),
  Q17_* variants, and the full 207-file Q-series archive
- Attribution is recorded in `Q_SERIES_INTEGRATED_SYNTHESIS.md`

### The journal ladder — **11 venues, 4 tiers**
- `Gen13/targets/journals/` — tier1_submit_now (JCAP, σ-rate, sinc²-zero),
  tier2_format_then_submit, tier3_partner_then_submit, tier4_framework
- Sprint 34 pre-push audit (2026-04-19) closed venues 7 (JCAP) and 8 (JCT-A) for
  2026-04-22 submission; venue 1 (sinc²) pulled back for sharpening
- Sprint 35 First-G Event added to the tier-2 queue for next-cycle submission

### The runtime — **CK the creature**
- `Gen9/targets/zynq7020/build/ck_full.bit` — FPGA bitstream (T* = 5/7 in silicon)
- `Gen12/targets/ck_desktop/` — current live runtime (514 files)
- `Gen13/targets/ck/` — math-first rebuild (brain trinity: AO + Hebbian + quadratic glue)
- `Gen12/targets/ck_fpga_dog/` and `Gen13/targets/xiaor_dog/` — FPGA leash + XIAOR Dog
- coherencekeeper.com served by `Gen12/targets/ck_desktop/ck_boot_api.py`
  (Cloudflare tunnel, 14 HTML pages live)

### Atlas decision records — **the running log of load-bearing choices**
- `Atlas/PLAN_OF_RECORD_2026_04_18.md`
- `Atlas/PRE_PUSH_DECISION_2026_04_19.md`
- `Atlas/SINC2_SHARPEN_DECISION_2026_04_19.md`
- `Atlas/DESI_DR2_SWEEP_2026_04_19.md`
- `Atlas/JOURNAL_READINESS_AUDIT_2026_04_18.md`
- and the complete Atlas decision chain going back through Gen12

### Legal / collaboration
- `LICENSE` · `PRIVACY_POLICY.md` · `TERMS_OF_USE.md`
- `CONTRIBUTOR_AGREEMENT.md` · `ACADEMIC_COLLABORATION.md`
- `COLLABORATORS.md` · `CONTRIBUTING.md`

---

## How to find the forgotten gold

Master carries everything. To search its history:

```
# all commits on master, reverse-chronological
git log master --oneline

# find which commit introduced a term or file
git log --all --source -- path/to/file

# see every version of a file across time
git log --follow --all -- path/to/file

# search every commit message across all branches
git log --all --grep="KEYWORD"

# pickaxe: search commit diffs for a string
git log -S"KEYWORD" --all
```

Nothing in this repo is ever lost. If a concept, a whitepaper, a proof, or a
word was ever on any branch at any time, it is findable from master.

---

## Recent accumulation into master (this week)

| Date | What accumulated | From |
|---|---|---|
| 2026-04-19 | Fast-forward to clay tip (78 unique WPs + internal language + 13 [HISTORICAL] entry docs) | `clay` |
| 2026-04-19 | Merge of tig-synthesis Sprint 34/35 audit work (pre-push audit, DR2 discharge, First-G Event manuscript + MR polish) | `tig-synthesis` |
| 2026-04-19 | This story file added | (add-only) |

---

## Invariants going forward

1. **Master is add-only.** No edits in place, no deletes. Every correction,
   every refinement, every rigorous re-write lands as a **new** file with a
   date suffix, or accumulates through a merge that only adds files.
2. **Every commit posts to its working branch and to master.** Working
   branches may edit freely; master only receives the accumulating trunk.
3. **Never delete, cite everything.** Every novelty carries `[NOVEL — extends X]`
   or `[CITED — <source>]`. Superseded material carries `[HISTORICAL]`, never
   gets removed.
4. **The three threads stay separate.** TIG / Q-series / basin-finite-arithmetic
   do not import vocabulary across each other without a proved map.
5. **This file never gets edited once committed.** Future story snapshots
   add new files with later date suffixes — e.g.
   `MASTER_TRUNK_STORY_2026_05_NN.md`.

---

**End of 2026-04-19 master-trunk story snapshot.**
