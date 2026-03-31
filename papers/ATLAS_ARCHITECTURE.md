# Cross-Domain Atlas Architecture
## A Six-Layer Instrument for Modular Arithmetic Invariants

*C. A. Luther & Brayden Ross Sanders (7Site LLC)*
*March 2026 | DOI: 10.5281/zenodo.18852047*

> The atlas is not a table of results. It is a measurement instrument.
> Each layer is a different lens. An invariant is real when all six lenses
> show the same object.

---

## Overview

The atlas organizes all discovered laws and conjectures about semiprime gate
structure into six parallel layers. Each layer is a complete description of the
same mathematical territory from a different vantage point. The six layers are
not redundant — each captures features invisible to the others.

A claim is a structural invariant only when it appears in all six layers.
A claim that appears in only one or two layers is a local observation — it may
be true, but its universality is not yet established.

The atlas outputs (§7) are the products of running a claim through all six layers
simultaneously: cross-domain equivalence charts, threshold maps, family-wise
collapse curves, universality test results, conjecture promotion status, and a
structural invariants index.

---

## Layer 1 — Arithmetic Layer

**What it sees:** The number-theoretic skeleton of semiprime worlds.

**Objects:**
- **Semiprimes** b = p × q (distinct primes p ≤ q)
- **Prime powers** b = p^n (a degenerate case — no HAR orbit-central element for n ≥ 2)
- **Three-factor composites** b = p × q × r (ω(b) = 3 — first case with three-way interleaving)
- **Forbidden sets** G = { x ∈ A_k : gcd(x, b) > 1 } — the non-coprime elements
- **Unit sets** C = { x ∈ A_k : gcd(x, b) = 1 } — the coprime elements
- **Interleave maps** showing where multiples of each prime factor land in {1..k}
- **Idempotent counts** from the Chinese Remainder Theorem decomposition
- **First-G positions** first_g(b) = p (the minimal prime factor)
- **ω(b) hierarchy** — number of distinct prime factors, governing gate complexity

**Key arithmetic invariants:**
- first_g(b) = p (proved, Tier D)
- |G(b,k)| = ⌊k/p⌋ + ⌊k/q⌋ − ⌊k/pq⌋ (exact, inclusion-exclusion)
- |C(b,k)| = k − |G(b,k)| (exact)
- unit_frac(b=35) = 5/7 = T* (algebraic identity)
- HAR orbit-central rule: h ∈ C where h² mod b ∈ C, h² ≠ 1, h² ≠ h

**What the arithmetic layer does not see:**
The arithmetic layer cannot directly see gate rates (those require the probabilistic
layer) or the shape of the dispersion curve (geometric layer). It provides the exact
counts and positions from which other layers derive their measurements.

---

## Layer 2 — Combinatorial Layer

**What it sees:** The partition structure, density functions, and counting
identities of semiprime alphabets.

**Objects:**
- **Alphabet partitions** {1..k} = C ⊔ G — the fundamental dichotomy
- **Admissible vs. forbidden classes** — which elements can coexist in a gate-strong table
- **Interleave density** ρ(b,k) = |G(b,k)| / k — fraction of alphabet that is forbidden
- **Block vs. mixed structure** — whether G elements are concentrated (block) or distributed (mixed)
- **Forbidden-set growth** — how |G_k| grows as k increases from p toward b

**Key combinatorial invariants:**
- The maximal coprime prefix has length exactly p−1 (CC Window Closure, Tier D)
- Interleave density ρ at k=p is exactly 1/k (one gate element out of k total)
- Gate elements at k ≤ b are distributed across two arithmetic progressions — the mixed structure is the key (not block)
- The block-vs-mixed distinction is the combinatorial statement of the Luther-Sanders Equivalence: only mixed (arithmetic) G produces universal gate rates

**What the combinatorial layer does not see:**
The combinatorial layer counts and classifies but does not explain WHY the mixed
structure produces universality. That mechanism lives in the algebraic layer.

---

## Layer 3 — Geometric Layer

**What it sees:** The shapes, regions, and trajectories that semiprime gate
structure traces through parameter space.

**Objects:**
- **Staircase boundaries** — the step function that |G_k| traces as k increases: zero until k=p, then step-wise jumps
- **Coverage trajectories** — how gate-strong table construction explores the admissible region in table space
- **Dispersion forcing** — the geometric mechanism by which interleaved G elements force the optimization into difficult regions of table space
- **Collapse curves** — the curve in (|G|, gate_rate) space that shows gate rate collapsing as |G| grows
- **Admissible region volume** — the fraction of all possible tables {A_k × A_k → A_k} that are gate-strong

