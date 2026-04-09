# SPRINT: TWO-PARTITION SUFFICIENCY PROGRAM
## From n=30 to a General Theorem
*Partition lattice only. Proved vs. conjectural labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — Foundation Theorem

**Definition (Unresolved-pair set).**
For a partition π on a finite set X, define:

U(π) = { {x,y} : x ≠ y and x ~_π y }

That is, U(π) is the set of all pairs of distinct elements that lie in the same block.

---

**Theorem 0 (Disjoint U-sets ⟺ Discrete Meet).**
For partitions π, ρ on X:

meet(π, ρ) = π_disc  ⟺  U(π) ∩ U(ρ) = ∅

**Proof.**

The blocks of meet(π, ρ) are the non-empty intersections B ∩ C for B ∈ π, C ∈ ρ. Two elements x, y lie in the same meet-block iff x and y lie in the same π-block AND the same ρ-block.

Formally: x ~_{meet} y iff x ~_π y AND x ~_ρ y.

Therefore:

U(meet(π, ρ)) = { {x,y} : x ~_π y AND x ~_ρ y } = U(π) ∩ U(ρ)

meet(π, ρ) = π_disc  ⟺  U(meet(π, ρ)) = ∅  ⟺  U(π) ∩ U(ρ) = ∅  □

**Corollary.** A 2-partition family {π, ρ} is sufficient iff U(π) ∩ U(ρ) = ∅.

**Corollary.** For any family {π₁,...,πₘ}:
meet(π₁,...,πₘ) = π_disc  ⟺  ⋂ U(πᵢ) = ∅

---

## Part 2 — Recasting n=30 Successes

**Case 1: {π_SPEC, π_{15}} for n=30.**

U(π_SPEC) = { {x, 30−x} : x = 1,...,14 }  (14 pairs)

U(π_{15}) = { {x, x+15} : x = 0,...,14 }  (15 pairs, including {0,15})

**Intersection test:** Suppose {a,b} ∈ U(π_SPEC) ∩ U(π_{15}). Then:
- a + b = 30  (from U(π_SPEC): b = 30−a)
- b = a + 15  (from U(π_{15}): the pair {a, a+15})
  or a = b + 15

Case b = a+15: a+(a+15) = 30 ⟹ 2a = 15 ⟹ a = 7.5. Not an integer.
Case a = b+15: b+(b+15) = 30 ⟹ 2b = 15 ⟹ b = 7.5. Not an integer.

Therefore U(π_SPEC) ∩ U(π_{15}) = ∅. ✓

**Why this works:** The SPEC pairs are {x, 30−x} = {x, −x mod 30}. The π_{15} pairs are {x, x+15}. These encode two different "involutions" of Z/30Z: negation and translation-by-half. The obstruction to their intersection (requiring x = 7.5) is exactly that n/4 = 7.5 is not an integer — a consequence of 4 ∤ 30.

---

**Case 2: {π_DYN(7), π_DYN(11)} for n=30.**

Recall orbits (from prior sprint):
- π_DYN(7): {1,7,13,19}, {2,8,14,26}, {3,9,21,27}, {4,16,22,28}, {6,12,18,24}, {11,17,23,29}, plus singletons {0,5,10,15,20,25}.
- π_DYN(11): 10 singletons (multiples of 3: {0,3,6,...,27}) plus 10 pairs {1,11},{2,22},{4,14},{5,25},{7,17},{8,28},{10,20},{13,23},{16,26},{19,29}.

**Intersection test:** A pair {x,y} ∈ U(π_DYN(7)) ∩ U(π_DYN(11)) requires x and y to be in the same T₇-orbit AND the same T₁₁-orbit.

Check each non-singleton T₇-orbit:
- {1,7,13,19}: T₁₁ orbits: 1∈{1,11}, 7∈{7,17}, 13∈{13,23}, 19∈{19,29}. All four in distinct T₁₁ orbits. No two share a T₁₁ orbit. ✓
- {2,8,14,26}: 2∈{2,22}, 8∈{8,28}, 14∈{4,14}, 26∈{16,26}. All distinct. ✓
- {3,9,21,27}: all multiples of 3, hence singletons in T₁₁. All distinct T₁₁ orbits. ✓
- {4,16,22,28}: 4∈{4,14}, 16∈{16,26}, 22∈{2,22}, 28∈{8,28}. All distinct. ✓
- {6,12,18,24}: all multiples of 3 (since 3|6,12,18,24), singletons in T₁₁. ✓
- {11,17,23,29}: 11∈{1,11}, 17∈{7,17}, 23∈{13,23}, 29∈{19,29}. All distinct. ✓

