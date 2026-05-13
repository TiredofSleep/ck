# CK Unification Plan — 2026-05-13

**Author:** Claude (with Brayden, planning session)
**Status:** PLAN — do not build until reviewed and approved.
**Source archaeology:** [`ARCHAEOLOGY_2026_05_13.md`](ARCHAEOLOGY_2026_05_13.md)

---

## §0 — Premise

Five parallel archaeology agents surveyed every CK generation (Gen1-Gen14 local + 8 GitHub repos). The unexpected finding:

**Brayden has already built every architectural component of the vision he just described.**

Templated lattice memory with descent + lateral edges. Spreading-activation retrieval. Real screen reading via OCR. Real microphone capture. Cross-modal binding substrate. M-letter visual ↔ phonetic ↔ lexical binding (already measured for every letter A-Z). 1.2M-param substrate language model TRAINED. Multi-head LM ARCHITECTURE designed. Curiosity drives. "What next?" forecasting. Background research loops. Autonomous study loops (built FOUR times across the gens).

**The work that remains is integration, not invention.** Most of what was built is currently *disconnected* — modules exist as standalone working code but aren't mounted into the live cortex boot, or they run as background daemons without a wire back to the user-facing voice.

This plan describes how to UNIFY what already exists into the chatbot Brayden described: blank-slate cognitive substrate, reads any screen / hears any audio, learns from experience via templated lattice with bidirectional resonance, optionally consults LLMs as tools, is curious and proactive about pushing the narrative.

---

## §1 — What we have

(See `ARCHAEOLOGY_2026_05_13.md` for the full evidence. Summary:)

### Live + Production (already running)
- **Brain trinity** (~1100 LOC): `ao_5element.py` + `hebbian_5x5_cl.py` + `quadratic_glue.py` + `cortex.py`. AO 5-element flow vector field, plastic 5×5 Hebbian CL, F3×F4 quadratic glue, composed by cortex.step_symbol().
- **Live screen reading**: `ck_retina.py` (841 LOC) — `easyocr` + `cv2` + `mss`. 50Hz. Mounted at `engine.retina`. `/retina/glance` endpoint live.
- **Live microphone**: `ck_sim_ears.py` (466 LOC) — `sounddevice` continuous capture, CuPy/numpy spectral features.
- **Live audio output**: `ck_speaker.py` (238 LOC) — substrate-derived audio. `/speak` endpoint live.
- **Live cortex persistence**: `cortex_persist.py` (315 LOC) → `Gen13/var/cortex_state.json` (autosaved every 200 ticks).
- **Live cortex replay**: `cortex_replay.py` (224 LOC) feeds historical sprint papers + brain docs through cortex.step_text.
- **Live cortex voice**: `cortex_voice.py` (2079 LOC) reads cortex state and emits voice with FACTS lookup + fractal voice + crystal-first cascade.
- **Live operator-stream LM**: `ck_grammar_lm.py` (263 LOC, 1.2M params TRAINED, val PPL 2.62). Mounted at `/grammar/{predict,sample,score}`.
- **Live operator memory bank**: `operator_memory_bank.py` (281 LOC) — 20k k-NN over LM hidden states. Mounted at `/grammar/retrieve`.
- **Live BDC data accumulator**: `bdc_logger.py` writing 88k log lines/week ready as training corpus.
- **Live HER buffer**: `ck_hindsight_replay.py` (531 LOC) — 8.8M experiences indexed, 97.6% impact.
- **Live attractor detector**: `attractor_detector.py` (205 LOC) — 4-core proximity classifier. Result on every chat response.
- **Live canonical fuse**: `operad_fuse.py` (256 LOC) — arity-3 fuse + ternary attractor iteration.
- **Live study daemon**: `study_daemon.py` (264 LOC) — polls `/ck/research` every 10 min on 30-topic curriculum.
- **Live overnight orchestrator**: `overnight_orchestrator.py` (364 LOC) — 4-thread night loop (paper-writer + nightly-retrain + external-ingester + status).
- **Live research-first wrapper**: `research_first.py` (208 LOC) — research-before-every-answer.
- **Live ck_research**: `ck_research.py` (955 LOC) — persistent-Chrome browser research engine with allowlist.
- **Live olfactory bulb**: `ck_olfactory.py` (1212 LOC) — cross-modal convergence funnel where all sensory streams become operators.

