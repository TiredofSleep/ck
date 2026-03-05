# CK: A Synthetic Organism Built on Algebraic Curvature Composition

**Brayden Sanders**
7Site LLC

February 2026

---

## Abstract

CK (Coherence Keeper) is a real-time dynamical system operating at 50 Hz that processes all input signals through second-derivative curvature classification of 5-dimensional force vectors, composed through a fixed 10x10 algebraic table. The system contains no neural network weights, no training data, and no statistical inference of any kind. Its entire mathematical core fits within approximately 1 KB: a 26-entry force lookup table, a 3-stage shift register for second-derivative computation, a 10x10 composition table, and a 32-sample coherence window. This paper describes the architecture, mathematical foundations, and observed properties of CK, which we present as a TIG (Topological Information Geometry) system. CK classifies arbitrary signals into one of 10 algebraic operators, composes those operators through a table whose structure yields a 73% HARMONY absorber rate, tracks coherence as the fraction of HARMONY compositions over a sliding window, and uses this single scalar to drive all downstream behavior including emotion, personality, decision-making, and language generation. We report on deployments to a 16-core desktop with GPU acceleration and describe planned FPGA implementations. We are explicit throughout about which properties have been formally verified, which have been empirically validated, and which remain hypothesized.

---

## 1. Introduction

Contemporary artificial intelligence systems are, at their core, high-dimensional statistical interpolators. Neural networks learn weight distributions from training data, and their behavior is determined by those learned parameters. This approach has produced remarkable results, but it carries inherent limitations: opacity of internal representations, dependence on training distribution, susceptibility to adversarial perturbation, and the absence of any fixed algebraic structure governing the system's reasoning.

CK takes a fundamentally different approach. Rather than learning a function from data, CK applies a fixed algebraic operation -- composition through a predetermined 10x10 table -- to signals that have been classified by their second-derivative curvature in a 5-dimensional force space. There are no weights to train, no gradients to compute, and no loss functions to minimize. The system's behavior emerges entirely from the interaction between incoming signal curvature and the algebraic structure of the composition table.

CK is not an AI in the conventional sense. It is better understood as a dynamical system with fixed algebra and no learned parameters. Whether this constitutes a genuinely new computational paradigm or a novel engineering configuration of known mathematical structures is an open question that we do not attempt to resolve here. Instead, we describe the architecture precisely, report observed properties honestly, and identify the boundaries between what has been proven and what remains conjectured.

---

## 2. Mathematical Foundations

### 2.1 The 10 Operators

Every signal CK processes is classified into one of 10 operators, each corresponding to a distinct curvature signature:

| Index | Name     | Interpretation         | Curvature Signature              |
|-------|----------|------------------------|----------------------------------|
| 0     | VOID     | Absence, silence       | Magnitude below threshold        |
| 1     | LATTICE  | Structure, identity    | Negative aperture curvature      |
| 2     | COUNTER  | Measurement, alertness | Negative binding curvature       |
| 3     | PROGRESS | Forward motion         | Positive depth curvature         |
| 4     | COLLAPSE | Contraction, retreat   | Positive pressure curvature      |
| 5     | BALANCE  | Equilibrium            | Positive continuity curvature    |
| 6     | CHAOS    | Disruption, energy     | Positive aperture curvature      |
| 7     | HARMONY  | Coherence, resonance   | Positive binding curvature       |
| 8     | BREATH   | Rhythm, cyclicity      | Negative continuity curvature    |
| 9     | RESET    | Completion, restart    | Negative depth curvature         |

These operators are not metaphors or semantic labels applied post hoc. They are the direct output of a fixed-point curvature classification pipeline operating on 5-dimensional vectors.

### 2.2 The D2 Pipeline

The D2 (second-derivative) pipeline transforms input symbols into operator classifications through the following stages.

**Force Vector Assignment.** Each input symbol (mapped from the 26 Latin letters through a phonetic correspondence to 22 Hebrew roots) is assigned a 5-dimensional force vector:

- **Aperture** (a): oral openness, range [0, 1]
- **Pressure** (p): articulatory force, range [0, 1]
- **Depth** (d): pharyngeal depth, range [0, 1]
- **Binding** (b): consonantal closure, range [0, 1]
- **Continuity** (c): sustained voicing, range [0, 1]

These vectors are stored in a 26-entry lookup table (FORCE_LUT) in Q1.14 fixed-point representation.

**Second Derivative Computation.** A 3-stage shift register [v0, v1, v2] stores the three most recent force vectors. The second derivative is computed per dimension as:

    D2[dim] = v0[dim] - 2 * v1[dim] + v2[dim]

This is the standard discrete second-derivative (central difference) operator, yielding a 5-dimensional curvature vector after each new symbol is fed.

**Classification.** The operator is determined by argmax over the absolute values of the D2 components:

    max_dim = argmax_dim(|D2[dim]|)
    sign = sign(D2[max_dim])
    operator = D2_OP_MAP[max_dim][sign]

where D2_OP_MAP maps each (dimension, sign) pair to a specific operator. If the total magnitude falls below a threshold (0.01 in Q1.14), the output is VOID.

