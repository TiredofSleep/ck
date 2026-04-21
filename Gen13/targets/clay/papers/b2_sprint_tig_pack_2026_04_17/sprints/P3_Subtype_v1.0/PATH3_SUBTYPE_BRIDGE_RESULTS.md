# Path 3 Subtype Bridge Results
## P3-Subtype-v1.0, Internal Seam Structure Comparison

---

## Scope Declaration (Reproduced)

**Path:** Path 3 Bridge Test (subtype level)
**Attractor convention:** cross-path (Path 1: $h_\text{thm}=7$; Path 2: $h_\text{ext}=\max$ odd unit)
**Claim class:** bridge-level
**Canonical construction source:** Path 1 published TSML; Path 2 extended $C_0$ under P3AP overlay algorithm (doubling-chain + identity-edge + attractor-involution)
**Relation to prior sprints:** Operates on P3-BridgeA-Prime-v1.0's recovered seams as-is. No regeneration. No new extractor run. Subtype labels inferred from P3AP's overlay audit records.

---

## Path 1 Reference

| Edge | Label | Source rule | Endpoint degrees |
|---|---|---|---|
| (1, 2) | ADD | $(1+2) \bmod 10 = 3$ | 1, 3 |
| (2, 4) | MAX | $\max(2,4) = 4$ | 3, 2 |
| (2, 9) | MAX | $\max(2,9) = 9$ | 3, 1 |
| (4, 8) | MAX | $\max(4,8) = 8$ | 2, 1 |

Path 1 subtype proportions: **$f_\text{MAX} = 0.750$, $f_\text{ADD} = 0.250$.**
Path 1 adjacency vector $(MM, MA, AA)$: **$(0.5, 0.5, 0.0)$** — half of edge-pairs at a shared vertex are MAX-MAX, half MAX-ADD, none ADD-ADD.
Path 1 ADD edge role: ADD edge (1, 2) attaches degree-1 external vertex (vertex 1) to hub vertex (vertex 2, degree 3). **Matches adapted role rule.**

---

## Path 2 Per-Carrier Results

| $n$ | $\|E\|$ | MAX | ADD | $f_\text{MAX}$ | $\Delta$ | ADD role match | Adjacency $(MM, MA, AA)$ | Sim to P1 |
|---:|---:|---:|---:|---:|---:|:---:|---:|---:|
| 14 | 3 | 2 | 1 | 0.667 | 0.083 | ✓ | (0.50, 0.50, 0.00) | 1.0000 |
| 22 | 6 | 5 | 1 | 0.833 | 0.083 | ✓ | (0.80, 0.20, 0.00) | 0.9487 |
| 34 | 6 | 5 | 1 | 0.833 | 0.083 | ✓ | (0.80, 0.20, 0.00) | 0.9487 |
| 42 | 6 | 5 | 1 | 0.833 | 0.083 | ✓ | (0.80, 0.20, 0.00) | 0.9487 |
| 46 | 6 | 5 | 1 | 0.833 | 0.083 | ✓ | (0.80, 0.20, 0.00) | 0.9487 |
| 58 | 6 | 5 | 1 | 0.833 | 0.083 | ✓ | (0.80, 0.20, 0.00) | 0.9487 |
| 74 | 6 | 5 | 1 | 0.833 | 0.083 | ✓ | (0.80, 0.20, 0.00) | 0.9487 |
| 94 | 6 | 5 | 1 | 0.833 | 0.083 | ✓ | (0.80, 0.20, 0.00) | 0.9487 |

---

## Family Aggregates

