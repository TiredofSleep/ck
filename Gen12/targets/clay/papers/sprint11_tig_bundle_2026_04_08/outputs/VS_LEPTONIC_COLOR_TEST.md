# VS_LEPTONIC_COLOR_TEST
## Is V_s = Leptonic Color Forced, Preferred, or External?
*Base state settled. One question: can the staged path close from within the algebra?*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — The Single Load-Bearing Interpretive Step

The two-stage corridor is algebraically exact:

```
su(4,2)   →[metric-sign filter]→   su(4)⊕su(2)⊕u(1)   →[commutant of Q_{B-L}]→   su(3)⊕su(2)⊕u(1)
```

The first stage is fully automatic — given the algebra, the compact subalgebra is determined by structure theory.

The second stage requires a specific Cartan generator Q_{B-L}. The algebra has 5 independent Cartan generators. Among these 5, Q_{B-L} = i·diag(1/3,1/3,1/3,0,0,−1) is one choice. The question: is it forced, or is it chosen?

**The honest statement:**

Without a principle selecting Q_{B-L} over the other 4 Cartan generators, the second corridor is underdetermined — it could close to any of several 12-dimensional subalgebras of su(4)⊕su(2)⊕u(1), depending on which Cartan is used.

With Q_{B-L} selected, the commutant is exactly the SM. But "use the B-L generator" is the same as saying "interpret V_s as leptonic color." The selection of Q_{B-L} and the interpretation V_s = leptonic color are the same step stated differently.

**The real next problem:** Not closing the algebra. Not computing commutants. The question is whether the su(4,2) structure, together with the physical requirement that the IR be a known gauge algebra, *uniquely selects* leptonic color as the correct interpretation of V_s — or whether this is an irreducible external input.

---

## Part 2 — Testing Internal Asymmetries

### Asymmetry 1: Dimensional Asymmetry (V_c=3, V_w=2, V_s=1)

The three subspaces have dimensions 3, 2, 1. Is the 1-dimensionality of V_s algebraically distinctive?

**Analysis:**

In the 6-dimensional fundamental representation of su(4,2), the three subspaces split as ℂ³ ⊕ ℂ² ⊕ ℂ¹. The dimensions are set by the block decomposition we chose for the Hodge sign flip (+1,−1,+1). The choice (3,2,1) is not forced by the algebra alone — we could also have chosen (2,2,2), (1,1,4), (4,1,1), etc., all giving signature (4,2) with η a block-diagonal metric with appropriate signs.

**But:** Among all decompositions of ℂ⁶ into blocks of dimensions (n₁, n₂, n₃) with metric signature (n₁+n₃, n₂) = (4,2), only these decompositions produce a (4,2) signature with three blocks:

(n₁,n₂,n₃) with n₁+n₃ ≥ n₂, and two blocks positive, one negative:
- (3,2,1), (1,2,3), (2,2,2), (4,2,0)≡two blocks, (4,0,2)≡two blocks...

Among three-block decompositions with the middle block negative: (n₁, n₂, n₁) — symmetric cases — or (3,2,1) — asymmetric.

**The (3,2,1) decomposition is the smallest** that contains a non-trivial structure in each block while matching the SM-relevant dimensions (3 colors, 2 weak charges, 1 remaining). It is "minimal" in the sense that adding a fourth block would increase the total dimension beyond 6.

**Does 1-dimensionality force V_s to be a singlet direction?**

Yes, in a limited sense: a 1-dimensional complex subspace ℂ¹ carries a U(1) = SO(2) rotation symmetry, nothing richer. It cannot support an SU(n) for n ≥ 2. So V_s must represent something with only phase (U(1)) degrees of freedom — which is consistent with lepton number (a U(1) charge), but also consistent with any other U(1) quantum number (dark charge, baryon number, etc.).

**Verdict on asymmetry 1:** The 1-dimensionality of V_s forces it to be a U(1)-type direction, but does not specify which U(1). Necessary but not sufficient for leptonic color.

---

### Asymmetry 2: Metric Asymmetry (V_c and V_s share metric sign +1; V_w has metric −1)

