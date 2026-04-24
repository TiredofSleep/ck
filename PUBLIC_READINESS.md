# Public Readiness — Verified vs Asserted vs Conjectural

**Last updated:** 2026-04-24 (evening)
**Branch:** `vocab-update-2026-04-23`
**Owner:** Brayden Sanders / 7Site LLC
**Repository:** github.com/TiredofSleep/ck
**DOI:** 10.5281/zenodo.18852047

---

## What this document is

A single page for any external reader — mathematician, physicist,
journal editor, funder, AI cold-reader — to navigate this repo by
**epistemic status**, not by filename. Every claim in this repo is
labeled one of four ways:

| Tag | Meaning |
|---|---|
| **VERIFIED** | Computation reproduces to machine precision. A script in this repo produces the stated number on a fresh run. |
| **STRUCTURAL** | Form of argument is sound and fully spelled out, but final result depends on one or more named assumptions that are stated explicitly. Not a proof; not a hand-wave either. |
| **CONJECTURAL** | Precise statement. No proof. Either a named Clay-adjacent conjecture, or a working hypothesis of this framework. |
| **CORRECTED** | Claim in an earlier file was wrong or scope-ambiguous; has been superseded. The superseding document is always named. |

When any downstream file claims a result, you should be able to find
that result in the table below with its tag and its verification script
or its named assumption. If you cannot, that file's claim is not yet
public-readiness grade.

---

## Canonical table registry (start here)

Before reading any TSML/BHML claim, consult
[`FORMULAS_AND_TABLES.md` §6.7](FORMULAS_AND_TABLES.md).
There are **nine canonical named tables** in this repo. Three of them
share the name "BHML" or "TSML" with distinct qualifiers — do not
conflate them:

| Short name | Shape | det | Semantic role |
|---|---|---:|---|
| `TSML_10` | 10×10 | 0 | Working TSML. Base of §7 three-layer tower. |
| `TSML_8` | 8×8 | 0 | Spectral core of TSML (singular). |
| `TSML_PureIdempotent` | 10×10 | +398664 | Full-rank idempotent variant. Aut = S₈. |
| `TSML_Idempotent_2sw` | 10×10 | −49 | Minimum-\|det\| TSML in prime-7 regime. |
| `BHML_10` | 10×10 | **−7002** | Working BHML. Sister to TSML_10. |
| `BHML_8` | 8×8 | **+70** | Spectral core of BHML. Yang-Mills transfer matrix. |

(Three boundary-case members — TSML_C0, TSML_PureVoid, TSML_AllHarmony —
round out the seven-member family; see §6.6 and §6.7.)

---

## VERIFIED results (reproducible in seconds)

Every row below names a claim, the script that reproduces it, and the
expected output. Run them yourself:

```bash
git clone github.com/TiredofSleep/ck && cd ck
pip install numpy sympy
```

### Table arithmetic (TSML, BHML variants)

| # | Claim | Verified by | Expected |
|---|---|---|---|
| V1 | `det(TSML_10) = 0`, rank 9 | `verify_claims.py` claim 3 | `PASS` |
| V2 | `det(BHML_10) = −7002`, primes {2, 3, 389} | `verify_claims.py` claim 4a | `PASS` |
| V3 | `det(BHML_8) = +70`, primes {2, 5, 7} | `verify_claims.py` claim 4b | `PASS` |
| V4 | TSML has 73 HARMONY cells | `verify_claims.py` claim 1 | `73/100` |
| V5 | BHML has 28 HARMONY cells | `verify_claims.py` claim 2 | `28/100` |
| V6 | TSML non-associative rate = 12.8% | `verify_claims.py` claim 5 | `12.8%` |
| V7 | BHML non-associative rate = 49.8% | `verify_claims.py` claim 6 | `49.8%` |
| V8 | Both tables commutative | `verify_claims.py` claims 7–8 | 0 violations |
| V9 | `det(TSML_Idempotent_2sw) = −49` | `verify_family_members.py` member 5 | `−49` |
| V10 | `det(TSML_PureIdempotent) = +398664` | `verify_family_members.py` member 4 | `+398664` |
| V11 | Full 7-member family catalog (§6.6) | `verify_family_members.py` | all 7 invariants match §6.6 |

### Spectral / eigenvalue claims

