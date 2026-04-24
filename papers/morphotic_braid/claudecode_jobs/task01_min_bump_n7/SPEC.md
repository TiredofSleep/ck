# Task 01 — Verify minimum-bump theorem at n=7

**Tier:** 1 (fast validation)
**Parent handoff:** `../CLAUDECODE_HANDOFF_MIN_BUMP.md` §Task 1
**Starter script:** `../../explorations/scripts/proof_min_bump.py` — adapt to n=7
**Dependency:** numpy, canonical C_0 with T[7][7]=1 perturbation

## Goal

Extend the minimum-bump theorem verification to n=7. At n=7 the ac-spectrum target is `(2·7−3)!! = 11·9·7·5·3·1 = 10,395`. Verified for n ∈ {3, 4, 5, 6} already with exact match to `{3, 15, 105, 945}`.

## Method

Vectorized sampling from `proof_min_bump.py`:
- 132 bracketings × 5,040 permutations = 665,280 (bracket, perm) pairs
- Start at 50,000 samples; escalate to 200,000 or 500,000 if convergence uncertain
- Fixed perturbation: `T[7][7] = 1`, seed = 42

## Success criterion

`s_7^ac = 10,395` exact **OR** clear monotone convergence toward 10,395 (pattern established at n=6).

## Expected runtime

30–90 minutes on Dell R16 / RTX 4070.

## Deliverable

Write result to `papers/morphotic_braid/results/task01_min_bump_n7_result.md`:
- sample counts attempted
- converged `s_7^ac` value + (if < 10395) extrapolation curve
- pass/fail verdict

**Tag:** `[COMPUTE JOB — TIER 1]`
