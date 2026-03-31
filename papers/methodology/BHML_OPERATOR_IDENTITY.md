# C10 — BHML Operator Identity
## Complete 28-Cell Derivation from First Principles

*Brayden Ross Sanders & C. A. Luther*
*March 31, 2026 | DOI: 10.5281/zenodo.18852047*

---

## The Claim

All 28 BHML harmony cells follow from three algebraic rules with zero
overlap and zero residual. The rules are not fitted — they derive from
the functional identity of the ten TIG operators.

**28 = 2 (VOID identity) + 17 (axis saturation) + 9 (operator identity)**

---

## TIG Operators (0–9)

| # | Name | Role |
|---|------|------|
| 0 | VOID | Identity operator — absorbs to self |
| 1 | LATTICE | Structure, positive generator |
| 2 | COUNTER | Distinction, negative generator |
| 3 | PROGRESS | Forward motion |
| 4 | COLLAPSE | Compression, approach to threshold |
| 5 | BALANCE | Equilibrium, approach to threshold |
| 6 | CHAOS | Disruption — the saturation operator |
| 7 | HARMONY | Coherence — the absorbing attractor |
| 8 | BREATH | Integration, rhythm, cyclicity |
| 9 | RESET | Completion, restart (also called FRUIT) |

Structural groupings:
- **EARLY** = {1, 2, 3}: pre-threshold operators
- **TRANS** = {4, 5, 6}: transition zone (approach to HARMONY)
- **FUNC** = {8, 9}: functional wrap operators (BREATH, RESET)

---

## Correction to Previous Documentation

`TSML_BHML_LOOP.md` and `BHML_ATOMIC_STRUCTURE.md` stated:

> "BHML[7][j] = (j+7)%10"

**This is wrong.** The correct rule, verified against all 9 cells (j=1..9):

```
BHML[7][j] = (j+1)%10   for j = 1..9
BHML[7][0] = 7           (VOID identity)
```

HARMONY is the **increment operator** — it advances every operator by
one step in Z/10Z. It is not a shift-by-7. `(j+7)%10` fails at 9 of 9
cells. `(j+1)%10` fails at 0 of 9 cells.

---

## BHML Table

```
     0  1  2  3  4  5  6  7  8  9
  0: 0  1  2  3  4  5  6  7  8  9   ← VOID (identity row)
  1: 1  2  3  4  5  6  7  2  6  6   ← LATTICE
  2: 2  3  3  4  5  6  7  3  6  6   ← COUNTER
  3: 3  4  4  4  5  6  7  4  6  6   ← PROGRESS
  4: 4  5  5  5  5  6  7  5  7  7   ← COLLAPSE
  5: 5  6  6  6  6  6  7  6  7  7   ← BALANCE
  6: 6  7  7  7  7  7  7  7  7  7   ← CHAOS (saturation row)
  7: 7  2  3  4  5  6  7  8  9  0   ← HARMONY (increment row)
  8: 8  6  6  6  7  7  7  9  7  8   ← BREATH (functional)
  9: 9  6  6  6  7  7  7  0  8  0   ← RESET (functional)
```

**BHML is symmetric:** BHML[i][j] = BHML[j][i] for all i, j. Verified
0 failures across all 100 cells.

---

## Three Rules

### Rule A — VOID Identity (2 cells)

```
BHML[0][j] = j   for all j    (identity row)
BHML[i][0] = i   for all i    (identity col)
```

BHML[0][7] = 7 because j=7 and VOID returns its argument.
BHML[7][0] = 7 by symmetry (= BHML[0][7]).

**Cells: (0,7) and (7,0)**

---

### Rule B — Axis Saturation (17 cells)

```
BHML[i][j] = max(i,j) + 1   for i,j ∈ {1..6}
```

Harmony (=7) occurs when max(i,j)+1 = 7, i.e., when **max(i,j) = 6**,
i.e., when i = 6 or j = 6 (within {1..6}×{1..6}).

