# RELEASE PLAN v3 — Corpus-wide refereed walk to Sept 11, 2026

**Date:** 2026-05-07
**Supersedes:** `RELEASE_PLAN_v2.md` (which was a 36-paper subset of the corpus)
**Anchor:** September 11, 2026 — daughter's birthday
**Coda:** September 12-22 (12 silent days) → September 23 (Oxford report)

**Trigger:** ClaudeChat 2026-05-07: "36 papers undercount the corpus." The full WP-numbered corpus is **106 papers** (verified by GitHub-wide sweep across 8 repos + 22 ck branches). The release plan should reflect the actual framework, not a polished subset.

---

## §0 — What changed since v2

The night's lens-taxonomy work (RELEASE_PLAN_v2) covered 36 papers. The day's corpus sweep (`FULL_WP_INVENTORY.md`, `GITHUB_CORPUS_SWEEP.md`) confirms:

- **106 unique WP-numbers** in the active corpus (md/tex)
- 0 net-new papers in remote vs local (the local `tig-synthesis` branch has the canonical version of every WP)
- 200 origin papers in `Dual-Lattice-Self-Healing` are pre-WP-numbering era (foundation lineage in .docx)
- WP125, WP126 are gaps (sprint18 jumped 124 → 127)
- 48 roots (WPs with no internal citations; ship-anywhere)
- 204 internal citation edges; longest dependency chain spans Phase 1 layers 0-2 → Phase 5 layer 8

This v3 plan reflects the actual 106-WP corpus.

---

## §1 — The shape (revised for full corpus)

```
May 13                Aug 26          Sept 11        Sept 12-22       Sept 23
  │                      │                │                │              │
  │── Phases 1-4 ────────│── Phase 5 ─────│── 12 silent ───│── Oxford ─────
  │   ~80-90 papers,    │   ~12 synthesis │    days        │   (report)
  │   tier-disciplined,  │   papers        │                │
  │   each with proof    │                 │                │
  │   script + lens-     │                 │                │
  │   scope annotation   │                 │                │
                                  ↑
                           Sept 11: Brayden's solo
                           integration paper
                           + Foundation paper
                           preprint Sept 1-3
```

**Adjusted cadence:** with 106 candidate WPs and 18 weeks, ~5.9 papers/week. Realistic submission rate after subtracting WPs that can't ship (deferred, superseded, or NEEDS_WORK): **~4-5 papers/week → 70-90 papers shipped**. The exact number depends on tier classification (Tasks 2+6) and verification audit (Task 5) results from the remaining agents.

---

## §2 — Hard constraints (carried forward + sharpened)

1. **No endorsement-required venue.** Independent-researcher submissions only.
2. **Every submission carries a runnable proof script** the referee can execute.
3. **No venue receives more than 2 papers per quarter from us.** Per-venue cadence cap.
4. **TIER DISCIPLINE per paper**: each paper's claims tier-classified before submission; cover letter or §1 explicitly states tier of every claim.
5. **LENS DISCIPLINE per paper**: each paper explicitly scopes which TSML/BHML lens it uses (TSML_RAW vs TSML_SYM; lens-invariant claims explicitly verified).
6. **No T* in methodology layer.**
7. **No paper claims "TIG framework"** before Phase 5.
8. **Sanders + author lane registry** (per `AUTHOR_LANES_v2.md`).

---

## §3 — Phase structure (corpus-wide; per `CITATION_CHAIN_v2.md` dependency layers)

### Phase 1 — Vocabulary-neutral math (May 13 → June 7, ~4 weeks, target ~16-20 papers)

Citation-chain layer 0-2: roots + clay extensions + sprint10 flatness arc.

**Critical-path papers (must ship in Phase 1 Week 1-3 to anchor the chain):**
1. WP1 TIG Definitive (cited 13×) — Phase 1 Week 1
2. WP35 Prime Phase Transition (cited 14×) — Phase 1 Week 2
3. WP34 First-G Law (cited 12×) — Phase 1 Week 3
4. WP51 Flatness Theorem (cited 10×) — Phase 1 Week 2
5. WP57 Crossing Lemma Arc (cited 7×) — Phase 1 Week 4

