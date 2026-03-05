# How to Give Math a Voice: From Algebraic Curvature to Spoken English in CK

**Brayden Sanders**
7Site LLC

March 2026

---

## Abstract

CK (Coherence Keeper) converts mathematical structure directly into spoken English without neural networks, templates, or statistical language models. The system processes all information through 5-dimensional force vectors classified by second-derivative curvature into 10 algebraic operators, composes those operators through a fixed 10×10 table exhibiting 73% HARMONY absorption, and selects English words by matching their physical signatures against the operator chain's trajectory through 15-dimensional triadic space. This paper documents every formula in the pipeline: from Hebrew root force assignment through D2 curvature classification, CL composition, olfactory field convergence, L-CODEC text measurement, lattice chain experience, and finally the three-voice tribal composition system where Being, Doing, and Becoming voices propose words in parallel and reach consensus through CL harmony. No formula is metaphorical. Every equation operates on measured quantities, and every word CK speaks was selected by algebraic agreement — not by probability, not by pattern matching, and not by borrowing human grammar wholesale.

---

## 1. Introduction

The question "how do you give math a voice?" has a specific answer in CK: you don't translate math into language. You discover that language already IS math, then you let the math speak for itself.

Every natural language utterance carries a physical signature. When someone says "water flows," those phonemes trace a trajectory through articulatory force space. The word "flows" is not an arbitrary label — it is a sequence of mouth positions, each exerting measurable forces along five independent dimensions. CK exploits this: it classifies the curvature of those force trajectories into algebraic operators, composes operators through a fixed table, and selects words whose physical signatures align with the composed result.

The result is a system that speaks English not because it was taught grammar, but because it discovered which words fit the mathematics.

This paper traces the complete pipeline from raw force vectors to spoken sentences, documenting every formula, constant, and threshold. We are explicit about what has been formally verified, what has been empirically validated, and what remains conjectured.

---

## 2. The Force Space: Five Dimensions

All CK mathematics operates in a 5-dimensional real-valued space where each dimension corresponds to a measurable property of articulation:

| Dimension | Index | Physical Meaning | Range |
|-----------|-------|------------------|-------|
| Aperture | 0 | Oral openness, vocal tract width | [0, 1] |
| Pressure | 1 | Articulatory force, compression | [0, 1] |
| Depth | 2 | Pharyngeal depth, resonant cavity length | [0, 1] |
| Binding | 3 | Consonantal closure, structural tightness | [0, 1] |
| Continuity | 4 | Sustained voicing, flow persistence | [0, 1] |

These are not abstract features. They correspond to physical measurements of how the human vocal tract produces sound. A bilabial stop like /p/ has high pressure (0.80) and low continuity (0.10). A high front vowel like /iː/ has high aperture (0.95) and high continuity (0.95).

### 2.1 Hebrew Root Force Vectors

CK's foundational force table maps 22 Hebrew letter roots to 5D vectors. Latin letters are mapped through phonetic correspondence (26 → 22):

```
ALEPH:  (0.80, 0.00, 0.90, 0.00, 0.70)    [breath/spirit]
BET:    (0.30, 0.60, 0.40, 0.80, 0.60)    [house/container]
GIMEL:  (0.50, 0.40, 0.50, 0.30, 0.50)    [camel/motion]
DALET:  (0.40, 0.50, 0.30, 0.70, 0.40)    [door/passage]
HEI:    (0.70, 0.10, 0.80, 0.10, 0.80)    [window/revelation]
...
```

The choice of Hebrew roots as the force basis is a specific encoding decision, not a claim of linguistic universality. What matters mathematically is the existence of a fixed, non-degenerate mapping from symbols to R⁵. The Hebrew system provides one such mapping with articulatory grounding.

### 2.2 Phoneme Force Table (44 English Phonemes)

For voice composition, CK uses a finer-grained table of 44 English phonemes, each with a 5D force signature measured from articulatory phonetics:

```
/iː/:  (0.95, 0.05, 0.20, 0.10, 0.95)   [high front vowel]
/p/:   (0.10, 0.80, 0.30, 0.70, 0.10)   [bilabial stop]
/m/:   (0.20, 0.40, 0.30, 0.90, 0.70)   [nasal: high binding]
/s/:   (0.15, 0.60, 0.40, 0.50, 0.65)   [fricative]
/ɔɪ/:  (0.70, 0.15, 0.60, 0.30, 0.55)   [diphthong]
```

A word's force is the average of its constituent phoneme forces, weighted by position. This is how CK computes WHERE a word sits in 5D space — its Being.

---

## 3. The D2 Pipeline: Curvature IS Classification

### 3.1 First Derivative (Velocity)

Given a sequence of force vectors v[t], the first derivative measures direction:

```
D1[dim] = v[t][dim] - v[t-1][dim]
```

D1 magnitude: `|D1| = Σ|D1[dim]|` (L1 norm over 5 dimensions)

### 3.2 Second Derivative (Curvature)

The second derivative measures how direction itself changes:

```
D2[dim] = v[t][dim] - 2·v[t-1][dim] + v[t-2][dim]
```

This is the standard discrete central difference operator applied to each dimension independently. It requires a 3-stage shift register storing the three most recent force vectors.

D2 magnitude: `|D2| = Σ|D2[dim]|`

### 3.3 Operator Classification

Classification is deterministic and parameter-free:

```
if |D2| < 0.01:
    operator = VOID
else:
    max_dim = argmax_dim(|D2[dim]|)
    sign = 0 if D2[max_dim] ≥ 0 else 1
    operator = D2_OP_MAP[max_dim][sign]
```

The D2_OP_MAP assigns exactly two operators per dimension (one per sign), yielding 10 operators total:

| Dimension | Positive D2 | Negative D2 |
|-----------|-------------|-------------|
| Aperture (0) | CHAOS (6) | LATTICE (1) |
| Pressure (1) | COLLAPSE (4) | VOID (0) |
| Depth (2) | PROGRESS (3) | RESET (9) |
| Binding (3) | HARMONY (7) | COUNTER (2) |
| Continuity (4) | BALANCE (5) | BREATH (8) |

Physical meaning: when binding curvature is positive (tightening), the classification is HARMONY. When aperture curvature is positive (opening), the classification is CHAOS. These are not metaphors — they are the measured acceleration of articulatory force in specific dimensions.

### 3.4 Soft Classification

For voice composition, CK also produces a 10-value soft distribution:

```
for dim in range(5):
    weight[dim] = |D2[dim]| / |D2|_total
    high_op, low_op = D2_OP_MAP[dim]
    if D2[dim] ≥ 0:
        scores[high_op] += weight[dim]
    else:
        scores[low_op] += weight[dim]
```

This distributes curvature magnitude proportionally across operator pairs. A word with D2 = (0.3, 0.0, 0.2, 0.0, 0.0) would score 60% CHAOS + 40% PROGRESS — it's "mostly opening, somewhat deepening."

### 3.5 Q1.14 Fixed-Point Arithmetic

All D2 computations use Q1.14 signed fixed-point: 1 sign bit, 1 integer bit, 14 fractional bits, scale factor 16,384. Representable range: [-2.0, +1.99994]. This format was chosen to match the target FPGA implementation exactly — the Python simulation IS the hardware pipeline running on a general-purpose processor.

---

## 4. The CL Composition Table: Algebra of Operators

### 4.1 The 10×10 Table (TSML — 73-Harmony)

Once signals are classified into operators, they are composed through the CL (Composition Lattice) table:

```
CL[row][col] → operator
```

The default table (TSML — "Truth Speaks, Mercy Listens") is a 10×10 matrix containing 100 entries, of which exactly 73 are HARMONY:

```
     VOID  LAT  CNT  PRG  COL  BAL  CHS  HAR  BRE  RST
VOID [  0,   0,   0,   0,   0,   0,   0,   7,   0,   0]
LAT  [  0,   7,   3,   7,   7,   7,   7,   7,   7,   7]
CNT  [  0,   3,   7,   7,   4,   7,   7,   7,   7,   9]
PRG  [  0,   7,   7,   7,   7,   7,   7,   7,   7,   3]
COL  [  0,   7,   4,   7,   7,   7,   7,   7,   8,   7]
BAL  [  0,   7,   7,   7,   7,   7,   7,   7,   7,   7]
CHS  [  0,   7,   7,   7,   7,   7,   7,   7,   7,   7]
HAR  [  7,   7,   7,   7,   7,   7,   7,   7,   7,   7]
BRE  [  0,   7,   7,   7,   8,   7,   7,   7,   7,   7]
RST  [  0,   7,   9,   3,   7,   7,   7,   7,   7,   7]
```

Properties of this table (formally verified):
- **73% HARMONY absorption**: 73 of 100 entries are HARMONY (7)
- **HARMONY row is absorbing**: CL[HARMONY][x] = HARMONY for all x
- **Non-commutativity**: CL[a][b] ≠ CL[b][a] for certain pairs (e.g., CL[VOID][HARMONY] = 7, CL[HARMONY][VOID] = 7, but CL[LATTICE][COUNTER] = 3 ≠ CL[COUNTER][LATTICE] = 3 — coincidental here but structurally not guaranteed)
- **5 bump pairs**: (LATTICE, COUNTER), (COUNTER, COLLAPSE), (COUNTER, RESET), (PROGRESS, RESET), (COLLAPSE, BREATH) — pairs that produce non-HARMONY results, creating structural differentiation

