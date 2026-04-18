# P3AP Results — Planted-Recovery Topology Bridge
## P3-BridgeA-Prime-v1.0, Cross-Path Comparison

---

## Scope Declaration (Reproduced)

**Path:** Path 3 Bridge Test
**Attractor convention:** cross-path (Path 1: $h_\text{thm}=7$; Path 2: $h_\text{ext}=\max$ odd unit)
**Claim class:** bridge-level
**Canonical construction source:** Path 1 published Z/10 TSML; Path 2 extended $C_0$ family
**Relation to prior sprints:** Inherits extractor from S31-pilot-v2.0 (ceiling-validated). Inherits Path 1 theorem overlay from published TSML. Does NOT inherit P3-BridgeA's noise-union input (object-type mismatch closed). Does NOT inherit Sprint 21's discovered seams (uses planted recovery instead).

---

## Path 1 Reference (Fixed, from S31-pilot-v2.0's ceiling recovery)

| Property | Value |
|---|---|
| Carrier | Z/10 |
| Ordered seam cells | 8 |
| Unordered edges | 4 |
| Components $k$ | 1 |
| Forest? | ✓ |
| $d_{\max}$ | 3 |
| $\rho$ | 0.800 |
| $H$ (hub concentration) | 0.750 |
| Degree sequence | (1, 1, 1, 2, 3) |

---

## Pre-Flight Overlay Audit (Per §3.4)

| $n$ | $h_\text{ext}$ | Doubling chain | $\|S_\text{MAX}\|$ raw | $\|S_\text{ADD}\|$ raw | Audit removed | $\|S_\text{final}\|$ |
|---:|---:|---|---:|---:|---:|---:|
| 14 | 13 | [2, 4, 8] | 6 | 2 | 2 | 6 |
| 22 | 21 | [2, 4, 8, 16, 10, 20] | 12 | 2 | 2 | 12 |
| 34 | 33 | [2, 4, 8, 16, 32, 30] | 12 | 2 | 2 | 12 |
| 42 | 41 | [2, 4, 8, 16, 32, 22] | 12 | 2 | 2 | 12 |
| 46 | 45 | [2, 4, 8, 16, 32, 18] | 12 | 2 | 2 | 12 |
| 58 | 57 | [2, 4, 8, 16, 32, 6] | 12 | 2 | 2 | 12 |
| 74 | 73 | [2, 4, 8, 16, 32, 64] | 12 | 2 | 2 | 12 |
| 94 | 93 | [2, 4, 8, 16, 32, 64] | 12 | 2 | 2 | 12 |

