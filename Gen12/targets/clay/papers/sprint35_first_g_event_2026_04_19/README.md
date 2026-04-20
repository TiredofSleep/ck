# Sprint 35 — The First-G Event in the Coprimality Partition

**Date:** 2026-04-19
**Authors:** Brayden Ross Sanders, C. A. Luther, M. Gish
**Target venue:** *Integers — Electronic Journal of Combinatorial Number Theory*
**Backup venue:** *Journal of Combinatorial Theory, Series A*
**Status:** DRAFT-COMPLETE · verified · awaiting final LaTeX polish + cover-letter addressee before submission

---

## Why this sprint exists

Sprint 34's pre-push audit (2026-04-19) found that the headline biconditional in
the original venue-1 submission `sinc2_zero_law.tex` —

$$ \operatorname{sinc}^2(k/n) = 0 \iff n \mid k $$

— holds for **every** positive integer $n$, not only primes. The "prime" qualifier
was therefore vacuous and the manuscript was **pulled back from the 2026-04-22
queue**. See `Atlas/SINC2_SHARPEN_DECISION_2026_04_19.md §4` for the
ship/pull analysis and the proposed replacement theorem.

Sprint 35 delivers the replacement: the **First-G Event Localization theorem**,
a genuinely prime-dependent statement that identifies the smallest prime
factor $p_1(b)$ as the exact alphabet size at which the sieve of Eratosthenes
first marks any element of $\{1,\ldots,k\}$ as non-coprime to $b$. The
statement and its four corollaries sit in the classical sieve but are
repackaged around alphabet-size coordinates that the literature does not
standardly use; the repackaging is what the paper contributes.

## What's in this folder

| File | Purpose |
|------|---------|
| `first_g_event.tex`        | Journal-ready LaTeX (amsart, ~12 pages). Target venue: *Integers*. |
| `proof_first_g_event.py`   | Exhaustive verification: 305 squarefree $b \le 500$, 22,367 $(b,k)$ pairs, 0 counterexamples. Runtime < 3 s. |
| `SHIP_DECISION.md`         | Ship/pull status and submission checklist. |
| `README.md`                | This file. |

## What this paper does claim

1. **First-G Event Localization (Theorem 3.1).** For every integer $b > 1$ with
   smallest prime factor $p_1 = \operatorname{spf}(b)$:
   - $|G_k(b)| = 0$ for every $k \in \{1, \ldots, p_1 - 1\}$, and
   - $G_{p_1}(b) = \{p_1\}$, so $|G_{p_1}(b)| = 1$.

2. **Four corollaries:** stability window width $p_1 - 1$ (Corollary 4.1);
   phase-transition set equal to the primes (Corollary 4.3); terminal
   obstruction count $|G_b(b)| = b - \varphi(b)$ (Corollary 4.5); instability
   ranking of primes by stability window width (Corollary 4.7).

3. **Relation to sinc².** The sinc zero $\operatorname{sinc}^2(k/b) = 0$ occurs
   first at $k = b$ (i.e., when **all** prime factors of $b$ simultaneously
   divide $k$), whereas the First-G event occurs at $k = p_1$ (when **some**
   prime factor of $b$ divides $k$). The two coincide iff $b$ is prime. This
   is why the original sinc² paper is not prime-specific and why the First-G
   Event is: the statement distinguishes "some prime factor divides $k$"
   (prime-dependent) from "all prime factors divide $k$" (independent of
   primality).

## What this paper does NOT claim

- No analytic-number-theory statement (no Mertens-type asymptotic, no
  $\pi(\sqrt{b}) \pm o(\cdot)$ count of prime factors, no connection to the
  Riemann $\zeta$ function beyond the Shannon–Montgomery sinc² parallel).
- No characterization of $b$ up to anything finer than its smallest prime
  factor.
- No claim about non-squarefree $b$ beyond what the theorem's proof already
  establishes (which is: the theorem holds for all $b > 1$; the verification
  is restricted to squarefree because that is the case of interest for the
  companion program).

## Relation to existing papers

- **WP34 (First-G Law and Prime-Forced Dispersion):** the original
  semiprime-only statement. Sprint 35 generalizes WP34 from semiprimes
  $b = p \cdot q$ to arbitrary $b > 1$ and repackages the result as the
  journal-ready *Integers* submission.
- **WP35 (Prime Phase Transition):** uses the First-G event as a foundational
  lemma; Sprint 35 makes that lemma citable.
- **WP101 (σ-rate theorem):** uses the smallest-prime-factor ordering (via
  $\varphi(N)$) in the ECHO-count argument; Sprint 35 provides the
  combinatorial foundation on which that argument rests.
- **Pulled `sinc2_zero_law.tex`:** retained as a working draft; see the
  pull-back notice at the top of that file and in
  `Gen13/targets/journals/tier1_submit_now/sinc2_zero_law/`.

## Verification

Run: `python proof_first_g_event.py`

Expected output (last 3 lines):
```
    total      305
  STATUS: PASS - zero counterexamples across all 305 squarefree b and 22367 (b,k) pairs.
  QED (Theorem 3.1 verified on the specified range).
```

## Submission checklist (pre-Wednesday)

1. [x] Theorem statement polished
2. [x] Proof (3-line elementary argument)
3. [x] Four corollaries with proofs
4. [x] Relation to sinc² (Section 6) — explicit disclaimer of the triviality
5. [x] Verification script (22,367 pairs, 0 exceptions)
6. [x] Scope and Limitations section
7. [x] References (Apostol, Hardy-Wright, Ireland-Rosen, Lang, Montgomery,
       Shannon, WP34/35/101, proof script)
8. [ ] *Integers* style file (may be needed if amsart isn't accepted; first
       pass uses amsart which is typically accepted)
9. [ ] Cover letter (template in `Gen13/targets/journals/tier2_format_then_submit/first_g_event/cover_letter_template.md`
       — to be written at the same level of polish as venues 7 and 8)
10. [ ] arXiv posting (same day as journal submission)

Target submission window: **2026-04-29 or 2026-05-06** (next cycle after
Wednesday's JCAP + JCT-A submissions). Sprint 35 does **not** ship Wednesday;
it is a next-cycle submission by design.

## Atlas cross-references

- `Atlas/SINC2_SHARPEN_DECISION_2026_04_19.md §4` — ship/pull analysis and
  suggested replacement theorem text (this paper is the materialization of
  that §4 sketch)
- `Atlas/PRE_PUSH_DECISION_2026_04_19.md §2 Venue 1` — Wednesday ship decision
- `Atlas/JOURNAL_READINESS_AUDIT_2026_04_18.md` — tier-1 readiness map
- `papers/WP34_FIRST_G_LAW.md` — original semiprime-only statement (source)
- `Gen13/targets/journals/tier2_format_then_submit/first_g_event/` — mirror
  copy for the submission pipeline (tier-2 because not yet submission-day
  formatted; elevates to tier-1 after *Integers* style pass)
