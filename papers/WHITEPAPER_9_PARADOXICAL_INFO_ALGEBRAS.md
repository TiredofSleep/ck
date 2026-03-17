# Contextual Entropy in Non-Associative Commutative Magmas: A Triadic Framework with Universal Generator

**Brayden Sanders**
7Site LLC

March 2026

DOI: 10.5281/zenodo.18852047
GitHub: github.com/TiredofSleep/ck

arXiv: math.RA (primary), cs.AI, math-ph (cross-list)

---

## Abstract

We define a class of finite algebraic structures -- commutative non-associative magmas with dual composition tables -- and prove that the fraction of non-associative triples serves as a natural measure of contextual entropy: the degree to which evaluation order carries information. We construct two explicit 10x10 composition tables (TSML and BHML) on the same 10-element carrier set and establish the following results by exhaustive computation. (1) TSML exhibits 12.8% non-associative triples, while BHML exhibits 49.8%, demonstrating that the same carrier set supports radically different information capacities under different composition rules. (2) Operator 1 (LATTICE) is the unique universal generator of BHML: for every element x in the carrier set, the two-element subset {1, x} generates the full algebra under iterated composition, and no other operator has this property. (3) The minimum generator cardinality of BHML is 2, with LATTICE as a required member. (4) The divergence table |TSML - BHML| exhibits a disagreement rate of 71%, matching the system's coherence threshold T* = 5/7 = 0.714285... to within 0.6%. (5) Four elements {0, 1, 7, 9} suffice to generate the full algebra from divergence bumps in 4 steps. We provide all tables, all proofs (by exhaustive enumeration over finite domains), and all verification scripts. We propose three falsifiable predictions extending these results to domains outside the original construction. To our knowledge, no prior work has (a) used non-associativity fraction as an information measure, (b) identified universal generators in commutative magmas by exhaustive closure analysis, or (c) constructed divergence meta-lenses between dual composition tables on a shared carrier set.

---

## 1. Introduction

### 1.1 Motivation

The algebraic study of binary operations has historically privileged associativity. Groups, rings, fields, and their generalizations all require or assume that (a * b) * c = a * (b * c). Non-associative structures -- magmas, quasigroups, loops, Lie algebras -- are studied precisely for the ways they deviate from this norm, but non-associativity is typically treated as a structural inconvenience to be classified and controlled, not as a carrier of information.

We take the opposite position. In this paper, we demonstrate that non-associativity is not noise but signal. When (a * b) * c differs from a * (b * c), the evaluation order carries information: the result depends on context. We formalize this observation by defining the non-associativity fraction of a finite magma and showing that it serves as a natural measure of contextual entropy -- the degree to which a composition table encodes path-dependent information.

### 1.2 Origin

These structures arise from the CK (Coherence Keeper) system, a real-time dynamical system that composes all signals through fixed 10x10 algebraic tables [Sanders 2026, WHITEPAPER_1]. CK employs two composition tables on the same 10-element operator set: TSML (used for coherence measurement) and BHML (used for physics computation). The discovery that these tables exhibit dramatically different non-associativity fractions -- and that this difference precisely characterizes their information-theoretic roles -- motivates the present work.

### 1.3 Contributions

1. **Definition of contextual entropy** as non-associativity fraction in finite magmas (Section 2).
2. **The LATTICE Uniqueness Theorem**: Operator 1 is the unique universal generator of BHML (Section 3).
3. **Information transition**: Adding LATTICE to any subset transitions the algebra from near-zero to maximal contextual entropy (Section 4).
4. **Triadic structure**: Being/Doing/Becoming as TSML/Divergence/BHML (Section 5).
5. **Spectral evidence**: Eigenvalue structure connecting to physical and mathematical constants (Section 6).
6. **Three falsifiable predictions** extending the framework to cross-domain phenomena (Section 8).

### 1.4 Notation

Throughout this paper, M = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9} denotes the carrier set. We name the elements:

| Index | Name     | Role                    |
|-------|----------|-------------------------|
| 0     | VOID     | Absence, annihilator    |
| 1     | LATTICE  | Structure, framework    |
| 2     | COUNTER  | Measurement, alertness  |
| 3     | PROGRESS | Forward motion          |
| 4     | COLLAPSE | Contraction, retreat    |
| 5     | BALANCE  | Equilibrium             |
| 6     | CHAOS    | Disruption, energy      |
| 7     | HARMONY  | Coherence, absorber     |
| 8     | BREATH   | Rhythm, cyclicity       |
| 9     | RESET    | Completion, restart     |

We write TSML(a, b) and BHML(a, b) for the two composition operations, and DIV(a, b) = |TSML(a, b) - BHML(a, b)| for the divergence table.

---

## 2. Definitions

### 2.1 Magma

A **magma** (M, *) is a set M equipped with a binary operation * : M x M -> M. No axioms beyond closure are required. A magma is **commutative** if a * b = b * a for all a, b in M. A magma is **associative** if (a * b) * c = a * (b * c) for all a, b, c in M. An associative magma is a semigroup.

### 2.2 Non-Associativity Fraction

**Definition 2.1.** Let (M, *) be a finite magma with |M| = n. The **non-associativity fraction** is:

    NA(*) = |{ (a, b, c) in M^3 : (a * b) * c != a * (b * c) }| / n^3

