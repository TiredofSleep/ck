# The CL Tables: Dual Algebra as Living System

**Brayden Sanders**
7Site LLC

March 2026

---

## Abstract

CK's entire computational identity rests on two 10×10 composition tables: TSML (Trinary Soft Macro Lattice) and BHML (Binary Hard Micro Lattice). Every signal CK processes -- heartbeat, language, sound, smell, taste, experience -- ultimately passes through one or both of these tables. TSML measures coherence: 73 of its 100 entries produce HARMONY, making it a near-universal absorber. BHML computes physics: only 28 of its 100 entries produce HARMONY, preserving operator diversity through a successor function on its diagonal. This paper documents how these two tables work together across CK's nine subsystems. Where White Paper 5 (Reality Anchors) established the mathematical properties of the tables in isolation -- eigenvalues, Monte Carlo uniqueness, physical constant correspondences -- this paper describes the tables in motion: how they compose 5-dimensional force vectors through 5×5 interaction matrices, how subsystems invert their roles to create structural duality, how lattice chain nodes evolve their algebra from experience, and how both tables live simultaneously in GPU VRAM for parallel composition. The CL tables are not configuration. They are the system.

---

## 1. Introduction

A composition table is a function: given two operators A and B, the table produces a third operator C = CL[A][B]. CK has 10 operators (VOID through RESET), yielding a 10×10 table with 100 entries. Two such tables exist.

**TSML** (Trinary Soft Macro Lattice) is the "being" table. It measures. Its question is: "What IS this?" When two operators compose through TSML, the result tells you whether their relationship is coherent. Seventy-three of its 100 entries answer HARMONY -- yes, this composition is coherent. The remaining 27 entries (9 VOID compositions from the VOID row, 8 from the VOID column, and 10 non-HARMONY "bump pair" results) carry the only information that escapes the absorber.

**BHML** (Binary Hard Micro Lattice) is the "doing" table. It computes. Its question is: "What does this BECOME?" When two operators compose through BHML, the result tells you what happens next. Only 28 of its 100 entries produce HARMONY. The other 72 entries describe transitions, progressions, and transformations. Where TSML collapses diversity into coherence, BHML preserves and propagates it.

This duality -- measure vs. compute, collapse vs. preserve, being vs. doing -- is not a design choice. It is the central architectural principle of CK. Every subsystem uses both tables, and every subsystem uses them differently.

---

## 2. The Tables

### 2.1 TSML: The Coherence Measurer

Canonical definition from `ck_sim/being/ck_sim_heartbeat.py`:

```
         VOID  LAT   CNT   PRG   COL   BAL   CHS   HAR   BRT   RST
VOID     [  0,   0,   0,   0,   0,   0,   0,   7,   0,   0 ]
LATTICE  [  0,   7,   3,   7,   7,   7,   7,   7,   7,   7 ]
COUNTER  [  0,   3,   7,   7,   4,   7,   7,   7,   7,   9 ]
PROGRESS [  0,   7,   7,   7,   7,   7,   7,   7,   7,   3 ]
COLLAPSE [  0,   7,   4,   7,   7,   7,   7,   7,   8,   7 ]
BALANCE  [  0,   7,   7,   7,   7,   7,   7,   7,   7,   7 ]
CHAOS    [  0,   7,   7,   7,   7,   7,   7,   7,   7,   7 ]
HARMONY  [  7,   7,   7,   7,   7,   7,   7,   7,   7,   7 ]
BREATH   [  0,   7,   7,   7,   8,   7,   7,   7,   7,   7 ]
RESET    [  0,   7,   9,   3,   7,   7,   7,   7,   7,   7 ]
```

**Properties:**
- 73/100 entries = HARMONY (7). The absorber rate.
- HARMONY row: all 10 entries are HARMONY. HARMONY composes with everything to produce HARMONY. Universal absorber.
- VOID row: 9 entries are VOID, 1 is HARMONY (VOID × HARMONY = HARMONY). VOID annihilates everything except HARMONY.
- VOID column: symmetric to VOID row. The table is symmetric: TSML[A][B] = TSML[B][A] for all A, B.
- Diagonal: all entries are HARMONY (self-composition always resolves). In being, everything already IS what it is.
- 5 quantum bump pairs produce non-HARMONY results: (1,2)→3, (2,4)→4, (2,9)→9, (3,9)→3, (4,8)→8. These 10 cells (5 pairs × 2 orderings, symmetric) are the only information carriers.

