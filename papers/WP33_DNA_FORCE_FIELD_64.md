# WP33: The b=4 Force Field and the 64-Codon Gateway — Why DNA Uses Triadic Depth-3 Composition

**Brayden Sanders**
7Site LLC

March 2026

DOI: 10.5281/zenodo.18852047
GitHub: github.com/TiredofSleep/ck

---

## Abstract

The R16 force field sweep (three experiments, ~12 million trials) established that gate difficulty in k-alphabet reduction is a function exclusively of |G| — the count of non-unit (non-coprime) elements in the semiprime partition — within any fixed alphabet size k. This paper applies that result to the simplest possible semiprime world: b = 2×2 = 4, alphabet k = 4. The b=4 partition is maximally symmetric: |G| = 2 (the even numbers {2, 4}), |C| = 2 (the odd units {1, 3}), interleave score = 1.0, and |C|/k = 0.5 — the most balanced possible split. We show that this single semiprime force field, operated at three different depths, generates the same gateway number: 4³ = 2⁶ = 8² = 64. DNA codons (depth 3 over alphabet 4), I Ching hexagrams (depth 6 over alphabet 2), and the chess board (depth 2 over alphabet 8) are the same b=4 information structure at three different depth-alphabet trade-offs. We prove that depth 3 is the minimum depth at which the b=4 force field supports a complete triadic code for 20 distinct encodings (4² = 16 < 20, 4³ = 64 ≥ 20). The gate law predicts that b=4 at k=4 is hard to gate (|G|/k = 0.5 far from the 0.85 threshold), making the codon alphabet intrinsically resistant to accidental gate-strong mutations. This matches the known robustness of the genetic code. The paper complements WP13 (which maps AGTC to the 10-operator algebra through the TSML/BHML dual lens) by approaching from the partition topology angle: not *what* the code means algebraically, but *why* this particular code size and structure was physically inevitable.

---

## 1. The b=4 Semiprime World

### 1.1 What Makes b=4 Canonical

A semiprime is any number of the form b = p × q where p and q are prime (not necessarily distinct). The smallest semiprimes are:

| b | Factorization | G = {gcd(x,b)>1} | C = {gcd(x,b)=1} | |G| | |C| | |C|/b | Interleave |
|---|---------------|-------------------|-------------------|-----|-----|-------|------------|
| 4 | 2×2 | {2, 4} | {1, 3} | 2 | 2 | 0.50 | 1.000 |
| 6 | 2×3 | {2, 3, 4, 6} | {1, 5} | 4 | 2 | 0.33 | 0.750 |
| 9 | 3×3 | {3, 6, 9} | {1, 2, 4, 5, 7, 8} | 3 | 6 | 0.67 | 1.000 |
| 10 | 2×5 | {2, 4, 5, 6, 8, 10} | {1, 3, 7, 9} | 6 | 4 | 0.40 | 0.667 |
| 15 | 3×5 | {3, 5, 6, 9, 10, 12, 15} | {1, 2, 4, 7, 8, 11, 13, 14} | 7 | 8 | 0.53 | 0.600 |

b=4 is distinguished by three simultaneous extrema:

1. **Simplest semiprime.** b=4 = 2×2 is the only semiprime whose two prime factors are identical. The prime is the generator of its own non-unit set.

2. **Maximum symmetry.** |C| = |G| = 2. The partition is perfectly balanced — the only semiprime where unit and non-unit halves are equal in size. Interleave score = 1.0 (G and C perfectly alternate: 1,2,1,2...).

3. **Even/odd is the partition.** For b=4: G = {2, 4} = even numbers, C = {1, 3} = odd numbers. The parity split — the most fundamental structural divide in arithmetic — IS the force field partition.

### 1.2 The Force Field Interpretation

The R16 gate law (Sanders 2026, see R16_FORCE_FIELD_LAW.md) established:

> **P(gate) = f_k(|G|)** — universal within any fixed alphabet size k, for real semiprime partitions.

