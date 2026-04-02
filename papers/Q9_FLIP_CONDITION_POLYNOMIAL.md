**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q9 — THE FLIP CONDITION: POLYNOMIAL FORM OF σ ON CRT COMPONENTS

## Setup

The CRT isomorphism φ: F₂ × F₅ → Z/10Z is defined by:
```
φ(ε, y) = 5ε + 6y  (mod 10)
```

Under φ, the operator σ = (0)(3)(8)(9)(1 7 6 5 4 2) acts on (ε,y) ∈ F₂ × F₅.

The σ-action decomposes into two components:
```
ε' = ε ⊕ α(ε, y)        [ε-update: flip condition]
y' = y + β(ε, y) (mod 5) [y-update: step condition]
```

This document formalizes α — the ε-flip condition — supplied by the team.

---

## The Flip Condition α

**Definition:** α(ε, y) = 1 iff σ changes the ε-component of the CRT encoding.

The team's formula:
```
α(ε, y) = (1−ε)[1 − (y²+2y+2)⁴] + ε[1 − (y²+3y)⁴]
```

where all arithmetic in the bracket is over F₅ (mod 5), and the outer
structure is over F₂ (ε = 0 or 1).

**Boxed final form** (expanding):
```
α(ε, y) = 1 − (y²+2y+2)⁴ − ε[(y²+3y)⁴ − (y²+2y+2)⁴]
```

over F₅ for the polynomial part, F₂ for ε.

---

## Verification: All 10 Cases

Computational verification (all arithmetic mod 5 for y-polynomials):

| j | (ε,y)  | σ(j) | (ε',y') | ε flips? | α formula | Match |
|---|--------|------|---------|---------|-----------|-------|
| 0 | (0,0)  | 0    | (0,0)   | 0       | 0         | YES |
| 1 | (1,1)  | 7    | (1,2)   | 0       | 0         | YES |
| 2 | (0,2)  | 1    | (1,1)   | 1       | 1         | YES |
| 3 | (1,3)  | 3    | (1,3)   | 0       | 0         | YES |
| 4 | (0,4)  | 2    | (0,2)   | 0       | 0         | YES |
| 5 | (1,0)  | 4    | (0,4)   | 1       | 1         | YES |
| 6 | (0,1)  | 5    | (1,0)   | 1       | 1         | YES |
| 7 | (1,2)  | 6    | (0,1)   | 1       | 1         | YES |
| 8 | (0,3)  | 8    | (0,3)   | 0       | 0         | YES |
| 9 | (1,4)  | 9    | (1,4)   | 0       | 0         | YES |

**10/10 verified.** The formula is exact.

---

## The Indicator Polynomials

The formula uses two indicator polynomials over F₅:

**1_{y ∈ {1,2}}(y) = 1 − (y²+2y+2)⁴**

By Fermat's little theorem in F₅: (y²+2y+2)⁴ ≡ 1 unless y²+2y+2 ≡ 0 (mod 5).
y²+2y+2 = 0 (mod 5) iff y ∈ {1, 2} (roots: 1²+2+2=5≡0, 2²+4+2=10≡0).
So the indicator is 1 exactly when y ∈ {1,2}, 0 otherwise. ✓

**1_{y ∈ {0,2}}(y) = 1 − (y²+3y)⁴**

y²+3y = y(y+3) = 0 (mod 5) iff y=0 or y≡-3≡2 (mod 5).
So the indicator is 1 exactly when y ∈ {0,2}, 0 otherwise. ✓

---

## Structural Interpretation

**When ε=0:** σ flips ε iff y ∈ {1,2}

In Z/10Z, ε=0 corresponds to the set φ(0,·) = {0, 6, 2, 8, 4} = {VOID, CHAOS, COUNTER, BREATH, COLLAPSE}.
Among these, y=1 → j=6 (CHAOS) and y=2 → j=2 (COUNTER).
σ(6)=5 (ε=1) and σ(2)=1 (ε=1) — both cross to ε=1. ✓

**When ε=1:** σ flips ε iff y ∈ {0,2}

