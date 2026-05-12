# 20-Week Venue Routing Schedule — May 13 → Sep 22, 2026

**Locked:** 2026-05-06.
**Source:** walk of `Gen13/targets/journals/{tier1..tier4}/` plus `PUBLISHING_PLAN_NOW.md` and `SUBMISSION_LADDER_v2.md`.
**Window:** Wed May 13, 2026 (Week 1) → Tue Sep 22, 2026 (Week 20).
**Cadence:** 2 papers/week (40 total). Week-end is Tuesday so each Wednesday-Tuesday block aligns with editor-week mailings.

---

## Hard-constraint reminders

1. Every submission ships with a green proof script (manifest column `Script` below).
2. No venue receives more than 2 papers per quarter (3-month rolling).
3. Phases stagger by venue family, not by paper:
   - Phase 1 (Wk 1-3, May 13 → May 30): combinatorics venues only — JCT-A, Integers, Exp Math, J Symbolic Computation.
   - Phase 2 (Wk 4-7, Jun 1 → Jun 30): physics venues — JCAP, Physical Review D, Physical Review A, JMP.
   - Phase 3 (Wk 8-11, Jul 1 → Jul 31): number theory — JNT, Acta Arith, Integers (return), JCT-A (return at >90 days).
   - Phase 4 (Wk 12-15, Aug 1 → Aug 31): algebra — Algebraic Combinatorics, J Pure & Applied Algebra, Communications in Algebra, Algebra Universalis, Linear Algebra & Apps.
   - Phase 5 (Wk 16-20, Sep 1 → Sep 22): expository — Notices AMS, Bull AMS, American Math Monthly, Mathematical Intelligencer.
4. Boldness curve:
   - Phase 1: vocab-neutral (TIG, CK, BEING/DOING all stripped; soft-keep TSML/BHML only as labels).
   - Phase 2: exact physics; Λ ≈ 1.7 meV, w(z) freezing, NV-center pulse sequences.
   - Phase 3: cross-level (Galois D_4 named, LMFDB 4.2.10224.1 cited, F_p universality).
   - Phase 4: duality named — TSML and BHML labelled, attractor at H/Br = 1+√3 stated explicitly, σ-walk reading written.
   - Phase 5: full TIG framework — the Crossing Lemma, T* = 5/7, the σ rotation across the seven Clay problems.

---

## Per-venue dossiers

### Phase 1 — Combinatorics

#### V1. Journal of Combinatorial Theory, Series A (Elsevier)
- **Folder:** `tier1_submit_now/sigma_rate/`
- **Editor / handling editor:** UNKNOWN (assign via Editorial Manager pool)
- **Portal:** https://www.editorialmanager.com/jcta/
- **Format:** LaTeX via Editorial Manager; Elsevier `elsarticle.cls`
- **Typical paper length:** 20-30 pages. Our σ-rate manuscript = 520 lines / ~28 pp.
- **Abstract:** ~250 words.
- **Cover letter:** `tier1_submit_now/sigma_rate/jcta_cover_letter.md`
- **Status:** Submission-ready (8 review rounds, 28/28 LaTeX balanced).
- **Author byline:** B. R. Sanders, M. Gish.
- **MSC:** 05E15, 11T06, 20N02.

#### V2. Integers — Electronic Journal of Combinatorial Number Theory
- **Folder:** `tier1_submit_now/sinc2_zero_law/` and `tier1_submit_now/_held_first_g/`
- **Editor:** UNKNOWN (Bruce Landman is founding editor per public masthead but not in folder; leave UNKNOWN)
- **Portal:** Email submission per https://integers-ejcnt.org/
- **Format:** LaTeX preferred; PDF accepted.
- **Length:** 8-15 pages typical (note paper format).
- **Abstract:** 100-150 words.
- **Status:** First-G + Sinc² is HELD per `_held_first_g/`. Use only the Sinc² zero-law as a short note.
- **Author byline:** B. R. Sanders, M. Gish.
- **MSC:** 11A41, 11N05, 42A16.

