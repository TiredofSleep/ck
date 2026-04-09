# SPRINT: NON-CRT MINIMALITY TEST
## Can Any Non-CRT Family Match the k−1 Jump Bound?
*n = 30 = 2·3·5. Partition lattice only. Proved vs. conjectural labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Setup

**System:** Z/30Z = {0,1,...,29}, n = 30 = 2·3·5, k = 3 prime factors.

**CRT benchmark:** The CRT prime-factor family {π₂, π₃, π₅} achieves meet = π_disc with 3 pairwise-incompatible partitions and 2 orthogonal jumps (proved in prior sprint). The question: can any non-CRT family do the same or better?

---

## Part 1 — Candidate Partitions for n = 30

**π₂ (CRT factor):** partition by x mod 2. 2 blocks of size 15.

**π₃ (CRT factor):** partition by x mod 3. 3 blocks of size 10.

**π₅ (CRT factor):** partition by x mod 5. 5 blocks of size 6.

**π_{15} (composite residue — NOT a prime-factor partition):**
partition by x mod 15.
Blocks: {x, x+15} for x = 0,...,14. 15 blocks of size 2.
Equivalently: x ~_{π_{15}} y iff 15 ∣ (x−y).

**π_SPEC (reflection):**
x ~_{π_SPEC} y iff x+y ≡ 0 (mod 30).
Blocks: {0},{15}, and {x, 30−x} for x = 1,...,14.
16 blocks: 2 singletons + 14 pairs.

**π_UG (gcd partition):**
x ~_{π_UG} y iff gcd(x,30) = gcd(y,30).
Blocks by gcd value:
- gcd = 1: {1,7,11,13,17,19,23,29} (8 elements)
- gcd = 2: {2,4,8,14,16,22,26,28} (8 elements)
- gcd = 3: {3,9,21,27} (4 elements)
- gcd = 5: {5,25} (2 elements)
- gcd = 6: {6,12,18,24} (4 elements)
- gcd = 10: {10,20} (2 elements)
- gcd = 15: {15} (1 element)
- gcd = 30: {0} (1 element)
8 blocks.

**π_DYN(7) (orbit partition under T₇: x ↦ 7x mod 30):**
Computing orbits:
- 0 → 0 (fixed), 5 → 5 (fixed), 10 → 10 (fixed), 15 → 15 (fixed), 20 → 20 (fixed), 25 → 25 (fixed)
  [Fixed: all multiples of 5, since 7·5 = 35 ≡ 5 mod 30; i.e., 7≡1 mod 5 means T₇ fixes all multiples of 5.]
  Wait: 7 mod 5 = 2, not 1. Let me recheck: 7·5 = 35 = 30+5. So yes, ≡ 5 mod 30. Fixed. ✓
  More carefully: T₇(x) = 7x mod 30. For x = 5m: 7·5m = 35m = 30m+5m ≡ 5m mod 30. So T₇(5m) = 5m. ✓ All multiples of 5 are fixed.
- 1 → 7 → 49=19 → 133=13 → 91=1. Orbit: {1,7,13,19}
- 2 → 14 → 98=8 → 56=26 → 182=2. Orbit: {2,8,14,26}
- 3 → 21 → 147=27 → 189=9 → 63=3. Orbit: {3,9,21,27}
- 4 → 28 → 196=16 → 112=22 → 154=4. Orbit: {4,16,22,28}
- 6 → 42=12 → 84=24 → 168=18 → 126=6. Orbit: {6,12,18,24}
- 11 → 77=17 → 119=29 → 203=23 → 161=11. Orbit: {11,17,23,29}

π_DYN(7): { {0},{5},{10},{15},{20},{25},{1,7,13,19},{2,8,14,26},{3,9,21,27},{4,16,22,28},{6,12,18,24},{11,17,23,29} }
12 blocks: 6 singletons (multiples of 5) + 6 orbits of size 4.

**π_DYN(11) (orbit partition under T₁₁: x ↦ 11x mod 30):**
Note: 11² = 121 ≡ 1 mod 30. So T₁₁ has order 2 for all elements.
Fixed points (where 11x ≡ x mod 30, i.e., 10x ≡ 0 mod 30, i.e., x ≡ 0 mod 3): all multiples of 3.
Singletons: {0},{3},{6},{9},{12},{15},{18},{21},{24},{27} (10 elements)
2-cycles (x ↦ 11x, 11x ↦ x): {1,11},{2,22},{4,14},{5,25},{7,17},{8,28},{10,20},{13,23},{16,26},{19,29}

