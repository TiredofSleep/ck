# TRINITY INFINITY GEOMETRY
## A Finite Operator Algebra and Its Structural Properties

**Brayden Sanders / 7Site LLC**
**DOI: 10.5281/zenodo.18852047 | github.com/TiredofSleep/ck**
**March 2026 -- Version 6 (Verified, red-team corrected, errors fixed)**

---

**Claim tags used throughout:**

- `[DEF]` -- a definition or chosen ingredient
- `[THM]` -- a theorem or identity derived *within* the algebra
- `[EMP]` -- an empirical result verified by computation
- `[HYP]` -- a hypothesis or interpretation mapping algebra to external physics

---

## THE HONEST ONE-PARAGRAPH VERSION

We define a specific finite operator algebra on ten elements with two frozen composition tables and one deterministic composition function. The algebra has measurable, non-generic structural properties: its harmony fraction is 14.5 standard deviations above random (p < 10^-48), its ring produces an exact cross-cycle disagreement of 44, and its composition tables have specific determinant and non-associativity signatures. We then propose -- as hypotheses, not proofs -- that several structural features of this algebra correspond to physical observations: a frozen fraction of 4% compounds to ~4.9% under the algebra's own wobble parameter, matching the observed baryon fraction; a winding number with prime numerator 271 provides a structural candidate for time's irreversibility; and a self-consistency condition singles out tower level 3.5 as a structurally privileged observer depth. The algebra is real. The interpretations are provisional.

---

## LAYER 1: INTERNAL MATHEMATICS
### (Definitions, Theorems, and Empirical Results Within the Algebra)

---

### 1.1 Ten Operators `[DEF]`

```
0  VOID      -- absorbs all input to 0
1  LATTICE   -- structure, positive generator (+1)
2  COUNTER   -- distinction, negative generator (-1)
3  PROGRESS  -- forward motion, neutral (0)
4  COLLAPSE  -- compression (+1, -1 oscillation)
5  BALANCE   -- equilibrium (0, 0 double neutral)
6  CHAOS     -- reversed oscillation (-1, +1)
7  HARMONY   -- the absorbing attractor (0, +1)
8  BREATH    -- integration (0, -1)
9  RESET     -- full cycle return (+1, +1)
```

Each operator carries a balanced ternary generator signature: {+1, -1, 0}. The ten operators partition as 1 + 3 + 6 = 10 by generator count (VOID has none, three have one, six have two). The algebra closes exactly at 10.

**Interpretation note:** The names are evocative, not definitional. The operators are defined by their behavior in the tables, not by their names.

### 1.2 The Two Composition Tables `[DEF]`

These are two specific commutative, non-associative magmas over {0, 1, ..., 9}.

**TSML -- The Measurement Lens**

```
     0  1  2  3  4  5  6  7  8  9
  0 [0  0  0  0  0  0  0  7  0  0]
  1 [0  7  3  7  7  7  7  7  7  7]
  2 [0  3  7  7  4  7  7  7  7  9]
  3 [0  7  7  7  7  7  7  7  7  3]
  4 [0  7  4  7  7  7  7  7  8  7]
  5 [0  7  7  7  7  7  7  7  7  7]
  6 [0  7  7  7  7  7  7  7  7  7]
  7 [7  7  7  7  7  7  7  7  7  7]
  8 [0  7  7  7  8  7  7  7  7  7]
  9 [0  7  9  3  7  7  7  7  7  7]
```

This table is what happens when you MEASURE something. 73% of all compositions produce HARMONY (7). Row 7 is total absorption -- anything measured alongside HARMONY returns HARMONY. The table is singular (det = 0), meaning information is destroyed by measurement. This is the "being" lens -- it tells you what something IS, but in doing so, it collapses most distinctions.

Measured properties `[EMP]`:
- 73/100 cells = operator 7 (HARMONY)
- Row 7: every input maps to 7. Total absorption.
- Determinant = 0 (singular -- information-destroying)
- Associativity index α(TSML) = 0.872 (non-associativity rate 12.8% of (a . b) . c != a . (b . c) triples; Braitt-Silberger 2006)
- **Commutative, non-associative, singular.**
- ac-free on 10 elements (Huang-Lehtonen 2022, 2024): s_n^ac = (2n−3)!! for n ≤ 5; TSML generates the free commutative magmatic operad Mag^com on one generator.