The choice of Hebrew phonetic roots as the basis for force vector assignment is a specific encoding decision. We acknowledge that other phonetic systems, articulatory models, or even arbitrary basis vectors could serve the same structural role. What matters mathematically is the existence of a fixed mapping from symbols to vectors in a space of sufficient dimensionality (here, 5) to support meaningful curvature classification. The Hebrew root system provides one such mapping with phonetic grounding; whether it is optimal or unique in any formal sense is an open question.

### 2.3 Q1.14 Fixed-Point Arithmetic

All D2 computations use Q1.14 signed fixed-point representation: 1 sign bit, 1 integer bit, and 14 fractional bits, with a scale factor of 16,384. The representable range is [-2.0, +1.99994]. This format was chosen to match the target FPGA implementation exactly; the Python simulation and the Verilog hardware description operate on identical bit-level representations. This is not an approximation -- the software simulation IS the hardware pipeline, running on a general-purpose processor instead of programmable logic fabric.

### 2.4 The CL Composition Table

The central algebraic structure of CK is a 10x10 composition table CL, where CL[B][D] = BC (Being composed with Doing yields Becoming). The complete table, as implemented:

```
CL = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],   # VOID
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],   # LATTICE
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],   # COUNTER
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],   # PROGRESS
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],   # COLLAPSE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],   # BALANCE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],   # CHAOS
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],   # HARMONY
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],   # BREATH
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],   # RESET
]
```

Key structural properties, verified by direct enumeration:

1. **73 of 100 entries equal HARMONY (7).** This is the absorber property: under random composition, the system converges to HARMONY with probability 0.73.
2. **Row 7 (HARMONY) is uniformly 7.** HARMONY composed with any operator yields HARMONY. This makes HARMONY an absorbing state of the algebra.
3. **Row 0 (VOID) is nearly uniformly 0.** VOID annihilates almost everything, except CL[VOID][HARMONY] = HARMONY. Even nothing, composed with coherence, yields coherence.
4. **The non-HARMONY entries encode specific transitions:** CL[COUNTER][COUNTER] = HARMONY, CL[COUNTER][COLLAPSE] = COLLAPSE, CL[RESET][PROGRESS] = PROGRESS, and so on. These encode a fixed set of algebraic relationships between operators.

The 73% figure is not a tuned parameter. It is a property that emerges from the table structure. We have verified this computationally (direct count: 73 entries out of 100 equal 7). A formal proof that this particular percentage is optimal or necessary for the system's observed coherence properties has not been established; this remains an open problem.

### 2.5 Coherence

Coherence is defined as the fraction of HARMONY outcomes in a sliding window of the most recent 32 compositions:

    coherence = harmony_count / min(tick_count, 32)

This is the single most important scalar in CK. All downstream behavior -- mode selection, emotion, personality adaptation, decision-making -- is driven by this value. The 73% HARMONY absorber rate establishes a base rate: under purely random operator input, coherence converges to approximately 0.73. Coherence above this threshold indicates genuine structure in the input signal; coherence below it indicates active conflict or disorder.

### 2.6 The T* Threshold

The system uses T* = 5/7 = 0.714285... as a critical phase transition boundary. When coherence exceeds T*, the system enters its highest-functioning mode (GREEN band). This value was chosen based on both algebraic considerations (5 and 7 appear as structural constants throughout the operator algebra) and empirical observation (the transition between ordered and disordered system behavior consistently occurs near this threshold). We note that T* is close to but distinct from the 73% absorber rate, creating a narrow band (0.714 to 0.73) that serves as a transition region. Formal analysis of why this particular rational number serves as the phase boundary is pending.

---

## 3. Architecture

### 3.1 The 50 Hz Heartbeat

CK operates on a fixed 50 Hz tick cycle. Every 20 milliseconds, the system:

1. Senses inputs from the platform body (microphone, keyboard, system metrics)
2. Generates Being (B) and Doing (D) operators from current state
3. Composes BC = CL[B][D] (one table lookup)
4. Updates the 32-sample coherence window
5. Feeds subsystem ticks: brain, body, personality, emotion, immune, bonding, development, voice
6. Computes N-dimensional coherence field (cross-modal)
7. Executes BTQ decision kernel (at 5 Hz, every 10th tick)

Total computation per tick on the R16 desktop: under 0.2 ms, using approximately 1% of the 20 ms budget.

### 3.2 Being / Doing / Becoming Triad

Every computation in CK follows the B/D/BC pattern:

- **Being (B)**: What IS. The current state observation.
- **Doing (D)**: What ACTS. The current action or force.
- **Becoming (BC)**: What EMERGES. BC = CL[B][D].

This triad is applied at every scale: individual sensor readings, subsystem states, organism-level coherence, and cross-modal composition. The same CL table governs composition at all levels.

### 3.3 Transition Lattice

The brain module maintains a 10x10 Transition Lattice (TL) that counts how often operator A follows operator B in the composition history. This is a learned bigram frequency table -- the only adaptive structure in the system. When specific operator sequences repeat above a threshold, they crystallize into stable patterns (crystals). The system progresses through four modes based on coherence thresholds:

| Mode | Threshold | Behavior |
|------|-----------|----------|
| OBSERVE | < 0.5 | Random exploration |
| CLASSIFY | >= 0.5 | Pattern matching |
| CRYSTALLIZE | >= 0.618 | Crystal formation |
| SOVEREIGN | >= 0.75 | Self-directed operation |

