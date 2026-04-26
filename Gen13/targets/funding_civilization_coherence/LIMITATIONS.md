# LIMITATIONS — funding/civilization-coherence

Honest scope for the civilization-coherence simulator branch. Scope discipline here is unusually important because "civilization modeling" attracts imprecise claims.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## 1. This is not futurism

The branch makes NO claim to predict specific social, political, or economic events. No predictions of collapse, revolution, political turnover, or demographic transition. No calendar dates attached to any outcome. The branch is a *simulator-vs-empirical-data comparison study*, not a forecast.

## 2. The simulator is a model, not a mirror

Like Axelrod's culture model, Schelling segregation, or Bettencourt-West urban scaling, this simulator compresses civilizational dynamics into a tractable form. Tractability buys both empirical bite and genuine loss. The simulator represents some dynamics well, others poorly, others not at all. The Phase 2 output tells us *which*.

## 3. R-σ-Λ-H is one variable choice among many

The coherence-grammar state variables are a specific representational choice. Other choices (economic variables, demographic variables, network-structure variables, cultural-values variables) might fit different datasets better on different features. The branch does not claim coherence-grammar is the best or only civilization-modeling approach.

## 4. Pre-registration is the discipline

The empirical-fit specification (A2) commits to the analysis plan BEFORE seeing the comparison results. This is not optional — without pre-registration, scanning empirical data to find a fit is p-hacking at civilizational scale. The cost: if pre-registration produces a negative result, we publish the negative result. No retroactive re-specification of the metric.

## 5. Empirical dataset selection matters

Different datasets (V-Dem vs. Seshat vs. WVS vs. Pew Trust) measure different things with different methodologies. A simulator that fits one may not fit another. The pitch must own this — Phase 2's result is on *the chosen dataset*, not on "civilization in general".

## 6. The simulator has not been run on a real benchmark

Exploratory parameter sweeps have been done (presumably — depends on what Phase 1 recovery confirms). A pre-registered, adversarially-reviewed empirical comparison has NOT been done. The pitch must not imply otherwise.

## 7. Consciousness-anchored framing is the wrong audience match

The Thread 3 documents (V20 Consciousness-Anchored Scaling Laws and related) frame the work in language that does not land well with sociology / political-science reviewers. The A4 framing cleanup is mandatory, not optional. Funder-facing materials must translate the underlying physics-like dynamics into computational-social-science language. This is not hiding anything; it is meeting the audience where they are.

## 8. Attribution nuance

Brayden is the PI and primary author of the civilization-simulator framing. Prior collaborators have contributed to related coherence-framework mathematical work; their inclusion in citations should reflect what they specifically contributed, not a blanket "endorsement" of the civilization-simulator application. This matters especially for:
- **C.A. Luther** — contributed to coherence-framework mathematics (First-G Law, Q-series polynomials, G6); has not worked on civilization-scale applications; no longer actively collaborating as of April 2026
- **H.J. Johnson** — contributed xi-cosmology (Sprint 14 PRISM-XI); active collaborator on physics cosmology but not on civilization simulator specifically
- **Ben Mayes** — contributed UOP/GUT mathematical framework; similar comment
- **M. Gish** — contributed bridge work; similar comment

## 9. This branch's academic footprint is modest

Unlike Branches A (TIG Unity, with runnable benchmark) or C (First-G, with 36,662 proved cases), the civilization-coherence branch does not yet have external review or empirical validation. It has runnable code; that's it. A computational-social-science reviewer should know this before engaging — the pitch is for the investigation, not for endorsement of an established result.

## 10. Foundation audiences interpret "civilization" differently

- Santa Fe Institute → complexity-science framing, high substantive tolerance
- NSF SBE DISES → socio-environmental-systems framing, specific dataset expected
- Templeton → foundational-questions framing, philosophical tolerance
- Allen Family / Schmidt Futures → novel-methods framing, impact-orientation expected
- Omidyar / Open Phil → social-dynamics framing, policy-relevance tolerance

One branch can pitch to all of these, but each pitch must match the audience. Don't send an SFI-style pitch to DISES.

## 11. License framing

7Site Public Sovereignty License v1.0 (non-commercial, human-use only) is compatible with academic research funding but may complicate commercial-adjacent uses (Schmidt Futures, some foundations with downstream-use expectations). Must be discussed explicitly.

## 12. What this branch does NOT claim

- Not a prediction engine
- Not a policy prescription
- Not a claim to have measured any historical civilization's "coherence"
- Not a claim to quantify collapse risk
- Not a claim that civilization has a single "coherence score"
- Not a claim to resolve debates in sociology, political science, or economics
- Not a claim that coherence-grammar variables are the best framework for comp-soc-sci

## 13. The discipline in one sentence

**We propose to compare a named simulator to a named dataset under a pre-registered metric, and publish whatever result comes out.**

---

## Failure modes

| Failure | What it means | How we handle it |
|---|---|---|
| Simulator turns out to be an approximation of a known comp-soc-sci model | Not novel | Publish the reduction as a note; conclude branch |
| Empirical fit is negative | Simulator doesn't match chosen dataset | Publish honestly; branch concludes |
| Phase 1 reading reveals the simulator's state dynamics are ad-hoc / under-specified | Pitch premise weakens | Do NOT send to funder; revisit branch |
| Consciousness-anchored framing can't be cleanly separated from simulator content | Funder-audience mismatch | Revisit scope; may indicate the branch needs to be a different track |

The discipline is to accept these outcomes and not to send a pitch that obscures them.