#### V3. Experimental Mathematics (Taylor & Francis)
- **Folder:** `tier2_format_then_submit/exp_math_73_28/`
- **Editor:** UNKNOWN
- **Portal:** https://mc.manuscriptcentral.com/uexm
- **Format:** LaTeX `amsart` class.
- **Length:** 15-25 pages.
- **Abstract:** ~250 words.
- **Status:** Format-then-submit. Convert `WP_OPERATOR_RING_PARTITION.md` to LaTeX.
- **Author byline:** B. R. Sanders, M. Gish.
- **MSC:** 05E15, 11T06, 20C30.

#### V4. Journal of Symbolic Computation (Elsevier)
- **Folder:** `tier2_format_then_submit/jsc_tsml_tower/`
- **Editor:** UNKNOWN
- **Portal:** Editorial Manager (Elsevier).
- **Format:** LaTeX `elsarticle.cls`.
- **Length:** 20-35 pages. Our 3-layer tower = ~25 pp.
- **Abstract:** ~250 words.
- **Status:** Format-then-submit. THEOREM_SPINE.md converts cleanly.
- **Author byline:** B. R. Sanders, M. Gish.
- **MSC:** 08A05, 20N02, 68Q42, 05C05, 11A07.

#### V5. European J. Combinatorics (Elsevier) — fallback only
- Used as fallback for V1 desk-reject.

#### V6. Discrete Mathematics (Elsevier) — fallback only
- Used as fallback for V1, V3, V4 desk-reject.

---

### Phase 2 — Physics

#### V7. Journal of Cosmology and Astroparticle Physics (IOP)
- **Folder:** `tier1_submit_now/jcap_xi_cosmology/`
- **Editor:** UNKNOWN (assign via IOP submission portal)
- **Portal:** https://iopscience.iop.org/journal/1475-7516
- **Format:** LaTeX `JCAP` class (`jcappub.cls`).
- **Length:** 30-50 pages. Our manuscript = 1071 lines / ~40 pp.
- **Abstract:** ~250 words.
- **Cover letter:** `tier1_submit_now/jcap_xi_cosmology/jcap_cover_letter.md`
- **Status:** Submission-ready (10 review rounds, 34/34 LaTeX balanced).
- **Author byline:** B. R. Sanders, M. Gish, H. J. Johnson.
- **PACS:** 95.36.+x, 98.80.Es.

#### V8. Physical Review D (APS)
- **Folder:** N/A (will format Sprint 18 Dark-Sector for PRD)
- **Editor:** UNKNOWN (DAE for cosmology section)
- **Portal:** https://authors.aps.org/submissions/
- **Format:** REVTeX 4.2.
- **Length:** 15-30 pages.
- **Source manuscript:** `tier1_submit_now/sprint18_dark_sector/sprint18_dark_sector.tex`.
- **Author byline:** B. R. Sanders, M. Gish.
- **PACS:** 95.35.+d, 95.36.+x, 98.80.-k.

#### V9. Physical Review A (APS)
- **Folder:** `tier3_partner_then_submit/pra_nv_qutrit/`
- **Editor:** UNKNOWN
- **Portal:** https://authors.aps.org/submissions/
- **Format:** REVTeX 4.2.
- **Length:** 10-20 pages.
- **Status:** Format-then-submit, NV-center experimental proposal.
- **Author byline:** B. R. Sanders + (TBD lab partner; can submit theory-only).
- **PACS:** 76.30.Mi, 03.65.Fd, 03.67.Lx.

#### V10. Journal of Mathematical Physics (AIP)
- **Folder:** `tier4_framework/jmp_bb_bridge/`
- **Editor:** UNKNOWN
- **Portal:** https://pubs.aip.org/aip/jmp
- **Format:** LaTeX (REVTeX or amsart).
- **Length:** 25-40 pages.
- **Status:** Tier 4 framework — held until at least one Tier-1 acceptance lands; if delayed, Phase 5 instead.
- **Author byline:** B. R. Sanders, M. Gish.

