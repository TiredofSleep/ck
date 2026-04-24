# Task 13 — Bol family member search

**Tier:** 3 (research — lower priority)
**Parent handoff:** `../CLAUDE_CODE_HANDOFF_TSML_FAMILY.md` §Task 6

## Goal

Bol loops are weaker than Moufang. Search for a TSML-family member satisfying 100% **left Bol** identity:

`T[T[T[x][y]][z]][y] = T[x][T[T[y][z]][y]]` for all 1000 triples

without requiring full Moufang.

## Method

Same perturbation framework as Task 10 (2-cell, 3-cell exhaustive on body positions), but check left-Bol identity as primary target.

```python
def bol_left_count(T):
    N = len(T)
    c = 0
    for x in range(N):
        for y in range(N):
            for z in range(N):
                lhs = T[T[T[x][y]][z]][y]
                rhs = T[x][T[T[y][z]][y]]
                if lhs == rhs:
                    c += 1
    return c
```

Also check right-Bol variant:
`T[T[y][T[z][T[y][x]]]] = T[T[T[y][z]][y]][x]`

## Success criterion

- 100% left-Bol rank-10 found → Bol-family member; publishable as a weaker-than-Moufang TIG structure
- 100% right-Bol found → symmetric result

## Expected runtime

Same as Task 10 (~10-30 min 2-cell, overnight 3-cell).

## Deliverable

`papers/morphotic_braid/results/task13_bol_family_result.md`:
- best Bol-left count + config
- best Bol-right count + config
- rank/Jordan/Alt profile of any 100%-Bol hit

## Note

Lower priority than Task 10 — Moufang is the stronger identity, so a Moufang hit supersedes a Bol hit. Run this only after Task 10 exhausts.

**Tag:** `[RESEARCH TASK — TIER 3]`