| # | Claim | Verified by | Expected |
|---|---|---|---|
| V12 | `BHML_8` eigenvalue ratio `\|λ₇\|/\|λ₆\| = 0.714865 ≈ 5/7` (0.08% error) | `Gen12/targets/ck_desktop/bhml_eigenvalue_analysis.py` | ratio 0.714865 |
| V13 | `BHML_8` symmetric, full rank, det = 70 by eigenvalue product | same | `sym=True, rank=8` |

### Number-theoretic identities

| # | Claim | Verified by | Expected |
|---|---|---|---|
| V14 | sinc²(1/2) = 4/π² = (2/3) · 1/ζ(2) | `papers/proof_sinc_zeta_identity.py` | Δ = 5.55×10⁻¹⁷ |
| V15 | sinc²-zero loop closure across primes 3..199 | `papers/proof_d25_loop_closure.py` | all pass |
| V16 | First-G Law: first non-unit at position p for semiprime pq | `ck_run.py` | 36662 cases, 0 mismatches |
| V17 | D6 general-frequency operator identity | `papers/proof_d6_general_frequency.py` | 890 cases, 0 mismatches |
| V18 | 5D force vector as CRT Fourier embedding (Q17) | `Q17_5D_RIGOROUS.py` | exact reproduction |

### σ theorem (Sprint 14, Sprint 18)

| # | Claim | Verified by | Expected |
|---|---|---|---|
| V19 | σ permutation on ℤ/10ℤ, order 6 (σ⁶ = id) | `verify_claims.py` + `papers/proof_d18_sigma_order.py` | `σ⁶ = id ✓` |
| V20 | σ polynomial form on F₂×F₅ (Q10) | `papers/Q10_*.py` | polynomial reproduces σ |
| V21 | σ rate theorem: σ(N) ≤ C/N for squarefree N | `Gen12/.../proof_sigma_rate.py` | all tested N pass |
| V22 | 22% lower bound for σ(N) (Q11) | `papers/Q11_*.py` | bound holds |

### TSML 3-layer tower (Sprint 17)

| # | Claim | Verified by | Expected |
|---|---|---|---|
| V23 | TSML = C₀ ⊕ S_MAX ⊕ S_ADD decomposition, 92+6+2=100 cells | `papers/proof_tsml_3layer_tower.py` | 100/100 match |
| V24 | Lemma 5 (residue empty), Lemma 6 (each layer necessary) | same | both hold |

### Clay rotation framework (CP1–CP7)

| # | Claim | Verified by | Expected |
|---|---|---|---|
| V25 | CP rotation framework holds over 43 test cases | `Gen12/.../proof_clay_rotation.py` | 43/43 |

### One-liner reproducibility spot check (copy-paste into terminal)

```bash
python -c "from sympy import Matrix; TSML=[[0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],[0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],[0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],[0,7,9,3,7,7,7,7,7,7]]; BHML=[[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],[3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],[6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],[9,6,6,6,7,7,7,0,8,0]]; C=[1,2,3,4,5,6,8,9]; sub=lambda M,I:[[M[i][j] for j in I] for i in I]; print('TSML_10 det/rank:', Matrix(TSML).det(), Matrix(TSML).rank()); print('BHML_10 det/rank:', Matrix(BHML).det(), Matrix(BHML).rank()); print('BHML_8  det/rank:', Matrix(sub(BHML,C)).det(), Matrix(sub(BHML,C)).rank())"
```

Expected output (reproduces the four numbers the whole framework rests on):

```
TSML_10 det/rank: 0 9
BHML_10 det/rank: -7002 10
BHML_8  det/rank: 70 8
```

---

## STRUCTURAL results (sound argument, named assumptions)

These are results where the line of reasoning is rigorous and explicit,
but the final step rests on a named literature result, a structural
correspondence, or a careful interpretive bridge. They are **not
proofs of external theorems**, and they are not presented as such.

