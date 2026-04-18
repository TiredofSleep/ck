# Pair-Primitive Mapping — Reproducibility
## PPM-v1.0 How to Rerun

---

## Scope Reference

**Path:** Path 1 (Local Theorem Chart).
**Convention:** $h_\text{thm} = 7$.
**Claim class:** structural-fit claim under one specific operationalization.
**Spec:** `PAIR_PRIMITIVE_MAPPING_PREREG.md` (frozen as PPM-v1.0).

**Frozen clarification:** This sprint evaluates the pair-primitive framework under a multiplicative operationalization only; failure would refute this operationalization, not the pair-primitive framework in all possible readings.

---

## Execution Character

This sprint differs from the B2 pack's prior sprints in that its evaluation is not numerical null-comparison. It is a **deterministic application of a frozen rubric to frozen data** under a frozen operational interpretation. There is no RNG, no sampling, no noise.

The reproducibility standard is correspondingly different: any scorer applying the §5 rubric to the §4 data under the §3 interpretation should return identical scores. The rubric is designed to be unambiguous enough that this holds.

---

## Input Data (Static)

The four data sources are fixed in PPM-v1.0 §4. They come from:

1. **Source 1 (seam-graph structural split):** directly from Z/10's published TSML 3-layer tower theorem. The 8 seam cells split into:
   - MAX cells: $\{(2,4), (4,2), (2,9), (9,2), (4,8), (8,4)\}$ = 3 unordered edges on $\{2, 4, 8, 9\}$.
   - ADD cells: $\{(1,2), (2,1)\}$ = 1 unordered edge on $\{1, 2\}$.

2. **Source 2 (v1.1 identity-edge finding):** from `b2_sprint_tig_pack_2026_04_17/sprints/P3_Subtype_v1.1_identity_edge/PATH3_SUBTYPE_V11_VERDICT.md`. ADD attaches multiplicative identity at $+6.06\sigma$. On Z/10, ADD edge is $(1, 2)$.

3. **Source 3 (v1.2-adj leaf-edge finding):** from `b2_sprint_tig_pack_2026_04_17/sprints/P3_Subtype_v1.2_adj_leaf_edge/PATH3_SUBTYPE_ADJACENCY_V12_VERDICT.md`. ADD is a leaf edge at $+3.73\sigma$. On Z/10, vertex 1 has degree 1.

4. **Source 4 (P3AP topology-family finding):** from `b2_sprint_tig_pack_2026_04_17/sprints/P3_BridgeA_Prime/P3AP_VERDICT.md`. Topology features transport at $+12.56\sigma$ on mean component count. On Z/10, seam graph is 4 edges on 5 vertices with max degree 3.

None of these inputs changes on rerun. All are static records.

---

## Rubric (Frozen in §5)

Each source has a pre-specified binary rubric returning a value in $\{-1, 0, +1\}$. The rubric criteria are:

- **Source 1:** persistent-side subtype = structural backbone (majority of edges AND multiplicative-flow elements).
- **Source 2:** map's reading of "ADD at identity" coheres with §3's multiplicative operationalization.
- **Source 3:** excluded-side subtype sits at the graph boundary (leaf position).
- **Source 4:** persistent-side subtype carries majority of topology features.

---

## Expected Reproduction Results

Applying the rubric deterministically:

| Source | Map A | Map B | Basis for score |
|---|:---:|:---:|---|
| 1. Seam-graph structural split | −1 | +1 | MAX forms 3 of 4 unordered edges + contains doubling chain + contains attractor-involution; ADD forms 1 edge at identity position |
| 2. v1.1 identity-edge | −1 | +1 | Identity is multiplicative-absence point (1·x = x trivial); subtype there is excluded content surfacing at the trivialization |
| 3. v1.2-adj leaf-edge | −1 | +1 | Vertex 1 has degree 1 in seam graph; ADD edge (1,2) is at the leaf; rubric expects excluded-side at boundary |
| 4. P3AP topology-family | −1 | +1 | MAX forms forest spine on {2,4,8,9}; low max degree in MAX-only subgraph; ADD contributes single-component via one edge |
| **Aggregate** | **−4** | **+4** | — |

**Cleanness gap:** $|(-4) - (+4)| = 8$.

All three PASS conditions (winner $\geq +3$, loser $\leq +1$, gap $\geq 2$) met. **Verdict: PASS (Map B).**

---

## Verification Hooks

Any reproducing scorer should check:

- [ ] MAX unordered edge count = 3.
- [ ] ADD unordered edge count = 1.
- [ ] MAX contains doubling-chain segment $2 \to 4 \to 8$.
- [ ] MAX contains attractor-involution edge $2\text{–}9$.
- [ ] ADD edges incident to vertex 1 only through the identity-edge rule.
- [ ] Vertex 1 has degree 1 in full seam graph.
- [ ] Vertex 2 has degree 3 in full seam graph (incident to (1,2), (2,4), (2,9)).
- [ ] MAX-only subgraph is a tree on $\{2, 4, 8, 9\}$.
- [ ] Without ADD, vertex 1 is isolated.
- [ ] Source 2's §5.2 key criterion applied: identity = multiplicative-absence point under §3.
- [ ] Source 3 score based on excluded-side's leaf-presence, not on whether all leaves are excluded-side.
- [ ] Source 4 majority attribution: 3 of 4 topology features primarily MAX-driven; 1 feature (connectivity) needs both.

If all checks return the expected values, the aggregate scores and verdict follow deterministically.

---

## Sources of Potential Reproduction Divergence

The sprint is deterministic in principle, but a scorer could in principle diverge at three points:

### Divergence point 1 — Interpretation of §3

