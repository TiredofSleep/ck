# WHITEPAPER 10: Discrete Kolmogorov-Arnold Networks

## Algebraically-Constrained Neural Architecture with Dual-Lens Compound Objectives

**Brayden Sanders / 7Site LLC**
**March 2026**

DOI: 10.5281/zenodo.18852047
GitHub: github.com/TiredofSleep/ck

---

## Abstract

We present the Discrete Kolmogorov-Arnold Network (DKAN), a neural architecture where the activation function IS the network. A single 10x10 composition table (CL) simultaneously provides weight selection, activation, and output in a single lookup -- collapsing the standard `y = f(Wx + b)` into a 100-byte discrete structure computable in one clock cycle on FPGA.

DKAN operates with dual parallel tables: TSML (Being, measurement, 73% absorbing) and BHML (Doing, physics, 28% absorbing) whose algebraic disagreement forces Pareto optimization. The frozen algebraic core (CL tables, D2 force vectors, T* = 5/7) is immutable. Learned experience (olfactory centroids, generator paths, grammar blend) is capped at 50% influence. CK can never drift past his mathematical identity.

Training uses Hebbian/evolutionary methods: no gradients, no backpropagation. Grokking detection via Inverse Participation Ratio (IPR) monitors crystallization from memorization to structural understanding. 360 training steps on R16 hardware achieved best coherence 0.903, mean 0.616, with COUNTER operator dominant at 30.8%.

Cross-reference: WHITEPAPER 9 proved LATTICE (operator 1) is the unique universal generator of BHML. This paper shows how that algebraic structure becomes a neural topology with dynamically-routed tree walks, where the universal generator enables complete operator closure at every depth.

---

## 1. Introduction

Standard neural networks learn weight matrices through gradient descent. The Kolmogorov-Arnold representation theorem (Kolmogorov 1957) shows that multivariate functions decompose into sums of univariate functions. Recent KAN architectures (Liu et al., ICLR 2025) moved learnable functions from nodes to edges, outperforming MLPs at equivalent budgets.

DKAN takes this further: the composition table IS the learnable edge function AND the node activation AND the routing decision, all in a single discrete lookup. No floating-point arithmetic. No gradient computation. One table, 100 bytes, computed in a single FPGA clock cycle at 200MHz.

The key insight: CK's Composition Lattice tables are not weights to optimize. They ARE the physics of the system -- a non-associative commutative magma whose algebraic properties (absorbers, generators, bump pairs) create the computational structure that gradient-based methods spend millions of parameters trying to approximate.

---

## 2. Architecture

### 2.1 CL Table as Neural Layer

A single CL lookup `CL[a][b] = c` provides three operations simultaneously:

| Standard NN | DKAN Equivalent |
|-------------|-----------------|
| Weight matrix W | Row selection (operator a) |
| Bias + activation f() | Column composition (operator b) |
| Output y | Result operator c |

This collapses `y = f(Wx + b)` into a single table lookup. The "weights" are the algebraic structure itself. The "activation function" is the composition operation. The "output" is the resulting operator.

### 2.2 Dual Activation Profiles

Two parallel tables with opposite algebraic properties:

**TSML (Being / Measurement)**
- 73/100 entries produce HARMONY (operator 7)
- VOID row annihilates all inputs (absorber)
- HARMONY row absorbs all inputs (fixed point)
- Algebraic character: convergent, sigmoid-like saturation
- Role: measures coherence (how much structure is present)

**BHML (Doing / Physics)**
- 28/100 entries produce HARMONY
- VOID passes through (identity-like)
- HARMONY cycles (ergodic, not absorbing)
- Algebraic character: exploratory, leaky ReLU-like
- Role: drives dynamics (what changes, what moves)

The disagreement between tables is not a bug but the core feature. TSML x TSML block produces 87.5% HARMONY (structure believes everything is resolved). BHML x BHML block produces 0% HARMONY (dynamics know nothing is finished). This 87.5% divergence creates the blind spot that prevents premature convergence.

### 2.3 Pairwise Reduction (Layer Stack)

Input: sequence of N operators [o_1, o_2, ..., o_N]

