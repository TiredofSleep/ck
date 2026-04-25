# Counting the crossings between Lie and Jordan sides

**Date:** 2026-04-25
**Source script:** `count_crossings.py`
**Verification:** machine precision throughout

---

## What I set out to do

Brayden noted that today's work was almost entirely Lie-side (antisymmetric register), and that Mantero works in Jordan-side territory (symmetric, commutative-algebra register). The intuition: since the two halves cover the algebra exactly, **the gap between us is the structural frontier**, and the question is *how many crossings are there between the two sides?*

If the structure is genuinely "two sides of one coin," the crossing count should be a meaningful invariant — not arbitrary, but forced by the algebra.

---

## The 20 left-regular representations and their decomposition

For each row of TSML and BHML, the left-regular representation L_T[i] and L_B[i] decomposes uniquely:

```
L = A + S
A = (L − L^T)/2      (Lie / antisymmetric register)
S = (L + L^T)/2      (Jordan / symmetric register)
```

20 left-regs total = 10 TSML + 10 BHML.

### Self-crossings (per left-reg, has both A and S nonzero?)

```
TSML: 10 of 10 are crossings (every L_T[i] has both A and S parts nonzero)
BHML:  9 of 10 are crossings
       L_B[0] is the ONE exception — it's PURE Jordan
```

**`L_B[0] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]` — the identity row of BHML**, the natural numbering of indices. It maps i → i. As a matrix in the regular rep, it's diagonal-symmetric, with no antisymmetric content. **It's the singular "label-only" generator.**