V_c (metric +1) and V_s (metric +1) are in the same metric sector. V_w (metric −1) is the "opposite" sector. W_decoh kills the color-weak cross-sector generators (A₁). The compact subalgebra su(4) acting on V_c ⊕ V_s treats these two subspaces as part of a single 4-dimensional +1 sector.

**What does the metric say about V_s relative to V_c?**

Within the +1 metric sector (V_c ⊕ V_s = ℂ⁴), the group SU(4) acts on the full 4-dimensional space. The su(4) subalgebra does NOT algebraically distinguish V_c from V_s — both are subspaces of the same metric sector. From the metric perspective alone: V_c and V_s are "same kind." The metric puts V_w apart but does not separate V_c from V_s.

**The 3+1 splitting of ℂ⁴ is not forced by the metric.** The metric on ℂ⁴ is proportional to the identity (all +1). SU(4) acts transitively on 1-dimensional subspaces of ℂ⁴ and transitively on 3-dimensional subspaces. There is no SU(4)-invariant way to single out the "V_s direction" from "V_c directions" using only the metric.

**Verdict on asymmetry 2:** The metric asymmetry (between V_c⊕V_s and V_w) is used fully by Stage 1. Within the +1 sector, the metric does NOT distinguish V_c from V_s. The 3+1 split of ℂ⁴ into "color" and "singlet" requires additional structure beyond the metric.

---

### Asymmetry 3: Role of V_s in Enlarging Color su(3) → su(4)

Inside the compact subalgebra, su(4) acts on V_c ⊕ V_s = ℂ⁴. The subalgebra su(3) ⊂ su(4) is the one that acts trivially on V_s and non-trivially on V_c. There is exactly one such su(3) (up to conjugation by SU(4) elements that preserve V_s). 

**The unique su(3) ⊂ su(4) that preserves V_s:** The stabilizer of a 1-dimensional subspace V_s in SU(4) is S(U(3)×U(1)) = SU(3)×U(1)/ℤ₃. The su(3) factor is uniquely determined (up to the SU(4) orbit) as the algebra acting trivially on V_s.

**Question: is the "4th dimension" V_s in SU(4) generically identifiable as "leptonic" or as "any 4th color"?**

In the Pati-Salam model: the 4-dimensional space of SU(4)_c contains quarks (R,G,B) and the 4th direction = lepton. The identification is *imposed* by requiring the theory to unify quarks and leptons — it is not derived from SU(4) alone.

In abstract SU(4): any 1-dimensional direction can be singled out as "the 4th." The group SU(4) acts transitively on 1-dimensional subspaces of ℂ⁴ — so all choices of V_s inside ℂ⁴ are SU(4)-equivalent. There is no algebraic distinction between V_s and any other 1-dimensional subspace.

**Verdict on asymmetry 3:** V_s is not algebraically distinguished within su(4). The identification "V_s = leptonic color" comes from the physical requirement that the 4th component of a color multiplet should be leptons — a requirement from the quark-lepton unification program, not from the algebra itself.

---

### Asymmetry 4: Cartan Naturalness

The Cartan subalgebra of su(4,2) has rank 5. An explicit Cartan basis includes generators of the form i·diag(λ₁,λ₂,λ₃,λ₄,λ₅,λ₆) with Σλ_j = 0. The 5 independent generators form a 5-dimensional real vector space.

**Is Q_{B-L} = i·diag(1/3,1/3,1/3,0,0,−1) distinguished among all Cartan generators?**

Within the compact subalgebra su(4)⊕su(2)⊕u(1), the Cartan has rank 3+1+1 = 5 (2 independent generators for su(3) ⊂ su(4), 1 for su(2), plus 2 from u(1) factors). Q_{B-L} is a specific element of this 5-dimensional space.

**Candidate natural Cartan generators in the compact sector:**

- Q₁ = i·diag(1,−1,0,0,0,0) — SU(3) Cartan (gluon direction)
- Q₂ = i·diag(1,1,−2,0,0,0) — SU(3) Cartan (other gluon direction)
- Q₃ = i·diag(0,0,0,1,−1,0) — SU(2) Cartan (weak isospin)
- Q₄ = i·diag(1,1,1,0,0,−3) — measures "color vs singlet" content (∝ B−L after rescaling if V_s=lepton)
- Q₅ = i·diag(1,1,1,−1,−1,−1)·α — measures "color+singlet vs weak" (hypercharge-like)

