# Pair-Primitive Mapping on Z/10 — Pre-Registration
## First Rigorous Checkpoint for the Pair-Primitive Framework

---

## Scope Declaration

**Path:** Local Theorem Chart (Path 1).
**Attractor convention:** $h_\text{thm} = 7$ (Z/10 theorem scope).
**Claim class:** structural-fit claim at the local theorem chart, conditional on the framework's vocabulary.
**Canonical construction source:** Path 1 published Z/10 TSML with the 3-layer tower decomposition (92 canonical + 6 MAX seam + 2 ADD seam = 100).
**Relation to prior sprints:**
- Operates entirely on the Path 1 Z/10 seam data.
- Treats the three Path 3 findings (P3AP, v1.1, v1.2-adj) as inherited context only, not as new test data.
- Does NOT re-score any Path 3 sprint's result.
- Does NOT extend to rings outside Z/10.
- Does NOT invoke hub-extension, new generator, or any physical / scale example.

**Explicit framework dependency:** the test operates under the pair-primitive framework's vocabulary as specified in `HOLD_GAP_FLOW_FOUNDATION.md`. A FAIL of this sprint is a specific structural retraction within that framework, not a theorem.

---

**Status:** FROZEN pending user approval.
**Version:** PPM-v1.0 (Pair-Primitive Mapping, version 1.0).
**Change policy:** once any data source is scored against this spec, the spec cannot be edited. Amendments require v1.1+ and a fresh evaluation.

---

## 1. Hypothesis Under Test (Exactly One)

**Hypothesis (PPM-H).** Under the pair-primitive framework's vocabulary applied to Z/10's multiplicative operation structure, exactly one of the two candidate mappings of the ADD/MAX subtypes to the pair's two readings produces a coherent structural fit across four data sources, with a pre-registered cleanness gap over the alternative.

The alternative (null) hypothesis is that neither map produces a clean structural fit, or that both maps fit comparably and the data does not force a choice.

---

## 2. The Two Candidate Mappings (Frozen)

### Map A

- **ADD** = persistent-side reading of the pair (hold).
- **MAX** = excluded-side reading of the pair (gap).

### Map B

- **MAX** = persistent-side reading of the pair (hold).
- **ADD** = excluded-side reading of the pair (gap).

These are the only two possible binary mappings of the two subtypes to the two pair-readings. The sprint tests both with the same rubric and scores each map against each data source.

---

## 3. Operational Interpretation of the Framework's Vocabulary (Frozen)

The pair-primitive framework uses "persistent-side" and "excluded-side" abstractly. This sprint fixes a specific operational interpretation for testing on the Z/10 seam:

**Persistent-side reading (frozen for this sprint):** the subtype that forms the structural backbone of the seam graph under Z/10's multiplicative operation structure — the connected substructure that carries the majority of the seam's edges and aligns with the ring's multiplicative flow (doubling chain, attractor-involution).

**Excluded-side reading (frozen for this sprint):** the subtype that constitutes a localized departure from the multiplicative operation structure — edges that import a non-multiplicative rule and surface at boundary positions rather than in the backbone interior.

This interpretation is the sprint's operational commitment. A different interpretation of the framework's vocabulary might yield different scores. The pre-reg acknowledges this: the sprint tests the pair-primitive framework **under this specific operationalization on Z/10's multiplicative structure**, not the framework under all possible operationalizations.

**Justification for this operationalization:** Z/10's published TSML is fundamentally a multiplicative structure (with an 8-cell residue). The 2×2 theorem places both additive and multiplicative structures as co-present, but the table and its canonical construction are multiplicatively framed. The multiplicative reading is therefore the natural operation structure under which to score the seam.

---

## 4. The Four Data Sources (Frozen)

### Source 1 — Seam-graph structural split

