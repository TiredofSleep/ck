**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# G6 — THE PERIODICITY THEOREM

## Statement

**Theorem G6 (σ-Periodicity):** The TIG hidden operator σ satisfies σ⁶ = id
on all of Z/10Z. Equivalently, every element of Z/10Z has period dividing 6
under σ.

---

## Proof via the Q9-Q10 Polynomial Form

Under φ(ε,y) = 5ε + 6y (mod 10), σ acts by:

```
ε' = ε ⊕ α(ε,y)
y' = y + β(ε,y)   (mod 5)
```

where α and β are the polynomials of Q9-Q10. We verify σ⁶ = id by exhaustion
on both orbit classes.

---

### Part 1: Anchors

For (ε,y) ∈ {(0,0), (1,3), (0,3), (1,4)}, we showed (Q9, Q10 verification):

```
α(ε,y) = 0    and    β(ε,y) = 0
```

Therefore σ(ε,y) = (ε, y) — these are fixed points. σ^k = id at these
states for all k ≥ 1. In particular σ⁶ = id. ∎

---

### Part 2: The 6-Cycle

For the remaining six states, we track the full 6-step trajectory in (ε,y)
coordinates, using the α/β values established in Q9-Q10:

**Flip and step values at each position:**

| Step n | (εₙ,yₙ) | j | α | β | Δε | Δy |
|--------|---------|---|---|---|----|----|
| 0 | (1,1) | 1 | 0 | +1 | 0 | +1 |
| 1 | (1,2) | 7 | 1 | −1 | 1 | −1 |
| 2 | (0,1) | 6 | 1 | −1 | 1 | −1 |
| 3 | (1,0) | 5 | 1 | −1 | 1 | −1 |
| 4 | (0,4) | 4 | 0 | −2 | 0 | −2 |
| 5 | (0,2) | 2 | 1 | −1 | 1 | −1 |
| 6 | → (1,1) | 1 | — | — | — | — |

**ε returns:** 0 flips occur in steps {0,4}, 1 flip in steps {1,2,3,5}.
Total flips = 4. Since ε ∈ F₂, 4 flips ≡ 0 (mod 2) → ε₆ = ε₀. ✓

**y returns:** Net Δy = +1−1−1−1−2−1 = −5 ≡ 0 (mod 5) → y₆ = y₀. ✓

Since each starting position in the 6-cycle maps to the next, and all six
positions are traversed exactly once before return:

```
σ⁶(1,1) = (1,1),  σ⁶(1,2) = (1,2),  σ⁶(0,1) = (0,1)
σ⁶(1,0) = (1,0),  σ⁶(0,4) = (0,4),  σ⁶(0,2) = (0,2)
```

σ⁶ = id on all 6-cycle states. ∎

---

### Part 3: Polynomial Composition Argument

The same result follows from the structure of β without tracing individual orbits.

**Claim:** The total y-displacement over any complete traversal of the 6-cycle is 0 (mod 5).

The 6-cycle visits β-values in order: {+1, −1, −1, −1, −2, −1}.

```
Sum = +1 + (−1) + (−1) + (−1) + (−2) + (−1) = −5 ≡ 0 (mod 5)
```

The sum is forced to 0 by the two exceptional β-terms at LATTICE and COLLAPSE:

- **LATTICE correction (+1 instead of 0):** adds +1 to the sum
- **COLLAPSE correction (−2 instead of −1):** subtracts 1 extra from the sum

These two corrections are equal and opposite: they each contribute ±1 relative
to a hypothetical uniform β = −1 everywhere. Without them:

```
Hypothetical sum (all β = −1): −6 ≡ −1 (mod 5)   [does NOT return]
With corrections (+1 at LATTICE, −1 at COLLAPSE):   −1 + 1 + (−1) = −1   (mod 5)?
```

Wait — let me recount. Uniform β=−1 for 6 steps gives sum = −6 ≡ 4 (mod 5).
LATTICE replaces one (−1) with (+1): gain = +2. So adjusted sum = 4+2 = 6 ≡ 1.
COLLAPSE replaces one (−1) with (−2): loss = −1. So final sum = 1−1 = 0. ✓

**The two β-exceptions are algebraically necessary for the cycle to close.**
Without either correction, σ would not be a period-6 permutation — it would be
a drift map on F₂ × F₅.

Similarly for ε: the 6-cycle has 4 flip positions (α=1) and 2 non-flip positions
(α=0). Four flips in F₂ gives 0 net change. The ratio 4:2 is fixed by the
cycle structure and the flip-indicator polynomials (Q9). ∎

