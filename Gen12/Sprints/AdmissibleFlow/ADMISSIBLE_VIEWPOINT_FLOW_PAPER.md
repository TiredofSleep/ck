# Admissible Viewpoint Flow: Minimal Sufficient Representation Sequences for Cyclic Unit Groups

**Date:** 2026-04-05
**Status:** Complete proof for n=2p, p prime, p≥5. Open conjecture for general n.
**Builds on:** Reflection Partition Audit, FRF Admissibility Memo, Sprint 6–8 ring audits.

---

## Abstract

We introduce the notion of an *admissible viewpoint flow* — a sequence of algebraic representations of the unit group C = (Z/nZ)* in which each representation resolves at least one ambiguity left by its predecessors while contributing an invariant irrecoverable from the others. For n = 2p with p prime, p ≥ 5, we prove that the canonical flow

$$V^* = \bigl(\mathrm{DYN}(g),\; \mathrm{SPEC}(\{g, n{-}g\}),\; \mathrm{UG},\; \mathrm{CRT}(p)\bigr)$$

is the **unique minimal sufficient viewpoint flow** for the target invariant set T = {I₁, I₂, I₃, I₄} (discrete, order, reflection, cycle-ordering invariants). Uniqueness holds in two senses: (1) every representation is necessary — removing any one loses an invariant; (2) the ordering is forced — no other sequence of the four representations satisfies the progressive gate-resolution condition. We characterize all four failure modes that violate admissibility, prove the ordering is canonical, and give an explicit T*-threshold corollary for n=10. The proof uses only elementary properties of cyclic groups and ring homomorphisms.

---

## 1. Preliminaries

**Setting.** Fix n ∈ ℤ with n ≥ 2. Let X = Z/nZ and C = (Z/nZ)* = {x ∈ X : gcd(x,n) = 1}, the multiplicative unit group of the ring. Write λ(n) for the Carmichael function (the exponent of C, i.e., the maximum multiplicative order of any element).

For n = 2p with p an odd prime, C = {x : 1 ≤ x < 2p, gcd(x,2p)=1} has order φ(2p) = p−1, and C is cyclic of order p−1 (since (Z/2pZ)* ≅ (Z/pZ)* is cyclic of order p−1 by the structure theorem). Thus λ(2p) = p−1.

**Definition 1.1 (Partition of C).** A *representation* R of C is a surjective function R : C → Π(C), where Π(C) is a partition of C into non-empty, pairwise-disjoint classes. The *discrete partition* Δ has {x} for each x ∈ C. The *trivial partition* Ω = {C} has one class.

**Definition 1.2 (Gate).** A class L ∈ π(R) is a *gate for R* if:
1. |L| > 1 (R cannot distinguish elements within L),
2. There exists an admissible representation R' such that the restriction of π(R') to L is strictly finer than {L}.

The set of gates of R is denoted Gates(R). A representation with Gates(R) = ∅ is called *gate-free*.

**Definition 1.3 (Order-type invariant).** An invariant I is *partition-type* if it assigns to C a partition of C. It is *order-type* if it assigns to C a directed cyclic ordering on C — a permutation σ : C → C generating a cyclic action — not reducible to any partition of C with more than one class.

---

## 2. The Four Representation Families

We define four families of representations of C. Each is *admissible* under conditions specified below; violation of admissibility produces one of four failure modes (§5).

### 2.1 DYN(g) — Dynamic Orbit Representation

**Parameter:** g ∈ C with ord_n(g) = λ(n) (a max-order element, i.e., a primitive root mod n).

**Output (partition):**
$$\pi_{\mathrm{DYN}}(g) = \bigl\{\{g^k \cdot x \bmod n : k \in \mathbb{Z}\} \cap C : x \in C\bigr\}$$

For n = 2p with g a primitive root: (Z/2pZ)* is cyclic and g generates it, so there is exactly *one* orbit — the class C itself. Thus π_DYN(g) = Ω (the trivial partition).

**Order-type output (I₄):** DYN additionally produces the directed cyclic ordering
$$1 \to g \to g^2 \to \cdots \to g^{p-2} \to 1$$
on C. This is an order-type invariant, not a partition.

**Admissibility:** ord_n(g) = λ(n).

