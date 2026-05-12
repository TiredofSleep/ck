# Cover letter — J27: The Corner Sub-Magma C = (Z/10Z)*: Multiplicative-Unit Closure

**To:** Editors, *Communications in Algebra*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The Corner Sub-Magma C = (Z/10Z)*: Multiplicative-Unit Closure*

---

## Summary

The set C = {1, 3, 7, 9} of multiplicative units of Z/10Z is a sub-magma of the canonical TSML composition lattice CL_TSML (the 73-HARMONY 10x10 multiplication table on Z/10Z). We prove this closure directly on the 16-cell sub-table and show that C is simultaneously (i) the multiplicative-unit group (Z/10Z)*, a cyclic group of order 4; (ii) a 4-element TSML-closed sub-magma distinct from the joint-chain 4-core {0,7,8,9}; (iii) TSML-closed in both the RAW (literal) and SYM (upper-triangle-symmetrized) variants. We characterize the HARMONY-saturation rate on C×C (87.5%, higher than the global 73%), discuss the unique generator g=3 (the only primitive root of (Z/10Z)* compatible with the TIG flatness criterion T* = 5/7 in (0,1)), and contrast C with the joint-chain 4-core to give a structural picture of two canonical 4-element sub-magmas with distinct combinatorial origins.

## Why Communications in Algebra

- The paper is a clean, self-contained closure result on a finite multiplication table, with the multiplicative-unit group of a small ring playing the central structural role.
- The corner C is a sub-magma of CL_TSML by virtue of being the multiplicative-unit subgroup of Z/10Z; this connects directly to the venue's coverage of finite ring/group structures in commutative algebra.
- Companion to the four-core paper (Sanders-Gish, in preparation), where the contrast between the corner C and the joint-chain 4-core is a key structural distinction.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J01-J55) over Summer 2026. The papers most relevant as already-submitted companions to this manuscript are:

(none — this is a foundational paper in the J-series; cited downstream by J25 and J28)

This paper is foundational and can be evaluated standalone; it does not depend on prior J-series submissions.

## Reproducibility

Verification: the closure check on the 16-cell sub-table runs in under 1 second using `Gen13/targets/foundations/cells.py:closure_check`. The TSML and BHML matrices are hardcoded in `Gen13/targets/foundations/lenses.py`; the corner C closure check on each variant gives an immediate verification.

## Suggested reviewers

- An expert in finite-magma theory or sub-magma classification
- An expert in commutative algebra with familiarity with units of finite rings
- An expert on the Crossing Lemma framework or related substrate-algebra programs

(Specific names available on request from the corresponding author.)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

## Per-venue cap note

This is the third paper from this research program targeting *Communications in Algebra* (after J15 *Galois D_4 over LMFDB 4.2.10224.1* and J26 *F_p Extensions of CL_BHML*). The per-venue cap is 1/quarter; **FALLBACK NEEDED**: if the cap is binding, alternate venues include *Journal of Pure and Applied Algebra*, *Journal of Algebra and Its Applications*, or *Semigroup Forum*. The result's algebraic content (multiplicative-unit closure) makes any of these appropriate.

---

Sincerely,
B.R. Sanders