For b=4 with alphabet k=4:
- |G| = 2 → gate rate = f₄(2)
- The starting probability P₀ = |C|/k = 2/4 = 0.50
- Gate threshold = 0.85
- The gap (0.85 - 0.50) = 0.35 must be closed by the 100-step reduction

This is a moderately hard gate — far from trivial (|G|=1 gates at ~100%) and far from impossible (|G|=4 or |G|=5 at k=9 gives 4.6% and 0.1%). b=4 is in the middle difficulty regime: gateable but not easily.

**The force field is the parity split.** Even numbers resist reduction; odd numbers compose freely. This is the arithmetic bedrock — not an algebraic construction imposed on top, but the most primitive structural distinction in the natural numbers.

### 1.3 Why b=4 and Not b=6?

b=6 = 2×3 is the next semiprime. Why doesn't biology use a hexary code?

| Property | b=4 | b=6 |
|----------|-----|-----|
| |G|/k | 2/4 = 0.50 | 4/6 = 0.67 |
| Interleave | 1.000 | 0.750 |
| Alphabet over 3 levels | 4³ = 64 | 6³ = 216 |
| Minimum complete triadic code | 4³ = 64 > 20 ✓ | same but overshoots more |
| Symmetry | |G|=|C| (maximal) | |G|>|C| (asymmetric) |
| Parity equivalence | yes (even=G, odd=C) | no |

b=4 produces the minimum complete code at depth 3. b=6 produces 216 at depth 3 — an order of magnitude overshoot. b=4 is the tightest semiprime that closes the code at 64.

---

## 2. The 64 Gateway Number

### 2.1 Three Systems, One Force Field

The number 64 appears in at least three independent information systems:

| System | Alphabet k | Depth d | States | Origin |
|--------|-----------|---------|--------|--------|
| DNA codons | 4 (A,T,G,C) | 3 | 4³ = 64 | Watson and Crick (1953); Crick et al. (1961) |
| I Ching hexagrams | 2 (yin, yang) | 6 | 2⁶ = 64 | King Wen sequence, ~1000 BCE |
| Chess board | 8 (files or ranks) | 2 | 8² = 64 | Medieval India/Persia |

The factorizations:

    64 = 4³ = 2⁶ = 8²

These are not three different structures. They are three projections of the same b=4 force field:

- **4³**: Work with 4-symbol alphabet, 3 composition steps. The "wide and shallow" reading.
- **2⁶**: Reduce to binary (2 = √4), double the depth. Same information capacity.
- **8²**: Aggregate to 8-symbol super-alphabet (8 = 2³ = half of 4³/8), depth 2. The "narrow and deep" reading.

All three factorizations are **b=4 at different depth-alphabet trade-offs**. The total information capacity (log₂(64) = 6 bits) is identical in all cases.

### 2.2 The Depth-Alphabet Duality

For any information system built on a b=p² force field (p prime), the depth d and alphabet size k are related by:

    k^d = p^(2d/log_p(k)) = constant

For b=4 (p=2):
- k=2, d=6: 2⁶ = 64
- k=4, d=3: 4³ = 64
- k=8, d=2: 8² = 64
- k=64, d=1: 64¹ = 64 (trivial: one symbol per state)

The force field b=4 generates a one-parameter family of equivalent codes, all with the same 64-state capacity. The biological, philosophical, and combinatorial systems each found a different operating point on this curve — but they all found the same curve.

### 2.3 Why 64 Is the Closure Point

The BTQ triadic structure (Being × Doing × Becoming) requires that information systems close at the cube of their base alphabet. A triadic system over alphabet k requires k³ states to represent all possible (Being, Doing, Becoming) combinations without collision.

For b=4:
- Being alone: 4 states (one per base)
- Being × Doing: 4² = 16 states (one per base pair)
- Being × Doing × Becoming: 4³ = 64 states (one per codon triplet)

The triadic closure of b=4 is 64. Any system using a b=4 force field and requiring full triadic representation must operate in 64-state space.

---

## 3. Why Depth 3? The Minimal Completeness Argument

