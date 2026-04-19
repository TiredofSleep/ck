# Memory Atlas: The Tables
## The reference that stops getting forgotten

**Author:** Brayden Ross Sanders (7Site LLC)
**Compiled:** 2026-04-18
**Purpose:** TSML, BHML, CL, and the Doing table are the canonical 10×10 matrices that every TIG derivation leans on. They fall out of context constantly. This document is the disciplined reference that keeps them together with their structural invariants, composition rules, anchor cells, and known-cell verifiers — so any Claude, any collaborator, any future Brayden can reconstruct the framework in minutes rather than days.
**Canonical source:** `ck_tig.py` in `github.com/TiredofSleep/ck` (branch `tig-synthesis`). When this doc and the repo disagree, the repo wins. This doc is the memory scaffold, not the ground truth.
**TSML SHA-256:** `7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787`
**DOI:** 10.5281/zenodo.18852047

---

## Quick orientation

Four named 10×10 integer matrices structure the framework:

| Table | Role | Determinant | HARMONY cells | Associative subalgebra |
|---|---|---|---|---|
| **TSML** | Being / measurement / singular / "synthesis" | **0** (rank 9, nullity 1) | **73 / 100** | A = {HARMONY} = {7} |
| **BHML** | Becoming / transformation / invertible | **70** | **28 / 100** | {VOID} = {0} |
| **CL** | Composition / binding kernel / frozen commutative non-assoc magma | — | 73% cells absorb to HARMONY (gravity) | HARMONY absorbs |
| **Doing** | |TSML − BHML| — "where physics actually happens" | dominant eigenvalue ≈ 24 (cube rotation group) | 71% disagree rate ≈ T* |

**Lens mapping:**
- **Einstein = BHML lens** (invertible, deterministic, classical)
- **Bohr = TSML lens** (singular, measurement-collapses, quantum)
- **Doing table = where physics actually happens** (the difference-register)

**Uniqueness:** P < 2.15 × 10⁻²⁷ (CK_HANDOFF_2026_02_18). Monte Carlo 0/100,000 random tables match structural constraints.

---

## §1. The 10 operators

Every row and column is indexed by the ten TIG operators:

| Index | Name | Fruit of Spirit | CREATION cycle | DISSOLUTION cycle |
|---|---|---|---|---|
| 0 | **VOID** | Love | — | — |
| 1 | **LATTICE** | Joy | ✓ (1) | — |
| 2 | **COUNTER** | Peace | — | ✓ (2) |
| 3 | **PROGRESS** | Patience | ✓ (3) | — |
| 4 | **COLLAPSE** (earlier: TENSION) | Kindness | — | ✓ (4) |
| 5 | **BALANCE / BALANCE** | Goodness | — | — |
| 6 | **CHAOS** | Faithfulness | — | ✓ (6) |
| 7 | **HARMONY** | Gentleness | ✓ (7) | — |
| 8 | **BREATH** | Self-Control | — | ✓ (8) |
| 9 | **RESET** | Reset → Love | ✓ (9) | — |

- **CREATION cycle:** [1, 3, 9, 7] — the odd multiplicative orbit mod 10 under g = 3
- **DISSOLUTION cycle:** [2, 4, 8, 6] — the even multiplicative orbit mod 10 under g = 2
- **VOID (0)** and **BALANCE (5)** are the two fixed points not in either cycle
- COLLAPSE = 4 = (+1, −1) oscillation; CHAOS = 6 = (−1, +1) reversed
- Naming note: TENSION and COLLAPSE both appear in the history; D-tier canonical is **COLLAPSE** (per WP19_NS_BREATH where "BREATH persists only in COLLAPSE context")

---

## §2. TSML — the synthesis table (D-tier version)

### Structural invariants [fire, all PROVED]

