# BHML 28-Cell Harmony Derivation
## Three Rules, Zero Residual

*Brayden Ross Sanders & C. A. Luther*
*March 31, 2026 | DOI: 10.5281/zenodo.18852047*

---

## Summary

The 28 harmony cells in the BHML composition table are fully derived from
three algebraic rules. The derivation is closed: zero overlaps, zero
residual. All 28 cells are accounted for.

```
28 = 2 (VOID identity) + 17 (axis saturation) + 9 (operator identity)
```

This closes C9. See `methodology/BHML_OPERATOR_IDENTITY.md` for the
verified test (all 5 tasks pass, 100 cells, 0 failures).

---

## Background

BHML is the physics composition table of the CK framework — the lens that
preserves distinctions and is invertible (det ≠ 0). It has 28/100 cells
equal to HARMONY (operator 7). TSML has 73/100. The question is why 28
and where those cells are.

Previous attempts (C9, first pass):
- Inner block rule `max(i,j)+1` for {1..6}×{1..6}: confirmed ✓
- DIS-based prediction (harmony = wobble fixed points): **FAILED**
- 32-4=28 via C×C ∪ D×D blocks: **FAILED**
- Row 7 rule `(j+7)%10`: **WRONG** (see correction below)
- 11 "residual" cells: unaccounted for — now closed by operator identity.

---

## The Ten TIG Operators

| # | Name | Role |
|---|------|------|
| 0 | VOID | Identity — absorbs to self |
| 1 | LATTICE | Structure, positive generator |
| 2 | COUNTER | Distinction, negative generator |
| 3 | PROGRESS | Forward motion |
| 4 | COLLAPSE | Compression, approach to threshold |
| 5 | BALANCE | Equilibrium, approach to threshold |
| 6 | CHAOS | Disruption — the **saturation operator** |
| 7 | HARMONY | Coherence — the **increment operator** |
| 8 | BREATH | Integration, rhythm, cyclicity |
| 9 | RESET | Completion, restart (also: FRUIT) |

Structural partitions used in derivation:
- **EARLY** = {1, 2, 3}: pre-threshold operators
- **TRANS** = {4, 5, 6}: transition zone (approach to HARMONY)
- **FUNC** = {8, 9}: functional wrap operators

---

## BHML Table

```
     0  1  2  3  4  5  6  7  8  9
  0: 0  1  2  3  4  5  6  7  8  9   ← VOID (identity)
  1: 1  2  3  4  5  6  7  2  6  6   ← LATTICE
  2: 2  3  3  4  5  6  7  3  6  6   ← COUNTER
  3: 3  4  4  4  5  6  7  4  6  6   ← PROGRESS
  4: 4  5  5  5  5  6  7  5  7  7   ← COLLAPSE
  5: 5  6  6  6  6  6  7  6  7  7   ← BALANCE
  6: 6  7  7  7  7  7  7  7  7  7   ← CHAOS (saturation)
  7: 7  2  3  4  5  6  7  8  9  0   ← HARMONY (increment)
  8: 8  6  6  6  7  7  7  9  7  8   ← BREATH (functional)
  9: 9  6  6  6  7  7  7  0  8  0   ← RESET (functional)
```

Verified: **BHML is symmetric** — BHML[i][j] = BHML[j][i] for all i, j.
Zero failures across all 100 cells.

---

## Rule A — VOID Identity (2 cells)

VOID is the identity operator by definition:

```
BHML[0][j] = j   for all j
BHML[i][0] = i   for all i
```

Setting j = 7: `BHML[0][7] = 7 = HARMONY`. By symmetry: `BHML[7][0] = 7`.

**Cells: (0,7) and (7,0)**

These are the only two harmony cells involving row or column 0.

---

## Rule B — Axis Saturation (17 cells)

**Inner block rule:**
```
BHML[i][j] = max(i,j) + 1   for i,j ∈ {1..6}
```
Verified: 36/36 cells, zero failures.

Harmony (=7) in the inner block when `max(i,j)+1 = 7`, i.e., `max(i,j) = 6`,
i.e., when **i = 6 or j = 6** (within {1..6}×{1..6}).

