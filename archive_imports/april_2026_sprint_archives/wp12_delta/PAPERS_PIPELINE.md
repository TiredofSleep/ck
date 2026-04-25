# TIG Papers Pipeline — Journal Submission List

**Updated:** April 24, 2026 (after WP12)

---

## Submitted / ready for arXiv

### WP11 — SO(8) Identification *(finalized April 23, 2026)*
- Title: *The Lie Algebra Structure of the Coherence Lattice*
- Result: CL (flow antisymmetrization) generates so(8) = D₄
- Status: journal-ready draft (391 lines, MSC 2020 classified)
- Target: arXiv math.RA → J. Algebra or Trans. AMS

### WP12 — SO(10) Identification *(finalized April 24, 2026) ← NEW*
- Title: *An so(10) Identification from the Coupled Coherence Tables*
- Result: CL ∪ BHML jointly generate so(10) = D₅
- Status: journal-ready draft (441 lines, MSC 2020 classified)
- Target: arXiv math.RA (companion to WP11) → J. Algebra or Math. Z.

---

## Earlier whitepapers (WP1–WP10) — already in repo

*github.com/TiredofSleep/ck*

1. WP1 — UOP foundation (Unified Orthogonality Principle)
2. WP2 — Crossing Lemma  
3. WP3 — Productive Incompleteness addendum
4. WP4 — MVJN (Minimal Viable Jordan Non-triviality)
5. WP5 — p-kernel obstruction
6. WP6 — Z/10Z physics constants sprint (1/α, dark matter, visible matter)
7. WP7 — Compositional Lattice rigorous analysis
8. WP8 — D2 breakthrough (operators as second derivatives)
9. WP9 — LATTICE theorem / paradoxical information algebras *(pending)*
10. WP10 — DKAN *(pending)*

---

## Future pipeline (in priority order)

### WP13 — Explicit Triality
- Title: *Triality as the Explicit Outer Automorphism of the Coherence Lattice Algebra*
- Goal: construct τ : so(8) → so(8) of order 3, explicit 28×28 matrix
- Prerequisites: WP11
- Estimated effort: 1–2 sprints
- Target: Trans. AMS or Math. Z.

### WP14 — Clifford Extension
- Title: *Spinor Representations of the TIG so(10) and a Route to e₈*
- Goal: construct the 16-dim spinor of so(10) via Cl(V) and examine if TIG's 22-shell is the natural carrier
- Prerequisites: WP12
- Estimated effort: 3+ sprints (research program)
- Target: Adv. Math. or Invent. Math.

### WP15 — Octonion Structure
- Title: *Does fuse(a, b, c) on Ω ∖ {VOID, HARMONY} Recover Octonion Multiplication?*
- Goal: test whether the CL composition on the 8-element non-absorber set matches octonion product
- Prerequisites: WP11
- Estimated effort: 1 sprint
- Target: J. Algebra

### WP13-alt — Mantero Collaboration Paper
- Title: *Pure-but-not-matroidal Simplicial Complexes: The TIG Bump Complex*
- Goal: formalize the 21.9% basis-exchange defect of Δ_B in Mantero's focal matroid language
- Collaborator: Dr. Paolo Mantero (U Arkansas)
- Prerequisites: MathOverflow post, initial Mantero engagement
- Estimated effort: 6–12 months collaborative
- Target: Trans. AMS or Math. Z.

---

## Commitments made publicly

1. **MathOverflow post** (committed to Mantero April 24, 2026):
   - Scope: projective dimension pd(A) and Koszul property of I_CL = (x_i x_j − CL(i,j) x_0)
   - May also include BHML analog: I_BHML = (x_i x_j − BHML(i,j) x_0)
   - Tags: ac.commutative-algebra, monomial-ideals, koszul-algebras, matroids
   - Link to be sent to Mantero when posted

2. **Reproducibility** (standing commitment):
   - All verification scripts available in repo
   - Python 3.11 + numpy 1.26 + scipy 1.11 standard environment
   - Machine tolerances documented

---

## Structural roadmap

```
     WP11 (so(8))  ← complete
       │
       ├──→ WP13 (triality)
       │
       └──→ WP12 (so(10))  ← complete
              │
              ├──→ WP13-alt (Mantero: pure-not-matroidal)
              │
              └──→ WP14 (Cl(V), spinor, route to e₈)
                     │
                     └──→ [future] WP16+: exceptional tower if reachable
                                          ├── F₄
                                          ├── E₆
                                          ├── E₇
                                          └── E₈

     WP15 (octonions): parallel track, needed for Freudenthal-Tits
```

---

🙏 LATTICE.
