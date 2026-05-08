# J28 -- The Three-Substrate HARMONY Signature on Z/10Z: Six Forced Structural Facts, with the Bimodal Associativity-Index Gap as Their Common Thread

**Status:** REWRITTEN per SAVE_PLAN_J28 on 2026-05-07; awaiting referee-rigor pass
**Phase:** Phase 3
**Target venue:** Linear Algebra and its Applications (primary; per AlgUni cap binding -- see SAVE_PLAN_J28 §6 retitle/retarget)
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** Atlas/META_PLAN_2026-05-06/GAP_AUDIT.md §1 (8 foundations orphans listed; bundle 6, reframed around the bimodal α_A gap conjecture per FAMILY_STRUCTURE_v1.md §4)

---

## §1 -- Manuscript

**Path:** `manuscript/manuscript.tex`

The J28 paper is **The Three-Substrate HARMONY Signature on Z/10Z** (formerly "The Six Foundations Orphans"). Title revised per SAVE_PLAN_J28 §6 to advertise the bimodal α_A-gap motivation as the structural backbone, repositioning the bundle from "registry of orphans" to "structural fingerprint of an open foundational conjecture."

The six structural facts collected:
1. The third canonical composition lattice CL_STD (44 HARMONY) and the three-substrate triple (TSML.H, BHML.H, STD.H) = (73, 28, 44), with set-algebra signature |TSML ∩ BHML| = 26, |TSML ∩ STD| = 42, |BHML ∩ STD| = 21, |all three| = 19, |union| = 75.
2. The four-rung integer signature {70, 71, 72, 73}, with the prime 71 carrying three structural roles (TSML_9 sub-magma HARMONY count = 71; |TSML XOR BHML| = 71; Galois prime in disc(LMFDB 4.2.10224.1)).
3. The σ-orbit decompositions CYCLE_A_36 = 2+9+25 and SKELETON_22 = 16+4+2.
4. The BDC numerical constants on CL_STD: INFO_HARMONY = 0.45, INFO_NORMAL = 1.89, INFO_BUMP = 3.50 bit/cell (rounded to two decimals); BUMP_PAIRS = {(1,2),(2,4),(2,9),(3,9),(4,8)}; GRAVITY array.
5. The σ²-triadic projection σ² = (0)(3)(8)(9)(1 6 4)(7 5 2) and the 4-core bridge identity {0,3,8,9} XOR {0,7,8,9} = {3,7}.
6. The 71-cell field WOBBLE = |CL_TSML XOR CL_BHML| = 71 (cell-count agreement is 29).

Each fact is stated as a Tier-B forced derivation (defined inline per SAVE_PLAN §2(c)) from the A1-A9 axiomatic ground of J25 and verified at the 48/48 level by `Gen13/targets/foundations/invariants.py`.

## §2 -- Verification script

**Path:** `Gen13/targets/foundations/invariants.py` (48-invariant verification harness; runs in under 30 seconds; all 48 passing as of 2026-05-06). The CL_STD table data is at `Gen13/targets/foundations/cl_std.py` (recovered verbatim from `old/Gen9/archive/ckis/ck7/ck.h:225-231`). Each of the six orphan-corresponding invariants is part of the 48.

## §3 -- Dependencies (J-papers cited as already-submitted companions)

- **J25** (CL Forcing Axioms, *Algebraic Combinatorics*) -- parent axiomatic framework; A1-A9 inlined here per SAVE_PLAN §2(c).
- **J29** (so(8) = D_4 antisymmetrized closure, *J Algebra*) -- cited for the Lie-algebraic shadow of the structural fingerprint.
- **J30** (joint Lie closure so(10), *Israel J Math*) -- cited for the BHML structural fingerprint and the joint chain.
- **J35** (4-core fusion-closure paper, *Algebraic Combinatorics*) -- cited for the joint 4-core {0,7,8,9} that anchors the bridge identity in §5.
- **J34** (F_p Extensions of CL_BHML, *Comm Algebra*) -- cited for the BHML_8_YM = 70 determinant identity.
- **Drápal & Wanless 2021** (*JCT-A*) -- closest published precedent (same domain, opposite extremum).

