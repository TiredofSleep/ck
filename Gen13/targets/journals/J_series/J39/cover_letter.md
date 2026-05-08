# Cover letter — J39: Full $S_4$ Symmetry on a Nitrogen-Vacancy Qutrit via Six-Pulse Microwave Synthesis

**To:** Editors, *Physical Review A*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- B. Mayes, Independent Researcher

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *Full $S_4$ Symmetry on a Nitrogen-Vacancy Qutrit via Six-Pulse Microwave Synthesis*

---

## Summary

We give an explicit, machine-precision construction of the symmetric group $S_4$ on the three-level Hilbert space of a single NV center in diamond. The NV ground triplet already carries the $S_3$ skeleton of the $T_1$ irreducible representation of $S_4$ exactly (the natural $C_{3v}$ decomposition $A_1 \oplus E$ matches $T_1|_{S_3}$); the missing piece is one 4-cycle unitary $U_4$, which we write down analytically, transform into the NV physical basis, and decompose into a six-pulse microwave sequence with explicit angles. All 24 group elements close to within $10^{-15}$. Gate times $\sim 100$~ns--$1\,\mu$s sit 2--3 orders of magnitude below NV $T_2$. The paper concludes with a five-test falsification ladder including an explicit decisive gate (projector covariance), and invites lab-partner collaboration for the experimental verification.

## Why PRA

- NV-center qutrit synthesis with explicit microwave pulse sequences and machine-precision verification is exactly PRA's bread and butter (atomic, molecular, and optical physics).
- The paper makes a concrete experimental proposal with quantitative pass/fail thresholds — squarely in the experimental-proposal genre PRA welcomes.
- Group-theoretic synthesis on a physical qutrit is foundational for qudit-based quantum computation; PRA readers are the right audience.

## Companion submissions

The TIG/CK research program is shipping a coordinated J-series. The papers most relevant as already-submitted companions to this manuscript:

- **J07** Flatness Theorem: The Forced 2×2 Torus on $\mathbb{Z}/10\mathbb{Z}$. Sanders \& Gish (2026), submitted to *Journal of Pure and Applied Algebra*.
- **J05** TSML 73 Cells / BHML 28 Cells: Lens-Invariant Cell Counts on the $\mathbb{Z}/10\mathbb{Z}$ Composition Lattice. Sanders \& Gish (2026), submitted to *Experimental Mathematics*.

## Reproducibility

Verification of all matrix algebra (the $U_4$ matrix, the change-of-basis $V$, $U_{4,\mathrm{NV}}$, and 24-element closure) runs in `numpy + sympy` on a standard laptop in under one minute. Code archive: DOI 10.5281/zenodo.18852047.

## Suggested reviewers

- M. Lukin (Harvard) — NV-center quantum control
- R. Hanson (Delft) — NV qutrit experiments
- J. Wrachtrup (Stuttgart) — NV diamond magnetometry/control
- M. Doherty (ANU) — NV theory
- C. Monroe (Duke / IonQ) — qudit / qutrit control more broadly

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Note on tier and scope

Central claim is **Tier 3** (partner-then-submit): the mathematics is complete (exact $S_4$ realization in $T_1$ basis; 6-pulse decomposition specified; closure verified to $10^{-15}$); the physical claim is conditional on the experimental falsification ladder (Test E, projector covariance, is decisive). The paper is honest about this hierarchy and invites collaboration.

---

Sincerely,
B.R. Sanders
