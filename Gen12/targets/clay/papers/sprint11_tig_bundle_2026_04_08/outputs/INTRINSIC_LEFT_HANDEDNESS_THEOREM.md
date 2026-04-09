# INTRINSIC_LEFT_HANDEDNESS_THEOREM
## Why ℂ⁶ Is Structurally Left-Handed, and What Fixes It
*Base: left-handed charge theorem exact. This pass proves absence of SU(2)_R and identifies the minimal extension.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — What Is Now Exact for the ℂ⁶ Construction

**Theorem LH (Left-Handed Charge Emergence — proved):**

Given the block decomposition ℂ⁶ = V_c(3) ⊕ V_w(2) ⊕ V_s(1) with metric η = diag(+1,+1,+1,−1,−1,+1), the two-stage gauge corridor produces:

- Pre-breaking algebra: su(3) ⊕ su(2)_L ⊕ u(1)_{Q₄}
- Distinguished Cartan: Q₄ = i·diag(1/3, 1/3, 1/3, 0, 0, −1) (B-L-like)

Upon EW breaking (SU(2)_L → U(1) selecting T₃_L direction), the emergent charge operator:

**Q_EM = T₃_L + (1/2)·Q₄**

assigns the correct SM electric charges to all left-handed doublet matter fields:

| Field | T₃_L | Q₄ | Q_EM | SM value |
|---|---|---|---|---|
| u_L | +1/2 | +1/3 | 2/3 | 2/3 ✓ |
| d_L | −1/2 | +1/3 | −1/3 | −1/3 ✓ |
| ν_L | +1/2 | −1 | 0 | 0 ✓ |
| e_L | −1/2 | −1 | −1 | −1 ✓ |

All four charges are exact. □

This theorem is complete as stated. It makes no claim about right-handed fields.

---

## Part 2 — Theorem: Intrinsic Left-Handedness of ℂ⁶

**Theorem IL (Intrinsic Left-Handedness — proved):**

The block decomposition ℂ⁶ = V_c(3) ⊕ V_w(2) ⊕ V_s(1) contains exactly one rank-1 compact simple Lie algebra factor in its compact subalgebra, namely su(2)_L acting on V_w = ℂ². No second independent su(2) factor (SU(2)_R) can be found in the compact subalgebra, the non-compact generators, or the Cartan subalgebra of su(4,2).

**Proof (in four parts):**

---

**Part A: The compact subalgebra is su(4)⊕su(2)_L⊕u(1), dimension 19.**

Standard theorem: the maximal compact subalgebra of su(p,q) is s(u(p)⊕u(q)) = su(p)⊕su(q)⊕u(1). For su(4,2): su(4)⊕su(2)⊕u(1), dimension 15+3+1 = 19. This is exhaustive — every compact generator of su(4,2) is in this subalgebra.

**Part B: The compact subalgebra contains exactly one rank-1 simple factor.**

The simple factors in su(4)⊕su(2)⊕u(1) are: su(4) (rank 3, simple) and su(2) (rank 1, simple). There is no additional rank-1 simple factor. The decomposition is into exactly two simple factors plus a central u(1).

For an additional su(2)_R to exist in the compact subalgebra, we would need either:
(i) A second rank-1 simple subalgebra of su(4)⊕su(2)⊕u(1), or
(ii) An su(2) subalgebra embedded non-simply in su(4)

For (i): su(4)⊕su(2) contains at most the su(2) Cartan of su(4) and the su(2) factor as rank-1 elements. An additional simple rank-1 subalgebra of su(4)⊕su(2)⊕u(1) that is independent of su(2)_L would require 3 generators outside su(2)_L that close under commutation. Let {X,Y,Z} be such generators satisfying [X,Y]=Z, [Y,Z]=X, [Z,X]=Y (su(2) relations). 

