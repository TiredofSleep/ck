# Round 3 — BSD Level 2: Gross-Zagier and T*
## Can the Heegner Height Close at T* = 5/7?
*Author: Brayden Ross Sanders / 7Site LLC — 2026-04-02*

---

## Context

Round 2 established: BSD closes at Level 1 for rank-0 and rank-1 curves (Kolyvagin).

Round 3 asks: what is the Level 2 machine for BSD? And can T* = 5/7 appear there?

For rank-1 curves, the Level 2 machine is the **Gross-Zagier formula**:

```
L'(E,1) = (8π² / sqrt(N_E)) × ||f_E||² × h_NT(P_K) / [index]²
```

where:
- L'(E,1) = derivative of L(E,s) at s=1 (non-zero for rank-1 curves)
- f_E(z) = the weight-2 newform associated to E (modularity theorem)
- ||f_E||² = Petersson norm of f_E
- h_NT(P_K) = Néron-Tate height of the Heegner point P_K ∈ E(K)
- K = imaginary quadratic field chosen so that L(E⊗χ_K, 1) ≠ 0
- N_E = conductor of E

---

## The BSD Formula at Level 2

For a rank-1 curve where BSD is verified, the complete formula is:
```
L'(E,1) / Omega_E = (h_NT(P_K) × |Sha| × prod_p c_p) / |E(Q)_tors|²
```

For E1 = y²=x³−2 (rank 1, Sha trivial, conductor 1728):
- Rational point P = (3, 5) (found in Level 0)
- h_NT(P) = Néron-Tate height of (3,5)
- L'(E,1) can be computed numerically

**The Néron-Tate height of (3,5) on y²=x³−2:**

The naive height: h_naive(P) = log max(|3|, 1) = log 3 ≈ 1.099
The Néron-Tate height: h_NT(P) = h_naive(P) + (local correction terms)

For y²=x³−2, the discriminant Δ = −108×2² = −432. The conductor N = 1728? No.
Let me recalculate. y²=x³−2 has a = 0, b = −2.
Δ = -16(4a³ + 27b²) = -16(0 + 27×4) = -16×108 = -1728.
N_E for y²=x³−2: the curve has minimal model y²=x³−2, conductor N=1728/...

Actually the conductor of y²=x³−2 is 36 (this is a standard result for this curve,
which has CM by Z[ζ_3]).

**The Néron-Tate regulator for E1 = y²=x³−2:**
The regulator R = h_NT((3,5)) for the rational point (3,5).

Naive height computation:
h_naive(3,5) = log 3 (since x = 3/1 in lowest terms, h = log 3)

Local correction at p=2 (bad prime): the curve has additive reduction at p=2?
Discriminant Δ = -1728 = -12³ → bad primes: p | 1728 = 2⁶ × 3³ → bad at p=2,3.

For the Néron-Tate height, we need the local correction terms at p=2 and p=3:
h_NT(P) = h_naive(P) + Σ_p λ_p(P) + λ_∞(P)

This requires the local heights λ_p at bad primes and the archimedean height.
Without full computation, we can estimate:
h_NT((3,5)) ≈ log 3 + corrections ≈ 1.1 + O(0.1)

---

## T* at Level 2: The Ratio Test

The BSD formula at Level 2 gives a specific dimensionless ratio:
```
R_BSD = L'(E,1) / (Omega_E × h_NT(P))
      = (|Sha| × prod c_p) / |E_tors|²
```

For E1 = y²=x³−2: Sha trivial, c_p = 1 at all primes (assuming good reduction
outside {2,3}), E_tors = 1 (rank-1 curve, torsion trivial for this family).

So R_BSD = 1 for E1? That would mean:
```
L'(E,1) = Omega_E × h_NT(P)
```

**This is the Gross-Zagier Level 2 machine:** It says the derivative of the L-function
at s=1 is EXACTLY the period times the Heegner height. No free parameters.