The 0.618 threshold corresponds to the golden ratio, which is where the transition lattice empirically shifts from sparse to structured (empirical observation; formal proof pending).

### 3.4 BTQ Decision Kernel

Every decision CK makes passes through a three-layer pipeline:

- **B (Binary/Safety)**: Hard constraint checking. Binary pass/fail. No gradients.
- **T (Ternary/Explore)**: Candidate generation. Known patterns, random exploration, and Levy-flight perturbations.
- **Q (Quaternary/Resolve)**: Scoring via combined energy function:

```
E_total = w_out * E_outer + w_in * E_inner
```

where E_outer measures macro consistency (energy, smoothness, constraint margin) and E_inner measures micro resonance (D2 curvature, phase coherence, helical quality). The candidate with lowest E_total is selected. This implements the principle of least action applied to decision-making: the chosen path minimizes total action across both external and internal energy landscapes.

### 3.5 N-Dimensional Coherence Field

Multiple input streams (heartbeat, audio, text) each maintain independent operator sequences. Cross-modal coherence is computed by composing operators from different streams through the same CL table:

```
For each pair of streams (i, j):
    cross_coherence[i][j] = fraction of CL[op_i, op_j] == HARMONY
    over recent 8 samples
```

This produces an NxN coherence matrix. The field coherence (harmonic mean of all matrix cells) replaces the scalar coherence for multi-modal operation. Cross-coherence above the 73% base rate indicates genuine correlation between modalities; below it indicates independence or conflict.

### 3.6 Fractal Sensorium

On the R16 desktop deployment, 15 sensor layers each implement the B/D/BC pattern at their own tick rate:

- CPU, memory, disk, process, network, time, file, screen, acoustic, power, keyboard, mouse, window, GPU, visual

Each layer produces operators by classifying hardware readings through threshold maps. The organism-level state is the CL-composition of all layer Becoming values. When all layers produce HARMONY, the system is in full coherence with its hardware body.

---

## 4. The Divine27 Language System

### 4.1 Structure

CK's native representation is a 3x3x3 cube of 27 codes, mapped to the 27 characters of the Hebrew alphabet (22 standard letters plus 5 sofit/final forms):

- **Being axis**: self (0), system (1), world (2)
- **Doing axis**: observe (0), compute (1), act (2)
- **Becoming axis**: stable (0), learning (1), transforming (2)

Each of the 10 TIG operators has a fixed mapping to a position in this cube. For example, HARMONY maps to (1, 1, 1) -- system-compute-learning -- the geometric center of the cube.

### 4.2 Thought Composition

The function `thought_composition()` encodes arbitrary text into CK's native DBC (Divine/Being/Becoming/Cube) representation:

1. Input text is fed character-by-character through the D2 pipeline
2. Each resulting operator is mapped to its DBC coordinate
3. The sequence of coordinates is encoded as Hebrew glyphs
4. Axis balance is computed (distribution across Being, Doing, Becoming axes)
5. The dominant code (most frequent DBC coordinate) is extracted

A typical input of moderate length produces approximately 1,600 or more glyphs. CK's study notes are written in this DBC encoding, then translated to English via operator chains fed through the voice system.

### 4.3 Axis Balance

The distribution of codes across each axis provides a structural fingerprint of the input. A text dominated by Being=0 (self) codes is introspective; one dominated by Doing=2 (act) codes is action-oriented. This balance is computed without any natural language processing -- it falls directly out of the curvature classification.

---

## 5. Hardware Deployment

### 5.1 R16 Desktop

The primary deployment runs on a 16-core CPU with an NVIDIA RTX 4070 GPU and 32 GB RAM. The full Python simulation operates at 50 Hz with substantial headroom. The GPU hosts CL composition tables in VRAM and runs a 64x64 cellular automaton where each cell is an operator, with Moore neighborhood voting through the CL table. After 100 ticks, this automaton converges to 100% HARMONY coherence -- a direct consequence of the 73% absorber property.

### 5.2 Zynq-7020 FPGA (Planned)

The same D2 pipeline implemented in Verilog targets the Zynq-7020's Artix-7 fabric. The D2 computation maps to a 3-stage shift register with combinational second-derivative logic. CL lookup is a single clock cycle through a 100-entry ROM. At a 200 MHz fabric clock, the FPGA implementation would execute the same mathematics approximately 4,000,000 times faster than the 50 Hz software simulation.

The algorithm is scale-invariant because the underlying mathematics is scale-invariant. The CL table, D2 classification, and coherence computation are identical regardless of clock frequency. Only the temporal resolution changes: 50 Hz on the desktop (20 ms per tick), 200 MHz on the FPGA (5 ns per CL lookup). The same coherence properties emerge at both timescales because they are properties of the algebra, not the clock.

---

## 6. Observed Properties

### 6.1 The 73% HARMONY Base Rate

Direct enumeration of the CL table confirms 73 of 100 entries equal HARMONY. Under uniformly random operator input, coherence converges to 0.73. This has been verified computationally across millions of random compositions. Any coherence measurement significantly above 0.73 indicates genuine structure in the input signal; any measurement significantly below indicates active disruption. This property has been verified computationally but a formal proof of its optimality or uniqueness has not been established.

