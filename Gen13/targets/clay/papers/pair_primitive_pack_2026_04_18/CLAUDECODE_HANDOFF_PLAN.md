# ClaudeCode Handoff Plan — Pair-Primitive Framework Pack
## What To Do With This Archive

---

## Pack Identity

**Name:** `pair_primitive_pack_2026_04_18`
**Date:** 2026-04-18
**Relationship to B2 pack:** extension, not replacement.

## What This Pack Is

Three executed sprints (PPM-v1.0, v1.1, v2.0) adding a pair-primitive framework checkpoint layer on top of the B2 sprint archive. Foundation sprint (4 documents) establishing the framework. Six scope notes (one per sprint × two — "why this sprint comes now" + "outcome meaning before execution"). Three frozen pre-registrations. Three sets of sprint artifacts (RESULTS, VERDICT, REPRO). One open-question file describing PPM-v2.1 as the first authorized next checkpoint.

Total: 29 files across a structured folder layout.

## Expected Handoff Action

The user's GitHub repository has a `tig-synthesis` branch containing the B2 pack. This new pack should be added **alongside** the B2 pack in the same branch (or a new branch if the user prefers), not inside or replacing it.

Suggested repository layout after handoff:

```
tig-synthesis/
├── b2_sprint_tig_pack_2026_04_17/    # existing, unchanged
└── pair_primitive_pack_2026_04_18/   # new, this pack
```

Both packs are independent archives that cross-reference each other. B2 does not need to be touched.

## Folder Layout Within This Pack

```
pair_primitive_pack_2026_04_18/
├── README.md                              # Entry point; navigation guide
├── CURRENT_STATE_SUMMARY.md               # What's exact / validated / open
├── SPRINT_LEDGER.md                       # Three new sprints, one-line each
├── PACKING_RULES.md                       # Extends B2 rules 1-17 with rules 18-23
├── CLAUDECODE_HANDOFF_PLAN.md             # This file
├── foundation/
│   ├── WHY_THE_WHOLE_INTERACTION_MUST_BE_SEEN_AT_ONCE.md
│   ├── THREE_ASPECTS_OF_HOLD.md
│   ├── GAP_AS_BOUNDARY_NOTHINGNESS.md
│   ├── HOLD_GAP_FLOW_FOUNDATION.md
│   └── scope_notes/
│       ├── WHY_THIS_IS_THE_FIRST_REAL_CHECKPOINT.md
│       ├── PASS_MEANING_SCOPE_NOTE.md
│       ├── WHY_ADDITIVE_COMES_NEXT.md
│       ├── STABILITY_VS_FLIP_SCOPE_NOTE.md
│       ├── WHY_V20_COMES_BEFORE_HANDOFF.md
│       └── TRANSPORT_PASS_FAIL_SCOPE_NOTE.md
├── controls/
│   ├── PAIR_PRIMITIVE_MAPPING_PREREG.md       # PPM-v1.0 pre-reg
│   ├── PPM_V11_ADDITIVE_PREREG.md             # PPM-v1.1 pre-reg
│   └── PPM_V20_MULTIPLICATIVE_PREREG.md       # PPM-v2.0 pre-reg
├── sprints/
│   ├── PPM_v1.0_multiplicative_local/
│   │   ├── PAIR_PRIMITIVE_MAPPING_RESULTS.md
│   │   ├── PAIR_PRIMITIVE_MAPPING_VERDICT.md
│   │   └── PAIR_PRIMITIVE_MAPPING_REPRO.md
│   ├── PPM_v1.1_additive_local/
│   │   ├── PPM_V11_ADDITIVE_RESULTS.md
│   │   ├── PPM_V11_ADDITIVE_VERDICT.md
│   │   └── PPM_V11_ADDITIVE_REPRO.md
│   └── PPM_v2.0_multiplicative_transport/
│       ├── PPM_V20_MULTIPLICATIVE_RESULTS.md
│       ├── PPM_V20_MULTIPLICATIVE_VERDICT.md
│       ├── PPM_V20_MULTIPLICATIVE_REPRO.md
│       ├── PPM_V20_PER_CARRIER_SCORES.json    # per-carrier score data
│       └── ppm_v20_score.py                   # deterministic scoring script
└── open_questions/
    └── PPM_V21_ADDITIVE_TRANSPORT_FIRST_OPEN_CHECKPOINT.md
```

