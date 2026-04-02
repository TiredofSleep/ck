# K11_ZERO_HEIGHT_CORRELATION.md

**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

## K11 Attempt F: Numerical Cross-Correlation at ζ-Zero Heights

**Status**: D-tier no-go (numerically confirmed).
**Script**: `k11_zero_height_test.py`

---

## 1. Protocol

Evaluate the Kloosterman-Dirichlet partial sum:

```
A3_N(s) = Σ_{p≤2000} Kl(1,1;p) · p^{-s}     (303 primes, N=303)
```

at two sets of imaginary heights:
- **Test set**: s = 1.6 + i·γ_k for k=1,...,100 (known ζ-zero locations γ_k)
- **Control set**: s = 1.6 + i·t for 300 uniformly random t ∈ [0.5, 250]

**Question**: Is |A3_N(1.6 + i·γ_k)| statistically distinct from |A3_N(1.6 + i·t)|?

If yes → A3 has local analytic structure at ζ-zero heights (new result, C-tier).
If no → The Kloosterman series carries no pointwise memory of ζ-zero locations (D-tier no-go).

---

## 2. Results (Computed, k11_zero_height_test.py)

```
Metric              At ζ-zeros    At random t    Ratio
------------------------------------------------------
Mean |A3_N|           0.377808      0.370910    1.0186
Std dev               0.152149      0.156288    0.9735
Median                0.374286      0.386243    0.9690
Min                   0.050411      0.053045
Max                   0.710738      0.717306

KS statistic (two-sample): 0.053
```

**Interpretation of KS = 0.053:**
- KS < 0.10 → distributions are statistically indistinguishable
- The two samples (zeros vs random) have essentially identical CDFs
- The 1.9% mean difference is well within one standard deviation of natural fluctuation

**First 15 ζ-zeros individually:**
- Values at γ_k scatter between −1.5σ and +1.2σ from the random mean
- No systematic bias (not all above, not all below)
- No clustering near zero (which would indicate A3 has zeros at these heights)

---

## 3. Verdict: D-Tier No-Go

**Theorem K11.F (D-tier, numerical):**

A3_N(3/2 + i·γ_k) for the first 100 ζ-zeros is statistically indistinguishable
from A3_N(3/2 + i·t) at random heights. KS statistic = 0.053 (< 0.10 threshold).

**Consequence:** The Kloosterman-Dirichlet series A3(s) carries no **pointwise**
analytic signature at ζ-zero heights when evaluated on the line Re(s) = 3/2.

---

## 4. What This Means for the Bridge

The negative result is structurally informative:

**Confirmed**: The Eisenstein bridge must be **global** (integral over all t),
not local (special values at isolated t = γ_k). This was already the theoretical
expectation from K10 (the integrand |ζ(1+2it)|^{-2} encodes zeros through its
global Fourier spectrum, not through point values).

**Closed**: The hypothesis that A3(s) has zeros or poles at s = 3/2 + i·γ_k.

**Remaining**: Only the global integral mechanism survives:
```
A3^{Eis}(s) = ∫ |ζ(1+2it)|^{-2} K(s,t) dt
```
The γ_k appear as Fourier frequencies of |ζ|^{-2}, not as special values of A3.

---

## 5. K11 Structural Implications

The result redirects the program:

1. **Pointwise approach is closed.** No further computation of A3 at specific heights
   will reveal ζ-zero locations. The connection is global (integral), not local (evaluation).

2. **Double Dirichlet Z(s,w) is the last theoretical path.** Its functional equation
   (if it exists) would provide the global structural link without pointwise dependence
   on zero locations.

3. **K12 direction**: Study the global integral ∫ |ζ(1+2it)|^{-2} K(s,t) dt from the
   A3 side. Can the Kloosterman data determine this integral without computing |ζ(1+2it)|?
   This requires Z(s,w) or a Fredholm operator with better properties than K10.F3 found.
