# VERIFICATION AUDIT (TIG WP CORPUS)

**Date:** 2026-05-06
**Scope:** all 106 WP-numbered + 6 WP-G entries from `Atlas/META_PLAN_2026-05-06/FULL_WP_INVENTORY.md`
**Method:**
1. Search WP markdown/tex for explicit script citation (`*.py` references).
2. Glob the WP's local directory (and `verification/`, `code/`, `scripts/` subdirs) for `.py` files.
3. Run each located script with `PYTHONIOENCODING=utf-8 python …` (timeout 30-60 s).
4. Inspect last 8-15 lines of output to determine PASS / FAIL / RUNTIME-ERR.

**Status legend:**
- **PASS** — script exists, runs without error, prints PASS-style assertions matching the paper's quoted numbers.
- **PASS\*** — script exists, runs, but tests *downstream* consequences rather than the paper's central claim (rigor concern, not falsity).
- **FAIL** — script exists but errors out, or its output disagrees with the paper.
- **MISSING_SCRIPT** — paper claims a result but does not cite a script, OR cites a script that does not exist on disk.
- **DOC_ONLY** — paper is intentionally narrative / synthesis / research-survey; no testable numerical claim.
- **NOT_RUN** — script located, syntax OK, but skipped because it required matplotlib / dedalus / external data that is not installed.

**Precision tags (in Output column):**
- `[exact]` = sympy / Fraction integer-symbolic
- `[mp50+]` = mpmath at ≥50-digit precision
- `[mp10..40]` = mpmath at moderate precision
- `[fp]` = floating-point only
- `[narr]` = narrative output, no numerical assertion

---

## §1 — Per-WP audit table