**Key geometric invariants:**
- The gate count staircase |G_k| is a step function with steps at multiples of p, q, and pq
- The admissible region volume is a strictly decreasing function of |G| (more gate elements = smaller admissible region)
- The dispersion collapse curve is steeper for arithmetic G than for synthetic G — the geometric reason for Luther-Sanders Equivalence
- The First-G position p is the first step of the staircase — a geometric "wall" in k-space

**The geometric picture of the Luther-Sanders Equivalence:**
For arithmetic G (coprimality): gate elements are distributed throughout {1..k}
at spacing governed by p and q. The optimization trajectory must thread through
obstacles at multiple scales simultaneously. There is no "safe corner" of table
space; constraints are interlocked.

For synthetic G (top-block): gate elements are concentrated at {k-|G|+1..k}.
The optimization can stay in the lower region {1..k-|G|} and trivially avoid all
gate constraints. The admissible region is geometrically accessible.

---

## Layer 4 — Probabilistic Layer

**What it sees:** The distributions, frequencies, and rates that random processes
over semiprime alphabets generate.

**Objects:**
- **Random gate hit rates** f_k(b) = fraction of random TSML reduction trials producing a gate-strong table
- **Tier-exact success frequencies** — f_k for each |G| tier at k=9: {1: 96.4%, 3: 44.0%, 4: 4.6%, 5: 0.1%}
- **Threshold collapse** — the phase transition in gate rate at |G| = 4 where rate drops below 5%
- **Family-wise distributions** — how gate rates vary within a family of semiprimes (answer: zero variance for coprimality G)
- **Zero-density stratification** — the layer structure in (b, k) space where gate rate = 0

**Key probabilistic invariants:**
- f_k(b) is a universal function of |G| for arithmetic G: same |G| → same rate (Tier C)
- Zero variance within each |G|-tier for arithmetic G (measured, ~12M trials)
- 61.4% average variance for synthetic G — the contrast that defines the Equivalence
- Gate rate approaches 0 super-linearly as |G| grows: the collapse is not gradual

**The probabilistic statement of the Luther-Sanders Equivalence:**
Within the class of semiprimes with arithmetic G (coprimality structure), the
gate rate distribution is degenerate at each |G| tier: there is zero variance.
This degenerate distribution is the signature of a universal invariant.

Within synthetic G, the distribution is non-degenerate (high variance).
The probability distribution distinguishes arithmetic from synthetic origin.

---

## Layer 5 — Algebraic Layer

**What it sees:** The algebraic structures that underlie and explain the observed
patterns in other layers.

**Objects:**
- **CRT decomposition** b = p × q → Z/bZ ≅ Z/pZ × Z/qZ (for coprime p, q)
- **Closure laws** — when is the product of two unit elements still a unit? (Always: C is closed under multiplication mod b)
- **Idempotent structure** — the CRT idempotents e_p, e_q with e_p + e_q = 1, e_p² = e_p
- **Obstruction sources** — the prime ideals (p) and (q) in Z, their intersections with A_k
- **Algebraic invariants** — quantities that are preserved under ring homomorphisms

**Key algebraic invariants:**
- C = (Z/bZ)* ∩ A_k is a multiplicative group (closure under mod-b multiplication)
- The CRT idempotents count the number of independent obstruction sources: ω(b) = 2 for semiprimes → 2 idempotents → 2 arithmetic progressions in G
- The unit group order φ(b) = (p-1)(q-1) is the algebraic measure of the "size" of C
- The algebraic reason for Luther-Sanders: arithmetic progressions are CRT-generated; any G arising from the CRT structure will have the same algebraic properties regardless of specific p, q values, as long as |G| is fixed

