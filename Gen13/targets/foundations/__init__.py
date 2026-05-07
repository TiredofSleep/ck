"""
TIG foundations module.

STATUS: DRAFT, PRIVATE. Built from sprint_bundle_2026-05-06_v31_RIGOR_PASS.
Not for live deployment; not for public repo. See
`Gen13/sprint_bundle_2026-05-06_v31_RIGOR_PASS/SCRUTINY_BY_CK_2026-05-06.md`
for context.

Layout:
    substrate.py    A0 -- the substrate Z/10Z, ADD, MUL, sigma, sigma_units, CRT
    properties.py   A1 + A2 -- commutativity, non-associativity assertions
    generators.py   A3 -- BEING / DOING / BECOMING generator triples
    fusion.py       A4 -- fuse(3, 4, 7) = 8 axiom (verified on BHML, fails on TSML)
    lenses.py       A5 -- TSML via C_0 rule + perturbations; BHML via 4 rules.
                          Constructed FROM RULES, not hardcoded.
    verifications/
        v1_tsml_closure.py   Generator triples close under TSML's C_0 rule
        v2_bhml_closure.py   Generator triples close under BHML's 4 rules
        v3_uniqueness.py     [STUB] V3 uniqueness theorem -- requires Dell R16

The foundations module is intentionally minimal at this stage. The audited
journal papers (sigma-rate, four-core consolidated, JCAP, Sprint 18) carry
their own self-contained verification scripts and should remain
authoritative until V3 lands and the foundational paper is rebuilt to
inherit the audited posture.
"""

__version__ = "0.1.0-draft"
__status__ = "private"
