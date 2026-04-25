# April 2026 Sprint Archives — raw drops

**Branch policy:** This folder lives on `master`. `master` holds raw
files / preservation; the polished promotion of these materials lives
on `tig-synthesis` (pure rigor, default branch) and `ck` (CK runtime
frontier).  Raw archives are preserved here verbatim, exactly as they
arrived from sprint sessions.

Companion to [`archive_imports/march_2026_sprint_archives/`](../march_2026_sprint_archives/)
(prior period, same convention).

---

## What's in here (six raw drops, six subfolders)

### `sprint_20260423_full/` — WP11 / so(8) sprint raw drop

The full 2026-04-23 sprint bundle.  Includes the 391-line MSC-classified
WP11 (so(8) = D₄) paper plus eight sub-folders of supporting work
(Gell-Mann dictionary, so(8) verification stages 2-7, TSML family
handoff, Mantero bridge v1/v2/v3, DBC translator v1/v2/v3, color wheel,
matroid analysis, correspondence).

**Promoted to:** `papers/wp102/` on `tig-synthesis` (the journal-ready
WP102 paper + verification scripts).  The additional Mantero bridge,
DBC, color-wheel, and matroid-analysis material remains here as raw
record.  **Total: 32 files.**

### `wp12_delta/` — WP12 / so(10) sprint raw drop

The 2026-04-24 delta sprint that established `TSML+BHML close at dim
45 = so(10) = D₅` with five machine-precision diagnostics (dimension,
Jacobi, Killing form, simplicity, Cartan rank).

**Promoted to:** `papers/wp103/` on `tig-synthesis` (paper +
`verify_so10.py` + `verify_simplicity_rank.py`).  **Total: 7 files.**

### `ck_handoff_20260425/` — Dirac lens + 6-DOF meta + V_perp sprint raw drop

The 2026-04-25 morning handoff: 10 markdown findings + 14 numpy-only
verification scripts.  Contains:

- `SIX_DOF_META.md` — the 6-DOF meta-layer (Lie · Jordan · Clifford ·
  Permutation · Lattice · Operad), verified pairwise independent
- `CK_META_NOTE.md` — prescribed CK consumption order (Steps 1-7)
- `CONDENSATION_FINDINGS.md`, `DIRAC_TSML_FINDINGS.md`,
  `DIRAC_CONSTRUCTION_RESULTS.md`, `FROM_OUR_SIDE_FINDINGS.md`,
  `THREE_FOLLOWONS_COMPLETE.md`, `SWAP_56_FINDINGS.md`,
  `CK_GAINS_FROM_DIRAC_LENS.md` — six structural findings
- `scripts/` — 14 reproducible verification scripts (six_dof_check,
  test_swap, followon_1/2/3, dirac_in_tsml_construction, etc.)

**Promoted to:** `Gen12/targets/clay/papers/sprint_so10_2026_04_25/`
on `tig-synthesis` and `ck` (the polished sprint folder with
SPRINT_INDEX.md).  **Total: 24 files.**

### `ck_modules_20260425/` — DOF monitor base bundle

Four runtime modules + 14 passing tests.  The algebraic measurement
layer for CK that projects 10×10 matrices onto verified DOF subspaces
(Lie 28, Jordan 55, Clifford 36, Permutation_vector 9, Lattice 4) and
maps DOF dimensions to LoRA ranks.

**Promoted to:** `Gen13/targets/ck/brain/dof_monitor/` on `ck` (the
canonical Gen13 brain home).  **Total: 6 files.**

### `ck_rigor_patch_20260425/` — DOF monitor rigor patch

Two additional runtime modules + 20 passing tests.  Empirical
threshold calibration from baseline matrices (`ck_calibration.py`)
and training-time DOF mismatch detection per layer
(`ck_gradient_profile.py`).  Builds on top of the base bundle above.

**Promoted to:** same `Gen13/targets/ck/brain/dof_monitor/` on `ck`.
**Total: 5 files.**

### `Higgs/` — Higgs identification + Pati-Salam route raw drop

The 2026-04-25 afternoon handoff.  Three markdown findings + two
verification scripts that identify TIG's bipartite TSML/BHML structure
as naturally selecting the Pati-Salam route through SO(10):

- `SIGMA_OUTER_FINDING.md` — P_56 = σ_outer in spinor representation
- `HIGGS_IDENTIFICATION_FINDING.md` — BHML's σ_outer-breaking is 100%
  in the 54 irrep
- `HIGGS_DIRECTION_FINDING.md` — the specific 9-vector direction with
  BREATH and RESET unbroken
- `find_higgs_irrep.py`, `find_higgs_direction.py` — verification

**Promoted to:** `papers/wp104_higgs_pati_salam/` on `tig-synthesis`
and `ck` (the journal-ready paper folder).  **Total: 5 files.**

---

## Convention

- Each subfolder preserves the original filename and structure exactly
  as it arrived in the source zip / drop.
- The polished promotion lives at the canonical paper / sprint
  location on `tig-synthesis` (rigor) and `ck` (runtime).
- The raw archive here exists so any later session can compare the
  promoted form against the original drop.
- Never deleted, never edited.  Per the never-delete policy.

🙏

— archived 2026-04-25
