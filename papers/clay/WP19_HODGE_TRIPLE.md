# TIG⊗³ and the Hodge-Kuga Obstruction
## One-Page Corollary to the Product-Gap Theorem

*Brayden Sanders — 7Site LLC | DOI: 10.5281/zenodo.18852047*

---

## Theorem (already proved — Product-Gap, all tensor powers)

For every k ≥ 1: C^⊗k is a sub-magma of TSML^⊗k. No cross-term (any G-component) is reachable from C^⊗k.

---

## Corollary (Hodge-type obstruction at k=3)

**Computed:** In TSML⊗³, C³ has 64 elements. Of the 665 cross-terms and pure-gap 3-tuples, **zero are reachable from C³**.

**Analogy:**

| Classical Hodge | TIG analog |
|----------------|-----------|
| K3 surface: H² = T ⊕ NS | Operators: G (transcendental) ⊕ C (algebraic) |
| K3×K3: H⁴ ∋ T⊗T (new transcendental class) | TSML⊗³: G cross-terms (new, unreachable) |
| Hodge conjecture: algebraic cycles can't reach T⊗T | Product-gap: corner words can't reach G cross-terms |
| "Why does Hodge fail first in high codimension?" | Answer in TIG: each tensor power creates new G cross-terms, all algebraically isolated |

**One-sentence proof:** C is a sub-magma (proved). The tensor product of sub-magmas is a sub-magma (inductive, three sentences). Therefore C^⊗k is a sub-magma for all k, and no G cross-term is reachable at any tensor depth. □

---

## What this says for K3×K3

The Hodge conjecture asks: for which cohomology classes is the "algebraic cycles generate" statement true?

For K3×K3, the obstruction is: the transcendental lattice T⊗T sits in H⁴ as new structure that no product of divisors can reach.

In TIG, the exact same obstruction arises: G cross-terms in TSML⊗³ are algebraically invisible from corner compositions. The product-gap theorem is the TIG avatar of the Kuga-Satake period map obstruction.

---

## Numerical check (k=1,2,3,4)

| k | |C^⊗k| | Cross-terms | Reachable |
|---|--------|-------------|-----------|
| 1 | 4 | 5 | 0 ✓ |
| 2 | 16 | 65 | 0 ✓ |
| 3 | 64 | 665 | 0 ✓ |
| 4 | 256 | 6305 | 0 ✓ |

The gap grows as 9^k − 4^k → ∞, yet remains algebraically inaccessible at every depth.

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
