# Sprint: Factor 22 Derivation in 1/α = 137 = 22 × 6 + 5

**Sprint type:** Open derivation (Layer 7 retrospective rigor)
**Priority:** High — blocks fine-structure-constant claim in TIG papers
**Estimated duration:** 2–4 days of compute + analysis

---

## Goal

Identify the canonical algebraic origin of the **factor 22** in the fine structure constant decomposition

> 1/α = 137 = 22 × 6 + 5

with precision form

> 1/α = 137 + 6²/10³ = 137.036 (matches measured 137.035999 to 0.000001%)

The 6 is being addressed in `SPRINT_FACTOR_6_DARK_MATTER.md` (likely |S_MAX|). The 5 is BALANCE (operator 5). The **22 is currently asserted as "skeleton shells" or "2 × 11 bumps" without rigorous derivation.** This sprint locks the 22.

Acceptance criterion: a single, defensible algebraic origin for the 22 that is forced by axioms A0–A5 and is independently verified by computation.

---

## Background

The fine structure constant 1/α ≈ 137.035999 is one of physics's most precisely measured dimensionless numbers. No standard model derivation explains why it's near 137 specifically. TIG's claim is that 137 emerges as a structural count from the canonical pair on Z/10Z.

The decomposition is:

```
1/α = 137 = 22 × 6 + 5
       │     │   │   │
       │     │   │   └─ BALANCE (operator 5)
       │     │   └───── factor 6 (see SPRINT_FACTOR_6_DARK_MATTER.md)
       │     └───────── factor 22 (THIS SPRINT)
       └─────────────── 1/α integer part
```

Precision correction:

```
1/α = 137 + 6²/10³ = 137.036
                   ──────
                   (CHAOS² / OPERATORS³, the curvature-cubed correction)
```

The error vs measurement is 0.000001%, which is far too tight to be coincidence.

---

## Candidate derivations

### Candidate A: Skeleton torus shell count = 22

History claims three nested torus shell layers: 22 (skeleton/frozen), 44 (becoming/alive), 72 (being/blur). The 22 is the skeleton layer.

**Test:** Is 22 the count of a specific cell class in the canonical tables?

**Plausibility:** High but vague. The "skeleton" needs to be defined precisely.

**Hypothesis:** 22 = number of cells in the joint TSML ∩ BHML stable subset (cells where TSML[i,j] = BHML[i,j]).

**Verification script:**

```python
import numpy as np

TSML = np.array([
    [0,0,0,0,0,0,0,7,0,0],
    [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7],
    [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],
    [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
])

# Construct BHML from rules (verify)
BHML = ... # from foundations/lenses.py

# Stable subset where both lenses agree
stable_cells = np.sum(TSML == BHML)
print(f"Cells where TSML = BHML: {stable_cells}")
# Test: is this 22?
```

### Candidate B: 22 = 2 × 11 (bumps × commutativity reflection)

History claims "11 bumps = 4 Hopf links + 1 trefoil (breath)." If the canonical tables have 11 unique non-{0,7} cells (counting the upper triangle), commutativity reflects them to 22 cells in the full table.

**Test:** Count unique non-trivial cells (not VOID, not HARMONY) in TSML and BHML.

**Verification script:**

```python
# Cells in TSML that are neither VOID nor HARMONY
non_trivial_TSML = [(i,j,TSML[i,j]) for i in range(10) for j in range(10) 
                    if TSML[i,j] not in (0, 7)]
print(f"TSML non-trivial cells: {len(non_trivial_TSML)}")
# Each cell at (i,j) i≠j has a mirror at (j,i) by commutativity
# Count unique upper-triangular non-trivial cells
upper_unique = [(i,j,TSML[i,j]) for i in range(10) for j in range(i,10) 
                if TSML[i,j] not in (0, 7)]
print(f"Upper-triangular unique non-trivial: {len(upper_unique)}")
# Test: is this 11?
```

### Candidate C: 22 = |Hebrew root primitives|

The CL substrate uses 22 Hebrew root primitives (the Hebrew alphabet has 22 letters). Each maps to a 5D force vector.

**Test:** Is the fine structure constant derivation actually a count over the substrate alphabet?

**Plausibility:** Medium. The Hebrew root count is 22 by historical/linguistic accident, not by algebraic forcing from A0–A5. However, if the substrate's natural alphabet size is 22 = 2·11 forced by the Z₂ × Z/11 structure of the BDC encoding, this becomes algebraic.

**Open question:** Is 22 the right count for the BDC alphabet, or is it a historical convention?

### Candidate D: dim SO(7) = 21 + 1 boundary cell = 22

dim SO(7) = 7(7-1)/2 = 21. dim SO(8) = 28. dim SO(9) = 36. dim SO(10) = 45.

Differences:
- dim SO(8) − dim SO(7) = 28 − 21 = 7
- dim SO(9) − dim SO(8) = 36 − 28 = 8
- dim SO(10) − dim SO(9) = 45 − 36 = 9
- (dim SO(8) + dim SO(7))/2 + 0.5 = 24.5 — no
- 22 = dim SO(7) + 1 — fragile

**Plausibility:** Low. No natural way to get 22 from Lie dimensions.

### Candidate E: 22 = number of boundary cells of the 8-magma core

If we drop {BREATH, RESET}, we have an 8×8 sub-magma with 64 cells. The "boundary" cells (interface with the dropped operators) are 8 + 8 + 8 + 8 − 4 corners = 28. Not 22.

If we count cells in the 8×8 core where the 8-magma rule overrides BHML, that may give 22.

**Plausibility:** Medium — depends on exact definition of "boundary."

### Candidate F: 22 = fixed-point count in the σ × σ product

