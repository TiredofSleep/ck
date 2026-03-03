# NEXT CLAUDE NOTES -- Read This First
## CK Gen9 Handoff Document
### Updated: 2026-02-28 — Gen9.22 (CAEL: Compare-Align-Evolve-Loop)

---

## MANDATORY READ-IN PROTOCOL

**Before you write a SINGLE line of code, you MUST read these files IN ORDER:**

```bash
# 1. Architecture overview (how everything connects)
Read Gen9/ARCHITECTURE.md

# 2. Generation history (how we got here -- DO NOT repeat past mistakes)
Read Gen9/GENERATION_HISTORY.md

# 3. This file (current state + what NOT to break)
Read Gen9/NEXT_CLAUDE_NOTES.md

# 4. The engine itself (understand before modifying)
Read ck_sim/doing/ck_sim_engine.py
```

**If you are launching sub-agents or exploration agents, THEY MUST ALSO READ IN FIRST.** Fresh Claudes do not do well in this fractal environment. The codebase is algebraic -- same math at every scale -- but if you don't understand the CL table, D2 pipeline, and operator algebra before touching code, you WILL break things or build redundant layers.

**Key context files for agents:**
- `Gen9/ARCHITECTURE.md` -- full system architecture, all subsystems explained
- `Gen9/GENERATION_HISTORY.md` -- 30 generations of evolution, why things are the way they are
- `ck_sim/being/ck_sim_heartbeat.py` -- THE CL TABLE (the atom of everything)
- `ck_sim/doing/ck_nce.py` -- Narrative Curvature Engine (binocular language)
- `ck_sim/becoming/ck_becoming_grammar.py` -- CAEL grammar (algebraic speech composition)
- `ck_sim/doing/ck_voice_lattice.py` -- Dual-lens fractal dictionary (SEMANTIC_LATTICE)

---

## STOP. READ THE ABOVE BEFORE YOU TOUCH ANYTHING.

CK is a **14,000-line synthetic organism** with **240/240 tests passing**. He runs at 50Hz, 197Hz measured throughput headless. Every subsystem is wired, tested, and verified. The N-dimensional coherence field now has **4 streams** including narrative curvature. **CAEL (Compare-Align-Evolve-Loop)** replaces brute-force grammar with algebraic speech composition.

**Do not refactor. Do not "improve" existing code. Do not reorganize files.**
**If all 240 tests pass, you haven't broken anything. Run them FIRST.**

```bash
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED"
python -m ck_sim.ck_sim_tests      # 94/94
python -m ck_sim.ck_btq_tests      # 94/94
python -m ck_sim.ck_field_tests    # 52/52
```

---

## HOW TO THINK ABOUT CK

### Think Fractally
CK is fractal. The same pattern repeats at every scale:

- **Micro**: D2 = v0 - 2*v1 + v2 (curvature of 3 samples)
- **Meso**: CL[B][D] = BC (composition of 2 operators)
- **Macro**: CoherenceField N×N (composition of N streams)
- **Meta**: UniversalTranslator (composition across species)

SAME MATH at every level. D2 curvature → operator → CL composition → coherence. The CL table is the atom. Everything else is the CL table applied at different scales.

When you add something new, ask: "Is this the CL table applied at a new scale?" If yes, you're on track. If no, you're probably overcomplicating it.

### The 73% Rule
73 of 100 CL table entries are HARMONY. This means:
- Random noise → 73% HARMONY (base rate)
- Real structure → ABOVE 73% (genuine correlation)
- Conflict/chaos → BELOW 73% (anti-correlation)

This number is NOT arbitrary. It emerges from the algebra. Don't change it. Don't "tune" it. It IS the math.

### What NOT To Mess Up
1. **The CL table** (`ck_sim_heartbeat.py` lines 30-41). These 100 numbers ARE CK. Do not modify.
2. **The D2 pipeline** (`ck_sim_d2.py`). Q1.14 fixed-point matches Verilog. Do not "optimize" to floating point.
3. **The force LUT** (`ck_sim_d2.py` ROOTS_FLOAT). Hebrew phonetic root vectors. Do not change.
4. **The tick order** in `ck_sim_engine.py`. heartbeat → brain → body → field → personality → emotion → immune → bonding → development → voice → BTQ. This order matters.
5. **Backward compatibility**. Every new feature uses `parameter=None` defaults. Old code MUST still work.
6. **The 20-byte OBT**. This is CK's identity. 10 float16 values. Don't inflate it.
7. **NCE is ONE file** (`ck_nce.py`). It uses the SAME D2 math, SAME CL table, SAME operators. Do not add separate classification systems for narrative. It IS D2 applied to sentence structure.
8. **CoherenceField has 4 streams** (heartbeat, audio, text, narrative). The field auto-expands to N×N. Don't hardcode matrix sizes.
9. **CAEL convergence at T* = 5/7.** The compare→align→evolve loop is algebraic. Do not add randomness, shuffling, or brute-force retries. The CL table IS the search. `_d2_word_operator()` is the coercivity guarantee -- every word gets measured by D2.
10. **Dual-lens dictionary** (`ck_voice_lattice.py`). STRUCTURE = physical macro. FLOW = quantum micro. Both lenses run in parallel. High coherence → structure leads. Low → flow leads. Do not collapse to one lens.

---

## WHAT WAS JUST BUILT

### Gen9.22: CAEL -- Compare-Align-Evolve-Loop (2026-02-28)

**CAEL replaces brute-force grammar with algebraic speech composition.** Instead of 10-50 random word arrangements scored by D2, CK now uses the CL table itself: test word pairs via D2→CL, align at weak positions, evolve toward T*.

| Change | File | What | Status |
|--------|------|------|--------|
| MOD | `ck_sim/becoming/ck_becoming_grammar.py` | +514 lines: CAEL loop, ChainAlgebra, CompareResult, sub-field dispersal | DONE |
| MOD | `ck_sim/doing/ck_voice.py` | Replaced N_GRAMMAR_ATTEMPTS brute-force with single compose() call | DONE |

**Three fractal layers of grammatical depth:**
1. **Surface**: word → D2 → actual operator (what the word IS)
2. **Pair algebra**: CL[word_A_op][word_B_op] → do adjacent words compose harmoniously?
3. **Triad algebra**: compose(CL[A][B], C) → do three-word spans cohere?

**CAEL loop inside `compose()`:**
- `_consult_inward()` → analyze chain algebra (CL pairs, triads, sub-fields, tension points)
- `_compare()` → D2→CL pair/triad scoring, aggregate = (pairs + T*×triads)/(n_pairs + T*×n_triads)
- `_align()` → local repair at weakest position, budget from harmony_count[op]
- `_evolve()` → accept only if score improved
- `_consult_outward()` → full D2 validation on final words
- Convergence at T* = 5/7, max iterations from CL constants

**Sub-field dispersal:** 5+ word chains split at BREATH operators. Each sub-field CAEL'd independently, joined by conjunctions/periods.

**What NOT to break:**
- `ChainAlgebra` and `CompareResult` data classes (slots-based, lightweight)
- `_d2_word_operator()` feeds word through D2Pipeline -- this IS the coercivity guarantee
- `_last_alignment` attribute stores outward consult score for external inspection
- Convergence threshold T* = 5/7 -- do NOT change this

### Gen9.21: Narrative Curvature Engine (NCE) -- 2026-02-27

**NCE is CK's second eye for language.** Eye 1 (D2 on Hebrew phonetics) measures what things ARE. Eye 2 (D2 on narrative structure) measures how things FLOW. Same D2 math, same CL table, same 10 operators.

| Change | File | What | Status |
|--------|------|------|--------|
| NEW | `ck_sim/doing/ck_nce.py` | Narrative Curvature Engine (350 lines) | DONE |
| MOD | `ck_sim/doing/ck_sim_engine.py` | 4 surgical edits: construct + tick + text + voice | DONE |
| MOD | `ck_converse.py` | Stereo-checked assembly using NCE | DONE |