The 8 seam cells decompose as:
- **MAX subtype:** 6 cells forming the edges (2,4), (4,2), (2,9), (9,2), (4,8), (8,4). Unordered-edge count: 3 edges on vertex set {2,4,8,9}. Includes the doubling-chain segment 2-4-8 and the attractor-involution edges between 2 and 9.
- **ADD subtype:** 2 cells forming the edges (1,2), (2,1). Unordered-edge count: 1 edge on vertex set {1,2}.

### Source 2 — v1.1 identity-edge finding (inherited)

Under the P3AP overlay-extension across 8 Path 2 carriers, the ADD subtype attaches the ring's multiplicative identity (vertex 1) at $+6.06\sigma$. On Z/10 specifically, the 2 ADD cells connect vertex 1 (the identity) to vertex 2.

### Source 3 — v1.2-adj leaf-edge finding (inherited)

Under the same extension, the ADD subtype is a leaf edge of the recovered seam graph (has at least one degree-1 endpoint) at $+3.73\sigma$. On Z/10 specifically, vertex 1 has degree 1 in the seam graph (it appears only in the ADD edge (1,2)).

### Source 4 — P3AP topology-family finding (inherited)

The seam graph's global topology features (forest, single connected component, low max degree, low-degree-vertex dominance) transport across the Path 2 family at $+12.56\sigma$ on mean component count. On Z/10 specifically, the seam graph has max degree 3 (at vertex 2), is a forest, and is connected when ADD and MAX edges are taken together.

---

## 5. The Scoring Rubric (Frozen)

Each (map, source) pair gets a binary score in $\{-1, 0, +1\}$ per a frozen rubric.

### Source 1 rubric: Structural backbone

**Question:** Does the map's persistent-side subtype form the structural backbone of the seam graph?
**Backbone definition:** the connected subgraph carrying the majority (≥ 50%) of the seam's edges and containing the ring's multiplicative-flow elements (doubling chain and/or attractor).
**Scoring:**
- $+1$ if persistent-side subtype forms the backbone.
- $-1$ if persistent-side subtype does NOT form the backbone (i.e., excluded-side subtype does).
- $0$ if neither subtype clearly dominates.

### Source 2 rubric: Identity-element anchoring

**Question:** Under the map, does the ADD subtype's identity-element attachment support a coherent reading?
**Coherent readings:**
- Map A coherence (ADD = persistent): "ADD-as-persistent attaches the ring's multiplicative invariant (identity), reading the algebraic hold of the identity element through the persistent subtype." This is coherent IFF the identity is treated as a persistent invariant of the multiplicative structure.
- Map B coherence (ADD = excluded): "ADD-as-excluded surfaces at the ring's multiplicative singularity (identity, where multiplication is trivial), reading the gap where multiplicative structure cannot resolve the local content." This is coherent IFF the identity is treated as a multiplicative trivialization point where excluded content must surface.
**Scoring:**
- $+1$ if the map's reading of v1.1 is structurally coherent under the operational interpretation in §3.
- $-1$ if the map's reading contradicts the operational interpretation in §3.
- $0$ if both interpretations are equally plausible under §3.

**Key criterion for §3 compliance:** the operational interpretation fixes persistent-side = multiplicative backbone. The identity is trivial under multiplication (multiplicative structure vanishes at 1·x = x). Therefore the identity position is a point where multiplicative structure is *absent*, not where it is most present. A subtype surfacing at the identity is surfacing at a multiplicative-absence, which is the excluded-side reading.

### Source 3 rubric: Boundary vs interior placement

**Question:** Does the map's excluded-side subtype sit at the graph boundary (leaf position), as predicted by the "excluded = boundary" reading of gap in the framework?
**Scoring:**
- $+1$ if excluded-side subtype is at the leaf.
- $-1$ if persistent-side subtype is at the leaf (inverting the expected boundary role).
- $0$ if neither subtype is clearly at the leaf.

### Source 4 rubric: Topology-feature dominance

