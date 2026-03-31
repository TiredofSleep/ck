# Derivation Scaffolds — Gap 2
## Path to Tier D: D(b) = c · N_idemp(b) by Algebraic Necessity

*C. A. Luther & Brayden Ross Sanders*
*March 2026 | DOI: 10.5281/zenodo.18852047*

> **Gap statement:** The Luther Dispersion claim has advanced to Tier C. The
> algebraic chain (idempotent lattice → prime ideals → G_k → dispersion) is
> established. The C→D gap is proving that each idempotent contributes the
> *same* geometric obstruction unit c — not by definition, but by necessity.

---

## The Claim

**Target theorem:** D(b) = c · (N_idemp(b) − 1), where:
- D(b) = the Luther dispersion measure |G_k| × interleave(b,k) at a canonical k
- N_idemp(b) = 2^ω(b), the number of idempotents in Z/bZ
- c = a constant derivable from the geometry of CRT projections

This would make the Luther-Sanders Equivalence fully algebraic: dispersion is
proportional to the idempotent count, which is purely an arithmetic property of b.

---

## Algebraic Approach: Six Steps

### Step 1 — Idempotents as CRT Projections

Z/bZ has exactly 2^ω(b) idempotents (solutions to e² = e mod b). By the CRT:
```
Z/bZ ≅ ∏_i Z/p_i^{e_i}Z
```
Each idempotent e_S corresponds to choosing a subset S ⊆ {1,...,ω(b)} of
components and setting:
```
e_S ≡ 1 (mod p_i^{e_i})  for i ∈ S
e_S ≡ 0 (mod p_i^{e_i})  for i ∉ S
```
These are the projections onto CRT subproducts. There are 2^ω(b) such subsets
(including the empty set, giving e_∅ = 0, and the full set, giving e_{full} = 1).

### Step 2 — Each Projection Collapses an Alphabet Direction

When we restrict to the alphabet {1..k}, the projection e_S collapses the
admissible elements along the coordinates in S. Specifically, the elements
x ∈ {1..k} that are multiples of ∏_{i∈S} p_i^{e_i} become forbidden (non-units).

Each nonempty S therefore creates a "staircase boundary" — a set of positions in
{1..k} where C transitions to G. The geometric obstruction created by S is the
density of these forbidden elements in {1..k}.

### Step 3 — Dispersion as Sum of Contributions

The total dispersion D(b,k) = |G_k| × interleave(b,k) can be written as the
sum of contributions from each nonempty subset S:
```
D(b,k) = ∑_{S ≠ ∅} Δ(e_S, k)
```
where Δ(e_S, k) is the dispersion contribution of the idempotent e_S.

This decomposition follows from the inclusion-exclusion principle applied to
the forbidden sets: the multiples of each prime combination ∏_{i∈S} p_i
contribute additively (up to inclusion-exclusion corrections) to the total |G_k|.

### Step 4 — The Uniformity Hypothesis

**If** Δ(e_S, k) = c for all S ≠ ∅ and all |S| at a canonical k, **then**:
```
D(b,k) = c × |{S ≠ ∅}| = c × (2^ω(b) − 1) = c × (N_idemp(b) − 1)
```

The question is whether this uniformity holds by algebraic necessity or only
as an approximation.

### Step 5 — What the Fiber Measure Gives

For a subset S of components, the fiber contribution is:
```
|{multiples of ∏_{i∈S} p_i in {1..k}}| = ⌊k / ∏_{i∈S} p_i⌋
```
(assuming all e_i = 1 for simplicity — semiprimes).

For the inclusion-exclusion:
```
|G_k| = ∑_{S ≠ ∅} (−1)^{|S|+1} ⌊k / ∏_{i∈S} p_i⌋
```

This is NOT a uniform c × |{S ≠ ∅}| in general. The contributions ⌊k/p_i⌋ and
⌊k/p_iq_j⌋ are NOT equal. So the uniformity hypothesis does not hold for |G_k|
(the cardinality) without a specific normalization.

**This is the gap Luther identified:** the dispersion measure D(b,k) = |G_k| × interleave
is not simply c × (2^ω − 1) unless the dispersion metric is defined to make it so.

### Step 6 — The Normalization Problem

