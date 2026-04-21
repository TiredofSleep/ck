# Why Additive Comes Next
## Sprint Ordering Rationale

---

## The Situation After PPM-v1.0

PPM-v1.0 passed under one specific operationalization of the pair-primitive framework. The frozen clarification in that sprint made the narrowness explicit: the checkpoint evaluated the framework under a **multiplicative** reading of Z/10's seam, not under every possible reading the framework admits.

That narrowness was disciplined rather than incidental. The foundation note's 2×2 theorem places Z/10Z with four co-present structures: additive structure, multiplicative structure, additive flow, multiplicative flow. No one of them is the primary reading; their refusal to collapse into each other is what forces T* = 5/7. A checkpoint that tests the framework under only the multiplicative reading has only tested one of the four structural lenses the framework is supposed to hold under.

PPM-v1.1 exists to close the most structurally symmetric gap: the additive reading. Multiplicative and additive are the two base operation structures of the ring. Flows (additive flow, multiplicative flow) are their dynamic readings. Running the additive operationalization next completes the pair of static readings before any other sprint is attempted.

---

## What "Additive Operationalization" Concretely Means

The multiplicative reading in PPM-v1.0 §3 fixed:

- **Persistent-side** = structural backbone under Z/10's multiplicative operation structure; connected substructure aligning with doubling chain and attractor-involution.
- **Excluded-side** = localized departure from multiplicative structure; imports a non-multiplicative rule, surfaces at boundary positions.

An additive operationalization reads the same seam under the ring's additive structure instead. The base change affects what counts as "backbone" and what counts as "departure." Specifically:

- Under the additive structure, the ADD rule $T(x,y) = (x+y) \bmod 10$ *is* the native operation. It is not an import or a departure. It is the operation structure itself applied at the cell.
- Under the additive structure, the MAX rule $T(x,y) = \max(x,y)$ is the non-additive rule — it does not respect addition, it imports an order-based choice, and it surfaces at positions where the additive rule would not produce the table's value.

The map-to-pair assignment therefore has to be redone from scratch under this different operational lens. Nothing about PPM-v1.0's result is transferred. The rubric gets the same binary per-source structure but the rubric's reading of "backbone" vs "departure" changes because the operation structure changed.

---

## Three Possible Outcomes, Each With a Clear Meaning

**Outcome 1 — Map stays B (MAX = persistent, ADD = excluded) under additive reading.**

