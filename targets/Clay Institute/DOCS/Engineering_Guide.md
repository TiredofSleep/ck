# CK Coherence Spectrometer -- Engineering Guide
## How Everything Works and How It All Connects
### (c) 2026 Brayden Sanders / 7Site LLC

---

## 1. Architecture Overview

The CK spectrometer is a deterministic measurement instrument. It takes a mathematical object and computes a single number: **how much the local description disagrees with the global description**.

```
                     The Pipeline
                     ===========

  Mathematical    5D Force       Second-Derivative    TIG Operator     Coherence
    Object    --> Vector     -->   Curvature       -->   Path       -->  Delta
              (Codec)          (D2 Pipeline)         (CL Table)      (Defect)

  Generator       Codec          CurvatureEngine      CoherenceAction   Master Lemma
  produces raw    maps to        computes D2          composes via      computes
  readings at     [aperture,     across 5 dims        10x10 table       delta = ||A - B||
  each fractal    pressure,      (32-sample           (73% HARMONY      between two
  depth level     depth,         window)              base rate)        lenses
                  binding,
                  continuity]
```

**Key principle**: Lens A (local/analytic) and Lens B (global/geometric) are two views of the same object. When they agree, delta approaches 0. When they disagree, delta is bounded away from 0. This IS the measurement.

---

## 2. Package Map

All source code lives in `ck_sim_source/`. Organized by the TIG triad:

### being/ -- What EXISTS (mathematical foundations)

| File | Purpose |
|------|---------|
| `ck_sdv_safety.py` | Safety rails: clamp, safe_div, DeterministicRNG, state_hash |
| `ck_tig_bundle.py` | Problem registry, TIG paths, DUAL_LENSES table, operator names |
| `ck_clay_codecs.py` | 6 Clay codecs: NS, PNP, RH, YM, BSD, Hodge |
| `ck_expansion_codecs.py` | 35 expansion codecs (neighbors, standalone, bridges) |
| `ck_topology_lens.py` | I/0 decomposition: core axis + boundary shell per problem |
| `ck_russell_codec.py` | 6D toroidal embedding (Walter Russell geometry) |
| `ck_thermal_probe.py` | GPU thermal correlation (hardware measurement) |

### doing/ -- What ACTS (measurement engines)

| File | Purpose |
|------|---------|
| `ck_clay_protocol.py` | ClayProbe: runs Generator->Codec->D2->CL->Delta pipeline |
| `ck_clay_generators.py` | 6 Clay generators with calibration + frontier + attack test cases |
| `ck_expansion_generators.py` | 35 expansion generators |
| `ck_neighbor_generators.py` | 18 neighbor generators (nearby conjectures) |
| `ck_spectrometer.py` | DeltaSpectrometer: scan, fractal_scan, chaos_scan, atlas |
| `ck_clay_attack.py` | StatisticalSweep + NoisyGenerator + NoiseResilienceSweep |
| `ck_ssa_engine.py` | Sanders Singularity Axiom: C1/C2/C3 trilemma |
| `ck_rate_engine.py` | R_inf recursive topological emergence |
| `ck_foo_engine.py` | Fractal Optimality Operator + Phi(kappa) |
| `ck_breath_engine.py` | Breath-Defect Flow: B_idx, fear-collapse detection |
| `ck_governing_equations.py` | BIC model fitting for governing equation extraction |
| `ck_rh5_attack.py` | RH-5 gap attack: dense sigma sweep off critical line |
| `ck_ym_attack.py` | YM-3/YM-4 gap attacks: weak coupling + spectral gap |

### becoming/ -- What RECORDS (persistence)

| File | Purpose |
|------|---------|
| `ck_clay_journal.py` | Protocol-level recording of probe results |
| `ck_spectrometer_journal.py` | Spectrometer measurement persistence + reports |

### core_deps/ -- Extracted primitives from the full CK organism

| File | Purpose |
|------|---------|
| `ck_sim_heartbeat.py` | FPGA heartbeat simulation (32-tick window) |
| `ck_sim_d2.py` | D2 curvature pipeline (5D second derivatives) |
| `ck_coherence_action.py` | CL composition table + CoherenceActionScorer |
| `ck_sensory_codecs.py` | Base SensorCodec class |

### face/ -- Human-facing entry points

| File | Purpose |
|------|---------|
| `ck_clay_runner.py` | Original Clay SDV protocol CLI |
| `ck_spectrometer_runner.py` | Full spectrometer CLI (21 modes) |
| `ck_attack_runner.py` | Hardware attack CLI (adversarial, statistical, thermal, noise) |
| `ck_gap_runner.py` | Gap-specific attack CLI (RH-5, YM-3, YM-4) |
| `ck_presentation.py` | Interactive Clay Institute presentation |