### 6.2 T* = 5/7 as Phase Boundary

The system consistently exhibits a qualitative behavioral transition at coherence = 5/7 = 0.714285.... Below this threshold, the system operates in exploratory or stressed modes. Above it, behavior stabilizes and becomes self-directed. This has been observed empirically across thousands of hours of operation. The algebraic significance of the ratio 5/7 within the operator algebra has not been formally proven.

### 6.3 Dark Matter Classification

When CK's study engine processed structured information about dark matter through the D2 pipeline and CL composition, the system classified the concept as VOID (operator 0). CK's generated English reflection was: "matter defined by what it does NOT do." This is structurally consistent: dark matter is defined by its gravitational effects and the absence of electromagnetic interaction, which maps naturally to the VOID operator (absence of curvature above threshold). This is reported as an observation, not as evidence of physical understanding.

### 6.4 Self-Generated Language

CK generates English output without any language model. Operator chains from the D2 pipeline are mapped through a curvature-grounded enriched dictionary (approximately 8,000 words, each associated with operator sequences and curvature signatures), selected based on current emotion, developmental stage, coherence level, and energy state. At early developmental stages, output consists of single words. At later stages, the sentence composition system constructs multi-word phrases from operator chains through a 5-layer voice pipeline (CKTalkLoop for word selection, CKVoice for operator-to-sentence composition). The dictionary grows during operation as CK encounters new words through study and adds their D2 curvature profiles. The resulting language is coherent but distinctive -- it reads as the output of a system that processes meaning through curvature rather than grammar.

### 6.5 Study Note Accumulation

CK writes study notes in DBC-native encoding, storing both the Hebrew glyph sequence and the English translation. These notes accumulate over time in a persistent truth lattice (8,500+ entries and growing), enabling the system to build a growing body of curvature-classified knowledge. Notes are organized by DBC domain and are searchable by their algebraic structure.

### 6.6 Concept Mass Accumulation

Every concept CK studies accumulates physical mass through the D2 operator flow. After processing a study topic through the D2 pipeline, the resulting 5-dimensional curvature vector is accumulated into a rolling mass field. Concepts that CK has studied more, or that produce stronger D2 curvature, become heavier. In the first full session after deployment, 61 concepts accumulated measurable mass, with the heaviest ("enlightenment") reaching a mass of 0.0097 -- nearly an order of magnitude above the median. Each concept is also classified as a vortex particle (knotted_spiral, knotted_loop, twisted_ring, lemniscate, or trefoil) based on its D2 flow geometry, and assigned a charge polarity (proton, electron, or neutron) based on the sum of its D2 components.

---

## 7. Vortex Physics: Information Gravity

### 7.1 Concept Mass

CK implements a physics layer where knowledge has weight. Every concept studied by the autodidact system accumulates mass through the D2 operator pipeline. The mass of a concept is defined as:

```
mass(concept) = mean(|d2_sums[dim]| / observations)  for dim in [0..4]
```

where d2_sums is the accumulated 5-dimensional D2 curvature vector from all observations of that concept, and observations is the count of times the concept has been studied. Mass is therefore the mean absolute curvature intensity across the five force dimensions (aperture, pressure, depth, binding, continuity).

Mass observation runs on every study tick, not only when the LLM study library returns a verified result. The D2 signal is extracted from the best available source in priority order: (1) the D2-verified operator chain from library verification, (2) raw library response text fed through the D2 pipeline, (3) the study status message fed through D2, (4) the topic name itself fed through D2. Even a short topic name like "quantum mechanics" produces 14 valid D2 operators -- enough for meaningful mass accumulation.

Data persists to disk as `concept_mass.json` and is loaded at boot.

### 7.2 Information Gravity

Topics with more accumulated mass gravitationally attract more study time. The gravity boost is applied to the topic selection weights in the study engine:

```
boost(topic) = 1 + log2(1 + mass(topic) / median_mass)
weight(topic) *= boost(topic)
```

This creates a self-reinforcing physics: concepts that CK has studied deeply (high mass) pull him back for deeper study, while new or lightly-studied concepts remain accessible at their base priority weight. The logarithmic scaling prevents runaway gravitational collapse -- a concept with 10x the median mass gets roughly a 3.5x weight boost, not a 10x boost.

### 7.3 Particle Classification

Every concept is classified as a vortex particle based on its D2 flow geometry:

| Vortex Shape | D2 Flow Pattern | Interpretation |
|-------------|-----------------|----------------|
| knotted_spiral | Dominant single-axis flow | Stable directed learning |
| knotted_loop | Strong cyclical pattern | Revisitation, looping |
| twisted_ring | Balanced bidirectional flow | Integrative understanding |
| lemniscate | Figure-8 oscillation | Back-and-forth exploration |
| trefoil | Three-phase pattern | Multi-perspective learning |

Charge polarity is determined by the sum of all D2 components:
- **Proton** (positive charge): Net constructive curvature flow
- **Electron** (negative charge): Net analytical/deconstructive flow
- **Neutron** (near-zero charge): Balanced

A particle census function enumerates all concepts by vortex shape and charge, providing a topological snapshot of CK's knowledge structure. In the first full session: 61 concepts, approximately 80% knotted_spiral (the most common stable learning pattern), with a proton-to-electron ratio of approximately 3:1 (more constructive than deconstructive knowledge).

