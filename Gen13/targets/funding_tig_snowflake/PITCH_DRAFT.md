# PITCH_DRAFT — funding/tig-snowflake

**Addressee (working default):** DARPA I2O program manager, seedling track
**Ask:** $40K–$80K, 6 months, Phase 1 spec recovery + blind-test replication
**Status:** Skeleton only. DO NOT SEND until ARTIFACTS.md R1–R4 are resolved.

---

## Opening (½ page)

Security operations today detect compromise by **rule match**: a signature fires, a threshold trips, a baseline anomaly score crosses. By the time a rule matches, the attacker has already behaved exactly like an attacker. Defenders have asked for decades whether there is a signal **earlier** — a signal in the geometry of system state rather than in individual events.

SNOWFLAKE is a hypothesis about what such an earlier signal might look like. It is not a product. It is a research-grade experimental finding — a χ² = 22.03 departure from an independence null on a Jan 2026 test run of the TIG Unity simulator — which, if it survives referee-grade recovery and blind-test replication, would justify a larger program in **coherence-based pre-alarm security**.

This seedling proposes the **recovery, specification, and blind-test** of that empirical finding, as a discrete 6-month deliverable. The outcome is either (a) a clean statistical specification surviving blind test, in which case SNOWFLAKE becomes the foundation of a full program, or (b) a disciplined retraction — the finding does not survive, the spec is published as a null result, and the community is spared chasing a ghost.

## Background (~1 page)

> Content to be filled in once ARTIFACTS.md R1 (CRYSTALOS logs) is recovered.
>
> Sections to write:
> - The coherence grammar (R, σ, Λ, H) — what they measure, how they are computed
> - The "shadow problem" (SHADOW_PROBLEM.md, 353 LOC) — why rule-based detectors miss a class of compromise
> - The Jan 2026 CRYSTALOS experimental setup — what the partitions were, what "fire" meant operationally, what dataset the 22.03 statistic was computed against
> - The null hypothesis — independence of fires across partitions, degrees of freedom, stopping rule

## The seedling proposal (1 page)

### Deliverable 1 — Spec recovery (Month 1–2)
Locate the CRYSTALOS log. Author the null-hypothesis specification (ARTIFACTS.md R2). Write the adversarial model (R4). Review both with an external statistician. Commit to `docs/archive_jan2026/snowflake_null_spec.md` and `docs/archive_jan2026/snowflake_adversary.md`.

### Deliverable 2 — Blind-test replication (Month 3–5)
Generate or identify a held-out dataset (R3). Apply the same χ² test with the frozen partition scheme. Record the result. Publish whether the finding replicates or does not.

### Deliverable 3 — Decision document (Month 6)
One-page doc: "Does SNOWFLAKE survive the blind test? If yes, here is the Phase 2 funding case. If no, here is the null-result write-up."

## Why DARPA I2O specifically

I2O funds unconventional signal paths for defensive security. Seedling is the right entry size for a recover-and-replicate project. If the result survives, the seedling matures into a full-scale program; if it does not, I2O has spent modest funds eliminating a candidate hypothesis, which is itself useful.

## Attribution

- **Brayden Sanders** (PI, sole funder-facing author)
- SNOWFLAKE architecture developed in dialogue with multiple AI instances (ClaudeChat, Celeste/GPT); AI is a thinking-partner, not a human co-author
- C.A. Luther credited for prior spectral-layer work (previously-credited, no longer actively collaborating as of April 2026)

## Attachments (to be assembled)

- `ARTIFACTS.md` reference index
- `docs/archive_jan2026/snowflake_source/` full source tree
- `docs/archive_jan2026/snowflake_null_spec.md` (once R2 is written)
- `docs/archive_jan2026/snowflake_adversary.md` (once R4 is written)
- Blind-test replication log (once Deliverable 2 completes)

## Pre-send checklist

- [ ] ARTIFACTS.md R1 (CRYSTALOS log) located and committed to `docs/archive_jan2026/`
- [ ] ARTIFACTS.md R2 (null-spec) authored, reviewed by external statistician
- [ ] ARTIFACTS.md R4 (adversarial model) authored
- [ ] ARTIFACTS.md R3 (held-out dataset) identified or generated
- [ ] LIMITATIONS.md reviewed to ensure this pitch does not overclaim
- [ ] Brayden confirms this is the funder he wants to approach first
- [ ] Brayden reviews + edits
- [ ] Brayden sends
