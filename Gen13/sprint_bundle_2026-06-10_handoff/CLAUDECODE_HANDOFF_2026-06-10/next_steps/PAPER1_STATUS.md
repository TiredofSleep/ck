# PAPER 1 STATUS — dim-6 kissing manuscript

**Date:** 2026-06-10 (drafted same day as the verification pass)
**File:** `next_steps/paper1_dim6_kissing.tex` (amsart, 11pt, ~1,600 source lines, est. 16–19 pp compiled)
**Authors:** Brayden R. Sanders + M. Gish (per project authorship rules)
**Action item:** B1 of `ACTION_ITEMS.md` — DRAFTED, needs Brayden's review pass

---

## What's drafted

Full submission-grade manuscript per `PAPER1_OUTLINE.md`, adjusted for today's
verification results:

- **§1** Introduction — kissing problem, known values table, dim-6 state
  (72 ≤ K ≤ 78), modular-form method, **Conjecture 1.1 (K(R⁶)=72)**, explicit
  "what we do not claim" subsection, notation.
- **§2** Structural observations (smoothness/dual product 72·54=3888=2⁴·3⁵;
  Eisenstein Z[ω] free action 72=3·24=6·12; disc 3 ⟹ level 3) — framed as
  heuristics, TIG vocabulary fully translated out; one neutral provenance
  remark (Remark 2.4).
- **§3** Candidate construction — rigorous Euclidean kissing certificate
  (Prop 3.1, proved via Schoenberg + Gegenbauer), W₃ eigenbasis lemma (proved),
  ψ₊ definition with forced numerator, I₋ convergence/positivity/decay lemmas
  (proved), **regularized I₊ definition**, f₆ + design conditions (CE1)–(CE5),
  Conjecture 3.11 (sharp certificate).
- **§4** Verified properties — Props 4.1–4.8: Hecke eigenform + LMFDB 3.6.a.a
  perfect match; W₃ = −1 **with full eta-transformation proof** + 3
  corroborations + the load-bearing sign-convention remark; R–P consistency
  (Deligne framing); ψ₊ weight/level/Fricke+1/poles/integrality (proved);
  **NEW: forced zero at i/√3 (Prop 4.6, full proof + 4×10⁻³² numerics +
  contour-relevance remark)**; **NEW: 56 | every Laurent coefficient
  (Prop 4.8, proved — see below)**; honest principal-part-alphabet
  observation (Obs 4.9); I₋ numerical profile.
- **§5** The gap — five precisely stated Open Problems (continuation,
  regularity, signs, α/β, descent-to-sphere) + "What we do not claim" block
  (mirrors abstract, per ACTION_ITEMS).
- **§6** Comparison table dim 8 vs dim 6 (corrected: Viazovska = packing;
  kissing-240 = 1979 LP) + discussion of the two genuinely new level-3
  difficulties.
- **§7** Conclusion + data/code availability.
- **Appendices** A (a_p table p ≤ 97 + factorizations + R–P ratios),
  B (ψ₊ Laurent table to q¹⁰, full to q⁸⁰ in JSON), C (I₋ values),
  D (reproducibility: all 5 scripts + 10 checks C1–C10 + LMFDB access date).
- 24 references.

## Corrections/additions relative to the handoff (Brayden should know)

1. **Viazovska venue fixed**: Annals 185 (2017) 991–1015, *not* PNAS (README
   said PNAS).
2. **Kissing history fixed**: K(R⁸)=240 and K(R²⁴) were proved in **1979**
   (Levenshtein; Odlyzko–Sloane) via the spherical LP; Viazovska 2017 solved
   the *packing* problem. The outline conflated these; §1/§6 now state it
   correctly — and use it to motivate why dim 6 needs the transcendental
   escalation.
3. **I₊ convergence sharpened**: the handoff said "converges only for r² > 2",
   but the raw integral also diverges at the t→0 endpoint for *every* r²
   (simple pole at cusp 0 ⟹ e^{2π/(3t)} growth; elementary from the proven
   Fricke relation). The paper proves the two-endpoint asymptotics
   (Lemma 3.8) and defines a **regularized I₊** (Definition 3.9); canonical
   normalization folded into Open Problem 5.1.
