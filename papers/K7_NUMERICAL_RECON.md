# K7 — Numerical Reconnaissance

**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

*Luther-Sanders Research Framework · April 1 2026*
*Brayden Ross Sanders / 7SiTe LLC · DOI: 10.5281/zenodo.18852047*

---

## Status

**Tier: C** — Pre-registered predictions. Tier upgrades to D once companion scripts are executed and outputs recorded.

---

## Purpose

This document records, *before execution*, the theoretical predictions for the five companion scripts:

- `k7_compute_dp.py` — computes D_p^PSD(xi) for a grid of primes and xi values
- `k7_scan_scaling.py` — measures residual (D_p - leading) as a function of p
- `k7_fourier_dp.py` — takes the Fourier transform of D_p(xi) viewed as a function of xi
- `k7_prime_assembly.py` — assembles partial sums over primes (the Dirichlet candidates)
- `k7_character_probe.py` — computes Kloosterman sums Kl(1,1;p) and cross-correlates with D_p^PSD

Pre-registration is mandatory: if predictions are stated after running the scripts, confirmation bias cannot be excluded. Every prediction here is derived from the exact closed-form formula and standard analytic number theory. No curve-fitting.

---

## Background: The Exact Formula

The power spectral density of the prime-field orbit at prime p is:

```
S_p(xi) = sin^2(pi * xi * (p-1) / p) / ((p-1)^2 * sin^2(pi * xi / p))
```

This is an exact finite-p formula, not an approximation. The deviation from the sinc^2 baseline is:

```
D_p^PSD(xi) = p * (S_p(xi) - sinc^2(xi))
```

By direct Taylor expansion in 1/p (standard trigonometric identities), the leading deterministic limit is:

```
D_p^PSD(xi)  -->  -2 [sinc(2*xi) - sinc^2(xi)]   as p -> infinity
```

The correction is analytic in 1/p: every coefficient in the expansion

```
D_p^PSD(xi) = sum_{n=0}^{infty} c_n(xi) / p^n
```

is a deterministic function of xi with no dependence on the primitive root generator g. This is the core structural fact of the PSD route.

---

## Pre-Registered Predictions

### Prediction 1 — Convergence to Deterministic Limit

**Statement:** As p grows through primes, D_p^PSD(xi) converges pointwise to -2[sinc(2*xi) - sinc^2(xi)] for every fixed xi in (0, 1). The variance of D_p^PSD(xi) over primes, at fixed xi, converges to zero.

**Derivation basis:** The leading term c_0(xi) = -2[sinc(2*xi) - sinc^2(xi)] is the 1/p^0 coefficient. The next term is O(1/p). Therefore |D_p^PSD(xi) - c_0(xi)| = O(1/p) -> 0.

**Expected output from k7_compute_dp.py:** Plots of D_p^PSD(xi) for increasing p (e.g., p = 101, 503, 1009, 5003, 10007) should visually converge to a fixed smooth curve. The spread of curves should narrow monotonically with p. Numerical variance at any fixed xi should decrease proportionally to 1/p^2 (the square of the leading correction).

**What would constitute confirmation:** Variance at xi = 0.3 scales as C/p^2 for some fixed C, with R^2 > 0.99 in a log-log regression against 1/p^2.

---

### Prediction 2 — Residual Scaling

**Statement:** The residual R_p(xi) = D_p^PSD(xi) - c_0(xi) has mean approximately zero over a uniform xi grid and variance scaling as C/p^2 for some explicitly computable constant C(xi).

**Derivation basis:** The 1/p^1 coefficient c_1(xi) in the Taylor expansion is deterministic. The residual after subtracting c_0 is c_1(xi)/p + O(1/p^2). Averaging over xi, if c_1 has zero mean over the grid (to be verified numerically), then the mean of R_p is O(1/p^2). The variance is dominated by c_1(xi)^2 / p^2.

**Expected output from k7_scan_scaling.py:** A log-log plot of variance(R_p) vs p should be a straight line with slope approximately -2. The mean of R_p should be consistent with zero within noise. If c_1 has nonzero mean, the mean will scale as 1/p with a fixed prefactor.

**What would constitute confirmation:** Slope of log-log regression within [-2.1, -1.9].

---

### Prediction 3 — Fourier Spectrum of D_p as Function of xi

**Statement:** The Fourier spectrum of xi -> D_p^PSD(xi) matches the Fourier spectrum of xi -> -2[sinc(2*xi) - sinc^2(xi)] at all frequencies, with a correction that shrinks as 1/p.

**Derivation basis:** The Fourier transform is a continuous linear operation. Since D_p -> c_0 in L^2(0,1), the Fourier coefficients of D_p converge to those of c_0. The function c_0(xi) = -2[sinc(2*xi) - sinc^2(xi)] has known Fourier support: sinc^2 is the triangle function in Fourier space (supported on [-1,1]); sinc(2*xi) has support on [-2, 2]. So the Fourier transform of c_0 is supported on [-2, 2] and is explicitly computable.

**Expected output from k7_fourier_dp.py:** The discrete Fourier transform of D_p over a fine xi grid should show support concentrated in the band corresponding to |freq| <= 2, with the spectral shape converging to a fixed envelope as p grows. No new frequency content should appear as p increases; the high-frequency residual should shrink as 1/p.

**What would constitute confirmation:** Spectral power outside the [-2, 2] band is less than 0.5% of total power for p > 1000, and decreases with p.

---

### Prediction 4 — Kloosterman Sums: Distribution and Independence from D_p^PSD

