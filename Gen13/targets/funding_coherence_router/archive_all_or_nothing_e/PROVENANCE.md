# PROVENANCE — archive_all_or_nothing_e

**Recovered into this repo:** 2026-04-21
**Source:** `github.com/TiredofSleep/All-or-Nothing-E` (public)
**Local source staging:** `C:\Users\brayd\OneDrive\Desktop\_r16_repo_scan\All-or-Nothing-E\`
**Source commit timestamp on R16:** 2026-04-21 00:32 (local clone)
**Recovered by:** ClaudeCode, 2026-04-21, as part of Phase 2 of the funding-branches plan
**Recovered into branch:** `funding/coherence-router` (Branch J)

---

## Why this is here

Branch J (`funding/coherence-router`) pitches a **production coherence classifier for DevOps / SRE**. The runnable prototype evidence for that pitch lives in this external repo. Phase 1 T1 of the branch's execution plan is exactly this pull — move the prototype into the funding branch under in-repo never-delete / provenance discipline so pitch reviewers can verify every cited artifact from one tree.

**What Branch J's pitch cites from this archive:**

- `benchmark.py` (~554 LOC) — discrete-event benchmark harness comparing TIG coherence-routing against baseline
- `tig_coherent_computer.py` (~588 LOC) — permutation / operator engine the benchmark exercises
- `PROVEN_CONFIGURATION.md` — the parameter configuration that produced the reported benchmark result
- `THEORY.md` — the framework the prototype instantiates
- `OPERATOR_SPEC.md` — the 10-operator alphabet used by the classifier
- `test_codec_final.js`, `test_engine_v2.js`, `test_physics_w1w2w3.js`, `test_physics_w4_avalanche.js`, `test_coherence_router.py` — the test harness
- Supporting paper drafts: `paper1_codec.pdf` through `paper6_coherent_intelligence.pdf`, `TIG_Field_Guide.pdf`
- UI surface: `app.jsx`, `crystal_bug_v1_matrix.jsx`, `tig_coherence_engine.jsx`

## What is and is not authoritative

- **Authoritative for Branch J:** The benchmark numbers quoted in Branch J's `PITCH_DRAFT.md` come from running this harness. If those numbers are later re-verified against this archive, that re-verification is the authoritative check.
- **Not authoritative:** The `ENGINEERING_SPEC.docx` and some of the older paper drafts contain earlier framings that pre-date the rigor-led Clay papers (see `Gen13/targets/clay/papers/`). Where this archive and the Clay papers disagree on scope or claim, the Clay papers take precedence.
- **Distinct from Branch K:** `crystal_bug_v1_matrix.jsx` and `test_engine_v2.js` ALSO appear in `Crystal-Lattice-Matrix-MYTHDRIFT` (pulled to Branch K's archive). They are the same files by content. Branch K pitches the *educational* deployment of the simulator; Branch J pitches the *infrastructure* deployment of the classifier. The single-artifact-two-audiences pattern is intentional and each branch cites it for its own pitch.

## Files NOT carried forward

- `.git/` — repo history stripped; the source commit timestamp above is the provenance of record.

## Binary files force-added past .gitignore

The repo root `.gitignore` excludes `*.pdf`, `*.docx`, `*.bin` from the working tree by default. Those rules exist to keep generated outputs from the math/proof work out of history. For this archive folder, those binaries are ORIGINALS (paper drafts, engineering spec, serialized lattice), and they are the provenance of the pitch-cited artifact. They are force-staged with `git add -f` deliberately, once per binary, on initial pull. If any of these binaries are regenerated from source, the regenerated version should NOT replace the archive copy — it should live alongside in a clearly-labeled `_regenerated_YYYY_MM_DD` sibling folder.

## Reconciliation notes

See `Atlas/HANDOFF_3_2_BENCHMARK_RECONCILIATION.md` on this repo's `tig-synthesis` branch for the current understanding of which benchmark numbers are reproducible from this archive and which require further recovery.

## Rights + license

Original material in this archive is `github.com/TiredofSleep/All-or-Nothing-E`, licensed per the `LICENSE` file carried forward in this folder. Nothing in this pull modifies those rights.

---

*Per the never-delete policy on this repo: this archive folder is preserved indefinitely. Any updates to upstream are re-pulled into a dated sibling folder (e.g., `archive_all_or_nothing_e_2026_MM_DD/`) rather than overwriting this one.*