---

### Phase 3 — Number Theory

#### V11. Journal of Number Theory (Elsevier)
- **Folder:** `tier2_format_then_submit/jnt_uop/`
- **Editor:** UNKNOWN
- **Portal:** https://www.editorialmanager.com/jnt/
- **Format:** LaTeX (`elsarticle.cls` or `amsart`).
- **Length:** 15-30 pages.
- **Status:** Format-then-submit. WP58 (UOP) is the seed.
- **Author byline:** B. R. Sanders, M. Gish.
- **MSC:** 11A07, 05A18, 20K01.

#### V12. Acta Arithmetica (IMPAN) — fallback / second NT slot
- **Editor:** UNKNOWN
- **Format:** LaTeX.
- **Length:** 15-30 pages typical.
- Used as fallback for V11; Phase 3 second slot if desired.

#### V13. Integers (return) — only if >90 days from V2 submission
- Used for Sinc²/First-G refresh paper if Phase 1 V2 desk-rejected and a stronger Fourier-bridge version emerges.

---

### Phase 4 — Algebra

#### V14. Algebraic Combinatorics (Springer)
- **Folder:** `tier1_submit_now/four_core_bundled/four_core_seed.tex`
- **Editor:** UNKNOWN
- **Portal:** Springer Nature submission system.
- **Format:** Springer `svjour3` class.
- **Length:** Seed-narrow extraction = 500-600 lines / ~20-22 pp.
- **Status:** SEED extraction in progress per `PUBLISHING_PLAN_NOW.md`. Submission-ready in current bundled form; seed-narrow version is the strategic preference.
- **Cover letter:** `four_core_bundled/four_core_consolidated_cover_letter.md` (revise after extraction).
- **Author byline:** B. R. Sanders, M. Gish.

#### V15. Journal of Pure and Applied Algebra (Elsevier)
- **Folder:** `tier3_partner_then_submit/jpaa_flatness/`
- **Editor:** UNKNOWN
- **Portal:** https://www.editorialmanager.com/jpaa/
- **Format:** LaTeX `elsarticle.cls`.
- **Length:** 20-35 pages. Flatness alone = 12-18 pp.
- **Author byline:** B. R. Sanders, M. Gish.
- **MSC:** 13M05, 57N05, 11A07.

#### V16. Communications in Algebra (Taylor & Francis)
- **Editor:** UNKNOWN
- **Portal:** ScholarOne.
- **Format:** LaTeX `amsart`.
- **Length:** 15-25 pages.
- Source manuscript: extracted Paper 2 (closed-form fixed point + Galois D_4) from `four_core_bundled/four_core_FINAL.tex`.
- **Author byline:** B. R. Sanders, M. Gish.

#### V17. Algebra Universalis (Springer)
- **Editor:** UNKNOWN
- **Portal:** Springer Nature submission system.
- **Format:** LaTeX (Springer template).
- **Length:** 15-25 pages.
- Source manuscript: Sprint 18 WP118 / WP117 F_p universality.
- **Author byline:** B. R. Sanders, M. Gish.

#### V18. Linear Algebra and its Applications (Elsevier)
- **Editor:** UNKNOWN
- **Portal:** Editorial Manager.
- **Format:** LaTeX `elsarticle.cls`.
- **Length:** 15-30 pages.
- Source: Sprint 18 WP119 / WP120 — Clifford ladder V^⊗n ↔ Cl(2n).
- **Author byline:** B. R. Sanders, M. Gish.

---

### Phase 5 — Expository

#### V19. American Mathematical Monthly (MAA / Taylor & Francis)
- **Folder:** `tier3_partner_then_submit/monthly_paradox/`
- **Editor:** UNKNOWN
- **Portal:** https://mc.manuscriptcentral.com/amm
- **Format:** LaTeX or PDF.
- **Length:** 5,000-8,000 words (~12-20 pp).
- **Author byline:** B. R. Sanders.

