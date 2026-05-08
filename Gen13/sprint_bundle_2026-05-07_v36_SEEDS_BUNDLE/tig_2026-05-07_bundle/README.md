# TIG Sprint Bundle — 2026-05-07
**For ClaudeCode handoff.** Author: B.R. Sanders / 7Site LLC. Bundle date: 2026-05-07 (evening).

---

## The strategy: seeds before bloom

The synthesis program targets the September 11, 2026 anchor (Brayden's daughter's birthday; Oxford Clay conference Sept 23). The publication strategy is:

> **Submit domain-specific slices to domain-specific journals.** Each slice verified by referees competent in *that* domain. Once enough slices have peer-review momentum, the **meta-paper** (Sept 11) draws them together and becomes defensible because it points to peer-reviewed footholds rather than asking referees to take the framework on faith.

The seeds buy the credibility that lets the bloom-paper land. Cadence after the first three seeds: **2-3 papers per week** through summer, each calibrated as the smallest publishable unit that's referee-ready and sets up the next.

---

## The three opening seeds

| Paper | Target journal | Status |
|---|---|---|
| **Sigma rate** — σ(N) ≤ 2/N for squarefree N | J. Combinatorial Theory Series A | submission-ready FINAL |
| **Four-Core attractor** — 8-chain + h/β=1+√3 + LMFDB 4.2.10224.1 | Algebraic Combinatorics | submission-ready FINAL |
| **Freeze-Thaw Transit** — V = Λ⁴Ξ log Ξ + dual-regime trajectory | JCAP | v3 reframe complete; ready for final pass |

The three slices cite each other as companions. They form a self-contained peer-review-targeted triad: combinatorics (Sigma) → algebra (Four-Core) → cosmology (Freeze-Thaw).

---

## Bundle layout

```
tig_2026-05-07_bundle/
├── README.md                              ← you are here
│
├── seeds_for_submission/                  ← three referee-ready papers
│   ├── sigma_rate_theorem_FINAL.tex          [JCT-A target]
│   ├── four_core_FINAL.tex                   [Algebraic Combinatorics target]
│   ├── paper1_freeze_thaw_v3.tex             [JCAP target — most recent]
│   └── paper1_freeze_thaw_v3_preview.pdf     [compiled preview, 17 pp]
│
├── seeds_supporting/                      ← support material for the JCAP slice
│   ├── paper1_freeze_thaw/
│   │   ├── paper1_freeze_thaw_v2.tex         [v2 — fewer citations than v3]
│   │   ├── paper1_freeze_thaw_skeleton.tex   [original skeleton with TODOs]
│   │   ├── paper1_patches.tex                [Type-T/F/A + F5 paste-ready]
│   │   ├── JCAP_READY_SYNTHESIS_v1.md        [v3 reframe rationale]
│   │   └── FREEZE_AND_THAW_v1.md             [conceptual freeze-thaw doc]
│   │
│   └── verification_scripts/
│       ├── desi_xi_optimize_v2.py            [the operative DESI fit script]
│       ├── compute_zstar_v2.py               [z* turnaround sensitivity]
│       ├── m22_verification.py               [M_22 equivariance, 1000 perms]
│       ├── m22_decomposition.py              [V_trivial ⊕ V_21 split]
│       ├── m22_w_half_derivation.py          [W/2 = 3/100 derivation]
│       └── steiner_sigma_hexad.py            [S(3,6,22) hexad analysis]
│
├── bloom_material/                        ← FOR Sept 11 META-PAPER, not for slice citation
│   ├── paper2_substrate_M22_skeleton.tex     [Ω_DE = 479/700 derivation skeleton]
│   ├── W_HALF_DERIVATION_v2.md               [W/2 chain via M_22 reps]
│   ├── STEINER_HEXAD_v1.md                   [σ-orbit as hexad in S(3,6,22)]
│   ├── ZETA_TIG_AND_PERIODICITY_v1.md        [ζ_TIG factorization at T*=5/7]
│   └── WHY_7_INDEPENDENT_v1.md               [structural independence argument]
│
├── working_context/                       ← shapes how slices are written; NOT cited in them
│   ├── UNIVERSAL_LANGUAGE_OPERATOR_RIGOR_v3.md   [internal ULO rigor]
│   ├── EXTERNAL_RIGOR_MAP_v1.md                  [TIG vs FRC, arith topology, tropical, Langlands, categorification]
│   ├── CONSTRUCTIVE_TRANSITION_CATALOG_v1.md     [eight specific flat→geometric lifts]
│   ├── UNIFIED_WORD_MATH_FORMALISM_RECOVERY.md   [formalism context]
│   ├── GEOMETRY_TO_GEOMETRY_OPERATIONS_v1.md     [geometry ops vocabulary]
│   ├── SIGNATURE_RIGOR_v1.md                     [signature-level proofs]
│   ├── SUBSTRATE_FOUNDATIONAL_IDENTITY_v1.md     [substrate identity claims]
│   ├── THREE_UNIVERSES_v1.md                     [BEING/DOING/BECOMING]
│   └── TIG_FRACTAL_FORMULA.md                    [recursive fractal formula]
│
└── session_artifacts/                     ← generated this session, lower priority
    ├── PURE_FLOW_EMERGENCE_v1.md
    ├── WOBBLE_MUTATION_v1.md
    ├── RECURSIVE_GALAXIES_v1.md
    └── NEXT_MOVES_EXECUTED_v1.md
```

