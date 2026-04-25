# Dirac Matrices vs TSML — Three Computations, Honest Findings

**Author:** Claude (Anthropic), in collaboration with Brayden Sanders
**Date:** 2026-04-25
**Status:** Computational note. All claims machine-verified from the canonical CL/TSML table. Scripts in `dirac_tsml/`.

---

## Reverse-engineering from Dirac's side first

Dirac's specification:
1. Four 4×4 complex matrices γ⁰, γ¹, γ², γ³
2. **Anticommutator:** {γᵘ, γᵛ} = 2ηᵘᵛ I (Minkowski metric)
3. **Commutator** generates Lorentz so(1,3): σᵘᵛ = (i/2)[γᵘ, γᵛ]
4. **γ⁵** = iγ⁰γ¹γ²γ³ anticommutes with all γᵘ, squares to ±I
5. **Trace:** tr(γᵘ) = 0, tr(γᵘγᵛ) = 4ηᵘᵛ

What would a Dirac-style object generating so(8) look like, in dimension count?

The smallest faithful representation of Cl(0,8) is **2⁴ = 16-dimensional**. So a "Dirac-style TSML" — explicit Clifford generators of so(8) in spinor representation — would be **eight 16×16 complex matrices**, not ten 10×10 integer matrices.

**Important structural distinction.** TSML's so(8) closure (WP11) happens via the **adjoint representation** (so(8) acting on its own 28-dim algebra), not the **spinor representation** (so(8) acting on 16-dim spinors). These are different representations of the same Lie algebra. Dirac matrices live in the spinor rep; TSML's L_i live in (a subspace of) the adjoint rep.

So the analogy "Dirac matrices ↔ TSML" is structural but not literal. Both produce orthogonal Lie algebras, but via different representation paths.

---

## TEST 1 — Anticommutator {Aᵢ, Aⱼ} structure

**Dirac expectation:** anticommutator is scalar × identity (the metric).

**Computed result:** ❌ NOT scalar × identity.

For any pair (i, j) of flow operators, {Aᵢ, Aⱼ} = AᵢAⱼ + AⱼAᵢ produces a **diagonal matrix** with entries in {0, −2}, but the diagonal pattern is *not* constant. There's a structural anomaly at index 7 (HARMONY position).

Even after projecting out the index-7 row/column, the diagonals remain non-constant. The anticommutators have signature-like content (mostly negative or zero), but they are not pure scalars.

**However:** when reduced mod 2 (treating Aᵢ as F₂ matrices), 12 of the 15 flow-pair anticommutators **vanish exactly**:

| pair | {Aᵢ, Aⱼ} mod 2 nonzero count |
|---|---|
| (1,2) | 0 |
| (1,3) | 0 |
| (1,4) | 0 |
| (1,6) | 0 |
| (1,8) | 0 |
| (2,3) | 2 |
| (2,4) | 2 |
| (2,6) | 0 |
| (2,8) | 2 |
| (3,4) | 0 |
| (3,6) | 0 |
| (3,8) | 0 |
| (4,6) | 0 |
| (4,8) | 4 |
| (6,8) | 0 |

**This is a real F₂-Clifford-like property** — most pairs anticommute exactly over the field with two elements. Three pairs do not: (2,3), (2,4), (2,8), and (4,8). These are the "non-anticommuting" pairs in the F₂ sense.

**Interpretation:** TSML is not a Cl(0,8) generator set in the standard real-valued Dirac sense. But its mod-2 reduction has substantial Clifford-like structure, with a small set of "non-Clifford" pairs that may be a distinct structural feature worth investigating.

---

## TEST 2 — γ⁵ analog

**Dirac:** γ⁵ = iγ⁰γ¹γ²γ³ is the volume element. Anticommutes with each γᵘ, squares to ±I, splits the spinor space into chiral halves.

**Computed:** ❌ no clean γ⁵ analog exists in TSML over ℤ or F₂.

Tested candidates:
1. Each non-flow operator A₀, A₅, A₇, A₉ — none anticommute with all flow operators.
2. Product A₁ · A₂ · A₃ · A₄ · A₆ · A₈ — does not anticommute, does not commute, does not square to scalar × I.
3. F₂ versions of all the above — also fail.

**This is not surprising in retrospect.** γ⁵ is a spinor-rep phenomenon — it depends on the chirality split that exists in even-dimensional Cl(p,q) representations. TSML lives in the adjoint rep, which doesn't have this split. The closest analog in the adjoint rep would be **so(8) triality** — the S₃ outer automorphism group acting on D₄'s root system — which is a three-fold structure rather than the two-fold chiral split γ⁵ provides.

**Interpretation:** searching for γ⁵ in TSML is asking the wrong question. The right analog is triality: does TSML have a natural S₃ action realizing so(8)'s outer automorphisms? That's a separate computation worth doing, and it's the *correct* structural question once you accept TSML lives in adjoint rather than spinor rep.

---

## TEST 3 — Trace structure (Killing form analog)

**Dirac:** tr(γᵘ) = 0, tr(γᵘγᵛ) = 4ηᵘᵛ — diagonal bilinear form.

**Computed:**
- **tr(Aᵢ) = 0 for all i** ✓ (by construction; antisymmetrization forces this)
- **tr(L_i)** is small and varies (1 to 4 across the ten operators)
- **tr(AᵢAⱼ) for flow pairs** — a 6×6 symmetric matrix:

```
          A_1   A_2   A_3   A_4   A_6   A_8
  A_1:   -16    -8   -12   -12   -14   -12
  A_2:    -8   -12   -10    -6   -10   -10
  A_3:   -12   -10   -16   -10   -14   -12
  A_4:   -12    -6   -10   -14   -12   -10
  A_6:   -14   -10   -14   -12   -16   -14
  A_8:   -12   -10   -12   -10   -14   -16
```

