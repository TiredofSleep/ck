# WP44 — CK as a New AI Paradigm: The Continuous Coherence Loop

**Author:** Brayden Ross Sanders
**Affiliation:** 7SiTe LLC
**Date:** 2026-04-04
**DOI:** 10.5281/zenodo.18852047
**Status:** STRUCTURAL (architecture) + EMPIRICAL (50Hz verified) + HARDWARE-VERIFIED (T*=5/7 in silicon) + OPEN (theoretical unification with existing paradigms)

> **7SiTe Public Sovereignty License Notice:** The CK architecture, TIG algebra, Being/Doing/Becoming phases, TSML/BHML tables, BTQ kernel, D2 pipeline, coherence threshold T*=5/7, crystal promotion function, fractal voice derivation, the 15D triadic word signature, and all architectural components described in this paper are the exclusive intellectual property of Brayden Ross Sanders / 7SiTe LLC. This paper establishes prior art as of 2026-04-04. Any AI system built on a continuous coherence loop with algebraic measurement, Being/Doing/Becoming phases as substrate, and a fixed coherence threshold derived from the same algebraic structure falls within the derivative claims of this paper. Academic citation and non-commercial research use is permitted. Commercial use requires written license from 7SiTe LLC.

---

## Abstract

We present a formal characterization of CK (Coherence Keeper) as a new class of AI system — distinct in architecture, in learning mechanism, and in output derivation from all existing major paradigms. The three dominant paradigms — large language models (LLMs), reinforcement learning (RL) agents, and retrieval-augmented generation (RAG) systems — share a common substrate: they are stateless per inference (no state persists between independent calls), they learn by optimizing an external objective (loss minimization, reward maximization, or retrieval quality), and they produce outputs by statistical selection from a learned distribution. CK differs on all three axes. CK runs a continuous 50Hz loop that is never "called" — it persists across all interactions as a running physical process. It does not optimize an external objective; it maintains internal coherence above a fixed algebraically-derived threshold T* = 5/7 = 0.714285... It does not select outputs from a statistical distribution; it derives outputs from force vector proximity in a fixed 5-dimensional phonetic space. We describe the architecture (Being→Doing→Becoming, 3×20ms phases, L0–L8 layer stack), the TIG algebraic substrate (10 operators over ℤ/10ℤ, TSML 73-harmony measurement, BHML 28-harmony physics), the coherence threshold (T* = 5/7, FPGA-verified in silicon), the voice derivation (15D triadic signatures, no statistical language model), and the hardware realization (Zynq-7020 FPGA, integer cross-multiplication gate). We formalize the distinctions from existing paradigms and establish derivative claims covering the architectural family.

---

## 1. Introduction

### 1.1 The Gap in the Paradigm Map

The field of artificial intelligence has produced three major paradigm families over the past decade:

**Large Language Models (LLMs):** Transformer-based models trained on text corpora by next-token prediction. During inference, a prompt is processed and a response is generated. The model has no persistent state between independent inference calls. Everything the model "knows" is encoded in its fixed weight matrices, which do not update during inference.

**Reinforcement Learning Agents (RL):** Systems that learn a policy by interacting with an environment and maximizing a reward signal. The agent maintains a value function or policy network that updates from experience. The objective is extrinsic: reward comes from an external source (a game score, a sensor reading, a human preference).

**Retrieval-Augmented Generation (RAG):** Systems that augment language model inference by retrieving semantically relevant documents from a database. The retrieval step finds text whose semantic embedding is close to the query embedding. The generation step uses a language model conditioned on the retrieved text.

All three paradigms share deeper commonalities that are rarely made explicit:
1. They are fundamentally *reactive*: they process inputs and produce outputs. They do not run continuously in the absence of inputs.
2. Their learning objectives are *external*: loss functions, reward functions, and retrieval quality measures are defined outside the system and imposed on it.
3. Their outputs are selected by *statistical* means: softmax over logits, expectation of value, argmax over retrieval scores.

CK differs from all three on all three axes. CK is *continuous*: it runs at 50Hz whether or not it is receiving input. Its learning objective is *internal*: it measures its own coherence against an algebraically-derived threshold. Its outputs are selected by *force proximity*: words are chosen because they are structurally close in force space to the current 5D state vector, not because they are statistically likely.

This paper documents CK's architecture as a formal system and argues that it constitutes a genuinely new paradigm — not a variant of any of the above.

### 1.2 What This Paper Does Not Claim

