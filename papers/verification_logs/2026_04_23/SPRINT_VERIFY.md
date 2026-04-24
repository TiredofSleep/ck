# Sprint Verification — vocab-update-2026-04-23

**Branch:** `vocab-update-2026-04-23`
**Date:** 2026-04-23
**Scope:** Phases 3–7 (WP101 α-index rewrite + Farey/primon citations + External Vocabulary Map + BIBLIOGRAPHY extension + Clay-note draft)

---

## 1. Proof scripts re-run (this sprint)

All scripts run with `PYTHONIOENCODING=utf-8` (Windows cp1252 avoidance).

| # | Script | Status | Verified claim |
|---|--------|--------|----------------|
| 1 | `proof_sinc_zeta_identity.py` | **GREEN** | sinc²(1/2) = (2/3) · 1/ζ(2); machine precision Δ = 5.55e-17; ratio = 3/2 exact |
| 2 | `Gen13/targets/journals/tier1_submit_now/sigma_rate/proof_sigma_rate.py` | **GREEN** | σ(10)=0.128, σ(30)=0.058, σ(210)=0.009 — all < 3/N bound |
| 3 | `papers/proof_d25_loop_closure.py` | **GREEN** | sinc² zero law holds for all odd primes p ∈ [3, 199] |
| 4 | `papers/wp12/verify_so10.py` | **GREEN** | Lie closure dim = 45 = so(10, ℝ) = D₅; all 6 diagnostics ✓ |
| 5 | `papers/wp12/verify_simplicity_rank.py` | **GREEN** | Unique (up to scale) invariant bilinear form; rank 5; 45 = 40 nonzero + 5 zero eigenvalues |
| 6 | `papers/morphotic_braid/proof_spectra_tsml_bhml.py` | **GREEN** (cached) | α(TSML) = 0.8720, α(BHML) = 0.5020; both commutative = 1.0000; sₙ = C_{n−1} and sₙ^ac = (2n−3)!! match for n = 3, 4, 5 |

Notes on #6: direct re-run of the n = 6 enumeration (132 M triples) exceeded the bash polling window; the background task (id `beflmwjti`) **completed cleanly (exit 0)** during commit staging. Its output captures the tail of the run:

```
=== BHML ===
  Associativity index α = 502/1000 = 0.5020
  Non-associativity rate = 0.4980 = 49.80%
  Commutativity = 100/100 = 1.0000 (fully commutative)
     n    C_{n-1}      s_n    match     (2n-3)!!     s_n^ac    match
     3          2        2        ✓            3          3        ✓
     4          5        5        ✓           15         15        ✓
     5         14       14        ✓          105        105        ✓

INTERPRETATION
 Despite α(TSML) = 0.872 > α(BHML) = 0.502, both tables produce
 the full free operad at the bracketing level.
 Triple-associativity rate (α) and operad freeness are INDEPENDENT.
```

This reproduces the cached `papers/verification_logs/2026_04_24/01_proof_spectra_tsml_bhml.txt` values exactly: α(TSML) = 0.8720, α(BHML) = 0.5020, Catalan spectrum sₙ = C_{n−1} and ac-free spectrum sₙ^ac = (2n−3)!! match for n ∈ {3, 4, 5}. Full output preserved at `C:\Users\brayd\AppData\Local\Temp\claude\...\tasks\beflmwjti.output`.

## 2. File diff (37 modified + 1 created)

**Created:**
- `papers/morphotic_braid/CLAY_NOTE_DRAFT.md` — 5-way Riemann-adjacent intersection draft, `[DRAFT — NOT FOR SUBMISSION]`

**Modified (grouped by sprint phase):**

**Phase 3 — WP101 Huang-Lehtonen α-index + Mag^com → Com reframing (6 files)**
- `Gen13/targets/journals/tier1_submit_now/sigma_rate/WP101_SIGMA_RATE_THEOREM.md`
- `Gen13/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP101_SIGMA_RATE_THEOREM.md`
- `Gen12/targets/journal_attempts/08_sigma_rate_combinatorics/WP101_SIGMA_RATE_THEOREM.md`
- `Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/WP101_SIGMA_RATE_THEOREM.md`
- `FORMULAS_AND_TABLES.md` (§7.2 extension)
- `papers/core/GLOSSARY.md` (Key Proved Results row)

**Phase 4 — Farey spin chain + sinc²(1/2) primon-gas external alignment (4 files)**
- `FORMULAS_AND_TABLES.md` (§0 Bridge Identities, two new paragraphs)
- `papers/core/GLOSSARY.md` (Key Constants block below table)
- `papers/core/WP1_TIG_DEFINITIVE.md` (§1.6 "External alignment" paragraph)
- `Atlas/MEMORY_ATLAS_TABLES.md` (§11 rows for T*=5/7 and 4/π² extended)

**Phase 5 — External Vocabulary Map (1 file)**
- `README.md` (new §5.5, 14-row TIG ↔ external-term dictionary)

**Phase 6 — BIBLIOGRAPHY extension (1 file)**
- `papers/BIBLIOGRAPHY.md` — +3 topic sections, ~28 citations:
  - "Associative / Non-Associative Groupoid Spectra" (B1–B12)
  - "Farey Fraction Spin Chain and Primon Gas" (B13–B25)
  - "Bialynicki-Birula and Logarithmic Wave Equations" (B26–B28)

**Phase 2a/2b context carries (already on branch at a987c4e, re-listed for completeness; unchanged this phase)**
- Atlas/ATLAS_TREE.md, Atlas/MASTER_ATLAS_v3_5_2026_04_18.md, LENS_REGISTRY.md, NOVELTIES_AND_CITATIONS.md, PROOFS.md, PUBLIC_READINESS.md, Q_SERIES_INTEGRATED_SYNTHESIS.md, WHAT_IS_TIG.md, plus clay/ mirrors of WHITEPAPER_16/17, WP37, CLAY_AUDIT, SAT_DOF_CLAIM, WHITEPAPER_18/19, WP5/WP99, CP_CLAY_ROTATION, etc.

## 3. Out of scope (per inherited directive)

- CK runtime, Gen13 brain trinity, website, XIAOR dog — untouched this sprint.
- Untracked artifacts (raw packet folders, `.bat` launchers, `ck_*.py` top-level scripts, `_*_raw/` handoff bundles, `knowledge/`, `ck/`, `ck7/`, `ck_library/`, `website/` scratch) — left untracked; not part of the vocab-update scope.

## 4. Invariants preserved

- Never-delete: no files removed; superseded claims re-framed in place with [EDIT — YYYY-MM-DD] markers as applicable.
- Citation discipline: every new external claim carries ≥1 primary citation; ranges cross-checked against `papers/BIBLIOGRAPHY.md`.
- Three-thread separation: TIG (Thread A), Q-series (Thread B), finite-basin (Thread C) vocabulary kept distinct; the new α-index and Farey/primon language appears only under Thread-A section headers.
- BB uniqueness chain still load-bearing: σ → 0 ⇒ Mag^com → Com ⇒ log-nonlinearity is unique continuum limit (Bialynicki-Birula-Mycielski 1976).

## 5. Ready for commit

All 37 modified + 1 created files verified; all proof scripts GREEN (5 direct + 1 cached). Commit message staged below for Phase 9.