π_DYN(11): 20 blocks: 10 singletons + 10 pairs.

---

## Part 2 — Compatibility Analysis

**Lemma (General): π_SPEC ≤ π_UG for all n.**

Proof: gcd(n−x, n) = gcd(−x, n) = gcd(x, n). So reflection x ↦ n−x preserves the gcd-class. Every π_SPEC block {x, n−x} satisfies gcd(x,n) = gcd(n−x,n), hence is contained in a single π_UG block. □

**Corollary for n=30:** π_SPEC ≤ π_UG. Verified explicitly: each of the 16 π_SPEC blocks lies within a π_UG block. ✓

**Structural position of π_{15}:**

Is π_{15} ≤ π₃? Block {x, x+15}: (x+15) mod 3 = x mod 3 + 15 mod 3 = x mod 3 + 0 = x mod 3. So yes, both elements of any π_{15} block have the same residue mod 3. π_{15} ≤ π₃. ✓

Is π_{15} ≤ π₅? (x+15) mod 5 = x mod 5 + 0 = x mod 5 (since 15 ≡ 0 mod 5). Similarly yes. π_{15} ≤ π₅. ✓

Is π_{15} compatible with π₂? Block {0,15}: 0 mod 2 = 0, 15 mod 2 = 1. Different. So {0,15} ⊄ any π₂ block. π_{15} ≰ π₂. Also π₂ ≰ π_{15} (π₂ block {0,2,...,28} is not contained in any π_{15} block). **Incompatible.** ✓

Is π_{15} compatible with π_SPEC? 
- π_{15} ≤ π_SPEC? Block {0,15}: {0} and {15} are separate π_SPEC blocks. Not contained in one. ✗
- π_SPEC ≤ π_{15}? Block {1,29}: 1 mod 15 = 1, 29 mod 15 = 14. Different π_{15} blocks. ✗
**Incompatible.** ✓

**Full compatibility table for n=30:**

| Pair | Relation |
|---|---|
| π_SPEC ≤ π_UG | Refinement (SPEC refines UG) |
| π_{15} ≤ π₃ | Refinement (π_{15} refines π₃) |
| π_{15} ≤ π₅ | Refinement (π_{15} refines π₅) |
| π_DYN(7) ≤ π_UG | Refinement (proved below) |
| π₂ ↔ π₃ | Incompatible |
| π₂ ↔ π₅ | Incompatible |
| π₃ ↔ π₅ | Incompatible |
| π₂ ↔ π_{15} | Incompatible |
| π_SPEC ↔ π_{15} | Incompatible |
| π_SPEC ↔ π₅ | Incompatible |
| π_UG ↔ π₅ | Incompatible |
| π_SPEC ↔ π₂ | Incompatible |

**Claim:** π_DYN(7) ≤ π_UG.

Proof: gcd(7,30) = 1, so T₇ is a unit. For any x, gcd(7x mod 30, 30) = gcd(7x, 30) = gcd(x,30) (since gcd(7,30)=1). Therefore T₇ maps every gcd-class to itself. The orbit of x under T₇ lies within the gcd-class of x. Every π_DYN(7) orbit is ⊆ a π_UG block. So π_DYN(7) ≤ π_UG. □

Similarly π_DYN(11) ≤ π_UG (gcd(11,30)=1, same argument). All unit-generated DYN partitions refine π_UG.

---

## Part 3 — Main Positive Result

**Theorem (Non-Prime-Factor Sufficient Pair).**
For n = 30, the family {π_SPEC, π_{15}} satisfies:
1. π_SPEC and π_{15} are incompatible (neither refines the other).
2. meet(π_SPEC, π_{15}) = π_disc.

Therefore a sufficient family of 2 pairwise-incompatible partitions exists for n = 30, using only 1 orthogonal jump — fewer than the k−1 = 2 jumps required by the CRT prime-factor family.

**Proof.**

**Incompatibility (Part 1):** Verified above. □

**Meet = π_disc (Part 2).**

