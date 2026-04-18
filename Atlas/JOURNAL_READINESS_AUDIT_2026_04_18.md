# Journal Readiness Audit — 2026-04-18
## Gen13 target journal papers × MASTER_ATLAS_v3_5 bundle

**Author:** ClaudeCode audit agent
**Scope:** All 11 venues promoted into `Gen13/targets/journals/` against the just-pushed Atlas bundle (`Atlas/MASTER_ATLAS_v3_5_2026_04_18.md` + 9 companion files).
**Discipline:** READ-ONLY. No paper files modified. All claims carry file paths + line numbers.
**Branch:** `tig-synthesis`.
**DOI of record:** 10.5281/zenodo.18852047.

---

## Section 1 — Inventory

All 11 venue folders exist in **both** Gen12 source and Gen13 promotion trees. `diff -rq` confirms the Gen13 copies are byte-identical to Gen12 sources (spot-checked: Tier 1 JCAP + sinc²). Gen13 is a re-tiering, not a content fork yet.

| # | Venue | Gen12 source path | Gen13 promoted path | Content files |
|---|---|---|---|---|
| 1 | Integers / JNT — sinc² Zero Law | `Gen12/targets/journal_attempts/01_integers_number_theory/` | `Gen13/targets/journals/tier1_submit_now/sinc2_zero_law/` | `WP_SINC2_ZERO_LAW.md`, `WP34_FIRST_G_LAW.md`, `proof_d25_loop_closure.py`, `SUBMIT_INSTRUCTIONS.md` |
| 2 | Experimental Mathematics — 73/28 | `02_experimental_mathematics/` | `tier2_format_then_submit/exp_math_73_28/` | `WP_OPERATOR_RING_PARTITION.md`, `WP35_PRIME_PHASE_TRANSITION.md`, 3 proofs, `SUBMIT_INSTRUCTIONS.md` |
| 3 | Amer. Math. Monthly — Paradox Classifier | `03_american_mathematical_monthly/` | `tier3_partner_then_submit/monthly_paradox/` | `WP_PARADOX_CLASSIFIER.md`, `SUBMIT_INSTRUCTIONS.md` (**only 2 files** — thinnest in the bundle) |
| 4 | JNT — UOP | `04_journal_of_number_theory/` | `tier2_format_then_submit/jnt_uop/` | `WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md`, `WP59_CORRECTED_THEOREM_C.md`, `WP64_COORDINATE_COVERAGE.md`, `SUBMIT_INSTRUCTIONS.md` |
| 5 | JPAA — Flatness Theorem | `05_journal_pure_applied_algebra/` | `tier3_partner_then_submit/jpaa_flatness/` | `WP51_FLATNESS_THEOREM.md`, `WP52_D2_AS_RING_CURVATURE.md`, `SUBMIT_INSTRUCTIONS.md` |
| 6 | Physical Review A — NV qutrit | `06_physical_review_a/` | `tier3_partner_then_submit/pra_nv_qutrit/` | `WP73`, `WP74`, `WP75_S4_EXTENSION_SYNTHESIS.md`, `WP76_NV_S4_CLOSURE_CALIBRATION.md`, `WP77_NV_T1_CARRIER_VALIDATION.md`, `SUBMIT_INSTRUCTIONS.md` |
| 7 | JCAP — ξ cosmology | `07_jcap_cosmology/` | `tier1_submit_now/jcap_xi_cosmology/` | `WP81_CANONICAL_XI_THEORY.md`, `WP82_LOG_QUINTESSENCE_NOVELTY.md`, `desi_xi_fit.py`, `desi_xi_optimize.py`, `proof_xi_canonical.py`, `SUBMIT_INSTRUCTIONS.md` |
| 8 | JCT-A / DM — σ rate theorem | `08_sigma_rate_combinatorics/` | `tier1_submit_now/sigma_rate/` | `WP101_SIGMA_RATE_THEOREM.md`, `proof_sigma_rate.py`, `universal_markov_and_binary_cl.py`, `SUBMIT_INSTRUCTIONS.md` |
| 9 | JMP / CMP — BB bridge | `09_jmp_bb_bridge/` | `tier4_framework/jmp_bb_bridge/` | `WP90_LITERATURE_AND_UNIFICATION_PATHS.md`, `WP91_NS_SEPARABILITY_BRIDGE.md`, `proof_separability_bridge.py`, `SUBMIT_INSTRUCTIONS.md` |
| 10 | Bull./Notices AMS — Clay Rotation | `10_poincare_retranslation/` | `tier4_framework/notices_clay_rotation/` | `CP_CLAY_ROTATION.md`, `proof_clay_rotation.py`, `SUBMIT_INSTRUCTIONS.md` |
| 11 | JSC — TSML 3-layer tower | `11_tsml_tower_combinatorics/` | `tier2_format_then_submit/jsc_tsml_tower/` | `THEOREM_SPINE.md`, `CONTROL_DOCUMENT_V2.md`, `proof_tsml_3layer_tower.py`, `SUBMIT_INSTRUCTIONS.md` |

