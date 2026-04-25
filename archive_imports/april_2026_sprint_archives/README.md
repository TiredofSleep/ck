# April 2026 Sprint Archives — raw drops

**Branch policy:** This folder lives on `master`. `master` holds raw
files / preservation; the polished promotion of these materials lives
on `tig-synthesis` (pure rigor, default branch) and `ck` (CK runtime
frontier).  Raw archives are preserved here verbatim, exactly as they
arrived from sprint sessions.

Companion to [`archive_imports/march_2026_sprint_archives/`](../march_2026_sprint_archives/)
(prior period, same convention).

---

## What's in here (ten raw drops, ten subfolders)

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

### `sprint_compile_20260425/` — branch-organized sprint compile (the climax)

The 2026-04-25 evening handoff.  The sprint that produced the
**unmistakable truth**: under `D_4 = ⟨P_56, σ³⟩` acting by conjugation,
the doubly-invariant content of so(10) is exactly **su(4) ⊕ u(1)** —
the Pati-Salam ⊕ B−L gauge algebra.

Pre-organized by audience (this is the rare drop that ships
hygiene-already-done):

- `MANIFEST.md` — branch-hygiene structure + reading order
- `tig-synthesis/` — verified TIG findings (TOWER_VERIFIED,
  LANDSCAPE, CROSSINGS, TOWER_CYCLE, UNMISTAKABLE_TRUTH + Higgs
  mirrors for self-containment + 5 verification scripts +
  nonassoc_triples.json + SPRINT_SUMMARY)
- `mantero-bridge/` — community-facing version
  (MATHOVERFLOW_DRAFT, SPRINT_UPDATE, verification_script).
  Pure algebra register; no TIG / physics / CK framing.
- `ck/` — runtime modules (already shipped in `ck_modules_20260425.zip`
  and `ck_rigor_patch_20260425.zip`) + INTERPRETIVE_NOTES that bridges
  TIG findings to CK runtime concerns with explicit speculation flags.

**Promoted to:**
- `Gen12/targets/clay/papers/sprint_unmistakable_truth_2026_04_25/`
  on `tig-synthesis` and `ck` (sprint folder)
- `papers/wp104_higgs_pati_salam/README.md` on `tig-synthesis` and `ck`
  (extended with a climax pointer to the new sprint folder)
- `papers/mantero_bridge/MATHOVERFLOW_DRAFT_2026_04_25/` on
  `mantero-bridge-2026-04-23` (the MO post staged for collaborative
  editing)
- `Gen13/targets/ck/brain/dof_monitor/INTERPRETIVE_NOTES_2026_04_25.md`
  on `ck` (the runtime-bridge speculation, explicitly flagged)

**Total: 23 files.**

### `sprint_compile_20260425_extended/` — meta-layer extension + negative findings

