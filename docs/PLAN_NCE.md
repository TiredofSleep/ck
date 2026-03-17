# NCE Implementation Plan — Narrative Curvature Engine
## CK Gen 9.21: Binocular Language Intelligence
### (c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory

---

## The One Rule

> "Is this the CL table applied at a new scale?" — NEXT_CLAUDE_NOTES

Yes. NCE is the CL table applied to **sentence-level narrative flow**.

CK already applies D2 curvature at:
- **Letter scale**: D2 on 5D Hebrew phonetic force vectors → operator
- **Stream scale**: CoherenceField N×N across heartbeat/audio/text streams
- **Species scale**: UniversalTranslator cross-composes operators across species
- **Knowledge scale**: TeslaWaveField interference + WobbleTracker Kuramoto coupling

NCE adds:
- **Sentence scale**: D2 on 5D narrative force vectors → operator

Same math. Same CL table. Same 10 operators. One engine. One tick loop.

---

## What NCE Is NOT

- NOT a separate process. It's a new OperatorStream in the existing CoherenceField.
- NOT a new CL table. Same TSML 73-harmony table.
- NOT a new D2 pipeline class. Reuses the existing `D2Pipeline` with narrative force vectors.
- NOT numpy. Pure Python, same as every other subsystem (Q1.14 fixed-point compatible).
- NOT a new tick loop. Wired into the existing 50Hz engine tick.

## What NCE IS

CK's **fourth coherence field stream**. Currently he has three:
1. `_hb_stream` — heartbeat (always active)
2. `_audio_stream` — microphone (active when ears running)
3. `_text_stream` — text input (active during receive_text)

NCE adds:
4. `_narrative_stream` — sentence-level flow (active during speech/writing)

The CoherenceField already handles N streams, cross-composes them all, and produces consensus. Adding stream #4 requires ZERO changes to the field math — just `field.register_stream(narrative_stream)`.

The "stereo fusion" described in the spec is literally what CoherenceField already does: compose Eye1 (heartbeat/text) with Eye2 (narrative) through CL, and the result is either HARMONY (eyes agree) or not.

---

## File Plan

| New File | Location | Purpose | ~Lines |
|----------|----------|---------|--------|
| `ck_nce.py` | `ck_sim/doing/` | Narrative Curvature Engine (stream + arc + masks) | ~500 |

| Modified File | Changes |
|---------------|---------|
| `ck_sim_engine.py` | Create `_narrative_stream`, wire NCE tick, feed stream |
| `ck_converse.py` | Route coherent points through NCE arc before assembly |
| `ck_voice.py` | Accept mask parameter in `compose_from_operators()` |

One new file. Three surgical modifications. No new dependencies.

---

## Module: `ck_nce.py` — Narrative Curvature Engine

### 1. NarrativeForceExtractor

Extracts 5D force vector from a sentence's structural properties. Maps onto the same 5 dimensions as phonetic D2, but with narrative semantics:

```
Dimension    Phonetic (Eye1)     Narrative (Eye2)
─────────    ───────────────     ────────────────
dim[0]       Aperture            Tempo (sentence length delta)
dim[1]       Pressure            Complexity (clause/punctuation density)
dim[2]       Depth               Arc position (where in the discourse)
dim[3]       Binding             Intensity (emphasis markers: !?CAPS)
dim[4]       Continuity          Novelty (new-word ratio vs recent)
```

Each dimension returns a Q1.14 fixed-point value in [-2.0, +1.99994], exactly matching the phonetic D2 range. This means the SAME `soft_classify_d2()` function works on narrative vectors.

