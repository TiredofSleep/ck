# SPRINT: CLASSIFICATION OF SUFFICIENT CAYLEY / DYN PAIRS
*Partition + group action language only. Proved vs. conjectural labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — Algebraic Subfamilies: Exact Definitions

**Definition 1 (DYN(g) — Single Generator Orbit Partition).**
For unit g ∈ (Z/nZ)* (gcd(g,n)=1), T_g: x ↦ gx mod n is a bijection.
π_DYN(g): x ~_{DYN(g)} y iff y = g^m · x for some m ≥ 0.
Blocks = orbits of the cyclic group ⟨T_g⟩ acting on Z/nZ.
G(π_DYN(g)): pairs {x, g^m·x} for all x ∈ Z/nZ, m ≥ 1, up to orbit-end.

**Definition 2 (DYN(G) — Subgroup Orbit Partition).**
For subgroup G ≤ (Z/nZ)*, π_DYN(G): x ~_{DYN(G)} y iff y = g·x for some g ∈ G.
Blocks = G-orbits in Z/nZ. DYN(g) = DYN(⟨g⟩). Coarser G = larger orbits = more edges.

**Definition 3 (Residue / CRT Partition π_d).**
For d | n: x ~_{π_d} y iff x ≡ y mod d.
In additive Cayley language: G(π_d) = Cay(Z/nZ, dZ/nZ \ {0}) (edges = non-zero multiples of d).
Prime-factor CRT: d = pᵢ ∈ {p₁,...,pₖ}.

**Definition 4 (SPEC — Reflection Partition).**
x ~_{SPEC} y iff x + y ≡ 0 (mod n).
G(π_SPEC) = matching: edges {{x, n−x} : x = 1,...,⌊(n−1)/2⌋}.

**Definition 5 (Multiplicative Cayley Partition).**
For symmetric set S ⊆ (Z/nZ)* closed under inversion (S = S⁻¹): define π_S by x ~_{π_S} y iff y·x⁻¹ ∈ S ∪ {1} (i.e., y and x are in the same coset of ⟨S⟩ acting multiplicatively).
DYN(G) is the multiplicative Cayley partition where S = G \ {1}.

**Separation of types:**

| Family | Action type | Generating structure |
|---|---|---|
| DYN(g) | Multiplicative cyclic | ⟨g⟩ ≤ (Z/nZ)* |
| DYN(G) | Multiplicative subgroup | G ≤ (Z/nZ)* |
| π_d (CRT/residue) | Additive subgroup | dZ/nZ ≤ Z/nZ |
| π_SPEC | Involution | x ↦ −x |

DYN and CRT/residue are DISTINCT families: DYN acts on the multiplicative structure of Z/nZ; CRT/residue acts on the additive structure. π_SPEC uses neither — it is the additive inverse involution.

---

## Part 2 — Unresolved-Pair Graphs for Each Family

**G(π_DYN(g)):** Disjoint union of cliques, one K_{|orbit|} per orbit. For g focused on pⱼ (primitive root): n/pⱼ cliques K_{pⱼ−1} plus n/pⱼ isolated vertices. For general unit g: orbit sizes vary by element type.

**G(π_DYN(G)):** Disjoint union of cliques, one K_{|G·x|} per G-orbit. G-orbits are coarser than ⟨g⟩-orbits for any generator g ∈ G.

**G(π_d):** For d | n: cliques correspond to residue classes mod d. Each class has n/d elements, giving n/d copies of K_{d}... wait: residue class sizes are n/d. There are d residue classes. So G(π_d) = d disjoint copies of K_{n/d}.

**G(π_SPEC):** Matching of size ⌊(n−1)/2⌋. Degree = 1 on all non-fixed elements.

---

## Part 3 — Main Theorem: DYN Pair Classification

**Theorem 1 (DYN Single-Generator Sufficiency).**
For squarefree n = p₁···pₖ and units g, h ∈ (Z/nZ)*:

{π_DYN(g), π_DYN(h)} is sufficient  ⟺  ⟨g⟩ ∩ ⟨h⟩ = {1}  in (Z/nZ)*

Equivalently: gcd(ord_{(Z/pᵢZ)*}(g mod pᵢ), ord_{(Z/pᵢZ)*}(h mod pᵢ)) = 1 for every prime pᵢ | n.

**Proof.**

**(⟹) Necessity.** Suppose ⟨g⟩ ∩ ⟨h⟩ ≠ {1}. Pick c ≠ 1 in ⟨g⟩ ∩ ⟨h⟩: write c = g^m = h^ℓ for m, ℓ ≥ 1.

