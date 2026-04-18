# P3A Results — Theorem Seam vs Regenerated Discovered Seams
## P3-BridgeA-v1.0, Cross-Path Topology Comparison

---

## Scope Declaration (Reproduced)

**Path:** Path 3 Bridge Test
**Attractor convention:** cross-path (Path 1 under $h_\text{thm}=7$, Path 2 under $h_\text{ext}=\max$ odd unit)
**Claim class:** bridge-level
**Canonical construction source:** Path 1 published Z/10 TSML; Path 2 extended $C_0$ family
**Relation to prior sprints:** Path 1 seam inherited from the theorem (B1-confirmed). Path 2 seams regenerated per §3.2 protocol (no Sprint 21 artifact substitution occurred).

---

## Path 1 Reference (Fixed)

| Property | Value |
|---|---|
| Ordered seam cells | 8 |
| Unordered edges | 4 |
| Non-isolated vertices | 5 |
| Components $k$ | 1 |
| Forest? | Yes |
| $d_{\max}$ | 3 |
| $\rho$ | 0.8000 |
| Degree sequence | (1, 1, 1, 2, 3) |

A tree on 5 vertices with one hub (degree 3), one branch node (degree 2), three leaves.

---

## Path 2 Per-Carrier Results

| $n$ | $\|E\|$ | $\|V_{\text{ni}}\|$ | $k$ | Forest? | $d_{\max}$ | $\rho$ | MAX% | ADD% |
|---:|---:|---:|---:|:---:|---:|---:|---:|---:|
| 14 | 3 | 4 | 1 | ✓ | 2 | 1.000 | 0.0 | 33.3 |
| 22 | 8 | 12 | 4 | ✓ | 2 | 1.000 | 12.5 | 0.0 |
| 34 | 17 | 20 | 4 | ✗ | 3 | 0.900 | 0.0 | 0.0 |
| 42 | 23 | 24 | 2 | ✗ | 4 | 0.833 | 4.3 | 0.0 |
| 46 | 29 | 35 | 7 | ✗ | 3 | 0.829 | 0.0 | 3.3 |
| 58 | 45 | 43 | 4 | ✗ | 5 | 0.767 | 6.7 | 2.2 |
| 74 | 80 | 65 | 3 | ✗ | 7 | 0.615 | 0.0 | 1.2 |
| 94 | 144 | 89 | 1 | ✗ | 8 | 0.371 | 0.0 | 0.0 |

---

## Family Aggregates (Real)

| Metric | Value | Threshold | Met? |
|---|---:|---|:---:|
| $\mu_k$ (mean components) | 3.2500 | $\leq 3.0$ | ✗ |
| $\mu_F$ (forest fraction) | 0.2500 (2/8) | $\geq 0.75$ | ✗ |
| $\mu_d$ ($d_{\max}\leq 5$ fraction) | 0.7500 (6/8) | $\geq 0.75$ | ✓ |
| $\mu_\rho$ ($\rho\geq 0.60$ fraction) | 0.8750 (7/8) | $\geq 0.75$ | ✓ |

Two of four family-metric thresholds met. The two that failed are precisely the features most diagnostic of Path 1's topology: component count and forest-ness. Path 1 is a *tree with one component*; Path 2's regenerated seams are *multi-component graphs with cycles* at most carriers.

---

## Null Statistics (100 replicates, seed 32100)

| Quantity | Null mean | Null std |
|---|---:|---:|
| $\mu_F^\text{null}$ | 0.1900 | 0.1305 |
| $\mu_\rho^\text{null}$ | 0.8275 | 0.0607 |
| $\mu_k^\text{null}$ | 4.0038 | 0.3955 |
| $\mu_d^\text{null}$ | 0.7500 | 0.0866 |

## Sigma Separations (Real vs Null)

| Metric | Separation | Threshold | Met? |
|---|---:|---:|:---:|
| $\mu_F$ | +0.46σ | ≥ 2.0σ | ✗ |
| $\mu_\rho$ | +0.78σ | ≥ 2.0σ | ✗ |

Real $\mu_F$ (0.2500) only slightly exceeds null mean (0.1900). Random graphs of matching edge count produce forest-ness at this rate about 19% of the time on average; observed Path 2 produces it 25% of the time. Difference is within 0.5σ — uninformative.

