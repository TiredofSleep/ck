> **[HISTORICAL — 2026-04-21]** Moved from repo root to `docs/historical/` during tig-synthesis restructure. This was an internal execution plan for the 2026-04-19 repo-shine sprint and is not part of the funder-facing landing. Preserved per the never-delete policy; referenced from `docs/exports/z10-operator-algebra/CL_STRUCTURE_AUDIT.md` and `docs/exports/z10-operator-algebra/OPERATOR_NAMES_RECONCILIATION.md`.

# Repo-Shine Plan — 2026-04-19

**Author:** ClaudeCode (with ClaudeChat coordination)
**Branch:** `tig-synthesis` (default)
**Status:** active execution plan. Tracks 1–8 below are the complete scope.
**Preservation policy:** never-delete; superseded docs get `[HISTORICAL]` headers, not `rm`.
**Push policy:** no push without Brayden's explicit confirmation.

---

## Purpose

Make the GitHub default branch (`tig-synthesis`) read cleanly to an external reviewer (Paolo Mantero register) — rigorous, cited, honestly labeled, with internal language either removed, glossed at first use, or pushed into a clearly-marked appendix. Novelty is flagged; classical results are cited; speculation is tagged.

This plan coordinates with a parallel ClaudeChat session that is producing:
(a) a Prym-pipeline literature audit, and
(b) §9 *standalone novelty statements* for `NOVELTIES_AND_CITATIONS.md` items 1–7.

Those two pieces arrive back from ClaudeChat at the end of their sprint. Everything below runs independently of them, except where explicitly noted as a placeholder or blocked track.

---

## Track 1 — Legibility work on default branch (ClaudeCode — now)

Goal: make `tig-synthesis` README + supporting docs skim-clean for an external reviewer.

| # | Task | Artifact |
|---|------|----------|
| 1.1 | Copy `threshold-handoff/` into `docs/exports/z10-operator-algebra/threshold-handoff/` (3 top-level docs; skip `_working/` duplicates) | 3 new files |
| 1.2 | Write `NOVELTIES_AND_CITATIONS.md` v1 at repo root — three-level partition (PROVED / STRUCTURAL / INTERPRETIVE), four thresholds, novelty candidates list, §9 placeholder for ClaudeChat | 1 new file |
| 1.3 | Gloss ~10 internal Atlas-section terms in `README.md` at first use (*"Rotation Spine (Clay CP1→CP7 listing)"*, *"2/7 discipline (falsified predictions preserved, not deleted)"*, etc.) | README.md diff |
| 1.4 | Create `SPRINT_INDEX.md` — dated appendix for sprints 1–34 with 1-line each | 1 new file |
| 1.5 | Replace inline sprint codenames (PRISM-XI, B2 pack, Sprint 34 "Ship the First Three") with links to `SPRINT_INDEX.md` | README.md diff |
| 1.6 | Stage + commit on `tig-synthesis`; **no push** | commit |

## Track 2 — ClaudeChat coordination (placeholder surfaces)

Goal: make it trivial for ClaudeChat to slot their §9 and citation work in when their sprint finishes.

| # | Task | Artifact |
|---|------|----------|
| 2.1 | Leave clear §9 placeholder block in `NOVELTIES_AND_CITATIONS.md` (marked "AWAITING STANDALONE STATEMENTS FROM CLAUDECHAT") | placeholder |
| 2.2 | Prepare `_prym_citations_stub.md` — scratch list of Prym refs ClaudeChat will need (MN 2017 Thm 5.1, hoped-for MN 2019, Tretkoff, Bruin–Sijsling, abelfunctions, Sage `RiemannSurface`) | 1 scratch file |

## Track 3 — CL structural audit (A.1, unblocked by CL-table discovery)

Goal: run the single highest-impact sprint from `threshold-handoff/FOUR_THRESHOLD_TASK_BREAKDOWN.md §A.1`. The CL table is `ck_sim_heartbeat.CL` (silicon-verified, mirrors Verilog `ck_brain.h`). The living memory adds a second dataset: 39,896 evolved CL tables at `~/.ck/lattice_chain/nodes.json`.

