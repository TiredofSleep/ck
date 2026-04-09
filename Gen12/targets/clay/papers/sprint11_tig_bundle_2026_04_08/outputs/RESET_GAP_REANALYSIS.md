# RESET_GAP_REANALYSIS
## Is There a Reset-Gap Grammar? Or Just k=4?
*Simulation-grounded. All numbers from code. Seed=42.*

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## Part 1 — What Is Dead, What Survived

**DEAD:**
- k=7 as universal attractor. Simulations rejected this. k=4 wins broadly.
- c/7/week as physics. Type III error. Closed.
- "Bounded agents rediscover 7." No evidence across 15 parameter settings.

**SURVIVED:**
- Short cycles dominate most task classes (k=3–5 best in memory, planning, coverage).
- Long cycles emerge when coordination overhead dominates (Env C: k=16–21 when sync is expensive).
- k=7 is near-optimal in the specific low-decay reset-slot regime (decay≈0.08, Env E).
- The persistent motif across environments is **reset-gap structure**, not the integer 7.

The reanalysis question: is there a lower-dimensional invariant — a dimensionless ratio — that predicts good cycle lengths better than raw k alone?

---

## Part 2 — Dimensionless Reset-Gap Variables

For each environment, the relevant quantities:

**γ (gamma) = k / half-life**

The reset interval measured in units of the decay half-life. This is the natural dimensionless ratio for memory/quality environments.

- γ < 1: resetting more often than the decay half-life. Fast refresh.
- γ ≈ 1: resetting at approximately the decay timescale. Balanced.
- γ >> 1: resetting much slower than decay. Letting quality degrade substantially before recovery.

**For Env A (decay=0.15, half-life=4.3 steps):**

| k | γ = k/HL | Loss |
|---|---|---|
| 2 | 0.47 | 0.467 |
| **3** | **0.70** | **0.441** ← optimal |
| 4 | 0.94 | 0.451 |
| 5 | 1.17 | 0.473 |
| 7 | 1.64 | 0.521 |
| 10 | 2.35 | 0.593 |

Optimal gamma at decay=0.15: **γ* ≈ 0.70**. The optimal cycle is roughly 70% of one half-life.

**For Env E (decay=0.08, half-life=8.3 steps) — the k=7 win case:**

| k | γ | Loss |
|---|---|---|
| 6 | 0.72 | best neighbor |
| **7** | **0.84** | **−0.566 ← optimal** |
| 8 | 0.96 | −0.561 |

Optimal gamma: **γ* ≈ 0.84**. Still below 1.0. Still "reset before a full half-life."

**Critical finding: γ* is not stable across decay rates.**

| Decay | Best k | Half-life | γ* |
|---|---|---|---|
| 0.05 | 5 | 13.5 | 0.37 |
| 0.08 | 4 | 8.3 | 0.48 |
| 0.10 | 4 | 6.6 | 0.61 |
| 0.15 | 3 | 4.3 | 0.70 |
| 0.20 | 3 | 3.1 | 0.97 |
| 0.25 | 3 | 2.4 | 1.25 |
| 0.30 | 3 | 1.9 | 1.54 |

**γ* range: [0.37, 1.54]. Mean: 0.84. Std: 0.40.**

The std/mean ratio is 0.47 — nearly 50% coefficient of variation. **Gamma is NOT a stable invariant.** The optimal reset interval, measured in half-lives, varies by a factor of 4 across the tested decay range. There is no single dimensionless ratio that collapses the optimal-k problem.

**Why gamma is not stable:** At low decay rates, the cost of over-refreshing (wasted review overhead) dominates — so the optimal gamma is small (refresh early, cheaply). At high decay rates, quality degrades fast regardless, so the marginal cost of waiting decreases and gamma rises. The tradeoff is nonlinear and shifts with the relative magnitude of decay loss vs review cost.

**For Env C (coordination, dps=0.1, N=5):**