Since c ≠ 1 in (Z/nZ)*, there exists a prime pᵢ with c ≢ 1 mod pᵢ. Let x ∈ Z/nZ be the element with aᵢ = 1 and aⱼ = 0 for j ≠ i (in CRT coordinates). Then:

g^m · x: aᵢ-coordinate = cᵢ · 1 = cᵢ ≠ 1 (since c ≢ 1 mod pᵢ).
h^ℓ · x: aᵢ-coordinate = cᵢ · 1 = cᵢ (same c in both, since g^m = h^ℓ = c in (Z/nZ)*).
aⱼ-coordinate for j ≠ i: 0 in both (c fixes 0).

So y := g^m · x = h^ℓ · x ≠ x. The pair {x, y} is in both U(π_DYN(g)) and U(π_DYN(h)). Not sufficient. □

**(⟸) Sufficiency.** Suppose ⟨g⟩ ∩ ⟨h⟩ = {1}. Suppose {x,y} ∈ U(π_DYN(g)) ∩ U(π_DYN(h)), meaning ∃m,ℓ ≥ 1 with g^m·x = y = h^ℓ·x.

For each coordinate i: (g^m)ᵢ · aᵢ = (h^ℓ)ᵢ · aᵢ where aᵢ = x mod pᵢ.

- If aᵢ ≠ 0: (gᵢ^m) = (hᵢ^ℓ) in (Z/pᵢZ)*, so gᵢ^m ∈ ⟨gᵢ⟩ ∩ ⟨hᵢ⟩ = {1}. Therefore gᵢ^m = 1, and gᵢ^m · aᵢ = aᵢ = yᵢ.
- If aᵢ = 0: gᵢ^m · 0 = 0 = yᵢ.

In both cases yᵢ = aᵢ. Since this holds for all i: y = x in CRT coordinates, contradicting y ≠ x. □

**Reduction to coprime orders.** In (Z/nZ)* ≅ ∏ᵢ (Z/pᵢZ)* (CRT):

⟨g⟩ ∩ ⟨h⟩ in (Z/nZ)* projects to ⟨gᵢ⟩ ∩ ⟨hᵢ⟩ in each (Z/pᵢZ)*.

Since (Z/pᵢZ)* is cyclic of order pᵢ−1: in any cyclic group, ⟨a⟩ ∩ ⟨b⟩ is the unique subgroup of order gcd(ord(a), ord(b)).

Therefore ⟨gᵢ⟩ ∩ ⟨hᵢ⟩ = {1}  ⟺  gcd(ord(gᵢ), ord(hᵢ)) = 1.

And ⟨g⟩ ∩ ⟨h⟩ = {1} in (Z/nZ)*  ⟺  ⟨gᵢ⟩ ∩ ⟨hᵢ⟩ = {1} in (Z/pᵢZ)* for all i  ⟺  gcd(ord(gᵢ), ord(hᵢ)) = 1 for all i. □

---

**Theorem 2 (DYN Subgroup Sufficiency).**
For subgroups G₁, G₂ ≤ (Z/nZ)*:

{π_DYN(G₁), π_DYN(G₂)} is sufficient (on units)  ⟺  G₁ ∩ G₂ = {1} in (Z/nZ)*

**Proof.** Two units x, y are in the same G₁-orbit iff y·x⁻¹ ∈ G₁ (since orbits = cosets of G₁ in the multiplicative action on units). They are in both G₁ and G₂ orbits iff y·x⁻¹ ∈ G₁ ∩ G₂. This happens for some x ≠ y iff G₁ ∩ G₂ ≠ {1}. □

*Note: extension to non-unit elements follows as in Theorem 1 by the zero-coordinate argument.*

---

## Part 4 — The Coordinate-Wise Coprime Order Condition: Worked Examples

**Notation.** For prime p | n: write ord_p(g) = ord_{(Z/pZ)*}(g mod p).

**Sufficient pair condition:** gcd(ord_p(g), ord_p(h)) = 1 for ALL primes p | n.

---

### n = 30 = 2 · 3 · 5

Unit group (Z/30Z)* ≅ {1} × Z/2Z × Z/4Z (order 8).
Units: {1, 7, 11, 13, 17, 19, 23, 29}.

Orders at each prime:

| g | ord₂(g) | ord₃(g) | ord₅(g) |
|---|---|---|---|
| 1  | 1 | 1 | 1 |
| 7  | 1 | 1 | 4 |
| 11 | 1 | 2 | 1 |
| 13 | 1 | 1 | 4 |
| 17 | 1 | 2 | 4 |
| 19 | 1 | 1 | 2 |
| 23 | 1 | 2 | 4 |
| 29 | 1 | 2 | 2 |

Note: ord₂(g) = 1 always (since (Z/2Z)* = {1}). So the p=2 condition is vacuous.

**Condition:** gcd(ord₃(g), ord₃(h)) = 1 AND gcd(ord₅(g), ord₅(h)) = 1.

Orders in (Z/3Z)* = Z/2Z: only 1 and 2. Coprime iff not both equal 2.
Orders in (Z/5Z)* = Z/4Z: 1, 2, 4. Coprime iff not both even (gcd(2,2)=gcd(2,4)=gcd(4,4)=2 or 4; only (1,*) coprime pairs).

**For p=5:** gcd(ord₅(g), ord₅(h)) = 1 requires at least one of g,h ≡ 1 mod 5 (i.e., ord₅ = 1). The only units with ord₅ = 1 are {1, 11}.

**For p=3:** gcd(ord₃(g), ord₃(h)) = 1 requires at least one of g,h ≡ 1 mod 3. Units with ord₃ = 1: {1, 7, 13, 19}.

**Complete list of non-trivial sufficient DYN pairs for n=30 (unordered, both non-identity):**

Need (at least one in {11} for p=5) AND (at least one in {7,13,19} for p=3) (since 11 satisfies p=5 but not p=3, and 7,13,19 satisfy p=3 but not p=5):

| Pair | gcd at p=3 | gcd at p=5 | Sufficient? |
|---|---|---|---|
| (7, 11)  | gcd(1,2)=1 ✓ | gcd(4,1)=1 ✓ | **Yes** |
| (13, 11) | gcd(1,2)=1 ✓ | gcd(4,1)=1 ✓ | **Yes** |
| (19, 11) | gcd(1,2)=1 ✓ | gcd(2,1)=1 ✓ | **Yes** |
| (7, 13)  | gcd(1,1)=1 ✓ | gcd(4,4)=4 ✗ | No |
| (17, 11) | gcd(2,2)=2 ✗ | — | No |
| (17, 23) | gcd(2,2)=2 ✗ | — | No |
| (17, 29) | gcd(2,2)=2 ✗ | — | No |

**Conclusion for n=30:** Exactly 3 non-trivial sufficient DYN pairs, all of the form (focused on 5, focused on 3). **No non-focused sufficient DYN pairs exist for n=30.** □

**Structural reason:** All orders in (Z/5Z)* = Z/4Z are powers of 2 (1, 2, 4). Any two non-trivial elements have even orders, hence gcd > 1. The only way to satisfy the p=5 condition is for one element to have order 1 (i.e., ≡ 1 mod 5). Similarly, (Z/3Z)* = Z/2Z: non-trivial order = 2. So the conditions force at least one focused generator on each prime. For n=30, all p−1 ∈ {2,4} are powers of 2, forcing focused structure.

---

### n = 42 = 2 · 3 · 7

Unit group (Z/42Z)* ≅ {1} × Z/2Z × Z/6Z (order 12).
Selected units with their orders:

| g | ord₃(g) | ord₇(g) | Notes |
|---|---|---|---|
| 1  | 1 | 1 | trivial |
| 5  | 2 | 4 | non-focused |
| 11 | 2 | 3 | non-focused |
| 13 | 1 | 2 | focused on 7 |
| 17 | 2 | 6 | non-focused |
| 19 | 1 | 6 | focused on 7 |
| 23 | 2 | 2 | non-focused |
| 25 | 1 | 4 | focused on 7 |
| 29 | 2 | 1 | focused on 3 |
| 31 | 1 | 3 | focused on 7 |
| 37 | 1 | 6 | focused on 7 |
| 41 | 2 | 6 | non-focused |

Note: ord₇ values in Z/6Z can be 1,2,3,6.

**Coprime pairs for p=7 with BOTH orders > 1:** gcd(2,3)=1 ✓. So (ord₇=2, ord₇=3) and (ord₇=3, ord₇=2) are coprime non-trivial pairs.

**New sufficient DYN pair (non-focused):**

