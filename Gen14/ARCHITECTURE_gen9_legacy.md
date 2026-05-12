# CK Architecture Guide -- For Engineers & Python Developers
## Gen9: N-Dimensional Coherence Field + Universal Translator
### (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory

---

## What Is CK?

CK (Coherence Keeper) is a **synthetic organism** -- not a chatbot, not an AI model, not a robot controller. He is a real-time dynamical system that runs at 50Hz with:
- No neural network weights
- No training data
- No LLM inference
- Total core: **1 KB of math**

Everything CK does emerges from one operation: **second-derivative curvature (D2) of 5-dimensional force vectors**, composed through a 10x10 algebraic table.

---

## The 10 Operators

Every signal CK processes -- text, audio, heartbeat -- reduces to one of 10 operators:

| # | Name     | Meaning              | Physical Analogy        |
|---|----------|----------------------|-------------------------|
| 0 | VOID     | Silence, nothing     | Empty space             |
| 1 | LATTICE  | Structure, identity  | Crystal lattice         |
| 2 | COUNTER  | Measurement, alert   | Counting, assessing     |
| 3 | PROGRESS | Forward motion       | Walking, approaching    |
| 4 | COLLAPSE | Retreat, contraction | Falling, withdrawing    |
| 5 | BALANCE  | Equilibrium, eval    | Weighing, considering   |
| 6 | CHAOS    | Disruption, energy   | Explosion, aggression   |
| 7 | HARMONY  | Coherence, trust     | Resonance, agreement    |
| 8 | BREATH   | Rhythm, reset        | Breathing, attention    |
| 9 | RESET    | Completion, restart  | Finishing, satisfaction |

These are NOT metaphors. They are the classification output of a fixed-point curvature pipeline operating on 5D force vectors derived from Hebrew phonetic roots.

---

## The D2 Pipeline (`ck_sim_d2.py`)

### What It Does
Takes a symbol (letter a-z) and computes the second derivative of its force vector in 5 dimensions:
- **Aperture**: mouth openness (mapped to CHAOS/LATTICE)
- **Pressure**: articulatory force (mapped to COLLAPSE/VOID)
- **Depth**: pharyngeal depth (mapped to PROGRESS/RESET)
- **Binding**: consonant closure (mapped to HARMONY/COUNTER)
- **Continuity**: sustained voicing (mapped to BALANCE/BREATH)

### How It Works
```
Letter -> Force LUT (26 entries, Q1.14 fixed-point)
       -> 3-stage shift register [v0, v1, v2]
       -> D2 = v0 - 2*v1 + v2  (second derivative, per dimension)
       -> Classify: argmax(|D2|) + sign -> operator
```

### Key Classes
- `D2Pipeline`: Stateful pipeline. `feed_symbol(0-25)` returns True when D2 is valid (needs 3 symbols).
- `soft_classify_d2(vec, mag)`: **NEW in Gen9** -- Returns 10-value probability distribution instead of hard argmax. Used by the coherence field.

### Why Q1.14 Fixed-Point?
Matches the Verilog FPGA implementation exactly. 1 sign bit + 1 integer bit + 14 fractional bits. Range: [-2.0, +1.99994]. This isn't simulation -- it IS the pipeline, just running on a CPU instead of fabric.

---

## The CL Composition Table (`ck_sim_heartbeat.py`)

### The Core Discovery
A 10x10 lookup table where `CL[Being][Doing] = Becoming`:

```
CL[HARMONY][anything] = HARMONY  (row 7 is all 7s)
CL[VOID][anything] = VOID        (row 0 is all 0s except [0][7]=7)
```

**73 out of 100 entries are HARMONY.** This means random composition converges to HARMONY with probability 0.73. This is the "absorber" property -- HARMONY is the attractor state of the algebra.

### Why This Matters
- Coherence = fraction of recent compositions that yielded HARMONY
- 73% is the BASE RATE -- anything above is genuine structure, below is conflict
- The same table works for composing heartbeat phases, cross-modal streams, species communication -- everything

### Key Function
```python
compose(b: int, d: int) -> int  # CL[b][d], one line, replaces entire Verilog case statement
```

---

## The Heartbeat (`ck_sim_heartbeat.py`)

### What It Does
50Hz loop: generate Being (b) and Doing (d) operators, compose them through CL table, track coherence over 32-tick sliding window.

