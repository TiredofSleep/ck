# Natural Carrier Criterion
## What Counts as a Natural Carrier for TSML/BHML?

---

## Purpose

Before running the instrument on any system, verify that the system lives on a natural carrier. If it does not, the instrument should not be applied — or, if applied, the result should be interpreted as a test of the encoding, not of the system.

This criterion is frozen going forward. It is not relaxed to accommodate specific test targets.

---

## The Criterion

A system $X$ is a **natural carrier** for TSML/BHML testing if all of the following hold:

### Requirement N1: Finite state space of appropriate size

The system's symbolic state space, after any agreed-upon symbolic encoding, has exactly 10 elements (for Z/10Z) or $n$ elements where $n$ is in the 35-member compatibility family.

Failure mode: states are continuous and have no natural discretization into the target cardinality.

### Requirement N2: Modular or residue structure

The symbolic state space carries an additive or multiplicative structure compatible with $\mathbb{Z}/n\mathbb{Z}$. Specifically, at least one of:
- Addition mod $n$ makes structural sense (e.g., phase counters, congruential counters, cyclic indices).
- Multiplication mod $n$ makes structural sense.
- The state space is naturally indexed by elements of a finite commutative ring.

Failure mode: the states are labeled by integers only nominally, with no meaningful arithmetic structure.

### Requirement N3: Natural shell partition

A partition of the units $U(n)$ into shells exists, either:
- Directly given by the system (e.g., eigenvalue multiplicities, orbit structure).
- Derived from a principled 2-adic or $p$-adic valuation on the state labels.
- Preserved under the system's dynamics in a statistically detectable way.

Failure mode: the shell partition must be imposed arbitrarily because the system has no analog.

### Requirement N4: Distinguished attractor

The system has a **distinguished** element (not just a modal output) that plays the role of attractor. This means:
- The element is identifiable by structural argument, not statistics.
- The element absorbs most transitions under some interpretable rule.

Failure mode: the modal output is determined by encoding artifacts (e.g., a lumped class) rather than by system dynamics.

### Requirement N5: Commutative or symmetrizable kernel

The empirical operator $E$ (or its symmetrized version $E^{\text{sym}}(x,y) = \text{mode}\{z : (x,y) \text{ or } (y,x) \text{ observed}\}$) is commutative, at least approximately. Specifically:
- For pairs where both $(x,y)$ and $(y,x)$ are observed, at least 80% agree.

Failure mode: the operator is structurally non-commutative (like Rule 110's directional update).

### Requirement N6: Small seam

The seam — the set of $(x,y)$ pairs where the canonical construction disagrees with $E$ — is small relative to the carrier:
- $|S| / |\text{support}(E)| \leq 0.15$ in well-behaved cases.

Failure mode: seam is large, dense, contains cycles on too many vertices. This indicates the system's structure is not captured by a collapse-plus-exceptions decomposition.

### Requirement N7: Transport companion exists (optional for T-only testing; required for pair testing)

If paired (T, B) testing is intended, the system must support both a collapse operator and a transport operator on the same carrier. Transport must be commutative and have non-zero integer determinant.

Failure mode: only one kind of dynamic is present in the system (all-collapse or all-transport), making pair testing meaningless.

---

## Pre-Test Checklist

Before committing to any test of TSML/BHML on a candidate system:

- [ ] N1: state space is size 10 (or a compatibility family size).
- [ ] N2: modular or residue structure is natural, not imposed.
- [ ] N3: shell partition is motivated by system structure or by a principled valuation.
- [ ] N4: an attractor is identified by structural argument.
- [ ] N5: kernel commutativity pre-check passes (or symmetrization is justified).
- [ ] N6: preliminary analysis suggests small seam.
- [ ] N7: if pair testing is intended, both operators are identifiable.

If any of N1–N6 fail for a T-only test, do not run the full instrument on that system. Diagnose and report.

If N7 fails, do not claim pair testing. T-only or B-only may still be meaningful individually.

---

## Examples

### Passes the criterion

- **Residue arithmetic controllers** (N1–N6 satisfied by construction).
- **Synthetic benchmarks B1, B2, B3** (N1–N7 satisfied by design).
- **Error-correcting codes over $\mathbb{Z}/10$** (N1, N2, partial N3-N6).
- **Finite-state systems with cyclic structure** (N1, N2, N5 often).

### Fails the criterion

- **Rule 110 with 4-cell window encoding** (fails N5: non-commutative; fails N3: no natural shell partition).
- **Logistic map with decile binning** (fails N2: no natural modular structure on orbit values; fails N4: attractors are invariant measures, not ring elements).
- **Ising lattice with energy-level encoding** (fails N2 and N3 unless a modular interpretation is motivated).
- **Arbitrary time series with quantile binning** (fails N2, N3 in general).

### Borderline

- **Phase oscillators binned by phase-modulo-$n$** (N1, N2 pass; N3–N6 depend on system details).
- **Cellular automata with rule numbers in a specific modular class** (N1, N2 pass; others require case analysis).

---

## What Changes With This Criterion

### What the criterion forbids

- Running the instrument on systems where requirements are not met and interpreting the result as evidence about TSML/BHML.
- Reporting match rates without reporting criterion compliance.
- Tuning $\Phi$ to force criterion compliance after seeing data.

### What the criterion permits

- Running the instrument on candidate systems and reporting partial compliance; this can still be informative.
- Using the instrument on systems that clearly meet the criterion, with high confidence that a pass/fail result speaks to the system.
- Designing experiments (like the shell-native benchmarks) explicitly to meet the criterion.

---

## Falsifier for the Criterion Itself

If a future experiment discovers a system that **fails N1–N6** but the instrument nonetheless **reveals meaningful, reproducible structure** not detectable by standard methods, then the criterion has been too restrictive.

In that case: relax the criterion with care, document precisely which requirement was dropped and why, and re-spec the instrument's scope.

Until that happens: the criterion is the frozen gate between the instrument and the data.

---

## Discipline Statement

The point of the criterion is not to prevent testing. It is to prevent category confusion between instrument failure and scope mismatch. A failure in-category is diagnostic of the instrument. A failure out-of-category is a tautology.

**The criterion is the instrument's self-check before it is applied to anything.**