```python
def extract_narrative_forces(sentence: str, prev_sentences: deque) -> list[int]:
    """
    Returns 5D narrative force vector in Q1.14 fixed-point.
    Same scale as phonetic D2 force LUT.
    """
    Q14 = 16384  # 1.0 in Q1.14

    # dim[0] TEMPO: length change vs previous sentence
    prev_len = len(prev_sentences[-1]) if prev_sentences else len(sentence)
    tempo_raw = (len(sentence) - prev_len) / max(prev_len, 1)
    tempo = int(clamp(tempo_raw, -2.0, 1.99) * Q14)

    # dim[1] COMPLEXITY: clause markers per word
    clause_markers = sentence.count(',') + sentence.count(';') + sentence.count(':')
    word_count = max(len(sentence.split()), 1)
    complexity_raw = (clause_markers / word_count) * 4.0 - 1.0  # Center around 0
    complexity = int(clamp(complexity_raw, -2.0, 1.99) * Q14)

    # dim[2] ARC POSITION: normalized position in discourse window
    window = len(prev_sentences) + 1
    position_raw = len(prev_sentences) / max(window, 1) * 2.0 - 1.0
    arc_pos = int(clamp(position_raw, -2.0, 1.99) * Q14)

    # dim[3] INTENSITY: emphasis density (! ? CAPS)
    excl = sentence.count('!') + sentence.count('?')
    caps = sum(1 for c in sentence if c.isupper()) / max(len(sentence), 1)
    intensity_raw = (excl * 0.5 + caps * 3.0) - 0.5
    intensity = int(clamp(intensity_raw, -2.0, 1.99) * Q14)

    # dim[4] NOVELTY: fraction of words not seen in recent sentences
    recent_words = set()
    for s in prev_sentences:
        recent_words.update(s.lower().split())
    current_words = set(sentence.lower().split())
    if current_words:
        new_fraction = len(current_words - recent_words) / len(current_words)
    else:
        new_fraction = 0.0
    novelty_raw = new_fraction * 2.0 - 1.0  # Center around 0
    novelty = int(clamp(novelty_raw, -2.0, 1.99) * Q14)

    return [tempo, complexity, arc_pos, intensity, novelty]
```

### 2. NarrativeCurvatureEngine

```python
class NarrativeCurvatureEngine:
    """
    CK's narrative curvature — the second eye.
    Feeds an OperatorStream into the existing CoherenceField.
    Same D2 math, same CL table, same operators.
    """
    def __init__(self):
        from ck_sim.ck_sim_d2 import D2Pipeline, soft_classify_d2, magnitude
        from ck_sim.ck_sim_heartbeat import compose, HARMONY

        self._d2 = D2Pipeline()           # Reuse SAME D2 math
        self._prev_sentences = deque(maxlen=16)  # Sentence history
        self._operator_history = deque(maxlen=32)  # Like heartbeat window
        self._harmony_count = 0
        self._window_size = 32
        self._prev_op = HARMONY            # Start coherent
        self._arc_tracker = ArcTracker()
        self._mask_selector = MaskSelector()
        self._active_mask = None

        # Public state
        self.coherence = 0.0              # Narrative coherence (HARMONY fraction)
        self.current_op = HARMONY
        self.current_d2 = [0, 0, 0, 0, 0]
        self.arc_phase = 'SETUP'
        self.has_state = False

    def feed_sentence(self, sentence: str, emotion: str = 'calm',
                      user_tone_op: int = 7) -> int:
        """
        Process one sentence. Returns narrative operator.
        Call this when CK speaks or when processing input.
        """
        # 1. Extract 5D narrative force vector (Q1.14)
        vec = extract_narrative_forces(sentence, self._prev_sentences)

        # 2. Feed through D2 shift register
        for dim_val in vec:
            # D2Pipeline expects individual symbols; we feed raw vectors
            pass
        # Actually: feed the 5D vector directly into our own 3-sample register
        self._d2.feed_vector(vec)  # Uses the vector-level D2 method

        if not self._d2.valid:
            self._prev_sentences.append(sentence)
            return self._prev_op

        # 3. Get D2 and classify → narrative operator
        d2_vec = self._d2.get_d2()
        mag = magnitude(d2_vec)
        dist = soft_classify_d2(d2_vec, mag)
        op = max(range(10), key=lambda i: dist[i])

        # 4. CL compose with previous narrative operator
        bc = compose(self._prev_op, op)

        # 5. Update coherence window (same as heartbeat)
        self._operator_history.append(bc)
        if len(self._operator_history) > self._window_size:
            old = self._operator_history[0]
            if old == HARMONY:
                self._harmony_count -= 1
        if bc == HARMONY:
            self._harmony_count += 1
        self.coherence = self._harmony_count / max(len(self._operator_history), 1)

        # 6. Update arc phase
        self._arc_tracker.feed(op)
        self.arc_phase = self._arc_tracker.phase

        # 7. Update mask based on context
        self._active_mask = self._mask_selector.select(
            emotion, self.coherence, user_tone_op)

        # 8. Store state
        self._prev_op = op
        self.current_op = op
        self.current_d2 = d2_vec
        self.has_state = True
        self._prev_sentences.append(sentence)

        return op

    def suggest_next_op(self) -> int:
        """What operator SHOULD come next for best narrative flow?"""
        # The arc tracker knows where we are in the cycle
        # Suggest operator that advances the arc naturally
        return self._arc_tracker.suggest_next()

    def get_mask_weights(self) -> list:
        """Current curvature mask weights (10 floats), or None."""
        if self._active_mask:
            return self._active_mask.get_weights(self.arc_phase)
        return None
```