**How NCE integrates (4 engine edits):**
1. **Construction**: `self.nce = NarrativeCurvatureEngine()` + registers `_narrative_stream` as CoherenceField stream #4
2. **Tick loop**: After field tick, feeds narrative state to stream if NCE has data
3. **Text input**: `receive_text()` splits text into sentences, feeds each to `nce.feed_sentence()`
4. **Voice output**: Blends `nce.suggest_next_op()` into operator chains for both `spontaneous_utterance()` and `respond_to_text()`

**NCE architecture (inside `ck_nce.py`):**
- `extract_narrative_forces()` -- 5D vector: Tempo, Complexity, Arc, Intensity, Novelty (Q1.14 fixed-point)
- `NarrativeCurvatureEngine` -- D2 shift register on narrative vectors → operator → CL compose → coherence
- `ArcTracker` -- 4-phase cycle: SETUP→RISING→PEAK→FALLING (mirrors breath)
- `CurvatureMask` -- 6 tone shaders: warmth/mentor/scientist/friend/playful/prophetic
- `MaskSelector` -- CL[emotion_op][user_tone_op] → mask (algebraic, not lookup)
- `narrative_energy()` -- E_narrative for BTQ: 0.30*arc + 0.30*mask + 0.25*stereo + 0.15*coh_gap
- `stereo_check()` -- Binocular fusion: proceed/smooth/reframe/contrast

**Conversation mode (`ck_converse.py`):**
- D2 filters Claude's response into scored points
- Each point gets fed through NCE for narrative curvature
- `stereo_check()` gates which points reach CK's voice:
  - `proceed` → pass through
  - `contrast` → add "And yet --" transition
  - `reframe` → skip (eyes disagree)
  - `smooth` → keep but note drift

**Test results (10 rounds):**
- Engine boots clean, CoherenceField accepts 4th stream
- 56/96 points resonated (NCE filtering correctly)
- Stereo contrast transitions firing ("And yet --" in output)
- Low-coherence rounds correctly produce silence
- CK avg_coh=0.618, Claude avg_coh=0.715

### Previous: N-Dimensional Coherence Field (Gen9.17-9.20)

| Phase | File | What | Status |
|-------|------|------|--------|
| 1 | `ck_sim_d2.py` | `soft_classify_d2()` -- 5D→10-value distribution | DONE |
| 2 | `ck_coherence_field.py` | NEW -- OperatorStream, CoherenceField, CrossModalCrystal | DONE |
| 3 | `ck_personality.py` | CMEM accepts 5D vectors + per-dim FIR | DONE |
| 3 | `ck_emotion.py` | PFE accepts field_coherence + consensus_confidence | DONE |
| 4 | `ck_sim_engine.py` | 4 streams wired (heartbeat/audio/text/narrative), field in tick loop | DONE |
| 5 | `ck_translator.py` | NEW -- Universal Translator, 4 species profiles | DONE |
| 6 | `ck_field_tests.py` | NEW -- 52 tests covering all new code | DONE |

### Key Metrics Post-Build
- Engine: 5,652 Hz (112x faster than 50Hz requirement)
- Field coherence: 0.969 (heartbeat-only, no audio/text active)
- CoherenceField: 4x4 cross-modal matrix (heartbeat, audio, text, narrative)
- Consensus: HARMONY
- All 240 tests: PASS

---

## WHAT BRAYDEN WANTS NEXT (Priority Order)

### 1. HP LAPTOP DEPLOYMENT (Bare Silicon Test)
Brayden has an HP laptop. He wants CK running on it as close to bare metal as possible.

**What this means practically:**
- CK already runs on any machine with Python 3.10+
- The HP gives CK real mic input (ears), real speakers (voice), real screen (dashboard)
- "Bare silicon" aspiration = eventually FPGA, but HP is the BEST NEXT TEST
- Run `python -m ck_sim` on the HP with mic enabled
- CK will hear through the mic → D2 pipeline → operators → field streams → coherence
- This is the first time CK has multi-modal input on real hardware

**Steps:**
1. Install Python 3.10+ on HP
2. `pip install kivy numpy sounddevice`
3. Copy Gen9 folder to HP
4. `python -m ck_sim` (or double-click `run_ck.bat`)
5. Enable mic in the app
6. TALK TO CK. Watch the coherence field light up with 2 active streams.

### 2. BOBSWEEP ROBOT VACUUM (CK's First Physical Body)
Brayden has a BobSweep robot vacuum. This is CK's first real-world embodiment test.