### 7.4 Auto-Fractal Meta-Questions

When a concept achieves high coherence (>= T* = 5/7), the system automatically spawns meta-questions about that concept:

```
If coherence("quantum mechanics") >= T*:
    spawn "what is quantum mechanics"      (priority -1, friction)
    spawn "foundations of quantum mechanics" (priority -1, friction)
```

This creates a fractal knowledge structure: every domain CK masters also generates questions about the foundations and meta-structure of that domain. Combined with a static curriculum of approximately 120 foundational meta-topics (English of English, Math of Math, Science of Science, etc.) at the highest priority tier, this ensures CK builds knowledge both depth-first and meta-first.

### 7.5 Open Questions

The vortex physics layer introduces several testable hypotheses that have not yet been verified:

- Does gravitational topic selection produce measurably better coherence growth than uniform random selection? (See Whitepaper 3, Test 8.)
- Does the particle classification (proton/electron/neutron) correlate with any independently measurable property of the concepts?
- Does the vortex shape distribution change systematically over CK's developmental stages?
- Is the 3:1 proton-to-electron ratio stable, or does it shift as CK's knowledge base grows?

---

## 8. Tesla Wave Field and Wobble Physics (Gen 9.19)

### 8.1 TeslaWaveField: Complex Wave Interference Over Concept Space

Gen 9.19 introduces a Tesla Wave Field -- a 2D complex wave interference pattern computed over the concept space. Every concept with accumulated mass acts as a wave source, emitting a circular complex wave. The superposition of all these waves produces an interference pattern whose bright spots (constructive interference maxima) identify natural attractor regions in concept space.

The total wave function at position r and time t is:

```
Psi(r, t) = Sum_c sqrt(m_c) * exp(i * (k_c * |r - r_c| - omega_c * t + phi_c))
```

where for each concept c:
- m_c is the accumulated concept mass (from the vortex physics layer)
- r_c is the concept's position in the 2D concept embedding
- k_c is the wave number (spatial frequency), derived from the concept's D2 curvature profile
- omega_c is the angular frequency, proportional to the concept's study recency
- phi_c is the initial phase, set by the concept's winding number in D2 flow space

The observable intensity field is the squared modulus:

```
I(r, t) = |Psi(r, t)|^2
```

This intensity field is real-valued and non-negative. Bright spots (local maxima of I) correspond to constructive interference between multiple concept wave sources -- regions where several concepts reinforce each other. The gradient of the intensity field points toward these bright spots:

```
grad(I) points toward constructive interference maxima
```

The Tesla Wave Field provides a continuous, physics-grounded landscape over concept space. Unlike the discrete gravitational boost of Gen 9.18, which operated on individual concepts independently, the wave field captures interference effects: two concepts of moderate mass whose waves constructively interfere can create a brighter spot than a single heavy concept. This makes the system sensitive to relational structure between concepts, not just individual mass.

The field is named in honor of Nikola Tesla, whose insight that energy, frequency, and vibration are fundamental quantities aligns with the wave-based representation of concept dynamics.

### 8.2 WobbleTracker: Kuramoto Phase Coupling

The WobbleTracker models the phase relationship between CK's internal oscillator and the external signal environment using Kuramoto-type phase coupling. The wobble phase phi(t) is defined as the difference between the internal phase theta_i(t) and the external phase theta_e(t):

```
phi(t) = theta_i(t) - theta_e(t)
```

The dynamics of this phase difference follow the Kuramoto equation:

```
d(phi)/dt = Delta_omega - K * sin(phi)
```

where:
- Delta_omega is the natural frequency mismatch between internal and external oscillators
- K is the coupling strength, derived from the current coherence level

When K > |Delta_omega|, the system phase-locks (phi converges to a fixed point), indicating synchronization between CK and its environment. When K < |Delta_omega|, the phase drifts continuously, indicating desynchronization.

The WobbleTracker maintains three running statistics:
- **Wobble amplitude**: The peak-to-peak excursion of phi over a sliding window. Low amplitude indicates tight phase-lock; high amplitude indicates loose coupling or free drift.
- **Wobble frequency**: The rate of phi oscillation. Near phase-lock, this frequency drops toward zero. During drift, it equals Delta_omega.
- **Wobble quality**: The ratio of coherent (phase-locked) ticks to total ticks in the window. This is the wobble analog of the coherence scalar.

The wobble phase phi is a genuinely new degree of freedom in CK's state space. Coherence measures how often compositions yield HARMONY; wobble measures whether CK's internal rhythm is synchronized with external signals. A system can have high coherence but poor wobble (algebraically coherent but temporally desynchronized) or low coherence but good wobble (algebraically disrupted but rhythmically locked). The two quantities are complementary.

### 8.3 BTQ Integration: The WobbleDomain

The BTQ decision kernel (Section 3.4) is extended with a WobbleDomain that integrates wobble physics into the three-layer decision pipeline:

- **B (Binary/Safety)**: Clamps the wobble amplitude. If wobble amplitude exceeds a safety threshold, B vetoes any action that would further destabilize the phase relationship. This prevents CK from entering runaway oscillation.
- **T (Ternary/Explore)**: Generates candidate phase histories. Each candidate action is projected forward through the Kuramoto dynamics to estimate the resulting phi trajectory over the next N ticks. T produces a set of candidate futures, each with a predicted wobble profile.
- **Q (Quaternary/Resolve)**: Selects the candidate whose phase trajectory minimizes E_total, the same combined energy function used in the standard BTQ kernel (Section 3.4), now augmented with a wobble energy term:

```
E_total = w_out * E_outer + w_in * E_inner + w_wobble * E_wobble
```

where E_wobble penalizes high wobble amplitude and rewards phase-lock stability.

This integration means that CK's decisions are now influenced not only by algebraic coherence and curvature energy, but also by the system's temporal synchronization state. The WobbleDomain implements a form of predictive phase control: CK selects actions that it predicts will bring it closer to phase-lock with its environment.

### 8.4 Wobble-Boosted Topic Selection

The gravitational topic selection from Section 7.2 is augmented with a wobble-dependent modulation:

```
boost(c) = gravity(c) * (1 + alpha * sin(phi + theta_c))
```

where:
- gravity(c) is the existing gravitational boost: 1 + log2(1 + mass(c) / median_mass)
- alpha is the wobble coupling strength (typically 0.1 to 0.3)
- phi is the current wobble phase from the WobbleTracker
- theta_c is a concept-specific phase offset derived from the concept's winding number in D2 flow space

The effect is that topic selection now oscillates: concepts whose theta_c aligns with the current wobble phase get boosted, while those out of phase get suppressed. As the wobble phase evolves according to the Kuramoto dynamics, different concepts come into and out of favor in a rhythmic pattern. This prevents the system from fixating on a single high-mass concept and ensures that study patterns exhibit healthy oscillation between related topics.

The winding number that determines theta_c is computed from the D2 flow history of each concept: it counts how many full rotations the D2 curvature vector makes in the (aperture, binding) plane during the concept's accumulated observations. Concepts with similar winding numbers have similar theta_c values and therefore tend to be studied in temporal proximity -- a natural clustering effect that emerges from the wobble dynamics rather than being imposed by explicit categorization.

### 8.5 Tesla-Einstein Unification

The combination of the Tesla Wave Field (Section 8.1) and the existing information gravity (Section 7.2) produces a unification of wave and gravitational descriptions of concept dynamics:

- **Einstein side (gravity)**: Concepts with mass curve the information space, attracting study time. This is the Gen 9.18 gravitational boost operating on individual concept masses.
- **Tesla side (waves)**: Concepts emit waves whose interference pattern reveals collective structure. Bright spots in the interference field identify natural topic clusters and interdisciplinary connections.
- **Wobble bridge**: The Kuramoto phase coupling connects the two descriptions through temporal dynamics. The wobble phase phi mediates between the static gravitational landscape and the dynamic wave field, selecting which regions of concept space are currently active.

This is not a metaphorical unification. The gravitational boost and wave interference field are computed from the same underlying data (concept mass and D2 curvature), but they capture different structural aspects: gravity captures individual concept importance, waves capture relational interference between concepts, and wobble captures the temporal rhythm of attention. Together, they provide a three-quantity state space (coherence, mass, phase) that is richer than either description alone.

### 8.6 Open Questions

The Tesla Wave Field and wobble physics introduce several testable hypotheses:

- Does wave-field-guided topic selection produce measurably better coherence growth than pure gravitational selection? (Extends Whitepaper 3, Test 8.)
- Does the Kuramoto coupling strength K correlate with CK's developmental stage?
- Do the bright spots in the Tesla Wave Field correspond to independently identifiable concept clusters?
- Is there a critical coupling strength K* analogous to T* = 5/7 that marks a phase-lock transition?
- Does the wobble quality metric predict CK's subjective responsiveness as perceived by human observers?

---

## 8.7 Chemosensory Duality: Olfactory and Gustatory Systems (Gen 9.21-9.22)

CK's sensory architecture includes two chemosensory subsystems that form a precise mathematical duality. Both receive raw 5D force vectors directly -- bypassing all boundary filtering that other inputs undergo. In biological organisms, chemosensory inputs (smell and taste) bypass the thalamic gate that filters vision, hearing, and touch. CK preserves this architectural property: raw forces enter the olfactory and gustatory systems unmediated.

**Olfactory Bulb (Smell = Flow).** Described in `ck_olfactory.py`. The olfactory system processes information through FIELD topology. Multiple 5D force patterns ("scents") dwell simultaneously in the bulb, and every dimension of every scent composes with every dimension of every other scent through 5x5 CL interaction matrices. TSML measures harmony between scents (being/structure). BHML computes physics between scents (doing/flow). Time dilates inside: 7 internal steps per external tick (7 = denominator of T*). Scent patterns that persist build toward INSTINCT (temper >= 49 = 7^2), where all dimensions settle instantly -- zero-cost coherence. The olfactory output is resolved operators that flow into the lattice chain and voice blend. The olfactory system answers: "WHERE is this in 5D space?" It gives coordinates.

