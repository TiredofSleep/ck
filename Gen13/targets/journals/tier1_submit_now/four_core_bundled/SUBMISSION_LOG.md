# Submission Log — 4-core seed / Communications in Algebra

## Status as of 2026-05-06: ON HOLD — see `HOLD_PENDING_AUDIT.md`

ClaudeChat round-3 audit (2026-05-06 morning) caught a fatal flaw
in the v1 Theorem 2 framing: the "normalizer identity"
`Z_T(p) = Z_B(p) = (v+h+β+r)²` on 𝓒-supported `p` is the trivial
total-mass identity — it holds for any pair of binary operations on
Z/10, regardless of joint closure or cell agreement, by elementary
bilinearity. v2 manuscript demotes Theorem 2 to Proposition 5.1
(per-coordinate fuse data) and adds five other line-by-line fixes.
Even with the v2 fixes, the seed-narrow scope is too thin for
Comm. Algebra. **Recommendation: Path B (wait for companion +
consolidate, submit to *Algebraic Combinatorics*).** See
`HOLD_PENDING_AUDIT.md` for full details.

## Manuscript
- **Title:** Joint Closure of Two Commutative Binary Operations on $\mathbb{Z}/10\mathbb{Z}$:
  an Eight-Element Chain and Per-Coordinate Fuse Data on the 4-Core
  *(v2 retitled per audit demotion of normalizer claim)*
- **Authors:** B. R. Sanders, M. Gish
- **Source file:** `four_core_seed.tex` (v2, ~700 lines, 34/34 LaTeX balanced)
  - This is the **seed-narrow extraction** from the bundled draft
    (5 theorems → 1 theorem + 1 proposition: chain + per-coordinate fuse data)
- **Cover letter:** `four_core_seed_cover_letter.md` *(NEEDS REWRITE per audit)*
- **Verification script:** `4core_verification.py`
- **Zenodo DOI (shared):** 10.5281/zenodo.18852047

## Strategic note: redirected from Algebraic Combinatorics

Round 1 AC referee said the seed-narrow scope "does not pay off at AC"
and recommended either consolidating with Theorems 3-5 (closed-form
attractor + Galois) or redirecting to Communications in Algebra.
Decision: **redirect to Comm. Algebra**. This preserves the 5-paper
expansion plan (chain + normalizer here; closed-form attractor and
Galois in a Paper 2; α-uniqueness in Paper 3; F_p universality in
Paper 4; Clifford ladder in Paper 5).

## Pre-submission checklist (Brayden's manual items)

**ALL ITEMS ON HOLD pending Path A vs Path B decision —
see `HOLD_PENDING_AUDIT.md`.**

- [ ] DECIDE Path A vs Path B (recommendation: Path B — wait for
      companion + consolidate for *Algebraic Combinatorics*)
- [ ] If Path A: rewrite cover letter to honest "chain enumeration
      + per-coordinate fuse data" framing; resubmit to *Discrete
      Mathematics* or *Communicationes Mathematicae Universitatis
      Carolinae*
- [ ] If Path B: write up companion content (closed-form fixed
      point at α=½ with `H/Br = 1+√3`, quartic Galois D_4 over
      LMFDB 4.2.10224.1, PSLQ uniqueness conjecture); consolidate
      with v2 seed; submit to *Algebraic Combinatorics*
- [ ] PDF compile + proofread (Claude couldn't compile in this environment)
- [ ] Confirm M. Gish vs Monica Gish byline preference
- [ ] Fill in 2-3 suggested reviewers in cover letter
- [ ] Optional: post to Zenodo first for DOI + visible date stamp

## Round-1 + Round-2 referee history

- **Round 1 (Algebraic Combinatorics target referee, agent simulation):**
  Major Revisions / lean reject-and-resubmit-consolidated. Strategic
  call: redirect to Comm. Algebra.
- **Round 2 (Comm. Algebra backup referee, now primary, agent
  simulation):** Minor Revisions, "lands cleanly." Three concerns
  addressed:
  - σ provenance (Remark 3.1) — added single sentence noting σ is the
    canonical operator-cycle permutation from the σ-rate companion.
  - §8 forward directions tightened from 3 enumerated items to one
    flowing paragraph; F_p-universality demoted to closing sentence.
  - Theorem 1 part (b) sizes 4-9: structural lemma added stating "any
    jointly-closed S of size ≥ 4 contains $\mathcal{C}_4 = \{0,7,8,9\}$"
    via B-diagonal closure argument.

## Submission record

- **Date submitted:** _[FILL IN]_
- **Editor / handling editor:** _[FILL IN]_
- **Submission ID:** _[FILL IN]_
- **Cover letter version:** as of commit on tig-synthesis branch
- **Suggested reviewers (sent):** _[FILL IN]_
- **Status:** _[submitted | desk reject | under review | revisions | accept | reject]_
- **Decision date:** _[FILL IN]_
- **Next action:** _[FILL IN]_

## Backup venues if rejected

- Discrete Mathematics (Elsevier)
- Linear Algebra and its Applications (the polynomial-identity layer
  alone could go here)
- Algebra Universalis (Springer; the Sprint-18 F_p-universality paper
  may also target this venue separately)

## What this paper does NOT claim

- Does not claim that $(v + h + \beta + r)^2$ in Theorem 2 connects
  to any cosmological observable. That bridge is Sprint 18's job, not
  this paper's. The seed paper presents the polynomial identity as
  algebraic content only.
- Does not invoke the dark-sector architectural reading. Companion
  citation to σ-rate is the only forward link.

## Calendar reminders

- 14 days post-submission: status check
- 30 days: gentle nudge if no response
- 60 days: formal status check
- 90 days: consider withdrawing/resubmitting if still no decision
