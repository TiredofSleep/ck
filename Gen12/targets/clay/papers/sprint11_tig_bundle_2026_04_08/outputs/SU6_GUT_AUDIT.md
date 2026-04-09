# SU6_GUT_AUDIT
## Honest Audit: From "35-Dimensional Closure" to Real GUT Candidate or Not
*Mathematics first. No hype. All claims labeled: exact / computed / structural / conjectural.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 0 — The Starting Claim (Restated Precisely)

**Stated:** Beginning with 11 generators (8 color + 3 weak), closure under commutation produces 35 independent generators. The resulting algebra is identified as su(6)-type, containing the Standard Model gauge algebra after symmetry breaking. The (+1,-1,+1) Hodge sign flip breaks the direct product and produces the extra 23.

**What needs to be audited before this becomes a claim:**

1. Does the closure actually give 35 dimensions, and if so, how?
2. Is the 35-dimensional algebra provably su(6) or only a dimension match?
3. Does the SM subalgebra sit inside it with the right structure?
4. Is the sign flip a genuine algebraic deformation or a basis artifact?
5. What is the chirality status?
6. What does symmetry breaking require?
7. What is the status of the numerical claims?

---

## Part 1 — The Closure Dimension: An Obstruction

**The standard block-diagonal embedding does not close to 35. This needs to be resolved before the rest proceeds.**

**Setup (exact):**

Embed SU(3) generators λ_a (a=1..8, Gell-Mann matrices, 3×3 anti-Hermitian) and SU(2) generators τ_i (i=1,2,3, Pauli matrices ×i, 2×2 anti-Hermitian) in the standard block-diagonal way inside 6×6 matrices:

```
L_a = [[λ_a | 0  | 0],    (upper 3×3 block for SU(3))
       [0   | 0  | 0],
       [0   | 0  | 0]]

R_i = [[0   | 0  | 0 ],   (middle 2×2 block for SU(2))
       [0   | τ_i| 0 ],
       [0   | 0  | 0 ]]
```

(with a U(1) generator possibly in the remaining diagonal entry)

**The commutator structure (exact):**

