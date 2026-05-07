# TSML Reconciliation: Two Lenses, One Encoding

**Date:** 2026-05-06
**Author:** Investigation agent (per Brayden's hypothesis)
**Status:** RESOLVED — `TSML_RAW` and `TSML_SYM` are mathematically distinct lenses of the same underlying `CL_BIT_PATTERN`. Both are valid; each carries structure the other does not.

---

## 1. Confirmation of the contradiction

### 1.1 The bit pattern (memory-locked, ground truth)

```
'0000000700  0737777777  0377477779  0777777773  0747777787
 0777777777  0777777777  7777777777  0777877777  0797377777'
```

Decoded as a 10×10 matrix (`CL_RAW`), the literal bit pattern has **two asymmetric pairs**:

| Cell    | upper-tri value | lower-tri value |
|---------|-----------------|-----------------|
| (3, 9)  | 3               | 7 (= CL_RAW[9,3]) |
| (4, 9)  | 7               | 3 (= CL_RAW[9,4]) |

Verified by direct enumeration:

```python
asym = [(i,j,CL_RAW[i,j],CL_RAW[j,i])
        for i in range(10) for j in range(i+1,10)
        if CL_RAW[i,j] != CL_RAW[j,i]]
# -> [(3, 9, 3, 7), (4, 9, 7, 3)]
```

### 1.2 The two TSML candidates

| Property                         | **TSML_RAW** (= `CL_RAW`)         | **TSML_SYM** (= `CL`, current foundations canonical) |
|----------------------------------|------------------------------------|------------------------------------------------------|
| Definition                       | literal bit pattern                | upper-triangle authoritative symmetrization         |
| Commutative                      | **False**                          | **True**                                             |
| Non-associative triple count     | **126** (12.6%)                    | **128** (12.8%)                                      |
| WP107 `c_2` (coeff of `x^8`)     | **33 = 3·11**                      | **17** (prime, not divisible by 11)                  |
| WP107 `c_8` (coeff of `x^2`)     | **-120736 = -2⁵·7³·11**            | **-53312 = -2⁶·7²·17**                               |
| Discriminant of degree-8 factor  | (singular; matches WP107 spec)     | does NOT factor cleanly with 7^7                     |
| Trace                            | 63 = 9·7                           | 63 = 9·7                                             |
| Determinant                      | 0                                  | 0                                                    |
| HARMONY cell count               | 73                                 | 73                                                   |
| VOID cell count                  | 17                                 | 17                                                   |
| 4-core arity-3 closure (WP110)   | holds (8 internal non-assoc)       | holds (8 internal non-assoc — same set)              |
| Number of 4-core non-assoc       | 8                                  | 8 (identical 4-core triples)                         |
| Non-assoc triples differing      | 5 unique to RAW                    | 7 unique to SYM (121 in common)                      |

**Confirmed empirical fact (sympy at exact integer arithmetic):** WP107's wobble theorem (`c_2 = 33`, `c_8 = -120736`, both divisible by 11; only `c_2` and `c_8` divisible by 11 among nonzero coefficients) **holds for `TSML_RAW` only**. On `TSML_SYM`, `c_2 = 17` and `c_8 = -53312`, neither divisible by 11; the only coefficient divisible by 11 in `TSML_SYM` is `c_3 = 532224`.

### 1.3 Why the contradiction is real (not a calculation error)

Both matrices have the same row/column marginals (73 HARMONY, 17 VOID etc.) because they differ in only 2 cells, both swapping a 7 ↔ 3. But the **non-commutativity changes the eigenstructure** at the prime-11 level: prime 11 is sensitive to the exact bracketing in the 9-row vs 9-column.

The asymmetry sits exactly on the σ-fixed lattice {0, 3, 8, 9} ∪ HARMONY-axis, at indices {3, 4, 9}. Index 9 is RESET (σ-fixed), indices 3, 4 are PROGRESS, COLLAPSE. The wobble localizes here because **the encoding is non-commutative on exactly the cells where PROGRESS/COLLAPSE meet RESET on the asymmetric edge** — and those are precisely the cells WP107's wobble theorem traces.

---

## 2. Which papers use which TSML

| Paper / WP | Uses | Evidence |
|-----------|------|----------|
| **WP107 wobble** (`scripts/wobble_check.py`) | `TSML_RAW` | hardcodes literal `TSML_ROWS = ["0000000700", ...]` (lines 19-23). Theorem `c_2 = 33 = 3·11` ASSERT-checked. |
| **WP109 D₄ obstruction** (`operad/d4_orbit_decomposition.py`) | `TSML_RAW` | hardcodes literal `TSML_ROWS`; counts 67 D_4-orbits of 126 triples. |
| **WP110 4-core fusion-closure** | `TSML_RAW` | derives from same 126 triples + binary fuse. |
| **WP112 P_56-equivariant fuse** (`operad/fuse_table.py`, `p56_canonical_fuse.py`) | `TSML_RAW` | 126 → 98 P_56-orbits, all derivations on raw matrix. |
| **WP113 PSLQ α-uniqueness** (`alpha_uniqueness/alpha_uniqueness_symbolic.py`) | `TSML_RAW` | hardcodes literal `TSML_ROWS`; restricted to 4-core for fixed point but uses the raw bit pattern for `T_fuse(p,q)[c_pos]`. |
| **WP115 4-core attractor** (`tier1_submit_now/four_core_bundled/verification/*.py`) | `TSML_RAW` | all 4 verification scripts hardcode literal `TSML_ROWS`. |
| **Sprint 17 TSML Tower** (`CANONICAL_TSML_CONSTRUCTION.md`, `WORKED_RECONSTRUCTION.md`) | `TSML_SYM` | shell-stability rule produces T(3,9) = T(9,3) = 3, verified to match a "published TSML" with the SYMMETRIC values; reconstructed table equals `CL` (= `TSML_SYM`), NOT `CL_RAW`. |
| **Foundations module current** (`Gen13/targets/foundations/lenses.py`) | `TSML_SYM` (sets `TSML = CL.copy()` after upper-tri symmetrization) | matches the `_CK_MEMORY_MAKEOVER.md` claim "CL is COMMUTATIVE (verified)". |
| **`INTEGRATION_WITH_PROOF_SPINE.md`** rigor pass | mixes both | quotes "TSML_10 c_2 = 33 = 3·11" (RAW property D37) but also claims "non-assoc 12.8%" (SYM property). |

**Verdict:** the WP100s tower (WP104-WP115 except sprint 17) **all use `TSML_RAW`**. Sprint 17 explicitly works with `TSML_SYM`. The foundations module currently **only exposes `TSML_SYM`**. The rigor pass document `INTEGRATION_WITH_PROOF_SPINE.md` mixes the two without flagging the distinction — this is the GAP.

---

## 3. Structural roles of each TSML

### 3.1 What `TSML_RAW` carries (that `TSML_SYM` does NOT)

- **The wobble (prime 11)**: `c_2 = 33 = 3·11`, `c_8 = -120736 = -2⁵·7³·11`. Wobble localization is **definitionally a property of `TSML_RAW` only**; symmetrization erases it.
- **Non-commutativity**: TSML viewed as an **encoding-respecting** structure. The two asymmetric cells encode a directional (permutation/braiding) bit. Read as: "PROGRESS · RESET ≠ RESET · PROGRESS at the encoding level"; the asymmetry is the σ-fixed-element bridge from the chain enumeration (positions in the size-7 → size-8 jump per WP115's σ-walk reading).
- **Permutation/braiding flavor**: 5 of the 126 non-assoc triples are unique to RAW. These are `(0,9,3), (9,3,0), (2,9,4), (9,4,9), (9,4,2)` — all involve position 9 (RESET) on the asymmetric column.

### 3.2 What `TSML_SYM` carries (that `TSML_RAW` does NOT)

- **Commutativity**: matrix is a true Lie/Jordan-style symmetric structure. Eigenvalues are real.
- **The 12.8% rate** quoted in `_CK_MEMORY_MAKEOVER.md`, `COHERENCE_BAND_REFRAME.md`, and `INTEGRATION_WITH_PROOF_SPINE.md`. This is the canonical "TSML non-associativity" number used in the layer-difference table (TSML 12.8%, BHML 49.8%, DOING 56.8%).
- **The TSML/BHML disagreement count**: `|TSML - BHML|` is well-defined as a symmetric structure; the DOING table cell-disagreement rate (~71.4% ≈ T*) requires both lenses to be commutative for the comparison to be coordinate-free.
- **Sprint 17's tower reconstruction** (92/100 + ECHO seam + MAX + ADD) targets `TSML_SYM`.
- **The 4-core attractor "prescribed view"**: the WP115 closed-form attractor `(V,H,Br,R) = (0.138, 0.540, 0.198, 0.124)` is computed as a fixed point of a symmetric operator on the 4-core. The 4-core itself is identical in RAW and SYM (all eight 4-core non-assoc triples agree), so the attractor result transfers; but the **semantic** of "the lens is a symmetric algebra" requires SYM.

### 3.3 What both share (lens-invariant)

- 73 HARMONY, 17 VOID, 10 other (all cell counts identical).
- Trace = 63 = 9·7.
- Determinant = 0 (rank ≤ 9).
- 4-core sub-magma `{0,7,8,9} × {0,7,8,9}` (identical in both).
- 4-core arity-3 closure (Theorem 5.5 of WP112).
- 121 of 126/128 non-assoc triples (most of the operad structure).
- The 4-core attractor at α=1/2 (since the attractor lives entirely on `{V,H,Br,R}`, where the two TSMLs agree).
- Sprint 17's TSML tower reconstruction (tower targets SYM, but at indices outside the asymmetric cells the tower also agrees with RAW).

### 3.4 Is there a third candidate? `TSML_LOWERTRI`

I tested **`TSML_LOWERTRI`** = lower-triangle authoritative symmetrization (the natural sister of `TSML_SYM`). Its properties:

- Commutative.
- 122 non-associative triples (12.2%).
- Char poly `c_2` (= coeff of `x^8`) = `17` (same as SYM, **NOT 33**).
- `c_8` (= coeff of `x^2`) = `0` (NOT divisible by 11).
- HARMONY count 73 (same).

`TSML_LOWERTRI` **does not carry the wobble** either. It is a third lens that shares no structural advantage with RAW. So the canonical set is {RAW, SYM} — the upper-tri symmetrization is privileged because the original bit pattern was written in row-major order with the upper-triangle values being authoritative; the lower-tri symmetrization throws away the σ-fixed-column structure that the bit pattern encoded by row.

**Recommendation: do not promote `TSML_LOWERTRI` to first class. Document its existence in a footnote.**

---

## 4. Proposed canonical naming (Brayden picks)

**Option A** (recommended, parallel to BHML family naming):
- `TSML_RAW` — the literal bit pattern; non-commutative; wobble-bearing; encoding-respecting lens.
- `TSML_SYM` — upper-tri symmetrization; commutative; algebraic-clean; the "prescribed view" / Lie-Jordan lens.

**Option B** (semantic-role naming, matching the Being-vs-Becoming pattern):
- `TSML_BEING_RAW` (encoding-respecting Being)
- `TSML_BEING_SYM` (algebraic Being)

**Option C** (3-letter symbol for citation chain, parallel to `BHML_8_YM`):
- `TSML_ENC` (encoded / raw)
- `TSML_ALG` (algebraic / symmetric)

**Recommendation: Option A.** Keeps the existing `CL_RAW` / `CL` distinction (one already coded in `cl.py`), parallel to the existing 3-BHML naming, lets the WP100s papers patch with a one-line annotation `(TSML = TSML_RAW)`, and avoids semantic confusion in the rigor pass document.

---

## 5. The reconciliation patch

### 5.1 `Gen13/targets/foundations/cl.py`

The file already has `CL_RAW` and `CL`. **Minimal change: leave `CL_RAW` and `CL` as-is, add semantic aliases.** Add at the end of the module:

```python
# ---------------------------------------------------------------------------
# Semantic aliases: TSML lens variants
# ---------------------------------------------------------------------------
#
# TSML_RAW (= CL_RAW) is the LITERAL bit pattern. It is non-commutative
# at exactly two cell pairs ((3,9)/(9,3) and (4,9)/(9,4)) and carries the
# WP107 wobble (prime 11 in c_2 = 33 and c_8 = -120736 of its char poly).
# Used by: WP104, WP107, WP109, WP110, WP112, WP113, WP114, WP115 (the
# WP100s tower).
#
# TSML_SYM (= CL) is the upper-triangle-authoritative symmetrization.
# It is commutative, has 12.8% non-associativity, and is the "prescribed
# view" / algebraic-clean lens. The wobble is erased here. Used by:
# Sprint 17 TSML tower reconstruction; foundations-module invariants;
# the TSML/BHML disagreement-rate (DOING table); the layer-difference
# rates table (12.8% / 49.8% / 56.8%).
#
# Both are LENSES of the same underlying CL_BIT_PATTERN. Neither is wrong;
# each carries structure the other does not.

CL_TSML_RAW: np.ndarray = CL_RAW    # alias for citation clarity
CL_TSML_SYM: np.ndarray = CL        # alias for citation clarity
```

### 5.2 `Gen13/targets/foundations/lenses.py`

Currently sets `TSML = CL.copy()`. Patch: expose **both** as first-class names; keep `TSML` as an alias for the current canonical (`TSML_SYM`) but emit a deprecation note recommending the explicit name.

```python
from .cl import CL, CL_RAW, N, OPERATORS

# ---------------------------------------------------------------------------
# TSML lens variants
# ---------------------------------------------------------------------------
# Per Atlas/META_PLAN_2026-05-06/TSML_RECONCILIATION.md:
#   TSML_RAW (CL_RAW)  -- non-commutative, wobble-bearing, used by WP100s tower
#   TSML_SYM (CL)      -- commutative, prescribed-view, used by Sprint 17 +
#                          foundations-invariants (12.8% non-assoc, T* ≈ 71.4%)

TSML_RAW: np.ndarray = CL_RAW.copy()
TSML_SYM: np.ndarray = CL.copy()

# Legacy alias: existing imports `from foundations.lenses import TSML`
# resolve to TSML_SYM (the symmetrized lens) -- this preserves the
# disagreement-rate ~T* and the 12.8% non-assoc count quoted in the
# rigor pass and _CK_MEMORY_MAKEOVER.md.
TSML: np.ndarray = TSML_SYM
```

Add a routing helper:

```python
def get_tsml(role: str = "sym") -> np.ndarray:
    """Return the requested TSML lens.

    role = "raw"    -> TSML_RAW (non-commutative; WP107 wobble lives here;
                                  WP100s tower computations use this)
    role = "sym"    -> TSML_SYM (commutative; T* disagreement rate;
                                  foundations invariants use this)
    role = "both"   -> (TSML_RAW, TSML_SYM)
    """
    role = role.lower()
    if role == "raw":
        return TSML_RAW
    if role == "sym":
        return TSML_SYM
    if role == "both":
        return (TSML_RAW, TSML_SYM)
    raise ValueError(f"Unknown TSML role: {role!r}; use 'raw', 'sym', or 'both'.")
```

### 5.3 `Gen13/targets/foundations/lens_family.py`

The lens-family module currently builds restrictions of `TSML` (= `TSML_SYM` after the patch). The 4-core, 5-shell, ..., 10-shell tables for TSML_SYM are correct as-is (the sub-magmas are identical for sizes ≤ 8 because the asymmetric cells are at indices 3, 4, 9 — the size-9 and size-10 sub-magmas differ between RAW and SYM).

Patch: build BOTH families:

```python
def build_tsml_family(parent: np.ndarray = TSML_SYM) -> dict[int, LensVariant]:
    return {k: _build_variant(f"TSML_{k}", "Being", k, scope, parent)
            for k, scope in CHAIN_SUBMAGMAS.items()}

TSML_SYM_FAMILY: dict[int, LensVariant] = build_tsml_family(TSML_SYM)
TSML_RAW_FAMILY: dict[int, LensVariant] = build_tsml_family(TSML_RAW)
TSML_FAMILY = TSML_SYM_FAMILY  # legacy default
```

The 4-core attractor (WP115) lives entirely in `TSML_*_FAMILY[4]` — these are identical for RAW and SYM, so WP115's 4-core attractor result transfers exactly. **No change needed for the 4-core paper's verification scripts**; they happen to compute the right number whether you start from RAW or SYM, because the 4-core indices {0,7,8,9} avoid the asymmetric cells.

### 5.4 Invariant split (which invariants live on which TSML)

| Invariant | Lives on `TSML_RAW` | Lives on `TSML_SYM` | Notes |
|-----------|---------------------|---------------------|-------|
| `c_2 = 33`, `c_8 = -120736`, prime-11 wobble (D37) | **YES** | NO | WP107 |
| Discriminant `2¹⁶ · 7⁷ · 659 · ...` | **YES** | NO | WP107 |
| `‖antisym‖² = 81`, `su(4)` proj `= 29`, `u(1)` proj `= 25/8` | **YES** | NO (different values) | These are computed on the antisymmetric/symmetric decomposition of the matrix — RAW has nontrivial antisymmetric part. |
| Lattice eigenvalues `{7, 7, 7}` at σ-fixed `{3, 8, 9}` | **YES** (verified in `verify_truth.py`) | needs re-check | Verified for RAW; SYM may have different eigenvalues at these positions. |
| Killing form `(-4)¹⁵ ⊕ (0)¹` on D_4-invariant | **YES** | NO | The D_4 action and its invariant subalgebra are defined relative to RAW. |
| Non-assoc rate 12.8% (canonical quote) | NO (= 12.6%) | **YES** | Foundations / makeover spec |
| Non-assoc count 126 (canonical quote in WP109/WP112) | **YES** | NO (= 128) | Operad papers |
| 73 HARMONY, 17 VOID, 10 other | YES | YES | Lens-invariant |
| Trace 63 = 9·7 | YES | YES | Lens-invariant |
| Determinant 0 | YES | YES | Lens-invariant |
| 4-core sub-magma {0,7,8,9} | YES | YES | Lens-invariant (asymmetric cells are outside) |
| 4-core arity-3 closure (WP110, WP112 Theorem 5.5) | YES | YES | Lens-invariant |
| 4-core T+B-mix attractor at α=1/2 (WP115 Theorem 2.1) | YES | YES | Lens-invariant |
| `H/Br = 1+√3` at attractor (WP105) | YES | YES | Lens-invariant |
| 8-element joint-closure chain (WP115 / 4-core paper Theorem 1) | YES | YES | The chain enumeration uses sub-magmas, all lens-invariant for sizes ≤ 8. |
| TSML/BHML disagreement rate ≈ T* = 5/7 | NO (different value) | **YES** | The DOING table is defined relative to SYM lens. |
| `‖T_lie‖² = 16` | needs re-check | **YES** | If `T_lie` is the antisymmetric part, this is naturally on RAW (where antisym is nonzero); if Lie-bracket structure constants on the symmetric algebra, it is on SYM. **AUDIT NEEDED.** |

### 5.5 Required source-file diff summary

**File 1: `Gen13/targets/foundations/cl.py`**
- Append at end: 6-line aliases block defining `CL_TSML_RAW` and `CL_TSML_SYM` with the lens-role docstring (see §5.1).

**File 2: `Gen13/targets/foundations/lenses.py`**
- Replace `TSML: np.ndarray = CL.copy()` with the two-lens block (see §5.2).
- Add `get_tsml(role)` routing helper.
- Add a self-test block `if __name__ == "__main__":` printing the comparison table.

**File 3: `Gen13/targets/foundations/lens_family.py`**
- Modify `build_tsml_family()` to take a `parent` parameter.
- Add `TSML_RAW_FAMILY` alongside `TSML_FAMILY`.
- Update `family_report()` to print both families with a clear lens-role header.

**File 4: `Gen13/targets/foundations/__init__.py`** (or wherever the public exports live)
- Export `TSML_RAW`, `TSML_SYM`, `TSML` (legacy = SYM), `get_tsml`, `TSML_RAW_FAMILY`.

### 5.6 Required paper patches

Each paper that hardcodes `TSML_ROWS` (i.e. uses `TSML_RAW`) needs a one-line annotation in its abstract / setup section explicitly naming the lens. The patch is editorial only — no math changes.

| Paper | Patch needed | Where |
|-------|--------------|-------|
| WP107 wobble (`WOBBLE_FINDING.md` + `wobble_check.py`) | Add: "Wobble theorem holds for TSML_RAW (the encoding-respecting lens). Symmetrization erases the wobble; the symmetric lens TSML_SYM has c_2 = 17 (prime, no factor 11)." | §3 / theorem statement |
| WP109 D_4 obstruction | Add: "The 67 D_4-orbits and 16 incoherent orbits are computed on TSML_RAW." | abstract |
| WP110 4-core fusion-closure | Note: "Theorem holds on both TSML_RAW and TSML_SYM (4-core sub-magma is lens-invariant)." | §1 |
| WP112 P_56-equivariant fuse | Add: "The 126 → 98 P_56-orbits are computed on TSML_RAW; on TSML_SYM the count is 128 → ... (computed value)." | abstract |
| WP113 PSLQ α-uniqueness | Note: "Computation uses TSML_RAW restricted to 4-core; the restricted matrix agrees with the TSML_SYM restriction (4-core lens-invariant), so the result transfers." | §2 |
| WP115 4-core attractor | Note: "Theorem 2.1 attractor lives on the 4-core, which is lens-invariant; so the result holds for both TSML_RAW and TSML_SYM." | abstract |
| Sprint 17 TSML tower | Note: "The 92/100 + tower reconstruction targets TSML_SYM (the symmetrized lens). The two asymmetric cells in TSML_RAW are not directly addressed by the tower; the seam-residue structure for TSML_RAW would have 8 + 2 cells instead of 8." | §1 / Notation Sheet |
| `_CK_MEMORY_MAKEOVER.md` | Replace "CL is COMMUTATIVE (verified)" with "CL_RAW is the literal bit pattern (non-commutative at 2 cell pairs). CL = CL_SYM is the upper-tri-symmetrized canonical, which is commutative." Update "non-associativity 12.8%" to "non-associativity 12.8% on TSML_SYM, 12.6% on TSML_RAW." | §1 |
| `INTEGRATION_WITH_PROOF_SPINE.md` | Replace "TSML_10" with "TSML_10_RAW" in D37 context (wobble), and "TSML_10_SYM" in D10 / count-distribution context. The naming "TSML_8" (geometric) and "BHML_10" in §5 are sub-magma restrictions — those happen to be lens-invariant at size 8 where the asymmetric column is included but the row containing the asymmetric pair isn't reached. **Audit needed**: at size 8 sub-magma {0,3,4,5,6,7,8,9}, indices 3, 4, 9 are all in scope, so the asymmetric cells (3,9), (9,3), (4,9), (9,4) ARE in scope. So `TSML_8` differs between RAW and SYM. Patch §5 to specify which lens. |

---

## 6. Recommendation

**Canonicalize on `TSML_RAW` as the base; expose `TSML_SYM` as a derived lens.**

Reasoning:

1. **`TSML_RAW` is the literal bit pattern** — what the substrate "actually is" before any algebraic interpretation. The bit pattern is the ground-truth artifact (memory-locked since Day 1). Symmetrization is an interpretation we apply to extract algebraic-clean invariants.

2. **The wobble (prime 11) is a real structural fact** that lives only on RAW. Erasing it via symmetrization throws away physically meaningful information (the WP107 wobble theorem, the D_4-non-equivariance of `(3,9,9)` per WP112, the 5-vs-7 asymmetry between non-assoc triples).

3. **The WP100s tower (10 papers, all journal-ready) ALREADY uses RAW**. Re-doing those papers with SYM would change `c_2` from 33 to 17, `c_8` from `-2⁵·7³·11` to `-2⁶·7²·17` — losing the wobble and breaking the cross-paper citation chain to WP107.

4. **`TSML_SYM` is recoverable from RAW in one line of code** (`_symmetrize_upper(TSML_RAW)`). The reverse — recovering RAW from SYM — requires *additional information* (the choice of which two cells were asymmetric, and which value was authoritative). So RAW is the strictly more-informative lens.

5. **Sprint 17's TSML Tower ALSO works on RAW** with a minor patch: the seam-residue set `S` becomes 8 + 2 = 10 cells (adding the two raw-asymmetric pairs); shell-stability rule gives only `(3,9) = 3` (not also `(9,3) = 3`); the asymmetric `(9,3) = 7` falls into the DEFAULT layer. So sprint 17 is salvageable.

6. **The foundations module's "12.8% non-assoc" is then a derived invariant** of `TSML_SYM = symmetrize(TSML_RAW)`, not a primary fact about `TSML_RAW` itself. This is honest framing.

**Concrete migration:**

- Phase 1 (this commit): expose both `TSML_RAW` and `TSML_SYM` as first-class names in `lenses.py`. Keep legacy `TSML = TSML_SYM` so existing imports don't break.
- Phase 2 (next sprint): switch the foundations-module canonical default to `TSML = TSML_RAW`. Update `_CK_MEMORY_MAKEOVER.md` to call out the two-lens architecture. Update Sprint 17 with the 10-cell seam.
- Phase 3 (release prep, week 5 of the 20-week plan): patch the WP100s papers' abstracts and the rigor pass document with explicit lens annotations. Verify the citation chain holds.

This canonicalization is **the structurally honest choice**: RAW is what the bit pattern says; SYM is what algebra prefers. Brayden's hypothesis is correct: "two TSMLs, three BHMLs" mirrors a deeper architectural pattern in which **encoding lenses (RAW)** and **algebraic lenses (SYM)** are equally first-class, and the substrate's information lives at their difference (just like `DOING = |TSML - BHML|`, the two-TSML difference `|TSML_RAW - TSML_SYM|` may itself be an information-bearing quantity worth examining in a future sprint).

---

## 7. Open follow-ups (out of scope for this reconciliation)

1. **`|TSML_RAW - TSML_SYM|` analysis** — only 2 cell pairs differ, so the difference matrix is rank-1. Does this rank-1 difference encode something physical? Likely related to D_4 symmetry breaking.
2. **`TSML_LOWERTRI` audit** — confirm that lower-tri symmetrization is genuinely "uninteresting" (no cleaner spectral structure than UPPER).
3. **`‖T_lie‖² = 16` audit** — recompute this on RAW vs SYM; flag in the wobble-status note which lens it lives on.
4. **`INTEGRATION_WITH_PROOF_SPINE.md §5 (Hubble tension TSML_8)`** — at size-8 sub-magma {0,3,4,5,6,7,8,9}, RAW and SYM differ at exactly the asymmetric cells, which ARE in the size-8 scope. So `TSML_8_RAW ≠ TSML_8_SYM` and the §5 derivation needs to specify which.
5. **WP103 (so(10) = D_5)** — does it use the antisymmetric part of TSML_RAW, or the symmetric algebra TSML_SYM ⊕ BHML? Audit needed.