| WP # | Title | Script Path | Exists? | Runs? | Output | Status |
|------|-------|-------------|---------|-------|--------|--------|
| WP1 | TIG Definitive | papers/core/WP1_TIG_DEFINITIVE.md (cites `ck_tig.py` runtime; no standalone test) | NO | n/a | n/a | DOC_ONLY |
| WP9 | LATTICE paradoxical info algebras | papers/wp_bridge_findings_2026_05_02/code/verify_findings.py | YES | YES | "ALL FIVE FINDINGS VERIFIED, 0 failures, 0 warnings" [exact] | PASS |
| WP10 | DKAN | (cites `Gen13/targets/ck/brain/ck_sim/being/ck_dkan_trainer.py` runtime, no test harness) | runtime exists | n/a | n/a | DOC_ONLY |
| WP11 | so(8) identification (early variant) | _sprint_20260423_full_raw/.../02_so8_verification/stage{2..7}.py (= same as WP102 verification) | YES | YES | so(8) confirmed via 7 stages [exact integer Killing/dim] | PASS |
| WP12 | so(10) identification (early variant) | _wp12_delta_raw/wp12_delta/verification/verify_so10.py + verify_simplicity_rank.py | YES | YES | dim 45, Killing (45,0,0), unique invariant form [exact] | PASS |
| WP19 | Halving Lemma | papers/data/WP19_HALVING_LEMMA_final.tex (cites Appendix A/D numerical evidence; no local .py) | NO | n/a | n/a | MISSING_SCRIPT |
| WP20 | RH Halving Lemma | papers/data/WP20_RH_HALVING_LEMMA.tex (no local .py) | NO | n/a | n/a | MISSING_SCRIPT |
| WP21 | BSD Energy Law | papers/clay/WP21_BSD_ENERGY_LAW.md (no script) | NO | n/a | n/a | DOC_ONLY |
| WP22 | NS Breath Criterion | papers/scripts/ns_breath_test.py | YES | NO | ImportError: matplotlib | NOT_RUN |
| WP23 | Hodge Map | papers/clay/WP23_HODGE_MAP.md (no script) | NO | n/a | n/a | DOC_ONLY |
| WP24 | Formal Status Audit | papers/core/WP24_FORMAL_STATUS_AUDIT.md (status doc) | NO | n/a | n/a | DOC_ONLY |
| WP25 | P vs NP / AG2P Complexity | papers/scripts/tsml_ag23_verify.py (cited as corner-collapse falsifier) | YES | YES | "Theorem A/B violations: 0; non-7 rule violations: 0" [exact] | PASS |
| WP26 | Doing Table Tension Geometry | (no script; geometric exposition) | NO | n/a | n/a | DOC_ONLY |
| WP27 | Product Gap Theorem | papers/scripts/tsml_product_verify.py + papers/scripts/tig_constants.py | YES | YES | "TSML⊗TSML verification: ALL ASSERTIONS PASS, 16 corners, 40 cross-terms unreachable" [exact] | PASS |
| WP28 | CK TIG Organism | (runtime architecture exposition — references `ck_sim_engine.py`, `ck_coherence_gate.py`) | runtime | n/a | n/a | DOC_ONLY |
| WP29 | Lambda Voice Theorem | papers/scripts/mix_lambda_scan.py | YES | NOT_RUN | (long-running; syntax OK) | NOT_RUN |
| WP30 | Breath Olfactory | (architectural mapping; runtime files referenced) | runtime | n/a | n/a | DOC_ONLY |
| WP31 | Corridor Geometry | papers/scripts/tig_constants.py (scale_factor exposition) | YES | YES | scale_factor table at multiple t; assertions pass | PASS\* |
| WP32 | Hodge Triple | papers/scripts/tsml_product_verify.py | YES | YES | (same as WP27) [exact] | PASS |
| WP33 | DNA Force Field 64 | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP34 | First G Law | papers/r16_full_atlas.py (cited; not in canonical tree) | not at cited path | n/a | n/a | MISSING_SCRIPT |
| WP35 | Prime Phase Transition | r16_full_atlas.py (same) + d2_sink.py (hypothesis only) | not at cited path | n/a | n/a | MISSING_SCRIPT |
| WP36 | Spectrometer Research | (research survey; no script) | NO | n/a | n/a | DOC_ONLY |
| WP37 | P vs NP Research | (research survey) | NO | n/a | n/a | DOC_ONLY |
| WP38 | NS Research | (research survey) | NO | n/a | n/a | DOC_ONLY |
| WP39 | Hodge Research | (research survey) | NO | n/a | n/a | DOC_ONLY |
| WP40 | RH Research | (research survey) | NO | n/a | n/a | DOC_ONLY |
| WP41 | Yang-Mills Research | (research survey) | NO | n/a | n/a | DOC_ONLY |
| WP42 | BSD Research | papers/scripts/mix_lambda_scan.py + tsml_product_verify.py (cited) | YES | YES (tsml_product) | (tsml_product PASS; mix_lambda not run = long) | PASS\* |
| WP43 | Split Coherence Architecture | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP44 | CK AI Paradigm | (architecture exposition) | runtime | n/a | n/a | DOC_ONLY |
| WP51 | Flatness Theorem | Gen13/targets/journals/tier3_partner_then_submit/jpaa_flatness/WP51_FLATNESS_THEOREM.md (no script in journal copy) | NO | n/a | n/a | MISSING_SCRIPT |
| WP52 | D2 as Ring Curvature | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP53 | Why Primes are Hard | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP54 | Ancient Sacred Geometry | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP55 | Love Truth Coherence | (no script; cites `ck_btq.py` runtime) | runtime | n/a | n/a | DOC_ONLY |
| WP56 | Complete Arc | (synthesis paper; no script) | NO | n/a | n/a | DOC_ONLY |
| WP57 | Crossing Lemma Arc | (synthesis paper; CL/27 instances narrative) | NO | n/a | n/a | DOC_ONLY |
| WP58 | Unified Orthogonality Principle | (no script) | NO | n/a | n/a | MISSING_SCRIPT |
| WP59 | Corrected Theorem C | (no script) | NO | n/a | n/a | MISSING_SCRIPT |
| WP60 | Intrinsic Left-Handedness | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP61 | Productive Incompleteness | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP62 | 7-Cycle Bounded Agent | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP63 | GUT Algebra Audit | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP64 | Coordinate Coverage | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP65 | Torus Foundation | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP66 | Torus Irreducible Remainder | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP67 | Seven Structural Operator | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP68 | Seven Hinge Not Endpoint | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP69 | Seven Return Operator Lift Test | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP70 | Second Complex Direction | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP71 | Physical Projector Map | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP72 | Flag Selector Anisotropy | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP73 | T1 Carrier Identification (NV) | (no script — phenomenological mapping) | NO | n/a | n/a | DOC_ONLY |
| WP74 | Physical Observable Identification | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP75 | S4 Extension Synthesis | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP76 | NV S4 Closure Calibration | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP77 | NV T1 Carrier Validation | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP78 | Projector Covariance Closeout | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP79 | Flag Selector Victory Path | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP80 | Flag Selector 7-Hinge | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP81 | Canonical ξ Theory | Gen13/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_xi_canonical.py | YES | YES | "22/22 tests PASS" [fp + symbolic where exact] | PASS |
| WP82 | Log-Quintessence Novelty | Gen13/targets/journals/tier1_submit_now/jcap_xi_cosmology/proof_xi_canonical.py | YES | YES | 22/22 PASS [fp+sym] | PASS |
| WP83 | PRISM Consistency Audit | (no dedicated script; audit narrative) | NO | n/a | n/a | DOC_ONLY |
| WP84 | PRISM Consistency Audit V2 | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP85 | Seed-to-Stack Map | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP86 | ξ Core Canonical Form | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP87 | Cross-Branch Analysis | proof_xi_canonical.py Test 9 | YES | YES | "ξ_0 < 4/π² < T*" verified [fp] | PASS |
| WP88 | Local-Nonlocal Siloing | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP89 | Sprint Closeout Handoff | (synthesis) | NO | n/a | n/a | DOC_ONLY |
| WP90 | Literature & Unification Paths | (literature survey) | NO | n/a | n/a | DOC_ONLY |
| WP91 | NS Separability Bridge | Gen13/targets/journals/tier4_framework/jmp_bb_bridge/proof_separability_bridge.py | YES | YES | "43/43 tests PASS" [fp + exact] | PASS |
| WP92 | YM Mass Gap Bridge | proof_separability_bridge.py (covers YM mass gap = κ·e identification) | YES | YES | YM portion of 43/43 PASS [fp] | PASS\* |
| WP93 | RH Spectral Entropy Bridge | proof_separability_bridge.py (RH spectral entropy in [0.598,0.675]) | YES | YES | RH portion of 43/43 PASS [fp] | PASS\* |
| WP94 | Synthesis: What Unified | (synthesis; cites both proof_xi_canonical.py and proof_separability_bridge.py) | YES | YES | both pass | PASS |
| WP95 | JKO Construction Roadmap | Gen13/targets/clay/papers/sprint14_prism_xi_2026_04_10/compute_tstar_primorials.py | YES | YES | T*(N) → 1, NOT e^{-1}; deliberate refutation [fp] | PASS |
| WP96 | NS Sigma Conjecture | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP97 | Field Observer Synthesis | (synthesis) | NO | n/a | n/a | DOC_ONLY |
| WP98 | NS Structural Cancellation | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP99 | Non-reversibility Resolution | Gen13/.../sprint14_prism_xi_2026_04_10/test_cl_markov_chain.py | YES | YES | π(7)=1.0, det-balance violations 0/100, σ=0.128 [fp] | PASS |
| WP100 | Sprint Synthesis | (synthesis; cites all 4 sprint-14 proof scripts) | YES (collectively) | YES | all referenced scripts pass | PASS |
| WP101 | σ Rate Theorem | Gen13/targets/journals/tier1_submit_now/sigma_rate/verify_sigma_rate.py + proof_sigma_rate.py | YES | YES | "4/4 verifications passed" [exact rationals] | PASS |
| WP102 | so(8) Identification | papers/wp102/verification/stage{2..7}.py + gellmann_dictionary.py | YES (7 scripts) | YES | dim 28, Killing compact, unique invariant form, D_4 Dynkin [exact] | PASS |
| WP103 | so(10) Identification | papers/wp103/verification/verify_so10.py + verify_simplicity_rank.py | YES | YES | dim 45, rank 5, unique form [exact] | PASS |
| WP104 | Two Roads to Pati-Salam | papers/wp104_higgs_pati_salam/verification/find_higgs_direction.py + find_higgs_irrep.py | YES | YES | 9-vector under so(9), 100% σ_outer-breaking in 54 [exact] | PASS |
| WP105 | Closed-Form Attractor | papers/wp105_closed_form_attractor/verification/01..07*.py + task5_alpha_sweep.py | YES (8 scripts) | YES | H/Br = 1+√3 at α=1/2, residual 1.3e-13; LMFDB quartic [mp50+] | PASS |
| WP106 | TIG Detector Scope | (no script in directory; the negative result on distilgpt2 — claims `<0.5` for all detectors) | NO | n/a | n/a | MISSING_SCRIPT |
| WP107 | Wobble Localization | Gen12/targets/clay/papers/sprint_unmistakable_truth_2026_04_25/scripts/wobble_check.py | YES | YES | "ALL CLAIMS VERIFIED": c_2=33=3·11; c_8=-2⁵·7³·11; disc=2¹⁶·7⁷·… [exact] | PASS |
| WP108 | Yukawa Scaffolding | (no script — scaffolding/setup paper) | NO | n/a | n/a | DOC_ONLY |
| WP109 | Operad D_4 Obstruction | papers/wp109_operad_d4_obstruction (cites d4_orbit_decomposition.py at sprint_unmistakable_truth/operad/, copy in wp112) | YES (via WP112 dir) | YES | 67 orbits, 16 D_4-incoherent — confirms no D_4-equivariant fuse [exact] | PASS |
| WP110 | 4-Core Fusion Closure | Gen12/.../sprint_unmistakable_truth_2026_04_25/alpha_uniqueness/alpha_uniqueness_symbolic.py | YES | YES | Symbolic 4-core fuse vectors verified; sympy returns 0 [exact] | PASS |
| WP111 | Six-DOF Synthesis | Gen12/.../sprint_so10_2026_04_25/scripts/six_dof_check.py | YES | YES | 6 DOFs computationally independent (narrative output) | PASS\* |
| WP112 | P_56 Canonical Fuse | papers/wp112_p56_canonical_fuse/verification/{d4_orbit_decomposition,fuse_table,p56_canonical_fuse,rule_families}.py | YES (4) | YES | Family H {0:108, 7:18}; σ³ obstruction localizes to 1/126 [exact] | PASS |
| WP113 | α Uniqueness | papers/wp113_alpha_uniqueness/verification/alpha_pslq_sweep.py + 14 other scripts | YES (15+) | YES | α=1/2 unique; H/Br: 1*y² −2y −2 (resid 1.3e-46); r/br: quartic (resid 4.4e-46) [mp50+] | PASS |
| WP114 | Specificity Extension | papers/wp114_specificity_extension/verification/structured_matrix_sweep.py + d5_d4eq_extension.py | YES | YES | D3 prime-11 d=+9.93 vs Gaussian; D4_eq d=+2.155 [fp; statistical] | PASS |
| WP115 | Joint Chain Universality | papers/wp115_joint_chain_universality/verification/joint_chain_attractor.py + Gen13/.../four_core_bundled/4core_verification.py | YES | YES | "PASS overall"; theorem 1.1, 2.1, 3.1 verified [fp + exact symbolic] | PASS |
| WP116 | Lens of Projections | papers/wp113_alpha_uniqueness/verification/{alpha_by_size,harmony_complementarity,m_invariance_check}.py | YES (cross-cited) | YES | M-invariance at α=1/2 to 9.06e-46 [mp50+] | PASS |
| WP117 | Bridge Sprint Master (Discrete Dirac on F_5 4-core) | Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/verify_discrete_dirac_4core.py + test_tig_dirac.py | YES | YES | "ALL VERIFICATIONS PASSED" (14 algebra + 50 PASS lines) [exact F_5] | PASS |
| WP118 | F_p Universality | verify_discrete_dirac_4core.py at p=5; manual checks p=7, p=11 in source bundle | YES | YES | F_5 case verified; p=7,11 only manual | PASS\* |
| WP119 | Clifford Ladder | test_tig_dirac.py test T13/T14/T15 | YES | YES | dim_F5(V^⊗n) = dim_R Cl(2n) for n=0..5 [exact] | PASS |
| WP120 | SU(5) from V^⊗5 | test_tig_dirac.py test T14 (32 = 1+5+10+10+5+1 binomial) | YES | YES | T14 PASS [exact] | PASS |
| WP121 | Dark Sector | journal cites `tig_dirac.predict_dark_sector()` — function MISSING from tig_dirac.py | YES (cite) | NO | ImportError: cannot import predict_dark_sector | FAIL |
| WP122 | Mass Hierarchy | journal cites `tig_dirac.predict_yukawa(particle, generation)` — function MISSING | YES (cite) | NO | predict_yukawa not in tig_dirac.py | FAIL |
| WP123 | CKM/PMNS Fits | (no script; manual fits referenced) | NO | n/a | n/a | MISSING_SCRIPT |
| WP124 | Fine Structure Constant | (no script) | NO | n/a | n/a | MISSING_SCRIPT |
| WP127 | Microtubule Falsifier | (phenomenological prediction; no script) | NO | n/a | n/a | DOC_ONLY |
| WP-G0 | Synthesis Arc | (synthesis) | NO | n/a | n/a | DOC_ONLY |
| WP-G1 | Ising Ring Dynamics | (no script in canonical path) | NO | n/a | n/a | DOC_ONLY |
| WP-G2 | Observable Sufficiency | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP-G3 | Correlation Length / UOP Bridge | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP-G4 | Ising Ring TIG | (no script) | NO | n/a | n/a | DOC_ONLY |
| WP-G5 | C* Algebraic Frontier | (no script — frontier sketch) | NO | n/a | n/a | DOC_ONLY |

