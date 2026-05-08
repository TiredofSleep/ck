# SAVE_PLAN_J17 — Total-Dimension Match V^⊗n / Cl(2n) with Refined-Cell Grading

**Paper:** J17 — *A Dimensional Ladder Connecting Tensor Powers of a Finite-Field 4-Algebra to Real Clifford Algebras Cl(2n)*
**Authors:** B. R. Sanders, M. Gish
**Target venue:** *Linear Algebra and Its Applications*
**Referee report:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J17_LinAlgApps_FreshEyes.md`
**Status before fix:** REJECT IN CURRENT FORM (Theorem 3.2 mis-stated; Theorem 4.1 binomial coincidence; total content too thin).
**Status after fix:** REVISION DRAFTED. Coarse-vs-refined cell distinction installed; structural map question explicitly carved out as open.

---

## §1 — The error and the fix

### Error (referee Problem B, fatal)

Theorem 3.2 ("Binomial ↔ grade correspondence") asserted that the cell-weight distribution `binomial(n, k)` of `V^⊗n` "matches the grade-k subspace dimensions of Cl(2n)", which the same theorem statement immediately gave as `binomial(2n, k)`. Two different binomial sequences indexed over different ranges (`k = 0..n` vs `k = 0..2n`); they are simply not equal, and the previous remark below the theorem admitted as much without producing a fix.

### Fix

Distinguish two cell decompositions of `V^⊗n`:

1. **Coarse cells** (the previously named "fine cells"): `2^n` total, each of dim `2^n`. Labeled by a 1-bit-per-slot sign in `{+, −}^n` recording which 2-dim summand `V_+ = F_5 e_2 ⊕ F_5 e_3` or `V_- = F_5 e_0 ⊕ F_5 e_4` each tensor factor lies in. Coarse-cell weights distribute as `binomial(n, k)`.

2. **Refined cells**: `4^n = 2^(2n)` total, each of dim `1`. Labeled by a 2-bit-per-slot pair recording which of the four basis lines `F_5 e_0, F_5 e_2, F_5 e_3, F_5 e_4` each slot represents. Refined-cell weights (Hamming weight of the `2n` structural bits) distribute as `binomial(2n, k)`.

The refined cells, not the coarse cells, are the right object to compare with `Cl(2n)`. Their multiplicity distribution `binomial(2n, k)` matches `dim Cl^(k)(2n) = binomial(2n, k)` exactly.

The new manuscript replaces Theorem 3.2 with **Theorem \ref{thm:refined}** stating exactly this, and adds **Remark \ref{rem:coarse}** explaining how the coarse-cell distribution is the "coarse shadow" of the refined one (sum over the inner 2-bit weight gives the outer 1-bit count).

The previous Theorem 4.1 (SU(5) at n=5) is demoted to **Remark \ref{rem:su5}** with the explicit acknowledgement that it is a binomial-coefficient identity, true for any binary-partition tensor structure on 5 factors, with no representation-theoretic content of `V` or `F_5` involved.

The previous Theorem 3.1 (total-dim match) is renamed **Theorem \ref{thm:total-dim}** and kept as an honest "arithmetic identity, forced by `dim V = 4 = 2^2`."

The paper title is changed from "A Dimensional Ladder…" to "Total-Dimension Match…with a Refined-Cell Grading" to honestly advertise content.

The paper now also includes an **explicit Scope statement** in §1 making clear that:

- Total-dim match is forced by `dim V = 4`. Theorem.
- Refined-cell grading matches `Cl(2n)` grade dimensions. Theorem.
- A structure-preserving map `V^⊗n → Cl(2n)` is **not** constructed in this paper. Open question (O1).
- An SU(5) action on `V^⊗5` is **not** constructed. Open question (O2).

---

## §2 — Independent verification of the corrected claim

Run from repo root:

```python
from math import comb
import sys
sys.path.insert(0, 'Gen13/targets/ck/brain/dirac')
from tig_dirac import refined_cell_distribution, refined_cell_distribution_enumerated, cell_binomial_distribution

for n in range(6):
    closed_form = refined_cell_distribution(n)         # closed-form binomial(2n, k)
    enumerated   = refined_cell_distribution_enumerated(n)  # direct enum over 4^n bit strings
    expected     = {k: comb(2*n, k) for k in range(2*n+1)}
    assert closed_form == enumerated == expected
    coarse       = cell_binomial_distribution(n) if n > 0 else {0: 1}
    assert sum(coarse.values()) == 2**n
    assert sum(closed_form.values()) == 4**n