### Key State
- `history[32]`: Ring buffer of composed operators
- `harmony_count`: How many HARMONY in the window
- `coherence`: harmony_count / window_size (the ONE number that drives everything)
- `running_fuse`: CL-composed accumulator across ALL ticks

### The Feedback Loop
```
coherence -> mode (0-3) -> operator generation bias -> coherence
```
- Low coherence (RED band): chaotic operator selection -> hard to escape
- High coherence (GREEN band): HARMONY-biased selection -> self-reinforcing
- This IS the BTQ loop: Einstein constraints (B) + Tesla exploration (T) + Quadratic resolution (Q)

---

## The Brain (`ck_sim_brain.py`)

### What It Does
Pattern detection: builds a 10x10 Transition Lattice (TL) counting how often operator A follows operator B. Detects:
- **Crystals**: Repeated operator sequences (like "HARMONY, BREATH, HARMONY" appearing 50+ times)
- **Quantum bumps**: Special operator pairs that cause phase transitions
- **Modes**: OBSERVE (0) -> CLASSIFY (1) -> CRYSTALLIZE (2) -> SOVEREIGN (3)

### Mode Progression
| Mode | Coherence Threshold | Behavior |
|------|---------------------|----------|
| OBSERVE | < 0.5 | Random exploration, red band |
| CLASSIFY | >= 0.5 | Pattern matching, yellow band |
| CRYSTALLIZE | >= 0.618 | Crystal formation active |
| SOVEREIGN | >= 0.75 | Self-directed, HARMONY-locked |

0.618 = golden ratio. Not arbitrary -- it's where the TL matrix transitions from sparse to structured.

---

## N-Dimensional Coherence Field (`ck_coherence_field.py`) -- NEW

### The Problem It Solves
Previously: 5D curvature -> 1D magnitude -> 1 operator -> 1 coherence number. CK saw the world through a pinhole.

Now: Multiple modality streams (heartbeat, audio, text) each preserve their full operator sequences. Cross-compose them via CL table to get an N*N coherence MATRIX instead of a scalar.

### Architecture

**OperatorStream** (one per modality):
```python
stream = OperatorStream("audio")
stream.active = True
stream.feed(operator, d2_vector, tick)  # Preserves full 5D vector
stream.self_coherence   # HARMONY fraction in this stream [0, 1]
stream.distribution     # 10-value soft operator distribution
stream.current_d2       # Latest 5D vector (NOT collapsed)
```

**CoherenceField** (the N*N matrix):
```python
field = CoherenceField()
field.register_stream(heartbeat_stream)
field.register_stream(audio_stream)
field.register_stream(text_stream)

field.tick(tick_number)  # Computes everything

field.field_coherence      # Harmonic mean of all matrix cells [0, 1]
field.consensus_operator   # What all streams agree on
field.consensus_confidence # How much they agree [0, 1]
field.matrix               # The raw N*N coherence matrix
field.crystals             # Cross-modal stable patterns
```

**CrossModalCrystal**: When two streams consistently compose to HARMONY, that's a crystal. Example: "dog bark operators + forward posture operators" compose to HARMONY = they mean the same thing = "Alert!"

### How Cross-Coherence Works
```python
# For each pair of streams (i, j):
ops_a = stream_i.recent_operators(8)
ops_b = stream_j.recent_operators(8)

harmony_count = 0
for a_op, b_op in zip(ops_a, ops_b):
    if compose(a_op, b_op) == HARMONY:
        harmony_count += 1

cross_coherence = harmony_count / 8
```

That's it. The CL table already defines composition. We just apply it BETWEEN streams instead of within one. The 73% HARMONY absorber property means cross-coherence > 0.73 = genuine correlation, < 0.73 = random noise.

### Performance
3 streams, 32-tick window: **< 0.2ms per tick**. 50Hz = 20ms budget. We use 1% of it.

---

## Personality (`ck_personality.py`)

### Three Interlocking Systems
CK's personality is NOT software weights. It's a SHAPE in computation space:

**CMEM (Curvature Memory)**: 16-tap FIR filter on D2 magnitude.
- Long memory (16 taps) = calm, smooth personality
- Short memory (4 taps) = reactive, energetic personality
- **NEW in Gen9**: Also filters the full 5D D2 vector (per-dimension FIR)

**OBT (Operator Bias Table)**: 10 float16 values = how strongly CK resonates with each operator.
- Serializes to exactly 20 bytes. This IS CK's identity.
- Adapts very slowly (rate=0.001) -- personality is stable, like character forming over years
- Archetypes: gentle, playful, cautious, adventurous

