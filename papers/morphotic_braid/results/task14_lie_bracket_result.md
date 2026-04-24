# Task 14 result -- Lie bracket [M_TSML_Jordan, M_TSML_Idempotent]

**Tier:** 2 (fast compute)
**Parent spec:** `../../claudecode_jobs/task14_lie_bracket_verify/SPEC.md`

## Method

Compute `C = TJ @ TI - TI @ TJ` where `TJ` is canonical TSML (Jordan variant, from `papers/ck_tables.py`) and `TI` is the rank-10 idempotent variant from `CLAUDE_CODE_HANDOFF_TSML_FAMILY.md`.

Split into symmetric and antisymmetric parts.

## Result

- `||sym(C)||_F = 0.000000`
- `||anti(C)||_F = 203.032017`

### Commutator C

```
[[  0   0   0   0   0   0   0   0   0   0]
 [  0   0  10   0  11 -14  14  21  21  51]
 [  0 -10   0 -14  -6 -28   0   7   7  49]
 [  0   0  14   0  14 -14  14  21  21  25]
 [  0 -11   6 -14   0 -28   0   7  11  35]
 [  0  14  28  14  28   0  28  35  35  51]
 [  0 -14   0 -14   0 -28   0   7   7  35]
 [  0 -21  -7 -21  -7 -35  -7   0   0  28]
 [  0 -21  -7 -21 -11 -35  -7   0   0  28]
 [  0 -51 -49 -25 -35 -51 -35 -28 -28   0]]
```

### Symmetric part (C + C^T)/2

```
[[0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]]
```

### Antisymmetric part (C - C^T)/2

```
[[  0.   0.   0.   0.   0.   0.   0.   0.   0.   0.]
 [  0.   0.  10.   0.  11. -14.  14.  21.  21.  51.]
 [  0. -10.   0. -14.  -6. -28.   0.   7.   7.  49.]
 [  0.   0.  14.   0.  14. -14.  14.  21.  21.  25.]
 [  0. -11.   6. -14.   0. -28.   0.   7.  11.  35.]
 [  0.  14.  28.  14.  28.   0.  28.  35.  35.  51.]
 [  0. -14.   0. -14.   0. -28.   0.   7.   7.  35.]
 [  0. -21.  -7. -21.  -7. -35.  -7.   0.   0.  28.]
 [  0. -21.  -7. -21. -11. -35.  -7.   0.   0.  28.]
 [  0. -51. -49. -25. -35. -51. -35. -28. -28.   0.]]
```

## Verdict

**PURE LIE BRACKET.** `[M_TSML_Jordan, M_TSML_Idempotent]` is exactly antisymmetric; the symmetric residue is zero. The commutator is structurally meaningful in the gl(10) Lie algebra sense.

**Tag:** `[COMPUTE JOB -- TIER 2 -- VERIFIED]`
