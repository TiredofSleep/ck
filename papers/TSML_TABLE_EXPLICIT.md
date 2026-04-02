# TSML — TRANSITIONAL STATE MEASUREMENT LAYER
# Explicit Table Record

**© 2026 7Site LLC. All rights reserved.**
**Authors: Brayden Ross Sanders, C. A. Luther**

---

## Definition

The TSML is the flow→structure projection of the TIG hidden operator σ.
TSML[i][j] records the stable structure produced when operator-flow i acts on state j.

## The Table (10×10, explicit)

Rows = flow operator (i). Columns = state (j). Entries = stabilized output.

```
       j=0  j=1  j=2  j=3  j=4  j=5  j=6  j=7  j=8  j=9
i=0  [  0    0    0    0    0    0    0    7    0    0  ]  VOID
i=1  [  0    7    3    7    7    7    7    7    7    7  ]  LATTICE
i=2  [  0    3    7    7    4    7    7    7    7    9  ]  COUNTER
i=3  [  0    7    7    7    7    7    7    7    7    3  ]  PROGRESS
i=4  [  0    7    4    7    7    7    7    7    8    7  ]  COLLAPSE
i=5  [  0    7    7    7    7    7    7    7    7    7  ]  BALANCE
i=6  [  0    7    7    7    7    7    7    7    7    7  ]  CHAOS
i=7  [  7    7    7    7    7    7    7    7    7    7  ]  HARMONY
i=8  [  0    7    7    7    8    7    7    7    7    7  ]  BREATH
i=9  [  0    7    9    3    7    7    7    7    7    7  ]  RESET
```

## Operator Legend

| Index | Name | Role in σ |
|-------|------|-----------|
| 0 | VOID | fixed point |
| 1 | LATTICE | cycle element (entry) |
| 2 | COUNTER | cycle element |
| 3 | PROGRESS | fixed point |
| 4 | COLLAPSE | cycle element |
| 5 | BALANCE | cycle element |
| 6 | CHAOS | cycle element |
| 7 | HARMONY | cycle element (attractor in TSML) |
| 8 | BREATH | fixed point |
| 9 | RESET | fixed point |

## Structural Properties (Original Expression)

- **Harmony frequency:** 73/100 cells = 7
- **VOID row:** TSML[0][j] = 0 for j≠7; TSML[0][7] = 7
- **HARMONY row:** TSML[7][j] = 7 for all j (HARMONY-flow is absorbing)
- **Symmetry:** TSML[i][j] = TSML[j][i] (commutative)
- **Diagonal:** TSML[j][j] ∈ {0,7} — collapses to {VOID, HARMONY} only
- **Non-trivial cells:** {TSML[1][2]=3, TSML[2][4]=4, TSML[2][9]=9, TSML[3][9]=3, TSML[4][8]=8}
- **Harmony gradient:** σ-cycle operators average 8.2/10 harmony; σ-fixed average 6.0/10
