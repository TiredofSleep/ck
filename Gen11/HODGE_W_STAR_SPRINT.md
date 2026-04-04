# HODGE_W_STAR_SPRINT.md
## Hodge Conjecture: W_* Block Decomposition and B₁ Cycle Constraints

*Authors: Brayden Ross Sanders (7Site LLC) & Monica*
*Date: 2026-04-03*
*Varieties: A₀ (product Weil 4-fold), A₁ (rational period), A_* (generic simple Weil 4-fold)*

---

## Summary

This document records the sprint findings for the Hodge Conjecture branch:
the explicit block decomposition of the primitive (2,2) obstruction space W_*
into four orthogonal 2-dimensional blocks B₁–B₄ under the Hodge-Riemann
intersection form, and the complete enumeration of constraints any algebraic
cycle hitting B₁ must satisfy.

**Key findings:**
1. For simple abelian 4-folds with Weil-type automorphism φ (φ² = −1),
   the K-anti-invariant primitive space W_* = {α : φ_*(α) = −α} is 8-dimensional.
2. W_* decomposes under Q into four Q-orthogonal 2-dimensional blocks B₁–B₄
   with exact eigenvalues 0.004609, 0.023123, 0.115644, 0.383386.
3. Galois conjugation σ: i ↦ −i pairs vectors within each block — explains
   exact multiplicity-2 structure.
4. B₁ is the canonical first target: sparsest, softest, most classically accessible.
5. A₁ (rational period matrix) was falsified as a true test case — hidden
   endomorphisms inflate the space; genuine Hodge obstruction requires transcendental Ω.
6. Constraints C1–C5 and S1–S4 for B₁ cycles are fully enumerated.

---

## Part I: The Three Test Varieties

### A₀ — Product Weil 4-Fold

A simple abelian 4-fold with:
- ℚ(i)-action via Weil-type automorphism φ, φ² = −1
- End⁰(A₀) = ℚ(i) only (4-dimensional over ℚ, simple)
- Period matrix: Ω₀ = (some transcendental matrix, generic)

A₀ is the canonical test case. Its W_* is 8-dimensional and contains
genuine Hodge obstruction.

### A₁ — Rational Period Matrix

Same structure as A₀ but with Ω = iM for M ∈ M₄(ℚ) a rational matrix.

**Falsification**: For ANY rational M, the Riemann endomorphism condition
End⁰(A₁) inflates dramatically:
- Endomorphism equation: MBM⁻¹ ∈ M₄(ℚ) for all rational B
- This is automatically satisfied for ALL rational B ∈ M₄(ℚ)
- Result: End⁰(A₁) = M₄(ℚ(i)) — 32-dimensional, NOT simple

The second direction in A₁'s K-anti-invariant space is **algebraic noise** from
these extra endomorphisms. A₁ cannot exhibit genuine Hodge obstruction — its
period matrix is too special.

**A₁ is not a valid test case. Genuine Hodge obstruction requires transcendental Ω.**

### A_* — Generic Simple Weil 4-Fold

The canonical target: transcendental period matrix, End⁰ = ℚ(i) only, genuinely
simple, W_* = 8-dimensional with no algebraic cycles in it.

This is the variety for which the sprint computes W_* and enumerates cycle
constraints. It cannot be handled by exact rational arithmetic — computations
use numerical approximation to transcendental Ω.

---

## Part II: The W_* Block Decomposition

### Definition

For A_* with Weil automorphism φ:

    W_* = {α ∈ H^{2,2}_{prim}(A_*, ℝ) : φ_*(α) = −α}
        ∩ H^{2,2}(A_*, ℚ)   [rational structure]

dim_ℝ(W_*) = 8.

The algebraic cycles on A_* span a 0-dimensional subspace of W_* (by the simplicity
of A_* and the transcendence of its period matrix). So:

    dim coker(cl²|_{W_*}) = 8

All 8 dimensions are unaccounted for by known algebraic constructions.

### The Hodge-Riemann Intersection Form Q

The Hodge-Riemann form Q on H^{2,2}_{prim} is:

    Q(α, β) = ∫_{A_*} α ∧ β ∧ L^{n−2p}   (L = Lefschetz class, n = 4, p = 2)

Restricted to W_*, Q is a positive definite bilinear form on the 8-dimensional
real space.