[L_a, L_b] = f_{abc} L_c (stays in the 3×3 upper block → SU(3) algebra)
[R_i, R_j] = ε_{ijk} R_k (stays in the 2×2 middle block → SU(2) algebra)
[L_a, R_i] = 0 (the blocks don't talk — block diagonal commutativity)

**Consequence (proved):** The Lie closure of {L_a, R_i} in the standard block-diagonal embedding is the 11-dimensional algebra su(3)⊕su(2). The commutators generate no new generators. You cannot get from 11 to 35 by taking commutators of block-diagonal generators.

**What this means for the claim:** The closure to 35 cannot come from the standard block-diagonal embedding. The claim requires one of:

(A) A non-block-diagonal embedding of the 11 generators in 6×6 matrices, such that [L_a, R_i] ≠ 0 and generates off-diagonal elements.

(B) The 11 generators are supplemented with additional "bridge" generators (the 23 extra) as input, and the full 35-dimensional set closes. In that case the claim is not "11 generators close to 35" but rather "a 35-dimensional set containing the 11 closes."

(C) The Hodge sign flip changes the algebra structure so that what were formerly zero cross-commutators become nonzero. If the sign flip modifies the inner product and therefore the structure constants, this is a genuine algebraic deformation — but it changes the algebra, not just the basis.

**Resolution required before proceeding:** Which mechanism is actually claimed? The answer determines whether the closure claim is valid and what algebra results.

---

## Part 2 — Is the 35-Dimensional Algebra Provably su(6)?

**Necessary and sufficient conditions to identify a real Lie algebra:**

35 dimensions means the algebra is a candidate for a simple Lie algebra of rank 5. The 35-dimensional simple Lie algebras are:

| Algebra | Real form | Dimension | Killing form signature |
|---|---|---|---|
| su(6) | compact | 35 | (−35) — negative definite |
| sl(6,ℝ) | split real | 35 | (10,25) — indefinite |
| su(p,6−p) for p=1,2,3 | non-compact | 35 | indefinite, varies |

**Dimension alone does not identify the algebra.** Four distinct real forms of A₅ all have dimension 35.

**The tests needed (exact methods):**

**Test 1 — Killing form signature.** Compute B(X,Y) = Tr(ad_X ∘ ad_Y) for a basis of the algebra. For su(6): negative definite everywhere. For sl(6,ℝ) or su(p,q): indefinite. If generators are anti-Hermitian complex matrices: the Killing form is negative semidefinite (compact form).

**Test 2 — Structure constant computation.** From the 35 generators {T_I}, compute [T_I, T_J] = f_{IJ}^K T_K and check:
- f_{IJ}^K fully antisymmetric (→ Lie algebra ✓)
- rank of Cartan subalgebra = 5 (→ A₅ candidate ✓)
- Dynkin diagram of root system matches A₅ (→ su(6) or real form ✓)

**Test 3 — Anti-Hermitian basis check.** If all generators are anti-Hermitian (T_I† = −T_I) as complex matrices, the real span is a compact real form → su(n) for some n. Hermitian generators → non-compact.

**Current status (labeled conjectural until computed):**

The identification "su(6)" is currently a dimension-match plus a plausibility argument based on the embedding context. It is a **candidate identification**, not a verified one. The algebra could be any of the four real 35-dimensional forms listed above. Only the Killing form computation or explicit structure constant verification resolves this.

**What needs to be done:** Produce the 35 generators explicitly as 6×6 anti-Hermitian complex matrices (if compact su(6) is the claim), compute their commutators, verify closure, and check the Killing form signature.

---

## Part 3 — Standard Model Embedding: What the Branching Must Look Like

**This is computable from standard Lie theory. Here is what is required and what is known.**

If the 35-dimensional algebra is su(6), the adjoint decomposes under the maximal subgroup chain SU(6) ⊃ SU(5) ⊃ SU(3)×SU(2)×U(1) as follows:

**Step 1: SU(6) → SU(5)×U(1)**

**35** of SU(6) → **24** + **5** + **5̄** + **1** under SU(5)×U(1)

(24 + 5 + 5 + 1 = 35 ✓)

**Step 2: SU(5) → SU(3)×SU(2)×U(1)_Y**

The **24** of SU(5) decomposes as:

**24** = **(8,1)₀** + **(1,3)₀** + **(1,1)₀** + **(3,2)_{−5/6}** + **(3̄,2)_{+5/6}**

Counting: 8 + 3 + 1 + 6 + 6 = 24 ✓

The **5** of SU(5):

**5** = **(3,1)_{−2/3}** + **(1,2)_{+1/2}**

Counting: 3 + 2 = 5 ✓

The **5̄** of SU(5):

**5̄** = **(3̄,1)_{+2/3}** + **(1,2)_{−1/2}**

**Step 3: Full adjoint 35 under SU(3)×SU(2)×U(1)**

| Representation | Multiplicity | Content | Role |
|---|---|---|---|
| **(8,1)₀** | 8 | SU(3) gluons | ← these are the 8 color generators |
| **(1,3)₀** | 3 | SU(2) weak bosons | ← these are the 3 weak generators |
| **(1,1)₀** | 2 | U(1) hypercharge (2 from SU(5) + SU(6)/SU(5)) | ← and U(1) |
| **(3,2)_{−5/6}** | 6 | leptoquark-type generators | bridge: color-weak mixing |
| **(3̄,2)_{+5/6}** | 6 | anti-leptoquark generators | bridge: color-weak mixing |
| **(3,1)_{−2/3}** | 3 | from **5** of SU(5) | additional bridge |
| **(3̄,1)_{+2/3}** | 3 | from **5̄** of SU(5) | additional bridge |
| **(1,2)_{+1/2}** | 2 | from **5** of SU(5) | additional bridge |
| **(1,2)_{−1/2}** | 2 | from **5̄** of SU(5) | additional bridge |

Total: 8+3+2+6+6+3+3+2+2 = **35** ✓

**The identification of the "23 extra generators":**

Starting from 8+3 = 11, the remaining 24 generators in the **24** plus the **5** + **5̄** + extra **U(1)** from SU(6)/SU(5) total:

- From **24**: 6+6 = 12 leptoquark generators (the **(3,2)** + **(3̄,2)**) + 1 extra U(1) = 13 from **24**
- From **5** + **5̄** in adj SU(6): 3+3+2+2 = 10
- From SU(6)/SU(5) U(1): 1

Total extra: 13+10+1 = 24... wait, 35-11=24. Let me recount: 35 total − 8 gluons − 3 weak = 24 extra, not 23. The U(1) hypercharge generator is the 12th of the original "SM" generators, so 35 − 12 = 23 extra. This is consistent with the claim **if** the U(1) is included in the "original 11" count. The claim says 11 = 8+3, not 12, so the 12th (U(1)) is among the generated extras. This is internally consistent.

**What the "bridge generators" are (exact, from branching):**

The 23 extra generators (from the adjoint of SU(6) beyond the SM generators) include:
- 6 + 6 = 12 leptoquark/X-Y boson generators in **(3,2)_{±5/6}** — these mediate quark-lepton transitions and are responsible for proton decay in SU(5) GUTs
- 3 + 3 = 6 generators in **(3,1)** representations — color triplet scalars in the adjoint
- 2 + 2 = 4 generators in **(1,2)** representations — weak doublet scalars in the adjoint
- 1 U(1) hypercharge generator

**This is exactly the SU(5)-type GUT bridge generator structure.** The content of the "23 extras" is fully determined by the standard SU(5)→SU(3)×SU(2)×U(1) branching. This is not new — it is the standard result of group theory applied to the adjoint of SU(6).

---

## Part 4 — The Hodge Sign Flip (+1,−1,+1): What It Can and Cannot Do

**Precise analysis:**

**What a sign flip in the inner product does:**

A sign flip (changing the Killing form signature) corresponds to changing the real form of the algebra. Under the "Cayley transform," compact generators (imaginary eigenvalues of ad) can be traded for non-compact generators (real eigenvalues) by multiplying by i.

Example: su(3) has generators T_a with T_a† = −T_a (anti-Hermitian). Change one generator T → iT: the new T' = iT satisfies (T')† = T' (Hermitian). The algebra of {Hermitian, anti-Hermitian} generators is a non-compact real form.