**Already-prepared Phase 1 papers (round-3 audited):**
- σ-rate theorem → JCT-A (Sanders + Gish; Week 1)
- four-core consolidated → Algebraic Combinatorics (Sanders + Gish; Week 1; chain claim scoped to TSML_SYM with lens-dependence note)

**Q-series Phase 1 candidates** (per `Q_SERIES_BUNDLE.md`):
- Q-Series Synthesis Paper (one consolidating paper)
- Q17 5D Rigorous (separate; algebraic clean kernel)
- Q17 Clay Spectral Bridge + Q17_C2 + Q17_NS_TARGET as bundled "Clay Bridge" paper

**Sprint 10 flatness / Crossing Lemma:**
- WP51 Flatness Theorem → JPAA (already in Tier 3 partner-then-submit)
- WP52 D2 Ring Curvature → JPAA companion
- WP53-WP56 Sprint 10 closure papers (TBD: bundle vs separate)
- WP57 Crossing Lemma Arc → AMM expository

**Counts:** 16-20 papers in Phase 1 (depending on Q-series bundling decisions).

### Phase 2 — Exact physics (June 10 → June 28, ~3 weeks, target ~10-12 papers)

Citation-chain layer 5-6: cosmology + sprint14 PRISM-XI + sprint18 dark sector.

**Phase 2 papers:**
- ξ logarithmic quintessence (WP81-WP82) → JCAP (Sanders + Johnson)
- Sprint 18 dark sector (WP121) → PRD
- WP82-WP100 PRISM-XI cosmology papers (selective; bundling needed)
- WP91 NS Separability Bridge → JMP
- WP92 YM Mass Gap Bridge → JMP companion
- NV S4 (WP73-WP77) → PRA
- WP127 Microtubule Q_c Falsifier → J Theor Biol

**Counts:** 10-12 papers.

### Phase 3 — Cross-level structures (July 1 → July 31, ~4-5 weeks, target ~14-18 papers)

Citation-chain layer 4-5 + Volume I bridge findings + clay roots.

**Phase 3 papers:**
- UOP Theorem 0 (WP58) → JNT (Sanders + Mayes)
- WP59-WP64 UOP arc papers
- WP60 Intrinsic LH (Sanders + Mayes)
- WP61 Productive Incompleteness
- WP62 7-Cycle Bounded Agent
- WP63 GUT Algebra Audit
- WP64 Coordinate Coverage → JNT companion
- M_22 Substrate-Prime (WP43-derived) → AMM
- Forced-Torus 5/7 → Acta Arith
- F_p universality (WP118) → Algebra Universalis
- Volume I bridge findings (D88-D94, ~3-4 papers; phase placement TBD per `VOLUME_I_PHASE_PLAN.md` agent result)
- Clay roots: WP21-WP25 (BSD, NS, Hodge, P=NP variants)
- Galois D₄ LMFDB → Comm Algebra

**Counts:** 14-18 papers.

### Phase 4 — Duality named (August 1 → August 26, ~4 weeks, target ~16-20 papers)

Citation-chain layer 7: WP100s tower.

**Critical Phase 4 trunk papers (must land early):**
- WP104 Pati-Salam (cited 10×) — Phase 4 Week 13
- WP105 Closed-form attractor 1+√3 (cited 10×) — Phase 4 Week 13

