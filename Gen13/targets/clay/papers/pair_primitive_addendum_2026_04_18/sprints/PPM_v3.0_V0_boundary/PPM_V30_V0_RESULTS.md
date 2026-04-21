# PPM-v3.0 V0 Boundary Checkpoint — Results
## Per-Source Rubric Applied to Z/10's V0 Region Under Two Source-3 Branches

---

## Scope Declaration (Reproduced)

**Path:** Path 1 Local Theorem Chart, $h_\text{thm} = 7$.
**Operationalization:** V0-adapted persistent/excluded reading with Source 3 sensitivity branch.
**Data:** Z/10 V0 region (19 cells), from canonical construction Rule (b).
**Inherited clarification:** Verdict applies to this specific operational reading of V0 only; does not refute or confirm the framework in all possible readings. Prohibited substitutions (§8) honored: no third Source 3 reading, no Source 4 demotion mid-run.

---

## V0 Structural Facts (Verified)

From `CANONICAL_TSML_CONSTRUCTION.md` Rule (b) applied to Z/10:

- **Total V0 cells:** 19.
- **V0_Z (zero-output):** 17 cells = 89.5% of V0. All V0 cells EXCEPT $(0,7)$ and $(7,0)$.
- **V0_H (HARMONY-output):** 2 cells = $\{(0,7), (7,0)\}$.
- **Split:** 17/2, with V0_H exactly the 2 cells touching $h = 7$.

All §2 pre-reg assertions verified deterministically in `ppm_v30_score.py`.

---

## Per-Source Scoring

### Fixed Sources (Same Under Both S3 Branches)

#### Source 1 — V0 rule-majority / default-behavior backbone

**Evaluation:**
- V0_Z: majority ✓ (17/19 ≥ 50%); aligns with Rule (b) default (zero-absorption) ✓. Meets both criteria. Backbone.
- V0_H: minority ✗ (2/19); aligns with Rule (b) override, not default ✗. Fails both. Not backbone.

**Scores:**
- Map-V0-I (persistent=V0_Z): persistent IS backbone. **+1**.
- Map-V0-II (persistent=V0_H): persistent is NOT backbone. **−1**.

#### Source 2 — Exception-structure reading

**Evaluation:**
- V0_H: minority ✓, is default-rule override ✓, restricted to cells touching distinguished element $h = 7$ ✓. Meets all three criteria. Localized exception.
- V0_Z: majority ✗, is default not override ✗, spans 9 vertices ✗. Fails all three. Not localized exception.

**Scores:**
- Map-V0-I (excluded=V0_H): excluded IS localized exception. **+1**.
- Map-V0-II (excluded=V0_Z): excluded is NOT localized exception. **−1**.

#### Source 4 — Pair-object symmetry

**Evaluation:**
- V0_H = $\{(0,7), (7,0)\}$: exactly 2 cells, swap-symmetric under $(x,y) \mapsto (y,x)$. Matches pair-object signature.
- V0_Z: 17 cells, not a 2-cell pair. Does not match.

**Scores:**
- Map-V0-I (excluded=V0_H): **+1**.
- Map-V0-II (excluded=V0_Z): **−1**.

### Fixed Subtotal

| | Map-V0-I | Map-V0-II |
|---|---:|---:|
| Source 1 | +1 | −1 |
| Source 2 | +1 | −1 |
| Source 4 | +1 | −1 |
| **Fixed subtotal (S1+S2+S4)** | **+3** | **−3** |

### Source 3 Sensitivity Branch

#### S3a — Attractor privilege → excluded-side (hold at boundary)

Under S3a criterion: V0_H cells manifest $h$'s V0-privilege as surviving distinction at a boundary that otherwise collapses to nothingness → "hold" content → excluded-side.

**Scores:**
- Map-V0-I (excluded=V0_H): attractor privilege at excluded-side = hold at boundary = coheres. **+1**.
- Map-V0-II (persistent=V0_H): attractor privilege at persistent-side contradicts Rule (b)'s override framing. **−1**.

#### S3b — Attractor privilege → persistent-side (gravity well)

Under S3b criterion: $h$ is "where structure gathers"; V0_H cells preserve $h$ at the boundary, carrying the attractor's persistent signature → "persistent at attractor" → persistent-side.

**Scores:**
- Map-V0-I (persistent=V0_Z): persistent-side lacks attractor-privilege content. **−1**.
- Map-V0-II (persistent=V0_H): persistent-side has attractor-privilege content. **+1**.

---

## Per-Branch Aggregates

| | Map-V0-I | Map-V0-II | Gap |
|---|---:|---:|---:|
| Fixed (S1+S2+S4) | +3 | −3 | 6 |
| **Under S3a** | **+4** | **−4** | **8** |
| **Under S3b** | **+2** | **−2** | **4** |

---

## Per-Branch Verdicts (§7.1)

### Under S3a

- Map-V0-I = +4 ≥ +3 ✓
- Map-V0-II = −4 ≤ +1 ✓
- Gap = 8 ≥ 2 ✓

**Branch verdict: PASS-V0-I.**

### Under S3b

- Map-V0-I = +2 < +3 ✗
- Map-V0-II = −2 < +3 ✗

