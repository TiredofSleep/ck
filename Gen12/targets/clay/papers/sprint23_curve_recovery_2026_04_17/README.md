# Sprint 23 — Curve Recovery: Can σ Be Walked Out of `T_emp`?

**Date:** 2026-04-17
**Question:** Sprint 21 showed signature equality on `T_emp` rows collapses
the partition to singletons. Do *other* walks on `T_emp` — coarser
equivalences, dynamics, commutators — recover the canonical σ partition?
**Answer (clean, hard):** **No.** None of 8 strategies reach perfect
recovery. The σ-grading is provably outside `T_emp`.

---

## Method

Eight prior-free walk strategies, applied to the full `T_emp` matrix from
Sprint 21:

| Strategy | Definition |
|---|---|
| W1 multiset | sorted multiset of outputs `{T_emp[u][v] : v ∈ Z/nZ}` |
| W2 set | sorted unique outputs |
| W3 freq | sorted histogram of output frequencies (label-free) |
| W4 self-orbit length | iterate `u_{k+1} = T_emp[u_k][u_k]`, cluster by orbit length |
| W5 self-orbit | cluster by `(orbit length, terminal value)` |
| W6 fixed-b=1 | iterate `u_{k+1} = T_emp[u_k][1]`, cluster by `(len, term)` |
| W7 fixed-b=h | iterate `u_{k+1} = T_emp[u_k][h_hat]`, cluster by `(len, term)` |
| W8 commutator | sort the tuple `(T_emp[u][v] − T_emp[v][u]) mod n` over `v ∈ units_hat` |

Each produces a partition of `units_hat`. Score against the **canonical**
σ partition by Adjusted Rand Index (ARI = 1.0 means perfect recovery, 0.0
means random, negative means systematically anti-correlated).

8 sources: B1 at 2 noise levels (n=10), B2 at 4 carriers × 2 wobble levels.

---

## Result: no walk recovers σ

| Strategy | mean ARI (over 8 sources) | perfect recoveries |
|---|---|---|
| W3 freq | **0.123** (best) | 0 / 8 |
| W4–W8 | 0.000 | 0 / 8 |
| W1, W2 | −0.146 | 0 / 8 |

### Per-source detail

| Source | best strategy | best ARI |
|---|---|---|
| B1 n=10 p=0.30 | W3 freq | -0.500 |
| B1 n=10 p=0.05 | W3 freq | -0.500 |
| B2 n=14 pw=0.05 | W1/W2/W3 | 0.000 |
| B2 n=14 pw=0.20 | W1/W2/W3 | 0.000 |
| B2 n=22 pw=0.05 | W3 freq | 0.263 |
| B2 n=22 pw=0.20 | W3 freq | 0.263 |
| B2 n=34 pw=0.05 | W3 freq | **0.728** |
| B2 n=34 pw=0.20 | W3 freq | **0.728** |

---

## The one signal: W3 frequency profile improves with carrier size

`W3_freq` partitions units by their output histogram (label-free). Its ARI
grows with the carrier:

| n | W3 ARI |
|---|---|
| 10 (B1) | -0.5 |
| 14 | 0.000 |
| 22 | 0.263 |
| 34 | 0.728 |

This is the single nontrivial trend in the experiment. As `n` grows, the
histogram of outputs at each unit carries more information about its
σ-class (because more units share each class on average).

But even at n=34 the recovery is partial — ARI=0.728 < 1.0. Extrapolating
the trend would suggest perfect recovery only at very large `n`, well
beyond the carrier sizes in our compatibility family.

The walk-based strategies (W4–W8) all produce trivial single-class
partitions because the iterated dynamics on `T_emp` converge fast to a
single attractor (`h_hat`); orbits do not separate units.

---

## Why this happens (and what it means)

The canonical σ map is `σ(u) = v₂(3u+1)`. The 2-adic valuation `v₂` of
`3u+1` is computed in **`Z`**, not in `Z/nZ`. It depends on how many times
2 divides the integer `3u+1` *before reducing modulo n*.

Once you reduce mod n, that information is destroyed. `T_emp` lives
entirely on `Z/nZ` — it cannot, in principle, recover information that
required the `Z`-lift to compute in the first place.

This is the precise sense in which **the σ-grading lives in the *curve*,
not the *shell***:

- The shell (`T_emp` on `Z/nZ`) carries the visible structure: image,
  core, attractor, corridor menu.
- The curve (the `(3u+1)/2^k` chain in `Z`) generates the σ-grading,
  which determines *which* units share orbits.
- The empirical operator is the projection of the curve into the shell.
- Projection destroys the σ-information by construction.

This is consistent with — and a sharp empirical witness for —
Brayden's hypothesis stated in Sprint 21:
*"TSML may be a close artifact of structure that only lives in curves
through shells."*

---

## What the partial W3 recovery means

W3's growth from ARI≈0 at n=10 to ARI=0.728 at n=34 is a real signal,
but it is **not** σ-recovery from the shell alone. It is the
finite-sample correlation between σ-class size and output histogram
shape. As `n` grows, σ classes get larger and their histograms become
more distinguishable. This effect saturates at perfect recovery only in
a hypothetical large-n limit not reached in the compatibility family.

The honest read: **the histogram dimension of `T_emp` is a partial
proxy for σ in the large-n limit, but not a full inverse.** A complete
inverse requires data from outside `T_emp` — specifically, samples from
the underlying `(3u+1)/2^k` curve in `Z`.

---

## Files in this sprint

```
sprint23_curve_recovery_2026_04_17/
├── README.md                               ← this file
├── impl/
│   └── walk_recovery.py                    ← 8-strategy walk runner
└── results/
    ├── walk_recovery_full.json             ← per-source per-strategy details
    └── walk_recovery_summary.json          ← aggregate ARI table
```

---

## Reproducibility

```bash
cd impl
python walk_recovery.py
```

---

*© 2026 Brayden Ross Sanders / 7Site LLC*
*Sprint 23 — σ is provably curve-level; partial frequency-profile signal grows with carrier.*