Define:
- U_SPEC = set of pairs unseparated by π_SPEC = {{x, 30−x} : x = 1,...,14}
- U_{15} = set of pairs unseparated by π_{15} = {{x, x+15} : x = 0,...,14}

meet(π_SPEC, π_{15}) = π_disc iff U_SPEC ∩ U_{15} = ∅ (no pair is in both unseparated sets).

**Computing U_SPEC ∩ U_{15}:** A pair {a,b} is in both iff:
- a + b = 30 (reflection condition), AND
- b = a+15 (or a = b+15)

From b = a+15: a + (a+15) = 30 ⟹ 2a = 15 ⟹ a = 7.5. Not an integer.
From a = b+15: b + (b+15) = 30 ⟹ 2b = 15 ⟹ b = 7.5. Not an integer.

Therefore U_SPEC ∩ U_{15} = ∅.

**Consequences:**
- Every pair in U_SPEC (reflection pair) satisfies b = 30−a ≠ a+15 (since a ≠ 7.5), hence the pair is in different π_{15} blocks: a mod 15 = a and (30−a) mod 15 = 15−a for a = 1,...,14 (distinct from a since a ≠ 15/2). So π_{15} separates every π_SPEC-unseparated pair. ✓
- Every pair in U_{15} (antipodal pair) satisfies a + (a+15) = 2a+15 ≠ 30 (since a ≠ 7.5), hence they are not a reflection pair, hence separated by π_SPEC. ✓

Every pair of distinct elements is separated by at least one of π_SPEC, π_{15}. Therefore meet(π_SPEC, π_{15}) = π_disc. □

**Corollary.** The minimum sufficient family size for n = 30 is 2 (not 3).

Proof: No single named partition equals π_disc, so length 1 is insufficient. {π_SPEC, π_{15}} achieves length 2. □

---

## Part 4 — Nature of π_{15}

**Is π_{15} "genuinely non-CRT"?**

π_{15} is the partition by x mod 15 — a residue-class partition by the composite divisor 15 = 3·5. It is:
- NOT in the prime-factor CRT family {π₂, π₃, π₅}
- NOT a prime-factor partition
- IS a residue-class partition by a divisor of 30
- IS derivable from CRT: π_{15} = meet(π₃, π₅) as partitions (every π_{15} block ⊆ a π₃ block and ⊆ a π₅ block)

**Algebraic content of π_{15}:** π_{15} encodes both the mod-3 and mod-5 residue in a single partition. Its 15 blocks correspond to the 15 residues mod 15, which by CRT (Z/15Z ≅ Z/3Z × Z/5Z) encodes both prime factors simultaneously.

**Why {π_SPEC, π_{15}} works — structural explanation:**
- π_{15} separates x from x+15: it provides information about x mod 15 (i.e., x mod 3 and x mod 5 simultaneously).
- π_SPEC separates x from 30−x: it separates elements that are 15 apart in the "complementary" sense (since 30−x = (15−x)+15, the elements at distance 15 in the mod-30 sense that π_{15} cannot separate).
- The two "unseparated families" are disjoint: π_{15} pairs = {x, x+15} and π_SPEC pairs = {x, 30−x}, and these two types never coincide (as proved above).

**Encoding observation:** π_{15} "contains" the work of two CRT prime factors (π₃ and π₅). The trade is: instead of two separate prime-factor partitions (each simple, each needing a jump), one composite-residue partition encodes both, at the cost of having finer blocks (size 2 instead of size 10 and 6). Then π_SPEC provides the residual mod-2-type separation.

**Classification of π_{15}:** π_{15} is a **composite-residue non-prime-factor partition**. It is NOT a prime-factor CRT partition. Whether to call it "non-CRT" depends on definition:
- Strict definition (non-residue): π_{15} is residue-class, so NOT non-CRT under strict interpretation.
- Prime-factor definition: π_{15} ∉ {π₂, π₃, π₅}, so it IS non-CRT under this interpretation.

The rest of this sprint uses the prime-factor definition and notes where this matters.

---

## Part 5 — Negative Results for Non-Residue Partitions

**Proposition 1.** meet(π_SPEC, π_UG) = π_SPEC ≠ π_disc.