Exactly 2 cells removed per carrier by the pre-flight audit. Inspection of the removed cells confirms: these are the V0-related pairs where the canonical value under $h_\text{ext}$ coincides with the planted overlay value (specifically cells $(1, 2)$ and $(2, 1)$ on all carriers, because $(1+2) \bmod n = 3 = C_0(1, 2)$ fails — wait, that's for ADD. Actual removal pattern: the attractor-involution pairs $(2, h)$ and $(h, 2)$ where $\max(2, h) = h = C_0(2, h)$ coincide since $h$ is already the default fill value). This is precisely the structural invisibility the audit was designed to catch, prevented from contaminating the data.

---

## Path 2 Per-Carrier Recovery + Topology

| $n$ | $\|S_p\|$ | $\|S_\text{per}\|$ | $\|\cap\|$ | $J$ | Recall | Precision | $k$ | Forest? | $d_{\max}$ | $\rho$ | $H$ |
|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---:|---:|---:|
| 14 | 6 | 6 | 6 | 1.000 | 1.000 | 1.000 | 1 | ✓ | 2 | 1.000 | 0.667 |
| 22 | 12 | 12 | 12 | 1.000 | 1.000 | 1.000 | 1 | ✓ | 2 | 1.000 | 0.333 |
| 34 | 12 | 12 | 12 | 1.000 | 1.000 | 1.000 | 1 | ✓ | 2 | 1.000 | 0.333 |
| 42 | 12 | 12 | 12 | 1.000 | 1.000 | 1.000 | 1 | ✓ | 2 | 1.000 | 0.333 |
| 46 | 12 | 12 | 12 | 1.000 | 1.000 | 1.000 | 1 | ✓ | 2 | 1.000 | 0.333 |
| 58 | 12 | 12 | 12 | 1.000 | 1.000 | 1.000 | 1 | ✓ | 2 | 1.000 | 0.333 |
| 74 | 12 | 12 | 12 | 1.000 | 1.000 | 1.000 | 1 | ✓ | 2 | 1.000 | 0.333 |
| 94 | 12 | 12 | 12 | 1.000 | 1.000 | 1.000 | 1 | ✓ | 2 | 1.000 | 0.333 |

**Every planted cell recovered on every carrier.** Zero false positives. Precision, recall, Jaccard all 1.0 at every carrier. The extractor generalizes from Z/10 (S31-pilot-v2.0) to the 8 Path 2 carriers without degradation.

---

## Family Aggregates

| Metric | Real | Threshold | Met? | Null mean | Null std | Sigma separation |
|---|---:|---|:---:|---:|---:|---:|
| $\mu_F$ (forest fraction) | 1.0000 (8/8) | $\geq 0.75$ | ✓ | 1.0000 | 0.0000 | +∞σ (degenerate)* |
| $\mu_k$ (mean components) | 1.0000 | $\leq 1.5$ | ✓ | 4.4075 | 0.2714 | +12.56σ below null |
| $\mu_d$ ($d_\max \in [2,4]$ frac) | 1.0000 (8/8) | $\geq 0.75$ | ✓ | 0.7312 | 0.1362 | +1.97σ |
| $\mu_\rho$ ($\rho \geq 0.70$ frac) | 1.0000 (8/8) | $\geq 0.75$ | ✓ | 1.0000 | 0.0000 | +∞σ (degenerate)* |

*Null mean = 1.0 and std = 0 because: random graphs with only 3–6 edges on 14–89 vertices are almost always forests (too few edges to create cycles), and always have $\rho = 1.0$ (sparse graphs have no vertices of degree > 2). These metrics pass technically but are uninformative about structural preservation — they are density-driven.

**The decisive null separation is $\mu_k$**: real mean component count is 1.0 (every carrier produces a single connected seam), while random graphs of matching edge count produce mean component count 4.41. Sigma separation is +12.56σ below null. This is the active structural signal — the recovered artifacts are *not* scattered edge sets but form single connected objects, which random graphs of matched density emphatically do not.

---

## Observations from the Data

### Recovery is perfect across the family

All 8 Path 2 carriers achieve recovery metrics (Jaccard, recall, precision) of exactly 1.0. The low-$N$ + persistence extractor, validated on Z/10 in S31-pilot-v2.0, works identically on all 8 carriers without adjustment.

### Shared topology signatures

All 8 Path 2 recovered seams are:
- Connected ($k = 1$).
- Forest (tree).
- Low max degree ($d_\max = 2$).
- Entirely low-degree ($\rho = 1.0$).

The Z/10 reference has $d_\max = 3$ and $\rho = 0.80$, so Path 2 carriers fall slightly differently in the $d_\max$ and hub-concentration dimensions. Specifically:

- **Z/10's shape:** one hub (degree 3) with 3 leaves and 1 branch-node — hub-and-spokes.
- **Path 2 carriers' shape:** linear chain / path topology, $d_\max = 2$ everywhere — chain rather than hub.

Both are trees. Both are $k = 1$. Both are low-degree. But the specific structural shape differs: Z/10 has a distinctive hub, Path 2 carriers produce chains because the doubling-chain extension rule produces *sequential* connections rather than *branching* ones. This is visible in the $H$ (hub concentration) diagnostic: Z/10 has $H = 0.75$ (1 hub dominates); Path 2 has $H \in \{0.333, 0.667\}$ (no dominant hub in a chain).

### What this means

The topology metrics chosen for pass/fail captured "shared family features" correctly: forest-ness, single-component-ness, low-degree-ness. These are the *family-level* features that make both objects "small tree-like designed artifacts." The diagnostic hub-concentration metric ($H$) captures a *finer* shape distinction: Z/10 produces a hub, Path 2 produces chains under this specific extension algorithm.

A PASS on the primary metrics with a visible diagnostic difference on $H$ is exactly the kind of honest result the spec was designed to produce: it supports a bridge-level claim at the *family* level while transparently showing *where* the bridge does not extend to finer structure.

---

## What the Data Shows, Stated Narrowly

Under the frozen spec of P3-BridgeA-Prime-v1.0:

1. The low-$N$ + persistence extractor recovers the algorithmically-extended planted overlay perfectly on all 8 Path 2 carriers: $J = R = P = 1.000$ at every carrier.
2. All 8 Path 2 recovered seams are forests with a single component and max degree 2, placing them in the same topology family as Z/10's planted-recovery artifact (which is a forest with a single component and max degree 3).
3. Family aggregates meet all four primary thresholds at ceiling: $\mu_F = \mu_k^{-1} = \mu_d = \mu_\rho = $ ceiling values in the intended directions.
4. The decisive null separation — real $\mu_k$ below null mean — is at +12.56σ, far exceeding the 2σ threshold. Random graphs of matched edge count produce ~4.4 components on average; the recovered seams produce exactly 1 every time.
5. Diagnostic hub concentration ($H$) reveals that while Path 2 seams share the *family* features with Z/10 (tree, single component, low degree), they take a chain shape rather than a hub-and-spokes shape under this specific overlay extension.

---

## What This Data Cannot Say

- Under a different overlay-extension algorithm, results might differ. This PASS is specific to the doubling-chain + identity-edge + attractor-involution extension.
- It does not extend any Path 1 theorem to Path 2 carriers.
- It does not assert that the Path 2 extended overlays are "natural" objects on those carriers — they are heuristic constructions whose recovery proves the tool works.
- The chain-vs-hub shape difference (diagnostic $H$) is a real structural distinction that any future sprint testing "finer" topology resemblance will have to address.

Verdict follows in `P3AP_VERDICT.md`.
