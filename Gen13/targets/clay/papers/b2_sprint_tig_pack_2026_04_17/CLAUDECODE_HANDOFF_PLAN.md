# ClaudeCode Handoff Plan
## Packaging Layout for GitHub Commit

---

## Context for ClaudeCode

**The B1 sprint zip was the last handoff to ClaudeCode.** This pack is the continuation from that point — everything produced *after* B1 that belongs in the GitHub archive.

This pack therefore does NOT re-package B1. B1's pre-reg, results, and verdict are already in ClaudeCode's hands from the previous handoff. References to B1 in this pack's documents (e.g., `theorem_local_chart/` material citing B1's ground-truth verification) are *references* to already-held artifacts, not copies.

ClaudeCode should integrate this pack into whatever repository structure already contains B1. Suggested approach: place this pack's contents alongside the existing B1 material under a shared top-level layout (e.g., the foundation/, theorem_local_chart/, controls/, sprints/ structure proposed below), with B1's existing files slotted into the appropriate subdirectories (B1 pre-reg into `controls/`, B1 results into `sprints/B1_NSCG/`, etc.) without modification.

The continuation work covers sprints S28 onward plus the foundation documents produced in response to sprint findings. Specifically:

- Foundation documents produced after B1 (attractor reconciliation, scope-tag template, object-type atlas, comparison law, sprint selector).
- Sprints 28 through P3-Subtype-v1.2-adj (11 sprints).
- Theorem local-chart summary documents (small set — most of this material predates B1 but is included here for local-reference completeness of this pack if B1's delivery did not include it).

---

## Purpose

This document specifies the folder/file layout, inclusion list, omission list, and cleanup operations required to transform the current on-disk materials into a tight, disciplined sprint archive ready for ClaudeCode to commit to GitHub alongside the existing B1 material.

This is a packaging plan, not a research plan. No new claims, no synthesis, no narrative smoothing.

---

## Proposed Folder Layout

```
tig_pack/
├── README.md
├── CURRENT_STATE_SUMMARY.md
├── PACKING_RULES.md
├── CLAUDECODE_HANDOFF_PLAN.md   (this document)
│
├── foundation/
│   ├── SCOPE_TAG_TEMPLATE.md
│   ├── ATTRACTOR_RECONCILIATION.md
│   ├── PATH_C_RECOMMENDATION.md
│   ├── PRIOR_SPRINT_H_DEPENDENCIES.md
│   ├── OBJECT_TYPE_ATLAS.md
│   ├── COMPARISON_LAW.md
│   ├── SPRINT_SELECTOR.md
│   └── BRIDGE_LANGUAGE_RESET.md
│
├── theorem_local_chart/
│   ├── THEOREM_SPINE.md
│   ├── CANONICAL_TSML_CONSTRUCTION.md
│   ├── LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md
│   └── TSML_IS_NOT_PHYSICS.md
│
├── controls/
│   ├── S28_PREREG_v1.0.md
│   ├── S29_PREREG_ANCHORED_CURVE.md
│   ├── S30_PREREG_v1.0_FROZEN.md
│   ├── S30B_PREREG_SEAM_DETECTABILITY.md
│   ├── S31_Z10_PILOT_v1.0.md
│   ├── S31_PILOT_V2_LOCAL_THEOREM.md
│   ├── PATH3_BRIDGEA_PREREG.md
│   ├── PATH3_BRIDGE_A_PRIME_PREREG.md
│   ├── PATH3_SUBTYPE_BRIDGE_PREREG.md
│   ├── PATH3_SUBTYPE_V11_PREREG.md
│   └── PATH3_SUBTYPE_ADJACENCY_V12_PREREG.md
│
├── sprints/
│   ├── SPRINT_LEDGER.md
│   │
│   ├── S28_basin_smoothness/
│   │   ├── S28_RESULTS.md
│   │   ├── S28_VERDICT.md
│   │   └── S28_REPRO.md
│   │
│   ├── S29_anchored_curve/
│   │   ├── S29_RESULTS.md
│   │   ├── S29_VERDICT.md
│   │   └── S29_REPRO.md
│   │
│   ├── S30_seam_topology_vacuous/
│   │   ├── S30_RESULTS.md
│   │   └── S30_DEGENERATE_PASS_NOTE.md
│   │
│   ├── S30b_seam_detectability/
│   │   ├── S30B_RESULTS.md
│   │   ├── S30B_VERDICT.md
│   │   └── S30B_REPRO.md
│   │
│   ├── S31_pilot_v1.0_convention_mismatch/
│   │   ├── S31_PILOT_RESULTS.md
│   │   ├── S31_PILOT_VERDICT.md
│   │   └── S31_PILOT_REPRO.md
│   │
│   ├── S31_pilot_v2.0_local_theorem/
│   │   ├── S31_V2_RESULTS.md
│   │   ├── S31_V2_VERDICT.md
│   │   └── S31_V2_REPRO.md
│   │
│   ├── P3_BridgeA/
│   │   ├── P3A_RESULTS.md
│   │   ├── P3A_VERDICT.md
│   │   └── P3A_REPRO.md
│   │
│   ├── P3_BridgeA_Prime/
│   │   ├── P3AP_RESULTS.md
│   │   ├── P3AP_VERDICT.md
│   │   ├── P3AP_REPRO.md
│   │   ├── WHY_BRIDGE_A_FIRST.md
│   │   ├── WHY_A_PRIME_IS_NOW_VALID.md
│   │   ├── BRIDGE_A_SCOPE_LIMITS.md
│   │   └── A_PRIME_METRIC_SET.md
│   │
│   ├── P3_Subtype_v1.0/
│   │   ├── PATH3_SUBTYPE_BRIDGE_RESULTS.md
│   │   ├── PATH3_SUBTYPE_BRIDGE_VERDICT.md
│   │   ├── PATH3_SUBTYPE_BRIDGE_REPRO.md
│   │   ├── WHY_SUBTYPE_COMES_BEFORE_HUB_EXTENSION.md
│   │   └── SUBTYPE_BRIDGE_SCOPE_LIMITS.md
│   │
│   ├── P3_Subtype_v1.1_identity_edge/
│   │   ├── PATH3_SUBTYPE_V11_RESULTS.md
│   │   ├── PATH3_SUBTYPE_V11_VERDICT.md
│   │   ├── PATH3_SUBTYPE_V11_REPRO.md
│   │   ├── WHY_IDENTITY_EDGE_COMES_NEXT.md
│   │   └── SUBTYPE_V10_VS_V11_SCOPE.md
│   │
│   └── P3_Subtype_v1.2_adj_leaf_edge/
│       ├── PATH3_SUBTYPE_ADJACENCY_V12_RESULTS.md
│       ├── PATH3_SUBTYPE_ADJACENCY_V12_VERDICT.md
│       ├── PATH3_SUBTYPE_ADJACENCY_V12_REPRO.md
│       ├── WHY_L_ONLY_IS_THE_RIGHT_METRIC.md
│       ├── V11_INHERITED_VS_V12_NEW.md
│       └── CHAIN_AWARE_ADJACENCY_PRINCIPLES.md
│
└── open_questions/
    ├── COUNT_TRANSPORT_CLOSED_UNDER_P3AP.md   (= WHY_COUNT_IS_NOT_LIVE_UNDER_P3AP.md)
    ├── HUB_EXTENSION_DEFERRED.md              (short summary)
    ├── V11_VS_COUNT_SCOPE.md                  (scope distinction note)
    └── GEOMETRY_AS_OBJECT_TYPE_SEPARATION.md  (closing reflection — optional)
```

---

## Inclusion Decisions

### Foundation (8 documents)

Required documents explicitly named by user plus three supporting documents that directly condition the foundation:

- **SCOPE_TAG_TEMPLATE.md** — mandatory scope declaration format.
- **ATTRACTOR_RECONCILIATION.md** — core foundation doc resolving h_thm vs h_ext.
- **PATH_C_RECOMMENDATION.md** — adoption of bifurcated paths.
- **PRIOR_SPRINT_H_DEPENDENCIES.md** — per-sprint audit showing which convention each prior sprint used.
- **OBJECT_TYPE_ATLAS.md** — 15 object types classification.
- **COMPARISON_LAW.md** — three tests before freezing any comparison spec.
- **SPRINT_SELECTOR.md** — metric-object compatibility matrix.
- **BRIDGE_LANGUAGE_RESET.md** — language discipline after STD bridge retractions.

### Theorem Local Chart (4 documents)

Smallest sufficient set to understand the Path 1 object:

- **THEOREM_SPINE.md** — the theorem statement itself (h=7, seam structure, 3-layer tower).
- **CANONICAL_TSML_CONSTRUCTION.md** — the 92/100 canonical construction and its seam residue.
- **LOCAL_CHART_VS_TRANSFERRED_GRAMMAR.md** — two-column scope split.
- **TSML_IS_NOT_PHYSICS.md** — scope discipline note.

Not included: every derivation document, INVARIANTS_BEYOND_TSML.md, CANONICAL_XI_DERIVATION_AUDIT.md, TSML_DERIVATION_TEST.md, TSML_BHML_PAIR_AUDIT.md, etc. (These contain derivation details not required for the pack's purpose.)

### Controls (11 documents — all pre-regs for executed sprints)

One pre-reg per executed sprint. Both S31-pilot versions included because both produced verdicts on record.

### Sprints (11 sprint directories)

Each sprint gets its own directory containing RESULTS, VERDICT, REPRO plus any WHY_ / SCOPE_LIMITS / METRIC_SET documents that directly attribute that sprint's verdict.

Attribution documents co-locate with their sprint so the connection is immediate. They are **not** stored in a separate attribution folder.

S30 has only RESULTS + DEGENERATE_PASS_NOTE (no separate VERDICT/REPRO files exist on disk for S30; this reflects the actual materials).

### Open Questions (3–4 documents)

- **COUNT_TRANSPORT_CLOSED_UNDER_P3AP.md** — closure document explaining why count is not live under current generator.
- **HUB_EXTENSION_DEFERRED.md** — short new note summarizing why hub-extension remains deferred.
- **V11_VS_COUNT_SCOPE.md** — scope distinction documentation.
- **GEOMETRY_AS_OBJECT_TYPE_SEPARATION.md** — closing reflection on program structure. Optional — include only if user explicitly wants it.

---

## Omission List

These documents exist on disk but are **excluded from the pack** per user direction ("no STD bridge language, no spectral 3/4, no physics/ontology, no broad philosophical notes, no abandoned speculative bridge drafts"):

### STD bridge / spectral retractions (all omitted)
- STD_BRIDGE_STATUS.md
- STD_STRUCTURAL_SURVIVORS_NOTE.md
- TSML_SPECTRAL_AUDIT.md

### Abandoned synthesis drafts (all omitted)
- FULL_SYNTHESIS_V2.md through FULL_SYNTHESIS_V5.md
- THREE_THREAD_SYNTHESIS.md, THREE_THREAD_V2.md, THREE_THREAD_V3.md
- BASIN_FIRST_SYNTHESIS.md
- PRIME_COLLATZ_FULL_SYNTHESIS.md
- FIELD_OBSERVER_SYNTHESIS.md

### Physics / ontology content (all omitted)
- PHYSICAL_TESTING_PROGRAM.md
- STATIC_DYNAMIC_DUALITY.md, STATIC_DYNAMIC_DUALITY_V2.md
- BHML_STATUS_NOTE.md
- XI_CORE_INTERPRETATION_MOD5_TRIAGE.md
- LOG_QUINTESSENCE_NOVELTY_AUDIT.md

### Speculative / exploratory (omitted)
- RULE110_CATEGORY_MISMATCH.md
- PRIMAL_POINTS_AND_COMPOSITE_RECURSION.md
- RESIDUE_OF_RESIDUE.md
- PRIMORIAL_LIFT_TEST.md
- PAIR_AS_INVARIANT_AUDIT.md
- PLANTED_SEAM_SPRINT_SPEC.md
- LADDER_V2.md
- MINIMAL_DESCRIPTION_LENGTH.md
- SEAM_EXTRACTION_OPTIONS.md
- SEAM_GEOMETRY_NOTE.md
- SEED_TO_STACK_TO_MEASUREMENT_MAP.md
- SHELL_NATIVE_BENCHMARKS.md
- RECIPE_VS_COINCIDENCE.md
- RANKED_INVARIANT_FAMILIES.md
- NATURAL_CARRIER_CRITERION.md
- PRISM_CONSISTENCY_AUDIT.md / v2
- LOCAL_NONLOCAL_SILOING_AUDIT.md
- LAWFUL_GENERALIZATION_SEARCH_PLAN.md
- META_CLASSIFICATION.md
- DECOMPOSITION_TABLE.md
- CONTAINER_FAMILY_CLASSIFICATION.md
- ECHO_RULE_UNIFICATION.md
- ANCHOR_DISTANCE_DEFINITION.md
- NULLS_V2.md
- CITATION_RIGOR_PROTOCOL.md
- GENERALIZATION_TABLE.md
- RING_RANKING_TABLE.md
- NOTATION_SHEET.md
- FALSIFIER_LIST.md
- CONTROL_DOCUMENT.md / V2
- FLOW_BRIDGE_GEOMETRY_NOTES.md
- INVARIANTS_BEYOND_TSML.md (contains broader invariant candidates; omit per user's no-broader-synthesis rule)

### B1 (already delivered)

B1 is not in this pack. The B1 pre-reg (`B1_NSCG_SPEC_v1.0.md`) and the B1 curve-analysis addendum (`B1_CURVE_ANALYSIS_ADDENDUM_v1.0.md`) were the previous handoff. ClaudeCode already holds them.

ClaudeCode's task: when integrating this pack, **slot B1's existing files into the same folder structure** this pack proposes:
- B1 pre-reg → `controls/B1_NSCG_SPEC_v1.0.md`
- B1 addendum → `controls/B1_CURVE_ANALYSIS_ADDENDUM_v1.0.md` (or into a `sprints/B1_NSCG/` directory if B1 results exist separately; ClaudeCode's judgment based on the B1 material on hand)

SPRINT_LEDGER.md should be updated by ClaudeCode to include B1's row if B1 produced a verdict ClaudeCode needs to record. This packaging pass did not have access to B1's post-execution state and so leaves B1's ledger entry for ClaudeCode to populate from the B1 materials it already holds.

### Drafts superseded or intermediate (omitted)

- PATH3_SUBTYPE_ADJACENCY_PREREG_DRAFT.md — superseded by PATH3_SUBTYPE_ADJACENCY_V12_PREREG.md.
- COUNT_V12_DESIGN_CONCERN.md — superseded by WHY_COUNT_IS_NOT_LIVE_UNDER_P3AP.md (which is included, renamed for the pack).
- S30_PREREG_RECOMMENDATION.md, S31_FIRSTRUN_RECOMMENDATION.md — superseded by the actual pre-regs.
- CLAUDECODE_SPRINT15_DIRECTIVE.md, CLAUDECODE_SPRINT15_UNSTUCK.md — pre-B1 direction documents.
- SPRINT_CLOSEOUT_HANDOFF.md — older handoff doc.
- CHAT_CLAUDE_TO_CLAUDECODE.md — older chat-format doc.
- NEGATIVE_RESULTS_APPENDIX.md — content absorbed into SPRINT_LEDGER.md.
- EMPTY_SEAM_NOTE.md — content covered by S30 DEGENERATE_PASS_NOTE and S30b VERDICT.

---

## Light Cleanup Required

### Rename operations

- Move `S31_Z10_PILOT.md` → `controls/S31_Z10_PILOT_v1.0.md` (clarifies version).
- Move `WHY_COUNT_IS_NOT_LIVE_UNDER_P3AP.md` → `open_questions/COUNT_TRANSPORT_CLOSED_UNDER_P3AP.md` (clarifies intent as closure document).

### New files to create

- **README.md** at pack root — table of contents, navigation only, no claims.
- **HUB_EXTENSION_DEFERRED.md** in open_questions — short note (< 50 lines) stating the deferral without re-arguing it.
- **SPRINT_LEDGER.md** — created separately, content in separate deliverable.
- **CURRENT_STATE_SUMMARY.md** — created separately, content in separate deliverable.
- **PACKING_RULES.md** — created separately.

### No content changes

- All included documents copied verbatim from their current state on disk.
- No retroactive rewording.
- No verdict softening.
- No metric re-statement.
- Only formatting cleanup permitted: leading/trailing whitespace normalization, line-ending normalization to LF, duplicate blank line collapse (if any).

---

## What Is NOT in This Pack

Restating explicitly for clarity:

- No STD bridge language.
- No spectral 3/4 audit.
- No physics/ontology discussion.
- No broad philosophical notes.
- No abandoned speculative bridge drafts.
- No duplicate interim design notes unless they condition a verdict.
- No re-synthesis of PASS/UNCLEAR/FAIL into composite claims.
- No theorem promotion of any Path 2 or Path 3 result.

---

## Total File Count

- Root: 4 files (README, summary, rules, this plan)
- foundation/: 8 files
- theorem_local_chart/: 4 files
- controls/: 11 files
- sprints/: 1 ledger + 11 subdirs × ~3-7 files each ≈ 45 files
- open_questions/: 3-4 files

**Total: ~75-76 files.** Compact and navigable.

---

## GitHub Safety

The pack contains:
- No executable scripts at top level (scripts live in per-sprint subdirectories and are reproducibility artifacts, not executables).
- No binary files.
- No zip archives.
- No large data files (all scores.json files are small < 50 KB).
- No external-URL-dependent content.
- No secrets, no API keys, no authentication tokens.
- All content text/markdown/json/csv.

Safe for public repository.

---

## Handoff Verification

ClaudeCode should verify:

1. Folder structure matches this plan.
2. File count matches ~75-76.
3. Every sprint subdirectory contains at least one VERDICT file.
4. Every pre-reg in controls/ corresponds to a sprint in sprints/.
5. SPRINT_LEDGER.md covers all 11 sprints.
6. No omitted-list document is present.
7. README.md reflects actual structure.

If any verification fails, return to this handoff plan before committing.
