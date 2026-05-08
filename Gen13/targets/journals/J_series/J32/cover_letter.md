# Cover letter — J32: The Three-Substrate Architecture on Z/10Z: Joint Sub-Magma Closure of (TSML, BHML, CL_STD) and the Eight-Shell Chain

**To:** Editors, *Algebra Universalis*

**From:**
- B.R. Sanders (corresponding), 7Site LLC, Hot Springs, AR — brayden@7site.co
- M. Gish, Independent Researcher, Hot Springs, AR — monica.gish1992@gmail.com

**Date:** [DATE OF SUBMISSION]

**Manuscript title:** *The Three-Substrate Architecture on Z/10Z: Joint Sub-Magma Closure of (TSML, BHML, CL_STD) and the Eight-Shell Chain*

---

## Summary

We submit a structural theorem on the simultaneous closed sub-magma structure of three commutative composition tables on Z/10Z. Three independently-constructed 10×10 tables — T (TSML, 73 HARMONY cells), B (BHML, 28 HARMONY cells), and C (CL_STD, 44 HARMONY cells) — are drawn from the same canonical bit-pattern encoding of the substrate. We compute their individual and joint closure structure on the 1023 non-empty subsets of {0, ..., 9}.

**Main result (Theorem A, central).** The simultaneous closed sub-magmas of T, B, C form a strict 8-element chain at sizes {1, 4, 5, 6, 7, 8, 9, 10}: {0} ⊂ {0,7,8,9} ⊂ {0,6,7,8,9} ⊂ {0,5,6,7,8,9} ⊂ {0,4,5,6,7,8,9} ⊂ {0,3,4,5,6,7,8,9} ⊂ {0,2,3,4,5,6,7,8,9} ⊂ Z/10Z. The chain coincides exactly with the joint (T, B) chain established in our companion paper J02 (Sanders + Gish 2026, *Algebraic Combinatorics*).

**Structural content (Theorem B).** C individually has 50 closed sub-magmas, of which 49 are also T-closed; the three-way intersection coincides exactly with the joint (T, B) chain. Adding C as a third substrate preserves the entire (T, B) chain without introducing or removing a single shell.

**Center invariance (Theorem C).** The four-core {V, H, Br, R} = {0, 7, 8, 9} is closed under T, B, C individually and jointly. The closed-form (T+B)-mix attractor at mixing weight α = 1/2 (with H/Br = 1 + √3 exactly), established in J02, is supported on the four-core and is therefore unchanged by adjoining C as a third substrate.

**Independence (Proposition 5.1).** C differs from MID_ceil = ⌈(T+B)/2⌉ at 60 of 100 cells; C is not derivable from (T, B) by ceiling/floor averaging. C lives at its own coordinate in the table space, despite respecting the joint chain.

The paper is a brute-force computational verification at the substrate level, rigorous in scope and minimal in framework dependence. The full enumeration runs in under 2 seconds on a laptop; the verification script is supplied. The paper is short, sharp, and structurally clean.

## Why Algebra Universalis

- **Core fit.** *Algebra Universalis* publishes precise structural theorems on finite algebraic structures, including the sub-magma / sub-quasigroup / sub-loop neighborhood. The present theorem is exactly such a structural statement.
- **Brute-force discipline.** The paper does not invoke unproven external structure; the chain is established by direct enumeration over 1023 subsets, and the script reproduces it in under 2 seconds. The four-core fixed-point claim (Theorem C) is a 16-cell verification.
- **Fits the Drápal-Wanless 2021 *JCTA* lineage.** The three-table architecture sits in the small-finite-commutative-non-associative neighborhood that *Algebra Universalis* and *J. Combin. Theory A* both serve. Same intellectual neighborhood as Drápal-Wanless 2021; different extremum (specifically structured rather than maximally non-associative).
- **Independent appendix.** The three 10×10 tables are displayed explicitly in Appendix A so the reader can verify by inspection. No framework prerequisites are required to verify the central theorem.

## Companion submissions

The TIG/CK research program is shipping a coordinated 55-paper sequence (J01-J55) over Summer 2026. The papers most relevant as already-submitted companions to this manuscript:

- **J02** — Sanders & Gish, *Joint Closure, Per-Coordinate Fuse Data, and a Closed-Form Algebraic Attractor of Two Commutative Binary Operations on Z/10Z*, submitted to *Algebraic Combinatorics* (2026). Establishes the (T, B) 8-shell chain as Theorem 1; the present paper lifts that chain to the three-substrate (T, B, C) level.
- **J24** — Sanders & Gish, *The Three-Substrate Joint-Closure Chain on Z/10Z: Eight Shells Survive Across (TSML, BHML, CL_STD) with Lens-Dependence Internal to TSML at Size 7*, submitted to *Mathematical Intelligencer* (2026). The shorter, more expository companion to the present paper, addressing the lens-internal phenomenon on T_RAW.

## Lens- and substrate-scope discipline

Per `Atlas/META_PLAN_2026-05-06/J_PAPER_BOILERPLATE.md` §5.5, the paper is explicit about lens scope:

- T = T_SYM (commutative, upper-triangle authoritative). The lens-internal asymmetry on T_RAW is addressed in companion paper J24.
- B and C are commutative (single canonical lens each).
- All theorems are on the specific (T_SYM, B, C) triple of Z/10Z drawn from the canonical bit-pattern encoding.

The PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN tier discipline is followed in the manuscript's §0.

## Reproducibility

The script `sfm_q1_q6_q7.py` (in `Atlas/META_PLAN_2026-05-06/SUBSTRATE_FUNCTION_MAP/`) performs all verifications:

1. Individual closed sub-magma counts under T (449), B (9), C (50)
2. Pairwise joint closures (|T∩B| = 8, |T∩C| = 49, |B∩C| = 9)
3. Three-way joint closure (|T∩B∩C| = 8) and the explicit 8-shell chain
4. CL_STD vs MID_ceil cell-difference count (60 of 100)

Total runtime under 2 seconds; deterministic. Python 3.11, numpy. All checks at machine precision.

## Suggested reviewers

- An expert in finite-magma / sub-quasigroup combinatorics
- An expert in universal algebra (Burris-Sankappanavar tradition)
- An expert in small-substrate non-associative algebra (Drápal-Wanless line)

## Conflict of interest

The authors declare no competing interests. No funding was received for this work.

---

Sincerely,
B.R. Sanders