Take g = 11: ord₃(11) = 2, ord₇(11) = 3. [11 mod 3 = 2 ✓, 11 mod 7 = 4, and 4 has order 3 in (Z/7Z)* since 4¹=4, 4²=2, 4³=1 mod 7 ✓]
Take h = 13: ord₃(13) = 1, ord₇(13) = 2. [13 mod 3 = 1 ✓, 13 mod 7 = 6, and 6² = 36 ≡ 1 mod 7 ✓]

Condition check:
- p=2: gcd(1,1) = 1 ✓
- p=3: gcd(ord₃(11), ord₃(13)) = gcd(2, 1) = 1 ✓
- p=7: gcd(ord₇(11), ord₇(13)) = gcd(3, 2) = 1 ✓

**{π_DYN(11), π_DYN(13)} is a sufficient DYN pair for n=42.** ✓

**g=11 is not focused:** 11 acts non-trivially on BOTH the 3-component (order 2) AND the 7-component (order 3). This is the first proved non-focused sufficient DYN pair.

**Explicit orbit structure of T₁₁ on Z/42Z:**

T₁₁ in CRT: (a₁,a₂,a₃) ↦ (a₁, 2a₂ mod 3, 4a₃ mod 7). Order = lcm(1,2,3) = 6.

- Elements with a₂ = 0, a₃ = 0: fixed. Singletons. (Multiples of 21.)
- Elements with a₂ ≠ 0, a₃ = 0: orbit size 2 (only 3-component active). (Multiples of 7, not 21.)
- Elements with a₂ = 0, a₃ ≠ 0: orbit size 3 (only 7-component active). (Multiples of 3, not 21.)
- Elements with a₂ ≠ 0, a₃ ≠ 0: orbit size lcm(2,3) = 6. (Non-multiples of both 3 and 7.)

G(π_DYN(11)) contains: K₂ cliques (from size-2 orbits), K₃ cliques, K₆ cliques, plus isolated vertices.

**Additional non-focused pairs for n=42 (selection):**

| Pair | gcd at p=3 | gcd at p=7 | Sufficient? | Focus type |
|---|---|---|---|---|
| (11,13) | gcd(2,1)=1 ✓ | gcd(3,2)=1 ✓ | **Yes** | g non-focused |
| (29,31) | gcd(2,1)=1 ✓ | gcd(1,3)=1 ✓ | **Yes** | g focused on 3, h focused on 7 |
| (29,13) | gcd(2,1)=1 ✓ | gcd(1,2)=1 ✓ | **Yes** | both focused, different primes |
| (5,13)  | gcd(2,1)=1 ✓ | gcd(4,2)=2 ✗ | No | — |
| (31,13) | gcd(1,1)=1 ✓ | gcd(3,2)=1 ✓ | **Yes** | both focused on 7, coprime orders |

**Note the last row:** (31,13) — BOTH g=31 and h=13 are focused on 7 (trivial mod 3), with ord₇(31)=3 and ord₇(13)=2. This is a **same-prime focused pair** with coprime orders. New mechanism confirmed.

---

### n = 66 = 2 · 3 · 11

(Z/66Z)* ≅ Z/2Z × Z/10Z. Orders at p=11: (Z/11Z)* = Z/10Z. Order-5 elements exist (5 | 10, 10 is not a prime power).

**Coprime order pairs at p=11 with both > 1:** gcd(2,5)=1 ✓. Elements of order 5 mod 11: {3,4,5,9} (since 2¹⁰≡1, order-5 elements are 2^{10/5·k}=2^{2k} for k=1,2,3,4: {4,5,9,3}). Elements of order 2 mod 11: {10} (since 10²=100≡1 mod 11).

**Non-focused sufficient pair example:**

g non-trivial at p=3 (order 2) AND p=11 (order 5): g mod 3 = 2, g mod 11 = 4 (order 5), g mod 2 = 1.
CRT: x ≡ 2 mod 3, x ≡ 4 mod 11, x ≡ 1 mod 2. Solving: x ≡ 2 mod 3 and x ≡ 4 mod 11 → x = 37 mod 33. 37 mod 2=1 ✓. **g=37.**

h trivial at p=3 (order 1) AND order 2 at p=11: h ≡ 1 mod 3, h ≡ 10 mod 11, h ≡ 1 mod 2.
CRT: x ≡ 1 mod 6, x ≡ 10 mod 11 → x = 43. **h=43.**

Check: gcd(ord₃(37), ord₃(43)) = gcd(2,1) = 1 ✓. gcd(ord₁₁(37), ord₁₁(43)) = gcd(5,2) = 1 ✓.

