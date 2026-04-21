# PPM-v1.1 Additive Operationalization — Reproducibility
## How to Rerun

---

## Scope Reference

**Path:** Path 1 (Local Theorem Chart), $h_\text{thm} = 7$.
**Operationalization:** Additive.
**Spec:** `PPM_V11_ADDITIVE_PREREG.md`.
**Verdict:** FAIL.

---

## Execution Character

Identical to PPM-v1.0: deterministic application of a frozen rubric to frozen data under a frozen operational interpretation. No RNG, no sampling, no noise. The rubric is specified in prose; any scorer applying it correctly should return identical scores.

---

## Input Data (Static)

Identical to PPM-v1.0 inputs:

1. Z/10 seam structural split from the published 3-layer tower theorem.
2. v1.1 identity-edge finding from `b2_sprint_tig_pack_2026_04_17/sprints/P3_Subtype_v1.1_identity_edge/`.
3. v1.2-adj leaf-edge finding from `b2_sprint_tig_pack_2026_04_17/sprints/P3_Subtype_v1.2_adj_leaf_edge/`.
4. P3AP topology-family finding from `b2_sprint_tig_pack_2026_04_17/sprints/P3_BridgeA_Prime/`.

None changes on rerun.

---

## Rubric (Frozen in PPM-v1.1 §5)

Four sources, binary scoring in $\{-1, 0, +1\}$. Criteria:

- **Source 1:** additive backbone requires majority edges AND native-additive-flow alignment (strict AND).
- **Source 2:** requires coherent additive-structural reading of "ADD at vertex 1" with v1.0's key argument as the template.
- **Source 3:** topology-neutral, inherits v1.0 §5.3.
- **Source 4:** topology-neutral, inherits v1.0 §5.4.

---

## Expected Reproduction Results

| Source | Map A | Map B | Basis |
|---|:---:|:---:|---|
| 1. Additive backbone | 0 | 0 | ADD is native but minority; MAX is majority but non-additive; neither meets strict AND |
| 2. Identity-edge (additive) | 0 | 0 | Vertex 1 is additive generator, not additive identity; v1.0's multiplicative-trivialization argument has no structural parallel |
| 3. Leaf-edge | −1 | +1 | Topology-neutral, same as v1.0: ADD at leaf; Map A persistent-at-leaf triggers −1; Map B excluded-at-leaf triggers +1 |
| 4. Topology-family | −1 | +1 | Topology-neutral, same as v1.0: MAX carries 3 of 4 unordered edges; persistent-is-MAX matches majority (Map B +1); persistent-is-ADD does not (Map A −1) |
| **Aggregate** | **−2** | **+2** | |
| **Cleanness gap** | | **4** | |
| **Verdict** | | **FAIL** | Neither reaches +3 |

---

## Verification Hooks

Any reproducing scorer should verify:

- [ ] ADD unordered edge count = 1 (minority).
- [ ] MAX unordered edge count = 3 (majority).
- [ ] ADD rule (x+y) mod 10 is Z/10's native additive operation.
- [ ] MAX rule max(x,y) is order-based, not aligned with additive flow.
- [ ] Additive identity on Z/10 is 0, not 1.
- [ ] Vertex 0 is in V0 boundary, not in seam graph.
- [ ] Vertex 1 is the additive generator of Z/10 (generates cyclic group under addition).
- [ ] Source 1's strict AND criterion: both majority AND native-flow conditions required.
- [ ] Source 2's key criterion: vertex 1 is not the additive identity; v1.0's multiplicative argument has no parallel.
- [ ] Sources 3 and 4 are topology-neutral and score identically to v1.0.

If all checks pass, aggregate scores and verdict follow deterministically.

---

## Source of Rubric Decisions

The v1.1 pre-reg made two specific rubric choices under additive reading:

### Decision 1: Strict AND criterion in Source 1

The v1.0 §5.1 rubric required majority edges AND containment of multiplicative-flow elements. For symmetry and to preserve structural parity with v1.0, the v1.1 rubric required majority edges AND containment of additive-flow elements.

Under this strict criterion, no subtype meets both conditions on Z/10's seam under additive reading.

**Alternative considered:** relaxing to "majority OR native-flow alignment" would have given ADD as backbone (native-additive ✓). This alternative was rejected to preserve structural symmetry with v1.0 and to avoid back-door tuning.