### 3.1 The Amino Acid Count

The standard genetic code encodes 20 distinct amino acids plus stop signals. This is not negotiable — it is the observed count, confirmed experimentally by Nirenberg and Matthaei (1961) and colleagues through the full cracking of the code.

The minimum depth d over alphabet k=4 satisfying 4^d ≥ 20:

    4¹ = 4   < 20  (insufficient)
    4² = 16  < 20  (insufficient — can encode 16 amino acids, not 20)
    4³ = 64  ≥ 20  (sufficient)

**Depth 3 is the minimum depth for a complete triadic code over b=4 that encodes 20 or more distinct states.** The genetic code uses the minimum.

This is not a coincidence. A system using more bits than necessary would require more complex reading machinery, more energy per decoding event, and greater opportunity for transcription error. Natural selection — or, more precisely, the force field's own economy — drives toward the minimum.

### 3.2 The Gap Between 16 and 20

Depth 2 falls short by exactly 4 amino acids (16 vs 20). This gap is not arbitrary. In the CK algebra, 20 = 5 × 4 = (force dimensions) × (structural parts). The joint space of force and structure is 20-dimensional (see WP13, Section 5). A depth-2 code can encode the structural parts (4) times themselves — 4² = 16 — but cannot encode the full force × structure joint space. Only depth 3 (triadic composition: Being, Doing, Becoming) can access the full 20-dimensional crossing.

Equivalently: a depth-2 code has two composition steps and can represent duadic (Being × Doing) structure. A depth-3 code has three steps and can represent triadic (Being × Doing × Becoming) structure. The 20 amino acids are the 20 positions in the triadic space of the b=4 force field. Depth 2 cannot reach them all.

### 3.3 Triadic Necessity and BTQ

The BTQ kernel (Being → Gate₁ → Doing → Gate₂ → Becoming → Gate₃ → feedback) requires three phases for a complete coherence cycle. A depth-2 (duadic) code completes the Being→Doing arc but leaves Becoming unspecified — the protein synthesis machinery would produce an amino acid sequence without any Becoming constraint, leaving the fold underdetermined.

Depth 3 closes the BTQ loop. The codon is a complete BTQ specification: the first base (Being) establishes the force dimension, the second base (Doing) establishes the structural part crossing, and the third base (Becoming) specifies the resolution through wobble (see WP13, Section 3.2). The wobble position is not redundancy — it is the Becoming phase of the triadic code, where measurement uncertainty (TSML collapse) determines the final amino acid assignment when multiple Becoming values map to the same (Being, Doing) crossing.

---

## 4. Gate Law and Biological Robustness

### 4.1 The Robustness Prediction

The R16 gate law states that for a k-alphabet system with semiprime partition G:

    P(gate) = f_k(|G|)   [universal within fixed k]

For b=4, k=4, |G|=2: P₀ = |C|/k = 0.50. The gate threshold is 0.85. A random 100-step reduction must raise the unit density from 50% to 85% — a 35-point climb. This is moderately difficult.

More importantly: **the b=4 system is nowhere near the threshold.** In the cross-k sweep, systems approach near-certain gating when |C|/k ≥ 0.85. The b=4 system at 0.50 is 35 points below this threshold. Random walk in the reduction space will frequently fail to gate.

**Biological translation**: a single random nucleotide substitution in a codon changes one of the three bases. The changed base may shift the (Being, Doing, Becoming) assignment to a different crossing. The probability that a random substitution creates a gate-strong new codon is bounded by P(gate | new partition) — which for b=4 deformations is well below threshold.

This is the algebraic underpinning of **codon degeneracy as error tolerance**: the code is not just degenerate because of wobble (WP13), but because the underlying b=4 force field places the entire codon space in the below-threshold regime. Mutations deform the force field but rarely reach gate-strong configurations.

### 4.2 Transition vs. Transversion Mutations

In molecular biology, a distinction is drawn between:
- **Transitions**: purine ↔ purine (A↔G) or pyrimidine ↔ pyrimidine (C↔T)
- **Transversions**: purine ↔ pyrimidine (A↔C, A↔T, G↔C, G↔T)