**The (+1,−1,+1) pattern:**

If applied to the three directions corresponding to the two SU(3) blocks and the SU(2) block in a 6×6 embedding (this would correspond to a (4,2) or (3,3) split in the metric signature), the result is:

- If (p,q) = (4,2): the real form is su(4,2) — the conformal algebra in (3+1)D (!) — dimension 35. This is a non-compact real form of A₅.
- If (p,q) = (3,3): the real form is su(3,3) — dimension 35. Another non-compact form.
- If (p,q) = (5,1): the real form is su(5,1) — dimension 35. Yet another.

**A (+1,−1,+1) signature in a 3-fold block structure could produce su(4,2) or su(3,3)** depending on how the sign flip acts on the 6 dimensions. These are real 35-dimensional algebras — but they are non-compact. For a physical gauge theory, non-compact groups give non-unitary representations in the standard sense, which is problematic.

**What the sign flip does NOT do (exact):**

The sign flip does not generate new generators from 11 to 35. A basis change (even one that changes the bilinear form) does not change the dimension of the algebra. If the 11 block-diagonal generators are in an algebra that closes to 11 dimensions, no redefinition of the inner product changes the algebra structure — it only changes the real form (compact vs non-compact).

**What the sign flip CAN do:**

If the 11 generators are embedded in a way that the sign flip forces them to sit inside a non-compact real form of a larger algebra — e.g., su(4,2) — then the sign flip is revealing that the generators' natural home is the larger algebra, not forcing them into it. The 35-dimensional closure would still require the additional 24 generators to be present (derived or assumed).