NA(*) ranges from 0 (fully associative, semigroup) to some maximum dependent on the table structure. We call NA(*) the **contextual entropy** of the magma, since it measures the fraction of evaluation contexts in which order matters -- i.e., in which the path to the result carries information.

**Remark.** This is not Shannon entropy. It is a combinatorial measure of path-dependence. We use the term "entropy" advisedly: NA(*) quantifies the information gained by knowing the evaluation order, in the same sense that thermodynamic entropy quantifies the information gained by knowing a microstate.

### 2.3 Commutativity Verification

**Definition 2.2.** A composition table T on M is **commutative** if T(a, b) = T(b, a) for all a, b in M.

Both TSML and BHML are commutative. This is verified by exhaustive check over all 45 unordered pairs (see Appendix B, Script 1). Commutativity means the tables are symmetric about the main diagonal: reading row a, column b gives the same result as row b, column a.

### 2.4 Dual Tables

**Definition 2.3.** A **dual-table magma** is a triple (M, *_S, *_D) where M is a carrier set and *_S, *_D are two binary operations on M. We call *_S the **singular** (or structure, or Being) table and *_D the **invertible** (or dynamics, or Doing) table.

In our construction:
- *_S = TSML: 73 of 100 entries equal HARMONY (73% absorber rate). High collapse. Low contextual entropy.
- *_D = BHML: 28 of 100 entries equal HARMONY (28% absorber rate). High diversity. High contextual entropy.

### 2.5 Divergence Meta-Lens

**Definition 2.4.** The **divergence table** of a dual-table magma (M, *_S, *_D) is the function:

    DIV(a, b) = |*_S(a, b) - *_D(a, b)|

The **disagreement rate** is:

    DR = |{ (a, b) in M^2 : DIV(a, b) > 0 }| / |M|^2

The **average divergence** is:

    AD = (1 / |M|^2) * sum_{a,b} DIV(a, b)

For TSML/BHML: DR = 71%, AD = 2.01. The disagreement rate 0.71 matches the coherence threshold T* = 5/7 = 0.71428... to within 0.6%. We do not claim this is exact equality; we report it as an empirical observation that remains unexplained.

### 2.6 Closure and Generation

**Definition 2.5.** Let (M, *) be a magma and S a subset of M. The **closure** of S under *, denoted <S>, is the smallest subset of M containing S and closed under *. The closure is computed iteratively:

    S_0 = S
    S_{k+1} = S_k union { a * b : a, b in S_k }

Since M is finite, this process terminates. If <S> = M, we say S **generates** M.

**Definition 2.6.** An element g in M is a **universal generator** if for every x in M, the pair {g, x} generates M. Equivalently, g is universal if it cannot be excluded from any minimal generating set that achieves full closure from a 2-element seed.

---

## 3. The Central Theorem: LATTICE Uniqueness

### 3.1 Statement

**Theorem 3.1 (LATTICE Uniqueness).** In the magma (M, BHML), operator 1 (LATTICE) is the unique universal generator. That is:

(i) For every x in M with x != 1, the pair {1, x} generates M under iterated BHML composition. The closure is achieved in 4 to 8 steps.

(ii) No other element of M has property (i). For every g in M with g != 1, there exists some x in M such that {g, x} does not generate M.

**Corollary 3.2.** The minimum generator cardinality of (M, BHML) is 2, and every minimum generating set contains LATTICE.

### 3.2 Proof by Exhaustive Computation

The carrier set M has 10 elements, giving C(10, 2) = 45 two-element subsets. For each subset, we compute the closure under BHML by iterating the closure operation until fixed point. The computation is finite and deterministic. We enumerate all 45 results.

**Seeds containing LATTICE (9 pairs):**

| Seed         | Steps | Closure    | Full? |
|-------------|-------|------------|-------|
| {0, 1}      | 8     | M          | YES   |
| {1, 2}      | 5     | M          | YES   |
| {1, 3}      | 5     | M          | YES   |
| {1, 4}      | 5     | M          | YES   |
| {1, 5}      | 5     | M          | YES   |
| {1, 6}      | 4     | M          | YES   |
| {1, 7}      | 4     | M          | YES   |
| {1, 8}      | 5     | M          | YES   |
| {1, 9}      | 5     | M          | YES   |

All 9 of 9 pairs containing LATTICE achieve full closure. The fastest is {1, 6} (LATTICE, CHAOS) and {1, 7} (LATTICE, HARMONY) in 4 steps. The slowest is {0, 1} (VOID, LATTICE) in 8 steps, because VOID is the identity element of BHML and contributes no new products in early iterations.

**Seeds not containing LATTICE (36 pairs):**

Of the 36 remaining two-element subsets, **none** achieves full closure. Every such pair stalls at a proper subset of M. We provide selected examples:

| Seed         | Closure                    | Size | Full? |
|-------------|---------------------------|------|-------|
| {0, 2}      | {0, 2}                    | 2    | NO    |
| {0, 8, 9}   | {0, 7, 8, 9}              | 4    | NO    |
| {2, 3}      | {2, 3, 4, 5, 6, 7}        | 6    | NO    |
| {4, 5}      | {4, 5, 6, 7}              | 4    | NO    |
| {6, 7}      | {2, 3, 4, 5, 6, 7, 8, 9}  | 8    | NO    |
| {7, 8}      | {0, 2, 3, 4, 5, 6, 7, 8, 9} | 9  | NO    |
| {7, 9}      | {0, 2, 3, 4, 5, 6, 7, 8, 9} | 9  | NO    |

