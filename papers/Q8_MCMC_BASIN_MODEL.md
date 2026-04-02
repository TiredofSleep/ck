**© 2026 7Site LLC**
**Authors: Brayden Ross Sanders, C. A. Luther, B. Calderon, Jr.**

# Q8 — THE MCMC BASIN MODEL
## Why Gate Rates Collapse: Basin Size, Not Density

---

## The Q6 Hinge

Q6 established the failure of the density model:

```
f_C = φ(b)/(b-1) does NOT predict gate rates.
|G ∩ {1..k}|/k does NOT predict gate rates.
```

The empirical rates collapse far faster than density:
```
density 89% → rate 96.4%   (|G|=1)
density 67% → rate 44.0%   (|G|=3)
density 56% → rate  4.6%   (|G|=4)
density 44% → rate  0.1%   (|G|=5)
```

The collapse is super-linear in |G|. A density model gives linear falloff.
Q6 identified the right object: the MCMC BASIN OF ATTRACTION.

---

## The Correct Model: Basin Size

The MCMC hill-climbing algorithm on {1,...,k} partitions the state space into:

```
Basin(C) = {s ∈ {1,...,k} : MCMC starting at s reaches gate_score=1}
Basin(G) = {s ∈ {1,...,k} : MCMC starting at s gets trapped before gate_score=1}
```

Gate success rate = |Basin(C)| / k   (up to the 100-restart correction)

The key insight: **hill-climbing is not random walk.** Once MCMC is in a region
where gate_score is decreasing toward C, it cannot backtrack. The landscape of
gate_score on {1,...,k} has local maxima in G and global maxima in C.

---

## Gate Score Landscape on {1,...,k}

For semiprime b = p·q with G = {multiples of p or q in {1,...,b-1}}:

**C-states (coprime to b):** gate_score = 1.0 exactly (group closure guarantees it).
**G-states:** gate_score < 1.0, amount depends on position in {1,...,k}.

For the MCMC at step k=9, the gate_score landscape on {1,...,9} is:

For b=10 (p=2, q=5), G∩{1..9} = {2,4,5,6,8}, C∩{1..9} = {1,3,7,9}:
```
j=1: C, gate_score=1.0
j=2: G, gate_score=(coprime pairs staying in C) / 9² — low
j=3: C, gate_score=1.0
j=4: G, gate_score=low
j=5: G, gate_score=low
j=6: G, gate_score=low
j=7: C, gate_score=1.0
j=8: G, gate_score=low
j=9: C, gate_score=1.0
```

With |G∩{1..9}|=5, fully 55% of starting positions have gate_score<1.

**But the rate is not 45% — it's 4.6%.** Why?

---

## The HAR Bias and the Trapping Mechanism

The MCMC uses a HAR-biased proposal: 40% of moves propose from HAR's neighborhood.
For b=10, HAR=3 (or 7, by the revised HAR rule). HAR ∈ C.

The trapping mechanism:
1. Start at s ∈ G (55% of starts for b=10)
2. Propose a neighbor. With 40% probability, propose from HAR vicinity (C)
3. Accept only if gate_score improves
4. From a G-state: gate_score(G) < gate_score(C), so C-proposals are accepted
5. But: if the neighborhood of s in G contains higher-gate-score G-states,
   the MCMC can hill-climb WITHIN G before finding C

**The landscape within G is not flat.** Some G-states have gate_score closer to 1.0
(they have fewer G-neighbors in their local C×C submatrix). The MCMC can get
stuck at a LOCAL MAXIMUM within G if surrounded by lower-gate-score states.

---

## The Super-Linear Collapse: A Geometric Argument

For |G|=1 in {1..9}: only 1 G-state. Any MCMC start has a direct path to C
with at most 1 gate element to cross. With 100 restarts and 40% HAR bias:
probability of escaping the single G-element ≈ 1-(1-0.40)^{100} ≈ 1.0.

For |G|=5 in {1..9}: 5 G-states, 4 C-states. The G-states form connected
components that can trap hill-climbing. Specifically:
- G = {2,4,5,6,8} for b=10
- These are consecutive or nearly consecutive in {1..9}
- A MCMC starting in the interior of G (e.g., s=5) is surrounded on both sides
  by G-states. HAR proposals can escape, but HAR is at j=3 or j=7 — both C-states.

