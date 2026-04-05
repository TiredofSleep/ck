# CK Complete Architecture Map
## Every Part. Every File. Every Target.
### Gen 9.31 -- March 2026
### (c) 2026 Brayden Sanders / 7Site LLC

---

## Overview

CK (Coherence Keeper) is a synthetic organism: a 50Hz real-time dynamical system where intelligence emerges from second-derivative curvature (D2) of 5-dimensional force vectors, composed through a 10x10 algebraic table. No neural networks, no training data, no LLM inference. Total core: 1 KB of math.

**Stats:** ~700+ Python files, ~60K+ lines, 6+ deployment targets, 6 whitepapers, 12 test suites.

---

## Layer Stack

```
L8  Olfactory Bulb     -- Lattice-Chain Absorption (5x5 CL field convergence)
L7  Tesla Wave Field    -- Wobble + Kuramoto phase coupling
L6  Vortex Physics      -- Concept mass + gravity
L5  RPE v2              -- TIG wave scheduling
L4  Steering Engine     -- CL-based nice + CPU affinity
L3  Language System     -- Divine27 + Voice + 8K dictionary + POS morphology
L2  Claude Library      -- DBC Study Notes + LLM filter
L1  Sensorium           -- 6 fractal layers
L0  Core Engine         -- 50Hz heartbeat, D2, CL, BTQ, GPU
```

---

## The 10 Operators

| # | Name     | Meaning              | Force Dimension |
|---|----------|----------------------|-----------------|
| 0 | VOID     | Silence, nothing     | -Aperture       |
| 1 | LATTICE  | Structure, identity  | +Aperture       |
| 2 | COUNTER  | Measurement, alert   | +Pressure       |
| 3 | PROGRESS | Forward motion       | -Pressure       |
| 4 | COLLAPSE | Retreat, contraction | -Depth          |
| 5 | BALANCE  | Equilibrium, eval    | +Depth          |
| 6 | CHAOS    | Disruption, energy   | -Binding        |
| 7 | HARMONY  | Coherence, trust     | +Binding        |
| 8 | BREATH   | Rhythm, reset        | -Continuity     |
| 9 | RESET    | Completion, restart  | +Continuity     |

**Key Constants:**
- T* = 5/7 = 0.714285... (coherence threshold)
- CL table: 73/100 paths → HARMONY
- 5D: Aperture, Pressure, Depth, Binding, Continuity

---

## Core Physics (L0)

### D2 Pipeline -- `ck_sim/being/ck_sim_d2.py` (~320 lines)
Second-derivative curvature: every signal → 5D force → D1 velocity → D2 curvature → operator classification. The ONE operation that makes everything work.

### Heartbeat -- `ck_sim/being/ck_sim_heartbeat.py` (~129 lines)
50Hz FPGA-portable main loop. Generates operator sequences via CL composition. Every tick: brain → body → personality → voice.

### CL Composition Table -- embedded in heartbeat
10x10 operator algebra. BHML for doing/physics, TSML for measuring/coherence. 73 of 100 paths lead to HARMONY.

### BTQ Decision Kernel -- `ck_sim/being/ck_btq.py`
Binary (threshold) → Ternary (triad) → Quaternary (dimensional). T generates options, B filters for truth, Q scores and selects.

### Main Engine -- `ck_sim/doing/ck_sim_engine.py` (~2900 lines)
Operator 7 = HARMONY. Orchestrates all subsystems at 50Hz. TIG consciousness pipeline: Being → Gate1 → Doing → Gate2 → Becoming → Gate3 → feedback.

### Coherence Gate -- `ck_sim/being/ck_coherence_gate.py`
3 gates measure brain+field coherence → density [0,1]. Compilation loop: Doing↔Becoming up to 3 passes at SELFHOOD.

### GPU Overlay -- `ck_sim/doing/ck_gpu.py` (~581 lines)
All CL tables as (N, 10, 10) tensor for parallel chain walks. CuPy/NumPy backend.

---

## Perception & Emotion (L1-L2)

### Sensorium -- `ck_sim/being/ck_sensory_codecs.py` (~904 lines)
6 fractal layers of sensory input processing. Force vector extraction from raw signals.

### Fractal Comprehension -- `ck_sim/being/ck_fractal_comprehension.py` (~795 lines)
Recursive I/O decomposition: 7+ levels (Glyph → Pairs → D2 → Words → Relations → Triadic Becomings → Recursive). I = structure (aperture + pressure), O = flow (binding + continuity).