| Property | Value | Source |
|---|---|---|
| Dimensions | 10 × 10 | — |
| Entries | integers in {0, ..., 9} | — |
| Determinant | **0** | D-tier |
| Rank | **9** | D-tier |
| Nullity | **1** | D-tier (on full 10×10) |
| HARMONY cells (value = 7) | **73 / 100** | D10 |
| Iterated harmony basin | **79%** (73 direct + 6 shallow-escape after one iteration) | 2026 refinement |
| Associative subalgebra | **A = {7}** (HARMONY only) | D-tier |
| 8×8 cycle-element core | rank 7, nullity 1, Sylvester signature (4, 3, 1) | Sprint 9 7-zero decomposition |
| Unique null direction | **v_null = (BALANCE − CHAOS) / √2** | Sprint 9 |
| 8×8 harmony density | **82.8% HARMONY** → 1.77 effective dims | WP17 stage |
| SHA-256 | `7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787` | committed |

### Anchor cells (named, do not forget)

| Cell | Value | Significance |
|---|---|---|
| **TSML[0][j] = j** for all j ≠ 7 | identity on row 0 | D-tier correction (earlier versions had row 0 all zeros) |
| **TSML[0][7] = 7** | = HARMONY | Row 0's one non-identity-flavored cell lands on HARMONY |
| **TSML[7][7] = 8 = BREATH** | **NEVER rewritten — Layer 0 of CK organism** | HARMONY composed with itself yields BREATH, not HARMONY |
| **TSML[BREATH][COLLAPSE] = TSML[8][4] = 8 = BREATH** | foundation of WP19_NS_BREATH | "BREATH persists only in COLLAPSE context" |

### The 7-zero decomposition (Sprint 9) [PROVED]

On the 8×8 cycle-element core:

- **6 frozen zeros:** {LATTICE, COUNTER, PROGRESS, COLLAPSE, BREATH, RESET}
- **1 ether zero:** null direction (BALANCE − CHAOS) at α = 5 boundary (observer blind spot)
- **Sum of 7 zeros:** the full nullity-1 kernel of the 10×10 D-tier TSML

### TSML as a table (D-tier, schema)

The full 10×10 D-tier TSML is 100 integer cells. The canonical committed form is in `ck_tig.py` under the SHA above. Reconstruction rules for the D-tier:

1. **Row 0 (VOID row):** TSML[0][j] = j for all j
2. **HARMONY column behavior:** column 7 largely absorbs to HARMONY (column 7 cells tend toward 7)
3. **HARMONY × HARMONY = BREATH:** the single boundary-breaking cell (7, 7) → 8
4. **Harmony dominance:** 73 of the 100 cells contain 7 (HARMONY)
5. **Null direction:** any row/column linear combination along (BALANCE − CHAOS) lies in the kernel
6. **Associative closure:** only {7} closes under TSML; every other subset eventually leaks

```
Schematic structure (not cell-exact; consult ck_tig.py for verified cells):

    VOI LAT CTR PRG COL BAL CHA HAR BRT RST
    [0]  1   2   3   4   5   6   7   8   9     ← row 0 (identity)
LAT  ·   ·   ·   ·   ·   ·   ·   7   ·   ·     ← HARMONY-dominant
CTR  ·   ·   ·   ·   ·   ·   ·   7   ·   ·
PRG  ·   ·   ·   ·   ·   ·   ·   7   ·   ·
COL  ·   ·   ·   ·   ·   ·   ·   7   ·   ·
BAL  ·   ·   ·   ·   ·   ·   ·   7   ·   ·     ← BALANCE/BALANCE row: part of null direction
CHA  ·   ·   ·   ·   ·   ·   ·   7   ·   ·     ← CHAOS row: completes null direction
HAR  ·   ·   ·   ·   ·   ·   ·  [8]  ·   ·     ← (7,7) = 8 = BREATH, NEVER rewritten
BRT  ·   ·   ·   ·  [8]  ·   ·   7   ·   ·     ← (8,4) = 8 = BREATH, NS_BREATH foundation
RST  ·   ·   ·   ·   ·   ·   ·   7   ·   ·

(dots = HARMONY-or-nearby per D10; 73 of these cells = 7)
```

**If you need the exact cell values:** `load_tsml()` in `ck_tig.py`. Verify SHA on load.

---

## §3. BHML — the becoming table

### Structural invariants [fire, all PROVED]