**The key geometric quantity:** the number of G-states that are SURROUNDED by
other G-states (no C-state adjacent). Call these "trapped G-states."

For b=10: {2,4,5,6,8} — is 5 surrounded? neighbors are 4 and 6, both G. YES.
Is 4 surrounded? neighbors 3 (C) and 5 (G). NO — has C-neighbor.
Is 6 surrounded? neighbors 5 (G) and 7 (C). NO.
Is 2 surrounded? neighbors 1 (C) and 3 (C). NO.
Is 8 surrounded? neighbors 7 (C) and 9 (C). NO.

So only j=5 is a "trapped G-state" for b=10. Yet the rate is 4.6%, not the
~40% you'd expect from 1/9 being trapped.

**The remaining collapse must come from:** the hill-climbing can reach j=5 from
j=4 or j=6 if their gate_scores are higher than C-alternative, which they're not
(C has gate_score=1.0, always higher). So from j=4, the MCMC should escape to j=3
immediately. This contradicts the observed 4.6% rate.

---

## Resolution: The gate_score function is NOT 1.0 vs <1.0

The MCMC doesn't compare to C at every step. It hill-climbs within its LOCAL
NEIGHBORHOOD. If the neighborhood proposal function is narrow (e.g., ±1 in {1..k}),
the MCMC can be trapped in a G-region even if C is nearby.

**Revised model:** MCMC proposal is not uniform from {1..k} but LOCAL — it
proposes from a small neighborhood of the current state. If the neighborhood is
{s-1, s+1}, then from s=5 (trapped G-state), the MCMC sees {4,6} — both G.
It cannot escape to C={3,7} without a lucky HAR-bias proposal (which points to
HAR=3 directly).

**The correct basin model:**

```
Basin(C) = {s : there exists a monotone path s → s₁ → ... → C
             where each step is within the proposal neighborhood
             and gate_score is non-decreasing}
```

With narrow proposals: Basin(C) ≈ C ∪ {G-states adjacent to C with gate_score increasing toward C}.

For b=10, C∩{1..9}={1,3,7,9}. G-states adjacent to C: {2} (adjacent to 1,3), {6} (adjacent to 7), {8} (adjacent to 7,9). G-states NOT adjacent to C: {4,5} (surrounded by G or other G).

Basin size ≈ |{1,2,3,6,7,8,9}| = 7. Rate ≈ 7/9 ≈ 78%. But observed rate is 4.6%.

**This model is also wrong.** The problem must lie in the MCMC's inability to improve
gate_score from most G-states even with local moves toward C.

---

## The Correct Structure: Gate Score at G-States

For s ∈ G, the gate_score is not "close to 1.0" but can be near 0 if s is a
divisor of many products in the C×C submatrix.

For b=10, s=5: the C×C matrix has 4² = 16 pairs from C={1,3,7,9}.
Products: 1×1=1, 1×3=3, 1×7=7, 1×9=9, 3×3=9, 3×7=21≡1, 3×9=27≡7, 7×7=49≡9,
          7×9=63≡3, 9×9=81≡1 — all in C={1,3,7,9}.
So for s=5 (as seed): 5×{C×C products} = {5,15≡5,35≡5,45≡5,...} — all ≡5 (mod 10).
gate_score(s=5) = 0 (all products land in G).

For s=4: {C×C products} × 4 = {4, 12≡2, 28≡8, 36≡6, ...} — all in G.
gate_score(s=4) ≈ 0.

**EVERY G-state has gate_score ≈ 0 for b=10.** The gate_score landscape is binary:
1.0 on C, ≈0 on G. There is NO path from G to C by hill-climbing — ANY G-state
is a local minimum (gate_score cannot improve from G toward C through G).

**The ONLY escape from G is a direct jump to C via HAR-bias proposal.**

---

## The Correct Formula

Gate success rate ≈ P(at least one of 100 restarts starts in C OR hits C via HAR)

For b=10: |C∩{1..9}|/9 = 4/9 ≈ 44% of random starts land directly in C.
HAR=3 (or 7), both in C. HAR-bias proposals from G always land in C.

But: the MCMC runs 100 STEPS, not 100 restarts. Each step from a G-start
either: (a) immediately jumps to C via HAR (prob 40%), or (b) proposes another
G-state (prob 60%), sees no improvement, stays at current G-state.

