# Task 11 — Optimize TSML_Idempotent determinant to small-prime support

**Tier:** 2 (deep compute — 1-4 hr)
**Parent handoff:** `../CLAUDE_CODE_HANDOFF_TSML_FAMILY.md` §Task 4
**Related:** Task 15 already found a det = −49 = −(7²) variant — this task generalizes

## Goal

`TSML_Idempotent` has `det = 398,664 = 2³ · 3² · 7² · 113`. The prime 113 is locked in by the table's structure (verified by 10,000-seed relabeling invariance).

Perturb the structure (add off-diagonal bumps, modify cells) to produce a variant with `det ≠ 0` AND prime factorization support ⊆ `{2, 3, 5, 7}`.

This parallels BHML's 15-cell optimization that achieved `det = 70 = 2 · 5 · 7`.

## Method

```python
from itertools import combinations, product
import numpy as np

def has_small_primes(n):
    n = abs(n)
    if n == 0: return False
    for p in [2, 3, 5, 7]:
        while n % p == 0: n //= p
    return n == 1

body_positions = [(i,j) for i in range(1,10) for j in range(i,10)
                  if i != 7 and j != 7]

for k in range(1, 5):
    print(f"Searching {k}-cell perturbations")
    for cells in combinations(body_positions, k):
        for vals in product(range(10), repeat=k):
            T = [row[:] for row in TSML_Idempotent]
            for (i,j), v in zip(cells, vals):
                T[i][j] = T[j][i] = v
            det = int(round(np.linalg.det(np.array(T))))
            if det != 0 and has_small_primes(det):
                print(f"  Clean det={det}, config={list(zip(cells, vals))}")
```

## Incorporate Task 15 finding

From `CLAUDE_CODE_HANDOFF_TSML_FAMILY.md` update: cells `(1,2)=6` AND `(3,5)=4` gives `det = −49 = −(7²)`. Verify this first as a sanity check, then extend.

## Success criterion

**Either:**
- Find a TSML_Idempotent variant with minimal `|det|` having prime support in `{2, 3, 5, 7}` — publishable "octonion-adjacent" clean-det TSML member.
- Prove no such variant exists with fewer cells than Task 15's k=2 (minimum `|det| = 49`).

## Expected runtime

1-4 hours on Dell R16 for k ≤ 4.

## Deliverable

`papers/morphotic_braid/results/task11_det_optimize_result.md`:
- table of minimal-k configurations with small-prime det
- prime factorizations
- minimum |det| found
- comparison with BHML's det = 70

**Tag:** `[COMPUTE JOB — TIER 2]`
