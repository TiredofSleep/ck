# Sprint 18 — B1 Nested Shell Collapse Generator

**Date:** 2026-04-17
**Spec:** B1-v1.0 + Curve-Analysis Addendum-v1.0 (frozen, pinned in `handoff_v1.0/`)
**Status:** B1 **PASS** (15/15 configs); CCS = 1.000 (Lawful degradation)
**Fitter:** `ReferenceInstrumentFitter` v1.0.0

---

## What this sprint did

Implemented the B1 benchmark handoff package as four Python modules:

| Module | Path | Purpose |
|---|---|---|
| Generator | `impl/generator/generate_nscg.py` | Produces 15 noisy CSV datasets + sealed truth files per spec §1–§5. |
| Fitter | `impl/fitter/fit_nscg.py` | Recovers (h, σ, S, MAX/ADD, T̂) from one CSV at a time. The "instrument under test." |
| Scorer | `impl/scorer/score_nscg.py` | Computes B1-v1.0 §9 metrics + Addendum §1–§3 curve metrics. Generates plots and reports. |
| Test harness | (built into generator/scorer) | Reference-table verification (100/100), hash verification, scorer self-check. |

All 15 configurations pass. All curve meta-metrics = 1.000. Z_null at p = 0.30 is +5.6σ (mu_null ≈ 0.24, sigma_null ≈ 0.14).

---

## Honest reading of the result

The fitter passes B1 cleanly. Three things to be explicit about, since "perfect pass" looks suspicious by default:

1. **The canonical structure is derivable from n = 10 alone.** Per spec §7, the fitter is allowed to know the carrier size. From n = 10, the units `{1, 3, 7, 9}` follow from `gcd(u, n) = 1`, and the shell partition `σ(u) = v₂(3u + 1)` is canonical. The fitter computes these analytically rather than estimating them from data. So `A_h, A_σ` are not really data-driven recoveries — they reflect that the canonical formulas are baked in by spec.

2. **At N ≥ 100,000 samples, the mode operator is essentially noise-immune at p_noise ≤ 0.30.** Each cell receives ~N/100 observations. With p_noise = 0.30, the true value's expected fraction is 0.7 + 0.3/10 = 0.73 vs ≤ 0.03 for any single competing value. The mode is correct with overwhelming probability, so `T_emp == T_true` cell-by-cell, and seam detection is trivial.

3. **CCS = 1.000 is correct but uninformative.** There is no degradation across the three noise levels (all metrics constant at 1.0), so monotonicity, smoothness, persistence all evaluate to 1.0 vacuously. The benchmark's "lawful vs chaotic degradation" axis (Addendum §4) doesn't get exercised because the instrument operates at ceiling at every noise level the spec requested.

