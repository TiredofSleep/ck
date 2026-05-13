# Phase 0 — Architectural Decisions

**Date:** 2026-05-13
**Authority:** Brayden granted full agency ("proceed with the build as you see fit, hold nothing back, this is research")
**Decisions use defaults from CK_UNIFICATION_PLAN_2026_05_13.md §7.**

---

## Decision 1 — Template signature for memory slots

**Choice:** Combination scheme.

Outer axes (the 4 algebraic measurements, derivable from any (b, d) operator pair):
- `operator` ∈ Z/10Z — the raw next-operator value
- `sigma_orbit` ∈ {0: V, 1: F-cycle (1,7,9,3), 2: cycle (2,8,6,4), 3: BAL-fixed (5)} — the σ-orbit class
- `shell` ∈ {0..7} — which joint-closed sub-magma shell (sizes {1, 4, 5, 6, 7, 8, 9, 10})
- `four_core` ∈ {V=0, H=7, Br=8, R=9, outside=4} — 4-core proximity

Inner refinement (Tag2x2 from `ck_meta_memory_coord.py`):
- `tag_2x2` ∈ {INTERNAL_STRUCTURE, INTERNAL_CONTENT, EXTERNAL_STRUCTURE, EXTERNAL_CONTENT}

**Address:** `(operator, sigma_orbit, shell, four_core, tag_2x2)` → 10 × 4 × 8 × 5 × 4 = 6400 distinct cells.

**Rationale:** algebraic measurements give CK substrate-fluency at retrieval time; Tag2x2 inner refinement keeps the privacy/ontology axis the ck_meta_memory_coord literature pointed at; total cell count (6400) is small enough for fast spreading-activation and large enough to capture meaningful variation. Tag3x3 and Tag4x4 are deferred until needed.

---

## Decision 2 — Canonical lattice graph implementation

**Choice:** Keep `ck_lattice_chain.py` as the canonical evolving lattice; add a thin wrapper that exposes the unified `recall(query, depth)` operator.

**Rationale:** `ck_lattice_chain` already works (769 LOC, mounted in Gen13 brain, `walk_multilevel` already returns 6 simultaneous lenses). It evolves via observation, persists, has descent edges via stored chain_path. Re-writing it would lose those guarantees. The wrapper adds the unified `recall()` operator that routes across `lattice_chain` + `divine_memory` + `HER` + `truth_lattice` + `crystals` — making them composable without re-implementing any of them.

---

## Decision 3 — Persistent memory store

**Choice:** Hybrid.

- **Crystals + truth lattice** → SQLite via `Gen12/targets/ck_r16/ck_lm/memory/crystal_store.py` (already built; RGMem + MemoryOS scoring).
- **Raw experience log + BDC events** → JSONL append-only (`Gen13/var/bdc_logs/`, already running).
- **HER buffer** → numpy `.npy` (already the case).
- **Cortex Hebbian W** → JSON snapshot via `cortex_persist.py` (already running).
- **Lattice chain nodes** → mounted in-memory + serialized via existing `ck_lattice_chain.persist()`.

**Rationale:** every storage layer has its own format already working. Don't refactor; just connect them through the unified `recall()` operator. SQLite gives ACID for crystals (the canonical-facts layer); JSONL gives append-only durability for raw experience (where the volume is); numpy gives speed for HER (where retrieval is hot).

---

## Decision 4 — Voice-push mechanism

**Choice:** Both — event-driven for drives + research findings; idle-tick polling for frontier scanner.

- Event-driven triggers (fire immediately when condition met):
  - Drive activation: any of curiosity/study/self_discovery firing at strength ≥ 0.7
  - Surprisal spike: recent surprisal_log entry > μ + 2σ
  - Research result ready: `paper_writer` or `external_ingester` completes a useful finding
  - Forecast pathway with HARMONY ≥ 0.85 not yet voiced
- Idle-tick polling (fires every N seconds when no recent user activity):
  - Frontier scanner: walk `Atlas/FRONTIERS_*.md`, surface unmentioned frontier related to recent topic
  - Cortex history reflection: "I've been thinking about X recently"

**Rationale:** event-driven gives responsiveness; idle-poll gives presence. The combined approach lets CK feel proactive without being intrusive — events fire when something genuinely happens; idle-poll fills the silence with curiosity.

Both gated by a per-session cadence limiter (max 1 proactive push every 60 seconds) to prevent spamming.

---

## Decision 5 — Phase 6 (public 06_runtime/ ship)

**Choice:** Build privately, hold public mirror per distribution stance.

**Rationale:** the distribution stance in the public TIG repo says journal/arXiv amplification is on hold until CK ships in a form ordinary people can deploy. Internal build proceeds; the slim public version waits in the queue until CK is actually working and Brayden confirms ready-to-ship. When the time comes, Phase 6 is a 3-5 day pruning + repackaging pass.

---

## Decision 6 — MYTHDRIFT historical agent (errored)

**Choice:** Skip.

**Rationale:** the other five agents picked up the most relevant historical material (TIGCodexEngine from Dual-Lattice, Word-Math from Crystals, the React quadratic core from Crystal-Lattice-Matrix). The remaining unsurveyed repos (`TIG-UNIFIED-THEORY-MYTHDRIFT [2/6]`, `TIME-FOR-HELP-MYTHDRIFT [5/6]`) are most likely to contain early whitepaper drafts and engine iterations that have since been superseded. If something specific from those repos becomes relevant during the build, we'll fetch it then.

---

## Implementation order (for Phase 1+)

1. **Today (session 1):**
   - Survey `Gen14/targets/ck/` current state
   - Write `ck_boot_unified.py` — single entry point that mounts all live + unwired modules
   - Mount `ck_goals.py` DriveSystem
   - Mount `ck_lattice_chain` + `ck_divine_memory` for memory writes/retrievals
   - Mount `ck_forecast.py` for proactive what-next surfacing
   - Smoke test boot
   - Document progress

2. **Session 2:**
   - Implement `recall(query, depth)` unified retrieval operator
   - Connect background-loop findings to `proactive_queue`
   - Wire `ck_meta_memory_coord.py` Tag2x2 addressing layer

3. **Session 3:**
   - Train the 4-head LM (Phase 2)
   - Mount `multi_head_lm.py` 4-head substrate fluency

4. **Session 4:**
   - Build `proactive_trigger.py` (Phase 4)
   - Build `frontier_scanner.py`
   - Quality gate with Brayden

5. **Session 5+:**
   - Phase 5 tiny pieces (pixel-to-stroke, refinements)
   - Phase 6 public mirror (when Brayden says go)

**Commitment for this session:** items in (1) — get the unified boot existing and booting, even if some components are stubbed.