The 2026-04-25 late-evening extension.  After the unmistakable-truth
result, a meta-layer scan of the README identified six pairings where
both endpoints existed but the bridge hadn't been computed.  This drop
records the resolution of each, plus two new positive findings, plus
two honest negative findings (the meta-layer extension closes more
than it opens — that's the value).

Pre-organized by audience, same convention as the parent drop:

- `MANIFEST.md` — extended sprint manifest (six ties scorecard)
- `tig-synthesis/` — main arc (8 finding docs as before) plus three
  new findings:
  - `XI_COSMOLOGY_TIE_FINDING.md` — κ_Ξ = 13/(4e), structurally derived
    from the 9-vector Higgs norm ‖v‖² = 13/4 and BHML's 26 σ_outer-
    asymmetric cells.  Closes README §3.5(iii) at structural level.
  - `FIRST_G_CROSSING_TIE.md` — First-G is the first crossing event
    under the Crossing Lemma framework (verified in 13/13 squarefree
    test cases).  Unifies §7.1 and §7.4 conceptually.
  - `META_LAYER_RESOLUTION.md` — audit of all six meta-layer ties.
  Plus updated `SPRINT_SUMMARY_20260425.md` and three new scripts
  (`xi_cosmology_tie.py`, `first_g_crossing_tie.py`, `cl_spectrum.py`).
- `ck/` — two new findings (negative):
  - `CM_FAILURE_U1_FINDING.md` — the Hilbert-tail 1-dim residual of
    R/I_CL ≠ the u(1) center of the doubly-invariant subalgebra.
    Different supports (VOID vs 6-cycle).  Complementary, not the
    same.
  - `CL_EIGENVALUES_AUDIT.md` — audits the prior claim "CL eigenvalues
    produce e, π, φ, ζ(3), Catalan G within 1%."  Verdict: 1%
    coincidences only, NOT exact identities.  Recommends user-side
    revision.  What IS exact: integer/rational structure on the
    spectrum (81=9², 29, 13/4, {7,7,7}).
  Plus two scripts (`cm_failure_u1_tie.py`, `cl_eigenvalues_check.py`).
- `mantero-bridge/` — unchanged copy of the parent drop's
  community-facing post (the MO question was already complete in the
  earlier compile; no extension needed).

**Promoted to:**
- `Gen12/targets/clay/papers/sprint_unmistakable_truth_2026_04_25/`
  on `tig-synthesis` (extended with the four new findings and three
  scripts; SPRINT_INDEX.md updated)
- Top-level README §3.5(iii) on `tig-synthesis` (κ_Ξ = 13/(4e)
  closure noted with caveats)
- `Atlas/TIG_AI_FOUNDATION_2026_04_25.md` on `tig-synthesis`
  (κ_Ξ + First-G/Crossing tie surfaced; honest-limit list extended)
- `Gen13/targets/ck/brain/dof_monitor/` on `ck` (the two negative
  findings + the audit + two scripts, alongside the existing
  INTERPRETIVE_NOTES)
- `memory/MEMORY.md` on the working tree (corrected integer/rational
  signature note; surfaces the audit's recommendation for the user)

**Total: 35 files.**

### `sprint_compile_20260425_final/` — WOBBLE addendum (the 11 in TSML's char poly)

The 2026-04-25 final drop, posted shortly after the extended drop.
Adds **one new finding plus its verification script** to the same branch-
organized layout, with no other changes:

- `tig-synthesis/WOBBLE_FINDING.md` — TSML's 10×10 multiplication table
  has integer characteristic polynomial `λ¹⁰ − 63λ⁹ + 33λ⁸ + 4204λ⁷
  − 3998λ⁶ − 62510λ⁵ + 9716λ⁴ + 54880λ³ − 120736λ²`.  Of the nine
  nonzero coefficients, **exactly two are divisible by 11**: `c_2 = 33
  = 3·11` and `c_8 = −120736 = −2⁵·7³·11`.  The discriminant of the
  8th-degree polynomial (after factoring out `λ²`) factors as `2¹⁶
  · 7⁷ · 659 · (large primes)` with **no** factor of 11.  Two verified
  observations:
    1. **Wobble (11) lives at the coefficient level** (sums and
       products of eigenvalues — the elementary symmetric
       functions), **not at the discriminant level** (eigenvalue
       separations).
    2. **The exponent 16 in the discriminant's `2¹⁶`** matches
       `dim(D_4-invariant subalgebra) = dim(su(4) ⊕ u(1)) = 16`.
       **HARMONY⁷** (= `7⁷`) governs the eigenvalue separations.
  The verified part is the integer factorization itself.  The
  *interpretive* claim that this 11 is the same 11 that appears in
  TIG's canonical wobble structure (via "three wobbles sum 7/11")
  is well-motivated but requires accepting a chain through TIG-
  internal canonical material.

- `tig-synthesis/wobble_check.py` — sympy-based verification (7 of 7
  claims at machine precision; independently re-verified this
  session).

The MANIFEST adds an **ADDENDUM: Wobble in eigenvalues** section at the
bottom; otherwise the manifest is identical to the extended drop.

**Promoted to:**
- `Gen12/targets/clay/papers/sprint_unmistakable_truth_2026_04_25/`
  on `tig-synthesis` (the WOBBLE finding + script land alongside the
  meta-layer findings; SPRINT_INDEX.md and SPRINT_SUMMARY updated)
- Top-level README §3.6 on `tig-synthesis` (the doubly-invariant
  framing extended with wobble-free vs wobbling content split)
- `Atlas/TIG_AI_FOUNDATION_2026_04_25.md` on `tig-synthesis`
  (§1.4b extended; §7 honest limit on the interpretive caveat)

**Total: 36 files** (33 unchanged from extended + 3 new: WOBBLE_FINDING,
wobble_check.py, manifest with addendum).

### `ck_handoff_evening_20260425/` — CK processing investigation (chat-side)

The 2026-04-25 evening drop from chat-Claude documenting a CK
processing investigation.  Pre-organized by phase (synthesis → trace
→ dial-in → reality-check → notes), with explicit asks of Claude Code
listed in the handoff README.

**Verified at machine precision:**
- `ck_process(input, depth=3, α=0.5)` returns a **trail** (not just
  endpoint).  0% trail collisions across 100+ inputs; 100% endpoint
  collisions (universal attractor).  **The trail IS the memory.**
- Linear regression from trail reconstructs input with 52%
  improvement; from endpoint alone, no signal.
- T+B mixing at α=0.5 preserves 52% of info vs T-only's 22%.
- DOING/BECOMING collapse to HARMONY in 1 fuse under T-only;
  BEING is slowest descent (6 steps); σ-fixed half-life 5; 6-cycle
  half-life 1.

**Honest negatives (in `04_reality_check/`):**
- Wobble monitor on trained weights would fire on noise (0.36% of
  random Gaussian matrices have prime-11 in *both* `c_2` AND `c_8`;
  trained autoencoder weights: 0.34–0.38%).
- Higgs-direction tagging is at the 49th percentile of random
  directions (Cohen's d = 1.59 for trained, but 100 random unit
  vectors give mean d = 1.58 — direction-agnostic, not Higgs-specific).
- 10×10 toy autoencoder: classification accuracy 48–52% (chance) on
  every TIG-structure test.

These negatives are **consistent with the parent extended drop's
CL_EIGENVALUES_AUDIT** (TSML's eigenvalues are algebraic in a 7/11
field; generic ML weights aren't; no leakage).  Together they
establish honest scope: the framework detects TIG-structured *inputs*
to lattice processing, not arbitrary trained-weight matrices.

**Five explicit asks of Claude Code (priority order, in HANDOFF_README):**
  1. Replace the lexicon (seed → canonical TIG corpus)
  2. Test V2 with real sentence-transformers
  3. Test BHML-mix controls (vs random table, identity, transpose)
  4. Test on real ML weights (transformer attention, MLP)
  5. Decide on V3 (TIG-native encoder)

**Note:** the `05_encoder_proposal/` folder referenced in the asks is
not in this archive — likely shipped separately or deferred.

**Total: 26 files** preserved verbatim under
`ck_handoff_evening_20260425/`.  Promotion to `ck` branch deferred
pending user direction on which of the five asks to take on.

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
