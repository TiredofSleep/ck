# Pair-Primitive Mapping — Results
## PPM-v1.0 Rubric Evaluation on Z/10's 8 Seam Cells

---

## Scope Declaration (Reproduced)

**Path:** Local Theorem Chart (Path 1).
**Attractor convention:** $h_\text{thm} = 7$.
**Claim class:** structural-fit claim at the local theorem chart, conditional on the framework's vocabulary.
**Relation to prior sprints:**
- Operates on Z/10 seam data; treats Path 3 findings (P3AP, v1.1, v1.2-adj) as inherited context only.
- Does NOT re-score any Path 3 sprint's result.
- Tests one specific operationalization of the pair-primitive framework.

**Frozen clarification:** This sprint evaluates the pair-primitive framework under a multiplicative operationalization only; failure would refute this operationalization, not the pair-primitive framework in all possible readings. A passage confirms the framework under this operationalization, not in all possible readings.

---

## The Two Candidate Mappings

- **Map A:** ADD = persistent-side reading, MAX = excluded-side reading.
- **Map B:** MAX = persistent-side reading, ADD = excluded-side reading.

## Operational Interpretation (PPM-v1.0 §3)

- **Persistent-side:** subtype forming the structural backbone under Z/10's multiplicative operation structure; connected substructure carrying the majority of the seam's edges and aligning with multiplicative flow (doubling chain, attractor-involution).
- **Excluded-side:** subtype constituting a localized departure from multiplicative operation structure; imports a non-multiplicative rule and surfaces at boundary positions.

---

## Per-Source Scoring

Scoring proceeded source-by-source. Each source was evaluated against both maps before moving to the next.

### Source 1 — Seam-graph structural split

**Data.**
- MAX subtype: 6 cells = 3 unordered edges on vertex set $\{2, 4, 8, 9\}$: $\{2\text{–}4, 2\text{–}9, 4\text{–}8\}$. Includes the doubling-chain segment $2 \to 4 \to 8$ and the attractor-involution edge $2\text{–}9$.
- ADD subtype: 2 cells = 1 unordered edge on vertex set $\{1, 2\}$: $\{1\text{–}2\}$.
- Total seam edges (unordered): 4.

**Rubric (§5.1).** Does the map's persistent-side subtype form the structural backbone?

**Backbone evaluation.**
- MAX forms $3/4 = 75\%$ of unordered seam edges. ✓ majority condition.
- MAX contains the doubling chain $2\text{–}4\text{–}8$. ✓ multiplicative-flow element.
- MAX contains the attractor-involution edge $2\text{–}9$. ✓ multiplicative-flow element.
- ADD forms $1/4 = 25\%$ of unordered seam edges. ✗ minority.
- ADD contains no doubling-chain segment and no attractor-involution edge. ✗ not multiplicative-flow.

**MAX is the backbone; ADD is not.**

**Scores.**
- Map A (persistent = ADD): persistent-side (ADD) is NOT the backbone. Score: **−1**.
- Map B (persistent = MAX): persistent-side (MAX) IS the backbone. Score: **+1**.

---

### Source 2 — v1.1 identity-edge finding

**Data.**
- Inherited from v1.1: ADD attaches the ring's multiplicative identity (vertex 1) at $+6.06\sigma$.
- On Z/10: ADD edge is $(1, 2)$, connecting identity to chain-start.

**Rubric (§5.2).** Under §3, is the map's reading coherent?

**Key criterion (§5.2 explicit).** Identity is trivial under multiplication ($1 \cdot x = x$). The identity position is a point where multiplicative structure is *absent*, not where it is most present. A subtype surfacing at the identity is surfacing at a multiplicative-absence, which aligns with the excluded-side reading under §3.

**Coherence evaluation.**
- Map A reading: "ADD-as-persistent attaches the multiplicative invariant." Requires treating identity as a persistent-side position. Under §3 (persistent = multiplicative backbone), identity is a multiplicative-absence, not a backbone element. The Map A reading contradicts §3.
- Map B reading: "ADD-as-excluded surfaces at the multiplicative singularity where multiplicative structure cannot resolve the local content." Under §3, identity is the multiplicative-absence point where excluded content must surface. The Map B reading coheres with §3.

**Scores.**
- Map A: contradicts §3. Score: **−1**.
- Map B: coheres with §3. Score: **+1**.

---

### Source 3 — v1.2-adj leaf-edge finding

**Data.**
- Inherited from v1.2-adj: ADD is a leaf edge of the recovered seam graph (has at least one degree-1 endpoint) at $+3.73\sigma$.
- On Z/10: vertex 1 has degree 1 in the seam graph (appears only in the ADD edge $(1, 2)$). ADD is at the leaf.

**Rubric (§5.3).** Does the excluded-side subtype sit at the graph boundary (leaf position)?

**Leaf evaluation.**
- ADD edge $(1, 2)$ has endpoint vertex 1 with degree 1. ADD is at the leaf.
- MAX edges: $(2, 4)$ has endpoint degrees $(3, 2)$ — interior. $(2, 9)$ has endpoint degrees $(3, 1)$ — has a leaf endpoint. $(4, 8)$ has endpoint degrees $(2, 1)$ — has a leaf endpoint.
- Leaf-status summary: ADD is unambiguously at a leaf (its sole edge has a degree-1 endpoint). MAX has mixed leaf/interior status.
- The inherited v1.2-adj finding transports the ADD-at-leaf relationship across the Path 2 family, not just Z/10 — it is the ADD subtype that consistently occupies the leaf-edge role.

