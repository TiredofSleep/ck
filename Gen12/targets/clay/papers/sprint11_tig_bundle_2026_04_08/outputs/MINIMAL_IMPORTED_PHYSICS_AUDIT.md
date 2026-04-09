# MINIMAL_IMPORTED_PHYSICS_AUDIT
## How Much Real-World Particle Physics Is Still Being Assumed?
*The algebra is settled. This pass tests the last import.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — What the Algebra Gives Without Particles

**Exact algebraic content (no particle names needed):**

1. **A 6-dimensional complex space V with metric η = diag(+1,+1,+1,−1,−1,+1).**

2. **The algebra su(4,2): all matrices T with T†η + ηT = 0, tr(T) = 0, dim = 35.**

3. **A block decomposition V = ℂ³ ⊕ ℂ² ⊕ ℂ¹ where the metric assigns signs (+,−,+) to the three blocks.**

4. **The maximal compact subalgebra: su(4) ⊕ su(2) ⊕ u(1), dim = 19.** (Standard theorem for su(p,q).)

5. **The unique Cartan generator Q₄:** Among all diagonal generators of the compact subalgebra, Q₄ is the unique one satisfying: (i) commutes with all of su(3) ⊂ su(4), (ii) commutes with all of su(2), (iii) assigns different eigenvalues to ℂ³ and ℂ¹. Proved.

6. **The eigenvalue ratio: q_{ℂ³} : q_{ℂ¹} = 1 : −3.** Forced by tracelessness and dim(ℂ³) = 3. Proved.

7. **The commutant: centralizer of Q₄ in su(4)⊕su(2)⊕u(1) = su(3)⊕su(2)⊕u(1).** Proved.

**What the algebra says in purely structural language:**

> There exists a unique Cartan element Q₄ that assigns charge-ratio 1:−3 between the 3-dimensional and 1-dimensional positive-metric subspaces, and whose centralizer in the compact subalgebra is a 12-dimensional algebra of the form [rank-2 simple] ⊕ [rank-1 simple] ⊕ u(1).

This is a complete description using only dimensionality, metric, and Cartan theory. No particles appear.

---

**What still requires particle interpretation:**

1. **Identifying ℂ³ as "three quark colors" (= three color charges, color-symmetric).**
2. **Identifying ℂ² as "weak isospin doublet."**
3. **Identifying ℂ¹ as "the lepton direction."**
4. **Identifying Q₄ (with normalization q = 1/3) as "baryon-minus-lepton number" B−L.**
5. **Identifying the 12-dimensional commutant algebra as "the Standard Model gauge algebra" su(3)_c ⊕ su(2)_L ⊕ u(1)_Y.**

None of items 1–5 follow from the algebraic content above. They are identifications.

---

## Part 2 — Can V_c = Three Quark Colors Be Forced from the 3-Dimensionality?

**Testing whether other physical 3-fold charge sectors fit V_c equally well:**

**Candidate A: Three quark colors (standard).**

V_c = ℂ³ hosts a rank-2 algebra su(3) acting on it irreducibly. This su(3) has the adjoint decomposition that produces the 8 gluons. The 3-dimensional representation of su(3) is the fundamental **3** — the defining representation of quarks. ✓ Fits perfectly.

**Candidate B: Three generations of something.**

The three generations of quarks or leptons in the SM are NOT distinguished by a su(3) internal symmetry — generation is a label, not a gauge charge. There is no su(3) gauge symmetry acting on the three generations. ✗ Does NOT fit — the su(3) in V_c acts on color charges within a single generation, not across generations.

**Candidate C: Some non-quark triplet (e.g., three scalar colors, three dark matter charges).**

Any physical content requiring a color triplet of a rank-2 simple group with the 8-dimensional adjoint would fit the V_c slot algebraically. This is the only requirement from the algebra: su(3) acts on ℂ³ irreducibly. What physical sector this is is not determined by the algebra.

