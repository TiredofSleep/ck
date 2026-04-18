# Packing Rules
## Rules for Maintaining the Sprint Archive

---

## Purpose

These rules govern how the archive is constructed, what changes are permitted during packaging, and what changes are prohibited. Apply strictly. When in doubt, do not modify.

---

## Preservation Rules

### Rule 1 — Preserve original verdicts verbatim

Each sprint's VERDICT document is copied into the pack unchanged. No softening, no strengthening, no rewording. A FAIL stays FAIL. An UNCLEAR stays UNCLEAR. A vacuous PASS stays a vacuous PASS. A PASS stays PASS with its original sigma separation reported as stated.

**Prohibited:**
- Rewriting "UNCLEAR" as "partial PASS" or "mixed result."
- Rewriting "FAIL" as "informative negative" within the verdict document itself (it already says that where it says that).
- Adding retrospective context that changes the apparent strength of a verdict.

**Permitted:**
- Copying the document as-is.

### Rule 2 — No new interpretation

The pack contains no new synthesis across sprints except where explicitly specified by user (SPRINT_LEDGER.md, CURRENT_STATE_SUMMARY.md). No new "big picture" documents. No "what does this mean together" documents. No retrospective reframing.

**Prohibited:**
- Creating new narrative summaries that weren't commissioned.
- Writing retrospective analysis sections.
- Building compound claims that bridge multiple sprints beyond what was already written.

**Permitted:**
- The four user-commissioned packaging deliverables (plan, rules, summary, ledger).
- A README.md limited to table-of-contents navigation.

### Rule 3 — No merging of PASS + UNCLEAR into composite claims

v1.1 PASSed on identity-edge. v1.2-adj PASSed on leaf-edge. The compound claim "the ADD edge is a leaf edge whose leaf endpoint is the identity element" exists in the VERDICT documents as a retrospective-synthesis observation, but it does not get promoted to its own document or its own sprint.

**Prohibited:**
- Writing a "Subtype Bridge Confirmed Features" document that combines v1.1 and v1.2-adj results.
- Computing a composite sigma across metrics.
- Claiming an accumulated multi-sprint finding that is stronger than any single sprint earned.

**Permitted:**
- Listing each verdict separately in SPRINT_LEDGER.md.
- In CURRENT_STATE_SUMMARY.md §"bridge-confirmed", listing each confirmed feature as a bullet tied to its specific sprint.

### Rule 4 — No retroactive wording changes

Documents on disk reflect their state at the time of their associated sprint. The pack copies them as they were.

**Prohibited:**
- "Fixing" phrasing in old documents.
- "Clarifying" an earlier document using knowledge from later sprints.
- Updating thresholds, metric definitions, or claim language in pre-regs after their sprints ran.

**Permitted (cleanup only):**
- Leading/trailing whitespace normalization.
- Line-ending normalization (LF).
- Duplicate-blank-line collapse.
- Fixing obviously malformed Markdown (e.g., unclosed code blocks) — but only if genuinely malformed, not just aesthetically off.

### Rule 5 — Keep scope tags visible

Every pre-reg in the controls/ folder retains its Scope Declaration block at the top. Every results/verdict/repro document retains its scope reference.

**Prohibited:**
- Removing scope tags for brevity.
- Collapsing scope tags into footnotes.
- Omitting scope tags from newly created navigation documents like README.md.

**Permitted:**
- Displaying scope tags as they appear in the source.

---

## Negative Result Preservation

### Rule 6 — All negative results stay

The pack includes FAILs and the vacuous S30 PASS. None of these are removed, reclassified, or minimized.

Six informative negatives on record:
- S28-v1.0 (basin smoothness transport, null inverted)
- S29-v1.0 (anchored curve, no depth organization)
- S30b-v1.0 (no seam under uniform noise)
- S31-pilot-v1.0 (convention mismatch)
- P3-BridgeA-v1.0 (object-type mismatch)
- P3-Subtype-v1.0 (UNCLEAR — 2 of 3 nulls inadequate)

One vacuous PASS:
- S30-v1.0 (empty seams; formal pass, evidentially uninformative)

All retained with full verdict documents.

### Rule 7 — Attribution of negatives preserved

Each negative has a specific cause documented in its VERDICT (and often in its attribution sub-document). The pack preserves those causes.

**Prohibited:**
- Stripping attribution out of VERDICT documents.
- Summarizing FAILs in one sentence that omits the cause.

**Permitted:**
- SPRINT_LEDGER.md's one-line attribution column (a short cause summary with reference to the VERDICT document).

---

## Structural Rules

### Rule 8 — Each sprint directory is self-contained

A sprint's directory contains everything needed to understand that sprint's verdict:

- Results data file.
- Verdict document.
- Reproducibility document (where it exists on disk).
- Attribution sub-documents tied to that sprint (WHY_, SCOPE_LIMITS, METRIC_SET).

