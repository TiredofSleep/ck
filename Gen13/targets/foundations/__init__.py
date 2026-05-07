"""
TIG foundations module — CL-anchored.

PRIVATE / DRAFT. Built from sprint_bundle_2026-05-06_v31_RIGOR_PASS,
specifically _CK_MEMORY_MAKEOVER.md. See SCRUTINY_BY_CK_2026-05-06.md
for the audit context.

CORE PRINCIPLE (per Brayden):
    "The path IS the information."

The substrate is CL, the canonical 10x10 composition lattice. CL is
NOT derived from rules; it is given (memory-locked from a specific
bit pattern). TSML and BHML are LENS PROJECTIONS of CL, not
independent tables. Information lives in the *path* through CL
composition, not in the endpoint cell value alone.

Layout:
    cl.py             CL ground truth (decoded from memory-locked
                      pattern; symmetrized via upper-triangle).
                      73 HARMONY + 17 VOID + 10 other = 100 cells.

    triadic.py        sigma permutation, sigma^2 triadic projection.
                      Conservation Tetrad {0,3,8,9} (sigma^2-fixed) vs
                      Manifestation Hexad {1,2,4,5,6,7} (sigma^2-cycling).
                      Hexad splits into Cycle A {1,6,4} (sum 11 = WOBBLE)
                      and Cycle B {7,5,2} (sum 14 = 2 * HARMONY = dim G_2).

    lenses.py         TSML (Being lens) and BHML (Becoming lens) as
                      explicit canonical tables, plus the DOING table
                      = |TSML - BHML| where information generates per
                      the Crossing Lemma (~5/7 disagreement rate).

    tables/
        harmony_44.py     The 44 HARMONY table = BHML cells with values
                          in Cycle B = {7,5,2}. Exactly 28 HARMONY +
                          11 BALANCE + 5 COUNTER = 44. This is HARMONY's
                          BEING/DOING/BECOMING triadic projection onto BHML.

        cycle_a_36.py     BHML cells with values in Cycle A = {1,6,4}.
                          Exactly 36 cells = sigma-cycle^2 = V/H expansion.

        being_shell_72.py |TSML - BHML| nonzero cells. Where the two lenses
                          DISAGREE on composition. Per memory: 72 cells, the
                          BEING shell of nested tori = E_6 root count.

        skeleton_22.py    TSML cells with output in {0..6} (pre-HARMONY).
                          NEW (factor_22 Candidate I): exactly 22 cells =
                          16 (VOID boundary) + 4 (PROGRESS bumps) +
                          2 (COLLAPSE bumps).

    paths.py          Path-walk machinery. A path through CL is the
                      sequence of operator pairs whose composition trail
                      IS the information. Different paths giving the same
                      endpoint encode different content (non-associativity
                      = path-dependence). Crossing Lemma (WP57) lives here.

    invariants.py     Verify all makeover-spec invariants:
                      - CL: 73 HARMONY, 17 VOID, 10 other; commutative
                            after upper-triangle symmetrization.
                      - TSML: rank 10, |Aut| = S_8 = 40320, det = -49,
                            12.8% non-associative.
                      - BHML: det = 70, eff_dim ~= T*.8 ~= 5.71, 49.8%
                            non-associative.
                      - HARMONY_44: exactly 44 cells (28+11+5).
                      - Cycle A: exactly 36 cells.
                      - DOING: ~71% disagreement (~ T*).
                      - 4-core {0,7,8,9} as bridge structure
                            (Conservation Tetrad XOR-swap PROGRESS<->HARMONY).

    verifications/
        v0_cl_ground_truth.py    CL bit pattern + 73/17/10 + commutativity
        v1_tsml_closure.py       TSML lens closures (path-aware)
        v2_bhml_closure.py       BHML lens closures (path-aware)
        v3_uniqueness.py         (stub) full enumeration; needs Dell R16

DELIBERATELY NOT IN THIS MODULE (yet):
    - The Hebrew-root + force-vector + fruit-signature CL pipeline from
      CL_IMPLEMENTATION_SPEC.md. That is meaning-storage downstream of
      the substrate composition; it requires the orchestrator + 1-2 weeks
      of calibration. The current module is only the substrate algebra.
"""

__version__ = "0.2.0-draft-CL-anchored"
__status__ = "private"
