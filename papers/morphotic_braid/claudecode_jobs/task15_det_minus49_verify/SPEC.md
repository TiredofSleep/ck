# Task 15 — Verify the det = −49 = −(7²) TSML_Idempotent variant

**Tier:** 2 (fast compute — <5 min)
**Parent handoff:** `../CLAUDE_CODE_HANDOFF_TSML_FAMILY.md` §Update (2026-04-23 final session) "Finding A"

## Goal

Claim: `TSML_Idempotent` with cells `(1,2) = 6` and `(3,5) = 4` (symmetric, so `(2,1) = 6` and `(5,3) = 4` also) produces:
- 100% Jordan identity
- `det = −49 = −(7²)`
- prime set: `{7}` only

Verify this directly.

## Method

```python
import numpy as np

TSML_Idempotent = np.array([
    [0,0,0,0,0,0,0,7,0,0],
    [0,1,7,7,7,7,7,7,7,7],
    [0,7,2,7,7,7,7,7,7,7],
    [0,7,7,3,7,7,7,7,7,7],
    [0,7,7,7,4,7,7,7,7,7],
    [0,7,7,7,7,5,7,7,7,7],
    [0,7,7,7,7,7,6,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,9],
])

T = TSML_Idempotent.copy()
T[1][2] = T[2][1] = 6
T[3][5] = T[5][3] = 4

det = int(round(np.linalg.det(T)))
print("det =", det)  # expect -49

# Jordan identity count
def jordan_count(T):
    N = len(T)
    c = 0
    for x in range(N):
        for y in range(N):
            # Jordan: (x² · y) · x = x² · (y · x)
            xx = T[x][x]
            lhs = T[T[xx][y]][x]
            rhs = T[xx][T[y][x]]
            if lhs == rhs:
                c += 1
    return c, N*N

j, tot = jordan_count(T)
print(f"Jordan: {j}/{tot}")  # expect 100/100

# prime factorization
def factor(n):
    from sympy import factorint
    return factorint(abs(n))
print("prime factorization of |det|:", factor(det))  # expect {7: 2}
```

## Success criterion

All three claims reproduce:
- `det == -49`
- Jordan = 100/100
- prime set of |det| = {7}

## Expected runtime

<5 minutes.

## Deliverable

`papers/morphotic_braid/results/task15_det_minus49_result.md`:
- det value
- Jordan tally
- prime factorization
- verdict (PASS / FAIL)

**Tag:** `[COMPUTE JOB — TIER 2]`
