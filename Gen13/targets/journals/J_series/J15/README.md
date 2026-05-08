# J15 — A Discrete $\sinc^2$ Identity in Finite-Dimensional Quantum Mechanics

**Status:** DRAFT (with fallback flagged on per-venue cap)
**Phase:** Phase 2
**Target venue:** Journal of Mathematical Physics (preferred); *Letters in Mathematical Physics* / *J Phys A* / *Comm Math Phys* as fallbacks
**Author lane:** Sanders + Mayes
**Tier:** B (Tier 1/2 fully proved)
**WP source:** Discrete sinc² identity (Theorem 3.1 in `first_g_sinc2_FINAL.tex`); QM application is novel framing

---

## §1 — Manuscript

**Local path:** `manuscript/J15_DiscreteSinc2_QM_JMathPhys.md`

**Abstract (one paragraph).** For an integer $f \ge 2$ and $k \ge 1$, the squared overlap of a momentum eigenstate with a position-space rectangular window of size $k$ in finite-dimensional QM on $\mathbb{Z}/N\mathbb{Z}$ admits the closed form $R(k,f) = \sin^2(\pi k/f)/(k^2 \sin^2(\pi/f))$. We derive three QM-relevant consequences: (i) a finite uncertainty product, (ii) a first-zero theorem (for prime $f$, first zero at $k = f$), and (iii) the continuum limit $R(k,f) \to \sinc^2(k/f)$. We close with the synchronization with the arithmetic First-G event: for $f = \mathrm{spf}(b)$, the first integer zero of $R(\cdot, f)$ coincides with the smallest $k$ at which $\{1,\dots,k\}$ contains a non-coprime element of $\mathbb{Z}/b\mathbb{Z}$.

**Source corpus:**
- The closed-form identity (Theorem 3.1) is taken from the source paper `first_g_sinc2_FINAL.tex` (J04 / J08 corpus); the QM framing (Hilbert space on $\mathbb{Z}/N\mathbb{Z}$, momentum-position rectangular-window overlap, finite uncertainty) is novel for J15.
- The synchronization is reproduced from companions [J04, J08].

## §2 — Verification script

**Path:** Closed-form is verified at machine precision on $f \in \{3,5,7,11,13,17,19,23\}$ (max deviation $4.44 \times 10^{-16}$) by direct comparison with the literal geometric sum. The verification carries over from the J04/J08 corpus; a J15-dedicated `verify_J15_sinc2.py` could be added (TBD, would be 10 lines of `numpy`).

## §3 — Dependencies (J-papers cited as already-submitted companions)

J04 (First-G Law, *Integers*), J08 (Sinc² Zero Law, *Integers*), J13 (BB Bridge, *JMP*).

## §4 — Cover letter

See `cover_letter.md` in this folder. Drafted; finalize after Brayden's referee-rigor pass.

## §5 — Notes & Status

**Status: DRAFT (manuscript drafted; per-venue cap flag — fallback path identified).**

**Per-venue cap warning.** This is the **3rd JMP target** in the J-series (J13 1st, J14 2nd). The 2/quarter cap is reached. **Action required before submission:** decide between

1. **Defer JMP submission to Q2 next quarter** (after J13 + J14 are accepted/under review), OR
2. **Submit immediately to a fallback venue:**
    - *Letters in Mathematical Physics* (Springer) — preferred fallback (short-format note)
    - *Journal of Physics A: Mathematical and Theoretical* (IOP) — natural alternative
    - *Communications in Mathematical Physics* (Springer) — higher impact

The cover letter and README make the cap conflict explicit so Brayden can choose the venue path during the referee-rigor pass.

The paper is **Tier 1/2** (fully proved): all theorems are elementary and verified at machine precision. No conjectural content.

## §6 — Submission checklist

- [x] Manuscript .md drafted (J Math Phys-format, single file)
- [ ] LaTeX (amsart) conversion pending
- [x] Verification at machine precision (carries from J04/J08); standalone script TBD
- [x] Tier-classified central claim explicit (Tier 1/2 fully proved)
- [x] Lens-scope annotation: lens-invariant
- [x] Cover letter drafted (with summary, Why-JMP-with-fallback, suggested reviewers)
- [ ] Dependencies → cite J04, J08, J13 as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete
- [x] Per-venue cap check: **3rd JMP target — fallback to LMP / J Phys A / CMP recommended**
- [ ] Final venue decision
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Mayes, B. (2026). "A Discrete $\sinc^2$ Identity in Finite-Dimensional Quantum Mechanics." Submitted to *Journal of Mathematical Physics* (or *Letters in Mathematical Physics* as fallback per per-venue cap; see README §5).