So we have:
- **20 nonzero symmetric (Jordan-side) generators**
- **19 nonzero antisymmetric (Lie-side) generators** (one is killed by L_B[0]'s pure-symmetry)

### The 19 vs 20 asymmetry

This is the structural origin of every "magic number" that follows:

```
A·S product nonzero pairs:    19 × 20 = 380
A·A product nonzero pairs:    19 × 19 = 361   ← appears repeatedly
A·S bracket nonzero pairs:    19 × 19 = 361   (same count via different measure)
S·S bracket nonzero pairs:    340 / 400       (with 40 commuting off-diagonal)
```

The number **361 = 19²** is the count of structurally non-trivial crossings between the Lie register and itself when acting on the Jordan register. It's not "deep" — it's the count of pair products among nonzero antisymmetric generators. But it IS forced by the structure.

---

## The Lie-side closure picture

19 raw active generators → 18-dim linear span (one redundancy) → 45-dim Lie closure.

```
Raw subspace:        18 dim
Brackets-added:      27 dim
Total so(10):        45 dim
```

The closure adds 27 dimensions that can ONLY be reached through the Lie bracket — they're not in the span of the raw generators themselves.

That 27 = "purely brackety" dimensions is the size of the Lie-side's "self-creating" capacity from a smaller set of input generators.

---

## The Jordan-side mirror — the surprising part

Here is where switching sides revealed something I didn't expect.

I asked the dual question: forget the antisymmetric generators entirely. **From only the 20 symmetric (Jordan-side) generators, how much of so(10) can you reach via commutators?**

```
Span of [S_i, S_j] for all pairs of TSML+BHML symmetric generators:
                                              dim = 45
```

**The Jordan side alone generates all of so(10) via brackets, with no help from explicit antisym generators.**

This is the real structural finding. The two sides aren't independent registers that need to be combined — **either side, by itself, contains enough information to regenerate the full algebra through bracketing.**

The "Lie-side analysis" we've been doing all session, and the "Jordan-side analysis" that Mantero would naturally do, are not two separate stories. They're **the same story expressed through different brackets.**

---

## What this means structurally

### Two faithful presentations of the same algebra

Lie-side presentation:
- Take antisymmetric parts of L_T[i] and L_B[i]
- Close under commutator [A, B]
- Get so(10) = 45-dim

Jordan-side presentation:
- Take symmetric parts of L_T[i] and L_B[i]
- Close under commutator [S, S']
- **Also get so(10) = 45-dim**

Both routes land in the same place. The bracket [S, S'] of two symmetric matrices is automatically antisymmetric, so the second presentation is implicitly Lie-side once you take the bracket — but the *generators* are explicitly symmetric.

### The 60 commuting Jordan pairs

Of 400 (S_i, S_j) pairs, 60 commute. The 60 = 20 (diagonal, S_i with itself) + 40 off-diagonal commuting pairs.

The 40 off-diagonal commuting pairs are the "Jordan-pure" crossings: they STAY in the Jordan register when bracketed. These are candidates for a maximal commutative subalgebra in the Jordan-product structure — exactly the thing a commutative algebraist would care about.

This is the point of contact with Mantero's natural register: the **40 off-diagonal commuting Jordan-pairs** form the symmetric/commutative skeleton that doesn't need the Lie register at all.

---

## The crossing-count summary

| Crossing type | Count | Out of |
|---|---|---|
| Self-crossings (per left-reg) | 19 | 20 |
| Lie-Lie pair products nonzero | 361 | 400 |
| Lie-Jordan brackets nonzero | 361 | 400 |
| Lie-Jordan anticommutators nonzero | 380 | 400 |
| Jordan-Jordan brackets nonzero | 340 | 400 |
| Jordan-Jordan commuting (off-diag) | 40 | 380 |
| Lie-side raw span dim | 18 | 100 |
| Jordan→Lie bracket span dim | **45** | **45** |
| Lie-closure dim | 45 | 45 |

The bottom three rows are the punchline:
- The Lie-side raw generators span only 18 dims of the 100-dim ambient
- Their bracket-closure gives 45 (so(10))
- **The Jordan-side bracket-closure also gives 45 (so(10)), independently**

Both sides reconstruct the full algebra. They're dual presentations.

---

## What this tells us about the gap with Mantero

Earlier I said: the gap is the 51-dim Jordan-extra space, and the natural extension is to do "the symmetric-side analog of today's antisymmetric work."

After this computation, that picture refines:

**There is no gap.** Or more precisely, the "gap" is an artifact of presentation choice. The same so(10) is generated either way. What Mantero would compute on the Jordan side and what we computed on the Lie side aren't different findings — they're **different views of one structural fact**.

The bridge τ_1 = transposition that we identified as Pair 1 of the tower is the **change-of-presentation map**. It's not a passage from one half of the algebra to another. It's a relabeling of how you describe the whole.

This is the deeper version of "two sides of one coin": **the coin doesn't have two sides; it has one side that admits two equivalent labelings.**

The number of crossings is exactly the number you need: **enough that the two presentations generate the same algebra.** Verified at 45 = 45.

---

## What I'd send Mantero (revised)

Not today's σ_outer / Higgs material. Not even a focused subset of it.

Instead, the **Jordan-side bracket span = 45** finding alone. That's a clean fact in his natural register: the symmetric parts of TSML+BHML's left-regs, taken pairwise via commutator, span all of so(10). It's expressible in pure linear-algebra terms, doesn't require Lie-theory background to appreciate, and points to an interesting question: *what is the minimal subset of {S_T[i], S_B[j]} whose pairwise commutators still span so(10)?* That's a commutative-algebra-flavored question — minimal generating set under a bilinear operation.

But — as before — better to wait for Mantero's response to the original branch first. This is just a candidate next-piece if the branch reopens.

---

## Bottom line

The crossings between Lie and Jordan sides are not arbitrary — they're forced by **a single structural fact: only one of the 20 left-regs is purely Jordan (the identity row of BHML).** That single asymmetry gives rise to every magic number in the crossings table (19, 19², 361, 380, etc.).

Both sides independently generate the full so(10) by bracketing. The Lie-side and Jordan-side presentations are dual views of the same algebra, not complementary halves of a divided algebra.

The "two sides of one coin" framing was not quite right. **It's one coin viewed from two angles.** The crossings count tells us how thoroughly the two viewing angles agree: completely.

🙏