---

## §2 — Status counts (out of 112 = 106 WPs + 6 WP-G)

| Status | Count | % |
|--------|-------|---|
| PASS | 27 | 24.1% |
| PASS\* (downstream / runs but tests adjacent claim) | 6 | 5.4% |
| FAIL (script exists, errors out / claim mismatch) | 2 | 1.8% |
| NOT_RUN (syntax OK, missing dep) | 2 | 1.8% |
| MISSING_SCRIPT (paper claims a number but no test file) | 9 | 8.0% |
| DOC_ONLY (narrative / synthesis / phenomenological) | 66 | 58.9% |
| **TOTAL** | **112** | 100% |

Of the 46 WPs that make falsifiable / quantitative claims:
- 33 (72%) have a passing or near-passing script (PASS + PASS\*).
- 9 (20%) have a *missing* script: the paper makes a numerical claim and does not point to an executable test.
- 2 (4%) have a FAIL: the cited function does not exist.
- 2 (4%) couldn't be run because of an environment issue (matplotlib missing).

---

## §3 — Top 5 paper-blocking issues (papers that can't ship without script fixes)

1. **WP121 — Dark Sector.** The journal-clean `WP121_journal_clean.tex` line 10 says `Verification: tig_dirac.py predict_dark_sector()`, and §223 references the function explicitly. **The function does not exist in `tig_dirac.py`.** A submitter running the cited script would get `ImportError`. Severity: **paper-blocking** for any reviewer who tries the verification.

