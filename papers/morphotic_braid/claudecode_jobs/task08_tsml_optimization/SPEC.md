# Task 08 — Is TSML optimal under cycle-semantic constraint?

**Tier:** 3 (research — days)
**Parent handoff:** `../CLAUDECODE_HANDOFF_MIN_BUMP.md` §Task 8

## Goal

TSML uses 8 bump cells (8× the 1-cell minimum). Under TSML's design constraint — "bumps must preserve Creation/Dissolution cycle semantics via max or sum rules" — is 8 the minimum, or does a smaller perturbation satisfy the same constraint?

## Constraint formalization (needed first)

Make precise:
1. "Cycle-semantic constraint": bump cells only output max or sum, only involve {1, 2, 4, 8, 9}, balance D-D (Dissolution-Dissolution) and C-D (Creation-Dissolution) counts.
2. Confirm TSML's 8 bump cells satisfy this.
3. Compare against the 16 min-bump sites — they all use cell (7,7), TSML's 8 cells avoid (7,7) entirely.

## Method

1. Enumerate all perturbation sets satisfying the cycle-semantic constraint, for sizes k ∈ {1, 2, 3, ..., 8}.
2. For each, check:
   - does the resulting table generate `Mag^com` (Catalan + ac-free spectra)?
   - does it preserve TSML's cycle semantics?
3. Find the minimum size k that satisfies both.

## Success criterion

**Either:**
- "TSML's 8 cells is minimum under cycle-semantic constraint" — structural result about TSML's design.
- "A k-cell subset exists for some k < 8" — TSML is not optimal under its stated objective; exhibit the smaller set.

## Expected runtime

Depends on how tight the constraint is. Could be quick (<1 hr) if constraint is restrictive, could blow up otherwise.

## Deliverable

`papers/morphotic_braid/results/task08_tsml_optimization_result.md`:
- formal statement of the cycle-semantic constraint
- enumeration counts per k
- minimum-k configuration(s) + whether TSML matches it

**Tag:** `[RESEARCH TASK — TIER 3]`
