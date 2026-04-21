# Comparison Law
## Rules for Comparing Objects in the Program

---

## Purpose

Given an object atlas (`OBJECT_TYPE_ATLAS.md`), the comparison law answers one question: *when you have two objects, can you legitimately compare them?*

Three categories of answer:

1. **Direct comparison permitted.** Objects share type, scope, and generation procedure. Metrics computed on one are interpretable on the other without a bridge.
2. **Bridge comparison required.** Objects differ in path, convention, or generation type, but a meaningful question can be asked across them *if* an explicit bridging rule is pre-registered.
3. **Category mismatch by construction.** Objects are different kinds of thing. No metric can compare them meaningfully; any apparent comparison is semantically empty.

Every sprint that compares two objects must classify the comparison into one of these three categories before freezing.

---

## Rule 1 — Direct Comparison Permitted When ALL Of

A direct comparison between objects $A$ and $B$ is permitted when all of these hold:

- **Same path.** $A$ and $B$ both belong to Path 1, or both to Path 2, or both to Path 3 as Path 3 objects (not as Path 3 bridging inputs).
- **Same carrier family.** $A$ and $B$ live on the same ring, or on the same explicitly-declared family of rings.
- **Same generator type.** Both are theorem-generated, or both are $C_0$-canonical under the same convention, or both are noise-residue at comparable $(N, p, K)$ parameters, or both are recovered from planted overlays under comparable conditions.
- **Same topology type.** Both are scalar, or both are cell sets, or both are graphs on the same kind of vertex set, or both are partitions of the same kind of element set.
- **Same epistemic class.** Both theorem, both observed, both recovered, etc. Mixed-class direct comparison is a bridge, not a direct comparison.

### Examples of direct comparison permitted

- Two per-seed seams at the same $(N, p, \text{carrier})$ with different $r$. Purpose: measure seed-agreement, as in Jaccard stability tests.
- Two corridor closure results under pure $C_0$ at different carriers in the same family. Purpose: test Sprint 25-style closure.
- Two ARI values from shell-partition recovery at different carriers at the same analytic regime. Purpose: test Sprint 26-style shape recovery.
- A recovered persistent seam from a planted experiment compared against the planted seam itself. Purpose: recovery validation, as in S31-pilot-v2.0.

### Examples that look like direct comparison but are NOT

- Published TSML on Z/10 ($h_\text{thm}$) against $C_0$ on Z/10 ($h_\text{ext}$). Different generators → bridge required.
- Path 1 planted theorem seam against Path 2 noise-union seam. Different generator types, different epistemic classes → bridge required at minimum (and may be category mismatch, see Rule 3).
- Basin ratio on Z/10 against basin ratio on Z/14 under the same convention. Same path, same generator, same topology type — but the *measurement* (basin ratio) is a scalar summary. Comparison across carriers at the scalar level is permitted; inferring that the scalar-summary *curve* has a specific shape is a separate question that requires its own metric (which is what S28/S29 tested and failed).

---

## Rule 2 — Bridge Comparison Required When ANY Of

Two objects require a bridge comparison spec when any of these hold:

- **Different paths.** Any comparison between a Path 1 object and a Path 2 object is necessarily a bridge. Path 3 is the name for that bridge.
- **Different attractor convention.** Even within Path 1 (if Path 1 is extended) or within Path 2, if the two objects use different $h$ conventions, direct comparison is unsafe.
- **Different generator types.** Theorem-generated vs noise-residue generated; recovered vs synthetic; per-seed vs persistence-filtered at different parameters — each pair needs an explicit bridging rule.
- **Different epistemic class.** A theorem-level object compared with an observation-level object requires a bridge to state what the relational claim actually means.

### Required elements of a bridge comparison spec

When a sprint requires a bridge, the spec must explicitly state:

1. **Which two paths (or within-path scopes) are being bridged.**
2. **The bridging rule:** what operation takes object $A$ and object $B$ to a commensurable form.
3. **The comparison metric:** what is measured on the commensurable form.
4. **What claim the comparison supports under PASS.** Always bridge-level (relational), never theorem-level, never observation-level.
5. **What claim is ruled out under FAIL.** Narrow; specific to the bridge, not to the objects in isolation.

### Examples of bridge comparisons

- Path 1 theorem seam vs Path 2 discovered seam at the topology level (P3-BridgeA).
- Path 1 canonical $C_0$ cell values vs Path 2 canonical $C_0$ cell values on the same ring (would require a bridge even though the ring is the same — because the conventions differ).
- Theorem-level claim about Z/10 vs observation-level claim about the compatibility family, at the level of shared rule menus.

### Not every possible bridge is worth running

A bridge is legitimate if the two objects are *expected to share something structurally meaningful* under the bridging rule. A bridge that compares objects known in advance to be incompatible is a category mismatch (see Rule 3), not a bridge.

---

## Rule 3 — Category Mismatch by Construction

Some comparisons are semantically empty — the two objects are different kinds of things and no reasonable bridging rule can make them commensurable. These comparisons should not be run, even under a bridge spec, because any metric result is meaningless.

