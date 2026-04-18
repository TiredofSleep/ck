# Path 3 Subtype Adjacency v1.2 — Reproducibility
## P3-Subtype-v1.2-adj — How to Rerun

---

## Scope Reference

**Path:** Path 3 Bridge Test (leaf-edge placement)
**Convention:** cross-path (Path 1: $h_\text{thm}=7$; Path 2: $h_\text{ext}$ via P3AP extension)
**Claim class:** bridge-level
**Spec:** `PATH3_SUBTYPE_ADJACENCY_V12_PREREG.md`

Operates on P3-BridgeA-Prime-v1.0's recovered seams as-is. No new data generation, no new extractor run.

---

## Environment

- Python 3.11+ (tested on 3.12).
- NumPy (`numpy.random.default_rng`).
- Standard library: `json`, `csv`.

---

## Input Files (Inherited — Read-Only)

Both produced by P3-BridgeA-Prime-v1.0:
- `/home/claude/path3_bridgeAprime/P3AP_OVERLAY_AUDIT.json` — per-carrier overlay rules, audit-removed cells.
- `/home/claude/path3_bridgeAprime/P3AP_PATH2_GRAPHS.json` — per-carrier recovered seams with topology metrics.

If either is missing, the sprint cannot execute. They are not regenerated.

---

## Output Files

Written to `/home/claude/path3_subtype_v12_adj/`:

- `P3SAL_LABELS_AND_ROLES.json` — per Path 2 carrier: recovered edges, subtype labels, ADD edge, endpoint degrees, computed $L/M/I$ values.
- `P3SAL_NULL_STATS.csv` — per (carrier, null replicate): which edge received ADD label, $L/M/I$.
- `P3SAL_SCORES.json` — family aggregate, null statistics, sigma separation, sub-conditions, verdict.

---

## Random Seed Handling

Single RNG stream: `numpy.random.default_rng(33400)`. Deterministic label-scrambling across all 8 carriers × 100 replicates = 800 null label assignments.

Seed bases distinct from all prior sprints:
- P3AP: 33000 (data), 33100 (null).
- P3-Subtype-v1.0: 33200 (null).
- P3-Subtype-v1.1: 33300 (null).
- P3-Subtype-v1.2-adj: 33400 (null).

---

## Command to Rerun

```bash
cd /home/claude/path3_subtype_v12_adj
python3 p3sal_run.py
```

Expected runtime: < 1 second.

---

## Verification Hooks

After rerun, verify in `P3SAL_SCORES.json`:

- `spec_version == "P3-Subtype-v1.2-adj"`
- `scope == "Path 3 Bridge Test (leaf-edge placement)"`
- `null_seed == 33400`
- `family_metrics.mu_L_real_scored == 1.0`
- `family_metrics.mu_M_real_diagnostic == 1.0`
- `family_metrics.mu_I_real_inherited_from_v1_1 == 1.0`
- `path2_per_carrier[*].L_real == 1` for all 8 carriers
- `path2_per_carrier[*].add_edge == [1, 2]` for all 8 carriers
- `path2_per_carrier[*].endpoint_degrees == [1, 2]` for all 8 carriers
- `null_statistics.mu_L_null_mean ≈ 0.3588`
- `null_statistics.mu_L_null_std ≈ 0.1720`
- `null_statistics.mu_L_null_max ≈ 0.875`
- `sigma_separations.L_scored ≈ 3.73`
- `sub_conditions.mu_L_ge_0p75 == true`
- `sub_conditions.null_sep_ge_2sigma == true`
- `verdict == "PASS"`

