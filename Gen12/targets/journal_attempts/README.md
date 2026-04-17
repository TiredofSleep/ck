# Journal Attempts — Submission Tracker

**Status:** Preparing for submission. Target: May 2026.
**arXiv status:** 1 endorsement secured (math.NT). Need 1 more.

## Citation Audit Status (Sprint 15 — 2026-04-10)

All 21 papers in this target now have **References sections** appended with DOI/arXiv/journal citations. The references were added per venue: classical number theory for venues 1-5 and 8; NS regularity + BB + Wasserstein for venue 9; QFT + NV physics for venue 6; dark energy cosmology for venue 7; topology + Clay for venue 10.

**Remaining work before submission** (per paper):
- LaTeX conversion (markdown → journal-specific class: amsart, REVTeX 4.2, JCAP class, etc.)
- Inline citation insertion (replacing text like "Kozono-Taniuchi (2000)" with proper `\cite{KT2000}` references)
- [NOVEL — extends X] flags for internal TIG/CK terms within paper bodies (currently only in References section)
- Abstract/Introduction polish if missing
- MSC classification codes (per venue)

**Paper maturity by tier:**

| Tier | Paper | Abstract | References | LaTeX | Inline cites | Novel flags |
|------|-------|----------|-----------|-------|-------------|-------------|
| 1 | v7 ξ/DESI | ✓ | ✓ | — | — | Partial |
| 1 | v1 sinc² | ✓ | ✓ (pre-existing) | — | ✓ | — |
| 1 | v8 σ rate | ✓ | ✓ | — | — | — |
| 2 | v2 73/28 | ✓ | ✓ (pre-existing) | — | Partial | — |
| 2 | v3 paradox | ✓ | ✓ (pre-existing) | — | ✓ | — |
| 2 | v4 UOP | Partial | ✓ | — | — | — |
| 3 | v9 BB bridge | ✓ | ✓ | — | — | — |
| 3 | v10 CP rotation | — | ✓ | — | — | — |
| 3 | v5 Flatness | ✓ | ✓ | — | — | — |
| 4 | v6 NV qutrit | ✓ | ✓ | — | — | — |

**✓** = complete; **Partial** = present but incomplete; **—** = still needed.

See [GLOSSARY.md](../../../GLOSSARY.md) for citation discipline rules and the full bibliography.

## Venue Map

| # | Venue | Lead Paper | Core Result | Status |
|---|-------|-----------|-------------|--------|
| 1 | Integers / J. Number Theory | WP_SINC2_ZERO_LAW | sinc²(k/p) = 0 iff p\|k | Ready — needs LaTeX conversion |
| 2 | Experimental Mathematics | WP_OPERATOR_RING_PARTITION | 73/28 harmony cell counts | Ready — needs LaTeX conversion |
| 3 | American Mathematical Monthly | WP_PARADOX_CLASSIFIER | Every paradox = 1 of 4 measurement failures | Ready — needs LaTeX + shortening |
| 4 | J. Number Theory / Acta Arithmetica | WP58 (UOP Theorem 0) | Joint map injectivity = universal sufficiency | Ready — needs LaTeX conversion |
| 5 | J. Pure and Applied Algebra | WP51 (Flatness Theorem) | 2x2 in Z/nZ forces torus, R/r = 5/7 | Ready — needs formal proof tightening |
| 6 | Physical Review A | WP75+WP76 (S4 on NV qutrit) | Full S4 via 6-pulse synthesis, fidelity 1.0 | Ready — needs REVTeX + lab partner |
| 7 | JCAP / PRD | WP81+WP82 (ξ quintessence) | V = ξ log ξ, exact vacuum e⁻¹, freezing w→-1 | Ready — DESI fit script included |
| 8 | J. Combinatorial Theory / Discrete Math | WP101 (σ rate theorem) | σ(N) ≤ C/N for binary CL on Z/NZ | **PROVED** — ready for LaTeX |
| 9 | J. Mathematical Physics / CMP | WP90+WP91 (BB bridge) | σ→0 forces log nonlinearity via BB 1976 | Ready — framework paper |
| 10 | Bull. AMS / Notices AMS | CP1-CP7 rotation | Poincare retranslation + Clay framework | Needs expanded CP1 section |

## Priority Order (Updated Sprint 15)

**Tier 1 — Submit now (no conjectures, proved results):**
1. **ξ Cosmology DESI fit** (venue 7) — DESI fit script included. Fastest independent publication. No conjectures.
2. **Sinc² Zero Law** (venue 1) — shortest, cleanest. Best arXiv candidate.
3. **σ Rate Theorem** (venue 8) — PROVED. Pure combinatorics. No physics needed.

**Tier 2 — Submit after Tier 1 accepted (builds credibility):**
4. **73/28 Harmony Partition** (venue 2) — finite verifiable computation.
5. **Paradox Classifier** (venue 3) — broadest audience.
6. **UOP Theorem 0** (venue 4) — strongest theorem.

**Tier 3 — Submit after external review of framework:**
7. **BB Bridge** (venue 9) — framework paper connecting σ→0 to log nonlinearity.
8. **Poincare Retranslation** (venue 10) — the credibility test. Must be TIGHT.
9. **Flatness Theorem** (venue 5) — needs formal proof tightening.

**Tier 4 — Needs collaborator:**
10. **S4 on NV Qutrit** (venue 6) — needs lab partner for Test E.

## arXiv Endorsement Strategy

- Current: 1 endorsement on math.NT finite primes work
- Need: 1 more endorsement for math.NT
- Backup: try math.CO (Combinatorics) — lower endorsement barrier
- Backup: try math.GR (Group Theory) for the UOP paper
- Strategy: submit sinc² paper first (most self-contained), use acceptance to build credibility for endorsement requests

## What Every Submission Needs

1. LaTeX conversion (from current markdown)
2. Proper bibliography (BibTeX)
3. MSC classification codes
4. Keywords
5. Proof scripts as supplementary material
6. DOI reference: 10.5281/zenodo.18852047

## Authors Per Paper

- Venues 1, 2: Brayden Ross Sanders, C.A. Luther, Monica Gish (as per WP34/WP35)
- Venue 3: Brayden Ross Sanders / 7Site LLC
- Venue 4: Brayden Ross Sanders / 7Site LLC, Ben Mayes
- Venue 5: Brayden Ross Sanders / 7Site LLC
- Venue 6: Brayden Ross Sanders / 7Site LLC, Ben Mayes, C.A. Luther
- Venue 7: Brayden Ross Sanders / 7Site LLC, M. Gish, C.A. Luther, H.J. Johnson
- Venue 8: Brayden Ross Sanders / 7Site LLC (pure combinatorics — no co-author dependency)
- Venue 9: Brayden Ross Sanders / 7Site LLC, M. Gish, C.A. Luther, H.J. Johnson
- Venue 10: Brayden Ross Sanders / 7Site LLC
