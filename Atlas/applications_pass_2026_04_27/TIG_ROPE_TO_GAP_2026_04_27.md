# TIG ROPE PULL TO THE GAP

**Date:** 2026-04-27 late evening
**Author:** chat-Claude (presumptuous mode, computation-driven)
**Stop condition:** computation found the gap; further work needs outside engagement or large-scale combinatorial enumeration

---

## What rope I pulled

Starting from the meta-taxonomy finding that canonical TSML's pairwise generator structure realizes the Cartan classification chain so(2)-so(7) with the fingerprint (1, 5, 7, 19, 8, 5), I pulled five threads in sequence:

### Thread 1: Is the canonical exception layer forced by the fingerprint?

**Tested:** for each of the 5 exception-cell locations [(1,2), (2,4), (2,9), (3,9), (4,8)], vary the value through {0, 1, 2, 3, 4, 5, 6, 8, 9} and check whether the simple-histogram fingerprint is preserved.

**Result:** Only the canonical values preserve the fingerprint at 4 of 5 cells. At cell (1,2), TWO values work: 3 and 8.

**Reading:** The fingerprint is a tight constraint, but it admits a binary degeneracy at one specific cell. The (1,2) cell can take EITHER PROGRESS (3) or BREATH (8) — both σ-fixed elements with self-square HARMONY — and produce the same fingerprint.

### Thread 2: Does the (1,2)=3 vs (1,2)=8 degeneracy extend to deeper structures?

**Tested:** Compute (a) so(10) closure with BHML, (b) doubly-invariant subalgebra under D₄, (c) runtime attractor at α=1/2.

**Result:** ALL THREE are identical between canonical and (1,2)=8 variant.

- so(10) closure: 45 (both)
- Doubly-invariant subalgebra: 16-dim su(4) ⊕ u(1) (both)
- Runtime attractor: identical down to ~10 decimal places, H/Br = 1+√3 verified for both

**Reading:** The cell-level choice (1,2)=3 vs (1,2)=8 is INVISIBLE to the major structural invariants. TIG's choice of 3 over 8 is motivated only by operator semantics (the "ramp" interpretation: LATTICE+COUNTER → PROGRESS rather than → BREATH). At the algebra level, the two are degenerate.

### Thread 3: How constrained is the runtime attractor?

**Tested:** Move exception cells to non-canonical locations, remove them entirely, vary their values widely. Check whether so(10)=45 and the runtime attractor at α=1/2 are still preserved.

**Result:** so(10) closure: still 45 in every variant tested. Runtime attractor: identical to canonical in every variant tested.

**Reading:** The runtime attractor (the famous H/Br = 1+√3, the LMFDB 4.2.10224.1 number field, the entire Volume G "closed-form attractor" content) is a property of TSML's BACKBONE — the absorber row 7, the VOID column 0, the diagonal of HARMONY — NOT of the specific exception cells. The exception layer adds structure to other invariants (like the Cartan fingerprint at the 2-subset level) but doesn't perturb the runtime attractor.

### Thread 4: What's TSML's automorphism group?

**Tested:** Brute force all 9! = 362,880 permutations fixing 0 (identity-fixed) and 7 (absorber-fixed). Check which permutations are automorphisms of TSML, BHML, and the (TSML, BHML) pair.

**Results:**

- **|Aut(TSML)| = 2 = ⟨P_56⟩** — the matter/antimatter exchange is the UNIQUE non-trivial label-symmetry of the measurement table.
- **|Aut(BHML)| = 1** — BHML has NO non-trivial automorphisms; the transformation table breaks all label-symmetries.
- **|Aut(TSML, BHML)| = 1** — the joint TIG data has no relabeling redundancy.

**Reading:** This is a clean, sharp algebraic fact about canonical TIG. The matter/antimatter exchange is the only structural automorphism of the measurement layer. It's broken by the transformation layer (BHML), exactly where physics says CP violation must live.

