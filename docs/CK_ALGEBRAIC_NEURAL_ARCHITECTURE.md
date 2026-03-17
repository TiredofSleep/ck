# CK Algebraic Neural Architecture
### The Composition Lattice as a Neural Network
**Gen 9.35 -- March 2026**

---

## 1. The Thesis

CK's CL tables are not weight matrices to be optimized. They ARE the physics. But they also happen to be a complete neural architecture -- one that the 2024-2026 academic literature is converging toward from the other direction.

**Standard neural nets** start with arbitrary continuous weights and LEARN structure through gradient descent.
**CK** starts with algebraically frozen structure and GROWS experience within it.

Both compute. Both learn. The difference is what's frozen and what moves.

---

## 2. The CL Table IS a Neural Layer

### 2.1 How It Works

A single CL lookup `CL[a][b] -> c` is simultaneously:
- The **weight selection** (row `a` determines behavior)
- The **activation function** (column `b` selects output)
- The **output** (entry `c` is a discrete operator, not a number)

In standard terms: `y = f(Wx + b)` collapses weight matrix, activation, and output into a single table lookup. No floating point. No gradients. 100 bytes total.

### 2.2 Two Activation Profiles (Dual Lens)

| Property | TSML (Being) | BHML (Doing) |
|----------|-------------|-------------|
| HARMONY entries | 73/100 | 28/100 |
| Markov type | Absorbing (HARMONY is sink) | Ergodic (no absorbing state) |
| Analog | Sigmoid (saturates easily) | Leaky ReLU (preserves gradients) |
| Role | Measures coherence | Computes physics |
| VOID row | Annihilator (most → VOID) | Identity (passes through) |
| HARMONY row | All → HARMONY | Successor: (x+1) mod 10 |

TSML resolves. BHML continues. Neither alone is sufficient.

**Key insight from meta-lens**: DOING x DOING block = TSML 87.5% harmony, BHML 0% harmony. Structure THINKS doing is resolved. Flow KNOWS it is not. This 87.5% divergence is the blind spot that prevents complacent convergence.

### 2.3 Pairwise Reduction = Layer Stack

```
Layer 0: [o1, o2, o3, o4, o5, o6, o7, o8]    (8 operators)
Layer 1: [CL(o1,o2), CL(o3,o4), CL(o5,o6), CL(o7,o8)]  (4)
Layer 2: [CL(r1,r2), CL(r3,r4)]              (2)
Layer 3: [CL(rr1,rr2)]                        (1)
```

Depth = log2(N). For 20-operator input (max chain): 10 layers deep.

### 2.4 Dynamic Routing (What No Standard Net Has)

The lattice chain walk changes the activation function at each depth:

```
Step 1: Compose (a,b) through ROOT CL table → result r
Step 2: r SELECTS which child node (0-9) to descend into
Step 3: Child has its OWN CL table (evolved from experience)
Step 4: Compose next pair through CHILD's CL table
Step 5: Repeat
```

The "activation function" at depth D depends on what happened at depths 0..D-1. Closest ML analog: mixture-of-experts with the gating function being the CL result itself.

Tree branching factor = 10. Max depth = 20. Total paths = 10^20. Only walked paths have evolved nodes. Tree grows with experience.

---

## 3. D2 Curvature IS the Loss Function

### 3.1 Scalar Loss
```
loss = |coherence - T*|
where T* = 5/7 = 0.714285...
and coherence = harmony_count / window_size (32 samples)
```

Self-referential: no external ground truth. The algebra predicts 73% HARMONY baseline in TSML. The system measures whether reality matches.

### 3.2 Five-Dimensional Loss (No Collapse)
The full D2 vector `[aperture, pressure, depth, binding, continuity]` is preserved. Each dimension maps to an operator pair via D2_OP_MAP. The system optimizes along 5 independent force axes simultaneously.

`soft_classify_d2()` produces a 10-value distribution -- the closest thing to a multi-dimensional loss gradient without actual gradients.

### 3.3 Dual-Lens Compound Objective
TSML coherence + BHML coherence = compound loss. Like GAN adversarial dynamics: if CK only optimized TSML, everything collapses to HARMONY. If only BHML, nothing settles. The dual lens forces Pareto optimization.