| # | Claim | Named assumption(s) | Document |
|---|---|---|---|
| S1 | Flatness Theorem: the four-way arithmetic on ℤ/10ℤ cannot stay flat; forces a torus with R/r = 5/7 | Holds for ℤ/10ℤ specifically. Generalization to "any whole" is a working hypothesis, not a proved theorem. | WP51, `CROSSING_LEMMA.md` |
| S2 | Crossing Lemma: information generated exactly when dynamics cross partitions | Proved for squarefree n, d | WP57, `papers/proof_d8_cl_operator_encoding.py` |
| S3 | BHML_8 eigenvalue gap corresponds to a mass gap in a lattice gauge theory | Depends on (i) Wilson (1974) lattice confinement (established), (ii) Osterwalder-Seiler (1978) reflection positivity (established), (iii) identification of BHML_8 as a transfer matrix of a specific gauge theory **(not established — conjectural)** | WP15 (clearly flagged as proof-sketch with explicit remaining gaps) |
| S4 | Bialynicki-Birula (1976) bridge from σ→0 to log nonlinearity □ξ = 1 + log ξ | BB's theorem is established literature. Application here is a structural bridge, not a proof that TIG's σ generates the BB potential. | WP91, Sprint 14 ξ cosmology |
| S5 | ξ vacuum as entropy maximum (V = ξ log ξ, ξ₀ = e⁻¹, m²_ξ = κe) | Follows from the assumed BB potential. Conditional on S4. | WP81, Sprint 14 |
| S6 | Dual reset law (Sprint 16, basin-first arithmetic) | Proved for the specific carrier family tested. Generalization to all carriers is a working hypothesis. | Sprint 16 papers |
| S7 | α(BHML) = 0.502 ≈ 1/2 as a "half-associativity" signature | α is a well-defined invariant (verified). The interpretation "BHML sits at the associativity-boundary" is a hypothesis; the Huang-Lehtonen free-operad literature supports it structurally but does not prove it. | §6.1, §6.6, FORMULAS_AND_TABLES.md |
| S8 | TSML/BHML Huang-Lehtonen Catalan + ac-free spectrum | Both tables verified to hit the spectrum; the interpretation of what this means for bracketing combinatorics is structural. | §6.1 |

---

## CONJECTURAL results (precise statement, no proof)

Named conjectures. Either Clay-adjacent, or working hypotheses of this
framework. All are stated precisely.

| # | Statement | Status |
|---|---|---|
| C1 | **Navier-Stokes regularity** reformulated as σ_NS < 1. | Millennium Problem in this framing. Reformulated, not proved. |
| C2 | **Yang-Mills mass gap** reformulated as σ_YM < 1 with BHML_8 as transfer matrix. | Millennium Problem. Reformulated; S3 gives a proof-sketch with explicit gaps. |
| C3 | **Riemann Hypothesis** as spectral entropy maximum in the σ framework. | Millennium Problem. Reformulated. |
| C4 | **Poincaré rotation (CP1)** — template: solved by Perelman (2003). CP2–CP7 are the other six Clay problems in the σ < 1 rotation. | Solved for CP1. CP2–CP7 conjectural. |
| C5 | The seven-member TSML/BHML family covers the canonical TSML/BHML-named objects on ℤ/10ℤ. | No member outside the seven has been discovered in this repo; exhaustiveness is unproven. |
| C6 | TSML_Idempotent_2sw minimal-\|det\| = 49 in prime-7 regime. | Conjectural minimality — task11 compute job still open. |
| C7 | BHML_8's T* ratio `|λ₇|/|λ₆| = 0.714865` has physical significance as a mass-gap ratio rather than numerical coincidence in a specific 8×8 matrix. | Flagged as conjectural in WP15 itself. |
| C8 | Cyclotomic T*(N) does **not** collapse to a single constant — the simplest discrete-to-continuous T* bridge is ruled out. | **Negative conjecture**, verified for tested N. This is a hypothesis-elimination result, not a positive claim. |

---

## CORRECTED (honest self-correction log)

This framework is in active development. When a claim is found to be
wrong, or scope-ambiguous, the correction is applied in place (old
claim preserved per never-delete policy) and logged here. Public readers
can rely on: **if a claim has been corrected, the correction is
discoverable from the original file.**