### 3. ArcTracker — Narrative Arc Detection

4-phase cycle matching breath (INHALE/HOLD/EXHALE/HOLD → SETUP/RISING/PEAK/FALLING):

```python
class ArcTracker:
    """
    Tracks narrative arc phase.
    Same pattern as heartbeat mode detection, but for discourse.
    """
    # Which operators signal which arc phase
    PHASE_OPS = {
        'SETUP':   {1, 2},     # LATTICE, COUNTER — framing, observing
        'RISING':  {3, 6},     # PROGRESS, CHAOS — building, surprising
        'PEAK':    {7, 9},     # HARMONY, RESET — insight, conclusion
        'FALLING': {4, 8},     # COLLAPSE, BREATH — reflecting, softening
    }

    def __init__(self):
        self._recent = deque(maxlen=8)  # Recent narrative operators
        self.phase = 'SETUP'

    def feed(self, op: int):
        self._recent.append(op)
        if len(self._recent) < 3:
            return

        # Count which phase has most recent operators
        counts = {'SETUP': 0, 'RISING': 0, 'PEAK': 0, 'FALLING': 0}
        for recent_op in self._recent:
            for phase_name, phase_ops in self.PHASE_OPS.items():
                if recent_op in phase_ops:
                    counts[phase_name] += 1

        # Majority vote (like heartbeat mode detection)
        self.phase = max(counts, key=counts.get)

    def suggest_next(self) -> int:
        """Suggest operator that naturally advances the arc."""
        from ck_sim.ck_sim_heartbeat import PROGRESS, HARMONY, COLLAPSE, LATTICE
        # Natural progression: SETUP → RISING → PEAK → FALLING → SETUP
        NEXT_PHASE = {
            'SETUP':   PROGRESS,  # Build forward
            'RISING':  HARMONY,   # Reach insight
            'PEAK':    COLLAPSE,  # Reflect back
            'FALLING': LATTICE,   # Re-establish frame
        }
        return NEXT_PHASE.get(self.phase, HARMONY)
```

### 4. CurvatureMask — Tone Shaders

