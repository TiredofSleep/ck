# DECOHERENCE_GUT_PHASE_II
## From Plausible Scaffold to Explicit Algebra or Identified Failure
*No hype. Explicit basis written. All claims labeled exact / structural / phenomenological / open.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — Explicit 35-Generator Basis

### 1.1 Choosing the Metric

**The (+1,−1,+1) sign structure with block decomposition:**

The 6-dimensional fundamental representation space **V = ℂ⁶** is decomposed as:

V = V_c ⊕ V_w ⊕ V_s

where:
- **V_c = ℂ³**: color subspace (3 complex dimensions, metric +1)
- **V_w = ℂ²**: weak subspace (2 complex dimensions, metric −1)
- **V_s = ℂ¹**: singlet subspace (1 complex dimension, metric +1)

**The pseudometric (exact):**

η = diag(+1, +1, +1, −1, −1, +1)  ∈ GL(6, ℝ)

This is a Hermitian form of signature (4, 2): four +1 entries (3 color + 1 singlet), two −1 entries (2 weak).

**The group preserving η:** SU(4,2) — the subgroup of GL(6,ℂ) satisfying:

g† η g = η  and  det(g) = 1

This is a non-compact real form of A₅ with dimension **35**. ✓

### 1.2 Generator Condition

A generator T of SU(4,2) satisfies:

T† η + η T = 0   (infinitesimal form of g†ηg = η)

Equivalently: (ηT)† = ηT, i.e., ηT is Hermitian.

Writing T in block form with V = V_c ⊕ V_w ⊕ V_s split as (3+2+1):

```
T = [[A   B   C],
     [D   E   F],
     [G   H   K]]
```

where A ∈ M_{3×3}(ℂ), E ∈ M_{2×2}(ℂ), K ∈ M_{1×1}(ℂ), etc.

The constraint T†η + ηT = 0 with η = diag(+I₃, −I₂, +I₁) gives block conditions:

- Diagonal blocks: A† = −A (anti-Hermitian, 3×3), E† = −E (anti-Hermitian, 2×2), K† = −K (anti-Hermitian, 1×1)
- Off-diagonal between +1 and +1 blocks (color-singlet): C† = −G, G† = −C (anti-Hermitian cross)
- Off-diagonal between +1 and −1 blocks (color-weak): B† = D (Hermitian cross — noncompact!)
- Off-diagonal between −1 and +1 blocks (weak-singlet): F† = −H, H† = −F (with sign flip)

**Key structural fact (exact):**

Generators connecting two subspaces with the **same metric sign** are anti-Hermitian (compact).
Generators connecting subspaces with **opposite metric sign** are Hermitian (non-compact).

Since V_c has sign +1 and V_w has sign −1: generators in the B and D blocks (color ↔ weak) are **Hermitian/non-compact**. These are the leptoquark-type generators.

### 1.3 The Explicit Basis

**Notation:** Let {e_i} be the standard basis of ℂ⁶, with e_1,e_2,e_3 spanning V_c, e_4,e_5 spanning V_w, e_6 spanning V_s. Define E_{ij} = e_i e_j† (the matrix with 1 in position (i,j), zeros elsewhere).

**Compact generators (anti-Hermitian, preserve metric sectors):**

*SU(3) sector (in V_c):* 8 generators

λ̃_a = (standard Gell-Mann matrices in upper 3×3 block) × (i/2)

Explicitly: T_a = (i/2)·diag_block(λ_a, 0₂, 0) for a = 1,...,8

Condition: T_a†η + ηT_a = (−i/2)λ_a† ⊕ 0 + (i/2)λ_a ⊕ 0 = 0 (since λ_a† = λ_a for Gell-Mann, so (i/2)(λ_a − λ_a†) = 0). Wait: we need T_a anti-Hermitian in the SU(4,2) sense. Let T_a = diag_block(A_a, 0, 0) where A_a is anti-Hermitian (A_a† = −A_a). Then T_a†η = diag(A_a†, 0, 0)·η = diag(A_a†, 0, 0) (η acts as +1 on color block). And ηT_a = η·diag(A_a, 0, 0) = diag(A_a, 0, 0). So T_a†η + ηT_a = diag(A_a† + A_a, 0, 0) = 0 iff A_a is anti-Hermitian. Use A_a = −(i/2)λ_a for a=1,...,8 (Gell-Mann matrices are Hermitian, so −iλ_a are anti-Hermitian). ✓