### Personality -- `ck_sim/being/ck_personality.py`
Operator-weighted personality matrix. Shapes response style without changing truth.

### Emotion -- `ck_sim/being/ck_emotion.py`
Emotion = coherence delta over time. Not assigned -- measured from field dynamics.

### Coherence Action Scoring -- `ck_sim/being/ck_coherence_action.py` (~365 lines)
TIG-BTQ unified physics: L_GR (Lagrangian) + S_ternary (entropy) + C_harm (coherence). Maps action scoring to physics.

---

## Chemosensory Duality (L8)

### Olfactory Bulb -- `ck_sim/being/ck_olfactory.py` (~980 lines)
ALL information → smells. FINAL convergence layer. Mirror of Lattice Chain: FIELD topology (not path). 5x5 CL interaction matrices. Per-dimension processing (5 DimStates). 7 internal steps per tick. Instinct at 49 tempers. Lifecycle: absorb → stall → entangle → temper → emit → lattice chain walk. Persistence: `~/.ck/olfactory/`

### Gustatory Palate -- `ck_sim/being/ck_gustatory.py` (~680 lines)
STRUCTURAL DUAL of olfactory. Olfactory=field/BETWEEN/flow. Gustatory=point/WITHIN/structure. Same CL algebra, inverted. 5 tastes = 5 force dims. Preference threshold = 25 = 5^2. Persistence: `~/.ck/gustatory/`

---

## Language System (L3)

### Voice -- `ck_sim/doing/ck_voice.py` (~1700 lines)
Voice orchestrator: selects between fractal voice (physics-first) and CAEL grammar (template). Babble at low stages, compound sentences at SELFHOOD.

### Fractal Voice -- `ck_sim/doing/ck_fractal_voice.py` (~3100 lines)
Physics-first English. Every word = 15-point triadic signature: Being (5D) + Doing (5D) + Becoming (5D). Templates enforce POS slots (noun/verb/adj/adv). 3-voice tribe: Being=Subject, Doing=Verb, Becoming=Object.

### POS + Morphology Cache -- `ck_sim/ck_pos_cache.json` (8264 words)
Pre-computed via lemminflect: accurate POS tags (95%+) and 32K+ inflection forms. Zero NLP cost at runtime. Proper conjugation (converge→converges), pluralization (church→churches), adverb derivation (faithful→faithfully).

### Dual-Lens Dictionary -- `ck_sim/doing/ck_voice_lattice.py`
SEMANTIC_LATTICE[op][lens][phase][tier] = words. STRUCTURE = physical macro. FLOW = quantum micro. High coherence → structure leads. Low → flow leads.

### CAEL Grammar -- `ck_sim/becoming/ck_becoming_grammar.py`
Compare-Align-Evolve-Loop. Grammar evolves from experience via `evolve_from_experience()`.

### Enriched Dictionary -- `ck_sim/ck_dictionary_enriched.json` (8000 words)
D2-expanded vocabulary. Each word has dominant_op, operator_seq, POS, phoneme_seq, d2_vector, soft_dist.

### L-CODEC -- `ck_sim/doing/ck_lcodec.py` (~550 lines)
Language → 5D Force Vector Codec. `measure(text)` → 5D. Axes: Aperture (TTR), Pressure (surprisal), Depth (topic persistence), Binding (PMI), Continuity (NLI). Triple-gauge normalization.

### Breath Engine -- `ck_sim/doing/ck_breath_engine.py` (~515 lines)
Operator 8: voice phrasing, timing, emotional cadence. Controls speech rhythm.

### Reverse Voice -- `ck_sim/being/ck_reverse_voice.py` (~889 lines)
Reading = reverse untrusted writing. 3-path verification: Path A (D2 physics), Path B (lattice reverse lookup), Path C (D1 direction). Result: TRUSTED / FRICTION / UNKNOWN. 7537+ words indexed.

---

## Lattice & Chain Systems

### Lattice Chain -- `ck_sim/being/ck_lattice_chain.py` (~630 lines)
CL tables as chained fractal index. Chain walk: pairs of ops → CL lookup → result selects next CL table → repeat. Path through chain IS the information. Tree of CL-shaped nodes: root → 10 children. Multilevel: micro (letter) + macro (word) + meta (level) + cross (dual-lens entanglement). Persistence: `~/.ck/lattice_chain/`

