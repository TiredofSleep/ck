# ARTIFACTS — funding/mqw-ternary

This branch is the most recovery-heavy of the funding set. The conceptual ancestor exists in documented form; the current-generation work (the MQW trilogy) exists but is not yet located in this repo.

---

## Target artifacts (to be recovered)

### T1 — Teardrop GaN Photonic Node Proposal (conceptual ancestor)
- **Authored**: 2026-01-29 as part of Thread 3 Trifecta
- **Commit reference**: `ed8ef620` per `JAN2026_RECOVERY_MANIFEST.md`
- **Total Trifecta size**: ~134KB across 11 documents; the Teardrop piece is one of them
- **Thread 3 contents (per manifest)**:
  - V20 Consciousness-Anchored Scaling Laws
  - Hardware Embodiment Safety Case
  - Comparative Field Theory Review
  - **Teardrop GaN Photonic Node Proposal** ← this branch's primary ancestor
- **Recovery priority**: high; this is the latest located ancestor
- **Where to search**:
  1. MYTHDRIFT source — specifically `TIG-UNIFIED-THEORY-under-scrutinyMYTHDRIFT` repo
  2. ClaudeChat export bundle if available
  3. R16 filesystem Jan 29 2026 date range
  4. `archive_imports/` if already pulled
- **Destination**: `docs/archive_jan2026/teardrop_gan/` with provenance header

### T2 — MQW three-state paper trilogy (the current work)
- **Status**: location unknown
- **Content**: three papers advancing the ternary-MQW design beyond the Teardrop conceptual ancestor
- **Recovery priority**: **highest** — this branch's core technical content
- **Recovery strategy** (per `JAN2026_RECOVERY_MANIFEST.md` Priority 4):
  1. Search R16 for physics-content documents authored between Jan 29 and Apr 20 2026
  2. Grep for "MQW", "quantum well", "three-state", "ternary", "GaN" across filesystem and all archive_imports
  3. Check `archive_imports/feb2026/`, `archive_imports/mar2026/` if they exist
  4. Review ClaudeChat exports in the Feb–Apr window
- **Destination**: `docs/archive_mqw/` with provenance header
- **Blocker level**: absolute — no fab-oriented funder can engage without these

### T3 — V20 Consciousness-Anchored Scaling Laws
- **Co-located with**: Teardrop (same Trifecta commit `ed8ef620`)
- **Relevance**: may contain design-law statements relevant to MQW parameter selection; may also contain framing that MUST be adjusted before funder-facing use (the word "consciousness" in a photonic-hardware proposal is a problem unless the framing is clean)

### T4 — Hardware Embodiment Safety Case
- **Co-located with**: Teardrop
- **Relevance**: pre-existing safety-engineering thinking; useful for the agency-proposal section on risk

### T5 — Comparative Field Theory Review
- **Co-located with**: Teardrop
- **Relevance**: literature positioning for the Teardrop / MQW design

---

## Fresh artifacts required (to be authored after recovery)

### A1 — MQW three-state technical summary
- **Form**: 8–12 page technical document
- **Content**: distilled from T2 (MQW trilogy); specifies well widths, barrier heights, wavelength, distinguishability criterion, operating temperature
- **Blocker**: cannot be written until T2 is recovered

### A2 — Measurement plan
- **Form**: 3–5 page document
- **Content**: what instruments verify three-state operation, what is pass/fail
- **Can be drafted before recovery**: partially — the measurement instrument landscape is known to the field and can be scaffolded. Precise pass/fail criteria depend on A1.

### A3 — Fabrication cost estimate
- **Form**: 1–2 page document
- **Content**: named foundry, wafer size, cost per run, expected turnaround
- **Dependencies**: a collaborator or a quote from a facility
- **Candidate facilities**: UCSB Nanofabrication, Stanford Nano Shared Facilities, Georgia Tech IEN, commercial GaN foundries (Wolfspeed for SiC/GaN; specialty epitaxy houses for MQW)

### A4 — Competitor-landscape survey
- **Form**: 3–5 page survey
- **Content**: silicon-photonics logic (existing), optical-neural-network chips (Lightmatter, Lightelligence), Mach-Zehnder-based arithmetic (PSiQ), other ternary-logic approaches. Where does MQW ternary sit?
- **Can be drafted before recovery**: yes — this is an external-literature task independent of the MQW trilogy

---

## What is already in the ck repo (pre-existing, no recovery needed)

The ck repo does NOT currently contain MQW-specific photonic-computing content. The branch is a **recovery + authoring** branch, not a consolidation-of-existing branch. This is unusual relative to the other funding branches (TIG Unity, First-G, CK-interpretability all have substantial existing material).

---

## Recovery tasks summary

| Task | Target | Priority | Status |
|---|---|---|---|
| T1 | Teardrop GaN Photonic Node Proposal | high | NOT RECOVERED |
| T2 | MQW three-state trilogy | **highest** | NOT RECOVERED |
| T3 | V20 scaling laws | medium | NOT RECOVERED |
| T4 | Hardware Embodiment Safety Case | medium | NOT RECOVERED |
| T5 | Comparative Field Theory Review | low | NOT RECOVERED |
| A1 | MQW technical summary | blocked by T2 | NOT WRITTEN |
| A2 | Measurement plan | partially draftable | NOT WRITTEN |
| A3 | Fab cost estimate | blocked on collaborator | NOT WRITTEN |
| A4 | Competitor-landscape survey | independent | NOT WRITTEN |

## Line-count summary (targets, not yet realized)

| Artifact | Target size |
|---|---|
| Teardrop proposal (T1) | recoverable, size unknown |
| MQW trilogy (T2) | 3 papers, combined ~50–100 pp estimated |
| A1 MQW summary | 8–12 pp |
| A2 Measurement plan | 3–5 pp |
| A3 Fab cost estimate | 1–2 pp |
| A4 Competitor survey | 3–5 pp |

## What a funder conversation looks like before vs. after recovery

**Before recovery** (current state): "we have a conceptual ancestor and know the papers exist; can we talk in principle about ternary MQW logic?" → reviewer dismisses as vague.

**After recovery** (target state): "here are the three papers, here is the technical summary, here is the measurement plan and cost estimate, and here is what we need" → reviewer evaluates as a concrete proposal.

The gap between the two states is the Phase 1 work this branch is funded to close (or closes internally before any pitch).