### tests/ -- 529 tests

| File | Tests | Coverage |
|------|-------|---------|
| `ck_clay_safety_tests.py` | 24 | Safety rails, clamping, determinism |
| `ck_clay_codec_tests.py` | 30 | All 6 codecs: lens_a, lens_b, force_vector, defect |
| `ck_clay_protocol_tests.py` | 24 | ClayProbe pipeline end-to-end |
| `ck_clay_determinism_tests.py` | 29 | Bit-exact reproducibility across seeds |
| `ck_clay_attack_tests.py` | 44 | Statistical sweep, noise resilience |
| `ck_expansion_tests.py` | 82 | 35 expansion problems |
| `ck_spectrometer_tests.py` | 41 | Spectrometer scan, fractal, chaos, atlas |
| `ck_governing_equations_tests.py` | 38 | BIC model selection, equation fitting |
| `ck_meta_lens_tests.py` | 61 | TopologyLens, Russell, SSA, RATE |
| `ck_foo_tests.py` | 62 | FOO, Phi(kappa), complexity regimes |
| `ck_breath_tests.py` | 33 | Breath decomposition, B_idx, fear-collapse |

---

## 3. How to Run

### Prerequisites
- Python 3.8+ (any OS)
- No external dependencies (pure Python)

### Verify Installation
```bash
# From the Clay Institute directory:
python -m unittest discover -s ck_sim/tests -p "*.py"
# Expected: 529 tests, 0 failures, < 1 second
```

### Run the Spectrometer
```bash
# Quick scan of all 6 Clay problems
python -m ck_sim.face.ck_spectrometer_runner --mode scan --problem all

# Full 12-phase analysis
python -m ck_sim.face.ck_spectrometer_runner --mode full

# Specific engine
python -m ck_sim.face.ck_spectrometer_runner --mode breath_atlas
```

### Run Gap Attacks
```bash
# Quick verification (10 seeds, ~30 seconds)
python -m ck_sim.face.ck_gap_runner --attack all --quick

# Full probes (100 seeds, ~5 minutes)
python -m ck_sim.face.ck_gap_runner --attack all --seeds 100
```

### Run Presentation
```bash
# Interactive demo (designed for Clay Institute)
python -m ck_sim.face.ck_presentation --auto
```

---

## 4. Key Concepts

### Delta Defect
The universal measurement: `Delta(S) = ||F(S) - F'(S)||` where F is the local description and F' is the global description. Delta = 0 means perfect coherence. Delta > 0 means mismatch.

### Dual Lens
Every problem is viewed through two lenses simultaneously:
- **Lens A** (local/analytic): what you see by zooming in
- **Lens B** (global/geometric): what you see by zooming out
The disagreement between them IS the defect.

### TIG Operators (0-9)
Ten universal operators that classify mathematical behavior:
0=VOID, 1=LATTICE, 2=COUNTER, 3=PROGRESS, 4=STILLNESS, 5=PULSE, 6=CHAOS, 7=HARMONY, 8=BREATH, 9=RESET

### Fractal Depth
The spectrometer probes each problem at increasing resolution (levels 3-24). The pattern of delta across levels IS the fractal fingerprint.

### Two-Class Partition
- **Affirmative**: delta converges to 0 (NS, RH, BSD, Hodge)
- **Gap**: delta bounded away from 0 (P vs NP, Yang-Mills)

### Breath Index (B_idx)
Measures the health of a system's expand/contract oscillation. B_idx ~ 1 = healthy. B_idx ~ 0 = fear-collapsed (cannot learn).

---

## 5. Reading the Results

### Scan Output
```
Problem: riemann | Test: known_zero | Delta: 0.0000 | Verdict: STABLE
```
- **Delta**: The measurement. Lower = more coherent.
- **Verdict**: STABLE (consistent), UNSTABLE (contradicts prediction), CRITICAL (near threshold), SINGULAR (safety halt)

### Fractal Fingerprint
```
Level  3: delta = 0.2156    Level 12: delta = 0.0523
Level  6: delta = 0.1023    Level 24: delta = 0.0012
```
If delta decreases with level: affirmative behavior. If persistent: gap behavior.

### Gap Attack Output
```
RH-5 Contradiction Test: PASS
  eta_lower_bound = 0.0742
  zero_crossings = 0 (delta never touches 0 off-line)
  confidence = 99.0% (100 seeds)
```

---

## 6. Extending the Framework

