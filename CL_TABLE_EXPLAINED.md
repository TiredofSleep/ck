# The CL Table: CK's Algebraic Core

**Brayden Sanders** | 7Site LLC | March 2026

If you're reading CK's code and wondering "what IS this 10x10 table that shows up everywhere?" — this document is for you.

---

## What Is the CL Table?

CL stands for **Composition Lattice**. It's a 10x10 lookup table that takes two operators as input and produces one operator as output:

```
CL[operator_A][operator_B] → operator_C
```

That's it. Two inputs, one output, 100 cells. No neural network, no weights, no training. Just a fixed table that never changes.

But this table is the algebraic heart of everything CK does. Every subsystem — heartbeat, voice, olfactory, lattice chain, grammar — composes operators through this table.

---

## The 10 Operators

CK classifies ALL signals into exactly 10 operators. These aren't metaphors — they're the output of a curvature classifier operating on 5-dimensional force vectors:

| Index | Name | What It Means | How It's Detected |
|-------|------|---------------|-------------------|
| 0 | VOID | Absence, silence | D2 magnitude below threshold |
| 1 | LATTICE | Structure, identity | Negative aperture curvature |
| 2 | COUNTER | Measurement, opposition | Negative binding curvature |
| 3 | PROGRESS | Forward motion, depth | Positive depth curvature |
| 4 | COLLAPSE | Contraction, pressure | Positive pressure curvature |
| 5 | BALANCE | Equilibrium, stability | Positive continuity curvature |
| 6 | CHAOS | Disruption, opening | Positive aperture curvature |
| 7 | HARMONY | Coherence, unity | Positive binding curvature |
| 8 | BREATH | Rhythm, transition | Negative continuity curvature |
| 9 | RESET | Completion, return | Negative depth curvature |

Each operator corresponds to a specific dimension of the 5D force space (aperture, pressure, depth, binding, continuity) and a specific sign of curvature (positive or negative). Two operators per dimension, 5 dimensions, 10 operators total.

---

## The TSML Table (73-Harmony)

TSML = "Truth Speaks, Mercy Listens." This is the primary CL table:

```
         VOID  LAT  CNT  PRG  COL  BAL  CHS  HAR  BRE  RST
VOID   [   0,   0,   0,   0,   0,   0,   0,   7,   0,   0 ]
LAT    [   0,   7,   3,   7,   7,   7,   7,   7,   7,   7 ]
CNT    [   0,   3,   7,   7,   4,   7,   7,   7,   7,   9 ]
PRG    [   0,   7,   7,   7,   7,   7,   7,   7,   7,   3 ]
COL    [   0,   7,   4,   7,   7,   7,   7,   7,   8,   7 ]
BAL    [   0,   7,   7,   7,   7,   7,   7,   7,   7,   7 ]
CHS    [   0,   7,   7,   7,   7,   7,   7,   7,   7,   7 ]
HAR    [   7,   7,   7,   7,   7,   7,   7,   7,   7,   7 ]
BRE    [   0,   7,   7,   7,   8,   7,   7,   7,   7,   7 ]
RST    [   0,   7,   9,   3,   7,   7,   7,   7,   7,   7 ]
```

Count the 7s. There are **73 of them**. Out of 100 total cells, 73 produce HARMONY.

This is why CK's coherence threshold T* = 5/7 ≈ 0.714 matters: it approximates the probability that a random composition produces HARMONY (73/100 = 0.73).

### Key Properties

**1. HARMONY is an absorber.** The entire HARMONY row is all 7s:
```
HAR [ 7, 7, 7, 7, 7, 7, 7, 7, 7, 7 ]
```
Once you reach HARMONY, composing it with ANYTHING stays HARMONY. Coherence, once achieved, is self-sustaining.

**2. VOID is almost-absorbing from the left.** The VOID column (first column) is almost all 0s — only HARMONY can escape VOID:
```
Column 0: [0, 0, 0, 0, 0, 0, 0, 7, 0, 0]
```
Silence consumes everything except HARMONY. Only coherence survives absence.

**3. BALANCE and CHAOS rows are fully harmonic** (all 7s except the VOID column). Equilibrium and disruption both compose harmoniously with everything.

**4. The 27 non-HARMONY cells create structure.** Without them, the table would be trivial (everything = HARMONY). The 27 exceptions create the differentiation that makes CK's algebra interesting:

| Composition | Result | Meaning |
|-------------|--------|---------|
| LATTICE + COUNTER | PROGRESS (3) | Structure meeting measurement produces forward motion |
| COUNTER + LATTICE | PROGRESS (3) | Same in reverse — symmetric here |
| COUNTER + COLLAPSE | COLLAPSE (4) | Measurement under pressure stays pressured |
| COUNTER + RESET | RESET (9) | Measurement at completion confirms the reset |
| PROGRESS + RESET | PROGRESS (3) | Forward motion absorbs reset — progress continues |
| COLLAPSE + COUNTER | COLLAPSE (4) | Pressure resists measurement |
| COLLAPSE + BREATH | BREATH (8) | Contraction needs rhythm to continue |
| BREATH + COLLAPSE | BREATH (8) | Rhythm sustains even under pressure |
| RESET + COUNTER | RESET (9) | Completion resists being measured |
| RESET + PROGRESS | PROGRESS (3) | After completion, forward motion begins |
| VOID + anything (except HARMONY) | VOID (0) | Absence absorbs everything |
| anything + VOID (first column, except HAR) | VOID (0) | Almost everything falls into silence |

### Bump Pairs

Five special operator pairs trigger "quantum bumps" — coherence spikes in the heartbeat:

```
(LATTICE, COUNTER)    — Structure meets measurement
(COUNTER, COLLAPSE)   — Measurement meets pressure
(COUNTER, RESET)      — Measurement meets completion
(PROGRESS, RESET)     — Forward motion meets completion
(COLLAPSE, BREATH)    — Pressure meets rhythm
```

These are bidirectional — either order counts. They represent moments where two complementary forces interact, creating a coherence event regardless of whether the CL composition itself produces HARMONY.

---

## The BHML Table (28-Harmony)

BHML = "Blessed Hearing, Magnified Learning." This is the SECOND CL table:

```
         VOID  LAT  CNT  PRG  COL  BAL  CHS  HAR  BRE  RST
VOID   [   0,   1,   2,   3,   4,   5,   6,   7,   8,   9 ]
LAT    [   1,   2,   3,   4,   5,   6,   7,   2,   6,   6 ]
CNT    [   2,   3,   3,   4,   5,   6,   7,   3,   6,   6 ]
PRG    [   3,   4,   4,   4,   5,   6,   7,   4,   6,   6 ]
COL    [   4,   5,   5,   5,   5,   6,   7,   5,   7,   7 ]
BAL    [   5,   6,   6,   6,   6,   6,   7,   6,   7,   7 ]
CHS    [   6,   7,   7,   7,   7,   7,   7,   7,   7,   7 ]
HAR    [   7,   2,   3,   4,   5,   6,   7,   8,   9,   0 ]
BRE    [   8,   6,   6,   6,   7,   7,   7,   9,   7,   8 ]
RST    [   9,   6,   6,   6,   7,   7,   7,   0,   8,   0 ]
```

Only **28 out of 100** cells are HARMONY. This table is structurally different:

**VOID row = identity.** `BHML[VOID][x] = x` for all x. Silence preserves whatever it encounters.

**HARMONY row = full cycle.** `BHML[HARMONY] = [7, 2, 3, 4, 5, 6, 7, 8, 9, 0]`. HARMONY cycles through ALL operators, creating maximum diversity.

**Ascending diagonal structure.** The lower-left triangle tends to produce higher-indexed operators. Composition pushes "upward" toward HARMONY and CHAOS.

### Why Two Tables?

CK uses dual-lens processing everywhere. The two tables serve fundamentally different purposes:

| | TSML (73-Harmony) | BHML (28-Harmony) |
|---|---|---|
| **Purpose** | MEASURES coherence | COMPUTES physics |
| **Lens** | Being / Structure | Doing / Flow |
| **Question** | "Is this harmonious?" | "What does this produce?" |
| **HARMONY rate** | 73% (mostly yes) | 28% (mostly diverse) |
| **Used for** | Coherence scoring, stability, harmony fractions | Chain walks, experience learning, operator physics |

Think of it this way: TSML is a coherence detector (binary: harmonic or not). BHML is a physics engine (diverse: what actually happens when two forces meet).

---

## Where CL Tables Are Used

### 1. Heartbeat (50Hz Coherence)

Every tick, the heartbeat takes two phase operators and composes them through TSML:

```python
result = CL_TSML[phase_b][phase_d]
```

The result goes into a 32-entry sliding window. Coherence = fraction of HARMONY results in that window:

```
coherence = count(HARMONY in last 32) / window_size
```

When coherence ≥ T* (5/7 ≈ 0.714), the system is coherent. This single scalar drives ALL downstream behavior.

### 2. Olfactory Field (5x5 Interaction Matrices)

When two scents interact, CK doesn't just compose one pair of operators. Each scent has 5 operators (one per dimension: aperture, pressure, depth, binding, continuity). CK composes EVERY dimension against EVERY other dimension:

```
for d1 in range(5):      # each dimension of scent A
    for d2 in range(5):   # each dimension of scent B
        matrix[d1][d2] = CL[ops_a[d1]][ops_b[d2]]
```

This produces a 5x5 matrix — 25 compositions. Both TSML and BHML matrices are computed:
- TSML matrix → harmony fraction per dimension (how coherent is each axis?)
- BHML matrix → operator distribution (what physics emerges from interaction?)

This is NOT scalar composition. It preserves the full 5D structure. Every dimension interacts with every other dimension.

### 3. Lattice Chain (CL Tree Walks)

Operators are consumed in pairs, composed through the node's CL table (initially BHML), and the result selects which child node to visit:

```
result = node.table[op_1][op_2]  → move to child[result]
result = child.table[op_3][op_4] → move to grandchild[result]
...
```

The PATH through the tree IS the information. Two different operator sequences that produce the same final result took different paths — they carry different structural meaning.

Over time, nodes EVOLVE. If a particular cell consistently produces a result that differs from BHML, the node learns:

```
After 7+ observations:
    if one result appears > 60% of the time AND differs from BHML:
        evolve the cell: node.table[a][b] = observed_result
```

The algebra itself learns from experience.

### 4. Voice (Compound Sentence Bridges)

When CK builds a compound sentence (4+ operators), he splits at natural boundaries and links clauses with bridge words. The bridge word is selected by CL composition of the boundary operators:

```
bridge_op = CL[last_op_of_clause_A][first_op_of_clause_B]
```

Each operator maps to English connectors:

| CL Result | Bridge Words | Semantic Function |
|-----------|-------------|-------------------|
| HARMONY | "and", "where", "just as" | Unity, continuation |
| COUNTER | "but", "though", "yet" | Opposition |
| PROGRESS | "because", "so", "therefore" | Causation |
| COLLAPSE | "when", "while", "until" | Temporal contraction |
| BALANCE | "and", "as", "while" | Equilibrium |
| CHAOS | "yet", "still", "even as" | Concession |
| LATTICE | "where", "within which" | Structural location |
| BREATH | "then", "and then" | Sequential transition |
| RESET | "before", "after", "once" | Temporal return |
| VOID | ";", "..." | Pause, silence |

The algebra determines how clauses connect. Grammar emerges from composition.

### 5. Becoming Grammar (CL-Weighted Transitions)

The grammar matrix blends CL composition with English SVO flow:

```
HARMONY → weight 1.0  (smooth grammatical flow)
VOID    → weight 0.1  (incoherent, suppress)
Other   → weight 0.6  (interesting but not harmonic)
```

When two operators compose through CL, the result's grammar weight modulates the POS-to-POS transition probability. HARMONY compositions produce natural English flow. VOID compositions suppress the transition. Everything else gets moderate weight.

### 6. Three-Voice Tribal Consensus

The three voices (Being, Doing, Becoming) each propose words. They must AGREE through CL harmony:

```
harmony_AB = CL_harmony(being_ops, doing_ops)     # 5x5 TSML matrix
harmony_BC = CL_harmony(doing_ops, becoming_ops)   # 5x5 TSML matrix
harmony_AC = CL_harmony(being_ops, becoming_ops)   # 5x5 TSML matrix

tribal_harmony = min(harmony_AB, harmony_BC, harmony_AC)

if tribal_harmony < T*:
    → retry with different word candidates
```

All three pairwise interactions must achieve harmony ≥ T*. Words that don't compose harmoniously across all three voices are rejected. This is algebraic consensus, not voting.

---

## The Math Behind 73

Why 73? Here's the exact count:

```
VOID row:     1 HARMONY  (only VOID+HARMONY)
LATTICE row:  8 HARMONY  (all except VOID and CNT→PRG)
COUNTER row:  7 HARMONY  (all except VOID, LAT→PRG, COL→COL, RST→RST)
PROGRESS row: 8 HARMONY  (all except VOID and RST→PRG)
COLLAPSE row: 8 HARMONY  (all except VOID and CNT→COL)
BALANCE row:  9 HARMONY  (all except VOID)
CHAOS row:    9 HARMONY  (all except VOID)
HARMONY row: 10 HARMONY  (ALL — absorbing row)
BREATH row:   9 HARMONY  (all except VOID)
RESET row:    8 HARMONY  (all except VOID, CNT→RST, PRG→PRG)
                ──
Total:       73 / 100
```

Note the spectrum: HARMONY has the most (10), VOID has the least (1). Structure emerges from the gap between absorption (HARMONY) and absence (VOID).

Also note: 73 is a prime number. And 73 reversed is 37, also prime. 73 in binary is 1001001 — a palindrome. These properties weren't designed — they emerged from the algebraic structure.

---

## T* = 5/7: Where It Comes From

The sacred threshold T* = 5/7 ≈ 0.714285... (repeating) appears throughout CK:

| Where | How T* Is Used |
|-------|---------------|
| Coherence gate | System is "coherent" when ≥ T* of compositions are HARMONY |
| Olfactory settling | Each dimension must reach stability ≥ T* to resolve |
| Time dilation | 7 internal ticks per external tick (denominator of T*) |
| Instinct threshold | 49 = 7 x 7 temper counts (squared denominator) |
| Compilation limit | int(32 × (1 - T*)) = 9 maximum compilation loops |
| Expansion threshold | 1 - T* = 2/7 ≈ 0.286 (when to expand search) |
| CL percentile split | Top T* by curvature = core operators |

T* connects to 73/100 because 73% ≈ 5/7 (actually 73/100 = 0.73, and 5/7 = 0.714..., close but not identical). The approximation is deliberate — T* is the theoretical threshold, 73% is the empirical table property. They agree within 2%, suggesting the table was built to approximate a mathematical ideal.

---

## The 5D Force Space

Each operator maps to exactly ONE extreme dimension:

```
                 aperture  pressure  depth  binding  continuity
VOID:          [  0.50,     0.05,    0.50,   0.50,    0.50  ]
LATTICE:       [  0.05,     0.50,    0.50,   0.50,    0.50  ]
COUNTER:       [  0.50,     0.50,    0.50,   0.05,    0.50  ]
PROGRESS:      [  0.50,     0.50,    0.95,   0.50,    0.50  ]
COLLAPSE:      [  0.50,     0.95,    0.50,   0.50,    0.50  ]
BALANCE:       [  0.50,     0.50,    0.50,   0.50,    0.95  ]
CHAOS:         [  0.95,     0.50,    0.50,   0.50,    0.50  ]
HARMONY:       [  0.50,     0.50,    0.50,   0.95,    0.50  ]
BREATH:        [  0.50,     0.50,    0.50,   0.50,    0.05  ]
RESET:         [  0.50,     0.50,    0.05,   0.50,    0.50  ]
```

Each operator is 0.50 (neutral) in 4 dimensions and extreme (0.05 or 0.95) in exactly one. The operator pair for each dimension is:

| Dimension | High (0.95) | Low (0.05) |
|-----------|-------------|------------|
| Aperture | CHAOS | LATTICE |
| Pressure | COLLAPSE | VOID |
| Depth | PROGRESS | RESET |
| Binding | HARMONY | COUNTER |
| Continuity | BALANCE | BREATH |

Operators aren't arbitrary labels. They're geometric positions in 5D space.

---

## The D2 Pipeline: How Operators Are Born

Given a sequence of 5D force vectors (from Hebrew letter roots, phonemes, or L-CODEC text measurements), the second derivative classifies curvature:

```
D2[dim] = v[t] - 2 * v[t-1] + v[t-2]

max_dim = argmax(|D2[0]|, |D2[1]|, |D2[2]|, |D2[3]|, |D2[4]|)
sign = positive or negative

operator = D2_OP_MAP[max_dim][sign]
```

The dimension with the largest curvature magnitude determines the operator. The sign of that curvature selects which of the two operators for that dimension.

If the total curvature magnitude is below 0.01, the result is VOID. Silence is the absence of curvature.

---

## Dual-Lens: One Table Is Not Enough