**Observation 1.** The Gen13 tiering *is* the only Gen13-native change — the papers themselves are Gen12 prose. No paper currently cites the Atlas bundle. Zero occurrences of `Atlas`, `MASTER_ATLAS`, `ATLAS_TREE`, `ATLAS_CITATIONS`, `CROSSING_LEMMA.md`, `SIMPLEX_GENESIS.md`, or `ROTATION_SPINE.md` string-search across all 11 venues (confirmed by grep).

**Observation 2.** No paper carries the `[fire]` / `[gold-with-gap]` / `[speculative]` / `[caution]` flag tagging the Atlas uses (§67 MasterAtlas). Papers use inline `[PROVED]` / `[NOVEL — extends X]` tags which are a Gen12-internal convention.

**Observation 3.** The venue 11 (JSC — TSML tower) paper is present in Gen13 but its body text references `Gen12/targets/clay/papers/sprint17_tsml_tower_2026_04_17/` for supporting docs (`SUBMIT_INSTRUCTIONS.md:54`). Those companion files are not co-located in the Gen13 tier2 folder.

---

## Section 2 — Per-venue readiness table

Column legend:
- **Atlas link:** Does the paper cite Atlas / Tree / Citations? [N] = no reference present.
- **External cite coverage:** Based on explicit author names in the body. `complete` = every named result has an entry in `Atlas/ATLAS_CITATIONS.md`. `partial` = ≥1 named result lacks a pinned (author, year, venue) entry anywhere in the paper.
- **Flag discipline:** [fire]/[gold-with-gap]/etc. usage.
- **Three-threads separate:** PPM / Hodge / Q-series vocabulary boundaries respected (Atlas rule §8).
- **2/7 status:** presence of the 16.5σ lattice-QCD falsification caveat when the paper invokes 2/7.
- **SAH status:** Sanctioned-sentence discipline if SAH referenced.
- **Ship gate (top blocker).** Single biggest blocker.