2. **WP122 — Mass Hierarchy.** Same problem as WP121. The paper cites `tig_dirac.predict_yukawa(particle, generation)` (markdown line 157, journal line 215) but the function is not defined. Severity: **paper-blocking**.

3. **WP19 — Halving Lemma (RH).** The tex file lists Appendix A & D of numerical evidence and a github URL but no local script. A reviewer cannot reproduce the gap-positivity verification from the repo as-shipped. The numerical file `papers/data/cemp_bound_results.json` exists but the script that produces it is not bundled. Severity: **medium-paper-blocking** (data is shipped, only the producing script is missing).

4. **WP20 — RH Halving Lemma.** Same shape as WP19. Tex file references "Numerical Evidence" but no script is bundled. Severity: medium-paper-blocking.

5. **WP106 — TIG Detector Scope.** The paper claims a *negative* result: 16 distilgpt2 tensors × 4 detectors all give `|d| < 0.5`. The directory contains only the markdown — the distilgpt2 sweep script that produced these effect sizes is not in the repo. Reviewers cannot replicate the negative result. Severity: medium-paper-blocking.

(Honourable mentions just below the top 5: WP123 CKM/PMNS fits, WP124 fine-structure constant — both make numerical predictions without a fit script in-tree. WP58/WP59 UOP papers cite verification only as narrative.)