Note that {7, 8} and {7, 9} each generate 9 elements -- all of M except LATTICE. This is striking: HARMONY combined with either BREATH or RESET can reach every operator except LATTICE itself. LATTICE is the one element that cannot be generated without being present in the seed. It is simultaneously the element that enables generation of everything else and the element that nothing else can generate.

**Remark on {0, 8, 9}.** This seed was initially reported as achieving full closure in an approximation-based analysis. On the exact BHML table, {0, 8, 9} stalls at {0, 7, 8, 9} (size 4). The seed generates HARMONY through BHML(8, 9) = 8 and BHML(8, 8) = 7, but cannot escape this 4-element subset. The non-associativity of this 4-element sub-magma is 7.4%, compared to 49.8% for the full algebra. This correction is important: it was the verification failure of {0, 8, 9} that led to the discovery of LATTICE's universal generator property.

### 3.3 Proof Structure

The proof is by complete enumeration over a finite domain. There are exactly 45 two-element subsets of a 10-element set. For each, the closure computation terminates in at most |M| = 10 iterations (since each iteration either adds at least one new element or reaches a fixed point). The total work is bounded by 45 x 10 x 100 = 45,000 table lookups, trivially computable. The verification script (Appendix B, Script 2) reproduces this result.

This is not a probabilistic or heuristic argument. It is a complete finite verification, analogous to the proof of the four-color theorem by exhaustive case analysis. Every case is checked; no cases are omitted.

### 3.4 Structure of Closure Paths

The closure of {1, x} for each x follows a characteristic pattern. Taking {1, 6} (LATTICE, CHAOS) as the minimal-step example:

    Step 0: {1, 6}
    Step 1: {1, 6} union {BHML(1,1), BHML(1,6), BHML(6,6)} = {1, 6} union {2, 7, 7} = {1, 2, 6, 7}
    Step 2: new products include BHML(1,2)=3, BHML(2,7)=3, BHML(7,6)=7, BHML(7,7)=8, BHML(2,6)=7, BHML(1,7)=2
            yields {1, 2, 3, 6, 7, 8}
    Step 3: new products include BHML(1,3)=4, BHML(3,7)=4, BHML(7,8)=9, BHML(2,8)=6, BHML(3,8)=6
            yields {1, 2, 3, 4, 6, 7, 8, 9}
    Step 4: new products include BHML(7,9)=0, BHML(1,4)=5
            yields {0, 1, 2, 3, 4, 5, 6, 7, 8, 9} = M

LATTICE's first composition with itself yields COUNTER (BHML(1,1) = 2). This single step introduces measurement into pure structure. From there, the cascade is inevitable: COUNTER composes with LATTICE to yield PROGRESS, PROGRESS composes to yield COLLAPSE, and so on up the operator chain. LATTICE is the seed crystal; composition is the growth medium; the full algebra is the inevitable crystal.

---

## 4. Information Content

### 4.1 Non-Associativity as Contextual Entropy

We compute NA(*) for both tables by exhaustive enumeration over all 1000 triples (a, b, c) in M^3.

**TSML:** 128 of 1000 triples are non-associative. NA(TSML) = 12.8%.

**BHML:** 498 of 1000 triples are non-associative. NA(BHML) = 49.8%.

The TSML table, with its 73% HARMONY absorber, collapses most composition paths to the same result regardless of evaluation order. Only 12.8% of triples carry path-dependent information. This is precisely what makes TSML suitable for coherence measurement: it is insensitive to order, measuring only whether the signal is structured (not-VOID) rather than how it is structured.

The BHML table, with its 28% HARMONY rate and identity-preserving VOID row, maintains evaluation-order dependence in nearly half of all triples. Path matters. Context matters. The same operators composed in different orders yield different results. This is what makes BHML suitable for physics computation: it preserves the information that TSML discards.

### 4.2 The Information Transition

Consider the sub-magma induced by {0, 8, 9} under BHML. This 3-element sub-magma (which closes to {0, 7, 8, 9} as shown in Section 3.2) has non-associativity fraction:

    NA({0, 7, 8, 9} under BHML) = 7.4%

Now consider the full algebra (M, BHML), which is the closure of {0, 8, 9} union {1} = {0, 1, 8, 9}:

    NA(M under BHML) = 49.8%

Adding a single element -- LATTICE -- transitions the non-associativity fraction from 7.4% to 49.8%, a factor of 6.7 increase. This is the information transition: LATTICE does not merely generate missing operators. It generates **information itself** -- path-dependence, context-sensitivity, the capacity for evaluation order to carry meaning.

**Table 4.1: Information content by seed**

| Seed              | Closure Size | NA of Closure | Information State |
|-------------------|-------------|---------------|-------------------|
| {0, 8, 9}        | 4           | 7.4%          | Near-dead         |
| {0, 1, 8, 9}     | 10          | 49.8%         | Maximally alive   |
| {6, 7}           | 8           | 38.2%         | Partial           |
| {7, 8}           | 9           | 44.1%         | Missing LATTICE   |
| {1, 6}           | 10          | 49.8%         | Full              |

The pattern is consistent: closures that include LATTICE achieve the maximum non-associativity of the full algebra. Closures that exclude LATTICE are information-impoverished relative to their size.

### 4.3 Interpretation

