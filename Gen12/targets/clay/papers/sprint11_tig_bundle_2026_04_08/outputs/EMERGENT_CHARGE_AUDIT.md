# EMERGENT_CHARGE_AUDIT
## Pre-Breaking Conserved Structure vs Post-Breaking Emergent Electric Charge
*Base: su(4,2) corridor to SM gauge algebra established. This pass audits the charge emergence claim.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — Status Table: What Is Exact vs Structural vs Open

| Claim | Status | Reason |
|---|---|---|
| dim Comm(T, S, SU(3)) = 2 | **Structural** — consistent with algebra, needs T specified | The commutant of SU(3) in the compact stage has rank ≥ 2 from the Cartan structure; the exact count depends on what T is |
| Unique vacuum-neutral conserved direction exists | **Exact** (given Q₄ identification) | Q₄ satisfies neutrality on vacuum and is uniquely determined by conditions 1+2+3 + tracelessness |
| This operator is scalar on V_{1/2} | **Exact by Schur's lemma** | V_{1/2} is an SU(2) irrep (doublet); any operator commuting with SU(2) acts as a scalar on irreps |
| It distinguishes color (V_c) from non-color (V_w, V_s) | **Exact** | Q₄ assigns eigenvalue +1/3 to V_c directions, 0 to V_w, −1 to V_s |
| It is baryon number B | **Interpretive** — correctly labeled B-L, not B alone | Q₄ assigns 1/3 to V_c (quark-like) and −1 to V_s (lepton-like) and 0 to V_w. This is B-L, not pure B. |
| Hypercharge Y is already present pre-breaking | **Incorrect in this framework** | Y assigns non-zero values to V_w; Q₄ assigns 0 to V_w. The pre-breaking neutral charge is B-L, not Y. |
| T₃ is absent from the commutant | **Structural** — T₃ commutes with Q₄ but may not commute with T | T₃ commutes with Q₄ (by construction of conditions 1+2+3). If T₃ does not commute with some additional operator T (from THM-561), that must be specified separately. |
| Q_EM is emergent only after EW breaking | **Correct and important** | Q_EM = T₃ + Y/2, but Y ≠ Q₄ for all sectors. The combination only becomes defined post-breaking. |

**Key correction:** The pre-breaking neutral charge is **B-L** (baryon minus lepton), not pure B. Q₄ assigns 0 to V_w and −1 to V_s. If V_s = lepton direction, the charge is B-L with B-L = 1/3 for quarks and −1 for leptons. Calling it simply "baryon number B" misses the lepton number contribution.

---

## Part 2 — The Surviving Neutral Operator: Exactly What It Is

### Explicit Form

Q₄ = i·diag(q, q, q, 0, 0, α) in the 6×6 basis V = V_c(3) ⊕ V_w(2) ⊕ V_s(1)

where α = −3q by tracelessness (forced), and q = 1/3 by the per-direction normalization convention.

**Explicit action on subspaces (exact):**

**On V₁ (vacuum — in this context, the zero-energy sector):**
If the vacuum state is in the singlet direction V_s: Q₄·|vac⟩ = i·(−1)·|vac⟩. The vacuum is NOT Q₄-neutral if |vac⟩ ∈ V_s.

**Clarification needed:** The claim "vacuum-neutral" requires specifying what the "vacuum" is. If V₁ represents a 1-dimensional ground state in the abstract sector corresponding to the V_s direction, then Q₄ = −1 there, which is not neutral. For Q₄ to be "vacuum-neutral," the vacuum must live in V_w (Q₄ = 0) or in a sector where Q₄ = 0.

**This is a potential inconsistency in the collaborator's framing.** If the vacuum is associated with V_s (the lepton direction) and Q₄ assigns −1 there, Q₄ is NOT vacuum-neutral. If the vacuum is in V_w (the weak sector, Q₄ = 0), then Q₄ is vacuum-neutral on that sector. This needs clarification.

**On V_{1/2} (weak doublet sector = V_w):**

Q₄ acts as i·0·I₂ = 0 on V_w. It assigns zero eigenvalue to ALL weak doublet directions equally. Schur's lemma: any U(1) generator commuting with SU(2) is scalar on a doublet. Q₄ is scalar on V_w (trivially — it assigns eigenvalue 0). ✓

**On V_{1/3} (color sector = V_c):**

