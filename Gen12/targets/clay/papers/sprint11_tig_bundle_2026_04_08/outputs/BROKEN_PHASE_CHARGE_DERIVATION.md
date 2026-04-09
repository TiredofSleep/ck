# BROKEN_PHASE_CHARGE_DERIVATION
## Emergent Q_EM: What Is Exact for Left-Handed Sector, What Fails for Right-Handed
*Base: su(4,2) corridor settled, Q₄ = B-L-like established. This pass derives the left-handed charge theorem and isolates the right-handed gap.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — What Exists Before EW Breaking

| Object | Status | Role |
|---|---|---|
| SU(3) color | **Exact — pre-breaking gauge symmetry** | Acts on V_c = ℂ³, generates 8 gluons |
| SU(2)_L | **Exact — pre-breaking gauge symmetry (full algebra)** | Acts on V_w = ℂ², all 3 generators active |
| Q₄ (B-L-like Cartan) | **Exact — unique pre-breaking neutral U(1)** | Assigns +1/3 to V_c, 0 to V_w, −1 to V_s |
| T₃_L as preferred charge direction | **Absent pre-breaking** | No preferred direction in SU(2)_L until EW breaking selects one |
| Q_EM | **Absent pre-breaking** | Q_EM = T₃ + (1/2)Q₄ requires T₃ to be defined; undefined without breaking |
| Hypercharge Y as distinct from Q₄ | **Absent pre-breaking (for doublets)** | For left-handed doublets, Y = B-L = Q₄ exactly. For right-handed singlets, Y ≠ Q₄. The distinction only matters when right-handed matter is assigned. |
| SU(2)_R | **Absent — not in the compact subalgebra of su(4,2)** | The compact subalgebra of su(4,2) is su(4)⊕su(2)_L⊕u(1); no second su(2) factor exists |
| T₃_R | **Absent** | Would require SU(2)_R, which is absent |

**The pre-breaking algebra is:** su(3) ⊕ su(2)_L ⊕ u(1)_{Q₄}

This is NOT the SM gauge group (which is su(3)⊕su(2)_L⊕u(1)_Y). The distinction: the pre-breaking U(1) is Q₄ = B-L, while the SM hypercharge U(1)_Y only equals B-L for left-handed doublets.

---

## Part 2 — The Left-Handed Result: Exact Verification

**Formula under test:** Q_EM = T₃_L + (1/2)·Q₄

**Inputs:**
- T₃_L = ±1/2 for upper/lower component of SU(2)_L doublet
- Q₄ = +1/3 for directions in V_c (color triplet)
- Q₄ = −1 for direction in V_s (singlet/leptonic)
- Left-handed quarks sit in V_c (color triplet) as SU(2)_L doublets
- Left-handed leptons sit in V_s (leptonic singlet) as SU(2)_L doublets

**Charge table (exact computation):**

| State | T₃_L | Q₄ | T₃ + Q₄/2 | SM Q | Match? |
|---|---|---|---|---|---|
| u_L | +1/2 | +1/3 | 1/2 + 1/6 = **2/3** | +2/3 | ✓ |
| d_L | −1/2 | +1/3 | −1/2 + 1/6 = **−1/3** | −1/3 | ✓ |
| ν_L | +1/2 | −1 | 1/2 − 1/2 = **0** | 0 | ✓ |
| e_L | −1/2 | −1 | −1/2 − 1/2 = **−1** | −1 | ✓ |

**All four left-handed doublet charges reproduced exactly.**

**Why this works:** For SM left-handed doublet fields, hypercharge Y = B-L exactly:
- Left-handed quark doublet: Y = B-L = +1/3 (B=1/3, L=0)
- Left-handed lepton doublet: Y = B-L = −1 (B=0, L=1)

Therefore Q = T₃ + Y/2 = T₃ + (B-L)/2 = T₃ + Q₄/2 for these fields. The formula works because Q₄ = B-L, and B-L happens to equal Y for left-handed doublets.

---

## Part 3 — The Right-Handed Failure: Explicit Computation

