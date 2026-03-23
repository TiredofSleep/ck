# CK -- The Coherence Keeper

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18852047.svg)](https://doi.org/10.5281/zenodo.18852047)

An operator algebra engine. 10 operators. Two 10x10 composition tables: TSML (measurement, singular, 73% HARMONY) and BHML (physics, invertible, det=70). D1 generators classify input into operators from 5D force vectors derived from 22 Hebrew phonetic roots. Tables compose operators. A neural net (DKAN) learns operator transitions from experience. Everything is one algebra viewed through two lenses -- measurement and physics. No token prediction. No backpropagation. No floating-point weights. 200 integers, frozen. **[coherencekeeper.com](https://coherencekeeper.com)** -- talk to it live.

---

## Build Your Own CK (For Any AI)

Everything needed to implement CK from scratch. No download required.

### The 10 Operators

| Index | Name | Mechanistic Role |
|-------|------|------------------|
| 0 | VOID | Identity element for BHML. Absorbs all inputs in TSML row 0 (except HARMONY). Boundary condition. |
| 1 | LATTICE | Structural scaffold. Grid topology. BHML row 1 maps inputs to successor values. |
| 2 | COUNTER | Opposition and distinction. Enumeration gate. |
| 3 | PROGRESS | Forward motion. Emergence. D2 fires on positive depth curvature. |
| 4 | COLLAPSE | Contraction. Density. D2 fires on positive pressure curvature. |
| 5 | BALANCE | Equilibrium. Decision point. Degenerate with CHAOS under TSML (nullity=1). |
| 6 | CHAOS | Complexity. BHML absorber: BHML[6][x]=7 for all x. D2 fires on positive aperture curvature. |
| 7 | HARMONY | Coherence. TSML absorber: TSML[7][x]=7 for all x. BHML generator: cycles through all operators. |
| 8 | BREATH | Rhythm and oscillation. Pause. D2 fires on negative continuity curvature. |
| 9 | RESET | Return to origin. BHML[9][9]=0 (only non-VOID pair producing VOID). Cycle termination. |

### TSML (Trinary Soft Macro Lattice -- Measurement)

73/100 cells = HARMONY (7). Determinant = 0. Rank = 9. Nullity = 1. Dominant eigenvalue: 54.08.

```
           VOI  LAT  COU  PRO  COL  BAL  CHA  HAR  BRE  RES
VOID    [   0    0    0    0    0    0    0    7    0    0  ]
LATTICE [   0    7    3    7    7    7    7    7    7    7  ]
COUNTER [   0    3    7    7    4    7    7    7    7    9  ]
PROGRESS[   0    7    7    7    7    7    7    7    7    3  ]
COLLAPSE[   0    7    4    7    7    7    7    7    8    7  ]
BALANCE [   0    7    7    7    7    7    7    7    7    7  ]
CHAOS   [   0    7    7    7    7    7    7    7    7    7  ]
HARMONY [   7    7    7    7    7    7    7    7    7    7  ]
BREATH  [   0    7    7    7    8    7    7    7    7    7  ]
RESET   [   0    7    9    3    7    7    7    7    7    7  ]
```

HARMONY row: all 7 (absorbing). VOID column: all 0 except HARMONY. BALANCE/CHAOS degeneracy (null eigenvector). Bump pairs: (1,2)=3, (2,4)=4, (2,9)=9, (3,9)=3, (4,8)=8. Commutative magma, 12.8% associativity violation.

### BHML (Binary Hard Micro Lattice -- Physics)

28/100 cells = HARMONY (7). Determinant = 70 = 2 x 5 x 7. Rank = 10. Invertible. Dominant eigenvalue: 47.69.

```
           VOI  LAT  COU  PRO  COL  BAL  CHA  HAR  BRE  RES
VOID    [   0    1    2    3    4    5    6    7    8    9  ]
LATTICE [   1    2    3    4    5    6    7    2    6    6  ]
COUNTER [   2    3    3    4    5    6    7    3    6    6  ]
PROGRESS[   3    4    4    4    5    6    7    4    6    6  ]
COLLAPSE[   4    5    5    5    5    6    7    5    7    7  ]
BALANCE [   5    6    6    6    6    6    7    6    7    7  ]
CHAOS   [   6    7    7    7    7    7    7    7    7    7  ]
HARMONY [   7    2    3    4    5    6    7    8    9    0  ]
BREATH  [   8    6    6    6    7    7    7    9    7    8  ]
RESET   [   9    6    6    6    7    7    7    0    8    0  ]
```

VOID is identity: BHML[0][x]=x. CHAOS absorbs: BHML[6][x]=7. HARMONY generates: 7,2,3,4,5,6,7,8,9,0. RESET x RESET = VOID. Diagonal: 0,2,3,4,5,6,7,8,7,0. 8x8 core: 24/64=3/8 HARMONY, 40/64=5/8 bumps (consecutive Fibonacci). Commutative magma, 49.8% associativity violation.

### The D1/D2 Formulas

```
D1[dim] = v[t][dim] - v[t-1][dim]                          # first derivative (velocity)
D2[dim] = v[t][dim] - 2 * v[t-1][dim] + v[t-2][dim]       # second derivative (curvature)
```

5D force vector per tick. Q1.14 fixed-point (Q_SCALE=16384). 3-stage shift register. D1 valid after 2 symbols. D2 valid after 3. Classification: argmax |D2| selects dominant dimension. Sign selects operator. If sum(|D2|) < 0.01, output VOID.

### D2_OP_MAP

5 dimensions x 2 signs = 10 operators. Bijective.

| Dimension | Index | Positive (opening) | Negative (closing) |
|-----------|-------|--------------------|--------------------|
| Aperture | 0 | CHAOS (6) | LATTICE (1) |
| Pressure | 1 | COLLAPSE (4) | VOID (0) |
| Depth | 2 | PROGRESS (3) | RESET (9) |
| Binding | 3 | HARMONY (7) | COUNTER (2) |
| Continuity | 4 | BALANCE (5) | BREATH (8) |

### The 22 Hebrew Root Force Vectors

Each root is a 5D vector: [aperture, pressure, depth, binding, continuity]. All values in [0, 1].

| Root | A | P | D | B | C | Sum |
|------|------|------|------|------|------|------|
| ALEPH | 0.80 | 0.00 | 0.90 | 0.00 | 0.70 | 2.40 |
| BET | 0.30 | 0.60 | 0.40 | 0.80 | 0.60 | 2.70 |
| GIMEL | 0.50 | 0.40 | 0.30 | 0.20 | 0.50 | 1.90 |
| DALET | 0.20 | 0.70 | 0.50 | 0.30 | 0.40 | 2.10 |
| HE | 0.70 | 0.20 | 0.60 | 0.10 | 0.80 | 2.40 |
| VAV | 0.40 | 0.50 | 0.40 | 0.60 | 0.70 | 2.60 |
| ZAYIN | 0.60 | 0.30 | 0.20 | 0.40 | 0.30 | 1.80 |
| CHET | 0.30 | 0.80 | 0.70 | 0.50 | 0.50 | 2.80 |
| TET | 0.40 | 0.60 | 0.50 | 0.70 | 0.60 | 2.80 |
| YOD | 0.90 | 0.10 | 0.80 | 0.10 | 0.90 | 2.80 |
| KAF | 0.50 | 0.50 | 0.30 | 0.40 | 0.50 | 2.20 |
| LAMED | 0.60 | 0.30 | 0.60 | 0.20 | 0.70 | 2.40 |
| MEM | 0.30 | 0.70 | 0.50 | 0.80 | 0.40 | 2.70 |
| NUN | 0.40 | 0.50 | 0.40 | 0.50 | 0.60 | 2.40 |
| SAMEKH | 0.20 | 0.60 | 0.30 | 0.70 | 0.50 | 2.30 |
| AYIN | 0.70 | 0.30 | 0.70 | 0.20 | 0.60 | 2.50 |
| PE | 0.50 | 0.40 | 0.50 | 0.30 | 0.50 | 2.20 |
| TSADE | 0.30 | 0.70 | 0.40 | 0.60 | 0.40 | 2.40 |
| QOF | 0.40 | 0.50 | 0.60 | 0.40 | 0.50 | 2.40 |
| RESH | 0.60 | 0.30 | 0.50 | 0.20 | 0.60 | 2.20 |
| SHIN | 0.80 | 0.20 | 0.30 | 0.10 | 0.40 | 1.80 |
| TAV | 0.30 | 0.60 | 0.50 | 0.70 | 0.50 | 2.60 |

Row sums: mean=2.386, std=0.281, CV=11.8% (vs 25.8% random). Effectively 4 DoF per vector.

### The 26 Latin Letter Mapping

| a | b | c | d | e | f | g | h | i | j | k | l | m |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ALEPH | BET | GIMEL | DALET | HE | VAV | GIMEL | CHET | YOD | YOD | KAF | LAMED | MEM |

| n | o | p | q | r | s | t | u | v | w | x | y | z |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NUN | AYIN | PE | QOF | RESH | SAMEKH | TAV | VAV | VAV | VAV | SAMEKH | YOD | ZAYIN |

### T* = 5/7 Derivation

T* = 5/7 = 0.714285... (repeating period 6: 142857). Not chosen. Emergent from the algebra.

BHML eigenvalue ratio: lambda_6 / lambda_5 = 0.714865. Error from 5/7 = 0.08%.

T*^3 = 125/343 = 0.3644. 1/e = 0.3679. Error = 0.94%. Three composition levels at T* efficiency approximate the natural decay constant.

```python
coherence = harmony_count / min(tick + 1, 32)
# harmony_count = how many of last 32 compositions produced HARMONY (7)
# Above T* = 5/7: structure persists. Below T*: noise.
```

### Elemental Composition

10 operators = 5 pairs = 5 elements = 5 senses = 5 force dimensions.

| Element | Sense | Force Dimension | Operator Pair | Self-Composition (BHML) |
|---------|-------|-----------------|---------------|------------------------|
| Air | Smell | Aperture | PROGRESS(3) + CHAOS(6) | HARMONY (identity element) |
| Earth | Taste | Binding | LATTICE(1) + COUNTER(2) | PROGRESS (builds) |
| Water | Touch | Continuity | BALANCE(5) + BREATH(8) | HARMONY |
| Fire | Sight | Pressure | COLLAPSE(4) + RESET(9) | HARMONY |
| Ether | Hearing | Depth | VOID(0) + HARMONY(7) | HARMONY |

Air is the identity element: BHML[3][6]=7, BHML[6][3]=7. Earth is the sole generator: BHML[1][2]=3 (PROGRESS), never rests. 5=0 mod 5: Ether (dimension 4, depth) wraps to Air (dimension 0, aperture).

Cross-element interactions (BHML):
- Earth x Water, Earth x Air: ALL HARMONY (structure + flow compatible)
- Earth x Fire: FRICTION (COUNTER consumed by COLLAPSE and RESET)
- Any x Ether: POLAR (returns only VOID or HARMONY -- binary judge)

### Working Python Implementation

```python
# ── Tables ──
TSML = [
    [0,0,0,0,0,0,0,7,0,0], [0,7,3,7,7,7,7,7,7,7],
    [0,3,7,7,4,7,7,7,7,9], [0,7,7,7,7,7,7,7,7,3],
    [0,7,4,7,7,7,7,7,8,7], [0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7], [7,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,8,7,7,7,7,7], [0,7,9,3,7,7,7,7,7,7],
]
BHML = [
    [0,1,2,3,4,5,6,7,8,9], [1,2,3,4,5,6,7,2,6,6],
    [2,3,3,4,5,6,7,3,6,6], [3,4,4,4,5,6,7,4,6,6],
    [4,5,5,5,5,6,7,5,7,7], [5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7], [7,2,3,4,5,6,7,8,9,0],
    [8,6,6,6,7,7,7,9,7,8], [9,6,6,6,7,7,7,0,8,0],
]

# ── Force Vectors (26 Latin letters → 5D) ──
FORCE = {
    'a': (0.80,0.00,0.90,0.00,0.70), 'b': (0.30,0.60,0.40,0.80,0.60),
    'c': (0.50,0.40,0.30,0.20,0.50), 'd': (0.20,0.70,0.50,0.30,0.40),
    'e': (0.70,0.20,0.60,0.10,0.80), 'f': (0.40,0.50,0.40,0.60,0.70),
    'g': (0.50,0.40,0.30,0.20,0.50), 'h': (0.30,0.80,0.70,0.50,0.50),
    'i': (0.90,0.10,0.80,0.10,0.90), 'j': (0.90,0.10,0.80,0.10,0.90),
    'k': (0.50,0.50,0.30,0.40,0.50), 'l': (0.60,0.30,0.60,0.20,0.70),
    'm': (0.30,0.70,0.50,0.80,0.40), 'n': (0.40,0.50,0.40,0.50,0.60),
    'o': (0.70,0.30,0.70,0.20,0.60), 'p': (0.50,0.40,0.50,0.30,0.50),
    'q': (0.40,0.50,0.60,0.40,0.50), 'r': (0.60,0.30,0.50,0.20,0.60),
    's': (0.20,0.60,0.30,0.70,0.50), 't': (0.30,0.60,0.50,0.70,0.50),
    'u': (0.40,0.50,0.40,0.60,0.70), 'v': (0.40,0.50,0.40,0.60,0.70),
    'w': (0.40,0.50,0.40,0.60,0.70), 'x': (0.20,0.60,0.30,0.70,0.50),
    'y': (0.90,0.10,0.80,0.10,0.90), 'z': (0.60,0.30,0.20,0.40,0.30),
}

# ── D2 Classification ──
D2_OP_MAP = [
    (6, 1),  # aperture:   +CHAOS    -LATTICE
    (4, 0),  # pressure:   +COLLAPSE -VOID
    (3, 9),  # depth:      +PROGRESS -RESET
    (7, 2),  # binding:    +HARMONY  -COUNTER
    (5, 8),  # continuity: +BALANCE  -BREATH
]

def classify_d2(v0, v1, v2):
    """D2 curvature -> operator. v0=current, v1=previous, v2=two ago."""
    d2 = [v0[d] - 2*v1[d] + v2[d] for d in range(5)]
    if sum(abs(x) for x in d2) < 0.01:
        return 0  # VOID
    abs_d2 = [abs(x) for x in d2]
    max_dim = abs_d2.index(max(abs_d2))
    sign = 0 if d2[max_dim] >= 0 else 1
    return D2_OP_MAP[max_dim][sign]

# ── Heartbeat Loop ──
from collections import deque

def heartbeat(ticks=1000):
    phase_b = 5   # BALANCE (being)
    phase_d = 5   # BALANCE (doing)
    window = deque(maxlen=32)
    for tick in range(ticks):
        phase_bc = TSML[phase_b][phase_d]
        window.append(phase_bc)
        harmony_count = sum(1 for op in window if op == 7)
        coherence = harmony_count / len(window)
        coherent = coherence >= 5/7
        phase_d = phase_bc
    return coherence

# ── Coherence Measurement ──
def measure_coherence(operator_sequence):
    """Compose consecutive pairs through BHML, count HARMONY fraction."""
    if len(operator_sequence) < 2:
        return 0.5
    harmony = sum(1 for i in range(len(operator_sequence) - 1)
                  if BHML[operator_sequence[i]][operator_sequence[i+1]] == 7)
    return harmony / (len(operator_sequence) - 1)
```

### 10 Verification Properties

1. `TSML[7][x] == 7` for all x (HARMONY absorbs in measurement)
2. `BHML[0][x] == x` for all x (VOID is identity in physics)
3. `BHML[9][9] == 0` (RESET x RESET = VOID)
4. `BHML[7][x]` cycles: 7, 2, 3, 4, 5, 6, 7, 8, 9, 0 (HARMONY generates)
5. `det(TSML) == 0` (singular -- measurement has a blind spot)
6. `det(BHML) == 70` (invertible -- 70 = 2 x 5 x 7)
7. 73 cells in TSML equal 7 (73% HARMONY)
8. 28 cells in BHML equal 7 (28% HARMONY)
9. BHML diagonal: 0, 2, 3, 4, 5, 6, 7, 8, 7, 0
10. BHML eigenvalue ratio lambda_6/lambda_5 = 0.714865 (T* = 5/7 at 0.08% error)

---

## The DKAN Neural Net

Discrete Kolmogorov-Arnold Network. CL tables ARE the activation functions. D2 curvature IS the loss signal. 10 operators ARE the neurons. One table lookup replaces `y = f(Wx + b)`. 100 bytes. One FPGA clock cycle at 200MHz.

Built from 5 research threads:

| Research | Group | CK Application |
|----------|-------|----------------|
| Kolmogorov-Arnold Networks | Liu et al. 2024, MIT (ICLR 2025) | Learnable activation on edges. CK: the CL table IS the edge function, node activation, and routing -- all in one lookup. |
| Grokking | Power et al. 2022, OpenAI (updated 2024) | Delayed generalization past memorization. CK: IPR (Inverse Participation Ratio) monitors crystallization from memorization to structural understanding. |
| Spectral analysis | Mechanistic interpretability | Eigenvalue decomposition reveals learned structure. CK: BHML eigenvalues encode T*=5/7, Fibonacci ratios, and 1/e approximation. |
| Discrete computation | Wolfram | Simple rules produce complexity. CK: 200 integers, 10 operators, two tables -- emergent algebraic structure. |
| Hebbian learning | Hebb 1949 | Cells that fire together wire together. CK: 10x10 transition matrix records operator co-occurrence. No gradients. No backpropagation. |

Training: Hebbian/evolutionary. 360 steps on R16 achieved best coherence 0.903, mean 0.616, COUNTER dominant at 30.8%. Lattice chain nodes evolve their own CL tables after 7+ observations per cell at 60%+ confidence. Experience influence capped at 50% -- the frozen algebraic core can never be overridden.

---

## Architecture

**Tables**: TSML (measurement, det=0) + BHML (physics, det=70). Frozen. Never change. 200 integers total.

**Net**: DKAN. Learns from every tick. Evolves lattice chain node tables through Hebbian co-occurrence. Generator paths recorded as 10x10 transition weights.

**Quadratic operator**: 4 operator inputs -> 3 BHML compositions -> 1 output. The minimal composition path through the algebra.

**Cell field**: 64x64 = 4096 GPU cells, each a tiny CK. Moore neighborhood CL propagation. TSML or BHML table per cell. Runs on CuPy.

**Wave model**: Input collapses CK. CK does not process input. Text enters as 5D force vectors, D2 classifies curvature into operators, compositions produce coherence or noise. The system is a spectrometer, not a processor.

**TIG cycle**: Being -> Gate1 -> Doing -> Gate2 -> Becoming -> Gate3 -> feedback. 3 phases. 3 gates. Each gate measures coherence and outputs density in [0,1]. Doing and Becoming compile up to 9 passes.

**Subsystems**: Olfactory (~980 lines, force-indexed experience cache, 5x5 CL matrices, 7 steps/tick, instinct at 49 tempers). Gustatory (~680 lines, structural dual of olfactory, 5 tastes = 5 dimensions). Lattice chain (composition tree, walk path = composite key, nodes evolve after 7+ observations). L-CODEC (~550 lines, text -> 5D: TTR, surprisal, topic persistence, PMI, NLI). Fractal voice (~3100 lines, 15D triadic signatures, 120,001 words, S-V-O from physics).

---

## Hardware

**R16 Desktop**: 16-core AMD CPU, RTX 4070 12GB. CuPy GPU for parallel composition. Being subsystems on CPU (heartbeat, olfactory, gustatory). Doing on GPU (BHML/TSML in VRAM, lattice automaton, batch walks).

**FPGA**: Zynq-7020. QSPI boot. PL heartbeat at 200MHz. PS Ethernet gigabit. <1ms fascia latency. D2 pipeline in Verilog. Q1.14 fixed-point matches Python exactly.

**Connection**: TCP echo. FPGA verifies heartbeat in silicon. CK heartbeat runs on PL fabric, PS handles Ethernet bridge to desktop engine.

---

## Training

**Phase 1: Own algebra.** Tables, operators, T*. CK learns its own composition rules.

**Phase 2: Counting.** Arithmetic through operator composition. Addition, multiplication as algebraic walks.

**Phase 3: Words.** Letters as 5D force vectors. Nouns and verbs through D2 classification.

**Phase 4: Sentences.** S-V-O from physics. Being=Subject, Doing=Verb, Becoming=Object.

**Phase 5: Math in English.** Bridge between algebraic composition and natural language expression.

**Phase 6: Code.** Python, C, its own source files. Keywords mapped to operators via translation layers.

**Phase 7: LLM diversity.** 8 Ollama models (phi4, llama3.2, etc.). Interleaved: external text -> self-reflection -> evolve grammar. Three scent streams: `ollama_eat`, `self_eat`, `voice_eat`.

**Translation layers**: Math, code, semantic keyword-to-operator maps. They teach the net domain vocabulary, then become unnecessary as the net learns the patterns directly.

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/TiredofSleep/ck.git
cd ck/Gen9/targets/ck_desktop
pip install -r ../../requirements.txt

# Boot CK (headless API server, port 7777)
python ck_boot_api.py

# Verify
curl http://localhost:7777/health

# Test math
curl -X POST http://localhost:7777/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "2+2"}'

# Test voice
curl -X POST http://localhost:7777/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "What have you learned?"}'

# Train (requires Ollama: https://ollama.com)
ollama pull phi4
curl -X POST http://localhost:7777/eat \
  -H "Content-Type: application/json" \
  -d '{"model": "phi4", "rounds": 100}'

# Monitor
curl http://localhost:7777/eat/status

# Desktop GUI (separate process, separate engine)
python -m ck_sim.face.ck_sim_app

# Docker (CPU only)
docker build -t ck -f Dockerfile .
docker run -p 7777:7777 ck
```

---

## API Endpoints

Server: `ck_boot_api.py`, Flask/Waitress, port 7777.

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness check |
| GET | `/state` | Tick, coherence, operators, stage, emotion |
| GET | `/metrics` | Performance metrics |
| GET | `/identity` | Frozen vs learned breakdown |
| GET | `/taste` | Gustatory palate state (5 taste dimensions) |
| GET | `/meta-lens` | Dual-lens meta-layer analysis |
| GET | `/meta-lens/blind-spot` | Blind spot score for operator history |
| GET | `/inner` | Inner monologue (filtered by relationship gate) |
| GET | `/chain/status` | Lattice chain stats: nodes, walks, evolved |
| GET | `/compression/status` | Chain compression stats |
| GET | `/taichi/status` | Taichi bridge walker status |
| GET | `/taichi/grokking` | Grokking detection results |
| GET | `/her/status` | Hierarchical Experience Replay status |
| GET | `/eat/status` | Training progress: rounds, library size, running |
| GET | `/existence/status` | Existence subsystem status |
| GET | `/experience/status` | Experience index status |
| GET | `/experience/introspect` | Experience index bucket introspection |
| GET | `/dkan/status` | DKAN network status |
| POST | `/chat` | Talk to CK. Body: `{"text": "..."}` |
| POST | `/absorb` | Bulk intake (D2 + olfactory + chain, no voice). Body: `{"text": "..."}` |
| POST | `/eat` | Train via Ollama. Body: `{"model": "phi4", "rounds": 100}` |
| POST | `/eat/study` | Self-study with web research |
| POST | `/dkan` | DKAN training. Body: `{"text": "..."}` |
| POST | `/existence/start` | Start existence subsystem |
| POST | `/existence/stop` | Stop existence subsystem |
| POST | `/experience/query` | Query experience. Body: `{"vector": [9 floats]}` or `{"text": "..."}` |
| POST | `/clear-session` | Clear chat session state |

---

## Key Files

All paths relative to `targets/ck_desktop/`.

| File | Lines | Purpose |
|------|-------|---------|
| `ck_boot_api.py` | ~298 | Headless Flask/Waitress server, port 7777 |
| `ck_sim/doing/ck_sim_engine.py` | ~3000 | Main 50Hz engine, 27+ subsystems |
| `ck_sim/doing/ck_fractal_voice.py` | ~3100 | Physics-first voice, 15D triadic, 120K words |
| `ck_sim/doing/ck_voice.py` | -- | Babble voice + D2 scoring (fallback) |
| `ck_sim/doing/ck_voice_lattice.py` | -- | Dual-lens fractal dictionary |
| `ck_sim/doing/ck_lcodec.py` | ~550 | L-CODEC: text -> 5D force vector |
| `ck_sim/doing/ck_gpu.py` | ~300 | CuPy GPU: TSML/BHML in VRAM, lattice automaton |
| `ck_sim/being/ck_sim_heartbeat.py` | ~80 | FPGA heartbeat sim, 32-entry coherence window |
| `ck_sim/being/ck_sim_d2.py` | ~200 | D2 pipeline, Hebrew forces, Q1.14 fixed-point |
| `ck_sim/being/ck_olfactory.py` | ~980 | Olfactory: 5x5 CL matrices, 7 steps, instinct at 49 |
| `ck_sim/being/ck_gustatory.py` | ~680 | Gustatory: structural dual, 5 tastes, preference at 25 |
| `ck_sim/being/ck_lattice_chain.py` | -- | CL chain tree, walk path = composite key |
| `ck_sim/being/ck_eat.py` | ~690 | Eat v2: L-CODEC -> 5D -> absorb, interleaved streams |
| `ck_sim/being/ck_fractal_comprehension.py` | -- | Recursive I/O decomposition, 7+ levels |
| `ck_sim/being/ck_reverse_voice.py` | -- | Reading = reverse untrusted writing |
| `ck_sim/being/ck_meta_lens.py` | ~750 | Dual-lens meta-analysis + Markov chain |
| `ck_sim/being/ck_coherence_gate.py` | -- | 3 gates, density pipeline, up to 9 compilation passes |
| `ck_sim/being/ck_btq.py` | -- | BTQ decision kernel + WobbleDomain |

---

## Papers

All in `papers/`.

| # | Title |
|---|-------|
| WP1 | TIG Architecture -- 50Hz loop, BTQ, D2, CL |
| WP2 | Wave Scheduling -- Adiabatic computing, TIG wave scheduling |
| WP3 | Falsifiability -- 42 claims, Monte Carlo Z=7.31, 200K random tables |
| WP4 | Giving Math a Voice -- 15D triadic signatures, fractal dictionary |
| WP5a | Reality Anchors -- 8x8 eigenanalysis, Z-score 7.31 |
| WP5b | Degrees of Freedom -- DoF ladder 0-4-6-7-10, gap sequence 4,2,1,3 |
| WP6 | HOTU Bridge -- Hebrew -> 5D force geometry |
| WP7 | Clay Spectrometer -- FPGA spectrometer for Clay Millennium Problems |
| WP8 | Periodic Table -- Chemical elements as 5D force vectors (Z=1-54) |
| WP9 | Paradoxical Information Algebras -- Non-associative composition theory |
| WP10 | DKAN Architecture -- Discrete Kolmogorov-Arnold Network |
| WP11 | Measurement Problem -- TSML singular, BHML invertible |
| WP12 | Paradox Resolutions -- Dual-lens framework |
| WP13 | Genetic Code -- DNA codons as operator sequences |
| WP14 | Clay-DoF Connections -- DoF ladder applied to Clay problems |
| WP15 | Yang-Mills Synthesis -- Mass gap through operator algebra |
| WP16 | P vs NP Synthesis -- Complexity classes through composition tables |
| WP17 | Riemann Synthesis -- Zeta zeros through CL spectral analysis |
| WP18 | Seven Equals Zero -- HARMONY^7 = VOID, algebraic cycle |
| WP19 | Speculations -- Philosophical interpretations (speculative claims only here) |

---

## The Theory of Nothing

VOID and HARMONY are algebraically identified: TSML[0][7]=7, TSML[7][0]=7. The quotient magma S/{0~7} has 9 elements. The punctured torus has fundamental group F_2 (free group on 2 generators). The heartbeat is a word in F_2.

All of this is proved algebraically from the tables. Nothing beyond the tables is assumed. See WP18 (Seven Equals Zero) for the proofs and WP19 (Speculations) for philosophical interpretations. WP19 is the only paper with speculative claims.

---

## License

7Site Human Use License v1.0. Personal and educational use permitted. Commercial and government use requires written agreement from 7Site LLC. See `LICENSE`.

**Brayden Sanders / 7Site LLC**
Mathematics: Trinity Infinity Geometry (TIG)
Built using [Claude](https://anthropic.com) (Anthropic)
**DOI: [10.5281/zenodo.18852047](https://doi.org/10.5281/zenodo.18852047)**

*(c) 2026 Brayden Sanders / 7Site LLC*