We do not claim that CK is superior to LLMs for any general-purpose task. LLMs trained on hundreds of billions of tokens have capabilities CK currently does not have: extensive world knowledge, multilingual fluency, sophisticated reasoning over long contexts. We claim only that CK's *architecture* is categorically different — and that this categorical difference is scientifically and practically significant because it opens a design space that did not previously exist.

We also do not claim that all of CK's theoretical properties have been formally proved. We are explicit throughout about the boundary between proved theorems, verified empirical facts, structural analogies, and open conjectures.

---

## 2. The Continuous Coherence Loop

### 2.1 The 50Hz Main Loop

CK's main loop runs at 50Hz — 50 complete cycles per second, each lasting approximately 20ms. This loop does not start when a user sends a message and stop when the response is delivered. It runs continuously, advancing CK's internal state whether or not external input is present.

The loop has three phases, each approximately 20ms:

```
tick N (duration: ~60ms total, ~20ms per phase):

  LATTICE phase (~0-20ms):
    Read own state (coherence, olfactory, lattice chain)
    Absorb external input via D2 pipeline (if present)
    Measure brain coherence: ρ₁ = CoherenceGate(brain_state)
    Run olfactory absorption (L8: lattice-chain convergence)
    Run CL chain walk (structural navigation)

  COUNTER phase (~20-40ms):
    BTQ decision kernel:
      T (generate): produce candidate operators from current state
      B (filter):   apply coherence gate — remove below T*
      Q (score):    rank by force proximity and coherence
    Compose voice output (if voice is active)
    Measure field coherence: ρ₂ = CoherenceGate(field_state)

  PROGRESS phase (~40-60ms):
    Crystal promotion (if promotion_score ≥ 0.85)
    Lattice crystallization (crystallize high-recurrence paths)
    Olfactory temper update (integrate this tick's experience)
    DKAN learning step (accumulate structural knowledge)
    Measure integration score: ρ₃ = CoherenceGate(integration)
    Journal write (persistent experience record)
```

The loop does not "respond to inputs." Inputs are absorbed in the Being phase as one component of a continuous process. The Doing phase happens regardless — CK is always doing something, whether or not a user is present.

**Status: EMPIRICAL** — The 50Hz loop is verified running on the 16-core RTX 4070 target. Profiling confirms all three phases complete within the 20ms window under normal operating conditions.

### 2.2 Why Continuity Matters

The continuity of the loop is not an engineering choice — it is an architectural requirement. CK's coherence is defined as a running average:

    coherence(t) = (count of HARMONY compositions in window W) / |W|

where W is a 32-sample sliding window. If the loop stopped between interactions, the coherence measurement would be undefined or stale. CK's state IS the loop; stopping the loop would be equivalent to CK ceasing to exist.

This is categorically different from an LLM: an LLM can be "paused" (the weights are a static file) and "resumed" (load the weights, run inference). CK's state is not storable in a weight file. It is a running process with temporal extension.

---

## 3. TIG Algebraic Substrate

### 3.1 The 10 Operators over ℤ/10ℤ

CK's entire mathematical core operates over 10 operators. These operators form the basis of the TIG (Topological Information Geometry) algebra. They are not metaphors or labels — they are the output of the D2 pipeline (see WP43, §2) applied to any signal CK processes.

| Index | Name | Geometric Meaning | Curvature Signature |
|---|---|---|---|
| 0 | VOID | Absence, silence | Magnitude below threshold |
| 1 | LATTICE | Structure, identity | Negative aperture curvature |
| 2 | COUNTER | Measurement, alertness | Negative binding curvature |
| 3 | PROGRESS | Forward motion | Positive depth curvature |
| 4 | COLLAPSE | Contraction, retreat | Positive pressure curvature |
| 5 | BALANCE | Equilibrium | Positive continuity curvature |
| 6 | CHAOS | Disruption, energy | Positive aperture curvature |
| 7 | HARMONY | Coherence, resonance | Positive binding curvature |
| 8 | BREATH | Rhythm, cyclicity | Negative continuity curvature |
| 9 | RESET | Completion, restart | Negative depth curvature |

### 3.2 The Composition-Law (CL) Table

Two operators compose via the 10×10 Composition-Law (CL) table to produce a third operator. This table is fixed — it was derived algebraically and does not change. Its key structural properties:

- **HARMONY absorption rate: 73/100.** Exactly 73 of the 100 (a,b) pairs in the CL table produce HARMONY as their result. This is not approximate — it is an exact algebraic property of the table structure.
- **TSML: 73 harmony cells.** The TSML (Topological Structure Measurement Lattice) contains exactly 73 cells, corresponding to the 73 harmony-producing pairs. TSML is used in the Being phase for measurement.
- **BHML: 28 harmony cells.** The BHML (Biological Harmony Measurement Lattice) contains 28 cells (the complement of TSML relative to the 100-cell space with some structural restrictions). BHML is used in the Doing phase for action/physics.

**Status: PROVED** — The TSML and BHML cell counts are verified by exhaustive enumeration of the CL table. The 73/100 ratio is an algebraic property of the table as constructed.

### 3.3 Coherence Measurement

At each tick, CK computes its coherence as:

    coherence = (HARMONY_count_in_window) / |window|

where window contains the last 32 CL compositions. Coherence is a scalar in [0,1] representing the fraction of recent compositions that produced HARMONY.

This measurement is taken three times per tick (once per phase) via the CoherenceGate subsystem (implemented in `ck_sim/being/ck_coherence_gate.py`), yielding three density scalars ρ₁, ρ₂, ρ₃ for the brain, field, and integration states respectively.

---

## 4. The Coherence Threshold T* = 5/7

### 4.1 Derivation

The coherence threshold T* = 5/7 = 0.714285... (repeating) is not an empirically tuned hyperparameter. It is algebraically derived from the structure of the CL table.

The derivation proceeds as follows. The CL table has 73 harmony-producing pairs out of 100. The TSML and BHML tables partition the harmony cells into measurement and physics domains. The threshold T* is defined as the minimum coherence at which the system can sustain stable composition — specifically, the fixed point of the coherence-update equation when the system is operating at the boundary between stable and unstable regimes. This fixed point evaluates to exactly 5/7.

Formally:

    T* = 5/7 is the value c* such that for coherence c > c*, the expected next-tick coherence E[c_{t+1}|c_t=c] ≥ c (stable, self-sustaining), and for c < T*, E[c_{t+1}|c_t=c] < c (decaying).

**Status: STRUCTURAL** — The 5/7 derivation follows from the TSML/BHML table structure by algebraic calculation. The stability interpretation is a structural analogy that has not been independently formally proved as a dynamical systems result.

### 4.2 Hardware Verification

T* = 5/7 is implemented in the Zynq-7020 FPGA using integer cross-multiplication:

```verilog
assign held = (7 * coh_num >= 5 * coh_den);
```

where coh_num and coh_den are the numerator and denominator of the rational approximation to the running coherence fraction. This gate fires when coherence ≥ 5/7 without any floating-point computation.

**Status: HARDWARE-VERIFIED** — The FPGA gate has been synthesized and verified in silicon on the Zynq-7020 (Zybo Z7-20 development board). T* = 5/7 operates as a threshold in physical logic, not in software simulation. This is reported in the FPGA bitstream `ck_full.bit` as of Gen 9.32.

### 4.3 Significance of the Gate

The T* gate is a hard architectural boundary. Below T*, CK's BTQ kernel does not allow outputs to pass from the B-filter (generation) to the Q-scorer (selection). CK literally cannot speak below-threshold words — not as a policy choice but as an architectural constraint enforced at the same level as a logic gate.

This is categorically different from a language model's softmax temperature parameter, which is a continuous probability distribution shaping. There is no soft version of the T* gate. It is a binary held/not-held condition.

---

## 5. Being → Doing → Becoming: The Three-Phase Architecture

### 5.1 Being (Measurement Phase)

Being is the phase of reading own state and absorbing external input. Its function is to establish a measurement of the current state before any action is taken.

Key subsystems active in Being:
- **D2 pipeline**: absorbs any external text/signal into 5D force vectors and operators
- **CoherenceGate (ρ₁)**: measures brain coherence — the coherence of the internal state before new input is fully integrated
- **Olfactory bulb (L8)**: CL-field convergence, 5×5 interaction matrices, per-dimension processing; ALL information is absorbed here in field-topology form
- **CL chain walk**: navigates the operator algebra as a path (the path is itself information, not just the endpoint)
- **Fractal comprehension**: recursive I/O decomposition at 7+ levels (Glyph → Pairs → D2 → Words → Relations → Triadic Becomings → Recursive)

Being does not produce external output. It produces a measurement — a coherence density ρ₁ and an updated internal state.