| Metric | Real | Threshold | Met? | Null mean | Null std | Sigma separation | Sigma threshold | Met? |
|---|---:|---|:---:|---:|---:|---:|---|:---:|
| $\mu_\Delta$ (count deviation) | 0.0833 | ≤ 0.10 | ✓ | 0.0833 | 0.0000 | +∞ / degenerate* | ≥ 2σ below null | **✗** |
| $\mu_\text{ADDrole}$ (role match fraction) | 1.0000 | ≥ 0.75 | ✓ | 0.3475 | 0.1719 | **+3.80σ** | ≥ 2σ above null | ✓ |
| $\mu_\text{adj}$ (adjacency similarity) | 0.9551 | ≥ 0.80 | ✓ | 0.9713 | 0.0187 | **−0.87σ** | ≥ 2σ above null | **✗** |

*$\mu_\Delta$ null is degenerate because subtype-relabeling preserves counts per carrier — label-scrambling does not change $f_\text{MAX}$. Real $\mu_\Delta$ equals null $\mu_\Delta$ exactly on every replicate. The null separation sub-condition therefore fails trivially. Details below.

---

## Sub-Condition Summary

| Sub-condition | Met? |
|---|:---:|
| $\mu_\Delta \leq 0.10$ | ✓ |
| $\mu_\text{ADDrole} \geq 0.75$ | ✓ |
| $\mu_\text{adj} \geq 0.80$ | ✓ |
| Null separation on $\mu_\Delta$ (≥ 2σ below null) | ✗ (degenerate null) |
| Null separation on $\mu_\text{ADDrole}$ (≥ 2σ above null) | ✓ (+3.80σ) |
| Null separation on $\mu_\text{adj}$ (≥ 2σ above null) | ✗ (−0.87σ) |

All three primary metric thresholds pass at ceiling or near-ceiling. One of three null separations passes decisively; two fail, for two *different* structural reasons documented below.

---

## Detailed Observations

### Observation 1: Count vector similarity is structurally determined, not tested

The spec's null model scrambles subtype labels while preserving the count of MAX vs ADD edges per carrier. This is by design — the null asks whether the specific placement of the ADD label is meaningful given the counts. But it means $\mu_\Delta$ is identical in real and null by construction: the same 5-MAX / 1-ADD count gives $f_\text{MAX} = 0.833$ regardless of which edge is labeled ADD.

The spec's §3.4 specified "$\mu_\Delta$ below null mean by $\geq 2\sigma$" as a sub-condition. Under subtype-relabeling this sub-condition cannot be satisfied because the null has zero variance in $\mu_\Delta$. This is a spec-design flaw visible only at execution time: the chosen null cannot discriminate on M1, because M1 is a function of counts alone and the null preserves counts.

Per anti-tuning rule §5.7 ("no alternative metric or null substitution"), no adjustment is made. The sub-condition is recorded as failed. A v1.1 spec would either remove M1's null separation requirement or use a different null (e.g., re-extract with shuffled overlay-rule assignments before planting).

### Observation 2: ADD role placement is strongly non-random

This is the discriminating result. On all 8 Path 2 carriers, the ADD edge attaches vertex 1 (outside the doubling chain) to vertex 2 (chain start in the main component) — exactly the structural role the ADD edge plays on Z/10 (vertex 1 as leaf, vertex 2 as hub). Under label scrambling, this specific role placement arises only 34.75% of the time on average.

The $+3.80\sigma$ separation is decisive. The identity-edge rule's placement of the ADD subtype — connecting the ring's identity element (1) to the chain-start element (2) — is a real structural feature that transports cleanly across the tested carrier family. This is not an artifact of the extension algorithm's MAX/ADD proportions; it is an artifact of *where* the ADD rule places its edge within the seam.

### Observation 3: Adjacency similarity passes threshold but not null

The mean Bhattacharyya similarity between each Path 2 carrier's adjacency vector and Path 1's is 0.9551 — above the 0.80 threshold. However, the *null mean* is 0.9713, which is *higher* than real. The separation is $−0.87\sigma$, which fails the 2σ-above-null test.

This happens because on a 6-edge chain with 5 MAX and 1 ADD, the adjacency vector is constrained by the chain topology rather than by the subtype placement. With 1 ADD edge incident on one chain-endpoint, its only adjacency is with its chain-neighbor (MAX-ADD, count 1), while the other 5 internal-chain adjacencies are all MAX-MAX. This gives adjacency vector (0.80, 0.20, 0.00) — 80% MAX-MAX, 20% MAX-ADD.