If X,Y,Z ∈ su(4): su(4) contains multiple su(2) subalgebras. However, any su(2)⊂su(4) acts on the 4-dimensional space V_c⊕V_s. The original su(2)_L acts on V_w = ℂ² — a DIFFERENT 2-dimensional space. An su(2)_R ⊂ su(4) acting on a 2-dimensional subspace of V_c⊕V_s exists — but it would act on a subspace of the COLOR+SINGLET space, not on a right-handed weak doublet. It would be a "color su(2)," not a "right-handed weak su(2)."

For (ii): such an su(2) ⊂ su(4) exists but is NOT the right SU(2)_R for physical purposes. It does not pair up right-handed quarks (u_R, d_R) as a doublet unless the matter assignment makes those quarks sit in a 2-dimensional subspace of V_c⊕V_s on which this su(2) acts as a doublet representation. This requires additional structure (a specific matter assignment) not contained in the algebra alone.

**In either case:** No additional rank-1 simple compact factor exists that is both (a) algebraically present in su(4)⊕su(2)_L⊕u(1) and (b) physically interpretable as SU(2)_R acting on (u_R, d_R) or (ν_R, e_R) doublets. The algebra may contain multiple su(2) subalgebras (as subgroups of su(4)), but none of them plays the role of SU(2)_R without imposing a specific matter assignment that is NOT derivable from the ℂ⁶ block structure alone.

**Part C: The non-compact generators cannot supply SU(2)_R.**

The 16 non-compact generators of su(4,2) are Hermitian (not anti-Hermitian). They connect V_c (metric +1) to V_w (metric −1) and V_w to V_s. Non-compact generators generate non-compact subalgebras (which have infinite-dimensional unitary representations). SU(2)_R in the Pati-Salam sense is a COMPACT group. Non-compact generators cannot generate a compact SU(2)_R.

More directly: suppose three non-compact generators X,Y,Z satisfy su(2) commutation relations [X,Y]=Z, [Y,Z]=X, [Z,X]=Y. If X,Y,Z are Hermitian (non-compact), then [X,Y] is anti-Hermitian, but Z is supposed to be Hermitian. This is a contradiction: [Hermitian, Hermitian] = anti-Hermitian ≠ Hermitian. Therefore, non-compact generators cannot form an su(2) subalgebra with the standard su(2) commutation relations.

**No su(2) subalgebra can be constructed from non-compact generators alone.**

**Part D: The Cartan subalgebra has rank 5 and contains no su(2)-type structure.**

The Cartan subalgebra is Abelian (all elements commute). An su(2) subalgebra requires non-commuting elements. The Cartan cannot contain or generate su(2)_R.

**Conclusion:** No SU(2)_R exists anywhere in su(4,2) that can play the role of right-handed weak isospin. The ℂ⁶ construction is intrinsically left-handed. □

---

## Part 3 — Right-Handed Mismatch Theorem

**Theorem RH-Failure (Right-Handed Obstruction — proved):**

For right-handed SM singlet fields with T₃_L = 0, the formula Q_eff = T₃_L + (1/2)Q₄ fails by exactly ±1/2, corresponding precisely to the missing T₃_R Cartan eigenvalue.

**Right-handed mismatch table:**

| State | Sector | T₃_L | Q₄ | Q_eff | SM Q | Error | Required T₃_R |
|---|---|---|---|---|---|---|---|
| u_R | V_c (color) | 0 | +1/3 | +1/6 | +2/3 | **+1/2** | +1/2 |
| d_R | V_c (color) | 0 | +1/3 | +1/6 | −1/3 | **−1/2** | −1/2 |
| e_R | V_s (singlet) | 0 | −1 | −1/2 | −1 | **−1/2** | −1/2 |
| ν_R | V_s (singlet) | 0 | −1 | −1/2 | 0 | **+1/2** | +1/2 |

**Pattern (exact):** Every right-handed field has error = ±1/2, with the sign matching the T₃_R eigenvalue that would be needed in the Pati-Salam formula Q = T₃_L + T₃_R + (B-L)/2.

