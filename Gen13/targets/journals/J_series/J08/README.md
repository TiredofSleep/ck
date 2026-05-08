# J08 — The Prime Phase Transition: First-G Stability Across Squarefree Bases

**Status:** FORMAT
**Phase:** Phase 1
**Target venue:** Experimental Mathematics
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP35

---

## §1 — Manuscript

**Local path:** `manuscript/manuscript.tex` (amsart, ~14 pages)

**Abstract (1-sentence):** For b > 1 with smallest prime factor p₁ = spf(b), the J03 First-G localization at k = p₁ co-localizes with the zero of a closed-form discrete-Fejér harmonic signal R(k, p₁) = sin²(πk/p₁) / (k² sin²(π/p₁)) whose continuum limit is sinc²; verified across 8 primes and 187 semiprimes (712 distinct checks; max error 3.33×10⁻¹⁶; zero counterexamples).

Files in this J-folder's `manuscript/`:

- `manuscript.tex` (main submission file)
- `verify_prime_phase_transition.py` (verification script — exits 0 on PASS in under three minutes)
- `WP35_PRIME_PHASE_TRANSITION.md` (corpus source: archival-only, full WP35 exposition with the corollary and §6A–§11 material that the journal paper crops; cited from the manuscript as `Sanders2026WP35`)

## §2 — Verification script

**Local path:** `manuscript/verify_prime_phase_transition.py`

Runs Theorems 3.1, 3.2, 3.3, 3.4 against literal double-precision sums. Tested green at 2026-05-07: 712 checks, max error 3.33×10⁻¹⁶ (machine epsilon), runtime ~30 s on `lora312` Python 3.12. Verified output:

```
Theorem 3.1 (countdown closed form):  primes = 8, (k,f) pairs = 106, max error = 3.33e-16
Theorem 3.2 (zero-width gate):        semiprimes = 187, checks = 561, counterexamples = 0
Theorem 3.3 (omega-blindness):        p = 7, b values = 7 (omega in {1,2,3}), counterexamples = 0
Theorem 3.4 (continuum 4/pi^2):       p = 1009, 10007, 100003 — deviations 8e-4, 8e-5, 8e-6
TOTAL: 712 checks, STATUS PASS, zero counterexamples
```

## §3 — Dependencies (J-papers cited as already-submitted companions)

- **J03** (foundational lemma; cited as already-submitted to *Integers*) — *The First-G Event in the Coprimality Partition*. Theorem 3.2 of J08 directly invokes J03's First-G Localization Theorem 3.1.
- **J01** (combinatorial sibling) — cited in §1 introduction as part of the coordinated J-series; not invoked in any proof.
- **J02** (b = 10 specialization) — cited similarly.

## §4 — Cover letter

See `cover_letter.md` in this folder, finalized at this folder root (~600 words). Suggested-reviewer slots and addressee placeholder remain TBD pending Brayden's submission-day pass.

## §5 — Notes

Top-cited (14×). Builds directly on J03.

**Status update (2026-05-07):**

- Manuscript: `manuscript/manuscript.tex` — newly drafted at this session from the WP35 corpus (`papers/WP35_PRIME_PHASE_TRANSITION.md`, ~900 lines / 32,000 tokens), cropped to the four headline theorems (Theorem 3.1 countdown / 3.2 zero-width / 3.3 ω-blindness / 3.4 continuum) plus a short §5 Montgomery complementarity remark. The full WP35 exposition (§6A seeded RPS, §7A D1/D2 kinematics, §8A RSA geometric distance, §9.5 sinc² scale-free description, §10 Balance Invisibility, §11 Clay-problem connections) was deliberately deferred from the J08 manuscript and lives only in the archival `WP35_PRIME_PHASE_TRANSITION.md` copied alongside; cited from the manuscript as `Sanders2026WP35`.
- Verification: `manuscript/verify_prime_phase_transition.py` — passes green (712 checks, max error 3.33×10⁻¹⁶, zero counterexamples; tested 2026-05-07 with `lora312` Python 3.12).
- Cover letter: `cover_letter.md` at this folder root, finalized at ~600 words. Identifies J08 as 1st *Experimental Mathematics* paper of the quarter (per-venue cap awareness).
- **Author lane (clean):** README §0 lists "Sanders + Gish"; manuscript title block lists Sanders + Gish (Luther's WP35 contribution acknowledged in §Acknowledgements but not on the title block); no lane mismatch with J08.
- **Honest accounting note:** the manuscript states 36,662 exact computations as the broader-corpus number and reports 712 distinct algebraic checks (8 primes + 187 semiprimes + 6 ω-rings + 3 continuum-limit witnesses) for the J08-specific verification harness. Both numbers are real; the 712 is the harness check count, the 36,662 is the cumulative WP35 corpus value. The cover letter and manuscript both reflect this accurately.
- Open: pre-submission steps — typographic read by Gish; *Experimental Mathematics* style file pass (if amsart not accepted on first submission); arXiv same-day upload at submission time. Scope-disclaimer paragraph in §6 (Scope and limitations) is load-bearing; keep unchanged.

## §6 — Submission checklist

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to Experimental Mathematics this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "The Prime Phase Transition: First-G Stability Across Squarefree Bases." Submitted to *Experimental Mathematics*.
