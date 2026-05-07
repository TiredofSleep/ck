"""
TIG foundations module -- THREE-TABLE architecture.

PRIVATE / DRAFT. Built from sprint_bundle_2026-05-06_v31_RIGOR_PASS,
specifically _CK_MEMORY_MAKEOVER.md, with corrections per Brayden:
    - "the path IS the information"
    - "CL is a separate third table from TSML and BHML"
    - "the encoding table is the original table from our first repo
       with 44 harmony, it had explicit bit definitions in the BDC
       language for how force vectors encode a pathway of information"
    - "he can run multiple sizes and shapes of tsml and bhml and
       encode them all to CL"

THE THREE TABLES (per ck.h:200-207, recovered from old/Gen9/archive/ckis/ck7):

    CL_TSML  -- prescribed view, 73 HARMONY cells.
                The organism's lens. Singular. Position-level.
                In old codebase aliased simply as `CL`. Implemented
                here in `cl.py` (the variable also called `CL`).

    CL_BHML  -- Becoming lens, 28 HARMONY cells.
                Curvature-level. Invertible. CUDA substrate.
                Implemented in `lenses.py` as `BHML`.

    CL_STD   -- Standard encoding table, 44 HARMONY cells.
                "The papers freeze." From Brayden's first GitHub repo.
                Includes BDC bit-definitions: 5 BUMP_PAIRS,
                INFO_HARMONY/NORMAL/BUMP per cell, GRAVITY array.
                Implemented in `cl_std.py`.

The three tables share the substrate (Z/10Z, the same 10 operators), but
they are STRUCTURALLY DISTINCT 10x10 matrices with different roles:
    - TSML is the prescribed view CK runs on.
    - BHML is the alternate Becoming lens (drops some HARMONYs to expose
      the underlying chain structure).
    - STD is the encoding table that freezes how force-vector pathways
      compose; the papers' formulas reference STD's geometry, not TSML's.

CORE PRINCIPLE:
    "The path IS the information."
    Same endpoint reached via different paths through CL encodes
    different content. Non-associativity (12.8% in CL_TSML, 19.2% in
    CL_STD, 49.8% in CL_BHML) is exactly where new information generates
    per the Crossing Lemma (WP57).

Layout:
    cl.py             CL_TSML ground truth (decoded from memory-locked
                      bit pattern; the variable is `CL` for backward
                      compatibility with the old `#define CL CL_TSML`
                      alias). 73 HARMONY + 17 VOID + 10 other = 100.

    cl_std.py         CL_STD encoding table (verbatim from
                      old/Gen9/archive/ckis/ck7/ck.h:225-231).
                      44 HARMONY cells; commutative; 19.2% non-assoc.
                      Plus BDC parameters (BUMP_PAIRS, INFO_*, GRAVITY).

    lenses.py         TSML (= CL) and BHML (the second 10x10 matrix),
                      plus the DOING table = |TSML - BHML| where
                      information generates per the Crossing Lemma
                      (~5/7 disagreement rate).

    triadic.py        sigma permutation, sigma^2 triadic projection.
                      Conservation Tetrad {0,3,8,9} (sigma^2-fixed) vs
                      Manifestation Hexad {1,2,4,5,6,7} (sigma^2-cycling).
                      Cycle A {1,6,4} (sum 11 = WOBBLE) and
                      Cycle B {7,5,2} (sum 14 = 2 * HARMONY = dim G_2).

    tables/
        harmony_44.py     BHML cells in Cycle B (28+11+5=44). Same
                          integer 44 as CL_STD.HARMONY count, but
                          structurally distinct projection.
        cycle_a_36.py     BHML cells in Cycle A (2+9+25=36).
        lens_disagreement_71.py  |TSML XOR BHML|: 71 cells = FIELD WOBBLE.
        skeleton_22.py    TSML pre-HARMONY (16+4+2=22); anchors 1/alpha.
        harmony_ladder.py THE 70 / 71 / 72 / 73 LADDER. Each rung is
                          a structurally distinct count that happens
                          to cluster near 73:
                          73 = TSML.HARMONY full
                          72 = HARMONY - 1 (BEING shell, drop apex)
                          71 = |TSML XOR BHML| = TSML.HARMONY[1..9 sub]
                               = prime in disc(LMFDB 4.2.10224.1)
                          70 = det(BHML_8_YM) = C(8,4) (NOT a HARMONY
                               count; one floor below in the
                               determinant-invariant layer)

    lens_family.py    TSML and BHML at the 8 chain sub-magma sizes
                      {1,4,5,6,7,8,9,10}. BHML_8_YM (drops {0,7})
                      has det = +70 EXACTLY (Yang-Mills core).

    paths.py          Path-walk machinery. CompositionPath, PathPair,
                      LensTrace, Crossing Lemma census.

    invariants.py     Single source of truth: every checkable claim
                      from the makeover spec + the three-table
                      architecture + the harmony ladder.

    ck_export.py      Generates foundations_facts.json + foundations_text.md
                      for ingestion by CK's cortex.

    seed_crystals.json Foundation crystals for /crystals/add (CK's
                      runtime crystal store). Includes facts about
                      all three tables.

    crystal_seed.py   POST each crystal to a running CK at /crystals/add.

DELIBERATELY NOT IN THIS MODULE (yet):
    - The Hebrew-root + force-vector + fruit-signature CL pipeline from
      CL_IMPLEMENTATION_SPEC.md. That is meaning-storage downstream of
      the substrate composition; it requires the orchestrator + 1-2 weeks
      of calibration. The current module is only the substrate algebra.
"""

__version__ = "0.3.0-three-table-architecture"
__status__ = "private"