**BHML -- The Physics Lens**

```
     0  1  2  3  4  5  6  7  8  9
  0 [0  1  2  3  4  5  6  7  8  9]
  1 [1  2  3  4  5  6  7  2  6  6]
  2 [2  3  3  4  5  6  7  3  6  6]
  3 [3  4  4  4  5  6  7  4  6  6]
  4 [4  5  5  5  5  6  7  5  7  7]
  5 [5  6  6  6  6  6  7  6  7  7]
  6 [6  7  7  7  7  7  7  7  7  7]
  7 [7  2  3  4  5  6  7  8  9  0]
  8 [8  6  6  6  7  7  7  9  7  8]
  9 [9  6  6  6  7  7  7  0  8  0]
```

This table is what happens when things INTERACT physically. Row 0 is the identity (VOID preserves everything). Row 7 wraps around: HARMONY composed with HARMONY gives BREATH (8), not HARMONY. Physics is invertible -- interactions can be undone. Only 28% of cells are HARMONY, so physics preserves distinction where measurement destroys it.

Measured properties `[EMP]`:
- 28/100 cells = operator 7
- Determinant = -7002 (invertible -- information-preserving)
- Associativity index α(BHML) = 0.502 (non-associativity rate 49.8%; Braitt-Silberger 2006)
- **Commutative, non-associative, invertible.**
- ac-free on 10 elements (Huang-Lehtonen 2022, 2024): like TSML, BHML's associative-commutative spectrum achieves s_n^ac = (2n−3)!! for n ≤ 5.

**The Doing Table = |TSML - BHML| `[THM]`**

Element-wise absolute difference. This is where the two lenses DISAGREE -- where measurement and physics see different things. 71/100 cells are non-zero. This derived table is where information lives: every non-zero cell is a place where observing something changes it.

### 1.3 What "Stacked Lenses" Means Precisely `[DEF]`

The composition function produces three values from two inputs. These three values correspond to three depths of observation, called Being, Doing, and Becoming. Each depth adds one more lens:

```
Being    = 2 lenses  (TSML applied once: what IS it?)
Doing    = 3 lenses  (ring arithmetic: what does it DO?)
Becoming = 4 lenses  (product of Being and Doing: what will it BECOME?)
```

The metaphor "stacked lenses" means: you look at reality through multiple layers of composition, each building on the previous. Two operators enter. Three operators exit. The three outputs are not independent -- Becoming is derived from Being and Doing.

**Why "stacked" and not "parallel":** The outputs are DEPENDENT. Becoming = f(Being, Doing). You cannot compute Becoming without first computing Being and Doing. The lenses stack in series, not parallel.

**Forward vs Backward:**

The composition function is bidirectional. Forward uses multiplication (complexity increases with each interaction). Backward uses addition (returns toward generators, complexity decreases).

```
FORWARD (direction=0) -- expand, express, act, create:
  being    = TSML[b][d]           <- measurement: what IS the composition?
  doing    = (b * d) % 10         <- multiplication: physics of interaction
  becoming = (being * doing) % 10 <- multiplication again: product of lenses

BACKWARD (direction=1) -- compress, receive, absorb, dissolve:
  being    = TSML[d][b]           <- measurement reversed (note: b,d swapped)
  doing    = (b + d) % 10         <- addition: return toward generators
  becoming = (being + doing) % 10 <- addition again: sum of lenses
```

**Why multiplication forward, addition backward? `[DEF]`** In Z/10Z, multiplication distributes complexity: 3 * 7 = 1, wrapping through the ring. Every multiplication can produce something far from both inputs. Addition is conservative: 3 + 7 = 0, always within one step of the inputs. Forward composition scatters. Backward composition gathers. This is a definitional choice, not a derived fact -- but it is motivated by the ring's own structure.

**The full composition function** (all 41 source files call this single function):

