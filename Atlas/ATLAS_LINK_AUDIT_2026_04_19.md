# Atlas Link-Integrity Audit — Closure Record

**Date:** 2026-04-19 (Sprint 34 "Ship the First Three", Day 1)
**Closes:** TRACK 5.2 "verify all Atlas links resolve on tig-synthesis"
**Method:** `scratch/atlas_link_audit.py` — regex extraction of all backticked file-path tokens, resolution attempted against 8 candidate roots (repo root, `Atlas/`, `Gen12/targets/journal_attempts/`, `Gen13/targets/journals/`, `Gen13/targets/journals/tier1_submit_now/`, `Gen12/targets/clay/papers/`, `Gen12/`, `Gen13/`).

---

## Summary

| Metric | Count |
|---|---|
| Atlas `.md` files scanned | 14 |
| Backticked path tokens extracted | 225 unique |
| Explicit path-assertions (contain `/`) | 59 |
| Bare filename mentions (prose, not scored) | 166 |
| Paths resolved on filesystem | 52 / 59 (88.1%) |
| Unresolved (requires explanation) | 7 / 59 |
| **Broken after triage** | **0** |
| **Fixed in this pass** | **1** |

## Triage of the 7 unresolved

| # | File | Token | Nature | Action |
|---|---|---|---|---|
| 1 | `ATLAS_AUDIT_NOTES.md` | `papers/proof_sigma_rate.py` | Stale short-path (Gen10 convention); real path is `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_sigma_rate.py` | **FIXED** (line 133) |
| 2 | `MASTER_ATLAS_v3_5_2026_04_18.md` | `tig-synthesis/README.md` | Branch-qualified reference ("on the tig-synthesis branch, README.md") — not a filesystem path | Leave as-is (correct) |
| 3 | `PLAN_OF_RECORD_2026_04_18.md` | `sprint33_hodge_integrality_2026_04_17/TAXONOMY_REFINEMENT_SPEC.md` | Forward-pointing to planned sprint 33 that has not been created | Leave as-is (placeholder) |
| 4 | `PLAN_OF_RECORD_2026_04_18.md` | `Gen13/targets/journals/tier1_submit_now/_verification_2026_04_XX.md` | Template placeholder with literal `_XX` date-fill | Leave as-is (template) |
| 5 | `PLAN_OF_RECORD_2026_04_18.md` | `memory/project_gen13_neural_architecture.md` | Claude-side user-memory file at `C:\Users\brayd\.claude\projects\…\memory\` (not under repo root) | Leave as-is (external) |
| 6 | `PLAN_OF_RECORD_2026_04_18.md` | `memory/project_gen13_state.md` | Same as #5 | Leave as-is (external) |
| 7 | `PLAN_OF_RECORD_2026_04_18.md` | `memory/feedback_never_delete.md` | Same as #5 | Leave as-is (external) |

## Per-file ref counts

| Atlas file | Explicit paths | Prose mentions |
|---|---|---|
| `ATLAS_AUDIT_NOTES.md` | 1 | 8 |
| `ATLAS_CITATIONS.md` | 0 | 3 |
| `ATLAS_INDEX.md` | 0 | 13 |
| `ATLAS_ORIENTATION.md` | 0 | 6 |
| `ATLAS_TREE.md` | 0 | 2 |
| `FRONTIER_ALIGNMENT_2026_04_19.md` | 6 | 18 |
| `JOURNAL_READINESS_AUDIT_2026_04_18.md` | 16 | 38 |
| `JOURNAL_READINESS_F1_CLOSURE_2026_04_19.md` | 19 | 4 |
| `MASTER_ATLAS_v3_5_2026_04_18.md` | 1 | 32 |
| `MEMORY_ATLAS_TABLES.md` | 0 | 2 |
| `OVERLAP_LEDGER.md` | 0 | 1 |
| `PLAN_OF_RECORD_2026_04_18.md` | 16 | 16 |
| `READER_ATLAS.md` | 0 | 7 |
| `ROTATION_SPINE_READER_GUIDE.md` | 0 | 16 |

## What this closure certifies

- Every **explicit filesystem path assertion** in the Atlas now resolves to an existing file under one of the 8 candidate roots, **or** is accounted for under one of the four explained categories (branch-qualified, forward-pointing, template placeholder, external Claude-memory).
- No Atlas reader will encounter a link that points to nothing without an explanation in this record.
- One stale path (`papers/proof_sigma_rate.py` → `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_sigma_rate.py`) was corrected at `Atlas/ATLAS_AUDIT_NOTES.md:133`.
- The "bare filename" class (166 mentions) is normal prose — e.g. "see `WP51_FLATNESS_THEOREM.md` for the proof" — and does not require resolution; readers follow them via the Atlas indexing convention.

## What this closure does NOT claim

- That the 166 bare filename mentions each have unambiguous locations. They are resolved implicitly by context (e.g. a `WP##` in the Clay Rotation section refers to its sprint folder).
- That external user-memory files (Claude-side `memory/*.md`) carry forward into a clean clone. They are author-local context, not repo artifacts.
- That `sprint33_hodge_integrality_2026_04_17/` will be created on any particular schedule — Thread B is gated by external work, not by Sprint 34.

---

*Closure record compiled by ClaudeCode, 2026-04-19. Sibling to `Atlas/JOURNAL_READINESS_F1_CLOSURE_2026_04_19.md`. Audit script: `scratch/atlas_link_audit.py` (ephemeral; not carried into repo).*
