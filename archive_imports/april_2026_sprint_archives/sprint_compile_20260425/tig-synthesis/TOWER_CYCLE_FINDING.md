# Cycling through the tower — three involutions, three different decompositions

**Date:** 2026-04-25
**Source scripts:** `cycle_tower_v2.py` and follow-ups
**Verification:** machine precision

---

## The unified table

For each tower-level involution τ, I decomposed the antisymmetric content of TSML+BHML into +1 and −1 eigenspaces under conjugation, then computed the bracket-closure dimension on each side.

| Involution | what it is | +1 dim (Lie subalg) | −1 dim | Sum |
|---|---|---|---|---|
| **τ_1 = transposition** | Lie/Jordan flip | 0 | 45 | 45 |
| **τ_2 = P_56 conjugation** | Clifford/Permutation | **36** = so(9) | **9** = R⁹ vector | 45 |
| **τ_3 = σ³ conjugation** | the 6-cycle's Z_2 | 24 | 21 | 45 |

τ_1 is degenerate on antisymmetric content (transposition sends A → −A, so the +1 side is empty). It's the involution of the *full* (sym+antisym) algebra, not of the antisym side specifically.

τ_2 gives the textbook so(10) → so(9) ⊕ R⁹ split that we already knew.

**τ_3 gives a 24+21 split that is not a textbook decomposition.** This is the new finding from cycling through the tower.

---

## What 24 + 21 is

σ³ has cycle structure `(0)(3)(8)(9) | (1,5)(7,4)(6,2)` — four fixed indices and three transposition pairs.

The 24-dim +1 eigenspace decomposes as:

- **so(4) on the 4 fixed indices** (dim 6) — the rotations of {0, 3, 8, 9}
- **σ³-symmetric F↔P couplings** (dim 12) — between fixed indices and pair-blocks, taking the symmetric combination under each pair-swap
- **σ³-symmetric P↔Q couplings** (dim 6) — between two distinct pair-blocks, taking the swap-symmetric combination

Total: 6 + 12 + 6 = 24 ✓

The 21-dim −1 eigenspace decomposes as:

- **so(2) on each pair** (dim 3) — the within-pair rotations, which σ³ flips because σ³ swaps within each pair
- **σ³-antisymmetric F↔P couplings** (dim 12)
- **σ³-antisymmetric P↔Q couplings** (dim 6)

Total: 3 + 12 + 6 = 21 ✓

---

## The pattern that emerged from cycling

I expected one of two things:

1. The same pattern at each level (boring)
2. Wildly different patterns at each level (no story)

What actually happened is **a clean third option**: each level decomposes so(10) along a different orbit-structure, and the dimensions are forced by the cycle structure of the involution.

| Involution | Cycle structure on 10 indices | so(10) split |
|---|---|---|
| τ_2 = P_56 | (5,6) and 8 fixed | 36 + 9 |
| τ_3 = σ³ | three (·,·)'s and 4 fixed | 24 + 21 |

For an involution with `f` fixed indices and `p` transposition pairs (so `f + 2p = n = 10`), the +1 eigenspace dimension is:

```
+1 dim = C(f, 2) + p + f·p + C(p, 2)·2
       = f(f-1)/2 + p + fp + p(p-1)
```

Verifying:
- P_56: f=8, p=1 → 8·7/2 + 1 + 8·1 + 0 = 28 + 1 + 8 = 37? No wait that's not 36.

Let me reconsider. For P_56 (one transposition pair on indices 5,6, eight fixed):