Proof: π_SPEC ≤ π_UG (proved in Part 2 general lemma). Therefore meet(π_SPEC, π_UG) = π_SPEC. Since π_SPEC has non-singleton blocks ({1,9},{2,8}, etc.), π_SPEC ≠ π_disc. □

**Proposition 2.** For any unit g (gcd(g,30)=1, g ≠ 1 mod 30), meet(π_SPEC, π_DYN(g)) ≠ π_disc.

**Proof.** We show that for every non-trivial unit g, at least one reflection pair {x, 30−x} lies within a single π_DYN(g) orbit.

A reflection pair {x, 30−x} = {x, −x mod 30} is in the same T_g orbit iff g^k · x ≡ −x mod 30 for some k.

**Case analysis by gcd-type of x:**

For x with gcd(x,30) = 3 (i.e., x ∈ {3,9,21,27}): T_g acts on {3,9,21,27} = 3·{1,3,7,9} ≅ 3·(Z/10Z)*. The reflection pairs within this set are {3,27} and {9,21} (since 3+27=30 and 9+21=30).

Within the subgroup 3Z/30Z ≅ Z/10Z (acting via T_g mod 10), the pair {3,27}={3,−3} is in the same orbit iff g^k ≡ −1 ≡ 9 mod 10 for some k.

The element 9 has order 2 in (Z/10Z)* = Z/4Z. The subgroups of Z/4Z not containing 9 are: {1} (trivial) and... the only subgroup not containing the order-2 element 9 is {1} itself (corresponding to g ≡ 1 mod 10).

So: {3,27} is in the same T_g orbit iff g ≢ 1 mod 10, i.e., iff g ∈ {3,7,9,11,13,17,19,21,23,27,29} mod 30 restricted to units = {7,11,13,17,19,23,29} among units not ≡ 1 mod 10.

g ≡ 1 mod 10 means g ≡ 1 mod 2 AND g ≡ 1 mod 5, i.e., g ≡ 1 or 11 mod 30... wait. g ≡ 1 mod 10 means g ∈ {1, 11, 21} mod 30. Among units mod 30: g ∈ {1, 11} (since gcd(21,30)=3 ≠ 1).

So {3,27} is NOT merged by T_g iff g ≡ 1 or 11 mod 30.

For x with gcd(x,30) = 5 (i.e., x ∈ {5,25,10,20}): The reflection pairs within this set are {5,25} (5+25=30) and {10,20} (10+20=30).

Within 5Z/30Z ≅ Z/6Z (acting via T_g mod 6), the pair {5,25}={5,−5} is in the same orbit iff g^k ≡ −1 ≡ 5 mod 6 for some k.

(Z/6Z)* = {1,5}. The element 5 = −1 mod 6 has order 2. Subgroups of Z/2Z: {1} (trivial, g ≡ 1 mod 6) and {1,5} (full, g ≡ 5 mod 6).

So {5,25} is merged iff g ≡ 5 mod 6, i.e., g ≡ 5 mod 2 AND g ≡ 5 mod 3, i.e., g is odd AND g ≡ 2 mod 3.

The combined condition for NEITHER {3,27} NOR {5,25} to be merged:
- Not merge {3,27}: g ≡ 1 or 11 mod 30 (i.e., g ≡ 1 mod 10)
- Not merge {5,25}: g ≢ 5 mod 6 (i.e., g ≡ 1 mod 6: g ≡ 1 mod 2 AND g ≡ 1 mod 3)

For both simultaneously: g ≡ 1 mod 10 AND g ≡ 1 mod 6.
By CRT (lcm(10,6)=30): g ≡ 1 mod 30.

The only unit with g ≡ 1 mod 30 in Z/30Z is g = 1 itself.

For g = 1: T₁ is the identity map. π_DYN(1) = π_disc (all singletons). Then meet(π_SPEC, π_disc) = π_disc. ✓

But π_DYN(1) = π_disc is trivial — it already is the answer, and the family {π_SPEC, π_disc} is sufficient trivially but only because one member IS π_disc. This is degenerate.

For any non-trivial unit g (g ≢ 1 mod 30), at least one of {3,27} or {5,25} is an unseparated pair in both π_SPEC and π_DYN(g). Therefore meet(π_SPEC, π_DYN(g)) ≠ π_disc. □