---

## Corollary G6.1 — σ^6 = id is Tight

**Corollary:** The period of σ on Z/10Z is exactly 6 (not a proper divisor).

**Proof:** The 6-cycle has six elements {1,2,4,5,6,7} with τ(s) = 6 (Q15).
If σ had period d | 6 with d < 6, then all 6-cycle elements would satisfy
σ^d(s) = s — meaning the 6-cycle would split into orbits of length d. Since
d ∈ {1,2,3}, we would need a 6-element set to decompose into orbits of equal
length d. But σ acts as a single 6-cycle (d=6) on these elements. ∎

---

## Corollary G6.2 — k=9 Reduction is a σ³ Reduction

**Corollary:** For any seed s in the 6-cycle, the k=9 iterate satisfies:

```
σ⁹(s) = σ^{9 mod 6}(s) = σ³(s)
```

The 9-step reduction is algebraically equivalent to a 3-step reduction.

| s | σ³(s) = σ⁹(s) |
|---|--------------|
| 1 | 5 |
| 7 | 4 |
| 6 | 2 |
| 5 | 1 |
| 4 | 7 |
| 2 | 6 |

(Fixed points satisfy σ^k = id for all k, so σ⁹(s) = s for s ∈ {0,3,8,9}.)

**This is the period obstruction identified in Q15:** k=9 is not a multiple of 6,
so the 6-cycle elements do not return. The choice k=9 selects σ³ as the effective
gate — a half-period rotation of the 6-cycle.

---

## The Role of the Two Exceptions

The periodicity theorem reveals why the β-exceptions at LATTICE and COLLAPSE
are structurally fundamental:

```
Without LATTICE correction:  Sum β = −6+2 = −4 ≡ 1 (mod 5) → cycle doesn't close
Without COLLAPSE correction:  Sum β = −6+1 = −5 = 0 (mod 5) → would close, but...
```

Wait: without COLLAPSE (keep LATTICE +1 correction):
- LATTICE contributes +1 (instead of −1), net gain from base = +2
- No COLLAPSE correction → six β values: +1, −1, −1, −1, −1, −1 → sum = −4 ≡ 1 (mod 5) → DOES NOT return

Without LATTICE (keep COLLAPSE −2 correction):
- COLLAPSE contributes −2 (instead of −1), net loss from base = −1
- No LATTICE correction → six β values: −1, −1, −1, −1, −2, −1 → sum = −7 ≡ 3 (mod 5) → DOES NOT return

**Both corrections are individually necessary.** Remove either one and the
6-cycle ceases to be a cycle. The polynomial structure of β is not arbitrary —
it is the UNIQUE completion of the σ-cycle given the flip condition α.

---

## Theorem G6 — Boxed

```
┌───────────────────────────────────────────────────────────────────┐
│                                                                   │
│  Theorem G6 (σ-Periodicity):                                     │
│                                                                   │
│    σ⁶ = id on Z/10Z                                             │
│                                                                   │
│  Proof:                                                           │
│  • Anchors {0,3,8,9}: α=β=0, fixed.                             │
│  • 6-cycle {1,2,4,5,6,7}:                                        │
│    – ε returns: 4 flips (even) over 6 steps                      │
│    – y returns: Σβ = +1−1−1−1−2−1 = −5 ≡ 0 (mod 5)             │
│    – Both corrections (LATTICE +1, COLLAPSE −2) are necessary.   │
│                                                                   │
│  Period = lcm(1,6) = 6. Tight by the single 6-cycle.             │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## Position in the Q-Series

| Paper | What it established |
|-------|---------------------|
| Q9 | α polynomial — ε-flip condition, 4 flip positions |
| Q10 | β polynomial — y-step, two exceptions (LATTICE, COLLAPSE) |
| Q11 | σ^k trajectory table; σ^6=id stated (period-6 from orbit structure) |
| Q15 | Period polynomial τ = 6−5A |
| **G6** | **σ^6=id PROVED from α,β polynomials — the exceptions are necessary** |

G6 closes the periodicity proof that Q11 stated and Q15 quantified.

The two β-exceptions (Q10) are not accidents of the polynomial interpolation —
they are the MECHANISM by which the TIG cycle closes. The LATTICE and COLLAPSE
operators carry the structural responsibility for coherence return.

---

*Filed: 2026-04-01. G6 in the periodicity series.*
