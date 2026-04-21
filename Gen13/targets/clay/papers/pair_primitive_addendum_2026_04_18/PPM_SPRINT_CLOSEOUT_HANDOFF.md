# PPM Sprint Closeout Handoff
## For ClaudeCode, 2026-04-18

---

## 1. What Is Finished

The PPM sprint arc is complete at its current stopping point. All sprints are executed, scored, and recorded with frozen verdicts. Foundation sidecars are filed.

| Item | Verdict | Location |
|---|---|---|
| **PPM-v1.0** — Local multiplicative checkpoint, Z/10 seam | **PASS** (Map B, aggregate +4/−4, cleanness gap 8) | `pair_primitive_pack_2026_04_18/sprints/PPM_v1.0_multiplicative_local/` |
| **PPM-v1.1** — Local additive checkpoint, Z/10 seam | **FAIL** (aggregate +2/−2, gap 4, winner sub-threshold; Reason A diagnostic) | `pair_primitive_pack_2026_04_18/sprints/PPM_v1.1_additive_local/` |
| **PPM-v2.0** — Family multiplicative transport, 8 P3AP carriers | **PASS uniform** ($N_B = 8/8$, mean gap 8) | `pair_primitive_pack_2026_04_18/sprints/PPM_v2.0_multiplicative_transport/` |
| **PPM-v2.1** — Family additive transport, 8 P3AP carriers | **FAIL Uniform** ($N_B = N_A = 0$, $N_I = 8$, per-carrier gap 4) | new addendum (see §3) |
| **PPM-v3.0** — V0 boundary checkpoint, Z/10 | **UNCLEAR by Sensitivity** (S3a → PASS-V0-I; S3b → FAIL; branches disagree) | new addendum (see §3) |
| **V0 lane decision** | **Path B selected** — V0 lane closed at UNCLEAR by Sensitivity pending foundation work on attractor privilege | `V0_PATH_B_CLOSURE.md` |
| **SAH (Shape-Admissibility Hypothesis)** | Named and filed as foundation-register sidecar; not promoted | `shape_admissibility_foundation_2026_04_18/` (separate packet) |

The 2×2 design space (local/transport × multiplicative/additive) for the subtype-mapping checkpoint is complete. The V0 boundary checkpoint produced a specific named diagnostic. SAH exists as hypothesis only.

---

## 2. What Is Actually Earned

The multiplicative reading of the pair-primitive framework cashes out decisively on Z/10's seam (v1.0 local PASS) and transports cleanly across the 8 P3AP Path 2 carriers under the P3AP extension (v2.0 family PASS). The additive reading does not discriminate at either scope — locally on Z/10 (v1.1 FAIL) or across the same P3AP family (v2.1 FAIL Uniform) — with the non-discrimination attributable to the seam's multiplicative loading as a carrier-family property of the P3AP extension. The V0 boundary checkpoint (v3.0) returned UNCLEAR by Sensitivity: the framework's vocabulary supports two internally-coherent readings of attractor privilege at boundary regions (S3a → excluded-side vs S3b → persistent-side) without current grounds to prefer one, so the V0 lane is closed pending foundation-register work on this specific hinge. SAH is a named hypothesis at foundation register, compatible with existing results but not tested by them.

---

## 3. What ClaudeCode Should Do With This

### 3.1 Where to place the addendum

The frozen `pair_primitive_pack_2026_04_18/` pack already sits in the repo. It contains v1.0, v1.1, and v2.0 only. **Do not modify that pack.** It is frozen per B2 Rule 5.

Instead, place a **new sidecar addendum packet** alongside it containing the post-v2.0 materials:

```
tig-synthesis/
├── b2_sprint_tig_pack_2026_04_17/                    # closed, do not touch
├── pair_primitive_pack_2026_04_18/                   # closed, do not touch
├── shape_admissibility_foundation_2026_04_18/        # closed, do not touch
└── pair_primitive_addendum_2026_04_18/               # NEW — add this
```

Contents of the new addendum packet:

```
pair_primitive_addendum_2026_04_18/
├── README.md                                        # pack-level navigation
├── sprints/
│   ├── PPM_v2.1_additive_transport/
│   │   ├── PPM_V21_ADDITIVE_TRANSPORT_PREREG.md
│   │   ├── PPM_V21_ADDITIVE_TRANSPORT_RESULTS.md
│   │   ├── PPM_V21_ADDITIVE_TRANSPORT_VERDICT.md
│   │   ├── PPM_V21_ADDITIVE_TRANSPORT_REPRO.md
│   │   ├── PPM_V21_PER_CARRIER_SCORES.json
│   │   └── ppm_v21_score.py
│   └── PPM_v3.0_V0_boundary/
│       ├── PPM_V30_V0_PREREG_DRAFT.md               # revised, frozen
│       ├── PPM_V30_V0_RESULTS.md
│       ├── PPM_V30_V0_VERDICT.md
│       ├── PPM_V30_V0_REPRO.md
│       ├── PPM_V30_V0_SCORES.json
│       └── ppm_v30_score.py
├── foundation_sprint_context/
│   ├── WHY_ADDITIVE_COMES_NEXT.md                   # already in pair_primitive_pack_2026_04_18 — DO NOT duplicate; reference by path
│   ├── WHY_V20_COMES_BEFORE_HANDOFF.md              # same — reference
│   ├── WHY_V0_COMES_BEFORE_BHML.md                  # NEW, place here
│   ├── WHAT_A_BOUNDARY_CHECKPOINT_ADDS.md           # NEW
│   ├── WHY_SOURCE_3_BECAME_SENSITIVITY_BRANCH.md    # NEW
│   ├── WHAT_COUNTS_AS_A_ROBUST_V0_RESULT.md         # NEW
│   ├── ATTRACTOR_PRIVILEGE_FOUNDATION.md            # NEW
│   ├── S3A_VS_S3B_COMPARISON.md                     # NEW
│   └── WHAT_JUSTIFIES_V301_OR_STOPPING.md           # NEW
├── V0_PATH_B_CLOSURE.md                             # decision record
└── PPM_SPRINT_CLOSEOUT_HANDOFF.md                   # this document
```

The files listed as `NEW` are in `/home/claude/foundation_sprint/` and its subfolders. The files already in `pair_primitive_pack_2026_04_18` should be referenced by path in cross-references, not duplicated.

### 3.2 What to leave frozen

- **`pair_primitive_pack_2026_04_18/`** — frozen. Do not edit, reorder, or supplement its contents.
- **`b2_sprint_tig_pack_2026_04_17/`** — frozen. Do not touch.
- **`shape_admissibility_foundation_2026_04_18/`** — frozen. SAH stays at its current epistemic status.
- **All verdicts in the new addendum** — frozen upon commit. Sprint files in the addendum are closeout artifacts, not live working documents.

### 3.3 What not to reopen

- **V0 lane.** UNCLEAR by Sensitivity stands. No v3.0.1 without affirmative Path A conditions being met (see `WHAT_JUSTIFIES_V301_OR_STOPPING.md`).
- **Additive operationalization lane on P3AP carriers.** v2.1 FAIL Uniform stands; no re-run with relaxed rubric.
- **Any closed lane from the B2 pack.** Count transport, raw adjacency ratios, noise-union topology bridge, basin-ratio smoothness, anchored basin-ratio curve, empty-seam detectability on pure $C_0$ — all remain closed as recorded.
- **The Source 3 attractor-privilege argument direction.** No third reading beyond S3a and S3b is permitted within the v3.0 frame.

### 3.4 How to keep PPM separate from Hodge