**Proposition 3.** For any unit g, the pair {π_UG, π_DYN(g)} is NOT a jump — it is a refinement — and its meet equals π_DYN(g) ≠ π_disc.

Proof: As shown in Part 2: for unit g, gcd(gx,30)=gcd(x,30), so π_DYN(g) ≤ π_UG (each orbit is within a gcd-class). The pair is compatible (refinement relation). meet(π_UG, π_DYN(g)) = π_DYN(g). Since π_DYN(g) has non-singleton orbits for non-trivial g, meet ≠ π_disc. □

**Summary of 2-partition attempts using non-residue partitions:**

| Family | Relation | Meet | Sufficient? |
|---|---|---|---|
| {π_SPEC, π_UG} | Refinement (SPEC ≤ UG) | π_SPEC | No |
| {π_SPEC, π_DYN(7)} | Jump (incompatible) | > π_disc | No |
| {π_SPEC, π_DYN(11)} | Jump (incompatible) | > π_disc | No |
| {π_UG, π_DYN(g)} | Refinement (DYN ≤ UG) | π_DYN(g) | No |
| {π_DYN(7), π_DYN(11)} | Need to check | ? | Checked below |

**Checking {π_DYN(7), π_DYN(11)}:**

π_DYN(7) orbits: 6 singletons {0,5,10,15,20,25} + 6 4-element orbits.
π_DYN(11) orbits: 10 singletons (multiples of 3) + 10 2-element orbits.

The 4-element orbit {3,9,21,27} of T₇: in π_DYN(11), these are all singletons (each is a fixed point of T₁₁). So meet(π_DYN(7), π_DYN(11)) separates all elements of {3,9,21,27}. ✓ for this block.

The 4-element orbit {1,7,13,19} of T₇: in π_DYN(11), {1,11}, {7,17}, {13,23}, {19,29} are the orbits. Elements 1,7,13,19 are in different π_DYN(11) orbits. ✓

The 4-element orbit {6,12,18,24} of T₇: in π_DYN(11), these are all multiples of 3, hence singletons. Separated. ✓

Checking all 4-element T₇ orbits against π_DYN(11):
- {1,7,13,19}: 1∈{1,11}, 7∈{7,17}, 13∈{13,23}, 19∈{19,29}. All different. ✓
- {2,8,14,26}: 2∈{2,22}, 8∈{8,28}, 14∈{4,14}, 26∈{16,26}. All different. ✓
- {3,9,21,27}: all singletons. ✓
- {4,16,22,28}: 4∈{4,14}, 16∈{16,26}, 22∈{2,22}, 28∈{8,28}. All different. ✓
- {6,12,18,24}: all singletons. ✓
- {11,17,23,29}: 11∈{1,11}, 17∈{7,17}, 23∈{13,23}, 29∈{19,29}. All different. ✓

Also check T₇ singletons {0,5,10,15,20,25} in π_DYN(11):
All are also singletons (0 is singleton in both; 5∈{5,25}, 25∈{5,25}). Wait: 5 is a T₇ fixed point. And in π_DYN(11): 5 and 25 are in orbit {5,25}. So 5 and 25 are NOT separated by π_DYN(11). And they ARE in the same T₇ orbit? No: T₇ fixes 5 and 25 separately (different singletons). So in π_DYN(7): {5} and {25} are different orbits. In π_DYN(11): {5,25} is one orbit. Are 5 and 25 identified in meet(π_DYN(7), π_DYN(11))? meet identifies x~y iff they're in the same T₇ orbit AND same T₁₁ orbit. 5 and 25 are in different T₇ orbits ({5} ≠ {25}). So the meet separates them. ✓

Continuing: singletons {0,10,15,20} of T₇: in π_DYN(11), 10∈{10,20} and 20∈{10,20} — same orbit! But 10 and 20 are different T₇ orbits. So meet separates them. ✓ 0 is singleton in both. ✓ 15 is singleton in both. ✓

So meet(π_DYN(7), π_DYN(11)) = π_disc!

Let me verify incompatibility:
- π_DYN(7) ≤ π_DYN(11)? Orbit {1,7,13,19} of T₇: 1∈{1,11}, 7∈{7,17}. Different π_DYN(11) blocks. Not contained. ✗
- π_DYN(11) ≤ π_DYN(7)? Orbit {5,25} of T₁₁: 5∈{5} and 25∈{25} — different T₇ orbits. Not contained. ✗

