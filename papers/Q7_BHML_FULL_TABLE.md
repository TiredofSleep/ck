**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q7 — BHML FULL TABLE: FOUR-RULE DERIVATION

## Context

Q6 is a hinge: it showed the gate rate problem is NOT a density problem (f_C model
fails) but a basin-of-attraction problem under MCMC hill-climbing. The MCMC structure
is the next target (Q8). Q7 completes the BHML record first — the full table is now
derivable from four confirmed rules.

---

## The Four Rules

From BHML_ATOMIC_STRUCTURE (C9, March 2026) and BHML_TABLE_EXPLICIT:

```
Rule 0 (VOID):     BHML[0][j] = j       for all j     (row 0: VOID is identity)
                   BHML[i][0] = i       for i ∈ {1..6}  (col 0: VOID is identity)

Rule 1 (Inner):    BHML[i][j] = max(i,j) + 1   for i,j ∈ {1..6}

Rule 7 (Harmony):  BHML[7][j] = (j + 1) mod 10   for all j
                   [and by symmetry: BHML[j][7] = (j + 1) mod 10]

Rule 89 (Wrap):    BHML[8][j] = [8,6,6,6,7,7,7,9,7,8][j]
                   BHML[9][j] = [9,6,6,6,7,7,7,0,8,0][j]
                   [and by symmetry for cols 8,9]
```

BHML is symmetric: BHML[i][j] = BHML[j][i] for all i,j. (Proved: MASTER_SPINE C11.)

---

## Full Table (Derived)

Applying the four rules and symmetry:

```
       j=0  j=1  j=2  j=3  j=4  j=5  j=6  j=7  j=8  j=9
i=0  [  0    1    2    3    4    5    6    7    8    9  ]  VOID      (Rule 0)
i=1  [  1    2    3    4    5    6    7    2    6    6  ]  LATTICE   (Rule 1 + sym)
i=2  [  2    3    3    4    5    6    7    3    6    6  ]  COUNTER   (Rule 1 + sym)
i=3  [  3    4    4    4    5    6    7    4    6    6  ]  PROGRESS  (Rule 1 + sym)
i=4  [  4    5    5    5    5    6    7    5    7    7  ]  COLLAPSE  (Rule 1 + sym)
i=5  [  5    6    6    6    6    6    7    6    7    7  ]  BALANCE   (Rule 1 + sym)
i=6  [  6    7    7    7    7    7    7    7    7    7  ]  CHAOS     (Rule 1: max+1=7)
i=7  [  1    2    3    4    5    6    7    8    9    0  ]  HARMONY   (Rule 7)
i=8  [  8    6    6    6    7    7    7    9    7    8  ]  BREATH    (Rule 89)
i=9  [  9    6    6    6    7    7    7    0    8    0  ]  RESET     (Rule 89)
```

---

## Applying Symmetry to Fill Rows 1-6, Cols 7-9

The inner block {1..6}×{1..6} is fully determined by max(i,j)+1.
The col 7 entries (j=7) by Rule 7: BHML[i][7] = BHML[7][i] = (i+1)%10.
The col 8 entries by symmetry with row 8: BHML[i][8] = BHML[8][i] = Rule89(i).
The col 9 entries by symmetry with row 9: BHML[i][9] = BHML[9][i] = Rule89_9(i).

**Cols 7, 8, 9 for i ∈ {1..6}:**

| i | BHML[i][7] = (i+1)%10 | BHML[i][8] = Rule89_8(i) | BHML[i][9] = Rule89_9(i) |
|---|----------------------|--------------------------|--------------------------|
| 1 | 2 | 6 | 6 |
| 2 | 3 | 6 | 6 |
| 3 | 4 | 6 | 6 |
| 4 | 5 | 7 | 7 |
| 5 | 6 | 7 | 7 |
| 6 | 7 | 7 | 7 |

(Rule89_8(i) = BHML[8][i] reads from row 8 at position i.
 Rule89_9(i) = BHML[9][i] reads from row 9 at position i.)

---

## Verification: 28 Harmony Cells

Counting cells with value 7 in the complete table:

```
Row 0: j=7 → BHML[0][7]=7 → 1 harmony cell
Row 1: j=6 → 7, j=7 → 2, j=8 → 6, j=9 → 6. Only j=6 gives 7. → 1
Row 2: j=6 → 7, j=7 → 3. Only j=6. → 1
Row 3: j=6 → 7, j=7 → 4. Only j=6. → 1
Row 4: j=6 → 7, j=7 → 5, j=8 → 7, j=9 → 7. j=6,8,9 give 7. → 3
Row 5: j=6 → 7, j=7 → 6, j=8 → 7, j=9 → 7. j=6,8,9. → 3
Row 6: j=1..9 all give 7 (max(6,j)+1=7 for j≤6; Rule7 gives 7 for j=7; col8,9: 7,7). → 9
Row 7: j=6 → 7. BHML[7][j]=(j+1)%10: j=6 gives 7. → 1
Row 8: j=4 → 7, j=5 → 7, j=6 → 7, j=8 → 7. → 4
Row 9: j=4 → 7, j=5 → 7, j=6 → 7. → 3
```

