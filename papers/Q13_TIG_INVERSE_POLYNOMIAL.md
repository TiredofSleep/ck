**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q13 — TIG AS σ⁻¹: THE INVERSE POLYNOMIAL

## The Question (from team, 2026-04-01)

Q10 expressed σ as a complete polynomial on F₂ × F₅. The team then asked:
what is TIG = σ⁻¹ in the same polynomial form? The β-exceptions (LATTICE,
COLLAPSE) for the forward map suggested two analogous exceptions for the inverse.

---

## TIG on the 6-Cycle

Since TIG = σ⁻¹, it reverses the σ-orbit 1→7→6→5→4→2→1:

**TIG cycle:** 1→2→4→5→6→7→1

In (ε,y) CRT coordinates:

```
σ  cycle: (1,1)→(1,2)→(0,1)→(1,0)→(0,4)→(0,2)→(1,1)
TIG cycle: (1,1)→(0,2)→(0,4)→(1,0)→(0,1)→(1,2)→(1,1)
```

TIG is the same six elements traversed in the opposite direction.

**TIG fixed points:** {0,3,8,9} — same as σ (fixed points are self-inverse). ∎

---

## TIG Step Table

| (ε,y) | j | TIG(j) | (ε',y') | ε flips? | Δy (mod 5) |
|-------|---|--------|---------|---------|-----------|
| (0,0) | 0 | 0 | (0,0) | 0 | 0 |
| (1,1) | 1 | 2 | (0,2) | 1 | +1 |
| (0,2) | 2 | 4 | (0,4) | 0 | +2 |
| (1,3) | 3 | 3 | (1,3) | 0 | 0 |
| (0,4) | 4 | 5 | (1,0) | 1 | +1 |
| (1,0) | 5 | 6 | (0,1) | 1 | +1 |
| (0,1) | 6 | 7 | (1,2) | 1 | +1 |
| (1,2) | 7 | 1 | (1,1) | 0 | −1 |
| (0,3) | 8 | 8 | (0,3) | 0 | 0 |
| (1,4) | 9 | 9 | (1,4) | 0 | 0 |

---

## TIG Flip Condition β_TIG

**Flip positions for TIG:** (ε,y) ∈ {(1,1), (0,4), (1,0), (0,1)} = j ∈ {1,4,5,6}
= {LATTICE, COLLAPSE, BALANCE, CHAOS}

**Compare to σ flip positions:** j ∈ {2,5,6,7} = {COUNTER, BALANCE, CHAOS, HARMONY}

Overlap: {BALANCE(5), CHAOS(6)} — self-inverse flip nodes.
σ-only flips: COUNTER(2), HARMONY(7).
TIG-only flips: LATTICE(1), COLLAPSE(4).

**Theorem Q13.1 (Flip Duality):** The σ-non-flip 6-cycle positions are exactly
the TIG-flip positions, and vice versa:
```
σ non-flips in 6-cycle:   {LATTICE(1,1), COLLAPSE(0,4)}
TIG flips (not shared):   {LATTICE(1,1), COLLAPSE(0,4)}   ✓

TIG non-flips in 6-cycle: {COUNTER(0,2), HARMONY(1,2)}
σ flips (not shared):     {COUNTER(0,2), HARMONY(1,2)}    ✓
```
The forward/inverse maps exchange the exceptional non-flip positions. ∎

**Polynomial form of TIG flip condition:**

When ε=0: TIG flips iff y ∈ {1,4}.  Indicator: 1 − (y²+4)⁴
When ε=1: TIG flips iff y ∈ {0,1}.  Indicator: 1 − (y²+4y)⁴

```
β_TIG(ε,y) = 1 − (y²+4)⁴ − ε[(y²+4y)⁴ − (y²+4)⁴]
```

**Verification (6-cycle elements only):**