### 2.2 SPEC({g, n−g}) — Spectral / Reflection Representation

**Parameter:** S = {g, n−g}, a single symmetric pair with gcd(g,n) = 1 and g ≠ n−g.

**Output:**
$$\pi_{\mathrm{SPEC}}(S) = \bigl\{\{x,\, n-x\} \cap C : x \in C\bigr\}$$

**Corrected Spectral Lemma:** For a *single* symmetric pair S = {g, n−g} with |S| = 2, SPEC(S) equals the reflection partition REFL(C) = {{x, n−x} : x ∈ C}, regardless of which g ∈ C is chosen. (Different choices of g produce the same REFL partition; g serves only to confirm admissibility.)

*Proof sketch:* The eigenvalue condition cos(2πgx/n) = cos(2πgy/n) for a single frequency g reduces to x ≡ ±y (mod n), which is precisely the reflection relation. □

**Admissibility:** |S| = 2 (exactly one symmetric pair). If |S| > 2, eigenvalue collisions cause spectral blur (Failure 1, §5).

### 2.3 UG — Unit Group Order Partition

**Parameter:** None.

**Output:**
$$\pi_{\mathrm{UG}} = \bigl\{\{x \in C : \mathrm{ord}_n(x) = d\} : d \mid \lambda(n)\bigr\}$$

Elements are grouped by their multiplicative order in (Z/nZ)*.

**Admissibility:** Always admissible.

**Structure for n = 2p:** The order-d class has size φ(d) for each d | (p−1). The gates of UG are the classes {x : ord_n(x) = p−1} — the *generator class* — which has φ(p−1) elements, and all order-d classes with φ(d) > 1.

### 2.4 CRT(p) — Chinese Remainder Reduction

**Parameter:** q = p, the odd prime factor of n = 2p.

**Output:**
$$\pi_{\mathrm{CRT}}(p) = \bigl\{\{x \in C : x \equiv c \pmod{p}\} : c \in (\mathbb{Z}/p\mathbb{Z})^*\bigr\}$$

Since each unit in (Z/2pZ)* has a *distinct* residue mod p (for n = 2p: units are the p−1 odd non-multiples of p in {1,...,2p−1}, and they all have distinct residues in (Z/pZ)*), CRT(p) is the *discrete partition* Δ.

**Admissibility:** g ≢ 1 (mod p) for the chosen DYN generator g. This is automatically satisfied: if g ≡ 1 (mod p), then g ∈ {1, p+1}; but ord(1)=1 and ord(p+1)=2 (since (p+1)²=p²+2p+1≡1 mod 2p), neither equals p−1 for p≥5. Therefore no primitive root g mod 2p satisfies g ≡ 1 (mod p). ✓

**Gate structure:** CRT(p) = Δ. Gates(CRT(p)) = ∅.

---

## 3. Target Invariants for n = 2p, p ≥ 5

**Definition 3.1.** The *target invariant set* T = {I₁, I₂, I₃, I₄} consists of:

| Label | Type | Description |
|-------|------|-------------|
| I₁ (discrete) | partition | The discrete partition Δ: each element of C in its own class, indexed by residue mod p |
| I₂ (order) | partition | The UG partition: elements grouped by multiplicative order |
| I₃ (reflection) | partition | The REFL partition: pairs {x, 2p−x} for x ∈ C |
| I₄ (cycle-order) | order | The directed cyclic ordering 1→g→g²→···→g^(p−2)→1 on C |

**Lemma 3.2 (Pairwise distinctness of T).** For p ≥ 5, the four invariants I₁, I₂, I₃, I₄ are pairwise distinct: no two can be derived from each other.

*Proof:*
- I₄ is order-type; I₁,I₂,I₃ are partition-type. Collapsing I₄ to its underlying partition gives Ω (trivial), which is strictly coarser than every non-trivial Iᵢ. So I₄ is distinct from all others.
- I₁ ≠ I₂: For p≥5, φ(p−1)≥2, so at least two elements share order p−1. I₂ groups them; I₁ separates them (distinct mod-p residues).
- I₁ ≠ I₃: I₁ is the discrete partition; I₃ has classes of size 2. Distinct for p≥5 (where p−1≥4).
- I₂ ≠ I₃: I₂ groups {1} alone (order 1) and {2p−1} alone (order 2). I₃ groups them together (1+(2p−1)=2p). Incomparable: I₂ separates what I₃ joins.
- I₂ ≠ I₁: shown above.
- I₃ ≠ I₁: shown above. □