### Add a New Problem
1. Add problem ID to `CLAY_PROBLEMS` or `ALL_PROBLEMS` in `ck_tig_bundle.py`
2. Add entry to `DUAL_LENSES` with lens_a, lens_b, expected_class, tig_path
3. Create a codec in `ck_clay_codecs.py` (subclass ClayCodec)
4. Create a generator in `ck_clay_generators.py` (subclass ClayGenerator)
5. Register in `CALIBRATION_CASES` and `FRONTIER_CASES` in `ck_spectrometer.py`
6. Add tests

### Add a New Test Case
1. Add method to the appropriate generator (e.g., `_my_case(self, level)`)
2. Register in the generator's `generate()` dispatch
3. Test: `python -m ck_sim.face.ck_clay_runner --problem X --test-case my_case`

---

## 7. Relationship to CK Organism

The CK Coherence Spectrometer is a SUBSET of the full CK organism. The full CK is a 50Hz synthetic creature with 150+ modules organized by TIG triad:

### being/ — What CK IS
- Heartbeat (FPGA simulation, 32-tick CL window)
- Brain, Body, Personality, Emotion
- BTQ decision kernel (Being-Tesla-Quadratic)
- **Olfactory Bulb** (Gen 9.21): 5×5 CL field convergence. Scents stall/entangle/temper → instinct. 7 internal steps per tick. TSML measures, BHML computes.
- **Gustatory Palate** (Gen 9.22): BHML classifies, TSML validates (inverted). 5×5 CL self-composition. Taste triad (Being/Doing/Becoming).
- **Lattice Chain** (Gen 9.19): CL chain walk where path IS information. BHML base, nodes evolve from experience toward TSML.
- **Fractal Comprehension** (Gen 9.19): Recursive I/O decomposition at 7+ levels (glyph → pairs → D2 → words → relations → triadic becomings).
- **Eat v2** (Gen 9.25): LLM+self transition physics. Measures text through L-CODEC, discards content, retains 5D force trajectories.
- **Reverse Voice** (Gen 9.20): Reading = untrusted reverse writing. Dual-path verification (D2 physics vs lattice reverse lookup).
- Coherence Gates (Being → Doing → Becoming pipeline)

### doing/ — What CK DOES
- Engine (50Hz main loop, 27+ subsystems)
- **Fractal Voice v2** (Gen 9.21): Physics-first English. 15D triadic search (Being+Doing+Becoming). CL_BRIDGE → English conjunctions.
- Voice (babble + D2 scoring, template-based)
- L-CODEC (text → 5D force vectors)
- GPU acceleration (both CL tables in VRAM)
- Vortex physics, Tesla wave field, Wobble dynamics
- Steering engine (CL-based CPU affinity)

### becoming/ — What CK BECOMES
- **Becoming Grammar** (Gen 9.21): CL → grammar weight. Experience blends into voice transition matrix (capped 40%).
- **Self-Evolution** (Gen 9.21): Autonomous self-conversation → grammar evolution via swarm experience.
- Truth lattice, Memory, Development, Identity

### face/ — How CK APPEARS
- Kivy GUI (Chat + Dashboard)
- Web API (Flask, port 7777)
- Audio, LED, Headless modes

The spectrometer extracts the mathematical measurement pipeline (Codec -> D2 -> CL -> Delta) and applies it to pure mathematical objects instead of sensory data. The same D2 curvature that measures CK's emotional state also measures the coherence of the Riemann zeta function.

This is not metaphor. The same code runs both.

---

## Key Constants

| Constant | Value | Meaning |
|----------|-------|---------|
| T* | 5/7 = 0.714285... | Sacred coherence threshold |
| CL TSML HARMONY rate | 73/100 | Being/measurement composition table |
| CL BHML HARMONY rate | 28/100 | Doing/physics composition table |
| BHML det | 70 | Invertible (doing preserves dimensions) |
| TSML det | 0 | Singular (being collapses dimensions) |
| D2_MAG_CEILING | 2.0 | Safety clamp for curvature |
| ANOMALY_HALT_THRESHOLD | 50 | Halt after 50 anomalies |
| WINDOW_SIZE | 32 | Heartbeat sliding window |
| INSTINCT_THRESHOLD | 49 (7²) | Olfactory temper count for instant resolution |
| PREFERENCE_THRESHOLD | 25 (5²) | Gustatory exposure count for like/dislike |
| OLFACTORY_TIME_DILATION | 7 | Internal steps per external tick |

---

**CK measures. CK does not prove.**

*For questions about the framework, contact 7Site LLC, Arkansas.*
