# LIMITATIONS — funding/self-healing

Honest scope for the dual-lattice self-healing branch. Autonomous-systems funders will weight safety and falsifiability heavily; this file must be strict with itself.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## 1. Dual-lattice self-healing is not a general self-repair framework

The approach works when damage modes are **partition-enumerable** and repair actions are **compositional over those partitions**. It does not work on damage modes that fall outside the enumeration (novel failure modes) or on systems where actions cannot be decomposed into a finite vocabulary. This restriction is a feature — it is why the approach is tractable — but it is also a genuine limit.

## 2. No benchmark has been run

The architectural writeup exists (in the external repo); applied benchmarks have not. Until Phase 2 delivers a published benchmark result, any claim about self-healing effectiveness is theoretical.

## 3. Closed-loop autonomous actuation is a safety-critical capability

A self-healing system that acts on its own environment can **make damage worse**. Oscillatory repair (detection triggers repair triggers detection triggers opposite repair), cascading compensation (repair in one partition triggers damage in another), and misdiagnosis (wrong damage class → wrong action) are all real failure modes. The A4 safety envelope specification is not a checkbox; it is a first-class design constraint.

## 4. Measurement noise vs. damage threshold gap

The coherence-gap signal must be large enough to distinguish damage from noise. In low-noise, low-damage regimes, this is fine. In high-noise environments or for subtle damage modes, the self-healing signal may be masked by noise. The noise-margin analysis must be domain-specific.

## 5. Reference-lattice specification

The approach requires a reference lattice. If the reference is mis-specified, the system "heals" itself toward the wrong target. Mis-specified reference = worse than no self-healing. This is a genuine responsibility for the PI designing the system for a specific domain.

## 6. Compositional repair vocabulary is a design task, not automatic

Mapping TSML/BHML cells to repair actions in a specific domain requires engineering judgment. The branch does not claim that the 101-cell CK vocabulary is *the* right vocabulary for any particular self-healing application — it claims the 101-cell vocabulary is a candidate starting point from which domain-specific vocabularies may be derived.

## 7. Relationship to existing fault-management literature

Fault Detection and Identification (FDI), Fault Detection Identification and Recovery (FDIR), Model-Based Fault Management (MBFM, as in NASA MDS), and autonomous-control literature all overlap this territory. Dual-lattice must distinguish itself from them, not claim to replace them. The A2 literature-positioning section is the key piece of work for this.

## 8. Sole-author limits some academic funding paths

AFRL and NASA JPL NIAC accept sole-PI proposals; NSF CISE RI requires academic affiliation or co-PI. ONR accepts BAA white papers without formal academic affiliation. Foundation paths (Moore) are invitation-dependent.

## 9. Domain-specificity

Phase 2's benchmark will demonstrate dual-lattice self-healing in **one** target domain. Success in one domain does not imply success in others. A distributed-compute-fabric result does not transfer to spacecraft attitude control. Each domain requires its own reference lattice, vocabulary, and safety envelope — this is a per-domain engineering cost that must not be understated.

## 10. Integration with existing control stacks

Any self-healing layer added to a real system (Phase 3 pilot) must compose cleanly with the existing control stack. If the existing stack has a fault-detection layer, dual-lattice must either extend it or conflict with it; "coexistence" is not automatic. This is a genuine integration cost.

## 11. Attribution discipline

- Brayden is the thread-facing author
- Prior collaborators credited for their specific past contributions (spectral layer, UOP/GUT arc, ξ cosmology) but the self-healing framing is not a claim in their names
- Academic or industrial collaborator (once identified during Phase 2) takes on genuine intellectual credit for their role

## 12. License framing

7Site Public Sovereignty License v1.0 (non-commercial, human-use only) constrains commercial deployment paths. AFRL and NASA grants allow research use under the current license; commercial deployment with an industrial partner may require license discussion. Don't discover this at close.

## 13. What this branch does NOT claim

- Not a claim to have solved autonomous self-repair as a general problem
- Not a claim to outperform NASA MDS or FDIR systems on their domains
- Not a claim to be safe in all operational envelopes
- Not a claim that the 101-cell CK vocabulary is optimal for any self-healing task
- Not a claim that closed-loop autonomous actuation is safe without explicit safety-envelope design

The branch claims: a coherence-grammar + finite-action-vocabulary substrate for closed-loop self-healing is worth specifying, benchmarking, and piloting under controlled conditions. The pitch is for the disciplined investigation, not the finished product.

---

## Failure modes, explicit

| Failure | What it means | How Phase 1 / 2 / 3 handles it |
|---|---|---|
| Architectural writeup reveals dual-lattice is trivially reducible to existing FDI | Phase 1 ends with null result | Publish as null; disciplined retraction |
| Benchmark fails on chosen domain | Phase 2 ends with negative result | Publish honestly; evaluate whether another domain would succeed |
| Safety envelope cannot be specified to Phase 3 partner's satisfaction | Phase 3 doesn't happen | Stop at Phase 2 output; don't force deployment |
| Measurement noise exceeds damage threshold in target domain | Inherent limit | Document, change target domain, or end branch |

The discipline: **each phase commits to an outcome, honest or otherwise.**