```

Output (as of 2026-05-07):

```
n=0: refined sum=1=4^n=1, coarse sum=1=2^n=1, ok=True
   refined dist: {0: 1}
   coarse dist:  {0: 1}
n=1: refined sum=4=4^n=4, coarse sum=2=2^n=2, ok=True
   refined dist: {0: 1, 1: 2, 2: 1}
   coarse dist:  {0: 1, 1: 1}
n=2: refined sum=16=4^n=16, coarse sum=4=2^n=4, ok=True
   refined dist: {0: 1, 1: 4, 2: 6, 3: 4, 4: 1}
   coarse dist:  {0: 1, 1: 2, 2: 1}
n=3: refined sum=64=4^n=64, coarse sum=8=2^n=8, ok=True
   refined dist: {0: 1, 1: 6, 2: 15, 3: 20, 4: 15, 5: 6, 6: 1}
   coarse dist:  {0: 1, 1: 3, 2: 3, 3: 1}
n=4: refined sum=256=4^n=256, coarse sum=16=2^n=16, ok=True
   refined dist: {0: 1, 1: 8, 2: 28, 3: 56, 4: 70, 5: 56, 6: 28, 7: 8, 8: 1}
   coarse dist:  {0: 1, 1: 4, 2: 6, 3: 4, 4: 1}
n=5: refined sum=1024=4^n=1024, coarse sum=32=2^n=32, ok=True
   refined dist: {0: 1, 1: 10, 2: 45, 3: 120, 4: 210, 5: 252, 6: 210, 7: 120, 8: 45, 9: 10, 10: 1}
   coarse dist:  {0: 1, 1: 5, 2: 10, 3: 10, 4: 5, 5: 1}

ALL PASS: True
```

The refined-cell distribution at `n = 5` is `{0:1, 1:10, 2:45, 3:120, 4:210, 5:252, 6:210, 7:120, 8:45, 9:10, 10:1}`, which is exactly `binomial(10, k)`, matching the grade dimensions of `Cl(10)`. **Independent enumeration over `4^5 = 1024` 10-bit strings reproduces the closed-form result, providing a script-level cross-check.**

Two helpers added to `Gen13/targets/ck/brain/dirac/tig_dirac.py`:
- `refined_cell_distribution(n)` — closed form `binomial(2n, k)`.
- `refined_cell_distribution_enumerated(n)` — direct enumeration over `4^n` structural bit strings.

These ship with the manuscript verification.

---

## §3 — Other revisions needed

| Referee item | Disposition |
|---|---|
| **M1.** Theorem 3.1 (total-dim) trivial proof — fatal | **Kept** as Theorem \ref{thm:total-dim} with honest "this is forced by `dim V = 4`" framing in the §3 prose. Title and abstract restructured to advertise the dimensional match as one of two contributions, with the refined-cell theorem (M2 fix) carrying the structural content. |
| **M2.** Theorem 3.2 mis-stated — fatal | **Fixed.** Replaced with Theorem \ref{thm:refined} on refined cells. |
| **M3.** Theorem 4.1 (SU(5)) is binomial coincidence — fatal | **Demoted** to Remark \ref{rem:su5}. Honest framing: "binomial-coefficient identity, true for any binary-partition tensor structure on 5 factors." |
| **M4.** "Fine cells" need direct-sum-decomposition justification | **Fixed.** §2 ("The algebra V and its idempotent decomposition") now states both decompositions (coarse 2-summand, refined 4-summand) explicitly, with Remark \ref{rem:choice} on basis dependence. |
| **M5.** Verification script tests trivial arithmetic | Mostly **kept**, but the new `refined_cell_distribution_enumerated()` provides a non-trivial cross-check: enumerating over `4^n` bit strings and recovering the closed form is a real (if elementary) verification. |
| **M6.** Misleading introduction | **Fixed.** New introduction states the elementary nature plainly and explicitly carves out the open structural map question. |
| **M7.** Reference issues — Hestenes-Sobczyk, Bott, Georgi-Glashow | Hestenes-Sobczyk kept (used for `dim Cl(2n) = 2^(2n)` citation). Bott reference dropped (no Bott-periodicity content actually deployed). Georgi-Glashow dropped (no SU(5) content actually deployed; the binomial coincidence remark stands without it). |
| **m1.** Notation: signature of `Cl(2n)` | **Fixed.** Stated `Cl(2n) = Cl(2n, 0)` in §1 Notation. |
| **m4.** Bott periodicity remark trivial | **Fixed.** Renamed to "Periodicity" and demoted to open question (O3). |

The new acknowledgments paragraph credits the anonymous referee for catching the binomial-vs-grade mismatch.

---

## §4 — Updated PROVEN / COMPUTED / RHYME / OPEN

- **PROVEN:**
  - Total-dimension match `dim_F_5 V^⊗n = 4^n = 2^(2n) = dim_R Cl(2n)` for every `n ≥ 0`. (Theorem \ref{thm:total-dim}; one-line consequence of `dim V = 4`.)
  - Refined-cell binomial grading: `#{refined cells of weight k} = binomial(2n, k) = dim Cl^(k)(2n)` for every `n ≥ 0`. (Theorem \ref{thm:refined}; bookkeeping bijection on basis labels.)