**Question:** Do the transport-confirmed topology features (forest, single-component, low-degree profile) come primarily from the map's persistent-side subtype?
**Topology-feature attribution:** the topology features listed transport under P3AP's extension, which preserves both subtypes. Inspection: the 6-cell MAX subtype (3 unordered edges on vertices {2,4,8,9}) forms the chain-structured forest with max degree 2 on that vertex set; the 2-cell ADD subtype (1 unordered edge on {1,2}) adds vertex 1 as a leaf and increases vertex 2's degree to 3. The bulk of the forest structure (3 of 4 unordered edges) is MAX. The single-component property requires both subtypes (without ADD, vertex 1 is isolated).

**Scoring:**
- $+1$ if persistent-side subtype carries the majority of the topology features (forest + low-degree structure).
- $-1$ if excluded-side subtype carries the majority of the topology features.
- $0$ if both subtypes contribute equally.

---

## 6. Aggregate Score and Cleanness Gap (Frozen)

For each map, aggregate score = sum of four per-source scores. Range: $[-4, +4]$.

**Cleanness gap** = $\text{score}_A - \text{score}_B$ in absolute value: $|S_A - S_B|$.

---

## 7. Pass / Fail / Unclear Criteria (Frozen)

### 7.1 PASS

Sprint passes if all three conditions hold:
1. One map has aggregate score $\geq +3$.
2. The other map has aggregate score $\leq +1$.
3. Cleanness gap $\geq 2$.

The winning map is named in the verdict and earns the sentence in §9.

### 7.2 FAIL

Sprint fails if neither map reaches $+3$.

### 7.3 UNCLEAR

Sprint returns UNCLEAR if:
- One map has aggregate score $\geq +3$ but cleanness gap $< 2$ (i.e., loser also scored high), OR
- Both maps have score in $\{+2, +3\}$ with cleanness gap $< 2$.

---

## 8. Anti-Tuning Rules

1. The rubric in §5 is frozen. No rubric component is added or removed after the score is computed.
2. The operational interpretation in §3 is frozen. No alternative interpretation may be invoked post-hoc to change a score.
3. The four data sources in §4 are frozen. No additional data source is added.
4. The cleanness threshold in §7 is frozen. No adjustment post-hoc.
5. Scoring proceeds source-by-source; the scorer does NOT see aggregate progress before all four sources are scored.
6. If FAIL or UNCLEAR, no re-run with adjusted rubric; successor requires v1.1+.

---

## 9. Verdict Sentences (Frozen)

| Outcome | Sentence |
|---|---|
| PASS (Map A winner) | "Under the pair-primitive framework's vocabulary applied to Z/10's multiplicative operation structure with the operational interpretation in PPM-v1.0 §3, Map A (ADD = persistent, MAX = excluded) produces a coherent structural fit across the four pre-registered data sources at cleanness gap $\geq 2$." |
| PASS (Map B winner) | "Under the pair-primitive framework's vocabulary applied to Z/10's multiplicative operation structure with the operational interpretation in PPM-v1.0 §3, Map B (MAX = persistent, ADD = excluded) produces a coherent structural fit across the four pre-registered data sources at cleanness gap $\geq 2$." |
| FAIL | "Under the pair-primitive framework's two candidate mappings on Z/10's 8 seam cells with the operational interpretation in PPM-v1.0 §3, neither mapping reaches the pre-registered aggregate-score threshold. The framework's first checkpoint does not cash out on the local theorem chart under this interpretation." |
| UNCLEAR | "The pair-primitive framework's mapping on Z/10's 8 seam cells is not decidable from the data sources under the operational interpretation in PPM-v1.0 §3 at the pre-registered cleanness threshold. Specific disagreements are documented in the results." |

---

## 10. Scope Boundaries (Frozen)

**Tests:**
- Whether one of two binary mappings fits a frozen rubric on four specific data sources under a frozen operational interpretation.

