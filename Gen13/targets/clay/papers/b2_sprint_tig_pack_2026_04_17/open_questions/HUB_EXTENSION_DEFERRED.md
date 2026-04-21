# Hub Extension — Deferred
## Short Note on a Deliberately Unrun Sprint Family

---

## What It Is

A "hub-extension overlay rule" would be an alternative overlay-extension algorithm for Path 2 carriers, designed to produce hub-and-spokes topology (matching Path 1's Z/10 shape) rather than the chain topology that the P3AP extension produces.

Under P3AP, Path 2 seams have $d_\max = 2$ and chain structure. Under Z/10's theorem, the seam has $d_\max = 3$ with one dominant hub vertex (vertex 2). A hub-extension rule would place multiple overlay edges at a single vertex to reproduce hub shape.

## Why It Is Deferred

Per `WHY_BRIDGE_A_FIRST.md` (in `sprints/P3_BridgeA_Prime/`): introducing a new overlay-extension rule would add a second uncertainty to any bridge test. A failure under a hub-extension sprint could be attributed either to the bridge hypothesis being false, or to the new extension rule being a poor choice. Clean attribution requires testing bridges on validated extension rules first.

P3-BridgeA-Prime-v1.0 passed on topology family; P3-Subtype-v1.1 passed on identity-element; P3-Subtype-v1.2-adj passed on leaf-edge. All three under the same P3AP extension. Each finding is scoped as conditional on the P3AP rule specifically.

## What Would Make Hub Extension Live

A hub-extension sprint becomes authorized when:

1. A specific hub-extension rule is designed with explicit generator declaration.
2. The rule is validated (e.g., pilot recovery confirms the rule's planted artifacts are recoverable at ceiling under noise, analogous to S31-pilot-v2.0's validation of the P3AP extension on Z/10).
3. A new Path 3 bridge spec is pre-registered with scope declaration naming the new extension family.

Until steps 1–3 are complete, hub extension is not a sprint candidate.

## What Hub Extension Would Test

Once authorized, a hub-extension sprint could test whether the bridge findings that transport under P3AP also transport under a different rule-to-shape mapping. Specifically:

- Does identity-element attachment (v1.1) persist when the extension produces a hub topology rather than a chain topology?
- Does the leaf-edge pattern (v1.2-adj) transport when the ADD edge is no longer naturally at a chain endpoint?
- Do the topology-family features (P3AP) hold on hub artifacts?

These are legitimate questions for future sprints, but each requires its own pre-registration.

## Not In Scope

This note does not propose a specific hub-extension rule. It does not specify parameters. It does not predict outcomes. It documents only the deliberate deferral and the conditions under which the deferral would be lifted.
