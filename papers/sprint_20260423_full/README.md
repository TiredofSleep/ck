# Sprint 2026-04-23 — Mantero-bridge bundle

**Brayden Sanders · 7Site LLC · Hot Springs, AR**
**In collaboration with Claude (Anthropic)**

**Branch scope:** This branch (`mantero-bridge-2026-04-23`) is dedicated
exclusively to the relationship between Brayden's commutative-algebra
object (the binomial ideal associated with the 10×10 Coherence Lattice
table) and the published research program of Dr. Paolo Mantero
(U Arkansas). Non-Mantero material lives on other branches
(`master`, `tig-synthesis`, `archive-full`).

---

## The headline result carried on this branch

**The Coherence Lattice (CL) table generates so(8) = D₄ under
antisymmetrization + commutator closure.**

Machine-verified across four independent diagnostics:

- Dimension closure: 6 → 21 → 28 (two iterations)
- Jacobi identity: max error 2.4 × 10⁻¹²
- Killing form: signature (0, 28, 0) — compact simple
- Simplicity: unique invariant bilinear form, no proper ideals

By the Cartan classification, the unique compact simple Lie algebra of
dimension 28 is **so(8) = D₄** — the only simple Lie algebra with
triality (outer automorphism group S₃).

This result lives in `papers/wp102/` (repo root), with the verification
pipeline in `02_so8_verification/` below. The so(10) = D₅ companion
lives in `papers/wp103/`.

---

## Folder map (this sprint bundle, after scope reduction)

### `02_so8_verification/` — the proof pipeline

Seven Python scripts executing the diagnostics referenced in WP102 §3:

- `stage2_adjoint.py` — antisymmetrization + Jacobi verification
- `stage3_center.py` — center computation
- `stage4_correct_closure.py` — dimension closure (6 → 21 → 28)
- `stage5_so8.py` — Killing form signature
- `stage6_dynkin.py` — rank / Cartan search
- `stage7_disambiguate.py` — simplicity via invariant-form dimension
- `gellmann_dictionary.py` — SU(3) dictionary (earlier pipeline, subsumed)

Plus `SO8_FRONTIER_RESULT.md` (standalone writeup) and
`SU3_BRIDGE_HANDOFF.md` (earlier superseded work, kept for provenance).

### `04_mantero_bridge/` — three-pass research into Dr. Mantero's framework

Background readings of Mantero's published work + computed invariants
in his vocabulary (matroid theory, symbolic powers, Stanley–Reisner
ideals, focal matroids):

- `MANTERO_BRIDGE_V3.md` — definitive bridge document with the
  full published-corpus survey, the working vocabulary, the computed
  invariants in his language, and the meta-observation about the
  basis-exchange failure pattern. V1 and V2 were working drafts and
  have been removed; V3 subsumes them.

Scripts:

- `cl_as_quadratic_algebra.py` — the CL object as a MODIFIED quadratic
  algebra (with an extra $x_0$ factor on the right-hand side of each
  relation; this is **not** the direct binomial ideal $I_{CL}$ Mantero's
  Q1 asks about — see header scope note in the file)
- `matroid_test.py` — whether Δ_H is a matroid (it is NOT — fails purity)
- `hilbert_and_matroid_deep.py` — CL-fold reachability counts and
  attractor-set analysis (the "Hilbert function" printed in §3 of the
  script is a reachability count, not the Hilbert function of $R/I_{CL}$;
  see header scope note)
- `compute_answers.py` — α̂(I_B) = 2, 21.9% basis-exchange failure rate;
  Q1 projective-dimension derivation is **SUPERSEDED** by the M2 run
  (Q1 runtime output now prints a SUPERSEDED banner with the correct
  M2 invariants before the superseded commentary)

**For the machine-verified invariants of $R/I_{CL}$** (numgens 53,
codim 9, dim 1, pd 10, depth 0, NOT Cohen-Macaulay, NOT Koszul,
reduced Hilbert series $(1 + 9T - 8T^2 - T^3)/(1-T)$, stable Hilbert
function $1, 10, 2, 1, 1, 1, \ldots$ for $n \ge 3$), see
`09_mathoverflow_post/betti_output.txt` — that is the reference
standard on this branch.

