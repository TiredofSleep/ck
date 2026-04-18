# S30b Reproducibility
## Sprint 30b — How to Rerun

---

## Spec Reference

Implementation strictly follows `S30B_PREREG_SEAM_DETECTABILITY.md`. Supporting documents: `SEAM_EXTRACTION_OPTIONS.md`. No spec amendments.

---

## Environment

- Python 3.11+ (tested on 3.12).
- NumPy for RNG (`numpy.random.default_rng`) and array operations.
- Standard library: `json`, `csv`, `math.gcd`, `itertools.combinations`.

No other dependencies. No network access required.

---

## Files

Single script at `/home/claude/sprint30b/s30b_run.py`.

Outputs in the same directory:
- `S30B_PERSISTENT_SEAMS.json` — per-carrier: mean seed size, persistent size, persistent edges, Jaccard, tie fraction.
- `S30B_PER_SEED_SEAMS.csv` — per (carrier, seed): seam size.
- `S30B_STABILITY.json` — per-carrier Jaccard and aggregate $\mu_J$.
- `S30B_SCORES.json` — aggregates, thresholds, sub-conditions, verdict.

---

## Random Seed Handling

Two layers of seeding, both deterministic:

1. **Data seed base:** `DATA_SEED_BASE = 30000` (frozen).
2. **Per-carrier per-run seed:** `seed = 30000 + 1000 * n + r` where `r` ∈ {0, 1, ..., 19}.

This gives each (carrier, seed_index) pair a unique, deterministic stream. Carriers' random streams do not collide: at $n = 10$, seeds are 30000–30019; at $n = 14$, seeds are 44000–44019; and so on.

Each run uses:
- `numpy.random.default_rng(seed)` for all sample generation.
- Sample sequence: `integers(0, n)` for $x$, then $y$, then `random()` for $u$, then conditionally `integers(0, n)` for $z$ if $u < p_\text{noise}$.
- Vectorized: `xs = rng.integers(0, n, N)` etc. This uses LAPACK-style vector RNG, which is stable across NumPy versions 1.17+.

Given the same NumPy version and seeds, output is bit-exact reproducible.

---

## Command to Rerun

```bash
cd /home/claude/sprint30b
python3 s30b_run.py
```

Expected runtime: ~20–30 seconds on standard hardware. The most expensive part is count aggregation at large carriers ($n = 100$ has $N = 100{,}000$ samples per seed, $\times 20$ seeds $= 2{,}000{,}000$ samples).

---

## Verification Hooks

After rerun, verify in `S30B_SCORES.json`:

- `spec_version == "S30b-v1.0"`
- `K_seeds == 20`, `pi_persist == 0.50`, `p_noise == 0.10`
- `data_seed_base == 30000`
- `aggregates.mu_ne == 0.0` (persistent seam is empty everywhere)
- `aggregates.mu_size == 0.0`
- `aggregates.mu_J ≈ 0.18` (within ~0.01 of 0.1798)
- `aggregates.mu_tied` is `null` (NaN) or absent
- `verdict == "FAIL"`

For carrier-level spot checks in `S30B_PERSISTENT_SEAMS.json`:
- Persistent size is 0 for every carrier in the family.
- Mean seed size at $n = 10$ ≈ 0.10.
- Mean seed size at $n = 100$ ≈ 8.60.
- Mean Jaccard at $n = 10$ ≈ 0.805 (trivial: most seeds are empty).
- Mean Jaccard at $n = 62$ or larger ≈ 0.000.

If any diverge, the environment or code has changed from spec.

---

## What Cannot Be Changed Without a Spec Bump

Per S30b-v1.0 §6 anti-tuning rules:
- 29-carrier family.
- $N(n) = 10 \cdot n^2$.
- $p_\text{noise} = 0.10$.
- $K = 20$ seeds.
- $\pi = 0.50$ persistence threshold.
- Data seed base 30000.
- Per-carrier seed scheme (30000 + 1000$n$ + $r$).
- Mode tie-breaking (smallest $z$, i.e., `np.argmax`'s default).
- Four metric thresholds (0.70, 2.0, 0.30, 0.60).

Any change requires S30b-v1.1+ and a fresh run.

---

## Full Command Pipeline

```bash
# Clean workspace
rm -f /home/claude/sprint30b/S30B_PERSISTENT_SEAMS.json \
      /home/claude/sprint30b/S30B_PER_SEED_SEAMS.csv \
      /home/claude/sprint30b/S30B_STABILITY.json \
      /home/claude/sprint30b/S30B_SCORES.json

# Run
cd /home/claude/sprint30b
python3 s30b_run.py

# Inspect
cat S30B_SCORES.json
head -15 S30B_PER_SEED_SEAMS.csv
```

---

## Integrity

- No external inputs other than the hardcoded carrier list (matching S28–S30).
- No null model (by design — S30b is detectability only).
- Verdict driven solely by frozen thresholds on computed quantities.
- Fully deterministic given seeds and NumPy version.
- No randomness in verdict logic.

---

## If Rerun Gives a Different Verdict

The FAIL verdict follows from the persistent seam being empty on every carrier. Under the frozen parameters, this is determined by:

- The low mode-flip probability per cell at $N(n) = 10 n^2$ and $p_\text{noise} = 0.10$.
- The statistical independence of flips across seeds (uniform noise does not preferentially flip any specific cell).
- The persistence threshold $\pi = 0.50$ requiring $\geq 10$ agreements in 20 runs.

Any rerun with the same spec parameters will produce empty persistent seams. If a rerun produces non-empty persistent seams, either:

1. The seed scheme was changed.
2. The persistence threshold was changed.
3. $N$ or $p_\text{noise}$ was changed.
4. The tie-breaking in `argmax` changed behavior (very unlikely — stable across NumPy versions).

None of these would constitute a valid S30b-v1.0 result.

---

## Cross-Sprint Comparison

| Spec | Seed base | Extractor | Verdict |
|---|---|---|---|
| S28-v1.0 | 28 | Basin-ratio smoothness | FAIL |
| S29-v1.0 | 29 | Basin-ratio anchored trend | FAIL |
| S30-v1.0 | 30 | Mode mismatch at high N | PASS (vacuous, uninformative) |
| S30b-v1.0 | 30000 | Low-$N$ mode mismatch + persistence | FAIL |

Four sprints, four outcomes under discipline. The third is a formal PASS recorded as evidentially empty. The fourth confirms that a conservative baseline extractor does not find persistent structural seams in noised canonical $C_0$ data on the tested family.