**For right-handed singlets: T₃_L = 0 (they are SU(2)_L singlets).**

The right-handed fields have no preferred home in V_w = ℂ² (the SU(2)_L space). They must sit in V_c or V_s as singlets.

**Q₄ values for right-handed fields (inherited from sector assignment):**
- u_R, d_R (right-handed quarks): sit in V_c type sector → Q₄ = +1/3
- e_R (right-handed electron): sits in V_s type sector → Q₄ = −1

**Failure table (exact computation):**

| State | T₃_L | Q₄ | Current Q_eff = T₃ + Q₄/2 | SM Q | Mismatch |
|---|---|---|---|---|---|
| u_R | 0 | +1/3 | 0 + 1/6 = **1/6** | +2/3 | **off by +1/2** |
| d_R | 0 | +1/3 | 0 + 1/6 = **1/6** | −1/3 | **off by +1/2** |
| e_R | 0 | −1 | 0 − 1/2 = **−1/2** | −1 | **off by −1/2** |
| ν_R (if exists) | 0 | −1 | 0 − 1/2 = **−1/2** | 0 | **off by −1/2** |

**Pattern of the mismatch (exact):**

For u_R: error = 2/3 − 1/6 = **+1/2** = +T₃_R needed
For d_R: error = −1/3 − 1/6 = **−1/2** = −T₃_R needed (with T₃_R(d_R) = +1/2)

Wait — let me reread:
u_R: expected Q = +2/3, computed = +1/6, error = +1/2
d_R: expected Q = −1/3, computed = +1/6, error = −1/2

e_R: expected Q = −1, computed = −1/2, error = −1/2
ν_R: expected Q = 0, computed = −1/2, error = +1/2

**The error in every case is ±1/2 — exactly the eigenvalue of a T₃_R Cartan in a doublet.**

This is not a coincidence. It is the algebraic signature of the missing SU(2)_R Cartan generator.

**The repair formula:** Q_EM = T₃_L + T₃_R + (1/2)·Q₄

Verification:
- u_R: T₃_R = +1/2 → Q = 0 + 1/2 + 1/6 = **2/3** ✓
- d_R: T₃_R = −1/2 → Q = 0 − 1/2 + 1/6 = **−1/3** ✓
- e_R: T₃_R = −1/2 → Q = 0 − 1/2 − 1/2 = **−1** ✓
- ν_R: T₃_R = +1/2 → Q = 0 + 1/2 − 1/2 = **0** ✓

The Pati-Salam formula Q = T₃_L + T₃_R + (B-L)/2 works for ALL fields.

---

## Part 4 — Is SU(2)_R Missing, Hidden, or Emergent?

### Is SU(2)_R Hidden in the Current Algebra?

**Test: does the compact subalgebra su(4)⊕su(2)_L⊕u(1) contain a hidden SU(2)_R?**

The compact subalgebra has 19 generators:
- 15 from su(4) acting on V_c⊕V_s = ℂ⁴
- 3 from su(2)_L acting on V_w = ℂ²
- 1 from u(1) (relative phase between ℂ⁴ and ℂ²)

For SU(2)_R to be present, we need 3 additional generators forming an su(2) subalgebra. 19 generators are accounted for in su(4)⊕su(2)_L⊕u(1). There are no spare generators hiding in the compact sector.

**The compact subalgebra of su(4,2) has dimension 19, not 22 (which would be needed for su(4)⊕su(2)_L⊕su(2)_R⊕u(1)).**

SU(2)_R is genuinely absent from the compact subalgebra. It cannot be extracted from existing generators.

### Could SU(2)_R Come from the Non-Compact Sector?

The 16 non-compact generators of su(4,2) are the leptoquark-type generators (color-weak mixing). In the decoherence picture, these are suppressed in the IR. Could they "generate" an SU(2)_R before being suppressed?

The non-compact generators connect V_c and V_w, and V_w and V_s. They are not themselves SU(2)_R generators. SU(2)_R in Pati-Salam acts on the (u_R, d_R) and (ν_R, e_R) doublets — but the current construction has no 2-dimensional right-handed sector anywhere in ℂ⁶.