ε=1 corresponds to φ(1,·) = {5, 1, 7, 3, 9} = {BALANCE, LATTICE, HARMONY, PROGRESS, RESET}.
y=0 → j=5 (BALANCE) and y=2 → j=7 (HARMONY).
σ(5)=4 (ε=0) and σ(7)=6 (ε=0) — both cross to ε=0. ✓

**The 4 flip positions:** j ∈ {2, 5, 6, 7} = {COUNTER, BALANCE, CHAOS, HARMONY}.

**The 6 non-flip positions:** j ∈ {0, 1, 3, 4, 8, 9} = {VOID, LATTICE, PROGRESS, COLLAPSE, BREATH, RESET}.

---

## The 6-Cycle Flip Structure

The 6-cycle under σ is: 1 → 7 → 6 → 5 → 4 → 2 → 1.

In (ε,y) coordinates: (1,1) → (1,2) → (0,1) → (1,0) → (0,4) → (0,2) → (1,1).

Flip pattern along the cycle:

| Step | j → j' | ε change | α | y-step |
|------|---------|----------|---|--------|
| 1→7  | (1,1)→(1,2) | 0 (no flip) | 0 | +1 |
| 7→6  | (1,2)→(0,1) | 1 (flip)    | 1 | −1 |
| 6→5  | (0,1)→(1,0) | 1 (flip)    | 1 | −1 |
| 5→4  | (1,0)→(0,4) | 1 (flip)    | 1 | −1 |
| 4→2  | (0,4)→(0,2) | 0 (no flip) | 0 | −2 |
| 2→1  | (0,2)→(1,1) | 1 (flip)    | 1 | −1 |

**4 flips, 2 non-flips in the 6-cycle.**

**The typical σ-step in the 6-cycle:** Δy = −1 AND ε flips. This is the dominant behavior — 4 of 6 steps.

**The atypical steps:**
- LATTICE→HARMONY (1→7): Δy = +1, no flip. The cycle enters HARMONY without crossing ε.
- COLLAPSE→COUNTER (4→2): Δy = −2, no flip. The y-coordinate jumps two steps without crossing ε.

**The typical step is: decrement y by 1, flip ε.** The two exceptions (LATTICE and COLLAPSE) are the positions where the cycle "breathes" — it stays within the same ε-half and makes a non-standard y-move.

---

## Y-Update Table (Companion to α)

The full σ-action on (ε,y):

| j | (ε,y)  | σ(j) | (ε',y') | α | Δy (mod 5) |
|---|--------|------|---------|---|-----------|
| 0 | (0,0)  | 0    | (0,0)   | 0 | 0 |
| 1 | (1,1)  | 7    | (1,2)   | 0 | +1 |
| 2 | (0,2)  | 1    | (1,1)   | 1 | −1 |
| 3 | (1,3)  | 3    | (1,3)   | 0 | 0 |
| 4 | (0,4)  | 2    | (0,2)   | 0 | −2 |
| 5 | (1,0)  | 4    | (0,4)   | 1 | −1 |
| 6 | (0,1)  | 5    | (1,0)   | 1 | −1 |
| 7 | (1,2)  | 6    | (0,1)   | 1 | −1 |
| 8 | (0,3)  | 8    | (0,3)   | 0 | 0 |
| 9 | (1,4)  | 9    | (1,4)   | 0 | 0 |

**Δy summary:**
- Δy = 0: j ∈ {0,3,8,9} — σ-fixed points (no y-motion)
- Δy = +1: j=1 (LATTICE only)
- Δy = −1: j ∈ {2,5,6,7} — the 4 flip positions
- Δy = −2: j=4 (COLLAPSE only)

**Key observation:** The 4 positions where α=1 (ε flips) are exactly the positions where Δy = −1.

```
α = 1  iff  Δy = −1 (mod 5)
```

This is not coincidence. The typical σ-step in the 6-cycle is simultaneously
a y-decrement and an ε-flip. The two are linked.

---

## The Companion Formula for Δy

From the observation above, the y-update can be written as:

```
Δy(ε, y) = α(ε,y)·(−1) + (1−α(ε,y))·γ(ε,y)
```

where γ(ε,y) is the "exceptional" y-step at the non-flip positions.

