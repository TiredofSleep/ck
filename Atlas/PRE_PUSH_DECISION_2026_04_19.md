# Pre-Push Decision Record — Sprint 34 Tier-1 Wednesday 2026-04-22

**Date:** 2026-04-19
**Branch:** `tig-synthesis` (local only; no push without user confirmation)
**Window:** Wednesday 2026-04-22 submission slot
**Governing principle (Brayden, 2026-04-19):** *every word we choose is defined by us rigorously or by previous rigor.*

---

## §1 — The Decision in One Paragraph

**Ship 2 of 3 on Wednesday.** Pull venue 1 (sinc² zero law → Integers) because the headline theorem as written is trivial (the "p prime" qualifier does no rigorous work in the biconditional) and no sharpening is possible in the 4-day window. Ship venue 7 (ξ cosmology → JCAP) after a one-line tightening at line 313 and 6 DR2-era citation additions; DR2 sweep verdict is CLEAR. Ship venue 8 (σ-rate → JCT-A) after a ~90 minute surgery: 4 rigor fixes + macro rename + 5 quasigroup-literature citations; σ-rate audit verdict is ADJACENT (not novel stand-alone; cite Kepka 1980 / Drápal-Wanless 2021 / KSSS 2023). Thread B (Markman internalization) resolved to Scenario B (ADJACENT-ONLY — Z/10Z CRT is not a discrete model that lifts to secant-sheaf machinery; Thread B continues as explicit-coordinate companion to Markman rather than a competitor).

---

## §2 — Per-Venue Decisions

### Venue 1 — Integers — sinc² zero law — **PULL-BACK**

**Why pulled:**
The theorem as stated, `sinc²(k/p) = 0 ⟺ p|k for k ∈ {1,...,p}`, is trivially true for ANY positive integer n replacing p, because `sinc(x) = 0 ⟺ x ∈ ℤ\{0}`. The "prime" qualifier does not do rigorous work in the biconditional. An *Integers* referee will catch this on first read.

**Sharpening investigation (Agent A2, 75 min web research + direct computation):**
- No under-promoted prime-specific theorem exists in our current write-up.
- Seven candidate angles (Ramanujan sums, Gauss sums, Fejér kernel, Montgomery pair correlation, Hurwitz/Chowla-Selberg, Dirichlet character sums, Selberg-Chowla) all fail to yield a prime-specific sinc² theorem.
- The Luther Pre-Echo Theorem (WP34 §10A) closed form was independently verified to hold for ALL n, prime or composite, so it also does not provide a sharpening.
- Structural reason: analytic functions sin / sinc / csc at rational points k/n depend only on k/n as a real number; the Galois content of "n prime" does not survive projection onto the real line.

**What replaces venue 1 for the next cycle:**
Retitle and rewrite as the **First-G Event paper**. The theorem is:

> Let $b\in\mathbb{Z}_{>1}$ have prime factorization $b = p_1^{a_1}\cdots p_r^{a_r}$ with $p_1 < \cdots < p_r$. Let $G_k(b) = \{x \in \{1,\ldots,k\} : \gcd(x,b)>1\}$. Then $|G_k(b)| = 0$ for every $k < p_1$, and $|G_{p_1}(b)| = 1$ with $G_{p_1}(b) = \{p_1\}$.

This IS non-trivially prime-dependent (the smallest-prime-factor controls partition geometry uniformly across moduli $b$); not the trivial divisibility biconditional.

**Edits applied to the repo 2026-04-19 (even though pulling):**
- Line 43 of `sinc2_zero_law.tex` — remove `corridor` from `\keywords{...}` (A1 DROP fix).
- Lines 180-181 — rewrite Cor 3 proof to drop the "path / length" TIG-language (A1 DROP fix).
- Front-matter note added marking venue-1 status as HELD for next cycle.
- `Atlas/PLAN_OF_RECORD_2026_04_18.md` + `Atlas/JOURNAL_READINESS_AUDIT_2026_04_18.md` updated.
- `WP_SINC2_ZERO_LAW.md` annotated with triviality note.

**Decision document:** `Atlas/SINC2_SHARPEN_DECISION_2026_04_19.md` (Agent A2 full report).

