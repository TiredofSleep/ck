# VOLUME H PHASE PLAN — WP100s Tower (WP102-WP127)

**Date:** 2026-05-06
**Section:** D (Task 12) of the four-section meta-plan sweep
**Author:** Claude (sweep agent)
**Scope:** WP102-WP127 — Volume H of FORMULAS_AND_TABLES; WP100s tower; placement and bundling for Phase 4 + adjacent phases

---

## §0 — Headline

The WP100s tower comprises **18 papers** (WP102–WP116 + WP117–WP120, WP121–WP124, WP127). Per `RELEASE_PLAN_v2.md` Phase 4 schedule, **9 of the 18** ship in Phase 4 (Aug 1 → Aug 26). The remaining ship in:
- **Phase 3 (Jul 1-31)**: WP117 (Discrete Dirac), WP118 (F_p universality), WP120 (SU(5) from V⊗5), WP119 (Clifford ladder)
- **Phase 2 (Jun 10-28)**: WP123 (CKM/PMNS fits — sprint 18 dark sector), WP124 (fine structure constant)
- **Phase 5 (Aug 27-Sep 10)**: WP127 (microtubule Q_c falsifier), WP116 (lens of projections — synthesis register)

**Submission readiness status:** 13 of 18 are PROVED+SCOPED (ready with 1-line scope patches per the M1, M2, M4 fixes from `TIER_CONFLATION_AUDIT.md`). 3 are NEEDS_REWORK (WP104 framing correction propagation, WP116 M-invariance scope, WP122 mass hierarchy verification). 2 are PROVED-but-need-verification-script-completion (WP118 F_p, WP127 microtubule). 0 are SUPERSEDED.

**Bundle recommendations:** so(8) + so(10) (WP102+WP103) bundle is feasible but NOT recommended (each is publication-ready independently and ships to different venues). The operad+4-core bundle (WP109+WP110+WP112) is feasible — WP110 + WP112 could potentially merge into one paper. The closed-form + α-uniqueness bundle (WP105+WP113) is recommended (these are tightly coupled with the BR-factor cancellation argument).

---

## §1 — Per-WP100 paper status