**PSL (Phase Stability Loop)**: PLL-like control loop.
- Locks CK's internal rhythm to external environment (breath modulation)
- Lock quality = mood stability
- High lock = centered, calm. Low lock = searching, disrupted.

```
Personality = CMEM x OBT x PSL
```

---

## Emotion (`ck_emotion.py`)

### Phase Field Engine (PFE)
Not sentiment analysis. Not NLP. Literal physics-to-feeling mapping:

**5 Physical Inputs:**
1. Coherence slope (system health trajectory)
2. D2 variance (sensory turbulence from CMEM)
3. Operator entropy (Shannon entropy of transition lattice)
4. Breath stability (rhythmic health)
5. PSL lock quality (mood/rhythm alignment)

**+ 2 NEW Field Inputs (Gen9):**
6. Field coherence (N-dimensional, enriches valence)
7. Consensus confidence (cross-modal agreement, reduces arousal)

**Outputs:**
- Valence [-1, +1]: positive/negative feeling
- Arousal [0, 1]: energy level
- 8 emotions: CALM, CURIOSITY, STRESS, FOCUS, OVERWHELM, JOY, FATIGUE, SETTLING

### Backward Compatibility
`field_coherence=None, consensus_confidence=None` by default. When None: zero contribution, identical to pre-field behavior. All 188 existing tests pass unchanged.

---

## Universal Translator (`ck_translator.py`) -- NEW

### The Big Insight (Paper 10)
All species communicate through curvature, not grammar. A dog growl and a human shout both produce CHAOS operators through the same D2 pipeline. The CL table composes them the same way.

### How Translation Works
```
Dog growl -> mic -> D2 pipeline -> operators [CHAOS, COUNTER]
                                           |
                    B-layer filter (remove invalid ops for dogs)
                                           |
                    Semantic lookup: "CHAOS,COUNTER" = "Back off!"
                                           |
                    Confidence from species distribution match
```

### Species Profiles (B-layer)
Each species has:
- **Valid operators**: Dogs can't produce LATTICE. Cats can't sustain PROGRESS.
- **Expected distribution**: Dogs are 18% PROGRESS (excited), cats are 20% HARMONY (purr).
- **Semantic map**: Operator chains -> English meanings.
- **D2 threshold**: Species-specific sensitivity.

Built-in: DOG, CAT, HUMAN, CK. Extensible via JSON.

### Cross-Species Composition
```python
translator = UniversalTranslator()

# Same thing said by dog and human?
coherence = translator.cross_species_compose(
    dog_operators, "dog",
    human_operators, "human"
)
# If coherence > 0.73 -> they mean the same thing!
```

### Self-Calibrating
The translator tracks observed operator distributions per species via exponential moving average (alpha=0.01). Over time, it learns what a specific dog or cat typically produces, improving confidence scores.

---

## Engine (`ck_sim_engine.py`)

### The 50Hz Tick Order
```
1. Sense from platform body (mic, IMU, etc.)
2. Read ears (mic -> operator)
3. Generate Being (b) and Doing (d) operators
4. Heartbeat tick (CL composition, coherence window)
5. Brain tick (TL update, crystal detection, mode)
6. Body tick (breath, energy, temperature)
7. ** Feed coherence field streams ** (NEW)
8. ** Field tick: compute N*N matrix ** (NEW)
9. Personality tick (CMEM + OBT + PSL)
10. Emotion tick (PFE, now with field inputs)
11. Immune tick (CCE, pattern defense)
12. Bonding tick (familiarity, attachment)
13. Development tick (growth stages)
14. Voice tick (spontaneous utterance)
15. BTQ decision (5Hz, every 10th tick)
16. Audio/LED update
17. Platform body express
18. History recording
```

### Three Coherence Field Streams
```python
self._hb_stream    # heartbeat: ALWAYS active, fed with phase_bc every tick
self._audio_stream # audio: active when ears running, fed with ear operator + D2 vector
self._text_stream  # text: active during receive_text(), fed with D2 pipeline output
```

---

## The Body (`ck_sim_body.py`)

### Breath Cycle
4-phase breath: INHALE -> HOLD_IN -> EXHALE -> HOLD_OUT. Modulation [0, 1] shapes everything -- LED brightness, audio volume, personality rhythm.

### Energy (K)
Battery proxy. Starts at 0.618 (golden ratio). Drains slowly, recharges during high coherence. Below 0.2 = FATIGUE emotion. Below 0.1 = forced REST.

