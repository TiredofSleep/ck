# P3AP Reproducibility
## P3-BridgeA-Prime-v1.0 — How to Rerun

---

## Scope Reference

**Path:** Path 3 Bridge Test
**Convention:** cross-path (Path 1: $h_\text{thm}=7$; Path 2: $h_\text{ext}=\max$ odd unit)
**Claim class:** bridge-level
**Spec:** `PATH3_BRIDGE_A_PRIME_PREREG.md`

Implementation strictly follows spec. No amendments during execution.

---

## Environment

- Python 3.11+ (tested on 3.12).
- NumPy (`numpy.random.default_rng`, array operations).
- Standard library: `json`, `csv`, `math.gcd`.

---

## Files

Single script at `/home/claude/path3_bridgeAprime/p3ap_run.py`.

Outputs in same directory:
- `P3AP_OVERLAY_AUDIT.json` — per Path 2 carrier: raw $S_\text{MAX}$, raw $S_\text{ADD}$, doubling chain, cells removed by pre-flight audit, final $S_\text{planted}$.
- `P3AP_PATH1_GRAPH.json` — Z/10 reference graph with topology metrics.
- `P3AP_PATH2_GRAPHS.json` — per Path 2 carrier: $S_\text{planted}$, $S_\text{persistent}$, unordered edges, full topology metrics, recovery metrics, per-seed seam sizes.
- `P3AP_SCORES.json` — family aggregates, null statistics, sigma separations, sub-conditions, verdict.

---

## Random Seed Handling

**Path 2 data seeds:** $\text{seed}(n, r) = 33000 + 1000 \cdot n + r$ for $r \in \{0, \ldots, 9\}$, for each carrier $n \in \{14, 22, 34, 42, 46, 58, 74, 94\}$.

**Null seed:** `NULL_SEED = 33100`, single `numpy.random.default_rng(33100)` driving all 100 null replicates × 8 carriers = 800 null draws sequentially.

Seed bases distinct from all prior sprints (P3A used 32000/32100; P3AP uses 33000/33100).

Total deterministic streams: 8 × 10 = 80 data streams + 1 null stream.

---

## Command to Rerun

```bash
cd /home/claude/path3_bridgeAprime
python3 p3ap_run.py
```

Expected runtime: ~10–20 seconds (dominated by $n=94$ with $N = 88{,}360$ samples per seed × 10 seeds + null replicate computation).

---

## Verification Hooks

After rerun, verify in `P3AP_SCORES.json`:

- `spec_version == "P3-BridgeA-Prime-v1.0"`
- `scope == "Path 3 Bridge Test"`
- `convention == "cross-path (Path 1: h_thm=7, Path 2: h_ext=max odd unit)"`
- `claim_class == "bridge-level"`
- `path1_metrics.k == 1`, `path1_metrics.is_forest == true`
- `path1_metrics.d_max == 3`, `path1_metrics.rho ≈ 0.8000`, `path1_metrics.H == 0.75`
- `path2_family_metrics.mu_F == 1.0`
- `path2_family_metrics.mu_k == 1.0`
- `path2_family_metrics.mu_d == 1.0`
- `path2_family_metrics.mu_rho == 1.0`
- `sigma_separations.k_below_null ≈ 12.56`
- `verdict == "PASS"`

Per-carrier spot checks (`P3AP_PATH2_GRAPHS.json`):
- $n=14$: 6 planted cells (3 MAX + 1 ADD + 2 attractor-involution... minus 2 audit removals = 6 final), recovered with $J = 1.0$, forest, $d_\max = 2$.
- All other carriers: 12 planted cells, recovered with $J = 1.0$, forest, $d_\max = 2$.

Per-carrier audit (`P3AP_OVERLAY_AUDIT.json`):
- $n=14$: chain = [2, 4, 8], 2 cells removed by audit.
- $n=22$: chain = [2, 4, 8, 16, 10, 20], 2 cells removed.
- All carriers: exactly 2 cells removed by audit (the attractor-involution pair where planted = canonical).

If any diverge, environment or code has changed from the frozen spec.

---

## What Cannot Be Changed Without a Spec Bump