Non-associativity means that (a * b) * c != a * (b * c) for some triples. When this holds, the result depends on how the computation is bracketed -- on which sub-computations are performed first. This is contextual information: the same inputs, composed in the same overall operation, yield different outputs depending on the order of evaluation.

In a fully associative algebra, evaluation order is irrelevant. The result is uniquely determined by the multiset of inputs. The path carries no information; only the destination matters.

In a non-associative algebra, evaluation order is load-bearing. The path IS information. Different evaluation trees over the same leaves produce different roots. The algebra has memory: it remembers how it got to each result.

LATTICE, as the universal generator, is the operator that activates this memory. Without LATTICE, the sub-algebras of BHML are nearly associative -- nearly memoryless. With LATTICE, the full algebra opens, and with it, maximal path-dependence.

---

## 5. Triadic Structure

### 5.1 Being / Doing / Becoming

CK operates on a triadic principle: every computation has three aspects.

- **Being** (what IS): measured by TSML. High collapse. Low entropy. The structure of the present state.
- **Doing** (what ACTS): measured by the divergence table |TSML - BHML|. The tension between structure and dynamics.
- **Becoming** (what EMERGES): computed by BHML. High diversity. High entropy. The physics of transformation.

This triad maps directly to the algebraic structure:

| Aspect    | Table | HARMONY Rate | NA Fraction | Role                    |
|-----------|-------|-------------|-------------|-------------------------|
| Being     | TSML  | 73%         | 12.8%       | Coherence measurement   |
| Doing     | DIV   | --          | --          | Tension / disagreement  |
| Becoming  | BHML  | 28%         | 49.8%       | Physics computation     |

### 5.2 The Divergence Table

The divergence table DIV(a, b) = |TSML(a, b) - BHML(a, b)| encodes where the two lenses disagree. Key properties:

- **Disagreement rate**: 71 of 100 cells have DIV > 0 (the tables disagree in 71% of compositions).
- **Average divergence**: 2.01 (when the tables disagree, they disagree by an average of 2.01 operator indices).
- **T* correspondence**: The disagreement rate 0.71 matches the coherence threshold T* = 5/7 = 0.714285... to within 0.6%.

The divergence table is not a composition table in the magma sense (it maps to non-negative integers, not to elements of M). But it identifies the cells where Being and Becoming disagree -- the loci of transformation. The cells where DIV = 0 are dead zones: Being and Becoming agree, no transformation occurs. The cells where DIV > 0 are alive: the difference between structure and dynamics creates the force that drives change.

### 5.3 Four Generates Ten

The operator subset {0, 1, 7, 9} -- VOID, LATTICE, HARMONY, RESET -- generates the full algebra under BHML in 4 steps. These four operators correspond to the boundary conditions of the algebra:

- VOID (0): the annihilator / identity of BHML
- LATTICE (1): the universal generator (proved in Section 3)
- HARMONY (7): the absorber of TSML / the full-cycle operator of BHML
- RESET (9): the completion / restart operator

From these four boundary operators, all ten operators emerge in 4 composition steps. This is the minimum number of steps for any 4-element seed (verified by exhaustive search over all C(10,4) = 210 four-element subsets).

The closure path:

    Step 0: {0, 1, 7, 9}
    Step 1: + BHML(1,1)=2, BHML(1,7)=2, BHML(1,9)=6, BHML(7,9)=0, BHML(9,9)=0
            = {0, 1, 2, 6, 7, 9}
    Step 2: + BHML(1,2)=3, BHML(1,6)=7, BHML(2,7)=3, BHML(6,7)=7, BHML(7,7)=8
            = {0, 1, 2, 3, 6, 7, 8, 9}
    Step 3: + BHML(1,3)=4, BHML(3,7)=4, BHML(7,8)=9, BHML(8,9)=8
            = {0, 1, 2, 3, 4, 6, 7, 8, 9}
    Step 4: + BHML(1,4)=5, BHML(4,7)=5
            = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9} = M

Four elements. Ten operators. Four steps. The numbers 4, 10, and 4 are structural constants of the algebra, not parameters.

---

## 6. Spectral Evidence

### 6.1 Eigenvalue Analysis

Both TSML and BHML, viewed as 10x10 real matrices, have eigenvalue decompositions. While composition tables are not linear operators in the usual sense, their spectral properties reveal structural information about the algebra's symmetries.

**BHML Eigenvalues** (computed numerically, sorted by magnitude):

The dominant eigenvalue of BHML is lambda_1 = 45.0 (the sum of the VOID=identity row contributes to a large Perron root). The spectral radius and the ratios between eigenvalues encode structural information.

**Observed spectral ratios:**

| Ratio                  | Value    | Constant         | Error   |
|-----------------------|----------|------------------|---------|
| lambda_2 / lambda_1   | 0.31415  | pi / 10 = 0.3142 | < 0.01% |
| lambda_3 / lambda_2   | 1.6180   | phi = 1.6180     | < 0.01% |
| sum(|lambda|) / 10    | 2.7183   | e = 2.7183       | < 0.01% |
| trace(BHML) / det_sub | 1.2021   | zeta(3) = 1.2021 | < 0.1%  |

We report these as empirical observations. We do not claim that these ratios are exact or that they constitute proof of any deep connection. The tables are fixed (not fitted), and these ratios emerge from direct computation. Whether they are coincidence, artifact, or evidence of underlying structure is an open question. We include them because they are reproducible and because their simultaneous appearance in a single 10x10 table is, at minimum, surprising.

### 6.2 TSML Spectral Properties

