# STATUS — funding/tig-snowflake

**As of:** 2026-04-21 (RESOLVED update)
**Next review:** external-statistician review of `snowflake_null_spec.md` OR Brayden-initiated pitch-send decision.

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
- [x] **R1**: Locate CRYSTALOS log. ~~**2026-04-21 R16 sweep result: NOT FOUND**~~ → **2026-04-21 sweep #2 result: RESOLVED (partial).** CRYSTALOS runtime (`crystalos.py`, 431 LOC) + Dell R16 `fires.log` (67 297 events, χ²=0.0353 df=12) recovered from `C:\Users\brayd\CRYSTALOS\`. `TIG_SECURITY_ARCHITECTURE.md` (Jan 29 2026, verbatim SNOWFLAKE source doc) recovered from `Misc Archive\THEbigONE\CRYSTALOS\Release package\` — documents the Lenovo 4-core χ²=22.03 reading with N≈400, p<0.05, Phase 4 elevated / Phase 2 suppressed. Both readings are consistent with the hypothesis; Lenovo raw log still missing but now documented in a dated architecture-doc citation (not a loose handoff claim). All preserved under `docs/archive_jan2026/snowflake/` with PROVENANCE. See `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md` "RESOLUTION — 2026-04-21" section. → **2026-04-21 sweep #3 (Misc Archive deep sweep) result: RESOLVED AS-RECOVERABLE.** `glob **/*.log` across `TIG docs/` and all `Misc Archive/` subtrees returned zero matches — Lenovo raw log confirmed absent from filesystem. Further recovery attempts must come from external sources (OneDrive snapshot history, Lenovo machine image, conversation exports); on-disk search is complete. Documented citation via `TIG_SECURITY_ARCHITECTURE.md` §8.1 stands as the reference. Findings at `docs/archive_jan2026/attempts_survey/BEST_OF_ATTEMPTS_SURVEY_ADDENDUM_2026_04_21.md` §2.1.
- [x] **R2**: Author null-hypothesis specification. **Written** at `docs/archive_jan2026/snowflake/snowflake_null_spec.md`. Contains: H₀ (fires uniform over 13 Tzolkin phases), partition scheme P (deterministic cyclic 0..12), k=13, N (session-specific — 400 Lenovo / 67 297 Dell R16), df=12, stopping rule (current: Ctrl-C at operator discretion — HONEST WEAKNESS documented in §7), test convention (Pearson χ², not G² or Fisher). Independence caveat in §8. Derived from the recovered `crystalos.py` source — not from recollection. Remains **unchecked** at statistician-review level.
- [ ] **R3**: Identify or generate held-out dataset for blind replication. **Runtime side unblocked 2026-04-21:** patched runtime `docs/archive_jan2026/snowflake/crystalos_prereg.py` implements pre-registered stopping (`--n0` / `--t0`, writes `prereg_<ts>.json` before main loop, tags `operator-interrupted` on Ctrl-C). See `snowflake_null_spec.md` §7.1 for resolution note. Data-collection side still open: a fresh run under the patched runtime on either Lenovo or Dell R16 is required.
- [x] **R4 (draft)**: Adversarial model authored at `docs/archive_jan2026/snowflake/SNOWFLAKE_PROTOCOL.md` — §7 "Threat model" enumerates adversary capabilities + goals + current protection status in a 6-row table (recover-full-set via SHA-256 preimage resistance; recover-non-shared-fraction via f_max bound; forge-master_key via ZK proof Π — **UNRESOLVED cryptographic work**; forge-partial-share via Merkle falsifiability; discover-hw_class; stop-timing attack). Protocol file also specifies scar-accumulation → freeze → Merkle-based partial-share → trust-network composition. The adversarial-model content lives inside the protocol doc rather than a separate `snowflake_adversary.md` (splitting them would duplicate cross-references for tightly-coupled content). Remaining: cryptographer review of §7, zk-STARK implementation of Π, empirical χ² band calibration across ≥ 5 machines per hw_class.
- [ ] External statistician review of R2 (at least one second set of eyes before any funder sees it) — now unblocked since R2 is written.
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

