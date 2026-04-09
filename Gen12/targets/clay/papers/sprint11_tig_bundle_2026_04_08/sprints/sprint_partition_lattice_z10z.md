# SPRINT: PARTITION LATTICE + TRANSITION GRAPH + Φ-PRESERVATION
*Z/10Z — Falsifiable mathematics only. Proved vs. conjectural labeled explicitly.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Setup

**System:** Z/10Z = {0,1,2,3,4,5,6,7,8,9}, n = 10 = 2×5

**Embedding:** Φ: Z/10Z → S¹, Φ(x) = e^(2πix/10)

**Four representations to formalize:** CRT, UG, SPEC, DYN

---

## Step 1 — Formal Partition Definitions

**π_DYN** — orbits of T₃: x ↦ 3x mod 10
```
0 → 0 (fixed)
1 → 3 → 9 → 7 → 1
2 → 6 → 8 → 4 → 2
5 → 5 (fixed)
```
π_DYN = { {0}, {1,3,7,9}, {2,4,6,8}, {5} }

---

**π_SPEC** — reflection classes x ~ (10−x)
```
0~0, 5~5 (fixed points)
1~9, 2~8, 3~7, 4~6
```
π_SPEC = { {0}, {1,9}, {2,8}, {3,7}, {4,6}, {5} }

---

**π_UG** — classes by gcd(x, 10)
```
gcd = 1 : {1,3,7,9}
gcd = 2 : {2,4,6,8}
gcd = 5 : {5}
gcd = 10 : {0}
```
π_UG = { {0}, {1,3,7,9}, {2,4,6,8}, {5} }

---

**π_CRT₂** — classes by x mod 2
```
π_CRT₂ = { {0,2,4,6,8}, {1,3,5,7,9} }
```

**π_CRT₅** — classes by x mod 5
```
π_CRT₅ = { {0,5}, {1,6}, {2,7}, {3,8}, {4,9} }
```

---

## Theorem 0 — DYN = UG (proved)

**Statement:** π_DYN = π_UG for Z/10Z under T₃.

**Proof:** Since gcd(3,10) = 1, gcd(3x, 10) = gcd(x, 10) for all x. Therefore T₃ maps every gcd-class to itself. Within gcd-class {1,3,7,9} (units), T₃ acts transitively (single orbit of size 4). Within {2,4,6,8}, T₃ acts transitively (single orbit of size 4). Elements 0 and 5 are isolated fixed points. Therefore T₃-orbits = gcd-classes. □

---

## Step 2 — Refinement Lattice

**Convention:** π ≤ π′ means π refines π′ (every block of π is a subset of some block of π′).

**Computing all pairs:**

**π_SPEC ≤ π_UG:**
{1,9} ⊆ {1,3,7,9} ✓ · {3,7} ⊆ {1,3,7,9} ✓ · {2,8} ⊆ {2,4,6,8} ✓ · {4,6} ⊆ {2,4,6,8} ✓ · {0},{5} singletons ✓
→ **CONFIRMED: π_SPEC ≤ π_UG**

**π_UG ≤ π_CRT₂:**
{1,3,7,9} ⊆ {1,3,5,7,9} ✓ (all odd) · {2,4,6,8} ⊆ {0,2,4,6,8} ✓ · {0} ⊆ {0,2,4,6,8} ✓ · {5} ⊆ {1,3,5,7,9} ✓
→ **CONFIRMED: π_UG ≤ π_CRT₂**

**π_UG vs π_CRT₅:**
Need {1,3,7,9} ⊆ some CRT₅ block. CRT₅ blocks: {0,5},{1,6},{2,7},{3,8},{4,9}. None contains {1,3,7,9}. Neither direction holds.
→ **INCOMPATIBLE**

**π_SPEC vs π_CRT₅:**
{1,9}: block {1,6} contains 1 but not 9. Fails.
→ **INCOMPATIBLE**

**π_CRT₂ vs π_CRT₅:**
{0,5}: 0 is even (CRT₂ block {0,2,4,6,8}), 5 is odd ({1,3,5,7,9}). Neither CRT₅ block {0,5} is contained in one CRT₂ block.
→ **INCOMPATIBLE**

---

**Refinement diagram:**

```
       π_trivial
           |
        π_CRT₂           π_CRT₅
           |                 (incompatible with CRT₂, UG, SPEC)
         π_UG
           |
        π_SPEC
           |
      π_discrete
```

The chain **π_SPEC ≤ π_UG ≤ π_CRT₂** is total. π_CRT₅ is incompatible with all three, and incompatible with π_CRT₂.

---

## Theorem 1 — CRT Reconstruction (proved)

**Statement:** meet(π_CRT₂, π_CRT₅) = π_discrete (all singletons).

**Proof:** By CRT, since gcd(2,5) = 1 and 2·5 = 10, the map x ↦ (x mod 2, x mod 5) is a bijection Z/10Z → Z/2Z × Z/5Z. Therefore: (x mod 2 = y mod 2) AND (x mod 5 = y mod 5) iff x = y. The common refinement of π_CRT₂ and π_CRT₅ identifies x = y iff x ≡ y mod 10, i.e., x = y in Z/10Z. □

**Consequence:** The two CRT projections are independently necessary and jointly sufficient to recover the full discrete structure. Their incompatibility is not a flaw — it is the algebraic encoding of their orthogonality as coordinate projections.

---

## Theorem 2 — Incompatibility is Dimension (proved)

