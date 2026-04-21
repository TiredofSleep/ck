# S29 Results — Anchored Deviation Curve Data
## Sprint 29, S29-v1.0, Real Curve

---

## Anchor Values

- $R_\text{anchor} = \mathbb{Z}/10\mathbb{Z}$
- $|U(10)| = 4$
- $\beta_\text{anchor} = 0.790000$ (from canonical $C_0$)

---

## Carrier Table, Sorted by Depth $d_1 = |U(n)| - 4$

| $n$ | $\|U(n)\|$ | $d_1$ | $h$ | $\beta(R_n)$ | $D(R_n)$ | $D \leq 0.25$ |
|---:|---:|---:|---:|---:|---:|:---:|
| 10 | 4 | 0 | 9 | 0.7900 | 0.0000 | ✓ |
| 14 | 6 | 2 | 13 | 0.7908 | 0.0008 | ✓ |
| 18 | 6 | 2 | 17 | 0.8549 | 0.0649 | ✓ |
| 20 | 8 | 4 | 19 | 0.8525 | 0.0625 | ✓ |
| 30 | 8 | 4 | 29 | 0.9056 | 0.1156 | ✓ |
| 22 | 10 | 6 | 21 | 0.7955 | 0.0055 | ✓ |
| 26 | 12 | 8 | 25 | 0.8240 | 0.0340 | ✓ |
| 28 | 12 | 8 | 27 | 0.8508 | 0.0608 | ✓ |
| 36 | 12 | 8 | 35 | 0.8958 | 0.1058 | ✓ |
| 42 | 12 | 8 | 41 | 0.9087 | 0.1187 | ✓ |
| 34 | 16 | 12 | 33 | 0.8244 | 0.0344 | ✓ |
| 38 | 18 | 14 | 37 | 0.8123 | 0.0223 | ✓ |
| 54 | 18 | 14 | 53 | 0.8954 | 0.1054 | ✓ |
| 44 | 20 | 16 | 43 | 0.8435 | 0.0535 | ✓ |
| 50 | 20 | 16 | 49 | 0.8724 | 0.0824 | ✓ |
| 66 | 20 | 16 | 65 | 0.9139 | 0.1239 | ✓ |
| 46 | 22 | 18 | 45 | 0.8181 | 0.0281 | ✓ |
| 70 | 24 | 20 | 69 | 0.9018 | 0.1118 | ✓ |
| 78 | 24 | 20 | 77 | 0.9190 | 0.1290 | ✓ |
| 90 | 24 | 20 | 89 | 0.9374 | 0.1474 | ✓ |
| 58 | 28 | 24 | 57 | 0.8291 | 0.0391 | ✓ |
| 62 | 30 | 26 | 61 | 0.8213 | 0.0313 | ✓ |
| 68 | 32 | 28 | 67 | 0.8406 | 0.0506 | ✓ |
| 74 | 36 | 32 | 73 | 0.8307 | 0.0407 | ✓ |
| 82 | 40 | 36 | 81 | 0.8297 | 0.0397 | ✓ |
|100 | 40 | 36 | 99 | 0.8851 | 0.0951 | ✓ |
| 86 | 42 | 38 | 85 | 0.8225 | 0.0325 | ✓ |
| 98 | 42 | 38 | 97 | 0.8650 | 0.0750 | ✓ |
| 94 | 46 | 42 | 93 | 0.8251 | 0.0351 | ✓ |

---

## Aggregate Metrics

| Metric | Value | Threshold | Met? |
|---|---|---|---|
| M1 Kendall tau | 0.062907 | $\geq 0.35$ | ✗ |
| M2 linear $R^2$ | 0.000046 | $\geq 0.40$ | ✗ |
| M2 slope | 0.000023 | (reported) | — |
| M2 intercept | 0.063243 | (reported) | — |
| M3 in-cap count | 29/29 | $\geq 27$ | ✓ |

Only one of three primary metrics passes (M3). M1 and M2 fail by orders of magnitude.

---

## Observations (Neutral, From the Data)

- The full range of $D(R_n)$ across the family is [0.0000, 0.1474]. All 29 carriers are well below the 0.25 cap.
- $D$ does not rise monotonically with $d_1$. Maximum $D$ in the family is 0.1474, at $n = 90$, $d_1 = 20$. At the deepest carrier ($d_1 = 42$, $n = 94$), $D = 0.0351$.
- At fixed $d_1$, $D$ values vary substantially. For example, at $d_1 = 8$ (carriers 26, 28, 36, 42), $D$ ranges from 0.0340 to 0.1187 — a spread of 0.085 at a single depth.
- The slope of the best linear fit is 0.000023 per unit of $d_1$. Over the full depth range of 42, the fitted trend predicts a $D$ increase of about 0.001 — i.e., essentially flat.

These observations are reported as data. They do not modify the verdict, which is determined by the frozen pass/fail rules applied to the frozen metrics.

---

## Real Metrics at a Glance

- Real Kendall tau is 0.063, far below the 0.35 threshold and barely above zero.
- Real $R^2$ is 0.000046 — essentially no linear trend of $D$ on $d_1$.
- Real M3 passes trivially: all 29 carriers have $D \leq 0.25$; the max $D$ observed is 0.1474.

Null comparison follows in `S29_NULL_COMPARISON.md`.
