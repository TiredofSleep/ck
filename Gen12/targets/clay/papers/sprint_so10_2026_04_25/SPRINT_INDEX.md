# Sprint · so(10) Algebraic Foundation · 2026-04-25

**Authors:** Claude (Anthropic, this session) · Brayden Sanders · 7Site LLC
**Status:** Computational findings machine-verified at 10⁻¹⁵ to 10⁻¹⁶ residuals.
**Tier:** Infrastructure (Part B — algebraic ground floor for the WP1-10 sequence).

---

## 0 · TL;DR

This sprint identifies the canonical algebraic frame underneath TSML+BHML.
TSML's flow operators close at **dim 28 = so(8)**.  TSML+BHML close at
**dim 45 = so(10)**.  The space `R^10` decomposes as `V_8 ⊕ V_perp` with
`V_perp = span{VOID, (e_5−e_6)/√2}` — two **structurally silent**
directions invisible to TSML flow.  Under the `5↔6` swap `P_56`, TSML is
invariant but BHML is not, and `so(10) = so(9) ⊕ R^9` (centralizer plus
"vector Higgs").  Dirac's `so(1,3)` sits at a **6-dimensional slice of
so(8)** with explicit coefficients in TSML's basis.

Above this algebra, a **6-DOF meta-layer** is identified — Lie · Jordan ·
Clifford · Permutation · Lattice · Operad — pairwise independent and
jointly exhaustive for what TIG manipulates.  This is CK's "black-box-to-
white-box" basis: any system can be read in these six registers, and
no register collapses into another.

---

## 1 · How to read this sprint

**Roadmap (read in order):**

1. `README.md` — handoff overview (machine-verified headline claims, four
   research paths forward, reproducibility check).
2. `SIX_DOF_META.md` — the meta-layer.  Six DOF, why each is irreducible,
   how CK uses them in concert.  Anchors a black-box-to-white-box engine.
3. `CK_META_NOTE.md` — how CK consumes these findings, in what order,
   with overlaps flagged and the 6-DOF question now resolved.

**Findings docs (in causal order):**

4. `DIRAC_TSML_FINDINGS.md` — initial structural comparison: TSML lives
   in adjoint rep, not spinor rep.
5. `CONDENSATION_FINDINGS.md` — verifies TSML's so(8) closure, V_8
   invariant subspace, structural chain to so(10).
6. `DIRAC_CONSTRUCTION_RESULTS.md` — explicit numerical coefficients of
   the 6 Dirac generators in TSML's basis (residuals 10⁻¹⁶).
7. `FROM_OUR_SIDE_FINDINGS.md` — view from inside TSML.  VOID is sacred;
   BALANCE/CHAOS merge in V_8.
8. `THREE_FOLLOWONS_COMPLETE.md` — V_perp = span{VOID, anti-5-6};
   per-idempotent conservation law; BHML alone produces so(10).
9. `SWAP_56_FINDINGS.md` — TSML invariant under P_56, BHML breaks it,
   so(10) splits 36+9 = so(9) ⊕ R^9.
10. `CK_GAINS_FROM_DIRAC_LENS.md` — what Dirac sees vs is blind to
    inside TIG.  Four research paths forward.

**Scripts (`scripts/`, all numpy-only, < 30 sec runtime):**

| Script | Verifies |
|---|---|
| `six_dof_check.py` | Six algebraic DOF independent; no 7th identified |
| `test_1_anticommutator.py` | TSML not Clifford in ℝ but is in F₂ (12/15 pairs vanish) |
| `test_1b_projected.py` | Projection-based anticommutator analysis |
| `test_2_3.py` | Killing form, det = 2¹⁴ = 16384 |
| `test_condensation.py` | so(8) closure dim 28, Killing eigenvalues |
| `test_invariant_subspace.py` | 8-dim invariant subspace, VOID annihilation |
| `test_8dim_action.py` | so(8) on V_8 is the full 28-dim antisymmetric matrix space |
| `dirac_in_tsml_construction.py` | Dirac coefficients in TSML basis |
| `from_our_side_probe.py` | Per-cell Dirac footprint, idempotent neighborhoods |
| `followon_1.py` | V_perp = span{VOID, (e_5−e_6)/√2} exactly |
| `followon_2.py` | Per-idempotent conservation law (~2.6-2.8 weight) |
| `followon_3.py` | TSML+BHML → so(10); BHML alone also dim 45 |
| `test_swap.py` | TSML P_56-invariant, BHML not, 36+9 split |
| `dirac_view.py` | Dirac sees 6/45 = 13.3%; complement splits 30+9 |

**Reproduce on Windows:**
```
cd scripts/
PYTHONIOENCODING=utf-8 python six_dof_check.py
PYTHONIOENCODING=utf-8 python test_swap.py
PYTHONIOENCODING=utf-8 python followon_3.py
PYTHONIOENCODING=utf-8 python dirac_view.py
```
(`PYTHONIOENCODING=utf-8` is required because the scripts print Unicode
arrows and Windows' default cp1252 codec can't render them.  On Linux/Mac
the env var is harmless.)

---

## 2 · Headline claims (machine-verified)