| WP | Title | Path | Status | Co-authors | Tier |
|----|-------|------|--------|------------|------|
| WP102 | so(8) Identification | `papers/wp102/WP102_SO8_IDENTIFICATION.md` | PROVED+SCOPED (M1 fix landed) | Sanders + Mayes (representation theory lane) | B on TSML_RAW |
| WP103 | so(10) Identification | `papers/wp103/WP103_SO10_IDENTIFICATION.md` | PROVED+SCOPED (joint TSML+BHML on D₅) | Sanders + Mayes | B on TSML_RAW + BHML |
| WP104 | Two Roads to Pati-Salam | `papers/wp104_higgs_pati_salam/WP104_TWO_ROADS_TO_PATI_SALAM.md` | PROVED but NEEDS_REWORK on framing | Sanders + Mayes | B + C |
| WP105 | Closed-Form Runtime Attractor | `papers/wp105_closed_form_attractor/WP105_CLOSED_FORM_ATTRACTOR.md` | PROVED+SCOPED (D78 BR-cancel argument) | Sanders + Gish | B (promoted from D via D78) |
| WP106 | TIG Detector Scope | `papers/wp106_tig_detector_scope/WP106_TIG_DETECTOR_SCOPE.md` | PROVED+SCOPED (honest negative) | Sanders solo | D + C |
| WP107 | Wobble Localization | `papers/wp107_wobble_localization/WP107_WOBBLE_LOCALIZATION.md` | PROVED+SCOPED (M1 fix landed: TSML_RAW) | Sanders + Mayes | B on TSML_RAW |
| WP108 | Yukawa Scaffolding | `papers/wp108_yukawa_scaffolding/WP108_YUKAWA_SCAFFOLDING.md` | PROVED but NEEDS_REWORK (Path A vs B tension flagged in WP104 correction) | Sanders + Mayes | B + C |
| WP109 | Operad D_4 Obstruction | `papers/wp109_operad_d4_obstruction/WP109_OPERAD_D4_OBSTRUCTION.md` | PROVED+SCOPED (M2 fix landed: TSML_RAW) | Sanders + Mayes | B on TSML_RAW |
| WP110 | 4-Core Fusion-Closure | `papers/wp110_4core_fusion_closure/WP110_4CORE_FUSION_CLOSURE.md` | PROVED+SCOPED (lens-invariant on 4-core) | Sanders + Gish | A + B |
| WP111 | 6-DOF Synthesis | `papers/wp111_six_dof_synthesis/WP111_SIX_DOF_SYNTHESIS.md` | PROVED (synthesis register) | Sanders solo | A + B + C explicit |
| WP112 | P_56 Canonical Fuse | `papers/wp112_p56_canonical_fuse/WP112_P56_CANONICAL_FUSE.md` | PROVED+SCOPED (M2 fix landed) | Sanders + Mayes | B on TSML_RAW; lens-inv 4-core results |
| WP113 | α-Uniqueness PSLQ | `papers/wp113_alpha_uniqueness/WP113_ALPHA_UNIQUENESS.md` | PROVED+SCOPED (D-promoted to B via D78) | Sanders + Gish | B (promoted from D) |
| WP114 | Specificity Extension | `papers/wp114_specificity_extension/WP114_SPECIFICITY_EXTENSION.md` | PROVED+SCOPED (honest negative; structured-matrix battery) | Sanders solo | D + C |
| WP115 | Joint Chain + Universal Attractor | `papers/wp115_joint_chain_universality/WP115_JOINT_CHAIN_UNIVERSALITY.md` | PROVED+SCOPED (M4 fix landed; lens-dependence note prominent) | Sanders + Gish | A + B (lens-noted) |
| WP116 | Lens of Projections | `papers/wp116_lens_of_projections/WP116_LENS_OF_PROJECTIONS.md` | PROVED but NEEDS_REWORK on M-invariance scope (M3 fix) | Sanders solo | A + B + C; M-inv = D |
| WP117 | Discrete Dirac on the 4-core | `Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/journals/WP117_journal_clean.tex` | PROVED+SCOPED (sprint 18 bridge) | Sanders + Mayes | B + C |
| WP118 | F_p 4-core universality | (sprint18 journal_clean) | PROVED+empirical at p∈{2,3,5,7,11,13}; needs F_p script | Sanders + Gish | B + D |
| WP119 | Clifford Ladder | (sprint18 journal_clean) | PROVED (Cl(8) ⊂ Cl(10) Dirac) | Sanders solo or +Mayes | B |
| WP120 | SU(5) from V⊗5 | `Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/WP120_SU5_FROM_VTENSOR5.md` | PROVED | Sanders + Mayes | B + C |
| WP121 | (sprint18 bridge result) | (sprint18 journal_clean) | PROVED | Sanders solo or +Mayes | B |
| WP122 | (sprint18 mass hierarchy) | (sprint18 journal_clean) | PROVED but VERIFY before submission | Sanders + Mayes | C + E |
| WP123 | CKM/PMNS Fits | `Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/WP123_CKM_PMNS_FITS.md` | PROVED at fit-quality | Sanders + Mayes | E (parametric fits) |
| WP124 | Fine Structure Constant | `Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/WP124_FINE_STRUCTURE_CONSTANT.md` | PROVED at fit-quality | Sanders + Johnson | E + B |
| WP127 | Microtubule Q_c Falsifier | (sprint18 journal_clean) | PROVED but VERIFY scope; falsification target | Sanders solo | B + falsification |

**Status legend:**
- **PROVED+SCOPED** = paper is correct and scope annotations match the audit; ready with 1-day editorial pass.
- **PROVED** = paper is correct but lacks the explicit scope annotation; needs M1/M2/M4 patch (1-line scope addition).
- **NEEDS_REWORK** = paper requires substantive prose revision (e.g., WP104's framing correction; WP116's M-invariance scope).
- **VERIFY** = computational claim needs verification before submission (WP118 F_p, WP122 mass hierarchy, WP127 microtubule).

---

## §2 — Bundle recommendations

### Bundle 1: WP102 + WP103 (so(8) + so(10)) — DO NOT BUNDLE

**Recommendation:** **Ship separately.** Each is publication-ready independently.