| Property | Value | Source |
|---|---|---|
| Dimensions | 10 × 10 | — |
| Determinant | **70** | WP17 |
| Invertible | YES | det ≠ 0 |
| HARMONY cells (value = 7) | **28 / 100** | D10 |
| Associative subalgebra | **{VOID} = {0}** | D-tier |
| Non-associative triples | **49.8%** | WP16 Lemma A, PROVED |
| λ₆ / λ₅ (eigenvalue ratio) | ≈ **0.714865** (T* to 0.08%) | WP15 Stage 2 |
| 8×8 harmony density | **12.5% HARMONY** → 5.73 effective dims | WP17 stage |
| IPR (Inverse Participation Ratio) | ≈ T* | WP17 |
| Spectral gap (vs TSML) | **54.93** | computed |
| Doing disagree rate | **71%** ≈ T* | Doing = \|TSML − BHML\| |

### Anchor cells and composition rules

| Property | Value |
|---|---|
| **LATTICE(1) is universal generator of BHML** | every pair (1, x) under BHML reaches close to full algebra |
| **9/9 pairs with LATTICE close** (closure test) | | 
| **0/36 pairs without LATTICE close** | LATTICE is the unique universal starter |
| **{1, 4, 9} → full algebra in 2 steps** | LATTICE ∪ COLLAPSE ∪ RESET generates everything quickly |
| **{0, 8, 9} stalls at {0, 7, 8, 9}** | VOID + BREATH + RESET cannot escape without LATTICE |
| **fuse(9, 9, 9) = 7 = HARMONY** | three RESETs compose to HARMONY |
| **fuse([3, 4, 7]) = 8 = BREATH** | PROGRESS + COLLAPSE + HARMONY → BREATH (doomdo form) |

### BHML as a table (schema)

```
Schematic structure (not cell-exact; consult ck_tig.py):

- det = 70 = 2 × 5 × 7 = 2 · p · q where q = HARMONY
- Much more algebraic variation than TSML (only 28% HARMONY)
- Non-associative in 49.8% of triples
- LATTICE (row 1 / column 1) has maximal closure degree
- {VOID} is the associative core

Generator triples that produce full algebra: {0,1,2}, {0,7,1}, {1,2,3}
  → numeric encoding: 012, 071, 123 (the three canonical CL generators)
```

### Four-rule derivation (Q7) [fire]

BHML's full 100 cells derive from **4 structural rules + symmetry**:

1. VOID is annihilating / identity-like depending on side
2. LATTICE generates multiplicatively against all non-VOID operators
3. Primary operators (1, 3, 7, 9 — CREATION cycle) behave multiplicatively
4. Secondary operators (2, 4, 6, 8 — DISSOLUTION cycle) behave additively with CREATION-cycle partners

Plus the commutativity-style symmetry constraint. From this, all 100 cells are determined.

---

## §4. CL — the composition / binding kernel

### Structural invariants [fire]

| Property | Value |
|---|---|
| Algebraic type | **Frozen commutative non-associative magma** — NOT a monoid |
| HARMONY gravity | **73% of compositions collapse to HARMONY** (universal absorbing element) |
| Bump cells | **11 cells** concentrate information (deviate from absorption) |
| Non-associativity (TSML view) | 12.8% |
| Non-associativity (BHML view) | 49.8% |
| Non-associativity (Doing view) | 56.8% |
| Uniqueness | Monte Carlo 0 / 100,000 random tables match; Z = 21.3; p < 10⁻⁵⁰ |
| Spectral gap | 54.93 |
| Eigenvalues | produce **e, 1/e, π, φ, ζ(3), Catalan's G** all within 1% |

### The 11 bumps

The 11 cells where CL deviates from the HARMONY-absorption rule. These are the **information-carrying** cells.

- **4 Hopf links** (paired bumps)
- **1 trefoil** — the BREATH bump (requires community; three crossings)
- **6 additional bumps** completing the 11 structural bumps

**Structural claim:** the 11 bumps encode all the non-trivial composition information in CL. Everything else collapses to HARMONY.

### Operator equation

```
O(x) = a·x² + b·x + c
Δ = b² − 4a·c   (the binding kernel / discriminant)
```

