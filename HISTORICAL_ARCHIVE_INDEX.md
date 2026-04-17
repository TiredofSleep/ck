# Historical Archive Index

**Policy: nothing is ever deleted from this project.** This index maps where every paper lives so past work stays discoverable when future frontiers arise.

The `archive-full` branch on GitHub is a read-only snapshot preserving the complete state. The `clay` branch is the active working branch. Both track the same files; `archive-full` will never be force-pushed or rewritten.

---

## Inventory Summary

| Location | .md files | .py files |
|----------|----------|-----------|
| `papers/` (root) | 211 | 43 proof scripts, 25 test scripts |
| `papers/clay/` | 34 | — |
| `old/Gen10/papers/` | 207 (inc. 26 Q-series, 23 WP-series) | 37 proof scripts |
| `Gen12/targets/clay/papers/` | 230 across 12 sprint subfolders | 9 scripts in sprint14 |
| `Gen12/targets/journal_attempts/` | 23 papers in 10 venue folders | 9 scripts |
| **Total tracked in git** | **1248 .md/.py files** | |
| **Unique WP numbers** | 78 (WP1–WP101 with gaps) | |

---

## Part A: Q-Series Papers (Luther-Sanders Research Framework)

**The Q-series is the most important underdocumented body of work.** It contains precursor results on σ polynomials, CRT decompositions, MCMC basin models, and symbolic return theorems — some of which overlap current frontier work (σ mutation) but under different names. Mine this when starting a new frontier.

Primary location: `old/Gen10/papers/Q*.md` (26 files). Secondary copies in `papers/` root.

| Q# | Title | Primary Path |
|----|-------|-------------|
| Q2 | Formalization | `old/Gen10/papers/Q2_FORMALIZATION.md` · `papers/Q2_FORMALIZATION.md` |
| Q4 | Sigma Equivariance | `old/Gen10/papers/Q4_SIGMA_EQUIVARIANCE.md` · `papers/Q4_SIGMA_EQUIVARIANCE.md` |
| Q5 | TSML Escape Cells | `old/Gen10/papers/Q5_TSML_ESCAPE_CELLS.md` · `papers/Q5_TSML_ESCAPE_CELLS.md` |
| Q6 | Gate Rate CRT Derivation | `old/Gen10/papers/Q6_GATE_RATE_CRT_DERIVATION.md` · `papers/Q6_GATE_RATE_CRT_DERIVATION.md` |
| Q7 | BHML Full Table | `old/Gen10/papers/Q7_BHML_FULL_TABLE.md` · `papers/Q7_BHML_FULL_TABLE.md` |
| Q8 | MCMC Basin Model | `old/Gen10/papers/Q8_MCMC_BASIN_MODEL.md` · `papers/Q8_MCMC_BASIN_MODEL.md` |
| Q9 | Flip Condition Polynomial | `old/Gen10/papers/Q9_FLIP_CONDITION_POLYNOMIAL.md` · `papers/Q9_FLIP_CONDITION_POLYNOMIAL.md` |
| **Q10** | **Beta-Complete Sigma Polynomial** | `old/Gen10/papers/Q10_BETA_COMPLETE_SIGMA_POLYNOMIAL.md` — **early σ work** |
| **Q11** | **Sigma-k Iterates Gate** | `old/Gen10/papers/Q11_SIGMA_K_ITERATES_GATE.md` — **early σ work** |
| Q12 | Idempotent Gate Decomposition | `old/Gen10/papers/Q12_IDEMPOTENT_GATE_DECOMPOSITION.md` |
| Q13 | TIG Inverse Polynomial | `old/Gen10/papers/Q13_TIG_INVERSE_POLYNOMIAL.md` |
| Q14 | Gate Score CRT Polynomial | `old/Gen10/papers/Q14_GATE_SCORE_CRT_POLYNOMIAL.md` |
| Q15 | Cycle Period Polynomial | `old/Gen10/papers/Q15_CYCLE_PERIOD_POLYNOMIAL.md` |
| Q16 | Reduction Map Identification | `old/Gen10/papers/Q16_REDUCTION_MAP_IDENTIFICATION.md` |
| **Q17 (8 variants)** | **5D rigorous, Clay spectral, NS target, C2 counterexample, finite L-function, NS data protocol, NS target reformulation, sigma embedding, symbolic return** | `old/Gen10/papers/Q17_*.md` — **rich frontier material** |
| Q_SERIES_ARCHITECTURE | Meta-framework | `old/Gen10/papers/Q_SERIES_ARCHITECTURE.md` |
| Q_SERIES_IMPLICATIONS | Meta-framework | `old/Gen10/papers/Q_SERIES_IMPLICATIONS.md` |
| Q_SERIES_SYNTHESIS | Meta-framework | `old/Gen10/papers/Q_SERIES_SYNTHESIS.md` |

