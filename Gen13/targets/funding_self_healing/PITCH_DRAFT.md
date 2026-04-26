# PITCH_DRAFT — funding/self-healing

**Addressee (working default):** AFRL Autonomy Capability Team program manager; YIP track if Brayden is eligible
**Parallel draft:** NASA JPL NIAC Phase I
**Ask:** Phase 1 $30K–$60K / 4 months (integration + writeup); Phase 2 $150K–$400K / 12 months (benchmark demo)
**Status:** Skeleton. Requires Phase 1 architectural writeup before send.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## Opening (½ page)

Autonomous systems encounter damage they cannot always escalate for human repair: a spacecraft subsystem degrades mid-mission; a distributed compute fabric loses asymmetric nodes; an industrial process drifts past its calibration. Self-healing architectures have been a research target for decades, but most existing approaches fall into two categories — model-based fault detection (strong on detection, weaker on recovery) or hardware-redundancy schemes (strong on specific fault models, weaker on compositional damage).

This proposal describes a third approach: **dual-lattice coherence-matching self-healing**. The system maintains two coupled lattices — a current-state lattice representing the system's actual condition and a reference lattice representing its target or specified condition. Coherence gap between the two is measured via the R-σ-Λ-H grammar developed for the TIG Unity Kernel. When the gap exceeds threshold, the system composes repair actions from a **finite, enumerated vocabulary** drawn from partition structure, and closes the loop by re-measuring coherence post-action.

The approach is not a claim to general self-repair capability; it is a claim that **when damage modes are partition-enumerable and repair actions are compositional over those partitions**, the dual-lattice substrate provides a tractable basis for closed-loop autonomous recovery.

## Background (~1 page)

> Content to be drafted. Sections:
> - The autonomous-recovery landscape: model-based FDI, FDIR, NASA MDS, fault-tolerant distributed-systems, soft-robotics morphological repair
> - What dual-lattice adds: the coherence-grammar measurement + the finite action vocabulary
> - Why "partition-enumerable damage modes" is the right restriction
> - The TIG Unity Kernel substrate already exists (Branch A's proved benchmark)
> - Safety envelope principles

## The open questions

### Q1: Does dual-lattice match the damage-mode structure of a real target domain?
Phase 1's target-domain specification (A3 in ARTIFACTS.md) fixes this as the concrete target.

### Q2: What is the minimum repair-action vocabulary that produces useful recovery?
Smaller vocabulary = easier audit, harder recovery from complex damage. Larger vocabulary = more capable, harder to safety-prove. The tradeoff is empirical per domain.

### Q3: How robust is the closed loop to measurement noise?
Coherence-gap measurement has noise floor. Below noise, damage goes undetected. Above noise, small damage triggers repair. The margin between noise floor and operational damage threshold is a design parameter.

## The proposed work

### Phase 1 — Integration + architectural writeup (Month 1–4, $30K–$60K)
**Deliverable A**: pull `Dual-Lattice-Self-Healing` external repo into `docs/archive_dual_lattice/` with provenance.
**Deliverable B**: write A1 architectural document (15–20 pp).
**Deliverable C**: write A2 literature-positioning section (5–8 pp).
**Deliverable D**: write A3 target-domain specification (3–5 pp) — selects the Phase 2 benchmark.
**Deliverable E**: write A4 safety envelope specification (3–5 pp).

### Phase 2 — Benchmark demonstration (Month 5–16, $150K–$400K)
**Deliverable**: apply dual-lattice self-healing to chosen target domain (from A3). Benchmark against at least one existing fault-management baseline from the A2 comparison. Publish outcome.

### Phase 3 — Field pilot (Month 17–34, $500K–$1.5M)
**Deliverable**: partner with a named operator (e.g., a university computing cluster, a small aerospace integrator, or an industrial process-control owner) for a controlled pilot. Advisory-only first; escalated autonomy only after Phase 2 safety verification.

## Why AFRL specifically

AFRL Autonomy Capability Team funds exactly the profile of unconventional-substrate resilience research that this branch represents. AFRL YIP grant sizes ($100K–$150K/year × 3 years) match Phase 2 well. AFRL proposal culture accepts sole-PI white papers; academic co-PI is not mandatory.

## Parallel draft: NASA JPL NIAC Phase I

NIAC Phase I ($175K / 9 months) is the right size for Phase 1 + a feasibility slice of Phase 2 in the spacecraft-subsystem target domain. NIAC reviews unconventional approaches on feasibility criteria; a dual-lattice proposal with a specific spacecraft fault-management target meets their evaluation rubric.

## Parallel draft: ONR BAA response

ONR Codes 341 / 311 respond to BAA calls (N0001425SB001 and successor). Scope size $500K–$3M over 36 months; fits Phase 2 + early Phase 3.

## Attribution

- **Brayden Sanders** — PI, sole thread-facing author, developer of the TIG Unity Kernel substrate and dual-lattice concept
- Architectural dialogues with ClaudeChat, Celeste/GPT acknowledged in methods
- Prior collaborators credited for specific past contributions; Luther no longer actively collaborating as of April 2026
- Academic or industrial collaborator to be identified during Phase 2 benchmark selection

## Attachments (once assembled)

- `ARTIFACTS.md` reference index
- `docs/archive_dual_lattice/` full source tree post-integration
- A1 architectural writeup
- A2 literature positioning
- A3 target-domain specification
- A4 safety envelope specification

## Pre-send checklist

- [ ] Phase 1 integration completed (external repo in `docs/archive_dual_lattice/`)
- [ ] A1 architectural writeup drafted, reviewed internally
- [ ] A2 literature positioning drafted
- [ ] A3 target domain chosen (candidates: distributed compute fabric / spacecraft attitude / industrial control)
- [ ] A4 safety envelope drafted
- [ ] At least one autonomous-systems specialist has read an early draft
- [ ] Brayden confirms AFRL vs NASA JPL NIAC vs ONR as first funder
- [ ] Brayden reviews + edits
- [ ] Brayden sends