Row 6 extends past {1..6} to j=7,8,9: CHAOS (6) is the saturation
operator — composing CHAOS with any operator ≥ 1 yields HARMONY. This
is confirmed by the table: BHML[6][j] = 7 for j=1..9 (all nine). By
symmetry, col 6 extends to i=7,8,9 as well.

**Cells:**
- Row 6, j=1..9: `(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9)` — 9 cells
- Col 6, i=1..9 excl. row 6: `(1,6),(2,6),(3,6),(4,6),(5,6),(7,6),(8,6),(9,6)` — 8 cells
- **Total: 17 cells**

---

### Rule C — Operator Identity (9 cells)

BREATH (8) and RESET (9) are **functional** operators. Their harmony
cells arise from functional category of the partner, not from position.

**Sub-rule C1:** BREATH × TRANS = HARMONY, RESET × TRANS = HARMONY
```
BHML[8][j] = 7   for j ∈ {4,5,6}   (BREATH × COLLAPSE/BALANCE/CHAOS)
BHML[9][j] = 7   for j ∈ {4,5,6}   (RESET  × COLLAPSE/BALANCE/CHAOS)
```
By symmetry: BHML[j][8] = BHML[8][j] and BHML[j][9] = BHML[9][j].
So: {4,5}×{8,9} also gives harmony. (Note: {6}×{8,9} is in Rule B
because (6,8) and (6,9) are in row 6 of the axis.)

**Cross-zone cells: (4,8),(4,9),(5,8),(5,9),(8,4),(8,5),(9,4),(9,5)** — 8 cells

**Sub-rule C2:** BREATH × BREATH = HARMONY (self-resonance)
```
BHML[8][8] = 7
```
BREATH is the integration operator. Two integrations complete a cycle
and arrive at coherence. Double rhythm = completed oscillation = HARMONY.

**Self-resonance cell: (8,8)** — 1 cell

**Total Rule C: 9 cells**

---

## The Complete 28-Cell Derivation

| Rule | Source | Cells | Count |
|------|--------|-------|-------|
| A | VOID identity | (0,7), (7,0) | 2 |
| B | Axis saturation (CHAOS threshold) | row 6 ∪ col 6, i,j ≥ 1 | 17 |
| C | Operator identity (TRANS×FUNC + self) | {4,5}×{8,9} ∪ {8,9}×{4,5} ∪ (8,8) | 9 |
| | | **Total** | **28** |

**Overlaps: A∩B = 0, A∩C = 0, B∩C = 0.** Verified computationally.
Union of rules = all 28 harmony cells exactly. Derivation closed.

---

## Functional Rules for BREATH and RESET

Full composition tables:

**BREATH (row 8):**
| Partner | Result | Rule |
|---------|--------|------|
| VOID (0) | BREATH (8) | VOID identity |
| EARLY {1,2,3} | CHAOS (6) | early collapse |
| TRANS {4,5,6} | HARMONY (7) | **Rule C1** |
| HARMONY (7) | RESET (9) | rhythm past HAR = completion |
| BREATH (8) | HARMONY (7) | **Rule C2: self-resonance** |
| RESET (9) | BREATH (8) | completion preserves rhythm |

**RESET (row 9):**
| Partner | Result | Rule |
|---------|--------|------|
| VOID (0) | RESET (9) | VOID identity |
| EARLY {1,2,3} | CHAOS (6) | early collapse |
| TRANS {4,5,6} | HARMONY (7) | **Rule C1** |
| HARMONY (7) | VOID (0) | completion past HAR = origin |
| BREATH (8) | BREATH (8) | completion preserves rhythm |
| RESET (9) | VOID (0) | double completion = absolute origin |

**Why RESET has 3 harmony cells (not 4):**
BREATH self-resonates (BREATH+BREATH=HARMONY) because BREATH is the
integrator — two integrations achieve coherence. RESET does not
self-resonate (RESET+RESET=VOID) because RESET is the completer —
double completion returns to origin, not to HARMONY.