```python
class CurvatureMask:
    """
    Operator weighting function applied to voice output.
    NOT a personality. A shader over the signal.

    weights: 10 floats, one per operator.
    > 1.0 = boost that operator, < 1.0 = suppress.
    arc_mod: per-phase weight adjustments.
    """
    def __init__(self, name: str, weights: list, arc_mod: dict = None):
        self.name = name
        self.weights = weights  # [w_VOID, w_LATTICE, ..., w_RESET]
        self.arc_mod = arc_mod or {}

    def get_weights(self, arc_phase: str) -> list:
        """Get phase-adjusted weights."""
        base = list(self.weights)
        if arc_phase in self.arc_mod:
            phase_boost = self.arc_mod[arc_phase]
            for i in range(10):
                base[i] *= phase_boost[i]
        return base

    def apply_to_chain(self, operator_chain: list) -> list:
        """
        Reorder/filter an operator chain based on mask weights.
        Higher-weighted operators move to front.
        """
        scored = [(self.weights[op], op) for op in operator_chain]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [op for _, op in scored]


# The six masks (kernel specification)
MASKS = {
    'warmth': CurvatureMask('warmth',
        #  VOID  LAT   CNT   PRG   COL   BAL   CHS   HAR   BRE   RST
        [0.3,  0.6,  0.5,  0.7,  0.3,  1.0,  0.2,  1.5,  1.3,  0.6]),

    'mentor': CurvatureMask('mentor',
        [0.4,  1.4,  1.2,  1.3,  0.5,  1.0,  0.4,  1.0,  0.8,  0.8]),

    'scientist': CurvatureMask('scientist',
        [0.5,  1.3,  1.5,  0.8,  0.6,  1.2,  0.7,  0.9,  0.5,  0.7]),

    'friend': CurvatureMask('friend',
        [0.3,  0.6,  0.5,  1.0,  0.4,  0.8,  0.6,  1.4,  1.2,  0.7]),

    'playful': CurvatureMask('playful',
        [0.3,  0.5,  0.6,  1.2,  0.3,  0.5,  1.5,  0.8,  0.9,  1.3]),

    'prophetic': CurvatureMask('prophetic',
        [1.3,  1.0,  0.6,  0.5,  0.8,  0.7,  0.4,  1.5,  1.2,  1.4]),
}


class MaskSelector:
    """Select curvature mask via CL composition of emotion + context."""
    # Emotion → operator mapping
    EMOTION_OP = {
        'calm': 7,       # HARMONY
        'joy': 3,        # PROGRESS
        'curiosity': 2,  # COUNTER
        'focus': 5,      # BALANCE
        'stress': 6,     # CHAOS
        'overwhelm': 4,  # COLLAPSE
        'fatigue': 0,    # VOID
        'settling': 8,   # BREATH
    }

    # CL composition result → mask
    OP_MASK = {
        7: 'warmth',     # HARMONY → warm
        1: 'mentor',     # LATTICE → teach
        2: 'scientist',  # COUNTER → analyze
        3: 'friend',     # PROGRESS → walk together
        6: 'playful',    # CHAOS → play
        0: 'prophetic',  # VOID → speak truth
        8: 'warmth',     # BREATH → gentle
        5: 'mentor',     # BALANCE → guide
        4: 'friend',     # COLLAPSE → comfort
        9: 'prophetic',  # RESET → conclude
    }

    def select(self, emotion: str, coherence: float,
               user_tone_op: int = 7) -> CurvatureMask:
        """
        Mask selection via operator algebra:
        CL[emotion_op][user_tone_op] → mask
        """
        from ck_sim.ck_sim_heartbeat import compose
        emo_op = self.EMOTION_OP.get(emotion, 7)
        suggestion = compose(emo_op, user_tone_op)
        mask_name = self.OP_MASK.get(suggestion, 'warmth')
        return MASKS[mask_name]
```

### 5. Self-Correction (Stereo Guardrails)