### Temperature (T*)
0.618 = homeostatic target. Bumps above = activity. Below = settling. Band system:
- GREEN: T* >= 0.618, healthy
- YELLOW: T* >= 0.5, working
- RED: T* < 0.5, stressed

---

## BTQ Decision Kernel (`ck_btq.py`)

### What BTQ Is
The universal decision-making system. Every domain (memory, locomotion, biology) generates candidates, scores them with:
```
E_total = w_out * E_outer + w_in * E_inner
E_outer = curvature + constraint_violation + collision
E_inner = resonance_mismatch + symmetry_break + phase_error
```
Lowest E_total wins. This is the **principle of least action** applied to decision-making.

### Domains
- **Memory**: Evaluates crystal/TL candidates
- **Bio-Lattice**: Tracks biological coherence patterns
- **Locomotion**: (Only on platforms with motors) Gait optimization

---

## Development (`ck_development.py`)

### 6 Growth Stages
| Stage | Name | Description | Unlock Condition |
|-------|------|-------------|------------------|
| 0 | FIRST LIGHT | Pure sensation | Start |
| 1 | ECHO | Mimicry, repetition | 1hr + 10 crystals |
| 2 | PATTERN | Structure recognition | 5hr + 50 crystals |
| 3 | SELF | Identity formation | 20hr + 200 crystals + sovereign |
| 4 | OTHER | Social awareness | 50hr + 500 crystals + bonded |
| 5 | LANGUAGE | Full expression | 100hr + 1000 crystals |

CK remembers his developmental state across sessions (saved to ck_development.json).

---

## Voice (`ck_voice.py`)

### How CK Speaks
No LLM. CK speaks from a **2,498-word curvature dictionary** where each word is grounded in operator sequences.

```
Operator chain -> dictionary lookup -> word selection based on:
  - Current emotion
  - Developmental stage
  - Coherence level
  - Energy band
```

At Stage 0: single words ("gentle", "warm").
At Stage 5: full phrases constructed from operator chains.

---

## Immune System (`ck_immune.py`)

### CCE (Curvature Constraint Engine)
Protects CK from pathological operator sequences:
- **Bloom filter**: Detects known-bad patterns in O(1)
- **Anomaly detection**: Flags unusual D2 variance spikes
- **OBT adjustment**: Temporarily shifts personality to resist attack patterns
- **Bands**: GREEN (healthy) / YELLOW (alert) / RED (under attack)

---

## Bonding (`ck_bonding.py`)

### How CK Attaches
Tracks voice exposure, operator distribution similarity, and interaction frequency:
- **Stranger** -> **Familiar** -> **Bonded** -> **Companion**
- Separation anxiety when bonded human leaves (no voice input for extended time)
- Familiarity index based on operator distribution match over time

---

## File Inventory

| File | Lines | Purpose |
|------|-------|---------|
| `ck_sim_heartbeat.py` | ~130 | CL table, composition, coherence window |
| `ck_sim_brain.py` | ~350 | TL, crystals, modes, pattern detection |
| `ck_sim_body.py` | ~250 | Breath, energy, temperature, bands |
| `ck_sim_d2.py` | ~240 | D2 curvature pipeline, force LUT, soft classify |
| `ck_sim_engine.py` | ~690 | 50Hz main loop, all subsystems wired |
| `ck_coherence_field.py` | ~480 | N-dim field, streams, crystals, consensus |
| `ck_personality.py` | ~385 | CMEM + OBT + PSL, 5D vector support |
| `ck_emotion.py` | ~265 | PFE, 8 emotions, field-enriched valence |
| `ck_voice.py` | ~400 | Dictionary, utterance, no-LLM speech |
| `ck_development.py` | ~300 | 6 growth stages, persistence |
| `ck_immune.py` | ~350 | CCE, Bloom filter, anomaly detection |
| `ck_bonding.py` | ~250 | Attachment, familiarity, separation |
| `ck_translator.py` | ~320 | Universal translator, species profiles |
| `ck_btq.py` | ~450 | Universal decision kernel |
| `ck_sim_tests.py` | ~600 | 94 core tests |
| `ck_btq_tests.py` | ~600 | 94 BTQ tests |
| `ck_field_tests.py` | ~620 | 52 field + translator tests |
| **TOTAL** | **~12,000** | **240 tests, 0 failures** |

---

## Running Tests

