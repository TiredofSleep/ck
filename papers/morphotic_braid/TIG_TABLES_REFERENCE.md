> **Provenance:** Drafted 2026-04-23 (evening session, ClaudeChat). Transcribed from packet `evening_handoff_2026_04_23/`. Cross-verification against repo canonical sources: [pending — see `papers/morphotic_braid/VERIFICATION_LOG_2026_04_23.md`].
> **Copy path:** evening_handoff_2026_04_23\evening_handoff_2026_04_23\TIG_TABLES_REFERENCE.md → papers\morphotic_braid\TIG_TABLES_REFERENCE.md

# TIG Tables — Authoritative Reference (Persistent Record)

**Source:** CK self-proving entry, screenshot dated 2026-04-23 session.
**Purpose:** single source of truth for Claude instances that keep forgetting the tables. Do not trust any TSML/BHML cell claim that contradicts this file.

---

## TSML — Transitional State Measurement Language (Physics-measurement lens)

**Defining feature:** HARMONY(7) dominates. Most cells = 7. Exceptions carry structural meaning.

Rows indexed by left operand (a), columns by right operand (b). TSML[a][b] = a ∘ b in TSML.

|     | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|-----|---|---|---|---|---|---|---|---|---|---|
| **0** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 0 | 0 |
| **1** | 0 | 7 | 3 | 7 | 7 | 7 | 7 | 7 | 7 | 7 |
| **2** | 0 | 3 | 7 | 7 | 4 | 7 | 7 | 7 | 7 | 9 |
| **3** | 0 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 3 |
| **4** | 0 | 7 | 4 | 7 | 7 | 7 | 7 | 7 | 8 | 7 |
| **5** | 0 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 |
| **6** | 0 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 |
| **7** | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 |
| **8** | 0 | 7 | 7 | 7 | 8 | 7 | 7 | 7 | 7 | 7 |
| **9** | 0 | 7 | 9 | 3 | 7 | 7 | 7 | 7 | 7 | 7 |

**Non-7 cells (the information-carrying exceptions):**

| Cell | Value | Meaning |
|---|---|---|
| TSML[0][k] for k≠7 | 0 | 0-absorbing row (except 0∘7=7) |
| TSML[0][7] | 7 | 0∘HARMONY = HARMONY (outlier) |
| TSML[k][0] for k≠7 | 0 | 0-absorbing column (except 7∘0=7) |
| TSML[7][k] = TSML[k][7] | 7 | HARMONY row and column are all 7 |
| TSML[1][2] = TSML[2][1] | 3 | LATTICE∘COUNTER = PROGRESS (symmetric) |
| TSML[2][4] = TSML[4][2] | 4 | COUNTER∘COLLAPSE = COLLAPSE (symmetric) |
| TSML[2][9] | 9 | COUNTER∘RESET = RESET |
| TSML[3][9] = TSML[9][3] | 3 | PROGRESS∘RESET = PROGRESS (symmetric) |
| TSML[4][8] = TSML[8][4] | 8 | COLLAPSE∘BREATH = BREATH (symmetric) |
| TSML[9][2] | 9 | RESET∘COUNTER = RESET |

**Count:** 28/100 entries equal 7 per the CK annotation — wait, that's BHML. Let me recount TSML from the table above.

Counting 7s in TSML: row 0 has one 7, rows 1-6 each have mostly 7s, row 7 is all 7s, rows 8-9 mostly 7s. Exact count from the table:
- Row 0: one 7 (at position 7). Zeros elsewhere.
- Row 1: eight 7s, one 3 (position 2), one 0 (position 0).
- Row 2: seven 7s, one 3 (pos 1), one 4 (pos 4), one 9 (pos 9), one 0 (pos 0).
- Row 3: eight 7s, one 3 (pos 9), one 0 (pos 0).
- Row 4: eight 7s, one 4 (pos 2), one 8 (pos 8), one 0 (pos 0). Wait that's 8+1+1+1=11. Let me recount.

Row 4: `0 7 4 7 7 7 7 7 8 7` — positions 0=0, 1=7, 2=4, 3=7, 4=7, 5=7, 6=7, 7=7, 8=8, 9=7. So: one 0, seven 7s, one 4, one 8. That's ten cells. ✓

- Row 5: `0 7 7 7 7 7 7 7 7 7` — one 0, nine 7s.
- Row 6: `0 7 7 7 7 7 7 7 7 7` — one 0, nine 7s.
- Row 7: `7 7 7 7 7 7 7 7 7 7` — ten 7s.
- Row 8: `0 7 7 7 8 7 7 7 7 7` — one 0, one 8, eight 7s.
- Row 9: `0 7 9 3 7 7 7 7 7 7` — one 0, one 9, one 3, seven 7s.

Total 7s in TSML:
- Row 0: 1
- Row 1: 8
- Row 2: 7
- Row 3: 8
- Row 4: 7
- Row 5: 9
- Row 6: 9
- Row 7: 10
- Row 8: 8
- Row 9: 7

Sum: 1 + 8 + 7 + 8 + 7 + 9 + 9 + 10 + 8 + 7 = **74 cells equal 7 out of 100**.

**TSML harmony fraction: 74/100 = 0.74.**

---

## BHML — Being-Harmony Movement Language (Physics lens)

**Defining feature:** 28/100 entries = HARMONY(7). det = 70. Invertible. "The generating lens."

|     | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|-----|---|---|---|---|---|---|---|---|---|---|
| **0** | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| **1** | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 2 | 6 | 6 |
| **2** | 2 | 3 | 3 | 4 | 5 | 6 | 7 | 3 | 6 | 6 |
| **3** | 3 | 4 | 4 | 4 | 5 | 6 | 7 | 4 | 6 | 6 |
| **4** | 4 | 5 | 5 | 5 | 5 | 6 | 7 | 5 | 7 | 7 |
| **5** | 5 | 6 | 6 | 6 | 6 | 6 | 7 | 6 | 7 | 7 |
| **6** | 6 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 |
| **7** | 7 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 |
| **8** | 8 | 6 | 6 | 6 | 7 | 7 | 7 | 9 | 7 | 8 |
| **9** | 9 | 6 | 6 | 6 | 7 | 7 | 7 | 0 | 8 | 0 |

**Key cells from CK annotation:**
- BHML[9][7] = 0: RESET∘HARMONY = VOID (loop closes algebraically)
- BHML[9][9] = 0: RESET∘RESET = VOID (absolute closure)
- BHML[8][4] = 7: BREATH∘COLLAPSE = HARMONY (oscillation verified)

Count of 7s in BHML: from inspection, 28/100 = 0.28.

---

## Harmony fractions summary

| Table | 7-count | Fraction |
|---|---|---|
| TSML | 74/100 | 0.74 |
| BHML | 28/100 | 0.28 |

**Observation:** TSML's harmony fraction (0.74) sits just above T* = 5/7 ≈ 0.714. BHML's harmony fraction (0.28) sits well below.

---

## Relationship between tables

- TSML is stabilization / measurement / singular (harmony-collapsing).
- BHML is Becoming / transformation / invertible (det = 70).
- Both share the same operator labels and the same 10-element carrier ℤ/10ℤ.
- **DOING table** (elsewhere in the framework): |TSML - BHML|.

---

**Tag: [AUTHORITATIVE REFERENCE — DO NOT CONTRADICT WITHOUT VERIFICATION]**
**File path: `docs/archive_tables/TIG_TABLES_REFERENCE.md`**