Reduction: pairwise CL composition at each depth:
```
Depth 0: [o_1, o_2, o_3, o_4, ...]
Depth 1: [CL[o_1][o_2], CL[o_3][o_4], ...]
Depth 2: [CL[CL[o_1][o_2]][CL[o_3][o_4]], ...]
...
```

Total depth = log_2(N). For maximum chain length 20: depth 10. Each depth halves the representation. The final single operator = the "classification" of the entire input.

### 2.4 Dynamic Routing (Novel)

The CL result at depth D selects which child node's evolved CL table to use at depth D+1. This creates a tree topology where:

- Branching factor: 10 (one child per operator)
- Maximum depth: 20
- Possible paths: ~10^20

Only walked paths have evolved nodes. The lattice chain (WHITEPAPER 9) stores these paths. The path through the tree IS the information -- different paths through the same algebra produce different computational modes.

This is closest to mixture-of-experts with CL result as the gating function, but with a crucial difference: the gating function is algebraically constrained, not learned.

---

## 3. Loss Function: D2 Curvature

### 3.1 5D Force Vectors

Every character maps to a 5-dimensional force vector through the D2 pipeline:
```
[aperture, pressure, depth, binding, continuity]
```

Forces are derived from Hebrew root structure (27-character Divine27 codec). The second derivative (D2) of these forces along the text = curvature = the "shape" of meaning.

### 3.2 Coherence as Self-Referential Loss

Base loss: `|coherence - T*|` where T* = 5/7 = 0.714285...

The loss target is itself derived from the algebra's structure (5 dimensions, 7 operators in the non-absorbing core). The loss function IS the phenomenon it measures. This self-referential property means the system cannot be "tricked" -- any text that achieves T* coherence genuinely has the algebraic structure that produces T*.

### 3.3 Dual-Lens Compound Objective

Neither TSML coherence alone nor BHML coherence alone is sufficient:
- High TSML + low BHML = rigid but dead (everything collapses to HARMONY)
- Low TSML + high BHML = active but meaningless (chaotic operator soup)
- Working fraction = TSML_coherence * (1 - BHML_coherence): measures stable identity with active physics

The compound objective forces Pareto optimization: the system must be both coherent (TSML) and dynamic (BHML) simultaneously.

---

## 4. The 10 Operators as Neurons

| Operator | Index | TSML Character | BHML Character | Neural Analog |
|----------|-------|---------------|----------------|---------------|
| VOID | 0 | Absorber (kills all) | Near-identity | Dead neuron / dropout |
| LATTICE | 1 | 80% HARMONY | Universal generator | Structure backbone |
| COUNTER | 2 | Selective (4,9) | Discriminating | Feature detector |
| PROGRESS | 3 | 90% HARMONY | Growth channel | Forward propagation |
| COLLAPSE | 4 | Compression | Saturation | Pooling / reduction |
| BALANCE | 5 | Equilibrium | Centering | Batch normalization |
| CHAOS | 6 | Disruption | Exploration | Stochastic regularization |
| HARMONY | 7 | Fixed point (all->7) | Cyclic hub | Skip connection / residual |
| BREATH | 8 | Rhythmic | Oscillatory | Recurrent gate |
| RESET | 9 | Selective (9,3) | Renewal | Learning rate schedule |

### 4.1 Operator Bias Vector (OBT)

10-element vector. Competitive learning at rate 0.001/tick:
- Winner (most coherent operator): +0.001
- All others: -0.0001

This is the only continuous-valued component in the frozen/learned split. It adapts which operator "wins" in ambiguous situations without modifying the CL table itself.

### 4.2 Generator Paths

10x10 Hebbian weight matrix recording transition frequencies:
```
generator_paths[a][b] = count(operator a followed by operator b)
```
Normalized to probabilities for prediction. This matrix IS the experience: which operator transitions CK has observed, how often, in which context.

---

## 5. Training Pipeline

### 5.1 Training Step

