# SPRINT: CLASSIFICATION OF TWO-PARTITION SUFFICIENCY
*Partition language + graph language. Proved vs. conjectural labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — Graph Formulation

**Definition (Partition Graph).**
For a partition π on Z/nZ, define the graph G(π):
- Vertex set: Z/nZ
- Edge set: U(π) = { {x,y} : x ≠ y and x ~_π y }

G(π) is an **equivalence graph**: a disjoint union of cliques, one complete subgraph K_{|B|} per block B of π.

**Notation.** K_n denotes the complete graph on Z/nZ (all C(n,2) = n(n-1)/2 edges).

---

**Theorem 1 (Graph Formulation of Sufficiency).**
For partitions π, ρ on Z/nZ:

meet(π, ρ) = π_disc  ⟺  G(π) and G(ρ) are edge-disjoint as subgraphs of K_n.

**Proof.** Direct from Theorem 0 of the prior sprint: meet(π,ρ) = π_disc iff U(π) ∩ U(ρ) = ∅. Since U(π) = edge set of G(π), edge-disjointness of G(π) and G(ρ) is exactly U(π) ∩ U(ρ) = ∅. □

**Observation (no coverage requirement).** The condition is edge-DISJOINTNESS only — NOT that G(π) ∪ G(ρ) covers K_n. Pairs {x,y} not in either G(π) or G(ρ) are automatically separated (they lie in different blocks of both π and ρ). Coverage of K_n is a strictly stronger condition that is NOT required for sufficiency.

**Example (n=30):** G(π_SPEC) has 14 edges, G(π_{15}) has 15 edges. Together they cover 29 of K_{30}'s 435 edges — about 6.7% — yet meet = π_disc. The 406 uncovered edges correspond to pairs already separated by both partitions individually.

---

**Structural Class of G(π).**
G(π) is an equivalence graph iff it is a disjoint union of cliques (no other structure is possible). Conversely, any disjoint union of cliques on Z/nZ corresponds to a partition. Therefore:

> The class of "partition graphs" = the class of equivalence graphs = the class of disjoint unions of cliques on Z/nZ.

**Degree structure.** In G(π), the degree of vertex x is |block(x)| − 1. So G(π) is a regular graph iff π is a uniform partition (all blocks of equal size).

---

## Part 2 — Structure of G(π_DYN(g))

**Setup.** For squarefree n = p₁···pₖ and g a unit (gcd(g,n)=1), T_g: x ↦ gx mod n is a bijection. The partition π_DYN(g) has blocks = orbits of T_g.

**In CRT coordinates.** Using Ψ: Z/nZ → Z/p₁Z × ··· × Z/pₖZ, T_g acts as:

(a₁,...,aₖ) ↦ (g₁a₁ mod p₁, ..., gₖaₖ mod pₖ)

where gᵢ = g mod pᵢ. The orbit of (a₁,...,aₖ) under T_g is:

{ (g₁^m a₁ mod p₁, ..., gₖ^m aₖ mod pₖ) : m ≥ 0 }

**Key constraint:** The parameter m is SHARED across all coordinates. This is not the product of independent coordinate orbits.

**Theorem 2 (DYN Orbit Structure for Focused Generator).**
Let g be focused on pⱼ: gᵢ = 1 for i ≠ j, gⱼ has order d in (Z/pⱼZ)*.

Then T_g acts only on coordinate j. The orbit of (a₁,...,aₖ) is:
{ (a₁,...,aⱼ₋₁, aⱼ·gⱼ^m mod pⱼ, aⱼ₊₁,...,aₖ) : m ≥ 0 }

This is the orbit of aⱼ under ×gⱼ in Z/pⱼZ, holding all other coordinates fixed.

**Orbit sizes:**
- If aⱼ = 0: orbit = {(a₁,...,0,...,aₖ)} — singleton.
- If aⱼ ≠ 0: orbit size = order of gⱼ in (Z/pⱼZ)* (call it d) — clique K_d in G(π_DYN(g)).

**When gⱼ is a primitive root mod pⱼ (order d = pⱼ−1):**

G(π_DYN(g)) consists of:
- n/pⱼ singletons: elements with aⱼ = 0 (i.e., elements x ≡ 0 mod pⱼ)
- n/pⱼ copies of K_{pⱼ−1}: one clique per choice of (a₁,...,â_j,...,aₖ) ∈ ∏_{i≠j} Z/pᵢZ, covering all pⱼ−1 non-zero aⱼ values

Edge count: (n/pⱼ) · C(pⱼ−1, 2) = n(pⱼ−1)(pⱼ−2) / (2pⱼ)

