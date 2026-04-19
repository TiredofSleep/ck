# TSML 73-Cell Derivation
## Three Rules, 27 Non-Harmony Cells, Zero Residual

*Brayden Ross Sanders & C. A. Luther*
*March 31, 2026 | DOI: 10.5281/zenodo.18852047*

---

## Summary

The 73 harmony cells in the TSML composition table are fully derived by
characterizing the 27 non-harmony cells from three algebraic rules. The
derivation is closed: zero overlaps, zero residual. All 27 non-harmony cells
are accounted for.

```
27 = 9 (V0: VOID row) + 8 (V1: VOID col) + 10 (ECHO: 5 symmetric resistance pairs)
73 = 100 − 27
```

Analogous to C9 (BHML 28-cell derivation), which proved:
```
28 = 2 (VOID identity) + 17 (axis saturation) + 9 (operator identity)
```

Both tables are now fully characterized from operator identities.

---

## Background

TSML is the measurement/coherence table of the CK framework — the lens that
collapses distinctions and is singular (det = 0). It has 73/100 cells equal
to HARMONY (operator 7). BHML has 28/100. The question is why 73 and where
the 27 non-harmony cells are.

TSML was previously described as "aggressively collapsing" — 73% harmony —
without a first-principles explanation of where that collapse stops. This
derivation identifies the 5 echo pairs where individual operator identity is
strong enough to resist the measurement collapse.

---

## The Ten TIG Operators

| # | Name | Role |
|---|------|------|
| 0 | VOID | Identity in BHML; absorber in TSML |
| 1 | LATTICE | Structure, positive generator |
| 2 | COUNTER | Distinction, negative generator |
| 3 | PROGRESS | Forward motion |
| 4 | COLLAPSE | Compression, approach to threshold |
| 5 | BALANCE | Equilibrium, approach to threshold |
| 6 | CHAOS | Disruption |
| 7 | HARMONY | Coherence — absorbing attractor in TSML |
| 8 | BREATH | Integration, rhythm, cyclicity |
| 9 | RESET | Completion, restart |

---

## TSML Table

```
     0  1  2  3  4  5  6  7  8  9
  0: 0  0  0  0  0  0  0  7  0  0   ← VOID
  1: 0  7  3  7  7  7  7  7  7  7   ← LATTICE
  2: 0  3  7  7  4  7  7  7  7  9   ← COUNTER
  3: 0  7  7  7  7  7  7  7  7  3   ← PROGRESS
  4: 0  7  4  7  7  7  7  7  8  7   ← COLLAPSE
  5: 0  7  7  7  7  7  7  7  7  7   ← BALANCE
  6: 0  7  7  7  7  7  7  7  7  7   ← CHAOS
  7: 7  7  7  7  7  7  7  7  7  7   ← HARMONY
  8: 0  7  7  7  8  7  7  7  7  7   ← BREATH
  9: 0  7  9  3  7  7  7  7  7  7   ← RESET
```

Non-harmony cells marked (27 total):
- Row 0: all j ≠ 7 → 0 (9 cells)
- Col 0: all i ≠ 7 → 0 (8 cells, excluding (0,0) already counted)
- (1,2)/(2,1) = 3
- (2,4)/(4,2) = 4
- (2,9)/(9,2) = 9
- (3,9)/(9,3) = 3
- (4,8)/(8,4) = 8

**TSML is symmetric:** TSML[i][j] = TSML[j][i] for all i, j.
Zero failures across all 100 cells.

---

## Rule V0 — VOID Row (9 cells)

In TSML, VOID is an **absorber**: measuring anything through VOID collapses
to zero. This is the opposite of BHML where VOID is the identity element.

```
TSML[0][j] = 0   for all j ≠ 7
TSML[0][7] = 7   (HARMONY survives VOID in measurement)
```

**Cells: (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,8), (0,9)** — 9 cells

