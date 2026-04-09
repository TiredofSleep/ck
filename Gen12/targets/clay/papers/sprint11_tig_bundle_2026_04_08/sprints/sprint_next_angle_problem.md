# SPRINT: THE NEXT ANGLE PROBLEM
## A Flagship Tomography Benchmark for UOP-Guided Measurement Choice
*Benchmark: 4×4 discrete phantom, parallel-beam CT. All matrices explicit and reproducible.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## The Imaging Question

A 2D parallel-beam CT scanner takes projection measurements at discrete angles. After one angle, you can afford one more scan. Which angle maximizes information?

> **"You already collected one projection. You can afford one more scan. Which angle should you take?"**

This is the core decision in sparse-view CT, limited-angle CT, and adaptive scanning protocols.

---

## System: 4×4 Discrete Phantom

**Image:** μ ∈ ℝ^16, indexed as a 4×4 grid. Pixel (r,c) at vector index 4r+c, for r,c ∈ {0,1,2,3}.

```
Pixel layout (index in vector):

  c=0  c=1  c=2  c=3
r=0: [ 0,   1,   2,   3 ]
r=1: [ 4,   5,   6,   7 ]
r=2: [ 8,   9,  10,  11 ]
r=3: [12,  13,  14,  15 ]
```

**Projection model:** Parallel-beam CT. Angle θ gives a set of line-integral measurements across the image. Each ray sums pixel values along its path.

**Three exact projection angles defined here:**

| Angle | Direction | Rays | Matrix size |
|---|---|---|---|
| θ = 0° | Horizontal (left-right) | 4 rows | R₀ ∈ ℝ^{4×16} |
| θ = 90° | Vertical (top-bottom) | 4 columns | R₉₀ ∈ ℝ^{4×16} |
| θ = 45° | Diagonal (top-left to bottom-right) | 7 diagonals | R₄₅ ∈ ℝ^{7×16} |

---

## Explicit Projection Matrices

**R₀ — horizontal (θ=0°):**
```
Each row i sums pixels in row i: μ[4i], μ[4i+1], μ[4i+2], μ[4i+3].

R₀ = [[1,1,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0],   ← row 0 sum
      [0,0,0,0, 1,1,1,1, 0,0,0,0, 0,0,0,0],   ← row 1 sum
      [0,0,0,0, 0,0,0,0, 1,1,1,1, 0,0,0,0],   ← row 2 sum
      [0,0,0,0, 0,0,0,0, 0,0,0,0, 1,1,1,1]]   ← row 3 sum
```

**R₉₀ — vertical (θ=90°):**
```
Each column j sums pixels in column j: μ[j], μ[4+j], μ[8+j], μ[12+j].

R₉₀ = [[1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0],  ← col 0 sum
       [0,1,0,0, 0,1,0,0, 0,1,0,0, 0,1,0,0],  ← col 1 sum
       [0,0,1,0, 0,0,1,0, 0,0,1,0, 0,0,1,0],  ← col 2 sum
       [0,0,0,1, 0,0,0,1, 0,0,0,1, 0,0,0,1]]  ← col 3 sum
```

**R₄₅ — diagonal (θ=45°):**
```
The 7 diagonals of the 4×4 image, indexed by offset d = c − r:

d=-3: {(3,0)=12}
d=-2: {(2,0)=8,  (3,1)=13}
d=-1: {(1,0)=4,  (2,1)=9,  (3,2)=14}
d= 0: {(0,0)=0,  (1,1)=5,  (2,2)=10, (3,3)=15}
d=+1: {(0,1)=1,  (1,2)=6,  (2,3)=11}
d=+2: {(0,2)=2,  (1,3)=7}
d=+3: {(0,3)=3}

R₄₅ = [[0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],  ← d=-3
        [0,0,0,0, 0,0,0,0, 1,0,0,0, 0,1,0,0],  ← d=-2
        [0,0,0,0, 1,0,0,0, 0,1,0,0, 0,0,1,0],  ← d=-1
        [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1],  ← d= 0
        [0,1,0,0, 0,0,1,0, 0,0,0,1, 0,0,0,0],  ← d=+1
        [0,0,1,0, 0,0,0,1, 0,0,0,0, 0,0,0,0],  ← d=+2
        [0,0,0,1, 0,0,0,0, 0,0,0,0, 0,0,0,0]]  ← d=+3
```

