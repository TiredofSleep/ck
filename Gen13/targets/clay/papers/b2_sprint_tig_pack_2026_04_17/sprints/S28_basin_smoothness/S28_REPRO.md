# S28 Reproducibility
## Sprint 28 — How to Rerun

---

## Spec Reference

Implementation strictly follows `S28_PREREG_v1.0.md`. No spec amendments.

---

## Environment

- Python 3.11+
- NumPy (for `np.random.default_rng`, `np.mean`, `np.std`, `np.full`, `np.sum`, arithmetic)
- Standard library: `json`, `csv`, `math.gcd`

No other dependencies. No network access required.

---

## Files

Single script located at `/home/claude/sprint28/s28_run.py`.

Outputs in the same directory:
- `S28_CURVE_DATA.csv` — one row per carrier with $n$, $h$, $\beta$, `in_band`, adjacent step.
- `S28_NULL_DATA.csv` — one row per (carrier, scramble_id) with $n$, scramble id, $h^\text{scr}$, $\beta^\text{scr}$, whether random $h$ matched the rule.
- `S28_SCORES.json` — metrics, thresholds, null statistics, sub-conditions, verdict.

---

## Random Seed Handling

Single seed: `NULL_SEED = 28` (hardcoded, per §4 frozen spec).

The entire null process — 100 scrambles × 29 carriers × 2 random draws per carrier (h_scr and sigma_scr) = 5800 uses of the RNG — is driven by `numpy.random.default_rng(28)`. The sequential use pattern is:

```
for s_id in range(100):
    for n in CARRIERS:
        h_scr = rng.integers(0, n)
        for u in units(n):
            sigma_scr[u] = rng.integers(1, 3)
        # compute basin ratio
```

Given the same NumPy version and seed, output is deterministic and bit-exact reproducible.

No randomness in the real-curve computation — `max_odd_unit(n)` is deterministic; `shell_v2` is deterministic; `canonical_C0` is deterministic.

---

## Command to Rerun

```bash
cd /home/claude/sprint28
python3 s28_run.py
```

Expected runtime: under 5 seconds on standard hardware. Output is printed to stdout; files are written to the current directory.

---

## Verification Hooks

After running, verify:

- `S28_SCORES.json["spec_version"] == "S28-v1.0"`
- `S28_SCORES.json["null_seed"] == 28`
- `S28_SCORES.json["n_carriers"] == 29`
- `S28_SCORES.json["n_scrambles"] == 100`
- `S28_SCORES.json["metrics"]["A"] == 1.0`
- `S28_SCORES.json["metrics"]["B_band"] == 1.0`
- `S28_SCORES.json["metrics"]["C_smooth"]` is `0.056406` (to 6 decimal places)
- `S28_SCORES.json["derived"]["C_smooth_sigma_separation"] == -3.3468…` (negative; i.e., real is less smooth than null)
- `S28_SCORES.json["verdict"] == "FAIL"`

If any of these diverge, do not proceed — either the environment (NumPy version) differs or the code has been modified.

---

## What Cannot Be Changed Without a Spec Bump

Per §6 anti-tuning rules in S28-v1.0:

- The 29-carrier list.
- The band [0.60, 0.95].
- The smoothness threshold 0.10.
- The null scrambling procedure.
- The seed value 28.
- The pass threshold values in §5.1.

Any change constitutes S28-v1.1 or higher and requires re-running against a new spec document. Results scored against v1.0 cannot be retroactively re-classified.

---

## Full Command Pipeline

```bash
# Clean workspace
rm -f /home/claude/sprint28/S28_CURVE_DATA.csv \
      /home/claude/sprint28/S28_NULL_DATA.csv \
      /home/claude/sprint28/S28_SCORES.json

# Run
cd /home/claude/sprint28
python3 s28_run.py

# Inspect
cat S28_SCORES.json
head -10 S28_CURVE_DATA.csv
head -5 S28_NULL_DATA.csv
```

---

## Integrity

- The script uses no external inputs other than the hardcoded carrier list (matching §2 of pre-registration exactly).
- The script outputs the verdict based solely on the frozen thresholds — no human judgment in the run.
- The script does not consult any ground-truth or reference file at runtime (there is no ground truth for this kind of test; the canonical construction is self-contained).

---

## If Rerun Gives a Different Verdict

The implementation is fully deterministic; divergence would indicate:

1. NumPy version mismatch (very rare at this level — `default_rng` is stable).
2. Hardware floating-point differences (should not affect integer-valued operations).
3. Code modification.

No legitimate source of variation exists. The verdict FAIL is the single result this specification produces on this seed.