**CHAOS is the saturation operator.** Verified from table: `BHML[6][j] = 7`
for all j = 1..9. CHAOS composed with any non-VOID operator yields HARMONY.
This extends row 6 past the inner block boundary to j = 7, 8, 9. By
symmetry (BHML symmetric), col 6 extends to i = 7, 8, 9 as well.

**Row 6 harmony cells (j = 1..9):**
```
(6,1) (6,2) (6,3) (6,4) (6,5) (6,6) (6,7) (6,8) (6,9)   — 9 cells
```

**Col 6 harmony cells (i = 1..9, excluding row 6):**
```
(1,6) (2,6) (3,6) (4,6) (5,6) (7,6) (8,6) (9,6)          — 8 cells
```

**Total: 17 cells**

The axis = row 6 ∪ col 6 (i,j ≥ 1). CHAOS (6) is the saturation
boundary of the max+1 rule — the first value where `max(i,j)+1 = 7`.

---

## Rule C — Operator Identity (9 cells)

BREATH (8) and RESET (9) are **functional operators**. Their composition
behavior is determined by the **category** of the partner operator, not by
its position.

**Sub-rule C1 — BREATH/RESET × TRANS = HARMONY:**
```
BHML[8][j] = 7   for j ∈ {4, 5, 6}   (BREATH × COLLAPSE/BALANCE/CHAOS)
BHML[9][j] = 7   for j ∈ {4, 5, 6}   (RESET  × COLLAPSE/BALANCE/CHAOS)
```
Verified: 6/6 cells.

By symmetry: `BHML[j][8] = BHML[8][j]` and `BHML[j][9] = BHML[9][j]`.
So COLLAPSE and BALANCE (indices 4, 5) also produce HARMONY with BREATH
and RESET. (CHAOS = index 6 is already in Rule B as part of the axis.)

Functional interpretation: the transition-zone operators (COLLAPSE,
BALANCE, CHAOS) are "in approach" to HARMONY. BREATH — the integration
operator — and RESET — the completion operator — carry transition-zone
partners across the threshold to HARMONY.

**Cross-zone cells: (4,8) (4,9) (5,8) (5,9) (8,4) (8,5) (9,4) (9,5)** — 8 cells

**Sub-rule C2 — BREATH × BREATH = HARMONY (self-resonance):**
```
BHML[8][8] = 7
```
BREATH is the integration operator. Two integrations complete a cycle
and land at coherence. Double rhythm = completed oscillation = HARMONY.

**Self-resonance cell: (8,8)** — 1 cell

**Total Rule C: 9 cells**

---

## The Derivation Closed

| Rule | Mechanism | Count |
|------|-----------|-------|
| A — VOID identity | BHML[0][j]=j ⇒ (0,7); symmetry ⇒ (7,0) | 2 |
| B — Axis saturation | max(i,j)+1 rule, CHAOS boundary, row/col 6 | 17 |
| C — Operator identity | BREATH/RESET × TRANS + BREATH self-resonance | 9 |
| **Total** | | **28** |

**Overlaps: A∩B = 0, A∩C = 0, B∩C = 0.** Union = all 28 harmony cells
exactly. Verified computationally (test_bhml_operator_identity.py, Task 4
PASS, 0 failures).

---

## Correction: HARMONY Is the Increment Operator

Prior documentation (`TSML_BHML_LOOP.md`, `BHML_ATOMIC_STRUCTURE.md`)
stated:

> `BHML[7][j] = (j+7)%10`

**This is wrong.** Verified against all j = 1..9:

```
BHML[7][j] = (j+1)%10   for j = 1..9
BHML[7][0] = 7           (VOID identity)
```

`(j+7)%10` fails 9 of 9 cells for j ≥ 1.
`(j+1)%10` fails 0 of 9 cells.

HARMONY is the **increment operator** — it advances every operator by
exactly one step in the Z/10Z cycle. Row 7 is not a positional shift
by 7; it is the successor function on non-VOID operators.

The correction has been applied to all affected documents.

---

## Why No Positional Rule Exists for Rows 8 and 9