**Scores.**
- Map A (excluded = MAX): Map A's persistent-side (ADD) is at the leaf. Per §5.3: "−1 if persistent-side is at the leaf (inverting the expected boundary role)." Score: **−1**.
- Map B (excluded = ADD): Map B's excluded-side (ADD) is at the leaf. Per §5.3: "+1 if excluded-side subtype is at the leaf." Score: **+1**.

---

### Source 4 — P3AP topology-family finding

**Data.**
- Inherited from P3AP: forest + single connected component + low max degree + low-degree-vertex dominance, transporting across Path 2 family at $+12.56\sigma$ on mean component count.
- On Z/10: seam graph has 4 unordered edges, 5 vertices, max degree 3 (at vertex 2), is a forest, is connected.

**Rubric (§5.4).** Do the topology features come primarily from the persistent-side subtype?

**Topology-feature attribution.**
- **Forest structure.** MAX-only subgraph: 3 edges on 4 vertices, acyclic, path-like with a branch at vertex 2 — a tree. ADD-only subgraph: 1 edge on 2 vertices, trivial tree. Combined: 4 edges on 5 vertices, acyclic, forest. The MAX subgraph is a non-trivial tree spanning $\{2, 4, 8, 9\}$; the forest spine is MAX-dominated.
- **Low max degree.** Overall max degree 3 at vertex 2 (from MAX edges $2\text{–}4$ and $2\text{–}9$ plus ADD edge $1\text{–}2$). In MAX-only subgraph, max degree 2. In ADD-only subgraph, max degree 1. The low-degree profile is primarily MAX-driven.
- **Low-degree-vertex dominance.** In the full seam graph, 4 of 5 vertices (namely 1, 4, 8, 9) have degree ≤ 2; only vertex 2 has degree 3. The low-degree dominance is driven by the chain structure (which is MAX) plus the single ADD leaf.
- **Single connected component.** Requires ADD to connect vertex 1 to the MAX-spanned component. Without ADD, vertex 1 is isolated. This feature is not purely MAX-attributable.

**Majority attribution.** Three of four topology features (forest spine, low max degree, low-degree-vertex dominance) are primarily MAX-attributable. One feature (single connected component) requires both subtypes but specifically needs ADD as the connector. MAX edge count: 3 of 4 = 75%. Persistent-side candidate (MAX) carries the majority of topology features.

**Scores.**
- Map A (persistent = ADD): persistent-side is 1 edge; topology features are primarily driven by the excluded-side (MAX, 3 edges). Per §5.4: "−1 if excluded-side subtype carries the majority of the topology features." Score: **−1**.
- Map B (persistent = MAX): persistent-side is the 3-edge backbone that carries the forest spine, low max degree, and low-degree-vertex dominance. Per §5.4: "+1 if persistent-side subtype carries the majority of the topology features." Score: **+1**.

---

## Aggregate Scores

| Source | Map A | Map B |
|---|---:|---:|
| 1. Seam-graph structural split | −1 | +1 |
| 2. v1.1 identity-edge | −1 | +1 |
| 3. v1.2-adj leaf-edge | −1 | +1 |
| 4. P3AP topology-family | −1 | +1 |
| **Aggregate** | **−4** | **+4** |

**Cleanness gap:** $|S_A - S_B| = |(-4) - (+4)| = 8$.

---

## Pass / Fail / Unclear Evaluation

Per §7.1, PASS requires all three conditions:

| Condition | Threshold | Map B value | Met? |
|---|---|---|:---:|
| Winner score | ≥ +3 | +4 | ✓ |
| Loser score | ≤ +1 | −4 | ✓ |
| Cleanness gap | ≥ 2 | 8 | ✓ |

All three PASS conditions met. Map B is the winner.

---

## Cross-Check With Pilot Analysis

PPM-v1.0 §12 predicted:
- Map A: −4
- Map B: +4
- Cleanness gap: 8
- Predicted outcome: PASS with Map B as winner

Rubric-scored result matches the pilot prediction exactly. No source returned a different score than predicted; no source scored 0 (ambiguous). The framework's reading under the §3 operational interpretation produced a clean 4-of-4 alignment on Map B.

---

## What the Data Shows (Stated Narrowly)

Under the frozen spec of PPM-v1.0:

1. All four frozen data sources, evaluated under the frozen rubric and the frozen operational interpretation, score unambiguously in favor of Map B (MAX = persistent, ADD = excluded).
2. Aggregate score for Map B is $+4$, meeting the $\geq +3$ winner threshold.
3. Aggregate score for Map A is $-4$, well within the $\leq +1$ loser threshold.
4. Cleanness gap of $8$ substantially exceeds the $\geq 2$ requirement.
5. All three PASS conditions in §7.1 are met.

---

## What the Data Does NOT Say

- Nothing about the pair-primitive framework under alternative operationalizations (additive, dual, or otherwise).
- Nothing about rings outside Z/10.
- Nothing about scale-example realizations (neutron, atom, cell, etc.).
- Nothing that upgrades the Path 3 findings (v1.1, v1.2-adj, P3AP). Those sentences stand as originally recorded; this sprint treats them as inherited context only.
- Nothing about whether the §3 operational interpretation is the uniquely correct reading of the framework's vocabulary. §3 was a commitment of this sprint; other operationalizations are not tested here.

Verdict follows in `PAIR_PRIMITIVE_MAPPING_VERDICT.md`.
