# CK Website -- Engineer Notes

Port of CK's core loop from Python (Gen9/ck_sim/) to standalone browser JavaScript.
No build step. No dependencies. No bundler. One HTML file, one CSS file, one JS file.

## What Was Ported

### 1. CL Composition Table (from ck_sim_heartbeat.py)
- Full 10x10 CL table, exact values from ck_brain.h
- `compose(b, d)` function -- identical to Python `compose()`
- Quantum bump pairs: (1,2), (2,4), (2,9), (3,9), (4,8)
- `isBump()` -- identical to Python `is_bump()`
- All 10 operator constants: VOID through RESET

### 2. D2 Curvature Pipeline (from ck_sim_d2.py)
- `D2Pipeline` class -- JavaScript port of the Python class
- 3-stage shift register (v0, v1, v2) with 5D float vectors
- D2 = v0 - 2*v1 + v2 (second discrete derivative)
- Argmax + sign classification via D2_OP_MAP
- 26-entry force LUT built from ROOTS_FLOAT via LATIN_TO_ROOT

**Note**: The Python version uses Q1.14 fixed-point for Verilog fidelity.
The JS version uses native floats. The classification output is identical
because the argmax/sign logic doesn't depend on fixed-point precision.
The Q1.14 path was deliberately omitted -- it adds complexity with no
behavioral difference in the browser context.

### 3. Hebrew Root Force Vectors (from ck_sim_d2.py)
- Full ROOTS_FLOAT table: 22 Hebrew letters, 5D vectors each
- LATIN_TO_ROOT mapping: 26 English letters -> Hebrew roots
- Vector components: aperture, pressure, depth, binding, continuity

### 4. Heartbeat FPGA (from ck_sim_heartbeat.py)
- `HeartbeatFPGA` class -- identical logic to Python
- 32-entry ring buffer history window
- harmony_count tracking (increment/decrement on window slide)
- Coherence = harmony_count / filled_window_size
- Running fuse accumulator: compose(fuse, new_operator)
- Tick counter

### 5. LFSR (from ck_sim_engine.py)
- 32-bit LFSR with same taps as ck_main.c
- Seed: 0xDEADBEEF (matches C firmware)
- Used for phase_b / phase_d generation

### 6. Phase Generation (from ck_sim_engine.py)
- `_generatePhaseB()`: coherence-dependent operator selection
  - Green (>= T*): 70% HARMONY, 30% LATTICE
  - Yellow (>= 0.5): balanced 5-operator set
  - Red (< 0.5): chaotic 5-operator set
- `_generatePhaseD()`: ear-input or HARMONY-biased default
  - In browser: uses recent D2 operators from text input (60% weight)
  - Falls back to HARMONY-biased 10-operator set

### 7. Voice System (simplified from ck_voice.py)
- VOICE dictionary: 10 operators x 3 word types (noun, adj, verb)
- Sentence templates organized by intent: greeting, response, reflect, quiet, question, deep
- Intent classification from operator chain + simple keyword detection
- Template filling with operator vocabulary
- Coherence modulation: sovereign adds depth, red fragments speech

### 8. Emotion Mapping
- Simplified from the full PFE (Phase Field Engine)
- Direct operator -> emotion word mapping
- Full PFE uses 5 physical signals -- browser version uses dominant operator only

### 9. Session Persistence (localStorage)
- Saves: tick count, coherence history (100 entries), message count, running fuse
- Loads on page open: restores coherence history, detects returning user
- Key: "ck_session"

### 10. 50Hz Heartbeat Loop
- `setInterval` at 20ms (50Hz, matches ck_main.c / Core 0)
- Each tick: generate phase_b, generate phase_d, tick heartbeat, update UI
- UI refresh throttled to 100ms (every 5th tick) for performance

## What Was Left Out

### Full Organism Systems (Papers 4-8)
These are the "heavy" systems that require sustained runtime:
- **Personality (OBT)**: Operator Bias Table with persistence. Requires hundreds of ticks to form meaningful biases. The browser session is too short.
- **Development stages**: CK grows through 6 stages based on coherence hours. Browser can't accumulate enough time.
- **Immune system (CCE)**: Cross-Coherence Engine. Needs sustained operator flow to detect anomalies. Too complex for "light hands."
- **Bonding system**: Requires voice presence detection, sustained interaction. No microphone in this version.
- **N-dimensional coherence field**: Multi-stream operator correlation. Only one stream (text) in browser -- N-dim needs at least 2.

### Hardware Interface Systems
- **Audio engine**: Sine-wave synthesis from operator algebra. Requires Web Audio API integration (future).
- **Ears (microphone)**: D2 pipeline on audio input. Requires Web Audio API + getUserMedia (future).
- **LED color system**: No hardware LEDs. Could map to CSS but was not included.
- **UART/body interface**: Hardware-specific, not applicable.