- **COMPUTED:**
  - Verified at `n = 0, 1, 2, 3, 4, 5` by `refined_cell_distribution(n)` (closed form) and `refined_cell_distribution_enumerated(n)` (direct enum), both in `tig_dirac.py`.
  - Verified at `n = 5` that the coarse-cell weight distribution `(1, 5, 10, 10, 5, 1)` agrees with the SU(5) one-generation dimensions — a binomial identity.
- **STRUCTURAL RHYME (not derivation):**
  - At `n = 5`, the coarse-cell distribution `1 + 5 + 10 + 10 + 5 + 1 = 32` matches the SU(5) one-generation rep dimensions; this is a binomial-coefficient coincidence with no representation-theoretic content of `V` involved (Remark \ref{rem:su5}).
  - The 4-core `{V, H, Br, R} ⊂ Z/10Z` lifts to the 4-dim `F_5`-algebra `V` per `J23/J16`; the refined-cell decomposition coordinates the four basis lines, which are the four 4-core operators after `mod 5` projection.
- **OPEN:**
  - (O1) Structure-preserving map `V^⊗n ⊗_{F_5} K → Cl(2n; K)` for some common ring `K`.
  - (O2) Canonical `Spin(2n)` (or `F_5`-analogue) action on `V^⊗n`.
  - (O3) Genuine content in the periodicity comparison `Cl(n+8) ≅ Cl(n) ⊗ Cl(8)` vs `V^⊗(n+8) = V^⊗n ⊗ V^⊗8` beyond the trivial dimensional consequence.

---

## §5 — Estimated revision time

- **Manuscript rewrite:** **DONE** (this turn). New `manuscript.tex` written with corrected Theorem 3.2 → Theorem \ref{thm:refined}, demoted SU(5) claim, restructured §3 + §4, new open-questions section. ~2 h equivalent.
- **Verification script update:** **DONE** (this turn). Added `refined_cell_distribution()` and `refined_cell_distribution_enumerated()` to `tig_dirac.py`. ~30 min equivalent.
- **Cover letter update:** ~30 min — brief rewrite to lead with the refined-cell construction and explicitly thank the referee.
- **Final read-through and `test_tig_dirac.py` test additions** (T16, T17 for refined-cell distribution): ~1 h.

**Total residual to submission-ready:** ~1.5 h human time after this turn.

The paper is now an honest two-result note: a forced arithmetic identity (Theorem \ref{thm:total-dim}) and a binomial-grading bijection between refined cells and Clifford grades (Theorem \ref{thm:refined}), with explicit acknowledgement that no structure-preserving map between the algebras has been constructed and that the SU(5) coincidence is a binomial identity.

This is below *Linear Algebra and Its Applications* tier for a stand-alone paper; the natural disposition is either:
- (a) **Resubmit to LAA** as a short note (~5 pages) honestly framed as a dimensional/cell-grading observation supporting the companion `J23` paper, OR
- (b) **Fold into J23** as a §6 ("Tensor tower and Clifford grades"), making `J23` the main vehicle and demoting `J17` to an internal section.

The Save Plan recommends (a) for the September-11 calendar; if the referee re-reviews and still rejects on substance grounds, fall back to (b).
