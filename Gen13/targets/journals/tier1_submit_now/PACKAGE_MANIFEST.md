# Package Manifest — Tier 1 Submissions, May 5, 2026

## Four submission-ready manuscripts (3 in flight + 1 new)

### 1. JCAP — Logarithmic Quintessence

| Property | Value |
|---|---|
| **Source file** | `papers/jcap_xi_cosmology_FINAL.tex` |
| **Lines** | 1071 |
| **LaTeX integrity** | 34/34 begin/end pairs balanced |
| **Authors** | B. R. Sanders, M. Gish, H. J. Johnson |
| **Target venue** | Journal of Cosmology and Astroparticle Physics (JCAP) |
| **Cover letter** | `cover_letters/jcap_cover_letter.md` |
| **Verification script** | `scripts/desi_xi_optimize_v2.py` |
| **Diagnostic script** | `scripts/desi_xi_optimize_signfix_diagnostic.py` |
| **Review rounds completed** | 10 (R1 self + R2 Grok + R3-R10 GPT cross-review) |
| **Final numerical results** | Λ⁴/ρ_{c,0}=0.231, Ξ_i=0.925, w₀=-0.7933, w_a=-0.4497, χ²=1.523 (vs ΛCDM=15.26) |
| **Verification status** | Script reproduces all manuscript values to 3-4 decimals |

**Headline result:** Two-parameter logarithmic-potential quintessence
with exact analytic minimum at Ξ₀ = e⁻¹, fitting DESI BAO + Planck CMB
+ Pantheon+ SNe with χ² ≈ 1/10 of ΛCDM.

---

### 2. JCT-A — σ-Rate Theorem

| Property | Value |
|---|---|
| **Source file** | `papers/sigma_rate_theorem_FINAL.tex` |
| **Lines** | 520 |
| **LaTeX integrity** | 28/28 begin/end pairs balanced |
| **Authors** | B. R. Sanders, M. Gish |
| **Target venue** | Journal of Combinatorial Theory, Series A (JCT-A) |
| **Cover letter** | `cover_letters/jcta_cover_letter.md` |
| **Verification script** | `scripts/verify_sigma_rate.py` |
| **Review rounds completed** | 8 (R1-R3 self + R4-R8 GPT cross-review) |
| **Verification status** | 4/4 verifications pass: Echo lemma exact, σ(N) < 2/N for all squarefree N ≤ 100, ε(N) ≤ 2φ(N) on full test set, asymptotic gap shrinking |

**Headline result:** σ(N) < 2/N for all squarefree N ≥ 3, with
matching lower bound 2(N-2)² - 2φ(N) ≤ σ(N)·N³ giving
Nσ(N) → 2 from below. Proof closed by direct subcase enumeration in
Case 3 (the original draft had a 2× proof gap which was caught by
direct empirical computation in R4 and rigorously closed).

---

### 3. Integers — First-G + Sinc²

| Property | Value |
|---|---|
| **Source file** | `papers/first_g_sinc2_FINAL.tex` |
| **Lines** | 551 |
| **LaTeX integrity** | 29/29 begin/end pairs balanced |
| **Authors** | B. R. Sanders, M. Gish |
| **Target venue** | Integers — Electronic Journal of Combinatorial Number Theory |
| **Cover letter** | `cover_letters/integers_cover_letter.md` |
| **Verification script** | `scripts/verify_first_g.py` |
| **Review rounds completed** | 4 (R1 draft + R2-R4 GPT cross-review) |
| **Verification status** | 5/5 verifications pass: First-G localization for 305 squarefree b in [2,500] (22,367 (b,k) pairs, zero exceptions), closed form below machine epsilon at all primes f∈{3,...,23}, synchronization at canonical test set, continuum limit at t=1/2 and t=1/4, and R(f-1,f)=1/(f-1)² endpoint identity |

**Headline result:** Four-theorem note synchronizing the First-G event
(arithmetic) and the first integer zero of R(k, p₁) (harmonic) at
k = spf(b) for every b > 1.

---

## Shared resources

- **Zenodo DOI:** 10.5281/zenodo.18852047 (covers all three papers
  + the broader supporting computational work)
- **Repository:** github.com/TiredofSleep/ck (private; date priority
  established via the Zenodo DOI)