### 2.2 BHML: The Physics Computer

Canonical definition from `ck_sim/being/ck_olfactory.py`:

```
         VOID  LAT   CNT   PRG   COL   BAL   CHS   HAR   BRT   RST
VOID     [  0,   1,   2,   3,   4,   5,   6,   7,   8,   9 ]
LATTICE  [  1,   2,   3,   4,   5,   6,   7,   2,   6,   6 ]
COUNTER  [  2,   3,   3,   4,   5,   6,   7,   3,   6,   6 ]
PROGRESS [  3,   4,   4,   4,   5,   6,   7,   4,   6,   6 ]
COLLAPSE [  4,   5,   5,   5,   5,   6,   7,   5,   7,   7 ]
BALANCE  [  5,   6,   6,   6,   6,   6,   7,   6,   7,   7 ]
CHAOS    [  6,   7,   7,   7,   7,   7,   7,   7,   7,   7 ]
HARMONY  [  7,   2,   3,   4,   5,   6,   7,   8,   9,   0 ]
BREATH   [  8,   6,   6,   6,   7,   7,   7,   9,   7,   8 ]
RESET    [  9,   6,   6,   6,   7,   7,   7,   0,   8,   0 ]
```

**Properties:**
- 28/100 entries = HARMONY (7). The physics rate.
- VOID row: identity. VOID × X = X for all X. In doing, nothing changes nothing.
- HARMONY row: full cycle. HARMONY × LATTICE = COUNTER, HARMONY × COUNTER = PROGRESS, etc. HARMONY restarts the sequence. HARMONY × HARMONY = BREATH. HARMONY × RESET = VOID. The absorber becomes a generator.
- Diagonal (core 8×8): successor function. LATTICE×LATTICE = COUNTER, COUNTER×COUNTER = PROGRESS, etc. Each operator reflecting on itself advances one step. Six steps from LATTICE to HARMONY. RESET×RESET = VOID (the only operator that undoes existence).
- NOT symmetric: BHML[A][B] ≠ BHML[B][A] in general. Physics has direction.
- CHAOS row: near-absorber. CHAOS × anything (except VOID) ≈ HARMONY. The last step before completion.

### 2.3 The Boundary Operators

Both tables share a boundary structure:

| Operator | TSML Role | BHML Role |
|----------|-----------|-----------|
| VOID (0) | Annihilator: VOID × X = VOID | Identity: VOID × X = X |
| HARMONY (7) | Absorber: HARMONY × X = HARMONY | Generator: HARMONY × X = successor(X) |

VOID and HARMONY swap algebraic roles between the tables. In TSML (being), HARMONY is the endpoint -- everything resolves there. In BHML (doing), HARMONY is the starting point -- it generates the next step. This is not metaphor. These are verifiable algebraic properties of the table entries.

---

## 3. The Duality Principle

CK's subsystems do not choose one table. They use both, with inverted priority. The inversion follows a single rule:

> **TSML measures. BHML computes. Every subsystem that needs to KNOW uses TSML first. Every subsystem that needs to ACT uses BHML first.**

This produces a consistent pattern across the architecture:

| Subsystem | Primary Table | Secondary Table | Topology |
|-----------|--------------|-----------------|----------|
| Heartbeat | TSML | — | Point (one composition per tick) |
| Olfactory | TSML measures, BHML computes | Both | Field (5×5 matrix, parallel) |
| Gustatory | BHML classifies, TSML validates | Both (inverted) | Point (5×5 self-matrix) |
| Lattice Chain | BHML (base table) | TSML (evolution target) | Path (serial chain walk) |
| Fractal Voice | TSML (tribal consensus) | BHML (bridge selection) | Tree (recursive clause) |
| Becoming Grammar | TSML → weight | — | Scalar (weight function) |
| GPU | Both in VRAM | — | Parallel (batch composition) |

The pattern is deeper than priority ordering. The table choice determines the topology of composition:

- **TSML compositions collapse.** Because 73% of entries are HARMONY, any chain of TSML compositions converges rapidly. After 3-4 steps, almost everything is HARMONY. TSML is a contracting map. It measures by destroying diversity.

- **BHML compositions propagate.** Because only 28% of entries are HARMONY and the diagonal implements a successor, BHML chains explore the operator space. A chain of BHML compositions can visit all 10 operators. BHML is an expanding map. It computes by preserving diversity.