This would mean the mapping is not symmetric between the two base operation structures. One subtype plays the persistent role in both readings, the other plays the excluded role in both. Structurally this would be a strong claim: the pair primitive has a dominant operation structure on Z/10 (probably multiplicative, since the ring's TSML is multiplicatively framed), and the additive reading inherits the multiplicative assignment rather than producing its own. The framework would be "asymmetric" at the operational level.

**Outcome 2 — Map flips to A (ADD = persistent, MAX = excluded) under additive reading.**

This would mean the mapping is operation-structure-dependent in a specific way: whichever subtype aligns with the active operation structure plays the persistent-side role. Under multiplication, MAX aligns (it is closer to a multiplicative-shape rule); ADD does not (it imports a different rule). Under addition, ADD aligns (it is the additive rule); MAX does not (it imports the order-based choice). The framework would be "symmetric" at the operational level — both operations get a valid reading where their native subtype is persistent. This is arguably what the 2×2 theorem's symmetry would predict.

**Outcome 3 — Neither map fits cleanly under additive reading (FAIL or UNCLEAR).**

This would mean the additive reading does not cash out on the seam data with the same discipline as the multiplicative reading. The seam is characterized primarily by multiplicative structure (per Z/10's TSML framing), and the additive reading might not produce enough structure to score clean per-source binaries. The framework would be "multiplicatively loaded" — it works when read multiplicatively but not additively, at least on this ring.

Each outcome teaches something distinct. The sprint is worth running because its three outcomes have non-overlapping structural consequences for how the framework should be understood on Z/10.

---

## Why Additive Before Anything Else

The authorized successors after PPM-v1.0 PASS were:

- PPM-v1.1: additive operationalization check
- PPM-v2.0: extension to Path 2 carriers outside Z/10
- PPM-v3.0: additional framework-derived checkpoint on different Z/10 data

Of these, v1.1 goes first because:

**It tests the operationalization question directly.** The framework's status after PPM-v1.0 is "passed under one operationalization." Until we know whether the framework is operationalization-stable or operationalization-dependent on Z/10, extending to other rings or other data sources amplifies the uncertainty. If v1.1 shows the mapping flips under additive reading, a v2.0 run on Path 2 carriers becomes two sprints (one per operationalization) rather than one. Establishing the operationalization landscape on Z/10 first makes every successor sprint cheaper to design.

**It uses the same data.** No new extraction, no new generator, no new object class. The 8 seam cells, the three inherited Path 3 findings — all identical to v1.0. Only the rubric's operational interpretation changes. This makes v1.1 the cheapest possible successor, and cheap successors should run first when each teaches something useful.

**It stays on Path 1.** Expanding to Path 2 carriers (v2.0) crosses a path boundary and requires bridge discipline. Staying on Path 1 keeps this checkpoint in the simplest possible scope-class.

**It completes a natural symmetry.** The 2×2 theorem has four co-present structures. PPM-v1.0 tested one (multiplicative). PPM-v1.1 tests its pair (additive). The two flow structures (additive flow, multiplicative flow) would be later sprints if authorized. Completing the static-structure pair first gives the program a symmetric pair of readings before attempting dynamic ones.

---

## What PPM-v1.1 Does Not Do

- It does not test the framework under every possible operationalization. Flow-based readings (additive flow, multiplicative flow) are not included. Dual-operation readings are not included. v1.1 is strictly the additive static-structure counterpart to v1.0's multiplicative static-structure.
- It does not extend to rings outside Z/10.
- It does not re-run any Path 3 sprint.
- It does not change v1.0's verdict. PPM-v1.0 PASS stands as originally recorded.
- It does not authorize scale examples, physics, or ontology, regardless of outcome.

---

## What the Rubric Needs to Change

PPM-v1.0's rubric was designed for multiplicative reading. For additive reading, three of the four rubric criteria need re-specification:

- **Source 1 (backbone):** backbone under multiplicative reading was the doubling chain and attractor-involution. Under additive reading, the backbone would be whatever substructure of the seam graph aligns with additive flow on Z/10 (cycles modulo 10, sum-based rules, etc.). The rubric needs to specify what counts as additive backbone.
- **Source 2 (identity-edge reading):** under multiplicative reading, identity was a multiplicative-absence point (1·x = x trivial). Under additive reading, the additive identity is 0, not 1. Vertex 1 is not the additive identity; it is a unit with additive content. The rubric's key criterion needs a different structural argument under additive reading.
- **Source 3 (leaf-edge):** this rubric was about graph boundary placement. It is more operation-structure-neutral than the others — leaves are leaves regardless of whether we read multiplicatively or additively. But the interpretation of "excluded = boundary" may need re-examination under additive reading.
- **Source 4 (topology-family):** similarly, topology features are more structure-neutral. But the attribution of which subtype's edges carry the topology features may read differently if we identify additive backbone with ADD edges.

The pre-reg will specify the additive-reading rubric for each source. The structural symmetry with v1.0 will be preserved where possible; where asymmetry is forced by the operation-structure change, the rubric will document the asymmetry explicitly.

---

## The Honest Prediction (To Be Disclosed in the Pre-Reg)

Pilot inspection suggests Outcome 2 (the map flips to A under additive reading) is most likely, because:

- Under additive structure, ADD is the native rule and MAX is the import. This inverts the multiplicative situation.
- The identity-element finding (v1.1) reads differently under additive reading because vertex 1 is not the additive identity (0 is). The "identity-element attachment" finding becomes less structurally anchored under additive reading — vertex 1 is just a unit, not a multiplicative trivialization point.
- The leaf-edge finding (v1.2-adj) is topology-neutral; it reads the same way regardless of operation structure, so its scoring should not flip.
- The topology-family finding (P3AP) attributes backbone features to whichever subtype dominates the edge count. MAX dominates the edge count (3 of 4 unordered edges), so under additive reading where MAX is excluded, the topology features come from the excluded side — inverting the rubric's expected direction.

Predicted per-source scoring under additive reading:
- Source 1: if additive backbone is ADD-associated, Map A wins (+1 for A, -1 for B). If additive backbone is still structurally MAX-associated regardless of operation reading, Map B wins. This source will be the most rubric-sensitive one.
- Source 2: under additive reading, identity at vertex 1 is less structurally meaningful. Possible score: 0 (neutral) for both maps, since the multiplicative-absence argument doesn't apply.
- Source 3: leaves are leaves. ADD is at the leaf. Under excluded-as-boundary reading, Map B wins. But this source is operation-structure-neutral so may be less diagnostic.
- Source 4: topology features are dominated by MAX edges. Under additive reading where MAX is excluded, topology-dominance-by-excluded inverts Map B's expected direction. Map A wins here.

Predicted aggregate under additive reading: Map A ≈ +2, Map B ≈ 0. Margin is tighter than v1.0's +4/−4, and may not exceed the cleanness-gap threshold of 2. The most likely outcome is **Outcome 3** (FAIL or UNCLEAR), with a secondary probability of **Outcome 2** (Map A wins cleanly).

Prediction does not modify thresholds. The sprint's rubric will decide. A PASS for Map A would be a genuine flip. A FAIL would be a diagnostic signal that the additive reading does not discriminate on this seam. An UNCLEAR would isolate the specific source(s) where the additive rubric fails to be decisive.

---

## Summary

PPM-v1.1 is the narrowest next checkpoint because it uses the same data, the same object class, and the same Path 1 scope as v1.0, but substitutes a single well-defined axis (operational interpretation). Its three possible outcomes each teach something structurally distinct about the pair-primitive framework on Z/10. Running it before v2.0 or v3.0 establishes the operationalization landscape on the simplest ring before extending anywhere.

The sprint does not make the framework broader. It tests whether the checkpoint's result is a property of the framework or of the operational interpretation. That distinction is necessary for every successor sprint to be correctly scoped.
