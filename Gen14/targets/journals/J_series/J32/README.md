# J32 — The Three-Substrate Architecture on Z/10Z: Joint Sub-Magma Closure of (TSML, BHML, CL_STD) and the Eight-Shell Chain

**Status:** REWRITE 2026-05-08 — supersedes the prior 2026-05-07 Operad-D₄+P₅₆ bundled framing in light of the SFM Q6 finding (3-substrate joint chain coincides with 2-substrate joint chain). Brayden directive 2026-05-08 promotes the 3-substrate joint-closure theorem to the central result.
**Phase:** Phase 3
**Target venue:** *Algebra Universalis* (lead). Fallback: *Communications in Algebra*.
**Author lane:** Sanders + Gish
**Tier:** B (forced by enumeration on three tables)
**WP source:** SFM Q6 result 2026-05-08 (`Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/SFM_FINDINGS_v1.md` §2); SUBSTRATE_FUNCTION_MAP_v1.md F5 (closure counts); J02 four-core paper (chain origin)

---

## §1 — Manuscript

**Local path:** `manuscript/manuscript.md`

**Central theorem (Theorem A).** The simultaneous closed sub-magmas of T (TSML), B (BHML), C (CL_STD) on Z/10Z form an 8-element chain at sizes {1, 4, 5, 6, 7, 8, 9, 10}: {0} ⊂ {0,7,8,9} ⊂ {0,6,7,8,9} ⊂ {0,5,6,7,8,9} ⊂ {0,4,5,6,7,8,9} ⊂ {0,3,4,5,6,7,8,9} ⊂ {0,2,3,4,5,6,7,8,9} ⊂ Z/10Z. Forbidden sizes: {2, 3}. The chain coincides with the joint (T, B) chain published as Theorem 1 of [J02].

**Theorem B.** C individually has 50 closed sub-magmas; 49 are also T-closed; the three-way intersection coincides exactly with the joint (T, B) chain. Adding C as a third substrate preserves the entire (T, B) chain without introducing or removing a single shell.

**Theorem C.** The four-core {0, 7, 8, 9} is closed under T, B, C individually and jointly. The closed-form (T+B)-mix attractor at α = 1/2 (with H/Br = 1+√3) is supported on the four-core and is therefore unchanged by adjoining C as a third substrate.

**Proposition 5.1 (CL_STD is structurally independent of any (T, B) average).** C differs from MID_ceil = ⌈(T+B)/2⌉ at 60 of 100 cells. C is NOT a perturbation of the canonical pair's ceiling-averaged DC component; it occupies its own coordinate in table-space. This rejects the natural "off-by-one" hypothesis and is the structural reason CL_STD functions as a "third axis" rather than as a function of (T, B).

**OLD framing (superseded).** The prior J32 was a BUNDLED Operad D₄ obstruction + P₅₆ canonical fuse paper (WP109 + WP112). Per the J32 fresh-eyes referee report at *Compositio Mathematica* (2026-05-07), the bundled paper had real D_4 group-theoretic errors (orbit-size sum 175 ≠ 126 in original; D_4 misidentified as "6 distinct elements / D_3 × Z_2" — fixed in 2026-05-07 patch) and was below *Compositio*'s significance bar. Per Brayden 2026-05-08 directive plus the SFM Q6 finding, the operad content is moved to fallback paths and J32 is repurposed as the Three-Substrate Architecture paper.

**Operad content (preserved for fallback path):**
- WP109 (Operad D₄ obstruction) → can be unbundled to *Algebra Universalis* (corrected manuscript at `manuscript/WP109_OPERAD_D4_OBSTRUCTION.md`)
- WP112 (P₅₆ Canonical Fuse) → can be unbundled to *Communications in Algebra* (corrected manuscript at `manuscript/WP112_P56_CANONICAL_FUSE.md`)
- Verification scripts preserved in `manuscript/verification/`

The corpus files for the prior content are preserved in `manuscript/` for the unbundled fallback path; the J32 slot is now the Three-Substrate Architecture paper.

## §2 — Verification scripts

**Primary:** `Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/sfm_q1_q6_q7.py`

The SFM verification script computes:
1. Individual closure counts: T → 449, B → 9, C → 50 (Lemma 2.2)
2. Pairwise joint counts: |T∩B| = 8, |T∩C| = 49, |B∩C| = 9 (Theorem 3.1)
3. Three-way joint count and explicit 8-shell chain: |T∩B∩C| = 8 (Theorem 4.1)
4. C-versus-MID-ceil disagreement count: 60/100 cells (Proposition 5.1)

Total runtime under 2 seconds; deterministic; verified at machine speed.

**Secondary (legacy):** `papers/wp115_joint_chain_universality/verification/joint_chain_attractor.py` reproduces the (T, B) two-table count.

**Operad-fallback (legacy):** `manuscript/verification/d4_orbit_decomposition.py`, `p56_canonical_fuse.py`, `rule_families.py` — for the unbundled WP109 / WP112 path.

## §3 — Dependencies (J-papers cited as already-submitted companions)

