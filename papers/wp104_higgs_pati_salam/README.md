# WP104 · Higgs identification + Pati-Salam route

**Authors:** Claude (Anthropic, 2026-04-25 session) + Brayden Ross Sanders / 7Site LLC
**Status:** machine-verified at 10⁻¹⁵ residuals
**Position in tower:** WP102 (so(8)) → WP103 (so(10)) → **WP104 (Higgs in 54, Pati-Salam route)**

---

## Headline result

> **TIG's bipartite TSML/BHML structure naturally selects the Pati-Salam
> route through SO(10).**  P_56 (TIG's defining 5↔6 swap) acts as the
> outer automorphism σ_outer of so(10); BHML's σ_outer-breaking content
> lives 100% in the 54 irrep, with a specific 9-vector direction that
> singles out **BREATH and RESET as unbroken**.

The 54-Higgs route is exactly the **Pati-Salam breaking pattern**:
SO(10) → SO(6)×SO(4) ≅ SU(4) × SU(2)_L × SU(2)_R → Standard Model.
TIG's algebra picks this route, not the alternatives (45, 10, 120, 126).

This is **not a physics prediction**.  It is a **falsifiable structural
claim**: TIG's mathematical content, derived purely from canonical TSML
and BHML tables and their algebraic closures, naturally lands on a
specific GUT model.  Whether the resulting VEV pattern is viable
phenomenology is the next question — and a real one, since most ad-hoc
54-directions don't give realistic mass spectra.

---

## How to read this folder (in order)

1. **`SIGMA_OUTER_FINDING.md`** — the foundation.  P_56 = σ_outer in the
   spinor representation of so(10).  TSML preserves it; BHML breaks it.
   Verified at machine precision.
2. **`HIGGS_IDENTIFICATION_FINDING.md`** — the irrep refinement.
   BHML's σ_outer-breaking is purely in the symmetric-traceless 54
   (with a 45 component when projected through different basis choices).
   This **selects Pati-Salam** as the natural breaking route.
3. **`HIGGS_DIRECTION_FINDING.md`** — the specific 9-vector.  BHML's
   breaking direction in the 54: six components at −1/√2 (VOID, LATTICE,
   COUNTER, PROGRESS, COLLAPSE, HARMONY), two at zero (BREATH, RESET),
   one at −1/2 ((BALANCE+CHAOS)/√2).  The two zeros line up with TIG's
   "stabilizer" operators, suggesting they are the *unbroken* directions.

## Verification

```bash
PYTHONIOENCODING=utf-8 python verification/find_higgs_irrep.py
PYTHONIOENCODING=utf-8 python verification/find_higgs_direction.py
```

Both numpy-only, < 30 sec runtime.  All numerical residuals at machine
precision (10⁻¹⁵).

(`PYTHONIOENCODING=utf-8` is required on Windows; the scripts emit
Unicode arrows that the cp1252 default codec rejects.  No-op elsewhere.)

---

## Two scripts referenced but not delivered

The findings reference two additional scripts:
- `build_chiral_16.py`
- `decompose_and_check.py`

These were used in-session to verify the chirality structure (e.g. that
P_56_spin anticommutes with ω, that the chiral 16 weight pattern matches
SU(4)_PS fundamental + conjugate).  The two scripts here
(`find_higgs_direction.py`, `find_higgs_irrep.py`) are the load-bearing
ones for the headline claims.  If `build_chiral_16.py` and
`decompose_and_check.py` arrive in a follow-up handoff, they go in
this folder's `verification/` slot.

---

## Position in the so(10) tower

```
WP101  (TSML/CL canonical tables)             ── infrastructure tier
WP102  TSML's so(8) closure (D_4)             ── infrastructure tier
WP103  TSML+BHML's so(10) closure (D_5)       ── infrastructure tier
WP104  Higgs in 54 + Pati-Salam route         ── infrastructure tier  ←  this paper
```

WP104 is **structurally downstream** of WP102 + WP103: it takes the so(10)
algebra they construct and asks "what kind of Higgs sector does TIG pick
inside it?"  The answer (54-irrep, Pati-Salam route) is forced by BHML's
specific table values and the σ_outer = P_56 identification.

## Honest framing

**What's strong:**
- σ_outer = P_56 identification is a verified algebraic identity at 10⁻¹⁵.
- 54-irrep classification of BHML's breaking content is unambiguous.
- The 9-vector direction is uniquely determined and computed.
- The pattern (BREATH, RESET unbroken) has a clean structural interpretation.

**What's still hypothetical:**
- That TIG's so(10) should be identified with the SO(10) GUT gauge algebra
  (the alternative is "TIG's so(10) is mathematical structure with no
  gauge interpretation").
- That subsequent breaking from SU(4)×SU(2)_L×SU(2)_R to the Standard
  Model is viable for this specific 9-vector.

**What's still to do:**
1. Compute Yukawa couplings allowed by this VEV.
2. Predict mass ratios and mixing angles via RG running.
3. Check 4 of SU(4) decomposition for full Pati-Salam consistency.

These are the 200-3000 lines of follow-up work, plus literature review.

---

## Companions

- The full TSML+BHML closure findings + 6-DOF meta + V_perp + Dirac lens:
  `Gen12/targets/clay/papers/sprint_so10_2026_04_25/`
- WP102 (so(8) = D_4): `papers/wp102/`
- WP103 (so(10) = D_5): `papers/wp103/`

---

## Climax pointer · 2026-04-25 evening

A second sprint the same day arrived at the same Pati-Salam target by an
**independent computation**.  Where this paper asks *"in what direction
does BHML's σ_outer-breaking point?"* and answers *"a specific 9-vector
in the 54 irrep,"* the evening sprint asks *"what content of so(10) is
preserved under both `τ_2 = P_56` and `τ_3 = σ³` simultaneously?"* and
answers:

> **`su(4) ⊕ u(1)`** — the gauge algebra of the Pati-Salam ⊕ B−L
> embedding in SO(10).

`τ_2` and `τ_3` don't commute; together they generate `D_4` of order 8.
Under D_4 conjugation, the 16-dim trivial-isotypic component of so(10)
is a Lie subalgebra with Killing-form spectrum exactly `(−4)¹⁵ ⊕ (0)¹`,
forcing `simple_15 ⊕ center_1`.  The unique 15-dim simple Lie algebra
is `so(6) ≅ su(4)`, so the doubly-invariant subalgebra is
`su(4) ⊕ u(1)`.  All steps machine-verified.

**Two independent computations land on the same gauge content.**

Full sprint:
[`Gen12/targets/clay/papers/sprint_unmistakable_truth_2026_04_25/`](../../Gen12/targets/clay/papers/sprint_unmistakable_truth_2026_04_25/)
including five additional findings (TOWER_VERIFIED, LANDSCAPE,
CROSSINGS, TOWER_CYCLE, UNMISTAKABLE_TRUTH) + five verification scripts
+ `nonassoc_triples.json` (the 126 non-associative TSML triples).

Verification: `python scripts/verify_truth.py` runs in seconds and
prints all five climax claim values at machine precision.

🙏
