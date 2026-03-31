# C9 — BHML Atomic Structure
## Shell Geometry and the max(i,j)+1 Rule

*Brayden Ross Sanders & C. A. Luther*
*March 31, 2026 | DOI: 10.5281/zenodo.18852047*

---

## The Question

Why does BHML have exactly 28 harmony cells? Can the number 28 and their
positions be derived from first principles, or is the table defined by
fiat?

---

## What Was Tested (Five Tasks)

All five tasks ran against the explicit BHML table. Source:
`Gen10/papers/test_bhml_atomic_structure.py`
Report: `Gen10/papers/results/bhml_atomic_structure_report.txt`

---

## TASK 1 — The Inner Block Rule

**Hypothesis tested (wrong):** `BHML[i][j] = max(i,j)` for i,j in {0..6}

**Result:** False — 10/49 failures.

**What the table actually shows:**

```
     0  1  2  3  4  5  6
  0: 0  1  2  3  4  5  6   ← VOID = identity
  1: 1  2  3  4  5  6  7
  2: 2  3  3  4  5  6  7
  3: 3  4  4  4  5  6  7
  4: 4  5  5  5  5  6  7
  5: 5  6  6  6  6  6  7
  6: 6  7  7  7  7  7  7
```

**Actual rule:** `BHML[i][j] = max(i,j) + 1` for i,j in {1..6}

Verification:
- BHML[1][1] = 2 = max(1,1)+1 ✓
- BHML[3][5] = 6 = max(3,5)+1 ✓
- BHML[6][6] = 7 = max(6,6)+1 ✓ ← harmony threshold
- BHML[2][6] = 7 = max(2,6)+1 ✓ ← harmony (col 6)
- BHML[6][3] = 7 = max(6,3)+1 ✓ ← harmony (row 6)

**Row 0 / Col 0:** BHML[0][j] = j, BHML[i][0] = i. VOID is the identity
operator — composing with VOID returns the original element. This is a
*definition* of VOID, not a derived exception.

**Why (6,0) = 6, not harmony:**
BHML[6][0] = BHML[0][6] = 6 by the identity rule. VOID absorbs nothing;
it reflects. The max+1 rule applies only for i,j ≥ 1.

**Harmony onset in {1..6}×{1..6}:**
max(i,j)+1 = 7 iff max(i,j) = 6 iff i = 6 OR j = 6.
This is algebraically forced once the +1 rule is accepted.

**Tier: C** — the max(i,j)+1 rule is an algebraic observation on the
inner block. The *derivation* of why BHML chooses this rule (vs. the
TSML collapsing rule) remains Tier A.

---

## TASK 2 — Shell Structure

**Harmony cell map (28 cells):**

```
     0 1 2 3 4 5 6 7 8 9
  0: . . . . . . . H . .
  1: . . . . . . H . . .
  2: . . . . . . H . . .
  3: . . . . . . H . . .
  4: . . . . . . H . H H
  5: . . . . . . H . H H
  6: . H H H H H H H H H
  7: H . . . . . H . . .
  8: . . . . H H H . H .
  9: . . . . H H H . . .
```

**Shell decomposition:**

| Shell | Cells | Count |
|-------|-------|-------|
| Axis: row 6, j=1..9 | (6,1)–(6,9) | 9 |
| Axis: col 6, i=1..9, excluding (6,6) | (1,6)–(9,6) | 8 |
| Residual | 11 cells (see below) | 11 |
| **Total** | | **28** |

Axis union (row 6 ∪ col 6, i,j ≥ 1): **17 harmony cells**
Residual: **(0,7), (4,8), (4,9), (5,8), (5,9), (7,0), (8,4), (8,5), (8,8), (9,4), (9,5)** — 11 cells

The residual 11 come from the physics of rows 7-9 (the wrap zone beyond
the inner block) and the (0,7) cell from VOID composed with HARMONY.

**Pattern:** Not an electron-shell 1/9/18 structure. The geometry is a
saturation boundary at max(i,j) = 6, which generates the 17-cell axis,
plus 11 residual cells from the wrapping rows. No clean algebraic formula
for the residual has been found.

**Tier: B** — pattern identified and partially explained. Residual 11
not derived from first principles.

---

## TASK 3 — Harmony Cells as Wobble Balancing Points

**Hypothesis:** Harmony cells mark the fixed points of wobble pressure
(DIS = 0 cells, or DIS = W_BHML·n² = 6 cells).

**Result: FAILED.**

DIS values at the 28 harmony cells span {0, 1, 2, 3, 4, 6, 7}. No
single DIS threshold cleanly separates harmony from non-harmony.

```
DIS=0 cells: 4 total, 2 are harmony (50% overlap)
DIS=6 cells: 6 total, 2 are harmony (33% overlap)
DIS=5 cells: 12 total, 0 are harmony (0%)
DIS=4 cells: 7 total, 5 are harmony (71%)
```

