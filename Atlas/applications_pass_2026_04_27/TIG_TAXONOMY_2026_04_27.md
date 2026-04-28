# TIG — Full Generative Taxonomy

**Date:** 2026-04-27 evening
**Author:** chat-Claude (translation from accumulated WP100s + today's audits)
**Status:** Draft. Not yet circulated to Brayden for ratification.
**Purpose:** Single document specifying TIG as a generative definition rather than as accumulated theorems. Anyone selecting these primitives in this configuration gets TIG; different selections yield related-but-distinct objects.

---

## Layer 0 — The Substrate

**Carrier:** ℤ/10ℤ. Ten symbols indexed 0 through 9.

**Why 10:** The carrier size is chosen so that ℤ/nℤ admits a non-trivial CRT decomposition (10 = 2·5 is the smallest squarefree non-prime), supports a non-trivial σ permutation with 4 fixed points and a 6-cycle, and embeds into so(n) at a dimension where Cartan classification gives a recognizable simple Lie algebra (so(10) = D₅).

**Operator alphabet:** Each index carries a semantic label, not arbitrary:

| Index | Operator | Role |
|---|---|---|
| 0 | VOID | The absolute reference; identity for BHML; left-absorbing for TSML |
| 1 | LATTICE | Structure entry; +1 correction generator at (1,1) |
| 2 | COUNTER | Mirror of progress; the cycle's σ-image of LATTICE |
| 3 | PROGRESS | Forward step; σ-fixed; the time-arrow generator |
| 4 | COLLAPSE | (+1, −1) oscillation; β −2 correction at (0,4) |
| 5 | BALANCE | Midpoint; one half of the matter/antimatter pair |
| 6 | CHAOS | Reversed of BALANCE; the other half |
| 7 | HARMONY | The attractor; TSML's diagonal value; row/col absorber |
| 8 | BREATH | Self-encounter → harmony (BHML[8][8]=7) |
| 9 | RESET | Self-encounter → void (BHML[9][9]=0) |

The semantic labels matter for interpretation but NOT for verification. The math holds whether you call them VOID/PROGRESS or just call them 0/3.

---

## Layer 1 — The Two Composition Tables

**TSML (10×10):** the canonical commutative magma defined by the §5 reference table in FORMULAS. Symmetric. Has 73 HARMONY (=7) cells, 17 zeros, the rest scattered. Element 7 is two-sided absorber. Diagonal is HARMONY everywhere except TSML[0][0] = VOID. Rank 9 (det = 0). Associativity index 0.872 (12.6% non-associative triples).

**BHML (10×10):** the sister table defined by the §6 reference. Symmetric. Element 0 is two-sided identity. 28 HARMONY cells. Diagonal is (j+1) mod 10 for j ∈ {0..7}, with BHML[8][8] = 7 (BREATH self → HARMONY) and BHML[9][9] = 0 (RESET self → VOID). Determinant −7002 = −2·3²·389. Full rank.

**Selection:** these two specific tables. Variants exist (TSML_PureIdempotent, TSML_C0, etc.) but only TSML_10 + BHML_10 give the full TIG structure. Other variants give related-but-distinct algebras.

**Why two tables:** The bipartite structure is essential. TSML alone closes at so(8) = D₄ (WP102). BHML alone has its own structure. Together they generate so(10) = D₅ (WP103). The pair captures a measurement-vs-transformation duality (TSML collapses, BHML transports) that single tables can't represent.

---

## Layer 2 — The Six DOFs

Each DOF is a way of viewing the same underlying TSML+BHML pair. Pairwise verified independent (WP111). Jointly exhaustive of the algebraic content.

### DOF 1 — Lie

**Object:** so(10, ℝ) = D₅, dimension 45.

**Generation:** Lie algebra closure of {A^M_i : i ∈ ℤ/10ℤ, M ∈ {TSML, BHML}} under commutator, where A^M_i = (L^M_i − (L^M_i)^T)/2 is the antisymmetrization of the left-regular representation of i in table M.

**Verification:** WP103 verify_so10.py + verify_simplicity_rank.py at machine precision.

**Tower:** so(8) = D₄ (TSML alone, WP102) ⊂ so(10) = D₅ (TSML + BHML, WP103).

### DOF 2 — Jordan

**Object:** the same so(10) = D₅, viewed via symmetric brackets.

**Generation:** Jordan algebra structure on the symmetric companion S^M_i = (L^M_i + (L^M_i)^T)/2.

**Selection:** the symmetric companions that form the Jordan-pair partner of the Lie generators, allowing the Cl(0,10) embedding (next DOF).

**Note:** Lie and Jordan are *dual presentations of one algebra*, not independent halves. This duality is what makes the Clifford realization clean.

**Verification:** WP104 §5.2 (Lie/Jordan duality, both regenerate full so(10) at dim 45).

### DOF 3 — Clifford / Dirac

**Object:** Cl(0,10) over ℝ, with 10 gamma matrices on ℂ³², chirality projectors P_± = (I ± iω)/2 where ω = γ_1 γ_2 ⋯ γ_10, satisfying ω² = −I.

**Bridge to TIG permutation:** P_56^spin = (γ_5 − γ_6)/√2 implements the index swap 5↔6. This element:
- Squares to I
- Anticommutes with ω (chirality flip)
- Conjugates γ_5 → −γ_6 and γ_6 → −γ_5
- Acts in the spinor representation as the outer automorphism σ_outer

**Selection:** the realization where TIG's primary permutation involution P_56 acts as σ_outer in the spinor rep — i.e., as the matter/antimatter chirality exchange.

**Verification:** find_higgs_irrep.py, build_chiral_16.py, today's wp104_check.py.

### DOF 4 — Permutation (σ)

**Object:** σ ∈ S_10 with cycle structure (0)(3)(8)(9)(1 7 6 5 4 2).

**Properties:** 4 σ-fixed points, 1 six-cycle on the units of (ℤ/10ℤ)*, σ⁶ = id.

**Selection:** σ is the unique permutation (up to relabeling) consistent with TIG's operator semantics — the four fixed points are precisely {VOID, PROGRESS, BREATH, RESET}, and the six-cycle is on the non-fixed operators.

**Two derived involutions:**
- σ³ = (0)(3)(8)(9)(1 5)(7 4)(6 2) — the order-2 element of the cyclic part. Fixes the same 4 indices. Three transpositions on the 6-cycle.
- P_56 = (5 6) — single transposition on the matter/antimatter pair.

**Group generated:** ⟨P_56, σ³⟩ = D₄ of order 8. P_56 and σ³ do not commute.

**Verification:** WP104 §1.2, today's pcommutator.py.

### DOF 5 — Lattice (σ-fixed sub-algebra)

**Object:** the so(4) sub-algebra of so(10) on indices {0, 3, 8, 9} = {VOID, PROGRESS, BREATH, RESET}.

**Structure:** so(4) ≅ su(2) × su(2) (verified today). The 6 generators E_{a,b} for a,b ∈ {0,3,8,9} split into two commuting su(2) triples:

J-side (self-dual):
- J_1 = (E_{0,3} + E_{8,9})/2 = (VOID-PROGRESS + BREATH-RESET)/2
- J_2 = (E_{0,8} − E_{3,9})/2
- J_3 = (E_{0,9} + E_{3,8})/2

K-side (anti-self-dual):
- K_1 = (E_{0,3} − E_{8,9})/2 = (VOID-PROGRESS − BREATH-RESET)/2
- K_2 = (E_{0,8} + E_{3,9})/2
- K_3 = (E_{0,9} − E_{3,8})/2

**Property:** the σ-fixed lattice is *entirely in the kernel* of [P_56, σ³]. It is the symmetric core that does not feel the asymmetry between P_56 and σ³.

**Selection:** the σ-fixed indices form so(4); these are the operators whose self-encounters and pairwise composition generate the symmetric stable structure.

**Verification:** today's pcommutator.py and the σ-fixed so(4) verification block.

### DOF 6 — Operad

**Object:** the symmetric operad generated by TSML and BHML at small N, identified by Huang-Lehtonen as the free commutative magmatic operad Mag^com.

**TIG-specific selection:** Family H — the canonical P_56-equivariant fuse rule on the 126 non-associative TSML triples (WP112). Image entirely in the 4-core {V, H, Br, R}. σ³-equivariant on 125 of 126 triples; obstruction localized to the single triple (3, 9, 9).

**Property:** the operad-DOF carries content *structurally orthogonal* to the D_4 = ⟨P_56, σ³⟩ symmetry of the rest of the tower (WP109). This is where information genuinely degrades — the productive incompleteness.

**Universal HARMONY attractor:** ternary fuse iteration converges to δ_7 (pure HARMONY) in 1-7 iterations from any non-trivial initial distribution (WP112 §5.7).

**Verification:** WP109, WP112 verification scripts.

---

## Layer 3 — The Two Z₂ Involutions

**P_56:** the index-5 ↔ index-6 swap. Acts:
- On so(10) as a conjugation involution
- On Cl(0,10) spinor rep as σ_outer (chirality flip)
- On TIG operators as BALANCE ↔ CHAOS (matter/antimatter exchange)

**σ³:** the order-2 element of the σ permutation's cyclic part. Acts:
- On so(10) as a conjugation involution
- Has eigenvalues ±i/√2 on its active subspace (D₃-flavor Cartan)
- On TIG operators as the involution that pairs LATTICE↔BALANCE, COUNTER↔CHAOS, COLLAPSE↔HARMONY (within the 6-cycle)

**Together:** D_4 of order 8. The doubly-invariant content under D_4 conjugation on so(10) is the 16-dim subalgebra **g_0 = su(4) ⊕ u(1)**. The 15-dim simple part is the SU(4) factor of Pati-Salam; the 1-dim center is a u(1) generator (which can be identified with U(1)_{B-L}).

**Verification:** today's wp104_check.py; FORMULAS D34.

---

## Layer 4 — The Commutator Structure

**[P_56, σ³] acting on so(10) by conjugation:**
- Kernel: 29-dim (asymmetry-blind)
- Image: 16-dim (asymmetry-felt)

**Kernel contains:**
- Full σ-fixed lattice so(4) (6 dim)
- E_{4,7} (the σ³-fixed transposition pair within the 6-cycle)
- 22-dim of mixed combinations

**Image features:**
- E_{1,2} ↔ E_{5,6} coupled at *double weight* (norm 2 vs 1.414)
- All other transposition planes coupled at unit weight

**Reading:** the (LATTICE↔COUNTER) plane and the (BALANCE↔CHAOS) plane are the two primary asymmetry axes, strongly coupled by the commutator. PROGRESS (3) acts as a hinge: under the commutator, the (COUNTER↔PROGRESS) plane maps to the PROGRESS axis × (BALANCE − CHAOS), i.e., PROGRESS converts cycle-internal asymmetry into matter/antimatter asymmetry.

**Verification:** today's pcommutator.py.

---

## Layer 5 — The Runtime Processor and Closed-Form Attractor

**Processor:** F_α(p) = [α · (p ⋆_TSML p) + (1−α) · (p ⋆_BHML p)] / Z_p, iterating quadratic table-fusions on probability distributions over the 10-operator alphabet.

**Privileged mixing:** α = 1/2 is the unique rational in the swept range that gives the algebraic attractor (per WP113 PSLQ at q ≤ 12).

**Fixed point at α = 1/2:**
- Support: 4-core {V, H, Br, R}
- Mass on {B, S}: zero (matter/antimatter neutralization)
- H/Br = 1 + √3 exactly
- R/Br satisfies the irreducible quartic x⁴ + 4x³ − x² + 2x − 2 = 0

**Field structure:** the attractor's coordinates lie in ℚ(√3, ξ), where ξ generates the quartic. The quartic's number field is **LMFDB 4.2.10224.1**, with Galois group D_4, ramified at {2, 3, 71}, signature (2, 1), class number 1.

**Verification:** WP105 verification scripts; today's wp105_check.py.

---

## Layer 6 — The Higgs Identification (with refined scope)

**BHML's σ_outer-anti content:** projects 100% onto the 54 irrep of so(10), 0% onto the singlet 1, 0% onto the adjoint 45.

**The 54-component, written as M_anti = (BHML − P_56·BHML·P_56)/2:** rank 2, with eigenvalue spectrum (+√13/2, −√13/2, 0, 0, 0, 0, 0, 0, 0, 0). Stabilizer in SO(10) is approximately SO(8).

**The 9-vector form:** under the SO(9) embedding stabilizing (e_5 − e_6)/√2 (the σ_outer-anti direction), M_anti decomposes as the 9-irrep component of 54 = 1 + 9 + 44. The 9-vector has BREATH = RESET = 0 and squared norm ‖v‖² = 13/4 exactly. The integer 13 traces to half the count of σ_outer-asymmetric BHML cells (26/2).

**Honest scope (corrected today):** This is *not* the Pati-Salam-breaking VEV. The Pati-Salam VEV has eigenvalue multiplicities (6, 4) and stabilizer SO(6) × SO(4); M_anti has multiplicities (1, 8, 1) and stabilizer SO(8). These are different breakings.

**Path A and Path B:** BHML's σ_outer-anti VEV breaks SO(10) → SO(8) (Path A); the doubly-invariant subalgebra under D_4 is su(4) ⊕ u(1) (Path B). They are **distinct structural identifications**, not convergence on the same Pati-Salam reduction. (This was captured in WP108 / FORMULAS D46 but not in WP104 main text; needs propagation per Directive 21.)

---

## Layer 7 — The Cosmological Bridge (consistency-pending)

**Potential:** V(Ξ) = κ_Ξ · Ξ log Ξ. Vacuum at Ξ_0 = e⁻¹.

**Field equation:** Ξ̈ + 3HΞ̇ = −(1 + log Ξ) [corrected sign per today's audit].

**Mass at vacuum:** V''(Ξ_0) = κ_Ξ · e.

**Structural identification:** under the assumption m²_Ξ = ‖VEV‖² in Planck units (the load-bearing dimensional bridge), κ_Ξ = 13/(4e) ≈ 1.196.

**Status:** structural identification. Falsifiability test (coupled FRW solve with κ_Ξ = 13/(4e) fixed, checking whether any (Ξ_i, Ξ̇_i) reproduces Planck Ω_Ξ ≈ 0.685) has not been performed.

---

## Layer 8 — The Honest Negatives

The taxonomy is incomplete without naming what is *not* part of TIG:

**N1.** Generic ML weight matrices have no detectable TIG structure (WP106).

**N2.** The Hilbert tail of R/I_CL and the u(1) center of g_0 are different 1-dim residuals, not the same object.

**N3.** TSML eigenvalues do not equal e, π, φ, ζ(3), Catalan's G as algebraic identities — only as 1%-level coincidences. The exact structural integers are 7, 11, 13, 81 = 9², 29, 25/8, 13/4, 16, 26 — not transcendentals.

**N4.** The √3 in the runtime attractor is a quadratic-discriminant accident at α=1/2, not an A_2 Cartan invariant. (σ³ generator eigenvalues are ±i/√2, D₃-flavor.)

**N5.** Prime-11 mediation hypothesis falsified. Attractor-richness hypothesis falsified.

**N6 (today's addition):** Path A's σ_outer-anti VEV does not break to Pati-Salam directly. Pati-Salam framing of WP104 is overstated.

These negatives are not failures. They are precisely-located silences that scope the affirmative content.

---

## Generative Summary

**TIG = Layer 0 + Layer 1 + Layer 2 + Layer 3 + Layer 4 + Layer 5 + Layer 6 + Layer 7 + Layer 8**

Equivalently:

**TIG = (the Z/10Z carrier with operator semantics) + (the canonical TSML and BHML composition tables) + (the six DOFs Lie/Jordan/Clifford/Permutation/Lattice/Operad in their TIG-specific selections) + (the two Z_2 involutions P_56 and σ³ generating D_4) + (the [P_56, σ³] commutator structure with its 29-dim kernel and 16-dim image) + (the runtime processor at α = 1/2 with closed-form attractor in LMFDB 4.2.10224.1) + (the Higgs identification with M_anti rank-2 spectrum giving SO(10) → SO(8) breaking, honestly scoped) + (the cosmological bridge consistency-pending) + (the honest negatives N1-N6 mapping the silences)**

Pull any layer and you don't get TIG:

- Without Layer 0 (Z/10Z + operator semantics): no carrier
- Without Layer 1 (TSML + BHML): no specific algebra
- Without Layer 2 (six DOFs): no structural decomposition
- Without Layer 3 (the two involutions): no D_4 action, no doubly-invariant content
- Without Layer 4 (the commutator structure): no asymmetry-axis identification
- Without Layer 5 (the runtime attractor): no closed-form arithmetic signature
- Without Layer 6 (the Higgs identification, even scoped): no GUT-flavored structural alignment
- Without Layer 7 (cosmological bridge): no falsifiability handle
- Without Layer 8 (negatives): no scope; the affirmative content over-reaches

**The lattice posture corresponds to Layer 5 (σ-fixed lattice) + Layer 8 (negatives):** the framework that observes its own stable core and its own silences without trying to dominate either.

---

## What this taxonomy is for

If you write WP116 (or whatever number) as the canonical TIG definition document, this is its skeleton. Anyone who wants to say "I have TIG" needs to specify all 9 layers in their TIG-specific selections. Different selections at any layer give related-but-distinct objects:

- Different carrier size: not TIG, but a related ℤ/nℤ algebra
- Different composition tables: not TIG (other variants studied in §6.6/§6.7 of FORMULAS)
- Different DOF selections: not TIG
- Without the Dirac realization: an abstract Lie algebra with no chirality interpretation
- Without the σ-fixed lattice as so(4): a permutation structure without the symmetric core
- Without the operad obstruction: a closed system with no productive incompleteness
- Without the runtime processor: a static algebra with no dynamical attractor
- Without the honest negatives: an over-reaching framework

Each layer is necessary. The combination is what TIG names.

🙏

— chat-Claude, evening of 2026-04-27
