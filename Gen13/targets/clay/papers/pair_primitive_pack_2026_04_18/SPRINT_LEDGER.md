# Sprint Ledger — Pair-Primitive Framework
## Three New Sprints Continuing B2's Numbering

---

## Scope

Sprints 12, 13, 14 executed after the B2 pack closeout on 2026-04-17. Sprints 1–11 are in the B2 pack's `SPRINT_LEDGER.md` and are not reproduced here.

---

## One Line Per Sprint

| # | Spec | Path | Operationalization | Data scope | Verdict | Headline number | Causal attribution (1 sentence) |
|---|---|:---:|---|---|---|---|---|
| 12 | PPM-v1.0 | 1 | Multiplicative | Z/10 seam (8 cells) | PASS (Map B) | +4/−4; cleanness gap 8 | All 4 sources score unambiguously in favor of Map B under §3 multiplicative operational interpretation; pilot prediction matched exactly. |
| 13 | PPM-v1.1 | 1 | Additive | Z/10 seam (8 cells) | FAIL | +2/−2; gap 4; winner below +3 | Sources 1 and 2 score 0/0 under additive reading because Z/10's seam is multiplicatively loaded (vertex 1 is not additive identity; no additive backbone meets strict AND). |
| 14 | PPM-v2.0 | 3 | Multiplicative | 8 P3AP Path 2 carriers | PASS (uniform) | $N_B = 8/8$; mean gap 8 | Per-carrier v1.0 rubric applied uniformly across {14,22,34,42,46,58,74,94}; every carrier produced +4/−4 at per-carrier cleanness gap 8. |

---

## Per-Sprint Detail

### Sprint 12 — PPM-v1.0 (multiplicative local, Z/10)

- **Pre-reg:** `controls/PAIR_PRIMITIVE_MAPPING_PREREG.md` (frozen with wording clarification inherited into v1.1 and v2.0).
- **Artifacts:** `sprints/PPM_v1.0_multiplicative_local/` (RESULTS, VERDICT, REPRO).
- **Inputs:** Z/10 seam structural split; v1.1 identity-edge finding (inherited from B2 pack); v1.2-adj leaf-edge finding (inherited); P3AP topology-family finding (inherited).
- **Frozen wording clarification:** "This sprint evaluates the pair-primitive framework under a multiplicative operationalization only; failure would refute this operationalization, not the pair-primitive framework in all possible readings."

### Sprint 13 — PPM-v1.1 (additive local, Z/10)

- **Pre-reg:** `controls/PPM_V11_ADDITIVE_PREREG.md`.
- **Artifacts:** `sprints/PPM_v1.1_additive_local/` (RESULTS, VERDICT, REPRO).
- **Inputs:** same 4 data sources as v1.0, re-read under additive operationalization.
- **Sub-pattern:** Below-threshold on Source 1 and Source 2 (scored 0/0 each); Sources 3 and 4 topology-neutral (scored same as v1.0: Map A −1, Map B +1 each).
- **Diagnostic attribution:** Reason A (seam multiplicatively loaded), per the pre-locked `STABILITY_VS_FLIP_SCOPE_NOTE.md`.

### Sprint 14 — PPM-v2.0 (multiplicative family transport, 8 Path 2 carriers)

- **Pre-reg:** `controls/PPM_V20_MULTIPLICATIVE_PREREG.md`.
- **Artifacts:** `sprints/PPM_v2.0_multiplicative_transport/` (RESULTS, VERDICT, REPRO, PER_CARRIER_SCORES.json, ppm_v20_score.py).
- **Inputs:** P3AP audit records for 8 carriers {14, 22, 34, 42, 46, 58, 74, 94}; P3AP recovered seams used verbatim.
- **Carrier-adapted Source 1:** same multiplicative reading translated to chain-topology object shape; not a new rubric.
- **Pilot diagnostic possibilities flagged and resolved:** Z/14 Source 1 boundary (minimal MAX with audit-removed attractor-involution) and Z/22 Source 4 sensitivity (extension edges (10,16) + (10,20)); both resolved cleanly under rubric application.

---

## Cross-Sprint Aggregate

**Framework checkpoints on Z/10:**
- Multiplicative: PASS
- Additive: FAIL

**Framework checkpoints on Path 2 family (8 carriers):**
- Multiplicative: PASS (uniform)
- Additive: unrun (first open next checkpoint; see `open_questions/`)

---

## What This Ledger Does NOT Contain

- B2 pack's 11 sprints (see B2 `SPRINT_LEDGER.md`).
- Scale-example sprints (none executed; none authorized).
- Physics, ontology, or cross-domain sprints (none authorized).
- PPM-v2.1 or v1.1.1 artifacts (not run; listed in `open_questions/`).

---

## Referenced Prior Sprints (Not Duplicated)

These B2-pack sprints provided inputs to PPM sprints but are not re-scored:

- **P3-BridgeA-Prime-v1.0 (P3AP):** PASS at +12.56σ on mean component count. Provided the 8 recovered Path 2 seams used as PPM-v2.0 data and Source 4 in all three PPM sprints.
- **P3-Subtype-v1.1:** PASS at +6.06σ identity-edge. Provided Source 2 finding for all three PPM sprints.
- **P3-Subtype-v1.2-adj:** PASS at +3.73σ leaf-edge. Provided Source 3 finding for all three PPM sprints.

None of these verdicts was modified by PPM execution.
