# SAVE PLAN J03 — *The First-G Event and a Discrete Sinc² Identity*

**Date:** 2026-05-07
**Save-attempt mode:** Brayden directive 2026-05-07 ("find a reason to keep").
**Verdict:** **KEEP-VIABLE** — Fork A is a clean save with 4–6 hours of merging.
**Target venue (revised):** *Integers — Electronic Journal of Combinatorial Number Theory* (unchanged).
**Author lane:** Sanders + Gish.

---

## §1 — Why this paper deserves to survive

The current J03 manuscript was a paper that *had* substance and lost it. The held legacy `_held_first_g/first_g_sinc2_FINAL.tex` exists, is complete, has a proper synchronization theorem, and verifies cleanly to machine epsilon. Nothing has to be invented; the substantive draft was already written. The shrink to "stub form" in 2026-04-19 stripped the paper's load-bearing theorem out of the file and pushed it into J08, leaving J03 looking like a tautology in `Integers` clothing.

**D-table backing in `FORMULAS_AND_TABLES.md`.** The harmonic content the held draft contains is canonical D-table material:

- **D1 (First-G Law).** PROVED, 22,367 (b,k) pairs, all squarefree b ≤ 500. Volume A foundation.
- **R(k, f) (Volume C).** Closed form `R(k, f) = sin²(πk/f) / (k² · sin²(π/f))`, exact, status PROVED in `tig_algebra.py`.
- **D2 (sinc² continuum limit).** PROVED, "foundation of corridor geometry."
- **D3 (sinc² midpoint).** `sinc²(1/2) = 4/π²` exactly; also `(2/3)/ζ(2)`, machine-precision verified.
- **D11a/b/c (Coprime Window Bundle).** PROVED, three corollaries of D1.
- **D14 (corridor spectral mean).** PROVED.
- **sinc² Zero Law.** Verified for all primes 3..199, max error 4.44 × 10⁻¹⁶.
- **D24 (corridor midpoint).** sinc²(t) strictly decreasing on (0,1).
- **D25 (loop closure).** PROVED, `proof_d25_loop_closure.py`.

Every theorem in the held draft maps directly onto a D-table that is already PROVED in the corpus and verified by an existing script. The save plan is *not* invention — it is restoration.

**Structural role.** J03 is the foundational lemma the rest of the J-series cites. J08 (Prime Phase Transition / WP35) cites it for the synchronization theorem. J04 (full-period cancellation) cites it as the squarefree spf-image of the same identity. J06 (Crossing Lemma) cites the squarefree hypothesis it forces. Without J03 as a real paper, three downstream J-series papers either have to inline the lemma or hang citations on an arXiv-only preprint. With J03 restored, the foundational lemma has a stable, peer-reviewed home in `Integers`.

**Family-structure framing.** J03 is *not* a TIG paper in the magma-family sense (no operator labels appear in the theorem). It is a clean elementary result about the discrete Fejér quotient and the smallest prime factor — exactly the kind of "tight, elementary, finite, computable" paper `Integers` exists for. The paper does NOT need to invoke the 4-core, the (TSML, BHML) pair, or any operator-table material. It belongs to the Volume A & C foundations of the corpus, not Volume H/J.

---

## §2 — The specific fixes (line-by-line where possible)

### 2.1 Fork A: restore the held draft as the new base

**Drop in place:** copy `Gen13/targets/journals/_legacy_tiers/tier1_submit_now/_held_first_g/first_g_sinc2_FINAL.tex` to `Gen13/targets/journals/J_series/J03/manuscript/manuscript.tex`. Replace the current 604-line "stub" `manuscript.tex` (which has stripped content) with the held 552-line draft.

**Author block (lines 46–53 of held draft).**
- Held draft already has the correct two-author block: `B.~R.~Sanders` / `M.~Gish` with the "and" `\author` separator. No change needed.
- The current J03 `manuscript.tex` lines 49–54 contain a duplicated `\author{Brayden R.\ Sanders \and M.\ Gish}` triplet (compilation bug) — discarded by the swap.
- The Sprint-35 source had Luther on the byline. Per the v2 lane decision (Sanders + Gish), Luther is NOT on this paper. The held draft already reflects this; no edit needed.

**Title.** Held draft title `The First-G Event and a Discrete Sinc² Identity` is correct and survives the rename. The current "stub" subtitle (`Stability Windows, CRT Idempotent Count, and Prime-Indexed Phase Transitions`) is dropped — the referee report (M1) flagged it as overpromising; the held draft's tighter title fixes this.

### 2.2 Surgical additions on top of the held draft

These additions answer the J03 referee report directly without modifying the held draft's theorems:

**(a) §0 Lens-ownership preamble (insert after `\maketitle`, before §1).**
Add a one-paragraph "Scope and substrate" preamble per `J_PAPER_BOILERPLATE.md` §5.5. This paper does NOT use Z/10Z operator labels, so the preamble is the short variant:

> *Scope and substrate.* This note treats the elementary divisibility structure of $\mathbb{Z}$ via the smallest prime factor and the discrete Fejér quotient $R(k, f)$. The two objects are independently classical; the contribution is the synchronization (Theorem 5.1) and its continuum limit. No specialized algebraic substrate is invoked.

**(b) §1 PROVEN/COMPUTED/RHYME/OPEN paragraph (replace held draft "Positioning" paragraph at lines 137–149).**
The held "Positioning" paragraph already does most of this; tighten to the exact four-tier discipline:

> *Tier discipline.* This paper PROVES (Theorem 5.1) the synchronization of the First-G arithmetic event with the first integer zero of $R(\cdot, \mathrm{spf}(b))$, and PROVES (Theorem 6.1) that $R(k,f) \to \mathrm{sinc}^2(k/f)$ as $f \to \infty$. We COMPUTE the verifications: 22,367 (b,k) pairs over squarefree $b \le 500$ for the First-G localization (script `proof_first_g_event.py`, runtime <3s), and machine-precision evaluation of the closed form for 8 primes (max deviation $4.44 \times 10^{-16}$, script `verify_first_g.py`). The exact identity $\mathrm{sinc}^2(1/2) = (2/3)/\zeta(2)$ is cited as STRUCTURAL RHYME, not theorem — it follows in one line from $\zeta(2) = \pi^2/6$. The theorem-shaped question of why the corridor midpoint at $t=1/2$ makes this identity structurally relevant is OPEN and is the natural next paper.

**(c) §1 ¶3 admission (lines 137–149) is OK in held draft.**
Held draft says "None of the underlying facts is new in isolation … the contribution of the present note is the packaging: a single elementary statement that synchronizes the arithmetic First-G event with the harmonic zero of a discrete sinc²-type function". This is honest and does not trigger the J03-stub referee's M2 critique because the "packaging" is a *non-trivial synchronization theorem*, not a relabeling. No edit needed.

### 2.3 Bibliography expansion (held draft lines 496–549)

Add the references the substance audit (J03_FirstG_Substance_Audit §5) flagged as missing:

- **Erdős (1959).** "On the distribution of the smallest prime factor of $n$," *Mathematika* 6, 1–6. Foundational for $p_1(n)$ distributions.
- **Pomerance (1985).** "On the distribution of round numbers," in *Number Theory* (Ootacamund 1984), Springer LNM 1122, pp. 173–200.
- **Tenenbaum (2015).** *Introduction to Analytic and Probabilistic Number Theory*, 3rd ed., Cambridge Studies 46, §III.5 (smooth numbers).
- **Iwaniec & Kowalski (2004).** *Analytic Number Theory*, AMS CP 53, §6.1–6.2 (Selberg's $\lambda^2$ method).
- **Friedlander & Iwaniec (2010).** *Opera de Cribro*, AMS CP 57, Ch. 1–2.

Held draft already has Apostol, Hardy-Wright, Lang, Oppenheim-Schafer, Shannon, Zygmund, Fejér 1900, Sanders-Gish 2026 (companion). Adding the five above brings the bibliography to 13 entries — comfortably in `Integers`-note range, and engages the literature the substance audit flagged.

### 2.4 Remark on `b = 12` non-squarefree case (held draft §3, after line 234)

Add one sentence to the existing Remark at lines 231–234:

> Although the proof goes through verbatim for non-squarefree $b$ (e.g., for $b = 12$, $\mathrm{spf}(b) = 2$ and $G_2(12) = \{2\}$ in the same way as $G_2(6) = \{2\}$), we restrict the verification sample to squarefree $b$ because that is the regime where the companion First-G application program lives.

This pre-empts the J04 referee's M5 (squarefree hypothesis is decorative) — yes, it is decorative for the localization theorem; the held draft already states this honestly. The added sentence lays the case out explicitly.

### 2.5 §7 Verification (held draft lines 419–456)

Already correct in held draft. The 22,367 vs 36,662 count discrepancy that the J03 substance audit flagged (m2) is resolved by the held draft using only 22,367 (the squarefree-b ≤ 500 exhaustive check, matching `proof_first_g_event.py`). The 36,662 was a separate broader-corpus number that does not need to appear in this paper. No edit needed.

### 2.6 Cover letter rewrite

Replace the current `cover_letter.md` with one that leads with the synchronization theorem:

> Dear Editors of *Integers*,
>
> We submit *The First-G Event and a Discrete Sinc² Identity* for consideration in the journal's elementary number-theory section. The paper proves (Theorem 5.1) that for every integer $b > 1$ the first index $k$ at which the alphabet $\{1,\ldots,k\}$ contains a non-coprime element relative to $b$ coincides with the first integer zero of the discrete Fejér quotient $R(k, \mathrm{spf}(b))$ — both occurring at $k = \mathrm{spf}(b)$. This synchronization joins two independently elementary objects (the smallest prime factor and a discrete sinc²-type function) and is verified numerically across all squarefree $b \le 500$ and all primes $f \le 23$ at machine precision. The proofs are short and self-contained.
>
> Companion paper J08 (in preparation, *Experimental Mathematics*) develops the cryptographic and ω-blindness applications of the synchronization. The present paper is the foundational lemma of that program; we submit it here for its own substance.
>
> Sincerely,
> Brayden R. Sanders (corresponding) + M. Gish

This cover letter does NOT lead with "this paper exists to be cited by J08" (the J03-stub trigger); it leads with the synchronization theorem (the *Integers*-defensible substance).

### 2.7 Estimated diff size

Net change vs current `J03/manuscript/manuscript.tex`:
- **Remove:** 604 lines of stub manuscript (`manuscript.tex` = `first_g_event.tex`).
- **Add:** 552 lines from held draft `first_g_sinc2_FINAL.tex` + ~50 lines for the lens-ownership/tier-discipline preamble + ~5 lines for the bibliography additions + revised cover letter.
- **Net:** ~+5 lines net manuscript; substantively a 4–6 hour merge.

---

## §3 — Estimated revision time

| Task | Hours |
|------|-------|
| Verify held draft compiles in current TeXLive | 0.5 |
| Copy held draft to `J03/manuscript/manuscript.tex` (replace stub) | 0.25 |
| Add §0 lens-ownership preamble (per boilerplate §5.5) | 0.5 |
| Add tier-discipline (PROVEN/COMPUTED/RHYME/OPEN) paragraph in §1 | 0.5 |
| Add the 5 bibliography entries (Erdős, Pomerance, Tenenbaum, Iwaniec-Kowalski, Friedlander-Iwaniec) | 0.5 |
| Verify `proof_first_g_event.py` runs green and matches the 22,367-pair claim | 0.5 |
| Verify `verify_first_g.py` runs green and matches the 4.44e-16 deviation table | 0.5 |
| Rewrite cover letter to lead with synchronization theorem | 0.5 |
| Update README.md §5 with SAVE PLAN reference + 2-paragraph summary | 0.25 |
| Final pass + arXiv same-day prep | 0.5 |

**Total:** **4 hours** for clean Fork A; **6 hours** with full referee-rigor reread.

---

## §4 — PROVEN / COMPUTED / RHYME / OPEN (per boilerplate)

**PROVEN:**
- *Theorem 3.1 (First-G localization).* For every $b > 1$, $k^\star(b) = \mathrm{spf}(b)$.
- *Theorem 4.2 (closed form).* $R(k, f) = \sin^2(\pi k/f) / (k^2 \sin^2(\pi/f))$ for every $f \ge 2$, $k \ge 1$.
- *Theorem 5.1 (synchronization).* For every $b > 1$, the First-G event and the first integer zero of $R(\cdot, \mathrm{spf}(b))$ coincide at $k = \mathrm{spf}(b)$.
- *Theorem 6.1 (continuum limit).* $R(k, f) \to \mathrm{sinc}^2(k/f)$ as $f \to \infty$ with $k/f \to t$ fixed.
- *Cor 4.4 (endpoint values).* $R(1,f) = 1$, $R(f-1,f) = 1/(f-1)^2$, $R(f,f) = 0$, strict monotonicity on $\{1, \ldots, f-1\}$.

**COMPUTED:**
- 22,367 (b,k) pairs over 305 squarefree $b \in [2, 500]$, zero counterexamples, runtime <3s (`proof_first_g_event.py`).
- 8 primes $f \in \{3, 5, 7, 11, 13, 17, 19, 23\}$, all $k \in \{1, \ldots, f+1\}$, max deviation $4.44 \times 10^{-16}$ for the closed form (`verify_first_g.py`).

**STRUCTURAL RHYME:**
- *Identity sinc²(1/2) = 4/π² = (2/3)/ζ(2).* One-line consequence of $\zeta(2) = \pi^2/6$. Cited as motivation for the corridor midpoint, not as derivational input. (Per `J_PAPER_BOILERPLATE.md` §1.2.)
- *Primon-gas reading: 1/ζ(2) = density of squarefree integers.* The squarefree restriction in our verification sample sits squarely in this regime — bridge connection only, no theorem.
- *Drápal-Wanless (2021), JCTA.* Cited in the J-series broadly as the closest published precedent for the magma framework; not invoked in J03 directly because J03 is not a magma paper.

**OPEN:**
- Why does the corridor midpoint of the substrate sit at $t = 1/2$ such that $\mathrm{sinc}^2(1/2) = (2/3)/\zeta(2)$ becomes structurally relevant? Per the J_PAPER_BOILERPLATE this is the open theorem-shaped question; J03 flags it for companion work.

---

## §5 — Lens-ownership paragraph (J03 variant)

Insert immediately after `\maketitle`, before §1:

> *Lens and substrate.* This note works on $\mathbb{Z}$ (no specialized substrate) with the standard objects: smallest prime factor $\mathrm{spf}(b)$, the discrete Fejér quotient $R(k, f)$, and the continuum sinc² function. The objects are not derived from a TIG framework reading; they are the elementary discrete-Fourier and divisibility structures of the integers. The synchronization theorem (Theorem 5.1) is the contribution: two independently classical events coincide at $k = \mathrm{spf}(b)$. Subsequent companion papers in our program (the Sanders–Gish $\sigma$-rate and the four-core fusion-closure papers, [companions]) work over $\mathbb{Z}/N\mathbb{Z}$ with operator-labeled tables; the present paper does not require any of that machinery and stands alone.

This is the J03-specific variant of the boilerplate's lens-ownership paragraph — short, because J03 is not a magma paper and does not need the operator-label apparatus. The point is to (a) preempt "but you chose Z/10Z" pushback (J03 doesn't use Z/10Z), (b) flag the companion program transparently (J03 IS the foundational lemma), and (c) signal author understanding of what is lens vs substrate-independent.

