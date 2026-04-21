# Why Subtype Comes Before Hub Extension
## Sprint Ordering Rationale

---

## The Two Candidates for the Next Path 3 Sprint

After P3-BridgeA-Prime's PASS at the topology-family level, two natural directions exist:

**A — Subtype-mix bridge.** Same object class as P3AP. Test whether the internal seam structure (MAX-like edges, ADD-like edges, role-based placement) is preserved across paths, not just the coarse topology.

**B — Hub-extension bridge.** Introduce a new overlay-extension rule designed to produce hub-and-spokes structure on Path 2 carriers, matching Z/10's specific shape. Test whether a different heuristic recovers the finer structure that the doubling-chain rule left as chains.

Both are legitimate. The question is order.

---

## Why Subtype First

### 1. Subtype uses the validated object class without modification

The P3AP object class — planted-recovery artifacts under $N = 10n^2$, $p = 0.10$, $K = 10$, $\pi = 0.50$, with doubling-chain + identity-edge + attractor-involution extension — is exactly the class that produced the passing bridge. The artifacts are already generated, already recovered at ceiling, already sitting in `P3AP_PATH2_GRAPHS.json`. A subtype sprint can operate on those exact artifacts without regenerating data or introducing new heuristics.

Hub-extension, by contrast, introduces a new overlay rule whose behavior is unknown. That rule has two uncertainties: does the new rule produce hub structure by construction, and does the extractor recover it cleanly. Even if both work, the hub-extension sprint answers a question about a different object class than the one already validated.

Principle: exhaust the questions a validated object can answer before introducing a new object.

### 2. Subtype has two possible failure modes, each informative

If subtype fails, the failure tells us something specific about which of two hypotheses is true:

- **Failure mode A:** subtype count vectors differ significantly across paths. This says the rule proportions themselves (MAX vs ADD) do not transport — Z/10's 75%/25% split is not a universal property.
- **Failure mode B:** subtype counts match but placement differs — e.g., Z/10's ADD edges are adjacent to MAX edges in a specific way, but Path 2 doesn't reproduce that adjacency pattern. This says the rule proportions transport but their *arrangement* does not.

Both failures are learnable. Hub-extension, by contrast, has a less diagnostic failure: if a new overlay rule doesn't produce hub structure, the conclusion is ambiguous — was the rule wrong, or is there no hub structure to find?

Principle: prefer sprints whose failure modes teach distinct things.

### 3. Subtype tests a claim the program has actually implicitly made

The program's working vocabulary treats "MAX" and "ADD" as real rule types that partition the theorem's seam. Sprint 25 tested the corridor closure $\{\text{MAX}, \text{MIN}\}$ on pure $C_0$ and found it. The theorem's published overlays explicitly use MAX on 6 cells and ADD on 2 cells. If these rule-type distinctions are real structural features rather than arbitrary labels, they should appear in the planted-recovery artifacts across paths.

A subtype bridge sprint operationalizes this implicit claim. It asks: when we recover planted seams on Path 2 under the extension algorithm, do we see the MAX/ADD partition at predictable proportions and in predictable roles within the seam graph?

Hub-extension tests a different claim: that a specific shape (hub-and-spokes vs chain) can be engineered via overlay choice. That is an interesting question but secondary to whether the rule-type vocabulary itself transports.

Principle: test the existing program's implicit claims before adding new ones.

### 4. Subtype failure does not invalidate P3AP; hub failure slightly muddies it

If subtype fails cleanly, P3AP's family-level PASS stands. The conclusion becomes: "coarse topology transports, but internal subtype structure does not, under this extension." That is a well-scoped finding.

If hub-extension fails, the interpretation gets messier: either the new rule is wrong, or hub structure is Z/10-specific, and attributing is hard without the subtype question already answered. Subtype is the question that cleanly separates "family-level bridges exist" from "specific-shape bridges exist" — it sits structurally between P3AP and any future hub sprint.

Principle: sprint ordering should avoid creating ambiguity about what prior sprints established.

### 5. The atlas supports the subtype sprint cleanly

Subtype-mix is an entry in `OBJECT_TYPE_ATLAS.md` §4.5 of the A-Prime metric set — noted as "diagnostic only" there because A-Prime was committing to topology-level only. A promotion from diagnostic to primary in a new sprint is exactly the kind of progression the atlas was built to support. The object type is the same (planted-recovery artifact under noise); the metric changes.

Hub-extension would require a new entry in the atlas for "hub-extended overlay" as an object class distinct from the doubling-chain class already tested. That is a legitimate atlas addition but a larger step.

Principle: follow the atlas's natural progression paths.

---

## The Specific Ordering

The sprint ladder from here, if each passes:

1. P3AP topology-family bridge. **PASSED.**
2. Subtype-mix bridge on same object class.
3. If subtype passes: subtype-structural bridge (role placement, adjacency patterns) at finer resolution.
4. If subtype fails on mix: alternative overlay rules (including hub-extension) as a new sprint family.
5. If subtype fails on placement but not mix: that tells us the ADD/MAX labels transport but their arrangement does not — prompting Sprint 3-with-placement-fix or a shell-native rule.

Hub-extension enters this ladder at step 4 or 5, not step 2.

---

## What Subtype Is Not

A subtype bridge is still a topology-plus-labeling test. It does not test:

- Cell identity across carriers.
- Exact rule equality beyond labels (a MAX-like edge on Z/14 has value $\max(c_i, c_{i+1})$; a MAX-like edge on Z/10 has value $\max(2, 4) = 4$; these are both "MAX-type" but the specific numerical values differ).
- Whether the MAX/ADD vocabulary is the right partition to describe the seams — it is the partition the theorem uses, and we are testing whether it transports, but a richer or coarser partition might describe the data better.

These limits are what make subtype a clean next step. It extends P3AP by one level of resolution (coarse topology → topology + edge labels), without opening the door to much finer questions that would require new pre-registrations.

---

## Summary

Subtype before hub because:

- Same object class, no new generator.
- Failure modes are informative and distinct.
- Tests an existing program claim implicit in the MAX/ADD vocabulary.
- Keeps P3AP's verdict clean regardless of subtype outcome.
- Follows the atlas's natural progression (diagnostic → primary on same object).

Hub-extension remains a legitimate sprint. It is the right move *after* subtype has been answered either way, not before.
