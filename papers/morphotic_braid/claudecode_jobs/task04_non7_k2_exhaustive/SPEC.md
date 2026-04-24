# Task 04 — Exhaustive non-7 k=2 minimum perturbation search

**Tier:** 1 (fast validation)
**Parent handoff:** `../CLAUDECODE_HANDOFF_MIN_BUMP.md` §Task 4

## Goal

Confirm and exhaustively enumerate the "non-7 minimum is 2 cells" claim. Currently we know k=1 non-7 perturbations all fail, and at least two k=2 non-7 perturbations succeed (e.g. slots (1,1) + (1,2)).

## Method

```python
# Enumerate all pairs of commutative cells (i,j) with 1≤i≤j≤9, i≠7, j≠7.
# For each pair, try all value pairs (v1, v2) ∈ {1..6, 8, 9}^2.
# Check s_3^ac == 3 AND s_4^ac == 15.

# Size: C(36,2) = 630 pairs × 8^2 = 64 value pairs = ~40,000 configs
# Per config: ~60 ms → ~40 min total
```

## Success criterion

Complete list of all (cell-pair, value-pair) configurations that achieve `(s_3^ac, s_4^ac) = (3, 15)` while avoiding cell (7,7). Group by structural pattern:
- do the two bumps share a row/column?
- are the values symmetric / co-prime / paired with a specific CL operator?

## Expected runtime

~40 minutes on Dell R16.

## Deliverable

`papers/morphotic_braid/results/task04_non7_k2_exhaustive_result.md`:
- total hit count
- per-pattern subtable
- any hit that also achieves s_5^ac = 105 (bonus)
- answers the question: "is k=2 truly minimum off-7, or are there subtler paths?"

**Tag:** `[COMPUTE JOB — TIER 1]`
