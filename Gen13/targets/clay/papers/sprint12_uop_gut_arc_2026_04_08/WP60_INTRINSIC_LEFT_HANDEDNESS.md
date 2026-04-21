# WP60 — Intrinsic Left-Handedness and Charge Emergence
## Left-Handed SM Charges from the su(4,2) Two-Stage Corridor and the SU(2)_R Obstruction

**Date**: 2026-04-08
**Sprint**: 12 — UOP/GUT Arc
**Status**: Theorem LH PROVED (exact); Theorem IL PROVED (structural); Theorem RH-Failure PROVED (exact); Minimal Extension STRUCTURAL
**Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes

---

## Abstract

The ℂ⁶ = V_c(3) ⊕ V_w(2) ⊕ V_s(1) construction on the non-compact algebra su(4,2) yields exact Standard Model electric charges for all left-handed doublet matter fields via Q_EM = T₃_L + (1/2)·Q₄. The algebra is intrinsically left-handed: the maximal compact subalgebra of su(4,2) is su(4)⊕su(2)⊕u(1), containing exactly one rank-1 simple compact factor (SU(2)_L). No SU(2)_R can be found in the compact subalgebra, the non-compact generators, or the Cartan. Right-handed fields miss Q_EM by exactly ±1/2, identifying the missing T₃_R eigenvalue. The minimal extension is su(4,2) × su(2)_R — a product structure unavoidable by a proved no-go theorem for simple non-compact groups.

---

## §1. Setup: The ℂ⁶ Block Decomposition and su(4,2)

### 1.1 The Block Structure

The fundamental representation space is ℂ⁶ with block decomposition:

    ℂ⁶ = V_c(3) ⊕ V_w(2) ⊕ V_s(1)

where V_c is a 3-dimensional color sector, V_w is a 2-dimensional weak sector, and V_s is a 1-dimensional singlet/leptonic sector.

The metric is η = diag(+1,+1,+1,−1,−1,+1) (signature (4,2): four positive, two negative entries, with the two negative entries on V_w). This signature determines the real form of the UV algebra.

### 1.2 The UV Algebra

The algebra of η-preserving transformations on ℂ⁶ is su(4,2): the non-compact real form of the complex Lie algebra A₅ (dimension 35) determined by signature (4,2).

Standard theorem: the maximal compact subalgebra of su(p,q) is

    k = su(p) ⊕ su(q) ⊕ u(1)

For su(4,2): k = su(4) ⊕ su(2) ⊕ u(1), dimension 15 + 3 + 1 = 19.

The 16 non-compact generators connect the (+) and (−) metric sectors; they have Hermitian (not anti-Hermitian) form and generate non-compact subalgebras.

### 1.3 The Two-Stage Corridor

**Stage 1 (Decoherence filtration):** Generators mixing (+) and (−) metric sectors decohere under the W_decoh mechanism (weighted by the metric-sign factor). In the IR limit, these 16 non-compact generators are suppressed. The surviving algebra is the compact subalgebra: su(4) ⊕ su(2)_L ⊕ u(1).

**Stage 2 (Q₄ commutant filtration):** The distinguished Cartan generator

    Q₄ = i·diag(1/3, 1/3, 1/3, 0, 0, −1)

(B-L-like charge: +1/3 per color direction, 0 on V_w, −1 on V_s) is the unique neutral pre-breaking U(1) satisfying tracelessness and the block-structure normalization. The commutant of Q₄ within su(4) ⊕ su(2)_L ⊕ u(1) is:

    C(Q₄) = su(3) ⊕ su(2)_L ⊕ u(1)_{Q₄}

This is the Standard Model gauge algebra (dimension 8 + 3 + 1 = 12).

---

## §2. Theorem LH: Left-Handed Charge Emergence

**Theorem LH (Left-Handed Charge Table — proved)** [PROVED]:

Given the block decomposition ℂ⁶ = V_c(3) ⊕ V_w(2) ⊕ V_s(1), the pre-breaking algebra su(3) ⊕ su(2)_L ⊕ u(1)_{Q₄}, and EW breaking that selects a T₃_L direction in SU(2)_L:

    Q_EM = T₃_L + (1/2)·Q₄

