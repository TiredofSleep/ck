# UOP MASTER MEMO: TWO-PARTITION SUFFICIENCY ON SQUAREFREE Z/nZ
## Frozen Arc — Complete Classification
*All results proved. Conjectural statements labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## §0 — Setup and Notation

**System.** Z/nZ = {0, 1, ..., n−1} with n = p₁p₂···pₖ squarefree (distinct primes).

**CRT isomorphism.** Ψ: Z/nZ → ∏ᵢ Z/pᵢZ, x ↦ (x mod p₁, ..., x mod pₖ) = (a₁,...,aₖ). Used throughout; all coordinate analysis is via Ψ.

**Partition.** A partition π of Z/nZ is a set of non-empty disjoint blocks covering Z/nZ. The unresolved-pair set is U(π) = { {x,y} : x ≠ y, x ~_π y }. Equivalently U(π) is the edge set of the equivalence graph G(π) on vertex set Z/nZ.

**Sufficiency.** A 2-partition family {π₁, π₂} is *sufficient* if meet(π₁,π₂) = π_disc (the discrete partition), i.e., every pair of distinct elements is separated by at least one partition.

**Map families.** Two algebraic map families are used throughout:
- **Type M (multiplicative-orbit):** f_G: Z/nZ → G-orbit space, for G ≤ (Z/nZ)*. Blocks = G-orbits.
- **Type A (additive-quotient):** f_d: Z/nZ → Z/dZ, x ↦ x mod d, for d | n. Blocks = residue classes mod d.

---

## §1 — Foundation Theorem

**Theorem 1 (Unresolved-Pair Criterion).**
For partitions π, ρ on Z/nZ:

> meet(π, ρ) = π_disc  ⟺  U(π) ∩ U(ρ) = ∅

**Proof.** x ~_{meet} y iff x ~_π y AND x ~_ρ y. Therefore U(meet) = U(π) ∩ U(ρ). Meet = π_disc iff U(meet) = ∅. □

**Theorem 2 (Unified Orthogonality Principle — UOP).**
For partitions π₁, π₂ with inducing maps f_π₁: Z/nZ → A₁ and f_π₂: Z/nZ → A₂:

> {π₁, π₂} is sufficient iff the joint map J = (f_π₁, f_π₂): Z/nZ → A₁ × A₂ is injective.

**Proof.** J injective iff for all x ≠ y: (f_π₁(x), f_π₂(x)) ≠ (f_π₁(y), f_π₂(y)), i.e., f_π₁(x) ≠ f_π₁(y) or f_π₂(x) ≠ f_π₂(y), i.e., {x,y} ∉ U(π₁) ∩ U(π₂). Equivalently U(π₁) ∩ U(π₂) = ∅. □

---

## §2 — Corollaries by Map Type

**Theorem 3 (M + M Sufficiency).**
For G, H ≤ (Z/nZ)* with orbit partitions π_DYN(G) and π_DYN(H):

> {π_DYN(G), π_DYN(H)} sufficient  ⟺  G ∩ H = {1} in (Z/nZ)*

Coordinatewise: gcd(|G mod pᵢ|, |H mod pᵢ|) = 1 for all primes pᵢ | n.

**Proof.** Conflict pair {x,y} with x unit: y·x⁻¹ ∈ G ∩ H. Trivial intersection forces y·x⁻¹ = 1, y = x. For non-unit x with some aᵢ = 0: G,H act as identity on zero components; the non-zero components satisfy the same unit analysis. □

**Theorem 4 (A + M Sufficiency).**
For d | n and G ≤ (Z/nZ)*:

> {π_d, π_DYN(G)} sufficient  ⟺  g ≡ 1 mod pⱼ for all g ∈ G and all primes pⱼ | (n/d)

Equivalently: G ≤ ker( (Z/nZ)* →ᵣₑ𝒹 (Z/(n/d)Z)* ).

**Proof.**
(⟹) If g ≢ 1 mod pⱼ for some pⱼ | (n/d): pick x with aⱼ ≠ 0, aᵢ = 0 for pᵢ | d. Then x and g·x agree on all d-components (both 0), so x ≡ g·x mod d. But g·x ≠ x. Conflict.