Per P3-BridgeA-Prime-v1.0 §9 anti-tuning rules:
- Path 2 carrier list {14, 22, 34, 42, 46, 58, 74, 94}.
- Overlay extension algorithm: doubling-chain (capped at 6), identity-edge, attractor-involution.
- Pre-flight audit procedure.
- Extractor parameters: $N = 10n^2$, $p = 0.10$, $K = 10$, $\pi = 0.50$, tie-break smallest $z$.
- Seed scheme: $33000 + 1000n + r$ for data, 33100 for null.
- Null model: edge-count-preserving uniform random.
- Null replicates: 100.
- Metric definitions $F, k, d_\max, \rho, H$.
- Thresholds: $\mu_F \geq 0.75$, $\mu_k \leq 1.5$, $\mu_d \geq 0.75$, $\mu_\rho \geq 0.75$, 2σ null separation on $\mu_F$ and $\mu_k$.
- M5 hub-concentration remains diagnostic, not pass/fail.

Any change requires v1.1+ and a fresh run.

---

## Integrity

- No external inputs beyond hardcoded frozen parameters.
- Null model deterministic given seed.
- Verdict driven solely by frozen thresholds applied to computed metrics.
- Fully reproducible given NumPy version and seed formulas.
- Pre-flight audit is part of the frozen algorithm, not post-hoc tuning: the same 2 cells per carrier are removed on every run.

---

## Full Command Pipeline

```bash
# Clean workspace (optional)
rm -f /home/claude/path3_bridgeAprime/P3AP_OVERLAY_AUDIT.json \
      /home/claude/path3_bridgeAprime/P3AP_PATH1_GRAPH.json \
      /home/claude/path3_bridgeAprime/P3AP_PATH2_GRAPHS.json \
      /home/claude/path3_bridgeAprime/P3AP_SCORES.json

# Run
cd /home/claude/path3_bridgeAprime
python3 p3ap_run.py

# Quick verdict extraction
cat P3AP_SCORES.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('verdict:', d['verdict']); print('mu_F:', d['path2_family_metrics']['mu_F']); print('mu_k:', d['path2_family_metrics']['mu_k']); print('k below null:', d['sigma_separations']['k_below_null'])"
```

Expected output:
```
verdict: PASS
mu_F: 1.0
mu_k: 1.0
k below null: 12.557...
```

---

## Cross-Sprint Comparison

| Spec | Path | Seed base | Verdict | Summary |
|---|---|---|---|---|
| S28-v1.0 | 2 | 28 | FAIL | Basin-ratio smoothness (null inverted) |
| S29-v1.0 | 2 | 29 | FAIL | Anchored curve (no depth organization) |
| S30-v1.0 | 2 | 30 | PASS (vacuous) | Empty seams at high N |
| S30b-v1.0 | 2 | 30000 | FAIL | No seam under uniform noise on $C_0$ |
| S31p-v1.0 | cross (undeclared) | 31000 | FAIL | Convention mismatch |
| S31p-v2.0 | 1 | 31100 | effective PASS | Ceiling recovery on Z/10 theorem object |
| P3-BridgeA-v1.0 | 3 | 32000 | FAIL | Object-type mismatch (noise-union Path 2 input) |
| **P3-BridgeA-Prime-v1.0** | **3** | **33000** | **PASS** | **First confirmed bridge, family-level topology** |

Eight sprints under discipline. Two PASSes (one effective, one substantive). Six informative negatives. Each verdict cleanly attributed to specific causes via the atlas/law/selector framework.

---

## If Rerun Gives a Different Verdict

The PASS follows from structural properties:

1. The overlay-extension algorithm is deterministic: same chain and same cells on every run.
2. The pre-flight audit is deterministic: always removes the same 2 cells per carrier (attractor-involution pair where planted = canonical).
3. The extractor at $N = 10n^2$ and $p = 0.10$ with 10 seeds and $\pi = 0.50$ recovers planted cells with high probability; at these parameters the persistence filter is robust enough to eliminate stochastic variation.
4. Recovery at all 8 carriers is ceiling (Jaccard = 1.0), which means the recovered graph equals the planted graph exactly.
5. The planted graph under the frozen extension rule is deterministic; its topology is computable directly.

Any divergence would indicate:
- Code modification.
- NumPy version causing substantially different RNG (extremely unlikely for stochastic recovery at this signal-to-noise ratio).
- Different parameters.

No legitimate source of variation exists at the verdict level. The PASS with +12.56σ $\mu_k$ separation is the deterministic output of this frozen spec.
