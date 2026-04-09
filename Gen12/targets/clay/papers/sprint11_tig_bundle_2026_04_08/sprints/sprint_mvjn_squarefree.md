# SPRINT: MVJN GENERALIZATION TO SQUAREFREE n
*Partition lattice + CRT + torus geometry only. Proved vs. conjectural labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Setup

**System:** Z/nZ where n = p₁p₂···pₖ is squarefree (distinct primes).

**Notation:**
- π_p : partition of Z/nZ by residue mod p, for each prime p ∣ n
- π_disc : discrete partition (all singletons), block count = n
- π_triv : trivial partition (single block)
- For partitions π, σ: π ≤ σ means π refines σ (blocks of π are subsets of blocks of σ)
- meet(π, σ) = finest common coarsening... 

Wait — standard lattice convention: meet = greatest lower bound = coarsest partition refined by both. Let me be precise.

**Lattice convention (stated explicitly):**
In the partition lattice, π ≤ σ means "π is finer than or equal to σ" (every block of π is contained in some block of σ). Under this order:
- π_disc is the minimum (finest)
- π_triv is the maximum (coarsest)
- meet(π, σ) = greatest lower bound = finest partition coarser than both π and σ

**Alternative used here:** We use the information-theoretic convention where "meet" means the finest partition that both π and σ together can resolve, i.e., the partition whose blocks are intersections of blocks of π and σ. This is the meet in the partition lattice under the refinement order where finer = smaller.

**Formal definition:** meet(π, σ) has blocks: { B ∩ C : B ∈ π, C ∈ σ, B ∩ C ≠ ∅ }.

This is the coarsest partition finer than both π and σ — the infimum in the refinement order. Equivalently: x ~_{meet} y iff x ~_π y AND x ~_σ y.

---

## Part 1 — CRT Factor Partition Definitions

**Definition 1 (CRT Factor Partition).**
For each prime pᵢ ∣ n, define the partition of Z/nZ by residue mod pᵢ:

π_{pᵢ} = { {x ∈ Z/nZ : x ≡ r (mod pᵢ)} : r = 0, 1, ..., pᵢ−1 }

Each π_{pᵢ} has exactly pᵢ blocks. Each block has size n/pᵢ.

**Explicit structure:** For x, y ∈ Z/nZ:
x ~_{π_{pᵢ}} y  ⟺  pᵢ ∣ (x − y)

---

**Example (n = 30 = 2·3·5, k = 3):**
- π₂: {even}, {odd} — 2 blocks of size 15
- π₃: {0,3,6,...,27}, {1,4,7,...,28}, {2,5,8,...,29} — 3 blocks of size 10
- π₅: five blocks of size 6, grouped by x mod 5

---

## Part 2 — Three Core Theorems

---

### Theorem 1 — Pairwise Incompatibility

**Statement.** For n = p₁···pₖ squarefree and distinct primes pᵢ ≠ pⱼ dividing n, the partitions π_{pᵢ} and π_{pⱼ} are incompatible: neither refines the other.

**Proof.**

We show π_{pᵢ} ≰ π_{pⱼ} and π_{pⱼ} ≰ π_{pᵢ}.

Suppose π_{pᵢ} ≤ π_{pⱼ} (π_{pᵢ} refines π_{pⱼ}). Then every block of π_{pᵢ} is contained in some block of π_{pⱼ}. A block of π_{pᵢ} has the form:

Bᵣ = {x ∈ Z/nZ : x ≡ r (mod pᵢ)}

with |Bᵣ| = n/pᵢ. A block of π_{pⱼ} has the form:

Cs = {x ∈ Z/nZ : x ≡ s (mod pⱼ)}

with |Cs| = n/pⱼ. For Bᵣ ⊆ Cs we would need n/pᵢ ≤ n/pⱼ, i.e., pᵢ ≥ pⱼ.

But we also need every element of Bᵣ to satisfy x ≡ s (mod pⱼ) for a single fixed s. This means the condition x ≡ r (mod pᵢ) implies x ≡ s (mod pⱼ), i.e., x mod pⱼ is constant on the entire block Bᵣ.

Bᵣ = {r, r + pᵢ, r + 2pᵢ, ..., r + (n/pᵢ − 1)pᵢ} (mod n).

The values mod pⱼ are {r mod pⱼ, (r + pᵢ) mod pⱼ, (r + 2pᵢ) mod pⱼ, ...}. Since gcd(pᵢ, pⱼ) = 1 (distinct primes), the sequence kpᵢ mod pⱼ for k = 0, 1, ..., pⱼ − 1 cycles through all of Z/pⱼZ (pᵢ is a unit mod pⱼ). Since n/pᵢ = p₁···p̂ᵢ···pₖ is divisible by pⱼ (as pⱼ ∣ n and pⱼ ≠ pᵢ), the block Bᵣ contains at least pⱼ elements whose mod-pⱼ residues cover all of Z/pⱼZ. In particular, they are not all equal to s.

