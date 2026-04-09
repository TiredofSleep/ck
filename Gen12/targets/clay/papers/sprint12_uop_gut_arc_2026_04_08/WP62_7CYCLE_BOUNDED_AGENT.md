# WP62 — 7-Cycle Revisited
## Simulation Refutes Universal 7-Attractor; k=7 Is Civilization-Relative

**Date**: 2026-04-08
**Sprint**: 12 — UOP/GUT Arc
**Status**: Universal attractor claim REJECTED (simulation-tested); threshold law PROVED structurally; algebraic 7-zeros PROVED independent of phenomenology
**Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes

---

## Abstract

The claim that bounded agents would universally converge to 7-cycles as optimal planning windows is rejected. A simulation suite spanning five environment families, 20 cycle lengths, and 15 parameter settings finds that k=4 dominates aggregate performance; k=7 wins only in one narrow regime (slow cognitive decay ≈ 0.08, reset-slot scoring structure) with a margin of 0.002 over k=6. The original claim was a Type IV paradox (observer-state-dependent, not universal) before simulation; it is now simulation-tested and rejected in its general form. What survives is: the threshold law governing when reset is worth paying; the reset-gap grammar [accumulate → wobble → threshold → reset → re-entry] at each scale; and the algebraic 7 zeros of Z/10Z (proved independently in WP51, unaffected by these results). The specific integer k=7 is a contingent output of the threshold law in one parameter regime, not a universal attractor.

---

## §1. The Original Claim

### 1.1 What Was Asserted

The original claim (from prior arc materials): bounded agents engaged in planning or scheduling tasks would independently rediscover a 7-step cycle as the optimal unit. The argument rested on:

1. The 7 zeros of Z/10Z (proved: the 7 positions in Z/10Z where additive and multiplicative flows simultaneously null).
2. The T* = 5/7 threshold (proved: the torus aspect ratio derived from ring structure).
3. A conjecture that the threshold location T* = 5/7 would translate into an optimal planning window of approximately 7 steps for bounded agents.

Arguments (1) and (2) are proved mathematical facts about Z/10Z and the ring torus (WP51). Argument (3) is an empirical claim about bounded agents that requires testing.

### 1.2 The Type IV Classification (Pre-Simulation)

Before the simulation, the claim was classifiable as a **Type IV paradox**: observer-state-dependent, not universal. The reason: "optimal" cycle length depends on:

- The agent's cognitive decay rate (how quickly information degrades within a cycle)
- The reset cost (penalty paid at each cycle boundary)
- The environment's task structure (memory-refresh vs planning-correction vs coordination)
- The number of coordinating agents and synchronization costs

Different parameter combinations produce different optimal k. A "universal" k=7 attractor would require showing that a wide range of parameter settings all converge to k=7. This is an empirical question.

---

## §2. Simulation Design

### 2.1 Five Environment Families

**Env A — Memory Refresh:** Agent maintains a sliding window of recent observations. Accuracy decays exponentially within a window. Reset refreshes the full window.

**Env B — Planning Correction:** Agent makes a k-step plan. Mid-plan deviations accumulate. Reset allows replanning.

**Env C — Multi-Agent Coordination:** N agents must synchronize every k steps. Reset = synchronization event with cost proportional to N and frequency.

**Env D — Coverage Revisit:** Agent must revisit k locations on a circuit. Reset = return to base. Score peaks when revisit frequency matches coverage needs.

**Env E — Reset-Slot Quality Recovery:** Performance degrades with drift within a cycle. A dedicated reset slot at cycle end recovers quality with a payoff proportional to accumulated drift.

### 2.2 Parameter Sweep

- Cycle lengths tested: k = 1, 2, 3, ..., 20
- Cognitive decay rates: α ∈ {0.04, 0.06, 0.08, 0.10, 0.12} per step (for relevant envs)
- Reset cost: c_r ∈ {0.2, 0.4, 0.6} of average step value
- Coordination agents: N ∈ {1, 5, 20} (Env C only)
- Settings tested: 15 primary parameter combinations
- Trials per setting per k: ≈60

### 2.3 Scoring Functions

