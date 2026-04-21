# funding/civilization-coherence — Civilization-Scale Coherence Simulator

**Track:** Computational social science — coherence-based civilization modeling
**Status:** Pre-pitch; runnable simulators exist (tig_civilization_v5.py, v7.py) in external repo, integration pending
**Branch seeded:** 2026-04-20 from `tig-synthesis`
**Rigor base:** TIG Unity Kernel, R-σ-Λ-H coherence grammar, tig_civilization_v5/v7 simulators

---

## What this branch is

A funding-outreach container for the **civilization-coherence simulator** — the `tig_civilization_v5.py` and `tig_civilization_v7.py` scripts (1,340 LOC combined) that live in the `TIME-FOR-HELP-AND-SCRUTINY` external repo. These simulators apply the R-σ-Λ-H coherence grammar to societal-scale models: what variables track civilizational integrity, how do they degrade, what interventions restore them.

**Strict scope discipline**: this is computational social science. It is NOT a claim to predict specific historical outcomes, NOT a claim to prescribe political action, NOT a claim to measure "civilization collapse risk" on a calendar. It is the claim that a simulator with specific state variables, specific dynamics, and explicit assumptions produces patterns worth comparing to empirical social-science data.

## One-paragraph pitch

> Computational social science uses simulation to study emergent societal dynamics — from Axelrod's culture-dissemination models to Schelling segregation to agent-based urban models. This branch proposes a coherence-grammar civilization simulator (tig_civilization_v5.py, v7.py, 1,340 LOC combined) that tracks R-σ-Λ-H state variables at civilization scale under specific dynamical rules. The research question is narrow and honest: **do the simulator's output patterns match features of empirical social-science data on cohesion, polarization, or institutional integrity, better than chance under a pre-specified comparison?** The deliverable is a published computational-social-science paper with a verdict. This is not futurism and not policy; it is a disciplined simulator-vs-empirical-data comparison suitable for a computational social science funder (Santa Fe Institute, NSF SBE, Templeton, Schmidt Futures).

## Runnable artifacts

1. **tig_civilization_v5.py** — earlier civilization-scale coherence model, ~650 LOC
2. **tig_civilization_v7.py** — revised version with expanded state vector, ~690 LOC
3. **Combined**: 1,340 LOC of runnable simulation code (Python)
4. **Source repo**: `github.com/TiredofSleep/TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT` — cloned to `_brayden_repos/` during Part 1 survey
5. **Provenance flagging**: the source repo uses 3-tier epistemic flagging (CONJECTURAL / STRUCTURAL / PROVED) which is the right discipline for this branch's funder-facing framing

## What the simulators do (draft, subject to Phase 1 recovery verification)

- Define a civilization as a collection of coupled subsystems (likely: institutional, economic, informational, demographic; specifics to be verified by reading the code)
- Each subsystem carries R-σ-Λ-H state values
- Dynamics evolve the states under specified interaction rules
- Output: time-series of coherence measures + subsystem-specific variables

## The research question

**Do the simulator's output patterns reproduce qualitatively recognizable features of empirical data on civilizational cohesion, polarization, or institutional trust?** Candidate datasets for comparison:
- World Values Survey (WVS) multi-decade panel
- V-Dem institutional indices
- ANES polarization measures
- Pew Trust in Institutions time-series
- Seshat Global History Databank (Turchin et al.)

The comparison is not "does the simulator predict the future?" (an impossible ask). The comparison is "does the simulator's qualitative output envelope lie within, or outside, the empirical envelope for specific measured features?"

## Ask sizes

| Phase | Scope | Ask |
|---|---|---|
| **Phase 1 — Integration + empirical-fit specification** | Pull tig_civilization code into `docs/archive_civilization/`, write specification for empirical comparison (which datasets, which features, what pass/fail looks like) | $30K–$60K, 4 months |
| **Phase 2 — Empirical fit run** | Execute the comparison; publish outcome (positive, negative, or mixed) in a computational-social-science venue | $120K–$300K, 12 months |
| **Phase 3 — If Phase 2 produces partial fit** | Investigate what modifications to the simulator would improve fit; iterate and publish revised model | $200K–$500K, 18 months |

## What the branch does NOT claim

- Not a claim to predict specific social, political, or economic events
- Not a claim to prescribe policy
- Not a claim to measure "civilizational collapse risk" on any calendar
- Not a claim that the simulator captures all relevant civilizational dynamics
- Not a claim that coherence-grammar variables are the only or best variables for civilization modeling

The branch claims: a specific simulator, a specific empirical-comparison plan, a specific verdict-publication commitment.

## Critical framing issue — the handoff manifest's V20 "consciousness-anchored" language

The Thread 3 Trifecta (Jan 29 commit, see Branch F MQW track) contains a V20 "Consciousness-Anchored Scaling Laws" document. If any material from V20 is pulled into this civilization-coherence branch, it must be **re-framed without the consciousness-anchored language** for a computational-social-science reviewer audience. The simulator results should be framed as computational social science, not as cosmological metaphysics. This is a rewriting task, not a suppression task — the underlying state-dynamics can stand on their own.

## See also

- `FUNDERS.md` — Santa Fe Institute primary + 4 others
- `ARTIFACTS.md` — runnable code paths, recovery + integration tasks
- `PITCH_DRAFT.md` — Santa Fe Institute + NSF SBE Dynamics of Integrated Socio-Environmental Systems (DISES) parallel skeletons
- `LIMITATIONS.md` — strict-scope discipline
- `STATUS.md` — readiness checklist