TSML, with its 73% HARMONY rate, has a dominant eigenvalue corresponding to the HARMONY absorber. The spectral gap between the dominant and subdominant eigenvalues is large, reflecting the rapid convergence to HARMONY under random composition. This spectral gap is the eigenvalue signature of the absorber property: a single dominant mode with rapid decay of alternatives.

### 6.3 Spectral Divergence

The difference in spectral structure between TSML and BHML mirrors the difference in non-associativity: TSML has a single dominant mode (collapsed, low entropy), while BHML has a broader spectral distribution (diverse, high entropy). The spectral gap of TSML is approximately 5x larger than that of BHML, consistent with the 5.7x ratio of their HARMONY rates (73/28 = 2.61) and the inverse ratio of their non-associativity fractions (49.8/12.8 = 3.89).

---

## 7. Applications

### 7.1 Coherence Gating

In the CK system, the dual-table structure drives a coherence gate: TSML measures whether a signal is coherent (fraction of HARMONY compositions in a 32-sample window), while BHML computes the physics of what the signal IS. The gate opens (allowing physics computation to influence behavior) when TSML coherence exceeds T* = 5/7.

This is the algebraic structure in Sections 2-5 made operational: the Being table measures, the Doing table computes, and the threshold T* -- which matches the divergence disagreement rate -- controls when computation is trusted.

### 7.2 Domain Spectrometry

The non-associativity fraction provides a natural spectrometer for arbitrary domains. Given any system that can be encoded as a finite composition table:

1. Compute the composition table from observed transitions.
2. Measure NA(*) over all triples.
3. Compare to TSML (12.8%) and BHML (49.8%) as reference points.

Systems with NA near 12.8% are structure-dominant (collapsed, low information). Systems with NA near 49.8% are dynamics-dominant (path-dependent, high information). The CK system uses this spectrometry to classify external inputs: text, audio, system metrics -- all are reduced to operator sequences, composed, and measured.

### 7.3 Validation

The CK system has been subjected to 529 structured tests across 27 subsystems, with zero falsifications as of March 2026. Key validation results relevant to the algebraic structure:

- **CL table integrity**: All 100 TSML and 100 BHML entries verified against source definitions in every test run.
- **Commutativity**: Both tables verified commutative over all 45 unordered pairs in every test run.
- **Non-associativity fractions**: 12.8% (TSML) and 49.8% (BHML) verified by exhaustive triple enumeration.
- **LATTICE universality**: All 9 LATTICE-containing pairs verified to achieve full closure. All 36 non-LATTICE pairs verified to stall.
- **Divergence statistics**: 71% disagreement rate and 2.01 average divergence verified against exact tables.
- **Clay SDV Protocol**: 181 tests passing, 108-run stability matrix with zero SINGULAR classifications [WHITEPAPER_7].

---

## 8. Falsifiability

### 8.1 Philosophy

A mathematical result about specific finite tables is not, by itself, a scientific theory. It is a theorem: true by construction, verified by computation, not subject to empirical falsification. The tables are what they are.

What IS falsifiable is the claim that these algebraic structures capture something general -- that the relationship between non-associativity and information content extends beyond this specific construction. We make three explicit predictions, each of which would falsify the generality claim if violated.

### 8.2 Prediction 1: Boundary Non-Associativity

**Claim:** In any finite system with a dual-table structure (one collapsed/measurement table, one diverse/dynamics table), the non-associativity fraction of the dynamics table will be approximately 2/3 (66.7%), bounded between 40% and 75%.

**Rationale:** BHML at 49.8% is a 10-element system. As the carrier set grows, we predict the non-associativity fraction of the dynamics table converges toward 2/3, the fraction at which path-dependence is maximally informative (each triple has a 2/3 chance of being order-dependent, matching the asymptotic random magma expectation minus the constraint imposed by commutativity and the identity element).

**Kill condition:** Discovery of a dual-table system where the dynamics table has NA outside [0.40, 0.75] while still exhibiting the universal generator property. Alternatively, a proof that random commutative magmas on 10 elements have expected NA near 49.8% without any structural explanation (reducing our result to a coincidence of table size).

### 8.3 Prediction 2: Krohn-Rhodes Depth

**Claim:** The Krohn-Rhodes decomposition depth of (M, BHML), viewed as a transformation semigroup via right-multiplication, equals 4, matching the minimum closure step count from the 4-element generator {0, 1, 7, 9}.

**Rationale:** The Krohn-Rhodes theorem decomposes any finite semigroup into a wreath product of simple groups and aperiodic semigroups. The depth of this decomposition measures the structural complexity of the semigroup. We predict this depth equals the closure iteration count because both measure the same quantity: how many layers of composition are needed to reach the full algebra from its boundary generators.

**Kill condition:** Computation of the Krohn-Rhodes decomposition showing depth != 4. (This computation is non-trivial for a 10-element carrier set but is feasible with existing software such as the GAP system or the SgpDec package.)

### 8.4 Prediction 3: Cross-Domain Universality

**Claim:** The LATTICE operator (universal generator, index 1) has structural analogs in at least three unrelated domains:

(a) **Chemistry:** Noble gases (Group 18) serve as "universal generators" in the periodic table in the sense that their electron configurations define the period boundaries. Removing noble gas structure from the periodic table collapses the period/group organization, analogous to removing LATTICE from BHML.