Similarly $\mu_\rho$: real 0.8750 vs null 0.8275. Difference of 0.05, within 1σ. The low-degree profile is a property of sparse graphs in general, not specific to the discovered seams.

---

## Structural Observation

The Path 2 regenerated seams grow with carrier size in a specific way:

- **Small $n$ (14, 22):** few cells flip mode under noise; seams are tiny trees.
- **Medium $n$ (34–58):** seam size grows; acyclicity breaks as cells accumulate cycles.
- **Large $n$ (74, 94):** seam size grows substantially (80 and 144 edges); $d_\max$ climbs to 7–8; $\rho$ drops to 0.37.

Path 1's seam, by contrast, is a *designed artifact* — the theorem planted exactly 4 unordered edges in a tree configuration with one dominant hub. That is the theorem's construction, not a noise-extracted pattern.

The regenerated Path 2 seams are *noise-union seams*: every cell that flipped mode in any of 20 seeds at $p = 0.10$. This union grows with $n^2$ approximately (since more cells × more noise opportunities), and eventually the union fills enough of the vertex set that tree topology is structurally impossible.

This is why forest-ness fails on 6 of 8 carriers. It is not that the discovered seam lacks structure — it is that "union across 20 noisy seeds" is not the right object for shape-level comparison against a theorem seam.

---

## Subtype Mix (Diagnostic Only)

Per frozen spec §4.5, subtype mix is reported but not pass/fail. Results for reference:

| $n$ | MAX-like % | ADD-like % | Other % |
|---:|---:|---:|---:|
| 14 | 0.0 | 33.3 | 66.7 |
| 22 | 12.5 | 0.0 | 87.5 |
| 34 | 0.0 | 0.0 | 100.0 |
| 42 | 4.3 | 0.0 | 95.7 |
| 46 | 0.0 | 3.3 | 96.7 |
| 58 | 6.7 | 2.2 | 91.1 |
| 74 | 0.0 | 1.2 | 98.8 |
| 94 | 0.0 | 0.0 | 100.0 |

Across all 8 carriers, MAX-like fractions are low (0–12.5%), ADD-like fractions are low (0–33%), and "Other" dominates at 66–100%. Path 1's theorem seam is 75% MAX-like and 25% ADD-like. The regenerated Path 2 seams do not replicate this profile at any carrier.

The "Other" category reflects modal empirical values that are neither $\max(x,y)$ nor $(x+y) \bmod n$ — they are the noise-driven consequences of uniform replacement sampling, which tend to produce the random value or the nearby V0/default value rather than a structured overlay value.

This diagnostic reinforces the main verdict: regenerated Path 2 seams are dominated by sampling artifacts, not by structural overlays resembling the Path 1 theorem.

---

## What the Data Shows

Under the frozen spec of P3-BridgeA-v1.0:

1. **Path 1's theorem seam has the topology signature the spec predicted** (1 component, tree, $d_\max=3$, $\rho=0.80$).
2. **Path 2's regenerated seams do not share that signature.** Most are multi-component, non-forest, with degree patterns driven by carrier size rather than by structural planting.
3. **Null graphs of matched edge count produce similar $\mu_F$ and $\mu_\rho$ to real Path 2 graphs.** The sigma separations are below 1σ on both. Random graphs of the same density behave nearly identically to the regenerated seams — the regeneration procedure does not produce topology patterns exceeding density-matched random.
4. **Subtype mix is overwhelmingly "Other"** on every Path 2 carrier, indicating the regenerated seams are noise-driven rather than structured.

These four observations are mutually consistent: the Path 2 input object (noise-union seam) is not structurally analogous to the Path 1 input object (planted theorem seam) at the topology level tested.

---

## What This Does Not Establish

- It does not refute any deeper bridge claim between the paths. A different Path 2 input (e.g., planted-seam recovery artifacts rather than noise-union) might show different topology signatures.
- It does not invalidate any prior sprint verdict.
- It does not address Bridge B's overlay-extension hypothesis.
- It does not speak to cell-identity correspondence, rule subtypes, or any non-topology invariant.