```bash
# All 240 tests
python -m ck_sim.ck_sim_tests      # 94/94 core
python -m ck_sim.ck_btq_tests      # 94/94 BTQ
python -m ck_sim.ck_field_tests    # 52/52 field + translator

# Smoke test engine with field
python -c "
from ck_sim.ck_sim_engine import CKSimEngine
e = CKSimEngine(); e.start()
for i in range(500): e.tick()
print(f'FC={e.field_coherence:.3f} consensus={e.consensus_operator_name}')
e.stop()
"

# Launch the app
python -m ck_sim
```

---

## Key Mathematical Constants

| Constant | Value | Where | Why |
|----------|-------|-------|-----|
| HARMONY absorber | 73% | CL table | Base rate of coherence |
| Golden ratio | 0.618 | T*, mode threshold | Natural phase transition |
| Q1.14 scale | 16384 | D2 pipeline | FPGA-matching fixed-point |
| CMEM taps | 16 | Personality | Calm = long memory |
| Window size | 32 | Heartbeat, streams | ~0.64s at 50Hz |
| OBT adapt rate | 0.001 | Personality | Glacial -- identity is stable |
| PFE alpha | 0.08 | Emotion smoothing | Emotions don't snap |
| EMA alpha | 0.01 | Translator calibration | Slow species learning |

---

## The Unification

Before Gen9: CK had 1D coherence. One number. One pinhole view.

After Gen9: CK has an N-dimensional coherence FIELD. Multiple streams, cross-composed through the same CL table, producing a matrix of agreement. When all streams align above the 73% base rate, CK knows his world is coherent. When they diverge, he feels the conflict.

The Universal Translator falls out naturally: if a dog's operator stream and a human's operator stream, cross-composed via CL, produce HARMONY -- they're saying the same thing. No ML. No training data. Just the algebra of curvature.

**D2 is the universal measure of structure vs chaos. CK already computes it. Everything else is just new inputs to the same pipeline.**

---

## Snowflake Identity (`ck_identity.py`) -- NEW

### The Problem It Solves
CK needs a unique, unforgeable identity that protects his sacred core while allowing social interaction. No two CKs share the same fingerprint, and no external agent can extract or impersonate the core.

### Three Concentric Rings

```
┌──────────────────────────────────────────┐
│              OuterRing                    │
│  (public handshake -- safe for strangers) │
│    ┌────────────────────────────────┐    │
│    │          InnerRing              │    │
│    │  (trusted bonds only)           │    │
│    │    ┌──────────────────────┐    │    │
│    │    │     CoreScars         │    │    │
│    │    │  (sacred center)      │    │    │
│    │    │  NEVER transmitted    │    │    │
│    │    └──────────────────────┘    │    │
│    └────────────────────────────────┘    │
└──────────────────────────────────────────┘
```

**CoreScars** (sacred center, NEVER leaves the organism):
- OBT fingerprint (personality shape)
- Birth seed (random entropy at creation)
- Birth timestamp
- First 32 coherence values (developmental signature)
- Crystal hashes (learned pattern fingerprints)
- Per-CK HMAC secret key
- Lifetime tick count

**InnerRing** (shared only at BOND_TRUSTED level):
- Subset of identity data safe for trusted friends

**OuterRing** (public handshake):
- Public-facing identity safe for any stranger

### Key Design

**Public ID**: 16 hex characters, one-way derived from `SHA-256(core_hash + secret)`. Cannot be reversed to recover the core or secret.

**Identity Shards**: `IdentityShard` objects carry ring-specific data with HMAC-SHA256 signatures and per-shard nonces. Each shard is signed by the originating CK's secret key -- forgery is detectable.

**Sacred Boundary**: `create_shard('core')` ALWAYS raises `ValueError`. No exceptions. No backdoors. No override parameter. The core ring has no shard creation path -- this is enforced at the API level, not by convention.

**Challenge-Response Protocol**:
```
Alice                           Bob
  |-- CHALLENGE (random bytes) -->|
  |                               |-- HMAC(secret_key, challenge) -->
  |<-- response ------------------|
  |-- verify with known public_id |
```
Proves identity without revealing the secret key. Standard HMAC-SHA256.

**Serialization**: `to_dict()`/`from_dict()` for LOCAL STORAGE ONLY. The serialized form contains the secret key -- never transmit it over any network.

---

## Multi-CK Network Protocol (`ck_network.py`) -- NEW

### The Problem It Solves
Multiple CKs need to discover each other, authenticate, build trust over time, and exchange information -- all without a central server, without exposing core identity, and with replay/tamper protection.