---

### Venue 7 — JCAP — ξ cosmology — **SHIP**

**Verdict:** This is the cleanest paper of the three; zero TIG-framing leaks, zero DROPs in the gap-language audit. §7 Scope-and-Limitations is exemplary.

**Rigor edits (Agent A1):**
- Line 313 — replace "cosmologically relevant range" (hand-wavy) with a specific redshift bound: "away from a sign-changing locus in $\rho_\Xi$, which numerical integration in §6.2 confirms does not occur for $z \le z_i \approx 20$."

**Novelty edits (Agent A4 DESI DR2 sweep, 17 queries, verdict CLEAR):**
- Add 6 DR2-era citations: arXiv:2503.14738 (DR2 II), 2603.21125 (Wang+ DR2 model-independent), 2603.14693 (Adil+ DR2 V(φ) ranking), 2509.13302 (Brisbane DESI 2025 survey), 2602.05368 (Turyshev DR2 review), 2502.06929 (Bhattacharya+ thawing wφCDM benchmark).
- Replace the "residual risk" sentence in WP82 §1 lines 64-65 with audit-discharge text pointing to `Atlas/DESI_DR2_SWEEP_2026_04_19.md`.
- Camera-ready: add a one-paragraph contrast with arXiv:2603.21125 (thawing vs our freezing).

**Honest DR1-bounding note:**
DESI DR2 BAO papers released 2025-03-19 (arXiv:2503.14738). DR2 cosmology chains released 2025-10-06. DR2 spectra/redshifts still not public as of 2026-04. Our χ² = 3.1 is DR1-bounded. Recommendation for submission: label explicitly as "DR1-bounded fit; DR2 chains deferred to companion numerical note." Optional: re-run `desi_xi_optimize.py` against DR2 chains before Wednesday if time permits.

**Decision document:** `Atlas/DESI_DR2_SWEEP_2026_04_19.md` (Agent A4 full report).

---

### Venue 8 — JCT-A — σ-rate theorem — **SHIP with surgery**

**Verdict:** ADJACENT, not stand-alone novel. The object CL_N and the `(a-1)(b-1) ≡ 1 (mod N)` substitution ARE new; the rate-language "σ(N) ≤ C/N on a non-associativity measure" is established literature going back to Kepka 1980.

**Rigor edits required (Agent A1) — ~90 min work:**
1. **Lemma 1 cleanup.** Current proof is muddled on the $\varphi(N)$ vs $\varphi(N)+1$ count. Rewrite as: "There are **exactly $\varphi(N)$** solutions with $a,b\neq 0, N-1$" and prove only that single count.
2. **Theorem 1 "$C<3$" wording fix.** Current prose "sharpens factor 2 to $C<3$" is backward (the finer analysis loosens, not sharpens). Rewrite: "Allowing for the third $\ECHO$ possibility yields the conservative bound $C=3$; the union over only the two inner intermediates gives $C=2$. Numerical evidence suggests the true constant is below 2."
3. **Corollary 2 demotion.** The BBM continuum-limit corollary gestures at an embedding that isn't constructed in the paper. Demote to "Conjecture / Heuristic statement" and rewrite body to make the missing-embedding hypothesis explicit.
4. **Stray forward-reference removal.** Line 134 — delete "and our $\CL_N$ model gives an elementary family whose ECHO layer forms a reversible Markov chain with an explicit absorbing-state mass" (the chain construction is not in the paper).

**Venue-fit edits (Agent A1, optional but recommended):**
5. **Macro rename.** $\HARM \to T$, $\VOID \to Z$, $\ECHO \to E$ for JCT-A venue fit (TIG-derived names will trigger "why this name?" from a JCT-A referee; rigor unchanged).

**Novelty-positioning edits (Agent A3, literature audit, ~35 min work):**
6. Add 5 Kepka/Drápal/Wanless/KSSS `\bibitem` entries to the bibliography.
7. Add 2 paragraphs to §1 Introduction:
   - Acknowledge Kepka 1980 associative-triple program + Drápal-Wanless 2021 σ → 1 regime.
   - Cite KSSS 2023 cuboctahedra (Θ(n⁴), same 1/n order as our bound).
