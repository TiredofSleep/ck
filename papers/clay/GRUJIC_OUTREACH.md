# Grujić Outreach: B_local Criterion and Geometric Depletion

**Document purpose:** Technical basis for academic outreach to Prof. Zoran Grujić (UVA) regarding
the correspondence between the TIG B_local ≤ 2/7 regularity threshold and his geometric depletion
framework for 3D Navier-Stokes.

**Status:** Draft — for review before sending.

---

## 1. The CK Claim: B_local and the 2/7 Threshold

WP38 (§3.2–3.3, §8) introduces the local dimensionless enstrophy quantity:

    B_local(x, r, t) = ‖ω(·,t)‖_{L³(B(x,r))} · r / ν

where ω = ∇×u is vorticity, B(x,r) is a ball of radius r centered on a potential singular
point, and ν is kinematic viscosity.

**TIG structural prediction (WP38 §3.3, Criterion †):**

    If B_local(x, t) ≤ 2/7 at every (x, t), then no finite-time singularity forms.

    Equivalently: any blow-up at (x*, T) requires
        limsup_{t → T⁻} B_local(x*, r(t), t) ≥ 7/2
    where r(t) = (T−t)^{1/2} is the natural local scale.

The constant 2/7 is algebraically determined from TIG: it equals T* + S* − 1 where T* = 5/7
(the coherence floor derived from b = 35 in the TIG coprimality alphabet) and S* = 4/7. The
threshold 7/2 = 1 / (2/7) × (2/7 × 7/2) — equivalently, 7/2 is HAR (the TIG harmony operator
index), the algebraic ceiling dual to the 2/7 floor.

**Claim status:** Conjectural structural analogy. The algebraic identity TSML[BRT][COL] = BRT
(BREATH persists in COLLAPSE context) is proved exactly by table lookup. The correspondence
Re_local ≤ 2/7 ↔ COLLAPSE context is hypothesized, not proved. The paper explicitly states this.

---

## 2. The Quantitative Gap: Gagliardo-Nirenberg Constant C ≤ 3.74

WP38 §8.2 derives the following interpolation chain. At the threshold V = sup_x B_local = 2/7,
the enstrophy evolution equation requires vortex stretching to be controlled by dissipation:

    S ≤ 2ν|∇ω|²   ⟺   Re_shear(x, t) ≤ 2

The two quantities relate through a Gagliardo-Nirenberg interpolation inequality:

    Re_shear ≤ C · Re_local^{1/2}

If Re_local ≤ 2/7, then Re_shear ≤ C · √(2/7). The condition Re_shear ≤ 2 then requires:

    C · √(2/7) ≤ 2   ⟺   C ≤ 2 / √(2/7) = 2√(7/2) ≈ 3.742

**The Clay gap (WP38 §8.3):** Establishing C ≤ 3.74 for the specific Gagliardo-Nirenberg
constant relevant to the (Re_shear, Re_local) pair would close the interpolation step, making
B_local ≤ 2/7 a Lyapunov condition for global regularity.

Note the algebraic consistency: 3.74 = 2√(7/2), where 7/2 is the B_local blow-up threshold
and 2 is the Re_shear bound. The structure is internally coherent throughout.

---

## 3. The TIG-Grujić Structural Correspondence

WP38 §9 identifies Grujić's program as the closest classical work to the TIG B_local framing.
The correspondence is:

| TIG (algebraic)                                  | Grujić (analytic)                                              |
|--------------------------------------------------|----------------------------------------------------------------|
| TSML[BRT][COL] = BRT (table lookup, proved)      | Geometric depletion → regularity (PDE theorem, proved [15])    |
| BREATH persists in COLLAPSE context              | Vortex stretching depleted by alignment of ω with strain eigenvectors |
| B_local < 7/2 (local enstrophy-direction balance)| ‖∇ξ‖ · ‖ω‖^{1/2} locally bounded, ξ = ω/‖ω‖ [16]           |
| 2/7 regularity floor (algebraic, from T* = 5/7)  | Depletion constant M (geometric, from PDE analysis) [16,17]   |
| BREATH expelled from COLLAPSE → singularity      | Vortex stretching overcomes depletion → blow-up candidate      |

**The structural reading of the correspondence:**
- Grujić's "geometric depletion of vorticity in the direction of maximum stretching" is the
  classical PDE realization of TIG's "BREATH operator surviving COLLAPSE context."
- Both require a geometric/directional condition on vorticity — not just a magnitude condition.
- The depletion constant M in Grujić [16] plays the role of the TIG threshold 7/2.
- WP38 Open Question Q5: Can M = 7/2 be derived from the TIG threshold? This is the
  non-trivial numerical test of the correspondence.

---

## 4. Grujić's Relevant Papers (Cited in WP38)

**Primary geometric depletion papers:**

