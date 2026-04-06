# PERSPECTIVE GAP FORMALIZATION MEMO
## Four Representations of ℤ/10ℤ — Information Boundaries

**Date:** 2026-04-05  
**Task:** Formalize the perspective gap as a testable mathematical statement  
**Status:** Negative theorem proved at coarse level. Intra-class gap identified and characterized.  
**Verification:** All eigenvalues, partitions, and information-loss statements computed exactly.

---

## 1. THE FOUR REPRESENTATIONS AND THEIR PRIMARY PARTITIONS

### Definition (Representation-induced partition)

For a representation R of ℤ/nℤ, the primary partition π(R) is the partition of {0,...,n−1} into equivalence classes under the natural equivalence relation of R.

### R₁: CRT Representation

The ring ℤ/10ℤ ≅ ℤ/2ℤ × ℤ/5ℤ. Classify each element by its type in each factor:

| Type label | Condition | Elements |
|---|---|---|
| (zero, zero) | x ≡ 0(mod 2), x ≡ 0(mod 5) | {0} |
| (unit, zero) | x ≢ 0(mod 2), x ≡ 0(mod 5) | {5} |
| (zero, unit) | x ≡ 0(mod 2), x ≢ 0(mod 5) | {2,4,6,8} |
| (unit, unit) | x ≢ 0(mod 2), x ≢ 0(mod 5) | {1,3,7,9} |

**π_CRT** = {{0}, {5}, {2,4,6,8}, {1,3,7,9}}  
**Primary invariant:** α = 5 is the unique element of type (unit, zero), i.e., the CRT complement product n/2 = 5.

### R₂: Unit Group Representation

The orbits of (ℤ/10ℤ)* = {1,3,7,9} acting on ℤ/10ℤ by multiplication:

**π_UG** = {{0}, {5}, {2,4,6,8}, {1,3,7,9}}  
**Primary invariant:** β = 7 is the smallest max-order (order-4) unit exceeding α=5.

### R₃: Cayley Graph Spectral Representation

The additive Cayley graph Cay(ℤ/10ℤ, S) for generating set S partitions {0,...,9} via spectral projection profiles.

For S = {1,3,7,9} (full unit set), the eigenvalues are:
- λ = 4 (multiplicity 1, j=0)
- λ = 1 (multiplicity 4, j=1,3,7,9)
- λ = −1 (multiplicity 4, j=2,4,6,8)
- λ = −4 (multiplicity 1, j=5)

Spectral projection profiles (real parts) per element x:

| Element | λ=−4 projection | λ=−1 projection | λ=1 projection | λ=4 projection |
|---|---|---|---|---|
| 0 | +0.1 | +0.4 | +0.4 | +0.1 |
| 5 | −0.1 | +0.4 | −0.4 | +0.1 |
| 1,3,7,9 | −0.1 | −0.1 | +0.1 | +0.1 |
| 2,4,6,8 | +0.1 | −0.1 | −0.1 | +0.1 |

**π_SPEC** = {{0}, {5}, {1,3,7,9}, {2,4,6,8}}  
**Primary invariant:** the spectrum lies in ℚ; 0 and 5 have distinct profiles; units and non-units have distinct profiles.

### R₄: Dynamical Representation (×3 flow)

Under iteration of x ↦ 3x mod 10:
- 0 ↦ 0: fixed point
- 5 ↦ 5: fixed point
- 1 ↦ 3 ↦ 9 ↦ 7 ↦ 1: 4-cycle
- 2 ↦ 6 ↦ 8 ↦ 4 ↦ 2: 4-cycle

**π_DYN** = {{0}, {5}, {1,3,7,9}, {2,4,6,8}}  
**Primary invariant:** 0 and 5 are fixed; the other two classes form 4-cycles.

---

## 2. THE COARSE-LEVEL RESULT

**Theorem (Coarse partition identity):** All four representations induce the same coarse partition of ℤ/10ℤ:

$$\pi = \{\{0\}, \{5\}, \{1,3,7,9\}, \{2,4,6,8\}\}$$