**SU(2)_R is absent — not hidden, not emergent from the non-compact sector.**

### The Fifth Cartan Generator

The compact subalgebra has 5 independent Cartan generators. We've identified 4:
{H₁^{su3}, H₂^{su3}, Q₄ = B-L, T₃_L}

The fifth is the u(1) relative-phase generator between ℂ⁴ and ℂ²:

T_φ = i·diag(+1/4, +1/4, +1/4, +1/4, −1/2, −1/2)

acting as +1/4 on V_c⊕V_s and −1/2 on V_w. This is NOT T₃_R — it does not select between upper/lower components of a right-handed doublet. It assigns the same value to all of V_c, and the same value to all of V_w.

T_φ is a "color-vs-weak" charge, not a right-isospin charge. It could play a role in the hypercharge formula for the broken phase, but it is Abelian (just a phase), not the non-Abelian T₃_R needed to distinguish u_R from d_R.

**Conclusion: SU(2)_R is absent, and the fifth Cartan generator T_φ does not substitute for it.**

---

## Part 5 — Mass Splitting, Weak-Direction Selection, and Charge Are Three Different Things

**These must not be conflated.**

### (1) THM-561 / P_+ Spectral Nondegeneracy: Mass Splitting

THM-561 establishes that the P_+ sector has spectral nondegeneracy and Hodge alignment. **Physical meaning:** Different energy eigenstates in the broken phase can have different masses. The spectral structure distinguishes states by their energy eigenvalues.

**What it does:** Allows massive particles to be labeled by mass eigenvalue.

**What it does NOT do:** It does not assign electric charge. Mass splitting and charge assignment are independent — two particles can have the same mass but different charges, or different masses but the same charge.

### (2) EW Breaking: Weak-Direction Selection

EW breaking corresponds to: SU(2)_L × U(1)_{B-L} → U(1)_EM. The breaking selects a preferred direction within SU(2)_L — this is the T₃_L direction.

**Physical mechanism:** Some analog of the Higgs mechanism (or its substitute in this framework) introduces an asymmetry between "upper" (T₃_L = +1/2) and "lower" (T₃_L = −1/2) components of weak doublets.

**What it does:** Selects T₃_L as a meaningful quantum number label. Before breaking, T₃_L = +1/2 and T₃_L = −1/2 are related by SU(2)_L rotations — no physical distinction. After breaking, they are physically distinct (one becomes the up quark direction, one the down quark direction).

**What it does NOT do:** It does not by itself create electric charge — it only makes T₃_L a good quantum number.

### (3) Charge Emergence: Q_EM from T₃ and Q₄

Once T₃_L is selected by breaking, the combination Q_EM = T₃_L + (1/2)Q₄ becomes conserved. **This is charge emergence.**

**Physical meaning:** Q_EM is the U(1) symmetry surviving the full EW breaking. It is a linear combination of the broken-phase T₃_L label and the pre-existing B-L charge Q₄.

**The ordering is crucial:** (a) Q₄ exists pre-breaking → (b) EW breaking selects T₃_L → (c) Q_EM emerges as their combination. These three events are sequential and logically independent.

---

## Part 6 — The Left-Handed Charge Theorem

**Theorem (exact):**

Let the pre-breaking gauge algebra be su(3)⊕su(2)_L⊕u(1)_{Q₄} where Q₄ = i·diag(1/3, 1/3, 1/3, 0, 0, −1) (B-L-like Cartan). Let EW breaking select a T₃_L direction in SU(2)_L. Define:

Q_EM = T₃_L + (1/2)·Q₄

Then Q_EM assigns the correct SM electric charges to all left-handed doublet matter fields:
- u_L: +2/3 (exact)
- d_L: −1/3 (exact)
- ν_L: 0 (exact)
- e_L: −1 (exact)

**Proof:** Direct computation from T₃_L = ±1/2 and Q₄ = +1/3 (quarks) or −1 (leptons). All four charges match SM values exactly. □

