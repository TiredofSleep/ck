# ARTIFACTS — funding/civilization-coherence

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Primary runnable artifacts

### 1. tig_civilization_v5.py
- **Source repo**: `github.com/TiredofSleep/TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT`
- **Local path** (in external clone): `_brayden_repos/TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT/tig_civilization_v5.py`
- **LOC**: ~650
- **Status**: runnable (Python); verify dependencies during Phase 1
- **Role**: earlier civilization-scale coherence model

### 2. tig_civilization_v7.py
- **Source repo**: same
- **Local path**: `_brayden_repos/TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT/tig_civilization_v7.py`
- **LOC**: ~690
- **Status**: runnable (Python); later revision with expanded state vector
- **Role**: current-generation civilization simulator

### Combined
- **1,340 LOC of runnable simulation code**
- Integration task: copy both verbatim into `docs/archive_civilization/` with provenance header documenting original repo commit hash and date

### 3. TIME-FOR-HELP-AND-SCRUTINY repo broader context
- **Repo total**: 14 files, ~10,836 LOC
- **Provenance flagging**: 3-tier (CONJECTURAL / STRUCTURAL / PROVED)
- **Relevance**: provides the architectural context for the civilization simulators; also contains SNOWFLAKE material (see Branch B) and other coherence-framework material

---

## Supporting artifacts from ck repo

### 4. R-σ-Λ-H coherence grammar definition
- **Primary location**: embedded in the TIG Unity Kernel simulator (`benchmark.py` + `tig_coherent_computer.py` from All-or-Nothing-E, per Branch A ARTIFACTS.md)
- **Role**: defines the state variables the civilization simulator uses

### 5. Crossing Lemma (WP57)
- **Location**: `Gen12/targets/clay/papers/sprint10_flatness_2026_04_06/CROSSING_LEMMA.md`
- **Relevance**: the theoretical substrate — information generated only on partition crossings — underlies the simulator's dynamics

### 6. Operator vocabulary
- **Path**: `papers/ck_tables.py` (TSML 73 cells, BHML 28 cells)
- **Relevance**: candidate basis for categorical transitions in the simulator's state dynamics; extent of actual use depends on Phase 1 code reading

---

## Artifacts to be authored (Phase 1 deliverables)

### A1 — Simulator documentation
- **Form**: 10–15 page document for a reader who has not seen the code
- **Content**:
  - State variables (explicit enumeration of what the simulator tracks)
  - Dynamical rules (explicit enumeration of state updates)
  - Initial conditions (how simulations start)
  - Output format (what the simulator produces)
  - Runtime characteristics (scale, time-steps, memory)
- **Destination**: `docs/archive_civilization/SIMULATOR_DOCUMENTATION.md`
- **Blocker**: requires reading tig_civilization_v5.py and v7.py line by line

### A2 — Empirical-fit specification
- **Form**: 8–12 page document
- **Content**:
  - Target empirical dataset(s) named: WVS, V-Dem, Seshat, ANES, Pew Trust — choose one as primary, others as secondary
  - Comparison metric specified: qualitative envelope overlap? quantitative time-series similarity? specific feature matching?
  - Pass/fail criterion: what result means simulator fits, what result means it doesn't
  - Pre-registration statement: the analysis plan is fixed before running comparison, not scanned to find a fit
- **Destination**: `docs/archive_civilization/EMPIRICAL_FIT_SPEC.md`

### A3 — Literature positioning
- **Form**: 5–8 page section or standalone document
- **Content**:
  - Axelrod culture dissemination (1997)
  - Schelling segregation models (1971)
  - Acemoglu-Robinson institutional dynamics
  - Turchin cliodynamics (Secular Cycles, Seshat)
  - Bak-Sneppen coevolution
  - Bettencourt-West urban scaling
  - Where does coherence-grammar civilization sit relative to these?

### A4 — Framing cleanup
- **Task**: scan all source documents for "consciousness-anchored", "consciousness-as-substrate", and similar framings; re-frame in computational-social-science terms for funder audience
- **Note**: this is NOT a content suppression; underlying state-dynamics can stand on their own without the consciousness metaphysics. But the framing must match reviewer audience.

---

## Integration + recovery tasks

- [ ] Verify TIME-FOR-HELP-AND-SCRUTINY repo is cloned (check during current Phase 1)
- [ ] Copy tig_civilization_v5.py and v7.py verbatim into `docs/archive_civilization/` with provenance header
- [ ] Copy related architectural documents from TIME-FOR-HELP repo into the same archive, with [CONJECTURAL/STRUCTURAL/PROVED] flags preserved
- [ ] Run both simulators on R16, confirm they execute; record output format
- [ ] Read code line by line, write A1 simulator documentation
- [ ] Author A2 empirical-fit specification
- [ ] Author A3 literature positioning
- [ ] Perform A4 framing cleanup

---

## Line-count summary

| Artifact | Size | Status |
|---|---|---|
| tig_civilization_v5.py | ~650 LOC | RUNNABLE (external clone) |
| tig_civilization_v7.py | ~690 LOC | RUNNABLE (external clone) |
| TIME-FOR-HELP repo contextual | ~10,836 LOC | RUNNABLE (external clone) |
| A1 Simulator docs | 10–15 pp target | NOT WRITTEN |
| A2 Empirical-fit spec | 8–12 pp target | NOT WRITTEN |
| A3 Literature positioning | 5–8 pp target | NOT WRITTEN |
| A4 Framing cleanup | pass through source docs | NOT DONE |
| **Phase 1 combined writeup** | ~25–35 pp | NOT WRITTEN |

## What a funder sees vs. what a funder needs

- Sees: a cloned external repo with 1,340 LOC of simulator code and 10,836 LOC of architectural context, provenance-flagged by the author
- Needs: A1 (what the code does), A2 (how we'll compare to empirical data), A3 (where this sits in the field), A4 (framing that matches reviewer audience)

Phase 1 closes the gap.