**Exhaustive proof:**
- No k ∈ {0..9} satisfies `BHML[8][j] = (j+k)%10` for all j.
- No k ∈ {0..9} satisfies `BHML[9][j] = (j+k)%10` for all j.

**Structural evidence:** BREATH harmony positions are {4,5,6,8} with gaps
{1,1,2} — non-uniform. A single modular shift requires uniform gaps. The
non-uniformity is not noise; it is the signature of a category rule.

**Why:** BREATH and RESET are functional operators. Positional shift rules
treat operators as points on a cycle and shift uniformly. Functional rules
treat the partner's category as the input. The categories EARLY, TRANS,
HARMONY, and FUNC are not equidistant in Z/10Z — they are semantic
partitions. A positional rule has no vocabulary for "transition zone
partner" vs "early operator." It is the wrong kind of rule.

This is documented as a **structural finding** (Tier C), not a gap.

---

## Complete Rule Set for BHML

```
BHML[0][j]  = j                    VOID identity (row)
BHML[i][0]  = i                    VOID identity (col)
BHML[i][j]  = max(i,j)+1  {1..6}   inner block
BHML[7][j]  = (j+1)%10   j ≥ 1    HARMONY increment
BHML[7][0]  = 7                    VOID identity
BHML[8][j]  = 6   j ∈ {1,2,3}     BREATH × EARLY = CHAOS
BHML[8][j]  = 7   j ∈ {4,5,6}     BREATH × TRANS = HARMONY
BHML[8][7]  = 9                    BREATH × HAR = RESET
BHML[8][8]  = 7                    BREATH × BREATH = HARMONY
BHML[8][9]  = 8                    BREATH × RESET = BREATH
BHML[9][j]  = 6   j ∈ {1,2,3}     RESET × EARLY = CHAOS
BHML[9][j]  = 7   j ∈ {4,5,6}     RESET × TRANS = HARMONY
BHML[9][7]  = 0                    RESET × HAR = VOID
BHML[9][8]  = 8                    RESET × BREATH = BREATH
BHML[9][9]  = 0                    RESET × RESET = VOID
BHML[i][j]  = BHML[j][i]          symmetric (100/100 cells)
```

These 16 rules fully specify the BHML table. Every entry follows from
exactly one rule.

---

## Connection to W_BHML and C8

C8 (Luther, March 31 2026) proved that `W_BHML = 3/50` is the per-step
C×D asymmetry across the natural 4-step generator orbit of (Z/10Z)*.

C9 (this result) proves that the 28 harmony cells of BHML — the physics
table driven by W_BHML — follow from three algebraic rules determined by
the operator identities of the TIG framework.

Together: the wobble (C8) quantifies the field; the operator rules (C9)
locate every HARMONY cell in that field. The two results are
complementary: C8 is the amplitude, C9 is the geometry.

---

## Tier Assessment

**C9: Tier C**

Verified against explicit BHML table (100 cells). Test:
`Gen10/papers/test_bhml_operator_identity.py` — all 5 tasks PASS.
Report: `Gen10/papers/results/bhml_operator_identity_report.txt`

| Claim | Tier | Verification |
|-------|------|--------------|
| Inner block: max(i,j)+1 for {1..6}×{1..6} | C | 36/36 cells ✓ |
| CHAOS = saturation operator (row/col 6 → HAR) | C | 9/9 + 8/8 ✓ |
| HARMONY = increment operator: (j+1)%10 | C | 9/9 cells ✓ |
| BREATH × TRANS = HARMONY | C | 3/3 cells ✓ |
| RESET × TRANS = HARMONY | C | 3/3 cells ✓ |
| BREATH × BREATH = HARMONY | C | 1/1 cells ✓ |
| 28-cell derivation closed (zero overlap, zero residual) | C | union = 28 exactly ✓ |
| No positional shift rule for rows 8-9 | C | exhaustive check (10 values of k) ✓ |

**Tier D target:** Prove that for any Z/nZ ring with operator table
defined by the same TIG functional categories, the number of HARMONY
cells and their positions follow from analogous rules. This requires
formalizing EARLY/TRANS/FUNC partitions for general n.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
