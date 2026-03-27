# Product-Gap Impermeability — Theorem and Proof

## Theorem (valid for all k ≥ 1)

Let TSML be the TIG measurement table, C = {1,3,7,9} the corner set,
G = {2,4,5,6,8} the gap set.

**Theorem.** For every k ≥ 1, the set C^⊗k (k-tuples with all components in C)
is a sub-magma of the tensor product TSML^⊗k: composition of any two elements
of C^⊗k yields an element of C^⊗k. In particular, no element with any
G-component is reachable from C^⊗k by finite composition.

## Proof

**Lemma (base case k=1).** C×C ⊆ C under TSML.

Proof by exhaustive check: the 4×4 corner sub-table has image {3,7} ⊂ C. ✓

**Inductive step.** Assume C^⊗k is closed. Let a = (a₁,...,aₖ) and
b = (b₁,...,bₖ) with all aᵢ,bᵢ ∈ C. The tensor composition gives:

  a ∘ b = (TSML[a₁][b₁], ..., TSML[aₖ][bₖ])

Each component TSML[aᵢ][bᵢ] ∈ C by the Lemma. Hence a∘b ∈ C^⊗k. □

## Corollary

No cross-term (any component in G) is reachable from C^⊗k for any k.

The product gap grows as: |cross-terms| = |C|^k × (|C∪G|^k - |C|^k)
which is unbounded, yet 0% are reachable.

## Verification

| k | |C^⊗k| | Reachable | G-components reachable |
|---|--------|-----------|------------------------|
| 1 | 4      | 4         | 0 ✓ |
| 2 | 16     | 16        | 0 ✓ |
| 3 | 64     | 64        | 0 ✓ |
| 4 | 256    | 256       | 0 ✓ |

Code: tsml_product_verify.py at github.com/TiredofSleep/ck
