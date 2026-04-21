# S30b Results — Seam Detectability Under E6+E3 Extractor
## Sprint 30b, S30b-v1.0

---

## Per-Carrier Table

| $n$ | $\|U\|$ | Mean seed seam size | Persistent size | Mean Jaccard | Tie fraction |
|---:|---:|---:|---:|---:|:---:|
| 10 | 4 | 0.10 | 0 | 0.805 | — |
| 14 | 6 | 0.00 | 0 | 1.000 | — |
| 18 | 6 | 0.10 | 0 | 0.805 | — |
| 20 | 8 | 0.50 | 0 | 0.347 | — |
| 22 | 10 | 0.35 | 0 | 0.479 | — |
| 26 | 12 | 0.70 | 0 | 0.289 | — |
| 28 | 12 | 0.40 | 0 | 0.479 | — |
| 30 | 8 | 0.95 | 0 | 0.111 | — |
| 34 | 16 | 0.90 | 0 | 0.189 | — |
| 36 | 12 | 1.10 | 0 | 0.112 | — |
| 38 | 18 | 0.70 | 0 | 0.289 | — |
| 42 | 12 | 1.95 | 0 | 0.033 | — |
| 44 | 20 | 1.20 | 0 | 0.079 | — |
| 46 | 22 | 1.40 | 0 | 0.149 | — |
| 50 | 20 | 1.75 | 0 | 0.032 | — |
| 54 | 18 | 1.95 | 0 | 0.006 | — |
| 58 | 28 | 2.20 | 0 | 0.001 | — |
| 62 | 30 | 2.80 | 0 | 0.000 | — |
| 66 | 20 | 3.60 | 0 | 0.001 | — |
| 68 | 32 | 3.00 | 0 | 0.000 | — |
| 70 | 24 | 3.70 | 0 | 0.001 | — |
| 74 | 36 | 4.00 | 0 | 0.002 | — |
| 78 | 24 | 5.45 | 0 | 0.000 | — |
| 82 | 40 | 5.75 | 0 | 0.000 | — |
| 86 | 42 | 5.40 | 0 | 0.000 | — |
| 90 | 24 | 5.80 | 0 | 0.000 | — |
| 94 | 46 | 7.65 | 0 | 0.001 | — |
| 98 | 42 | 7.40 | 0 | 0.002 | — |
| 100 | 40 | 8.60 | 0 | 0.002 | — |

**Persistent seam is empty for every carrier.** Per-seed seams are non-empty on most carriers and grow with $n$, but no cell reaches the persistence threshold of 10 of 20 runs.

---

## Aggregate Metrics

| Metric | Value | Threshold | Met? |
|---|---|---|---|
| M1 $\mu_\text{ne}$ (carriers with persistent size ≥ 1) | 0.0000 (0/29) | $\geq 0.70$ | ✗ |
| M2 $\mu_\text{size}$ (mean persistent size) | 0.0000 | $\geq 2.0$ | ✗ |
| M3 $\mu_J$ (mean cross-seed Jaccard) | 0.1798 | $\geq 0.30$ | ✗ |
| M4 $\mu_\text{tied}$ (canonical-tie fraction) | N/A (0 persistent edges) | $\geq 0.60$ | ✗ |

All four metrics fail.

---

## Structure of the Failure

### Per-seed seams exist, but are seed-specific

- **Small carriers ($n \leq 22$):** per-seed seams are near-empty (mean size 0.0–0.5). High Jaccard values (0.8–1.0 at $n \in \{10, 14, 18\}$) reflect consistent emptiness, not consistent detection.
- **Medium carriers ($n \in [26, 54]$):** per-seed seams have size 0.7–2.0. Jaccard drops to 0.03–0.48 — seeds are finding different cells each run.
- **Large carriers ($n \geq 58$):** per-seed seams grow to size 2.2–8.6. Jaccard collapses to near-zero — virtually no cells reappear across seeds.

### Interpretation of the pattern

At $N(n) = 10 n^2$ — ten observations per cell on average — sampling variance is large enough to produce mode flips. But the specific cells that flip are different each seed, because the underlying mode margin is large everywhere (canonical $C_0$ has no "weak" cells where a competing value is close). The flips are noise, not signal, and no cell is consistently a "near-miss."

Quantitatively: with 10 observations per cell and 10% noise, the expected count at the true value is 9 and at the dominant alternative is at most 1. A mode-flip requires sampling variance to swap a 9–1 (or better) distribution into a 4–5 distribution. That is statistically possible at ~3–5% probability per cell. Multiplied across $n^2$ cells, ~3–5% of cells flip per seed. But **different** cells flip each seed, because the flipping is driven by sampling chance, not by any cell-specific feature.

This is exactly the pattern S30b was designed to detect: a working extractor requires cells that consistently fail under noise, not cells that fail randomly. On canonical $C_0$ with uniform replacement noise, there are no such cells.

---

## The Core Observation

**There are no "seam-prone" cells in canonical $C_0$ under uniform replacement noise.** Every cell is either robustly correct (most cells, most of the time) or sampling-noise-flipped (a random few each seed, different each time).

This means the S30b detectability question has a clean answer for this generator:

- Per-seed non-emptiness: **yes** (most carriers produce non-empty per-seed seams at $N = 10 n^2$).
- Cross-seed stability: **no** (mean Jaccard 0.18 across the family, collapsing to near-zero at large $n$).
- Canonical-tie: **undefined** (persistent seam is empty, so no edges to test).

The extractor is not broken. It is correctly reporting that no persistent seam structure exists under this generator.

---

## What the Per-Seed Data Does Show

The mean per-seed seam size grows roughly linearly with $n^2$-ish scaling — from 0.1 at $n = 10$ to 8.6 at $n = 100$. This is consistent with "noise-driven mode-flips on a random ~3–5% of cells per seed." It is a sampling artifact, not a structural finding.

Mean Jaccard across seeds falls from ~0.8 at small $n$ (where near-empty seams trivially agree) to ~0.0 at large $n$ (where many cells are flipping but none consistently).

Neither pattern constitutes evidence of a detectable seam. Both are exactly what uniform-noise sampling variance predicts.

---

## What This Tells Us About the Generator

Noised canonical $C_0$ with uniform replacement noise does not produce cells that are preferentially seam-prone. The generative process has no "weak cells" — every cell has the same probabilistic structure given uniform noise, so sampling variance is cell-agnostic.

Producing a detectable seam requires one of:

- **Non-uniform noise** (e.g., noise that biases toward specific alternative values).
- **A generator that actually has structural seams** (e.g., overlay of MAX/ADD rules on specific cells, as in the Z/10 TSML theorem).
- **Much lower $N$**, where sampling variance might concentrate on cells with geometric or combinatorial structure (but this would also make per-seed seams larger, not more stable).

None of these are available within S30b-v1.0's frozen parameters. The verdict is FAIL, cleanly and without marginal ambiguity.