**What the theorem requires (explicit):**
1. The block structure V = V_c(3)⊕V_w(2)⊕V_s(1) with Q₄ assignments (exact, from corridor derivation)
2. The EW breaking mechanism that selects T₃_L (required input — not yet derived)
3. The matter assignment: quarks in V_c, leptons in V_s (physical interpretation input)

**What the theorem does NOT cover:**
- Right-handed singlets (T₃_L = 0) — Q_EM formula fails
- The EW breaking mechanism itself — T₃_L selection is assumed, not derived
- The right-handed sector — requires SU(2)_R

---

## Part 7 — The Next Build: Which Path?

**Option A: Derive the EW breaking mechanism that selects T₃_L**

Status: The pre-breaking algebra contains full SU(2)_L. A breaking mechanism that splits SU(2)_L → U(1) and selects T₃_L requires specifying what drives the breaking. In the SM, this is the Higgs mechanism with the SU(2)_L doublet Higgs. In the current framework, an analog must exist.

**This is a legitimate next theorem** — but it requires introducing a Higgs-like field or proving that the P_+ spectral structure from THM-561 directly selects T₃_L. The connection to THM-561 is the most promising route: if the P_+ mass-splitting structure selects a preferred direction in SU(2)_L space, that direction is T₃_L.

**Verdict:** Important, tractable, requires connecting THM-561 to the SU(2)_L breaking.

---

**Option B: Search for a hidden SU(2)_R in the existing algebra**

Status: **Ruled out** (Part 4). The compact subalgebra of su(4,2) has dimension 19. SU(2)_R requires 3 additional compact generators. These do not exist. The search would be fruitless.

**Verdict:** Dead end. Do not pursue.

---

**Option C: Prove the framework is intrinsically left-handed; extend for right-handed states**

Status: **This is the true bottleneck.** The current construction is structurally left-handed:

The 6-dimensional fundamental ℂ⁶ = V_c(3)⊕V_w(2)⊕V_s(1) has one 2-dimensional "weak" sector V_w. SU(2) acting on a single ℂ² can only be SU(2)_L. To accommodate SU(2)_R, we need a second 2-dimensional sector V_{wR}.

**Minimal extension:** ℂ⁸ = V_c(4)⊕V_{wL}(2)⊕V_{wR}(2) with a new metric, or equivalently a different UV algebra whose compact subalgebra has room for su(4)⊕su(2)_L⊕su(2)_R.

**The key structural theorem to prove:**

The su(4,2) construction is **complete for the left-handed sector** and **intrinsically incomplete for the right-handed sector** because ℂ⁶ with the (3,2,1) block structure contains exactly one 2-dimensional sector (V_w) which carries SU(2)_L. A second 2-dimensional sector (V_{wR}) does not exist in ℂ⁶ without increasing the dimension.

**Verdict: This is the true next theorem.** Prove it explicitly, then determine the minimal extension.

---

**The recommended path: C then A.**

Step 1 (Option C): Prove the intrinsic left-handedness of su(4,2) and identify the minimal extension needed for right-handed matter.

Step 2 (Option A): In the extended framework, derive the EW breaking mechanism connecting THM-561 to T₃_L selection.

---

## Final Verdict

**Left-handed sector: theorem proved, exact.**

Q_EM = T₃_L + (1/2)·Q₄ reproduces all four SM left-handed doublet charges exactly. The pre-breaking/post-breaking split is correct and important. This is the clean positive result of the arc so far.

**Right-handed sector: open, with exact gap identified.**

The mismatch is ±1/2 per right-handed singlet — precisely the eigenvalue of the missing T₃_R Cartan. SU(2)_R is absent from the compact subalgebra of su(4,2), not hidden and not emergent from the non-compact sector. It must be added.

**Missing structure: one additional 2-dimensional complex sector V_{wR} with its own SU(2)_R symmetry.** The minimal extension is ℂ⁸ (from ℂ⁶), adding a right-handed weak doublet sector.