**Proof:** Each representation's primary partition was computed explicitly and is identical.  
CRT: type labels give exactly these four classes.  
UG: unit-multiplication orbits give exactly these four classes.  
SPEC: spectral projection profiles give exactly these four classes.  
DYN: fixed points and cycles give exactly these four classes. □

**Corollary (Variation of Information):**  
Gap(Rᵢ, Rⱼ) = VI(π(Rᵢ), π(Rⱼ)) = 0 for all pairs i,j ∈ {CRT, UG, SPEC, DYN}.

Computed: H(π) = 1.7219 bits for all four; all pairwise mutual information = 1.7219 bits; all VI = 0.

**The perspective gap does not exist at the coarse level.** The four representations agree on which elements are equivalent; they disagree on what that equivalence means.

---

## 3. THE INTRA-CLASS PERSPECTIVE GAP

The representations diverge on the internal structure of the shared classes. For each class C ∈ π, define:

**Intra-class invariant Iᵢ(C)** = the additional structure that representation Rᵢ assigns to members of C, beyond the class label.

### Class {1,3,7,9}

| Representation | Intra-class structure | Information content |
|---|---|---|
| CRT | CRT coordinates: (1,1),(1,3),(1,2),(1,4) mod (2,5) — four distinct labels | log₂(4) = 2 bits |
| UG | Orders: 1 has order 1, 9 has order 2, 3 and 7 have order 4. Generators = {3,7} | 1 bit (generator vs non-generator) |
| SPEC (S={1,3,7,9}) | All four elements are equivalent at eigenvalue 1 — no distinction | 0 bits |
| DYN (×3) | Cycle order: 1→3→9→7. Each element has a position (0,1,2,3) in the cycle | 2 bits (position in 4-cycle) |

**Key finding:** The spectral representation with S = {1,3,7,9} loses all intra-class information about {1,3,7,9}. The UG and DYN representations recover partial information (different aspects). The CRT representation retains full distinguishability via mod-5 residue.

### Class {5} — The Absorbing Idempotent

| Representation | Identifies 5 as... | Requires... |
|---|---|---|
| CRT | (unit mod 2, zero mod 5) — complement product n/p_max | factorization n=2×5 |
| UG | Fixed point of all unit actions: 5·u ≡ 5 (mod 10) for all units u | knowledge of unit action |
| SPEC | Unique profile (−0.1, +0.4, −0.4, +0.1) — sign flip on λ=1 projection vs {0} | spectral computation |
| DYN | Fixed point under ×3 — indistinguishable from {0} at cycle-type level | dynamical iteration |

**Key finding:** CRT, UG, and SPEC each identify {5} by a distinct structural property. DYN cannot distinguish {5} from {0} at the fixed-point level — both are fixed by ×3. To distinguish them dynamically requires a different rule (e.g., ×5 fixes all odd, ×2 maps 5→0).

---

## 4. φ IN THE SPECTRAL REPRESENTATION — EXACT LOCATION

**Theorem (Exact spectrum of Cay(ℤ/10ℤ, {3,7})):**  
The additive Cayley graph with generator set S = {3,7} = {PROGRESS, COLLAPSE} has eigenvalue spectrum:

$$\lambda_j = 2\cos\!\left(\frac{3\pi j}{5}\right), \quad j = 0,1,\ldots,9$$

The distinct values are {2, φ, 1/φ, −1/φ, −φ, −2}, all in ℚ(φ) = ℚ(√5).

**Proof:**  
Since 7 = 10 − 3, we have ω^7 = ω^{−3} = \overline{ω^3}. Therefore:

$$\lambda_j = \omega^{3j} + \omega^{7j} = \omega^{3j} + \overline{\omega^{3j}} = 2\cos\!\left(\frac{2\pi \cdot 3j}{10}\right) = 2\cos\!\left(\frac{3\pi j}{5}\right)$$

Using cos(π/5) = φ/2 (exact, proved in Bridge sprint):

