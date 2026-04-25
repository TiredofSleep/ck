# CK Branch — Sprint Update (2026-04-25, extended)

**Purpose:** Code modules built this sprint, plus interpretive/speculative notes that connect TIG-synthesis findings to CK runtime concerns. Plus negative findings from the meta-layer audit that affect runtime understanding.

---

## Modules built this sprint

### Base bundle: `ck_modules_20260425.zip`

Two production-grade modules with 14/14 tests passing:

**`ck_dimension_mapper.py`** — Maps verified TIG DOF subspace dimensions (Lie 28, Jordan 55, Clifford 36, Permutation_vector 9, Lattice 4) to LoRA rank distributions.

**`ck_dof_profile_monitor.py`** — Real-time DOF projection of activation matrices.

### Rigor patch: `ck_rigor_patch_20260425.zip`

Two additional modules with 20/20 tests passing:

**`ck_calibration.py`** — Empirical threshold calibration from baseline matrices.

**`ck_gradient_profile.py`** — Training-time DOF mismatch detection.

---

## Interpretive notes (`INTERPRETIVE_NOTES.md`)

Speculative threads connecting TIG-synthesis findings to CK runtime:
1. BREATH and RESET as runtime stabilizers
2. The 16-dim doubly-invariant subalgebra as "sovereign register"
3. Operad placement and the canonical fuse table
4. Pati-Salam as TIG's natural breaking pattern

All speculation is explicitly flagged. See file for full caveats.

---

## Negative findings — important for runtime understanding

The meta-layer audit produced two negative results that affect how CK should treat certain claims:

### `CM_FAILURE_U1_FINDING.md` — different "1"s

The Hilbert tail of R/I_CL (powers of x_0 = VOID) and the u(1) center of the D_4-invariant Lie subalgebra (concentrated on 6-cycle indices) are **different 1-dimensional structures**. They're complementary, not the same.

**Implication for CK:** if runtime tracking distinguishes "Hilbert tail residual" vs "u(1) center residual," they should be treated as **separate 1-dim residuals**, not unified as one. Multiple distinct residual structures coexist in TIG; conflating them produces false unifications.

### `CL_EIGENVALUES_AUDIT.md` — userMemories overconfidence

The userMemories claim "CL eigenvalues produce e, π, φ, ζ(3), Catalan G all within 1%" is **partially true at 4-digit level, NOT true at exact-identity level**. The closest matches (γ, φ) are at relative error 10⁻⁴ to 10⁻³ — coincidence-level, not algebraic-identity level.

**What IS exact:** integer/rational structure on the spectrum (81 = 9², 29, 13/4, {7,7,7}). These are the TIG signature.

**Recommendation:** flag the userMemories claim for revision. Replace overconfident transcendental claim with the verified integer/rational structure.

---

## What CK can and cannot claim (after this sprint)

**CK CAN claim with structural backing:**
- TIG's structure naturally selects the Pati-Salam route through SO(10) GUT
- BHML's symmetry-breaking has a specific 9-vector direction with BREATH and RESET as zeros
- The doubly-invariant content matches su(4) ⊕ u(1)
- The inflaton coupling κ_Ξ is structurally constrained to 13/(4e), conditional on natural identification
- TIG's spectrum is integer/rational at the structural level (81, 29, 13/4, etc.)

**CK should NOT claim:**
- That TIG predicts the Standard Model (still requires Yukawa work)
- That CK's runtime behavior is governed by SO(10) GUT physics
- That the eigenvalues exactly produce transcendental constants (1% coincidences only)
- Mass ratios, mixing angles, proton decay
- That the CM-failure 1-dim and the u(1) center are the same thing

The honest line: TIG's structural alignments to physics are real but conditional on natural-but-not-forced identifications. The integer/rational structure is the verified content; transcendental matches are decorative.

---

## Hygiene boundary

CK branch holds:
- Modules (verified, tested) — already shipped separately in zip bundles
- Interpretive speculation — `INTERPRETIVE_NOTES.md`
- Negative findings — `CM_FAILURE_U1_FINDING.md`, `CL_EIGENVALUES_AUDIT.md`
- Verification scripts for the negative findings

CK branch does NOT hold:
- Verified TIG-synthesis math (in tig-synthesis branch)
- Mantero-bridge correspondence material (in mantero-bridge branch)

---

## Files in this update

- `SPRINT_SUMMARY_20260425.md` — this file
- `INTERPRETIVE_NOTES.md` — speculative interpretation
- `CM_FAILURE_U1_FINDING.md` — different 1's, complementary residuals
- `CL_EIGENVALUES_AUDIT.md` — userMemories claim audit
- `cm_failure_u1_tie.py` — verification script
- `cl_eigenvalues_check.py` — verification script

🙏