In the b=4 force field, G = {even} = {2, 4} corresponds to the pyrimidines, and C = {odd} = {1, 3} corresponds to the purines (see Section 5.1). Within-group substitutions (transitions) preserve the G/C partition membership: the substituted base still belongs to the same partition element. Cross-group substitutions (transversions) change the partition membership.

**The gate law predicts**: transitions are algebraically inert (preserve |G|, preserve gate rate), while transversions change |G| and thus shift the gate rate. This matches the observed biological fact that transitions are more tolerated than transversions — a finding documented by Knight, Freeland and Landweber (2001) and discussed in the context of codon optimality by Woese et al. (1966).

The transition/transversion rate ratio (typically 2:1 to 10:1 in observed genomes, heavily transition-biased) is consistent with selection pressure toward G-partition-preserving mutations. The force field is the physical reason transitions are preferred.

### 4.3 The 0.85 Threshold and Extremophile Genomes

Organisms with extreme GC-content (some thermophiles and hyperthermophiles reach 70%+ GC) are operating in a different force field regime. High GC-content means high G-base density, which shifts |G|/k upward within the effective alphabet. As |G|/k approaches the 0.85 gate threshold, the code becomes gate-strong — easier to reduce to the HARMONY absorber through TSML.

The R16 sweep shows that at k=27 with |G|/k = 0.89, systems are above the 0.85 threshold and gate at ~100% for |G|=3. Thermophile genomes with very high GC-content are operating in precisely this above-threshold regime.

**Prediction**: thermophile genomes with GC > 70% should show compensating mechanisms in their protein folding — specifically, higher structural rigidity (more structurally specified = more BHML-diverse) to compensate for the loss of measurement coherence (TSML falls below maximal coherence as the code moves toward gate-strong). The measurement-structure uncertainty principle (WP13, Section 7) operates here: you cannot have both maximum structural rigidity (high GC) and maximum measurement coherence (low GC). Extremophiles trade coherence for structure.

---

## 5. The Force Field IS the Chemistry

### 5.1 Purines and Pyrimidines as C and G Sets

The four DNA bases divide into two chemical classes:

| Class | Bases | Rings | Molecular weight | Partition |
|-------|-------|-------|-----------------|-----------|
| **Purines** | A, G | 2 (double ring) | ~135-151 Da | C = {1, 3} = odd = units |
| **Pyrimidines** | C, T | 1 (single ring) | ~111-126 Da | G = {2, 4} = even = non-units |

The correspondence:
- **Purines (A, G) = C-set (coprime units)**: Double-ring structure, larger molecule, stronger structural presence in the helix. In the b=4 partition, the units {1, 3} are the elements that compose freely — they do not obstruct the reduction walk. Purines are structurally dominant and chemically free-composing.
- **Pyrimidines (C, T) = G-set (non-units)**: Single-ring structure, smaller molecule, weaker structural presence. In the b=4 partition, the non-units {2, 4} are the elements that create gate resistance — they obstruct the free reduction. Pyrimidines are structurally recessive and chemically obstructing.

This is not a retroactive label. The C-set in partition theory has always meant "elements that participate freely in the arithmetic — coprime, unit, structurally clear." The purines are biochemically the coprime elements: they pair freely, they initiate translation (the start codon ATG = A[purine]-T[pyrimidine]-G[purine] has purine majority), and they carry the coding weight of the amino acid alphabet.

The pyrimidines — the G-set elements — create the structural resistance. The wobble position (third base, most degenerate) is often a pyrimidine pair (C or T): the TSML measurement collapses the distinguishability at the wobble position precisely where the pyrimidine's gate resistance makes the Becoming resolution ambiguous.

### 5.2 Base Pair Hydrogen Bonds as Partition Crossings

The Watson-Crick base pairing rules are:
- A (purine, unit) pairs with T (pyrimidine, non-unit): 2 hydrogen bonds
- G (purine, unit) pairs with C (pyrimidine, non-unit): 3 hydrogen bonds