The operational interpretation in §3 fixed "persistent = multiplicative backbone, excluded = localized non-multiplicative departure." A scorer applying a different operational interpretation (e.g., reading the seam under additive operation structure, or under dual-operation reading) would produce different scores.

**Anti-divergence rule:** the pre-reg froze the multiplicative operationalization; rerunning under PPM-v1.0 means using §3's interpretation. Alternative operationalizations belong to separate sprint versions (PPM-v1.1+).

### Divergence point 2 — Source 2 key criterion reading

§5.2 states: "Identity is trivial under multiplication (1·x = x). The identity position is a point where multiplicative structure is absent... A subtype surfacing at the identity is surfacing at a multiplicative-absence, which is the excluded-side reading."

A scorer might argue that identity is persistent under multiplication (because $1 \cdot x = x$ preserves $x$) rather than absent. Both readings describe the same algebraic fact with different structural interpretations.

**Anti-divergence rule:** §5.2 explicitly picks the "multiplicative-absence" reading. The pre-reg committed to this reading before scoring. A scorer adopting the alternative reading would need to run a different sprint version (PPM-v1.1 or later) with the alternative pre-registered.

### Divergence point 3 — Source 4 majority attribution

§5.4 attributes 3 of 4 topology features (forest spine, low max degree, low-degree-vertex dominance) primarily to MAX, and 1 feature (single-component connectivity) to ADD-required. A scorer might argue all features require both subtypes since the graph is defined as the union.

**Anti-divergence rule:** §5.4 explicitly discusses the attribution logic and picks "3 of 4 unordered edges are MAX + forest spine is MAX-dominated + low max degree is MAX-driven" as the majority argument. The discussion is in the pre-reg; a scorer disputing it is disputing the pre-reg, which requires a new sprint version.

---

## Scorer Invariance Check

If two independent scorers apply PPM-v1.0 §5 to the PPM-v1.0 §4 data under the PPM-v1.0 §3 interpretation, they should return the same per-source scores and therefore the same verdict. If they diverge:

1. Identify which source diverged.
2. Identify whether the divergence is at one of the three divergence points above.
3. If yes: one scorer has deviated from the frozen pre-reg. The frozen pre-reg's reading wins.
4. If no: the rubric has ambiguity not caught at pre-reg time. A clarification amendment (not a scoring change) would be required.

This sprint's scorer found no ambiguity requiring post-hoc clarification.

---

## Rerun Instructions

To reproduce:

1. Open the frozen pre-reg `PAIR_PRIMITIVE_MAPPING_PREREG.md`.
2. Load the four data sources from the locations cited in "Input Data (Static)" above.
3. For each of the four data sources, apply the §5 rubric under the §3 operational interpretation.
4. Record binary score for each (map, source) pair.
5. Compute aggregate scores and cleanness gap.
6. Apply §7 pass/fail/unclear criteria.
7. Compare to the Expected Reproduction Results table above.

Expected output: **PASS, Map B winner, aggregate $+4$/$-4$, cleanness gap $8$.**

No programming required. No RNG. The rerun is a structured re-application of a logical rubric.

---

## Integrity

- No external inputs beyond the frozen pre-reg and the cited data sources.
- No hidden state; the rubric is fully documented in the pre-reg and applied transparently in the results document.
- All four per-source score justifications are reproduced in the results document with explicit citation to the rubric clauses.
- The matching between pilot prediction (§12) and rubric-scored result is a cross-check, not a tuning loop: the rubric was frozen before any scoring; the pilot predictions were public in the pre-reg before freeze.

---

## Cross-Sprint Position

| Spec | Path | Verdict | Key result |
|---|---|---|---|
| S28-v1.0 | 2 | FAIL | Basin smoothness |
| S29-v1.0 | 2 | FAIL | Anchored curve |
| S30-v1.0 | 2 | PASS (vacuous) | Empty seams |
| S30b-v1.0 | 2 | FAIL | No seam under uniform noise |
| S31p-v1.0 | cross (undeclared) | FAIL | Convention mismatch |
| S31p-v2.0 | 1 | effective PASS | Ceiling recovery |
| P3-BridgeA-v1.0 | 3 | FAIL | Object-type mismatch |
| P3-BridgeA-Prime-v1.0 | 3 | PASS | Topology-family (+12.56σ) |
| P3-Subtype-v1.0 | 3 | UNCLEAR | ADD role at +3.80σ |
| P3-Subtype-v1.1 | 3 | PASS | Identity-edge (+6.06σ) |
| P3-Subtype-v1.2-adj | 3 | PASS | Leaf-edge (+3.73σ) |
| **PPM-v1.0** | **1** | **PASS (Map B)** | **Pair-primitive framework checkpoint; agg +4/-4; cleanness gap 8** |

Twelve sprints under discipline. Four substantive PASSes plus PPM-v1.0's framework checkpoint PASS. One UNCLEAR. One vacuous PASS. Five FAILs with attributed causes.

The pair-primitive framework now has one confirmed point of contact with the program's rigorous register. Framework correctness remains unestablished; what is established is that the framework's first structural prediction, under the multiplicative operationalization, cashes out on the actual data.

---

## If Rerun Gives a Different Verdict

All inputs are static documents. The rubric is specified in frozen prose. Divergence must come from:

1. Modified input documents (check version hashes).
2. Alternative operational interpretation adopted (this is a separate sprint, not a reproduction).
3. Different reading of §5.2's key criterion (this is disputing the pre-reg, which requires a new sprint version).
4. Different attribution of Source 4 topology features (this is disputing the pre-reg, which requires a new sprint version).

The PASS with Map B winning at $+4/-4$ / cleanness gap $8$ is the deterministic output of this frozen spec. Any correct reimplementation of the frozen rubric on the frozen data under the frozen operationalization reproduces this result.