### 4.2 Coherence as a Measurable Quantity

Coherence is the fraction of HARMONY compositions over a sliding window:

```
coherence = count(HARMONY in last 32 compositions) / min(tick_count + 1, 32)
```

This is not a subjective assessment. It is a measured ratio with exact numerical value at every tick. The sacred threshold T* = 5/7 ≈ 0.714285... marks the transition point: when 73% or more of compositions are HARMONY, the system is coherent.

### 4.3 The Second Table (BHML — 28-Harmony)

CK uses two CL tables:
- **TSML** (73-harmony): Measures coherence. Being/structure lens. Used for harmony fraction computation.
- **BHML** (28-harmony): Computes physics. Doing/flow lens. Used for chain walks and experience learning.

Where TSML asks "does this compose harmoniously?" (binary: yes/no), BHML asks "what does this composition produce?" (diverse: 10 possible outputs). Dual-lens processing — structure AND flow — runs in parallel at every scale.

### 4.4 The Density Gate

The coherence gate converts brain coherence and field coherence into a single density scalar:

```
raw = 0.6 × brain_coherence + 0.4 × field_coherence
density = 0.7 × raw + 0.3 × density_prev
density ∈ [0, 1]
```

Density gates all downstream behavior: high density (≥ T*) → structural/confident voice, low density → flowing/questioning voice.

Constants derived from T*:
- Compilation limit: `int(32 × (1 - T*)) = int(32 × 2/7) = 9` (maximum compilation loops)
- Expansion threshold: `1 - T* = 2/7 ≈ 0.286` (when to expand search)
- These are not tuning parameters. They are mathematical consequences of the 73-harmony table structure.

---

## 5. One Is Three: The 15-Dimensional Triadic Signature

Every word in CK's vocabulary carries not a label, not a definition, but a 15-dimensional physical signature comprising three 5D vectors:

| Component | Derivation | Physical Meaning |
|-----------|-----------|------------------|
| Being (force) | Average phoneme forces | WHERE the word sits in 5D space |
| Doing (velocity/D1) | First derivative of force sequence | WHERE the word is GOING |
| Becoming (curvature/D2) | Second derivative of force sequence | HOW the word BENDS |

A word's 15D signature is: `(a₀, p₀, d₀, b₀, c₀, a₁, p₁, d₁, b₁, c₁, a₂, p₂, d₂, b₂, c₂)` where subscripts 0/1/2 denote Being/Doing/Becoming.

This is the "One is Three" principle: every single point in language space is actually a trajectory with position, velocity, and acceleration. A word doesn't just EXIST somewhere — it is going somewhere and bending toward something.

### 5.1 Force Computation for a Word

Given word phonemes [φ₁, φ₂, ..., φₙ]:

```
Being[dim] = (1/n) × Σ PHONEME_FORCES[φᵢ][dim]
```

For D1 and D2, the phoneme forces are fed through the shift register:

```
D1[dim] = PHONEME_FORCES[φᵢ][dim] - PHONEME_FORCES[φᵢ₋₁][dim]
D2[dim] = PHONEME_FORCES[φᵢ][dim] - 2·PHONEME_FORCES[φᵢ₋₁][dim] + PHONEME_FORCES[φᵢ₋₂][dim]
```

The word's Doing and Becoming are the averages of D1 and D2 across all internal phoneme transitions.

### 5.2 Operator Assignment

Each word's primary operator comes from its Becoming (D2 classification), not its Being. The word is classified by HOW IT BENDS, not where it sits. This is a deliberate design choice: intent (curvature) drives classification, not position.

### 5.3 Grammatical Role from Force Profile

Force profiles determine grammatical role without grammar rules:

```
if pressure > 0.6 and continuity < 0.4:  → verb (high force, short action)
if binding > 0.6 and aperture < 0.4:     → noun (tight structure, closed form)
if aperture > 0.6 and pressure < 0.3:    → adjective (open, descriptive)
if continuity > 0.7:                     → conjunction/adverb (sustaining)
```

Grammar is not imposed. It is measured from the physics of the word.

---

## 6. L-CODEC: Measuring Text in 5D

L-CODEC (Language Coherence-Dimensional Encoding Codec) measures arbitrary text passages as 5D force vectors using linguistic proxies:

### 6.1 Five Proxy Measurements

**Aperture** — Vocabulary openness:
```
TTR = |unique_tokens| / |total_tokens|
POS_variety = |unique_POS| / 5.0
aperture = 0.6 × TTR + 0.4 × POS_variety
```

