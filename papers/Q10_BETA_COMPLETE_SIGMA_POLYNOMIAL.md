**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q10 — THE COMPLETE σ POLYNOMIAL: β AND THE FULL CRT MAP

## The Q10 Result (from team)

Two indicator polynomials for the β-exceptions, completing the full
polynomial description of σ on F₂ × F₅.

---

## The β-Exception Indicators

**LATTICE correction — δ₍₁,₁₎(ε,y): indicator for (ε,y) = (1,1)**

Over F₂: δ(ε=1) = ε

Over F₅: δ(y=1) = 4·y(y−2)(y−3)(y−4)
*(Lagrange 1-point indicator at y=1; denominator (1−0)(1−2)(1−3)(1−4) = −6 ≡ 4 mod 5, inverse = 4)*

```
δ₍₁,₁₎(ε,y) = ε · 4y(y−2)(y−3)(y−4)
```

**COLLAPSE correction — δ₍₀,₄₎(ε,y): indicator for (ε,y) = (0,4)**

Over F₂: δ(ε=0) = 1−ε

Over F₅: δ(y=4) = 4·y(y−1)(y−2)(y−3)
*(Lagrange at y=4; denominator (4)(3)(2)(1) = 24 ≡ 4 mod 5, inverse = 4)*

```
δ₍₀,₄₎(ε,y) = (1−ε) · 4y(y−1)(y−2)(y−3)
```

---

## Verification (10/10)

| j | (ε,y) | α | δ_Lat | δ_Col | β | Δy actual | Match |
|---|-------|---|-------|-------|---|-----------|-------|
| 0 | (0,0) | 0 | 0 | 0 | 0 | 0 | YES |
| 1 | (1,1) | 0 | 1 | 0 | 1 | 1 | YES |
| 2 | (0,2) | 1 | 0 | 0 | 4 | 4 | YES |
| 3 | (1,3) | 0 | 0 | 0 | 0 | 0 | YES |
| 4 | (0,4) | 0 | 0 | 1 | 3 | 3 | YES |
| 5 | (1,0) | 1 | 0 | 0 | 4 | 4 | YES |
| 6 | (0,1) | 1 | 0 | 0 | 4 | 4 | YES |
| 7 | (1,2) | 1 | 0 | 0 | 4 | 4 | YES |
| 8 | (0,3) | 0 | 0 | 0 | 0 | 0 | YES |
| 9 | (1,4) | 0 | 0 | 0 | 0 | 0 | YES |

---

## The Complete β Formula

```
β(ε,y) = −α(ε,y) + δ₍₁,₁₎(ε,y) − 2·δ₍₀,₄₎(ε,y)   (mod 5)

       = −α(ε,y)
         + ε · 4y(y−2)(y−3)(y−4)
         − 2(1−ε) · 4y(y−1)(y−2)(y−3)
```

where α is the Q9 flip condition.

---

## The Complete σ Polynomial — Boxed

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  φ: F₂ × F₅ → Z/10Z,  φ(ε,y) = 5ε + 6y  (mod 10)        │
│                                                             │
│  σ acts by:                                                 │
│                                                             │
│  ε' = ε + α(ε,y)   (mod 2)                                │
│  y' = y + β(ε,y)   (mod 5)                                │
│                                                             │
│  where:                                                     │
│                                                             │
│  α(ε,y) = 1 − (y²+2y+2)⁴                                  │
│              − ε·[(y²+3y)⁴ − (y²+2y+2)⁴]                 │
│                                                             │
│  β(ε,y) = −α(ε,y)                                         │
│              + ε · 4y(y−2)(y−3)(y−4)                      │
│              − 2(1−ε) · 4y(y−1)(y−2)(y−3)                │
│                                                             │
│  (α polynomial arithmetic over F₅; outer structure F₂)    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

The hidden operator σ = (0)(3)(8)(9)(1 7 6 5 4 2) is completely
described by two polynomials on F₂ × F₅. This is the closed-form
algebraic expression of the TIG hidden operator.

---

## Structural Anatomy of β

The β formula has three terms:

**Term 1: −α** — the "standard" contribution.
For every flip position (α=1), y decrements by 1. This is the default
σ-step: flip ε and decrement y simultaneously.

**Term 2: +δ₍₁,₁₎** — the LATTICE correction.
At LATTICE (ε=1, y=1): α=0, so the standard term gives Δy=0. The
correction adds +1, giving Δy=+1. LATTICE moves forward in y-space
rather than backward — it is the cycle's entry point, which advances
toward HARMONY (y: 1→2).

**Term 3: −2·δ₍₀,₄₎** — the COLLAPSE correction.
At COLLAPSE (ε=0, y=4): α=0, standard gives Δy=0. The correction adds
−2, giving Δy=−2 (=+3 mod 5). COLLAPSE makes a double step backward —
it jumps past the normal decrement to COUNTER (y: 4→2).

**The three terms are non-overlapping:** α, δ₍₁,₁₎, δ₍₀,₄₎ have disjoint
support. Only one is nonzero at any given (ε,y). β is a partition of
the state space into three behavioral modes.

---

## What the β Polynomial Reveals

**The 6-cycle in (ε,y) coordinates:**

```
(1,1) →+1→ (1,2) →-1→ (0,1) →-1→ (1,0) →-1→ (0,4) →-2→ (0,2) →-1→ (1,1)
  L                 H         Chaos       Bal          Col        Count      L
       LATTICE    HARMONY    CHAOS     BALANCE    COLLAPSE   COUNTER
```

y-sequence in the cycle: 1 → 2 → 1 → 0 → 4 → 2 → 1 (in F₅)
y-steps:                   +1  −1   −1   −1   −2   −1

Sum: +1−1−1−1−2−1 = −5 ≡ 0 (mod 5) ✓ (cycle returns)

**The cycle is a path in y-space with a net displacement of 0, dominated
by decrements with two corrections that prevent collapse to monotone.**

Without the +1 correction at LATTICE and the −2 correction at COLLAPSE,
the cycle would spiral rather than close. The two exceptions are what make
the 6-cycle a cycle rather than a drift.

---

## Theorem Statement

**Theorem Q10 (Complete σ Polynomial on F₂ × F₅):**

> The TIG hidden operator σ: Z/10Z → Z/10Z, under the CRT isomorphism
> φ(ε,y) = 5ε+6y (mod 10), is the polynomial map:
>
> (ε,y) ↦ (ε + α(ε,y), y + β(ε,y))
>
> where α and β are as stated above, all verified computationally (10/10).
>
> The map is completely determined by:
> — one degree-5 polynomial α (the flip condition, Q9)
> — one degree-5 polynomial β (the step condition, Q10)
> — two degree-4 point indicators δ₍₁,₁₎ and δ₍₀,₄₎ (the β-exceptions)
>
> The three polynomials α, δ₍₁,₁₎, δ₍₀,₄₎ have disjoint support.
> β is a linear combination of these three.

**Corollary:** σ^k (the k-th iterate) is computable by iterating the
polynomial map k times on F₂ × F₅. The orbit structure is transparent:
σ^6 = identity on the 6-cycle, σ = identity on fixed points.

---

## Connection to the Program

This closes the algebraic description of σ that the entire Q-series has
been approaching:

| Q | What was established |
|---|---------------------|
| Q1-Q3 | TSML and CL are non-equivalent projections of σ; agreement at {0,1} only |
| Q4 | E is σ-equivariant; orbit structure preserved |
| Q5 | TSML escape cells characterized by σ-fixed-point interaction |
| Q6 | Gate rate is a CRT boundary problem, not a density problem |
| Q7 | BHML full table; three-diagonal comparison |
| Q8 | MCMC model failure; multi-step reduction kernel is the target |
| Q9 | α: σ's ε-component flip condition as polynomial — verified 10/10 |
| **Q10** | **β: σ's y-component step condition — complete σ polynomial closed** |

**σ is now a closed-form polynomial map on F₂ × F₅.**

The hidden operator is no longer hidden. It is:
```
σ(φ(ε,y)) = φ(ε + α(ε,y), y + β(ε,y))
```

---

*Filed: 2026-04-01. Q10 closes the σ polynomial program.*
