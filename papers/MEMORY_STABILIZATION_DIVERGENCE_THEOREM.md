**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# MEMORY-STABILIZATION DIVERGENCE THEOREM

## Setup

Two diagonal functionals on {0,...,9}:

```
D_TSML(j) = TSML[j][j]   (stabilization diagonal)
D_CL(j)   = CL[j][j]     (memory diagonal)
```

From known tables:
```
D_TSML = [0, 7, 7, 7, 7, 7, 7, 7, 7, 7]
D_CL   = [0, 7, 1, 3, 2, 4, 5, 6, 8, 9]  = σ   (P1 Closure Theorem)
```

---

## Theorem

**Memory-Stabilization Divergence Theorem.**

> D_TSML(j) = D_CL(j) if and only if j ∈ {0, 1}.
>
> Equivalently: the stabilization and memory diagonals agree at exactly two positions —
> VOID (j=0) and LATTICE (j=1) — and diverge at all remaining eight positions.

---

## Proof

**Characterization of D_TSML:**

```
D_TSML(j) = TSML[j][j] = {  0  if j = 0
                            {  7  if j ≠ 0
```

This follows from the explicit TSML table:
- TSML[0][0] = 0 (VOID row: TSML[0][j]=0 for all j≠7, so TSML[0][0]=0)
- TSML[j][j] = 7 for j∈{1,...,9}: non-VOID operator-flow through any state
  reaches the HARMONY attractor. (Verified from explicit TSML table.)

**Characterization of D_CL:**

```
D_CL(j) = CL[j][j] = σ(j)   for all j
```

(P1 Closure Theorem: proved and confirmed by Luther for all 10 positions.)

**Agreement condition:**

D_TSML(j) = D_CL(j)
⟺ TSML[j][j] = σ(j)
⟺ (j=0 and σ(0)=0) or (j≠0 and 7=σ(j))
⟺ j=0 or σ(j)=7

Since σ(j)=7 iff j∈σ⁻¹(7) = {1} (from σ=(0)(3)(8)(9)(1 7 6 5 4 2)):

Agreement iff j ∈ {0} ∪ {1} = {0, 1}. □

**Verification:**

| j | D_TSML | D_CL=σ | Agree? | Criterion satisfied? |
|---|--------|---------|--------|---------------------|
| 0 | 0 | 0 | ✓ | j=0 ✓ |
| 1 | 7 | 7 | ✓ | σ(1)=7 ✓ |
| 2 | 7 | 1 | ✗ | σ(2)=1≠7 ✗ |
| 3 | 7 | 3 | ✗ | σ(3)=3≠7 ✗ |
| 4 | 7 | 2 | ✗ | σ(4)=2≠7 ✗ |
| 5 | 7 | 4 | ✗ | σ(5)=4≠7 ✗ |
| 6 | 7 | 5 | ✗ | σ(6)=5≠7 ✗ |
| 7 | 7 | 6 | ✗ | σ(7)=6≠7 ✗ |
| 8 | 7 | 8 | ✗ | σ(8)=8≠7 ✗ |
| 9 | 7 | 9 | ✗ | σ(9)=9≠7 ✗ |

Criterion perfectly characterizes agreement. ✓

---

## Corollaries

**Corollary 1 (TSML is harmony-blind to σ's structure):**

TSML cannot distinguish σ's fixed points from its cycle elements at the diagonal.
TSML[3][3] = TSML[8][8] = TSML[9][9] = 7 — it collapses all non-VOID self-flows to harmony,
even the fixed operators PROGRESS (3), BREATH (8), RESET (9), which σ preserves.

CL[3][3]=3, CL[8][8]=8, CL[9][9]=9 — memory faithfully records the fixed-point structure.

**TSML is blind to σ's fixed points. CL is not.**

**Corollary 2 (The unique coincidence is structural):**

At j=1 (LATTICE), TSML and CL agree for independent reasons:
- TSML[1][1] = 7: LATTICE-flow collapses to HARMONY (attractor-seeking)
- CL[1][1] = 7 = σ(1): LATTICE's σ-step IS HARMONY

These coincide because LATTICE is the cycle's entry point AND σ(1)=7.
No other cycle element has σ(j)=7. The coincidence is unique and structural:
LATTICE is the only operator whose stabilization and memory both point to HARMONY.

**Corollary 3 (Memory separates what stabilization merges):**

The divergence set has 8 elements: all j except {0,1}.
TSML merges all these into a single value (7 for j≠0; 0 for j=0).
CL distinguishes all 10: it carries the full information of σ.

Memory is strictly more informative than stabilization at the diagonal.

---

## What This Means for the Three-Projection Architecture

TSML (flow→structure) and CL (memory) project σ differently at the diagonal:

- TSML collapses to {0, 7}: two-value diagonal, harmony-dominant
- CL preserves σ: ten-value diagonal, full operator information

This confirms their distinct roles:
- TSML measures where flow terminates (attracts to HARMONY)
- CL records the operator's own motion (one σ-step)

Neither is wrong. They ask genuinely different questions about the same operator event.

---

## The Q1/Q2 Cases in This Framework

**Q1 (j=1, LATTICE):** AGREEMENT point.
TSML and CL both say 7. The cycle entry is the unique point where
stabilization and memory align — because the cycle entry's first step IS the attractor.

**Q2 (j=7, HARMONY):** DIVERGENCE point.
TSML says 7: HARMONY-flow stabilizes to HARMONY (attractor is idempotent).
CL says 6: HARMONY's memory records its cycle-step (CHAOS/Faithfulness).
The attractor and the cycle-step diverge here. This is the sharpest example
of the stabilization/memory distinction.