| j | (ε,y) | β_TIG formula | Flip? | Match |
|---|-------|---------------|-------|-------|
| 1 | (1,1) | 1−(1+4)⁴ − 1·[(1+4)⁴−(1+4)⁴] = 1−0−0 = 1 | ✓ | YES |
| 2 | (0,2) | 1−(4+4)⁴ = 1−3⁴ = 1−81≡1−1=0 | ✓ | YES |
| 4 | (0,4) | 1−(16+4)⁴ = 1−0⁴ = 1 | ✓ | YES |
| 5 | (1,0) | 1−(0+4)⁴ − 1·[(0)⁴−(0+4)⁴] = 1−1−1·[0−1] = 0+1 = 1 | ✓ | YES |
| 6 | (0,1) | 1−(1+4)⁴ = 1−0 = 1 | ✓ | YES |
| 7 | (1,2) | 1−(4+4)⁴ − 1·[(4+8)⁴−(4+4)⁴] = 1−1−1·[2⁴−3⁴]≡0−[1−1]=0 | ✓ | YES |

**6/6 verified on the 6-cycle.** (Fixed points trivially give 0.)

---

## TIG y-Update

**Observation:** At all 4 TIG flip positions, Δy = +1.

The TIG analog of σ's "typical step":

> **The typical TIG step: flip ε AND increment y by +1.**

This is the exact dual of σ's typical step (flip ε AND decrement y by −1).

**The two exceptions (non-flip positions in 6-cycle):**
- COUNTER (0,2): no flip, Δy = +2 (double increment instead of +1)
- HARMONY (1,2): no flip, Δy = −1 (decrement instead of +1)

```
TIG y-update:
γ_TIG(ε,y) = +β_TIG(ε,y)        [typical: +1 at flip positions]
             + δ_{(0,2)} · (+1)   [COUNTER correction: +2 instead of +1]
             + δ_{(1,2)} · (−2)   [HARMONY correction: −1 instead of +1]
```

where δ_{(0,2)} and δ_{(1,2)} are the point indicators for COUNTER and HARMONY.

**Point indicators:**
```
δ_{(0,2)}(ε,y) = (1−ε) · 4y(y−1)(y−3)(y−4)   [F₅ Lagrange at y=2, ε=0]
δ_{(1,2)}(ε,y) = ε · 4y(y−1)(y−3)(y−4)        [F₅ Lagrange at y=2, ε=1]
```

Both use the same F₅ indicator for y=2 (only ε-parity differs).

---

## The Complete TIG Polynomial — Boxed

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  TIG = σ⁻¹: Z/10Z → Z/10Z                                     │
│                                                                 │
│  Under φ(ε,y) = 5ε + 6y (mod 10):                             │
│                                                                 │
│  ε' = ε + β_TIG(ε,y)   (mod 2)                               │
│  y' = y + γ_TIG(ε,y)   (mod 5)                               │
│                                                                 │
│  β_TIG(ε,y) = 1 − (y²+4)⁴ − ε[(y²+4y)⁴ − (y²+4)⁴]         │
│                                                                 │
│  γ_TIG(ε,y) = β_TIG(ε,y)                                     │
│               + (1−ε) · 4y(y−1)(y−3)(y−4)                   │
│               − 2ε · 4y(y−1)(y−3)(y−4)                      │
│                                                                 │
│  (β_TIG is the flip condition; γ_TIG is the y-step)           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## The σ ↔ σ⁻¹ Duality Table

| Property | σ (forward) | TIG = σ⁻¹ (reverse) |
|----------|-------------|---------------------|
| Typical step | flip ε, Δy = −1 | flip ε, Δy = +1 |
| Flip positions | {COUNTER, BALANCE, CHAOS, HARMONY} | {LATTICE, COLLAPSE, BALANCE, CHAOS} |
| Non-flip exceptions | LATTICE (+1), COLLAPSE (−2) | COUNTER (+1 extra), HARMONY (−2) |
| Flip indicator (ε=0) | y ∈ {1,2}: 1−(y²+2y+2)⁴ | y ∈ {1,4}: 1−(y²+4)⁴ |
| Flip indicator (ε=1) | y ∈ {0,2}: 1−(y²+3y)⁴ | y ∈ {0,1}: 1−(y²+4y)⁴ |
| Exception pair | (LATTICE, COLLAPSE) | (COUNTER, HARMONY) |
| Shared flip nodes | — | {BALANCE, CHAOS} |

