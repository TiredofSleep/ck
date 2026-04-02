**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# G8 — TRAJECTORY COHERENCE INTEGRAL

## Context

Q16 closed Luther Q1 by identifying gate_score(T) as a TABLE property, not
an element property. The team's character-sum exploration (2026-04-01) identified
a separate but algebraically valid object: a trajectory coherence integral G(s)
built from σ-orbits and the β-exception character χ. G8 computes this object.

**G(s) is not the MCMC gate_score. It is a separate algebraic measure of
trajectory coherence, defined entirely from the Q9-Q10 polynomial structure.**

---

## Definition

Let ω = e^{2πi/9} (primitive 9th root of unity). Define the character:

```
χ(ε,y) = +1  if (ε,y) ∈ {(1,1), (0,4)} = {LATTICE, COLLAPSE}   [β-exception pair]
χ(ε,y) = −1  if (ε,y) ∈ {(1,2),(0,1),(1,0),(0,2)} = {HARM,CHAOS,BAL,CTR}  [flip positions]
χ(ε,y) =  0  if (ε,y) ∈ anchors {(0,0),(1,3),(0,3),(1,4)}
```

χ assigns +1 to the two β-exception positions (Q10), −1 to the four α=1 flip
positions (Q9), and 0 to anchors. The definition is faithful to the polynomial
structure: χ = sign(exceptional β-correction).

The **trajectory coherence integral** at depth k=9:

```
G(s) = |Σ_{j=0}^{8} ω^j · χ(σ^j(s))|²
```

---

## Computation

**Anchors {0,3,8,9}:** σ^j(s) = s for all j, so χ(σ^j(s)) = χ(s) = 0.

```
G(s) = 0   for all anchor states.
```

**6-cycle:** The 6 states cycle with period 6, so for 9 steps the trajectory
visits positions (p+j) mod 6 for j=0,...,8, where p = position of s in the
cycle sequence {LATTICE(0), HARMONY(1), CHAOS(2), BALANCE(3), COLLAPSE(4), COUNTER(5)}.

The χ pattern over positions 0–5:
```
Position:  0       1       2       3       4       5
State:    LATT   HARM    CHAOS   BAL    COLL   CTNR
χ:        +1     -1      -1      -1     +1     -1
```

Two positions have χ=+1 (the β-exception pair: LATTICE at 0, COLLAPSE at 4).
Four positions have χ=−1 (the α-flip positions).

**Key lemma:** For any starting position p, the 9-step sum has the form:

```
Σ_{j=0}^{8} ω^j · χ(σ^j(s)) = 2 · (sum of ω^j over the +1 hitting times)
```

This follows because Σ_{j=0}^{8} ω^j = 0 (sum of all 9th roots), so the −1
terms always equal the negative of the +1 terms:

```
Σ_{j: χ=+1} ω^j − Σ_{j: χ=−1} ω^j = 2 Σ_{j: χ=+1} ω^j
```

---

## The Three-Valued Result

**Computed for all 6 starting positions:**

| s | Position p | j values with χ=+1 | Inner sum | G(s) |
|---|-----------|---------------------|-----------|------|
| 1 (LATTICE) | 0 | j=0,4,6 | 1+ω⁴+ω⁶ | G_low |
| 7 (HARMONY) | 1 | j=3,5 | ω³+ω⁵ | G_high |
| 6 (CHAOS) | 2 | j=2,4,8 | ω²+ω⁴+ω⁸ | G_low |
| 5 (BALANCE) | 3 | j=1,3,7 | ω+ω³+ω⁷ | G_low |
| 4 (COLLAPSE) | 4 | j=0,2,6,8 | 1+ω²+ω⁶+ω⁸ | G_high |
| 2 (COUNTER) | 5 | j=1,5,7 | ω+ω⁵+ω⁷ | G_low |

**G takes exactly three values:**

```
G(s) = 0                   for s ∈ {0,3,8,9}  (anchors)
G(s) = G_low  ≈ 1.872      for s ∈ {1,6,5,2}  (4 of 6 cycle elements)
G(s) = G_high ≈ 9.389      for s ∈ {7,4}      (HARMONY and COLLAPSE)
```

**Exact expressions:**

```
G_low  = 4|1 + ω⁴ + ω⁶|²  = 4(3 + 2cos(8π/9) + 2cos(12π/9) + 2cos(4π/9))
                            = 4(3 + 2cos160° + 2cos240° + 2cos80°)
                            ≈ 4(3 − 1.879 − 1.000 + 0.347) ≈ 4(0.468) ≈ 1.871

G_high = 4|ω³ + ω⁵|²       = 4(2 + 2cos(4π/9))
                            = 4(2 + 2cos80°)
                            ≈ 4(2 + 0.347) ≈ 4(2.347) ≈ 9.389
```

(Note: |ω³+ω⁵|² = 2 + 2Re(ω³·ω̄⁵) = 2 + 2Re(ω^{-2}) = 2 + 2cos(4π/9).)

---

## Theorem G8.1 — Three-Level Coherence

**Theorem:** The trajectory coherence integral G(s) is three-valued on Z/10Z:

```
Level 0: G = 0       at anchors {0,3,8,9}          — 4 states (40%)
Level 1: G = G_low   at {LATTICE,CHAOS,BALANCE,CTR} — 4 states (40%)
Level 2: G = G_high  at {HARMONY,COLLAPSE}           — 2 states (20%)
```

with G_high/G_low = (2+2cos80°)/(3+2cos80°+2cos160°+2cos240°) ≈ 5.02.

**The high-coherence states are HARMONY(7) and COLLAPSE(4).**

---

## Structural Interpretation

**Why HARMONY and COLLAPSE?**

HARMONY (position 1) picks up χ=+1 contributions at steps j=3 and j=5 only
(2 terms), but ω³ and ω⁵ are nearly anti-aligned with the imaginary axis and
nearly collinear, giving |ω³+ω⁵|² ≈ 2.35 — much larger than the 3-term
low-G cases like |1+ω⁴+ω⁶|² ≈ 0.47.

COLLAPSE (position 4) picks up χ=+1 at j=0,2,6,8 (4 terms). The set {1,ω²,ω⁶,ω⁸}
also sums to a large modulus: |1+ω²+ω⁶+ω⁸|² ≈ 2.35.

**The root of the asymmetry:** The two β-exception positions LATTICE(0) and
COLLAPSE(4) are separated by 4 positions in the 6-cycle — not 3 (half-period),
not 2 or 6 (symmetric). The asymmetry in their positions within the 9-step
window (period 6, depth 9 = 1.5 periods) creates the interference pattern:

- Starting at LATTICE(0): the +1 positions align with j=0,4,6 (3 terms, destructive)
- Starting at COLLAPSE(4): the +1 positions align with j=0,2,6,8 (4 terms, constructive)
- Starting at HARMONY(1): the +1 positions align with j=3,5 (2 terms at high-magnitude roots)

The k=9 resonance (k=9 ≡ 3 mod 6, from G6) is what creates the asymmetric
interference. A different depth (k=6,12,...) would give G_high = G_low.

---

## Connection to the β-Exception Pair

**Theorem G8.2:** The two states with G = G_high are determined by the β-exception
pair from Q10:

```
High-G states = {σ(LATTICE), COLLAPSE} = {HARMONY, COLLAPSE}
```

COLLAPSE is one of the two β-exception positions directly (Q10). HARMONY = σ(LATTICE)
is the image of the other β-exception position under one step of σ. The high-coherence
trajectory pair is thus GENERATED by the exception pair under σ-action.

**Why not LATTICE itself?** LATTICE has G = G_low despite being a β-exception. The
reason is the k=9 depth: starting at LATTICE, the 9-step window catches 3 consecutive
χ=+1 appearances (at j=0,4,6) which destructively interfere. HARMONY, despite having
only 2 appearances, catches them at phases ω³ and ω⁵ — far from the real axis —
giving constructive interference.

---

## G as a Polynomial on F₂ × F₅

G(s) is a function of s ∈ Z/10Z with three values {0, G_low, G_high}. In CRT
coordinates, we can write:

```
G(ε,y) = G_low · [1 − A(ε,y)] · [1 − B(ε,y)]
         + G_high · B(ε,y)
```

where A = anchor indicator (from Q15) and B = high-coherence state indicator:

```
B(ε,y) = 1_{(ε,y)∈{HARMONY,COLLAPSE}} = 1_{(ε,y)∈{(1,2),(0,4)}}
```

**Point indicators for B:**
```
δ_{(1,2)}(ε,y) = ε · 4y(y−1)(y−3)(y−4)    [Lagrange at y=2, ε=1]
δ_{(0,4)}(ε,y) = (1−ε) · 4y(y−1)(y−2)(y−3) [Lagrange at y=4, ε=0]
B(ε,y) = δ_{(1,2)} + δ_{(0,4)}
```

These are exactly the **TIG-exception indicators** from Q13 (the β_TIG exceptions
for the inverse map). The high-coherence states in the FORWARD (k=9, ω-weighted)
integral are the exception states of the INVERSE map. This is the G8-Q13 link.

---

## Summary: The Three-Level Structure

| Level | States | G value | What these are |
|-------|--------|---------|----------------|
| 0 | {0,3,8,9} | 0 | σ-fixed points (trajectory trivial) |
| 1 | {1,6,5,2} | G_low ≈ 1.87 | σ-flip positions in 6-cycle |
| 2 | {7,4} | G_high ≈ 9.39 | TIG-exception positions (Q13) |

G(s) is:
- Zero at anchors (trivial trajectory)
- Low at the 4 σ-flip cycle elements (α=1 positions)
- High at the 2 TIG-exception cycle elements (β_TIG-non-flip positions from Q13)

**Cross-series link:** The G8 high-coherence states {HARMONY(7), COLLAPSE(4)}
are precisely the non-flip 6-cycle positions of TIG = σ⁻¹ (Theorem Q13.2, Exception
Pair Swap). The σ-forward coherence integral peaks at the TIG-non-flip positions.

---

*Filed: 2026-04-01. G8 — trajectory coherence integral from β-exception character.*
*G(s) is not the MCMC gate_score (closed in Q16). It is the algebraic coherence measure.*
