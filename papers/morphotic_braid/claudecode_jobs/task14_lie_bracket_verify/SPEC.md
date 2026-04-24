# Task 14 — Verify [M_TSML_Jordan, M_TSML_Idempotent] is exactly antisymmetric

**Tier:** 2 (fast compute — <5 min)
**Parent handoff:** `../CLAUDE_CODE_HANDOFF_TSML_FAMILY.md` §Update (2026-04-23 final session) "Finding B"

## Goal

The packet's final-session finding claims:

> "The commutator `[M_TSML_Jordan, M_TSML_Idempotent]` where `M_*[i,j] := TSML_*[i,j]` as a 10×10 matrix, is **exactly antisymmetric** (pure Lie bracket — no symmetric residue)."

Verify this directly against canonical `papers/ck_tables.py` (TSML_Jordan = canonical TSML; TSML_Idempotent defined in `CLAUDE_CODE_HANDOFF_TSML_FAMILY.md` lines 69-80).

## Method

```python
import numpy as np
from papers.ck_tables import TSML as TSML_Jordan

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
TJ = np.array(TSML_Jordan)
TI = TSML_Idempotent

C = TJ @ TI - TI @ TJ              # commutator
sym = (C + C.T) / 2                # symmetric part
antisym = (C - C.T) / 2            # antisymmetric part

print("commutator:\n", C)
print("symmetric part (should be zero):\n", sym)
print("antisymmetric part:\n", antisym)
print("Frobenius norm of symmetric part:", np.linalg.norm(sym, 'fro'))
```

## Success criterion

Symmetric part of commutator is **exactly zero** (Frobenius norm = 0 or < 1e-10 if using floats; == 0 if using integer arithmetic).

If TRUE: `[M_TSML_Jordan, M_TSML_Idempotent]` is a pure Lie bracket → structurally meaningful in the sense of gl(10) Lie algebra actions on ℤ/10.

If FALSE: claim is wrong; report the residual symmetric part.

## Expected runtime

<5 minutes total (script is ~20 lines, runs in seconds).

## Deliverable

`papers/morphotic_braid/results/task14_lie_bracket_result.md`:
- commutator matrix
- symmetric / antisymmetric split with Frobenius norms
- verdict: pure Lie bracket (YES/NO)

**Tag:** `[COMPUTE JOB — TIER 2]`
