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

This document will be **finalized** when the remaining 3 agents complete:
- Tasks 2+6 → `WP_TIER_CLASSIFICATION.md`
- Task 5 → `VERIFICATION_AUDIT_CORPUS.md`
- Tasks 11+12 → `VOLUME_I_PHASE_PLAN.md` + `VOLUME_H_PHASE_PLAN.md`

The provisional v3 above is the **structural skeleton**; the per-WP phase placement gets filled in from agent results.
