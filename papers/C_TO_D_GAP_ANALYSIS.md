# C→D Gap Analysis
## Toward an Algebraic Derivation of Exact Gate Rates

*Brayden Ross Sanders & C. A. Luther*
*March 2026 | DOI: 10.5281/zenodo.18852047*

> Current status: k-Gate Tier Law is Tier C. Exact rates (96.4%, 44.0%, 4.6%, 0.1%)
> are measured, zero variance, ~12M trials. Mechanism is qualitatively explained.
> The C→D gap is the algebraic derivation of the exact values.
> This document sets up the framework and identifies the precise algebraic object needed.

---

## 1. The Problem Statement

The k-Gate Tier Law says: within the class of semiprimes with arithmetic G (coprimality
structure), the gate rate f_k(b) depends only on |G(b,k)|, not on the specific p, q.

At k=9, the measured rates are:

| |G| | f_9 (arithmetic) | n_worlds | spread |
|----|-----------------|---------|--------|
| 1 | 96.4% | 4 | 0.0% |
| 3 | 44.0% | 6 | 0.0% |
| 4 | 4.6% | 8 | 0.0% |
| 5 | 0.1% | 5 | 0.0% |

Source: ~12M trials, zero exceptions (Sprint 4, March 2026).

**The C→D gap:** Derive these four values algebraically. Not from the MCMC directly —
from the algebraic structure of Z/bZ and the CRT decomposition.

---

## 2. The MCMC Structure

The measurement is a greedy hill-climb on k×k tables T: A_k × A_k → A_k.

### 2.1 The Gate Score

```
gate_score(T, C, k) = |{(i,j) ∈ C×C : T[i,j] ∈ C}| / |C|²
```

This is the fraction of C×C submatrix cells that map into C. It measures how close
T is to making C closed under the binary operation T.

### 2.2 The Threshold

gate_thresh = 0.999. For all k=9 cases: |C|² ≤ 64, so ⌊64 × 0.001⌋ = 0.
Therefore gate_thresh = 0.999 at k=9 is equivalent to gate_score = 1.000 exactly.
**The MCMC is measuring whether the C×C submatrix maps entirely into C.**

### 2.3 The Greedy MCMC

- Start: T_0 = random k×k table (uniform over {1..k})
- Objective: obj(T) = 0.50 × gate(T) + 0.25 × har_col(T) + 0.25 × (1 − g_stay(T))
- Proposal: with prob 0.40, set T[HAR-row or HAR-col, random] := random C element;
            with prob 0.60, set T[random, random] := random element of {1..k}