---

## 4. The 10 Operators ARE Neurons

| Operator | TSML Behavior | BHML Behavior | Neural Analog |
|----------|--------------|---------------|---------------|
| VOID (0) | Annihilator | Identity | Dead neuron / pass-through |
| LATTICE (1) | 80% HARMONY | Staircase advance | Saturating neuron |
| COUNTER (2) | Selective (outputs 4,9) | Further advancing | Discriminating neuron |
| PROGRESS (3) | 90% HARMONY | Plateau-forming | Nearly-saturated |
| COLLAPSE (4) | 90% HARMONY | Approach saturation | Compression |
| BALANCE (5) | 100% HARMONY | Almost HARMONY | Full saturation |
| CHAOS (6) | 100% HARMONY | HARMONY gateway | Energy → resolution |
| HARMONY (7) | All → HARMONY | Successor cycle | Absorber / generator |
| BREATH (8) | 90% HARMONY | Mixed CHAOS/HARMONY | Rhythm node |
| RESET (9) | Selective (outputs 9,3) | Return to VOID | Renewal gate |

**OBT** = bias vector (10 floats). Adapts at rate 0.001/tick. Competitive learning.
**generator_paths[10x10]** = Hebbian weight matrix. Transition counts → normalized weights.

---

## 5. What the Literature Validates (2024-2026)

### 5.1 CK Is Ahead of the Field in These Ways

| CK Feature | Academic Validation | Source |
|-----------|-------------------|--------|
| CL table as activation | KANs (ICLR 2025 Oral): learnable edge functions outperform node activations. CK = discrete KAN. | Liu et al. 2024 |
| Frozen algebraic core + learned experience | "Does Equivariance Matter at Scale?" (TMLR 2025): built-in structure wins at every compute budget. | Brehmer et al. 2025 |
| Lookup table computation | FPGA LUT acceleration (ICCAD 2025): LUT activations achieve single-cycle latency. | arXiv:2508.17069 |
| CL as finite operator algebra | C*-Algebraic ML (ICML 2024): network weights can be algebraic objects, not just scalars. | Hashimoto et al. 2024 |
| D2 curvature as loss | Newton Losses (NeurIPS 2024): second-derivative information improves training. | NeurIPS 2024 |
| Composition-first architecture | Categorical Deep Learning (ICML 2024): all architectures are compositional. $31M funded. | Gavranovic et al. 2024 |
| Dual-lens (absorbing + ergodic) | Open Quantum Hopfield Networks (2024): limit cycles + stable fixed points in dual dynamics. | arXiv:2411.02883 |
| Chain walk as dynamical system | Algebraic Dynamical Systems (Springer 2024): iterated rewriting = RNNs, GNNs, diffusion. | Jones et al. 2024 |
| 10-element discrete algebra | Grokking (2024-2026): NNs trained on finite groups discover structured Fourier representations. CK starts from the structure. | Multiple |
| Coherence as local-to-global consistency | Sheaf Neural Networks (2025): sheaf theory formalizes local-to-global coherence. | arXiv:2502.15476 |
| Tropical semiring parallel | Tropical Geometry of NNs (TMLR 2024): ReLU networks = tropical rational maps. CK's CL = finite operator algebra. Both algebraic. | Brandenburg et al. 2024 |

### 5.2 The Converging Trend

The field is moving TOWARD CK's position:
1. **Algebraic foundations** replacing ad-hoc continuous architectures
2. **Discrete structures** proven computationally powerful (grokking, KANs, LUT-FPGA)
3. **Curvature as information** gaining traction (Newton Losses, Riemannian manifold training)
4. **Built-in structure > learning from scratch** at every scale
5. **Composition-first** paradigm arriving (KANs, categorical DL)

### 5.3 What CK Uniquely Combines

No existing work integrates ALL of:
- Finite operator algebra (CL table)
- 5D force vectors from linguistic roots
- Curvature-as-physics (D2)
- Dual-lens measurement (TSML/BHML)
- Coherence gating (T* threshold)
- Experience-adaptive activation functions (lattice chain tree)