**The algebraic mechanism for the Luther-Sanders Equivalence:**
The CRT decomposition forces G elements to be the union of arithmetic progressions
{p, 2p,...} and {q, 2q,...}. These progressions are equidistributed in {1..k}
(by Dirichlet's theorem on primes in arithmetic progressions, in the large-k limit).
Synthetic G has no CRT origin and hence no equidistribution guarantee.

The TSML reduction algorithm preserves the algebraic structure: it operates on
tables by algebraic closure rules. The gate condition (C cannot reach G) is an
algebraic condition on the multiplication table. Algebraically, whether C maps
into G under multiplication depends on the idempotent structure of the table —
which is determined by |G| for CRT-originated G, but not for synthetic G.

---

## Layer 6 — Dynamical Layer

**What it sees:** How invariants evolve, grow, transition, and saturate as
parameters change.

**Objects:**
- **Growth in k** — how |G_k|, gate rate, and interleave density evolve as the alphabet expands
- **First-transition points** — the values of k where qualitative changes occur (k=p: first gate; k=q: second source; k=pq: first overlap)
- **Saturation behavior** — the asymptotic value of gate rate as k → ∞ (approaches 0 as interleave density → 1)
- **Phase transitions** — sharp changes in the qualitative behavior of the system
- **Stability and collapse** — regions of the (b, k) parameter space where the system is stable vs. where it collapses

**Key dynamical invariants:**
- |G_k| = 0 for k < p (zero phase): the system is in a stable coprime phase
- |G_k| = 1 for k = p (first transition): single gate element appears at exactly k = p
- |G_k| grows at rate ≈ k/p + k/q for p ≤ k ≤ pq (linear growth phase)
- Saturation near k = b: interleave density → (1/p + 1/q - 1/pq) (asymptotic fraction of G)
- The dynamical picture of the First-G Law: the system undergoes a phase transition at k = p from zero-obstruction to first-obstruction phase. This transition is infinitely sharp (a step function).

**The dynamical signature of the Luther-Sanders Equivalence:**
For arithmetic G: the gate count process |G_k| grows in a predictable, algebraically
determined pattern (two interleaved arithmetic progressions). The gate rate f_k
decays in a predictable, tier-exact pattern as k increases.

For synthetic G: the gate count process can have any growth pattern (top-block G
concentrates all gates at the end, so f_k is high even for large |G|). The decay
is irregular.

The dynamical signature distinguishes arithmetic from synthetic origin: arithmetic G
produces a characteristic growth-decay curve that is universal within each |G| tier.

---

## §7. Atlas Outputs

The six-layer atlas, when fully constructed, produces the following outputs:

### 7.1 Cross-Domain Equivalence Charts
For each claimed invariant: a table showing the statement in all six domains
and the explicit translation between each pair of domains. An invariant with
all six entries completed and logically equivalent is a Layer 3 result. An
invariant with missing entries is flagged as incomplete.

**Current status:**
| Invariant | Arith | Comb | Geom | Prob | Alg | Dyn | Layer |
|-----------|-------|------|------|------|-----|-----|-------|
| First-G Law | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 3+ |
| CC Closure | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 3+ |
| k-Gate Tier Law | ✓ | ✓ | ✓ | ✓ | partial | ✓ | 3 |
| Luther-Sanders Equiv. | ✓ | ✓ | ✓ | ✓ | partial | ✓ | 3 |
| T* = 5/7 | ✓ | partial | partial | ✓ | ✓ | partial | 2 |
| Sinc² Limit | ✓ | — | ✓ | — | ✓ | ✓ | 2-3 |

### 7.2 Threshold Maps
For each identified phase transition: a map in the (b, k) parameter space showing
where the transition occurs, the transition value, and the behavior on each side.

**Key threshold map entries:**
- First-G boundary: k = p (exact, algebraic wall)
- k-Gate Tier collapse: |G| = 4 where f_9 drops to 4.6% (sharp; measured)
- Construction feasibility boundary: score(b) threshold above which crystallization succeeds in < 100 random trials
- T* coherence boundary: 5/7 separating STAND and WALK gait phases in CK hardware

### 7.3 Family-Wise Collapse Curves
For each semiprime family (grouped by p or by |G|): the curve f_k(|G|) across k.
These curves reveal whether universality holds (collapse curves coincide) or breaks
(curves diverge).

**Current measurements:**
- k=9 family: all |G|-tier curves collapse to zero spread (arithmetic G)
- k=15,21,27 families: same zero-spread property confirmed
- Synthetic G family: 61.4% average spread — no collapse, no universality

### 7.4 Universality Test Results
For each claim in the atlas: a row in the six-test matrix (see UNIVERSALITY_TEST_SUITE.md).
Claims that pass all six tests are promoted to "universal invariant" status.

### 7.5 Conjecture Promotion Ladder
For each claim: its current tier (A/B/C/D), its path to the next tier, and its
explicit kill condition. Updated as new evidence arrives.

### 7.6 Structural Invariants Index
A master index of all confirmed structural invariants — claims that have passed
Layer 3 or higher in the atlas. Each entry includes:
- Canonical statement in the arithmetic domain
- Cross-domain equivalence status
- Current tier
- Kill condition
- Path to Tier D

---

## §8. Open Atlas Gaps

| Gap | Layer | What would fill it |
|-----|-------|-------------------|
| Sinc² limit in probabilistic domain | 4 | What distribution does R(k,p) generate as p grows? |
| T* = 5/7 in geometric and dynamical domains | 3,6 | What is the geometric shape of the T* threshold? How does it evolve? |
| Luther Dispersion in algebraic domain | 5 | CRT derivation of F_k functional form |
| k-Gate Tier values (96.4%, 44.0%, etc.) in algebraic domain | 5 | Derive exact rates from idempotent structure |
| ω(b) ≥ 3 in all domains | 1-6 | Extend all invariants to three-factor composites |
| Montgomery Bridge in dynamical domain | 6 | How does the duality evolve as the height of Riemann zeros grows? |

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