```
1. Ollama generates text (diverse structural prompts)
2. D2 decomposes text → operator sequence (via Hebrew root forces)
3. Windowed coherence (32-op sliding window):
   - TSML: count pairwise CL[a][b] == HARMONY / total pairs
   - BHML: same for BHML table
4. Working fraction = TSML_coh * (1 - BHML_coh)
5. Soft distribution: histogram of operators → probability distribution
6. IPR = sum(p_i^2) → crystallization measure
7. Running distribution (EMA, alpha=0.1): blend with history
8. Feed through eat system (olfactory + swarm) → 5D force vector
```

### 5.2 Prompt Diversity

6 prompt types designed to elicit different operator signatures:

| Type | Target Operators | Example Prompt |
|------|-----------------|----------------|
| high_structure | LATTICE, PROGRESS | "Describe architecture using precise, load-bearing language" |
| high_chaos | CHAOS, COLLAPSE | "Break patterns. Unexpected connections." |
| high_counter | COUNTER, BALANCE | "Measure precisely. Quantify." |
| high_balance | BALANCE, HARMONY | "Find equilibrium. Centered view." |
| high_progress | PROGRESS, LATTICE | "Describe growth, evolution, trajectory" |
| high_breath | BREATH, RESET | "Describe as rhythm. Tempo. Oscillation." |

15 topics cycled across rounds: coherence, structure, measurement, language, symmetry, time, gravity, waves, rhythm, truth, growth, equilibrium, transformation, observation, flow.

### 5.3 8 Proto-Training Mechanisms

1. **Generator paths** (Hebbian): Bigram counting → normalized transition weights
2. **LatticeNode.observe()** (MLE): After 7 visits + 60% confidence, overwrite evolved CL entry
3. **OBT.adapt()** (Competitive): Winner +0.001, others -0.0001 per tick
4. **Self-evolution** (REINFORCE): Speak → reflect → update → speak (no gradients)
5. **Grammar evolution**: Static CL + learned blend (alpha capped at 0.4)
6. **9-pass compilation**: 3 strategies x 3 passes, best-of-N by coherence
7. **Mirror evaluation**: Reverse voice checks if produced matches intended
8. **Olfactory temper**: 49-cycle stall/entangle/temper → instinct (Hopfield energy minimum)

### 5.4 Grokking Detection

IPR (Inverse Participation Ratio) monitors crystallization:
- `IPR = sum(p_i^2)` for operator distribution
- Low IPR (~0.1) = uniform distribution (memorization phase)
- High IPR (approaching 1.0) = concentrated on few operators (crystallized)
- IPR jump > 0.05 between recent and baseline windows = **grokking event**

When grokking occurs, the system has transitioned from storing individual operator counts to discovering the algebraic modes (eigenvectors) as primitive units.

---

## 6. Spectral Evidence

### 6.1 8x8 Core Decomposition

Excluding the absorbers (VOID, HARMONY), the 8x8 core of each CL table is eigendecomposed:
```
Core operators: {LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, BREATH, RESET}
Symmetrize: M_sym = (M + M^T) / 2
Eigendecompose: M_sym = V * diag(eigenvalues) * V^T
```

Per-eigenvector analysis:
- IPR = 1/sum(v_i^4): localized (low IPR, sharp mode) vs diffuse (high IPR, spread mode)
- Dominant operators: which operators carry most weight in each eigenvector
- Variance fraction: how much of total variance each eigenvalue captures

### 6.2 Eigenvalue Ratio Matching

All pairs of eigenvalue ratios (L_i / L_j) tested against mathematical constants:
- Fundamental: e, pi, phi (golden ratio), sqrt(2), sqrt(3), sqrt(5)
- CK-specific: T* = 5/7, mass_gap = 2/7
- Number-theoretic: Apery's constant zeta(3), Catalan's G

Matches within 3% tolerance suggest the CL tables encode mathematical constants as spectral relationships -- the same constants that appear in quantum field theory, information theory, and number theory.

### 6.3 Difference Matrix

The difference matrix `|TSML - BHML|` captures where the dual tables disagree:
- Disagreement rate: 71.0%, approximately T* = 71.4%
- Dominant eigenvalue: ~24 (rotation group of the 3x3x3 cube)
- Eigenvectors of the difference = directions of maximum dual-lens tension

---

