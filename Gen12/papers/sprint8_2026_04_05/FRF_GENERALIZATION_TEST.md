# FRACTAL RECURSIVE FLOW — GENERALIZATION TEST
## Does the Z/10Z result persist across other moduli?

**Date:** 2026-04-05  
**Question:** Do the three Sprint 8 results (coarse agreement, recursive divergence, gate behavior) hold for ℤ/6ℤ, ℤ/12ℤ, ℤ/18ℤ, ℤ/20ℤ?  
**Answer:** Partially. The coarse agreement theorem extends conditionally. The full 4-view divergence is specific to ℤ/10ℤ in this test set.

---

## RESULT 1: COARSE AGREEMENT — CONDITIONAL

**CRT = UG always (for any n).**  
The CRT type partition and the UG orbit partition agree for all tested moduli. This is expected: both partition ℤ/nℤ by the same ring-theoretic property (unit/zero-divisor/zero in each prime-power factor).

**DYN = UG if and only if (ℤ/nℤ)* is cyclic.**  
With a single max-order generator, DYN partitions ℤ/nℤ into one cycle per UG orbit — but only if the unit group is cyclic, so the single generator spans the entire orbit.

| n | (ℤ/nℤ)* cyclic? | DYN = UG? |
|---|---|---|
| 6 | Yes (λ=φ=2) | Yes |
| **10** | **Yes (λ=φ=4)** | **Yes** |
| 12 | No (λ=2 < φ=4) | No — {1,5,7,11} splits into {1,5} and {7,11} |
| 18 | Yes (λ=φ=6) | Yes |
| 20 | No (λ=4 < φ=8) | No — {1,3,7,9,...} over-splits |

**The cyclicity criterion:** (ℤ/nℤ)* is cyclic exactly for n ∈ {1, 2, 4, pᵏ, 2pᵏ} (odd prime p). The Sprint 8 theorem holds for this class of moduli, not universally.

**SPEC with full-unit Cayley graph:** For the additive Cayley graph with S = all units, the spectral projection separates the coarse classes (VOID, BALANCE, unit orbit, even orbit) correctly. SPEC = UG at the coarse level for n=6,10,18. For n=12,20 the non-cyclic structure causes additional spectral splits.

---

## RESULT 2: LEVEL-1 DISTINCT VIEWS — NOT UNIVERSAL

For the unit orbit specifically, the number of genuinely distinct Level-1 refinements across the four representations varies:

| n | Unit orbit | Distinct Level-1 views | Structure |
|---|---|---|---|
| 6 | {1,5} | **2** | CRT separates; UG=SPEC=DYN all give {{1,5}} |
| **10** | **{1,3,7,9}** | **Depends on SPEC choice** | With S={1,3,7,9}: 2 distinct; with S={3,7}: 3 distinct |
| 18 | {1,5,7,11,13,17} | **2** | CRT=discrete; UG=4 classes; SPEC=DYN={{all}} |

The Sprint 8 analysis used SPEC with S={3,7} (the PROGRESS-COLLAPSE generator pair), not the full unit group. With S={3,7}, the spectral projection gives a non-trivial INTERMEDIATE refinement {{1,9},{3,7}} of the unit class — coarser than CRT's discrete refinement but finer than DYN's trivial refinement. This intermediate level is what creates the 3-way (or 4-way including DYN's orbit-order) divergence.

**The S={3,7} choice is special to n=10:** The pair {3,7} is "reflection-symmetric" modulo 10 (3+7=10), which makes their Cayley graph spectrum land in ℚ(φ). For other n, finding an analogous intermediate-refinement generator pair requires separate analysis.

---

## RESULT 3: GATE BEHAVIOR — HOLDS CONDITIONALLY

The gate phenomenon (a class is visible under representation A but unresolvable without switching to B) holds wherever there is any non-trivial intra-class structure.

| n | Gate class | Visible under | Unresolvable without |
|---|---|---|---|
| 6 | {1,5} | CRT only | UG/SPEC/DYN all stall at {{1,5}} |
| **10** | **{3,7}** | **UG and SPEC(S={3,7})** | **CRT or DYN required to split** |
| 18 | {5,11} | UG (order-6 generators grouped together) | CRT or DYN required to split |

The gate phenomenon generalizes: wherever a non-singleton class exists in the Level-1 refinement of any representation, it constitutes a gate for representations that produced that class. For ℤ/6ℤ, the gate is at {1,5} (CRT resolves; UG/SPEC/DYN stall). For ℤ/18ℤ, the gate is at {5,11} (the order-6 generators).

---

## WHAT IS SPECIFIC TO ℤ/10ℤ

Three conditions converge at n=10 that do not all hold simultaneously for n=6 or n=18:

**Condition A — Cyclic unit group with φ(10)=4:**  
Gives a unit orbit of size 4, which is small enough for complete analysis but large enough for non-trivial internal structure. n=6 has only 2 units; n=18 has 6 (finer internal structure but harder to visualize).

**Condition B — Generator pair with reflection symmetry:**  
The pair {3,7} satisfies 3+7=10≡0, making ω^(3x) and ω^(7x) complex conjugates for all x. This forces the Cayley graph Cay(ℤ/10ℤ,{3,7}) to have real eigenvalues in ℚ(φ). For n=18, the generators {5,11}: 5+11=16≠18, so they are not a reflection pair. The "golden spectral structure" is specific to the {3,7} pair in ℤ/10ℤ.

**Condition C — SPEC gives a strictly intermediate refinement:**  
With S={3,7} on ℤ/10ℤ: SPEC gives {{1,9},{3,7}} — coarser than CRT's discrete {{1},{3},{7},{9}} but finer than DYN's trivial {{1,3,7,9}}. This three-level hierarchy (fine / intermediate / trivial) is what makes the gate at {3,7} non-degenerate. For n=6, there is no intermediate level: CRT is the only non-trivial refiner.

---

## HONEST SUMMARY

| Claim | Status |
|---|---|
| Coarse agreement theorem | Holds for all n with cyclic (ℤ/nℤ)* using correct representations |
| Recursive divergence (Gap_recursive > 0) | Holds for all tested n (CRT always gives a different refinement) |
| Gate behavior | Holds for all tested n (any non-trivial intra-class class constitutes a gate) |
| 4 genuinely distinct Level-1 views | Specific to ℤ/10ℤ with S={3,7} choice; not observed for n=6,18 |
| φ in the spectrum | Specific to Cay(ℤ/10ℤ,{3,7}) with reflection-symmetric S; not automatic for other n |
| Full FRF as stated in Sprint 8 | Holds for ℤ/10ℤ; partially holds for n=6,18; fails for n=12,20 (non-cyclic unit group) |

---

## NEXT STEP

The generalization program requires:
1. A general theorem characterizing which n admit the "4-distinct-views" FRF behavior
2. For each n with cyclic (ℤ/nℤ)*, finding the analogue of the {3,7} generator pair (reflection-symmetric generators that produce an intermediate spectral refinement)
3. Testing whether the gate structure generalizes to prime powers pᵏ vs products 2p

The Sprint 8 theorem stands as a **local theorem about ℤ/10ℤ** with a clear statement of what conditions it uses. The generalization is an open program, not an established result.
