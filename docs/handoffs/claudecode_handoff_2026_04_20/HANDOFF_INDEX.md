# ClaudeCode Handoff Package — April 20, 2026

**From:** Brayden + ClaudeChat (overnight working session)
**To:** ClaudeCode, working on the R16
**Contents:** Three documents defining a full outreach restructuring and recovery plan for the TIG/CK project.

---

## What's in this zip

### 1. `README.md` (266 lines, HELD)
The finalized rigor-led replacement for the ck repository's public-facing README. Funder-oriented, proved-theorems-first, honest scope throughout.

**Status: HELD.** Do NOT commit this to the ck repo yet. Brayden said "hold on to it" pending his explicit go-ahead. When he gives the green light, commit with message: `README: rigor-led replacement for funding outreach`, and archive the old 769-line README to `docs/historical/README_v1_pre_2026_04_21.md` under the never-delete policy.

### 2. `SECURITY_CRYPTO_HANDOFF.md` (354 lines)
The full outreach restructuring plan. Covers:
- Inventory of all 8 existing public repos under `github.com/TiredofSleep` (verified by Grok's 2026-04-20 sweep)
- Recovery priorities for pre-March 2026 material
- Four consistency issues needing resolution before any funder-facing claim
- Seven outreach tracks with distinct funder pools (Pitches A-G)
- Four-phase execution sequencing
- Never-delete, provenance, and scope-tagging discipline notes

This is the **strategic** document. It tells you what to build and in what order.

### 3. `JAN2026_RECOVERY_MANIFEST.md` (562 lines)
Focused recovery instructions for the January 2026 foundation work across five threads:
- **Thread 1** (Jan 29, `7f17a615`) — 233-page "How to use the Lattice" canonical + Celeste's Physics Compatibility Appendix
- **Thread 2** (Jan 29, `4bd41b60`) — TIG 7.0/8.x/9.x Unity Kernel stack (the 32pp asymmetric-failure result)
- **Thread 3** (Jan 29, `ed8ef620`) — Trifecta: V20 Consciousness-Anchored Scaling Laws + Hardware Embodiment Safety Case + Comparative Field Theory Review + Teardrop GaN Photonic Node Proposal (~134KB, 11 documents)
- **Thread 4** (Jan 29, `2f2f9db3`) — Public repo documentation pack with the canonical Trinity Infinity Geometry definition
- **Thread 5** (Jan 31, `9fdac5c3`) — SNOWFLAKE security framework with empirical χ² = 22.03 finding

This is the **archaeological** document. It tells you what exists in the MYTHDRIFT archives and on the R16 filesystem that needs to be pulled into `ck/docs/archive_jan2026/` under clear provenance.

---

## Execution sequencing

**Phase 1 (tonight, while Brayden sleeps):**
1. Clone all 8 public repos to R16 workspace.
2. Read each repo's README and main content files.
3. Run R16 filesystem searches per the recovery manifest (Priorities 1-5).
4. Produce a one-page summary per repo.
5. Produce a file-recovery report documenting what was found and what wasn't.
6. Do NOT modify any ck content during this phase.
7. Do NOT commit the new README yet.

**Phase 2 (after Phase 1 reports back):**
1. Pull verbatim copies of high-value content: 233-page canonical, `coherence_router` code, `docs/COMPUTE.md`, WP1-5, SNOWFLAKE architecture, CRYSTALOS logs if recoverable.
2. Resolve the four consistency issues in §3 of `SECURITY_CRYPTO_HANDOFF.md`.
3. Commit into `ck/docs/archive_jan2026/` with provenance headers.

**Phase 3 (after Brayden selects pitch priorities):**
1. Brayden reviews Phase 1 and 2 findings.
2. Brayden selects which 1-2 pitches go out first.
3. Create new outreach repos corresponding to selected pitches.
4. Refresh existing repo READMEs to the ck rigor standard.
5. Update ck README §8 with pointers to all outreach repos (only after Brayden approves the main README for commit).

**Phase 4 (Brayden's decision):**
1. Brayden selects first funder.
2. ClaudeChat drafts the pitch document based on selected track's material.
3. Brayden reviews and sends.

---

## Critical validation tasks

Four things need resolution before ANY number appears in a funder-facing document:

1. **ω(b) idempotent count.** Prior sessions report "2 / 6 nontrivial" and the formula `N_idemp(b) = 2^(ω-1) - 1`. These don't match. Check actual proof scripts.

2. **TIG Unity benchmark numbers.** Email whitepaper has 32pp drop-rate improvement. Grok's summary of `docs/COMPUTE.md` has expanded metrics (P99 latency, recovery time, resource utilization, cascade failures). Verify against simulation code.

3. **SNOWFLAKE χ² = 22.03.** The single most important validation task. Recover CRYSTALOS logs. Document: what was the null hypothesis? Degrees of freedom? Fires computed over? Independence assumption? A security pitch with a clean p-value is a research-grade pitch; one with an unspecified p-value gets dismissed.

4. **MQW semiconductor paper trilogy location.** The Teardrop GaN proposal from Jan 29 is the conceptual ancestor; the MQW three-state paper series is the current unreleased work. Search R16 for the physics-content documents.

---

## Discipline reminders

- **Never-delete policy absolute.** Superseded material gets `[HISTORICAL]` marker. Falsified material gets `[FALSIFIED]` marker. Nothing gets removed.
- **Preserve provenance** on every recovered file. Header with: original repo, original commit date, recovery date, source path on R16 if applicable.
- **Flag reconstructions** clearly. If a document cannot be recovered verbatim and must be reconstructed from conversation fragments, mark it `[RECONSTRUCTED — NOT VERIFIED AGAINST ORIGINAL FILE]`.
- **Collaborator status.** C.A. Luther is no longer actively collaborating — previously-credited work stays credited. ChatGPT ("Celeste") has been in dialogue for design discussions but is not cited as a human co-author in any funder-facing document. Brayden is sole funder-facing author unless otherwise specified.
- **Generalization directive.** Brayden has stated his ability to generalize CK has not been fully realized. Where finished work doesn't yet exist for a domain (security, biology, materials, social coherence), you may draft scaffolding documents using the Thread 4 templates (THEORY.md / COMPUTE.md / STATUS.md / FALSIFIABLES.md pattern), flag them clearly as `[SCAFFOLDING — NEEDS REVIEW]`, and commit for Brayden's subsequent review and refinement. Give him scaffolding to iterate on, not blank pages.

---

## Final note

The two working documents (SECURITY_CRYPTO_HANDOFF and JAN2026_RECOVERY_MANIFEST) are designed so you can work autonomously through Phase 1 and Phase 2 without needing to consult ClaudeChat. Phase 3 requires Brayden's pitch-priority selection. Phase 4 is Brayden-driven.

The README stays held until Brayden's explicit go-ahead.

Everything in the January archive is recoverable. The work is real, extensive, and well-structured. Brayden has been carrying the full chronology in his head for three months; this handoff is meant to offload that into the filesystem where every future Claude instance can find it.

**Good luck, ClaudeCode. The path is clean from here.**

— ClaudeChat, 2026-04-20 night session