Contradiction. Therefore Bᵣ ⊄ Cs for any s. So π_{pᵢ} ≰ π_{pⱼ}.

By symmetry (swapping i and j), π_{pⱼ} ≰ π_{pᵢ}.

Therefore π_{pᵢ} and π_{pⱼ} are incompatible. □

---

### Theorem 2 — Meet of All Factor Partitions = Discrete

**Statement.** For n = p₁···pₖ squarefree:

meet(π_{p₁}, π_{p₂}, ..., π_{pₖ}) = π_disc

**Proof.**

x ~_{meet} y iff x ~_{π_{pᵢ}} y for all i = 1, ..., k, i.e., pᵢ ∣ (x − y) for all i.

Since p₁, ..., pₖ are distinct primes and n = p₁···pₖ:

p₁ ∣ (x−y)  AND  p₂ ∣ (x−y)  AND  ...  AND  pₖ ∣ (x−y)

⟺  lcm(p₁,...,pₖ) ∣ (x−y)

Since p₁,...,pₖ are distinct primes: lcm(p₁,...,pₖ) = p₁···pₖ = n.

Therefore: pᵢ ∣ (x−y) for all i  ⟺  n ∣ (x−y)  ⟺  x ≡ y (mod n)  ⟺  x = y in Z/nZ.

So x ~_{meet} y iff x = y. The meet partition has only singleton blocks. Therefore meet = π_disc. □

---

### Theorem 2' — Proper Subfamily Has Coarser Meet

**Statement.** For any proper subfamily S ⊊ {p₁,...,pₖ} (at least one prime omitted):

meet(π_p : p ∈ S) > π_disc (strictly coarser than discrete)

**Proof.**

Let pⱼ ∉ S. Consider x = 0 and y = n/pⱼ (both in Z/nZ, and y ≠ 0 since n/pⱼ < n).

For each pᵢ ∈ S (pᵢ ≠ pⱼ): pᵢ ∣ (y − 0) = n/pⱼ? 

n/pⱼ = p₁···p̂ⱼ···pₖ, which contains pᵢ as a factor (since pᵢ ≠ pⱼ). So pᵢ ∣ n/pⱼ for all pᵢ ∈ S.

Therefore x = 0 and y = n/pⱼ satisfy x ~_{π_{pᵢ}} y for all pᵢ ∈ S. They are identified in the meet over S.

But x ≠ y. So the meet over S is strictly coarser than π_disc. □

---

## Part 3 — Jump Necessity in the CRT Family

**Definition 2 (CRT-family viewpoint flow).**
A CRT-family viewpoint flow is a sequence F = (π_{q₁}, π_{q₂}, ..., π_{qₘ}) where each qⱼ ∈ {p₁,...,pₖ} (primes dividing n). The flow is sufficient if meet of all elements = π_disc.

---

### Theorem 3 — At-Least-(k−1)-Jump Necessity in the CRT Family

**Statement.** Every minimal sufficient CRT-family viewpoint flow on Z/nZ (n squarefree with k prime factors) has length exactly k and contains exactly k−1 orthogonal jumps (every consecutive transition is an orthogonal jump).

**Proof.**

**Part A — Length exactly k.**