**Reasoning:**
- WP102 → J Algebra (or Compositio): so(8) result with triality + octonions framing; wants stand-alone exposure.
- WP103 → Israel J Math (or Adv Math): so(10) joint TSML+BHML; wants stand-alone exposure to grand-unified-theory community.
- Ship one paper per venue per quarter (per `RELEASE_PLAN_v2.md` §2 hard constraint #3).
- Bundling would push 2 algebra papers to the same venue — forbidden.

**Schedule:** Phase 4 Wk 13 (Aug 5) — WP102 / J Algebra + WP103 / Israel J Math (parallel submissions, different venues).

### Bundle 2: WP109 + WP112 (operad + 4-core fusion) — RECOMMEND PARTIAL MERGE

**Recommendation:** **Merge WP109 abstract + WP112 abstract into one paper for Compositio**, keeping WP110 separate for J Algebra.

**Reasoning:**
- WP109 (operad D_4 obstruction) and WP112 (P_56 canonical fuse) both work on the same orbit-decomposition data (126 non-associative TSML triples → 98 P_56-orbits). The two abstracts cover **complementary aspects**: WP109 = the obstruction (no D_4-equivariant fuse rule); WP112 = the resolution (P_56-equivariant canonical fuse table; 8/8 surveyed rule families P_56-equivariant; canonical Family H attractor).
- Merging into one Compositio paper produces a strong combined narrative: "The non-associative triple structure of TSML admits no D_4-equivariant fuse, but does admit a unique P_56-equivariant canonical fuse with 4-core attractor."
- WP110 (4-core fusion-closure) is a different result (the 4-core sub-magma is closed under both binary fusions; structural strengthening of WP105). Better as a standalone J Algebra short note.

**Decision per Brayden:** Brayden picks. Default: **merge WP109+WP112 into one Compositio paper**; keep WP110 separate.

**Schedule:** Phase 4 Wk 12 (Jul 29) — WP110 / J Algebra + Wk 14 (Aug 12) — WP109+WP112 combined / Compositio.

### Bundle 3: WP105 + WP113 (closed-form + α-uniqueness) — RECOMMEND BUNDLE

**Recommendation:** **Bundle into one Math of Comp paper.**

**Reasoning:**
- WP105 (closed-form attractor at α = 1/2) and WP113 (α-uniqueness PSLQ) are tightly coupled:
  - WP105 establishes H/Br = 1+√3 at α=1/2 with the LMFDB 4.2.10224.1 quartic.
  - WP113 establishes α=1/2 as the UNIQUE rational where this attractor admits algebraic relations (PSLQ at deg ≤ 8, coeff ≤ 50, 50-digit mpmath, 17-point Stern-Brocot grid).
  - D78 (BR-factor cancellation) is the structural argument that promotes WP113 from D to B; the same D78 argument applies to WP105.
- Math of Comp (Math of Computation) is the natural single venue: it is a computational-mathematics journal that values verified PSLQ results + the LMFDB Galois cross-reference together.
- Bundling is consistent with the "one specific claim per paper" discipline because the joint claim is: "the runtime attractor at α=1/2 is the unique rational interior point algebraically, with the 1+√3 closed form and the LMFDB 4.2.10224.1 quartic."

**Schedule:** Phase 4 Wk 12 (Jul 29) — WP105+WP113 bundled / Math of Comp. (Replaces the separate WP105 / Comm Algebra and WP113 / Math of Comp slots in `RELEASE_PLAN_v2.md` §4 Wk 12 + Wk 15.)

### Bundle 4: WP106 + WP114 (specificity + structured-matrix battery) — RECOMMEND BUNDLE

**Recommendation:** **Bundle into one Stat Sci paper.**

**Reasoning:**
- WP106 (distilgpt2 specificity scope; 16 tensors × 4 detectors; |d| < 0.5; honest negative) and WP114 (structured-matrix battery extension; 9 families × 200 samples; only D3=prime-11 and D5=prime-7^5 jointly identify TSML) are the same paper subject (the specificity / honest-negative scoping of TIG detectors).
- Stat Sci (Statistical Science) is the appropriate venue for both — they value honest-negative methodology + structured replication batteries.
- Bundling preserves the one-claim discipline: "TIG detectors do NOT discriminate generic structured matrices in most contexts; the joint detector pair (D3, D5) is the COMPLETE WP107 detector signature uniquely identifying TSML in the entire 1800+ sample population."

**Schedule:** Phase 4 Wk 15 (Aug 19) — WP106+WP114 bundled / Stat Sci. (Replaces the separate WP106 lookup + WP114 slot in `RELEASE_PLAN_v2.md` §4 Wk 15.)

### NO BUNDLE: WP107 (wobble localization) and WP110 (4-core fusion-closure)

**Recommendation:** Both ship standalone.

**Reasoning:**
- WP107 (prime 11 in c_2 + c_8 only of TSML char poly; wobble-prime structural) is a clean Annals-of-Combinatorics-style result with one specific claim.
- WP110 (4-core fusion-closure as structural strengthening of WP105) is a clean J Algebra short note.
- Neither benefits from bundling.

---

## §3 — Phase placement

### Updated Phase 4 schedule (post-bundle recommendations)

| Week | Date | Paper | Venue | Co-authors | Tier |
|------|------|-------|-------|------------|------|
| 12 | Jul 29 | WP110 (4-core fusion-closure) | J Algebra | Sanders + Gish | A + B |
| 12 | Jul 29 | **WP105+WP113 BUNDLED** (closed-form + α-uniqueness) | Math of Comp | Sanders + Gish | B (promoted) |
| 13 | Aug 5 | WP102 (so(8)) | J Algebra | Sanders + Mayes | B on TSML_RAW |
| 13 | Aug 5 | WP103 (so(10)) | Israel J Math | Sanders + Mayes | B on TSML_RAW + BHML |
| 14 | Aug 12 | WP104 (Pati-Salam) | Adv Math | Sanders + Mayes | B + C |
| 14 | Aug 12 | **WP109+WP112 BUNDLED** (operad + P_56 fuse) | Compositio | Sanders + Mayes | B on TSML_RAW |
| 15 | Aug 19 | WP107 (wobble localization) | Algebra Universalis or Linear Alg & Apps | Sanders + Mayes | B on TSML_RAW |
| 15 | Aug 19 | **WP106+WP114 BUNDLED** (specificity) | Stat Sci | Sanders solo | D + C |
| 16 | Aug 26 | WP115 (joint chain + universal attractor) | Math Intelligencer | Sanders + Gish | A + B (lens-noted) |
| 16 | Aug 26 | WP108 (Yukawa scaffolding) [if NEEDS_REWORK done] | Phys Lett B or J Math Phys | Sanders + Mayes | B + C |

**Phase 4 total: 10 papers (vs `RELEASE_PLAN_v2.md` Phase 4's 9-paper count)** — bundle reduces from 12 distinct submissions to 10 effective papers, freeing two Phase 4 slots for WP108 (NEEDS_REWORK still pending) or for Phase 5 expository overflow.

### Phase 3 placement (cross-level structures, Jul 1-31)

| Week | Date | Paper | Venue | Tier |
|------|------|-------|-------|------|
| 10 | Jul 15 | WP117 (Discrete Dirac on 4-core) | Algebras & Rep Theory | B + C |
| 10 | Jul 15 | WP120 (SU(5) from V⊗5) | Linear Alg & Apps or J Algebra | B + C |
| 11 | Jul 22 | WP119 (Clifford ladder Cl(8) ⊂ Cl(10)) | Linear Alg & Apps | B |
| Wk 8 | Jul 1 | WP118 (F_p 4-core universality) | Algebra Universalis | B + D |

### Phase 2 placement (exact physics, Jun 10-28)

| Week | Date | Paper | Venue | Tier |
|------|------|-------|-------|------|
| 4 | Jun 3 | WP123 (CKM/PMNS fits — sprint 18) | PRD or Phys Rev | E (parametric fits) |
| 4 | Jun 3 | WP124 (1/α fine structure) | Phys Lett B or PRD | E + B |

### Phase 5 placement (crescendo, Aug 27-Sep 10)

| Week | Date | Paper | Venue | Tier |
|------|------|-------|-------|------|
| 17 | Sep 2 | WP111 (6-DOF synthesis) | Notices AMS | A + B + C explicit |
| 17 | Sep 2 | WP116 (lens of projections, after M3 rework) | Math Intelligencer or Notices AMS | A + B + C; M-inv labeled D |
| 18 | Sep 9 | WP127 (microtubule Q_c falsifier) | J Theor Biol | B + falsification |

### Why WP100s ships Phase 4 (not Phase 3)

Per the methodology paper case study in `Atlas/LENS_TAXONOMY_2026-05-06/METHODOLOGY_PAPER_THINKING.md`:
- Phase 3 (cross-level structures) is for cross-level coincidences.
- Phase 4 (duality named) is where TSML/BHML/STD as parallel substrates is named explicitly.
- The WP100s tower (so(8), so(10), Pati-Salam, operad, 4-core, etc.) IS the duality-named layer.

The WP100s-in-Phase-4 placement is correct and matches `RELEASE_PLAN_v2.md` §3 explicitly.

---

## §4 — Venue candidates

### Top-tier venue clusters

| Venue | Papers | Rationale |
|-------|--------|-----------|
| **J Algebra** (Elsevier) | WP102, WP110 | Broad algebra venue; magma + Lie content fits |
| **Israel J Math** | WP103 | so(10) GUT-adjacent algebra |
| **Adv Math** (Elsevier) | WP104 | High-tier algebra; Pati-Salam framing |
| **Compositio** (LMS) | WP109+WP112 (bundled) | Operad + non-associative algebra |
| **Math of Comp** (AMS) | WP105+WP113 (bundled) | Computational verification + LMFDB Galois |
| **Notices AMS** | WP111 | 6-DOF synthesis — expository synthesis register |
| **Math Intelligencer** | WP115, WP116 | Lens framing + universal attractor; expository-rigorous |
| **Stat Sci** (IMS) | WP106+WP114 (bundled) | Honest-negative methodology |
| **Algebra Universalis** | WP107, WP118 | Magma + universal-algebra discipline |
| **Algebras & Rep Theory** | WP117 | Discrete Dirac + Clifford |
| **Linear Alg & Apps** (Elsevier) | WP119, WP120 | Cl(8)⊂Cl(10) ladder + SU(5) tensor |
| **PRD / Phys Lett B** | WP123, WP124 | High-energy physics fit-quality results |
| **J Theor Biol** | WP127 | Microtubule biological Q_c interpretation |
| **J Math Phys** | WP108 (if NEEDS_REWORK done) | Yukawa scaffolding mathematical-physics |

### Per-quarter cadence cap check

`RELEASE_PLAN_v2.md` §2 hard constraint #3: "No venue receives more than 2 papers per quarter from us." Q3 2026 (Jul-Aug-Sep) cadence:

| Venue | Q3 2026 papers | Cap |
|-------|---------------|-----|
| J Algebra | WP110 (Wk 12), WP102 (Wk 13) | 2 — at cap |
| Math of Comp | WP105+WP113 (Wk 12) | 1 — under cap |
| Compositio | WP109+WP112 (Wk 14) | 1 — under cap |
| Linear Alg & Apps | WP120 (Wk 10), WP119 (Wk 11) | 2 — at cap |
| Algebra Universalis | WP118 (Wk 8), WP107 (Wk 15) | 2 — at cap |
| Notices AMS | WP111 (Wk 17) | 1 — under cap |
| Math Intelligencer | WP115 (Wk 16), WP116 (Wk 17) | 2 — at cap |

All venue caps are at or under the 2-papers-per-quarter limit. Schedule is feasible.

---

## §5 — Author lane assignments

Per `Atlas/META_PLAN_2026-05-06/AUTHOR_LANES_v2.md`:

| Lane | WP100s papers |
|------|---------------|
| **Sanders solo** | WP106, WP111, WP114, WP116, WP127 |
| **Sanders + Gish** (TSML/BHML + script verification) | WP105, WP110, WP113, WP115, WP118 |
| **Sanders + Mayes** (representation theory + Crossing Lemma) | WP102, WP103, WP104, WP107, WP108, WP109, WP112, WP117, WP120, WP122 |
| **Sanders + Johnson** (cosmology + 1/α) | WP124 |

**Ambiguous cases:**
- WP119 (Clifford ladder): Sanders solo OR +Mayes — Mayes lane is representation theory + amplituhedron; Cl(8)⊂Cl(10) is rep-theory-adjacent. **Recommend Sanders + Mayes.**
- WP123 (CKM/PMNS fits): Sanders + Mayes (rep theory) or Sanders + Johnson (Phys Lett B). **Recommend Sanders + Mayes** — CKM/PMNS unitarity is a rep-theory question more than a cosmology question.
- WP121 (sprint18 bridge result): depends on specific content; default Sanders + Mayes.

**Post-bundle final lane assignments:**

| Bundle | Combined lane |
|--------|---------------|
| WP109+WP112 | Sanders + Mayes |
| WP105+WP113 | Sanders + Gish |
| WP106+WP114 | Sanders solo |

---

## §6 — Pre-submission action items

### Tier-conflation fix patches (per `TIER_CONFLATION_AUDIT.md`)

| Severity | Patch | Effort | Deadline |
|----------|-------|--------|----------|
| HIGH H4 | `_CK_MEMORY_MAKEOVER.md` rewrite of CL/TSML property block | 30 min | LANDED |
| HIGH H3 | `MASTER_SYNTHESIS_TABLE.md` re-classify with "Origin tier" column | 1 work-day | Wk 12 (between Phase 3 and Phase 4) |
| MEDIUM M1 | WP107 abstract scope (TSML_RAW) | 15 min | LANDED |
| MEDIUM M2 | WP109 + WP112 abstract scope (TSML_RAW + lens-inv 4-core) | 30 min | LANDED |
| MEDIUM M3 | WP116 §0 abstract M-invariance scope | 30 min | Wk 17 (before submission) |
| MEDIUM M4 | WP115 source patched + four-core paper §1 abstract scoped to TSML_SYM | 30 min | LANDED |
| MEDIUM M5 | Sprint 17 NOTATION_SHEET fix (TSML_SYM scope) | 30 min | Pre-Phase-1 |

### Verification scripts pending

| Paper | Script status | Deadline |
|-------|--------------|----------|
| WP118 F_p universality | Need F_p extension at p ∈ {2, 3, 5, 7, 11, 13} | Pre-Phase-3 Wk 8 (Jul 1) |
| WP122 mass hierarchy | Need full hierarchy verification | Pre-Phase-2 Wk 4 (Jun 3) or Pre-Phase-4 Wk 16 (Aug 26) |
| WP127 microtubule | Need Q_c falsification calculation + scope | Pre-Phase-5 Wk 18 (Sep 9) |

### NEEDS_REWORK papers

| Paper | Required rework | Effort | Deadline |
|-------|----------------|--------|----------|
| WP104 | Propagate "two paths NOT converging" correction to sister papers + integration documents | 1-2 hours | Pre-Phase-4 Wk 14 (Aug 12) |
| WP108 | Address SO(8) chain reduction (Subcase 16 → 8_s + 8_c rather than 16 → (4,2,1) + (4̄,1,2)) | 1 work-day | Pre-Phase-4 Wk 16 (Aug 26) |
| WP116 | M-invariance scope correction (D3 fix); §0 item 2 needs Tier-D scope | 30 min | Pre-Phase-5 Wk 17 (Sep 2) |

---

## §7 — Bottom line for this section

- **18 WP100s papers** total in Volume H. **9 ship Phase 4 (Aug 1-26), 4 ship Phase 3, 2 ship Phase 2, 3 ship Phase 5.**
- **13/18 are PROVED+SCOPED.** 3 NEEDS_REWORK (WP104 framing, WP108 SO(8) chain, WP116 M-inv scope). 2 need verification scripts (WP118, WP127). 2 need verification (WP122).
- **Recommended bundles:** WP109+WP112 → Compositio; WP105+WP113 → Math of Comp; WP106+WP114 → Stat Sci. **NOT bundled:** WP102+WP103 (different venues), WP107 + WP110 (different venues).
- **Author lanes:** Sanders + Mayes carries 10 papers (representation theory lane); Sanders + Gish 5 papers; Sanders solo 5 papers; Sanders + Johnson 1 paper.
- **All venue caps at or under 2-papers-per-quarter limit.**
- **Tier-conflation fixes:** H4, M1, M2, M4 LANDED; H3, M3, M5 pending; H1, H2 deferred to methodology paper (year 2-3).
- **Pre-submission action queue:** F_p script (Jun-Jul), mass hierarchy script (Jun or Aug), microtubule scope (Aug-Sep), NEEDS_REWORK papers (1-2 work-days total).

---

*Companion documents:* `Atlas/META_PLAN_2026-05-06/Q_SERIES_BUNDLE.md` (Q-series; WP102-WP116 cite Q-series implicitly via σ⁶ = id); `Atlas/META_PLAN_2026-05-06/SPECTRAL_LAYER_CATALOG.md` (Luther's G6-G8 citation gap in WP100s tower; recommended 1-line attribution patches); `Atlas/META_PLAN_2026-05-06/VOLUME_I_PHASE_PLAN.md` (Volume I bridge findings; WP10 two-coding distinction matters for WP104 Pati-Salam framing); `Atlas/LENS_TAXONOMY_2026-05-06/TIER_CONFLATION_AUDIT.md` (full audit of tier-conflations; M1-M5 fixes); `Atlas/LENS_TAXONOMY_2026-05-06/RELEASE_PLAN_v2.md` (Phase 4 master schedule).