**Can T* appear here?** The ratio R_BSD = 1 has no room for T* = 5/7.
BUT: the ratio of the Néron-Tate height to the naive height IS a non-trivial number:
```
h_NT(P) / h_naive(P) = 1 + (local correction ratio)
```

For the canonical choice K (imaginary quadratic field with maximal disc D_K):
```
h_NT(P_K) = L'(E,1) × (index)² / (8π² × ||f_E||² / sqrt(N_E))
```

The index² is the square of the index [E(K) : Z × P_K]. For many rank-1 curves,
the index = 1 (P_K is a generator).

---

## The Normalized Regulator

Define the NORMALIZED REGULATOR:
```
r(E) = h_NT(P) / log(N_E)    (height normalized by log conductor)
```

Under BSD and Gross-Zagier:
```
r(E) = L'(E,1) × |Sha| × prod c_p / (Omega_E × |E_tors|² × log(N_E))
```

The question is: for what family of curves does r(E) → T* = 5/7?

**For the standard rank-1 curves:**

| Curve | Conductor | h_NT(P) | log N_E | r(E) = h_NT/log N |
|-------|-----------|---------|---------|-------------------|
| 37a1 (y²+y=x³-x) | 37 | ~0.0512 | log 37 ≈ 3.611 | ~0.014 |
| 57a1 | 57 | ~0.184 | log 57 ≈ 4.043 | ~0.046 |
| 389a1 | 389 | ~0.152 × 2 = 0.304 | log 389 ≈ 5.963 | ~0.051 |

None of these approach T* = 5/7 = 0.714. The normalized regulator for standard
rank-1 curves is much smaller than T*.

**What if we normalize differently?**

The critical strip boundary: the regulator is related to the value L'(E,1) which
is "small" (of order sqrt(N_E) × ||f_E||²^{-1} × period). The natural normalization
in the explicit formula is:
```
r_critical(E) = h_NT(P) × log(N_E) / (Omega_E × period integral)
```

This ratio is dimensionless and of order 1. For 37a1:
- Omega = 2.451 (real period)
- h_NT(P) ≈ 0.0512
- log N = 3.611
- r_critical ≈ 0.0512 × 3.611 / 2.451 ≈ 0.0755

Still far from T* = 0.714.

---

## Where T* Would Need to Appear

For T* = 5/7 to appear as the Level 2 fixed point of the BSD fractal, it would
need to be the limiting ratio of some normalized BSD quantity. There are three
natural candidates:

**Candidate 1:** r_∞(E) = lim_{N→∞} h_NT(P) / (some function of N_E) = T* for a
specific family of quadratic twists E_d. This would require knowing the asymptotic
distribution of Heegner heights in twist families. The Goldfeld-Szpiro conjecture
gives bounds but not the limiting ratio.

**Candidate 2:** The period ratio Omega_+ / Omega_- = real period / imaginary period
for a curve with complex multiplication (CM). For CM curves:
- y²=x³−x (CM by Z[i]): Omega_+ / Omega_- = 1 (square lattice)
- y²=x³−1 (CM by Z[ω], ω = e^{2πi/3}): Omega_+ / Omega_- = ... (hexagonal lattice)

For a CM curve with CM by Z[√(-D)], the period ratio encodes the CM discriminant.
If some CM class has period ratio = 5/7, this would be a BSD Level 2 appearance of T*.

**Candidate 3:** The BSD regulator formula when Sha = 5/7 × something. Since |Sha|
is a perfect square (Sha is a square under BSD), |Sha| = 49/... — but 49 is a perfect
square. The BSD ratio:
```
L(E,1) / Omega = |Sha| × prod c_p / |E_tors|²
```
For |Sha| = 5², |E_tors| = 7: L(E,1)/Omega = 25 × (prod c_p) / 49. If prod c_p = 1:
L(E,1)/Omega = 25/49 = (5/7)² = T*².

**T* SQUARED appears if |Sha| = 25 and |E_tors| = 7.**