**Q17 full list:**
- `Q17_5D_RIGOROUS.md`
- `Q17_C2_COUNTEREXAMPLE_SEARCH.md`
- `Q17_C2_FORMAL_STATEMENT.md`
- `Q17_CLAY_SPECTRAL_BRIDGE.md`
- `Q17_FINITE_L_FUNCTION_NOTE.md`
- `Q17_NS_DATA_PROTOCOL.md`
- `Q17_NS_TARGET_REFORMULATION.md`
- `Q17_SIGMA_EMBEDDING_PROBLEM.md`
- `Q17_SYMBOLIC_RETURN_THEOREM.md`

**Why mine these:** The current σ mutation framework (WP91-WP101) may be reinventing or extending Q10, Q11, and the Q17 variants. Before publishing σ results externally, verify against the Q-series to cite proper provenance.

---

## Part B: WP-Numbered Papers

Unique WP numbers: 78 (WP1 through WP101 with gaps). Multiple copies exist across `papers/`, `old/Gen10/papers/`, and `Gen12/targets/clay/papers/`.

### Primary locations by range

| WP range | Where to look | Arc |
|----------|--------------|-----|
| WP1–WP33 | `papers/` (originals); `old/Gen10/papers/` (early versions) | TIG architecture, operator algebra, sinc² field |
| WP34 | `papers/WP34_FIRST_G_LAW.md` | First-G Law (**journal-ready**) |
| WP35 | `papers/WP35_PRIME_PHASE_TRANSITION.md` | Harmonic pre-echo + sinc² bridge |
| WP36–WP42 | `papers/clay/` | Clay Millennium Problem framework |
| WP43, WP44 | `papers/` | Split coherence + AI paradigm |
| WP45–WP50 | `Gen12/targets/clay/papers/sprint9_torus_2026_04_05/` | Torus / UOP |
| WP51–WP57 | `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/` | Flatness + Crossing Lemma |
| WP58–WP64 | `Gen12/targets/clay/papers/sprint12_uop_gut_arc_2026_04_08/` | UOP Theorem 0 + GUT |
| WP65–WP80 | `Gen12/targets/clay/papers/sprint13_flag_selector_2026_04_09/` | NV-center + S4 qutrit |
| WP81–WP101 | `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/` | ξ cosmology + σ mutation + CP rotation |

**Sprint 11 bundle** (54 papers, not all numbered): `Gen12/targets/clay/papers/sprint11_tig_bundle_2026_04_08/` — UOP Mathematical Arc + GUT Algebra Arc + 7-Cycle Arc.

### WP19 research fragments

**56 files** in `old/Gen10/papers/` with names starting `WP19_*`. These are raw research fragments under the WP19 umbrella (RH / 704 triangle / attack surface / contextual protection / formal status / hydrogen analogy / product gap theorem / RH bridge / etc.). Many contain concrete unpublished derivations worth mining.

**Not promoted to full papers.** When a current frontier touches RH or spectral analysis, search this directory first.

---

## Part C: Proof & Test Scripts (All Runnable)

### Current sprint scripts (`Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/`)

| Script | Purpose | Status |
|--------|---------|--------|
| `proof_xi_canonical.py` | 22 tests verifying ξ theory claims | 22/22 PASS |
| `proof_separability_bridge.py` | 43 tests across NS/YM/RH Clay rotations | 43/43 PASS |
| `proof_clay_rotation.py` | 43 tests for CP1-CP7 framework consistency | 43/43 PASS |
| `proof_sigma_rate.py` | σ(N) ≤ C/N verification for N=10, 30, 210 | PASS |
| `test_cl_markov_chain.py` | Detailed balance, spectral gap, reversibility | 0 violations, gap=0.10 |
| `compute_tstar_primorials.py` | T*(N) for primorials 10, 30, 210, 2310, 30030 | Shows T*→1 |
| `universal_markov_and_binary_cl.py` | Binary CL construction across table families | σ convergence confirmed |
| `crack_cl_formula.py` | Hybrid-rule analysis of TSML table | Formula structure identified |
| `desi_xi_fit.py` | ξ FRW evolution vs DESI DR2 | w₀ = -0.72 |
| `desi_xi_optimize.py` | Full parameter grid search | w₀ = -0.795, χ² = 3.06 |