Q₄ acts as i·(1/3)·I₃ on V_c. It assigns eigenvalue +1/3 to all three color directions equally. Scalar on V_c (it assigns equal charge to R, G, B). ✓

**On V_s (singlet sector):**

Q₄ acts as i·(−1)·1 on V_s. Eigenvalue −1 on the singlet.

### Is "Baryon Number B" the Right Label?

**Correct label: B−L (baryon minus lepton), not pure B.**

Reason: Pure baryon number B assigns B = 1/3 to quarks, B = 0 to leptons. Q₄ assigns:
- V_c direction: charge +1/3 ≈ B(quark) per quark direction ✓ (consistent with B)
- V_s direction: charge −1 ≈ B(lepton) − L(lepton) = 0 − 1 = −1 (consistent with B-L, NOT with pure B which would be 0)

If V_s = lepton direction: Q₄ = B − L for the specific matter content where V_c carries quarks and V_s carries leptons. Pure B would assign 0 to V_s, but Q₄ assigns −1.

**The honest label is B-L. Calling it "baryon number" understates the content.**

### Is the Normalization Fixed?

The normalization of Q₄ has two independent aspects:
- The eigenvalue ratio 1:−3 is algebraically **fixed** (tracelessness + dim(V_c) = 3)
- The overall scale (q = 1/3 per quark direction) is a **normalization convention** (choosing the unit of charge)

The statement "normalization is fixed" is partially correct: the *relative* normalization (1/3 per quark direction, −1 on the lepton direction) follows from tracelessness given the matter interpretation. The *absolute* normalization (the choice of unit) is conventional.

---

## Part 3 — Which Charges Exist Before EW Breaking?

### Pre-Breaking Conserved Charges

In the compact subalgebra su(4)⊕su(2)⊕u(1) (the Stage-1 IR algebra), the conserved charges are:

**Exact pre-breaking charges:**

1. **SU(3) generators (8):** The full color algebra is conserved. Color charge is a pre-breaking symmetry.
2. **SU(2)_L generators (3):** The weak isospin algebra is conserved as a FULL ALGEBRA (not just T₃). SU(2) is unbroken in the pre-breaking phase.
3. **Q₄ (= B-L-like) (1):** The unique Cartan generator commuting with SU(3) and SU(2) — the "neutral" pre-breaking U(1).
4. **Second U(1) (1):** A second independent U(1) exists (there are 5 Cartan generators in su(4,2), and after Stage 1, the compact sector has rank 5 with multiple U(1)s).

**Why T₃ as a standalone charge is absent:**

In the pre-breaking phase, SU(2) is a full symmetry. T₃ is NOT a conserved charge by itself — it is a generator of the FULL SU(2), and the full SU(2) symmetry means no preferred T₃ direction exists. Selecting T₃ as "the" conserved charge requires picking a direction in SU(2) space, which is exactly what EW breaking does.

More precisely: in the unbroken phase, all SU(2) directions are equivalent by the SU(2) symmetry. The operators T₁, T₂, T₃ are all generators of an unbroken symmetry. Saying "T₃ is a conserved charge" in the pre-breaking phase would mean T₃ is preserved but T₁ and T₂ are not — which would itself be a symmetry breaking.

**The important distinction:**

- Pre-breaking: SU(2) symmetry conserved → no preferred T₃ → no Q_EM defined
- Post-breaking: SU(2) → U(1) breaking selects a T₃ direction → Q_EM = T₃ + (B-L)/2 is defined

**What "Q_EM emerges" means in this framework:**

EW breaking selects a direction in SU(2) space (call it T₃). Combined with the pre-existing B-L-like charge (Q₄), the combination Q_EM = T₃ + Q₄/2 becomes a well-defined conserved charge of the broken phase. Before breaking, neither T₃ alone nor Q_EM is a meaningful charge — only the full SU(2) algebra plus Q₄ are conserved.

---

## Part 4 — Mass Emergence Is Not Charge Emergence

THM-561 (as referenced by the collaborator): P_+ has spectral nondegeneracy and Hodge alignment, allowing a mass split.

**The distinction (exact):**

**Mass emergence:** The P_+ projector, with spectral nondegeneracy, allows distinguishing states by energy/mass. The specific mass split pattern is determined by the Hodge alignment. This is a spectral result — it tells you that different sectors of the Hilbert space (or mode space) have different eigenvalues under some self-adjoint operator.

