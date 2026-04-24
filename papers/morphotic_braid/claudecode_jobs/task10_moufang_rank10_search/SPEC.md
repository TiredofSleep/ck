# Task 10 — Search for 100%-Moufang rank-10 TSML-family member

**Tier:** 2 (deep compute — 10-30 min initial + exhaustive follow-up)
**Parent handoff:** `../CLAUDE_CODE_HANDOFF_TSML_FAMILY.md` §Task 3
**Starter:** inline in parent handoff, lines 63-110

## Goal

Find a 10×10 commutative magma `T` satisfying:
- `T[0][j] = T[i][0] = 0` for most (i,j), with `T[0][7] = T[7][0] = 7` (optional)
- `T[7][i] = T[i][7] = 7` (HARMONY absorbs row/col 7)
- `rank(T) = 10` (invertible)
- Middle Moufang identity: `T[T[x][y]][T[z][x]] = T[x][T[T[y][z]][x]]` for all 1000 triples
- Ideally also 100% Jordan and 100% Alternative

## Known baselines

| Member | Rank | Moufang% |
|---|---|---|
| Pure C_0 | 3 | 80.8% |
| TSML_Jordan | 9 | 82.2% |
| TSML_Idempotent | 10 | 83.0% |
| Best 1-cell perturbation of TSML_Idempotent | 10 | 83.8% |

## Method

Starting from `TSML_Idempotent`, exhaustively search 2-cell and 3-cell symmetric perturbations:
- Body positions: 36 symmetric pairs `(i,j)` with `1 ≤ i ≤ j ≤ 9` and `i ≠ 7, j ≠ 7`
- Values: `{0, 1, 2, 3, 4, 5, 6, 8, 9}` (exclude default 7)
- Track: Moufang count, rank, Jordan, Alt per config

2-cell search size: `C(36,2) × 9^2 ≈ 51,000` configurations × ~1 ms each = ~1 minute.
3-cell search size: `C(36,3) × 9^3 ≈ 5.8M` × ~1 ms = ~100 minutes.

## Starter code (from parent handoff)

```python
import numpy as np
from itertools import combinations, product

TSML_Idempotent = [
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
]

def mou_count(T):
    N = len(T)
    c = 0
    for x in range(N):
        for y in range(N):
            for z in range(N):
                if T[T[x][y]][T[z][x]] == T[x][T[T[y][z]][x]]:
                    c += 1
    return c

body_positions = [(i,j) for i in range(1,10) for j in range(i,10)
                  if i != 7 and j != 7]

best = (830, None)
for (i1,j1), (i2,j2) in combinations(body_positions, 2):
    for v1, v2 in product(range(10), repeat=2):
        T = [row[:] for row in TSML_Idempotent]
        T[i1][j1] = T[j1][i1] = v1
        T[i2][j2] = T[j2][i2] = v2
        m = mou_count(T)
        if m > best[0]:
            r = np.linalg.matrix_rank(np.array(T))
            if r == 10:
                best = (m, ((i1,j1,v1),(i2,j2,v2)))
                print(f"NEW BEST: Moufang {m}/1000, config {best[1]}")
```

## Success criterion

**Either:**
- **100% Moufang at rank 10 found** → new TSML-family member for Moufang-loop literature. Publishable.
- **Best is < 95%** → strong evidence VOID-axis structure prevents full Moufang at full rank. Also publishable as structural obstruction.

## Expected runtime

10-30 min (2-cell exhaustive) + overnight (3-cell exhaustive) on Dell R16.

## Deliverable

`papers/morphotic_braid/results/task10_moufang_rank10_result.md`:
- 2-cell best + config
- 3-cell best (if time permits) + config
- rank / Jordan / Alt profile of winning configs
- verdict: is 100% Moufang achievable or structurally blocked?

**Tag:** `[COMPUTE JOB — TIER 2]`