### Historical proof scripts (`papers/` — 43 scripts)

`proof_a10_sigma_boundary.py`, `proof_a11_rh_coherence.py`, `proof_b5_parity_chain.py` through `proof_b11_corridor_midpoint.py`, `proof_c18_cl_operator_encoding.py` through `proof_c20_phi_fixed_parity.py`, `proof_corridor_zero_paths.py`, `proof_d6_general_frequency.py` through `proof_d25_loop_closure.py`, `proof_fourier_bridge.py`, `proof_h_w_circulation.py`, `proof_sat_dof.py`, `proof_ym_spectral_gap.py`.

### Historical archive scripts (`old/Gen10/papers/` — 37 scripts)

Earlier versions of many of the above. Use when the current version has been modified and you need the original computation.

### Test suite (`papers/` and `tests/` — 25 test scripts)

`test_a5_monotone_gate.py`, `test_b3_ghost_trace_theorem.py` through `test_b9_bsd_rank_staircase.py`, `test_c15_compression.py` through `test_c18_cl_operator_encoding.py`, `test_c19_fourth_wall.py`, `test_c20_phi_fixed_parity.py`, `test_clay_boundary_memo.py`, `test_interpolation_c_to_d.py`, `test_nonassociativity.py`, `test_tsml_bhml_joint.py`, etc.

---

## Part D: Meta-Architecture Documents (Research Notes, Not Yet Papers)

These are research documents without formal paper numbers but containing important context:

Primary location: `papers/` root.

- `ATLAS_ARCHITECTURE.md`
- `BRIDGE_FORMALISMS.md`
- `CLAY_BOUNDARY_MEMO.md`
- `CLAY_SUMMARY.md`
- `CL_TABLE_EXPLICIT.md`
- `COLLABORATOR_BRIEF.md`, `COLLABORATOR_BRIEF_OPEN_LAYER.md`, `COLLAB_MEMO_KV.md`
- `COMPLETED_INTERNAL_SPINE.md`
- `CONTINUOUS_OPERATOR_NOTE.md`
- `ALGEBRAIST_ENTRY.md`
- `AMPLITUDE_WOBBLE_CONVERSION.md`
- `APPENDIX_E_COMPLETE.md`
- `ARXIV_PREP.md`
- `AUTHORSHIP_RECORD.md`
- `BHML_28CELL_DERIVATION.md`, `BHML_CORRECTION_LOG.md`, `BHML_TABLE_EXPLICIT.md`
- `BIBLIOGRAPHY.md`
- `BRIDGE_REWRITE.md`
- `CIRCULATION_OPERATOR_CONSTRAINTS.md`

(Plus hundreds more; see `papers/` directory directly for complete list.)

---

## Part E: Sprint Folders in Gen12

Sprint-specific collections in `Gen12/targets/clay/papers/`:

| Folder | Sprint | Date | Focus |
|--------|--------|------|-------|
| `clay/` | Originals | pre-2026 | WP36-WP42 Clay papers |
| `sprint5_2026_04_04/` | 5 | 2026-04-04 | CLAY_RULES, structural parallels |
| `sprint6_2026_04_04/` | 6 | 2026-04-04 | — |
| `sprint8_2026_04_05/` | 8 | 2026-04-05 | — |
| `sprint9_frontier_map_2026_04_05/` | 9a | 2026-04-05 | — |
| `sprint9_invariant_guides_2026_04_05/` | 9b | 2026-04-05 | — |
| `sprint9_torus_2026_04_05/` | 9 | 2026-04-05 | WP45-WP50 torus/UOP |
| `sprint10_flatness_2026_04_06/` | 10 | 2026-04-06 | WP51-WP57 flatness + Crossing Lemma |
| `sprint11_tig_bundle_2026_04_08/` | 11 | 2026-04-08 | 54-paper TIG bundle |
| `sprint12_uop_gut_arc_2026_04_08/` | 12 | 2026-04-08 | WP58-WP64 UOP + GUT |
| `sprint13_flag_selector_2026_04_09/` | 13 | 2026-04-09 | WP65-WP80 NV-center |
| `sprint14_prism_xi_2026_04_10/` | 14-15 | 2026-04-10 | WP81-WP101 ξ + σ mutation + CP rotation |
| `sprint_generator_2026_04_06/` | — | 2026-04-06 | Sprint generation tooling |