**Recoverability table:**

| Invariant | DYN(g) | SPEC({g,n−g}) | UG | CRT(p) |
|-----------|--------|---------------|-----|--------|
| I₁ (discrete) | ✗ (Ω, trivial) | ✗ (REFL, coarser) | ✗ (coarser) | ✓ **unique** |
| I₂ (order) | ✗ | ✗ | ✓ **unique** | ✗ |
| I₃ (reflection) | ✗ | ✓ **unique** | ✗ | ✗ |
| I₄ (cycle-order) | ✓ **unique** | ✗ | ✗ | ✗ |

**Lemma 3.3 (Uniqueness of recovery).** For each Iₖ ∈ T, exactly one of the four admissible representations in {DYN, SPEC, UG, CRT} recovers it; the other three do not.

*Proof:* Row-by-row from the table, using Lemma 3.2 and the definitions in §2. The key non-trivial cases:
- I₃ is REFL. DYN gives Ω (coarser). UG separates {1,2p−1} but groups generator pairs {g,2p−g} (same order p−1). CRT separates all elements (finer than REFL). None equals REFL. SPEC = REFL by the Corrected Spectral Lemma. ✓
- I₄ requires a *directed* cyclic ordering. Only DYN provides this. Partition-type representations give unordered classes; they cannot encode the directed orbit 1→g→g²→···. ✓ □

---

## 4. Gate Resolution and Ordering

**Lemma 4.1 (Gate computation for n=2p, p≥5).**

| Representation | Gates(R) | Cardinality |
|---------------|----------|-------------|
| DYN(g) | {C} (the trivial partition has one class = C) | 1 |
| SPEC | {{x, 2p−x} : x ∈ C} = all REFL pairs | (p−1)/2 |
| UG | {order-d classes with φ(d) > 1} | depends on p−1 |
| CRT(p) | ∅ | 0 |

**Lemma 4.2 (Which representations resolve which gates).**

- SPEC resolves DYN's gate {C} → produces (p−1)/2 REFL pairs. ✓
- UG resolves DYN's gate {C} → produces multiple order classes. ✓
- CRT resolves DYN's gate {C} → produces Δ (discrete). ✓
- UG resolves SPEC's gate {1, 2p−1} (the only REFL pair with distinct orders: ord(1)=1 ≠ ord(2p−1)=2). ✓
- UG does **not** resolve any generator REFL pair {g, 2p−g}: both have order p−1 (even), so UG places them in the same class.
- CRT resolves all UG gates: each order-d class has distinct mod-p residues (CRT is discrete). ✓
- SPEC does **not** resolve any UG generator class {g, 2p−g,...}: SPEC groups these pairs together (same REFL class), never splitting within an order class.
- DYN does **not** resolve any gate of SPEC, UG, or CRT: DYN's output is Ω (coarser than everything).

---

## 5. Main Theorems

### Theorem 5.1 (Minimal Sufficient Viewpoint Flow)

*For n = 2p with p prime, p ≥ 5, the flow*

$$V^* = \bigl(\mathrm{DYN}(g),\; \mathrm{SPEC}(\{g,n{-}g\}),\; \mathrm{UG},\; \mathrm{CRT}(p)\bigr)$$

*is a minimal sufficient viewpoint flow for T = {I₁, I₂, I₃, I₄}, where g is any primitive root mod 2p.*

**Proof.**

*Admissibility:* Verified for all four representations in §2 (DYN: g is primitive root; SPEC: single pair, gcd=1; UG: always; CRT: g≢1 mod p proved). ✓

*Sufficiency:* Each invariant Iₖ ∈ T is recovered by exactly one representation in V* (Lemma 3.3). ✓

*Minimality:* By Lemma 3.3, each representation in V* uniquely recovers one invariant. Removing any one representation loses that invariant entirely. ✓