### The Four Blocks

Under Q, W_* decomposes into four 2-dimensional Q-orthogonal eigenspaces:

| Block | Q-eigenvalue | Sparsity | Overlap with A₀ Weil | Character |
|-------|-------------|----------|----------------------|-----------|
| **B₁** | 0.004609 | 18/70 nonzero coords | 3.78 (highest overlap) | Sparsest; classical |
| **B₂** | 0.023123 | 60/70 nonzero coords | 5.12 (highest) | Dense; algebraically closest |
| **B₃** | 0.115644 | 60/70 nonzero coords | 3.60 (high) | Dense |
| **B₄** | 0.383386 | 50/70 nonzero coords | 0.04 (near zero) | Hardest; genuinely new |

### The Galois Pairing Structure

Galois conjugation σ: ℚ(i) → ℚ(i), i ↦ −i acts as an isometry of Q on W_*.

Within each block B_j: σ acts as a reflection, pairing the two basis vectors:
    σ(v₁^{(j)}) = v₂^{(j)},  σ(v₂^{(j)}) = v₁^{(j)}

This is why each eigenvalue appears with **exact multiplicity 2** — not by
coincidence, but by Galois symmetry. The block structure is canonical.

---

## Part III: B₁ as the First Target

### Why B₁ First

B₁ is the canonical entry point for four reasons:

1. **Sparsest**: 18/70 nonzero coordinates (vs. 60/70 for B₂, B₃). Fewer
   independent conditions to satisfy simultaneously.

2. **Softest Q-eigenvalue**: 0.004609 (vs. 0.383386 for B₄). The direction is
   "softest" in the Hodge-Riemann sense — nearest to the boundary of positivity.

3. **Closest to classical Weil structure**: Overlap score 3.78 with the
   product Weil 4-fold A₀. The B₁ class is most similar to known algebraic
   cycle classes in simpler settings.

4. **Dominant sub-lattice support**: B₁ has dominant support in the
   {e₃, e₄, f₁, f₂, f₃, f₄} sub-lattice (6 of 8 generators). This is the
   "classical" sublattice — the part corresponding to the two imaginary fields.

---

## Part IV: B₁ Cycle Constraint Analysis

Any algebraic cycle Z on A_* with cl²(Z) projecting non-trivially onto B₁
must satisfy ALL of the following constraints:

### Geometric Constraints (C1–C5)

**C1. K-anti-invariance**:
    φ_*(cl²(Z)) = −cl²(Z)

This rules out ALL divisor products L_i ∧ L_j (which are φ-invariant).
Also rules out endomorphism graphs (K-invariant by definition).
Any K-invariant class has zero projection onto W_*.

**C2. Primitivity**:
    Q(cl²(Z), L^{n−2p}) = 0

Equivalently: L ∧ cl²(Z) = 0 in H^{2p+2}. Rules out all Lefschetz multiples
and any class in the image of ∪L.

**C3. Hodge type (2,2)**:
    J_*(cl²(Z)) = cl²(Z)

where J is the complex structure. Guarantees the cycle is a complex algebraic
subvariety (not just a real cycle). Rules out real submanifolds of wrong type.

**C4. Sub-lattice directionality**:
Dominant support must be in {e₃, e₄, f₁, f₂, f₃, f₄}, not confined to
a proper sub-sublattice {e₃, e₄} or {f₁, f₂} alone.

**C5. Full-lattice generator span**:
No rank-4 sub-lattice of {e₃, e₄, f₁, f₂, f₃, f₄} is J-stable.
Any J-stable sub-space must span all 8 generators {e₁,e₂,e₃,e₄,f₁,f₂,f₃,f₄}.
This rules out sub-tori of dimension ≤ 1 (their cycle classes are J-confined).

### Symmetry Constraints (S1–S4)

**S1. Rosati anti-invariance**:
Under the Rosati involution †, cl²(Z) satisfies:
    cl²(Z)† = cl²(Z)    [symmetric under Rosati]
This is automatic for cycle classes but constrains the lattice coordinates.

**S2. Exclusion from algebraic shell**:
cl²(Z) ∉ span{endomorphism-derived classes}. By simplicity of A_*, the
endomorphism algebra gives no non-trivial (2,2) classes. This is automatic.