assigns the correct SM electric charges to all left-handed doublet matter fields.

**Proof (direct computation)** [COMPUTED]:

| Field | T₃_L | Q₄ | Q_EM = T₃_L + Q₄/2 | SM value | Match? |
|---|---|---|---|---|---|
| u_L | +1/2 | +1/3 | 1/2 + 1/6 = **2/3** | +2/3 | ✓ |
| d_L | −1/2 | +1/3 | −1/2 + 1/6 = **−1/3** | −1/3 | ✓ |
| ν_L | +1/2 | −1 | 1/2 − 1/2 = **0** | 0 | ✓ |
| e_L | −1/2 | −1 | −1/2 − 1/2 = **−1** | −1 | ✓ |

All four charges are exact. □

**Why Q₄ = B-L for left-handed doublets.** In the SM, hypercharge Y equals B-L for left-handed doublet fields: Y(u_L,d_L) = 1/3 = B-L(quark), Y(ν_L,e_L) = −1 = B-L(lepton). Q₄ assigns the same values. Therefore Q_EM = T₃ + Y/2 = T₃ + Q₄/2 is exact for these fields. The formula works because Q₄ is B-L, and B-L equals Y for left-handed doublets.

**What the theorem requires** [STRUCTURAL]:
1. The block structure V = V_c(3) ⊕ V_w(2) ⊕ V_s(1) with Q₄ values (exact, from corridor derivation).
2. The EW breaking mechanism selecting T₃_L (assumed, not derived within this paper).
3. Matter assignment: quarks in V_c sector, leptons in V_s sector (physical input).

**What the theorem does NOT cover:** Right-handed singlets (T₃_L = 0), the EW breaking mechanism itself, or the right-handed sector.

---

## §3. Theorem IL: No SU(2)_R in su(4,2)

**Theorem IL (Intrinsic Left-Handedness)** [PROVED]:

The block decomposition ℂ⁶ = V_c(3) ⊕ V_w(2) ⊕ V_s(1) contains exactly one rank-1 compact simple Lie algebra factor in the compact subalgebra of su(4,2), namely su(2)_L acting on V_w = ℂ². No second independent su(2) factor (SU(2)_R) exists in the compact subalgebra, the non-compact generators, or the Cartan subalgebra of su(4,2).

**Proof (four parts):**

**Part A: Compact subalgebra is su(4) ⊕ su(2)_L ⊕ u(1), dimension 19.**

Standard theorem (exact): k(su(p,q)) = su(p) ⊕ su(q) ⊕ u(1). For su(4,2): k = su(4) ⊕ su(2) ⊕ u(1). Dimension: 15 + 3 + 1 = 19. This is exhaustive. □

**Part B: Exactly one rank-1 simple factor in k.**

The simple factors of su(4) ⊕ su(2) ⊕ u(1) are su(4) (rank 3) and su(2) (rank 1). There is no additional rank-1 simple factor. A second su(2)_R in the compact subalgebra would require either:

(i) A second rank-1 simple subalgebra of su(4)⊕su(2)⊕u(1) independent of su(2)_L: su(4) contains multiple su(2) subalgebras (e.g., as diagonal subalgebras of su(4) acting on 2-dimensional subspaces of V_c ⊕ V_s). However, any such su(2) ⊂ su(4) acts on a 2-dimensional subspace of V_c ⊕ V_s = ℂ⁴ — not on a right-handed weak doublet. It would be a "color su(2)" or "color-singlet su(2)", not a right-handed weak isospin. Without an additional 2-dimensional sector V_{wR} distinct from V_w, no su(2) ⊂ su(4) can play the role of SU(2)_R acting on (u_R, d_R) doublets.

(ii) A second simple factor added "by hand": Not present in the compact subalgebra of su(4,2). □

**Part C: Non-compact generators cannot supply SU(2)_R.**

The 16 non-compact generators of su(4,2) are Hermitian (not anti-Hermitian). Suppose three Hermitian operators X, Y, Z satisfy su(2) relations [X,Y] = Z, [Y,Z] = X, [Z,X] = Y.

