# The Pre-Form Foundation
## Three Layers: Foundation → Finite Grammar → Infinite Deployment

*Brayden Sanders / 7Site LLC | March 2026*
*Classification: §1–2 definitional. §3 exact (computed). §4–5 structural. §6 heuristic.*

---

## The Right Question

Not: "How do we extend TIG to everything?"

**"What is the smallest pre-form grammar from which TIG is one finite realization, and base-10 arithmetic is one infinite coordinate system?"**

A finite algebra and an infinite number system are doing different jobs. The finite algebra gives allowed local transformations. The infinite system gives address space, scaling, and recurrence depth. Both are realizations of the same deeper grammar. Neither is the foundation.

---

## Layer 1: The Pre-Form Foundation

Five primitives. Before numbers, before tables, before coordinates.

**P1 — Distinction.** Something can differ from something else. Without this: no structure.

**P2 — Relation.** Differences interact. Without this: no algebra.

**P3 — Recurrence.** Relations repeat across steps and scales. Without this: no persistence, no infinity.

**P4 — Support.** Some repeated relations stabilize; others do not. Without this: no corridor, no mode, no band.

**P5 — Cancellation.** Some supported relations reach exact balance. Without this: no zero, no node, no reset.

These five are necessary and sufficient. Every system in this program is a realization of some combination of them.

---

## Layer 2: Finite Realization (where TIG lives)

**TIG** (machine-verified, Gen10.14 commit d3db298, 65/65 tests):

| Primitive | TIG object | Status |
|-----------|-----------|--------|
| P1 Distinction | 9 states {1..9} | exact |
| P2 Relation | TSML/BHML tables (SHA: 7726d8a6...) | exact, SHA-pinned |
| P3 Recurrence | TSML closed on {1..9} | machine-proved |
| P4 Support | C={1,3,7,9} sub-magma; 6 λ-corridors | machine-proved |
| P5 Cancellation | HAR=7 absorbing; 71 pairs at λ=0, 13 at λ>0 | machine-proved |

**Two distinct gradings (not the same thing):**

*Algebraic grading* — the nested sub-magma chain:
- {7} — singleton HAR (absorbing element alone)
- {1,3,7,9} = C — corner sub-magma (C×C ⊆ C, proved)
- {1..9} — the whole algebra

*Metric grading* — the 6 λ-corridors (Pre-leak through CTR), defined by λ = 2|σ−½|

The algebraic grading has 3 levels. The metric grading has 6. The corridors are not sub-magma chains; they are metric stratifications of the same algebra. Both are needed.

---

## Layer 3: Infinite Deployment (where base-10 lives)

Base-10 is not the foundation. It is a coordinate scaffold for iterative deployment.

**The exact correspondence** (computed):

| Primitive | Base-10 | Base-6 | Base-12 | Critical strip |
|-----------|---------|--------|---------|---------------|
| P1 Distinction | digits {0..9} | {0..5} | {0..11} | σ+it labels |
| P2 Relation | × mod 10 | × mod 6 | × mod 12 | ζ functional eq. |
| P3 Recurrence | place value | place value | place value | t → ∞ |
| P4 Support | units {1,3,7,9} | units {1,5} | units {1,5,7,11} | zero-free strip |
| P5 Cancellation | 0 (additive) | 0 | 0 | Riemann zeros |

**The key fact** (computed): Primes mod 10 = {1,3,7,9} = TIG corner set C exactly. This is not a coincidence of base-10. In every base b, primes mod b = (ℤ/bℤ)* = the multiplicative units. The corner set IS the unit group. The gap set G={2,4,5,6,8} IS the non-units.

TIG formalizes what every base already knows: the support structure is the unit group, and the cancellation element (HAR=7, which acts as 1 mod the sub-magma) is the multiplicative identity.

**Base-10 is therefore one infinite address system for the same persistence grammar — not its cause.**

The same grammar can be deployed into: base-2, base-6, base-12, p-adic structures, affine planes AG(2,p), continuous strips, operator families. Each gives different address space but the same five primitives.