These 8 generators = **su(3) gluons**.

*SU(2) sector (in V_w):* 3 generators

T_{8+i} = diag_block(0₃, B_i, 0) where B_i = −(i/2)σ_i, σ_i = Pauli matrices.

Condition: T_{8+i}†η + ηT_{8+i}: the weak block has η = −I₂, so ηT_{8+i}|_{weak} = −B_i and T_{8+i}†η|_{weak} = B_i†·(−I₂) = B_i†·(−1). For B_i anti-Hermitian (B_i† = −B_i): T_{8+i}†η + ηT_{8+i}|_{weak} = (−B_i† − B_i) = (B_i − B_i) = 0. ✓

Wait: let me redo. T = diag_block(0, B, 0). T†η + ηT. In the weak-weak block: (T†)_{ww}·η_{ww} + η_{ww}·T_{ww} = B†·(−I₂) + (−I₂)·B = −B† − B. For this to be zero: B† = −B (anti-Hermitian). ✓ Use B_i = −(i/2)σ_i.

These 3 generators = **SU(2) weak bosons**.

*U(1) generators:* 2 generators (one for each independent Abelian factor)

T_{12} = diag(i·c₁, i·c₁, i·c₁, i·c₂, i·c₂, i·c₃) where c₁,c₂,c₃ are chosen for hypercharge.

The specific choice for SM hypercharge Y: 
T_Y = (i/6)·diag(+1,+1,+1,−3/2,−3/2,0) [up to normalization — exact normalization requires matter representation assignment]

A second U(1) from the SU(6)/SU(5) breaking: T_{13} = (i·k)·diag(2,2,2,−3,−3,0) for some k.

Condition: both are anti-Hermitian, and being diagonal they automatically satisfy T†η + ηT = 0 with the right block assignments. ✓

*Color-singlet mixing (compact cross):* Between V_c and V_s (both metric +1):

Off-diagonal between positions (i,6) and (6,i) for i=1,2,3. Six real generators:

T_{c-s, i}^{Re} = (1/2)(E_{i6} − E_{6i}) for i=1,2,3  (anti-Hermitian ✓)
T_{c-s, i}^{Im} = (i/2)(E_{i6} + E_{6i}) for i=1,2,3  (anti-Hermitian ✓)

These 6 generators mix color and singlet subspaces — still compact (both spaces have same metric sign).

Total compact so far: 8 + 3 + 2 + 6 = **19 compact generators**.

**Non-compact generators (Hermitian, mix metric-differing sectors):**

*Color-weak mixing (NON-COMPACT):* Between V_c (metric +1) and V_w (metric −1):

These are 3×2 = 6 complex = 12 real generators, but constrained:

For the off-diagonal block T|_{(c,w)}, the condition T†η + ηT = 0 gives:
- T_{wc}†·(+I₃) + (−I₂)·T_{wc}... let me redo for the off-diagonal.

Write T with only the (c,w) block nonzero: T = [[0,B,0],[D,0,0],[0,0,0]] where B is 3×2 (color rows, weak cols) and D is 2×3.

T†η + ηT: T† = [[0,D†,0],[B†,0,0],[0,0,0]]. With η = diag(+I₃,−I₂,+1):

(T†η)_{(c,c)} = 0, (T†η)_{(c,w)} = D†·(−I₂) = −D†, (T†η)_{(w,c)} = B†·(+I₃) = B†, etc.

(ηT)_{(c,w)} = (+I₃)·B = B, (ηT)_{(w,c)} = (−I₂)·D = −D.