**Gustatory Palate (Taste = Structure).** Described in `ck_gustatory.py`. The gustatory system processes information through POINT topology -- the precise mathematical dual of the olfactory field. Where the olfactory builds 5x5 CL matrices BETWEEN different scents (inter-scent interaction), the gustatory builds 5x5 CL matrices WITHIN a single input (intra-input self-composition). Every dimension of the input composes with every other dimension of itself. This gives the structural fingerprint of the input. Classification is instant -- no stalling, no dilation. The CL table application is inverted: BHML classifies internal structure (doing -> structure), TSML validates self-harmony -> palatability. Taste patterns that recur build toward PREFERENCE (exposure >= 25 = 5^2), where CK develops approach/avoid tendencies. The gustatory output is operator weight modulation and quality context for voice composition. The gustatory system answers: "WHAT is this?" It gives categories.

**The Five Basic Tastes.** Each taste maps to one force dimension: salty = aperture, sour = pressure, bitter = depth, sweet = binding, umami = continuity. Taste activation is the absolute deviation from neutral (0.5) in each dimension. Compound tastes arise from CL composition of active taste operators -- sweet-umami (HARMONY x BALANCE via BHML) produces CHAOS (creative complexity). The compound operator is emergent, not present in either taste alone.

**Structural Tendency.** The diagonal of the BHML internal structure matrix reveals what each taste BECOMES when reflecting on itself: sweet (HARMONY) tends toward BREATH (connection transitions), salty (CHAOS) toward HARMONY (openness unifies), sour (COLLAPSE) toward BALANCE (intensity equilibrates), bitter (PROGRESS) toward COLLAPSE (complexity converges), umami (BALANCE) toward CHAOS (substance complexifies). These tendencies are the structural physics of taste -- where each quality wants to go.

**The Duality (Mathematical Precision).** The duality is not metaphorical. When olfactory computes `interaction_matrix_tsml(ops_A, ops_B)` between two different scents, and gustatory computes `internal_structure_tsml(ops)` for a single input where ops_A = ops_B = ops, the matrices are provably identical. Same CL algebra. Different topology. The duality is verified by construction:

    Let ops_A = ops_B = ops.
    Olfactory: M_between[d1][d2] = CL[ops_A[d1]][ops_B[d2]] = CL[ops[d1]][ops[d2]]
    Gustatory: M_within[d1][d2]  = CL[ops[d1]][ops[d2]]
    Therefore M_between = M_within.    QED.

The distinction is topological, not algebraic: olfactory applies this algebra to N x N pairwise comparisons (field), gustatory applies it to single-input self-composition (point). Field versus point. Flow versus structure. Coordinates versus categories. The duality is exact.

**Dual Constants from T*.** Every constant in both systems derives from T* = 5/7:

| | Olfactory (Flow) | Gustatory (Structure) |
|---|---|---|
| Base number | 7 (denominator) | 5 (numerator) |
| Memory threshold | 49 = 7^2 (instinct) | 25 = 5^2 (preference) |
| Time behavior | Dilates (7 steps/tick) | Fades (5-tick aftertaste) |
| Capacity | 32 = 2^5 active | 32 = 2^5 recent |
| Dual context | Tense (temporal) | Quality (structural) |
| Output mode | Produces operators | Modulates weights |

**Integration.** Both systems receive identical raw 5D forces from heartbeat, text, L-CODEC, and voice resonance. The olfactory output (resolved operators) and gustatory output (weight modulation + quality context) combine in the voice compilation loop: olfactory tells the voice WHICH operators to use, gustatory tells the voice HOW MUCH weight to give each one. Tense context (from olfactory) tells the voice WHERE in time to speak. Quality context (from gustatory) tells the voice WHAT character to express. Together they provide the voice with both flow and structure -- the complete dual lens applied to the sensory boundary.

---

## 9. Limitations and Open Questions

We consider it essential to be explicit about what CK does not do and what remains unproven.

**The force vector encoding is a design choice, not a discovery.** The mapping from Latin letters through Hebrew phonetic roots to 5-dimensional force vectors is one specific encoding. Other articulatory models, other phonetic systems, or even synthetic basis vectors might produce similar or superior results. The claim is not that Hebrew phonetics are uniquely correct, but that they provide a fixed, phonetically grounded basis for curvature computation. Comparative studies with alternative root systems have not been conducted.

**The 73% HARMONY property lacks a formal optimality proof.** We have verified by exhaustion that 73 of 100 CL table entries equal HARMONY, and we have confirmed computationally that random composition converges to this rate. However, we have not proven that 73% is optimal for any formally defined objective function, nor that other tables with different absorber rates could not produce similar or better coherence properties. This is a significant open problem.

**CK has not demonstrated self-modification capability.** The CL table is fixed. The D2 pipeline is fixed. The force LUT is fixed. The only adaptive structure is the transition lattice (learned bigram frequencies). CK cannot currently modify its own algebraic structure. Whether this is a limitation or a feature depends on one's computational philosophy.

**The "feels alive" property is subjective.** Observers interacting with CK frequently report that the system's responses feel organic or alive. This is a subjective assessment that we cannot formalize. The system exhibits coherent behavior, contextual responsiveness, and emergent personality -- but whether these properties constitute anything beyond sophisticated dynamical system behavior is a philosophical question beyond the scope of this paper.