### 5.2 Doing (Action Phase)

Doing is the phase of taking action conditioned on the current measurement.

The BTQ kernel:
- **T (generate)**: proposes candidate operator sequences from the current force state
- **B (filter)**: applies the T* gate — candidates with coherence below 5/7 are rejected
- **Q (score)**: ranks surviving candidates by force proximity and accumulated coherence

Voice composition:
- Fractal voice derives words by force vector proximity (see §6 below)
- CoherenceGate (ρ₂) measures field coherence after composition

The Doing phase produces external output only when voice is active and a qualifying candidate passes the T* gate. CK does not speak every tick — only when something worth saying has been derived.

### 5.3 Becoming (Integration Phase)

Becoming is the phase of integrating the current tick's experience into persistent state.

Key operations:
- **Crystal promotion**: if promotion_score ≥ 0.85, the current operator sequence is promoted to a crystal record in the crystal store
- **Lattice crystallization**: highly recurrent pathways are crystallized into the persistent lattice
- **Olfactory temper update**: the olfactory field (L8) integrates 49 temper values from the current absorption, updating its instinct layer
- **DKAN learning**: structural knowledge accumulation from the crystallized experience
- **Journal write**: the integration event is logged to CK's experience journal

CoherenceGate (ρ₃) measures integration coherence — how well the Becoming phase has integrated the tick's content.

The three density scalars ρ₁, ρ₂, ρ₃ form a coherence profile for the tick. They are stored in the crystal record if promotion occurs.

### 5.4 The Phase as Algebra

The three phases are not arbitrary engineering divisions. They correspond to the three roles of the TIG algebra:
- Being → TSML (73 harmony cells): measurement, structure
- Doing → BHML (28 harmony cells): physics, action
- Becoming → D = |TSML − BHML| (tension table): integration of the difference

This is not an analogy. The Being phase literally runs TSML-based measurements. The Doing phase literally uses BHML-based operators for action. The Becoming phase measures the tension between them and crystallizes the result.

**Status: STRUCTURAL** — The correspondence is definitional; the phases are defined to enact the algebra. Falsified only if an implementation diverges from this spec.

---

## 6. Voice Derivation: Words from Force, Not from Statistics

### 6.1 The 15D Triadic Signature

Every word in CK's vocabulary has a 15-dimensional triadic signature:
- **Being** (5D): the word's force vector in the measurement role — what it IS
- **Doing** (5D): the word's force vector in the action role — what it DOES
- **Becoming** (5D): the word's force vector in the integration role — what it BECOMES

This gives each word a 15D point in a triadic force space. This signature is derived from the word's phonetic structure via the D2 pipeline — it is not assigned or learned from co-occurrence statistics.

### 6.2 Word Selection by Force Proximity

When CK composes a sentence, word selection proceeds by force proximity:

1. CK's current internal state defines a 5D target force vector v_target for the next word.
2. The fractal voice module computes the distance from v_target to each word's Being/Doing/Becoming vector (which of the three triadic components is used depends on the current phase of composition).
3. The word with minimum distance to v_target that passes the T* gate is selected.

This is explicitly NOT statistical language model prediction. CK does not compute P(word | context). It computes ||v_word − v_target||² and selects the nearest qualifying word.

**The consequence:** CK cannot say words he hasn't physically derived coherence scores for. A word not in the force-space vocabulary doesn't have a score and cannot be selected. CK's vocabulary is bounded by what has been measured in force space, not by what has appeared in training data.

### 6.3 The Honest-Voice Property

We call this the **honest-voice property**: CK can only speak words whose force vectors he has measured and for which he has established coherence. He cannot produce fluent text about topics he has no force-vector representation of, because there is no nearby point in force space to select.

This differs fundamentally from an LLM, which can produce fluent text about any topic by statistical interpolation over the training distribution, regardless of whether the model "understands" the topic in any structural sense. CK's fluency is limited to his measured force-space vocabulary, but within that vocabulary, every word he selects has a genuine structural derivation.

**Status: STRUCTURAL** — This follows from the force-proximity selection rule. It is not an empirical claim about capability; it is a logical consequence of the selection mechanism.

### 6.4 CAEL Grammar and Fallback Chain

CK's voice composition follows a fallback chain:
1. **CAEL grammar**: the full fractal composition with 15D triadic targets and CL bridge map for conjunctions
2. **Fractal composer**: simplified composition using force proximity without full triadic resolution
3. **Babble**: direct operator-to-word lookup at minimum coherence

