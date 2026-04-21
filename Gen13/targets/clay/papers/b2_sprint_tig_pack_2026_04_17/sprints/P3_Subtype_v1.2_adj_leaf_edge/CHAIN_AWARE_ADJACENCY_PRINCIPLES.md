# Chain-Aware Adjacency — What the Metric Must Preserve
## Short Note on Design Requirements

---

## The Failure Mode a New Metric Must Avoid

v1.0's M3 adjacency metric compared Path 2 carrier adjacency vectors (MM, MA, AA) against Path 1's (0.5, 0.5, 0.0) using Bhattacharyya similarity. It failed because of a structural asymmetry:

- Path 1's adjacency vector arises from a *hub-and-spokes tree* with one vertex of degree 3.
- Path 2's adjacency vectors arise from *linear chains* with max degree 2.

Given the same underlying rule ("ADD edge attaches the identity element to the main chain"), the two topologies produce different (MM, MA, AA) ratios:

- On hub topology: the identity-attached ADD edge is adjacent to 2 MAX edges at the hub vertex → 2 MA adjacencies. Plus 1 MM adjacency at another hub-incident vertex. Ratio: 1 MM : 2 MA → after normalization, (0.33, 0.67) — but due to vertex indexing that produces (0.5, 0.5, 0.0) in Z/10's specific case.
- On chain topology: the ADD edge is adjacent to 1 MAX edge at its chain-interior endpoint. The rest of the chain produces 4 MM adjacencies along chain interior. Ratio: 4 MM : 1 MA → (0.80, 0.20, 0.00).

Neither ratio is "right" — they are both correct outputs of the same relative-role rule applied to different shapes.

The metric penalized Path 2 for not reproducing Path 1's ratio *even when the underlying relative role was identical*. Random label-scrambling on chain graphs could produce more "balanced" ratios by placing ADD at interior positions, making null mean higher than real.

A chain-aware metric must not repeat this error.

---

## What "Chain-Aware" Must Mean

The metric must measure a property that is *invariant under topology change when the underlying relative role is preserved*. Equivalently: two configurations that embody the same relative role should produce the same metric value regardless of whether the host graph is a hub or a chain.

Three specific design principles follow.

### Principle 1 — Measure Role, Not Ratio

The metric should compute a *role attribute* of the ADD edge rather than a family-level adjacency ratio. Role attributes describe what the ADD edge *does* in its graph, not what fraction of adjacencies involve it.

Examples of role attributes that transfer between hub and chain topology:

- "The ADD edge is a leaf edge" (one endpoint has degree 1): Yes on Path 1 (vertex 1 has degree 1), yes on Path 2 chains (vertex 1 has degree 1 on the chain). Invariant.
- "The ADD edge is the *only* non-MAX edge incident to its main-component endpoint": Yes on Path 1 (vertex 2 is incident to 1 ADD + 2 MAX; the ADD is the only ADD); yes on Path 2 (vertex 2 is incident to 1 ADD + 1 MAX; the ADD is the only ADD). Invariant.
- "The ADD edge bridges between the main-component body and a degree-1 external vertex": Yes on Path 1 (vertex 2 in main body, vertex 1 external); yes on Path 2 (vertex 2 in chain body, vertex 1 external). Invariant.

These all say the same thing in different language. They describe what the ADD edge does, not how many adjacencies of each type exist.

### Principle 2 — Use Graph-Relative Distances, Not Raw Adjacency Counts

Raw adjacency counts are shape-dependent by construction (long chains produce lots of same-type adjacencies along their interior). Graph-relative distances measure how the ADD edge positions itself relative to distinguished vertices *after* accounting for the graph it lives in.

Useful graph-relative quantities:

- **Distance from ADD edge to main MAX component.** On Path 1: the ADD edge (1,2) shares vertex 2 with the MAX edges incident to vertex 2; distance is 0 (shared endpoint). On Path 2 chains: same; distance 0. Invariant.
- **Distance from ADD edge to attractor position** (vertex $h$). On Path 1: vertex 2 is 1 step from vertex 9 (via the (2,9) MAX edge). The ADD edge's main-component endpoint is 1 step from $h$. On Path 2: after audit, $h$ may not even be in the recovered seam graph (attractor-involution pairs were audit-removed). This is a legitimate shape difference that a metric should register but not penalize — unless the hypothesis specifically claims hub-to-attractor proximity.

### Principle 3 — Compare Invariants, Not Absolute Values