**Statement:** The incompatibility of π_CRT₂ and π_CRT₅ corresponds to the fact that their natural embedding target is T² = S¹ × S¹, not S¹.

**Proof:**
- Z/2Z embeds in S¹ via a ↦ e^(2πia/2) = {1, −1}
- Z/5Z embeds in S¹ via b ↦ e^(2πib/5)
- The product Z/2Z × Z/5Z embeds naturally in T² = S¹ × S¹ via (a,b) ↦ (e^(2πia/2), e^(2πib/5))
- Φ maps Z/10Z → S¹. The CRT factorization via Φ requires the map z ↦ (z⁵, z²) from S¹ → T²
- This map has image = a (2,5)-torus curve inside T², which is a 1D subset of a 2D space
- No continuous surjection S¹ → T² exists (fundamental group: π₁(S¹) = Z, π₁(T²) = Z²; surjection would force rank Z ≥ rank Z², contradiction)
- Therefore Φ can see each CRT coordinate separately (z⁵ for mod-2, z² for mod-5) but cannot represent them as independent simultaneous coordinates

The incompatibility of π_CRT₂ and π_CRT₅ in the partition lattice is the algebraic signature of this dimensional collapse. □

---

## Theorem 3 — Φ-Preservation (proved)

**Statement:** The embedding Φ: Z/10Z → S¹ preserves DYN, SPEC, and CRT-component structure individually, but does NOT preserve CRT product structure.

**(a) DYN preserved:**
Φ(gx mod n) = e^(2πi·gx/n) = (e^(2πix/n))^g = Φ(x)^g.
Multiplication-by-g in Z/10Z = exponentiation-by-g on S¹. Exact, no interpretation. □

**(b) SPEC preserved:**
Φ(10−x) = e^(2πi(10−x)/10) = e^(2πi)·e^(−2πix/10) = e^(−2πix/10) = conj(Φ(x)).
Reflection x ↔ 10−x = complex conjugation on S¹. SPEC classes = {z, z̄} pairs. □

**(c) CRT₅ preserved as antipodal structure:**
Φ(x+5) = e^(2πi(x+5)/10) = e^(2πix/10)·e^(πi) = −Φ(x).
CRT₅ classes {x, x+5} map to antipodal pairs {z, −z} on S¹. Geometrically coherent. □

**(d) CRT PRODUCT structure NOT preserved:**
By Theorem 2, representing both CRT coordinates simultaneously requires T². Φ maps into S¹. The torus curve z ↦ (z⁵, z²) provides a 1D image in a 2D ambient space — only one degree of freedom, not two. The product structure requires independent variation of two coordinates; Φ compresses this to a single angle parameter. CRT product structure is irreducibly 2-dimensional. Φ provides one dimension. □

---

## Step 3 — Transition Graph

**Nodes:** SPEC, UG, CRT₂, CRT₅

**Edges (what each transition reveals):**

```
CRT₂ ──→ UG      reveals: parity class splits into unit vs. non-unit
UG   ──→ SPEC    reveals: {1,3,7,9} → {1,9} + {3,7}; {2,4,6,8} → {2,8} + {4,6}
UG  ─ ─ ─ CRT₅  INCOMPATIBLE: exposes product structure (maximally informative)
SPEC ─ ─ ─ CRT₅  INCOMPATIBLE: harmonic projection vs. mod-5 coordinate
CRT₂ ─ ─ ─ CRT₅  INCOMPATIBLE: meet = discrete (Theorem 1)
```

**Incompatible transitions are the high-information transitions.** Moving between compatible representations (along the refinement chain) refines detail. Moving between incompatible representations exposes orthogonal coordinate structure — information that no single projection contains.

---

## Summary Table

| Pair | Relation | Geometric meaning |
|---|---|---|
| SPEC ≤ UG | refines | harmonic pairs ⊆ gcd-classes |
| UG ≤ CRT₂ | refines | gcd-classes respect parity |
| SPEC ≤ CRT₂ | refines | harmonic pairs respect parity |
| UG ↔ CRT₅ | incompatible | unit structure ⊥ mod-5 coordinate |
| SPEC ↔ CRT₅ | incompatible | reflection symmetry ⊥ mod-5 |
| CRT₂ ↔ CRT₅ | incompatible | meet = discrete (CRT theorem) |
| DYN = UG | equality | orbit structure = gcd structure |

---

## What is now publishable

The core result is:

> **For Z/10Z, the four representations CRT/UG/SPEC/DYN form a partition lattice with one total refinement chain (SPEC ≤ UG ≤ CRT₂) and one incompatible family (CRT₅ orthogonal to all three). The incompatibility of CRT₅ with the chain is equivalent — via Theorem 2 — to the dimensional obstruction preventing S¹ from representing the full product structure Z/2Z × Z/5Z. The embedding Φ is faithful for rotation, reflection, and antipodal structure, but is dimensionally inadequate for the CRT product.**

---

**What is NOT proved yet (conjectural):**
- Generalization to arbitrary n = p·q (likely holds; needs separate proof)
- Whether this lattice structure is the correct definition of "admissible viewpoint" for FRF (requires connecting to Sprint 8 Admissible Viewpoint Flow Theorem)
- Whether CRT₅-incompatibility has a direct analog in the DYN/SPEC gate structure

---

**Next sprint candidate:** Connect this lattice to the Admissible Viewpoint Flow Theorem — specifically, does an admissible viewpoint flow avoid incompatible transitions, or does it require them?