Condition in each block:
(c,w): −D† + B = 0 → D† = B → D = B†  
(w,c): B† + (−D) = 0 → B† = D

Both give D = B†. So the non-compact color-weak generators are parameterized by B ∈ M_{3×2}(ℂ), giving:

T_{nc}(B) = [[0, B, 0],[B†, 0, 0],[0, 0, 0]]

This is a **Hermitian** matrix (since T_{nc}(B)† = T_{nc}(B†) and with D=B† it equals T_{nc}(B)). ✓ (Hermitian = non-compact for SU(p,q) algebras.)

Dimension: B ∈ M_{3×2}(ℂ) ≅ ℝ¹², giving 12 non-compact generators for the color-weak mixing. These are the **12 leptoquark/X,Y generators** (6 types × real+imaginary).

*Weak-singlet mixing (NON-COMPACT):* Between V_w (metric −1) and V_s (metric +1):

Same analysis: B ∈ M_{2×1}(ℂ) ≅ ℝ⁴, giving **4 non-compact generators** for the weak-singlet mixing.

Total non-compact: 12 + 4 = **16 non-compact generators**.

### 1.4 Dimension Count

Compact (sector-preserving): 8 + 3 + 2 + 6 = 19
Non-compact (cross-mixing): 12 + 4 = 16

**Total: 19 + 16 = 35.** ✓

The basis is complete. The algebra is su(4,2) as claimed.

---

## Part 2 — Exact Real Form Identification

### "Which 35-dimensional real form is it, exactly?"

**The construction gives su(4,2). Here is the proof.**

**Theorem (exact):** The set of 6×6 complex matrices satisfying T†η + ηT = 0 with det(e^T) = 1, where η = diag(+1,+1,+1,−1,−1,+1), forms a Lie algebra isomorphic to su(4,2).

**Proof sketch:**
1. The condition T†η + ηT = 0 defines the Lie algebra of the group {g ∈ GL(6,ℂ) : g†ηg = η}, which is the pseudo-unitary group U(4,2).
2. Adding the determinant constraint det(g)=1 (equivalently tr(T)=0 for the Lie algebra) gives SU(4,2).
3. The Lie algebra su(4,2) has dimension dim(U(4,2)) − 1 = 6² − 1 = 35. ✓
4. The real form is determined by the metric signature: signature (4,2) means 4 positive and 2 negative eigenvalues. With η = diag(+1,+1,+1,−1,−1,+1), there are 4 positive eigenvalues and 2 negative → signature (4,2) → real form su(4,2). □

**Killing form signature (structural, not fully computed here):**

For su(p,q) with p+q=n, the Killing form has signature:
- Compact generators (= su(p)⊕su(q)⊕u(1) subalgebra): contribute negative eigenvalues to Killing form
- Non-compact generators: contribute positive eigenvalues to Killing form

For su(4,2): compact subalgebra = su(4)⊕su(2)⊕u(1) with dimension 15+3+1 = 19. Non-compact generators: 35−19 = 16.

Expected Killing form signature: **(−19, +16)** approximately (sign reversed in some conventions).

This is indefinite — confirming **non-compact real form**. ✓ (Compact su(6) would have (−35, 0) — fully negative definite.)

**Why NOT su(3,3) or su(5,1):**

- su(3,3): metric (3,3). Would require 3 negative directions in V_w, not 2. Our construction has |V_w| = 2 negative directions. Doesn't match.
- su(5,1): metric (5,1). Would require only 1 negative direction. Our construction has 2. Doesn't match.
- su(4,2): metric (4,2). Three positive (V_c) + one positive (V_s) = 4 positive; two negative (V_w) = 2 negative. Matches exactly. ✓

**The identification is exact, given the block decomposition (V_c=3, V_w=2, V_s=1) with signs (+,−,+).**

---

## Part 3 — SM-Stable Subalgebra from the Explicit Basis

### 3.1 The Compact Subalgebra of SU(4,2)

**The compact subalgebra of su(4,2) (exact):**