Desync timescale ≈ 14 steps. Best k=19, giving k/desync_time = 1.34. The coordination environment selects k well above the desync timescale — not because k=19 is somehow optimal per se, but because sync cost (0.8/event) is high enough that it is cheaper to let agents drift for a long time and pay the desync penalty than to sync frequently. This is a different regime entirely: coordination cost dominates over desync loss.

---

## Part 3 — Is There a Reset-Gap Grammar?

**Yes and no. Here is the precise statement:**

**What is structurally stable across all environments:**

Every optimal cycle has the form: [buildup phase of length w] + [reset of length 1]. The reset slot always appears. The grammar is: **w units of accumulation followed by 1 reset event.** This is the reset-gap structure.

What is NOT stable: the value of w. It ranges from 1 to 20+ depending on decay rate, coordination cost, and reset effectiveness. The grammar is real; the integer instantiation is not.

**Test: does (w+1) grammar supersede raw k?**

For Env A nested (two decay timescales, inner + outer reset):

| Structure | Inner k | Outer k | Loss | vs flat k=inner |
|---|---|---|---|---|
| w=2: 2+1 nested | 3 | 6 | **0.378** | flat k=3: 0.441 → nested wins by **0.063** |
| w=3: 3+1 nested | 4 | 12 | **0.429** | flat k=4: 0.451 → nested wins by **0.022** |
| w=4: 4+1 nested | 5 | 20 | 0.501 | flat k=5: 0.473 → nested **loses** by 0.028 |
| w=6: 6+1 nested | 7 | 42 | 0.625 | flat k=7: 0.521 → nested **loses** by 0.104 |

**Result: nested reset architecture wins for small w (w=2,3) but loses for larger w (w≥4).**

The nested structure beats flat cycles when two decay processes operate at different timescales (fast and slow components). When w is small (inner cycle=3,4), the nested architecture efficiently handles the fast component while the outer cycle handles slow drift. When w is large (inner cycle=7+), the overhead of the nested structure outweighs the benefit — flat k is better.

**This is the fractal test result:** A nested reset grammar exists and outperforms flat cycles for multi-timescale environments — but **the optimal nesting does not privilege 7**. The w=2 (inner=3) and w=3 (inner=4) structures win. k=7 nesting is dominated.

---

## Part 4 — Mutation Table

| Environment | Best k | Optimal gamma (γ*) | Does k=7 survive nearby? | Stable feature |
|---|---|---|---|---|
| A: Memory refresh (decay=0.15) | **3** | 0.70 | No (rank 6) | Reset at ~70% of half-life |
| A: Memory refresh (decay=0.08) | **4–5** | 0.48–0.61 | No (rank 7–9) | Reset well before half-life |
| B: Planning/drift (drift=0.05) | **3** | 0.15 × drift_time | No (rank 5–6) | Short accumulation before correction |
| C: Coordination (cc=0.8, N=5) | **16–21** | 1.34 × desync_time | No (rank 12–14) | Sparse sync when overhead is high |
| D: Coverage (update=0.12) | **2** | Very small | No (rank 9+) | Maximum revisit frequency |
| E: Reset slot (decay=0.08) | **7** | 0.84 | **Yes — barely (0.002 margin)** | Reset ≤ 1 half-life |
| E: Reset slot (decay=0.12) | **6** | 0.72 | Adjacent (k=7 rank 2 by 0.007) | Same structure, faster decay |
| E: Reset slot (decay=0.20) | **4** | 0.77 | No (rank 5) | Short cycles dominate at high decay |
| Nested (w=2, inner=3) | inner=**3** | — | No | Two-timescale decay; small inner k |
| Nested (w=3, inner=4) | inner=**4** | — | No | Two-timescale decay |

**Summary of "stable feature" column:** The stable feature is always a version of "reset cadence relative to accumulation timescale." It is never "the integer 7."

---

## Part 5 — The Nested Architecture Result

**Does nested reset grammar explain the landscape better than raw k?**

