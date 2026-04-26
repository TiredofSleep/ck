# ARTIFACTS — funding/tig-snowflake

Exact file paths, line counts, and recovery tasks. Numbers reflect the state documented during the 2026-04-20 external-repo survey.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## What is already in the CK repo (tig-synthesis)

### 1. TIME-FOR-HELP-AND-SCRUTINY repo clone
- **Source**: `github.com/TiredofSleep/TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT`
- **Local clone**: `_brayden_repos/TIME-FOR-HELP-AND-SCRUTINY-please-No-more-AI-MYTHDRIFT/` (on R16 desktop, not yet committed into ck repo)
- **Scope**: 14 files, ~10,836 lines of code and documentation
- **Provenance-flagging regime**: 3-tier (CONJECTURAL / STRUCTURAL / PROVED) applied per-claim
- **Key SNOWFLAKE material**: architecture notes, coherence-grammar state definitions, simulation harness
- **Recovery task**: copy verbatim into `docs/archive_jan2026/snowflake_source/` with provenance header

### 2. tig_civilization simulators
- **Source**: also within the TIME-FOR-HELP repo
- **Files**:
  - `tig_civilization_v5.py` — earlier civilization-scale coherence model
  - `tig_civilization_v7.py` — later revision with expanded state vector
- **Combined**: ~1,340 LOC
- **Why relevant to SNOWFLAKE**: the R-σ-Λ-H state variables used for anomaly detection are the same as those used in civilization-scale runs; the runtime machinery is shared

### 3. crystal_bug_v1_matrix.jsx
- **Source**: Crystal-Lattice-Matrix-MYTHDRIFT repo
- **Line count**: 699 LOC (single-file React component)
- **Role**: a visualization substrate for coherence-lattice state; could become the demo surface for a SNOWFLAKE pitch (funders respond to visible anomalies)
- **Recovery task**: evaluate whether to carry forward as part of the pitch or leave as auxiliary

### 4. SHADOW_PROBLEM.md
- **Source**: in TIME-FOR-HELP repo
- **Line count**: 353 LOC
- **Content**: documents the "shadow" failure mode — a class of compromise that remains invisible to rule-based detectors because no rule matches
- **Why relevant**: this is the threat model that SNOWFLAKE was designed to address; it should be the opening section of the PITCH_DRAFT

---

## What is missing and must be recovered (blockers for pitch)

### R1 — CRYSTALOS log with χ² = 22.03 output
- **Priority**: 1 (nothing ships without this)
- **Likely locations** (in order to search):
  1. `old/Gen10/` within this repo
  2. `archive_imports/jan2026/` if it exists
  3. R16 desktop loose files from Jan 31 2026 date range
  4. ClaudeChat export from Jan 31 working session — commit hash `9fdac5c3` per handoff manifest
- **What to extract**: the specific numbers — χ² value, degrees of freedom, dataset (number of events, number of partitions), stopping rule, seed

### R2 — Null-hypothesis specification document
- **Priority**: 1 (also blocking)
- **Status**: does not exist in written form; must be authored from the CRYSTALOS log content + Jan 31 conversation fragments
- **What it must contain**:
  - Statement of H₀ ("fires are independent and uniformly distributed across the partition scheme P with partition cardinality k")
  - Definition of the partition scheme P (what are the categorical axes, what are the boundaries)
  - Degrees of freedom: (rows − 1) × (cols − 1) of the contingency table
  - Sample size (N fires in the dataset)
  - Stopping rule: was χ² computed once on the full dataset, or was the dataset scanned with multiple comparisons?
  - Test statistic convention: Pearson χ² vs likelihood-ratio G²

### R3 — Independent replication dataset
- **Priority**: 2 (blocking a funder-grade result, not blocking a seedling conversation)
- **What's needed**: a held-out dataset that was not used to set the partition scheme P or the threshold for declaring an anomaly
- **Source**: this may need to be generated fresh from the tig_civilization simulators or collected from a real log source

### R4 — Adversarial model
- **Priority**: 2
- **What's needed**: a written statement of the attacker's capabilities (read access? write access? knowledge of the partition scheme? adaptive?)
- **Why it matters**: DARPA, ONR, IARPA, and NSF SaTC reviewers all want an explicit threat model before they fund defensive work

---

## Line-count and file-path summary

| File | Repo | Path | LOC | Status |
|---|---|---|---|---|
| SNOWFLAKE architecture | TIME-FOR-HELP | (14 files across repo) | ~10,836 total | cloned, uncommitted |
| `tig_civilization_v5.py` | TIME-FOR-HELP | root | ~650 | cloned |
| `tig_civilization_v7.py` | TIME-FOR-HELP | root | ~690 | cloned |
| `crystal_bug_v1_matrix.jsx` | Crystal-Lattice-Matrix | root | 699 | cloned |
| `SHADOW_PROBLEM.md` | TIME-FOR-HELP | root | 353 | cloned |
| CRYSTALOS χ²=22.03 log | (unknown) | (unknown) | (unknown) | **NOT FOUND** — R1 |
| Null-hypothesis spec | (to be authored) | `docs/archive_jan2026/snowflake_null_spec.md` | (new) | **NOT YET WRITTEN** — R2 |

---

## Recovery tasks for Phase 1

- [ ] Copy TIME-FOR-HELP repo contents verbatim into `docs/archive_jan2026/snowflake_source/` with provenance header documenting original repo commit hash and date
- [ ] Copy `crystal_bug_v1_matrix.jsx` similarly
- [ ] Search R16 for the CRYSTALOS log (R1)
- [ ] Once R1 is located: write R2 (null-spec) as a standalone doc, review for statistical soundness
- [ ] Generate or identify R3 (held-out replication dataset)
- [ ] Author R4 (adversarial model)
- [ ] Only after R1–R4 are complete: update PITCH_DRAFT with the actual numbers and send to first funder