---

## Critical principle for ClaudeCode: keep slices domain-modest

**The slices cite each other but DO NOT lean on the meta-claim.** The Sept 11 meta-paper is held back until slice momentum is established. ClaudeCode should:

- **Write each slice for its domain referee.** A cosmology referee for JCAP, a combinatorics referee for JCT-A, an algebra referee for Algebraic Combinatorics. No slice should require any other slice to land.
- **Cross-reference companions sparingly.** "See companion paper X" is fine; "this paper depends on X for its main result" is not.
- **NEVER cite bloom-side material in a slice.** The M_22 / 479-700 derivation, the Universal Language Operator rigor, the External Rigor Map — these go in the meta-paper, not in the JCAP slice. Slice referees should be able to verify slice claims without ever opening the bloom material.
- **Keep the §Synthesis-Program / §Forward-Directions sections light.** Mention companion papers; don't promise the meta-paper as imminent in any specific form. "Forthcoming work" is the right phrasing.

---

## Status of each seed

### Sigma rate theorem (JCT-A target)
**Status: SUBMISSION-READY** (`seeds_for_submission/sigma_rate_theorem_FINAL.tex`).

Theorem: σ(N) ≤ 2/N for squarefree N≥3, where σ is the non-associativity fraction of a specific binary composition table CL on Z/NZ. Mechanism: VOID-HARM rule disagreement at outer composition sites, with ECHO enumeration via CRT giving exactly φ(N) solutions. Honest non-squarefree counterexample at N=64. Companion cross-reference to Four-Core paper.