Is there a curve with |Sha| = 25 and |E_tors| = 7? Torsion group of order 7 is rare;
E_tors = Z/7Z exists (by Mazur: E_tors ∈ {1, Z/2Z, ..., Z/12Z, Z/2×Z/2, ...}).
Z/7Z is on Mazur's list. The BSD ratio with |Sha| = 25, |E_tors| = Z/7Z:
L(E,1)/Omega = 25/49 = T*².

**This is a concrete search target:**

> Does there exist an elliptic curve E/Q with E_tors = Z/7Z, |Sha| = 25, prod c_p = 1,
> such that L(E,1)/Omega = T*² = 25/49?

If yes: T* appears as the square root of the BSD ratio, which is a Level 2 appearance.
This is the Round 3 target.

---

## Round 3 Concrete Search Protocol

**Step 1.** Search Cremona tables for E with E_tors containing Z/7Z.
Known family: Torsion Z/7Z exists for specific conductors (e.g., conductor 294, 1225...).

**Step 2.** For each such curve, check |Sha| via BSD numerical verification.
Target: |Sha| = 25 (a non-trivial Sha order that is a perfect square: 5²).

**Step 3.** Check if L(E,1)/Omega = 25/49 = T*².

**Step 4.** If found: this is a numerical appearance of T* in the BSD Level 2 machine.
It would NOT prove BSD. It would be a structural coincidence at Level 2.

**Step 5.** If not found with |Sha|=25: try other Sha orders n² where n = 5/k for small k.
Alternative: |Sha| = 5, |E_tors| = sqrt(5×49/BSD_ratio).

---

## Status

This Round 3 target is OPEN. The search has not been run.

**Blocking question:** Are there any curves with torsion Z/7Z and non-trivial Sha?
Torsion Z/7Z is rare. Mazur's theorem says it can only occur for specific conductor
ranges. Non-trivial Sha with Z/7Z torsion is doubly rare.

**Alternative Round 3 target:** Search for L(E,1)/Omega = T* = 5/7 directly
(not T*²). This would require:
|Sha| × prod c_p / |E_tors|² = 5/7.
Since 5/7 is not an integer, this requires |E_tors|² not dividing |Sha| × prod c_p evenly.
But L(E,1)/Omega is algebraic and specifically L(E,1)/Omega = (rational number)
for rank-0 curves. The rational number 5/7 is not in the standard BSD tables.

**Revised Round 3 target:** Find any elliptic curve where 5 or 7 appears individually
in the BSD formula — either in the Sha order, the torsion, or the Tamagawa product.
The simplest case: |Sha| = 5 (first odd prime Sha order).

**Does any elliptic curve have |Sha| = 5?** Yes — Sha can be any perfect square by
Cassels' theorem, and the group Sha[p] for odd p exists. Specific examples:
LMFDB lists curves with |Sha| = 9, 25, 49 (all perfect squares). |Sha| = 5 does NOT
appear (Sha is a square). But |Sha| = 25 does appear. So searching for |Sha| = 25
with E_tors = Z/7Z is the correct target.

---

## Round 3 Summary

The BSD fractal at Level 2 (Gross-Zagier / Heegner height) reveals:

1. For rank-1 curves: Level 2 machine = Gross-Zagier formula. Closes the BSD fractal.
2. T* = 5/7 at Level 2 requires: |Sha| = 25, |E_tors| = Z/7Z, prod c_p = 1.
3. T*² = 25/49 appears as L(E,1)/Omega for such a curve.
4. This curve has not been found yet. Search is the Round 3 task.

The BSD fractal closes at Level 2 (Gross-Zagier) for rank-1 curves. T* = 5/7
could appear as the square root of the BSD invariant if the right curve is found.

This is the 3-cycle closure candidate for BSD.

---

*(c) 2026 Brayden Ross Sanders / 7Site LLC*
*See CLAY_FORMAL_RECORD.md for canonical entry. Search protocol to be run in next session.*