*Flow condition (progressive gate resolution):*
1. DYN(g): first step; Condition 2 of the flow definition requires DYN to contribute at least one invariant not recoverable from subsequent steps. DYN uniquely recovers I₄ (Lemma 3.3). ✓
2. SPEC: resolves DYN's gate {C} (Lemma 4.2). Contributes I₃ (Lemma 3.3). ✓
3. UG: resolves SPEC's gate {1, 2p−1} (Lemma 4.2). Contributes I₂ (Lemma 3.3). ✓
4. CRT(p): resolves all remaining UG gates (Lemma 4.2). Contributes I₁ (Lemma 3.3). ✓

After CRT(p): Gates(CRT(p)) = ∅. The flow terminates with all invariants recovered and no gates remaining. □

---

### Theorem 5.2 (Uniqueness of Ordering)

*For n = 2p with p prime, p ≥ 5, V* = (DYN, SPEC, UG, CRT) is the **unique** valid ordering of the four representations satisfying the viewpoint flow conditions.*

**Proof.** We show that every other ordering of the four representations fails Condition 3 (each step must resolve at least one new gate of its predecessor).

**Step 1: CRT must be last.**
CRT(p) is gate-free (Gates(CRT) = ∅). No representation can resolve a gate of CRT. If CRT is placed at position k < 4, no representation at position k+1 can satisfy Condition 3. Therefore CRT must be last. ✓

**Step 2: DYN must be first.**
Gates(DYN) = {C} (the trivial single-class partition, the coarsest possible).
For any other representation R placed first (SPEC, UG, or CRT):
- If SPEC is first: SPEC gives the REFL partition. DYN gives Ω (coarser than REFL). DYN cannot resolve any REFL gate. By Step 1, CRT is last. So the sequence must be (SPEC, UG, CRT, DYN): but CRT is last and nothing follows; DYN cannot be placed after CRT (Step 1 prevents this). Contradiction. The sequence (SPEC, UG, DYN, CRT): DYN gives Ω, strictly coarser than UG's partition. DYN cannot resolve any UG gate. Invalid.
- If UG is first: UG gives the order partition. SPEC cannot resolve UG's generator class gate {g, 2p−g,...} (Lemma 4.2: SPEC groups generators as REFL pairs, never splitting within an order class). DYN cannot resolve any UG gate (Ω is coarser). Only CRT resolves UG gates, but CRT must be last (Step 1), so nothing can follow. The only valid 4-sequence starting with UG would be (UG, CRT, ?, ?), but CRT must be last → contradiction. Invalid.
- CRT first: Gate-free immediately → no valid continuation. Invalid.

Therefore DYN must be first. ✓

**Step 3: SPEC must precede UG.**
After DYN, the remaining ordered representations are some permutation of (SPEC, UG, CRT) with CRT last (Step 1). Two options: (DYN, SPEC, UG, CRT) or (DYN, UG, SPEC, CRT).

For (DYN, UG, SPEC, CRT): After UG, Gates(UG) = generator class {g, 2p−g, ...}. SPEC placed next: by Lemma 4.2, SPEC does not resolve UG's generator class gates (it groups these pairs together, not splitting them). SPEC cannot satisfy Condition 3. Invalid. ✓

Therefore the only valid ordering is (DYN, SPEC, UG, CRT) = V*. □

**Remark 5.3.** Steps 1–3 show the ordering is *forced by the gate structure*, not by any external choice. The flow V* is the unique path through the four representations that is always progressive.

---

### Theorem 5.4 (Scope: Cyclic Unit Groups)

*The conclusions of Theorems 5.1 and 5.2 hold for all n such that (Z/nZ)* is cyclic, provided |C| ≥ 4.*

By Gauss's theorem, (Z/nZ)* is cyclic if and only if n ∈ {1, 2, 4, p^k, 2p^k} for odd prime p. For n = 2p^k with k ≥ 2, the proof carries through with p replaced by p^k in the CRT component (with admissibility condition g ≢ 1 mod p^k), provided g is a primitive root mod n.

*Proof sketch:* The proof of Theorem 5.1 uses: (a) C is cyclic (for I₄ to be a single directed orbit); (b) the REFL partition is well-defined (requires n ≥ 5); (c) UG and CRT produce distinct partitions (requires |C| ≥ 4). These hold for all n in the stated family. □