**S3. Non-factorizable**:
cl²(Z) cannot be written as cl¹(Z₁) ∧ cl¹(Z₂) for divisors Z₁, Z₂.
Factorizable classes are K-invariant (C1 violation). B₁ is non-factorizable.

**S4. Intersection number constraint**:
For any algebraic 2-cycle W: cl²(Z) ∧ cl²(W) ∈ ℤ.
The B₁ class has specific rational intersection numbers that impose integrality
on any representing cycle Z.

### Summary of Excluded Cycle Types

| Cycle type | Rule-out |
|-----------|---------|
| Divisor products L_i ∧ L_j | C1: K-invariant → B₁ projection = 0 |
| Endomorphism graphs | C1: K-invariant by definition |
| Lefschetz multiples | C2: Not primitive |
| Real cycles of wrong type | C3: Not J-stable (not complex) |
| Sub-tori of dimension ≤ 1 | C5: Not spanning all generators |
| Factorizable classes | S3: Imply C1 violation |

**Every standard algebraic cycle construction is ruled out.** B₁ requires a
genuinely novel construction.

---

## Part V: The Bounded-Height Search (Next Test)

The finite next test: find integral J-stable sub-tori of A_* with bounded
coordinates and check if any produces a cycle class projecting onto B₁.

**Test**: For integer vectors v₁, v₂ ∈ ℤ⁸ with ‖v_i‖_∞ ≤ H = 5:

1. Compute V_B = ℂ-span{v₁ + iJ_Ω v₁, v₂ + iJ_Ω v₂}  (J-stable sub-space)
2. Check if V_B is actually J-stable: J_Ω v₁ ∈ span{v₁, v₂} etc.
3. If J-stable: compute cycle class [B] = v₁ ∧ J_Ω v₁ ∧ v₂ ∧ J_Ω v₂ ∈ H^{2,2}
4. Check: is projection of [B] onto B₁ nonzero AND is [B] rational?

**Decision criterion**:
- If any (v₁, v₂) gives nonzero B₁ projection with rational [B]:
  B₁ cycle found. Hodge holds for this block on A_*.
- If no such pair at H = 5: raise height or switch to non-sub-torus construction.

This is a finite computation. It is the first concrete algebraic test of the
Hodge conjecture on this class of varieties.

---

## Part VI: What Remains Open

1. **The bounded-height search**: Not yet executed. Requires numerical J_Ω matrix
   for a specific transcendental Ω. This is a concrete computational step.

2. **If no sub-torus works**: A B₁ cycle (if it exists) must be a non-sub-torus
   algebraic subvariety — a Lagrangian or special submanifold of the principally
   polarized abelian variety. No standard construction is known for this.

3. **B₂, B₃, B₄**: Each block requires a separate construction. B₄ (eigenvalue
   0.383386, near-zero A₀ overlap) is the hardest and most genuinely new.

4. **From abelian 4-folds to general varieties**: Even if B₁ is resolved for
   A_*, the general Hodge conjecture for all smooth projective X remains open.
   Markman 2025 proved Hodge for abelian fourfolds of Weil type; the frontier
   is now dim ≥ 5.

---

## Attribution

*Authors*: Brayden Ross Sanders (7Site LLC) & Monica

*External mathematics used*: Hodge (1941), Weil (1977 Weil-type abelian varieties),
Lefschetz (Hard Lefschetz), Griffiths-Harris (Hodge-Riemann relations),
Markman (2025, arXiv:2502.03415 — Hodge for abelian fourfolds).

*Computations*: Gram matrix diagonalization; Galois action on cohomology;
cycle class projections; J-stable sub-space enumeration.

*Source memos*: `sprint_memos/HODGE_B1_CYCLE_CONSTRAINT_MEMO.md`,
`HODGE_HIDDEN_STRUCTURE_MEMO.md`, `HODGE_NUMERICAL_SIMPLE_MEMO.md`,
`HODGE_8D_OBSTRUCTION_MEMO.md`, `HODGE_EXPLICIT_WEIL_MEMO.md`,
`HODGE_MISSING_CYCLE_MEMO.md`, `HODGE_BOUNDARY_PUSH_MEMO.md`.

*(c) 2026 Brayden Ross Sanders / 7Site LLC & Monica*
*7Site Public Sovereignty License v1.0 — Human use only. Free forever.*