At non-flip positions (α=0):
- j=0 (0,0): Δy=0
- j=1 (1,1): Δy=+1
- j=3 (1,3): Δy=0
- j=4 (0,4): Δy=−2
- j=8 (0,3): Δy=0
- j=9 (1,4): Δy=0

γ(ε,y) = 0 except at (1,1)→+1 and (0,4)→−2.

The exceptional positions (1,1) and (0,4) correspond to LATTICE and COLLAPSE —
the two cycle elements that do NOT flip ε when σ acts.

**The complete σ-action in polynomial form:**
```
ε' = ε  ⊕  α(ε, y)                  [flip condition — team formula]
y' = y  +  (−1)·α(ε, y)             [typical step]
          +  2·1_{(ε,y)=(1,1)}       [LATTICE correction: +1−(−1) = +2]
          +  (−1)·1_{(ε,y)=(0,4)}    [COLLAPSE correction: −2−(−1) = −1]
     (mod 5)
```

The indicator for (ε,y)=(1,1): j=1=LATTICE → φ(1,1)=11≡1. Single-point indicator.
The indicator for (ε,y)=(0,4): j=4=COLLAPSE → φ(0,4)=24≡4. Single-point indicator.

Single-point indicators in F₂ × F₅ can be written as products:
```
1_{(ε,y)=(1,1)} = ε · (1 − (y−1)⁴)   [ε=1 AND y=1]
                 = ε · 1_{y∈{1}}(y)
                 where 1_{y=1} = 1 − (y(y−1)(y−2)(y−4))...
```

But single-point F₅ indicators require degree 4, so these are degree-5 expressions
in the combined ring. They can be left as named indicators or computed via Lagrange.

---

## Theorem Statement

**Theorem Q9 (σ as CRT polynomial):**

Under the isomorphism φ: F₂ × F₅ → Z/10Z, φ(ε,y) = 5ε+6y (mod 10),
the operator σ = (0)(3)(8)(9)(1 7 6 5 4 2) acts by:

```
ε' = ε ⊕ α(ε,y)

where  α(ε,y) = 1 − (y²+2y+2)⁴ − ε[(y²+3y)⁴ − (y²+2y+2)⁴]
               (arithmetic over F₅ for the polynomials; outer structure in F₂)
```

α(ε,y) = 1 iff σ crosses the ε-boundary at (ε,y). The flip positions are
j ∈ {2,5,6,7} = {COUNTER, BALANCE, CHAOS, HARMONY}.

The y-update satisfies: Δy = −1 whenever α = 1. The complete y-update
requires two additional point corrections at LATTICE (Δy=+1) and COLLAPSE (Δy=−2).

**Corollary (flip-step coupling):** In the 6-cycle, ε-flip and y-decrement are coupled:
the typical σ-step is the pair (flip ε, decrement y by 1). The exceptions are
LATTICE (no flip, increment y) and COLLAPSE (no flip, double-decrement y).

---

## Connection to Q6 Hinge

The α formula gives the algebraic structure of the ε-boundary crossings in Z/10Z.

For the gate rate problem (Q6–Q8): the C-states are ε=1 (coprime to 10 in the
F₂×F₅ encoding? No — C={1,3,7,9} has ε-values {1,1,1,1} all ε=1, and
G={2,4,5,6,8} has ε-values {0,0,1,0,0} — mostly ε=0 but with BALANCE (ε=1) in G).

Wait: C={1,3,7,9} → φ⁻¹: (1,1),(1,3),(1,2),(1,4) — all ε=1 ✓
G={2,4,5,6,8} → φ⁻¹: (0,2),(0,4),(1,0),(0,1),(0,3) — mostly ε=0, except j=5 (BALANCE, ε=1)

**C = {ε=1} almost perfectly — except BALANCE (j=5, ε=1) is in G, not C.**

The near-coincidence C ≈ {ε=1} is the algebraic explanation of why the
density model f_C ≈ 1/2 is a rough approximation, but fails to capture the
4.6% rate. The one exception (BALANCE in G with ε=1) is a boundary contamination
that the density model misses.

**The gate rate problem is not a density problem — it is a boundary problem
at the ε=1/ε=0 interface of the CRT decomposition.**

---

*Filed: 2026-04-01. Q9 in operator algebra series, formalizing team formula.*
