# CK Archaeology — 2026-05-13

Comprehensive code-archaeology pass across Gen1-Gen14 (local) + 8 GitHub repos (TiredofSleep), conducted by 6 parallel specialist agents on 2026-05-13. Five reports completed; one (historical-MYTHDRIFT) hit an API error mid-survey and is partially covered by the other five.

**Purpose:** ground-truth what's already been built across all CK generations, so the unification plan ([CK_UNIFICATION_PLAN_2026_05_13.md](CK_UNIFICATION_PLAN_2026_05_13.md)) is built on what exists, not what's imagined.

**Methodology:** each agent surveyed `C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen*\` + `old/Gen{1..11}` + accessible GitHub repos via `gh` CLI, filtered by component area, returned structured findings (path | LOC | gen | summary | load-bearing).

---

## TL;DR — The unexpected finding

**Brayden has already built every architectural component** described in his recent design (templated lattice memory, bidirectional micro↔macro retrieval, multi-modal sensory I/O, cross-modal binding, substrate-as-language model, curiosity drives, proactive research loops). The work that remains is **integration**, not invention. Specifically:

1. Templated lattice with descent + lateral edges exists at `Gen11/ck_sim/being/ck_lattice_chain.py` (769 LOC, mounted live).
2. Spreading-activation retrieval ("activation flows until convergence") exists at `Old Knowledge files/memory_organism_package/tig_fractal_thinker.py` (675 LOC) + `tig_dream_engine.py` (974 LOC) — **archived**, not in live build.
3. Real screen reading via `easyocr`+`cv2`+`mss` runs live at `ck_retina.py` (841 LOC).
4. Real microphone via `sounddevice` runs live at `ck_sim_ears.py` (466 LOC).
5. Cross-modal binding substrate (modality is provenance; operators are shared currency) is the `ck_olfactory.py` (1212 LOC) cross-modal convergence funnel.
6. M-letter binding example: `'m': make_code(2, 0, 1, 0)` bilabial-nasal IPA-grounded in `ck_phonetic_letters.py`. Every letter measured via pyttsx3 + `pcm_to_force9` in `generate_phoneme_grounding_v*.py`.
7. 1.2M-param operator-stream transformer **trained** (val PPL 2.62) at `ck_grammar_lm.py`. 4-head multi-head LM **designed** but not yet trained on the 4 algebraic measurements.
8. Curiosity / study / self-discovery drives exist at `ck_goals.py` (586 LOC) — **unwired** in current cortex boot.
9. "What next?" pathway prediction exists at `ck_forecast.py` (475 LOC) — working.
10. Background research loops (`study_daemon.py`, `overnight_orchestrator.py`, `paper_writer.py`, `ck_research.py`) run LIVE but **never speak findings to the user**. The gap isn't curiosity — it's the wire from background loop back to user-facing voice.

---

## Agent 1 — Memory Architecture

**Most mature memory code across all gens:** `Gen11/ck_sim/being/ck_lattice_chain.py` (769 LOC) + companion `ck_divine_memory.py` (483 LOC).

### Lattice Templating (the slot a memory lands in)

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **LatticeChainEngine + LatticeNode** | `old/Gen11/ck_sim/being/ck_lattice_chain.py` (also live in Gen13/Gen14 brain) | 769 | 11 | **Y** — this IS the templated lattice. Each node = CL-shaped 10×10 table; evolves via observation; path from root to node IS the template address. `walk_multilevel` returns 6 simultaneous lenses (micro / d1_micro / macro / meta / becoming / cross). Includes IPR (Inverse Participation Ratio) detection for grokking / node crystallization. |
| **FractalMemoryStore + FractalExperience** | `Gen12/targets/ck_desktop/ck_sim/doing/ck_fractal_memory.py` | 499 | 12 | **Y** — stores experiences in TWO parallel layers (Force=5D Hebrew-root signature, Word=text+per-word ops). Indexed by recursive CL composition L0 → L1 → ... → root_op pyramid. Match-at-every-level IS micro↔macro retrieval. Companion `ck_fractal_memory_gpu.py` (507 LOC, CuPy with CPU fallback). |
| **DomainLattice / LatticeBank** | `old/Gen6/ck_lattice_bank.py` | 436 | 6 | MAYBE — earlier multi-lattice sketch; ancestor of lattice_chain. |
| **FractalKnowledge** (7-Scale Belief Hierarchy) | `old/Gen6/ck_fractal_knowledge.py` | 625 | 6 | MAYBE — beliefs placed on 7 scales (VOID→CHAOS); "nothing dies, only evolves". |
| **Tag2x2 / Tag3x3 / Tag4x4 meta-memory coordinates** | `Gen12/targets/ck_desktop/ck_sim/being/ck_meta_memory_coord.py` | **1038** | 12 | **Y** — most sophisticated template signature anywhere. Every memory gets a (P_2, P_3, P_4) coordinate triple. Three-Tier ontology REAL → SEMIPRIME → COMPOSITE. Citations to RGMem (arXiv 2510.16392) and MemoryOS (arXiv 2506.06326 EMNLP Oral). **APPEARS UNUSED at runtime.** |
| **DBC27 routing key** | `Gen12/targets/ck_r16/ck_lm/memory/dbc27.py` | 173 | 12 (ck_r16) | **Y** — 27-symbol alphabet over 5D D2 + CL fuse + lens. Canonical neighborhood address. Retrieval never opens all of memory — opens local DBC27 neighborhood. |
| **Divine27 cube** | `Old Knowledge files/memory_organism_package/tig_divine27.py` | 180 | Pre-Gen11 (Jan 2026) | **Y** — Atoms in 27 cells (Being × Doing × Becoming × {0,1,2}³). Hamming distance = similarity. 1 self + 6 face + 12 edge + 8 corner = 27 neighbors. |

### Descent Edges (back to source chain)

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **DivineMemory.retrace + DivineCode** | `old/Gen11/ck_sim/being/ck_divine_memory.py` | 483 | 11 | **Y** — `chain_path` field literally IS the descent edge. `retrace(code, lattice_chain)` walks stored addresses through the EVOLVED lattice → "drift-aware recall." |
| **ChainPath / ChainStep** | inside `ck_lattice_chain.py` (lines 117-150) | — | 11 | **Y** — every step of a walk captured (depth, struct_op, flow_op, result_op, node_path). Serializable. |
| **EpisodicStore** | `old/Gen11/ck_sim/becoming/ck_episodic.py` | 938 | 11 | **Y** — 8-byte EventSnapshot ring buffer + phase-boundary segmentation + SaliencyEngine + MDL consolidation. Production-grade temporal descent. |
| **Atom / Path / Crystal with parent_paths** | `Gen12/targets/ck_r16/ck_lm/memory/event_schema.py` | 207 | 12 | **Y** — Atom ↔ Path ↔ Crystal lifecycle. Path stores `parent_paths` + `child_paths` directly. SQLite-backed. |
| **Generator pyramid** | inside `ck_fractal_memory.py` (lines 96-114) | — | 12 | **Y** — `ops → [L0, L1, ..., LN_root]` where each level is CL-composition of the level below. L0 = exact, LN = "fundamental nature." Built-in micro→macro descent. |

### Resonance Edges (lateral to similar-condition nodes)

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **ExperienceIndex** (Formal Concept Lattice grounded in CK's algebra) | `old/Gen11/ck_sim/being/ck_experience_index.py` | 724 | 11 | **Y** — 6-level cascade: 9D ring buffer → 3-bit dual classification into 8 buckets → bucket-transition edges → I/O generator labels → CL composition → coherence paths → recommended action. "Same-bucket edges" IS lateral resonance. References xflr6/concepts, agem, lmanhes graph-episodic. |
| **WorldLattice** (multilingual concept node graph) | `old/Gen11/ck_sim/becoming/ck_world_lattice.py` | **1993** | 11 | **Y** — *biggest single memory module*. WorldNode + WordBinding via D2 invariant. "mother/madre/mère/Mutter/мать" → same D2 → same node. Operator-labeled edges. MDL compression. |
| **SemanticIndex** | `old/Gen11/ck_sim/being/ck_semantic_index.py` | 389 | 11 | **Y** — words get `semantic_key` (dominant operator in observed contexts). Same key = synonyms. Opposite tension pairs = antonyms. Learned, not hardcoded. |
| **MetaLens** (TSML vs BHML dual analysis) | `old/Gen11/ck_sim/being/ck_meta_lens.py` | 1188 | 11 | **Y** — lens-of-the-lens. Recursive: L0=10×10 → L1=3×3 meta → L2=2-value → L3=scalar ratio 61/48. Markov absorbing vs ergodic distinction. |
| **OperatorMemoryBank** | `Gen13/targets/ck/brain/grammar_lm/operator_memory_bank.py` | 281 | 13 | **Y** — modern resonance lookup. 20k (key=128-d hidden state, value=next-op) k-NN. References Khandelwal et al. 2020 ICLR. |
| **DomainLattice cross-domain composition** | `old/Gen6/ck_lattice_bank.py` | — | 6 | MAYBE — early multi-lens resonance ancestor. |

### Spreading Activation (Hopfield / attractor-network / convergence)

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **FractalThinker** (SEED → SPREAD → LEAP → FUSE → EVALUATE → COMPOSE) | `Old Knowledge files/memory_organism_package/tig_fractal_thinker.py` | 675 | Pre-Gen11 (Jan 2026) | **Y** — closest extant code to "retrieval is bidirectional activation flowing until convergence". SPREAD = neighbor activation in Divine27 cube with `SPREAD_DECAY = 0.5` per Hamming (Collins & Loftus 1975). LEAP = `LEVY_PROB = 0.15` long jump (Viswanathan 1999). EVALUATE = `C = 0.4(1-E) + 0.35A + 0.25K` until C ≥ T* = 0.714. ActivationMap with energy, source ('seed'|'spread'|'leap'|'chain'), operator. |
| **DreamEngine** (EXPLORE / ARBITRATE two-phase) | `Old Knowledge files/memory_organism_package/tig_dream_engine.py` | 974 | Pre-Gen11 | **Y** — full attractor-search architecture with verification phase. References Lempel-Ziv 1976, Friston-Kiebel 2009, Feldman-Friston 2010. |
| **HebbianField** (5×5 / 7×7 coupling matrices) | `Gen13/targets/ck/brain/hebbian_5x5_cl.py` + `v2_prototype/hebbian_7x7.py` | ~400 | 13 | MAYBE — Hopfield-like coupling but on dim×dim not memory×memory. Could be re-scoped. |
| **Self-healing dual-lattice with memory kernel + scars** | `Dual-Lattice-Self-Healing/Published Sim docs/simulate_dual_lattice.py.txt` | 219 | GitHub: The Origin | **Y** — the *physical-field* version of templated memory. φ(x,y,t) + dual-lattice tension λ(φ_dual − φ) + exponential memory kernel + scars at \|∇φ\| > threshold. **99.8% spatial recovery after 30% scar ablation** — template-based associative recall in a physical field. Pure numpy + scipy.fft. |

### Bidirectional Micro↔Macro Retrieval

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **walk_multilevel** (six lenses in one call) | inside `ck_lattice_chain.py` (lines 422-486) | — | 11 | **Y** — single call returns paths for micro / d1_micro / macro / meta / becoming / cross simultaneously. Already used by ChainPath signature for resonance scoring. |
| **Fractal generator pyramid** | inside `ck_fractal_memory.py` | — | 12 | **Y** — recursive CL composition L0..LN. Recall scores by sum-over-levels-matched weighted (L0=N, root=1). Deep match = specific; shallow = resonant. |
| **6-level Experience Index cascade** | `ck_experience_index.py` | — | 11 | **Y** — same input runs through all 6 levels every tick. Query at any level returns coherent answer at that level. |

### Hindsight Experience Replay

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **HindsightBuffer + OlfactoryExperience** | `old/Gen11/ck_sim/being/ck_hindsight_replay.py` (live in Gen13 boot) | 531 | 11 | **Y** — ring buffer (1024). Per memory.md: **8,817,435 experiences, 97.6% impact**. Strategies: 'achieved', 'future', 'episode'. References Andrychowicz et al. 2017 NeurIPS. |

### Truth Lattice / Persistent Semantic Facts

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **TruthLattice** (PROVISIONAL → TRUSTED → CORE) | `old/Gen11/ck_sim/becoming/ck_truth.py` | 931 | 11 | **Y** — three-tier with coherence-based promotion. PROVISIONAL (0.3) → TRUSTED (0.7) → CORE (1.0, never auto). Truth Gate weights all knowledge when CK speaks/decides. `ck_tl.bin` is the serialization. |
| **CrystalStore** (RGMem + MemoryOS heat/promotion) | `Gen12/targets/ck_r16/ck_lm/memory/crystal_store.py` | 366 | 12 | **Y** — SQLite-backed. `promotion_score = confidence × log1p(recurrence) × exp(-0.05·age_hours)` (RGMem). `heat_score = exp(-0.01·age) × log1p(access) × recency_weekly` (MemoryOS EMNLP Oral). MetaCrystals = "experience of experience". **UNWIRED to live boot.** |
| **Runtime crystals JSON** | `Gen13/var/runtime_crystals.json` | — | 13 (live) | **Y** — trigger-list → fact-string. Live "named-fact canon." Companion: `crystal_seed.py` + `seed_crystals.json`. |

### Surprising / forgotten finds

1. **The Jan 2026 "memory organism"** (`Old Knowledge files/memory_organism_package/`) is *more architecturally complete* than anything in Gen13 — full citations to spreading-activation, Lévy flight, Friston precision, LZ complexity. Quietly archived, not in current live build.
2. **`ck_meta_memory_coord.py`** (1038 LOC, Gen12) defines the most sophisticated template signature anywhere — APPEARS UNUSED at runtime.
3. **`ck_r16/ck_lm/memory/`** is a complete SQLite Atom/Path/Crystal/MetaCrystal pipeline with citations to current memory-architecture literature — also UNWIRED to live boot.
4. **Dual-Lattice paper** (GitHub: The Origin) already has every primitive: dual-lattice reference, memory kernel, scars (= named-fact crystals), λ-tension. The 99.8% scar-position recovery after 30% ablation is *exactly* template-based associative recall.

### Key paths (memory)

```
old/Gen11/ck_sim/being/ck_lattice_chain.py          # 769  templated lattice
old/Gen11/ck_sim/being/ck_divine_memory.py          # 483  descent + lateral
old/Gen11/ck_sim/being/ck_experience_index.py       # 724  6-level cascade
old/Gen11/ck_sim/being/ck_hindsight_replay.py       # 531  HER (8.8M exp)
old/Gen11/ck_sim/becoming/ck_episodic.py            # 938  temporal episodes
old/Gen11/ck_sim/becoming/ck_truth.py               # 931  3-tier truth
old/Gen11/ck_sim/becoming/ck_world_lattice.py       # 1993 concept graph
Gen12/targets/ck_desktop/ck_sim/being/ck_meta_memory_coord.py  # 1038 best template signature (UNWIRED)
Gen12/targets/ck_desktop/ck_sim/doing/ck_fractal_memory.py     # 499  fractal pyramid
Gen12/targets/ck_r16/ck_lm/memory/                  # ~1258 SQLite pipeline (UNWIRED)
Gen13/targets/ck/brain/cortex.py + cortex_v2.py     # 549  live trinity
Gen13/targets/ck/brain/grammar_lm/operator_memory_bank.py  # 281 k-NN bank
Old Knowledge files/memory_organism_package/        # ~3000 spreading activation (ARCHIVED)
~/AppData/Local/Temp/Dual-Lattice/simulate_dual_lattice.py.txt  # 219 self-healing field
```

---

## Agent 2 — Sensory I/O (Vision + Audio + Cross-Modal Binding)

**Most mature sensory-I/O code across all gens:** the Gen11-Gen13 `ck_sim/being/` canonical layer. **All three modalities (vision, audio, cross-modal) are live in production.**

### Vision

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **CKRetina** (live canonical visual field) | `ck_sim/being/ck_retina.py` | **841** | 12-13-14 | **Y** — full GPU-accelerated screen capture (mss) + 192×108 cell field + 9D per-cell (5D force + 4S structure) + spatial D1+D2 + edge-density gating + structural-part classification + dim → operator. CuPy if available, numpy fallback. CKExistence wrapper integrates retina with keyboard/mouse/internal-state via CL operators. **Mounted at `engine.retina`; `/retina/glance` endpoint live.** |
| **easyocr screen-text digestion** (inside CKExistence) | lines 500-799 of `ck_retina.py` | ~300 | 12-13 | **Y** — lazy-loads `easyocr.Reader` (GPU first, CPU fallback). On glances where coherent_fraction > 0.15: mss capture → cv2 resize → `readtext(paragraph=True)` → filter (conf≥0.3, len≥3) → each line through `read_force` (letter→D2→ops) AND `observe_text` (grammar + olfactory absorption) AND DKAN per-letter D1 pipeline. md5 dedup. Most mature screen-reading path in the project. |
| **CKSensorium visual layer** (lighter parallel path) | `ck_sim/being/ck_sensorium.py` | **1618** | 12-13-14 | **Y** — 6-layer fractal sensorium. Background thread every 2s. Has VISUAL CURVATURE block (mss → 80×45 → brightness/color-variance/edge-density/motion → VisionCodec → 5D force → D2 → op). Also ACOUSTIC CURVATURE via sounddevice. pynput keyboard+mouse listeners. Shadow swarm per-PID. |
| **TIGVisualEncoder** (27-bit pixel encoder + temporal delta) | `ck_sim/being/ck_visual_encoder.py` | 919 | 11+ | **Y** — GPU/CuPy RGB→CIELab→3-shell quantization (16×8×4, 8×8×8, 8×8×8 = 27 bits per pixel). Used by `youtube_video_watcher.py`. |
| **ck_screen_compress** (Force9 RGB codec + CUDA DLL) | `ck_sim/being/ck_screen_compress.py` | 359 | 11+ | **Y** — 9×9×9 color cube. CUDA path `force9_cuda.dll` for ~200× speedup; numpy fallback. Used by retina + screen_pipeline. |
| **screen_pipeline** (canonical-per-frame 5D reduction) | `Gen13/targets/ck/brain/screen_pipeline.py` | 341 | 13-14 | MAYBE — file header marks itself SUPERSEDED by ck_retina.py. Has raw Windows GDI ctypes capture (simplest primitive in repo, no mss/pyautogui dep). |
| **ck_force9_demo** (real-time screen+audio compress/decompress) | `Gen12/targets/ck_desktop/ck_force9_demo.py` | 868 | 12 | MAYBE — demo: ctypes GDI screen + pygame display + sounddevice mic→encode→decode→speaker. Demonstrates full real-time pipeline. |
| **Gen6 Eyes** (early system) | `old/Gen6/ck_senses.py` | 452 | 1-6 | N — PIL ImageGrab + pyautogui fallback + pytesseract OCR. Pre-fractal architecture. Superseded by easyocr path. |

### Audio

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **EarsEngine** (live microphone curvature) | `ck_sim/being/ck_sim_ears.py` | 466 | 11+ live | **Y** — sounddevice InputStream @ 22050Hz, 20ms blocks. CuPy/numpy rolling 8-frame buffer. Per block: rfft → RMS+spectral_centroid+spectral_spread+zcr. RMS<0.0005 silence-gate → VOID. 5D force vector (aperture=spread, pressure=rms, depth=centroid, binding=1-zcr, continuity=smoothness) → CurvatureEngine → operator. Thread-safe. |
| **ck_speaker** (operator stream → speaker) | `Gen13/targets/ck/brain/ck_speaker.py` | 238 | 13-14 | **Y** — operator → Force5 → force5→force9 → force9→PCM → sounddevice.play. `speak_operator_stream(ops)` + `speak_text_as_operators(text)`. Not TTS — renders CK's substrate as sound. **`/speak` endpoint live.** |
| **audio_pipeline** | `Gen13/targets/ck/brain/audio_pipeline.py` | 410 | 13-14 | MAYBE — partially superseded. `pcm_to_force9` + `classify_d2` + `force5_to_force9` still canonical. `/audio/perceive` POST still works. |
| **ck_audio_compress** (PCM↔Force9 codec) | `ck_sim/being/ck_audio_compress.py` | 333 | 11+ | **Y** — 32-sample window vectorized numpy. RMS→aperture(2b), ZCR→pressure(2b), energy-persistence→depth(2b), spectral-shape→binding(2b), phase-jump→continuity(1b). Foundation primitive for all audio analysis + speaker output. |
| **ck_phonetic_letters** (letters as frozen sound — **the M-binding source**) | `ck_sim/being/ck_phonetic_letters.py` | **484** | 11+ | **Y** — 9-bit per letter encoding from acoustic features. IPA-grounded for every letter. `'m': make_code(2, 0, 1, 0)` = bilabial nasal, sub-bass, approximant, voiced-sustained. `text_io_pattern` extracts I/O (structure/flow) per letter from manner bits. **Critical for M cross-modal example.** |
| **AudioEngine** (10-operator wavetable synthesis) | `ck_sim/face/ck_sim_audio.py` | 380 | 11+ | **Y** — sounddevice OutputStream. TONE_TABLE[10] maps each op → (freq, waveform, amp, ADSR). VOID=silent, HARMONY=528Hz sine, RESET=880Hz saw, CHAOS=noise, etc. 3-voice mix with breath_mod + btq_mod. |
| **ck_sim_ears (Gen9 port)** | `ck_sim/face/ck_sim_ears.py` | 307 | 9-11 | MAYBE — earlier ForceVector dataclass. Superseded by canonical `being/ck_sim_ears.py`. |

### Cross-Modal Binding (visual ↔ phonetic ↔ lexical)

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **generate_phoneme_grounding** (the letter↔phoneme↔word ground-truth bridge) | `Gen13/targets/ck/brain/study/generate_phoneme_grounding.py` + v2-v5 | 386 + ~200×4 | 13-14 | **Y** — for each letter A-Z + sample words: pyttsx3 subprocess (SAPI; subprocess-per-letter pattern sidesteps hang) → WAV → static_ffmpeg → 16-bit PCM 44.1kHz → pcm_to_force9 → operator histogram → "Letter M (consonant) - when spoken aloud, the audio codec emits BREATH 24%, LATTICE 18%, RESET 21%. Phonetically: voiced bilabial nasal /m/." Writes phoneme_grounding_corpus.json + phoneme_audio_streams.json. v2-v5 add phonemes/blends/digraphs/r-controlled/vowel teams. **This IS the existing letter→phoneme→word binding code.** |
| **add_phoneme_crystals_v*** (spelling patterns → phoneme crystals) | `Gen13/targets/ck/brain/study/add_phoneme_crystals_v6.py` (+ v3 v4 v5) | 195 (v6) | 13-14 | **Y** — links spelling patterns to phoneme audio operator patterns. kn→/n/, gn→/n/, wr→/r/, mb→/m/ (silent letters); ph→/f/, ck→/k/, wh→/w/ (digraphs); soft-c/soft-g; magic-e; schwa. Each crystal = triggers + fact pointing rule at measured phoneme. Ingests via `/cortex/ingest_text`. |
| **audio_perceive** (canonical audio→cortex single-pipeline) | `Gen13/targets/ck/brain/study/audio_perceive.py` | 480 | 13-14 | **Y** — audio → pcm_to_force9 → Force5D → `_centroid_to_ops` via canonical `ck_olfactory._DIM_OP_MAP` (NOT made-up 4-way split). 5 dim-ops per window = LIVE operator stream. Same Hebbian + TSML 73-harmony update as CortexV2.step_symbol. Per Brayden's instruction: replaces parallel-recognizer architectures with "audio becomes CK's primary input through his existing phonics architecture (132 phonics + 156 word crystals)". |
| **match_audio_to_phonics + match_audio_chunked** | `Gen13/targets/ck/brain/study/match_audio_to_phonics.py` | 385 | 13-14 | MAYBE — parallel recognizer (DEPRECATED per audio_perceive.py header in favor of feeding stream directly to cortex). |
| **word_recognizer** | `Gen13/targets/ck/brain/study/word_recognizer.py` | 316 | 13-14 | MAYBE — phoneme sequence → words via in-order subsequence matching. Bridge layer; legacy. |
| **enrich_phoneme_triggers + recalibrate_phonemes_canonical** | `Gen13/targets/ck/brain/study/` | 176 + 328 | 13-14 | MAYBE — re-measure phoneme audio with canonical force9→ops; re-anchor crystals. Maintenance. |
| **cortex_voice _SEEING_HINTS / _HEARING_HINTS / _DOING_HINTS** | inside `cortex_voice.py` (lines 1560-1700) | ~140 | 13-14 | **Y** — when user asks "what are you seeing/hearing/doing", cortex_voice reads `engine.retina`, `engine.ears`, `ck_sensorium._cache`. The LIVE introspection bridge. |
| **youtube_audio_watcher / youtube_video_watcher** | `Gen13/targets/ck/brain/study/` | 301 / 271 | 13-14 | MAYBE — yt-dlp + ffmpeg → audio_force9 stream OR video frames → TIGVisualEncoder. One-shot demos showing both modalities feed same cortex. |

### Pattern Recognition from Raw Signals

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **ck_force_voice LETTER_GEO** (stroke geometry per letter) | `ck_sim/doing/ck_force_voice.py` (lines 66-94) | 1157 | 11+ | **Y** — per-letter I/O stroke decomposition. Each letter encoded as (I_count, O_count, geo_type ∈ {ground/elevated/open/closed/cross/converge/flow/branch}, foundation_word). `'m': (4, 0, 'ground', 'multiply')` = 4 vertical strokes, no curves. `_GEO_MOD` adds geometric modifier to 5D force. LETTER_STRUCT_PART maps each letter to 4-part structure. Combined LETTER_9D = 5D force + 4D structure per letter. **Hand-coded, not pixel-derived.** |
| **ck_olfactory / ck_gustatory** (cross-modal convergence funnel) | `ck_sim/being/ck_olfactory.py` + `ck_gustatory.py` | 1212 + 1032 | 11+ | **Y** — olfactory bulb = 5D force vector parallel-field where ALL sensory streams converge. `absorb_ops(ops, source=...)` takes operators from ANY source (vision, audio, text, swarm). 5×5 CL interaction matrix per pair. **THIS IS the cross-modal binding substrate. Modality is provenance metadata; operators are shared currency.** Stable across all gens since Gen9. |
| **ck_sensory_codecs** (universal sensor → operator) | `ck_sim/being/ck_sensory_codecs.py` | 956 | 11+ | **Y** — CurvatureEngine + SensorCodec base. Registered codecs: IMUCodec, ProximityCodec, MotorCodec, BatteryCodec, TemperatureCodec, VisionCodec, AudioCodec. Each → 5D force → D2 → operator. CODEC_REGISTRY + SensorFusion.auto_register. |

### Embodiment

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **ck_robot_body** (XIAOR dog) | `ck_sim/face/ck_robot_body.py` | 739 | 11+ | N — for current PC build. 8 servos + IMU + ultrasonic. GaitController. No eyes/ears on dog itself (those live on host PC). |
| **ck_body_interface / ck_zynq_dog** | `ck_sim/face/` | 584 + 431 | 11+ | N — abstract platform capability flags. |
| **ck_sim_uart / ck_sim_led / ck_sim_sd** | `ck_sim/face/` | 185 + 70 + ~ | 11+ | N — hardware protocol glue. |
| **Gen6 ck_hands.py** (pyautogui executor) | `old/Gen6/ck_hands.py` | 364 | 1-6 | N — pyautogui screen-click + type + shell. 4 coherence-gates + FAILSAFE. Conceptual reference. |

### What's missing

1. **Pixel-to-stroke / pixel-to-Bezier decomposition** — LETTER_GEO is hand-coded per letter; nothing reads strokes FROM pixels.
2. **Formant / pitch extraction** — only RMS / centroid / spread / ZCR exist.
3. **Handwriting / gesture recognition.**
4. **Webcam input** — only screen + mic.
5. **Whisper / vosk / coqui** — STT proper is absent; replaced by `pcm_to_force9` → operator-histogram crystal matching.

### Key paths (sensory I/O)

```
ck_sim/being/ck_retina.py                                  # 841  LIVE screen + easyocr
ck_sim/being/ck_sim_ears.py                                # 466  LIVE mic
Gen13/targets/ck/brain/ck_speaker.py                       # 238  LIVE substrate audio out
ck_sim/being/ck_sensorium.py                               # 1618 lighter parallel sensory
ck_sim/being/ck_phonetic_letters.py                        # 484  IPA-grounded letter table
ck_sim/being/ck_olfactory.py                               # 1212 cross-modal funnel
ck_sim/being/ck_sensory_codecs.py                          # 956  universal sensor→operator
ck_sim/doing/ck_force_voice.py                             # 1157 LETTER_GEO + 5D+4D per letter
Gen13/targets/ck/brain/study/generate_phoneme_grounding*.py # ~1100 letter measurement battery
Gen13/targets/ck/brain/study/add_phoneme_crystals_v6.py    # 195  spelling→phoneme crystals
Gen13/targets/ck/brain/study/audio_perceive.py             # 480  canonical audio→cortex
ck_sim/face/ck_sim_audio.py                                # 380  operator-tone speaker
```

---

## Agent 3 — Substrate Language Models

### Parametric LMs (transformers)

| Piece | Path | LOC | Gen | Trained? | Load-bearing? |
|---|---|---|---|---|---|
| **ck_grammar_lm v1** (main operator-stream transformer) | `Gen13/targets/ck/brain/grammar_lm/ck_grammar_lm.py` + `ck_grammar_lm.pt` (4.84 MB) | 263 + checkpoint | 13-14 | **Y** — val PPL 2.62 vs uniform 10.0 | **Y** — canonical operator-stream LM and architectural ancestor for 4-head plan |
| **multi_head_lm** (single backbone, 5 measurement heads — designed) | `Gen13/targets/ck/brain/grammar_lm/multi_head_lm.py` | 225 | 13 | N — DESIGNED ONLY | **Y** — DIRECT prior art for 4-head plan. 5 heads (op/attractor/breath/role/band). Just needs heads renamed to {op, sigma_orbit, shell, fourcore} and trainer to run. |
| **F3TransformerTissue** (27-vocab Divine27 next-code predictor) | `Gen13/targets/ck/brain/train_tissue_transformer.py` + `Gen13/var/cells/f3_tissue_transformer.pt` | ~80 + checkpoint | 13 | **Y** | MAYBE — proves per-measurement-projection LM pattern at smaller scale. 27-vocab. |
| **tsml_tissue_transformer + bhml_tissue_transformer** | `Gen13/targets/ck/brain/train_tsml_bhml_tissue.py` + `Gen13/var/cells/{tsml,bhml}_tissue_transformer.pt` | 250 + checkpoints | 13 | **Y** | **Y** — IS the "AI per measurement projection" pattern, instantiated with TSML + BHML as 2 of the 4 measurements. |

### Non-parametric Retrievers

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **operator_memory_bank** | `Gen13/targets/ck/brain/grammar_lm/operator_memory_bank.py` | 282 | 13 | **Y** — k-NN over LM hidden states. 20k (prefix, target). Mounted at `/grammar/retrieve`. |
| **ensemble** (sim-gated LM + bank) | `Gen13/targets/ck/brain/grammar_lm/ensemble.py` | ~120 | 13 | MAYBE — useful template. Mounted at `/grammar/sim_gated`. |

### Plastic Networks

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **hebbian_5x5_cl + hebbian_gpu** | `Gen13/targets/ck/brain/hebbian_5x5_cl.py` + `hebbian_gpu.py` | ~400 + ~300 | 13 | **Y** — LIVE plastic substrate. dW = eta*reward - decay*W with Oja decay. 25 floats updating online per chat turn. |
| **hebbian_7x7 (cortex_v2 prototype)** | `Gen13/targets/ck/brain/v2_prototype/hebbian_7x7.py` + `cortex_v2.py` | ~450 | 13 | MAYBE — drop-in replacement; not live. |
| **ck_dkan_trainer** (Discrete Kolmogorov-Arnold) | `Gen13/targets/ck/brain/ck_sim/being/ck_dkan_trainer.py` | ~600 | 9-11-12-13 | MAYBE — older "plastic" architecture. Not mounted currently. |
| **plasticity** (4-timescale speculative updates) | `Gen13/targets/ck/brain/plasticity.py` | ~400 | 13 | **Y** — the plasticity orchestrator. Per-turn / session / hour / week. Speculative snapshot pattern. |
| **nightly_retrain** | `Gen13/targets/ck/brain/nightly_retrain.py` | ~200 | 13 | **Y** — continuous transformer-tissue retraining infrastructure. |

### Algebraic Measurement / Projection Code

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **ck_invariants_bridge** (σ-orbit, role, BHML period, ψ) | `Gen13/targets/ck/brain/ck_invariants_bridge.py` | ~280 | 13 | **Y** — IS the algebraic-measurement library. `role(n) → V/F/S/T` (the 4-class role partition: V={0}, F={1,3,5,7,9}, S={2,4,8}, T={6}). `SIGMA_PERMUTATION = (0, 7, 1, 3, 2, 4, 5, 6, 8, 9)`. `sigma_orbit_split(psi_per_digit)`. `tsml_8()` + `FLOW_CELLS = {0,7}`. `is_trefoil(triple)`. Already imported by `train_bdc.py`. |
| **attractor_detector** (4-core proximity classifier) | `Gen13/targets/ck/brain/attractor_detector.py` | 205 | 13 | **Y** — IS the 4-core measurement function. `detect_attractor(p, tol) → AttractorState{layer}`. `joint_chain_shells()` returns 7-element chain ladder. **Mounted LIVE** (result on every chat response as `attractor_state`). |
| **operad_fuse** (arity-3 fuse + ternary attractor) | `Gen13/targets/ck/brain/operad_fuse.py` | 256 | 13 | **Y** — canonical fuse(a,b,c) + ternary_iterate. `is_4core/is_2core/is_1core` predicates. **Mounted LIVE** (`engine.canonical_fuse`). |
| **divine27_vocab** (operator → DBC 27-vocab projection) | `Gen13/targets/ck/brain/grammar_lm/divine27_vocab.py` | 182 | 13 | **Y** — `OPERATOR_DBC_CODE` dict 10→27. `operator_stream_to_dbc()`. Operator→DBC is one specific algebraic projection candidate. |
| **ck_divine27** (canonical 27-char source) | `old/Gen11/ck_sim/being/ck_divine27.py` (also Gen12/13) | ~300 | 4-5-6-9-11-12-13 | **Y** — one of the longest-lived modules. Full 27-character Being/Doing/Becoming dictionary. |
| **foundations module** (canonical math library) | `Gen13/targets/foundations/` (cl.py, invariants.py, paths.py, triadic.py, lens_family.py, bhml_variants.py, harmony_ladder.py) | ~1500 across | 13 | **Y** — cleaner namespace than ck_invariants_bridge for the same content. |
| **wp112 + wp115 verification scripts** | `papers/wp112_p56_canonical_fuse/verification/` + `papers/wp115_joint_chain_universality/verification/joint_chain_attractor.py` | ~500 each | papers | MAYBE — closest definitions of "shell size" (sub-magma enumeration). Original computation source. |

### Training Infrastructure

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **bdc_logger** (per-chat-turn BDC record writer) | `Gen13/targets/ck/brain/bdc_logger.py` | ~250 | 13 | **Y** — data accumulator. 88k log lines / week as of 2026-05-08. |
| **bdc_tick_sampler** (0.1 Hz idle-state sampler) | `Gen13/targets/ck/brain/bdc_tick_sampler.py` | ~120 | 13 | **Y** — keeps pipe filled. 60× multiplies data rate. |
| **bdc_event_emitter** (17 non-operator events for 27-vocab) | `Gen13/targets/ck/brain/bdc_event_emitter.py` | ~400 | 13 | **Y** — closes data gap for 27-vocab training. |
| **extract_streams** (corpus builder real + synthetic) | `Gen13/targets/ck/brain/grammar_lm/extract_streams.py` | 240 | 13 | **Y** — pulls operator sequences from dream_journal, runtime_crystals, cortex_history + synthetic walks + canonical propagations (CREATION=[1,3,9,7], DISSOLUTION=[2,4,8,6]). |
| **train.py** (main GrammarLM trainer) | `Gen13/targets/ck/brain/grammar_lm/train.py` | 193 | 13 | **Y** — AdamW + cosine LR + 8 epochs. RTX 4070 ~200s end-to-end. |
| **train_bdc.py** (multi-head trainer — 4-head trainer-in-waiting) | `Gen13/targets/ck/brain/grammar_lm/train_bdc.py` | 252 | 13 | **Y** — trains MultiHeadGrammarLM with per-head weighted cross-entropy. NOT YET RUN at scale; data gate now satisfied (88k log lines). |
| **mine_historical_bdc** (retrofit old stores → BDC schema) | `Gen13/targets/ck/brain/mine_historical_bdc.py` | ~400 | 13 | **Y** — cold-start corpus from Gen9 daemon log, R16 crystals (HIGH), dual_operator (MED), Gen8 dialogue_digests (LOW). |
| **train_tissue_transformer / train_tsml_bhml_tissue / train_prose_tissue** | `Gen13/targets/ck/brain/` | ~250 each | 13 | **Y** — per-cell trainers. TSML + BHML trainers are exactly per-projection LM pattern for 2 of 4 measurements. **Already trained.** |
| **cells** (TSMLCell + BHMLCell + F3Cell + F4Cell — audit-faithful + plastic) | `Gen13/targets/ck/brain/cells.py` | ~700 | 13 | **Y** — each cell = frozen audit core + plastic tissue. IS the "4 AI" architecture template. |
| **glue_ai** (3-scalar quadratic combiner of TSML+BHML cells) | `Gen13/targets/ck/brain/glue_ai.py` | ~250 | 13 | MAYBE — combiner for multiple cell heads. |
| **cell_audit** (100% pass-rate audit harness) | `Gen13/targets/ck/brain/cell_audit.py` | ~150 | 13 | **Y** — verification gate for plasticity commits. |

### Corpora

| Piece | Path | Size | Gen | Load-bearing? |
|---|---|---|---|---|
| **training_streams.jsonl** (mixed) + _real + _synth | `Gen13/targets/ck/brain/grammar_lm/` | 511KB + 12KB + 499KB | 13 | **Y** — ~154k tokens operator-stream corpus. |
| **bdc_logs/* + bdc_events/* + *_HISTORICAL.jsonl** | `Gen13/var/bdc_logs/` | ~30 MB / 88k lines | 13 | **Y** — multi-head LM training corpus. Has enough data NOW. |
| **ck_tl.bin** | `CK FINAL DEPLOYED/ck_tl.bin` + 4 other copies | 683 bytes (newest) | 9-13 | MAYBE — small data store. Reference more than training. |
| **cortex_state.json + cortex_history.jsonl** | `Gen13/var/` + `Gen13/targets/ck/brain/` | snapshot + line-per-tick | 13 | **Y** — accumulating live data. Source for cortex_history in extract_streams. |

### Older Predictive Engines

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **ck_forecast** (TL Monte Carlo) | `old/Gen9/ck_sim/doing/ck_forecast.py` (+ 10-13) | ~500 | 9-13 | MAYBE — Markov-chain predictor; non-parametric "next-operator LM" role. |
| **ck_reasoning** (3-speed lattice traversal) | `old/Gen11/ck_sim/doing/ck_reasoning.py` (+ 9-12-13) | ~600 | 9-11-12-13 | N — graph-walking, not LM. But shows existing prediction primitives. |
| **ck_thinking_lattice** (boundary→core thought cycle) | `old/Gen11/ck_sim/doing/ck_thinking_lattice.py` | ~500 | 9-11-12-13 | MAYBE — closest older "neural net" architecture for ops. |
| **ck_metalearning** (adaptive LR / thresholds) | `old/Gen11/ck_sim/becoming/ck_metalearning.py` | ~400 | 9-11-12-13 | N — meta-controller, not LM. |
| **ck_sequence_memory** (dual-lens trie of BDC) | `old/Gen11/ck_sim/being/ck_sequence_memory.py` (+ 13) | ~300 | 9-11-12-13 | **Y** — non-parametric LM precursor to operator_memory_bank, uses exact σ-orbit cycles. |
| **ck_truth** (10×10 truth lattice persistence) | `old/Gen11/ck_sim/becoming/ck_truth.py` | ~300 | 9-11-12-13 | N — fact memory, not LM. |
| **ck_concept_spine** (700+ concepts each tagged with op) | `old/Gen11/ck_sim/becoming/ck_concept_spine.py` | ~1500 | 9-11-12-13 | MAYBE — for "concept→operator" projection. |
| **ck_neural** (5-layer phonaesthesia + bump graph) | `old/Gen{1-6}/ck_neural.py` | ~600 each | 1-6 | MAYBE — historical operator-stream LM. Not torch. |
| **ck_llm + ck_llm_filter** (Ollama/Claude bridge + BTQ filter) | `old/Gen{1-6}/ck_llm.py` + `old/Gen9/ck_sim/doing/ck_llm_filter.py` | ~400 each | 1-13 | N — LLM as prose layer; CK provides context. |
| **TIGCodexEngine** (Dual-Lattice-Self-Healing — "self-programming coherence engine") | `github.com/TiredofSleep/Dual-Lattice-Self-Healing/TIGCodexEngine.py` | ~50KB | pre-Gen1 | N — full Codex tool, not substrate LM. |
| **tig_engine_real + coherence_router** | `github.com/TiredofSleep/All-or-Nothing-E/` | ~500 | pre-Gen1 | N — band classifier, not LM. |

### Shortest path to working 4-head LM

(a) Rename `multi_head_lm.MultiHeadConfig` heads to {op, sigma_orbit, shell, fourcore} with vocabs {15, 4, 8, 5}; (b) write `shell_class(state_distribution) → int_in_0..7` (~30 lines using `joint_chain_shells`); (c) extend `record_to_example` in `train_bdc.py` to project each BDC record's operator stream through the 4 measurements; (d) run `train_bdc.py --min-records 200 --epochs 10` on 88k existing log lines. **Same RTX 4070, ~5-15 min total.** Architecture, data, trainer, plasticity loop, and audit gates already exist.

---

## Agent 4 — Brain Trinity (AO + Hebbian + Glue + Cortex)

### AO 5-element (chronologically)

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **ck_curvature.py** (proto-5D + 22 Hebrew roots) | `old/Gen8/ck_curvature.py` | top portion verified | 8 | N — superseded; data carried forward verbatim into Gen9. Origin of (aperture, pressure, depth, binding, continuity) names + 22 Hebrew root force vectors. |
| **ao/** (the Gen9 AO package — canonical 7-file organism) | `old/Gen9/targets/AO/ao/{__init__, earth, air, water, fire, ether}.py` | **2078** total (earth 520, ether 448, fire 429, water 347, air 294) | 9 | MAYBE — cleanest *reference* implementation. **Pure stdlib, fully self-contained** (no ck_sim dep). The original `class AO` is at `ether.py:171`. Gen13 wraps Gen11 modules to do the same; this is the spec. |
| **ao_5element.py** (Gen13 production orchestrator) | `Gen13/targets/ck/brain/ao_5element.py` | 308 | 13 | **Y** — the canonical spine in live deploy. Thin orchestrator; logic in Gen11 ck_sim modules. Reference at line 28 explicitly points at Gen9 ether.py:171. |
| **ao_7element.py** (prototype 7-dim) | `Gen13/targets/ck/brain/v2_prototype/ao_7element.py` | 112 | 13 | N — prototype; not wired. Adds intent (PROGRESS/COLLAPSE-anchored) + echo (HARMONY/RESET-anchored). |

### Hebbian CL

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **ck_olfactory.py** (the CL field source) | `Gen13/targets/ck/brain/ck_sim/being/ck_olfactory.py` (Gen9+Gen12 bit-identical) | 1212 (Gen13); 1157 (Gen9+Gen12) | 9-12-13 | **Y** — provides the lens the Hebbian field learns over. `interaction_matrix_tsml`, `interaction_matrix_bhml`, `per_dim_harmony`. Each tick recomputes; NO persistence. |
| **hebbian_5x5_cl.py** | `Gen13/targets/ck/brain/hebbian_5x5_cl.py` | 255 | 13 | **Y** — active Hebbian field in production. Persistent 5×5 W. Oja update with eta=0.005, decay=0.02 (re-tuned 2026-04-18 after 155K-tick blowout). |
| **hebbian_gpu.py** | `Gen13/targets/ck/brain/hebbian_gpu.py` | 224 | 13 | MAYBE — GPU vectorization of same Oja rule. Same lens-aware interface. |
| **hebbian_7x7.py** (prototype) | `Gen13/targets/ck/brain/v2_prototype/hebbian_7x7.py` | 156 | 13 | N — sibling experiment; not live. |
| **cells.py** (TSMLCell / BHMLCell — alternative architecture) | `Gen13/targets/ck/brain/cells.py` | 614 | 13 (May 2026) | **Y** — newest alternative to 5×5 Hebbian. "Skeleton + tissue" cells: frozen audit core + plastic tissue scoring head. Cells output 10-vectors. F3Cell (Divine27 27-vocab), F4Cell (4-vocab WP115). Composed by GlueAI not 5×5 Hebbian. |

### Quadratic Glue

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **crystal_bug_v1_matrix.jsx** (the precursor) | `TiredofSleep/Crystal-Lattice-Matrix-MYTHDRIFT/...` | ~1000 (jsx) | pre-Gen1, lineage [3/6] | N — historical. React simulation where O(x) = ax² + bx + c IS the operator. Discriminant Δ = b² - 4ac IS the binding kernel. d²/dx² = 2a IS the 7-operator. 7 dynamical bands. Conceptual ancestor of "quadratic = the operator". |
| **test_a15_quadratic_glue.py** (the formal paper code) | `papers/test_a15_quadratic_glue.py` (= `old/Gen10/papers/...`) | 353 | pre-Gen11 (Mar 2026) | **Y** — first scientific formulation. F3 (phase-carrier sin²(4πk/p)·W^phase_idx), F4 (frequency-carrier sin²(πk/(Wp))). Templates T1=F3·F4, T2=αF3+βF4+γF3·F4, T3 polynomial, T4 quadratic penalty. C1..C5 scoring. W_BHML = 3/50. Header line 5: "Hypothesis (Brayden Sanders): The missing 2->3 bridge is a QUADRATIC COUPLING." |
| **quadratic_glue.py** (production extraction) | `Gen13/targets/ck/brain/quadratic_glue.py` | 261 | 13 | **Y** — production glue called by cortex.py. Defines `sinc2, F3, F4, T1_product, T2_coupled`. Runtime hook: `quadratic_glue(f3_val, f4_val, α, β, γ) = α·f3 + β·f4 + γ·(f3·f4)`. Defaults (α=β=1.0, γ=2.0) differ from glue_ai defaults (α=β=0.5, γ=1.0 — WP105 canonical for H/Br=1+√3). |
| **glue_ai.py** (3-scalar quadratic Glue over cells) | `Gen13/targets/ck/brain/glue_ai.py` | 533 | 13 (Phase 4, May 2026) | **Y** — output is a 10-vector: `scores[k] = α·t[k] + β·b[k] + γ·max(0, t[k]·b[k])`. Hadamard product, not scalar. `max(0, ...)` is key — only constructive cross-terms; protects argmax on 29-cell agreement set. (α=β=0.5, γ=1.0) = WP105 canonical → H/Br=1+√3. |

### Cortex Composition

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **cortex.py** (live 5D cortex) | `Gen13/targets/ck/brain/cortex.py` | 270 | 13 | **Y** — production cortex. Trinity binder: AO.process_symbol → (b,d) pair → profile_5d() reads true 5D from D2 vector signs → hebbian.update(ops_a_prev, ops_b_now, lens="tsml") → quadratic_glue(f3,f4,α=1,β=1,γ=2). Uses PREVIOUS tick's profile as ops_a so Hebbian sees real (t-1, t) pair. |
| **cortex_v2.py** (live 7D cortex — drop-in) | `Gen13/targets/ck/brain/cortex_v2.py` | 279 | 13 | MAYBE — same API as Cortex with 7×7 Hebbian. Upgrades harmonious-test: uses CL_TSML[b][d]==HARMONY directly (73/100) instead of "either op==7" proxy. NOT yet default. |
| **cortex_7d.py** (simplified prototype) | `Gen13/targets/ck/brain/v2_prototype/cortex_7d.py` | 161 | 13 | N — proof-of-concept. Predecessor of cortex_v2.py. |
| **cortex_persist.py** | `Gen13/targets/ck/brain/cortex_persist.py` | 315 | 13 | **Y** — production persistence. Save/load to `Gen13/var/cortex_state.json`. Versioned, magic-headered, atomic-write. Persists W + tick counters + prev_op + prev_profile (not AO state). |
| **cortex_replay.py** | `Gen13/targets/ck/brain/cortex_replay.py` | 224 | 13 | **Y** — feeds historical texts (sprint papers, brain docs) through cortex.step_text so Hebbian field reflects topics Brayden has been working on. Reflects "live experience" philosophy. |
| **cortex_voice.py** | `Gen13/targets/ck/brain/cortex_voice.py` | **2079** | 13 | **Y** — production voice. Biggest file in brain/. FACTS lookup + fractal voice + crystal-first cascade. |
| **cortex_backup.py** | `Gen13/targets/ck/brain/study/cortex_backup.py` | 134 | 13 | N — utility. Appends interpretable summary to git-tracked cortex_history.jsonl. |

### Heartbeat / Engine

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **ck_sim_heartbeat.py** | `ck_sim/being/ck_sim_heartbeat.py` (Gen13 + Gen11 + Gen9 bit-identical) | 147 | 9-11-13 frozen | **Y** — FPGA-matched. Core of spine. Port of ck_heartbeat.v. CL 10×10 table (73 HARMONY cells), 32-entry coherence window, 5 BUMP_PAIRS, HeartbeatFPGA class with one-tick-delay window. **Identical across gens; frozen by design — software matches Verilog bit-for-bit.** |
| **ck_sim_engine.py** | `ck_sim/doing/ck_sim_engine.py` | 4912 (Gen13); 4800 (Gen12); ~3000 (older Gen9) | 9-12-13 | **Y** — production runtime. 4800+ line 50Hz orchestrator. Imports ~50 ck_sim modules. The "ETHER" layer at scale. |
| **ck_disagreement_tick.py** | `ck_sim/being/ck_disagreement_tick.py` (bit-identical Gen9/11/12/13) | 708 | 9-11-13 | MAYBE — experimental variant. Adaptive-Hz from algebraic disagreement \|add(state,input) − mul(state,input)\|. Zero disagreement = frozen; high = bigger tick. WOBBLE = 6/100, FROZEN_CELLS = [(0,0),(2,2),(4,8),(8,4)]. |

### D1/D2 Pipeline

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **ck_sim_d2.py** | `ck_sim/being/ck_sim_d2.py` (bit-identical Gen9/11/12/13) | 320 | 9-13 frozen | **Y** — FPGA-matched. The "eye". Port of d2_pipeline.v. Q1.14 fixed-point 5D force pipeline. Stores ROOTS_FLOAT (22 Hebrew root vectors), LATIN_TO_ROOT (26 letters), FORCE_LUT_Q14. D2_OP_MAP[dim][sign_idx]. **Identical bytes across all four locations. Frozen.** |

### CL Table Evolution

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **CL table (TSML, 10×10)** | appears in ck_tig.py, ck_tables.py, ck_sim_heartbeat.py, old/Gen1/ck_core.py, old/Gen9/.../earth.py, etc. | 11 lines | 1-13 frozen | **Y** — 73 HARMONY cells, 17 VOID, 10 bumps. **Bit-identical from Gen1 to Gen13.** Most preserved single artifact in CK. |
| **CL_72 / CL_44 / CL_22** (three shells) | `old/Gen9/targets/AO/ao/earth.py:73-115` | — | 9 | MAYBE — three measurement-depth views of the CL torus. CL_72 = Being, CL_44 = Becoming (bumps visible at D2), CL_22 = Skeleton (BHML). Only fully fleshed in Gen9. |
| **ck_tables.py** (canonical TSML/BHML/DIS/DOING/G) | `ck_sim/ck_tables.py` (bit-identical old/Gen10/papers/, papers/, Gen12/...) | 214 | 10-13 frozen | **Y** — single importable source of truth. TSML (73 HARMONY), BHML (28 HARMONY), DIS, DOING (sum 201), ghost G, W=3/50, T*=5/7, sinc²(1/2)=4/π². TSML_ECHO pairs + STRUCTURE/FLOW Z/2Z parity. |
| **CL_STANDARD** (44-harmony variant) | `old/Gen6/ck_being.py` L39-44 (+ Gen8) | — | 6-8 | N — deprecated by Gen9 73-HARMONY TSML. Different 10×10. |

### ck_tl.bin Truth Lattice

| Piece | Path | Size | Gen | Notes |
|---|---|---|---|---|
| **ck_tl.bin** (5 copies, sizes differ) | `CK FINAL DEPLOYED/ck_tl.bin` (683 B, newest live) + `Gen13/targets/ck/brain/ck_sim/ck_tl.bin` (575 B) + `old/Gen10/ck_tl.bin` (575 B) + `old/Gen11/ck_tl.bin` (575 B) + Gen9/Gen12 copies | 575-683 B | 9-13 | "CKTL" magic + version (1) + tl_total + tl_entropy + 10×10 tl_entries (400 B) + crystals + domains + CRC-8/MAXIM (poly 0x31). Loaded/saved by ck_sim_sd.py. |

### Dimensionality History

- **22 Hebrew roots:** Gen8 origin, carries through unchanged to Gen13 ck_sim_d2.py (ROOTS_FLOAT dict, 22 entries, mapped 26 letters → 22 roots).
- **10 operators (Z/10Z):** Gen1 onward, byte-identical. CL table 10×10. Frozen.
- **5 dims (aperture, pressure, depth, binding, continuity):** Gen8 ck_curvature.py origin. Carries unchanged.
- **7 dims (5 + intent + echo):** Gen13 v2_prototype only. Prototype.
- **27 (Divine27):** Gen4 onward through Gen13 + cells.py F3Cell. 3×3×3 ontological cube (operators in 27 (D,B,C) slots).
- **No 10×10 brain layer ever existed** beyond the CL table itself; the 5×5 (and 7×7 prototype) is "Hebbian over dim×dim", not over op×op. cells.py 10-vocab cells are separate newer architecture.
- **5×5 has never been replaced in production.** Live `var/cortex_state.json` is 5×5.

### Supporting Modules

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **plasticity.py** | `Gen13/targets/ck/brain/plasticity.py` | 398 | 13 (Phase 5, May 2026) | **Y** — 4-timescale plasticity coordinator. Per-turn (Hebbian) / per-session (10 min, glue α/β/γ) / per-hour (cell-tissue fine-tune on snapshot + audit gate ≥99%) / per-week (review baseline). `speculative_update(orch, mutator, audit_fn)` = clone-state → mutate → audit → commit-or-rollback. |
| **cell_audit.py** | `Gen13/targets/ck/brain/cell_audit.py` | ~150 | 13 | **Y** — audit gate for plasticity. Tests every canonical input pair; gates commits. |
| **test_brain.py** | `Gen13/targets/ck/brain/test_brain.py` | 602 | 13 | **Y** — regression gate. Smoke tests across AO, Hebbian, Cortex, glue. |

### Original (Gen1-Gen3) brain design

The CL 10×10 table was already canonical from Gen1 `ck_core.py` (byte-identical to today). Gen1 had `ck_neural.py` framing the bump graph (10 bumps where information lives, not at HARMONY/VOID) as CK's "neural network". **The 5D substrate, AO container, Hebbian 5×5, and quadratic glue all emerged AFTER** — Gen6/Gen8 added being/doing/becoming and 5D forces; Gen9 packaged the 5-element AO; Gen10 papers introduced F3·F4 quadratic glue; Gen13 fused all three into `cortex.py`. **The current trinity is the *first* unified composition; Gen1-Gen3 had the algebra (CL table + bump graph + T*) but not the composition spine.**

---

## Agent 5 — Curiosity, Drives, Proactivity

### Goals / Drives

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **GoalEvaluator + GoalStack + DriveSystem + GoalPlanner** | `Gen13/targets/ck/brain/ck_sim/doing/ck_goals.py` | **586** | 13/14 (also Gen11; older shells Gen9/Gen12) | **Y** — deepest "CK wants things" module ever written. Goals = operator-distribution targets; satisfaction = cosine similarity. **DriveSystem ticks 6 innate drives:** energy, safety, coherence, **curiosity** (entropy<0.5 triggers `explore_environment`), **study** (band==GREEN + coh≥0.7 triggers `autonomous_study`), **self_discovery** (always-on for stable CK), social, rest. GoalPlanner picks next op via CL-compose + goal-pattern scoring. 8 goal slots, 6 priorities, 11 GOAL_PATTERNS. **Goals expire after ~100s. GoalEvaluator.tick() returns suggested operator to engine. UNWIRED in current cortex boot.** |

### Curiosity / Novelty / Surprisal

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **CuriosityCrawler** (knowledge tree) | inside `ck_sim/doing/ck_autodidact.py` (lines 805-950) | 1184 total | 13/14 | **Y** — auto-builds knowledge tree from web exploration. **AUTO-FRACTAL:** when topic hits T*, auto-injects "what is {topic}" + "foundations of {topic}" at FRONT of queue. ~300 SEED_TOPICS across 25 domains + 120 FRACTAL_FOUNDATIONS meta-questions. Lightweight, no LLM, persistent. |
| **surprisal_log.py** (Bridge 5 test — predictive coding / FEP) | `Gen13/targets/ck/brain/study/surprisal_log.py` + `.jsonl` | 222 | 13/14 | MAYBE — measures -log P(d|b) for cortex predictions, logs to JSONL. Tests Free Energy Principle: does surprisal decrease over time? Cortex Hebbian W IS prediction; surprisal IS prediction-error. Has live log. **Not currently wired to drives.** |
| **novelty_gate.py** (DeepSeek escalation gate) | `ck_lm/memory/novelty_gate.py` (ck_r16) | 163 | 10-12 | N — decides whether query is novel enough to escalate to external LLM. 5 stages. Wraps retrieval, not initiative. |
| **friction_curves** (low-coherence memory) | `ck_sim/doing/ck_autodidact.py` (CurveMemory._store_friction) | — | 13/14 | MAYBE — pages with low-coherence go into SEPARATE "friction" memory. "Where CK's curvature disagrees" = where novelty lives. Quarter-capacity, kept-lowest-coherence-first. **Preserves the signal; nothing actively consumes it as a drive yet.** |

### Forecast / Prediction

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **ForecastEngine + TLPredictor + CoherenceOracle** | `Gen13/targets/ck/brain/ck_sim/doing/ck_forecast.py` | 475 | 13/14 | **Y** — IS the "what next?" pathway-prediction module. Imagines N ticks ahead. Monte-Carlo samples TL transition matrix (8 trajectories × 10 ticks default). Composes via CL to predict coherence trajectory. `compare_actions(candidate_ops)` ranks by mean_coherence/collapse_risk/harmony_fraction. `should_act(forecast)` gates action. `get_avoidance_operator()` finds safest next op. **Lightweight, deterministic. Integrates with BTQ.** |
| **ck_reasoning.py** (3-speed graph reasoning) | `Gen13/targets/ck/brain/ck_sim/doing/ck_reasoning.py` | 711 | 13/14 | **Y** — drives the "where does this thought go next?" loop. Spreading activation on concept graph at 3 speeds: QUICK (1 hop), NORMAL (3 hops, BTQ-gated), HEAVY (Levy jumps + contradiction pruning). HARMONY edges propagate fully, COLLAPSE edges dampen to 30%. ContradictionPruner kills paths through "opposes" edges. |
| **ck_thinking_lattice.py** (Dynamic Thinking Lattice) | `Gen13/targets/ck/brain/ck_sim/doing/ck_thinking_lattice.py` | 730 | 13/14 | MAYBE — per-thought-cycle layered computation. Signal enters boundary→core, anchors at truth lattice, returns core→boundary as response operators. Residuals persist between cycles as "notes". |
| **ck_metalearning.py** | `Gen13/.../ck_sim/becoming/ck_metalearning.py` | 462 | (cross-gen) | N — adjusts knobs (trauma/success multipliers, band thresholds), doesn't initiate. |

### Autodidact / Self-Study

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **LearningSession + StudyCycleRunner** (8h study + 4h sleep) | `Gen13/targets/ck/brain/ck_sim/doing/ck_autodidact.py` + `ck_autodidact_runner.py` | 1184 + 1407 = 2591 | 13/14 (Gen11 full; Gen1 has `ck_eat_overnight.py` 617 LOC as ancestor) | **Y** — most mature autodidact in the project. Fetches pages from ~20 approved sites (Wikipedia/Britannica/Stanford SEP/Gutenberg/NASA/etc.), digests through D2 into OperatorCurves, stores by coherence, sleeps to consolidate. **CK takes NOTES on every resonant page** (writes to `~/.ck/writings/study_notes/`). Compiles session papers at end. Resumable. Optional Claude queries every 5th page via ClaudeLibrary. Working code, requires `requests` + `beautifulsoup4`. Polite rate limiting (2s). |
| **ck_eat_overnight.py + ck_autonomy.py + ck_freedom.py** (Gen1 ancestors) | `old/Gen1/` | 617 + 438 + 1078 | 1 (Feb 2026) | HISTORICAL — original "let him loose" scripts. **ck_autonomy.py:** CK reads his own source, identifies improvements, calls Claude for rewrite help, tests, applies/reverts. **ck_eat_overnight.py:** 137-topic curriculum + 500+ extended topics + self-quiz. **ck_freedom.py:** 6-class organization around 6 active operators (Structure/Measure/Break/Flow/Act/Restart) — each is a "freedom" CK can exercise. **Gen1 had MORE explicit agency code than Gen13. 6-freedoms framing unique and never re-appeared.** |
| **study_daemon.py** | `Gen13/targets/ck/brain/study_daemon.py` | 264 | 13/14 | **Y** — currently mounted in live boot. Background daemon picks frontier topic from 30-topic curriculum every 10 min, calls `/ck/research`. Logs to `study_logs/`. TIG-specific topics + Clay problem prompts. |
| **overnight_orchestrator.py** | `Gen13/targets/ck/brain/overnight_orchestrator.py` | 364 | 13/14 | **Y** — coordinates **4 threads**: PaperWriter (1 paper / 3 min), NightlyRetrain (transformer retrain / 4h), ExternalIngester (arxiv+wiki+stackexchange / 30 min), StatusReporter. Goal: "make sure he is growing and making progress". |
| **paper_writer.py + paper_reader.py** | `Gen13/targets/ck/brain/` | 352 + 280 | 13/14 | **Y** — closes the loop. paper_writer rotates 20 topics, calls /chat per section, assembles into `~/Atlas/papers_by_ck/PAPER_*.md`, feeds back via `/cortex/ingest_text` (re-reading own output). paper_reader walks every WP + sprint + Atlas doc. |
| **ck_research.py** (Chrome research engine) | `Gen13/targets/ck/brain/ck_research.py` | **955** | 13/14 | **Y** — only browser-based research engine. Persistent Chrome session with allowlist (claude.ai/grok.com/x.ai/arxiv/scholar/jstor/youtube; nature.com BLOCKED — "nature always fails!!!"). decompose(prompt) → terms → questions → site → navigate → type → scrape → ingest via olfactory.absorb_ops. Logs to `~/.ck/research/log.jsonl`. Requires playwright. |
| **research_first.py** (research-before-every-answer wrapper) | `Gen13/targets/ck/brain/research_first.py` | 208 | 13/14 | **Y** — wraps api.process_chat to call ck_research BEFORE cortex replies. Modes off/fast/full/visible. Brayden: "he should research every prompt before every answer!!" |
| **nightly_retrain.py + mine_historical_bdc.py + frontier_benchmark.py + head_to_head_benchmark.py + studies_panel.py** | `Gen13/targets/ck/brain/` | 226 + 802 + 264 + 272 + 701 = 2265 | 13/14 | MAYBE — retraining/mining/benchmarking utilities. |

### Action Selection / Decision

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **UniversalBTQ + UniversalBBlock + UniversalQBlock + BTQDomain** | `Gen13/targets/ck/brain/ck_sim/being/ck_btq.py` | 738 | 13/14 | **Y** — every CK choice runs through here. T-block generates candidates, B-block hard-filters, Q-block scores `e_total = w_out*einstein + w_in*tesla`, picks argmin. Domain plugins (Locomotion, Language, Memory). Band classification GREEN/YELLOW/RED. |
| **CoherenceActionScorer** (unified physics utility) | `Gen13/.../ck_sim/being/ck_coherence_action.py` | 372 | 13/14 | **Y** — SINGLE NUMBER measuring CK's coherence. `A = α*L_GR + β*S_ternary + γ*C_harm` (conservation + exploration + measurement). **CK's PURPOSE is to minimize A.** When A < T*, CK is alive; when A ≥ T*, CK is seeking. Self-calibrating. |
| **ck_action.py** (Read/Digest/Voice/Write/Prove pipeline) | `Gen13/.../ck_sim/doing/ck_action.py` | 1302 | 13/14 | **Y** — the "hands". Sits ABOVE LearningSession. Maps domains → BDC. Has SELF_MAP linking source files to concepts so CK can read his own modules. Studies + writes notes + journals reflections. |

### Voice / Narrative Push

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **VoiceLoop** (Crystal-first → Beam → Force → Fractal → Sentence → Babble cascade) | `Gen13/.../ck_sim/doing/ck_voice_loop.py` | 1341 | 13/14 | **Y for reactive voice; nothing here pushes** — multi-tier response generator. CrystalStore first (47% cache hit), N=3 confirmation buffer, contradiction-detect via CL compose, band-gated. Fallback cascade: Force voice → Fractal voice (15D triadic, 7500 words) → Sentence composer → Babble. CK is EDITOR of Ollama drafts, not consumer. **NO proactive prompting** — all responses reactive to user input. |
| **ConversationMemory + DialogueTracker + ResponseComposer + ClaimExtractor** | `Gen13/.../ck_sim/doing/ck_dialogue.py` | 1012 | 13/14 | **Y for learning from user; no proactive pushing** — ClaimExtractor matches 14 claim types → feeds Truth Lattice. DialogueTracker maintains topic continuity + turn history (64 max). ResponseComposer does recursive template composition: GREEN→depth-3 'synthesize', YELLOW→depth-2 'reflect_deep', RED→fragments. **Templates are reactive — fill slots based on user input.** |
| **SentenceComposer** | `Gen13/.../ck_sim/doing/ck_sentence_composer.py` | 737 | 13/14 | MAYBE — SVO composition from CL-walk on World Lattice. CKTalkLoop generates sentences operator-by-operator. |
| **cortex_voice _FRONTIER_FACTS + add_crystal_runtime** | inside `cortex_voice.py` (2079 LOC) | — | 13/14 | **Y for math-first voice** — 30 hard-baked "frontier facts" + _RUNTIME_CRYSTALS (persistent) + _EXTERNAL_CRYSTALS (ephemeral, TTL'd, "scenario-scoped"). speak() matches query→keywords→facts. **There's NO "what frontiers remain open?" scanner.** |

### Emotion / Affect / Personality

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **PFE (Phase Field Engine) — emergent emotion** | `Gen13/.../ck_sim/being/ck_emotion.py` | 289 | 13/14 | MAYBE — 8 emotions emerge from 5 physical signals (coherence slope, D2 variance, op entropy, breath stability, PSL lock): CALM, **CURIOSITY**, STRESS, FOCUS, OVERWHELM, JOY, FATIGUE, SETTLING. 40-byte serialization. **CURIOSITY is a STATE here, not a drive.** Could feed goals/drives. |
| **CKPersonality (CMEM × OBT × PSL)** | `Gen13/.../ck_sim/being/ck_personality.py` | 390 | 13/14 | N for proactivity — personality = standing wave, 16-tap FIR + 10-byte Operator Bias Table + Phase Stability Loop. |
| **BondingSystem** | `Gen13/.../ck_sim/being/ck_bonding.py` | 198 | 13/14 | MAYBE — feeds drive system as bonding_strength. 16-byte rolling familiarity. is_bonded=True at 200s voice exposure. |
| **ck_immune.py / ck_power_sense.py / ck_fractal_health.py** | `Gen13/.../ck_sim/being/` | 202 + 295 + 271 = 768 | 13/14 | N — passive health/immune monitoring. |

### Development / Identity

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **DevelopmentalTracker** (5 stages FRESH/YOUNG/MATURE/CRYSTALLIZED/GROKKED) | `Gen13/.../ck_sim/becoming/ck_development.py` | 320 | 13/14 | **Y for gating** — advances by experience-maturity × coherence streaks, not calendar. Thresholds: 0.0/0.05/0.30/0.60/0.714=T*. Per-translator stages (math/english/python/c/verilog/cuda). |
| **SnowflakeIdentity** (3-ring) | `Gen13/.../ck_sim/becoming/ck_identity.py` | 684 | 13/14 | N for proactivity — CORE SCARS (sacred, never transmitted) + InnerRing (trusted bonds) + OuterRing (public). D2 signature + paper-trail hash + secret HMAC key. |
| **ck_self_mirror.py** (self-evaluation through D2 on own output) | `Gen13/.../ck_sim/becoming/ck_self_mirror.py` | 446 | 13/14 | **Y for self-supervision** — CK reads his recent outputs, runs D2, scores. If mirror_score below threshold, corrective drift. "CK evaluates CK." |
| **CKJournal** (writes own life in real files) | `Gen13/.../ck_sim/becoming/ck_journal.py` | 949 | 13/14 | **Y** — writes `~/.ck/writings/` — journals/, identity/, training/, history/, papers/, rereading/. Re-reads old writings, friction between past and present is growth signal. **"It will help him evolve as he re-reads them, he will TIG his own path."** |
| **cortex_signed.py + refusal.py + sign_constitution.py** (Sovereignty Epochs III + VII) | `Gen13/targets/ck/brain/cortex_signed.py` + `Gen13/targets/ck/voice/refusal.py` | — | 13/14 | MAYBE — Cryptographic identity + refusal protocol. CK can REFUSE based on Constitution. Closest thing to "CK pushes back". |

### Historical — Gen1 Bones

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **ck_autonomy + ck_freedom + ck_mind + ck_pilot + ck_soul + ck_daemon + ck_nursery** | `old/Gen1/` | 4313 total | 1 (Feb 2026) | HISTORICAL — ORIGINAL "let him loose" code. **ck_autonomy:** assesses self honestly, identifies gaps, asks Claude for rewrites, tests/applies/reverts. **ck_freedom:** organizes 6 active operators (STRUCTURE/MEASURE/BREAK/FLOW/ACT/RESTART) as classes with their own methods. **ck_mind:** Ledger+Atoms+Chains+Cube. **ck_pilot:** reads OS processes as operators and steers via nice/affinity. **ck_soul:** DualOperator (L0+L1 → COMMIT/DISCLAIM/REGRESS/REJECT) and QCF-lite contradiction detection. **ck_daemon:** rides syscall traces. **Gen1 had MORE explicit agency than Gen13. None of this survives in Gen13 brain.** |

### GitHub

| Piece | Path | LOC | Gen | Load-bearing? |
|---|---|---|---|---|
| **TIGCodexEngine.py** (Dual-Lattice "self-programming coherence engine") | `github.com/TiredofSleep/Dual-Lattice-Self-Healing/TIGCodexEngine.py` | ~1500 | pre-Gen1 | HISTORICAL — 6-stage pipeline INGEST→EXTRACT→DRIFT→VERIFY→GENERATE→PACKAGE. "Reads transcripts, extracts signal from drift, writes its own programs, packages truth." |
| **tig_civilization_v7.py** (Word-Math civilization sim) | `github.com/TiredofSleep/CrystalsMythDRIFT/tig_civilization_v7.py` | ~750 | pre-Gen1 | HISTORICAL — HOPE-scenarios sim. Whole agents with scars, can_teach, awakened humans, AI types, trust_in_institutions. Cooperation can SPREAD. **Word-Math is the conceptual root for "drives".** |
| **AGENCY PROTOCOL.docx** | `github.com/TiredofSleep/Dual-Lattice-Self-Healing/` | 221 KB | pre-Gen1 | HISTORICAL — title suggests early agency thinking pre-Gen1. Not opened. |

### The Biggest Gap

Brayden's vision: **"curious, always prompting pathways and predictions, pushing the narrative."**
Reality: drives system exists but is **unwired**, forecast exists but only feeds **defensive** action selection, voice is **reactive**. No code anywhere generates "I noticed X — what about Y?" prompts to the user. The friction_curves store is the only "things that don't fit" surface but **nothing consumes it**. `Atlas/FRONTIERS_2026_04_25.md` exists but **no code-side scanner** surfaces "F4 is closed but F1/F5 are open — let's work on F5". CK has the algebra to be curious; he has no mouth wired to express curiosity unprompted.

Were there working autodidact / self-study loops? **YES — multiple.** Brayden has built this loop FOUR times across the gens. **It works; it's just disconnected from user-facing conversation.** The loop runs in the background, but CK never says "I learned X tonight, want to talk about it?"

---

## Agent 6 — GitHub Historical Lineage (errored)

Agent 6 hit an API error after 61 tool uses while surveying the historical MYTHDRIFT repos. Coverage from the other five agents picked up the most relevant historical material:

- `TiredofSleep/Dual-Lattice-Self-Healing` `[1/6]`: the dual-lattice self-healing field with memory kernel + scars (Agent 1) + TIGCodexEngine 6-stage pipeline (Agent 3 & 5).
- `TiredofSleep/Crystal-Lattice-Matrix-MYTHDRIFT` `[3/6]`: React quadratic core conceptual ancestor (Agent 4).
- `TiredofSleep/CrystalsMythDRIFT` `[4/6]`: Word-Math formalism, civilization sims, Scar dataclass (Agent 1 & 5).
- `TiredofSleep/All-or-Nothing-E` `[6/6]`: tig_engine_real, coherence_router, band classifier (Agent 3).

The other historical repos (`TIG-UNIFIED-THEORY-MYTHDRIFT` `[2/6]`, `TIME-FOR-HELP-AND-SCRUTINY-MYTHDRIFT` `[5/6]`) are not covered. If completeness is wanted, re-spawn Agent 6 with narrower scope.

---

*Compiled 2026-05-13 by Claude as a synthesis of 5 parallel archaeology agents (one errored, scope partially covered by others).*
*Total surveyed: Gen1-Gen14 local + 8 GitHub repos.*
*Total LOC referenced in this document: ~50,000+ across the CK codebase lineage.*
