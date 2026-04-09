# FINAL_NORMALIZATION_GAP_AUDIT
## Is the Last External Input Really Only Normalization?
*One question left: does V_s = leptonic color follow from the algebra, or does it import physics?*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — Separating What Is Algebraic from What Is Conventional from What Is Physical

The chain of reasoning currently is:

1. Q₄ is the unique Cartan satisfying conditions 1+2+3. **(Algebraic — proved.)**
2. Tracelessness forces the eigenvalue ratio on V_c:V_s = 1:−3. **(Algebraic — proved.)**
3. The commutant of Q₄ is the SM gauge algebra. **(Algebraic — proved.)**
4. The V_c charge is set to 1/3 (standard color normalization). **(Convention — from QCD.)**
5. Therefore V_s carries charge −1. **(Follows from 2+4.)**
6. Charge −1 = lepton number. **(Physical identification.)**
7. V_s = lepton sector = leptonic color. **(Physical identification + physical interpretation.)**

**The table:**

| Ingredient | Algebraic | Conventional | Physical |
|---|---|---|---|
| Q₄ uniqueness (conditions 1+2+3) | **Yes** | No | No |
| Eigenvalue ratio 1:−3 from tracelessness | **Yes** | No | No |
| Commutant = su(3)⊕su(2)⊕u(1) | **Yes** | No | No |
| Eigenvalue of Q₄ on V_c = +1/3 | No | **Yes** — choice of overall scale | No |
| Eigenvalue of Q₄ on V_s = −1 | No | **Yes** — follows from scale choice | No |
| Charge +1/3 = baryon number per quark | No | No | **Yes** — SM physics |
| Charge −1 = lepton number | No | No | **Yes** — SM physics |
| V_s = lepton sector | No | No | **Yes** — interpretation |

**Reading the table:** Rows 1–3 are exact. Rows 4–5 are conventional. Rows 6–8 are physical. The word "normalization" correctly describes steps 4–5. But the actual identification V_s = lepton (steps 6–8) is not normalization — it is a physical interpretation that imports B−L charge physics.

**The claim "just normalization" covers only steps 4–5. Steps 6–8 are additional physical content.** The normalization step and the physical identification step are distinct, and conflating them understates the remaining gap.

---

## Part 2 — Is the Normalization "1/(dim V_c)" Truly Forced Internally?

**The current claim:** Setting the charge per color direction to 1/dim(V_c) = 1/3 is natural because the 3 color directions are symmetric under SU(3).

**Stress test:**

Q₄ = i·diag(q, q, q, 0, 0, −3q) for any q ≠ 0.

The free parameter q is an overall scale of the Cartan generator. By convention, we can set q = 1 (which gives eigenvalue −3 on V_s), or q = 1/3 (which gives eigenvalue 1/3 on V_c and −1 on V_s), or q = anything.

**Is q = 1/3 forced internally?**

Test 1: Minimal charge quantum.

The minimal non-zero eigenvalue of Q₄ is |q|. Setting q = 1/3 gives minimum |q| = 1/3. But q = 1/7 or q = 1/π are equally valid minimal choices — "minimum" is not well-defined without fixing a unit. This does not force q = 1/3.

Test 2: Compatibility with su(3) generator normalization.

The standard su(3) Gell-Mann matrices are normalized as Tr(λ_a λ_b) = 2δ_{ab}. The SU(3) Cartan generators (λ₃ and λ₈) have eigenvalues of order 1 on quarks. But the normalization of these SU(3) generators does not constrain the overall scale of Q₄ — Q₄ is orthogonal to the SU(3) Cartans and its scale is a free parameter independent of the SU(3) normalization.

Test 3: Equal weight per basis direction in V_c.

This principle says: each direction in V_c should carry the same charge under Q₄. This is already guaranteed by the structure (Q₄ has equal eigenvalue q on all three V_c directions). It does NOT fix the value of q.

Test 4: Trace normalization of the fundamental.

For a representation where Q₄ acts, the trace Tr(Q₄) over the fundamental **6** of su(4,2) is:
Tr_{6}(Q₄) = 3q + 0 + 0 + (−3q) = 0.

This is already satisfied by construction (tracelessness) for any q. Does not fix q.

Test 5: Requiring that the commutant be SM and color directions remain symmetric.

The commutant of Q₄ is the SM for any nonzero q — the commutant depends only on which generators commute with Q₄ (i.e., which generators have zero commutator), and this is determined by the eigenvalue differences, not the overall scale. Scaling q does not change which generators commute with Q₄. So this test also does not fix q.

**Conclusion from stress tests:**

The normalization q = 1/3 is NOT forced by any internal principle of the su(4,2) algebra or its compact subalgebra. All five tests fail to determine q. The value 1/3 becomes natural only when it is matched to the known physics fact that quarks have baryon number 1/3.

