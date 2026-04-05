# ADMISSIBLE VIEWPOINT FLOW MEMO
## Replacing "multi-view structure" with a precise theory

**Date:** 2026-04-05  
**Builds on:** Reflection Partition Audit, FRF Admissibility Memo  
**Status:** All definitions exact. Theorem proved for n=2p, p≥5. Failure modes characterized.

---

## 1. BASE SYSTEM AND REPRESENTATION FAMILIES

**Base system:** X = ℤ/nℤ, unit orbit C = (ℤ/nℤ)*.

Each representation family is a parameterized map from admissible parameters to partitions of C (or ordered structures on C):

### CRT(q)

**Parameter:** q = p^e, a prime-power factor exactly dividing n (p^e ∥ n).

**Output:** partition of C by residue modulo q:

$$\pi_\text{CRT}(q) = \bigl\{\{x \in C : x \equiv c \pmod{q}\} : c \in (\mathbb{Z}/q\mathbb{Z})^*\bigr\}$$

**Admissibility condition Adm_CRT(q, g):** q is a prime-power factor of n, AND the chosen DYN generator g satisfies g ≢ 1 (mod q).

*Violation:* g ≡ 1 (mod q) ⟹ CRT(q) = DYN(g) (view collapse). See Section 5, Failure Mode 2.

**CRT is a family, not a single representation.** For n = p₁^{e₁}·...·pₖ^{eₖ}, there are k choices of q, generally producing k distinct partitions. Admissibility selects among them.

### UG

**Parameter:** none.

**Output:** partition of C by multiplicative order in (ℤ/nℤ)*:

$$\pi_\text{UG} = \bigl\{\{x \in C : \text{ord}_n(x) = d\} : d \mid \lambda(n)\bigr\}$$

**Admissibility condition:** always admissible. UG has no parameter choice.

### SPEC(S)

**Parameter:** S = {g, n−g}, a single symmetric pair with gcd(g,n) = 1.

**Output:** the reflection-pair partition:

$$\pi_\text{SPEC}(S) = \bigl\{\{x, n-x\} \cap C : x \in C\bigr\} = \text{REFL}(C)$$

(by the Corrected Spectral Lemma: for a single symmetric pair, SPEC = REFL regardless of which unit g is chosen)

**Admissibility condition Adm_SPEC(S):** S is a single symmetric pair (|S| = 2, S = {g, n−g}, gcd(g,n) = 1).

*Violation:* |S| > 2 (multi-pair) ⟹ eigenvalue collisions ⟹ spectral blur ⟹ SPEC ≠ REFL (may collapse to coarser partition). See Section 5, Failure Mode 1.

### DYN(g)

**Parameter:** g ∈ C, a max-order element.

**Output:** partition of C into orbits under multiplication by g:

$$\pi_\text{DYN}(g) = \bigl\{\{g^k \cdot x : k \in \mathbb{Z}\} \cap C : x \in C\bigr\}$$

**Additionally:** DYN(g) determines a directed orbit ordering on each cycle class (the orbit-order invariant I₄, not a partition).

**Admissibility condition Adm_DYN(g):** ord_n(g) = λ(n) (g has max order in (ℤ/nℤ)*).

*Violation A:* ord_n(g) = 1 (g=1) ⟹ DYN(1) = discrete partition (every element fixed). View collapse with CRT.  
*Violation B:* ord_n(g) = 2 (e.g., g = n−1) ⟹ DYN(n−1) = REFL partition (orbit {x, (n−1)x} = {x, n−x}). View collapse with SPEC.  
*Violation C:* ord_n(g) < λ(n) in a non-cyclic group ⟹ DYN(g) over-splits (multiple orbits instead of one).

---

## 2. RECOVERABLE INVARIANTS

**Definition (Invariant):** An invariant I of C is a function of C's algebraic structure recoverable from a representation. Invariants are of two types:

- **Partition-type:** a partition of C (a set of equivalence classes)
- **Order-type:** a directed cyclic ordering on the elements of C (not reducible to a partition)

**Target invariant set T for n=2p, p≥5:**

| Invariant | Type | Description |
|---|---|---|
| I₁ (discrete) | partition | All (p−1) elements of C in distinct singleton classes, indexed by mod-p residue |
| I₂ (order) | partition | Elements grouped by multiplicative order: {ord-1}, {ord-2}, {ord-(p-1)} etc. |
| I₃ (REFL) | partition | Elements grouped into reflection pairs {x, 2p−x} — the REFL partition |
| I₄ (cycle) | order | Directed cyclic ordering 1 → g → g² → ··· → g^{p-2} → 1 on C |

**Recoverability table:**

