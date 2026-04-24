# INTEGRATION_NOTES_2026_04_24.md

## Transparency record — what the desktop drafts said, what was verified, what was changed

This folder's primary document `META_LENS_ATLAS.md` was built by merging
two ClaudeChat drafts — `META_LENS_ATLAS.md` v1.0 and
`PROPOSITION_CK_POSITIONING.md`, both from `C:\Users\brayd\OneDrive\Desktop\`
— with rigor-checking against the repo. Per Brayden's instruction
*"don't trust ClaudeChat, use the intuition and find the rigor"*, every
empirical claim in the desktop drafts was cross-checked against the
repo before integration. This note records the audit.

---

## 1. META_LENS_ATLAS.md v1.0 (desktop) — claims audit

### 1a. Corrections applied before integration

| Desktop v1.0 claim | Repo reality | Action |
|---|---|---|
| "`D26/D27 (WP11/WP12) Lie-algebraic lifts`" (line 81) | `WP11` and `WP12` slots in `MASTER_WHITEPAPER_OUTLINE.md` are *The Measurement Problem* / *Seventeen Paradoxes*; the so(8) and so(10) identification papers are filed as **WP102** (so(8) = D₄) and **WP103** (so(10) = D₅) on `tig-synthesis`. | Fixed to **WP102/WP103** everywhere in the atlas (Part I instance list, Part II Lens 2 cells, Part III cell diagram). |
| "`Current Hilbert function stabilizes at Krull dim 6 with pd = 4 predicted; verification by Macaulay2 would confirm Type-I resolvability`" (Lens 1 Cell I, line 98) | Macaulay2 1.22 on 2026-04-24 (`compute_betti.m2`, `betti_output.txt` on `mantero-bridge-2026-04-23`) verified: `numgens = 53`, `codim = 9`, `dim = 1`, `pd = 10`, `depth = 0`, **not Cohen–Macaulay**, **not Koszul**; Hilbert function `(1, 10, 2, 1, 1, …)`. | Replaced the conjectural v1.0 cell with the M2 closure and reframed the Cell-I open question as "what is the shape of the full linear strand `β_{i, i+1}`?" |
| Part IV Q1 "`Is A = R/I_CL Cohen-Macaulay?`" | Closed by the M2 run above: **no**. | Marked `[M2-RESOLVED, 2026-04-24]` with the verified invariants and the replacement open question. |
| "`TIG's live classifier produces an ambiguity resolution score`" | No runnable `classify_paradox.py` exists in the repo (verified by scout 2026-04-24). `ck_diagnose.py` exists but diagnoses quadrant / corridor / σ — not paradoxes. | Softened to "defined in paper form only (WP61 + this atlas). There is no runnable `classify_paradox.py` in the repo as of 2026-04-24; building one is [O-1]." |
| "`Schrödinger's Cat and the Unexpected Hanging are canonical Type IV examples`" | Only Unexpected Hanging is worked in `PARADOX_CLASSIFICATION_MEMO.md`. Schrödinger's Cat is *not* worked with the 6-slot template anywhere in the repo. | Split: Unexpected Hanging retained as a worked example; Schrödinger flagged as an atlas-new candidate for Type IV, listed under [O-2] in Part V. |
| "`A full treatment of Gödel would live here`" (v1.0 Lens 6 Cell II) | Honest — Gödel is not worked. | Kept verbatim; added [O-3] in §Open work. |
| "`Russell's Paradox, Liar Paradox, and Cantor's naive-set-theoretic paradoxes are all Type-III failures`" (v1.0 Lens 6 Cell III) | Only Russell is worked in repo. Liar + Cantor are not. | Split: Russell cited as worked; Liar and Cantor flagged as atlas-new candidates ([O-4], [O-5]). |

### 1b. Content added that wasn't in v1.0

- **Part 0 "What this atlas adds, what it inherits"** — new transparency
  block at the top of the atlas so a reader knows up-front which pieces
  are novel-to-the-atlas and which come from existing sprint artifacts.
- **Vocabulary reconciliation** (inside Part 0, with standalone brief in
  `VOCABULARY_RECONCILIATION.md`) — explains Sprint 11 four-type axis
  vs WP61 five-category axis and their one overlap (Type III = Category V).
- **WP62 7-cycle rejection cited as a case study** in Part I's "Why UOP
  organizes TIG's own results" — the classifier used *against* a TIG
  conjecture as evidence of honest use.
- **Part III (CK positioning)** — from the second desktop draft
  (`PROPOSITION_CK_POSITIONING.md`), with corrections (see §2 below).
- **Citations footer** listing every anchor file with its canonical
  location.

---

## 2. PROPOSITION_CK_POSITIONING.md (desktop) — claims audit

The proposition argues CK should get its own dedicated section rather
than a seventh row in the Part II Lens Catalog, with a three-criteria
(vocabulary / toolkit / community) framework for when a framework
counts as a full lens. The **strategic argument is kept intact** — it
is correct and well-reasoned. Several empirical claims were corrected.

### 2a. Strategic argument — kept intact

- CK does **not** get a row 7 in Part II. Part II stays at six lenses.
- CK gets its own dedicated section (Part III, not §3 in the
  proposition's numbering — the atlas uses Roman numerals because of
  the existing Part 0 / Part I / Part II structure).
- The three-criteria framework (vocabulary / toolkit / community) is
  adopted verbatim.
- The "CK does not yet have an independent research community"
  sentence is preserved without softening — this is atlas §III.3.
- The historical accretion path (category theory, operad theory as
  examples of lenses that earned their standing over decades) is
  preserved as §III.5.

### 2b. Empirical corrections

