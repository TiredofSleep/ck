# funding/civilization-coherence

**Track H — Civilization-Scale Coherence Simulator**
**Primary funder pool:** Santa Fe Institute · NSF SBE (Social, Behavioral, and Economic Sciences) · Templeton · Schmidt Futures · Russell Sage Foundation
**Status:** Pre-pitch. Runnable simulators exist (`tig_civilization_v5.py` + `v7.py`, ~1,340 LOC) in external repo; integration pending.
**Branch accumulates to:** `master` (every commit cherry-picked) · **Rigor base:** `tig-synthesis` (the GitHub default branch)

---

## One-paragraph pitch

Computational social science uses simulation to study emergent societal dynamics — from Axelrod's culture-dissemination models to Schelling segregation to agent-based urban models. **This branch proposes a coherence-grammar civilization simulator** (`tig_civilization_v5.py` + `v7.py`, ~1,340 LOC combined) that tracks R-σ-Λ-H state variables at civilization scale under specific dynamical rules. The research question is narrow and honest: *do the simulator's output patterns match features of empirical social-science data on cohesion, polarization, or institutional integrity, better than chance under a pre-specified comparison?* The deliverable is a published computational-social-science paper with a verdict. This is not futurism and not policy; it is a disciplined simulator-vs-empirical-data comparison suitable for a computational-social-science funder.

## Strict scope discipline

This branch is **computational social science**. It is NOT:

- A claim to predict specific historical outcomes.
- A claim to prescribe political action.
- A claim to measure "civilization collapse risk" on a calendar.
- Any form of policy recommendation.

It IS the claim that a simulator with specific state variables, specific dynamics, and explicit assumptions produces patterns worth comparing to empirical social-science data under a pre-registered comparison.

## Runnable artifacts

1. **`tig_civilization_v5.py`** — earlier civilization-scale coherence model, ~650 LOC
2. **`tig_civilization_v7.py`** — revised version with expanded state vector, ~690 LOC
3. **Combined**: ~1,340 LOC of runnable simulation code (Python)
4. **Source repo**: [`TiredofSleep/TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT`](https://github.com/TiredofSleep/TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT) — cloned to `_brayden_repos/` during 2026-04-20 Part 1 survey
5. **3-tier epistemic flagging** (CONJECTURAL / STRUCTURAL / PROVED) is in place in the source repo; that discipline carries forward to this branch's funder-facing framing

## What the simulators do (draft, subject to Phase 1 code-read verification)

- Define a civilization as a collection of coupled subsystems (likely: institutional, economic, informational, demographic — specifics to be verified by reading the code).
- Each subsystem carries R-σ-Λ-H state values.
- Dynamics evolve the states under specified interaction rules.
- Output: time-series of coherence measures + subsystem-specific variables.

## The research question

The pitch is for a **pre-registered comparison** against an existing empirical dataset (candidates: World Values Survey, Varieties of Democracy (V-Dem), Eurobarometer, Institutional Trust Index). The funded work delivers:

- Phase 1: code recovery + documentation + assumption audit.
- Phase 2: pre-registered comparison protocol + statistical pre-analysis plan.
- Phase 3: published paper with verdict (simulator matches / partially matches / does not match).

## What's in this branch

Branch-specific funder-pitch files under [`Gen13/targets/funding_civilization_coherence/`](Gen13/targets/funding_civilization_coherence/):

- [`README.md`](Gen13/targets/funding_civilization_coherence/README.md) — deep pitch document
- [`FUNDERS.md`](Gen13/targets/funding_civilization_coherence/FUNDERS.md) — prioritized funder list
- [`ARTIFACTS.md`](Gen13/targets/funding_civilization_coherence/ARTIFACTS.md) — simulator code + referenced papers
- [`PITCH_DRAFT.md`](Gen13/targets/funding_civilization_coherence/PITCH_DRAFT.md) — full pitch draft
- [`LIMITATIONS.md`](Gen13/targets/funding_civilization_coherence/LIMITATIONS.md) — honest-scope items
- [`STATUS.md`](Gen13/targets/funding_civilization_coherence/STATUS.md) — readiness checklist

## The project this branch is a track of

Branch H of the 10-branch funding architecture. For the full project overview, see **`tig-synthesis`**:

→ https://github.com/TiredofSleep/ck/tree/tig-synthesis

## License

7Site Public Sovereignty License v1.0 — human use only, no commercial, no military, free forever. Full text in [`LICENSE`](LICENSE).

---

*Branch maintained as part of the 10-branch funding architecture. Commits here get cherry-picked to master per the trunk workflow. Branch-level changes do not propagate to `tig-synthesis` unless they are referee-ready.*