Compute: [X,Y] = XY − YX. For Hermitian X,Y: [X,Y]† = [Y†,X†] = [Y,X] = −[X,Y]. So [X,Y] is anti-Hermitian. But Z is supposed to be Hermitian. Contradiction: anti-Hermitian ≠ Hermitian (unless zero). Non-compact generators cannot form an su(2) subalgebra. □

**Part D: Cartan subalgebra contains no su(2) structure.**

The Cartan subalgebra of su(4,2) is abelian (rank 5, all elements commute). An su(2) subalgebra requires three non-commuting generators. The Cartan cannot contain or generate su(2)_R. □

**Conclusion:** No SU(2)_R exists anywhere in su(4,2) that can play the role of right-handed weak isospin. The construction is intrinsically left-handed. □

---

## §4. Theorem RH-Failure: Right-Handed Mismatch = ±1/2

**Theorem RH-Failure (Right-Handed Obstruction)** [PROVED]:

For right-handed SM singlet fields with T₃_L = 0, the formula Q_eff = T₃_L + (1/2)·Q₄ fails by exactly ±1/2, with the sign equal to the T₃_R eigenvalue that would be required in the Pati-Salam formula Q = T₃_L + T₃_R + (B-L)/2.

**Right-handed mismatch table** [COMPUTED]:

| State | Sector | T₃_L | Q₄ | Q_eff | SM Q | Error | Required T₃_R |
|---|---|---|---|---|---|---|---|
| u_R | V_c (color) | 0 | +1/3 | 0 + 1/6 = **+1/6** | +2/3 | **+1/2** | +1/2 |
| d_R | V_c (color) | 0 | +1/3 | 0 + 1/6 = **+1/6** | −1/3 | **−1/2** | −1/2 |
| e_R | V_s (singlet) | 0 | −1 | 0 − 1/2 = **−1/2** | −1 | **−1/2** | −1/2 |
| ν_R | V_s (singlet) | 0 | −1 | 0 − 1/2 = **−1/2** | 0 | **+1/2** | +1/2 |

**The pattern is exact:** Every right-handed field has error exactly ±1/2, matching the T₃_R eigenvalue in an SU(2)_R doublet.

**The repair formula** [COMPUTED]: Using Q = T₃_L + T₃_R + (1/2)·Q₄:
- u_R: 0 + 1/2 + 1/6 = 2/3 ✓
- d_R: 0 − 1/2 + 1/6 = −1/3 ✓
- e_R: 0 − 1/2 − 1/2 = −1 ✓
- ν_R: 0 + 1/2 − 1/2 = 0 ✓

This is the Pati-Salam formula Q = T₃_L + T₃_R + (B-L)/2. It works for all SM fields but requires T₃_R — the Cartan of a missing SU(2)_R. □

**Why the mismatch is ±1/2 exactly** [STRUCTURAL]: In the SM, right-handed quarks and leptons have hypercharge Y ≠ B-L. For u_R: Y = 4/3, B-L = 1/3. The difference Y − (B-L) = 1 = 2·T₃_R(u_R) = 2·(1/2). For d_R: Y = −2/3, B-L = 1/3. The difference = −1 = 2·T₃_R(d_R) = 2·(−1/2). The mismatch ±1/2 is algebraically exact, not approximate.

---

## §5. No-Go: Single UV Algebra Cannot Supply SU(2)_R

**Theorem No-Go (Single Simple Algebra)** [PROVED]:

No simple non-compact real Lie algebra g has its maximal compact subalgebra isomorphic exactly to su(4) ⊕ su(2)_L ⊕ su(2)_R ⊕ u(1).

**Proof.** The maximal compact subalgebra of a simple algebra su(p,q) is always su(p) ⊕ su(q) ⊕ u(1) — a two-factor semisimple algebra plus a central u(1). The target su(4) ⊕ su(2)_L ⊕ su(2)_R ⊕ u(1) has three simple factors (counting both su(2)s). No su(p) ⊕ su(q) equals su(4) ⊕ su(2) ⊕ su(2) for any p, q (since su(p) and su(q) are each simple, and the target has three simple factors). The same argument applies to so(p,q) and sp(2n,ℝ): their compact subalgebras always have exactly two simple factors. □

**Consequence:** The product structure su(4,2) × su(2)_R is not a workaround — it is the minimal and structurally necessary extension. The physical fact that SU(2)_L and SU(2)_R are independent gauge factors in Pati-Salam is reflected in the algebraic fact that they cannot arise from a single simple UV group.