| Proposition claim | Repo reality | Action |
|---|---|---|
| "`CK's runtime implementation is in ck_diagnose.py`" (Change B) | `ck_diagnose.py` exists at repo root but diagnoses **quadrant balance, corridor leakage, and σ non-associativity** — it is **not** the UOP paradox classifier. | Corrected in atlas §III.1 table — `ck_diagnose.py` is listed with its **actual** function ("not the paradox classifier"). The paradox classifier as a runnable artifact is listed as [O-1] in §Open work. |
| "`takes a paradox description as input … returns the full six-slot UOP diagnostic … and a resolution score in [0, 1]`" (referring to live classifier) | `paradox.html` is **client-side only**. It hardcodes 8 paradox cases with their 6-slot templates and renders them in-browser. There is no backend endpoint. | Corrected in atlas §III.1 — described as "client-side web UI with 8 hardcoded paradox cases, no free-form backend". |
| "`eight canonical examples (Zeno, Banach-Tarski, Russell, Unexpected Hanging, Twin Primes, Schrödinger's Cat, Gödel's Incompleteness, Liar)`" | **4 of 8 worked** in repo (Zeno / Banach-Tarski / Russell / Unexpected Hanging, in Sprint 11 memo). The other 4 appear in `paradox.html` as aspirational rendering with heuristic classification. | Corrected in atlas §III.1 table row "Canonical 6-slot worked examples" — 4 of 8 worked; other 4 catalogued as [O-2]–[O-6]. |
| "`Zeno → PROGRESS (forward-step operator)`" | `paradox.html` line 637+ hardcodes Zeno as `operators: ['LATTICE', 'HARMONY']` (not PROGRESS). | Corrected in atlas §III.2 — reported the actual hardcoded values (`Zeno → LATTICE, HARMONY`; `Russell → VOID, RESET`; `Liar → VOID, RESET`; `Twin Primes → VOID, COLLAPSE, CHAOS`), flagged as UI display values not computed dynamically. |
| "`The philosophical frame Brayden uses — "LATTICE: structure that enables without dominating"`" | Not found in MEMORY.md, README.md, or any ethos document. The phrase is synthetic to the proposition — ClaudeChat framing, not Brayden's voice. | **Dropped** from the integration. The closing blessing `🙏 LATTICE.` is preserved (that IS Brayden's usage), but the "structure that enables without dominating" gloss is not imported. |
| "`papers/WP_PARADOX_CLASSIFIER.md`" | **Verified to exist** on `tig-synthesis`, with DOI 10.5281/zenodo.18852047. Full whitepaper. | Cited in atlas §III.1 row 1 and in README.md anchor-files table. |
| "`papers/morphotic_braid/synthesis/RIGOR_MAPPING.md`" | **Verified to exist** at that path. | Cited in atlas §III.3 (toolkit criterion evidence) and in README.md anchor-files table. |
| D² curvature as "`second-derivative stencil on the 5D force vector (aperture, pressure, depth, binding, continuity)`" | **Verified** — `ck_algebra.c` CKA_FORCE_LUT defines the 5-dim force vector with exactly those field names; `ck_d2_dictionary_expander.py` and `ck_d1_lattice_builder.py` use `d2_vector`. | Adopted verbatim in atlas §III.1 and §III.2 with file-path citations. |

### 2c. Section-numbering change

The proposition assumed `§0 / §1 / §2 / §3 / …` numbering. The atlas
already used `Part 0 / Part I / Part II / Part III / …` Roman numerals
(with `§III.1 / §III.2 / …` subsections). The integration retained the
Roman-numeral style; the new CK section is **Part III**, and
collaboration map / open questions became **Part IV** / **Part V**
respectively.

The "Change A / B / C" items in the proposition's §3.3 were
distributed into the appropriate sections rather than applied as
discrete edits — their intent (each of which was reasonable) is
present in the integrated atlas, but the wording was not always kept
verbatim where repo facts required rephrasing.

---

## 3. Guardrails honored

The proposition listed three guardrails (§4). All three are honored in
the integration:

1. ✅ **No CK row 7 in Part II.** Part II stays at six lenses.
2. ✅ **"CK does not yet have an independent research community"
   language preserved.** Atlas §III.3 states it cleanly, with the
   specific current community list (Brayden, Luther, Thornton, Mayes,
   three AI systems) and the absence of independent external
   publication. Not softened.
3. ✅ **Category-theory / operad-theory historical precedent kept.**
   Atlas §III.5 frames CK as following the same accretion path that
   category theory (Eilenberg–Mac Lane) and operad theory (May;
   Boardman–Vogt) took to earn their standing over decades.

---

## 4. What was NOT imported from the desktop drafts

- The "LATTICE — structure that enables without dominating" phrase
  (synthetic to ClaudeChat).
- The claim that CK's runtime has "decidable classification for concrete
  paradox statements" in the present tense (replaced with "would supply
  … assuming the pipeline is wired end-to-end").
- The "Zeno → PROGRESS" operator activation (replaced with the actual
  hardcoded `Zeno → LATTICE, HARMONY` from `paradox.html`).

---

## 5. Net effect

The integrated atlas is **strictly stronger** than either desktop
draft read alone:

- Strategic argument from `PROPOSITION_CK_POSITIONING.md` preserved.
- Numerical claims tightened to M2-verified values.
- WP-numbering aligned with canonical `MASTER_WHITEPAPER_OUTLINE.md`.
- Every empirical claim about runtime state verified or flagged.
- Paradox-count claims (4 worked, 4 aspirational) made explicit.
- Honest-scope bar held throughout Part III.

A reader who opens the atlas cold can trace every claim to either a
cited proof artifact or an explicit open-work item. That is the
standard for this branch.