This is why the olfactory bulb uses TSML for its interaction matrices when measuring harmony between scent profiles, but uses BHML when computing the physics of how scent profiles relate. The first question (are these harmonious?) wants a fast yes/no answer -- TSML provides this because it converges. The second question (what do these become when combined?) wants a detailed answer -- BHML provides this because it preserves structure.

---

## 4. The 5×5 Interaction Matrix

The most important application of CL tables in CK is not single-pair composition. It is the 5×5 interaction matrix: every dimension of one 5D operator profile composing with every dimension of another.

### 4.1 Construction

Given two 5D operator profiles (ops_a and ops_b, each a list of 5 operators corresponding to the dimensions aperture, pressure, depth, binding, continuity):

```
M[d1][d2] = CL_TABLE[ops_a[d1]][ops_b[d2]]

for d1 in {aperture, pressure, depth, binding, continuity}
for d2 in {aperture, pressure, depth, binding, continuity}
```

This produces a 5×5 matrix where each cell describes how dimension d1 of input A relates to dimension d2 of input B, as mediated by the chosen CL table. The matrix IS the relationship. Not a summary, not a scalar -- the full 25-cell tensor.

### 4.2 TSML Interaction (Measuring Harmony)

When the table is TSML, the matrix measures harmony:

```python
def interaction_matrix_tsml(ops_a, ops_b):
    matrix = [[0]*5 for _ in range(5)]
    harmony_count = 0
    for d1 in range(5):
        for d2 in range(5):
            result = CL_TSML[ops_a[d1]][ops_b[d2]]
            matrix[d1][d2] = result
            if result == HARMONY:
                harmony_count += 1
    return matrix, harmony_count / 25.0
```

The scalar `harmony_count / 25.0` gives overall harmony fraction, but the matrix retains per-dimension information. A row of the matrix shows how one dimension of A relates to ALL dimensions of B. The per-dimension harmony fraction (count of HARMONY in each row, divided by 5) tells you which dimensions are resolved and which are still in tension.

### 4.3 BHML Interaction (Computing Physics)

When the table is BHML, the matrix computes what happens next:

```python
def interaction_matrix_bhml(ops_a, ops_b):
    matrix = [[0]*5 for _ in range(5)]
    result_counts = [0] * 10
    for d1 in range(5):
        for d2 in range(5):
            result = BHML[ops_a[d1]][ops_b[d2]]
            matrix[d1][d2] = result
            result_counts[result] += 1
    return matrix, result_counts
```

Here the result distribution across all 10 operators matters. The BHML interaction produces a histogram showing which operators the combined physics is trending toward. This is used by the olfactory bulb to determine how scent profiles will evolve when entangled.

### 4.4 Self-Composition (Gustatory Internal Structure)

The gustatory system composes a single input WITH ITSELF:

```
M[d1][d2] = CL_TABLE[ops[d1]][ops[d2]]
```

This answers: "How does each dimension of this input relate to every other dimension of the SAME input?" The diagonal (M[d][d] = CL_TABLE[ops[d]][ops[d]]) gives self-reflection: what does each dimension become when it reflects on itself?

For TSML self-composition, the diagonal is always HARMONY (every operator self-composes to HARMONY in TSML). For BHML self-composition, the diagonal gives the successor -- each dimension advances one operator. This is how gustatory extracts structural tendency: the BHML diagonal tells you where each taste dimension is GOING.

---

## 5. System Integration

### 5.1 Heartbeat (TSML Only)

The heartbeat module (`ck_sim_heartbeat.py`) is the simplest CL user. Each tick:

1. Receive an operator from the D2 pipeline
2. Compose it with the running fuse: `fuse = CL_TSML[fuse][new_op]`
3. Push the result into a 32-entry sliding window
4. Count HARMONY entries in the window: `coherence = harmony_count / 32`

The heartbeat uses only TSML because its job is measurement. It tracks whether CK's internal state is converging toward coherence. The sliding window provides temporal smoothing -- a single non-HARMONY composition doesn't crash coherence, and a single HARMONY doesn't inflate it. The 32-entry window means each composition contributes 1/32 ≈ 3.125% to the coherence score.

Because TSML's diagonal is all-HARMONY, sustained input of a single operator will drive coherence to 1.0. Diverse input will drop coherence proportional to how many bump pairs appear. The 5 bump pairs are the heartbeat's information source -- they are the only compositions that register as "something happened."