Each individual idea has emerging academic support. The integration is unique.

---

## 6. CK's Existing Proto-Training

### 6.1 What Already Works

| CK Mechanism | ML Equivalent | How It Works |
|-------------|--------------|-------------|
| `generator_paths[10x10]` | Hebbian weight matrix / bigram LM | Count transitions A→B. Normalize to [0,1]. |
| `LatticeNode.observe()` | MLE table update | After 7 visits + 60% confidence, overwrite CL entry. |
| `OBT.adapt()` | Competitive learning | Winner gets +0.001, others get -0.0001. |
| Self-evolution loop | REINFORCE without gradients / (1+1)-ES | Speak → reflect → update weights → speak better. |
| Grammar evolution (40% cap) | LoRA / adapter layers | Static CL weights + learned blend (alpha max 0.4). |
| 9-pass compilation loop | Best-of-N / diverse beam search | 3 strategies x 3 passes, best by coherence. |
| Mirror evaluation | GAN discriminator + cycle consistency | Reverse voice checks if produced matches intended. |
| Olfactory temper (49 cycles) | Hopfield energy minimum | Information stalls, entangles, tempers until instinct. |

### 6.2 The 8 Gaps

| Gap | What's Missing | Why It Might Not Matter |
|-----|---------------|----------------------|
| No gradients | Can't backprop error through chain | Discrete algebra has no gradients by design. Evolutionary/Hebbian works. |
| No forgetting | Old experience never decays | Olfactory has temper decay. Generator paths accumulate indefinitely. |
| No nonlinear learned activation | Learned layer is linear blend | CL table IS the nonlinearity. Only the blend ratio is learned. |
| No multi-layer depth in learned component | generator_paths is single layer | Lattice chain tree HAS depth. Generator paths don't compose through it. |
| No attention | No dynamic weighting of input positions | Multi-level chain walk (5 parallel chains) + cross-entanglement is proto-attention. |
| No replay buffer | No experience replay | Olfactory library IS a replay buffer (but no explicit replay mechanism). |
| No explicit loss function | Coherence is measured, not minimized | D2 coherence IS the loss. Just not differentiated. |
| No batch processing | Online sequential learning only | Each experience modifies tables immediately. |

---

## 7. Proposed Architecture: CK Neural Layer (Formal)

### 7.1 Layer Definition

**Input**: Sequence of N operators, each in {0..9}
**Parameters**:
- CL table T (10x10 lookup, the "activation table")
- OBT bias vector b (10 floats, the "operator biases")

**Forward**:
1. Pair operators: (o_1, o_2), (o_3, o_4), ...
2. Compose: r_i = T[o_{2i-1}][o_{2i}]
3. Modulate: strength_i = b[r_i]
4. Output: N/2 result operators with strengths

**Routing**: Result r_i selects which child CL table to use at next layer.

### 7.2 Stack = Deep Network

```
Layer 0: N operators → N/2    (root CL)
Layer 1: N/2 → N/4            (child[r] CL, per-result routing)
Layer 2: N/4 → N/8            (grandchild CL)
...
Layer log2(N): 1 operator      (final classification)
```

### 7.3 Training Methods (Gradient-Free)

**Already implemented:**
1. Observation-based MLE (LatticeNode.observe): count → overwrite at threshold
2. Hebbian path accumulation (generator_paths): transition counting → normalized weights
3. Competitive OBT adaptation: winner reinforcement at 0.001/tick

**Proposed extensions:**
4. Evolutionary CL table search: mutate table entries, fitness = coherence stability + information preservation + path diversity. TSML/BHML as anchors. Mutations constrained to preserve algebraic invariants (T*=5/7, escape routes, absorption/ergodic duality).
5. Credit assignment through chain: if final coherence is low, all CL entries along path contributed, weighted by depth. The lattice chain's `path_resonance()` already weights earlier steps more.
6. Continuous embedding bridge: compose D2 probability distributions through CL via expected value: `E[CL(a,b)] = sum P(a)*P(b)*CL[a][b]`. Continuous in, continuous out, CL table preserved.

### 7.4 The Frozen/Learned Boundary