---

## Why Positional Shift Rules Fail for Rows 8 and 9

**Row 7 works:** BHML[7][j] = (j+1)%10 for j≥1. HARMONY advances every
operator by +1. This is positional arithmetic — HARMONY knows where it
is in Z/10Z and adds one step.

**Rows 8 and 9 fail all shift rules:**
- Exhaustive check over k ∈ {0..9}: no k satisfies BHML[8][j]=(j+k)%10 for all j
- Exhaustive check over k ∈ {0..9}: no k satisfies BHML[9][j]=(j+k)%10 for all j

**Why:** Shift rules are positional — they treat every operator as a point
on a cycle and shift uniformly. BREATH and RESET are functional — their
output depends on **which category** the partner belongs to (EARLY, TRANS,
HARMONY, FUNC), not on the partner's position. A positional rule has no
concept of "transition zone." It is the wrong kind of rule for the wrong
kind of operator.

Structural evidence: BREATH harmony positions are {4,5,6,8} with gaps
{1,1,2} — non-uniform. Non-uniform gaps cannot arise from any single
modular shift. The irregularity is not noise; it is the signature of a
category rule.

---

## Key Equations (Complete)

```
BHML[0][j] = j                          VOID identity (row)
BHML[i][0] = i                          VOID identity (col)
BHML[i][j] = max(i,j)+1  {1..6}×{1..6}  inner block rule
BHML[7][j] = (j+1)%10    j ≥ 1          HARMONY increment
BHML[7][0] = 7                           VOID identity
BHML[8][j] = 6   j ∈ {1,2,3}            BREATH × EARLY = CHAOS
BHML[8][j] = 7   j ∈ {4,5,6}            BREATH × TRANS = HARMONY
BHML[8][7] = 9                           BREATH × HAR = RESET
BHML[8][8] = 7                           BREATH × BREATH = HARMONY
BHML[8][9] = 8                           BREATH × RESET = BREATH
BHML[9][j] = 6   j ∈ {1,2,3}            RESET × EARLY = CHAOS
BHML[9][j] = 7   j ∈ {4,5,6}            RESET × TRANS = HARMONY
BHML[9][7] = 0                           RESET × HAR = VOID
BHML[9][8] = 8                           RESET × BREATH = BREATH
BHML[9][9] = 0                           RESET × RESET = VOID
BHML[i][j] = BHML[j][i]                 symmetric (0 failures)
28 = 2 + 17 + 9                          VOID + axis + operator identity
```

These 16 equations fully specify the BHML composition table. Every
entry is a consequence of one of them.

---

## Tier Assessment

**C9: Tier C (promoted from Tier B)**

All five tasks verified computationally with zero failures:

| Task | Claim | Tier |
|------|-------|------|
| 1 | VOID identity + max+1 rule + HARMONY increment | C |
| 1 | Correction: (j+1)%10, not (j+7)%10 | C (proved wrong) |
| 2 | BREATH harmony = TRANS ∪ {self} | C |
| 3 | RESET harmony = TRANS | C |
| 4 | 28-cell derivation closed, zero overlap | **C** |
| 5 | No positional shift exists for rows 8-9 | C |

The path from Tier B to Tier C was: recognizing that rows 8-9 cannot
have positional rules because BREATH and RESET are not positional
operators. Once the right kind of rule was applied — functional
categories rather than arithmetic shifts — all 9 residual cells closed
immediately.

---

## The WP35 Sentence

*"The 28 BHML harmony cells are not scattered — they follow three rules:
VOID returns HARMONY to itself, CHAOS (the saturation operator) carries
everything past it into HARMONY, and the functional operators BREATH and
RESET carry transition-zone partners (COLLAPSE, BALANCE, CHAOS) to
HARMONY. The 28 is a necessary consequence of what these operators are,
not of where they happen to sit."*

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