- **a, b, c ∈ {0, 1, ..., 9}** (ten operators as coefficients)
- **Δ** is the "binding kernel" — controls 7 dynamical bands: {VOID, SPARK, FLOW, MOLECULAR, CELLULAR, ORGANIC, CRYSTAL}
- Implemented in 400-line zero-dep `coherence_router.py` (All-or-Nothing-E repo)

### CL generators (three canonical)

- **012** — VOID + LATTICE + COUNTER
- **071** — VOID + HARMONY + LATTICE  
- **123** — LATTICE + COUNTER + PROGRESS

From any of these three, CL generates the full 10-element algebra.

### CL IS the torus, not mapped onto it

The 11 bumps + composition structure realize the torus:

- 7-hole interior = harmony (HARMONY-absorbing bulk)
- 0-hole exterior = void (VOID boundary)
- Surface = life (the 11 bumps)
- **r > R** (self-intersecting torus — the knot geometry)
- **22 / 44 / 72 shells = nested tori:** 22 skeleton/frozen, 44 Becoming/alive, 72 Being/blur

---

## §5. The Doing table

**Definition:** Doing = |TSML − BHML| (cellwise absolute difference)

### Structural invariants

| Property | Value |
|---|---|
| Disagree rate (TSML vs BHML) | **71%** ≈ T* = 5/7 ≈ 71.4% |
| Dominant eigenvalue | **≈ 24** (cube rotation group \|O_h\| = 48 halved by chirality) |
| Non-associativity | **56.8%** |
| Role | **Where physics actually happens** — the Doing layer where information is generated |

### Why the Doing table matters

- **Additive partitions → LATTICE layer** (TSML)
- **Multiplicative orbits → PROGRESS layer** (BHML)
- **Their crossing → COUNTER layer** (this table) — the Crossing Lemma layer

**Score 0 on the Doing table** means refinement-only (not useless — Productive Incompleteness addendum WP61).

**Einstein lens = BHML** (determinism, invertibility)
**Bohr lens = TSML** (singularity, measurement collapse)
**Doing table = where the two lenses disagree** — which is where observable physics lives

---

## §6. Composition rules (the operational summary)

### Rules shared across tables

| Rule | TSML | BHML | CL |
|---|---|---|---|
| Commutative | partial | partial | **yes (frozen commutative)** |
| Associative | **only on {7}** | **only on {0}** | **non-associative** |
| Identity element | no full identity (row 0 behavior only) | no full identity | no full identity |
| Dominant absorber | HARMONY (73% gravity) | fewer HARMONY attractors | HARMONY (73% of compositions) |

### The generator tests that matter

Run these to verify any table claiming to be the canonical TIG table:

1. **TSML[7][7] = ?** must be **8** (BREATH). Layer 0 rule.
2. **TSML[8][4] = ?** must be **8** (BREATH). NS_BREATH foundation.
3. **TSML cell count of 7s:** must be **73**.
4. **BHML det:** must be **70**.
5. **BHML[1][·] closure:** LATTICE must universally generate (9/9 pairs close).
6. **Doing disagree rate:** must be ≈ **71%** (T* in cellwise form).
7. **CL eigenvalues:** must produce e, 1/e, π, φ within 1%.
8. **Monte Carlo uniqueness:** 0 / 100,000 random symmetric integer 10×10 matrices satisfy all the above.

If any test fails, the loaded table is NOT the canonical TIG table. Reload from `ck_tig.py` against SHA `7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787`.

---

## §7. Spectral structure

### TSML spectrum

- Rank 9, nullity 1
- Null direction: **v_null = (BALANCE − CHAOS) / √2**
- 8×8 cycle-element core: Sylvester signature (4, 3, 1) — 4 positive, 3 negative, 1 zero

### BHML spectrum [fire]

- det = 70
- Invertible
- **λ₆ / λ₅ ≈ 0.714865 = T* to 0.08%** (WP15 Stage 2)
- Eigenvalue ratios recover T* asymptotically

### CL spectrum

Produces these constants within 1% (WP18 cross-verified):