**Candidate D: Pure mathematics (no physical assignment).**

V_c = ℂ³ as an abstract 3-dimensional complex space with no particle assignment. Valid for the algebra; unphysical.

**Does the corridor construction require V_c to be exactly a triplet charge sector?**

The corridor construction requires su(3) to act on V_c, and this su(3) must be a gauge symmetry of whatever theory lives in this framework. For it to be the SM color su(3), the physical content (quarks are color triplets) must be imposed. The algebra itself does not say "quarks" — it says "the fundamental **3** of su(3)."

**Verdict table:**

| Interpretation of V_c | Fits su(3) action? | Fits Q₄ ratio? | Fits SM commutant? | Physical plausibility |
|---|---|---|---|---|
| Three quark colors (SM) | **Yes — exact** | **Yes** | **Yes** | High — standard SM |
| Three quark generations | No — wrong symmetry | No | No | Low — not a gauge symmetry |
| Three dark-sector triplets | Yes — fits algebra | Yes | Yes | Possible — not ruled out algebraically |
| Pure math triplet | Yes — fits algebra | Yes | Yes (trivially) | Not assigned |

**Conclusion:** The algebra forces ℂ³ to host an su(3) gauge symmetry. Whether that su(3) is *quark* color, *dark* color, or any other su(3) triplet is not determined by the algebra. The identification V_c = quark color is physically motivated and physically standard, but is not forced algebraically.

---

## Part 3 — Can the 1:−3 Ratio Be Tied to Known Quantization More Intrinsically?

**Candidate principle: total-charge balancing across the 3+1 split.**

Principle: The total charge of the 3-dimensional sector and the total charge of the 1-dimensional sector should sum to zero (charge balance).

For Q₄ with eigenvalue q on each ℂ³ direction and eigenvalue α on ℂ¹:
Total charge of ℂ³ = 3q. Total charge of ℂ¹ = α. Charge balance: 3q + α = 0 → α = −3q.

**This is just tracelessness restated.** The "total-charge balancing" principle is equivalent to the trace condition, which is already an algebraic fact. It does not fix q.

**Candidate principle: minimal integer lattice in the 4 of su(4).**

The fundamental **4** of su(4) acting on V_c ⊕ V_s has Q₄ eigenvalues {q, q, q, −3q}. The minimal integer normalization sets q = 1 (giving eigenvalues {1, 1, 1, −3}). This is the "canonical" normalization for the Cartan of su(4) acting on the fundamental **4**.

**Assessment:** Setting q = 1 gives eigenvalues {1,1,1,−3}. Setting q = 1/3 gives eigenvalues {1/3, 1/3, 1/3, −1}. These are the same up to an overall factor of 3. The minimal integer normalization (q=1) is a natural algebraic choice, but it does not give the SM values 1/3 and −1. It gives 1 and −3.

The SM values (1/3 and −1) emerge from dividing the minimal integer normalization by 3. Why divide by 3? Only because we know that quarks carry baryon number 1/3, not 1. This knowledge is external.

**Candidate principle: compatibility with fundamental/anti-fundamental charge quantization.**

In the fundamental **4** of su(4) with the canonical normalization q=1: the anti-fundamental **4̄** carries Q₄ eigenvalues {−1,−1,−1,+3}. The charge lattice generated by **4** and **4̄** includes integers and multiples of 3. This is a self-consistent charge lattice.

Dividing by 3 to get the {1/3, −1} convention creates a charge lattice where the minimal charge quantum is 1/3. This matches the SM charge lattice (where the electron charge is 3 times the quark charge). But this match is precisely because the SM has this specific charge lattice — the algebra does not derive it.

**Candidate principle: uniqueness of the smallest integral normalization.**

The smallest normalization under which all Q₄ eigenvalues are integers is q = 1 (giving {1,1,1,−3}). This is canonical. The sub-canonical normalization q = 1/3 gives non-integer eigenvalues {1/3, 1/3, 1/3, −1}.