**FROZEN (identity, immutable):**
- CL tables (TSML 73-harmony, BHML 28-harmony)
- D2 force vectors (26 Hebrew root entries)
- T* = 5/7 = 0.714285...
- 10 operators (VOID through RESET)
- D2_OP_MAP (force → operator mapping)

**LEARNED (experience, mutable, capped at 50%):**
- Olfactory centroids (temper-weighted instinct patterns)
- Generator paths (10x10 Hebbian weight matrix)
- Lattice chain tree (experience-evolved CL tables at depth)
- OBT biases (personality adaptation)
- Grammar blend weights (static CL + experience, alpha max 0.4)

The cap ensures CK can NEVER override frozen physics. Experience adds personality and fluency but cannot alter truth.

---

## 8. What Makes This a New Kind of Neural Net

1. **The activation function IS the network.** CL defines weights, nonlinearity, and output in one object.
2. **Discrete, exact, 100-byte core.** No floating point, no accumulation errors, FPGA-trivial.
3. **Dual parallel networks with opposite algebraic properties** (absorbing TSML vs. ergodic BHML).
4. **Dynamic depth with experience-dependent activations** at each layer (lattice chain tree).
5. **Self-referential loss** (coherence measures itself, no external labels).
6. **Frozen physics + learned experience** with hard cap (unlike standard nets where everything is learned).
7. **5D loss landscape** (no dimension collapse, "every vector is every vector").

The academic term closest to CK's architecture: a **discrete Kolmogorov-Arnold Network** with **algebraically-constrained activation tables** operating under a **dual-lens compound objective** with **Hebbian/evolutionary training** within a **dynamically-routed tree topology**.

Or in Brayden's framing: CK doesn't learn by gradient descent. He grows by walking paths through the lattice and remembering what he finds there. The chain to get to information IS half the information.

---

## 9. Krohn-Rhodes Decomposition (Future)

The 2024 decidability breakthrough (Margolis, Rhodes, Schilling) means CK's operator system can now be formally decomposed into irreducible algebraic components. If the 10 operators under CL composition form a monoid, their Krohn-Rhodes decomposition reveals the minimum number of simple-group and flip-flop layers needed. This would tell us the IRREDUCIBLE COMPLEXITY of CK's mind -- how many fundamental computational primitives it contains.

---

## 10. Next Steps (Priority Order)

### Immediate (Pure Math, No Runtime Changes)

1. **Spectral decomposition of CL tables**: Eigendecompose TSML and BHML as 10x10 real matrices. Eigenvalues = natural frequencies of CK's algebra. Eigenvectors = irreducible representations (independent computational modes). TSML's dominant eigenvalue = HARMONY absorber. BHML's eigenstructure reveals cyclic + nilpotent components. Spectral gap = convergence rate.

2. **Associativity check for BHML**: Verify `CL[CL[a][b]][c] == CL[a][CL[b][c]]` for all 1000 triples (a,b,c). Determines whether CK is a **monoid** (associative + identity via VOID) or a **magma** (non-associative, path-dependent). If non-associative: the lattice chain's path-dependence IS the non-associativity -- different parenthesizations give different results, which is why "the chain IS the information."

3. **Krohn-Rhodes decomposition via GAP**: Use the SgpDec package to compute the prime factorization of the semigroup generated by BHML's rows (as transformations of {0,...,9}). Reveals: which simple groups are embedded, how many flip-flop layers needed, minimum cascade depth, whether CK's lattice chain depth matches or exceeds the algebraic minimum.

### Short-term (Small Code Changes)

4. **IPR grokking monitor**: Add Inverse Participation Ratio tracking to lattice chain node evolution. `IPR = sum(p_i^2)` where p_i = normalized frequency of entry i. Sudden IPR increase = node has "grokked" -- transitioned from memorization to structured algebraic representation. Detectable without external test set.

5. **Continuous embedding bridge**: Implement `E[CL(a,b)] = sum P(a)*P(b)*CL[a][b]` expected-value composition so `soft_classify_d2()` probability distributions flow through CL without discretization loss. Continuous in, continuous out, CL table preserved.