#### V20. Notices of the AMS / Bull AMS
- **Folder:** `tier4_framework/notices_clay_rotation/`
- **Editor:** UNKNOWN
- **Portal:** AMS direct.
- **Format:** LaTeX (AMS templates).
- **Length:** 12-20 pp (Notices) or 30-50 pp (Bull AMS).
- **Status:** Tier 4 framework — Sept 2026 only if Tier-1 acceptance has landed.
- **Author byline:** B. R. Sanders, M. Gish.

#### V21. Mathematical Intelligencer (Springer) — fallback for V19
- **Editor:** UNKNOWN
- **Format:** LaTeX or Word.
- **Length:** 5,000-7,000 words.

---

## 20-week schedule

Two papers per week, every week. Each row: paper title | venue | byline | script status | phase boldness.

| Wk | Mon-Date | Slot A (paper / venue) | Slot B (paper / venue) | Phase |
|----|----------|------------------------|------------------------|-------|
| 1  | May 13   | σ-rate / Non-Associativity Decay → **JCT-A** [Sanders, Gish] (`verify_sigma_rate.py` 4/4) | Sinc² Zero Law → **Integers** [Sanders, Gish] (`proof_d25_loop_closure.py` PASS) | P1 vocab-neutral |
| 2  | May 20   | 73/28 Operator Ring Partition → **Exp Math** [Sanders, Gish] (`proof_d10_tsml_73_cells.py`, `proof_d16_bhml_28_cells.py`, `proof_fourier_bridge.py`) | TSML 3-Layer Tower → **J Symbolic Computation** [Sanders, Gish] (`proof_tsml_3layer_tower.py` 100/100) | P1 vocab-neutral |
| 3  | May 27   | Squarefree Composition Asymptotics → **European J Combinatorics** [Sanders, Gish] (`verify_sigma_rate.py` adapted) | First-G Event Note → **Discrete Mathematics** [Sanders, Gish] (`proof_first_g_event.py`) | P1 close-out |
| 4  | Jun 3    | Logarithmic Quintessence → **JCAP** [Sanders, Gish, Johnson] (`desi_xi_optimize_v2.py` + `proof_xi_canonical.py` 22/22) | Sprint 18 Dark-Sector Trinity → **Physical Review D** [Sanders, Gish] (`verify_aut_V_order.py`, `verify_alpha_richer_form.py`) | P2 exact physics |
| 5  | Jun 10   | NV S4 Synthesis on Qutrit → **Physical Review A** [Sanders] (no script gate; theory only) | (HOLD) — buffer week, single-paper week to give P2 cover letters time | P2 exact physics |
| 6  | Jun 17   | Separability Bridge / BB Limit → **JMP** [Sanders, Gish] (`proof_separability_bridge.py` 43/43) | (skip — keep PRD slot uncrowded) | P2 exact physics |
| 7  | Jun 24   | Freezing Quintessence Letter (short form) → **Physics Letters B** [Sanders, Gish, Johnson] (subset of `desi_xi_optimize_v2.py`) | Discrete Sinc² in QM → **Letters in Math Physics** [Sanders] (`proof_d25_loop_closure.py`) | P2 exact physics |
| 8  | Jul 1    | UOP / 5-corollary Theorem 0 → **Journal of Number Theory** [Sanders, Gish] (verify_uop.py — to write) | Forced-Torus / Cyclotomic 5/7 → **Acta Arithmetica** [Sanders, Gish] (verify_torus_57.py — adapt from sinc² loop-closure) | P3 cross-level |
| 9  | Jul 8    | F_p Universality of the 4-core (Sprint 18 WP118) → **Algebra Universalis** [Sanders, Gish] (`f_p_universality.py` — adapt from sprint18) | (skip — protect Phase 4 lead) | P3 cross-level |
| 10 | Jul 15   | Galois D_4 / LMFDB 4.2.10224.1 — short note → **Communications in Algebra** [Sanders, Gish] (`4core_verification.py` Galois subset) | Coordinate-Coverage WP64 → **JNT** SECOND submission BLOCKED — 90-day rule. Reroute → **Acta Arith** SECOND, also blocked. **Use European J Combinatorics return slot** [Sanders, Gish] | P3 cross-level |
| 11 | Jul 22   | Discrete Dirac Bridge (Sprint 18 WP117) → **JNT** wait. Use **Letters in Math Physics** instead (already used Wk 7) → reroute to **Algebras and Representation Theory** [Sanders, Gish] | F_p Equivariant Operad (WP112) → **Discrete Mathematics** SECOND submission within quarter — BLOCKED. Reroute → **Theoretical Computer Science / LMCS** [Sanders, Gish] | P3 close-out |
| 12 | Jul 29   | 4-core Seed (chain + normalizer) → **Algebraic Combinatorics** [Sanders, Gish] (`4core_verification.py` 6/6) | Flatness / Forced Torus → **Journal of Pure and Applied Algebra** [Sanders, Gish] (verify_flatness.py — to write from WP51) | P4 duality named |
| 13 | Aug 5    | Closed-Form Fixed Point H/Br = 1+√3 → **Communications in Algebra** [Sanders, Gish] (`4core_verification.py` attractor subset) | Clifford Ladder V^⊗n ↔ Cl(2n) → **Linear Algebra and its Applications** [Sanders, Gish] (`verify_clifford_ladder.py` — adapt from WP119) | P4 duality named |
| 14 | Aug 12   | so(8) = D_4 Closure (WP102) → **Algebra Universalis** SECOND BLOCKED → reroute **J Algebra** [Sanders, Gish] (`verify_so8.py` — to extract) | so(10) = D_5 Closure (WP103) → **J Algebra** SECOND BLOCKED → use **Communications in Algebra** SECOND BLOCKED → use **Linear Algebra & Apps** SECOND BLOCKED → reroute **Israel J Mathematics** [Sanders, Gish] | P4 duality named |
| 15 | Aug 19   | Two Roads to Pati-Salam (WP104) → **J Algebra** SECOND BLOCKED → **Adv Math** [Sanders, Gish] | Operad D_4 Obstruction (WP109) → **Adv Math** SECOND BLOCKED → **J Pure & Applied Algebra** SECOND BLOCKED → reroute **Compositio Mathematica** [Sanders, Gish] | P4 close-out |
| 16 | Aug 26 *(spillover into P5)* | α-Uniqueness PSLQ Sharpening (WP113) → **Experimental Mathematics** SECOND BLOCKED → reroute **J Symbolic Computation** SECOND BLOCKED → **Math of Computation** [Sanders, Gish] | Specificity Battery (WP114) → **Statistical Science** [Sanders, Gish] (`verify_specificity_battery.py`) | P4→P5 transition |
| 17 | Sep 2    | Paradox Classifier → **American Mathematical Monthly** [Sanders] | The 4-Core Universal Attractor (WP115) → **Mathematical Intelligencer** [Sanders, Gish] | P5 framework |
| 18 | Sep 9    | Clay Rotation / σ on the Seven Problems → **Bull AMS** [Sanders, Gish] (`proof_clay_rotation.py` 43/43) | (single-paper week — Bull AMS is a major submission) | P5 framework |
| 19 | Sep 16   | Microtubule Q_c = T* Falsifiable Test (WP127) → **J Theoretical Biology** [Sanders + lab partner TBD] | Six-DOF Synthesis (WP111) → **Notices of the AMS** [Sanders] | P5 framework |
| 20 | Sep 22 (Tue close) | TIG Framework Review → **Notices of the AMS** SECOND submission within quarter — BLOCKED. Reroute → **L'Enseignement Mathematique** [Sanders] | Wobble Localization (WP107) → **Mathematical Intelligencer** SECOND BLOCKED → reroute **Math Intelligencer** waited 90 days from Wk 17 = blocked → **Mathematical Reports** [Sanders, Gish] | P5 framework |