**Prohibited:**
- Splitting a sprint's attribution documents across directories.
- Cross-sprint-directory dependencies that require navigation to other sprints to understand a verdict.

**Permitted:**
- Cross-references within VERDICT text (pointers to foundation documents or to other sprints for context).
- Pre-reg living in controls/ with sprint output living in sprints/ (standard separation).

### Rule 9 — Controls directory is pre-regs only

The controls/ folder contains the frozen pre-registrations. One pre-reg per executed sprint.

**Prohibited:**
- Adding post-hoc spec revisions to controls/.
- Consolidating multiple pre-regs into one.
- Creating a "master controls" summary.

**Permitted:**
- Both S31-pilot-v1.0 and v2.0 pre-regs present, since both ran as distinct sprints.

### Rule 10 — Foundation directory is locked

The 8 foundation documents form the program's shared discipline. They are copied into the pack without modification.

**Prohibited:**
- Merging foundation docs to reduce count.
- Adding new foundation docs without an explicit governance change.
- Editing foundation docs to reflect later sprint outcomes (they already do, at the level they committed to).

**Permitted:**
- Formatting normalization as in Rule 4.

---

## Do-Not-Include Rules

### Rule 11 — Omission list is final

The CLAUDECODE_HANDOFF_PLAN.md §"Omission List" is the authoritative exclusion set. Documents on that list do not appear in the pack.

**Prohibited:**
- "Sneaking in" an omitted document via a renamed file.
- Copying omitted content into an included document.
- Keeping omitted content accessible via a reference or link.

**Permitted:**
- Adding a new omission to the list if the user explicitly requests.

### Rule 12 — No speculative content

Content that speculates about future findings, future sprints that would "probably pass," or future theorems that "might extend" — all excluded.

**Prohibited:**
- Predictions in VERDICT documents edited in to make PASSes look expected.
- Speculative addenda about what the findings "might mean."

**Permitted:**
- Predictions that were already present in pre-regs (these are part of the frozen record and stay).
- Honest open_questions/ documents noting what remains untested.

---

## Cross-Reference Rules

### Rule 13 — Internal references stay internal

Within the pack, documents reference each other by relative path or by document name. No external URLs that aren't already present in the source documents.

### Rule 14 — No circular synthesis

Sprint A's VERDICT may reference Sprint B (e.g., v1.2-adj references v1.1 for inheritance). These references are preserved. But no new document is created that circularly references multiple VERDICTs to build a "composite finding."

The inheritance relationships are:
- v1.2-adj inherits I from v1.1 (reported, not re-scored).
- v1.1 inherits object class from P3AP (uses P3AP's recovered seams).
- P3AP inherits extractor from S31-pilot-v2.0 (validated).
- All Path 2 sprints inherit the $h_\text{ext}$ convention from the attractor reconciliation.
- All Path 1 sprints inherit the $h_\text{thm}$ convention from the attractor reconciliation.

These inheritances are documented within each sprint's VERDICT where relevant. No new inheritance-map document.

---

## Scope Discipline

### Rule 15 — Path labels are not decorative

Path 1, Path 2, Path 3 are load-bearing scope markers. They determine claim class ceilings and permitted comparisons. The pack retains them in every document that has them.

**Prohibited:**
- Dropping path labels from section headers for brevity.
- Conflating "bridge-confirmed" with "theorem-level" anywhere in the pack.

**Permitted:**
- Using paths as a navigation aid in README.md and SPRINT_LEDGER.md.

### Rule 16 — Three claim classes stay distinct

- **theorem-level:** proven result. Only Path 1 can produce these.
- **observation-level:** pre-registered empirical finding. Only Path 2 can produce these.
- **bridge-level:** relational claim with explicit bridging rule. Only Path 3 can produce these.

No PASS in the pack is upgraded to a higher class than its path permits.

---

## Change Governance

### Rule 17 — Post-pack changes require user approval

Once the pack is committed to GitHub, further additions, reclassifications, or re-synthesis require explicit user approval. The pack is a snapshot, not a living document.

**Permitted without approval:**
- Typo fixes within a document (not wording changes).
- Adding new sprints' results to the archive (with their own pre-regs in controls/ and directories in sprints/).
- Updating SPRINT_LEDGER.md and CURRENT_STATE_SUMMARY.md when new sprint results arrive.

**Requires approval:**
- Removing documents.
- Editing VERDICTs.
- Reclassifying paths.
- Merging documents.
- Creating new synthesis documents.

---

## Summary

The pack is a disciplined archive. Every document in it earned its place through a pre-registered sprint, a foundation decision, or a commissioned packaging task. Nothing was added opportunistically. No speculative content. No broad synthesis. No promotion.

Apply these rules strictly. When in doubt, do not modify.