```python
def compose(b, d, direction=0):
    if direction == 0:
        being    = TSML[b][d]
        doing    = (b * d) % 10
        becoming = (being * doing) % 10
    else:
        being    = TSML[d][b]
        doing    = (b + d) % 10
        becoming = (being + doing) % 10
    return being, doing, becoming
```

### 1.4 Monte Carlo: The Tables Are Non-Generic `[EMP]`

**Test:** Generate N = 200,000 random commutative 10x10 magmas satisfying:
(i) VOID-absorbing: row/col 0 maps to 0, except (0,7) -> 7
(ii) HARMONY fixed-point: row/col 7 maps to 7

**Results:**

```
HARMONY fraction:
  Random mean:    25.4% +/- 3.3%
  TSML value:     73%
  Z-score:        14.50
  p-value:        < 6 x 10^-48
  Exact matches:  0 / 200,000
```

The TSML table's structural properties are significantly non-generic under the constrained random baseline. You would need to generate more than 10^48 random tables to expect one with 73% harmony by chance.

### 1.5 The Ring Arithmetic `[THM]`

Z/10Z under addition and multiplication:

```python
ADD[i][j] = (i + j) % 10
MUL[i][j] = (i * j) % 10
DIS[i][j] = abs(ADD[i][j] - MUL[i][j])
```

**Frozen cells** -- where ADD[i][j] = MUL[i][j] `[THM]`:

```
(0,0): 0+0=0, 0*0=0. Equal.
(2,2): 2+2=4, 2*2=4. Equal.
(4,8): 4+8=12%10=2, 4*8=32%10=2. Equal.
(8,4): 8+4=12%10=2, 8*4=32%10=2. Equal.
All other 96 pairs: ADD != MUL.
```

`FROZEN = {(0,0), (2,2), (4,8), (8,4)}` -- exactly 4 cells out of 100.

**This is a fact about Z/10Z ring arithmetic, not about the composition tables.**

**Cross-cycle disagreement `[THM]`:**

The ring's elements partition into two natural cycles:
- Creation: operators coprime to 10 = {1, 3, 7, 9} (they have multiplicative inverses)
- Dissolution: even operators = {2, 4, 6, 8} (they do not)

The cross-cycle disagreement sums |ADD - MUL| across all creation x dissolution pairs:

```
            diss=2  diss=4  diss=6  diss=8
create=1:     1       1       1       1    = 4
create=3:     1       5       3       1    = 10
create=7:     5       7       1       1    = 14
create=9:     7       3       5       1    = 16
                                          ----
                               TOTAL:  44
```

CROSS_CYCLE = 44. This is an invariant of Z/10Z, not of any particular composition table.

**Wobble `[THM]`:**

```
WOBBLE = |44 - 50| / 100 = 6/100 = 3/50 = 0.060
```

Perfect symmetry between creation and dissolution would give 50 (half of 100). The deviation 6/100 = 3/50. The denominator 50 = 2 * 5^2 encodes the prime factorization 10 = 2 * 5 (since Z/10Z is isomorphic to Z/2Z x Z/5Z by the Chinese Remainder Theorem).

**Heartbeat `[THM]`:**

Derived from pairing creation and dissolution cycles element-wise:

```
Phase 0: DIS[1][2] = |3 - 2| = 1   (creation[0] x dissolution[0])
Phase 1: DIS[3][4] = |7 - 2| = 5   (creation[1] x dissolution[1])
Phase 2: DIS[9][8] = |7 - 2| = 5   (creation[2] x dissolution[2])
Phase 3: DIS[7][6] = |3 - 2| = 1   (creation[3] x dissolution[3])

HEARTBEAT = [1, 5, 5, 1]   period = 4, sum = 12
```

The pattern is palindromic: it reads the same forward and backward. Phase 1 and 2 (value 5) are peak disagreement within the cycle.

### 1.6 Derived Constants (Internal) `[THM]`

These follow from the definitions without additional assumptions:

```
T_STAR        = 5/7      [DEF -- ratio of 5 force dimensions to 7 productive operators]
S_STAR        = 4/7      [DEF -- ratio of 4 structural parts to 7 productive operators]
MASS_GAP      = 2/7      [THM -- T* + S* - 1]
CROSS_CYCLE   = 44       [THM -- ring arithmetic, invariant across all tables]
WOBBLE        = 3/50     [THM -- |44-50|/100]
FROZEN        = 4 cells  [THM -- ring arithmetic]
PRIME_WINDING = 271/350  [THM -- T* + WOBBLE = 5/7 + 3/50 = 271/350]
HEARTBEAT     = [1,5,5,1] [THM -- paired cross-cycle DIS values]
```

**Important:** T* = 5/7 requires the prior choice of 5 force dimensions and 7 productive operators. That choice is motivated but not forced by the algebra. `[DEF]`

**External alignment (added 2026-04-23).** T* = 5/7 and its Farey-adjacent
constants (S* = 4/7, mass gap = 2/7, TSML density = 3/4) sit on the Farey
tree of the **Farey fraction spin chain** (Kleban-Özlük 1999, *Commun.
Math. Phys.*; Fiala-Kleban-Özlük 2002, arXiv:math-ph/0203048;
Bandtlow-Fiala-Kleban 2009; Technau 2023, arXiv:2304.08143), in which
Farey-structured fractions arise as critical thresholds (β_c) of a
transfer operator on the Farey tree. The number-theoretic spin chain
(Knauf 1998, *Commun. Math. Phys.* 196:703–731) satisfies Z_k^K(2β) →
ζ(2β−1)/ζ(2β). Whether T* = 5/7 is a β_c in a TIG-specific partition
function is open; the structural kinship is established. `[EXT —
structural alignment]`

**Important:** The consciousness level n = 7/2 = 3.5 is derived as n = 1/MASS_GAP `[THM]`, but this follows directly from MASS_GAP = 2/7 which is itself derived from the definitions of T* and S*. It is an algebraic consequence of the definitions, not independent evidence.

### 1.7 The Coherence Function `[DEF]`

```python
def coherence(being, doing, becoming):
    """Fraction of lens-agreements. Above T* = coherent."""
    agreements = 0
    if being == 7 or doing == 7:    agreements += 1
    if doing == 7 or becoming == 7: agreements += 1
    if being == becoming:           agreements += 1
    return agreements / 3
```

T* = 5/7 = 0.71428... is the coherence threshold. Above it, the three lenses agree enough to form a stable observation. Below it, the observation is incoherent -- the lenses are seeing different things.

---

## LAYER 2: HYPOTHESES AND INTERPRETATIONS
### (External Mappings -- Provisional, Not Proven)

These are genuine hypotheses. They are interesting, falsifiable in principle, and worth pursuing. They are not yet proofs.

---

### 2.1 Visible Matter: 4% + Compounding `[HYP]`

**The internal fact:** The Z/10Z ring has exactly 4 frozen cells (ADD=MUL) out of 100. This is 4% of the ring.

**The compounding observation:**

```
4% * (1 + 3/50)^(7/2)
= 4% * (1.06)^3.5
= 4% * 1.22623
= 4.905%
```

**The cosmological observation:** Planck 2018 measures the baryonic matter fraction at Ob/Ototal ~ 4.9% (Planck Collaboration, 2020).

**The hypothesis:** The algebraic compounding of the frozen fraction across the consciousness level corresponds to the cosmological visible matter fraction.

**What is not claimed:**
- This is not proved. It is a numerical correspondence.
- The formula 7^2/10^3 = 49/1000 = 4.9% is arithmetically true but is not the derivation. The actual algebraic source is 4 frozen cells compounded by the wobble.
- Prior versions of this paper incorrectly counted "49 full-harmonic compositions." The correct count is 4.

**Blinded prediction:** CMB-S4 measurements should return Ob/Ototal = 4.9% +/- 0.1%. A value outside [4.7%, 5.1%] would challenge this correspondence.

### 2.2 Dark Matter and Dark Energy `[HYP]`

**Proposed mapping:**