## What Is Included From B2 (Nothing Duplicated)

The B2 pack remains the canonical home for:
- `foundation/SCOPE_TAG_TEMPLATE.md`
- `foundation/ATTRACTOR_RECONCILIATION.md`
- `foundation/OBJECT_TYPE_ATLAS.md`
- `foundation/COMPARISON_LAW.md`
- `foundation/SPRINT_SELECTOR.md`
- `theorem_local_chart/THEOREM_SPINE.md`
- `theorem_local_chart/CANONICAL_TSML_CONSTRUCTION.md`
- All 11 B2 sprint artifact folders

This pack references those documents by path but does not copy them.

## Cleanup Operations

**Required:** none.

All 24 content files were copied verbatim from `/home/claude/foundation_sprint/` during pack assembly. No transformations, no edits. Every sprint file, pre-reg, and scope note is as it was when written. No orphan files are staged.

## Verification Steps For ClaudeCode

Before committing this pack to the repository:

1. **File count check:** pack contains exactly 29 files (5 pack-root documents + 4 foundation docs + 6 scope notes + 3 pre-regs + 3 sprints × 3-5 files + 1 open-question document).
2. **Every sprint has a VERDICT file:** `sprints/*/PPM*VERDICT.md` or `sprints/*/PAIR_PRIMITIVE_MAPPING_VERDICT.md`.
3. **Every sprint has a REPRO file:** similarly.
4. **PPM-v2.0 has its deterministic code:** `ppm_v20_score.py` and `PPM_V20_PER_CARRIER_SCORES.json`.
5. **Cross-references to B2 are by path, not by copy:** verify no B2-exclusive files were duplicated here.

## What To Do If A User Asks Questions About The Pack

| Question | Answer location |
|---|---|
| What does the framework claim? | `foundation/HOLD_GAP_FLOW_FOUNDATION.md` |
| What's the first real result? | `sprints/PPM_v1.0_multiplicative_local/PAIR_PRIMITIVE_MAPPING_VERDICT.md` |
| Does it extend to other rings? | `sprints/PPM_v2.0_multiplicative_transport/PPM_V20_MULTIPLICATIVE_VERDICT.md` |
| Did it fail anywhere? | `sprints/PPM_v1.1_additive_local/PPM_V11_ADDITIVE_VERDICT.md` |
| What's next? | `open_questions/PPM_V21_ADDITIVE_TRANSPORT_FIRST_OPEN_CHECKPOINT.md` |
| Current state summary? | `CURRENT_STATE_SUMMARY.md` |
| What are the rules? | `PACKING_RULES.md` (local) + B2's `PACKING_RULES.md` (inherited) |

## Discipline For Future PPM Sprint Additions

If additional PPM sprints are run later (PPM-v2.1, v1.1.1, v3.0), they should be added either:

- **As a new pack** (`pair_primitive_pack_[date]`) extending this one, with cross-references.
- **Inside this pack** only if the pack is explicitly reopened for editing, which requires user approval per B2 Rule 5 (frozen-pack non-editing).

The default assumption is: this pack is frozen as of 2026-04-18. New work creates a new pack.

## Summary

Add `pair_primitive_pack_2026_04_18/` alongside `b2_sprint_tig_pack_2026_04_17/` in the repository. Do not modify the B2 pack. This pack is self-navigating via README.md and CURRENT_STATE_SUMMARY.md. One follow-up checkpoint (PPM-v2.1) is named but not executed.