Q_{B-L} is proportional to Q₄ (Q_{B-L} = (1/3)·Q₄ up to overall normalization).

**Is Q₄ distinguished among {Q₁,...,Q₅}?**

Yes, in one specific sense: Q₄ is the unique Cartan generator (up to the SU(3)⊕SU(2) subalgebra) that **measures the V_s content of a state** — it assigns +1 to V_c directions and a different value to V_s, while assigning zero to V_w directions.

More precisely: Q₄ = i·diag(1,1,1,0,0,−3) separates:
- States in V_c: eigenvalue +1 (or equivalently baryon-number-like +1/3 per quark)
- States in V_w: eigenvalue 0
- State in V_s: eigenvalue −3 (equivalently lepton-number-like −1 per lepton after rescaling)

**Is this distinguished from the other Cartan generators?**

Q₄ is the unique Cartan generator of su(4)⊕su(2)⊕u(1) that:
- Acts trivially on V_w (eigenvalue 0 on V_w)
- Distinguishes V_c from V_s (different eigenvalues on V_c and V_s)
- Is orthogonal to all SU(3) and SU(2) Cartans

This is a non-trivial uniqueness condition: among all Cartan generators, Q₄ is the only one orthogonal to the su(3) Cartan and the su(2) Cartan and also to V_w, while distinguishing V_c and V_s.

**The uniqueness result (structural):** Q₄ is distinguished by being the unique generator in the Cartan of su(4)⊕su(2)⊕u(1) that:
1. Commutes with all of su(3) (automatically, as a Cartan of su(4) commuting with su(3) ⊂ su(4))
2. Commutes with all of su(2) (eigenvalue 0 on V_w)
3. Assigns non-equal values to V_c and V_s

**This is Q_{B-L} (up to normalization).** No other Cartan generator satisfies all three conditions simultaneously.

---

## Part 3 — Alternative Readings of V_s (Comparison Table)

| Interpretation | Naturalness from su(4,2) | Natural Cartan filter? | Closes to SM? | Extra assumptions |
|---|---|---|---|---|
| **A: Leptonic color** | Consistent with all algebraic structures | **Q₄ = Q_{B-L} (uniquely selected by conditions 1+2+3)** | **Yes — exact** | V_s = lepton number assignment |
| B: Arbitrary singlet | Consistent — algebra does not force any reading | No unique filter | No — depends on choice | Nothing forced; many possible 12-dim subalgebras |
| C: Sterile/dark singlet | Consistent — but disconnected from SM physics | Dark-charge generator (distinct from Q₄) | No — different commutant | Dark charge must be defined separately |
| D: Mathematical completion (no physical meaning yet) | Consistent | No natural physical Cartan | Undetermined | Deferred — leaves second corridor open |

**The table shows:** V_s = leptonic color is the **unique interpretation that makes Q₄ physically meaningful as a conserved charge**, and Q₄ is the **unique Cartan satisfying conditions 1+2+3**. The two uniqueness claims reinforce each other.

---

## Part 4 — Which Outcome Is Supported?

**Outcome 1:** V_s is uniquely distinguished as the only possible "4th color" direction by the block/metric structure.

**Assessment: FALSE.** The metric alone does not distinguish V_s from V_c within the +1 sector. The 3+1 split of ℂ⁴ is not forced by the metric.

**Outcome 2:** V_s is not uniquely forced, but leptonic color is the only interpretation that makes the second corridor land on a known physical gauge algebra, AND Q_{B-L} is the unique Cartan generator satisfying the three naturalness conditions.

**Assessment: SUPPORTED, with a strong form.** The algebraic uniqueness of Q₄ (conditions 1+2+3) is a real result. It says: among all Cartan elements of su(4)⊕su(2)⊕u(1), exactly one generator separates V_c from V_s while commuting with both su(3) and su(2). That generator is Q₄ ∝ Q_{B-L}. The commutant of Q₄ is the SM. No other Cartan generator satisfies all three conditions and also gives the SM as its commutant.

