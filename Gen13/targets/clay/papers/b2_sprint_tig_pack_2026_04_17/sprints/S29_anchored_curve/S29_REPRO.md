# S29 Reproducibility
## Sprint 29 — How to Rerun

---

## Spec Reference

Implementation strictly follows `S29_PREREG_ANCHORED_CURVE.md`. Supporting documents: `ANCHOR_DISTANCE_DEFINITION.md`, `NULLS_V2.md`. No spec amendments.

---

## Environment

- Python 3.11+ (tested on 3.12).
- NumPy (for `numpy.random.default_rng`, array ops, statistics).
- Standard library: `json`, `csv`, `math.gcd`.

No other dependencies. No network access required.

---

## Files

Single script at `/home/claude/sprint29/s29_run.py`.

Outputs in the same directory:
- `S29_CURVE_DATA.csv` — 29 rows: $n$, $|U|$, $d_1$, $h$, $\beta$, $D$, in-cap flag.
- `S29_NULL_DATA.csv` — 2,900 rows: $n$, scramble_id, $h^\text{scr}$, $\beta^\text{scr}$.
- `S29_SCORES.json` — metrics, thresholds, null statistics, sub-conditions, verdict.

---

## Random Seed Handling

Single seed: `NULL_SEED = 29` (hardcoded per S29 §4 / NULLS_V2 N1).

The null process uses `numpy.random.default_rng(29)` and draws:
- 100 scrambles × 29 carriers × 1 random draw per carrier (index into $U(n)$) = 2,900 uses of `rng.integers`.

Sequential order is scramble-outer, carrier-inner:
```
for s_id in range(100):
    for n in CARRIERS:
        h_scr_idx = rng.integers(0, len(units(n)))
        h_scr = units(n)[h_scr_idx]
```

No other randomness anywhere. The real-curve computation is fully deterministic: `max_odd_unit`, `shell_v2`, `canonical_C0` are pure integer functions.

Given the same NumPy version and seed, output is bit-exact reproducible.

---

## Command to Rerun

```bash
cd /home/claude/sprint29
python3 s29_run.py
```

Expected runtime: under 3 seconds on standard hardware. Console output matches the reported results; CSV and JSON files are written to current directory.

---

## Verification Hooks

After a rerun, verify:

- `S29_SCORES.json["spec_version"] == "S29-v1.0"`
- `S29_SCORES.json["null_seed"] == 29`
- `S29_SCORES.json["n_carriers"] == 29`
- `S29_SCORES.json["n_scrambles"] == 100`
- `S29_SCORES.json["anchor_n"] == 10`
- `S29_SCORES.json["anchor_beta"]` ≈ 0.79
- `S29_SCORES.json["metrics_real"]["M1_kendall_tau"]` ≈ 0.0629 (within float tolerance)
- `S29_SCORES.json["metrics_real"]["M2_linear_r2"]` ≈ 0.0000 (very near 0)
- `S29_SCORES.json["metrics_real"]["M3_carriers_in_cap"] == 29`
- `S29_SCORES.json["derived"]["tau_sigma_separation"]` ≈ 0.60
- `S29_SCORES.json["derived"]["r2_sigma_separation"]` ≈ −0.79
- `S29_SCORES.json["verdict"] == "FAIL"`

If any diverge, the environment or code has changed from this spec.

---

## What Cannot Be Changed Without a Spec Bump

Per S29-v1.0 §7 anti-tuning rules:
- 29-carrier list.
- Anchor choice ($R_{10}$).
- Primary distance $d_1 = |U(n)| - 4$.
- Response quantity $D = |\beta - \beta_\text{anchor}|$.
- Kendall tau for M1 (no switching to Spearman/Pearson).
- Linear fit for M2 (no nonlinear substitutes).
- Boundedness cap 0.25 for M3.
- Thresholds (tau 0.35, $R^2$ 0.40, M3 count 27, sigma 2.0).
- Null model (N1 primary, unit-valued attractor, canonical $\sigma$).
- Null seed 29.

Any change requires S29-v1.1+ and a fresh run against that new spec.

---

## Full Command Pipeline

```bash
# Clean workspace
rm -f /home/claude/sprint29/S29_CURVE_DATA.csv \
      /home/claude/sprint29/S29_NULL_DATA.csv \
      /home/claude/sprint29/S29_SCORES.json

# Run
cd /home/claude/sprint29
python3 s29_run.py

# Inspect
cat S29_SCORES.json
head -10 S29_CURVE_DATA.csv
head -5 S29_NULL_DATA.csv
```

---

## Integrity

- No external inputs other than the hardcoded carrier list (matching S29 §2 and S28's list exactly).
- Verdict driven solely by frozen thresholds applied to computed quantities.
- No ground-truth file — the canonical construction is self-contained and deterministic.
- No re-evaluation with alternative metrics or depth coordinates within this sprint.

---

## If Rerun Gives a Different Verdict

The implementation is fully deterministic. Any divergence would indicate:

1. NumPy version mismatch in `default_rng` (stable across 1.17+; unlikely to matter at this level).
2. Hardware floating-point differences (not expected to flip any condition — the real values fail by wide margins).
3. Code modification.

No legitimate variation source exists. The FAIL verdict is the single result this specification produces on seed 29.

---

## Cross-Sprint Comparison

| Spec | Seed | Null type | Primary metric | Verdict |
|---|---|---|---|---|
| S28-v1.0 | 28 | Full-range integer attractor | $C_\text{smooth}$ (adjacent smoothness) | FAIL |
| S29-v1.0 | 29 | Unit-valued attractor only | Kendall tau + linear $R^2$ | FAIL |

Two sprints, two frozen pre-registrations, two FAIL verdicts, two independent records. Both stand.
