# Journal Submission Ladder v2 — locked 2026-05-05

**Status:** Replaces Apr-17 v1 and the May 4 working version. This is the **locked May 5 layout** after the four-paper review sprint that produced the FirstJournalSprint050526 package and after the strategic split-call on the 4-core paper.

**Strategy:** Five narrow rigorous papers in five different venues (3 ready-to-ship, 1 to-extract from current bundled draft, 1 held). Mathematically independent — no theorem in any one is used by another. Companion-paper cross-citations weave the citation lattice. No arXiv endorsements required at any venue.

---

## Tier 1 — Ready to Ship This Week

### 1. JCAP — Logarithmic Quintessence
- **Manuscript:** `Gen13/targets/journals/tier1_submit_now/jcap_xi_cosmology/jcap_xi_cosmology_FINAL.tex` (1071 lines, 34/34 LaTeX balanced, 10 review rounds completed)
- **Authors:** B. R. Sanders, M. Gish, H. J. Johnson
- **Headline:** Two-parameter logarithmic-potential quintessence with exact analytic minimum at $\Xi_0 = e^{-1}$. χ²_Gauss = 1.52 vs ΛCDM = 15.26 against DESI DR1 published $(w_0, w_a)$ Gaussian summary. Λ ≈ 1.7 meV.
- **Verification:** `desi_xi_optimize_v2.py` reproduces all manuscript values; `proof_xi_canonical.py` 22/22 algebraic + stability tests.
- **Cover letter:** `cover_letters/jcap_cover_letter.md`
- **Endorsement:** None required (IOP Publishing).
- **Backup venues:** Phys. Rev. D, Physics Letters B (letter form).
- **Status:** Submission-ready. PDF compile + author affiliation confirms (Johnson) + suggested reviewers + Shajib/Frieman 2025 reference title — all in Brayden's manual checklist.

### 2. JCT-A — σ-rate / Non-Associativity Decay
- **Manuscript:** `Gen13/targets/journals/tier1_submit_now/sigma_rate/sigma_rate_theorem_FINAL.tex` (520 lines, 28/28 LaTeX balanced, 8 review rounds completed)
- **Authors:** B. R. Sanders, M. Gish
- **Headline:** σ(N) < 2/N for all squarefree N ≥ 3 with matching lower bound 2(N−2)² − 2φ(N) ≤ σ(N)·N³, giving Nσ(N) → 2 from below as N → ∞ along squarefree integers.
- **Verification:** `verify_sigma_rate.py` 4/4 verifications: Echo lemma exact, σ(N) < 2/N for all squarefree N ≤ 100, ε(N) ≤ 2φ(N) on full test set, asymptotic gap shrinking.
- **Cover letter:** `cover_letters/jcta_cover_letter.md`
- **Endorsement:** None required (Elsevier).
- **Backup venues:** European J. Combinatorics, Discrete Mathematics.
- **Status:** Submission-ready. Suggested reviewers — Brayden's manual checklist.

### 3. Algebraic Combinatorics — 4-core Seed (TO EXTRACT)
- **Source:** `Gen13/targets/journals/tier1_submit_now/four_core_bundled/four_core_FINAL.tex` (1082 lines, 49/49 LaTeX balanced, 3 review rounds completed). The bundled draft contains five theorems: chain (T1), normalizer (T2), closed-form attractor (T3), Galois D_4 (T4), α-sweep observations (T5).
- **Seed-narrow extraction (TO BE WRITTEN):** Keep T1 + T2 + Cor "4-core jointly closed" + σ-walk Remark 3.1 only. Cut T3, T4, T5. Length after cut: ~500-600 lines.
- **Why split:** T3 (the closed-form attractor at α=1/2 with H/Br = 1+√3) and T4 (the D_4 quartic / LMFDB 4.2.10224.1) belong in Paper 2 (algebra). T5 (α-sweep mixing-weight observations + α-uniqueness conjecture) belongs in Paper 3 (dynamics). The seed paper has **no dynamics, no parameter** — chain + normalizer only — leaving maximum room for Papers 2 and 3 to be inevitable rather than redundant.
- **Authors:** B. R. Sanders, M. Gish
- **Verification:** `4core_verification.py` 6/6 checks (chain enumeration, normalizer symbolic, h*/br* = 1+√3 to 10⁻⁴⁵, common attractor across shells, quartic Galois D_4, α-sweep PSLQ).
- **Cover letter (TO BE REVISED):** The bundled draft cover letter `cover_letters/four_core_cover_letter.md` covers the 5-theorem version; needs revision after the seed-narrow .tex exists.
- **Endorsement:** None required (Springer).
- **Backup venues:** Communications in Algebra (Taylor & Francis), Discrete Mathematics (Elsevier), Linear Algebra and its Applications (the Galois layer alone could go here too).
- **Status:** Bundled draft is submission-ready as-is. Strategic decision: extract seed-narrow before submission. Seed-narrow extraction is a Brayden-dispatched .tex edit (likely back through Chat Claude as the .tex editor).

