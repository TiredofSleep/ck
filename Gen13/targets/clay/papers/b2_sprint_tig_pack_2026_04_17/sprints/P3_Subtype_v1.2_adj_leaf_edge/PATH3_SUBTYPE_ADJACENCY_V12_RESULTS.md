# Path 3 Subtype Adjacency v1.2 — Results
## P3-Subtype-v1.2-adj — Leaf-Edge Placement Bridge

---

## Scope Declaration (Reproduced)

**Path:** Path 3 Bridge Test (leaf-edge placement)
**Attractor convention:** cross-path (Path 1: $h_\text{thm}=7$; Path 2: $h_\text{ext}$ under P3AP extension)
**Claim class:** bridge-level
**Canonical construction source:** Path 1 published TSML; Path 2 extended $C_0$ via P3AP extension
**Relation to prior sprints:**
- Operates on P3AP recovered seams as-is.
- Subtype labels from P3AP overlay audit.
- Successor to P3-Subtype-v1.0 (UNCLEAR) and v1.1 (PASS on identity-edge).
- Scoring discipline: $L$ is the sole scored metric. $M$ diagnostic. $I$ inherited from v1.1 and NOT re-scored.

---

## Sole Scored Metric

**M4 — Leaf-edge placement ($L$).** For each Path 2 carrier, $L_n = 1$ iff the recovered ADD-labeled edge has at least one endpoint of degree 1 in the seam graph; else $L_n = 0$.

**Family metric:** $\mu_L = $ fraction of Path 2 carriers with $L_n = 1$.

---

## Per-Carrier Results

| $n$ | $\|E\|$ | ADD edge | Endpoint degrees | $L$ | $M$ (diag.) | $I$ (inherited) |
|---:|---:|---|---|:---:|:---:|:---:|
| 14 | 3 | (1, 2) | (1, 2) | 1 | 1 | 1 |
| 22 | 6 | (1, 2) | (1, 2) | 1 | 1 | 1 |
| 34 | 6 | (1, 2) | (1, 2) | 1 | 1 | 1 |
| 42 | 6 | (1, 2) | (1, 2) | 1 | 1 | 1 |
| 46 | 6 | (1, 2) | (1, 2) | 1 | 1 | 1 |
| 58 | 6 | (1, 2) | (1, 2) | 1 | 1 | 1 |
| 74 | 6 | (1, 2) | (1, 2) | 1 | 1 | 1 |
| 94 | 6 | (1, 2) | (1, 2) | 1 | 1 | 1 |

All 8 Path 2 carriers have ADD edge $(1, 2)$ with endpoint degrees $(1, 2)$ — vertex 1 is a degree-1 leaf vertex, vertex 2 is an internal vertex of degree 2. The ADD edge is a leaf edge on every carrier. $L_n = 1$ for every $n$.

---

## Family Aggregates

| Metric | Role | Real | Null mean | Null std | Null range | σ separation | Threshold | Met? |
|---|---|---:|---:|---:|---|---:|---|:---:|
| $\mu_L$ | **SCORED** | 1.0000 | 0.3588 | 0.1720 | [0.000, 0.875] | **+3.73σ** | ≥ 2.0σ | ✓ |
| $\mu_M$ | diagnostic | 1.0000 | 0.6825 | 0.1494 | — | +2.13σ | — | — |
| $\mu_I$ | inherited | 1.0000 | 0.1850 | 0.1305 | — | +6.25σ | — | — |

### Scored result

$\mu_L = 1.0$ (8/8 carriers) exceeds threshold 0.75. Null separation +3.73σ exceeds threshold 2.0σ. Both scored sub-conditions pass.

### Diagnostic and inherited observations

