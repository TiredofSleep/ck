# PPM-v1.1 — Additive Operationalization Pre-Registration
## Parallel Checkpoint to PPM-v1.0 Under the Ring's Other Base Operation Structure

---

## Scope Declaration

**Path:** Local Theorem Chart (Path 1).
**Attractor convention:** $h_\text{thm} = 7$ (Z/10 theorem scope).
**Claim class:** structural-fit claim at the local theorem chart, conditional on the framework's vocabulary under additive operationalization.
**Canonical construction source:** Path 1 published Z/10 TSML with the 3-layer tower decomposition.
**Relation to prior sprints:**
- Inherits object class, data sources, and rubric *structure* from PPM-v1.0.
- Substitutes the §3 operational interpretation from multiplicative to additive.
- Does NOT re-score PPM-v1.0's verdict.
- Does NOT re-score any Path 3 sprint's verdict.
- Does NOT extend to rings outside Z/10.

**Inherited wording clarification:** This sprint evaluates the pair-primitive framework under an **additive** operationalization only; the verdict refutes or confirms that operationalization, not the framework in all possible readings.

---

**Status:** FROZEN per user's Execute direction.
**Version:** PPM-v1.1 (additive operationalization).
**Change policy:** once any source is scored, the spec cannot be edited.

---

## 1. Hypothesis Under Test

**Hypothesis (PPM-v1.1-H).** Under the pair-primitive framework's vocabulary applied to Z/10's **additive** operation structure via the rubric in §5, exactly one of Map A or Map B produces a coherent structural fit across the four data sources at the pre-registered cleanness threshold.

Null: neither map reaches the threshold under the additive reading, or both fit comparably without cleanness.

---

## 2. Candidate Mappings (Inherited from v1.0)

- **Map A:** ADD = persistent-side, MAX = excluded-side.
- **Map B:** MAX = persistent-side, ADD = excluded-side.

---

## 3. Operational Interpretation — Additive (FROZEN)

**Persistent-side reading:** the subtype forming the structural backbone under Z/10's additive operation structure; connected substructure aligning with additive flow (cyclic addition mod 10, additive-flow elements).

**Excluded-side reading:** the subtype constituting a localized departure from additive operation structure; imports a non-additive rule and surfaces at boundary positions relative to additive structure.

**Justification:** The 2×2 theorem places both multiplicative and additive structures as co-present on Z/10. v1.0 tested the multiplicative reading. This sprint tests the additive reading, completing the static-structure pair. The additive operation on Z/10 is the cyclic group structure $(\mathbb{Z}/10, +)$; the "additive flow" is the cyclic orbit of 1 generating the group.

**Key structural facts under additive reading:**
- The additive identity on Z/10 is **0**, not 1.
- Vertex 1 is the additive generator (generates the cyclic group under addition).
- The ADD rule $T(x,y) = (x+y) \bmod 10$ **is** the additive operation itself — it is the native rule under additive reading.
- The MAX rule $T(x,y) = \max(x,y)$ is order-based and does not align with additive structure — it is the imported rule under additive reading.

---

## 4. Data Sources (Inherited Verbatim from v1.0)

No changes. The four data sources remain:

1. Seam-graph structural split (MAX: 3 unordered edges on {2,4,8,9}; ADD: 1 edge on {1,2}).
2. v1.1 identity-edge finding (ADD attaches vertex 1 at +6.06σ).
3. v1.2-adj leaf-edge finding (ADD is a leaf edge at +3.73σ; vertex 1 has degree 1).
4. P3AP topology-family finding (forest + single-component + low max degree at +12.56σ on mean component count).

---

## 5. Scoring Rubric — Rewritten Where Operation-Dependent (FROZEN)

### Source 1 rubric: Structural backbone under additive reading

**Question:** Does the map's persistent-side subtype form the additive backbone?

**Additive backbone definition (§3-consistent):** the connected subgraph carrying the majority (≥ 50%) of the seam's edges **AND** containing the ring's additive-flow elements (cells where the additive rule produces the table value; edges within the additive cyclic structure).

**Evaluation under strict AND criterion (preserving v1.0 structure):**
- ADD: 1 of 4 unordered edges = **25% (minority)**. Contains additive-flow elements (ADD cells literally apply the additive rule).
- MAX: 3 of 4 unordered edges = **75% (majority)**. Does NOT contain additive-flow elements (MAX rule is non-additive).
- **Neither subtype satisfies both AND-conditions.**