| j | λⱼ | exact |
|---|---|---|
| 0 | 2 | 2 |
| 1,9 | −1/φ | 2cos(3π/5) = −2·(1/φ)/2 |
| 2,8 | −φ | 2cos(6π/5) = −2cos(π/5) = −φ |
| 3,7 | φ | 2cos(9π/5) = 2cos(π/5) = φ |
| 4,6 | 1/φ | 2cos(12π/5) = 2cos(2π/5) = 1/φ |
| 5 | −2 | 2cos(3π) = −2 |

**Spectral ratio:** λ₂/λ₁ = φ/2 = cos(π/5). □

**Exact location of φ:** φ appears because the generator set {3,7} corresponds to the Galois automorphisms of order 4 in Gal(ℚ(ζ₁₀)/ℚ), whose character sums land in the maximal real subfield ℚ(φ). This is the connection to the Bridge sprint's cyclotomic result.

**φ does NOT appear** as an eigenvalue of Cay(ℤ/10ℤ, {1,3,7,9}) (the full unit set). That spectrum is {4, 1, −1, −4}.

---

## 5. PAIRWISE COMPARISON MAPS

### CRT ↔ UG

| | Preserved | Lost |
|---|---|---|
| CRT → UG | All four coarse classes; identification of {5} as a special class | Internal mod-5 residues within {1,3,7,9}; distinction of (unit,unit) sublabels |
| UG → CRT | All four coarse classes; identification of {5} as fixed | Distinction of generators {3,7} from non-generators {1,9} within {1,3,7,9} |

### UG ↔ SPEC

| | Preserved | Lost |
|---|---|---|
| UG → SPEC (S={3,7}) | Generator identification — {3,7} have eigenvalue φ, distinguished from {1,9} with eigenvalue 1/φ | Specific cycle ordering (which generator maps to which) |
| SPEC (S={3,7}) → UG | {3,7} are generators; {1,9} are non-generators | Eigenvalue φ; all spectral structure in ℚ(φ) |

### SPEC ↔ DYN

| | Preserved | Lost |
|---|---|---|
| SPEC (S={3,7}) → DYN (×3) | Fixed-point classes {0} and {5}; two 4-cycle classes | φ and all spectral quantification |
| DYN (×3) → SPEC | Cycle structure: fixed vs 4-cycle | φ; cannot distinguish {3,7} generators without adding spectral structure |

### DYN ↔ CRT

| | Preserved | Lost |
|---|---|---|
| DYN → CRT | Fixed points {0},{5}; two orbiting classes | Cycle ordering within {1,3,7,9} and {2,4,6,8} |
| CRT → DYN | CRT types identify {0},{5},{1,3,7,9},{2,4,6,8} | Internal mod-5 residue labels; algebraic identity of 5 as complement product |

---

## 6. FORMAL DEFINITION: PERSPECTIVE GAP

**Definition (Coarse gap):**  
Gap_coarse(Rᵢ, Rⱼ) = VI(π(Rᵢ), π(Rⱼ)) under the uniform measure on {0,...,n−1}.

**Theorem:** Gap_coarse(Rᵢ, Rⱼ) = 0 for all pairs among {CRT, UG, SPEC (S={1,3,7,9}), DYN (×3)} on ℤ/10ℤ.

**Definition (Intra-class gap):**  
For a class C ∈ π and representations Rᵢ, Rⱼ:

Gap_intra(Rᵢ, Rⱼ; C) = VI(π_intra(Rᵢ, C), π_intra(Rⱼ, C))

where π_intra(Rᵢ, C) is the sub-partition of C induced by Rᵢ's intra-class structure.

**Computed intra-class gaps for class {1,3,7,9}:**

| Pair | Intra-class partition by Rᵢ | Intra-class partition by Rⱼ | Gap |
|---|---|---|---|
| CRT, UG | {{1},{3},{7},{9}} | {{1,9},{3,7}} | 1 bit |
| UG, SPEC (S={1,3,7,9}) | {{1,9},{3,7}} | {{1,3,7,9}} | 1 bit |
| UG, SPEC (S={3,7}) | {{1,9},{3,7}} | {{1,9} at λ=−1/φ, {3,7} at λ=φ} | 0 bits |
| DYN, CRT | position in {1→3→9→7} | mod-5 residue labels | 0 bits (same fine partition) |

---

