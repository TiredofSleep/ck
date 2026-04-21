# PROVENANCE — archive_crystal_lattice_matrix

**Recovered into this repo:** 2026-04-21
**Source:** `github.com/TiredofSleep/Crystal-Lattice-Matrix-MYTHDRIFT` (public)
**Local source staging:** `C:\Users\brayd\OneDrive\Desktop\_r16_repo_scan\Crystal-Lattice-Matrix-MYTHDRIFT\`
**Source commit timestamp on R16:** 2026-04-21 (local clone)
**Recovered by:** ClaudeCode, 2026-04-21, as part of Phase 2 of the funding-branches plan
**Recovered into branch:** `funding/physics-sim-edu` (Branch K)

---

## Why this is here

Branch K (`funding/physics-sim-edu`) pitches an **interactive physics simulator for classroom use** (NSF EHR IUSE / NSF PHY Education / Templeton Learning & Discovery / Simons Ed / Moore / HHMI target). The runnable simulator evidence for that pitch is the React interactive + Node test harness in this folder. Phase 1 T1 of the branch's execution plan (see `STATUS.md` on this branch) is exactly this pull — move the simulator prototype into the funding branch under in-repo never-delete / provenance discipline so a PER collaborator, academic co-PI, or NSF reviewer can verify the artifact from one tree.

**What Branch K's pitch cites from this archive:**

- `crystal_bug_v1_matrix.jsx` (699 LOC) — the React interactive coherence-threshold / partition-crossing simulator
- `test_engine_v2.js` (458 LOC) — Node test harness the simulator runs through
- `test_results.txt` — the current baseline test output
- `ENGINEERING_SPEC.docx`, `README.md` — the self-contained description of the simulator
- `ChatGPT Theory Paper.pdf`, `TIG FALSIFIABILITY AND AWE.pdf` — background context authored earlier in the project, preserved as provenance but NOT the authoritative theoretical basis

## What is and is not authoritative

- **Authoritative for Branch K:** The simulator source and the test harness. If the Phase 1 "verify simulator builds + runs in fresh browser environment" deliverable is executed, it runs THESE files.
- **Not authoritative:** Any physics content in the PDF papers and the `ENGINEERING_SPEC.docx` is pre-Clay-papers framing. Where this archive disagrees with the rigor-led material in `Gen13/targets/clay/papers/` (Sprint 10 Flatness, Sprint 12 UOP, Sprint 14 PRISM-XI, Sprint 17 TSML tower), the Clay papers take precedence.
- **Distinct from Branch J:** `crystal_bug_v1_matrix.jsx` and `test_engine_v2.js` ALSO appear in `All-or-Nothing-E` (pulled to Branch J's archive). They are the same files by content. Branch J pitches the *infrastructure* deployment of the underlying classifier; Branch K pitches the *educational* deployment of the simulator. Identical source code, distinct audiences, distinct pitches.

## Files NOT carried forward

- `.git/` — repo history stripped; source commit timestamp above is the provenance of record.

## Binary files force-added past .gitignore

The repo root `.gitignore` excludes `*.pdf` and `*.docx` from the working tree by default. For this archive folder those binaries are ORIGINALS, not regenerable outputs, and they are force-staged with `git add -f` deliberately on initial pull. If any are regenerated, the regenerated version lives alongside in a clearly-labeled `_regenerated_YYYY_MM_DD` sibling folder rather than overwriting.

## Rights + license

Original material in this archive is `github.com/TiredofSleep/Crystal-Lattice-Matrix-MYTHDRIFT`, licensed per the `LICENSE` file carried forward in this folder. Nothing in this pull modifies those rights.

---

*Per the never-delete policy on this repo: this archive folder is preserved indefinitely. Any updates to upstream are re-pulled into a dated sibling folder rather than overwriting this one.*