- **Author byline pattern:** Luther removed from all three (was on
  earlier drafts of papers #1 and #2 but became non-responsive);
  Johnson is on paper #1 only (cosmology, his domain); Gish on all
  three.

## Strategic context

These three papers form Brayden's **Tier 1 foundation triangle** for
the broader TIG / CK research program. Each is independently
submittable to its venue. Once accepted (or even posted as preprints),
they provide the citable foundation for Tier 2 and Tier 3 papers in
the program — every future paper invoking the Ξ field, the CL_N
composition table, or the First-G / sinc² identity can self-cite
into this triangle rather than re-deriving the foundational results.

## What this drop does NOT include

- The CK organism source code (lives in github.com/TiredofSleep/ck)
- WP9 (LATTICE theorem / paradoxical information algebras) — pending
- WP10 (DKAN) — pending
- Any of the proprietary TIG framework documents (T*=5/7 derivation,
  the wider 22-shell structure, BHML/TSML lattice architecture, etc.)
  — these belong in the broader research repo, not in venue submissions
- Material from WP35 that was deliberately excluded from paper #3 (RSA
  hardness inversion, Montgomery bridge, Clay connections, T*=5/7
  retrofit, Balance Invisibility ρ statistic, AI acknowledgments) —
  see the WP35 cleanup decision in transcript notes for rationale

---

### 4. Algebraic Combinatorics — 4-core paper

| Property | Value |
|---|---|
| **Source file** | `papers/four_core_FINAL.tex` |
| **Lines** | 1082 |
| **LaTeX integrity** | 49/49 begin/end pairs balanced |
| **Authors** | B. R. Sanders, M. Gish |
| **Target venue** | Algebraic Combinatorics (alt: Communications in Algebra, Discrete Mathematics) |
| **Cover letter** | `cover_letters/four_core_cover_letter.md` |
| **Verification script** | `scripts/4core_verification.py` |
| **Review rounds completed** | 3 (initial draft + adversarial verification round catching WP115 chain bug + external GPT prose review and Theorem 3 rigorous-existence rewrite) |
| **Verification status** | 6/6 checks pass: chain enumeration matches Theorem 1; normalizer Z_T = Z_B = (v+h+br+r)² verified symbolically; h*/br* matches 1+√3 to ~10⁻⁴⁵ in 99 iterations; common attractor lives on all 7 chain shells; quartic Galois D_4 confirmed; α-sweep PSLQ confirms only α=1/2 admits y²-2y-2=0. Theorem 3 (closed-form attractor) now has a fully rigorous existence + uniqueness proof — no Brouwer, no numerics, no computer algebra. |

**Headline result:** A pair of commutative binary operations on ℤ/10ℤ
admits an 8-element joint-closure chain (sizes {1,4,5,6,7,8,9,10}; sizes
{2,3} forbidden), with a normalizer coincidence Z_T = Z_B =
(v+h+br+r)² on the minimal non-trivial element {0,7,8,9} and a closed-
form runtime attractor at α=1/2 with H/Br = 1+√3 exactly.

**WP115 correction:** Initial draft inherited a chain-counting error
from WP115 preprint (claimed 7 elements, sizes {2,3,7} forbidden).
Brute-force enumeration during manuscript prep showed the chain has
8 elements with size 7 allowed at {0,4,5,6,7,8,9}. The σ-orbit walk
reading is cleaner with the correction: chain walks σ-forward orbit
of 7 (= 7→6→5→4→2→1) with one σ-fixed bridge step at size 7→8 (adds
3 before completing the cycle). FORMULAS_AND_TABLES.md / WP115
source should be updated.

---

## File listing

```
tier1_submissions/
├── CLAUDE_CODE_INSTRUCTIONS.md        2.4 KB    instructions for the agent
├── PACKAGE_MANIFEST.md                this file
│
├── papers/
│   ├── jcap_xi_cosmology_FINAL.tex     ~40 KB   876 lines, 32/32 LaTeX
│   ├── sigma_rate_theorem_FINAL.tex    ~26 KB   606 lines, 31/31 LaTeX
│   ├── first_g_sinc2_FINAL.tex         ~22 KB   553 lines, 29/29 LaTeX
│   └── four_core_FINAL.tex             ~45 KB   1082 lines, 49/49 LaTeX
│
├── scripts/
│   ├── desi_xi_optimize_v2.py          ~10 KB   reproduces JCAP central values
│   ├── desi_xi_optimize_signfix_diagnostic.py   diagnostic for sign convention
│   ├── verify_sigma_rate.py            ~9  KB   4/4 verifications, ~30s runtime
│   ├── verify_first_g.py               ~6  KB   5/5 verifications, ~3s runtime
│   └── 4core_verification.py           ~14 KB   6/6 verifications, ~30s runtime
│
└── cover_letters/
    ├── jcap_cover_letter.md
    ├── jcta_cover_letter.md
    ├── integers_cover_letter.md
    └── four_core_cover_letter.md
```

End of manifest.