**Outcome 3:** V_s remains genuinely ambiguous, so the construction is irreducibly two-input.

**Assessment: FALSE for the strong form.** Q₄ is algebraically distinguished (Outcome 2 holds). The ambiguity reduces to: why should Q₄ be the natural physical Cartan? Answer: because it is the unique Cartan satisfying the naturalness conditions 1+2+3. This is a real selection principle, not an arbitrary choice.

**The correct verdict: Outcome 2, strong form.**

---

## Part 5 — Paradox Classifier Applied to the Remaining Gap

**What kind of problem is the remaining gap, exactly?**

**Type I (missing view):** Partially applies. We now have the uniqueness of Q₄ — this is new information that was missing before this analysis. The "view" is now more complete: Q₄ is uniquely selected by the three naturalness conditions. What remains: the identification of Q₄ with B−L charge is a physical assignment, not an algebraic derivation.

**Type II (missing invariant):** This is the most relevant type. The gap is: is there a natural invariant quantity of the su(4,2) structure that, when computed, assigns the value B−L = −1 to V_s and B−L = +1/3 to V_c? If such an invariant exists in the algebra, the interpretation is derived. If not, it remains external.

**Candidate Type II resolution:** The Q₄ generator is already in the algebra. The eigenvalue structure (Q₄ on V_c = +i, Q₄ on V_s = −3i) is determined by the trace condition of su(4,2). The ratio of eigenvalues: Q₄ on V_s / Q₄ on V_c = −3/1. If this ratio is identified as the B−L ratio (B−L of lepton = −1 relative to B−L of quark = +1/3, giving ratio −3), then the assignment IS algebraically determined — the 3:1 dimension ratio of V_c:V_s forces the Q₄ eigenvalue ratio to be 3:1 by the tracelessness condition.

**The Type II invariant may be the trace condition itself:**

For Q₄ = i·diag(1,1,1,0,0,α): the tracelessness condition requires 3 + α = 0 → α = −3. The eigenvalue −3 on V_s is forced by tracelessness and the +1 eigenvalues on V_c. If we then divide by 3 (normalizing to the quantum of baryon number per quark = 1/3): B−L of V_s = −3/3 = −1 and B−L of V_c = 1/3 each. The normalization by 3 (the dimension of V_c) is natural — it gives the standard baryon number per quark.

**This is the invariant:** The tracelessness of su(4) combined with the 3-dimensional color sector forces the singlet direction to carry eigenvalue −3 under Q₄. Dividing by the dimension of V_c = 3 gives the standard B−L charges. The physical interpretation follows from the normalization convention.

**Type III (admissibility):** Not relevant — the algebra is well-defined.

**Type IV (observer-choice dependence):** The normalization choice (divide by 3 to get standard B−L charges) is a convention. Different normalization choices give the same physical content (the relative eigenvalue ratio is fixed). This is a Phase IV convention artifact, not a genuine ambiguity.

**Summary: The remaining gap is Type II, and the missing invariant may be the tracelessness condition + dimension-of-V_c normalization.**

---

## Part 6 — The Selection Principle

**Candidate principle (structural, not yet a theorem):**

*The physically admissible interpretation of V_s is the unique one for which Q₄ — the Cartan generator orthogonal to su(3) and su(2) that distinguishes V_c from V_s — carries eigenvalues determined by the tracelessness of su(4) and the dimension of V_c, normalized to assign baryon number 1/(dim V_c) to each V_c direction and B−L = −1 to V_s.*

**Testing this principle:**

1. **Q₄ is unique:** Verified in Part 2. Q₄ is the unique Cartan in su(4)⊕su(2)⊕u(1) orthogonal to su(3) and su(2) Cartans and distinguishing V_c from V_s. ✓

2. **Eigenvalue ratio forced by tracelessness:** dim(V_c)·q_c + dim(V_s)·q_s = 0 → 3·q_c + 1·q_s = 0 → q_s = −3·q_c. Fixing q_c = i (a conventional choice for the compact generator normalization), q_s = −3i. ✓