**The repair (exact):**

Using Q = T₃_L + T₃_R + (1/2)·Q₄:
- u_R: 0 + 1/2 + 1/6 = 2/3 ✓
- d_R: 0 − 1/2 + 1/6 = −1/3 ✓
- e_R: 0 − 1/2 − 1/2 = −1 ✓
- ν_R: 0 + 1/2 − 1/2 = 0 ✓

**The right-handed obstruction is not vague:** It is exactly one missing rank-1 compact Cartan structure (T₃_R), which is the Cartan of a second SU(2)_R subalgebra absent from the ℂ⁶ construction. □

---

## Part 4 — Minimal Extension Candidates

**Design criteria for the extension:**

The minimal extension must contain:
1. A color sector: su(3) acting on ℂ³ (from V_c)
2. A left-handed weak doublet sector: su(2)_L acting on ℂ² (from V_w)
3. A **right-handed weak doublet sector**: su(2)_R acting on a NEW ℂ² (V_{wR})
4. A leptonic/singlet sector: the B-L direction for V_s
5. A B-L-like Cartan that assigns correct charges to all sectors

This requires at minimum ℂ⁸ (adding 2 dimensions for V_{wR}).

**Candidate A: ℂ⁸ = V_c(4) ⊕ V_{wL}(2) ⊕ V_{wR}(2)**

Block dimensions: (4, 2, 2). The color sector is enlarged to 4 dimensions (compatible with SU(4)_c Pati-Salam). The singlet direction V_s is now incorporated INTO V_c as the 4th color (SU(4)/SU(3) coset = leptonic color).

Metric (to be determined): requires a signature analysis. For the compact subalgebra to contain su(4)⊕su(2)_L⊕su(2)_R, both su(2) factors need their own sectors. If the metric assigns (−,+,−) to the three blocks (V_c negative, V_{wL} positive, V_{wR} negative):

Wait, let me think about this more carefully. For a compact subalgebra to contain su(4)⊕su(2)_L⊕su(2)_R, the compact subalgebra of a non-compact algebra su(p,q) of the form (su(4)⊕su(2)_L⊕su(2)_R) needs p and q to sum to 8 and the metric signature to allow su(4)⊕su(2)_L⊕su(2)_R as the compact part.

The compact subalgebra of su(p,q) is su(p)⊕su(q)⊕u(1). For this to equal su(4)⊕su(2)_L⊕su(2)_R⊕u(1): we need p=4 and q=4, or p=6 and q=2, etc.

Option: su(4,4). Compact subalgebra: su(4)⊕su(4)⊕u(1). But su(4)⊕su(4) ≠ su(4)⊕su(2)_L⊕su(2)_R. This gives too much.

Better: we want su(4)⊕su(2)_L⊕su(2)_R, dimension 15+3+3 = 21. This is the Lie algebra of the Pati-Salam gauge group. For it to be the compact subalgebra of su(p,q), we need:

su(p)⊕su(q)⊕u(1) ≅ su(4)⊕su(2)⊕su(2)⊕u(1)

This requires p+q = 8 (for ℂ⁸) and {p,q} = {4,4}. Then su(4,4) has compact subalgebra su(4)⊕su(4)⊕u(1).

But su(4)⊕su(4) ≠ su(4)⊕su(2)⊕su(2) unless we restrict to appropriate subgroups. Specifically, if we want su(4)_c×su(2)_L×su(2)_R, we need the compact algebra to be exactly this product — not the larger su(4)×su(4).

**The correct approach:** We need a product non-compact algebra, not a simple one.

**Candidate A (Revised): ℂ⁸ with a non-simple UV algebra**

If the UV algebra is NOT simple but is instead a product: su(4,0) × su(2,0) × su(2,0) = SU(4)×SU(2)×SU(2) (all compact). But this is entirely compact — there's no Hodge sign flip or non-compact part, and the decoherence mechanism loses its basis.