The maximal compact subalgebra of su(p,q) is su(p)⊕su(q)⊕u(1). For su(4,2):

su(4) ⊕ su(2) ⊕ u(1)

with dimension 15 + 3 + 1 = 19.

This corresponds to:
- Generators preserving V_c ⊕ V_s (the +1 metric subspace, dim = 4): these form su(4)
- Generators preserving V_w (the −1 metric subspace, dim = 2): these form su(2)
- The U(1) phase generator mixing them

But the SM subgroup is su(3) ⊂ su(4) (not all of su(4)). The V_c ⊕ V_s = ℂ³ ⊕ ℂ¹ = ℂ⁴ is a 4-dimensional space. The full su(4) acting on ℂ⁴ has 15 generators. The SM color group su(3) preserves the color subspace V_c = ℂ³ and acts trivially on V_s — it is the embedding su(3) ↪ su(4) via:

T_a^{su(3)} = diag_block(A_a^{su(3)}, 0₂, 0) ⊂ su(4,2)

The **su(2)** weak generators in su(4,2) are exactly the generators of V_w = ℂ², which form the SU(2) compact factor.

**The SM gauge generators in the explicit basis:**

- **8 gluons:** T_a^{su(3)}, a=1..8. These are compact, preserve V_c. ✓
- **3 weak bosons:** T_i^{su(2)}, i=1,2,3. These are compact, preserve V_w. ✓
- **U(1) hypercharge:** A linear combination of the u(1) generator (mixing V_c⊕V_s and V_w) and the overall phase. Specific normalization requires matter representation assignment.

**The 6 color-singlet compact generators** (mixing V_c and V_s within the +1 metric sector): these belong to the su(4) factor but are NOT in the SM. They are compact but "beyond SM" — part of the SU(4)/SU(3) coset within the compact subalgebra.

### 3.2 Commutator Verification

**[SM, SM] closure (exact):**

[T_a^{su(3)}, T_b^{su(3)}] = f_{ab}^c T_c^{su(3)}: ✓ (SU(3) is a Lie algebra, closed by definition)
[T_i^{su(2)}, T_j^{su(2)}] = ε_{ijk} T_k^{su(2)}: ✓ (SU(2) is closed)
[T_a^{su(3)}, T_i^{su(2)}] = 0: ✓ (the blocks V_c and V_w are orthogonal in the matrix action — generators in different blocks commute)
[T_Y, T_a] = 0, [T_Y, T_i] = 0: ✓ (U(1) is Abelian; its generator is proportional to the identity on each sector)

**SM subalgebra closure is exact.** ✓

**[SM, cross] behavior (exact):**

A leptoquark generator T_{nc}(B) with B ∈ M_{3×2}(ℂ) transforms under su(3) and su(2) via the adjoint:

[T_a^{su(3)}, T_{nc}(B)] = T_{nc}(A_a · B)  (A_a acts on the color-row index of B)

The result is another leptoquark generator with B replaced by A_a·B — still in the (3,2) representation. This stays in the cross sector. ✓

[T_i^{su(2)}, T_{nc}(B)] = T_{nc}(B · B_i)  (B_i acts on the weak-column index of B)

Again, another leptoquark generator — stays cross. ✓

**[cross, cross] regenerates SM + cross (exact):**