**Consequence:** Source 1 scores 0/0 under additive reading. A future v1.1.1 could explicitly test the relaxed criterion.

### Decision 2: No substitution of v1.0's key criterion in Source 2

The v1.0 §5.2 rubric hinged on "identity is a multiplicative-trivialization point." Vertex 1 is not the additive identity, so this argument does not translate.

The v1.1 rubric could have substituted alternative structural arguments (e.g., "vertex 1 is the additive generator, so persistent anchored at the flow origin" or "vertex 1 generates the cycle, so excluded surfaces at flow-origin as a departure from multiplicative idleness").

Neither substitute was adopted because introducing a new structural argument is not a rubric translation — it is a different rubric requiring its own pre-registration.

**Consequence:** Source 2 scores 0/0 under additive reading. The identity-edge finding becomes non-diagnostic under this operationalization, consistent with the fact that the finding's original structural significance was multiplicative.

---

## Rerun Instructions

1. Load the frozen PPM-v1.1 pre-reg.
2. Confirm access to the four data sources (inputs unchanged from v1.0).
3. For each source, apply the v1.1 §5 rubric under the v1.1 §3 additive interpretation.
4. Record binary score per (map, source).
5. Aggregate and compute cleanness gap.
6. Apply v1.1 §7 pass/fail/unclear criteria.
7. Compare to Expected Reproduction Results above.

Expected output: **FAIL, aggregate Map A = −2 / Map B = +2, cleanness gap = 4.**

---

## Comparison With v1.0

| Aspect | v1.0 (multiplicative) | v1.1 (additive) |
|---|---|---|
| Source 1 | Map A −1, Map B +1 | Map A 0, Map B 0 |
| Source 2 | Map A −1, Map B +1 | Map A 0, Map B 0 |
| Source 3 | Map A −1, Map B +1 | Map A −1, Map B +1 |
| Source 4 | Map A −1, Map B +1 | Map A −1, Map B +1 |
| Aggregate | −4 / +4 | −2 / +2 |
| Cleanness gap | 8 | 4 |
| Verdict | PASS (Map B) | FAIL |

The difference is entirely in Sources 1 and 2, which lose discriminating power under additive reading. Sources 3 and 4 (topology-neutral) score identically.

---

## Cross-Sprint Position

| # | Spec | Path | Verdict | Key result |
|---|---|---|---|---|
| 1–11 | (B2 pack) | 1,2,3 | Mixed | See B2 `SPRINT_LEDGER.md` |
| 12 | PPM-v1.0 | 1 | PASS (Map B) | Multiplicative operationalization, +4/−4, gap 8 |
| 13 | **PPM-v1.1** | **1** | **FAIL** | **Additive operationalization, +2/−2, gap 4, winner below +3** |

Thirteen sprints under discipline. Four substantive PASSes (P3AP, v1.1 identity-edge, v1.2-adj leaf-edge, PPM-v1.0 Map B). One effective PASS (S31-pilot-v2.0). One UNCLEAR (P3-Subtype-v1.0). One vacuous PASS (S30). Six FAILs with attributed causes.

The pair-primitive framework now has one confirmed checkpoint (multiplicative operationalization) and one FAILed checkpoint (additive operationalization), with the FAIL diagnostically attributed to the seam's multiplicative loading of Sources 1 and 2.

---

## If Rerun Gives a Different Verdict

All inputs static. The rubric is prose-specified. Divergence must come from:

1. Adopting a relaxed Source 1 criterion (pseudo-PASS by rubric change — not a reproduction).
2. Substituting a new Source 2 key criterion (pseudo-PASS by rubric change — not a reproduction).
3. Modifying inputs (check version hashes of the B2 pack documents).

The FAIL with aggregate +2/−2 and cleanness gap 4 is the deterministic output of the frozen spec. Any correct reimplementation reproduces this result.

---

## Integrity

- No external inputs beyond the frozen pre-reg and cited data sources.
- No hidden state; rubric is fully documented.
- Per-source score justifications are reproduced in the results document with explicit rubric-clause citations.
- Pilot prediction matched rubric-scored result exactly, which is a cross-check on rubric unambiguity.
- No post-hoc rubric adjustment.
- v1.0 verdict unaffected.