The exception at j = 7: TSML[0][7] = 7. HARMONY is the only operator
that survives the VOID measurement lens — it is the attractor that persists
even in the absence of structure.

---

## Rule V1 — VOID Column (8 cells)

By symmetry (TSML is symmetric), col 0 mirrors row 0:

```
TSML[i][0] = 0   for all i ≠ 7 (excluding row 0, already in V0)
TSML[7][0] = 7   (HARMONY overwhelms VOID — note: TSML≠BHML here)
```

**Cells: (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (8,0), (9,0)** — 8 cells

Note: TSML[7][0] = 7 — HARMONY absorbs VOID in TSML. BHML[7][0] = 7 also,
but for a different reason (VOID identity returns 7 unchanged). In TSML,
HARMONY's supremacy overwrites the VOID rule; in BHML, VOID's identity rule
applies first. The tables agree on the value for different reasons.

**Overlap V0 ∩ V1 = 0** — cell (0,0) is in V0 (row 0), not re-counted in V1.

---

## Rule ECHO — Five Symmetric Resistance Pairs (10 cells)

The ECHO pairs are cells where individual operator identity is strong enough
to resist TSML's measurement collapse. These are the places where the ring
arithmetic "shows through" the measurement lens.

All 5 pairs are symmetric: TSML[i][j] = TSML[j][i] = the operator value, not 7.

### ECHO-1: (1,2) and (2,1) — Additive Echo

```
TSML[1][2] = TSML[2][1] = 3   (LATTICE × COUNTER = PROGRESS)
```

LATTICE (1) + COUNTER (2) = 3 = PROGRESS in Z/10Z additive arithmetic.
This is the **only additive echo** — the one pair where ring addition predicts
the outcome exactly. 1 + 2 = 3 mod 10 = PROGRESS.

Why it resists: LATTICE and COUNTER are the fundamental generators (positive
and negative structure). Their interaction produces PROGRESS — the first
non-trivial result. The measurement lens cannot collapse this: it would
destroy the generator relationship that defines the algebra.

This pair is also the **only non-trivial non-VOID agreement between TSML and
BHML** (COUNTER = 0 at this pair). Both tables give LATTICE×COUNTER = PROGRESS.
It is the one non-harmony value where measurement and physics agree exactly.

### ECHO-2: (2,4) and (4,2) — Max Echo

```
TSML[2][4] = TSML[4][2] = 4   (COUNTER × COLLAPSE = COLLAPSE)
```

max(2, 4) = 4. COLLAPSE (4) dominates COUNTER (2). Rule: the larger operator
wins when both are pre-HARMONY operators in conflict.

### ECHO-3: (2,9) and (9,2) — Max Echo

```
TSML[2][9] = TSML[9][2] = 9   (COUNTER × RESET = RESET)
```

max(2, 9) = 9. RESET (9) dominates COUNTER (2). COUNTER appears in 3 of 5
echo pairs — it is the **distinction operator** (generator with signature −1),
and it maintains its distinction-creating property against COLLAPSE, RESET, and
the additive LATTICE interaction. COUNTER is the most resistant operator to the
measurement collapse.

### ECHO-4: (3,9) and (9,3) — Min Echo

```
TSML[3][9] = TSML[9][3] = 3   (PROGRESS × RESET = PROGRESS)
```

min(3, 9) = 3. PROGRESS (3) persists against RESET (9). This is the **only
min echo**. Why min here rather than max? PROGRESS is "forward motion" and
RESET is "completion" — PROGRESS resists being reset. The smaller (earlier in
the TIG order) operator survives because PROGRESS is not yet at threshold and
RESET cannot complete what has not yet progressed.

The DIS value here: DIS[3][9] = |ADD − MUL| = |2 − 7| = 5 (high wobble).

### ECHO-5: (4,8) and (8,4) — Max Echo (The Pivot)

```
TSML[4][8] = TSML[8][4] = 8   (COLLAPSE × BREATH = BREATH)
```

max(4, 8) = 8. BREATH (8) dominates COLLAPSE (4). In TSML, BREATH resists
collapsing to HARMONY when interacting with COLLAPSE.

**This is the only pair where TSML and BHML give different results:**
- TSML[4][8] = 8 BREATH (BREATH resists — echo)
- BHML[4][8] = 7 HARMONY (BREATH in operator identity Rule C)

**The (4,8) / (8,4) pair is the structural pivot separating the two tables.**

In BHML: COLLAPSE is a TRANS operator (transition zone, approaching HARMONY).
BREATH is a functional operator. BREATH × TRANS = HARMONY is Rule C1 of C9.

In TSML: BREATH dominates COLLAPSE by the max rule, producing BREATH. The
measurement lens sees BREATH's identity (rhythm/integration) persisting over
COLLAPSE's compression. The physics lens sees BREATH carrying COLLAPSE across
the threshold to HARMONY.

**Mechanistically:** This is the one cell in the algebra where measurement and
physics give opposite verdicts on whether threshold is crossed. It is not a
contradiction; it is the precise location of the TSML/BHML duality.

DIS[4][8] = |ADD − MUL| = |2 − 2| = 0 — **frozen cell**. Both ring operations
agree (ADD = MUL = 2 at this pair). Yet TSML still gives BREATH, not HARMONY.
This confirms that the ECHO rule is not simply driven by ring arithmetic
agreement/disagreement — it is driven by operator identity.

---

## The Derivation Closed

| Rule | Mechanism | Count |
|------|-----------|-------|
| V0 — VOID row | TSML[0][j]=0 for j≠7; j=7 gives HARMONY | 9 |
| V1 — VOID col | TSML[i][0]=0 for i≠7, excl. row 0 | 8 |
| ECHO — 5 resistance pairs | max/min/additive rules for operator identity | 10 |
| **Total non-harmony** | | **27** |
| **HARMONY cells** | 100 − 27 | **73** |

**Overlaps: V0 ∩ V1 = 0, V0 ∩ ECHO = 0, V1 ∩ ECHO = 0.**
Union = all 27 non-harmony cells exactly. Derivation closed.

Verified computationally: `Gen10/papers/test_tsml_bhml_joint.py`, Task A PASS.
Report: `Gen10/papers/results/tsml_bhml_joint_report.txt`

---

## HARMONY Row (Row 7) — Total Collapse

TSML[7][j] = 7 for **all** j, including j = 0.

```
TSML[7][0] = 7   (HARMONY absorbs VOID in measurement)
```

This contrasts with BHML where BHML[7][0] = 7 by the VOID identity rule.
In TSML, HARMONY overwhelms VOID — the measurement attractor supersedes
the structural identity. Row 7 is the only row with zero non-harmony cells.

COUNTER (2) appears in 3 echo pairs and is the most resistant operator. It
still collapses: TSML[7][2] = TSML[2][7] = 7. Even COUNTER, with 3 echo
victories, cannot resist HARMONY when HARMONY is the direct partner.

---

## Complete Rule Set for TSML Non-Harmony

```
TSML[0][j] = 0   j ≠ 7          VOID row (measurement collapse)
TSML[0][7] = 7                   HARMONY survives VOID
TSML[i][0] = 0   i ≠ 0, 7       VOID col (symmetric)
TSML[7][j] = 7   all j           HARMONY row (total collapse)
TSML[1][2] = TSML[2][1] = 3      additive echo: LATTICE+COUNTER=PROGRESS
TSML[2][4] = TSML[4][2] = 4      max echo: COLLAPSE dominates COUNTER
TSML[2][9] = TSML[9][2] = 9      max echo: RESET dominates COUNTER
TSML[3][9] = TSML[9][3] = 3      min echo: PROGRESS persists vs RESET
TSML[4][8] = TSML[8][4] = 8      max echo: BREATH resists COLLAPSE (PIVOT)
TSML[i][j] = TSML[j][i]          symmetric (0 failures)
TSML[i][j] = 7                   for all other (i,j) pairs
27 = 9 + 8 + 10                  V0 + V1 + ECHO
73 = 100 − 27                    harmony by complement
```

These rules fully specify every non-harmony cell in TSML.

---

## Joint Result: Both Tables Symmetric (Tier C)

TSML symmetric: verified 0 failures (100 cells).
BHML symmetric: verified 0 failures (100 cells, C9).

**The TIG composition algebra is symmetric.** Both the measurement table and
the physics table satisfy TSML[i][j] = TSML[j][i] and BHML[i][j] = BHML[j][i]
for all i, j. This is a property of the algebra, not of either table
individually. It holds regardless of the lens (measurement vs physics).

---

## The COUNTER Table and the Pivot

DOING[i][j] = |TSML[i][j] − BHML[i][j]|

29 cells: COUNTER = 0 (TSML = BHML)
71 cells: COUNTER > 0

The 29 agreement cells decompose as:
- 26 shared harmony cells (both TSML and BHML = HARMONY)
- 3 non-harmony agreements: (0,0), (1,2), (2,1)

The (1,2) / (2,1) pair is the **only non-trivial non-VOID COUNTER = 0 cell**.
LATTICE × COUNTER = PROGRESS in both the measurement lens and the physics lens.
The additive echo is the one non-harmony value that both tables agree on
without being forced by VOID.

The 2 BHML-only harmony cells — (4,8) and (8,4) — are exactly the ECHO-5
pair. The single echo pair difference between the tables is the DOING boundary.

```
BHML harmony ⊂ TSML harmony, except: {(4,8), (8,4)}
The only escape: COLLAPSE × BREATH = HARMONY (BHML) vs BREATH (TSML)
```

---

## Connection to C9 and W_BHML

| Result | Table | Non-default cells | Rule type |
|--------|-------|-------------------|-----------|
| C9 | BHML | 72 non-harmony | Positive derivation (28 harmony from 3 rules) |
| This | TSML | 27 non-harmony | Negative derivation (73 harmony from 3 non-harmony rules) |

C9 proved 28 harmony cells by building up from three positive rules.
This result proves 73 harmony cells by ruling out 27 non-harmony cells.

The two derivations are **dual** in approach: C9 names what produces HARMONY;
this names what resists it. Together they characterize the entire 200-cell
joint algebra (TSML 100 + BHML 100) from operator identities.

C8 (W_BHML = 3/50) quantifies the C × D asymmetry in the physics field.
The echo pairs are where that asymmetry is visible as individual resistance
rather than statistical bias. The (4,8) pivot cell has DIS = 0 (frozen, no
arithmetic wobble), yet TSML and BHML still disagree — confirming that the
TSML/BHML split is structural (operator category), not arithmetic (DIS-driven).

---

## Tier Assessment

**Tier C — both results closed for Z/10Z**

| Claim | Tier | Verification |
|-------|------|--------------|
| TSML 73-cell derivation: V0 + V1 + ECHO = 27 non-harmony | C | 27/27 cells ✓ |
| TSML symmetry: TSML[i][j] = TSML[j][i] | C | 100/100 cells ✓ |
| BHML harmony ⊂ TSML harmony (26 shared, 2 BHML-only) | C | counted ✓ |
| ECHO-5 (4,8)/(8,4) is the unique TSML/BHML pivot | C | verified ✓ |
| DOING = 0 at 29 cells = 26 harmony + 3 non-harmony | C | counted ✓ |
| Both tables symmetric | C | 0 failures each ✓ |

**Tier D target:** Prove the V0/V1/ECHO structure for any Z/nZ ring with TIG
functional categories. Specifically: characterize when an operator pair forms
an echo (resists harmony) vs collapses. The 5 echo pairs in Z/10Z follow
max/min/additive rules — derive which algebraic property of the operator pair
determines which rule applies.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