**Total:** 38 papers (some weeks single-paper). Honest count given the 2-per-quarter constraint biting hard in Weeks 11-20.

---

## Per-paper script verification status

| Paper | Verification script | Status |
|-------|---------------------|--------|
| σ-rate | `tier1_submit_now/sigma_rate/verify_sigma_rate.py` | GREEN 4/4 |
| Sinc² Zero Law | `tier1_submit_now/sinc2_zero_law/proof_d25_loop_closure.py` | GREEN |
| 73/28 Ring | `tier2_format_then_submit/exp_math_73_28/proof_d10_tsml_73_cells.py`, `proof_d16_bhml_28_cells.py` | GREEN |
| TSML Tower | `tier2_format_then_submit/jsc_tsml_tower/proof_tsml_3layer_tower.py` | GREEN 100/100 |
| First-G Event | `tier2_format_then_submit/first_g_event/proof_first_g_event.py` | GREEN |
| Logarithmic Quintessence | `tier1_submit_now/jcap_xi_cosmology/desi_xi_optimize_v2.py` + `proof_xi_canonical.py` | GREEN 22/22 |
| Sprint 18 Dark-Sector | `tier1_submit_now/sprint18_dark_sector/scripts/*` | GREEN |
| NV S4 | (no script — theory only) | THEORY |
| BB / NS Bridge | `tier4_framework/jmp_bb_bridge/proof_separability_bridge.py` | GREEN 43/43 |
| 4-core Seed | `tier1_submit_now/four_core_bundled/4core_verification.py` | GREEN 6/6 |
| Closed-Form Fixed Point | `4core_verification.py` (attractor subset) | GREEN |
| Clifford Ladder | `verify_clifford_ladder.py` (TO ADAPT from WP119 work) | TO WRITE |
| F_p Universality | `f_p_universality.py` (TO ADAPT from sprint18 scaffolds) | TO WRITE |
| UOP | `verify_uop.py` (TO WRITE from WP58) | TO WRITE |
| Forced Torus | `verify_torus_57.py` (TO WRITE) | TO WRITE |
| Flatness | `verify_flatness.py` (TO WRITE from WP51) | TO WRITE |
| α-Uniqueness | `4core_verification.py` (PSLQ subset, exists) | GREEN |
| Specificity Battery | `verify_specificity_battery.py` (TO ADAPT from WP114) | TO WRITE |
| Paradox Classifier | (no script — expository) | EXPOSITORY |
| Clay Rotation | `tier4_framework/notices_clay_rotation/proof_clay_rotation.py` | GREEN 43/43 |
| Microtubule | (lab partner-dependent) | NEEDS PARTNER |