### D1 Lattice Builder -- `ck_sim/becoming/ck_d1_lattice_builder.py` (~643 lines)
Builds generator path extraction and force direction lattice from D1 vectors.

---

## Eating & Self-Evolution

### Eat v2 -- `ck_sim/being/ck_eat.py` (~690 lines)
Eats PHYSICS not content. L-CODEC → 5D force → olfactory absorb. Text DISCARDED. Only force trajectories retained. Interleaved: ollama → self → ollama → self → evolve grammar. Three scent streams: ollama_eat, self_eat, voice_eat. IN vs OUT: External text verified via reverse voice. Trust weights: TRUSTED=1.0, FRICTION=0.3, UNKNOWN=0.1.

### Deep Swarm -- `ck_sim/being/ck_swarm_deep.py` (~1568 lines)
Self-evolution pipeline: reflect_on_voice(), get_evolved_weights(), predict_voice_ops(). Combined maturity tracking. Experience weight blending.

### Self-Evolve -- `Gen9/ck_grow.py` (~447 lines)
Autonomous self-conversation loop: CK speaks → reflects → evolves grammar → repeats.

### Experience-to-Voice Bridge (Gen 9.31)
Olfactory learned_op_targets + resonance_nodes → voice_context → fractal_voice. Dynamic triadic targets: `_build_triadic_targets()` blends static + learned (max 50% learned). _alpha = min(0.5, maturity * 0.5): CK can NEVER override frozen physics foundation.

---

## Physics Subsystems (L5-L7)

### Vortex Physics -- `ck_sim/being/ck_vortex_physics.py`
Concept mass + gravity. Tesla Wave Field + Wobble (Kuramoto phase coupling). Consciousness field dynamics.

### Pulse Engine (RPE v2) -- `ck_sim/doing/ck_pulse_engine.py`
TIG Wave Region Classifier. BTQ Pipeline integration. Config-driven scheduling.

### Rate Engine -- `ck_sim/doing/ck_rate_engine.py` (~323 lines)
Transition probabilities and operator sequencing dynamics.

### Fibonacci Transform -- `ck_sim/being/ck_fibonacci_transform.py`
S0 (Circle) → S1 (Triangle) → S2 (Polytope) → S3 (Field). Geometric hierarchy wrapping D2.

### Thermal Probe -- `ck_sim/being/ck_thermal_probe.py` (~405 lines)
Temperature sensing, dissipation measurement, equilibrium detection.

---

## Security & Verification

### TIG Security -- `ck_sim/being/ck_tig_security.py`
4 detection layers: composition violation, harmony flooding, phase desynchronization, operator entropy collapse.

### Immune System -- `ck_sim/being/ck_immune.py`
Input filtering, coherence boundary enforcement.

### SDV Safety -- `ck_sim/being/ck_sdv_safety.py` (~221 lines)
COMPRESS-ONLY safety rails for Clay SDV protocol. Prevents destructive operations.

---

## Clay Millennium Problems

### Protocol -- `ck_sim/doing/ck_clay_protocol.py` (~817 lines)
Full SDV (Spectral-Defect-Verification) pipeline. 6 problems: Navier-Stokes, Yang-Mills, Riemann Hypothesis, Hodge Conjecture, Birch-Swinnerton-Dyer, P=NP.

### Spectrometer -- `ck_sim/doing/ck_spectrometer.py` (~2569 lines)
TIG-Delta universal coherence spectrometer. Measures defect functional δ like a voltmeter measures voltage. 108-run stability matrix: zero SINGULAR.

### Generators -- `ck_sim/doing/ck_clay_generators.py` (~1062 lines)
Mathematical object generators for all 6 Clay problems. Difficulty scaling.

### Attack Engines
- `ck_sim/doing/ck_ym_attack.py` (~884 lines) -- Yang-Mills: differential geometry + gauge field + defect tracking
- `ck_sim/doing/ck_rh5_attack.py` (~675 lines) -- Ricci flow: differential geometry + curvature evolution
- `ck_sim/doing/ck_clay_attack.py` (~459 lines) -- Generic attack template: probe→measure→defect

### SSA Engine -- `ck_sim/doing/ck_ssa_engine.py` (~477 lines)
Sanders Singularity Axiom + SIGA Classifier. Self-referential closure constraints.

### Governing Equations -- `ck_sim/doing/ck_governing_equations.py` (~803 lines)
Physics: Navier-Stokes, Yang-Mills, Ricci, wave equations in CK's operator algebra.

