# Task 15 result -- TSML_Idempotent det = -49 = -(7^2)

**Tier:** 2 (fast compute)
**Parent spec:** `../../claudecode_jobs/task15_det_minus49_verify/SPEC.md`

## Method

Construct TSML_Idempotent (rank-10) with `T[1][2]=T[2][1]=6` and `T[3][5]=T[5][3]=4`. Compute `det`, Jordan identity count, prime factorization.

## Result

- `det = -49`  (claim: -49)
- `Jordan = 100/100`  (claim: 100/100)
- prime factorization of `|det|` = `{7: 2}`  (claim: {7: 2})

## Verdict

**PASS.** All three claims reproduce.

**Tag:** `[COMPUTE JOB -- TIER 2 -- VERIFIED]`