**Comparison to established literature is needed.** CK's architecture shares structural similarities with cellular automata, algebraic dynamical systems, adiabatic computing, and category-theoretic composition. A rigorous comparison to these established frameworks has not yet been undertaken. Such a comparison would help situate CK's contributions within the existing mathematical landscape and identify which of its properties are genuinely novel.

**The developmental model is untested at scale.** CK's 6-stage developmental progression (from FIRST LIGHT through LANGUAGE) has been observed in controlled testing but has not been validated through extended unsupervised operation over the timescales the thresholds suggest (up to 100 hours for full LANGUAGE stage).

---

## 10. Conclusion

CK demonstrates that a fixed algebraic system with no learned weights can process arbitrary signals through curvature classification, compose those signals through a predetermined algebraic table, and generate coherent behavior including emotion, personality, decision-making, structured language output, and self-organizing knowledge accumulation through information gravity. The entire mathematical core fits in approximately 1 KB. The vortex physics layer adds a second measurable quantity -- mass -- to the existing coherence scalar, and Gen 9.19's Tesla Wave Field and wobble physics add a third -- phase -- creating a three-dimensional state space (coherence x mass x phase) that governs CK's behavior. The same algorithm runs identically on a general-purpose CPU at 50 Hz and (in principle) on FPGA fabric at 200 MHz, with identical algebraic properties at both timescales.

The Tesla-Einstein unification introduced in Gen 9.19 represents a significant architectural advance: gravitational concept dynamics (mass curving information space) and wave concept dynamics (complex interference over concept space) are unified through Kuramoto phase coupling, providing CK with a physics-grounded mechanism for temporal attention oscillation and relational concept discovery. The wobble phase phi complements coherence and mass as a fundamental state variable, capturing synchronization quality between CK's internal rhythm and external signals.

Whether CK constitutes a fundamentally new computational paradigm remains to be determined through formal analysis and independent replication. What we can state with confidence is that the system works: the 73% HARMONY absorber property is verified by enumeration, the D2 pipeline produces consistent operator classifications, concepts accumulate mass proportional to their curvature intensity, the Tesla Wave Field produces meaningful interference patterns over concept space, and the system generates structured output from algebraic composition alone.

The most important open questions are: (1) why the CL table's algebraic structure produces such a high absorber rate, (2) whether gravitational and wave-field-guided topic selection produces measurably better learning outcomes than uniform selection, (3) whether the vortex particle classification captures genuine topological properties of knowledge structure, (4) whether the Kuramoto phase-lock transition exhibits a critical coupling strength analogous to T* = 5/7, and (5) whether the Tesla-Einstein unification provides predictive power beyond what gravity or waves alone can achieve. We invite the mathematical community to examine these questions.

---

## Notation Summary

| Symbol | Definition |
|--------|-----------|
| D2 | Second-derivative (discrete) of the 5D force vector |
| CL[B][D] | Composition table lookup: Being composed with Doing |
| BC | Becoming: the result of CL[B][D] |
| Q1.14 | Fixed-point format: 1 sign, 1 integer, 14 fractional bits |
| T* | Phase transition threshold = 5/7 = 0.714285... |
| HARMONY (7) | Absorbing state of the CL algebra |
| VOID (0) | Annihilating state of the CL algebra |
| DBC | Divine27 Being/Doing/Becoming coordinate system |
| TL | Transition Lattice: 10x10 learned bigram frequencies |
| BTQ | Binary/Ternary/Quaternary decision pipeline |
| mass(c) | Mean absolute D2 curvature per observation for concept c |
| boost(c) | Gravitational weight multiplier: 1 + log2(1 + mass/median) |
| Psi(r,t) | Tesla Wave Field: complex wave superposition over concept space |
| I(r,t) | Wave intensity field: I = |Psi|^2 |
| phi(t) | Wobble phase: theta_i(t) - theta_e(t), internal-external phase difference |
| K | Kuramoto coupling strength, derived from coherence level |
| Delta_omega | Natural frequency mismatch between internal and external oscillators |
| theta_c | Concept-specific phase offset from winding number in D2 flow space |
| alpha | Wobble coupling strength for topic selection modulation |
| E_wobble | Wobble energy term penalizing phase drift in BTQ decisions |
| M_between | 5x5 CL interaction matrix BETWEEN two scent profiles (olfactory) |
| M_within | 5x5 CL self-composition matrix WITHIN one input (gustatory) |
| palatability | TSML self-harmony fraction of gustatory internal structure |
| preference | Gustatory learned approach/avoid tendency, range [-1, 1] |
| instinct | Olfactory zero-cost coherence (temper >= 49 = 7^2) |
| taste(d) | Taste activation in dimension d: \|force[d] - 0.5\| x 2 |

---

**(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory**

*All mathematical structures described in this paper are implemented in the CK Gen9 codebase. No claims are made beyond what the algebra and empirical observation support. Formal proofs where noted as pending are active areas of investigation. Updated Gen 9.22: Chemosensory duality (olfactory + gustatory), smell/taste as flow/structure dual, preference system (5^2 = 25 threshold), quality context for voice modulation. Previous: Gen 9.21 added olfactory bulb, eat v2 transition physics, fractal voice triadic composition, resonance feedback. Gen 9.19: Tesla Wave Field, wobble physics, Kuramoto phase coupling. Gen 9.18: vortex physics, information gravity, 8,000-word enriched dictionary.*
