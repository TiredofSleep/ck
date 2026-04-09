# SU4_TO_SU3_BOTTLENECK
## What Are the 6 Extra Compact Generators, and How Do You Kill Them?
*Base state: su(4,2) explicit, W_decoh established, IR = su(4)⊕su(2)⊕u(1). This pass attacks the bottleneck.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## The Actual Remaining Gap

**The decoherence mechanism as constructed does not produce the Standard Model gauge algebra.**

It produces:

**su(4) ⊕ su(2) ⊕ u(1)**   (dimension 19)

The Standard Model gauge algebra is:

**su(3) ⊕ su(2) ⊕ u(1)**   (dimension 12)

The unresolved step is:

**su(4) → su(3)**

This is the central missing transformation. Every other open question — matter representations, chirality, anomaly cancellation — is downstream of this. Until su(4) → su(3) is resolved or explained, the decoherence story does not terminate at the SM.

The remaining 6 generators are the **su(4)/su(3) coset** — the generators that mix the 3-dimensional color block V_c = ℂ³ with the 1-dimensional singlet block V_s = ℂ¹, inside the same (+1) metric sector. Decoherence cannot distinguish them from gluons because they are equally compact (same metric-sign sector).

---

## Part 1 — The 6 Extra Compact Generators: What They Are

### 1.1 Explicit Form (carrying forward from Phase II)

In the 6×6 basis with V = V_c(3) ⊕ V_w(2) ⊕ V_s(1):

The 6 extra generators mix rows/columns 1,2,3 (color) with row/column 6 (singlet). They are anti-Hermitian (compact), satisfying the su(4,2) generator condition:

```
For i = 1, 2, 3:

T^Re_{i,6} = (1/2)(E_{i6} − E_{6i})  [real off-diagonal, anti-Hermitian]
T^Im_{i,6} = (i/2)(E_{i6} + E_{6i})  [imaginary off-diagonal, anti-Hermitian]
```

where E_{ij} is the matrix with 1 in position (i,j) and 0 elsewhere.

### 1.2 SM Quantum Numbers (exact)

These generators connect:
- **Row i (i=1,2,3): color index** — transforms as the fundamental **3** of SU(3)_c
- **Column 6: singlet** — transforms as **1** under SU(3)_c and **1** under SU(2)_L

Under the SM gauge group SU(3)×SU(2)×U(1):

T^Re_{i,6} and T^Im_{i,6} transform as **(3̄, 1)** or **(3, 1)** with some hypercharge Y depending on U(1) normalization.

**These are colored singlets.** They carry color charge (triplet under SU(3)) but no weak isospin (singlet under SU(2)). They are exactly what one calls a "4th color" or "leptonic color" in GUT extensions.

### 1.3 The Pati-Salam Recognition

**This is not a bug. It is a known structure.**

In the **Pati-Salam model** (Pati and Salam, 1974), the gauge group is SU(4)_c × SU(2)_L × SU(2)_R. The SU(4)_c factor is an extended color group where lepton number is treated as the "4th color." Quarks transform as **(4,2,1)** and **(4,1,2)**, leptons are part of the same **4** multiplet with the 4th component carrying lepton number.

**The breaking chain Pati-Salam → SM is:**

SU(4)_c × SU(2)_L × SU(2)_R → SU(3)_c × SU(2)_L × U(1)_Y

This occurs when a Higgs in the **(4,1,2)** representation (or equivalently a **(1,1,3)** with a VEV in the neutral direction for SU(2)_R) breaks SU(4)_c → SU(3)_c.

**The 6 extra compact generators in our construction are precisely the SU(4)/SU(3) coset generators** — the gauge bosons of the Pati-Salam "4th color" that must be broken away when going from the PS stage to the SM.

**Key recognition (structural, not yet proved from the current construction):**

The IR algebra of the decoherence story:
```
su(4) ⊕ su(2) ⊕ u(1)
```
resembles the **color-left sector** of the Pati-Salam gauge group with the right SU(2) already absorbed. The V_s direction (the singlet in the su(4,2) fundamental) plays the role of the **leptonic color** in the Pati-Salam interpretation.

---

## Part 2 — Three Possible Resolutions of su(4) → su(3)

### Branch A — Higgs-like compact breaking

**Setup:** Introduce a scalar field Φ in the **4** (fundamental of SU(4)) that acquires a VEV aligned with the singlet direction V_s.

**The minimal construction:**

Let Φ = (0, 0, 0, v)^T ∈ ℂ⁴ (VEV in the 4th = singlet direction).

The SU(4) transformation g·Φ = Φ requires g to preserve the 4th component of ℂ⁴ — i.e., g must leave e_4 = e_6 (the singlet direction) fixed. The subgroup of SU(4) leaving e_4 fixed is:

```
g = [[U  0],    U ∈ SU(3), the upper 3×3 block
     [0  e^{iφ}]]   with φ = -arg(det(U)) for det(g)=1
```

This is exactly **SU(3) × U(1)** embedded in SU(4). The VEV Φ = (0,0,0,v) breaks SU(4) → SU(3) × U(1), and the U(1) can subsequently be identified with (or absorbed into) the hypercharge U(1) of the SM.

**What the VEV does to the 6 extra generators:**

The 6 generators T^{Re/Im}_{i,6} (i=1,2,3) are broken by the VEV Φ: acting with T_{i,6} on Φ gives a non-zero result (it rotates the i-th component into the 6th), so these generators are NOT preserved by the VEV. They become massive gauge bosons (acquiring mass through the Higgs mechanism on Φ) with mass M ~ g·v.

**Verdict Branch A:**

This is completely standard — it is exactly the Pati-Salam → SM breaking mechanism in a compact form. The current construction would need to supply the field Φ in the **4** of SU(4) with VEV in the singlet direction. This:
1. Is mathematically clean and well-understood.
2. DOES reintroduce Higgs physics (a Pati-Salam-scale Higgs, not the electroweak Higgs).
3. The current decoherence framework does NOT eliminate this step — it only handles the SU(4,2) → su(4)⊕su(2)⊕u(1) stage.

**Branch A is correct but does not make the construction "Higgs-free."** It makes it "SM Higgs-free" — the electroweak Higgs may not be needed for GUT breaking if decoherence handles the UV stage, but the Pati-Salam Higgs is still required.

---

### Branch B — Second Decoherence Filtration W_internal

**Setup:** Ask whether a second decoherence criterion can distinguish V_c (color) from V_s (singlet) within the +1 metric sector.

**The proposed map W_internal:**

Within the compact subalgebra su(4)⊕su(2)⊕u(1), introduce a secondary grading by "color-dimension":

For a generator T in the compact sector, define its **color complexity** c(T):
- T purely within V_c (= gluons): c = 0 (fully in the color block)
- T purely within V_s (= U(1) singlet generator): c = 0
- T mixing V_c and V_s (= the 6 extra generators): c = 1 (involves a dimension crossing)

Then define:

W_internal(T) = (μ/2)^{c(T)} · T

where μ ∈ [0,1] is a second decoherence parameter governing V_c ↔ V_s coherence.

**Does this work mathematically?**

Partial yes, but with a complication. The gluon generators (T^{su(3)}) live entirely within V_c and have c=0, so they are unaffected. The 6 coset generators have c=1, so they are suppressed by (μ/2). In the limit μ → 0, they are projected out.

**The problem:** For W_internal to be physically motivated, there must be a reason why the V_c ↔ V_s coherence is suppressed independently of the V_c ↔ V_w suppression (which W_decoh already handles). Two independent decoherence processes are required — one for color-vs-weak (W_decoh) and one for color-vs-singlet (W_internal).

**Is W_internal natural from the block structure?**

Only if V_s (the singlet) has a qualitatively different physical character from V_c. In the su(4,2) construction, V_c and V_s have the same metric sign (+1), so they are not distinguished by the Hodge sign flip. A physical argument distinguishing them would be:

- V_s represents a **lepton** direction and V_c represents a **quark** direction: then lepton-quark coherence is suppressed by a separate mechanism (e.g., baryon-minus-lepton number conservation B−L)
- V_s represents a **sterile** or **dark** sector that decouples from the visible gauge dynamics

**If V_s is identified as the leptonic color direction (Pati-Salam):** Then the V_c ↔ V_s coherence is suppressed by B−L conservation — a naturally preserved quantum number at low energies. This is not an ad hoc filtration but a consequence of the B−L symmetry of the SM vacuum. The 6 coset generators change B−L (they mediate quark ↔ lepton transitions) and are therefore filtered by W_internal with μ related to B−L breaking.

**Verdict Branch B:**

W_internal is mathematically definable and not completely ad hoc IF V_s is physically identified as the leptonic color direction. The natural mechanism is B−L conservation / lepton number conservation filtering the color-singlet coset generators. This is structurally clean and has a known physical basis (B−L is an approximate symmetry of the SM). The two-stage filtration would be:

Stage 1 (W_decoh): metric-sign filter → kills non-compact, leaves su(4)⊕su(2)⊕u(1)
Stage 2 (W_internal): B−L filter → kills su(4)/su(3) coset, leaves su(3)⊕su(2)⊕u(1)

**This is plausible but requires explicitly identifying V_s with the leptonic color and deriving B−L conservation from the construction.**

---

### Branch C — Reinterpretation as Intermediate Stage

**The correct reading may be:**