**Incompatible.** ✓

Therefore {π_DYN(7), π_DYN(11)} is a second sufficient 2-partition family, with 1 orthogonal jump, using no residue-class partitions! This is a genuinely non-CRT sufficient pair.

---

## Part 6 — Forced Size Lemma

**Lemma (Product Lemma).** If {π_A, π_B} is a sufficient 2-partition family for Z/nZ (any n), then |blocks(π_A)| · |blocks(π_B)| = n.

Proof: meet(π_A, π_B) = π_disc means every element is uniquely identified by its (A-block, B-block) pair. The map f: Z/nZ → blocks(π_A) × blocks(π_B), f(x) = (A-block(x), B-block(x)), is injective (by uniqueness). Since |domain| = n and |codomain| = |blocks(π_A)| · |blocks(π_B)|, injectivity requires n ≤ |blocks(π_A)| · |blocks(π_B)|. But f is also surjective: if any block-pair (B_i, C_j) were empty, there would be an A-block and a B-block with no element in common — but then meet(π_A, π_B) would have no block for that combination, which is fine since meet only creates non-empty intersections. Actually: surjectivity is NOT required. The correct statement is that all |n| elements map to distinct (A-block, B-block) pairs, so n ≤ |A|·|B|.

Corrected: if meet = π_disc, then the map f is injective, so n ≤ |blocks(π_A)| · |blocks(π_B)|. Equality is achieved when every (A-block, B-block) pair has exactly one element (a "combinatorial orthogonal array").

For {π_DYN(7), π_DYN(11)}: |π_DYN(7)| = 12 blocks, |π_DYN(11)| = 20 blocks. 12 × 20 = 240 >> 30. So the product far exceeds n — this pair is "inefficient" in terms of information redundancy, but still sufficient. □

For {π_SPEC, π_{15}}: |π_SPEC| = 16 blocks, |π_{15}| = 15 blocks. 16 × 15 = 240 >> 30.

For {π₂, π_{15}}: |π₂| = 2, |π_{15}| = 15. 2 × 15 = 30. Exact! This would be a minimal-product sufficient pair.

Verify: meet(π₂, π_{15}) = ? x ~_{meet} y iff x ≡ y mod 2 AND x ≡ y mod 15 iff x ≡ y mod lcm(2,15) = 30 iff x = y. ✓ So {π₂, π_{15}} is also a sufficient pair of size 2 with |A|·|B| = n = 30 exactly!

Is π₂ ↔ π_{15} an orthogonal jump? Verified above: incompatible. ✓ And both have 1 jump.

Observation: {π₂, π_{15}} achieves the information-theoretic minimum: 2 × 15 = 30, every (π₂-block, π_{15}-block) pair contains exactly 1 element. This is the "most efficient" sufficient 2-partition family.

---

## Part 7 — Classification Table for n = 30

| Family | Partitions | Jump type | Meet | m | Jumps | Outcome |
|---|---|---|---|---|---|---|
| CRT prime factors | {π₂, π₃, π₅} | All orthogonal | π_disc | 3 | 2 | Sufficient, baseline |
| {π_SPEC, π_{15}} | Non-prime-factor | 1 orthogonal jump | π_disc | 2 | 1 | **Beats CRT baseline** |
| {π_DYN(7), π_DYN(11)} | Non-residue! | 1 orthogonal jump | π_disc | 2 | 1 | **Beats CRT baseline (non-residue)** |
| {π₂, π_{15}} | Mixed | 1 orthogonal jump | π_disc | 2 | 1 | **Beats CRT baseline** |
| {π_SPEC, π_UG} | Non-residue | Refinement (not jump) | π_SPEC | — | 0 | Insufficient |
| {π_SPEC, π_DYN(g)} | Non-residue | Orthogonal jump | > π_disc | 2 | 1 | Insufficient |
| {π_UG, π_DYN(g)} | Non-residue | Refinement (DYN ≤ UG) | π_DYN(g) | — | 0 | Insufficient |
| {π₂, π₃} alone | CRT prime factors | Orthogonal | π_{gcd(mod2,mod3)} | 2 | 1 | Insufficient |