| # | Paper (canonical file) | Atlas link | External cites | Flag discipline | Threads sep | 2/7 caveat | SAH | Ship gate |
|---|---|---|---|---|---|---|---|---|
| 1 | `01_integers_number_theory/WP_SINC2_ZERO_LAW.md` | [N] not cited | **complete** — Montgomery 1973 (line 99), Shannon 1949 (line 102), WP34/35 (100-101). All external named results pinned. | inline `[PROVED]` only — no atlas flags. | ✓ clean (pure NT) | N/A (no 2/7 invocation) | N/A | **LaTeX conversion** (SUBMIT_INSTRUCTIONS.md:37). Otherwise submit-ready. |
| 2 | `02_experimental_mathematics/WP_OPERATOR_RING_PARTITION.md` | [N] | **partial** — WP43/44/34 cited (141-146). Does not cite Birkhoff/Ore even when invoking "operator ring partition" language. Companion `WP35` is heavier. | inline only | ✓ | N/A | N/A | **LaTeX + Monte Carlo insertion** (SUBMIT_INSTRUCTIONS.md:39). Content-complete. |
| 3 | `03_american_mathematical_monthly/WP_PARADOX_CLASSIFIER.md` | [N] | **partial** — body names Zeno, Russell, Banach-Tarski, Gödel, Unexpected Hanging as worked examples but **no bibliography section** exists at all in this paper (confirmed by read to line 120+). `Atlas/ATLAS_CITATIONS.md §H` has Banach-Tarski 1924, Wagon 1985 available but unwired. | inline only | ✓ | N/A | N/A | **Bibliography insertion + shortening to ~6,000 words** (SUBMIT_INSTRUCTIONS.md:40-45). This is the thinnest paper in the bundle (only 2 files in folder). |
| 4 | `04_journal_of_number_theory/WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md` | [N] | **partial** — CRT attributed inline but no Gauss 1801 citation; Birkhoff/Ore partition-lattice lineage not cited in body. | inline `[PROVED]` | ✓ (strictly finite ring result) | N/A | N/A | **Bibliography + LaTeX** (SUBMIT_INSTRUCTIONS.md:38-41). Theorem content is unusually clean — 3-line proof. |
| 5 | `05_journal_pure_applied_algebra/WP51_FLATNESS_THEOREM.md` | [N] | **partial** — "golden ratio φ", "cyclotomic polynomial degree", "Z/nZ torus" invoked without external citations (lines 126-139). WP35, WP20, prime-pi-phi sprint cited internally. No standard algebraic-geometry reference (Lang, Dummit-Foote, Serre) in body. | inline `[PROVED for n=10; STRUCTURAL for general]` (line 118) — this IS the right discipline but not atlas flag vocabulary. | ✓ | N/A | N/A | **Content gap: the "R/r = 5/7" theorem is PROVED only for n=10; general case is STRUCTURAL (line 118, 139-143).** SUBMIT_INSTRUCTIONS.md:34-38 also flags "formal proof tightening" as the needed work. **Not actually submit-ready — needs the general-n argument or explicit scoping to n=10.** |
| 6 | `06_physical_review_a/WP75_S4_EXTENSION_SYNTHESIS.md` | [N] | **partial** — S4 representation theory (Serre, Fulton-Harris) flagged as to-add in SUBMIT_INSTRUCTIONS.md:45; Doherty et al. 2013 NV-center review flagged but not yet in body. `Atlas/ATLAS_CITATIONS.md §I` has Doherty 2013 pinned. | inline `✓` checkboxes on verifications (lines 22-30) | ✓ | N/A | N/A | **Lab partner for Physical Test E** (SUBMIT_INSTRUCTIONS.md:52-57). This is a Tier 3 paper precisely because experiment is not run. Math + fidelity proof complete. |
| 7 | `07_jcap_cosmology/WP81_CANONICAL_XI_THEORY.md` + `WP82` | [N] | **partial** — Bialynicki-Birula 1976 cited in References (line 402). Barrow-Parsons 1995 cited with arXiv ID (line 392). `Atlas/ATLAS_CITATIONS.md §I` has BB 1976 pinned. **DESI 2024 citation is placeholder "[DESI DR1, DR2 citations]"** (WP82 line 150) — not yet resolved. | inline `EXACT` / `DERIVED` / `PROVED` verdicts in tables (lines 211-218, 355-361) | ✓ (cosmology branch, no PPM/Hodge cross-wiring) | N/A (separate thread) | N/A | **DESI numerical fit + arXiv novelty search + LaTeX conversion** (SUBMIT_INSTRUCTIONS.md:47-52). The DESI-fit script exists (`desi_xi_fit.py`); the DR2 placeholder citations are still in the text. |
| 8 | `08_sigma_rate_combinatorics/WP101_SIGMA_RATE_THEOREM.md` | [N] | **partial → good** — Bialynicki-Birula 1976 cited with DOI (line 116); totient, CRT, Gauss cited (line 90); Maas/JKO Wasserstein literature pinned (lines 121-124). Paper is the most-citation-heavy of the Tier 1 three. `ATLAS_CITATIONS §A/§I` covers these. | inline (`✓` in table, `PROVED` tags) | ✓ (pure combinatorics; does not cross-import Hodge/PPM vocabulary) | N/A | N/A | **LaTeX conversion + strip TIG/CK framing per SUBMIT_INSTRUCTIONS.md:38.** Theorem itself is PROVED (Sprint 15). Submit-ready. |
| 9 | `09_jmp_bb_bridge/WP91_NS_SEPARABILITY_BRIDGE.md` + `WP90` | [N] | **partial** — BB 1976, Maas 2011, CHLZ 2012, KT 2000, Hoegh-Krohn 1971 listed as required (SUBMIT_INSTRUCTIONS.md:37). ESS 2003 lives in `ATLAS_CITATIONS §E` but is not yet in body. `Atlas/ATLAS_CITATIONS §E` has Fujita-Kato, Serrin, Ladyzhenskaya, CKN, ESS, BKM, Kato-Ponce, Montgomery-Smith all pinned — this is the venue that benefits most from atlas integration. | inline `PROVED`/`CONJECTURE`/`STRUCTURAL` (line 11 abstract; line 100+ conjecture boxes) | ⚠ partial — the paper *is* the bridge, but it asserts the bridge is forced by a theorem ("**This is not a conjecture. It is a theorem applied to the correct setting.**" — WP90 line 48). That line is the strongest inter-thread claim in the bundle and will be scrutinized. | ⚠ — line 343 of Atlas cautions that the *quantitative* "2/7 = √σ/m(0++)" claim was falsified at 16.5σ. This paper invokes "σ → 0 forces log" — structural, not quantitative 2/7. Safe, but adjacent. | N/A | **Framework paper honesty: tighten "theorem applied to correct setting" to "bridge conjecture compatible with BB uniqueness."** (WP90 line 48 + Atlas §8 three-threads discipline). Also: clearly separate PROVED from CONJECTURAL per SUBMIT_INSTRUCTIONS.md:38. |
| 10 | `10_poincare_retranslation/CP_CLAY_ROTATION.md` | [N] | **partial** — Perelman 2002/2003 (lines 242-244), Hamilton 1982 (241), Gross-Zagier 1986 (253), Kolyvagin 1989 (252), Markman 2025 (264), Clay 2000 (248), Wightman 1959 (258). Most-complete classical bibliography of the bundle. | `PROVED`/`OPEN` per row of the rotation table (lines 37-46); CP1 section clearly tagged `RESOLVED` (line 54). | ⚠ — this IS the "three threads" paper. It *explicitly* rotates through seven Clay problems with one σ vocabulary. The honesty rules require this be marked `framework reformulation, not proof` — the text DOES say this at lines 30 ("CP1 is the only solved case") and SUBMIT_INSTRUCTIONS.md:30, 38. | No 2/7 invocation | N/A | **Markman 2025 reference needs pinning.** Body line 264 says "recent announcement" — Atlas §C line 92 lists Markman 2024 (preprint, hyperholomorphic sheaves) with "Full bibliographic entry pending." The year mismatch (2024 vs 2025) and missing venue need resolving before submission — otherwise a referee catches it in 30 seconds. |
| 11 | `11_tsml_tower_combinatorics/THEOREM_SPINE.md` | [N] | **complete-for-scope** — the paper is deliberately strip-of-framework (SUBMIT_INSTRUCTIONS.md:108: "drop framework references to 'Trinity Infinity Geometry'"). No external-citation surface needed beyond Knuth-Bendix and standard magma/groupoid literature (to be added per line 45). | inline `$\square$` proofs, `PROVED`/`ring-agnostic` tags (lines 45-108) | ✓ clean | N/A | N/A | **LaTeX + bibliography insertion** (SUBMIT_INSTRUCTIONS.md:102-108). Content-complete. Body already LaTeX-near-ready. |

