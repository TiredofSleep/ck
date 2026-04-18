# Path 3 Subtype Bridge Reproducibility
## P3-Subtype-v1.0 — How to Rerun

---

## Scope Reference

**Path:** Path 3 Bridge Test (subtype level)
**Convention:** cross-path (Path 1: $h_\text{thm}=7$; Path 2: $h_\text{ext}=\max$ odd unit)
**Claim class:** bridge-level
**Spec:** `PATH3_SUBTYPE_BRIDGE_PREREG.md`

Operates on P3-BridgeA-Prime-v1.0's recovered seams as-is. No new data generation, no new extractor run.

---

## Environment

- Python 3.11+ (tested on 3.12).
- NumPy (`numpy.random.default_rng`).
- Standard library: `json`, `csv`, `math.sqrt`.

---

## Input Files (Inherited)

Both required files produced by P3-BridgeA-Prime-v1.0 and read-only in this sprint:
- `/home/claude/path3_bridgeAprime/P3AP_OVERLAY_AUDIT.json` — per-carrier overlay rules, doubling chains, audit-removed cells.
- `/home/claude/path3_bridgeAprime/P3AP_PATH2_GRAPHS.json` — per-carrier recovered seams with topology metrics.

If these files are not present, the sprint cannot execute. They are not regenerated.

---

## Output Files

Written to `/home/claude/path3_subtype/`:

- `P3S_EDGE_LABELS.json` — per path: edges with subtype labels, Path 1 and Path 2 separately.
- `P3S_NULL_STATS.csv` — per (carrier, null replicate): f_max, delta, addrole, adj_sim.
- `P3S_SCORES.json` — family aggregates, null statistics, sigma separations, sub-conditions, verdict.

---

## Random Seed Handling

Single RNG stream driven by `numpy.random.default_rng(33200)`. Deterministic label-scrambling across all 8 carriers × 100 replicates = 800 null label assignments.

Seed bases distinct from all prior sprints (P3AP used 33000/33100; P3S uses 33200).

---

## Command to Rerun

```bash
cd /home/claude/path3_subtype
python3 p3s_run.py
```

Expected runtime: < 1 second. No extractor, no sampling — just graph operations and label manipulations.

---

## Verification Hooks

After rerun, verify in `P3S_SCORES.json`:

- `spec_version == "P3-Subtype-v1.0"`
- `scope == "Path 3 Bridge Test (subtype level)"`
- `path1_metrics.f_max == 0.75`
- `path1_metrics.adj_vec == [0.5, 0.5, 0.0]`
- `path1_metrics.addrole_match == true`
- `path2_family_metrics.mu_delta ≈ 0.0833`
- `path2_family_metrics.mu_addrole == 1.0`
- `path2_family_metrics.mu_adj ≈ 0.9551`
- `sigma_separations.addrole_above_null ≈ 3.80`
- `sigma_separations.delta_below_null == Infinity or similar degenerate value` (null_delta_std = 0)
- `sigma_separations.adj_above_null ≈ -0.87`
- `verdict == "UNCLEAR"`

Per-carrier spot checks (`P3S_EDGE_LABELS.json`):
- Z/14 path2: 3 edges, 2 MAX, 1 ADD.
- Z/22 path2: 6 edges, 5 MAX, 1 ADD, ADD edge is (1, 2).
- All other Path 2 carriers: 6 edges, 5 MAX, 1 ADD, ADD edge is (1, 2).

---

## What Cannot Be Changed Without a Spec Bump

Per P3-Subtype-v1.0 §5 anti-tuning rules:

- Path 2 carrier list (inherited from P3AP).
- Subtype label assignments from P3AP overlay audit records.
- Adapted role-matching rule (degree-1 external vertex attached to main component).
- Metric definitions M1, M2, M3.
- Null model (subtype-label scrambling, counts preserved per carrier).
- Null seed (33200).
- 100 null replicates.
- Thresholds: $\mu_\Delta \leq 0.10$, $\mu_\text{ADDrole} \geq 0.75$, $\mu_\text{adj} \geq 0.80$, 2σ null separation required on all three.