---

## Part 8 — Main Theorems

**Theorem 1 (Non-CRT 2-Partition Sufficiency).**
For n = 30, both the family {π_SPEC, π_{15}} and the family {π_DYN(7), π_DYN(11)} are sufficient 2-partition families. Each achieves meet = π_disc with exactly 1 orthogonal jump. The CRT prime-factor family {π₂, π₃, π₅} requires 3 partitions and 2 jumps. Therefore the CRT prime-factor family is NOT the minimum-jump sufficient family for n = 30. *Proved.*

**Theorem 2 (SPEC Cannot Pair with Non-Residue DYN).**
For n = 30 and any non-trivial unit g (g ≢ 1 mod 30), meet(π_SPEC, π_DYN(g)) ≠ π_disc. Specifically, at least one of the pairs {3,27} or {5,25} is unseparated by both partitions simultaneously. *Proved.*

**Theorem 3 (Jump Count in 2-Partition Families).**
Every sufficient 2-partition family for Z/30Z using partitions from the set {π₂, π₃, π₅, π_{15}, π_SPEC, π_UG, π_DYN(7), π_DYN(11)} must contain at least 1 orthogonal jump. *Proof: Any refinement-compatible pair lies on a common chain; the chain does not achieve π_disc for n=30 (the finest named chain member is π_SPEC < π_disc). Alternatively: any pair with meet = π_disc must have incompatible partitions (if π_A ≤ π_B, meet = π_A, and π_A < π_disc for all named partitions). □*

---

## Part 9 — Outcome Classification

**OUTCOME A (CRT uniquely minimal): FALSE.**
{π_DYN(7), π_DYN(11)} is a sufficient 2-partition family that does not use any residue-class partition. CRT is not the unique minimal family.

**OUTCOME B (CRT not unique, jump count tight): PARTIALLY TRUE.**
Within the prime-CRT family alone, 2 jumps are required. But admitting other partitions, 1 jump suffices. The jump count k−1 = 2 is NOT tight across all admissible representations — it is tight only within the prime-CRT family.

**OUTCOME C (non-CRT family beats CRT): TRUE (with correct interpretation).**
For n = 30:
- Minimum jump count using prime-factor CRT: 2 jumps (k−1 = 2, unavoidable within that family).
- Minimum jump count using any partition family: 1 jump (achieved by {π_SPEC, π_{15}} or {π_DYN(7), π_DYN(11)}).
- The 1-jump bound is tight: no 2-partition family has 0 jumps (no refinement pair achieves π_disc).

**The CRT prime-factor family is suboptimal on jump count.** It uses three partitions with individually coarse block structure (2, 3, and 5 blocks respectively). The 2-partition families use fewer partitions with individually finer or more informative block structure.

---

## Summary

**Strongest honest claim:**
> For n = 30, the minimum sufficient family has m = 2 partitions and exactly 1 orthogonal jump. This is strictly less than the k−1 = 2 jumps required by the CRT prime-factor family. The improvement is possible because a single non-prime-factor partition (like π_{15} or π_DYN(11)) can encode the work of two prime-factor partitions simultaneously. The jump count k−1 from the prior sprint is the correct count *within the CRT prime-factor family*, not across all admissible representations.

**Strongest honest boundary:**
> The lower bound "at least 1 jump" is established (no sufficient refinement-only pair exists). Whether 1 jump is achievable for all squarefree n with k ≥ 3 prime factors, or whether the minimum jump count grows with k for some representation families, is not yet determined. The Z/30Z result shows only that k-1 is NOT a universal lower bound; it is a CRT-family lower bound. A general lower bound on minimum jumps across all possible partition families for squarefree n requires a separate theorem.

**Open problem (for next sprint):**
> Characterize the minimum sufficient family size m_min(n) and minimum jump count j_min(n) as a function of n for squarefree n. For n = p·q (k=2), prior results show j_min = 1 and m_min = 2. For n = p·q·r (k=3), this sprint shows j_min = 1 and m_min = 2. Conjecture: j_min = 1 and m_min = 2 for all squarefree n ≥ 2. Proof would require constructing, for any squarefree n, a sufficient 2-partition family with 1 orthogonal jump.