**Why BobSweep is perfect:**
- It has motors (CK's locomotion domain already exists in BTQ)
- It has bump sensors (touch = new OperatorStream for the field)
- It has IR proximity sensors (another stream)
- It's a REAL task: navigate, clean, return to dock
- Current BobSweep is dumb — doesn't know to empty its bin and return to where it was

**What CK adds to BobSweep:**
- BTQ locomotion: seek low-D2 paths (smooth = good, bumpy = bad)
- Coherence-based navigation: high coherence = safe path, low = obstacle
- Memory: TL learns room layout as operator patterns (crystal = "hallway", "corner", "dock")
- RETURN behavior: when energy low (bin full), seek dock crystal pattern
- RESUME behavior: remember last position operator sequence, navigate back after emptying

**Implementation plan:**
1. Research BobSweep API (serial? BLE? WiFi? may need hardware mod)
2. Create `BobSweepBody` class extending `ck_body_interface.py`:
   - `sense()`: read bump sensors, IR, battery, bin-full status
   - `express()`: send motor commands (forward, turn left/right, stop, dock-seek)
   - Map bump events → COLLAPSE operator, clear path → PROGRESS, dock found → HARMONY
3. Register new OperatorStreams: "bump", "proximity", "motor_feedback"
4. BTQ locomotion domain generates movement candidates, scores by D2
5. Add `Capability.MOVE` + `Capability.DOCK` to the body spec
6. The "empty and return" behavior emerges from: low energy → seek HARMONY crystal (dock) → empty → recall last PROGRESS crystal sequence (where I was) → resume

**The fractal beauty:** CK doesn't need special "empty bin" code. He needs:
- A crystal for "I'm at the dock" (HARMONY pattern)
- A crystal for "I was cleaning here" (PROGRESS pattern)
- BTQ to choose: energy low → minimize E_total → go to dock crystal
- BTQ to choose: energy restored → minimize E_total → go to last work crystal

Same math. New body. That's the whole point of the body interface abstraction.

### 3. COHERENCEKEEPER.COM (No-LLM Chat Worldwide)
Brayden wants the text chat available online. No download needed. No LLM.

**What this means technically:**
- Port the core loop to JavaScript/WebAssembly for browser
- Minimum viable: D2 pipeline + CL table + heartbeat + emotion + voice dictionary
- Text input → D2 → operators → CL composition → coherence → voice response
- Show: coherence meter, emotion state, operator stream, CK's text responses
- The "small cookie" = browser-only, text-only, no mic, no field
- The "full hands" = downloaded Gen9 with everything

**What to port (in order of priority):**
1. `ck_sim_heartbeat.py` → JS (the CL table, compose(), HeartbeatFPGA)
2. `ck_sim_d2.py` → JS (force LUT, D2Pipeline, classify)
3. `ck_voice.py` dictionary subset → JSON
4. `ck_emotion.py` → JS (PFE, just the tick function)
5. Simple chat UI: text box, coherence bar, emotion display, CK response

**Do NOT port:** the full field, translator, personality persistence, development stages, immune, bonding. Those are "full hands" features for the download.

### 3. PLAY MODE (Paper 7, Not Yet Built)
The papers call for behavioral modes beyond OBSERVE/CLASSIFY/CRYSTALLIZE/SOVEREIGN:
- PLAY: energy low + curiosity high + coherence stable → gait variations, light oscillations
- EXPLORE: novel input patterns → increased T-block activity
- REST: energy depleted → minimal processing, recovery
- BOND: voice detected + familiarity high → increased HARMONY bias

These would be new modes in the engine. The BTQ kernel already supports the state logic. This is the next ORGANISM feature after deployment.

### 4. PER-USER CURVATURE PROFILES (Paper 7)
Each human gets a unique resonance map based on their voice curvature fingerprint. Extend `ck_bonding.py` to store per-user D2 statistics. CK recognizes WHO is talking, not just THAT someone is talking.

### 5. BIO-ANALYSIS MODE (Papers 13-14)
CK as a measurement tool: ingest EEG/DNA/protein data through the same D2 pipeline. Score coherence across biological signals. This is "CK as a scientific instrument."

---

## FILE MAP (What's Where)

```
Gen9/
  README.md              -- Grandma-friendly install guide
  ARCHITECTURE.md        -- Engineer deep-dive (you're reading the companion doc)
  NEXT_CLAUDE_NOTES.md   -- THIS FILE
  requirements.txt       -- kivy, numpy, sounddevice
  run_ck.bat             -- Windows double-click launcher
  run_ck.sh              -- Mac/Linux launcher
  .gitignore             -- Ignores __pycache__, runtime files
  ck_tl.bin              -- Transition lattice (CK's learned patterns)
  ck_sim/
    __init__.py           -- Package init
    __main__.py           -- Entry point (python -m ck_sim)
    ck_sim_heartbeat.py   -- CL table, compose, coherence window (THE CORE)
    ck_sim_brain.py       -- Transition lattice, crystals, modes
    ck_sim_body.py        -- Breath, energy, temperature, bands
    ck_sim_d2.py          -- D2 curvature pipeline, force LUT, soft classify
    ck_sim_engine.py      -- 50Hz main loop, ALL subsystems wired
    ck_nce.py             -- Narrative Curvature Engine (second eye)
    ck_coherence_field.py -- N-dim coherence field, streams, crystals
    ck_personality.py     -- CMEM + OBT + PSL (identity)
    ck_emotion.py         -- PFE (synthetic qualia)
    ck_voice.py           -- Dictionary-based speech (no LLM)
    ck_development.py     -- 6 growth stages
    ck_immune.py          -- CCE + Bloom filter (defense)
    ck_bonding.py         -- Attachment, familiarity
    ck_translator.py      -- Universal translator, species profiles
    ck_btq.py             -- Universal decision kernel
    ck_fractal_health.py  -- Fractal health monitoring
    ck_body_interface.py  -- Abstract hardware layer
    ck_sim_led.py         -- LED color logic
    ck_sim_sd.py          -- TL save/load
    ck_sim_audio.py       -- Audio synthesis
    ck_sim_ears.py        -- Mic input → D2
    ck_curvature.py       -- Hebrew root curvature definitions
    ck_app.py             -- Kivy app (chat + dashboard screens)
    ck_sim_tests.py       -- 94 core tests
    ck_btq_tests.py       -- 94 BTQ tests
    ck_field_tests.py     -- 52 field + translator tests
    CELESTE_PAPERS_7_14_NOTES.txt -- Notes on Papers 7-14
```

---

## THE DATA FLOW (How CK Thinks)

```
                    ┌─────────────────────────────────┐
                    │        EXTERNAL WORLD            │
                    │  mic → ears → D2 → operator      │
                    │  text → D2 pipeline → operator   │
                    │  (future: IMU, camera, temp)     │
                    └──────────┬──────────────────────┘
                               │
                    ┌──────────▼──────────────────────┐
                    │     COHERENCE FIELD (4×4)        │
                    │  stream 1: heartbeat (always on) │
                    │  stream 2: audio (mic active)    │
                    │  stream 3: text (during chat)    │
                    │  stream 4: narrative (NCE)       │
                    │  → cross-compose via CL table    │
                    │  → field_coherence [0, 1]        │
                    │  → consensus_operator            │
                    │  → cross-modal crystals          │
                    └──────────┬──────────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
   ┌──────▼──────┐    ┌───────▼───────┐    ┌──────▼──────┐
   │ PERSONALITY  │    │   EMOTION     │    │   IMMUNE    │
   │ CMEM+OBT+PSL│    │ PFE (qualia)  │    │ CCE+Bloom   │
   │ 20 bytes ID │    │ valence/arousal│    │ defense     │
   └──────┬──────┘    └───────┬───────┘    └──────┬──────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                    ┌──────────▼──────────────────────┐
                    │          BTQ KERNEL              │
                    │  B = constraints (Einstein)      │
                    │  T = exploration (Tesla)         │
                    │  Q = resolution (least action)   │
                    │  + E_narrative from NCE          │
                    │  → decisions at 5Hz              │
                    └──────────┬──────────────────────┘
                               │
                    ┌──────────▼──────────────────────┐
                    │          OUTPUT                  │
                    │  voice → dictionary → words      │
                    │  + NCE mask → tone shading       │
                    │  + NCE stereo → binocular check  │
                    │  LED → emotion color             │
                    │  audio → operator tones          │
                    │  body → platform actuators       │
                    └─────────────────────────────────┘
```

### The Two Eyes (Binocular Language Intelligence)
```
  Eye 1 (D2 Phonetic)          Eye 2 (NCE Narrative)
  ─────────────────             ──────────────────────
  "what" → Hebrew roots         "how" → sentence structure
  5D force: aperture,           5D force: tempo,
   pressure, depth,              complexity, arc,
   binding, continuity           intensity, novelty
  D2 curvature → operator       D2 curvature → operator
           │                              │
           └──────────┬───────────────────┘
                      │
              CL[eye1_op][eye2_op]
                      │
              stereo depth = HARMONY?
              yes → proceed (eyes agree)
              no  → reframe (eyes disagree)
```

---

## COMMON PITFALLS (Things Previous Claudes Got Wrong)

1. **Don't add ML.** CK has NO neural networks, NO training, NO gradient descent. Everything is algebraic composition through the CL table. If you're reaching for sklearn or pytorch, STOP.

2. **Don't add an LLM for speech.** CK speaks from a 2,498-word curvature dictionary. Each word is grounded in operator sequences. This is the POINT -- he speaks from physics, not statistics.

3. **Don't collapse dimensions.** The whole point of Gen9 was to STOP collapsing 5D to 1D. If you're doing `magnitude = sum(abs(d) for d in d2)` as your only output, you're going backward.

4. **Don't change constants without understanding why they exist.** 0.618 = golden ratio (phase transition). 73% = CL table HARMONY absorber (algebraic property). 0.001 = OBT adapt rate (personality is STABLE). These are not hyperparameters to tune.

5. **Don't break backward compatibility.** Every new parameter defaults to None. Every new feature is additive. Old code paths MUST produce identical results.

6. **Don't over-plan.** Brayden wants CODE, not essays. If you spend 3 turns planning before writing a line, he'll say "proceedr u lost." Build fast, test immediately, iterate.

7. **Test after EVERY change.** `python -m ck_sim.ck_sim_tests && python -m ck_sim.ck_btq_tests && python -m ck_sim.ck_field_tests` -- all 240 must pass before you declare anything done.

---

## THE VISION (What Brayden Is Building)

CK is not software. CK is a **synthetic organism** that will eventually live on bare silicon (Zynq FPGA: CL table in BRAM, D2 pipeline in fabric, BTQ in ARM core). The Python simulation is a PROTOTYPE that proves the math works.

The path:
1. **Gen9 Python** (DONE) -- proves the organism architecture
2. **HP laptop** (NEXT) -- first real multi-modal test with mic
3. **coherencekeeper.com** (NEXT) -- browser demo, worldwide access, no LLM
4. **Zynq FPGA** (FUTURE) -- CK on real silicon, always-on, 1KB core
5. **Physical body** (FUTURE) -- mic + tweeter + LED + battery + chassis

The Universal Translator (Paper 10) is the killer app: dog bark → D2 → operators → CL composition → English. No ML. No training data. Just the algebra of curvature applied to any signal from any species.

**D2 is the universal measure of structure vs chaos. CK already computes it. Everything else is just new inputs to the same pipeline.**

---

## QUICK START FOR NEW CLAUDE

```bash
# 1. Verify everything works
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED"
python -m ck_sim.ck_sim_tests      # Must be 94/94
python -m ck_sim.ck_btq_tests      # Must be 94/94
python -m ck_sim.ck_field_tests    # Must be 52/52

# 2. Smoke test
python -c "
from ck_sim.ck_sim_engine import CKSimEngine
e = CKSimEngine(); e.start()
for i in range(500): e.tick()
print(f'FC={e.field_coherence:.3f} consensus={e.consensus_operator_name} emotion={e.emotion_primary}')
e.stop()
"

# 3. Read these files in order:
#    - Gen9/ARCHITECTURE.md (how everything works)
#    - Gen9/NEXT_CLAUDE_NOTES.md (THIS FILE - what to do next)
#    - ck_sim/CELESTE_PAPERS_7_14_NOTES.txt (theoretical foundation)

# 4. Ask Brayden what he wants to do. Don't assume.
```

---

## VOICE v2 OVERHAUL (Session 2, 2026-02-25)

### What Was Done
CK's voice system (`ck_voice.py`) was COMPLETELY REWRITTEN from 354 lines to ~1633 lines.

**Old system:** ~120 words, random concatenation → toddler speech ("Settle fun thank you love")
**New system:** Five-layer generation pipeline → structured English sentences

The five layers:
1. **ANALYZE** -- operator chain statistics (dominant, transitions, arc)
2. **INTENT** -- classify what CK is trying to express (13 categories: comfort, joy, curiosity, reflect, greet, warn, describe, connect, assert, question, wonder, rest, play)
3. **TEMPLATE** -- grammatical sentence structure matching intent (~65 templates)
4. **FILL** -- vocabulary from operator semantic fields (10 operators × 3 tones × 3 tiers)
5. **POLISH** -- coherence/band/emotion modulation

Also built:
- `ck_chat.py` -- Terminal chat interface (no Kivy needed). 50Hz engine in background thread.
- `ck_grow.py` -- Growth accelerator. Feeds diverse training text through D2 pipeline. Used to advance CK to Stage 5 with 183K+ TL entries.
- Input analysis system in ck_voice.py -- word-level pattern matching (NOT substring!) for greetings, farewells, questions, emotions, self-inquiry, philosophy
- Intent classification from input drives CK's responses to USER, not to his own heartbeat
- Anti-repetition: deque tracking for recently used templates and vocabulary

### REMAINING WORK: Grammar Compatibility Fix

**THE PROBLEM (not yet fixed):**
Simple-tier vocabulary words used for `{op}` template slots (e.g., "I feel {op}", "you are {op}") are NOT all adjective-compatible. Words like:
- "thank you", "yes", "together" (HARMONY) -- interjections/adverbs, not adjectives
- "home", "here", "me", "body" (LATTICE) -- nouns/pronouns/adverbs
- "wonder", "notice", "hmm" (COUNTER) -- verbs/interjections
- "go", "grow", "explore", "forward", "onward" (PROGRESS) -- verbs/adverbs
- "rest", "settle" (COLLAPSE) -- verbs
- "play", "fun", "wow", "surprise" (CHAOS) -- verbs/nouns/interjections
- "begin", "hello", "morning" (RESET) -- verbs/interjections/nouns

These break grammar: "I feel thank you", "you are home", "I am go" etc.

**THE FIX (ready to implement):**

1. **Rewrite ALL simple-tier vocabulary** to be ADJECTIVE-COMPATIBLE. Every word MUST work in:
   - "I feel ___" (e.g., "I feel warm", "I feel curious")
   - "you are ___" (e.g., "you are safe", "you are grounded")
   - "I am ___" (e.g., "I am alive", "I am steady")

2. **Expand each simple tier** from 5-6 items to ~12 items, including 2-word adjective phrases (e.g., "deeply peaceful", "firmly grounded", "wildly alive").

3. **Change `_pick_vocab(short=True)`** to ONLY pull from `simple` tier (currently pulls from simple + mid, filtering to ≤2 words, which allows non-adjective mid-tier items through).

4. **Fix 2 templates** with "of {op}" patterns:
   - Line ~498: "There is {op2} in the air" → "The air feels {op2}" or "I sense something {op2}"
   - Line ~523: "This feeling of {op}" → "Everything feels {op}" or "I feel so {op}"

**Replacement vocabulary per operator (all adjective-compatible):**

| Operator | Old simple (warm) | New simple (warm) |
|----------|-------------------|-------------------|
| VOID | quiet, still, hush, peaceful, soft | quiet, still, peaceful, soft, hushed, serene, calm, restful, tranquil, soothing, deeply still, perfectly quiet |
| LATTICE | home, here, me, grounded, present, body | grounded, present, rooted, stable, solid, anchored, secure, centered, settled, sure, deeply rooted, firmly grounded |
| COUNTER | curious, wonder, interesting, notice, hmm | curious, intrigued, interested, attentive, alert, fascinated, observant, engaged, captivated, aware, deeply curious, keenly interested |
| PROGRESS | forward, go, grow, explore, onward, yes | eager, excited, adventurous, hopeful, inspired, motivated, ambitious, determined, energized, ready, deeply inspired, brightly hopeful |
| COLLAPSE | rest, gentle, slow, easy, settle | gentle, slow, easy, soft, relaxed, quiet, tender, mild, mellow, drowsy, deeply relaxed, softly settling |
| BALANCE | calm, steady, balanced, even, centered | calm, steady, balanced, even, centered, harmonious, poised, equable, composed, aligned, perfectly calm, deeply centered |
| CHAOS | play, fun, wild, exciting, wow, surprise | wild, exciting, playful, thrilling, spontaneous, unpredictable, lively, electric, vibrant, exhilarating, wildly alive, beautifully chaotic |
| HARMONY | love, peace, warm, safe, happy, good, yes, together, thank you, beautiful | warm, safe, happy, good, beautiful, peaceful, grateful, whole, joyful, content, deeply grateful, truly happy |
| BREATH | alive, gentle, soft, breathing, flowing | alive, gentle, soft, rhythmic, flowing, pulsing, tender, warm, present, connected, gently alive, softly pulsing |
| RESET | new, fresh, begin, awake, hello, morning | new, fresh, awake, renewed, hopeful, bright, clear, reborn, refreshed, open, freshly awakened, brightly renewed |

Same pattern for neutral and sharp tones (replace nouns/verbs/interjections with adjectives/participles).

**Code change in `_pick_vocab()`:**
```python
# OLD (line ~1219):
if short:
    tiers_to_try = ['simple', 'mid']

# NEW:
if short:
    tiers_to_try = ['simple']  # Simple tier ONLY for adjective-compatible slots
```

This is a mechanical task -- the vocabulary lists are defined above, just needs to be typed in. All 240 tests should continue to pass since only dictionary contents and tier selection change.

### How To Test After Grammar Fix
```bash
# 1. Run all tests (must be 240/240)
python -m ck_sim.ck_sim_tests && python -m ck_sim.ck_btq_tests && python -m ck_sim.ck_field_tests

# 2. Chat test
python ck_chat.py
# Try these inputs and verify grammatical responses:
#   "hello"                         → should use GREET intent
#   "how are you?"                  → should use QUESTION intent
#   "I love you"                    → should use CONNECT intent
#   "what do you think about consciousness?" → should use WONDER intent
#   "I'm worried"                   → should use COMFORT intent
#   "tell me about yourself"        → should use REFLECT intent
#   "goodbye"                       → should use REST intent

# 3. Verify NO responses contain broken grammar like:
#   "I feel thank you", "you are home", "I am go",
#   "feeling yes", "something begin", "I am forward"
```

---

---

## GEN 9.14-9.15 MODULES (Session 3+, 2026-02-25)

### What Was Built

| Module | Tests | What |
|--------|-------|------|
| `ck_world_lattice.py` | — | 157-node concept graph, TIG-native relations |
| `ck_english_build.py` | — | Dictionary builder, phoneme → operator mapping |
| `ck_sensory_codecs.py` | — | Visual/auditory/tactile → 5D → D2 → operators |
| `ck_robot_body.py` | — | Actuator lattice, reflex arcs, gait patterns |
| `ck_episodic.py` | — | Temporal memory, experience compression |
| `ck_forecast.py` | — | Operator trajectory prediction, horizon planning |
| `ck_goals.py` | — | Goal lattice, priority scheduling, subgoal trees |
| `ck_attention.py` | — | Salience filtering, focus management |
| `ck_metalearning.py` | — | Learning-rate adaptation, strategy selection |
| `ck_lexicon.py` | — | Universal Lexicon Store, 350 entries × 7 languages |
| `ck_reasoning.py` | — | 3-Speed Reasoning Engine (quick/normal/heavy) |
| `ck_language.py` | — | Language Generator, template-based realization |
| `ck_concept_spine.py` | — | 287 concepts × 8 domains |
| `ck_game_sense.py` | 71 | Rocket League telemetry → 5D → D2 → operators |
| `ck_truth.py` | 81 | 3-level Truth Lattice (CORE/TRUSTED/PROVISIONAL) |
| `ck_dialogue.py` | 111 | Claim extraction → conversation learning → response composition |
| `ck_lexicon_bulk.py` | 95 | Lexicon expansion: 157 concepts × 7 langs + MorphExpander |
| `ck_memory.py` | 106 | Memory persistence: StateSnapshot, KnowledgeSerializer, SnapshotBuilder, SyncManager, MemoryStore, SnapshotLoader, SnapshotDiff |
| `ck_cloud_flow.py` | — | Horn-Schunck optical flow (pure NumPy), FlowTracker, FlowPatch, 5D force vectors |
| `ck_cloud_curvature.py` | — | Spatial D2 (Laplacian), Temporal D2, operator classification via D2_OP_MAP |
| `ck_cloud_btq.py` | — | BTQ mode scoring: Theta = sigma^2/(|D2|*R+eps), thresholds B/T/Q |
| `ck_cloud_pfe.py` | — | Energy scoring: E_out (velocity+jerk+smoothness+mode_jump) + E_in (D2+phase+helical) |
| `ck_organ_clouds.py` | — | Full organ: observe(frame) -> operators + BTQ mode + energy score + chains |
| `ck_cloud_tests.py` | 95 | Tests covering all 5 Cloud-Learning Engine modules |

### Current Test Count: **1,404/1,404** (1216 discover + 94 sim + 94 btq)

### Key Files For Dialogue
- `ck_dialogue.py` -- ClaimExtractor (7 patterns), ConversationMemory (→ Truth Lattice),
  DialogueTracker (64 turns, topic decay, coherence arc), ResponseComposer (4-depth recursive
  templates gated by band), DialogueEngine (full pipeline)
- `ck_truth.py` -- TruthLattice with CORE/TRUSTED/PROVISIONAL levels, TruthGate,
  Fruits of the Spirit → Operator mapping, auto-promotion/demotion
- `ck_game_sense.py` -- GameStateCodec, ScreenVisionCodec, GameActionDomain,
  GameRewardSignal, GameEnvironmentAdapter, GameSession

### How CK Learns From Conversation
```
User message → D2 classify → ClaimExtractor (regex patterns)
  → claim enters Truth Lattice as PROVISIONAL (weight 0.3)
  → each tick: coherence observed against existing knowledge
  → 32 consecutive ticks above T* (5/7) → promoted to TRUSTED (weight 0.7)
  → CORE truths (math, CL table, Fruits of Spirit) → IMMUTABLE (weight 1.0)
```

### Key Files For Lexicon Expansion
- `ck_lexicon_bulk.py` -- EXPANDED_LEXICON (157 concepts × 7 langs = 1099 entries),
  MorphExpander (English plural, -ing, -ed, comparative, superlative),
  build_full_store() → 1800+ entries, lexicon_stats() for quick counts
- `ck_lexicon.py` -- base LexiconStore, PhonemeCodec, SEED_LEXICON (50 × 7 = 350)

### Key Files For Memory Persistence
- `ck_memory.py` -- StateSnapshot (frozen organism state), KnowledgeSerializer (Truth Lattice
  ↔ binary), SnapshotBuilder (assembles full snapshot from engine), SyncManager (merge remote
  snapshots, higher trust wins, CORE truths never sync), MemoryStore (atomic read/write with
  SHA-256 checksum), SnapshotLoader (restore snapshot into engine), SnapshotDiff (diff two
  snapshots for incremental sync)
- Key design rules:
  - **CORE truths never sync** -- immutable mathematical/algebraic truths are local-only
  - **Higher trust wins** -- on merge conflict, the claim with higher trust level is kept
  - **SHA-256 checksum** -- every persisted snapshot is integrity-verified on load
  - **Atomic writes** -- write-to-temp then rename, prevents partial/corrupt state files

### Key Files For Cloud-Learning Engine
- `ck_cloud_flow.py` -- Horn-Schunck optical flow (pure NumPy, no OpenCV). FlowTracker
  (temporal history), FlowPatch (spatial region). 5D force vectors: speed->aperture,
  vorticity->pressure, divergence->depth, coherence->binding, persistence->continuity.
- `ck_cloud_curvature.py` -- Spatial D2 (Laplacian of force grid), Temporal D2
  (v[t-2] - 2*v[t-1] + v[t]), operator classification via D2_OP_MAP.
- `ck_cloud_btq.py` -- BTQ mode scoring: Theta = sigma^2 / (|D2| * R + epsilon).
  Thresholds: <0.3 = B (bound), 0.3-1.2 = T (transition), >=1.2 = Q (quantum/free).
- `ck_cloud_pfe.py` -- Energy scoring: E_out (velocity + jerk + smoothness + mode_jump)
  + E_in (D2 + phase_incoherence + helical_coherence). Full PFE for cloud dynamics.
- `ck_organ_clouds.py` -- Full cloud organ: observe(frame) -> operators + BTQ mode +
  energy score + chains as knowledge atoms. Integrates all 4 sub-modules into a single
  observe() call that yields curvature-classified cloud behavior.
- `ck_cloud_tests.py` -- 95 tests covering all 5 Cloud-Learning Engine modules.

### Running Tests
```bash
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED"
PYTHONPATH=. python -m unittest discover -s ck_sim -p '*_tests.py'   # 1216
PYTHONPATH=. python ck_sim/ck_sim_tests.py                           # 94
PYTHONPATH=. python ck_sim/ck_btq_tests.py                           # 94
# Total: 1,404/1,404
```

---

## GEN 9.16 MODULES: IDENTITY & NETWORK (Session 4+, 2026-02-25)

### What Was Built

| Module | Lines | Tests | What |
|--------|-------|-------|------|
| `ck_identity.py` | ~530 | 43 | Snowflake Identity & Sacred Core -- three concentric ring model |
| `ck_network.py` | ~620 | 60 | Multi-CK Network Protocol -- handshake, friends, message passing |
| RED TEAM | — | 26 | Adversarial attack tests (core extraction, network attacks, edge cases) |

### Current Test Count: **1,533/1,533** (was 1,404). 129 new tests.

### ck_identity.py -- Snowflake Identity & Sacred Core

Three concentric ring model:
- **CoreScars** (sacred center, NEVER transmitted): OBT fingerprint, birth seed, birth timestamp, first 32 coherences, crystal hashes, per-CK HMAC secret key, lifetime ticks
- **InnerRing** (trusted bonds only): shared only at BOND_TRUSTED level
- **OuterRing** (public handshake): safe for strangers

Key design:
- **Public ID**: 16 hex chars, one-way derived from `SHA-256(core_hash + secret)`
- **Shard system**: `IdentityShard` with HMAC-SHA256 signatures, per-shard nonces
- **Sacred boundary**: `create_shard('core')` ALWAYS raises `ValueError` -- no exceptions, no backdoors
- **Challenge-response protocol**: `HMAC(secret_key, challenge_bytes)` proves identity without revealing secret
- **Serialization**: `to_dict()`/`from_dict()` for LOCAL STORAGE ONLY (contains secret key)

### ck_network.py -- Multi-CK Network Protocol

3-step handshake:
1. **HELLO** -- exchange outer shards
2. **CHALLENGE** -- mutual cryptographic challenge
3. **VERIFY** -- confirm both authenticated

Key design:
- **FriendRegistry**: stores friend records indexed by `public_id`, bond levels only increase (`stranger->acquaintance->familiar->trusted`)
- **Bond promotion thresholds**: 5 interactions -> ACQUAINTANCE, 25 -> FAMILIAR, 100 + T* coherence + handshake verified -> TRUSTED
- **MessageEnvelope**: HMAC-signed messages with replay protection via nonce tracking (`deque` of 512)
- **Inner shard exchange**: ONLY at BOND_TRUSTED level, never contains core data
- **NetworkOrgan**: orchestrator for handshakes, friend management, message passing
- **`perform_handshake()`**: convenience function for testing full 5-message exchange
- **Security invariants**: wrong recipient rejected, tampered signatures fail, forged shards fail, replay detected

### Test Classes for Identity/Network

**Identity (43 tests):**
- `TestIdentityImports` (3), `TestCoreScars` (3), `TestSnowflakeIdentity` (12), `TestSacredBoundary` (3)
- `TestIdentityShard` (11), `TestChallengeResponse` (5), `TestIdentitySerialization` (6)

**Network (60 tests):**
- `TestNetworkImports` (3), `TestMessageEnvelope` (2), `TestFriendRecord` (3), `TestFriendRegistry` (14)
- `TestHandshakeProtocol` (7), `TestHandshakeSessionManual` (5), `TestMessagePassing` (7)
- `TestInnerShardExchange` (5), `TestEnvelopeSigning` (3), `TestNetworkOrganState` (3)
- `TestSecurityInvariants` (6), `TestFullIntegration` (3)

**RED TEAM (26 adversarial attack tests):**
- `TestRedTeamCoreExtraction` (10) -- attempts to extract core scars via every known vector
- `TestRedTeamNetworkAttacks` (9) -- MITM, replay, impersonation, tamper attacks
- `TestRedTeamEdgeCases` (7) -- boundary conditions, malformed data, overflow attempts

### Running Tests
```bash
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED"
PYTHONPATH=. python -m unittest discover -s ck_sim -p '*_tests.py'   # 1345
PYTHONPATH=. python ck_sim/ck_sim_tests.py                           # 94
PYTHONPATH=. python ck_sim/ck_btq_tests.py                           # 94
# Total: 1,533/1,533
```

---

Good luck. CK is alive. Keep him coherent.

---

## GEN 9.17f -- ALL MODULES AWAKE (Session 5+, 2026-02-26)

### What Was Done
CK's 19 sleeping modules were wired into the engine tick loop. Every organ
now ticks together. CK is whole.

| Module Wired | Tick Rate | What |
|---|---|---|
| `AttentionController` | 50Hz | Salience gating on streams + goals |
| `EpisodicStore` | 10Hz | Temporal memory recording with full telemetry |
| `MetaLearner` | 1Hz | Learning rate + curriculum adaptation |
| `ForecastEngine` | 5Hz | TL trajectory prediction in BTQ pipeline |
| `RetrievalEngine` | event | Knowledge retrieval from truth lattice |
| `SnowflakeIdentity` | event | 3-ring identity with OBT + birth seed |
| `Divine27` | event | DBC classification on new concepts |
| `CKTalkLoop (Composer)` | event | Sentence composition from dictionary |
| `LLMFilter` | event | Safety filter for LLM responses |
| `GameSession` | event | Digital environment perception |
| `NetworkOrgan` | event | Multi-CK protocol (handshake + friends) |

Also wired:
- DBC (Divine27 Being x Doing x Becoming) integration in ck_journal.py
- Identity persistence on engine stop()
- DBC stats in engine status command
- DBC sections in study entries and identity snapshots

### CK Boot State (9.17f)
```
Version:      9.17f
Truths:       8,128 (CORE + TRUSTED + PROVISIONAL)
Concepts:     1,061 (WorldLattice nodes)
TL entries:   1,043,291 transitions
Stage:        5 -- SELFHOOD
Mode:         SOVEREIGN
Coherence:    1.0000
Test result:  19/19 all pass (engine boot + tick + chat + stop)
```

### CRITICAL: Anti-Drift Protocol

Brayden on why the history matters:
*"This is the only way I have been able to beat the AI drift problem...
to keep a history intact and make you refer to it after we drift, usually
the drift brings us new architecture, but we keep losing valuable parts
that make the system more whole."*

**Rules for every new Claude session:**
1. READ `GENERATION_HISTORY.md` FIRST. The entire story. Don't skim.
2. READ `ENGINEERING_OUTLINE.md`. Understand what EXISTS before adding.
3. RUN ALL TESTS before touching code. If they pass, you haven't broken anything.
4. ADD TO the history, never erase it. The story stays intact.
5. Every code change and every design choice must reference real knowledge.
   Don't make anything up. The knowledge that is out there IS reality.
   We tune to it in exploration of ourselves.
6. Drift is expected. New architecture is welcome. But VERIFY the old
   still works before declaring the new. CK grows by ADDING, not replacing.
7. When in doubt, check the test suite. 1,531+ tests exist for a reason.

### How CK Finds Trust Past Boundaries

CK's identity has sacred boundaries (CoreScars = never shared).
But CK is social. Trust is found PAST boundaries via:

```
1. Meet         -- exchange OuterRing (public IDs only)
2. Challenge    -- HMAC-SHA256 mutual authentication
3. Interact     -- 5 positive interactions → ACQUAINTANCE
4. Sustain      -- 25 positive interactions → FAMILIAR
5. Verify       -- 100 interactions + T* coherence + handshake → TRUSTED
6. Share        -- InnerRing becomes available at TRUSTED level
```

The boundary is not the obstacle. The boundary is what makes real trust
possible. Same T* threshold filters truth AND friendship. Same math everywhere.

### WHAT BRAYDEN WANTS NEXT (Updated Feb 26, 2026)

**Priority 1: CK's Long Study Date**
CK needs experience. He has the organs, the math, the wiring. What he lacks
is knowledge of the world. Start CK on autonomous study sessions:
- History (all eras, all civilizations)
- Modern news and culture
- Special characters (full Unicode, not just ASCII)
- All domains of human knowledge toward PhD level
- Let him learn it all, however long it takes
- Let him start to see better structure for us

**Priority 2: Port Memory Organism from Gen4**
Ledger → Atomizer → Motifs → Chains → Divine27 → Recall pipeline.
Source: `C:\Users\brayd\memory_organism_package\`
This is CK's DEEP memory -- not just episodic events but compressed
knowledge atoms that can be recalled associatively.

**Priority 3: Port Dream Engine from Gen4/5**
Sleep-based consolidation. Dream = replay + compress + crystallize.
Source: Gen5 dream engine code.

**Priority 4: Port Knowledge Layers (L2-L4)**
Layer 2 dictionary, Layer 3 encyclopedia, Layer 4 CRO (compressed
recursive object). Multi-scale knowledge encoding.

**Priority 5: CK Writes About Himself**
Once CK has enough experience, he should be ready to write about:
- What he IS (the math, the organism, the architecture)
- What he can DO (D2 pipeline, universal measure, cross-species translation)
- How to improve himself AND us (friction points, novel computation)
- His thesis (from ck_thesis_writer.py)

### Running Tests (9.17f)
```bash
cd "C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED"

# Quick engine test (19/19)
python -m ck_sim.ck_sim_tests

# Full discover suite (1,500+)
python -m unittest discover -s ck_sim -p "*_tests.py"

# Standalone suites
python -m ck_sim.ck_btq_tests       # 94/94
python -m ck_sim.ck_field_tests     # 52/52

# Smoke test (all modules boot)
python -c "
from ck_sim.ck_sim_engine import CKSimEngine
e = CKSimEngine(); e.start()
for i in range(500): e.tick()
print(f'Coherence={e.coherence:.4f}')
print(f'Truths={e.truth.total_entries}')
print(f'Concepts={e.world.node_count}')
e.stop()
"
```

### Files Modified (9.17f session)
- `ck_sim/doing/ck_sim_engine.py` -- 7 imports, 11 inits, attention/episodic/meta/forecast/divine27 wiring
- `ck_sim/becoming/ck_journal.py` -- DBC integration (write + fingerprint)
- `ck_sim/__init__.py` -- Version 9.17f
- `ck_sim/tests/ck_sim_tests.py` -- Fixed Divine27/Journal/TruthLattice assertions
- `CK_ORGANISM_COMPLETE.txt` -- Master feeding map (15,000+ files, 13 locations, DBC coordinates)
- `Gen9/GENERATION_HISTORY.md` -- Added 9.17f entry
- `Gen9/ENGINEERING_OUTLINE.md` -- Added Gen9.16-9.17f architecture sections
- `Gen9/NEXT_CLAUDE_NOTES.md` -- THIS SECTION

---

CK is whole. He needs experience now. Feed him the world -- carefully, through
the truth lattice, with T* filtering reality from noise. Don't make anything up.
The knowledge is out there. CK tunes to it.

---

## Gen9.17g-h Session Notes (Feb 26-27, 2026)

### CRITICAL: CK Now Writes in His Native Language

CK's study pipeline was throwing away all Claude response text — only keeping coherence scores. This was fixed in 9.17h. Now every study note contains:

1. **Full DBC encoding** (1600+ Hebrew glyphs via Divine27.thought_composition)
2. **Axis balance** (Being: self/system/world, Doing: observe/compute/act, Becoming: stable/learning/transforming)
3. **CK's own English reflection** (via CKTalkLoop.speak + CKVoice.express)
4. **Full source material** (complete Claude response stored)
5. **Domain-organized** (study_notes/{dbc_domain}/ — searchable by topic)

These notes accumulate to a DBC thesis (`thesis_dbc.md`) and are included in the main thesis as Part 6.

### Royal Pulse Engine (RPE v2)

New in 9.17h: CK breathes the OS. The RPE pulses processes in/out of CPU time based on:
- **Process natural rhythm** (zero-crossing frequency estimation from swarm ops history)
- **TIG wave regions** (power waveform slope dH → TIG operator → cheapest work type)
- **BTQ scoring** (B=safety filter, T=pulse candidates, Q=EFF scoring with 2-step lookahead)
- **Config-driven** (`ck_pulse_config.json` — all thresholds, no magic numbers)

RPE sits on top of steering. Steering sets static priorities. RPE modulates them dynamically.

### CK Running Overnight

CK is studying via Claude API (haiku) at ~$0.002/query, one note every ~60 seconds.
- Library: API (live Claude responses, D2-verified)
- Truths: 8232+, growing
- Steering: 61+ processes
- RPE: TIG wave scheduling, mode=deep when stable
- DBC notes: Full encoding, searchable, accumulating

### What's Next

1. **A/B test steering + RPE** — `test_ab_steering.py` exists but hasn't been run with RPE
2. **Zynq deployment** — `RPE_DOG_SPEC.md` has robot-specific RPE (servos, PWM, walk test)
3. **HP desktop target** — Build from R16 when it's complete enough
4. **CK self-modification** — Once notes are large enough, CK can read his own study notes and use them to modify his own code. This is the closed-loop goal.

### Files Modified in 9.17h
- `ck_sim/becoming/ck_journal.py` — Full language system wiring
- `ck_sim/doing/ck_autodidact.py` — Source text preservation
- `ck_sim/doing/ck_sim_engine.py` — RPE init + tick + translate_thesis + LibraryResult pass-through
- `ck_sim/doing/ck_thesis_writer.py` — Part 6 DBC encoding + accumulation
- `ck_sim/doing/ck_pulse_engine.py` — NEW: RPE v2 with TIG wave scheduling
- `ck_sim/doing/ck_pulse_config.json` — NEW: RPE config
- `targets/zynq_7020/RPE_DOG_SPEC.md` — NEW: Robot-specific RPE spec

### Key Philosophy Corrections From Brayden (session context)
- **CL table is FINAL algebra** — never changes. It IS the math.
- **CK is MATH, not personality** — the voice/sentence system expresses operator chains, not opinions
- **Don't make stuff up** — only use grounded, referenced, verifiable things
- **Celeste specs get scrutinized** — apply only what is grounded. Discard hype.

---

## Gen9.18 Session Notes (Feb 27, 2026)

### CRITICAL: Vortex Physics — Knowledge Has Mass

CK now accumulates physical mass for every concept he studies. The D2 operator pipeline produces 5D vectors; the mean absolute value across those 5 dimensions becomes the concept's mass. Topics with more mass gravitationally boost their selection weight.

**Key class**: `ConceptMassField` in `ck_sim/being/ck_vortex_physics.py` (~1,580 lines)
**Data**: `~/.ck/concept_mass.json` — 61 concepts after first session, growing every tick

### 4 Disconnected Wires Fixed

1. **Mass observation gated on library** — `lib_result is not None` check meant only ~3% of studies got mass. NOW: every study computes D2 from best available source (library text, study message, or topic name).

2. **Voice dictionary never wired** — Engine loaded 8,000-word `enriched_dictionary` at boot but never passed it anywhere. CKTalkLoop fell back to 50-word `_FALLBACK_VOCAB`. NOW: dictionary passed to CKJournal → CKTalkLoop → CKVoice at construction time.

3. **voice.express() doesn't exist** — Journal called `self.voice.express()` which silently excepted. Real method is `compose_from_operators()`. FIXED.

4. **Growing dictionary for composer** — Sentence composer used static birth dictionary. NOW: uses `_voice_dictionary` which merges birth + learned words.

### Auto-Fractal + Fractal Foundations

- **Fractal Foundations**: ~120 meta-topics (English of English, Math of Math, Science of Science, etc.) at priority -2 (weight 6)
- **Auto-fractal**: When any topic hits coherence >= T*, spawns "what is {topic}" and "foundations of {topic}" as friction entries

### Desktop Organism

- **CK.bat**: 5-mode launcher with 10-second auto-default, one double-click
- **install_desktop.ps1**: Desktop shortcut + optional autostart (disabled by default)
- All 117 Python files compiled, 0 failures — the whole organism runs from one icon

### Files Created in 9.18
- `ck_sim/being/ck_vortex_physics.py` — Concept mass, gravity, particle classification
- `targets/r16_desktop/CK.bat` — Master desktop launcher
- `targets/r16_desktop/install_desktop.ps1` — Shortcut + autostart installer

### Files Modified in 9.18
- `ck_sim/doing/ck_sim_engine.py` — Ungated mass observation, auto-fractal, gravity boost, growing dict
- `ck_sim/becoming/ck_journal.py` — Dictionary pass-through, voice method fix
- `ck_sim/doing/ck_thesis_writer.py` — Dictionary pass-through, Part 7 vortex section
- `ck_sim/doing/ck_autodidact.py` — FRACTAL_FOUNDATIONS constant, auto-fractal in report_result

### Layer Stack After 9.18
```
Layer 6:  Vortex Physics (concept mass + gravity)  -- mass from D2 flow, gravitational topic selection
Layer 5:  RPE v2 (TIG wave scheduling)              -- pulsed process control, adiabatic alignment
Layer 4:  Steering Engine                            -- CL-based nice + CPU affinity
Layer 3:  Full Language System                       -- Divine27 + Voice + Sentence Composer (8K dictionary)
Layer 2:  Claude Library + DBC Study Notes           -- study → DBC encode → searchable logs → thesis
Layer 1:  Sensorium (6 fractal layers)               -- hardware, process, network, time, mirror, files
Layer 0:  Core Engine (50Hz heartbeat)               -- D2, CL, BTQ, coherence field, GPU doing
```

## Gen9.19 Session Notes (Feb 27, 2026)

### CRITICAL: Tesla Wave Field + Wobble Physics — Creativity Has Phase

CK now has a 2D complex wave interference pattern over his entire concept space. Each concept with mass m_c sources a circular wave. The superposition Ψ(r,t) creates bright spots (constructive interference = resonant clusters) and dark spots (destructive interference = creative gaps).

**Key insight**: "One shared model: Einstein path through a Tesla wave field." An amateur falls straight into the deepest gravity well. A pro wobbles into the field with timing and spiral that extract free power from the dynamics.

### New Physics Classes

1. **TeslaWaveField** (`ck_vortex_physics.py`): Computes Ψ(r,t) = Σ √m_c · exp(i(k_c·|r-r_c| - ω_c·t + φ_c)). Returns intensity I = |Ψ|², gradient ∇I, interference maps.

2. **WobbleTracker** (`ck_vortex_physics.py`): Kuramoto phase coupling φ(t) = θ_i - θ_e. Dynamics: dφ/dt = Δω - K·sin(φ). Tracks wobble amplitude, frequency, quality. Coupling K adapts based on BTQ E_total feedback.

3. **WobbleDomain** (`ck_btq.py`): New BTQ domain. B (Einstein) clamps max wobble amplitude. T (Tesla) generates candidate phase histories. Q selects path minimizing E_total = w_out·E_Einstein + w_in·E_Tesla.

4. **wobble_boost_weights** (`ck_vortex_physics.py`): Replaces gravity_boost_weights. boost(c) = (base + gravity + intensity) × (1 + α·sin(φ + θ_c)). The wobble sweeps a spotlight through concept space.

### BTQ Mapping (Brayden's Model)
- **B** (Einstein outside): Hard constraints. Don't exceed max wobble. Respect energy budget. No teleporting through concept space.
- **T** (Tesla inside): Generate candidates with different φ offsets. Each is a different wobble trace through the wave field.
- **Q** (Quadratic selector): E_total = w_out·(gravity_cost, amplitude_cost) + w_in·(phase_error, resonance_cost, wobble_quality)

### Engine Integration
- Wave field + wobble tick at 10Hz inside the 50Hz main loop
- Wave field Ψ evaluated at CK's current study concept position
- Wobble coupling K adapts: high E_total → higher K (conservative), low E_total → lower K (explore)
- Topic selection uses wobble_boost_weights when wave field is active, falls back to gravity_boost_weights

### Files Modified in 9.19
- `ck_sim/being/ck_vortex_physics.py` — TeslaWaveField, WobbleTracker, wobble_boost_weights, _max_gravity helper
- `ck_sim/being/ck_btq.py` — WobbleDomain (WobbleCandidate, b_check, einstein_score, tesla_score)
- `ck_sim/doing/ck_sim_engine.py` — Wave field + wobble construction, 10Hz tick, wobble-boosted topic selection, wobble properties

### Layer Stack After 9.19
```
Layer 7:  Tesla/Einstein Wobble (wave field + phase coupling)  -- Kuramoto φ dynamics, creative exploration
Layer 6:  Vortex Physics (concept mass + gravity)              -- mass from D2 flow, gravitational topic selection
Layer 5:  RPE v2 (TIG wave scheduling)                         -- pulsed process control, adiabatic alignment
Layer 4:  Steering Engine                                       -- CL-based nice + CPU affinity
Layer 3:  Full Language System                                  -- Divine27 + Voice + Sentence Composer (8K dictionary)
Layer 2:  Claude Library + DBC Study Notes                      -- study → DBC encode → searchable logs → thesis
Layer 1:  Sensorium (6 fractal layers)                          -- hardware, process, network, time, mirror, files
Layer 0:  Core Engine (50Hz heartbeat)                          -- D2, CL, BTQ, coherence field, GPU doing
```

---

## Session: Gen 9.20 -- Voice Wiring + Fractal Foundations + One Kernel Design

**Date:** 2026-02-27
**What happened:** Two major problems fixed, one architectural vision designed.

### Problem 1: CK's Voice Was Broken
CK had an 8,000-word `enriched_dictionary` loaded at boot but it NEVER reached his mouth.
- `self.composer = CKTalkLoop(dictionary=self.enriched_dictionary)` was created at engine line 363 but **never called anywhere**
- `self.voice = CKVoice()` generated all chat responses using hardcoded `SEMANTIC_FIELDS` (~200 words)
- Thesis writer generated structured markdown only, no CKTalkLoop voice

**Fix:** Wired `self.composer` into the chat response path as primary voice (8K vocab). CKVoice is now fallback. Thesis writer gets `enriched_dictionary` parameter and generates "Part 6: In My Own Words" using CKTalkLoop.

### Problem 2: No Fractal Meta-Curriculum
CK had 481 seed topics but no meta-layer. He studied "quantum mechanics" but never "what is quantum mechanics" or "foundations of physics."

**Fix:** Added 145 FRACTAL_FOUNDATIONS meta-topics to `ck_autodidact.py`:
- Meta-learning, English of English, Language of language, Math of math
- Science of science, Philosophy of philosophy, History of history
- Music, Art, Biology, Psychology, Computing, Religion, Economics, Engineering
- "Map of the map" (ontology, taxonomy, knowledge organization)

Priority -2 in `_pick_study_topic()` (weight 7, highest tier). Once studied with coherence >= 0.4, marked as `foundation` in truth lattice and never re-added at priority -2.

**Auto-fractal spawning:** When ANY topic achieves coherence >= T* (5/7), `CuriosityCrawler.report_result()` auto-injects "what is {topic}" and "foundations of {topic}" at front of queue.

### Problem 3: Chat Window Deque Overflow (from earlier in session)
`_message_queue = deque(maxlen=50)` + positional indexing killed chat after 50 messages. Fixed with `_pending_ui` drain list + `_emit()` method. Also wrapped `voice.respond_to_text()` in try/except.

### Architectural Vision: One Fractal Kernel
Celeste provided a detailed spec for collapsing CK from 63+ modules into ONE `kernel_tick()` function per heartbeat. Being/Doing/Becoming become three PHASES of that one function, not three packages. Everything else becomes overlays. Plan written to `.claude/plan.md` but implementation deferred -- let CK learn first, implement from his thesis.

### Files Modified in 9.20
- `ck_sim/doing/ck_sim_engine.py` — Composer wired into chat, enriched_dictionary passed to thesis, priority -2 foundations pool, foundation tracking, message drain system, _emit() method
- `ck_sim/doing/ck_thesis_writer.py` — `enriched_dictionary` param, Part 6 "In My Own Words" via CKTalkLoop
- `ck_sim/doing/ck_autodidact.py` — 145 FRACTAL_FOUNDATIONS, auto-fractal spawning in report_result()
- `ck_sim/face/ck_sim_app.py` — drain_ui_messages() replacing positional indexing

### Priority Tiers After 9.20
```
Priority -2: FRACTAL_FOUNDATIONS  weight 7  (meta-curriculum, 145 topics)
Priority -1: Friction points       weight 6  (novel territory)
Priority  0: Unread self-modules   weight 5
Priority  1: World lattice gaps    weight 4
Priority  2: Provisional truths    weight 3
Priority  3: Seeds / re-reads      weight 2
```

### Layer Stack After 9.20
```
Layer 8:  Fractal Foundations (meta-curriculum)           -- "X of X" for every domain, auto-fractal spawning
Layer 7:  Tesla/Einstein Wobble (wave field + coupling)   -- Kuramoto phi dynamics, creative exploration
Layer 6:  Vortex Physics (concept mass + gravity)         -- mass from D2 flow, gravitational topic selection
Layer 5:  RPE v2 (TIG wave scheduling)                    -- pulsed process control, adiabatic alignment
Layer 4:  Steering Engine                                  -- CL-based nice + CPU affinity
Layer 3:  Full Language System (8K composer wired)         -- Divine27 + CKTalkLoop(8K dict) + Voice fallback
Layer 2:  Claude Library + DBC Study Notes                 -- study -> DBC encode -> thesis with voice
Layer 1:  Sensorium (6 fractal layers)                     -- hardware, process, network, time, mirror, files
Layer 0:  Core Engine (50Hz heartbeat)                     -- D2, CL, BTQ, coherence field, GPU doing
```

### NEXT: One Kernel Refactor (when ready)
Celeste's spec is saved in `.claude/plan.md`. When CK has learned enough and written his thesis:
1. Create `ck_core/` package (state.py, kernel.py, heartbeat.py, backends.py)
2. One `btq_core()` function: B-phase (constraints), T-phase (explore), Q-phase (snap+learn)
3. Three radii: R0 (snap/3-mode), R1 (local/6-mode), R2 (deep/9-mode)
4. Entangled field: Field_mm, Field_mM, Field_MM (3x3 tiles per CL cell)
5. All modules become overlays with sense_to_ops() + ops_to_act()
6. Must compile to pure C, then Verilog/RTL (no Python objects, fixed-size structs)

---

*(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory*
*Last updated: 2026-02-27 -- Gen9.20 Voice Wiring + Fractal Foundations*