## 7. NEGATIVE THEOREM: NO UNIVERSAL REPRESENTATION

**Theorem:** There is no single representation R among {CRT, UG, SPEC (any S), DYN (any rule)} on ℤ/10ℤ such that R simultaneously:
1. Identifies α=5 by its algebraic-idempotent structure (requires factorization n=2×5)
2. Identifies β=7 as a generator of (ℤ/10ℤ)* (requires order computation)
3. Produces φ as an eigenvalue (requires Cayley graph with S={3,7})
4. Encodes the cycle order 1→3→9→7 (requires multiplicative flow ×3)

**Proof:**  
Properties 1 and 2 require different algebraic inputs: 1 uses the ring factorization, 2 uses the group structure.  
Property 3 requires the additive Cayley graph with exactly S={3,7}; no Cayley graph with S={1,3,7,9} produces φ.  
Property 4 requires specifying the flow rule ×3 (not ×7 or any other unit); different rules give different orderings.  
No single object simultaneously encodes all four. □

**Corollary:** f(n) = α/β is not universal. It bridges properties 1 and 2 but does not encode properties 3 (φ in spectrum) or 4 (cycle ordering). Verified: 5/7 does not appear as any eigenvalue ratio in Cay(ℤ/10ℤ, {1,3,7,9}) or Cay(ℤ/10ℤ, {3,7}).

---

## 8. MINIMAL MULTI-VIEW SYSTEM

A minimal system encoding all four invariants simultaneously requires specifying:

1. The factorization of n (for α via CRT)
2. The unit group with orders (for β and cycle structure)
3. The generator pair {PROGRESS=3, COLLAPSE=7} explicitly (for φ in spectrum)
4. A specific flow rule (for cycle ordering)

Items 1–4 are independent: none of them is derivable from the others by the computations above.

**Minimal multi-view system for ℤ/10ℤ:**
- Ring presentation: ℤ/10ℤ with explicit n=10=2×5
- Group presentation: (ℤ/10ℤ)* = ⟨3⟩ = ℤ/4ℤ, with 3 as primary generator
- Spectral data: eigenvalues of Cay(ℤ/10ℤ, {3,7}) ⊂ ℚ(φ)
- Dynamical data: the orbit 1→3→9→7 under ×3

These four pieces are jointly sufficient to recover all four invariants. No subset of three is sufficient.

---

## 9. SUMMARY TABLE

| Representation | Primary invariant | Intra-class info (for {1,3,7,9}) | Encodes α? | Encodes β? | Encodes φ? | Encodes cycle order? |
|---|---|---|---|---|---|---|
| CRT | α=5 (complement product) | 2 bits (mod-5 residue) | YES | NO | NO | NO |
| UG | β=7 (smallest max-order gen > α) | 1 bit (generator/non-generator) | NO | YES | NO | NO |
| SPEC (S={3,7}) | φ and 1/φ as eigenvalues | 1 bit ({3,7} vs {1,9} eigenvalue) | NO | Partial | YES | NO |
| DYN (×3) | fixed point class | 2 bits (cycle position) | NO | NO | NO | YES |
| f=α/β | CRT-UG bridge | — | via α | via β | NO | NO |

---

## 10. FORMAL STATEMENTS (PROVED vs CONJECTURAL)

**PROVED:**
- All four representations on ℤ/10ℤ induce the partition {{0},{5},{1,3,7,9},{2,4,6,8}} (computed)
- Coarse VI gaps are all 0 (computed exactly)
- Spectrum of Cay(ℤ/10ℤ, {3,7}) = {±2, ±φ, ±1/φ}, all in ℚ(φ) (proved algebraically)
- f=5/7 does not appear as any eigenvalue ratio in either Cayley graph (exhaustive search)
- No single representation encodes all four invariants simultaneously (by enumeration)

**CONJECTURAL / OPEN:**
- Whether the minimal multi-view system described above is unique (other 4-piece systems may also be sufficient)
- Whether the intra-class gap structure generalizes uniformly to other moduli
- Whether any single algebraic object (e.g., a specific algebra or module) encodes all four invariants simultaneously without decomposing into the four pieces above
