# Path 3 Subtype v1.1 Results
## P3-Subtype-v1.1 — Identity-Edge Bridge

---

## Scope Declaration (Reproduced)

**Path:** Path 3 Bridge Test (identity-edge)
**Attractor convention:** cross-path (Path 1: $h_\text{thm}=7$; Path 2: $h_\text{ext}=\max$ odd unit, P3AP extension)
**Claim class:** bridge-level
**Canonical construction source:** Path 1 published TSML; Path 2 extended $C_0$ via P3AP overlay algorithm
**Relation to prior sprints:**
- Operates on P3-BridgeA-Prime-v1.0's recovered seams as-is.
- Subtype labels from P3AP's overlay audit records.
- Successor to P3-Subtype-v1.0 (UNCLEAR), isolating that sprint's strongest surviving finding.
- No bundling of count or adjacency metrics.
- No new generator.

---

## Single Primary Metric

**M4 — Identity-edge attachment.** For each Path 2 carrier, $I_n = 1$ iff the recovered ADD-labeled edge is incident to vertex 1 (the ring's multiplicative identity element); else $I_n = 0$.

**Family metric:** $\mu_\text{ID} = $ fraction of Path 2 carriers with $I_n = 1$.

---

## Per-Carrier Results

| $n$ | $\|E\|$ | $\|E_\text{ADD}\|$ | $\deg_S(1)$ | ADD edge(s) | $I_n$ |
|---:|---:|---:|---:|---|:---:|
| 14 | 3 | 1 | 1 | (1, 2) | 1 |
| 22 | 6 | 1 | 1 | (1, 2) | 1 |
| 34 | 6 | 1 | 1 | (1, 2) | 1 |
| 42 | 6 | 1 | 1 | (1, 2) | 1 |
| 46 | 6 | 1 | 1 | (1, 2) | 1 |
| 58 | 6 | 1 | 1 | (1, 2) | 1 |
| 74 | 6 | 1 | 1 | (1, 2) | 1 |
| 94 | 6 | 1 | 1 | (1, 2) | 1 |

All 8 carriers recover exactly one ADD edge. That edge is $(1, 2)$ on every carrier. Vertex 1 has degree 1 in the seam graph on every carrier.

**$\mu_\text{ID} = 1.0000$ (8/8 carriers).**

---

## Null Model Results

**Null N1:** subtype-label scrambling on the same recovered seam graphs. 100 replicates at seed 33300. For each replicate and each carrier, randomly select which edges receive the ADD label (preserving count $|E_\text{ADD}| = 1$ per carrier, with remaining edges labeled MAX). Compute $I_n$ on the scrambled labels.

| Statistic | Value |
|---|---:|
| $\mu_\text{ID}^\text{null}$ mean | 0.1963 |
| $\mu_\text{ID}^\text{null}$ std | 0.1326 |
| $\mu_\text{ID}^\text{null}$ min across 100 replicates | 0.0000 |
| $\mu_\text{ID}^\text{null}$ max across 100 replicates | 0.5000 |

**Sigma separation:** real $\mu_\text{ID}$ (1.0000) exceeds null mean (0.1963) by **+6.06σ**.

The theoretical null expectation, computed per-carrier as $\deg_S(1) / |E|$ (probability of random label placement touching vertex 1):
- Z/14: $1/3 \approx 0.333$.
- Z/22, 34, 42, 46, 58, 74, 94: $1/6 \approx 0.167$.
- Mean across 8 carriers: $(1/3 + 7 \cdot 1/6) / 8 = (0.333 + 1.167) / 8 = 0.188$.

The observed null mean (0.1963) matches the theoretical expectation closely. The null model is behaving as designed.

Across 100 replicates, the null never reaches 0.75 and never exceeds 0.50. Real $\mu_\text{ID} = 1.0$ is substantially outside the null distribution's entire observed range.

---

## Sub-Conditions

| Sub-condition | Result | Status |
|---|---:|:---:|
| $\mu_\text{ID} \geq 0.75$ | 1.0000 (8/8) | ✓ |
| Null separation $\geq 2\sigma$ | +6.06σ | ✓ |

Both sub-conditions met. No marginal flags.

---

## Observations

### The identity-edge pattern is strictly universal in the tested family

Every one of the 8 Path 2 carriers produces recovered ADD edge equal to $(1, 2)$. This is a consequence of the P3AP overlay-extension algorithm (specifically, the identity-edge component of §3.2 planting $(1, 2)$ and $(2, 1)$ as ADD cells on every carrier), but the *recovery* of that planted edge under noise is what the extractor has to accomplish — and S31-pilot-v2.0 plus P3AP's recovery quality metrics confirm that planted edges are recovered at ceiling under these parameters. So the observed 8/8 pattern combines two separate facts: (a) the extension algorithm plants identity-to-chain-start on every carrier, and (b) the extractor recovers it every time.

### The algebraic property transports

The Z/10 theorem places an ADD edge from vertex 1 (identity element of $\mathbb{Z}/10\mathbb{Z}$) to vertex 2 (smallest non-trivial element). The P3AP extension places the analogous ADD edge from vertex 1 (identity of $\mathbb{Z}/n\mathbb{Z}$) to vertex 2 on every Path 2 carrier. The extractor recovers this edge at ceiling.

This is structurally meaningful because vertex 1 is not just a graph vertex — it is the ring's multiplicative identity, an algebraic invariant. The transported feature is therefore algebraic rather than merely combinatorial.

### Null sharply rejects random explanation

With 6 edges per carrier on most tested rings and one ADD edge, random label placement touches vertex 1 only 1/6 ≈ 17% of the time per carrier. Across 8 carriers, the expected null rate is ~19%. The observed null mean (19.6%) matches this. The real rate (100%) is +6 standard deviations above null, far outside the range of any of the 100 replicates.

### Degree of vertex 1 is small in all seams

In all 8 Path 2 recovered seams, vertex 1 has degree 1 — connected only to vertex 2 via the ADD edge. This is a property of the extension algorithm (vertex 1 does not appear in the doubling chain, which starts at 2, and the identity-edge rule connects 1 only to 2). It is not a property the extractor had to discover; it is a property of the planted overlay that the extractor correctly preserved.

---

## What the Data Shows (Stated Narrowly)

Under the frozen spec of P3-Subtype-v1.1:

1. All 8 Path 2 carriers produce recovered ADD edges that touch vertex 1 (the ring's identity element). $\mu_\text{ID} = 1.0$, meeting the threshold of 0.75.
2. Under subtype-label scrambling on the same recovered seam graphs, random ADD-label placement touches vertex 1 at mean rate 0.196 with standard deviation 0.133.
3. Real identity-edge attachment exceeds null mean by +6.06σ, decisively exceeding the 2σ threshold.
4. Both sub-conditions pass. No marginal flags.

---

## What the Data Does NOT Say

- Nothing about count-proportion transport (deferred; would require a different null).
- Nothing about adjacency-pattern transport (deferred; would require a chain-topology-aware metric).
- Nothing about hub-and-spokes structural transport under a different overlay extension.
- Nothing about whether the theorem-level construction on Z/10 extends to non-Z/10 carriers.
- Nothing about identity-edge transport under overlay-extension algorithms other than P3AP's.
- Nothing about physical, ontological, or real-world invariants.

Verdict follows in `PATH3_SUBTYPE_V11_VERDICT.md`.