**The "normalization = just a convention" claim is correct but incomplete.** The claim should be: "the normalization q is a free parameter, and choosing q = 1/3 is natural only given the physical identification of V_c directions as quarks with standard baryon number."

**This means step 4 is not just a harmless convention — it is a physical choice.** Setting q = 1/3 uses knowledge of QCD physics to fix the scale. This is more than a convention: it is an import of quark baryon-number physics into the algebra.

---

## Part 3 — Can the Normalization Be Derived from an Internal Principle?

**The question:** Is there any principle from within the su(4,2) structure that selects q = 1/3 without reference to external QCD physics?

**Candidate principle — minimal charge quantum under quark-lepton unification:**

If we require that the charges under Q₄ be rationally related to the charges under the SU(3) Cartan generators, and that the resulting charge lattice be the minimal one compatible with the SU(4) representation theory, then:

The fundamental **4** of SU(4) has Q₄ eigenvalues (+q, +q, +q, −3q). The SU(3) ⊂ SU(4) subalgebra assigns charges to the 3 + 1 decomposition. The **4** of SU(4) decomposes as **3** + **1** under SU(3). The minimal charge lattice compatible with this decomposition assigns Q₄ charges in ratio 1:1:1:−3 (as determined by tracelessness). The smallest rational number with this property is q = 1/3 (giving charges +1/3, +1/3, +1/3, −1, with the least common denominator being 3).

But: "smallest rational number" is not a mathematical principle — it is an aesthetic preference. The algebra does not rule out q = 2/3 or q = 7/3.

**Candidate principle — uniqueness of charge quantization:**

Charge quantization in quantum mechanics requires that all observable charges be integer multiples of some fundamental unit e. If the fundamental unit is 1 (for the electron charge), then quark charges ±1/3, ±2/3 are fractions. This is the standard charge quantization issue in particle physics, resolved in GUT models by the embedding into a compact group.

In the SU(4) framework: the charge lattice of Q₄ must be compatible with the charge lattice of the SM (where charges come in multiples of 1/3). This fixes q = 1/3 (or an integer multiple). But this requirement imports the SM charge lattice — which is the thing we are trying to derive.

**Verdict on Part 3:**

**Outcome C: The factor 1/3 is chosen to match known physics, not derived internally.**

No internal principle of su(4,2) or its compact subalgebra forces q = 1/3. The value is natural only in retrospect — given that we know quarks carry baryon number 1/3, we set the Q₄ normalization to match. This is circular in the strict sense: the normalization that makes V_s = lepton is chosen because we already know what the physical content should be.

**What CAN be derived internally:**

The eigenvalue ratio V_c:V_s = 1:−3 is algebraically forced. The statement "V_s carries charge with the opposite sign and magnitude 3 times the charge per V_c direction" is a theorem. The specific numbers 1/3 and −1 are normalization-dependent.

---

## Part 4 — What Is Really Derived: Leptonic Color, or Only a B-L-Shaped Singlet?

**The structural statement (proved):**

V_s is the unique 1-dimensional subspace in V = V_c ⊕ V_w ⊕ V_s such that the unique Cartan Q₄ (satisfying conditions 1+2+3) assigns to it a charge of opposite sign and 3 times the magnitude relative to each V_c direction.

This is the theorem. It says: V_s carries a "B-L-shaped" charge relative to V_c, in the ratio 1:−3.

**The physical statement (not proved):**

V_s is the lepton sector. The charge on V_s is the B−L quantum number of a lepton.

**Do they imply each other?**

The structural statement implies the physical statement **only given** that:
(a) V_c represents quarks (each carrying equal color, i.e., the three directions in V_c are the three quark colors)
(b) The B-L normalization assigns +1/3 to quarks (i.e., q = 1/3)
(c) A charge of −1 under Q₄ corresponds to lepton number −1 (i.e., the physical charge "lepton number" has this eigenvalue)

None of (a), (b), (c) are proved from the su(4,2) structure. They are physical inputs.

**The honest statement:**

The algebra derives a B-L-shaped singlet with eigenvalue ratio 1:−3. It does not derive "lepton number = −1 on V_s." Those are the same claim only after the physical identification of V_c as quark colors and the normalization of B-L charges.

**The terminology gap:** "B-L-shaped" is a structural/algebraic description. "Leptonic color" is a physical description. The algebra gives the former; the latter requires additional physics.

**What is actually derived:**

The staged corridor produces: a singlet direction V_s with a unique charge (B-L-shaped, ratio 1:−3) under a distinguished Cartan of su(4)⊕su(2)⊕u(1), such that the commutant of that Cartan is the SM gauge algebra. The physical identification of this charge as lepton number requires external input.

---

## Part 5 — Paradox Classifier on the Final Gap

**What kind of problem is the remaining gap?**

**Type II (missing invariant): Partially applies.**