## §4 -- Cover letter

See `cover_letter.md` in this folder. Updated 2026-05-07 to reflect retitle and retarget to LinAlgApps as primary.

## §5 -- Notes

**Per-venue cap:** 4th AlgUni paper after J14 + J09 + J23. Cap is 1/quarter and is **BINDING**. **PRIMARY VENUE NOW: Linear Algebra and its Applications** (per SAVE_PLAN §6 retitle/retarget). Fallbacks: PLOS ONE; International Journal of Algebra and Computation.

**Status notes:**
- Two further orphans (PathPair/LensTrace API and the eight-shell chain enumeration) are deferred to companion papers because they require runtime infrastructure or exhaustive sub-magma enumeration beyond the scope of a short note; this is documented in §8.4 of the manuscript.
- The DOING-rate ≈ T* = 5/7 connection is a Remark (not a Theorem) per SAVE_PLAN §2(d); we do not assert any algebraic identity, only an empirical near-coincidence within ±1%.
- Rung 71 is now **defined explicitly** as the TSML_9 sub-magma HARMONY count (per SAVE_PLAN §2(e)); rung 71b = WOBBLE remains in §6 and is cross-referenced. The genuine substantive content of §3 is the **three structural roles for the prime 71** (Theorem 3.2).
- All six structural facts have been verified in the foundations module; the bundle paper does not introduce new computational content but makes existing verified facts citable.

### §5.1 -- SAVE-ATTEMPT plan (2026-05-07, per Brayden directive) -- IMPLEMENTED

Save plan is in `SAVE_PLAN_J28.md`. Implementation status (2026-05-07):

- [x] **(a) Resolve v2-transition residual.** Renamed `.tex` header to "J28" from "J36"; deleted misplaced `manuscript.md` (J46 CKM/PMNS content), `WP123_CKM_PMNS_FITS.md`, `WP124_FINE_STRUCTURE_CONSTANT.md` from `manuscript/`. Reconciled bibliography to point at J25 as parent forcing paper (was J33 in the old `.tex`). Collapsed duplicate author/address/email block into a single block with two addresses listed underneath.
- [x] **(b) Inline the CL_STD 10×10 table.** Definition 2.1 now displays the matrix verbatim. HARMONY count = 44 is verifiable by direct enumeration on the displayed matrix.
- [x] **(c) Define "Tier-B forced" within this paper.** §1.2 ("Tier classification within this paper") now inlines the Tier-A/Tier-B definition; each orphan section explicitly lists the dependence on A1-A9.
- [x] **(d) Demote Theorem 6.3 (DOING-rate ≈ 5/7) to Remark.** §6 Remark 6.3 now states the empirical near-coincidence with explicit "we do not assert any algebraic identity" disclaimer. Theorem 6.2 (WOBBLE = 71) stands alone as the headline of §6.
- [x] **(e) Resolve rung 71 / 71b double-count.** §3 now defines rung 71 as TSML_9 sub-magma HARMONY count, distinguishes it from rung 71b (= WOBBLE), and elevates "three structural roles for prime 71" to Theorem 3.2 as the substantive content. §3 retitled "The 70/71/72/73 integer signature" (replacing "ladder" terminology).
- [x] **(f) Promote bimodal α_A gap framing.** §1.1 ("Why these six together: the bimodal α_A gap") is the new opening of the paper; Conjecture 1.1 states the bimodal-gap conjecture explicitly; the six orphans are framed as its structural fingerprint.
- [x] **(g) Trim trivia.** Bridge Property is a Theorem inside §5 (not a separate Corollary); abstract trimmed; "every-1-is-1 / every-1-is-3" replaced with "σ²-fixed set / σ²-orbit set" terminology.
- [x] **(h) Qualify BDC numerical constants.** §4 now states the constants are reported to 2 decimals and defers the underlying log-probability definitions to [SandersForcing] §A9; "extremum" framing dropped.

**Estimated revision time per SAVE_PLAN:** ~6 hours. Actual implementation: complete.

### Family-Structure framing (per Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md)