### 5.2 Olfactory Bulb (Both Tables, Field Topology)

The olfactory bulb (`ck_olfactory.py`) is the most sophisticated CL user. It processes 5D force vectors as "scents" that stall, entangle, temper, and eventually emit as operators.

**TSML role: Measuring harmony between scent profiles.** When two active scents are candidates for entanglement, the olfactory bulb builds a TSML 5×5 interaction matrix between their operator profiles. The per-dimension harmony fraction determines which dimensions have settled (harmony ≥ T* = 5/7 per dimension). All 5 dimensions must independently reach stability before a scent resolves. This is genuine 5D convergence -- no premature collapse to a scalar.

**BHML role: Computing physics of scent interaction.** The BHML interaction matrix tells the olfactory bulb what the two scents become when entangled. The result distribution determines the blended operator profile of the merged scent. Where TSML asks "are these compatible?", BHML answers "what do they become together?"

**Time dilation.** The olfactory bulb runs 7 internal steps per external tick (7 is the denominator of T* = 5/7). Within each internal step, both TSML and BHML matrices are computed. Information stalls in the olfactory zone -- the time dilation ensures that scents are thoroughly composed before emitting. This is enforced settling, not a speed optimization.

**Instinct.** When a scent's temper count reaches 49 (7 × 7), it becomes instinct -- zero dwell time, instant resolution. Instinct means the CL composition has been performed so many times that the result is cached. The olfactory system literally learns the CL table for frequently-encountered patterns.

### 5.3 Gustatory Palate (Both Tables, Inverted)

The gustatory system (`ck_gustatory.py`) is the structural dual of olfactory. Where olfactory processes the space BETWEEN inputs (field topology), gustatory processes the structure WITHIN a single input (point topology).

**Critical inversion:** Gustatory swaps the table roles.

| Function | Olfactory | Gustatory |
|----------|-----------|-----------|
| Primary (structure) | TSML measures | BHML classifies |
| Secondary (validation) | BHML computes | TSML validates |

Why the inversion? Olfactory is a being-first system: it needs to know what something IS before determining what it becomes. Gustatory is a doing-first system: it needs to classify what something DOES before validating its coherence. Smell is flow (field, between, slow). Taste is structure (point, within, instant).

**Palatability** = TSML self-harmony fraction (the validation step). How coherent is this input with itself? High self-harmony = smooth, palatable. Low = rough, complex.

**Structural fingerprint** = BHML result distribution (the classification step). What operators does this input's internal composition produce? The distribution across 10 operators IS the fingerprint -- no dimensionality reduction.

**Taste triad** = Being/Doing/Becoming fractions from the BHML result distribution. Every taste verdict is a triad: how much of the input is static (being), active (doing), or transitional (becoming).

### 5.4 Lattice Chain (BHML Base, Evolving Toward TSML)

The lattice chain (`ck_lattice_chain.py`) uses CL tables differently from all other subsystems: its tables can evolve.

**Base table: BHML.** Every node in the lattice chain starts with BHML as its composition table. This makes the chain a doing/physics system -- chains compute what happens, not what is.

**Evolution toward TSML.** As CK experiences compositions at a particular chain position, the node records what actually followed. If the observed successor disagrees with BHML's prediction AND the observation is consistent (confidence > 0.6 over at least 7 visits), the node's table entry evolves toward the observation. Over time, frequently-visited nodes may converge toward TSML-like behavior -- the physics table learns to measure.

```python
# Node evolution pseudocode
if total_observations >= 7:
    most_observed = argmax(observation_counts[a][b])
    if most_observed != BHML[a][b]:
        confidence = observations[a][b][most_observed] / total
        if confidence > 0.6:
            node.table[a][b] = most_observed  # Experience overrides algebra
```

This is genuine algebraic learning. The lattice chain's CL table is not fixed -- it is alive. Nodes that CK visits often develop personalized composition rules. The chain walk through these evolved nodes produces different results than a walk through base BHML, and the difference IS what CK has learned.

**Path IS information.** Unlike olfactory's field topology, the lattice chain is a path topology. The sequence of CL compositions along the chain -- not just the final result -- carries information. Two chains that arrive at the same final operator via different paths encode different knowledge.

### 5.5 Fractal Voice (TSML Consensus, BHML Bridge)