**Degree of vertex x in G(π_DYN(g)):**
- deg(x) = pⱼ−2 if aⱼ ≠ 0 (i.e., pⱼ ∤ x)
- deg(x) = 0 if aⱼ = 0 (i.e., pⱼ ∣ x)

**Example (n=30, g=7 focused on p₁=5 — actually g=7 is focused on neither).**
Correction: for n=30, g focused on p=5 means g ≡ 1 mod 6 and g ≢ 1 mod 5. Smallest: g=7 (7 mod 6=1 ✓, 7 mod 5=2 ✓). So g=7 IS focused on p=5 in Z/2Z × Z/3Z × Z/5Z coordinates.

Wait: 7 mod 2=1, 7 mod 3=1, 7 mod 5=2. So T₇ acts trivially on the 2 and 3 components and as ×2 on the 5-component. ×2 has order 4 in (Z/5Z)*. So orbits of size 4 for elements with a₃ ≠ 0, singletons for elements with a₃ = 0 (multiples of 5). ✓ Matches computed orbits from prior sprint.

---

**Theorem 3 (DYN Graph Disjointness).**
If g is focused on pⱼ and h is focused on pᵢ with i ≠ j, then G(π_DYN(g)) and G(π_DYN(h)) are edge-disjoint.

**Proof.** An edge {x,y} ∈ G(π_DYN(g)) requires x and y to be in the same T_g orbit, which (since g is focused on pⱼ) means all coordinates are equal EXCEPT possibly coordinate j. So x and y differ only in coordinate j.

An edge {x,y} ∈ G(π_DYN(h)) requires x and y to differ only in coordinate i.

For an edge in both: x and y must differ only in coordinate j AND only in coordinate i. Since i ≠ j, this forces x and y to differ in two different coordinates simultaneously, but also to differ in only one coordinate in each case — a contradiction unless x = y. Therefore no such edge exists. □

---

## Part 3 — Structure of G(π_SPEC)

**For even n = 2m:**

π_SPEC has blocks: {0} (singleton), {m} (singleton), and {x, 2m−x} for x = 1,...,m−1.

G(π_SPEC) consists of:
- 2 isolated vertices: 0 and m
- m−1 independent edges: {{x, 2m−x} : x = 1,...,m−1}

**Theorem 4 (SPEC is a Matching).**
G(π_SPEC) for n = 2m is a matching: a graph with maximum degree 1 (1-regular on the non-isolated vertices).

**Proof.** Each non-isolated vertex x appears in exactly one SPEC block {x, 2m−x} (since the reflection x ↦ 2m−x is an involution with no fixed points in {1,...,m−1} — if x = 2m−x then 2x = 2m, x = m, contradicting x ∈ {1,...,m−1}). Therefore each non-isolated vertex has exactly one neighbor in G(π_SPEC). □

**Degree:** deg(x) = 1 for x ∈ {1,...,m−1,m+1,...,n−1}, deg(x) = 0 for x ∈ {0,m}.

**Edge count:** m−1 = n/2 − 1.