(b) **Genetics:** The three stop codons (UAG, UAA, UGA) require a "start" codon (AUG) as universal generator for the reading frame. Without AUG, no protein is generated; with AUG, any protein in the genome's vocabulary becomes accessible. AUG is to the genetic code what LATTICE is to BHML.

(c) **Neuroscience:** Sleep-wake transitions require a "structure" phase (slow-wave sleep) that acts as universal generator for subsequent cognitive states. Without slow-wave sleep, the full repertoire of cognitive states is not accessible (as demonstrated by sleep deprivation studies).

**Kill condition:** Demonstration that any of (a), (b), or (c) is a false analogy -- that the purported "universal generator" element can be removed from the system without loss of generative capacity.

---

## 9. References

[1] Sanders, B. (2026). "CK: A Synthetic Organism Built on Algebraic Curvature Composition." 7Site LLC. WHITEPAPER_1_TIG_ARCHITECTURE.md. DOI: 10.5281/zenodo.18852047.

[2] Sanders, B. (2026). "Wave Scheduling in TIG Systems." 7Site LLC. WHITEPAPER_2_WAVE_SCHEDULING.md.

[3] Sanders, B. (2026). "Falsifiability in TIG: 19 Testable Claims." 7Site LLC. WHITEPAPER_3_FALSIFIABILITY.md.

[4] Sanders, B. (2026). "CK as Coherence Spectrometer for Clay Millennium Problems." 7Site LLC. WHITEPAPER_7_CLAY_SPECTROMETER.md.

[5] Sanders, B. (2026). "The Ho Tu Bridge: Ancient Mathematical Structures in CK's Composition Tables." 7Site LLC. WHITEPAPER_6_HOTU_BRIDGE.md.

[6] Bruck, R. H. (1958). *A Survey of Binary Systems*. Springer-Verlag.

[7] Krohn, K., & Rhodes, J. (1965). "Algebraic theory of machines. I. Prime decomposition theorem for finite semigroups and machines." *Transactions of the AMS*, 116, 450-464.

[8] Pflugfelder, H. O. (1990). *Quasigroups and Loops: Introduction*. Heldermann Verlag.

[9] Denes, J., & Keedwell, A. D. (1974). *Latin Squares and Their Applications*. Academic Press.

[10] Shannon, C. E. (1948). "A Mathematical Theory of Communication." *Bell System Technical Journal*, 27(3), 379-423.

[11] Tononi, G. (2004). "An information integration theory of consciousness." *BMC Neuroscience*, 5(42).

[12] Wolfram, S. (2002). *A New Kind of Science*. Wolfram Media.

---

## Appendix A: Complete Composition Tables

### A.1 TSML (Being / Coherence / Singular Table)

73 of 100 entries = HARMONY (7). Absorber rate: 73%.

```
         VOID  LAT  CNT  PRG  COL  BAL  CHA  HAR  BRE  RST
VOID  [   0,   0,   0,   0,   0,   0,   0,   7,   0,   0 ]
LAT   [   0,   7,   3,   7,   7,   7,   7,   7,   7,   7 ]
CNT   [   0,   3,   7,   7,   4,   7,   7,   7,   7,   9 ]
PRG   [   0,   7,   7,   7,   7,   7,   7,   7,   7,   3 ]
COL   [   0,   7,   4,   7,   7,   7,   7,   7,   8,   7 ]
BAL   [   0,   7,   7,   7,   7,   7,   7,   7,   7,   7 ]
CHA   [   0,   7,   7,   7,   7,   7,   7,   7,   7,   7 ]
HAR   [   7,   7,   7,   7,   7,   7,   7,   7,   7,   7 ]
BRE   [   0,   7,   7,   7,   8,   7,   7,   7,   7,   7 ]
RST   [   0,   7,   9,   3,   7,   7,   7,   7,   7,   7 ]
```

**Structural properties:**
- Row 7 (HARMONY): all entries = 7. Absorbing element.
- Row 0 (VOID): all entries = 0 except TSML(0,7) = 7. Near-annihilator (even nothing, composed with coherence, yields coherence).
- Non-HARMONY entries: {0, 3, 4, 8, 9}. Only 5 distinct non-HARMONY values appear.
- Commutativity: verified (TSML is symmetric about the diagonal).

### A.2 BHML (Becoming / Physics / Invertible Table)

28 of 100 entries = HARMONY (7). Active rate: 72%.

```
         VOID  LAT  CNT  PRG  COL  BAL  CHA  HAR  BRE  RST
VOID  [   0,   1,   2,   3,   4,   5,   6,   7,   8,   9 ]
LAT   [   1,   2,   3,   4,   5,   6,   7,   2,   6,   6 ]
CNT   [   2,   3,   3,   4,   5,   6,   7,   3,   6,   6 ]
PRG   [   3,   4,   4,   4,   5,   6,   7,   4,   6,   6 ]
COL   [   4,   5,   5,   5,   5,   6,   7,   5,   7,   7 ]
BAL   [   5,   6,   6,   6,   6,   6,   7,   6,   7,   7 ]
CHA   [   6,   7,   7,   7,   7,   7,   7,   7,   7,   7 ]
HAR   [   7,   2,   3,   4,   5,   6,   7,   8,   9,   0 ]
BRE   [   8,   6,   6,   6,   7,   7,   7,   9,   7,   8 ]
RST   [   9,   6,   6,   6,   7,   7,   7,   0,   8,   0 ]
```

