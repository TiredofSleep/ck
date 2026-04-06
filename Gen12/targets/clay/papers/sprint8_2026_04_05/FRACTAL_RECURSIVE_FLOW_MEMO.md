# FRACTAL RECURSIVE FLOW MEMO
## Recursive Refinement Law in ℤ/10ℤ — Formalization and TIG Connection

**Date:** 2026-04-05  
**Builds on:** Perspective Gap Memo (coarse partition identity proved)  
**Status:** All claims computed or proved. All gap values exact.

---

## 1. FORMAL DEFINITIONS

### Definition 1.1 (Refinement of a partition class)

Let X be a finite set, π a partition of X, and R a representation of X with associated partition π(R) = X/∼_R (the quotient by R's equivalence relation). The **Level-1 refinement** of class C ∈ π under R is the trace of π(R) on C:

$$\pi^1(R, C) = \bigl\{\, B \cap C \;\colon\; B \in \pi(R),\; B \cap C \neq \varnothing \,\bigr\}$$

That is, each element of π¹(R,C) is the intersection of an R-equivalence class with C, retaining only nonempty intersections.

Inductively, for C' ∈ π^{k-1}(R, C), the **Level-k refinement** is:

$$\pi^k(R, C') = \bigl\{\, B \cap C' \;\colon\; B \in \pi(R),\; B \cap C' \neq \varnothing \,\bigr\}$$

### Definition 1.2 (Recursive Gap)

For representations Rᵢ, Rⱼ on X with shared coarse partition π₀:

$$\text{Gap}_\text{recursive}(R_i, R_j) = \sum_{C \in \pi_0} \frac{|C|}{|X|} \cdot \text{VI}\!\left(\pi^1(R_i, C),\ \pi^1(R_j, C)\right)$$

where VI is the variation of information between two partitions π, π′ of a class C under the uniform measure μ = |·|/|C|:

$$\text{VI}(\pi, \pi') = H(\pi) + H(\pi') - 2\,I(\pi;\pi')$$

with entropy and mutual information given by:

$$H(\pi) = -\sum_{B \in \pi} \frac{|B|}{|C|} \log_2 \frac{|B|}{|C|}$$

$$I(\pi;\pi') = \sum_{\substack{B \in \pi \\ B' \in \pi'}} \frac{|B \cap B'|}{|C|} \log_2 \frac{|B \cap B'| \cdot |C|}{|B| \cdot |B'|}$$

where the sum excludes terms with $|B \cap B'| = 0$.

### Definition 1.3 (Fractal Recursive Flow)

A collection of representations {R₁,...,Rₖ} on a finite set X exhibits **Fractal Recursive Flow** if:

1. All representations agree on a non-trivial coarse partition:  
   π₀ = π(R₁) = π(R₂) = ... = π(Rₖ)  (non-trivial = neither discrete nor trivial)

2. At least two representations give different Level-1 refinements of at least one class C ∈ π₀:  
   ∃ C ∈ π₀, ∃ i ≠ j : π¹(Rᵢ, C) ≠ π¹(Rⱼ, C)

3. Each representation contributes at least one invariant not recoverable from any combination of the others:  
   ∀ i ∃ invariant Iᵢ such that no Rⱼ (j≠i), alone or in combination, recovers Iᵢ

4. The join of all intra-class refinements equals the discrete partition of X:  
   ⋁ᵢ π¹(Rᵢ, C) = discrete(C) for all C ∈ π₀

### Definition 1.4 (Gate)

A **gate** at class C' ∈ π^k(R) is a point in the refinement tree where representation R cannot further refine C' (π^{k+1}(R, C') = π^k(R, C') = {C'}), but some other representation Rⱼ can:

$$\pi^1(R_j, C') \neq \{C'\}$$

The gate marks where the current representation must be exchanged to continue refinement.

---

## 2. THE FOUR LEVEL-1 REFINEMENTS ON ℤ/10ℤ

All four representations agree on π₀ = {{0},{5},{1,3,7,9},{2,4,6,8}} (proved in previous memo). The following Level-1 refinements apply to the two non-singleton classes.

### Class {1,3,7,9}

| Representation | π¹(R, {1,3,7,9}) | Information | Basis |
|---|---|---|---|
| CRT | {{1},{3},{7},{9}} | 2 bits (discrete) | distinct mod-5 residues: 1,3,2,4 |
| UG | {{1},{9},{3,7}} | log₂(4/3) + ... ≈ 1.58 bits | orders: 1, 2, 4 |
| SPEC (S={3,7}) | {{1,9},{3,7}} | 1 bit | spectral projection sign on λ=φ eigenspace |
| DYN (×3) | {{1,3,7,9}} | 0 bits (partition) | all in one 4-cycle; internal order not exposed as a partition |

**Note on DYN:** DYN does not partition {1,3,7,9} further — as a set partition it contributes 0 bits. However DYN uniquely contributes **orbit-order information**: the directed cycle 1→3→9→7→1, which assigns each element a position (0,1,2,3) in the flow. This is not a partition refinement; it is an ordered structure on the class. The distinction between partition information and orbit-order information is explicit throughout this memo.

**UG and SPEC agree** that {3,7} belong together (generators of order 4 vs spectral λ=φ class). **CRT and DYN** give discrete partitions but on different groupings (mod-5 vs cycle-position respectively).

### Class {2,4,6,8}

| Representation | π¹(R, {2,4,6,8}) | Information | Basis |
|---|---|---|---|
| CRT | {{2},{4},{6},{8}} | 2 bits (discrete) | distinct mod-5 residues: 2,4,1,3 |
| UG | {{2,8},{4,6}} | 1 bit | {2,8} via units 1,9 (orders 1,2); {4,6} via units 7,3 (order 4) |
| SPEC (S={3,7}) | {{2,8},{4,6}} | 1 bit | spectral projection: same sign grouping as UG |
| DYN (×3) | {{2,4,6,8}} | 0 bits (partition) | all in one 4-cycle 2→6→8→4; contributes orbit-order, not partition refinement |

**UG and SPEC give identical refinements of {2,4,6,8}.** This is the unique inter-representation agreement at Level 1.

---

## 3. LEVEL-2: THE GATE AT {3,7}

The class {3,7} appears as a non-singleton at Level 1 from both UG (order-4 generators) and SPEC (λ=φ class). Attempting Level-2 refinement:

| Representation | π²(R, {3,7}) | Resolves? | Basis |
|---|---|---|---|
| CRT | {{3},{7}} | **YES** | 3 mod 5 = 3, 7 mod 5 = 2 |
| UG | {{3,7}} | **NO** | both have order 4; they are inverses (3·7≡1 mod 10) |
| SPEC (S={3,7}) | {{3,7}} | **NO** | identical spectral profiles (cos-symmetric) |
| DYN (×3) | {{3},{7}} | **YES** | cycle positions 1 and 3 in 1→3→9→7 |

**The gate is at {3,7}.** Representations UG and SPEC produce this class but cannot resolve it. The refinement must switch to CRT or DYN to separate PROGRESS(3) from COLLAPSE(7).

**Why SPEC cannot resolve {3,7}:** Since 7 = n−3 = 10−3, we have ω^7 = ω^(−3), so for any eigenspace computation:

$$P_\lambda(3) = \sum_{j: \lambda_j = \lambda} \frac{\omega^{3j} + \overline{\omega^{3j}}}{n} = P_\lambda(7)$$

The spectral profile of 3 and 7 are identical under any real-valued Cayley graph on ℤ/10ℤ. This is exact and not a coincidence — it follows from 3 + 7 = 10 ≡ 0 (mod 10), making them "reflection-symmetric" elements.

---

## 4. RECURSIVE GAP TABLE

Exact computation of Gap_recursive(Rᵢ, Rⱼ) = (4/10)·VI_UNIT + (4/10)·VI_EVEN:

| Pair | VI on {1,3,7,9} | VI on {2,4,6,8} | Gap_recursive | Gap_coarse |
|---|---|---|---|---|
| CRT, UG | 0.5000 | 1.0000 | **0.6000** | 0 |
| CRT, SPEC | 1.0000 | 1.0000 | **0.8000** | 0 |
| CRT, DYN | 2.0000 | 2.0000 | **1.6000** | 0 |
| UG, SPEC | 0.5000 | 0.0000 | **0.2000** | 0 |
| UG, DYN | 1.5000 | 1.0000 | **1.0000** | 0 |
| SPEC, DYN | 1.0000 | 1.0000 | **0.8000** | 0 |

All Gap_coarse = 0 (proved). All Gap_recursive > 0 (computed).

**The representations are coarsely compatible and recursively divergent: Gap_coarse = 0 for all pairs, Gap_recursive > 0 for all pairs.**

---

## 5. THE MAIN THEOREM

**Theorem (Fractal Recursive Flow on ℤ/10ℤ):**  
The system {CRT, UG, SPEC(S={3,7}), DYN(×3)} on ℤ/10ℤ exhibits Fractal Recursive Flow.

**Proof:**

*(Condition 1 — Shared coarse partition):*  
Proved in the Perspective Gap Memo: all four representations induce π₀ = {{0},{5},{1,3,7,9},{2,4,6,8}} on ℤ/10ℤ. Non-trivial: the shared coarse partition is neither the indiscrete partition (one class) nor the discrete partition (ten singletons).

*(Condition 2 — Divergent Level-1 refinements):*  
Computed above: π¹(CRT,{1,3,7,9}) = {{1},{3},{7},{9}} ≠ π¹(SPEC,{1,3,7,9}) = {{1,9},{3,7}}. Multiple witnesses. ✓

*(Condition 3 — Each representation uniquely refines):*  
- CRT uniquely identifies α=5 via CRT type and gives discrete mod-5 partition refinement  
- UG uniquely identifies β=7 as a max-order generator, partitioning {1,3,7,9} by order  
- SPEC(S={3,7}) uniquely places φ in the spectrum of the generator-pair Cayley graph  
- DYN(×3) uniquely determines the orbit order 1→3→9→7 (an order-type invariant, not a partition refinement)  

Each of these is the sole representation achieving its invariant (proved in the minimality section below). ✓

*(Condition 4 — Join = discrete):*  
For class {1,3,7,9}: CRT gives the discrete partition, so the join over all representations is discrete. For {2,4,6,8}: same. The join condition is satisfied, though its interest here is limited — the substance is that the representations expose different non-discrete sub-structures, not that their join is discrete. ✓ □

---

## 6. MINIMALITY THEOREM

**Theorem (Minimal sufficiency):** The system {CRT, UG, SPEC, DYN} is minimally sufficient for the four invariants I₁–I₄, where I₁–I₃ are partition-type invariants and I₄ is an orbit-order invariant. Removing any one representation removes exactly one invariant.

**Invariant type distinction:**
- **CRT, UG, SPEC** contribute **partition refinements**: sub-partitions of coarse classes into finer equivalence classes.
- **DYN** contributes **orbit-order refinement**: a directed cyclic ordering on the elements of each non-fixed class. This is a strictly richer structure than a partition (a partition is recovered from the orbit order by forgetting direction), and it is not recoverable from any partition-type invariant alone.

The minimality claim must be understood accordingly: the 4-piece system is minimally sufficient when both partition-type and order-type invariants are admitted. A system of four partition-type representations cannot recover I₄.

| Removed rep | Missing invariant | Invariant type |
|---|---|---|
| CRT | I₁: α=5 as CRT complement product | partition-type |
| UG | I₂: β=7 as max-order generator | partition-type |
| SPEC | I₃: φ in eigenvalue spectrum | partition-type |
| DYN | I₄: cycle ordering 1→3→9→7 | **orbit-order type** |

**Proof:** Each invariant has exactly one covering representation (computed in the recoverability table). Each 3-subset misses one invariant. The orbit-order invariant I₄ is not a partition and cannot be expressed as a sub-partition of any coarse class. □

**Non-uniqueness note:** Equivalent minimal systems exist. For example, DYN(×7) also provides a cycle ordering (7→9→3→1), just in a different direction. Similarly, using S={1,9} instead of S={3,7} for the Cayley graph would change which spectral invariant is accessible. The claimed minimality is for the specific system {CRT, UG, SPEC(S={3,7}), DYN(×3)}.

---

## 7. TIG OPERATOR GRAMMAR AS REFINEMENT STRUCTURE

The following is an exact mapping — not an interpretation. It states which elements of the refinement hierarchy correspond to TIG operator labels.

### Level 0 (universally agreed by all representations):

| TIG operator | Label | Role at Level 0 |
|---|---|---|
| 0 | VOID | Singleton class {0} — coarsely isolated by all representations |
| 5 | BALANCE | Singleton class {5} — coarsely isolated by all representations |
| {1,3,7,9} | UNIT operators | One coarse class — not yet differentiated at Level 0 |
| {2,4,6,8} | EVEN operators | One coarse class — not yet differentiated at Level 0 |

### Level 1 (representation-dependent):

| TIG operator | Refinement by UG | Refinement by SPEC |
|---|---|---|
| 1 (BEGINNING) | Order 1 — singleton | In {1,9} class (λ=−1/φ) |
| 9 (RESET) | Order 2 — singleton | In {1,9} class (λ=−1/φ) |
| 3 (PROGRESS) | Order 4 — grouped with 7 | In {3,7} class (λ=φ) |
| 7 (COLLAPSE) | Order 4 — grouped with 3 | In {3,7} class (λ=φ) |

### Level 2 (gate — requires representation switch):

| TIG operators | CRT resolves? | DYN resolves? |
|---|---|---|
| 3 (PROGRESS) vs 7 (COLLAPSE) | **YES** — mod-5 residues 3 vs 2 | **YES** — cycle positions 1 vs 3 |

### TIG structural mappings (exact):

**Gap = intra-class VI gap:**  
The numerical gap between SPEC and DYN is 0.8 bits. This quantifies precisely how much information the φ-spectral structure and the cycle ordering fail to share about the class {1,3,7,9}.

**Flow = representation switch that opens new refinement:**  
CRT→UG: gain {1}≠{9} (order distinction, 0.5 bits on unit class); lose discrete mod-5 detail  
UG→SPEC: gain φ as eigenvalue (spectral quantification); lose individual order labels  
SPEC→DYN: gain cycle ordering 1→3→9→7 (2 bits); lose φ and spectral structure

**Gate = point where refinement requires representation change:**  
Within {3,7}: SPEC and UG both stop here. CRT or DYN required to proceed. The gate corresponds exactly to distinguishing PROGRESS(3) from COLLAPSE(7) — the two generators — which requires either their mod-5 residues (CRT) or their position in the PROGRESS-driven cycle (DYN).

**T\* = α/β = 5/7 as a cross-level cross-representation ratio:**  
α=5 lives at Level 0 (universally isolated).  
β=7 lives at Level 1 (accessible only via UG, as the smallest generator above α=5).  
T\* is not a single-representation quantity; it bridges Level 0 (CRT structure) and Level 1 (UG structure).

---

## 8. STRONGEST HONEST CLAIM

The perspective gap in ℤ/10ℤ is not a failure of representation but a recursive refinement phenomenon: the coarse structure is shared by all four views, while the hidden internal structure of each class appears only under specific representations. The gap is zero at the coarse partition level and strictly positive (between 0.2 and 1.6 bits) at the intra-class level for every representation pair.

## 9. STRONGEST HONEST BOUNDARY

What is not yet established is whether this recursive refinement law is specific to ℤ/10ℤ and the chosen four representations, or whether it generalizes as a genuine multi-view structural principle across other moduli and other algebraic systems.
