# S28 Results — Carrier-by-Carrier Data
## Sprint 28, S28-v1.0, Real Curve

---

## Real Carrier Table

All 29 carriers in the pre-registered list. Computed from canonical $C_0(R, h, \sigma)$ with $h = \max \text{ odd unit of } U(n)$ and $\sigma(u) = v_2(3u+1)$.

| $n$ | $h(R_n)$ | $\beta(R_n)$ | In band [0.60, 0.95]? | Adjacent step $\|\Delta\beta\|$ |
|---:|---:|---:|:---:|---:|
| 10  |   9 | 0.7900 | ✓ | 0.000800 |
| 14  |  13 | 0.7908 | ✓ | 0.064133 |
| 18  |  17 | 0.8549 | ✓ | 0.002444 |
| 20  |  19 | 0.8525 | ✓ | 0.004463 |
| 22  |  21 | 0.7955 | ✓ | 0.028521 |
| 26  |  25 | 0.8240 | ✓ | 0.026775 |
| 28  |  27 | 0.8508 | ✓ | 0.054723 |
| 30  |  29 | 0.9056 | ✓ | 0.081144 |
| 34  |  33 | 0.8244 | ✓ | 0.071333 |
| 36  |  35 | 0.8958 | ✓ | 0.083511 |
| 38  |  37 | 0.8123 | ✓ | 0.096451 |
| 42  |  41 | 0.9087 | ✓ | 0.065206 |
| 44  |  43 | 0.8435 | ✓ | 0.025382 |
| 46  |  45 | 0.8181 | ✓ | 0.054283 |
| 50  |  49 | 0.8724 | ✓ | 0.022978 |
| 54  |  53 | 0.8954 | ✓ | 0.066361 |
| 58  |  57 | 0.8291 | ✓ | 0.007796 |
| 62  |  61 | 0.8213 | ✓ | 0.092556 |
| 66  |  65 | 0.9139 | ✓ | 0.073349 |
| 68  |  67 | 0.8406 | ✓ | 0.061237 |
| 70  |  69 | 0.9018 | ✓ | 0.071037 |
| 74  |  73 | 0.8307 | ✓ | 0.088267 |
| 78  |  77 | 0.9190 | ✓ | 0.089349 |
| 82  |  81 | 0.8297 | ✓ | 0.007193 |
| 86  |  85 | 0.8225 | ✓ | 0.114815 |
| 90  |  89 | 0.9374 | ✓ | 0.112267 |
| 94  |  93 | 0.8251 | ✓ | 0.039894 |
| 98  |  97 | 0.8650 | ✓ | 0.020100 |
|100  |  99 | 0.8851 | — | — (last carrier) |

## Aggregate Metrics

| Metric | Value | Threshold | Met? |
|---|---|---|---|
| $A$ (attractor rule concordance) | 1.0000 | $= 1.0$ | ✓ |
| $B_\text{band}$ (carriers in band) | 1.0000 (29/29) | $\geq 0.80$ | ✓ |
| $C_\text{smooth}$ (mean step) | 0.056406 | $\leq 0.10$ | ✓ |

**All three primary metrics pass.** Under the primary metric thresholds alone (§5.1, points 1–3), the invariant is observed to transport.

## Observations

- $h(R_n) = n - 1$ for all 29 carriers. Since all 29 carriers are even, and $n - 1$ is odd and coprime to $n$, this is always a unit and always the largest odd unit. The attractor rule "max odd unit" collapses to "n − 1" on this family.
- $\beta$ values range from 0.7900 (at $n = 10$) to 0.9374 (at $n = 90$). All well within the pre-specified band [0.60, 0.95].
- $\beta$ trends slightly upward with $n$, but not monotonically. Largest single adjacent step: 0.114815 between $n = 82$ and $n = 86$. Smallest: 0.000800 between $n = 10$ and $n = 14$.
- Mean $\beta$ across family: 0.855.

## What This Table Does Not Claim

- It does not claim the curve has a specific functional form.
- It does not claim the $\beta$ trend is monotone.
- It does not claim the 0.855 mean has physical meaning.
- It does not compare against non-canonical constructions or non-ring settings.

The primary-metric numbers are reported exactly. Null comparison follows in `S28_NULL_COMPARISON.md`. Verdict follows in `S28_VERDICT.md`.