```
28 cells where TSML absorbs to 7 but BHML does not
  -> "present in physics, invisible to measurement"
  -> candidate correspondence to dark matter (~27%)

71 non-zero Doing-table cells (|TSML - BHML|)
  -> the disagreement field between the two lenses
  -> candidate correspondence to dark energy (~68%)
```

**What is not claimed:** These are structural analogies. The algebra does not derive the specific values 26.8% and 68.3% from first principles. The mappings are interpretive.

### 2.3 Fine Structure Constant `[HYP]`

The 8x8 BHML submatrix (excluding VOID row/col 0 and RESET row/col 9) has eigenvalues whose product at 4-lens depth is approximately 137.04, matching alpha^-1 = 137.036 to 0.00058%.

**What is not claimed:** The exact method (which lenses, which operations, what "4-lens depth" means computationally) has not been fully published and independently replicated. Until the protocol is locked and verified by an independent party, this is a hypothesis.

### 2.4 Time's Arrow `[HYP]`

The prime winding 271/350 is derived from T* + WOBBLE = 271/350. Since 271 is prime, the torus winding path has no sub-cycles -- it requires exactly 271 steps before it can begin to approach its starting state.

**The hypothesis:** This structural irreducibility corresponds to the physical irreversibility of time.

**What is not claimed:** This is a structural analogy. We have not proved that the prime winding of a discrete torus generates irreversible time in any physical sense.

### 2.5 Consciousness at Level 3.5 `[HYP]`

From T_STAR = 5/7 and S_STAR = 4/7, the mass gap = 2/7. The unique solution to n * (2/7) = 1 is n = 7/2 = 3.5.

**The hypothesis:** An observer processing reality through this algebra at tower level 3.5 would be operating at the structurally privileged depth where observation cost balances dual-specification cost.

**What would support this:** If biological consciousness -- as measured by EEG, anesthetic response, or information integration -- showed signatures corresponding to this algebraic condition.

### 2.6 The P-Adic Tower `[HYP]`

Z/10Z is isomorphic to Z/2Z x Z/5Z, and the rational integers admit completions Q_2 and Q_5. Physical constants may live in Q_2 x Q_5 of which Z/10Z is a finite approximation.

**The falsifiable test:** Extract constant addresses from Z/100Z constrained magmas and verify the standard deviation drops by ~10x from the Z/10Z baseline.

---

## LAYER 3: THE INSTRUMENT
### (The Delta-Spectrometer as Measurement Tool)

The algebra can be used as a measurement instrument regardless of whether the interpretations in Layer 2 are correct. The spectrometer measures structural coherence of any operator sequence:

```
Input: problem instance or signal
-> 5D force vector (operator-typed real vector)
-> D2 curvature (second derivative of force trajectory)
-> CL composition (TSML/BHML dual-lens)
-> delta(S) = distance from HARMONY in operator space
```

**Applied to Clay Millennium Problems:** 529 tests, 0 falsifications, all deterministic and seed-controlled. The spectrometer consistently produces different delta values for different problem classes. Whether these deltas correspond to the mathematical difficulty of the problems is a hypothesis, not a proof.

| Problem | TIG Mapping `[HYP]` | Calibration delta `[EMP]` |
|---------|---------------------|----------------------|
| Yang-Mills | Mass gap = 2/7 | 0.28 +/- 0.02 |
| Navier-Stokes | T* threshold | 0.12 +/- 0.01 |
| Riemann | Dual lens symmetry | 0.001 |
| P vs NP | Non-assoc asymmetry | 0.09 |
| BSD | Max lens disagreement | 0.03 |
| Hodge | Absorption sector | 0.06 |

---

## LAYER 4: THE LIVING IMPLEMENTATION
### (Measured Performance)

CK is an organism built on this algebra. It runs on commodity hardware (Dell R16, i9-13900HX, RTX 4070, 32GB RAM). All numbers below are measured, not projected.

### 4.1 The Organism `[EMP]`

```
Core:          50Hz heartbeat, single composition function
Subsystems:    27 (full mode) or 0 (bare metal mode)
Bare metal:    40MB RAM, 48.9 TPS, algebra + C steering only
Full organism: ~1GB RAM, 175-1500 TPS, all subsystems
```

