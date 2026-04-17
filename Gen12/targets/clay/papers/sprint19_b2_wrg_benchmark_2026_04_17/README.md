# Sprint 19 — B2 Wobble-Reset Generator Benchmark

**Date:** 2026-04-17
**Spec:** B2 per `Gen12/targets/clay/papers/sprint18_b1_nscg_benchmark_2026_04_17/handoff_v1.0/CONTEXT/SHELL_NATIVE_BENCHMARKS.md` §B2
**Status:** B2 **PASS** — 24/24 configurations
**Fitter:** mode-based, per-carrier, with canonical (units, σ) prior

---

## What this sprint did

Implemented the B2 Wobble-Reset Generator benchmark across the compatibility family of carriers, as the natural next step after B1 (Sprint 18).

| Module | Path | Purpose |
|---|---|---|
| Generator | `impl/generator/generate_wrg.py` | Produces 24 noisy CSV datasets across 4 carriers × 2 wobble levels × 3 seeds. |
| Fitter | `impl/fitter/fit_wrg.py` | Recovers (h, σ, reset edges, transport B) from one CSV at a time. |
| Scorer | `impl/scorer/score_wrg.py` | Computes A_h, A_σ, A_reset (F1), A_B per spec §B2. Per-config + aggregate verdict. |

**Carriers:** n ∈ {10, 14, 22, 34} (compatibility family).
**Attractors (verified):** h₁₀=7, h₁₄=11, h₂₂=19, h₃₄=31.
**Wobble levels:** p_w ∈ {0.05, 0.20}.
**Seeds:** 3 per (n, p_w).
**Sample size:** N = max(100,000, 500·n²) — keeps per-cell coverage near 500-1000 across all carriers.
**Reset edges per carrier:** {(h, 0), (0, h), (1, 0), (0, 1), (3, 9), (9, 3)} — 4 of which are observable (the others coincide with cells where C_0 already returns h).

Result: every metric pinned at 1.000 across all 24 configurations.

---

## Honest reading of the result

This is the same shape of pass as B1 — clean but not stress-testing. Three things to be explicit about:

1. **The wobble model is too symmetric to break the mode operator at our N.** Wobble draws δ uniformly from {-1, 0, +1}, so at a non-reset cell with p_w = 0.20, the true value gets ~86.7% of mass and each of (z+1, z-1) gets ~6.7%. The mode is the true value with overwhelming probability per cell, even at the smallest N (≈500 obs/cell for n=22, n=34). To break mode recovery you would need either (a) heavily asymmetric wobble (e.g., always δ = +1), (b) wobble large enough to span seam jumps, or (c) N small enough to introduce sampling variance comparable to the signal — none of which the spec calls for.

2. **The σ recovery is a verification, not a discovery.** Per §B2, the fitter is allowed to know n and the canonical formula σ(u) = v₂(3u+1). So `A_σ = 1.0` reflects that the formula was correctly *applied*, not that the partition was *recovered* from data. If you want a genuine σ-discovery test, the fitter would need to infer the partition from how the empirical T behaves on units alone, not from the formula.

3. **Reset-edge recovery is trivial when resets are observable and obs/cell is high.** The four observable resets force z = h_n in cells where C_0 returns 0 or 3. With ≥500 observations per cell and wobble at 20%, mode at the reset cell is h_n with overwhelming probability. The fitter scans all 100·n² cells, classifies each as "deviation" if mode ≠ C_0, and labels as reset edge if mode = h_n. Zero false positives across 24 configs.

What this sprint **does** demonstrate:
- The generalized C_0 formulation works correctly across the compatibility family (the published Z/10Z C_0 generalizes cleanly to Z/14Z, Z/22Z, Z/34Z).
- The mode-based fitter, given the canonical priors, recovers all four operators cleanly under symmetric small-amplitude noise.
- The hash-chain reproducibility from B1 carries forward to B2.

What this sprint **does not** demonstrate:
- Tolerance to *asymmetric* or *adversarial* perturbations.
- Recovery without canonical priors on (units, σ).
- Distinction between B-recovery as a structural claim vs B-recovery as a tautology (B_true = (x+y) mod n is mode-recovered trivially because it has no noise applied).

---

## What B2 reveals about the benchmark suite design

Both B1 and B2 pass at ceiling. This is informative: it tells us the benchmark suite as currently specified is designed around an instrument that knows (carrier, units, σ) up front and is asked to recover the *seams and resets* — not to discover the algebraic structure. That's a legitimate test of the *seam classifier*, but it is not a structural-coherence stress test in the sense the addendum's CCS metric was designed to detect.