3. **Normalization to baryon number:** Dividing by dim(V_c) = 3: charge per V_c direction = q_c/3 = i/3 = standard baryon number per quark (in natural units). V_s charge = q_s/3 = −i = standard lepton number per lepton (B−L = −1). This normalization is determined by the requirement that each V_c direction carries equal charge (= one unit per quark). ✓

4. **Commutant is SM:** Verified exactly. ✓

**Does this principle pick out leptonic color uniquely?**

Yes: the only consistent interpretation of V_s is one where it carries B−L charge = −1 (in the normalization where quarks carry B−L = +1/3). This is lepton number. There is no other consistent assignment with this normalization.

**But the principle requires the normalization convention "each V_c direction carries equal charge."** This is natural but is a convention. The alternative "each V_s direction carries unit charge" would give different numbers (and would not match the SM). The convention selection is physically motivated (quarks are 3-fold symmetric under color) but is not purely algebraic.

---

## Final Verdict

**Is V_s = leptonic color forced, strongly preferred, physically best, or irreducibly external?**

**Verdict: Strongly preferred, approaching forced, with one normalizable convention.**

The derivation path:
1. Q₄ is the unique Cartan in the compact subalgebra satisfying the three naturalness conditions (orthogonal to su(3) and su(2), distinguishes V_c from V_s). **Exact.**
2. The eigenvalue ratio of Q₄ on V_s vs V_c is −3:1, forced by tracelessness and dim(V_c)=3. **Exact.**
3. Normalizing by dim(V_c)=3 (so each color direction carries charge 1/dim = 1/3) assigns B−L = −1 to V_s. **Convention-dependent normalization, but physically natural.**
4. B−L = −1 is lepton number (in the B−L charge scheme). V_s = leptonic direction. **Physical identification, follows from step 3.**

The remaining "irreducibly external" component: the normalization convention (step 3). Choosing to normalize by dim(V_c) rather than by any other number is a natural but not algebraically forced choice. All other normalization conventions give the same *relative* charge structure (V_s carries charge = −dim(V_c) times the charge per V_c direction), but the absolute identification with lepton number requires fixing this convention.

**The construction is not fully self-closing. The single remaining external input is a normalization convention that assigns the quantum of charge per color direction.** Once this convention is chosen (as it naturally would be in any quantum field theory using the standard color normalization), V_s = leptonic color follows algebraically from the tracelessness and dimension conditions.

**In practice:** This is the weakest possible remaining "external input" — it is equivalent to choosing a normalization for the generators of SU(3), which is done in every quantum field theory textbook. The interpretation V_s = leptonic color is as close to "forced" as any physical interpretation can be without being purely algebraic. It is "forced, given the standard normalization convention for color charges."

---

## Sections Summary

### Is V_s Forced, or Chosen?

**Forced given one normalization convention.** Q₄ is the unique Cartan satisfying the three naturalness conditions (orthogonal to su(3) and su(2), distinguishes V_c and V_s). Its eigenvalue ratio is fixed by tracelessness and the 3:1 dimension ratio of V_c:V_s. The standard color normalization (baryon number 1/3 per quark) completes the identification as B−L charge. Under this convention, V_s = lepton is forced, not chosen.

### Can Q_{B-L} Be Selected Intrinsically?

**Yes — with one convention.** Q_{B-L} is uniquely determined as the Cartan of su(4)⊕su(2)⊕u(1) that (1) commutes with su(3) and su(2), (2) distinguishes V_c from V_s, and (3) is orthogonal to the SU(3) and SU(2) Cartan generators. Its eigenvalues are set by tracelessness. The normalization to B−L charges requires fixing the baryon number per color direction = 1/dim(V_c) = 1/3. This is the standard normalization of SU(3) color in QCD. Given this convention (which is universal in the SM), Q_{B-L} is intrinsic.

### The Two-Stage Corridor: Does It Self-Close?

**Yes, with one conventional input.** The two stages of the corridor use:
- Stage 1: the metric signature (4,2) — fully intrinsic to su(4,2)
- Stage 2: Q_{B-L} — intrinsic given the standard QCD color normalization

The construction is as self-closing as any physical theory can be: it reduces to one conventional normalization choice that is universal in the SM and well-motivated by the color symmetry of quarks.