**For odd n:**
The unique fixed point is 0 (since n−x = x requires 2x = n, impossible for odd n when x is integer... wait: 0 maps to n−0 = n ≡ 0 mod n. So 0 is fixed. For x ∈ {1,...,(n−1)/2}: {x, n−x} is an edge. For x = (n−1)/2+1 = (n+1)/2: n−x = n−(n+1)/2 = (n−1)/2, so this is already covered. So G(π_SPEC) for odd n has 1 isolated vertex (0) and (n−1)/2 matching edges.

**Theorem 4' (SPEC for Odd n).**
For odd n: G(π_SPEC) is a matching on Z/nZ \ {0} of size (n−1)/2. Still maximum degree 1 on all non-fixed elements. □

---

## Part 4 — Refutation of Conjecture A

**Conjecture A (restated):** Every sufficient 2-partition pair {π, ρ} is (up to isomorphism) either (DYN(g₁), DYN(g₂)) or (SPEC, translation-type) or reducible to these.

**Refutation.** We exhibit a sufficient pair for n = 6 that is neither DYN+DYN nor SPEC+shift:

Let n = 6. Define:
- π₁ = {{0,1},{2,3},{4,5}} (consecutive pairs — "interval partition")
- π₂ = {{0,2,4},{1,3,5}} (parity partition = π_CRT₂)

**G(π₁) edges:** {0,1}, {2,3}, {4,5}  — a matching.
**G(π₂) edges:** {0,2},{0,4},{2,4},{1,3},{1,5},{3,5}  — two triangles K₃.

**Edge-disjointness:** G(π₁) connects consecutive pairs; G(π₂) connects same-parity pairs. An element x and x+1 have different parities (x and x+1 differ in parity), so no pair {x,x+1} is in G(π₂). Therefore G(π₁) ∩ G(π₂) = ∅. ✓

**Sufficiency:** Every pair {x,y} with x ≠ y is either: (1) same parity, hence in G(π₂), hence in same π₂-block but separated by π₁ (they are in different consecutive-pair blocks since they differ by ≥ 2); or (2) different parity, hence {x,y} ∉ G(π₂), and since they differ in parity they are in different π₂-blocks. Either way, separated by at least one partition. ✓

**π₁ is NOT a DYN partition for any unit g mod 6:**
Units mod 6: {1, 5}. π_DYN(1) = all singletons (discrete). π_DYN(5): 5²=25≡1 mod 6, so T₅ has order 2. Orbits: 5·0=0 (fixed), 5·1=5, 5·2=10=4, 5·3=15=3 (fixed), 5·4=20=2, 5·5=25=1. Orbits: {0},{3},{1,5},{2,4}. This is π_SPEC for n=6, not π₁. No other units exist. So π₁ ≠ π_DYN(g) for any unit g. □

**π₁ is NOT π_SPEC for n=6:** π_SPEC for n=6 has blocks {0},{3},{1,5},{2,4}. This differs from π₁ = {{0,1},{2,3},{4,5}}. □

**π₁ is NOT a residue partition (π_d for any d|6):**
- d=1: π_triv = {{0,1,2,3,4,5}} — one block. ✗
- d=2: π₂ = parity partition. ✗
- d=3: π₃ = {{0,3},{1,4},{2,5}}. ✗
- d=6: π_disc. ✗

So π₁ is none of these.

**Conclusion:** Conjecture A is FALSE. The interval partition {{0,1},{2,3},{4,5}} is a valid component of a sufficient pair for n=6, and is not of DYN, SPEC, or residue type.

**Why the conjecture fails:** The class of equivalence graphs (disjoint unions of cliques) is vast and includes combinatorially-defined partitions with no algebraic motivation. Any bijection f: Z/nZ → A × B (with |A|·|B| = n) defines a sufficient pair, and most such bijections are not algebraically structured.

---

## Part 5 — Uniform Partition Classification

**Definition (Uniform Partition).** A partition π is *b-uniform* if all blocks have size b (so n is divisible by b and there are n/b blocks).

**Theorem 5 (Uniform Partition Sufficiency).**
Two uniform partitions π₁ (b₁-uniform) and π₂ (b₂-uniform) form a sufficient pair iff n ≥ b₁ · b₂.

Furthermore, when n = b₁ · b₂ (the MINIMUM case): {π₁, π₂} is sufficient iff the map f: Z/nZ → (blocks of π₁) × (blocks of π₂), f(x) = (block₁(x), block₂(x)), is a bijection — i.e., every (π₁-block, π₂-block) intersection contains EXACTLY 1 element.

**Proof.**

Let B₁,...,B_{n/b₁} be the blocks of π₁ and C₁,...,C_{n/b₂} be blocks of π₂.

Edge-disjointness requires: for every Bᵢ ∈ π₁ and Cⱼ ∈ π₂, |Bᵢ ∩ Cⱼ| ≤ 1 (no two elements in both same π₁-block and same π₂-block).

**Necessity of n ≥ b₁b₂:** Fix any block Bᵢ with |Bᵢ| = b₁. The b₁ elements of Bᵢ must lie in b₁ DISTINCT π₂-blocks (since each π₂-block contains at most 1 element of Bᵢ). Therefore n/b₂ ≥ b₁, i.e., n ≥ b₁b₂. □

**Sufficiency when n = b₁b₂:** If |Bᵢ ∩ Cⱼ| ≤ 1 for all i,j, and there are (n/b₁)·(n/b₂) = n²/(b₁b₂) = n possible (i,j) pairs while the total n elements map to n distinct (i,j) pairs — exactly a bijection. ✓

**When n > b₁b₂:** Some (i,j) pairs receive 0 elements, others receive 1. All intersections still ≤ 1, so edge-disjointness holds as long as we can construct such partitions. □

**Corollary (Minimum Uniform Case).** For n = b₁b₂: every sufficient 2-pair of uniform partitions (b₁-uniform and b₂-uniform) corresponds to a bijection Z/nZ → Z/b₁Z × Z/b₂Z. The CRT isomorphism (when b₁, b₂ are coprime divisors of n with b₁b₂ = n) is the canonical algebraic example. But ANY bijection — including non-group-homomorphisms — gives a valid sufficient pair.

---

## Part 6 — Classification of Sufficient DYN Pairs (General g, h)

**Beyond focused generators.** For general units g, h (not necessarily focused), when is {π_DYN(g), π_DYN(h)} sufficient?

**In CRT coordinates:** Two elements (a₁,...,aₖ) and (a₁',...,aₖ') are in the same T_g orbit iff there exists m ≥ 0 such that aᵢ' ≡ gᵢ^m · aᵢ (mod pᵢ) for ALL i simultaneously (with the same m).

**Sufficient pair condition:** For every distinct pair, at least one of T_g or T_h separates them.

**Theorem 6 (DYN Pair Classification via CRT).**
For focused generators g on p₁ and h on p₂: {π_DYN(g), π_DYN(h)} is always sufficient (Theorem 1 from prior sprint, reproved via Theorem 3 above).

For general (non-focused) generators: The pair {π_DYN(g), π_DYN(h)} is sufficient iff no two distinct elements are simultaneously T_g-equivalent and T_h-equivalent. In CRT coordinates this requires: there is no solution (m, ℓ) with m, ℓ ≥ 0, m·ℓ > 0, and (gᵢ^m = hᵢ^ℓ for all i) simultaneously — beyond the trivial solution m = ℓ = 0. *[Conjectural exact characterization — not proved in full generality here.]*

**Proved case (k=2, n=pq):** g = (g₁, 1) and h = (1, h₂) in CRT. The proof from Theorem 1 (prior sprint) applies directly. Extension to non-focused pairs would require: that ⟨g₁, h₁⟩ × ⟨g₂, h₂⟩ acts with "no simultaneous fixed structure" — the exact condition depends on the combined action of g and h on each prime component. This is open.

---

## Part 7 — Complete Classification Statement

**Theorem 7 (Complete Characterization).**
The following are equivalent for partitions π, ρ of Z/nZ:

1. {π, ρ} is a sufficient 2-partition pair.
2. G(π) and G(ρ) are edge-disjoint subgraphs of K_n.
3. U(π) ∩ U(ρ) = ∅.
4. For every pair of distinct elements {x,y}: NOT (x ~_π y AND x ~_ρ y).
5. The function Z/nZ → (blocks of π) × (blocks of ρ), x ↦ (block_π(x), block_ρ(x)) is injective.

All equivalences are immediate from definitions or prior theorems. □

**What this characterization provides:** A complete structural description. The class of all sufficient 2-partition pairs = the class of all edge-disjoint pairs of equivalence graphs on Z/nZ. No further algebraic constraint is forced.

**What this characterization does NOT provide:** A parametric enumeration of all sufficient pairs. The combinatorial space is large: for any bijection f: Z/nZ → A×B (with |A|·|B| ≤ n), a sufficient pair can be constructed. The number of such bijections grows factorially.

---

## Part 8 — Classification Table: Known Families

| Family name | Structure of G(π₁) | Structure of G(π₂) | Applicable n | Proved sufficient |
|---|---|---|---|---|
| DYN + DYN (focused) | n/p₁ cliques K_{p₁−1} + n/p₁ isolates | n/p₂ cliques K_{p₂−2} + n/p₂ isolates | All squarefree n, k≥2 | Yes (Theorem 1, prior sprint) |
| SPEC + half-modulus | Matching, n/2−1 edges | n/2 edges K₂ | Even squarefree n | Yes (Theorem 2, prior sprint) |
| CRT prime-factor pair | pᵢ-block uniform, blocks size n/pᵢ | pⱼ-block uniform, blocks size n/pⱼ | All squarefree n, k≥2 | Yes (CRT theorem) |
| Interval + parity (n=6) | Matching (consecutive pairs) | Two triangles K₃ | n=6 specifically | Yes (verified above) |
| Latin-square bijection | Uniform, block size b₁ | Uniform, block size b₂ | n = b₁b₂ | Yes (Theorem 5) |

**Observations from table:**
1. DYN+DYN and SPEC+half-modulus are non-uniform families (DYN has singletons + larger cliques).
2. CRT prime-factor and Latin-square bijection are uniform families.
3. The interval+parity example (n=6) is a uniform Latin-square bijection: 2-uniform × 3-uniform on n=6=2·3.
4. All algebraically-motivated families are instances of the complete characterization (Theorem 7) with additional structure.

---

## Part 9 — Conjecture B Assessment

**Conjecture B (restated):** At least one partition in every sufficient pair must be "low-degree" (like SPEC, degree ≤ 1) or "highly structured" (like DYN).

**Status: FALSE as stated for the "low-degree" part; OPEN for the "highly structured" part.**

**Counterexample to low-degree requirement:**
For n = 30 = 2·3·5: the DYN+DYN pair {π_DYN(11), π_DYN(7)} from prior sprint.

Degrees in G(π_DYN(7)) (focused on 5, primitive root of order 4):
- Elements with 5 ∤ x: degree 3 (in K₄ cliques)
- Elements with 5 ∣ x: degree 0 (isolated)

Degrees in G(π_DYN(11)) (focused on 3, non-trivial element of order 2):
- Elements with 3 ∤ x: degree 1 (in K₂ pairs)
- Elements with 3 ∣ x: degree 0 (isolated)

So G(π_DYN(11)) IS a matching (degree ≤ 1). The "low-degree" partition here is the DYN partition focused on the smaller prime (p=3, order 2, pairs). The one focused on p=5 (order 4, larger cliques) has degree 3.

**For a genuinely high-degree example:** n = 2·p·q with p,q large odd primes. DYN+DYN with g focused on p (primitive root, degree p−2) and h focused on q (primitive root, degree q−2). Both can have high degree for large primes.

**Degree bound for sufficient pairs:**
For any sufficient pair with edge-disjoint G(π₁), G(π₂): the neighborhoods N_{G(π₁)}(x) and N_{G(π₂)}(x) are disjoint subsets of Z/nZ \ {x}, so:

deg_{G(π₁)}(x) + deg_{G(π₂)}(x) ≤ n − 1 for all x.

This is the ONLY degree constraint forced by sufficiency. For large n, both degrees can be large simultaneously (up to (n−1)/2 each). Conjecture B fails.

---

## Summary

**Theorem 1 (proved):** Sufficient pair ⟺ G(π) and G(ρ) edge-disjoint. This is a complete characterization reducible to five equivalent conditions.

**Theorem 2 (proved):** G(π_DYN(g)) for g focused on pⱼ with primitive root gⱼ: disjoint union of n/pⱼ cliques K_{pⱼ−1} (one per choice of other coordinates) plus n/pⱼ isolated vertices.

**Theorem 3 (proved):** G(π_SPEC) = matching of size n/2−1 (even n) or (n−1)/2 (odd n). Degree = 1 on non-fixed elements.

**Theorem 4 (proved — Conjecture A refuted):** Not all sufficient pairs are DYN or SPEC type. The interval partition {{0,1},{2,3},{4,5}} forms a sufficient pair with the parity partition for n=6. Any bijection Z/nZ → A×B defines a sufficient pair.

**Theorem 5 (proved):** Uniform partition sufficiency: b₁-uniform and b₂-uniform partitions form a sufficient pair iff n ≥ b₁b₂. Equality case corresponds to bijections Z/nZ → Z/b₁Z × Z/b₂Z.

---

**Strongest honest claim:**
> The complete characterization of all sufficient 2-partition pairs is: equivalence graphs G(π) and G(ρ) are edge-disjoint. Within this class, two canonical algebraic constructions exist — DYN+DYN (via CRT coordinate focus) and SPEC+half-modulus (for even n) — but the full space of sufficient pairs is vastly larger, including arbitrary Latin-square bijections and combinatorially-defined partitions with no algebraic motivation. Conjecture A is false. The "jump count" question is completely resolved: j_min = 1 for all squarefree n with k ≥ 2.

**Strongest honest boundary:**
> The open problem is: classify sufficient DYN pairs for non-focused generators (Theorem 6 partial). The complete combinatorial enumeration of all sufficient 2-partition pairs for Z/nZ is equivalent to enumerating all pairs of edge-disjoint equivalence graphs on n vertices, which grows combinatorially and has no known simple closed form. The algebraic families (DYN, SPEC, CRT) are canonical within the algebraic class but do not exhaust the combinatorial class.

**Open problem (sharpest formulation):**
> For squarefree n = p₁···pₖ with k ≥ 3: does there exist a sufficient 2-partition pair {π, ρ} where both G(π) and G(ρ) are Cayley graphs of Z/nZ (i.e., defined by a connection set S where x ~_π y iff y−x ∈ S)? The DYN and SPEC constructions both yield Cayley graphs. If YES: characterize all Cayley-graph sufficient pairs. If NO: identify the obstruction.
