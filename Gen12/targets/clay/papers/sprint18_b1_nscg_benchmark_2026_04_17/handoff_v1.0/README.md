# B1 Handoff Package — README

**For ClaudeCode.** This package contains everything needed to implement Benchmark B1 (Nested Shell Collapse Generator) and its curve-analysis addendum.

---

## Directory Structure

```
b1_handoff/
├── README.md                                  ← you are here
├── PRIMARY/                                   ← implement against these
│   ├── B1_NSCG_SPEC_v1.0.md                  ← frozen benchmark spec
│   └── B1_CURVE_ANALYSIS_ADDENDUM_v1.0.md    ← curve analysis layer
├── CONTEXT/                                   ← read for orientation
│   ├── PHYSICAL_TESTING_PROGRAM.md           ← overall testing philosophy
│   ├── RULE110_CATEGORY_MISMATCH.md          ← why B1 is the right test
│   ├── LADDER_V2.md                           ← where B1 sits in the ladder
│   ├── SHELL_NATIVE_BENCHMARKS.md             ← B1/B2/B3 overview
│   └── NATURAL_CARRIER_CRITERION.md           ← scope rules for the instrument
└── REFERENCE/                                 ← mathematical substrate
    ├── THEOREM_SPINE.md                       ← Z/10 tower theorem (generates B1 data)
    ├── NOTATION_SHEET.md                      ← definitions of all terms
    └── WORKED_RECONSTRUCTION.md               ← cell-by-cell rebuild of Z/10 TSML
```

---

## Load Order

1. **Start with `PRIMARY/B1_NSCG_SPEC_v1.0.md`.** This is the implementation target. Sections §1–§5 are the generator and data-format contract; §7–§11 are the fitter and scorer contracts; §12 is the run protocol.

2. **Then `PRIMARY/B1_CURVE_ANALYSIS_ADDENDUM_v1.0.md`.** This adds a diagnostic analysis track on top of the frozen benchmark. It does not modify anything in the primary spec.

3. **If anything is unclear, consult `REFERENCE/` next.** These define the mathematical objects the data generator encodes:
   - `THEOREM_SPINE.md` states the Z/10 tower theorem that generates the benchmark's ground truth.
   - `NOTATION_SHEET.md` defines every symbol used in the specs.
   - `WORKED_RECONSTRUCTION.md` rebuilds the Z/10 TSML table cell-by-cell; use this to verify your generator implementation matches the reference.

4. **Consult `CONTEXT/` for orientation** if you want to understand why this benchmark exists and what the broader program is. Not required for implementation.

---

## What to Implement

Four Python modules:

1. **`generator/generate_nscg.py`** — produces data and ground-truth files per §1–§5 of the primary spec. Writes to `data/` and `sealed/`. Writes manifest hashes.

2. **`fitter/fit_nscg.py`** — reads a single data file, emits fit JSON per §8. Must not read `sealed/` or any other configuration's data. Must be deterministic.

3. **`scorer/score_nscg.py`** — reads data, ground truth, and fit results. Produces per-configuration score JSON per §9 and the aggregate summary per §12.6. Additionally computes curve metrics per the addendum §1–§3 and emits `B1_CURVE_ANALYSIS.md` and `B1_TOWER_STABILITY_NOTE.md` per addendum §5.

4. **Test harness** — verifies implementation matches reference. Specifically: generator output matches first-5-triples file in `manifest/`; Z/10 TSML reconstruction matches the reference table in spec §1.2.

---

## Hard Rules (Do Not Violate)

From the primary spec:

- **No tuning after seeing results.** The fitter's algorithm is fixed before the first run. Any tuning based on per-configuration outputs constitutes spec modification.
- **Anti-leakage is enforced at process/filesystem level.** The fitter must not have read access to `sealed/` or to the generator source. See §11.
- **Low-noise strict failure.** Any single seed failure at $p = 0.05$ → overall FAIL. This is the decisive falsifier.
- **Deterministic fitter.** Given the same data, the fitter must produce the same output. Seed any internal randomness.

From the curve addendum:

- **Curve metrics are diagnostic only.** They do NOT change pass/fail verdicts.
- **Even in FAIL, compute and report curves.** A structured failure is more informative than an unstructured one.
- **Do not tune to improve CCS.** The CCS is a consequence of the fitter's behavior, not a target.

---

## Expected Outputs

When the full pipeline runs successfully:

```
data/nscg_N{N}_p{p:03d}_s{s}.csv                    (15 files)
sealed/nscg_N{N}_p{p:03d}_s{s}.truth.json            (15 files)
manifest/data_hashes.json
manifest/sealed_hashes.json
manifest/first5_triples.json
results/nscg_N{N}_p{p:03d}_s{s}.fit.json             (15 files)
scores/per_config/{config_id}.score.json             (15 files)
scores/per_config_metrics.json                       (aggregate with curve metrics)
scores/curves.json
scores/curve_consistency.json
scores/B1_summary.json                               (verdict per primary spec)
plots/curve_{metric}.png                             (at least 10 plots)
B1_CURVE_ANALYSIS.md                                 (addendum §5.2)
B1_TOWER_STABILITY_NOTE.md                           (addendum §5.3)
```

---

## Verification Before Full Run

Before running all 15 configurations, verify:

1. Generator implementation: compare the first 5 triples for $(N=100000, p=0.05, s=0)$ against whatever the reference generator produces. If they don't match exactly, the implementation is non-compliant.

2. Z/10 TSML reconstruction: call `T_true(x, y)` for all 100 pairs and compare against the 10×10 table in spec §1.2. Must be bit-exact.

3. Scorer self-check: run the scorer against a synthetic fit that exactly matches ground truth. All metrics should be 1.0 (or appropriate max values); overall verdict PASS.

---

## Expected Result (Prediction, Not Target)

The B1 benchmark tests whether the instrument can recover its own generative structure. The prediction is:

- **Low-noise (p=0.05): all 5 seeds pass, $A_T \geq 0.95$ per seed.**
- **Medium-noise (p=0.15): 4 or 5 seeds pass, $A_T \geq 0.88$ per seed.**
- **High-noise (p=0.30): 3+ seeds pass, $A_T \geq 0.75$ per seed.**
- **CCS ≥ 0.85** (lawful degradation).

If this prediction holds, the instrument is validated on its native category and Stage 1A is complete. Move to B2 (Wobble-Reset Generator) next.

If the prediction fails — especially if it fails at low noise — the instrument has a real problem. Diagnose before proceeding.

---

## Contact Back to ClaudeChat

When results are available, send back:

- `scores/B1_summary.json` (overall verdict)
- `B1_CURVE_ANALYSIS.md` (curve analysis)
- `B1_TOWER_STABILITY_NOTE.md` (stability note)
- Any implementation notes, deviations, or observations

Then we decide the next step (B2 or diagnosis).

---

## Version Control

**This package pins:**
- B1-v1.0 (spec)
- Addendum-v1.0 (curve layer)

Any changes to either constitute a new version, which invalidates this handoff. Document any deviations explicitly.