No pair within any T₇-orbit lies in a common T₁₁-orbit. Therefore U(π_DYN(7)) ∩ U(π_DYN(11)) = ∅. ✓

**Why this works:** T₁₁ fixes all multiples of 3 (since 11x ≡ x mod 30 iff 10x ≡ 0 mod 30 iff 3|x). The T₇-orbit {3,9,21,27} (all multiples of 3) lands in T₁₁-singletons. For the unit-class orbits: T₇ and T₁₁ generate different subgroups of (Z/30Z)* = Z/2Z × Z/4Z (T₇ has order 4; T₁₁ has order 2) — their actions on unit orbits are "complementary" in the sense formalized below.

---

## Part 3 — General Construction via CRT Coordinates

**Setup.** For squarefree n = p₁p₂···pₖ, the Chinese Remainder Theorem gives an isomorphism:

Ψ: Z/nZ  ⟶  Z/p₁Z × Z/p₂Z × ··· × Z/pₖZ
    x    ↦  (x mod p₁, x mod p₂, ..., x mod pₖ) = (a₁, a₂, ..., aₖ)

All computations below use this coordinate representation.

**Definition (Component-Focused Generator).**
An element g ∈ Z/nZ is *focused on prime pⱼ* if:
- g ≡ gⱼ mod pⱼ with gⱼ ≠ 1 in (Z/pⱼZ)* (acts non-trivially on the j-th coordinate)
- g ≡ 1 mod pᵢ for all i ≠ j (acts as identity on all other coordinates)

Such g exists by CRT (choose any non-identity unit gⱼ in (Z/pⱼZ)* and solve g ≡ 1 mod (n/pⱼ), g ≡ gⱼ mod pⱼ).

**In CRT coordinates:** T_g acts as (a₁,...,aₖ) ↦ (a₁,...,gⱼ·aⱼ mod pⱼ,...,aₖ), changing only the j-th coordinate.

---

**Theorem 1 (Universal 2-Partition Sufficiency).**
For any squarefree n = p₁···pₖ with k ≥ 2: let g be focused on p₁ and h be focused on p₂. Then:

meet(π_DYN(g), π_DYN(h)) = π_disc

**Proof.**

By Theorem 0, it suffices to show U(π_DYN(g)) ∩ U(π_DYN(h)) = ∅.

Let (a₁,...,aₖ) ≠ (a₁',...,aₖ') be two distinct elements of Z/nZ. We must show they are separated by at least one of T_g, T_h.

Since the two elements are distinct, they differ in at least one coordinate. Let the coordinates be compared as follows:

**Case A: a₁ ≠ a₁' and a₂ = a₂', (a₃,...,aₖ) = (a₃',...,aₖ').**

T_h orbit of (a₁,...,aₖ): T_h changes only the 2nd coordinate (h is focused on p₂). The orbit is {(a₁, a₂·h₂^k mod p₂, a₃,...,aₖ) : k ≥ 0}. The 1st coordinate a₁ is fixed throughout. T_h orbit of (a₁',...) similarly fixes a₁'. Since a₁ ≠ a₁', these are in different T_h orbits. **Separated by T_h.** ✓

**Case B: a₂ ≠ a₂' and a₁ = a₁', (a₃,...,aₖ) = (a₃',...,aₖ').**

T_g orbit of (a₁,...,aₖ): T_g changes only the 1st coordinate. The 2nd coordinate a₂ is fixed. T_g orbit of (a₁', a₂',...) fixes a₂'. Since a₂ ≠ a₂', different T_g orbits. **Separated by T_g.** ✓

**Case C: aⱼ ≠ aⱼ' for some j ≥ 3 (with aᵢ = aᵢ' for i < j).**

