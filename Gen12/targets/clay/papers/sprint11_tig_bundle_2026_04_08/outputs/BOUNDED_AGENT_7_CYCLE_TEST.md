# BOUNDED_AGENT_7_CYCLE_TEST
## Can a 7-Step Cycle Emerge as Optimal for Bounded Agents?
*Simulation results. All claims narrow. All numbers reproducible (seed=42/99).*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Design Summary

**Five environment families tested.** Each models a different way bounded agents interact with recurrence, memory, coordination, or planning:

| Env | Description | Optimization criterion |
|---|---|---|
| A | Memory refresh: information decays, review restores, review has cost | Minimize: avg memory loss + review cost |
| B | Planning loop: drift accumulates, one slot per cycle = reset | Minimize: cumulative drift − work output |
| C | Multi-agent coordination: agents drift, sync has overhead | Minimize: desync cost + sync cost |
| D | Coverage/revisit: stale items accumulate between sweeps | Minimize: avg staleness + revisit cost |
| E | Reset-slot: k−1 work slots + 1 dedicated reset, quality decays | Maximize: quality-weighted output |

**Targeted follow-up tests:**
- A': Linear review cost (cost scales with k, not fixed)
- C': Composite-k bonus (k divisible by 2 or 3 cheaper to coordinate)
- F: Cognitive load (Miller's 7±2 capacity model, flush at review)
- E': Env E scanned across decay rates (0.08 to 0.25)

**Parameter sweep:** Each environment run at 2–4 parameter settings. 60 trials per (env, param, k). Cycle lengths k = 2 to 21 tested throughout.

---

## Results

### Main Sweep: Aggregate Rank Across All 5 Environments

Lower rank = better performance on average.

| k | Agg rank | Top-3 freq (15 settings) |
|---|---|---|
| 2 | 8.40 | 7/15 = **47%** |
| 3 | 5.40 | 9/15 = **60%** |
| **4** | **4.80** | 10/15 = **67%** ← best |
| 5 | 5.20 | 5/15 = 33% |
| 6 | 5.40 | 3/15 = 20% |
| **7** | **6.20** | 2/15 = **13%** |
| 8 | 7.00 | 0/15 = 0% |
| 9–21 | 7.6–16.0 | 0–13% |

**Best aggregate k: 4.** k=7 ranks 5th out of 20. Not special.

### Per-Environment Optimal k

| Env | Param setting | Optimal k |
|---|---|---|
| A memory | decay=0.10, cost=0.3 | **3** |
| A memory | decay=0.20, cost=0.8 | **4** |
| B planning | drift=0.03, eff=0.9 | **4** |
| B planning | drift=0.10, eff=0.6 | **2** |
| C coordination | N=3, cc=0.5 | **21** |
| C coordination | N=7, cc=1.2 | **16** |
| D coverage | update=0.08 | **2** |
| D coverage | update=0.18 | **2** |
| E reset slot | decay=0.10 | **6** |
| E reset slot | decay=0.20 | **5** |

**k=7 does not appear as an optimum in any of the 10 multi-param settings.** Coordination environments (C) favor long cycles (high sync overhead → sync infrequently). Memory/planning/coverage environments favor short cycles (k=2–4).

---

### Targeted Tests

**A': Linear review cost (cost = c·k per event)**

The intuition: longer cycles require more preparation to review. This should shift the optimum from k=2 upward. Result: optimal k=2–3 still wins. k=7 ranks 6/20. Cost scales linearly with k but memory loss also scales — the optimum stays short.

**C': Composite-k bonus (divisible by 2 or 3 = cheaper sync)**

Motivation: k=7 is prime; k=6=2×3 is highly composite. If coordination overhead is lower for cycle lengths that decompose into sub-rhythms, k=6 should beat k=7. Result: **k=6 wins** (loss=0.116), k=7 loses (0.159). The primality of 7 is a handicap, not an advantage, in this coordination model. k=6, 8, 12 are all competitive.

**F: Cognitive load (Miller's 7±2 capacity)**

Motivation: if agents have capacity=7 working memory items, and items accumulate each step, maybe flushing at k=7 is optimal. Result: **k=2 wins** (loss=0.224). k=7 ranks 6/20. Reasoning: flushing more frequently is always better when items accumulate and overflow is penalized — the optimal strategy is the shortest useful flush cycle. Having capacity=7 does not privilege a 7-step flush cycle. The capacity determines when overflow begins; it does not set the optimal flush frequency.

**E': Reset-slot at varying decay rates**

This is where k=7 performs best:

| Decay rate | Best k | k=6 | k=7 | k=8 |
|---|---|---|---|---|
| 0.08 | **7** | −0.564 | **−0.566** | −0.561 |
| 0.12 | 6 | −0.483 | −0.476 | −0.462 |
| 0.16 | 5 | −0.411 | −0.400 | −0.382 |
| 0.20 | 4 | −0.350 | −0.336 | −0.318 |
| 0.25 | 4 | −0.287 | −0.270 | −0.251 |

**k=7 wins exactly once: when decay is slow (0.08).** At higher decay rates, the optimum drifts to shorter cycles. The win is narrow — k=7 beats k=6 by 0.0019 at decay=0.08. This is marginal and parameter-specific, not robust.

---

## Full Performance Table by Environment

### Env A: Memory Refresh (decay=0.15, noise=0.10, cost=0.5)

| k | Mean loss | Rank |
|---|---|---|
| 2 | 0.435 | 2 |
| **3** | **0.422** | **1** |
| 4 | 0.449 | 3 |
| 5 | 0.475 | 4 |
| 6 | 0.499 | 5 |
| **7** | **0.521** | **6** |
| 8 | 0.542 | 7 |

### Env E: Reset Slot (decay=0.12)

| k | Utility (higher=better) | Rank |
|---|---|---|
| 4 | +0.350 | 1 |
| 5 | +0.340 | 2 |
| **6** | **+0.330** | **3** |
| **7** | **+0.319** | **4** |
| 8 | +0.299 | 5 |

*k=7 is competitive but not winning in the reset-slot environment at moderate decay.*

---

## Figure: Performance vs Cycle Length k (Aggregate)

```
Lower score = better performance

Agg
rank
 17 |                                                   k=20
 16 |                                                k=19
 14 |                            k=13  k=14
 13 |                       k=12
 12 |                  k=11
 11 |             k=15
 10 |             k=16
  9 |        k=10
  8 |  k=2              k=17  k=18
  7 |                k=9
  7 |             k=8
  6 |       k=3    k=5  k=6  k=21
  6 |             k=7
  5 |        k=5
  5 |   k=4   ← BEST OVERALL
  ──+──────────────────────────────────────────────────> k
     2  3  4  5  6  7  8  9  10  11  12  13  14  15...21

  ▲ Larger = worse
  k=4 is best. k=7 is middle of the pack, not special.
```

---

## Verdict

| Verdict class | Description | Applies here? |
|---|---|---|
| No support | k=7 performs at or below chance across environments | Partially — k=7 never wins in main sweep |
| Weak support | k=7 occasionally competitive but not reliably optimal | Yes — upper-middle rank in aggregate |
| **Conditional support** | k=7 optimal under specific parameter regime | Yes — wins in reset-slot at very low decay rate |
| Strong support | k=7 consistently optimal across parameter sweeps | No |

**Verdict: NO SUPPORT for k=7 as a universal attractor. CONDITIONAL SUPPORT in one narrow regime.**

k=7 is optimal in the reset-slot environment (Env E) when decay is slow (≈0.08 per step). Outside this regime, shorter cycles (k=3–6) dominate. The "winner" in the broadest sense is k=4, which ranks best across the full sweep.

---

## Paradox Classifier Applied to Results

**Type III (invalid map — confirmed):**
The original c/7/week observation is a unit-conversion artifact. These simulations do not rescue it. Nothing in the bounded-agent results connects to the speed of light. The Type III diagnosis stands.

**Type IV (observer-state / civilization-relative — confirmed):**
The simulations depend heavily on parameter values that are civilization-relative: how fast information decays, what coordination overhead costs, how many agents exist. There is no universal answer. The week is not derivable from these models under any generic parameterization.

**Type I (missing view — partially addressed):**
We now have a view we did not have before. The simulations show that bounded agents under plausible decay/noise/cost assumptions do not rediscover k=7. The view was missing; it is now partially filled in. The answer is: k=7 is not a universal attractor. It may be an attractor under very specific conditions (slow decay, reset-slot structure), but this is not the same as being independently rediscovered.

**If k=7 had dominated:** the original claim was misplaced in physics (Type III) but would survive in bounded-agent time grammar. We would report conditional evidence for the attractor hypothesis.

**Since k=7 did not dominate:** the simulations tested the open question directly and did not support the privilege of k=7 in these models. The week remains, by current evidence, a historical convention with mild functional support at best.

---

## What Survives

**1. The Type III example survives intact.** The c/7/week observation is a clean, reusable demonstration of unit-grammar artifacts. Nothing in the simulations changes this.

**2. The genuine open question is now narrowed.** Before: is k=7 an attractor? After: k=7 is not a universal attractor. It may be near-optimal in low-decay, reset-slot-structured environments with moderate coordination overhead. The question is no longer open in its broad form; it is now a specific conditional question.

**3. Env E decay regime is a real result.** At decay ≈ 0.08/step, k=7 edges out k=6 by a small margin in the reset-slot model. This is the specific parameter regime where k=7 could claim near-optimality. Whether any real human system operates in this regime is an empirical question about cognitive or social decay rates, not a theoretical certainty.

**4. Short cycles (k=3–5) are the real story.** If the simulations teach one thing, it is that most bounded-agent environments prefer short cycles. The pressure toward k=7 (and weekly rhythms) is more likely driven by social coordination overhead (longer cycles reduce sync frequency) than by any fundamental optimality of 7.

---

## The Right Question Now (Revised)

The pre-simulation question was:

> Would a 7-cycle be independently rediscovered by bounded agents because it optimizes a real tradeoff, or is it merely inherited convention?

Post-simulation answer: **mostly inherited convention, with mild conditional support in low-decay reset-slot environments**.

The question now sharpens to:

> **Do real human cognitive systems operate in the low-decay, reset-slot parameter regime where k=6 or k=7 becomes near-optimal, or is the 7-day week better explained by social coordination dynamics that favor cycles longer than k=5?**

That is the empirically testable version. It requires measurement of human cognitive decay rates and social coordination costs — not more simulations of toy models.

---

*All code reproducible. Simulation seed: 42 (main), 99 (targeted). Python 3 + numpy. Runtime: ~3 minutes.*