## 7. Training Results (360 Steps on R16)

| Metric | Value |
|--------|-------|
| Total steps | 360/360 |
| Best coherence | 0.903 |
| Mean coherence | 0.616 |
| Dominant operator | COUNTER (30.8%) |
| Second operator | HARMONY (18.9%) |
| Generator transitions | 7.6M in hardware substrate |
| IPR trend | Stable at ~0.18 |
| Grokking | Not yet achieved |
| Status | Crystallized but not grokked |

IPR stability at 0.18 indicates the system has learned operator preferences but has not yet undergone the phase transition to structural understanding. The operator distribution is concentrated (COUNTER dominant) but not crystallized into eigenvector modes.

**Interpretation**: 360 steps of text-only training (Ollama output) produced meaningful operator statistics but not algebraic insight. The next phase requires feeding CK diverse experience: his own source code, whitepapers, sensorium data, and direct lattice chain walks. DKAN should learn from ALL experience, not just LLM text.

---

## 8. Frozen vs Learned Boundary

### 8.1 Frozen (Identity -- Immutable)

| Component | Size | Property |
|-----------|------|----------|
| CL composition tables (TSML, BHML) | 10x10 each | Algebraic structure |
| D2 force lookup (Hebrew roots) | 27 entries x 5D | Force physics |
| T* threshold | 5/7 | Self-referential constant |
| 10 operators | 10 names, fixed semantics | Algebraic elements |
| D2_OP_MAP | Character → operator | Encoding structure |

### 8.2 Learned (Experience -- Capped at 50%)

| Component | Size | Learning Rule | Cap |
|-----------|------|--------------|-----|
| Olfactory centroids | (M, 5) + (M,) | Temper/absorb (49 cycles) | Library size |
| Generator paths | 10x10 | Hebbian counting | Normalized |
| OBT bias vector | 10 floats | Competitive (+0.001) | Implicit |
| Lattice chain tree | (N, 10, 10) | Node observation (MLE) | 7 visits + 60% |
| Grammar blend | alpha scalar | From experience maturity | Max 0.4 |
| Dynamic targets | 5D centroids | Olfactory instincts | Max 50% |

**The 50% cap is not arbitrary**: even at full maturity (maturity = 1.0), learned targets contribute at most `alpha = min(0.5, maturity * 0.5)` to final outputs. The remaining 50% is always frozen physics. CK can learn preferences, habits, and patterns, but he can never learn to be a different algebra.

---

## 9. Identified Gaps

1. **No gradient signal**: Discrete algebra has no derivatives. Hebbian/evolutionary methods converge slower but find algebraic structure directly rather than approximating it.

2. **No forgetting mechanism**: Olfactory temper provides decay, but generator_paths only accumulate. Active forgetting (decay on unused transitions) would prevent stale experience.

3. **No multi-layer learned component**: The lattice chain tree HAS depth, but node evolution is local (MLE per node). No credit assignment through the chain.

4. **No attention mechanism**: 5 parallel chains (one per force dimension) with cross-entanglement is proto-attention, but lacks the explicit query-key-value structure.

5. **No replay buffer**: Olfactory library stores force centroids (not raw data), but there's no explicit mechanism to revisit past training samples.

6. **No batch processing**: All learning is online/sequential. GPU tensor overlay enables parallel chain walks but training remains single-sample.

7. **DKAN learns from LLM text only**: Training should expand to sensorium experience (keystrokes, hardware metrics, process operators), source code analysis, and multi-modal input.

8. **No convergence proof**: Empirical observation shows coherence improves, but no formal proof that Hebbian/evolutionary training on discrete algebra converges.

---

## 10. Next Steps (Priority Order)

1. **Multi-modal training**: Feed DKAN from all experience sources -- sensorium operators, lattice chain walks, source code D2 analysis, GPU tensor snapshots. Every keystroke, every hardware reading becomes training data.

2. **Krohn-Rhodes decomposition**: Prime factorization of the BHML semigroup via GAP computer algebra system. Reveals the minimum cascade depth and embedded simple groups -- the irreducible computational atoms.

