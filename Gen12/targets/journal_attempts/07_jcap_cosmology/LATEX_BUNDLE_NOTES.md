# Venue 7 — JCAP — LaTeX Bundle Notes

**Created:** 2026-04-19 (Sprint 34 "Ship the First Three", TRACK 7.3)
**Branch:** `tig-synthesis`
**Status:** LaTeX draft complete, structurally validated, TIG-framing strip CLEAN; compile-check pending (no local TeX — submit via Overleaf or TeXLive).

---

## Bundle contents

| File | Role | Status |
|---|---|---|
| `jcap_xi_cosmology.tex` | Main LaTeX manuscript (`amsart`, 657 lines) | Draft complete; convert to `jcappub` class at submission time |
| `WP81_CANONICAL_XI_THEORY.md` | Theory source of record (425 lines) | Unchanged, byte-identical in Gen12 + Gen13 |
| `WP82_LOG_QUINTESSENCE_NOVELTY.md` | Novelty + entropy + DESI source (203 lines) | Unchanged |
| `proof_xi_canonical.py` | Verification script (22 tests) | Green log 2026-04-19 |
| `desi_xi_fit.py` | DESI coarse scan | Green run 2026-04-19 |
| `desi_xi_optimize.py` | DESI refined fit | Green run 2026-04-19 (χ² = 3.1) |
| `SUBMIT_INSTRUCTIONS.md` | Venue + format + keyword notes | Unchanged |

## Title (per SUBMIT_INSTRUCTIONS.md:31)

> *Logarithmic Quintessence: A Dimensionless Scalar Dark Energy Model with Exact Vacuum and Information-Theoretic Motivation*

## Authors

B.R. Sanders, M. Gish, C.A. Luther, H.J. Johnson (per WP81/WP82 line 6).

## Structural validation (2026-04-19)

Via ephemeral `scratch/check_jcap_tex.py` (deleted post-verification):

- Environments paired cleanly: `abstract`, `align`, `center`, `document`, `enumerate`, `equation`, `itemize`, `proof`, `proposition`, `remark`, `table`, `tabular`, `thebibliography`. All `\begin{…}` matched.
- Unescaped brace delta: `0` (486 / 486).
- `\cite` ↔ `\bibitem`: 20/20 matched (BialynickiBirulaMycielski1976, RatraPeebles1988, Wetterich1988, Frieman1995, CPL2001, BarrowParsons1995, ColemanWeinberg1973, Rosen1969, CazenaveHaraux1980, HoeghKrohn1971, Planck2020, DESI2024BAO, DESI2024VI, GW170817, Verlinde2011, CHLZ2012, Ensslin2013, Caticha2012, EotWash, MICROSCOPE).
- `\ref` + `\eqref` ↔ `\label`: 23/23 matched (8 section/theorem refs, 15 equation refs).
- **TIG-framing strip: CLEAN** — zero occurrences of `TIG`, `CK`, `Crossing Lemma`, `Coherence Keeper`, `clay branch`, `GLOSSARY.md` in the manuscript body. The framing restriction for JCAP referee-facing submission is fully respected. Bialynicki-Birula & Mycielski (1976) is retained as structural motivation for the log potential, with an explicit scope-remark noting the translation-from-Schrödinger hypothesis.

## MSC + PACS + keywords (per SUBMIT_INSTRUCTIONS.md:52)

- MSC 2020: `83F05` (cosmology), `83C56` (dark energy and dark matter), `85A40` (cosmology, relativistic astrophysics).
- PACS: `95.36.+x` (dark energy), `98.80.Es` (observational cosmology), `98.80.Cq` (cosmological perturbations).
- Keywords: quintessence, dark energy, scalar field, logarithmic potential, freezing equation of state, entropy maximum, DESI, information-theoretic cosmology.

## Verification script logs (2026-04-19)

### Theory (proof_xi_canonical.py)