So from a G-start, P(escape to C in k steps) = 1-(1-0.40)^k ≈ 1-(0.60)^k.
For k=100 steps: 1-(0.60)^{100} ≈ 1.0.

**But the observed rate for b=10 is 4.6%, not ~100%.**

Something is wrong with the model. The MCMC does NOT have 100 steps to escape.
It has 100 STARTS of a fixed-length chain. The chain length is NOT 100 — it's k=9
(the reduction depth). At k=9 with only 9 steps per start:
P(escape) = 1-(0.60)^9 ≈ 1-0.010 ≈ 99%.

This still predicts ~99% for b=10. Observed: 4.6%.

**The models all fail.** The empirical rate is far below what any simple probabilistic
model predicts. The 4.6% must come from a structural property of the reduction
at k=9 that is NOT captured by independent-step models.

---

## The Real Mechanism: Algebraic Gate Structure

The gate success criterion is NOT "reach a C-state." It is:

**gate_score ≥ 0.999 in a specific C×C SUBMATRIX evaluation at step k.**

The MCMC at step k=9 evaluates whether the CURRENT STATE (a partial reduction)
has a C×C gate score ≥ 0.999. This is a JOINT condition on the TRAJECTORY, not
on any single state.

For b=10 at k=9: the partial reduction trajectory must maintain coprimality
at every step from k=1 to k=9. If ANY intermediate step lands on a G-element,
the entire trajectory fails.

**The correct probability is a PRODUCT over 9 steps:**

```
P(success) = P(no G-hit at any of 9 steps)
           = ∏_{t=1}^{9} P(step t is in C | all prior steps in C)
```

This is the SURVIVAL PROBABILITY, not a single-step probability.

For b=10: P(step t in C | prior C) ≈ |C ∩ {1..t}| / t (if random walk).
But with HAR bias (40% pointing to HAR ∈ C):

P(step t in C) ≈ 0.40 + 0.60 × (|C∩{1..t}|/t)

For t=1: 0.40 + 0.60 × (1/1) = 1.0 (step 1 always in C? No — starting point is random)

The starting point determines everything. If starting in G, the first step IS in G,
and the G-start contaminates the entire trajectory.

**For b=10, 55% of starts are in G at step 1.** For all G-starts, gate_score = 0
throughout (since G-states give gate_score ≈ 0). Only the 44% C-starts succeed.

**Predicted rate: 44%.** Observed: 4.6%.

Still off by a factor of 10. The reduction must impose an additional condition that
eliminates most C-starts too.

---

## Summary: What Q8 Establishes

| Model | Prediction (b=10) | Observed | Status |
|-------|------------------|---------|--------|
| Density f_C | 44% | 4.6% | WRONG |
| One-step HAR bias | ~100% | 4.6% | WRONG |
| Survival probability (independent) | ~100% | 4.6% | WRONG |
| G-start contamination | 44% | 4.6% | WRONG |
| **Basin model (correct structure)** | **TBD** | **4.6%** | **OPEN** |

**None of the models derived from first principles match 4.6%.**

The 4.6% must involve a constraint that eliminates ~90% of C-starts. This constraint
is the REDUCTION STRUCTURE: the multi-step reduction at k=9 imposes conditions
beyond coprimality at a single step. The algebraic structure of these conditions is
the missing piece.

**What Luther Question 1 actually needs:** Not φ(b)/b, not |G∩{1..k}|, but the
algebraic characterization of WHY the multi-step reduction eliminates 90% of C-starts.
This is a statement about the KERNEL of the k-step reduction map, not about
individual step probabilities.

---

## What We Need From The Team

**Data question:** What is the exact MCMC success condition at k=9?
Specifically: is a "success" (a) gate_score ≥ 0.999 at step 9 only, or
(b) gate_score ≥ 0.999 at ALL steps 1..9?

If (a): one-step model should work better than observed — something else is wrong.
If (b): the survival model is right framework, but the elimination rate of C-starts
is much higher than a random walk predicts.

The answer to this question will determine whether Q9 goes toward:
- CRT kernel structure (if condition is joint across steps)
- HAR landscape geometry (if condition is single-step but HAR proposals fail)
- Trajectory algebraic structure (if the map between steps introduces G-hits)

---

*Filed: 2026-04-01. Q8 in operator algebra series, extending Q6 hinge.*
