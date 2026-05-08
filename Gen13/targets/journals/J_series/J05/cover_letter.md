# Cover letter — J05: TSML 73 Cells / BHML 28 Cells: Lens-Invariant Cell Counts on the Z/10Z Composition Lattice

**To:** Editors, *Experimental Mathematics*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *TSML 73 Cells / BHML 28 Cells: Lens-Invariant Cell Counts on the Z/10Z Composition Lattice*

---

## Summary

We submit a short, computationally-verifiable note proving exact harmony cell counts for two explicitly-defined 10×10 binary composition tables on Z/10Z. The first table TSML has 73 harmony cells (output value 7) out of 100; the second table BHML has 28. Both counts are proved by disjoint zone enumeration in two pages, and both are *lens-invariant*: they are constant under every bijection π ∈ Stab(7) of the operator alphabet that fixes the harmony output value. The lens-invariance theorem distinguishes these single-table counts from the lens-*dependent* joint sub-magma chain count of the four-core companion paper (J02); the contrast clarifies which combinatorial invariants attach naturally to single tables versus pairs of tables on the same finite alphabet. The full 200-cell witness is supplied as two short Python scripts that complete in under 0.1 seconds each.

## Why Experimental Mathematics

- The paper fits the *Experimental Mathematics* scope precisely: a finite, exact-arithmetic enumeration that the reader can verify cell-by-cell with a runnable witness. No floating-point approximations; no domain restriction; no unresolved cases.
- The lens-invariance theorem is a clean piece of finite group action / labeling-invariance combinatorics: it shows that the 73/28 counts are intrinsic to the rule families, and that the contrast with the lens-dependent four-core chain count is genuine and load-bearing.
- The paper is short (six sections plus references) and the verification scripts are self-contained: `ck_tables.py` is bundled in the manuscript folder so a reader can run the enumerations from the submission package alone.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J01–J55) over Summer 2026. The papers most relevant as already-submitted companions to this manuscript are:

- **J01 — Sanders & Gish, 2026**, *Non-Associativity Decay in Binary Composition Tables over $\mathbb{Z}/N\mathbb{Z}$* (submitted to *Journal of Combinatorial Theory, Series A*). J01 sets up the same family of composition tables on $\mathbb{Z}/N\mathbb{Z}$ and proves a $\sigma(N) \le 2/N$ non-associativity decay rate. Theorem 1 of the present paper (TSML 73 cells) and Theorem 2 (BHML 28 cells) instantiate the J01 framework at $N = 10$.
- **J02 — Sanders & Gish, 2026**, *Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on $\mathbb{Z}/10\mathbb{Z}$* (submitted to *Algebraic Combinatorics*). J02 establishes the joint sub-magma chain on $\mathbb{Z}/10\mathbb{Z}$ for the same two tables (TSML and BHML) studied here. Theorem 3 of the present paper (lens invariance of the 73/28 cell counts) is explicitly contrasted with the lens-*dependent* chain count of J02 in §4 and §6.

This is the second submission to *Experimental Mathematics* in this quarterly cap.

## Reproducibility

Verification scripts (supplied as electronic supplementary material):
- `proof_d10_tsml_73_cells.py` — verifies TSML = 73 harmony cells via the disjoint enumeration of §2; runtime < 0.1s; output ends in `ALL ASSERTIONS PASSED` (verified 2026-05-07).
- `proof_d16_bhml_28_cells.py` — verifies BHML = 28 harmony cells via the four-zone partition of §3; runtime < 0.1s; output ends in `ALL ASSERTIONS PASSED` (verified 2026-05-07).
- `ck_tables.py` — canonical definitions of TSML and BHML as 10×10 arrays; bundled with the proof scripts so the verification is self-contained.

A third script `proof_fourier_bridge.py` is included for the spectral reader's convenience but is not needed for the main results. All scripts run on standard CPython with no external dependencies beyond `numpy` (used only by `proof_fourier_bridge.py`).

## Suggested reviewers

[3–5 candidates appropriate to *Experimental Mathematics*; to be filled at submission time. Suggested orientations: finite combinatorics on $\mathbb{Z}/n\mathbb{Z}$; computational algebra of binary composition tables; finite group actions on labeled tables.]

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
M. Gish