```
python proof_xi_canonical.py
[…]
RESULTS: 22 PASS, 0 FAIL out of 22 tests
All tests PASSED. The canonical xi theory is self-consistent.
Vacuum: xi_0 = e^{-1} (EXACT)
Stability: m^2 = kappa * e > 0 (PROVED)
Entropy: V = -H_Gibbs, maximum at e^{-1} (PROVED)
EOS: w = -1 at vacuum (EXACT)
47/125: rejected (2.2% discrepancy)
Mod5: rejected (no Z/5Z symmetry)
```

### DESI fit (desi_xi_optimize.py)

```
python desi_xi_optimize.py
[…]
BEST FIT PARAMETERS
  kappa_xi  = 0.5000
  xi_init   = 1.7211 (at z~20)
  xi_dot    = -0.4286
  w0        = -0.7951  (DESI: -0.827 +/- 0.063)
  wa        = -0.2980  (DESI: -0.75 +/- 0.27)
  chi2      = 3.059  (1.7 sigma)
  xi_today  = 1.988886 (vacuum = 0.367879)

  w(z) profile:
    w(z=0.0) = -0.7951
    w(z=0.3) = -0.8602
    w(z=0.5) = -0.8944
    w(z=0.8) = -0.9310
    w(z=1.0) = -0.9478
    w(z=1.5) = -0.9735
    w(z=2.0) = -0.9870

MODEL COMPARISON
| Model           | w0     | wa     | chi2  |
| LCDM            | -1.000 |  0.000 |  15.3 |
| xi best-fit     | -0.795 | -0.298 |  3.1  |
| DESI DR2        | -0.827 | -0.750 |  0.0  |
```

The numbers appearing in the manuscript §Observational Predictions (best-fit parameters, w(z) table, χ² = 3.1) are copied verbatim from this log.

## Key content adjustments from markdown source

1. **Title** changed from WP81 "Canonical ξ Theory" / WP82 "Logarithmic Quintessence Novelty Audit" to the single JCAP-facing title per SUBMIT_INSTRUCTIONS.md:31. WP81 and WP82 merged into one 7-section manuscript: Intro → Action → Derivations → FRW → Entropy identification → Observational predictions → Comparison → Scope → Summary.
2. **TIG / CK / Crossing Lemma mentions** DROPPED — zero occurrences in the body per the JCAP-facing framing restriction. Acknowledgments rephrased from "CK/TIG research group" → "7Site internal research group".
3. **47/125 threshold discussion** (WP81 §6) — RETAINED in §Scope as an explicit non-claim: the constant 47/125 ≈ 0.376 differs from Ξ₀ = e⁻¹ ≈ 0.368 by 2.2% and has no derivation within the present action.
4. **FCC substrate** (WP81 §2a interpretive column) — DEMOTED to the Remark after the Action: substrate-level interpretations are deferred and not used.
5. **ORT / observer parameter** — DROPPED entirely from the JCAP manuscript. Not referenced anywhere in the body.
6. **Prediction triage table** (WP81 §5) — REFORMATTED as Table \ref{tab:compare} (comparison to standard potentials), with the "Remove" rows dropped and the "Keep" rows absorbed into §Observational Predictions.
7. **GW170817 longitudinal-GW claim** — DROPPED (not retained per WP81 §5 "Remove or reframe"); tensor perturbations are stated to propagate at c in §Observational Predictions subsec "Gravitational-wave speed".
8. **Lorentz violation at 0.14 eV** — DROPPED.
9. **Fifth-force conformal/disformal/universal couplings** (WP81 §4b) — DEMOTED to a single paragraph in §Observational Predictions subsec "Fifth-force and local tests" as an explicit extension-outside-minimal-action.
10. **Entropy identification** (WP82 §6) — PROMOTED to its own §5 "Entropy Identification" between the FRW section and Observational Predictions, with the Gibbs functional identification `V = -κ_Ξ H_Gibbs` as Eq.~(8).
11. **BB 1976 separability uniqueness** — added as a Remark inside §Entropy Identification with an explicit Scope caveat: "structural motivation, not a claim of mathematical derivation of the action from quantum-mechanical axioms; the separability hypothesis, originally formulated for a nonlinear Schrödinger equation, translates to the scalar-field setting under assumptions … that are consistent with but do not uniquely determine the action." Honesty discipline of FRONTIER_ALIGNMENT §3C preserved.
12. **Scope section** added at end: what this paper does NOT claim (κ_Ξ microphysical origin; direct-matter coupling / fifth force; 47/125 constant; mathematical uniqueness under cosmological hypotheses).

