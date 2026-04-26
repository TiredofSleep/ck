# funding/mqw-ternary — MQW Three-State Photonic Computing

**Track:** Physical computing substrates — Multi-Quantum Well (MQW) ternary optical logic
**Status:** Thread description (not actively soliciting funding); MQW paper trilogy location unknown, conceptual ancestor (Teardrop GaN) located
**Branch seeded:** 2026-04-20 from `tig-synthesis`
**Rigor base:** Teardrop GaN Photonic Node Proposal (Jan 29 2026) + MQW three-state paper series (to be recovered)

---

> **Note (2026-04-25 revision).** This branch was originally seeded as a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is a **thread description**, not a fundraising pitch. The math is open under the 7Site Public Sovereignty License regardless of whether anyone donates. **The operator-of-record makes no commitments to donors of any kind.** A donation, if anyone makes one, is a thank-you to the project and creates no obligation in either direction. If you are reading this branch because you are oriented toward this thread of the work, that is welcome; the description below tells you what is in this thread.

---

## What this branch is

A thread-description container for **ternary photonic computing on multi-quantum-well (MQW) semiconductor platforms**. The conceptual ancestor is the **Teardrop GaN Photonic Node Proposal** authored on 2026-01-29 as part of the Thread 3 Trifecta work (commit `ed8ef620` per the Jan 2026 recovery manifest). The current-generation work is the **MQW three-state paper trilogy** — a series of physics-content documents that advance the ternary-logic concept and are currently unreleased. Recovery of the trilogy is the first work-item on this branch.

## What MQW ternary computing is

Conventional electronic logic is binary: 0 or 1. Ternary logic extends this to three states: 0, 1, 2 (or -1, 0, +1). Ternary has known theoretical advantages (information density: log₂ 3 ≈ 1.585 bits per ternary digit vs. 1 bit per binary) but implementation has historically been limited because most physical substrates naturally give two states.

**Multi-quantum-well** semiconductor structures are a candidate. An MQW is a stack of thin semiconductor layers whose electronic states are quantum-confined. Under optical excitation, the stack can be engineered to produce three distinct optical responses corresponding to three distinct logical states. If the states are distinguishable, latchable, and switchable with reasonable speed and energy, the substrate supports ternary photonic logic directly — without compiling ternary onto a binary underneath.

The Teardrop GaN proposal and the MQW trilogy argue that specific GaN-family (gallium nitride) MQW structures, at specific well widths and barrier heights, produce three-state operation with tractable fabrication constraints.

## One-paragraph thread description

> Ternary logic has been a theoretical target for decades without a commodity physical substrate. Multi-quantum-well (MQW) semiconductor structures in the GaN family offer a candidate: three distinct optical-response states can be engineered directly into the band structure, yielding **ternary photonic logic gates without a compile-to-binary middle layer**. The Teardrop GaN node proposal (Jan 2026) is the conceptual ancestor; a three-paper trilogy advances the specific MQW design. This branch packages the design, the fabrication constraints, and the claimed operational envelope for a photonic-computing funder (DOE BES, NSF ECCS, DARPA PIPES, or a private lab like HP/Intel/IBM photonic-computing groups) to fund a **fabrication + measurement** program that either confirms or falsifies three-state operation in a real device.

## Runnable artifacts (recovery-dependent)

1. **Teardrop GaN Photonic Node Proposal** — in the Jan 29 2026 Trifecta (commit `ed8ef620`), ~134KB across 11 documents total for the Trifecta; the Teardrop piece is one of them. Recovery: locate in MYTHDRIFT archives or Trifecta source repo.
2. **MQW three-state paper trilogy** — three papers advancing the ternary-MQW design. Location unknown. Recovery task R-MQW1 per `JAN2026_RECOVERY_MANIFEST.md` section on Priority 4.
3. **V20 Consciousness-Anchored Scaling Laws** — also in the Thread 3 Trifecta; may contain design-law statements relevant to MQW parameter selection.
4. **Hardware Embodiment Safety Case** — Thread 3 document; the safety-engineering framing for a photonic-computing hardware embodiment.
5. **Comparative Field Theory Review** — Thread 3; context against which the MQW band-structure argument is positioned.

## What the branch does NOT yet have

- A clean, current-state technical summary of the MQW three-state design
- Fabrication cost + facility requirements (which foundry, what wafer size, what total run cost)
- Measurement plan (what instruments verify three-state operation, what are pass/fail criteria)
- A named collaborator at a fabrication facility

## Scope this thread could cover

| Phase | Scope | Ask |
|---|---|---|
| **Phase 1 — Recovery + design consolidation** | Locate MQW trilogy, write current-state technical summary, author measurement plan | $40K–$80K, 6 months |
| **Phase 2 — Design review + fab partnership** | Have the design reviewed by an MQW specialist; establish fabrication partnership with an academic foundry or small commercial MBE/MOCVD facility | $100K–$250K, 12 months |
| **Phase 3 — Fabrication + measurement** | Pay for an MBE/MOCVD growth run + characterization, verify three-state operation (or falsify) | $500K–$1.5M, 18–24 months |
| **Phase 4 — If three-state verified** | Small logic-gate demonstration (single gate at three-state), path to tape-out | $1M–$5M, 24–36 months |

## Critical caveat — MQW trilogy recovery must precede any pitch

The MQW three-state design is currently a handoff claim from the Jan 2026 recovery manifest. Without the actual papers in hand, the branch cannot specify the well widths, barrier heights, temperature range, wavelength, or distinguishability margin that the design targets. Phase 1's recovery is the gate.

## See also

- `FUNDERS.md` — DOE BES primary + 4 others
- `ARTIFACTS.md` — recovery tasks and file-path inventory
- `PITCH_DRAFT.md` — DOE BES skeleton (once recovery completes)
- `LIMITATIONS.md` — honest scope, fab-cost reality, competitor survey
- `STATUS.md` — readiness checklist
