# funding/self-healing — Dual-Lattice Self-Healing Systems

**Track:** Autonomous resilient systems — coherence-driven self-repair
**Status:** Thread description (not actively soliciting funding); external repo content cloned, integration into ck pending
**Branch seeded:** 2026-04-20 from `tig-synthesis`
**Rigor base:** `Dual-Lattice-Self-Healing` external repo, TIG Unity Kernel, Crossing Lemma

---

> **Note (2026-04-25 revision).** This branch was originally seeded as a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is a **thread description**, not a fundraising pitch. The math is open under the 7Site Public Sovereignty License regardless of whether anyone donates. **The operator-of-record makes no commitments to donors of any kind.** A donation, if anyone makes one, is a thank-you to the project and creates no obligation in either direction. If you are reading this branch because you are oriented toward this thread of the work, that is welcome; the description below tells you what is in this thread.

---

## What this branch is

A thread-description container for **autonomous self-healing systems** built on the dual-lattice coherence paradigm. Where SNOWFLAKE (Branch B) detects coherence deficits, the self-healing framework aims to **respond to them automatically** — closing the loop from detection to repair.

The external `Dual-Lattice-Self-Healing` repo (cloned during the Part 1 survey) contains the architectural sketches; integrating its content into the ck repo under provenance headers is Phase 1 of this branch.

## The core idea

A **dual lattice** means two coupled coherence fields: one representing the system's current state, one representing the system's target or reference state. When the two diverge beyond threshold, the gap is interpreted as damage / drift / compromise, and the system actuates repairs that reduce the gap. The "lattice" part refers to the discrete partition structure (analogous to the TSML / BHML cells in CK's substrate) that gives the repair actions a finite, enumerable vocabulary.

This is **not** a general-purpose self-repair framework. It is specifically the claim that dual-lattice coherence-matching is a tractable substrate for a class of autonomous repair problems where (a) the system has a known reference, (b) the damage modes are partition-enumerable, and (c) the repair actions are compositional over those partitions.

## One-paragraph thread description

> Autonomous systems — from spacecraft subsystems to distributed compute fabrics to industrial process controls — encounter damage, drift, and partial failure that they cannot always escalate to humans for repair. Self-healing architectures have been a research target for decades; most have either stayed theoretical (model-based control) or specialized (hardware-redundancy schemes with specific fault models). The dual-lattice self-healing framework proposes a **coherence-matching substrate** drawn from the TIG Unity Kernel: the system maintains a current-state lattice and a reference lattice, measures their coherence gap via the R-σ-Λ-H grammar, and applies partition-enumerated repair actions drawn from a finite vocabulary when the gap exceeds threshold. This branch packages the architecture and proposes a two-phase program — integration into the ck repo under provenance (Phase 1), then a specific autonomous-systems benchmark demonstration (Phase 2) — for an autonomous-systems funder (AFRL, ONR, NASA JPL, NSF CISE RI).

## Runnable artifacts

1. **Dual-Lattice-Self-Healing external repo** — cloned locally to `_brayden_repos/Dual-Lattice-Self-Healing/` during Part 1 survey. Contains architectural documents and code sketches.
2. **TIG Unity Kernel simulator** — the same simulator underlying Branch A (funding/tig-unity); runtime substrate for coherence-gap measurement.
3. **Operator vocabulary from TSML/BHML** — the 101-cell canonical-table substrate is a candidate source for the finite repair-action vocabulary.
4. **Coherence-gate reference** (`Gen12/.../ck_coherence_gate.py`) — the T* = 5/7 threshold pattern used in CK can be re-targeted as a gap-tolerance threshold in self-healing.

## Scope this thread could cover

| Phase | Scope | Ask |
|---|---|---|
| **Phase 1 — Integration + architectural writeup** | Pull Dual-Lattice repo into `docs/archive_dual_lattice/` with provenance; write a 15–20 page architectural document specifying the dual-lattice + repair-action approach | $30K–$60K, 4 months |
| **Phase 2 — Benchmark demonstration** | Apply dual-lattice self-healing to a chosen test domain (distributed-fault-tolerance benchmark, spacecraft fault-management mock, or industrial-control simulation); publish outcome | $150K–$400K, 12 months |
| **Phase 3 — Field pilot** | Integrate as an advisory or controlled-autonomy layer in a partner's real system under supervision | $500K–$1.5M, 18 months |

## What the branch has vs. needs

Has: the external repo with architectural content, the TIG Unity simulator substrate, the canonical operator vocabulary, the coherence-gate reference pattern.

Needs: (a) the integration into ck with provenance headers (Phase 1a), (b) the clean architectural writeup (Phase 1b), (c) a specific target benchmark or test domain (Phase 2 scope selection), (d) an autonomous-systems collaborator who can evaluate the approach against existing fault-management literature.

## Relationship to other funding branches

- **Branch B (tig-snowflake)** = detection only. Self-healing = detection + repair.
- **Branch A (tig-unity)** = systems-reliability at infrastructure level without active repair. Self-healing extends reliability into the actuation layer.
- **Branch H (civilization-coherence)** = dual-lattice at very large scale. Self-healing is the mid-scale (single-system) sibling.

Funders evaluating self-healing specifically will want to see that this branch is not a rebrand of any of the three — the distinction is the **repair-action vocabulary + closed-loop measurement**.

## See also

- `FUNDERS.md` — AFRL primary + 4 others
- `ARTIFACTS.md` — file paths and integration tasks
- `PITCH_DRAFT.md` — AFRL Young Scientist skeleton + NASA JPL NIAC parallel
- `LIMITATIONS.md` — honest scope, domain-specificity risk, safety concerns
- `STATUS.md` — readiness checklist