$M$ (main-component attachment) shows a null separation of +2.13σ, which happens to cross 2σ but is not a scored metric. $M$ was deliberately excluded from scoring because on chain topology it is structurally redundant (every degree-1 endpoint is automatically connected to the main component by its sole edge). The +2.13σ null separation for $M$ comes from the fact that random label placement that lands on an interior edge produces $M = 1$ trivially, so the null mean is elevated ($\approx 0.68$). Since $M = 1$ is guaranteed whenever the ADD edge is incident to any vertex in the main MAX component, and on these graphs that condition is easier to satisfy than either $L = 1$ or $I = 1$, the null rate for $M$ is higher than for the other two. The sprint correctly avoided scoring $M$.

$I$ (identity-element attachment) reproduces v1.1's result at +6.25σ (matching v1.1's reported +6.06σ up to seed-specific sampling variation). This is inherited evidence, not new evidence.

---

## Null Statistics in Detail

Across 100 null replicates at seed 33,400:

- **$\mu_L$ null distribution:** mean 0.3588, std 0.1720, min 0.000, max 0.875.
- **Real $\mu_L$ = 1.0** is outside the observed range of null ($\geq$ max 0.875).

Theoretical null expectation for $L$: for chain graphs with $|E|$ edges and exactly 2 leaf edges (the two chain-endpoint edges), random placement of 1 ADD label produces $L = 1$ with probability $2/|E|$.

- $n = 14$: $|E| = 3$, theoretical $P(L=1) = 2/3 \approx 0.667$.
- $n = 22, 34, 42, 46, 58, 74, 94$: $|E| = 6$, theoretical $P(L=1) = 2/6 \approx 0.333$.

Family-mean theoretical: $(0.667 + 7 \cdot 0.333)/8 = 0.375$.

Observed null mean: 0.359. Close to theoretical 0.375 (within one standard error for 100 replicates at this variance). The null model is behaving as designed.

---

## What the Data Shows

Under the frozen spec of P3-Subtype-v1.2-adj:

1. All 8 Path 2 carriers produce recovered ADD edges whose endpoint-degree pairs are $(1, 2)$ — vertex 1 is a degree-1 leaf and vertex 2 is an internal vertex.
2. The ADD edge is therefore a leaf edge (incident to at least one degree-1 vertex) on every carrier. $\mu_L = 1.0$ meets the $\geq 0.75$ threshold.
3. Under subtype-label scrambling on the same graphs, random ADD-label placement produces leaf-edge placement at mean rate 0.359 with standard deviation 0.172, across 100 replicates.
4. Real $\mu_L$ exceeds null mean by +3.73σ, decisively exceeding the 2σ threshold.
5. The real value of 1.0 is outside the entire observed null range (max 0.875), confirming the separation is not a marginal effect.

Both scored sub-conditions pass unambiguously.

---

## Inherited Context From v1.1 (Not Re-Scored)

For transparency of the full role signature, v1.1's identity-element metric $I$ is reported here:

- **$I$ real:** 1.0 on all 8 carriers (ADD edge's degree-1 endpoint is vertex 1).
- **$I$ null mean:** 0.1850 at seed 33400.
- **$I$ σ separation:** +6.25σ, consistent with v1.1's reported +6.06σ (at seed 33300).

This is inherited from v1.1's PASS, not a new result of v1.2-adj. Reporting here is for readers comparing sprints; the $I$ measurement does not contribute to v1.2-adj's verdict.

The consistency between v1.2-adj's computed $I$ (+6.25σ) and v1.1's reported $I$ (+6.06σ) at different seeds is a sanity check on the methodology: both runs produce nearly identical results on the same hypothesis, confirming reproducibility.

---

## What the Data Cannot Say

- Nothing about count-proportion transport (closed under P3AP generator).
- Nothing about raw adjacency ratios (shape-entangled metric abandoned with v1.0).
- Nothing about hub-and-spokes transport (different extension algorithm would be required).
- Nothing about identity-element attachment beyond what v1.1 already established. $I$ is reported for context, not re-tested.
- Nothing about the underlying cause of leaf-edge transport — whether it reflects a ring-structural invariant or is an artifact of the P3AP extension algorithm's specific identity-edge component.

Verdict follows in `PATH3_SUBTYPE_ADJACENCY_V12_VERDICT.md`.
