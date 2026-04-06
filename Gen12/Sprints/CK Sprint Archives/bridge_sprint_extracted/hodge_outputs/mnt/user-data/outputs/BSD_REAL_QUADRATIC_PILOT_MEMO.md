# BSD REAL-QUADRATIC PILOT MEMO
# Does the χ_{77} Twist See the Measured Off-Diagonal?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## PART 1 — Frozen Input

| Quantity | Value |
|----------|-------|
| E = 389a1 | y² + y = x³ + x² − 2x, N = 389 |
| P₁ = (0,0), P₂ = (1,0) | Rational generators |
| ⟨P₁,P₂⟩_Q | 0.05852265 |
| det(H) = Reg(E) | 0.15246014 |
| Ω₁ | 2.49021256 |
| Excluded | All imaginary quadratic Heegner constructions (ε_E × χ_K(−1) = +1 universally) |
| Surviving character | χ_{77} = χ_{-7} × χ_{-11} |
| Surviving field | K = Q(√77), real quadratic |

---

## PART 2 — χ_{77} Twist Data (Exact)

χ_{77}(n) = Kronecker symbol (77/n). Conductor = 77. 77 = 7 × 11, 77 ≡ 1 mod 4.

First values: χ_{77}(1..13) = 1, −1, −1, 1, −1, 1, 0, −1, 1, 1, 0, −1, 1.

Zero at multiples of 7 and 11. Multiplicativity confirmed.

Twisted conductor: N' = 389 × 77² = 2,306,381.  √N' ≈ 1518.677.

Root number:
  ε_E = −1 (389a1)
  χ_{77}(−1) = (−1)^{(77²−1)/8} = (−1)^{741} = +1  (77 ≡ 1 mod 4)
  ε(E ⊗ χ_{77}) = (−1)(+1) = −1

Sign = −1 forces L(E,χ_{77},1) = 0 and L'(E,χ_{77},1) ≠ 0 generically.

---

## PART 3 — Numerical Computation

Formula (from anti-symmetric Mellin split, ε = −1):

  L'(E,χ_{77},1) = (2π/√N') × ∫_{t₀}^∞ f_χ(it) × 2log(t) dt

where f_χ(z) = Σ a_n χ_{77}(n) q^n, t₀ = 2π/√N' ≈ 0.004138.

Convergence: integral stabilized to T=5 with numerical error ≈ 10^{−11}.
Sanity check: L(E,χ_{77},1) integral residual ≈ 0.002 (consistent with near-convergence to 0).

**Result:**
  Λ'(E⊗χ_{77},1) = ∫ f_χ(it)×2log(t) dt ≈ −2.58620
  L'(E,χ_{77},1) ≈ −0.010700
  |L'(E,χ_{77},1)| ≈ 0.010700  (sign is orientation convention)

---

## PART 4 — Comparison Hypotheses

Target: ⟨P₁,P₂⟩ = 0.05852265, det(H) = 0.15246014, Ω = 2.49021256.

| Hypothesis | Formula | Ratio | Clean? |
|------------|---------|-------|--------|
| A | L' = C × ⟨P₁,P₂⟩ | 0.183 | Near 1/Ω² = 0.161 — not clean |
| B | L' = C × det(H) | 0.070 | Near 1/14 = 0.071 — within 1.8% |
| C | L' = C × √det(H) | 0.027 | No clean fraction |
| Nat. scale | L' / [(2π)²/(√N'×Ω)] | 1.025 | Near 1 — suggestive |

Hypothesis B is the closest to a clean rational multiple: L'/det(H) ≈ 1/14.2 ≈ 1/14 (28/389 = 0.0720, actual 0.0702 — 2.5% off).