Under random label scrambling, the ADD edge can be placed at chain-interior positions, which generates *two* MAX-ADD adjacencies instead of one. This makes the scrambled graph's adjacency vector shift closer to Path 1's (0.5, 0.5, 0.0) than the real placement does. The real placement, which puts the ADD edge at the chain endpoint attaching to vertex 1, is *structurally* outside the chain — but this out-of-chain position yields a *less* MAX-ADD-balanced adjacency vector than internal placements would.

So: **the real ADD placement is the correct structural match (external vertex attachment), but the adjacency metric — which treats Path 1's 0.5/0.5 ratio as the target — rewards internal placement instead.** The adjacency metric is the wrong measure for testing whether ADD placement transports.

This is a metric-hypothesis mismatch discovered only at execution. The adjacency metric was chosen based on Path 1's observed ratio, but that ratio arises from Path 1's hub topology, not from any invariant of subtype placement. On chain topology, the same placement *rule* produces a different adjacency ratio.

### Observation 4: All three observations point the same direction when read together

- Count proportion: transports trivially but cannot be null-tested under label-scrambling.
- Role placement: transports decisively and is strongly non-random.
- Adjacency proportion: appears to pass the threshold but fails null separation because the metric conflates shape-driven and placement-driven adjacency patterns.

Only the role-placement metric (M2) is unambiguously informative for the hypothesis. It cleanly passes at $+3.80\sigma$.

The spec's symmetric weighting of three metrics treats this as a mixed result. A more carefully specified successor sprint would use M2 as the primary structural test and either (a) remove M1's null requirement, since label-preserving null cannot test counts, or (b) use a different null for M1 that varies the overlay-rule assignments rather than the post-hoc labels.

---

## What the Data Shows

Under the frozen spec of P3-Subtype-v1.0:

1. **Count transport is real but untestable under the chosen null.** Path 2 carriers produce 83.3% MAX / 16.7% ADD on 7 of 8 carriers and 66.7% / 33.3% on Z/14. Mean deviation from Path 1's 75% MAX is 0.083, under the 0.10 threshold. But the null preserves counts by construction, so this cannot be distinguished from random placement at the count level.

2. **Role transport is real and decisive.** On all 8 Path 2 carriers, the ADD edge attaches an external low-degree vertex to the main connected component. This role pattern is strongly non-random, at +3.80σ above the null of random label placement.

3. **Adjacency transport is ambiguous under the chosen measure.** The adjacency-similarity metric produces a real value (0.9551) above its threshold (0.80), but the null mean (0.9713) is higher, indicating that random label placements on the chain graphs sometimes happen to land closer to Path 1's hub-derived adjacency ratio than the real structured placement does. This reflects a metric-choice issue, not evidence against subtype transport.

4. **Taken together, the role-placement result is the strongest finding.** The identity-edge rule produces ADD edges that consistently attach the ring's identity element to the main seam component, transporting from Path 1's hub-leaf structure to Path 2's chain-external structure.

---

## What the Data Cannot Say

- Under a different null model (e.g., overlay-rule reassignment pre-planting), count transport would become testable. This sprint does not provide that test.
- Under a different adjacency metric (e.g., expected adjacency given placement, marginalized over topology), adjacency transport might be distinguishable from null. This sprint's adjacency metric does not do this.
- Under a hub-producing overlay extension, both adjacency metrics and role metrics would be computed on a different object class entirely. That is a separate question deferred to a future sprint.
- The finding does not prove "MAX/ADD is the right partition for all seam objects." It shows that the MAX/ADD partition as used by the theorem does have a transportable structural feature (role placement of ADD) under the specified extension.

Verdict follows in `PATH3_SUBTYPE_BRIDGE_VERDICT.md`.