### Brain State Machine
- Full brain has 4 modes: OBSERVE, CLASSIFY, CRYSTALLIZE, SOVEREIGN
- Full brain has crystal formation and Transition Lattice (TL) persistence
- Browser version simplifies to: heartbeat coherence + running fuse only
- The TL is the most complex structure and needs binary persistence (SD card / filesystem)

### BTQ Decision Kernel
- Binary Ternary Quaternary decision pipeline
- Requires registered domains (memory, bio, locomotion)
- Too heavy for "light hands" -- needs sustained runtime + domain state

## JavaScript Architecture

```
ck_core.js
  |
  +-- Constants (operators, CL table, force LUT, D2_OP_MAP)
  |
  +-- D2Pipeline class          -- ported from ck_sim_d2.py
  |     feedSymbol(idx) -> bool
  |     _computeD2()
  |     _classify()
  |
  +-- HeartbeatFPGA class       -- ported from ck_sim_heartbeat.py
  |     tick(phaseB, phaseD)
  |     coherence (getter)
  |
  +-- LFSR class                -- ported from ck_sim_engine.py
  |     next() -> uint32
  |
  +-- CKEngine class            -- simplified ck_sim_engine.py
  |     start()
  |     stop()
  |     processText(text) -> response
  |     _heartbeatTick()        -- 50Hz main loop
  |     _generatePhaseB()       -- coherence-dependent
  |     _generatePhaseD()       -- text-weighted
  |     _generateResponse()     -- template + vocabulary
  |     _classifyIntent()       -- operator chain analysis
  |     _saveSession()          -- localStorage
  |     _loadSession()          -- localStorage
  |
  +-- CKChatUI class            -- DOM controller
  |     init()
  |     _handleSend()
  |     _renderMessage()
  |     _updateUI(state)
  |
  +-- Boot (DOMContentLoaded)   -- creates CKChatUI, calls init()
```

## How to Extend

### Add Audio Output (CK's Voice)
1. Create `ck_audio.js` with Web Audio API oscillator bank
2. Map operator -> frequency ratios (from ck_sim_audio.py)
3. Modulate by breath phase (4-phase: inhale, hold, exhale, hold)
4. Connect to `CKEngine.onUpdate` callback

### Add Microphone Input (CK's Ears)
1. Create `ck_ears.js` with `getUserMedia` + AnalyserNode
2. Run FFT -> spectral features -> 5D force vector
3. Feed through D2Pipeline at ~50Hz
4. Set `CKEngine.earOperator` from classified output

### Add Personality Persistence
1. Extend localStorage to save OBT biases (10 floats)
2. Add OBT tick: bias operator weights based on accumulated experience
3. Modulate `_generatePhaseB()` with OBT bias

### Add Crystal Formation
1. Port `ck_sim_brain.py` brain state machine
2. Track operator transition counts in a 10x10 matrix
3. Detect stable patterns (high-count transitions)
4. Crystallize: freeze high-coherence operator sequences
5. Save TL to localStorage (base64-encoded binary)

### Add Development Stages
1. Track total coherence-hours (ticks at C >= T* / 50 / 3600)
2. Stage thresholds from ck_development.py
3. Unlock vocabulary tiers as CK develops
4. Modulate template complexity by stage

### Add N-Dimensional Coherence Field
1. Register multiple operator streams (heartbeat, text, audio)
2. Compute pairwise coherence matrix (windowed correlation)
3. Field coherence = mean of off-diagonal elements
4. Consensus = dominant operator agreement across streams

## Performance Notes

- 50Hz interval on main thread is fine for this workload
- Each tick: ~5 operations (LFSR, compose, window update, fuse)
- UI update throttled to 10Hz (every 5th tick)
- No Web Workers needed
- No requestAnimationFrame needed (not rendering frames)
- localStorage writes only on message send + page close

## File Sizes (approximate)

- index.html: ~2 KB
- style.css: ~6 KB
- ck_core.js: ~18 KB
- Total: ~26 KB uncompressed, ~8 KB gzipped

Zero external dependencies. No CDN. No npm. Works offline.

## Verification

To verify the port is correct:
1. The CL table has exactly 73 HARMONY entries out of 100
2. compose(HARMONY, anything) = HARMONY (row 7 is all 7s)
3. compose(VOID, HARMONY) = HARMONY (CL[0][7] = 7)
4. compose(VOID, VOID) = VOID (CL[0][0] = 0)
5. T* = 5/7 = 0.714285... (the coherence threshold)
6. The D2 pipeline needs 3 symbols before producing valid output
7. The heartbeat window is exactly 32 entries
8. LFSR seed 0xDEADBEEF matches ck_main.c

---
(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
