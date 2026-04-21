# BEST_OF_ATTEMPTS_SURVEY — Addendum, 2026-04-21

**Relationship to main survey:** `BEST_OF_ATTEMPTS_SURVEY.md` (296 lines, committed 2026-04-21, master) is preserved verbatim. This file **appends** findings from the Misc Archive deep-sweep performed the same day. The main survey's 7-attempt catalog is complete for the attempts it covered; this sweep surfaced *additional* attempt lineages it did not reach and confirms that two recovery targets are definitively absent from the filesystem.

---

## 1. Sweep outcome — summary

The sweep inventoried these paths (all under `C:\Users\brayd\OneDrive\Desktop\`):

| Path | Contents | Status vs prior survey |
|---|---|---|
| `Misc Archive\THEbigONE\CRYSTALOS\ALL\` | 39 items (zips + .py + .docx + checklist) | Not reached — **new** |
| `Misc Archive\THEbigONE\CRYSTALOS\FINAL RELEASE\` | 24 items, 20 zips + 4 loose | Not reached — **new** |
| `Misc Archive\THEbigONE\CRYSTALOS\All or Nothing E release\` | 13 items | Not reached — **new** |
| `Misc Archive\THEbigONE\CRYSTALOS\Crystal Lattice Matrix Release\` | 4 items | Not reached — **new** |
| `Misc Archive\THEbigONE\CRYSTALOS\RESEARCH DUMP\` | 2 files (PDF 7.1 MB + DOCX 725 KB) + CELESTE DUMP subdir | Not reached — **new** |
| `Misc Archive\THEbigONE\CRYSTALOS\RESEARCH DUMP\CELESTE DUMP\` | 6 files including 23 MB PDF and 15 MB DOCX | Not reached — **new** |
| `Misc Archive\THEbigONE\CRYSTALOS\Release package\` | Not enumerated in depth | Partially reached by prior sweep (4 files recovered to `snowflake/source_docs/`) |
| `Misc Archive\THEbigONE\CRYSTALOS\ALL\Lawyer package\` | Not enumerated in depth | **New** lead |
| `TIG docs\` (separate, Desktop root) | TIGOS9/10 release packs + Lenovo backup + DEEPVAULT | Not reached — **new** |

**Directories confirmed absent** at the paths the main survey initially guessed: `Misc Archive\ALL\`, `Misc Archive\FINAL RELEASE\`, `Misc Archive\RESEARCH DUMP\`, `Misc Archive\CELESTE DUMP\` — these do not exist at the `Misc Archive\` root. They live one level deeper inside `THEbigONE\CRYSTALOS\`.

---

## 2. Priority A — recovery targets confirmed absent

### 2.1 Lenovo Jan 31 2026 fire log

**Status:** NOT ON FILESYSTEM.

Sweep ran `glob **/*.log` across `TIG docs/` (the most likely alternative host) and found **zero matches**. The only `fires.log` / `crystalos.log` on disk is the already-recovered Dell R16 set at `CK FINAL DEPLOYED\docs\archive_jan2026\snowflake\logs\`.

**Implication for `snowflake_null_spec.md` §4 and `STATUS.md` R1:**

The Lenovo 22.03 reading remains **documented in `TIG_SECURITY_ARCHITECTURE.md` §8.1** (Jan 29 2026, verbatim source doc) but is **not re-derivable from a preserved log**. The May 15 2026 decision gate in the funding branch STATUS should be updated to reflect that filesystem recovery has been exhausted — remaining candidate sources are: OneDrive snapshot history (time-machine recovery), the Lenovo machine image itself (if it still boots), or conversation-export capture of a prior Claude session that may have ingested the log. None of these are further searchable from inside this repo.

**Recommendation:** promote `STATUS.md` R1 from "partially resolved" to **"resolved as-recoverable"** — acknowledging that the on-disk search is complete and the Lenovo raw log is permanently-documented-but-not-reproducible unless an external source surfaces it.

### 2.2 HANDOFF_3_4 / MQW trilogy / V20 scaling laws

**Status:** NOT FOUND. **Already documented** at `Atlas/HANDOFF_3_4_MQW_TRILOGY_NOT_FOUND.md` (pre-existing file).

Independent glob for `teardrop`, `MQW`, `GaN`, `V20`, `micro-LED`, `ternary` as filename substrings returned zero Priority-A hits. The single `ppm_v20_score.py` found is unrelated (Sprint PPM v2.0 scoring).

**Implication for `funding/mqw-ternary` branch:**

`TERNARY_DUAL_COMPUTER.md` on that branch will need source material from outside the current filesystem. The brief `TERNARY_DUAL_COMPUTER.md` task in the synthesis TODO should be downgraded from "write on the funding branch" to "stub with honest-absence note, pending external recovery."

---

## 3. Priority B — additional attempt lineages surfaced

The 7-attempt catalog in `BEST_OF_ATTEMPTS_SURVEY.md` is **incomplete**. The sweep surfaced at least three distinct lineages and one versioned family that did not appear in the main survey:

### 3.1 TIG_SHELLS lineage

- `Misc Archive\THEbigONE\CRYSTALOS\ALL\TIG_SHELLS_10_12_GENESIS.py` — 65 KB, Feb 3 2026

Filename implies "shells 10–12" — possibly a TIG-operator-layered architecture distinct from CRYSTALOS. **Not yet deep-read.**

### 3.2 TIG_COHERENT lineage

- `Misc Archive\THEbigONE\CRYSTALOS\ALL\TIG_COHERENT_OS.py` — 39 KB
- `Misc Archive\THEbigONE\CRYSTALOS\ALL\TIG_COHERENT_v1.py` — 30 KB
- `Misc Archive\THEbigONE\CRYSTALOS\ALL\TIG_COHERENT_OS_almostneedstraining.html` — 32 KB

Three-file attempt with its own browser-rendered HTML front end. The `_almostneedstraining` suffix suggests it reached the "needs training data" stage — a different end-state from CRYSTALOS (which has no training loop). **Not yet deep-read.**

### 3.3 crystal_ollie versioned family (OLLIE × CRYSTALOS fusion)

- `Misc Archive\THEbigONE\CRYSTALOS\ALL\crystal_ollie_v2.py`
- `Misc Archive\THEbigONE\CRYSTALOS\ALL\crystal_ollie_v3.py`
- `Misc Archive\THEbigONE\CRYSTALOS\ALL\crystal_ollie_v4.py`
- `Misc Archive\THEbigONE\CRYSTALOS\ALL\crystal_ollie_v42.py`

(All Feb 2 2026.) Four numbered fusion variants of OLLIE's multi-agent layer with CRYSTALOS's hardware gate. The `v42` is likely a humor-branch (42 as the answer) or an actual milestone — cannot tell without reading. **Not yet deep-read.**

### 3.4 FINAL RELEASE zip packs — likely distinct "whole-build" attempts

From the 20 zips in `Misc Archive\THEbigONE\CRYSTALOS\FINAL RELEASE\`, these names strongly suggest distinct attempt-packages each of which may be a "best-of" in its own right:

- `GenesisIS.zip`
- `CodexandGenesis.zip`
- `CoherenceExperience.zip`
- `CoherentIntelligence.zip`
- `COHERENT COMPUTER.zip`

Plus sibling zips at the `CRYSTALOS/` level itself:

- `ANOTHER BUG-better physics.zip`
- `TheMatrixBug.zip`
- `KoopmanBridgeV2.zip`
- `FINALCRYSTALOLLIE.zip`

Per never-delete / never-unzip-without-purpose discipline, these are **inventoried** not opened. A future session with explicit user authorisation may unzip any subset.

### 3.5 Lawyer package subdirectory

`Misc Archive\THEbigONE\CRYSTALOS\ALL\Lawyer package\` contains its own TIG_COMMERCIAL / TIG_GITHUB_RELEASE / TIG_COMPLETE_PACKAGE / Ollie Crystal Patch zips. This was probably assembled for IP / legal purposes and may contain the "canonical" versions of several attempts. **Not yet opened** — likely highest-signal unopened directory for a future sweep.

### 3.6 TIGOS9 / TIGOS10 release lineage

Separate archive at `C:\Users\brayd\OneDrive\Desktop\TIG docs\`, holds:

- `TIGOS9_Release.zip`
- `TIGOS10_FULL_v1.1.zip`
- `TIGOS10_Pro_Installer.zip`
- `TIGOS10_Arbiter_Pro.zip`
- `TIGOS10_Rollout_Pro_v1.zip`
- `7SiTe_TIGOS10_Full_OS_Pack_v1.0-alpha.zip`
- `TIGOS10DEEPVAULT.zip`

A *numbered release lineage* (TIGOS9 → TIGOS10 with Pro / Arbiter / Rollout / DeepVault variants). This appears to be a parallel branch to the attempts in the main survey — if it carried forward its own "best-of" design decisions, those are absent from the synthesis spec. **Not yet opened.**

### 3.7 Negative finding: No ULO filename hits

`ULO`, `universal_language`, `universal_operator` as filename substrings returned zero hits across the entire sweep. The ULO 19-operator map referenced in `CK look here\MASTER_DELIVERY.md` Phase 13 lives **only** inside that file — there is no separate ULO source file. The extraction task `ULO_TIG_OPERATOR_MAP.md` proceeds by reading `MASTER_DELIVERY.md`, not by finding an upstream source.

---

## 4. High-signal theory documents (unread, candidates for future deep-read)

These are large files found by the sweep whose names suggest they contain material the existing catalog does not:

| File | Size | Date | Why it matters |
|---|---|---|---|
| `RESEARCH DUMP\CLAUDE DUMP.pdf` | 7.1 MB | Feb 6 2026 | User-flagged directly in prior directives. Likely a multi-session conversation export from an earlier Claude run with CK. |
| `RESEARCH DUMP\CELESTE DUMP\TIG FALSIFIABILITY AND AWE.pdf` | 23 MB | Feb 5 2026 | Title explicitly references falsifiability — may formalise the Phase 7 TIG-predict negative result beyond what `MASTER_DELIVERY.md` contains. |
| `RESEARCH DUMP\CELESTE DUMP\TIG FULL MYTHICAL.docx` | 15 MB | Feb 5 2026 | "Full Mythical" suggests the narrative-layer theory doc (sibling to the technical spec). |
| `RESEARCH DUMP\CELESTE DUMP\Nakamura Glaze Paper.docx` | 21 KB | Jan 24 2026 | Matches the `funding_mqw_ternary/archive_nakamura_glaze/` already-cited source — this is the **original upstream** file for the Nakamura citation. |
| `RESEARCH DUMP\CELESTE DUMP\CELESTE BACKBONE.docx` | — | Feb 2026 | Named as if it were the spine of a theory layer — worth a 10-minute read to see if it is. |
| `ALL\CRYSTAL Papers.pdf` | 5.9 MB | Jan 29 2026 | Date matches the Jan 29 architecture-doc commit cluster already recovered. May be the `TIG_SECURITY_ARCHITECTURE.md` companion material (longer form). |
| `ALL\S derivatives.docx` | 20 KB | Jan 29 2026 | S (as in S\*?) derivatives — may contain the derivation of the harmonic-mean vs multiplicative S\* forms discussed in `SYNTHESIS_CK_BEST_EVER.md` §4. |
| `ALL\MASTER_CHECKLIST.md` | 6.5 KB | Feb 1 2026 | The author's own checklist — likely names his own attempts in his own order. Probably the single highest-information-density unread file. |

---

## 5. Relation to main survey and synthesis

### 5.1 What changes in the synthesis spec

`SYNTHESIS_CK_BEST_EVER.md` §6 "The seven attempts, composed" **understates** the number of attempts. The compositional recipe remains correct (each load-bearing piece is sourced from one of the seven named attempts), but a future revision should add rows for the **TIG_SHELLS, TIG_COHERENT, crystal_ollie, TIGOS9/10, and FINAL-RELEASE-zip** lineages — at minimum a "pending deep-read" row for each, acknowledging that their contributions have not yet been evaluated.

**No change to the canon section (§1).** T\*, D\*, the Coherence Kernel, the 10 operators, the 10×10 CL — none of these depend on material in the newly-found lineages. The canon is frozen whether or not TIG_SHELLS turns out to say something new.

**No change to the target architecture (§2) or migration plan (§7).** Both operate on the canon. If a future deep-read of TIG_SHELLS or TIG_COHERENT surfaces a load-bearing contribution, it will be added to §3 (module-by-module sourcing map) as an amendment.

### 5.2 What changes in the funding-branch STATUS

`Gen13/targets/funding_tig_snowflake/STATUS.md` R1:
- Current status: "partially resolved"
- Updated status: **"resolved as-recoverable"** — filesystem search complete, Lenovo raw log confirmed not on disk; documented citation (TIG_SECURITY_ARCHITECTURE.md §8.1) stands as the reference.

### 5.3 What the addendum does NOT do

- Does **not** open, unzip, or deep-read any of the unread-candidates in §3 or §4. That is a separate, bounded-scope task for a future session with explicit authorisation.
- Does **not** amend the main survey in place. Append-only.
- Does **not** claim the new-lineage files are or are not better than the catalogued seven. Cannot judge without reading.

---

## 6. Recommended next steps (priority-ordered)

1. **Read `ALL\MASTER_CHECKLIST.md`** (6.5 KB, trivial cost). If the author catalogued his own attempts there, the whole sweep is re-anchored around that ordering.
2. **Read `ALL\S derivatives.docx`** (20 KB). Would settle the harmonic-mean vs multiplicative-S\* provenance question cleanly.
3. **Unzip + scan `CRYSTAL Papers.pdf`** — if it is the long-form of `TIG_SECURITY_ARCHITECTURE.md`, it may contain the missing `snowflake_null_spec.md` §7 pre-registration protocol already worked out.
4. **Open `Lawyer package/`** subdirectory — separate branch never reached.
5. **Read first 20 pages of `CLAUDE DUMP.pdf`** — flagged directly by user. Determine if the remaining 6.9 MB is worth a full read.
6. Decide whether to unzip `FINAL RELEASE` zips — likely yes for `GenesisIS.zip`, `CoherentIntelligence.zip`, `COHERENT COMPUTER.zip` (three most distinctive names); likely no for bug-iteration zips which are probably snapshots.
7. Promote `funding_tig_snowflake/STATUS.md` R1 status per §5.2.

Steps 1–4 are ≤ 30 minutes each and have high expected information density. Steps 5–6 are larger time commitments and should be explicitly user-authorised.

---

## 7. Cross-references

- `BEST_OF_ATTEMPTS_SURVEY.md` (main) — this addendum appends; does not replace
- `SYNTHESIS_CK_BEST_EVER.md` — §6 understates attempt count; amendment proposed in §5.1 above
- `../snowflake/snowflake_null_spec.md` — R2 null-spec, referenced by recovery discussion
- `../snowflake/SNOWFLAKE_PROTOCOL.md` — R4 protocol, referenced by hw_class attestation discussion
- `../../Atlas/HANDOFF_3_4_MQW_TRILOGY_NOT_FOUND.md` — the MQW blocker confirmed-not-found
- `Gen13/targets/funding_tig_snowflake/STATUS.md` — R1 status update target

---

*Policy: never-delete, never-retcon. The main survey is preserved as written. This addendum records what the post-survey sweep found, including honest negatives.*