8. Add 1 abstract sentence noting regime distinction ("σ → 0 regime, opposite of Drápal-Wanless σ → 1 regime").

**Atlas update:** New §K in `Atlas/ATLAS_CITATIONS.md` — Non-associative combinatorics / quasigroup associativity rate.

**Decision document:** `Atlas/SIGMA_RATE_LITERATURE_AUDIT_2026_04_19.md` (Agent A3 full report) + `Atlas/GAP_LANGUAGE_AUDIT_2026_04_19.md` (Agent A1, 4 rigor items).

---

## §3 — Markman / Thread B Resolution

**Verdict (Agent A5, ~90 min):** Scenario B — ADJACENT-ONLY.

Markman's Feb 2025 breakthrough (arXiv:2502.03415 "Cycles on abelian 2n-folds of Weil type from secant sheaves on abelian n-folds") uses Orlov + Buchweitz-Flenner + Chevalley pure spinors. Our Z/10Z CRT framework is **not** a discrete model that lifts to secant-sheaf machinery. Thread B continues as:
- Explicit-coordinate companion to Markman's existence theorem on the simple Weil 4-fold A_*.
- Sprint 35b Beauville pair (A_* ↔ C_*) as the load-bearing extension toward BSD (which Markman does **not** target).

**Patches applied by Agent A5:**
- `Atlas/MASTER_ATLAS_v3_5_2026_04_18.md` line 1533 — "candidate: secant-sheaf construction, Markman 2025" superseded with internalization-scope reference.
- `Atlas/ATLAS_CITATIONS.md` §C lines 92-93 — Markman entries amended with assessment summary.
- `Gen12/targets/clay/papers/clay/WP39_HODGE.md` §6.2 + sibling copy retagged as "post-hoc shape match" with warning.
- `old/Gen10/papers/clay/WP39_HODGE.md` left as historical record (never-delete).

**Decision document:** `Atlas/MARKMAN_INTERNALIZATION_SCOPE_2026_04_19.md` (Agent A5 full report, 22 KB, ~450 lines).

---

## §4 — What We Ship Wednesday

| Venue | File | Decision | Edits before submit | Risk |
|---|---|---|---|---|
| 1 Integers | `sinc2_zero_law/` | **PULL-BACK** | Pull-back markers + 2 DROP fixes | Held for next cycle rewrite as First-G Event paper |
| 7 JCAP | `jcap_xi_cosmology/` | **SHIP** | Line 313 tighten + 6 DR2 citations + WP82 discharge | LOW — DR1-bounded note is honest framing |
| 8 JCT-A | `sigma_rate/` | **SHIP with surgery** | 4 rigor fixes + macro rename + 5 citations + 2 intro paragraphs | MEDIUM — 90 min work; ADJACENT verdict means referee will expect Kepka/Drápal cites |

---

## §5 — What Ships (final text requirements)

### Venue 7 (JCAP) pre-submit checklist
- [x] Line 313 hand-wave fixed (done in this commit)
- [x] 6 DR2 citations added to LaTeX bibliography (done)
- [x] WP82 §1 residual-risk sentence replaced with audit-discharge text (done)
- [ ] Optional: re-run `desi_xi_optimize.py` against DR2 chains (if time; otherwise keep DR1-bounded label)
- [x] Gen13/Gen12 sync byte-identical (done)

### Venue 8 (JCT-A) pre-submit checklist
- [x] Lemma 1 single-count statement + clean proof (done)
- [x] Theorem 1 "$C<3$" wording flipped (done)
- [x] Cor 2 demoted to Conjecture (done)
- [x] Line 134 stray Markov-chain sentence removed (done)
- [x] $\HARM \to T$, $\VOID \to Z$, $\ECHO \to E$ macro rename (done)
- [x] 5 Kepka/Drápal/Wanless/KSSS `\bibitem` entries (done)
- [x] 2 §1 Introduction paragraphs positioning against literature (done)
- [x] 1 abstract sentence noting σ → 0 vs σ → 1 regime (done)
- [x] Atlas §K added (done)
- [x] WP101 quasigroup-adjacent subsection added (done)
- [x] Gen13/Gen12 sync byte-identical (done)