Any change requires v1.1+ and a fresh run.

---

## Known Structural Properties of the Verdict

Three sub-conditions fail in specific, documented ways:

1. **M1 null separation degenerate** because subtype-relabeling null preserves counts. This is a consequence of null choice, not a data issue. A different null (e.g., pre-planting overlay rule reassignment) would test M1 meaningfully.

2. **M3 null separation negative** because adjacency metric rewards balanced (MAX-ADD)-heavy adjacency vectors which random chain-interior placement can produce. The real external placement produces less-balanced adjacencies by topology, not by placement quality. Different metric design would address this.

3. **M2 null separation decisive at +3.80σ** because ADD role placement (identity-element attachment to main component) is a genuinely structural feature not reproduced by random labeling.

These three properties are deterministic given the inputs and the spec. Any rerun will produce them.

---

## Integrity

- No external inputs beyond frozen parameters and P3AP artifact files.
- Null model deterministic given seed.
- Verdict driven solely by frozen thresholds applied to computed metrics.
- Fully reproducible given NumPy version and seed.
- No sampling from noise models; all randomness is in label permutations.

---

## Full Command Pipeline

```bash
# Verify input files exist
ls /home/claude/path3_bridgeAprime/P3AP_OVERLAY_AUDIT.json
ls /home/claude/path3_bridgeAprime/P3AP_PATH2_GRAPHS.json

# Clean workspace (optional)
rm -f /home/claude/path3_subtype/P3S_EDGE_LABELS.json \
      /home/claude/path3_subtype/P3S_NULL_STATS.csv \
      /home/claude/path3_subtype/P3S_SCORES.json

# Run
cd /home/claude/path3_subtype
python3 p3s_run.py

# Quick verdict extraction
cat P3S_SCORES.json | python3 -c "
import json, sys
d = json.load(sys.stdin)
print('verdict:', d['verdict'])
print('mu_addrole null sep:', d['sigma_separations']['addrole_above_null'])
print('mu_adj null sep:', d['sigma_separations']['adj_above_null'])
print('sub conditions passed:', sum(1 for v in d['sub_conditions'].values() if v), '/', len(d['sub_conditions']))
"
```

Expected output:
```
verdict: UNCLEAR
mu_addrole null sep: 3.795...
mu_adj null sep: -0.866...
sub conditions passed: 4 / 6
```

---

## Cross-Sprint Comparison

| Spec | Path | Verdict | Key result |
|---|---|---|---|
| S28-v1.0 | 2 | FAIL | Basin smoothness (null inverted) |
| S29-v1.0 | 2 | FAIL | Anchored curve |
| S30-v1.0 | 2 | PASS (vacuous) | Empty seams at high N |
| S30b-v1.0 | 2 | FAIL | No seam under uniform noise |
| S31p-v1.0 | cross (undeclared) | FAIL | Convention mismatch |
| S31p-v2.0 | 1 | effective PASS | Ceiling recovery |
| P3-BridgeA-v1.0 | 3 | FAIL | Object-type mismatch |
| P3-BridgeA-Prime-v1.0 | 3 | PASS | First bridge, topology family |
| **P3-Subtype-v1.0** | **3** | **UNCLEAR** | **ADD-role transport confirmed at +3.80σ; count/adjacency nulls inadequate** |

Nine sprints under discipline. Each verdict cleanly attributed.

---

## If Rerun Gives a Different Verdict

Every computation in this sprint is deterministic:
- Input files are static artifacts.
- Label assignments derived from JSON records are deterministic.
- Null model uses fixed seed.

The verdict UNCLEAR with its specific sigma separations (+3.80 on ADDrole, degenerate on delta, -0.87 on adj) is the deterministic output of this frozen spec. Any divergence indicates:

1. Modified input files (P3AP artifacts).
2. Modified code.
3. NumPy version change affecting RNG (extremely unlikely to change magnitudes materially).

No legitimate source of variation exists at the verdict level.