### Examples of category mismatch

- **A theorem-generated designed artifact vs a noise-union accumulation, at the topology level.** Path 1's planted seam is a *fixed-size designed object with hub-and-spokes structure*. Path 2's noise-union seam is a *growing accumulation whose size scales with $n^2$ and whose topology is dominated by density*. Topology metrics on both are computable, but the metrics measure different features of fundamentally different objects. P3-BridgeA documented this by FAIL; the FAIL itself is informative, but only because it cleanly demonstrated the mismatch. Future bridge sprints should not repeat this mismatch.

- **A scalar summary vs a graph.** Comparing $\beta(R_n)$ (a number) to a seam graph (a combinatorial object) at any level requires so much transformation that the result tells us about the transformation, not the objects.

- **A theorem about Z/10 vs an empirical finding about a different carrier, with no specified bridging rule.** Even with same-topology-type metrics, a theorem about a specific ring and an observation about a different ring are different kinds of statement. Asking if they "agree" without specifying what agreement means is ill-defined.

- **Recovered objects at dramatically different parameters.** A persistent seam at $N = 1000, p = 0.02, \pi = 0.50$ and a persistent seam at $N = 100000, p = 0.30, \pi = 0.10$ are not in the same category — the first is a high-signal low-sampling object; the second is a high-noise highly-filtered object. Comparing them directly assumes a commensurability that parameter difference may not preserve.

### How to detect a category mismatch at spec-design time

Ask: *what would a PASS on this comparison concretely mean?* If the answer is "the two objects share some shape" but no specific shape-sharing hypothesis can be named in advance, it is likely a category mismatch. Real bridge claims have the form "if $A$ has property $P$ and $B$ has property $Q$ under mapping $f$, then $f$ is a structural correspondence between $A$ and $B$" — with $P$, $Q$, and $f$ all specified in advance.

Bridge spec design should start from the relational hypothesis, not from "let's see what happens if we measure these things the same way."

---

## Three Quick Tests Before Freezing Any Comparison Spec

### Test 1 — Path and convention coherence

Do both objects use the same path and convention? If yes, proceed to Test 2. If no, specify bridging rule before Test 2.

### Test 2 — Generator type commensurability

Are both objects generated by processes that produce the same kind of thing (small designed artifact vs small designed artifact; growing noise accumulation vs growing noise accumulation)? If yes, proceed to Test 3. If no, re-examine whether the bridging rule in Test 1 (if applicable) actually bridges generator type.

### Test 3 — Metric-object match

Does the chosen metric measure a property both objects meaningfully have? A metric asking "is this a tree?" is meaningful for small cell sets; it is less meaningful for cell sets whose size grows with $n^2$ by construction (where tree-ness becomes structurally impossible at large $n$ regardless of underlying structure).

A spec passing all three tests can be frozen. A spec failing any test must be redesigned before freezing.

---

## Worked Examples Against the Recent Sprints

| Sprint | Direct, bridge, or category mismatch? | Under this law, would it have been allowed? |
|---|---|---|
| S28 basin smoothness | Direct (within Path 2, same scalar type across carriers) | Yes — but the metric (adjacent smoothness) was mis-aimed for the object type. |
| S29 anchored curve | Direct (within Path 2, basin ratios on same family) | Yes — the mismatch was metric-to-hypothesis, not object-type. |
| S30 topology on empty seam | Direct, but on degenerate input | Yes — the mismatch was that the generator produced nothing under tested parameters. |
| S30b persistent-seam detectability | Direct (within Path 2) | Yes — produced negative finding cleanly. |
| S31-pilot-v1.0 | Bridge required but not declared | **No — would have been blocked by Test 1.** |
| S31-pilot-v2.0 | Direct (Path 1 only, scope correctly declared) | Yes. |
| P3-BridgeA-v1.0 | Bridge declared, but object-type mismatch (Test 2 failure) | **Would have been flagged by Test 2 as a probable category mismatch, not a bridge.** |

The comparison law would have caught S31-pilot-v1.0 at Test 1 (different conventions, bridge not declared) and would have flagged P3-BridgeA-v1.0 at Test 2 (Path 1 designed artifact vs Path 2 noise-union have different generator types at the outset). Neither sprint would have been blocked from running entirely — they could have been redesigned with appropriate bridging rules, or with different Path 2 input — but the mismatches would have been visible before freezing.

---

## Authority and Updates

This document defines the comparison law as of the current program state. Updates occur when:

- A new path is added to the program.
- A new object type enters the atlas.
- An existing comparison class is refined based on sprint evidence.

Updates are not silent. Any change to this document is accompanied by a note explaining what changed and why. Prior comparison specs are not retroactively invalidated by updates to this law.

---

## Reading Discipline

This document does not replace the spec freezing process. Every sprint still writes its own pre-registration, declares its own scope, specifies its own metrics and nulls. The comparison law is a sanity check run before freezing — three tests that take under five minutes to apply but would have prevented two of the recent sprint failures.

Apply before freezing. Do not apply retroactively to change verdicts already on the record.
