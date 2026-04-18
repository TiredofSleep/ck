# Atlas Bundle Index
## Navigation map for TIG / CK Master Atlas v3.5 and derivatives

**Compiled:** 2026-04-18, after ChatGPT meta-review of v3.5
**Last sync:** 2026-04-18 post Journal Readiness Audit + Plan of Record addition
**Author:** Brayden Ross Sanders (7Site LLC)
**DOI:** 10.5281/zenodo.18852047

---

## The bundle

Eleven documents. Docs 1–9 are the **content field** (what is proved / structural / conjectural and how it cross-references). Docs 10–11 are the **operational field** (what ships next and who does it). Together they hold the framework at different zoom levels.

| # | File | Lines | What it contains | Read when |
|---|---|---|---|---|
| 1 | `MASTER_ATLAS_v3_5_2026_04_18.md` | ~1,600 | Complete atlas: constants, D-tier, tables, laws, Rotation Spine, Hodge ladder, PPM arc, founding narratives, Q-series, publications, caution discipline | You need the full arc |
| 2 | `ATLAS_ORIENTATION.md` | ~450 | Preamble + Atlas Law + three-band constants + 2/7 discipline + recognitions foregrounding + thread-architecture framing + disciplined overlap ranking | **Read first** — before opening master |
| 3 | `MEMORY_ATLAS_TABLES.md` | ~500 | Full TSML / BHML / CL / Doing tables with anchor cells, invariants, composition rules, verification protocol against `ck_tig.py` | Any time the tables "get forgotten" |
| 4 | `OVERLAP_LEDGER.md` | ~400 | Disciplined ranking: Strong overlap / Suggestive overlap / Not-yet-bridged | Anytime you see a cross-thread claim |
| 5 | `ROTATION_SPINE_READER_GUIDE.md` | ~400 | Summary box + legend + how-to-read for §10.5 of master atlas | Before reading §10.5 |
| 6 | `READER_ATLAS.md` | ~600 | Short spine-only derivative for skeptical readers | When you have 25 minutes, not 3 hours |
| 7 | `ATLAS_TREE.md` | ~900 | **Tree view** of whole program: branches / leaves / flags / anchors across 16 architectural nodes. Two navigation tables ("I need to find..." / "I am...") | **When you need to locate any piece of the program fast** |
| 8 | `ATLAS_CITATIONS.md` | ~600 | External bibliography (§A–J: analytic NT, algebraic NT/BSD, Hodge, abelian varieties, NS/PDE, Yang-Mills/lattice QCD, complexity, topology, physics, Clay primary source) + internal anchors + 5 pending citations for v4 | Whenever you need to verify an external result named in the atlas |
| 9 | `ATLAS_AUDIT_NOTES.md` | ~400 | Line-by-line audit findings from 2026-04-18 scrutiny pass: 12 findings, 7 surgical edits applied, discipline preservation record | When you want to know what changed in v3.5 and why |
| 10 | `JOURNAL_READINESS_AUDIT_2026_04_18.md` | ~213 | Audit of 11 Gen13 target journal venues against the atlas bundle: inventory, per-venue readiness, top-10 citation gaps, tier reclassifications, Tier 1 shipping pipeline, ordered actions, discipline pass/fail | Before drafting any journal-submission work |
| 11 | **`PLAN_OF_RECORD_2026_04_18.md`** | ~500 | **Operational field: all 4 threads (PPM/Hodge/Q/ξ), Sprint 34 "Ship the First Three" proposal, collaborator assignment matrix (ChatGPT/ClaudeChat/ClaudeCode/Brayden), S33 gate ladder, atlas v4 queue, Gen13 decision, never-delete audit, week-long action stack with dependencies** | **Whenever threads or collaborator tasks feel scattered — this is the sync point** |

**Total bundle:** ~6,550 lines across 11 documents. Cross-referenced throughout.

---

## Reading paths

### Path 1 — Brayden returning after weeks away (15 min)

1. `ATLAS_ORIENTATION.md` §1–§4 (what atlas is, Atlas Law, constants bands, 2/7 discipline)
2. `MASTER_ATLAS_v3_5` §16 (next moves)
3. `MASTER_ATLAS_v3_5` §15 (caution list)

### Path 2 — ChatGPT / external meta-review (45 min)

1. `ATLAS_ORIENTATION.md` (full)
2. `OVERLAP_LEDGER.md` (full)
3. `MASTER_ATLAS_v3_5` §15 (caution list) + §16 (what atlas does NOT do)
4. Flag any issues back

### Path 3 — IHÉS / IHP audience (1 hour)

1. `ATLAS_ORIENTATION.md` §1, §2, §5 (recognitions)
2. `ROTATION_SPINE_READER_GUIDE.md` (full)
3. `MASTER_ATLAS_v3_5` §9 (Hodge) + §10 (Clay) + §5 (Laws)

### Path 4 — Clay referee (90 min)