---

## The Classification Problem

**Definition.** A *persistence grammar* of type (n, G, A, k) is a finite set X with |X|=n, binary operation ∘, generating set G ⊆ X, absorbing element A∈X, and a chain of k nested sub-magmas ∅ ⊊ S₁ ⊊ ... ⊊ Sₖ = X.

**TIG** is type (9, {1..9}, 7, 3) with algebraic grading k=3 and metric grading k=6.

**The gap question becomes precise:**

*Generative gap:* States not reachable from the generators in any number of steps. For TIG: G={2,4,5,6,8} — reachable from C in 0 steps (since C∘C⊆C, no element of G appears). Permanent. Algebraic.

*Support gap:* States reachable by the grammar but not sustainably occupiable under infinite deployment. For ζ: a zero at σ≠½ is expressible (it's a point in the critical strip) but not sustainable (frequency×duration→0). Asymptotic. Analytic.

**These have different causes and require different proofs:**

| Gap type | Cause | TIG proof | ζ proof |
|----------|-------|-----------|---------|
| Generative | Sub-magma closure | C×C⊆C (proved, Proc. AMS) | Cancellation locus 71→13 (82% contraction) |
| Support | Corridor freq×duration | Jutila × two-tick → 0 (machine-verified to t≈10,000) | Appendix E corridor seals |

---

## The Deployment Map

```
PRE-FORM FOUNDATION: {Distinction, Relation, Recurrence, Support, Cancellation}
        │
        ├──→ FINITE REALIZATIONS (compressed local models)
        │         ├── TIG:  n=9, k=6 corridors, spectral gap 3/4, rational thresholds
        │         ├── Bool: n=2, k=1, trivial
        │         ├── Z/nZ: n=any, k=1 (units/non-units only), no corridor grading
        │         └── ?: minimum n for k=6 graded, irrational spectral gap
        │
        └──→ INFINITE DEPLOYMENTS (extended coordinate systems)
                  ├── Base-10: units={1,3,7,9}, primes=support, 0=cancellation
                  ├── Base-6:  units={1,5}, same grammar, 2-element support
                  ├── ζ(s):    zero-free strip=support, zeros=cancellation, KV=floor
                  ├── AG(2,p): lines=corridors, survivors=Ω(p²), 1 corridor=O(1)
                  └── L²(strip): continuous deployment (bridge still open)
```

---

## The Invariant (Final Form)

**Weakest version:** A persistence grammar is any system realizing P1–P5.

**Stronger:** A persistence grammar is a finite magma with an absorbing element, a proper generating sub-magma, and a metric stratification making the cancellation locus strictly larger at the ground level than at any positive distance.

**Strongest (survives scrutiny):** *A persistence grammar is a finite non-associative magma $(X, \circ)$ with absorbing element $a \in X$, sub-magma $C \subseteq X$ with $C \circ C \subseteq C$, and cancellation locus $\mathcal{Z}(\lambda) = \{(s,c): \mathrm{Mix}_\lambda[s][c] = a\}$ satisfying $|\mathcal{Z}(0)| > |\mathcal{Z}(\lambda)|$ for all $\lambda > 0$.*

**TIG satisfies this:** |Z(0)| = 71, |Z(λ>0)| = 13. The ground level has 5.5× more cancellation room. This is why σ=½ supports zeros and σ≠½ does not — not by assumption, but by the structure of the grammar.

---

## What the Classification Asks

1. What is the minimum n for a persistence grammar with k=6 graded levels and rational spectral gap?
2. Are there degree-(n,6) grammars with irrational spectral gap? (If yes, TIG is not forced; if no, TIG is the unique rational-gap realization)
3. Which infinite deployments of a degree-(n,k) grammar preserve the full corridor grading? (This is the "which deployments are faithful" question — and the answer for ζ is what closes RH)

These are clean classification questions. They do not require TIG to be special; they ask *whether* it is, and *why*.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.14 | DOI: 10.5281/zenodo.18852047*
