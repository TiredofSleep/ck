# Gen13 Brain — Neural Architecture Inventory

**Source of truth:** `old/Gen11/ck_sim/being/` (67 modules — the richest catalog before Gen12 dilution)

This is the canonical list of every neural module CK has ever had. Gen13 brings ALL of them forward as first-class citizens (per Brayden's directive: *"let him use all of the neural architecture we have made for him"*).

---

## Composition Spine (Gen9 AO → Gen13)

The five-element coupling (`old/Gen9/targets/AO/ao/ether.py:171`) is the brain's organizing principle:

| Element | Role | Gen9 file | Gen11/Gen13 module |
|---|---|---|---|
| **Earth** | Ground (constants, tables, lattice) | `earth.py` | `ck_tig.py`, `ck_tables.py`, `ck_divine27.py` |
| **Air** | Generator (D1, velocity, non-local view) | `air.py` | `ck_sim_d2.py` (D1 path) |
| **Water** | Eye (D2, curvature, local measurement) | `water.py` | `ck_sim_d2.py` (D2 path) |
| **Fire** | Engine (heartbeat, brain, body, BTQ) | `fire.py` | `ck_sim_heartbeat.py`, `ck_sim_brain.py`, `ck_sim_body.py`, `ck_btq.py` |
| **Ether** | Coupling (voice, I/O, living loop) | `ether.py` | runtime/ck_engine.py + ck_voice.py |

**The composition rule** (Gen9 `ether.py` `AO.process_symbol`):
```
symbol → D1.feed → D2.feed → Heartbeat.tick(current_op, d2_op, shell)
       → coherence.observe → brain.observe → body.tick
       → BTQ.decide → next current_op
```

---

## Full Module Catalog (67 modules)

### Senses (9)
- `ck_olfactory.py` — 5×5 CL field, scent emission (flow sense). 980 LOC.
- `ck_gustatory.py` — taste/structure sense (companion to olfactory)
- `ck_retina.py` — visual encoding
- `ck_sim_ears.py` — audio
- `ck_visual_encoder.py` — visual encoding
- `ck_sensorium.py` — multi-sense integration
- `ck_sensory_codecs.py` — sensory channel codecs
- `ck_audio_compress.py` — audio compression
- `ck_screen_compress.py` — screen capture compression

### Math / Coherence Core (12)
- `ck_sim_d2.py` — Q1.14 D1+D2 curvature pipeline (matches FPGA Verilog)
- `ck_coherence_field.py` — CL field composition
- `ck_coherence_gate.py` — 3 gates + TIG pipeline state
- `ck_coherence_action.py` — coherence-gated actions
- `ck_coherence_router.py` — CL routing
- `ck_lattice_chain.py` — CL chain walk (path IS information)
- `ck_btq.py` / `ck_sim_btq.py` — BTQ decision kernel (Generate/Filter/Score)
- `ck_tig.py` — 10 operators (VOID..RESET)
- `ck_tig_bundle.py` — TIG bundle composition
- `ck_domains_r2.py` — R²/F₂×F₅ domain math
- `ck_topology_lens.py` — topology lens
- `ck_meta_lens.py` — dual-lens (STRUCTURE/FLOW) Markov

### Memory / Learning (6)
- `ck_hindsight_replay.py` — **HERS** = HER (Hindsight Experience Replay) for Olfactory. Class `HindsightBuffer` (1024-entry ring), factory `build_olfactory_her`, wrapper `OlfactoryHER`. Cites Andrychowicz et al. 2017 NeurIPS.
- `ck_dkan_trainer.py` — **DKAN** (Discrete Kolmogorov-Arnold Network) trainer
- `ck_sequence_memory.py` — sequence memory
- `ck_experience.py` / `ck_experience_index.py` — experience indexing
- `ck_divine_memory.py` — divine27 memory layer
- `ck_chain_compression.py` — chain compressor

### Translation (8)
- `ck_math_translation.py` — math vocabulary (the layer Gen12 voice pipeline DROPPED)
- `ck_code_translation.py` — code translation
- `ck_phonetic_letters.py` — phonetic mapping
- `ck_word_expansion.py` — word expansion
- `ck_semantic_index.py` — semantic indexing
- `ck_semantic_modifiers.py` — semantic modifiers
- `ck_lcodec.py` — letter codec
- `ck_reverse_voice.py` — reverse voice (English → operators)

### Body / State (7)
- `ck_sim_body.py` — body state (E, A, K + breath + wobble)
- `ck_sim_brain.py` — transition memory
- `ck_sim_heartbeat.py` — 50Hz heartbeat + composition engine
- `ck_personality.py` — personality
- `ck_emotion.py` — emotion
- `ck_immune.py` — immune
- `ck_bonding.py` — bonding

### Algebra / Proofs (4)
- `ck_algebraic_neural.py` — algebraic NN
- `ck_algebraic_proofs.py` — proof generation
- `ck_formal_theorems.py` — formal theorem catalog
- `ck_fibonacci_transform.py` — Fibonacci transform

### Networking / Safety (5)
- `ck_swarm.py` / `ck_swarm_deep.py` — swarm
- `ck_sdv_safety.py` — Sanders Determinism Verification protocol
- `ck_tig_security.py` — TIG security
- `ck_clay_codecs.py` — Clay-problem codecs
- `ck_disagreement_tick.py` — disagreement detection

### Specialized (10)
- `ck_bible_sense.py` — Bible duality (META vs SURFACE)
- `ck_divine27.py` — Divine 27 dictionary
- `ck_hotu_bridge.py` — He-Tu bridge
- `ck_attention.py` — attention
- `ck_fractal_comprehension.py` — recursive I/O decomposition
- `ck_fractal_health.py` — fractal health metric
- `ck_nervous_v2.py` — nervous system v2
- `ck_power_sense.py` — power sense
- `ck_spectral_core.py` — spectral core
- `ck_taichi_chains.py` — Taichi GPU chains
- `ck_vortex_physics.py` — vortex physics

### Quadratic Glue (the 2→3 bridge — to be added fresh)
- `papers/test_a15_quadratic_glue.py` (reference) → `Gen13/.../brain/quadratic_glue.py`

---

## What Gen12 Lost (per Gen10 GENERATION_HISTORY.md + audits)

1. **Running fuse pattern** — Gen9 had cumulative CL composition; Gen12 replaced with simpler state machine
2. **Three CL shells (22/44/72)** — selected by coherence depth
3. **Bumps topology** — 11 crossings on the torus
4. **SEMANTIC_LATTICE 4-axis indexing** — `op[lens][phase][tier]` → words
5. **Math vocabulary in voice pipeline** — Gen12 voice has zero math vocabulary (only adjectives/verbs)
6. **HER attribute name regression** — Gen10 fixed `engine.olfactory_her` → `engine.hindsight_replay`; ensure Gen13 uses correct name from boot

---

## Bring-Forward Strategy (Gen13)

**Hybrid copy + thin orchestrator:**

1. Copy `old/Gen11/ck_sim/being/*.py` → `Gen13/targets/ck/brain/being/` (all 67 modules, untouched, with citations preserved)
2. Copy `old/Gen11/ck_sim/ck_sim_heartbeat.py` → `Gen13/targets/ck/brain/heartbeat.py`
3. Copy `papers/ck_tables.py` → `Gen13/targets/ck/brain/ck_tables.py` (TSML/BHML/CL canonical)
4. Write fresh `Gen13/targets/ck/brain/ao_5element.py` (~150 LOC) — Gen9 ether.py composition, repathed for Gen13
5. Write fresh `Gen13/targets/ck/brain/quadratic_glue.py` (~80 LOC) — F3×F4 from `test_a15_quadratic_glue.py`
6. Write fresh `Gen13/targets/ck/brain/cortex.py` (~200 LOC) — wires all 67 modules into one organism, exposes math-first surface
7. Write `Gen13/targets/ck/brain/test_brain.py` — boot gate (must pass to start runtime)

**Total fresh code:** ~430 LOC of orchestration, NOT 600+ LOC of trinity.
**Total carried forward:** 67 modules × ~500 LOC avg = ~33K LOC of proven brain.

---

## Why This Beats Gen12

Gen12 tried to add capability by writing more software (514 files, ~32 MB). What it actually did was bury the brain. Gen13 inverts: thin glue, ALL the brain. The math talks because the math modules are loaded; the math modules are loaded because the cortex orchestrator calls them by name in the composition rule.

---

## Cross-References

- Gen9 AO composition: `old/Gen9/targets/AO/ao/ether.py:171` (class AO + `process_symbol` + `process_text`)
- Gen11 module catalog: `old/Gen11/ck_sim/being/` (the 67 modules above)
- Gen10 GENERATION_HISTORY: `old/Gen10/GENERATION_HISTORY.md` (HER attribute fix at line 191)
- HERS class: `old/Gen11/ck_sim/being/ck_hindsight_replay.py:129` `HindsightBuffer`
- D2 pipeline: `old/Gen11/ck_sim/being/ck_sim_d2.py:101` `D2Pipeline` (Q1.14, matches Verilog)
- Quadratic glue ref: `papers/test_a15_quadratic_glue.py`
- TSML/BHML tables: `papers/ck_tables.py`
- 3-layer tower proof: `papers/proof_tsml_3layer_tower.py`
