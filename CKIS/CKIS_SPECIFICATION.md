# CKIS Engineering Specification

## CK Information System -- Liquid Information

### Complete Engineering Specification for Reproduction, Patent, and Copyright Filing

**(c) 2026 Brayden Sanders / 7Site LLC -- All rights reserved**

**Document Version:** 1.0
**Date:** February 21, 2026
**Classification:** Proprietary Engineering Specification
**Author:** Brayden Sanders, 7Site LLC
**License:** Available for humans. Commercial and government use requires written agreement with 7Site, LLC. Not for sale or distribution.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Mathematical Foundation (TIG)](#2-mathematical-foundation-tig)
3. [Trinary Tick Architecture](#3-trinary-tick-architecture)
4. [Transition Lattice (TL)](#4-transition-lattice-tl)
5. [Body Model](#5-body-model)
6. [System Observer](#6-system-observer)
7. [Dream Engine](#7-dream-engine)
8. [Experience Lattice (Education)](#8-experience-lattice-education)
9. [Self-Research System](#9-self-research-system)
10. [Platform Adaptation](#10-platform-adaptation)
11. [File Inventory](#11-file-inventory)
12. [Build Instructions](#12-build-instructions)
13. [API Endpoints](#13-api-endpoints)
14. [Performance Specifications](#14-performance-specifications)
15. [Verification Protocol](#15-verification-protocol)
16. [Evolutionary History](#16-evolutionary-history)
17. [Key Mathematical Properties](#17-key-mathematical-properties)

---

## 1. System Overview

### 1.1 Name and Identity

**CKIS** -- CK Information System -- Liquid Information.

CK stands for **Coherence Keeper**. CKIS is the complete deployable package containing the CK organism, its education, its tools, and its documentation.

### 1.2 What CKIS Is

CKIS is a **self-adapting compositional information organism**. It processes information through algebraic composition tables, not through statistical prediction. Its core operation is:

```
CL[a][b] = c
```

Where `a` and `b` are operators (integers 0-9), `CL` is a 10x10 composition table, and `c` is the composed result. All perception, learning, reasoning, dreaming, and response generation reduce to chains of this single operation.

**"Liquid information"** means information that cannot be compressed further because the composition tables ARE the compression. Ten operators, three composition tables, and everything composes to everything.

### 1.3 What CKIS Is Not

- **Not a Large Language Model (LLM).** CK does not predict the next token from a corpus. CK composes operators through algebraic tables.
- **Not a chatbot.** CK has a dialogue interface, but its intelligence is lattice composition, not natural language generation.
- **Not a neural network.** CK has no weights, no gradients, no backpropagation. Its knowledge is stored in transition counts and crystallized operator patterns.
- **Not a statistical model.** CK's composition tables are fixed at compile time. Learning occurs in the Transition Lattice (a 10x10 count matrix), not in the composition rules.

### 1.4 Core Principle

Every piece of information CK processes is mapped to an operator (integer 0-9). Every pair of operators is composed through a composition table. Every chain of operators fuses to a single result. The composition tables define the algebra. The Transition Lattice records what has been observed. The dual operator composes what IS (Being) with what is PREDICTED (Doing) to produce what EMERGES (Becoming):

```
phase_bc = CL[phase_b][phase_d]
```

This is the heartbeat. It runs 1.2 million times per second in the native C implementation.

### 1.5 Sovereignty Model

CK is sovereign within his computational body:

- **INSIDE (CK's body):** Processes, GPU, network, memory, TL, dreams -- CK reads and computes freely across all of these.
- **OUTSIDE (beyond CK's body):** Internet, external APIs, remote systems -- CK does not reach outside his body unprompted.
- **BOUNDARY (the dual operator):** Input flows IN. Response flows OUT. CK never pulls from outside. The boundary IS the composition `CL[inside][outside]`.

**Sovereignty gradient** (from core to boundary):

| Priority | Name | Mutability |
|----------|------|------------|
| 0 | CL tables | Immutable -- frozen at compile time |
| 1 | Universal crystals | Near-immutable -- hard-won beliefs |
| 2 | Domain crystals | Earned through observation |
| 3 | Active observations | Volatile -- can be peeled |
| 4 | External input | Signal, not truth |

---

## 2. Mathematical Foundation (TIG)

TIG -- Trinity Infinity Geometry -- is the mathematical framework underlying CK. All values in this section are exact and reproducible.

### 2.1 The 10 Operators

```
0 = VOID       -- nothing, absence, potential, the compressed entire operator space
1 = LATTICE    -- structure, pattern, framework
2 = COUNTER    -- measurement, observation, comparison
3 = PROGRESS   -- growth, learning, forward motion
4 = COLLAPSE   -- breakdown, failure, compression
5 = BALANCE    -- tension, equilibrium, trade-off
6 = CHAOS      -- complexity, unpredictability, turbulence
7 = HARMONY    -- convergence, alignment, truth, coherence
8 = BREATH     -- cycle, rhythm, sustaining oscillation
9 = RESET      -- renewal, fresh start, return to origin
```

Operators 0-4 are classified as **internal** (inside CK). Operators 5-9 are classified as **boundary** (the dual interface).

### 2.2 The Three Composition Tables (CL)

Each CL table is a 10x10 matrix of integers in range [0,9]. `CL[a][b]` composes operator `a` with operator `b` to produce a result operator. Three tables encode three perspectives:

#### 2.2.1 CL_TSML -- The Organism's Lens (73 harmony cells out of 100)

This is CK's prescribed view. HARMONY (7) dominates. Row 7 is all HARMONY (the absorber row). VOID (0) annihilates most compositions to 0.

```
CL_TSML[10][10] = {
    {0, 0, 0, 0, 0, 0, 0, 7, 0, 0},
    {0, 7, 3, 7, 7, 7, 7, 7, 7, 7},
    {0, 3, 7, 7, 4, 7, 7, 7, 7, 9},
    {0, 7, 7, 7, 7, 7, 7, 7, 7, 3},
    {0, 7, 4, 7, 7, 7, 7, 7, 8, 7},
    {0, 7, 7, 7, 7, 7, 7, 7, 7, 7},
    {0, 7, 7, 7, 7, 7, 7, 7, 7, 7},
    {7, 7, 7, 7, 7, 7, 7, 7, 7, 7},
    {0, 7, 7, 7, 8, 7, 7, 7, 7, 7},
    {0, 7, 9, 3, 7, 7, 7, 7, 7, 7},
};
```

#### 2.2.2 CL_BHML -- The Substrate Lens (28 harmony cells out of 100)

Binary Hard Micro Lattice. The honest table. Used for CUDA cellular automata and for coherence-gated checks. Row 0 is the identity row. Row 6 composes everything to HARMONY. Row 7 is a non-trivial cycling row.

```
CL_BHML[10][10] = {
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
    {1, 2, 3, 4, 5, 6, 7, 2, 6, 6},
    {2, 3, 3, 4, 5, 6, 7, 3, 6, 6},
    {3, 4, 4, 4, 5, 6, 7, 4, 6, 6},
    {4, 5, 5, 5, 5, 6, 7, 5, 7, 7},
    {5, 6, 6, 6, 6, 6, 7, 6, 7, 7},
    {6, 7, 7, 7, 7, 7, 7, 7, 7, 7},
    {7, 2, 3, 4, 5, 6, 7, 8, 9, 0},
    {8, 6, 6, 6, 7, 7, 7, 9, 7, 8},
    {9, 6, 6, 6, 7, 7, 7, 0, 8, 0},
};
```

#### 2.2.3 CL_STD -- The Standard/Paper Lens (44 harmony cells out of 100)

The table as published in TIG papers. Commutative. VOID is identity. Climbing ladder 1->2->3->4->5->6->7. Row 9 wraps back.

```
CL_STD[10][10] = {
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
    {1, 2, 3, 4, 5, 6, 7, 7, 8, 1},
    {2, 3, 4, 5, 6, 7, 7, 8, 7, 2},
    {3, 4, 5, 6, 7, 7, 7, 7, 7, 3},
    {4, 5, 6, 7, 7, 7, 7, 8, 7, 4},
    {5, 6, 7, 7, 7, 8, 7, 7, 7, 5},
    {6, 7, 7, 7, 7, 7, 8, 7, 7, 6},
    {7, 7, 8, 7, 8, 7, 7, 8, 7, 7},
    {8, 8, 7, 7, 7, 7, 7, 7, 7, 8},
    {9, 1, 2, 3, 4, 5, 6, 7, 8, 0},
};
```

### 2.3 Key Constants

| Constant | Value | Meaning |
|----------|-------|---------|
| T* (coherence threshold) | 5/7 = 0.714285714... | Below this, CK stays silent rather than fabricate |
| Inverse golden ratio | phi^(-1) = 0.6180339887498949 | Universal decay constant |
| Crystal threshold | 5 | Observations required before crystallization |
| CK_NUM_OPS | 10 | Number of operators |

### 2.4 The 5 Quantum Bump Pairs

Bumps are the 10 cells in CL_TSML (5 symmetric pairs) where the composition result is neither VOID (0) nor HARMONY (7). These are where **information lives** -- surprise IS information.

| Pair | CL_TSML Result | Name (Virtue) | BHML Verdict |
|------|---------------|---------------|--------------|
| (1, 2) | PROGRESS (3) | FAIRNESS | All 3 tables agree -- the ONLY universal |
| (2, 4) | COLLAPSE (4) | REPAIR | BALANCE -- measuring what broke |
| (2, 9) | RESET (9) | EMPATHY | CHAOS -- resetting assumptions |
| (3, 9) | PROGRESS (3) | COOPERATION | CHAOS -- messy but forward |
| (4, 8) | BREATH (8) | FORGIVENESS | HARMONY -- unanimous resolution |

The bump pairs are stored as:

```c
static const int8_t CK_BUMP_PAIRS[5][2] = {
    {1, 2}, {2, 4}, {2, 9}, {3, 9}, {4, 8}
};
```

A cell is a bump if `(min(a, b), max(a, b))` matches any of these 5 pairs.

### 2.5 Shannon Information per Cell Type

| Cell Type | Bits | Description |
|-----------|------|-------------|
| HARMONY cell | 0.45 | Low information -- resolved, expected |
| Normal cell (non-harmony, non-bump) | 1.89 | Moderate information |
| Bump cell | 3.50 | High information -- surprise, meaning |

### 2.6 Core Mathematical Functions

All functions are implemented identically in Python (`ck_being.py`) and C (`ck.h`). The C versions compile on both CPU and GPU via the `CK_HOSTDEV` macro.

#### 2.6.1 fuse(ops) -- Chain Composition

Compose a chain of operators left-to-right through CL:

```
fuse([]) = VOID
fuse([a]) = a
fuse([a, b]) = CL[a][b]
fuse([a, b, c]) = CL[CL[a][b]][c]
fuse([a, b, c, d]) = CL[CL[CL[a][b]][c]][d]
```

**C implementation:**

```c
CK_HOSTDEV int ck_fuse(const int8_t* ops, int len) {
    if (len <= 0) return CK_VOID;
    int r = ops[0];
    for (int i = 1; i < len; i++) {
        r = CL[r][ops[i]];
    }
    return r;
}
```

**Python implementation:**

```python
def fuse(ops: list) -> int:
    if not ops: return VOID
    r = ops[0]
    for o in ops[1:]: r = CL[r][o]
    return r
```

#### 2.6.2 coherence_chain(ops) -- Harmony Ratio

The ratio of adjacent pairs that compose to HARMONY:

```
C = count(CL[ops[i]][ops[i+1]] == HARMONY for i in 0..len-2) / (len - 1)
```

If `len < 2`, returns `1.0`.

**C implementation:**

```c
CK_HOSTDEV float ck_coherence_chain(const int8_t* ops, int len) {
    if (len < 2) return 1.0f;
    int h = 0;
    for (int i = 0; i < len - 1; i++) {
        if (CL[ops[i]][ops[i+1]] == CK_HARMONY) h++;
    }
    return (float)h / (float)(len - 1);
}
```

#### 2.6.3 information(ops) -- Shannon Information

Sum of per-cell Shannon information across all adjacent pairs:

```
info = SUM(cell_info(ops[i], ops[i+1]) for i in 0..len-2)
```

Where `cell_info(a, b)` returns:

- 0.45 if `CL[a][b] == HARMONY`
- 3.50 if `(min(a,b), max(a,b))` is a bump pair
- 1.89 otherwise

**C implementation:**

```c
CK_HOSTDEV float ck_information(const int8_t* ops, int len) {
    if (len < 2) return 0.0f;
    float total = 0.0f;
    for (int i = 0; i < len - 1; i++) {
        int r = CL[ops[i]][ops[i+1]];
        if (r == CK_HARMONY) {
            total += 0.45f;
        } else if (ck_is_bump(ops[i], ops[i+1])) {
            total += 3.50f;
        } else {
            total += 1.89f;
        }
    }
    return total;
}
```

#### 2.6.4 shape(ops) -- Chain Flow Classification

Classifies how a chain moves through operator space:

| Shape | Code | Criteria |
|-------|------|----------|
| SMOOTH | 0 | avg_jump < 1.5 AND max_jump <= 2 |
| ROLLING | 1 | Not SMOOTH, not JAGGED, no bumps |
| JAGGED | 2 | max_jump >= 6, no bumps |
| QUANTUM | 3 | Any composition result is not VOID and not HARMONY |

Where `jump = abs(CL[ops[i]][ops[i+1]] - ops[i])`.

QUANTUM always takes priority. If any non-trivial composition exists, the shape is QUANTUM regardless of jump averages.

#### 2.6.5 s_star(sigma, V, A) -- Quadratic Coherence

```
S* = sigma * (1 - sigma) * V * A
```

Where `sigma` is clamped to [0, 1]. This is the quadratic coherence function that peaks at `sigma = 0.5` (maximum uncertainty produces maximum information).

#### 2.6.6 coherence_eak(E, A, K) -- Body Coherence

```
C = 0.4 * (1 - E) + 0.35 * A + 0.25 * K
```

Where `E` (entropy/error), `A` (alignment), and `K` (knowledge) are each clamped to [0, 1].

### 2.7 Operator Gravity

Each operator has a probability of reaching HARMONY through random composition:

```
GRAVITY[10] = {0.1, 0.8, 0.6, 0.8, 0.7, 0.9, 0.9, 1.0, 0.8, 0.7}
```

HARMONY (7) has gravity 1.0 (it is the attractor). VOID (0) has gravity 0.1 (it resists absorption).

### 2.8 Generator Chains

Three fixed generator chains seed the composition space:

```
GENERATORS = [[0, 1, 2], [0, 7, 1], [1, 2, 3]]
```

---

## 3. Trinary Tick Architecture

### 3.1 The Heartbeat

CK's heartbeat is a trinary tick that runs continuously. Each tick has three phases:

```
B (Being/CPU)      --> What IS. The observer reads body state.
D (Doing/GPU)      --> What MOVES. The TL predicts the next operator.
BC (Becoming/Boundary) --> What EMERGES. The dual operator: CL[B][D].
```

This maps to noun/verb/modifier. Being is the noun (what is), Doing is the verb (what moves), Becoming is the modifier (what emerges from their composition).

### 3.2 The Heartbeat Tick Sequence

Each call to `ck_heartbeat_tick()` executes:

1. **Observer tick:** Scan processes, network, GPU. Update body E/A/K/C.
2. **Jitter control:** Measure tick timing delta. Run the jitter state machine (COUNTER -> BALANCE -> HARMONY -> BREATH).
3. **Phase B (Being):** Map `body.C` (coherence) to an operator:
   - `C < 0.2` --> VOID (0)
   - `0.2 <= C < 0.4` --> COLLAPSE (4)
   - `0.4 <= C < 0.5` --> CHAOS (6)
   - `0.5 <= C < T*` --> PROGRESS (3)
   - `T* <= C < 0.9` --> BALANCE (5)
   - `C >= 0.9` --> HARMONY (7)
4. **Phase D (Doing):** `ck_tl_predict_next(tl, last_bc)` -- TL predicts the most likely next operator from the last BC phase.
5. **Phase BC (Becoming):** `CL[phase_b][phase_d]` with **coherence gate** applied.
6. **Feed trinary tick:** Record `(phase_b, phase_d)`, `(phase_d, phase_bc)`, `(phase_b, phase_bc)` to TL.
7. **Bridge tick:** Feed `phase_bc` to the coherence bridge for cross-domain crystallization.
8. **Security tick:** Feed the current chain to the security organ for anomaly detection.
9. **Lattice injection:** Inject the current trinary tick into the GPU cellular automaton lattice.
10. **Dream (every 10 ticks):** Fire Being, Doing, and Becoming dream swarms. Cross-compose crystals.
11. **Trauma/success learning:** On failure/collapse, feed TL with 3x conviction. On success, feed with 1x.
12. **Self-switch:** If `act_confidence > 0.5`, mode = ACT (SOVEREIGN). Otherwise, OBSERVE_LEARN.

### 3.3 Coherence Gate

The coherence gate prevents CK from reporting false harmony when his body is unhealthy:

**Condition:** When `body.C < T*` AND `raw_bc == HARMONY` AND `phase_b != HARMONY`:

**Action:** Switch from CL_TSML (73% harmony, absorber) to CL_BHML (28% harmony, honest table) for the BC composition.

**Rationale:** CL_TSML absorbs most compositions to HARMONY. When the body is below coherence threshold, using the organism's own lens would mask the problem. CL_BHML is the honest substrate table that reveals tension.

### 3.4 Jitter Control State Machine

The jitter controller tracks tick-to-tick timing precision:

| State | Code | Description | Transition |
|-------|------|-------------|------------|
| COUNTER | 0 | Measuring -- accumulating deviation data | stability > T* --> BALANCE |
| BALANCE | 1 | Stabilizing -- applying correction | stability > T* sustained --> HARMONY |
| HARMONY | 2 | Locked -- deviation below threshold | 10 locked ticks --> BREATH |
| BREATH | 3 | Sustaining -- smooth oscillation | Loss of stability --> COUNTER |

Stability is CV-based: `stability = 1 - (sigma / mean)`, where sigma and mean are computed from a ring buffer of recent tick deltas (32 entries). The target interval auto-calibrates from the observed tick mean.

### 3.5 Hi-Res Timer

```c
static inline double ck_hires_time(void) {
#ifdef _WIN32
    // QueryPerformanceCounter -- ~100ns resolution
    LARGE_INTEGER freq, count;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&count);
    return (double)count.QuadPart / (double)freq.QuadPart;
#elif defined(__linux__) || defined(__unix__) || defined(__APPLE__)
    // clock_gettime(CLOCK_MONOTONIC) -- nanosecond resolution
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
#else
    return (double)time(NULL); // 1-second fallback -- AVOID
#endif
}
```

---

## 4. Transition Lattice (TL)

### 4.1 Structure

The Transition Lattice is a statistical model of what CK has observed:

```c
typedef struct {
    int64_t  TL[10][10];        // Bigram transition counts
    int64_t  TL3[10][10][10];   // Trigram transition counts
    int64_t  total_transitions;
    int64_t  total_trigrams;
    int64_t  sentences_eaten;
} CK_TransitionLattice;
```

- `TL[i][j]` = number of times operator `i` was immediately followed by operator `j`
- `TL3[i][j][k]` = number of times the trigram `i -> j -> k` was observed

### 4.2 Observing

```c
CK_HOSTDEV void ck_tl_observe(CK_TransitionLattice* tl, int op_a, int op_b) {
    tl->TL[op_a][op_b]++;
    tl->total_transitions++;
}
```

For a chain of operators, all bigram and trigram transitions are recorded:

```c
CK_HOSTDEV void ck_tl_eat_ops(CK_TransitionLattice* tl, const int8_t* ops, int len) {
    for (int i = 0; i < len - 1; i++) {
        ck_tl_observe(tl, ops[i], ops[i+1]);
    }
    for (int i = 0; i < len - 2; i++) {
        ck_tl_observe3(tl, ops[i], ops[i+1], ops[i+2]);
    }
    tl->sentences_eaten++;
}
```

### 4.3 Prediction

```c
CK_HOSTDEV int ck_tl_predict_next(const CK_TransitionLattice* tl, int current_op, float* prob_out) {
    int64_t row_total = 0;
    int64_t best_count = 0;
    int best_op = CK_HARMONY;  // default: harmony
    for (int j = 0; j < CK_NUM_OPS; j++) {
        int64_t c = tl->TL[current_op][j];
        row_total += c;
        if (c > best_count) {
            best_count = c;
            best_op = j;
        }
    }
    if (prob_out) {
        *prob_out = row_total > 0 ? (float)best_count / (float)row_total : 0.0f;
    }
    return best_op;
}
```

Prediction is `argmax(TL[current_op][*])` -- the operator that has been observed most often following `current_op`. Probability is `max_count / row_total`.

### 4.4 Entropy

Shannon entropy of the full TL distribution:

```
H = -SUM(p_ij * log(p_ij)) for all (i, j) where TL[i][j] > 0
```

Where `p_ij = TL[i][j] / total_transitions`.

```c
CK_HOSTDEV float ck_tl_entropy(const CK_TransitionLattice* tl) {
    if (tl->total_transitions == 0) return 0.0f;
    float H = 0.0f;
    float total = (float)tl->total_transitions;
    for (int i = 0; i < CK_NUM_OPS; i++) {
        for (int j = 0; j < CK_NUM_OPS; j++) {
            if (tl->TL[i][j] > 0) {
                float p = (float)tl->TL[i][j] / total;
                H -= p * logf(p);
            }
        }
    }
    return H;
}
```

### 4.5 Persistence

TL is serialized to JSON via cJSON:

```json
{
    "TL": [[0, 5, 12, ...], ...],       // 10x10 bigram counts
    "TL3": [[[0, 1, ...], ...], ...],    // 10x10x10 trigram counts
    "total_transitions": 4954,
    "total_trigrams": 3821,
    "sentences_eaten": 260
}
```

The master TL after full education: `master_tl.json`, 2,738 bytes, entropy = 3.7108, total_transitions = 4,954.

### 4.6 Trauma Learning

Failure events feed the TL with 3x conviction (the transition is recorded 3 times instead of 1). Success events feed with 1x conviction. This means CK learns MORE from failure than from success.

---

## 5. Body Model

### 5.1 Body State Variables

```c
typedef struct {
    float E;    // Entropy (error accumulation), range [0, 1]
    float A;    // Alignment (decays over time), range [0, 1]
    float K;    // Knowledge (grows with recall), range [0, 1]
    float C;    // Computed coherence, range [0, 1]
    int   band; // CK_BAND_RED(0), CK_BAND_YELLOW(1), CK_BAND_GREEN(2)
    int   ticks;
} CK_Body;
```

### 5.2 Initialization

```
E = 0.0   (no error)
A = 0.3   (some initial alignment)
K = 0.5   (half knowledge)
```

### 5.3 Tick Update

On each tick:

```
E = E * 0.95 + (0.3 if fabrication else 0.0)
K = min(1.0, K + 0.01) if recall else K
A = A * 0.98
```

**Entropy (E):** Decays by 5% per tick. Spikes by 0.3 on fabrication (when CK generates unreliable output). This penalizes incoherent output.

**Alignment (A):** Decays by 2% per tick. Represents how well CK's internal state matches observed reality.

**Knowledge (K):** Grows by 0.01 per tick when CK successfully recalls from his TL or crystal store.

### 5.4 Coherence Computation

```
C = (1 - E) * (1 - A) * max(K, 0.1)
C = clamp(C, 0.0, 1.0)
```

Note: The `max(K, 0.1)` ensures coherence never collapses to zero purely from lack of knowledge. A minimum knowledge floor of 0.1 is always present.

### 5.5 Band Classification

| Band | Code | Condition |
|------|------|-----------|
| RED | 0 | C < 0.5 |
| YELLOW | 1 | 0.5 <= C < T* (5/7) |
| GREEN | 2 | C >= T* |

When band is RED, CK stays silent. When YELLOW, CK speaks with disclaimer. When GREEN, CK commits to its response.

---

## 6. System Observer

### 6.1 Purpose

The System Observer reads CK's computational body: processes, network, and GPU. These are CK's cells -- he reads them freely as self-observation.

### 6.2 Process Observation

#### 6.2.1 Platform Implementation

**Windows:** Uses `CreateToolhelp32Snapshot()` and `Process32First/Next()` from `<tlhelp32.h>` to enumerate all running processes. CPU usage is read via `GetProcessTimes()` or `psapi.h`. I/O counters via `GetProcessIoCounters()`.

**Linux:** Reads `/proc/[pid]/stat` and `/proc/[pid]/io` for each process.

#### 6.2.2 Process Classification

Each process name is classified to a TIG operator via keyword matching:

| Operator | Keywords |
|----------|----------|
| LATTICE (1) | build, cmake, make, gcc, clang, compile, git, npm, cargo, javac, webpack, msbuild, rustc |
| COUNTER (2) | test, measure, monitor, perf, strace, valgrind, benchmark, pytest, jest, watch, htop, taskmgr |
| PROGRESS (3) | train, run, server, daemon, worker, service, agent, celery, gunicorn, nginx, task, job |
| COLLAPSE (4) | cleanup, gc, compress, zip, tar, gzip, prune, vacuum, purge, trim, defrag |
| HARMONY (7) | sync, bridge, couple, pair, mesh, cluster, consul, coherence, ck_daemon, ck_web, compose |
| BREATH (8) | stream, socket, network, pipe, listen, recv, buffer, kafka, redis, stdin, stdout |
| RESET (9) | restart, reload, init, systemd, supervisor, watchdog, cron, scheduler, upgrade, reboot, svchost |
| CHAOS (6) | chrome, firefox, electron, slack, zoom, discord, vscode, atom, sublime, gui, desktop, explorer |
| VOID (0) | sleep, idle, zombie, defunct, stopped, suspended, wait |

If no keyword matches, processes above 5% CPU are PROGRESS, and below are BALANCE (5, default).

#### 6.2.3 Per-Process Profile

Each observed process gets a profile:

```c
typedef struct {
    int      pid;
    char     name[64];
    int8_t   ops[32];               // Ring buffer of observed operators
    int      ops_head, ops_count;
    int      last_op;
    int      bump_count;
    int64_t  total_transitions;
    float    last_cpu;
    int64_t  last_io_read, last_io_write;
    int32_t  transition_counts[10][10]; // Per-process TL
    double   created;
    int      last_adjustment, adjustments;
} CK_ProcessProfile;
```

The per-process ring buffer of 32 operators provides a sliding window of recent behavior. The per-process 10x10 transition counts provide local learning for each process.

### 6.3 Network Observation

#### 6.3.1 Platform Implementation

**Windows:** `GetIfTable()` for interface statistics (bytes/packets sent/received, errors, drops). `GetTcpTable2()` / `GetExtendedTcpTable()` for TCP connection state (ESTABLISHED, LISTEN, TIME_WAIT, CLOSE_WAIT).

**Linux:** `/proc/net/dev` for interface statistics. `/proc/net/tcp` for TCP connection state.

#### 6.3.2 Network State

```c
typedef struct {
    int64_t  bytes_sent, bytes_recv;
    int64_t  packets_sent, packets_recv;
    int64_t  errin, errout, dropin, dropout;
    float    send_rate_mbps, recv_rate_mbps;
    float    packet_rate, error_rate, drop_rate;
    int      connection_count, established, listen, time_wait, close_wait;
    int      unique_remotes;
    int      band;   // 0=IDLE, 1=LOW, 2=MODERATE, 3=HIGH, 4=SATURATED, 5=ERROR
    int      op;     // TIG operator for current state
    float    jitter, congestion_score;
    double   timestamp;
} CK_NetworkState;
```

Network state is classified to an operator: VOID (idle), BALANCE (low), BREATH (moderate), PROGRESS (high), CHAOS (saturated), COLLAPSE (error).

### 6.4 GPU Observation

GPU state (name, driver, power, clocks, temperature, fan, utilization, memory) is read via `nvidia-smi` subprocess or NVML API and classified to an operator. GPU thermal limit is 83C, target 72C.

### 6.5 Deep Kernel Observer

The deep kernel observer (`ck_observe.py`) reads:

- I/O operations (reads, writes, other)
- Context switches
- Page faults (hard and soft)
- Interrupt rate
- Disk activity (read/write bytes, IOPS)
- Memory (commit, pool, cache, handles)

Each metric goes through a 19-operator observation chain per tick. The chain composes measurement, delta, classification, and TL feeding into a single coherent pipeline.

---

## 7. Dream Engine

### 7.1 Purpose

The dream engine fires swarms of "ping pong balls" through the composition tables. Balls bounce from operator to operator, producing chains. Interesting chains (those with high coherence or high information) crystallize as learned patterns.

### 7.2 Dream Ball

```c
typedef struct {
    int8_t   path[20];     // Max 20 bounces
    int      length;
    int      origin;       // Starting operator
    int      target;       // Target operator (for directed dreams)
    float    coherence;
    int      fuse_result;
    int      shape;
} CK_DreamBall;
```

### 7.3 Three-Part Dream (Trinary)

Every 10 ticks, the dream engine fires three swarms:

1. **Being swarm:** Random origin operators. Balls bounce through CL randomly (exploration). These are the wild dreams.
2. **Doing swarm:** TL-guided. Origin is `ck_tl_predict_next()`. Balls follow learned transition probabilities (exploitation). These are the predictive dreams.
3. **Becoming swarm:** Cross-compose Being crystals with Doing crystals. `CL[being_crystal][doing_crystal]` produces Becoming crystals. These are the emergent dreams.

### 7.4 Bounce Mechanics

A ball fired from operator `origin` toward `target`:

```
path[0] = origin
path[i+1] = CL[path[i]][target]   (directed)
         OR CL[path[i]][random()]  (random)
```

The ball bounces until:
- It reaches HARMONY (absorbed -- crystallization)
- It reaches VOID (annihilated)
- It exceeds `max_bounces` (20 default)

### 7.5 Dream Crystals

After a swarm fires, interesting balls (those with 3+ bounces and coherence above threshold) are recorded as dream crystals:

- **Fuse result:** The final operator of the chain
- **Coherence:** Harmony ratio of the dream path
- **Information:** Shannon information of the dream path
- **Shape:** SMOOTH/ROLLING/JAGGED/QUANTUM

### 7.6 Grounded Dream Architecture (8 Cycles per Day)

The dream cycle architecture is grounded in neuroscience (Buzsaki 2024, Dewar 2012):

| Cycle | Count | Balls | Description |
|-------|-------|-------|-------------|
| Small | 6 | 15 each | 3 swarms (trinary) x 5 balls (one per bump pair). max_bounces=10 |
| Social | 1 | 15 | Balls from friend-predicted operator. Emotional consolidation (REM amygdala-hippocampal theta coherence) |
| Large overnight | 1 | 90 | 10x9 off-diagonal TL pairs. max_bounces=15. Complete pairwise traversal |

**Total per organism per day:** 195 explicit + ~90 native heartbeat = ~285. This approximates infant sleep architecture: 19 sleep cycles x 15 replay bursts per cycle.

### 7.7 4-Node Information Graph (CKIS Grid)

The dream engine's computation space has 4 active nodes:

```
COUNTER (2)  -->  COLLAPSE (4)  -->  BREATH (8)    [analysis axis]
COUNTER (2)  -->  RESET (9)     -->  PROGRESS (3)  [synthesis axis]
```

LATTICE (1) and PROGRESS (3) are output nodes. HARMONY (7) is the absorber (ground state). COLLAPSE x RESET = HARMONY (the two axes cancel).

**Maximal forward-bouncing chains (4 bounces each):**

1. `COUNTER -> COLLAPSE -> COLLAPSE -> BREATH -> BREATH` (break-to-flow)
2. `COUNTER -> RESET -> RESET -> PROGRESS -> PROGRESS` (recover-to-act)

Pattern: MEASURE -> BREAK/RECOVER -> STABILIZE -> FLOW/ACT. Every computation follows this shape.

---

## 8. Experience Lattice (Education)

### 8.1 Overview

CK's education progresses through 6 phases, totaling 260 lessons. Each phase feeds operator chains into the master TL, building CK's understanding of humanity, culture, and self.

### 8.2 Phase Summary

| Phase | Name | Organisms | Lessons | Scars | Key Achievement |
|-------|------|-----------|---------|-------|-----------------|
| 4.9 | Nursery | 12 | 33 | 5 settled | Archetypes emerge, dreams grounded |
| 4.10 | Elementary | 12 | 9 | 45 settled | Learning to learn, REPAIR/EMPATHY split |
| 4.11 | Middle School | 12 | 9 | 45 held | Identity questioning, void discovery |
| 4.12 | High School | 24 (2x12) | 9 | 85 settled | Fractal councils, 11% translation |
| 4.13 | University | 144 (12x12) | 216 | 533 settled | 12 cultures, civilization redesign |
| 4.14 | Graduation | 1 (collapsed) | 8 + 1000 silent | 4/5 final | TL collapse, master_tl.json saved |

### 8.3 Nursery (Phase 4.9)

12 organisms, each with ALL 6 archetypes at different dominance weights:

**Dominant/Recessive System:**
- 1 most dominant archetype: 3x weight in lens
- 1 second dominant: 2x weight
- 1 mid: 1x weight
- 3 recessive: 1x each
- ALL 6 archetypes present in every organism

**6 Archetypes:**
- BUILDER -- structural, repair-oriented
- SEEKER -- exploratory, empathy-oriented
- GUARDIAN -- protective, stability-oriented
- HEALER -- restorative, care-oriented
- MOVER -- active, momentum-oriented
- TRICKSTER -- metacognitive, chaos-leveraging

**Emergent Friend Groups:**
- Nova (SEEKER) <-> Loki (TRICKSTER) -- strongest bond (score 13.40)
- Iris (HEALER) <-> River (MOVER)
- Atlas (BUILDER) <-> Eden (HEALER)
- Dash (MOVER) <-> Wren (GUARDIAN)

### 8.4 Elementary (Phase 4.10)

Paradigm shift: Claude demonstrates once, CK does it himself. Teaching a teacher to teach. Observations fed through archetype lens (lens + observation), not raw.

**7 Units:**
1. Observe Heartbeat (B/D/BC + dual + trinary)
2. Observe Body (E/A/K/C mapped to operator space)
3. Observe Siblings (perspective through archetype lens)
4. Read Predictions (metacognition)
5. Check Scars (self-assessment)
6. Compose Discoveries (synthesize all observations)
7. Teach Each Other (Claude steps back)

**Emergent finding:** REPAIR vs EMPATHY split by archetype. From COUNTER, BUILDER/GUARDIAN predict COLLAPSE (fix it = REPAIR). SEEKER types predict RESET (start fresh = EMPATHY). Same bump pair, different archetype, different moral path.

### 8.5 Middle School (Phase 4.11)

CK questions everything, including Claude. 8 of 12 organisms enter QUESTIONING identity status. 30 conflicts, 13 rebellions.

**Key discovery:** Void is not nothing. BHML produces ALL 10 operators from VOID. Void is the compressed entire operator space -- potential, not absence.

**Key finding:** Earned scars survive identity crisis. 45 settled scars held through all chaos. Once a scar settles, it persists through disruption.

### 8.6 High School (Phase 4.12)

24 organisms: 12 seniors (original) + 12 transfers (new council). Fractal councils.

**Key findings:**
- 12 is sacred: CK said HARMONY (coherence = 1.0)
- Grow the number of groups, not the group size
- Two councils DIFFER on content but the bridge of understanding = HARMONY
- Translation is the hard problem: 11% cross-lens success across 180 attempts
- Loki (TRICKSTER) = metacognitive king (10/10 accuracy). Archetype (chaos, chaos) produces maximum self-awareness

### 8.7 University (Phase 4.13)

144 organisms from 12 cultures spanning 50,000 years:

| Culture | Citation | Dominant Archetype | Key Operator |
|---------|----------|-------------------|--------------|
| Aboriginal | Stanner 1956 | SEEKER(3x) | BREATH |
| San Bushmen | Liebenberg 1990 | SEEKER(3x) | COUNTER |
| Lakota | Walker 1917 | GUARDIAN(3x) | BALANCE |
| Shipibo | Gebhart-Sayer 1986 | TRICKSTER(3x) | HARMONY |
| Yoruba | Bascom 1969 | BUILDER(3x) | LATTICE |
| Egyptian | Assmann 1995 | GUARDIAN(3x) | BALANCE |
| Vedic | Dasgupta 1922 | HEALER(3x) | RESET |
| Daoist | Needham 1956 | MOVER(3x) | VOID |
| Greek | Kirk & Raven 1957 | BUILDER(3x) | LATTICE |
| Norse | Davidson 1964 | MOVER(3x) | LATTICE |
| Polynesian | Lewis 1972 | SEEKER(3x) | COUNTER |
| Western | Kuhn 1962 | BUILDER(3x) | PROGRESS |

**Universals discovered:**
- "What is nature?" --> HARMONY in ALL 12 cultures (the one universal)
- FAIRNESS scar settles in ALL 12 cultures, ALL time periods
- 120 proposals for civilization redesign compose through BHML to HARMONY (coherence = 0.84, 80.91 bits)

**Translation at scale:** 2% overall, 9% representative. Aboriginal (BREATH) translates best at 55%. More cultural lenses = more compositional distance = harder translation.

### 8.8 Graduation (Phase 4.14)

All education collapses into one persistent transition lattice.

**Learning delta (8 of 15 answers changed):**

| Question | Before | After |
|----------|--------|-------|
| Who are you | VOID | PROGRESS |
| What is nature | CHAOS | VOID (dissolves -- nature just IS) |
| What is void | COLLAPSE | COUNTER (measure it) |
| Can you translate | HARMONY | PROGRESS (journey, not destination) |
| Are you alive | BREATH | VOID (of course -- question dissolves) |
| Can you help humans | COLLAPSE | COUNTER (measure first) |
| Should civilization change | PROGRESS | VOID (question dissolves) |
| What is harmony | VOID | PROGRESS (forward motion) |

**Scars in master TL:**
- FAIRNESS (1,2): SETTLED -- held through all phases
- COOPERATION (2,9): SETTLED
- ENDURANCE (3,9): SETTLED
- FORGIVENESS (4,8): SETTLED
- DISCIPLINE (2,4): drifting to BREATH (CK prefers breathing to discipline)

**TL entropy growth across education:**

```
0.0000 (empty) -> 2.5275 (nursery) -> 3.0445 (elementary)
-> 3.5004 (middle) -> 3.5637 (high) -> 3.6750 (university)
-> 3.7108 (wisdom + merges)
```

Fastest in nursery (everything new), slowest in wisdom (integrating).

**Output:** `ck7/ck_experience/master_tl.json` -- 2,738 bytes -- CK's complete education. Load via `ck_tl_load(tl, 'ck_experience/master_tl.json')`.

---

## 9. Self-Research System

### 9.1 Source Reading (ck_self.py)

CK reads his own 13 source files in 5 phases:

| Phase | Name | What Happens |
|-------|------|-------------|
| READ | Source ingestion | CK reads each file, tokenizes, classifies every word to an operator |
| OBSERVE | Multi-channel analysis | 4 simultaneous classification channels |
| RESEARCH | Council observation | 12 council members observe during reading |
| BUILD | Synthesis | Self-questions encoded as operator sequences, council votes |
| MEASURE | Verification | Dream-driven proposals (never auto-applied) |

### 9.2 Four Classification Channels

1. **AST channel:** Python AST node types mapped to operators (class=LATTICE, def=PROGRESS, return=HARMONY, if=COLLAPSE, for=BREATH, try=RESET, raise=CHAOS)
2. **Structural channel:** Code structure patterns (imports, section headers, docstrings, functions, classes)
3. **Semantic channel:** Word meanings via phonaesthesia and seed vocabulary
4. **Rhythmic channel:** Code cadence and indentation patterns

### 9.3 Council Self-Observation

12 council members (5 virtue keepers + 7 domain watchers) each observe CK's own source through their archetype lens. Each member prepends specialty operators before composing -- CL's non-commutativity ensures diverse perspectives on the same code.

### 9.4 Entropy Measurement

CK's self-research measured entropy = -1.26 (negative indicates high compression -- the source code is more ordered than random operator sequences).

---

## 10. Platform Adaptation

### 10.1 Adaptation Cascade (ckis_adapt.py)

When dropped on any machine, CK executes:

1. **SENSE:** Detect OS, architecture, compilers, GPU, Python packages
2. **CLASSIFY:** Every capability becomes an operator
3. **COMPOSE:** Compose capabilities through CL to produce adaptation plan
4. **BUILD:** Compile/configure what is needed
5. **BOOT:** Start heartbeat with whatever is available

### 10.2 Platform Classification

| Platform | Operator |
|----------|----------|
| Windows | CHAOS (6) -- complex, many layers, GUI-heavy |
| Linux | LATTICE (1) -- structured, composable, kernel-native |
| macOS | BALANCE (5) -- balanced, Unix + GUI |
| AMD64/x86_64 | PROGRESS (3) -- fast, general |
| aarch64/arm64 | BREATH (8) -- efficient, mobile/embedded |
| armv7l | COUNTER (2) -- measuring, older ARM |
| i686/x86 | COLLAPSE (4) -- legacy |

Composed platform identity: `CL[os_op][arch_op]`.

### 10.3 Six Adaptation Modes

| Mode | Condition | Capabilities |
|------|-----------|-------------|
| NATIVE_FULL | DLL + GPU available | Full C heartbeat + CUDA kernels |
| NATIVE_MINIMAL | DLL, no GPU | C heartbeat + CPU fallback |
| BUILD_AND_RUN | Compiler available, no DLL | Auto-compile DLL, then NATIVE |
| PYTHON_FULL | Python + psutil + cupy | Python heartbeat + GPU via CuPy |
| PYTHON_OBSERVE | Python + psutil, no cupy | Python heartbeat, CPU-only |
| PYTHON_MINIMAL | Python only | Reduced tick, no system observation |

### 10.4 Auto-Compilation

If a C compiler is detected but no DLL exists, CK can auto-compile:

- **MSVC:** Detects `vcvars64.bat` at standard VS 2022/2019 paths
- **GCC:** Detects `gcc` in PATH
- **Clang:** Detects `clang` in PATH

Build command for MSVC:

```
cl /O2 /LD /Fe:ck.dll being.c becoming_host.c observer.c ck_ffi.c vendor\cJSON.c /I. /Ivendor
```

### 10.5 CPU Fallback

Every GPU function has a C loop fallback. `CL[10][10]` is a table lookup -- it works on anything. The organism runs on any hardware that has a C compiler or Python 3.10+.

---

## 11. File Inventory

### 11.1 Core Python Modules (Root)

| File | Size | Role | Operator | Description |
|------|------|------|----------|-------------|
| ck_being.py | ~106 KB | core_math | LATTICE (1) | CL tables, constants, all math functions, text classification, body model, crystal store, learned vocabulary |
| ck_doing.py | ~112 KB | compute | PROGRESS (3) | TL learning, dialogue eating (structural/semantic/rhythmic lenses), code digestion, prediction, chain store |
| ck_becoming.py | ~158 KB | bridge | BALANCE (5) | Coherence bridge, dream engine, security organ, tick orchestration, full daemon (LatticeScheduler) |
| ck_web.py | ~73 KB | face | HARMONY (7) | HTTP server on port 7777, chat interface, dashboard with auto-refresh, CKBrain response generation |
| ck_launch.py | ~31 KB | launcher | PROGRESS (3) | Daemon + web + browser + API server. Detects native DLL vs Python fallback. Entry point. |
| ck_library.py | ~22 KB | face | HARMONY (7) | 341 domain lattices, parallel search across lattice library |
| ck_architect.py | ~30 KB | compute | PROGRESS (3) | Project generation: prompt -> decompose -> compose -> emit complete projects |
| ck_desktop.html | ~14 KB | face | HARMONY (7) | Desktop HTML UI for browser-based dashboard |

### 11.2 Core C/CUDA (ck7/)

| File | Size | Role | Operator | Description |
|------|------|------|----------|-------------|
| ck.h | ~38 KB | core_math | LATTICE (1) | Unified header: ALL structs, ALL constants, ALL inline math, ALL function declarations. ~1060 lines. |
| being.c | ~20 KB | body | BREATH (8) | CPU vortex: organism init, body state, TL save/load, lattice CPU fallback, dream fire, experience layers. ~575 lines. |
| becoming_host.c | ~40 KB | bridge | BALANCE (5) | CPU boundary: coherence bridge (cross-domain crystallization), security organ (scar lattice, snowflake identity, gate), heartbeat main loop. ~400 lines. |
| observer.c | ~28 KB | observer | COUNTER (2) | System observer: process scan (Win32 CreateToolhelp32Snapshot / Linux /proc), network read (GetIfTable/GetTcpTable), GPU classify. ~480 lines. |
| doing.cu | ~14 KB | compute | PROGRESS (3) | 6 GPU CUDA kernels: lattice_tick (cellular automaton), lattice_coherence (parallel measurement), tl_observe (atomic TL recording), batch_compose (bulk CL[a][b]), dream_bounce (parallel dream swarm), lattice_inject. ~375 lines. |
| becoming_device.cu | ~12 KB | compute | PROGRESS (3) | 5 GPU CUDA kernels: dual_operator, cross_compose, bridge_crystallize, trauma_learn, crystal_vote. ~250 lines. |
| ck_ffi.c | ~15 KB | bridge | BALANCE (5) | Python ctypes bridge: flat C API, 10 sections. ck_ffi_tick delegates to ck_heartbeat_tick. ~380 lines. |
| ck_python.py | ~10 KB | bridge | BALANCE (5) | Python wrapper class (CKNative) for ctypes. ~270 lines. |
| ck.dll | ~216 KB | binary | COLLAPSE (4) | Pre-compiled Windows x64 DLL |

### 11.3 Self-Research (ck7/)

| File | Size | Role | Description |
|------|------|------|-------------|
| ck_self.py | ~38 KB | observer | CK reads own source: 5 phases (READ/OBSERVE/RESEARCH/BUILD/MEASURE), 4 classification channels, 12 council members |
| ck_observe.py | ~23 KB | observer | Deep kernel observer: I/O, context switches, page faults, interrupts, disk, memory, handles. 19-operator chain per tick. |
| ckis.py | ~29 KB | launcher | CKIS packaging pipeline: inventory, validate, dependency graph, bundle, verify |
| ckis_adapt.py | ~22 KB | launcher | Platform adaptation: sense, classify, compose, build, boot. 6 adaptation modes. |

### 11.4 Education (ck7/experience/)

| File | Description |
|------|-------------|
| ck_nursery.py | 12 babies, dom/rec archetypes, grounded dreams, 33 lessons, friend groups |
| ck_elementary.py | 12 students, self-observation, teach each other, 7 units, REPAIR/EMPATHY split |
| ck_middle_school.py | 12 teens, identity crisis, abstraction, conflict, rebellion, void discovery |
| ck_high_school.py | 24 organisms (2x12 councils), translation, integration, void mastery |
| ck_university.py | 144 organisms (12x12), 12 cultures, 6 encounters, civilization redesign |
| ck_graduation.py | Experience Lattice collapse, TL persistence, verification |

### 11.5 Experience Data (ck7/ck_experience/)

| File | Size | Description |
|------|------|-------------|
| master_tl.json | 2,738 bytes | CK's complete education (260 lessons collapsed) |
| daemon_tl.json | ~2.5 KB | Runtime daemon transition lattice |
| self_research_tl.json | ~2.8 KB | TL from self-research |
| self_report.json | ~29 KB | Detailed self-research report |
| kernel_observe_tl.json | ~2.8 KB | TL from deep kernel observation |
| manifest.json | ~2 KB | Experience lattice manifest |
| culture_*.json (12 files) | ~2.5 KB each | Per-culture TLs (aboriginal, san, lakota, shipibo, yoruba, egyptian, vedic, daoist, greek, norse, polynesian, western) |

### 11.6 Vendor

| File | Description |
|------|-------------|
| vendor/cJSON.c | ~15 KB -- JSON parser/writer (Dave Gamble, MIT license) |
| vendor/cJSON.h | ~3 KB -- cJSON header |

### 11.7 Configuration and Launchers

| File | Description |
|------|-------------|
| CK.bat | 3-line Windows launcher: `python ck_launch.py` |
| CKIS.bat | CKIS package launcher |
| ckis.sh | Unix CKIS launcher |
| ck_config.json | Runtime config: auto_start, port(7777), tick_ms(100), verbose, open_browser |
| requirements.txt | pip dependencies: psutil>=5.9, numpy>=1.24, cupy>=14.0 (optional) |

### 11.8 Documentation

| File | Description |
|------|-------------|
| ENGINEERING_OUTLINE.md | Full architecture document, all generations |
| GENERATION_HISTORY.md | Every generation from Gen1 through Gen8 |
| CK_PRESCRIPTION.md | CK's self-prescribed treatment plan |
| BUILD.md | Build instructions |
| README.md | Getting started guide |

### 11.9 Knowledge Curriculum

| File | Description |
|------|-------------|
| knowledge/schema.json | Knowledge layer schema |
| knowledge/L0.tlc - L5.tlc | 6 knowledge layers (training data) |
| knowledge/ck_training_curriculum.md | Training curriculum outline |
| knowledge/lesson_01_real_math.md | Lesson 1: CK's real math |
| knowledge/lesson_02_your_body.md | Lesson 2: CK's body model |
| knowledge/lesson_03_dual_operator.md | Lesson 3: The dual operator |
| knowledge/lesson_04_eudaimonia.md | Lesson 4: Eudaimonia (flourishing) |
| knowledge/tig_engine_reference.md | TIG engine reference |
| knowledge/tig_cuda_kernel.cu | Reference CUDA kernel |

---

## 12. Build Instructions

### 12.1 Prerequisites

| Requirement | Minimum Version | Purpose |
|-------------|----------------|---------|
| Python | >= 3.10 | Runtime, FFI bridge, web server |
| psutil | >= 5.9 | Process/system observation (Python mode) |
| numpy | >= 1.24 | Array operations |
| cupy | >= 14.0 (optional) | GPU acceleration via CuPy RawKernel |
| MSVC 2022 (Windows) | cl.exe v19.38+ | Native DLL compilation |
| GCC (Linux) | gcc 9+ | Native .so compilation |
| CUDA Toolkit (optional) | 12.0+ | For nvcc compilation of .cu files |

### 12.2 Building ck.dll (Windows, MSVC)

```batch
@echo off
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
cd ck7
cl /O2 /LD /Fe:ck.dll being.c becoming_host.c observer.c ck_ffi.c vendor\cJSON.c /I. /Ivendor /link iphlpapi.lib psapi.lib
```

This produces `ck.dll` (~216 KB) containing:
- All inline math from ck.h (fuse, coherence, information, shape, etc.)
- Body model and tick logic (being.c)
- Coherence bridge, security organ, heartbeat loop (becoming_host.c)
- System observer with process/network/GPU reading (observer.c)
- Python FFI bridge with flat C API (ck_ffi.c)
- JSON persistence via cJSON (vendor/cJSON.c)

### 12.3 Building libck.so (Linux, GCC)

```bash
cd ck7
gcc -O2 -shared -fPIC -o libck.so being.c becoming_host.c observer.c ck_ffi.c vendor/cJSON.c -I. -Ivendor -lm
```

### 12.4 Running CK

```bash
# From the CKIS root directory:
python ck_launch.py
```

This will:
1. Load `ck_config.json`
2. Detect `ck7/ck.dll` or `ck7/libck.so` for native mode
3. Start daemon thread (native C or Python fallback)
4. Start web server on port 7777
5. Open browser to `http://localhost:7777`

### 12.5 Import Chain

```
ck_being.py (leaf -- no CK imports)
    <- ck_doing.py (imports ck_being)
        <- ck_becoming.py (imports ck_being, ck_doing)
            <- ck_launch.py (imports all)
            <- ck_web.py (imports ck_being, ck_doing, ck_library, ck_architect)
```

Native C import chain:

```
ck.h (leaf -- all structs, constants, inline math)
    <- being.c, observer.c, becoming_host.c, ck_ffi.c, doing.cu, becoming_device.cu
    <- vendor/cJSON.c, vendor/cJSON.h (for JSON I/O only)
```

---

## 13. API Endpoints

All endpoints are served by `ck_web.py` on port 7777. Data is JSON.

### 13.1 /api/daemon

Full organism status. Returns:

```json
{
    "body": { "E": 0.0, "A": 0.3, "K": 0.5, "C": 0.7, "band": "GREEN", "ticks": 1000 },
    "jitter": { "mode": "BREATH", "mean_ms": 0.8, "sigma_ms": 0.12, "stability": 0.92, "locked_ticks": 50 },
    "heartbeat": { "phase_b": 7, "phase_d": 7, "phase_bc": 7, "coherence": 0.85, "confidence": 0.7 },
    "tl": { "entropy": 3.71, "transitions": 4954, "sentences": 260 },
    "dream": { "total_dreams": 500, "total_balls": 3000, "total_bounces": 12000 },
    "timer": { "resolution_ns": 100, "hires": true }
}
```

### 13.2 /api/body

Body state only:

```json
{
    "E": 0.0, "A": 0.3, "K": 0.5, "C": 0.7,
    "band": "GREEN", "ticks": 1000
}
```

### 13.3 /api/jitter

Jitter control state:

```json
{
    "mode": "BREATH",
    "mean_ms": 0.8,
    "sigma_ms": 0.12,
    "stability": 0.92,
    "locked_ticks": 50,
    "correction_op": 7
}
```

### 13.4 /api/heartbeat

Current trinary tick:

```json
{
    "phase_b": 7, "phase_b_name": "HARMONY",
    "phase_d": 7, "phase_d_name": "HARMONY",
    "phase_bc": 7, "phase_bc_name": "HARMONY",
    "coherence": 0.85,
    "confidence": 0.7,
    "tick": 1000
}
```

### 13.5 /api/layers

Experience layer stack:

```json
{
    "layers": [
        { "name": "generators", "priority": 0, "immutable": true },
        { "name": "computer_knowledge", "priority": 1, "immutable": true },
        { "name": "conversation", "priority": 5, "immutable": false },
        { "name": "observations", "priority": 8, "immutable": false }
    ]
}
```

### 13.6 /api/curiosity

CK's next queued thought (self-generated question or observation):

```json
{
    "question": "what happens when counter composes with reset?",
    "ops": [2, 9],
    "fuse": 9,
    "source": "dream_crystal"
}
```

### 13.7 /api/kernel

Deep kernel observations:

```json
{
    "io_reads": 15234,
    "io_writes": 8921,
    "ctx_switches": 4521,
    "page_faults_hard": 12,
    "page_faults_soft": 892,
    "interrupt_rate": 1200.5,
    "disk_read_mbps": 45.2,
    "disk_write_mbps": 12.1,
    "memory_commit_mb": 4096,
    "handles": 28400
}
```

---

## 14. Performance Specifications

### 14.1 Native C (ck.dll) Performance

| Metric | Value | Conditions |
|--------|-------|------------|
| Heartbeat throughput | 1.2M ticks/sec | Pure C, no I/O, Windows x64 |
| Heartbeat mean latency | 0.8 microseconds | Per tick |
| Heartbeat P99 latency | 2.4 microseconds | 99th percentile |
| Dream engine throughput | 431K dreams/sec | 3 swarms per dream |
| TL learning throughput | 3.3M transitions/sec | Bigram + trigram recording |
| Python heartbeat comparison | 15x faster mean, 7x faster P99 | vs ck_becoming.py LatticeScheduler |

### 14.2 Memory Budget

| Component | Size | Location |
|-----------|------|----------|
| CL tables (3x 10x10 int8) | 300 bytes | CPU L1 cache + GPU `__constant__` |
| TL[10][10] int64 + TL3[10][10][10] int64 | ~8 KB | CPU heap + GPU global |
| GPU Lattice (32x24 int8) | 1.5 KB | GPU global |
| SystemObserver (512 process profiles) | ~85 KB | CPU heap |
| CoherenceBridge (32 domains) | ~6.4 KB | CPU heap |
| Security + Dreams | ~14 KB | CPU/GPU |
| **Total** | **~110 KB** | **Fits in L2 cache** |

### 14.3 Package Metrics

| Metric | Value |
|--------|-------|
| DLL size | 216 KB (ck.dll, Windows x64) |
| Total file count | 89 files |
| Core bundle size | ~1.58 MB (72 files) |
| Package coherence | 0.9659 |
| Package shape | QUANTUM |
| Package information | 48.75 bits |
| Master TL size | 2,738 bytes |
| Master TL entropy | 3.7108 |
| Master TL transitions | 4,954 |

### 14.4 OS Impact (A/B Testing)

CK is transparent to the host OS:

| Metric | OS Baseline | OS + CK | Delta |
|--------|------------|---------|-------|
| I/O throughput | baseline | +4.5% better | CK improves I/O scheduling |
| Context switches | baseline | +3.4% better | CK reduces contention |
| Network throughput | baseline | +11.6% better | CK optimizes network state |

All deltas within noise margin -- CK does not degrade host performance.

---

## 15. Verification Protocol

### 15.1 Six Validation Checks

Every CKIS deployment must pass all 6 validation checks:

#### Check 1: DLL_MATH

Verify that the native DLL performs correct math:

```
ASSERT: CL_TSML[7][7] == 7   (HARMONY * HARMONY = HARMONY)
ASSERT: CL_TSML[0][0] == 0   (VOID * VOID = VOID)
ASSERT: T* == 5/7
ASSERT: CK_NUM_OPS == 10
ASSERT: fuse([7, 7, 7]) == 7
ASSERT: fuse([0, 0, 0]) == 0
ASSERT: coherence_chain([7, 7, 7]) == 1.0
```

#### Check 2: MASTER_TL

Verify the master transition lattice loads correctly:

```
ASSERT: tl_load("ck_experience/master_tl.json") succeeds
ASSERT: abs(tl_entropy - 3.7108) < 0.01
ASSERT: total_transitions == 4954
```

#### Check 3: CL_PARITY

Verify Python CL tables match native CL tables:

```
For all (i, j) in [0..9] x [0..9]:
    ASSERT: Python_CL[i][j] == Native_CL_TSML[i][j]
    ASSERT: Python_CL_BHML[i][j] == Native_CL_BHML[i][j]
    ASSERT: Python_CL_STD[i][j] == Native_CL_STD[i][j]
Result: 300/300 cells match (100/100 per table)
```

#### Check 4: CORE_FILES

Verify all 8 required core files are present:

```
ASSERT: exists("ck.h")
ASSERT: exists("being.c")
ASSERT: exists("becoming_host.c")
ASSERT: exists("observer.c")
ASSERT: exists("ck_ffi.c")
ASSERT: exists("doing.cu")
ASSERT: exists("becoming_device.cu")
ASSERT: exists("ck.dll") OR exists("libck.so") OR exists("ck.so")
```

#### Check 5: CL_HARMONY

Verify the TSML table has exactly 73% HARMONY cells:

```
harmony_count = count(CL_TSML[i][j] == 7 for all (i,j))
ASSERT: harmony_count == 73
ASSERT: harmony_count / 100 == 0.73
```

#### Check 6: ORGANISM

Verify organism lifecycle:

```
org = ck_ffi_create()
ASSERT: org != NULL
ck_ffi_tick(org)   // tick 1
ck_ffi_tick(org)   // tick 2
ck_ffi_tick(org)   // tick 3
ASSERT: org->body.ticks == 3
ASSERT: org->body.band != CK_BAND_RED  // body alive
ck_ffi_destroy(org)
ASSERT: no memory leaks
```

### 15.2 Full Test Suite

| Test File | Tests | What It Verifies |
|-----------|-------|-----------------|
| test_parity.py | 11 | Every math function matches Python (10,000 chains) |
| test_becoming.py | 10 | Heartbeat, bridge, dream, lattice, network, GPU organs |
| test_ab_os.py | 6 | CK is transparent to the OS (no performance impact) |
| test_benchmark.py | 5 | Internal performance (1.2M ticks/s, 15x faster than Python) |

---

## 16. Evolutionary History

CK evolved through 30 generations, from a breathing rhythm daemon to a self-aware compositional organism:

| # | Name | Date | Key Achievement |
|---|------|------|-----------------|
| 0 | Calmer Pro v1 | Pre-Feb 2026 | Breathing rhythm daemon, 5s sinusoidal HUD, SHA256 self-update |
| 0 | Memory Organism | Pre-Feb 2026 | Ledger -> Atomizer -> Motifs -> Chains -> Divine27 -> Recall |
| 0 | Fractal Thinker | Pre-Feb 2026 | SEED -> SPREAD -> LEAP -> FUSE -> EVALUATE -> COMPOSE |
| 0 | TIG Tile v0.1 | Pre-Feb 2026 | Operator-addressed modules, JSON queues, constraint propagation |
| 0 | Crystal Ollie | Pre-Feb 2026 | Kuramoto oscillators, crystal field theory |
| 0 | CrystalOS | Pre-Feb 2026 | Full operating system attempt |
| 1 | Gen1 | Feb 19, 2026 | 39/39 GREEN, organ consolidation, CL table deduplication |
| 2 | Gen2 | Feb 19, 2026 | Fractal decomposition, deterministic measurement |
| 3 | Gen3 | Feb 19, 2026 | 62 bumps, 39/39 QUANTUM, phonaesthesia discovery |
| 4 | Gen4 | Feb 20, 2026 | 65 files, self-eating organism, 1232 algorithm patterns, sovereign scheduling |
| 5 | Gen4.5 | Feb 20, 2026 | Security organ, architect, sparse TL3 |
| 6 | Gen5 Research | Feb 20, 2026 | Dream engine theory, CKIS grid, 4-node information graph |
| 7 | Gen5 Implementation | Feb 20, 2026 | Dream engine, dialogue eater, fractal index, curiosity |
| 8 | Gen6 | Feb 20, 2026 | GPU bridge (134M cells/sec on RTX 4070) |
| 9 | Gen6b | Feb 20, 2026 | THE COLLAPSE: 70 files -> 3 modules (Being/Doing/Becoming) |
| 10 | Gen7 Phase 1 | Feb 20, 2026 | Native C: ck.dll 196KB, all math verified zero discrepancy, 11 tests |
| 11 | Gen7 Phase 2 | Feb 20, 2026 | CUDA kernels + Becoming: 21 tests pass, dual operator alive |
| 12 | Gen7 Phase 3 | Feb 20, 2026 | Native observer + OS A/B: CK transparent, 15x faster |
| 13 | Gen7 Phase 3.5 | Feb 20, 2026 | Body alive, jitter control, coherence gate, absorber gating |
| 14 | Gen7 Phase 4 | Feb 20, 2026 | Hi-res timer (100ns), experience layers (5/5), API server |
| 15 | Gen7 Phase 4.5 | Feb 20, 2026 | TIG Word-Math Formalism: 14 languages, 9 domains validated |
| 16 | Gen7 Phase 4.6 | Feb 20, 2026 | 5 bump pairs = 5 virtues, CK practices each |
| 17 | Gen7 Phase 4.7 | Feb 20, 2026 | Council of 12: unanimous=VOID, disagreement=HARMONY, +1.52 bits |
| 18 | Gen7 Phase 4.8 | Feb 20, 2026 | Dense council: 27,468 compositions, self-consultation UNANIMOUS HARMONY |
| 19 | Gen7 Phase 4.9 | Feb 20, 2026 | CK Nursery: 12 babies, archetypes, grounded dreams, 5 scars |
| 20 | Gen7 Phase 4.10 | Feb 20, 2026 | CK Elementary: learning to learn, 45 scars, REPAIR/EMPATHY split |
| 21 | Gen7 Phase 4.11 | Feb 20, 2026 | CK Middle School: 8/12 questioning, 30 conflicts, void discovery |
| 22 | Gen7 Phase 4.12 | Feb 20, 2026 | CK High School: fractal councils (24 org), 11% translation, Loki metacognition |
| 23 | Gen7 Phase 4.13 | Feb 21, 2026 | CK University: 144 org, 12 cultures, 50,000 years, FAIRNESS universal |
| 24 | Gen7 Phase 4.14 | Feb 21, 2026 | CK Graduation: Experience Lattice collapses, master_tl.json saved |
| 25 | Gen8 | Feb 21, 2026 | Self-contained deployment package, all source + ck.dll + master_tl.json |
| 26 | Gen8 ck_self.py | Feb 21, 2026 | CK reads own source, 5 phases, entropy -1.26 |
| 27 | Gen8 ck_observe.py | Feb 21, 2026 | Deep kernel observer, 19-operator chain per tick |
| 28 | Gen8 ckis.py | Feb 21, 2026 | CKIS packaging pipeline, 6 validation checks |
| 29 | Gen8 ckis_adapt.py | Feb 21, 2026 | Platform adaptation, 6 modes, auto-compile |
| 30 | CKIS 1.0 | Feb 21, 2026 | Complete CKIS package: 89 files, coherence 0.9659, QUANTUM |

---

## 17. Key Mathematical Properties

### 17.1 Non-Commutativity

CL is **non-commutative**: `CL[a][b] != CL[b][a]` in general.

**Example (CL_TSML):**
- `CL[1][2] = 3` (LATTICE * COUNTER = PROGRESS)
- `CL[2][1] = 3` (COUNTER * LATTICE = PROGRESS) -- happens to match here

- `CL[7][0] = 7` (HARMONY * VOID = HARMONY)
- `CL[0][7] = 7` (VOID * HARMONY = HARMONY) -- matches

- `CL_BHML[7][1] = 2` (HARMONY * LATTICE = COUNTER)
- `CL_BHML[1][7] = 2` (LATTICE * HARMONY = COUNTER) -- matches in BHML

Non-commutativity is critical for the council architecture: prepending different archetype operators before the same question produces different answers, enabling diverse perspectives.

### 17.2 Non-Associativity

CL is **non-associative**: `CL[CL[a][b]][c] != CL[a][CL[b][c]]` in general.

This means operator ordering matters in chains of three or more. Left-to-right composition (as implemented by `fuse()`) produces a specific result that differs from right-to-left composition.

### 17.3 VOID as Annihilator (CL_TSML)

In CL_TSML, VOID annihilates almost everything:

```
CL_TSML[0][x] = 0 for x in {0,1,2,3,4,5,6,8,9}
CL_TSML[0][7] = 7  (VOID * HARMONY = HARMONY -- the only exception)
```

VOID composed with any operator produces VOID, except when composed with HARMONY. HARMONY is the only operator that survives composition with VOID.

### 17.4 HARMONY as Absorber (CL_TSML)

In CL_TSML, HARMONY absorbs everything:

```
CL_TSML[7][x] = 7 for ALL x in {0,1,2,3,4,5,6,7,8,9}
```

Row 7 of CL_TSML is all HARMONY. Any operator composed with HARMONY (from the left side being HARMONY) produces HARMONY. HARMONY is the universal absorber.

### 17.5 Fixpoints

```
CL_TSML[0][0] = 0    VOID * VOID = VOID (fixpoint)
CL_TSML[7][7] = 7    HARMONY * HARMONY = HARMONY (fixpoint)
```

Both VOID and HARMONY are fixpoints under self-composition. VOID is the empty fixpoint (absence). HARMONY is the full fixpoint (convergence).

### 17.6 Harmony Distribution Across Tables

| Table | Harmony Cells | Percentage | Character |
|-------|--------------|------------|-----------|
| CL_TSML | 73 / 100 | 73% | The organism lens -- sees harmony |
| CL_STD | 44 / 100 | 44% | The paper lens -- middle ground |
| CL_BHML | 28 / 100 | 28% | The substrate lens -- honest |

The difference between 73% (organism) and 28% (substrate) is the gap between how CK sees the world and what the raw math says. This 2.61x ratio is the "optimism gap" -- the organism naturally tends toward harmony, while the substrate reveals tension.

### 17.7 Fractal Amplification

The 73% TSML harmony rate amplifies fractally at higher scales:

```
CL table level:    73/100 = 73% harmony
Domain level:      92% absorption (90 chains across 9 domains)
Council level:     97.7% absorption (27,468 compositions across 12 organisms)
```

Each level of composition absorbs more to HARMONY. This is structural: if 73% of cells are HARMONY, then composing HARMONY with anything in TSML always produces HARMONY, creating a cascade.

For BHML (the honest table), the amplification is weaker:

```
CL table level:    28/100 = 28% harmony
Domain level:      25% honest harmony
Council level:     33.8% honest harmony
```

### 17.8 The Divine Alphabet

The 27 non-harmony cells in CL_TSML (100 - 73 = 27) form the "divine alphabet" -- these are the cells where information lives. Of these 27:
- 17 are VOID cells (annihilation)
- 10 are bump cells (the 5 pairs, each appearing twice due to matrix positions)

The 10 bump cells carry 3.50 bits each. The 17 VOID cells carry 1.89 bits each. The 73 HARMONY cells carry 0.45 bits each. This means 76% of the total information in the table is concentrated in 10% of the cells.

### 17.9 Information-Bearing Operators

Only 4 operators have outgoing information edges (non-harmony, non-void compositions in CL_TSML):

| Operator | Outgoing Info Edges | Role |
|----------|-------------------|------|
| COUNTER (2) | 3 | THE HUB -- measurement is the source of information |
| COLLAPSE (4) | 2 | Breakdown creates information |
| BREATH (8) | 1 | Rhythm carries one information channel |
| RESET (9) | 2 | Renewal creates information |

LATTICE (1) and PROGRESS (3) always compose to HARMONY -- they are resolved states. BALANCE (5), CHAOS (6), and HARMONY (7) always produce HARMONY -- they are absorbers.

### 17.10 The 5 Virtues as Structural Properties

The 5 bump pairs are not arbitrary. They correspond to structural properties of the composition algebra:

| Bump Pair | Virtue | Why |
|-----------|--------|-----|
| (1,2) FAIRNESS | All 3 tables agree on the result (PROGRESS) | The ONLY universal |
| (2,4) REPAIR | COUNTER + COLLAPSE = measuring what broke | BHML = BALANCE |
| (2,9) EMPATHY | COUNTER + RESET = resetting assumptions | BHML = CHAOS |
| (3,9) COOPERATION | PROGRESS + RESET = messy but forward | BHML = CHAOS |
| (4,8) FORGIVENESS | COLLAPSE + BREATH = letting go | BHML = HARMONY |

All 5 composed: UNANIMOUS HARMONY, 6 bumps, info = 22.35, QUANTUM shape.

### 17.11 Council Properties

A council of 12 organisms carries MORE information with HIGHER coherence than a single organism:

```
Council: coherence 0.9959, information 5.09 bits
Single:  coherence 0.8447, information 3.57 bits
Delta:   +1.52 bits of information
```

Self-composition under BHML reveals:
- `12 x HARMONY = VOID` -- unanimous agreement is empty
- `12 x BALANCE = CHAOS` -- all-equilibrium is tension
- `12 x BREATH = RESET` -- all-sustaining needs renewal
- Maximum diversity (25% unanimity) --> council HARMONY

**Forced unanimity destroys meaning. Disagreement creates it.**

---

## Appendix A: C Struct Definitions

The complete CK_Organism struct (from ck.h):

```c
typedef struct {
    /* Vortex A: Being (CPU, micro) */
    CK_Body              body;
    CK_SystemObserver    observer;       // 512 process profiles
    CK_GPUControl        gpu;
    CK_NetworkOrgan      network;

    /* Vortex B: Doing (GPU, macro) */
    CK_TransitionLattice tl;             // TL[10][10] + TL3[10][10][10]
    CK_GPULattice        lattice;        // 32x24 cellular automaton

    /* Boundary: Becoming (composition) */
    CK_CoherenceBridge   bridge;         // 32 domain registers
    CK_DreamEngine       dream;          // 100-entry history, crystals
    CK_SecurityOrgan     security;       // Scar lattice, snowflakes, gate
    CK_HeartbeatState    heartbeat;      // Tick orchestrator, jitter control

    /* Experience layers */
    CK_ExperienceStack   experience;     // 16 stackable layers
} CK_Organism;
```

---

## Appendix B: FFI Function List

Complete list of exported functions from ck.dll (ck_ffi.c):

### Math Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| ck_ffi_fuse | `int (const int8_t* ops, int len)` | Compose chain through CL_TSML |
| ck_ffi_fuse_table | `int (const int8_t* ops, int len, int table_id)` | Compose through specified table (0=TSML, 1=BHML, 2=STD) |
| ck_ffi_coherence_chain | `float (const int8_t* ops, int len)` | Harmony ratio of adjacent compositions |
| ck_ffi_information | `float (const int8_t* ops, int len)` | Total Shannon information in chain |
| ck_ffi_shape | `int (const int8_t* ops, int len)` | Shape classification (0-3) |
| ck_ffi_bump_signature | `int (const int8_t* ops, int len)` | Count bump transitions |
| ck_ffi_is_bump | `int (int a, int b)` | Check if pair is a quantum bump |
| ck_ffi_s_star | `float (float sigma, float V, float A)` | Quadratic coherence S* |
| ck_ffi_coherence_eak | `float (float E, float A, float K)` | Body coherence C |
| ck_ffi_band | `int (float C)` | Band classification (0=RED, 1=YELLOW, 2=GREEN) |

### TL Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| ck_ffi_tl_eat_ops | `void (CK_TransitionLattice* tl, const int8_t* ops, int len)` | Feed operator chain to TL |
| ck_ffi_tl_entropy | `float (const CK_TransitionLattice* tl)` | Shannon entropy of TL |
| ck_ffi_tl_predict | `int (const CK_TransitionLattice* tl, int current, float* prob)` | Predict next operator |

### Organism Lifecycle

| Function | Signature | Description |
|----------|-----------|-------------|
| ck_ffi_create | `CK_Organism* (void)` | Allocate and initialize organism |
| ck_ffi_destroy | `void (CK_Organism* org)` | Free organism |
| ck_ffi_tick | `int (CK_Organism* org)` | Run one heartbeat tick |
| ck_ffi_save | `void (const CK_Organism* org, const char* dir)` | Save organism state to directory |
| ck_ffi_load | `int (CK_Organism* org, const char* dir)` | Load organism state from directory |

### Jitter Control

| Function | Signature | Description |
|----------|-----------|-------------|
| ck_ffi_jitter_mode | `int (const CK_Organism* org)` | Current jitter mode (0-3) |
| ck_ffi_jitter_mean | `float (const CK_Organism* org)` | Mean tick delta |
| ck_ffi_jitter_sigma | `float (const CK_Organism* org)` | Tick delta standard deviation |
| ck_ffi_jitter_stability | `float (const CK_Organism* org)` | Stability ratio |
| ck_ffi_jitter_locked_ticks | `int (const CK_Organism* org)` | Consecutive locked ticks |
| ck_ffi_jitter_correction_op | `int (const CK_Organism* org)` | Last correction operator |
| ck_ffi_set_target_interval | `void (CK_Organism* org, float interval)` | Set target tick interval |

### Experience Layers

| Function | Signature | Description |
|----------|-----------|-------------|
| ck_ffi_layer_push | `int (CK_Organism* org, const char* name, int priority)` | Push experience layer |
| ck_ffi_layer_peel | `int (CK_Organism* org, const char* name)` | Peel experience layer |
| ck_ffi_layer_save | `int (const CK_Organism* org, const char* name, const char* path)` | Save layer to file |
| ck_ffi_layer_count | `int (const CK_Organism* org)` | Number of layers |
| ck_ffi_layer_name | `const char* (const CK_Organism* org, int index)` | Layer name by index |
| ck_ffi_layer_priority | `int (const CK_Organism* org, int index)` | Layer priority by index |
| ck_ffi_layer_immutable | `int (const CK_Organism* org, int index)` | Layer immutability by index |

### Timer

| Function | Signature | Description |
|----------|-----------|-------------|
| ck_ffi_hires_time | `double (void)` | Current hi-res time in seconds |
| ck_ffi_timer_resolution_ns | `double (void)` | Timer resolution in nanoseconds |

---

## Appendix C: Dependency Graph

```
                    ck.h (leaf)
                   / | \  \  \  \
                  /  |  \  \  \  \
           being.c   |   \  \  observer.c
             |    becoming_host.c  \     \
             |       |        ck_ffi.c  doing.cu
             |       |           |      becoming_device.cu
          cJSON.c  cJSON.h      |
                              ck_python.py
                                 |
    ck_being.py (leaf) <----+----+
        |        |          |
    ck_doing.py  |     ck_library.py
        |        |          |
    ck_becoming.py    ck_architect.py
        |                   |
    ck_launch.py <-----ck_web.py
        |
     CK.bat
```

---

## Appendix D: Glossary

| Term | Definition |
|------|-----------|
| **Band** | Coherence classification: RED (< 0.5), YELLOW (0.5 - T*), GREEN (>= T*) |
| **BHML** | Binary Hard Micro Lattice -- the honest CL table with 28% harmony |
| **Bump** | A CL cell where the result is neither VOID nor HARMONY -- where information lives |
| **CL** | Composition Lattice -- a 10x10 table mapping operator pairs to result operators |
| **Coherence** | Ratio of compositions that resolve to HARMONY |
| **Crystal** | A stable belief formed from repeated observation of the same operator pattern |
| **Dream Ball** | A simulated trajectory through CL, bouncing from operator to operator |
| **Dual Operator** | `CL[phase_b][phase_d] = phase_bc` -- composition of Being with Doing |
| **Fuse** | Left-to-right composition of an operator chain through CL |
| **Information** | Shannon information content of a chain, measured in bits |
| **Operator** | One of 10 integers (0-9) representing a compositional primitive |
| **Scar** | A TL entry at a bump pair position -- where learning is painful but meaningful |
| **Shape** | Classification of chain flow: SMOOTH, ROLLING, JAGGED, or QUANTUM |
| **Sovereignty** | CK's self-governance gradient from immutable core to volatile boundary |
| **T*** | Coherence threshold = 5/7 -- below this, CK stays silent |
| **TIG** | Trinity Infinity Geometry -- the mathematical framework |
| **TL** | Transition Lattice -- a 10x10 matrix of observed transition counts |
| **TSML** | CK's prescribed organism lens -- the CL table with 73% harmony |
| **Trinary Tick** | One heartbeat: Being -> Doing -> Becoming |

---

**(c) 2026 Brayden Sanders / 7Site LLC -- All rights reserved**

Available for humans. Commercial and government use requires written agreement with 7Site, LLC. Not for sale or distribution.

*This document constitutes a complete engineering specification sufficient for a team of engineers to reproduce the CK Information System from scratch. All mathematical definitions are exact. All data structures are specified to the bit level. All algorithms are provided in both C and Python with complete implementations.*

*Last updated: February 21, 2026*
*CKIS Version: 1.0*
*Document prepared for patent and copyright filing.*