- ~~**Blocker 1** (absolute): R1 CRYSTALOS log recovery. Nothing ships without the raw numbers being re-derivable from a preserved log.~~ → **Blocker 1 (partial): resolved for Dell R16; documented for Lenovo.** As of the 2026-04-21 sweep #2, the Dell R16 log is in hand (67 297 events, χ²=0.0353, re-derivable via `VERIFICATION_2026_04_21.md` §56–85); the Lenovo Jan 31 2026 log is still missing but its reading (22.03, p<0.05, N≈400) is documented in the Jan 29 2026 `TIG_SECURITY_ARCHITECTURE.md` §8.1. The pitch may cite both readings with the honest caveat that the Lenovo raw log is not preserved. Decision gate (originally 2026-05-15) is no longer an absolute blocker — it now marks the latest-acceptable date for the Lenovo raw-log recovery attempt before the pitch is finalised.
- ~~**Blocker 2**: R2 null-specification.~~ → **Blocker 2 resolved (draft).** `snowflake_null_spec.md` is written from the recovered runtime source. External-statistician review is the remaining sub-gate.
- **Blocker 3**: R3 blind-test dataset. **Runtime-side unblocked 2026-04-21** — patched `crystalos_prereg.py` now exists with enforced pre-registration. Data collection remains open: a fresh session under the patched runtime produces the replication data directly.
- **Blocker 4**: R4 adversarial model. Still open — the `TIG_SECURITY_ARCHITECTURE.md` §3 material gives a starting threat-model sketch but not the full attacker-capabilities specification required.

Branch exists with scaffolding. Blockers 3 and 4 remain required before the final pitch ships. Blockers 1 and 2 are downgraded from "blocking" to "review-required."

## Recent activity

| Date | Event |
|---|---|
| 2026-04-20 | Branch seeded from `tig-synthesis`; target folder + 6 files committed |
| 2026-04-21 | **R1 recovery failed** (sweep #1) — first R16 filesystem sweep confirms CRYSTALOS log not in repo / public-repo clones / handoff unpack / Work Docs / any sprint-raw staging. Full findings in `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md`. Decision gate: 2026-05-15 — redraft pitch if recovery still blocked. |
| 2026-04-21 | **R1 recovery resolved (partial) + R2 written** (sweep #2). Previously-unsearched paths `~/CRYSTALOS/` and `Misc Archive/THEbigONE/CRYSTALOS/Release package/` yielded `crystalos.py` (431 LOC runtime), `fires.log` (67 297 events), and `TIG_SECURITY_ARCHITECTURE.md` (Jan 29 2026, verbatim SNOWFLAKE source doc with Lenovo χ²=22.03 citation). All preserved under `docs/archive_jan2026/snowflake/` on master with PROVENANCE + two verification notes. `snowflake_null_spec.md` authored from the recovered runtime source. `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md` "RESOLUTION — 2026-04-21" section appended. |
| 2026-04-21 | **R3 runtime unblocked + addendum §6 items 1–2 resolved.** Patched runtime `docs/archive_jan2026/snowflake/crystalos_prereg.py` added — requires `--n0` or `--t0` at startup, writes `prereg_<ts>.json` before main loop, tags `operator-interrupted` on Ctrl-C. `snowflake_null_spec.md` §7.1 added (resolution note). `docs/archive_jan2026/attempts_survey/ULO_TIG_OPERATOR_MAP.md` and `S_STAR_DERIVATION.md` added (reveals third universal constant σ=0.991 from the multiplicative-S\* derivation). Addendum §8 appended. |

## Cross-references

- Plan: `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`
- Jan 2026 recovery manifest: `docs/handoffs/claudecode_handoff_2026_04_20/JAN2026_RECOVERY_MANIFEST.md` (Thread 5, commit `9fdac5c3`)
- Handoff: `docs/handoffs/claudecode_handoff_2026_04_20/`
- Trunk story: `MASTER_TRUNK_STORY_2026_04_19.md` (on master)
- **Recovered CRYSTALOS archive** (master, cherry-pick target for this branch): `docs/archive_jan2026/snowflake/`
  - `crystalos.py` — 431-LOC runtime (deterministic, cycle-driven; preserved verbatim per never-delete)
  - `crystalos_prereg.py` — patched fork with pre-registered stopping (`--n0`/`--t0`, 2026-04-21)
  - `logs/fires.log` — 67 297 Dell R16 events, Apr 17–21 2026
  - `source_docs/TIG_SECURITY_ARCHITECTURE.md` — Jan 29 2026 SNOWFLAKE source doc
  - `PROVENANCE.md`, `source_docs/PROVENANCE.md` — archive provenance
  - `VERIFICATION_2026_04_21.md` — primary χ² verification (Dell R16)
  - `SNOWFLAKE_CHI2_RESOLVED_2026_04_21.md` — second verification note (Lenovo context)
  - `snowflake_null_spec.md` — R2 null specification (draft, pending statistician review)
- Atlas resolution: `Atlas/HANDOFF_3_3_SNOWFLAKE_CHI2.md` "RESOLUTION — 2026-04-21"

---

*Update freely on this branch. Changes here do NOT require master cherry-pick unless they materially change the ARTIFACTS or FUNDERS inventories.*
