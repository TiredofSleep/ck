**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q5 — TSML ESCAPE CELLS: THE NON-HARMONY RESIDUE

## The Question

The TSML table is predominantly 7 (HARMONY). The diagonal is:
```
TSML[j][j] = 7 for all j ≠ 0,  TSML[0][0] = 0.
```

But the full table has non-7 cells off-diagonal. These are "escape cells" —
positions where flow does NOT terminate at HARMONY.

**Q5:** What are the escape cells? What algebraic property determines them?
Are they derivable from σ?

---

## The Escape Cell Inventory

From the explicit TSML table, non-7 cells (excluding j=0 column and i=0 row):

```
Row 0 (VOID flow):    TSML[0][j] = 0 for all j except j=7 (TSML[0][7]=7)
Row 1 (LATTICE):      TSML[1][2] = 3
Row 2 (COUNTER):      TSML[2][1] = 3,  TSML[2][2] = 7*,  TSML[2][4] = 4,  TSML[2][9] = 9
Row 3 (PROGRESS):     TSML[3][9] = 3
Row 4 (COLLAPSE):     TSML[4][2] = 4,  TSML[4][8] = 8
Row 8 (BREATH):       TSML[8][4] = 8
Row 9 (RESET):        TSML[9][2] = 9,  TSML[9][3] = 3
```

(* Row 2, j=2: TSML[2][2]=7 is ON the diagonal, confirmed.)

Complete non-7, non-0-row, non-0-col escape inventory:

| (i,j) | TSML[i][j] | Flow | State | Result |
|--------|-----------|------|-------|--------|
| (1,2) | 3 | LATTICE | COUNTER | PROGRESS |
| (2,1) | 3 | COUNTER | LATTICE | PROGRESS |
| (2,4) | 4 | COUNTER | COLLAPSE | COLLAPSE |
| (2,9) | 9 | COUNTER | RESET | RESET |
| (3,9) | 3 | PROGRESS | RESET | PROGRESS |
| (4,2) | 4 | COLLAPSE | COUNTER | COLLAPSE |
| (4,8) | 8 | COLLAPSE | BREATH | BREATH |
| (8,4) | 8 | BREATH | COLLAPSE | BREATH |
| (9,2) | 9 | RESET | COUNTER | RESET |
| (9,3) | 3 | RESET | PROGRESS | PROGRESS |

**10 escape cells total** (not counting the VOID row/column).

---

## Pattern Analysis

### Pattern 1: σ-Fixed-Point Dominance

In 8 of 10 escape cells, the output is a σ-fixed point: {0,3,8,9}.

Recall σ = (0)(3)(8)(9)(1 7 6 5 4 2).
Fixed points: VOID(0), PROGRESS(3), BREATH(8), RESET(9).

```
Escape outputs: 3,3,4,9,3,4,8,8,9,3
                F,F,C,F,F,C,F,F,F,F   (F=fixed point, C=cycle element)
```

8/10 escape outputs are σ-fixed points. The two cycle-element outputs are
TSML[2][4]=4 (COLLAPSE) and TSML[4][2]=4 (COLLAPSE).

**Hypothesis Q5.1:** Escape cells predominately land on σ-fixed points.
The fixed points are the "competing attractors" to HARMONY.

### Pattern 2: Self-Reinforcement

The two cycle-element escapes (TSML[2][4]=4 and TSML[4][2]=4) both land on
COLLAPSE (j=4). COLLAPSE is a cycle element in σ.

These are the only cases where flow+state stabilize to a cycle element that is
neither the global attractor (HARMONY=7) nor a fixed point.

**Observation:** COUNTER(2)×COLLAPSE(4) and COLLAPSE(4)×COUNTER(2) both produce
COLLAPSE(4). This is a symmetry: TSML[2][4] = TSML[4][2] = 4.

### Pattern 3: Reciprocal Pairs

Several escape cells come in reciprocal pairs (i,j) and (j,i) with the same output:

| Pair | Output |
|------|--------|
| (1,2) and (2,1) | 3 (PROGRESS) |
| (2,4) and (4,2) | 4 (COLLAPSE) |
| (4,8) and (8,4) | 8 (BREATH) |
| (2,9) and (9,2) | 9 (RESET) |