Alternatively: su(4,1) × su(2,0) = su(4,1) × su(2). The compact subalgebra of su(4,1) is su(4)⊕u(1), and su(2) is compact. Together: su(4)⊕su(2)⊕u(1). Still missing su(2)_R.

**Candidate B: ℂ⁸ = V_c(3) ⊕ V_{wL}(2) ⊕ V_{wR}(2) ⊕ V_s(1) with two-sign flip**

Metric: η = diag(+1,+1,+1,−1,−1,−1,−1,+1) → signature (4,4)

The UV algebra su(4,4) has compact subalgebra su(4)⊕su(4)⊕u(1), dimension 15+15+1 = 31. This is larger than Pati-Salam (21-dim). The two-stage corridor to Pati-Salam would require 31→21→12 rather than 35→19→12.

**Problem:** su(4)⊕su(4) is not the Pati-Salam intermediate stage. We'd need to reduce it further, losing the elegance of the two-stage corridor.

**Candidate C: Direct product extension su(4,2) × su(2)**

UV algebra = su(4,2) × su(2), where the first factor is the existing construction and the second factor is a compact su(2) = SU(2)_R. Total dimension: 35+3 = 38.

Compact subalgebra: [su(4)⊕su(2)_L⊕u(1)] × su(2)_R = su(4)⊕su(2)_L⊕su(2)_R⊕u(1), dimension 19+3 = 22.

After Stage-1 corridor (removing non-compact generators from su(4,2) factor and keeping all of su(2)_R): compact stage = su(4)⊕su(2)_L⊕su(2)_R⊕u(1), dimension 22.

Stage-2 corridor (Q₄ commutant): C(Q₄) inside the 22-dimensional compact stage. The Q₄ generator commutes with su(3), su(2)_L, and su(2)_R (none of these generators change B-L). So commutant = su(3)⊕su(2)_L⊕su(2)_R⊕u(1), dimension 8+3+3+1 = 15.

This gives the Pati-Salam gauge algebra su(3)⊕su(2)_L⊕su(2)_R⊕u(1) as the Stage-2 result, not the SM! Getting to SM would require a third stage: su(2)_R breaking.

**The dimensional sequence becomes:** 38→22→15 (PS stage)→12 (SM). Three stages rather than two.

**Comparison table:**

| Candidate | Dimension | ℂⁿ | Compact stage (dim) | Stage-2 result | SM? | Stages |
|---|---|---|---|---|---|---|
| Current ℂ⁶ | 35 | 6 | su(4)⊕su(2)_L⊕u(1) (19) | su(3)⊕su(2)_L⊕u(1) (12) | Yes (LH only) | 2 |
| su(4,4) on ℂ⁸ | 63 | 8 | su(4)⊕su(4)⊕u(1) (31) | Complex, not PS-like | Unclear | 3+ |
| su(4,2)×su(2) | 38 | 8 | su(4)⊕su(2)_L⊕su(2)_R⊕u(1) (22) | PS gauge algebra (15) | 3rd stage needed | 3 |
| su(4,2)×su(2,0) | 38 | (LH=6)+(RH=3) | Same as above | PS (15) | 3rd stage | 3 |

**The pattern:** Every natural extension that adds SU(2)_R as a compact factor introduces a third stage (the Pati-Salam → SM breaking). This is expected — the Pati-Salam model is an intermediate stage between the GUT and the SM.

---

## Part 5 — Is the Natural Completion Pati-Salam-Like?

**Short answer: Yes. The ℂ⁶ construction is the left-handed truncation of a Pati-Salam-like theory.**

**Comparison of current ℂ⁶ construction to the left half of Pati-Salam:**