| Constant | Value | Matches |
|---|---|---|
| e | 2.718... | ✓ |
| 1/e | 0.367... | ✓ (also ξ₀ value) |
| π | 3.141... | ✓ |
| φ (golden ratio) | 1.618... | ✓ |
| ζ(3) (Apéry) | 1.202... | ✓ |
| Catalan's G | 0.915... | ✓ |

**Implication:** the CL spectrum is dense in transcendental structure. Not random.

### Doing table spectrum

- Dominant eigenvalue ≈ 24 (half of full cube rotation order 48)
- Interpretation: Doing encodes the chiral projection of cube symmetry

---

## §8. Harmony-basin iteration dynamics

**First-order (D10):** TSML has 73 HARMONY cells. Iterate TSML on any operator and 73% immediately hit HARMONY.

**Second-order refinement:** 6 additional "shallow-escape" cells reach HARMONY after one more TSML application. Iterated stable basin: **79% HARMONY.**

**Fixed residual (21%):** cells that land on non-HARMONY stable points. Structure:
- Fixed boundary: VOID (0) fixed (0-absorbing)
- Bifurcation marker: HARMONY (7) is projection-induced attractor in TSML, not true σ-fixed point (Q3 caution)
- Other residuals: RESET cycle, BREATH boundary

**Status:** refines D10 (73%), not contradicts. Resolves the "6 zeroes thread" from the pre-March handoff — the six extra basin cells are the shallow escape.

---

## §9. Cycle structure under σ (the Q10 operator)

From the σ polynomial on F₂ × F₅ (§5 of master atlas, Q10 boxed):

- **σ cycle structure:** (0)(3)(8)(9)(1 7 6 5 4 2)
  - **Fixed:** VOID, PROGRESS, BREATH, RESET
  - **6-cycle:** LATTICE → HARMONY → CHAOS → BALANCE → COLLAPSE → COUNTER → LATTICE

- **TIG = σ⁻¹ cycle structure:** (0)(3)(8)(9)(1 2 4 5 6 7)
  - **Fixed:** same four
  - **6-cycle reversed:** LATTICE → COUNTER → COLLAPSE → BALANCE → CHAOS → HARMONY → LATTICE

- **σ⁶ = id** on all 10 states [PROVED from polynomial, G6 Luther]

**Key fact:** σ and TIG fix the same four operators: {VOID, PROGRESS, BREATH, RESET}. This is the **Fix(σ) ∩ Fix(TIG) = {0, 3, 8, 9}** anchor set. The 6-cycle elements are {1, 2, 4, 5, 6, 7}.

**Pure-C fraction (Q11):** C ∩ Fix(σ) = {3, 9} = **2/9 ≈ 22%** — the algebraic peak of gate_score before search dynamics.

---

## §10. Related derived tables

### The 22 / 44 / 72 nested-tori shells

| Shell | Size | Role |
|---|---|---|
| 22 | skeleton | frozen structure |
| 44 | PROGRESS | alive (cellwise dynamics) |
| 72 | LATTICE | blur (smoothed / measurement) |

These are **derived from TSML + BHML**, not standalone tables. They describe the composition hierarchy at three zoom levels.

**Note:** PROGRESS = 44 = matches the "44% of file = harmony's exact lattice proportion" observation from CK architecture.

### The 7 dynamical bands (CL classifier)

From `coherence_router.py`:

1. **VOID** — null / silent
2. **SPARK** — onset
3. **FLOW** — continuous
4. **MOLECULAR** — bound pairs
5. **CELLULAR** — bound cells with membrane
6. **ORGANIC** — bound cells with exchange
7. **CRYSTAL** — bound lattice, symmetry-locked

**Mapping to Δ = b² − 4ac:** each band corresponds to a range of Δ values in CL's binding kernel.

---

## §11. The "constants fallout" that makes the tables unique

When the canonical tables are loaded, these constants emerge as byproducts (each derivable three or more independent ways):

