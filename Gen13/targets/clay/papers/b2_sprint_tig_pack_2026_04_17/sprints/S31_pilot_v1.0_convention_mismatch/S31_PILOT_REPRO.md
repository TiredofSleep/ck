# S31 Pilot Reproducibility
## S31-pilot-v1.0 — How to Rerun

---

## Spec Reference

Implementation strictly follows `S31_Z10_PILOT.md`. No spec amendments.

---

## Environment

- Python 3.11+ (tested on 3.12).
- NumPy (for `numpy.random.default_rng` and array operations).
- Standard library: `json`, `csv`, `math.gcd`, `collections.Counter`.

No other dependencies. No network access required.

---

## Files

Single script at `/home/claude/sprint31_pilot/s31_pilot_run.py`.

Outputs in the same directory:
- `S31P_PER_SEED.csv` — per (overlay, noise, seed): seam size, seam edges.
- `S31P_PERSISTENT.json` — per (overlay, noise): planted seam, persistent seam, intersection, metrics, per-seed sizes.
- `S31P_SCORES.json` — per-condition metrics, sub-condition pass flags, marginal flags, verdict.

---

## Random Seed Handling

Two-layer seeding, fully deterministic:

1. Per-run seed formula:
$$\text{seed} = 31000 + 10000 \cdot \text{overlay\_idx} + 100 \cdot \text{noise\_idx} + r$$

where overlay_idx ∈ {NONE=0, MAX=1, ADD=2, MAX_ADD=3}, noise_idx ∈ {0.02=0, 0.10=1, 0.20=2}, r ∈ {0, …, 9}.

2. Per-run extraction uses `numpy.random.default_rng(seed)` with vectorized sampling:
```
xs = rng.integers(0, n, N)     # N = 1000
ys = rng.integers(0, n, N)
us = rng.random(N)
zs_noise = rng.integers(0, n, N)
```
Sequential draws from a single RNG → bit-reproducible across NumPy versions 1.17+.

Total per-run seeds: 4 overlays × 3 noise × 10 runs = 120 distinct seeds.

---

## Command to Rerun

```bash
cd /home/claude/sprint31_pilot
python3 s31_pilot_run.py
```

Expected runtime: ~1–2 seconds. Grid is small; each per-run extraction is microseconds.

---

## Verification Hooks

After rerun, verify in `S31P_SCORES.json`:

- `spec_version == "S31-pilot-v1.0"`.
- `carrier == 10`, `K_seeds == 10`, `pi_persist == 0.5`, `N_samples == 1000`.
- `data_seed_base == 31000`.
- `verdict == "FAIL"`.
- `per_condition["MAX_p0.02"]["J"] ≈ 0.6667` (4/6 exact).
- `per_condition["ADD_p0.02"]["J"] == 1.0`.
- `per_condition["MAX_ADD_p0.02"]["J"] == 0.75` (6/8 exact).
- `per_condition["NONE_p0.02"]["n_persistent"] == 0`.

For a spot check of the failure's noise-invariance:
- `per_condition["MAX_p0.02"]["J"] == per_condition["MAX_p0.1"]["J"] == per_condition["MAX_p0.2"]["J"]`.
- Same for MAX_ADD.

If any diverge, environment or code has changed from this spec.

---

## What Cannot Be Changed Without a Spec Bump

Per S31-pilot-v1.0 §9 anti-tuning rules:
- Carrier (Z/10).
- Overlay definitions (§3).
- Attractor $h = 9$ (inherited from "max odd unit" rule).
- Shell partition $\sigma(u) = v_2(3u+1)$.
- $N = 1{,}000$ per run.
- Noise levels $\{0.02, 0.10, 0.20\}$.
- $K = 10$ seeds.
- $\pi = 0.50$ persistence threshold.
- Data seed base 31,000 and seed formula.
- Mode tie-break (smallest $z$).
- Metric definitions (§7).
- Thresholds (§8).

Any change requires S31-pilot-v1.1+ and a fresh run.

---

## Full Command Pipeline

```bash
# Clean workspace
rm -f /home/claude/sprint31_pilot/S31P_PER_SEED.csv \
      /home/claude/sprint31_pilot/S31P_PERSISTENT.json \
      /home/claude/sprint31_pilot/S31P_SCORES.json

# Run
cd /home/claude/sprint31_pilot
python3 s31_pilot_run.py

# Inspect
cat S31P_SCORES.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['verdict'])"
head -20 S31P_PER_SEED.csv
```

---

## Integrity

- No external inputs other than hardcoded frozen parameters.
- No null model (this is a recovery pilot; see §7 of spec).
- Verdict driven solely by frozen thresholds applied to computed metrics.
- Fully deterministic given NumPy version and seed formula.
- No randomness in verdict logic.

---

## If Rerun Gives a Different Verdict

The FAIL verdict follows from structural properties:
- MAX and MAX+ADD overlays include cells $(2,9)$ and $(9,2)$.
- Under $h = 9$, both $C_0$ and the MAX overlay assign value 9 to these cells.
- Therefore empirical mode = $C_0$ = 9 on these cells, regardless of sampling or noise.
- Jaccard = 4/6 and 6/8 are arithmetic consequences, not statistical estimates.

Any rerun with the same frozen parameters will produce Jaccard values of exactly 0.6667 and 0.7500 on MAX and MAX+ADD at all three noise levels. Divergence would indicate:

1. Code modification.
2. Different attractor choice (violates §5 freeze).
3. Different overlay domain (violates §3 freeze).

No legitimate source of variation exists. The FAIL verdict is the deterministic output of this specification on this carrier.

---

## Cross-Sprint Comparison

| Spec | Seed base | Core question | Verdict |
|---|---|---|---|
| S28-v1.0 | 28 | Basin-ratio smoothness transport | FAIL |
| S29-v1.0 | 29 | Basin-ratio anchored trend | FAIL |
| S30-v1.0 | 30 | Empirical seam topology transport | PASS (vacuous) |
| S30b-v1.0 | 30000 | Seam detectability under uniform noise | FAIL |
| S31-pilot-v1.0 | 31000 | Known-chart seam recovery on Z/10 | FAIL (spec-design) |

Five sprints under discipline. Three genuine FAILs, one vacuous PASS, one spec-design FAIL whose informative failure mode exposed a convention mismatch. All recorded with full attribution, none reinterpreted.

The pattern is informative: each FAIL has taught something specific about what the tool can and cannot do. The S31-pilot failure uniquely identifies a pre-execution spec-writing oversight (two coexisting attractor conventions not reconciled). A successor pilot must resolve that before retesting recovery.