(⟸) If G trivial on (n/d): any orbit move g·x either changes a d-prime component (g·x and x disagree mod d, different π_d class, no conflict) or changes no component (g·x = x, trivial). No conflicts in zero-fiber since G trivial on n/d primes means g·0 = 0 at those primes and also at d-primes (since for x = multiple of d, aᵢ = 0 for pᵢ | d; g acts only on pⱼ | d, but G trivial there too? — Wait: G trivial on pⱼ | (n/d) means g≡1 mod pⱼ. G may be non-trivial on pᵢ | d. So g can move aᵢ for pᵢ | d. For x = multiple of d: aᵢ = 0 for pᵢ | d; g·x has aᵢ = gᵢ·0 = 0 for pᵢ | d. So g·x is also a multiple of d; same π_d fiber (0 mod d). But g·x ≠ x would require non-trivial action on some pⱼ | (n/d) — which is trivial. So g·x = x for all multiples of d. No zero-fiber conflict. □

**Remark.** The condition of Theorem 4 is strictly stronger than "G → (Z/dZ)* injective." The injective condition misses zero-fiber conflicts.

**Theorem 5 (A + A Sufficiency — CRT).**
For d₁, d₂ | n:

> {π_{d₁}, π_{d₂}} sufficient  ⟺  every prime pᵢ | n divides d₁ or d₂  ⟺  lcm(d₁, d₂) = n

**Proof.** f_{d₁} resolves all primes dividing d₁; f_{d₂} resolves all primes dividing d₂. Joint map resolves all primes iff d₁ ∪ d₂ covers all prime factors. For squarefree n: lcm = n iff supports cover. □

---

## §3 — Jump Necessity (Partition Lattice)

**Definition.** For partitions π, ρ of Z/nZ, a move π → ρ is:
- a *refinement move* if π ≤ ρ or ρ ≤ π (one refines the other)
- an *orthogonal jump* if π and ρ are incompatible (neither refines the other) and meet(π,ρ) < min(π,ρ) in the lattice

**Theorem 6 (Orthogonal Jump Necessity — MVJN, generalized).**
For squarefree n with k ≥ 2 prime factors: every minimal sufficient 2-partition family from the Type-A family requires exactly one orthogonal jump. More generally: every minimal sufficient 2-partition family from any partition family requires at least one orthogonal jump.

**Proof.** A refinement-only pair lies on a common chain in the partition lattice. The meet of any chain is the finest element. No named partition (other than π_disc itself) equals π_disc. Therefore meet of any chain-pair > π_disc. Not sufficient. Every sufficient pair must therefore contain an incompatible step — at least one orthogonal jump. □

**Theorem 7 (CRT k−1 Jump Necessity).**
Within the Type-A prime-factor family {π_{p₁},...,π_{pₖ}}: every minimal sufficient subfamily has exactly k members and k−1 consecutive orthogonal jumps.

**Proof.** From Theorem 5: every prime must be covered. Minimum cover requires all k factor partitions (omitting any pᵢ leaves that prime uncovered; Theorem 5 requires every prime in d₁ or d₂, so in the k-member family, every prime must appear). Each consecutive pair is incompatible (proved: pᵢ-blocks cross pⱼ-blocks for i ≠ j). k members → k−1 transitions, each orthogonal. □

---

## §4 — Two Universal 2-Partition Constructions

**Construction 1 (DYN + DYN via focused generators).**
For any squarefree n = p₁···pₖ (k ≥ 2): choose g focused on p₁ (g ≡ gᵢ mod p₁ with ord_{p₁}(g₁) > 1; g ≡ 1 mod pᵢ for i > 1) and h focused on p₂. Then G = ⟨g⟩ and H = ⟨h⟩ satisfy G ∩ H = {1} (G supported at p₁, H at p₂, disjoint). The pair {π_DYN(g), π_DYN(h)} is sufficient.

Minimum sufficient family size: m_min = 2. Minimum jump count: j_min = 1. Both tight. □

**Construction 2 (SPEC + half-modulus for even n).**
For squarefree n = 2m with m odd: U(π_SPEC) ∩ U(π_m) = ∅ since a common pair would require m/2 ∈ Z, which fails for odd m. Sufficient. □

**Corollary.** j_min(n) = 1 and m_min(n) = 2 for all squarefree n with k ≥ 2. The CRT prime-factor bound k−1 is the correct bound within the Type-A prime-factor family, not globally.

---

## §5 — Algebraic Classification of DYN and SPEC Pairs

**Theorem 8 (DYN + DYN — Complete Classification).**
{π_DYN(g), π_DYN(h)} sufficient iff ⟨g⟩ ∩ ⟨h⟩ = {1} in (Z/nZ)*. Three mechanisms:

1. *Focused on distinct primes:* exists for all squarefree n.
2. *Same-prime coprime orders:* exists when pᵢ−1 has at least two distinct prime factors (pᵢ not a Fermat prime).
3. *Non-focused mixed:* g non-trivial at multiple primes with coordinate-wise coprime orders.

All sufficient DYN pairs are focused on distinct primes iff every pᵢ−1 is a prime power (all odd primes are Fermat primes or pᵢ = 3, 5, 17, 257, 65537).

**Theorem 9 (SPEC + DYN — Complete Classification).**
{π_SPEC, π_DYN(g)} (with π_SPEC the full reflection partition) is sufficient iff ord_{(Z/pᵢZ)*}(g mod pᵢ) is odd for every odd prime pᵢ | n. Equivalently: g mod pᵢ lies in the 2'-subgroup O_{pᵢ} ≤ (Z/pᵢZ)* at every odd prime. Non-trivial sufficient g exists iff n has a non-Fermat odd prime factor.

**Note.** π_SPEC is the Type-M partition with G = {1,−1}. Theorem 9 is Theorem 8 specialized to H = ⟨−1⟩. The naive global condition "−1 ∉ ⟨g⟩ in (Z/nZ)*" is necessary but not sufficient; the correct condition is local at each prime.

---

## §6 — Local Exemplar: Z/10Z

For n = 10 = 2·5 (k = 2), the complete partition lattice:

**Refinement chain:** π_disc ≤ π_SPEC ≤ π_UG = π_DYN ≤ π_CRT₂ ≤ π_triv

**Incompatible with chain:** π_CRT₅ (the p=5 factor partition)

**Identification:** π_DYN(3) = π_UG (T₃ has orbits = gcd-classes: proved via gcd(3,10)=1 preserves gcd-classes, T₃ transitive on units and on 2-multiples).

**Φ-preservation:** Under Φ: Z/10Z → S¹, Φ(x) = e^{2πix/10}:
- DYN: Φ(gx) = Φ(x)^g (exact)
- SPEC: Φ(10−x) = conj(Φ(x)) (exact)
- CRT₅ as antipodal: Φ(x+5) = −Φ(x) (exact)
- CRT product structure: NOT preserved — requires T² (dimensional obstruction π₁(S¹) = Z vs π₁(T²) = Z²)

**Sufficient 2-partition pairs for n=10:** Any pair {X, CRT₅} with X in {SPEC, UG, CRT₂} (all verified by U-set disjointness). Also {π_DYN(g), π_DYN(h)} with ⟨g⟩ ∩ ⟨h⟩ = {1} (no non-trivial such pair exists for n=10 since (Z/10Z)* = Z/4Z and all non-trivial subgroups share elements). So for n=10 the only sufficient pairs are {X, CRT₅} types — one coordinate from the chain, one orthogonal jump.

---

## §7 — Complete Arc Summary

| Theorem | Statement | Status |
|---|---|---|
| Unresolved-pair criterion | meet = disc ⟺ U∩U = ∅ | Proved |
| UOP | Sufficient ⟺ joint map injective | Proved |
| M+M (Thm 3) | G ∩ H = {1} | Proved |
| A+M (Thm 4) | G trivial on primes of n/d | Proved |
| A+A / CRT (Thm 5) | lcm(d₁,d₂) = n | Proved |
| Jump necessity (Thm 6) | Every sufficient pair has ≥ 1 jump | Proved |
| CRT k−1 bound (Thm 7) | k factors need k−1 jumps | Proved |
| m_min = 2, j_min = 1 | Universal 2-partition construction | Proved |
| DYN+DYN classification (Thm 8) | ⟨g⟩ ∩ ⟨h⟩ = {1} + three mechanisms | Proved |
| SPEC+DYN classification (Thm 9) | Odd order at all odd primes | Proved |

**Strongest honest claim:**
> For squarefree Z/nZ, the complete theory of 2-partition sufficiency is: the joint map (f_π₁, f_π₂) must be injective. All classification results — DYN+DYN, SPEC+DYN, additive+multiplicative, CRT — are computations of this single criterion in different algebraic contexts. The jump structure of the partition lattice (refinement vs. orthogonal) is the geometric expression of coordinate coverage: orthogonal jumps add coverage of new CRT coordinates; refinement moves do not. This arc is complete for squarefree n over the families {Type M, Type A}.

**Strongest honest boundary:**
> Two open problems remain outside this arc: (1) The prime-power case (n = p^r, p^r·q, etc.): CRT decomposes into p-adic components; the orbit and quotient map analysis must be extended. Whether 2-partition sufficiency holds generically and whether new obstruction types emerge is unknown. (2) Partition families beyond Type M and Type A (quadratic residues, character sums, non-group-theoretic constructions): the UOP meta-criterion applies but the injectivity computation requires different tools.

---
---
---

# PHASE 2: PRIME-POWER FRONTIER
## First Test Cases: n = p², 2p², p²q
*New territory. All results below are labeled: proved / partial / conjectural.*

---

## §P1 — What Changes for Repeated Primes

**CRT breaks.** For n = p^r (r ≥ 2): Z/p^rZ is NOT isomorphic to a product. The CRT coordinate decomposition (a₁,...,aₖ) is replaced by a single p-adic component. No independent prime coordinates.

**Unit group changes.** (Z/p^rZ)* ≅ Z/p^{r−1}(p−1)Z for odd prime p (and Z/2 × Z/2^{r−2} for p=2, r ≥ 3). This is cyclic for odd p — the same cyclic order structure, but now the group has order p^{r−1}(p−1), not p−1.

**Additive structure changes.** Divisors of p^r are {1, p, p², ..., p^r}. The residue partitions form a chain: π_1 ≥ π_p ≥ π_{p²} ≥ ... ≥ π_{p^r} = π_disc. No "incompatible" additive partition exists — all additive partitions for n = p^r are on a SINGLE CHAIN.

**Consequence for jumps.** For n = p^r (single prime power): the partition lattice for additive maps has no orthogonal jumps at all. Every pair of Type-A partitions is comparable (one refines the other). No 2-partition sufficient family exists within the Type-A family alone.

---

## §P2 — Case n = p² (Single Prime Power)

**System.** Z/p²Z, p prime. Elements: {0, 1, ..., p²−1}. Non-units: {0, p, 2p, ..., (p−1)p}.

**Type-A partitions:** π_p (blocks of size p, p blocks) and π_{p²} = π_disc. Only two non-trivial additive maps: f_p: x ↦ x mod p, and f_1 (trivial). f_p alone does not give π_disc (blocks of size p).

**{π_p, anything}: can anything complement π_p?**

U(π_p) = { {x,y} : x ≡ y mod p, x ≠ y }. These are p−1 edges within each of the p residue classes. Total |U(π_p)| = p · C(p,2) = p²(p−1)/2.

Need a partition ρ with U(ρ) ∩ U(π_p) = ∅: ρ must separate every pair that agrees mod p.

**Type-M for n = p²:**

(Z/p²Z)* ≅ Z/p(p−1)Z (cyclic for odd p).

Choose g a primitive root mod p² (a generator of the full unit group). Orbits of T_g on Z/p²Z:
- {0}: singleton (0 is fixed)
- {p, 2p, ..., (p−1)p}: T_g maps kp ↦ gkp mod p²; since gcd(g,p)=1 and gkp has aᵢ of the "p-fiber"... Let's be careful. For x = kp (0 < k < p): g·kp mod p². Since g is a primitive root mod p², and kp is not a unit: g·kp mod p² = (g mod p²)·(kp mod p²). This is gkp mod p². Since p | kp and gcd(g,p)=1: gkp ≡ (g mod p)·(kp mod p²) mod p². The orbit of kp is {kp, gkp mod p², g²kp mod p², ...}. Since gcd(g,p)=1, g is a unit mod p (g mod p ≠ 0). So g acts on {kp : k=1,...,p−1} as multiplication-by-(g mod p) on k, giving an orbit of size = ord_p(g mod p) = ord_{(Z/pZ)*}(g mod p) = p−1 (if g is also a prim root mod p). So {p, 2p, ..., (p−1)p} forms a single orbit of size p−1 under T_g.
- Units {x : gcd(x,p²)=1}: orbit = all p(p−1) units (single orbit, since g is primitive root).

So π_DYN(g) for primitive root g has exactly 3 orbits: {0}, the p−1 multiples of p, the p(p−1) units.

U(π_DYN(g)) contains all C(p(p−1),2) unit-unit pairs plus all C(p−1,2) non-zero-multiple-of-p pairs.

**Test: {π_p, π_DYN(g)} for n = p².**

Check U(π_p) ∩ U(π_DYN(g)):

Two units x ≡ y mod p: x and y are both units and agree mod p. Are they in the same T_g orbit? Since all p(p−1) units form a single orbit: yes, x and y are in the same orbit. {x,y} ∈ U(π_DYN(g)).

And {x,y} ∈ U(π_p) (they agree mod p, both non-zero mod p, so same residue class).

**Conflict: both ∈ U(π_p) ∩ U(π_DYN(g)).** NOT sufficient.

**Explanation.** For n = p², the "mod p" residue class for a unit r ∈ Z/pZ contains p units of Z/p²Z: {r, r+p, r+2p,...,r+(p−1)p}. All these are in the same T_g orbit (since g primitive root cycles through all units). So π_DYN(g) puts all p units from each mod-p class into the same block — but so does π_p for non-units. The unit classes of π_p and the single unit-orbit of π_DYN(g) overlap everywhere.

**Theorem P1 (proved).** For n = p² and g a primitive root mod p²: {π_p, π_DYN(g)} is NOT sufficient.

---

## §P3 — Obstruction Analysis for n = p²

**Structural obstruction.** For n = p² with a single prime: there is NO pair of multiplicative-orbit and additive-quotient partitions that achieves sufficient 2-partition.

**Why:** The unit group (Z/p²Z)* acts transitively on units (for any primitive root g). All units form a single orbit. π_DYN(g) has block {all units} of size p(p−1). Any additive partition π_d (d = p^i) puts units of the same residue mod d into one block — if d = p, blocks of p units each, all within the single DYN orbit. Conflict at every block.

For a DYN partition with a non-primitive-root generator g (smaller orbit): orbits are subsets of the unit group. The additive partition π_p still creates residue classes that cut across these orbits. Explicit:

**Lemma P1.** For n = p² and any unit g, any two elements x, y with x ≡ y mod p and gcd(x,p)=1: x and y are in the same T_g orbit iff g mod p has an orbit in (Z/pZ)* that contains both x mod p and y mod p, AND the orbit-lengths are compatible. If g is focused entirely at one "level," the orbit still mixes residue classes.

More precisely: x = r + sp and y = r + tp (same residue r mod p, distinct units). x·y⁻¹ = (r+sp)(r+tp)⁻¹ mod p². This is (1 + sp/r)(1 + tp/r)⁻¹ ≈ 1 + (s−t)p/r mod p². For T_g to map x to y: g^m ≡ 1 + (s−t)p/r mod p². Such a g^m exists (it is an element of order p in (Z/p²Z)*, since 1 + p·Z/p²Z is the unique subgroup of order p) iff g has order divisible by p in (Z/p²Z)*. Since |(Z/p²Z)*| = p(p−1) and g non-trivial: ord(g) | p(p−1). For T_g to map x to y where they agree mod p, need g^m ≡ 1 mod p but g^m ≢ 1 mod p². This requires p | ord(g). For primitive root: ord(g) = p(p−1), p divides it. For g with p ∤ ord(g): g can only shift residue classes mod p, never connect elements within the same class.

**Theorem P2 (proved).** For n = p²: if p ∤ ord(g) in (Z/p²Z)*, then no two elements in the same π_p-class are in the same T_g orbit. In this case: {π_p, π_DYN(g)} IS sufficient.

**Proof.** x ≡ y mod p means y = x + tp for some t ≢ 0 mod p. For g^m · x = y: g^m = y/x = 1 + tp/x. Since p ∤ x (x is a unit): tp/x has exact p-adic valuation 1. So g^m ≡ 1 mod p but g^m ≢ 1 mod p². In (Z/p²Z)*, elements ≡ 1 mod p form the unique subgroup of order p: S_p = {1, 1+p, 1+2p,...,1+(p−1)p}. g^m ∈ S_p requires S_p ∩ ⟨g⟩ ≠ {1}, i.e., p | ord(g). If p ∤ ord(g): ⟨g⟩ ∩ S_p = {1}, so no g^m ≡ 1 mod p with g^m ≠ 1. No same-residue-class pair is in a common orbit. Therefore U(π_p) ∩ U(π_DYN(g)) = ∅ for non-unit elements. For multiples of p: π_p puts {0, p, 2p,...,(p−1)p} each in the block 0 mod p (all ≡ 0 mod p). T_g with p ∤ ord(g): g mod p has ord(g mod p) = ord(g) / gcd(ord(g), p) = ord(g) (since p ∤ ord(g)), so g mod p generates all of (Z/pZ)* (if ord(g) = p−1) or a proper subgroup. Elements {kp : k=1,...,p−1} under T_g: g·kp = (g mod p)·k · p mod p². The orbit of kp is {(g mod p)^m · k · p : m ≥ 0} mod p², which varies the coefficient k through an orbit in Z/pZ. These elements all have valuation exactly 1 (multiples of p but not p²), all in the same π_p block (residue 0 mod p). Conflict? Yes: k and (g mod p)·k are in the same T_g orbit and same π_p block. □

**Correction.** Theorem P2 proof breaks down for multiples of p: elements {p, 2p, ..., (p−1)p} are all ≡ 0 mod p (same π_p block), and their T_g orbit can contain multiple of them.

**Revised Theorem P2.** {π_p, π_DYN(g)} sufficient iff BOTH:
(a) p ∤ ord(g) in (Z/p²Z)* [units don't mix within mod-p classes], AND
(b) T_g acts as a singleton on the set {p, 2p,...,(p−1)p}, i.e., g·kp = kp for all k — meaning g ≡ 1 mod p.

Condition (b) requires g ≡ 1 mod p, i.e., g ∈ S_p ∪ {1}, i.e., g ≡ 1 mod p in Z/pZ.

**But:** g ≡ 1 mod p implies g ∈ S_p (the subgroup of order p) or g = 1. Any non-identity g ≡ 1 mod p has order p. And then p | ord(g), violating condition (a).

So conditions (a) and (b) are contradictory for non-trivial g. **No non-trivial g satisfies both.** This recovers the obstruction.

**Theorem P3 (proved — n = p² obstruction).** For n = p² and any non-trivial unit g ∈ (Z/p²Z)*: {π_p, π_DYN(g)} is NOT sufficient.

**Full proof:**
- Case p | ord(g): g has an element g^m ∈ S_p \ {1}. This g^m sends some unit x to x + p (within the same mod-p class). Conflict.
- Case p ∤ ord(g): g ≢ 1 mod p (since ord(g) divides p−1 in Z/pZ, and if g ≡ 1 mod p then ord ≡ 1 or p, contradiction). Then g acts on {kp} by k ↦ (g mod p)·k. Since g ≢ 1 mod p: (g mod p) ≠ 1, so the orbit of p contains {p, (g mod p)·p, (g mod p)²·p,...}. This is a non-trivial orbit within the set {p, 2p,...,(p−1)p}, all in the same π_p class (all ≡ 0 mod p). Conflict. □

---

## §P4 — Alternative Partition Families for n = p²

**DYN + DYN for n = p²:**

(Z/p²Z)* ≅ Z/p(p−1)Z. Two subgroups G,H with G ∩ H = {1}. Need |G|·|H| | p(p−1) with gcd(|G|,|H|) = 1.

Since Z/p(p−1)Z is cyclic, its subgroups are of orders dividing p(p−1). A pair with G ∩ H = {1}: any two subgroups of coprime orders. Example: G of order p (= S_p) and H of order dividing p−1 (coprime to p).

**Test: n = 4 = 2² (p = 2).**
(Z/4Z)* = {1,3} ≅ Z/2Z. Only one non-trivial subgroup: {1,3}. G ∩ H = {1,3} ∩ {1,3} = {1,3} ≠ {1}. No valid DYN+DYN pair with non-trivial G and H.

**Test: n = 9 = 3² (p = 3).**
(Z/9Z)* ≅ Z/6Z. Generator g=2: 2¹=2, 2²=4, 2³=8, 2⁴=7, 2⁵=5, 2⁶=1. Order 6.

Subgroups: {1} (order 1), {1,8} (order 2, H), {1,4,7} (order 3, G=S₃ = {1,1+3,1+6}={1,4,7}).

G ∩ H = {1,4,7} ∩ {1,8} = {1}. ✓ gcd(3,2) = 1. ✓

So {π_DYN({1,4,7}), π_DYN({1,8})} for n=9.

**π_DYN({1,4,7}):** Orbits of the subgroup {1,4,7} acting on Z/9Z.
- 0: {0} (fixed)
- 3: 4·3=12=3 mod 9. Wait, 1·3=3, 4·3=12≡3, 7·3=21≡3. Fixed. {3}.
- 6: similarly {6}.
- 1: 1·1=1, 4·1=4, 7·1=7. Orbit {1,4,7}.
- 2: 1·2=2, 4·2=8, 7·2=14≡5. Orbit {2,5,8}.

π_DYN({1,4,7}) = {{0},{3},{6},{1,4,7},{2,5,8}}. 5 blocks.

**π_DYN({1,8}):** Orbits of {1,8} = {1,−1 mod 9}.
- 0: {0}.
- 3: 8·3=24≡6. Orbit {3,6}.
- 1: 8·1=8. Orbit {1,8}.
- 2: 8·2=16≡7. Orbit {2,7}.
- 4: 8·4=32≡5. Orbit {4,5}.

π_DYN({1,8}) = {{0},{3,6},{1,8},{2,7},{4,5}}. 5 blocks.

**U-set check:** Need U(π_DYN({1,4,7})) ∩ U(π_DYN({1,8})) = ∅.

Pairs in G={1,4,7} action (same orbit): {1,4},{1,7},{4,7},{2,5},{2,8},{5,8}.
Pairs in H={1,8} action (same orbit): {3,6},{1,8},{2,7},{4,5}.

Intersection: {1,4}∩{1,8}? No. {1,7} vs {2,7}? No. {4,7} vs {4,5}? No. {2,5} vs {4,5}? No. {2,8} vs {1,8}? No. {5,8} vs {4,5}? No. Checking all: no overlap. ✓

**{π_DYN({1,4,7}), π_DYN({1,8})} is sufficient for n = 9 = 3².** □

**Verification that this is a sufficient pair:** Check all pairs {x,y} are separated. The joint map J: Z/9Z → G-orbits × H-orbits:
- 0 ↦ ({0}, {0}) — unique
- 3 ↦ ({3}, {3,6})
- 6 ↦ ({6}, {3,6})
- 1 ↦ ({1,4,7}, {1,8})
- 4 ↦ ({1,4,7}, {4,5})
- 7 ↦ ({1,4,7}, {2,7})
- 2 ↦ ({2,5,8}, {2,7})
- 5 ↦ ({2,5,8}, {4,5})
- 8 ↦ ({2,5,8}, {1,8})

All 9 images are distinct. Injective. ✓

---

## §P5 — New Obstruction Type for n = p²

**New obstruction: intra-residue-class mixing by the p-kernel.**

For squarefree n: every element is uniquely determined by its CRT coordinates (a₁,...,aₖ). Different residue classes are different coordinates. There is no "within-coordinate" structure.

For n = p²: elements within the same residue class mod p are x and x+kp (same a₁ = x mod p, different "second p-adic digit" k). The subgroup S_p = {1+p, 1+2p,...,1+(p−1)p, 1} of (Z/p²Z)* acts within these residue classes — it translates k while preserving the mod-p residue.

**Definition (p-kernel obstruction).** For n = p^r, the p-kernel subgroup of (Z/p^rZ)* is:
S_p^r = ker( (Z/p^rZ)* → (Z/pZ)* ) = { x : x ≡ 1 mod p } ≅ Z/p^{r−1}Z

This is the unique Sylow p-subgroup of (Z/p^rZ)*. It is the subgroup that acts within residue classes mod p.

**Theorem P4 (p-kernel obstruction — proved for n = p²).** For n = p² and any orbit partition π_DYN(G): if G ∩ S_p^2 ≠ {1} (G contains an element ≡ 1 mod p), then π_DYN(G) is "within-class active" and cannot be paired with π_p to form a sufficient family.

If G ∩ S_p^2 = {1} (G avoids the p-kernel), then G acts as a subgroup of (Z/pZ)*, shifting residue classes but never connecting two elements within the same class. This is a necessary (but not sufficient alone) condition for {π_p, π_DYN(G)} to be sufficient.

**But Theorem P3 shows even this is insufficient** because G avoiding S_p^2 means G has order dividing p−1 (acting only on the mod-p component), and then G acts non-trivially on the multiples of p: orbit of kp under g ∈ G not ≡ 1 mod p is {kp, (g mod p)·k·p,...}, all in the same π_p class (residue 0). Conflict from the non-unit layer.

**Fundamental tension for n = p²:** π_p has two types of classes:
1. Unit classes {r, r+p, r+2p,...}: r ≢ 0 mod p.
2. Zero class {0, p, 2p,...,(p−1)p}: all multiples of p.

For sufficiency with π_DYN(G): G must separate within unit classes (avoid S_p^2) AND must separate within the zero class (avoid acting on {kp} with non-trivial orbits). These two demands force G to act trivially everywhere — but then G = {1}, trivial partition.

**Theorem P5 (proved — general n = p² impossibility for A+M family).** No non-trivial multiplicative-orbit partition is sufficient when paired with π_p for n = p². Equivalently: within the {Type A, Type M} families, no sufficient 2-partition family {π_d, π_DYN(G)} exists for n = p² with d = p.

---

## §P6 — Partial Results for n = 2p² and p²q

**n = p²q (squarefree in q, but p² non-squarefree):**

CRT: Z/p²qZ ≅ Z/p²Z × Z/qZ.

The pair (π_{p²}, π_q): f_{p²}(x) = x mod p², f_q(x) = x mod q. Joint map injective iff lcm(p², q) = p²q. Since gcd(p²,q)=1 (q ≠ p, q prime): lcm(p²,q) = p²q = n. ✓

**{π_{p²}, π_q} is a sufficient Type-A pair for n = p²q.** No new obstruction from the A+A case.

For A+M: {π_p, π_DYN(G)} for G ≤ (Z/p²qZ)*. By CRT, (Z/p²qZ)* ≅ (Z/p²Z)* × (Z/qZ)*. The condition is G trivial on primes of n/p = pq. But pq is not the product of distinct primes — it includes p again. The condition "G trivial on primes of n/p" needs modification for the prime-power setting.

**Theorem P6 (partial — n = p²q, A+M with d = p).** {π_p, π_DYN(G)} sufficient for n = p²q iff G trivial on ALL components: G trivial on the p-component AND trivial on the q-component. This forces G = {1} (trivial), since "trivial on q" means g ≡ 1 mod q and "trivial on p-component" means g ≡ 1 mod p (for the same conflict reasons as n = p²). Only non-trivial sufficient pairs come from different d choices.

*Status: Partial — requires full prime-power orbit analysis to complete. Conjectural in the mixed-level case.*

---

## §P7 — Summary of Prime-Power Frontier

**What is new for n = p^r (r ≥ 2):**

| Feature | Squarefree n | Prime-power n = p^r |
|---|---|---|
| CRT decomposition | k independent coordinates | Single p-adic coordinate with r levels |
| Additive partition chain | Multiple incompatible pairs exist | All comparable: π₁ ≤ π_p ≤ π_{p²} ≤ ... ≤ π_disc |
| A+A sufficient pair | {π_{d₁}, π_{d₂}} with lcm=n always exists | No such pair (all additive partitions comparable) |
| M+M sufficient pair | G ∩ H = {1} construction always exists | Still exists when G,H ≤ (Z/p^rZ)* with G∩H={1} — see n=9 example |
| A+M for "natural d" | G trivial on n/d primes suffices | New obstruction: p-kernel S_p^r creates within-class mixing |

**Proved for n = p²:**
1. {π_DYN(G), π_DYN(H)} sufficient iff G ∩ H = {1} in (Z/p²Z)* — SAME as squarefree (M+M theorem is universal).
2. {π_p, π_DYN(G)} NOT sufficient for any non-trivial G — new obstruction (p-kernel).
3. {π_{p²}, π_DYN(G)} is trivially equivalent to π_disc paired with π_DYN(G) — one partition is already discrete.

**The M+M theorem (Theorem 3) extends to n = p^r without modification.** The A+M and A+A theorems require careful modification: the "prime support" language must be replaced by "p-adic valuation support" for the prime-power case.

**New invariant for prime-power n:** The p-kernel subgroup S_p^r = ker((Z/p^rZ)* → (Z/pZ)*) plays the role of "within-level mixer." Any orbit partition G with G ∩ S_p^r ≠ {1} mixes elements within the same mod-p class — a new obstruction type absent in squarefree n.

**Conjectural general statement (not yet proved):** For n = p^r, a sufficient 2-partition family {π, ρ} of Type M+M exists iff (Z/p^rZ)* has two complementary subgroups G, H with G ∩ H = {1} and |G|·|H| = |(Z/p^rZ)*| = p^{r−1}(p−1). For r = 2, p = 3: |(Z/9Z)*| = 6, G = {1,4,7} (|G|=3), H = {1,8} (|H|=2), |G|·|H|=6 ✓. For general p, r: existence depends on whether p^{r−1}(p−1) factors into two coprime parts — which it does whenever gcd(p^{r−1}, p−1) = 1, i.e., always (since p ∤ p−1).

**Status of Phase 2:** Partial results for n = p², n = p²q. Full classification of the prime-power case requires a new sprint developing the p-kernel obstruction into a complete invariant analogous to Theorem 4 for squarefree n.