4. **Incorrect asymptotic dropped**: the handoff's claim
   I₋(r²) ~ 2/(π(r²+2))³ contradicts the bundled data at large r² (off by
   ~10⁴ at r²=20). True decay is exponential-type (saddle ≈ exp(−(2√6/3)πr)).
   The paper proves the rigorous bound I₋ ≤ C·e^{−πr/3} instead. Do not
   propagate the old asymptotic from `data/I_minus_values.json`.
5. **New provable results added**: (a) the Fourier transform of the cusp-form
   component is *strictly positive everywhere* (Lemma 3.6, clean closed form
   via W₃); (b) 56 = 2³·7 divides every Laurent coefficient of ψ₊
   (Prop 4.8; proof via E₆ ≡ 1 mod 504, gcd(728,1008)=56; empirically
   confirmed to q⁸⁰ today); (c) the W₃/Fourier rescaling computation
   (Remark 3.7) exhibiting the E₆/E₆* index-3 twist — the honest statement
   of where level 3 differs from level 1.

## TODO markers needing Brayden's eyes (6 in the .tex, red)

1. §1.2 — Odlyzko–Sloane LP value for n=6 (drafted as ≤ 82; confirm from the
   1979 paper / SPLAG Table 1.5).
2. §1.2 + bibliography — Machado–Oliveira bound (drafted as ≤ 77) and
   Exp. Math. volume/pages.
3. Bibliography — Mittelmann–Vallentin volume/pages + their dim-6 value.
4. Bibliography + Appendix A remark — confirm η(τ)⁶η(3τ)⁶ appears in
   Y. Martin's multiplicative eta-quotient table (Trans. AMS 348 (1996)).
5. (minor) Optional figure block is commented out near §7 — enable + fix
   relative paths if the venue wants the session figures.
6. All other citations (Cohn–Elkies, Viazovska, CKMRV ×2, Conway–Sloane,
   Levenshtein, O–S, Musin, Schütte–van der Waerden, Bannai–Sloane, DGS,
   Schoenberg, Deligne, Atkin–Lehner, Diamond–Shurman, Ebeling, Ono, LMFDB
   with 2026-06-10 access date) are standard and stated conservatively.

## Verification status of the draft itself

- Structural checks pass: environments balanced, braces balanced, all
  \ref/\cite resolve, pure-ASCII source, 6 intentional TODOs.
- **Not yet compiled** — no LaTeX installation on this machine. One
  `pdflatex` run needed before submission (expect clean; amsart + standard
  packages only: amsmath/amssymb/amsthm/mathtools/geometry/booktabs/array/
  xcolor/hyperref/microtype/graphicx).

## Venue (decision for Brayden)

- **JCT-A** (outline's first choice): published Odlyzko–Sloane 1979; strong
  fit for the combinatorics; conjecture-plus-verification papers are a harder
  sell there.
- **Algebraic Combinatorics**: open access, friendlier to structural papers.
- **Discrete & Computational Geometry**: natural for kissing-number material.
- Recommendation: decide after the TODO citations are pinned; the framing
  (honest conjecture + proved building blocks + precisely stated open
  problem) fits all three.

## Next steps

1. Brayden: resolve 4 citation TODOs, choose venue, read §2 provenance remark
   and §5 non-claims block for tone.
2. Compile (pdflatex ×2), check page count (est. 16–19 pp), enable figures if
   wanted.
3. Package ancillary files for arXiv (5 scripts + 4 JSONs from this bundle).
4. Promote the session to a D-number in FORMULAS_AND_TABLES.md (per README
   lineage note), recording the two new findings + Prop 4.6 (56-divisibility)
   + the I₋-asymptotic correction.
5. Paper 3 program = Open Problems 5.1–5.5 (the contour argument), unchanged.