### 4. (Held) — First-G + Sinc²
- **Manuscript:** `four_core_bundled/first_g_sinc2_FINAL.tex` (551 lines, 4 review rounds completed)
- **Status:** Held — headline "smallest k with |G_k(b)| > 0 equals smallest prime factor of b" is essentially definitional once the coprimality partition is named. The sinc² synchronization is real but not enough on its own to land at Integers as a standalone result.
- **Future:** Manuscript and verification script stay in the package as future-Fourier-paper seed material if the harmonic side gets developed further.

---

## Tier 2 — Sprint 18 Follow-on (after Tier 1 lands)

These are the natural downstream papers from the 4-core seed plus the discrete-Dirac Sprint 18 work. All to be drafted/submitted after at least one Tier-1 acceptance lands.

### 5. (Paper 2) — Closed-Form Fixed Point + Galois D_4
- **Source:** Extract Theorems 3 + 4 from the bundled `four_core_FINAL.tex`.
- **Headline:** At α=1/2 the convex-combination iteration on Δ₉ has a unique non-degenerate 4-core-supported fixed point with $p_7/p_8 = 1 + \sqrt{3}$ exactly; $p_9/p_8$ satisfies the irreducible integer quartic $y^4 + 4y^3 - y^2 + 2y - 2 = 0$ with Galois group $D_4$ over $\mathbb{Q}$, generating LMFDB 4.2.10224.1.
- **Target venues (no endorsement):** Communications in Algebra, J. Algebra, Linear Algebra and its Applications.
- **Cites:** seed paper for chain & normalizer (load-bearing), σ-rate paper for the substrate construction (load-bearing companion).
- **Status:** Theorems already in the bundled draft. To be extracted after seed paper lands.

### 6. (Paper 3) — Mixing-Weight Observations + α-Uniqueness Conjecture
- **Source:** Extract Theorem 5 from the bundled `four_core_FINAL.tex`.
- **Headline:** At α∈{0, 1/4, 1/2, 3/4, 1} the runtime fixed-point ratio $p_7/p_8$ admits a small-coefficient quadratic only at α=1/2 (PSLQ verified at deg ≤ 24, coeff ≤ 200, precision 100 digits, denominators ≤ 11). Whether α=1/2 is the unique rational mixing weight in $(0,1) \cap \mathbb{Q}$ with this property is the open question.
- **Target venues (no endorsement):** Experimental Mathematics, Journal of Symbolic Computation.
- **Cites:** seed paper, Paper 2.
- **Status:** Theorem already in the bundled draft. To be extracted after seed paper lands.

### 7. (Paper 4) — F_p Universality of the 4-core Algebra
- **Source:** Sprint 18 WP118 + WP117 V-A asymmetry shadow content. Manuscript exists at `Gen12/targets/clay/papers/sprint18_bridge_dirac_2026_05_04/journals/WP117_journal_clean.tex` and `WP118_journal_clean.tex` (drafts; not yet through full review rounds).
- **Headline:** The 4-core multiplication table over $\mathbb{F}_p$ has the same structural skeleton — 3 non-zero idempotents, Minkowski 1+3 signature under $L_{e_2}$, chirality 2+2 under $L_{e_0}$, empty (massive, right-chiral) eigenspace, $|\mathrm{Aut}(V)| = 40$, power-associativity, 1-dim associator image — for all primes $p \in \{2, 3, 5, 7, 11, 13\}$ tested.
- **Target venues (no endorsement):** Algebra Universalis, Communications in Algebra.
- **Cites:** seed paper for chain & normalizer (the F_p-universality strengthens both Theorems).
- **Status:** Drafts exist; need full cross-review rounds before submission.

### 8. (Paper 5) — Clifford Ladder $V^{\otimes n} \leftrightarrow \mathrm{Cl}(2n)$
- **Source:** Sprint 18 WP119 + WP120 (`WP119_journal_clean.tex`).
- **Headline:** $\dim_{\mathbb{F}_5} V^{\otimes n} = 4^n = \dim_\mathbb{R} \mathrm{Cl}(2n)$ exactly for $n = 0, 1, 2, 3, 4, 5$, with binomial cell decomposition matching the Clifford grade decomposition. At $n = 5$, the binomial $1+5+10+10+5+1 = 32$ matches the SU(5) GUT representation content for one Standard Model fermion generation plus its antimatter conjugate.
- **Target venues (no endorsement):** Linear Algebra and its Applications, J. Mathematical Physics.
- **Cites:** seed paper, Paper 4 (F_p universality of the underlying algebra).
- **Status:** Draft exists; needs full cross-review rounds before submission.

