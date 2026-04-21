# funding/self-healing

**Track G — Dual-Lattice Self-Healing Systems**
**Primary funder pool:** AFRL · ONR · NASA JPL · NSF CISE RI · DARPA (autonomous systems)
**Status:** Pre-pitch. External `Dual-Lattice-Self-Healing` repo cloned; integration into `ck` pending. Partners with Branch B (`funding/tig-snowflake`) — detection + response loop.
**Branch accumulates to:** `master` (every commit cherry-picked) · **Rigor base:** `tig-synthesis` (the GitHub default branch)

---

## One-paragraph pitch

Autonomous systems — from spacecraft subsystems to distributed compute fabrics to industrial process controls — encounter damage, drift, and partial failure that they cannot always escalate to humans for repair. Self-healing architectures have been a research target for decades; most have either stayed theoretical (model-based control) or specialized (hardware-redundancy schemes with specific fault models). **The dual-lattice self-healing framework proposes a coherence-matching substrate drawn from the TIG Unity Kernel**: the system maintains a *current-state lattice* and a *reference lattice*, measures their coherence gap via the R-σ-Λ-H grammar, and applies partition-enumerated repair actions drawn from a finite vocabulary when the gap exceeds threshold. This branch packages the architecture and proposes a two-phase program — integration into the ck repo under provenance (Phase 1), then a specific autonomous-systems benchmark demonstration (Phase 2) — for an autonomous-systems funder.

## The core idea

A **dual lattice** means two coupled coherence fields: one representing the system's current state, one representing the system's target or reference state. When the two diverge beyond threshold, the gap is interpreted as damage / drift / compromise, and the system actuates repairs that reduce the gap. The "lattice" part refers to the discrete partition structure (analogous to the TSML / BHML cells in CK's substrate) that gives the repair actions a finite, enumerable vocabulary.

This is **not** a general-purpose self-repair framework. It is specifically the claim that dual-lattice coherence-matching is a tractable substrate for a class of autonomous repair problems where:
1. The system has a known reference.
2. The damage modes are partition-enumerable.
3. The repair actions are compositional over those partitions.

## Runnable artifacts

1. **`Dual-Lattice-Self-Healing` external repo** — cloned locally to `_brayden_repos/Dual-Lattice-Self-Healing/` during the 2026-04-20 Part 1 survey. Contains architectural documents and code sketches.
2. **TIG Unity Kernel simulator** — the same simulator underlying Branch A; runtime substrate for coherence-gap measurement.
3. **Operator vocabulary from TSML/BHML** — the 101-cell canonical-table substrate is a candidate source for the finite repair-action vocabulary.
4. **Coherence-gate reference** (`Gen12/.../ck_coherence_gate.py`) — the $T^* = 5/7$ threshold pattern used in CK, re-targetable as a gap-tolerance threshold in self-healing.

## Cross-branch relationship to SNOWFLAKE (Branch B)

Branch B (`funding/tig-snowflake`) funds the **detection** layer: a coherence-deficit in R-σ-Λ-H grammar precedes rule-based alarms. Branch G funds the **response** layer: given a detected deficit, apply partition-enumerated repair actions from a finite vocabulary to reduce the gap. Together they form a detection → response loop. The two branches can be pitched independently (different funder pools: security research vs. autonomous systems) or together (AFRL / DARPA cross-cutting).

## What's in this branch

Branch-specific funder-pitch files under [`Gen13/targets/funding_self_healing/`](Gen13/targets/funding_self_healing/):

- [`README.md`](Gen13/targets/funding_self_healing/README.md) — deep pitch document
- [`FUNDERS.md`](Gen13/targets/funding_self_healing/FUNDERS.md) — prioritized funder list (AFRL / ONR / NASA JPL / NSF CISE)
- [`ARTIFACTS.md`](Gen13/targets/funding_self_healing/ARTIFACTS.md) — external repo content + integration plan
- [`PITCH_DRAFT.md`](Gen13/targets/funding_self_healing/PITCH_DRAFT.md) — full pitch draft
- [`LIMITATIONS.md`](Gen13/targets/funding_self_healing/LIMITATIONS.md) — honest-scope items (specific-class of repair problems)
- [`STATUS.md`](Gen13/targets/funding_self_healing/STATUS.md) — readiness checklist

## The project this branch is a track of

Branch G of the 10-branch funding architecture. For the full project overview, see **`tig-synthesis`**:

→ https://github.com/TiredofSleep/ck/tree/tig-synthesis

## License

7Site Public Sovereignty License v1.0 — human use only, no commercial, no military, free forever. Full text in [`LICENSE`](LICENSE).

---

*Branch maintained as part of the 10-branch funding architecture. Commits here get cherry-picked to master per the trunk workflow. Branch-level changes do not propagate to `tig-synthesis` unless they are referee-ready.*