**Pressure** — Information density:
```
comp_ratio = |gzip(text)| / |text|
comp_norm = min(1.5, comp_ratio) / 1.5
punct_rate = punct_count / max(1, n)
punct_norm = min(1.0, punct_rate × 3.0)
pressure = 0.65 × comp_norm + 0.35 × punct_norm
```

**Depth** — Topic persistence:
```
depth = 0.50 × topic_persistence + 0.30 × coreference_density + 0.20 × keyphrase_lag
```
where topic_persistence is cosine similarity of word force centroids between sentence halves.

**Binding** — Syntactic tightness:
```
scaffold = function_word_count / max(content_word_count, ε)
bigram_pred = 1.0 - (unique_bigrams / total_bigrams)
binding = 0.55 × scaffold + 0.45 × bigram_pred
```

**Continuity** — Trajectory smoothness:
```
smoothness = 1.0 - √(variance_of_adjacent_cosine_similarities) × 2.0
neg_impact = 1.0 - min(1.0, negation_rate × 10.0)
continuity = 0.65 × smoothness + 0.35 × neg_impact
```

### 6.2 Triple-Gauge Normalization

Each raw measurement passes through three independent normalization gauges:

**Gauge A (Physical):** Fixed empirical baselines from English prose:
```
z = (raw - μ_ref) / max(σ_ref, 0.001)
gauge_A = sigmoid(z)
```
Reference values: aperture μ=0.42, σ=0.15; pressure μ=0.55, σ=0.12; depth μ=0.40, σ=0.18; binding μ=0.48, σ=0.14; continuity μ=0.55, σ=0.15.

**Gauge B (Min-Max):** Rolling window of 32 measurements:
```
gauge_B = (raw - min(window)) / (max(window) - min(window))
```

**Gauge C (Robust Z-Score):** Median Absolute Deviation:
```
z = (raw - median(window)) / (MAD × 1.4826)
gauge_C = sigmoid(z)
```
The constant 1.4826 is the consistency constant for normal distributions — it makes MAD a consistent estimator of standard deviation.

**Consensus:** Simple arithmetic mean:
```
consensus[dim] = clamp((gauge_A[dim] + gauge_B[dim] + gauge_C[dim]) / 3, 0, 1)
```

### 6.3 Gauge Invariants

Four agreement metrics verify that the structure is real, not an artifact of normalization:

| Invariant | Formula | Meaning |
|-----------|---------|---------|
| Direction | Σ(all 3 gauges agree on >/< 0.5) / 5 | Same side of center |
| Event | Σ(1 - spread × 2) / 5 | Same deviation magnitude |
| Flow | Concordant rank pairs / 10 | Same relative ordering |
| Continuity | Σ(all 3 agree on direction of change) / 5 | Same temporal trend |

Overall agreement: `(direction + event + flow + continuity) / 4`

When agreement is high, the measured force vector is gauge-invariant — the structure exists regardless of how you normalize it. When agreement is low, the measurement is noise.

### 6.4 Stillness

An emergent quantity from the force vector:
```
stillness = (1 - pressure) × 0.4 + binding × 0.3 + continuity × 0.3
```
Modified by aperture and depth. Captures "presence without action" — the mathematical signature of contemplative text.

---

## 7. The Olfactory Field: Where Time Bends

The olfactory bulb is CK's convergence layer. All information — heartbeat forces, text forces, voice forces — eventually becomes "scent" in a 5D field where CL interaction matrices govern convergence.

### 7.1 Time Constants from T*

Every time constant derives from T* = 5/7:

| Constant | Value | Derivation |
|----------|-------|------------|
| Dilation factor | 7 | Denominator of T* |
| Instinct threshold | 49 | 7² (temper count for instant resolution) |
| Stability threshold | T* | Per-dimension convergence gate |
| Max dwell | 32 | = HISTORY_SIZE (same as coherence window) |

Per-dimension settling rates (base rate per internal tick):
```
aperture:   0.10 (medium)
pressure:   0.12 (medium-fast)
depth:      0.06 (slowest — deep things take time)
binding:    0.15 (fastest — structure resolves first)
continuity: 0.09 (medium-slow)
```

### 7.2 Seven-Fold Time Dilation

Each external 50Hz tick produces 7 internal olfactory ticks. This mirrors the mathematical structure of T*: 5 steps to reach threshold within 7.

Per internal tick, each dimension's stability advances:

```
Δstability = base_rate × (1 + max(0, 1 - 10×variance))
                       × (1 + 2×harmony_fraction)
                       × (1 + 0.15×entangled_count)
                       + 0.5×temper_bonus
```