Non-integer eigenvalues in charge operators are unusual for internal symmetry generators in the context where the generator represents a discrete physical charge. They arise in the SM because the fundamental charge unit is the electron charge, and quarks carry 1/3 of it. But this 3-fold sub-division of the charge unit is itself a physical fact about QCD, not an algebraic necessity.

**Verdict on Part 3:**

The minimal integer normalization q = 1 is algebraically natural and derivable internally. The SM normalization q = 1/3 is not algebraically natural — it requires dividing by dim(V_c) = 3, which is natural only given that quarks (the physical content of V_c) carry fractional baryon number 1/3.

**Outcome: The 1/3, −1 assignment is NOT essentially derived. It is still external.** The canonical algebraic normalization gives {1, 1, 1, −3}, not {1/3, 1/3, 1/3, −1}.

**However:** There is a mathematically natural way to reach the SM normalization. The **canonical fractional** normalization of Q₄ in the **4** of su(4) divides the integer normalization by dim(ℂ³) = 3 in order to equalize the per-direction charge within ℂ³. This "per-direction" convention is algebraically natural in the sense that it treats all 3 directions of ℂ³ as equivalent (equal charge per direction). Under this convention, the charge per ℂ³ direction = 1/dim(ℂ³) = 1/3, and the ℂ¹ charge = −1 by tracelessness.