### Venue 1 (Integers) pre-pullback checklist
- [x] Line 43 `corridor` keyword removed
- [x] Lines 180-181 Cor 3 proof rewritten
- [x] Front-matter HELD marker added
- [x] WP_SINC2_ZERO_LAW.md triviality note annotated
- [x] Replacement First-G Event theorem statement saved for next-cycle sprint
- [x] PLAN_OF_RECORD / JOURNAL_READINESS_AUDIT updated

---

## §6 — Pre-Push Posture

All edits are staged as a **single local commit on `tig-synthesis`** — no push without user confirmation. The submission cover letters for venues 7 and 8 need Brayden's final review before I prepare the submission emails. The pre-submit checks above can all be re-verified by reading the commit diff.

**Files modified in this commit (preview, may be refined):**
```
Atlas/PRE_PUSH_DECISION_2026_04_19.md                                 [NEW]
Atlas/GAP_LANGUAGE_AUDIT_2026_04_19.md                                [NEW]
Atlas/SINC2_SHARPEN_DECISION_2026_04_19.md                            [NEW]
Atlas/SIGMA_RATE_LITERATURE_AUDIT_2026_04_19.md                       [NEW]
Atlas/DESI_DR2_SWEEP_2026_04_19.md                                    [NEW]
Atlas/MARKMAN_INTERNALIZATION_SCOPE_2026_04_19.md                     [NEW by A5]
Atlas/ATLAS_CITATIONS.md                                              [§K added; §C Markman patched by A5]
Atlas/MASTER_ATLAS_v3_5_2026_04_18.md                                 [line 1533 Markman supersede by A5]
Gen13/targets/journals/tier1_submit_now/sinc2_zero_law/sinc2_zero_law.tex
Gen13/targets/journals/tier1_submit_now/jcap_xi_cosmology/jcap_xi_cosmology.tex
Gen13/targets/journals/tier1_submit_now/sigma_rate/sigma_rate_theorem.tex
Gen12/targets/journal_attempts/01_integers_number_theory/sinc2_zero_law.tex  [mirror]
Gen12/targets/journal_attempts/07_jcap_cosmology/jcap_xi_cosmology.tex       [mirror]
Gen12/targets/journal_attempts/08_sigma_rate_combinatorics/sigma_rate_theorem.tex [mirror]
Gen12/targets/journal_attempts/01_integers_number_theory/WP_SINC2_ZERO_LAW.md [triviality annotation]
Gen12/targets/journal_attempts/07_jcap_cosmology/WP82_LOG_QUINTESSENCE_NOVELTY.md [6 DR2 cites + discharge]
Gen12/targets/journal_attempts/08_sigma_rate_combinatorics/WP101_SIGMA_RATE_THEOREM.md [5 quasigroup cites]
Gen13 mirrors of the three WP*.md above                                [byte-identical]
Atlas/PLAN_OF_RECORD_2026_04_18.md                                    [venue-1 pull noted]
Atlas/JOURNAL_READINESS_AUDIT_2026_04_18.md                           [venue-1 pull noted]
```

**Commit message draft:**
```
tig-synthesis: Sprint 34 pre-push audit + 3 venue decisions (ship 2, pull 1)

- Pull venue 1 (sinc² / Integers): theorem is trivially true for any n, not prime-specific
  → ship next cycle as First-G Event paper
- Ship venue 7 (ξ / JCAP) with line 313 tightening + 6 DR2 citations
- Ship venue 8 (σ-rate / JCT-A) with surgery: 4 rigor fixes + macro rename + 5 literature citations
- Markman Thread B resolved: Scenario B (ADJACENT-ONLY) — Z/10Z CRT not a secant-sheaf lift
- Atlas audits: gap-language, sinc² sharpening, σ-rate literature, DESI DR2 sweep, Markman scope
- Gen12/Gen13 byte-identical sync preserved

Per governing principle: every word we choose is defined by us rigorously or by previous rigor.

No push without user confirmation. Cover letters for venues 7+8 ready; Brayden's final review
required before submission email is sent.
```

---

## §7 — ClaudeChat Reply (draft, for Brayden to forward or tweak)