```
UV:         su(4,2)              (35-dim, Hodge-sign-flipped)
          ↓ W_decoh (metric-sign filter)
Mid-scale: su(4) ⊕ su(2) ⊕ u(1) (19-dim, compact subalgebra)
          ↓ SU(4) → SU(3) breaking (Pati-Salam scale)
IR:         su(3) ⊕ su(2) ⊕ u(1) (12-dim, Standard Model)
```

**Comparison to known chains:**

| Chain | Stage 1 | Stage 2 | Stage 3 |
|---|---|---|---|
| SU(5) GUT | SU(5) full | SU(5)→SM Higgs | SM |
| SO(10) GUT | SO(10) full | SO(10)→SU(5)→SM | SM |
| **Pati-Salam** | **SU(4)×SU(2)_L×SU(2)_R** | **PS-scale Higgs → SM** | **SM** |
| **Current** | **su(4,2) via decoherence** | **su(4)⊕su(2)⊕u(1) intermediate** | **Need: su(4)→su(3)** |

The current construction's intermediate stage **su(4)⊕su(2)⊕u(1)** is not exactly Pati-Salam (which is SU(4)×SU(2)_L×SU(2)_R) because:
- Pati-Salam has an SU(2)_R factor; the current construction has only one SU(2) and a U(1)
- Pati-Salam's SU(4) acts on a 4-dimensional quark-lepton multiplet; the current V_c⊕V_s is a 4-dimensional color-singlet space

The structure is **closer to "SU(4)×SU(2)×U(1) as an intermediate unification stage"** — which resembles flipped SU(5)-type embeddings rather than standard Pati-Salam. But the key qualitative feature is the same: there is a known class of GUT models where SU(4) unification of color and a fourth degree of freedom (lepton number / B−L) appears as an intermediate stage.

**This reading makes the current result a partial success, not a failure.** The decoherence mechanism provides a novel derivation of the intermediate stage su(4)⊕su(2)⊕u(1). The further breaking to the SM is then handled by standard (and well-understood) model-building tools.

---

## Part 3 — Is There a Second Wobble / Internal Filtration Map W_internal?

**The recursion question:** Can the same logic that filtered su(4,2) → compact sector be applied again inside the compact sector to filter su(4) → su(3)?

**First stage:** The Hodge sign flip defines a metric on V = V_c ⊕ V_w ⊕ V_s. The metric asymmetry (V_w has opposite sign from V_c and V_s) is the physical input. W_decoh filters by metric-sign mixing — this is a natural structure from the algebra.

**Second stage candidate:** For W_internal to be recursive, there must be an analogous "asymmetry" within the +1 metric sector that distinguishes V_c from V_s.

**One natural candidate: dimensionality asymmetry.**

V_c = ℂ³ (3-dimensional), V_s = ℂ¹ (1-dimensional). The dimension ratio is 3:1. A generator mixing V_c and V_s has a "dimensional cost" — it mixes a 3-dimensional space with a 1-dimensional space, which is structurally asymmetric.

**Proposed W_internal via dimensional grading:**

Assign to each generator T a **dimensional mixing index** d(T):
- T within V_c: d = 0 (no dimensional crossing)
- T within V_s: d = 0
- T mixing V_c (dim=3) and V_s (dim=1): d = |dim(V_c) − dim(V_s)| = 2

Then: W_internal(T) = (γ/2)^{d(T)} · T

With d=2 for the 6 coset generators: W_internal suppresses them by (γ/2)^2.

**Is this natural?** Partially. The 3:1 dimension ratio between V_c and V_s is a real feature of the block decomposition. Whether it generates a physical decoherence effect requires identifying what physical process decoheres V_c ↔ V_s transitions with a (γ/2)² rate.

**The B−L interpretation provides a cleaner physical basis:**

If V_s is the leptonic color direction, then transitions V_c ↔ V_s change baryon minus lepton number: ΔB ≠ 0 or ΔL ≠ 0. In the SM vacuum, B−L is conserved (to very high precision). A decoherence process induced by the B−L-conserving vacuum would suppress V_c ↔ V_s transitions — but this is NOT a free parameter; it is a consequence of the specific physical identification of V_s.

**Verdict:** W_internal exists and is mathematically natural IF V_s is physically identified as the leptonic color direction. The recursion is:

W_decoh: filter by metric-sign asymmetry (Hodge) → su(4)⊕su(2)⊕u(1)
W_internal: filter by baryon/lepton number conservation (B−L) → su(3)⊕su(2)⊕u(1)

The second filter is a different kind of filtration (conservation law rather than metric-sign), so it is recursive in form (same grammar: "physical asymmetry filters generators") but not recursive in the sense of applying the same mathematical map a second time.

---

## Part 4 — Known Group Chain Comparison

