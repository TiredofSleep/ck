# Pair-Primitive Addendum — 2026-04-18
## Closeout of the PPM Sprint Arc

---

## What This Pack Is

A closeout addendum to the frozen `pair_primitive_pack_2026_04_18/`. Contains two executed sprints (PPM-v2.1, PPM-v3.0) plus foundation-register context that supports them, plus the Path B decision record on V0 and the handoff documentation for ClaudeCode.

This pack is **additive** to the existing repo state. Nothing in the prior PPM pack is modified, duplicated, or reframed.

## Relationship To Prior Packs

```
tig-synthesis/
├── b2_sprint_tig_pack_2026_04_17/              # closed (11 sprints, do not touch)
├── pair_primitive_pack_2026_04_18/             # closed (v1.0, v1.1, v2.0; do not touch)
├── shape_admissibility_foundation_2026_04_18/  # closed (SAH at foundation register)
└── pair_primitive_addendum_2026_04_18/         # THIS PACK (v2.1, v3.0, closeout)
```

The addendum extends but does not replace. All prior verdicts stand as originally recorded.

## Navigation

| Location | Contents |
|---|---|
| `README.md` | This file. |
| `PPM_SPRINT_CLOSEOUT_HANDOFF.md` | Four-section closeout summary: what's finished, what's earned, what ClaudeCode should do, what remains open. Start here. |
| `WHAT_CLAUDECODE_SHOULD_CHANGE_AND_NOT_CHANGE.md` | Concrete repo-facing instructions: where to place the addendum, what to leave frozen, what not to reopen, PPM/Hodge separation rules. |
| `WHY_THIS_ARC_IS_READY_TO_HAND_OFF.md` | Three stopping conditions and the positive case for handoff now without another sprint. |
| `V0_PATH_B_CLOSURE.md` | Decision record closing V0 lane at UNCLEAR by Sensitivity. |
| `sprints/PPM_v2.1_additive_transport/` | Sprint 15 artifacts: PREREG, RESULTS, VERDICT, REPRO, per-carrier JSON, scoring script. FAIL Uniform. |
| `sprints/PPM_v3.0_V0_boundary/` | Sprint 16 artifacts: revised PREREG (Source 3 sensitivity branch), RESULTS, VERDICT, REPRO, scores JSON, scoring script. UNCLEAR by Sensitivity. |
| `foundation_sprint_context/` | Seven foundation notes (Why V0 first / What a boundary checkpoint adds / Why Source 3 became sensitivity branch / What counts as robust / Attractor-privilege foundation / S3a vs S3b comparison / What justifies v3.0.1 or stopping). |

## Verdict Ledger Addition

| # | Sprint | Path | Verdict | Attribution |
|---|---|---|---|---|
| 15 | PPM-v2.1 | 3 (bridge test) | **FAIL Uniform** | $N_B = N_A = 0$, $N_I = 8$; per-carrier +2/−2, gap 4; additive non-discrimination transports Reason A from Z/10 to the P3AP family. |
| 16 | PPM-v3.0 | 1 (V0 boundary) | **UNCLEAR by Sensitivity** | Fixed sources +3/−3; S3a → PASS-V0-I (+4/−4, gap 8); S3b → FAIL (+2/−2, gap 4); branches disagree on attractor-privilege direction. |

Sprints 1–11 are in the B2 pack; 12–14 are in the original pair-primitive pack. The 2×2 subtype-mapping design space is complete with v2.1; v3.0 opens a second structurally-independent checkpoint and closes at sensitivity-diagnostic.

## What The Framework Has And Has Not Earned (Unchanged From Prior Pack + New Items)

**Earned:**
- Local multiplicative PASS on Z/10 seam (v1.0).
- Local additive FAIL on Z/10 seam (v1.1).
- Family multiplicative transport PASS across 8 P3AP carriers (v2.0).
- Family additive transport FAIL across 8 P3AP carriers (v2.1) — carrier-family property of multiplicative loading.
- V0 boundary diagnostic: UNCLEAR by Sensitivity at the attractor-privilege hinge (v3.0).
- Seven foundation notes specifying V0 checkpoint structure and post-v3.0 resolution options.

**Not earned:**
- Framework correctness in general.
- Operationalization-independence at any scope.
- Extension beyond Z/10 seam + 8 P3AP carriers + Z/10 V0.
- Any scale-example realization.
- Any physics, ontology, or cross-domain reading.
- SAH validation.
- A resolved direction for attractor privilege at boundary regions.

## Reading Order For New Eyes

1. `PPM_SPRINT_CLOSEOUT_HANDOFF.md` — four-section orientation.
2. `WHAT_CLAUDECODE_SHOULD_CHANGE_AND_NOT_CHANGE.md` — operational repo instructions.
3. `sprints/PPM_v2.1_additive_transport/PPM_V21_ADDITIVE_TRANSPORT_VERDICT.md` — v2.1 verdict.
4. `sprints/PPM_v3.0_V0_boundary/PPM_V30_V0_VERDICT.md` — v3.0 verdict.
5. `foundation_sprint_context/ATTRACTOR_PRIVILEGE_FOUNDATION.md` — what the v3.0 hinge is.
6. `V0_PATH_B_CLOSURE.md` — why the V0 lane is closed.
7. Remaining foundation notes as needed.

## Scope Of This Archive

Snapshot. Frozen on commit. Changes require a new sidecar pack, not edits to this one.

## Commit Message Suggestion

```
Add pair_primitive_addendum_2026_04_18 (PPM closeout: v2.1 + v3.0 + V0 Path B + foundation context)
```
