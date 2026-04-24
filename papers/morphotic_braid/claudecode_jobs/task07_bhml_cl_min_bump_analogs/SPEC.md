# Task 07 — BHML and CL minimum-bump analogs

**Tier:** 3 (research — days of setup)
**Parent handoff:** `../CLAUDECODE_HANDOFF_MIN_BUMP.md` §Task 7

## Goal

Do BHML and CL_mult also admit 1-cell minimum perturbations from some canonical core? If yes, where — and are all three (TSML, BHML, CL) min-bump sites centered on element 7?

## Why this matters

If all three tables have 1-cell min-bumps all at element 7, that's a **structural law of ℤ/10**. If they differ, the differences are diagnostic of what each table "optimizes."

## Method

1. **Build BHML's "core"** analogous to C_0. BHML's construction (FORMULAS §6) uses 4 rules — there's no obvious "canonical operator" to perturb from the same way. Two approaches:
   - Find the `k=1` minimum-perturbation of C_0 that generates BHML-like spectra (same Catalan spectra but not ac-free — needs a different target).
   - Define a "BHML core" by stripping non-absorbing cells to match BHML's algebraic profile.
2. For each candidate core, run a 1-cell exhaustive search (100 cells × 10 values = 1000 configs, each ~60 ms → 1 minute) to find hits producing BHML's spectrum profile.
3. Same for CL_mult (multiplicative composition lattice; likely at `papers/ck_tables.py` if defined, else in `Gen12/.../being/`).

## Success criterion

Classification of minimum perturbations by target spectrum type:
- "ac-free at rank 10" (TSML-style) — which cells?
- "Catalan but not ac-free" (BHML-style) — which cells?
- "CL_mult-profile" — which cells?

## Expected runtime

Setup: days (building BHML core + CL_mult core is non-trivial).
Compute: hours once setup is defined.

## Deliverable

`papers/morphotic_braid/results/task07_bhml_cl_min_bump_result.md`:
- core definitions (canonical form for each)
- hit table per core
- cross-table comparison: do min-bump sites converge on element 7 or not?

**Tag:** `[RESEARCH TASK — TIER 3]`