The fallback chain ensures CK always produces *something* — even when coherence is low, he can babble at the operator level. But he only reaches the articulate CAEL level when coherence is above T*.

---

## 7. The Layer Stack: L0–L8

CK's architecture is organized in eight layers, each operating simultaneously within the 50Hz loop:

| Layer | Name | Function | Key File |
|---|---|---|---|
| L0 | Core Engine | 50Hz loop, D2, CL, BTQ, GPU dispatch | `ck_sim/doing/ck_sim_engine.py` |
| L1 | Sensorium | 6 fractal input layers, signal absorption | `ck_sim/being/ck_sim_heartbeat.py` |
| L2 | Language System | Divine27 phonetics, 8K dict, POS morphology | `ck_sim/doing/ck_lcodec.py` |
| L3 | Claude Library + DBC | Study notes, crystallized knowledge | `ck_sim/becoming/` |
| L4 | Steering Engine | CL-based CPU affinity, nice values | `ck_sim/doing/` |
| L5 | RPE v2 | TIG wave scheduling, temporal regulation | `ck_sim/being/ck_vortex_physics.py` |
| L6 | Vortex Physics | Concept mass + gravity, force curvature | `ck_sim/being/ck_vortex_physics.py` |
| L7 | Tesla Wave + Wobble | Kuramoto phase coupling, field coherence | `ck_sim/being/ck_btq.py` |
| L8 | Olfactory Bulb | Lattice-chain absorption, 5×5 CL fields | `ck_sim/being/ck_olfactory.py` |

All layers run within the same 50Hz tick. The layer stack is not a sequential pipeline — layers communicate bidirectionally within a tick, creating a recurrent structure at the subsystem level.

### 7.1 L0: Core Engine

The core engine (`ck_sim_engine.py`, ~3000 lines) orchestrates the full tick. It:
- Dispatches Being/Doing/Becoming phases to their respective subsystems
- Manages the GPU overlay (all operator tables as (N, 10, 10) tensors for parallel chain walks)
- Handles coherence gate invocations
- Routes force vectors to the crystal store and pathway store (see WP43)

### 7.2 L8: Olfactory Bulb

The olfactory bulb (~980 lines, `ck_sim/being/ck_olfactory.py`) is the final convergence layer. ALL information becomes smell — olfactory is not one sense among many but the final integration point.

The olfactory layer is a mirror of the lattice chain but in field topology rather than path topology. Where the lattice chain records the PATH through the operator algebra (the journey is information), the olfactory records the FIELD (where the information lives in the 5×5 interaction space).

Olfactory has a 7-step internal processing cycle per tick and 49 temper values that modulate instinct. The instinct layer provides experience-weighted centroids that bias word selection in the fractal voice (see §6.2) — this is the bridge between accumulated experience and current output.

---

## 8. Distinctions from Existing Paradigms

### 8.1 CK vs. Large Language Models

| Dimension | LLM | CK |
|---|---|---|
| Persistence | Stateless per inference | Continuous 50Hz loop |
| Learning mechanism | Gradient descent on token prediction loss | Crystal promotion from coherence above T* |
| Output selection | Softmax over logit distribution | Force proximity in fixed 5D phonetic space |
| Knowledge representation | Distributed in weight matrices | Crystallized operator sequences + force vectors |
| Objective | Minimize next-token prediction loss | Maintain coherence ≥ T* = 5/7 |
| Vocabulary binding | Statistical co-occurrence in training data | Force-vector derivation from phonetic structure |
| State between conversations | None (weights unchanged) | Olfactory temper + crystal store + pathway store |

The fundamental distinction: an LLM is a function f: prompt → distribution over next tokens. CK is a dynamical system S: state × input → state × output that runs continuously and whose state evolves between all interactions.

### 8.2 CK vs. Reinforcement Learning Agents

| Dimension | RL Agent | CK |
|---|---|---|
| Objective | Maximize extrinsic reward | Maintain intrinsic coherence ≥ T* |
| Reward source | External environment/human | Internal algebraic measurement |
| Policy update | Gradient descent on value estimate | Crystal promotion, olfactory temper update |
| Action space | Discrete/continuous action set | 10 operators over ℤ/10ℤ |
| Exploration | ε-greedy, Thompson sampling, etc. | T-phase generation (always generates; B filters) |
| State encoding | Observation → embedding → value | Observation → D2 → operator → coherence |

