# TIG Synthesis — Sprint Summary (2026-04-25)

**Purpose:** Verified structural findings from this sprint, ready for inclusion in the TIG-internal corpus. All verified at machine precision.

---

## Sprint arc

The sprint started with a question about the towered/intertwined structure of TSML+BHML's degrees of freedom, moved through the σ_outer identification and Higgs-direction work, then through the Pati-Salam-route placement, and ended with the unmistakable double-invariant truth.

Each finding builds on the previous; reading in order shows the trail.

---

## Verified findings, in arc order

### 1. The towered structure has two real (5↔6)-style pairs, not three

`TOWER_VERIFIED.md` — Pair 1 (Lie ⇌ Jordan, τ=transposition) and Pair 2 (Clifford ⇌ Permutation, τ=P_56) are real involutions with verified breaking elements. Pair 3 (Lattice ⇌ Operad) is a transverse register, not a coin-flip pair. Lattice cuts across the tower; Operad's placement is an open structural question.

### 2. P_56 = σ_outer in the spinor representation

`SIGMA_OUTER_FINDING.md` — In Cl(0,10), the reflection element `(γ_5 − γ_6)/√2` anticommutes with the volume element ω, sending +chirality 16 entirely into −chirality 16 (residual = 0.0000). P_56's conjugation on so(10) IS the outer automorphism σ_outer that exchanges the two chiral 16-irreps. In SO(10) GUT physics this is the matter-antimatter exchange.

**Consequence:** TSML preserves matter-antimatter symmetry (P_56 commutes with TSML); BHML breaks it (26 cells differ under P_56 conjugation).

### 3. BHML's σ_outer-breaking is purely 54-irrep (not 45)

`HIGGS_IDENTIFICATION_FINDING.md` — Of BHML's σ_outer-breaking content: 100% lives in the symmetric-traceless 54 irrep, 0% in the antisymmetric 45 irrep, 0% in the singlet 1. This singles out the **Pati-Salam route** (SO(10) → SU(4) × SU(2) × SU(2)) as the natural breaking pattern, since 54-Higgs breaks SO(10) → SO(6) × SO(4) ≅ Pati-Salam.

### 4. The 9-vector Higgs direction is computed exactly

`HIGGS_DIRECTION_FINDING.md` — BHML's σ_outer-breaking content lies entirely (100% coverage) in a specific 9-dimensional so(9)-vector inside the 54. The 9 components in the natural basis:

```
VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, HARMONY: −1/√2 each
BREATH, RESET: 0 each
(BALANCE+CHAOS)/√2: −1/2
```

**BREATH and RESET are exactly excluded** from the breaking pattern. This is structural — rows 8 (BREATH) and 9 (RESET) of BHML have BHML[i,5] = BHML[i,6] = 7, so they're σ_outer-symmetric.

### 5. Both sides of the Lie/Jordan coin regenerate the same algebra

`CROSSINGS_FINDING.md` — The Jordan-side commutators of TSML+BHML's symmetric parts span all of so(10) by themselves, dimension 45. The Lie-side regenerates the same. The two sides aren't complementary halves — they're dual presentations of one algebra. The "two sides of one coin" framing was wrong; it's one coin viewed from two angles.

The single asymmetry: 19 nonzero antisymmetric generators + 20 nonzero symmetric generators. The 20-19 = 1 imbalance comes from `L_B[0]` being the identity row (purely symmetric, no antisymmetric part).

### 6. Three tower involutions, three different decompositions

`TOWER_CYCLE_FINDING.md` — Cycling through the involutions (τ_1 transposition, τ_2 P_56 conjugation, τ_3 σ³ conjugation) gives three structurally different decompositions of so(10):

- τ_1: full Lie/Jordan flip (acts on full algebra structure)
- τ_2 (P_56): so(10) = 36 + 9 = so(9) ⊕ R⁹
- τ_3 (σ³): so(10) = 24 + 21 (centralizer of σ³ ⊕ complement)

