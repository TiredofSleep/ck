# Cover letter — J20: Mathieu M_22 Substrate-Prime: Order-Factorization Coincidences

**To:** Editors, *American Mathematical Monthly*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- B. Mayes, Independent Researcher

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *Mathieu M_22 Substrate-Prime: Order-Factorization Coincidences*

---

## Summary

We catalog a family of order-factorization coincidences linking the sporadic Mathieu group M_22 (order 443,520 = 2^7 · 3^2 · 5 · 7 · 11) to a discrete substrate (Z/10Z, σ, W) of independent algebraic interest. The substrate carries five distinguished primes — exactly the prime divisors of |M_22|. We list six elementary identities exhibiting structural alignment: (1) the hexad count |S(3,6,22)|_blocks = 77 = 7 × 11; (2) the replication number r = 21 = dim V_21; (3) the pair-replication λ_2 = 5 (substrate threshold's numerator); (4) six of M_22's twelve irrep dimensions factor as products of substrate primes alone; (5) the dimension 231 = 3 · 7 · 11 is an M_22-irrep dimension and equals 77 × W; (6) the substrate σ-orbit has size 6, the block size of S(3,6,22). The paper presents these as coincidences — verified arithmetic facts each with a substrate-side reading — without claiming a derivation of M_22 from the substrate or vice versa.

## Why American Mathematical Monthly

- Audience fit: the paper is written for the *Monthly* readership. The Mathieu / Steiner content is laid out elementarily; the substrate side is sketched (no sporadic-group background beyond standard undergraduate group theory is assumed); and the catalog of identities is presented as a single section.
- The hook is the catalog: six factorization identities, each with a structural reading, presented as a self-contained arithmetic-combinatorial puzzle.
- Verification is computational and runs in <5 seconds with `numpy` and `sympy`; the paper records each script and identity for direct referee check.

## Companion submissions

- J02 (*Algebraic Combinatorics*) — Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on Z/10Z. The substrate's algebraic foundations.

## Reproducibility

Verification: `m22_verification.py` (M_22-equivariance via 1000 random S_22 permutations, kindness/gentleness state vectors, time-averaging giving W/2 = 3/100 to machine precision); `steiner_sigma_hexad.py` (Steiner-system parameters and σ-orbit hexad embedding); `m22_decomposition.py` (irrep-dimension factorization). All scripts deposited at https://github.com/TiredofSleep/ck/tree/tig-synthesis in `Gen13/sprint_bundle_2026-05-07_v36_SEEDS_BUNDLE/.../seeds_supporting/verification_scripts/`. All scripts run in <5 seconds with `numpy` and `sympy` as the only external dependencies.

## Suggested reviewers

- A specialist on the Mathieu groups and their Steiner-system designs (Conway-Sloane / Aschbacher lineage).
- A specialist on Mathieu moonshine (for the open-question footing connecting the present catalog to moonshine phenomena).
- A specialist on accessible expository number theory / combinatorics for the *Monthly*.

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