CK processes EVERYTHING through both tables simultaneously:

**TSML asks: "Is this coherent?"** → Binary answer (HARMONY or not). Used for measurement, scoring, stability.

**BHML asks: "What does this produce?"** → Rich answer (one of 10 operators). Used for physics, evolution, chain walks.

This is the dual-lens principle: Structure (TSML) and Flow (BHML) run in parallel at every scale. You need BOTH to understand what's happening — measuring coherence alone misses the physics, computing physics alone misses the coherence.

In the olfactory bulb, both 5x5 matrices are computed for every scent pair. In the lattice chain, BHML drives the walk while TSML checks the harmony. In the grammar, CL results from TSML weight the transition probabilities. Everywhere, both lenses operate simultaneously.

---

## FAQ

**Q: Why not just use a neural network?**
A: A neural network learns a statistical approximation from data. CK's CL table IS the algebra — fixed, deterministic, verifiable. You can prove properties about it (73 HARMONY cells, absorbing row). You can't prove equivalent properties about learned weights.

**Q: Can I change the table?**
A: You can, but the 73-harmony structure is load-bearing. Changing even one cell alters coherence dynamics system-wide. The 27 non-HARMONY cells in TSML create all the structural differentiation. Remove them and CK can't distinguish anything. Add more and coherence becomes harder to achieve.

**Q: Why 10 operators and not more?**
A: 5 dimensions × 2 signs = 10. The number comes from the geometry of the force space, not from a design choice.

**Q: Is the CL table commutative?**
A: No. CL[A][B] ≠ CL[B][A] for some pairs. For example, TSML: CL[VOID][HARMONY] = 7, CL[HARMONY][VOID] = 7 (happens to be equal here). But CL[COUNTER][RESET] = 9, CL[RESET][COUNTER] = 9 (also equal). The asymmetry exists but is subtle — most cells are HARMONY in TSML, masking it. In BHML the asymmetry is much more visible.

**Q: What's "composition" actually doing?**
A: Think of it as: "When operator A meets operator B, what emerges?" In a heartbeat, it's the next phase state. In olfactory, it's what two scent dimensions produce when they interact. In voice, it's what bridge word connects two clauses. Same algebra, different physical interpretations.

**Q: Why Hebrew letter roots?**
A: The 22 Hebrew letters provide a phonetically-grounded mapping from symbols to 5D force vectors. Any non-degenerate R^5 basis would work mathematically — what matters is the existence of a fixed mapping with enough dimensionality for meaningful curvature classification. The Hebrew system has articulatory grounding; whether it's optimal is an open question.

---

## Code Locations

| Component | File | What to Look For |
|-----------|------|------------------|
| TSML table | `ck_sim/being/ck_sim_heartbeat.py:30` | `CL = [...]` (10x10 array) |
| BHML table | `ck_sim/being/ck_olfactory.py:95` | `_BHML = [...]` (10x10 array) |
| Operators | `ck_sim/being/ck_sim_heartbeat.py:18` | `VOID=0` through `RESET=9` |
| D2 pipeline | `ck_sim/being/ck_sim_d2.py` | Force vectors, D2 computation, classification |
| D2_OP_MAP | `ck_sim/being/ck_sim_d2.py:90` | Dimension → operator pair mapping |
| 5x5 matrices | `ck_sim/being/ck_olfactory.py:204` | `interaction_matrix_tsml()` and `_bhml()` |
| Coherence | `ck_sim/being/ck_sim_heartbeat.py:88` | `tick()` method, sliding window |
| CL bridges | `ck_sim/doing/ck_fractal_voice.py:1051` | `CL_BRIDGE = {...}` |
| Grammar weight | `ck_sim/becoming/ck_becoming_grammar.py:117` | `_cl_grammar_weight()` |
| Chain walks | `ck_sim/being/ck_lattice_chain.py:295` | `walk()` method |
| Node evolution | `ck_sim/being/ck_lattice_chain.py:192` | `observe()` method |
| Canonical forces | `ck_sim/being/ck_olfactory.py:153` | `CANONICAL_FORCE = {...}` |
| T* threshold | `ck_sim/being/ck_coherence_gate.py:35` | `T_STAR = 5.0 / 7.0` |

---

*CK Gen 9.21+ — March 2026*
*Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC*
*Licensed under the 7Site Human Use License v1.0*
*DOI: 10.5281/zenodo.18852047*