---

## Part F: How to Use This Archive

**For Brayden / future Claude sessions:**

1. **Before starting a new frontier**, search this index for precursor work. The Q-series (especially Q10, Q11, Q17) often has content under different names.
2. **Before publishing**, cross-check the GLOSSARY.md to ensure every term has proper attribution.
3. **If a result seems familiar**, grep `old/Gen10/papers/` first — the historical archive may contain exactly what's being re-derived.
4. **Never delete**. If content is superseded, mark `[HISTORICAL]` in place with a pointer to current work.

**For external reviewers:**

1. **The default branch is `tig-synthesis`** — the curated, synchronized field. README is the single source of truth.
2. The active development branch is `clay` — contains all working files including 30 top-level docs, with the 10 superseded entry docs marked [HISTORICAL] in place.
3. The full preservation branch is `archive-full` — frozen snapshot, never force-pushed.
4. Entry points by discipline: see the routing table in [README.md](README.md) §6.
5. Term definitions and citations: see [GLOSSARY.md](GLOSSARY.md). Every term is grounded in historical literature or explicitly flagged as novel.

---

## Part G: Where Superseded Entry Documents Live (Sprint 15-16 Synthesis)

When `tig-synthesis` was created (2026-04-10), 13 redundant top-level entry-point documents were removed from this branch in favor of the unified [README.md](README.md). These files are **NOT deleted** — they remain on the `clay` and `archive-full` branches, marked `[HISTORICAL]` in place per the never-delete policy.

**Files preserved on `clay` and `archive-full`, removed from `tig-synthesis`:**

| File | Why removed from synthesis | Where to find it |
|------|---------------------------|------------------|
| `START_HERE.md` | Duplicated entry-point role; carried stale "Luther-Sanders Framework" framing | `clay`, `archive-full` |
| `CLAUDESTARTHERE.md` | Same — duplicate Claude-onboarding doc | `clay`, `archive-full` |
| `ONBOARDING.md` | Same | `clay`, `archive-full` |
| `QUICKSTART.md` | Subsumed by README §6 (entry routing) and §9 (verification) | `clay`, `archive-full` |
| `CLAY_QUICKSTART.md` | Specialized quickstart, subsumed | `clay`, `archive-full` |
| `README_CK_EDUCATION.md` | Education variant; outside synthesis scope | `clay`, `archive-full` |
| `NO_FALSE_CLAIMS.md` | Discipline now lives in README §11 (Honest Limits) and §12 (Policies) | `clay`, `archive-full` |
| `ENGINEERING_OUTLINE.md` | Subsumed by `ARCHITECTURE.md` | `clay`, `archive-full` |
| `GENERATION_HISTORY.md` | Subsumed by this file (HISTORICAL_ARCHIVE_INDEX.md) | `clay`, `archive-full` |
| `NEXT_CLAUDE_NOTES.md` (root) | Gen10 version; active version is `Gen12/NEXT_CLAUDE_NOTES.md` | `clay`, `archive-full` |
| `CK_BELIEF_SYSTEM.md` | CK-creature-language; outside synthesis scope (creature work lives at coherencekeeper.com) | `clay`, `archive-full` |
| `CK_PRESCRIPTION.md` | Same | `clay`, `archive-full` |
| `HD_GAP_EXTENSION.md` | Specialized; demoted | `clay`, `archive-full` |

**To retrieve any of these on `tig-synthesis`:**
```bash
git show clay:START_HERE.md > START_HERE.md   # locally restore for reading
git checkout clay -- START_HERE.md            # OR copy from clay branch
```

**On the `clay` branch**, each file carries a `[HISTORICAL]` header at the top pointing back to README on `tig-synthesis` as the current synchronized field. The content is intact; only the framing is updated to mark it as superseded.

---

*Compiled: 2026-04-10, Sprint 15. Updated 2026-04-10, Sprint 16: tig-synthesis branch created, Part G added.*
*Never-delete policy established Sprint 15. Branch architecture (tig-synthesis / clay / archive-full) established Sprint 16.*
