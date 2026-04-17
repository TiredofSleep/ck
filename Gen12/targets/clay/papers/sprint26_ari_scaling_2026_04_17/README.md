# Sprint 26 — ARI Scaling: σ IS Shell-Recoverable in the Asymptotic Limit

**Date:** 2026-04-17
**Question:** Sprint 23 concluded "no walk on `T_emp` recovers σ" at carrier
sizes n ∈ {10, 14, 22, 34} on noisy data. Does that conclusion hold in the
asymptotic limit (analytic `C_0`, no noise) at larger `n`?
**Answer:** **No — Sprint 23's conclusion was noise-limited.** On analytic
`C_0`, W3-freq achieves near-perfect σ recovery starting at n ≈ 22 and
PERFECT recovery (ARI = 1.0) for many `n ≥ 38`.

---

## The revision to Sprint 23

| Source | n | data | ARI W3-freq |
|---|---|---|---|
| Sprint 23 (real B2 data, noise) | 10 | finite, noisy | -0.500 |
| Sprint 23 (real B2 data) | 14 | finite, noisy | 0.000 |
| Sprint 23 (real B2 data) | 22 | finite, noisy | 0.263 |
| Sprint 23 (real B2 data) | 34 | finite, noisy | 0.728 |
| **Sprint 26 (analytic C_0)** | 22 | infinite | **0.868** |
| **Sprint 26 (analytic C_0)** | 34 | infinite | **0.973** |
| **Sprint 26 (analytic C_0)** | 38 | infinite | **1.000** ★ |
| **Sprint 26 (analytic C_0)** | 46 | infinite | **1.000** ★ |
| **Sprint 26 (analytic C_0)** | 70 | infinite | **1.000** ★ |
| **Sprint 26 (analytic C_0)** | 158-194 | infinite | **1.000** ★ (multiple) |

The gap between Sprint 23 (0.728) and Sprint 26 (0.973) at the same `n=34`
is the **noise penalty**, not a structural barrier. Remove the noise, and
W3-freq closes the recovery.

---

## Method

For each `n` in 32 carriers up to n=230:

1. Build `T = C_0(R_n, h_n, σ_n)` analytically (Sprint 25 proof of
   constructibility).
2. Compute discovered units `units_hat` (inputs in seam cells).
3. Compute three label functions:
   - `W1_multiset` — sorted multiset of all outputs at row `u`
   - `W2_set` — sorted unique outputs at row `u`
   - `W3_freq` — sorted output frequency profile (label-free histogram)
4. Cluster units by label equality.
5. Compute Adjusted Rand Index against canonical σ partition.

This is pure math — no data generation, no randomness, no noise. Pure
asymptotic / "infinite-data" behavior of each strategy.

---

## Result: W3-freq recovers σ; W1/W2 do not

| n | n_units | n_canonical_σ_classes | ARI_W1 | ARI_W2 | **ARI_W3** |
|---|---|---|---|---|---|
| 10 | 2 | 2 | 0.000 | 0.000 | 0.000 |
| 14 | 4 | 4 | 0.000 | 0.000 | 0.000 |
| 22 | 8 | 5 | -0.061 | -0.061 | **0.868** |
| 34 | 14 | 5 | -0.022 | -0.022 | **0.973** |
| **38** | 16 | 5 | 0.000 | 0.000 | **1.000 ★** |
| **46** | 20 | 5 | 0.000 | 0.000 | **1.000 ★** |
| 50 | 18 | 5 | -0.013 | -0.013 | 0.985 |
| 58 | 26 | 6 | -0.006 | -0.006 | 0.993 |
| 62 | 28 | 6 | -0.005 | -0.005 | 0.994 |
| **70** | 22 | 5 | 0.000 | 0.000 | **1.000 ★** |
| 74 | 34 | 6 | -0.004 | -0.004 | 0.996 |
| 82 | 38 | 6 | -0.003 | -0.003 | 0.997 |
| 94 | 44 | 7 | -0.002 | -0.002 | 0.998 |
| 106 | 50 | 6 | -0.002 | -0.002 | 0.998 |
| 110 | 38 | 6 | -0.003 | -0.003 | 0.997 |
| 118 | 56 | 7 | -0.001 | -0.001 | 0.999 |
| 122 | 58 | 7 | -0.001 | -0.001 | 0.999 |
| 130 | 46 | 6 | -0.002 | -0.002 | 0.998 |
| 134 | 64 | 7 | -0.001 | -0.001 | 0.999 |
| 142 | 68 | 7 | -0.001 | -0.001 | 0.999 |
| **158** | 76 | 7 | 0.000 | 0.000 | **1.000 ★** |
| **166** | 80 | 7 | 0.000 | 0.000 | **1.000 ★** |
| **170** | 62 | 6 | 0.002 | 0.002 | **1.000 ★** |
| **178** | 86 | 7 | 0.000 | 0.000 | **1.000 ★** |
| **190** | 70 | 6 | 0.002 | 0.002 | **1.000 ★** |
| **194** | 94 | 7 | 0.000 | 0.000 | **1.000 ★** |
| **202** | 98 | 7 | 0.000 | 0.000 | **1.000 ★** |
| **206** | 100 | 7 | 0.000 | 0.000 | **1.000 ★** |
| 214 | 104 | 8 | -0.0004 | -0.0004 | 0.9996 |
| 218 | 106 | 8 | -0.0004 | -0.0004 | 0.9996 |
| 226 | 110 | 8 | -0.0003 | -0.0003 | 0.9996 |
| **230** | 86 | 7 | 0.000 | 0.000 | **1.000 ★** |