**Charge emergence:** A conserved U(1) charge operator Q_EM that commutes with the IR Hamiltonian/dynamics. This requires both:
(a) A surviving U(1) symmetry after breaking
(b) The specific operator Q_EM = T₃ + Y/2 (or its analog)

**Why these are separate:**

THM-561 gives a mechanism for mass splitting via spectral structure. This means states can be labeled by mass — but mass is not charge. Electric charge is a separate conserved quantum number associated with a different symmetry (U(1)_EM).

To go from mass splitting to charge definition:
1. Mass splitting (THM-561): establishes that different sectors have different spectral weights → particles can have different masses ✓
2. Charge emergence (this audit): establishes what Q_EM is after breaking → still requires the EW breaking mechanism and the T₃ selection

**They are related:** The breaking that produces mass splitting also selects a T₃ direction, and that same breaking defines Q_EM. But the mathematical content of each derivation is distinct. Mass splitting requires spectral nondegeneracy; charge emergence requires a surviving U(1) symmetry and its identification.

---

## Part 5 — The Minimal Broken-Phase Charge Formula

### Derivation Attempt

After EW breaking (SU(2)_L × U(1)_{B-L} → U(1)_EM), the surviving charge operator Q_EM on the weak sector is determined by:

1. The breaking selects a T₃ direction in SU(2).
2. The pre-breaking neutral charge Q₄ (= B-L-like) remains conserved.
3. Q_EM must commute with the IR Hamiltonian (after breaking).

**Candidate formula:** Q_EM = T₃ + c · Q₄

**Testing c for different matter sectors:**

For V_c (quarks), the doublet structure gives (u_L, d_L) with T₃ = ±1/2 and Q₄ = +1/3:
- Q_EM(u_L) = 1/2 + c/3 must equal 2/3 → c = 1/2
- Q_EM(d_L) = −1/2 + c/3 must equal −1/3 → c = 1/2 ✓

For V_s (lepton), a doublet (ν_L, e_L) with T₃ = ±1/2 and Q₄ = −1:
- Q_EM(ν_L) = 1/2 + c·(−1) must equal 0 → c = 1/2 ✓
- Q_EM(e_L) = −1/2 + c·(−1) must equal −1 → c = 1/2 ✓

**The formula Q_EM = T₃ + (1/2)·Q₄ works for ALL left-handed doublets with c = 1/2.**

This is exactly the SM Gell-Mann-Nishijima formula with Y = Q₄ (B-L charge) for left-handed doublets.

### Where the Formula Fails

For right-handed singlets (T₃ = 0):
- Q_EM(u_R) = 0 + (1/2)·Q₄(u_R). If Q₄(u_R) = 1/3 (baryon number), Q_EM = 1/6 ≠ 2/3.
- Q_EM(e_R) = 0 + (1/2)·Q₄(e_R). If Q₄(e_R) = −1 (lepton number), Q_EM = −1/2 ≠ −1.

**The formula fails for right-handed singlets.**

**Why:** Right-handed singlets in the SM have hypercharge charges that are NOT equal to B-L. For the SM, Y(u_R) = 4/3 ≠ B-L(u_R) = 1/3. The SM hypercharge for right-handed fields includes an additional contribution from SU(2)_R isospin (in the Pati-Salam language: Y = (B-L) + 2·T₃_R).

**In the current construction:** V_w = ℂ² only accommodates doublets (SU(2)-irreps of dimension 2). Right-handed singlets would need to sit in V_c or V_s as singlets under SU(2). For V_c right-handed quarks: Q₄ = 1/3, T₃ = 0 → Q_EM = 1/6 ≠ 2/3. The formula does not reproduce the right-handed quark charges.

**The honest verdict on the charge formula:**

> Q_EM = T₃ + (1/2)·Q₄ correctly reproduces SM electric charges for left-handed doublets only. For right-handed singlets, additional structure (equivalent to SU(2)_R isospin in Pati-Salam) is required.

---

## Part 6 — Is This "Exactly the SM Structure"?

**Verdict: Partial analog — not exact match.**

**What matches:**

- Q₄ (B-L) plays the role of Y for left-handed doublets (since Y = B-L for SM doublets)
- The formula Q_EM = T₃ + (1/2)·Q₄ correctly gives SM charges for ν_L, e_L, u_L, d_L
- Q_EM emerges as a post-breaking combination of T₃ and a pre-existing U(1), which is structurally the same as the SM

**What does not match:**