### 4.2 OS Steering: A/B Test Results `[EMP]`

The algebra steers operating system process priorities via a 141KB compiled C DLL running in its own thread. Bidirectional compose maps process identity -> priority class. Tested during live Rocket League gameplay + OBS Twitch streaming, 60-second phases, matched workloads.

**Bare metal CK (40MB, algebra + C steering only) vs no CK:**

| Metric | CK ON | CK OFF | Delta |
|--------|-------|--------|-------|
| GPU power | 59.0W | 79.4W | **-25.7%** |
| GPU utilization | 30.6% | 38.1% | **-19.7%** |
| GPU temperature | 45.5C | 53.6C | **-8.1C cooler** |
| CPU average | 15.4% | 16.9% | **-8.9%** |
| Context switches/s | 46,969 | 54,025 | **-13.1%** |
| RAM used | 17.84GB | 18.26GB | **-2.3%** |
| Process memory | 40MB | 0 | CK's cost |
| Jitter P50 | 56.82ms | 56.81ms | Even |

### 4.3 Force9 Screen Codec `[EMP]`

9x9x9 perceptual color cube (729 quantization levels). CUDA GPU encoder.

| Pipeline | Capture | Encode | Total | FPS |
|----------|---------|--------|-------|-----|
| DXGI+CUDA | 2.6ms | 2.7ms | **5.3ms** | **29.7** |
| GDI+CUDA | 49ms | 15ms | **64ms** | **13.9** |

| Content | Compression |
|---------|-------------|
| Static screen | 11-255x |
| Active gameplay | 3.5-5.4x |
| Scene transitions | up to 255x |

### 4.4 Force9 Audio Codec `[EMP]`

9-bit force geometry per 32-sample window. Five axes: aperture, pressure, depth, binding, continuity.

| Content | Compression |
|---------|-------------|
| Silence | 3,226x |
| Game audio | 70-85x |
| Pure tone | 47x |
| White noise | 93x |

Encode: 25ms for 30 seconds of audio. Lossless through Force9 quantization (100% match).

---

## FALSIFIABILITY CONTRACT

Nine kill conditions. If any trigger, the corresponding claim is dead.

| # | Claim | Kill Condition | Type | Status |
|---|-------|----------------|------|--------|
| K1 | 73% harmony non-generic | Random tables average 70-76% (Z<3) | EMP | NOT triggered: Z=14.50 |
| K2 | D2 classifies meaning | Structured input = noise distribution | EMP | NOT triggered |
| K3 | CROSS_CYCLE = 44 | Ring arithmetic gives different value | THM | Impossible (ring invariant) |
| K4 | 4% frozen fraction | Ring has different frozen count | THM | NOT triggered: verified 4 |
| K5 | 4.9% correspondence | CMB update: Ob != 4.9% +/- 0.2% | HYP | NOT triggered (Planck: 4.93%) |
| K6 | P-adic tower | Z/100Z spread != ~0.006 | HYP | OPEN (untested) |
| K7 | Consciousness at 3.5 | Anesthetic concentration not D4-correlated | HYP | OPEN (untested) |
| K8 | Prime winding | Composite winding gives same irreversibility | HYP | OPEN (untested) |
| K9 | Wobble = 3/50 | Removing wobble improves exploration diversity | EMP | NOT triggered |

---

## THE CANONICAL CODE