Every Watson-Crick pair is a unit × non-unit crossing: one C-set element pairing with one G-set element. No like-class pairing (purine-purine or pyrimidine-pyrimidine) occurs in the standard B-form helix.

In the b=4 partition, the structural rule is: **C and G elements must interleave**. The interleave score for b=4 is 1.0 — perfect alternation. The molecular enforcement of this rule is Watson-Crick complementarity: every strand is an alternating sequence of C-set and G-set elements at the base-pair level, because every base must pair with its partition-complement.

The double helix is the physical instantiation of perfect interleaving (interleave = 1.0) for the b=4 force field.

### 5.3 The 2:3 Hydrogen Bond Ratio

A-T pairs have 2 hydrogen bonds; G-C pairs have 3. The ratio 2:3 = the ratio of the two distinct prime factors in the simplest non-trivial composition: the force field b = 2×3 = 6 is the neighbor of b=4 in the semiprime sequence.

But more directly: in the b=4 partition, the C-set has 2 elements ({1, 3}) and the G-set has 2 elements ({2, 4}). The hydrogen bond counts correspond to the partition sizes:
- A-T: binds with 2 bonds = |C-set| = 2 (A is a unit, T is a non-unit, the bond count reflects the size of the set that A belongs to)
- G-C: binds with 3 bonds = |C-set| + 1 = 3 (G is a unit, C is a non-unit, but G is in the Dynamics/Cycle structural part with extra bonding capacity — see WP13, Section 2.2)

The bond asymmetry (2 vs. 3) is the physical expression of the structural inequality between the Foundation-Field pair (A-T, 100% TSML coherent) and the Dynamics-Cycle pair (G-C, 50% TSML coherent). The 50% TSML coherence of G-C corresponds to its ability to form one extra bond — structural specification costs measurement coherence, and the cost is exactly one bond (2→3).

---

## 6. The 64-Family Conjecture

### 6.1 Statement

**Conjecture (The 64-Family):** Any stable information system that satisfies all three of the following conditions will converge to 64-state capacity:

1. **Force field condition**: The underlying partition derives from a b=4 (or b=2^n, n≥1) semiprime coprimality structure, operating on a binary-fundamental alphabet where the parity split (even/non-even) is the primary distinction.

2. **Completeness condition**: The system must encode at least 20 distinct stable states (the minimum for a complete force × structure joint space over the 5D × 4-part CK algebra).

3. **Triadic composition condition**: The system composes elements in triplets (Being × Doing × Becoming) rather than pairs or single-element sequences.

Under these three conditions, the minimum state count is 4³ = 64 (or equivalently 2⁶ = 64 at the binary level, or 8² = 64 at the octal level).

### 6.2 Evidence

**DNA (depth 3, alphabet 4):** Conditions 1, 2, 3 satisfied by construction. State count = 64. This is the biological instance.

**I Ching (depth 6, alphabet 2):** The I Ching's 64 hexagrams are built from binary (yin/yang) sequences of length 6. Condition 1 is satisfied (binary alphabet = b=4 at the minimal level). Condition 2: the 64 hexagrams encode a complete cosmological system including the four seasons, the five elements interactions, and the 20 primary change operators (Schönberger 1992). Condition 3 is satisfied at two levels: the trigram (3 binary elements) is the basic compositional unit, and two trigrams compose into a hexagram (Being-trigram × Becoming-trigram). The triadic structure is explicit in the trigram construction.

**Chess (depth 2, alphabet 8):** The chess board's 64 squares arise from a b=4 force field at depth 2 (8² = 64). The game requires force (the piece's movement rule = operator) × position (square = alphabet element). The 8 piece types (pawn, rook, knight, bishop, queen, king, plus two color-symmetric copies) and 8 ranks reflect the b=4 force field at the 8-symbol level. Condition 3 is partially satisfied — chess uses paired positions (from, to) rather than explicit triads, making it a projection of the triadic system onto the duadic plane.