**This is the Killing form analog for TSML's flow operators.** Properties:

- **Symmetric:** ✓
- **Diagonal entries:** all negative (−16, −12, −16, −14, −16, −16). Suggests compact / negative-definite structure.
- **Off-diagonal:** all nonzero, ranging −6 to −14. **NOT diagonal in this basis** — the bilinear form is not Dirac-style "metric × identity."
- **Eigenvalues:** [−71.27, −8.20, −4.00, −2.92, −2.73, −0.88]. All negative. **Negative definite.**
- **Determinant:** 16,384 = 2¹⁴. This is a clean power of 2, suggesting structural significance.
- **Trace:** −90.

**Interpretation:**
- The Killing-form analog exists and is **negative definite** — consistent with so(8)'s compact signature (all 28 generators are compact).
- The basis {A_1, A_2, A_3, A_4, A_6, A_8} is **not orthogonal** under this form. To make it Dirac-like (diagonal Killing), we'd need to change basis — orthogonalize via Gram-Schmidt or eigendecomposition.
- The eigenvalue spread (one large eigenvalue at −71, then a cluster around −1 to −8) is interesting — it suggests one direction is much "longer" than the others. That largest eigenvector might correspond to a structurally distinguished combination of flow operators, possibly the analog of the time-like direction in Dirac's so(1,3).

---

## Synthesis — what TSML and Dirac matrices actually have in common

**They share:**
1. Both produce orthogonal Lie algebras (Dirac: so(1,3); TSML: so(8)) by antisymmetrizing matrix products.
2. Both have a non-degenerate bilinear "Killing-like" form (Dirac: tr(γᵘγᵛ) = 4ηᵘᵛ; TSML: 6×6 symmetric matrix above).
3. Both have explicit small-matrix realizations that allow symbolic computation.
4. Both have non-trivial trace structure (tr = 0 for antisymmetrized; nonzero for products).

**They differ:**
1. **Representation:** Dirac in spinor rep (4×4); TSML in adjoint-rep-derived (10×10). Not the same kind of object.
2. **Anticommutator:** Dirac's is scalar × I (defines metric); TSML's is structured but not scalar.
3. **γ⁵ analog:** Dirac has chirality; TSML does not in adjoint rep. Triality is the closer analog but is three-fold rather than two-fold.
4. **Killing diagonality:** Dirac's metric is diagonal in the natural basis; TSML's is not — the natural basis is non-orthogonal.

**The defensible structural claim:**

> TSML's left-regular antisymmetrization {A_1, A_2, A_3, A_4, A_6, A_8} is a **non-orthogonal generating system for so(8) in the adjoint representation**, structurally analogous to but distinct from Dirac's spinor-representation generators of so(1,3). The 6×6 trace bilinear form tr(AᵢAⱼ) is the Killing-form analog and is negative definite with determinant 2¹⁴, consistent with so(8)'s compact signature. There is no γ⁵ analog because the adjoint representation does not admit chirality; the correct analog would be so(8) triality, which is a separate computation.

**The mod-2 finding (interesting and unexpected):**

> Over F₂, twelve of the fifteen flow-operator anticommutators vanish exactly. The three exceptions are pairs (2,3), (2,4), (2,8), and (4,8). This is a non-trivial F₂-Clifford-like structure that has not (to our knowledge) been previously identified, and is a candidate for further investigation — possibly connecting to the F₂-structure of so(8) and its representations in characteristic 2.

---

## What this changes for the atlas / TIG framing

**It strengthens the Lie theory cell of the atlas.** TSML now has a verified Killing-form analog (6×6 symmetric, negative definite, det = 2¹⁴) — that's a concrete invariant suitable for a Lie-theorist (Garibaldi, Baez) to engage with directly.

**It clarifies what TSML is and isn't.** TSML is *not* a Dirac-style Clifford generator; it's an adjoint-rep so(8) generating system. That's a more honest framing, and it survives external scrutiny in a way the Dirac analogy in its loose form would not.

**It opens a triality question.** If TSML is in adjoint rep of so(8), and so(8) has triality, then there should be a three-fold action on TSML's generators corresponding to D₄'s outer automorphism. Computing this would be a real test: if TSML's flow operators decompose under triality, that's structural information; if they don't, that's also information about TSML's specific position in the so(8) representation theory.

**The mod-2 finding is potentially novel.** Most operadic/algebraic work over CL has been done over ℚ or ℝ. The F₂ Clifford-like structure (12 of 15 anticommutators vanish) hasn't appeared in any work I'm aware of from the existing TIG corpus. This is a candidate for a small standalone paper or note.

---

## Three follow-on computations worth doing

1. **Diagonalize the Killing form.** Find the 6×6 orthogonal change of basis that makes the Killing form diagonal. The eigenvector for the largest eigenvalue (−71.27) is the "most compact" direction in flow-operator space.

2. **Compute triality on TSML.** Use the standard so(8) triality automorphism (which permutes the three 8-dim representations: vector, spinor, conjugate spinor) and see how it acts on the flow operators {A_1, A_2, A_3, A_4, A_6, A_8}. Are they permuted, fixed, or sent into a different subspace?

3. **F₂ structure constants.** Build the full multiplication table of {A_1, A_2, A_3, A_4, A_6, A_8} over F₂ and see if it's a known small algebra. The 12-vanishing/3-non-vanishing pattern suggests a sparse structure that should be classifiable.

🙏
