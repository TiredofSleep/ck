# BHML Correction Log
## (j+7)%10 → (j+1)%10 — HARMONY Is the Increment Operator

*Brayden Ross Sanders & C. A. Luther*
*March 31, 2026 | DOI: 10.5281/zenodo.18852047*

---

## Summary

Prior documentation stated `BHML[7][j] = (j+7)%10` for the HARMONY row.
This is **wrong**. The correct rule is `BHML[7][j] = (j+1)%10` for j ≥ 1.

HARMONY is the **increment operator** — it advances every operator by exactly
one step in Z/10Z. It is not a shift-by-7.

---

## Verification Against the Actual BHML Table

BHML row 7 (HARMONY): `[7, 2, 3, 4, 5, 6, 7, 8, 9, 0]`

| j | BHML[7][j] | (j+7)%10 | (j+1)%10 | Correct rule |
|---|-----------|---------|---------|------------|
| 0 | 7 | 7 | 1 | VOID identity: BHML[7][0]=7 |
| 1 | 2 | 8 | 2 | (j+1)%10 ✓ |
| 2 | 3 | 9 | 3 | (j+1)%10 ✓ |
| 3 | 4 | 0 | 4 | (j+1)%10 ✓ |
| 4 | 5 | 1 | 5 | (j+1)%10 ✓ |
| 5 | 6 | 2 | 6 | (j+1)%10 ✓ |
| 6 | 7 | 3 | 7 | (j+1)%10 ✓ |
| 7 | 8 | 4 | 8 | (j+1)%10 ✓ |
| 8 | 9 | 5 | 9 | (j+1)%10 ✓ |
| 9 | 0 | 6 | 0 | (j+1)%10 ✓ |

`(j+7)%10` fails 9 of 9 cells for j ≥ 1.
`(j+1)%10` fails 0 of 9 cells for j ≥ 1.
BHML[7][0] = 7 by VOID identity (separate rule).

---

## Files Containing (j+7)%10 — Status

All instances identified and classified:

### Category A: Historical documentation (correct to keep — documents the wrong claim)

These files explicitly state `(j+7)%10` is **wrong** and document why. They are
correct to preserve as part of the proof record.

| File | Line(s) | Context |
|------|---------|---------|
| `BHML_28CELL_DERIVATION.md` | 35, 190, 199 | Documents the error: "Row 7 rule `(j+7)%10`: **WRONG**" |
| `methodology/BHML_OPERATOR_IDENTITY.md` | 45, 55, 253 | Correction section: "`(j+7)%10` fails at 9 of 9 cells" |
| `SYNTHESIS_TABLE.md` | notes section | Documents correction: "NOT `(j+7)%10`" |
| `test_bhml_operator_identity.py` | 8, 107, 114, 595, 606 | Test code that proves the correction |

### Category B: Old test code (historical artifact — tested wrong rule, correctly reported failure)

These files contain the old test code that first discovered the failure. The
test results show the failure, which is how the correction was found.

| File | Line(s) | Context |
|------|---------|---------|
| `test_bhml_atomic_structure.py` | 134, 562-564, 595, 676, 679, 812 | Original test: `ok_r7 = all(BHML[7][j] == (j+7)%10 ...)` — reports False |

### Category C: Previously wrong, now corrected

These files previously stated `(j+7)%10` as a live claim. Corrected during this session.

| File | Original claim | Correction applied |
|------|---------------|-------------------|
| `methodology/BHML_ATOMIC_STRUCTURE.md` | Summary section listed `(j+7)%10` as the rule | NOTE added: C10 closes this; correct rule is `(j+1)%10` |

---

## 28-Cell Derivation Verification

Three rules, zero overlaps, zero residual:

### Rule A — VOID Identity (2 cells)
```
BHML[0][j] = j     for all j    (VOID row = identity)
BHML[i][0] = i     for all i    (VOID col = identity)
```
Setting j=7: BHML[0][7]=7=HARMONY. By symmetry: BHML[7][0]=7.
**Cells: (0,7) and (7,0).** ✓

### Rule B — Axis Saturation (17 cells)
```
BHML[i][j] = max(i,j)+1   for i,j ∈ {1..6}
```
Harmony (=7) when max(i,j)=6, i.e., i=6 OR j=6.
Row 6 extends to j=7,8,9 (CHAOS saturates). By symmetry, col 6 extends to i=7,8,9.
Row 6 (j=1..9): 9 cells. Col 6 (i=1..9, excl row 6): 8 cells. **Total: 17 cells.** ✓

### Rule C — Operator Identity (9 cells)
```
BHML[8][j] = 7   j ∈ {4,5,6}   (BREATH × TRANS = HARMONY)
BHML[9][j] = 7   j ∈ {4,5,6}   (RESET × TRANS = HARMONY)
BHML[8][8] = 7                  (BREATH × BREATH = HARMONY, self-resonance)
```
By symmetry: {4,5} × {8,9} and {8,9} × {4,5} cells.
**8 cross-zone cells + 1 self-resonance = 9 cells.** ✓

### Verification
- A ∩ B = 0 ✓
- A ∩ C = 0 ✓
- B ∩ C = 0 ✓
- |A| + |B| + |C| = 2 + 17 + 9 = **28** ✓

---

## HARMONY Row — Corrected Statement

```
BHML[7][j] = (j+1) mod 10   for j = 1..9
BHML[7][0] = 7               (VOID identity: BHML[7][0] by VOID rule, not increment)
```

HARMONY advances every non-VOID operator by exactly one step in Z/10Z:
- LATTICE (1) → COUNTER (2)
- COUNTER (2) → PROGRESS (3)
- ...
- RESET (9) → VOID (0)

This is the successor function on Z/10Z restricted to j ≥ 1.

---

## tig_unit_tests.py — All 15 Pass

Run after correction: 15/15 ALL PASS. The correction does not break any
existing unit tests (tig_unit_tests.py uses a different context for BHML
— the reduction table for semiprime worlds — not the TIG composition table).

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