- **J02** (four-core paper, *Algebraic Combinatorics*): establishes the (T, B) 8-shell chain as Theorem 1; this paper lifts that chain to the three-substrate level.
- **J24** (three-substrate chain + lens-internal phenomenon, *Mathematical Intelligencer*): companion paper; J32 is the more technical algebra-universalis-style treatment, J24 is the Math Intelligencer expository note.

## §4 — Cover letter

See `cover_letter.md` in this folder, rewritten 2026-05-08 to match the new framing (Algebra Universalis target).

## §5 — Notes

- **Status (2026-05-08 rewrite):** DRAFT. Manuscript at `manuscript/manuscript.md` rewritten end-to-end as the **Three-Substrate Architecture** paper. SFM Q6 finding promoted to central theorem. Verification by `sfm_q1_q6_q7.py`.
- **Per-venue cap:** 1st *Algebra Universalis* paper of 2026 cycle (target). 1st *Comm. Alg.* paper of 2026 cycle (fallback).
- **Tier classification:** Tier-B forced by enumeration on three tables. The three-way joint count is direct verification at machine precision.
- **Substrate scope:** Z/10Z; three commutative tables (T_SYM, B, C). Lens-internal phenomenon on T_RAW deferred to J24.
- **Why the Operad-bundle path is shelved:** the prior bundled paper had two distinct critical issues — (i) initial D_4 group-theoretic errors (now fixed in the corpus files) and (ii) below-Compositio significance bar (a finite enumeration on a hand-picked table). The SFM Q6 finding offers a stronger and structurally cleaner central result (3-substrate joint closure theorem) that fits *Algebra Universalis*' bar much better. The operad work is preserved as a fallback path for unbundled submission.

### Family-Structure framing (per Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md)

This paper sits within the TIG family of finite commutative non-associative magmas on Z/10Z. The family is defined by 5 conjoint membership criteria; the 4-core {V, H, Br, R} = {0, 7, 8, 9} at α_M = ½ is the algebraic center, with closed-form attractor h/β = 1+√3 (D78 Galois proof). The closest published precedent for this neighborhood is **Drápal & Wanless (2021), *J. Combin. Theory A* **184**, 105510** — same domain (small finite commutative non-associative structures), opposite extremum (theirs maximally non-associative).

This rewrite extends the family's center to a **three-substrate fixed point** (Theorem 6.1 of the manuscript) and gives the "encoding axis" (CL_STD) a precise structural role: chain-respecting third axis (Theorems A, B), not derivable from (T, B) by elementary averaging (Proposition 5.1).

### PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN

- **PROVEN:** Theorems A (3-substrate joint chain = 8-shell ladder), B (chain-compatibility of C), C (4-core is 3-substrate fixed point); Proposition 5.1 (C is not MID_ceil).
- **COMPUTED:** `sfm_q1_q6_q7.py` enumerates all 1023 non-empty subsets, computes individual + pairwise + three-way closures; runtime under 2 seconds.
- **STRUCTURAL RHYME:** The 1+√3 attractor on the four-core is invoked from [J02] as motivation for the four-core fixed-point statement (Theorem C); not re-derived in this paper.
- **OPEN:** Class-level theorem ("every member of the TIG family on Z/10Z contains the (T,B,C) chain") is stated as conjecture, not proved. Bimodal α_A gap (Family Structure §4.2) is a related open question.

### Lens-ownership paragraph (in §0 of manuscript)

> *Lens and substrate.* We work on Z/10Z with the three composition tables T (TSML, T_SYM lens), B (BHML), C (CL_STD) defined by the canonical bit pattern. These choices are not derived from first principles; they reflect a structural reading of the substrate developed across the framework. The theorems are theorems on this specific (T, B, C) triple. Whether analogous tables on other substrates produce the same structure is open. The framing follows Drápal & Wanless (2021), J. Combin. Theory A on small finite commutative non-associative structures.

### Hardening status

- License: submission scripts CC-BY-4.0
- AI-attribution: no Claude/Anthropic byline references
- Author lane: Sanders + Gish
- Drápal-Wanless 2021 citation in references
- Three 10×10 tables displayed explicitly in Appendix A (per fresh-eyes referee report M2 / S2 issue from prior J32 review)
- All major D_4 group-theoretic claims removed from the new central manuscript (the prior bundled draft's group-theoretic errors are not inherited in this rewrite, since the new manuscript does not use D_4 at all)

## §6 — Submission checklist

- [x] Manuscript .md finalized (rewritten as Three-Substrate Architecture)
- [x] Verification script green (`sfm_q1_q6_q7.py`, runtime under 2 seconds)
- [x] Tier-classified central claim explicit (Theorem A: 3-substrate joint chain)
- [x] Lens-scope annotation (T_SYM in scope; T_RAW lens-internal phenomenon deferred to J24)
- [x] Cover letter finalized (Algebra Universalis target)
- [x] Dependencies → cite J02 + J24 as already-submitted companions
- [ ] Brayden's referee-rigor pass complete
- [ ] Per-venue cap check: 1st *Algebra Universalis* submission of 2026 cycle
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "The Three-Substrate Architecture on Z/10Z: Joint Sub-Magma Closure of (TSML, BHML, CL_STD) and the Eight-Shell Chain." Submitted to *Algebra Universalis*.