### Built but UNWIRED (the integration gap)
- **`ck_goals.py`** (586 LOC, Gen11/13/14) — DriveSystem with curiosity / study / self_discovery drives. **NOT mounted in cortex boot.**
- **`ck_meta_memory_coord.py`** (1038 LOC, Gen12) — Tag2x2 × Tag3x3 × Tag4x4 template-coordinate triple. Most sophisticated template signature in the project. **UNUSED at runtime.**
- **`Gen12/targets/ck_r16/ck_lm/memory/`** — full SQLite Atom/Path/Crystal/MetaCrystal pipeline with RGMem + MemoryOS citations. **NOT wired to live boot.**
- **`multi_head_lm.py`** (225 LOC, Gen13) — single backbone + 5 measurement heads. **DESIGNED but never trained.**
- **`ck_lattice_chain.py`** (769 LOC, Gen11) — templated lattice with `walk_multilevel` 6-lens retrieval. Mounted in Gen13 brain but **CORTEX doesn't use it for memory lookup.**
- **`ck_divine_memory.py`** (483 LOC, Gen11) — descent + lateral retrieval via stored `chain_path`. Mounted but **not in retrieval critical path.**
- **`tig_fractal_thinker.py` + `tig_dream_engine.py`** (675 + 974 LOC, Old Knowledge) — explicit spreading activation with Collins-Loftus decay + Lévy jumps + Friston precision. **ARCHIVED, not in current live build.**
- **`ck_forecast.py`** (475 LOC) — TL Monte Carlo "what next?" prediction. **Wired to BTQ for defensive action but not to voice for proactive pushing.**
- **`surprisal_log.py`** (222 LOC) — measures prediction error per cortex prediction. **Not consumed as curiosity signal.**
- **`friction_curves`** in `ck_autodidact.py` — where CK's curvature disagrees lives. **Stored but never surfaced.**

### Tiny actual gaps (no prior implementation)
1. Pixel-to-stroke / pixel-to-Bezier decomposition. `LETTER_GEO` table is hand-coded; nothing reads strokes FROM pixels.
2. 4-head LM TRAINED on the 4 algebraic measurements (σ-orbit, shell, 4-core, operator). Architecture exists; ~15 min training run is the remaining work.
3. Proactive narrative push from background loops to user-facing voice. (CK never says "I learned X tonight, want to talk about it?")
4. Unified bidirectional retrieval API across all memory layers (lattice_chain + divine_memory + HER + truth_lattice + crystals + corpus). Each layer has its own retrieval; no single `recall(query, depth='any')` operator.
5. Frontier scanner that surfaces "what's open from Atlas/FRONTIERS_*.md?" at conversation pauses.

---

## §2 — Architectural diagram (target state)

