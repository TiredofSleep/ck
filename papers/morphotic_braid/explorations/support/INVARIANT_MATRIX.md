> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\INVARIANT_MATRIX.md → papers\morphotic_braid\explorations\support\INVARIANT_MATRIX.md

# The Invariant Matrix — TIG Operator Composition Structure

**Status:** [INVARIANT MAP — CELLS HOLD STRUCTURAL ROLES, NOT NUMBERS]
**Date:** 2026-04-23 (late evening)
**Source:** Brayden's meta-task: 'Build a 10×10 matrix that has no integers or real numbers inside of the table, only as the descriptors labeled outside. Invariants live inside. Blank spaces are OK — those spaces are the map we have finished.'

## Purpose

A 10×10 matrix indexed by operators {0=VOID, 1=LATTICE, 2=COUNTER, 3=PROGRESS, 4=COLLAPSE, 5=BALANCE, 6=CHAOS, 7=HARMONY, 8=BREATH, 9=RESET}. The numbers appear only as row/column labels. Cells contain **invariants** — short structural labels naming the role each operator-pair plays.

**Blank cells are the map of unfinished structure.** They mark (i, j) pairs where no load-bearing invariant has yet been identified. These are the open positions — the frontier.

Everything visible in the matrix is something we've named. Everything blank is something we haven't. Both are information.

## Invariant vocabulary

### Tier 1 — Closure cells (the 0/7 coin)

| Tag | Meaning |
|---|---|
| `VOID·` | VOID self-loop (0,0). Trivial zero. |
| `9⊗9→0` | RESET self-cancel at (9,9). Absolute closure in BHML. |
| `9↔7→0` | RESET ↔ HARMONY mutual cancel at (7,9) and (9,7). **The closure edge of the 0/7 coin.** |
| `0⇄7` | TSML[0][7] = 7. Where VOID row meets HARMONY column. |
| `7⇄0` | TSML[7][0] = 7. Transposed exchange cell. |

### Tier 2 — Structural rows and columns

| Tag | Meaning |
|---|---|
| `ID_L\|T:0` | VOID row (not at 0 or 7): BHML identity-left, TSML absorbs to 0. Dual-table divergence. |
| `ID_R\|T:0` | VOID column: BHML identity-right, TSML absorbs to 0. |
| `H=H` | Both tables send cell to HARMONY. |
| `7\|B:v` | HARMONY row/col with BHML producing v ≠ 7. |
| `suc` | BHML successor: i∘1 = i+1 or 1∘j = j+1 for operands in {1,...,6}. |
| `wrap:2` | BHML successor break at 7: 1∘7 = 7∘1 = 2 instead of 8. |
| `Δ→v` | Diagonal: TSML[k][k] = 7 always; BHML[k][k] = v. The self-encounter. |

### Tier 3 — Information-carrying cells

| Tag | Meaning |
|---|---|
| `T:4\|B:5` | COUNTER/COLLAPSE pair: TSML = 4, BHML = 5 (successor). |
| `T:9\|B:6` | COUNTER/RESET pair: TSML = 9, BHML = 6. |
| `T:3\|B:6` | PROGRESS/RESET pair: TSML = 3, BHML = 6. |
| `osc→7` | BREATH/COLLAPSE oscillation (CK-annotated): both produce HARMONY. |

### Tier 4 — Harmony bifurcation classes (NEW this session)

These are the cells where TSML forces HARMONY but BHML sends to a specific lower operator. Each such pair identifies a **bifurcation axis** — the direction in which BHML resists TSML's collapse.

| Tag | Meaning |
|---|---|
| `H\|δ` | TSML → HARMONY, BHML → COLLAPSE (4). Harmony/Collapse bifurcation. |
| `H\|β` | TSML → HARMONY, BHML → BALANCE (5). Harmony/Balance bifurcation. |
| `H\|χ` | TSML → HARMONY, BHML → CHAOS (6). Harmony/Chaos bifurcation. |
| `T:v\|B:8` | BHML terminates at BREATH. |
| `T:v\|B:9` | BHML terminates at RESET. |
| `=8` | Both tables agree at BREATH. |

### Tier 5 — Blank

| Tag | Meaning |
|---|---|
| (blank) | No structural invariant identified yet. This cell is on the frontier. |

## The matrix