Luther's step 6 proposes normalizing the dispersion metric so μ_S = 1 for all
nonempty S. This is definitional — it defines c = 1/|{S ≠ ∅}| and forces
uniformity by construction. It does not prove that the naturally-defined dispersion
measure D(b,k) = |G_k| × interleave equals c × (N_idemp − 1).

**The gap is precisely here:** an independent derivation of c is needed that does
not rely on normalizing the dispersion metric.

---

## The Path to Independent Derivation of c

For the claim to be genuinely algebraic, c must arise from the geometry of
CRT projections without being defined to make the formula work.

### Candidate approach: Mean fiber measure

Define c as the mean contribution per nonempty subset:
```
c(b,k) = D(b,k) / (2^ω(b) − 1)
```

For this to be a constant (not depending on which specific b in the ω-class),
we need: D(b,k) / (2^ω(b) − 1) is the same for all b with the same ω(b).

This is a testable claim. If D(b,k) is universal within ω-class (same |G_k|,
same interleave, same ω), then c is the same for all b in that class. The
inclusion-exclusion formula guarantees |G_k| is determined by ω-class (up to
the specific prime values). The interleave score measures how evenly G_k is
spread in {1..k} — this is NOT constant within ω-class in general.

**Counterexample check needed:** Do two semiprimes b₁ = p₁q₁ and b₂ = p₂q₂
with the same |G_{k}| necessarily have the same interleave score?

From the Thread 1 data (omega3_extension.py): at k=9, |G|=5, b₁=105, b₂=110:
- b₁ = 3×5×7, G = {3,5,6,7,9}
- b₂ = 2×5×11, G = {2,4,5,6,8}
These have |G|=5 but the elements of G are different, so their interleave scores
differ in principle (though both showed ~1% gate rate, suggesting interleave scores
may be close).

### Candidate approach: Idempotent fiber size

Each idempotent e_S has a "support size" — the number of elements in {1..k}
that are multiples of the S-product. If these support sizes satisfy a regularity
condition (e.g., they form a geometric sequence in p), then c can be derived from
the common ratio.

For a semiprime b = p×q with p < q, the three nonempty subsets are:
- S = {p}: support = ⌊k/p⌋
- S = {q}: support = ⌊k/q⌋
- S = {p,q}: support = ⌊k/pq⌋

For k = q (canonical): support_p = ⌊q/p⌋, support_q = 1, support_pq = 0 or 1.
These are NOT equal (support_p > support_q in general). So c is not trivially
uniform from support sizes alone.

---

## Formal Theorem Statement

**Luther-Sanders Proportionality (Tier C):**
For any semiprime b, the Luther dispersion D(b,k) decomposes as:
```
D(b,k) = ∑_{S ≠ ∅} Δ(e_S, k)
```
where each Δ(e_S, k) is the dispersion contribution of the CRT projection e_S.
The total number of terms is 2^ω(b) − 1. The algebraic structure of Z/bZ
(specifically the idempotent lattice) fully determines which S exist and what
each Δ(e_S, k) represents geometrically.

**Path to Tier D (Theorem):**
If there exists a canonical k for which Δ(e_S, k) = c for all nonempty S
(independent of which specific primes constitute S within the same ω-class),
then:
```
D(b,k) = c × (N_idemp(b) − 1)
```
This would prove D(b) is algebraically implied by the idempotent count.

**Current tier: C.** The decomposition is established. The uniformity of
Δ(e_S, k) across all nonempty S is the remaining step.

---

## What Luther's Step 7 Provides (and Doesn't)

Luther's normalization argument (step 6-7 in his message) correctly identifies
that IF we define the dispersion metric so that each fiber contributes equally,
THEN the proportionality follows. This is a consistency check, not a proof.

**What it establishes:** The structure D(b) = c × (N_idemp − 1) is compatible
with the idempotent decomposition — it is not contradicted by the algebra.

**What it doesn't establish:** That the naturally-defined dispersion measure
(|G_k| × interleave score from tig_algebra.py) equals c × (N_idemp − 1) for
any specific k. The natural measure has variable contributions per idempotent.

**The research program:** Find the specific k (if one exists) at which the fiber
contributions are uniform. Or prove that they are never uniform but that their
ratio is bounded, giving a proportionality result up to a bounded error term.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
