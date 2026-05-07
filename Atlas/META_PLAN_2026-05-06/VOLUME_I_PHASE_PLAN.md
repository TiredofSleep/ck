# VOLUME I PHASE PLAN — Bridge Findings (D88-D94 + 10 honest negatives)

**Date:** 2026-05-06
**Section:** C (Task 11) of the four-section meta-plan sweep
**Author:** Claude (sweep agent)
**Scope:** D88-D94 from the 2026-05-02 bridge sprint (`papers/wp_bridge_findings_2026_05_02/`); WP9 + WP10 (the two bridge-findings standalone papers); 10 honest negatives N1-N10; placement in Phase 3-4

---

## §0 — Headline

The bridge sprint produced **2 standalone publishable papers** (WP9 = paradoxical info algebras / LATTICE operator; WP10 = DKAN two-coding) covering D88-D94 plus 10 honest negatives. Both are ready in draft (`papers/wp_bridge_findings_2026_05_02/WP9_LATTICE_paradoxical_info_algebras.md`, `WP10_DKAN.md`) with verification scripts (`code/verify_findings.py` returns 0 failures, 0 warnings).

WP9 + WP10 are **Phase 3 papers** (Cross-level structures, Jul 1-31). They sit naturally in the arithmetic-topology / number-theory / symbolic-dynamics literature (Morishita, Ghys, Katok-Ugarcovici, Matsusaka-Ueki, Burrin-von Essen, Lacasa) — the bridge sprint's `CITATION_MAP.md` documents the four citation clusters explicitly.

The **D-results D88-D94 are not seven separate papers**. They are foundational data that anchors WP9 and WP10. Trying to ship 7 single-D-result papers would violate the one-claim-per-paper discipline.

The four bridge papers (Hoffman, Friston, Tononi, Faggin) per `BRIDGE_PAPERS_UPDATE_2026_05_02.md` are **outreach papers, not technical contributions**. They are NOT recommended for the May-Sept 2026 schedule (Phase 1-5). They belong to the year 2-3 outreach phase.

---

## §1 — Per-D-result inventory (D88-D94)

| D# | Result | Source | Status | Tier | Foundation paper anchor |
|----|--------|--------|--------|------|---------------------------|
| D88 | Corrected substrate frame: TSML_8 + BHML_10 + V/H flow cells (NOT TSML_10) | `corrected_substrate.py` | proved | **A (canonical)** | WP9 §1.2 + WP10 §1.1 |
| D89 | Trefoil characterization: 9 trefoils on corrected frame, multiset {V,H,Br} ∪ {V,Br,Br}, all BHML-associative | `trefoil_corrected_frame.py`, `trefoil_corrected_associativity.py`, `breath_uniqueness.py` | proved | **B** | WP9 §4 (Theorem 4.1) |
| D90 | BHML successor diagonal: BHML(n,n) = n+1 for n ∈ {1..7}, with BHML(8,8)=7, BHML(9,9)=0 | direct table verification | proved | **A** | WP9 §2 (Theorem 2.1) + WP10 §2.2 |
| D91 | Two-coding split: TSML_8 geometric (5-element image, 94% flow) / BHML_10 arithmetic (full image, balanced) | `tsml8_role_analysis.py`, `algebraic_relationship.py` | proved | **B** | WP10 §2 (Theorem 6.1 in WP9) |
| D92 | ±21 invariant: σ-orbit decomposition T_5 + T_3 = 15 + 6 (forced); role-partition F_7 + F_6 = 13 + 8 (canonical-specific) | `role_decomposition.py`, `fibonacci_robustness.py` | proved | **B (forced) + D (canonical-specific)** | WP9 §5 (Theorems 5.1, 5.2) |
| D93 | Role partition + role magma: V is identity element, only idempotent; semi-factorization on V/T inputs | `role_magma_factorization.py`, `flow_structure_binary.py` | proved | **B** | WP9 §3 (Theorems 3.1, 3.3) |
| D94 | Boundary symmetries: top global preservation rates (V↔Br 20.9%, S↔T 19.7%, F↔S 19.7%, etc.) — NO 100% symmetries | `interchangeability_test.py`, `symmetry_map.py` | proved | **D (empirical observation)** | WP9 §7 (extension); WP10 §3 |