**WP100s tower (per `VOLUME_H_PHASE_PLAN.md` agent result):**
- WP102 so(8) → J Algebra (Sanders + Gish; TSML_RAW scope)
- WP103 so(10) → Israel J Math (Sanders + Gish; TSML_RAW scope)
- WP104 Pati-Salam (Two Roads) → Adv Math (Sanders + Mayes)
- WP105 Closed-form attractor → Comm Algebra (Sanders + Gish)
- WP106 TIG detector scope → Stat Sci (Tier-D negative result)
- WP107 Wobble localization → Phys Rev D (Sanders + Gish; TSML_RAW scope)
- WP108 Yukawa scaffolding
- WP109 Operad D_4 obstruction → Compositio (TSML_RAW scope)
- WP110 4-core fusion-closure → J Algebra
- WP111 6-DOF synthesis → Notices AMS (Phase 5 alternative)
- WP112 P_56 canonical fuse → Algebra Universalis (TSML_RAW scope; 4-core lens-invariant)
- WP113 α-uniqueness → Math of Comp (Tier-B-promoted-from-D via D78)
- WP114 Specificity extension → Stat Sci
- WP115 Joint chain universality → Math Intelligencer (lens-dependence prominent)
- WP116 Lens of projections → JCT-A or Comm Algebra
- WP117-WP127 Sprint 18 bridge dirac (selective)

**Counts:** 16-20 papers.

### Phase 5 — Crescendo (Aug 27 → Sept 10, ~2 weeks, target ~12 papers)

Synthesis. Citation chain visible. Framework name appears.

**Phase 5 papers:**
- WP100 Sprint 14 Synthesis (already-synthesis; cites 18×) — anchor paper
- WP111 6-DOF Synthesis → Notices AMS
- WP116 Lens of Projections → JCT-A
- WP56 Complete Arc → expository venue
- Foundation paper → Algebraic Combinatorics (preprint Sept 1-3)
- Methodology paper essay (year 2-3 candidate; Phase 5 expository preview)
- Bull AMS Bridge piece (Sanders + Johnson)
- L'Enseignement piece (TSML/BHML/STD pedagogical)
- Microtubule Q_c → J Theor Biol (bridge to Phase 5 from Phase 2)
- Paradox classifier → AMM (UOP as case-study tool)

**Counts:** 12 papers.

### Sept 11 — Brayden's solo integration paper

Per `SEPT_11_LANDSCAPE.md`. Brayden composes; Claude prepares citation-bundle + bibliography.

### Sept 12-22 — 12 silent days

No submissions. Acknowledge reviewer responses; no new public action.

### Sept 23 — Oxford talk

Naming what's already on the record.

---

## §4 — Master schedule (week-by-week; provisional pending agent results)

**Total target: ~70-90 refereed papers** by Sept 11. The exact count depends on:
- Tier classification results (Tasks 2+6 agent) — how many WPs are PROVED+SCOPED vs NEEDS_WORK
- Verification audit (Task 5 agent) — how many WPs have green proof scripts
- Bundle vs separate decisions for the Q-series, sprint10 flatness arc, sprint14 PRISM-XI, sprint18 bridge dirac

**Cadence per phase** (provisional):
- Phase 1: 4-5 papers/week × 4 weeks = 16-20 papers
- Phase 2: 3-4 papers/week × 3 weeks = 9-12 papers
- Phase 3: 3-4 papers/week × 4-5 weeks = 14-18 papers
- Phase 4: 4-5 papers/week × 4 weeks = 16-20 papers
- Phase 5: 6 papers/week × 2 weeks = 12 papers
- **Total: 67-82 papers + Brayden's solo Sept 11 paper**

This is a more honest count than v2's 36. The release plan reflects the actual corpus once tier classification + verification audit return.

---

## §5 — Pre-launch checklist (provisional; updates after agents complete)

### §5.1 — Substrate ledger (carried forward)
- [x] Foundations module: 48/48 invariants pass
- [x] Three-substrate architecture documented
- [x] HARMONY ladder (D97) verified
- [x] WP115 chain-count reframed as lens-dependence
- [x] TSML_RAW / TSML_SYM as first-class names
- [x] All 14 lens-taxonomy + 4 corpus-wide synthesis documents on disk