Additional verification (inherited metrics, not scored):
- `sigma_separations.I_inherited ≈ 6.25` (should match v1.1's +6.06σ within sampling tolerance).
- `sigma_separations.M_diagnostic ≈ 2.13` (reported but not scored).

---

## What Cannot Be Changed Without a Spec Bump

Per P3-Subtype-v1.2-adj §6:

- Path 2 carrier list (inherited from P3AP).
- Subtype label assignments from P3AP overlay audit.
- Scored metric = $L$ only.
- $M$ and $I$ remain diagnostic/inherited; cannot be promoted to scored.
- Null model (subtype-label scrambling preserving counts per carrier).
- Null seed 33400.
- 100 null replicates.
- Thresholds: $\mu_L \geq 0.75$, null separation $\geq 2\sigma$.

Any change requires v1.2.1+ and a fresh run.

---

## Theoretical Verification of Null Expectation

For each carrier with seam graph $S$ and $|E_\text{ADD}| = 1$, the probability that a random single-ADD-label assignment lands on a leaf edge is:

$P(L_n = 1 | \text{random labeling}) = (\text{number of leaf edges}) / |E(S)|$

On P3AP's recovered seams (all chain topology with $d_\max = 2$):
- Number of leaf edges = 2 (the two chain endpoint edges).
- $|E|$ varies by carrier.

Theoretical per-carrier null probabilities:
- $n=14$: $|E|=3$, $P = 2/3 \approx 0.667$.
- $n=22, 34, 42, 46, 58, 74, 94$: $|E|=6$, $P = 2/6 \approx 0.333$.

Expected family-mean null: $(0.667 + 7 \cdot 0.333) / 8 = 0.375$.

Observed null mean: 0.3588 (close to theoretical 0.375, within sampling variability at 100 replicates).

This provides a cross-check: any correct reimplementation should produce null mean within a few percent of 0.375.

---

## Integrity

- No external inputs beyond frozen parameters and P3AP artifact files.
- Null model deterministic given seed.
- Verdict driven solely by frozen thresholds applied to computed metrics.
- Fully reproducible given NumPy version and seed.
- Pure combinatorics: no sampling from noise models; all randomness is in label permutations.
- $L$ is the only metric used in pass/fail. $M$ and $I$ are computed and reported but do not affect the verdict.

---

## Full Command Pipeline

```bash
# Verify input files exist
ls /home/claude/path3_bridgeAprime/P3AP_OVERLAY_AUDIT.json
ls /home/claude/path3_bridgeAprime/P3AP_PATH2_GRAPHS.json

# Clean workspace (optional)
rm -f /home/claude/path3_subtype_v12_adj/P3SAL_LABELS_AND_ROLES.json \
      /home/claude/path3_subtype_v12_adj/P3SAL_NULL_STATS.csv \
      /home/claude/path3_subtype_v12_adj/P3SAL_SCORES.json

# Run
cd /home/claude/path3_subtype_v12_adj
python3 p3sal_run.py

# Quick verdict extraction
cat P3SAL_SCORES.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('verdict:', d['verdict'])
print('mu_L (scored):', d['family_metrics']['mu_L_real_scored'])
print('L sigma separation:', d['sigma_separations']['L_scored'])
print('Null L max across 100 replicates:', d['null_statistics']['mu_L_null_max'])
print('Inherited I sigma (from v1.1, not re-scored):', d['sigma_separations']['I_inherited'])
"
```

Expected output:
```
verdict: PASS
mu_L (scored): 1.0
L sigma separation: 3.7285...
Null L max across 100 replicates: 0.875
Inherited I sigma (from v1.1, not re-scored): 6.2462...
```

---

## Cross-Sprint Comparison

| Spec | Path | Verdict | Key result |
|---|---|---|---|
| S28-v1.0 | 2 | FAIL | Basin smoothness |
| S29-v1.0 | 2 | FAIL | Anchored curve |
| S30-v1.0 | 2 | PASS (vacuous) | Empty seams |
| S30b-v1.0 | 2 | FAIL | No seam under uniform noise |
| S31p-v1.0 | cross (undeclared) | FAIL | Convention mismatch |
| S31p-v2.0 | 1 | effective PASS | Ceiling recovery |
| P3-BridgeA-v1.0 | 3 | FAIL | Object-type mismatch |
| P3-BridgeA-Prime-v1.0 | 3 | PASS | Topology-family (+12.56σ) |
| P3-Subtype-v1.0 | 3 | UNCLEAR | ADD role at +3.80σ; count/adj nulls inadequate |
| P3-Subtype-v1.1 | 3 | PASS | Identity-edge (+6.06σ) |
| **P3-Subtype-v1.2-adj** | **3** | **PASS** | **Leaf-edge placement (+3.73σ)** |

Eleven sprints under discipline. Four PASSes (S31p-v2.0 effective; P3AP, v1.1, v1.2-adj substantive). One UNCLEAR with residual content. Six informative negatives.

---

## If Rerun Gives a Different Verdict

All inputs are static (read-only P3AP artifacts); the sprint is pure combinatorics over fixed recovered seams with deterministic label-scrambling. Any divergence indicates:

1. Modified input files (P3AP artifacts).
2. Modified code.
3. NumPy version causing different RNG stream (unlikely to change magnitudes materially at 100 replicates).

The PASS with +3.73σ separation on $L$ and +6.25σ inherited reading on $I$ is the deterministic output of this frozen spec. The theoretical null expectation of 0.375 provides a sanity check that any correct reimplementation should satisfy within a few percent.
