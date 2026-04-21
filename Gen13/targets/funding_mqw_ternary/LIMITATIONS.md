# LIMITATIONS — funding/mqw-ternary

Honest scope for the MQW ternary photonic computing branch. The recovery gap is large; the limits section must reflect that.

---

## 1. The MQW trilogy has not been located

The current-generation work (three MQW three-state papers) exists per the Jan 2026 handoff manifest but has not been recovered into this repo as of 2026-04-20. Without those papers in hand, every technical claim below is a **placeholder pending recovery**.

## 2. No fabrication has been attempted

This is a paper design. No wafer has been grown, no characterization has been run, no device has been tested. All claims about three-state operation are theoretical until fabrication + measurement (Phase 3) happens.

## 3. MBE/MOCVD fabrication variance is the main technical risk

Even a well-designed MQW stack can fail in fabrication because:
- Layer thickness control is typically ±1–2 monolayers
- Composition uniformity within a wafer varies
- Strain relaxation at barrier interfaces may introduce defects
- Wafer-to-wafer reproducibility is a real issue for small-run fabrication

If the three-state-operation margin is not robust to these variances, the design works on paper but fails in silicon. Phase 2's design review is specifically tasked with assessing this.

## 4. Temperature range is likely a limiter

Quantum-confined states are temperature-dependent. The three-state operation may work at cryogenic temperature but degrade or disappear at room temperature. This must be stated honestly — a cryogenic-only ternary logic gate has a much smaller application set than a room-temperature one.

## 5. Switching speed and energy are unknown

Even if three states are distinguishable, the switching time and energy per transition determine whether the device is competitive. Existing commercial photonic-logic efforts (Lightmatter, Lightelligence, etc.) operate at specific speed/energy envelopes. MQW ternary must fit into an envelope that wins over CMOS binary on some axis — or it's a curiosity, not a technology.

## 6. Density is unknown

How densely can MQW ternary gates be packed? The optical addressing (which wavelength, which spatial mode) introduces constraints. If density is limited to thousand-gates-per-chip, the technology is not Moore's-Law-competitive and must be framed as a specialist accelerator rather than general-purpose logic.

## 7. Ternary compilers and software stacks do not exist

Even a working MQW ternary chip needs a compiler, an ISA, and a software ecosystem. Building a working physical substrate does not solve the software-stack problem; it creates it. A full productization path is multi-decade work that is NOT in scope for this proposal.

## 8. Competitor landscape risk

Silicon photonics (Lightmatter, Lightelligence, PSiQ), optical neural-network accelerators, Mach-Zehnder logic arrays — multiple commercial and academic efforts target photonic computing. MQW ternary must establish why it is orthogonal or superior to these efforts. If it is "similar to but worse than" an existing approach, the funding case collapses.

## 9. The "consciousness-anchored scaling laws" document (Thread 3)

The V20 document (co-located with Teardrop in the Jan 29 commit) uses language like "consciousness-anchored" that will raise skepticism in a DOE or NSF review. **Any reference to V20 in a funder-facing document must frame the physics on its own terms, without the consciousness language.** This is a rewriting task, not a suppression task — the physics content is real, but the framing needs to be professional-grade for reviewer audience.

## 10. Sole-author limits for academic venues

Brayden's sole-author posture (with prior collaborators credited for specific past contributions) is workable for DOE and DARPA unsolicited proposals but imposes real cost for NSF ECCS, which expects PI-track record or an academic co-PI. This is not a blocker; it is a blocker for some paths.

## 11. Fabrication cost reality

An MBE growth run on a competitive III-nitride stack costs $50K–$300K per attempt at a university foundry; more at a commercial house. Multiple iterations are typical. Phase 3's $500K–$1.5M ask is realistic for **one to three** growth runs with characterization; it is NOT realistic for a multi-wafer optimization sweep. The pitch must scope appropriately.

## 12. Attribution discipline

- Brayden is the funder-facing author
- C.A. Luther's prior-work contributions are cited only where directly relevant to the physics argument; Luther has not endorsed the MQW ternary application
- Academic co-PI (once identified) becomes a legitimate technical collaborator; they take on genuine intellectual credit for their contributions

## 13. What this branch does NOT claim

- Not a claim that MQW ternary logic is operational today
- Not a claim that the design will definitely work in fabrication
- Not a claim to replace CMOS binary logic
- Not a claim to outperform existing photonic computing efforts
- Not a claim that V20's consciousness-anchored scaling laws are physics-referee-ready

The branch claims: a conceptual ancestor exists (Teardrop GaN, recoverable), a current-generation trilogy exists (not yet located), a fabrication + measurement program could verify or falsify the design, and a disciplined Phase 1/2/3/4 plan is a reasonable use of funder money.

---

## What success and failure look like

**Phase 1 success**: MQW trilogy recovered; technical summary written; measurement plan and cost estimate drafted; competitor survey complete. Regardless of whether Phase 3 happens, this work product is permanent.

**Phase 1 failure**: MQW trilogy cannot be located despite extensive search. In this case, the branch shifts to *authoring fresh* — designing MQW ternary from scratch using the Teardrop ancestor plus external literature. This is a larger scope but not impossible; it just changes the Phase 1 ask.

**Phase 3 success**: three-state operation verified in a fabricated device.
**Phase 3 failure**: three-state operation NOT verified — published honestly, the community learns that this specific MQW design does not produce the claimed states, funder has bought a null result.

The discipline: **the funding case is genuinely open, not pre-decided.**