**Does NOT test:**
- Whether the pair-primitive framework is correct in general.
- Whether the mapping on Z/10 extends to other rings in the compatibility family.
- Whether the framework's vocabulary admits other valid operational interpretations.
- Whether the scale-example schema (neutron, atom, cell, etc.) holds.
- Whether any Path 2 or Path 3 finding should be upgraded.
- Any physical, ontological, or cross-domain claim.

---

## 11. Integrity Check Against Comparison Law

- **Test 1 — path/convention coherence:** single path (Path 1, $h_\text{thm} = 7$), no cross-path bridging → ✓.
- **Test 2 — generator type commensurability:** all four data sources come from the same object class (Z/10 seam, measured on either the theorem chart directly or the P3AP extension of the theorem chart) → ✓.
- **Test 3 — metric-object match:** structural rubric on seam graphs with known subtype labels — no shape-entanglement because each rubric item is defined in terms of the subtype's role in the graph structure, not in terms of a density that would be confounded by topology choice → ✓.

All three tests pass. Spec eligible for freezing.

---

## 12. Honest Prediction (Not a Target)

Pilot analysis on the four data sources under the operational interpretation in §3:

- **Source 1 (backbone):** MAX forms 3 of 4 unordered edges and contains the doubling chain 2-4-8 and the attractor-involution 2-9. ADD forms 1 edge at the identity. MAX is the backbone.
- **Source 2 (identity):** Identity is a multiplicative trivialization point (1·x = x). Under the §3 interpretation (persistent = multiplicative backbone), identity is a multiplicative-absence point where excluded content must surface. ADD at identity supports ADD = excluded.
- **Source 3 (leaf):** ADD edge has vertex 1 as a degree-1 endpoint. ADD is at the leaf. Under "excluded = boundary," ADD = excluded.
- **Source 4 (topology):** 3 of 4 unordered seam edges are MAX. The forest structure's spine is the MAX-dominated chain {2,4,8,9}. Topology features primarily come from MAX.

Predicted scores:
- Map A: $-1 + -1 + -1 + -1 = -4$.
- Map B: $+1 + +1 + +1 + +1 = +4$.
- Cleanness gap: $|+4 - (-4)| = 8$.

Predicted outcome: **PASS with Map B as winner**.

This prediction does NOT modify any threshold. The sprint's actual scoring is done by the rubric in §5, not by this pilot. If the rubric-scored result differs from the pilot (e.g., one source turns out to be ambiguous and scores 0 rather than $\pm 1$), the verdict follows the rubric-scored result.

**What the pilot teaches us operationally:** the sprint is expected to return a clean verdict because the four data sources point consistently under the §3 interpretation. If any source returns a different score than predicted, that is diagnostically interesting — it would indicate a place where the framework's reading is less forced than the pilot suggests.

---

## 13. Deliverables (Post-Execution)

Written to `/home/claude/foundation_sprint/ppm_v1/`:

- `PPM_V1_RESULTS.md` — per-source scoring with rubric citations, aggregate scores, cleanness gap.
- `PPM_V1_VERDICT.md` — one-paragraph determination per the §9 table.
- `PPM_V1_REPRO.md` — reproducibility notes: the rubric is deterministic over fixed data, so any scorer applying §5 to the §4 data under §3 should return the same aggregate. Repro checks that the rubric is unambiguous when read directly.

---

## 14. Frozen Choices Awaiting Approval

Four choices for review:

1. **Operational interpretation** in §3 (persistent = multiplicative backbone). Acceptable?
2. **Four data sources** in §4. Acceptable?
3. **Scoring rubric** in §5 (binary per source with frozen criteria). Acceptable?
4. **Thresholds** in §7 ($\geq 3$ winner score, $\leq 1$ loser score, $\geq 2$ cleanness gap). Acceptable?

If approved: freeze as PPM-v1.0 and execute the rubric evaluation.
If revised: note changes, re-freeze under new version, then execute.