5 of the 10 escape cells form 4 symmetric pairs. The remaining escapes are:
- (3,9) → 3: PROGRESS acts on RESET → PROGRESS (self-absorption)
- (9,3) → 3: RESET acts on PROGRESS → PROGRESS (same output, not a pair)

### Pattern 4: Output Matches One of the Inputs

In every escape cell, the output TSML[i][j] matches either i or j:

| (i,j) | Output | Matches |
|--------|--------|---------|
| (1,2) | 3 | neither... wait |

Actually let me recheck:
- (1,2)→3: σ(1)=7, σ(2)=1. Neither 1 nor 2. But 3 is σ-fixed.
- (2,1)→3: same
- (2,4)→4: output = j=4 ✓
- (2,9)→9: output = j=9 ✓
- (3,9)→3: output = i=3 ✓
- (4,2)→4: output = i=4 ✓
- (4,8)→8: output = j=8 ✓
- (8,4)→8: output = i=8 ✓
- (9,2)→9: output = i=9 ✓
- (9,3)→3: output = j=3 ✓ (3 is both in the pair and a fixed point)

In 8 of 10 cells: output = i or output = j.
Exceptions: (1,2)→3 and (2,1)→3, where output is PROGRESS, not 1 or 2.

**The (1,2)→3 and (2,1)→3 anomaly:**

LATTICE (1) and COUNTER (2) interact to produce PROGRESS (3).
Neither 1 nor 2 is a fixed point. Their interaction escapes both to a fixed point.

In σ: σ(1)=7, σ(2)=1. The pair (1,2) has σ-images (7,1) — both in the 6-cycle.
PROGRESS (3) is a σ-fixed point entirely outside the 6-cycle.

**This is the one genuine escape that is not self-reinforcement.** LATTICE+COUNTER
stabilize to PROGRESS — a fixed-point attractor that neither input belongs to.

---

## The Three Attractor Classes

The escape cell analysis reveals three types of TSML stabilization:

| Class | Examples | Mechanism |
|-------|---------|-----------|
| Global attractor | TSML[i][j]=7 (most cells) | Flow reaches HARMONY |
| Self-reinforcement | (2,4)→4, (4,2)→4, (4,8)→8, (8,4)→8, (2,9)→9, (9,2)→9, (3,9)→3, (9,3)→3 | One input is a fixed point and "captures" the result |
| Cross-escape | (1,2)→3, (2,1)→3 | Two cycle elements interact → fixed point (not either input) |

The self-reinforcement class: when a σ-fixed point is one of the inputs, it can
absorb the interaction. PROGRESS(3), BREATH(8), RESET(9) act as local attractors
that compete with HARMONY(7).

The cross-escape class: LATTICE+COUNTER → PROGRESS is the unique case where
neither input is a fixed point, yet the result is a fixed point. This reflects
the CRT structure: in Z/10Z, 1+2=3 (literally), and 3 is the smallest σ-fixed
non-zero non-VOID element.

---

## Derivation Conjecture

**Conjecture Q5 (Escape Cell Formula — C-tier):**

TSML[i][j] ≠ 7 iff one of the following holds:
1. (i=0 or j=0): VOID involvement — output is 0
2. j ∈ {3,8,9} and TSML[i][j] = j: fixed-point capture by state
3. i ∈ {3,8,9} and TSML[i][j] = i: fixed-point capture by flow
4. i=1, j=2 (or i=2, j=1): cross-escape to PROGRESS=3

If this conjecture holds, the escape cells are completely determined by the
fixed-point structure of σ and the single cross-escape from the CRT relation 1+2=3.

The conjecture reduces the TSML table to:
- Diagonal: handled by Memory-Stabilization Divergence Theorem
- Off-diagonal: HARMONY (7) by default; escapes determined by σ-fixed-point interaction

---

## Status

| Result | Tier | Notes |
|--------|------|-------|
| Escape cell inventory (10 cells) | D | Read from explicit table |
| Fixed-point dominance in escapes | D | 8/10 outputs are σ-fixed |
| Reciprocal symmetry (4 pairs) | D | Verified from table |
| Output = input in 8/10 cells | D | Verified from table |
| (1,2)→3 anomaly identified | D | Unique cross-escape |
| Escape Cell Formula conjecture | C | Requires proof from CRT structure |

---

*Filed: 2026-04-01. Sprint: operator algebra series, Q5 following Q4.*