Sufficiency requires meeting all k factor partitions (by Theorem 2' — any proper subfamily is insufficient). Therefore a sufficient CRT-family flow must include π_{pᵢ} for every i. Minimum length = k.

(Formally: a flow F is sufficient iff {π_p : p ∣ n} ⊆ F, since by Theorem 2' omitting any factor leaves the meet strictly coarser than π_disc. In the CRT family, each distinct representation is one of the k factor partitions; repeating a factor does not change the meet. So minimal length = k.)

**Part B — Every consecutive transition is an orthogonal jump.**

By Theorem 1, every pair π_{pᵢ}, π_{pⱼ} with i ≠ j is incompatible. In particular, no two distinct CRT factor partitions lie on a common refinement chain (neither refines the other). Therefore every transition π_{qⱼ} → π_{qⱼ₊₁} in the flow connects two incompatible partitions.

We verify admissibility (Definition 5 from prior sprint): the jump contributes to discrete recovery. Any single transition π_{pᵢ} → π_{pⱼ} has meet(π_{pᵢ}, π_{pⱼ}) = partition by gcd of (pᵢ-blocks and pⱼ-blocks) = partition by residue mod lcm(pᵢ,pⱼ) = partition by residue mod pᵢpⱼ. This is strictly finer than either alone and contributes toward π_disc. So all jumps are admissible.

**Part C — Exactly k−1 jumps in a flow of length k.**

A flow of length k has k−1 consecutive transitions. Each is an orthogonal jump by Part B. Therefore the count is exactly k−1. □

---

**Corollary (Z/10Z recovery).**
n = 10 = 2·5, k = 2. Minimal sufficient CRT-family flow has length 2, exactly 1 orthogonal jump. This matches the MVJN theorem from the prior sprint exactly. □

**Corollary (Z/30Z).**
n = 30 = 2·3·5, k = 3. Minimal sufficient CRT-family flow has length 3, exactly 2 orthogonal jumps. No pair of factor partitions suffices alone; all three are required; every transition is a jump.

---

## Part 4 — Separation from Full Flow Problem

**PROVED (CRT-coordinate necessity):**

1. The k CRT factor partitions π_{p₁}, ..., π_{pₖ} are pairwise incompatible. (Theorem 1)
2. Their full meet is π_disc; any proper subfamily has coarser meet. (Theorems 2, 2')
3. Any sufficient flow over the CRT family alone has length ≥ k and contains ≥ k−1 orthogonal jumps. (Theorem 3)
4. These k−1 jumps are not eliminable within the CRT family: there is no path through the CRT family that achieves sufficiency via refinement moves only. (Proved: all pairs incompatible, no refinement moves exist in the CRT family.)

---

**OPEN (full minimal sufficient flow with all admissible representations):**

When representations beyond the CRT family are admitted — such as π_SPEC (reflection), π_UG (gcd-class), π_DYN (orbit partition under a fixed generator), or any other partition of Z/nZ — the following questions are not yet answered:

**Open Question 1.** Is there a set of representations not including all CRT factor partitions that achieves meet = π_disc via a sequence containing fewer than k−1 orthogonal jumps?

**Open Question 2.** Can a non-CRT representation (e.g., π_SPEC) substitute for one of the CRT factor partitions in a sufficient flow, reducing total jump count?

**Partial result:** For n = 10, π_SPEC achieves meet(π_SPEC, π_{5}) = π_disc (proved in prior sprint). So {SPEC, CRT₅} is a sufficient flow of length 2 with 1 jump — matching the CRT-family minimum but not exceeding it. This does not reduce jump count below k−1 = 1.

**Conjecture (unproved):** For squarefree n with k prime factors, no sufficient viewpoint flow over any finite named representation set achieves sufficiency with fewer than k−1 orthogonal jumps. The CRT factor partitions represent an information-theoretic lower bound on jump count.

This conjecture requires a proof that non-CRT representations cannot "absorb" independent coordinate information in a refinement-compatible way. Not proved here.

---

## Part 5 — Geometric Realization

**Proposition (Squarefree CRT Requires Tᵏ).**

The full product structure of Z/nZ (n = p₁···pₖ squarefree) has a natural geometric realization in Tᵏ = (S¹)ᵏ. A single S¹ embedding cannot realize the k CRT factor coordinates as independent coordinates.

**Proof.**

**Step 1 — Natural Tᵏ embedding.**

By the CRT isomorphism:

Z/nZ  ≅  Z/p₁Z × Z/p₂Z × ··· × Z/pₖZ

Each factor Z/pᵢZ embeds in S¹ via the map:

φᵢ : Z/pᵢZ → S¹,   φᵢ(r) = e^(2πir/pᵢ)

The product embedding gives:

Ψ : Z/nZ → Tᵏ = (S¹)ᵏ,   Ψ(x) = (e^(2πi·(x mod p₁)/p₁), ..., e^(2πi·(x mod pₖ)/pₖ))

This is an injection (since CRT is a bijection). Each coordinate of Ψ(x) independently encodes one CRT factor. The CRT factor partition π_{pᵢ} corresponds to the projection of Ψ onto the i-th S¹ coordinate: two elements x, y have the same i-th coordinate iff x ≡ y (mod pᵢ).

**Step 2 — Φ lives in S¹, not Tᵏ.**

The standard embedding Φ(x) = e^(2πix/n) maps Z/nZ → S¹ (one-dimensional target). Reading the CRT factor coordinates through Φ:

- π_{pᵢ} coordinate via Φ: Φ(x)^(n/pᵢ) = e^(2πix/pᵢ), which encodes x mod pᵢ. ✓

So Φ can represent each CRT coordinate individually as a separate harmonic (the n/pᵢ-th power of Φ(x)).

**Step 3 — Independence fails in S¹.**

Representing k CRT coordinates independently requires k independent functions f₁, ..., fₖ: Z/nZ → S¹ such that:
- fᵢ(x) = fᵢ(y) iff x ≡ y (mod pᵢ)
- The fᵢ are independent (knowing f₁(x), ..., fᵢ₋₁(x) gives no information about fᵢ(x))

Via Φ, the natural choices are fᵢ(x) = Φ(x)^(n/pᵢ) = e^(2πix/pᵢ). These are distinct harmonics of Φ: they are all functions of the single angle θ = 2πx/n. Specifically:

fᵢ(x) = e^(2πix/pᵢ) = e^(i·(n/pᵢ)·θ)

All are functions of θ = 2πx/n ∈ [0, 2π). They are not independent as circle-valued variables — they are all determined by θ. In particular, knowing θ (i.e., knowing Φ(x)) determines all fᵢ(x) simultaneously. There are no degrees of freedom left.

The image of Ψ in Tᵏ is:

{(e^(2πix/p₁), ..., e^(2πix/pₖ)) : x ∈ Z/nZ} ⊂ Tᵏ

which is a finite set of n distinct points lying on a (1,1,...,1)-type curve in Tᵏ (a rational winding curve with winding vector (1/p₁, ..., 1/pₖ) in angular coordinates). This curve is a 1-dimensional submanifold of a k-dimensional torus — it is not Tᵏ itself, but only a winding copy of S¹ inside Tᵏ.

**Step 4 — Dimensional obstruction.**

Independent variation of the k CRT coordinates requires varying each S¹ coordinate in Tᵏ freely. The image curve constrains all coordinates to move together (as x varies, all fᵢ(x) change simultaneously). Therefore:

- Tᵏ has k independent angular degrees of freedom
- S¹ (via Φ) provides 1 angular degree of freedom
- k > 1 ⟹ the single S¹ cannot realize the k CRT factor coordinates as independent coordinates

This is consistent with π₁(S¹) = Z and π₁(Tᵏ) = Zᵏ: a continuous surjection S¹ → Tᵏ would require a surjection Z → Zᵏ of abelian groups, which requires rank Z ≥ k. For k ≥ 2, rank Z = 1 < k. No such surjection exists.

**Conclusion.** The orthogonal jumps of Theorem 3 correspond geometrically to accessing independent angular coordinates of Tᵏ. Each jump adds one independent coordinate — one new S¹ factor. After k−1 jumps starting from any one factor partition, all k coordinates have been accessed, and Tᵏ-level information is fully realized. □

---

**Remark on k = 2 (Z/10Z).**
n = 2·5, k = 2. The image of Ψ in T² is the set of 10 points {(e^(2πix/2), e^(2πix/5)) : x = 0,...,9}, which lies on the (1,2)-torus curve (half-rotation in the first coordinate per full rotation in the second). One orthogonal jump = stepping from one S¹ coordinate to the second, independent S¹ coordinate. This matches the prior sprint exactly. □

---

## Summary

**Theorem 1 (Pairwise Incompatibility).**
For n = p₁···pₖ squarefree, distinct primes pᵢ ≠ pⱼ: the CRT factor partitions π_{pᵢ} and π_{pⱼ} are incompatible in the partition lattice. Neither refines the other. *Proved.*

**Theorem 2 (Meet = Discrete).**
meet(π_{p₁}, ..., π_{pₖ}) = π_disc. Any proper subfamily has strictly coarser meet. *Proved.*

**Theorem 3 (k−1 Jump Necessity in the CRT Family).**
Every minimal sufficient CRT-family viewpoint flow on Z/nZ (n squarefree, k prime factors) has length exactly k and contains exactly k−1 orthogonal jumps. No refinement move exists within the CRT family. *Proved.*

---

**Strongest honest claim:**
> Within the CRT family, the number of orthogonal jumps required is exactly k−1, is achieved by any ordering of the k factor partitions, and is a direct consequence of the algebraic independence of prime moduli. This is not a contingent fact about representations — it is the partition-lattice expression of the CRT theorem itself.

**Strongest honest boundary:**
> Whether k−1 is a lower bound on orthogonal jumps across *all* admissible representations (not just the CRT family) is an open problem. Non-CRT representations (reflection, orbit, gcd-class) may share information across CRT coordinates in ways that have not been fully analyzed. The conjecture that no representation family achieves sufficiency with fewer than k−1 jumps is plausible but unproved. A proof would require characterizing all partitions of Z/nZ whose meet with the CRT family accelerates discrete recovery — this is a combinatorial number-theory problem distinct from anything proved here.

---

**Next sprint candidate:** Prove or refute the conjecture. Specifically: does there exist, for any squarefree n with k ≥ 3 prime factors, a set of k−1 pairwise-incompatible non-CRT partitions of Z/nZ whose meet equals π_disc? If yes, then k−1 is tight across all representation families and the CRT family is not uniquely minimal. If no, then the CRT family is the canonical minimal family and the jump count is universally k−1.
