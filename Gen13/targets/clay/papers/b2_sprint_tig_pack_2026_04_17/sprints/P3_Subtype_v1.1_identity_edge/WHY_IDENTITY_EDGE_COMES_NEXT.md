# Why Identity-Edge Comes Next
## Sprint Design Rationale

---

## The Situation After v1.0

P3-Subtype-v1.0 tested three things in one spec: count proportion, role placement, and adjacency similarity. The literal verdict was UNCLEAR because two of three null-separation sub-conditions failed and one passed at $+3.80\sigma$. The substantive content of the result was narrower than the literal verdict: **one clean structural finding (ADD-role placement transports) wrapped in two methodological failures (count-null degenerate, adjacency metric mis-aligned with chain topology)**.

The temptation at this point is to re-run a broader v1.1 that "fixes the methodology" on all three metrics at once. That temptation should be resisted.

---

## The Narrower Move

The strongest result from v1.0 is the role-placement finding at $+3.80\sigma$. The weaker results are not failures of the underlying hypothesis — they are failures of the spec's chosen null (for counts) and the spec's chosen metric (for adjacency). Those could be fixed, but fixing them is a different research question than the one v1.0 accidentally answered.

The clean question that v1.0 actually answered was: **when the extractor recovers an ADD-rule edge on a Path 2 carrier, does that edge attach an external low-degree vertex to the main seam component?** The answer was yes, 8 of 8 carriers, $+3.80\sigma$ above a random-relabeling null.

A tighter question hiding inside that one is: **does the ADD edge attach the *identity element* specifically, or would any low-degree external vertex do?** On all 8 carriers in v1.0, the ADD edge connected vertex 1 to vertex 2. Vertex 1 is not just any low-degree vertex — it is the ring's multiplicative identity. The adapted role-matching rule from v1.0 (§3.2) was deliberately forgiving because the chain-vs-hub topology mismatch made the original "leaf-to-hub" rule inapplicable; but the actual placement pattern in the data is tighter than the rule required.

Testing the tighter pattern directly is v1.1's sole purpose.

---

## Why Not a Broader v1.1

Three separate temptations exist, and each should be declined:

### Temptation A: Fix the count-null methodology and re-run M1

A better count-test would use a null that varies the overlay-rule assignments before planting (e.g., randomly assign the "ADD" label to 1 of 6 edges during the extension algorithm, then plant and recover). This tests whether the observed 83.3%/16.7% split is more Path-1-like than random rule-assignments would produce.

This is a legitimate sprint. It is not the right next sprint because:

- It introduces a new generator step (random rule assignment pre-planting). That is a new object class, not v1.0's object class.
- It tests a different question (do count proportions transport?) than v1.0's live finding (does ADD placement transport?).
- Mixing "count transport" with "identity-edge transport" in one spec would reproduce v1.0's error of bundling.

### Temptation B: Redesign the adjacency metric for chain topology and re-run M3

A chain-topology-aware adjacency metric would normalize the expected (MM, MA, AA) proportions against the graph's inherent topology-imposed adjacency structure, then ask whether the label placement shifts adjacencies beyond topology-expected values. This is a legitimate metric; it requires a more involved null model.

Also not the right next sprint because:

- It asks about adjacency patterns, which are a finer question than role placement.
- v1.0 showed that role placement transports. Adjacency is downstream of role placement. Until the cleanest form of role placement is confirmed, measuring adjacency conditioned on role placement is premature.

### Temptation C: Test the full three-metric battery with fixed methodologies

Rolling up all three corrections (count null, adjacency metric, identity-edge tightening) into a single v1.1 would produce the exact problem v1.0 had: multiple hypotheses bundled, mixed results, unclear attribution when one fails and others pass. The scope-tag discipline and the comparison law both argue against this.

---

## Why Identity-Edge Specifically

Three reasons:

**First, it is the strongest form of v1.0's live finding.** v1.0 showed that the ADD edge attaches *some* external low-degree vertex to the main component. v1.1 tightens this to *the identity element specifically*. If v1.1 passes, the role-placement finding upgrades from "ADD edges attach a low-degree external vertex" to "ADD edges attach the ring's identity element." That is a structurally more meaningful claim because it ties the transport to an algebraic invariant of the ring (the multiplicative identity) rather than a merely graph-theoretic property (degree-1 vertex).

**Second, it is binary and clean.** For each Path 2 carrier, the question "does the ADD edge touch vertex 1?" has a yes/no answer. Aggregation across the family is trivial (count yes-answers). Null comparison is clean (under subtype-label scrambling, what fraction of random label placements puts the ADD label on an edge incident to vertex 1?). The metric cannot accidentally pass or fail by topology-shape interference.

**Third, it isolates what P3AP and v1.0 established.** P3AP established that topology-family transport holds. v1.0 established that role-placement transport holds at +3.80σ but with methodological issues on the other two metrics. v1.1 isolates the specific, testable, non-methodologically-fragile piece: is identity-element attachment the transportable feature?

---

## What v1.1 Gains By Being Narrow

A narrower sprint has cleaner outcomes:

- **Clean PASS:** "The identity-edge placement pattern transports across the tested Path 2 family at pre-registered significance, under the P3AP extension algorithm." One sentence, precise, attributable.
- **Clean FAIL:** "The identity-edge pattern observed on Path 2 is reproducible by random label-scrambling; identity-element attachment is not a transportable feature." One sentence, precise, attributable.
- **Clean UNCLEAR:** marginal null separation only; no bundled-methodology mixed results.

By not bundling other questions, v1.1 cannot produce v1.0's style of partial-verdict ambiguity. Whatever it returns is unambiguously about identity-edge transport.

---

## What v1.1 Costs By Being Narrow

The obvious cost: it does not close the broader subtype-transport question. Count transport remains untested under any adequate null. Adjacency-pattern transport remains untested under any adequate metric. A subtype bridge at the full resolution v1.0 attempted is still open.

This cost is acceptable because:

- v1.0 did not close those broader questions either (the nulls and metrics were inadequate).
- The atlas and comparison law argue for narrow accumulation over broad assertions.
- A cleanly passing identity-edge bridge sets up successor sprints naturally: count transport under a pre-planting null becomes v1.2-count; adjacency transport under a chain-aware metric becomes v1.2-adj. Each is isolable.

The program's pattern is: narrow sprints whose verdicts compose. v1.1 fits that pattern; a broader "fix everything" v1.1 would not.

---

## Specifically Out of Scope for v1.1

Committed exclusions, enforced by the scope declaration:

- No count-proportion metric (M1 from v1.0).
- No adjacency-pattern metric (M3 from v1.0).
- No new overlay extension (hub-extension and shell-native rules deferred).
- No theorem-level claims.
- No claim about what is "natural" on non-Z/10 carriers.
- No modification of P3AP's recovered seams or extraction process.

The spec will be small. The metric will be binary. The null will be label-scrambling on the same graphs. The verdict will be one of three clean outcomes.

---

## Summary

v1.1 exists to finish answering the one question v1.0's strong finding raised. It does not rescue v1.0; v1.0's UNCLEAR stands. It does not close the subtype bridge as a whole; the broader question remains open. It does answer cleanly, in one number, whether identity-element attachment is the structural feature that transports under the tested extension algorithm.

Narrow. One question. One metric (with its binary structural variant). One null. One verdict. That is the correct successor design under this program's discipline.