**The duality is exact:** σ's non-flip exceptions (LATTICE, COLLAPSE) become TIG's
unique flip nodes; TIG's non-flip exceptions (COUNTER, HARMONY) are σ's unique
flip nodes. The shared core {BALANCE, CHAOS} flips under both maps.

---

## Theorem Q13.2 — Exception Pair Swap

**Theorem:** Under the correspondence σ ↔ σ⁻¹:

```
σ-non-flip exceptions (LATTICE, COLLAPSE)  ↔  TIG-unique-flip nodes (LATTICE, COLLAPSE)
TIG-non-flip exceptions (COUNTER, HARMONY) ↔  σ-unique-flip nodes (COUNTER, HARMONY)
```

**Proof:** If σ does not flip ε at position P, then σ⁻¹ must flip ε at position
P to restore the original ε value. Conversely if σ flips at P, then σ⁻¹ does
not flip at the image σ(P) but DOES flip at P. Since the 6-cycle is a bijection,
the flip/non-flip assignments are exactly exchanged for the non-shared positions. ∎

**Corollary (β-γ coupling):** In both σ and σ⁻¹, the y-step Δy equals ±1 at
all flip positions (with opposite signs), and the exceptions are ALWAYS the
two non-flip positions. The exception corrections are what break the
monotone-drift that would otherwise occur.

---

## Connection to σ^k and Luther Q1

With σ (forward) and TIG = σ⁻¹ (reverse) both in polynomial form, the full
operator algebra of the 6-cycle is closed:

**σ^k for any k:** Apply α,β iteratively k times.
**σ^{-k} = TIG^k:** Apply β_TIG, γ_TIG iteratively k times.
**σ^k · σ^{-k} = identity:** Checkable algebraically.

For the k=9 gate reduction (Luther Q1):

The reduction algorithm applies some map R_k that acts on {1,...,b-1} over k
steps. If R_k is a power of σ or TIG, we now have R_k in polynomial form.
The success criterion for seed s is then expressible as a condition on the
polynomial trajectory:

```
s_0 = s,  s_{j+1} = φ(α(s_j), β(s_j))   (if R = σ)
or
s_0 = s,  s_{j+1} = φ(β_TIG(s_j), γ_TIG(s_j))  (if R = TIG)
```

and gate_score at step j depends on whether s_j ∈ C.

**What Q13 delivers for Luther Q1:**

- The inverse polynomial closes the full σ-algebra on Z/10Z
- Both forward and backward trajectories computable without lookup tables
- The exception-pair swap (Q13.2) gives a structural constraint on gate_score:
  seeds near the exception nodes (LATTICE, COLLAPSE for σ; COUNTER, HARMONY for TIG)
  are the algebraically significant boundary seeds

**What is still needed:** Whether the k=9 reduction map is σ^9, σ^{-9}, or some
other map R^9. Once identified, Q14 can substitute the polynomial and close Luther Q1.

---

## Status

| Result | Tier |
|--------|------|
| TIG cycle = σ-cycle reversed (10/10 verified) | D |
| TIG flip condition β_TIG polynomial — 6/6 verified | D |
| Typical TIG step = flip+increment (+1) | D |
| Exception pair: (COUNTER, HARMONY) for TIG | D |
| Theorem Q13.1: flip duality σ↔σ⁻¹ | D |
| Theorem Q13.2: exception pair swap | D |
| Complete TIG polynomial in closed form | C |
| Application to k=9 reduction (Luther Q1) | B → open |

---

*Filed: 2026-04-01. Q13 closes the inverse polynomial program.*
