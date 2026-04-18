# S30 Results — Observed Seam Graph Topology Data
## Sprint 30, S30-v1.0

---

## Per-Carrier Graph Summary

| $n$ | $\|E\|$ | $\|V_\text{ni}\|$ | $k$ components | Forest? | $d_{\max}$ | $\rho$ |
|---:|---:|---:|---:|:---:|---:|---:|
| 10 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 14 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 18 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 20 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 22 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 26 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 28 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 30 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 34 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 36 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 38 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 42 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 44 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 46 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 50 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 54 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 58 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 62 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 66 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 68 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 70 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 74 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 78 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 82 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 86 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 90 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 94 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 98 | 0 | 0 | 0 | ✓ | 0 | 1.000 |
| 100 | 0 | 0 | 0 | ✓ | 0 | 1.000 |

**Every carrier has an empty seam graph.**

## Aggregate Metrics

| Metric | Value | Threshold | Met? |
|---|---|---|---|
| $K_{\text{pass}}$ (fraction with $k \leq 3$) | 1.0000 (29/29) | $\geq 0.85$ | ✓ |
| $F_{\text{pass}}$ (fraction that are forests) | 1.0000 (29/29) | $\geq 0.80$ | ✓ |
| $D_{\text{pass}}$ (fraction with $d_{\max} \leq 4$) | 1.0000 (29/29) | $\geq 0.85$ | ✓ |
| $P_{\text{pass}}$ (fraction with $\rho \geq 0.70$) | 1.0000 (29/29) | $\geq 0.85$ | ✓ |

All four aggregate metrics pass their frozen thresholds. However, the pass is vacuous: empty graphs trivially satisfy every topology bound.

## The Core Observation

The observed seam set $S^{\text{obs}}(R_n) = \{(x, y) : T^{\text{emp}}_n(x, y) \neq C_0(x, y)\}$ is **empty for every carrier in the family**.

Under the data-generation parameters frozen in S30-v1.0 §3.3 ($N = 200{,}000$, $p_{\text{noise}} = 0.10$), the mode operator $T^{\text{emp}}_n$ equals $T_{\text{true}}_n = C_0(R_n, h_n, \sigma_n)$ exactly at every cell. At 200,000 samples per carrier, each $(x, y)$ pair receives on average $N/n^2$ observations (e.g., 2,000 for Z/10, 20 for Z/100). The mode votes with probability overwhelmingly matching the true value at every cell, so no disagreements appear.

This is the same noise-immunity behavior B1 exhibited at high $N$: uniform replacement noise does not flip modes until $p_{\text{noise}}$ approaches the margin defined by the next-most-frequent value.

## Why the Observed Seam Is Empty

At the frozen parameters, for any $(x, y)$ pair:
- With probability $1 - 0.10 = 0.90$: observation = $T_{\text{true}}(x, y)$.
- With probability $0.10$: observation = uniform random in $\{0, \ldots, n-1\}$.
  - With probability $1/n$: matches $T_{\text{true}}(x, y)$ by chance.
  - With probability $(n-1)/n$: a different value.

Expected fraction of observations matching $T_{\text{true}}(x, y)$ is $0.90 + 0.10/n$, which for all tested carriers is at least $0.90 + 0.001 = 0.901$.

Expected fraction of observations at any single competing value is at most $0.10 \cdot (1/n) \leq 0.01$ for all carriers.

Gap: at least $0.89$. Mode voting correctly identifies $T_{\text{true}}$ at every cell with overwhelming probability given $\geq 20$ samples per cell (and we have 2,000–20,000). No seams arise.

## What This Result Shows

- The mode operator on noised canonical $C_0$ data at moderate noise and high $N$ does not produce any structural seam relative to $C_0$ itself.
- The "observed seam graph" protocol in S30-v1.0 §3 returns empty graphs on this family under these parameters.
- The four topology metrics pass trivially because every threshold is satisfied by empty graphs.
- The null model, which preserves edge count, produces equally empty graphs — and the sigma separation is technically infinite (both variances are zero).

Null comparison in `S30_NULL_COMPARISON.md`. Verdict in `S30_VERDICT.md`.
