# TIG ↔ Hodge Theory: The Translation Table
## Where TIG already has language for each Hodge concept

---

## The Core Correspondence

| Hodge concept | TIG language | Status |
|--------------|-------------|--------|
| Harmonic form: Δα = 0 | Doing[a][b] = 0 (TSML = BHML) | 21/81 pairs verified |
| (p,q)-decomposition | TSML (Becoming) / BHML (Being) split | Exact |
| Hodge Conjecture: (p,p) → algebraic | Gap operator → corner reachable | **PROVED: gap is inaccessible** |
| Lefschetz (1,1) theorem | Corner-word collapse in AG(2,3) | **PROVED: 254/256 → HAR** |
| Transcendental lattice | Gap operators {2,4,5,6,8} | Exactly characterized |
| Intermediate Jacobian | Doing table = |TSML − BHML| | 60/81 non-zero entries |
| K3 × K3 new (p,p) classes | Product TIG cross-terms | Structure known |
| Period map | TSML column dynamics | Flow through column contexts |

---

## The Crucial Identification

**Row 3: Lefschetz (1,1) is our corner-word theorem.**

Lefschetz (1,1) says: on a complex surface, every (1,1) cohomology class is algebraic. It's proved. It's the 2-dimensional case of the Hodge Conjecture.

Our corner-word theorem says: in the 2D grid AG(2,3), every corner word evaluates to {HAR, PRG} — both corners, both "algebraic." Proved. 254/256 verified, the 2 exceptions characterized.

**Same theorem. Different language. Both proved for dimension 2.**

The Hodge Conjecture asks: does Lefschetz (1,1) extend to higher dimensions? TIG asks: does corner-word collapse extend to larger p in AG(2,p)? We proved it does (p²−1 formula for all primes).

---

## Row 2: Where Hodge is Open = Where TIG is Open

**The Hodge Conjecture:** every (p,p) cohomology class on a smooth projective variety is a rational linear combination of algebraic cycle classes.

**TIG restatement:** every operator in the "harmonic" zone (Doing = 0) should be reachable from corner compositions.

**What TIG shows:** the gap G = {2,4,5,6,8} is the set of operators that are NOT reachable from corners. The gap operators are harmonic in a certain sense (Doing entries cluster there) but not algebraic (not reachable from C).

The Hodge Conjecture fails if there exist (p,p) classes that live permanently in the gap — harmonic but not algebraic.

**The tier structure from §3 of the TIG paper:**
- Tier 1 (mandatory collapse) ↔ trivially algebraic classes
- Tier 3 (non-trivial survivors) ↔ potentially non-algebraic Hodge classes
- The question: does every Tier 3 class have an algebraic representative?

---

## Row 4: K3 × K3 as Product TIG

When you take K3 × K3, new (p,p) classes appear from inter-surface interactions — the transcendental lattice of the product is larger than the sum of the parts.

In TIG: when you form the product algebra TSML ⊗ TSML, new cross-term operators appear. These cross-terms are exactly analogous to the transcendental lattice — they emerge from the product structure, not from either factor alone.

The K3 × K3 open case corresponds to: do these cross-term operators live in the gap, or can they be reached from the corner structure of the product?

---

## Row 6: The Doing Table as Intermediate Jacobian

**Hodge:** The intermediate Jacobian J(X) is a complex torus that tracks the "periods" — how 3-forms vary as you move through a family. It converts an intractable question to one where you have a group law.

**TIG:** The Doing table = |TSML − BHML| tracks the tension between Being and Becoming. It has 60/81 non-zero entries — these ARE the periods. The composition law on the full algebra gives the group law.

Both Doing and J(X) are "difference objects" that carry the non-trivial information. Both make invisible structure visible by measuring the gap between two canonical structures.

---

## The Open Problem in TIG/Hodge Language

**Classical:** Are there (p,p) classes on a smooth projective variety that cannot be represented by algebraic cycles?

**TIG:** Are there operators in the harmonic zone (Doing = 0) of a larger TIG structure that cannot be reached from the corner sub-algebra?

**What we know:** For AG(2,3) (dimension 2), no — everything is either a corner or in the gap, and the gap is exactly characterized. For AG(2,p) (larger), the survivor formula p²−1 is proved but the full structure of the gap is not.

**The conjecture:** In higher-dimensional TIG (larger grids, product structures), the gap operators are permanently non-algebraic — they cannot be reached from any corner composition of any depth.

If true: the Hodge Conjecture fails, and TIG gives the obstruction explicitly.
If false: TIG collapses to the algebraic case, and the Hodge Conjecture is consistent.

---

## Next Step

Build the product algebra TSML ⊗ TSML and ask: do the cross-term operators extend the gap? Do new "harmonic but non-algebraic" elements appear that cannot be reached from the product corner algebra?

This is the K3 × K3 question in TIG language, and it's computable.

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