The algebra has a B-L-shaped Cartan generator Q₄ (uniquely determined by conditions 1+2+3 and tracelessness). This IS an invariant of the algebraic structure. The physical identification of Q₄'s eigenvalues as baryon/lepton number requires a normalization choice and a physical interpretation. The "missing invariant" is not internal to the algebra — it is the link between the abstract Cartan eigenvalue ratio and the physical charge assignments of QCD+QED.

**Type I (missing view): Applies.**

The view we are missing is: a principle that *derives* why V_c should be identified as quarks and V_s as leptons from the algebraic structure alone. This would require showing that the decomposition V_c ⊕ V_w ⊕ V_s is not just one possible way to split ℂ⁶, but the only way consistent with some internal constraint of su(4,2). This view is currently absent.

**Type IV (observer/convention dependence): Applies to the normalization step.**

The choice q = 1/3 is observer-convention-dependent: it is the convention that makes the numbers match known QCD physics. A physicist who did not know about quarks would not know to choose q = 1/3. The convention imports the observer's knowledge of QCD.

**Summary:**

The remaining gap has three components:
1. Type II: A B-L-shaped invariant exists in the algebra (proved), but the identification of its eigenvalues with physical B-L charges requires a normalization convention.
2. Type I: The physical interpretation of V_c = quarks and V_s = leptons is a missing view — it requires the physical identification of ℂ³ as "three quark colors" and ℂ¹ as "lepton."
3. Type IV: The normalization q = 1/3 is convention-dependent and requires matching to known QCD physics.

---

## Part 6 — The Strongest Honest Theorem

**Theorem (proved — exact parts italicized):**

*Let η = diag(+1,+1,+1,−1,−1,+1) and let su(4,2) be the corresponding Lie algebra.*

*(Step 1 — exact): The maximal compact subalgebra of su(4,2) is su(4) ⊕ su(2) ⊕ u(1).*

*(Step 2 — exact): The unique Cartan generator Q₄ of su(4)⊕su(2)⊕u(1) satisfying (i) [Q₄, su(3)] = 0, (ii) [Q₄, su(2)] = 0, and (iii) Q₄ assigns different eigenvalues to V_c and V_s has eigenvalue ratio q_c:q_s = 1:−3, where q_c is fixed by tracelessness and dim(V_c) = 3.*

*(Step 3 — exact): The commutant of Q₄ in su(4)⊕su(2)⊕u(1) is su(3)⊕su(2)⊕u(1).*

*Step 4 (conventional): Setting q_c = 1/3 (normalizing so that the total Q₄ charge per fundamental V_c direction is 1/3) gives q_s = −1.*

*Step 5 (physical interpretation): Under the identification V_c = three quark colors and the convention that Q₄ represents the B-L charge with normalization q_c = 1/3 per quark direction, the charge q_s = −1 corresponds to lepton number −1 per lepton (B-L charge of V_s = −1 = "leptonic").*

**What is exact:** Steps 1, 2, 3.

**What is convention-fixed:** Step 4 — the normalization q_c = 1/3. This is the standard color normalization, not forced algebraically.

**What is physically interpreted:** Step 5 — the identification of V_c with quark colors, V_s with the lepton direction, and Q₄ with the B-L charge. These require physical content beyond the algebra.

---

## Final Verdict

**The staged path is: forced up to normalization AND physical interpretation.**

**Not "fully forced":** The physical content V_s = lepton sector requires the identification of V_c as quark colors and the interpretation of Q₄ as B-L charge. These are physical inputs not derivable from su(4,2) alone.

**Not "structurally preferred but still interpretive":** The Q₄ generator is uniquely algebraically distinguished (conditions 1+2+3, tracelessness). The "B-L-shaped structure" is a theorem, not an interpretation. The physical identification of this structure with actual B-L physics is the interpretive step.

**The correct characterization: "Forced up to normalization, with one remaining physical interpretation step."**

The algebra gives: a B-L-shaped singlet direction with eigenvalue ratio 1:−3. This is a structural fact. The identification of "B-L-shaped" with "actual lepton number" requires:
1. Knowing that quarks carry baryon number +1/3 (from QCD)
2. Knowing that leptons carry lepton number −1 (from SM physics)

These two facts are not derivable from su(4,2). They are external physics inputs.

**The one genuinely external physics input (honestly stated):**

The construction derives a Cartan generator Q₄ with eigenvalue ratio 1:−3 between V_c and V_s. Calling this "B-L charge" requires knowing that in the physical world, the 3 quark colors each carry B-L = +1/3 and leptons carry B-L = −1. This fact about the physical world — the specific quantum number assignments of SM particles — is what the algebra cannot derive.

**The construction derives the structure. The physical content of that structure still imports SM physics.**

This is not a fatal flaw — all GUT constructions import some SM physics as input (usually the representations of matter under the SM gauge group). The current construction has reduced the external physics input to: "quarks carry B-L = +1/3 and leptons carry B-L = −1," which is a remarkably minimal set of physical assumptions for a GUT derivation. But it is not zero.

**Classification: Forced up to normalization + one specific physical quantum-number input.**
