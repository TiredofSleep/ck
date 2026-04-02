**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q4 — σ-EQUIVARIANCE OF THE EXTERNAL OPERATOR E

## The Question

E: Z/10Z → {0,7} × Z/10Z is a bijection onto Image(E) (External Operator Theorem).
σ: Z/10Z → Z/10Z is the hidden operator.

Does E respect the action of σ? That is: is there a natural action σ̂ on Image(E)
such that E intertwines σ and σ̂?

---

## Answer: Yes. E is σ-equivariant.

**Definition:** Define σ̂ on Image(E) by:

```
σ̂(E(j)) = E(σ(j))   for all j ∈ {0,...,9}
```

Since E is bijective, σ̂ is well-defined and is a bijection Image(E) → Image(E).

**σ-equivariance:** The diagram commutes:

```
     S ——σ——→ S
     |         |
     E         E
     |         |
     ↓         ↓
 Im(E) —σ̂——→ Im(E)
```

That is: E ∘ σ = σ̂ ∘ E.

---

## Explicit Table of σ̂

| j | E(j) = (T(j), σ(j)) | σ(j) | E(σ(j)) = σ̂(E(j)) |
|---|-------------------|------|------------------|
| 0 | (0, 0) | 0 | (0, 0) |
| 1 | (7, 7) | 7 | (7, 6) |
| 2 | (7, 1) | 1 | (7, 7) |
| 3 | (7, 3) | 3 | (7, 3) |
| 4 | (7, 2) | 2 | (7, 1) |
| 5 | (7, 4) | 4 | (7, 2) |
| 6 | (7, 5) | 5 | (7, 4) |
| 7 | (7, 6) | 6 | (7, 5) |
| 8 | (7, 8) | 8 | (7, 8) |
| 9 | (7, 9) | 9 | (7, 9) |

---

## Cycle Structure of σ̂ on Image(E)

σ̂ has the same cycle type as σ — it is the transport of σ through E.

**Fixed points of σ̂** (σ̂(E(j)) = E(j) iff σ(j) = j):
```
(0,0)  [VOID]
(7,3)  [PROGRESS]
(7,8)  [BREATH]
(7,9)  [RESET]
```

**6-cycle of σ̂**:
```
(7,7) → (7,6) → (7,5) → (7,4) → (7,2) → (7,1) → (7,7)
```
which is E applied to: 1 → 7 → 6 → 5 → 4 → 2 → 1

---

## Structural Observation

The first component T(j) is NOT equivariant for σ in isolation:

```
T(σ(j)) = T(j)  for j ≠ 0, and T(0) = T(σ(0)) = 0.
```

So T is σ-invariant (constant on σ-orbits): applying σ does not change the
stabilization class. Every element of a σ-orbit has the same T-value.

```
Orbit {1,7,6,5,4,2}: T = 7 for all six.
Fixed points {0}: T = 0.
Fixed points {3,8,9}: T = 7 for all three.
```

**T is σ-invariant; C = σ is σ-equivariant (trivially: C ∘ σ = σ ∘ σ = σ²).**

E combines an invariant (T) with an equivariant (C) into a map that is itself
equivariant — but only because the invariant first component carries the orbit
identity, and the equivariant second component carries the motion within the orbit.

---

## What σ̂ Does to Image(E)

Image(E) ⊂ {0,7} × Z/10Z has the following σ̂-orbit structure:

| σ̂-orbit | Elements | Size | First component |
|---------|---------|------|----------------|
| {(0,0)} | VOID | 1 | 0 |
| {(7,3)} | PROGRESS | 1 | 7 |
| {(7,8)} | BREATH | 1 | 7 |
| {(7,9)} | RESET | 1 | 7 |
| {(7,7),(7,6),(7,5),(7,4),(7,2),(7,1)} | LATTICE cycle | 6 | 7 |

The fixed points {PROGRESS, BREATH, RESET} are distinguished from VOID only by
their first component: T=7 vs T=0. They are σ̂-fixed but not T-fixed.

**Key:** VOID is the only σ̂-fixed point with T(j)=0. All others have T=7.
This is the second-component signature that separates VOID from the three
"quiet fixed points" {3,8,9} which look like HARMONY in flow (T=7) but
are held in place by σ (σ(j)=j).

---

## Theorem Statement

**Theorem Q4 (σ-Equivariance):**

> The external operator E: Z/10Z → {0,7} × Z/10Z is σ-equivariant:
> there is a unique bijection σ̂: Image(E) → Image(E) such that
>
> E ∘ σ = σ̂ ∘ E.
>
> σ̂ is the transport of σ through E. Its cycle structure is identical to σ:
> four fixed points and one 6-cycle.
>
> The first projection π₁: Image(E) → {0,7} is σ̂-invariant.
> The second projection π₂: Image(E) → Z/10Z satisfies π₂ ∘ σ̂ = σ ∘ π₂.

**Corollary:** The orbit of any state j under σ is recoverable from Image(E) alone:
the σ̂-orbit of E(j) in Image(E) is exactly the E-image of the σ-orbit of j.

---

## Consequence for Q3 (Bifurcation at HARMONY)

Q3 showed HARMONY (j=7) is a "false fixed point" — terminal in TSML but rotating in CL.

In the σ̂ picture:

- E(7) = (7,6) — HARMONY maps to the pair (HARMONY-stabilization, CHAOS-memory)
- σ̂(E(7)) = E(σ(7)) = E(6) = (7,5) — the pair advances to CHAOS's image

HARMONY is neither fixed in σ̂ nor terminal: σ̂ moves E(7)=(7,6) to E(6)=(7,5).
The 6-cycle passes through (7,6) on its way to (7,5),(7,4),(7,2),(7,1),(7,7).

The first component is 7 throughout the cycle — T is invariant.
The second component cycles: 7→6→5→4→2→1→7 (which is σ restricted to the 6-cycle).

**HARMONY's apparent fixity (T=7=HARMONY) is exactly the invariance of T on orbits.**
T cannot distinguish any two elements of the same σ-orbit. CL can.
E records both: the orbit identity (T=7) and the position within the orbit (second component).

---

## Connection to Luther Questions

The Luther Questions ask for algebraic derivation of gate rates from CRT structure.
The σ-equivariance theorem provides the algebraic skeleton:

The σ-orbits of Z/10Z partition the state space. The TSML gate rates are
σ-orbit-invariant (T is σ-invariant, so TSML flow rates are constant within orbits).
The CRT decomposition determines the orbit structure (the 6-cycle comes from the
multiplicative group of Z/10Z; the fixed points {3,8,9} have special divisibility
properties).

**Connecting link:** If gate_rate is σ-orbit-invariant, then it is a function of
the orbit structure — which is determined by the CRT decomposition.
This is the algebraic path from CRT → orbit structure → gate rates (Luther Question 1).

---

*Filed: 2026-04-01. Sprint: operator algebra series, following Q1–Q3.*