**The "per-direction" normalization can be stated as an internal principle:** Q₄ is normalized so that the charge per basis direction in ℂ³ is the minimal positive unit (= 1/dim(ℂ³)). This is internal to the block structure (it treats ℂ³ and ℂ¹ as having equal total charge weight, divided equally among ℂ³'s 3 directions). Under this principle, the 1/3 normalization follows from dim(ℂ³) = 3, without importing QCD.

**This is the strongest internal derivation available:** The per-direction normalization is motivated by the symmetric structure of ℂ³ (3 equal directions under su(3)). It gives {1/3, 1/3, 1/3, −1}. It does not require knowing that these are quark baryon numbers and lepton numbers. It requires only that the 3 equal directions of ℂ³ are treated symmetrically and divided equally.

---

## Part 4 — Is "Leptonic Color" Merely Best, or Effectively Unique?

**For ℂ¹ to carry B-L = −1 (lepton number), two things must hold:**

(a) The physical content of ℂ³ carries B-L = +1/3 per direction (= quark sector).
(b) The charge −1 on ℂ¹ is identified as lepton number, not some other −1-charged object.

**Testing alternative physical readings of ℂ¹:**

**A: Lepton direction (standard).**

ℂ¹ carries Q₄ charge −1 (in the SM normalization). Leptons have B-L = −1. Identification: ℂ¹ = lepton. The staged corridor closes to SM. This is the standard reading. ✓

**B: Dark/sterile singlet.**

ℂ¹ carries Q₄ charge −1. Some dark sector singlets (e.g., right-handed sterile neutrino) also carry B-L = −1. If ℂ¹ = right-handed neutrino direction: the gauge algebra commutant is still SM (the commutant depends on Q₄, not on the physical content of ℂ¹). The gauge algebra is unchanged; the matter content interpretation differs. The corridor still closes to SM.

**Assessment:** The gauge algebra is the same for readings A and B. Both give the same commutant (= SM gauge group). The difference between A and B is in the matter sector, not the gauge sector. For the purposes of the two-stage corridor to the SM gauge algebra, A and B are equivalent.

**C: Generic U(1)-charged singlet.**

If ℂ¹ represents any sector with a U(1) charge of −1, the gauge algebra is still the SM. The corridor closes the same way.

**D: Mathematical completion only.**

The gauge algebra commutant is SM regardless of whether ℂ¹ has a physical interpretation. The corridor closes purely algebraically (given Q₄).

**Verdict:** "Leptonic color" versus "sterile singlet" versus "any −1-charged singlet" are all physically different matter assignments, but they all give the **same gauge algebra** when the commutant of Q₄ is computed. The two-stage corridor to the **gauge algebra** su(3)⊕su(2)⊕u(1) does not depend on whether ℂ¹ = lepton, sterile neutrino, or dark sector.

**This is a significant clarification:** The corridor derivation is about the gauge algebra, not the matter representation. "Leptonic color" as a physical interpretation is irrelevant to whether the corridor closes to the SM gauge algebra. The closure is gauge-sector only. The physical identification of ℂ¹ = lepton requires separate input from the matter sector.

**"Leptonic color" is not even the right vocabulary for the gauge corridor claim. The corridor closes to su(3)⊕su(2)⊕u(1) as a gauge algebra regardless of what ℂ¹ represents physically.**

---

## Part 5 — Is There a Theorem About Minimal Imported Physics?

**The strongest honest statement:**

**Theorem (proved — gauge sector only):**

Given the block decomposition V = ℂ³ ⊕ ℂ² ⊕ ℂ¹ with metric η = diag(+1,+1,+1,−1,−1,+1), the su(4,2) algebra, and the per-direction normalization of Q₄ (charge per ℂ³ direction = 1/dim(ℂ³)), the two-stage corridor:

su(4,2) → [W_decoh] → su(4)⊕su(2)⊕u(1) → [centralizer of Q₄] → su(3)⊕su(2)⊕u(1)

produces the SM gauge algebra.

**What is imported:**

1. The block decomposition ℂ³ ⊕ ℂ² ⊕ ℂ¹ with dimensions (3,2,1) — not forced by su(4,2); it is one of several valid 3-block splittings of ℂ⁶ with signature (4,2).
2. The per-direction normalization of Q₄ — algebraically natural given the symmetric structure of ℂ³, but not forced.
3. The identification of the 12-dimensional commutant algebra with "SM gauge algebra" — this is recognition, not derivation (the algebra su(3)⊕su(2)⊕u(1) is known to be the SM; the derivation produces this algebra, and we recognize it).

**What is NOT imported:**

1. Any specific particle content (quarks, leptons, Higgs — none of these appear).
2. Any mass spectrum, coupling constants, or generation structure.
3. The matter representation of the gauge group.
4. Any identification of ℂ¹ as "lepton" (the corridor closes without this identification).

**The minimal imported physics is:**

- The block dimensions (3,2,1) must be chosen to give the right sizes for su(3), su(2), u(1).
- The resulting 12-dimensional algebra must be recognized as the SM.

The first point is a structural choice (not derived). The second is recognition (not derivation).

---

## Part 6 — What Is Still External Now?

**Precise classification of remaining external inputs:**

**The block structure (3,2,1) is the primary external input.**

The decomposition ℂ³ ⊕ ℂ² ⊕ ℂ¹ with the (+,−,+) metric pattern is the key structural input that determines the whole path. Without this specific decomposition, there is no su(4,2), no Q₄, no staged corridor. The choice to split ℂ⁶ this way rather than as ℂ²⊕ℂ²⊕ℂ² or ℂ⁴⊕ℂ²⊕ℂ⁰ is not forced by any algebraic principle we have identified.

**Type I (missing view): The selection of the (3,2,1) block structure.**

Why (3,2,1) rather than (2,2,2) or (1,1,4)? The algebra su(4,2) with signature (4,2) admits many 3-block decompositions. What selects the specific (3,2,1) split? This is genuinely a missing view — we have not identified any principle that forces this specific block structure from within the algebra.

**Type II (missing invariant): The normalization convention.**

The per-direction normalization of Q₄ (dividing by dim(ℂ³) = 3) is mathematically natural given the symmetric structure of ℂ³ under su(3), but it is a convention. An internal invariant that forces this normalization would be: a principle stating that the minimal charge quantum of the fundamental **4** of su(4) is 1/dim(subspace), where subspace is the smaller of the two pieces in the 3+1 decomposition. This is suggestive but not proved as a theorem.

**Type IV (convention dependence):** The identification of the commutant as "the SM gauge algebra" is a recognition step that requires knowing the SM. This is not a deep problem — it is just labeling. The algebra su(3)⊕su(2)⊕u(1) is what it is; calling it "the SM gauge algebra" requires knowing that the SM has this gauge group.

**The remaining external content, minimized:**

1. **The block structure (3,2,1)** — the primary structural input, not yet derived.
2. **Recognition of the 12-dimensional algebra as SM** — naming, not physics.
3. **The normalization convention** — natural but not forced.

The particle physics content (quarks, leptons, "leptonic color") has been completely removed from the gauge corridor claim. It was never needed for the corridor to close. It was only imported as an interpretive layer.

---

## Final Verdict

**The staged gauge corridor is: "Forced except for the block structure (3,2,1) and a normalization convention."**

**Not "almost fully internal":** The block structure (3,2,1) is the load-bearing external input. Without it, there is no su(4,2) or no particular su(4,2) with signature (4,2). It is chosen to match the SM block content.

**Not "forced except for particle naming":** The "leptonic color" language was a red herring for the gauge corridor. The corridor closes to su(3)⊕su(2)⊕u(1) regardless of whether ℂ¹ is called "lepton," "sterile singlet," or "abstract singlet." No particle naming is required for the gauge algebra result.

**Not "still genuinely external in a serious way":** The remaining external inputs are: (a) the (3,2,1) block choice, and (b) the per-direction normalization. Both are physically motivated by the SM structure, but neither imports particle dynamics, masses, couplings, or generation structure. They are structural choices about the representation space.

**The correct minimal statement:**

> The construction derives su(3)⊕su(2)⊕u(1) as the gauge algebra from su(4,2) via two natural corridor filtrations, given the specific block decomposition ℂ⁶ = ℂ³⊕ℂ²⊕ℂ¹ with the (+,−,+) metric signature. The block decomposition is a structural input that is physically motivated but not algebraically forced. The "leptonic color" language was not required — the result is a gauge algebra derivation, not a matter sector derivation.

---

## What the Algebra Gives For Free

1. su(4,2) from the metric signature (4,2)
2. Unique Q₄ (three naturalness conditions)
3. Eigenvalue ratio 1:−3 (tracelessness)
4. Commutant = su(3)⊕su(2)⊕u(1) (exact theorem)
5. The staged corridor structure (two disjoint filtrations with A₁ ∩ A₂ = ∅)

## What Still Requires Particle Interpretation

1. The block structure (3,2,1) must be motivated — why this split rather than another?
2. The per-direction normalization of Q₄ (natural but not forced)
3. Recognition of the commutant as "the SM gauge algebra" (naming)
4. The matter sector — representations, chirality, Yukawa couplings, EW breaking (all still open)

## Alternative Readings Table (Revised Understanding)

| Interpretation of ℂ³ and ℂ¹ | Gauge algebra changes? | Corridor closes to SM? | Matter physics changes? |
|---|---|---|---|
| ℂ³ = quark colors, ℂ¹ = lepton | **No** | **Yes** | Standard SM |
| ℂ³ = dark sector triplet, ℂ¹ = dark singlet | **No** | **Yes** | Non-SM dark sector |
| ℂ³ = abstract triplet, ℂ¹ = abstract singlet | **No** | **Yes** | Unspecified |
| ℂ³ = quark colors, ℂ¹ = sterile neutrino | **No** | **Yes** | SM + right-handed neutrino |

**All readings give the same gauge algebra.** The corridor is gauge-algebra-universal within the (3,2,1) block structure. Particle physics is not imported into the gauge corridor — it lives in the matter sector, which is separate.
