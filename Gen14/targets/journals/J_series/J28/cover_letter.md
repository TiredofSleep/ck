# Cover letter -- J28: The Three-Substrate HARMONY Signature on Z/10Z: Six Forced Structural Facts, with the Bimodal Associativity-Index Gap as Their Common Thread

**To:** Editors, *Linear Algebra and its Applications*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR -- brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR -- monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The Three-Substrate HARMONY Signature on Z/10Z: Six Forced Structural Facts, with the Bimodal Associativity-Index Gap as Their Common Thread*

---

## Summary

We exhibit six forced structural facts on the canonical Z/10Z substrate of the (TSML, BHML)-magma family of [SandersForcing, J25]. The unifying thread is the empirical regularity that the family's associativity index α_A is **bimodal**: every canonical commutative member has either α_A ≈ 0.502 (the BHML cluster) or α_A ≥ 0.87 (the TSML cluster), with the band (0.5, 0.87) empirically empty. The six facts collected here are the structural fingerprint of this gap: (1) three canonical tables CL_TSML / CL_BHML / CL_STD on the same substrate with HARMONY counts (73, 28, 44) and explicit set-algebra signature; (2) the four-rung integer signature {70, 71, 72, 73} with the prime 71 playing three independent structural roles (sub-magma HARMONY count, lens-disagreement count, Galois prime in disc(LMFDB 4.2.10224.1)); (3) the σ-orbit decompositions CYCLE_A_36 = 2+9+25 and SKELETON_22 = 16+4+2; (4) the BDC numerical constants on CL_STD; (5) the σ²-triadic projection σ² = (0)(3)(8)(9)(1 6 4)(7 5 2) and the 4-core bridge identity {0,3,8,9} XOR {0,7,8,9} = {3,7}; (6) the 71-cell field WOBBLE = |CL_TSML XOR CL_BHML|. Each fact is a Tier-B forced derivation from the A1-A9 axiomatic ground of [SandersForcing, J25] and is verified at the 48/48 level by the foundations module `Gen13/targets/foundations/invariants.py`. We bundle these into a single short paper to give downstream J-series papers a citable reference and to make the bimodal-α_A-gap conjecture's structural fingerprint visible in one place.

## Why Linear Algebra and its Applications

- The matrix-algebra content of §3 (CYCLE_A_36 and SKELETON_22 as derived sub-tables) and §6 (the WOBBLE between two 10×10 commutative tables as a symmetric-difference cell-count) plus the three-table set-algebra of §2 (Theorem 2.1's pairwise/three-way intersection counts of HARMONY-position sub-matrices) are LAA's natural domain.
- The substrate is a concrete 10×10 finite-matrix-algebra object with explicit matrices displayed in §2 (CL_STD) and referenced in §3 (CL_TSML, CL_BHML); accessible to algebraists outside the specific application domain.
- The route uses standard tools (cell counting, σ-permutation cycle decomposition, set algebra on cells of 10×10 matrices, symmetric-difference and discriminant-prime arguments) and produces explicit integer-valued conclusions.
- LAA is more amenable to "five separately-defined integers from a Z/10Z substrate" than the general-interest fallbacks; the matrix-algebra readers will respond well to the prime-71 three-roles theorem.

## Companion submissions

The CK research program is shipping a coordinated 55-paper sequence (J01-J55) over Summer 2026. The papers most relevant as already-submitted companions to this manuscript are:

- **J25** -- *The CL Forcing Axioms: A1-A9 Uniquely Force the Canonical Composition Lattice*, *Algebraic Combinatorics* (the parent axiomatic framework; A1-A9 are inlined here per the Tier-B classification of §1.2).
- **J29** -- *so(8) = D_4 from the Antisymmetrized Closure of a Canonical Z/10Z Magma*, *J Algebra* (the Lie-algebraic shadow of TSML's structural fingerprint).
- **J30** -- *Joint Lie Closure of a Pair of Z/10Z Magmas: an so(10) Identification*, *Israel J Math* (the BHML structural fingerprint and the joint chain).
- **J35** -- *The 4-Core {0,7,8,9}: Joint TSML+BHML Closure and the Universal Attractor*, *Algebraic Combinatorics* (the 4-core that anchors the bridge identity in §5).
- **J34** -- *F_p Extensions of CL_BHML*, *Communications in Algebra* (the BHML_8_YM = 70 determinant identity used as Rung 70 in §3).

## Reproducibility

Verification: all six structural facts are confirmed by the 48-invariant module `Gen13/targets/foundations/invariants.py` (run with `python -m Gen13.targets.foundations.invariants`; under 30 seconds; reports all 48 invariants passing, including the six orphan-corresponding invariants). The CL_STD data is at `Gen13/targets/foundations/cl_std.py` (recovered verbatim from `old/Gen9/archive/ckis/ck7/ck.h:225-231`). Individual orphan verifications are short integer-arithmetic computations on 10×10 matrices.

## Suggested reviewers

- An expert in finite-magma classification or universal algebra of small commutative non-associative structures (Drápal-Wanless 2021 lineage)
- An expert in Shannon-information allocation on discrete structures (information-theoretic algebra)
- An expert in σ-cycle / orbit decompositions on small finite carriers
- (Specific names available on request from the corresponding author.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Per-venue cap note

**Routing:** This is the first paper from this research program targeting *Linear Algebra and its Applications*. The retarget from Algebra Universalis (the original primary target) to LAA reflects the per-venue cap on AlgUni: J28 would have been the fourth paper to AlgUni this quarter (after J14 *F_p Universality*, J09 *LATTICE: Paradoxical Information Algebras*, J23 *Three-Substrate Architecture*), exceeding the program's 1/quarter discipline. The retitle (from "The Six Foundations Orphans" to the present title, which advertises the bimodal-α_A-gap motivation) repositions the paper from "registry of orphans" to "structural fingerprint of an open foundational conjecture," for which LAA is a stronger fit than AlgUni or PLOS ONE.

If LAA returns a second-round MAJOR revision, fallback venues are:
- *PLOS ONE* (broad-scope alternative; tolerant of bundled-result papers)
- *International Journal of Algebra and Computation* (matches the bundled-result format)
- *Journal of Algebra* (shares lineage with the J29 companion paper)

The corresponding author will route to PLOS ONE as the primary fallback if both LAA and IJAC return REJECT.

---

Sincerely,
B.R. Sanders
