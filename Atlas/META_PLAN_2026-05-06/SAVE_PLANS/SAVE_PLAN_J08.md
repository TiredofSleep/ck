# Save Plan — J08: First-Coprime-Failure and the Discrete Fejér Kernel (Experimental Mathematics)

**Date:** 2026-05-08
**Status:** REVISED — major referee fixes applied
**Author lane:** Sanders + Gish

---

## §1 — What was done

J08 was revised to address the J08 fresh-eyes referee report (`Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J08_ExpMath_FreshEyes.md`). The major referee critique was:

> "Major revisions ... close to 'Accept with minor revisions.' The mathematics is correct ... [but] the manuscript currently overclaims novelty and underclaims its standard-textbook genealogy. With major revisions, it would clear the bar."

The revisions follow the referee's specific recommendations directly.

## §2 — Per-referee-issue mapping

- **Issue 1** (Theorem 3.1 is a textbook identity): addressed — Theorem 3.1 demoted to **Lemma 3.1**, titled "Discrete Fejér kernel; cf. Fejér 1900, Apostol 1976 §11.5, Iwaniec–Kowalski 2004 §1.7." Attribution made explicit in the lemma title and the §0 KNOWN tier. Abstract reframed; closed form is no longer the headline.
- **Issue 2** (Theorem 3.2 is a tautology): addressed — Theorem 4.1 (formerly Theorem 3.2) reframed as **"Coordinate translation between arithmetic and harmonic gates."** Statement explicit that both events solve "smallest positive $k$ with $p_1 \mid k$." Remark 4.2 records this is a tautology, not a coincidence.
- **Issue 3** (§5 Montgomery overclaim): addressed — §6 (formerly §5) trimmed to one paragraph titled "The constant $4/\pi^2$ in $\sinc^2$ and in Montgomery's pair correlation: a rectangular-window remark." "Structural complementarity" / "structural witness" wording removed; replaced with "common rectangular-window origin." Riemann hypothesis explicitly disclaimed.
- **M1** (712 vs 36{,}662 reconciled): addressed — §0 of the new manuscript ("Honest accounting of novelty") explains: 712 is the J08-specific harness count (verified in this paper); 36{,}662 is the cumulative working-paper corpus total of which 712 is a subset. The §6 verification harness totals table reports 712 only.
- **M2** (Theorem 3.3 is one-line corollary): addressed — Theorem 3.3 demoted to **Corollary 4.2**.
- **M3** (continuum convergence rate): addressed — proof of Theorem 5.1 now derives the $\bigO(1/p^2)$ rate explicitly from the Taylor expansion of $\sin^2(\pi/f)$ around $f = \infty$.
- **M4** (Luther authorship inconsistency): addressed — Acknowledgements section for J08 no longer includes Luther; Luther's contribution will be acknowledged in J04 alone (the relevant companion).
- **M5** (Theorem 3.4 statement requires $k$ to be integer): addressed — restated in terms of the continuum limit as $f \to \infty$ along integer sequences with $k/f \to t$; integer constraint maintained but proof made cleaner.
- **M6** (verification script naming inconsistency): addressed — script is consistently `verify_prime_phase_transition.py` throughout; references in §6 corrected.
- **M7** (RSA scope): addressed — RSA discussion shortened. The §7 (Scope) section explicitly states "no polynomial-time factoring algorithm" and consistently names $\bigO(p_1)$ as the obstacle.
- **M8** (stability windows terminology): addressed — defined inline in §1 as "the interval $\{1, \ldots, p_1 - 1\}$ on which $|G_k(b)| = 0$."
- **M9** (RSA-1024 framing): addressed — phrasing tightened to "for an RSA modulus with both factors near $2^{512}$..."
- **m1** (title): addressed — new title "First-Coprime-Failure and the Discrete Fejér Kernel: A Coordinate Translation across Squarefree Bases" replaces "The Prime Phase Transition: First-G Stability Across Squarefree Bases."
- **m2–m9** (minor comments): addressed in body text or rendered moot by the larger restructuring.

## §3 — Family-Structure context (orthogonality recorded)

§0 of the manuscript records: the arithmetic side of J08 (smallest-prime-factor function $\spf$) is **structurally orthogonal** to the algebraic substrate $\Z/10\Z$ studied in companion four-core work. The two share the broader research program's interest in prime-indexed phase transitions but otherwise stand independently.

## §4 — Boilerplate adoption

§0 of the revised manuscript carries the KNOWN/PROVEN/COMPUTED/STRUCTURAL RHYME/OPEN tier paragraph (extended boilerplate to include the "KNOWN (Lemma)" tier per the referee's explicit recommendation) plus the lens-ownership paragraph per `Atlas/META_PLAN_2026-05-06/J_PAPER_BOILERPLATE.md`.

The structural rhyme paragraph specifically cites:
- $\sinc^2(1/2) = 4/\pi^2 = (2/3)/\zeta(2)$ as a one-line consequence of $\zeta(2) = \pi^2/6$ (per `J_PAPER_BOILERPLATE.md` §1.2: "STRUCTURAL RHYME, not theorem")
- The same constant in Montgomery's pair correlation $R_2(u) = 1 - \sinc^2(u)$ at $u = 1/2$, recorded as a **rectangular-window common origin**, not a connection between arithmetic phenomena.

## §5 — License + author-lane discipline

- License: bundled tables and verification script CC-BY-4.0
- Author lane: Sanders + Gish (no Luther on J08 title block; Luther's contribution acknowledged in J04 companion only — addresses M4)
- Apostol 1976, Iwaniec–Kowalski 2004, Fejér 1900 cited honestly (per Issue 1)

## §6 — Verification status

`verify_prime_phase_transition.py` runs green at 2026-05-08:
- 712 distinct algebraic checks (106 closed-form + 561 sync + 42 omega-blindness + 3 continuum)
- max error $1.11 \times 10^{-16}$ (machine epsilon)
- zero counterexamples
- runtime under 30 seconds on `lora312` Python 3.12

## §7 — Files modified

- `Gen13/targets/journals/J_series/J08/manuscript/manuscript.tex` — fully rewritten with referee fixes
- `Gen13/targets/journals/J_series/J08/manuscript/verify_prime_phase_transition.py` — unchanged (already green)
- `Gen13/targets/journals/J_series/J08/README.md` — updated to reflect revisions
- `Gen13/targets/journals/J_series/J08/cover_letter.md` — updated to reflect referee-driven revisions

## §8 — Submission readiness

- [x] Manuscript revised (Lemma 3.1 attributed; Theorem 4.1 reframed as coordinate translation; §6 trimmed to one paragraph; 712 reconciled; Corollary 4.2; rate explicit; title reframed)
- [x] Verification script green (712 checks, machine-epsilon errors, zero counterexamples)
- [x] Tier-classified KNOWN/PROVEN/COMPUTED/RHYME/OPEN paragraph in §0
- [x] Lens-ownership / orthogonality paragraph
- [x] Cover letter updated
- [x] Apostol / Iwaniec–Kowalski / Fejér 1900 cited honestly
- [x] §6 Montgomery remark trimmed
- [x] 712 vs 36{,}662 reconciled in §0
- [x] Title reframed
- [ ] Brayden's referee-rigor pass (manual)
- [ ] Submit