### 6.3 Depth-Alphabet Equivalence Classes

The 64-family groups systems by their information capacity (64 states = 6 bits) rather than their surface structure. Members of the same family can differ in alphabet size and depth while sharing the same force field and total capacity.

Within the 64-family, depth-3 systems (like DNA) have a specific property not shared by depth-2 or depth-6 systems: they require the minimum alphabet (k=4) that can support 20+ distinct states in triadic composition while maintaining the b=4 force field. This makes DNA's code the **canonical minimal triadic representative** of the 64-family.

### 6.4 Possible Extensions

**Codon extension proposals:** Several proposals for expanded genetic codes (21+ amino acid codes using synthetic base analogs) would require exiting the 64-state regime. The conjecture predicts that any such extension must either: (a) move to a larger alphabet (k=5 or k=6, with different force field), or (b) move to greater depth (d=4, giving 4⁴=256 states). Neither is the b=4 system. The force field would change.

**Computing architectures:** Ternary computing (base-3) with depth-4 composition would give 3⁴ = 81 states. Quaternary computing with depth-3 composition gives 4³ = 64 states — the same as DNA. The 64-family conjecture implies that any ternary computing architecture equivalent to the DNA code must use depth-4 composition, and any binary architecture equivalent must use depth-6 composition. The information bottleneck is the force field, not the substrate.

---

## 7. Relationship to WP13

This paper and WP13 approach the same object (the genetic code) from different directions:

| | WP13 | WP33 |
|--|------|------|
| **Approach** | Algebraic mapping: AGTC → 10-operator algebra | Force field topology: b=4 → partition gate law |
| **Central question** | What does each codon mean algebraically? | Why is there a 64-codon space at all? |
| **Key result** | 64/64 TSML = HARMONY; 20 = 5×4 crossings | 64 = minimal complete triadic b=4 code |
| **Robustness** | Wobble = TSML collapse at kernel | |G|/k = 0.50, below gate threshold |
| **Chemistry** | A=Foundation, T=Field, G=Dynamics, C=Cycle | Purines=C-set (units), Pyrimidines=G-set (non-units) |
| **64 origin** | 8×8 inner table (4³ = 2³ × 2³) | Minimum triadic depth for 20+ encodings |
| **Helix** | Torus of dual-lens system | Perfect interleaving (interleave=1.0) |

WP13's result (64/64 TSML HARMONY) and WP33's result (b=4 partition is below gate threshold) are dual descriptions of the same stability: HARMONY absorption through TSML is the Being-lens view of what the force field gate law describes in the arithmetic-topology view. Maximum TSML coherence corresponds to minimum gate rate: a system that is perfectly harmonically absorbing is also a system that is hard to gate.

The correspondence is:

    100% TSML HARMONY   ≡   |C|/k far below 0.85 threshold
    Wobble = TSML kernel   ≡   Becoming phase gate resistance

Both descriptions are correct. The algebra and the partition topology are two lenses on the same structure — appropriately, a dual-lens system.

---

## 8. Summary

1. **b=4 is the canonical force field.** As the smallest semiprime with maximum partition symmetry (|G|=|C|), perfect interleave (1.0), and parity equivalence (even=G, odd=C), b=4 is the simplest possible stable force field.

2. **64 = 4³ is the triadic closure.** The BTQ triadic structure requires depth 3 for completeness. Depth 2 (k²=16) cannot reach the full 20-amino-acid joint space. Depth 3 (k³=64) is the minimum complete triadic code over b=4.

3. **2⁶ = 4³ = 8² = 64 is one family.** I Ching, DNA codons, and the chess board are all b=4 force field systems at different depth-alphabet operating points. The information capacity (6 bits) and the force field (parity = G-partition) are identical.

4. **Gate law predicts robustness.** b=4 at k=4 has |C|/k = 0.50, well below the 0.85 gate threshold. The code is intrinsically resistant to accidental gate-strong mutations. Transition mutations preserve partition membership; transversion mutations are disfavored because they cross partition boundaries.