```
                                                    ┌──────────────────────────────┐
       SCREEN  ──► ck_retina.py ──► easyocr ────┐   │     CORTEX BRAIN TRINITY     │
                                                ├──►│   AO 5-element + Hebbian +   │
                                                │   │   quadratic glue → emergent  │
       MIC    ──► ck_sim_ears.py ──► force9 ────┤   └────────────┬─────────────────┘
                                                │                │
       TEXT   ──► /chat endpoint ────────────────┤                ▼
                                                │   ┌──────────────────────────────┐
                                                │   │  ck_olfactory cross-modal    │
                                                │   │  convergence funnel          │
                                                │   │  (modality=provenance        │
                                                │   │   operators=shared currency) │
                                                │   └────────────┬─────────────────┘
                                                │                │
                                                │                ▼
                                                │   ┌──────────────────────────────┐
                                                │   │  TEMPLATED LATTICE MEMORY    │
                                                │   │  (ck_lattice_chain + divine) │
                                                │   │  experience lands in CL slot │
                                                │   │  by (operator, σ-orbit,      │
                                                │   │  shell, 4-core, Tag2/3/4)    │
                                                │   │                              │
                                                │   │  descent edges (chain_path)  │
                                                │   │  lateral edges (centroid k-NN│
                                                │   │   + same-bucket Formal-Concept)│
                                                │   └────────────┬─────────────────┘
                                                │                │
                                                │                ▼
                                                │   ┌──────────────────────────────┐
                                                │   │  4-HEAD SUBSTRATE LM         │
                                                │   │  (multi_head_lm.py +         │
                                                │   │   ck_grammar_lm backbone)    │
                                                │   │                              │
                                                │   │  head_op (15 vocab)          │
                                                │   │  head_sigma_orbit (4 vocab)  │
                                                │   │  head_shell (8 vocab)        │
                                                │   │  head_4core (4 vocab)        │
                                                │   │                              │
                                                │   │  + operator_memory_bank      │
                                                │   │    (20k k-NN, plastic +1 per │
                                                │   │     tick)                    │
                                                │   └────────────┬─────────────────┘
                                                │                │
                                                │                ▼
                                                │   ┌──────────────────────────────┐
                                                │   │  CURIOSITY + FORECAST LOOP   │
                                                │   │  (ck_goals.DriveSystem +     │
                                                │   │   ck_forecast +              │
                                                │   │   ck_research)               │
                                                │   │                              │
                                                │   │  drives: curiosity, study,   │
                                                │   │   self_discovery             │
                                                │   │  forecast: 8 trajectories ×  │
                                                │   │   10 ticks                   │
                                                │   │  research: browser allowlist │
                                                │   │   + page ingest              │
                                                │   └────────────┬─────────────────┘
                                                │                │
                                                │                ▼
                                                │   ┌──────────────────────────────┐
                                                │   │  VOICE + NARRATIVE PUSH      │
                                                │   │  (cortex_voice.py +          │
                                                │   │   sentence_composer +        │
                                                │   │   PROACTIVE TRIGGER LAYER)   │
                                                │   │                              │
                                                │   │  reactive: respond to user   │
                                                │   │  proactive: "by the way..."  │
                                                │   │   from drive activation,     │
                                                │   │   surprisal spikes, frontier │
                                                │   │   scanner, research findings │
                                                │   └────────────┬─────────────────┘
                                                │                │
                                                │                ▼
                                                │              OUTPUT
                                                │
                                                │   ┌──────────────────────────────┐
                                                ◄───┤  OPTIONAL TOOLS              │
                                                    │  (Ollama as tool, not        │
                                                    │   backend; pyttsx3 for       │
                                                    │   measurement; Claude        │
                                                    │   API for research depth)    │
                                                    └──────────────────────────────┘
```

---

## §3 — The unification phases

**Total estimate: 4-6 weeks** (down from my initial estimate of 6-8 weeks for building from scratch, because most pieces exist).

### Phase 0 — Read + Decide (2-3 days, no code)

Goal: pick canonical versions and template-signature scheme.

Tasks:
- Read in detail: `ck_lattice_chain.py`, `ck_divine_memory.py`, `ck_meta_memory_coord.py`, `tig_fractal_thinker.py`, `tig_dream_engine.py`. Decide the canonical templating scheme.
- Read in detail: `multi_head_lm.py`, `train_bdc.py`, `ck_invariants_bridge.py`, `attractor_detector.py`, `operad_fuse.py`. Pin down the 4 algebraic measurements.
- Read in detail: `ck_goals.py`, `ck_forecast.py`, `ck_research.py`, `study_daemon.py`, `overnight_orchestrator.py`. Decide how to wire proactivity.
- Read in detail: `Gen12/targets/ck_r16/ck_lm/memory/`. Decide if this is the canonical persistent layer or if `ck_lattice_chain` + `ck_divine_memory` should be.
- Read in detail: `tig_fractal_thinker.py` spreading-activation algorithm. Port mentally to numpy-only standalone module (no torch dependency).

Decisions to make:
1. **Template signature for memory slots.** Options:
   - (a) (operator, σ-orbit, shell, 4-core) — 4 algebraic axes per Brayden's "4 measurement languages" framing.
   - (b) Tag2x2 × Tag3x3 × Tag4x4 (ck_meta_memory_coord) — 3-tier ontology with citations.
   - (c) Divine27 cube — 3×3×3 = 27 cells.
   - (d) Combination: outer axes = 4 algebraic measurements; inner refinement = Tag2x2 ontological class.