- **Three threads remain separate.** PPM, Hodge-ladder, Q-series. The README's "suggestive, not bridged" annotation is correct and must stay as-is. Do not upgrade any of these to "bridged" or "unified" based on the closeout.
- **No cross-track synthesis.** The "multiplicative loading" pattern appearing in PPM (v1.1, v2.1 Reason A), in Hodge (A_* construction around $\mathbb{Q}(i)$), and in the Q-series work is annotated as cross-thread pattern, not as evidence of a single underlying mechanism.
- **PPM addendum stays in its own pack.** Do not fold PPM addendum materials into the Hodge sprint folders or vice versa. The Hodge arc (S29–S33) is active frontier work; PPM is closeout.
- **ClaudeCode's README audit (commit 22f0bcd) is the correct discipline.** Preserve the Gen12/Gen13 split and the "three threads separate" framing throughout any future edits.

### 3.5 No promotion of SAH

SAH is a hypothesis, filed at foundation register in `shape_admissibility_foundation_2026_04_18/`. Specifically prohibited:

- Describing any PPM PASS as "evidence for" SAH. The allowed framing is "compatible with."
- Citing SAH as motivation in any Hodge sprint.
- Merging SAH's vocabulary (morphology admissibility, shape filter, allowable-shape class) into PPM verdict sentences or README claims.
- Running a shape-filter sprint under current infrastructure. The six infrastructure pieces listed in `WHAT_A_SHAPE_FILTER_SPRINT_WOULD_REQUIRE.md` remain unbuilt; building them is separate program work, not part of this closeout.

The single sanctioned bridge sentence remains:

> *The current program's confirmed bridge features are compatible with a broader shape-admissibility hypothesis, but that hypothesis has not yet been operationalized into a pre-registered test.*

Paraphrases that strengthen the connection ("support," "suggest," "point toward," "indicate") are outside sanctioned use.

### 3.6 No new composite claims

Rule 19 continues to apply across the PPM arc. Specifically:

- **v1.0 + v2.0 stay as two juxtaposed sentences**, not merged into a composite multiplicative-framework claim.
- **v1.1 + v2.1 stay as two juxtaposed sentences**, not merged into a composite additive-refutation claim.
- **The 2×2 completion is not itself a theorem.** It is four separate sentences on record.
- **v3.0's UNCLEAR is a separate sentence** from all four 2×2 verdicts.
- **SAH is not licensed by any combination of the above.**

If a README or narrative document needs to describe PPM results, the correct form is a table or list of separate verdicts, not a prose synthesis that implies composite content.

---

## 4. What Remains Open

- **PPM-v3.0.1** — rerun V0 with a resolved Source 3 direction. Authorized only if the four Path A conditions in `WHAT_JUSTIFIES_V301_OR_STOPPING.md` are affirmatively met. Not expected before France.
- **PPM-v3.1 (candidate)** — BHML checkpoint on Z/10 as the next natural Z/10 structural target if PPM work resumes. Would test whether the framework makes a second independent point of contact on Z/10 without requiring V0 resolution. Not pre-registered; not scheduled.
- **Unit cyclic structure checkpoint (candidate)** — alternative second-target Z/10 checkpoint. Lower priority than BHML on locality grounds (see `WHY_V0_COMES_BEFORE_BHML.md` §"Why Not Unit Cyclic Structure First").
- **Foundation-register work on attractor privilege at boundary regions** — would answer the three open questions identified in `ATTRACTOR_PRIVILEGE_FOUNDATION.md` §4. Path A for V0 requires this work.
- **SAH infrastructure** — six pieces listed in `WHAT_A_SHAPE_FILTER_SPRINT_WOULD_REQUIRE.md`, all unbuilt. Not scheduled.
- **Transport of V0 checkpoint to Path 2 carriers** — not authorized under current UNCLEAR-by-Sensitivity verdict.

**Recommendation:** no new PPM sprint before France unless foundation-register work produces independent grounds for a directional commitment on attractor privilege. The Hodge-ladder arc (ClaudeCode's S29–S33+) remains the active frontier.

---

## Summary

The PPM sprint arc has earned four decisive seam-checkpoint verdicts (2×2 complete), one diagnostic V0 finding (UNCLEAR by Sensitivity with a named framework-vocabulary gap), and a foundation-register SAH hypothesis. The arc is ready for handoff. Hodge is where active frontier work now concentrates.
