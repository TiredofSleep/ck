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
- [ ] Bibliography cross-check against MathSciNet (AMS MR numbers where
      available)
- [ ] Typographic read by a second party (Luther or Gish)
- [ ] Title polish pass — current title is *"The First-G Event in the
      Coprimality Partition: Stability Windows, CRT Idempotent Count, and
      Prime-Indexed Phase Transitions"* — consider shortening to
      *"The First-G Event in the Coprimality Partition"* for marquee

### Cover letter (template → final)
- [ ] Draft template letter ~330 words, style matching JCAP (venue 7) and
      JCT-A (venue 8) cover letters
- [ ] Location: `Gen13/targets/journals/tier2_format_then_submit/first_g_event/cover_letter_template.md`
- [ ] Addressee: *Integers* managing editor (Douglas S. Bowman, or as
      listed on `www.integers-ejcnt.org` masthead at time of submission)
- [ ] Journal-scope paragraph: "clean combinatorial-number-theory statement
      with elementary proof and exhaustive verification; appropriate for
      *Integers* short-paper track"

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

## Decision

**Sprint 35 is DRAFT-COMPLETE as of 2026-04-19 20:55 and enters the
next-cycle submission window (2026-04-29 or later).** No pre-Wednesday
ship pressure. Manuscript + proof script + README committed now; cover
letter and style polish happen during the following week.