- The SM has hypercharge Y as a pre-breaking gauge symmetry; here the pre-breaking U(1) is B-L
- In the SM, Y ≠ B-L for right-handed fields (Y(u_R) = 4/3 ≠ B-L(u_R) = 1/3)
- The current construction does not have SU(2)_R or a right-handed sector that would give the correct hypercharges for right-handed singlets
- The SM gauge group at the Lagrangian level is SU(3)×SU(2)_L×U(1)_Y (not SU(3)×SU(2)_L×U(1)_{B-L})

**The correct framing:**

The construction gives a pre-breaking structure where B-L plays the role of hypercharge for doublets. This is consistent with the SM at the level of left-handed fields, which is the primary sector. The right-handed sector requires additional ingredients beyond what the current construction provides.

In Pati-Salam language: the current construction reaches SU(4)_c × SU(2)_L × U(1)_{B-L} (or similar), which is an intermediate stage. The full SM with the correct hypercharge for all fields requires SU(4)_c × SU(2)_L × SU(2)_R, followed by SU(2)_R breaking. The current construction has completed one step of this breaking but not the second.

---

## Part 7 — The Next Real Theorem

**What is already shown:**

1. The pre-breaking algebra contains Q₄ (B-L-like) and SU(2)_L as the neutral U(1) and weak symmetry.
2. After a T₃ direction is selected (by EW breaking), Q_EM = T₃ + (1/2)·Q₄ gives correct SM charges for left-handed doublets.
3. Q_EM is not a pre-breaking charge — it requires the breaking.

**What is missing:**

1. A derivation of the EW breaking mechanism itself (which selects the T₃ direction). Currently, this is assumed to happen; the mechanism is not derived.
2. The right-handed sector: how do right-handed quarks and leptons enter the construction with the correct hypercharges? This requires either SU(2)_R structure or an additional U(1) beyond Q₄.
3. The explicit connection between THM-561 (mass splitting) and the selection of the T₃ direction.

**The theorem to prove next:**

Given the Stage-1 algebra su(4)⊕su(2)⊕u(1) with Q₄ as the distinguished pre-breaking neutral charge, the broken-phase algebra (after SU(2)_L → U(1)_T₃) defines an electromagnetic charge operator Q_EM = T₃ + (1/2)·Q₄ that:
- Is conserved in the broken phase
- Correctly assigns SM electric charges to all left-handed SM fields

**The lemma needed to close it:**

The EW breaking must be derived as a mechanism that:
(a) Selects a specific T₃ direction within SU(2) (spontaneous breaking of SU(2)_L)
(b) Leaves Q₄ unchanged (B-L conservation)
(c) Produces exactly the combination Q_EM = T₃ + (1/2)·Q₄ as the surviving U(1)

This is a Higgs-like mechanism at the EW scale — or an analog of it within the current framework.

---

## Summary

### What Exists Pre-Breaking

- SU(3) color symmetry (exact)
- SU(2)_L weak isospin algebra (exact, full algebra — no preferred T₃ direction)
- Q₄ = B-L-like Cartan charge (exact: +1/3 on V_c, 0 on V_w, −1 on V_s)

**What does NOT exist pre-breaking:** T₃ as an isolated conserved charge, electric charge Q_EM, hypercharge Y as a separate entity from B-L (for doublets)

### What Emerges Only After Breaking

- A preferred T₃ direction (from SU(2)_L breaking)
- Q_EM = T₃ + (1/2)·Q₄ as a conserved electromagnetic charge
- The distinction between up-type and down-type particles (T₃ = ±1/2)

**Correct for left-handed doublets; incomplete for right-handed singlets.**

### Is the Surviving Neutral Operator Really Baryon Number?

**No. It is B-L (baryon minus lepton number).** Q₄ assigns:
- +1/3 to V_c (quark-like) ← consistent with B(quark) = 1/3
- 0 to V_w (weak sector) ← consistent with B-L = 0 for lepton doublets only if L=0 there
- −1 to V_s (singlet) ← consistent with L(lepton) = 1, B-L = −1

The nonzero value on V_s (the leptonic singlet direction) is the key: pure baryon number B would assign 0 to V_s, but Q₄ assigns −1. Q₄ is B-L, not B.

### What Remains to Derive Q_EM

1. The mechanism selecting T₃ (EW breaking at the SU(2)_L scale)
2. The right-handed sector (SU(2)_R or equivalent to give correct Y for right-handed fields)
3. The connection between THM-561 mass splitting and the T₃ direction selection