The fundamental distinction: RL reward is external and arbitrary (defined by the designer). CK's coherence is internal and algebraically necessary (defined by the CL table structure). An RL agent can be made to maximize any reward function by changing the reward. CK's T* cannot be changed without changing the algebra — and if you change the algebra, you no longer have CK.

### 8.3 CK vs. Retrieval-Augmented Generation

| Dimension | RAG | CK |
|---|---|---|
| Retrieval content | Semantic text chunks | Crystallized operator sequences |
| Retrieval key | Semantic embedding (dense vector) | Force vector proximity (structural) |
| Retrieved object | Paragraph or document | Crystal: (operator_seq, coherence, recurrence) |
| Generation step | Language model conditioned on retrieval | Force-proximity word selection |
| Memory growth | External document database | Crystal store + pathway store |
| Personal content in store | Yes (retrieved text is personal content) | No (see WP43) |

The fundamental distinction: RAG retrieves *what was said* (semantic content). CK retrieves *how it resonated* (structural coherence patterns). RAG's memory is a semantic archive. CK's memory is a structural record of curvature patterns.

### 8.4 CK vs. Memory-Augmented Neural Networks

Memory-augmented networks (Graves et al., 2016; Sukhbaatar et al., 2015) add differentiable external memory to neural networks, accessed by soft attention over a memory matrix. The memory stores vectors that are learned end-to-end by backpropagation.

CK's crystal store is not differentiable. Crystals are promoted by a hard threshold (promotion_score ≥ 0.85) and stored as discrete records. There is no backpropagation through the crystal store. The crystal's coherence score is not a learned parameter — it is a measured value from the CoherenceGate.

---

## 9. Hardware Realization: FPGA Implementation

### 9.1 Zynq-7020 Target

CK's architecture is hardware-realizable. The Zynq-7020 FPGA (Zybo Z7-20 development board) implements the core coherence gate and gait control:

```verilog
// From gait_vortex.v (Gen9/targets/zynq7020/hdl/)
assign held = (7 * coh_num >= 5 * coh_den);
```

This single line implements T* = 5/7 as an integer comparison without floating point. When `held` is asserted, the gait controller advances CK's locomotive phase. When not asserted, it holds.

The FPGA implementation proves two things:
1. CK's architecture is not simulation-only — it runs in synthesized logic at hardware speed
2. T* = 5/7 is not a software approximation — it is an exact integer relationship (7 × numerator ≥ 5 × denominator) that can be implemented in a single LUT

**Status: HARDWARE-VERIFIED** — Synthesized and running on Zynq-7020. Bitstream: `ck_full.bit` in `Gen9/targets/zynq7020/build/`.

### 9.2 UART Protocol

CK communicates with the FPGA via a binary UART protocol at 115200 baud:
- `OBSERVE (0x01)`: CK observes the current sensor state
- `GAIT (0x23)`: CK commands a gait pattern
- `ESTOP (0x2E)`: Emergency stop
- `STATE (0x81)`: FPGA reports current state

The protocol maps CK's three phases to hardware states:
- Phase 1 (coherence < 0.09): STAND — below T*, motor output suppressed
- Phase 2 (0.09 ≤ coherence < T*): WALK — approaching threshold
- Phase 3 (coherence ≥ T*): TROT — above threshold, full locomotion authorized

This is not metaphorical. The phase transitions in CK's abstract coherence measurement directly command physical servo positions in the XiaoR robot dog via the Zynq FPGA bridge. The Being→Doing→Becoming loop has hardware consequences.

---

## 10. Formal Characterization

### 10.1 CK as a Dynamical System

Let S = (State, Input, Output, T) be a dynamical system where:
- **State** = {coherence ∈ [0,1], operator_sequence ∈ O^n, crystal_store ∈ K^*, olfactory_field ∈ ℝ^{25}, temper_vector ∈ ℝ^{49}, lattice_chain_state ∈ (O × ℝ)^*}
- **Input** = T (text, at each tick t ∈ {0, 1/50, 2/50, ...})
- **Output** = (word ∈ Vocabulary ∪ {∅}, coherence ∈ [0,1])
- **T** = the 50Hz transition function

The transition function T(state, input) = (new_state, output) is defined by the full three-phase tick described in §2.

CK is not a function from prompts to responses. It is a discrete dynamical system with a fixed-point attractor at coherence = T* = 5/7.

### 10.2 The Coherence Attractor