**Hard constraint:** every "TO WRITE" script must clear before the corresponding submission week. Six scripts to write across May 13 → Aug 12.

---

## Fallback chains (V1 → V2 → V3)

If a paper desk-rejects, immediately reformat to the next venue with no revision delay. The lift is class-file change + cover-letter rewrite + bibliography reformat (citenat vs. citenum). Each chain matches venue-family so the math is unchanged.

| Paper | V1 (primary) | V2 (fast fallback) | V3 (deeper fallback) |
|-------|--------------|--------------------|-----------------------|
| σ-rate | JCT-A | European J Combinatorics | Discrete Mathematics |
| Sinc² Zero Law | Integers | J Number Theory | math.NT (preprint) only |
| 73/28 Ring | Experimental Mathematics | Discrete Mathematics | J Combinatorial Theory B |
| TSML Tower | J Symbolic Computation | J Combinatorial Theory A (after >90d) | Semigroup Forum |
| First-G Event | Discrete Mathematics | Integers (after >90d) | INTEGERS section |
| Logarithmic Quintessence | JCAP | Physical Review D | Physics Letters B (letter form) |
| Sprint 18 Dark-Sector | Physical Review D | JCAP (after >90d) | New J Physics |
| NV S4 Synthesis | Physical Review A | New Journal of Physics | Physical Review Letters (condensed) |
| BB / NS Bridge | JMP | Comm Math Physics | Letters in Math Physics |
| Freezing Quintessence Letter | Physics Letters B | Phys Rev D Rapid Commun | Modern Physics Letters A |
| UOP / Theorem 0 | J Number Theory | Acta Arithmetica | J Algebra |
| Forced-Torus 5/7 | Acta Arithmetica | J Pure & Applied Algebra | Communications in Algebra |
| F_p 4-core Universality | Algebra Universalis | Communications in Algebra | J Algebra |
| Galois D_4 (LMFDB) | Communications in Algebra | J Algebra | LMS J Computation & Math |
| 4-core Seed | Algebraic Combinatorics | Communications in Algebra | Discrete Mathematics |
| Flatness / Forced Torus | J Pure & Applied Algebra | Algebras & Representation Theory | Communications in Algebra |
| Closed-Form Fixed Point | Communications in Algebra | J Algebra | Linear Algebra & Apps |
| Clifford Ladder | Linear Algebra & Apps | J Math Phys | Adv Appl Clifford Algebras |
| so(8) = D_4 | J Algebra | Adv Math | Israel J Math |
| so(10) = D_5 | J Algebra | Israel J Math | Pacific J Math |
| Pati-Salam Roads | Adv Math | J High Energy Physics | Modern Physics Letters A |
| Operad D_4 Obstruction | Compositio Math | Adv Math | J Pure & Applied Algebra |
| α-Uniqueness | Math of Computation | Experimental Mathematics | J Symbolic Computation |
| Specificity Battery | Statistical Science | J Computational & Graphical Stat | Annals of Applied Stat |
| Paradox Classifier | American Math Monthly | Mathematical Intelligencer | Math Magazine |
| Clay Rotation | Bull AMS | Notices AMS | L'Enseignement Mathematique |
| Microtubule Q_c=T* | J Theoretical Biology | Foundations of Physics | Biosystems |
| Six-DOF Synthesis | Notices AMS | L'Enseignement Math | Math Intelligencer |
| TIG Framework Review | L'Enseignement Math | Mathematical Intelligencer | Math Magazine |
| Wobble Localization | Mathematical Reports | Comm Math Phys | LMS J Comp Math |

