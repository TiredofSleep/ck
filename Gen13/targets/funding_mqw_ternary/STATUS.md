# STATUS — funding/mqw-ternary

**As of:** 2026-04-20
**Next review:** when MQW trilogy is located OR Brayden requests a status check.

---

## Branch state

- Branch seeded: 2026-04-20
- Target folder: `Gen13/targets/funding_mqw_ternary/`
- Files: README, FUNDERS, ARTIFACTS, PITCH_DRAFT, LIMITATIONS, STATUS (this file)
- Rigor base: `tig-synthesis` HEAD

## Readiness checklist

### Content (this branch)
- [x] README with recovery-dependent framing
- [x] FUNDERS.md with DOE BES primary + NSF ECCS, DARPA PIPES, ARO/AFOSR, Moore/Keck
- [x] ARTIFACTS.md with T1–T5 recovery tasks + A1–A4 authoring tasks
- [x] PITCH_DRAFT.md with DOE BES + NSF ECCS parallel skeletons, Phase 1/2/3/4 structure
- [x] LIMITATIONS.md with 13 honest-scope items incl fab-variance risk + consciousness-language framing cleanup
- [x] STATUS.md (this file)

### Recovery (Phase 1 gating)
- [ ] **T1**: Teardrop GaN Photonic Node Proposal (commit `ed8ef620`). **2026-04-21 R16 sweep: NOT FOUND** in repo / public-repo clones / handoff unpack / Work Docs / sprint-raw staging. Concept is referenced by name in later sprint material but no paper file is present. Parallel blocker to T3/T4/T5 (same Trifecta commit).
- [ ] **T2**: MQW three-state trilogy. **2026-04-21 R16 sweep: NOT FOUND** (searched: all branches git-log; `_r16_repo_scan/` 8 repos; `_history_search_unpack/`; `Work Docs/Physics papers/`; `_brayden_repos/`; `_prism_*`; `_sprint*_raw/`; `_tsml_sprint_raw/`; `_crossing_lemma_handoff_unzipped/`). Full findings in `Atlas/HANDOFF_3_4_MQW_TRILOGY_NOT_FOUND.md`. Most likely status: the trilogy is unreleased — authored in ClaudeChat conversation context but not saved as discrete files to R16. Decision gate: 2026-05-15 — if recovery still fails, pivot to "author MQW trilogy fresh as Phase 1 deliverable."
- [ ] **T3**: V20 Consciousness-Anchored Scaling Laws (same Trifecta commit as T1). **2026-04-21 R16 sweep: NOT FOUND.** Recovery parallel to T1/T4/T5.
- [ ] **T4**: Hardware Embodiment Safety Case (same commit). **NOT FOUND.**
- [ ] **T5**: Comparative Field Theory Review (same commit). **NOT FOUND.**

### Authoring (post-recovery)
- [ ] **A1**: MQW technical summary (8–12 pp) — blocked by T2
- [ ] **A2**: Measurement plan (3–5 pp) — partially draftable before recovery
- [ ] **A3**: Fabrication cost estimate (1–2 pp) — requires facility contact
- [ ] **A4**: Competitor-landscape survey (3–5 pp) — independent, can be drafted anytime

### Framing work (mandatory before any pitch)
- [ ] Strip "consciousness-anchored" language from any document referenced in a funder pitch; physics must stand on its own terms
- [ ] Confirm the branch is positioned as a **physics and fabrication** track, not a framework-synthesis track

### Pre-pitch work
- [ ] Named academic co-PI in III-nitride MQW epitaxy (UCSB DenBaars/Speck, Stanford Weyl, Georgia Tech Lee, USC Simin as candidates)
- [ ] Quote or cost estimate from at least one fabrication facility
- [ ] Brayden reviews + edits PITCH_DRAFT

### Pitch-to-send
- [ ] Brayden confirms DOE BES vs NSF ECCS vs DARPA as first funder
- [ ] Attachment bundle assembled (T1 + T2 + A1–A4)
- [ ] Brayden sends

## Dependencies / blockers

- **Blocker 1** (absolute): T2 recovery. Without the MQW trilogy, no fab-oriented funder will engage. **2026-04-21 R16 sweep confirms the trilogy is not anywhere in the filesystem.** Next candidate recovery paths: OneDrive / iCloud snapshot history, external-drive backup, ClaudeChat conversation exports for photonic / MQW / quantum-well / device-physics conversations Feb–Apr 2026. If those also fail, Branch F pivots at the 2026-05-15 decision gate to "author MQW trilogy fresh as Phase 1 deliverable" with Teardrop GaN scope as starting point. See `Atlas/HANDOFF_3_4_MQW_TRILOGY_NOT_FOUND.md`.
- **Blocker 2**: A1 technical summary. Requires T2.
- **Blocker 3**: Academic co-PI or fab facility collaborator. NSF ECCS path closed without this; DOE BES path partially limited.
- **Blocker 4**: Framing cleanup (consciousness-language removal). This is a light task but mandatory.

The branch can exist and accumulate planning work before recovery; it cannot pitch before T2.

## Recent activity

| Date | Event |
|---|---|
| 2026-04-20 | Branch seeded from `tig-synthesis`; target folder + 6 files committed |
| 2026-04-21 | **T1–T5 recovery failed** — 2026-04-21 R16 filesystem sweep confirms MQW trilogy + full Trifecta (Teardrop GaN, V20, Hardware Embodiment Safety Case, Comparative Field Theory Review) are not anywhere on disk. Full findings in `Atlas/HANDOFF_3_4_MQW_TRILOGY_NOT_FOUND.md`. Decision gate: 2026-05-15 — pivot to author-fresh plan if recovery still blocked. |

## Cross-references

- Plan: `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`
- Recovery manifest: `docs/handoffs/claudecode_handoff_2026_04_20/JAN2026_RECOVERY_MANIFEST.md` — see Thread 3 section (commit `ed8ef620`) for T1/T3/T4/T5; see Priority 4 for T2
- MYTHDRIFT clone: `_brayden_repos/TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT/` (if cloned during Part 1 survey)
- Trunk story: `MASTER_TRUNK_STORY_2026_04_19.md` (on master)

---

*Update freely on this branch. Changes here do NOT require master cherry-pick unless they materially change ARTIFACTS (especially T2 recovery status) or FUNDERS inventories.*