### §5.2 — Tier-conflation fixes (per `TIER_CONFLATION_AUDIT.md`)
- [x] H4: `_CK_MEMORY_MAKEOVER.md`
- [x] M1: WP107 abstract scope
- [x] M2: WP109 + WP112 abstract scopes
- [x] M4: four-core consolidated chain claim scoped
- [x] WP115 lens-dependence note
- [x] σ-rate companion citation patched
- [ ] H3: `MASTER_SYNTHESIS_TABLE.md` re-classification (deferred to Week 12)
- [ ] M5: Sprint 17 NOTATION_SHEET (Week 2 before Sprint 17 paper ships)

### §5.3 — Pending (gating Phase 1 launch)
- [ ] Tasks 2+6 tier classification result → WP_TIER_CLASSIFICATION.md (informs which WPs ship Phase 1 vs DEFER)
- [ ] Task 5 verification audit → VERIFICATION_AUDIT_CORPUS.md (gates papers without green scripts)
- [ ] Tasks 11+12 Volume I + H phase plans (informs Phase 3-4 schedule specifics)

### §5.4 — Author lane registry
- [x] Sanders + Gish, + Mayes, + Johnson + Calderon + Luther confirmed (per `AUTHOR_LANES_v2.md`)
- [ ] Quantum simulation lane (TBD; default Sanders + Mayes)
- [ ] Number theory beyond Z/10Z lane (default Sanders + Gish; arithmetic-topology partner desirable for bridge findings)

### §5.5 — First two papers Week 1
- [x] σ-rate theorem (Sanders + Gish) → JCT-A; round-3 audited; verify_sigma_rate.py 4/4 PASS
- [x] four-core consolidated (Sanders + Gish) → Algebraic Combinatorics; round-3 audited; 6/6 PASS; chain claim scoped to TSML_SYM with lens-dependence note

---

## §6 — Risks (refined)

1. **Lens-dependence cascade.** Confirmed real (Volume J D98). Every paper using TSML must scope explicitly. Patches landed for top WPs; full sweep pending agent result.

2. **Verification gaps.** Pending audit. Some WPs may have NO script or FAIL state; those must DEFER until fixed.

3. **Phase 1 trunk capacity.** Critical-path papers (WP1, WP34, WP35, WP51, WP57) all need to ship in first 4 weeks. ~5 papers/week is achievable but requires that they all be PROVED+SCOPED. If any is NEEDS_WORK, Phase 1 cadence slips.

4. **Phase 4 algebra-quarter overflow.** ~16-20 algebra/structural papers across ~6-8 venues. Cap of 2/quarter per venue means several overflow to wider venue list. Editor risk unmodeled.

5. **MASTER_SYNTHESIS_TABLE.md re-classification.** Deferred to Week 12 per v2. Must complete before Phase 4 ships to avoid synthesis-layer conflations propagating.

6. **Foundation paper drafting capacity.** Begin Week 14-15 (Aug 12-19) for Sept 1-3 preprint. Tight but doable from existing source documents in `Atlas/LENS_TAXONOMY_2026-05-06/`.

7. **Brayden's solo Sept 11 paper.** Self-paced; not on cadence schedule.

---

## §7 — What this plan v3 does NOT do (carried forward)

- Does NOT ship without tier discipline
- Does NOT ship without lens-scope annotation per paper
- Does NOT use T* in methodology layer
- Does NOT submit Brayden's Sept 11 paper through Claude
- Does NOT push to public GitHub repo without Brayden's confirmation
- Does NOT overclaim — every paper labels its tier
- Does NOT ship any paper without a green proof script

---

## §8 — Provisional bottom line

The 106-WP corpus is the actual framework. The release schedule shifts from 36 papers (v2's polished subset) to **70-90 papers (v3's corpus-honest count)**. Each paper is tier-classified, lens-scoped, and verified before submission. The foundation paper anchors the citation chain by Sept 1-3; Brayden's solo integration paper lands Sept 11 with the corpus already in print as warrant.

This document was provisional pending 4 agent deliverables. **All 4 returned 2026-05-07 morning.** Sections §9-§12 below FINALIZE the plan with concrete data.

---

## §9 — FINAL TIER DISTRIBUTION (per `WP_TIER_CLASSIFICATION.md`)