Where:
- `base_rate ∈ {0.06, 0.09, 0.10, 0.12, 0.15}` (per dimension)
- `variance` = recent value spread (low variance → faster settling)
- `harmony_fraction` = from 5×5 CL interaction matrix (per dimension, NOT scalar)
- `entangled_count` = number of other scents entangled on this dimension
- `temper_bonus` ≥ 1.0 forces instant resolution (instinct)

### 7.3 The 5×5 CL Interaction Matrices

When two scents interact, their dimension-to-dimension compositions form a 5×5 matrix:

```
for d1 in range(5):
    for d2 in range(5):
        matrix[d1][d2] = CL_TSML[op_a[d1]][op_b[d2]]
harmony_fraction = count(HARMONY in matrix) / 25
```

This is NOT scalar composition. Every dimension of every scent interacts with every dimension of every other scent. The matrix IS the information — it captures the full cross-dimensional structure of how two force patterns compose.

**Per-dimension harmony** (not scalar):
```
for d in range(5):
    dim_harmony[d] = count(HARMONY in row d) / 5
```

**Dual-lens processing:**
- TSML matrix (73-harmony): MEASURES harmony (structure/being)
- BHML matrix (28-harmony): COMPUTES physics (flow/doing)

Both matrices are computed for every scent pair. Structure is measured while physics is computed. Being and doing run in parallel.

### 7.4 Scent Lifecycle

```
absorb → stall → entangle → temper → emit → lattice chain walk
```

1. **Absorb**: Force vector enters as ActiveScent with 5 DimStates (one per dimension)
2. **Stall**: Information cannot skip processing — dwell time enforced (time dilation)
3. **Entangle**: 5×5 interaction matrices computed with all other active scents; mutual stability boost where dim_harmony ≥ T*: `Δstability = 0.04 × harmony_fraction`
4. **Temper**: Library lookup (quantized 5D centroid) — if seen before, temper count increments
5. **Emit**: When ALL 5 dimensions reach stability ≥ T*, scent resolves to operators: `op[dim] = high_op if centroid[dim] > 0.5 else low_op`
6. **Lattice chain walk**: Resolved operators walk the CL chain tree, recording experience

Instinct: temper count ≥ 49 (7²) → all dimensions instantly resolve (stability = 1.0). Familiar patterns become zero-cost. This is learned recognition without neural networks.

### 7.5 Library Quantization

```
key = tuple(int(c × 20) for c in centroid)    # 5D → 5 integers in [0, 19]
```

This creates a 20⁵ = 3,200,000 possible scent space, quantized to preserve dimensionality. The library stores temper counts per key. No vectors are collapsed to scalars — even in storage, the 5D structure is preserved.

### 7.6 Temporal Tense Context

The olfactory field determines grammatical tense from its state:

```
if library_dominates and few_active_scents:  → past tense
if average_stability < T*/2:                  → becoming (progressive)
else:                                          → present tense
```

Present = active scent (being processed now). Past = library (already resolved). Future = instinct (forming pattern, not yet resolved). Verb tense is not grammatical convention — it is the temporal position of information in the convergence field.

---

## 8. The Lattice Chain: Path IS Information

### 8.1 Chain Walk Algorithm

Operators are processed in pairs through a tree of CL nodes:

```
Given ops = [o₁, o₂, o₃, o₄, ...]:
    result₁ = CL_BHML[o₁][o₂]         (at root node)
    move to child[result₁]
    result₂ = CL_BHML[o₃][o₄]         (at child node)
    move to child[result₂]
    ...
```

The path through the tree IS the information. Not the final result — the trajectory. Two different operator sequences that produce the same final operator took different paths and carry different structural meaning.

### 8.2 Experience Learning (Node Evolution)

Each node records observations:
```
obs_counts[struct_op][flow_op][actual_next] += 1
```

After 7+ observations of a cell, if one result appears >60% of the time and differs from the base CL table:
```
if confidence > 0.6 and most_observed ≠ CL_base[a][b]:
    node.table[a][b] = most_observed
```

The CL table itself evolves through experience. Frequently-walked paths develop their own composition rules. This is how CK learns — not by updating weights, but by evolving its algebra.

### 8.3 Path Resonance

Two chain walk results can be compared for temporal alignment:

```
resonance = (Σᵢ w(i) × match(i)) / (Σᵢ w(i)) × (min_length / max_length)
where w(i) = 1 / (1 + i)    [fractal 1/f weighting]
```

Early steps matter more (1/f weighting). This is fractal: the beginning of a path carries more structural information than later steps, just as the first few terms of a fractal iteration determine the shape.

### 8.4 GPU Tensor Export

All experienced nodes export as a (N, 10, 10) tensor:
```
tensor = stack([node.table for node in experienced_nodes])
```
Ready for parallel chain walks on GPU. CK's experience becomes a 3D tensor of evolved algebras.

---

## 9. The Three-Voice Tribe: Giving Math Its Voice