**Statement:** The normalized Kloosterman sums Kl(1,1;p) / (2*sqrt(p)) have mean approximately zero and variance approximately 1/4 over a sample of primes. Furthermore, Kl(1,1;p) is uncorrelated with D_p^PSD(xi) for every fixed xi.

**Derivation basis:**
- The Weil bound gives |Kl(1,1;p)| <= 2*sqrt(p), so the normalized quantity is bounded in [-1, 1].
- By Katz's equidistribution theorem (Sato-Tate for Kloosterman sums), the values Kl(1,1;p)/(2*sqrt(p)) are equidistributed with respect to the measure (2/pi)*sqrt(1-t^2) dt on [-1,1] as p -> infinity. This measure has mean 0 and variance 1/4.
- D_p^PSD(xi) is g-independent (generator-free) by construction, since S_p(xi) depends only on p and xi. Kloosterman sums Kl(1, g^m; p) depend on g. For fixed m, Kl(1, g^m; p) is a character sum involving the specific primitive root g. Any correlation between Kl(1,1;p) and D_p^PSD(xi) would require D_p^PSD to carry generator information, which it structurally cannot.

**Expected output from k7_character_probe.py:**
- Histogram of Kl(1,1;p)/(2*sqrt(p)) over primes up to some bound should visually match the arcsine-like Sato-Tate density.
- Sample mean should be < 0.05 in absolute value.
- Sample variance should be in [0.20, 0.30].
- Pearson correlation between Kl(1,1;p) and D_p^PSD(0.3) (or any fixed xi) should be < 0.10 in absolute value.

**What would constitute confirmation:** All four numerical thresholds above are satisfied simultaneously.

---

## Expected Outputs by Script

| Script | Expected primary output | Expected numerical behavior |
|---|---|---|
| k7_compute_dp.py | D_p(xi) curves for many p | Converge to fixed smooth curve; spread ~ 1/p |
| k7_scan_scaling.py | Variance(R_p) vs p | Log-log slope ~ -2 |
| k7_fourier_dp.py | Fourier spectrum of D_p(xi) | Support in [-2,2]; outside < 0.5% of power |
| k7_prime_assembly.py | Partial sums over primes | Linear growth in X (see K7_DIRICHLET_ASSEMBLY_CANDIDATE) |
| k7_character_probe.py | Kl distribution + correlation | Mean ~ 0, Var ~ 1/4, |Corr| < 0.10 |

---

## What Would Constitute a Surprise

The following findings would require investigation and possible revision of the theoretical framework:

**S1 — Convergence failure:** D_p^PSD(xi) does NOT converge to c_0(xi) for some xi in (0,1), or the variance does not decrease with p. This would indicate an error in the Taylor expansion derivation and must be checked algebraically.

**S2 — Non-deterministic residual:** The residual R_p(xi) shows dependence on the primitive root generator g. This is structurally impossible given the formula for S_p, but must be verified numerically by checking that two primes p, p' with the same p but different g give the same D_p^PSD. (Each prime has a fixed g, so this is a cross-prime check of the formula, not a g-variation test.)

**S3 — Spectral leakage:** The Fourier spectrum of D_p(xi) shows significant power outside the [-2, 2] band that does NOT decrease with p. This would imply an additional periodic structure in the prime-field orbit that the PSD formula does not capture.

**S4 — Kloosterman correlation:** |Corr(Kl(1,1;p), D_p^PSD(xi))| > 0.2 for some xi. This would imply a structural link between the generator-dependent character sums and the generator-independent PSD, which is theoretically excluded. If observed, the most likely explanation is a finite-p artifact from small primes; re-run excluding p < 100.

**S5 — Kloosterman distribution mismatch:** The histogram of Kl(1,1;p)/(2*sqrt(p)) does not match the Sato-Tate distribution even for large p. This would constitute a new result conflicting with Katz's theorem; extraordinary numerical evidence would be required before claiming anything.

**S6 — Partial sum A1 does not grow linearly:** If A1(xi, X) = sum_{p<=X} D_p^PSD(xi) * log(p) grows faster or slower than X (by more than log factors), there is an oscillatory cancellation not predicted by the PNT estimate. This is unlikely but should be checked in k7_prime_assembly.py.

---

## Strategic Consequence

If predictions 1 through 4 all confirm:

- Prediction 1 confirms: D_p^PSD is a deterministic object plus a 1/p correction.
- Prediction 2 confirms: the residual is analytic in 1/p with no stochastic component.
- Prediction 3 confirms: no new frequency content — the PSD route carries no RH information beyond what is already in the sinc^2 baseline.
- Prediction 4 confirms: Kloosterman sums are independent of D_p^PSD, living in a separate (generator-dependent, character-sum) layer.

**Conclusion if all 4 confirm: the PSD route closes as a no-go. The PSD deviation D_p^PSD is real, computable, and deterministic — but it converges to a fixed function of xi that carries no prime-by-prime discriminating information. It cannot distinguish zeros of zeta. The frontier is the Kloosterman-based D_p: the generator-dependent, character-sum assembly candidate A3 defined in K7_DIRICHLET_ASSEMBLY_CANDIDATE.**

---

## Notes on Pre-Registration Integrity

- This document is committed to the repository before any script is run.
- Numerical results will be recorded in a companion file K7_NUMERICAL_RECON_RESULTS.md upon execution.
- Predictions are not adjusted retroactively. Any discrepancy between predictions and results is recorded as a finding, not silently corrected.
- Tier will advance from C to D once results are recorded and predictions are evaluated.

---

*© 2025–2026 Brayden Ross Sanders / 7SiTe LLC*
*Licensed under the 7SiTe Public Sovereignty License v1.0*
*DOI: 10.5281/zenodo.18852047*