**The parity claim:**

The claim that the sign flip "explains parity violation" conflates two distinct things:
- **Algebraic asymmetry:** The (−1) signature in one direction creates a left-right asymmetry in the algebra structure. This is real.
- **Chiral asymmetry in representations:** This requires that the matter fields transform in inequivalent left-handed vs right-handed representations under the gauge group. The sign flip in the algebra does not automatically produce this.

The Standard Model is chiral because quarks and leptons sit in complex (not real or pseudoreal) representations: the **(3,2)_{1/6}** for the left-handed quark doublet vs **(3̄,1)_{2/3}** + **(3̄,1)_{1/3}** for right-handed quarks. This representation content cannot be derived from the sign flip in the algebra alone — it requires specifying the matter representation content, which is separate from the gauge algebra structure.

**Verdict on sign flip:** The mechanism is a real algebraic ingredient (it changes the real form of the algebra). Whether it addresses parity violation in the physical sense requires a separate representation theory analysis.

---

## Part 5 — The Chirality Problem

**The standard model is chiral. This is the central stress test.**

**What chiral means precisely:** The gauge group generators act inequivalently on left-handed vs right-handed fermions. Formally: the matter content is a complex representation of the gauge group — the representation R and its conjugate R̄ are inequivalent. For SU(5): quarks and leptons sit in the **5̄** and **10** of SU(5), which are complex representations.

**What SU(6) offers:**

SU(6) has complex representations: **6**, **6̄**, **15**, **15̄**, **21**, **21̄**, **35** (adjoint, real), etc.

The adjoint representation **35** is real (self-conjugate). Gauge bosons always sit in the adjoint, so the gauge sector is vector-like. Chirality must come from the matter sector.

**The question is about the matter representation:**

The claim being audited is about the gauge algebra (the 35-dimensional closure). This is the gauge boson sector. The matter fields (quarks and leptons) are separate — they sit in representations of the gauge group, and their chirality is determined by which representations they occupy.

For the construction to reproduce the SM chirality:
- Left-handed quark doublets (u_L, d_L) in **(3,2)_{1/6}** of SU(3)×SU(2)×U(1)
- Right-handed quarks in **(3,1)_{2/3}** and **(3,1)_{-1/3}**
- Left-handed leptons in **(1,2)_{-1/2}**, right-handed in **(1,1)_{-1}**

These need to come from a representation of SU(6). The standard assignment:
- **6̄** of SU(6) → **(3̄,1)_{1/3}** + **(1,2)_{-1/2}** + **(1,1)_0** under SU(3)×SU(2)×U(1)
- **15** of SU(6) → **(3,2)_{1/6}** + **(3̄,1)_{-2/3}** + **(3,1)_{-1/3}** + ... (partial list)

**The missing steps for chirality:**

1. The specific matter representation of SU(6) that reproduces the SM fermion content needs to be identified.
2. The anomaly cancellation conditions must be checked for these representations.
3. The mechanism by which the right-handed neutrino (if present) is given large mass must be identified.
4. Crucially: none of this follows automatically from the gauge algebra closure. The gauge algebra determines which gauge bosons exist. The matter content is an independent input.

**Current gap, stated plainly:**

The 35-dimensional algebra closure — if correct — establishes the gauge sector. The matter sector (where chirality lives) has not been addressed. This is a major unresolved component, not a minor technical detail. **The Standard Model chirality cannot be derived from the gauge algebra alone — it requires specifying and justifying the matter representation content.**

**What is missing for chirality:** A specific representation R of SU(6) containing the SM fermions, with the correct quantum numbers and anomaly cancellation, and a mechanism (likely symmetry breaking of SU(6) to the SM) that produces the chiral spectrum rather than a vector-like one.

---

## Part 6 — Symmetry Breaking

**SU(6) → SU(3)×SU(2)×U(1) is not derived. Here is what would be required.**