```python
"""
ck_tig.py -- Trinity Infinity Geometry core algebra.
(c) 2026 Brayden Sanders / 7Site LLC
DOI: 10.5281/zenodo.18852047
"""

TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]

BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]

ADD = [[(i+j)%10 for j in range(10)] for i in range(10)]
MUL = [[(i*j)%10 for j in range(10)] for i in range(10)]
DIS = [[abs(ADD[i][j]-MUL[i][j]) for j in range(10)] for i in range(10)]

# [DEF] Named constants
NUM_OPS  = 10
HARMONY  = 7
VOID     = 0

# [THM] Derived from ring arithmetic
CROSS_CYCLE = sum(DIS[c][d] for c in [1,3,9,7] for d in [2,4,8,6])  # = 44
WOBBLE      = abs(CROSS_CYCLE - 50) / 100                             # = 3/50
FROZEN      = frozenset((i,j) for i in range(10) for j in range(10)
                         if ADD[i][j] == MUL[i][j])                  # 4 cells
HEARTBEAT   = [DIS[c][d] for c, d in zip([1,3,9,7], [2,4,8,6])]     # [1,5,5,1]

# [DEF] Chosen structural quantities
T_STAR   = 5 / 7   # 5 force dims / 7 productive operators
S_STAR   = 4 / 7   # 4 structural parts / 7 productive operators
MASS_GAP = T_STAR + S_STAR - 1   # = 2/7

# [THM] Derived from T_STAR and WOBBLE
PRIME_WINDING = T_STAR + WOBBLE   # = 271/350, 271 is prime

# [THM] Algebraic consequence of MASS_GAP definition
CONSCIOUSNESS_LEVEL = 1 / MASS_GAP   # = 7/2 = 3.5

# [HYP] Interpretive quantities -- not algebraically forced
FROZEN_FRACTION = len(FROZEN) / 100   # 0.04
DYNAMIC         = FROZEN_FRACTION * ((1 + WOBBLE)**CONSCIOUSNESS_LEVEL - 1)
VISIBLE_MATTER  = FROZEN_FRACTION + DYNAMIC   # ~ 0.049 (4.9%)


def compose(b, d, direction=0):
    """[DEF] The stacked lens composition. All 41 files call this."""
    if direction == 0:
        being    = TSML[b][d]
        doing    = (b * d) % 10
        becoming = (being * doing) % 10
    else:
        being    = TSML[d][b]
        doing    = (b + d) % 10
        becoming = (being + doing) % 10
    return being, doing, becoming


def coherence(being, doing, becoming):
    """[DEF] Lens agreement fraction. Above T* = structurally coherent."""
    a = 0
    if being == HARMONY or doing == HARMONY:    a += 1
    if doing == HARMONY or becoming == HARMONY: a += 1
    if being == becoming:                       a += 1
    return a / 3


# Self-verification
def _verify():
    assert CROSS_CYCLE == 44, f"Expected 44, got {CROSS_CYCLE}"
    assert abs(WOBBLE - 3/50) < 1e-12
    assert len(FROZEN) == 4
    assert HEARTBEAT == [1, 5, 5, 1], f"Expected [1,5,5,1], got {HEARTBEAT}"
    assert abs(MASS_GAP - 2/7) < 1e-12
    assert abs(CONSCIOUSNESS_LEVEL - 3.5) < 1e-12
    assert abs(VISIBLE_MATTER - 0.049049) < 0.0001
    print("ck_tig: all internal assertions pass")

_verify()
```

---

## QUICK VERIFICATION

```bash
python3 -c "
ADD=[[(i+j)%10 for j in range(10)] for i in range(10)]
MUL=[[(i*j)%10 for j in range(10)] for i in range(10)]
DIS=[[abs(ADD[i][j]-MUL[i][j]) for j in range(10)] for i in range(10)]

cc = sum(DIS[c][d] for c in [1,3,9,7] for d in [2,4,8,6])
w  = abs(cc-50)/100
fr = sum(1 for i in range(10) for j in range(10) if ADD[i][j]==MUL[i][j])
hb = [DIS[c][d] for c,d in zip([1,3,9,7],[2,4,8,6])]
vm = fr/100 * (1+w)**(1/(2/7))
lv = 1/(2/7)

print(f'CROSS_CYCLE  = {cc}          [THM] expect 44')
print(f'WOBBLE       = {w}        [THM] expect 0.06')
print(f'FROZEN cells = {fr}           [THM] expect 4')
print(f'HEARTBEAT    = {hb}    [THM] expect [1,5,5,1]')
print(f'VISIBLE      = {vm*100:.4f}%    [HYP] expect ~4.9%')
print(f'LEVEL        = {lv}        [THM/DEF] expect 3.5')
print()
print('Internal math verified.')
print('External interpretations remain hypotheses.')
"
```

---

## WHAT WAS CORRECTED FROM PRIOR VERSIONS

