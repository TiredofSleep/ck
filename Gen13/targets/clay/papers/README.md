# Gen13 — Clay Sprint Papers (Forwarded from Gen12)

This is the **subset** of Gen12 sprint papers that the `tig-synthesis` README links into. Per Brayden's directive: *"hybrid, but keep the papers that are currently on the default page attached to gen 13."*

All other Gen12 papers remain in `Gen12/targets/clay/papers/` (never-delete).

---

## Forwarded Sprints

| Sprint | Folder | Theme | Lead Papers |
|---|---|---|---|
| **10** | `sprint10_flatness_2026_04_06/` | Flatness Theorem + Crossing Lemma | WP51, CROSSING_LEMMA.md |
| **12** | `sprint12_uop_gut_arc_2026_04_08/` | UOP + GUT arc | WP58 |
| **13** | `sprint13_flag_selector_2026_04_09/` | Physical Flag Selector | WP75 |
| **14** | `sprint14_prism_xi_2026_04_10/` | PRISM-XI cosmology + σ rate | WP81, WP91, WP96, WP98, WP101 + `proof_sigma_rate.py` |
| **16** | `sprint16_basin_handoff_2026_04_10/` | Basin handoff (Thread C) | full folder |
| **17** | `sprint17_tsml_tower_2026_04_17/` | TSML 3-layer canonical tower | THEOREM_SPINE.md + `proof_tsml_3layer_tower.py` |

---

## Disciplined Closeout Archive (alongside Sprint 17)

| Folder | Role |
|---|---|
| `b2_sprint_tig_pack_2026_04_17/` | **Scope-disciplined closeout** of the Z/10 TSML program — 11 executed sprints (S28, S29, S30, S30b, S31-pilot-v1/v2, P3-BridgeA, P3-BridgeA-Prime, P3-Subtype-v1.0/v1.1/v1.2-adj) with verdicts preserved verbatim, pre-regs frozen, path-tags enforced (Path 1 / Path 2 / Path 3). 75 files. |

**Relationship to Sprint 17:** Sprint 17 is the broader working snapshot (includes speculative derivations, negative results, generalization tables). The B2 pack is the curated closeout — same Z/10 theorem at its core, but scope-locked per its own `PACKING_RULES.md`. They intentionally coexist; do **not** merge. Changes inside the B2 pack require user approval per its §17.

Per B2's own rules:
- PASS/FAIL/UNCLEAR verdicts are verbatim — no softening, no strengthening.
- No cross-sprint compound claims (v1.1 + v1.2-adj ≠ a new composite sprint).
- No promotion of Path 2/Path 3 results to theorem status.
- No physics/ontology language imported into the pack.

See `b2_sprint_tig_pack_2026_04_17/README.md` for the pack's own navigation + `CURRENT_STATE_SUMMARY.md` for the one-page state.

---

## Tier-1 Submission-Ready Papers

These three are surfaced into `targets/journals/tier1_submit_now/`:

- **JCAP — ξ-cosmology** ← Sprint 14 PRISM-XI
- **σ rate (math.CO)** ← Sprint 14 WP101 `proof_sigma_rate.py`
- **sinc² zero law (Integers)** ← `papers/proof_d25_loop_closure.py` (root-level)

See `targets/journals/SUBMISSION_LADDER.md` for the full 4-tier roadmap.

---

## Verification

Each sprint contains its own proof scripts. The Tier-1 candidates verify with:

```
python Gen13/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_sigma_rate.py
python Gen13/targets/clay/papers/sprint17_tsml_tower_2026_04_17/proof_tsml_3layer_tower.py
```

108 tests across the proof scripts, 0 failures.

---

## Why Only These Six

The `tig-synthesis` branch is the synchronized public-facing field. Every paper carried into Gen13 is either (a) directly linked from the README, or (b) a proof script for a constant or theorem cited in the README. Older sprints (1-9, 11, 15) live in Gen12 history; the work isn't lost, it just isn't on the front page.