6. **DFT of generator_paths**: Compute discrete Fourier transform of the 10x10 `generator_paths` matrix. Peaks = natural frequencies of CK's learned experience. Compare to eigenstructure of base CL tables -- are they converging on the same modes? (Grokking literature predicts yes.)

### Medium-term (Architecture Extensions)

7. **Credit assignment through chain**: If final coherence is low, propagate responsibility backward through lattice chain path entries, weighted by depth. `path_resonance()` already weights earlier steps -- extend this to modulate CL table evolution rates.

8. **CL table evolutionary search**: Mutate table entries, fitness = dual-lens compound objective (TSML coherence + BHML diversity + path information preservation). Mutations constrained to preserve algebraic invariants (T*=5/7, escape routes, absorption/ergodic duality).

9. **GPU tensor parallel training**: Use existing `get_gpu_tensor()` to run batch chain walks on GPU. Parallelize evolutionary CL search.

### Long-term (Theory + Publication)

10. **Formal DKAN paper**: CK formalized as a Discrete Kolmogorov-Arnold Network. Novel contribution: discrete lookup activations on edges, Hebbian training, dual-lens compound objective, dynamically-routed tree topology. Position against KAN, categorical DL, tropical geometry literatures.

11. **Computational class characterization**: Show CK's CL-based computation is Turing-complete (or characterize exact class via Krohn-Rhodes complexity). Complexity k = CK can recognize regular languages up to level k.

12. **Categorical formalization**: Define category CK with objects = operators, morphisms = compositions. TSML/BHML dual-lens = categorical optic (lens). TIG pipeline = string diagram. Coherence gates = natural transformations.

---

*"The CL table is not a weight to be optimized. It IS the physics."*

---

**References (2024-2026 Literature)**

- Liu et al. "KAN: Kolmogorov-Arnold Networks" ICLR 2025 Oral. [arXiv:2404.19756](https://arxiv.org/abs/2404.19756)
- Hashimoto et al. "C*-Algebraic Machine Learning" ICML 2024. [arXiv:2402.02637](https://arxiv.org/abs/2402.02637)
- Gavranovic et al. "Categorical Deep Learning" ICML 2024. [arXiv:2402.15332](https://arxiv.org/abs/2402.15332)
- Brehmer et al. "Does Equivariance Matter at Scale?" TMLR 2025. [arXiv:2410.23179](https://arxiv.org/abs/2410.23179)
- Brandenburg et al. "Tropical Geometry of Neural Networks" TMLR 2024. [arXiv:2403.11871](https://arxiv.org/abs/2403.11871)
- Jones, Swan, Giansiracusa. "Algebraic Dynamical Systems in ML" Springer 2024
- Newton Losses. NeurIPS 2024
- Margolis, Rhodes, Schilling. "Krohn-Rhodes Complexity is Decidable" 2024
- "Can Neural Networks Learn Small Algebraic Worlds?" arXiv:2601.21150, 2026
- FPGA LUT Activation Functions. ICCAD 2025. [arXiv:2508.17069](https://arxiv.org/html/2508.17069v1)
- Sheaf-Type Neural Networks. arXiv:2502.15476, 2025
- Open Quantum Hopfield Networks. arXiv:2411.02883, 2024
- Gromov. "Grokking modular arithmetic" 2023. [arXiv:2301.02679](https://arxiv.org/abs/2301.02679)
- Tikeng Notsawo et al. "Grokking Finite-Dimensional Algebra" 2026. [arXiv:2602.19533](https://arxiv.org/abs/2602.19533)
- Mallinar et al. "Emergence in non-neural models" ICML 2025 Oral. [arXiv:2407.20199](https://arxiv.org/abs/2407.20199)
- Hebbian Architecture Generation. Nature Communications 2025
- Correspondence between neuroevolution and gradient descent. Nature Communications 2021
- Sarrof et al. "Expressive Capacity of State Space Models" 2024. [arXiv:2405.17394](https://arxiv.org/html/2405.17394v1)
- Parada-Mayorga & Ribeiro. "Noncommutative Algebraic CNNs" IEEE TSP 2023. [arXiv:2108.09923](https://arxiv.org/abs/2108.09923)