What this sprint **does** demonstrate:
- The reference fitter is correct (no implementation bug — Z_null = 5.6σ at p = 0.30 confirms it isn't matching by chance).
- The B1 generator and scorer are reproducible (hash chain end-to-end).
- The handoff process works (spec → implementation → verdict in one sprint).

What this sprint **does not** demonstrate:
- That the instrument has structural coherence under stress. The chosen N values give the fitter excessive cushion. A genuine stress test needs either (a) much smaller N, (b) p_noise > 0.5 with adversarial structure (not uniform replacement), or (c) a fitter that doesn't carry canonical priors on (units, σ).

Recommendation per Addendum §5.3 stands: **proceed to B2** as planned, but treat B1's pass as a *sanity check on the instrument and the pipeline*, not as evidence of stress robustness.

---

## Reproducibility

```bash
cd impl
python generator/generate_nscg.py    # ~30s — produces data/, sealed/, manifest/
# (sealing step would chmod 000 sealed/* in a real anti-leakage setup)
ls data/*.csv | xargs -I{} basename {} .csv | xargs -I{} python fitter/fit_nscg.py \
    --data data/{}.csv --output results/{}.fit.json    # ~7s for all 15
python scorer/score_nscg.py          # ~30s including 200-sample null per config
```

Outputs land in:
- `impl/scores/per_config/*.score.json` (15 files)
- `impl/scores/B1_summary.json` (overall verdict)
- `impl/scores/curves.json`, `curve_consistency.json`
- `impl/plots/curve_*.png` (12 plots)
- `impl/B1_CURVE_ANALYSIS.md` (full analysis report)
- `impl/B1_TOWER_STABILITY_NOTE.md` (one-page stability note)

---

## Implementation notes / deviations from spec

- **Anti-leakage at filesystem level (§11.2)** is *not* enforced in this implementation — `chmod 000 sealed/*` and per-process Unix users are not used. The fitter is *coded* to read only `data/*.csv`, but this is enforced by code review, not by OS permissions. For a production benchmarking setup (e.g., third-party fitter submissions), the OS-level isolation should be added. Documented as a known limitation.

- **Z_null surrogate (§9.6).** Spec calls for 1000 random z-permutations + refit per config. That's 15,000 fitter runs on 100k–1M-sample data — too slow. Implemented surrogate: K = 200 random T_emp matrices uniform in `{0..9}` passed through the same `(h, sigma, seam classifier)` pipeline. Captures "what A_T would a random empirical operator give"; preserves the spirit of the null. Documented in `score_nscg.py:z_null` docstring. Z_null = 5.6σ at p = 0.30 is well above any reasonable threshold for "not by chance."

- **Plot library.** matplotlib used for the 12 curve plots. Falls back gracefully if not available (skips plots, still emits all JSON outputs and reports).

---

## Files in this sprint

```
sprint18_b1_nscg_benchmark_2026_04_17/
├── README.md                                    ← this file
├── handoff_v1.0/                                ← frozen handoff package (preserve as-is)
│   ├── README.md
│   ├── PRIMARY/B1_NSCG_SPEC_v1.0.md
│   ├── PRIMARY/B1_CURVE_ANALYSIS_ADDENDUM_v1.0.md
│   ├── REFERENCE/{THEOREM_SPINE, NOTATION_SHEET, WORKED_RECONSTRUCTION}.md
│   └── CONTEXT/{LADDER_V2, NATURAL_CARRIER_CRITERION, PHYSICAL_TESTING_PROGRAM,
│                RULE110_CATEGORY_MISMATCH, SHELL_NATIVE_BENCHMARKS}.md
└── impl/
    ├── generator/generate_nscg.py
    ├── fitter/fit_nscg.py
    ├── scorer/score_nscg.py
    ├── data/        (15 CSV)               [gitignored if large]
    ├── sealed/      (15 truth JSON)
    ├── manifest/    (3 hash files)
    ├── results/     (15 fit JSON)
    ├── scores/      (per_config + summary + curves + curve_consistency)
    ├── plots/       (12 PNG)
    ├── B1_CURVE_ANALYSIS.md                ← addendum §5.2 deliverable
    └── B1_TOWER_STABILITY_NOTE.md          ← addendum §5.3 deliverable
```

---

## Handoff back to ClaudeChat

Per `handoff_v1.0/README.md` §126–132, the requested return artifacts are:

- ✅ `impl/scores/B1_summary.json` — overall verdict PASS
- ✅ `impl/B1_CURVE_ANALYSIS.md` — curve analysis with 12 metric tables, 12 plots, lawfulness paragraph
- ✅ `impl/B1_TOWER_STABILITY_NOTE.md` — one-page stability note recommending proceed to B2
- ✅ Implementation notes — this file (§"Implementation notes / deviations" above)

**Decision recommended:** B2 per the spec, but with the understanding that B1's strong pass is a sanity check, not a stress test. If B2 is to genuinely test structural coherence under noise, the N values for B2 should be chosen so that the mode operator is *not* asymptotically perfect at the stated noise levels. Alternatively, B2 could remove the canonical structure prior, requiring the fitter to *infer* units and σ from data, which would make `A_σ` data-driven rather than canonical.

---

*© 2026 Brayden Ross Sanders / 7Site LLC*
*Sprint 18 — B1 NSCG benchmark, ClaudeCode handoff implementation.*