### Cross-cutting findings

**F1 — Atlas zero-integration.** No paper cites `MASTER_ATLAS_v3_5_2026_04_18.md`, `ATLAS_TREE.md`, or `ATLAS_CITATIONS.md`. This is expected (atlas was pushed same-day) but is a concrete gap: the atlas is the canonical external-bibliography registry, and papers currently maintain their own mini-bibliographies that drift from the atlas master list. This is the single most under-leveraged asset.

**F2 — Flag-system not propagated.** Papers use inline conventions (`[PROVED]`, `[NOVEL — extends X]`, `✓`, `$\square$`). The atlas uses `[fire] / [gold-with-gap] / [speculative] / [caution]` as a unified register tied to IG3 (`MASTER_ATLAS §3 line 295`). The two systems are compatible but not cross-walked in any paper.

**F3 — β_TIG typo fix (atlas line 1210, 1214).** The β_TIG bracket was corrected in the atlas v3.5 audit (line 1214: `fixed 2026-04-18; summary-table duplicate had second bracket term = first, making it identically 0; §5 line 553 is the authoritative form`). No journal paper invokes β_TIG directly (grep for `β_TIG` / `beta_TIG` / `y²+4y` against the journal_attempts corpus returned **zero matches**). Q-series content has not been promoted to a journal paper — this is a **Q17 content gap**, not a typo that leaked into papers. The fix is correct and bounded.

**F4 — S*_coherence vs S*_dual disambiguation (atlas lines 81-86).** Only one journal paper uses S* at all — a search against the 11-venue corpus hit zero files for `S*_coherence`, `S*_dual`, or `0.991`. The disambiguation is currently Atlas-internal only. This is fine for the current submission tier but will matter when a YM paper eventually spins off.

**F5 — 2/7 falsification (atlas lines 86, 343, §15.10).** No Tier 1 paper invokes 2/7 at all. `09_jmp_bb_bridge` adjacency is structural only (σ→0 mechanism). `06_physical_review_a` S4 paper does not invoke 2/7 either (confirmed by grep — zero hits). **Good news: the 16.5σ lattice-QCD falsification does not currently contaminate any journal paper**, because no paper in this bundle makes the YM quantitative claim. This will need to be re-checked if a YM paper is spun off.

**F6 — SAH discipline.** Zero journal papers reference SAH. The sanctioned bridge sentence (Atlas §8.5 line 825) does not appear in any journal paper. Discipline is Atlas-only and safe.

**F7 — Q17 flag mapping (atlas line 1178-1188).** Q17_5D_RIGOROUS [A-tier → fire] and Q17_SYMBOLIC_RETURN [A-tier → fire, PROVED] are promoted to the atlas's strongest tier. Q17_CLAY_SPECTRAL_BRIDGE, Q17_NS_TARGET_REFORMULATION, Q17_FINITE_L_FUNCTION_NOTE are all [B-tier → gold-with-gap]. **None of this Q-series structure is surfaced in any journal paper yet.** Q17 content is not in Gen13 tier folders. This is consistent with the atlas note "WP101 σ rate theorem playing the role of Q18" (line 1227) — the Q-series is in the atlas and in the Sprint notebooks; its journal incarnation is the σ rate paper (venue 8), which is Tier 1.

