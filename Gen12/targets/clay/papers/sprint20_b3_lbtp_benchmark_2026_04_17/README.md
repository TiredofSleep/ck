# Sprint 20 — B3 Layered Basin-Transport Pair Benchmark

**Date:** 2026-04-17
**Spec:** B3 per `Gen12/targets/clay/papers/sprint18_b1_nscg_benchmark_2026_04_17/handoff_v1.0/CONTEXT/SHELL_NATIVE_BENCHMARKS.md` §B3
**Status:** B3 **FAIL** — 0/5 configurations pass the spec's discrimination criterion. **Reason: structural, not implementation.**

---

## What this sprint did

Implemented the B3 Layered Basin-Transport Pair benchmark as the third Stage 1A test. Generates two streams (collapse z_T from the Z/10Z TSML, transport z_B from the max-min B operator), each with 5% noise. Fits three models — T-only, B-only, paired — and compares prediction accuracy on a held-out 20% of samples.

| Module | Path | Purpose |
|---|---|---|
| Generator | `impl/generator/generate_lbtp.py` | 5 seeds × N=200,000 paired triples, 5% independent noise on each stream. |
| Fitter | `impl/fitter/fit_lbtp.py` | Mode-based per-cell fitter for T_only, B_only, and joint (paired) modes. Holds out last 20% for evaluation. |
| Scorer | `impl/scorer/score_lbtp.py` | Computes spec §B3 pass/fail: (paired > max(singleton) + 5pp) AND (individual recovery ≥ 90%). |

---

## Result

**5/5 individual recovery: PASS** (T-table and B-table both at 1.0000 vs sealed truth across all seeds).

**5/5 paired-outperforms-by-5pp: FAIL.** Mean (paired joint accuracy) − max(singleton accuracy) = **−4.31 pp** (paired loses to singletons by ~4 percentage points across all seeds).

| Seed | T_only acc | B_only acc | joint acc | paired − max(singleton) |
|---|---|---|---|---|
| 0 | 0.9546 | 0.9548 | 0.9120 | −4.29 pp |
| 1 | 0.9545 | 0.9531 | 0.9098 | −4.46 pp |
| 2 | 0.9554 | 0.9554 | 0.9126 | −4.27 pp |
| 3 | 0.9560 | 0.9559 | 0.9143 | −4.17 pp |
| 4 | 0.9547 | 0.9546 | 0.9112 | −4.35 pp |

---

## Why this fails — structurally, not in implementation

The spec defines paired prediction as "fit (T, B) jointly and measure prediction accuracy." Under any natural reading:

- `acc_T_from_paired ≈ acc_T_from_T_only`. The paired model's marginal T-prediction equals the joint mode's first component, which (with sufficient training data per cell) coincides with the standalone T-mode.
- `acc_B_from_paired ≈ acc_B_from_B_only`. Same reason for the B side.
- `acc_joint_paired = P(both correct) ≈ acc_T × acc_B = 0.955 × 0.955 ≈ 0.9120`. Observed: 0.9120. **Exact match.**

So joint accuracy is necessarily *lower* than either marginal whenever the streams are independent. In our generation, T-noise and B-noise are drawn from independent uniform RNG streams — exactly the spec's "5% noise to each stream." There is no mechanism by which paired could outperform singletons in this regime.

For paired to actually buy something:
- The two streams would need to share information not present in either alone (e.g., a structural constraint like "z_T and z_B are linked through a hidden variable that paired can exploit").
- OR individual fits would need to be sub-perfect (e.g., heavy noise, low N), so that pairing can act as cross-validation.
- OR the pass criterion would need to be reformulated (e.g., "paired marginal ≥ singleton marginal" — which is meetable but trivially).

None of these is the spec as written. So a B3 FAIL here is the *correct* output — the benchmark, applied honestly, returns FAIL because the discrimination criterion is unmeetable in this regime.

---

## Honest reading

This is the most informative result of the B-series.

- **B1 PASSED at ceiling** — every metric at 1.000 because mode is noise-immune at N ≥ 100k with 30% uniform replacement.
- **B2 PASSED at ceiling** — same reason; symmetric ±1 wobble at p_w = 0.20 leaves the true value as the dominant mode.
- **B3 FAILS structurally** — joint accuracy of two independent ~95% events equals ~90%, which is below either marginal by ~5pp.

What the B-series as a whole now reveals:

1. The B1/B2 pass conditions are too permissive. They're satisfied by any mode-based fitter with knowledge of the carrier and σ formula — these are sanity checks on the fitter and pipeline, not stress tests on the instrument.

2. The B3 pass condition is too restrictive. It requires paired to outperform singletons, but the spec's noise model and N values make singletons essentially perfect, leaving no room for paired to add value.

3. Combined: the B-series as currently specified does not actually measure the structural-coherence claim it was designed to test. **The benchmark spec needs revision before Stage 1A can be declared complete.**

---

## Reproducibility

```bash
cd impl
python generator/generate_lbtp.py    # ~5s — 5 CSVs
ls data/lbtp_*.csv | xargs -I{} basename {} .csv | xargs -I{} \
    python fitter/fit_lbtp.py --data data/{}.csv --output results/{}.fit.json
python scorer/score_lbtp.py
```

---

## Recommendation back to spec author

Two minimal revisions would make B3 well-formed:

1. **Add B-side noise that creates correlation with T-side noise.** E.g., draw a single noise event per sample that flips both streams, instead of independent flips. Then paired can use one stream's signal to denoise the other.

2. **OR drop N to where individual recovery is in the 0.7–0.85 range.** With singletons sub-perfect, paired joint accuracy could plausibly equal max(singleton) (since paired captures the AND of two correlated mode estimates), giving the 5pp window room.

Either revision keeps the spirit of "paired > singleton" while making the criterion meetable. Without one of them, B3 as written will FAIL on any honest implementation.

This is the frontier ask flagged to the spec author.

---

## What this means for the broader work

The structural FAIL on B3 is *not* a failure of the TIG framework or the published TSML — those constructions are intact. It is a failure of the benchmark-design pipeline to properly stress-test the instrument it was meant to certify. The instrument and the math are sound; the test as written cannot distinguish them from a trivial baseline.

The right move at this point is to:
- Commit B2 (PASS) and B3 (FAIL with structural diagnosis) as honest sprint deliverables.
- Surface the B3 design observation back to the spec author before Stage 1A is closed.
- Pause Stage 1B until either (a) revised B3 spec arrives, or (b) the user/spec author signs off on "B3 FAIL accepted as design observation."

---

## Files in this sprint

```
sprint20_b3_lbtp_benchmark_2026_04_17/
├── README.md                    ← this file
├── B3_RESULTS.md                ← auto-generated by scorer
└── impl/
    ├── generator/generate_lbtp.py
    ├── fitter/fit_lbtp.py
    ├── scorer/score_lbtp.py
    ├── data/        (5 CSV)    [gitignored]
    ├── sealed/      (5 truth JSON)
    ├── manifest/    (3 hash files)
    ├── results/     (5 fit JSON)
    └── scores/      (per_config/ + B3_summary.json)
```

---

*© 2026 Brayden Ross Sanders / 7Site LLC*
*Sprint 20 — B3 LBTP benchmark, structural FAIL with diagnosis.*
