# Sprint Index — TIG / CK Research Program

**Author:** Brayden Ross Sanders (7Site LLC)
**Opened:** 2026-04-19
**Scope:** one-line descriptions for every dated sprint folder in the repo.
**Purpose:** let an external reader decode sprint codenames (PRISM-XI, B2 pack, Sprint 34 "Ship the First Three", etc.) without having to open each folder.
**Preservation:** append-only; superseded sprint entries carry `[HISTORICAL]` headers, not deletions.

---

## How to read this index

| Column | Meaning |
|---|---|
| **#** | Sprint number. Gaps are real (Sprint 15 rolled into 16; there is no Sprint 7 under this numbering). |
| **Slug** | The folder name on disk. |
| **Date** | ISO-8601 opening date of the sprint folder. |
| **One-liner** | The single load-bearing claim or arc the sprint produced. |
| **Status** | Resolution tag — `[PROVED]`, `[STRUCTURAL]`, `[FALSIFIED]`, `[OPEN]`, `[EDITORIAL]`. |

Every sprint is one unit of work. A sprint folder contains whitepapers (WPxx), a manifest, any proof scripts, and handoff notes.

---

## The table

| # | Slug | Date | One-liner | Status |
|---|---|---|---|---|
| 4 | `sprint4_2026_03_30` | 2026-03-30 | Early ring-theory work on Z/nZ; seed results that later became D1 (First-G Law) and the M+M theorem. | [PROVED] |
| 5 | `sprint5_2026_04_04` | 2026-04-04 | Case-B naildown memo; fixed the first set of internal scoring conventions. | [EDITORIAL] |
| 6 | `sprint6_2026_04_04` | 2026-04-04 | Mathematical-conversations transcript; raw derivation log for later formalization. | [EDITORIAL] |
| 8 | `sprint8_2026_04_05` | 2026-04-05 | **Admissible Viewpoint Flow** memo (AVFT). The n=2p case of the Crossing Lemma — the cleanest canonical proof instance. | [PROVED] |
| 9t | `sprint9_torus_2026_04_05` | 2026-04-05 | Bloom-session torus work; consolidated the six derivations of T\* = 5/7 into `CL_TORUS_TOPOLOGY_PAPER.md`. | [PROVED] |
| 9f | `sprint9_frontier_map_2026_04_05` | 2026-04-05 | Frontier-map memo; named the four-way frontier between proved / structural / conjectural / editorial. | [EDITORIAL] |
| 9i | `sprint9_invariant_guides_2026_04_05` | 2026-04-05 | Invariant-guides memo; specified IG1–IG5 (engine invariants for CK's memory writes). | [STRUCTURAL] |
| 10 | `sprint10_flatness_2026_04_06` | 2026-04-06 | **Flatness Theorem (WP51)** on Z/10Z + **CROSSING_LEMMA.md** (formal statement). WP57 = 27-instance catalog of the Crossing Lemma across the whole arc. | [PROVED] |
| 11 | `sprint11_tig_bundle_2026_04_08` | 2026-04-08 | TIG sprint bundle; UOP Arc, GUT Algebra Arc, 7-Cycle Arc. Co-author: Ben Mayes. | [STRUCTURAL] |
| 12 | `sprint12_uop_gut_arc_2026_04_08` | 2026-04-08 | **WP58 (Unified Orthogonality Principle)** + GUT + 7-Cycle; formalization pass on UOP. Co-author: Ben Mayes. | [STRUCTURAL] |
| 13 | `sprint13_flag_selector_2026_04_09` | 2026-04-09 | **Physical Flag Selector arc** (WP65–WP80) + torus-foundation audit. Co-authors: Ben Mayes, C.A. Luther. | [STRUCTURAL] |
| 14 | `sprint14_prism_xi_2026_04_10` | 2026-04-10 | **PRISM-XI** (Primes · Riemann · Information · Structure · Motion, sprint XI): ξ scalar-field cosmology. V(ξ)=κξ log ξ, vacuum ξ₀=e⁻¹, mass gap m²_ξ=κe. WP81 through WP97 + WP101 σ-rate theorem (`proof_sigma_rate.py`). Co-authors: M. Gish, C.A. Luther, H.J. Johnson. | [PROVED + STRUCTURAL] |
| 16 | `sprint16_basin_handoff_2026_04_10` | 2026-04-10 | Finite-room basin analysis (Thread C); 4 stable invariants + dual reset law. | [STRUCTURAL] |
| 17 | `sprint17_tsml_tower_2026_04_17` | 2026-04-17 | **THEOREM_SPINE** + BHML status note; organized the D1–D25 proof spine into a three-layer tower. | [EDITORIAL + PROVED] |
| 18 | `sprint18_b1_nscg_benchmark_2026_04_17` | 2026-04-17 | **B1 benchmark** — Nested Shell Collapse Generator empirical run. | [STRUCTURAL] |
| 19 | `sprint19_b2_wrg_benchmark_2026_04_17` | 2026-04-17 | **B2 benchmark** — Wobble-Reset Generator empirical run ("the B2 pack"). | [STRUCTURAL] |
| 20 | `sprint20_b3_lbtp_benchmark_2026_04_17` | 2026-04-17 | **B3 benchmark** — Log-Balanced Torus Prior empirical run. | [STRUCTURAL] |
| 21 | `sprint21_structural_discovery_2026_04_17` | 2026-04-17 | Prior-free structural discovery (B1.5 + B2.5 sub-benchmarks). | [STRUCTURAL] |
| 22 | `sprint22_collapse_point_2026_04_17` | 2026-04-17 | N-Stress; located where the collapse point lives on the benchmark grid. | [STRUCTURAL] |
| 23 | `sprint23_curve_recovery_2026_04_17` | 2026-04-17 | Curve recovery — can σ be walked out of T_emp? Preliminary. | [OPEN] |
| 24 | `sprint24_collapse_synthesis_2026_04_17` | 2026-04-17 | Collapse-point synthesis across B1/B2/B3. | [STRUCTURAL] |
| 25 | `sprint25_corridor_closure_proof_2026_04_17` | 2026-04-17 | Corridor closure — algebraic proof for canonical C₀. | [PROVED] |
| 26 | `sprint26_ari_scaling_2026_04_17` | 2026-04-17 | ARI scaling — σ is shell-recoverable in the asymptotic limit. | [STRUCTURAL] |
| 27 | `sprint27_b3_spec_revision_memo_2026_04_17` | 2026-04-17 | B3 specification revision memo. | [EDITORIAL] |
| 28 | `sprint28_curve_recovery_prereg_2026_04_17` | 2026-04-17 | Pre-registration for the curve-based σ-label recovery experiment. | [EDITORIAL] |
| 29 | `sprint29_hodge_r1_kequivariant_2026_04_17` | 2026-04-17 | **Hodge ladder R1** — K-equivariant Chern-class route on A_\*: closure attempt. | [OPEN] |
| 30 | `sprint30_hodge_r1b_r2_r3_2026_04_17` | 2026-04-17 | **Hodge ladder R1b + R2 + R3** — bundle-based Hodge routes on A_\*. | [OPEN] |
| 31 | `sprint31_clay_rotation_2026_04_17` | 2026-04-17 | Clay rotation memo — CP1–CP7 framework. | [STRUCTURAL] |
| 32 | `sprint32_beauville_bsd_hodge_2026_04_17` | 2026-04-17 | Beauville residual — BSD–Hodge synthesis attempt. | [OPEN] |
| 33 | `sprint33_hodge_integrality_2026_04_17` | 2026-04-17 | **S33 gate** — Hodge integrality audit status. | [OPEN] |
| 34 | `sprint34_ship_first_three_2026_04_18` | 2026-04-18 | **"Ship the First Three"** — Tier-1 submission pipeline for three submit-ready papers: sinc² Zero Law (Integers), σ-rate theorem (math.CO), JCAP-ξ cosmology (JCAP). | [EDITORIAL] |
| 35a | `sprint35a_deterministic_rank_2026_04_18` | 2026-04-18 | Sprint 35a verdict — Hodge integrality on A_\*, deterministic. | [STRUCTURAL] |
| 35b | `sprint35b_beauville_explicit_2026_04_18` | 2026-04-18 | Hodge C_\* target note — Beauville explicit form. | [OPEN] |

---

## Codename decoder

Short lookup table for codenames that appear in the README without the full sprint number:

| Codename | Sprint | Slug |
|---|---|---|
| **AVFT** / **Admissible Viewpoint Flow Theorem** | 8 | `sprint8_2026_04_05` |
| **Flatness Theorem** / **WP51** | 10 | `sprint10_flatness_2026_04_06` |
| **UOP arc** / **WP58** | 12 | `sprint12_uop_gut_arc_2026_04_08` |
| **Physical Flag Selector** | 13 | `sprint13_flag_selector_2026_04_09` |
| **PRISM-XI** | 14 | `sprint14_prism_xi_2026_04_10` |
| **B1 / NSCG** | 18 | `sprint18_b1_nscg_benchmark_2026_04_17` |
| **B2 pack** / **WRG** | 19 | `sprint19_b2_wrg_benchmark_2026_04_17` |
| **B3 / LBTP** | 20 | `sprint20_b3_lbtp_benchmark_2026_04_17` |
| **Hodge ladder R1** | 29 | `sprint29_hodge_r1_kequivariant_2026_04_17` |
| **Hodge ladder R1b/R2/R3** | 30 | `sprint30_hodge_r1b_r2_r3_2026_04_17` |
| **Clay rotation memo** | 31 | `sprint31_clay_rotation_2026_04_17` |
| **S33 gate** | 33 | `sprint33_hodge_integrality_2026_04_17` |
| **"Ship the First Three"** / **Sprint 34** | 34 | `sprint34_ship_first_three_2026_04_18` |

---

## Earlier-generation sprints (preserved under `old/Gen10/` and `Gen12/papers/`)

| Path | Note |
|---|---|
| `old/Gen10/papers/sprint4_2026_03_30` | Original sprint-4 artifacts, preserved. |
| `old/Gen10/papers/sprint5_2026_04_04` | Same slug as Gen12 `sprint5_2026_04_04`; Gen10 copy retained per never-delete. |
| `old/Gen11/sprint_memos/` | Gen11-era loose sprint memos; not re-sorted into this index. |
| `Gen12/Sprints/` + `Gen12/Sprints/CK Sprint Archives/` | Raw sprint archives including pre-Gen10 (`sprint3` zip). Preserved intact. |
| `Gen12/papers/sprint7_2026_04_05` | Pre-Gen12 arc; sprint 7 exists at this path only, not under `Gen12/targets/clay/papers/`. |

---

## Co-authors per sprint

| Sprint | Lead + co-authors |
|---|---|
| 1–9 (through torus) | Brayden Ross Sanders (sole) |
| 10 Flatness | Brayden (sole) |
| 11 TIG bundle | Brayden + Ben Mayes |
| 12 UOP/GUT/7-Cycle | Brayden + Ben Mayes |
| 13 Flag Selector | Brayden + Ben Mayes + C.A. Luther |
| 14 PRISM-XI | Brayden + M. Gish + C.A. Luther + H.J. Johnson |
| 16 Basin handoff | Brayden (with chat-Claude handoff) |
| 17 TSML tower + spine | Brayden + C.A. Luther |
| 18–28 B1/B2/B3 benchmarks | Brayden + C.A. Luther |
| 29–35 Hodge ladder | Brayden (tool-assisted: MAGMA / Sage attempts) |
| 34 Ship the First Three | Brayden + ChatGPT + ClaudeChat + ClaudeCode (coordination) |

---

*End of SPRINT_INDEX.md v1. Bumps 1.1, 1.2, … land inline as new sprints open.*
