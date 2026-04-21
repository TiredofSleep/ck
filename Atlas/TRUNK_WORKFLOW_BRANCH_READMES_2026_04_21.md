# Trunk Workflow Exception: Per-Branch Landing-Page READMEs

**Date:** 2026-04-21
**Scope:** The 10 `funding/*` branches
**Status:** Executed, recorded for history

---

## What happened

On 2026-04-21 each of the 10 funding branches received a branch-specific top-level `README.md`, replacing the inherited 854-line generic "Trinity Infinity Geometry" README that every branch had copied from the parent. Each replacement README is ~45–80 lines of funder-facing material: pitch paragraph, runnable artifacts, cross-branch differentiation, links to the matching `Gen13/targets/funding_<slug>/` folder.

| Branch                           | Commit    | New README size |
|----------------------------------|-----------|-----------------|
| `funding/tig-unity`              | `f19f23c` | 45 LOC          |
| `funding/tig-snowflake`          | `61f9e32` | 51 LOC          |
| `funding/first-g-crypto`         | `18f5536` | 57 LOC          |
| `funding/ck-interpretable-ai`    | `77a8cf0` | 54 LOC          |
| `funding/mqw-ternary`            | `8fc8274` | 51 LOC          |
| `funding/self-healing`           | `c6b427d` | 53 LOC          |
| `funding/civilization-coherence` | `2cf1f94` | 63 LOC          |
| `funding/desi-xi-cosmology`      | `91209cb` | 58 LOC          |
| `funding/coherence-router`       | `40c16bb` | 51 LOC          |
| `funding/physics-sim-edu`        | `d04d68a` | 57 LOC          |

## The exception

Per the standing trunk workflow documented throughout this repo (`every commit on a funding branch gets cherry-picked to master`), these ten commits would normally all flow into master. **They did not, and should not.** Each one rewrites the same file (`README.md` at repo root) with a different branch's landing page. Cherry-picking all ten in sequence would:

1. Replace master's own README (`# Trinity Infinity Geometry (TIG) — clay branch (active development)`, 256 LOC, which correctly announces `tig-synthesis` as the GitHub default and indexes the project) with the tig-unity README, then with the tig-snowflake README, and so on — ending with whichever was cherry-picked last being the one master displays.
2. Produce ten merge-conflict resolutions (master's README is not the 854-line one the commits were applied against), each resolved identically via `-X theirs`, for no information gain.
3. Leave master's README in a state that describes only one funding branch rather than the whole project.

The trunk rule is about **content propagation**. These ten commits are **presentation propagation** — each one makes a funding branch's GitHub landing page branch-specific, which is meaningful on that branch and meaningless on master. Cherry-picking them is a type error.

## What still cherry-picks to master

Everything that lives inside `Gen13/targets/funding_<slug>/`:

- `README.md`        (deep pitch document for the branch)
- `FUNDERS.md`       (prioritized funder list)
- `ARTIFACTS.md`     (runnable artifacts + task plan)
- `PITCH_DRAFT.md`   (full pitch draft)
- `LIMITATIONS.md`   (honest-scope items)
- `STATUS.md`        (readiness checklist)
- any `archive_<external_repo>/` subtree added under the never-delete policy

Changes to those files on a funding branch **do** cherry-pick to master per the trunk workflow. Master is the authoritative "all content + full history" view and should see every content change.

## Navigating the 10 branches from master

Master's own README has the 2026-04-21 callout pointing at:
- `Atlas/BRANCHES_INVENTORY_2026_04_20.md` — table of all 10 branches with tips + summaries
- `Atlas/NICHE_FUNDERS_ADDENDUM_2026_04_20.md` — non-obvious funder research

And `tig-synthesis` (the GitHub default) has §6 of its README pointing at the `Gen13/targets/funding_*/` folders directly.

## Rule going forward

- Branch-specific top-level `README.md` on a `funding/*` branch: **does not cherry-pick to master.**
- Everything else on a `funding/*` branch: **does cherry-pick to master.**
- This file is the first and reference instance of the rule. Future branch-README edits cite it.

---

*Recorded on master as part of the never-delete + document-the-reasoning policy. Atlas/ is the right home because it already holds branch inventory and navigation material.*