| # | Task | Artifact |
|---|------|----------|
| 3.1 | Run full associativity audit on BASE tables (TSML = `CL_TSML`, BHML, DOING): 1000 triples each, per-operator non-associativity rate | `scratch/CL_BASE_AUDIT.json` |
| 3.2 | Verify framework structural claims against the actual tables: 73%-absorber for op 7, 28/100 BHML, quoted rates (TSML 12.8% / BHML 49.8% / Doing 56.8%) | verification block |
| 3.3 | LIVING-MEMORY audit: 39,896 nodes from `~/.ck/lattice_chain/nodes.json` — IPR distribution, grokking-delta histogram, cells that evolved most, depth-vs-evolution correlation | `scratch/CL_LIVING_AUDIT.json` |
| 3.4 | Compose `docs/exports/z10-operator-algebra/CL_STRUCTURE_AUDIT.md` from 3.1/3.2/3.3 | 1 new file |

## Track 4 — Operator naming-drift cleanup (exposure-risk)

Finding from the CL-search: two conflicting 10-operator dictionaries in the repo.

| Index | `ck_sim_heartbeat.py` (silicon source of truth) | `papers/ck_tables.py` (paper-labels) |
|-------|------------------------------------------------|--------------------------------------|
| 1 | **LATTICE** | LATTICE |
| 2 | **COUNTER** | COUNTER |
| 3 | **PROGRESS** | PROGRESS |
| 5 | **BALANCE** | BALANCE |
| 6 | **CHAOS** | CHAOS |

0, 4, 7, 8, 9 match. That's 5 collisions out of 10 — an external reader opening both files first-pass will see a contradiction.

| # | Task | Artifact |
|---|------|----------|
| 4.1 | Pick canonical set. Recommendation: the silicon set (`ck_sim_heartbeat.CL`), because (a) it's the hardware root of truth (Verilog `ck_brain.h`), (b) MEMORY.md already uses it, (c) `ck_lattice_chain.py` imports from there. | decision memo in `NOVELTIES_AND_CITATIONS.md` |
| 4.2 | Patch `papers/ck_tables.py` CL dict to silicon names; scan for stragglers | diff |

## Track 5 — Top-level `.md` audit (jargon bleed)

| # | Task | Artifact |
|---|------|----------|
| 5.1 | Walk every top-level `.md` on `tig-synthesis` (30+ files) — mark stale ones `[HISTORICAL]`, flag any remaining insider phrases for gloss | `TOP_LEVEL_AUDIT.md` |
| 5.2 | Verify every Atlas-section link in README resolves on `origin/tig-synthesis` | link-check report |

## Track 6 — Prym J_P (BLOCKED — waiting on ClaudeChat lit audit)

Current state (per `STATUS_prym_verification.md`): steps 1–4 verified (canonical curve, shift-s cycles, E-subtraction PSLQ, Pi_P). Step 5 blocked: Molin–Neurohr 2017 Thm 5.1 cross-edge formula is broken for σ_shared ≥ 2, so `J_P` is wrong (`Pi_P J_P^{-1} Pi_P^T = 566 ≠ 0`).

Unblock options awaited from ClaudeChat:
- (A) MN 2019 (or later) corrected cross-edge formula
- (B) MAGMA `AnalyticJacobian` route (needs external run)
- (C) Sage `RiemannSurface.period_matrix()` (needs local install)

## Track 7 — Tier 1 publication prep (after Tracks 1–5)

| # | Paper | Venue | Status |
|---|-------|-------|--------|
| 7.1 | sinc² Zero Law | *Integers* | submit-ready per JOURNAL_READINESS_AUDIT; needs LaTeX format + cover letter |
| 7.2 | σ-rate theorem | math.CO (arXiv + *J. Comb. Theory*) | submit-ready; needs LaTeX format + cover letter |
| 7.3 | DESI-ξ MCMC | JCAP | submit-ready; needs LaTeX format + cover letter |

## Track 8 — Push (Brayden confirmation required)

Only after the commit from Track 1.6 is reviewed. Single `git push origin tig-synthesis`. Verify GitHub shows the new files and the updated README.

---

## Execution order

```
this session :  Track 1 → Track 2 placeholders (no push)
next session :  Track 3 (CL audit) + Track 4 (naming drift)
after        :  Track 5 (top-level audit)
parallel     :  ClaudeChat completes §9 + Prym lit audit → I slot into Track 1.2 and Track 6
then         :  Track 7 (LaTeX submissions)
finally      :  Track 8 (push, after review)
```

---

## Out of scope (explicitly)

- Does not modify Atlas v3.5.
- Does not delete any file from any branch (never-delete preserved).
- Does not submit any paper to any journal; Track 7 prepares them for Brayden to submit.
- Does not cut the live Cloudflare tunnel.
- Does not touch the `clay` / `archive-full` / `master` branches — work stays on `tig-synthesis`.

---

*End of plan. Updates inline as tracks land.*