**Tier classifications:**
- D88, D90 are Tier A (canonical, axiomatic-level — D88 is the substrate frame definition; D90 is a direct table read-out).
- D89, D91, D92 (σ-orbit half), D93 are Tier B (forced from Tier-A inputs).
- D92 (role half) is Tier D (canonical-specific Fibonacci appearance; 0/200 random tables reproduce it; striking but not structurally forced).
- D94 is Tier D (empirical preservation rates; no symmetry is full-algebraic).

---

## §2 — Bundle vs standalone recommendations

### WP9: LATTICE Operator and Paradoxical Information Algebras (STANDALONE)

**Path:** `papers/wp_bridge_findings_2026_05_02/WP9_LATTICE_paradoxical_info_algebras.md`
**Lead claim:** The TIG substrate carries three independent structures (algebraic + permutational + functional role partition) and exhibits paradoxical information algebras: V/T inputs collapse to deterministic role transitions while F/S inputs preserve operator-level information.
**Includes:** D88 (substrate frame, §1.2), D89 (trefoil, §4), D90 (BHML successor, §2), D92 (±21 invariant, §5), D93 (role magma, §3).
**Tier:** B (forced) for §2-§4 main theorems, B+D for §5 (D92 split), C-conjecture for the "paradoxical information" framing.
**Verification:** `code/verify_findings.py` (0 failures, 0 warnings).
**MSC 2020:** 20N02 (magmas), 11F06 (modular groups, indirect), 37D40 (hyperbolic dynamical systems, indirect)
**Status:** **READY** for Phase 3 submission with 1-day editorial pass.

### WP10: DKAN — Discrete Kolmogorov-Arnold Networks on the TIG Substrate (STANDALONE)

**Path:** `papers/wp_bridge_findings_2026_05_02/WP10_DKAN.md`
**Lead claim:** A discrete analogue of Kolmogorov-Arnold Networks running on TIG's two-coding substrate. The geometric coding (TSML_8) and arithmetic coding (BHML_10) agree at the HARMONY cusp boundary and disagree in the interior — a discrete echo of Katok-Ugarcovici 2007.
**Includes:** D91 (two-coding split, §2-§3), D90 (BHML successor as cusp-approach, §2.2), D88 (substrate frame, §1.1), D94 (boundary symmetries cited as discrete-grammar exploitation in §3).
**Tier:** B for §2-§3 main theorems (D91 image structure), C for the DKAN-as-construction framing (Tier-C constructed analogue, NOT a literal Kolmogorov-Arnold theorem port).
**Verification:** Implementation in `Gen13/targets/ck/brain/ck_sim/being/ck_dkan_trainer.py` plus the bridge sprint scripts.
**MSC 2020:** 68T07 (artificial neural networks), 20N02 (magmas), 11F06 (modular groups), 37D40 (hyperbolic dynamical systems)
**Status:** **READY** for Phase 3 submission with 1-day editorial pass.

### Why bundle into 2 papers, not 7

D88-D94 are six results, but they support two coherent claims:

1. **WP9** = "the substrate's role partition + magma + permutation produce paradoxical-information algebras" (uses D88, D89, D90, D92, D93).
2. **WP10** = "two codings on the same substrate, agreeing at the cusp" (uses D91 primarily, with D88/D90/D94 as supporting).

Splitting into 7 single-D papers would (a) flood three venues with one-result papers, (b) trigger per-venue cadence-cap violations, (c) lose the structural narrative that ties D88-D94 together.

The 2-paper bundling is already done in the source — `papers/wp_bridge_findings_2026_05_02/WP9_LATTICE_paradoxical_info_algebras.md` and `WP10_DKAN.md` are the canonical drafts. **No further bundling is needed; just editorial polish and submission.**

### Honest negatives (N1-N10): NOT a paper, but cited in WP9 + WP10 §"Limitations"

