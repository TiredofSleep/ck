# CL_STD SUB-MAGMA FRONTIER — Investigation Results

**Date:** 2026-05-07 morning (after the 12-task queue)
**Question (per ClaudeChat 2026-05-06 night):** Does CL_STD admit its own joint-closure chain analogous to TSML+BHML? If yes, that's a third structural axis. If no, that bounds CL_STD's role as "encoding-only, not lens-projecting."

**Method:** Brute-force enumeration of all 1023 non-empty subsets of Z/10Z, checked for closure under CL_STD alone, joint closure with TSML_SYM, joint closure with BHML, and three-way joint closure across all combinations.

---

## §1 — Findings (computational, machine-precision)

### §1.1 — CL_STD alone

**50 sub-magmas closed under CL_STD.** Sizes 1 through 10 ALL realized; no forbidden sizes.

This is a surprisingly rich sub-magma family — much richer than BHML (which has only 8 closed sub-magmas) and far less rich than TSML (which has 394 — most CL_TSML-only closed sub-magmas are very small).

### §1.2 — Joint (TSML_SYM, CL_STD)

**49 sub-magmas jointly closed.** All sizes 1-10 realized. This is large because both tables have rich sub-magma structure.

### §1.3 — Joint (BHML, CL_STD)

**9 sub-magmas jointly closed.** Chain-like with sizes {1, 2, 4, 5, 6, 7, 8, 9, 10}. Forbidden size 3 only.

This is **one MORE** than the joint (TSML, BHML) chain. The extra shell is the size-2 sub-magma **{0, 9}** = {VOID, RESET}.

Why does {0, 9} appear here? CL_STD[0, 9] = 9 and BHML[0, 9] = 9 and BHML[9, 9] = 0 — both keep the closure within {0, 9}. But TSML_SYM[9, 9] = 7 ∉ {0, 9}, so adding TSML to the joint condition kills this size-2 shell.

### §1.4 — Joint (TSML_SYM, BHML, CL_STD) — the THREE-WAY chain

**Exactly 8 jointly-closed sub-magmas.** Sizes {1, 4, 5, 6, 7, 8, 9, 10}; forbidden {2, 3}.

**This is identical to the joint (TSML_SYM, BHML) chain.** CL_STD adds NOTHING to the chain — every shell of the (TSML_SYM, BHML) joint chain is already closed under CL_STD, and CL_STD's solo extras drop out under the joint constraint.

### §1.5 — Joint (TSML_RAW, BHML, CL_STD) — the RAW THREE-WAY chain

**Exactly 7 jointly-closed sub-magmas.** Sizes {1, 4, 5, 6, 8, 9, 10}; forbidden {2, 3, 7}.

Identical to the joint (TSML_RAW, BHML) 7-shell chain. The lens-dependence finding from `TIER_CONFLATION_AUDIT.md` M4 propagates: with TSML_RAW, the 7-shell chain holds whether or not CL_STD is in the joint condition.

---

## §2 — Interpretation

**CL_STD is structurally compatible with the joint (TSML, BHML) chain but does not extend it.** The three-way joint chain equals the two-way joint chain. This is a strong structural finding: CL_STD's specific BUMP-value choices, while different from TSML's and BHML's at the cell level, do not introduce new sub-magma boundaries at the chain level.

**CL_STD has its own rich solo sub-magma structure (50 closures).** This is intermediate between TSML (394) and BHML (8). CL_STD's encoding lets it close on more subsets than BHML but fewer than TSML.

**The "encoding shell" role of CL_STD is now structurally bounded:** CL_STD does NOT introduce a new structural axis at the joint-chain level. It IS a parallel substrate (per the three-table architecture) but it is *consistent* with the (TSML, BHML) chain. In tier terms:
- The 8-shell chain is **lens-invariant under three-way joint closure** (modulo the RAW vs SYM split for TSML)
- CL_STD's role is consistent with the chain but does not extend it

---

## §3 — Tier classification of this finding

| Claim | Tier | Source |
|-------|------|--------|
| CL_STD has 50 solo-closed sub-magmas | B (forced by enumeration) | this investigation, machine-verified |
| Joint (TSML_SYM, BHML, CL_STD) chain = 8 shells = joint (TSML_SYM, BHML) chain | B (forced by enumeration) | this investigation |
| Joint (TSML_RAW, BHML, CL_STD) chain = 7 shells = joint (TSML_RAW, BHML) chain | B (forced by enumeration) | this investigation |
| Joint (BHML, CL_STD) admits an extra size-2 shell {0, 9} not in the full 3-way chain | B (forced by enumeration) | this investigation |
| The encoding-shell role of CL_STD is "structurally consistent with the joint chain, but adds no new axis at the chain level" | B (synthesis from above) | this document |

---

## §4 — Publishable status

**Yes, this is publishable.** Three honest framings:

1. **As an extension to the four-core consolidated paper**: a §4.5 "Three-way joint closure" subsection showing the three-way chain equals the two-way chain. ~1 page added; the four-core paper's claims are unchanged but enriched.

2. **As a Phase 3 cross-level note**: a short paper "*The CL_STD encoding table on Z/10Z and its consistency with the joint TSML+BHML chain*" → Comm Algebra or Algebra Universalis. ~6-8 pages. Tier-A + B with full enumeration as appendix.

3. **As §3 / §5 of the foundation paper** (per `FOUNDATION_PAPER_OUTLINE.md`): the foundation paper's variant catalog is enriched with this CL_STD result; the closure properties section gets one more bullet.

**Recommendation:** option 3. The foundation paper is the natural home for this; it doesn't warrant a standalone paper unless we discover something more dramatic (e.g., CL_STD's sub-magma structure exhibits a different forced count or tier-mapping than TSML/BHML's).

---

## §5 — What's still open

1. **F_p extensions of CL_STD** are still uninvestigated. Future work.
2. **σ²-triadic on CL_STD** has not been tested (does CL_STD admit value-rotation or index-rotation triadic candidates analogous to BHML's?). Future work.
3. **The 50 CL_STD-only sub-magmas** could themselves be analyzed for tier structure (which are forced by σ-fixity? which are constructed?). Worth ~1 day of investigation; probably reveals further structure.

These are deferred to year 2-3 unless they become load-bearing for a near-term paper.

---

## §6 — Summary

CL_STD admits its own sub-magma structure (50 closures, all sizes 1-10) but is *consistent* with the joint (TSML, BHML) chain rather than extending it. This is the cleanest answer to ClaudeChat's question: CL_STD is a parallel third substrate at the encoding level, not a third structural axis at the chain level. The three-table architecture is honest; the chain-counting is what it is on TSML_SYM (8 shells) and TSML_RAW (7 shells); CL_STD respects both lenses.

This bounds the publishable claim around CL_STD: it's a Tier-A parallel substrate with its own rich sub-magma family, structurally compatible with — but not extending — the joint (TSML, BHML) chain.