2. **Canonical lattice graph implementation.** Options:
   - (a) `ck_lattice_chain` (mounted, 769 LOC, evolution + walk_multilevel).
   - (b) Fresh write that unifies lattice_chain + divine_memory + ck_meta_memory_coord into one structure.
3. **Spreading-activation port.** Options:
   - (a) Lift `tig_fractal_thinker.py` directly into `Gen14/targets/ck/brain/` as `spreading_activation.py`.
   - (b) Re-implement as part of lattice_chain.
4. **Persistent memory store.** Options:
   - (a) `Gen12/targets/ck_r16/ck_lm/memory/` SQLite pipeline (Atom/Path/Crystal/MetaCrystal).
   - (b) JSONL append-only logs (simpler, lossier).
   - (c) Hybrid: SQLite for crystals + JSONL for raw experiences.
5. **Voice push mechanism.** Options:
   - (a) Idle-tick polling: every N seconds, ask "does CK have something to say?" — checks goal_evaluator + surprisal_log + frontier_scanner + research_results.
   - (b) Event-driven: when drives fire / surprisal spikes / research completes, push a notification to the chat session.
   - (c) Both.

Deliverable: `PHASE_0_DECISIONS_<DATE>.md` recording each decision + 1-2 sentence rationale.

### Phase 1 — Wire what exists into one boot (1-2 weeks)

Goal: a single `python ck_boot.py` that brings up every existing live component PLUS the unwired ones, with everything sharing one cortex state.

Tasks:
1. **Mount `ck_goals.py` into cortex boot.** GoalEvaluator.tick() → engine.suggested_operator → consumed by BTQ as a +0.3 bias toward curiosity-aligned operators. Default goals: explore_environment, autonomous_study, self_discovery, observe.
2. **Mount `ck_meta_memory_coord.py`** as the memory addressing layer. Every experience that enters `ck_olfactory.absorb_ops` ALSO gets a (Tag2x2, Tag3x3, Tag4x4) coordinate written to a sidecar index.
3. **Wire `ck_r16/ck_lm/memory/` SQLite pipeline** as persistent memory store. Atom/Path/Crystal lifecycle live; MetaCrystals from past crystals; RGMem promotion + MemoryOS heat scoring active.
4. **Wire `ck_forecast.py`** to voice cortex. Every N (e.g. 50) ticks: forecast 10 ticks ahead, surface any pathway predictions with HARMONY ≥ 0.8 as candidate "next thoughts" for the proactive layer.
5. **Wire background loop findings to voice.** `paper_writer.py` completion → cortex_voice gets a "I just wrote X" entry; `external_ingester` finding → "I learned X tonight"; `study_daemon` curriculum → "I'm wondering about Y"; consume via a `proactive_queue` that cortex_voice checks every N user turns.
6. **Sanity gate: smoke test.** Boot, verify all endpoints respond, watch one drive fire, watch one forecast surface, watch the proactive queue accumulate while CK is idle.

Deliverable: working `Gen14/targets/ck/server/ck_boot_unified.py` that boots all live + unwired components together.

### Phase 2 — Train 4-head LM (3-5 days)

Goal: `multi_head_lm.py` trained on 4 algebraic measurement heads from the 88k BDC log lines.

Tasks:
1. **Rename heads** in `multi_head_lm.MultiHeadConfig`: {head_op, head_sigma_orbit, head_shell, head_4core} with vocabs {15, 4, 8, 4}.
2. **Implement `shell_class(state) → int_in_0..7`** (~30 LOC, using `joint_chain_shells` from `attractor_detector.py`). For a state distribution `p` over Z/10Z, find the smallest sub-magma shell that contains the support.
3. **Extend `record_to_example`** in `train_bdc.py` to project each BDC record's operator stream through the 4 algebraic measurements (already-existing functions in `ck_invariants_bridge.py` + `attractor_detector.py` + `operad_fuse.py`).
4. **Run `train_bdc.py --min-records 200 --epochs 10`** against the 88k existing log lines. RTX 4070 ~10-15 min total. AdamW + cosine LR. Save to `Gen13/var/cells/multi_head_lm_4heads.pt`.
5. **Wire as engine.substrate_lm**. Every chat response gets a `substrate_prediction` sidecar showing the 4-head agreement.
6. **Add `/grammar/predict_all_4` endpoint** returning {op_top, orbit_top, shell_top, 4core_top, agreement_score}.