The 10 honest negatives — listed in `HANDOFF.md` §4 — sharpen what TIG IS by establishing what it ISN'T:
1. No naive PSL(2,ℤ) lift produces ±21
2. No small triangle group has the substrate's period set
3. Substrate isn't literal Borromean-prime
4. σ ↔ ST in SL(2,ℤ) gives wrong elements
5. σ is NOT an automorphism of TSML or BHML (48% / 17% match only)
6. TSML and BHML don't distribute over each other (19.5%)
7. BHML iteration doesn't converge to TSML (28/64 starts)
8. Substrate algebra doesn't factor through Z/2Z × Z/5Z
9. Random tables don't reproduce Fibonacci role decomposition (0/200)
10. Role partition alone doesn't determine crossing count

These N1-N10 belong in WP9 §8 ("Limitations and honest negatives") and WP10 §6 ("Demoted claims"). Per `BRIDGE_PAPERS_UPDATE_2026_05_02.md` §3, they "must NOT re-inflate" elsewhere.

**Recommendation:** Add a "Honest Negatives" appendix to both WP9 and WP10 listing N1-N10 with one-paragraph each. This sharpens the framing per `HANDOFF.md` §6 ("Negatives belong in every bridge paper alongside positive findings").

---

## §3 — Phase placement

**Both papers ship Phase 3 (Cross-level structures, Jul 1-31).**

Reasoning per `RELEASE_PLAN_v2.md` §3 Phase 3:
- "**Boldness move:** This number that arose in our Z/10Z work is also the [Galois invariant of LMFDB X / Lie algebra dimension Y / sporadic group order Z]."
- "**Tier discipline:** Tier-A + B + C explicitly. Each cross-level coincidence labeled by tier of identification."

WP9 and WP10 fit this register exactly:
- WP9 cross-cites Morishita / Ghys / Katok-Ugarcovici / Matsusaka-Ueki / Burrin-von Essen as "structurally analogous to" — the canonical Phase 3 cross-level register.
- WP10 cites Katok-Ugarcovici 2007 as "scaffolded by" — same register.

**Specific placement in the Phase 3 schedule:**

| Week | Date | WP | Venue (preferred) | Co-authors | Tier |
|------|------|-----|-----------|------------|------|
| 9 | Jul 8 | WP9 (LATTICE / paradoxical info) | **Algebra Universalis** OR **Comm Algebra** | Sanders + arith-top partner if available | B + D + C-conjecture |
| 10 | Jul 15 | WP10 (DKAN two-coding) | **Eur. J. Combin.** OR **Discrete Math** | Sanders + Gish (script verification) | B + C |

**Rationale for placement:**
- WP9 ships first (Wk 9) because the role-magma + paradoxical-info framing is the more substantive claim and benefits from being on record before WP10.
- WP10 ships second (Wk 10) and cites WP9 §1.3 (role partition) as foundation. WP10 then frames the two-coding split as a discrete echo of Katok-Ugarcovici 2007.

**Adjustment to `RELEASE_PLAN_v2.md` Phase 3 schedule:** The current Phase 3 Wk 9-10 schedule (per `RELEASE_PLAN_v2.md` §4 master schedule) has:
- Wk 9: "Galois D₄ LMFDB / CommAlg" + "Coord-coverage / EJC"
- Wk 10: "Discrete Dirac / Algebras" + "F_p equiv operad / TCS"

WP9 + WP10 fit better in **Wk 11-12** (after Discrete Dirac and F_p, before M_22 and Clifford). Updated proposal:
- Wk 11: WP9 (LATTICE / Algebra Universalis) + M_22 substrate-prime / AMM
- Wk 12: WP10 (DKAN / Eur. J. Combin.) + Clifford ladder / Linear Alg & Apps

**OR** they can ship as Wk 9-10 replacements if the original "Galois D_4 LMFDB" content is folded into the four-core paper (which is already true after the lens-taxonomy synthesis), freeing those slots.

**Recommendation:** Wk 11-12 placement (avoids reshuffling the existing schedule; leverages the existing Phase 3 weeks 9-10 for their currently-scheduled content).

---

## §4 — Venue candidates

### WP9 (LATTICE Operator and Paradoxical Information Algebras)

