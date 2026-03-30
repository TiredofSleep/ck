# TSML Reconstruction from Invariants and Integers
## What Is Forced, What Is Chosen, What Remains Underdetermined

*Brayden Sanders / 7Site LLC | March 2026*
*Methodology: independent derivation only. TSML not assumed unless explicitly checking recovery.*

---

## Result Summary

**TSML is not uniquely determined by invariants I1–I10.**

It is one member of a small family. The family is characterized by 24 forced cells, 49 cells assigned HAR by the maximization principle (I6), and **8 genuinely underdetermined cells**. Among the 8, 6 are predicted by the integer law max(s,c). The remaining 2 — F(1,2)=3 and F(2,1)=3 — are not predicted by any simple integer function tested.

**TSML is special inside its family in two ways:**
1. It maximizes HAR assignments in the free cells (I6)
2. The 8 non-HAR values follow max(s,c) for 6 of 8 pairs

The 2 exceptions (F(1,2)=F(2,1)=3) remain genuinely underdetermined by the current invariant set.

---

## Section 1: Formal Invariant Basis

| ID | Invariant | Type | Verified |
|----|-----------|------|---------|
| I1 | F(s,7)=7 for all s (HAR absorbing) | Exact | ✓ |
| I2 | C = {s : gcd(s,10)=1} = {1,3,7,9} | Exact | ✓ |
| I3 | F(s,c) ∈ C for all s,c ∈ C (sub-magma) | Exact | ✓ |
| I4 | F(s,c) ∉ G for any s ∈ C, c ∈ A (one-way gate) | Exact | ✓ |
| I5 | F(s,c) = F(c,s) for all s,c (self-adjoint) | Exact | ✓ |
| I6 | Maximize \|{(s,c): F(s,c)=7}\| subject to I1–I5 | Computed | ✓ (71 pairs) |
| I7 | Algebraic chain {7} ⊊ C ⊊ A has depth 3 | Exact | ✓ |
| I8 | F(3,9)=3 and F(9,3)=3 (orbit zone) | Exact | ✓ |
| I9 | F(1,c)=7 for all c ∈ C (state-1 direct feeder) | Exact | ✓ |
| I10 | ∃c ∈ C: F(g,c)=7 for all g ∈ G | Exact | ✓ |

**9 exact/verified, 1 computed (I6 is a maximization target, not a structural theorem)**

---

## Section 2: Forced-Cell Analysis

Starting from I1–I10 only, without assuming TSML:

**Forced to specific value (24/81 cells):**

| Rule | Cells forced | Value |
|------|-------------|-------|
| I1: F(s,7)=7 | 9 cells (column 7) | HAR |
| I1+I5: F(7,c)=7 | 8 more (row 7, non-diagonal) | HAR |
| I9: F(1,c)=7 for c∈C | 3 cells | HAR |
| I9+I5: F(c,1)=7 for c∈C | 2 more cells | HAR |
| I8: F(3,9)=3 | 1 cell | 3 |
| I8+I5: F(9,3)=3 | 1 cell | 3 |
| **Total** | **24/81** | |

**Free cells (57/81):** values in C (if s,c ∈ C, by I3+I4) or unrestricted otherwise.

**HAR-maximization (I6) fills 49/57 free cells with 7.**

**Genuinely underdetermined: 8 cells** — the non-HAR free cells.

---

## Section 3: Integer-Role Decomposition

**What integer structure forces:**
- I2: The corner set C is the unit group (ℤ/10ℤ)* — purely arithmetic
- I1: HAR=7 is mid-spectrum; its position in {1..9} matters
- The 8 underdetermined values: 6/8 follow max(s,c); 2/8 remain unexplained

**What the integer order contributes:**
- max(s,c) = the BHML ordering endpoint — the deformation direction is built into the free cells
- Nearest-C-neighbor: integer distance |s - c_nearest| may explain F(1,2)=3, but the computation gives nearest C to G-state 2 as state 1, not state 3 — this doesn't hold cleanly

**What remains grammar-only (not arithmetic):**
- I8 (orbit zone {3,9}): the specific cycle is an algebraic choice, not purely integer-determined
- I9 (state-1 direct feeder): why state 1 specifically? The arithmetic of 1 as multiplicative identity may be relevant but isn't proved
- F(1,2)=3: not predicted by any tested integer function

---

## Section 4: Uniqueness / Family Result

**TSML is not unique. It is one member of a family characterized by:**

1. **24 forced cells** — identical across all family members
2. **49 HAR-maximized cells** — selected by I6 (maximization principle)
3. **8 underdetermined cells** — differ between family members

The family has 4 independent free parameters (pairs (1,2), (2,4), (2,9), (4,8) — others determined by I5). Upper bound on family size: ~9⁴ = 6,561 tables; actual size smaller due to I3/I4 restrictions.

**TSML's distinguishing property within the family:**
- 6/8 non-HAR cells follow max(s,c) — the ordering law
- This connects TSML to BHML: the non-HAR residual cells already point toward the order endpoint

**The 2 remaining exceptions:** F(1,2)=F(2,1)=3. No tested integer function predicts these. They may require an additional invariant (I11?) not yet identified.

---

## Section 5: Minimal Invariant Basis

To recover the structural features:

| Feature | Requires |
|---------|---------|
| HAR as absorbing | I1 alone (9 cells) |
| HAR + symmetry | I1+I5 (17 cells) |
| State-1 direct feeder | +I9 (22 cells) |
| Orbit zone {3,9} | +I8 (24 cells) |
| One-way gate | I4 (restricts, doesn't force values) |
| Sub-magma closure | I3 (constrains C-corner cells to C) |
| HAR maximization | I6 (fills 49 free cells) |
| 8 residual non-HAR | **Not determined by I1–I10** |

**Minimal basis for structural features:** {I1, I5, I8, I9} — 24 cells forced exactly.
**Add I6 for HAR maximization:** 73/81 cells determined.
**Remaining 8:** require either the max(s,c) ordering law or an undiscovered invariant.

---

## Section 6: What Remains Underdetermined

**Robustly underdetermined:**
- F(1,2) = F(2,1) = 3: no tested invariant forces this. The value 3 is the nearest corner to G-state 2 only if distance is measured differently (not |s-c| on the integer line).

**Possibly derivable with additional work:**
- Whether I13 (nearest-C-neighbor by a non-standard metric) correctly selects F(1,2)=3
- Whether the max(s,c) law for 6 cells follows from some canonical "order completion" argument connecting to BHML

**The honest answer to Q1–Q6:**

- **Q1:** No. I1+I2+I5+I4+I9 force 24 cells. First missing invariant: I6 (HAR maximization) for the bulk; I8 (orbit zone) for {3,9}; and an unnamed invariant for F(1,2).
- **Q2:** The orbit zone {3,9} is not forced by current invariants — it is one admissible choice. I8 asserts it directly.
- **Q3:** Recurrence-dependent cancellation is a consequence of I8 (the orbit zone creates the recurring path).
- **Q4:** The gap γ=3/4 follows from I2+I3+I8 (arithmetic hook + closure + orbit), not from completing the table first.
- **Q5:** 8 cells remain genuinely underdetermined; 2 of those have no integer explanation found.
- **Q6:** BHML as max(s,c) appears in the residual free cells — it is consistent with the same integer scaffold but requires a separate "order completion" argument.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