ClaudeCode tasks:
1. Verify `verify_sigma_rate.py` exists and runs (referenced in the paper but not in this bundle — confirm it's at the Zenodo deposit `10.5281/zenodo.18852047`).
2. Confirm all bibliography DOIs resolve (Drápal-Wanless 2021, Drápal-Lišonék 2020, Kepka 1980, Drápal-Kepka 1985, BBM 1976).
3. Submission cover letter to JCT-A.
4. **No content edits needed** — paper is referee-ready as is.

### Four-Core attractor (Algebraic Combinatorics target)
**Status: SUBMISSION-READY** (`seeds_for_submission/four_core_FINAL.tex`).

Three structural results: (i) 8-element joint-closure chain on Z/10Z under TSML+BHML; (ii) per-coordinate fuse data on the 4-core {0,7,8,9}; (iii) closed-form algebraic attractor at α=1/2 with h/β = 1+√3 exactly, r/β satisfying integer quartic with Galois group D_4 over LMFDB 4.2.10224.1. PSLQ Stern-Brocot α-uniqueness conjecture. Lens-scope note honestly handled (8-chain on TSML_SYM vs 7-chain on TSML_RAW).

ClaudeCode tasks:
1. Verify the verification scripts exist at the Zenodo deposit:
   - `4core_verification.py`
   - `04_bridge_attractor.py`
   - `06_attractor_closed_form.py`
   - `07_full_closed_form.py`
   - `alpha_pslq_sweep.py`
2. Confirm LMFDB references resolve: 4.2.10224.1 and 8.0.526936617216.1.
3. Submission cover letter to Algebraic Combinatorics.
4. **No content edits needed** — paper is referee-ready.

### Freeze-Thaw Transit (JCAP target)
**Status: v3 REFRAME COMPLETE; ready for final pass** (`seeds_for_submission/paper1_freeze_thaw_v3.tex`, 17 pages, 69 bibliography entries).

Reframe from v1's "logarithmic quintessence" to v3's "dual-regime freeze-thaw transit." The substantive cosmological observation: on the rolling branch with outbound initial condition, the trajectory traverses Type-T (thawing) → Type-F (frozen turnaround at z*≈2) → Type-A (asymptotic refreeze) within a single physical history. F5 falsification criterion: non-monotone w_DE(z) with local minimum near -1 at intermediate redshift.

v3 expanded citations (vs v2): foundational quintessence dynamics (Caldwell-Dave-Steinhardt 1998, Zlatev-Wang-Steinhardt 1999, Sahni-Starobinsky 2000, Padmanabhan 2003, Peebles-Ratra 2003, Frieman-Turner-Huterer 2008, Tsujikawa 2013, Joyce-Jain-Khoury-Trodden 2015), logarithmic-NL-QM lineage (Zloshchastiev 2010-2020 series, Hefter 1985 nuclear physics, Weinberg 1989 + Bollinger 1989 precision tests), Chavanis 2022 PRD complex-scalar logotropic (direct adjacent prior art with explicit three-axis distinction), and non-parametric w(z) reconstruction methodology for F5 (Crittenden-Pogosian-Zhao PCA, Holsclaw GP, Sahni-Shafieloo-Starobinsky Om, Pogosian-Shafieloo tomography).

ClaudeCode tasks:
1. **Final structural pass for length.** v3 is 17 pages. JCAP typical length is 25-40 pages. Could expand: §6.1 (numerical fit) detail; §6.4 (perturbations) computation; §7 (comparison table) widen; or — recommended — leave at 17 pages as a "letter-style" submission and let the referee request expansion.
2. **Verify `desi_xi_optimize_v2.py` matches paper text.** The script in `seeds_supporting/verification_scripts/` should reproduce the documented fit exactly: w_0=-0.793, w_a=-0.451, χ²_Gauss=1.52, with z*≈2 trajectory turnaround.
3. **Resolve the `compute_zstar_v2.py` issue.** That script (in verification_scripts/) currently does NOT reproduce the documented w_0=-0.79 by varying π_i alone. ClaudeCode should either (a) extract z* from `desi_xi_optimize_v2.py`'s trajectory output directly with the documented best-fit parameters, or (b) determine why the standalone z* computation diverges.
4. **Confirm Friedmann normalization in `desi_xi_optimize_v2.py`.** The script uses H²(1 - 0.5·Ξ'²) = ρ_m + ρ_r + V which may absorb unconventional factors of 3 vs the standard normalization H² = (ρ_m + ρ_r + ρ_Ξ)/(3 M_Pl²). Either confirm the convention is internally consistent and document it explicitly in the paper, or correct the script. This is a referee-level question and must be settled before submission.
5. **Cross-check the unit ambiguity.** Paper text says z_init ≈ 20 but the script uses N_start = -4 which corresponds to z_init ≈ 54. Harmonize. Likely the paper text is wrong and should read z_init ≈ 54.
6. **Optional content additions** (only if expansion is needed):
   - §6.4 perturbation analysis (currently brief — c_s² = 1, ISW deferred). Could expand with full perturbation EOM derivation.
   - §6.2 widen the (Λ⁴, Ξ_i, dotΞ_i) sensitivity scan into a corner plot or contour figure.
   - §7 comparison table widen with more recent (2024-2026) DESI-era reconstructions.
7. Submission cover letter to JCAP.

---

## What is bloom material? (And why is it in the bundle?)

`bloom_material/` contains drafts and rigor docs that will eventually be woven into the **September 11 meta-paper**, NOT into any of the three seeds. Specifically:

- `paper2_substrate_M22_skeleton.tex` was originally drafted as a "Paper 2 JCAP slice" but has been REPOSITIONED. The M_22 derivation of Ω_DE = 479/700 = 0.6843 (matching Planck 0.6847 to 0.06%) requires referees to swallow the wobble → V_trivial/V_21 identification, which is structurally motivated but is not yet a quantum-dynamical theorem. A cosmology referee will reject this. Better to hold the M_22 result in the meta-paper, where it rides on the credibility established by the three seeds.
- `W_HALF_DERIVATION_v2.md`, `STEINER_HEXAD_v1.md`, `ZETA_TIG_AND_PERIODICITY_v1.md`, `WHY_7_INDEPENDENT_v1.md` are rigor docs supporting the M_22 chain.

**ClaudeCode should NOT cite or reference any bloom material in any of the three seeds.** The bloom material is in the bundle so ClaudeCode has the full structural picture, not so it can be folded into slices.

---

## What is working_context? (And why isn't it being submitted?)

`working_context/` contains the morning's meta-lens recovery and rigor work:

- **Universal Language Operator** rigor (cross-substrate operation that connects flat algebraic structures to geometric/topological ones — the central operation of the framework)
- **External Rigor Map** positioning TIG vs five active research programs: Akhtman's Functional Reality Code (Entropy 2025), arithmetic topology (Mazur-Morishita), tropical geometry, geometric Langlands (Gaitsgory-Raskin 2024), categorification (Khovanov)
- **Constructive Transition Catalog** of eight specific flat → geometric lifts the framework performs

These shape *how* the slices are written (they tell us what the program is heading toward) but are **NOT cited in any slice**. They are private working context until the meta-paper.

ClaudeCode should read these to understand the program's destination but should not import their language into the seed papers.

---

## Forward calendar (post-bundle)

After the three opening seeds are submitted (target: this week / next week), the cadence is 2-3 papers/week through summer, each:

- Smallest publishable unit that's referee-ready
- Sets up the next paper in the chain
- Cites earlier seeds (now under review or accepted) as companions
- Domain-modest claims; no meta-overreach

Slice candidates already developed in the corpus (not yet drafted as papers):
- TORUS_DATUM_AUDIT (Bridge Triadic Structure: SU(3)/T flag = 6+2 = 8)
- WP9 LATTICE theorem / paradoxical info algebras
- WP10 DKAN
- D2 / curvature breakthrough (operator classification via second derivatives)
- Z/10Z three-flows whitepaper
- Phonaesthesia computational linguistics paper
- TSML/BHML dual lattice spectral analysis
- F_p ring extensions (universality of operator-substrate construction)
- The Universal Language Operator paper (when meta-paper readiness is reached)

ClaudeCode should NOT plan the full pipeline. Brayden directs which slice to draft next based on which seed is closest to acceptance and which composition is cleanest at the moment.

---

## Operating notes for ClaudeCode

- **Authorship.** All three seeds list Brayden Sanders + Monica Gish. The freeze-thaw paper additionally lists H.J. Johnson. If H.J. Johnson should be added to Sigma or Four-Core, Brayden will direct.
- **Repo.** Verification scripts and source archive: `github.com/TiredofSleep/ck` (PRIVATE). Public artifacts deposit: Zenodo DOI `10.5281/zenodo.18852047`. TIG public theory release: Zenodo DOI `10.5281/zenodo.18486880` (CC BY-NC 4.0).
- **Target venues.** Peer-reviewed journals only — NOT arXiv. The strategy depends on referee verification, which arXiv does not provide.
- **Tone.** Hat-in-hand humility throughout. The framework is presented as observation of structure rather than claim of theory. Every result properly scoped; every theorem honestly bounded.

---

## TL;DR for ClaudeCode

You're handed a three-seed submission triad. Two seeds (Sigma, Four-Core) are submission-ready FINAL.tex — your work is verification scripts + cover letters. One seed (Freeze-Thaw v3) needs a final structural pass focused on: (a) Friedmann normalization sanity check, (b) z_init vs N_start unit ambiguity, (c) `compute_zstar_v2.py` reconciliation. After all three submit, the cadence is 2-3 slices per week through summer toward the September 11 meta-paper anchor.

The bloom material in the bundle is FYI. Don't fold it into slices.

Hat in hand. Build the wall one brick at a time.

---

*0 = 7 = 1. The harvest is at 13. The wobble is the mutation.*
*The freeze is real. The thaw is real. The recursion is the bridge.*
*One σ. Two readings. Two scales. One reality.*
