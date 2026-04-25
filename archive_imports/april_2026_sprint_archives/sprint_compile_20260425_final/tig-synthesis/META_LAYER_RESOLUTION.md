# META-LAYER FINDINGS — THE SIX TIES, AUDITED

**Date:** 2026-04-25
**Status:** All six pairings from the post-zoom-out scan now resolved

---

## What this is

After the unmistakable-truth result on su(4) ⊕ u(1), I zoomed out and identified six pairings in the README where both endpoints existed but the bridge hadn't been computed. This document records the resolution of each.

---

## The six ties — final scorecard

| # | Tie | Result | Status |
|---|-----|--------|--------|
| 1 | ξ-cosmology ↔ so(10) tower | κ_Ξ = 13/(4e) | **POSITIVE** (structural) |
| 2 | T*=5/7 ↔ Killing −4 | The −4 is su(4)'s own internal scaling, not tied to T* | **CLARIFIED** (no direct tie) |
| 3 | First-G ↔ Crossing Lemma | First-G IS the first crossing event | **POSITIVE** (verified) |
| 4 | σ→0 rate ↔ ξ log nonlinearity | Bridge is via BB 1976, not yet quantitatively tested | NOT FULLY TESTED |
| 5 | Cohen-Macaulay failure ↔ u(1) center | Different 1's (complementary, not same) | **NEGATIVE** |
| 6 | CL eigenvalues ↔ 6-DOF spectrum | Loose 1% alignments only, not exact identities | **MIXED** |

---

## What survives as positive findings

### 1. κ_Ξ = 13/(4e) (FINDING: XI_COSMOLOGY_TIE_FINDING.md)

The 9-vector Higgs has ‖v‖² = 13/4 exactly, with the 13 traceable to BHML's σ_outer-asymmetric cell count (26/2). Under the GUT-natural identification m²_ξ = ‖VEV‖², κ_Ξ is forced to be 13/(4e) ≈ 1.196.

This closes README §3.5 question (iii) at the structural level. Falsifiability against DESI requires independent scale-fixing not yet computed.

### 3. First-G = first crossing event (FINDING: FIRST_G_CROSSING_TIE.md)

First-G's stability window {1, ..., p_1 − 1} is the size of the pre-crossing region in the Crossing Lemma's framework. The two theorems describe the same partition-geometry phenomenon at different abstraction levels.

This unifies §7.1 and §7.4 conceptually but doesn't change §3.1's open status.

### Bonus structural integers (from the spectral investigation)

- ‖TSML antisym‖² = 39, ‖BHML antisym‖² = 42, total = **81 = 9²** (exact)
- Projection onto su(4) simple part = exactly **29**
- Projection onto u(1) center = **25/8**
- Lattice projection eigenvalues = **{7, 7, 7}** (three HARMONYs at σ-fixed indices 3, 8, 9)
- ‖T_lie‖² = exactly **16**

These are clean structural integers. They're the verified content of TSML's spectrum.

---

## What's been clarified (not positive but useful)

### 2. T*=5/7 ↔ Killing −4 — clarified, no direct tie

The Killing eigenvalues are exactly −4 because:
- The 15-dim simple part is so(6) ≅ su(4)
- Standard su(4) Killing form is K = 2n·tr(XY) = 8·tr(XY)
- With basis normalized to tr(X²) = −1/2, K(X,X) = −4

The −4 is **su(4)'s own internal scaling**, not derived from T* = 5/7. The two appear independently in TIG. They both involve the integers 4 and 7 but for different reasons.

T* = 5/7 governs the threshold for coherent state survival in TIG runtime. The Killing −4 governs the metric on the gauge algebra. Different mathematical roles, no direct connection.

---

## What's negative (honest results)

### 5. Cohen-Macaulay failure ↔ u(1) center — different 1's

The Hilbert tail of R/I_CL is concentrated on x_0 = VOID. The u(1) center of the D_4-invariant subalgebra explicitly avoids VOID (and other σ-fixed indices), living entirely on the 6-cycle.

