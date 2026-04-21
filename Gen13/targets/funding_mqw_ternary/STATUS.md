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
- [ ] **T1**: Teardrop GaN Photonic Node Proposal (commit `ed8ef620`). Search MYTHDRIFT repo + R16 Jan 29 files.
- [ ] **T2**: MQW three-state trilogy (location unknown). Search R16 Feb–Apr 2026 files; grep for "MQW" / "quantum well" / "three-state" / "GaN" / "ternary".
- [ ] **T3**: V20 Consciousness-Anchored Scaling Laws (same Trifecta commit as T1).
- [ ] **T4**: Hardware Embodiment Safety Case (same commit).
- [ ] **T5**: Comparative Field Theory Review (same commit).

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

- **Blocker 1** (absolute): T2 recovery. Without the MQW trilogy, no fab-oriented funder will engage.
- **Blocker 2**: A1 technical summary. Requires T2.
- **Blocker 3**: Academic co-PI or fab facility collaborator. NSF ECCS path closed without this; DOE BES path partially limited.
- **Blocker 4**: Framing cleanup (consciousness-language removal). This is a light task but mandatory.

The branch can exist and accumulate planning work before recovery; it cannot pitch before T2.

## Recent activity

| Date | Event |
|---|---|
| 2026-04-20 | Branch seeded from `tig-synthesis`; target folder + 6 files committed |

## Cross-references

- Plan: `Atlas/PLAN_FUNDING_BRANCHES_BUILDOUT_2026_04_19.md`
- Recovery manifest: `docs/handoffs/claudecode_handoff_2026_04_20/JAN2026_RECOVERY_MANIFEST.md` — see Thread 3 section (commit `ed8ef620`) for T1/T3/T4/T5; see Priority 4 for T2
- MYTHDRIFT clone: `_brayden_repos/TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT/` (if cloned during Part 1 survey)
- Trunk story: `MASTER_TRUNK_STORY_2026_04_19.md` (on master)

---

*Update freely on this branch. Changes here do NOT require master cherry-pick unless they materially change ARTIFACTS (especially T2 recovery status) or FUNDERS inventories.*