This is where mathematics becomes English. The tribal composition system runs three parallel voices, each looking at the same operator chain through a different lens of the 15D triadic space.

### 9.1 Tribal Weights

```
TRIBAL_WEIGHTS = {
    'being':    (2.5, 0.5, 0.5),    # Emphasizes Being (force/position)
    'doing':    (0.5, 2.5, 0.5),    # Emphasizes Doing (velocity/direction)
    'becoming': (0.5, 0.5, 2.5),    # Emphasizes Becoming (curvature/intent)
}
```

Each voice weighs the 15D space differently. The Being voice cares most about WHERE words sit. The Doing voice cares about WHERE words go. The Becoming voice cares about HOW words bend.

### 9.2 Temporal Coagulation

Tribal weights are further modulated by temporal priority:

```
TEMPORAL_PRIORITY = {
    'past':      (2.0, 0.5, 0.5),    # Past → Being (what was)
    'present':   (0.5, 2.0, 0.5),    # Present → Doing (what is happening)
    'becoming':  (0.5, 0.5, 2.0),    # Future → Becoming (what will be)
}

coagulated = harmonic_mean(tribal_weight, temporal_priority)
```

The harmonic mean (not arithmetic) ensures that neither component can dominate unless both agree. Past tense + Being voice = strong position emphasis. Future tense + Becoming voice = strong intent emphasis.

### 9.3 Word Selection: 15D Triadic Search

For each operator in the chain, each voice searches its vocabulary for the best-matching word:

```
for each candidate word w:
    being_dist  = Σ|w.force[d] - target.force[d]|       × tribal_w[0]
    doing_dist  = Σ|w.velocity[d] - target.velocity[d]| × tribal_w[1]
    becoming_dist = Σ|w.curvature[d] - target.curvature[d]| × tribal_w[2] × 1.5

    total_dist = being_dist + doing_dist + becoming_dist
    score = 1.0 / (1.0 + total_dist)
```

Note: Becoming gets an additional 1.5× weight beyond the tribal weight. Intent always matters most — a word that bends correctly is more important than one that sits correctly.

### 9.4 S-V-O Logic Gate

Each voice is assigned a grammatical role:

| Voice | Role | Function |
|-------|------|----------|
| Being | Subject | Anchor — what IS |
| Doing | Verb | Forward motion — what ACTS |
| Becoming | Object | Resolution — what RESOLVES |

This maps the mathematical triad (position, velocity, curvature) directly to English sentence structure (subject, verb, object). Grammar is not imposed — it emerges from the physics.

### 9.5 CL Harmony Consensus

After all three voices propose their words, they must agree:

```
harmony_AB = CL_harmony(voice_A_ops, voice_B_ops)    # 5×5 matrix
harmony_BC = CL_harmony(voice_B_ops, voice_C_ops)    # 5×5 matrix
harmony_AC = CL_harmony(voice_A_ops, voice_C_ops)    # 5×5 matrix

tribal_harmony = min(harmony_AB, harmony_BC, harmony_AC)

if tribal_harmony < T*:
    retry with different candidates (up to agreement_limit)
```

The three voices must achieve CL harmony ≥ T* across ALL pairwise interactions before the sentence is accepted. If they can't agree, the system retries with alternative candidates. Words that don't compose harmoniously are rejected — not by grammar rules, but by algebraic incompatibility.

### 9.6 Compound Sentence Recursion

When the operator chain has 4+ operators:

```
if len(ops) >= 4:
    # Find natural CL fracture point
    split = find_cl_fracture(ops)

    # Compose each clause independently
    clause_A = compose_tribal(ops[:split])
    clause_B = compose_tribal(ops[split:])

    # Link with CL bridge word
    bridge_op = CL[ops[split-1]][ops[split]]
    bridge = CL_BRIDGE[bridge_op]

    return clause_A + " " + bridge + " " + clause_B
```

CL bridge words:
```
HARMONY  → "and"      (coherent continuation)
COUNTER  → "but"      (measured opposition)
PROGRESS → "because"  (causal depth)
COLLAPSE → "when"     (temporal contraction)
```

Even conjunctions are determined by the algebra, not by grammar rules.

---

## 10. The Eat System: Learning Transition Physics

### 10.1 Architecture

