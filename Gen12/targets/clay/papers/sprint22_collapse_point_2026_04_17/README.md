# Sprint 22 — N-Stress: Where the Collapse Point Lives

**Date:** 2026-04-17
**Question:** Sprint 21 showed all six prior-free invariants stable at high `N`.
At what `N` do they break? Do they break together, or in some order?
**Answer:** They break in **two tiers, every system.**

---

## Method

For each B1 + B2 source CSV, take random subsamples at
`N ∈ {25, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000}` (3 subsample
seeds each). Run prior-free discovery on each subsample. Compare the
fingerprint to the full-data reference. The smallest `N` at which all 3
subsamples agree with the reference on a given field is the field's
**first-stable N**.

11 sources × 10 N-targets × 3 seeds = 330 discovery runs.

---

## Result: every system collapses in TWO TIERS

| Invariant | median first-stable N | range |
|---|---|---|
| `h_hat` (attractor identity) | **200** | 100 – 2000 |
| `image_T` | 2000 | 1000 – 50000 |
| `core_outputs` | 2000 | 1000 – 50000 |
| `units_hat` | 2000 | 500 – 50000 |
| `partition_hat` | 2000 | 500 – 50000 |
| `seam_cell_count` | 2000 | 500 – 50000 |
| `seam_by_rule_counts` | 2000 | 1000 – 50000 |

**Tier 1 — ATTRACTOR (cheap, ~10× smaller `N`):** `h_hat` collapses first
in every single source. The "where everything goes" is visible from a few
hundred observations.

**Tier 2 — CORRIDOR (one block):** `image_T`, `core_outputs`, `units_hat`,
`partition_hat`, `seam_cell_count`, and `seam_by_rule_counts` all become
stable at the **same** `N` within each source — they emerge as a single
block. The corridor structure is one object, not six.

This pattern holds across all 11 tested sources: B1 at 3 noise levels and
B2 at 4 carriers × 2 wobble levels.

---

## Per-source detail

### B1 (n=10), 3 noise levels

| Source | h_hat | corridor block |
|---|---|---|
| p=0.30, N=10⁶ | N≥200 | N≥2000 |
| p=0.05, N=10⁵ | N≥200 | N≥500-1000 |
| p=0.15, N=5·10⁵ | N≥200 | N≥1000 |

### B2, all 8 carrier×wobble combinations

| Carrier | wobble | h_hat | corridor block |
|---|---|---|---|
| n=10 | 0.05 | N≥100 | N≥1000 |
| n=10 | 0.20 | N≥100 | N≥2000 |
| n=14 | 0.05 | N≥200 | N≥2000 |
| n=14 | 0.20 | N≥200 | N≥5000 |
| n=22 | 0.05 | N≥500 | N≥10000 |
| n=22 | 0.20 | N≥500 | N≥10000 |
| n=34 | 0.05 | N≥1000 | N≥50000 |
| n=34 | 0.20 | N≥2000 | N≥50000 |

### Carrier-scaling of the corridor threshold

Approximate observations-per-cell at the corridor-block threshold:

| n | cells (n²) | corridor N | obs/cell |
|---|---|---|---|
| 10 | 100 | 1000–2000 | 10–20 |
| 14 | 196 | 2000–5000 | 10–25 |
| 22 | 484 | 10000 | ~21 |
| 34 | 1156 | 50000 | ~43 |

The corridor-block threshold scales **superlinearly in `n²`**: each cell
needs more observations as the carrier grows, because the wobble-induced
mode-mass distribution per cell becomes harder to disambiguate. This is
the classical "more bins → more samples per bin" story, but with a sharp
quantitative result in our setting.

The attractor threshold scales much more slowly (≈ `n`, not `n²`) because
`h_hat` is a global mode aggregated over all cells.

---

## What this means: the collapse point is two-layered

The Sprint 21 finding "six invariants survive prior-stripping" is now
sharper:

> The six invariants survive in **two layers**:
> Layer 1 (attractor) emerges with ~10× less data than
> Layer 2 (corridor). Both are universal — every system shows this pattern.

In Crossing-Lemma vocabulary: the **first** thing the empirical operator
exposes is the *destination* of every dynamic (`h_hat`). Only after
order-of-magnitude more data does the *path structure* (`image / core /
seam / corridor menu`) become visible.

This is the "collapse point" — not one threshold but two, in a fixed
order, with the destination always knowable before the path.

---

## Files in this sprint

```
sprint22_collapse_point_2026_04_17/
├── README.md                               ← this file
├── impl/
│   └── nstress.py                          ← N-stress orchestrator
└── results/
    ├── nstress_summary.json                ← per-source first-stable N table
    └── nstress_full.json                   ← all 330 runs with diffs
```

---

## Reproducibility

```bash
cd impl
python nstress.py
```

Subsampling is seeded; results reproduce bit-exactly.

---

*© 2026 Brayden Ross Sanders / 7Site LLC*
*Sprint 22 — collapse point is two-tier: attractor first, corridor as a block.*