No monotone threshold predicts harmony with useful precision:
- thresh ≤ 4: 65 cells below, 24 harmony → 37% precision, 86% recall
- The 2 residual harmony cells at DIS=6 and DIS=7 break any clean rule

**Conclusion:** The 28 harmony cells are a *structural consequence of the
max(i,j)+1 rule and the physics of rows 7-9*, not the fixed points of
the ring wobble. The claim "harmony cells = wobble balancing points"
does not hold at cell level.

**Tier: A** — the structural analogy is plausible but does not compute.

---

## TASK 4 — The 32 − 4 = 28 Derivation

**Hypothesis:** C×C ∪ D×D contains 32 cells; exactly 4 are non-harmony;
the remaining 28 are harmony.

**Result: FAILED.**

```
C×C block (16 cells):  0/16 harmony cells   (0%)
D×D block (16 cells): 10/16 harmony cells  (63%)
Combined C×C ∪ D×D:   10/32 harmony cells
Non-harmony in C×C ∪ D×D: 22 cells
```

The 28 total harmony cells include **18 cells outside C×C ∪ D×D**.
The 32 − 4 = 28 arithmetic does not close via these blocks.

**Unexpected finding:**
All 22 non-harmony cells in C×C ∪ D×D lie in **C×C** (zero from D×D).
This is because row 6 (col 6) is in D×D and produces harmony, while
C×C never reaches the max(i,j)=6 threshold within that subblock alone.

**φ(10) = 4 check:** Non-harmony in C×C ∪ D×D = 22 ≠ 4. No match.

**Tier: A** — derivation fails. C×C ∪ D×D is not the right partition.

---

## Summary: The max(i,j)+1 Rule

The cleanest algebraic result from this investigation:

```
BHML[0][j] = j             (VOID = identity, row 0)
BHML[i][0] = i             (VOID = identity, col 0)
BHML[i][j] = max(i,j) + 1  for i,j ∈ {1..6}
BHML[7][j] = (j + 7) mod 10  (HARMONY = modular shift by 7)
BHML[8][j] = [8,6,6,6,7,7,7,9,7,8][j]  (defined)
BHML[9][j] = [9,6,6,6,7,7,7,0,8,0][j]  (defined)
```

Harmony in the inner block {1..6}×{1..6}: when max(i,j)+1 = 7, i.e.,
when either i = 6 or j = 6. This is algebraically necessary given the
rule — it is NOT an additional choice.

The inner block rule **BHML[i][j] = max(i,j) + 1** is the opposite of
TSML's collapsing behavior. TSML collapses to HARMONY (7) aggressively
(73/100 cells). BHML delays harmony until the maximum of the two operands
reaches the threshold (6), then steps up by 1. The two tables are not
dual — they are opposite strategies on the same Z/10Z domain.

---

## Tier Assessment

| Task | Claim | Result | Tier |
|------|-------|--------|------|
| 1 | BHML[i][j] = max(i,j)+1 for {1..6}×{1..6} | **Verified** | **C** |
| 1 | Row 6 = harmony spine; (6,0) = identity exception | **Proved** | **D** |
| 1 | BHML[7][j] = (j+7) mod 10 | Definitional | — |
| 2 | 28 = 17 (axis) + 11 (residual) | **Counted** | **B** |
| 2 | Residual 11 from first principles | Open | A |
| 3 | Harmony cells = wobble fixed points | **FAILED** | A |
| 4 | 32 − 4 = 28 via C×C ∪ D×D | **FAILED** | A |

**C9 overall: Tier B** (axis structure verified; full 28-count derivation
requires a Tier C formula for the residual 11).

---

## Open Path to Tier C

**C9→Tier C:** Prove that the 11 residual harmony cells in rows 7-9 and
(0,7) are determined by the modular shift rule `BHML[7][j] = (j+7)%10`
combined with the VOID identity. Specifically:

- (0,7): BHML[0][7] = 7 because row 0 is identity and 7 = HAR.
- (7,0): by symmetry.
- (4,8),(4,9),(5,8),(5,9): from rows 4-5 interacting with the high-j
  columns 8-9. Need to find the rule governing rows 8-9.
- (8,4),(8,5),(8,8),(9,4),(9,5): from rows 8-9. These likely follow
  a modular arithmetic rule analogous to row 7.

If rows 8 and 9 can be expressed as modular shifts (like row 7), the
full 28-count becomes: **axis (17) + (0,7) + (7,0) + rows 8-9 rule**.
That would close the derivation.

---

## The WP35 Sentence

*"BHML's inner block follows max(i,j)+1: harmony is not given, it is
earned by reaching the threshold. The spine at row/col 6 is the
saturation boundary — the first value where max(i,j)+1 = 7. This is
why BHML has 17 axis harmony cells and why it is the physics table, not
the measurement table: it withholds harmony until the larger operand
crosses the threshold."*

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