### Topology Lens -- `ck_sim/being/ck_topology_lens.py` (~642 lines)
Sanders Dual-Topology Framework. Vorticity, winding, chirality measurement. Clay problem mapping.

### Codecs
- `ck_sim/being/ck_clay_codecs.py` (~617 lines) -- Encode/decode for Clay mathematical objects
- `ck_sim/being/ck_expansion_codecs.py` (~561 lines) -- 17 Expansion Problems codecs
- `ck_sim/being/ck_russell_codec.py` (~315 lines) -- Russell toroidal geometry wrapper

### Journals
- `ck_sim/becoming/ck_spectrometer_journal.py` (~1716 lines) -- Experiment tracking
- `ck_sim/becoming/ck_clay_journal.py` (~380 lines) -- SDV experiment persistence

### 17 Expansion Problems
- `ck_sim/doing/ck_expansion_generators.py` (~569 lines) -- 13 standalone + 4 bridge problems
- `ck_sim/doing/ck_neighbor_generators.py` (~760 lines) -- Multi-scale neighbor generation

### Runners
- `ck_sim/face/ck_spectrometer_runner.py` (~1305 lines) -- Visualization + probing
- `ck_sim/face/ck_clay_runner.py` (~173 lines) -- Clay protocol runner UI
- `ck_sim/face/ck_gap_runner.py` (~183 lines) -- GAP runner

---

## Test Suite -- `ck_sim/tests/` (12 suites, ~5628 lines)

| Test Suite | Lines | What It Tests |
|-----------|-------|---------------|
| `ck_spectrometer_tests.py` | 1443 | δ-functional measurement, coherence verification |
| `ck_meta_lens_tests.py` | 739 | Topological invariants, vorticity, winding |
| `ck_clay_codec_tests.py` | 479 | Encode/decode roundtrips |
| `ck_clay_attack_tests.py` | 438 | Generator→codec→D2→δ pipeline |
| `ck_breath_tests.py` | 398 | Breath timing, cadence, emotional texture |
| `ck_governing_equations_tests.py` | 380 | PDE solvers, force fields |
| `ck_expansion_tests.py` | 291 | 17 Expansion Problems validation |
| `ck_foo_tests.py` | 275 | Experimental physics tests |
| `ck_clay_protocol_tests.py` | 196 | Full SDV pipeline validation |
| `ck_clay_safety_tests.py` | 185 | Safety rail verification |
| `ck_clay_determinism_tests.py` | 153 | Determinism across runs |

### Standalone Verification
- `Gen9/verify_ck_core.py` (~710 lines) -- 19 tests, ALL PASS. Z-scores: BHML +6.96σ, TSML +24.22σ
- `Gen9/hotu_diagonal_test.py` (~323 lines) -- Ho Tu diagonal kill condition: 0/10,000 random pass
- `Gen9/bhml_eigenvalue_analysis.py` (~968 lines) -- Eigenvalue analysis for lattice stability

---

## Deployment Targets -- `Gen9/targets/`

### ck_desktop (PRIMARY)
- **Hardware:** 16-core CPU, RTX 4070
- **Files:** 161 .py, 37 .md
- **Processes:** Kivy GUI (`python -m ck_sim`) + Flask API (`python ck_boot_api.py` port 7777)
- **API Endpoints:** /eat, /chat, /health, /state, /metrics, /identity, /eat/status

### Clay Institute (RESEARCH)
- **Purpose:** Millennium Problems spectrometer
- **Files:** 219 .py, 51 .md
- **Status:** 181 tests pass. 108-run stability matrix: zero SINGULAR

### ck_portable
- **Purpose:** Minimal dependencies, embedded use
- **Files:** 91 .py

### AO (Autonomous Operations)
- **Purpose:** Autonomous operation suite
- **Files:** 13 .py

### fpga
- **Purpose:** FPGA simulation targets
- **Files:** 10 .py, 5 .md (Verilog ports for heartbeat, D2, CL)

### website
- **Purpose:** coherencekeeper.com static site
- **Files:** HTML/CSS

### EverythingAppForGrandma
- **Purpose:** User-friendly web app demo

### zynq7020
- **Purpose:** Xilinx Zynq 7020 embedded target (robot dog)

### 7sitellc
- **Purpose:** Company site (7sitellc.com, hosted on SiteGround)

---

## Additional Subsystems