These are **complementary** 1-dim residuals. Not the same.

The lesson: TIG carries multiple distinct 1-dim residual structures, each in its own context (Hilbert tail in commutative algebra, u(1) center in Lie algebra, three exact HARMONYs in spectral-on-lattice, etc.). They shouldn't be conflated.

### 6. CL eigenvalues vs transcendental constants — 1% coincidences only

The userMemories claim "CL eigenvalues produce e, π, φ, ζ(3), Catalan G within 1%" is **partially true at 4-digit level**, **NOT true at exact-identity level**.

Closest "exact" match: |λ/10 − γ| = 6.2×10⁻⁵ (γ Euler-Mascheroni). That's 4-digit precision, not 16-digit precision. Coincidence-level, not algebraic-identity level.

What IS exact: the integer/rational structure on the spectrum (81, 29, 13/4, {7,7,7}). These are the TIG signature, not the transcendental approximations.

**Recommend:** flag the userMemories claim for revision. Replace with the verified integer/rational structure.

---

## What hasn't been tested fully (deferred)

### 4. σ→0 rate ↔ ξ log nonlinearity (BB bridge)

The README §3.5 cites Bialynicki-Birula 1976 as selecting the log nonlinearity as the unique separability-preserving wave-equation nonlinearity. WP101 gives σ(N) ≤ C/N for squarefree N with C < 3.

Whether the *exact* σ-rate constant C ties to the ξ-coupling κ_Ξ via the BB bridge is a separate calculation requiring careful unpacking of BB's argument. Not done in this sprint.

This is the same open issue as in the README §3.5 question (iii); my κ_Ξ result addresses ONE direction (Higgs VEV → coupling), but the BB-rate direction is still open.

---

## The honest meta-pattern

After exploring all six ties, the pattern that emerges:

**TIG has clean structural integer/rational content** (45, 16, 29, 9², 13/4, 7³, T*=5/7, 4/7, 2/7, the count 26 of σ_outer-asymmetric cells).

**TIG has loose 1%-level alignments to transcendentals** (γ, φ, Catalan G, 4/π²) — these are coincidences, not identities.

**TIG has multiple distinct residual 1-dim structures** (Hilbert tail, u(1) center, etc.) — these don't reduce to one universal 1.

**TIG's structural alignments to physics** (so(10), su(4)⊕u(1), Pati-Salam, 9-vector Higgs, ξ-coupling κ_Ξ) are real but conditional on natural-but-not-forced identifications.

Each of these is a *positive* finding when stated honestly. None is "TIG predicts physics from first principles." All are "TIG's structure aligns with physics under specific (well-motivated) identifications."

---

## What this means for the project

The README §3 frontiers have been advanced incrementally. Specifically:

- **§3.1 cryptography:** unified with Crossing Lemma; open question unchanged
- **§3.4 ξ-cosmology:** κ_Ξ now structurally constrained
- **§3.5 BB bridge / morphotic-braid:** partially addressed via κ_Ξ, BB-rate direction still open
- **§3.6 SO(10) tower:** strengthened by su(4)⊕u(1) finding

What remains for the §3.6 promise of "physics prediction" is still:
- Yukawa-level computation (200-3000 LOC)
- Independent scale-fixing (TIG ↔ Planck)
- Mass ratios, mixing angles, proton decay rates

These are substantial. None done in this sprint.

---

## Status of the project after this sprint

The verified algebraic structure has gotten richer (su(4)⊕u(1), 9-vector exact direction, κ_Ξ rational), but the gap to falsifiable physics prediction remains the same: substantial work in absolute scale-fixing.

The branches stay clean:
- **mantero-bridge:** D_4 / 16-dim subalgebra question, MathOverflow ready
- **tig-synthesis:** verified findings + κ_Ξ + First-G/Crossing tie
- **ck:** modules + speculation, including these meta-layer notes

🙏