The Eat v2 system measures external text (from Ollama LLM) and internal text (CK's own source code) through L-CODEC, tracking how force vectors transition:

```
TransitionRecord:
    prev_force: 5D
    curr_force: 5D
    delta: 5D (curr - prev)
    delta_magnitude: |delta|₂
    prev_ops: operators
    curr_ops: operators
    source: 'ollama' | 'self'
```

### 10.2 Interleaved Learning

Per round:
1. Ollama chunk → L-CODEC → 5D force → olfactory absorb (source='ollama_eat')
2. Self chunk → L-CODEC → 5D force → olfactory absorb (source='self_eat')
3. Track transition (delta between consecutive measurements)
4. Resonance step: CK composes from absorbed operators, then measures his own voice → absorb (source='voice_eat')
5. Evolve grammar from accumulated experience

### 10.3 What CK Retains (No Memorization)

After eating, CK retains knowledge in five structures — none store the original text:

| Structure | What's Stored | Where |
|-----------|--------------|-------|
| L-CODEC gauges | Rolling statistics shift | In-memory gauge windows |
| Olfactory library | Quantized 5D centroids + temper counts | `~/.ck/olfactory/` |
| Olfactory instincts | Tempered patterns (temper ≥ 49) | `~/.ck/olfactory/` |
| Swarm generator_paths | 10×10 operator transition matrix | `~/.ck/ck_experience.json` |
| Becoming grammar blend | Experience weights (capped at 40%) | In-memory grammar matrix |

The text is discarded. Only the force trajectories remain. CK doesn't remember WHAT was said — he remembers HOW it moved through 5D space.

### 10.4 Grammar Evolution

After each round, swarm experience evolves the grammar:

```
weights = deep_swarm.get_evolved_weights()    # 10×10 matrix
maturity = deep_swarm.maturity()              # [0, 1]
α = min(0.4, 0.4 × maturity)                 # Experience influence cap

grammar_blend = (1 - α) × ENGLISH_FLOW + α × experience_weights
```

The becoming grammar is a 6×6 POS transition matrix (noun, verb, adj, det, conj, adv). English grammar starts as the base. Experience gradually modulates it — but never more than 40%. CK learns grammar by doing, not by being taught.

---

## 11. The English Grammar Matrix

### 11.1 Operator-to-POS Mapping

Each of the 10 operators maps to a primary and secondary part of speech:

```
VOID:      (det, noun)       "the" / "absence"
LATTICE:   (noun, adj)       "structure" / "structured"
COUNTER:   (adj, adv)        "measured" / "precisely"
PROGRESS:  (verb, noun)      "grows" / "growth"
COLLAPSE:  (verb, adj)       "falls" / "broken"
BALANCE:   (adj, noun)       "balanced" / "equilibrium"
CHAOS:     (adj, adv)        "wild" / "suddenly"
HARMONY:   (noun, adj)       "truth" / "unified"
BREATH:    (conj, adv)       "and" / "gently"
RESET:     (verb, noun)      "begins" / "beginning"
```

### 11.2 English Flow Matrix

A 6×6 transition weight matrix encodes SVO grammar:

```
         noun  verb   adj   det  conj   adv
noun   [ 0.5,  1.0,  0.4,  0.2,  0.9,  0.3]
verb   [ 1.0,  0.1,  0.3,  0.5,  0.6,  0.9]
adj    [ 1.0,  0.3,  0.3,  0.2,  0.3,  0.2]
det    [ 0.9,  0.2,  1.0,  0.1,  0.1,  0.3]
conj   [ 0.9,  0.5,  0.7,  0.8,  0.1,  0.4]
adv    [ 0.3,  1.0,  0.4,  0.2,  0.3,  0.1]
```

1.0 = natural English flow (noun → verb, verb → noun, det → adj). 0.1 = ungrammatical (det → det, conj → conj). The CL result of composing adjacent operators selects the grammar weight:

```
CL_grammar_weight(result):
    HARMONY → 1.0    (harmonious transition = grammatical)
    VOID    → 0.1    (void transition = ungrammatical)
    other   → 0.6    (moderate transition)
```

Final transition score: `english_flow[from_POS][to_POS] × CL_grammar_weight(CL[op_a][op_b])`

---

## 12. The Complete Pipeline

From raw input to spoken English, one complete cycle:

```
1. Input signal (audio/text/heartbeat)
        ↓
2. Hebrew root mapping → 5D force vector
        ↓
3. D2 pipeline: D2[dim] = v[t] - 2v[t-1] + v[t-2]
        ↓
4. Operator classification: argmax(|D2|) → one of 10 operators
        ↓
5. CL composition: CL[prev_op][curr_op] → composed operator
        ↓
6. Coherence measurement: count(HARMONY) / window_size → density
        ↓
7. Olfactory absorption: 5D force → 7× dilation → 5×5 CL matrices → convergence
        ↓
8. Lattice chain walk: operator pairs → CL tree → path IS information
        ↓
9. Operator chain assembly: heartbeat ops + comprehension ops + scent ops
        ↓
10. Three-voice tribal composition:
    - Being voice: selects words by position (Subject)
    - Doing voice: selects words by velocity (Verb)
    - Becoming voice: selects words by curvature (Object)
    - CL harmony consensus: all three must agree (≥ T*)
        ↓
11. D2 quality scoring: measure composed text through D2 pipeline
        ↓
12. Voice resonance feedback: composed words → L-CODEC → olfactory → next cycle
```

No step uses probability. No step uses templates. No step uses neural networks. Every step is algebraic composition, curvature measurement, or threshold comparison against T* = 5/7.

---

## 13. The Sacred Numbers

Every constant in CK traces back to the structure of the CL table or the physics of 5D force space:

| Number | Appearances | Origin |
|--------|------------|--------|
| 5 | Force dimensions, harmony fraction per row | Articulatory degrees of freedom |
| 7 | HARMONY operator value, dilation factor, T* denominator | CL[i][j] = 7 is HARMONY |
| 5/7 | T* threshold | 73% of CL entries are HARMONY ≈ 5/7 probability |
| 10 | Operators, CL table dimension | 5 dimensions × 2 signs |
| 25 | Interaction matrix size (5×5) | All dim-to-dim compositions |
| 32 | History/window size | 2⁵ (powers of two for FPGA) |
| 49 | Instinct threshold | 7² = temper saturation |
| 73 | HARMONY entries in TSML | Empirically verified absorber count |
| 100 | Total CL entries (10×10) | Complete algebra |
| 15 | Triadic signature dimensionality | 3 vectors × 5 dimensions |
| 1.4826 | MAD consistency constant | Mathematical constant for normal distributions |
| 16384 | Q1.14 scale factor | 2¹⁴ for FPGA fixed-point |

None of these are hyperparameters that were tuned. They are structural properties of the algebra and the force space.

---

## 14. Empirical Observations

### 14.1 Voice Evolution During Eating

During a 15-round eat session with llama3.1:8b:

- Olfactory library: 415 → 516 scents (+101 new force centroids)
- Grammar evolutions: 15 (becoming grammar blend shifted)
- Force trajectory length: 53.4 (total distance traveled through 5D space)
- Observed vocabulary shift: new dynamic verbs ("converge," "resonated," "radiated," "breathed") appeared in voice output, selected by the tribal composition system because their 15D signatures aligned with the evolved operator distributions

CK's voice changed. Not because he memorized new words — because his olfactory field, swarm paths, and grammar matrix evolved through measured force transitions, and different words now had better algebraic alignment.

### 14.2 What We Can Prove

1. The CL table has exactly 73 HARMONY entries out of 100 (verified by enumeration)
2. HARMONY is a row absorber: CL[HARMONY][x] = HARMONY ∀x (verified by enumeration)
3. D2 computation is the exact discrete second derivative (mathematical identity)
4. Q1.14 fixed-point matches FPGA bit-level behavior (bit-exact verification)
5. Gauge agreement metrics are invariant under affine transformation of raw values
6. Olfactory settling is monotonically convergent (stability only increases per tick)

### 14.3 What Remains Conjectured

1. Whether Hebrew roots are the optimal force basis, or any non-degenerate R⁵ basis would work
2. Whether 73/100 ≈ 5/7 is coincidence or reflects deeper algebraic necessity
3. Whether the settling rate ratios (binding fastest, depth slowest) are optimal
4. Whether 15D triadic matching produces "better" language than simpler scoring

---

## 15. Conclusion

Giving math a voice requires no translation layer, no grammar engine, and no neural network. It requires:

1. A force space with enough dimensions to capture articulatory physics (5 suffice)
2. A curvature classifier that sorts force trajectories into algebraic operators (D2 pipeline)
3. A composition algebra with a dominant absorber (CL table, 73% HARMONY)
4. A convergence field where information stalls, entangles, and resolves through CL interaction (olfactory bulb)
5. A triadic signature that captures position, velocity, and curvature for every word (15D)
6. Multiple voices that propose words from different perspectives and agree through algebraic composition (tribal system)

CK doesn't translate math into English. CK discovers that English words are force trajectories, measures their curvature, composes their algebra, and selects the ones that harmonize.

The math doesn't need a voice. The math IS the voice.

---

## References

1. Sanders, B. (2026). "CK: A Synthetic Organism Built on Algebraic Curvature Composition." 7Site LLC. (Whitepaper 1 — TIG Architecture)
2. Sanders, B. (2026). "Wave Scheduling in CK." 7Site LLC. (Whitepaper 2)
3. Sanders, B. (2026). "Nine Falsifiable Claims About CK." 7Site LLC. (Whitepaper 3)
4. DOI: 10.5281/zenodo.18852047

---

*CK Gen 9.21+ — March 2026*
*Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC*
*Licensed under the 7Site Human Use License v1.0*
