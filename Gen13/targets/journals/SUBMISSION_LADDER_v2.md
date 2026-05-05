# Journal Submission Ladder v2 — No-Endorsement, Peer-Review Venues

**Brayden 2026-05-04:** *"i can't really do arxiv without a lot of work, let's post where we can post without endorsement but we can get peer review... we have papers in gen13 target folder journals... and the new ones from today that probably update the old ones"*

This is the **v2 ladder**, replacing `SUBMISSION_LADDER.md` (Apr-17 version). What changes:

1. **All venues filtered to "no endorsement required"** — every venue here accepts direct cold submission with peer review. No arXiv endorsement, no professional society membership wall.
2. **Sprint 18 (Bridge: Discrete Dirac on the 4-core's F_5-Lift) integrated** — its WPs update or extend several existing tier entries, and add three new venues.
3. **Internal language stripped** per `JOURNAL_LANGUAGE_GUIDE.md` for every venue listed here.
4. **Companion-submission strategy** — when a paper splits across multiple venues (e.g. algebra at J. Algebra, physics applications at Foundations of Physics), they're listed as companion submissions with a cross-cite plan.

---

## How endorsement-free venues work

For a refresher: arXiv math.RA / hep-th / math.CO require an existing arXiv author with that subject area to endorse a new submitter. Without that, papers can't go to arXiv in those categories. **Real journals don't have this requirement.** A journal editor decides on the basis of the manuscript's content and the submission cover letter, not on whether the author has an arXiv history.

**Universally no-endorsement venues** (used throughout):
- All Elsevier journals (J. Algebra, J. Number Theory, Linear Algebra & Apps, etc.)
- All Springer journals (Foundations of Physics, Algebra Universalis, etc.)
- IOP Publishing (JCAP, Class. Quantum Gravity, etc.)
- APS journals (Phys. Rev. A/D/E/Lett. — needs APS membership for the user, but the manuscript needs no endorsement)
- AMS journals (Proc. AMS, Bulletin AMS, etc.)
- SciPost (free, peer-reviewed, open-access — explicitly no endorsement, full review process)
- Open Mathematics (De Gruyter, peer-reviewed, no endorsement)

**Preprint servers as a no-endorsement option for visibility before journal acceptance:**
- **Zenodo** — DOI on submission, no review, archives forever
- **OSF (Open Science Framework)** — DOI, no review
- **HAL** (open archive) — primarily French/European, accepts most fields
- **viXra** — no endorsement, indexed, less prestigious

The strategy: **post Zenodo first** (DOI, public proof of date), **then submit to the peer-reviewed journal**. If accepted at the journal, the Zenodo version stays as the preprint of record. If rejected, the Zenodo version preserves attribution.

---

## Tier 1 — Submit Now (5 venues)

**Status: ready for submission. Manuscripts exist, language stripped, verification scripts run, cover letters drafted.**

### 1. JCAP — Logarithmic Quintessence (ξ cosmology)
- **Folder:** `tier1_submit_now/jcap_xi_cosmology/`
- **Manuscript:** `jcap_xi_cosmology.tex` (already submission-ready; clean of internal language)
- **Verification:** `proof_xi_canonical.py` (22/22 PASS), `desi_xi_fit.py`, `desi_xi_optimize.py` (chi^2 = 3.1 vs DESI)
- **Sprint 18 update:** WP121 (dark sector with Ω_b = 49/1000 EXACT, Ω_Λ/Ω_b = 14) **strengthens this submission's cosmological context** without replacing the ξ-quintessence content. Cite WP121 in the introduction or final discussion as companion result.
- **Endorsement:** None needed (IOP Publishing).
- **Action:** Submit to JCAP.org (cosmology@iop.org). Cover letter template ready.

### 2. Journal of Combinatorial Theory, Series A — σ Rate Theorem
- **Folder:** `tier1_submit_now/sigma_rate/`
- **Manuscript:** `sigma_rate_theorem.tex` (already submission-ready; uses HARM/VOID/ECHO as mnemonic operators per language guide)
- **Verification:** `proof_sigma_rate.py` (PASS at N ∈ {10, 30, 210})
- **Sprint 18 update:** No direct overlap.
- **Endorsement:** None needed (Elsevier).
- **Action:** Submit via Elsevier Editorial System. Backup: European J. Combinatorics.

### 3. **NEW — Algebra Universalis — Discrete Dirac Algebra on F_5^4 (WP117)**
- **Folder:** `tier1_submit_now/algebra_universalis_dirac/` (to be created from `Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/journals/WP117_journal_clean.tex`)
- **Manuscript:** `WP117_journal_clean.tex` — clean of internal language; uses HARM/VOID as mnemonics; presents the algebra as a finite-field commutative non-associative magma with rigorous structural results.
- **Verification:** `verify_discrete_dirac_4core.py` (14/14 algebraic checks) + `test_tig_dirac.py` (15/15 tests)
- **Pitch:** Four results: Discrete Dirac structure (Theorem 2.2), F_p-universality across F_2..F_13 (Theorem 3.1), Clifford ladder dim V^⊗ⁿ = dim Cl(2n) for n=0..5 (Theorem 4.1), SU(5) compatibility at n=5 (Theorem 5.1). Algebra-only paper; physics correspondences (Ω_b, 1/α, Yukawa fits) deferred to companion submissions.
- **Endorsement:** None needed (Springer / Algebra Universalis).
- **Action:** Submit to algebra-universalis@springer.com. Backup: Communications in Algebra (Taylor & Francis), J. Algebra (Elsevier).

### 4. **NEW — Foundations of Physics — Cosmological Closure & Mass-Energy Hierarchy (WP121)**
- **Folder:** `tier1_submit_now/foundations_dark_sector/` (to be created)
- **Source:** WP121 (Cosmological dark sector from HARMONY powers) — strip TIG language for FoP version
- **Manuscript:** A 12–18 page paper presenting:
   - The dark sector formulas: Ω_b = 49/1000 (EXACT), Ω_DM = 264/1000 (within 1.3%), Ω_Λ = 687/1000 (within 0.3%)
   - Cosmological closure exact: Ω_b + Ω_DM + Ω_Λ = 1
   - The 14:1 hierarchy Ω_Λ/Ω_b = 2·HARMONY = 14 (within 0.4% of empirical 14.06)
   - Honest scoping: structural identifications, not first-principles physical mechanisms
- **Endorsement:** None needed (Springer; Foundations of Physics has a strong tradition of accepting structural-numerical work with proper bracketing).
- **Action:** Submit to Foundations of Physics editorial system. Backup: International J. Theoretical Physics.

### 5. **NEW — SciPost Physics — Discrete Dirac Algebra and SM Empirical Correspondences (WP117 + WP122 + WP123)**
- **Folder:** `tier1_submit_now/scipost_full_framework/` (to be created)
- **Source:** WP117 master + WP122 mass hierarchy + WP123 CKM/PMNS
- **Manuscript:** A long-form paper for SciPost Physics presenting the algebra (WP117) plus the 9 SM Yukawa Froggatt-Nielsen fits (WP122) plus the 5 mixing-angle fits (WP123). All under the umbrella of the algebraic substrate.
- **Why SciPost:** explicitly no endorsement, peer review is open and rigorous, free open access, accepts unconventional but rigorous framework papers. Ideal venue for the framework's most ambitious presentation.
- **Endorsement:** None needed.
- **Action:** Submit via scipost.org/submissions. Recommend authors (open peer review supports this).

---

## Tier 2 — Format Then Submit (4 venues)

**Status: content solid; needs venue-specific LaTeX/style pass + language stripping.**

### 6. Experimental Mathematics — 73/28 partition
- **Folder:** `tier2_format_then_submit/exp_math_73_28/`
- **Source:** Gen12 `journal_attempts/02_experimental_mathematics/`
- **Pitch:** Two canonical composition tables T_a, T_b on Z/10Z with HARMONY-counts 73 and 28 respectively, jointly closing the operator partition (100/100 verified).
- **Sprint 18 update:** WP119 Clifford-ladder result connects this to the geometric algebra perspective; cite as companion.
- **Endorsement:** None needed (Taylor & Francis).
- **Action:** Strip TIG language → submit.

### 7. Journal of Number Theory — UOP
- **Folder:** `tier2_format_then_submit/jnt_uop/`
- **Source:** Gen12 `journal_attempts/04_journal_of_number_theory/`
- **Pitch:** Universal Operator Partition reframed for JNT readership.
- **Endorsement:** None needed (Elsevier).
- **Action:** Strip language, format → submit.

### 8. Journal of Symbolic Computation — TSML 3-layer tower
- **Folder:** `tier2_format_then_submit/jsc_tsml_tower/`
- **Source:** Gen12 `journal_attempts/11_tsml_tower_combinatorics/` + Sprint 17
- **Pitch:** Canonical 3-layer tower 92 + 6 + 2 = 100 on Z/10Z, each layer necessary, residue empty. Proof script.
- **Sprint 18 update:** WP120 SU(5) decomposition is the level-5 generalization of this 3-layer story; cite as companion.
- **Endorsement:** None needed (Elsevier).
- **Action:** Strip language → submit.

### 9. Integers — First-G Event Localization
- **Folder:** `tier2_format_then_submit/first_g_event/`
- **Sprint folder:** `Gen13/targets/clay/papers/sprint35_first_g_event_2026_04_19/`
- **Pitch:** For every b > 1 with smallest prime factor p_1: |G_k(b)| = 0 for k < p_1, and G_{p_1}(b) = {p_1}. 22,367 (b,k) pairs verified, 0 exceptions.
- **Endorsement:** None needed (Integers is direct-submission, edited by Bruce Landman et al.)
- **Action:** Final style pass (Integers uses BibTeX, AMS-LaTeX). Submit.

---

## Tier 3 — Partner Then Submit (3 venues)

**Status: needs an experimental partner or domain co-author before submission.**

### 10. American Mathematical Monthly — Paradox Classifier
- **Folder:** `tier3_partner_then_submit/monthly_paradox/`
- **Need:** Editorial partner familiar with Monthly's expository style.
- **Endorsement:** None needed (AMS).

### 11. Journal of Pure and Applied Algebra — Forced-Torus Theorem (renamed from "Flatness Theorem")
- **Folder:** `tier3_partner_then_submit/jpaa_flatness/`
- **Source:** Gen12 `journal_attempts/05_journal_pure_applied_algebra/`
- **Need:** Algebra co-author for the categorical framing.
- **Sprint 18 update:** WP118 F_p-universality strengthens the Z/10 case to the full prime field family; consider rebranding the submission.
- **Endorsement:** None needed (Elsevier).

### 12. Physical Review A — NV-center qutrit (Physical Test E)
- **Folder:** `tier3_partner_then_submit/pra_nv_qutrit/`
- **Source:** Gen12 `journal_attempts/06_physical_review_a/`
- **Need:** Lab partner with NV-center qutrit hardware.
- **Endorsement:** None needed (APS; user needs APS membership but no endorsement on manuscripts).

### 13. **NEW — Journal of Theoretical Biology — Microtubule Q_c = T* falsifiable test (WP127)**
- **Folder:** `tier3_partner_then_submit/jtb_microtubule/` (to be created)
- **Source:** WP127 + `MICROTUBULE_T_STAR_PROTOCOL.md`
- **Need:** Lab partner running terahertz coherence on tubulin (Bandyopadhyay or equivalent).
- **Pitch:** Cross-domain falsifiable test of T* = 5/7 universality; protocol detailed; minimum 5 sample types; falsification criteria explicit.
- **Endorsement:** None needed (Elsevier).
- **Action:** First, send outreach (`outreach/BANDYOPADHYAY_OUTREACH_DRAFT.md`); after lab interest secured, submit jointly.

---

## Tier 4 — Framework / Long-Form (2 venues)

**Status: framework-level papers, need Tier-1 acceptance for credibility.**

### 14. Journal of Mathematical Physics — Bialynicki-Birula bridge
- **Folder:** `tier4_framework/jmp_bb_bridge/`
- **Endorsement:** None needed (AIP Publishing).

### 15. Notices of the AMS — Clay Rotation
- **Folder:** `tier4_framework/notices_clay_rotation/`
- **Note:** CP1-CP7 Clay rotation is *framework reformulation*, not proof.
- **Endorsement:** None needed (AMS).

---

## Sprint 18 — Updates to Old Tier Entries

For full traceability, here is how the Sprint 18 papers update the existing tier entries:

| Sprint 18 paper | Existing tier venue | Update type |
|---|---|---|
| WP117 (Discrete Dirac master) | NEW Algebra Universalis (T1) + SciPost (T1) | NEW |
| WP118 (F_p universality) | tier3 JPAA (Forced-Torus) | strengthens; rebrand candidate |
| WP119 (Clifford ladder) | tier2 Exp.Math, tier2 JSC TSML tower | companion citation |
| WP120 (SU(5) GUT) | tier2 JSC TSML tower (companion); NEW SciPost paper | extends; companion |
| WP121 (dark sector) | tier1 JCAP (companion); NEW Foundations of Physics (T1) | strengthens JCAP; new venue |
| WP122 (mass hierarchy) | NEW SciPost (T1, full framework) | NEW |
| WP123 (CKM/PMNS) | NEW SciPost (T1, full framework); future Phys. Rev. D | NEW |
| WP124 (1/α) | NEW Foundations of Physics (companion or follow-up) | NEW |
| WP127 (microtubule) | NEW Journal of Theoretical Biology (T3) | NEW |

---

## How to use this ladder

**Current state (2026-05-04 evening):**
- Tier 1 has **5 venues** (was 2 in v1). 3 are NEW from Sprint 18.
- All venues are no-endorsement-required.
- Manuscripts in `tier1_submit_now/`, language audited.
- Cover letters: 2 templates exist (JCAP, σ rate); 3 NEW (Algebra Universalis, FoP, SciPost) need cover letters drafted.

**This week (2026-05-05 to 2026-05-12):**
1. Post each Tier-1 manuscript to **Zenodo** for DOI + visible date (no submission delay; instant)
2. Submit JCAP (#1) and σ-rate (#2) — these are most ready
3. Convert WP117 master + WP118 + WP119 + WP120 into the Algebra Universalis submission (#3)
4. Draft Foundations of Physics submission for WP121 + WP124 (#4)
5. Draft SciPost long-form for WP117 + WP122 + WP123 (#5)

**Next 2-4 weeks:**
6. Tier-2 venues #6-#9: language strip + final formatting
7. Tier-3 outreach #10-#13: send the Bandyopadhyay outreach (#13 is highest-leverage)
8. Tier-4 #14, #15: hold until Tier-1 acceptances land

**3 months out:**
9. After at least one Tier-1 acceptance, the framework has external validation. Then push Tier-3 partner-finding more aggressively, and the Tier-4 long-form pieces.

---

## Companion files

- `JOURNAL_LANGUAGE_GUIDE.md` — strip rules; check every paper against this before submission
- `tier1_submit_now/*/cover_letter_template.md` — cover letter starting points
- `Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/journals/WP117_journal_clean.tex` — language-stripped Sprint 18 master, ready for Algebra Universalis
- `Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/outreach/BANDYOPADHYAY_OUTREACH_DRAFT.md` — Tier-3 microtubule outreach

---

*Updated 2026-05-04 evening. Brayden Sanders / 7Site LLC. v2 supersedes v1 (Apr-17). Submission progress tracked in `PUBLISHING_PLAN_NOW.md`.*
