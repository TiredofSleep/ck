# Explicit Construction: Dirac Spinor-Rep Generators Inside TSML's so(8)

**Date:** 2026-04-25
**Status:** Computation complete, machine-verified at 10^-16 precision
**Files:** `build_v2.py` (reproducible)

---

## What was computed

The six anti-Hermitian generators of so(1,3) in the 4-dim Dirac spinor representation:

```
M̃^{0i} = (i/2) γ^0 γ^i        (boosts, i = 1, 2, 3)
M̃^{ij} = (1/4) [γ^i, γ^j]      (rotations, ij ∈ {12, 13, 23})
```

were lifted to real 8×8 antisymmetric matrices via the standard C^4 ↔ R^8 isomorphism, then projected onto TSML's so(8)-on-V_8 basis (where V_8 is the 8-dim invariant subspace inside R^10 that TSML's flow operators act faithfully on).

**Result:** All six M̃^μν project with residual at machine precision (10^-16). Each can be written as an explicit linear combination of the 28 TSML-derived so(8) basis elements. The five largest-magnitude coefficients for each generator were extracted and printed.

The reconstruction error (M̃^μν versus its expansion in TSML basis) is bounded by 2 × 10^-15 in Frobenius norm for all six generators.

## What this means rigorously

### The strong honest claim

**Six specific elements of TSML's so(8) Lie algebra, viewed as antisymmetric 8×8 matrices on V_8, are equal (up to machine precision) to the Dirac spinor-rep generators of so(1,3) under the C^4 ↔ R^8 lifting.**

The coefficients are explicit and reproducible. The construction is constructive, not existential.

### The qualifier that matters

This worked because **so(8) on V_8 is the *full* 28-dim Lie algebra of antisymmetric 8×8 matrices.** Any antisymmetric 8×8 matrix lies in it automatically — it's a containment forced by dimension count, not by any property specific to TSML's generators.

What TSML *does* contribute is a specific basis of this 28-dim space derived from its 6 flow operators via Lie closure. The coefficients of M̃^μν in that basis are what we computed. A different generating set producing the same so(8) would give different coefficients.

### What is novel and what isn't

**Not novel:** that so(1,3) ⊂ so(8) and that Dirac generators realize so(1,3). This is textbook.

**Not novel:** that any antisymmetric 8×8 matrix lies in so(8). Trivially true.

**Possibly useful:** the explicit numerical expression of the six Dirac generators in TSML's specific basis. This makes the abstract embedding into a concrete computational object you can manipulate. If anyone wants to ask questions like "what does γ^0 γ^1 look like as a TSML expression?", the answer is computable from these coefficients.

**Worth noting:** the construction extends to so(10) once BHML is included. The same projection — but onto TSML+BHML's so(10)-on-V_? — would write the so(1,3) generators in a basis that has SO(10) GUT structure baked in. That's the version that connects to physics.

## What I ran, what I verified

### Verified
- TSML so(8) closure dim 28 ✓ (re-confirmed WP11)
- so(8) acts on V_8 ⊂ R^10 with VOID annihilated ✓
- so(8) on V_8 spans the full 28-dim antisymmetric matrix space ✓
- Standard Dirac matrices satisfy {γ^μ, γ^ν} = 2η^{μν} I ✓ (all 16 anticommutators)
- M̃^μν generators are anti-Hermitian on C^4 ✓
- M̃^μν Lie commutators satisfy so(1,3) relations on representative pairs ✓
- Real 8×8 lifts of M̃^μν are antisymmetric ✓
- Lie closure of the 6 lifted M̃^μν is dim 6 ✓
- All six M̃^μν project onto TSML's so(8) basis with 10^-16 residual ✓

### Coefficients (sample, top 5 by magnitude)

```
M̃^01: a_3=+0.683 a_11=+0.593 a_26=-0.565 a_21=-0.379 a_9=-0.332 
M̃^02: a_6=+0.674 a_24=+0.522 a_8=-0.511 a_0=+0.489 a_4=+0.356 
M̃^03: a_6=+0.683 a_2=+0.488 a_25=+0.409 a_15=-0.358 a_4=-0.347 
M̃^12: a_2=+0.573 a_4=+0.517 a_25=+0.495 a_23=-0.474 a_16=-0.413 
M̃^13: a_24=-0.645 a_15=-0.455 a_14=+0.406 a_3=-0.390 a_12=+0.377 
M̃^23: a_9=+0.747 a_5=-0.461 a_8=+0.395 a_25=-0.383 a_26=-0.342 
```

(Indices refer to TSML's specific so(8) basis as ordered by Lie closure construction.)

## What this does NOT prove

The construction shows the embedding works in TSML's specific 28-dim so(8) basis. It does **not** prove:

1. That TSML's basis is "physically natural" or selected. The basis comes from a deterministic Lie closure procedure but has no a priori physical meaning.
2. That the coefficients have a closed-form expression. They are real numbers obtained from SVD; whether they equal simple algebraic combinations of TIG constants is a separate question worth checking.
3. That this construction produces SO(10) GUT physics. To get there, the same construction needs to be done with TSML+BHML producing so(10), then the chiral spinor 16 of Spin(10), then restriction to so(1,3). Each step is well-defined; none have been computed yet.

## Reasonable next computations

1. **Repeat with so(10) (TSML + BHML).** Need the BHML table. Output: Dirac generators expressed in TSML+BHML's so(10) basis.

2. **Look for closed-form coefficients.** Check whether the numerical coefficients above match simple expressions involving the TIG constants T* = 5/7, S* = 4/7, σ-permutation entries, etc. If they do, that's structurally significant. If not, the coefficients are basis-dependent numerical facts.

3. **Compute the conjugating element Q ∈ O(8).** There exists Q such that Q · so(1,3)_Dirac · Q^T equals a specific subspace of TSML's so(8). Finding Q explicitly would give the geometric "rotation" between TSML's natural frame and the Dirac frame.

## Honest framing for the atlas / write-up

The right sentence for outside audiences:

> *TSML's flow generators close into so(8), which has so(1,3) as a subalgebra by general theory. The Dirac spinor-rep generators of so(1,3), lifted to 8×8 real antisymmetric matrices, can be written explicitly as linear combinations of TSML's 28-element so(8) basis (see coefficients in [filename]). The construction is constructive but inherits its embedding from standard Lie theory; the contribution of TSML is providing an explicit, computationally manageable basis for the so(8) it generates.*

That sentence will pass referee reading. It claims what's true. It doesn't claim more than that.

🙏