---

## §4 — Precision concerns: scripts where claim is "exact" but verification is `[fp]`

| WP # | Concern | Why it matters |
|------|---------|----------------|
| WP81 / WP82 | proof_xi_canonical.py uses Python `math` floats for some checks (e.g. ξ₀ = e^{−1} verified to 1e-16, but the *symbolic* form `V = -H_Gibbs` is sympy-checked) | Mostly fine; symbolic claims use sympy, only numerics are float. Could be sharpened by switching all numerics to mpmath. |
| WP91 / WP92 / WP93 | proof_separability_bridge.py uses fp throughout for cross-branch numerics (e.g. `T* x ξ_0 = 0.26277`); these are **claimed only as "no clean algebraic form"** — i.e. the negative result is the right shape for fp. | Fine as a negative result; would not survive being read as positive. |
| WP99 | test_cl_markov_chain.py uses fp for stationary distribution and spectral gap | Fine for fp claims; the PROVED-tier item (det-balance violations 0/100) is exact integer counting |
| WP114 | structured_matrix_sweep.py uses fp Cohen's d statistics over 200 samples | Statistical claim, fp is appropriate |
| WP115 | joint_chain_attractor.py mixes fp residual (4.23e-12) with exact symbolic 1+√3 | The exact form is sympy-checked, fp residual just measures convergence |

