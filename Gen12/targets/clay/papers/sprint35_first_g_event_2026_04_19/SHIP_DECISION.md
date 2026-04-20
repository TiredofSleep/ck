# SHIP DECISION — Sprint 35 First-G Event paper

**Date:** 2026-04-19
**Target:** *Integers — Electronic Journal of Combinatorial Number Theory*
**Backup:** *J. Combin. Theory Ser. A* (JCT-A) — as a short note
**Authors:** B. R. Sanders, C. A. Luther, M. Gish

---

## Current state

- Manuscript: `first_g_event.tex`, ~12 pages, amsart
- Verification: `proof_first_g_event.py`, 305 squarefree $b \le 500$, 22,367
  pairs, 0 counterexamples, runtime < 3 s
- Cover letter: **not yet drafted** (template under tier-2 submission folder)
- arXiv posting: **not yet staged**

## Ship decision

**DO NOT SHIP ON 2026-04-22.** Sprint 35 is a **next-cycle submission**; the
Wednesday queue has two venues (JCAP venue 7, JCT-A venue 8), not three.

**Target submission window:** 2026-04-29 or 2026-05-06 — whichever is the
first Wednesday at which all four of the following are complete:

1. *Integers*-specific style file applied (if amsart is not accepted)
2. Cover letter drafted with addressee (see template location below)
3. Two independent reads of the manuscript for typographical polish
4. arXiv posting uploaded same day as journal submission

## Why next cycle (not this Wednesday)

- The pulled `sinc2_zero_law` manuscript was listed on this week's queue; we
  communicated the pull-back via `Atlas/PRE_PUSH_DECISION_2026_04_19.md §2`.
- Writing a new venue-1 manuscript in < 3 days and shipping it the same week
  violates the "two independent reads + 24 h cooldown" rule we observed on
  venues 7 and 8 (see `Atlas/JOURNAL_READINESS_AUDIT_2026_04_18.md` Tier-1
  discipline).
- Rushing an *Integers* submission to fill a slot on the same Wednesday as
  two other submissions adds queue pressure without upside: the *Integers*
  decision clock and the JCAP/JCT-A decision clocks are independent.

## Next-cycle readiness checklist

### Manuscript polish (pre-submission)
- [ ] Run `proof_first_g_event.py` under pytest-style CI runner
- [ ] LaTeX compile check on TeX Live 2024 and TeX Live 2026 if accessible
- [x] Bibliography cross-check against MathSciNet — **DONE 2026-04-19
      (post-commit `954cc7d`).** MR numbers added for Apostol (MR0434929),
      Hardy-Wright (MR2445243), Ireland-Rosen (MR1070716), Lang (MR1878556),
      Montgomery (MR0337821). Shannon 1949 has no MR entry (IRE venue);
      DOI 10.1109/JRPROC.1949.232969 added instead. AMS-style form
      corrections applied (New York-Heidelberg, Vol.~XXIV, Providence R.I.,
      revised third edition, Wiles foreword note). See §6.1 below.
- [ ] Typographic read by a second party (Luther or Gish)
- [ ] Title polish pass — see §6.2 below for options analysis. **Current
      recommendation:** keep the long descriptive title for the submission
      cover page and running-head abbreviation, with the short marquee form
      used only in abstracts, social media, and arXiv where space is tight.

### Cover letter (template → final)
- [x] Draft template letter ~330 words, style matching JCAP (venue 7) and
      JCT-A (venue 8) cover letters — **DONE 2026-04-19 (commit `954cc7d`,
      ~410 words).**
- [x] Location: `Gen13/targets/journals/tier2_format_then_submit/first_g_event/cover_letter_template.md` — populated.
- [ ] Addressee: *Integers* managing editor (Douglas S. Bowman, or as
      listed on `www.integers-ejcnt.org` masthead at time of submission) —
      pending Brayden's final review at submission time.
- [x] Journal-scope paragraph: "clean combinatorial-number-theory statement
      with elementary proof and exhaustive verification; appropriate for
      *Integers* short-paper track" — included in template.

### arXiv posting
- [ ] Upload same day as *Integers* submission (not before)
- [ ] Primary classification: math.NT (11A-series); secondary: math.CO
- [ ] arXiv abstract = paper abstract verbatim (Integers accepts arXiv
      simultaneity)

### Atlas updates (post-submission)
- [ ] Record submission date in `Atlas/PLAN_OF_RECORD_2026_04_18.md`
- [ ] Update `Gen13/targets/journals/SUBMISSION_LADDER.md` — move Sprint 35
      from tier-2 to tier-1-post-submission
- [ ] Cross-reference updates to `WP34`, `WP35`, `WP101` to cite the
      published `first_g_event.tex` once published