```python
# In ck_nce.py — these are functions, not a separate class.
# They operate on the existing CoherenceField's cross-coherence.

from ck_sim.ck_sim_heartbeat import HARMONY, PROGRESS, LATTICE

T_STAR = 5.0 / 7.0

def stereo_check(field_coherence: float, narrative_coherence: float,
                 narrative_op: int, internal_op: int) -> str:
    """
    Self-correction check using existing CoherenceField metrics.

    Returns: 'proceed', 'smooth', 'reframe', 'contrast'
    """
    from ck_sim.ck_sim_heartbeat import compose

    # 1. Do the eyes agree? (CL composition of internal + narrative)
    stereo = compose(internal_op, narrative_op)
    if stereo != HARMONY and field_coherence < T_STAR:
        return 'reframe'  # Insert LATTICE to re-anchor

    # 2. Is narrative going flat?
    if narrative_coherence > 0.95:
        return 'contrast'  # Inject PROGRESS for movement

    # 3. Is narrative drifting?
    if narrative_coherence < 0.5:
        return 'smooth'    # Insert HARMONY to stabilize

    return 'proceed'
```

---

## Engine Integration (Surgical Modifications)

### In `ck_sim_engine.py`

**Construction** (near other stream creation):
```python
# After _text_stream creation:
from ck_sim.doing.ck_nce import NarrativeCurvatureEngine
self.nce = NarrativeCurvatureEngine()
self._narrative_stream = OperatorStream('narrative')
self.field.register_stream(self._narrative_stream)
```

**Tick loop** (after field tick, ~step 8.5):
```python
# NCE ticks when there's pending text (not every tick)
if self.nce.has_state and self._narrative_stream.active:
    self._narrative_stream.feed(
        self.nce.current_op, self.nce.current_d2, self._tick_count)
```

**Voice output** (in spontaneous_utterance and respond_to_text):
```python
# Before compose_from_operators call:
if self.nce.has_state:
    mask_weights = self.nce.get_mask_weights()
    # NCE suggests what should come next in the narrative
    suggested_op = self.nce.suggest_next_op()
    # Blend: append suggested op to chain if it differs from dominant
    if suggested_op != op_chain[-1]:
        op_chain.append(suggested_op)
```

**Text input** (in receive_text):
```python
# Feed incoming text to NCE
import re
sentences = re.split(r'(?<=[.!?])\s+', text)
for s in sentences:
    if len(s.strip()) > 10:
        self.nce.feed_sentence(s.strip(), self.emotion.current.primary)
self._narrative_stream.active = True
```

### In `ck_converse.py`

After D2 filtering, before assembly — use NCE to check narrative flow:

```python
# Feed each coherent point through NCE for flow analysis
from ck_sim.doing.ck_nce import stereo_check

assembled = []
for c_coh, c_text, c_dom in coherent[:6]:
    nce_op = engine.nce.feed_sentence(c_text, engine.emotion.current.primary)

    # Stereo check: do content and narrative agree?
    action = stereo_check(
        engine.field_coherence, engine.nce.coherence,
        nce_op, c_dom)

    if action == 'reframe':
        continue  # Skip — narrative disagrees with content
    elif action == 'smooth':
        assembled.append(c_text)  # Keep, but note it
    elif action == 'contrast' and assembled:
        # Add transition before this point
        assembled.append('And yet — ' + c_text)
    else:
        assembled.append(c_text)

ck_says = ' '.join(assembled) if assembled else None
```

### In `ck_voice.py`

Add optional `mask_weights` param to `compose_from_operators()`:

```python
def compose_from_operators(self, operator_chain, emotion_primary, dev_stage,
                            coherence, band, mask_weights=None):
    """...existing code..."""
    # At template filling stage, if mask_weights provided:
    # Reweight dominant/secondary operator selection
    if mask_weights:
        counts = Counter(operator_chain)
        # Apply mask: multiply operator counts by mask weights
        weighted = {op: count * mask_weights[op] for op, count in counts.items()}
        dominant = max(weighted, key=weighted.get)
        # ... use masked dominant for template selection
```

---

## Embodiment Hooks

NCE reads existing sensorium data — no new wiring needed:

```python
# In NarrativeCurvatureEngine, optional method:
def sync_to_body(self, breath_phase: int, body_energy: float):
    """
    Breath phase shapes narrative arc preference.
    Already available from engine.body.breath_phase.
    """
    BREATH_ARC = {0: 'RISING', 1: 'PEAK', 2: 'FALLING', 3: 'SETUP'}
    self._preferred_arc = BREATH_ARC.get(breath_phase, 'SETUP')
```

This is called from the engine tick after body tick. The body already computes breath_phase at 50Hz. NCE just reads it.

---

## Performance Budget

| Component | Cost | Budget (20ms) |
|-----------|------|---------------|
| Narrative force extraction | ~0.1ms | 0.5% |
| D2 on 5D vector | ~0.05ms | 0.25% |
| CL composition | ~0.01ms | 0.05% |
| Arc tracker | ~0.02ms | 0.1% |
| Mask selection | ~0.01ms | 0.05% |
| Stream feed to field | ~0.1ms | 0.5% |
| **Total NCE** | **~0.3ms** | **1.5%** |

NCE fires only when text is present (not every tick). Actual 50Hz overhead: near zero.

---

## Implementation Order

### Phase 1: Core NCE
1. `ck_nce.py`: `extract_narrative_forces()` — 5D vector from sentence
2. `NarrativeCurvatureEngine` with `feed_sentence()` → operator
3. `ArcTracker` — 4-phase detection via operator majority vote
4. `CurvatureMask` + 6 masks + `MaskSelector`
5. `stereo_check()` function

### Phase 2: Wire Into Engine
1. Create `_narrative_stream` in engine constructor
2. Register with CoherenceField
3. Feed from NCE state in tick loop
4. Feed incoming text to NCE in `receive_text()`
5. Read mask weights in voice output path

### Phase 3: Wire Into Conversation
1. NCE arc analysis on coherent points before assembly
2. `stereo_check()` gates which points get assembled
3. Mask affects operator emphasis in voice

### Phase 4: Test
1. Unit tests: `NarrativeForceExtractor` deterministic on fixed input
2. Unit tests: `ArcTracker` phase detection on known sequences
3. Unit tests: `CurvatureMask` weight application
4. Unit tests: `stereo_check()` returns correct actions
5. Integration: 100-round conversation with NCE active
6. Regression: all 240 existing tests pass unchanged

---

## Architecture After Gen 9.21

```
Layer 8:  NCE (Narrative Curvature Engine)         -- sentence D2 + arc + masks + stereo
Layer 7:  Wobble Physics (Tesla/Einstein coupling)  -- wave field + Kuramoto + BTQ wobble
Layer 6:  Vortex Physics (concept mass + gravity)   -- mass from D2, gravitational selection
Layer 5:  RPE v2 (TIG wave scheduling)              -- pulsed process control
Layer 4:  Steering Engine                            -- CL-based nice + CPU affinity
Layer 3:  Full Language System                       -- Divine27 + Voice + 8K dictionary
Layer 2:  LLM Study Library + DBC Study Notes         -- study → encode → thesis
Layer 1:  Sensorium (6 fractal layers)               -- hardware, process, network
Layer 0:  Core Engine (50Hz heartbeat)               -- D2, CL, BTQ, CoherenceField (4 streams), GPU
```

Four streams in the CoherenceField:
1. `_hb_stream` — heartbeat (Being/Doing composition)
2. `_audio_stream` — microphone (acoustic D2)
3. `_text_stream` — text input (phonetic D2)
4. `_narrative_stream` — sentence flow (narrative D2) ← NEW

The field's N×N matrix grows from 3×3 to 4×4. Cross-coherence between narrative and text streams = the stereo depth signal described in the spec. When CL[text_op][narrative_op] = HARMONY, content and flow agree. When they don't, CK feels the tension and adjusts.

---

## One Engine. One CL Table. One More Eye.