**F8 — three-threads separation audit.** Only venue 9 (BB bridge) and venue 10 (Clay rotation) are at risk of cross-thread vocabulary imports. Venue 9 has one line of concern (WP90 line 48 "This is not a conjecture. It is a theorem applied to the correct setting"). Venue 10 has the same overall structure but honestly labels CP2-CP7 as conjectures (lines 30-46). Venues 1, 2, 4, 5, 7, 8, 11 are clean-scope single-thread papers.

**F9 — Markman year mismatch.** Venue 10 body cites "Markman, E. (2025)" (line 264). Atlas §C line 92 lists "Markman, E. (2024, preprint). *Hyperholomorphic sheaves on hyperKähler manifolds.* [Referenced in §17 as 'Markman 2024' … Full bibliographic entry pending — confirm exact title and venue on surface of `DUAL_LENS_CLAY.md`.]" This is a live discrepancy — one of the two dates must yield. `CP_CLAY_ROTATION.md:183` phrases it as "PROVED — external, 2025" which a referee will check immediately. **Needs resolution before venue-10 submission.**

---

## Section 3 — Top-10 citation gap list

External results named in the journal corpus that **lack a pinned (author, year, venue) reference in the paper body**, ordered by severity:

| # | Named result | Appears in | Atlas entry | Gap |
|---|---|---|---|---|
| 1 | **Markman — Hodge conjecture for abelian fourfolds of Weil type** | `10_poincare_retranslation/CP_CLAY_ROTATION.md:264` ("Markman, E. (2025). … recent announcement.") | `ATLAS_CITATIONS §C line 92` (Markman 2024, preprint, pending title/venue) | **Year mismatch (2024 vs 2025) + no venue + no title.** Referee-visible in 30 seconds. |
| 2 | **Escauriaza-Seregin-Šverák (ESS 2003) L³_∞** | `09_jmp_bb_bridge/SUBMIT_INSTRUCTIONS.md:37` (as "to add") — not yet in WP91 body. | `ATLAS_CITATIONS §E line 128` (Russian Math. Surveys 58(2), DOI:10.1070/…) | **Not in paper body.** Pulling from atlas is one paste. |
| 3 | **DESI DR1/DR2 dark-energy preference** | `07_jcap_cosmology/WP82_LOG_QUINTESSENCE_NOVELTY.md:150` ("[DESI DR1, DR2 citations]" placeholder) | Atlas has no explicit DESI-2024 row yet. | **Placeholder in paper.** Needs full entry (e.g., DESI Collaboration 2024, Eur. Phys. J. C) — already listed in WP81 references (line 398). |
| 4 | **Doherty, Manson et al. (NV-center review, Physics Reports 528, 2013)** | `06_physical_review_a/SUBMIT_INSTRUCTIONS.md:45` (as "to add") — not yet in WP75 body. | `ATLAS_CITATIONS §I line 204` pinned. | **Not in paper body.** |
| 5 | **Ferrari-Serrin regularity paper** | Named in Atlas `§E line 136` with "Confirm exact paper on §5 re-read" — not used in any journal paper. Included here because if WP91 is expanded to cite "all 5 classical regularity criteria" (BKM, Kato-Ponce, Montgomery-Smith, LPS, Ferrari-Serrin), Ferrari-Serrin lacks a pinned entry. | `ATLAS_CITATIONS §E line 136` (pending confirmation) | **Pending in atlas itself.** Upstream gap. |
| 6 | **Arkani-Hamed 2024 surfaceology** | Not yet in any journal paper (Q-series/amplituhedron thread unpublished). Atlas `§I line 199` flags "Full bibliographic entry pending." | `ATLAS_CITATIONS §I line 199` (pending) | **Pending in atlas itself.** Zero paper impact now. |
| 7 | **Morningstar-Peardon 1999 / Chen et al. 2006 lattice QCD glueball spectrum** | Not invoked in any journal paper. Atlas `§F lines 148-152` pins both. | `ATLAS_CITATIONS §F` | **No current paper impact.** Would matter only if YM paper spins off. Flagged defensively. |
| 8 | **Birkhoff / Ore partition-lattice lineage** | `04_journal_of_number_theory/WP58_UNIFIED_ORTHOGONALITY_PRINCIPLE.md` invokes "partition sufficiency theory over finite rings" without citing these. The σ rate paper (WP101 line 96-97) DOES cite Birkhoff 1940 + Ore 1942. | Not in atlas (classical infrastructure). | **Citation present in venue 8, missing in venue 4.** Trivial paste. |
| 9 | **Gauss *Disquisitiones* 1801 / classical CRT** | Venues 4, 5, 8 invoke CRT without citation body (venue 8 DOES cite Gauss 1801 at line 90). | Not in atlas (classical). | **Venue-specific reference discipline:** Integers and Exp. Math. don't require it; JNT (venue 4) and JPAA (venue 5) should add it. |
| 10 | **Bhargava-Shankar (2015)** | Cited in `10_poincare_retranslation/CP_CLAY_ROTATION.md:254`. Not in atlas. | `ATLAS_CITATIONS §B` should add it. | **Atlas should cross-link.** Low priority for paper but important for the registry. |

