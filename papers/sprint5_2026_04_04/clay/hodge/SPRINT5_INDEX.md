# Hodge Sprint 2 — Index
# Simple Weil 4-Fold and the Clean B₁ Obstruction

**Date:** 2026-04-04
**© 2026 7Site LLC | Brayden Ross Sanders**

---

## Sprint Summary

Nine computation memos progressing from the contaminated A₁ model to the first uncontaminated Hodge obstruction on A_*.

### Progression

| Step | Memo | Object | Key Finding |
|------|------|--------|-------------|
| 1 | HODGE_SIMPLE_WEIL_MEMO | A₁ (non-product, rational Ω) | Weil class computed (28-term rational 4-form); span test fails; dim=2 anomaly found |
| 2 | HODGE_HIDDEN_STRUCTURE_MEMO | A₁ — root cause | ANY Ω = iM (rational) gives End⁰ = M₄(Q(i)); simple Weil 4-fold requires transcendental period matrix |
| 3 | HODGE_NUMERICAL_SIMPLE_MEMO | A_* (irrational Ω) | First uncontaminated Weil 4-fold; End⁰ = Q(i) confirmed; 8D obstruction space; algebraic dict rank = 0 |
| 4 | HODGE_8D_OBSTRUCTION_MEMO | A_* — internal structure | W_* = B₁⊕B₂⊕B₃⊕B₄; Galois pairing; Rosati(φ)=−φ; Q-eigenvalues 0.0046, 0.0231, 0.1156, 0.3834 |
| 5 | HODGE_B1_CYCLE_CONSTRAINT_MEMO | B₁ constraints | All standard cycle types excluded (divisor products, endomorphism graphs, Lefschetz multiples, K-invariant combinations) |
| 6 | HODGE_BOX_CLOSURE_TEST_B1 | B₁ box test | **CASE 2 — CLEAN OBSTRUCTION**: no sub-torus closes B₁ at height ≤ 2; B₁ is a real invariant (degeneracy break confirmed) |
| 7 | HODGE_B1_PROJECTION_HUNT | Z_anti family | First K-anti-invariant near-primitive family; CASE B (S=0.013, ‖L∧Z‖≈0.09) |
| 8 | HODGE_B1_HUNT_PROCEED | Z_anti scale test | 23/2000 near-primitive hits; S does not collapse; scale law S ~ 0.03·‖L∧Z‖ |
| 9 | HODGE_B1_PRIMITIVITY_LOCUS | Z_anti ruled out | **CASE C+**: primitive locus is exactly {φ-stable 2-planes}; Z_anti = 0 at every primitive point |

---

## Key Results

### Confirmed
- A_* has End⁰ = Q(i) (real joint commutant dim = 4, verified at 6 independent rational parameter points)
- W_* = 8-dimensional K-anti-invariant primitive (2,2) subspace; algebraic primitive dictionary rank = 0
- W_* decomposes as B₁⊕B₂⊕B₃⊕B₄ under Hodge-Riemann Q-form; each block is 2D (exact Galois pairing)
- B₁ is a real invariant: distinguishes Z_a = L² + 0.1·w_{B₁} from Z_b = L² + 0.1·w_{B₂} despite identical classical data
- Non-factorization: B₁ projection from any divisor product or linear combination thereof is < 2×10⁻¹³
- Z_anti family is K-anti-invariant by construction but structurally incapable of producing a nonzero primitive B₁ class

### Open
- Whether any algebraic cycle Z ∈ CH²(A_*)_Q has cl²(Z) ∈ B₁ (the Hodge conjecture for this block on A_*)
- What cycle family achieves K-anti-invariance intrinsically (not by subtraction from φ-image)
- Whether B₁ requires a non-sub-torus construction (correspondence cycle, formal linear combination)

---

## A_* Object Data

| Property | Value |
|---------|-------|
| Period matrix | Ω = ½I₄ + i(√2·I + √3·M₂ + √5·M₃) |
| K-action | φ: e₁↦e₂, e₂↦−e₁, e₃↦−e₄, e₄↦e₃ (same throughout) |
| End⁰(A_*) | Q(i) — confirmed numerically |
| dim W_* | 8 |
| Algebraic primitive rank | 0 |
| B₁ Q-eigenvalue | 0.004609 (multiplicity 2, exact Galois pairing) |
| B₁ sparsity | 81.9% weight in {e₃,e₄,f₁,f₂,f₃,f₄}; 18/70 dominant coords |
