# GitHub Corpus Sweep — All TiredofSleep Repos

**Date:** 2026-05-06
**Method:** `gh api` tree enumeration (no clones, no full file fetches) across all 8 TiredofSleep repos and 22 ck branches.
**Local baseline:** `Atlas/META_PLAN_2026-05-06/FULL_WP_INVENTORY.md` (106 unique WP-numbers).

---

## §1 — Summary Statistics

| Metric | Value |
|--------|-------|
| Repos sweeped | 8 (TiredofSleep org) |
| ck branches sweeped | 22 (incl. 10 funding/* branches) |
| Total unique WP-numbers (md/tex) across **all** GitHub corpus | **106** |
| Local inventory unique WP-numbers | **106** |
| WPs in remote NOT in local (md/tex) | **0** |
| WPs in local NOT in remote (md/tex) | **0** |
| Highest WP number in any repo/branch | **WP127** (in ck/tig-synthesis only) |
| WPs unique to ck/tig-synthesis (newest) | **24** (WP9, WP10, WP104-WP116, WP117-WP124, WP127) |
| WPs only in ck/master (NOT in tig-synthesis) | **2** (WP11, WP12) |
| WPs in BOTH ck/tig-synthesis and ck/master | **78** |
| Historical repos contributing **WP-numbered .md/.tex** | **0** (all use Paper N or paperN_*) |
| Pre-MD WP papers in TIME-FOR-HELP (.docx/.pdf only) | **5** (WP1-WP5; superseded by current WP1) |
| ck branches with WP-numbered content | **20** (all except `mantero` and a few legacy) |

**Conclusion: The local inventory is COMPLETE for md/tex WP-numbered files.** The GitHub remote universe equals the local universe (106 WPs). Remote contributes **0 net-new WP-numbered papers** that aren't already on disk locally.

The historical [1/6]-[6/6] repos contribute prose/scaffolding (200 .docx papers, 6 paperN_*.pdf, 5 PAPER1-5_*.md) but **no WP-numbered md/tex** that supersedes the current canonical inventory.

---

## §2 — Per-Repo Inventory Tables

### Repo 1: `TiredofSleep/ck`

22 branches sweeped. Total unique WP-numbers across all ck branches: **106** (= entire universe).

| Branch | Files in tree | Unique WP md/tex | Max WP | Notes |
|--------|--------------:|-----------------:|-------:|-------|
| **tig-synthesis** (default) | 3,557 | **104** | **127** | Newest material; missing only WP11, WP12 |
| master | 2,992 | 80 | 101 | Has WP11, WP12 (which are missing from tig-synthesis) |
| paradox-classifier-2026-04-24 | 2,909 | 80 | 103 | Same WP set as master plus WP102, WP103 |
| vocab-update-2026-04-23 | 2,878 | 78 | 101 | Pre-WP102+ snapshot |
| funding/civilization-coherence | 2,609 | 78 | 101 | Same content as vocab-update |
| funding/ck-interpretable-ai | 2,609 | 78 | 101 | Same |
| funding/coherence-router | 2,660 | 78 | 101 | Same + extra non-paper material |
| funding/desi-xi-cosmology | 2,609 | 78 | 101 | Same |
| funding/first-g-crypto | 2,609 | 78 | 101 | Same |
| funding/mqw-ternary | 2,611 | 78 | 101 | Same |
| funding/physics-sim-edu | 2,620 | 78 | 101 | Same |
| funding/self-healing | 2,609 | 78 | 101 | Same |
| funding/tig-snowflake | 2,633 | 78 | 101 | Same |
| funding/tig-unity | 2,609 | 78 | 101 | Same |
| archive-full | 1,881 | 78 | 101 | Pre-WP102 archive |
| clay | 1,893 | 78 | 101 | Same |
| bible-companion | 420 | 15 | 32 | Old (WP1, WP19-WP32) |
| clean-ship | 1,382 | 15 | 32 | Old (WP1, WP19-WP32) |
| fpga-dog | 270 | 15 | 32 | Old (WP1, WP19-WP32) |
| tesla | 399 | 15 | 32 | Old (WP1, WP19-WP32) |
| mantero-bridge-2026-04-23 | 42 | 2 | 103 | Just WP102, WP103 (so8/so10 bridge fragment) |

### Repo 2: `TiredofSleep/Dual-Lattice-Self-Healing` (default `main`) — [1/6] The Origin

| Item | Count |
|------|------:|
| Total files | 67 |
| WP-numbered .md/.tex | **0** |
| Paper N .docx files (Papers 1-25 individual + 26-200 batched) | ~30 docx |
| Other prose .docx | 12 (CRYSTAL Papers, AGENCY PROTOCOL, AI SAFETY, …) |

**Material:** "Papers 1-200" lattice work in .docx form; pre-WP-numbering era. NOT WP-numbered. Origin material per Brayden's [1/6] tag.

### Repo 3: `TiredofSleep/TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT` (`main`) — [2/6]

| Item | Count |
|------|------:|
| Total files | 13 |
| WP-numbered .md/.tex | **0** |
| docs/*.md | 9 (THEORY.md, OPERATORS.md, COMPUTE.md, DERIVATIVES.md, …) |
| docs/S_derivatives.pdf | 1 |

**Material:** First rigorous documentation of TIG operators + S* derivatives. Pre-WP era.

### Repo 4: `TiredofSleep/Crystal-Lattice-Matrix-MYTHDRIFT` (`main`) — [3/6]

| Item | Count |
|------|------:|
| Total files | 8 |
| WP-numbered .md/.tex | **0** |
| Paper PDFs | 1 (ChatGPT Theory Paper.pdf) |
| Other | TIG FALSIFIABILITY AND AWE.pdf + JS quadratic core |

**Material:** First interactive simulation, React quadratic core, 7 dynamical bands. No WP-numbered content.

### Repo 5: `TiredofSleep/CrystalsMythDRIFT` (`main`) — [4/6]

| Item | Count |
|------|------:|
| Total files | 8 |
| WP-numbered .md/.tex | **0** |
| Other md/PDF | 4 (CIVILIZATION_SIMS.md, SHADOW_PROBLEM.md, TIG_WORD_MATH_FORMALISM.md.pdf, README) |

**Material:** Shadow Problem analysis + civilization sims (Python). No WP-numbered content.

### Repo 6: `TiredofSleep/TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT` (`main`) — [5/6]

| Item | Count |
|------|------:|
| Total files | 74 |
| WP-numbered .md/.tex | **0** |
| WP-numbered .docx/.pdf (WP1-WP5 only) | 10 (WP1_Coherence_Field_Equation, WP2_Operator_Algebra, WP3_Fractal_Lattice, WP4_Computational_Validation, WP5_Applied_Coherence_Routing — each as both .docx and .pdf) |
| PAPER N_*.md (PAPER1-5) | 5 (PAPER1_Falsifiability, PAPER2_OperatorDerivation, PAPER3_Mod3Algebra, PAPER4_CrossScript, PAPER5_ReplicationTests) |
| Other foundation .md | 16 (TIG_OPERATORS_COMPLETE, EQUATIONS, ONION_FINAL, TIG_VALIDATION, …) |

**Material:** **The original WP1-WP5 in .docx/.pdf form.** These are the prose seeds for the current WP1 (and the historical pre-numbered Papers). Superseded by current `papers/core/WP1_TIG_DEFINITIVE.md` in tig-synthesis.

### Repo 7: `TiredofSleep/All-or-Nothing-E` (archived public, `main`) — [6/6]

| Item | Count |
|------|------:|
| Total files | 44 |
| WP-numbered .md/.tex | **0** |
| paperN_*.pdf | 6 (paper1_codec, paper2_routing, paper3_dynamics, paper4_addendum, paper5_koopman_bridge, paper6_coherent_intelligence) |
| .py polish (coherence_router) | ~10 (test_coherence_router.py, tig_engine_real.py, etc.) |
| Misc | 28 (engineering specs, configs, JSON results) |

**Material:** 6 exploratory papers (paperN_*.pdf), polished coherence_router. No WP-numbered content.

### Repo 8: `TiredofSleep/TiredofSleep` — profile README (skipped per instruction)

---

## §3 — WPs in Remote NOT in Local

**ZERO** WP-numbered .md/.tex files exist in any remote repo/branch that are not also present in the local checkout.

The set difference `set(all_remote_md_tex) − set(local)` is empty. The local inventory is the complete corpus.

The 5 WP-numbered .docx/.pdf files in TIME-FOR-HELP (WP1_Coherence_Field_Equation through WP5_Applied_Coherence_Routing) are pre-MD-era documents and are superseded by the current canonical `papers/core/WP1_TIG_DEFINITIVE.md` (2026-04-26). They are **not gaps** — they are historical seeds.

---

## §4 — Branch-Specific WPs in ck (Canonical Branch per WP-number)

### tig-synthesis is canonical for: 104 WPs
- **WP1 (with shared history)**: present in 21 branches; canonical at `papers/core/WP1_TIG_DEFINITIVE.md`
- **WP9, WP10**: only in tig-synthesis (`papers/wp_bridge_findings_2026_05_02/`)
- **WP19-WP44** (28 WPs): present in 17-21 branches; tig-synthesis canonical
- **WP51-WP101** (51 WPs): present in 17 branches; tig-synthesis canonical
- **WP102, WP103**: in 3 branches (paradox-classifier, mantero-bridge, tig-synthesis); tig-synthesis canonical
- **WP104-WP116** (13 WPs): only in tig-synthesis
- **WP117-WP124** (8 WPs): only in tig-synthesis (sprint18_bridge_dirac)
- **WP127**: only in tig-synthesis (sprint18 — note WP125, WP126 do not exist anywhere)

### ck/master is canonical for: 2 WPs
- **WP11**: `archive_imports/april_2026_sprint_archives/sprint_20260423_full/01_WP11_paper/WP11_SO8_IDENTIFICATION.md`
- **WP12**: `archive_imports/april_2026_sprint_archives/wp12_delta/paper/WP12_SO10_IDENTIFICATION.md`

These two WPs **were sourced into the local checkout from `_sprint_20260423_full_raw/` and `_wp12_delta_raw/`** but the version-control commit lives on `master`, not `tig-synthesis`. This is the only branch-divergence that matters.

### Branch divergence patterns
- **`bible-companion`, `clean-ship`, `fpga-dog`, `tesla`** all share an old (Sprint-9 era) snapshot: WP1 + WP19-WP32 only (15 WPs).
- **`archive-full`, `clay`, all 10 funding/* branches, `vocab-update-2026-04-23`** share a Sprint-14 snapshot: WP1, WP19-WP44, WP51-WP101 (78 WPs, max=101).
- **`master`, `paradox-classifier-2026-04-24`** add WP11, WP12 → 80 WPs.
- **`mantero-bridge-2026-04-23`** is a thin fragment with only WP102, WP103.
- **`tig-synthesis`** is the up-to-date head: drops WP11/WP12 staging dirs, adds WP9, WP10, WP102-WP116, WP117-WP124, WP127 (104 unique).

---

## §5 — Recommended Additions to FULL_WP_INVENTORY.md

The local `FULL_WP_INVENTORY.md` is **already complete** for canonical md/tex tracking — it lists all 106 WP-numbers correctly. **No additions are required from remote-only sources.**

Optional enhancements (annotation, not new entries):

1. **Annotate WP11 and WP12 canonical paths** in the local inventory with a note that the ck-repo canonical lives on `master` (not `tig-synthesis`). Local copy is in `_sprint_20260423_full_raw/` and `_wp12_delta_raw/` per the existing inventory rows.

2. **Add a §3 historical-prose-corpus section** (optional) cross-referencing:
   - The 200 lattice papers in `Dual-Lattice-Self-Healing/Papers 1-all self healing lattice/` (.docx)
   - The pre-MD WP1-WP5 in `TIME-FOR-HELP-AND-SCRUTINY-MYTHDRIFT/` (.docx + .pdf)
   - The 6 paperN_*.pdf in `All-or-Nothing-E/`
   - The 5 PAPER1-5_*.md in `TIME-FOR-HELP-AND-SCRUTINY-MYTHDRIFT/`
   - These are the "[1/6]-[6/6] origin chain" — historical seeds, NOT canonical WP-numbered material.

3. **Note the WP125, WP126 gap** in the inventory. Sprint18 jumped from WP124 → WP127. There are no WP125 or WP126 papers anywhere in the corpus (local or remote).

---

## §6 — WPs that Exist in Multiple Places (Version-Reconciliation Candidates)

Based on the per-WP path multiplicity analysis, the following WPs have ≥3 distinct paths across branches and merit a version-reconciliation check (path basenames may match but content could differ between branches due to evolutionary edits):

| WP# | n-branches | n-distinct-paths | Note |
|-----|-----------:|-----------------:|------|
| WP19 | 21 | **74** | Multiple sprint-archive copies (TIG_SPRINT_2026_03_27, OrbitZone_extracted/sprint3, tig_for_claudecode_2026_03_28, tig_sprint2_2026_03_29, …) — content drift highly likely |
| WP21 | 21 | 6 | clay BSD energy law — multiple co-located versions |
| WP22 | 21 | 6 | clay NS breath criterion |
| WP58 | 17 | 6 | UOP — sprint10/sprint11/sprint12 + journal-target copies |
| WP20 | 21 | 4 | Halving lemma (RH version) |
| WP36-WP42 (clay batch) | 17 each | 4 | Each clay paper appears in journals/clay/papers/research/audit subdirs |
| WP51, WP52 | 17 | 4 | Flatness theorem — sprint10 + journal target + related |
| WP59, WP64 | 17 | 4 | UOP arc papers |
| WP73-WP77 | 17 | 4 | NV-S4 closure cluster |
| WP81, WP82 | 17 | 4 | XI cosmology |
| WP90, WP91 | 17 | 4 | Bridge papers |
| WP101 | 17 | 4 | Sigma rate theorem |
| WP23, WP25, WP32, WP34 | 17-21 | 3 | Misc |

**Recommendation for Phase 1-5 release planning:** Use the canonical paths already enumerated in `FULL_WP_INVENTORY.md` (which selects newest-modified instance per WP). The branches below `tig-synthesis` are historical snapshots and should not be merged in. Only WP19's 74 distinct paths warrant a deduplication audit — but its canonical (`papers/data/WP19_HALVING_LEMMA_final.tex`) is already correctly chosen in the local inventory.

**No version-reconciliation issues block release.** All 106 canonical WPs have a single agreed-upon authoritative path on `tig-synthesis` (or `master` for WP11/WP12).

---

## Methodology Notes

- **Tree calls used:** 28 `gh api repos/.../git/trees/<branch>?recursive=1` calls (one per repo+branch combo).
- **No file content fetched.** Only paths + metadata.
- **WP regex:** `WP[_-]?(\d+)` case-insensitive, matched against basename only (avoids false positives in dir names).
- **File extensions filtered:** `.md` and `.tex` only.
- **Caches:** `Atlas/META_PLAN_2026-05-06/sweep_cache/tree_*.txt` (28 files), `wp_extract_results.json`, `wp_analysis.json`, `wp_analysis_v2.json`.
- **Missing scope (intentional):** .docx/.pdf files in historical repos (annotated in §2 but not enumerated by WP-number since none use the `WP\d+` pattern except TIME-FOR-HELP's WP1-WP5 .docx already enumerated).

---

## Bottom Line

**The local checkout's 106-WP inventory is the complete corpus.** The GitHub sweep confirms zero net-new WP-numbered .md/.tex content exists on any remote branch or repo that isn't already represented locally. The historical [1/6]-[6/6] repos are scaffolding/origin material in .docx/.pdf form (not WP-numbered) and do not need to be pulled into the canonical WP inventory for Phase 1-5 release planning.