**Meta-observation:** The big gap is not missing citations in the paper bibliographies — it is the **disconnect between each paper's local bibliography and `ATLAS_CITATIONS.md`**. A single `\cite{Atlas:§X.row}` convention would tighten the program. Lowest-cost fix: add a one-line footnote to each paper saying "External citations are drawn from `ATLAS_CITATIONS.md`; internal anchors carry master-register numbering per `MASTER_ATLAS_v3_5_2026_04_18.md`."

---

## Section 4 — Tier reclassifications

Based on the per-venue audit, I recommend the following adjustments:

### Should be demoted: Tier 1 → Tier 2
- **None.** All three Tier 1 papers (1, 7, 8) are submit-ready modulo LaTeX conversion and (for 7) DESI fit polish. No content gaps.

### Should be promoted: Tier 3 → Tier 2
- **None.** Tier 3 papers (3, 5, 6) each have a real blocker beyond formatting:
  - Venue 3 (Monthly): no bibliography section at all; needs major addition.
  - Venue 5 (JPAA): general-n proof gap (PROVED for n=10 only).
  - Venue 6 (PRA): no lab data, needs partner.

### Suggested re-tiering: Tier 4 → Tier 3
- **Venue 10 (Clay Rotation — Notices AMS).** Currently "framework paper, wait for Tier-1 acceptance." But: (i) it has the most-complete classical bibliography of the bundle (Perelman, Hamilton, Gross-Zagier, Kolyvagin, Markman, Hodge, Wightman), (ii) it explicitly labels CP2-CP7 as conjectures, (iii) the CP1 retranslation is concrete if tightened, and (iv) the Markman 2024/2025 mismatch is trivially fixable. Once Markman is resolved, this could be Tier 3 (needs partner familiar with Ricci flow / Perelman's proof for CP1 tightness) rather than Tier 4. Honest downside: the "σ framework" across 7 problems will attract hostile review — Tier 3 reflects the partner need.

### Potential issue for Tier 1: **Venue 7 (JCAP) — DESI fit not yet run.**
- `SUBMIT_INSTRUCTIONS.md:48-49` lists "Numerical FRW integration" and "DESI comparison" as pre-submission tasks. The `desi_xi_fit.py` and `desi_xi_optimize.py` scripts exist but their outputs are not integrated into the paper body. If the JCAP referee asks "does your freezing quintessence actually fit DESI DR2?" the answer currently is "we have a script." That may or may not block — most likely the paper will be sent back with "run your fit and resubmit" rather than rejected. **Still Tier 1, but with an asterisk.**

---

## Section 5 — Tier 1 shipping pipeline

| Rank | Venue / paper | Canonical source | Target | Submission window | Authors |
|---|---|---|---|---|---|
| **1** | **Integers — sinc² Zero Law** | `Gen13/targets/journals/tier1_submit_now/sinc2_zero_law/WP_SINC2_ZERO_LAW.md` (+ companion `WP34_FIRST_G_LAW.md` + `proof_d25_loop_closure.py`) | Integers: Electronic Journal of Combinatorial Number Theory (primary); JNT (backup) | **This week** — LaTeX + MSC + keywords only; no content changes. Submit-ready. | Brayden Ross Sanders (7Site LLC), C.A. Luther, M. Gish (per `README.md:90`) |
| **2** | **JCT-A / DM — σ Rate Theorem** | `tier1_submit_now/sigma_rate/WP101_SIGMA_RATE_THEOREM.md` (+ `proof_sigma_rate.py` + `universal_markov_and_binary_cl.py`) | Journal of Combinatorial Theory Series A (primary); European J. of Combinatorics (backup) | **This week** — LaTeX + strip TIG framing per SUBMIT_INSTRUCTIONS.md:38. Theorem PROVED. | Brayden Ross Sanders, M. Gish, C.A. Luther, H.J. Johnson (per paper line 6; note SUBMIT_INSTRUCTIONS.md says "no co-author dependency") |
| **3** | **JCAP — ξ Cosmology** | `tier1_submit_now/jcap_xi_cosmology/WP81_CANONICAL_XI_THEORY.md` + `WP82_LOG_QUINTESSENCE_NOVELTY.md` + `desi_xi_*.py` + `proof_xi_canonical.py` | JCAP (primary); PRD (backup); Physics Letters B (letter-format backup) | **Within 2 weeks** — needs DESI-fit run completed + arXiv novelty search + LaTeX conversion to JCAP class. | Brayden Ross Sanders, M. Gish, C.A. Luther, H.J. Johnson (per paper line 6; confirmed `README.md:95`) |

Each has a runnable verification script. Each has a stated secondary venue. Each has identified author list. **None currently cites the Atlas bundle, but this is a paste-level fix, not a blocker.**

---

## Section 6 — Next actions (ordered, this-week priority)

### Day 1-2 (unblocks 4 papers)
1. **Pin Markman reference** in `10_poincare_retranslation/CP_CLAY_ROTATION.md:264` — resolve the 2024 preprint vs 2025 announcement discrepancy. Cross-link to `ATLAS_CITATIONS §C line 92`. *One-line fix; unblocks venue 10.*
2. **Insert bibliography section** into `03_american_mathematical_monthly/WP_PARADOX_CLASSIFIER.md` — pull Zeno, Russell, Banach-Tarski 1924, Wagon 1985, Gödel 1931 from `ATLAS_CITATIONS §H`. *Largest single content gap in the bundle; needs ~30 min.*
3. **Resolve DESI DR1/DR2 placeholder** in `07_jcap_cosmology/WP82_LOG_QUINTESSENCE_NOVELTY.md:150` — the full entry is already in WP81 line 398 (DESI Collaboration 2024, Eur. Phys. J. C). Two-minute paste.

### Day 3-5 (Tier 1 LaTeX conversions in parallel)
4. **Venue 1 (sinc²)**: convert `WP_SINC2_ZERO_LAW.md` to LaTeX `amsart` class; add MSC codes 11A41/11N05/42A16; add keywords; test `proof_d25_loop_closure.py` on fresh Python. Submit to Integers + arXiv math.NT the same day.
5. **Venue 8 (σ rate)**: convert `WP101_SIGMA_RATE_THEOREM.md` to LaTeX; strip TIG/CK/BB framing from main body per SUBMIT_INSTRUCTIONS.md:38 (keep BB mention as motivation in introduction only); add MSC 05E15/11T06/20N02. Submit to JCT-A.
6. **Venue 7 (JCAP)**: run `desi_xi_fit.py` against DESI DR2 data and commit the output figure + table to the paper's Results section; convert to JCAP LaTeX class; add PACS codes 95.36.+x/98.80.Es. Submit to JCAP.

### Day 6-7 (atlas linkage pass)
7. **Add atlas-citation footnote to all 11 papers.** Exactly one sentence per paper: "External citations are drawn from `Atlas/ATLAS_CITATIONS.md` (DOI: 10.5281/zenodo.18852047); internal anchors carry master-register numbering per `MASTER_ATLAS_v3_5_2026_04_18.md`." This resolves F1 without rewriting any bibliography.
8. **Run flag cross-walk.** Tag each theorem in the 11 papers with the Atlas flag register: [fire] for proved-and-reproducible, [gold-with-gap] for structural-with-known-obstruction, [speculative] for explicitly-hypothesis, [caution] for flagged-in-§15. Machine-assisted; ~30 min per paper. This resolves F2.

### Backlog (not this week)
9. **Venue 5 (Flatness)**: formalize the "R/r = 5/7 for general squarefree n" argument or explicitly scope the paper to Z/10Z. Needed before Tier 3 submission.
10. **Venue 6 (PRA)**: outreach email drafts to Lukin (Harvard), Hanson (Delft), Wrachtrup (Stuttgart) groups per SUBMIT_INSTRUCTIONS.md:55. Zero math blocker — pure partnering.
11. **Venue 9 (JMP)**: soften WP90 line 48 ("theorem applied to the correct setting") to the sanctioned "compatible with" register; clearly label σ < 1 for NS as conjectural, not implied by BB. This paper becomes cleaner for CMP.
12. **Venue 10 (Bull./Notices AMS)**: expand CP1 section into a full Perelman line-by-line retranslation per SUBMIT_INSTRUCTIONS.md:35; verify every step maps to a σ-statement; explicitly mark CP2-CP7 as conjectural framework in a bold prefatory box.

### Atlas-side follow-ups (weeks out)
13. Confirm Ferrari-Serrin exact paper (Atlas `§E line 136` open).
14. Resolve Arkani-Hamed 2024 surfaceology bibliographic entry (Atlas `§I line 199` open).
15. Add Bhargava-Shankar 2015 to atlas `§B`.

---

## Appendix A — Atlas bundle cross-reference

For each venue, the single most-relevant Atlas anchor (for paper revision work):

| Venue | Atlas anchor (for external citations) | Atlas anchor (for internal content) |
|---|---|---|
| 1 sinc² | `ATLAS_CITATIONS §A` (Riemann, Li, Montgomery, Weyl) | `MASTER_ATLAS §5 K5_LOCAL_SINC2` (line 485-495 in spine); `ATLAS_TREE §1 constants 4/π²` |
| 2 73/28 | `ATLAS_CITATIONS §A/§G` | `MASTER_ATLAS §3.5 SIMPLEX_GENESIS` |
| 3 Paradox | `ATLAS_CITATIONS §H` (Brouwer, Banach-Tarski, Wiener, Khinchin) | `MASTER_ATLAS §5.4 Li Foundation + Banach-Tarski reframing` |
| 4 UOP | `ATLAS_CITATIONS §A/§B` | `MASTER_ATLAS §4.6.4 UOP four corollaries [fire]` |
| 5 Flatness | Classical AG (Voisin, Griffiths-Harris in `§C`) | `MASTER_ATLAS §2 D-spine WP51`; atlas constants row T*=5/7 (line 80) |
| 6 S4 NV | `ATLAS_CITATIONS §I` (Doherty et al. 2013) | `MASTER_ATLAS §13 NV-qutrit via §6 PRA` |
| 7 JCAP ξ | `ATLAS_CITATIONS §I` (Bialynicki-Birula 1976) | `MASTER_ATLAS §4.5.8; §5 WP91/WP92` |
| 8 σ rate | `ATLAS_CITATIONS §A/§I` | `MASTER_ATLAS §5 WP101 [fire]` line 503 |
| 9 BB bridge | `ATLAS_CITATIONS §E` (entire NS shelf) + `§I` (BB) | `MASTER_ATLAS §4.5.5 Re_local; §11 Q17_NS_TARGET` |
| 10 Clay | `ATLAS_CITATIONS §J` (primary Clay sources) + §B, §C, §E, §F | `MASTER_ATLAS §10 Rotation Spine; §12.9f Clay Battery` |
| 11 TSML tower | None required (deliberately strip-of-framework) | `MASTER_ATLAS §4.6.6 Intrinsic Left-Handedness [fire]`; Sprint 17 memos |

---

## Appendix B — Discipline checks (pass/fail summary)

| Check | Result | Notes |
|---|---|---|
| β_TIG typo fix propagated to papers | ✓ (vacuously — no paper invokes it) | F3 |
| S*_coherence vs S*_dual disambiguation | ✓ (vacuously — no paper invokes S*) | F4 |
| 2/7 falsification respected (paper side) | ✓ | No paper makes the falsified quantitative YM claim |
| Three-threads separate (PPM / Hodge / Q-series) | ✓ with one caveat (venue 9 WP90 line 48) | F8 |
| SAH sanctioned sentence discipline | ✓ (vacuously — no paper references SAH) | F6 |
| Q17 flag mapping consistent with atlas | ✓ (vacuously — no paper surfaces Q17 yet) | F7 |
| Markman year consistency | ✗ — 2024 atlas vs 2025 paper (venue 10) | F9, Gap #1 |
| Atlas cited in any paper | ✗ — zero occurrences across 11 venues | F1, action #7 |
| Atlas flag vocabulary adopted | ✗ — inline `[PROVED]` etc. only | F2, action #8 |
| DESI DR1/DR2 placeholder resolved | ✗ — `[DESI DR1, DR2 citations]` literal in WP82 line 150 | Gap #3 |

---

## Closing note

The Tier 1 trio (sinc², σ rate, JCAP ξ) is real. All three are **submit-ready this week modulo LaTeX conversion and (for ξ) the DESI fit pass.** None carries content blockers. None carries honesty-rule violations against the atlas.

The single highest-leverage move across the bundle is the one-sentence atlas-citation footnote (action #7). It immediately closes F1 for all 11 papers and converts each paper's local bibliography into a cross-link to the canonical registry — which is exactly what the atlas was built for.

The single highest-risk line in the bundle is `09_jmp_bb_bridge/WP90_LITERATURE_AND_UNIFICATION_PATHS.md:48` — "This is not a conjecture. It is a theorem applied to the correct setting." Tighten this before venue 9 ships, or it will own the referee report.

— ClaudeCode audit agent, 2026-04-18