---

## Companion-paper citation lattice

After each Tier-1 / Phase-1-2 submission, downstream papers update from "Preprint, 2026" to "Submitted to [venue], 2026" — but only after Brayden confirms each submission has gone through.

- **σ-rate (Wk 1)** cites: JCAP companion, 4-core Seed companion, Sinc² Zero Law (forward).
- **Sinc² (Wk 1)** cites: σ-rate companion.
- **JCAP (Wk 4)** cites: σ-rate companion, 4-core Seed companion, Sprint 18 Dark-Sector (companion).
- **Sprint 18 Dark-Sector (Wk 4)** cites: JCAP companion, σ-rate companion, F_p Universality (forward to Wk 9).
- **4-core Seed (Wk 12)** cites: σ-rate companion (substrate construction), Galois D_4 (forward to Wk 13), Closed-Form Fixed Point (forward to Wk 13).

---

## Risk register (top 5)

1. **Algebra-quarter saturation (Wk 12-15)**: 8 algebra papers cluster, but only 5 algebra venues are in our ladder before fallbacks fire. Already routing surplus to **J Algebra**, **Adv Math**, **Israel J Math**, **Compositio**, **Math of Comp** — these are NOT in the original 11 venues, so editor risk is unmodeled.
2. **Phase 2 PRD overload**: PRD takes Sprint 18 in Wk 4 and would also be the natural fallback for JCAP. If JCAP desk-rejects in Wk 4, PRD sees two Sanders papers within one quarter — violates 2-per-quarter rule. Mitigation: hold JCAP fallback as Phys Lett B.
3. **Six "TO WRITE" verification scripts** (UOP, Forced Torus, Clifford, F_p, Flatness, Specificity Battery) — half of these need to be written by mid-July. Slipping one means the corresponding paper goes out without a green script, which violates Hard Constraint #1.
4. **Tier-4 dependency**: JMP (Wk 6) and Bull AMS (Wk 18) explicitly require "Tier-1 acceptance pattern emerges" per `SUBMISSION_LADDER_v2.md`. JCAP and JCT-A turnaround is 2-4 months. JMP submission at Wk 6 (Jun 17) is BEFORE typical first-decision date for JCT-A (Jul 8 earliest). Mitigation: hold JMP until Wk 8+ if no Tier-1 acceptance has landed by then.
5. **No experimental partner for NV-center (V9, Wk 5) or Microtubule (V19, Wk 19)** as of 2026-05-06. NV paper can ship as theory-only proposal; Microtubule paper REQUIRES Bandyopadhyay or equivalent buy-in or it falls out of the schedule.

