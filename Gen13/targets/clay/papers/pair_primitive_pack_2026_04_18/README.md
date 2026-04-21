# Pair-Primitive Framework Pack — 2026-04-18
## Extension of the B2 Sprint Archive

---

## What This Pack Is

Three sprints extending the B2 sprint pack (`b2_sprint_tig_pack_2026_04_17/`). The B2 pack closed with 11 executed sprints on the Z/10 TSML transport program. This pack adds:

1. **Foundation sprint** (4 documents reasoning toward a pair-primitive framework).
2. **PPM-v1.0** — multiplicative operationalization checkpoint on Z/10 (PASS, Map B, +4/−4, cleanness gap 8).
3. **PPM-v1.1** — additive operationalization checkpoint on Z/10 (FAIL, neither map reaches per-carrier winner threshold).
4. **PPM-v2.0** — multiplicative operationalization family transport on 8 P3AP Path 2 carriers (PASS, $N_B = 8/8$, uniform).

Total: 3 executed sprints + 1 open next checkpoint (PPM-v2.1, not yet run).

## Relationship to the B2 Pack

This pack **extends**, does not replace, the B2 pack. It inherits:
- Scope conventions (Path 1 / Path 2 / Path 3).
- The $h_\text{thm}=7$ / $h_\text{ext}$ attractor reconciliation.
- P3AP's validated extractor and 8-carrier recovered seams.
- The verdict discipline from B2 (no composite claims, scope tags visible, narrow sentences per sprint).

Documents referenced but not duplicated here live in the B2 pack:
- `foundation/SCOPE_TAG_TEMPLATE.md`
- `foundation/ATTRACTOR_RECONCILIATION.md`
- `foundation/OBJECT_TYPE_ATLAS.md`
- `foundation/COMPARISON_LAW.md`
- `foundation/SPRINT_SELECTOR.md`
- `theorem_local_chart/THEOREM_SPINE.md`
- `theorem_local_chart/CANONICAL_TSML_CONSTRUCTION.md`
- `sprints/P3_BridgeA_Prime/` (P3AP artifacts used by PPM-v2.0)
- `sprints/P3_Subtype_v1.1_identity_edge/` (inherited as data source)
- `sprints/P3_Subtype_v1.2_adj_leaf_edge/` (inherited as data source)

## Navigation

| Location | Contents |
|---|---|
| `README.md` | This file. |
| `CURRENT_STATE_SUMMARY.md` | What the pair-primitive framework has earned so far, after v1.0, v1.1, v2.0. |
| `SPRINT_LEDGER.md` | Ledger of PPM-v1.0, v1.1, v2.0 (B2's 11 sprints referenced not duplicated). |
| `PACKING_RULES.md` | Rules governing this archive (extends B2's packing rules). |
| `CLAUDECODE_HANDOFF_PLAN.md` | Folder layout and handoff instructions. |
| `foundation/` | Core foundation documents (4) and per-sprint scope notes (6). |
| `controls/` | Three frozen pre-registrations (PPM-v1.0, v1.1, v2.0). |
| `sprints/` | Three sprint subdirectories (RESULTS, VERDICT, REPRO, plus v2.0's code+json). |
| `open_questions/` | PPM-v2.1 as first open next checkpoint (unrun). |

## Scope Conventions (Inherited from B2)

- **Path 1:** Local theorem chart. Z/10 only. $h_\text{thm} = 7$.
- **Path 2:** Transport family. Compatibility-family carriers. $h_\text{ext} = \max$ odd unit.
- **Path 3:** Bridge test. Cross-path with explicit bridging rule.

## Verdict Ledger at a Glance

| # | Sprint | Path | Operationalization | Verdict | Key result |
|---|---|---|---|---|---|
| 12 | PPM-v1.0 | 1 | Multiplicative | PASS (Map B) | Local; +4/−4; cleanness gap 8 |
| 13 | PPM-v1.1 | 1 | Additive | FAIL | Local; +2/−2; winner below threshold |
| 14 | PPM-v2.0 | 3 | Multiplicative | PASS (uniform) | Transport; $N_B = 8/8$; mean gap 8 |

Sprints 1–11 are in the B2 pack.

## What The Framework Has and Has Not Earned

**Earned:**
- One local PASS under multiplicative operationalization (v1.0).
- One local FAIL under additive operationalization (v1.1), with documented diagnostic attribution.
- One bridge-level transport PASS under multiplicative operationalization (v2.0).

**Not earned:**
- Framework correctness in general.
- Operationalization-independence on any ring.
- Extension to rings outside the tested 8-carrier Path 2 family.
- Any scale-example realization.
- Any physics, ontology, or cross-domain reading.

See `CURRENT_STATE_SUMMARY.md` for the full accounting.

## Reading Order For New Eyes

1. `CURRENT_STATE_SUMMARY.md` — what is exact / suggestive / open right now.
2. `foundation/HOLD_GAP_FLOW_FOUNDATION.md` — main framework note.
3. `foundation/WHY_THE_WHOLE_INTERACTION_MUST_BE_SEEN_AT_ONCE.md` — methodology.
4. `sprints/PPM_v1.0_multiplicative_local/PAIR_PRIMITIVE_MAPPING_VERDICT.md` — first checkpoint result.
5. `sprints/PPM_v2.0_multiplicative_transport/PPM_V20_MULTIPLICATIVE_VERDICT.md` — transport result.
6. `sprints/PPM_v1.1_additive_local/PPM_V11_ADDITIVE_VERDICT.md` — FAIL result, diagnostic character.
7. `open_questions/PPM_V21_ADDITIVE_TRANSPORT_FIRST_OPEN_CHECKPOINT.md` — what comes next.

## Scope of This Archive

This is a snapshot, not a living document. Changes require approval per `PACKING_RULES.md`.