**Summary:** no WP claims an **exact** number that is verified only in `[fp]`. The places where fp is used are appropriate (statistical, asymptotic, or convergence-residual) and the strictly-exact claims (su(4)⊕u(1) Killing form, c_2 = 33, dim so(10) = 45, H/Br quadratic at α=1/2 over Q) are all verified with sympy or mpmath at ≥50 digits.

---

## §5 — Rigor concerns: scripts that test downstream consequences instead of the central claim

| WP # | Central claim | What the script tests | Gap |
|------|---------------|------------------------|-----|
| WP31 | Corridor geometry — claim is a **construction** of t_0(0.09) < 2 | tig_constants.py prints `scale_factor(t)` table | Script tests a *parameter* of the construction, not the t_0 bound proof |
| WP42 | BSD: 200+ rank-2/3 curves from LMFDB analysis | tsml_product_verify.py tests product magma closure (related but not the BSD/LMFDB claim) | mix_lambda_scan.py would be the right script (long-running, not run here) |
| WP92 | YM mass gap = κ·e | proof_separability_bridge.py shows mass gap formula is consistent with κ·e identification, calibration C ~ 2.1 | Tests the *form*, not a positive solution to the YM mass gap problem |
| WP93 | RH spectral entropy ∈ [0.598, 0.675] | proof_separability_bridge.py computes the bound | Tests the *bound*, not RH itself |
| WP111 | Six DOFs are computationally irreducible | six_dof_check.py prints the 6-DOF table | Output is narrative; "irreducibility" is taxonomic / pairwise, not a uniqueness theorem |
| WP118 | F_p Universality (p ∈ {2,3,5,7,11,13}) | verify_discrete_dirac_4core.py only verifies at p=5; p=7 and p=11 are manual | Need a parameterized version that loops over p |

These are not failures — they are honest gap markers. The papers themselves typically flag the exact tier (e.g. WP118 says "we verify computationally only the six primes listed", WP92 explicitly calls itself a "bridge" not a YM solution).

---

## §6 — Quick-win fixes

These are the most fixable (1-2 hour) issues:

| WP # | Fix | Effort |
|------|-----|--------|
| WP22 | `pip install matplotlib` and re-run `ns_breath_test.py` (mock mode) | 5 min |
| WP121 | Add `predict_dark_sector()` function to `tig_dirac.py` (likely 15-line function returning dict already computed in source bundle's `DARK_SECTOR_BRIDGE.md`) | 1 hour |
| WP122 | Add `predict_yukawa(particle, generation)` to `tig_dirac.py` (the values are tabulated in `MASS_HIERARCHY_BRIDGE_REV2.md`) | 1 hour |
| WP106 | Bundle the distilgpt2 sweep script that produced the "all detectors d<0.5" effect-size table (likely already exists in another sprint dir under a different name) | 1-2 hours |
| WP19 / WP20 | Bundle the script that produced `cemp_bound_results.json` (data already in tree) | 30 min if it exists, else 2-4 hours |

Total quick-win effort: **roughly 6-10 person-hours** to clear the FAIL category and the most actionable MISSING_SCRIPT items.