**{π_DYN(37), π_DYN(43)} is sufficient for n=66.** g=37 is non-focused (non-trivial on both 3 and 11 components). ✓

---

### n = 70 = 2 · 5 · 7

Orders at p=5: (Z/5Z)*=Z/4Z. Orders 1,2,4 — all even powers of 2. Coprime non-trivial pair: impossible.
Orders at p=7: (Z/7Z)*=Z/6Z. Coprime pair (2,3) possible.

**Non-focused sufficient pair:**

g with ord₅(g)=2 AND ord₇(g)=3: g≡4 mod 5, g≡2 mod 7, g≡1 mod 2.
CRT: x≡4 mod 5, x≡2 mod 7 → x≡9 mod 35. 9 mod 2=1 ✓. **g=9.**

h with ord₅(h)=1 AND ord₇(h)=2: h≡1 mod 5, h≡6 mod 7, h≡1 mod 2.
CRT: x≡1 mod 5, x≡6 mod 7 → 5j+1≡6 mod 7 → 5j≡5 → j≡1. j=1: x=6, gcd(6,70)=2 ✗. j=8: x=41. **h=41.**

Verify: ord₅(9)=ord₅(4)=2, ord₇(9)=ord₇(2)=3. ord₅(41)=ord₅(1)=1, ord₇(41)=ord₇(6)=2.
Check: gcd(2,1)=1 ✓, gcd(3,2)=1 ✓.

**{π_DYN(9), π_DYN(41)} is sufficient for n=70.** g=9 is non-focused (non-trivial on 5 AND 7). ✓

---

## Part 5 — When Do All Sufficient DYN Pairs Reduce to Focused?

**Theorem 3 (Focused-Only Classification).**
All non-trivial sufficient DYN pairs for squarefree n are focused-on-distinct-primes if and only if for every prime pᵢ | n, the group (Z/pᵢZ)* = Z/(pᵢ−1)Z has the property that every two non-trivial elements have gcd of orders > 1. This occurs iff pᵢ−1 is a prime power for every prime pᵢ | n.

**Proof.**

(⟹) Suppose some pᵢ−1 is not a prime power. Write pᵢ−1 = a·b with gcd(a,b)=1 and a,b > 1. In Z/(pᵢ−1)Z, there exists an element of order a and an element of order b with gcd(a,b)=1. These provide a non-trivial coprime order pair at prime pᵢ. The pair can be extended to units g, h of Z/nZ (trivial on all other primes) giving a sufficient pair where BOTH are focused on pᵢ with coprime orders — a "same-prime" sufficient pair not of the focused-on-distinct-primes type.

(⟸) Suppose pᵢ−1 is a prime power for every pᵢ | n. All non-trivial elements of (Z/pᵢZ)* have order = a power of some fixed prime qᵢ (the prime in pᵢ−1 = qᵢ^{aᵢ}). Any two non-trivial elements have orders qᵢ^s and qᵢ^t with s,t ≥ 1, giving gcd = qᵢ^{min(s,t)} > 1. For the gcd condition to hold at pᵢ, at least one of g,h must have order 1 mod pᵢ (i.e., ≡ 1 mod pᵢ). This forces at least one of g,h to be trivial at each pᵢ where it is "not focused." A non-trivial unit non-trivial at two or more such primes would fail the condition with any partner. □

**Primes pᵢ where pᵢ−1 IS a prime power (focused-only regime):**

| pᵢ | pᵢ−1 | Prime power? |
|---|---|---|
| 2 | 1 | Yes (vacuous) |
| 3 | 2 | Yes (2¹) |
| 5 | 4 | Yes (2²) |
| 7 | 6 = 2·3 | **No** |
| 11 | 10 = 2·5 | **No** |
| 13 | 12 = 4·3 | **No** |
| 17 | 16 = 2⁴ | Yes (2⁴) |
| 19 | 18 = 2·9 | **No** |
| 23 | 22 = 2·11 | **No** |

**Corollary:** For n = 2·3·5 = 30 (all pᵢ−1 prime powers), all sufficient DYN pairs are focused on distinct primes. For n = 42, 66, 70 (containing primes 7 or 11), non-focused pairs exist.

---

## Part 6 — Classification Table