[T_{nc}(B), T_{nc}(B')] = [[0,B,0],[B†,0,0],[0,0,0]], [[0,B',0],[B'†,0,0],[0,0,0]]]

Computing the (c,c) block: B·B'† − B'·B† (a 3×3 anti-Hermitian matrix → su(3) generator)
Computing the (w,w) block: B†·B' − B'†·B (a 2×2 anti-Hermitian matrix → su(2) generator)

So [leptoquark, anti-leptoquark] → su(3) ⊕ su(2) components. ✓ This regenerates SM generators.

**The decomposition is verified from the explicit basis:**

- [SM, SM] → SM (closed subalgebra)
- [SM, cross] → cross (cross generators form a representation of SM)
- [cross, cross] → SM + cross (the full algebra)

---

## Part 4 — Decoherence Projection as a Mathematical Map

### 4.1 The Minimum Environment Model

**What is required for the (η/2)^H and (η/2)^{2H} law to hold:**

The decoherence must be **dephasing in the metric-sector basis** — meaning the environment couples to the sector labels (color, weak, singlet) but not to the continuous gauge degrees of freedom within a sector.

**Minimum model (phenomenological, not fundamental):**

Let {|c⟩, |w⟩, |s⟩} label the three metric sectors. A "sector-dephasing" channel ε_η acts on density matrices of the 6-dimensional system as:

ε_η(ρ) = η · ρ · η_op + (1−η)·Π(ρ)

where Π is the complete dephasing projection (diagonal in sector basis) and η_op is the total coherence parameter.

Under this channel repeated H times:
- Elements within a single sector (e.g., color-color): survival ∝ (η/2)^H
- Elements between two sectors (e.g., color-weak): require coherence in BOTH sectors simultaneously: survival ∝ (η/2)^H × (η/2)^H = (η/2)^{2H}

**The factor-of-2 in the cross exponent:**

This is exact under the **independence assumption**: color decoherence and weak decoherence are statistically independent. If ρ_{color⊗weak} = ρ_color ⊗ ρ_weak (product state in the sector basis), then maintaining coherence across both sectors requires maintaining coherence in each separately. The joint amplitude is the product.

**Label: phenomenological effective rule.** The independence assumption is physically plausible (color and weak are different forces with different sector environments) but is not derived from a fundamental Lagrangian. It is a model assumption, not a theorem.

### 4.2 The Decoherence Map W_decoh (Formal Definition)

**Definition:** Let g be the su(4,2) algebra with basis split into compact generators {T_a^compact} and non-compact generators {T_α^nc}. Define the weighted norm on g:

‖T‖_{W} = Σ_a |c_a|² + w · Σ_α |c_α|²

where T = Σ_a c_a T_a^compact + Σ_α c_α T_α^nc and w = (η/2)^H for some coherence depth H ≥ 0.

**The decoherence projection map (exact definition):**

W_decoh: g → g is the projection operator:

W_decoh(T) = Π_compact(T) + (η/2)^H · Π_{nc}(T)

where Π_compact is the projection onto the compact (sector-preserving) generators and Π_{nc} is the projection onto the non-compact (cross-mixing) generators.

For cross generators mixing k sectors:

W_decoh(T_α^nc(k)) = (η/2)^{kH} · T_α^nc(k)

**W_decoh is a graded filtration on the algebra (structural, not a deformed bracket):**

Let g^{(k)} = span of generators mixing exactly k distinct metric sectors. Then:

g = g^{(0)} ⊕ g^{(1)} ⊕ g^{(2)}

where:
- g^{(0)}: generators within a single sector = compact generators (the 19 compact of su(4,2))
- g^{(1)}: generators mixing 2 adjacent sectors but within the same metric sign (e.g., color-singlet compact cross) — these are the 6 compact color-singlet generators
- g^{(2)}: generators mixing sectors of opposite metric sign (color-weak, weak-singlet) = the 16 non-compact generators

Wait: this is not quite right. Let me be more precise.

**Revised grading by metric-sign mixing:**

g^{(same)}: generators connecting subspaces with the same metric sign = compact generators
g^{(mixed)}: generators connecting subspaces with opposite metric sign = non-compact generators

W_decoh acts as:
- W_decoh|_{g^{(same)}} = (η/2)^H · identity
- W_decoh|_{g^{(mixed)}} = (η/2)^{2H} · identity

**W_decoh is NOT a Lie algebra homomorphism.** After applying W_decoh, the bracket:

[W_decoh(T), W_decoh(T')] ≠ W_decoh([T,T'])

in general, because [cross, cross] → SM, but W_decoh assigns different weights to cross and SM generators. The decoherence-weighted bracket is:

{T,T'}_W = W_decoh([T,T'])

This is NOT the original su(4,2) bracket. The IR algebra under W_decoh is NOT a subalgebra of su(4,2) in the bracket sense — it is a **graded truncation** that projects out the non-compact (mixed-sector) generators and retains the compact (sector-preserving) ones.

**The surviving structure as η → 0 (strong decoherence):**

As (η/2)^H → 0 for the compact generators and (η/2)^{2H} → 0 faster for the cross generators:

W_decoh → Π_compact = projection onto g^{(same)}

The IR algebra in the strong decoherence limit is:

g_IR = g^{(same)} = compact subalgebra of su(4,2) = su(4) ⊕ su(2) ⊕ u(1)

**This is NOT su(3) ⊕ su(2) ⊕ u(1). It is su(4) ⊕ su(2) ⊕ u(1).**

The SM algebra su(3) ⊕ su(2) ⊕ u(1) is a proper subalgebra of the decoherence-stable compact subalgebra su(4) ⊕ su(2) ⊕ u(1). The full decoherence-stable sector includes **6 extra su(4)/su(3) generators** that are compact but not SM.

**This is the most important finding of this pass.** See Part 5.

---

## Part 5 — Does Decoherence Break the Gauge Group, or Only Hide Part of It?

### "The Extra Compact Generators: The Failure Point"

**The decoherence projection W_decoh selects the compact subalgebra su(4) ⊕ su(2) ⊕ u(1) as the IR algebra, NOT su(3) ⊕ su(2) ⊕ u(1).**

The 6 extra generators (in the su(4)/su(3) coset within the compact sector) survive W_decoh with the same weight as the SM generators. They are compact, sector-preserving (within V_c ⊕ V_s), and do not mix the color and weak sectors. W_decoh cannot distinguish them from the gluons.

**These 6 extra compact generators correspond to:**
- The mixing between V_c = ℂ³ (color) and V_s = ℂ¹ (singlet)
- They transform as (3,1) and (3̄,1) representations under SU(3)
- They carry the (color triplet, no weak charge) quantum numbers

**For the decoherence story to produce the SM (not SM + extra SU(4)/SU(3) gauge bosons), a second mechanism is required:**

Either:
(A) A further spontaneous breaking SU(4) → SU(3) using a Higgs in some representation (e.g., a 4-plet of SU(4) with a VEV breaking SU(4) → SU(3)). This reintroduces Higgs physics at the SU(4)/SU(3) level.
(B) A further decoherence criterion that distinguishes V_c from V_s within the +1 metric sector. This would require a second metric asymmetry beyond the (+1,−1,+1) sign flip.
(C) The singlet V_s is already constrained to represent a different physical object (e.g., right-handed neutrino sector), and the SU(4)/SU(3) generators are identified as physical and massive via a different mechanism.

**The correct language for the current IR theory:**

The decoherence mechanism produces a **projection from su(4,2) onto its compact subalgebra su(4)⊕su(2)⊕u(1)**. This is:
- A graded truncation (not a subalgebra with the original bracket)
- An effective superselection rule (dynamics restricted to the compact sector)
- NOT spontaneous symmetry breaking (the full su(4,2) is still present in the UV)
- NOT a replacement for all Higgs physics (SU(4)→SU(3) still requires additional breaking)

**Electroweak breaking:** The decoherence argument as constructed says nothing about SU(2)×U(1) → U(1)_EM. This remains a separate problem requiring the Higgs mechanism or an equivalent. The current construction terminates at su(4)⊕su(2)⊕u(1), not at the electroweak scale.

---

## Part 6 — Ingredient Checklist

| Ingredient | Status | What Remains |
|---|---|---|
| UV algebra (35-dimensional) | **EXPLICIT** — su(4,2) with η=diag(+1,+1,+1,−1,−1,+1) | Explicit 35 generators constructed in Part 1 |
| Real form identification | **EXACT** — su(4,2) confirmed by metric signature (4,2) | Killing form computation would verify numerically; algebraic argument is exact |
| Block decomposition mechanism | **EXACT** — (+1,−1,+1) sign flip = (V_c,V_w,V_s) metric structure | Specified: color (+), weak (−), singlet (+) |
| Compact subalgebra | **EXPLICIT** — su(4)⊕su(2)⊕u(1), dimension 19 | Constructed in Part 1 |
| SM subalgebra closure | **EXACT** — su(3)⊕su(2)⊕u(1) ⊂ compact subalgebra | Verified in Part 3 |
| [SM,SM] closure | **EXACT** | Verified |
| [SM,cross] → cross | **EXACT** | Verified |
| [cross,cross] → SM+cross | **EXACT** | Verified |
| Decoherence map W_decoh | **FORMAL DEFINITION GIVEN** — graded filtration by metric-sign mixing | Independence assumption is phenomenological, not derived |
| Decoherence law exponents | **PHENOMENOLOGICAL** — plausible from product dephasing, not derived from fundamental Lagrangian | Need: specific environment model, master equation derivation |
| Decoherence selects SM exactly | **FAILS** — W_decoh selects su(4)⊕su(2)⊕u(1), not su(3)⊕su(2)⊕u(1) | 6 extra compact generators survive decoherence; require additional breaking mechanism |
| SU(4) → SU(3) breaking | **NOT ADDRESSED** | Requires Higgs (4-plet VEV) or additional decoherence criterion |
| Matter representations | **NOT ADDRESSED** | Quarks and leptons need assignments in representations of su(4,2) or su(6) |
| Chirality | **NOT ADDRESSED** | Gauge algebra is vector-like; chirality requires matter sector |
| Anomaly cancellation | **NOT CHECKED** | Requires explicit matter representation |
| Proton decay bound | **NOT COMPUTED** | Requires M_X from leptoquark sector; bound M_X ≳ 10¹⁵ GeV must hold |
| Coupling normalization | **NOT VERIFIED** | sin²θ_W and α_s predictions require normalization from explicit basis |
| Electroweak breaking | **NOT ADDRESSED** | SU(2)×U(1) → U(1)_EM still requires Higgs or equivalent |

---

## What Is Now Actually Shown

1. The explicit 35-generator basis of su(4,2) has been constructed from the (+1,−1,+1) sign flip with (V_c=3, V_w=2, V_s=1) block decomposition.
2. The real form is identified exactly as **su(4,2)** (not su(6), not su(3,3), not sl(6,ℝ)).
3. The compact subalgebra su(4)⊕su(2)⊕u(1) is identified and has dimension 19. The SM subalgebra su(3)⊕su(2)⊕u(1) is a proper subalgebra of this compact sector.
4. All commutator relations [SM,SM], [SM,cross], [cross,cross] are verified exactly from the basis.
5. The decoherence map W_decoh is formally defined as a graded filtration by metric-sign mixing degree.
6. A critical failure point is identified: W_decoh selects su(4)⊕su(2)⊕u(1), not the SM. The extra SU(4)/SU(3) generators survive decoherence alongside the gluons.

## What Still Blocks a True GUT Claim

**The primary new obstruction (found this pass):**

The decoherence mechanism projects onto su(4)⊕su(2)⊕u(1), which is 4 dimensions larger than the SM. The 6 extra compact generators (color-singlet mixing, the su(4)/su(3) coset) survive the decoherence filter. A second symmetry-breaking mechanism is required to reduce su(4) → su(3). This either reintroduces Higgs physics or requires a physically motivated extension of the decoherence criterion.

**The pre-existing gaps (not closed by this pass):**

Matter representations, chirality, anomaly cancellation, proton decay bound, coupling normalization, electroweak breaking.

**The decoherence story is real progress** — the explicit algebra is su(4,2), the compact subalgebra is provably su(4)⊕su(2)⊕u(1), and the SM sits inside it. But the story is not complete at the gauge sector level: su(4) ≠ su(3). The extra symmetry is a real problem.