**Scoring:** When no subtype is the backbone under the strict criterion:
- Map A (persistent = ADD): ADD is not the backbone (fails majority). Score: **0** (not -1, because "not backbone" doesn't invert a framework expectation; it just fails to meet the positive criterion).
- Map B (persistent = MAX): MAX is not the backbone (fails native-flow alignment). Score: **0**.

### Source 2 rubric: Identity-edge reading under additive reading

**Question:** Under §3 (additive operationalization), does the map's reading of "ADD at vertex 1" cohere?

**Key criterion under additive reading:** Vertex 1 is **not** the additive identity (additive identity is 0, which is in the V0 boundary of the TSML and outside the seam graph). Vertex 1 is the additive generator. The structural parallel to v1.0's "identity is a multiplicative trivialization point" argument does not transfer — the additive generator is where additive structure is most *productive*, not absent.

**Scoring:** When the original finding's structural anchor (multiplicative identity) has no clean parallel under additive reading, the finding becomes non-diagnostic under this operationalization:
- Map A: no coherent additive reading of "ADD at generator" parallels v1.0's multiplicative argument. Score: **0**.
- Map B: no coherent additive reading parallels v1.0's multiplicative argument. Score: **0**.

**Alternative interpretations considered and rejected:**
- "ADD at generator = persistent at flow origin" (would score Map A +1) was rejected because this is not structurally parallel to v1.0's "excluded at trivialization" — it introduces a new structural argument not derived from the framework's vocabulary.
- "ADD at generator = excluded at flow origin" (would score Map B +1) was rejected for the same reason.

The principled choice is 0/0, acknowledging that the finding's structural anchor is multiplicative-specific and does not translate.

### Source 3 rubric: Leaf-edge placement (INHERITED — topology-neutral)

Rubric unchanged from v1.0 §5.3. Leaf status is a topological fact independent of operation-structure reading.

**Evaluation:** ADD is unambiguously at the graph boundary (vertex 1 has degree 1; ADD edge (1,2) is a leaf edge).
- Map A (persistent = ADD): persistent is at the leaf. Per rubric: **-1** (inverting expected boundary role).
- Map B (excluded = ADD): excluded is at the leaf. Per rubric: **+1**.

### Source 4 rubric: Topology-feature dominance (INHERITED — topology-neutral)

Rubric unchanged from v1.0 §5.4. Topology features are attributed by edge-count majority independent of operation reading.

**Evaluation:** MAX carries 3 of 4 unordered edges, forest spine on {2,4,8,9}, low-degree profile.
- Map A (persistent = ADD): persistent does NOT carry majority of topology features. Per rubric: **-1**.
- Map B (persistent = MAX): persistent DOES carry majority. Per rubric: **+1**.

---

## 6. Aggregate and Cleanness Gap

Same structure as v1.0. Aggregate range $[-4, +4]$; cleanness gap $= |S_A - S_B|$.

---

## 7. Pass / Fail / Unclear Criteria (Inherited from v1.0)

### 7.1 PASS
One map ≥ +3 AND other ≤ +1 AND cleanness gap ≥ 2.

### 7.2 FAIL
Neither map reaches +3.

### 7.3 UNCLEAR
One map ≥ +3 but cleanness gap < 2, OR both maps in {+2, +3} with cleanness gap < 2.

---

## 8. Anti-Tuning Rules (Inherited)

All v1.0 §8 rules apply. Specifically: the rubric in §5, the operational interpretation in §3, the data sources in §4, and the thresholds in §7 are all frozen. No post-hoc adjustment.

---

## 9. Verdict Sentences (FROZEN)

| Outcome | Sentence |
|---|---|
| PASS (Map A) | Under the pair-primitive framework's vocabulary applied to Z/10's additive operation structure with the operational interpretation in PPM-v1.1 §3, Map A (ADD = persistent, MAX = excluded) produces a coherent structural fit at pre-registered cleanness. |
| PASS (Map B) | Under the pair-primitive framework's vocabulary applied to Z/10's additive operation structure with the operational interpretation in PPM-v1.1 §3, Map B (MAX = persistent, ADD = excluded) produces a coherent structural fit at pre-registered cleanness. |
| FAIL | Under the pair-primitive framework's vocabulary applied to Z/10's additive operation structure with the operational interpretation in PPM-v1.1 §3, neither map reaches the pre-registered aggregate-score threshold. The additive operationalization does not cash out decisively on the local theorem chart. |
| UNCLEAR | Under the additive operationalization, one or both maps score in the ambiguous range at the pre-registered cleanness threshold. Specific disagreements are documented. |

---

## 10. Scope Boundaries

**Tests:** whether the additive operationalization of the framework produces a coherent mapping on Z/10's seam under the frozen rubric.

**Does NOT test:** multiplicative operationalization (v1.0 territory), other rings, scale examples, cross-operation synthesis, framework correctness in general.

**v1.0's PASS stands unchanged regardless of v1.1's verdict.**

---

## 11. Honest Prediction

Pilot analysis:

- Source 1 under strict AND criterion: ADD has native-flow alignment but minority edges; MAX has majority but no native-flow alignment. Neither meets both conditions. **Predicted: 0 for both maps.**
- Source 2 under additive reading: vertex 1 is the additive generator, not the additive identity. The v1.0 multiplicative-trivialization argument has no clean parallel. **Predicted: 0 for both maps.**
- Source 3: topology-neutral, inherits v1.0 scoring. **Predicted: Map A -1, Map B +1.**
- Source 4: topology-neutral, inherits v1.0 scoring. **Predicted: Map A -1, Map B +1.**

**Predicted aggregate:** Map A = -2, Map B = +2. Cleanness gap = 4.

**Predicted verdict: FAIL** (Map B leads by 4 but fails to clear +3 threshold because Sources 1 and 2 lose discriminating power under additive reading).

**Predicted diagnostic:** Outcome 3 / Reason A from the scope note — Z/10's seam is multiplicatively loaded. Map B retains its lean from the topology-neutral sources; additive-specific sources produce no discriminating signal.

Prediction does not modify thresholds. The rubric scores deterministically.

---

## 12. Approval Status

Frozen per user's Execute direction. Executing immediately.