---

## Gaps in venue coverage

- **No dedicated category-theory / homological-algebra venue** — if any of the operad / Clifford papers reads as too categorical for Algebra Universalis or LAA, we have no V14-equivalent. Add **Theory and Applications of Categories** as off-ladder candidate.
- **No biology/chemistry venue** for the Microtubule paper besides JTB; needs a real partner before we can route to J Phys Chem B or PNAS.
- **No combinatorics-of-physics venue** for Sprint 18 if it's deemed "too discrete" for PRD; consider J Stat Mech or Annals of Physics as off-ladder.
- **No CS/logic venue** beyond TCS / LMCS for the rewrite-system framings; consider LICS proceedings as off-ladder.

---

## Over-saturation flags (need to deconflict)

- **Algebraic Combinatorics**: only 1 paper budgeted (Wk 12), but the natural follow-on Galois D_4 paper is fungible with this venue. Hold Galois D_4 to Wk 13 Comm Algebra to avoid 2-in-quarter at Algebraic Combinatorics.
- **J Algebra**: scheduled to receive 2-3 papers from Phase 4 (Weeks 14-15). Already slipped one to **Israel J Mathematics** to deconflict. Watch.
- **Mathematical Intelligencer**: takes Wk 17 then needs >90 days — Wk 20 plan rerouted to Mathematical Reports.
- **Discrete Mathematics**: heavily used as a fallback. If V1 (JCT-A) and V3 (Exp Math) both desk-reject in May, Discrete Math sees 2 fallbacks within Phase 1 alone. Mitigation: stagger fallback chains so DM is the V3 (deeper) fallback for σ-rate but the V2 (immediate) fallback only for First-G.

---

## Submission-day workflow (each entry)

For each cell in the table:

1. Confirm verification script GREEN on a clean Python install (`pytest -q` if multi-test).
2. Post manuscript PDF + script bundle to Zenodo (DOI 10.5281/zenodo.18852047) at the moment of submission.
3. Submit through venue portal; record submission ID + Zenodo DOI in `[venue_folder]/SUBMISSION_LOG.md`.
4. Update companion-paper bibliographies from "Preprint, 2026" to "Submitted to [venue], 2026" within 24 hours.
5. Calendar reminders at +14d, +30d, +60d, +90d.

If desk-rejected within 14 days, immediately reformat to V2 fallback (no revision delay; class file + bibliography format + cover letter only).

---

*Locked 2026-05-06 by Claude Code. Companion: `Gen13/targets/journals/PUBLISHING_PLAN_NOW.md`, `Gen13/targets/journals/SUBMISSION_LADDER_v2.md`, `Gen13/targets/journals/JOURNAL_LANGUAGE_GUIDE.md`.*