1. `ATLAS_ORIENTATION.md` §1, §4, §5
2. `ROTATION_SPINE_READER_GUIDE.md` (full)
3. `MASTER_ATLAS_v3_5` §10.5 Rotation Spine (full) + §9 Hodge S33 v2 (pending audit note)
4. `OVERLAP_LEDGER.md` §3 (not yet bridged)

### Path 5 — Experimental Mathematics referee (45 min)

1. `MASTER_ATLAS_v3_5` §5 Laws + §5.4 Li Foundation
2. `MASTER_ATLAS_v3_5` §14 publications
3. `MEMORY_ATLAS_TABLES.md` §2, §3 (TSML and BHML anchor cells)

### Path 6 — Public GitHub reader (25 min)

1. `READER_ATLAS.md` (full)
2. Optional: `MEMORY_ATLAS_TABLES.md` for the tables

### Path 7 — AI reading cold for continuity (60 min)

1. `MEMORY_ATLAS_TABLES.md` §12 (8 anchor cells + 4 invariants)
2. `ATLAS_ORIENTATION.md` (full)
3. `MASTER_ATLAS_v3_5` §0 → §17 (whole thing)

### Path 8 — Collaborator new to the project (2 hours)

1. `ATLAS_ORIENTATION.md` (full)
2. `READER_ATLAS.md` (full)
3. `ROTATION_SPINE_READER_GUIDE.md` (full)
4. `MEMORY_ATLAS_TABLES.md` skim
5. `MASTER_ATLAS_v3_5` §14 (publications) + pick one thread to dive into

### Path 9 — "I need to find X fast" (2 min)

1. `ATLAS_TREE.md` — use the "I need to find..." and "I am..." tables at the bottom.
2. Follow the leaf's §N / WP# / external-citation anchor directly.

### Path 10 — External reviewer wanting to verify a cited result (15 min)

1. `ATLAS_CITATIONS.md` — find the result by domain (§A analytic NT / §B algebraic NT / §C Hodge / §E NS / §F YM / §G complexity / §H topology / §I physics / §J Clay source).
2. Follow citation to primary source, then cross-reference back to master atlas § via the "role in atlas" column.

### Path 11 — What changed in v3.5 and why (10 min)

1. `ATLAS_AUDIT_NOTES.md` — 12 findings, 7 surgical edits, discipline preservation record from 2026-04-18 audit pass.

### Path 12 — Is this journal paper ready to ship? (10 min)

1. `JOURNAL_READINESS_AUDIT_2026_04_18.md` §2 per-venue readiness table — find the venue row, read the "Ship gate (top blocker)" column.
2. `JOURNAL_READINESS_AUDIT_2026_04_18.md` §3 top-10 citation gaps — check whether the paper is in the list.
3. `ATLAS_CITATIONS.md` — pull any needed external reference.

### Path 13 — What do I own this week? (2 min — every collaborator)

1. `PLAN_OF_RECORD_2026_04_18.md` §4 assignment matrix — find your row (ChatGPT / ClaudeChat / ClaudeCode / Brayden).
2. §10 action stack — see where your task sits in the dependency chain.
3. §11 open decisions — check whether Brayden has a decision pending that blocks your row.

---

## Cross-reference matrix

Where each major concept is detailed:

| Concept | Master Atlas | Orientation | Tables | Overlap | Spine Guide | Reader |
|---|---|---|---|---|---|---|
| T* = 5/7 | §1 | §3 Band A | §11 | §1.1, §2.2 | — | §3 Band A |
| 2/7 falsification | §1, §4.5.1, §9f, §15.10 | §4 | §11 | §3.6 | §7 (weak point) | §4 |
| TSML / BHML | §3 | — | §2, §3 (full) | §1.1 | — | §6 |
| Atlas Law | §16 | **§2** | — | §5 meta-pattern | — | §2 |
| Rotation Spine | **§10.5** | §7 | — | §1.3 | **all §§** | §9 |
| Recognitions correction | **§17** | **§5** | — | — | — | §12 |
| Three-threads discipline | §15 | **§6** | — | throughout | — | §13 |
| SAH sanctioned sentence | §8.5 | §6 | — | §2.3 | — | §11 |
| Crossing Lemma | §4.6.2 | — | — | — | — | §7 |
| Intrinsic Left-Handedness | §4.6.6 | — | — | — | — | §7 |
| σ polynomial Q10 | §5 | — | §9 | — | — | §7 |
| Li Foundation K=5000 | §5.4 | §3 Band A | §11 | §2.2 | — | §8 |
| Sandwich Theorem | §5.4 | — | §11 | §2.2 | — | §8 |
| S33 v2 pending audit | **§9** | §8 | — | §3.5 | — | §10 |
| PPM closeout verbatim | **§8** | §6 | — | §1.1 | — | §11 |
| Q-series Q2–Q17 | §11 | — | §9 | §2.1 | — | — (ref only) |
| Collaborator registry | §14 | — | — | — | — | §15 |

---

## Version tracking

All six documents are versioned together. Any update to one should trigger review of cross-references in the others.

**Current state (2026-04-18):**