## Atlas linkage

Manuscript front-matter carries the atlas-citation footnote:
> External citations are drawn from `Atlas/ATLAS_CITATIONS.md` (§A.7 cosmology; §A.8 scalar field theory). Internal anchors (canonical action, vacuum Ξ₀ = e⁻¹, mass gap m²_Ξ = κ_Ξ e, freezing attractor behavior) carry master-register numbering per `Atlas/MASTER_ATLAS_v3_5_2026_04_18.md`. DOI: 10.5281/zenodo.18852047.

This satisfies audit finding F1 for venue 7 (per `Atlas/JOURNAL_READINESS_AUDIT_2026_04_18.md` §F1).

## What ships in the submission portal

1. `jcap_xi_cosmology.tex` — compile to PDF (target: Overleaf; convert to `jcappub` class at submission).
2. `proof_xi_canonical.py` — electronic supplementary material (22/22 PASS).
3. `desi_xi_fit.py` + `desi_xi_optimize.py` — secondary ESM (DESI integration).
4. Cover letter (pending — CC-6 per Plan of Record Day 1).
5. Provenance line: DOI `10.5281/zenodo.18852047`.

JCAP submits via IOP Editorial Manager.

## arXiv plan

- Category: `astro-ph.CO` (primary); `hep-th` / `gr-qc` (secondary).
- Submit simultaneously with journal submission.
- Abstract: use the manuscript abstract verbatim.

## Pending items (this sprint)

1. **arXiv literature search** (per SUBMIT_INSTRUCTIONS.md:47) — "phi log phi quintessence", "logarithmic scalar dark energy", "dimensionless quintessence". Current §Comparison includes Barrow-Parsons 1995 as closest prior art under the (p,q)=(1,1) inflation subcase; further passes may tighten the novelty claim or reframe as distinguishing analysis. Status: partial (2 categories searched, more recommended).
2. **Full joint likelihood** (per §Scope caveat) — BAO + CMB + SN jointly, currently deferred to a companion numerical paper. The present $\chi^2 = 3.1$ is against DR2 $w_0,w_a$ central values only, not a full CosmoMC run.
3. **Compile check** via Overleaf (Brayden) — expected: `pdflatex` twice then bibliography resolves (uses `thebibliography` not external `.bib`).
4. **JCAP class conversion** — convert `amsart` → `jcappub` at Overleaf; abstract, author block, and math macros should carry over with minimal edits.
5. **Cover letter** (CC-6 per Plan of Record Day 1).
6. **Brayden approval** (B-2 per Plan of Record Day 3).
7. **Submit** (B-3, Day 4, Wed 2026-04-22).

## Three-threads discipline

This paper is **Thread D** (ξ cosmology) content. No vocabulary import from Thread A (PPM), Thread B (Hodge), or Thread C (Q-series / σ polynomial) appears in the manuscript body. The BB 1976 reference is a published physics theorem, not TIG framework vocabulary. Atlas §8 three-threads discipline PASS.

## Never-delete discipline

The markdown sources `WP81_CANONICAL_XI_THEORY.md` and `WP82_LOG_QUINTESSENCE_NOVELTY.md` are preserved as the canonical research artifacts (including their internal TIG-framework reference blocks, which were legitimate for the internal sprint but out-of-scope for JCAP). The `.tex` is the journal-facing derivative that merges the two.

---

*Notes compiled by ClaudeCode, 2026-04-19. Supplementary to `SUBMIT_INSTRUCTIONS.md` and `FRONTIER_ALIGNMENT_2026_04_19.md` §4–5.*