---

## Tier 3 — Microtubule + Other (partner-then-submit)

### 9. (WP127) — Microtubule $Q_c = T^*$ Falsifiable Test
- **Source:** Sprint 18 WP127 (`WP127_journal_clean.tex`) + outreach draft (`outreach/BANDYOPADHYAY_OUTREACH_DRAFT.md`).
- **Headline:** Predicted: microtubule coherence quality factor $Q_c = T^* = 5/7 \approx 0.714$ across multiple sample types, independent of biological origin. Falsification: a single experimental campaign testing 5+ sample types.
- **Target venues (no endorsement):** Journal of Theoretical Biology, Foundations of Physics.
- **Need:** Experimental partner (Bandyopadhyay or equivalent terahertz-coherence lab).
- **Status:** Outreach draft ready; awaits Brayden's send + lab response.

### 10-12 (other Tier-3 venues from earlier ladder)
- American Mathematical Monthly — Paradox Classifier (needs editorial partner)
- JPAA — Forced-Torus Theorem (needs algebra co-author)
- Phys. Rev. A — NV-center qutrit / Physical Test E (needs lab partner)

(See `archived/SUBMISSION_LADDER_v1.md` if needed for details on these legacy entries.)

---

## Tier 4 — Framework / Long-Form (after multi-acceptance)

- JMP — BB bridge (`tier4_framework/jmp_bb_bridge/`)
- Notices of the AMS — Clay Rotation (`tier4_framework/notices_clay_rotation/`)

These are framework-level pieces; hold until Tier-1 + Tier-2 acceptance pattern is established for credibility.

---

## Author bylines (locked)

- **JCAP (paper #1):** B. R. Sanders, M. Gish, H. J. Johnson
- **JCT-A (paper #2):** B. R. Sanders, M. Gish
- **Algebraic Combinatorics (4-core seed paper #3):** B. R. Sanders, M. Gish
- **Future Papers 2/3 (Comm. in Alg / Exp. Math) — extracted from 4-core bundle:** B. R. Sanders, M. Gish
- **Future Papers 4/5 (Algebra Universalis / Linear Algebra & Apps) — Sprint 18:** B. R. Sanders + (TBD)
- C. A. Luther was on earlier drafts of papers #1 and #2; removed from all three Tier-1 papers due to non-responsiveness. Do not re-add.
- Johnson is on the JCAP paper only (cosmology, his domain).

---

## Companion-paper cross-citation policy

Each Tier-1 paper carries a "Preprint, 2026" citation to the other companion(s). Specifically:

- **σ-rate** cites: JCAP companion (continuum dark-energy development of the discrete family); 4-core seed companion (joint-closure structure for the (T,B) pair at N=10 — load-bearing for the 4-core seed paper's "why these two operations" framing).
- **JCAP** cites: σ-rate companion (the discrete origin of the family of which the JCAP scalar is the continuum limit).
- **4-core seed** cites: σ-rate companion (the substrate construction from which T and B are extracted at N=10) — load-bearing per the strategic framing decision.

After the first paper is formally submitted, the corresponding citation in the other two updates from "Preprint, 2026" to "Submitted to [venue], 2026" — but only after Brayden confirms each submission has gone through.

---

## Shared resources

- **Zenodo DOI:** 10.5281/zenodo.18852047 (covers all Tier-1 papers + supporting computational work)
- **Repository:** github.com/TiredofSleep/ck (private; date priority via Zenodo)
- **Verification scripts archive:** all .py files at the same Zenodo DOI

---

## Submission sequencing (this week)

1. **Mon-Tue:** Submit JCAP (paper #1). Post Zenodo first for DOI + visible date proof.
2. **Mon-Tue:** Submit JCT-A (paper #2). Post Zenodo first.
3. **Wed-Fri:** Brayden dispatches the 4-core seed-narrow .tex extraction (likely via Chat Claude as the .tex editor). Once seed-narrow .tex is ready, submit Algebraic Combinatorics (paper #3) with revised cover letter.
4. **Following week:** Tier-2 follow-on planning.

The First-G manuscript stays in the package archive but does not ship in this submission cycle.

---

*Updated 2026-05-05 by Claude Code per the FirstJournalSprint050526 package + the strategic split-call from Chat Claude. Companion: `JOURNAL_LANGUAGE_GUIDE.md`, `PUBLISHING_PLAN_NOW.md`. v2 supersedes the May 4 working version.*