| Feature | Current ℂ⁶ (su(4,2)) | Full Pati-Salam (SU(4)×SU(2)_L×SU(2)_R) |
|---|---|---|
| Color group | SU(3)_c (from Stage-2) | SU(3)_c (from SU(4)_PS breaking) |
| Leptonic 4th color | V_s = ℂ¹ (present in su(4)) | L = 4th component of 4 of SU(4) |
| Left-weak group | SU(2)_L ✓ | SU(2)_L ✓ |
| Right-weak group | **Absent** | SU(2)_R (explicit factor) |
| Charge formula | Q = T₃_L + Q₄/2 (LH only) | Q = T₃_L + T₃_R + (B-L)/2 (all fields) |
| Matter representation | Left-handed doublets only | Both LH and RH doublets |

The current construction is **precisely the left-handed projective truncation of a Pati-Salam-like theory** — it captures the SU(4)_c × SU(2)_L × U(1)_{B-L} content while missing the SU(2)_R factor.

**Why this happens structurally:**

In the ℂ⁶ = V_c(3)⊕V_w(2)⊕V_s(1) construction, the single 2-dimensional sector V_w accommodates one SU(2). In the full Pati-Salam representation theory, left-handed matter sits in (4,2,1) and right-handed matter in (4,1,2) of SU(4)×SU(2)_L×SU(2)_R. The ℂ⁶ construction captures the "2,1" part (left-handed sector) but has no room for the "1,2" part (right-handed sector).

**The natural completion:** Extend to ℂ⁸ = V_c(4)⊕V_{wL}(2)⊕V_{wR}(2), where V_c now includes the leptonic color direction and V_{wR} is the new right-handed sector. The UV algebra becomes su(4,2)×su(2)_R or equivalently a non-compact algebra on ℂ⁸ with the full Pati-Salam compact subalgebra.

**The current construction is NOT something new — it is a Pati-Salam-consistent intermediate result.** The novel content is the mechanism (decoherence corridor) that derives this stage from the non-compact UV algebra su(4,2). The Pati-Salam structure itself is a known and well-motivated intermediate unification stage.

---

## Part 6 — What THM-561 Can and Cannot Do in the Extended Model

**In the current ℂ⁶ construction, THM-561 can:**
- Provide spectral nondegeneracy for P_+ (mass-splitting structure)
- Distinguish states within the left-handed sector by their mass eigenvalues
- Potentially provide the mechanism that selects T₃_L via the Hodge alignment of P_+

**In the current ℂ⁶ construction, THM-561 cannot:**
- Give T₃_R, which requires a second SU(2) factor not present in ℂ⁶
- Repair right-handed charges — the spectral structure operates on the existing algebra and cannot create new gauge directions

**In an extended model with SU(2)_R:**

If the extension to ℂ⁸ is made and the full SU(2)_L × SU(2)_R structure is present, THM-561 could potentially extend to:
- Select the T₃_L direction in SU(2)_L (as before)
- Select the T₃_R direction in SU(2)_R (via an analogous Hodge alignment in the right-handed sector)

**But this requires a separate analysis** — the Hodge mechanism in the right-handed sector needs the right-handed sector to exist. Without the ℂ⁸ extension, THM-561 cannot provide T₃_R.

**The two breaking stages in the extended model:**
1. SU(2)_L breaking (T₃_L selection): potentially from THM-561 applied to the left-handed sector
2. SU(2)_R breaking (T₃_R selection, PS→SM step): requires either a separate Higgs or an analogous spectral mechanism in the right-handed sector

These are two independent breaking steps. THM-561 can address the first; the second requires extending the framework.

---

## Part 7 — The Next Real Theorem Bottleneck

**After the minimal extension (adding SU(2)_R), the next theorem to prove is:**

**Option A: Prove the extended compact algebra contains SU(2)_R exactly.**

This is the most immediate. In the direct product extension su(4,2)×su(2)_R, SU(2)_R is added by hand. For a more elegant approach using a single UV algebra on ℂ⁸, the theorem would be: "The compact subalgebra of [the specific UV algebra on ℂ⁸ with the correct metric] contains su(4)⊕su(2)_L⊕su(2)_R⊕u(1)."