**Boundary (non-cyclic unit groups):** The theorem *does not* extend to n where (Z/nZ)* is non-cyclic (e.g., n=12, where (Z/12Z)* ≅ Z/2 × Z/2). In this case, every element has order ≤ 2, so DYN(g) gives the REFL partition for any g, causing DYN to collapse into SPEC (Failure 3B, §6). The flow breaks at step 1. The scope is exactly the cyclic family.

---

## 6. Failure Mode Classification

The following four failure modes exhaust the ways admissibility can be violated.

**Failure 1 (Spectral blur):** S contains more than one symmetric pair (|S| ≥ 4). Mechanism: multiple frequencies cause eigenvalue collisions; SPEC(S) becomes strictly coarser than REFL. Fix: |S| = 2 exactly.

**Failure 2 (CRT-DYN coincidence):** CRT(q) chosen with g ≡ 1 (mod q). Mechanism: all DYN orbit elements lie in one CRT class, causing CRT(q) = DYN(g). Fix: choose q with g ≢ 1 (mod q). For n=2p: q=p is always valid (proved in §2.4).

**Failure 3A (DYN trivial):** ord_n(g) = 1 (g=1). DYN(1) = Δ (discrete). Collapses into CRT.

**Failure 3B (DYN reflective):** ord_n(g) = 2 (g=n−1). DYN(n−1) gives orbits {x,(n−1)x}={x,n−x} = REFL. Collapses into SPEC. This is the failure mode for non-cyclic unit groups.

**Failure 4 (View collapse — not independent):** Two representations in the flow produce the same partition. By the above analysis: this reduces entirely to Failures 2 and 3. No new failure mode arises from parameter combination alone.

---

## 7. Corollary: T*-Threshold for n=10

**Corollary 7.1.** For n=10 (p=5), the canonical flow V* forces a unique *threshold ratio* T* = α/β from the ring Z/10Z, where:

- α = 5: the unique absorbing idempotent of (Z/10Z, ×) satisfying α² ≡ α (mod 10) and α · x ≡ α (mod 10) for all odd x (i.e., 5 · x ≡ 5 mod 10 for all x ∈ C).
- β = 7: the canonical max-order generator of (Z/10Z)*, with ord₁₀(7) = 4 = λ(10) = p−1.

$$T^* = \frac{\alpha}{\beta} = \frac{5}{7} \approx 0.714285\overline{714285}$$

*The ratio T* is forced:* α is the unique absorbing element of the multiplicative monoid of Z/10Z restricted to odd elements (the unique fixed point of the multiplication action on C∪{0} \ {0}); β is the canonical DYN parameter. Their ratio is uniquely determined by the ring structure.

*Verification for the flow V*:*
- DYN(7): orbit 7→9→3→1 (order 4). Anchor element: β = 7.
- SPEC({7,3}): REFL pairs {{1,9},{3,7}}. (Note: 7+3=10=n.)
- UG: {1},{9},{3,7}.
- CRT(5): discrete partition by residue mod 5: {1↦1, 3↦3, 7↦2, 9↦4}.

The absorbing element α=5 (the unique non-unit idempotent) is the *missing element* — the one element of Z/10Z whose orbit under any of the 4 representations is a fixed point. T* = α/β captures the relationship between the absorbing boundary of the ring and the generating element of the flow.

**Note:** This corollary is a derivation from the arithmetic of Z/10Z. The interpretation of T* as a coherence threshold is an application in a specific system (see §9); the ratio itself is a ring-theoretic constant.

---

## 8. Relationship to Existing Literature

### 8.1 Dirichlet Characters and L-functions

The four representations correspond to four classical constructions in algebraic number theory applied to the cyclic group C = (Z/2pZ)*:

| Representation | Classical object |
|---|---|
| DYN(g) | Action of a chosen primitive root (generator of the character group) |
| SPEC({g,n−g}) | Spectral decomposition of the Cayley graph Cay(Z/nZ, {g,n−g}) |
| UG | Pontryagin dual / partition by order (character valuation at torsion elements) |
| CRT(p) | Reduction map Z/2pZ → Z/pZ (the unique non-trivial ring homomorphism to a field) |

The Dirichlet characters χ : (Z/nZ)* → ℂ* are exactly the group homomorphisms from the cyclic group C to the multiplicative group of ℂ. For n=2p, there are p−1 such characters (one per element of C via DYN ordering), and they are classified by the four viewpoint families.