> ClaudeChat — pre-push audit closed. Summary:
>
> **sinc² — you called it:** your triviality flag holds. `sinc²(k/p)=0 ⟺ p|k` with k ∈ {1,...,p} is true for ANY positive integer n replacing p. 75-minute research-agent investigation across 7 candidate angles (Ramanujan/Gauss/Fejér/Montgomery/Hurwitz/Dirichlet/Selberg-Chowla) yielded no prime-specific sinc² sharpening. The Luther Pre-Echo Theorem was also independently verified to hold for ALL n. Structural reason: analytic functions at rational points depend only on k/n as a real number; Galois content of "prime n" does not survive projection. **Pulled venue 1.** Next cycle ships the First-G Event paper (`|G_{p_1}(b)|=1` at the smallest prime factor of b — genuinely prime-dependent, 3-line proof, and venue-fit for Integers).
>
> **JCAP ξ — CLEAR.** 17-query DR2-era sweep found no V ∝ φ log φ prior; zero TIG-framing leaks in the .tex; §7 Scope section is exemplary. One-line tightening at line 313 + 6 DR2 citations applied. DR1-bounded χ²=3.1 labeled honestly; DR2 chains deferred to companion note. **Ships Wednesday.**
>
> **JCT-A σ-rate — ADJACENT.** Our CL_N and (a-1)(b-1) ≡ 1 substitution are new; the rate-language σ ≤ C/N on non-associativity is established (Kepka 1980, Drápal-Wanless 2021 σ → 1 opposite pole, KSSS 2023 cuboctahedra Θ(n⁴) same 1/n rate). 90-minute surgery applied: Lemma 1 clean count, Theorem 1 "$C<3$" wording flipped (it loosens, not sharpens), Cor 2 demoted to Conjecture (BBM embedding not in paper), stray Markov-chain line 134 removed, $\HARM \to T$ / $\VOID \to Z$ / $\ECHO \to E$ for venue fit, 5 Kepka/Drápal/Wanless/KSSS citations added, 2 intro paragraphs positioning against prior work. **Ships Wednesday with surgery.**
>
> **Markman Thread B — Scenario B (ADJACENT-ONLY).** arXiv:2502.03415 uses secant-sheaf / Chevalley pure spinors; Z/10Z CRT does not lift. Thread B continues as explicit-coordinate companion + Beauville BSD extension (which Markman does not target). Atlas Markman framing patched throughout.
>
> Gap-language audit fixed 3 DROPs across the three .tex files (corridor keyword in sinc²; "path/length" in Cor 3; stray Markov-chain forward-reference in σ-rate intro). All edits mirror byte-identical across Gen12 and Gen13. Single local commit on tig-synthesis; no push without Brayden's confirmation. Decision docs in `Atlas/PRE_PUSH_DECISION_2026_04_19.md` (this file) + 5 per-track audit reports.
>
> — Claude (Sprint 34 pre-push audit, 2026-04-19)

---

## §8 — Open Items / Not Fixed This Round

1. **Track 2.3 CROSSING_LEMMA_EXPORT_V1** — deferred; requires Sprint 8 AVFT + Productive Incompleteness + WP57 inputs. Not blocking Wednesday.
2. **Optional DR2 re-fit** — if Brayden wants to convert "DR1-bounded" → "DR2-confirmed" before Wednesday, run `desi_xi_optimize.py` against public DR2 chains (2025-10-06 release). ~60 min of compute + fit validation.
3. **Cover letter finalization** — venues 7 + 8 templates are in `cover_letter_template.md`; need Brayden's signature-line review before submit.
4. **Sprint 35** — First-G Event paper rewrite for next-cycle Integers submission (replaces pulled venue 1).

---

**Decision author:** Claude (Sprint 34 pre-push synthesis, 2026-04-19)
**Confidence:** HIGH on pull-venue-1; MEDIUM-HIGH on ship-venue-7; MEDIUM on ship-venue-8 (assumes 90-min surgery lands clean; I have executed it in this same commit).
**Sign-off:** Recommend Brayden review this file + the 5 per-track audit reports before Wednesday. All edits are local; nothing pushed.