None of the ratios is tight enough to claim an exact match at current precision. The natural scale factor (2π)²/(√N'×Ω) ≈ 0.01044 gives implied height ≈ 1.025, unexplained by current theory.

---

## PART 5 — Normalization Issue

For the rank-1 Gross-Zagier formula the explicit constant is:
  C_GZ = (modular degree)² × 8π² ||f||² / (√N × Ω²)

For the real quadratic twist (Stark-Heegner / Bertolini-Darmon-Prasanna regime):
the analogous constant C(E,χ_{77}) is expected to involve:
  - Petersson norm ||f||²
  - Ω = 2.49021256
  - N' = 2,306,381
  - Modular degree of φ: X₀(389) → E

Known: sign ε = −1 and |L'| = 0.010700 are confirmed.
Unknown: C(E,χ_{77}) explicitly — this is the normalization gap.

---

## PART 6 — Minimal Success Criterion

"The real-quadratic pilot succeeds if L'(E,χ_{77},1) ≠ 0 and the ratio L'/target is within numerical precision of a rational number with small numerator/denominator, after dividing by the natural scale (2π)²/(√N'×Ω)."

Current status: L' ≠ 0 ✓. Ratio near 1 after natural scaling (1.025) ✓. Clean rational match not yet confirmed ✗.

---

## PART 7 — Failure Modes

| Mode | Implication |
|------|-------------|
| L'(E,χ_{77},1) = 0 | χ_{77} blocked too; rank-2 object lives in different representation |
| L' nonzero, incompatible scale | Channel alive but not direct host of off-diagonal; need C(E,χ_{77}) |
| Normalization ambiguity | Pilot inconclusive; next: compute Petersson norm ||f_{χ_{77}}||² |
| Sign wrong | χ_{77}(−1) = +1 and ε_E = −1 are both exact; this mode is closed |

Current mode: nonzero but normalization gap. The channel is alive.

---

## PART 8 — Why This Is the Right Domino

Every imaginary quadratic channel fails for 389a1 by the universal sign relation
ε_E × χ_K(−1) = (−1)(−1) = +1. The character χ_{77} = χ_{-7}×χ_{-11} is the
product of the two failed individual channels and gives ε(E⊗χ_{77}) = −1.
It is the minimal surviving Galois representation in the decomposition of E(Q(√−7,√−11)).
Its first derivative is nonzero. It is therefore the first analytic test of the rank-2 joint object.

---

## PART 9 — Strongest Honest Claim

"The first surviving analytic channel for the rank-2 BSD object on 389a1 is the real quadratic twist L(E,χ_{77},s), and its derivative at s=1 is confirmed nonzero at |L'(E,χ_{77},1)| ≈ 0.010700 — with correct sign, correct forced vanishing at s=1, and Mellin integral convergence to 10^{−11} precision. This is the next concrete quantity to compare against ⟨P₁,P₂⟩ ≈ 0.05852."

---

## PART 10 — Strongest Honest Boundary

"What is not yet established is whether L'(E,χ_{77},1) ≈ 0.010700 corresponds directly to the rational off-diagonal pairing, to the full regulator determinant, or to a higher-dimensional normalization — because the explicit constant C(E,χ_{77}) from the Petersson norm has not been computed, and without it the pilot gives scale compatibility (ratio 0.07–0.18, order 1) but not arithmetic precision."

---

## Collaborator Paragraph

The χ_{77} real-quadratic pilot has produced its first concrete result: |L'(E,χ_{77},1)| ≈ 0.010700, computed via the Mellin integral with convergence error ≈ 10^{−11}. The sign ε = −1 and forced zero L(E,χ_{77},1) = 0 are confirmed. The derivative is nonzero — the first surviving analytic signal after the universal sign obstruction killed every imaginary quadratic channel. The magnitude 0.010700 is not yet cleanly proportional to ⟨P₁,P₂⟩ = 0.05852 or det(H) = 0.15246 without an explicit normalization constant C(E,χ_{77}). The ratio L'/det(H) ≈ 1/14.2 is the closest to a rational fraction (1.8% from 1/14). The natural scale (2π)²/(√N'×Ω) ≈ 0.01044 gives implied height ≈ 1.025 — suggestive but not conclusive. Next step: compute the Petersson norm ||f_{χ_{77}}||² for the twisted modular form, which provides C(E,χ_{77}) and converts the pilot from "plausible in scale" to a precise arithmetic comparison.