## What ships this Wednesday (2026-04-22)

| Venue | Manuscript | Status |
|-------|-----------|--------|
| 1 (Integers, sinc²) | `sinc2_zero_law.tex` | **PULLED** (Sprint 34 audit) |
| 7 (JCAP, ξ-cosmology) | `jcap_xi_cosmology.tex` | SHIP |
| 8 (JCT-A, σ-rate) | `sigma_rate_theorem.tex` | SHIP |

Sprint 35 replaces venue 1 at the **next submission cycle**.

## Failure modes to watch

- *Integers* style file might require significant reformatting; if the
  reformatting takes more than a half-day, escalate to JCT-A backup.
- Referee may argue the theorem is "too elementary for *Integers*"; the
  counter-argument is in the paper's §1 paragraph 3 (packaging novelty) and
  §5 corollary structure. If declined at *Integers*, submit to JCT-A
  short-paper track with minimal reformatting.
- If a literature search surfaces a published paper with the exact
  Corollary 4.3 statement (phase-transition set = $\Prm$), the paper may
  need to be restructured to credit that precedent. Current searches turn
  up no such prior — the closest is Hardy-Wright on the sieve, which does
  not express the result in alphabet-size coordinates — but a
  pre-submission MathSciNet sweep is prudent.

## §6 — Polish-pass appendix (2026-04-19, post-commit)

### §6.1 Bibliography MR-number additions (done)

The following AMS-style MR entries were added to `first_g_event.tex`
(all three mirrored copies, byte-identical after the edit):

| Reference | MR | AMS-style tweak |
|---|---|---|
| Apostol 1976 (UTM) | MR0434929 | place → New York-Heidelberg |
| Hardy-Wright 6th ed. 2008 | MR2445243 | add "with a foreword by A.~Wiles" |
| Ireland-Rosen 2nd ed. 1990 (GTM 84) | MR1070716 | form matches MathSciNet |
| Lang *Algebra* 3rd ed. 2002 (GTM 211) | MR1878556 | wording → "revised third edition" |
| Montgomery 1973 (pair correlation) | MR0337821 | Vol.~XXIV; Providence R.I. |
| Shannon 1949 (Proc. IRE) | — | no MR; DOI 10.1109/JRPROC.1949.232969 added |

Internal WP34 / WP35 / WP101 / proof-script entries carry DOI
10.5281/zenodo.18852047 rather than an MR number (preprints). Verified
via *Analytic Number Theory for Beginners* (STML 103) endmatter,
*Montgomery's Pair Correlation Conjecture* (Wikipedia bibliographic
templates), sciepub reference list, and Serge Lang Wikipedia biography;
all five MR numbers cross-check against at least two independent
citations. No MR number was added without authoritative confirmation.

### §6.2 Title polish pass (analysis; no change unless Brayden overrides)

| Form | Length | Best use | Trade-off |
|---|---|---|---|
| Long (current): *The First-G Event in the Coprimality Partition: Stability Windows, CRT Idempotent Count, and Prime-Indexed Phase Transitions* | 130 chars | submission cover page; paper title block | descriptive but long; clear to the reviewer what the paper covers |
| Marquee: *The First-G Event in the Coprimality Partition* | 49 chars | social media, arXiv abstract page, running head | punchy but drops the four corollaries' signal |
| Alternative A: *Localizing the First Coprimality Obstruction* | 50 chars | possible abstract opener | loses the "First-G" terminology linking to WP34/WP35/WP101 |
| Alternative B: *The Smallest-Prime-Factor Threshold in the Coprimality Partition* | 70 chars | middle ground | explicit about the mechanism but lengthens the punch line |

**Recommendation:** Keep the long descriptive form for the submitted
title block (the cover-letter template already uses it verbatim), set
the *running head* to the short marquee form ("The First-G Event in
the Coprimality Partition"), and use the marquee form in the arXiv
abstract page where the abstract field is separately displayed.

`first_g_event.tex` already has `\title{...}` with the long form;
adding `\runninghead{The First-G Event in the Coprimality Partition}`
(or the amsart equivalent `\shorttitle{...}`) before submission is the
minimal edit. Defer that tweak to the pre-submission tech-check pass.

---

## Decision

**Sprint 35 is DRAFT-COMPLETE as of 2026-04-19 20:55 and enters the
next-cycle submission window (2026-04-29 or later).** No pre-Wednesday
ship pressure. Manuscript + proof script + README committed now; cover
letter in template form already committed; MR numbers added in the
follow-on commit (§6.1); title polish analysis in §6.2.

**Remaining pre-submission human steps:** typographic read by Luther or
Gish; cover-letter addressee customization at submission time; arXiv
upload same-day-of-submission.