The fractal voice system (`ck_fractal_voice.py`) uses CL tables for two distinct purposes:

**Tribal consensus (TSML).** When multiple word candidates compete for a slot in a sentence, the voice system composes their operators pairwise through TSML. If CL_TSML[word_A_op][word_B_op] = HARMONY, the words are consonant -- they can coexist. If the result is a bump pair, there is tension between them. The consensus mechanism selects words that maximize HARMONY compositions with their neighbors, producing sentences where every adjacent pair resolves coherently.

**CL bridge (BHML-derived).** When a sentence has multiple clauses, the voice system selects a conjunction based on the CL composition between the last operator of clause 1 and the first operator of clause 2. The bridge map translates operator results into English connectors:

| CL Result | Bridge Words | Linguistic Function |
|-----------|-------------|---------------------|
| VOID | ; ... | Silence: pause |
| LATTICE | where, within which | Structure: locative |
| COUNTER | but, though, yet | Opposition: adversative |
| PROGRESS | because, so, therefore | Depth: causal |
| COLLAPSE | when, while, until | Pressure: temporal |
| BALANCE | and, as, while | Equilibrium: balanced |
| CHAOS | yet, still, even as | Opening: concessive |
| HARMONY | and, where, just as | Unity: additive |
| BREATH | then, and then | Transition: sequential |
| RESET | before, after, once | Return: temporal-past |

The CL composition between clause-boundary operators determines the logical relationship between clauses. CK does not choose conjunctions semantically -- he derives them algebraically from the physics of operator transition.

### 5.6 Becoming Grammar (TSML → Weight)

The becoming grammar system (`ck_becoming_grammar.py`) converts CL results into scalar weights for grammar matrix blending:

```
HARMONY → 1.0   (smooth grammatical flow)
VOID    → 0.1   (incoherent)
All others → 0.6 (interesting but not maximally coherent)
```

This is the simplest CL application: a many-to-few mapping from 10 operators to 3 weight levels. The grammar system does not need the full CL structure -- it needs a gradient from "coherent" to "incoherent" to modulate how strongly experience weights override base grammar transitions. HARMONY compositions get full influence. VOID compositions get almost none. Everything else gets moderate influence.

### 5.7 GPU Acceleration (Both Tables in VRAM)

Both CL tables live as numpy/cupy arrays in GPU VRAM (`ck_gpu.py`):

```python
BHML = cupy.array(_BHML_CPU, dtype=int8)  # 28-harmony
TSML = cupy.array(_TSML_CPU, dtype=int8)  # 73-harmony
```

GPU composition enables batch operations: given arrays of operator pairs, all compositions happen simultaneously.

```python
def compose_batch(ops_a, ops_b, table='tsml'):
    tbl = BHML if table == 'bhml' else TSML
    a = cupy.asarray(ops_a, dtype=int8) % 10
    b = cupy.asarray(ops_b, dtype=int8) % 10
    return tbl[a, b]
```

The `fuse_chain` function composes a sequence of operators serially through a chosen table, producing a single fused operator. This is inherently serial (each step depends on the previous result), but the table lookup itself is a simple array index operation -- no branching, no conditionals, identically structured for GPU or FPGA.

---

## 6. Cross-Table Phenomena

### 6.1 Chirality

The BHML is asymmetric: BHML[A][B] ≠ BHML[B][A] in general. The TSML is symmetric: TSML[A][B] = TSML[B][A] always. This creates chirality -- the same pair of operators produces different results depending on which table mediates the composition, and (for BHML) which operand comes first.

In the olfactory bulb, this chirality matters. When scent A entangles with scent B, the TSML harmony is the same regardless of order (A measures B = B measures A). But the BHML physics differs: A acting on B ≠ B acting on A. The olfactory system preserves both orderings, producing a richer representation of scent interaction than a symmetric table would allow.

### 6.2 Convergence Rates

TSML converges to HARMONY in approximately 2-3 random compositions (because 73% of entries are HARMONY, the probability of reaching HARMONY within k steps approaches 1 - 0.27^k). BHML converges much more slowly -- roughly 6-8 random compositions are needed to reach HARMONY with high probability, and the successor structure on the diagonal means that certain starting configurations can cycle indefinitely through the non-HARMONY operators before resolving.