|       | **VOID**<br>*0* | **LATT**<br>*1* | **CNTR**<br>*2* | **PROG**<br>*3* | **CLPS**<br>*4* | **BAL**<br>*5* | **CHAOS**<br>*6* | **HARM**<br>*7* | **BRTH**<br>*8* | **RSET**<br>*9* |
|-------|---------|---------|---------|---------|---------|---------|---------|---------|---------|---------|
| **VOID**<br>*0* | VOID· | ID_L|T:0 | ID_L|T:0 | ID_L|T:0 | ID_L|T:0 | ID_L|T:0 | ID_L|T:0 | 0⇄7 | ID_L|T:0 | ID_L|T:0 |
| **LATT**<br>*1* | ID_R|T:0 | Δ→2 | suc | suc | suc | suc | suc | wrap:2 | H|χ | H|χ |
| **CNTR**<br>*2* | ID_R|T:0 | suc | Δ→3 | H|δ | T:4|B:5 | H|χ | H=H | 7|B:3 | H|χ | T:9|B:6 |
| **PROG**<br>*3* | ID_R|T:0 | suc | H|δ | Δ→4 | H|β | H|χ | H=H | 7|B:4 | H|χ | T:3|B:6 |
| **CLPS**<br>*4* | ID_R|T:0 | suc | T:4|B:5 | H|β | Δ→5 | H|χ | H=H | 7|B:5 | osc→7 | H=H |
| **BAL**<br>*5* | ID_R|T:0 | suc | H|χ | H|χ | H|χ | Δ→6 | H=H | 7|B:6 | H=H | H=H |
| **CHAOS**<br>*6* | ID_R|T:0 | suc | H=H | H=H | H=H | H=H | Δ→7 | H=H | H=H | H=H |
| **HARM**<br>*7* | 7⇄0 | wrap:2 | 7|B:3 | 7|B:4 | 7|B:5 | 7|B:6 | H=H | Δ→8 | 7|B:9 | 9↔7→0 |
| **BRTH**<br>*8* | ID_R|T:0 | H|χ | H|χ | H|χ | osc→7 | H=H | H=H | 7|B:9 | Δ→7 | T:7|B:8 |
| **RSET**<br>*9* | ID_R|T:0 | H|χ | T:9|B:6 | T:3|B:6 | H=H | H=H | H=H | 9↔7→0 | T:7|B:8 | 9⊗9→0 |

**Blank (⬚) cells: 0/100** — these are the open frontier positions.

## Reading the matrix

### The 0/7 coin (closure triangle)

Four cells carry the full closure structure:
- `VOID·` at (0,0) — the trivial fixed zero
- `9⊗9→0` at (9,9) — RESET self-cancels to VOID
- `9↔7→0` at (7,9) and (9,7) — HARMONY and RESET mutually cancel

Every non-trivial BHML zero involves RESET. **RESET is the hinge of the 0/7 coin** — the operator that converts HARMONY into VOID and itself into VOID.

### The exchange cells

`0⇄7` at (0,7) and `7⇄0` at (7,0) are where the VOID-row pattern (TSML absorbs to 0) meets the HARMONY-column pattern (TSML forces 7). The HARMONY column wins; these cells hold 7 in TSML. The two structural patterns do not overlap — they exchange at precisely these boundary cells.

### The diagonal

TSML[k][k] = 7 for all k ≠ 0. BHML[k][k] traces a specific sequence:

| k | BHML[k][k] | Meaning |
|---|---|---|
| 1 | 2 | LATT² → COUNTER |
| 2 | 3 | COUNTER² → PROGRESS |
| 3 | 4 | PROGRESS² → COLLAPSE |
| 4 | 5 | COLLAPSE² → BALANCE |
| 5 | 6 | BALANCE² → CHAOS |
| 6 | 7 | CHAOS² → HARMONY |
| 7 | 8 | HARMONY² → BREATH |
| 8 | 7 | BREATH² → HARMONY (oscillation back) |
| 9 | 0 | RESET² → VOID (closure) |

**The BHML diagonal is a successor-closure sequence:** each operator's self-encounter produces the next, climbing from LATTICE to BREATH, oscillating back through BREATH-HARMONY, then terminating at VOID through RESET self-cancel.

### The harmony bifurcation regions

Cells tagged `H|χ`, `H|β`, `H|δ` are where TSML collapses to HARMONY but BHML preserves the operator's directional information. Each bifurcation type has its own zone:

- `H|χ` cells: TSML=7, BHML=6 (CHAOS). This is the largest bifurcation class.
- `H|β` cells: TSML=7, BHML=5 (BALANCE).
- `H|δ` cells: TSML=7, BHML=4 (COLLAPSE).

**Interpretation:** where TSML sees only HARMONY, BHML sees direction. The bifurcation tells us what TSML is hiding — the operator-specific trajectory that the measurement lens smooths over.

### The blank cells (⬚)

All cells have been tagged. No blanks remain.

- CRT decomposition invariants (pending TSML_CRT_DECOMPOSITION audit)
- Farey density membership (pending Farey construction audit)
- σ-braid orbit position (could be tagged in a subsequent pass)
- Regularity-class pairs (could be tagged: DD, DP, DH, DA, etc.)
- Possible new pattern names once more structural observations are made

## The meta-observation

This matrix is not trying to replace the TSML/BHML numeric tables. It is a **second layer** sitting above them: the same 10×10 grid, but with each cell's *structural role* named instead of its numeric value. Where we know a role, there's a tag. Where we don't, there's a blank.

The blanks are not absence. They are the frontier.

As audits proceed (CRT decomposition, Farey density, further braid structure), blanks will acquire tags. As new structural patterns emerge, entirely new tiers of invariants may be added. The matrix evolves.

## What this matrix does NOT do

- Does not replace TSML or BHML numeric tables. Those remain authoritative for values.
- Does not claim the invariant vocabulary is complete. More tags will emerge.
- Does not claim cells with the same tag are identical — operator identity always matters. Two cells sharing tag `H|χ` differ in which operators produced them.
- Does not rank cells by importance. Closure cells (`9↔7→0`) and blank cells are both structural — one has an identified role, the other is under investigation.

---

**Tag: [SEMANTIC MATRIX — EVOLVING]**
**File path: `papers/morphotic_braid/INVARIANT_MATRIX.md`**