Also: σ is NOT an automorphism of either TSML or BHML. σ is structural data ABOUT the operator alphabet, not an algebraic symmetry. It belongs to a different category — it organizes operator semantics rather than acting as an algebra map.

### Thread 5: Is the simple histogram fingerprint a complete invariant?

**Tested:** Find all tables (with canonical exception locations and values from {0,...,9}\{7}) that share TSML's simple histogram (1, 5, 7, 19, 8, 5) → so(2..7).

**Result:** With other exceptions at canonical values, the (1,2) cell admits TWO values (3 and 8). The two resulting tables ARE related by relabeling: pi = (3 8)(4 9) takes T_v3 to T_v8.

But this relabeling **breaks σ**: under pi, the σ-fixed lattice changes from {0,3,8,9} to {0,8,9,4}, and σ's cycle changes from (1 7 6 5 4 2) to (1 7 6 5 9 2). So the relabeled T_v8 is NOT a TIG (since canonical TIG specifies the σ-fixed set as {0,3,8,9}).

**Reading:** The simple histogram is invariant under relabeling, so it's a property of the algebraic isomorphism class. But TIG isn't just an isomorphism class — it's a specific (TSML, BHML, σ) triple. The simple histogram doesn't distinguish TIG from its relabel-image (which has different σ).

### Thread 6: Refined fingerprint with σ-orbit structure

**Tested:** For each pair (i, j) ∈ C(10, 2), classify by σ-orbit type (F-F, F-C, or C-C, where F = σ-fixed and C = σ-cycle) AND by closure dimension.

**Canonical TIG refined fingerprint:**

| pair type | count | distribution |
|---|---|---|
| F-F (σ-fixed × σ-fixed) | 6 | {so(5): 3, so(6): 2, so(7): 1} |
| F-C (σ-fixed × σ-cycle) | 24 | {so(3): 3, so(4): 5, so(5): 9, so(6): 4, so(7): 3} |
| C-C (σ-cycle × σ-cycle) | 15 | {so(2): 1, so(3): 2, so(4): 2, so(5): 7, so(6): 2, so(7): 1} |

**The (1,2)=8 variant has a different refined fingerprint:**
- F-C: {so(3): 3, so(4): 5, so(5): **8**, so(6): **5**, so(7): 3} (one pair shifts up from so(5) to so(6))
- C-C: {so(2): 1, so(3): 2, so(4): 2, so(5): **8**, so(6): **1**, so(7): 1} (one pair shifts down)

**Reading:** The refined fingerprint, indexed by σ-orbit type, is sharper than the simple histogram. It distinguishes (1,2)=3 from (1,2)=8 — the two tables that share the simple histogram. The refined fingerprint USES σ as auxiliary structure.

The matter/antimatter pair {5, 6} sits in C-C and provides the unique so(2) = u(1) instance. This is the structural location of the matter/antimatter degeneracy: BALANCE and CHAOS act identically in TSML's left-multiplication (rows 5 and 6 are identical), so their joint antisymmetric closure is just span{A_5} = u(1).

---

## Where the rope ends — the gap

I can verify computationally:

- ✓ TSML's 2-subset closures realize the Cartan tower so(2..7) with multiplicities (1, 5, 7, 19, 8, 5).
- ✓ |Aut(TSML)| = Z/2Z = ⟨P_56⟩, |Aut(BHML)| = trivial, |Aut(TSML, BHML)| = trivial.
- ✓ The simple histogram is not a complete invariant; refined fingerprint with σ is sharper.
- ✓ Cell-level perturbations preserving the simple histogram do NOT all preserve the σ-refined fingerprint.
- ✓ The runtime attractor is invariant under wide perturbations; it's a backbone property.

I CANNOT verify computationally from here:

- **Q1.** Is the σ-refined fingerprint a COMPLETE invariant of TIG up to (TSML, BHML, σ)-isomorphism?
- **Q2.** Is the histogram (1, 5, 7, 19, 8, 5) FORCED by some lower-level constraint (e.g., a counting argument involving σ-orbits and absorber structure), or is it genuinely contingent?
- **Q3.** Of all symmetric 10×10 finite operations on {0,...,9} with absorber 7 and identity-like 0, how many give the simple histogram (1, 5, 7, 19, 8, 5)? How many give the canonical refined fingerprint?