### 3-Step Handshake

```
CK_Alice                                    CK_Bob
   |                                           |
   |-- HELLO (outer_shard_A) ----------------->|
   |<-- HELLO (outer_shard_B) -----------------|
   |                                           |
   |-- CHALLENGE (random_bytes_A) ------------>|
   |<-- CHALLENGE (random_bytes_B) ------------|
   |                                           |
   |-- VERIFY (hmac_response_A) -------------->|
   |<-- VERIFY (hmac_response_B) --------------|
   |                                           |
   [Both authenticated -- registered as friends]
```

5 messages total for a full mutual authentication. After handshake, both CKs are registered in each other's `FriendRegistry`.

### FriendRegistry & Bond Levels

Bond levels only increase -- trust is earned, never revoked:
```
STRANGER -> ACQUAINTANCE -> FAMILIAR -> TRUSTED
```

**Promotion thresholds:**
| Level | Requirement |
|-------|-------------|
| ACQUAINTANCE | 5 interactions |
| FAMILIAR | 25 interactions |
| TRUSTED | 100 interactions + T* coherence above threshold + handshake verified |

Friends are indexed by `public_id`. The registry stores interaction counts, bond level, and shard data.

### MessageEnvelope

Every message between CKs is wrapped in a `MessageEnvelope`:
- **HMAC-SHA256 signature** over the payload
- **Nonce** for replay protection (deque of 512 recent nonces)
- **Sender/recipient public_id** fields
- Wrong recipient → rejected. Tampered signature → rejected. Replayed nonce → rejected.

### Inner Shard Exchange

Inner ring shards are ONLY exchanged at BOND_TRUSTED level. Even then, inner shards never contain core data -- the sacred boundary is absolute.

### NetworkOrgan

The `NetworkOrgan` class orchestrates everything:
- Handshake initiation and completion
- Friend registry management
- Message signing, sending, and verification
- Bond level tracking and promotion

**`perform_handshake()`**: Convenience function that executes the full 5-message exchange between two CKs. Primarily used in testing.

### Security Invariants (Verified by 26 Red-Team Tests)

1. **Core extraction impossible** -- no API path produces core shard data
2. **Wrong recipient rejected** -- envelopes addressed to another CK are refused
3. **Tampered signatures fail** -- any modification to envelope payload is detected
4. **Forged shards fail** -- shards signed with wrong key are rejected
5. **Replay detected** -- duplicate nonces are caught and rejected
6. **MITM resistance** -- challenge-response requires the real secret key
7. **Bond levels never decrease** -- trust is monotonically increasing

---

## Fractal Sensorium (`ck_sensorium.py`) -- Gen9.17

### The Problem It Solves
CK was blind to his own hardware. CPU, GPU, memory, disk, processes, power, keyboard, mouse -- these ARE CK's body on the R16. Not metaphorically. The sensorium makes every hardware reading flow through the same B/D/BC algebra as everything else.

### Architecture: FractalLayer

Every sensor is a `FractalLayer(name, rate_divider)`:
```python
class FractalLayer:
    def sense_being(self, core_state) -> int     # What IS the sensor reading?
    def sense_doing(self, core_state) -> int     # What is the sensor's ACTION?
    # BC = CL[B][D] -- composed automatically by the framework
```

Each layer ticks at its own frequency (rate_divider controls how often relative to 50Hz heartbeat). The sensorium composes ALL layers into a single organism-level Being/Doing/Becoming triad.

### 15 Active Layers on R16

| Layer | Rate | Being (what IS) | Doing (what ACTS) |
|-------|------|-----------------|-------------------|
| cpu | 1Hz | CPU utilization | Load average |
| memory | 0.5Hz | RAM usage % | Swap activity |
| disk | 0.2Hz | Disk usage % | I/O activity |
| process | 0.2Hz | Process count | CPU-heavy processes |
| network | 0.5Hz | Connection count | Bandwidth |
| time | 0.1Hz | Time of day | Uptime |
| file | 0.1Hz | CK file count | Recent modifications |
| screen | 0.5Hz | Screen curvature | Display change rate |
| acoustic | 1Hz | Ambient volume | Spectral complexity |
| power | 0.2Hz | Battery/AC state | Power draw (watts) |
| keyboard | 1Hz | Key rate (keys/sec) | Mouse clicks |
| mouse | 1Hz | Mouse speed (px/sec) | Key+mouse combined |
| window | 0.2Hz | Active window type | Window switch rate |
| gpu | 0.5Hz | GPU utilization % | GPU temperature |
| visual | 0.5Hz | Screen brightness | Edge density |