- so(8) on the 8 fixed indices (those that aren't 5 or 6): C(8,2) = 28
- so(2) on the (5,6) pair: dim 1, but **this is P_56-anti, not P_56-fixed** (because P_56 is the swap itself, applied to E_56 - E_65 gives -(E_56 - E_65)). So 0 from this block on +1 side, 1 on −1.
- F↔P couplings: 8 fixed × 1 pair × 2 components = 16 basis elements, splitting 8 σ³-fixed + 8 σ³-anti
- P↔P: only 1 pair, so no cross-pair couplings

Total: 28 + 0 + 8 = 36 ✓ on +1 side
And: 0 + 1 + 8 + 0 = 9 on −1 side ✓

Now σ³ verification:
- so(4) on 4 fixed: C(4,2) = 6
- so(2) on each of 3 pairs: 0 σ³-fixed (these are anti)
- F↔P: 4 × 3 × 2 = 24, splitting 12+12
- P↔P: C(3,2) = 3 pairs-of-pairs, 4 basis elements each = 12 total, splitting 6+6

+1: 6 + 0 + 12 + 6 = 24 ✓
−1: 0 + 3 + 12 + 6 = 21 ✓

So the formula is:
```
+1 dim = C(f, 2) + 0 + f·p + C(p, 2)·2
−1 dim = 0 + p + f·p + C(p, 2)·2
+1 + −1 = C(f, 2) + p + 2fp + 2·C(p, 2)·2
        = f(f-1)/2 + p + 2fp + 2p(p-1)
        = (f² - f)/2 + p + 2fp + 2p² - 2p
        = (f² - f)/2 - p + 2fp + 2p²
```

Check at f=8, p=1: (64-8)/2 - 1 + 16 + 2 = 28 - 1 + 16 + 2 = 45 ✓
Check at f=4, p=3: (16-4)/2 - 3 + 24 + 18 = 6 - 3 + 24 + 18 = 45 ✓

So the +1 dim formula is `f(f-1)/2 + fp + 2·p(p-1)/2·1 = f(f-1)/2 + fp + p(p-1)`.

And the −1 dim is `p + fp + p(p-1)`.

---

## What this tells us about the tower

The two non-trivial involutions of so(10) we have come from elements of finite order in O(10):

- **P_56** is order 2, acts as a single transposition on 10 indices → splits so(10) as 36 + 9
- **σ³** is order 2, acts as 3 disjoint transpositions on 10 indices → splits so(10) as 24 + 21

These are different inner automorphisms of so(10). They give different gradings.

**P_56's grading** (36 + 9) is the **so(9) ⊕ R⁹** decomposition associated with the SO(10) → SO(9) breaking in GUT physics. We've identified this with the matter/antimatter outer automorphism σ_outer.

**σ³'s grading** (24 + 21) is associated with a different breaking. The +1 subalgebra (dim 24) acts on a 4-dim invariant subspace (the σ-fixed indices) and a 6-dim "symmetric pair-component" subspace. The structure is `so(4) ⊕ (something 18-dim)`. The "something" couples the 4-fixed block to the 3 pair-blocks via σ³-symmetric combinations.

In SO(10) GUT terms, σ³ is *not* the matter/antimatter swap. It's a different, finer involution sitting inside SO(10). The 24+21 decomposition is the first hint of a structure that we haven't yet placed in standard GUT phenomenology.

---

## What this means for "cycling through the tower"

The three tower involutions are **not equivalent**. They produce distinct gradings of so(10):

```
τ_1 (transposition):    full so(10), no inner split (the involution acts on outer structure)
τ_2 (P_56):             45 = 36 + 9    [so(9) ⊕ R⁹]
τ_3 (σ³):               45 = 24 + 21   [centralizer of σ³ ⊕ its complement]
```

Both τ_2 and τ_3 are *inner* involutions (induced by elements of O(10) acting by conjugation). They give different decompositions because they're different elements.

**The tower's two real Z_2 involutions correspond to two distinct gradings of so(10).** Each one tells you a different structural fact:

- τ_2 tells you the matter/antimatter (σ_outer) and Higgs-irrep structure
- τ_3 tells you something about the σ-fixed lattice's relationship to the 6-cycle pairs — a finer grading we haven't fully interpreted

That's a bigger structural payload than I expected. There are TWO orthogonal gradings of so(10) implicit in TIG, not one.

---

## What this changes about the bridge to Mantero

The 24 + 21 decomposition is much more "commutative-algebra-shaped" than the 36 + 9 one:

- 24-dim Lie subalgebra fixed under σ³-conjugation = **the centralizer of an order-2 element**. Centralizers of involutions are studied extensively in algebraic group theory.
- The 4 fixed indices {0, 3, 8, 9} form an invariant subspace. The 6-dim pair-subspace splits into 3 ⊕ 3 under σ³ (symmetric and antisymmetric pair-components).
- This is the kind of decomposition Mantero's circle would recognize from the structure theory of finite-group-equivariant rings.

The MathOverflow question we'd post for him isn't "is TIG real" — it's something like: *"Given a commutative non-associative magma whose left-regular antisymmetrization closes at so(8) and whose extension to so(10) splits 24+21 under a natural Z_2 element, what structural properties of the magma are forced?"*

That's a clean, specific, answerable question for the algebra community. It doesn't mention TIG, GUT, physics, or Brayden's framework. It's just a math question about a small magma.

---

## Bottom line

Cycling through the tower didn't reveal one repeated pattern. It revealed:

1. **τ_1 (transposition) is the global Lie/Jordan flip** — both sides regenerate the full algebra
2. **τ_2 (P_56) gives the σ_outer / matter-antimatter / so(9) grading** (45 = 36 + 9)
3. **τ_3 (σ³) gives a different inner grading** (45 = 24 + 21), structured around fixed indices vs. the 6-cycle pairs

The "two sides of one coin" was right for τ_1 (one coin, two views).
**The tower has multiple coins.** Each involution flips a different coin, exposing a different facet of so(10).

That's a structural finding worth one MathOverflow post, written in the algebra community's language, no TIG framing.

🙏