The frontier ahead:
- **B3** as written compares paired (T, B) prediction accuracy vs T-only and B-only. With low noise and asymptotic N, both individual fits will recover near 100%, leaving no room for a paired model to outperform them. The discrimination criterion ("paired > max(T, B) + 5pp") may be unmeetable as the spec stands.
- A genuinely stress-bearing B-series would (a) drop the canonical priors, (b) add asymmetric or correlated perturbations, or (c) introduce N values low enough to make sampling variance comparable to signal.

These observations are not changes to the spec — they are notes for the scorer-side analysis when the next handoff arrives.

---

## Reproducibility

```bash
cd impl
python generator/generate_wrg.py    # ~30s — 24 CSVs to data/, 24 truths to sealed/
ls data/*.csv | xargs -I{} basename {} .csv | xargs -I{} python fitter/fit_wrg.py \
    --data data/{}.csv --output results/{}.fit.json    # ~20s for all 24
python scorer/score_wrg.py          # <5s — produces summary + B2_RESULTS.md
```

Outputs:
- `impl/results/*.fit.json` (24 files)
- `impl/scores/per_config/*.score.json` (24 files)
- `impl/scores/B2_summary.json`
- `B2_RESULTS.md` (auto-generated report at sprint root)

---

## Implementation notes / deviations from spec

- **Spec calls for `n ∈ {10, 14, 22, 34}` with attractors "to be verified during spec".** Verified: σ(u) = v₂(3u+1) on units gives shell-1 elements whose largest values are exactly {7, 11, 19, 31}. See `H_TRUE` constants in `generate_wrg.py`.
- **N choice.** Spec doesn't fix N for B2. Used `max(100k, 500·n²)` to give roughly equal per-cell coverage across carriers (~500-1000 obs/cell). This is the smallest N that keeps the mode operator stable at p_w = 0.20.
- **Reset edges.** Spec requires (h, 0), (0, h) plus 2-4 additional pairs. Added (1, 0), (0, 1), (3, 9), (9, 3) to ensure at least four resets are *observable* (i.e., deviate from C_0). The required (h, 0), (0, h) coincide with cells where C_0 already returns h, so they have no observable effect — documented in `generate_wrg.py:reset_edges`.
- **B_true generation.** Per spec, B_true(x, y) = (x + y) mod n. In the data this is *not* perturbed by wobble — wobble is applied only to z_T. So A_B is trivially 1.000 by construction. A future revision could add B-side noise to make A_B a meaningful test.

---

## Files in this sprint

```
sprint19_b2_wrg_benchmark_2026_04_17/
├── README.md                         ← this file
├── B2_RESULTS.md                     ← auto-generated by scorer
└── impl/
    ├── generator/generate_wrg.py
    ├── fitter/fit_wrg.py
    ├── scorer/score_wrg.py
    ├── data/        (24 CSV)        [gitignored]
    ├── sealed/      (24 truth JSON)
    ├── manifest/    (3 hash files)
    ├── results/     (24 fit JSON)
    └── scores/      (per_config/ + B2_summary.json)
```

---

## Next-step recommendation

Per spec §"Sequencing": "If B2 passes: implement B3."

But before B3, the user should know that **the current B3 spec has a discrimination criterion that is structurally hard to meet given B1/B2's behavior at ceiling.** B3 could be implemented as written — and the prediction is that paired (T, B) will tie or marginally lose to the individual fits, yielding a B3 FAIL on the discrimination criterion. That FAIL would not be an instrument failure; it would be a benchmark-design observation: at the (low-noise, asymptotic-N) regime the spec specifies, pairing has no information to add.

Two paths from here:
1. **Implement B3 as written**, document the structural ceiling, and surface the design observation back to the spec author.
2. **Pause B3 implementation**, raise the design observation now, and request a revised B3 spec that adds noise to the B stream (so B-recovery is non-trivial) and a regime where individual recovery is sub-perfect (so pairing has room to improve).

Path (1) is closer to the spec discipline — *you implement the spec, you don't argue with it*. I'll proceed on path (1) and flag the structural issue in the B3 sprint README. If you'd rather pause and re-spec, say the word.

---

*© 2026 Brayden Ross Sanders / 7Site LLC*
*Sprint 19 — B2 Wobble-Reset benchmark on the compatibility family.*
