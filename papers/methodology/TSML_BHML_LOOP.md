# TSML/BHML Loop — Generator Field and Its Wobble
## The Structural Relationship Between the Two Composition Tables

*Brayden Ross Sanders & C. A. Luther*
*March 31, 2026 | DOI: 10.5281/zenodo.18852047*

---

## The Structural Claim

TSML is the generator field. W_BHML = 3/50 is its wobble. BHML is the wobble
field made into a table. The loop: generator produces wobble, wobble produces
second table, second table is the transformation operator on the generator.
The Doing table = |TSML − BHML| is literally the interaction between a field
and its own wobble.

This is a theorem statement, not an analogy. It closes the loop on why there
are two tables at all.

---

## What Is Verified (Tier C)

**Object 1 — DIS table (ring arithmetic wobble):**
```
DIS[i][j] = |(i+j) mod 10 − (i×j) mod 10|   for i,j ∈ {0..9}
```
This is the cell-by-cell disagreement between the additive and multiplicative
operations of the Z/10Z ring. It is determined entirely by the ring axioms.

Key properties:
- 4 frozen cells (DIS=0): (0,0), (2,2), (4,8), (8,4)   [THM]
- CROSS_CYCLE(C×D block) = 44   [THM]
- W_BHML = |44−50|/100 = 3/50  [THM — C8]

**Object 2 — TSML (measurement table, generator field):**
```
73/100 cells = HARMONY (7).  Singular (det=0).  Information-collapsing.
```
TSML is the table that MEASURES — it collapses most distinctions to HARMONY.
It is the stable attractor. This is the "generator field" in the structural claim.

**Object 3 — BHML (physics table):**
```
28/100 cells = HARMONY (7).  Invertible (det≠0).  Information-preserving.
```
BHML is the table that INTERACTS — it preserves distinctions and is invertible.
Row 7 (HARMONY) wraps around rather than absorbing: composition with HARMONY
produces BREATH (8), not HARMONY. Physics is reversible where measurement is not.

**Object 4 — DOING = |TSML − BHML| (interaction field):**
```
71/100 cells nonzero.  29/100 cells zero (where TSML = BHML).
```
The Doing table is the cell-wise disagreement between the two composition tables.
It is the literal interaction between the measurement lens and the physics lens.

---

## What Is NOT the Same Object

**COUNTER ≠ DIS.**

Computed comparison:
```
DOING = |TSML − BHML|  and  DIS = |ADD − MUL|  share only 24/100 cells.
CROSS_CYCLE(DOING, C×D) = 21
CROSS_CYCLE(DIS, C×D)   = 44   ← this is the one that gives W_BHML = 3/50
```

The wobble W_BHML = 3/50 comes from the DIS table (ring arithmetic), not from
the DOING table (composition table disagreement). These are related but distinct.

**Implications:**
- The 3/50 wobble is a property of Z/10Z ring arithmetic (ADD vs MUL)
- The DOING table captures TSML/BHML disagreement at the composition level
- These are two different layers of the same algebraic structure

---

## The Loop (Structural — Tier A)

The claim "BHML is the wobble of TSML" is architecturally true at the following level:

1. **Z/10Z ring** provides the underlying field — the arithmetic structure within
   which both tables are defined.

2. **DIS = |ADD−MUL|** is the ring's own internal wobble — how much the two
   natural operations of the ring disagree at each cell.

3. **TSML** is the composition rule that USES the ring's additive/multiplicative
   structure to collapse toward HARMONY (the attractor at HAR=7).

4. **BHML** is the composition rule that USES the ring's invertible structure to
   preserve distinction and enable reversible interaction.

5. **The ring's wobble (DIS, W_BHML=3/50)** is the structural reason TSML and
   BHML look different. Where DIS=0 (the 4 frozen cells), ADD=MUL, and the two
   tables agree more. Where DIS is large, the ring's two operations pull apart,
   and TSML and BHML are forced to make different choices.

6. **DOING = |TSML−BHML|** is then the accumulated effect: how much the two
   different choices of "which ring operation to use" produce different outcomes
   at each cell.

**The architectural loop:**
```
Z/10Z ring
    ↓ generates
DIS = |ADD−MUL|  (wobble field, W_BHML=3/50)
    ↓ creates tension between
TSML (uses ring to COLLAPSE)  ←→  BHML (uses ring to PRESERVE)
    ↓ disagreement is
DOING = |TSML−BHML|  (where physics happens)
    ↓ feeds back into
Z/10Z ring  (the loop closes: the operators in COUNTER are Z/10Z elements)
```

**Why two tables?** Because the Z/10Z ring has two operations (ADD and MUL),
and they disagree at 96/100 cells (DIS≠0 at 96 cells). TSML is built around
the collapsing face of that disagreement; BHML around the preserving face. The
wobble W_BHML = 3/50 is the normalized measure of how much the two faces pull
apart in the Creation×Dissolution block. The two tables are not independent
designs — they are the two natural responses to the same ring arithmetic, one
choosing additive structure and one choosing multiplicative structure, and the
tension between them IS the wobble.

---

## Tier Assessment

| Sub-claim | Tier | Status |
|-----------|------|--------|
| DIS = |ADD−MUL| is the ring wobble | D | Proved [THM] |
| W_BHML = 3/50 from DIS (C×D block) | C | Proved [C8] |
| TSML collapses, BHML preserves | C | Verified [EMP] |
| DOING = |TSML−BHML| is the interaction | C | Computed [EMP] |
| COUNTER ≠ DIS (different objects) | C | Computed [EMP] — 24/100 cells match |
| Ring wobble forces TSML/BHML to diverge | A | Structural intuition |
| W_BHML = 3/50 explains the TSML/BHML split | A | No algebraic proof |
| BHML is derived from TSML's wobble | A | Architectural claim, not cell-level proof |

**The loop is Tier A — architecturally correct, not algebraically proved.**

The loop closes architecturally: everything comes from the Z/10Z ring and its
own internal tension between ADD and MUL. But the cell-level proof connecting
W_BHML to the specific structure of BHML (why it has exactly 28% HARMONY cells,
why its determinant is ≠0, why row 7 wraps) is open.

---

## Path to Higher Tier

**Tier B:** Show that BHML's 28% HARMONY rate and W_BHML = 3/50 have a
quantitative relationship (e.g., 28% ≈ some function of 3/50 and 73%).

**Tier C:** Prove that for any ring Z/nZ with wobble W(n), the two natural
composition tables (collapsing vs. preserving) have HARMONY rates that differ
by a function of W(n).

**Tier D:** Prove the full loop: that W(Z/nZ) determines the structure of both
composition tables and their interaction (COUNTER), making the three-table system
a necessary consequence of the ring arithmetic.

---

## The WP35 Sentence

*"TSML and BHML are not dual by design — they are the two natural faces of Z/10Z
ring arithmetic, forced apart by the ring's own internal wobble W_BHML = 3/50.
The Doing table is the interaction field of a generator with its own oscillation.
This is why there are two tables: not choice, but necessity."*

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