**The problem stated precisely:** A gauge theory with gauge group SU(6) has SU(6) symmetry. For the physical world to have only SU(3)×SU(2)×U(1) symmetry, the extra SU(6)/SM generators must be broken. In standard GUT model-building, this requires:

**Option A: Higgs mechanism.** Introduce scalar fields in representations of SU(6) that acquire vacuum expectation values (VEVs) aligned along the SU(3)×SU(2)×U(1) direction. Standard choice: a Higgs in the **35** or **189** of SU(6). The VEV alignment must be justified (why does it break to the SM and not to some other subgroup?).

**Option B: Geometric breaking.** In extra-dimensional models, boundary conditions can break the GUT group. Not standard 4D field theory.

**Option C: Dynamical breaking.** Strong-coupling effects at the GUT scale force a condensate. Requires non-perturbative analysis.

**What the current framework provides:** The algebra closure establishes what the unbroken symmetry group is. It says nothing about the breaking mechanism. The claim "SM sits inside after symmetry breaking" is trivially true for any GUT containing SU(3)×SU(2)×U(1) as a subgroup — but "sitting inside" is not the same as "explaining why it is the unbroken subgroup."

**Natural candidates from the framework:** If the Hodge sign flip distinguishes the SU(3)×SU(2)×U(1) direction algebraically (by some projection related to the ±1 signature), this could be the seed of a symmetry-breaking direction. But this needs to be made explicit: what is the VEV? What is its representation? What is the Higgs potential?

**What has to be added before this becomes a usable GUT candidate:**

1. A specific representation for the symmetry-breaking Higgs field
2. A potential (or other mechanism) that selects the SM as the unbroken subgroup
3. A matter sector with the correct representation content and anomaly cancellation
4. Yukawa couplings that reproduce fermion masses (after further breaking to U(1)_EM)
5. Proton decay rate calculation from the leptoquark generators (testable prediction)

None of these follow from the algebra closure alone.

---

## Part 7 — Numerical Claims Audit

**The three numerical claims examined:**

| Claimed number | Physical quantity | Source of claim | Exact derivation? | Normalization-dependent? | RG running needed? | Status |
|---|---|---|---|---|---|---|
| α_s ≈ 1/(12π) ≈ 0.0265 | Strong coupling | Algebraic | **No** | Yes — depends on coupling normalization and energy scale | Yes | Pattern-level match at best |
| α = 1/137 | EM fine structure | Observed value | **No** | Yes — depends on embedding U(1) normalization | Yes — this is the low-energy value | No derivation |
| sin²θ_W = 1/4 = 0.25 | Weinberg angle | Algebraic | **No** | Yes — depends on SU(2)/U(1) normalization ratio | Yes — measured at Z-pole is ~0.231 | Approximate only |

**Detailed assessment:**

**α_s = 1/(12π):**

The strong coupling at the Z boson mass scale is α_s(M_Z) ≈ 0.118 from experiment. The value 1/(12π) ≈ 0.0265 is the one-loop QCD running coupling at some energy scale, but not at a scale immediately identifiable with a natural GUT prediction. The factor 12π = 4π × 3 could come from a normalization convention with 3 colors. If this comes from a specific normalization of the SU(3) generators in the 6×6 embedding, it is a convention artifact until a physical derivation is given.

**α = 1/137:**

The fine structure constant at the electron mass scale α(m_e) ≈ 1/137. In any GUT, the three coupling constants unify at the GUT scale M_GUT ≈ 10¹⁵ GeV. The low-energy value 1/137 requires renormalization group (RG) running from M_GUT down to m_e — this is a 10+ order-of-magnitude running in energy. No algebraic argument produces the specific value 1/137 at the electron scale without this running. If the construction produces 1/137 without RG running, it is either a coincidence of normalization choices or incorrectly stated.

**sin²θ_W = 1/4:**

In the SU(5) GUT (parent of many SU(6) models), the tree-level prediction at the GUT scale is sin²θ_W = 3/8 = 0.375. After RG running to the Z-pole, the measured value ≈ 0.231. The value 1/4 = 0.25 is between the GUT-scale prediction and the observed value — plausible as a "halfway" result but not derived precisely from either. In some SU(6) embeddings, specific group-theoretic factors can give sin²θ_W = 1/4 at the matching scale. This requires specifying exactly which U(1) generator is identified as hypercharge and checking the normalization.

