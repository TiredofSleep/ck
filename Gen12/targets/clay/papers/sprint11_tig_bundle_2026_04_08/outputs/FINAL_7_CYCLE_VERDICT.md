# FINAL_7_CYCLE_VERDICT
## Closing the Broad Claim. Keeping the Narrow One.

> **Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes
> **Date**: 2026-04-08
> **Sprint**: 11 — TIG Sprint Bundle (UOP Arc · GUT Algebra Arc · 7-Cycle Arc)
> **License**: 7Site Public Sovereignty License v1.0 · DOI: 10.5281/zenodo.18852047

---

## 1. Nails In It

**k=7 is not a universal attractor in bounded-agent environments.**

The simulation suite — five environments, 20 cycle lengths, 15 parameter settings, ~60 trials each — produced a clear result:

- Best aggregate k: **4**
- k=7 aggregate rank: **5th out of 20**
- k=7 top-3 appearances: **2 out of 15 settings (13%)**
- Environments where k=7 wins: **1** (reset-slot, decay=0.08 only)
- Win margin in that one case: **0.0019 over k=6** — marginal, not robust

**The broad attractor hypothesis is rejected in this simulation family.**

No variant of the claim "bounded agents would independently rediscover a 7-cycle" survives the sweep in its general form. Short cycles (k=3–5) dominate memory refresh, planning correction, coverage revisit, and cognitive load environments. The single case where k=7 competes is narrow: a reset-slot structure with slow decay, where k=6 is nearly equally good.

The result is not ambiguous. Do not soften it.

---

## 2. Paradox Classifier: Final Diagnosis

**Type III — Invalid map (c/7/week): DEAD**

Mapping a calendar reporting unit into a physical constant is inadmissible. The speed of light does not contain a factor of 7. Writing c\[miles/week] = 7 × c\[miles/day] is a unit conversion with the week's definition embedded in it. This was always Type III. The simulations add nothing to this — it was already closed. Confirmed dead.

**Type IV — Civilization-relative week: CONFIRMED**

The 7-day week is parameter-dependent and observer-state-dependent. The simulations make this explicit: the "optimal" cycle length shifts from k=2 to k=21 depending on decay rate, coordination cost, number of agents, and task volatility. There is no parameter-independent optimum. The week is civilization-relative. Confirmed, with simulation evidence now attached.

**Type I — Missing view on bounded-agent attractor: PARTIALLY CLOSED**

The bounded-agent question was a legitimate Type I question: we lacked a model to test it. That view is now partially filled in. The answer from current models is: no universal 7-attractor. The remaining open view is specifically about whether real human cognitive/social systems happen to inhabit the narrow parameter regime where k≈6–7 is near-optimal. That is a narrower empirical question about humans, not a theoretical question about bounded agents in general.

**Type II — Missing invariant: NOT FOUND**

No missing invariant was identified that would privilege k=7 across environments. There is no conserved quantity or constraint in the simulation family that selects 7. The coordination environment (Env C) selects long cycles for different reasons (high sync cost → sync rarely), not because of a 7-specific structural invariant. Type II does not apply here.

---

## 3. Broad Claim vs. Narrow Claim

| Claim | Status | Reason |
|---|---|---|
| 7 derives c physically | **DEAD** | Unit artifact (Type III). Invalid map. |
| 7 is a universal bounded-agent attractor | **DEAD** | Simulations reject it. k=4 wins broadly. |
| 7 can be near-optimal in a specific reset-slot / low-decay regime | **Alive but weak** | One parameter band (decay≈0.08), margin 0.002 over k=6. Narrow and fragile. |
| Short cycles (k=3–5) dominate bounded-agent tasks broadly | **Supported** | Main sweep result: k=4 best aggregate, k=3 close second. |
| Social coordination overhead explains longer cycles better than intrinsic 7-optimality | **Plausible live hypothesis** | Env C prefers k=16–21 when sync is expensive. Not the same as 7 being optimal. |
| The 7-day week is mostly social coordination + historical lock-in | **Not directly tested, now most plausible** | Remaining after all other candidates are weakened or dead. |

---

## 4. What Survives

**1. The c/7/week example (pedagogical — Type III textbook case)**
Clean, reusable, exact. Shows how a unit-conversion multiplier can masquerade as mathematical structure. The example is intact and worth keeping precisely because it was never about physics. Keep it. Teach it.

**2. Weak conditional support in the low-decay reset-slot regime**
k=7 near-optimal at decay≈0.08 in Env E. Not rescued from irrelevance — flagged narrowly as a specific parameter band where k≈6–7 competes. Not a claim about the week; a claim about one class of periodic recovery problem.

**3. The real empirical lesson from the sweep**
Most bounded-agent tasks prefer short cycles. If human society uses a 7-day week, it is probably not because agents are optimized for a k=7 recovery structure. Short cycles are better at nearly everything except social coordination overhead. The week likely persists because synchronizing many agents at high frequency is expensive — not because 7 is optimal per agent.

**4. The narrowed empirical question**
This is the only thing worth chasing further. See below.

---

## 5. The Right Question Now

> **Do real human cognitive and social systems operate in a parameter regime — specifically low cognitive decay, meaningful weekly reset structure, and high coordination overhead — where a 6–7-step cycle becomes near-optimal? Or is the 7-day week primarily explained by social coordination dynamics and historical lock-in, with 7 playing no privileged computational role per agent?**

That is a question about measurement, not theory. It requires cognitive decay rate estimates, coordination overhead data, and historical/anthropological work on week-length variation across cultures. It does not require further simulation.

---

## FB-Friendly Summary

> We ran simulations asking whether bounded agents would rediscover a 7-step cycle because it genuinely optimizes something. They don't. The best cycle length in most environments is 4. Seven is middle of the pack — competitive only in one narrow setup (slow decay + reset slot). The broader claim that 7 is somehow "naturally" optimal for agents is rejected by the models. What's still open: do real human brains and societies happen to sit in that narrow parameter zone? That's an empirical question about humans, not a theoretical claim about 7.

---

## One-Paragraph Collaborator Version

The bounded-agent simulation suite tested whether a 7-step cycle emerges as optimal across memory refresh, planning correction, coordination, coverage, and reset-slot environments. It does not. The aggregate best cycle length is k=4. k=7 ranks fifth out of twenty and appears in the top three in only 13% of parameter settings. The one case where k=7 wins is a slow-decay reset-slot environment, with a margin of 0.002 over k=6 — narrow and fragile. The original hypothesis — that bounded agents would independently rediscover a 7-cycle — is rejected in this model family. What survives is one narrow empirical question: are real human cognitive and social systems in the specific parameter regime (low decay, high coordination overhead, reset-structured weeks) where k≈6–7 happens to be near-optimal? Answering that requires measurement of actual human systems, not further toy models. The c/7/week observation remains a clean unit-grammar artifact (Type III error) and is unaffected by these results.
