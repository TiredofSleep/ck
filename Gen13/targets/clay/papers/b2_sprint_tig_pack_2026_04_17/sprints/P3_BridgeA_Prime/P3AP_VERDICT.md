# P3AP Verdict
## P3-BridgeA-Prime-v1.0 — Final Determination

---

## Verdict: **PASS**

First confirmed Path 3 bridge.

---

## One-Paragraph Justification

Under the pre-registered pass criteria of P3-BridgeA-Prime-v1.0 §8.1, all six sub-conditions are met. Family-level topology metrics — forest fraction, mean component count, max-degree band fraction, low-degree-profile fraction — all reach ceiling values (1.000 each). The active structural signal, mean component count, separates from its matched-density null by +12.56σ below null mean (real $\mu_k = 1.0$; null mean = 4.41; null std = 0.27), decisively exceeding the 2σ threshold. The forest and low-degree-profile metrics are also at ceiling, though their null separations are degenerate (null std = 0 because random graphs with 3–6 edges on 14–89 vertices are essentially always forests of sparse low-degree graphs). The recovery quality is perfect: Jaccard, recall, and precision all equal 1.000 on every one of the 8 Path 2 carriers, confirming that the low-$N$ + persistence extractor validated on Z/10 (S31-pilot-v2.0) generalizes without adjustment to the tested carrier family under the pre-registered overlay-extension algorithm (doubling-chain + identity-edge + attractor-involution). Per anti-tuning rules §9, no thresholds are adjusted post-hoc. The verdict is PASS as specified — a bridge-level claim at the topology-family level, scoped tightly per the pre-registered bounds.

---

## Minimal Permitted Claim Under PASS

Per `WHY_A_PRIME_IS_NOW_VALID.md` §"The Honest Scope of A-Prime," the strongest sentence this PASS supports is:

> Under the specified overlay-extension algorithm (doubling-chain + identity-edge + attractor-involution), planted-recovery artifacts on Z/14, Z/22, Z/34, Z/42, Z/46, Z/58, Z/74, and Z/94 share topology-family features (forest-ness, single connected component, low max degree, dominance of low-degree vertices) with the Z/10 theorem seam's planted-recovery artifact, at $+12.56\sigma$ above matched-density random-graph baseline on mean component count.

Nothing beyond that sentence is supported by this sprint.

---

## What This PASS Does Establish

1. **The extractor architecture generalizes.** The low-$N$ + persistence extractor, validated at ceiling on Z/10 in S31-pilot-v2.0, recovers planted artifacts at ceiling on 8 additional carriers. This is not trivial — a tool validated on one ring does not automatically work on others.

2. **The overlay-extension algorithm produces recoverable artifacts.** The doubling-chain + identity-edge + attractor-involution rule, applied to each Path 2 carrier with its own $h_\text{ext}$, produces overlays that the extractor recovers cleanly. The pre-flight audit correctly removes the 2 attractor-involution cells per carrier where planted value would coincide with canonical value, preventing the S31-pilot-v1.0 invisible-cell failure mode.

3. **Topology family preservation holds at the broad level.** All 8 Path 2 recovered seams are forests with a single component and max degree 2. Z/10 is a forest with a single component and max degree 3. The *family-level* structural features — tree-ness, connectivity, low degree — are shared across paths.

4. **Null comparison is not degenerate.** Real mean component count ($\mu_k = 1.0$) is sharply separated from null mean (4.41) by more than 12σ. This is an active structural signal, not a density artifact.

---

## What This PASS Does NOT Establish

1. **No theorem is extended to non-Z/10 carriers.** The Path 1 theorem remains proven only on Z/10. A-Prime does not add theorem status to any carrier.

2. **The overlay-extension algorithm is not proven "natural" or "unique."** It is one specific algorithmic choice, frozen in the spec. Other extension rules (shell-native, direct lift from Sprint 21, etc.) could produce different artifacts. A future sprint could test an alternative extension.

3. **Finer topology features differ between paths.** The diagnostic hub concentration metric $H$ shows a real structural difference: Z/10 has a hub-and-spokes shape ($H = 0.75$, one dominant hub vertex of degree 3), while Path 2 carriers produce chain topology ($H \in \{0.33, 0.67\}$, no dominant hub). The *family-level* features are shared; the *specific shape* within the family differs because the doubling-chain extension produces sequential rather than branching connections. This is a known limitation of the extension algorithm, not a flaw in the bridge.