**Status of all three:** These are pattern-level matches that require additional work (normalization verification, RG running analysis, scale identification) before they can be called "derived." They may be correct — but they are not yet derived from the algebra.

---

## Part 8 — Claim Status Table

| Claim | Status | Reason |
|---|---|---|
| 11 generators close to a 35-dimensional algebra | **UNVERIFIED — depends on mechanism** | Standard block-diagonal embedding does NOT close to 35. A non-block-diagonal embedding or explicit generator construction is required first. |
| The 35-dimensional algebra is su(6) exactly | **CANDIDATE, NOT PROVEN** | Dimension matches A₅ = su(6). Real form (compact vs non-compact) requires Killing form signature check. Could be su(4,2), su(3,3), or sl(6,ℝ). |
| SM gauge algebra su(3)×su(2)×u(1) sits inside as subalgebra | **STRUCTURALLY TRUE for any SU(6) ⊃ SM embedding** | The adjoint branching (computed above) confirms SM generators appear in the 35. Their explicit identification in the 35 generators requires the explicit generator basis. |
| Bridge generators (the 23 extra) are leptoquark-type | **COMPUTED FROM BRANCHING** | Adjoint 35 under SU(3)×SU(2)×U(1) contains (3,2)_{±5/6} leptoquark generators + (3,1) + (1,2) types. This follows from standard group theory. |
| Hodge sign flip (+1,−1,+1) generates the extra 23 | **MECHANISM UNSPECIFIED** | Sign flip changes real form of algebra but does not increase dimension. If this means "reveals the SU(6) structure," the exact construction needs to be given. |
| Parity violation is explained | **NOT SHOWN** | The sign flip creates algebraic asymmetry but does not produce chiral matter representations. These are distinct. |
| Proton-decay-type generators appear | **STRUCTURALLY EXPECTED** | If the algebra is really SU(6)/SU(5)-based, proton decay generators are in the adjoint branching. They appear as (3,2)_{−5/6} generators. Decay rate prediction requires the full coupling and matter assignment. |
| Chirality emerges from the construction | **NOT SHOWN** | The gauge algebra is vector-like. Chirality requires the matter representation content to be specified separately. |
| Symmetry breaking SU(6) → SM is derived | **NOT DERIVED** | No breaking mechanism (Higgs field, VEV, potential) has been specified. |
| α_s ≈ 1/(12π), α ≈ 1/137, sin²θ_W ≈ 1/4 | **PATTERN-LEVEL ONLY** | None are derived from the algebra with verified normalizations and RG running. |

---

## Part 9 — Final Classification

**Between Class 2 and Class 3, with specific limitations:**

**Class 2 (genuine 35-dimensional Lie closure, identification unresolved):** The 35-dimensional claim requires an explicit construction of the 35 generators to verify. The dimension-match to su(6) is real but insufficient for identification.

**Class 3 (genuine su(6)-type candidate algebra with explicit SM subalgebra):** Partially reached. The adjoint branching of a genuine su(6) algebra under SU(3)×SU(2)×U(1) is computed and correct — the SM generators and the leptoquark bridge generators are accounted for. What is missing: the explicit generator basis (the 35 matrices), the Killing form check, and the mechanism that produces 35 generators from 11.

**Not Class 4 (candidate GUT scaffold with no chirality/breaking) yet:** Getting to Class 4 requires resolving the chirality and breaking questions.

**The gap between Class 3 and Class 4 is the gap between "the algebra is the right group" and "the physics is the right model."**

---

## What Is Actually Proved (Summary)