| Breaking chain | Intermediate stage | IR | Similarity to current |
|---|---|---|---|
| SU(5) → SM | SU(5) = 24-dim | su(3)⊕su(2)⊕u(1) | SU(5) ≠ our 19-dim; closer to SU(5) if we include SU(2)_R |
| SO(10) → SU(5) → SM | SO(10)=45-dim, SU(5)=24-dim | su(3)⊕su(2)⊕u(1) | Larger UV; same terminal structure |
| **Pati-Salam** → SM | **SU(4)×SU(2)_L×SU(2)_R**, dim=15+3+3=21 | su(3)⊕su(2)⊕u(1) | **Closest: SU(4) acting on quark+lepton as 4-plet** |
| Current: su(4,2) → su(4)⊕su(2)⊕u(1) → SM | su(4)⊕su(2)⊕u(1), dim=19 | su(3)⊕su(2)⊕u(1) | Like Pati-Salam with SU(2)_R→U(1), via decoherence at UV |

**Key differences from Pati-Salam:**

1. In Pati-Salam, SU(2)_R is an explicit gauge factor that must be broken to U(1). In the current construction, only one SU(2) appears at the intermediate stage — the SU(2)_R is either absent or absorbed.

2. In Pati-Salam, the UV group is SU(4)×SU(2)_L×SU(2)_R (21-dimensional). In the current construction, the UV group is su(4,2) (35-dimensional non-compact). The current UV is strictly richer.

3. The decoherence mechanism at the UV stage is novel — Pati-Salam does not have a decoherence derivation of the intermediate stage from a larger non-compact algebra.

**The current construction is best understood as: a non-compact extension of a Pati-Salam-like intermediate stage, with the UV-to-PS transition explained by decoherence rather than by a Higgs at the SU(4,2) scale.**

---

## Part 5 — Final Classification

**Verdict:**

**Class 4: Decoherence gives a novel staged breaking chain worth pursuing.**

The reasoning:

1. The decoherence mechanism W_decoh gives a principled derivation of the intermediate stage su(4)⊕su(2)⊕u(1) from the 35-dimensional UV algebra su(4,2).

2. The intermediate stage su(4)⊕su(2)⊕u(1) is not a dead end — it is a recognizable intermediate unification stage of Pati-Salam type (SU(4) with color-lepton unification).

3. The su(4)→su(3) step can be resolved by either (A) standard Pati-Salam-scale Higgs (Branch A — clean, well-understood, reintroduces Higgs at PS scale), or (B) B−L conservation as a second decoherence filter W_internal (Branch B — physically motivated, avoids additional Higgs, requires identifying V_s as leptonic color).

4. The full chain:
```
su(4,2)   →[W_decoh: metric-sign]→   su(4)⊕su(2)⊕u(1)   →[W_internal: B−L or PS Higgs]→   su(3)⊕su(2)⊕u(1)
```
This is a coherent two-stage breaking chain with a novel mechanism at the first stage.

**What makes this worth pursuing versus just being standard PS:**

The UV algebra su(4,2) is the **conformal group of (3+1)D spacetime**. The fact that the Hodge sign flip selects the metric structure of Minkowski space (+,+,+,−,−,+) and that the resulting compact subalgebra looks like the Pati-Salam intermediate stage is physically intriguing. It suggests a connection between the gauge structure and the spacetime conformal symmetry at the GUT scale. This is not something standard Pati-Salam models derive.

---

## Summary

**What the 6 extra generators really are:** They are the SU(4)/SU(3) coset generators — the "leptonic color" bosons of a Pati-Salam-type unification where V_s plays the role of the 4th color (lepton number).

**Three resolutions:**

- **Branch A (standard):** Introduce a fundamental Higgs of SU(4) with VEV in V_s direction. This is exactly Pati-Salam breaking. Clean, standard, reintroduces one level of Higgs physics.

- **Branch B (novel):** Identify V_s as the leptonic color direction. Apply W_internal filtered by B−L conservation — the approximate symmetry of the SM vacuum naturally suppresses the color-singlet coset generators. Two-stage decoherence chain without additional Higgs at the PS scale.

- **Branch C (reframing):** Accept su(4)⊕su(2)⊕u(1) as the correct intermediate unification stage. The su(4,2) → su(4)⊕su(2)⊕u(1) derivation via decoherence is the novel content; the su(4)⊕su(2)⊕u(1) → SM step is handled by known methods.

**The most honest verdict:**

Branch C is correct as the framing. Branch A or B resolves the final step depending on how much Higgs physics you want to retain. The construction is not a dead end — it is a novel derivation of a Pati-Salam-like intermediate stage from a non-compact UV algebra via decoherence. **This is a genuine structural result, not complete, but not a failure.**