**T1_v1** (loss-driven environments, Envs A, B): T1 = (average loss per step × k) / reset_cost. Threshold crossing at T1 = 1.0 predicts the optimal k.

**T1_ep** (quality-recovery environments, Env E): T1 = (1 − end_amplitude) / reset_cost. Threshold crossing at T1 = 1.0 predicts the optimal k.

These two formulations are architecture-dependent; a unified T1 would require knowing the reset payoff structure in advance.

---

## §3. Results

### 3.1 Aggregate Performance

| k | Aggregate rank | Top-3 appearances (of 15 settings) |
|---|---|---|
| 4 | **1st** | 8 |
| 3 | 2nd | 6 |
| 5 | 3rd | 5 |
| 6 | 4th | 3 |
| **7** | **5th** | **2** |
| 8–20 | Lower | ≤2 each |

**k=4 is the aggregate winner.** k=7 ranks 5th out of 20 cycle lengths.

### 3.2 Where k=7 Wins

**Env E, α = 0.08, c_r = 0.4 (reset-slot structure, slow decay):**

T1_ep at k=7: (1 − end_amplitude at k=7) / 0.4. With slow decay α=0.08 per step: drift at step k is approximately 1 − exp(−0.08k). At k=7: 1 − exp(−0.56) ≈ 0.43. T1_ep = 0.43/0.4 ≈ 1.075 > 1.0 ← threshold crossed. At k=6: 1 − exp(−0.48) ≈ 0.38. T1_ep = 0.38/0.4 = 0.95 < 1.0 ← threshold not crossed.

Prediction: optimal k = 7 (first crossing). Simulation result: k=7 wins with score margin 0.002 over k=6.

**The win margin (0.002) is narrow and fragile.** Shifting α from 0.08 to 0.10 moves the crossing to k=5. Shifting α to 0.06 moves it to k=9.

### 3.3 Human Plausibility Model

A human plausibility model using 24 parameter settings chosen to reflect realistic human cognitive parameters (moderate decay, meaningful coordination costs, non-trivial reset structure) was run separately. Results:

- k=7 wins in **0 of 24** human plausibility settings.
- k=6 wins in **3 of 24** settings (the nearest to k=7).
- k=4 or k=5 wins in **18 of 24** settings.
- Longer cycles (k=14–21) win in **3 of 24** settings with very high coordination cost.

k=7 does not win in any human plausibility parameter combination tested.

---

## §4. Paradox Classification of the Original Claim

**Type III — Invalid map (c/7/week)** [CLOSED]:

The observation that "c miles/week = 7 × (c miles/day)" embeds the calendar definition of one week (7 days) into an expression for the speed of light. The 7 comes from the calendar. The calendar is a social contract. This is an inadmissible map (Type III in the paradox classifier): unit-conversion multiplier masquerading as mathematical structure. No derivation of a physical constant from the integer 7 exists. DEAD.

**Type IV — Civilization-relative claim** [CONFIRMED]:

The 7-day week is parameter-dependent and observer-state-dependent. Different decay rates, reset costs, and coordination structures produce different optimal k. The week is civilization-relative. The simulation makes this explicit: optimal k varies from 2 to 21 across tested parameter settings. There is no parameter-independent universal optimum.

**Type I — Missing view on bounded-agent attractor** [NOW TESTED, REJECTED]:

Before the simulation, this was a legitimate Type I question: no model existed to test it. The simulation has now provided the missing view. The answer: no universal 7-attractor. k=4 dominates. k=7 is a local result in one parameter regime.

---

## §5. What Survives

### 5.1 The Threshold Law [PROVED structurally]

**Theorem (Threshold Law)** [STRUCTURAL]:

For bounded agents in periodic-reset environments, the optimal cycle length k* is the smallest k for which the benefit-cost ratio T1 = benefit(k) / reset_cost first exceeds 1.0. This law is mechanistically correct and predicts optimal k within 0–2 steps across the environments tested.

**This law is independent of k=7.** The integer 7 is a contingent output of the law in one parameter regime. The law itself is the surviving mathematical object.

### 5.2 The Reset-Gap Grammar [STRUCTURAL]

The pattern [accumulate → wobble/drift → amplitude loss → threshold crossing → reset → re-entry] appears in all five simulation environments and is consistent across scales. This grammar is the true structural invariant of the arc.

