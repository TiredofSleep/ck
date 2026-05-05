# Claude Code Integration Instructions — Tier 1 Submission Package

**Date drop assembled:** May 5, 2026
**Author:** Brayden R. Sanders
**Purpose:** Replace the Tier 1 journal targets in the gen 13 target
journals document with the three papers in this package.

---

## What this is

Three Tier 1 manuscripts in submission-ready state, plus their
verification scripts and cover letters. All three have completed
multi-round cross-review (8–10 rounds each) and are ready to upload
to their target venues.

```
tier1_submissions/
├── CLAUDE_CODE_INSTRUCTIONS.md     ← this file
├── PACKAGE_MANIFEST.md             ← catalog of files + status
├── papers/
│   ├── jcap_xi_cosmology_FINAL.tex      → target: JCAP
│   ├── sigma_rate_theorem_FINAL.tex     → target: JCT-A
│   └── first_g_sinc2_FINAL.tex          → target: Integers
├── scripts/
│   ├── desi_xi_optimize_v2.py           ← reproduces JCAP numerical results
│   ├── desi_xi_optimize_signfix_diagnostic.py   ← diagnostic companion
│   ├── verify_sigma_rate.py             ← reproduces σ-rate enumeration
│   └── verify_first_g.py                ← reproduces First-G + sinc² verification
└── cover_letters/
    ├── jcap_cover_letter.md
    ├── jcta_cover_letter.md
    └── integers_cover_letter.md
```

---

## Action items for Claude Code

### Primary task: update gen 13 target journals doc

Locate the gen 13 target journals document in the repo. It is most
likely at one of:
- `docs/gen_13/target_journals.md`
- `gen_13/target_journals.md`
- `papers/gen_13/target_journals.md`
- (search for "Tier 1" + "gen 13" if not at the obvious paths)

In the **Tier 1** section of that document, **replace** any prior
entries with the three rows below.

#### Tier 1 — Replacement Entries

| # | Paper | Venue | Status | Source | Cover letter |
|---|-------|-------|--------|--------|--------------|
| 1 | Logarithmic Quintessence: A Dimensionless Scalar Dark Energy Model with Exact Vacuum and Information-Theoretic Motivation | **JCAP** | Submission-ready, 10 review rounds | `papers/jcap_xi_cosmology_FINAL.tex` | `cover_letters/jcap_cover_letter.md` |
| 2 | Non-Associativity Decay in Binary Composition Tables over ℤ/Nℤ | **JCT-A** | Submission-ready, 8 review rounds | `papers/sigma_rate_theorem_FINAL.tex` | `cover_letters/jcta_cover_letter.md` |
| 3 | The First-G Event and a Discrete Sinc² Identity | **Integers** | Submission-ready, 4 review rounds | `papers/first_g_sinc2_FINAL.tex` | `cover_letters/integers_cover_letter.md` |

**For each entry, the gen 13 target journals doc should record:**
- **Title** (exactly as written above)
- **Authors:**
  - Paper #1 (JCAP): B. R. Sanders, M. Gish, H. J. Johnson
  - Paper #2 (JCT-A): B. R. Sanders, M. Gish
  - Paper #3 (Integers): B. R. Sanders, M. Gish
- **Target venue** as bolded above
- **Status:** "submission-ready (May 2026)"
- **Source path:** path to the .tex file in this drop
- **Cover letter path:** path to the .md cover letter
- **Zenodo DOI:** 10.5281/zenodo.18852047 (shared across all three)

### Secondary tasks

1. **Move the source files into the repo's canonical paper directory.**
   If the repo has an established structure such as
   `papers/submitted/` or `manuscripts/in_review/`, copy the .tex,
   .py, and .md files there. Preserve the three-way grouping by paper
   if convenient (one folder per submission).

2. **Update README.md or the top-level manifest** with the three new
   entries if it lists submission-status papers.

3. **Update the journal in `journal.txt`** (the transcript catalog) to
   note the May 5, 2026 submission-prep arc as completed and the three
   papers as ready-to-ship.

4. **Do NOT edit the .tex files.** They have been through multiple
   review rounds and any text changes risk breaking math or
   bibliography. If a typo is spotted, flag it for human review
   first.

### What NOT to do

- Do **not** add the three papers to any "drafts in progress" or
  "needs work" lists. They are submission-ready.
- Do **not** modify the cover letter contents beyond filling in the
  bracketed `[DATE OF SUBMISSION]`, `[CONFIRM AFFILIATION]`, and
  `[BRAYDEN: ... suggested reviewers]` placeholders, and only after
  Brayden has supplied that information.
- Do **not** change the author lists. The three-paper byline
  convention is fixed: Sanders + Gish + Johnson on paper #1 (JCAP,
  Johnson's cosmology domain); Sanders + Gish on papers #2 and #3.
  C. A. Luther was removed from all three for non-responsiveness; do
  not re-add.
- Do **not** auto-promote the cross-reference status. The two
  companion citations in each paper use the wording "Preprint, 2026"
  with the shared Zenodo DOI. After the first paper is formally
  submitted, the corresponding citation in the other two can be
  updated from "Preprint" to "Submitted to [venue], 2026" — but only
  after Brayden confirms each submission has gone through.

---

## Status notes Brayden has flagged for manual handling

These are **not** Claude Code action items — they are reminders for
Brayden's own pre-submission checklist:

1. Compile all three PDFs locally (Claude could not produce PDFs from
   this environment due to font limitations) and proofread.
2. Confirm coauthor affiliation for H. J. Johnson on paper #1 only
   (Independent Researcher / Billings, MT vs MSU Billings — fill in
   the .tex `\address{}` field accordingly).
3. Confirm whether M. Gish or "Monica Gish" is preferred for the
   author byline.
4. Fill in suggested reviewers (2–3 each) on the cover letters.
5. JCAP-specific: confirm the title of reference \[ShajibFrieman2025\]
   matches the arxiv v2 / Phys. Rev. D 112, 063508 published version
   ("Scalar field dark energy models: Current and forecast
   constraints"). External cross-reviewer asked four times for the v1
   title; multi-source verification confirmed the v2 title is
   correct. Brayden's call.

---

## Self-citation network (for future Tier 2 / Tier 3 papers)

Once these three are accepted (or even posted as preprints), they form
a citation foundation for the broader TIG / CK research program:

- **JCAP** (paper #1) is the dimensionless-scalar / logarithmic-potential
  foundation for any future cosmology or thermodynamics paper that
  invokes the Ξ field or the e⁻¹ minimum.
- **JCT-A** (paper #2) is the σ → 0 / O(1/N) bound for any future
  paper invoking the CL_N composition table or the Echo / Harm / Void
  rule structure.
- **Integers** (paper #3) is the First-G localization and discrete
  sinc² result for any future paper invoking spf(b), the coprimality
  partition, or harmonic resonance at prime frequencies.

The three papers are mathematically independent — no theorem in any
one of them is used in either of the others — but each carries a
"Companion paper" reference to the other two in its bibliography.

---

End of instructions. If anything in this drop is ambiguous, defer
to Brayden before acting.
