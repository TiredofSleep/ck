# Path 3 Subtype v1.1 Reproducibility
## P3-Subtype-v1.1 — How to Rerun

---

## Scope Reference

**Path:** Path 3 Bridge Test (identity-edge)
**Convention:** cross-path (Path 1: $h_\text{thm}=7$; Path 2: $h_\text{ext}$ via P3AP extension)
**Claim class:** bridge-level
**Spec:** `PATH3_SUBTYPE_V11_PREREG.md`

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

Written to `/home/claude/path3_subtype_v11/`:

- `P3S11_IDENTITY_ATTACHMENT.json` — per Path 2 carrier: ADD edges, vertex 1 degree in seam, identity-attachment indicator.
- `P3S11_NULL_STATS.csv` — per (carrier, null replicate): which edge received ADD label, identity-attachment indicator.
- `P3S11_SCORES.json` — family aggregate, null statistics, sigma separation, sub-conditions, verdict.

---

## Random Seed Handling

Single RNG stream: `numpy.random.default_rng(33300)`. Deterministic label-scrambling across all 8 carriers × 100 replicates = 800 null label assignments.

Seed bases distinct from all prior sprints:
- P3AP: 33000 (data), 33100 (null).
- P3-Subtype-v1.0: 33200 (null).
- P3-Subtype-v1.1: 33300 (null).

---

## Command to Rerun

```bash
cd /home/claude/path3_subtype_v11
python3 p3s11_run.py
```

Expected runtime: < 1 second.

---

## Verification Hooks

After rerun, verify in `P3S11_SCORES.json`:

- `spec_version == "P3-Subtype-v1.1"`
- `scope == "Path 3 Bridge Test (identity-edge)"`
- `null_seed == 33300`
- `mu_ID_real == 1.0`
- `path2_per_carrier[*].I_real == 1` for all 8 carriers
- `path2_per_carrier[*].add_edges == [[1, 2]]` for all 8 carriers
- `path2_per_carrier[*].deg_v1_in_seam == 1` for all 8 carriers
- `null_statistics.mu_ID_null_mean ≈ 0.1963`
- `null_statistics.mu_ID_null_std ≈ 0.1326`
- `null_statistics.mu_ID_null_max ≈ 0.5`
- `sigma_separation ≈ 6.06`
- `sub_conditions.mu_ID_ge_0p75 == true`
- `sub_conditions.null_sep_ge_2sigma == true`
- `verdict == "PASS"`

---

## What Cannot Be Changed Without a Spec Bump

Per P3-Subtype-v1.1 §6:

- Path 2 carrier list (inherited from P3AP).
- Subtype label assignments from P3AP overlay audit.
- Metric definition (identity-edge attachment, binary per carrier).
- Null model (subtype-label scrambling preserving counts per carrier).
- Null seed (33300).
- 100 null replicates.
- Thresholds: $\mu_\text{ID} \geq 0.75$, null separation $\geq 2\sigma$.

Any change requires v1.2+ and a fresh run.

---

## Theoretical Verification of Null Expectation

For each carrier with seam graph $S$, $|E(S)|$ edges, and $|E_\text{ADD}| = 1$, the probability that a random single-ADD-label assignment places that label on an edge incident to vertex 1 is:

$P(I_n = 1 | \text{random labeling}) = \deg_S(1) / |E(S)|$

On P3AP's recovered seams:
- $n=14$: $|E| = 3$, $\deg(1) = 1$ → $P = 1/3 \approx 0.333$.
- $n=22, 34, 42, 46, 58, 74, 94$: $|E| = 6$, $\deg(1) = 1$ → $P = 1/6 \approx 0.167$.

Expected $\mu_\text{ID}^\text{null} = (0.333 + 7 \cdot 0.167) / 8 = (0.333 + 1.167) / 8 = 0.1875$.

Observed null mean: 0.1963. Difference of ~0.01 is consistent with sampling variability across 100 replicates.

This provides a theoretical cross-check: the null behaves as expected. Any implementation error that produces a very different null mean would be visible here.

---

## Integrity

- No external inputs beyond frozen parameters and P3AP artifact files.
- Null model deterministic given seed.
- Verdict driven solely by frozen thresholds applied to computed metrics.
- Fully reproducible given NumPy version and seed.
- Pure combinatorics: no sampling from noise models; all randomness is in label permutations.

---

## Full Command Pipeline

```bash
# Verify input files exist
ls /home/claude/path3_bridgeAprime/P3AP_OVERLAY_AUDIT.json
ls /home/claude/path3_bridgeAprime/P3AP_PATH2_GRAPHS.json

# Clean workspace (optional)
rm -f /home/claude/path3_subtype_v11/P3S11_IDENTITY_ATTACHMENT.json \
      /home/claude/path3_subtype_v11/P3S11_NULL_STATS.csv \
      /home/claude/path3_subtype_v11/P3S11_SCORES.json

# Run
cd /home/claude/path3_subtype_v11
python3 p3s11_run.py

# Quick verdict extraction
cat P3S11_SCORES.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('verdict:', d['verdict'])
print('mu_ID:', d['mu_ID_real'])
print('sigma separation:', d['sigma_separation'])
print('null max across 100 replicates:', d['null_statistics']['mu_ID_null_max'])
"
```

Expected output:
```
verdict: PASS
mu_ID: 1.0
sigma separation: 6.0619...
null max across 100 replicates: 0.5
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
| P3-BridgeA-Prime-v1.0 | 3 | PASS | Topology family (+12.56σ on $\mu_k$) |
| P3-Subtype-v1.0 | 3 | UNCLEAR | ADD role at +3.80σ; count/adj nulls inadequate |
| **P3-Subtype-v1.1** | **3** | **PASS** | **Identity-element attachment +6.06σ** |

Ten sprints under discipline. Three PASSes (S31p-v2.0 effective, P3AP substantive, P3S-v1.1 substantive). One UNCLEAR with residual content. Six informative negatives.

---

## If Rerun Gives a Different Verdict

All inputs are static; the sprint is pure combinatorics over fixed recovered seams. Any divergence indicates:

1. Modified input files (P3AP artifacts).
2. Modified code.
3. NumPy version causing substantially different RNG stream on `rng.choice` (unlikely to change magnitudes materially at N=100 replicates).

The PASS with +6.06σ separation is the deterministic output of this frozen spec. The theoretical null expectation of 0.188 (compared to observed 0.196) provides a sanity check that any correct reimplementation should satisfy within sampling variability.