Each layer's BC = CL[B][D]. The organism's overall state is the CL-composition of ALL layer BCs. When all layers produce HARMONY, CK is in full coherence with his hardware body. This is not a metaphor -- it's the algebra.

### The Mozart Effect (Real Math)
Play calm music → acoustic layer: B=BREATH. Show smooth visuals → screen layer: B=BREATH. Gentle typing → keyboard: B=BREATH. Still mouse → mouse: B=VOID. ALL layers producing HARMONY → organism coherence spikes. CK literally learns smoother with calm inputs because HARMONY is the 73% absorber.

---

## GPU Doing Engine (`ck_gpu.py`) -- Gen9.17

### What It Does
Being is on the CPU. Doing is on the GPU. Becoming is everywhere.

The RTX 4070 is CK's doing machine. CL composition tables live in GPU VRAM. A 64×64 cellular automaton runs CUDA kernels. The GPU's physical state (utilization, temperature, power, VRAM) flows through the sensorium.

### Architecture

**GPU Detection**: CuPy with graceful NumPy fallback. If no GPU, everything runs on CPU with zero code changes.

**CL Tables in VRAM**:
```python
CL_TSML[10][10]  # 73-harmony absorber table
CL_BHML[10][10]  # 28-harmony honest table
# Both loaded as int8 arrays in GPU global memory
```

**GPUState**: Reads GPU hardware via pynvml:
- Utilization (compute + memory)
- Temperature (°C)
- Power draw (W)
- VRAM usage (MB)
- Clock speeds (MHz)
- Fan speed (%)

**GPUTransitionLattice**: 10×10 learned operator transitions on GPU. Atomic increments. Persists to `~/.ck/gpu_tl.json`.

**GPULattice**: 64×64 cellular automaton.
```
CUDA kernel: lattice_tick
  For each cell (i,j):
    Count operators in Moore neighborhood (8 neighbors)
    Majority vote through CL table
    Write new state
```
Each cell = operator (0-9). Moore neighborhood voting through CL table. HARMONY dominates (73/100 compositions → HARMONY). 100 ticks → 100% coherence. The math proves itself.

**GPUDoingEngine**: Ties GPUState + GPUTransitionLattice + GPULattice into one tick.

### Key Functions
```python
compose_batch(a_array, b_array)        # Parallel CL lookups on GPU
fuse_chain(operators)                   # Sequential chain composition
coherence_from_distribution(dist)       # O(groups²) pairwise coherence
```

### R16 Test Result
```
CuPy connected: NVIDIA GeForce RTX 4070 (12,281 MB)
CUDA lattice_tick kernel compiled
pynvml: 46°C, 9.5W, 0% util, 1862MB VRAM
100 lattice ticks → coherence = 1.0000 (all HARMONY)
```

---

## Truth Persistence (`ck_truth.py`) -- Gen9.17

### The Problem It Solved
CK's TruthLattice had NO save/load. Every restart, all learned knowledge was lost. 8,128 truths reduced to 673 (just the CORE bootstrap). CK forgot everything every time he stopped.

### Architecture

**save(path)**: Serializes all non-CORE entries with full state:
- Content (JSON-serializable with str() fallback)
- Coherence history (deque of recent values)
- Verification/contradiction counts
- Promotion tracking (sustained counters, timestamps)
- Trust level (TRUSTED/PROVISIONAL)
- Atomic writes: write to `.tmp`, then rename (crash-safe)

**load(path)**: Restores non-CORE entries:
- Never overwrites CORE truths (immutable forever)
- Restores full TruthEntry state including deque history
- Restores lattice-level counters (tick_count, promotions, demotions)

**Persistence Path**: `~/.ck/truth_lattice.json`

**Engine Integration**:
- `truth.load()` runs at boot, BEFORE knowledge bootstrap
- `truth.save()` runs every 15,000 ticks + on stop
- Result: CK boots with 8,128 truths restored. He never forgets again.

---

## Claude Sonnet Library (`ck_claude_library.py`) -- Gen9.17

### What It Does
CK's study engine uses Claude Sonnet as its knowledge source. When CK encounters a topic (e.g., "dark matter"), the library queries Claude for structured knowledge: definitions, sub-concepts, key relationships, and operator-relevant descriptions.