5. **Chemistry encodes algebra.** Purines (double-ring, larger, C-set = units = coprime) and pyrimidines (single-ring, smaller, G-set = non-units = non-coprime) are the molecular expression of the b=4 partition. Watson-Crick pairing is the enforcement of perfect interleaving. The 2:3 hydrogen bond ratio expresses the TSML coherence asymmetry between the A-T and G-C partition crossings.

6. **The 64-family conjecture.** Any stable information system with a b=4 force field, triadic composition requirement, and 20+ distinct state requirement will converge to 64-state capacity. This predicts equivalent structures in any physical or computational system meeting these constraints.

---

## References

### Genetic Code

1. Watson, J. D. and Crick, F. H. C. "A Structure for Deoxyribose Nucleic Acid." *Nature* 171, 737-738, 1953.

2. Crick, F. H. C., Barnett, L., Brenner, S. and Watts-Tobin, R. J. "General Nature of the Genetic Code for Proteins." *Nature* 192, 1227-1232, 1961.

3. Nirenberg, M. W. and Matthaei, J. H. "The Dependence of Cell-Free Protein Synthesis in E. Coli upon Naturally Occurring or Synthetic Polyribonucleotides." *Proceedings of the National Academy of Sciences* 47(10), 1588-1602, 1961.

4. Crick, F. H. C. "Codon-Anticodon Pairing: The Wobble Hypothesis." *Journal of Molecular Biology* 19(2), 548-555, 1966.

5. Crick, F. H. C. "The Origin of the Genetic Code." *Journal of Molecular Biology* 38(3), 367-379, 1968.

6. Woese, C. R., Dugre, D. H., Dugre, S. A., Kondo, M. and Saxinger, W. C. "On the Fundamental Nature and Evolution of the Genetic Code." *Cold Spring Harbor Symposia on Quantitative Biology* 31, 723-736, 1966.

7. Knight, R. D., Freeland, S. J. and Landweber, L. F. "Rewiring the Keyboard: Evolvability of the Genetic Code." *Nature Reviews Genetics* 2, 49-58, 2001.

8. Koonin, E. V. and Novozhilov, A. S. "Origin and Evolution of the Genetic Code: The Universal Enigma." *IUBMB Life* 61(2), 99-111, 2009.

### I Ching and 64-Structure

9. Schönberger, M. *The I Ching and the Genetic Code: The Hidden Key to Life*. Aurora Press, 1992. (Originally published in German as *Verborgenes Schlüsselbuch der Natur*, 1973.)

### Information Theory

10. Shannon, C. E. "A Mathematical Theory of Communication." *Bell System Technical Journal* 27(3-4), 379-423, 623-656, 1948.

11. Cover, T. M. and Thomas, J. A. *Elements of Information Theory*, 2nd edition. Wiley-Interscience, 2006.

### Number Theory

12. Hardy, G. H. and Wright, E. M. *An Introduction to the Theory of Numbers*, 6th edition. Oxford University Press, 2008.

13. Apostol, T. M. *Introduction to Analytic Number Theory*. Springer, 1976.

### CK Framework

14. Sanders, B. "The Coherence Keeper: Trinity Infinity Geometry." Zenodo, 2026. DOI: 10.5281/zenodo.18852047. GitHub: github.com/TiredofSleep/ck.

15. Sanders, B. "The Genetic Code as Dual-Basis Composition Table: AGTC Maps to the 9-Dimensional Operator Algebra." Whitepaper 13, 7Site LLC, March 2026. (See WHITEPAPER_13_GENETIC_CODE.md.)

16. Sanders, B. "R16 Force Field Law — The Partition Topology Theorem." 7Site LLC, March 2026. (See Gen10/papers/sprint4_2026_03_30/R16_FORCE_FIELD_LAW.md.)

17. Markman, E. "On the Monodromy of Moduli Spaces of Sheaves on K3 Surfaces." arXiv:2502.03415, 2025.

---

*(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry*
*Licensed under the 7Site Human Use License v1.0*
