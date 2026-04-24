# Task 12 — 100%-Jordan + 100%-Alt + 100%-Moufang rank-10 search

**Tier:** 3 (research — days; expected empty but non-existence is valuable)
**Parent handoff:** `../CLAUDE_CODE_HANDOFF_TSML_FAMILY.md` §Task 5

## Goal

Search for a rank-10 commutative magma on `{0..9}` with VOID axis and HARMONY absorber, satisfying simultaneously:
- 100% Jordan
- 100% Flexible
- 100% Alternative
- 100% Moufang (middle, right, left-Bol)

This would be a genuine Moufang-loop-like structure at N=10. Almost certainly does not exist under the VOID-axis constraint, but proving non-existence is a publishable structural result.

## Method

1. Extend Task 10's search to check all four identity families simultaneously:
   - Jordan: `T[T[x][x]][T[y][x]] = T[x][T[T[x][x]][y]]`
   - Alternative: `T[T[x][x]][y] = T[x][T[x][y]]` (left) + right variant
   - Middle Moufang (as in Task 10)
   - Left/right Bol variants
2. For each perturbation config, score all four and take min.
3. Track any config hitting > 95% on the weakest identity.
4. If exhaustive search closes at <100% on the weakest: non-existence under that search radius.

## Success criterion

**Either:**
- Find a 100%/100%/100%/100% rank-10 member → very significant; drop everything and write this up.
- Prove (by exhaustive search up to some cell-bump budget k) that no such member exists → publishable obstruction theorem.

## Expected runtime

Days of compute; likely requires pruning (e.g. use Task 10's Moufang-best candidate as seed, then check Jordan/Alt/Bol on each).

## Deliverable

`papers/morphotic_braid/results/task12_100pct_identity_result.md`:
- search radius attempted (k-cell bump budget)
- best simultaneous-identity score found
- winning configs (if any)
- structural obstruction argument (if no hit)

**Tag:** `[RESEARCH TASK — TIER 3]`