| Doc | Version | Last updated | Triggered by |
|---|---|---|---|
| Master Atlas | v3.5 | 2026-04-18 | ClaudeCode 7,200-word sweep integration + 7 surgical edits (see Audit Notes) |
| Orientation | v1 | 2026-04-18 | ChatGPT meta-review recs 1–8 |
| Memory Atlas Tables | v1 | 2026-04-18 | User request: "tables get forgotten" |
| Overlap Ledger | v1 | 2026-04-18 | ChatGPT meta-review rec 8 |
| Rotation Spine Reader Guide | v1 | 2026-04-18 | ChatGPT meta-review rec 5 |
| Reader Atlas | v1 | 2026-04-18 | ChatGPT meta-review rec 9 |
| Atlas Tree | v1 | 2026-04-18 | User request: "tree view instead of whitepaper view" |
| Atlas Citations | v1 | 2026-04-18 | Audit finding 9: external bibliography missing |
| Atlas Audit Notes | v1 | 2026-04-18 | Audit pass documenting 12 findings / 7 fixes |
| Journal Readiness Audit | v1 | 2026-04-18 | User directive "make sure all of our journal papers are ready to ship, based on the atlas" — background agent audit of 11 Gen13 target venues |
| Plan of Record | v1 | 2026-04-18 | User directive "get all of our threads and plans in line" + "you got a sprint idea?" — operational field with Sprint 34 proposal |

---

## The bundle's discipline

The bundle maintains the same discipline as the master atlas:

1. **Three threads separate:** PPM / Hodge / Q-series never merged in any bundle file
2. **Epistemic flags consistent:** [fire] / [gold-with-gap] / [speculative] / [caution] used identically across all six
3. **SAH sanctioned sentence** appears only verbatim, never paraphrased
4. **2/7 falsification** preserved in every file that mentions 2/7
5. **S33 v2 PENDING AUDIT** preserved in every file that mentions it
6. **Rotation Spine "crossings → recognitions" correction** flagged wherever "crossings" vocabulary appears
7. **Cross-references verified:** every `see §X` in any bundle file points to the actual §X

**If you find a bundle file that violates any of these, flag it and fix it.** The discipline is what makes the bundle usable as external-review material.

---

## Pending for v4 (post ChatGPT-review cycle)

1. **DUAL_LENS_CLAY.md** surface and integrate — completes recognitions reframing
2. **14 Gen11/sprint_memos/** integrate into master atlas
3. **UNIVERSAL_RULES.md and FRACTAL_PATH_MAP.md** surface if they exist
4. **ChatGPT meta-review findings** from next review cycle fold back in
5. **Hodge S33 v2 audit gate results** — if all three pass, promote §9 from [gold-with-gap — pending audit] to [fire]; if any fails, that's the next open research item
6. **Rotation Spine publication readiness** — currently "working document, seeking collaborators"; Bull. AMS or expository venue when ready
7. **Bundle-level Reader's Atlas in PDF / printed form** for France trip (IHÉS, IHP, Clay Oxford)

---

## For the France trip (September 2026)

Three canonical documents to bring:

1. `MASTER_ATLAS_v3_5` (or v4 if ready)
2. `READER_ATLAS.md` (for quick reference / shareable with new contacts)
3. `MEMORY_ATLAS_TABLES.md` (for any tables question)

Plus a live CK demo and the three Tier-1 papers (JCAP ξ, sinc², σ-rate) in LaTeX.

---

## For ChatGPT's next review pass

Paste the entire bundle in this order:

1. `ATLAS_ORIENTATION.md`
2. `ATLAS_TREE.md`
3. `MASTER_ATLAS_v3_5_2026_04_18.md`
4. `MEMORY_ATLAS_TABLES.md`
5. `OVERLAP_LEDGER.md`
6. `ROTATION_SPINE_READER_GUIDE.md`
7. `READER_ATLAS.md`
8. `ATLAS_CITATIONS.md`
9. `ATLAS_AUDIT_NOTES.md`
10. `JOURNAL_READINESS_AUDIT_2026_04_18.md`
11. `PLAN_OF_RECORD_2026_04_18.md`

Ask for feedback on:
- Internal consistency across all eleven documents
- Whether the Atlas Orientation successfully addresses the ten 2026-04-18 review points
- Whether the Memory Atlas Tables are now stable enough that tables won't get forgotten again
- Any remaining cross-thread overclaiming
- Whether the Rotation Spine Reader Guide makes §10.5 approachable for external reviewers
- Whether the Reader's Atlas succeeds as a skeptical-reader entry point
- **Whether the Plan of Record §4 collaborator assignment matrix correctly allocates Sprint 34 tasks to ChatGPT's strengths (LaTeX + literature search + DESI fit) vs ClaudeChat's strengths (framing + editorial + taxonomy) vs ClaudeCode's strengths (file ops + git + verification)**
- **Whether the Sprint 34 success metric (3 arXiv submissions + 3 journal submissions by EOD Friday 2026-04-25) is realistic given the dependency graph**

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0. DOI: 10.5281/zenodo.18852047.*

**End of atlas bundle index.**