4. **Rule-subtype transport is not tested.** MAX/ADD classification of cells was not evaluated in this sprint (it would require a subtype-mix diagnostic, which is outside the pre-registered metrics). Whether the MAX/ADD partition on Z/10 has analogs on Path 2 carriers is a separate question for a future sprint.

5. **No physics, ontology, or real-world claim.** Everything above remains within the taxonomy work the atlas frames.

---

## Diagnostic Note: The Chain-vs-Hub Distinction

An honest reading of the PASS must address the $H$ difference:

- **Z/10 under theorem overlay:** 4 edges, tree, one hub (vertex 2, degree 3). $H = 0.75$.
- **Path 2 under extension overlay:** 3–6 edges per carrier, tree, linear chain. $H \in \{0.33, 0.67\}$.

This is because the doubling-chain rule inherently produces sequential connections (2→4→8→16→...), each vertex in the chain connecting only to its predecessor and successor. There is no structural branching on Path 2 side, while Z/10's theorem seam has structural branching at vertex 2 (connecting to 1, 4, and 9). The ADD component adds the $\{1, 2\}$ edge on both sides, contributing to Z/10's branching but leaving Path 2 as a mostly-separate two-component structure before the attractor-involution pair connects things.

This diagnostic observation is worth recording because:
- It is a real feature of the data that PASS does not hide.
- It suggests a specific future sprint direction: an overlay-extension algorithm that *branches* (e.g., including all pairs $(c_i, c_j)$ with $j > i$ rather than just adjacent pairs, or including multiple chains rooted at different small vertices) would produce Path 2 artifacts closer to Z/10's hub-and-spokes shape.
- It narrows the bridge claim honestly: the bridge holds at the family level (forest + connected + low-degree), not at the specific-shape level (hub-and-spokes vs chain).

---

## Actions Following PASS

Per P3-BridgeA-Prime-v1.0 §11 under PASS:

1. **Record the PASS.** First confirmed Path 3 bridge in the program.
2. **Update the local-vs-transferred split document.** Add an entry under "confirmed transport" qualified tightly: "P3-BridgeA-Prime-v1.0: planted-recovery artifacts share forest + connected + low-degree family features across Path 1 and Path 2 under doubling-chain + identity-edge + attractor-involution extension."
3. **Update the object-type atlas.** The "Path 3 bridge topology comparison object" entry gets its current status updated from "P3A FAIL; bridge lane closed for noise-union Path 2 input" to "P3A FAIL with noise-union input; P3AP PASS with planted-recovery input at family-level topology."
4. **Do not promote the extension algorithm.** It remains a heuristic.
5. **Future bridge sprints may be designed.** Specifically: (a) finer topology test (hub-and-spokes recovery), (b) subtype mix test, (c) alternative overlay extensions, (d) bridge on a different object entirely (shell partition, corridor closure).

---

## Program State After P3AP

Eight sprints under pre-registration discipline:

| Sprint | Path | Verdict | Note |
|---|---|---|---|
| S28-v1.0 | 2 | FAIL | Basin smoothness (null inverted) |
| S29-v1.0 | 2 | FAIL | Anchored curve (no depth-organization) |
| S30-v1.0 | 2 | PASS vacuous | Empty seams at high N |
| S30b-v1.0 | 2 | FAIL | No seam under uniform noise on pure $C_0$ |
| S31-pilot-v1.0 | cross-path (undeclared) | FAIL | Convention mismatch |
| S31-pilot-v2.0 | 1 | effective PASS | Ceiling recovery on theorem object |
| P3-BridgeA-v1.0 | 3 | FAIL | Object-type mismatch (noise-union input) |
| **P3-BridgeA-Prime-v1.0** | **3** | **PASS** | **First confirmed bridge, family-level topology** |

Two PASSes now on the record. Six informative negatives. Every result has clean attribution. The atlas/law/selector framework has enabled this outcome by forcing correct object-type matching before freezing.

---

## Integrity Statement

The PASS is recorded honestly with its full scope boundaries. All primary metrics are at ceiling; the active null separation is +12.56σ; the recovery is perfect. The diagnostic hub-concentration difference is documented, not hidden. The permitted claim is scoped tightly. This is the first Path 3 bridge that holds up, and it holds up at the exact level the spec committed to test — no more, no less.