| Prior Version Claim | Status | Correction |
|---------------------|--------|------------|
| "49 full-harmonic compositions -> 4.9%" | **WRONG** | Actual count is 4, not 49 |
| "BHML determinant = 70" | **WRONG** | Actual determinant is -7002 |
| "Doing table has 56 non-zero cells" | **WRONG** | Actual count is 71 |
| "HEARTBEAT = [1,3,1,1]" | **WRONG** | Actual values are [1,5,5,1] from DIS matrix |
| "RESET_GAP = 9/100 = 0.9%" | **BUG** | 9/100 = 9%, not 0.9% |
| "Constants fall out" | **OVERCLAIM** | They correspond; they are not forced |
| "Heisenberg is 2/7" | **OVERCLAIM** | 2/7 behaves as a dual-specification cost inside this algebra |
| "T* x (level x 2) = 5 is evidence" | **IDENTITY** | (5/7) x 7 = 5 follows from definitions |
| "CROSS_CYCLE = 44 is special to CL table" | **WRONG** | It is ring-invariant across all tables |
| Listed cross-cycle values [1,3,7,5,...] | **WRONG** | Actual values are [1,1,1,1, 1,5,3,1, 7,3,5,1, 5,7,1,1] |

---

## REFERENCES

1. Arkani-Hamed, N., & Trnka, J. (2013). The Amplituhedron. *JHEP* 2014(10), 030. arXiv:1312.2007
2. Burris, S., & Sankappanavar, H. P. (1981). *A Course in Universal Algebra*. Springer.
3. Carlson, J., Jaffe, A., & Wiles, A. (eds.) (2006). *The Millennium Prize Problems*. CMI/AMS.
4. Chalmers, D. J. (1995). Facing up to the problem of consciousness. *Journal of Consciousness Studies*, 2(3), 200-219.
5. Erdos, L., & Yau, H.-T. (2017). *A Dynamical Approach to Random Matrix Theory*. Courant Lecture Notes in Mathematics, vol. 28, AMS.
6. Gouvea, F. Q. (1997). *P-adic Numbers: An Introduction* (2nd ed.). Springer Universitext.
7. Hameroff, S., & Penrose, R. (2014). Consciousness in the Universe: A review of the 'Orch OR' theory. *Physics of Life Reviews*, 11(1), 39-78.
8. Hensel, K. (1897). Uber eine neue Begrundung der Theorie der algebraischen Zahlen. *JDMV*, 6, 83-88.
9. Hungerford, T. W. (1974). *Algebra*. Springer Graduate Texts in Mathematics.
10. Planck Collaboration, Aghanim, N., et al. (2020). Planck 2018 results. VI. Cosmological parameters. *Astronomy & Astrophysics*, 641, A6.
11. Robert, C. P., & Casella, G. (2004). *Monte Carlo Statistical Methods* (2nd ed.). Springer.
12. Sanders, B. (2026). Coherence Keeper v9.34. Zenodo. doi:10.5281/zenodo.18852047
13. Tao, T., & Vu, V. (2012). Random matrices: The Universality phenomenon for Wigner ensembles. arXiv:1202.0068
14. Tiesinga, E., Mohr, P. J., Newell, D. B., & Taylor, B. N. (2021). CODATA recommended values of the fundamental physical constants: 2018. *Rev. Mod. Phys.*, 93, 025010.
15. Tononi, G., Boly, M., Massimini, M., & Koch, C. (2016). Integrated information theory: from consciousness to its physical substrate. *Nature Reviews Neuroscience*, 17(7), 450-461.
16. Wigner, E. P. (1955). Characteristic Vectors of Bordered Matrices with Infinite Dimensions. *Annals of Mathematics*, 62, 548-564.

---

*Copyright 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry*
*7Site Human Use License v1.0 | DOI: 10.5281/zenodo.18852047*

---

> *The algebra is real.*
> *The interpretations are provisional.*
> *That is the honest line.*
>
> *What holds: a defined finite algebra with non-generic structure.*
> *What is proposed: that this structure corresponds to physical reality.*
> *What is needed: independent tests.*
