# The Towered, Intertwined Structure — Verified Pieces and Honest Gaps

**Date:** 2026-04-25
**Script:** `compute_transitions.py`
**Status:** Pairs 1 and 2 verified. Pair 3 partially. Coupling matrix computed.

---

## What I had to abandon

The "three pairs stacked" picture from my last message was already too clean. The data forced corrections:

- **The "idempotents" of TIG aren't multiplication-idempotents.** T[i,i] = i only for i ∈ {0, 7}. The set {0, 3, 8, 9} called "idempotents" in userMemories are σ-fixed points, not e² = e. So what I labeled "Lattice" isn't sitting on Jordan/Lie — it's sitting *inside* Permutation.
- **Lie flow does not preserve the σ-fixed set.** Of all the flow operators acting on σ-fixed basis vectors, only one map (A_3 on e_9) stayed in the σ-fixed span. Every other action escaped. So Lattice and Lie genuinely tangle — they don't commute at all.

Both of those are intertwinings I had glossed over with the staircase metaphor.

## What actually verified

### Pair 1 (Lie ⇌ Jordan): the involution is transposition

τ_1(M) = M^T.

- Symmetric part (Jordan) is +1 eigenspace
- Antisymmetric part (Lie) is −1 eigenspace
- For TSML's L_i, both parts have nontrivial norm — Lie/Jordan ratio ranges around 0.5–1.5 across the 10 left-reps.
- Breaking element: the multiplication T itself. Without T, the Lie and Jordan halves are independent. With T, multiplying a symmetric and antisymmetric matrix produces something with both parts: `||sym(A_1 S_1)|| = nontrivial` and `||antisym(A_1 S_1)|| = nontrivial`. T is what couples the halves.

This is solid.

### Pair 2 (Clifford ⇌ Permutation): the involution is P_56-conjugation

τ_2(X) = P_56 X P_56^T on so(10).

- +1 eigenspace = 36 generators (so(9), centralizer of P_56) — Clifford-side
- −1 eigenspace = 9 generators — Permutation-side, the "vector that BHML adds"
- Total: 45 = dim so(10). Verified at machine precision.

Breaking element: σ (the larger 6-cycle permutation). Verified that σ does NOT commute with P_56 — the group they generate has order ≥ 270 (probably the dihedral D_5 or a Weyl-related extension).

This is solid.

### Pair 3 (Lattice ⇌ Operad): I do NOT have a clean involution

I sketched it conceptually (currying, arity exchange) but couldn't produce a matrix realization that swaps a Lattice subspace with an Operad subspace. **The honest answer: Pair 3 is not yet shown to be a (5↔6)-style swap.**

What the data DOES show:
- The σ-fixed set {0, 3, 8, 9} is genuinely structured — these are positions Lie flow can't trap inside their own span
- Arity-3 fuse is provably distinct from binary TSML (computed last sprint: TSML(TSML(3,4),7) = 7 ≠ fuse([3,4,7]) = 8)
- But these two facts don't combine into an involution

So either the tower has only two (5↔6)-style levels and a third level of a *different* structural type, or I need a more clever involution that I haven't found yet.

## The actual coupling matrix (what touches what)

Computing ||[X, Y]|| for representative elements of each DOF:

```
                    Lie        Jordan     P_56       σ          Lattice
Lie (A_1)           0.000      21.166     0.000      6.000      2.828
Jordan (S_1)        21.166     0.000      0.000      6.000      2.828
P_56                0.000      0.000      0.000      2.449      0.000
σ (perm)            6.000      6.000      2.449      0.000      0.000
Lattice (P_fixed)   2.828      2.828      0.000      0.000      0.000
```

This tells the actual story of what tangles with what:

### Strongest coupling: Lie ⇌ Jordan (||21.17||)

The two halves of the same product talk to each other most loudly. They are *most tangled* at Pair 1's level. This is consistent with their being the **two complementary halves of the multiplication itself** — they're forced to communicate.

### Zero coupling: P_56 with both Lie and Jordan