1. SU(6) is a genuine GUT candidate — this is standard physics, known since the 1970s (Georgi, Glashow, Frampton, etc.).
2. The adjoint **35** of SU(6) branches under SU(3)×SU(2)×U(1) to give SM gauge bosons + leptoquark bridge generators. This is computed and correct.
3. The dimension 35 = 6² − 1 matches A₅ = su(6). Necessary condition established.
4. If the algebra is identified as su(6), the SM subalgebra sits inside it and the bridge generators are the expected leptoquark generators.

## What Is Still Missing (Summary)

1. **Explicit generator construction:** The 35 generators as 6×6 matrices, derived from the 11 starting generators via the specified mechanism (not the block-diagonal embedding, which doesn't work).
2. **Real form identification:** Killing form computation to distinguish su(6) from su(4,2), su(3,3), etc.
3. **Sign flip mechanism specified:** Exactly how (+1,−1,+1) produces 35 from 11 — algebraically explicit, not schematic.
4. **Matter sector:** The representation R of SU(6) in which quarks and leptons sit — with correct quantum numbers and anomaly cancellation.
5. **Chirality mechanism:** How the chiral SM spectrum arises. Currently: not shown.
6. **Breaking mechanism:** Higgs field, VEV, potential, or alternative that selects SU(3)×SU(2)×U(1) as the unbroken subgroup.
7. **Coupling derivations:** Normalization-verified derivations of the numerical claims, including their scale and RG running.

---

## Dead / Alive / Narrowed Table

| Object | Status |
|---|---|
| SU(6) as GUT group (general claim) | **Alive** — established by standard physics; Georgi-Glashow-type models exist |
| 35-dimensional adjoint branching to SM+leptoquarks | **Alive** — computed above, standard group theory |
| "11 generators close to 35" via block-diagonal commutators | **Dead** — block-diagonal embedding stays at 11. A different mechanism is required. |
| Real form is compact su(6) | **Unresolved** — needs Killing form; could be su(4,2) or another real form |
| Hodge sign flip as mechanism | **Alive as concept, unresolved as construction** — needs explicit generator derivation |
| Chirality from gauge algebra | **Dead** — gauge algebra is vector-like; chirality requires matter sector input |
| SU(6) breaking to SM derived from framework | **Not shown** — needs explicit breaking mechanism |
| Numerical predictions α, α_s, sin²θ_W as derived | **Narrowed** — plausible as algebraic outputs with correct normalizations; not yet verified |
| This construction is novel vs existing SU(6) GUTs | **Unresolved** — depends on whether the sign-flip mechanism is distinct from known SU(6) models |

---

## Appendix: The Adjoint Branching (Computational Result)

**Adjoint 35 of SU(6) under SU(5)×U(1):**
35 → 24₀ + 5_{+6} + 5̄_{−6} + 1₀

**Adjoint 35 of SU(6) under SU(3)_c × SU(2)_L × U(1)_Y (via SU(5)):**

| Rep | Dim | Y | Physical role |
|---|---|---|---|
| (8,1)₀ | 8 | 0 | Gluons |
| (1,3)₀ | 3 | 0 | W bosons |
| (1,1)₀ | 1+1 | 0 | B (hypercharge) + U(1) from SU(6)/SU(5) |
| (3,2)_{−5/6} | 6 | −5/6 | X,Y leptoquarks (proton decay) |
| (3̄,2)_{+5/6} | 6 | +5/6 | X̄,Ȳ antileptoquarks |
| (3,1)_{−2/3} | 3 | −2/3 | From **5** of SU(5) in adj SU(6) |
| (3̄,1)_{+2/3} | 3 | +2/3 | From **5̄** |
| (1,2)_{+1/2} | 2 | +1/2 | From **5** |
| (1,2)_{−1/2} | 2 | −1/2 | From **5̄** |

Total: 8+3+2+6+6+3+3+2+2 = **35** ✓

The "23 extra beyond the 12 SM" are: the 12 leptoquarks + 6 color-triplets + 4 weak-doublets + 1 extra U(1) = 23. This matches the claim. **The content of the 23 is exactly the SU(5)-type leptoquark + extra adjoint matter generators.** This is a standard result of the SU(5) ⊂ SU(6) embedding.