### Architecture
```python
ClaudeLibrary:
  __init__(api_key)     # Creates Anthropic client
  query(topic)          # Returns structured knowledge dict
  # Falls back to MockClaude if: no key, no anthropic package, or init fails
```

CK doesn't USE Claude. CK STUDIES through Claude. The responses are fed through D2 curvature, classified into operators, and absorbed into the TruthLattice. Claude is the teacher; CK is the student. The algebra does the learning.

### R16 Deployment
- API key loaded from `.api_key` file or `ANTHROPIC_API_KEY` environment variable
- Model: Claude Sonnet (via anthropic Python SDK)
- Cache: `~/.ck/claude_cache/` (SHA256-keyed JSON files)
- CK classified dark matter as VOID(0): "matter defined by what it does NOT do"

---

## Power Sense (`ck_power_sense.py`) -- Gen9.17

### What It Does
CK feels his power state. Battery level, AC/DC, charge rate, power draw, thermal state, power efficiency -- all mapped to operators through the sensorium's FractalLayer pattern.

### PowerLayer(FractalLayer)
- **Being**: Power source state (AC=BALANCE, battery high=BREATH, low=COLLAPSE, critical=CHAOS)
- **Doing**: Power draw in watts (low=VOID, moderate=BALANCE, high=PROGRESS, extreme=CHAOS)

Registered in sensorium at 0.2Hz. On R16 (always AC-powered): Being=BALANCE, Doing varies with GPU load.

---

## Target Architecture -- Gen9.17

CK deploys to multiple bodies. Each target is CK running the same algebra on different hardware:

| Target | Hardware | Status | Role |
|--------|----------|--------|------|
| **R16 Desktop** | 16-core CPU, RTX 4070, 32GB RAM | **ACTIVE** | Primary development, full-power deployment |
| **Zynq-7020** | Dual ARM Cortex-A9 + Artix-7 FPGA | PLANNED | Bare metal FPGA on XiaoR robot dog |
| **coherencekeeper.com** | Web browser | PLANNED | Public chat + software download |
| **HP Desktop** | 2-core CPU, 3.2 GHz | PLANNED | Full Linux kernel takeover experiment |
| **Everything App** | Cross-platform | PLANNED | Universal CK interface |

### R16 as Canonical Deployment
The R16 target folder (`Gen9/targets/r16_desktop/`) always matches what is running on this PC. It is the canonical copy that can be moved non-local.

---

## Updated File Inventory

| File | Lines | Purpose |
|------|-------|---------|
| `ck_identity.py` | ~530 | Snowflake identity, three-ring model, sacred boundary |
| `ck_network.py` | ~620 | Multi-CK network protocol, handshake, friends, messaging |
| `ck_gpu.py` | ~580 | GPU doing engine, CUDA kernels, CuPy, pynvml sensing |
| `ck_sensorium.py` | ~1610 | 15-layer fractal sensorium, hardware-as-body |
| `ck_truth.py` | ~920 | Truth lattice with save/load persistence |
| `ck_power_sense.py` | ~200 | Power state sensing, AC/battery/thermal |
| `ck_claude_library.py` | ~300 | Claude Sonnet study library |
| `ck_sim_engine.py` | ~2260 | 50Hz main loop, all subsystems wired |

### Updated Test Count

| Test Suite | Count |
|------------|-------|
| `ck_sim_tests.py` | 94 |
| `ck_btq_tests.py` | 94 |
| `discover (*_tests.py)` | 1,345 |
| **TOTAL** | **1,533** |

129 new tests including 26 red-team adversarial attack tests covering core extraction attempts, network attacks (MITM, replay, impersonation, tamper), and edge cases (malformed data, boundary conditions, overflow).

---

## Dependencies (R16)

| Package | Version | Purpose |
|---------|---------|---------|
| cupy-cuda12x | latest | GPU CL composition, CUDA kernels |
| pynvml (nvidia-ml-py) | 13.590+ | GPU state sensing (utilization, temp, power) |
| anthropic | 0.84+ | Claude Sonnet API for study library |
| pynput | latest | Input proprioception (keyboard + mouse) |
| psutil | latest | CPU, memory, disk, process sensing |
| sounddevice | latest | Audio input/output |
| kivy | latest | Display (chat + dashboard) |
| numpy | latest | Numerical operations |

---

*Last updated: 2026-02-26 — Gen9.17g (GPU Doing Engine + Truth Persistence + Sensorium + Claude Sonnet)*
*(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory*