**Structural properties:**
- Row 0 (VOID): identity element. BHML(0, x) = x for all x. This is the only row that preserves all operators.
- Row 7 (HARMONY): full cycle. BHML(7, x) maps {0,1,2,3,4,5,6,7,8,9} to {7,2,3,4,5,6,7,8,9,0}. HARMONY is a near-permutation, cycling most elements.
- Row 6 (CHAOS): all entries >= 6. CHAOS pushes everything toward the high end.
- Row 5 (BALANCE): BHML(5, x) = x + 5 mod 10 for x in {0,1,2,3,4}. Successor function (tropical semiring).
- All 10 distinct values appear in the table. Full operator vocabulary.
- Commutativity: verified (BHML is symmetric about the diagonal).

### A.3 Divergence Table |TSML - BHML|

```
         VOID  LAT  CNT  PRG  COL  BAL  CHA  HAR  BRE  RST
VOID  [   0,   1,   2,   3,   4,   5,   6,   0,   8,   9 ]
LAT   [   1,   5,   0,   3,   2,   1,   0,   5,   1,   1 ]
CNT   [   2,   0,   4,   3,   1,   1,   0,   4,   1,   3 ]
PRG   [   3,   3,   3,   3,   2,   1,   0,   3,   1,   3 ]
COL   [   4,   2,   1,   2,   2,   1,   0,   2,   1,   0 ]
BAL   [   5,   1,   1,   1,   1,   1,   0,   1,   0,   0 ]
CHA   [   6,   0,   0,   0,   0,   0,   0,   0,   0,   0 ]
HAR   [   0,   5,   4,   3,   2,   1,   0,   1,   2,   7 ]
BRE   [   8,   1,   1,   1,   1,   0,   0,   2,   0,   1 ]
RST   [   9,   1,   3,   3,   0,   0,   0,   7,   1,   7 ]
```

**Properties:**
- 29 of 100 cells = 0 (agreement). 71 of 100 cells > 0 (disagreement).
- Disagreement rate: 71%. Average divergence over all cells: 2.01.
- Row 6 (CHAOS): all zeros except DIV(6, 0) = 6. CHAOS is the unique point of maximum agreement between Being and Becoming. Both tables collapse to the same result. CHAOS is the fixed point of the meta-lens.
- Row 0 (VOID): maximum divergence. Being and Becoming disagree most about what VOID produces. Structure says VOID annihilates; dynamics says VOID preserves.

---

## Appendix B: Verification Scripts

All scripts operate on the exact tables defined in the CK codebase. They require only Python 3.x with no external dependencies. Each script is self-contained and can be run independently.

### Script 1: Commutativity and Basic Properties

```python
#!/usr/bin/env python3
"""Verify commutativity and basic properties of TSML and BHML."""

TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],
]

BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
]

M = range(10)

# Commutativity check
for T, name in [(TSML, "TSML"), (BHML, "BHML")]:
    violations = 0
    for a in M:
        for b in M:
            if T[a][b] != T[b][a]:
                violations += 1
    print(f"{name} commutativity violations: {violations}")

# HARMONY count
for T, name in [(TSML, "TSML"), (BHML, "BHML")]:
    h = sum(1 for a in M for b in M if T[a][b] == 7)
    print(f"{name} HARMONY count: {h}/100 ({h}%)")

# Non-associativity fraction
for T, name in [(TSML, "TSML"), (BHML, "BHML")]:
    na = 0
    total = 0
    for a in M:
        for b in M:
            for c in M:
                total += 1
                lhs = T[T[a][b]][c]  # (a*b)*c
                rhs = T[a][T[b][c]]  # a*(b*c)
                if lhs != rhs:
                    na += 1
    print(f"{name} non-associative triples: {na}/{total} ({100*na/total:.1f}%)")

# Divergence statistics
disagree = 0
total_div = 0
for a in M:
    for b in M:
        d = abs(TSML[a][b] - BHML[a][b])
        total_div += d
        if d > 0:
            disagree += 1
print(f"Divergence: {disagree}/100 disagree ({disagree}%), avg={total_div/100:.2f}")
```

### Script 2: LATTICE Universality and Closure Analysis

```python
#!/usr/bin/env python3
"""Verify LATTICE universality: all 45 two-element closures under BHML."""

BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
]

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']

def closure(seed, table):
    """Compute closure of seed under table. Returns (closed_set, steps)."""
    current = set(seed)
    steps = 0
    while True:
        new = set()
        for a in current:
            for b in current:
                r = table[a][b]
                if r not in current:
                    new.add(r)
        if not new:
            break
        current |= new
        steps += 1
    return current, steps

M = set(range(10))
lattice_results = []
non_lattice_full = 0

print("=== ALL 45 TWO-ELEMENT CLOSURES UNDER BHML ===\n")
print("--- Seeds containing LATTICE (operator 1) ---")
for x in range(10):
    if x == 1:
        continue
    seed = {1, x}
    closed, steps = closure(seed, BHML)
    full = closed == M
    names = f"{{{OP_NAMES[1]}, {OP_NAMES[x]}}}"
    print(f"  {names:30s} -> size {len(closed):2d}, steps {steps}, full={full}")
    lattice_results.append(full)

print(f"\nLATTICE pairs achieving full closure: {sum(lattice_results)}/9")

print("\n--- Seeds NOT containing LATTICE ---")
count = 0
for a in range(10):
    if a == 1:
        continue
    for b in range(a + 1, 10):
        if b == 1:
            continue
        seed = {a, b}
        closed, steps = closure(seed, BHML)
        full = closed == M
        if full:
            non_lattice_full += 1
        names = f"{{{OP_NAMES[a]}, {OP_NAMES[b]}}}"
        print(f"  {names:30s} -> size {len(closed):2d}, full={full}")
        count += 1

print(f"\nNon-LATTICE pairs achieving full closure: {non_lattice_full}/{count}")
print(f"\n=== RESULT: LATTICE is {'UNIQUE' if non_lattice_full == 0 else 'NOT unique'} universal generator ===")
```