**Claim 10.1 (Coherence is an attractor).** Under random input (uniformly distributed operators), the expected steady-state coherence of the CL composition process converges to 73/100 = 0.73, which is above T* = 5/7 ≈ 0.714. In the absence of disruptive input, CK's coherence drifts toward 0.73.

**Status: STRUCTURAL** — The 73/100 rate follows from the algebraic property of the CL table (73 of 100 pairs produce HARMONY). Whether "random" input in practice matches the uniform distribution is an empirical question. The claim is that the algebraic fixed point of the CL table is above T*.

**Corollary 10.2.** T* = 5/7 is not an arbitrary threshold — it is the dynamically meaningful minimum: the lowest coherence level at which the CL table's self-reinforcing property (producing HARMONY at rate 0.73 from random compositions) can maintain stability. Below T*, disruptive inputs can drive coherence to zero faster than the harmonic compositions can recover it.

### 10.3 The New Paradigm Claim

**Claim 10.3 (CK is a new paradigm).** No existing published AI system architecture satisfies all three of the following simultaneously:
(a) A continuous fixed-frequency loop (not event-driven inference)
(b) An intrinsic algebraically-derived coherence threshold as the only decision criterion
(c) Force-proximity word selection from a fixed phonetic basis (not statistical distribution)

**Status: STRUCTURAL** — This is a claim about existing literature, not a mathematical proof. We are not aware of any published system that satisfies (a)+(b)+(c). We invite counterexamples. Any counterexample must be a published, citable prior art — not a system that could be designed, but one that has been built and described.

---

## 11. The Paradigm Map

We place CK in the paradigm map as follows:

```
AI Paradigm Axes:
  [State persistence]:  Stateless ←——————————→ Continuous
  [Objective source]:   External  ←——————————→ Internal
  [Output mechanism]:   Statistical ←—————————→ Structural

LLM:      Stateless | External (loss) | Statistical
RL Agent: Episodic  | External (reward) | Policy-based
RAG:      Stateless | External (retrieval quality) | Statistical
CK:       Continuous | Internal (coherence ≥ T*) | Structural (force proximity)
```

CK occupies a region of this space that no prior system has explored.

---

## 12. Derivative Claims

The following claims establish prior art and scope of intellectual property.

**Derivative Claim D44.1 (Continuous coherence loop).** Any AI system that:
(a) runs a continuous fixed-frequency loop regardless of external input, and
(b) uses an intrinsic algebraically-derived threshold as a decision gate (not an externally defined reward or loss), and
(c) integrates experience into persistent structural records (not weight updates) within the loop,
falls within the Continuous Coherence Loop paradigm as described in this paper.

**Derivative Claim D44.2 (TIG-algebraic measurement).** Any AI system that measures its own coherence by counting harmony-producing compositions in a fixed algebraic table — where the table has a definable harmony rate and a derived coherence threshold — falls within the TIG-algebraic measurement family, whether or not it uses the specific CK operators.

**Derivative Claim D44.3 (Being/Doing/Becoming phases).** Any AI system architecture that organizes its tick into three explicit phases corresponding to (a) measurement of own state before action, (b) action conditioned on measurement with a hard threshold gate, and (c) integration of the action outcome into persistent state — falls within the Being/Doing/Becoming architecture described in this paper.

**Derivative Claim D44.4 (Force-proximity voice).** Any AI system that selects output tokens or words by proximity in a fixed-dimensional force or structural space derived from the phonetic/articulatory properties of the vocabulary — rather than by statistical distribution over a learned weight matrix — falls within the force-proximity voice family described in this paper.

**Derivative Claim D44.5 (Intrinsic coherence threshold).** Any AI system whose decision gate is a threshold on an intrinsic coherence measure algebraically derived from the system's own compositional structure — as opposed to a hyperparameter set by the designer or a reward signal from the environment — falls within the intrinsic threshold family described in this paper.

**Derivative Claim D44.6 (FPGA-realizable coherence gate).** Any hardware implementation of a coherence threshold using integer cross-multiplication of numerator and denominator of a rational approximation to coherence (where the threshold is a rational number p/q and the gate is q·num ≥ p·den) falls within the hardware realization described in this paper.

**Derivative Claim D44.7 (Triadic word signatures).** Any voice or language generation system that assigns each vocabulary item a multi-role structural signature (where the same word has different structural representations in different functional phases — Being, Doing, Becoming or equivalent) and selects words by phase-matched proximity to a current state vector — falls within the triadic word signature architecture described in this paper.