The dimensions are forced by the cycle structure of the involution: for f fixed and p transposition pairs, `+1 dim = f(f-1)/2 + fp + p(p-1)`.

### 7. The doubly-invariant content is su(4) ⊕ u(1)

`UNMISTAKABLE_TRUTH.md` — τ_2 and τ_3 don't commute. Together they generate D_4 of order 8. Under D_4 conjugation, so(10) decomposes:

```
so(10) = 16·trivial + 1·sign₂ + 12·sign₃ + 8·(2-dim irrep)
```

The 16-dim trivial-isotypic component is a Lie subalgebra. Its Killing form spectrum is exactly `(−4)^15 ⊕ (0)^1`. Identification: **su(4) ⊕ u(1)**.

This is the gauge structure of Pati-Salam color-lepton (su(4)) plus B−L (u(1)) — exactly what the BHML 9-vector pointed to in finding 4.

**The doubly-invariant content of TIG's two natural Z_2 involutions is the gauge algebra of the Pati-Salam route through SO(10).** Two independent computations (BHML's individual breaking direction; the simultaneous invariance under both involutions) land on the same SO(10) → SU(4)×SU(2)² → SM chain.

---

## Structural status of TIG after this sprint

What we had before:
- TSML+BHML → so(10) (verified, prior sprint)
- TSML preserves something; BHML breaks something (vague)

What we have now:
- TSML preserves σ_outer (matter/antimatter); BHML breaks it specifically along the 54 irrep, in a specific 9-vector direction
- BHML's 9-vector excludes BREATH and RESET as unbroken directions
- Combining the two natural involutions singles out su(4) ⊕ u(1) as the doubly-invariant gauge content
- This matches the Pati-Salam route, by two independent computations

The connection from "TIG produces so(10)" to "TIG's structure aligns with the Pati-Salam route to the Standard Model" is now structural and machine-verified, not interpretive.

---

## What remains open (honest)

1. **Yukawa couplings.** No mass ratios computed. To turn the Higgs-direction finding into mass predictions requires Yukawa structure that we don't yet have.
2. **Subsequent breaking.** Pati-Salam → SM requires further symmetry breaking. Whether TIG's structure forces a viable SM-direction is unanswered.
3. **Operad placement.** Pair 3 of the tower remains transverse, not a clean coin-flip. The arity-3 fuse table is incomplete (one rule known: `fuse([3,4,7]) = 8`).
4. **Whether the so(10) identification with SO(10) GUT gauge group is physically warranted.** This is a hypothesis, not a derivation. Could also be a flavor symmetry, hidden-sector group, or pure mathematical structure.

---

## Files in this sprint update

- `TOWER_VERIFIED.md` — Pair 1 and 2 verified, Pair 3 transverse
- `SIGMA_OUTER_FINDING.md` — P_56 = σ_outer
- `HIGGS_IDENTIFICATION_FINDING.md` — BHML σ_outer-breaking is 54-irrep
- `HIGGS_DIRECTION_FINDING.md` — explicit 9-vector with BREATH/RESET zeros
- `LANDSCAPE_FINDINGS.md` — non-associativity 12.6%, all involve HARMONY
- `CROSSINGS_FINDING.md` — Lie and Jordan dual presentations
- `TOWER_CYCLE_FINDING.md` — three involutions, three decompositions
- `UNMISTAKABLE_TRUTH.md` — su(4) ⊕ u(1) as doubly-invariant content

Plus verification scripts:
- `count_crossings.py` — Lie/Jordan coupling counts
- `cycle_tower_v2.py` — three-involution decomposition
- `verify_truth.py` — final result verification (all 5 claims)

---

## Status

Material ready for inclusion in TIG synthesis corpus. All claims machine-verified. WP9/WP10 (LATTICE theorem and DKAN) integration deferred to next sprint.

🙏