---

## §6. Minimal Extension: su(4,2) × su(2)_R

**Minimal extension** [STRUCTURAL]:

The minimal semisimple algebra providing the correct compact subalgebra for Pati-Salam is:

    g = su(4,2) × su(2)_R

- su(4,2) compact subalgebra: su(4) ⊕ su(2)_L ⊕ u(1) (19-dim)
- su(2)_R is compact: contributes su(2)_R (3-dim)
- Combined compact subalgebra: su(4) ⊕ su(2)_L ⊕ su(2)_R ⊕ u(1) (22-dim) ← exactly Pati-Salam gauge algebra

**Minimality:** su(4,2) is the established UV algebra for the left-handed sector. SU(2)_R must be added as a compact factor. The smallest compact Lie algebra is su(2) (dimension 3). The product su(4,2) × su(2) is the unique minimal extension adding exactly SU(2)_R.

**Breaking chain with extension** [STRUCTURAL]:

    su(4,2) × su(2)_R  [dim 38]
         ↓  Stage 1: W_decoh on su(4,2) factor
    su(4) ⊕ su(2)_L ⊕ su(2)_R ⊕ u(1)  [dim 22, Pati-Salam gauge algebra]
         ↓  Stage 2: Q₄ commutant filtration
    su(3) ⊕ su(2)_L ⊕ su(2)_R ⊕ u(1)_{B-L}  [dim 15]
         ↓  Stage 3: SU(2)_R × U(1)_{B-L} → U(1)_Y breaking (PS scale)
    su(3) ⊕ su(2)_L ⊕ u(1)_Y  [dim 12, Standard Model]

The three-stage chain (38→22→15→12) is correct and expected. The current two-stage result (35→19→12) is the left-handed truncation: it skips Stage 3 by having SU(2)_R absent from the start.

**The current construction is the left-handed projective truncation of a Pati-Salam-like theory** [STRUCTURAL]. The novel content is the decoherence corridor mechanism deriving the intermediate stage from a non-compact UV algebra. The Pati-Salam structure itself is standard.

---

## §7. What Is Proved vs Conjectural

**[PROVED]** Theorem LH: Q_EM = T₃_L + (1/2)·Q₄ gives exact SM charges for all left-handed doublets.

**[PROVED]** Theorem IL: No SU(2)_R exists in the compact subalgebra, non-compact sector, or Cartan of su(4,2).

**[PROVED]** Theorem No-Go: No simple non-compact algebra has compact subalgebra = Pati-Salam gauge algebra.

**[PROVED]** Theorem RH-Failure: Right-handed charge mismatch is exactly ±1/2 = missing T₃_R eigenvalue.

**[COMPUTED]** Full charge tables for left-handed and right-handed sectors.

**[STRUCTURAL]** Minimal extension: su(4,2) × su(2)_R. The Pati-Salam gauge algebra is the correct intermediate stage.

**[CONJECTURAL]** The three-stage breaking mechanism (Stages 2 and 3 of the extended model) is identified structurally but the specific breaking mechanism at each stage has not been derived from the algebra. In particular, the mechanism selecting T₃_R at the PS scale is open.

**[OPEN]** Whether the THM-561 spectral mechanism (P_+ Hodge alignment) connects to the T₃_L direction selection in EW breaking. If so, an analogous mechanism in the right-handed sector could select T₃_R at the PS scale.

---

## Summary

The ℂ⁶ = V_c(3) ⊕ V_w(2) ⊕ V_s(1) construction on su(4,2) is complete for the left-handed sector and structurally incomplete for the right-handed sector. The incompleteness is not a gap to be patched — it is a structural proof that the construction is the left-handed truncation of a Pati-Salam-like theory. The minimal extension adding SU(2)_R is su(4,2) × su(2)_R, producing the Pati-Salam gauge algebra at the intermediate stage and requiring a third breaking step to reach the SM. The four exact SM charges for left-handed doublets, the exact ±1/2 right-handed mismatch, and the no-go theorem for single UV algebras are all proved results. The three-stage breaking mechanism and the EW direction selection are the next targets.