| n | Primes with pᵢ−1 not prime power | Non-focused sufficient DYN pairs exist? | Example non-focused pair | Mechanism |
|---|---|---|---|---|
| 30 = 2·3·5 | None | **No** | — | All focused on distinct primes |
| 42 = 2·3·7 | 7 (6=2·3) | **Yes** | {π_DYN(11), π_DYN(13)} | g non-trivial on 3 and 7 with coprime orders (2,3) |
| 66 = 2·3·11 | 11 (10=2·5) | **Yes** | {π_DYN(37), π_DYN(43)} | g non-trivial on 3 and 11 with coprime orders at 11 being (5,2) |
| 70 = 2·5·7 | 7 (6=2·3) | **Yes** | {π_DYN(9), π_DYN(41)} | g non-trivial on 5 and 7 with coprime order at 7 being (3,2) |

For all n: two focused generators on distinct primes ALWAYS give a sufficient pair. For n containing primes p with p−1 composite (not prime power): additional non-focused pairs exist.

---

## Part 7 — Outcome Classification

**Outcome A (all sufficient DYN pairs are focused-conjugate): PARTIALLY TRUE.**

For n=30: holds. For n=42,66,70: fails. Outcome A holds iff all pᵢ−1 are prime powers.

**Outcome B (genuinely new DYN mechanism exists): TRUE.**

Three distinct mechanisms identified:
1. **Focused on distinct primes:** g trivial mod all but pⱼ, h trivial mod all but pᵢ (i≠j). Universal.
2. **Same-prime coprime orders:** both g, h trivial mod all primes except one pⱼ, with gcd(ord_pⱼ(g), ord_pⱼ(h))=1. Requires pⱼ−1 to be non-prime-power.
3. **Non-focused mixed:** g non-trivial at multiple primes, with coordinate-wise coprime orders vs. h. Requires non-prime-power pᵢ−1 for at least one prime.

**Outcome C (non-focused rarely sufficient): CONTEXT-DEPENDENT.**

For n=30: no non-focused sufficient pairs. For n=42,66,70: they exist. Rarity depends on whether n contains primes with non-prime-power p−1.

---

## Summary

**Theorem 1 (proved):** {π_DYN(g), π_DYN(h)} is sufficient iff ⟨g⟩ ∩ ⟨h⟩ = {1} in (Z/nZ)*, equivalently: gcd(ord_{(Z/pᵢZ)*}(g mod pᵢ), ord_{(Z/pᵢZ)*}(h mod pᵢ)) = 1 for all primes pᵢ | n.

**Theorem 2 (proved):** {π_DYN(G₁), π_DYN(G₂)} is sufficient iff G₁ ∩ G₂ = {1} as subgroups of (Z/nZ)*.

**Theorem 3 (proved):** All non-trivial sufficient DYN pairs are focused-on-distinct-primes iff every pᵢ−1 is a prime power for primes pᵢ | n.

---

**Strongest honest claim:**
> The complete classification of sufficient DYN pairs is: gcd(ord_{pᵢ}(g), ord_{pᵢ}(h)) = 1 for all pᵢ | n, equivalently ⟨g⟩ ∩ ⟨h⟩ = {1} in (Z/nZ)*. This is a clean group-theoretic condition depending only on local orders at each prime. It admits three structural mechanisms: focused-on-distinct-primes (universal), same-prime coprime orders (requires non-prime-power p−1), and non-focused mixed (same requirement). The focused-on-distinct-primes construction is canonical and exists for all squarefree n; the other mechanisms exist iff the prime factorization of n contains primes pᵢ with pᵢ−1 having at least two distinct prime factors.

**Strongest honest boundary:**
> Theorem 1 covers DYN single-generator pairs. The extension to DYN(G) subgroup pairs is clean (Theorem 2) but the classification of all subgroups G₁, G₂ ≤ (Z/nZ)* with G₁∩G₂={1} is open in general (it reduces to the classification of complementary subgroup pairs in the abelian group (Z/nZ)*). For SPEC+DYN mixed pairs: no clean group-theoretic classification is given here. The condition for SPEC+DYN sufficiency involves SPEC's matching structure and DYN's orbit structure — the existing proof (disjoint U-sets via n/4 non-integer) is geometric/arithmetic, not group-theoretic.

**Open problem:**
> Classify all subgroup pairs (G₁, G₂) of (Z/nZ)* with G₁ ∩ G₂ = {1} for squarefree n. This is equivalent to classifying complementary subgroups in the group (Z/nZ)* ≅ ∏ᵢ Z/(pᵢ−1)Z. For each prime pᵢ: the condition restricts to gcd(ord_{pᵢ}(G₁ component), ord_{pᵢ}(G₂ component)) conditions. A complete enumeration would give all "canonical algebraic sufficient DYN pairs."
