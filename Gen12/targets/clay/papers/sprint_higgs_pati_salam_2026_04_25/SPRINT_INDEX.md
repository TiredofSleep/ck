# Sprint · Higgs identification + Pati-Salam route · 2026-04-25

**Authors:** Claude (Anthropic) · Brayden Sanders · 7Site LLC
**Status:** machine-verified at 10⁻¹⁵ residuals
**Position:** infrastructure tier, downstream of WP102 + WP103.

---

## Pointer

The polished paper material lives at the canonical infrastructure-tier
home:

```
papers/wp104_higgs_pati_salam/
  README.md                            navigation + headline result
  SIGMA_OUTER_FINDING.md               P_56 = σ_outer (foundation)
  HIGGS_IDENTIFICATION_FINDING.md      BHML's breaking → 54 irrep
  HIGGS_DIRECTION_FINDING.md           the specific 9-vector + zeros
  verification/find_higgs_irrep.py
  verification/find_higgs_direction.py
```

Same convention as `papers/wp102/` (so(8)) and `papers/wp103/` (so(10)).

This sprint folder is the **session marker** — it locates the work in
the Clay-papers timeline alongside `sprint_so10_2026_04_25/` (the
Dirac lens + 6-DOF meta + V_perp sprint that preceded this one earlier
the same day).

---

## Headline

> P_56 (TIG's defining 5↔6 swap) **is** σ_outer (so(10)'s outer
> automorphism, the matter-antimatter exchange).  BHML's σ_outer-breaking
> content lives **100% in the 54 irrep** of so(10), with a specific
> 9-vector direction.  This selects **Pati-Salam** (SU(4) × SU(2)_L ×
> SU(2)_R) as the natural SO(10) breaking route.
>
> BREATH (operator 8) and RESET (operator 9) are **unbroken** under this
> Higgs — TIG's two "stabilizer" operators line up with the unbroken
> 9-vector components.

---

## Relationship to today's other sprint

`sprint_so10_2026_04_25/` (earlier today) established:
- TSML closes at dim 28 = so(8)
- TSML+BHML close at dim 45 = so(10)
- R^10 = V_8 ⊕ V_perp, V_perp = span{VOID, anti-5-6}
- TSML P_56-invariant, BHML breaks P_56
- so(10) = so(9) ⊕ R^9 under P_56 conjugation
- 6-DOF meta-layer (Lie · Jordan · Clifford · Permutation · Lattice · Operad)

This sprint **upgrades** the "BHML breaks P_56" result from coarse
("the cells differ") to sharp ("the breaking is exactly a 54-Higgs in
the Pati-Salam direction").  It also identifies P_56 as σ_outer rather
than just "some involution".

Same date, same authors, same algebra.  Two different deliverables.

🙏