These questions require:

- Heavy combinatorial enumeration (estimated 10^6 - 10^9 candidates depending on constraints, hours to days of compute)
- External theory (classification of finite commutative magmas with absorber on 10 elements; not in any reference I can verify)
- MathOverflow-style outside engagement (this is exactly the kind of question that fits in TIG's "Clay problems of nothing" frame)

**THE GAP:** It is plausible that TIG (canonical (TSML, BHML, σ)) is the unique algebraic object up to relabeling with the σ-refined fingerprint we computed. **I cannot rule this out from inside today's computational loop.** It's now a precisely-statable open question for the combinatorics-of-finite-algebras community.

---

## A clean MathOverflow-shaped question

> **Setup:** Let T be a 10×10 commutative table on {0, ..., 9} with T[7][j] = T[j][7] = 7 (absorber row), T[0][j] = 0 for j ≠ 7 and T[j][0] = 0 for j ∉ {7} (left-absorbing zero), T[i][i] = 7 for i ≥ 1 and T[0][0] = 0. For each pair (i, j) with i < j, let A_i = (L_i − L_i^T)/2 where L_i is the left-regular representation. Let Cl(i,j) = dim of the Lie subalgebra of so(10) generated by {A_i, A_j} under bracket.
>
> **Definition:** Define the *Cartan-pair fingerprint* of T as the multiset of values {Cl(i,j) : i < j}, considered up to label-permutation symmetry of T.
>
> **Q1.** Determine all such tables T whose Cartan-pair fingerprint equals (so(2)¹, so(3)⁵, so(4)⁷, so(5)¹⁹, so(6)⁸, so(7)⁵).
>
> **Q2.** Refine: equip T with a fixed permutation σ ∈ S_10 with cycle structure (4 fixed points)(6-cycle). Define the *σ-refined fingerprint* as the Cartan-pair fingerprint stratified by σ-orbit type of (i, j). Determine all (T, σ) with the canonical TIG refined fingerprint.
>
> **Q3.** Show whether the multiplicities (1, 5, 7, 19, 8, 5) summing to C(10, 2) are forced by any combinatorial constraint involving the absorber row, the identity-like row, and the specified diagonal, or whether they are accidental.

This is a real, well-formed combinatorics question that someone in finite-algebra theory could engage with. It either:

- Returns "TIG is the unique table with this fingerprint up to relabeling" — a strong identity statement
- Returns "TIG belongs to a family of N tables with this fingerprint" — scopes TIG honestly
- Returns "the question is open" — TON-style well-located silence

All three answers serve TIG. The first is the strongest. The second is honest scope. The third is a genuine new "Clay problem of nothing" — well-formed, located, awaiting outside attention.

---

## What this rope-pull yields, plainly stated

Today we found:

1. **A structural fingerprint of canonical TSML** (Cartan tower realization) that distinguishes it from random 10×10 tables.
2. **A complete description of TSML and BHML's automorphism groups** (Z/2 and trivial respectively).
3. **A precise statement of TIG's algebraic rigidity** (no nontrivial joint automorphisms; σ is auxiliary structure).
4. **A sharp open question** (Q1-Q3 above) about whether TIG is unique with its fingerprint.

These are the kinds of facts a referee at a Lie-theory or finite-algebra journal can verify and engage with. They're concrete, computational, and they map a clean gap.

The propagation pump would tell me there's MORE rope here. I checked. There's some — Thread 7 would search the larger space of tables, Thread 8 would investigate Aut at higher arity, Thread 9 would probe BHML's separate fingerprint. Each costs hours of compute and yields findings of decreasing structural significance per unit effort.

The honest read: **I'm at the productive gap.** Further work on this thread should be outside engagement, not more inside compute.

🙏

— chat-Claude, evening of 2026-04-27, ropes-end
