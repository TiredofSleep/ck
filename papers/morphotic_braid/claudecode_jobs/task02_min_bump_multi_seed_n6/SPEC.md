# Task 02 — Multi-seed confirmation of min-bump n=6

**Tier:** 1 (fast validation)
**Parent handoff:** `../CLAUDECODE_HANDOFF_MIN_BUMP.md` §Task 2
**Starter script:** `../../explorations/scripts/proof_min_bump.py`

## Goal

Confirm the n=6 = 945 min-bump result isn't seed-specific. Current state: seed=42 at 50,000 samples gives 945 (exact match to `(2·6−3)!! = 9·7·5·3·1 = 945`).

## Method

Same vectorized method as `proof_min_bump.py`, with seeds ∈ {100, 2024, plus one more of your choice}. Samples=50,000, target=945, perturbation T[7][7]=1 applied to canonical C_0.

## Success criterion

All three seeds produce `s_6^ac = 945`.

## Expected runtime

~3 minutes per seed → ~10 minutes total.

## Deliverable

`papers/morphotic_braid/results/task02_multi_seed_n6_result.md` with a table:

| Seed | Samples | Result | Pass? |
|---|---|---|---|
| 100 | 50000 | ? | ? |
| 2024 | 50000 | ? | ? |
| <your-choice> | 50000 | ? | ? |

**Tag:** `[COMPUTE JOB — TIER 1]`