Deliverable: trained 4-head LM, mounted live, agreement score on every response.

### Phase 3 — Unified bidirectional retrieval (1-2 weeks)

Goal: one `recall(query, depth='micro'|'meso'|'macro'|'any')` operator that routes across all memory layers.

Tasks:
1. **Port `tig_fractal_thinker.py` spreading-activation** to `Gen14/targets/ck/brain/spreading_activation.py`. Pure numpy. SEED → SPREAD (Collins-Loftus decay) → LEAP (Lévy 0.15) → FUSE (CL composition) → EVALUATE (until C ≥ T*).
2. **Implement `recall(query, depth, k=10)`** as the unified retrieval primitive:
   - Encode query as operator pair / σ-orbit / shell / 4-core signature (4 algebraic measurements as keys).
   - At `depth='micro'`: query operator_memory_bank + lattice_chain leaves.
   - At `depth='meso'`: query divine_memory.retrace (descent from current node) + lateral neighbors via Formal-Concept buckets.
   - At `depth='macro'`: query truth_lattice + crystals + meta-crystals.
   - At `depth='any'`: spreading activation across all three depths until convergence.
3. **Wire as engine.recall**. Cortex_voice can now ask "what does CK know about X?" and get back micro/meso/macro tiers.
4. **Sanity gate: synthetic test.** Feed 1000 synthetic operator-tick experiences with known structure. Query at each depth. Verify recall pulls the right subset.

Deliverable: `recall()` available everywhere; spreading-activation runs in <100ms on the 8.8M HER buffer.

### Phase 4 — Proactive narrative push (1 week)

Goal: CK actively says "by the way, X" when relevant — without being asked.