Neither map reaches +3.

**Branch verdict: FAIL.**

---

## Robustness Evaluation (§7.2)

| Check | Value |
|---|---|
| S3a branch verdict | PASS-V0-I |
| S3b branch verdict | FAIL |
| Verdicts agree? | **No** |

The two branches disagree. Per §7.2 robustness rule, the final verdict is **UNCLEAR by Sensitivity**.

---

## Final Verdict

**UNCLEAR by Sensitivity.**

The checkpoint's discriminating content on V0 depends on the Source 3 argument direction. Under S3a (attractor privilege → excluded-side), Map-V0-I wins decisively at aggregate +4/−4, cleanness gap 8. Under S3b (attractor privilege → persistent-side), the Source 3 reversal reduces the aggregate to +2/−2, cleanness gap 4 — the +2 lead is real but falls below the pre-registered per-branch winner threshold of +3.

---

## What the Data Shows

Under the frozen spec of PPM-v3.0 (revised):

1. All four fixed sources (S1, S2, S4) scored unambiguously +1 for Map-V0-I and −1 for Map-V0-II.
2. The Source 3 sensitivity branch produced opposite signs on the two maps as predicted:
   - S3a scored +1/−1 (favoring Map-V0-I).
   - S3b scored −1/+1 (favoring Map-V0-II).
3. Per-branch aggregates: S3a gives +4/−4 (gap 8); S3b gives +2/−2 (gap 4).
4. S3a branch verdict: PASS-V0-I. S3b branch verdict: FAIL.
5. Branches disagree → final verdict: **UNCLEAR by Sensitivity.**

---

## Cross-Check With Pilot Prediction

§11 of the pre-reg predicted:

- Fixed sources: +3/−3 ✓ matched exactly.
- S3a: +4/−4, gap 8 → branch PASS-V0-I ✓ matched.
- S3b: +2/−2, gap 4 → branch FAIL ✓ matched.
- Final: UNCLEAR by Sensitivity ✓ matched.

Every per-source, per-branch, and final-outcome prediction matched the rubric-scored result exactly. The pre-reg's design-level reasoning about Source 3 fragility was operationally verified: under one defensible reading of the attractor-privilege argument, Map-V0-I wins; under the other, no map wins. The revision converted a predicted fragile PASS into a predicted diagnostic UNCLEAR, and the rubric application confirmed the diagnostic outcome.

---

## What UNCLEAR by Sensitivity Means (Not Interpretation Beyond the Frozen Claim)

Per `WHAT_COUNTS_AS_A_ROBUST_V0_RESULT.md`, UNCLEAR by Sensitivity is a specific verdict category — **not a near-pass, not a near-fail**. The sprint earned a diagnostic finding:

> The checkpoint's discriminating content on V0 depends on the Source 3 argument direction. The framework's vocabulary has not settled whether attractor privilege at a boundary region reads as "hold at boundary" (excluded-side) or as "structural gravity well" (persistent-side). Both readings are internally coherent; they produce opposite scores on Source 3.

This is the specific finding v3.0 earned. It is neither weaker nor stronger than that.

Per user's main discipline — "if the result is UNCLEAR by Sensitivity, record that as the earned diagnostic, not as a near-pass or near-fail" — the recorded verdict follows the rubric's frozen categorization. No framing shifts.

---

## What the Data Does NOT Say

- Does NOT refute the pair-primitive framework.
- Does NOT refute Map-V0-I or Map-V0-II. Neither map is refuted; the rubric's verdict is sensitivity-dependent.
- Does NOT establish that V0 is "close to passing" or "close to failing." The aggregate under S3b is +2/−2, sub-threshold by pre-registered rules; framing it as "near-pass" would be exactly the inflation the user discipline prohibits.
- Does NOT upgrade or modify any prior PPM verdict (v1.0, v1.1, v2.0, v2.1).
- Does NOT authorize merging with prior verdicts (Rule 19).
- Does NOT extend to other rings, other checkpoints, or any transport test.
- Does NOT validate or refute SAH. SAH stays at foundation register.
- Does NOT authorize scale examples, physics, ontology, or cross-domain reading.
- Does NOT authorize a re-run with adjusted rubric (§10). Successor would require v3.0.1+.

---

## Earned, Not Assumed

Per user discipline: the UNCLEAR by Sensitivity result is earned by:

1. Deterministic scoring of all 16 source-map-branch combinations in `ppm_v30_score.py`.
2. Each per-source rationale traceable to the frozen §5 criteria.
3. Prohibited substitutions honored: no third S3 reading introduced; Source 4 remained scored throughout.
4. Pilot prediction cross-check recorded transparently; every per-source and per-branch prediction matched exactly.
5. The sensitivity revealed (S3a favors Map-V0-I, S3b favors Map-V0-II) is specifically what the pre-reg revision was designed to surface.
6. Recording the verdict as UNCLEAR by Sensitivity rather than "near-pass" or "near-fail" honors the scope discipline.

The result is not documentation reasoning; it is rubric application producing 16 specific scores, aggregating them per frozen §7 rules, and returning the category the pre-reg specified for this outcome pattern.

Verdict follows in `PPM_V30_V0_VERDICT.md`.