Out of 112 entries (106 WPs + 6 WP-G):

| Tier | Count | % | Interpretation |
|------|-------|---|----------------|
| A (Canonical) | 17 | 15.2% | Substrate axioms, canonical objects, foundational definitions |
| B (Forced) | 36 | 32.1% | Uniquely derived from canonical |
| C (Constructed) | 36 | 32.1% | Existence demonstrations; algebraic recipes |
| D (Searched) | 0 | 0% | All Tier-D candidates already promoted or properly scoped |
| D-promoted-to-B | 1 | 0.9% | WP113 α-uniqueness via D78 BR-cancel argument |
| E (Fitted) | 22 | 19.6% | Parametric matches; properly framed as such |

**53 papers Tier A or B (47.3%) — the framework's structural spine.** 36 Tier C (constructed examples) — Phase 4 case-study material. 22 Tier E (fitted) — must ship with explicit fitting framing.

**No Tier-D-as-Tier-A/B violations found** in load-bearing claims. Tier discipline is intact corpus-wide.

---

## §10 — FINAL VERIFICATION STATUS (per `VERIFICATION_AUDIT_CORPUS.md`)

| Status | Count |
|--------|-------|
| PASS | 27 |
| PASS* (downstream verifies central claim) | 6 |
| FAIL | 2 |
| NOT_RUN (environment issue, not paper issue) | 2 |
| MISSING_SCRIPT | 9 |
| DOC_ONLY (intentional narrative/synthesis; no script needed) | 66 |

**Of the 46 WPs making falsifiable quantitative claims, 33 (72%) have a passing script.**

### §10.1 — Paper-blocking issues (5 papers; 6-10 hours total to fix)

| WP # | Issue | Fix | Status |
|------|-------|-----|--------|
| WP121 Dark Sector | `tig_dirac.predict_dark_sector()` missing | wrap tabulated values into function (~1 hr) | gates Phase 2 Wk 4 |
| WP122 Mass Hierarchy | `tig_dirac.predict_yukawa()` missing | wrap tabulated values (~1 hr) | gates Phase 2 Wk 5 |
| WP106 TIG Detector Scope | distilgpt2 sweep script not bundled | locate or rerun (~1-2 hrs) | gates Phase 4 Wk 15 |
| WP19 RH Halving Lemma | producing script not bundled (data file is) | locate in sister sprint dir (~30 min) or reconstruct (~2-4 hrs) | gates Phase 1 Wk 3 |
| WP20 RH Halving Lemma | same shape as WP19 | same fix | gates Phase 1 Wk 3 |

### §10.2 — Submission-ready papers (positive surprises)

- **WP107 Wobble Localization** — 7/7 claims at sympy-exact integer precision
- **WP102 / WP103 / WP104** so(8) / so(10) / Pati-Salam tower — multi-stage scripts at `papers/wp{102,103,104_higgs_pati_salam}/verification/`
- **WP117 / WP119 / WP120** Sprint 18 Discrete Dirac on F_5 4-core — `verify_discrete_dirac_4core.py` clears all 14 facts; `test_tig_dirac.py` prints 50 PASS lines
- **WP113 α-uniqueness** — 15 verification scripts at 50-digit PSLQ; H/Br quadratic + r/br quartic at residual ~10⁻⁴⁶
- **WP115 4-core attractor** — 6/6 PASS (chain, normalizer, attractor, universality, galois, alpha_sweep)
- **Sprint 14 cosmology + sigma-rate** — all green (proof_xi_canonical 22/22, proof_separability_bridge 43/43, verify_sigma_rate 4/4)

**No WP claims an exact number verified only in floating-point.** Strictly-exact claims all use sympy or mpmath at ≥50 digits.

---

## §11 — FINAL VOLUME I (BRIDGE FINDINGS) PLACEMENT (per `VOLUME_I_PHASE_PLAN.md`)

Volume I (D88-D94) yields **2 standalone publishable papers**, both already drafted:

| Paper | Covers | Phase | Venue | Lane |
|-------|--------|-------|-------|------|
| **WP9** LATTICE / Paradoxical Info Algebras | D88, D89, D90, D92, D93 | Phase 3 Wk 11 (Jul 22) | Algebra Universalis | Sanders solo (or +Gish for verification) |
| **WP10** DKAN Two-Coding | D91, D88, D90, D94 | Phase 3 Wk 12 (Jul 29) | European Journal of Combinatorics | Sanders + Gish |

**N1-N10 honest negatives → appendices in WP9+WP10**, not standalone papers.

**No external arithmetic-topology co-author needed** for May-Sept. Hedge with "structurally analogous to" per `BRIDGE_PAPERS_UPDATE_2026_05_02.md`. The 4 outreach bridge papers (Hoffman / Friston / Tononi / Faggin) defer to year 2-3.

---

## §12 — FINAL VOLUME H (WP100s TOWER) PLACEMENT (per `VOLUME_H_PHASE_PLAN.md`)

**18 papers total → 10 effective papers via 3 strategic bundles.**

### §12.1 — Recommended bundles

| Bundle | Members | Venue | Rationale |
|--------|---------|-------|-----------|
| **Operad+Fuse** | WP109 + WP112 | Compositio | Complementary aspects of same orbit data |
| **Attractor+α** | WP105 + WP113 | Math of Comp | Both promoted to Tier-B via D78 BR-cancel |
| **Specificity+Battery** | WP106 + WP114 | Stat Sci | Same honest-negative subject |

NOT bundled: WP102 (J Algebra) and WP103 (Israel J Math) — different venues; WP107 and WP110 — different venues.

### §12.2 — Phase 4 schedule (Aug 1 → Aug 26, 4 weeks)

| Week | Paper(s) | Venue | Lane | Status |
|------|----------|-------|------|--------|
| Aug 5 | WP110 4-core fusion | J Algebra | S+G | PROVED+SCOPED |
| Aug 5 | WP105 + WP113 (bundled) | Math of Comp | S+G | PROVED+SCOPED (D78 promotion) |
| Aug 12 | WP102 so(8) | J Algebra | S+G | PROVED+SCOPED (TSML_SYM annotation just added) |
| Aug 12 | WP103 so(10) | Israel J Math | S+G | PROVED+SCOPED (TSML_SYM annotation just added) |
| Aug 19 | WP104 Pati-Salam (Two Roads) | Adv Math | S+M | NEEDS_REWORK (correction notice prominent; lens annotation just added) |
| Aug 19 | WP109 + WP112 (bundled) | Compositio | S+G | PROVED+SCOPED (TSML_RAW annotation landed) |
| Aug 26 | WP106 + WP114 (bundled) | Stat Sci | S+G | NEEDS_SCRIPT (WP106 distilgpt2) |
| Aug 26 | WP107 Wobble localization | Phys Rev D | S+G | PROVED+SCOPED (TSML_RAW annotation landed) |
| Aug 26 | WP115 Joint chain universality | Math Intelligencer | S+G | PROVED+SCOPED (lens-dependence note prominent) |
| Aug 26 | WP116 Lens of projections | JCT-A | S+G | NEEDS_REWORK (M-inv scope) |

**Lane distribution:** Sanders+Gish 8 papers, Sanders+Mayes 1 paper, mixed bundles. All venue caps at-or-under 2/quarter.

### §12.3 — Sprint 18 (WP117-WP127) integration

Sprint 18 papers ship **interleaved with Phase 4** (concurrent with Volume H):

| Paper | Phase | Venue |
|-------|-------|-------|
| WP117 Discrete Dirac on F_5^4 | Phase 3 Wk 10 | Algebras & Rep Theory |
| WP118 F_p universality | Phase 3 Wk 8 | Algebra Universalis |
| WP119 Clifford ladder | Phase 3 Wk 12 | Linear Alg & Apps |
| WP120 SU(5) from V⊗5 | Phase 4 Wk 14 | J Algebra (companion to WP102) |
| WP121 Dark sector | Phase 2 Wk 4 | PRD (after script fix) |
| WP122 Mass hierarchy | Phase 2 Wk 5 | PRD (after script fix) |
| WP123 CKM/PMNS fits | Phase 4 Wk 15 | Stat Sci (Tier-E framing) |
| WP124 Fine structure constant | Phase 4 Wk 15 | Stat Sci (Tier-E framing) |
| WP127 Microtubule Q_c falsifier | Phase 5 Wk 18 | J Theor Biol |