**Summary:**
- 12 / 32 carriers give PERFECT σ recovery (ARI = 1.0).
- All carriers `n ≥ 22` give ARI ≥ 0.868 — a non-trivial recovery.
- Carriers `n ≥ 38` give ARI ≥ 0.985 — near-perfect everywhere.
- W1 (multiset) and W2 (set) plateau near 0 — they preserve too much
  information (each unit's row signature is unique-ish, partitioning to
  near-singletons).

---

## Why W3-freq works (the structural argument)

Sprint 25 proved canonical `C_0` returns either `MAX(x, y)` or `MIN(x, y)`
on every seam cell. By the σ-rule:

> When `x, y ∈ Core` with `σ(x) ≠ σ(y)`, `C_0(x, y) = x` if `σ(x) < σ(y)`,
> else `y`.

So at row `u`:

- For each `v` with `σ(v) > σ(u)`: `T[u][v] = u` (u wins).
- For each `v` with `σ(v) < σ(u)`: `T[u][v] = v` (v wins).
- Equal σ or boundary cases → `h_n` or `0`.

The output histogram at row `u` is determined by:

1. The number of "u wins" cells = the count of units with σ-value greater
   than σ(u).
2. The frequencies of "v wins" outputs = the σ-class sizes below σ(u).
3. The boundary contributions to `h_n` and `0`.

Two units `u, u'` in the **same σ-class** see the same up/down
partitioning of the rest of the σ-spectrum, so they produce identical
output histograms — hence W3-freq groups them together. Two units in
different σ-classes see different partitionings, so their histograms
differ.

The recovery is exact when each σ-class has a unique histogram signature,
which begins to fail when:

- The carrier is too small (few units, identical histograms by chance).
- Two distinct σ-classes happen to have the same up/down partitioning of
  the spectrum.

The pattern of perfect-vs-near-perfect ARI in the table reflects exactly
this: at carriers where the σ-classes have distinct sizes, recovery is
exact; where two classes happen to have the same size, the histograms
collide and ARI drops to 0.99x.

This makes W3-freq an **algebraic shell-projection of σ** — the histogram
encodes precisely the σ-class size profile, which is an invariant of σ
modulo class relabeling.

---

## Sprint 23 vs Sprint 26: reconciling

The two findings are not contradictory; they're **complementary**:

| Conclusion | Where it holds | Where it fails |
|---|---|---|
| "σ is curve-only" (Sprint 23) | Noisy data at small carriers | Large `n` analytic limit |
| "σ is shell-projectable" (Sprint 26) | Analytic `C_0`, large `n` | Small `n` or noisy finite data |

The honest combined statement:

> The σ-grading is **shell-projectable via output histograms** (W3-freq),
> with recovery quality scaling jointly in carrier size `n` and data
> quality (ratio of `N` to noise variance). At infinite data and `n ≳ 38`,
> recovery is exact (ARI = 1.0). At finite noisy data with `n ≤ 34`,
> recovery is partial (ARI ≤ 0.73 in our tests).

This re-positions the σ-curve / σ-shell distinction:

- **`T_emp` row signatures** (W1/W2): too fine — collapse to singletons.
- **`T_emp` row histograms** (W3): just right — recover σ-class structure
  asymptotically.
- **σ-class identity** (which orbit am I): this *is* in the shell, but
  encoded only in the count distribution, not the cell-by-cell pattern.

---

## What this means for the framework

This sharply revises the synthesis-branch claim that "the curve carries
σ, the shell carries the rest." The new statement is:

> The shell carries σ at the **histogram level** (sizes of σ-classes,
> recoverable for `n ≳ 38`). The shell does NOT carry σ at the
> **labeling level** (which specific units are in each class — that
> still requires the `Z`-lift via `(3u+1)/2^k` to compute exactly).

The 2×2 + paradox-classifier meta-spine still holds: the paradox
classifier's three-axis menu is shell-visible. The σ-grading's
**partition structure** (how many classes, of what sizes) is also
shell-visible asymptotically. The σ-grading's **labeling** (the bijection
units → class) requires the curve.

This is a more nuanced and accurate statement than Sprint 23's
"σ is curve-only" — and it surfaces a clean information-theoretic
quantity: **the asymptotic mutual information between (output
histogram of `T[u][·]`) and (σ-class of `u`) approaches 1 as `n` grows.**

---

## Open questions surfaced

1. **Closed-form characterization** of which `n` give exact ARI=1.0 vs
   which give 0.99x. Empirically the failures are when two σ-classes
   have equal size; can this be made precise?
2. **Mutual-information recovery rate**: the W3-freq ARI as a continuous
   function of `n` and noise level. Sprint 23 + Sprint 26 give the
   endpoints; the joint surface is unmapped.
3. **Re-examining other walk strategies on analytic `C_0`**: W4-W8 in
   Sprint 23 all returned trivial single-class partitions. Repeating with
   analytic `C_0` at large `n` may reveal which were also noise-limited.

---

## Files

```
sprint26_ari_scaling_2026_04_17/
├── README.md                        ← this file
├── impl/
│   └── ari_scaling.py               ← W1/W2/W3 ARI scan on analytic C_0
└── results/
    └── ari_scaling.json             ← per-n results
```

---

## Reproducibility

```bash
cd impl
python ari_scaling.py
```

Pure analytic computation. No data, no randomness. Deterministic.
~2 seconds for all 32 carriers.

---

*© 2026 Brayden Ross Sanders / 7Site LLC*
*Sprint 26 — σ IS shell-recoverable via W3-freq histogram, asymptotically perfect for n ≳ 38.*