---

## Null Space Analysis

**Null space of R₀:**

ker(R₀) = { μ ∈ ℝ^16 : all row sums = 0 }

Dimension: 16 − rank(R₀) = 16 − 4 = **12**.

Basis: for each row r ∈ {0,1,2,3} and each pair of pixels in that row, the difference vector e_{4r+c} − e_{4r+c'} is in ker(R₀). Any image whose pixels within each row sum to zero is invisible to R₀.

**Visual examples of elements in ker(R₀):**

```
Invisible to θ=0° (row sums all zero):

Pattern A          Pattern B
[+1 -1  0  0]    [+1 +1 -1 -1]
[ 0  0  0  0]    [ 0  0  0  0]
[+1 -1  0  0]    [ 0  0  0  0]
[ 0  0  0  0]    [ 0  0  0  0]

Both have row sums = 0. Neither is visible to the horizontal scanner.
These represent the "ambiguity" that one horizontal projection cannot resolve.
```

**Null space of R₉₀:**

ker(R₉₀) = { μ : all column sums = 0 }

Dimension: 16 − 4 = **12**.

**Null space of R₄₅:**

ker(R₄₅) = { μ : all diagonal sums = 0 }

Dimension: 16 − rank(R₄₅). Since each of the 7 diagonal sums is independent (each pixel in exactly one diagonal), rank(R₄₅) = 7.  Null space dimension: 16 − 7 = **9**.

---

## Joint Null Spaces After Adding Each Candidate

**Rank analysis (proved):**

rank(R₀) = 4.

rank([R₀; R₉₀]):
Rows of R₀ are horizontal sums; rows of R₉₀ are column sums. The total pixel sum = (sum of row 0) + ... + (sum of row 3) = (sum of col 0) + ... + (sum of col 3). This is one linear dependency between the two sets of rows. No other dependencies exist (for a 4×4 image, row-sum measurements and column-sum measurements are otherwise independent).

**rank([R₀; R₉₀]) = 4 + 4 − 1 = 7.** Null space dimension = 9.

rank([R₀; R₄₅]):
The grand total appears in both R₀ and R₄₅ (sum of all row sums = sum of all diagonal sums = total pixel sum). One linear dependency.

For additional dependencies: R₀ rows group pixels by horizontal coordinate; R₄₅ rows group pixels by diagonal coordinate. For the 4×4 integer grid, these groupings have no other linear relationships.

**rank([R₀; R₄₅]) = 4 + 7 − 1 = 10.** Null space dimension = 6.

rank([R₀; R₀]) = rank(R₀) = 4 (exact repeat — no new rows).

**Null space dimension after adding each candidate:**

| Candidate | rank([R₀; R_θ]) | Null space dim | Rank gain (UOP score) |
|---|---|---|---|
| R₀ repeat (θ=0°) | 4 | 12 | **0** |
| R₉₀ (θ=90°) | 7 | 9 | **3** |
| R₄₅ (θ=45°) | 10 | 6 | **6** |
| R₁₃₅ (θ=135°) | 10 | 6 | **6** |

**Theorem (proved — Repeat-Angle Null Space Invariance):**

For parallel-beam CT, any repeat of angle θ (or its antipodal θ+180°) leaves the null space of the current measurement set unchanged: rank(F ∪ {R_θ}) = rank(F) whenever R_θ ∈ F (or R_{θ+180°} ∈ F, since R_{θ+180°} = R_θ for parallel-beam). UOP score = 0 exactly.

**Proof:** In parallel-beam CT, the projection at angle θ and angle θ+180° measure identical line integrals (same lines, same direction). Mathematically: R_{θ+180°} = R_θ (equal matrices). Adding a repeated row to any matrix does not change its rank. Therefore rank(F ∪ {R_θ}) = rank(F). The null space is unchanged. □

---

## The Divergence: Noise Scenario

**Physical motivation:** Horizontal projections (θ=0°) in a hospital CT scanner align with the gantry axis — minimal mechanical vibration, stable detector geometry. Vertical projections (θ=90°) require rotating the gantry 90° — more vibration, different detector response. Diagonal projections (θ=45°) are intermediate. The upshot: σ(θ=0°) < σ(θ=45°) < σ(θ=90°).

**Noise levels:**

| Candidate | Angle | Noise σ | Physical reason |
|---|---|---|---|
| R₀_repeat | 0° | **0.3** | Gantry at home position — lowest noise |
| R₄₅ | 45° | 0.8 | Gantry at 45° — moderate noise |
| R₉₀ | 90° | 1.0 | Gantry at 90° — most noise |

**FIM trace contribution from each candidate (over current setup after R₀ with σ₀=1.0):**

FIM addition from candidate θ with noise σ_θ:

ΔJ_θ = (1/σ_θ²) × R_θᵀ R_θ

trace(R₀ᵀR₀): Each of the 16 pixels appears in exactly one row of R₀, so each diagonal entry (R₀ᵀR₀)[j,j] = 1. trace = 16.

trace(R₉₀ᵀR₉₀): Same argument (each pixel in one column). trace = 16.

trace(R₄₅ᵀR₄₅): Same argument (each pixel in one diagonal). trace = 16.

**FIM trace addition from each candidate:**

- R₀_repeat (σ=0.3): ΔJ trace = (1/0.09) × 16 = **177.8** ← classical loves this
- R₄₅ (σ=0.8): ΔJ trace = (1/0.64) × 16 = **25.0**
- R₉₀ (σ=1.0): ΔJ trace = (1/1.0) × 16 = **16.0**

**The divergence is stark:**

Classical trace criterion: R₀_repeat wins by a factor of 7. The lower noise (σ=0.3 vs σ=0.8) translates to a (0.8/0.3)² = 7.1× trace advantage. An engineer optimizing total FIM trace would scan the gantry at 0° again.

UOP: R₀_repeat is eliminated (score=0). It adds nothing to the null space.

---

## Decision Table

| Candidate | Angle | σ | UOP rank gain | FIM trace | Classical rank | Hybrid rank | Null space after |
|---|---|---|---|---|---|---|---|
| **R₀_repeat** | **0°** | **0.3** | **0** | **177.8** | **1st** | **ELIMINATED** | 12D (unchanged) |
| R₄₅ | 45° | 0.8 | **6** | 25.0 | 2nd | **1st** | 6D |
| R₉₀ | 90° | 1.0 | 3 | 16.0 | 3rd | 2nd | 9D |

**Classical picks R₀_repeat (trace=177.8).** After the scan: null space unchanged. The 12-dimensional ambiguity is completely intact. The image cannot be reconstructed any better than before.

**Hybrid picks R₄₅ (score=6, trace=25.0).** After the scan: null space shrinks from 12D to 6D. Six previously ambiguous structure classes are resolved.

---

## Hybrid Protocol Applied

**Step 1 — UOP structural screen:**

For each candidate θ: compute rank gain = rank([R_current; R_θ]) − rank(R_current).

- R₀_repeat: rank gain = 0. **ELIMINATED.** "The horizontal projection adds no new distinguishable structure. Adding it precisely measures what is already measured."
- R₄₅: rank gain = 6. **Survives.**
- R₉₀: rank gain = 3. **Survives.**

**Step 2 — Classical rank survivors:**

FIM trace: R₄₅ (25.0) > R₉₀ (16.0).

**Step 3 — Select R₄₅.**

---

## What the Null Space Looks Like: Pattern Analysis

**ker(R₀) — structures invisible to θ=0° (horizontal):**

These are images with all row sums = 0. They include:
- Any within-row contrast pattern: alternating ±values within a row
- Examples: horizontal checkerboards, vertical stripes with alternating signs

```
Sample element of ker(R₀):
[+1 -1 +1 -1]   ← row sum = 0
[+1 -1 +1 -1]   ← row sum = 0
[+1 -1 +1 -1]   ← row sum = 0
[+1 -1 +1 -1]   ← row sum = 0

A "vertical stripe" pattern — completely invisible to horizontal projection.
```

**ker([R₀, R₉₀]) — structures invisible to BOTH horizontal and vertical:**

Must have all row sums AND all column sums = 0. These are the "doubly invisible" patterns.

For a 2×2 sub-block, the canonical element:
```
[+1 -1]
[-1 +1]    ← sum of each row = 0, sum of each column = 0
```

For the 4×4 image, the 9-dimensional null space of [R₀; R₉₀] is spanned by 9 independent "checkered" patterns:

```
Sample element of ker([R₀;R₉₀]):
[+1 -1  0  0]
[-1 +1  0  0]
[ 0  0  0  0]
[ 0  0  0  0]

Row sums: 0,0,0,0 ✓
Col sums: 0,0,0,0 ✓
→ Invisible to both horizontal AND vertical projection.
```

These are the "checkerboard ambiguities" that neither horizontal nor vertical scanning can resolve. A third angle (45° or other) is needed.

**ker([R₀, R₄₅]) — structures invisible to horizontal AND diagonal:**

Must have all row sums = 0 AND all diagonal sums = 0. This is more constrained — 6-dimensional.

The structures invisible to the horizontal+diagonal pair are more exotic: they require zero in both horizontal and diagonal integrated density, which forces specific multi-directional cancellations. 6 fewer degrees of freedom than the 12D original null space.

---

## Reconstruction Consequence

**One-angle (R₀ only):**

From 4 measurements (4 row sums), 16 unknowns. Under-determined by 12. Any image μ can be replaced by μ + v for any v ∈ ker(R₀) without changing the measurement. The "reconstruction" can set any within-row contrast arbitrarily — vertical stripes are invisible.

**Two-angle {R₀, R₉₀}:**

From 7 independent measurements. Under-determined by 9. The checkerboard ambiguities (within-row AND within-column) remain unresolved.

**Two-angle {R₀, R₄₅}:**

From 10 independent measurements. Under-determined by 6. More structure resolved, but still under-determined. Six residual ambiguity classes remain.

**Two-angle {R₀, R₀_repeat}:**

Still 4 independent measurements. Under-determined by 12. IDENTICAL to one-angle. The precise repeat gives confidence in the row sums but adds no resolution of vertical structure.

**The engineering consequence:** Buying a second scan at θ=0° with 2× better detector (σ=0.3 vs 1.0) gives σ/√2 ≈ 0.71 standard deviation on the row sums — 29% reduction. It gives **zero** reduction in the null-space uncertainty: the within-row structure remains completely unknown.

---

## Frequency-Domain Interpretation

In 2D CT, the Fourier Slice Theorem (proved) states: the projection at angle θ fills the frequency domain along the line perpendicular to θ (through the origin).

- θ=0° fills the **horizontal frequency line** (all frequencies with ky=0).
- θ=90° fills the **vertical frequency line** (kx=0).
- θ=45° fills the **diagonal frequency line** (kx=−ky).
- θ=0° repeat fills the **same horizontal line** — no new frequencies added.

The null space of a set of angles = all frequency components NOT covered by any angle's Fourier line. The residual ambiguity after angle set F is the set of image components at uncovered frequencies.

**UOP score of a new angle θ = number of new frequency components covered** (= rank gain of the projection matrix).

A near-repeat (θ=1°) adds a frequency line very close to the θ=0° line — minimal new coverage. An orthogonal angle (θ=90°) adds the perpendicular line — maximum new coverage for a single scan after θ=0°.

---

## Proposition: Classical FIM Trace Does Not Measure New Coverage

**Proposition (proved).**
For parallel-beam CT with measurement R_θ at noise σ:

trace(FIM addition from θ) = (1/σ²) × |{rays at angle θ}|

This is **independent of the current measurement set** and **independent of the null space reduction** provided by angle θ. It depends only on the noise level and number of rays.

**Proof.** FIM addition = (1/σ²) × R_θᵀR_θ. For the 4×4 grid with one pixel per ray: trace(R_θᵀR_θ) = sum of squared norms of columns of R_θ = number of pixels (each pixel in exactly one ray) = 16. Therefore trace(FIM addition) = 16/σ². Independent of which angle θ, independent of what was measured before. □

**Corollary.** FIM trace criterion applied to candidate angles ranks them entirely by noise level, with no information about structural coverage. The criterion cannot distinguish a repeat angle from a genuinely new angle, because trace(R₀ᵀR₀/σ₀²) = trace(R₉₀ᵀR₉₀/σ₉₀²) = 16/σ² regardless of direction.

**This is the divergence.** A 0° repeat with σ=0.3 has trace 177.8. A 90° scan with σ=1.0 has trace 16.0. Classical trace ranks the repeat 11× better. UOP eliminates the repeat (score=0) and selects the 90° scan (score=3) or 45° scan (score=6).

---

## Summary

**Benchmark:** 4×4 discrete phantom, parallel-beam CT. Explicit projection matrices. Reproducible.

**Current scan:** θ=0° (horizontal), σ=1.0. Null space: 12-dimensional.

**Classical top pick:** θ=0° repeat (σ=0.3, FIM trace = 177.8). After the scan: null space unchanged (12D). The repeated scan gives excellent row-sum precision but zero new structural information.

**Hybrid top pick:** θ=45° diagonal (score=6, trace=25.0). After the scan: null space shrinks to 6D. Six previously ambiguous image classes are resolved.

**Decision table (key rows):**

| Candidate | σ | UOP score | FIM trace | Selected by | Null space after |
|---|---|---|---|---|---|
| θ=0° repeat | 0.3 | **0** | **177.8** | Classical | 12D (no change) |
| θ=45° | 0.8 | **6** | 25.0 | **Hybrid** | 6D |
| θ=90° | 1.0 | 3 | 16.0 | — | 9D |

**Theorem (proved):** Repeating any projection angle gives rank gain = 0 regardless of noise level. FIM trace from a repeated angle = 16/σ² (grows without bound as σ→0) while null space reduction = 0. Classical trace criterion and UOP diverge monotonically: as σ→0 for the repeated angle, classical rank → 1st while UOP score remains 0.

**Strongest honest claim:**
> For discrete CT, the second-scan decision is answered structurally: choose the angle with maximum rank gain (UOP score), not maximum FIM trace. FIM trace measures precision in directions already covered by the first scan — it grows with better detector hardware and says nothing about structural coverage of new image components. The 4×4 benchmark makes this exact: any horizontal repeat, however precise, cannot resolve vertical texture. The hybrid protocol correctly selects the diagonal angle (score=6) over the precise repeat (score=0, trace=177.8).

**Strongest honest boundary:**
> The 4×4 discrete benchmark uses an idealized projection model (binary projection matrices, no partial pixel coverage, no beam divergence). Real CT scanners use continuous fan-beam or cone-beam geometry with area-weighted projection matrices. In that setting: (1) the "exact repeat" is replaced by a "near-repeat" (slightly different path through pixels), giving a tiny positive rank gain rather than exactly zero; (2) the UOP score becomes a continuous quantity (rank gain measured by effective rank, not integer rank); (3) the FIM trace divergence holds qualitatively but the exact threshold between "structurally useful" and "structurally redundant" requires the ε-practical score from the prior sprint. The fundamental result — that angular diversity drives reconstruction quality more than measurement precision — holds in continuous geometry and is the theoretical basis for compressed sensing CT angle selection.