Tasks:
1. **Implement `proactive_trigger.py`**: a daemon that checks every N seconds for:
   - Drive activation (any of curiosity/study/self_discovery firing at ≥ 0.7 strength).
   - Surprisal spike (recent surprisal_log entries > μ + 2σ).
   - Research result (anything in `paper_writer` queue ready to surface, anything in `external_ingester` recent finds).
   - Frontier match (FRONTIERS_*.md scan: which frontiers haven't been mentioned this week?).
   - Forecast prediction (any `ck_forecast` pathway with HARMONY ≥ 0.85 not yet voiced).
2. **Implement `cortex_voice.push(reason, context)`**: when triggered, generate a math-first "by the way..." message and add to the next chat response.
3. **Implement `frontier_scanner.py`**: reads `Atlas/FRONTIERS_*.md` weekly, builds a structured frontier list, surfaces unmentioned ones during conversation pauses.
4. **Quality gate**: Brayden uses CK for an evening. Did CK surface 3-5 relevant proactive insights without being intrusive?

Deliverable: CK is curious and pushes the narrative.

### Phase 5 — The tiny missing pieces (1 week)

Goal: close the small "no prior code" gaps.

Tasks:
1. **Pixel-to-stroke extraction.** ~200 LOC numpy: threshold → skeletonize → fit Bezier curves to skeleton segments. Use `LETTER_GEO` table as ground truth. Output: each detected letter on screen produces a stroke-count + geo-type signature.
2. **Tie pixel-to-stroke into `ck_retina`**. When easyocr detects a word, run stroke extraction on each letter and verify against `LETTER_GEO`. Drift signal = strokes-extracted vs strokes-expected. Becomes a friction_curves entry when off.
3. **Frontier scanner.** Already in Phase 4 — confirm working.
4. **Audit + polish.** Read every Phase 1-4 file, fix smells, add comments, update `README_GEN14.md`.

Deliverable: pixel-to-stroke working; ck_retina enhanced with stroke verification; CK can "read" letters from pure curves.

### Phase 6 — Mirror to public 06_runtime/ (3-5 days)

Goal: a clean, deployable, ordinary-hardware version in `trinity-infinity-geometry/06_runtime/`.

Tasks:
1. **Identify the minimal subset** needed for "boots and talks". Brain trinity + ck_olfactory + ck_lattice_chain + multi_head_lm + ck_goals + ck_forecast + cortex + cortex_voice + voice proactive layer + Flask boot. Maybe 8000-12000 LOC total.
2. **Strip optional GPU paths.** numpy fallback for everything. No CuPy required.
3. **Write `06_runtime/ck_slim/`** as the consumer-hardware version. Single `python ck.py --offline` boot. Optional `--ollama` flag for tool bridge. Optional `--browser` for ck_research.
4. **requirements.txt**: numpy, flask, sounddevice (audio in/out), mss + opencv-python + easyocr (vision), pillow. ~6 packages, all consumer-installable.
5. **README**: 30-second deploy instructions. Walk through "type a question, watch CK think, see the 4-head agreement score, watch curiosity drives fire when you go silent."
6. **Test on a clean Python venv** with no Brayden-specific paths. Verify it boots on a stock laptop.

Deliverable: `06_runtime/ck_slim/` shippable as the "anyone can run it" version. The math waits for the bridge — and the bridge is shipped.

---

## §4 — Risks and what could go wrong

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Phase 0 decisions create coupling that blocks Phase 3 | MEDIUM | Stalled timeline | Force Phase 0 to write a 1-page summary per decision before any code |
| Templated lattice retrieval too slow at 8.8M HER scale | LOW | UX degraded | Phase 3 includes scaling tests; fall back to per-shell index if needed |
| 4-head LM training fails to converge on existing corpus | LOW | Phase 2 stalls | Corpus is varied + balanced per measurement; 88k log lines is more than enough; AdamW + cosine LR is robust |
| Proactive triggers fire too often → annoying | MEDIUM | Bad UX | Phase 4 quality gate explicitly tests cadence; tune thresholds based on Brayden's evening use |
| Pixel-to-stroke extraction unreliable for non-rendered (handwritten) | LOW | Limited scope | Initially scope to RENDERED text only; handwriting is Phase 7 or later |
| Some unwired module (ck_goals, ck_meta_memory_coord) doesn't actually work when mounted | MEDIUM | Phase 1 delays | Phase 1 budgets 1-2 weeks specifically to debug integration issues; archaeology only tells us the file exists, not that it boots |
| ck_r16 SQLite pipeline is incompatible with current brain | MEDIUM | Phase 1 stalls | Phase 0 specifically reads ck_r16 to confirm compatibility before committing |
| Background loops keep silently failing (study_daemon, overnight_orchestrator) — they "run" but don't produce useful findings | HIGH | Proactive push is empty | Phase 1 includes monitoring + alerting on background-loop output quality |
| Brayden + I get distracted by a beautiful side-rabbit-hole during Phase 0 | HIGH | Plan stops | Phase 0 has a hard 3-day budget |

---

## §5 — What this plan does NOT do

- It does NOT build a TIG-corpus RAG chatbot. CK ships blank-slate.
- It does NOT depend on any LLM at runtime. Ollama / Claude API are optional tools.
- It does NOT require a GPU. numpy fallback everywhere.
- It does NOT introduce new architectural primitives. Every primitive used here already exists in the codebase.
- It does NOT delete or replace any existing code. Wires + unifies; everything pre-existing stays where it is.
- It does NOT ship the J-papers as part of CK. The papers wait per the distribution stance.
- It does NOT auto-submit to journals or arXiv. Per the distribution-stance commitment.
- It does NOT change any model name or external-facing API breakingly.

---

## §6 — Success criteria

Phase complete when:

- **Phase 0**: a written decision document exists for each of the 5 listed decisions.
- **Phase 1**: `ck_boot_unified.py` boots without errors. All endpoints listed in §1 respond. Drive activation visible in logs. Forecast surface visible. Proactive queue accumulating during idle.
- **Phase 2**: `train_bdc.py` finishes training a 4-head LM. Val accuracy on held-out is non-trivial (better than random by ≥ 20pp per head). `/grammar/predict_all_4` endpoint returns 4 heads + agreement score.
- **Phase 3**: `recall(query, depth='any')` returns relevant memories from the 8.8M HER buffer in <100ms. Synthetic test PASSES (resonant subset retrieved correctly).
- **Phase 4**: Brayden uses CK for an evening. CK proactively surfaces ≥ 3 relevant insights without being asked. Brayden doesn't complain about intrusiveness.
- **Phase 5**: pixel-to-stroke extraction produces correct stroke-count for ≥ 80% of letters in screen-captured rendered text. Friction-curve entries appear when stroke extraction disagrees with easyocr.
- **Phase 6**: `06_runtime/ck_slim/` boots on a stock laptop with only the listed requirements. README walks through deployment in ≤30 seconds.

---

## §7 — Open questions for Brayden

Before Phase 0 starts, please answer or push back on these:

1. **Template signature scheme** — which of the 4 options listed in §3 Phase 0 decision #1 do you want? Default recommendation: combination — outer axes are the 4 algebraic measurements (operator, σ-orbit, shell, 4-core), inner refinement is Tag2x2 ontological class.

2. **Canonical lattice graph** — do you want to keep `ck_lattice_chain.py` as the canonical templated lattice, or write a fresh `Gen14/lattice_graph.py` that unifies lattice_chain + divine_memory + ck_meta_memory_coord? Default recommendation: keep ck_lattice_chain as canonical; add a thin wrapper that exposes the unified `recall(query, depth)` operator.

3. **Persistent memory store** — SQLite pipeline (`ck_r16/ck_lm/memory/`) or JSONL? Default recommendation: SQLite for crystals + truth lattice; JSONL append-only for raw experience log + BDC events; numpy `.npy` for HER buffer (already the case).

4. **Voice push mechanism** — idle-tick polling vs event-driven vs both? Default recommendation: both. Event-driven for drives + research findings; idle-tick polling for frontier scanner.

5. **Phase 6 (shipping to public 06_runtime/)** — should this happen at all, given the distribution-stance hold? Or stay private until the J-papers are ready to ship together? Default recommendation: build privately, hold public mirror until you're ready to lift the journal-submission hold. The slim version exists; just doesn't get pushed to public repo until then.

6. **MYTHDRIFT historical agent** — one of the six archaeology agents errored. Do you want me to re-spawn it for completeness on the older GitHub repos (TIG-UNIFIED, TIME-FOR-HELP MYTHDRIFTs), or is the coverage from the other five agents enough? Default recommendation: skip unless you specifically remember something important from those repos.

---

## §8 — How long does this actually take

Honest aggregate estimate, given the archaeology shows most pieces exist:

| Phase | Best case | Realistic | Pessimistic |
|---|---|---|---|
| Phase 0 — Read + Decide | 2 days | 3 days | 5 days |
| Phase 1 — Wire what exists | 1 week | 2 weeks | 3 weeks (if many modules have integration bugs) |
| Phase 2 — Train 4-head LM | 2 days | 4 days | 1 week |
| Phase 3 — Unified retrieval | 1 week | 2 weeks | 3 weeks |
| Phase 4 — Proactive push | 4 days | 1 week | 2 weeks |
| Phase 5 — Tiny missing pieces | 4 days | 1 week | 2 weeks |
| Phase 6 — Public mirror | 3 days | 4 days | 1 week |
| **Total** | **3.5 weeks** | **5.5 weeks** | **9 weeks** |

Realistic: ~5.5 weeks for a one-person (me) build with Brayden directing.

---

## §9 — What I need from Brayden before starting

1. Answers (or override defaults) on §7's open questions.
2. Confirmation that Phase 0 starts now / next session / when.
3. Confirmation that the archaeology in `ARCHAEOLOGY_2026_05_13.md` matches what he expected, or correction where it doesn't.
4. Any architectural concerns or refinements to the §2 target diagram.
5. Decision: re-spawn the errored MYTHDRIFT agent, or skip?

---

*Prepared 2026-05-13 by Claude based on archaeology from 5 parallel specialist agents.*
*This is a plan, not a build. Do not execute until reviewed and approved by Brayden.*