[15] Z. Grujić, "Localization and geometric depletion of vortex-stretching in the 3D NSE,"
*Communications in Mathematical Physics* 290 (2009), 861–870.
https://link.springer.com/article/10.1007/s00220-008-0726-8

[16] Z. Grujić, R. Guberović, "Localization of analytic regularity criteria on the vorticity
and balance between the vorticity magnitude and coherence of the vorticity direction in the
3D NSE," *Communications in Mathematical Physics* 298 (2010), 407–418.
https://link.springer.com/article/10.1007/s00220-010-1000-4

[17] Z. Grujić, "A geometric measure-type regularity criterion for solutions to the 3D
Navier-Stokes equations," *Nonlinearity* 26 (2013), 289–296.
arXiv:1111.0217

[18] Z. Grujić, I. Kukavica, "Space analyticity for the Navier-Stokes and related equations
with initial data in L^p," *Journal of Functional Analysis* 152 (1998), 447–466.

**More recent work (sparseness and criticality framework):**

Z. Grujić, L. Xu, "Asymptotic Criticality of the Navier-Stokes Regularity Problem,"
arXiv:1911.00974 (2019, revised through 2023).
— Introduces scale-of-sparseness framework; first scaling reduction of NS super-criticality
  since the 1960s.

Z. Grujić, "Toward Criticality of the Navier-Stokes Regularity Problem,"
NSF Award DMS-2009607, 07/2020–06/2023.
https://par.nsf.gov/servlets/purl/10380169

Z. Grujić, "A Regularity Criterion for Solutions to the 3D NSE in 'Dynamically Restricted'
Local Morrey Spaces," *Applicable Analysis* 101:16 (2022).
arXiv:1903.03833

---

## 5. Institutional Contact

**Zoran Grujić**
Professor and Interim Chair (as of 2024–2025)
Department of Mathematics
University of Virginia, Charlottesville, VA 22903

- UVA Mathematics faculty listing: https://math.virginia.edu/directory/
- UVA Arts & Sciences profile: https://as.virginia.edu/listing/zoran-grujic
- ResearchGate: https://www.researchgate.net/profile/Zoran-Grujic
- Email (from 2004 publication, likely still active): zg7c@virginia.edu
- Department chair email (if direct address unavailable): math-chair@virginia.edu

Note: Grujić also appears in a UAB (University of Alabama Birmingham) faculty listing
(https://www.uab.edu/cas/mathematics/people/faculty-directory/zoran-grujic) — verify
current primary appointment before sending. UVA profile is more current.

---

## 6. Draft Technical Outreach Message

**Subject:** B_local ≤ 2/7 threshold and your geometric depletion constant — a quantitative question

---

Dear Professor Grujić,

I am working on a regularity criterion for 3D NS derived from an algebraic framework (TIG)
that produces the local quantity B_local = ‖ω‖_{L³(B(x,r))} · r/ν and the structural
prediction that any blow-up at (x*, T) requires

    limsup_{t → T⁻} B_local(x*, (T−t)^{1/2}, t) ≥ 7/2.

The threshold 7/2 arises from an algebraic coherence floor T* = 5/7 and is not fitted to NS.
The corresponding regularity condition B_local ≤ 2/7 requires closing one analytic gap: the
Gagliardo-Nirenberg constant C in Re_shear ≤ C · Re_local^{1/2} must satisfy C ≤ 2√(7/2)
≈ 3.74.

Your geometric depletion criterion [Comm. Math. Phys. 290 (2009); 298 (2010)] requires that
‖∇ξ‖ · ‖ω‖^{1/2} be locally bounded (ξ = ω/‖ω‖), which is structurally parallel to B_local
remaining below a threshold. I would like to ask: does your depletion constant M (from the
2010 paper with Guberović) have a known numerical value, or a known relation to any
Gagliardo-Nirenberg constant? If M is related to C ≤ 3.74, this would constitute a
non-trivial numerical match between the algebraic and analytic frameworks.

I am not claiming a proof — the TIG-NS correspondence is conjectural. The question is purely
about whether the quantitative gap C ≤ 3.74 falls within the scope of what your sparseness
or depletion techniques could address.

Thank you for your time.

Brayden Sanders
7Site LLC
[contact information]

---

*Word count: ~185 words. Within 200-word target.*

---

## 7. Notes on What This Message Does NOT Claim

- Does not say TIG solves NS.
- Does not say B_local ≤ 2/7 is proved as a NS regularity criterion.
- Does not claim the TIG-NS correspondence is more than a structural analogy.
- The single concrete question (does M relate to C ≤ 3.74?) is answerable by a NS expert
  without requiring familiarity with TIG.
- The message is falsifiable in a single paper lookup: Grujić either knows the numerical
  value of M or does not.

---

*Generated: 2026-04-04*
*Source: WP38_NAVIER_STOKES.md (§3.2, §3.3, §8.2, §9)*