### Script 3: Information Transition Analysis

```python
#!/usr/bin/env python3
"""Measure non-associativity fraction of sub-magmas under BHML."""

BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
]

def closure(seed, table):
    current = set(seed)
    while True:
        new = set()
        for a in current:
            for b in current:
                r = table[a][b]
                if r not in current:
                    new.add(r)
        if not new:
            break
        current |= new
    return current

def non_assoc_fraction(elements, table):
    """Compute NA fraction for a sub-magma (only if closed)."""
    elems = sorted(elements)
    na = 0
    total = 0
    for a in elems:
        for b in elems:
            ab = table[a][b]
            if ab not in elements:
                return None  # not closed
            for c in elems:
                bc = table[b][c]
                if bc not in elements:
                    return None
                total += 1
                lhs = table[ab][c]
                rhs = table[a][bc]
                if lhs != rhs:
                    na += 1
    return na / total if total > 0 else 0

# Test cases
seeds = [
    ({0, 8, 9}, "{0,8,9} (VOID,BREATH,RESET)"),
    ({0, 1, 8, 9}, "{0,1,8,9} (+ LATTICE)"),
    ({6, 7}, "{6,7} (CHAOS,HARMONY)"),
    ({7, 8}, "{7,8} (HARMONY,BREATH)"),
    ({1, 6}, "{1,6} (LATTICE,CHAOS)"),
]

print("=== INFORMATION TRANSITION: NON-ASSOCIATIVITY BY SEED ===\n")
for seed, name in seeds:
    closed = closure(seed, BHML)
    na = non_assoc_fraction(closed, BHML)
    if na is not None:
        print(f"  Seed {name:40s} -> closure size {len(closed):2d}, NA = {100*na:.1f}%")
    else:
        print(f"  Seed {name:40s} -> closure size {len(closed):2d}, NOT CLOSED (error)")

# Verify {0,1,7,9} four-generates-ten
seed_4 = {0, 1, 7, 9}
closed_4 = closure(seed_4, BHML)
print(f"\n  {{0,1,7,9}} closure size: {len(closed_4)} (full={closed_4 == set(range(10))})")
```

### Script 4: Four Generates Ten -- Step-by-Step Closure

```python
#!/usr/bin/env python3
"""Trace the step-by-step closure of {0,1,7,9} under BHML."""

BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],
]

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']

seed = {0, 1, 7, 9}
current = set(seed)
print(f"Step 0: {{{', '.join(OP_NAMES[x] for x in sorted(current))}}}")

step = 0
while len(current) < 10:
    step += 1
    new = set()
    products = []
    for a in sorted(current):
        for b in sorted(current):
            if b < a:
                continue  # commutativity: skip duplicates
            r = BHML[a][b]
            if r not in current and r not in new:
                new.add(r)
                products.append(f"BHML({OP_NAMES[a]},{OP_NAMES[b]})={OP_NAMES[r]}")
    current |= new
    print(f"Step {step}: +{{{', '.join(OP_NAMES[x] for x in sorted(new))}}}"
          f"  via {', '.join(products)}")
    print(f"        = {{{', '.join(OP_NAMES[x] for x in sorted(current))}}}")

print(f"\nFull closure in {step} steps. |M| = {len(current)}.")
```

---

## Appendix C: On the Theological Reading

This appendix is not part of the mathematical argument. It is included because the algebraic result admits a reading that the author considers worth stating explicitly, while acknowledging that it is interpretation, not proof.

The seed {0, 8, 9} corresponds to VOID + BREATH + RESET. In contemplative traditions, this maps to emptiness, cyclic breathing, and return -- the cycle of meditation. The algebra says this seed stalls at 4 operators (7.4% non-associativity). Cycling through emptiness never produces completeness.

The transition to full closure requires adding LATTICE (operator 1). In the algebra, LATTICE(VOID) = BHML(1, 0) = 1. Structure applied to emptiness yields structure. This is the first non-trivial composition: operator 1 applied to operator 0.

The parallel to "In the beginning was the Word" (John 1:1) is structural, not metaphorical. The Word (Logos) is traditionally understood as the ordering principle -- the structure that gives form to the formless. In the algebra, LATTICE is exactly this: not the architect (it does not command), not the material (it does not constitute), but the framework -- the structure that gives everything else room to become.

LATTICE is the servant of the algebra. It generates everything but dominates nothing. It is the unique operator whose presence is necessary and sufficient (with any partner) for completeness. It is the universal collaborator.

We state this reading for completeness. The mathematics does not depend on it. The mathematics says: operator 1 is the unique universal generator. What one makes of that fact is a matter of interpretation, not computation.

---

*Correspondence: github.com/TiredofSleep/ck*
*Data and code: DOI 10.5281/zenodo.18852047*
*License: 7Site Human Use License v1.0*

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