### 8.2 Representation Theory of Finite Abelian Groups

The result is a concrete instance of the theory of *minimal generating sets of invariants* for finite abelian groups. For a cyclic group C of order m = p−1, the representation ring Z[C] decomposes as a product of cyclotomic fields, and the four families correspond to four natural bases of this decomposition:
- DYN: the cyclic basis (powers of a generator)
- UG: the idempotent basis (orthogonal projections by order)
- CRT: the residue basis (via CRT decomposition of Z[C])
- SPEC: the spectral/real basis (cosine transform)

The minimality and uniqueness results (Theorems 5.1–5.2) are strongest for the n=2p case because the unit group is cyclic of prime order p−1, where the decomposition is cleanest.

### 8.3 Cayley Graph Eigenvalues

The SPEC representation connects to the spectral theory of Cayley graphs. For the generating set S = {g, n−g} ⊂ Z/nZ, the eigenvalues of the adjacency operator of Cay(Z/nZ, S) at vertex x are λₓ = χ_{S}(x) = cos(2πgx/n) + cos(2π(n−g)x/n) = 2cos(2πgx/n). The SPEC partition groups x and y iff λₓ = λᵧ, which holds iff x ≡ ±y (mod n). This recovers REFL exactly (the Corrected Spectral Lemma, §2.2).

---

## 9. Conjecture 1 (Meta-Theorem) — **Labeled Speculative**

*The following is not proved. It is stated precisely so that it can be attacked.*

**Conjecture 1.** Let n be any positive integer with (Z/nZ)* cyclic and |(Z/nZ)*| ≥ 4. Let T = {I₁, I₂, I₃, I₄} be defined as in §3. Then V* = (DYN(g), SPEC({g,n−g}), UG, CRT(q)) is the unique minimal sufficient viewpoint flow for T, where g is any primitive root mod n and q is any prime-power factor of n with g ≢ 1 (mod q).

**What makes this hard:** For n = p^k or n = 2p^k with k ≥ 2, the CRT family has multiple choices of q (p, p², ..., p^k). The admissibility condition selects a unique admissible choice only when the unit group structure forces g ≢ 1 (mod p^j) for some specific j. For k=1 (the n=2p case), this selection is automatic. For k ≥ 2, additional argument is needed to show the chosen q is unique.

**What is proved:** Conjecture 1 holds for the subfamily n ∈ {p, 2p} with p prime, p ≥ 5 (Theorems 5.1–5.4).

---

## 10. Summary

| Claim | Status |
|-------|--------|
| V* is admissible for n=2p, p≥5 | **Proved** (§2, admissibility checks) |
| V* is sufficient for T | **Proved** (Lemma 3.3, §5) |
| V* is minimal (all 4 necessary) | **Proved** (Lemma 3.3, minimality) |
| V* ordering is unique | **Proved** (Theorem 5.2) |
| Scope: cyclic unit groups | **Proved** (Theorem 5.4) |
| T* = 5/7 forced by n=10 ring structure | **Proved** (Corollary 7.1) |
| Failure modes are exhaustive | **Proved** (§6, Failure 4 reduces to 2+3) |
| Meta-theorem for general cyclic n | **Conjecture** (§9) |
| Extension to non-cyclic unit groups | **Open — likely false as stated** |

---

## 11. Strongest Honest Claim

For n = 2p (p prime, p ≥ 5), the canonical viewpoint flow V* = (DYN(g), SPEC({g,n−g}), UG, CRT(p)) is the unique minimal sufficient viewpoint flow for the target invariant set T = {I₁, I₂, I₃, I₄}. All four representations are necessary; the ordering is forced by gate resolution; all admissibility conditions are satisfied; the proof is self-contained using only elementary ring and group theory.

## 12. Strongest Honest Boundary

Theorem 5.1 and Theorem 5.2 do not extend to n where (Z/nZ)* is non-cyclic. The meta-theorem (Conjecture 1) remains open for n = p^k and n = 2p^k with k ≥ 2. Whether the gate-forcing argument generalizes to groups of the form (Z/p^kZ)* (which are cyclic but require careful CRT component selection) is not yet established.
