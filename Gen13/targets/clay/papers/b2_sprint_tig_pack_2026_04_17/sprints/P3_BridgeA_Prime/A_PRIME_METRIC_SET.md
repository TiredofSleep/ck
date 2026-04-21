# A-Prime Metric Set
## Topology-Only Metrics for Bridge A-Prime

---

## Constraints

The `SPRINT_SELECTOR.md` compatibility matrix permits graph-topology metrics on small designed artifacts. Both A-Prime inputs (Z/10 theorem-seam recovery artifact and Path 2 extended-overlay recovery artifacts) are small designed artifacts recovered by the same extractor. Graph-topology metrics are therefore ✓ for A-Prime.

Out of scope for this metric set:
- Scalar summaries (handled elsewhere; different object type).
- Cell-identity matching (different carriers, different cells; not commensurable).
- Rule-subtype transport (diagnostic only, by prior sprint discipline).
- Recovery quality per se (that's the R category from the sprint selector, already done in S31-pilot-v2.0).

In scope:
- Topology invariants of the recovered seam graph.
- Distinguishability from null graphs of matched density.

---

## Five Candidate Metrics, Ranked

### Metric M1 — Forest-ness (primary)

**Definition.** $F(R) := \mathbb{1}[|E_\text{simple}| = |V_\text{ni}| - k]$ on the unordered-edge seam graph (self-loops excluded from $E_\text{simple}$, no self-loops expected).

**Why primary.** The Path 1 theorem seam is a tree: 4 edges on 5 non-isolated vertices, 1 component, $|E| = 5 - 1 = 4$. Tree-ness is the single most distinctive topology feature of the Z/10 seam. If the Path 2 extended overlays produce recoverable seams that are consistently forest-like, that is the strongest shared-family signal we can ask for at the topology level.

**Threshold calibration.** Path 1 reference value: $F = 1$. Family metric: $\mu_F = $ fraction of Path 2 carriers with $F = 1$.

### Metric M2 — Component count profile (primary)

**Definition.** $k(R) := $ number of connected components on non-isolated vertices.

**Why primary.** Path 1's seam has $k = 1$ (fully connected). A consistent small $k$ across Path 2 carriers is a signature that the extended overlay produces a single coherent seam object, not a scattered set of independent cells.

**Threshold calibration.** Path 1 reference: $k = 1$. Family metric: $\mu_k = $ mean $k$ across Path 2 carriers.

### Metric M3 — Max degree band (primary)

**Definition.** $d_\text{max}(R) := $ maximum vertex degree.

**Why primary.** Path 1 has $d_\text{max} = 3$ (vertex 2 is the hub, connecting to 1, 4, 9). The extended overlay on non-Z/10 carriers has a similar designed structure: doubling-chain contributes degree-2 connections along the chain, attractor-involution contributes a high-degree vertex at $h_\text{ext}(R_n)$ or near-attractor positions. If the extractor recovers this cleanly, $d_\text{max}$ should cluster near 3 across carriers.

**Threshold calibration.** Path 1 reference: $d_\text{max} = 3$. Family metric: $\mu_d = $ fraction of Path 2 carriers with $d_\text{max} \in \{2, 3, 4\}$ (band of $\pm 1$ around Z/10's value).

### Metric M4 — Low-degree profile (primary)

**Definition.** $\rho(R) := $ fraction of non-isolated vertices with degree $\leq 2$.

**Why primary.** Path 1 has $\rho = 4/5 = 0.80$ (the hub has degree 3, the other four vertices have degree 1 or 2). Small designed artifacts with one hub and multiple leaves/branches typically have $\rho$ in the range 0.75–0.90. A consistent $\rho$ band across Path 2 carriers indicates preservation of the hub-and-spokes shape, not just arbitrary sparse connectivity.

**Threshold calibration.** Path 1 reference: $\rho = 0.80$. Per-carrier threshold: $\rho(R_n) \geq 0.70$ (20-percentage-point tolerance).

### Metric M5 — Hub concentration (diagnostic, not pass/fail)

**Definition.** $H(R) := $ fraction of edges incident to the vertex of maximum degree.

**Why diagnostic.** Path 1's hub (vertex 2) has 3 of 4 edges incident to it, giving $H = 0.75$. A high $H$ value means the seam is dominated by a single hub; a low value means edges are distributed more evenly. This is informative about whether Path 2 extended overlays preserve the specific hub-structure shape, but it's a finer-grained metric than the primary four, so it is reported for reference rather than used for pass/fail.

**Purpose.** Report per-carrier $H$ values. If the primary metrics pass and $H$ is also concentrated near 0.60–0.80 across carriers, that is a strong structural signal worth documenting for future sprints. If $H$ varies wildly, that is worth documenting as a caution against over-claiming.

---

## Null Model

**N1 — Edge-count-preserving uniform random graph.**

For each Path 2 carrier, draw 100 null graphs with the same number of unordered edges as the recovered seam, on the same vertex set, uniform random without replacement (no self-loops). Compute the four primary metrics on each null.

This null controls for density. Any topology feature the real recovered seam shows that a random graph of matching edge count also shows equally is a density artifact, not a structural signal.

---

## Thresholds

Conservative, informed by P3-BridgeA's experience.

| Metric | Threshold | Rationale |
|---|---|---|
| $\mu_F \geq 0.75$ | At least 6/8 carriers forest-like | Tighter than P3-BridgeA (which failed at 2/8); requires substantive preservation |
| $\mu_k \leq 1.5$ | Mean components ≤ 1.5 | Much tighter than P3-BridgeA's $\leq 3$; reflects that planted recovery should give nearly-single-component seams |
| $\mu_d \geq 0.75$ | At least 6/8 carriers with $d_\text{max} \in \{2, 3, 4\}$ | Tighter band than P3-BridgeA's $\leq 5$; reflects planted structure with defined hub |
| $\mu_\rho \geq 0.75$ | At least 6/8 carriers with $\rho \geq 0.70$ | Same as P3-BridgeA; preserves hub-and-spokes signal |
| Null sigma on $\mu_F$ | $\geq 2.0\sigma$ | Standard |
| Null sigma on $\mu_k$ | $\geq 2.0\sigma$ (real below null mean) | New vs P3-BridgeA; components should be *fewer* than random, not more |

Two new features vs P3-BridgeA's thresholds:

- **$\mu_k$ threshold is much tighter** (1.5 vs 3.0). Reflects that planted recovery should produce coherent small objects, not multi-component noise accumulations. This would have been a soft-impossible threshold under P3-BridgeA's noise-union input; under A-Prime's planted-recovery input it is achievable if the hypothesis holds.
- **$\mu_k$ also has a null-separation requirement**, which means the real object must have *fewer* components than a random graph of matching edge count — an actively structural property rather than a passive statistical one.

---

## What Could Go Wrong

Failure modes I predict in advance, in decreasing probability:

1. **Recovery quality degrades on non-Z/10 carriers.** If the extractor that worked at ceiling on Z/10 does not recover the extended overlay cleanly at other carriers, the recovered seam contains both planted cells and noise-residual cells. Topology metrics get corrupted. Signature: recovery precision < 0.9 at some carriers, followed by increased component count and/or reduced forest-ness.

2. **The overlay-extension algorithm produces structurally different artifacts per carrier.** Doubling chains have different lengths on different rings; identity-edge pairs are fixed but attractor involutions vary. If these algorithmic differences propagate into topology-level differences (e.g., some carriers get 2-hub structures instead of 1-hub), the topology family resemblance fails even under perfect recovery. Signature: $\mu_k$ fails at moderate carriers where doubling chains are longer, $d_\text{max}$ values scatter.

3. **Z/10 is genuinely unique in its topology.** The published theorem's specific 1-hub-3-leaves-1-branch tree might be an artifact of Z/10's particular arithmetic. Other carriers might produce recoverable but topologically distinct artifacts that don't cluster near Z/10's signature. Signature: metrics pass thresholds but null separation is weak; artifacts are structured but structured differently per carrier.

4. **Everything works cleanly and A-Prime passes.** This is the prediction I'd place at ~40% a priori, ~50% given the extractor's S31-pilot-v2.0 performance and the careful object-type matching.

The metric set is designed so that each failure mode has a distinctive signature. Diagnosis under FAIL should be possible from the output data alone.

---

## Integrity Check Against Comparison Law

Running the three tests from `COMPARISON_LAW.md`:

**Test 1 — Path and convention coherence.** Objects are in different paths (Path 1 theorem-recovery vs Path 2 extended-overlay-recovery). Bridging rule required. A-Prime is explicitly a Path 3 bridge sprint. ✓

**Test 2 — Generator type commensurability.** Both objects are produced by planting an overlay and recovering it with the same low-$N$ + persistence extractor. Both are small designed artifacts under noise. Same generator type. ✓

**Test 3 — Metric-object match.** Topology metrics on small designed artifacts are in the ✓ cell of the compatibility matrix. Metrics chosen are semantically meaningful for both objects. ✓

All three tests pass. The spec is eligible for freezing.