P_56 commutes with both A_1 and S_1. **TSML's flow operators and TSML's symmetric parts are both invariant under the 5↔6 swap.** This is the same fact we established earlier (TSML is P_56-invariant), but seen from the cross-DOF angle: the Lie/Jordan pair lives entirely *inside* the symmetric eigenspace of P_56. Pair 1 sits below Pair 2 because Pair 1's content is contained in Pair 2's +1 register.

### Non-zero coupling: σ touches everything

σ commutes with nothing — it tangles with Lie (||6||), Jordan (||6||), and even P_56 (||2.45||). σ is the most "mixing" element in the entire structure. It's the element that breaks Pair 2's symmetry, but it also disturbs Pair 1.

### Lattice (P_fixed) commutes with σ and P_56, tangles with Lie/Jordan

This is the surprising one. **The σ-fixed-point projector commutes exactly with both σ and P_56**, but does NOT commute with Lie or Jordan (||2.83|| each). In words: the discrete symmetries (σ, P_56) preserve the σ-fixed set by construction, but the multiplication-derived structures (Lie, Jordan) do not.

This is the actual intertwining you were pointing at. Lattice is *fixed by* permutation but *moved by* multiplication. So Lattice can't simply sit above Permutation — it's defined by Permutation but acted on by Lie/Jordan from below.

## The corrected picture

Forget the staircase. The structure is:

```
                  σ (the 6-cycle permutation)
                        breaks
                   /           \
            Pair 2 (P_56-symm)
            (Clifford ⇌ Permutation)
            36                     9
                        breaks
                   /           \
            Pair 1 (transpose-symm)
            (Lie ⇌ Jordan)
            antisym               sym
            both fixed by P_56    both fixed by P_56
            both tangled with Lattice
```

And **Lattice (σ-fixed set)** is not a third pair-level. It's a **transverse register** that:
- Lives in Pair 2's +1 eigenspace (commutes with P_56)
- Is fixed by σ (commutes with σ)
- Is moved by Pair 1's content (does NOT commute with Lie or Jordan)

Lattice cuts across the tower rather than sitting on top of it.

**Operad** I haven't placed cleanly yet. The arity-3 fuse is real and distinct from binary, but I don't have an involution that swaps it with Lattice. It might also be transverse, or it might live at a third level I haven't found.

## What's tangled, what's untanglable

**Tangled (verified):**
- Lie ⇌ Jordan (transpose, broken by T) — strongest tangle, ||21||
- Clifford ⇌ Permutation (P_56, broken by σ) — verified 36+9 split
- σ tangles with everything except itself (||6||, ||6||, ||2.45||)
- Lattice tangles with the multiplication side but not the permutation side

**Untanglable (verified):**
- Lie and P_56 commute exactly (TSML flow is P_56-invariant)
- Jordan and P_56 commute exactly (same reason)
- Lattice and σ commute exactly (Lattice IS the σ-fixed set, by construction)
- Lattice and P_56 commute exactly (P_56 is in σ's group, fixes σ-fixed)

**Open (not verified):**
- Where exactly Operad sits in this structure
- Whether Pair 3 has a real involution or whether the tower terminates at Pair 2 with Lattice and Operad both being transverse registers

## Honest summary

The tower has two clean (5↔6)-style pairs (Lie⇌Jordan, Clifford⇌Permutation), each with explicit involution and explicit breaking element. The arrangement is genuinely intertwined: each pair's invariance is broken by an element that comes from the level above (T breaks Pair 1's transpose-symm at the multiplication-data level; σ breaks Pair 2's P_56-symm at the larger-permutation level).

Lattice doesn't sit on top of Permutation — it's a transverse register that's preserved by Permutation and disturbed by multiplication.

Operad's structural placement is open.

The "three stacked pairs" picture I drew last message was too clean. The real picture has two pairs and at least one transverse register, with Operad as a loose end.

This is closer. There's still slack. The 5↔6 lesson — that the structure is intertwined, not stacked — applies, but I needed the data to show me how it actually intertwines rather than how I expected it to.

🙏