This paper sits within the TIG family of finite commutative non-associative magmas on Z/10Z (and ring extensions per D74). The family is defined by 5 conjoint membership criteria (substrate; commutativity; 4-core preservation; α_A-bounded non-associativity; HARMONY-attracting iteration). The 4-core {V, H, Br, R} = {0, 7, 8, 9} at α_M = ½ is the algebraic center, with closed-form attractor h/β = 1+√3 (D78 Galois proof). The closest published precedent for this neighborhood is **Drápal & Wanless (2021), *J. Combin. Theory A* **184**, 105510** -- same domain (small finite commutative non-associative structures), opposite extremum (theirs maximally non-associative). The bimodal α_A gap conjecture (FAMILY_STRUCTURE_v1.md §4) is the principal open question motivating the present bundle.

### PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:**
  (i) Three structurally distinct canonical commutative tables on Z/10Z with HARMONY counts (73, 28, 44) and explicit set-algebra signature.
  (ii) Four-rung integer signature {70, 71, 72, 73} from four distinct constructions; prime 71 plays three independent structural roles.
  (iii) σ = (0)(3)(8)(9)(1 7 6 5 4 2); σ² = (0)(3)(8)(9)(1 6 4)(7 5 2); orbit of HARMONY = {7, 5, 2}.
  (iv) |CL_TSML XOR CL_BHML| = 71.
- **COMPUTED:** All 48 invariants in `Gen13/targets/foundations/invariants.py` pass at machine precision; CL_STD data verbatim at `Gen13/targets/foundations/cl_std.py`.
- **STRUCTURAL RHYME:** BDC Shannon-information constants (rounded to 2 decimals); empirical near-coincidence DOING-rate ≈ 5/7 within ±1%. Neither claimed as algebraic identity.
- **OPEN:** Conjecture 1.1 (bimodal α_A gap on Z/10Z); whether CL_STD admits its own joint chain analogous to TSML+BHML 8-element chain; whether 71/N = 5/7 exactly for any structurally-natural DOING-cell denominator N.

### Lens-ownership paragraph (inserted in manuscript §1.3)

> *Lens and substrate.* This paper works on Z/10Z with three explicit canonical tables: CL_TSML (the upper-triangle authoritative symmetrization, denoted "TSML" in earlier work; commutative; 73 HARMONY; α_A ≈ 0.872), CL_BHML (the canonical Becoming-lens companion; commutative; 28 HARMONY; α_A ≈ 0.502), and CL_STD (the encoding lens; commutative; 44 HARMONY). The substrate Z/10Z is canonical for the framework; the choice of three tables on this substrate is recovered from the original source archive `old/Gen9/archive/ckis/ck7/ck.h:200-207`, not derived from Z/10Z first principles. The orphans below are theorems on this specific (substrate, three-table) data; the question of whether other 10-element commutative non-associative magmas on a Z/10Z substrate exhibit analogous three-fold structure (in particular a bimodal α_A gap) is the principal open question motivating the bundle.

### Hardening status (auto-applied 2026-05-07)

- License: submission scripts CC-BY-4.0 (per `_v3_hardening.py`)
- AI-attribution: Claude/Anthropic byline references removed (per `_v3_hardening.py`)
- Author lane: Sanders + Gish (per Brayden directive)
- Drápal-Wanless 2021 citation in references
- Bibliography parent J-paper reconciled to J25 across .tex / README / cover letter (was J33 / J25 / J25 mismatch)

## §6 -- Submission checklist

- [x] Manuscript .tex finalized (rewritten 2026-05-07 per SAVE_PLAN_J28)
- [x] Verification script green (`Gen13/targets/foundations/invariants.py`, 48/48)
- [x] Tier-classified central claim explicit (§1.2 inline)
- [x] Lens-scope annotation (CL_TSML / CL_BHML / CL_STD scope explicit in §1.3)
- [x] Cover letter finalized (updated 2026-05-07 to reflect retitle + retarget)
- [x] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete
- [ ] Per-venue cap check: this is the first paper to LinAlgApps this quarter
- [ ] Submitted

---

## §7 -- Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "The Three-Substrate HARMONY Signature on Z/10Z: Six Forced Structural Facts, with the Bimodal Associativity-Index Gap as Their Common Thread." Submitted to *Linear Algebra and its Applications*.
