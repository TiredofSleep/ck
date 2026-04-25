# DOF Monitor — CK's algebraic measurement layer

**Status:** 34/34 tests passing (14 base + 20 rigor patch)
**Source session:** 2026-04-25 so(10) sprint
**Position:** CK runtime, Gen13 brain trinity adjacent

> **2026-04-25 evening update.** New CK-side speculation document
> `INTERPRETIVE_NOTES_2026_04_25.md` (this folder) cross-references the
> day's verified findings on `tig-synthesis` to runtime hygiene
> hypotheses. Verified math:
> `Gen12/targets/clay/papers/sprint_unmistakable_truth_2026_04_25/`
> on `tig-synthesis` (the 16-dim doubly-invariant subalgebra of so(10)
> under D_4 = ⟨P_56, σ³⟩ is **su(4) ⊕ u(1)**, the Pati-Salam ⊕ B−L gauge
> structure). The notes file makes explicit what's verified vs what's
> speculative. Modules in this folder are unchanged.

---

## What this is

Three layers of **read-only diagnostic** that tell you whether CK's
internal activations and training gradients are behaving in a
DOF-consistent way:

1. **Algebraic ground truth** — `ck_dof_profile_monitor.py`.  Project a
   10×10 matrix onto the verified DOF subspaces (Lie · Jordan · Clifford
   · Permutation_vector · Lattice) and emit a profile.  Concentrated
   profile = healthy.  Diffuse profile = drift.
2. **Empirical context** — `ck_calibration.py`.  Run the monitor over a
   baseline corpus of "honest" matrices (your call to define what
   honest means) and emit empirically-calibrated thresholds, replacing
   the hard-coded 0.7 default.
3. **Optimizer hygiene** — `ck_gradient_profile.py`.  Same projection
   machinery applied to gradient updates per training step.  Flag when
   the optimizer is pushing a layer in a direction that doesn't match
   its DOF tag.

Together these separate **what's true** (algebra) from **what's normal**
(calibration) from **what's healthy** (gradient alignment).  Each fails
independently and surfaces independently.

---

## Module index

| File | Role | Test count |
|---|---|---|
| `ck_dof_profile_monitor.py` | base monitor — projects 10×10 → DOF profile | 8 of 14 |
| `ck_dimension_mapper.py` | LoRA rank distribution from canonical DOF dims | 6 of 14 |
| `ck_calibration.py` | empirical threshold setting from baseline | 9 of 20 |
| `ck_gradient_profile.py` | training-time DOF mismatch detection | 11 of 20 |
| `test_modules.py` | 14 tests for base modules | runs both above |
| `test_rigor_patch.py` | 20 tests for calibration + gradient | runs both above |

Run `PYTHONIOENCODING=utf-8 python test_modules.py` and
`PYTHONIOENCODING=utf-8 python test_rigor_patch.py` for green checkmarks.

---

## Canonical DOF dimensions (verified)

| DOF | Dim | Source |
|---|---|---|
| Lie (so(8) ⊂ so(9)) | 28 | TSML flow Lie closure |
| Jordan (sym 10×10) | 55 | basis count |
| Clifford (so(9), P_56 +1 eigenspace) | 36 | so(10) centralizer |
| Permutation_vector (P_56 −1 eigenspace) | 9 | so(10) anticentralizer |
| Lattice (σ-fixed) | 4 | indices {0, 3, 8, 9} |
| **Total raw (with overlaps)** | **132** | |
| **Orthogonal partition total** | **100** | covers M₁₀(ℝ) exactly |

Subspaces overlap (Lie ⊂ Clifford; Lattice ⊂ Jordan), so the monitor
exposes two views: `raw_profile` (sums > 1) and `orthogonal_profile`
(sums to 1.0, used for concentration / diffuseness).

---

## Hygiene rules baked into the modules

The modules are deliberately disciplined.  They do **NOT**:

- Generate baseline data.  Caller decides what "honest" means.
- Auto-correct drift.  Read-only.  CK / operator decide.
- Infer DOF from layer names.  DOF tagging is a design decision.
- Use coupling-norm magnitudes.  Those are basis-dependent; we use
  basis-invariant subspace dimensions instead.

These are flagged in the module docstrings.  A wrong baseline produces
wrong thresholds — that's the most important rule.

---

## How CK uses this

The DOF monitor slots into CK's runtime as the **measurement layer**
that the AI Sovereignty Plan and the so(10) Runtime Integration Plan
both reference:

- **Sovereignty Epoch I (Sight)**: `ck/brain/lm_geometry.py` projects
  LM hidden states onto a 5-element AO basis.  The DOF monitor projects
  onto a **5-DOF basis at 10-dimension resolution** (different basis,
  same purpose: make black-box activations legible).  Both can run side
  by side.
- **Runtime Plan Step 5 (UOP × so(10))**: this is where the DOF monitor
  is most directly referenced.  Each UOP Type (I/II/III/IV) corresponds
  to a so(10) substructure (so(9) Lorentz, R⁹ vector, V_perp VOID,
  σ-rate flow).  The monitor's `orthogonal_profile` is the runtime
  classifier that maps a state to its substructure.
- **Step 6 (9-Higgs)**: the monitor's Permutation_vector slot (dim 9)
  is exactly the 9-vector Higgs subspace identified in
  `papers/wp104_higgs_pati_salam/`.  When a state has substantial
  Permutation_vector content, BHML's σ_outer-breaking is active.

See `Gen13/CK_RUNTIME_INTEGRATION_PLAN.md` for the full integration
roadmap (planned, not yet implemented).

---

## Open questions deferred from the source session

1. **Operad handler** — only one fuse rule is in CK's tables today
   (`fuse([3,4,7]) = 8`).  Building an Operad module on one data point
   would invent TIG content.  Need full fuse table first.
2. **Mode switching from associativity gaps** — 12.6% of TSML triples
   are non-associative; all gaps land on {0,3,4,7,8,9} with 7 always
   involved.  Structurally interesting but not yet enough data to drive
   runtime mode switching.

These are flagged in the modules as deliberate non-implementations.

---

## Dependencies

Pure numpy.  No torch, no sklearn, no scipy.  Both test suites run on
any Python 3.10+ in seconds.

(`PYTHONIOENCODING=utf-8` is required on Windows because the modules
print Unicode check marks.  Harmless elsewhere.)

---

## Reference

- Higgs identification + 9-vector + Pati-Salam route: `papers/wp104_higgs_pati_salam/`
- Sprint context (so(10) closure + 6-DOF meta + V_perp): `Gen12/targets/clay/papers/sprint_so10_2026_04_25/`
- Runtime integration plan: `Gen13/CK_RUNTIME_INTEGRATION_PLAN.md`
- AO basis (sister algebraic projection): `ck/brain/ao_basis.py`
- Hebbian 5×5 (cortex memory): `ck/brain/hebbian_5x5.py`

🙏