T_g orbit fixes all coordinates except the 1st. Orbit of (a₁,...,aₖ) has fixed (a₂,...,aₖ). Orbit of (a₁',...,aₖ') has fixed (a₂',...,aₖ') = (a₂,...,aⱼ₋₁,aⱼ',aⱼ₊₁',...). Since aⱼ ≠ aⱼ', the tuples (a₂,...,aₖ) and (a₂',...,aₖ') differ at position j ≥ 3. Different T_g orbit "labels" (the fixed-coordinate tuple). **Separated by T_g.** ✓

All cases are exhausted. Therefore U(π_DYN(g)) ∩ U(π_DYN(h)) = ∅. □

**Corollary.** For any squarefree n with k ≥ 2 prime factors: j_min(n) = 1 and m_min(n) = 2.

Proof: Single-partition sufficiency requires the partition to be π_disc itself (any proper partition has non-singleton blocks). Therefore m_min ≥ 2. The construction achieves m_min = 2. Since the two partitions are incompatible (proved below), j_min = 1. □

**Incompatibility of π_DYN(g) and π_DYN(h) (g focused on p₁, h focused on p₂):**

Elements (a₁, a₂, a₃,...) and (a₁, a₂', a₃,...) with a₂ ≠ a₂': T_g orbit fixes the 2nd coordinate, so these are in different T_g orbits. But if a₂' = h₂·a₂ for one step of T_h, they are in the same T_h orbit. So some pairs are identified by T_h but separated by T_g.

Elements (a₁, a₂,...) and (a₁', a₂,...) with a₁ ≠ a₁': same T_h orbit label (same 1st coordinate? no — T_h fixes 1st coordinate). Hmm: T_h orbit of (a₁,a₂,a₃,...) has fixed 1st coordinate a₁. T_h orbit of (a₁',a₂,a₃,...) has fixed 1st coordinate a₁' ≠ a₁. Different T_h orbits. But T_g orbit of (a₁,a₂,a₃,...) = {(a₁·g₁^k, a₂, a₃,...)}. If a₁' = a₁·g₁^k for some k: same T_g orbit! So some pairs are identified by T_g but separated by T_h.

Therefore neither π_DYN(g) ≤ π_DYN(h) nor the converse. The two partitions are **incompatible**, and the transition is an orthogonal jump. □

---

## Part 4 — Second Construction: SPEC + Half-Modulus

**Theorem 2 (SPEC + Half-Modulus Sufficiency).**
For any squarefree n = 2m with m odd: the family {π_SPEC, π_m} satisfies meet(π_SPEC, π_m) = π_disc.

**Proof.**

U(π_SPEC) = { {x, 2m−x} : x = 1,...,m−1 } ∪ {∅}  (fixed points {0} and {m} are singletons)

U(π_m) = { {x, x+m} : x = 0,...,m−1 }  (partition by x mod m; each block = {r, r+m} for r = 0,...,m−1)

**Intersection test:** Suppose {a,b} ∈ U(π_SPEC) ∩ U(π_m). Then:
- a + b = 2m  (from U(π_SPEC))
- b = a + m   (from U(π_m))

Substituting: a + (a+m) = 2m ⟹ 2a = m ⟹ a = m/2.

Since m is odd (n = 2m squarefree, so 4 ∤ n, so m is odd), m/2 is not an integer. Contradiction.

Therefore U(π_SPEC) ∩ U(π_m) = ∅. □

**Incompatibility of π_SPEC and π_m (m odd):**

π_m block {0, m}: 0 is a π_SPEC singleton ({0}) and m is a π_SPEC singleton ({m}). So {0,m} is not contained in any single π_SPEC block. π_m ≰ π_SPEC.

π_SPEC block {1, 2m−1}: 1 mod m = 1, (2m−1) mod m = m−1. Since m ≥ 3, 1 ≠ m−1. Different π_m blocks. π_SPEC ≰ π_m.

Therefore π_SPEC and π_m are **incompatible**. The transition is an orthogonal jump. □

**Comparison of the two constructions:**

For even n = 2m (m odd): both {π_DYN(g), π_DYN(h)} (Theorem 1) and {π_SPEC, π_m} (Theorem 2) are valid.

π_m is a residue partition (by x mod m = x mod p₂···pₖ). It corresponds to the "composite CRT factor" encoding all odd prime information simultaneously. {π_SPEC, π_m} effectively uses one partition to encode all k−1 odd prime CRT coordinates at once, paired with one partition that handles the "negation-vs-half-shift" separation.

π_DYN(g) and π_DYN(h) use two orbit partitions, each focused on one prime factor. For k = 3 (as in n = 30, 42, 66, 70), Theorem 2 is "more efficient" in block count (π_m has m = n/2 blocks of size 2, π_SPEC has n/2+1 blocks including singletons), while Theorem 1's partitions have coarser block structure.

---

## Part 5 — Verification for n = 42, 66, 70

### n = 42 = 2 · 3 · 7 (k = 3)

**Construction 1 (SPEC + half-modulus):** {π_SPEC, π_{21}}.
- n = 42, m = 21 (odd ✓).
- U(π_SPEC) ∩ U(π_{21}) = ∅ since n/4 = 10.5 ∉ Z. ✓

**Construction 2 (DYN + DYN):** Choose:
- g focused on 3: g ≡ 2 mod 3 (non-trivial, order 2 in (Z/3Z)*), g ≡ 1 mod 14.
  CRT: x ≡ 1 mod 14, x ≡ 2 mod 3. x = 14k+1; 14k+1 ≡ 2k+1 ≡ 2 mod 3 ⟹ 2k ≡ 1 mod 3 ⟹ k ≡ 2 mod 3. k=2: **g = 29**.
  Verify: 29 mod 2=1 ✓, 29 mod 3=2 ✓, 29 mod 7=1 ✓.

- h focused on 7: h ≡ 3 mod 7 (primitive root mod 7, order 6), h ≡ 1 mod 6.
  CRT: x ≡ 1 mod 6, x ≡ 3 mod 7. x = 6j+1; 6j+1 ≡ 3 mod 7 ⟹ 6j ≡ 2 mod 7 ⟹ j ≡ 2·6⁻¹ mod 7 = 2·6 = 12 ≡ 5 mod 7. j=5: **h = 31**.
  Verify: 31 mod 2=1 ✓, 31 mod 3=1 ✓, 31 mod 7=3 ✓.

{π_DYN(29), π_DYN(31)} sufficient for n=42 by Theorem 1. ✓

---

### n = 66 = 2 · 3 · 11 (k = 3)

**Construction 1:** {π_SPEC, π_{33}}.
- n = 66, m = 33 (odd ✓). n/4 = 16.5 ∉ Z. ✓

**Construction 2 (DYN + DYN):**
- g focused on 3: g ≡ 2 mod 3, g ≡ 1 mod 22.
  CRT: x ≡ 1 mod 22, x ≡ 2 mod 3. x = 22j+1; 22j+1 ≡ j+1 ≡ 2 mod 3 ⟹ j ≡ 1 mod 3. j=1: **g = 23**.
  Verify: 23 mod 2=1 ✓, 23 mod 3=2 ✓, 23 mod 11=1 ✓.

- h focused on 11: h ≡ 2 mod 11 (primitive root mod 11), h ≡ 1 mod 6.
  CRT: x ≡ 1 mod 6, x ≡ 2 mod 11. x = 6k+1; 6k+1 ≡ 2 mod 11 ⟹ 6k ≡ 1 mod 11 ⟹ k ≡ 6⁻¹ ≡ 2 mod 11. k=2: **h = 13**.
  Verify: 13 mod 2=1 ✓, 13 mod 3=1 ✓, 13 mod 11=2 ✓.

{π_DYN(23), π_DYN(13)} sufficient for n=66 by Theorem 1. ✓

---

### n = 70 = 2 · 5 · 7 (k = 3)

**Construction 1:** {π_SPEC, π_{35}}.
- n = 70, m = 35 (odd ✓). n/4 = 17.5 ∉ Z. ✓

**Construction 2 (DYN + DYN):**
- g focused on 5: g ≡ 2 mod 5 (order 4 in (Z/5Z)*), g ≡ 1 mod 14.
  CRT: x ≡ 1 mod 14, x ≡ 2 mod 5. x = 14j+1; 14j+1 ≡ 4j+1 ≡ 2 mod 5 ⟹ 4j ≡ 1 mod 5 ⟹ j ≡ 4 mod 5. j=4: **g = 57**.
  Verify: 57 mod 2=1 ✓, 57 mod 5=2 ✓, 57 mod 7=1 ✓.

- h focused on 7: h ≡ 3 mod 7 (primitive root mod 7), h ≡ 1 mod 10.
  CRT: x ≡ 1 mod 10, x ≡ 3 mod 7. x = 10m+1; 10m+1 ≡ 3m+1 ≡ 3 mod 7 ⟹ 3m ≡ 2 mod 7 ⟹ m ≡ 2·3⁻¹ ≡ 2·5 = 10 ≡ 3 mod 7. m=3: **h = 31**.
  Verify: 31 mod 2=1 ✓, 31 mod 5=1 ✓, 31 mod 7=3 ✓.

{π_DYN(57), π_DYN(31)} sufficient for n=70 by Theorem 1. ✓

---

## Part 6 — Why SPEC + π_{n/2} Does Not Extend to Odd n

**Proposition.** For odd squarefree n, no "half-modulus" partition π_{n/2} exists (n/2 ∉ Z). The Theorem 2 construction is specific to even n.

**Why odd squarefree n requires a different construction:**
For odd n = p₁···pₖ (all primes odd), there is no prime equal to 2. The "reflection" π_SPEC (x ↦ n−x) does not pair with any simple half-shift partition. The DYN+DYN construction (Theorem 1) applies uniformly to all squarefree n.

**For odd squarefree n: explicit construction via Theorem 1.**
Choose g focused on p₁ and h focused on p₂ (CRT). The same proof applies. Example:

n = 15 = 3·5 (k=2): g focused on 3 (g ≡ 2 mod 3, g ≡ 1 mod 5 ⟹ g = 11), h focused on 5 (h ≡ 2 mod 5, h ≡ 1 mod 3 ⟹ h = 7). {π_DYN(11), π_DYN(7)} sufficient for n=15.

Verify: 11 mod 3=2 ✓, 11 mod 5=1 ✓. 7 mod 3=1 ✓, 7 mod 5=2 ✓.
CRT coordinates: T₁₁ = (2,1) (non-trivial on p₁=3, trivial on p₂=5). T₇ = (1,2) (trivial on p₁, non-trivial on p₂). By Theorem 1: sufficient. ✓

---

## Part 7 — Classification Table

| n | k | CRT jumps | m_min | j_min | Sufficient 2-family (Construction 1) | Sufficient 2-family (Construction 2) |
|---|---|---|---|---|---|---|
| 15 = 3·5 | 2 | 1 | 2 | 1 | {π_DYN(11), π_DYN(7)} | {π₃, π₅} (CRT = minimal) |
| 30 = 2·3·5 | 3 | 2 | 2 | 1 | {π_SPEC, π_{15}} | {π_DYN(7), π_DYN(11)} |
| 42 = 2·3·7 | 3 | 2 | 2 | 1 | {π_SPEC, π_{21}} | {π_DYN(29), π_DYN(31)} |
| 66 = 2·3·11 | 3 | 2 | 2 | 1 | {π_SPEC, π_{33}} | {π_DYN(23), π_DYN(13)} |
| 70 = 2·5·7 | 3 | 2 | 2 | 1 | {π_SPEC, π_{35}} | {π_DYN(57), π_DYN(31)} |
| 105 = 3·5·7 | 3 | 2 | 2 | 1 | {π_DYN(g₁), π_DYN(g₂)} | (same theorem, k=3 odd) |

For n = 105 = 3·5·7 (odd, k=3): g focused on 3 (g ≡ 2 mod 3, g ≡ 1 mod 35 ⟹ g = 71), h focused on 5 (h ≡ 2 mod 5, h ≡ 1 mod 21 ⟹ h = 22). Note: g=71 mod 3=2 ✓, mod 5=1 ✓, mod 7=1 ✓. h=22 mod 3=1 ✓, mod 5=2 ✓, mod 7=1 ✓. {π_DYN(71), π_DYN(22)} sufficient. ✓

**Observation from table:** m_min = 2 and j_min = 1 for ALL squarefree n with k ≥ 2. The CRT prime-factor jump count k−1 exceeds j_min = 1 for all k ≥ 3.

---

## Part 8 — The k=2 Special Case

For n = p·q (k=2): the CRT family {π_p, π_q} also achieves m_min = 2 and j_min = 1. The CRT family IS minimal for k=2.

But the DYN+DYN construction ({π_DYN(g), π_DYN(h)}) also achieves it — these are distinct families.

**Are they equivalent?** For n=15: {π₃, π₅} vs {π_DYN(11), π_DYN(7)}.
- π_DYN(11) = π_{anti-3}: T₁₁ fixes multiples of 5 and acts as ×2 on 3-component. The orbits are NOT the same as π₃ blocks. Different partition. But both families achieve m_min.
- For k=2: the CRT family and the DYN family are different sufficient 2-partition families, both minimal.

---

## Part 9 — General Lower Bound: m_min ≥ 2

**Proposition.** For squarefree n ≥ 4 (at least 2 prime factors), no single partition π ≠ π_disc satisfies meet(π) = π_disc. Therefore m_min ≥ 2.

**Proof.** Any single partition π with at least one non-singleton block B satisfies U(π) ≠ ∅. The "meet" of a single partition with itself is itself, not π_disc. More directly: a single partition π = π_disc is the only partition satisfying U(π) = ∅. For any named non-discrete partition (SPEC, UG, DYN for non-trivial g, CRT factor), U(π) ≠ ∅. □

**Theorem (Tight Bound):** For squarefree n with k ≥ 2 prime factors: m_min(n) = 2 and j_min(n) = 1.

Proof: Lower bound m_min ≥ 2 by the Proposition. Upper bound m_min ≤ 2 by Theorem 1. The 1 jump in any sufficient 2-partition family is required because any refinement-compatible pair (one refines the other) has meet equal to the finer partition, which is never π_disc for named non-discrete partitions. Therefore every sufficient 2-partition family must contain at least one orthogonal jump: j_min ≥ 1. Theorem 1 achieves j_min = 1. □

---

## Summary

**Theorem 0 (proved):** meet(π, ρ) = π_disc ⟺ U(π) ∩ U(ρ) = ∅. The central equivalence: sufficiency is disjointness of unresolved-pair sets.

**Theorem 1 (proved):** For any squarefree n = p₁···pₖ (k ≥ 2): a sufficient 2-partition DYN family exists. Construction: g focused on p₁, h focused on p₂, with {π_DYN(g), π_DYN(h)} disjoint U-sets.

**Theorem 2 (proved):** For squarefree n = 2m (m odd): {π_SPEC, π_m} is a sufficient 2-partition family with disjoint U-sets. Construction specific to even squarefree n.

**Classification table:** m_min = 2, j_min = 1 for all tested squarefree n with k ≥ 2. Confirmed for n = 15, 30, 42, 66, 70, 105 by explicit construction.

---

**Strongest honest claim:**
> For any squarefree n with k ≥ 2 prime factors, a sufficient 2-partition family exists with exactly 1 orthogonal jump. This is tight: m_min = 2 (no single non-discrete partition suffices) and j_min = 1 (no refinement-only pair suffices). The CRT prime-factor family requires k−1 jumps, which equals 1 only for k=2. For k ≥ 3, the CRT family is suboptimal on jump count. The correct invariant is not "number of prime factors" but whether two partitions can be found with disjoint unresolved-pair sets, and Theorem 1 guarantees this always exists.

**Strongest honest boundary:**
> Theorem 1 is proved. What is NOT proved: (1) the explicit generators g and h in Theorem 1 must be chosen as "focused" on distinct prime components via CRT — a different choice of generators may or may not produce a sufficient DYN family (no general characterization of which pairs (g,h) work is given). (2) The minimum partition BLOCK COUNT across all sufficient 2-families is not determined. Theorem 2's {π_SPEC, π_m} has |π_m| = m = n/2 blocks, while Theorem 1's families may have very different block counts. (3) Whether the "focused generator" construction is the unique construction up to isomorphism is an open question.

**Open problem:**
> Characterize all sufficient 2-partition families for Z/nZ (n squarefree). The two constructions here (DYN+DYN via CRT focus, SPEC+half-modulus for even n) are provably sufficient but not claimed to be exhaustive or canonical. A complete classification of sufficient 2-families would be the next result.