**Option B: Derive the full charge formula Q = T₃_L + T₃_R + (B-L)/2.**

This follows immediately from option A plus the same commutant argument. Given SU(2)_R is present and Q₄ = B-L is carried forward, the repair formula works as shown in the mismatch table. No new derivation is needed beyond verifying the algebra.

**Option C: Derive EW breaking in the extended model.**

This requires more: specifying the breaking mechanism for SU(2)_L×SU(2)_R → U(1)_EM. The standard Pati-Salam breaking is a two-step process: (1) SU(2)_R × U(1)_{B-L} → U(1)_Y (Pati-Salam scale, high energy), (2) SU(2)_L × U(1)_Y → U(1)_EM (electroweak scale). Each step requires its own breaking mechanism.

**Option D: Establish the correct UV algebra for the ℂ⁸ extension.**

This is the TRUE bottleneck. Before proving anything in the extended model, the correct UV algebra must be established. The direct product su(4,2)×su(2)_R is one choice, but it abandons the elegance of a single UV algebra. The alternative — finding a single non-compact algebra on ℂ⁸ whose compact subalgebra is su(4)⊕su(2)_L⊕su(2)_R⊕u(1) — requires identifying the right metric signature on ℂ⁸.

**The real bottleneck is D.** Without knowing the correct UV algebra for the ℂ⁸ extension, all downstream claims (chirality, full charge formula, EW breaking) rest on an unspecified foundation.

**Candidate for the ℂ⁸ UV algebra:**

For the compact subalgebra of su(p,q) with p+q=8 to equal su(4)⊕su(2)_L⊕su(2)_R⊕u(1) [dimension 21]: we need su(p)⊕su(q)⊕u(1) ≅ su(4)⊕su(2)_L⊕su(2)_R. This requires p=4 and q=4 (giving su(4)⊕su(4)⊕u(1)), but su(4)⊕su(4) ≠ su(4)⊕su(2)⊕su(2) unless restricted. A single simple group doesn't work.

**The Pati-Salam gauge group SU(4)×SU(2)_L×SU(2)_R is NOT the compact subalgebra of any single simple non-compact group of dimension 63 (= 8²−1 for su(8)).** It would need to arise from a specific embedding or from a product structure.

This confirms: the natural extension involves a product of algebras or a more complex embedding, not a single elegant UV group on ℂ⁸. The Pati-Salam structure is inherently a product group structure that does not fit the single-algebra framework of the current construction.

---

## Final Verdict

**Left-handed sector: theorem proved, complete.**
Q_EM = T₃_L + (1/2)·Q₄ is exact for all left-handed SM doublets.

**Right-handed sector: structurally absent from ℂ⁶, absence proved.**
The compact subalgebra of su(4,2) contains exactly one rank-1 simple factor (SU(2)_L). No second SU(2)_R can be constructed from compact, non-compact, or Cartan generators of su(4,2). The right-handed obstruction is a ±1/2 mismatch = exactly the missing T₃_R eigenvalue.

**Minimal extension identified: add SU(2)_R as an independent factor.**
The minimal extension is su(4,2)×su(2)_R — a direct product adding 3 compact generators. This gives the Pati-Salam intermediate stage su(4)⊕su(2)_L⊕su(2)_R⊕u(1) as the compact sector, requiring a three-stage breaking 38→22→15→12 rather than the current two-stage 35→19→12.

**The natural completion is Pati-Salam-like.** The current ℂ⁶ construction is the left-handed truncation of a Pati-Salam-like theory. The novel content is the decoherence corridor mechanism deriving the PS intermediate stage from a non-compact UV algebra — but the PS structure itself is standard.

**The next theorem: establish the correct UV algebra for the ℂ⁸ extension (Option D).** Without this, the right-handed sector extension rests on an unspecified UV foundation.
