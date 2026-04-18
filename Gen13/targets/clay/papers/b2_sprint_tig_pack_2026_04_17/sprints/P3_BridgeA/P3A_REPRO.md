# P3A Reproducibility
## P3-BridgeA-v1.0 — How to Rerun

---

## Scope Reference

**Path:** Path 3 Bridge Test
**Convention:** cross-path (Path 1: $h_\text{thm}=7$; Path 2: $h_\text{ext}=\max$ odd unit)
**Claim class:** bridge-level
**Spec:** `PATH3_BRIDGEA_PREREG.md`

Implementation strictly follows spec with regenerated Path 2 seams (§3.2). No Sprint 21 artifact substitution occurred (artifacts not accessible in execution context).

---

## Environment

- Python 3.11+ (tested on 3.12).
- NumPy (`numpy.random.default_rng`, array ops).
- Standard library: `json`, `csv`, `math.gcd`, `collections.Counter`.

---

## Files

Single script at `/home/claude/path3_bridgeA/p3a_run.py`.

Outputs in same directory:
- `P3A_PATH1_GRAPH.json` — fixed Path 1 seam, edges, topology metrics.
- `P3A_PATH2_GRAPHS.json` — per Path 2 carrier: seam union, edges, metrics, subtype mix.
- `P3A_PER_SEED_PATH2.csv` — per (carrier, seed): seam size.
- `P3A_NULL_DATA.csv` — per (carrier, null replicate): topology metrics.
- `P3A_SCORES.json` — aggregates, nulls, sigma separations, sub-conditions, verdict.

---

## Random Seed Handling

Two deterministic layers:

1. **Path 2 data seeds:** $\text{seed}(n, r) = 32000 + 1000 \cdot n + r$ for $r \in \{0, \ldots, 19\}$. Each (carrier, seed-index) pair gets a distinct stream.

2. **Null model seed:** `NULL_SEED = 32100`. Single `numpy.random.default_rng(32100)` drives all 100 null replicates × 8 carriers = 800 null draws, sequentially.

Total seeds used: 8 carriers × 20 seeds = 160 data streams + 1 null stream.

Seed bases distinct from all prior sprints (S28=28, S29=29, S30=30, S30b=30000, S31pv1=31000, S31pv2=31100, P3A=32000 for data + 32100 for null).

---

## Command to Rerun

```bash
cd /home/claude/path3_bridgeA
python3 p3a_run.py
```

Expected runtime: ~30–60 seconds (most expensive at $n=94$ with $N = 88{,}360$ samples per seed × 20 seeds + null replicates).

---

## Verification Hooks

After rerun, verify in `P3A_SCORES.json`:

- `spec_version == "P3-BridgeA-v1.0"`
- `scope == "Path 3 Bridge Test"`
- `data_seed_base == 32000`, `null_seed == 32100`
- `path1_metrics.k == 1`, `path1_metrics.is_forest == true`, `path1_metrics.d_max == 3`
- `path1_metrics.rho ≈ 0.8000`
- `path2_family_metrics.mu_k ≈ 3.25`
- `path2_family_metrics.mu_F == 0.25` (exactly 2/8)
- `path2_family_metrics.mu_d == 0.75` (exactly 6/8)
- `path2_family_metrics.mu_rho == 0.875` (exactly 7/8)
- `sigma_separation.F ≈ 0.46`
- `sigma_separation.rho ≈ 0.78`
- `verdict == "FAIL"`

Per-carrier spot checks (`P3A_PATH2_GRAPHS.json`):
- $n=14$: edges=3, forest=True, $d_\max=2$.
- $n=94$: edges=144, forest=False, $d_\max=8$, $\rho≈0.371$.
- $n=22$: edges=8, forest=True, $d_\max=2$.

If any diverge, environment or code has changed from spec.

---

## What Cannot Be Changed Without a Spec Bump

Per P3-BridgeA-v1.0 §7 anti-tuning rules:
- Carrier list: {14, 22, 34, 42, 46, 58, 74, 94}.
- Path 1 reference seam.
- Data-gen parameters: $N(n) = 10n^2$, $p = 0.10$, $K = 20$.
- Seed scheme: $32000 + 1000n + r$.
- Null model: edge-count-preserving uniform random.
- Null seed: 32100.
- Null replicates: 100.
- Topology metrics $k, F, d_\max, \rho$.
- Thresholds: $\mu_k \leq 3$, $\mu_F \geq 0.75$, $\mu_d \geq 0.75$, $\mu_\rho \geq 0.75$, null sigma ≥ 2σ on $\mu_F$ and $\mu_\rho$.
- Subtype-mix status: diagnostic only, not pass/fail.

Any change requires v1.1+ and a fresh run.

---

## Known Non-Issues

The spec's §3.3 substitution clause permits use of Sprint 21 artifacts if located. At execution time, no such artifacts were available in the execution context. This is documented, not problematic — the regenerated seam protocol is complete and deterministic.

The P3A verdict is FAIL regardless of whether artifacts are later located, because:
1. Regenerated seams on 8 carriers show the topology pattern independent of artifact availability.
2. The substitution clause requires artifacts to match $h_\text{ext}$ with $p \in [0.05, 0.15]$ and $N \geq 5n^2$ — conditions that Sprint 21's protocol approximately satisfies, so substituted artifacts would likely produce similar union seams.
3. A Sprint 21 artifact substitution would need a new spec version (v1.1) and a fresh run under the substitution, not a retroactive reinterpretation of v1.0.

---

## Integrity

- No external inputs beyond hardcoded frozen parameters.
- Null model deterministic given seed.
- Verdict driven solely by frozen thresholds applied to computed metrics.
- Fully reproducible given NumPy version and seed formulas.

---

## Full Command Pipeline

```bash
rm -f /home/claude/path3_bridgeA/P3A_PATH1_GRAPH.json \
      /home/claude/path3_bridgeA/P3A_PATH2_GRAPHS.json \
      /home/claude/path3_bridgeA/P3A_PER_SEED_PATH2.csv \
      /home/claude/path3_bridgeA/P3A_NULL_DATA.csv \
      /home/claude/path3_bridgeA/P3A_SCORES.json

cd /home/claude/path3_bridgeA
python3 p3a_run.py

# Quick verdict extraction
cat P3A_SCORES.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('verdict:', d['verdict'])"
```

---

## Cross-Sprint Comparison

| Spec | Path | Verdict | Summary |
|---|---|---|---|
| S28-v1.0 | 2 | FAIL | Basin-ratio smoothness, null inverted |
| S29-v1.0 | 2 | FAIL | Anchored curve, no depth organization |
| S30-v1.0 | 2 | PASS (vacuous) | Empty seams at high N |
| S30b-v1.0 | 2 | FAIL | Uniform noise on $C_0$ has no seam-prone cells |
| S31p-v1.0 | cross (undeclared) | FAIL | Convention mismatch |
| S31p-v2.0 | 1 | effective PASS | Ceiling recovery on theorem object |
| **P3-BridgeA-v1.0** | **3** | **FAIL** | **Noise-union seams don't share topology with theorem seam** |

Seven sprints under discipline, diverse failure modes, each cleanly attributed. This is working as designed — the pre-registration system catches both real structural negatives and spec-design issues without allowing either to be rescued post-hoc.