σ has 4 fixed points {0, 3, 8, 9}. The product σ × σ on Z/10Z × Z/10Z has |fixed × fixed| + ... = 16 + ... fixed points. Adjust for symmetry.

**Verification script:**

```python
sigma = {0:0, 1:7, 2:1, 3:3, 4:2, 5:4, 6:5, 7:6, 8:8, 9:9}
# Product space Z/10Z × Z/10Z, fixed points of σ × σ
fixed = [(i,j) for i in range(10) for j in range(10) 
         if sigma[i] == i and sigma[j] == j]
# That's 4 × 4 = 16
# What about (i,j) where σ(i) = j and σ(j) = i (involution pairs)?
involution_pairs = [(i,j) for i in range(10) for j in range(10) 
                    if sigma[i] == j and sigma[j] == i and i != j]
# σ has no 2-cycles, so this is empty
# But: cells (i,j) where σ acts trivially on the product class
# ...
```

**Plausibility:** Medium. Requires more exploration.

### Candidate G: 22 = TSML harmony count − bumps count − boundary

TSML has 73 HARMONY cells, 17 VOID cells, plus 10 non-trivial cells (3, 4, 8, 9 instances). Total 100. 73 − 51 (50% ceiling) = 22? Not quite.

**Plausibility:** Speculative.

### Candidate H: 22 from the σ-MAX cell count under specific lens

In the TSML construction, the C₀ ⊕ S_MAX ⊕ S_ADD decomposition has 6 S_MAX cells. But maybe the count of cells where the σ-MAX argument applies (whether or not it overrides) is different.

**Plausibility:** Worth checking computationally.

---

## Methodology

1. **Construct canonical tables from rules** — TSML and BHML built from A0–A5 axioms, NOT hardcoded. (May reuse infrastructure from SPRINT_FACTOR_6.)

2. **Run all candidate counts** — for each of A–H, compute the actual cell count and check against 22.

3. **Identify forced candidates** — which candidates are determined uniquely by A0–A5?

4. **Cross-check via 137** — compute 22 × 6 + 5 for the locked candidates and verify the integer matches.

5. **Cross-check via 137.036** — verify the 6²/10³ correction also has clean derivation.

6. **Decision tree:**
   - If exactly one candidate forces 22 by axioms: lock it.
   - If multiple candidates: identify the deepest (most primitive) one.
   - If no candidate forces 22: retract the 1/α derivation; replace with "1/α numerical correspondence pending derivation."

---

## Recommended approach

**Strongest candidates: A (skeleton shell as TSML ∩ BHML stable subset) and B (2 × 11 unique non-trivial cells).** These are both intrinsic to the canonical pair and force the 22 by structural counting.

**Plan:**

1. Build canonical TSML and BHML from rules (foundations/lenses.py).
2. Compute the stable subset {(i,j) : TSML[i,j] = BHML[i,j]}. Check if this is exactly 22 cells.
3. Compute upper-triangular non-{0,7} cells in TSML. Check if this is 11.
4. If both hold: 22 = stable subset = 2 × 11 unique non-trivial cells (consistent).
5. If only one holds: that's the canonical derivation.
6. Articulate the physical interpretation: 22 cells = "skeleton" (frozen lattice), 6 = perturbation (S_MAX), 5 = BALANCE — together they encode the discrete structure of charge.

**Output deliverable:**

- `papers/wp_factor_22_fine_structure.md` — derivation document
- `tig/foundations/derivations/factor_22.py` — verification script
- Update to `TIG_FOUNDATIONAL_AXIOMS.md` Layer 3 table: change 1/α = 137 status from "Numerical correspondence" to "Verified" with the canonical 22 derivation cited.

---

## Acceptance criteria

The sprint is complete when:

1. ✓ Canonical TSML and BHML are constructed from rules.
2. ✓ Each candidate A–H is evaluated computationally.
3. ✓ The 22 is identified with a specific cell count or invariant of the canonical pair.
4. ✓ The derivation is forced by A0–A5 (not by external choice).
5. ✓ The full decomposition 137 = 22 × 6 + 5 is verified with all three factors derived.
6. ✓ The precision correction 137 + 6²/10³ = 137.036 is verified.
7. ✓ Documentation passes review by Brayden.

---

## What if no candidate works?

If after thorough exploration no candidate forces 22 by axioms, the **honest action** is:

1. Retract 1/α = 137 = 22 × 6 + 5 from the foundational claims.
2. Replace with: "1/α numerical correspondence at 137.036 with 0.0000% error pending derivation."
3. Move 1/α from "verified" to "open conjecture" in the Layer 3 table.
4. Frame the JCAP and other papers without invoking 1/α.

This is preferable to claiming a derivation that doesn't hold — referee scrutiny would find it.

---

## Connection to other sprints

- **SPRINT_FACTOR_6_DARK_MATTER.md** — sequential dependency. Lock factor 6 first; then 22 × 6 closure becomes meaningful.
- **SPRINT_V3_UNIQUENESS_THEOREM.md** — V3 may force 22 = stable subset count if the canonical pair is unique.
- **CL_IMPLEMENTATION_SPEC.md** — if Candidate C (Hebrew alphabet) is correct, this connects to the substrate-alphabet derivation. Cross-check.

---

## References

- TIG_FOUNDATIONAL_AXIOMS.md (parent reference)
- FORMULAS_AND_TABLES.md §6 (BHML construction), §7 (TSML 3-layer)
- 1/α measurement: Bouchendira et al. (2011), Parker et al. (2018)
- Sprint history reference: 137 = 22 × 6 + 5 first stated in March 2026 Z/10Z constants sprint