Partially. For multi-timescale environments (fast and slow decay components), yes: a (w+1) inner/(w+1)w outer structure outperforms flat k=w+1 for w ≤ 3. The improvement is real (0.063 for w=2) and meaningful.

For single-timescale environments, no: flat k beats nested k for the same inner cycle when there is only one decay rate. The overhead of the outer reset eats the benefit.

**What this means for the 7-attractor question:**

If the week's function is as an *outer* cycle in a nested (days + weeks) reset grammar — e.g., daily tasks are the inner cycle and weekly review is the outer cycle — then the nested architecture would need inner k=days and outer k=7×days. The nested model says small inner k (3–4 day units) outperforms larger inner k. A daily inner cycle (k=1) nested inside a weekly outer cycle (k=7) would correspond to w=6, which the simulation penalizes (loss=0.625 vs flat 0.521). The nested grammar does not rescue 7 as the outer cycle.

---

## Part 6 — Final Verdict

**Three candidate framings, evaluated:**

| Framing | Verdict |
|---|---|
| "7 is dead" | Correct for universal claims. k=7 is not a universal attractor. |
| "7 survives only as a local reset optimum" | Correct but narrow. k=7 is near-optimal at decay≈0.08 in the reset-slot model with a margin of 0.002 over k=6. This is not a strong survival. |
| **"Reset-gap grammar is the true invariant"** | **Correct, with one correction: the grammar is real, the integer is not fixed.** The stable object is: [w buildup slots] + [1 reset]. The optimal w shifts with decay rate, coordination cost, and task structure. 7 is one contingent value of w+1, valid only in a narrow parameter regime. |

**The true stable object:** a reset-gap grammar parameterized by the ratio of buildup length to accumulation timescale. Not a universal integer. Not 7. A ratio — and that ratio varies by a factor of 4 across plausible environments.

---

## Figure: Raw k vs Reset-Density Interpretation (Env A)

```
Loss                  Raw k landscape (Env A, decay=0.15)
0.70 |                              ·  ·  ·  ·  ·
0.65 |                         ·
0.60 |                    ·
0.55 |               ·
0.50 |          ·
0.45 |     · ·
0.44 |   *            ← k=3 optimal
     |
     +--+--+--+--+--+--+--+--+--+--+---> k
        2  3  4  5  6  7  8  9 10 11

Gamma (γ = k/half_life) landscape (same data)
0.70 |
0.65 |
0.60 |                              ·  ·  ·
0.55 |                         ·
0.50 |                    ·
0.45 |               ·
     |     · *← γ*≈0.70 (k=3)
     |  ·
     +--+------+------+------+------> γ
       0.5    1.0    1.5    2.0

Reset-density framing: optimal gamma ≈ 0.5–0.7 (sub-half-life)
But gamma itself shifts with decay rate — NOT a fixed invariant.
The grammar is: reset before complete decay. The integer is contingent.
```

---

## Conclusion

**The reset-gap grammar is the real surviving object from this entire arc.** The specific finding:

1. Every environment optimizes a [buildup → reset → re-entry] structure. This is universal.
2. The optimal buildup length (w) is determined by the ratio of buildup cost to reset cost, mediated by the decay/drift timescale.
3. k=7 is one specific value of w+1 that happens to be near-optimal when decay ≈ 0.08 per step and reset effectiveness ≈ 0.9. It is not universal.
4. Nested reset architecture (daily + weekly rhythm) does not rescue k=7 as the outer period; small inner cycles (w=2–3) dominate.
5. No single dimensionless ratio (gamma, rho, sigma) is stable across all decay rates. The optimal ratio shifts by 4× across the tested range.

**The right final statement:**

> The week's 7-day cycle is a specific discretization of a reset-gap grammar. The grammar — [accumulate → reset → re-enter] — is genuinely universal in bounded-agent systems. The integer 7 is a contingent realization of that grammar, near-optimal only in a narrow parameter band (low decay, reset-slot structure) and outperformed by shorter cycles (k=3–5) in most other regimes. The stable object is the grammar. The number is local and conditional.