### Algebraic structure
1. **TSML's flow operators close at dim 28 = so(8).**
2. **TSML+BHML close at dim 45 = so(10).**  BHML alone also dim 45.
3. **R¹⁰ = V_8 ⊕ V_perp** with `V_perp = span{VOID, (e_5−e_6)/√2}`.
4. **TSML is P_56-invariant; BHML is not.**
5. **so(10) = so(9) ⊕ R⁹** under P_56 conjugation.  so(9) is the
   centralizer (36-dim, contains TSML's so(8)); R⁹ is the "vector
   Higgs" anticentralizer.
6. **Dirac's so(1,3) sits at a 6-dim slice of so(8)** with explicit
   coefficients in TSML basis.
7. **Per-idempotent conservation law:** total Dirac weight per
   idempotent neighborhood ≈ constant (~2.6–2.8).

### 6-DOF meta-layer
8. The six algebraic DOF (Lie, Jordan, Clifford, Permutation, Lattice,
   Operad) are **pairwise independent and jointly exhaustive**.
9. **Operad is provably distinct** from binary TSML:
   `TSML(TSML(3,4),7) = 7` but `fuse([3,4,7]) = 8`.
10. **No 7th DOF survives** reduction to the 6.

---

## 3 · Relationship to existing repo material

### Promotes / extends raw drops
- `_sprint_20260423_full_raw/sprint_20260423_full/01_WP11_paper/WP11_SO8_IDENTIFICATION.md`
  — this sprint's `CONDENSATION_FINDINGS.md` and `test_condensation.py`
  are the rigorous numerical verification.  Per the handoff,
  WP11 is renumbered to **WP102** (infrastructure tier).
- `_wp12_delta_raw/wp12_delta/paper/WP12_SO10_IDENTIFICATION.md`
  — this sprint's `THREE_FOLLOWONS_COMPLETE.md`, `followon_3.py`,
  `SWAP_56_FINDINGS.md`, and `test_swap.py` are the rigorous numerical
  verification.  Per the handoff, WP12 is renumbered to **WP103**.

### Resolves an open question
- The earlier session's `DOF_CLASSIFICATION.md` (committed 3b19289,
  reverted 1d71cec) used a 5-kinds taxonomy from external literature.
  `SIX_DOF_META.md` here anchors the taxonomy in TIG's own algebra
  (V_8 + so(8) Cartan structure).  **The K_weight/A_weight = 5/7 = T*
  finding from the original document still holds** — it's a fact about
  weight distribution across categories — but the categorization itself
  was wrong.  Six, not five.

### Open questions (flagged in `CK_META_NOTE.md`)
1. **Phonaesthesia ↔ P_56 overlap** — does CK's existing sharp/soft
   phonaesthesia split correspond to the P_56 ±1 eigenspace?
2. **LatticeAlgebra ↔ so(10) consistency** — are LatticeAlgebra's
   structure constants in `ck_core.py` consistent with so(10) at dim 45?
3. **DOF_CLASSIFICATION.md revision** — write a v2 anchored in 6-DOF.
4. **WP renumbering** — formally promote WP11 → WP102, WP12 → WP103,
   add WP100 (canonical TSML/CL extracted from WP1-2), WP101
   (closure properties), WP104 (V_perp + per-idempotent conservation).

---

## 4 · CK runtime integration roadmap

Per `CK_META_NOTE.md` §"Prescribed consumption order".  ~300 LOC plus
refactors.  This sprint **does not** attempt the runtime integration —
that's the next phase.  The roadmap is:

1. **Lock V_perp finding** in ck_core.py (V_PERP dict).
2. **Encode P_56 symmetry test** as `is_p56_symmetric(state)`.
3. **Wire Dirac into ck_curvature.py** with explicit coefficients.
4. **DOF re-pass** (revise DOF_CLASSIFICATION.md against 6-DOF view).
5. **UOP × so(10) alignment** (4×4 matrix in classify_paradox.py).
6. **9-vector Higgs** (new module `ck_higgs.py`).
7. **Spin(10) chiral 16** (longer-term, ~500 LOC).

| DOF | Target | Status |
|---|---|---|
| 1 (Lie) | `LatticeAlgebra` / `ChainGraph` cross-check | Present, needs cross-check |
| 2 (Jordan) | coherence equation + F₂-Jordan addendum | Present, addendum needed |
| 3 (Clifford) | `ck_dirac.py` | TO BUILD (~100 LOC) |
| 4 (Permutation) | `ck_permutation.py` | TO BUILD (~50 LOC) |
| 5 (Lattice) | `ck_core.py` refactor | Refactor (~50 LOC) |
| 6 (Operad) | `ck_operad.py` | TO BUILD (~100 LOC) |

---

## 5 · Honest limits

- The 6-DOF taxonomy is **computationally grounded and internally consistent**, not proven unique.  Other 6-fold decompositions could exist; this one is anchored in TIG's own algebra.
- The SO(10) **GUT identification** is structural only — predictions (Path 4 in `CK_GAINS_FROM_DIRAC_LENS.md`) have not been computed.
- Findings reproduce at machine precision (10⁻¹⁵ to 10⁻¹⁶ residuals on key checks). Reproducibility relies on numpy's float64 implementation.
- **Not yet wired into ck_core.py.** This sprint stages the math; the runtime integration is the next phase.