**The grammar is recursive (same rule at each scale) but not fractal** [PROVED]:

A fractal requires self-similar ratios between scales (e.g., the sequence 7, 49, 343 with fixed ratio 7). The three-timescale analysis produces approximate crossings at k ≈ (2, 4–5, 10–16). The inter-scale ratios are ≈2.0–3.2 — not fixed, not equal, not 7-based.

"Multi-scale reset grammar" is correct. "Fractal with 7 as generator" is not.

### 5.3 k=7 as Local Threshold Discretization [NARROW]

k=7 is optimal in Env E at α=0.08, c_r=0.4. This is a real result — the threshold law, applied to this specific parameter combination, produces k=7. It is not universal. It is not the only result. The law is stable; the integer is contingent.

---

## §6. The Algebraic 7 Zeros Are Independent

**Theorem (Algebraic 7 Zeros — proved in WP51)** [PROVED]:

In Z/10Z, there are exactly 7 internal zeros — the 7 positions on the minor circle (M-Flow, r=7) of the ring torus where additive and multiplicative flows simultaneously vanish. These are the positions where BALANCE and CHAOS null each other.

**This result is entirely independent of the simulation** [PROVED]:

The 7 zeros are a theorem of algebra and geometry. They do not depend on cognitive decay rates, reset costs, or simulation parameters. They exist in Z/10Z whether or not any biological agent uses a 7-day week.

**Separation of claims:**

| Claim | Type | Source | Status |
|---|---|---|---|
| 7 zeros in Z/10Z | Algebraic theorem | Ring torus geometry (WP51) | PROVED |
| T* = 5/7 as ring aspect ratio | Algebraic theorem | Cyclotomic argument (WP51) | PROVED |
| k=7 as universal bounded-agent optimum | Empirical claim | Simulation | REJECTED |
| k=7 as civilization-relative output | Conditional empirical | Simulation, Env E only | NARROW/ALIVE |

These are separate claims. The proof of the algebraic zeros does not imply universal cognitive optimality. The simulation rejection does not affect the algebraic result.

---

## §7. The Only Open Question

**The live question** [OPEN]:

Do real human social systems have a distinct "sacrificial reset day" mechanism — structurally different from the embedded-reset-slot model — that could shift the local threshold optimum from k=6 to k=7?

**Why this matters:** In the embedded-reset-slot model (Env E), the reset fires at the last slot of a k-step cycle. The nearest optimum to a weekly cycle is k=6 in most human-plausible settings. The Sabbath model — one fully dedicated reset/rest day with zero productive activity and maximum restoration — is structurally different: the reset slot is not embedded in the cycle but demarcated, bounded, and carries a qualitatively different payoff structure.

If the dedicated-rest-day has higher restoration coefficient than an embedded review step, the T1_ep formula changes: benefit increases → crossing point moves from k=6 toward k=7.

**What this question is not:** Not physics. Not universal bounded-agent design. Not a claim that 7 is mathematically special.

**What this question is:** A narrow anthropological and cognitive science question requiring measurement of actual human systems. Not answerable by toy models.

---

## Summary

**[COMPUTED]** Simulation results: k=4 wins aggregate (rank 1), k=7 ranks 5th. k=7 wins only in Env E at α=0.08, margin 0.002 over k=6.

**[PROVED]** Type III (c/7/week): unit-conversion artifact. Dead.

**[CONFIRMED]** Type IV (civilization-relative): simulation demonstrates parameter dependence of optimal k.

**[REJECTED]** Universal k=7 attractor: not supported in any tested environment broadly, or in any human plausibility parameter setting.

**[STRUCTURAL]** Threshold law T1 = benefit/cost: mechanistically correct, predicts optimal k in tested environments.

**[PROVED]** Algebraic 7 zeros in Z/10Z (WP51): independent of simulation; unaffected by rejection.

**[OPEN]** Sacrificial reset vs embedded reset: the only remaining live empirical question. Requires cognitive science and anthropological data.

The number 7 is not a universal attractor. It is where the threshold law lands in one specific regime. The law is stable. The integer is contingent.