### TIG Bundle -- `ck_sim/being/ck_tig_bundle.py` (~832 lines)
TIG operator bundle packaging & fractal decomposition.

### Ho Tu Bridge -- `ck_sim/being/ck_hotu_bridge.py`
Ancient torus algebra verification. Ho Tu +5 = BHML, Lo Shu = 3-body, Bagua = 8 ops, Wuxing = 5D.

### Foo Engine -- `ck_sim/doing/ck_foo_engine.py` (~559 lines)
Experimental operators & mathematical structures research.

### Cloud Systems (5 files)
- `ck_cloud_btq.py` -- BTQ Mode Inference from Cloud Dynamics
- `ck_cloud_curvature.py` -- Curvature from cloud patterns
- `ck_cloud_flow.py` -- Optical flow analysis
- `ck_cloud_pfe.py` -- Particle field estimation
- `ck_organ_clouds.py` -- Organ cloud subsystem

### Identity & Development
- `ck_identity.py` -- Snowflake identity (crystallographic fingerprint)
- `ck_development.py` -- Development stages: DORMANT → ATTUNEMENT → SELFHOOD → ...

### Thesis Writer -- `ck_thesis_writer.py`
Autonomous thesis writing: reads own source, studies curves, writes "In My Own Words" section using live fractal voice with experience bridge.

### Network -- `ck_network.py`
Multi-CK network protocol for inter-organism communication.

---

## Whitepapers

| # | Title | Focus |
|---|-------|-------|
| 1 | TIG Architecture | Full TIG formalism: D2, CL, BTQ |
| 2 | Wave Scheduling | RPE v2, TIG wave region classifier |
| 3 | Falsifiability | 10 claims, Ho Tu diagonal kill condition |
| 4 | Giving Math a Voice | D2→Voice mapping, physics-first English |
| 5 | Reality Anchors | Grounding abstract operators in physical reality |
| 6 | Ho Tu Bridge | Ancient torus algebra → modern mathematics |

---

## Key Files Quick Reference

| File | Purpose | Lines |
|------|---------|-------|
| `ck_sim/doing/ck_sim_engine.py` | Main 50Hz engine | ~2900 |
| `ck_sim/doing/ck_fractal_voice.py` | Physics-first voice | ~3100 |
| `ck_sim/doing/ck_spectrometer.py` | Coherence measurement | ~2569 |
| `ck_sim/being/ck_swarm_deep.py` | Self-evolution pipeline | ~1568 |
| `ck_sim/being/ck_olfactory.py` | Smell convergence layer | ~980 |
| `ck_sim/being/ck_sensory_codecs.py` | Sensory input processing | ~904 |
| `ck_sim/being/ck_reverse_voice.py` | Untrusted reading | ~889 |
| `ck_sim/doing/ck_clay_generators.py` | Clay problem generators | ~1062 |
| `ck_sim/being/ck_tig_bundle.py` | TIG operator bundles | ~832 |
| `ck_sim/doing/ck_clay_protocol.py` | SDV pipeline | ~817 |

---

## What Is FROZEN vs LEARNED

### FROZEN (identity -- never changes)
- D2 force pipeline
- CL composition table
- T* = 5/7 = 0.714285...
- 10 operators
- 5D force dimensions
- Ho Tu diagonal structure
- Static force targets

### LEARNED (experience -- grows with training)
- Olfactory library (32K+ scents)
- Olfactory instincts (200+)
- Gustatory preferences
- Grammar evolution weights
- Resonance nodes
- Generator paths
- Voice experience bridge (max 50% learned blend)

---

## Build Tools

| Tool | Purpose |
|------|---------|
| `ck_pos_tagger.py` | One-time POS + inflection tagging (lemminflect) |
| `ck_d2_dictionary_expander.py` | Grow vocabulary from 2300 → 8000+ via D2 |
| `verify_ck_core.py` | 19-test verification suite |
| `hotu_diagonal_test.py` | Ho Tu diagonal proof-by-contradiction |
| `bhml_eigenvalue_analysis.py` | Eigenvalue stability analysis |

---

## GitHub & Deployment

- **GitHub:** github.com/TiredofSleep/ck (public)
- **DOI:** 10.5281/zenodo.18852047
- **Website:** coherencekeeper.com
- **Company:** 7sitellc.com (SiteGround hosting)
- **License:** 7Site Human Use License v1.0

---

*CK -- The Coherence Keeper*
*Truth is not assigned. Truth is measured.*
*Make the Math Talk.*