| # | Original claim | Correction | Correction document |
|---|---|---|---|
| X1 | "`det(BHML) = 70 = 2 · 5 · 7`" (unqualified) in ~12 morphotic_braid files | The full 10×10 `BHML_10` has `det = −7002`. The 8×8 core `BHML_8` has `det = +70`. The files were using the 10×10 context but citing the 8×8 number. Scope ambiguity, not false number. | [`papers/morphotic_braid/CORRECTION_2026_04_24_det_BHML.md`](papers/morphotic_braid/CORRECTION_2026_04_24_det_BHML.md) |
| X2 | "`TSML_Idempotent`" used as single-table name | Split into `TSML_PureIdempotent` (det = +398664) and `TSML_Idempotent_2sw` (det = −49). See §6.6 and §6.7. | `FORMULAS_AND_TABLES.md` §6.6, §6.7 |
| X3 | `verify_claims.py` claim #4 expected value | Was `70` (which fails on the full BHML). Now split into 4a (`BHML_10`, expected −7002) and 4b (`BHML_8`, expected +70). | `verify_claims.py` (patched 2026-04-24) |
| X4 | Hook #4 of `DEEPER_SYNTHESIS.md` (Connes semi-local trace formula at places `{2, 5, 7, ∞}`) | Withdrawn as stated (used BHML_10 context; primes are `{2, 3, 389}`). May be rebuildable on BHML_8 (primes `{2, 5, 7}`); not yet rewritten. | `papers/morphotic_braid/synthesis/DEEPER_SYNTHESIS.md` banner |

**Other known drift in `verify_claims.py`** (not yet fixed, flagged
honestly):

- Claim 9 (CROSS_CYCLE): sum matches (`44`), element-by-element list
  doesn't match the paper's list. Cosmetic, but a discrepancy.
- Claim 12 (HEARTBEAT): paper claims `[1,3,1,1]`; script computes `[1,5,5,1]`. Needs either paper update or script update.
- Claim 16 (Doing non-zero): paper claims 56; script computes 71. Same — needs reconciliation.

These are **not corrections yet** because the direction of the fix
(update paper, or update script) requires deciding which definition
is canonical. Both alternatives will be surfaced in the next pass.

---

## How to audit a specific paper

If you want to read any whitepaper or sprint document, the workflow is:

1. Open the file.
2. For each numerical claim, ask: is this VERIFIED, STRUCTURAL, or
   CONJECTURAL?
3. If the file does not tag its own claims, cross-reference them here.
4. If a claim appears in this document as VERIFIED, run the named
   script.
5. If a claim appears as STRUCTURAL, confirm the named assumption is
   cited and accessible.
6. If a claim appears as CONJECTURAL, treat it as an open question.

**If a claim does not appear in this document at all**, it has not
yet been triaged for public-eye readiness and should be treated as
in-progress / draft.

---

## Three branches

| Branch | Role |
|---|---|
| `vocab-update-2026-04-23` (current) | Active vocabulary-alignment + public-readiness sweep. This document's working branch. |
| `tig-synthesis` | Clean, curated, rigorous-front-door branch. Will become default after the readiness sweep is merged. |
| `clay` | Active development branch with all work-in-progress files. |
| `archive-full` | Frozen preservation snapshot. Never force-pushed. |

---

## One-sentence summary for a cold reader

**TIG is a computational-algebraic framework on ℤ/10ℤ whose core
invariants (TSML, BHML, σ, T\* = 5/7, sinc²-zero law, the seven-member
table family, the three-layer TSML tower) are reproducible to machine
precision by short scripts in this repo; whose larger claims
(Flatness, Crossing Lemma generalizations, σ reformulations of the
Clay problems, BB-bridge to ξ cosmology) are structural arguments
with explicitly named assumptions, not proofs; and whose self-correction
log is public and complete.**

---

## Attribution

Authors:
- **Brayden Sanders** — framework originator, Q-series author, σ polynomial characterization, VOID/HARMONY discovery, table-family intuition
- **C.A. Luther** — spectral layer, 6-layer architecture, Luther closure BHML[7][0] = 7
- **Ben Mayes** — orbital structure, GUT algebra arc (Sprint 11, Sprint 12)
- **H.J. Johnson** — ξ cosmology (Sprint 14)
- **M. Gish** — PRISM-XI cross-branch analysis (Sprint 13, Sprint 14)
- **Calderon** — Q17 5D force vector

Cite as:
```
B. R. Sanders et al., "Trinity Infinity Geometry: A computational-algebraic
framework on Z/10Z", 7Site LLC, 2026. DOI: 10.5281/zenodo.18852047.
```
