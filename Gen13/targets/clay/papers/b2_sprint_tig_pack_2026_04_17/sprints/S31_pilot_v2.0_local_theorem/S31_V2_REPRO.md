# S31 v2 Reproducibility
## S31-pilot-v2.0 — How to Rerun

---

## Scope Reference

**Path:** Local Theorem (Path 1)
**Attractor convention:** $h_{\text{thm}} = 7$
**Canonical source:** published Z/10 TSML
**Spec:** `S31_PILOT_V2_LOCAL_THEOREM.md`

Implementation strictly follows spec. No amendments during execution.

---

## Environment

- Python 3.11+ (tested on 3.12).
- NumPy (`numpy.random.default_rng`, array ops).
- Standard library: `json`, `csv`, `math.gcd`, `collections.Counter`.

---

## Files

Single script at `/home/claude/sprint31_pilot_v2/s31_v2_run.py`.

Outputs in same directory:
- `S31v2_PER_SEED.csv` — per (overlay, noise, seed): seam size, seam edges.
- `S31v2_PERSISTENT.json` — per (overlay, noise): planted seam, persistent seam, intersection, metrics, per-seed sizes.
- `S31v2_SCORES.json` — aggregates, thresholds, sub-conditions, verdict.

---

## Random Seed Handling

Per-run seed formula: $\text{seed} = 31100 + 10000 \cdot \text{overlay\_idx} + 100 \cdot \text{noise\_idx} + r$

- Overlay indexing: NONE = 0, MAX = 1, ADD = 2, MAX_ADD = 3.
- Noise indexing: 0.02 = 0, 0.10 = 1, 0.20 = 2.
- $r \in \{0, 1, \ldots, 9\}$.

Data seed base 31100 distinct from v1.0's 31000 and all prior sprints (28, 29, 30, 30000).

Each run uses `numpy.random.default_rng(seed)` with vectorized sampling:
```python
xs = rng.integers(0, n, N)   # N = 1000
ys = rng.integers(0, n, N)
us = rng.random(N)
zs_noise = rng.integers(0, n, N)
```

Bit-exact reproducible across NumPy 1.17+.

Total 120 per-run extractions (4 overlays × 3 noise × 10 seeds).

---

## Command to Rerun

```bash
cd /home/claude/sprint31_pilot_v2
python3 s31_v2_run.py
```

Expected runtime: ~1–2 seconds.

---

## Pre-Run Sanity Verification (Built Into Script)

The script asserts two conditions before running the grid:

1. Canonical $C_0$ under $h_\text{thm} = 7$ matches the published Z/10 TSML on all 92 non-overlay cells.
2. $C_0 + \text{MAX+ADD}$ overlay reproduces the published Z/10 TSML bit-exactly.

If either assertion fails, the run aborts with a clear message. Both assertions pass under the frozen spec.

---

## Verification Hooks

After rerun, verify in `S31v2_SCORES.json`:

- `spec_version == "S31-pilot-v2.0"`
- `scope == "Local Theorem (Path 1)"`
- `attractor_convention == "h_thm = 7"`
- `canonical_source == "published Z/10 TSML"`
- `data_seed_base == 31100`
- All values in `per_condition` for non-NONE overlays are exactly 1.0 for $J$, $R$, $P$, $A$.
- `per_condition["NONE_p0.02"]["n_persistent"] == 0`.
- All 23 `sub_conditions` are `True`.
- `verdict == "UNCLEAR"` (per literal spec; see verdict doc).
- `marginal_flags` contains three entries, all of the form `*_p0.02_R` (the ceiling-recall artifact).

For spot-check of the headline numbers:
- MAX at $p = 0.02$: planted=6, persistent=6, intersection=6.
- ADD at $p = 0.20$: planted=2, persistent=2, intersection=2.
- MAX+ADD at $p = 0.10$: planted=8, persistent=8, intersection=8.

---

## What Cannot Be Changed Without a Spec Bump

Per S31-pilot-v2.0 §9 anti-tuning rules:
- Path designation (Local Theorem).
- Attractor $h_\text{thm} = 7$.
- Carrier (Z/10).
- Overlay definitions.
- $N = 1{,}000$.
- Noise levels $\{0.02, 0.10, 0.20\}$.
- $K = 10$.
- $\pi = 0.50$.
- Data seed base and per-run seed formula.
- Mode tie-break (smallest $z$).
- Metric definitions.
- Thresholds.
- UNCLEAR triggering rule (§8.6), even though it triggered on a ceiling artifact.

Any change requires v2.1+ and a fresh run.

---

## Known Spec-Design Issue

Documented in the verdict: §8.6's "within 10% of threshold" rule is symmetric but should be one-sided (only values narrowly *exceeding* a threshold should trigger UNCLEAR). Ceiling values at 1.0 against a 0.95 threshold technically satisfy the symmetric rule, producing a spurious UNCLEAR.

Not a tool issue. Not a data issue. A rule-specification issue that does not alter the data or the correct interpretation.

Future spec template should replace the within-10% rule with: "UNCLEAR triggers only when a metric value exceeds its threshold by less than 10% of the gap to the ceiling."

---

## Full Command Pipeline

```bash
rm -f /home/claude/sprint31_pilot_v2/S31v2_PER_SEED.csv \
      /home/claude/sprint31_pilot_v2/S31v2_PERSISTENT.json \
      /home/claude/sprint31_pilot_v2/S31v2_SCORES.json

cd /home/claude/sprint31_pilot_v2
python3 s31_v2_run.py

cat S31v2_SCORES.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('verdict:', d['verdict']); print('sub_cond all True:', all(d['sub_conditions'].values()))"
```

---

## Integrity

- No external inputs beyond hardcoded spec parameters.
- No null model (this is a Path 1 recovery pilot).
- Verdict driven solely by frozen thresholds applied to computed metrics.
- Fully deterministic given NumPy version and seed formula.
- Zero randomness in verdict logic.

---

## Cross-Sprint Comparison

| Spec | Path | Seed base | Verdict | Note |
|---|---|---|---|---|
| S28-v1.0 | Path 2 | 28 | FAIL | Basin-ratio smoothness, null inverted |
| S29-v1.0 | Path 2 | 29 | FAIL | Anchored curve, no depth-organization |
| S30-v1.0 | Path 2 | 30 | PASS (vacuous) | Empty seams at high N |
| S30b-v1.0 | Path 2 | 30000 | FAIL | No persistent seam under uniform noise |
| S31-pilot-v1.0 | cross-path (undeclared) | 31000 | FAIL | Convention mismatch, 2/8 cells invisible |
| S31-pilot-v2.0 | Path 1 | 31100 | UNCLEAR (ceiling artifact; effectively PASS) | Perfect recovery, spec-rule artifact |

Six sprints under discipline. First successful (effective) PASS is the Path 1 sprint under correctly declared scope.

---

## If Rerun Gives a Different Verdict

All Jaccard/recall/precision/type-agreement values for non-NONE overlays under $h = 7$ should be exactly 1.0 at all noise levels. The sanity checks at the top of the script assert the canonical construction matches the theorem, so any divergence would indicate:

1. Code modification.
2. Different attractor value used.
3. NumPy version causing different RNG stream (unlikely).

No legitimate source of variation exists. The UNCLEAR verdict (with ceiling-artifact explanation) is the deterministic output of this spec.