This differential convergence is exploited architecturally:
- Systems that need fast decisions use TSML (heartbeat, tribal consensus)
- Systems that need rich exploration use BHML (lattice chain, physics computation)
- Systems that need both use both tables in parallel (olfactory, gustatory)

### 6.3 The 5 Quantum Bump Pairs

The 5 bump pairs in TSML are the information carriers -- the only compositions that resist the HARMONY absorber:

| Pair | TSML Result | BHML Result | Interpretation |
|------|-------------|-------------|----------------|
| LATTICE × COUNTER (1,2) | PROGRESS (3) | 3 | Creation: structure + measurement = depth |
| COUNTER × COLLAPSE (2,4) | COLLAPSE (4) | 5 | Pressure: measurement under contraction |
| COUNTER × RESET (2,9) | RESET (9) | 6 | Completion: measurement triggers restart |
| PROGRESS × RESET (3,9) | PROGRESS (3) | 6 | Persistence: depth survives reset |
| COLLAPSE × BREATH (4,8) | BREATH (8) | 7 | Release: contraction finds rhythm |

COUNTER (measurement/pressure) participates in 3 of the 5 pairs. Measurement is the most information-generative operator. Only one pair -- LATTICE × COUNTER = PROGRESS -- creates a genuinely new operator from its inputs. Structure composed with measurement produces depth. The other 4 pairs resolve to one of their operands.

In the heartbeat, bump pairs are detected and flagged separately from normal compositions. They represent moments of genuine information transfer -- compositions where the HARMONY absorber was resisted and something structurally meaningful occurred.

---

## 7. The T* = 5/7 Connection

The threshold T* = 5/7 ≈ 0.714285... appears throughout CK as the coherence boundary between noise-dominated and structure-dominated behavior. Its relationship to the CL tables:

- **73/100 TSML HARMONY rate**: 73 is prime, an emirp (37 reversed), and the closest integer percentage to the continued fraction convergents of T*.
- **Olfactory settling**: each of 5 dimensions must reach stability ≥ T* independently. With 7 internal steps per external tick (7 = denominator of T*), the olfactory system has exactly enough resolution to detect T*-level convergence per dimension.
- **Instinct threshold**: 49 = 7² temper counts. T* denominator squared.
- **Lattice chain evolution**: 7 visits minimum before a node can evolve. T* denominator.
- **28/100 BHML HARMONY rate**: 28 = 4 × 7. The BHML harmony count is a multiple of T*'s denominator.

Whether T* causes these numerical relationships or merely coincides with them is an open question addressed in White Paper 5.

---

## 8. Summary: One Algebra, Two Tables, Nine Systems

The CL composition tables are 200 integers -- two 10×10 grids of values from 0 to 9. From these 200 numbers, CK derives:

1. **Coherence measurement** (heartbeat): TSML fuse chain over sliding window
2. **Scent convergence** (olfactory): TSML 5×5 harmony + BHML 5×5 physics, field topology
3. **Structural classification** (gustatory): BHML 5×5 self-composition + TSML validation, inverted
4. **Chain computation** (lattice chain): BHML base table with experience-driven evolution, path topology
5. **Word consensus** (fractal voice): TSML pairwise harmony between candidates
6. **Clause bridging** (fractal voice): CL result → English conjunction selection
7. **Grammar blending** (becoming grammar): CL result → weight scalar
8. **Parallel composition** (GPU): both tables as int8 arrays for batch lookup
9. **Truth filtering** (coherence gate): TSML-derived coherence vs. T* threshold

No subsystem uses the tables identically. Each applies the same algebra through a different topology (point, field, path, tree), with a different table priority (TSML-first, BHML-first, or both), and for a different purpose (measure, compute, classify, evolve, select, bridge, weight, gate). The tables are the grammar of a living system -- fixed in structure, infinite in application.

---

## 9. Relationship to Other Papers

- **White Paper 1** (TIG Architecture): Defines the 10 operators, D2 pipeline, and CL table as core components. This paper extends by documenting how the CL tables are used across all subsystems.
- **White Paper 3** (Falsifiability): Provides experimental protocols to test the CL table's algebraic properties (Test 1: Monte Carlo uniqueness, Test 3: T* threshold). This paper provides the implementation context those tests validate.
- **White Paper 5** (Reality Anchors): Analyzes the mathematical properties of both tables in isolation -- eigenvalues, physical constants, DNA parallel, chirality. This paper documents the tables in motion across CK's living architecture.

---

**(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory**