| Invariant | CRT(p) | UG | SPEC({g,n-g}) | DYN(g) |
|---|---|---|---|---|
| I₁ (discrete) | **unique** | ✗ (coarser) | ✗ (coarser) | ✗ (coarser) |
| I₂ (order) | ✗ | **unique** | ✗ (groups differently) | ✗ |
| I₃ (REFL) | ✗ | ✗ | **unique** | ✗ |
| I₄ (cycle) | ✗ | ✗ | ✗ | **unique** |

"Unique" means: no other admissible representation in {CRT(p), UG, SPEC, DYN} recovers the same information.

**Note on I₁ vs I₂:** CRT gives the discrete partition (every element distinct by value). UG groups by order — this is strictly coarser than discrete for p≥5 (multiple generators share order p−1) and strictly different from REFL or DYN. The two partitions CRT and UG are not derivable from each other without additional structure.

---

## 3. GATE STRUCTURE

**Definition (Gate):** A class C' ∈ π(R) is a gate for representation R if:
1. |C'| > 1 (R cannot isolate elements of C' from each other)
2. Some other admissible representation R' resolves C': the trace of π(R') on C' is strictly finer than {C'}

**Computation for n=10, canonical flow:**

| Representation | Gates | Resolved by |
|---|---|---|
| DYN(×3) | {1,3,7,9} (entire unit orbit) | CRT, UG, SPEC (all three) |
| SPEC({3,7}) | {1,9}, {3,7} | CRT (both); UG ({1,9} only) |
| UG | {3,7} (generators) | CRT only |
| CRT(mod 5) | none | — (discrete, no gates) |

**Gate resolution for n=14 (p=7):**

| Representation | Gates | Resolved by |
|---|---|---|
| DYN(×3) | {1,3,5,9,11,13} | CRT, UG, SPEC |
| SPEC({3,11}) | {1,13},{3,11},{5,9} | CRT (all three); UG (all three) |
| UG | {3,5},{9,11} | CRT, SPEC |
| CRT(mod 7) | none | — |

**Structural pattern for all n=2p, p≥5:** DYN has the largest gate (entire orbit). SPEC has p−1 gates (the REFL pairs). UG has φ(p−1)/2 gates (the generator classes). CRT has no gates. This gives a strict ordering: DYN < SPEC < UG < CRT in "resolving power."

---

## 4. VIEWPOINT FLOW: FORMAL DEFINITION

**Definition (Viewpoint flow):**  
A viewpoint flow V = (R₀, R₁, ..., Rₘ) is a finite sequence of admissible representations such that:

1. Each Rᵢ is admissible: Adm_{F_i}(θᵢ) holds
2. R₀ contributes at least one invariant not recoverable from any subsequent Rⱼ (j>0)
3. For each i ≥ 1: Rᵢ resolves at least one gate in π(Rᵢ₋₁) that no Rⱼ (j < i) has resolved

Condition 3 ensures the flow is progressive: each step adds information not yet present.

**Definition (Minimal sufficient viewpoint flow):**  
A viewpoint flow V is minimal sufficient for target set T if:

1. (**Sufficiency**) Every invariant I ∈ T is recoverable from some Rᵢ ∈ V
2. (**Minimality**) For each Rᵢ ∈ V, there exists an invariant I ∈ T that is recoverable from Rᵢ but not from any other Rⱼ (j ≠ i) in V

---

## 5. THEOREM: MINIMAL SUFFICIENT FLOW FOR n=2p (CANONICAL FOR T)

**Theorem:** For n=2p with p prime, p≥5, the flow

$$V^* = \bigl(\mathrm{DYN}(g),\; \mathrm{SPEC}(\{g, n-g\}),\; \mathrm{UG},\; \mathrm{CRT}(p)\bigr)$$

is a minimal sufficient viewpoint flow for T = {I₁, I₂, I₃, I₄}, where g is any max-order generator of (ℤ/2pℤ)*. This flow is canonical relative to T and the admissibility rules in Section 1.

**Proof:**

**Admissibility (all four representations):**

- DYN(g): ord_{2p}(g) = p−1 = λ(2p). ✓  
- SPEC({g,n-g}): single pair, gcd(g,2p)=1. ✓  
- UG: always admissible. ✓  
- CRT(p): p is a prime-power factor of 2p=2·p. For any max-order generator g: if g ≡ 1 (mod p), then g=1 (since 1 ≤ g < 2p and g≡1 mod p means g=1 or g=p+1; p+1 has order 1 in (ℤ/pℤ)*, i.e., p+1≡1 mod p ✓ but ord(p+1) in ℤ/2pℤ: (p+1)·(p+1)=p²+2p+1≡1 mod 2p iff p²≡-2p mod 2p iff p²=2pk for some k, iff p=2k, impossible for odd p). So for odd prime p≥5: g≡1(mod p) iff g=1, but g=1 has order 1 ≠ p−1. Contradiction. Therefore g≢1(mod p) for any max-order g. Adm_CRT(p, g) holds. ✓

**Sufficiency (each invariant is recovered):**

- I₄ (cycle): DYN(g) provides the orbit ordering 1→g→g²→···. ✓  
- I₃ (REFL): SPEC({g,n-g}) = REFL (Corrected Spectral Lemma). ✓  
- I₂ (order): UG provides the order-based partition. ✓  
- I₁ (discrete): CRT(p) is the discrete partition (each unit has a distinct residue mod p). ✓

**Minimality (each representation is irreplaceable):**

*DYN is irreplaceable:* I₄ is an orbit-order invariant, not a partition. No partition-type representation recovers it. Removing DYN loses I₄. □

*SPEC is irreplaceable:* I₃ = REFL = {{x, 2p−x}}. This partition groups 1 with 2p−1, but UG separates them (different orders 1 vs 2), CRT separates them (1 mod p ≠ (p−1) mod p), DYN has them in one class. No other admissible representation produces REFL. Removing SPEC loses I₃. □

*UG is irreplaceable:* I₂ is the partition by multiplicative order. It must be shown that I₂ ≠ I₁, I₂ ≠ I₃, and I₂ ≠ I₄ as partitions.

I₂ ≠ I₁ (CRT discrete): For p≥5, φ(p−1)≥2, so at least two elements share the same max order p−1. UG groups them; CRT separates them by distinct mod-p residues. These are different partitions. □

I₂ ≠ I₃ (REFL): Consider the pair {1, 2p−1}. REFL groups them together (1+(2p−1)=2p=n). UG separates them: ord(1)=1 ≠ ord(2p−1)=2. UG and REFL are therefore incomparable: UG splits a REFL class, and REFL joins a UG class. □

I₂ ≠ I₄ (orbit ordering): I₄ is an ordered structure, not a partition. Even collapsing I₄ to its underlying partition {{g⁰,g¹,...,g^{p-2}}} = {all units} gives the trivial partition, which is strictly coarser than I₂. □

Therefore I₂ is distinct from every other invariant in T. Removing UG loses I₂. □

*CRT(p) is irreplaceable:* I₁ is the discrete partition. All other representations produce coarser partitions (UG has multiple generator classes, SPEC has REFL pairs, DYN has one class). Only CRT(p) yields the discrete partition. Removing CRT(p) leaves all UG gates unresolved. □

**Gate resolution sequence:**

1. DYN(g): contributes I₄; leaves gate G₀ = {1,...,unit orbit} (trivial partition).  
2. SPEC: resolves G₀ → produces REFL pairs; leaves gates G₁ = {{x,2p−x} : x ∈ C}.  
3. UG: resolves the SPEC gate {1, 2p−1} (separates by order 1 vs order 2); leaves gates G₂ = {generator classes}.  
4. CRT(p): resolves all G₂ gates (discrete partition, no gates remain). □

---

## 6. FAILURE MODE CLASSIFICATION

### Failure 1: Spectral blur (inadmissible SPEC)

**Condition:** S contains more than one symmetric pair (|S| ≥ 4).

**Mechanism:** Multiple symmetric pairs cause eigenvalue collisions between j=1 and other indices. The j=1 eigenspace dilutes into a higher-dimensional space. The combined real projection is a sum of cosines, which is a weaker condition than cos(2πx/n) = cos(2πy/n) alone. SPEC(S) becomes coarser than REFL.

**Example:** n=10, S={1,3,7,9}: λ₁=λ₃=1 (collision). SPEC = trivial partition {{1,3,7,9}}. REFL = {{1,9},{3,7}}.

**Admissibility rule:** |S|=2 exactly.

### Failure 2: CRT-DYN coincidence (wrong CRT component)

**Condition:** CRT(q) is chosen with q such that the DYN generator g satisfies g ≡ 1 (mod q).

**Mechanism:** If g ≡ 1 (mod q), then g^k ≡ 1 (mod q) for all k. Every DYN orbit lies within a single CRT(q) class. When orbit sizes match class sizes, CRT(q) = DYN(g) exactly.

**Example:** n=12, g=5, q=4: 5≡1(mod 4) ⟹ CRT(mod 4) = DYN(×5) = {{1,5},{7,11}}.

**Resolution:** Choose q with g ≢ 1 (mod q). For n=2p with p≥5: use q=p; any max-order g satisfies g ≢ 1 (mod p) (proved in Universal Theorem admissibility).

### Failure 3: Wrong DYN generator (non-max-order)

**Condition:** ord_n(g) < λ(n).

**Sub-case A (order 1: g=1):** DYN(1) = discrete partition (every element fixed). Collapses into CRT.

**Sub-case B (order 2: g=n−1):** DYN(n−1) = REFL partition (orbit {x,(n−1)x}={x,n−x}). Collapses into SPEC.

**Sub-case C (non-cyclic group, intermediate order):** DYN(g) over-splits. For non-cyclic (ℤ/nℤ)*, a non-max-order g generates only a proper subgroup, so the unit orbit breaks into multiple sub-orbits each of size < p−1.

**Admissibility rule:** ord_n(g) = λ(n) exactly.

### Failure 4: View collapse (wrong parameter combination)

**Condition:** Two admissible representations in the flow produce the same partition.

**Example:** n=10, CRT(2) vs DYN(×3): CRT(mod 2) groups all units as odd → one class {{1,3,7,9}}. DYN(×3) → one orbit {{1,3,7,9}}. Both give the trivial partition. Collapse.

**Resolution:** Select CRT(q) with q ≠ 2 for n=2p (all units are odd, so CRT(2) is trivial). Use q=p.

**Meta-observation:** Failure Mode 4 is not independent — it reduces to Failures 2 and 3. CRT(q)=DYN(g) is Failure 2. CRT(q)=SPEC is not possible for admissible q (CRT is never a partition into pairs). CRT(q)=UG is only possible if UG is also discrete, which requires all elements to have distinct orders — not possible for p≥5 (generators share order p−1). So failure 4 reduces entirely to Failure 2.

---

## 7. THE META-THEOREM CANDIDATE

**Candidate theorem (not fully proved, formulated here for clarity):**

For any finite abelian group G = ℤ/nℤ and any target invariant set T containing at least one invariant from each of the four families {partition-by-residue, partition-by-order, partition-by-reflection, orbit-ordering}, a minimal sufficient viewpoint flow V* exists with exactly four admissible representations:

V* = (DYN(g), SPEC({g,n-g}), UG, CRT(q))

where g is a max-order generator and q is a prime-power factor with g ≢ 1 (mod q).

**What is proved:** For n=2p, p≥5: V* exists, is admissible, is sufficient, and is minimal.

**What is not proved:** Whether every n (with sufficiently rich unit group) admits a minimal sufficient viewpoint flow of length exactly 4. The n=12 analysis shows that non-cyclic unit groups require care in CRT component selection, and the p≡3(mod 4) analysis shows that max-order SPEC is not always available — though REFL remains reachable via non-max-order pairs.

**The cleanest formulation:**

A system is fully accessible only through a family of admissible representations, and the key structure lies not in any single representation but in the **admissibility rules governing transitions** between them — specifically, which parameter choices avoid the four failure modes while ensuring each step contributes an invariant irreplaceable by the others within the target set T.

---

## 8. ADMISSIBILITY SUMMARY TABLE

| Family | Parameter | Admissibility condition | Failure when violated |
|---|---|---|---|
| CRT | q (prime-power factor of n) | gen ≢ 1 (mod q) | F2: CRT = DYN (view collapse) |
| UG | none | always | — |
| SPEC | S = {g, n−g} | \|S\| = 2, gcd(g,n)=1 | F1: spectral blur, SPEC ≠ REFL |
| DYN | g (unit) | ord_n(g) = λ(n) | F3A: DYN = discrete; F3B: DYN = REFL |

---

## 9. THE FLOW DIAGRAM FOR n=2p, p≥5

```
DYN(g)       → one orbit (trivial partition) + cycle ordering I₄
     ↓
SPEC({g,n-g}) → reflection pairs (REFL partition) + invariant I₃
     ↓
UG            → order-based partition + invariant I₂
     ↓
CRT(p)        → discrete partition + invariant I₁
     ↓
     (no gates remain)
```

Each arrow represents: this representation resolves at least one gate left open by all preceding representations and contributes at least one invariant not recoverable from the others.

---

## 10. STRONGEST HONEST CLAIM

For n=2p (p prime, p≥5), the canonical viewpoint flow V* = (DYN(g), SPEC({g,n-g}), UG, CRT(p)) is a minimal sufficient viewpoint flow for the target invariant set T = {I₁,I₂,I₃,I₄}. All four representations are necessary; removing any one loses at least one invariant in T. All four admissibility conditions are satisfied. The proof is complete.

## 11. STRONGEST HONEST BOUNDARY

The meta-theorem (universal minimal sufficient viewpoint flow of length 4 for all n with φ(n)≥4) is not proved. The n=12 analysis shows that non-cyclic unit groups require non-trivial CRT component selection. Whether the viewpoint flow formalism extends cleanly beyond the n=2p family — specifically whether a DYN representation based on a non-max-order generator can substitute when the unit group is non-cyclic — is not established.
