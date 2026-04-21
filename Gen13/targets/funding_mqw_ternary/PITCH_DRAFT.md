# PITCH_DRAFT — funding/mqw-ternary

**Addressee (working default):** DOE BES Materials Sciences and Engineering — III-nitride semiconductor-materials track
**Parallel draft:** NSF ECCS EPMD
**Ask:** Phase 1 $40K–$80K / 6 months (recovery + summary); Phase 2 $100K–$250K / 12 months (design review + fab partnership)
**Status:** Skeleton. DO NOT SEND until MQW trilogy (T2 in ARTIFACTS.md) is recovered.

---

## Opening (½ page)

Ternary logic has been a theoretical target since before binary computing was commercialized — three-state logic offers log₂ 3 ≈ 1.585 bits per digit (versus binary's 1 bit), lower switching energy per functional unit, and more compact arithmetic circuits. The reason ternary has remained theoretical is substrate: most physical media naturally produce two distinguishable states, not three. A ternary logic device either compiles down to binary underneath (defeating the purpose) or requires a physical substrate where three states are native.

This proposal describes a candidate native ternary substrate: **multi-quantum-well (MQW) structures in the GaN / AlN / InN family** whose band structure, under specific well-width and barrier-height engineering, produces three distinguishable optical-response states. The conceptual ancestor of this design is the Teardrop GaN Photonic Node Proposal (Jan 2026); the current-generation work is a three-paper trilogy developing specific MQW designs. This seedling proposes the **recovery, consolidation, and fabrication-partnership** work needed to convert the design from paper to a fabrication-ready specification.

## Background (~1 page)

> Content to be drafted after MQW trilogy (T2) recovery. Sections:
> - III-nitride MQW epitaxy: brief state-of-the-field review
> - Ternary logic: why it's attractive, why it hasn't happened, what substrates have been tried
> - The band-structure argument for three-state operation in specific GaN MQW designs
> - The Teardrop conceptual ancestor
> - Relationship to existing photonic-computing efforts (Lightmatter, Lightelligence, PSiQ, HP / Intel / IBM photonic groups)
> - Why MQW is orthogonal to those efforts (not a neural-accelerator; a logic substrate)

## The open question (½ page)

### Q1: Does the MQW trilogy design produce three distinguishable states in a real device?
This is the Phase 3 question. Phase 1 + Phase 2 set up the ability to answer Q1.

### Q2: What is the distinguishability margin under realistic fabrication variation?
MQW layer thickness control is limited to ~1–2 monolayers under MBE. The design margin must be large enough that wafer-to-wafer and within-wafer variation does not destroy three-state operation.

### Q3: What is the switching energy, speed, and density?
Practical ternary logic must compete with binary CMOS at some envelope. What is the envelope for MQW ternary, and where does it win?

## The proposed work

### Phase 1 — Recovery + design consolidation (Month 1–6, $40K–$80K)
**Deliverable A**: recover MQW three-state trilogy (T2 in ARTIFACTS.md), commit to `docs/archive_mqw/` with provenance.
**Deliverable B**: write MQW technical summary (A1 in ARTIFACTS.md), 8–12 pages.
**Deliverable C**: draft measurement plan (A2) and fabrication cost estimate (A3).
**Deliverable D**: write competitor-landscape survey (A4).

### Phase 2 — Design review + fab partnership (Month 7–18, $100K–$250K)
**Deliverable A**: design review by an MQW specialist (UCSB DenBaars/Speck, Stanford Weyl, Georgia Tech Lee, or USC Simin).
**Deliverable B**: fabrication partnership established with a named foundry.
**Deliverable C**: revised design based on review + partnership constraints.

### Phase 3 — Fabrication + measurement (Month 19–42, $500K–$1.5M)
**Deliverable**: MBE/MOCVD growth of the designed MQW stack. Characterization (PL spectroscopy, pump-probe, I-V under optical excitation) to test three-state operation. Outcome published regardless of result.

### Phase 4 — If Phase 3 verifies three states (Month 43+, $1M–$5M)
**Deliverable**: single ternary logic gate demonstration. Path to tape-out planning. Follow-on funding case.

## Why DOE BES specifically

BES funds fundamental III-nitride research at exactly the scale and scope needed for Phases 1–3. Historical BES awards in GaN MQW work typically run $300K–$1M/year per single-PI lab. A Phase 1 ask at $40K–$80K is inside BES's typical seedling range; the Phase 3 fabrication program is inside their normal grant scale.

## Parallel draft: NSF ECCS EPMD

NSF ECCS's Electronic, Photonic, and Magnetic Devices program funds exactly this kind of novel-device work. ECCS grants are typically $300K–$600K over 36 months — well-matched to Phase 2 of this proposal. ECCS requires academic co-PI, which will emerge naturally from Phase 2's design review.

## Parallel option: DARPA PIPES-successor

DARPA's current photonic-computing portfolio includes programs descended from PIPES. An MQW ternary logic proposal targeting a BAA response would be high-risk / high-reward; fits DARPA seedling or Young Faculty Award (if academic PI identified).

## Attribution

- **Brayden Sanders** — PI, sole funder-facing author, architect of Teardrop GaN and contributor to MQW trilogy
- Architectural dialogues with ClaudeChat, Celeste/GPT acknowledged in methods
- Prior collaborators (C.A. Luther et al.) credited only where their specific prior work is cited; Luther not actively collaborating as of April 2026
- Academic co-PI in III-nitride epitaxy to be identified during Phase 2

## Attachments (once assembled)

- Recovered Teardrop GaN proposal (T1)
- Recovered MQW trilogy (T2) — three papers
- MQW technical summary (A1)
- Measurement plan (A2)
- Fabrication cost estimate (A3)
- Competitor-landscape survey (A4)

## Pre-send checklist

- [ ] T2 MQW trilogy recovered and committed to `docs/archive_mqw/`
- [ ] A1 technical summary drafted
- [ ] A2 measurement plan drafted
- [ ] A3 fab cost estimate drafted (with quote from at least one facility)
- [ ] A4 competitor survey drafted
- [ ] Framing cleanup: remove "consciousness" language from V20 scaling-laws doc before referencing in a DOE pitch; frame physics on its own terms
- [ ] Academic co-PI identified or at least 2 candidate contacts engaged
- [ ] Brayden reviews + edits
- [ ] Brayden sends