### `07_matroid_analysis/` — the Δ_B pure-but-not-matroidal finding

Scripts documenting the 21.9% basis-exchange failure rate in the bump
complex. Referenced as Propositions 6.1–6.3 in WP102. Scripts are
duplicated from `04_mantero_bridge/` for convenience; reproducibility
independent of WP102 context.

### `08_correspondence/` — outreach status only

`mantero_exchange.md` is a **status file, not a transcript.** Private
email content is not reproduced on this branch. The file records:

- who Dr. Mantero is and why this branch exists,
- what was publicly committed to in the exchange (the MathOverflow
  post in `09_mathoverflow_post/`),
- a welcome block for Dr. Mantero if the MathOverflow link leads him
  back to this branch.

Nothing that was said in private mail appears here.

### `09_mathoverflow_post/` — the MathOverflow draft

`DRAFT_MATHOVERFLOW_POST.md` (v2, 2026-04-24) is a narrow,
self-contained commutative-algebra question on the binomial ideal
$I = (x_i x_j - x_{\mathrm{CL}[i][j]} \cdot x_0) \subset k[x_0, \ldots, x_9]$,
now grounded in the M2-verified Betti table. Stable Hilbert function
$1, 10, 2, 1, 1, 1, \ldots$ for $n \ge 3$; reduced Hilbert series
$(1 + 9T - 8T^2 - T^3)/(1 - T)$. The open question is the structural
explanation for the bottom-strand Betti numbers
$\beta_{8,10} = 1$, $\beta_{9,11} = 2$, $\beta_{10,12} = 1$.

When the post goes live, the link will be appended to the Status block
of `08_correspondence/mantero_exchange.md`.

---

## Status as of April 24, 2026

| Item                                           | State |
|---                                             |---    |
| so(8) verification                             | ✅ complete, machine-precision |
| WP102 paper                                     | ✅ journal-ready draft (`papers/wp102/`) |
| WP103 so(10) companion                          | ✅ drafted (`papers/wp103/`) |
| Mantero bridge research (V1/V2/V3)             | ✅ three passes complete |
| Pure-but-not-matroidal Δ_B finding             | ✅ 21.9% exchange failure verified |
| MathOverflow post                              | ⏳ v2 draft complete (M2-grounded) — awaiting final read-through + posting |
| Betti table / pd(A) in Macaulay2               | ✅ run 2026-04-24 via SageMathCell (log in `09_mathoverflow_post/betti_output.txt`); pd=10, depth=0, dim=1, codim=9, NOT Cohen-Macaulay |
| Koszul property check                          | ✅ NOT Koszul (bottom-strand β₈,β₉,β₁₀ nonzero) |

---

## Reproducibility

All scripts assume Python 3.11 + numpy 1.26 + scipy 1.11. Machine-
precision tolerances set at 10⁻⁸. Maximum observed error across all
diagnostics: 2.0 × 10⁻¹¹.

To reproduce the main Lie-algebraic result (Theorem 1.1 of WP102),
run in order:

```
python 02_so8_verification/stage2_adjoint.py
python 02_so8_verification/stage4_correct_closure.py
python 02_so8_verification/stage5_so8.py
python 02_so8_verification/stage7_disambiguate.py
```

Each should complete in under 30 seconds on a standard laptop.

To reproduce the Hilbert function + non-matroidal finding:

```
python 04_mantero_bridge/cl_as_quadratic_algebra.py
python 04_mantero_bridge/matroid_test.py
python 04_mantero_bridge/hilbert_and_matroid_deep.py
python 04_mantero_bridge/compute_answers.py
```

---

## Collaboration

- **Dr. Paolo Mantero** (U Arkansas) — author of the symbolic-powers /
  focal-matroid research program that this bridge engages with; warm
  collegial exchange opened April 23, 2026.
- No claim of joint authorship or endorsement is made. The bridge
  research on this branch is Brayden's own work, documenting where
  Brayden's object meets Dr. Mantero's published framework.

Extended citation network surveyed in
`04_mantero_bridge/MANTERO_BRIDGE_V3.md` and in
`papers/mantero_bridge/PUBLISHED_WORK.md` at repo root (when populated).