| Constant | Emergence |
|---|---|
| **T* = 5/7** | TSML/BHML eigenvalue ratio λ₆/λ₅; D4/D18c/D18d generator selection; Z.2 spectral gap; Li Foundation K*(6)=99; Sandwich Theorem (5/6)² < 5/7 < (6/7)² |
| **S* = 0.991...** | Paper I fixed point of S(σ) = σ(1−σ)VA |
| **4/π² = sinc²(1/2)** | Montgomery pair-correlation at u=1/2; TIG mid-journey amplitude; 890 D6 tests |
| **2/7 = T* + S* − 1 = 1 − T*** | Structural only. **[caution: quantitative match to lattice-QCD √σ/m(0++) falsified at 16.5σ per EXPERT_SUMMARY]** |
| **3/14 = T* − 1/2** | Universal crossing cost; bridge width between analytic (1/2) and algebraic (5/7) thresholds |
| **W = 3/50** | Wobble quantum from 44-cell PROGRESS table; COL(4) at ±W from midplane |
| **det(BHML) = 70 = 2 · 5 · 7** | Every prime factor is a named operator: DISSOLUTION (2) · BALANCE (5) · HARMONY (7) |

---

## §12. Quick reference — the anchor cells Brayden should memorize

Cold-load priority. If everything else is lost, these 8 cells + 4 invariants reconstruct the framework:

**Cells:**

1. TSML[7][7] = 8 (HARMONY² → BREATH — Layer 0)
2. TSML[8][4] = 8 (BREATH in COLLAPSE context — NS_BREATH)
3. TSML[0][j] = j for all j (VOID row is identity)
4. BHML[1][·] universal generator (LATTICE starts everything)
5. fuse(9, 9, 9) = 7 (triple RESET → HARMONY)
6. fuse([3, 4, 7]) = 8 (doomdo → BREATH)
7. σ cycle (1 7 6 5 4 2) and fixed {0, 3, 8, 9}
8. CL: 012, 071, 123 as canonical generators

**Invariants:**

1. **TSML: det = 0, 73 HARMONY cells, A = {7}**
2. **BHML: det = 70, 28 HARMONY cells, A = {0}**
3. **Doing disagree rate = 71% ≈ T***
4. **CL: 11 bumps, 0 / 100,000 MC match, eigenvalues recover e/π/φ within 1%**

**Canonical source:** `ck_tig.py`, SHA `7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787`. When in doubt, reload.

---

## §13. How to cite this document

When any derivation in the atlas references "TSML" or "BHML" or "CL" or "the Doing table," it points here. This document points at `ck_tig.py` as the ground truth.

**Citation form:**

> Sanders, B. R. (2026). *Memory Atlas: The Tables.* 7Site LLC. DOI: 10.5281/zenodo.18852047. Canonical source: github.com/TiredofSleep/ck, `ck_tig.py`, SHA-256 `7726d8a620c24b1e461ff03742f7cd4f775baed772f8357db913757cf4945787`.

---

## §14. What this document does NOT contain

- **Cell-exact 10×10 values** for TSML, BHML, CL — those live in `ck_tig.py` with SHA verification. This document provides anchor cells and structural constraints sufficient to verify a loaded table is canonical.
- **Proof of uniqueness** — that lives in WP papers and Monte Carlo logs.
- **Historical versions** — the pre-D-tier TSML (row 0 = all zeros) is not here; see archive-full branch.
- **The Crossing Lemma itself** — that's an operator-level theorem on partitions, not a table entry. See §4.6 of master atlas v3.5.

---

## §15. Version notes

**v1 (2026-04-18):** Initial compilation in response to ChatGPT meta-review feedback on atlas v3.5. ChatGPT noted the TSML/BHML tables "fall out of context constantly" and this document closes that gap. Anchor cells, structural invariants, composition rules, spectral structure, and the reload protocol against `ck_tig.py` with SHA verification are all preserved here so no context reset can lose them again.

**Pending additions:** Cell-exact matrices when `ck_tig.py` is tagged v1.0-frozen; formal proof of 4-rule derivation (Q7) in BHML; CL's 11-bump enumeration with explicit cell coordinates.

---

*© 2026 Brayden Ross Sanders / 7Site LLC. 7Site Human Use License v1.0. DOI: 10.5281/zenodo.18852047.*

**End of memory atlas tables reference.**