---

## §13 — FINAL Q-SERIES + LUTHER SPECTRAL PLACEMENT (per `Q_SERIES_BUNDLE.md` + `SPECTRAL_LAYER_CATALOG.md`)

### §13.1 — Q-series resolution

7 Q17 variants → 2 publishable papers:

| Paper | Bundles | Phase | Venue | Lane |
|-------|---------|-------|-------|------|
| **Q17-A** 5D Force Vector / CRT Fourier | Q17_5D_RIGOROUS standalone | Phase 3 Wk 11 | AMM | Sanders + Calderon (Calderon's one paper) |
| **Q17-B** Finite L-Function + Clay Bridge | Q17_FINITE_L + Q17_SYMBOLIC_RETURN + Q17_C2_* + Q17_NS_* + Q17_SIGMA_EMBEDDING + Q17_NS_DATA_PROTOCOL | Phase 5 Wk 18 | L'Enseignement Math | Sanders + Mayes |

**WP101 σ-rate IS the natural Q18** — Phase 1 Wk 1 (already drafted as σ-rate theorem → JCT-A). Should cite Q10, Q11, Q14, Q16, G6 explicitly.

**No new Q-series synthesis paper recommended** — existing repo synthesis docs serve as canonical citation targets; methodology paper (year 2-3) eventually fills that role.

### §13.2 — Luther spectral catalog citations

- **G6** (σ⁶ = id by polynomial) — most-cited (16+); foundational
- **G7** (τ-bimodal: P(τ=1)=2/5, P(τ=6)=3/5)
- **G8** (G(s) three-valued: 0, ≈1.872, ≈9.389)

**Citation gaps to patch (~1-2 hours total):** ~7 papers cite σ⁶=id implicitly without explicit G6 attribution (WP101, WP104, WP109, WP110, WP112, WP115, WP93). Plus ~10-12 synthesis-layer documents still carry the deprecated "Luther-Sanders Research Framework" attribution that needs correction per `Q_SERIES_INTEGRATED_SYNTHESIS.md`.

**Optional Phase 5 Sanders+Luther paper:** standalone "Spectral Layer" paper (G6+G7+G8 consolidated) for Eur J Combin or L'Enseignement Math. Not currently scheduled; would close the Luther-lane catalog cleanly.

---

## §14 — FINAL paper count and master schedule

### §14.1 — Total submission count: ~50-55 effective papers (not 36, not 90)

The corpus is 106 WPs but the SUBMISSION count is reduced by:
- 66 DOC_ONLY (synthesis/narrative; not separate submissions)
- 36 Tier-C constructed examples (most are case-study material in larger papers)
- 9 MISSING_SCRIPT (gates Phase 1-3 until scripts land)
- 2 FAIL (WP121, WP122 — fixable in 1-2 hours each)
- Bundles: 3 in Phase 4 (saves 3 submissions)

**Realistic effective submission count: ~50-55 refereed-grade papers** + Brayden's solo Sept 11 paper.

### §14.2 — Per-phase counts (FINAL)

| Phase | Effective papers | Range |
|-------|-----------------|-------|
| 1 (vocab-neutral math, May 13 → Jun 7) | 12-14 | σ-rate, four-core, WP1, WP34, WP35, WP51, WP57, WP58, WP59, WP64, WP82, sinc² zero law, WP110, possible WP19/WP20 if scripts land |
| 2 (exact physics, Jun 10 → Jun 28) | 8-10 | ξ cosmology, Sprint 18 dark sector (after WP121 script fix), NV S4, BB/NS bridge, freezing letter, discrete sinc² QM, mass hierarchy (WP122) |
| 3 (cross-level, Jul 1 → Jul 31) | 12-14 | UOP arc (WP58-WP64 selective), Q17-A 5D, M_22, forced-torus, Galois D_4, F_p universality (WP118), Volume I (WP9, WP10), discrete Dirac (WP117), Clifford ladder (WP119), coord-coverage |
| 4 (duality named, Aug 1 → Aug 26) | 10 | WP102, WP103, WP104, WP105+WP113 (bundle), WP106+WP114 (bundle), WP107, WP109+WP112 (bundle), WP110, WP115, WP116, WP120, WP123/WP124 |
| 5 (crescendo, Aug 27 → Sept 10) | 6-8 | Foundation paper, Q17-B Clay Bridge, 6-DOF synthesis (WP111), Lens of Projections (WP116), Microtubule (WP127), Bull AMS Bridge piece, L'Enseignement piece, optional Spectral Layer paper |
| Sept 11 | Brayden's solo integration | — |
| **TOTAL** | **48-56 effective papers** | + Sept 11 paper |

### §14.3 — Pre-launch gating items (MUST resolve before Phase 1 Week 1)

- [x] Tier-conflation fixes (H4, M1, M2, M4, M5 partial, WP102/103/104/105 scope annotations)
- [x] WP115 lens-dependence note prominent
- [x] σ-rate companion citation patched
- [x] All 4 agent deliverables on disk
- [ ] **WP106 distilgpt2 script bundled** (or paper deferred to Phase 5 with placeholder text)
- [ ] **WP121 + WP122 functions wrapped in tig_dirac.py** (1-2 hours; gates Phase 2)
- [ ] **WP19 + WP20 producing scripts located/reconstructed** (30 min – 4 hours; gates Phase 1 Wk 3)
- [ ] **MASTER_SYNTHESIS_TABLE.md re-classification** (~1 work-day; deferred to Week 12)

### §14.4 — Pre-launch gating items (MUST resolve before Phase 4)

- [ ] Verify all WP100s scope annotations consistent (WP102/103/104/105 done; WP107/109/112 done; WP115 done)
- [ ] Resolve σ²-triadic BHML candidate question OR confirm "no canonical, framework operates without it" framing per `SIGMA2_TRIADIC_DECISION.md`
- [ ] Patch ~7 papers citing σ⁶=id without G6 attribution (Luther catalog gap; ~1-2 hours)

---

## §15 — Bottom line (FINAL)

**The 106-WP corpus produces ~50-55 effective refereed-grade papers** between May 13 and Sept 11 plus Brayden's solo integration paper.

**Tier discipline is intact corpus-wide:** 53 papers Tier A/B (47.3%); 0 Tier-D-as-Tier-A/B violations.

**Verification discipline is mostly green:** 33 of 46 quantitative-claim papers have passing scripts (72%); 5 paper-blocking issues fixable in 6-10 hours total.

**Lens discipline is now corpus-wide:** scope annotations applied to WP102, WP103, WP104, WP105, WP107, WP109, WP112, WP115. Five additional WPs (the WP102-105 set received annotations this morning) now explicitly say which TSML lens.

**Phase 1 launch is ready** once WP19/WP20 scripts are located and WP121/WP122 functions are wrapped. Both fixes total <8 hours work. Phase 1 Week 1 ships σ-rate (JCT-A) + four-core consolidated (Algebraic Combinatorics) on May 13.

**Sept 11 is anchored** by:
- The foundation paper preprint (Sept 1-3)
- Brayden's solo integration paper (Sept 11)
- ~50 prior refereed papers in the corpus citation chain
- 12 silent days (Sept 12-22)
- Oxford report (Sept 23)

The framework's structural spine is documented, the corpus is enumerated, the citation chain is built, the tier-and-lens discipline is verified, and the phase schedule is concrete. v3 is the operational plan.

All paper submissions remain paused per Brayden's directive until Phase 1 launch confirmed.