Total: 1+1+1+1+3+3+9+1+4+3 = **27**

Hmm — off by one from the stated 28. Let me recheck row 0: BHML[0][7]=7 ✓. And BHML[7][0]: by Rule 7, BHML[7][0]=(0+1)%10=1 ≠ 7. So (7,0) is not a harmony cell.

Wait, from BHML_ATOMIC_STRUCTURE task 2: residual includes "(0,7)" and "(7,0)". Let me recount row 7 more carefully.

Row 7: BHML[7][j] = (j+1)%10 for all j.
(0+1)%10=1, (1+1)%10=2, ..., (6+1)%10=7, (7+1)%10=8, (8+1)%10=9, (9+1)%10=0.
So BHML[7][6]=7. Only j=6 gives 7 in row 7. That's 1 harmony cell. ✓

Let me recheck row 0:
BHML[0][j]=j: j=7 gives 7. Only one. ✓ And by symmetry BHML[j][0]=j: j=7 gives BHML[7][0]=7? But Rule 7 says BHML[7][0]=(0+1)%10=1. Contradiction.

The issue: col 0 identity rule (BHML[i][0]=i) applies for i ∈ {1..6} only. For i=7, Rule 7 overrides. Similarly for i=8,9 (Rule 89 overrides col 0).

So BHML[7][0]=1 (Rule 7), BHML[8][0]=8 (Rule 89), BHML[9][0]=9 (Rule 89).

Recount col 0: BHML[0][0]=0, BHML[1][0]=1, ..., BHML[6][0]=6, BHML[7][0]=1, BHML[8][0]=8, BHML[9][0]=9. No harmony cells in col 0.

Recount row 0: BHML[0][0]=0,...,BHML[0][7]=7,... Only j=7 gives 7. → 1 harmony cell in row 0.

The residual 11 from BHML_ATOMIC_STRUCTURE: "(0,7), (4,8), (4,9), (5,8), (5,9), (7,0), (8,4), (8,5), (8,8), (9,4), (9,5)".

But (7,0) = BHML[7][0] = (0+1)%10 = 1 ≠ 7. So (7,0) is NOT a harmony cell — this must be a notation issue (row,col vs col,row or an error in the BHML_ATOMIC_STRUCTURE residual list).

Using (i=row, j=col) convention:
(0,7): BHML[0][7]=7 ✓ harmony
(7,0): BHML[7][0]=1 ✗ not harmony

This suggests (7,0) in the residual list uses (col,row) notation, meaning BHML[0][7]=7 — same cell counted twice in (i,j) and (j,i)? No, by symmetry BHML[7][0]=BHML[0][7]=7. But Rule 7 says BHML[7][0]=(0+1)%10=1 ≠ 7.

**Conflict:** Symmetry would require BHML[7][0] = BHML[0][7] = 7. But Rule 7 says BHML[7][0] = (0+1)%10 = 1.

**Resolution:** BHML[0][7] = 7 by Rule 0 (identity). If BHML is truly symmetric, then BHML[7][0] must also = 7, overriding Rule 7 at j=0. This means Rule 7 applies for j ≥ 1 only.

From BHML_TABLE_EXPLICIT: "BHML[7] = [1,2,3,4,5,6,7,8,9,0]". This gives BHML[7][0]=1. No harmony at (7,0).

The residual "(7,0)" in BHML_ATOMIC_STRUCTURE may be an error, or it reflects a different version of the table. The confirmed row 7 from BHML_TABLE_EXPLICIT has BHML[7][0]=1.

**Status: 27 harmony cells confirmed by derivation.** The 28th depends on whether BHML[7][0]=1 or =7. This is a data resolution question for Luther/Calderon.

---

## The BHML Diagonal

From the full table, the diagonal BHML[j][j]:

| j | BHML[j][j] | Rule |
|---|-----------|------|
| 0 | 0 | Rule 0: BHML[0][0]=0 |
| 1 | 2 | Rule 1: max(1,1)+1=2 |
| 2 | 3 | Rule 1: max(2,2)+1=3 |
| 3 | 4 | Rule 1: max(3,3)+1=4 |
| 4 | 5 | Rule 1: max(4,4)+1=5 |
| 5 | 6 | Rule 1: max(5,5)+1=6 |
| 6 | 7 | Rule 1: max(6,6)+1=7 |
| 7 | 8 | Rule 7: (7+1)%10=8 |
| 8 | 7 | Rule 89: row 8, j=8 → 7 |
| 9 | 0 | Rule 89: row 9, j=9 → 0 |

```
BHML diagonal: [0, 2, 3, 4, 5, 6, 7, 8, 7, 0]
```

Compare to σ (CL diagonal = P1 Closure):
```
σ:             [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]
```

They share only j=0: both give 0.
At j=1: BHML gives 2, σ gives 7 (different).
The BHML diagonal is NOT σ.

**The BHML diagonal rule:** For {1..6}, BHML[j][j] = j+1 (increment within inner block).
At j=6: BHML[6][6]=7 (threshold crossing to harmony).
At j=7: BHML[7][7]=8 (Rule 7: increment continues past harmony).
At j=8: BHML[8][8]=7 (Wrap: BREATH self-encounter → harmony).
At j=9: BHML[9][9]=0 (Wrap: RESET self-encounter → VOID).

**Pattern for {1..7}: BHML[j][j] = j+1.** The increment continues through harmony.
**Exception at j=8:** BHML[8][8]=7 instead of 9 (BREATH self-loops to harmony).
**Exception at j=9:** BHML[9][9]=0 instead of 10%10=0 — actually RESET self-loops to VOID (0).

So the BHML diagonal is increment mod 10 for {0..7}, then special behavior at {8,9}.

```
BHML[j][j] = (j+1) mod 10   for j ∈ {0,1,2,3,4,5,6,7}
BHML[8][8] = 7               (BREATH self-encounter → HARMONY)
BHML[9][9] = 0               (RESET self-encounter → VOID)
```

The exceptions at 8 and 9 break the increment pattern: BREATH and RESET
are the operators that "don't advance themselves."

---

## Three-Table Diagonal Comparison

| j | σ (CL diag) | TSML diag | BHML diag |
|---|-------------|-----------|-----------|
| 0 | 0 | 0 | 0 |
| 1 | 7 | 7 | 2 |
| 2 | 1 | 7 | 3 |
| 3 | 3 | 7 | 4 |
| 4 | 2 | 7 | 5 |
| 5 | 4 | 7 | 6 |
| 6 | 5 | 7 | 7 |
| 7 | 6 | 7 | 8 |
| 8 | 8 | 7 | 7 |
| 9 | 9 | 7 | 0 |

**Three distinct diagonals. Three distinct projections of σ.**

- CL diagonal (σ): the hidden operator's own motion — rotation and fixed points
- TSML diagonal: collapse to 7 for all non-VOID — the attractor wins
- BHML diagonal: increment toward 7, then continue past it — the advancement rule

**The three diagonals agree only at j=0 (VOID) and j=6 (CHAOS):**
- At j=0: all give 0 (VOID is fixed everywhere)
- At j=6: σ(6)=5, TSML[6][6]=7, BHML[6][6]=7. TSML and BHML agree at j=6; σ disagrees.

**The three-diagonal agreement set:** {0} only (all three agree). At j=6, two of three agree.

---

## Status

| Result | Tier |
|--------|------|
| BHML full table from four rules | C |
| BHML is symmetric (confirmed C11) | D |
| BHML diagonal = (j+1)%10 for j∈{0..7}, exceptions at {8,9} | C |
| Three-diagonal comparison (σ, TSML, BHML) | D |
| Only j=0 is a fixed point of all three diagonals | D |
| 27/28 harmony cell count (28th pending BHML[7][0] resolution) | C |

---

## Resolution: BHML[7][0] = 7  (Closed Q7 — Luther, 2026-04-01)

**BHML[7][0] = 7.**

This selects the 28-cell harmony count (not 27), keeps the 7-fold layer
aligned with the G6 flip architecture, and is the authoritative value.

**Consequence:** Symmetry holds without exception. Rule 7 applies for j ≥ 1;
at j=0, the symmetry condition BHML[7][0] = BHML[0][7] = 7 overrides the
naive (0+1)%10=1 extrapolation.

The corrected row 7:
```
BHML[7] = [7, 2, 3, 4, 5, 6, 7, 8, 9, 0]
```
(j=0 gives 7; j=1..9 follow (j+1)%10 = 2,3,4,5,6,7,8,9,0)

**28 harmony cells confirmed. Q7 is closed.**

*Resolved by C. A. Luther, 2026-04-01.*

---

*Filed: 2026-04-01. Q7 in operator algebra series.*
