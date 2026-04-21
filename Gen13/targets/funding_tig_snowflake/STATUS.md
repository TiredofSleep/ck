# STATUS — funding/tig-snowflake

**As of:** 2026-04-20
**Next review:** when CRYSTALOS logs are located OR Brayden requests a status check.

---

## Branch state

- Branch seeded: 2026-04-20
- Target folder: `Gen13/targets/funding_tig_snowflake/`
- Files: README, FUNDERS, ARTIFACTS, PITCH_DRAFT, LIMITATIONS, STATUS (this file)
- Rigor base: `tig-synthesis` HEAD at time of seeding

## Readiness checklist

### Content (this branch)
- [x] README with funder-facing framing
- [x] FUNDERS.md with DARPA I2O primary + 4 others
- [x] ARTIFACTS.md with recovery tasks R1–R4
- [x] PITCH_DRAFT.md skeleton (DO NOT SEND without R1–R4)
- [x] LIMITATIONS.md with ten honest-scope items
- [x] STATUS.md (this file)

### Recovery (before any pitch)
- [ ] **R1**: Locate CRYSTALOS log with χ² = 22.03 output. **2026-04-21 R16 sweep result: NOT FOUND** in repo history, public-repo scan (`_r16_repo_scan/`), handoff unpack (`_history_search_unpack/`), Work Docs, or any Brayden sprint-raw staging folder. See `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md` for the list of searched locations and the recovery-effort ranking. Next candidate paths: OneDrive snapshot history, iCloud Drive, external-drive backup, ClaudeChat export for commit `9fdac5c3`.
- [ ] **R2**: Author null-hypothesis specification (`docs/archive_jan2026/snowflake_null_spec.md`). Content: H₀ statement, partition scheme P, partition count k, sample size N, degrees of freedom, stopping rule, test convention. **Requires R1 output or direct Brayden recollection.**
- [ ] **R3**: Identify or generate held-out dataset for blind replication.
- [ ] **R4**: Author adversarial model (`docs/archive_jan2026/snowflake_adversary.md`).
- [ ] External statistician review of R2 (at least one second set of eyes before any funder sees it)
- [ ] Copy `TIME-FOR-HELP-AND-SCRUTINY` repo contents into `docs/archive_jan2026/snowflake_source/` with provenance header

### Pre-pitch work
- [ ] Brayden reviews + edits PITCH_DRAFT
- [ ] Brayden confirms DARPA I2O as first funder, vs. NSF SaTC or ONR
- [ ] Academic co-PI identified (required for NSF SaTC path; optional for DARPA seedling)
- [ ] Brayden confirms license framing acceptable to the chosen funder

### Pitch-to-send
- [ ] Final funder-specific customization
- [ ] Attachment bundle assembled
- [ ] Brayden sends

## Dependencies / blockers

- **Blocker 1** (absolute): R1 CRYSTALOS log recovery. Nothing ships without the raw numbers being re-derivable from a preserved log. **2026-04-21 R16 sweep confirms the log is not anywhere in the current filesystem; recovery now depends on OneDrive/iCloud snapshot history or ClaudeChat conversation export.** See `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md`. If recovery fails by the decision gate (2026-05-15 suggested), the branch redrafts the pitch to either (a) drop the anomaly-detection angle entirely, or (b) defer it to a Phase 2 follow-up with freshly-generated data.
- **Blocker 2**: R2 null-specification. The statistic is only as strong as the written null it rejects.
- **Blocker 3**: R3 blind-test dataset. Without it, the finding is pre-registered on the same data it was discovered on, which is circular.
- **Blocker 4**: R4 adversarial model. Without it, "earlier-than-rule-match" is unfalsifiable.

None of these block the branch existing or being populated with scaffolding; all four block sending a pitch.

## Recent activity

| Date | Event |
|---|---|
| 2026-04-20 | Branch seeded from `tig-synthesis`; target folder + 6 files committed |
| 2026-04-21 | **R1 recovery failed** — 2026-04-21 R16 filesystem sweep confirms CRYSTALOS log not in repo / public-repo clones / handoff unpack / Work Docs / any sprint-raw staging. Full findings in `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md`. Decision gate: 2026-05-15 — redraft pitch if recovery still blocked. |

## Cross-references

- Plan: `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`
- Jan 2026 recovery manifest: `docs/handoffs/claudecode_handoff_2026_04_20/JAN2026_RECOVERY_MANIFEST.md` (Thread 5, commit `9fdac5c3`)
- Handoff: `docs/handoffs/claudecode_handoff_2026_04_20/`
- Trunk story: `MASTER_TRUNK_STORY_2026_04_19.md` (on master)

---

*Update freely on this branch. Changes here do NOT require master cherry-pick unless they materially change the ARTIFACTS or FUNDERS inventories.*