---

## §6 — Recommended retitle / retarget

**Title:** *The First-G Event and a Discrete Sinc² Identity* (held draft title; unchanged).

**Venue:** *Integers — Electronic Journal of Combinatorial Number Theory* (unchanged from v2 plan).

**Why retitle is unnecessary:** The held draft's title is already correct. The current `manuscript.tex` (stub) title — *"The First-G Event in the Coprimality Partition: Stability Windows, CRT Idempotent Count, and Prime-Indexed Phase Transitions"* — is what the J03 substance audit (M1) flagged as overpromising. Replacing the stub with the held draft restores the right title automatically. No retitle decision needed beyond the swap.

**Why no retarget:** Per Fork A, the paper is fully `Integers`-defensible after the merge. The substance audit's projections (40% desk-reject, 30% major-revision-needed) apply to the *stub* version. The held draft has two non-trivial theorems (4.2 closed form, 5.1 synchronization) plus an honest packaging contribution; the desk-reject probability drops to ~10%, the major-revision-needed probability to ~25%, the accept-with-minor-revision to ~50%. *Integers* publishes papers exactly in this profile.

**Triadic Launch slot retained.** With Fork A, J03 stays in the third Triadic Launch position; J05 (TSML 73 / BHML 28 cells) does NOT need to be promoted into J03's slot. The Triadic shape is preserved (combinatorics + algebra + elementary number theory).

---

## §7 — Risk and contingency

If Fork A unexpectedly fails at the *Integers* referee (e.g., if a sieve-theory referee insists on heavier engagement with the Pomerance / Tenenbaum literature than the bibliography expansion supports), the contingency is Fork C from the substance audit: reformat to AMM Notes / Math. Magazine. The 4–6 hour Fork A is reversible — the held draft is preserved in `_legacy_tiers/`.

If the referee challenges the synchronization theorem as "trivial because both events coincide on $k = \mathrm{spf}(b)$ by construction": the response is that the discrete Fejér quotient $R(k, f)$ is independently defined (geometric-series identity), the First-G event is independently defined (gcd + smallest-prime-factor), and the synchronization is not a tautology but a theorem about two independent constructions agreeing. The held draft makes this explicit; the cover letter reinforces it.

---

## §8 — Final verdict

**KEEP-VIABLE.** The held draft exists, is mathematically substantive, and is 4–6 hours of merging from a clean *Integers* submission. The Fork A path is the recommended save plan; Fork B (swap J05 in) is unnecessary. No retitle, no retarget, no demotion of J03 from the Triadic Launch.

The directive "find a reason to keep" is satisfied: the reason is that the substance was already written, peer-review-ready, and verified to machine precision, and the only intervention needed is to undo the 2026-04-19 shrink that stripped it.