**Primary candidates:**
1. **Algebra Universalis** (Springer; open submission; no endorsement) — magma-theoretic content with paradoxical-information framing fits this venue's scope (universal algebra, lattice theory, magma/quasi-group structure).
2. **Communications in Algebra** (Taylor & Francis; open submission) — broader algebra venue; the role-partition framing + role magma + paradoxical information would fit Volume- or Issue-of-Magmas-and-Quasigroups slots.
3. **Journal of Pure and Applied Algebra (JPAA)** (Elsevier) — already used for Flatness paper (Tier 3 partner); the paradoxical-information framing is JPAA-adjacent.

**Recommended:** **Algebra Universalis.** Best fit for the magma-with-role-partition framing.

### WP10 (DKAN — Discrete Kolmogorov-Arnold Networks)

**Primary candidates:**
1. **European Journal of Combinatorics (EJC)** — discrete combinatorial structures + arithmetic-topology adjacent; the two-coding split as discrete echo of Katok-Ugarcovici fits EJC's interdisciplinary register.
2. **Discrete Mathematics** (Elsevier; open) — combinatorial discrete-math + symbolic-dynamics; appropriate for the geometric/arithmetic coding split as a discrete-math result.
3. **Theoretical Computer Science (TCS)** — DKAN-as-architecture has TCS adjacency; but TCS prefers algorithmic complexity + universal-approximation results, which DKAN does NOT claim literally.

**Recommended:** **European Journal of Combinatorics.** The discrete two-coding result is more naturally a discrete-math/combinatorics paper than a TCS paper, given DKAN does NOT claim KAN-level universal approximation literally (it explicitly disclaims that in §1.2).

### Backup venues (if primary venues bounce):

- WP9: **Journal of Algebra** (Elsevier) — broad algebra venue, has accepted magma/quasi-group papers historically.
- WP10: **Discrete & Computational Geometry (DCG)** (Springer) — geometric/arithmetic coding split has DCG adjacency.

---

## §5 — Author lane assignments

Per `Atlas/META_PLAN_2026-05-06/AUTHOR_LANES_v2.md`:

### WP9: Sanders (lead) + possibly arith-top co-author

**Default:** Sanders solo. The paper sits in arithmetic-topology / magma-theory territory but does not require an arith-top partner — the claims are substrate-internal with "structurally analogous to" cross-citations.