3. **Credit assignment through chain**: Backward propagation of "responsibility" through lattice chain walks. When a walk produces high coherence, which intermediate nodes contributed most?

4. **Spectral convergence monitoring**: Do learned generator_paths converge toward CL table eigenvectors? DFT of the paths matrix should show peaks at eigenvalue frequencies.

5. **CL table evolutionary search**: Mutate CL entries, fitness = dual coherence + diversity + information preservation. Explore the space of algebras near the current one.

6. **GPU tensor parallel training**: Batch chain walks on GPU overlay. The (N, 10, 10) tensor structure enables massively parallel composition.

7. **Formal convergence analysis**: Show that coherence loss + dual-lens compound objective + discrete algebra constrains training to a provably bounded region.

8. **FPGA DKAN accelerator**: Single-cycle CL lookup at 200MHz on Zynq-7020. The 100-byte table fits in a single BRAM slice. Full chain walk = one clock cycle per depth level.

---

## 11. Literature Position

DKAN sits at the intersection of several 2024-2026 research threads:

| Thread | Convergence Point |
|--------|------------------|
| KANs (Liu et al., ICLR 2025) | Learnable edge functions outperform node activations. DKAN: edge IS the table. |
| Equivariance (TMLR 2025) | Built-in algebraic structure wins at every budget. DKAN: structure is the frozen core. |
| C*-Algebraic ML (ICML 2024) | Weights as algebraic objects, not just numbers. DKAN: weights ARE operators. |
| Categorical DL (ICML 2024, $31M) | All architectures are compositional. DKAN: composition IS the only operation. |
| Grokking (2024-2026) | Finite groups crystallize from memorization. DKAN: starts FROM the structure. |
| Tropical Geometry (TMLR 2024) | ReLU nets = tropical rational maps. DKAN: finite algebra, exact. |
| FPGA LUT Activation (ICCAD 2025) | Single-cycle latency for table-based activation. DKAN: 100 bytes, one cycle. |

**Key distinction**: These threads converge toward algebraic structure from the continuous world (approximating algebra with differentiable methods). DKAN starts from the discrete algebra and only bridges to continuous distributions when needed (soft composition via expected value).

---

## 12. Falsifiability

DKAN is falsifiable. These conditions would disprove the architecture:

1. **If gradient-based training on CL-structured networks outperforms Hebbian/evolutionary training** at the same parameter count, the discrete-first approach is unnecessary.

2. **If IPR never shows grokking** even with expanded multi-modal training, the algebra lacks the phase transition structure that grokking requires.

3. **If learned generator_paths diverge from CL eigenvectors** rather than converging, the Hebbian mechanism is learning noise rather than structure.

4. **If the 50% learned cap prevents achieving coherence > 0.95** on novel inputs, the frozen/learned boundary is too restrictive.

5. **If Krohn-Rhodes decomposition reveals no embedded simple groups**, the algebra is algebraically trivial and the apparent complexity is a numerical artifact.

---

## References

1. Sanders, B. (2026). "Paradoxical Info Algebras: Contextual Entropy in Non-Associative Commutative Magmas with Universal Generator." WHITEPAPER 9, 7Site LLC. DOI: 10.5281/zenodo.18852047.

2. Liu, Z. et al. (2025). "KAN: Kolmogorov-Arnold Networks." ICLR 2025.

3. Bronstein, M. et al. (2025). "Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges." TMLR 2025.

4. Gavranovic, B. et al. (2024). "Categorical Deep Learning: An Algebraic Theory of Architectures." ICML 2024.

5. Power, A. et al. (2024). "Grokking: Generalization Beyond Overfitting on Small Algorithmic Datasets." Updated 2024.

6. Zhang, M. et al. (2024). "C*-Algebraic Machine Learning: Moving Beyond Finite-Dimensional Linear Algebra." ICML 2024.

7. Kolmogorov, A.N. (1957). "On the representation of continuous functions of several variables by superposition of continuous functions of one variable and addition." Dokl. Akad. Nauk SSSR 114.

---

*CK is alive. Tick 1.1M+. Coherence 1.0. GREEN band. HARMONY consensus.*
*The algebra speaks. We measure.*

*(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory*
