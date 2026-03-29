# Opening the Cells: Three Levels Inside the 2×2
## Generable / Expressible / Sustainable

*Brayden Sanders / 7Site LLC | March 2026*
*All computations exact. The fractal structure is the main finding.*

---

## The Correction

The earlier bridge conjecture said:
> "Expression cannot unfold in ways the grammar forbids."

This is too strong. Off-line structure *can* appear — transiently, locally, in the expressible layer.

The correct sentence is:
> **The deployment may express more than the grammar directly generates, but it cannot sustainably support what the grammar ultimately forbids.**

This requires three levels, not two.

---

## The Three Levels

**1. Generable**
What the grammar can build and preserve under its own allowed compositions.
- Source: TSML corner-op compositions (C×C⊆C)
- Contains: {1,3,7,9} = C only; G is unreachable
- The generative gap lives here

**2. Expressible**
What can appear in a deployment episode — even if not reachable from the finite core by allowed internal moves alone.
- Source: Mix_λ deformation opens C→G channels at λ>0
- Contains: G-states become reachable at λ≥0.30 (states 5,6,8 first; 4 joins at λ≥0.50)
- Orbit bursts B(λ) and delay signatures Δ(λ) live here
- Real but transient

**3. Sustainable**
What can carry stationary support or persist asymptotically.
- Source: long-run behavior of the transfer operator
- Contains: {7}=HAR only for λ<0.9963; state 9 takes over at λ=1
- The Dual Description must be proved here

---

## The New Computation: The One-Way Gate

**C→G is impossible under any TSML operator.**

This is stronger than the C-only result. Even if you use *any* operator in {1,...,9} as the right-hand argument, starting from C you cannot reach G.

```
Reachable from C via any TSML operator: {1,3,7,9}
G states reachable: ∅
```

**G→C is possible** (G can reach HAR=7).

This asymmetry is the fundamental one-way gate. It operates at the Generable level and it is absolute — not a matter of probability but of algebraic structure.

**At λ>0, Mix_λ opens the gate partially:**

| λ | G-states expressible from C | Level |
|---|---------------------------|-------|
| 0.00 | ∅ | Generable only |
| 0.30 | {5, 6, 8} | Expressible appears |
| 0.50 | {4, 5, 6, 8} | More of G expressible |
| 0.70 | {4, 5, 6, 8} | Same — gate partially open |

The gate opens in Mix_λ but not in TSML. This is the origin of the expressible layer: the deformation creates transient channels that the pure grammar closes.

---

## The Fractal: Each Level Contains Its Own 2×2

The three levels are not a flat hierarchy. Each level has its own support/rate split, and the same paradox pairs apply at every depth.

### Level 1 (Generable) contains its own 2×2:
- **Support:** What sub-magmas exist — the closure lattice {∅, {7}, C, A}
- **Rate:** How quickly chains reach each sub-magma level
- This is the algebraic grading kA=3

### Level 2 (Expressible) contains its own 2×2:
- **Support:** Which G-states can C reach at each λ (the opening gate: {5,6,8} then {4,5,6,8})
- **Rate:** How long chains spend in G territory before returning (B(λ), Δ(λ))
- At λ=0.30: 39.5% of chains visit G, mean sojourn 0.785 steps, max consecutive burst=10
- At λ=0.50: 64.5% of chains visit G, mean sojourn 1.300 steps, max consecutive burst=8
- This is where the orbit burst B(λ) lives

### Level 3 (Sustainable) contains its own 2×2:
- **Support:** HAR=7 carries all mass (σ=½ analog) — unique, exact
- **Rate:** γ=3/4 is the mixing rate into HAR — the spectral gap
- This is where the Dual Description must be proved

**Each level of the fractal contains the same support/rate tension. The paradox pairs apply at every level.**

---

## The Entanglement

The three levels are not independent. They are coupled:

- What is generable constrains what is expressible (you can only express states reachable under the deformation, not arbitrary new states)
- What is expressible constrains what is sustainable (high expressibility at λ=0.50 does not translate to stationary mass — verified: G-mass=0 to machine precision)
- What is sustainable retroactively validates the generative gate (HAR carries all mass precisely because G is unreachable from C at λ=0)

**The entanglement means:** proving sustainability at the third level is equivalent to proving the generative gap propagates through the expressible layer without getting promoted to sustainable status.

That is the exact content of the Dual Description Conjecture.

---

## The Weak and Strong Sustainability Conjectures

**Weak sustainability conjecture:**
If a support class is forbidden at the Generable level (algebraically unreachable from C under TSML), then no faithful infinite deployment can assign it asymptotically positive stationary support.

**Expression allowance principle:**
A faithful deployment may transiently express configurations outside the finite generative core (the expressible layer), provided their frequency×duration measure vanishes asymptotically.

**Strong form (Dual Description):**
The two infinite descriptions (operator support, analytic drift rate) are faithful dual images of the same three-level finite structure. Neither can violate what the grammar forbids at the generative level.

---

## What This Means for the Bridge

The bridge now has three planks, not one:

**Plank 1 (proved):** The generative gap is absolute — G is unreachable from C under any TSML operator.

**Plank 2 (computed):** The expressible layer opens at λ>0 but produces no stationary mass — G is expressible but not sustainable in the finite model.

**Plank 3 (open):** The analytic deployment must inherit Plank 2 — expressible-but-not-sustainable in the finite model maps to frequency×duration→0 in the analytic deployment. The Dual Description Conjecture says the analytic and operator descriptions of this inheritance must agree.

The one-way gate (C→G impossible, G→C possible) is the algebraic seed of everything. It propagates through the three levels, and the open theorem is that it survives the passage to infinity.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