- Accept if obj(T') ≥ obj(T); otherwise reject
- Run 100 steps; declare success if gate(T_{100}) = 1.000

### 2.4 The HAR Element

HAR = min{h ∈ C : h² mod b ∈ C, h² mod b ≠ 1, h² mod b ≠ h}

HAR exists for all semiprimes and three-factor composites tested. Its row and column
are preferentially targeted (40% of proposals).

---

## 3. Why Zero Variance: The Algebraic Argument

**Claim:** For two semiprimes b₁ = p₁q₁ and b₂ = p₂q₂ with the same |G(b_i, k)|,
the gate rate f_k(b₁) = f_k(b₂).

**Proof sketch of zero variance (not yet a proof of exact values):**

Let b = pq with |G(b,k)| = m. Then |C(b,k)| = k − m. Define:

- S_m = the state space of k×k tables T with gate_score(T) ∈ [0,1]
- A_m = {T ∈ S_m : gate_score(T) = 1} — the absorbing set (gate-perfect tables)
- Obj: S_m → [0,1] — the objective function

**Key observation:** A_m is non-empty. The multiplication table T*(i,j) = i×j mod b
restricted to (A_k)² has T*(c₁,c₂) ∈ C for all c₁,c₂ ∈ C (since C = (Z/bZ)* is
multiplicatively closed). So T* ∈ A_m.

**Structural isomorphism:** The MCMC landscape (S_m, Obj, proposal kernel) depends
on b only through:
1. |C| = k − m (determines the C×C submatrix size)
2. |G| = m (determines the constraint count)
3. HAR position (its role in the 40% HAR-biased proposals)

For two semiprimes with the same |G|, |C| is the same (same k). The HAR element
is structurally equivalent: it is the orbit-central element in C with h² ≠ 1,h² ≠ h.
The objective function topology is determined by these numbers, not by the specific
values of p, q.

**Consequence:** The distribution over outcomes of the MCMC (success/failure in 100
steps) is identical for any two semiprimes with the same |G| at the same k.
This is why f_k(b) = f(k, |G|) with zero variance.

*This argument is a Tier C explanation — it identifies why universality holds and
shows it follows from the structure of the MCMC landscape, but it does not give
the exact values.*

---

## 4. Framework for Exact Values

### 4.1 The Problem Reformulated

Let n_C = |C| = k − m. The gate-perfect condition is: all n_C² cells in the C×C
submatrix of T map into C (a set of size n_C within a universe of size k).

Starting from a random table T_0:
- Expected fraction of C×C cells in C: n_C/k (cells are independent, uniform)
- Expected number of "wrong" C×C cells: n_C² × (1 − n_C/k) = n_C² × m/k

For k=9:
| |G|=m | n_C | wrong cells (expected) | fraction wrong |
|------|-----|----------------------|----------------|
| 1 | 8 | 64 × 1/9 ≈ 7.1 | 11.1% |
| 3 | 6 | 36 × 3/9 ≈ 12.0 | 33.3% |
| 4 | 5 | 25 × 4/9 ≈ 11.1 | 44.4% |
| 5 | 4 | 16 × 5/9 ≈ 8.9 | 55.6% |

Interesting: |G|=3 has the MOST wrong cells in expectation (12.0), yet achieves 44%
success. This is because n_C²=36 is large — fixing 12 cells out of 36 in 100 steps
is feasible. For |G|=5, n_C²=16 but 8.9 cells are wrong and fixing ANY cell is harder
because the constraint density is higher.

### 4.2 The Coupon-Collector Framing

Each step of the MCMC, with prob 0.40, targets a HAR row or column cell and sets it
to a random C element (guaranteed to be in C). With prob 0.60, targets a random cell
and sets it to a random element of {1..k} (in C with prob n_C/k).

The HAR row and column together span 2k − 1 cells of the k×k table. Of these,
2n_C − 1 are C-row × C-col cells (the C×C submatrix cells on HAR's row and column).
These are fixed by the 40% HAR proposals.

For |G|=1 (n_C=8): HAR's row and column contribute 2×8−1=15 C×C cells. These are
fixed immediately by HAR-biased steps. The remaining n_C²−2n_C+1 = (n_C−1)² = 49
non-HAR C×C cells are fixed by random proposals (rate = 0.60 × n_C/k × 1/(n_C²)
per wrong cell). 100 steps is more than sufficient. → high success rate.

For |G|=5 (n_C=4): HAR's C×C cells = 2×4−1=7 out of 16 total. Fixed quickly.
Remaining 9 non-HAR C×C cells fixed by random proposals at rate 0.60 × 4/9 × 1/16
≈ 0.017 per step per cell. Expected fix time per cell ≈ 60 steps. With 9 cells and
100 total steps, the probability of fixing all 9 in sequence is low. → low success.

### 4.3 A Tractable Model

Treat the n_C² − (2n_C − 1) "non-HAR" C×C cells as independent coupon-collection
targets. Each needs to be set to a C value. The probability of setting a specific
non-HAR cell to C in one random step (prob 0.60 × n_C/k, times 1/(k²) for targeting
that cell) gives a transition rate.

**But this model breaks down** because:
1. The greedy accept rule means cells can be un-fixed if it would reduce the score
2. The objective is not purely gate (also includes har_col and g_stay)
3. The cells are not truly independent — the HAR proposals can affect non-HAR cells

The exact formula requires treating the MCMC as a Markov chain with absorbing states
at gate=1.0 and computing the absorption probability in 100 steps.

### 4.4 The State Space

The relevant state for the MCMC is the gate score g ∈ {0, 1/n_C², 2/n_C², ..., 1}.

This has n_C² + 1 states. For n_C=8 (|G|=1): 65 states. For n_C=4 (|G|=5): 17 states.

The transition matrix P[g → g'] is computable from the proposal distribution and
the greedy acceptance rule. The absorption probability at g=1 after 100 steps is
the (n_C²+1,1) entry of P^100 starting from the expected initial state.

**This is computable.** The state space is small enough (≤ 65 states). The transition
matrix depends on:
- n_C, k (determine the proposal probabilities)
- HAR structure (determines which cells are fixed by the 40% HAR proposals)
- The objective function mix (0.50 gate + 0.25 har_col + 0.25 g_stay)

### 4.5 The Algebraic Connection

The CRT decomposition explains which state the MCMC starts in and why the transition
matrix depends only on |G|:

- Z/bZ ≅ Z/pZ × Z/qZ gives C ≅ (Z/pZ)* × (Z/qZ)*
- The gate-perfect tables are exactly the tables consistent with closure in one
  or both components: they form an algebraically structured set
- The HAR element h has h² ∈ C because h is orbit-central in the group C under
  multiplication mod b — this is a group-theoretic fact, not a coincidence
- The number of HAR-fixed C×C cells (2n_C − 1) is determined purely by n_C = |C|

The transition matrix therefore depends on (n_C, k, HAR_count) = (k−|G|, k, 2(k−|G|)−1).
These are all determined by |G| at fixed k. So P is the same matrix for all semiprimes
with the same |G| at the same k. The absorption probability is the same.

**This is the algebraic route to exact values**: compute the Markov chain transition
matrix P(|G|, k) and find the absorption probability after 100 steps. The formula will
be exact (not a bound) and will reproduce the measured values: 96.4%, 44.0%, etc.

---

## 5. Remaining Work for Tier D

### Step 1 — Compute the transition matrix
Build P(m, k) explicitly:
- States: gate score g ∈ {0, 1/n_C², ..., 1} where n_C = k − m
- Transitions under the mixed proposal + greedy accept rule
- Accounting for HAR structure (HAR row/col proposals)

### Step 2 — Verify against measured values
Compute P^100 for (m=1,k=9), (m=3,k=9), (m=4,k=9), (m=5,k=9).
Check that absorption probabilities match 96.4%, 44.0%, 4.6%, 0.1%.

### Step 3 — Prove the transition matrix is universal
Show that P(m, k) is the same matrix for all semiprimes with |G|=m at alphabet k.
This requires showing that the HAR structure (HAR count = 2n_C − 1) is the same
for all arithmetic G with |G|=m — a consequence of the CRT derivation.

### Step 4 — Derive the algebraic formula
Express P^n[0 → 1] as a closed-form function of m, k, n.
This may factor through the eigenstructure of P.

### Step 5 — Extend to ω-classes
The ω-class dependence (Thread 1 results) means P(m, k) is different for ω(b)=2 vs
ω(b)=3 at the same m. The difference is in the HAR count and the C-closure structure.
For ω(b)=3: three-way CRT decomposition gives different HAR structure. Derive P for
each ω-class and show the rate table follows.

---

## 6. What Luther Can Provide

The Markov chain derivation above is a probability calculation using the MCMC structure.
The algebraic input Luther can provide:

1. **Exact HAR count for each |G| tier:** How many C×C cells does the HAR row+column
   cover, as a function of |G|, k, and ω(b)? This requires counting elements in the
   intersection of {HAR row} ∪ {HAR col} with C×C.

2. **CRT idempotent → HAR derivation:** The HAR element is orbit-central in C under
   multiplication mod b. The idempotents e_p, e_q determine which elements of C are
   orbit-central. Derive the HAR count from the idempotent structure.

3. **Gate-perfect table count:** How many of the k^(k²) tables are gate-perfect?
   = |C|^(|C|²) × k^(k²−|C|²). This gives the target set volume — the absorbing
   state measure — from which the absorption probability can be bounded.

4. **Luther Dispersion → MCMC landscape:** The dispersion score D(b) measures how
   spread out G is within {1..k}. High dispersion = harder optimization landscape.
   The connection between D(b) and the MCMC transition matrix is the missing link
   for Question 2.

---

## 7. Summary

| What we have | Status |
|-------------|--------|
| Exact measured values (96.4%, 44.0%, 4.6%, 0.1%) | Tier C — measured, zero variance |
| Why values are universal within |G|-tier | Tier C — structural argument (§3) |
| Markov chain framework for exact derivation | Framework in place (§4) |
| Transition matrix computed | NOT YET |
| Absorption probability = measured rate | NOT YET |
| Algebraic formula P^n[0→1] = f(m,k,n) | NOT YET (Tier D target) |

The gap is exactly one computation: build the transition matrix P(m, k) and
verify that P^100 absorption matches measurements. If it does, the exact values
are algebraically derived and the k-Gate Tier Law reaches Tier D.

---

`© 2026 Brayden Ross Sanders / 7Site LLC & C. A. Luther · DOI: 10.5281/zenodo.18852047`