The metric's pass/fail structure should compare a role-invariant property between Path 1 and Path 2, and the null should shuffle labels in a way that varies the invariant, not in a way that gets trapped by shape.

For v1.0's adjacency metric, label-scrambling kept the graph fixed and shuffled labels. Under chain topology, random label placement could produce (MM, MA, AA) ratios closer to Path 1's hub-derived ratio by placing ADD in interior positions. This was a shape artifact.

For a role-invariant metric like "is the ADD edge's degree-1 endpoint the identity element?" — label-scrambling can answer meaningfully: under random label placement, what fraction of placements have a degree-1 endpoint equal to vertex 1? That fraction is computable from graph structure alone. Real versus null becomes a legitimate comparison.

---

## A Concrete Candidate Metric

Combining the three principles, a candidate metric is **ADD-edge role signature**:

For each carrier's recovered seam, compute the 3-tuple $(L, M, I)$ where:

- $L \in \{0, 1\}$: 1 iff the ADD edge has at least one degree-1 endpoint.
- $M \in \{0, 1\}$: 1 iff the ADD edge's higher-degree endpoint is in the main MAX-connected-component.
- $I \in \{0, 1\}$: 1 iff the ADD edge's degree-1 endpoint is vertex 1 (identity element).

Path 1's Z/10 ADD edge (1, 2): vertex 1 has degree 1, vertex 2 has degree 3 and is in the main MAX component (connected to 4, 9 via MAX), vertex 1 is the identity. Signature: $(1, 1, 1)$.

Path 2 on each carrier: vertex 1 has degree 1, vertex 2 has degree $\geq$ 2 and is the chain-start (in main component), vertex 1 is the identity. Signature: $(1, 1, 1)$.

Path 1 and Path 2 share signature $(1, 1, 1)$ across the entire tested family. The signature is topology-invariant: it does not depend on whether vertex 2's degree is 3 (hub) or 2 (chain-endpoint); only that it is $\geq 2$ and in the main MAX component.

$I$ is exactly v1.1's metric. $L$ and $M$ are new. The composite signature lets us ask a graded question — is the whole role signature preserved, or only parts of it?

---

## What the Null Model Should Do

For each carrier's recovered seam graph, the null should scramble subtype labels (the validated null from v1.1), preserve edge counts, and compute the signature on the scrambled labeling.

The null asks: given random labeling of the same graph, how often does the signature $(L, M, I)$ equal $(1, 1, 1)$?

Across 100 replicates × 8 carriers, compare to real's 8/8 match rate.

The signature is binary per carrier, so it produces a well-defined discrete distribution under label-scrambling. No topology artifact, no shape-driven bias. It tests whether the *composite role signature* is preserved beyond chance.

---

## What This Adjacency Sprint Does Not Test

- Adjacency ratios in the v1.0 (MM, MA, AA) sense. Those are shape-dependent and not the right question.
- Whether MAX edges occupy specific roles. That would require a separate MAX-role metric.
- Whether the ADD edge's position reflects any *algebraic* property beyond identity-element attachment. The signature covers three aspects; finer algebraic features would require new metrics.
- Cell-identity correspondence across carriers.
- Theorem transport.
- Hub-extension questions.

---

## One Subtle Issue To Watch

The composite signature $(L, M, I)$ has three components. The $I$ component is essentially v1.1's identity-edge test. Reporting the full signature alongside the $I$ component risks *double-counting the v1.1 result*: if $I = 1$ across all carriers (which we already know), then the signature's success on $I$ is not new information, and reporting a composite signature match of 8/8 overstates the new content.

The correct framing: the new content from this sprint is the $L$ and $M$ components *conditional on* $I$. The pre-reg should make this explicit by structuring the metric as "given identity-attachment holds (from v1.1), do the $L$ and $M$ components also hold at null significance?"

This avoids rediscovering v1.1's finding under a different name.

---

## Summary

A chain-aware adjacency metric must:

1. Measure role, not ratio.
2. Use graph-relative distances or binary role indicators, not raw adjacency counts.
3. Compare invariants that are preserved across hub and chain topology when the underlying rule is the same.
4. Not rediscover v1.1's identity-edge finding in a different form.

The candidate metric — composite ADD-edge role signature with $L$ (leaf endpoint), $M$ (main-component attachment), $I$ (identity element) components, with $I$ held constant by v1.1 — meets these requirements. The pre-reg builds on this candidate.