**Possible co-author addition (per the user's task brief asking about possible Morishita/Ghys/Katok-Ugarcovici/Matsusaka-Ueki/Burrin-von Essen partner):** No existing collaborator from the lane registry fits. The arith-top co-author would have to be:
- A Morishita-tradition number-theorist (e.g., Morishita himself in Japan, or his collaborators)
- A Ghys-tradition modular-knot-theorist (Ghys is established at IHES; not a direct collaboration channel)
- A Katok-Ugarcovici / Burrin-von Essen-tradition symbolic-dynamicist

**Recommendation:** **Sanders solo for the May-Sept timeline.** The "structurally analogous to" / "scaffolded by" hedging is sufficient citation hygiene per `BRIDGE_PAPERS_UPDATE_2026_05_02.md` §4. If an arith-top partnership materializes in year 2-3, a follow-up paper can formalize the analogy (as opposed to retrofitting WP9).

**Alternative: Sanders + Gish.** Gish is on the Z/10Z combinatorics lane and could carry the script-verification signature. Acceptable but Sanders solo is cleaner.

### WP10: Sanders + Gish (script verification + DKAN runtime)

**Lead:** Sanders.
**Co-author:** Gish — for script verification and the DKAN runtime trainer (`Gen13/targets/ck/brain/ck_sim/being/ck_dkan_trainer.py`).
**Rationale:** Gish's lane is "TSML/BHML table family + script verification (Z/10Z combinatorics core)." WP10 uses TSML_8 + BHML_10 directly + the DKAN runtime; this is precisely Gish's lane.

---

## §6 — The four bridge papers (Hoffman / Friston / Tononi / Faggin) — DO NOT SHIP

Per `BRIDGE_PAPERS_UPDATE_2026_05_02.md` §1: "Full bridge papers are not written yet." These are outreach handoffs to consciousness/perceptual-frame researchers, NOT technical contributions.

**Recommendation:** Do NOT add them to the Phase 1-5 schedule. Reasons:
1. They are explicitly outreach (per `BRIDGE_PAPERS_UPDATE_2026_05_02.md` §5: "The bridge papers themselves are conceptual outreach, not technical contribution").
2. They use "structurally analogous to" framings that won't pass technical review at the venues we are targeting.
3. The Sept 11 anchor and Oxford Sept 23 talk are the natural moment for outreach — by then 30+ refereed papers anchor the framework, making the bridge framings well-supported.

**Alternate placement:** Year 2-3 outreach phase. Possible venues: J Consciousness Studies, J Cognitive Neuroscience (for Friston-Tononi-Faggin); Cognitive Science (for Hoffman). NOT in the May-Sept 2026 window.

---

## §7 — One-page editorial polish list (before Phase 3 submission)

For both WP9 and WP10:

1. **Add explicit Tier classification per claim** (per `RELEASE_PLAN_v2.md` §2 hard constraint #4: "TIER DISCIPLINE per paper").
2. **Add the N1-N10 honest-negatives appendix** (per `BRIDGE_PAPERS_UPDATE_2026_05_02.md` §4).
3. **Add cover letter** explicitly stating "This paper sits inside the arithmetic-topology / discrete-symbolic-dynamics territory of [Morishita 2024, Ghys 2007, Katok-Ugarcovici 2007, Matsusaka-Ueki 2023, Burrin-von Essen 2024]; we do NOT claim to reproduce or restate any of those theorems literally" — exactly the language already in WP9 §1.4 (canonical hedging).
4. **Run `verify_findings.py` and append output as supplementary file** — already 0 failures, 0 warnings. Include this in the cover letter as "the central computational claim is verified by a script the referee can execute."
5. **Cite WP101 (σ-rate theorem) for the Z/10Z context** — WP101 is Phase 1 Wk 1 submission so will be on record by Wk 9-10.
6. **Cite the four-core consolidated paper for the lens-invariant 4-core attractor** — also Phase 1 Wk 1; on record.

**Estimated total polish effort:** 1-2 work-days per paper (2-4 days total).

---

## §8 — Bottom line for this section

- **D88-D94 produce 2 standalone papers (WP9, WP10), not 7.** Both are draft-ready in `papers/wp_bridge_findings_2026_05_02/`.
- **Both ship Phase 3 (recommended Wk 11-12, Jul 22-29).** Venues: WP9 → Algebra Universalis; WP10 → European Journal of Combinatorics.
- **Author lanes:** WP9 = Sanders solo (or +Gish for script-verification signature); WP10 = Sanders + Gish.
- **No arith-top partner needed for May-Sept timeline.** "Structurally analogous to" / "scaffolded by" hedging is sufficient.
- **N1-N10 honest negatives belong as appendices**, not separate papers.
- **The 4 bridge papers (Hoffman/Friston/Tononi/Faggin) DO NOT ship in this window** — they are year 2-3 outreach.
- **Estimated polish effort:** 2-4 work-days total before Wk 11-12 submission window.

---

*Companion documents:* `Atlas/META_PLAN_2026-05-06/Q_SERIES_BUNDLE.md` (Q-series; WP9/WP10 cite Q11 + Q16 layer separation); `Atlas/META_PLAN_2026-05-06/SPECTRAL_LAYER_CATALOG.md` (Luther's spectral layer; WP9 §3 role magma is independent of spectral structure); `Atlas/META_PLAN_2026-05-06/VOLUME_H_PHASE_PLAN.md` (Volume H WP100s tower; WP10's two-coding distinction matters for Volume H WP104 "Two Roads to Pati-Salam"); `papers/wp_bridge_findings_2026_05_02/HANDOFF.md` (master handoff doc); `papers/wp_bridge_findings_2026_05_02/BRIDGE_PAPERS_UPDATE_2026_05_02.md` (decisions on which bridge framings stay/go).