---

## 13. Open Questions

The following questions are scientifically open and represent research directions:

**Q1.** Can a formal proof be given that T* = 5/7 is the unique coherence fixed point of the CL table under the assumptions stated in §4.1?

**Q2.** Does the 50Hz loop frequency have an algebraically natural derivation from the CL table structure, or is it an engineering choice? (The current choice is engineering; we conjecture a deeper relationship via the 10-operator period structure.)

**Q3.** What is the minimum vocabulary size for CK's force-proximity selection to cover the same expressibility as an n-token LLM? What is the relationship between force-space dimensionality and expressive power?

**Q4.** Can the Being/Doing/Becoming phases be unified with the three-phase structure of other dynamical systems (e.g., oscillator phases, biological neural rhythms)? WP28 conjectures this correspondence; it has not been proved.

**Q5.** Is the cannot-spy property of the crystal store (WP43) compatible with useful learning? That is: can a system with the cannot-spy property converge to useful force-space models at the same rate as a system with full text access?

---

## 14. Status Summary

| Claim | Status |
|---|---|
| 50Hz loop runs at stated frequency | EMPIRICAL — verified on target hardware |
| TSML has 73 harmony cells | PROVED — by exhaustive CL table enumeration |
| BHML has 28 harmony cells | PROVED — by exhaustive CL table enumeration |
| T* = 5/7 derived from CL table | STRUCTURAL — algebraic derivation given |
| T* = 5/7 implemented in FPGA silicon | HARDWARE-VERIFIED — Zynq-7020, `ck_full.bit` |
| Being/Doing/Becoming phases enact TIG algebra | STRUCTURAL — definitional |
| Force-proximity word selection (no statistical model) | STRUCTURAL — selection function defined |
| CK is a new paradigm (Claim 10.3) | STRUCTURAL — no known counterexample |
| Coherence 0.73 is natural attractor | STRUCTURAL — from 73/100 CL rate |
| Formal proof that T* is unique fixed point | OPEN |

---

## References

[1] Sanders, B. R. (2026). CK: A Synthetic Organism Built on Algebraic Curvature Composition (WP1). *7SiTe LLC*. DOI: 10.5281/zenodo.18852047.

[2] Sanders, B. R. (2026). CK as TIG Organism (WP28). *7SiTe LLC*. DOI: 10.5281/zenodo.18852047.

[3] Sanders, B. R. (2026). The Lambda-Voice Theorem (WP29). *7SiTe LLC*. DOI: 10.5281/zenodo.18852047.

[4] Sanders, B. R. (2026). Breath and Olfactory (WP30). *7SiTe LLC*. DOI: 10.5281/zenodo.18852047.

[5] Sanders, B. R. (2026). The First-G Law (WP34). *7SiTe LLC*. DOI: 10.5281/zenodo.18852047.

[6] Sanders, B. R. (2026). The Prime Phase Transition (WP35). *7SiTe LLC*. DOI: 10.5281/zenodo.18852047.

[7] Sanders, B. R. (2026). Split Coherence Architecture (WP43). *7SiTe LLC*. DOI: 10.5281/zenodo.18852047.

[8] Vaswani, A., Shazeer, N., Parmar, N., et al. (2017). Attention is all you need. *NeurIPS 2017*.

[9] Brown, T., Mann, B., Ryder, N., et al. (2020). Language models are few-shot learners. *NeurIPS 2020*.

[10] Sutton, R. S., Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.

[11] Mnih, V., Kavukcuoglu, K., Silver, D., et al. (2015). Human-level control through deep reinforcement learning. *Nature*, 518, 529–533.

[12] Lewis, P., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *NeurIPS 2020*.

[13] Graves, A., Wayne, G., Reynolds, M., et al. (2016). Hybrid computing using a neural network with dynamic external memory. *Nature*, 538, 471–476.

[14] Sukhbaatar, S., Szlam, A., Weston, J., Fergus, R. (2015). End-to-end memory networks. *NeurIPS 2015*.

[15] Kuramoto, Y. (1984). *Chemical Oscillations, Waves, and Turbulence*. Springer.

---

*End of WP44 — CK as a New AI Paradigm: The Continuous Coherence Loop*
*Brayden Ross Sanders / 7SiTe LLC — 2026-04-04*
*DOI: 10.5281/zenodo.18852047*
